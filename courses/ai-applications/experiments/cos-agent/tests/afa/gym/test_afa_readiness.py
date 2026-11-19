"""Readiness must distinguish attainable policies from hidden-world shortcuts."""
from copy import deepcopy

import numpy as np
import pytest

from beauty_agent.afa.environment import StaticAFAEnv, load_split
from beauty_agent.afa.readiness import public_information_optimum, semantic_witnesses


@pytest.fixture(scope="module")
def training():
    contract, rows = load_split("train")
    return contract, [r["environment_only"] for r in rows]


def test_optimum_cannot_choose_a_different_first_question_for_each_hidden_world(training):
    contract, worlds = training
    result = public_information_optimum(contract, worlds)
    # Per-world hindsight is 7/3, but those paths cannot be combined into one
    # public-input policy: the worlds are indistinguishable before asking.
    assert result["mean_cost"] == pytest.approx(2.5)
    assert result["mean_cost"] > 7 / 3
    for card in contract["tasks"]:
        roots = [s for s in result["states"] if s["card"] == card and not s["visible"]]
        assert len(roots) == 1
        assert contract["action_dictionary"][roots[0]["action_index"]] == ["ask_user", "method.body_site"]
    assert result["policy_training_use"] is False


def test_belief_analysis_is_invariant_to_private_world_order(training):
    contract, worlds = training
    first = public_information_optimum(contract, worlds)
    second = public_information_optimum(contract, list(reversed(deepcopy(worlds))))
    assert first["mean_cost"] == second["mean_cost"]
    public_choices = lambda r: sorted((s["card"], str(sorted(s["visible"].items())),
                                       s["remaining"], s["action_index"]) for s in r["states"])
    assert public_choices(first) == public_choices(second)


def test_validation_has_no_efficiency_headroom():
    contract, rows = load_split("val_internal")
    assert public_information_optimum(contract, [r["environment_only"] for r in rows])["mean_cost"] == 2


def test_mixed_action_worlds_have_explicit_unresolved_witnesses(training):
    witnesses = semantic_witnesses(training[0])
    assert len(witnesses) == 9
    for world in witnesses:
        expected = world["full_information_reference"]
        assert any(path["semantic"] != expected for path in world["terminal_paths"])
        assert "pending" in world["resolution"]
        assert all(path["questions"] and path["branch_ids"] for path in world["terminal_paths"])


def test_explicit_reset_preserves_random_world_stream():
    env = StaticAFAEnv()
    env.reset(seed=15, options={"world_index": 0})
    before = deepcopy(env.np_random.bit_generator.state)
    env.reset(options={"world_index": 1})
    assert env.np_random.bit_generator.state == before
    expected = np.random.default_rng()
    expected.bit_generator.state = before
    index = int(expected.integers(len(env._records)))
    observation, _ = env.reset()
    random_state = deepcopy(env.np_random.bit_generator.state)
    fixed, _ = env.reset(options={"world_index": index})
    np.testing.assert_array_equal(observation, fixed)
    assert env._world == env._records[index]["environment_only"]
    assert env.np_random.bit_generator.state == random_state
