"""Shared Phase 0 Pydantic contracts for Ppopy v3 End-to-End Architecture.

Defines strict inter-module I/O boundaries across:
1. 3-Stage Schema-Constrained NLU (`NLUExtractionResult`)
2. Myopic 1-Step Lookahead AFA (`AFAStepDecision`, `AFACandidateScore`)
3. Local Reference Literature Vector RAG (`RetrievalResult`, `ReferenceChunk`)
4. OpenAI-Compatible QLoRA SLM Serving (`SLMRequest`, `SLMResponse`)
5. Control Plane 1-Turn Pause/Resume & Observability (`RuntimeTurnRequestV3`, `RuntimeTurnResponseV3`, `TurnTrace`)
"""
from __future__ import annotations

from datetime import date
from hashlib import sha256
from typing import Annotated, Literal, Protocol
from urllib.parse import urlparse

from pydantic import Field, JsonValue, model_serializer, model_validator

from .contracts import Contract, ObservationSlot, OwnedProduct, Profile, Question

# ---------------------------------------------------------------------------
# Shared Enums & Constants
# ---------------------------------------------------------------------------
V3_CONTRACT_VERSION: Literal["v3.0"] = "v3.0"
SLMMode = Literal["solution", "hold", "nlu"]  # "question" mode intentionally excluded (0ms Quick Reply buttons)
AFAPolicySourceV3 = Literal["myopic_voi", "rule_baseline", "ppo_model"]
AFAStopStatusV3 = Literal["sufficient", "insufficient"]
RuntimeStatusV3 = Literal["awaiting_user", "completed", "held"]
RetrieverBackend = Literal["faiss", "chroma", "pgvector", "stub"]
ReferenceScope = Literal["general_skincare_practice", "non_clinical_only"]
CandidatePolarity = Literal["affirmed", "denied", "unknown"]
CandidateSubject = Literal["self", "other", "unknown"]
CandidateConfidence = Literal["high", "medium", "low"]
SymptomPersistence = Literal["recent", "repeated", "persistent", "unknown"]

DEFAULT_SLM_TIMEOUT_SECONDS = 15.0
MAX_SLM_RESPONSE_BYTES = 65536


# ---------------------------------------------------------------------------
# 1. NLU Layer Contracts (3-Stage Schema-Constrained NLU)
# ---------------------------------------------------------------------------
class SlotCandidate(Contract):
    """Normalized KB slot candidate extracted from free-text input."""

    variable_id: str = Field(min_length=1, max_length=120)
    value: JsonValue = None
    polarity: CandidatePolarity = "affirmed"
    subject: CandidateSubject = "self"
    confidence: CandidateConfidence = "medium"
    evidence_span: str = Field(min_length=1, max_length=300)

    @model_validator(mode="after")
    def reject_product_slot(self) -> SlotCandidate:
        if self.variable_id.startswith("product."):
            raise ValueError("product.* fields must come from catalog lookup, not user NLU slots")
        return self


class SymptomCandidateV3(Contract):
    """Unconfirmed symptom mention requiring explicit user confirmation."""

    symptom: str = Field(min_length=1, max_length=100)
    polarity: CandidatePolarity = "unknown"
    subject: CandidateSubject = "unknown"
    persistence: SymptomPersistence = "unknown"
    evidence_span: str = Field(min_length=1, max_length=300)


class ProductMentionCandidate(Contract):
    """Unconfirmed product mention with optional Stage 1 catalog hint."""

    raw_text: str = Field(min_length=1, max_length=200)
    usage_state: Literal["using", "stopped", "considering", "other_person", "unknown"] = "unknown"
    matched_catalog_hint: str | None = Field(default=None, min_length=1, max_length=150)


class NLUExtractionResult(Contract):
    """Stage 1-3 NLU output; never auto-confirms high-risk facts."""

    schema_version: Literal["v3.0"] = V3_CONTRACT_VERSION
    source_text: str = Field(min_length=1, max_length=4000)
    topics: list[str] = Field(default_factory=list)
    slot_candidates: list[SlotCandidate] = Field(default_factory=list)
    symptom_candidates: list[SymptomCandidateV3] = Field(default_factory=list)
    product_mentions: list[ProductMentionCandidate] = Field(default_factory=list)
    confirmed_by_user: Literal[False] = False

    @model_validator(mode="after")
    def verify_evidence_spans_in_source(self) -> NLUExtractionResult:
        for slot in self.slot_candidates:
            if not slot.evidence_span.strip() or slot.evidence_span not in self.source_text:
                raise ValueError(f"slot evidence_span not found in source_text: {slot.evidence_span!r}")
        for symptom in self.symptom_candidates:
            if not symptom.evidence_span.strip() or symptom.evidence_span not in self.source_text:
                raise ValueError(f"symptom evidence_span not found in source_text: {symptom.evidence_span!r}")
        return self


