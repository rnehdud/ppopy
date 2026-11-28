"""Export retrieved model inputs alongside an unchanged SOLUTION/HOLD dataset."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import Field

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))

from beauty_agent.contracts import Contract
from beauty_agent.rag.handoff import prepare_rag_input
from beauty_agent.rag.retriever import TwoStageReferenceRetriever
from beauty_agent.rag.selection import Layer2Selection
from beauty_agent.slm import build_messages
from beauty_agent.slm._citations import extract_citations
from beauty_agent.v3_contracts import SLMRequest
from scripts.build_rag_index import checked_entries, make_backends


class SourceQuestion(Contract):
    question: str = Field(min_length=1, max_length=4000)
    source_unit: str = Field(pattern=r"^L2U-\d{4}$")


def export_rows(dataset, retriever, source_questions, *, top_k=5):
    """Join by dataset row ID and keep assistant targets in the original file."""
    metadata = {
        e.chunk.layer2.unit_id: e.chunk.layer2
        for e in retriever.entries
        if e.chunk.layer2 is not None
    }
    scopes = {}
    for row_id, spec in source_questions.items():
        if spec.source_unit not in metadata:
            raise ValueError(f"{row_id}: unknown Tier 2 source unit {spec.source_unit!r}")
        meta = metadata[spec.source_unit]
        scopes[row_id] = Layer2Selection(
            source_id=meta.source_id,
            jurisdiction=meta.jurisdiction,
            document_version=meta.document_version,
            as_of=meta.as_of,
            purpose="source_explanation_only",
        )

    seen = set()
    results = []
    for row in dataset:
        row_id = row["id"]
        if not isinstance(row_id, str) or not row_id.strip() or row_id in seen:
            raise ValueError(f"expected unique non-empty dataset ID, got {row_id!r}")
        seen.add(row_id)
        system, user, assistant = row["messages"]
        if [system["role"], user["role"], assistant["role"]] != ["system", "user", "assistant"]:
            raise ValueError(f"{row_id}: expected system/user/assistant messages")
        request = SLMRequest.model_validate_json(user["content"])
        if request.mode not in ("solution", "hold") or request.mode != row["mode"]:
            raise ValueError(f"{row_id}: expected matching SOLUTION/HOLD modes")
        scope = scopes.get(row_id)
        source_question = source_questions[row_id].question if scope is not None else None
        prepared = prepare_rag_input(
            request,
            retriever,
            source_question=source_question,
            source_scope=[scope] if scope is not None else (),
            top_k=top_k,
        )
        model_request = prepared.request
        allowed_refs = set(model_request.allowed_evidence_refs) if model_request is not None else set()
        missing = sorted(
            set(extract_citations(assistant["content"])) - allowed_refs
        )
        results.append({
            "id": row_id,
            "split": row["split"],
            "mode": request.mode,
            "source_question": source_question,
            "source_scope": scope.model_dump() if scope is not None else None,
            "retrieval": prepared.retrieval.model_dump(mode="json", exclude_none=True),
            "source_miss": prepared.source_miss,
            "model_messages": build_messages(model_request) if model_request is not None else None,
            "missing_target_refs": missing,
            "requires_target_review": bool(missing or scope is not None),
        })
    if not seen:
        raise ValueError("dataset has no rows")
    if scopes.keys() - seen:
        raise ValueError(f"source question IDs not found in dataset: {sorted(scopes.keys() - seen)}")
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--source-questions", type=Path, help="JSON object keyed by dataset row ID")
    p.add_argument("--corpus", type=Path, default=COS / "data/rag/corpus")
    p.add_argument(
        "--additional-corpus", type=Path, default=COS / "data/rag/layer2/corpus",
    )
    p.add_argument("--chunks", type=Path, required=True)
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--backend", choices=["hash", "qwen"], default="qwen")
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", default="float16")
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--max-length", type=int, default=1024)
    p.add_argument("--local-files-only", action="store_true")
    p.add_argument("--threshold", type=float, required=True)
    p.add_argument("--top-k", type=int, choices=range(1, 6), default=5)
    args = p.parse_args()

    source_questions = {}
    if args.source_questions is not None:
        source_questions = {
            row_id: SourceQuestion.model_validate(item)
            for row_id, item in json.loads(args.source_questions.read_text(encoding="utf-8")).items()
        }
    entries = checked_entries(args.corpus, args.chunks, [args.additional_corpus])
    embed, rank = make_backends(
        args.backend, args.device, args.dtype, args.batch_size, args.max_length,
        local_files_only=args.local_files_only,
    )
    rag = TwoStageReferenceRetriever.from_index(
        args.index, entries, embed, rank, threshold=args.threshold,
    )
    with args.input.open(encoding="utf-8") as source:
        rows = export_rows(
            (json.loads(line) for line in source if line.strip()), rag, source_questions,
            top_k=args.top_k,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as destination:
        for row in rows:
            destination.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({
        "rows": len(rows),
        "backend": args.backend,
        "index_backend": "faiss" if rag.use_faiss else "stub",
        "embedding_signature": embed.signature,
        "reranking_signature": rank.signature,
        "threshold": args.threshold,
        "top_k": args.top_k,
        "tier2_requests": sum(row["source_scope"] is not None for row in rows),
        "tier2_no_match": sum(row["source_miss"] for row in rows),
        "target_review_rows": sum(row["requires_target_review"] for row in rows),
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
