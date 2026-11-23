"""The mechanics checker catches deliberately broken environment transitions."""
import pytest

from beauty_agent.afa.joint_environment import JointAFAEnv
from beauty_agent.afa.joint_validation import verify_world
from beauty_agent.afa.semantics import SemanticInspector


def test_one_world_all_reachable_public_states_pass_contract_check():
    counts = verify_world(JointAFAEnv(), 0, SemanticInspector(), {})
    assert counts["states"] > 1 and counts["valid_transitions"] > counts["states"]
    assert counts["masked_rejections"] > 0 and counts["terminal_transitions"] > 0


def test_wrong_reward_is_detected():
    class WrongReward(JointAFAEnv):
        def step(self, action):
            observation, reward, done, truncated, info = super().step(action)
            return observation, reward + 1, done, truncated, info

    with pytest.raises(ValueError, match="cost/termination"):
        verify_world(WrongReward(), 0, SemanticInspector(), {})
