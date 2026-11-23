"""Baseline information boundaries and metrics, not an independent model evaluation."""
import asyncio
from copy import deepcopy
import json

import numpy as np
import pytest

from beauty_agent.action_planner import RuleBasedActionPlanner
from beauty_agent.afa.baselines import (GreedyPolicy, RandomPolicy, RulePolicy, TabularBC,
                                       compare, describe_episodes, fit_bc, public_state)
from beauty_agent.afa.environment import StaticAFAEnv, load_split
from beauty_agent.afa.stage0 import snapshot
from beauty_agent.modules.kb_adapter import KBEngineAdapter


@pytest.fixture(scope="module")
def fit_data():
    contract, rows = load_split("train")
    return contract, rows, fit_bc(contract, rows)


def test_rule_order_and_bc_teacher_match_existing_runtime_planner(fit_data):
    contract, _, table = fit_data
    rule = RulePolicy(contract)
    kb = KBEngineAdapter()
    for key, label in table.items():
        sample = json.loads(key)
        observation = np.asarray(sample["observation"], dtype=np.float32)
        mask = np.asarray(sample["mask"], dtype=bool)
        card, visible, _ = public_state(contract, observation)
        context, _ = snapshot(contract, card, visible, kb)
        allowed = {tuple(contract["action_dictionary"][i]) for i in np.flatnonzero(mask)}
        context.available_actions = [a for a in context.available_actions if (a.action, a.target_id) in allowed]
        expected = asyncio.run(RuleBasedActionPlanner().plan_action(context))
        assert tuple(contract["action_dictionary"][label]) == (expected.action, expected.target_id)
        assert rule.select(observation, mask) == label


@pytest.mark.parametrize("fit", [fit_bc, GreedyPolicy])
def test_fitting_refuses_validation_or_test_rows(fit_data, fit):
    contract, rows, _ = fit_data
    broken = deepcopy(rows)
    broken[0]["split"] = "test_internal"
    with pytest.raises(ValueError, match="train-only"):
        fit(contract, broken)


def test_policies_receive_same_public_input_despite_different_hidden_worlds(fit_data):
    contract, rows, table = fit_data
    env = StaticAFAEnv()
    indices = [i for i, r in enumerate(env._records) if r["environment_only"]["card_id"] == "B-C02"]
    first, _ = env.reset(options={"world_index": indices[0]})
    first_mask = env.action_masks()
    second, _ = env.reset(options={"world_index": indices[1]})
    second_mask = env.action_masks()
    for factory in [lambda: RulePolicy(contract), lambda: GreedyPolicy(contract, rows),
                    lambda: TabularBC(contract, table), lambda: RandomPolicy(contract, 4)]:
        assert factory().select(first, first_mask) == factory().select(second, second_mask)


def test_bc_and_prior_support_fallbacks_are_counted(fit_data):
    contract, _, _ = fit_data
    env = StaticAFAEnv()
    obs, _ = env.reset(seed=0)
    mask = env.action_masks()
    expected = RulePolicy(contract).select(obs, mask)
    for policy in [TabularBC(contract, {}), GreedyPolicy(contract, [])]:
        assert policy.select(obs, mask) == expected
        assert policy.fallbacks == 1


def test_random_policy_only_uses_masked_actions_and_seed_reproduces(fit_data):
    contract, _, _ = fit_data
    env = StaticAFAEnv()
    obs, _ = env.reset(seed=0)
    mask = env.action_masks()
    a, b = RandomPolicy(contract, 3), RandomPolicy(contract, 3)
    first = [a.select(obs, mask) for _ in range(30)]
    assert first == [b.select(obs, mask) for _ in range(30)]
    assert all(mask[i] for i in first)
    assert {contract["action_dictionary"][i][0] for i in first} == {"ask_user", "hold"}
    acquire = RandomPolicy(contract, 3, acquisition_only=True)
    assert all(contract["action_dictionary"][acquire.select(obs, mask)][0] == "ask_user" for _ in range(10))


def test_no_drafts_has_undefined_conditional_error():
    episodes = [{"questions": 0, "cost": 0, "return": -5, "world_fingerprint": "synthetic",
                 "terminal": "hold", "correct_terminal": False, "semantic_match": False, "policy_fallbacks": 0}]
    summary = describe_episodes(episodes)
    assert summary["error_among_drafts"] is None
    assert summary["mean_questions"] == 0 and summary["correct_terminal_rate"] == 0


def test_stage4_never_scores_test_split():
    with pytest.raises(ValueError, match="does not score"):
        compare(evaluation_splits=("test_internal",))


def test_comparison_has_train_only_fit_and_paired_worlds():
    requested = []

    def factory(split):
        requested.append(split)
        return StaticAFAEnv(split)

    report = compare(seeds=(0,), env_factory=factory)
    assert requested == ["train", "val_internal"]
    assert report["fit"]["split"] == "train" and report["fit"]["worlds"] == 6
    for split in ("train", "val_internal"):
        groups = {}
        for row in report["episodes"]:
            if row["split"] == split:
                groups.setdefault(row["policy"], set()).add(row["world_fingerprint"])
        assert len(groups) == 5
        assert all(worlds == next(iter(groups.values())) for worlds in groups.values())
    validation = next(r for r in report["headroom_analysis_evaluator_only"] if r["split"] == "val_internal")
    assert validation["gap_to_hindsight"] == 0  # Honest lack of headroom on the tiny frozen validation set.
