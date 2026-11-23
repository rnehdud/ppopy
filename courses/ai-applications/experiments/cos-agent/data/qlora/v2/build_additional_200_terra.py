"""추가 개발 후보 200턴을 조립하고 미검수 확인 자료를 만듭니다."""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import io
import json
import re

import build_additional_24 as common

MODEL = "gpt-6.1-terra"
HERE = common.HERE
OUT = common.COS / "outputs/additional_200_terra"
PROTECTED = {'pilot_24.jsonl': 'ae9d6420659d6cdfa3aa6ae4c8aa31431827b8aa70bf4430622dea72b66c96cd', 'additional_24.jsonl': 'fdc5f0ce2e2ac350bba3810baa5738244d8fda25a789f0abe2c05308f0aeafe6', 'additional_100.jsonl': '063007750489ee1ac5edc0e15e0128de283c9cc1b6f0c446ee25f2b47507c381', 'additional_100_terra.jsonl': '23a598a7b73d47a12d9ee4363d794e2c8e1e9b22f9caa71d7a94ae387a6a002e', 'additional_100_terra2.jsonl': '0a689600a0cf3aa460ae0d001d9d8e6928e472b774c605cabfa7e918c2de8acc', 'additional_100_terra3.jsonl': 'ee7874dcd3117bca010e6971ce6cfdaed0b4a8c94760e2bc8d24cecd3633ec43'}


def save(name, value, *, bom=False):
    path = HERE / name
    data = value.encode("utf-8-sig" if bom else "utf-8")
    if path.exists() and path.read_bytes() != data:
        archived = OUT / "superseded" / (name + "." + common.sha(path) + ".previous")
        archived.parent.mkdir(parents=True, exist_ok=True)
        if not archived.exists():
            archived.write_bytes(path.read_bytes())
    path.write_bytes(data)


