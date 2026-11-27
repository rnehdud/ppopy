import json
from copy import copy
from pathlib import Path

import pytest

from beauty_agent.contracts import ObservationSlot
from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.corpus import load_corpus_entries
from beauty_agent.rag.handoff import prepare_rag_input
from beauty_agent.rag.retriever import TwoStageReferenceRetriever
from beauty_agent.slm import build_messages
from beauty_agent.v3_contracts import SLMRequest
from scripts.export_rag_contexts import SourceQuestion, export_rows

DATA = Path(__file__).resolve().parents[1] / "data" / "rag"


@pytest.fixture(scope="module")
def rag():
    entries = load_corpus_entries(
        DATA / "corpus", additional_corpus_dirs=[DATA / "layer2" / "corpus"],
    )
    return TwoStageReferenceRetriever(
        entries, HashFallback(), NoOpReranker(), threshold=-1,
    )


def dataset_row(row_id, request, *, answer="검수 대상입니다."):
    return {
        "id": row_id,
        "mode": request.mode,
        "split": "train",
        "messages": build_messages(request) + [{"role": "assistant", "content": answer}],
    }


def test_combined_index_scopes_each_row_without_leaking_to_next(rag):
    solution = SLMRequest(
        mode="solution",
        confirmed_observations={
            "method.body_site": ObservationSlot(
                variable_id="method.body_site", state="known", value="face", confirmed_by_user=True,
            ),
        },
        allowed_evidence_refs=["ref:cleansing-999", "catalog:fixture@v1"],
    )
    hold = SLMRequest(mode="hold")
    original = [
        dataset_row("document", solution, answer="검수 대상 [ref:cleansing-999]"),
        dataset_row("routine", solution),
        dataset_row("hold", hold),
    ]
    snapshot = json.dumps(original)
    document, routine, deferred = export_rows(original, rag, {
        "document": SourceQuestion(question="SCCS exposure assessment", source_unit="L2U-0001"),
    })

    assert document["retrieval"]["chunks"]
    assert {chunk["layer2"]["source_id"] for chunk in document["retrieval"]["chunks"]} == {
        "L2S-SCCS-1647-22-C2"
    }
    sent = json.loads(document["model_messages"][1]["content"])
    assert sent["reference_question"] == "SCCS exposure assessment"
    assert set(sent["allowed_evidence_refs"]) == {
        "catalog:fixture@v1", *(chunk["evidence_ref"] for chunk in sent["rag_chunks"]),
    }
    assert document["missing_target_refs"] == ["ref:cleansing-999"]
    assert document["requires_target_review"]
    assert routine["retrieval"]["chunks"]
    assert all("layer2" not in chunk for chunk in routine["retrieval"]["chunks"])
    assert "reference_question" not in json.loads(routine["model_messages"][1]["content"])
    assert routine["retrieval"]["index_version"] != document["retrieval"]["index_version"]
    assert deferred["retrieval"]["chunks"] == []
    assert deferred["model_messages"] == build_messages(hold)
    assert json.dumps(original) == snapshot


def test_document_miss_does_not_export_a_prompt(rag):
    row = dataset_row("document", SLMRequest(mode="solution"))
    strict = copy(rag)
    strict.threshold = 1.0
    result, = export_rows([row], strict, {
        "document": SourceQuestion(question="unrelated query xyz", source_unit="L2U-0001"),
    })
    assert result["retrieval"]["chunks"] == []
    assert result["model_messages"] is None
    assert result["requires_target_review"]


def test_blank_document_question_is_rejected(rag):
    row = dataset_row("document", SLMRequest(mode="solution"))
    with pytest.raises(ValueError, match="not be blank"):
        export_rows([row], rag, {
            "document": SourceQuestion(question="   ", source_unit="L2U-0001"),
        })


def test_source_explanation_scope_is_required(rag):
    with pytest.raises(ValueError, match="explicit"):
        prepare_rag_input(SLMRequest(mode="solution"), rag, source_question="SCCS")
