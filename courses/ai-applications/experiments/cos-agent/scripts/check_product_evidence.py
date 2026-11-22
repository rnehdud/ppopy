"""Run product-evidence health checks and write a machine-readable report."""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pydantic import ValidationError

from beauty_agent.afa.question_priority import MyopicVOIAFAPolicy
from beauty_agent.catalog_adapter import SyntheticCatalogAdapter
from beauty_agent.runtime import AgentRuntime
from beauty_agent.runtime_contracts import ProductEvidenceSelection, RuntimeTurnRequest, RuntimeTurnResponse

PRODUCT = "train-gel-cleanser-a"
VERSION = "v1.0"
MSG = "제품 설명에 있는 헹굼 안내를 확인해 주세요. 얼굴에 사용했습니다."
VAL_SHA256 = "c93110715e72b3dd925a7707fad53bc4648c585a1d78691c406592a24e6a4a67"


def require(condition, description):
    if not condition:
        raise ValueError(description)


def initial(catalog):
    runtime = AgentRuntime(catalog_adapter=catalog, afa_policy=MyopicVOIAFAPolicy(), auto_apply_nlp_features=True)
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id="health", message=MSG, profile={"confirmed": True},
        products=[{"product_id": PRODUCT, "version": VERSION, "confirmed": True}],
    ))
    return runtime, response


def lookup(runtime, target="product.instructions", version=VERSION):
    request = RuntimeTurnRequest.model_validate_json(json.dumps({
        "request_id": "health",
        "product_evidence_selection": {"product_id": PRODUCT, "version": version, "target_id": target},
    }))
    result = runtime.handle_turn(request)
    return RuntimeTurnResponse.model_validate_json(result.model_dump_json())


def expect_label(records, status, reason=None, freshness=None):
    runtime, first = initial(SyntheticCatalogAdapter(records))
    response = lookup(runtime)
    result = response.product_evidence
    require(result.status == status, f"expected {status}; got {result.status}")
    require(response.questions == first.questions, "pending question changed during evidence lookup")
    require(response.nlp is None and response.recommendation is None, "evidence lookup ran the advice path")
    if status == "found":
        require(result.freshness == freshness and result.evidence_ref.startswith("fixture:"),
                "unexpected freshness or source")
        require(not response.pending_product_evidence, "successful request was still pending")
    else:
        require(result.reason == reason and len(response.pending_product_evidence) == 1,
                "unavailable result lost its reason or pending request")
    return result.model_dump(mode="json")


def check_pending_and_retry(label):
    catalog = SyntheticCatalogAdapter({PRODUCT: label})
    runtime, _ = initial(catalog)
    for target in ("product.spf", "product.uva", "product.uva"):
        response = lookup(runtime, target)
    before = [x.target_id for x in response.pending_product_evidence]
    require(before == ["product.spf", "product.uva"], "pending requests lost or duplicated")
    catalog.records[PRODUCT]["label_fields"] = {
        "product.uva": {"label_text": "[합성 테스트] UVA 표시", "evidence_ref": "fixture:uva"}
    }
    response = lookup(runtime, "product.uva")
    after = [x.target_id for x in response.pending_product_evidence]
    require(response.product_evidence.status == "found" and after == ["product.spf"],
            "retry did not clear only the recovered item")
    return {"before": before, "after": after, "recovered": "product.uva"}


def check_request_schema():
    errors = []
    for extra in ({"target_id": "product.fake"}, {"version": 1}):
        try:
            RuntimeTurnRequest.model_validate_json(json.dumps({
                "request_id": "health", "product_evidence_selection":
                {"product_id": PRODUCT, "version": VERSION, "target_id": "product.instructions", **extra},
            }))
        except ValidationError as error:
            errors.extend(item["type"] for item in error.errors())
        else:
            raise ValueError("invalid evidence request was accepted")
    return {"invalid_requests_rejected": len(errors), "error_types": errors}


