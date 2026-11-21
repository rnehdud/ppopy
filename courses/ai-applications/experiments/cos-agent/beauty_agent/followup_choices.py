"""Quick replies for the runtime's KB questions and symptom confirmations."""
from __future__ import annotations

import json

from pydantic import JsonValue

from .contracts import ObservationSlot
from .runtime_contracts import CandidateConfirmationInput, QuestionChoice


# Only change display text and order here. The active KB supplies the values.
_LABELS = {
    "face": "얼굴", "hands": "손", "body": "몸", "scalp": "두피",
    "lukewarm": "미온수", "hot": "뜨거운 물", "cold": "찬물",
    "scrub_brush": "세안 브러시", "washcloth": "세안용 수건·천", "sponge": "스펀지",
    "gentle": "부드럽게 씻음", "strong": "세게 문지름",
    "pat_gently": "가볍게 눌러 닦음", "rubbing_strongly": "세게 문질러 닦음",
    "makeup_requires_removal": "메이크업이나 선크림을 지워야 함",
    "heavy_sweat": "많은 땀", "heavy_soiling": "심한 오염",
    "confirmed_removal_need": "지워야 할 잔여물이 있음",
    "no_additional_removal_need": "추가로 지울 것이 없음",
    "purpose_matched": "지울 것이 남아 다시 씻음",
    "habitual_without_reason": "별다른 이유 없이 습관으로 반복",
    "prompt_while_slightly_damp": "세안 후 피부가 살짝 촉촉할 때 바로 바름",
    "until_completely_dry": "피부가 완전히 마른 뒤 바름", "slightly_damp": "살짝 촉촉함",
    "moisturizing_not_needed_no_discomfort": "불편함이 없어 보습이 필요하지 않음",
    "moisturizing_function_used": "보습 제품을 사용함", "moisturizing_needed": "보습이 필요함",
    "comfortable": "불편함 없음", "persistent_pain": "통증이 계속됨",
    "persistent_stinging": "따가움이 계속됨", "persistent": "계속됨",
    "recurrent": "반복해서 따가움", "severe_persistent": "심한 따가움이 계속됨",
    "none": "없음", "prolonged": "야외에 오래 머묾", "yes": "예", "no": "아니요",
    "according_to_label": "제품 표시량에 맞춰 사용함", "deliberately_minimal": "일부러 아주 적게 바름",
    "repeated_only_because_water_resistant": "내수성이라는 이유로만 반복 세안함",
    "according_to_product_removal_instructions": "제품에 표시된 제거 방법을 따름",
    "matched_to_exposure_and_label": "노출 상황과 제품 표시에 맞춰 다시 바름",
    "reduced_due_to_layering": "겹쳐 바르기 어려워 덜 자주 바름", "present": "있음",
}
_FIELD_LABELS = {
    ("method.tools", "hands"): "손으로만 세안",
    ("sun.outdoor_time", "none"): "야외 활동 없음",
}
_ORDER = {value: index for index, value in enumerate(_LABELS)}
_MISSING = {"unknown": "모르겠어요 / 해당하는 답이 없어요", "declined": "건너뛰기"}

ChoiceAnswer = ObservationSlot | CandidateConfirmationInput


def observation_choices(
    field: str, values: list[JsonValue],
) -> tuple[list[QuestionChoice], dict[str, ChoiceAnswer]]:
    options = []
    answers: dict[str, ChoiceAnswer] = {}
    for index, value in enumerate(sorted(values, key=lambda value: _ORDER.get(str(value), len(_ORDER))), 1):
        choice_id = f"value-{index}"
        display = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        label = _FIELD_LABELS.get((field, display), _LABELS.get(display, display))
        options.append(QuestionChoice(id=choice_id, label=label))
        answers[choice_id] = ObservationSlot(
            variable_id=field, state="known", value=value, source="user_report", confirmed_by_user=True,
        )
    for choice_id, label in _MISSING.items():
        options.append(QuestionChoice(id=choice_id, label=label))
        answers[choice_id] = ObservationSlot(
            variable_id=field, state=choice_id, source="user_report", confirmed_by_user=True,
        )
    return options, answers


def symptom_choices(*, compact: bool = False) -> tuple[list[QuestionChoice], dict[str, ChoiceAnswer]]:
    labels = {
        "persistent": "본인에게 계속 있었음",
        "repeated": "본인에게 반복됐음",
        "recent": "본인에게 최근 한 번 있었음",
        "self_uncertain_time": "본인에게 있었으나 시점·지속 여부는 모름",
        "denied": "본인에게 없었음",
        "other": "다른 사람의 경험",
        **_MISSING,
    }
    answers: dict[str, ChoiceAnswer] = {
        "persistent": CandidateConfirmationInput(subject="self", state="affirmed", persistence="persistent"),
        "repeated": CandidateConfirmationInput(subject="self", state="affirmed", persistence="repeated"),
        "recent": CandidateConfirmationInput(subject="self", state="affirmed", persistence="recent"),
        "self_uncertain_time": CandidateConfirmationInput(subject="self", state="affirmed"),
        "denied": CandidateConfirmationInput(subject="self", state="denied"),
        "other": CandidateConfirmationInput(subject="other", state="affirmed"),
        "unknown": CandidateConfirmationInput(state="unknown"),
        "declined": CandidateConfirmationInput(state="declined"),
    }
    if compact:
        labels = {
            "recent": "본인에게 최근 한 번 있었음",
            "repeated": "본인에게 전에도 반복됐음",
            "persistent": "본인에게 계속 남아 있음",
            "unknown": "모르겠어요 · 해당하는 답이 없어요",
            "declined": "건너뛰기",
        }
        answers = {key: answers[key] for key in labels}
    return [QuestionChoice(id=choice_id, label=label) for choice_id, label in labels.items()], answers
