"""Offline behavior/safety tests; no GPU, FAISS, model downloads, or network."""

from pathlib import Path
import subprocess
import sys

import pytest

from beauty_agent.contracts import ObservationSlot
from beauty_agent.v3_contracts import ReferenceChunk, SLMRequest, RetrievalResult
from beauty_agent.rag.corpus import CorpusEntry, load_corpus_entries
from beauty_agent.rag.backends import HashFallback, NoOpReranker, normalize
from beauty_agent.rag.query_builder import build_query
from beauty_agent.rag.retriever import TwoStageReferenceRetriever


def entry(n, text):
    return CorpusEntry(
        "cleansing",
        text,
        "fixture.md",
        ReferenceChunk(
            evidence_ref=f"ref:cleansing-{n:03d}",
            text=text,
            source_url="https://example.com",
            locator="test fixture",
            checked_on="2026-11-25",
            limitations="synthetic software fixture",
        ),
    )


class FixedEmbedding:
    signature = "test-fixed-v1"

    def __init__(self):
        self.calls = []

    def encode(self, texts, *, is_query=False):
        self.calls.append((list(texts), is_query))
        return (
            [[1.0, 0.0] for _ in texts]
            if is_query
            else [[1.0, 0.0], [0.8, 0.6], [0.0, 1.0]][: len(texts)]
        )


class FixedRanking:
    signature = "test-rank-v1"

    def __init__(self):
        self.calls = []

    def score(self, query, documents, prior_scores):
        self.calls.append(list(documents))
        return [
            {"first\nfirst": 0.2, "second\nsecond": 0.9, "third\nthird": 0.1}[d]
            for d in documents
        ]


def sample_rag(**kwargs):
    return TwoStageReferenceRetriever(
        [entry(1, "first"), entry(2, "second"), entry(3, "third")],
        FixedEmbedding(),
        FixedRanking(),
        **kwargs,
    )


def test_stage_two_reorders_and_rejects_without_filling_top_k():
    rag = sample_rag(threshold=0.8)
    result = rag.retrieve("question")
    assert isinstance(result, RetrievalResult)
    assert [c.evidence_ref for c in result.chunks] == ["ref:cleansing-002"]
    assert rag.embedder.calls[0][0] == [
        "first\nfirst",
        "second\nsecond",
        "third\nthird",
    ]
    assert rag.reranker.calls[0] == ["first\nfirst", "second\nsecond", "third\nthird"]
    rag.threshold = 0.99
    assert rag.retrieve("question").chunks == []


@pytest.mark.parametrize("mode", ["hold", "nlu"])
def test_non_solution_does_not_call_any_retrieval_backend(mode):
    rag = sample_rag()
    before = len(rag.embedder.calls)
    assert rag.retrieve_for_request(SLMRequest(mode=mode)).chunks == []
    assert len(rag.embedder.calls) == before and rag.reranker.calls == []


def test_empty_and_invalid_top_k_do_not_query_models():
    rag = sample_rag()
    before = len(rag.embedder.calls)
    assert rag.retrieve("   ").chunks == []
    for k in [0, 6, -1]:
        with pytest.raises(ValueError):
            rag.retrieve("x", top_k=k)
    assert len(rag.embedder.calls) == before


def test_solution_request_builds_query_without_mutating_the_request():
    rag = sample_rag(threshold=0.8)
    request = SLMRequest(
        mode="solution",
        confirmed_observations={
            "method.body_site": ObservationSlot(
                variable_id="method.body_site",
                state="known",
                value="face",
                confirmed_by_user=True,
            ),
            "skin.dryness": ObservationSlot(
                variable_id="skin.dryness", state="unknown"
            ),
        },
        product_evidence=[{"status": "verified", "label_guidance": "rinse off"}],
    )
    original = request.model_dump()
    result = rag.retrieve_for_request(request, top_k=3)
    query_texts, is_query = rag.embedder.calls[-1]
    assert is_query and len(query_texts) == 1
    assert all(
        text in query_texts[0]
        for text in ["사용 부위", "face", "피부 건조: 미확인", "rinse off"]
    )
    assert result.chunks[0].evidence_ref == "ref:cleansing-002"
    assert request.model_dump() == original


