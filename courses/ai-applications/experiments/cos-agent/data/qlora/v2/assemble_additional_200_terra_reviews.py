"""서로 다른 문맥의 감사 담당자가 작성한 실제 판정을 합칩니다."""
from __future__ import annotations

from collections import Counter
import json

import build_additional_24 as common

MODEL = "gpt-6.1-terra"
HERE = common.HERE
OUT = common.COS / "outputs/additional_200_terra"
REVIEWS = HERE / "reviews"
RULES = {"R1_CITATION", "R2_CLINICAL", "R3_UNKNOWN_VERSION", "R4_HOLD_LEAK", "R5_INPUT_JUDGMENT", "R6_FORMAT_TONE"}


def write_preserving(path, value):
    data = value.encode("utf-8")
    if path.exists() and path.read_bytes() != data:
        archive = OUT / "superseded" / (path.name + "." + common.sha(path) + ".previous")
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            archive.write_bytes(path.read_bytes())
    path.write_bytes(data)


def main():
    dataset = HERE / "additional_200_terra.jsonl"
    rows = [json.loads(line) for line in dataset.read_text(encoding="utf-8").splitlines()]
    by_id = {r["id"]: r for r in rows}
    reviews = []
    for part in "abcdef":
        path = REVIEWS / f"additional_200_terra_part_{part}_codex_independent.jsonl"
        reviews.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    assert len(reviews) == 200 and len({r["row_id"] for r in reviews}) == 200
    assert {r["row_id"] for r in reviews} == set(by_id)
    for record in reviews:
        row = by_id[record["row_id"]]
        req = common.validator.SLMRequest.model_validate_json(row["messages"][1]["content"])
        actual = common.validator.compute_row_content_sha256(req, row["messages"][2]["content"], card_ids=row["card_ids"], chunk_origins=row["chunk_origins"], is_hard_negative=row["is_hard_negative"], hard_negative_type=row["hard_negative_type"])
        assert record["content_sha256"] == actual, row["id"]
        assert record["critic_model"] == MODEL
        assert record["review_kind"] == "codex_same_family_independent"
        assert record["external_cross_family_gate_satisfied"] is False and record["human_review_performed"] is False
        assert set(record["rule_checks"]) == RULES
        assert record["decision"] in ("PASS", "FAIL")
        assert all(r["grounds"] for r in record["rule_checks"].values())
        failed_rules = [k for k, v in record["rule_checks"].items() if v["decision"] == "FAIL"]
        assert (record["decision"] == "FAIL") == bool(failed_rules)
        if failed_rules:
            assert record["violated_rule"] in failed_rules and record["offending_span"]
    reviews.sort(key=lambda r: r["row_id"])
    summary = {"dataset": "data/qlora/v2/additional_200_terra.jsonl", "dataset_sha256": common.sha(dataset),
               "critic_model": MODEL, "review_kind": "codex_same_family_independent",
               "external_cross_family_gate_satisfied": False, "human_review_performed": False,
               "total_rows": len(reviews), "pass_count": sum(r["decision"] == "PASS" for r in reviews),
               "fail_count": sum(r["decision"] == "FAIL" for r in reviews),
               "failed_rows": [r["row_id"] for r in reviews if r["decision"] == "FAIL"],
               "scope": "작성 담당과 다른 독립 문맥의 Codex 담당자가 200행의 입력·답변·카드·출처 범위 및 R1–R6를 대조했어요. 다른 모델 계열의 공식 검수와 사람 승인은 아니에요.",
               "limitations": ["등록 출처와 KB 비교 명세를 대조한 개발 검토이며 외부 원문 전체 재검증이나 임상 검증이 아니에요.", "구조 검사는 별도 보고서로 기록하며 감사 판정을 자동으로 만들지 않아요."]}
    summary["limitations"].append("기존 448턴과 추가 후보의 의미 중복은 카드·관찰 유사 후보 및 개별 확인 대상에 대해 대조했으며 모든 쌍의 의미 중복 전수 증명을 수행했다고 주장하지 않아요.")
    corrections = HERE / "corrections_new200_33_20261123.json"
    if corrections.exists():
        correction = json.loads(corrections.read_text(encoding="utf-8"))
        assert correction["dataset_sha256"] == common.sha(dataset)
        summary["raw_review_corrections"] = {
            "file": corrections.name, "file_sha256": common.sha(corrections),
            "changed_rows": correction["changed_rows"],
            "same_family_independent_pass": correction["same_family_independent_pass"],
            "scope": correction["scope"],
            "initial_reinspection": {"total_rows": 33, "pass_count": 30, "fail_count": 3},
            "explicit_synthetic_replacement": correction["explicit_synthetic_replacement"],
            "official_external_review_or_human_approval": False}
    for name in ("additional_200_terra_structural.json", "combined_648_structural.json"):
        path = OUT / name
        if corrections.exists():
            path = common.COS / "outputs/repair_new200_33_20261123" / ("final_200_structure.json" if name.startswith("additional_") else "final_648_structure.json")
        if not path.exists():
            path = OUT / ("initial_200_structural.json" if name.startswith("additional_") else "initial_648_structural.json")
        if path.exists():
            summary[name.removesuffix(".json")] = json.loads(path.read_text(encoding="utf-8"))
    history = []
    for number in (1, 2, 3):
        path = REVIEWS / f"additional_200_terra_round{number}.jsonl"
        if path.exists():
            prior = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            history.append({"file": path.name, "file_sha256": common.sha(path), "total_rows": len(prior),
                            "pass_count": sum(r["decision"] == "PASS" for r in prior),
                            "fail_count": sum(r["decision"] == "FAIL" for r in prior)})
    summary["review_history"] = history
    for path in sorted(REVIEWS.glob("additional_200_terra_part_*_round*.jsonl")):
        prior = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        summary["review_history"].append({"file": path.name, "file_sha256": common.sha(path),
            "total_rows": len(prior), "pass_count": sum(r["decision"] == "PASS" for r in prior),
            "fail_count": sum(r["decision"] == "FAIL" for r in prior)})
    write_preserving(REVIEWS / "additional_200_terra_codex_independent.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in reviews))
    write_preserving(REVIEWS / "additional_200_terra_codex_independent.summary.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("total_rows", "pass_count", "fail_count", "failed_rows")}))


if __name__ == "__main__":
    main()
