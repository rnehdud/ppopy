"""Real library initialization/masking/serialization; no optimizer learning here."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile

import numpy as np
import pytest
import torch

from beauty_agent.afa import ppo
from beauty_agent.afa.environment import StaticAFAEnv


@pytest.fixture(scope="module")
def prepared():
    outputs = ppo.ROOT / "outputs"
    outputs.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="afa-ppo-setup-tests-", dir=outputs) as temporary:
        directory = Path(temporary) / "prepared"
        original = ppo.MaskablePPO.learn

        def forbidden(*args, **kwargs):
            raise AssertionError("prepare must not learn")

        ppo.MaskablePPO.learn = forbidden
        try:
            result = ppo.run("prepare", directory)
        finally:
            ppo.MaskablePPO.learn = original
        yield directory, result


def test_prepare_uses_real_libraries_without_learning(prepared):
    directory, result = prepared
    assert result["learning_executed"] is False
    assert result["num_timesteps"] == result["collector_mask_checks"] == 0
    assert result["save_reload_equivalent"]
    assert len(result["evaluation"]["episodes"]) == 6
    assert result["evaluation"]["summary"]["distinct_worlds"] == 6
    assert len(result["official_masked_evaluator"]["rewards"]) == 2
    assert (directory / "initialized_model.zip").is_file()
    assert not (directory / "model.zip").exists()
    assert not result["efficiency_claim"]


def test_saved_policy_probability_is_zero_for_disabled_actions(prepared):
    model, _ = ppo.load_checkpoint(prepared[0])
    env = StaticAFAEnv()
    try:
        obs, _ = env.reset(seed=0)
        mask = env.action_masks()
        tensor, _ = model.policy.obs_to_tensor(obs)
        with torch.no_grad():
            probabilities = model.policy.get_distribution(tensor, action_masks=mask).distribution.probs.cpu().numpy()[0]
        assert np.isfinite(probabilities).all()
        assert probabilities.sum() == pytest.approx(1)
        assert np.all(probabilities[~mask] == 0)
        for index in np.flatnonzero(mask):
            only = np.zeros_like(mask)
            only[index] = True
            action, _ = model.predict(obs, action_masks=only, deterministic=True)
            assert int(action) == int(index)
    finally:
        env.close()


def test_evaluation_refuses_validation_and_test():
    for split in ("val_internal", "test_internal"):
        with pytest.raises(ValueError, match="train only"):
            ppo.evaluate_cohort(None, split, 0)


def test_collector_audit_detects_invalid_selection():
    callback = ppo.MaskAuditCallback()
    callback.locals = {"action_masks": np.array([[True, False]]), "actions": np.array([0])}
    assert callback._on_step()
    assert callback.checked_actions == 1
    callback.locals["actions"] = np.array([1])
    with pytest.raises(ValueError, match="masked action"):
        callback._on_step()
    assert callback.checked_actions == 1


@pytest.mark.parametrize("changes,reason", [({"gamma": 0.99}, "total-cost"),
    ({"fit_split": "test_internal"}, "train-only"), ({"batch_size": 7}, "batch"),
    ({"total_timesteps": 33}, "rollout budget"), ({"approved_reference": True}, "approval")])
def test_invalid_protocol_rejected_before_model_creation(tmp_path, changes, reason):
    config = deepcopy(ppo.read_config())
    config.update(changes)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError, match=reason):
        ppo.read_config(path)


@pytest.mark.parametrize("tamper,reason", [("checkpoint", "bytes drift"), ("config", "config drift")])
def test_checkpoint_tampering_rejected_before_deserialization(prepared, tamper, reason):
    with tempfile.TemporaryDirectory(prefix="tampered-", dir=prepared[0].parent) as temporary:
        directory = Path(temporary) / "copy"
        shutil.copytree(prepared[0], directory)
        path = directory / ("initialized_model.zip" if tamper == "checkpoint" else "config.json")
        if tamper == "checkpoint":
            path.write_bytes(path.read_bytes() + b"synthetic corruption")
        else:
            config = json.loads(path.read_text(encoding="utf-8"))
            config["seed"] = 9
            path.write_text(json.dumps(config), encoding="utf-8")
        with pytest.raises(ValueError, match=reason):
            ppo.load_checkpoint(directory)


def test_code_drift_rejected(prepared, monkeypatch):
    monkeypatch.setattr(ppo, "input_hashes", lambda: {"changed": "synthetic"})
    with pytest.raises(ValueError, match="input/code drift"):
        ppo.load_checkpoint(prepared[0])


def test_existing_run_and_outside_outputs_refused(prepared):
    with pytest.raises(FileExistsError):
        ppo.run("prepare", prepared[0])
    with pytest.raises(ValueError, match="outputs"):
        ppo.output_path(ppo.EXPERIMENT / "weights")
