"""Train fixed B-C02 seeds and record validation curves before opening the test split."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

from sb3_contrib import MaskablePPO
from stable_baselines3.common.callbacks import BaseCallback

from .eda import ROOT, fingerprint
from .ppo_preflight import MaskedC02Env, PPO_SETTINGS, TRIAL_STEPS, evaluate, fixed_policy
from .tracking import receipt
from .v67_fixtures import SLOTS


class RolloutSummary(BaseCallback):
    def __init__(self):
        super().__init__()
        self.curve = []
        self.actions = 0
        self.incorrect = 0

    def _on_step(self):
        self.actions += len(self.locals["actions"])
        self.incorrect += sum(
            item.get("correct_terminal") is False for item in self.locals["infos"]
        )
        return True

    def _on_rollout_end(self):
        episodes = list(self.model.ep_info_buffer)
        if episodes:
            self.curve.append({
                "environment_steps": self.num_timesteps,
                "window_episodes": len(episodes),
                "mean_return": mean(item["r"] for item in episodes),
                "mean_actions": mean(item["l"] for item in episodes),
                "incorrect_stops_cumulative": self.incorrect,
            })


def experiment(seed, checkpoint):
    training = MaskedC02Env("train")
    validation = MaskedC02Env("val_internal")
    model = MaskablePPO("MlpPolicy", training, seed=seed, **PPO_SETTINGS)
    callback = RolloutSummary()
    start = perf_counter()
    model.learn(total_timesteps=TRIAL_STEPS, callback=callback)
    elapsed = perf_counter() - start
    if model.num_timesteps != TRIAL_STEPS or callback.actions != TRIAL_STEPS:
        raise ValueError("unexpected count of training actions")
    model.save(checkpoint)
    loaded = MaskablePPO.load(checkpoint, device="cpu")
    val = evaluate(validation, lambda obs, mask: int(
        loaded.predict(obs, action_masks=mask, deterministic=True)[0]))
    return {
        "mode": "development_preview", "production_enabled": False,
        "test_internal_evaluated": False, "seed": seed, "steps": model.num_timesteps,
        "training_seconds": elapsed, "settings": PPO_SETTINGS, "model": receipt(checkpoint),
        "train_fixture_sha256": fingerprint(training.rows), "val_fixture_sha256": fingerprint(validation.rows),
        "training_curve": callback.curve, "val_policy": val,
        "val_tools_first": evaluate(validation, fixed_policy(SLOTS)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, type=int, choices=(1, 2))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to(ROOT / "outputs"):
        parser.error("output directory must be under outputs/")
    output.mkdir(parents=True, exist_ok=True)
    report = output / f"validation-seed{args.seed}.json"
    checkpoint = output / f"model-seed{args.seed}.zip"
    if report.exists() or checkpoint.exists():
        parser.error("use fresh run files")
    result = experiment(args.seed, checkpoint)
    with report.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({"seed": args.seed, "steps": result["steps"],
                      "validation_correct": result["val_policy"]["correct_terminal_rate"],
                      "validation_mean_questions": result["val_policy"]["mean_questions"]}))


if __name__ == "__main__":
    main()