def check_data(path):
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == VAL_SHA256, "v67 val changed from the pinned snapshot")
    rows = [json.loads(line) for line in raw.decode("utf8").splitlines()]
    require(len(rows) == len({r["id"] for r in rows}) == 221, "unexpected row count or duplicate IDs")
    require(all(isinstance(r["input"]["message"], str) and r["split"] == "val_internal" for r in rows),
            "unexpected v67 record schema or split")
    return {"rows": 221, "sha256": digest, "freshness": "matches_pinned_snapshot"}


def check_regression(args):
    artifacts = {}
    for key, agent in (("baseline", args.baseline_agent_dir), ("integrated", ROOT)):
        out = args.output / key
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(args.audit_script), "--agent-dir", str(agent),
             "--validation", str(args.validation), "--output", str(out)],
            text=True, encoding="utf8", capture_output=True, timeout=90, check=False,
        )
        (args.output / f"{key}.stdout.txt").write_text(completed.stdout + completed.stderr, encoding="utf8")
        require(completed.returncode == 0, f"{key} audit exited {completed.returncode}")
        artifacts[key] = [json.loads(line) for line in (out / "cases.jsonl").read_text(encoding="utf8").splitlines()]
    before, after = artifacts.values()
    require(len(before) == len(after) == 221, "unexpected regression data length")
    changed = [b["id"] for a, b in zip(before, after, strict=True) if a != b]
    require(not changed, f"unselected flow changed: {changed}")
    replayed = [r for r in after if "status" in r.get("default", {})]
    require(len(replayed) == 179, "not all replayable rows passed the audit")
    return {"rows": len(after), "replayed": len(replayed), "excluded": len(after)-len(replayed),
            "replayed_by_expected_action": dict(Counter(r["gold_action"] for r in replayed)),
            "changed": changed, "explicit_selection_exercised": False}


def check_cli():
    prompt = "/evidence\n0\n/evidence\n1\n/quit\n"
    result = subprocess.run([sys.executable, "-X", "utf8", "-m", "beauty_agent.cli", "--offline-nlp"],
                            cwd=ROOT, input=prompt, encoding="utf8", capture_output=True, timeout=30, check=True)
    require("표시 자료 조회를 실행하지 않았습니다." in result.stdout, "cancel not displayed")
    require("출처: catalog:synthetic-cleanser-a@1.0.0" in result.stdout, "label source not displayed")
    return result.stdout


