"""Unit tests for Ppopy v3 Phase 0 shared inter-module Pydantic contracts."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from beauty_agent.contracts import ObservationSlot
from beauty_agent.v3_contracts import (
    AFACandidateScore,
    AFAStepDecision,
    ChoiceSelectionV3,
    NLUExtractionResult,
    ProductMentionCandidate,
    QuestionChoiceV3,
    ReferenceChunk,
    RetrievalResult,
    RuntimeQuestionV3,
    RuntimeTurnRequestV3,
    RuntimeTurnResponseV3,
    SLMRequest,
    SLMResponse,
    SlotCandidate,
    SymptomCandidateV3,
    TurnTrace,
)


def _sample_chunk(ref: str = "ref:aad-cleansing-01") -> ReferenceChunk:
    return ReferenceChunk(
        evidence_ref=ref,
        text="Use lukewarm water and gentle fingertips when washing the face.",
        scope="general_skincare_practice",
        source_url="https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
        locator="Section 1: Face washing basics",
        checked_on="2026-11-20",
        limitations="General consumer skincare guidance, not clinical diagnosis.",
    )


def test_nlu_extraction_valid_and_evidence_span_enforced():
    text = "어제 수건으로 세게 닦았고 따갑진 않고 볼이 좀 당겨요."
    result = NLUExtractionResult(
        source_text=text,
        topics=["cleansing", "moisturizing"],
        slot_candidates=[
            SlotCandidate(
                variable_id="method.drying",
                value="rubbing_strongly",
                evidence_span="수건으로 세게 닦았고",
            )
        ],
        symptom_candidates=[
            SymptomCandidateV3(
                symptom="stinging",
                polarity="denied",
                subject="self",
                evidence_span="따갑진 않고",
            )
        ],
        product_mentions=[ProductMentionCandidate(raw_text="선크림", usage_state="using")],
    )
    assert result.confirmed_by_user is False

    # Hallucinated evidence_span not in source_text must fail
    with pytest.raises(ValidationError, match="evidence_span not found"):
        NLUExtractionResult(
            source_text=text,
            slot_candidates=[
                SlotCandidate(
                    variable_id="method.water_temperature",
                    value="hot",
                    evidence_span="뜨거운 물로 씻었어요",
                )
            ],
        )


def test_nlu_rejects_product_slot_and_auto_confirmation():
    with pytest.raises(ValidationError, match="product\\.\\*"):
        SlotCandidate(variable_id="product.ph", value=5.5, evidence_span="약산성")

    with pytest.raises(ValidationError):
        NLUExtractionResult(source_text="미온수로 씻어요", confirmed_by_user=True)


def test_afa_step_decision_invariants():
    acq = AFAStepDecision(action="acquire", target_feature="method.drying", policy_source="myopic_voi")
    assert acq.stop_reason is None

    stop = AFAStepDecision(action="stop", stop_reason="sufficient", policy_source="myopic_voi")
    assert stop.target_feature is None

    score = AFACandidateScore(
        slot_id="method.drying",
        answer_count=2,
        expected_pruned=1.0,
        decision_change_rate=0.5,
        distinct_outcomes=2,
        reason="selected",
    )
    assert score.safety_weight == 1.0

    # AFA must never ask users for product.* slots
    with pytest.raises(ValidationError, match="product\\.\\*"):
        AFAStepDecision(action="acquire", target_feature="product.surfactant_type")

    # acquire with stop_reason or stop with target_feature must fail
    with pytest.raises(ValidationError):
        AFAStepDecision(action="acquire", target_feature="method.drying", stop_reason="sufficient")
    with pytest.raises(ValidationError):
        AFAStepDecision(action="stop", target_feature="method.drying", stop_reason="sufficient")


def test_reference_rag_requires_ref_prefix():
    res = RetrievalResult(
        chunks=[_sample_chunk("ref:aad-cleansing-01")],
        index_version="ref-v1.0",
        retriever_backend="faiss",
    )
    assert res.chunks[0].scope == "general_skincare_practice"

    with pytest.raises(ValidationError, match="must start with 'ref:'"):
        _sample_chunk("kb:B-C01")


def test_slm_request_forbids_question_mode_and_non_solution_rag():
    chunk = _sample_chunk()
    req = SLMRequest(
        mode="solution",
        confirmed_observations={
            "method.drying": ObservationSlot(
                variable_id="method.drying",
                state="known",
                value="rubbing_strongly",
                confirmed_by_user=True,
            )
        },
        rag_chunks=[chunk],
        allowed_evidence_refs=["kb:B-C02@0.6.1", "ref:aad-cleansing-01"],
        distractor_refs=["ref:unrelated-09"],
    )
    assert req.timeout_seconds == 15.0

    # QUESTION_MODE is forbidden in v3
    with pytest.raises(ValidationError):
        SLMRequest(mode="question")

    # RAG chunks must not be passed in hold or nlu modes
    with pytest.raises(ValidationError, match="only permitted in 'solution' mode"):
        SLMRequest(mode="hold", rag_chunks=[chunk])

    # allowed and distractor refs must be disjoint
    with pytest.raises(ValidationError, match="must be disjoint"):
        SLMRequest(
            mode="solution",
            allowed_evidence_refs=["ref:aad-cleansing-01"],
            distractor_refs=["ref:aad-cleansing-01"],
        )

    resp = SLMResponse(
        mode="solution",
        content="수건 마찰을 줄여 주세요 [ref:aad-cleansing-01].",
        cited_evidence_refs=["ref:aad-cleansing-01"],
        model="qwen-3.5-4b-qlora",
    )
    assert resp.fallback_used is False


def test_runtime_turn_request_and_response_invariants():
    fast_path = RuntimeTurnRequestV3(
        request_id="req-001",
        choice_selection=ChoiceSelectionV3(turn_index=1, question_id="method.drying", choice_id="pat_gently"),
    )
    assert fast_path.choice_selection is not None

    # Mixing choice_selection with free-text message must fail
    with pytest.raises(ValidationError, match="fast-path"):
        RuntimeTurnRequestV3(
            request_id="req-001",
            message="가볍게 눌러 닦아요",
            choice_selection=ChoiceSelectionV3(turn_index=1, question_id="method.drying", choice_id="pat_gently"),
        )

    trace = TurnTrace(
        request_id="req-001",
        turn_index=1,
        nlu_skipped_fast_path=True,
        afa_decision=AFAStepDecision(action="acquire", target_feature="method.drying"),
    )
    resp = RuntimeTurnResponseV3(
        request_id="req-001",
        status="awaiting_user",
        questions=[
            RuntimeQuestionV3(
                id="method.drying",
                text="물기를 닦을 때 수건으로 문지르나요, 가볍게 눌러 닦나요?",
                turn_index=1,
                choices=[QuestionChoiceV3(id="pat_gently", label="가볍게 눌러 닦음")],
            )
        ],
        trace=trace,
    )
    assert resp.mode == "development_preview"
    assert resp.production_enabled is False
    assert resp.requires_approval is True
    assert resp.saved is False

    # Production/approval/saved invariants cannot be bypassed
    with pytest.raises(ValidationError):
        RuntimeTurnResponseV3(request_id="req-001", status="completed", production_enabled=True)
    with pytest.raises(ValidationError):
        RuntimeTurnResponseV3(request_id="req-001", status="completed", requires_approval=False)
    with pytest.raises(ValidationError):
        RuntimeTurnResponseV3(request_id="req-001", status="completed", saved=True)
