"""Explicit, version-bounded retrieval eligibility for the tier-2 corpus."""

from typing import Literal

from pydantic import ConfigDict, model_validator

from beauty_agent.contracts import Contract
from beauty_agent.v3_contracts import NonemptyReferenceValue, ReferenceChunk


class Layer2Selection(Contract):
    """Caller-selected source explanation; never inferred from query keywords.

    Exact fields intentionally distinguish a scientific opinion from legislation
    in the same region. No wildcards, date inference, or product-safety mode.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)
    source_id: NonemptyReferenceValue
    jurisdiction: NonemptyReferenceValue
    document_version: NonemptyReferenceValue
    as_of: NonemptyReferenceValue
    purpose: Literal["source_explanation_only"]

    @model_validator(mode="after")
    def nonblank(self):
        if any(
            not v.strip() or v.strip().lower() in {"*", "unknown", "not_stated"}
            for v in self.model_dump().values()
        ):
            raise ValueError("explicit known source selection required")
        return self

    def matches(self, chunk: ReferenceChunk) -> bool:
        meta = chunk.layer2
        return (
            meta is not None
            and meta.verification_status == "ready"
            and all(
                getattr(meta, field) == getattr(self, field)
                for field in ("source_id", "jurisdiction", "document_version", "as_of")
            )
            and meta.permitted_use == self.purpose
        )
