"""Offline integration check for all L2 units, using deterministic embeddings.

--faiss exercises real FAISS persistence, not Qwen/model relevance quality.
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.corpus import (
    export_chunks_jsonl,
    load_chunks_jsonl,
    load_corpus_entries,
)
from beauty_agent.rag.retriever import TwoStageReferenceRetriever
from beauty_agent.rag.selection import Layer2Selection


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--faiss", action="store_true")
    args = p.parse_args()
    rows = load_corpus_entries(COS / "data/rag/layer2/corpus")
    selectors = {}
    for entry in rows:
        m = entry.chunk.layer2
        key = (m.source_id, m.jurisdiction, m.document_version, m.as_of)
        selectors[key] = Layer2Selection(
            source_id=key[0],
            jurisdiction=key[1],
            document_version=key[2],
            as_of=key[3],
            purpose="source_explanation_only",
        )
    selected = tuple(selectors.values())
    with tempfile.TemporaryDirectory() as d:
        path = Path(d)
        export_chunks_jsonl(rows, path / "chunks.jsonl")
        assert load_chunks_jsonl(path / "chunks.jsonl") == [r.chunk for r in rows]
        kwargs = {"use_faiss": args.faiss, "threshold": -1}
        r = TwoStageReferenceRetriever(rows, HashFallback(), NoOpReranker(), **kwargs)
        r.save(path / "index")
        restored = TwoStageReferenceRetriever(
            rows,
            HashFallback(),
            NoOpReranker(),
            build=False,
            layer2_selections=selected,
            **kwargs,
        )
        restored.load(path / "index")
        # Look up every actual corpus text in the saved/reloaded index. This
        # tests identity and metadata transport, not unseen-query relevance.
        for entry in rows:
            result = restored.retrieve(entry.embedding_text)
            assert entry.chunk in result.chunks, entry.chunk.evidence_ref
            assert all(
                c.layer2 and c.layer2.verification_status == "ready"
                for c in result.chunks
            )
        assert r.retrieve(rows[0].embedding_text).chunks == []
        print(
            json.dumps(
                {
                    "units_roundtripped": len(rows),
                    "self_lookup_passed": len(rows),
                    "unscoped_l2_results": 0,
                    "backend": "faiss" if args.faiss else "python",
                    "embedding": "HashFallback (software check only)",
                    "semantic_model_evaluation": "not_run",
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
