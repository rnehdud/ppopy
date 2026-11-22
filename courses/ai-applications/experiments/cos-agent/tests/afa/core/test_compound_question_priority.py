import json
import subprocess
import sys

import pytest

from beauty_agent.afa.compound_evaluation import DATA, PROJECT, _no_overlap, _read, evaluate
from beauty_agent.afa.question_priority import rank_questions
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime_contracts import QuestionCandidate


def test_cleansing_question_ranking_reduces_questions_without_changing_outcomes():
    result = evaluate(_read(DATA / "development.json"))
    assert result["summary"]["baseline"]["correct"] == result["summary"]["ranked"]["correct"] == 4
    assert result["new_outcome_errors"] == result["reasked"] == 0
    assert result["questions_saved"] > 0
    assert result["adopt"]


def test_rank_questions_returns_original_order_outside_scope_or_single():
    adapter = KBEngineAdapter()
    candidates = [
        QuestionCandidate(slot_id="method.drying", question_text="q1", card_ids=["B-C02"]),
        QuestionCandidate(slot_id="method.tools", question_text="q2", card_ids=["B-C02"]),
    ]
    evaluated = {"raw": {"overall": "hold", "guidance": []}, "hold_signals": [], "retrieve_slots": []}
    assert rank_questions(adapter, ["B-C01", "B-C02", "B-C05", "B-P01"], {}, candidates, evaluated) == candidates
    assert rank_questions(adapter, ["B-C02", "B-C05"], {}, candidates[:1], evaluated) == candidates[:1]


def test_development_and_heldout_remain_disjoint():
    dev = _read(DATA / "development.json")
    held = _read(DATA / "heldout.json")
    _no_overlap(dev, held)

    overlap = {**held, "cases": [{**held["cases"][0], "family": dev["cases"][0]["family"]}]}
    with pytest.raises(ValueError, match="disjoint"):
        _no_overlap(dev, overlap)


def test_heldout_cli_rejects_mismatched_lock(tmp_path):
    bad_lock = tmp_path / "bad_lock.json"
    bad_lock.write_text(json.dumps({"sources": {}, "gate": {}}), encoding="utf-8")
    out_path = tmp_path / "out.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "beauty_agent.afa.compound_evaluation",
            "heldout",
            "--lock",
            str(bad_lock),
            "--output",
            str(out_path),
        ],
        cwd=PROJECT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
