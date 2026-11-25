"""CLI to export data/rag/corpus/*.md into standardized data/rag/chunks.jsonl."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

REPO_EXP_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_EXP_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_EXP_ROOT))

from beauty_agent.rag.corpus import (
    export_chunks_jsonl,
    load_chunks_jsonl,
    load_corpus_entries,
)

DEFAULT_CORPUS_DIR = REPO_EXP_ROOT / "data" / "rag" / "corpus"
DEFAULT_OUTPUT_PATH = REPO_EXP_ROOT / "data" / "rag" / "chunks.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse Reference RAG Markdown corpus and export chunks.jsonl."
    )
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=DEFAULT_CORPUS_DIR,
        help="Directory containing curated Markdown corpus files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output JSONL path for ReferenceChunk records.",
    )
    args = parser.parse_args()

    entries = load_corpus_entries(args.corpus_dir)
    written = export_chunks_jsonl(entries, args.output)
    reloaded = load_chunks_jsonl(args.output)
    if len(reloaded) != written or reloaded != [entry.chunk for entry in entries]:
        raise RuntimeError("Round-trip verification failed for exported chunks.jsonl")

    by_domain = dict(sorted(Counter(entry.domain for entry in entries).items()))
    sha256 = hashlib.sha256(args.output.read_bytes()).hexdigest()
    summary = {
        "total_chunks": written,
        "by_domain": by_domain,
        "output": str(args.output),
        "sha256": sha256,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
