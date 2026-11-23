"""명시적 어휘 매핑과 품질 HOLD 수정을 준비해요. 과거 판정·원문은 보존해요."""
from __future__ import annotations

from copy import deepcopy
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys
import subprocess

import build_additional_24 as common
import build_pilot_24 as base

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]
OUT = COS / "outputs/corrections_20261123"
CSV = COS / "outputs/linear_conformance_20261123/controlled_vocabulary_issues.csv"
DATASETS = ("pilot_24", "additional_24", "additional_100", "additional_100_terra", "additional_100_terra2")
AFFECTED = DATASETS[2:]
RENAMES = {"syn-sol-0150": "syn-hold-0082", "syn-sol-0221": "syn-hold-0083"}
MAP = {
    "불편 없음": "none", "관찰 부위 불편 없음": "none", "현재 불편 없음": "none",
    "사용 중 불편 없음": "none", "현재 보고된 불편 없음": "none", "본인 불편 없음": "none",
    "붓기와 통증이 계속됨": "persistent", "기기 병용 때마다 통증 반복": "repeated",
    "지속 통증": "persistent", "사용 중 새로운 통증이 계속됨": "persistent",
    "persistent_swelling": "persistent", "사용 뒤 지속되는 통증": "persistent", "심한 통증": "severe",
    "현재 눈 통증이 있어요.": None, "제품 사용 후 불편 보고": None,
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup(path):
    target = OUT / "before_v2" / path.relative_to(HERE)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(path.read_bytes())


def row_hash(case):
    req = common.validator.SLMRequest.model_validate(case["request"])
    return common.validator.compute_row_content_sha256(req, case["answer"], card_ids=case["card_ids"],
        chunk_origins=case["chunk_origins"], is_hard_negative=case["is_hard_negative"], hard_negative_type=case["hard_negative_type"])


def preserve_reported_context(case):
    history = case.get("normalization_history", [])
    if not history:
        return
    obs = case["request"]["confirmed_observations"]
    previous = obs.get("skin.distribution")
    if previous and previous["state"] == "known" and isinstance(previous["value"], dict):
        value = deepcopy(previous["value"])
    else:
        value = {"previous_distribution_observation": deepcopy(previous)} if previous else {}
    statements = value.setdefault("reported_symptom_statements", [])
    for entry in history:
        report = {"source_variable": entry["variable"], "statement": entry["before"]["value"]}
        if report not in statements:
            statements.append(report)
    # 원문에 있는 부위·증상·시간은 그대로 남기며 없는 위치나 정도를 추가하지 않아요.
    obs["skin.distribution"] = base.obs("skin.distribution", value)
    if case["id"] == "syn-hold-0079":
        context = obs["routine.co_use_context"]["value"]
        for key in ("reported_product_response", "response_persistence", "response_severity"):
            context.pop(key, None)


def prepare():
    assert not (OUT / "prepared/receipt.json").exists(), "이미 준비된 수정본을 덮어쓰지 않아요."
    OUT.mkdir(parents=True, exist_ok=True)
    candidates, owners, wrappers = {}, {}, {}
    for name in AFFECTED:
        for part in "abc":
            prefix = f"{name}_part_{part}"
            ip = HERE / (prefix + "_inputs.json")
            ap = HERE / (prefix + ".json")
            inputs, authored = json.loads(ip.read_text(encoding="utf-8")), json.loads(ap.read_text(encoding="utf-8"))
            indexed = {c["id"]: c for c in inputs["cases"]}
            for c in authored["cases"]:
                assert {k: v for k, v in c.items() if k != "answer"} == indexed[c["id"]]
                candidates[c["id"]], owners[c["id"]] = deepcopy(c), prefix
            wrappers[prefix] = (inputs, authored)
    originals = deepcopy(candidates)
    changes = []
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        issues = list(csv.DictReader(stream))
    assert len(issues) == 25
    for issue in issues:
        case = candidates[issue["row_id"]]
        slot = case["request"]["confirmed_observations"][issue["variable"]]
        raw = slot["value"]
        assert raw == issue["value"] and slot["state"] == "known" and raw in MAP
        value = MAP[raw]
        before = deepcopy(slot)
        slot["value"] = value
        if value is None:
            slot.update(state="unknown", confirmed_by_user=False)
            reason = "지속·반복·일시적 불편의 구분이 원문에 없어 미상으로 유지해요. 별도 관찰의 통증과 실제 사용 사실은 보존해요."
        else:
            reason = "원문 의미가 명확한 고정 어휘로만 바꾸고 정도·원인·시점을 새로 만들지 않아요."
        if case["id"] == "syn-hold-0079":
            context = case["request"]["confirmed_observations"]["routine.co_use_context"]["value"]
            context["reported_product_response"] = raw
            context["response_persistence"] = "unknown"
            context["response_severity"] = "unknown"
        changes.append({"old_row_id": case["id"], "row_id": case["id"], "variable": issue["variable"],
                        "before": before, "after": deepcopy(slot), "reason": reason})
    hold_cases = []
    for old_id, new_id in RENAMES.items():
        case = candidates[old_id]
        case.update(id=new_id, mode="hold", pilot_bucket="hold", chunk_origins={}, is_hard_negative=False, hard_negative_type=None)
        if "B-S04" not in case["card_ids"]:
            case["card_ids"].append("B-S04")
        req = case["request"]
        req.update(mode="hold", rag_chunks=[], distractor_refs=[])
        if old_id == "syn-sol-0150":
            guidance = "표시 기한이 남아 있어도 색 또는 냄새 변화가 보고되어 해당 제품의 품질 확인 전 개별 사용 권고를 보류해요. 어느 변화인지, 원인과 실제 보호 수준은 확정하지 않아요."
        else:
            guidance = "용기 A의 정상 분리 표시는 용기 B의 새로운 비정상 냄새를 설명하지 않아요. 용기 B의 품질 확인 전 개별 사용 권고를 보류하며 용기 A까지 이상하다고 단정하지 않아요."
        req["kb_judgments"] = [{"card_id": "B-P08", "status": "hold", "guidance": guidance},
                               {"card_id": "B-S04", "status": "hold", "guidance": guidance}]
        req["allowed_evidence_refs"] = ["kb:B-P08@0.6.1", "kb:B-S04@0.6.1"] + [p["evidence_ref"] for p in req.get("product_evidence", [])]
        case["judgment_basis"] = {"kind": "authored_synthetic_case_against_KB_comparison_spec_not_engine_execution",
            "card_id": "B-S04", "comparison_spec": base.CARDS["B-S04"]["comparison_spec"],
            "supporting_card_comparison_specs": {"B-P08": base.CARDS["B-P08"]["comparison_spec"]}, "rationale": guidance}
        case["supersedes_row_id"] = old_id
        case["revision_note"] = "사용자 요청으로 품질 변화의 HOLD 조건을 반영했어요. 관찰은 추가·변경하지 않고 모드에 맞는 새 ID와 무청크 입력을 사용해요."
        case["answer"] = None
        hold_cases.append(case)
    affected_ids = {r["old_row_id"] for r in changes} | set(RENAMES)
    assert len(affected_ids) == 26
    for old_id in affected_ids:
        case = candidates[old_id]
        case["input_sha256"] = base.digest(case["request"])
        case["normalization_history"] = [r for r in changes if r["old_row_id"] == old_id]
        preserve_reported_context(case)
        case["input_sha256"] = base.digest(case["request"])
        if case["source_origin"] != "new_synthetic":
            raise AssertionError("원본 v67 관찰은 이 변경 대상이 아니에요.")
    for prefix, (inputs, authored) in wrappers.items():
        changed = any(c["id"] in affected_ids for c in authored["cases"])
        if not changed:
            continue
        backup(HERE / (prefix + "_inputs.json")); backup(HERE / (prefix + ".json"))
        revised = [candidates[c["id"]] for c in authored["cases"]]
        inputs["cases"] = [{k: v for k, v in c.items() if k != "answer"} for c in revised]
        authored["cases"] = revised
        inputs["correction_revision"] = "2026-11-23-fixed-vocabulary-and-quality-hold"
        authored["correction_revision"] = inputs["correction_revision"]
        dump(OUT / "prepared" / (prefix + "_inputs.json"), inputs)
        dump(OUT / "prepared" / (prefix + ".json"), authored)
    for name in DATASETS:
        for suffix in (".jsonl", "_plan.json", "_human_review.csv", "_review.md"):
            path = HERE / (name + suffix)
            if path.exists(): backup(path)
    for path in (HERE / "reviews").glob("*codex_independent*"):
        if path.is_file() and "history" not in path.name: backup(path)
    for path in HERE.glob("build_additional_100*.py"): backup(path)
    for path in HERE.glob("assemble_additional_100*reviews.py"): backup(path)
    initial_reviews = []
    for name in DATASETS:
        path = HERE / "reviews" / (name + "_codex_independent.jsonl")
        initial_reviews.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    history = HERE / "reviews/corrections_20261123_before.jsonl"
    assert not history.exists()
    history.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in initial_reviews), encoding="utf-8")
    dump(OUT / "hold_inputs_for_teacher.json", {"mode": "development_preview", "production_enabled": False,
        "cases": [{k: v for k, v in c.items() if k != "answer"} for c in hold_cases]})
    dump(OUT / "prepared/receipt.json", {"changed_old_ids": sorted(affected_ids), "id_mapping": RENAMES,
        "enum_changes": changes, "before_dataset_sha256": {n: sha(HERE / (n + ".jsonl")) for n in DATASETS},
        "before_content_sha256": {rid: row_hash(originals[rid]) for rid in affected_ids},
        "hold_inputs_file_sha256": sha(OUT / "hold_inputs_for_teacher.json"),
        "formal_human_review": "unreviewed", "external_cross_family_gate_satisfied": False})
    print(json.dumps({"enum_values": len(changes), "changed_rows": len(affected_ids), "hold_id_mapping": RENAMES, "active_datasets_modified": False}))


