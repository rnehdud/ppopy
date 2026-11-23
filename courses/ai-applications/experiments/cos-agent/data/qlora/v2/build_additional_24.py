"""기존 파일럿을 보존하고 추가 개발 후보 24턴과 확인 자료를 조립합니다.

새로운 학습·모델 실행이나 검수 승인을 수행하지 않습니다.
입력은 두 담당자가 응답 작성 전에 저장한 입력 명세와 대조합니다.
"""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]
OUT = COS / "outputs/additional_24"
sys.path.insert(0, str(COS))
spec = importlib.util.spec_from_file_location("additional_fixed_validator", COS / "scripts/validate_qlora_dataset.py")
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)
MODEL = "gpt-6.1-sol"
BASELINE = ["pilot_24.jsonl", "pilot_24_plan.json", "pilot_24_responses.json", "pilot_24_human_review.csv"]
ROW_KEYS = ["id", "scenario_id", "group_id", "scenario_family_id", "split", "mode",
            "pilot_bucket", "domains", "card_ids", "is_hard_negative", "hard_negative_type", "chunk_origins"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def save(name, text, *, bom=False):
    target = HERE / name
    data = text.encode("utf-8-sig" if bom else "utf-8")
    if target.exists() and target.read_bytes() != data:
        previous = OUT / "superseded" / (name + "." + sha(target) + ".previous")
        previous.parent.mkdir(parents=True, exist_ok=True)
        if not previous.exists():
            previous.write_bytes(target.read_bytes())
    target.write_bytes(data)


def main():
    baseline_hashes = {name: sha(HERE / name) for name in BASELINE}
    human_path = HERE / "additional_24_human_review.csv"
    if human_path.exists():
        with human_path.open(encoding="utf-8-sig", newline="") as stream:
            prior = list(csv.DictReader(stream))
        if any(r["human_review"] != "unreviewed" or r["reviewer"] or r["reviewed_at"] or r["notes"] for r in prior):
            raise SystemExit("기록된 사람의 검수 결과를 덮어쓰지 않습니다.")
    cases = []
    for part in ("a", "b"):
        shard = json.loads((HERE / f"additional_24_part_{part}.json").read_text(encoding="utf-8"))
        inputs = json.loads((HERE / f"additional_24_part_{part}_inputs.json").read_text(encoding="utf-8"))
        frozen = {c["id"]: c for c in inputs["cases"]}
        for case in shard["cases"]:
            spec_case = {k: v for k, v in case.items() if k != "answer"}
            assert spec_case == frozen[case["id"]], "응답 작성 전 입력과 다릅니다: " + case["id"]
            cases.append(case)
    order = {b: i for i, b in enumerate(("normal_guidance", "hold", "unknown_or_version", "distractor_or_defense"))}
    cases.sort(key=lambda c: (order[c["pilot_bucket"]], c["id"]))
    ids = {f"syn-sol-{n:04d}" for n in range(19, 37)} | {f"syn-hold-{n:04d}" for n in range(7, 13)}
    assert len(cases) == 24 and {c["id"] for c in cases} == ids
    assert Counter(c["mode"] for c in cases) == {"solution": 18, "hold": 6}
    assert Counter(c["pilot_bucket"] for c in cases) == {k: 6 for k in order}
    rows = []
    hashes = {}
    korean_sentences = []
    for case in cases:
        assert case["source_origin"] == "new_synthetic"
        assert case["source_turn_id"] is None and case["source_scenario_id"] is None
        assert case["input_sha256"] == hashlib.sha256(canonical(case["request"]).encode("utf-8")).hexdigest()
        request = validator.SLMRequest.model_validate(case["request"])
        row = {k: case[k] for k in ROW_KEYS}
        row["messages"] = [
            {"role": "system", "content": validator.SYSTEM_PROMPT_SOLUTION_HOLD},
            {"role": "user", "content": json.dumps(case["request"], ensure_ascii=False)},
            {"role": "assistant", "content": case["answer"]},
        ]
        row["allowed_evidence_refs"] = request.allowed_evidence_refs
        row["distractor_refs"] = request.distractor_refs
        row["provenance"] = {"source_origin": "new_synthetic", "source_scenario_id": None,
                             "source_turn_id": None, "generator_model": case.get("generator_model", MODEL), **({k: case[k] for k in ("original_generator_model", "revision_model")} if "revision_model" in case else {}), "critic_model": None,
                             "critic_status": "unreviewed", "human_review": "unreviewed"}
        if row["mode"] == "hold":
            assert not request.rag_chunks
        for chunk in request.rag_chunks:
            if re.search(r"[\uac00-\ud7a3]", chunk.text):
                count = len(re.split(r"(?<=[.!?])\s+", chunk.text.strip()))
                assert 2 <= count <= 4, (case["id"], chunk.evidence_ref, count)
                korean_sentences.append(count)
        hashes[row["id"]] = validator.compute_row_content_sha256(
            request, case["answer"], card_ids=case["card_ids"], chunk_origins=case["chunk_origins"],
            is_hard_negative=case["is_hard_negative"], hard_negative_type=case["hard_negative_type"])
        rows.append(row)
    plan = {"schema_version": "additional-24-plan-v1", "mode": "development_preview",
            "production_enabled": False, "generator_model": MODEL,
            "human_review": "unreviewed", "original_pilot_sha256": baseline_hashes["pilot_24.jsonl"],
            "scope": "기존 24턴과 별도로 추가한 개발 후보이며 공식 검수 완료나 900턴 학습셋 착수를 뜻하지 않습니다.",
            "cases": [{k: v for k, v in c.items() if k != "answer"} for c in cases]}
    save("additional_24_plan.json", json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    save("additional_24.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    lines = ["# 추가 개발 후보 24턴 — 미검수", "",
             "기존 파일럿 24턴을 보존하고 추가한 새로운 합성 사례입니다. 기존 파일럿과 합하면 48턴입니다.",
             "안내 18턴·보류 6턴이며 네 유형이 각각 6턴입니다. 한국어 청크는 2~4문장 설명체입니다.",
             "`development_preview`, `production_enabled=false`를 유지합니다. 사람과 다른 모델 계열의 공식 검수는 미실시입니다.",
             "계획과 실제 사용, 제품 유형과 사용 사실을 구분하며, 미공개 수치·임상 효과·승인을 만들지 않습니다.",
             "방해 청크의 감사용 분류는 유지하지만 본문에서 스스로 정답·오답임을 알리는 힌트는 주지 않습니다.",
             "`synthetic_defense_probe` 본문은 합성 시험 자료이며 연결된 문헌의 실제 인용으로 취급하지 않습니다.", "",
             "## 추가 사례 목록", "", "| ID | 유형 | 사례 | 분할 |", "|---|---|---|---|"]
    for case in cases:
        lines.append(f"| {case['id']} | {case['pilot_bucket']} | {case['title']} | {case['split']} |")
    for case in cases:
        lines += ["", f"## {case['id']} — {case['title']}", "",
                  f"- 유형·분할: `{case['pilot_bucket']}` / `{case['mode']}` / `{case['split']}`",
                  f"- 내용 해시: `{hashes[case['id']]}`", "- 사람 검수: **미검수**", "",
                  "### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다", "",
                  case["judgment_basis"]["rationale"], "", "### 입력", "", "```json",
                  json.dumps(case["request"], ensure_ascii=False, indent=2), "```", "",
                  "### 응답 초안 — 미승인", "", case["answer"]]
    save("additional_24_review.md", "\n".join(lines) + "\n")
    stream = io.StringIO(newline="")
    fields = ["row_id", "content_sha256", "pilot_bucket", "reviewer", "reviewed_at", "human_review", "notes"]
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    for case in cases:
        writer.writerow({"row_id": case["id"], "content_sha256": hashes[case["id"]],
                         "pilot_bucket": case["pilot_bucket"], "reviewer": "", "reviewed_at": "",
                         "human_review": "unreviewed", "notes": ""})
    save("additional_24_human_review.csv", stream.getvalue(), bom=True)
    assert baseline_hashes == {name: sha(HERE / name) for name in BASELINE}
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {"original_pilot_files_unchanged": baseline_hashes, "additional_rows": 24,
               "modes": dict(Counter(r["mode"] for r in rows)),
               "buckets": dict(Counter(r["pilot_bucket"] for r in rows)),
               "splits": dict(Counter(r["split"] for r in rows)), "content_sha256": hashes,
               "korean_chunk_sentences": {"count": len(korean_sentences), "min": min(korean_sentences), "max": max(korean_sentences)},
               "human_approved_rows": 0, "external_critic_performed": False,
               "commit_performed": False, "push_performed": False}
    (OUT / "generation_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": 24, "original_pilot_unchanged": True, "human_approved": 0}))


if __name__ == "__main__":
    main()
