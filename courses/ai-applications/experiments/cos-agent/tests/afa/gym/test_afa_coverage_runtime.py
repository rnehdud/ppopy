"""New hand-case coverage uses the unchanged runtime; no policy comparison here."""
import pytest
import numpy as np

from beauty_agent.afa.coverage_repair import BUNDLE
from beauty_agent.afa.joint_environment import JointAFAEnv


@pytest.mark.parametrize("split", ["val_internal", "test_internal"])
def test_new_hand_family_runs_through_the_existing_environment(split):
    env = JointAFAEnv(split, bundle=BUNDLE)
    index = next(i for i, row in enumerate(env._records) if row["environment_only"]["response_table"]["method.tools"]["value"] == "hands")
    obs, info = env.reset(seed=0, options={"world_index": index})
    assert info == {"dispatch_count": 0} and obs.shape == (64,)
    for _ in range(6):
        mask = env.action_masks()
        asks = [int(i) for i in np.flatnonzero(mask) if env._pairs[i][0] == "ask_user"]
        if asks:
            action = asks[0]
        else:
            enabled = [int(i) for i in np.flatnonzero(mask)]
            action = min(enabled, key=lambda i: {"request_draft": 0, "hold": 1}[env._pairs[i][0]])
        obs, reward, done, truncated, _ = env.step(action)
        assert env.observation_space.contains(obs) and not truncated
        if done:
            assert reward == 0
            break
    else:
        raise AssertionError("mechanics probe did not terminate")
