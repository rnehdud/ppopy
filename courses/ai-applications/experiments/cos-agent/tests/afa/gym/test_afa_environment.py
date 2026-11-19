"""Optional rl-group environment API tests; no training or model inference."""
import asyncio
import json

from gymnasium.wrappers import TimeLimit
import numpy as np
import pytest

from beauty_agent.afa.environment import StaticAFAEnv
from beauty_agent.afa import runtime


@pytest.fixture(scope="module")
def env():
    return StaticAFAEnv()


def choose_world(env, card="B-C02"):
    return next(i for i, row in enumerate(env._records) if row["environment_only"]["card_id"] == card)


def test_reset_has_no_action_and_same_card_hidden_worlds_are_not_exposed(env):
    indices = [i for i, r in enumerate(env._records) if r["environment_only"]["card_id"] == "B-C02"]
    first, first_info = env.reset(seed=7, options={"world_index": indices[0]})
    second, second_info = env.reset(seed=7, options={"world_index": indices[1]})
    np.testing.assert_array_equal(first, second)
    assert first_info == second_info == {"dispatch_count": 0}
    assert first.shape == (58,) and first.dtype == np.float32
    assert env.observation_space.contains(first) and env.visible_observations == {}
    assert env.dispatch_count == 0
    second_face, _, _, _, second_face_info = env.step(0)
    env.reset(seed=7, options={"world_index": indices[0]})
    first_face, _, _, _, first_face_info = env.step(0)
    np.testing.assert_array_equal(first_face, second_face)
    assert first_face_info == second_face_info


def test_only_selected_answer_is_revealed_with_one_dispatch(env, monkeypatch):
    env.reset(options={"world_index": choose_world(env)})
    calls = []
    original = runtime.dispatch_action

    async def spy(*args):
        calls.append(args[0].applied.target_id)
        return await original(*args)

    monkeypatch.setattr(runtime, "dispatch_action", spy)
    observation, reward, terminated, truncated, info = env.step(0)
    assert calls == ["method.body_site"] and info["dispatch_count"] == 1
    assert set(env.visible_observations) == {"method.body_site"}
    assert env.visible_observations["method.body_site"]["value"] == "face"
    assert reward == -1 and not terminated and not truncated
    assert env.observation_space.contains(observation)
    assert set(np.flatnonzero(env.action_masks())) == {2, 3, 4, 5}
    assert not any(k in json.dumps(info) for k in ("reference", "response_table", "world_id", "fingerprint"))


@pytest.mark.parametrize("action", [-1, 8, True, "0", 1])
def test_invalid_or_masked_action_has_no_transition(env, action):
    before, _ = env.reset(options={"world_index": choose_world(env)})
    token = env._prepared
    with pytest.raises(ValueError):
        env.step(action)
    assert env._prepared == token and env.dispatch_count == 0
    np.testing.assert_array_equal(before, env._encode(env._prepared, env._remaining))


def test_simulator_failure_rolls_back_entire_step(env, monkeypatch):
    before, _ = env.reset(options={"world_index": choose_world(env)})
    token = env._prepared
    original_answer = env._answer

    def fail(target):
        raise ValueError("synthetic answer failure")

    monkeypatch.setattr(env, "_answer", fail)
    with pytest.raises(ValueError, match="answer failure"):
        env.step(0)
    assert env._prepared == token and env.dispatch_count == 0 and env.visible_observations == {}
    np.testing.assert_array_equal(before, env._encode(env._prepared, env._remaining))
    monkeypatch.setattr(env, "_answer", original_answer)
    env.step(0)
    assert env.dispatch_count == 1


def test_premature_hold_is_penalized_and_requires_reset(env):
    env.reset(options={"world_index": choose_world(env)})
    _, reward, terminated, truncated, _ = env.step(5)
    assert reward == -5 and terminated and not truncated
    assert not env.action_masks().any()
    with pytest.raises(ValueError, match="reset required"):
        env.step(5)


def test_next_observation_encoding_failure_does_not_commit(env, monkeypatch):
    env.reset(options={"world_index": choose_world(env)})
    token = env._prepared

    def fail(*args):
        raise ValueError("synthetic encoding failure")

    monkeypatch.setattr(env, "_encode", fail)
    with pytest.raises(ValueError, match="encoding failure"):
        env.step(0)
    assert env._prepared == token and env.dispatch_count == 0 and env.visible_observations == {}


@pytest.mark.parametrize("split", ["train", "val_internal", "test_internal"])
def test_supported_worlds_finish_with_visible_only_valid_actions(split):
    env = StaticAFAEnv(split)
    for i in range(len(env._records)):
        env.reset(seed=0, options={"world_index": i})
        acquisitions = 0
        while True:
            enabled = list(np.flatnonzero(env.action_masks()))
            action = min(enabled, key=lambda n: {"ask_user": 0, "request_draft": 1, "hold": 2}[env._pairs[n][0]])
            if env._pairs[action][0] == "ask_user":
                acquisitions += 1
            observation, reward, done, truncated, info = env.step(action)
            assert env.observation_space.contains(observation) and not truncated
            if done:
                assert reward == 0  # Valid completion, including cold-water hold.
                assert env.dispatch_count == acquisitions + 1 <= 5
                break


def test_external_time_limit_returns_valid_final_observation(env):
    wrapped = TimeLimit(env, max_episode_steps=1)
    wrapped.reset(options={"world_index": choose_world(env)})
    observation, _, terminated, truncated, _ = wrapped.step(0)
    assert not terminated and truncated
    assert env.observation_space.contains(observation)
    assert set(env.visible_observations) == {"method.body_site"}


def test_concurrent_step_rejected_without_second_dispatch(env):
    env.reset(options={"world_index": choose_world(env)})

    async def run():
        return await asyncio.gather(env.astep(0), env.astep(0), return_exceptions=True)

    results = asyncio.run(run())
    assert sum(isinstance(r, ValueError) for r in results) == 1
    assert env.dispatch_count == 1


def test_sync_api_rejects_existing_loop_without_coroutine_leak(env):
    env.reset(options={"world_index": choose_world(env)})

    async def run():
        with pytest.raises(RuntimeError, match="astep"):
            env.step(0)
        return await env.astep(0)

    asyncio.run(run())
    assert env.dispatch_count == 1
