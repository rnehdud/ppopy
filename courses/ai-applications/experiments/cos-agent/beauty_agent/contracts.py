from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


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
