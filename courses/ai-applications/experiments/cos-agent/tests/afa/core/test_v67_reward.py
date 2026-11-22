import asyncio

import pytest

from beauty_agent.afa.v67_reward import RewardProtocol, check_rewards, score_stop


def test_penalty_keeps_correct_stop_better_than_zero_question_wrong_stop():
    protocol = RewardProtocol()
    with pytest.raises(ValueError, match="entire question budget"):
        RewardProtocol(incorrect_stop_loss=3)
    assert score_stop("hold_with_question_available", True, 0, protocol)["return"] == -4
    assert score_stop("hold_without_available_path", True, 3, protocol)["return"] == -3
    assert score_stop("draft_allowed", False, 1, protocol)["return"] == -5
    assert score_stop("required_hold", False, 0, protocol)["correct_terminal"]


def test_actual_paths_expose_gate_allowed_draft_with_different_reference():
    report = asyncio.run(check_rewards())
    rows = report["terminal_trace"]
    stress = report["branch_priority_check"]["paths"]
    assert stress["method.tools"]["status"] == stress["method.friction"]["status"] == "difference"
    assert stress["method.tools"]["correct_terminal"]
    assert stress["method.friction"]["reason"] == "reference_mismatch"
    assert any(r["reason"] == "hold_without_available_path" for r in rows)
    assert all(value is not None for value in report["best_reachable_valid_stop_by_fixture"].values())
