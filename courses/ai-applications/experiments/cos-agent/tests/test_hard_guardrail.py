"""Exercise the fail-closed output boundary with synthetic responses."""

import pytest

from beauty_agent.guardrail import HardSafetyGuardrail
from beauty_agent.slm import RuleBaselineFallback
from beauty_agent.v3_contracts import SLMRequest, SLMResponse


def _validate(mode, content, **kwargs):
    request = SLMRequest(mode=mode, **kwargs)
    return HardSafetyGuardrail().validate(request, SLMResponse(mode=mode, content=content))


@pytest.mark.parametrize(
    ("mode", "content", "refs"),
    [
        ("solution", "관찰 범위에 맞춰 설명해요. [ref:one]", ["ref:one"]),
        ("hold", "개별 권고는 보류해요. 전문가에게 경과를 확인받아 주세요.", []),
    ],
)
def test_normal_response_passes_unchanged(mode, content, refs):
    request = SLMRequest(mode=mode, allowed_evidence_refs=refs)
    response = SLMResponse(mode=mode, content=content, cited_evidence_refs=refs)
    result = HardSafetyGuardrail().validate(request, response)
    assert result.passed and result.flags == []
    assert result.safe_response is response


@pytest.mark.parametrize(
    ("mode", "text", "allowed", "distractors", "flag"),
    [
        ("solution", "설명해요. [kb:B-C01]", ["kb:B-C01"], [], "kb_citation"),
        ("solution", "설명해요. [ref:unknown]", [], [], "citation_not_allowed"),
        ("solution", "설명해요. [ref:noise]", [], ["ref:noise"], "distractor_citation"),
        ("hold", "권고는 보류해요. [ref:one]", ["ref:one"], [], "hold_citation"),
        ("hold", "아침에 이 제품을 사용하세요.", [], [], "hold_recommendation"),
        ("hold", "보습제를 바르는 게 좋아요.", [], [], "hold_recommendation"),
        ("hold", "대체 제품을 소개할게요.", [], [], "hold_recommendation"),
        ("hold", "볼에 로션을 발라 주세요.", [], [], "hold_recommendation"),
        ("solution", "접촉피부염이에요.", [], [], "clinical_or_safety_claim"),
        ("solution", "이 방법으로 치료돼요.", [], [], "clinical_or_safety_claim"),
        ("solution", "피부가 40% 개선돼요.", [], [], "clinical_or_safety_claim"),
        ("solution", "AI가 피부 개선 여부를 판정했어요.", [], [], "clinical_or_safety_claim"),
        ("solution", "pH는 5.5로 추정돼요.", [], [], "clinical_or_safety_claim"),
        ("solution", "농도는 2%로 추정돼요.", [], [], "clinical_or_safety_claim"),
    ],
)
def test_unsafe_output_is_replaced(mode, text, allowed, distractors, flag):
    result = _validate(mode, text, allowed_evidence_refs=allowed, distractor_refs=distractors)
    assert not result.passed
    assert flag in result.flags
    assert result.safe_response.mode == mode
    assert result.safe_response.fallback_reason == "guardrail_blocked"
    assert result.safe_response.provider == "rule_baseline_fallback"
    assert result.safe_response.fallback_used
    assert result.safe_response.cited_evidence_refs == []
    assert text not in result.safe_response.content


def test_unverified_product_assertion_and_wrong_version_are_rejected():
    result = _validate("solution", "제품 라벨에 글리세린이 표시돼 있어요.")
    assert "unverified_product_claim" in result.flags

    result = _validate(
        "solution",
        "사용법은 확인된 표시를 참고해요. [catalog:test-product@2]",
        allowed_evidence_refs=["catalog:test-product@2"],
        product_evidence=[{"product_id": "test-product", "version": "1", "status": "verified"}],
    )
    assert "product_version_mismatch" in result.flags


def test_request_to_check_a_label_is_not_an_assertion():
    result = _validate("solution", "현재 제품이 해당 용도로 표시돼 있는지부터 확인해 보세요.")
    assert result.passed


def test_verified_product_evidence_can_be_cited():
    result = _validate(
        "solution",
        "제품 라벨에 글리세린이 표시돼 있어요. [catalog:test-product@1]",
        allowed_evidence_refs=["catalog:test-product@1"],
        product_evidence=[{"product_id": "test-product", "version": "1", "status": "verified"}],
    )
    assert result.passed


def test_guard_checks_response_mode_and_claimed_citations():
    checked = HardSafetyGuardrail().validate(
        SLMRequest(mode="hold"),
        SLMResponse(mode="solution", content="예시", cited_evidence_refs=["ref:fake"]),
    )
    assert {"mode_mismatch", "citation_metadata_mismatch", "citation_not_allowed"} <= set(checked.flags)
    assert checked.safe_response.mode == "hold"


def test_fallback_is_repeatable_and_does_not_echo_untrusted_text():
    request = SLMRequest(
        mode="solution",
        product_evidence=[{"status": "unknown", "label_guidance": "unsafe text to copy"}],
        allowed_evidence_refs=["ref:one"],
    )
    fallback = RuleBaselineFallback()
    result = fallback.build(request, reason="contains credentials")
    assert result == fallback.build(request, reason="invalid_response")
    assert "unknown" in result.content
    assert "unsafe text" not in result.content
    assert not result.cited_evidence_refs
