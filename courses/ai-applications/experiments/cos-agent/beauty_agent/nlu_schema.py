"""KB v0.6.1 whitelist loader and Stage 3 deterministic NLU extraction verifier."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from beauty_agent.v3_contracts import NLUExtractionResult, NLURequest

_COS_AGENT_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = next(
    (p for p in _COS_AGENT_ROOT.parents if (p / "KB" / "Poppy_KB_v0.6.1").is_dir()),
    _COS_AGENT_ROOT,
)
DEFAULT_KB_SEED_PATH = _REPO_ROOT / "KB" / "Poppy_KB_v0.6.1" / "Poppy_KB_seed_v0.6.1.json"

ENUM_SLOT_VALUES: dict[str, frozenset[str]] = {
    "method.body_site": frozenset({"face", "hands", "body", "scalp"}),
    "method.water_temperature": frozenset({"lukewarm", "hot", "cold"}),
    "method.tools": frozenset({"hands", "scrub_brush", "washcloth", "sponge"}),
    "method.friction": frozenset({"gentle", "strong"}),
    "method.drying": frozenset({"pat_gently", "rubbing_strongly"}),
    "cleansing.target_load": frozenset({
        "makeup_requires_removal",
        "heavy_sweat",
        "heavy_soiling",
        "confirmed_removal_need",
        "no_additional_removal_need",
    }),
    "cleansing.repeat_wash": frozenset({
        "purpose_matched",
        "habitual_without_reason",
    }),
    "sun.outdoor_time": frozenset({"none", "prolonged"}),
    "sun.water_contact": frozenset({"yes", "no", "none"}),
    "sun.sweat": frozenset({"yes", "no", "none"}),
}

# Canonical symbolic strings used by executable KB preview rules (e.g. B-I01:2)
# alongside numeric counts for integer-typed KB variables.
CANONICAL_RULE_SLOT_STRINGS: dict[str, frozenset[str]] = {
    "cleansing.steps": frozenset({
        "repeated_only_because_water_resistant",
        "according_to_product_removal_instructions",
    }),
}

ALLOWED_SYMPTOMS: dict[str, str] = {
    "dryness": "건조함",
    "breakout": "트러블",
    "redness": "붉어짐",
    "stinging": "따가움",
    "itching": "가려움",
    "pain": "통증",
    "burning": "화끈거림",
    "swelling": "부어오름",
    "eye_stinging": "눈 시림/따가움",
    "peeling": "각질/벗겨짐",
    "tightness": "당김",
}

ALLOWED_TOPICS: frozenset[str] = frozenset({
    "outdoor_sun",
    "cleansing_method",
    "repeat_cleansing",
    "moisturizing",
    "discomfort_report",
    "storage_label",
    "routine_conflict",
    "other",
})


@dataclass(frozen=True)
class NLUWhitelist:
    """Canonical NLU target vocabulary derived from Poppy_KB_seed_v0.6.1.json."""

    variable_ids: frozenset[str]
    variable_labels: dict[str, str]
    variable_value_types: dict[str, str]
    enum_slot_values: dict[str, frozenset[str]]
    symptoms: dict[str, str]
    topics: frozenset[str]


@lru_cache(maxsize=4)
def load_nlu_whitelist(kb_seed_path: Path | None = None) -> NLUWhitelist:
    """Load consumer-facing non-product variable IDs and value types from KB v0.6.1."""
    path = (kb_seed_path or DEFAULT_KB_SEED_PATH).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"KB seed file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    variable_labels: dict[str, str] = {}
    variable_value_types: dict[str, str] = {}
    for var in payload.get("variables", []):
        vid = var.get("id")
        if not isinstance(vid, str) or not vid:
            continue
        if vid.startswith("product."):
            continue
        if var.get("consumer_question_allowed") is not True:
            continue
        label = var.get("label")
        variable_labels[vid] = label if isinstance(label, str) and label else vid
        vtype = var.get("value_type")
        variable_value_types[vid] = vtype if isinstance(vtype, str) and vtype else "structured"

    return NLUWhitelist(
        variable_ids=frozenset(variable_labels.keys()),
        variable_labels=variable_labels,
        variable_value_types=variable_value_types,
        enum_slot_values=ENUM_SLOT_VALUES,
        symptoms=dict(ALLOWED_SYMPTOMS),
        topics=ALLOWED_TOPICS,
    )


def _validate_non_enum_value(variable_id: str, value: Any, value_type: str) -> None:
    """Enforce KB value_type hygiene for non-enum slots (rejects arbitrary dicts/bad types)."""
    if value is None:
        return
    if isinstance(value, dict):
        raise ValueError(f"slot {variable_id!r} must not use an arbitrary dict value: {value!r}")

    if value_type in {"categorical", "ordinal", "string", "datetime"}:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"slot {variable_id!r} ({value_type}) requires a non-empty string value, got {value!r}")
    elif value_type == "integer":
        canonical_strings = CANONICAL_RULE_SLOT_STRINGS.get(variable_id, frozenset())
        if isinstance(value, str) and value in canonical_strings:
            return
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"slot {variable_id!r} (integer) requires an int"
                + (f" or one of {sorted(canonical_strings)}" if canonical_strings else "")
                + f", got {value!r}"
            )
    elif value_type == "quantity":
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValueError(f"slot {variable_id!r} (quantity) requires a number or string value, got {value!r}")
    elif value_type == "array":
        # PreviewEngine matches scalar symbolic strings (e.g. sun.coverage_gaps="none")
        # as well as list[str] for array-typed KB variables.
        if isinstance(value, str):
            if not value.strip():
                raise ValueError(f"slot {variable_id!r} (array) string value must not be blank")
        elif not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            raise ValueError(f"slot {variable_id!r} (array) requires a non-empty string or list[str], got {value!r}")
    else:
        if isinstance(value, str):
            if not value.strip():
                raise ValueError(f"slot {variable_id!r} string value must not be blank")
        elif isinstance(value, bool):
            return
        elif isinstance(value, list):
            if not all(isinstance(item, str) and item.strip() for item in value):
                raise ValueError(f"slot {variable_id!r} list value must contain non-empty strings, got {value!r}")
        else:
            raise ValueError(
                f"slot {variable_id!r} ({value_type}) requires a string, bool, or list[str], got {value!r}"
            )


def verify_nlu_extraction(
    result: NLUExtractionResult,
    *,
    request: NLURequest,
    whitelist: NLUWhitelist | None = None,
    strict_enum_values: bool = True,
) -> NLUExtractionResult:
    """Stage 3 deterministic whitelist, value-type, catalog-hint & source-span verifier."""
    if not isinstance(request, NLURequest):
        raise ValueError("Stage 3 verification requires the original NLURequest")

    wl = whitelist if whitelist is not None else load_nlu_whitelist()
    if result.confirmed_by_user is not False:
        raise ValueError("NLUExtractionResult.confirmed_by_user must remain False")

    if request.source_text != result.source_text:
        raise ValueError("NLUExtractionResult.source_text does not match NLURequest.source_text")
    if request.target_slot_id is not None and request.target_slot_id not in wl.variable_ids:
        raise ValueError(f"request target_slot_id not in KB v0.6.1 whitelist: {request.target_slot_id!r}")

    req_allowed_vars = set(request.allowed_variable_ids)
    req_allowed_symptoms = set(request.allowed_symptoms)
    req_allowed_topics = set(request.allowed_topics)
    for vid in req_allowed_vars:
        if vid not in wl.variable_ids:
            raise ValueError(f"request allowed_variable_ids contains unknown variable: {vid!r}")
    for sym in req_allowed_symptoms:
        if sym not in wl.symptoms:
            raise ValueError(f"request allowed_symptoms contains unknown symptom: {sym!r}")
    for top in req_allowed_topics:
        if top not in wl.topics:
            raise ValueError(f"request allowed_topics contains unknown topic: {top!r}")

    source_text = request.source_text

    for topic in result.topics:
        if topic not in wl.topics:
            raise ValueError(f"topic not in allowed NLU topics: {topic!r}")
        if req_allowed_topics and topic not in req_allowed_topics:
            raise ValueError(f"topic {topic!r} not in request.allowed_topics")

    for slot in result.slot_candidates:
        if slot.variable_id not in wl.variable_ids:
            raise ValueError(f"slot variable_id not in KB v0.6.1 NLU whitelist: {slot.variable_id!r}")
        if req_allowed_vars and slot.variable_id not in req_allowed_vars:
            raise ValueError(f"slot variable_id {slot.variable_id!r} not in request.allowed_variable_ids")
        if not slot.evidence_span.strip():
            raise ValueError("slot evidence_span must not be whitespace-only")
        if slot.evidence_span not in source_text:
            raise ValueError(f"slot evidence_span not in source_text: {slot.evidence_span!r}")

        if slot.polarity == "unknown":
            if slot.value is not None:
                raise ValueError(
                    f"slot {slot.variable_id!r} with polarity='unknown' must have value=None, got {slot.value!r}"
                )
        elif strict_enum_values and slot.variable_id in wl.enum_slot_values:
            allowed_vals = wl.enum_slot_values[slot.variable_id]
            if not isinstance(slot.value, str) or slot.value not in allowed_vals:
                raise ValueError(
                    f"invalid enum value {slot.value!r} for {slot.variable_id!r} (polarity={slot.polarity!r}); "
                    f"expected one of {sorted(allowed_vals)}"
                )
        else:
            vtype = wl.variable_value_types.get(slot.variable_id, "structured")
            _validate_non_enum_value(slot.variable_id, slot.value, vtype)

    for symptom in result.symptom_candidates:
        if symptom.symptom not in wl.symptoms:
            raise ValueError(f"symptom not in allowed NLU symptoms: {symptom.symptom!r}")
        if req_allowed_symptoms and symptom.symptom not in req_allowed_symptoms:
            raise ValueError(f"symptom {symptom.symptom!r} not in request.allowed_symptoms")
        if not symptom.evidence_span.strip():
            raise ValueError("symptom evidence_span must not be whitespace-only")
        if symptom.evidence_span not in source_text:
            raise ValueError(f"symptom evidence_span not in source_text: {symptom.evidence_span!r}")

    for mention in result.product_mentions:
        if not mention.raw_text.strip():
            raise ValueError("product mention raw_text must not be whitespace-only")
        if mention.raw_text not in source_text:
            raise ValueError(f"product mention raw_text not in source_text: {mention.raw_text!r}")
        if mention.matched_catalog_hint is not None:
            matched = any(
                hint.matched_catalog_hint == mention.matched_catalog_hint
                and hint.raw_span.strip() == mention.raw_text.strip()
                for hint in request.catalog_hints
            )
            if not matched:
                raise ValueError(
                    f"product mention matched_catalog_hint {mention.matched_catalog_hint!r} "
                    f"for {mention.raw_text!r} is not grounded in an exact matching request.catalog_hints span"
                )

    return result
