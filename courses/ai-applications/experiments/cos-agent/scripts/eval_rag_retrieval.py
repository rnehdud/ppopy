"""Evaluate frozen synthetic qrels; tune on calibration only, never held-out labels."""
# ruff: noqa: E402 -- Standalone CLI bootstraps the project import path.

from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import sys
from time import perf_counter

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from build_rag_index import checked_entries, make_backends
from beauty_agent.contracts import ObservationSlot
from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.retriever import (
    TwoStageReferenceRetriever,
    RetrievalTrace,
    ScoredReference,
    corpus_digest,
)
from beauty_agent.rag.query_builder import build_query
from beauty_agent.rag.evaluation import metrics, tune_threshold, THRESHOLDS, percentile


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_queries(path, refs):
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r\n" in raw:
        raise ValueError("query set must be UTF-8 without BOM and use LF")
    rows = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("duplicate query ID")
    if len({r["query"] for r in rows}) != len(rows):
        raise ValueError("duplicate query text")
    for row in rows:
        if row["split"] not in {"calibration", "evaluation"}:
            raise ValueError("invalid split")
        if not set(row["relevant_refs"]) <= refs:
            raise ValueError("qrel missing from corpus")
    return rows, hashlib.sha256(raw).hexdigest()


def benchmark_builder():
    obs = {
        "method.current_routine": ObservationSlot(
            variable_id="method.current_routine",
            state="known",
            value={"actual_site": "face", "rinse": True},
            confirmed_by_user=True,
        ),
        "constraints.goals": ObservationSlot(
            variable_id="constraints.goals",
            state="known",
            value=["세정 방법 확인"],
            confirmed_by_user=True,
        ),
        "skin.pain": ObservationSlot(
            variable_id="skin.pain", state="known", value="none", confirmed_by_user=True
        ),
    }
    product = [{"status": "verified", "label_guidance": "세정 후 물로 헹구기"}]
    times = []
    for _ in range(1000):
        start = perf_counter()
        build_query(obs, product)
        times.append((perf_counter() - start) * 1000)
    return {
        "iterations": 1000,
        "p50_ms": percentile(times, 0.5),
        "p95_ms": percentile(times, 0.95),
        "max_ms": max(times),
        "llm_calls": 0,
    }


def summarize(rows, traces):
    threshold, sweep = tune_threshold(rows, traces)
    selected = {
        split: metrics([r for r in rows if r["split"] == split], traces, threshold)
        for split in ["calibration", "evaluation"]
    }
    # Held-out sweep is diagnostic only; the selected threshold is already frozen.
    diagnostics = [
        {
            "threshold": t,
            **metrics([r for r in rows if r["split"] == "evaluation"], traces, t),
        }
        for t in THRESHOLDS
    ]
    return {
        "selected_threshold": threshold,
        "selection_rule": "calibration only; preserve >=90% positive hit rate if feasible, maximize MRR - 0.5*negative acceptance - 0.1*unjudged fraction",
        "calibration_sweep": sweep,
        "selected_metrics": selected,
        "held_out_diagnostic_sweep_not_used_for_tuning": diagnostics,
    }


