"""Build the model input from live retrieval without rewriting supervised labels."""

from collections.abc import Sequence
from dataclasses import dataclass

from beauty_agent.v3_contracts import RetrievalResult, SLMRequest

from .retriever import TwoStageReferenceRetriever
from .selection import Layer2Selection


@dataclass(frozen=True)
class PreparedRAGInput:
    request: SLMRequest
    retrieval: RetrievalResult


def prepare_rag_input(
    request: SLMRequest,
    retriever: TwoStageReferenceRetriever,
    *,
    source_question: str | None = None,
    source_scope: Sequence[Layer2Selection] = (),
    top_k: int = 5,
) -> PreparedRAGInput:
    """Use Tier 1 by default. An explicit document question uses its Tier 2 scope."""
    if retriever.layer2_selections:
        raise ValueError("pass a default retriever and select the source on each request")
    if source_question is not None and not source_question.strip():
        raise ValueError("source question must not be blank")
    if bool(source_question) != bool(source_scope):
        raise ValueError("document questions require both a question and an explicit source scope")
    if request.reference_question is not None and request.reference_question != source_question:
        raise ValueError("request reference_question must match the scoped question")
    if source_question is not None and request.mode != "solution":
        raise ValueError("source explanations require solution mode")

    if source_question is None:
        result = retriever.retrieve_for_request(request, top_k=top_k)
    else:
        result = retriever.for_sources(source_scope).retrieve(source_question, top_k=top_k)
    if request.mode != "solution":
        return PreparedRAGInput(request, result)

    distractors = set(request.distractor_refs)
    chunks = [chunk for chunk in result.chunks if chunk.evidence_ref not in distractors]
    allowed = [
        ref for ref in request.allowed_evidence_refs
        if ref.startswith(("catalog:", "alternative:"))
    ]
    data = request.model_dump()
    data["rag_chunks"] = [chunk.model_dump() for chunk in chunks]
    data["allowed_evidence_refs"] = list(dict.fromkeys(allowed + [c.evidence_ref for c in chunks]))
    data["reference_question"] = source_question
    prepared = SLMRequest.model_validate(data)
    return PreparedRAGInput(prepared, result.model_copy(update={"chunks": chunks}))
