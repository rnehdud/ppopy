from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Profile(Contract):
    confirmed: bool = False
    concerns: list[str] = Field(default_factory=list, max_length=10)
    excluded_product_ids: list[str] = Field(default_factory=list, max_length=30)


class OwnedProduct(Contract):
    product_id: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=100)
    confirmed: bool = False


class TurnRequest(Contract):
    schema_version: Literal["0.1.0"] = "0.1.0"
    deployment_context: Literal["synthetic_test"]
    device: Literal["ios", "smart_mirror", "web"]
    message: str = Field(default="", max_length=2000)
    profile: Profile
    products: list[OwnedProduct] = Field(max_length=30)

    @model_validator(mode="after")
    def unique_products(self):
        ids = [p.product_id for p in self.products]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate product IDs")
        return self


class Question(Contract):
    id: str
    text: str


class Step(Contract):
    product_id: str
    version: str
    period: Literal["am", "pm"]
    label_instruction: str
    evidence_id: str


class Draft(Contract):
    draft_hash: str
    rule_version: str
    steps: list[Step]
    requires_approval: Literal[True] = True
    saved: Literal[False] = False


class TurnResponse(Contract):
    schema_version: Literal["0.1.0"] = "0.1.0"
    status: Literal["needs_information", "draft"]
    message: str
    questions: list[Question]
    draft: Draft | None = None
    provider: Literal["baseline", "ollama", "baseline_fallback"]
    model: str | None = None
    limitation: str = "합성 제품 사용법을 배열한 기술 데모이며 실제 개인화·효능 판단 결과가 아닙니다."


class ObservationSlot(Contract):
    variable_id: str
    state: Literal["known", "unknown", "not_asked", "declined", "conflicting", "not_applicable"] = "unknown"
    # Preserve JSON types recursively, including numeric counts and structured
    # KB answers. In particular, integer 0/1 must not become boolean values.
    value: JsonValue = None
    source: Literal["user_report", "synthetic_fixture", "automated_extraction"] = "user_report"
    confirmed_by_user: bool = False

    @model_validator(mode="after")
    def known_requires_value(self):
        if self.state == "known" and self.value is None:
            raise ValueError("known observation requires a value")
        if self.confirmed_by_user and self.source == "automated_extraction":
            raise ValueError("automated extraction cannot be user confirmation")
        return self


class PipelineTrace(Contract):
    mode: Literal["development_preview"] = "development_preview"
    production_enabled: Literal[False] = False
    jev_products: list[str] = Field(default_factory=list)
    jev_symptoms: list[dict] = Field(default_factory=list)
    jev_clarifications: list[str] = Field(default_factory=list)
    jev_warnings: list[str] = Field(default_factory=list)
    mapping_findings: list[dict] = Field(default_factory=list)
    mapping_warnings: list[str] = Field(default_factory=list)
    kb_evaluated_cards: list[str] = Field(default_factory=list)
    kb_missing_ask_slots: list[str] = Field(default_factory=list)
    kb_retrieve_slots: list[str] = Field(default_factory=list)
    hold_signals: list[str] = Field(default_factory=list)
    pending_clarifications: dict[str, str] = Field(default_factory=dict)
    selected_route: Literal["ask_user", "retrieve_product", "hold_or_escalate", "ready_for_draft"] = "ask_user"


class PlannerOutput(Contract):
    provider: Literal["baseline", "ollama", "baseline_fallback"] = "baseline"
    model: str | None = None
    route: Literal["ask_user", "retrieve_product", "hold_or_escalate"] = "ask_user"
    # OwnedProduct permits 100 characters; the longest blocker prefix is
    # "resolve:" (8 characters). Keep the original blocker ID intact.
    target_slot: str = Field(default="general", max_length=108)
    question_id: str = Field(default="contextual_followup", max_length=108)
    question_ko: str = Field(min_length=1, max_length=500)
    reasoning_summary: str = Field(default="", max_length=500)


class PipelineTurnResponse(TurnResponse):
    """Opt-in response; the existing HTTP response schema stays unchanged."""
    trace: PipelineTrace
