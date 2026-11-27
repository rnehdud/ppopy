"""e14f625 원본을 보존하며 Critic FAIL 18건과 Wire 전송 키만 수정해요."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
ROOT = COS.parents[3]
sys.path.insert(0, str(COS))
from beauty_agent.slm.prompt_builder import build_messages
from beauty_agent.v3_contracts import SLMRequest
from scripts.validate_qlora_dataset import compute_row_content_sha256

BASE_REV = "e14f625"
BASE = COS / "data/qlora/v2/additional_900_20261126"
MASTER = BASE / "qlora_solution_hold_additional_900.jsonl"
ORIGINAL = COS / "data/qlora/v2/qlora_solution_hold_v2.jsonl"
CRITIC = BASE / "reviews/additional_900_critic.jsonl"
UNKNOWN = {
    "syn-sol-1159": "ref:sun_protection-014",
    "syn-sol-1250": "ref:sun_protection-005",
    "syn-sol-1263": "ref:sun_protection-008",
    "syn-sol-1268": "ref:sun_protection-009",
    "syn-sol-1330": "ref:storage_label-010",
    "syn-sol-1331": "ref:storage_label-011",
    "syn-sol-1375": "ref:storage_label-020",
}
REPLACEMENTS = {
    "syn-sol-0916": [
        (
            "현재 세정제의 실제 함유 여부는 확인되지 않았어요.",
            "특정 제품에 실제로 함유되어 있는지와 표시 품목 정보는 확인되지 않았어요.",
        )
    ],
    "syn-sol-0997": [
        ("정해진 제품과 기기 측정으로", "정해진 제품과 시점에서 수분 지표(%H) 측정으로")
    ],
    "syn-sol-1013": [("정해진 기제·부위·시점 비교", "정해진 기제와 측정 시점 비교")],
    "syn-sol-1019": [
        (
            "시험 부위를 바꾼 사용에 기제 순위를 그대로 옮기지 않아요.",
            "제시된 기제 비교를 얼굴 사용 결과로 그대로 옮기지 않아요.",
        ),
        (
            "건강한 참여자의 특정 부위·기제·시점에서 얻은 결과라는 조건이 있어요.",
            "건강한 참여자에서 시험한 기제와 측정 시점에 한정된 결과라는 조건이 있어요.",
        ),
    ],
    "syn-sol-1044": [
        (
            "물과 섞여 보이는 모습을 유화 구조의 확정 자료로 쓰지 않아요.",
            "물과 잘 섞이지 않아 보이는 모습만으로 유화 구조를 확정하지 않아요.",
        )
    ],
    "syn-sol-1157": [
        ("분사를 마쳤다는 이유만으로", "이미 도포를 마쳤다는 이유만으로"),
        (
            "이 안내는 분사하는 순간뿐 아니라 바른 채 화염 근처에 있었던 사고도 다루므로 분사 종료와 화염 안전을 같다고 보지 않아요.",
            "문헌은 인화성 경고가 있는 제품을 화염 근처에서 사용하지 않도록 안내하며, 바른 채 화염 근처에 있었던 사고도 다뤄요.",
        ),
    ],
    "syn-hold-0219": [("턱의 새로운 변화와 통증", "턱의 부풀어 오른 작은 병변과 통증")],
    "syn-hold-0273": [("개별 세안 권고를 보류해요.", "개별 권고를 보류해요.")],
    "syn-hold-0274": [("개별 세안 안내를 보류해요.", "개별 안내를 보류해요.")],
    "syn-hold-0277": [("개별 세안 권고를 보류해요.", "개별 권고를 보류해요.")],
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def baseline(path):
    return subprocess.check_output(
        ["git", "show", f"{BASE_REV}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT
    )


def parse(raw):
    return [
        json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()
    ]


def jsonl(rows):
    return ("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)).encode(
        "utf-8"
    )


def write(path, value, *, lines=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (
        jsonl(value)
        if lines
        else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    path.write_bytes(raw)


def digest(row):
    return compute_row_content_sha256(
        SLMRequest.model_validate_json(row["messages"][1]["content"]),
        row["messages"][2]["content"],
        card_ids=row.get("card_ids", []),
        chunk_origins=row["chunk_origins"],
        is_hard_negative=row["is_hard_negative"],
        hard_negative_type=row["hard_negative_type"],
    )


def request(row):
    return {
        "row_id": row["id"],
        "content_sha256": digest(row),
        "mode": row["mode"],
        "request": json.loads(row["messages"][1]["content"]),
        "assistant": row["messages"][2]["content"],
        "card_ids": row.get("card_ids", []),
        "chunk_origins": row["chunk_origins"],
        "is_hard_negative": row["is_hard_negative"],
        "hard_negative_type": row["hard_negative_type"],
        "generator_model": row["provenance"]["generator_model"],
        "runtime_invariants": row["runtime_invariants"],
    }


def main():
    old_raw, original_raw, critic_raw = (
        baseline(MASTER),
        baseline(ORIGINAL),
        baseline(CRITIC),
    )
    assert CRITIC.read_bytes() == critic_raw, "원본 외부 Critic 파일을 덮어쓰지 않아요."
    old, original, critiques = parse(old_raw), parse(original_raw), parse(critic_raw)
    by_id = {r["id"]: r for r in old}
    reviews = {r["row_id"]: r for r in critiques}
    target_ids = set(UNKNOWN) | set(REPLACEMENTS) | {"syn-sol-0695"}
    assert len(old) == len(reviews) == 900 and len(target_ids) == 18
    assert {r["row_id"] for r in critiques if r["decision"] == "FAIL"} == target_ids
    assert Counter(r["decision"] for r in critiques) == {"PASS": 882, "FAIL": 18}
    for row in old:
        assert digest(row) == reviews[row["id"]]["content_sha256"], row["id"]
    new = deepcopy(old)
    revised = {r["id"]: r for r in new}
    for rid in target_ids:
        row = revised[rid]
        if rid == "syn-sol-0695":
            row["is_hard_negative"] = False
            row["hard_negative_type"] = None
        elif rid in UNKNOWN:
            req = json.loads(row["messages"][1]["content"])
            catalog = [
                p["evidence_ref"]
                for p in req["product_evidence"]
                if p["status"] == "unknown"
            ]
            assert len(catalog) == 1 and UNKNOWN[rid] in req["allowed_evidence_refs"]
            token = "[" + catalog[0] + "]"
            assert row["messages"][2]["content"].count(token) == 1
            row["messages"][2]["content"] = row["messages"][2]["content"].replace(
                token, "[" + UNKNOWN[rid] + "]"
            )
            # 미확인 제품은 미상 그대로 보존하고, 인용 허용 목록에서만 제외해요.
            req["allowed_evidence_refs"] = [
                r for r in req["allowed_evidence_refs"] if r not in catalog
            ]
            row["allowed_evidence_refs"] = req["allowed_evidence_refs"]
            row["messages"][1]["content"] = json.dumps(
                req, ensure_ascii=False, separators=(",", ":")
            )
        else:
            for before, after in REPLACEMENTS[rid]:
                text = row["messages"][2]["content"]
                assert text.count(before) == 1, (rid, before)
                row["messages"][2]["content"] = text.replace(before, after)
    wire_log = []
    for label, rows in [("original_900", original), ("additional_900", new)]:
        for row in rows:
            req = json.loads(row["messages"][1]["content"])
            removed = {
                k: req[k] for k in ("timeout_seconds", "max_response_bytes") if k in req
            }
            if removed:
                before_hash = digest(row)
                for key in removed:
                    req.pop(key)
                row["messages"][1]["content"] = json.dumps(
                    req, ensure_ascii=False, separators=(",", ":")
                )
                assert digest(row) == before_hash, row["id"]
                wire_log.append(
                    {
                        "dataset": label,
                        "row_id": row["id"],
                        "removed": removed,
                        "canonical_content_sha256": before_hash,
                        "canonical_content_unchanged": True,
                    }
                )
            built = build_messages(
                SLMRequest.model_validate_json(row["messages"][1]["content"])
            )
            assert json.loads(built[1]["content"]) == json.loads(
                row["messages"][1]["content"]
            ), row["id"]
    assert Counter(r["dataset"] for r in wire_log) == {
        "original_900": 300,
        "additional_900": 300,
    }
    assert {r["id"] for r in new if digest(r) != digest(by_id[r["id"]])} == target_ids
    assert all(
        digest(a) == digest(b)
        and a["messages"][2] == b["messages"][2]
        and a["provenance"] == b["provenance"]
        for a, b in zip(original, parse(original_raw))
    )
    assert all(r["provenance"]["human_review"] == "unreviewed" for r in new)
    # 다른 사람이 추가한 변경을 조용히 덮어쓰지 않아요. 재실행은 같은 결과에만 허용해요.
    for path, before, result in [
        (MASTER, old_raw, new),
        (ORIGINAL, original_raw, original),
    ]:
        after = jsonl(result)
        assert path.read_bytes() in (before, after), f"예상하지 않은 변경: {path}"
        path.write_bytes(after)
    for path in sorted((BASE / "batches").glob("*.jsonl")):
        batch = parse(baseline(path))
        write(path, [revised[r["id"]] for r in batch], lines=True)
    changes = []
    for rid in sorted(target_ids):
        changes.append(
            {
                "row_id": rid,
                "original_critic": reviews[rid],
                "before": by_id[rid],
                "after": revised[rid],
                "before_content_sha256": digest(by_id[rid]),
                "after_content_sha256": digest(revised[rid]),
                "status": "재검수 요청 — 새로운 PASS나 사람 승인 아님",
            }
        )
    write(BASE / "reviews/additional_900_18_corrections.jsonl", changes, lines=True)
    write(
        BASE / "reviews/additional_900_recheck_18_requests.jsonl",
        [request(revised[rid]) for rid in sorted(target_ids)],
        lines=True,
    )
    write(
        BASE / "reviews/additional_900_882_preserved_pass.jsonl",
        [reviews[r["id"]] for r in new if r["id"] not in target_ids],
        lines=True,
    )
    write(BASE / "validation/wire_normalization_600.jsonl", wire_log, lines=True)
    receipt = {
        "base_revision": BASE_REV,
        "original_critic_sha256": sha(critic_raw),
        "original_critic_unchanged": True,
        "before_additional_dataset_sha256": sha(old_raw),
        "after_additional_dataset_sha256": sha(MASTER.read_bytes()),
        "before_original_dataset_sha256": sha(original_raw),
        "after_original_dataset_sha256": sha(ORIGINAL.read_bytes()),
        "original_900_canonical_content_unchanged": True,
        "original_900_answers_and_approvals_unchanged": True,
        "canonical_changed_rows": sorted(target_ids),
        "canonical_changed_row_count": 18,
        "assistant_changed_row_count": 17,
        "preserved_external_PASS_hash_matches": 882,
        "pending_recheck_rows": 18,
        "new_critic_PASS_created": False,
        "wire_only_rows": dict(Counter(r["dataset"] for r in wire_log)),
        "wire_only_canonical_hashes_unchanged": True,
        "all_1800_wire_inputs_match_build_messages": True,
        "additional_human_review": "unreviewed",
        "additional_hard_negative_count": sum(r["is_hard_negative"] for r in new),
    }
    write(BASE / "validation/remediation_18_receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
