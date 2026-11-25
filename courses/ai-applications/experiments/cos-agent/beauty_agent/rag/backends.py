"""Dependency-free interfaces and deterministic lexical test backends."""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from typing import Protocol, Sequence

Vector = list[float]


class Embedder(Protocol):
    signature: str

    def encode(
        self, texts: Sequence[str], *, is_query: bool = False
    ) -> list[Vector]: ...


class Reranker(Protocol):
    signature: str

    def score(
        self, query: str, documents: Sequence[str], prior_scores: Sequence[float]
    ) -> list[float]: ...


def normalize(vector: Sequence[float]) -> Vector:
    values = [float(x) for x in vector]
    if not values or not all(math.isfinite(x) for x in values):
        raise ValueError("embedding must be nonempty and finite")
    length = math.sqrt(sum(x * x for x in values))
    return [x / length for x in values] if length else values


class HashFallback:
    """CPU lexical feature hash, not a semantic/multilingual learned model.

    Korean titles make English paragraphs lexically discoverable, but this does
    not demonstrate cross-lingual semantic understanding. Never silently used
    when a requested Qwen backend fails to load.
    """

    def __init__(self, dimensions: int = 512):
        if dimensions < 16:
            raise ValueError("hash dimensions must be >=16")
        self.dimensions = dimensions
        self.signature = f"hash-lexical-v1:{dimensions}"

    def encode(self, texts: Sequence[str], *, is_query: bool = False) -> list[Vector]:
        result = []
        for text in texts:
            text = unicodedata.normalize("NFKC", text).casefold()
            words = re.findall(r"[\w]+", text, re.UNICODE)
            features = ["w:" + word for word in words]
            for word in words:
                features.extend("c:" + word[i : i + 2] for i in range(len(word) - 1))
            vector = [0.0] * self.dimensions
            for feature in features:
                digest = hashlib.blake2b(feature.encode(), digest_size=8).digest()
                bucket = int.from_bytes(digest[:4], "little") % self.dimensions
                vector[bucket] += 1.0 if digest[4] & 1 else -1.0
            result.append(normalize(vector))
        return result


class NoOpReranker:
    signature = "noop-cosine-v1"

    def score(
        self, query: str, documents: Sequence[str], prior_scores: Sequence[float]
    ) -> list[float]:
        if len(documents) != len(prior_scores):
            raise ValueError("document/score count mismatch")
        return list(prior_scores)
