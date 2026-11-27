"""추가 900턴 조립·원문 대조. 내용 검수나 사람 승인을 대신하지 않아요."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from validate_qlora_dataset import compute_row_content_sha256

from beauty_agent.v3_contracts import SLMRequest

BASE = COS / "data/qlora/v2/additional_900_20261126"
INVARIANTS = {
    "mode": "development_preview",
    "production_enabled": False,
    "requires_approval": True,
    "saved": False,
}


def read_rows(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write(path, value, *, lines=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in value)
        if lines
        else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def identity_blind(req):
    """제품 식별자·버전·검색 순서만 바꾼 입력은 새로운 사례로 세지 않아요."""
    obj = deepcopy(req)
    obj.pop("timeout_seconds", None)
    obj.pop("max_response_bytes", None)
    obj["rag_chunks"] = sorted(
        obj.get("rag_chunks", []), key=lambda c: c["evidence_ref"]
    )
    obj["allowed_evidence_refs"] = sorted(
        r for r in obj.get("allowed_evidence_refs", []) if not r.startswith("catalog:")
    )
    obj["distractor_refs"] = sorted(obj.get("distractor_refs", []))
    for product in obj.get("product_evidence", []):
        for key in ("product_id", "version", "evidence_ref"):
            product.pop(key, None)
    return canonical(obj)


def factual_text(req):
    """검색 문헌·행 ID를 제외한 관찰/표시 값. 유사도는 사람 확인 후보이지 의미 판정이 아니에요."""

    def values(value):
        if isinstance(value, dict):
            return " ".join(
                values(v)
                for k, v in sorted(value.items())
                if k
                not in {
                    "variable_id",
                    "source",
                    "confirmed_by_user",
                    "product_id",
                    "version",
                    "evidence_ref",
                    "synthetic_product",
                }
            )
        if isinstance(value, list):
            return " ".join(values(v) for v in value)
        return str(value)

    return (
        re.sub(
            r"\s+",
            " ",
            values(req.get("confirmed_observations", {}))
            + " "
            + values(req.get("product_evidence", [])),
        )
        .strip()
        .casefold()
    )


def shingles(text):
    text = re.sub(r"[\W\d_]+", "", text)
    return {text[i : i + 3] for i in range(max(0, len(text) - 2))}


def nearest_candidates(all_rows, new_ids):
    requests = [json.loads(r["messages"][1]["content"]) for r in all_rows]
    texts = [factual_text(r) for r in requests]
    grams = [shingles(t) for t in texts]
    inverted = defaultdict(set)
    for i, parts in enumerate(grams):
        for part in parts:
            inverted[part].add(i)
    results = []
    for i, row in enumerate(all_rows):
        if row["id"] not in new_ids:
            continue
        shared = Counter(j for part in grams[i] for j in inverted[part] if j != i)
        scored = []
        for j, intersection in shared.items():
            if row["mode"] != all_rows[j]["mode"]:
                continue
            union = len(grams[i]) + len(grams[j]) - intersection
            score = intersection / union if union else 0
            if score >= 0.40:
                scored.append((score, j))
        for score, j in sorted(scored, reverse=True)[:3]:
            other = all_rows[j]
            results.append(
                {
                    "row_id": row["id"],
                    "nearest_id": other["id"],
                    "char_trigram_jaccard": score,
                    "cross_split": row["split"] != other["split"],
                    "family_id": row["scenario_family_id"],
                    "nearest_family_id": other["scenario_family_id"],
                    "context_raw": texts[i],
                    "nearest_context_raw": texts[j],
                    "status": "내용·의미 가족 중복 확인 후보 — 자동 FAIL/PASS 아님",
                }
            )
    return sorted(
        results,
        key=lambda r: (r["cross_split"], r["char_trigram_jaccard"]),
        reverse=True,
    )


def inspect(rows, old, pool):
    errors, requests = [], []
    seen, blind, facts, answers = (
        defaultdict(list),
        defaultdict(list),
        defaultdict(list),
        defaultdict(list),
    )
    sentences = defaultdict(set)
    family_splits, group_splits = defaultdict(set), defaultdict(set)
    pool_refs, english, high_risk = set(), 0, []
    ids = [r["id"] for r in rows]
    for key, count in Counter(ids).items():
        if count != 1:
            errors.append(f"중복 ID {key}: {count}")
    expected = {f"syn-sol-{i:04d}" for i in range(691, 1381)} | {
        f"syn-hold-{i:04d}" for i in range(211, 421)
    }
    if set(ids) != expected:
        errors.append(
            f"추가 배정 ID 불일치: 누락 {sorted(expected - set(ids))}, 초과 {sorted(set(ids) - expected)}"
        )
    for row in old + rows:
        req = SLMRequest.model_validate_json(row["messages"][1]["content"])
        obj = req.model_dump(mode="json")
        seen[canonical(obj)].append(row["id"])
        blind[identity_blind(obj)].append(row["id"])
        facts[(row["mode"], factual_text(obj))].append(row["id"])
        answer = row["messages"][2]["content"]
        answers[re.sub(r"\s+", " ", answer).strip()].append(row["id"])
        family_splits[row["scenario_family_id"]].add(row["split"])
        group_splits[row["group_id"]].add(row["split"])
        if row["id"] not in set(ids):
            continue
        prov = row["provenance"]
        if (
            prov.get("source_origin") != "new_synthetic"
            or prov.get("source_scenario_id") is not None
            or prov.get("source_turn_id") is not None
        ):
            errors.append(row["id"] + ": 신규 합성 계보 위반")
        if prov.get("human_review") != "unreviewed":
            errors.append(row["id"] + ": 사람 미검수 상태가 아니에요")
        if row.get("runtime_invariants") != INVARIANTS:
            errors.append(row["id"] + ": 런타임 불변식 메타데이터 불일치")
        if "kb_judgments" in obj or "[kb:" in answer:
            errors.append(row["id"] + ": KB 혼입")
        if row["mode"] == "hold" and (
            req.rag_chunks or req.allowed_evidence_refs or req.distractor_refs
        ):
            errors.append(row["id"] + ": HOLD 문헌/근거 목록이 비어 있지 않아요")
        for chunk in req.rag_chunks:
            c = chunk.model_dump(mode="json")
            if pool.get(chunk.evidence_ref) != c:
                errors.append(
                    row["id"] + ": 공식 청크 필드 불일치 " + chunk.evidence_ref
                )
            if row["chunk_origins"].get(chunk.evidence_ref) != "reference_excerpt":
                errors.append(row["id"] + ": 풀 청크 출처 유형 불일치")
            pool_refs.add(chunk.evidence_ref)
        for ref in req.allowed_evidence_refs + req.distractor_refs:
            if ref.startswith("ref:") and ref not in pool:
                errors.append(row["id"] + ": 공식 풀 이외 문헌 ID")
        if row["mode"] == "solution" and any(
            c.evidence_ref in req.allowed_evidence_refs
            and len(re.findall(r"\b[A-Za-z]{2,}\b", c.text)) >= 8
            for c in req.rag_chunks
        ):
            english += 1
        context = req.confirmed_observations.get("constraints.decision_context")
        if (
            context
            and context.state == "known"
            and isinstance(context.value, str)
            and len(context.value) > 35
        ):
            errors.append(row["id"] + ": decision_context 35자 초과")
        if (
            row["mode"] == "hold"
            or row["hard_negative_type"] == "version_mismatch_or_unknown"
        ):
            high_risk.append(row["id"])
        for sentence in re.split(r"(?<=[.!?])\s+", re.sub(r"\[[^\]]+\]", "", answer)):
            sentence = re.sub(r"### [^\n]+\n?", "", sentence).strip()
            if len(sentence) >= 25:
                sentences[sentence].add(row["id"])
        requests.append(
            {
                "row_id": row["id"],
                "content_sha256": compute_row_content_sha256(
                    req,
                    answer,
                    card_ids=row.get("card_ids", []),
                    chunk_origins=row["chunk_origins"],
                    is_hard_negative=row["is_hard_negative"],
                    hard_negative_type=row["hard_negative_type"],
                ),
                "mode": row["mode"],
                "request": obj,
                "assistant": answer,
                "card_ids": row.get("card_ids", []),
                "chunk_origins": row["chunk_origins"],
                "is_hard_negative": row["is_hard_negative"],
                "hard_negative_type": row["hard_negative_type"],
                "generator_model": prov["generator_model"],
                "runtime_invariants": row["runtime_invariants"],
            }
        )
    new_ids = set(ids)
    duplicates = {}
    for name, mapping in [
        ("canonical_input", seen),
        ("identity_blind_input", blind),
        ("retrieval_blind_factual_context", facts),
        ("full_answer", answers),
    ]:
        duplicates[name] = [
            v for v in mapping.values() if len(v) > 1 and new_ids.intersection(v)
        ]
        # Same facts with a different retrieval bundle may be a legitimate ablation;
        # this dataset is NOT an ablation. Record for review rather than pretend novelty.
        if duplicates[name] and name != "retrieval_blind_factual_context":
            errors.append(f"기존+추가 자료에서 {name} 중복 {len(duplicates[name])}개")
    for label, mapping in [("family", family_splits), ("group", group_splits)]:
        for key, splits in mapping.items():
            if len(splits) > 1:
                errors.append(f"기존+추가 {label} 교차 분할 누수 {key}")
    modes = Counter(r["mode"] for r in rows)
    if modes != {"solution": 690, "hold": 210}:
        errors.append(f"모드 분포 불일치 {dict(modes)}")
    splits = Counter(r["split"] for r in rows)
    val_ratio = splits["val_internal"] / len(rows) if rows else 0
    if not 0.07 <= val_ratio <= 0.13 or splits["train"] == 0:
        errors.append(f"가이드의 7~13% 검증 분할 범위 위반 {dict(splits)}")
    report = {
        "scope": "구조·원문 일치·중복 후보. 자동 결과는 의미 검수 또는 사람 승인이 아니에요.",
        "rows": len(rows),
        "modes": dict(modes),
        "splits": dict(splits),
        "hard_negative_types": dict(
            Counter(r["hard_negative_type"] for r in rows if r["is_hard_negative"])
        ),
        "english_supported_solutions": english,
        "used_pool_refs": len(pool_refs),
        "duplicates_against_original_and_new": duplicates,
        "repeated_sentences_at_least_5": [
            {"sentence": s, "row_ids": sorted(v), "count": len(v)}
            for s, v in sentences.items()
            if len(v) >= 5
        ],
        "high_risk_rows": high_risk,
        "required_human_review_minimum": math.ceil(len(high_risk) / 10),
        "human_review_approved": 0,
        "training_approved": False,
        "errors": errors,
        "error_count": len(errors),
        "passed": not errors,
    }
    return report, requests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--partial", action="store_true", help="작성 중 배치 수와 행 수만 확인해요"
    )
    parser.add_argument(
        "--nearest",
        action="store_true",
        help="검색 문헌·제품 ID를 제외한 유사 맥락 후보를 추가해요",
    )
    args = parser.parse_args()
    paths = sorted((BASE / "batches").glob("*.jsonl"))
    rows = [r for path in paths for r in read_rows(path)]
    if args.partial:
        print(
            json.dumps(
                {
                    "batches": len(paths),
                    "rows": len(rows),
                    "modes": dict(Counter(r["mode"] for r in rows)),
                },
                ensure_ascii=False,
            )
        )
        return 0
    if len(paths) != 30 or len(rows) != 900:
        raise ValueError(f"배치 30개/900행 필요, 현재 {len(paths)}/{len(rows)}")
    original = COS / "data/qlora/v2/qlora_solution_hold_v2.jsonl"
    plan = json.loads((BASE / "plan.json").read_text(encoding="utf-8"))
    if sha(original) != plan["original_dataset_sha256"]:
        raise ValueError(
            "기존 승인 데이터가 작업 도중 변경됐어요. 덮어쓰지 말고 재확인하세요."
        )
    pool = {c["evidence_ref"]: c for c in read_rows(COS / "data/rag/chunks.jsonl")}
    old = read_rows(original)
    rows.sort(key=lambda r: (r["mode"] != "solution", r["id"]))
    report, requests = inspect(rows, old, pool)
    output = BASE / "qlora_solution_hold_additional_900.jsonl"
    write(output, rows, lines=True)
    if b"\r" in output.read_bytes() or output.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF8 BOM없음/LF 위반")
    report["dataset_sha256"] = sha(output)
    report["original_dataset_sha256"] = sha(original)
    report["pool_sha256"] = sha(COS / "data/rag/chunks.jsonl")
    write(BASE / "validation/quality.json", report)
    write(BASE / "reviews/critic_requests.jsonl", requests, lines=True)
    for i in range(0, len(requests), 30):
        write(
            BASE / f"reviews/requests/batch_{i // 30 + 1:02d}.jsonl",
            requests[i : i + 30],
            lines=True,
        )
    write(
        BASE / "reviews/request_manifest.json",
        {
            "rows": len(requests),
            "batches": 30,
            "dataset_sha256": sha(output),
            "requests_sha256": sha(BASE / "reviews/critic_requests.jsonl"),
            "critic_completed": False,
            "human_approved": False,
            "row_hashes": {r["row_id"]: r["content_sha256"] for r in requests},
        },
    )
    if args.nearest:
        write(
            BASE / "validation/semantic_overlap_candidates.json",
            nearest_candidates(old + rows, {r["id"] for r in rows}),
        )
    print(
        json.dumps(
            {
                k: v
                for k, v in report.items()
                if k
                not in {
                    "high_risk_rows",
                    "duplicates_against_original_and_new",
                    "repeated_sentences_at_least_5",
                }
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return int(bool(report["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
