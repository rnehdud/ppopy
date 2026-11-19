"""Joint environment: visibility, weighted transitions, safety and atomicity."""
from copy import deepcopy
import json

import gymnasium as gym
import numpy as np
import pytest

from beauty_agent.afa.joint_environment import JointAFAEnv


@pytest.fixture(scope="module")
def env():
    return JointAFAEnv()


def choose(env, **values):
    return next(i for i, row in enumerate(env._records) if all(
        row["environment_only"]["response_table"][key]["value"] == value for key, value in values.items()))


def ask(env, slot):
    return env.step(env._pairs.index(("ask_user", slot)))


def test_only_requested_answers_are_visible_and_schema_is_versioned(env):
    observation, info = env.reset(seed=1)
    assert observation.shape == (64,) and env.observation_space.contains(observation)
    assert info == {"dispatch_count": 0} and env.visible_observations == {}
    assert env._pairs != [] and not any(key in json.dumps(info) for key in ("reference", "root_world_id", "family"))
    ask(env, "method.body_site")
    assert set(env.visible_observations) == {"method.body_site"} and env.dispatch_count == 1


def test_friction_first_reopens_tools_only_in_joint_adapter(env):
    index = choose(env, **{"method.water_temperature": "hot", "method.friction": "strong"})
    env.reset(options={"world_index": index})
    for slot in ("method.body_site", "method.water_temperature", "method.friction"):
        ask(env, slot)
    assert env.action_masks()[env._pairs.index(("ask_user", "method.tools"))]
    assert not env.action_masks()[env._pairs.index(("request_draft", "label_draft"))]


@pytest.mark.parametrize("action", [-1, 8, True, "0", 1])
def test_invalid_or_masked_action_is_not_a_transition(env, action):
    before, _ = env.reset(seed=0)
    prepared = env._prepared
    with pytest.raises(ValueError):
        env.step(action)
    assert env._prepared == prepared and env.dispatch_count == 0
    np.testing.assert_array_equal(before, env._encode(env._prepared, env._remaining, env._remaining_cost))


@pytest.mark.parametrize("failure", ["answer", "encode"])
def test_late_failure_rolls_back_dispatch_state_and_cost(env, monkeypatch, failure):
    before, _ = env.reset(seed=0)
    prepared, left = env._prepared, env._remaining_cost

    def fail(*args):
        raise ValueError("synthetic failure")

    monkeypatch.setattr(env, "_answer" if failure == "answer" else "_encode", fail)
    with pytest.raises(ValueError, match="synthetic failure"):
        ask(env, "method.body_site")
    assert env._prepared == prepared and env.dispatch_count == 0 and env.visible_observations == {}
    assert env._remaining_cost == left


def test_weighted_cost_is_public_and_matches_the_asked_slot():
    env = JointAFAEnv(cost_protocol="weighted_sensitivity")
    observation, _ = env.reset(seed=0)
    assert set(observation[58:63]) == {1, 2} and observation[63] == 7
    assert ask(env, "method.body_site")[1] == -1
    assert ask(env, "method.friction")[1] == -2
    assert env._remaining_cost == 4


def test_premature_hold_and_external_truncation_are_distinct(env):
    env.reset(seed=0)
    _, reward, done, truncated, _ = env.step(env._pairs.index(("hold", "insufficient_information")))
    assert reward == -6 and done and not truncated and not env.action_masks().any()
    with pytest.raises(ValueError, match="reset required"):
        env.step(0)
    wrapper = gym.wrappers.TimeLimit(JointAFAEnv(), max_episode_steps=1)
    wrapper.reset(seed=0)
    _, reward, done, truncated, _ = wrapper.step(0)
    assert reward == -1 and not done and truncated


def test_explicit_world_does_not_advance_random_sequence(env):
    env.reset(seed=17, options={"world_index": 0})
    state = deepcopy(env.np_random.bit_generator.state)
    env.reset(options={"world_index": 1})
    assert env.np_random.bit_generator.state == state


def test_last_affordable_answer_still_allows_free_terminal(env):
    index = choose(env, **{"method.water_temperature": "hot", "method.tools": "hands",
                           "method.friction": "gentle", "method.drying": "pat_gently"})
    env.reset(options={"world_index": index})
    for slot in env._schema["slot_order"]:
        ask(env, slot)
    assert env._remaining == env._remaining_cost == 0
    _, reward, done, truncated, _ = env.step(env._pairs.index(("request_draft", "label_draft")))
    assert reward == 0 and done and not truncated


def test_injected_budget_exhaustion_is_termination_with_loss(env):
    env.reset(seed=0)
    env._remaining, env._remaining_cost = 1, 1  # engineering boundary, not a changed task protocol
    _, reward, done, truncated, info = ask(env, "method.body_site")
    assert reward == -7 and done and not truncated and info["execution_status"] == "task_budget_exhausted"