def run_backend(name, rag, rows, output):
    for row in [r for r in rows if r["split"] == "calibration"][:2]:
        rag.score_candidates(row["query"])
    traces = {}
    for i, row in enumerate(rows, 1):
        traces[row["id"]] = rag.score_candidates(row["query"])
        print(f"{name} {i}/{len(rows)} {row['id']}", flush=True)
    write(
        output / (name + "_scores.json"),
        {rid: asdict(trace) for rid, trace in traces.items()},
    )
    return traces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend", choices=["hash", "bm25", "qwen", "all"], default="hash"
    )
    parser.add_argument(
        "--queries", type=Path, default=COS / "data/rag/evaluation/queries.jsonl"
    )
    parser.add_argument(
        "--output", type=Path, default=COS / "outputs/rag_pipeline/evaluation"
    )
    parser.add_argument("--index-dir", type=Path, default=COS / "data/rag/index")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--local-files-only", action="store_true")
    args = parser.parse_args()
    entries = checked_entries(COS / "data/rag/corpus", COS / "data/rag/chunks.jsonl")
    rows, qhash = load_queries(args.queries, {e.chunk.evidence_ref for e in entries})
    args.output.mkdir(parents=True, exist_ok=True)
    # Recorded BEFORE model scores are inspected. Qrels are author judgments,
    # not expert approval; no thresholds/queries are rewritten to meet targets.
    frozen = {
        "query_sha256": qhash,
        "corpus_sha256": corpus_digest(entries),
        "query_ids": {
            split: [r["id"] for r in rows if r["split"] == split]
            for split in ["calibration", "evaluation"]
        },
        "thresholds": THRESHOLDS,
        "qrel_status": "author_assigned_pending_team_review",
    }
    write(args.output / "frozen_protocol.json", frozen)
    report = {
        "development_preview": True,
        "production_enabled": False,
        **frozen,
        "corpus_count": len(entries),
        "domain_counts": dict(Counter(r["domain"] for r in rows)),
        "query_builder": benchmark_builder(),
        "host": {"platform": platform.platform(), "python": platform.python_version()},
        "backends": {},
        "metric_limitations": "Positive qrels are not exhaustive relevance labels. Unjudged returned docs are not necessarily irrelevant. Negative-query acceptance is the explicit out-of-scope inflow metric. These synthetic, author-labeled queries do not establish clinical or production quality.",
    }
    if args.backend in {"hash", "all"}:
        hash_rag = TwoStageReferenceRetriever(entries, HashFallback(), NoOpReranker())
        hash_rag.save(args.index_dir / "hash")
        traces = run_backend("hash", hash_rag, rows, args.output)
        report["backends"]["hash"] = {
            "embedder": hash_rag.embedder.signature,
            "reranker": hash_rag.reranker.signature,
            "score_semantics": "lexical cosine, not learned relevance probability",
            **summarize(rows, traces),
        }
    if args.backend in {"bm25", "all"}:
        from beauty_agent.rag.bm25 import BM25Baseline

        baseline = BM25Baseline(entries)
        traces = run_backend("bm25", baseline, rows, args.output)
        report["backends"]["bm25"] = {
            "signature": baseline.signature,
            "package_version": importlib.metadata.version("rank-bm25"),
            "score_semantics": "max(0,BM25)/(1+max(0,BM25)); not calibrated probability",
            "timing_note": "dense_ms trace field denotes lexical Stage 1 time for this baseline",
            **summarize(rows, traces),
        }
    if args.backend in {"qwen", "all"}:
        import torch

        if args.device.startswith("cuda") and torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        start = perf_counter()
        embed, rank = make_backends(
            "qwen",
            args.device,
            args.dtype,
            args.batch_size,
            args.max_length,
            local_files_only=args.local_files_only,
        )
        rag = TwoStageReferenceRetriever(
            entries, embed, rank, use_faiss=True, build=False
        )
        location = args.index_dir / "qwen"
        if (location / "manifest.json").exists():
            rag.load(location)
        else:
            rag._build()
            rag.save(location)
        startup = perf_counter() - start
        startup_allocated = startup_reserved = 0
        if args.device.startswith("cuda"):
            torch.cuda.synchronize()
            startup_allocated = torch.cuda.max_memory_allocated()
            startup_reserved = torch.cuda.max_memory_reserved()
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        traces = run_backend("qwen_full", rag, rows, args.output)
        gpu = {
            "device": str(args.device),
            "cuda_available": torch.cuda.is_available(),
            "cuda_build": torch.version.cuda,
            "torch": torch.__version__,
        }
        if args.device.startswith("cuda"):
            gpu.update(
                {
                    "name": torch.cuda.get_device_name(),
                    "startup_max_allocated_bytes": startup_allocated,
                    "startup_max_reserved_bytes": startup_reserved,
                    "online_max_allocated_bytes": torch.cuda.max_memory_allocated(),
                    "online_max_reserved_bytes": torch.cuda.max_memory_reserved(),
                    "max_allocated_bytes": max(startup_allocated, torch.cuda.max_memory_allocated()),
                    "max_reserved_bytes": max(startup_reserved, torch.cuda.max_memory_reserved()),
                    "total_device_bytes": torch.cuda.get_device_properties(
                        0
                    ).total_memory,
                }
            )
        versions = {
            p: importlib.metadata.version(p)
            for p in ["transformers", "faiss-cpu", "numpy", "huggingface-hub"]
        }
        report["backends"]["qwen_full"] = {
            "embedder": embed.signature,
            "reranker": rank.signature,
            "device": gpu,
            "versions": versions,
            "startup_and_index_seconds": startup,
            "score_semantics": "yes/no softmax; not a calibrated safety probability",
            "embedding_truncated_inputs": embed.truncated_inputs,
            "reranker_truncated_inputs": rank.truncated_inputs,
            **summarize(rows, traces),
        }
        dense = {
            rid: RetrievalTrace(
                tuple(
                    ScoredReference(c.evidence_ref, c.dense_score, c.dense_score)
                    for c in t.candidates
                ),
                0,
                t.dense_ms,
                0,
                t.dense_ms,
            )
            for rid, t in traces.items()
        }
        report["backends"]["qwen_dense"] = {
            "score_semantics": "embedding cosine",
            "timing_note": "shared Stage 1 trace component, not a separately loaded model experiment",
            **summarize(rows, dense),
        }
    write(args.output / "report.json", report)
    summary = {
        name: {
            "threshold": b["selected_threshold"],
            "evaluation": b["selected_metrics"]["evaluation"],
        }
        for name, b in report["backends"].items()
    }
    print(
        json.dumps(
            {"report": str(args.output / "report.json"), "results": summary},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
