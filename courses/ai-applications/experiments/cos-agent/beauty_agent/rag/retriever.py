"""Two-stage local ReferenceRetriever with explicit solution-only entry point."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Sequence
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from beauty_agent.v3_contracts import RetrievalResult, SLMRequest

from .backends import Embedder, Reranker
from .corpus import CorpusEntry
from .index import FaissCosineIndex, PythonCosineIndex
from .query_builder import build_query
from .selection import Layer2Selection


@dataclass(frozen=True)
class ScoredReference:
    evidence_ref: str
    dense_score: float
    rerank_score: float


@dataclass(frozen=True)
class RetrievalTrace:
    candidates: tuple[ScoredReference, ...]
    query_ms: float
    dense_ms: float
    rerank_ms: float
    total_ms: float


def corpus_digest(entries: Sequence[CorpusEntry]) -> str:
    text = json.dumps(
        [
            {
                "title": e.title,
                "domain": e.domain,
                "chunk": e.chunk.model_dump(mode="json", exclude_none=True),
            }
            for e in entries
        ],
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(text.encode()).hexdigest()


class TwoStageReferenceRetriever:
    def __init__(
        self,
        entries: Sequence[CorpusEntry],
        embedder: Embedder,
        reranker: Reranker,
        *,
        threshold: float = 0.5,
        stage1_k: int = 15,
        use_faiss: bool = False,
        build: bool = True,
        layer2_selections: Sequence[Layer2Selection] = (),
    ):
        if not entries or len({e.chunk.evidence_ref for e in entries}) != len(entries):
            raise ValueError("corpus must be nonempty with unique refs")
        if any(
            not re.fullmatch(
                r"ref:(?:(?:cleansing|moisturizing|sun_protection|storage_label)-\d{3}|(?:regulatory|safety_method)-L2U-\d{4})",
                e.chunk.evidence_ref,
            )
            for e in entries
        ):
            raise ValueError("non-corpus/KB evidence ref rejected")
        if not math.isfinite(threshold) or not -1 <= threshold <= 1:
            raise ValueError("threshold must be finite and in [-1, 1]")
        if stage1_k < 5:
            raise ValueError("stage1_k must be >=5")
        # Revalidate mutable Pydantic inputs; model_copy can bypass validation.
        self.entries = tuple(
            CorpusEntry(
                e.domain,
                e.title,
                e.source_file,
                type(e.chunk).model_validate(e.chunk.model_dump()),
            )
            for e in entries
        )
        if any(
            e.chunk.layer2 and e.chunk.layer2.topic != e.domain for e in self.entries
        ):
            raise ValueError("layer2 topic mismatch")
        self.embedder = embedder
        self.reranker = reranker
        self.threshold = threshold
        self.stage1_k = stage1_k
        self.use_faiss = use_faiss
        # Different embedding revisions/configurations must not share the same
        # audit/cache identifier merely because their source paragraphs match.
        self._index_identity = corpus_digest(self.entries) + "|" + embedder.signature
        self._source_only = False
        self._set_source_scope(layer2_selections)
        self._by_ref = {e.chunk.evidence_ref: e for e in self.entries}
        self.index = None
        if build:
            self._build()

    def _set_source_scope(self, selections: Sequence[Layer2Selection]) -> None:
        self.layer2_selections = tuple(
            Layer2Selection.model_validate(selection.model_dump()) for selection in selections
        )
        identity = self._index_identity
        if self.layer2_selections:
            identity += "|" + json.dumps(
                [selection.model_dump() for selection in self.layer2_selections], sort_keys=True
            )
        self.index_version = "rag-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]

    def for_sources(self, selections: Sequence[Layer2Selection]) -> TwoStageReferenceRetriever:
        """Search only the selected sources using the existing index and models."""
        if self.index is None:
            raise RuntimeError("build or load the index before selecting a source scope")
        if not selections:
            raise ValueError("at least one explicit source selection is required")
        scoped = copy(self)
        scoped._source_only = True
        scoped._set_source_scope(selections)
        scoped.index_version += "-source-only"
        return scoped

    def _eligible(self, entry: CorpusEntry) -> bool:
        if entry.chunk.layer2 is None:
            return not self._source_only
        return any(s.matches(entry.chunk) for s in self.layer2_selections)

    def _build(self):
        vectors = self.embedder.encode([e.embedding_text for e in self.entries])
        if len(vectors) != len(self.entries):
            raise ValueError("embedding backend returned wrong row count")
        cls = FaissCosineIndex if self.use_faiss else PythonCosineIndex
        self.index = cls(vectors)

    def score_candidates(self, query: str) -> RetrievalTrace:
        start = perf_counter()
        if not query.strip():
            return RetrievalTrace((), 0, 0, 0, (perf_counter() - start) * 1000)
        if self.index is None:
            raise RuntimeError("index not loaded")
        encoded = self.embedder.encode([query], is_query=True)
        if len(encoded) != 1:
            raise ValueError("query encoder returned wrong row count")
        if not any(encoded[0]):
            return RetrievalTrace(
                (),
                0,
                (perf_counter() - start) * 1000,
                0,
                (perf_counter() - start) * 1000,
            )
        # Filter before truncating to stage1_k: an out-of-scope dense hit must
        # not crowd out eligible evidence or reach the reranker.
        search_k = (
            len(self.entries)
            if any(e.chunk.layer2 for e in self.entries)
            else self.stage1_k
        )
        candidates = [
            (i, score)
            for i, score in self.index.search(encoded[0], search_k)
            if self._eligible(self.entries[i])
        ][: self.stage1_k]
        if not candidates:
            return RetrievalTrace(
                (),
                0,
                (perf_counter() - start) * 1000,
                0,
                (perf_counter() - start) * 1000,
            )
        dense_end = perf_counter()
        docs = [self.entries[i].embedding_text for i, _ in candidates]
        scores = self.reranker.score(query, docs, [s for _, s in candidates])
        if len(scores) != len(candidates) or any(not math.isfinite(s) for s in scores):
            raise ValueError("reranker returned invalid scores")
        end = perf_counter()
        scored = tuple(
            ScoredReference(self.entries[i].chunk.evidence_ref, s, float(r))
            for (i, s), r in zip(candidates, scores)
        )
        return RetrievalTrace(
            scored,
            0,
            (dense_end - start) * 1000,
            (end - dense_end) * 1000,
            (end - start) * 1000,
        )

    def select(
        self, trace: RetrievalTrace, *, top_k: int = 5, threshold: float | None = None
    ) -> RetrievalResult:
        if not 1 <= top_k <= 5:
            raise ValueError("top_k must be between 1 and 5")
        cutoff = self.threshold if threshold is None else threshold
        if not math.isfinite(cutoff) or not -1 <= cutoff <= 1:
            raise ValueError("invalid threshold")
        ordered = sorted(
            trace.candidates,
            key=lambda c: (-c.rerank_score, -c.dense_score, c.evidence_ref),
        )
        chunks = [
            self._by_ref[c.evidence_ref].chunk.model_copy(deep=True)
            for c in ordered
            if c.rerank_score >= cutoff and self._eligible(self._by_ref[c.evidence_ref])
        ][:top_k]
        return RetrievalResult(
            chunks=chunks,
            index_version=self.index_version,
            retriever_backend="faiss" if self.use_faiss else "stub",
        )

    def retrieve(self, query: str, *, top_k: int = 5) -> RetrievalResult:
        if not 1 <= top_k <= 5:
            raise ValueError("top_k must be between 1 and 5")
        return self.select(self.score_candidates(query), top_k=top_k)

    def retrieve_for_request(
        self, request: SLMRequest, *, top_k: int = 5
    ) -> RetrievalResult:
        # Must return BEFORE query building, embedding or reranking for HOLD/NLU.
        if request.mode != "solution":
            return RetrievalResult(
                chunks=[],
                index_version=self.index_version,
                retriever_backend="faiss" if self.use_faiss else "stub",
            )
        return self.retrieve(
            build_query(request.confirmed_observations, request.product_evidence),
            top_k=top_k,
        )

    def _manifest(self):
        return {
            "format_version": 1,
            "corpus_sha256": corpus_digest(self.entries),
            "refs": [e.chunk.evidence_ref for e in self.entries],
            "embedder": self.embedder.signature,
            "dimensions": self.index.dimensions,
            "count": len(self.entries),
            "backend": "faiss" if self.use_faiss else "stub",
        }

    def save(self, directory: Path) -> None:
        if self.index is None:
            raise RuntimeError("no index to save")
        directory.mkdir(parents=True, exist_ok=True)
        if self.use_faiss:
            self.index.save(directory / "vectors.faiss")
            filename = "vectors.faiss"
        else:
            (directory / "vectors.json").write_text(
                json.dumps(self.index.vectors) + "\n", encoding="utf-8", newline="\n"
            )
            filename = "vectors.json"
        manifest = self._manifest()
        manifest["vector_file_sha256"] = hashlib.sha256(
            (directory / filename).read_bytes()
        ).hexdigest()
        (directory / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def load(self, directory: Path) -> None:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        expected = {
            "format_version": 1,
            "corpus_sha256": corpus_digest(self.entries),
            "refs": [e.chunk.evidence_ref for e in self.entries],
            "embedder": self.embedder.signature,
            "count": len(self.entries),
            "backend": "faiss" if self.use_faiss else "stub",
        }
        if any(manifest.get(k) != v for k, v in expected.items()):
            raise ValueError(
                "index manifest does not match corpus/backend/embedding configuration"
            )
        filename = "vectors.faiss" if self.use_faiss else "vectors.json"
        if hashlib.sha256(
            (directory / filename).read_bytes()
        ).hexdigest() != manifest.get("vector_file_sha256"):
            raise ValueError("persisted vector checksum mismatch")
        if self.use_faiss:
            self.index = FaissCosineIndex.load(
                directory / "vectors.faiss",
                dimensions=manifest["dimensions"],
                count=manifest["count"],
            )
        else:
            self.index = PythonCosineIndex(
                json.loads((directory / "vectors.json").read_text(encoding="utf-8"))
            )
            if (
                len(self.index.vectors) != manifest["count"]
                or self.index.dimensions != manifest["dimensions"]
            ):
                raise ValueError("persisted vector shape mismatch")
