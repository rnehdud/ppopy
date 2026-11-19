"""Fold role binding, fresh fitting, hidden-label exclusion and matched-quality scoring."""
from copy import deepcopy
import json

import numpy as np
import pytest

from beauty_agent.afa import fold_baselines as runner
from beauty_agent.afa.joint_baselines import TrainModel


@pytest.fixture(scope="module")
def source():
    return runner.load_schedule()


@pytest.fixture(scope="module")
def short_protocol():
    protocol = runner.read_protocol()
    # Unit mechanics only; the actual CLI uses all fixed seeds/costs/folds.
    protocol["seeds"] = [0]
    protocol["cost_protocols"] = ["unit_primary"]
    return protocol


@pytest.fixture(scope="module")
def one_fold(source, short_protocol):
    return runner.run_fold(source[0], source[1]["folds"][0], short_protocol)


def test_protocol_is_frozen_before_fold_scores():
    protocol = runner.read_protocol()
    assert protocol["seeds"] == [0, 1, 2] and protocol["folds"] == 16
    assert protocol["fit_worlds_per_fold"] == 45 and protocol["check_worlds_per_fold"] == 3
    assert protocol["cross_fold_model_or_checkpoint_carryover"] is False


def test_projection_changes_only_experiment_role_and_preserves_source(source):
    records, plan = source
    old = deepcopy(records)
    fold = plan["folds"][0]
    fit, check = runner.project_fold(records, fold)
    assert records == old and len(fit) == 45 and len(check) == 3
    assert set(row["root_world_id"] for row in fit) == set(fold["fit_root_ids"])
    assert not {row["family_id"] for row in fit} & {row["family_id"] for row in check}
    lookup = {row["root_world_id"]: row for row in records}
    for row in fit + check:
        original = lookup[row["root_world_id"]]
        assert row["environment_only"] == original["environment_only"]
        assert row["source_split"] == original["split"]
    assert all(row["split"] == "train" for row in fit)
    assert all(row["split"] == "fold_check" for row in check)


@pytest.mark.parametrize("kind", ["root", "family"])
def test_held_record_or_family_cannot_enter_fit(source, kind):
    records, plan = source
    fold = deepcopy(plan["folds"][0])
    if kind == "root":
        fold["fit_root_ids"][0] = fold["check_root_ids"][0]
    else:
        fold["fit_root_ids"][0], fold["check_root_ids"][0] = fold["check_root_ids"][0], fold["fit_root_ids"][0]
    with pytest.raises(ValueError, match="overlap|held family"):
        runner.project_fold(records, fold)


def test_check_role_is_refused_by_training_constructor(source):
    _, check = runner.project_fold(source[0], source[1]["folds"][0])
    with pytest.raises(ValueError, match="train-only"):
        TrainModel(check)


def test_private_held_reference_cannot_change_fitted_prior(source):
    records, plan = source
    fold = plan["folds"][0]
    fit, _ = runner.project_fold(records, fold)
    changed = deepcopy(records)
    for row in changed:
        if row["root_world_id"] in fold["check_root_ids"]:
            row["environment_only"]["reference"] = {"synthetic_marker": "never fit this"}
    other_fit, _ = runner.project_fold(changed, fold)
    assert TrainModel(fit).worlds == TrainModel(other_fit).worlds


def test_new_model_constructed_for_each_fold(source, short_protocol, monkeypatch):
    created = []

    class ObservedTrain(TrainModel):
        def __init__(self, records):
            super().__init__(records)
            created.append(self)

    monkeypatch.setattr(runner, "TrainModel", ObservedTrain)
    for fold in source[1]["folds"][:2]:
        result = runner.run_fold(source[0], fold, short_protocol)
        assert not set(result["fit_root_ids"]) & set(result["check_root_ids"])
    assert len(created) == 2 and created[0] is not created[1]
    assert set(created[0].fit_roots) != set(created[1].fit_roots)


def test_fold_env_exposes_no_fold_or_private_world_identity(source):
    _, check = runner.project_fold(source[0], source[1]["folds"][0])
    env = runner.FoldCheckEnv(check, "unit_primary")
    observations = []
    for index in range(3):
        observation, info = env.reset(seed=0, options={"world_index": index})
        observations.append(observation)
        assert info == {"dispatch_count": 0}
        assert env.visible_observations == {}
    for observation in observations[1:]:
        np.testing.assert_array_equal(observations[0], observation)


def test_pairing_and_quality_gate_for_cost_comparison(one_fold):
    episodes = one_fold["episodes"]
    result = runner.summarize(episodes)
    native = next(row for row in result if row["policy"] == "existing_rule_order")
    assert native["paired_mean_cost_saved_vs_native"] == 0
    assert native["correct_terminal_rate"] == 1 and native["distinct_worlds"] == 3
    altered = deepcopy(episodes)
    for row in altered:
        if row["policy"] == "uniform_all_allowed":
            row["correct_terminal"] = False
    random = next(row for row in runner.summarize(altered) if row["policy"] == "uniform_all_allowed")
    assert not random["matched_quality_to_native"] and random["paired_mean_cost_saved_vs_native"] is None
    with pytest.raises(ValueError, match="unpaired"):
        runner.summarize(episodes[:-1])


def test_changed_schedule_is_rejected_before_execution(tmp_path, monkeypatch):
    changed = json.loads(runner.PLAN.read_text(encoding="utf-8"))
    changed["folds"][0]["fold_id"] = 99
    path = tmp_path / "changed.json"
    path.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(runner, "PLAN", path)
    with pytest.raises(ValueError, match="plan drift"):
        runner.load_schedule()
