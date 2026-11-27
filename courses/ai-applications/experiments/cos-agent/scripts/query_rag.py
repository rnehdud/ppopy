"""Retrieve source explanations with an explicit L2 unit as the version selector.

No generation, evaluation, or service deployment. Hash mode is a plumbing check.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from beauty_agent.rag.retriever import TwoStageReferenceRetriever
from beauty_agent.rag.selection import Layer2Selection
from scripts.build_rag_index import checked_entries, make_backends


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query")
    p.add_argument("--corpus", type=Path, default=COS / "data/rag/corpus")
    p.add_argument("--additional-corpus", type=Path, action="append", default=[])
    p.add_argument("--chunks", type=Path, default=COS / "data/rag/chunks.jsonl")
    p.add_argument("--index", type=Path, required=True)
    p.add_argument(
        "--source-unit",
        action="append",
        default=[],
        help="L2U ID selecting its exact source, jurisdiction, version and as_of; repeatable",
    )
    p.add_argument("--backend", choices=["hash", "qwen"], default="hash")
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", default="float16")
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--max-length", type=int, default=1024)
    p.add_argument("--local-files-only", action="store_true")
    p.add_argument("--threshold", type=float, default=0.5)
    p.add_argument("--top-k", type=int, default=5)
    args = p.parse_args()
    entries = checked_entries(args.corpus, args.chunks, args.additional_corpus)
    metadata = {
        e.chunk.layer2.unit_id: e.chunk.layer2 for e in entries if e.chunk.layer2
    }
    selections = []
    for unit in args.source_unit:
        if unit not in metadata:
            p.error(f"unknown source unit: {unit}")
        m = metadata[unit]
        selection = Layer2Selection(
            **{
                key: getattr(m, key)
                for key in ("source_id", "jurisdiction", "document_version", "as_of")
            },
            purpose="source_explanation_only",
        )
        if selection not in selections:
            selections.append(selection)
    embed, rank = make_backends(
        args.backend,
        args.device,
        args.dtype,
        args.batch_size,
        args.max_length,
        local_files_only=args.local_files_only,
    )
    rag = TwoStageReferenceRetriever.from_index(
        args.index,
        entries,
        embed,
        rank,
        threshold=args.threshold,
        layer2_selections=selections,
    )
    print(
        json.dumps(
            {
                "permitted_use": "source_explanation_only"
                if selections
                else "layer1_only",
                "selected_sources": [s.model_dump() for s in selections],
                "result": rag.retrieve(args.query, top_k=args.top_k).model_dump(
                    mode="json", exclude_none=True
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