def check_explicit_v67(path, output):
    rows = [json.loads(line) for line in path.read_text(encoding="utf8").splitlines()]
    outcomes = []
    for row in rows:
        if row["output"]["action"] != "retrieve_evidence":
            continue
        target = row["output"]["target_id"]
        context = row["input"]
        snapshot = context["request_snapshot"]
        product, = snapshot["products"]
        row_result = {"id": row["id"], "target_id": target, "product_id": product["product_id"],
                      "version": product["version"]}
        try:
            selection = ProductEvidenceSelection(
                product_id=product["product_id"], version=product["version"], target_id=target,
            )
        except ValidationError:
            outcomes.append({**row_result, "tested": False, "reason": "target_not_in_poc_contract"})
            continue
        require(product["confirmed"], "fixture must use a confirmed product")
        ref = f"fixture:{row['id']}#{target}"
        label = {"version": selection.version, "label_fields": {
            target: {"label_text": "[합성 검사 자료] " + target, "evidence_ref": ref},
        }}
        results = {}
        for mode, records in (("missing", {}), ("provided_fixture", {selection.product_id: label})):
            runtime = AgentRuntime(catalog_adapter=SyntheticCatalogAdapter(records),
                                   afa_policy=MyopicVOIAFAPolicy(), auto_apply_nlp_features=True)
            runtime.handle_turn(RuntimeTurnRequest(
                request_id=row["id"], message=context["message"], profile=snapshot["profile"],
                products=snapshot["products"], observations=context["observations"],
            ))
            response = runtime.handle_turn(RuntimeTurnRequest(request_id=row["id"], product_evidence_selection=selection))
            result = RuntimeTurnResponse.model_validate_json(response.model_dump_json()).product_evidence
            require(result.selection == selection and response.recommendation is None, "selection changed or advice emitted")
            if mode == "missing":
                require(result.status == "unavailable" and result.reason == "not_found", "false label in empty catalog")
            else:
                require(result.status == "found" and result.evidence_ref == ref, "matching fixture was not returned")
            results[mode] = result.model_dump(mode="json")
        outcomes.append({**row_result, "tested": True, **results})
    (output / "explicit-v67.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in outcomes), encoding="utf8",
    )
    tested = [row for row in outcomes if row["tested"]]
    require(len(outcomes) == 22 and len(tested) == 14, "unexpected retrieval target coverage")
    return {"total": len(outcomes), "tested": len(tested), "unsupported": len(outcomes)-len(tested),
            "found_from_matching_fixture": sum(r["provided_fixture"]["status"] == "found" for r in tested),
            "unavailable_from_empty_catalog": sum(r["missing"]["status"] == "unavailable" for r in tested),
            "target_given_explicitly": True, "original_history_replayed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--audit-script", type=Path, required=True)
    parser.add_argument("--baseline-agent-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    checks = {}

    def record(name, probe):
        started = perf_counter()
        try:
            checks[name] = {"status": "pass", "observed": probe()}
        except (ValueError, AssertionError, KeyError, TypeError, OSError, subprocess.SubprocessError) as error:
            checks[name] = {"status": "fail", "error_type": type(error).__name__, "error": str(error)}
        checks[name]["seconds"] = round(perf_counter() - started, 3)

    label = {"name": "합성 테스트 제품", "version": VERSION, "label_guidance": "[합성 표시] 물로 헹굽니다.",
             "evidence_ref": "fixture:train-gel-cleanser-a@v1.0#instructions"}
    record("v67_snapshot", lambda: check_data(args.validation))
    record("input_schema", check_request_schema)
    record("correct_version", lambda: expect_label({PRODUCT: label}, "found", freshness="version_only"))
    record("missing_product", lambda: expect_label({}, "unavailable", "not_found"))
    record("wrong_version", lambda: expect_label({PRODUCT: {**label, "version": "v0.9"}},
                                                 "unavailable", "catalog_identity_or_version_mismatch"))
    record("missing_source", lambda: expect_label({PRODUCT: {**label, "evidence_ref": ""}},
                                                   "unavailable", "field_or_source_missing"))
    record("expired_label", lambda: expect_label({PRODUCT: {**label, "label_expires_at": "2000-01-01T00:00:00Z"}},
                                                   "unavailable", "expired"))
    expires = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    record("valid_dated_label", lambda: expect_label({PRODUCT: {**label, "label_expires_at": expires}},
                                                      "found", freshness="dated"))
    record("pending_targets_retry", lambda: check_pending_and_retry(label))
    if checks["v67_snapshot"]["status"] == "pass":
        record("unselected_v67_regression", lambda: check_regression(args))
        record("explicit_v67_evidence", lambda: check_explicit_v67(args.validation, args.output))
    else:
        for name in ("unselected_v67_regression", "explicit_v67_evidence"):
            checks[name] = {"status": "skipped", "reason": "v67_snapshot_failed"}
    record("cli_explicit_selection", check_cli)
    failed = [name for name, result in checks.items() if result["status"] == "fail"]
    report = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "status": "fail" if failed else "pass",
              "failed": failed, "checks": checks, "real_catalog_checked": False, "test_split_used": False}
    (args.output / "health-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf8")
    print(json.dumps({"status": report["status"],
                      "passed": sum(check["status"] == "pass" for check in checks.values()),
                      "failed": failed, "skipped": [name for name in checks if checks[name]["status"] == "skipped"]},
                     ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
