"""Conservative response templates for the shared SLM modes."""

from beauty_agent.v3_contracts import SLMRequest, SLMResponse

_FALLBACK_REASONS = frozenset({
    "timeout",
    "network_error",
    "http_error",
    "response_too_large",
    "invalid_response",
    "empty_content",
    "guardrail_blocked",
})


class RuleBaselineFallback:
    """Use input status only. Avoid copying untrusted observations or excerpts."""

    def build(self, request: SLMRequest, *, reason: str) -> SLMResponse:
        if request.mode == "hold":
            content = (
                "### 개별 권고 보류 안내\n현재 확인된 정보 범위에서는 개별 권고를 보류해요.\n\n"
                "### 필요한 다음 단계\n불편이 계속되면 전문가에게 경과를 확인받아 주세요."
            )
        elif request.mode == "solution":
            summary = (
                "사용자가 확인한 루틴 정보는 확인된 범위까지만 반영해요."
                if any(o.state == "known" and o.confirmed_by_user for o in request.confirmed_observations.values())
                else "사용자 루틴에서 확인된 정보가 제한적이에요."
            )
            content = (
                f"### 핵심 안내\n{summary} 개별 변경이나 대체 제품 제안은 보류해요.\n\n"
                "### 근거 및 이유\n확인된 정보의 범위를 넘어 구체적인 사용법을 정하기 어려워요.\n\n"
                "### 확인이 필요한 한계\n확인되지 않은 관찰값과 제품 정보는 미상(unknown)으로 남겨요."
            )
        else:
            content = '{"status":"unavailable","confirmed_by_user":false}'

        return SLMResponse(
            mode=request.mode,
            content=content,
            cited_evidence_refs=[],
            provider="rule_baseline_fallback",
            fallback_used=True,
            fallback_reason=reason if reason in _FALLBACK_REASONS else "invalid_response",
        )