def test_bad_scores_and_dimensions_fail_closed():
    rag = sample_rag()
    rag.reranker.score = lambda *args: [float("nan")] * 3
    with pytest.raises(ValueError, match="invalid scores"):
        rag.retrieve("x")
    with pytest.raises(ValueError):
        normalize([float("inf")])
    with pytest.raises(ValueError):
        rag.index.search([1, 2, 3], 3)
    with pytest.raises(ValueError):
        sample_rag(threshold=float("nan"))


def test_retrieved_chunks_are_not_mutable_corpus_aliases():
    rag = sample_rag(threshold=0.8)
    result = rag.retrieve("x")
    result.chunks[0].text = "changed by consumer"
    assert rag.retrieve("x").chunks[0].text == "second"


def test_query_preserves_denial_unknown_and_rejects_unverified_labels():
    obs = {
        "skin.pain": ObservationSlot(
            variable_id="skin.pain", state="known", value="none", confirmed_by_user=True
        ),
        "method.removal": ObservationSlot(
            variable_id="method.removal", state="unknown"
        ),
        "skin.dryness": ObservationSlot(
            variable_id="skin.dryness",
            state="known",
            value="severe",
            confirmed_by_user=False,
        ),
        "kb_judgments.guidance": ObservationSlot(
            variable_id="kb_judgments.guidance",
            state="known",
            value="answer shortcut",
            confirmed_by_user=True,
        ),
    }
    query = build_query(
        obs,
        [
            {
                "product_id": "secret-id",
                "version": "old",
                "status": "usage_held",
                "label_guidance": "unverified-old-label",
            },
            {"product_id": "id2", "status": "verified", "label_guidance": "rinse off"},
        ],
    )
    assert "none" in query and "미확인" in query and "rinse off" in query
    assert all(
        x not in query
        for x in ["severe", "answer shortcut", "secret-id", "unverified-old-label"]
    )
    assert query == build_query(
        dict(reversed(list(obs.items()))),
        [
            {"status": "usage_held"},
            {"status": "verified", "label_guidance": "rinse off"},
        ],
    )


def test_fallback_save_load_checks_corpus_and_vectors(tmp_path):
    entries = [entry(1, "부드러운 세안"), entry(2, "화장품 기한")]
    rag = TwoStageReferenceRetriever(
        entries, HashFallback(), NoOpReranker(), threshold=0.01
    )
    rag.save(tmp_path)
    restored = TwoStageReferenceRetriever(
        entries, HashFallback(), NoOpReranker(), threshold=0.01, build=False
    )
    restored.load(tmp_path)
    assert restored.retrieve("세안") == rag.retrieve("세안")
    bad = TwoStageReferenceRetriever(
        entries, HashFallback(1024), NoOpReranker(), build=False
    )
    assert bad.index_version != rag.index_version
    with pytest.raises(ValueError, match="manifest"):
        bad.load(tmp_path)
    changed = [entry(1, "바뀐 본문"), entry(2, "화장품 기한")]
    bad = TwoStageReferenceRetriever(
        changed, HashFallback(), NoOpReranker(), build=False
    )
    with pytest.raises(ValueError, match="manifest"):
        bad.load(tmp_path)
    (tmp_path / "vectors.json").write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        restored.load(tmp_path)


def test_official_corpus_passes_through_unchanged():
    entries = load_corpus_entries(
        Path(__file__).resolve().parents[1] / "data/rag/corpus"
    )
    rag = TwoStageReferenceRetriever(
        entries, HashFallback(), NoOpReranker(), threshold=0.01
    )
    result = rag.retrieve("선크림 SPF PA 뜻")
    originals = {e.chunk.evidence_ref: e.chunk for e in entries}
    assert result.chunks and all(c == originals[c.evidence_ref] for c in result.chunks)


