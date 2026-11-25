"""Cosine indices. FAISS/NumPy are optional and imported only on the dense path."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .backends import normalize


class PythonCosineIndex:
    backend = "stub"

    def __init__(self, vectors: Sequence[Sequence[float]]):
        if not vectors:
            raise ValueError("cannot index an empty corpus")
        self.vectors = [normalize(v) for v in vectors]
        self.dimensions = len(self.vectors[0])
        if any(len(v) != self.dimensions for v in self.vectors):
            raise ValueError("inconsistent embedding dimensions")

    def search(self, vector: Sequence[float], k: int) -> list[tuple[int, float]]:
        query = normalize(vector)
        if len(query) != self.dimensions:
            raise ValueError("query dimension mismatch")
        scored = [
            (i, max(-1.0, min(1.0, sum(x * y for x, y in zip(query, doc)))))
            for i, doc in enumerate(self.vectors)
        ]
        return sorted(scored, key=lambda item: (-item[1], item[0]))[:k]


class FaissCosineIndex:
    backend = "faiss"

    def __init__(self, vectors: Sequence[Sequence[float]]):
        import faiss
        import numpy as np

        checked = PythonCosineIndex(vectors)
        self.dimensions = checked.dimensions
        self._index = faiss.IndexFlatIP(self.dimensions)
        self._index.add(np.asarray(checked.vectors, dtype="float32"))

    def search(self, vector: Sequence[float], k: int) -> list[tuple[int, float]]:
        import faiss
        import numpy as np

        # Keep per-query validation/normalization in vectorized native code.
        # Own the buffer: normalize_L2 must not mutate a caller's ndarray.
        query = np.array(vector, dtype="float32", copy=True)
        if query.ndim != 1 or query.size != self.dimensions:
            raise ValueError("query dimension mismatch")
        if not np.isfinite(query).all():
            raise ValueError("query embedding must be finite")
        query = query.reshape(1, -1)
        faiss.normalize_L2(query)
        scores, ids = self._index.search(query, min(k, self._index.ntotal))
        return sorted(
            [
                (int(i), max(-1.0, min(1.0, float(s))))
                for i, s in zip(ids[0], scores[0])
                if i >= 0
            ],
            key=lambda item: (-item[1], item[0]),
        )

    def save(self, path: Path) -> None:
        import faiss

        faiss.write_index(self._index, str(path))

    @classmethod
    def load(cls, path: Path, *, dimensions: int, count: int):
        import faiss

        obj = cls.__new__(cls)
        obj._index = faiss.read_index(str(path))
        obj.dimensions = dimensions
        if (
            not isinstance(obj._index, faiss.IndexFlatIP)
            or obj._index.d != dimensions
            or obj._index.ntotal != count
        ):
            raise ValueError("persisted FAISS shape/type mismatch")
        return obj