def preserve_raw():
    assert not (OUT / "prepared/raw_preservation_receipt.json").exists()
    revised = []
    for path in (OUT / "prepared").glob("*_part_?.json"):
        authored = json.loads(path.read_text(encoding="utf-8"))
        inputs_path = path.with_name(path.stem + "_inputs.json")
        inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
        for c in authored["cases"]:
            if c.get("normalization_history"):
                preserve_reported_context(c)
                c["input_sha256"] = base.digest(c["request"])
                revised.append(c["id"])
        inputs["cases"] = [{k: v for k, v in c.items() if k != "answer"} for c in authored["cases"]]
        dump(path, authored)
        dump(inputs_path, inputs)
    assert len(revised) == len(set(revised)) == 24
    dump(OUT / "prepared/raw_preservation_receipt.json", {"rows": revised,
        "scope": "enum에 담기지 않는 원래의 증상·부위·시간 보고를 skin.distribution의 원문 진술로 함께 보존했어요. 알려지지 않은 위치·정도·지속은 추가하지 않았어요.",
        "prior_review": "review_before_raw_preservation.jsonl", "active_datasets_modified": False})
    print(json.dumps({"original_reports_preserved_rows": len(revised), "active_datasets_modified": False}))


def make_row(case, model):
    req = common.validator.SLMRequest.model_validate(case["request"])
    row = {k: case[k] for k in common.ROW_KEYS}
    row["messages"] = [{"role": "system", "content": common.validator.SYSTEM_PROMPT_SOLUTION_HOLD},
        {"role": "user", "content": json.dumps(case["request"], ensure_ascii=False)},
        {"role": "assistant", "content": case["answer"]}]
    row["allowed_evidence_refs"], row["distractor_refs"] = req.allowed_evidence_refs, req.distractor_refs
    row["provenance"] = {"source_origin": "new_synthetic", "source_scenario_id": None, "source_turn_id": None,
        "generator_model": model, "critic_model": None, "critic_status": "unreviewed", "human_review": "unreviewed"}
    return row


