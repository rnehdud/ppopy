"""Offline unit tests for Ppopy v3 NLU Step 0 contracts, KB whitelist, and validator."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from pydantic import ValidationError

from beauty_agent.nlu_schema import load_nlu_whitelist, verify_nlu_extraction
from beauty_agent.slm import SYSTEM_PROMPT_NLU, build_nlu_messages
from beauty_agent.v3_contracts import (
    CatalogHintCandidate,
    NLUExtractionResult,
    NLURequest,
    ProductMentionCandidate,
    SlotCandidate,
    SymptomCandidateV3,
)
from scripts.validate_nlu_dataset import validate_nlu_jsonl


def test_load_nlu_whitelist_from_kb_v061() -> None:
    wl = load_nlu_whitelist()
    assert len(wl.variable_ids) == 163
    assert "method.water_temperature" in wl.variable_ids
    assert "moisturizing.comfort" in wl.variable_ids
    assert "sun.outdoor_time" in wl.variable_ids
    assert not any(vid.startswith("product.") for vid in wl.variable_ids)
    assert "stinging" in wl.symptoms
    assert "cleansing_method" in wl.topics


def test_nlu_request_and_build_nlu_messages() -> None:
    req = NLURequest(
        source_text="미온수로 세안하고 선크림 A를 발랐는데 볼이 좀 따가워요.",
        catalog_hints=[
            CatalogHintCandidate(raw_span="선크림 A", matched_catalog_hint="브랜드 선크림 A", match_score=0.95)
        ],
        previous_question="세안할 때 물 온도는 어떤가요?",
        target_slot_id="method.water_temperature",
        allowed_variable_ids=["method.water_temperature"],
        allowed_symptoms=["stinging"],
        allowed_topics=["cleansing_method", "discomfort_report"],
    )
    messages = build_nlu_messages(req)
    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": SYSTEM_PROMPT_NLU}
    payload = json.loads(messages[1]["content"])
    assert payload["source_text"] == req.source_text
    assert payload["previous_question"] == "세안할 때 물 온도는 어떤가요?"
    assert payload["target_slot_id"] == "method.water_temperature"
    assert "timeout_seconds" not in payload
    assert "max_response_bytes" not in payload

    with pytest.raises(ValidationError):
        NLURequest(source_text="테스트", target_slot_id="product.pH")

    # P1: catalog_hint raw_span must exist in source_text
    with pytest.raises(ValidationError, match="raw_span"):
        NLURequest(
            source_text="얼굴이 따가워요.",
            catalog_hints=[
                CatalogHintCandidate(raw_span="없는로션", matched_catalog_hint="브랜드 없는로션")
            ],
        )


def test_verify_nlu_extraction_stage3_checks() -> None:
    src = "아침에 미온수로 세안하고 선크림 A를 썼는데 동생은 따갑다고 해요."
    req = NLURequest(
        source_text=src,
        catalog_hints=[
            CatalogHintCandidate(raw_span="선크림 A", matched_catalog_hint="브랜드 선크림 A")
        ],
        allowed_variable_ids=["method.water_temperature", "moisturizing.comfort"],
        allowed_symptoms=["stinging"],
        allowed_topics=["cleansing_method", "discomfort_report"],
    )
    valid = NLUExtractionResult(
        source_text=src,
        topics=["cleansing_method", "discomfort_report"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.water_temperature",
                value="lukewarm",
                polarity="affirmed",
                subject="self",
                confidence="high",
                evidence_span="미온수로 세안",
            )
        ],
        symptom_candidates=[
            SymptomCandidateV3(
                symptom="stinging",
                polarity="affirmed",
                subject="other",
                persistence="unknown",
                evidence_span="동생은 따갑다고 해요",
            )
        ],
        product_mentions=[
            ProductMentionCandidate(
                raw_text="선크림 A",
                usage_state="using",
                matched_catalog_hint="브랜드 선크림 A",
            )
        ],
    )
    assert verify_nlu_extraction(valid, request=req) == valid

    # P1: product mention raw_text absent from source_text is rejected by Stage 3 verifier
    missing_mention = NLUExtractionResult(
        source_text="얼굴이 따가워요.",
        product_mentions=[ProductMentionCandidate(raw_text="로션", usage_state="using")],
    )
    with pytest.raises(ValueError, match="raw_text"):
        verify_nlu_extraction(missing_mention)

    # P1: matched_catalog_hint not grounded in request.catalog_hints is rejected
    ungrounded_hint = valid.model_copy(
        update={
            "product_mentions": [
                ProductMentionCandidate(
                    raw_text="선크림 A",
                    usage_state="using",
                    matched_catalog_hint="입력에 없던 힌트",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="not grounded in request.catalog_hints"):
        verify_nlu_extraction(ungrounded_hint, request=req)

    # P2: denied enum slot with arbitrary dict value is rejected
    bad_denied_enum = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(
                    variable_id="method.water_temperature",
                    value={"arbitrary": "obj"},
                    polarity="denied",
                    evidence_span="미온수로 세안",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="invalid enum value"):
        verify_nlu_extraction(bad_denied_enum, request=req)

    # P2: non-enum structured/ordinal slot with invalid bare integer (e.g. moisturizing.comfort=42) is rejected
    bad_non_enum = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(
                    variable_id="moisturizing.comfort",
                    value=42,
                    polarity="affirmed",
                    evidence_span="미온수로 세안",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="requires a string"):
        verify_nlu_extraction(bad_non_enum, request=req)

    # P2: unknown polarity must have value=None
    bad_unknown_val = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(
                    variable_id="method.water_temperature",
                    value="hot",
                    polarity="unknown",
                    evidence_span="미온수로 세안",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="polarity='unknown'"):
        verify_nlu_extraction(bad_unknown_val, request=req)

    # P2: slot outside request.allowed_variable_ids is rejected
    outside_req_allowlist = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(
                    variable_id="sun.outdoor_time",
                    value="prolonged",
                    polarity="affirmed",
                    evidence_span="아침에",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="not in request.allowed_variable_ids"):
        verify_nlu_extraction(outside_req_allowlist, request=req)


def test_validate_nlu_dataset_checks_family_leakage_wire_schema_and_malformed_rows(tmp_path: Path) -> None:
    req1 = NLURequest(source_text="찬물로 세수했어요.")
    ext1 = NLUExtractionResult(
        source_text="찬물로 세수했어요.",
        topics=["cleansing_method"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.water_temperature",
                value="cold",
                evidence_span="찬물로",
            )
        ],
    )
    row1 = {
        "id": "nlu-0001",
        "scenario_family_id": "fam-cleanse-01",
        "split": "train",
        "messages": build_nlu_messages(req1)
        + [{"role": "assistant", "content": ext1.model_dump_json()}],
    }
    good_path = tmp_path / "good.jsonl"
    good_path.write_text(json.dumps(row1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    report = validate_nlu_jsonl(good_path)
    assert report["passed"] is True
    assert report["error_count"] == 0

    # P1: Paraphrased variant in same scenario_family_id across train & val_internal fails
    req2 = NLURequest(source_text="차가운 물로 얼굴을 씻었어요.")
    ext2 = NLUExtractionResult(
        source_text="차가운 물로 얼굴을 씻었어요.",
        topics=["cleansing_method"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.water_temperature",
                value="cold",
                evidence_span="차가운 물로",
            )
        ],
    )
    row2_same_family = {
        "id": "nlu-0002",
        "scenario_family_id": "fam-cleanse-01",
        "split": "val_internal",
        "messages": build_nlu_messages(req2)
        + [{"role": "assistant", "content": ext2.model_dump_json()}],
    }
    fam_leak_path = tmp_path / "fam_leak.jsonl"
    fam_leak_path.write_text(
        json.dumps(row1, ensure_ascii=False) + "\n" + json.dumps(row2_same_family, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    fam_report = validate_nlu_jsonl(fam_leak_path)
    assert fam_report["passed"] is False
    assert any("scenario_family_id leakage" in e for e in fam_report["errors"])

    # P2: Extra transport field (timeout_seconds) in user JSON fails wire-schema check
    bad_wire_user = json.loads(build_nlu_messages(req1)[1]["content"])
    bad_wire_user["timeout_seconds"] = 15.0
    bad_wire_row = {
        **row1,
        "id": "nlu-0003",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_NLU},
            {"role": "user", "content": json.dumps(bad_wire_user, ensure_ascii=False)},
            {"role": "assistant", "content": ext1.model_dump_json()},
        ],
    }
    wire_path = tmp_path / "bad_wire.jsonl"
    wire_path.write_text(json.dumps(bad_wire_row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    wire_report = validate_nlu_jsonl(wire_path)
    assert wire_report["passed"] is False
    assert any("wire schema" in e for e in wire_report["errors"])

    # P2: Malformed rows ([] and null messages) report errors cleanly without crashing batch
    malformed_path = tmp_path / "malformed.jsonl"
    malformed_path.write_text(
        "[]\n"
        + json.dumps({"id": "nlu-bad-msg", "scenario_family_id": "fam-x", "split": "train", "messages": [None, None, None]})
        + "\n"
        + json.dumps(row1, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    mal_report = validate_nlu_jsonl(malformed_path)
    assert mal_report["passed"] is False
    assert mal_report["total_rows"] == 3
    assert mal_report["split_counts"]["train"] == 2
    assert any("must be a JSON object" in e for e in mal_report["errors"])
    assert any("every item in messages must be a JSON object" in e for e in mal_report["errors"])
