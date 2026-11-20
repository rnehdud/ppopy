"""Shared Pydantic contracts for the Python Agent Runtime, NLP Layer, AFA Loop, and CLI/iOS wrapper."""
from __future__ import annotations

from typing import Literal, Protocol

from pydantic import Field, JsonValue, model_validator

from .contracts import Contract, ObservationSlot, OwnedProduct, Profile, Question

RuntimeActionKind = Literal[
    "ask_user",
    "confirm_candidate",
    "resolve_conflict",
    "lookup_weather",
    "lookup_product",
    "lookup_alternative",
    "recommend",
    "hold",
]

ToolStatus = Literal["found", "not_found", "failed"]
ExclusionDisposition = Literal[
    "candidate_excluded",
    "usage_held",
    "verified_contraindication",
]
RuntimeStatus = Literal["awaiting_user", "completed", "held"]
AFAPolicySource = Literal["rule_baseline", "ppo_model"]
AFAStopStatus = Literal["sufficient", "insufficient"]


class ProductQueryCandidate(Contract):
    """Unconfirmed product mention extracted for catalog/external lookup."""

    text: str = Field(min_length=1, max_length=200)
    usage_state: str = "unknown"
    subject: str = "unknown"
    correction: str = "unknown"
    confirmed_ownership: Literal[False] = False


class SymptomCandidate(Contract):
    """Unconfirmed symptom mention requiring explicit user/time confirmation."""

    candidate_id: str = Field(min_length=1, max_length=120)
    symptom: str = Field(min_length=1, max_length=100)
    label: str = Field(min_length=1, max_length=100)
    state: str = "unknown"
    subject: str = "unknown"
    requires_confirmation: Literal[True] = True
    prompt_ko: str = Field(min_length=1, max_length=500)


class CandidateConfirmationInput(Contract):
    """Explicit user confirmation for an unconfirmed NLP symptom candidate."""

    subject: Literal["self", "other", "unknown"] = "unknown"
    state: Literal["affirmed", "denied", "unknown", "declined"]
    persistence: Literal["recent", "repeated", "persistent", "unknown"] = "unknown"
    observed_at: str | None = None


class FeatureCandidate(Contract):
    """Unconfirmed KB slot value extracted from natural-language utterance."""

    slot_id: str = Field(min_length=1, max_length=120)
    state: Literal["known", "unknown", "declined"] = "known"
    value: str | None = None
    confirmed_by_user: Literal[False] = False