class CatalogHintCandidate(Contract):
    """Stage 1 offline catalog match hint passed into Stage 2 NLU."""

    raw_span: str = Field(min_length=1, max_length=200)
    matched_catalog_hint: str = Field(min_length=1, max_length=150)
    match_score: float = Field(default=1.0, ge=0.0, le=1.0)


class NLURequest(Contract):
    """Structured input contract for Stage 2 Schema-Constrained NLU SLM."""

    schema_version: Literal["v3.0"] = V3_CONTRACT_VERSION
    source_text: str = Field(min_length=1, max_length=4000)
    catalog_hints: list[CatalogHintCandidate] = Field(default_factory=list)
    previous_question: str | None = Field(default=None, max_length=500)
    target_slot_id: str | None = Field(default=None, min_length=1, max_length=120)
    allowed_variable_ids: list[str] = Field(default_factory=list)
    allowed_symptoms: list[str] = Field(default_factory=list)
    allowed_topics: list[str] = Field(default_factory=list)
    timeout_seconds: float = Field(default=DEFAULT_SLM_TIMEOUT_SECONDS, gt=0.0, le=60.0)
    max_response_bytes: int = Field(default=MAX_SLM_RESPONSE_BYTES, gt=0, le=MAX_SLM_RESPONSE_BYTES)

    @model_validator(mode="after")
    def validate_request_invariants(self) -> NLURequest:
        if self.target_slot_id is not None and self.target_slot_id.startswith("product."):
            raise ValueError("NLU target_slot_id must not target product.* catalog fields")
        for hint in self.catalog_hints:
            if not hint.raw_span.strip() or hint.raw_span not in self.source_text:
                raise ValueError(f"catalog_hint raw_span not found in source_text: {hint.raw_span!r}")
        return self


# ---------------------------------------------------------------------------
# 2. AFA Policy Contracts (Myopic 1-Step Lookahead VOI)
# ---------------------------------------------------------------------------
class AFACandidateScore(Contract):
    """Explainable per-feature lookahead metrics for TurnTrace and ITE 351 eval."""

    slot_id: str = Field(min_length=1, max_length=120)
    answer_count: int = Field(default=0, ge=0)
    expected_pruned: float = Field(default=0.0, ge=0.0)
    decision_change_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    distinct_outcomes: int = Field(default=0, ge=0)
    question_cost: float = Field(default=1.0, gt=0.0)
    safety_weight: float = Field(default=1.0, gt=0.0)
    reason: Literal[
        "selected",
        "selected_dependency",
        "lower_priority",
        "zero_impact",
        "no_branch_values",
        "already_answered",
        "product_evidence",
        "mandatory_hold",
    ]


class AFAStepDecision(Contract):
    """Single-step decision returned by AFA Policy to the Control Plane Hub."""

    action: Literal["acquire", "stop"]
    target_feature: str | None = Field(default=None, min_length=1, max_length=120)
    stop_reason: AFAStopStatusV3 | None = None
    policy_source: AFAPolicySourceV3 = "myopic_voi"

    @model_validator(mode="after")
    def validate_decision_fields(self) -> AFAStepDecision:
        if self.action == "acquire":
            if not self.target_feature or self.stop_reason is not None:
                raise ValueError("acquire requires target_feature and stop_reason=None")
            if self.target_feature.startswith("product."):
                raise ValueError("AFA must not ask users for product.* evidence")
        else:
            if self.stop_reason is None or self.target_feature is not None:
                raise ValueError("stop requires stop_reason and target_feature=None")
        return self


# ---------------------------------------------------------------------------
# 3. Reference Literature Vector RAG Contracts (SOLUTION_MODE only)
# ---------------------------------------------------------------------------
NonemptyReferenceValue = Annotated[str, Field(min_length=1, max_length=2000)]


