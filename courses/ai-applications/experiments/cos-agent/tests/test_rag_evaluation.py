import math
from copy import deepcopy
import pytest
from beauty_agent.rag.evaluation import metrics, tune_threshold
from beauty_agent.rag.retriever import RetrievalTrace, ScoredReference


def trace(*scores):
    return RetrievalTrace(
        tuple(ScoredReference(ref, score, score) for ref, score in scores), 0, 1, 2, 3
    )


def test_metric_denominators_and_rejection():
    rows = [{"id": "p", "relevant_refs": ["a", "b"]}, {"id": "n", "relevant_refs": []}]
    traces = {"p": trace(("x", 0.9), ("a", 0.8), ("b", 0.7)), "n": trace(("x", 0.1))}
    m = metrics(rows, traces, 0.5)
    assert m["recall_at_15"] == 1 and m["recall_at_5"] == 1
    assert m["mrr_at_5"] == 0.5
    assert m["negative_query_rejection_rate"] == 1
    assert m["unjudged_returned_document_fraction"] == pytest.approx(1 / 3)
    assert m["ndcg_at_5"] == pytest.approx(
        (1 / math.log2(3) + 1 / math.log2(4)) / (1 + 1 / math.log2(3))
    )


def test_tuning_cannot_use_held_out_labels():
    rows = [
        {"id": "c", "split": "calibration", "relevant_refs": ["a"]},
        {"id": "n", "split": "calibration", "relevant_refs": []},
        {"id": "e", "split": "evaluation", "relevant_refs": ["b"]},
    ]
    traces = {"c": trace(("a", 0.9)), "n": trace(("x", 0.2)), "e": trace(("b", 0.1))}
    selected, _ = tune_threshold(rows, traces, [0, 0.5, 0.95])
    changed = deepcopy(rows)
    changed[-1]["relevant_refs"] = []
    assert selected == tune_threshold(changed, traces, [0, 0.5, 0.95])[0] == 0.5


@pytest.mark.parametrize("qrels", [[], ["a"]])
def test_calibration_requires_both_positive_and_negative_queries(qrels):
    rows = [{"id": "c", "split": "calibration", "relevant_refs": qrels}]
    with pytest.raises(ValueError, match="positive and negative"):
        tune_threshold(rows, {"c": trace(("a", .5))})
