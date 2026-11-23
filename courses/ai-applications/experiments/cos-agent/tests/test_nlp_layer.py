"""Tests for the Kiwi -> Jev -> MappingReview NLP Layer and runtime/AFA contracts."""
import pytest
from pydantic import ValidationError

from beauty_agent.contracts import ObservationSlot
from beauty_agent.nlp_layer import NLPLayer, interpret_slot_answer, load_jev_api_key
from beauty_agent.runtime_contracts import (
    AFAHandoffResult,
    AFAStepDecision,
    NLPExtractionResult,
    ProductQueryCandidate,
    SymptomCandidate,
)


def test_offline_kiwi_fallback_keeps_candidates_unconfirmed():
    layer = NLPLayer(use_remote_jev=False)
    result = layer.analyze("오늘 야외에 오래 있는데 어제 쓴 폼클렌저 후 볼이 따가워")

    assert result.source_mode == "offline_kiwi_fallback"
    assert result.confirmed_by_user is False
    assert result.units
    assert "outdoor_sun" in result.topic_hints
    assert "discomfort_report" in result.topic_hints
    assert any(c.symptom == "stinging" and c.requires_confirmation is True for c in result.symptom_candidates)
    assert "offline_candidate_detection_not_jev_inference" in result.warnings


@pytest.mark.parametrize(("slot_id", "answer", "expected"), [
    ("method.friction", "세게 문지르지 않아요.", None),
    ("method.friction", "세게 안 문질러요.", None),
    ("method.friction", "세게 문지르지 않고 부드럽게 씻어요.", "gentle"),
    ("method.friction", "세게 문질러서 씻어요.", "strong"),
    ("method.drying", "수건으로 세게 닦지 않고 물기를 톡톡 눌러 닦아요.", "pat_gently"),
])
def test_friction_negation_in_initial_message_and_follow_up(slot_id, answer, expected):
    expected_answer = ("known", expected) if expected else None
    assert interpret_slot_answer(slot_id, answer) == expected_answer

    result = NLPLayer(use_remote_jev=False).analyze(f"얼굴 세안은 이렇게 해요. {answer}")
    candidates = {candidate.slot_id: candidate.value for candidate in result.feature_candidates}
    assert candidates.get(slot_id) == expected


def test_injected_jev_relations_flows_through_mapping_review():
    def fake_jev_extractor(message: str) -> dict:
        return {
            "schema_version": "relations-0.5",
            "source_text": message,
            "segmentation_method": "kiwi_morpheme",
            "units": [{"unit_id": "u0", "start": 0, "end": len(message), "text": message}],
            "products": [
                {
                    "text": "시카크림",
                    "start": 0,
                    "end": 4,
                    "relations": {
                        "usage_state": {"value": "used"},
                        "subject": {"value": "self"},
                        "correction": {"value": "current"},
                    },
                }
            ],
            "symptoms": [
                {
                    "symptom": "itching",
                    "label": "가려움",
                    "relations": {
                        "state": {"value": "affirmed", "status": "candidate", "score": 0.9},
                        "subject": {"value": "self", "status": "candidate", "score": 0.9},
                        "correction": {"value": "current", "status": "candidate", "score": 0.9},
                        "observation_time": {"value": "not_mentioned"},
                    },
                }
            ],
            "warnings": [],
            "clarifications": [],
        }

    layer = NLPLayer(extractor=fake_jev_extractor)
    result = layer.analyze("시카크림 바르고 가려워요", namespace="t42")

    assert result.source_mode == "injected_extractor"
    assert result.confirmed_by_user is False
    assert len(result.product_queries) == 1
    assert result.product_queries[0].text == "시카크림"
    assert result.product_queries[0].usage_state == "used"
    assert result.product_queries[0].confirmed_ownership is False
    assert len(result.symptom_candidates) == 1
    assert result.symptom_candidates[0].candidate_id == "clarify:t42:0"
    assert result.symptom_candidates[0].symptom == "itching"
    assert result.symptom_candidates[0].requires_confirmation is True
    assert any(f.get("issue") == "candidate_requires_user_and_time_confirmation" for f in result.mapping_findings)


def test_load_jev_api_key_prefers_env_then_first_env_file(tmp_path, monkeypatch):
    root_env = tmp_path / "root.env"
    proj_env = tmp_path / "proj.env"
    root_env.write_text('jev-key="root-secret-key"\n', encoding="utf-8")
    proj_env.write_text("TYPESAFE_API_KEY=proj-secret-key\n", encoding="utf-8")

    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    assert load_jev_api_key((root_env, proj_env)) == "root-secret-key"

    monkeypatch.setenv("TYPESAFE_API_KEY", "env-override-key")
    assert load_jev_api_key((root_env, proj_env)) == "env-override-key"


def test_runtime_contracts_forbid_extra_fields_and_auto_confirmation():
    with pytest.raises(ValidationError):
        ProductQueryCandidate(text="크림", confirmed_ownership=True)  # type: ignore[arg-type]

    with pytest.raises(ValidationError):
        SymptomCandidate(
            candidate_id="c1",
            symptom="stinging",
            label="따가움",
            requires_confirmation=False,  # type: ignore[arg-type]
            prompt_ko="확인",
        )

    with pytest.raises(ValidationError):
        NLPExtractionResult(
            source_text="test",
            source_mode="offline_kiwi_fallback",
            segmentation_method="kiwi_morpheme",
            unexpected_field="nope",  # type: ignore[call-arg]
        )


def test_afa_step_decision_and_handoff_contracts():
    acquire = AFAStepDecision.from_legacy_action("ask_user", "method.tools", policy_source="ppo_model")
    assert acquire.action == "acquire"
    assert acquire.target_feature == "method.tools"
    assert acquire.stop_reason is None
    assert acquire.policy_source == "ppo_model"

    sufficient = AFAStepDecision.from_legacy_action("request_draft", "label_draft", policy_source="ppo_model")
    assert sufficient.action == "stop"
    assert sufficient.stop_reason == "sufficient"
    assert sufficient.target_feature is None

    insufficient = AFAStepDecision.from_legacy_action("hold", "insufficient_information")
    assert insufficient.action == "stop"
    assert insufficient.stop_reason == "insufficient"

    with pytest.raises(ValidationError):
        AFAStepDecision(action="acquire", target_feature=None)

    with pytest.raises(ValidationError):
        AFAStepDecision(action="stop", target_feature="method.tools", stop_reason="sufficient")

    handoff = AFAHandoffResult(
        status="sufficient",
        acquired_features={
            "method.body_site": ObservationSlot(
                variable_id="method.body_site",
                state="known",
                value="face",
                source="synthetic_fixture",
                confirmed_by_user=True,
            ),
            "method.tools": ObservationSlot(
                variable_id="method.tools",
                state="known",
                value="scrub_brush",
                source="user_report",
                confirmed_by_user=True,
            ),
        },
        asked_feature_order=["method.tools"],
        unanswered_or_declined=[],
        policy_source="ppo_model",
    )
    assert handoff.status == "sufficient"
    assert handoff.acquired_features["method.tools"].value == "scrub_brush"
    assert handoff.asked_feature_order == ["method.tools"]