class Layer2Metadata(Contract):
    """Version-bounded evidence, not an assertion of current product compliance.

    Unknown conditions stay verbatim. Only the audited ready export is accepted.
    Sidecar locator/limitations are retained alongside the paragraph's own fields.
    """

    unit_id: str = Field(pattern=r"^L2U-\d{4}$")
    source_id: NonemptyReferenceValue
    topic: Literal["regulatory", "safety_method"]
    language: NonemptyReferenceValue
    text_type: Literal["independently_worded_summary"]
    source_url: NonemptyReferenceValue
    locator: NonemptyReferenceValue
    document_version: NonemptyReferenceValue
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    checked_on: NonemptyReferenceValue
    as_of: NonemptyReferenceValue
    jurisdiction: NonemptyReferenceValue
    scope: ReferenceScope
    limitations: NonemptyReferenceValue
    subject_identity: NonemptyReferenceValue
    product_type: NonemptyReferenceValue
    concentration_basis: NonemptyReferenceValue
    exposure_route: NonemptyReferenceValue
    population: NonemptyReferenceValue
    version_status: NonemptyReferenceValue
    effective_period: NonemptyReferenceValue
    verification_status: Literal["ready"]
    use_basis: NonemptyReferenceValue
    section_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    body_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    permitted_use: Literal["source_explanation_only"] = "source_explanation_only"

    @model_validator(mode="after")
    def validate_provenance(self) -> Layer2Metadata:
        if any(isinstance(v, str) and not v.strip() for v in self.model_dump().values()):
            raise ValueError("layer2 metadata must not be blank")
        if urlparse(self.source_url).scheme != "https" or not urlparse(self.source_url).netloc:
            raise ValueError("layer2 source must be an HTTPS URL")
        date.fromisoformat(self.checked_on)
        return self


class ReferenceChunk(Contract):
    """Single non-clinical literature/guideline chunk returned by Vector RAG."""

    evidence_ref: str = Field(min_length=5, max_length=150)
    text: str = Field(min_length=1, max_length=4000)
    scope: ReferenceScope = "general_skincare_practice"
    source_url: str = Field(min_length=1, max_length=500)
    locator: str = Field(min_length=1, max_length=200)
    checked_on: str = Field(min_length=1, max_length=40)
    limitations: str = Field(min_length=1, max_length=500)

    layer2: Layer2Metadata | None = None

    @model_serializer(mode="wrap")
    def preserve_layer1_wire(self, handler):
        data = handler(self)
        if self.layer2 is None:
            data.pop("layer2", None)
        return data

    @model_validator(mode="after")
    def validate_ref_prefix(self) -> ReferenceChunk:
        if not self.evidence_ref.startswith("ref:"):
            raise ValueError("ReferenceChunk evidence_ref must start with 'ref:'")
        is_layer2_ref = self.evidence_ref.startswith(("ref:regulatory-", "ref:safety_method-"))
        if self.layer2 is not None:
            meta = self.layer2
            if self.evidence_ref != f"ref:{meta.topic}-{meta.unit_id}":
                raise ValueError("layer2 stable evidence_ref mismatch")
            if any(getattr(self, key) != getattr(meta, key)
                   for key in ("source_url", "checked_on", "scope")):
                raise ValueError("layer2 provenance mismatch")
            if sha256(self.text.encode()).hexdigest() != meta.body_sha256:
                raise ValueError("layer2 body checksum mismatch")
        elif is_layer2_ref:
            raise ValueError("layer2 evidence requires audited metadata")
        return self


class RetrievalResult(Contract):
    """Output of the Local Reference Literature Vector RAG Retriever."""

    chunks: list[ReferenceChunk] = Field(default_factory=list)
    index_version: str = Field(min_length=1, max_length=80)
    retriever_backend: RetrieverBackend = "stub"


class ReferenceRetriever(Protocol):
    """Swappable Retriever interface (local FAISS/Chroma -> future AWS Aurora pgvector)."""

    def retrieve(self, query: str, *, top_k: int = 5) -> RetrievalResult: ...


