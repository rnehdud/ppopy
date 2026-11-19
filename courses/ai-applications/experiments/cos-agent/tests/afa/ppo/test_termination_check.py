from copy import deepcopy

import pytest

pytest.importorskip("sb3_contrib")

from beauty_agent.afa.partial_context_eval import ToolsFirst, run_case
from beauty_agent.afa.outcome_review import OutcomeEnv, runtime_outcome
from beauty_agent.afa.ppo_preflight import MaskedC02Env
from beauty_agent.afa.termination_check import GuardedEnv
from beauty_agent.afa.v67_fixtures import SLOTS


FIXTURE = "e26:scrub_brush:unknown:rubbing_strongly"


def case(env, prefilled):
    index = next(i for i, row in enumerate(env.rows) if row["fixture"]["fixture_id"] == FIXTURE)
    return run_case(env, index, prefilled, ToolsFirst())


@pytest.mark.parametrize("prefilled", [
    ("method.drying",),
    ("method.friction", "method.drying"),
])
def test_draft_gate_reopens_the_influential_tools_question(prefilled):
    original = case(MaskedC02Env("val_internal"), prefilled)
    guarded = case(GuardedEnv("val_internal"), prefilled)
    assert original["reason"] == "reference_mismatch" and original["questions"] == 0
    assert guarded["correct_terminal"] and guarded["asked_feature_order"] == ["method.tools"]
    assert guarded["reasked"] == []


def test_fully_observed_states_keep_question_free_stop():
    env = GuardedEnv("val_internal")
    rows = [run_case(env, index, tuple(SLOTS), ToolsFirst()) for index in range(len(env.rows))]
    assert all(row["correct_terminal"] and row["questions"] == 0 for row in rows)


def test_equal_b_c02_guidance_does_not_require_extra_question():
    env = OutcomeEnv("val_internal")
    index = next(i for i, row in enumerate(env.rows) if row["fixture"]["fixture_id"] == FIXTURE)
    result = run_case(env, index, ("method.drying",), ToolsFirst(),
                      outcome_signature=runtime_outcome)
    assert result["correct_terminal"] and result["questions"] == 0


def test_outcome_comparison_preserves_operational_differences():
    env = MaskedC02Env("val_internal")
    env.reset(options={"index": 0})
    public = env.book.answer(env.fixture_id, env.session.public, "method.drying")
    evaluated = env.adapter.evaluate(env.session._prepare(public).context.observations, ["B-C02"])
    original = runtime_outcome(evaluated)
    for field, value in [
        ("hold_signals", ["refer_for_professional_review"]),
        ("retrieve_slots", [*evaluated["retrieve_slots"], "product.formulation_ph"]),
    ]:
        changed = deepcopy(evaluated)
        changed[field] = value
        assert runtime_outcome(changed) != original
    changed = deepcopy(evaluated)
    changed["raw"]["results"][0]["automatic_product_replacement"] = True
    assert runtime_outcome(changed) != original
