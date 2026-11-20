"""Verify a completed connection trial without performing any further learning."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import torch

from . import ppo
from .stage0 import require


def verify(trained_dir, initial_dir):
    trained_dir, initial_dir = ppo.output_path(trained_dir), ppo.output_path(initial_dir)
    model, manifest = ppo.load_checkpoint(trained_dir)
    initial, initial_manifest = ppo.load_checkpoint(initial_dir)
    config = manifest["config"]
    require(config == initial_manifest["config"], "initial/trained configuration mismatch")
    require(initial.num_timesteps == 0 and model.num_timesteps == config["total_timesteps"],
            "expected untrained initial model and complete fixed-budget trial")
    current, original = model.policy.state_dict(), initial.policy.state_dict()
    require(current.keys() == original.keys(), "policy architecture changed")
    require(all(torch.isfinite(value).all().item() for value in current.values()), "non-finite weights")
    changed = [key for key in current if not torch.equal(current[key], original[key])]
    require(changed, "trial did not update policy parameters")
    max_change = max(float((current[key] - original[key]).abs().max()) for key in current)
    epochs = config["total_timesteps"] // config["n_steps"] * config["n_epochs"]
    optimizer_steps = [int(state["step"].item()) for state in model.policy.optimizer.state.values() if "step" in state]
    expected_steps = epochs * config["n_steps"] // config["batch_size"]
    require(model._n_updates == epochs and optimizer_steps and
            min(optimizer_steps) == max(optimizer_steps) == expected_steps, "optimizer/update budget mismatch")
    with (trained_dir / "logs/progress.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == config["total_timesteps"] // config["n_steps"], "missing rollout log rows")
    require([int(float(row["time/total_timesteps"])) for row in rows] ==
            list(range(config["n_steps"], config["total_timesteps"] + 1, config["n_steps"])), "rollout log budget mismatch")
    require(all(math.isfinite(float(value)) for row in rows for value in row.values() if value), "non-finite log values")
    require(any(row.get("train/loss") for row in rows), "missing optimization metrics")
    recorded = json.loads((trained_dir / "report.json").read_text(encoding="utf-8"))
    recorded_initial = json.loads((initial_dir / "report.json").read_text(encoding="utf-8"))
    require(recorded["learning_executed"] is True and recorded_initial["learning_executed"] is False,
            "learning provenance mismatch")
    require(recorded["collector_mask_checks"] == model.num_timesteps and recorded["save_reload_equivalent"],
            "collector/reload check incomplete")
    evaluated = ppo.evaluate_cohort(model, "train", config["seed"])
    evaluated_initial = ppo.evaluate_cohort(initial, "train", config["seed"])
    require(evaluated == recorded["evaluation"] and evaluated_initial == recorded_initial["evaluation"],
            "fresh reload evaluation changed")
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "single-seed train-only connection trial; no extra learning or tuning",
            "seed": config["seed"], "num_timesteps": model.num_timesteps,
            "collector_mask_checks": recorded["collector_mask_checks"], "invalid_action_selections": 0,
            "policy_tensors_changed": len(changed), "policy_tensors_total": len(current),
            "maximum_absolute_parameter_change": max_change,
            "all_weights_and_recorded_log_values_finite": True,
            "ppo_epoch_updates": model._n_updates, "optimizer_steps_per_parameter": expected_steps,
            "csv_rollout_rows": len(rows), "fresh_process_reload_evaluation_identical": True,
            "before_train_diagnostic": evaluated_initial["summary"], "after_train_diagnostic": evaluated["summary"],
            "test_or_validation_scoring": False, "efficiency_claim": False,
            "note": "SB3 dumps logs before each optimization; final update count is checked in the saved model",
            "versions": ppo.versions(), "source_hashes": manifest["source_hashes"],
            "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "initial_checkpoint_sha256": initial_manifest["checkpoint_sha256"],
            "trained_checkpoint_sha256": manifest["checkpoint_sha256"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trained-dir", type=Path, required=True)
    parser.add_argument("--initial-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    path = ppo.output_path(args.report)
    require(not path.exists(), "audit report already exists")
    result = verify(args.trained_dir, args.initial_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    ppo.write_json(path, result)
    print(json.dumps({k: v for k, v in result.items() if k not in {"source_hashes", "versions"}}))


if __name__ == "__main__":
    main()
