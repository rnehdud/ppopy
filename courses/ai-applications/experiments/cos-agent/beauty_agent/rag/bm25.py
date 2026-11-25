"""Optional lexical evaluation baseline, not a replacement for the Qwen path."""

from __future__ import annotations

import re
import unicodedata
from time import perf_counter

from .retriever import RetrievalTrace, ScoredReference


def tokenize(text: str) -> list[str]:
    """Same normalization on docs/queries; Korean bigrams need no morphology ML."""
    words = re.findall(r"[\w]+", unicodedata.normalize("NFKC", text).casefold())
    return ["w:" + word for word in words] + [
        "c:" + word[i : i + 2] for word in words for i in range(len(word) - 1)
    ]


class BM25Baseline:
    def __init__(self, entries):
        from rank_bm25 import BM25Okapi

        self.entries = tuple(entries)
        self.index = BM25Okapi(
            [tokenize(e.embedding_text) for e in entries], k1=1.5, b=0.75
        )
        self.signature = "rank-bm25:0.2.2:okapi:k1=1.5:b=0.75:nfkc-word-charbigram-v1"

    def score_candidates(self, query: str) -> RetrievalTrace:
        start = perf_counter()
        scores = self.index.get_scores(tokenize(query))
        ordered = sorted(enumerate(scores), key=lambda pair: (-pair[1], pair[0]))[:15]
        # A fixed monotonic transformation makes a finite [0,1) threshold grid
        # usable. It does NOT calibrate BM25 scores into relevance probabilities.
        candidates = tuple(
            ScoredReference(
                self.entries[i].chunk.evidence_ref,
                float(score),
                max(0.0, float(score)) / (1 + max(0.0, float(score))),
            )
            for i, score in ordered
        )
        elapsed = (perf_counter() - start) * 1000
        return RetrievalTrace(candidates, 0, elapsed, 0, elapsed)