# ---------------------------------------------------------------------------
# 4. OpenAI-Compatible QLoRA SLM Contracts (NO QUESTION_MODE)
# ---------------------------------------------------------------------------
class SLMRequest(Contract):
    """Structured request sent from Control Plane to the OpenAI-Compatible SLM server.

    KB judgments are intentionally excluded: KB scope is strictly limited to AFA/Runtime.
    """

    mode: SLMMode
    confirmed_observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    product_evidence: list[dict[str, JsonValue]] = Field(default_factory=list)
    rag_chunks: list[ReferenceChunk] = Field(default_factory=list)
    allowed_evidence_refs: list[str] = Field(default_factory=list)
    distractor_refs: list[str] = Field(default_factory=list)
    timeout_seconds: float = Field(default=DEFAULT_SLM_TIMEOUT_SECONDS, gt=0.0, le=60.0)
    max_response_bytes: int = Field(default=MAX_SLM_RESPONSE_BYTES, gt=0, le=MAX_SLM_RESPONSE_BYTES)

    @model_validator(mode="after")
    def validate_mode_and_refs(self) -> SLMRequest:
        if self.mode != "solution" and self.rag_chunks:
            raise ValueError("rag_chunks are only permitted in 'solution' mode")
        overlap = set(self.allowed_evidence_refs) & set(self.distractor_refs)
        if overlap:
            raise ValueError(f"allowed_evidence_refs and distractor_refs must be disjoint: {sorted(overlap)}")
        return self


class SLMResponse(Contract):
    """Response returned by the SLM client (or deterministic fallback)."""

    mode: SLMMode
    content: str = Field(min_length=1, max_length=16000)
    cited_evidence_refs: list[str] = Field(default_factory=list)
    provider: Literal["openai_compat", "rule_baseline_fallback"] = "openai_compat"
    model: str | None = None
    adapter_revision: str | None = None
    fallback_used: bool = False
    fallback_reason: str | None = None


class SolutionGenerator(Protocol):
    """Async client interface for OpenAI-Compatible /v1/chat/completions SLM serving."""

    async def generate(self, request: SLMRequest) -> SLMResponse: ...


# ---------------------------------------------------------------------------
# 5. Control Plane 1-Turn Pause/Resume & Observability Contracts
# ---------------------------------------------------------------------------
class QuestionChoiceV3(Contract):
    id: str = Field(min_length=1, max_length=100)
    label: str = Field(min_length=1, max_length=200)


class RuntimeQuestionV3(Question):
    turn_index: int = Field(ge=1)
    choices: list[QuestionChoiceV3] = Field(default_factory=list)


class ChoiceSelectionV3(Contract):
    turn_index: int = Field(ge=1)
    question_id: str = Field(min_length=1, max_length=120)
    choice_id: str = Field(min_length=1, max_length=100)


class RuntimeTurnRequestV3(Contract):
    """Single-turn request shared by Thin CLI Wrapper and future iOS HTTP API."""

    schema_version: Literal["v3.0"] = V3_CONTRACT_VERSION
    deployment_context: Literal["synthetic_test"] = "synthetic_test"
    request_id: str = Field(min_length=1, max_length=120)
    message: str = Field(default="", max_length=4000)
    profile: Profile | None = None
    products: list[OwnedProduct] | None = None
    observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    choice_selection: ChoiceSelectionV3 | None = None

    @model_validator(mode="after")
    def validate_fast_path_exclusivity(self) -> RuntimeTurnRequestV3:
        if self.choice_selection is not None and (
            self.message.strip() or self.observations or self.profile is not None or self.products is not None
        ):
            raise ValueError("choice_selection fast-path must be submitted without free-text or raw mutations")
        return self


class TurnTrace(Contract):
    """Per-turn observability trace for debugging and ITE 351 evaluation."""

    request_id: str = Field(min_length=1, max_length=120)
    turn_index: int = Field(ge=1)
    nlu_skipped_fast_path: bool = False
    afa_decision: AFAStepDecision | None = None
    afa_scores: list[AFACandidateScore] = Field(default_factory=list)
    rag_chunk_refs: list[str] = Field(default_factory=list)
    slm_mode: SLMMode | None = None
    slm_fallback_used: bool = False
    guardrail_flags: list[str] = Field(default_factory=list)
    latency_ms: dict[str, float] = Field(default_factory=dict)


class RuntimeTurnResponseV3(Contract):
    """Single-turn response enforcing preview, approval, and non-persistence invariants."""

    schema_version: Literal["v3.0"] = V3_CONTRACT_VERSION
    mode: Literal["development_preview"] = "development_preview"
    production_enabled: Literal[False] = False
    request_id: str = Field(min_length=1, max_length=120)
    status: RuntimeStatusV3
    message: str = Field(default="", max_length=16000)
    questions: list[RuntimeQuestionV3] = Field(default_factory=list)
    hold_reason: str | None = Field(default=None, max_length=1000)
    evidence_refs: list[str] = Field(default_factory=list)
    requires_approval: Literal[True] = True
    saved: Literal[False] = False
    trace: TurnTrace | None = None