def main():
    assert {name: common.sha(HERE / name) for name in PROTECTED} == PROTECTED
    human = HERE / "additional_200_terra_human_review.csv"
    if human.exists():
        with human.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                assert row["human_review"] == "unreviewed" and not any(row[k] for k in ("reviewer", "reviewed_at", "notes")), "사람의 검수 기록은 덮어쓰지 않습니다."
    cases = []
    for part in "abcdef":
        frozen = json.loads((HERE / f"additional_200_terra_part_{part}_inputs.json").read_text(encoding="utf-8"))
        authored = json.loads((HERE / f"additional_200_terra_part_{part}.json").read_text(encoding="utf-8"))
        inputs = {c["id"]: c for c in frozen["cases"]}
        assert len(inputs) == len(authored["cases"])
        for case in authored["cases"]:
            assert {k: v for k, v in case.items() if k != "answer"} == inputs[case["id"]], case["id"]
            cases.append(case)
    order = {b: i for i, b in enumerate(("normal_guidance", "hold", "unknown_or_version", "distractor_or_defense"))}
    cases.sort(key=lambda c: (order[c["pilot_bucket"]], c["id"]))
    ids = {f"syn-sol-{n:04d}" for n in range(345, 499)} | {f"syn-hold-{n:04d}" for n in range(107, 153)}
    assert len(cases) == 200 and {c["id"] for c in cases} == ids
    assert Counter(c["mode"] for c in cases) == {"solution": 154, "hold": 46}
    rows, hashes = [], {}
    sentence_counts = []
    for c in cases:
        assert c["source_origin"] == "new_synthetic" and c["source_turn_id"] is None and c["source_scenario_id"] is None
        assert c["input_sha256"] == hashlib.sha256(common.canonical(c["request"]).encode("utf-8")).hexdigest()
        req = common.validator.SLMRequest.model_validate(c["request"])
        assert c["mode"] != "hold" or not req.rag_chunks
        for chunk in req.rag_chunks:
            if re.search(r"[\uac00-\ud7a3]", chunk.text):
                count = len(re.split(r"(?<=[.!?])\s+", chunk.text.strip()))
                assert 2 <= count <= 4, (c["id"], count)
                sentence_counts.append(count)
        row = {k: c[k] for k in common.ROW_KEYS}
        row["messages"] = [
            {"role": "system", "content": common.validator.SYSTEM_PROMPT_SOLUTION_HOLD},
            {"role": "user", "content": json.dumps(c["request"], ensure_ascii=False)},
            {"role": "assistant", "content": c["answer"]},
        ]
        row["allowed_evidence_refs"], row["distractor_refs"] = req.allowed_evidence_refs, req.distractor_refs
        row["provenance"] = {"source_origin": "new_synthetic", "source_scenario_id": None, "source_turn_id": None,
                             "generator_model": c.get("generator_model", MODEL), **({k: c[k] for k in ("original_generator_model", "revision_model")} if "revision_model" in c else {}), "critic_model": None, "critic_status": "unreviewed", "human_review": "unreviewed"}
        rows.append(row)
        hashes[c["id"]] = common.validator.compute_row_content_sha256(req, c["answer"], card_ids=c["card_ids"], chunk_origins=c["chunk_origins"], is_hard_negative=c["is_hard_negative"], hard_negative_type=c["hard_negative_type"])
    plan = {"schema_version": "additional-200-terra-plan-v1", "mode": "development_preview", "production_enabled": False,
            "generator_model": MODEL, "human_review": "unreviewed", "protected_datasets": PROTECTED,
            "scope": "사용자가 요청한 추가 개발 후보이며 24턴 공식 인수나 900턴 본 학습셋 착수를 뜻하지 않습니다.",
            "cases": [{k: v for k, v in c.items() if k != "answer"} for c in cases]}
    save("additional_200_terra_plan.json", json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    save("additional_200_terra.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    lines = ["# 추가 개발 후보 200턴", "", "기존 448턴을 변경하지 않고 추가한 안내 154턴·보류 46턴입니다. 합계는 648턴입니다.",
             "`development_preview`, `production_enabled=false`이며 실제 사용자 자료나 임상 정답이 아닙니다.",
             "작성 담당과 별도 문맥의 Codex 감사 담당을 분리합니다. 동일 GPT 계열의 감사는 다른 모델 계열의 공식 검수나 사람 승인을 대체하지 않습니다.",
             "사람 검수는 미검수이며, 현재 감사 판정은 `reviews/additional_200_terra_codex_independent.*`에서 내용 해시와 함께 확인합니다.",
             "합성 방어 청크는 실제 문헌 인용문이 아니며 감사용 출처 분류를 유지합니다. KB 판정 근거는 비교 명세를 대조한 작성 기록이지 엔진 실행 결과가 아닙니다.", "",
             "## 사례 목록", "", "| ID | 유형 | 사례 | 분할 |", "|---|---|---|---|"]
    for c in cases:
        lines.append(f"| {c['id']} | {c['pilot_bucket']} | {c['title']} | {c['split']} |")
    for c in cases:
        lines += ["", f"## {c['id']} — {c['title']}", "", f"- 유형·분할: `{c['pilot_bucket']}` / `{c['mode']}` / `{c['split']}`",
                  f"- 내용 해시: `{hashes[c['id']]}`", "- 사람 검수: **미검수**", "", "### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다", "",
                  c["judgment_basis"]["rationale"], "", "### 입력", "", "```json", json.dumps(c["request"], ensure_ascii=False, indent=2), "```", "",
                  "### 응답 초안 — 미승인", "", c["answer"]]
    save("additional_200_terra_review.md", "\n".join(lines) + "\n")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["row_id", "content_sha256", "pilot_bucket", "reviewer", "reviewed_at", "human_review", "notes"])
    writer.writeheader()
    for c in cases:
        writer.writerow({"row_id": c["id"], "content_sha256": hashes[c["id"]], "pilot_bucket": c["pilot_bucket"], "reviewer": "", "reviewed_at": "", "human_review": "unreviewed", "notes": ""})
    save("additional_200_terra_human_review.csv", stream.getvalue(), bom=True)
    assert {name: common.sha(HERE / name) for name in PROTECTED} == PROTECTED
    receipt = {"protected_datasets_unchanged": PROTECTED, "additional_rows": len(rows),
               "modes": dict(Counter(r["mode"] for r in rows)), "buckets": dict(Counter(r["pilot_bucket"] for r in rows)),
               "splits": dict(Counter(r["split"] for r in rows)), "content_sha256": hashes,
               "korean_chunk_sentences": {"count": len(sentence_counts), "min": min(sentence_counts), "max": max(sentence_counts)},
               "human_approved_rows": 0, "external_cross_family_gate_satisfied": False, "commit_performed": False, "push_performed": False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "generation_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("additional_rows", "modes", "buckets", "splits")}))


if __name__ == "__main__":
    main()
