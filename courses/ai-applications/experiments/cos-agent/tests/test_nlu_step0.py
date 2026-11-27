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

    # P2: whitespace-only evidence_span is rejected even when source_text contains spaces
    with pytest.raises(ValidationError, match="evidence_span"):
        NLUExtractionResult(
            source_text="찬물로 세안했어요.",
            slot_candidates=[
                SlotCandidate(variable_id="method.water_temperature", value="hot", evidence_span=" ")
            ],
        )


def test_verify_nlu_extraction_stage3_checks() -> None:
    src = "아침에 미온수로 세안하고 Lotion A와 Lotion AB를 썼는데 동생은 따갑다고 해요."
    req = NLURequest(
        source_text=src,
        catalog_hints=[
            CatalogHintCandidate(raw_span="Lotion A", matched_catalog_hint="브랜드 Lotion A")
        ],
        allowed_variable_ids=["method.water_temperature", "moisturizing.comfort", "cleansing.steps"],
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
                raw_text="Lotion A",
                usage_state="using",
                matched_catalog_hint="브랜드 Lotion A",
            )
        ],
    )
    assert verify_nlu_extraction(valid, request=req) == valid

    # P1: Stage 3 requires original NLURequest (calling without request raises TypeError)
    with pytest.raises(TypeError):
        verify_nlu_extraction(valid)  # type: ignore[call-arg]

    # P1: B-I01 canonical symbolic string for cleansing.steps is accepted
    bi01_req = NLURequest(
        source_text="내수성 표시만 보고 두 번 세안했어요.",
        allowed_variable_ids=["cleansing.steps"],
    )
    bi01_ext = NLUExtractionResult(
        source_text="내수성 표시만 보고 두 번 세안했어요.",
        topics=["repeat_cleansing"],
        slot_candidates=[
            SlotCandidate(
                variable_id="cleansing.steps",
                value="repeated_only_because_water_resistant",
                polarity="affirmed",
                evidence_span="내수성 표시만 보고 두 번 세안",
            )
        ],
    )
    assert verify_nlu_extraction(bi01_ext, request=bi01_req) == bi01_ext

    # P1: product mention raw_text absent from source_text is rejected by Stage 3 verifier
    missing_req = NLURequest(source_text="얼굴이 따가워요.")
    missing_mention = NLUExtractionResult(
        source_text="얼굴이 따가워요.",
        product_mentions=[ProductMentionCandidate(raw_text="로션", usage_state="using")],
    )
    with pytest.raises(ValueError, match="raw_text"):
        verify_nlu_extraction(missing_mention, request=missing_req)

    # P2: prefix-overlapping Lotion A hint must NOT attach to Lotion AB
    prefix_mismatch = valid.model_copy(
        update={
            "product_mentions": [
                ProductMentionCandidate(
                    raw_text="Lotion AB",
                    usage_state="using",
                    matched_catalog_hint="브랜드 Lotion A",
                )
            ]
        }
    )
    with pytest.raises(ValueError, match="exact matching"):
        verify_nlu_extraction(prefix_mismatch, request=req)

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

    # P2: non-enum structured/ordinal slot with invalid bare integer (moisturizing.comfort=42) is rejected
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


def test_validate_nlu_dataset_checks_leakage_wire_schema_and_resilience(tmp_path: Path) -> None:
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

    # P2: Trailing whitespace difference across splits with different family_ids is caught as leakage
    req_ws = NLURequest(source_text="찬물로   세수했어요.  ")
    ext_ws = NLUExtractionResult(
        source_text="찬물로   세수했어요.  ",
        topics=["cleansing_method"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.water_temperature",
                value="cold",
                evidence_span="찬물로",
            )
        ],
    )
    row_ws = {
        "id": "nlu-0002",
        "scenario_family_id": "fam-cleanse-02",
        "split": "val_internal",
        "messages": build_nlu_messages(req_ws)
        + [{"role": "assistant", "content": ext_ws.model_dump_json()}],
    }
    ws_leak_path = tmp_path / "ws_leak.jsonl"
    ws_leak_path.write_text(
        json.dumps(row1, ensure_ascii=False) + "\n" + json.dumps(row_ws, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    ws_report = validate_nlu_jsonl(ws_leak_path)
    assert ws_report["passed"] is False
    assert any("source_text leakage" in e for e in ws_report["errors"])

    # P2: Non-string split ([] / {}) reports row error cleanly instead of raising TypeError
    # P3: Invalid UTF-8 bytes line reports decoding error cleanly; U+2028 in JSON string does NOT split line
    req_u2028 = NLURequest(source_text="찬물로\u2028세수했어요.")
    ext_u2028 = NLUExtractionResult(
        source_text="찬물로\u2028세수했어요.",
        topics=["cleansing_method"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.water_temperature",
                value="cold",
                evidence_span="찬물로",
            )
        ],
    )
    row_u2028 = {
        "id": "nlu-u2028",
        "scenario_family_id": "fam-u2028",
        "split": "train",
        "messages": build_nlu_messages(req_u2028)
        + [{"role": "assistant", "content": ext_u2028.model_dump_json()}],
    }
    u2028_path = tmp_path / "u2028.jsonl"
    u2028_path.write_bytes((json.dumps(row_u2028, ensure_ascii=False) + "\n").encode("utf-8"))
    u2028_report = validate_nlu_jsonl(u2028_path)
    assert u2028_report["passed"] is True
    assert u2028_report["total_rows"] == 1

    resilience_path = tmp_path / "resilience.jsonl"
    resilience_path.write_bytes(
        b"[]\n"
        + b"\xff\xfeinvalid-utf8\n"
        + (json.dumps({"id": "nlu-bad-split", "scenario_family_id": "fam-x", "split": [], "messages": []}) + "\n").encode("utf-8")
        + (json.dumps(row1, ensure_ascii=False) + "\n").encode("utf-8")
    )
    res_report = validate_nlu_jsonl(resilience_path)
    assert res_report["passed"] is False
    assert res_report["total_rows"] == 4
    assert any("must be a JSON object" in e for e in res_report["errors"])
    assert any("invalid UTF-8 bytes" in e for e in res_report["errors"])
    assert any("split must be a string" in e for e in res_report["errors"])
