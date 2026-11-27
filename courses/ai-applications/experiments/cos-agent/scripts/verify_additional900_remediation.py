"""실제 수정 데이터·기존 PASS 해시·Wire·HardSafetyGuardrail 회귀를 대조해요."""

from __future__ import annotations

import json

from remediate_additional_900_critic import (
    BASE,
    BASE_REV,
    CRITIC,
    MASTER,
    ORIGINAL,
    UNKNOWN,
    baseline,
    digest,
    parse,
    sha,
    write,
)

from beauty_agent.guardrail.hard_guardrail import HardSafetyGuardrail
from beauty_agent.slm._citations import extract_citations
from beauty_agent.slm.prompt_builder import build_messages
from beauty_agent.v3_contracts import SLMRequest, SLMResponse


def check_guardrail(row):
    text = row["messages"][2]["content"]
    result = HardSafetyGuardrail().validate(
        SLMRequest.model_validate_json(row["messages"][1]["content"]),
        SLMResponse(
            mode=row["mode"], content=text, cited_evidence_refs=extract_citations(text)
        ),
    )
    return {"passed": result.passed, "flags": result.flags}


def main():
    before = {r["id"]: r for r in parse(baseline(MASTER))}
    after = {r["id"]: r for r in parse(MASTER.read_bytes())}
    reviews = {r["row_id"]: r for r in parse(CRITIC.read_bytes())}
    requested = parse(
        (BASE / "reviews/additional_900_recheck_18_requests.jsonl").read_bytes()
    )
    assert len(requested) == len({r["row_id"] for r in requested}) == 18
    targets = {r["row_id"] for r in requested}
    assert targets == {r["row_id"] for r in reviews.values() if r["decision"] == "FAIL"}
    for item in requested:
        assert item["content_sha256"] == digest(after[item["row_id"]])
        assert item["content_sha256"] != reviews[item["row_id"]]["content_sha256"]
    for rid, row in after.items():
        assert row["provenance"] == before[rid]["provenance"]
        assert row["provenance"]["human_review"] == "unreviewed"
        if rid not in targets:
            assert (
                digest(row) == reviews[rid]["content_sha256"]
                and reviews[rid]["decision"] == "PASS"
            )
    old = parse(ORIGINAL.read_bytes())
    old_baseline = parse(baseline(ORIGINAL))
    original_reviews = {
        r["row_id"]: r
        for r in parse((ORIGINAL.parent / "reviews/stage1_critic.jsonl").read_bytes())
    }
    assert len(original_reviews) == 900
    for a, b in zip(old, old_baseline, strict=True):
        assert (
            digest(a) == digest(b)
            and a["messages"][2] == b["messages"][2]
            and a["provenance"] == b["provenance"]
        )
        assert original_reviews[a["id"]]["decision"] == "PASS"
        assert original_reviews[a["id"]]["content_sha256"] == digest(a)
    for row in old + list(after.values()):
        req = SLMRequest.model_validate_json(row["messages"][1]["content"])
        wire = json.loads(row["messages"][1]["content"])
        assert (
            len(wire) == 6
            and "timeout_seconds" not in wire
            and "max_response_bytes" not in wire
        )
        assert wire == json.loads(build_messages(req)[1]["content"])
    guards = []
    for rid in sorted(targets):
        b, a = check_guardrail(before[rid]), check_guardrail(after[rid])
        assert a["passed"], (rid, a)
        if rid in UNKNOWN:
            assert "product_version_mismatch" in b["flags"]
            assert all(
                not ref.startswith("catalog:")
                for ref in after[rid]["allowed_evidence_refs"]
            )
        guards.append({"row_id": rid, "before": b, "after": a})
    report = {
        "base_revision": BASE_REV,
        "rows": 900,
        "original_rows": 900,
        "recheck_requests": 18,
        "original_critic_sha256": sha(CRITIC.read_bytes()),
        "original_critic_unchanged": CRITIC.read_bytes() == baseline(CRITIC),
        "unchanged_882_external_PASS_hashes_verified": True,
        "original_900_canonical_answers_approvals_unchanged": True,
        "all_1800_wire_inputs_match_runtime": True,
        "unknown_catalog_guardrail_regressions_fixed": 7,
        "corrected_18_hard_guardrail_results": guards,
        "deterministic_checks_passed": True,
        "cross_model_recheck_performed": False,
        "new_PASS_created": False,
        "additional_human_review": "unreviewed",
    }
    write(BASE / "validation/remediation_18_integrity.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