class NLPExtractionResult(Contract):
    """Unified output of the Kiwi -> Jev -> MappingReview NLP Layer."""

    schema_version: Literal["nlp-layer-0.1"] = "nlp-layer-0.1"
    source_text: str
    source_mode: Literal["remote_jev", "offline_kiwi_fallback", "injected_extractor"]
    segmentation_method: str
    units: list[dict[str, JsonValue]] = Field(default_factory=list)
    product_queries: list[ProductQueryCandidate] = Field(default_factory=list)
    symptom_candidates: list[SymptomCandidate] = Field(default_factory=list)
    feature_candidates: list[FeatureCandidate] = Field(default_factory=list)
    topic_hints: list[str] = Field(default_factory=list)
    mapping_findings: list[dict[str, JsonValue]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    extraction_failed: bool = False
    confirmed_by_user: Literal[False] = False


class AFAStepDecision(Contract):
    """Single-step decision inside the AFA-Policy feature acquisition loop."""

    action: Literal["acquire", "stop"]
    target_feature: str | None = Field(default=None, min_length=1, max_length=120)
    stop_reason: AFAStopStatus | None = None
    policy_source: AFAPolicySource = "rule_baseline"

    @model_validator(mode="after")
    def validate_step_fields(self) -> AFAStepDecision:
        if self.action == "acquire":
            if not self.target_feature or self.stop_reason is not None:
                raise ValueError("acquire requires target_feature and stop_reason=None")
        else:
            if self.stop_reason is None or self.target_feature is not None:
                raise ValueError("stop requires stop_reason and target_feature=None")
        return self

    @classmethod
    def from_legacy_action(
        cls,
        kind: str,
        target_id: str,
        *,
        policy_source: AFAPolicySource = "rule_baseline",
    ) -> AFAStepDecision:
        """Map existing E26 PPO (action, target_id) pairs to AFAStepDecision."""
        if kind == "ask_user":
            return cls(action="acquire", target_feature=target_id, policy_source=policy_source)
        if kind == "request_draft":
            return cls(action="stop", stop_reason="sufficient", policy_source=policy_source)
        if kind == "hold":
            return cls(action="stop", stop_reason="insufficient", policy_source=policy_source)
        raise ValueError(f"unsupported legacy AFA action: {kind}")


class AFAHandoffResult(Contract):
    """Final payload handed off from AFA-Policy to Agent Runtime when acquisition stops."""

    status: AFAStopStatus
    acquired_features: dict[str, ObservationSlot] = Field(default_factory=dict)
    asked_feature_order: list[str] = Field(default_factory=list)
    unanswered_or_declined: list[str] = Field(default_factory=list)
    policy_source: AFAPolicySource = "rule_baseline"


class QuestionCandidate(Contract):
    slot_id: str
    question_text: str
    card_ids: list[str] = Field(default_factory=list)


class AFAPolicy(Protocol):
    """Plugin interface for the AFA feature-acquisition policy."""

    def decide_step(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        can_stop_sufficient: bool,
        can_stop_insufficient: bool = True,
    ) -> AFAStepDecision: ...


class QuestionSelector(Protocol):
    """Compatibility protocol for simple slot selection."""

    def select_question(
        self,
        observations: dict[str, ObservationSlot],
        candidates: list[QuestionCandidate],
        context_meta: dict[str, JsonValue],
    ) -> str: ...


class ToolLookupResult(Contract):
    tool_name: Literal["weather", "product_catalog", "alternative_search"]
    query_key: str = Field(min_length=1, max_length=120)
    status: ToolStatus
    source: str = Field(min_length=1, max_length=120)
    version: str | None = None
    observed_at: str | None = None
    data: dict[str, JsonValue] = Field(default_factory=dict)
    error_reason: str | None = None


class ExclusionItem(Contract):
    product_id: str = Field(min_length=1, max_length=100)
    disposition: ExclusionDisposition
    reason: str = Field(min_length=1, max_length=300)
    evidence_refs: list[str] = Field(default_factory=list)


class RecommendationItem(Contract):
    category: Literal["lifestyle_adjustment", "owned_product_usage", "alternative_candidate"]
    title: str
    guidance: str
    product_id: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class RecommendationBundle(Contract):
    lifestyle_adjustments: list[RecommendationItem] = Field(default_factory=list)
    owned_product_usage: list[RecommendationItem] = Field(default_factory=list)
    exclusions_or_holds: list[ExclusionItem] = Field(default_factory=list)
    alternatives: list[RecommendationItem] = Field(default_factory=list)
    requires_approval: Literal[True] = True
    saved: Literal[False] = False


class RuntimeSessionState(Contract):
    mode: Literal["development_preview"] = "development_preview"
    production_enabled: Literal[False] = False
    request_id: str
    turn_index: int = 0
    status: RuntimeStatus = "awaiting_user"
    profile: Profile = Field(default_factory=Profile)
    products: list[OwnedProduct] = Field(default_factory=list)
    confirmed_observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    active_cards: list[str] = Field(default_factory=list)
    card_selection_reasons: dict[str, list[str]] = Field(default_factory=dict)
    unrecognized_fields: list[str] = Field(default_factory=list)
    asked_feature_order: list[str] = Field(default_factory=list)
    afa_handoff: AFAHandoffResult | None = None
    pending_question: Question | None = None
    pending_action: RuntimeActionKind | None = None
    last_turn_fingerprint: str | None = None
    tool_results: dict[str, ToolLookupResult] = Field(default_factory=dict)
    pending_candidates: list[SymptomCandidate] = Field(default_factory=list)
    confirmed_candidates: dict[str, CandidateConfirmationInput] = Field(default_factory=dict)
    history: list[dict[str, JsonValue]] = Field(default_factory=list)


class RuntimeTurnRequest(Contract):
    deployment_context: Literal["synthetic_test"] = "synthetic_test"
    request_id: str
    message: str = ""
    profile: Profile | None = None
    products: list[OwnedProduct] | None = None
    observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    confirmations: dict[str, CandidateConfirmationInput] = Field(default_factory=dict)
    resolve_conflicts: tuple[str, ...] = ()


class RuntimeTurnResponse(Contract):
    mode: Literal["development_preview"] = "development_preview"
    production_enabled: Literal[False] = False
    request_id: str
    status: RuntimeStatus
    executed_actions: list[RuntimeActionKind] = Field(default_factory=list)
    pending_action: RuntimeActionKind | None = None
    questions: list[Question] = Field(default_factory=list)
    nlp: NLPExtractionResult | None = None
    afa_handoff: AFAHandoffResult | None = None
    recommendation: RecommendationBundle | None = None
    hold_reason: str | None = None
    required_product_evidence: list[str] = Field(default_factory=list)
    tool_results: dict[str, ToolLookupResult] = Field(default_factory=dict)
