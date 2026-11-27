"""Build/reuse a local index; index binaries remain outside Git."""


from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.corpus import load_chunks_jsonl, load_corpus_entries
from beauty_agent.rag.retriever import TwoStageReferenceRetriever


def checked_entries(corpus: Path, chunks: Path, additional_corpus_dirs=()):
    entries = load_corpus_entries(corpus, additional_corpus_dirs=additional_corpus_dirs)
    pool = load_chunks_jsonl(chunks)
    if [e.chunk for e in entries] != pool:
        raise ValueError(
            "Markdown/official chunks.jsonl mismatch; re-export/review before indexing"
        )
    return entries


def make_backends(
    backend,
    device,
    dtype,
    batch_size,
    max_length,
    *,
    with_reranker=True,
    local_files_only=False,
):
    if backend == "hash":
        return HashFallback(), NoOpReranker()
    from beauty_agent.rag.qwen import QwenEmbedder, QwenReranker

    kwargs = {
        "device": device,
        "dtype": dtype,
        "batch_size": batch_size,
        "max_length": max_length,
        "local_files_only": local_files_only,
    }
    embed = QwenEmbedder(**kwargs)
    rank = QwenReranker(**kwargs) if with_reranker else NoOpReranker()
    return embed, rank


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--backend", choices=["hash", "qwen"], default="hash")
    p.add_argument("--corpus", type=Path, default=COS / "data/rag/corpus")
    p.add_argument("--chunks", type=Path, default=COS / "data/rag/chunks.jsonl")
    p.add_argument("--output", type=Path, default=COS / "data/rag/index")
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", default="float16")
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--max-length", type=int, default=1024)
    p.add_argument("--local-files-only", action="store_true")
    p.add_argument("--additional-corpus", type=Path, action="append", default=[])
    args = p.parse_args()
    entries = checked_entries(args.corpus, args.chunks, args.additional_corpus)
    start = perf_counter()
    embed, rank = make_backends(
        args.backend,
        args.device,
        args.dtype,
        args.batch_size,
        args.max_length,
        with_reranker=False,
        local_files_only=args.local_files_only,
    )
    rag = TwoStageReferenceRetriever(
        entries, embed, rank, use_faiss=args.backend == "qwen"
    )
    rag.save(args.output)
    print(
        json.dumps(
            {
                "backend": args.backend,
                "count": len(entries),
                "domains": dict(Counter(e.domain for e in entries)),
                "index_version": rag.index_version,
                "output": str(args.output),
                "build_seconds": perf_counter() - start,
                "embedding_signature": embed.signature,
                "embedding_truncated_inputs": getattr(embed, "truncated_inputs", 0),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
