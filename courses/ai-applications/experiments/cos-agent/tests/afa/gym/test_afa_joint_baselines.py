"""Train-only fitting, public policy inputs, real planner order and paired scoring."""
import asyncio
from fractions import Fraction

import numpy as np
import pytest

from beauty_agent.action_planner import RuleBasedActionPlanner
from beauty_agent.afa.baselines import RulePolicy
from beauty_agent.afa.joint_baselines import (TrainModel, JointRule, JointGreedy, JointMultistep, compare,
                                             diagnostic_bounds, evaluate_episode, public_input)
from beauty_agent.afa.joint_data import load_joint_split
from beauty_agent.afa.joint_environment import JointAFAEnv


@pytest.fixture(scope="module")
def fitted():
    model = TrainModel(load_joint_split("train"))
    return model.inspector.base, model


@pytest.mark.parametrize("split", ["val_internal", "test_internal"])
def test_model_refuses_nontrain_responses(split):
    with pytest.raises(ValueError, match="train-only"):
        TrainModel(load_joint_split(split))


def test_public_decoder_handles_joint_cards_and_actual_costs(fitted):
    base, _ = fitted
    env = JointAFAEnv(cost_protocol="weighted_sensitivity")
    obs, _ = env.reset(seed=0)
    values, costs, states = public_input(base, obs, env.action_masks())
    assert values == {} and costs["method.friction"] == 2 and set(states.values()) == {"not_asked"}
    obs, *_ = env.step(0)
    assert public_input(base, obs, env.action_masks())[0] == {"method.body_site": "face"}
    bad = obs.copy()
    bad[47] = 0
    with pytest.raises(ValueError, match="task/mask"):
        public_input(base, bad, env.action_masks())


def test_rule_order_really_matches_current_runtime_planner(fitted):
    base, _ = fitted
    rule, env = JointRule(base), JointAFAEnv()
    for index in (0, 1, 2):
        observation, _ = env.reset(options={"world_index": index})
        while True:
            mask = env.action_masks()
            action = rule.select(observation, mask)
            expected = asyncio.run(RuleBasedActionPlanner().plan_action(env._prepared.context))
            assert env._pairs[action] == (expected.action, expected.target_id)
            observation, _, done, _, _ = env.step(action)
            if done:
                break


def test_policies_make_same_choice_for_indistinguishable_worlds(fitted):
    base, model = fitted
    env = JointAFAEnv()
    one, _ = env.reset(options={"world_index": 0})
    first_mask = env.action_masks()
    two, _ = env.reset(options={"world_index": 1})
    np.testing.assert_array_equal(one, two)
    for policy in (JointGreedy(base, model), JointMultistep(base, model)):
        assert policy.select(one, first_mask) == policy.select(two, env.action_masks())


@pytest.mark.parametrize("policy_class", [JointGreedy, JointMultistep])
def test_unseen_train_support_uses_counted_rule_fallback(policy_class):
    records = load_joint_split("train")
    model = TrainModel(records[:1])
    first_tools = records[0]["environment_only"]["response_table"]["method.tools"]["value"]
    env = JointAFAEnv()
    index = next(i for i, row in enumerate(env._records) if row["environment_only"]["response_table"]["method.tools"]["value"] != first_tools)
    env.reset(options={"world_index": index})
    env.step(0)
    obs, *_ = env.step(env._pairs.index(("ask_user", "method.tools")))
    mask = env.action_masks()
    policy = policy_class(model.inspector.base, model)
    assert policy.select(obs, mask) == JointRule(model.inspector.base).select(obs, mask)
    assert policy.fallbacks == 1


def test_multistep_expected_cost_agrees_with_actual_train_execution(fitted):
    base, model = fitted
    env = JointAFAEnv()
    policy = JointMultistep(base, model)
    episodes = [evaluate_episode(env, i, policy, 0) for i in range(len(env._records))]
    assert all(row["correct_terminal"] for row in episodes) and policy.fallbacks == 0
    assert model.solve({}, env._cost["ask_costs"])[0] == Fraction(sum(row["cost"] for row in episodes), len(episodes))


def test_neither_comparison_nor_bound_scores_test():
    with pytest.raises(ValueError, match="does not score"):
        compare(evaluation_splits=("test_internal",))
    with pytest.raises(ValueError, match="does not score"):
        diagnostic_bounds(load_joint_split("test_internal"), {k: 1 for k in TrainModel(load_joint_split("train")).inspector.domains})


def test_same_validation_worlds_are_used_for_every_policy():
    report = compare(seeds=(0,), evaluation_splits=("val_internal",), cost_protocols=("unit_primary",))
    assert report["fit"]["split"] == "train" and report["fit"]["worlds"] == 30
    groups = {}
    for row in report["episodes"]:
        groups.setdefault(row["policy"], set()).add(row["world_fingerprint"])
    assert len(groups) == 5 and all(len(worlds) == 9 for worlds in groups.values())
    assert all(worlds == next(iter(groups.values())) for worlds in groups.values())
    assert report["headroom_evaluator_only"][0]["policy_training_use"] is False
