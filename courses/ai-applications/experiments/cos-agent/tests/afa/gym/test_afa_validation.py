"""Exhaustive contract audit and deliberate defect detection; no policy fitting."""
import json

import pytest

from beauty_agent.afa.environment import StaticAFAEnv
from beauty_agent.afa.stage0 import DEFAULT
from beauty_agent.afa.validation import RawReference, boundary_probes, validate_all


@pytest.fixture(scope="module")
def report():
    return validate_all()


def test_all_supported_paths_and_masked_actions_match_raw_reference(report):
    assert report["summary"] == {
        "worlds": 10, "distinct_public_states": 34, "prefix_states": 88,
        "allowed_transitions": 203, "masked_rejections": 501, "terminal_paths": 125,
        "minimum_best_valid_vs_wrong_margin": 1.0}


def test_bad_stops_never_beat_even_longest_valid_completion(report):
    for world in report["worlds"]:
        assert world["best_wrong_exit_return"] < world["worst_valid_return"]
        assert world["correct_terminal_paths"] > 0 and world["incorrect_terminal_paths"] > 0
    assert any(w["branch_trace_differences_with_same_semantics"] for w in report["worlds"])


def test_reference_keeps_action_meaning_difference_instead_of_inventing_equivalence():
    reference = RawReference(json.loads(DEFAULT.read_text(encoding="utf-8")))
    tools = reference.evaluate("B-C02", {"method.body_site": "face", "method.tools": "scrub_brush"})
    friction = reference.evaluate("B-C02", {"method.body_site": "face", "method.friction": "strong"})
    assert tools["semantic"]["cards"][0]["text"] == friction["semantic"]["cards"][0]["text"]
    assert tools["semantic"] != friction["semantic"]


def test_validator_detects_injected_reward_bug():
    class RewardBug(StaticAFAEnv):
        def step(self, action):
            observation, reward, done, truncated, info = super().step(action)
            return observation, reward + 0.25, done, truncated, info

    with pytest.raises(ValueError, match="reward/termination mismatch"):
        validate_all(env_factory=RewardBug)


def test_validator_detects_injected_mask_bug():
    class MaskBug(StaticAFAEnv):
        def action_masks(self):
            mask = super().action_masks()
            mask[1] = True
            return mask

    with pytest.raises(AssertionError):
        validate_all(env_factory=MaskBug)


def test_budget_completion_and_existing_mandatory_hold_edges():
    probes = boundary_probes()
    assert probes["normal_budget_exhaustion_reachable"] is False
    assert probes["under_budget_injected_probe"]["passed"]
    assert probes["last_affordable_answer_then_free_completion"]
    assert probes["out_of_scope_B_B01_existing_safety_gate"]
