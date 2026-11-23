import pytest

pytest.importorskip("sb3_contrib")

from beauty_agent.afa.partial_context_eval import ToolsFirst, run_case
from beauty_agent.afa.ppo_preflight import MaskedC02Env, evaluate, fixed_policy
from beauty_agent.afa.v67_fixtures import SLOTS


def test_empty_context_preserves_legacy_baseline_per_case():
    legacy = evaluate(MaskedC02Env("val_internal"), fixed_policy(SLOTS))
    env = MaskedC02Env("val_internal")
    for index, expected in enumerate(legacy["cases"]):
        actual = run_case(env, index, (), ToolsFirst())
        assert {key: actual[key] for key in expected} == expected


def test_prefilled_answers_are_not_counted_as_questions():
    env = MaskedC02Env("val_internal")
    cases = [run_case(env, index, tuple(SLOTS), ToolsFirst()) for index in range(len(env.rows))]
    assert any("declined" in row["prefilled"].values() for row in cases)
    assert any("unknown" in row["prefilled"].values() for row in cases)
    assert all(not row["asked_feature_order"] and not row["reasked"] for row in cases)
    assert all(row["correct_terminal"] and row["return"] == 0 for row in cases)
