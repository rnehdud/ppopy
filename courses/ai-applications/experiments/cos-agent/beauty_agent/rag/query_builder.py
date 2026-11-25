"""Deterministic, bounded query construction; no LLM, I/O, or KB judgments."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from beauty_agent.contracts import ObservationSlot

LABELS = {
    "method.body_site": "사용 부위",
    "method.current_routine": "현재 관리 행동",
    "method.tools": "세정 도구",
    "method.friction": "피부 마찰",
    "method.drying": "물기 제거",
    "skin.current_discomfort": "현재 불편",
    "skin.dryness": "피부 건조",
    "skin.pain": "통증",
    "cleansing.steps": "세안 단계",
    "cleansing.repeat_wash": "반복 세안",
    "sun.activity": "야외 활동과 자외선차단",
    "constraints.goals": "확인하려는 내용",
    "environment.forecast": "날씨 예보",
    "environment.future_uv_index": "자외선 지수",
    "storage.sensory_change": "보관 중 색 냄새 분리 변화",
    "context.review_goal": "확인하려는 내용",
    "context.actual_use_sequence": "실제 사용 순서",
    "context.reported_findings": "보고된 관찰",
    "context.reported_timing": "보고된 시점",
    "context.sites_in_review": "검토 부위",
    "routine.goal": "루틴 목표",
    "routine.site": "루틴 부위",
    "routine.current_choice": "현재 선택 제품",
}
ALLOWED_PREFIXES = (
    "method.",
    "skin.",
    "sun.",
    "cleansing.",
    "moisturizing.",
    "environment.",
    "storage.",
    "dose.",
    "lifestyle.",
    "routine.",
    "constraints.",
    "makeup.",
    "shaving.",
    "hand.",
    "tool.",
    "person.",
    "introduction.",
    "adjunct.",
    "context.",
    "eye.",
    "symptom.",
    "weather.",
    "exposure.",
    "work.",
    "history.",
)
PRODUCT_FIELDS = (
    "product_type",
    "label_guidance",
    "ingredients",
    "removal_claim",
    "broad_spectrum",
    "spf",
    "pa",
)


def build_query(
    confirmed_observations: Mapping[str, ObservationSlot],
    product_evidence: Sequence[Mapping[str, object]],
    *,
    max_chars: int = 2000,
) -> str:
    """Use confirmed context; mark missing information, never promote old labels.

    Observations are already upstream-confirmed synthetic/user context. Arbitrary
    IDs, product versions, and model-generated guidance are not retrieval terms.
    Unknown/declined values are explicitly not treated as negative observations.
    """
    if not 1 <= max_chars <= 8000:
        raise ValueError("max_chars must be in [1, 8000]")
    parts = []
    for key, obs in sorted(confirmed_observations.items()):
        if not key.startswith(ALLOWED_PREFIXES):
            continue
        label = LABELS.get(key, key)
        if obs.state in {"unknown", "not_asked", "declined", "conflicting"}:
            parts.append(f"{label}: 미확인 ({obs.state})")
        elif obs.state == "known" and obs.confirmed_by_user:
            value = json.dumps(
                obs.value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            parts.append(f"{label}: {value}")
    for product in product_evidence:
        if product.get("status") != "verified":
            parts.append("제품 표시·버전: 미확인")
            continue
        for key in PRODUCT_FIELDS:
            value = product.get(key)
            if value is not None:
                parts.append(
                    f"제품 {key}: {json.dumps(value, ensure_ascii=False, sort_keys=True)}"
                )
    # Stop at field boundaries; do not cut a negation/unknown marker in half.
    selected = []
    size = 0
    for part in parts:
        if size + len(part) + 2 > max_chars:
            continue
        selected.append(part)
        size += len(part) + 2
    return "; ".join(selected)
