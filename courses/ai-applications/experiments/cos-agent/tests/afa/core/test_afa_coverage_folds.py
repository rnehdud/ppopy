"""All families can be checked in isolated folds without copying a singleton."""
from copy import deepcopy

import pytest

from beauty_agent.afa.coverage_folds import PLAN, build_plan, validate_plan
from beauty_agent.afa.joint_data import SPLITS, load_joint_split


@pytest.fixture(scope="module")
def original():
    return [row for split in SPLITS for row in load_joint_split(split)]


def test_fixed_fold_plan_covers_all_families_and_aligned_case():
    import json
    plan, report = build_plan()
    assert json.loads(PLAN.read_text(encoding="utf-8")) == plan
    assert report["folds"] == 16 and report["distinct_checked_roots"] == 48
    assert report["aligned_method_roots_checked"] == 3
    assert not report["fold_scores_computed"] and not report["independent_evaluation_ready"]


def test_reusing_a_held_world_for_fit_is_rejected(original):
    plan, _ = build_plan()
    changed = deepcopy(plan)
    changed["folds"][0]["fit_root_ids"][0] = changed["folds"][0]["check_root_ids"][0]
    with pytest.raises(ValueError, match="overlap or omission"):
        validate_plan(changed, original)


def test_duplicate_held_family_is_rejected(original):
    plan, _ = build_plan()
    changed = deepcopy(plan)
    changed["folds"][1] = deepcopy(changed["folds"][0])
    with pytest.raises(ValueError, match="duplicate or missing"):
        validate_plan(changed, original)


def test_checkpoint_carryover_is_not_allowed(original):
    plan, _ = build_plan()
    plan["checkpoint_carryover"] = True
    with pytest.raises(ValueError, match="fold-isolated"):
        validate_plan(plan, original)
