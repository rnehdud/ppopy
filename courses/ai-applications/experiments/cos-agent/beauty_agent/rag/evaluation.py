"""Transparent binary-qrel retrieval metrics and calibration-only tuning."""

from __future__ import annotations
import math
import statistics
from .retriever import RetrievalTrace

THRESHOLDS = (
    0.0,
    0.001,
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.15,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    0.95,
    0.99,
)


def percentile(values, q):
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def metrics(rows, traces: dict[str, RetrievalTrace], threshold: float):
    rr = []
    ndcg = []
    recall15 = []
    recall5 = []
    hits = []
    unjudged = returned = negative_count = negative_nonempty = 0
    dense_lat = []
    rerank_lat = []
    total_lat = []
    for row in rows:
        trace = traces[row["id"]]
        gold = set(row["relevant_refs"])
        dense = [s.evidence_ref for s in trace.candidates[:15]]
        ordered = sorted(
            trace.candidates,
            key=lambda c: (-c.rerank_score, -c.dense_score, c.evidence_ref),
        )
        retrieved = [c.evidence_ref for c in ordered if c.rerank_score >= threshold][:5]
        returned += len(retrieved)
        unjudged += sum(ref not in gold for ref in retrieved)
        dense_lat.append(trace.dense_ms)
        rerank_lat.append(trace.rerank_ms)
        total_lat.append(trace.total_ms)
        if gold:
            recall15.append(len(set(dense) & gold) / len(gold))
            recall5.append(len(set(retrieved) & gold) / len(gold))
            ranks = [i for i, ref in enumerate(retrieved, 1) if ref in gold]
            rr.append(1 / ranks[0] if ranks else 0.0)
            ideal = sum(1 / math.log2(i + 1) for i in range(1, min(5, len(gold)) + 1))
            ndcg.append(sum(1 / math.log2(i + 1) for i in ranks) / ideal)
            hits.append(bool(ranks))
        else:
            negative_count += 1
            negative_nonempty += bool(retrieved)

    def mean(values):
        return statistics.mean(values) if values else None

    return {
        "queries": len(rows),
        "positive_queries": len(rr),
        "negative_queries": negative_count,
        "recall_at_15": mean(recall15),
        "recall_at_5": mean(recall5),
        "mrr_at_5": mean(rr),
        "ndcg_at_5": mean(ndcg),
        "positive_hit_rate_at_5": mean(hits),
        "negative_query_nonempty_rate": negative_nonempty / negative_count
        if negative_count
        else None,
        "negative_query_rejection_rate": 1 - negative_nonempty / negative_count
        if negative_count
        else None,
        "unjudged_returned_document_fraction": unjudged / returned if returned else 0.0,
        "returned_documents": returned,
        "latency_ms": {
            "p50": percentile(total_lat, 0.5),
            "p95": percentile(total_lat, 0.95),
            "dense_p50": percentile(dense_lat, 0.5),
            "dense_p95": percentile(dense_lat, 0.95),
            "rerank_p50": percentile(rerank_lat, 0.5),
            "rerank_p95": percentile(rerank_lat, 0.95),
        },
    }


def tune_threshold(rows, traces, thresholds=THRESHOLDS):
    calibration = [r for r in rows if r["split"] == "calibration"]
    if (
        not calibration
        or not any(r["relevant_refs"] for r in calibration)
        or not any(not r["relevant_refs"] for r in calibration)
    ):
        raise ValueError(
            "threshold calibration requires positive and negative calibration queries"
        )
    sweep = [{"threshold": t, **metrics(calibration, traces, t)} for t in thresholds]

    def objective(m):
        feasible = m["positive_hit_rate_at_5"] >= 0.9
        utility = (
            m["mrr_at_5"]
            - 0.5 * m["negative_query_nonempty_rate"]
            - 0.1 * m["unjudged_returned_document_fraction"]
        )
        return feasible, utility, m["positive_hit_rate_at_5"], m["threshold"]

    selected = max(sweep, key=objective)
    return selected["threshold"], sweep