def test_no_optional_ml_dependency_imported():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import beauty_agent.rag.retriever; import beauty_agent.rag.qwen; assert not any(x in sys.modules for x in ['torch','numpy','faiss','transformers'])",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_kb_and_duplicate_refs_rejected():
    one = entry(1, "x")
    with pytest.raises(ValueError):
        TwoStageReferenceRetriever([one, one], HashFallback(), NoOpReranker())
    bad = entry(1, "x")
    bad.chunk.evidence_ref = "ref:U99"
    with pytest.raises(ValueError):
        TwoStageReferenceRetriever([bad], HashFallback(), NoOpReranker())


def test_query_builder_supports_kb_and_runtime_prefixes_and_blocks_forbidden():
    obs = {
        "moisturizing.timing": ObservationSlot(
            variable_id="moisturizing.timing",
            state="known",
            value="after_shower",
            confirmed_by_user=True,
        ),
        "dose.reapply_interval": ObservationSlot(
            variable_id="dose.reapply_interval",
            state="known",
            value="2h",
            confirmed_by_user=True,
        ),
        "lifestyle.sweat": ObservationSlot(
            variable_id="lifestyle.sweat",
            state="known",
            value="high",
            confirmed_by_user=True,
        ),
        "routine.goal": ObservationSlot(
            variable_id="routine.goal",
            state="known",
            value="보습 순서 확인",
            confirmed_by_user=True,
        ),
        "context.review_goal": ObservationSlot(
            variable_id="context.review_goal",
            state="known",
            value="아침 물 온도",
            confirmed_by_user=True,
        ),
        "constraints.budget": ObservationSlot(
            variable_id="constraints.budget",
            state="known",
            value="기존 보유 제품만",
            confirmed_by_user=True,
        ),
        "eye.visual_symptom_now": ObservationSlot(
            variable_id="eye.visual_symptom_now",
            state="known",
            value="none",
            confirmed_by_user=True,
        ),
        "symptom.other_report": ObservationSlot(
            variable_id="symptom.other_report",
            state="known",
            value="sibling_stinging",
            confirmed_by_user=True,
        ),
        "kb_judgments.guidance": ObservationSlot(
            variable_id="kb_judgments.guidance",
            state="known",
            value="forbidden_kb_judgment",
            confirmed_by_user=True,
        ),
        "kb.card_id": ObservationSlot(
            variable_id="kb.card_id",
            state="known",
            value="forbidden_kb_card",
            confirmed_by_user=True,
        ),
        "product.internal_rank": ObservationSlot(
            variable_id="product.internal_rank",
            state="known",
            value="forbidden_product_rank",
            confirmed_by_user=True,
        ),
        "provenance.source": ObservationSlot(
            variable_id="provenance.source",
            state="known",
            value="forbidden_provenance",
            confirmed_by_user=True,
        ),
        "runtime_invariants.mode": ObservationSlot(
            variable_id="runtime_invariants.mode",
            state="known",
            value="forbidden_invariant",
            confirmed_by_user=True,
        ),
        "commerce.price_tier": ObservationSlot(
            variable_id="commerce.price_tier",
            state="known",
            value="forbidden_commerce",
            confirmed_by_user=True,
        ),
        "regulatory.claim_flag": ObservationSlot(
            variable_id="regulatory.claim_flag",
            state="known",
            value="forbidden_regulatory",
            confirmed_by_user=True,
        ),
    }
    query = build_query(obs, [])
    for expected in (
        "after_shower",
        "2h",
        "high",
        "루틴 목표",
        "보습 순서 확인",
        "확인하려는 내용",
        "아침 물 온도",
        "기존 보유 제품만",
        "eye.visual_symptom_now",
        "sibling_stinging",
    ):
        assert expected in query
    for forbidden in (
        "forbidden_kb_judgment",
        "forbidden_kb_card",
        "forbidden_product_rank",
        "forbidden_provenance",
        "forbidden_invariant",
        "forbidden_commerce",
        "forbidden_regulatory",
    ):
        assert forbidden not in query