def stage():
    receipt = json.loads((OUT / "prepared/receipt.json").read_text(encoding="utf-8"))
    answers = json.loads((OUT / "hold_answers.json").read_text(encoding="utf-8"))
    assert answers["generator_model"] == "gpt-6.1-terra"
    assert answers["frozen_input_file_sha256"] == receipt["hold_inputs_file_sha256"] == sha(OUT / "hold_inputs_for_teacher.json")
    assert set(answers["responses"]) == set(RENAMES.values())
    before_rows = {r["id"]: r for name in DATASETS for r in (json.loads(l) for l in (OUT / "before_v2" / (name + ".jsonl")).read_text(encoding="utf-8").splitlines())}
    all_cases, new_rows = {}, {}
    for name in AFFECTED:
        cases = []
        for part in "abc":
            prefix = f"{name}_part_{part}"
            location = OUT / "prepared" if (OUT / "prepared" / (prefix + ".json")).exists() else HERE
            inputs = json.loads((location / (prefix + "_inputs.json")).read_text(encoding="utf-8"))
            authored = json.loads((location / (prefix + ".json")).read_text(encoding="utf-8"))
            for c in authored["cases"]:
                if c["id"] in answers["responses"]:
                    c["answer"] = answers["responses"][c["id"]]
                    assert isinstance(c["answer"], str) and c["answer"]
                fixed = next(f for f in inputs["cases"] if f["id"] == c["id"])
                assert {k: v for k, v in c.items() if k != "answer"} == fixed
                assert c["input_sha256"] == base.digest(c["request"])
                cases.append(c)
                all_cases[c["id"]] = c
            if location != HERE:
                dump(OUT / "staged/source_parts" / (prefix + "_inputs.json"), inputs)
                dump(OUT / "staged/source_parts" / (prefix + ".json"), authored)
        order = {b: i for i, b in enumerate(("normal_guidance", "hold", "unknown_or_version", "distractor_or_defense"))}
        cases.sort(key=lambda c: (order[c["pilot_bucket"]], c["id"]))
        model = "gpt-6.1-sol" if name == "additional_100" else "gpt-6.1-terra"
        rows = [make_row(c, model) for c in cases]
        assert len(rows) == 100
        expected = {"solution": 77, "hold": 23} if name == "additional_100" else {"solution": 76, "hold": 24}
        assert Counter(r["mode"] for r in rows) == expected
        target = OUT / "staged" / (name + ".jsonl")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8"))
        new_rows.update({r["id"]: r for r in rows})
    proposals = []
    for old_id in receipt["changed_old_ids"]:
        new_id = RENAMES.get(old_id, old_id)
        c = all_cases[new_id]
        proposals.append({"old_row_id": old_id, "row_id": new_id, "before_row": before_rows[old_id],
                          "row": new_rows[new_id], "content_sha256": row_hash(c),
                          "normalization_history": c.get("normalization_history", []),
                          "change_reason": "품질 변화의 개별 사용 권고를 HOLD로 수정했어요." if old_id in RENAMES else "통제 어휘와 확인되지 않은 지속·반복 상태를 올바르게 구분했어요."})
    assert len(proposals) == 26
    (OUT / "changed_rows_for_review.jsonl").write_bytes("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in proposals).encode("utf-8"))
    dump(OUT / "staged/receipt.json", {"dataset_sha256": {n: sha(OUT / "staged" / (n + ".jsonl")) for n in AFFECTED},
        "review_rows": len(proposals), "proposal_sha256": sha(OUT / "changed_rows_for_review.jsonl"),
        "active_datasets_modified": False})
    print(json.dumps({"staged_rows": 300, "review_rows": len(proposals), "hold_answers": len(answers["responses"])}))


def publish():
    assert not (OUT / "published_receipt.json").exists(), "이미 적용한 판본을 반복 적용하지 않아요."
    prepared = json.loads((OUT / "prepared/receipt.json").read_text(encoding="utf-8"))
    staged = json.loads((OUT / "staged/receipt.json").read_text(encoding="utf-8"))
    for name, before_hash in prepared["before_dataset_sha256"].items():
        assert sha(HERE / (name + ".jsonl")) == before_hash, name
    proposals = [json.loads(l) for l in (OUT / "changed_rows_for_review.jsonl").read_text(encoding="utf-8").splitlines()]
    assert sha(OUT / "changed_rows_for_review.jsonl") == staged["proposal_sha256"]
    reviewed = [json.loads(l) for l in (OUT / "correction_reviews.jsonl").read_text(encoding="utf-8").splitlines()]
    reviewed_by_id = {r["row_id"]: r for r in reviewed}
    assert len(reviewed) == len(reviewed_by_id) == len(proposals) == 26
    for proposal in proposals:
        record = reviewed_by_id[proposal["row_id"]]
        assert record["decision"] == "PASS" and record["content_sha256"] == proposal["content_sha256"]
        assert record["critic_model"] == "gpt-6.1-terra" and not record["human_review_performed"] and not record["external_cross_family_gate_satisfied"]
        assert set(record["rule_checks"]) == {"R1_CITATION", "R2_CLINICAL", "R3_UNKNOWN_VERSION", "R4_HOLD_LEAK", "R5_INPUT_JUDGMENT", "R6_FORMAT_TONE"}
        assert all(c["decision"] == "PASS" for c in record["rule_checks"].values())
    for name in AFFECTED:
        with (HERE / (name + "_human_review.csv")).open(encoding="utf-8-sig", newline="") as f:
            assert all(r["human_review"] == "unreviewed" and not any(r.get(k) for k in ("reviewer", "reviewed_at", "notes")) for r in csv.DictReader(f)), "사람의 기록을 덮어쓰지 않아요."
    # 현재 공개된 소배치 입력·답변을 같은 고정 수정본으로 교체해요.
    for path in (OUT / "staged/source_parts").glob("*.json"):
        assert sha(HERE / path.name) == sha(OUT / "before_v2" / path.name), "작업 중 다른 변경이 있는 파일을 덮어쓰지 않아요."
    for name in AFFECTED:
        report_dir = COS / "outputs" / name
        for report in report_dir.glob("*structural.json"):
            target = OUT / "before_validation" / name / report.name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists(): target.write_bytes(report.read_bytes())
    for path in (OUT / "staged/source_parts").glob("*.json"):
        (HERE / path.name).write_bytes(path.read_bytes())
    # 과거 보호 해시는 이력으로 보존하고, 검수 완료한 새 판본의 정확한 해시로 교체해요.
    for name in AFFECTED:
        script = HERE / ("build_" + name + ".py")
        text = script.read_text(encoding="utf-8")
        for previous in AFFECTED:
            text = text.replace(prepared["before_dataset_sha256"][previous], staged["dataset_sha256"][previous])
        if name == "additional_100_terra":
            old = 'ids = {f"syn-sol-{n:04d}" for n in range(114, 191)} | {f"syn-hold-{n:04d}" for n in range(36, 59)}'
            new = 'ids = ({f"syn-sol-{n:04d}" for n in range(114, 191)} - {"syn-sol-0150"}) | {f"syn-hold-{n:04d}" for n in range(36, 59)} | {"syn-hold-0082"}'
        elif name == "additional_100_terra2":
            old = 'ids = {f"syn-sol-{n:04d}" for n in range(191, 268)} | {f"syn-hold-{n:04d}" for n in range(59, 82)}'
            new = 'ids = ({f"syn-sol-{n:04d}" for n in range(191, 268)} - {"syn-sol-0221"}) | {f"syn-hold-{n:04d}" for n in range(59, 82)} | {"syn-hold-0083"}'
        else:
            old = new = ""
        if old:
            assert old in text
            text = text.replace(old, new).replace('{"solution": 77, "hold": 23}', '{"solution": 76, "hold": 24}').replace("안내 77턴·보류 23턴", "안내 76턴·보류 24턴")
        script.write_bytes(text.encode("utf-8"))
        subprocess.run([sys.executable, "-X", "utf8", str(script)], cwd=COS, check=True)
        assert sha(HERE / (name + ".jsonl")) == staged["dataset_sha256"][name], name
    # 수정된 행에 과거 PASS를 재사용하지 않고 실제 재검수 기록으로 교체해요.
    for name in AFFECTED:
        for part in "abc":
            path = HERE / "reviews" / f"{name}_part_{part}_codex_independent.jsonl"
            records = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
            records = [reviewed_by_id.get(RENAMES.get(r["row_id"], r["row_id"]), r) for r in records]
            path.write_bytes("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8"))
    aggregate = HERE / "assemble_additional_100_reviews.py"
    text = aggregate.read_text(encoding="utf-8")
    text = text.replace('assert record["critic_model"] == common.MODEL', 'assert record["critic_model"] in {common.MODEL, "gpt-6.1-terra"}')
    text = text.replace('"critic_model": common.MODEL, "review_kind":', '"critic_model": None, "critic_models": dict(Counter(r["critic_model"] for r in reviews)), "review_kind":')
    aggregate.write_bytes(text.encode("utf-8"))
    for name in AFFECTED:
        subprocess.run([sys.executable, "-X", "utf8", str(HERE / ("assemble_" + name + "_reviews.py"))], cwd=COS, check=True)
    changed = []
    for proposal in proposals:
        changed.append({"old_row_id": proposal["old_row_id"], "row_id": proposal["row_id"],
            "before_content_sha256": prepared["before_content_sha256"][proposal["old_row_id"]],
            "content_sha256": proposal["content_sha256"], "reason": proposal["change_reason"]})
    result = {"schema_version": "20261123-spec-corrections-v1", "mode": "development_preview", "production_enabled": False,
        "id_mapping": RENAMES, "enum_values_normalized": 25, "enum_rows_normalized": 24, "changed_rows": changed,
        "before_dataset_sha256": prepared["before_dataset_sha256"],
        "after_dataset_sha256": {name: sha(HERE / (name + ".jsonl")) for name in DATASETS},
        "prior_reviews": "reviews/corrections_20261123_before.jsonl", "new_reviews": "reviews/corrections_20261123_reviews.jsonl",
        "human_review": "unreviewed", "external_cross_family_gate_satisfied": False,
        "scope": "사용자 요청에 따른 고정 어휘·HOLD 데이터 판본 수정이며 원본 KB·고정 검증기·사람의 승인 내용은 변경하지 않아요."}
    (HERE / "reviews/corrections_20261123_reviews.jsonl").write_bytes((OUT / "correction_reviews.jsonl").read_bytes())
    dump(HERE / "corrections_20261123.json", result)
    dump(OUT / "published_receipt.json", result)
    print(json.dumps({"corrected_rows": 26, "total_rows": 348, "id_mapping": RENAMES, "human_approved": 0}))


if __name__ == "__main__":
    if sys.argv[1:] == ["prepare"]:
        prepare()
    elif sys.argv[1:] == ["stage"]:
        stage()
    elif sys.argv[1:] == ["preserve-raw"]:
        preserve_raw()
    elif sys.argv[1:] == ["publish"]:
        publish()
    else:
        raise SystemExit("prepare 단계와 별도 실제 답변·재검수를 먼저 수행해요.")
