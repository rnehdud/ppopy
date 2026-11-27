"""KB v0.6.1 whitelist loader and Stage 3 deterministic NLU extraction verifier."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path

from beauty_agent.v3_contracts import NLUExtractionResult

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
    "sun.water_contact": frozenset({"yes", "no"}),
    "sun.sweat": frozenset({"yes", "no"}),
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
    enum_slot_values: dict[str, frozenset[str]]
    symptoms: dict[str, str]
    topics: frozenset[str]


@lru_cache(maxsize=4)
def load_nlu_whitelist(kb_seed_path: Path | None = None) -> NLUWhitelist:
    """Load consumer-facing non-product variable IDs from KB v0.6.1."""
    path = (kb_seed_path or DEFAULT_KB_SEED_PATH).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"KB seed file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    variable_labels: dict[str, str] = {}
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

    return NLUWhitelist(
        variable_ids=frozenset(variable_labels.keys()),
        variable_labels=variable_labels,
        enum_slot_values=ENUM_SLOT_VALUES,
        symptoms=dict(ALLOWED_SYMPTOMS),
        topics=ALLOWED_TOPICS,
    )


def verify_nlu_extraction(
    result: NLUExtractionResult,
    *,
    whitelist: NLUWhitelist | None = None,
    strict_enum_values: bool = True,
) -> NLUExtractionResult:
    """Stage 3 deterministic whitelist & source-span verifier for NLU outputs."""
    wl = whitelist if whitelist is not None else load_nlu_whitelist()
    if result.confirmed_by_user is not False:
        raise ValueError("NLUExtractionResult.confirmed_by_user must remain False")

    for topic in result.topics:
        if topic not in wl.topics:
            raise ValueError(f"topic not in allowed NLU topics: {topic!r}")

    for slot in result.slot_candidates:
        if slot.variable_id not in wl.variable_ids:
            raise ValueError(f"slot variable_id not in KB v0.6.1 NLU whitelist: {slot.variable_id!r}")
        if slot.evidence_span not in result.source_text:
            raise ValueError(f"slot evidence_span not in source_text: {slot.evidence_span!r}")
        if (
            strict_enum_values
            and slot.variable_id in wl.enum_slot_values
            and slot.polarity == "affirmed"
            and slot.value is not None
        ):
            allowed_vals = wl.enum_slot_values[slot.variable_id]
            if str(slot.value) not in allowed_vals:
                raise ValueError(
                    f"invalid enum value {slot.value!r} for {slot.variable_id!r}; "
                    f"expected one of {sorted(allowed_vals)}"
                )

    for symptom in result.symptom_candidates:
        if symptom.symptom not in wl.symptoms:
            raise ValueError(f"symptom not in allowed NLU symptoms: {symptom.symptom!r}")
        if symptom.evidence_span not in result.source_text:
            raise ValueError(f"symptom evidence_span not in source_text: {symptom.evidence_span!r}")

    return result
