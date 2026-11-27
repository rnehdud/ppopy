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


def test_verify_nlu_extraction_stage3_checks() -> None:
    src = "아침에 미온수로 세안했는데 동생은 따갑다고 해요."
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
        product_mentions=[ProductMentionCandidate(raw_text="세안제", usage_state="unknown")],
    )
    assert verify_nlu_extraction(valid) == valid

    bad_var = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(variable_id="unknown.slot", value="x", evidence_span="미온수")
            ]
        }
    )
    with pytest.raises(ValueError, match="whitelist"):
        verify_nlu_extraction(bad_var)

    bad_enum = valid.model_copy(
        update={
            "slot_candidates": [
                SlotCandidate(
                    variable_id="method.water_temperature",
                    value="boiling_water",
                    evidence_span="미온수로 세안",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="invalid enum value"):
        verify_nlu_extraction(bad_enum)

    bad_symptom = valid.model_copy(
        update={
            "symptom_candidates": [
                SymptomCandidateV3(symptom="eczema", evidence_span="따갑다고")
            ]
        }
    )
    with pytest.raises(ValueError, match="symptoms"):
        verify_nlu_extraction(bad_symptom)

    bad_topic = valid.model_copy(update={"topics": ["diagnosis"]})
    with pytest.raises(ValueError, match="topics"):
        verify_nlu_extraction(bad_topic)


def test_validate_nlu_dataset_pass_and_fail(tmp_path: Path) -> None:
    req = NLURequest(source_text="찬물로 세수했어요.")
    ext = NLUExtractionResult(
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
    row = {
        "id": "nlu-0001",
        "split": "train",
        "messages": build_nlu_messages(req)
        + [{"role": "assistant", "content": ext.model_dump_json()}],
    }
    good_path = tmp_path / "good.jsonl"
    good_path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    report = validate_nlu_jsonl(good_path)
    assert report["passed"] is True
    assert report["error_count"] == 0

    # Leakage across train and val_internal should fail
    row2 = {**row, "id": "nlu-0002", "split": "val_internal"}
    bad_path = tmp_path / "leak.jsonl"
    bad_path.write_text(
        json.dumps(row, ensure_ascii=False) + "\n" + json.dumps(row2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    leak_report = validate_nlu_jsonl(bad_path)
    assert leak_report["passed"] is False
    assert any("leakage" in e for e in leak_report["errors"])
