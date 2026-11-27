"""파일럿 전체의 균형·정확한 Wire·요청/예상 후보·검수 해시를 대조해요."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from build_nlu_v1_pilot import content_hash

from beauty_agent.nlu_schema import (
    ALLOWED_SYMPTOMS,
    load_nlu_whitelist,
    verify_nlu_extraction,
)
from beauty_agent.slm.prompt_builder import build_nlu_messages
from beauty_agent.v3_contracts import NLUExtractionResult, NLURequest


def main():
    base = COS / "data/nlu/v1"
    raw = (base / "pilot_nlu_v1.jsonl").read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    assert len(rows) == len({r["id"] for r in rows}) == 49
    expected = {
        "turn1_utterance",
        "turn2_followup",
        "denied_polarity",
        "other_subject",
        "high_risk_symptom",
        "product_mention",
        "no_signal_noise",
    }
    buckets = Counter(r["primary_bucket"] for r in rows)
    assert set(buckets) == expected and set(buckets.values()) == {7}
    texts = {}
    families = defaultdict(set)
    symptoms = Counter()
    persistence = Counter()
    usage = Counter()
    slots = Counter()
    domains = set()
    prefix_checks = []
    review = [
        json.loads(line)
        for line in (base / "reviews/pilot_nlu_v1_critic_requests.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    hashes = {r["row_id"]: r["content_sha256"] for r in review}
    assert len(hashes) == len(review) == 49
    shared_allowed = None
    for row in rows:
        req = NLURequest.model_validate_json(row["messages"][1]["content"])
        ext = NLUExtractionResult.model_validate_json(row["messages"][2]["content"])
        assert row["messages"][:2] == build_nlu_messages(req), row["id"]
        assert verify_nlu_extraction(ext, request=req) == ext
        assert ext.confirmed_by_user is False
        assert "timeout_seconds" not in json.loads(row["messages"][1]["content"])
        assert "max_response_bytes" not in json.loads(row["messages"][1]["content"])
        assert hashes[row["id"]] == content_hash(row)
        if shared_allowed is None:
            shared_allowed = req.allowed_variable_ids
        assert req.allowed_variable_ids == shared_allowed
        text_key = re.sub(r"\s+", " ", req.source_text).strip()
        assert text_key not in texts, row["id"]
        texts[text_key] = row["split"]
        families[row["scenario_family_id"]].add(row["split"])
        assert row["split"] in {"train", "val_internal"}
        assert row["provenance"]["source_origin"] == "new_synthetic"
        assert (
            row["provenance"]["critic_status"]
            == row["provenance"]["human_review"]
            == "unreviewed"
        )
        assert row["runtime_invariants"] == {
            "mode": "development_preview",
            "production_enabled": False,
            "requires_approval": True,
            "saved": False,
        }
        bucket = row["primary_bucket"]
        if bucket == "turn1_utterance":
            assert req.previous_question is None and req.target_slot_id is None
        if bucket == "turn2_followup":
            assert req.previous_question and req.target_slot_id
        if bucket == "denied_polarity":
            assert any(
                x.polarity == "denied"
                for x in ext.slot_candidates + ext.symptom_candidates
            )
        if bucket == "other_subject":
            assert any(
                x.subject == "other"
                for x in ext.slot_candidates + ext.symptom_candidates
            )
        if bucket == "high_risk_symptom":
            assert ext.symptom_candidates
        if bucket == "product_mention":
            assert ext.product_mentions
        if bucket == "no_signal_noise":
            assert not (
                ext.topics
                or ext.slot_candidates
                or ext.symptom_candidates
                or ext.product_mentions
            )
        for candidate in ext.slot_candidates:
            assert not candidate.variable_id.startswith("product.")
            assert candidate.polarity != "unknown" or candidate.value is None
            slots[candidate.variable_id] += 1
            domains.add(candidate.variable_id.split(".")[0])
        for candidate in ext.symptom_candidates:
            symptoms[candidate.symptom] += 1
            persistence[candidate.persistence] += 1
        for mention in ext.product_mentions:
            usage[mention.usage_state] += 1
            if mention.matched_catalog_hint is not None:
                assert any(
                    h.raw_span.strip() == mention.raw_text.strip()
                    and h.matched_catalog_hint == mention.matched_catalog_hint
                    for h in req.catalog_hints
                )
            if any(
                mention.raw_text.startswith(h.raw_span)
                and mention.raw_text != h.raw_span
                for h in req.catalog_hints
            ):
                assert mention.matched_catalog_hint is None
                prefix_checks.append(
                    {
                        "row_id": row["id"],
                        "raw_text": mention.raw_text,
                        "matched_catalog_hint": None,
                    }
                )
    assert all(len(v) == 1 for v in families.values())
    assert set(symptoms) == set(ALLOWED_SYMPTOMS)
    assert set(persistence) == {"recent", "repeated", "persistent", "unknown"}
    assert set(usage) == {"using", "stopped", "considering", "other_person", "unknown"}
    assert {"method", "cleansing", "moisturizing", "sun", "storage"} <= domains
    report = {
        "passed": True,
        "scope": "49행 구조·범위·원문 대조 및 해시 검사. 독립 의미 검수나 모델 성능 측정이 아니에요.",
        "rows": 49,
        "primary_buckets": dict(buckets),
        "splits": dict(Counter(r["split"] for r in rows)),
        "unique_families": len(families),
        "cross_split_family_leakage": 0,
        "normalized_source_duplicates": 0,
        "exact_runtime_wire_messages": 49,
        "whitelisted_variables": len(load_nlu_whitelist().variable_ids),
        "common_allowed_variables": len(shared_allowed),
        "emitted_slot_ids": dict(slots),
        "symptoms": dict(symptoms),
        "persistence": dict(persistence),
        "product_usage": dict(usage),
        "prefix_collision_checks": prefix_checks,
        "review_request_hashes_verified": 49,
        "dataset_sha256": hashlib.sha256(raw).hexdigest(),
        "cross_model_critic_performed": False,
        "base_zero_shot_executed": False,
        "human_approved": False,
    }
    (base / "validation/pilot_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
