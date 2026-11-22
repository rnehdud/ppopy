"""Explicit prepare/train/evaluate commands for the synthetic v1 PPO connection."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform

import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
import torch

from .baselines import describe_episodes
from .environment import StaticAFAEnv
from .stage0 import DEFAULT, EXPERIMENT, ROOT, require
from .stage1 import BUNDLE
from .validation import RawReference

CONFIG = DEFAULT.parent.parent / "stage5a-v1/config.json"
PACKAGES = ("torch", "stable-baselines3", "sb3-contrib", "gymnasium", "numpy")


def read_config(path=CONFIG):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    require(config["mode"] == "development_preview" and config["production_enabled"] is False,
            "inactive preview required")
    require(config["fit_split"] == "train" and config["evaluation"] == {
        "split": "train", "deterministic": True, "test_scoring": False}, "train-only connection protocol")
    require(config["device"] == "cpu" and config["policy"] == "MlpPolicy", "CPU MlpPolicy connection only")
    require(config["gamma"] == 1 and config["shaping_beta"] == 0, "fixed total-cost objective")
    require(config["human_review"] == "unreviewed" and config["approved_reference"] is False,
            "reference approval boundary")
    for field in ("n_steps", "batch_size", "n_epochs", "total_timesteps", "torch_threads"):
        require(type(config[field]) is int and config[field] > 0, "positive integer " + field)
    require(config["batch_size"] > 1 and config["n_steps"] % config["batch_size"] == 0,
            "batch must divide one-environment rollout")
    require(config["total_timesteps"] % config["n_steps"] == 0, "whole rollout budget required")
    require(type(config["seed"]) is int and 0 <= config["seed"] < 2**32, "valid fixed seed required")
    require(np.isfinite(config["learning_rate"]) and config["learning_rate"] > 0, "finite learning rate")
    require(0 <= config["gae_lambda"] <= 1 and 0 < config["clip_range"] < 1 and
            np.isfinite(config["ent_coef"]) and config["ent_coef"] >= 0, "invalid PPO parameters")
    require(set(config["net_arch"]) == {"pi", "vf"} and all(
        layers and all(type(n) is int and n > 0 for n in layers) for layers in config["net_arch"].values()),
        "positive actor/critic layer sizes required")
    return config


def versions():
    return {"python": platform.python_version(), "platform": platform.system(),
            **{name: version(name) for name in PACKAGES}}


def input_hashes():
    paths = [DEFAULT, BUNDLE / "manifest.json", BUNDLE / "train.jsonl", EXPERIMENT / "pyproject.toml",
             EXPERIMENT / "uv.lock"]
    paths += [Path(__file__).with_name(name) for name in
              ("ppo.py", "environment.py", "runtime.py", "stage0.py", "stage1.py", "validation.py", "baselines.py")]
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def output_path(path):
    path = Path(path).resolve()
    require(ROOT / "outputs" in path.parents, "artifacts must be inside root outputs/")
    return path


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def create_model(config):
    torch.set_num_threads(config["torch_threads"])
    env = Monitor(StaticAFAEnv(config["fit_split"]))
    model = MaskablePPO(config["policy"], env, seed=config["seed"], device=config["device"],
                        policy_kwargs={"net_arch": deepcopy(config["net_arch"])},
                        **{key: config[key] for key in ("gamma", "learning_rate", "n_steps", "batch_size",
                                                       "n_epochs", "gae_lambda", "ent_coef", "clip_range")})
    return model


class MaskAuditCallback(BaseCallback):
    """Audit masks used by the actual SB3 collector; invalid actions also hard-fail in env."""
    def __init__(self):
        super().__init__()
        self.checked_actions = 0

    def _on_step(self):
        masks = np.asarray(self.locals["action_masks"], dtype=bool)
        actions = np.asarray(self.locals["actions"]).reshape(-1)
        require(masks.shape[0] == len(actions), "collector mask/action mismatch")
        require(all(masks[i, int(action)] for i, action in enumerate(actions)), "collector selected masked action")
        self.checked_actions += len(actions)
        return True


def evaluate_cohort(model, split, seed):
    """Full fixed cohort, no resampling; hidden references stay with evaluator."""
    require(split == "train", "Stage 5A scores train only; no validation selection or test scoring")
    env = StaticAFAEnv(split)
    reference = RawReference(env._contract)
    episodes = []
    try:
        for world_index, record in enumerate(env._records):
            observation, _ = env.reset(seed=seed, options={"world_index": world_index})
            require(env.dispatch_count == 0, "reset dispatched an action")
            visible, remaining = {}, env._contract["objective"]["max_questions"]
            total, questions, trace = 0.0, 0, []
            world = record["environment_only"]  # Evaluator-only; never passed to predict().
            for step in range(remaining + 1):
                mask = env.action_masks()
                action, _ = model.predict(observation.copy(), action_masks=mask.copy(), deterministic=True)
                index = int(np.asarray(action).item())
                require(0 <= index < len(mask) and mask[index], "evaluation selected masked action")
                expected = reference.transition(world, visible, remaining, index)
                observation, reward, done, truncated, info = env.step(index)
                require((reward, done, truncated) == (expected[2], expected[3], False), "evaluation transition mismatch")
                require(info["dispatch_count"] == step + 1, "step must dispatch exactly once")
                require(np.isfinite(reward) and np.isfinite(observation).all(), "non-finite transition")
                action_kind, target = reference.pairs[index]
                questions += int(action_kind == "ask_user")
                total += reward
                trace.append({"action": action_kind, "target": target, "reward": reward})
                visible, remaining = expected[0], expected[1]
                if done:
                    full = reference.evaluate(world["card_id"], {k: v["value"] for k, v in world["response_table"].items()})
                    episodes.append({"world_fingerprint": record["world_fingerprint"], "card": world["card_id"],
                                     "questions": questions, "cost": questions * env._contract["objective"]["ask_cost"],
                                     "return": total, "terminal": action_kind, "correct_terminal": bool(expected[5]),
                                     "semantic_match": reference.evaluate(world["card_id"], visible)["semantic"] == full["semantic"],
                                     "policy_fallbacks": 0, "trace": trace})
                    break
            else:
                raise ValueError("episode exceeded fixed acquisition/terminal bound")
        return {"split": split, "seed": seed, "deterministic": True,
                "scope": "tiny train diagnostic; not generalization or efficiency evidence",
                "summary": describe_episodes(episodes), "episodes": episodes}
    finally:
        env.close()


def save_checkpoint(model, directory, config, filename):
    checkpoint = directory / filename
    model.save(checkpoint)
    write_json(directory / "checkpoint.json", {"mode": "development_preview", "production_enabled": False,
               "config": config, "versions": versions(), "source_hashes": input_hashes(),
               "checkpoint": filename, "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
               "num_timesteps": model.num_timesteps, "learning_executed": model.num_timesteps > 0})
    return checkpoint


def load_checkpoint(directory):
    directory = output_path(directory)
    manifest = json.loads((directory / "checkpoint.json").read_text(encoding="utf-8"))
    require(manifest["mode"] == "development_preview" and manifest["production_enabled"] is False,
            "inactive checkpoint required")
    require(manifest["checkpoint"] in {"initialized_model.zip", "model.zip"}, "unknown checkpoint artifact")
    require(manifest["source_hashes"] == input_hashes(), "checkpoint input/code drift")
    require(manifest["versions"] == versions(), "checkpoint environment drift")
    require(manifest["config"] == read_config(directory / "config.json"), "checkpoint config drift")
    path = directory / manifest["checkpoint"]
    require(hashlib.sha256(path.read_bytes()).hexdigest() == manifest["checkpoint_sha256"], "checkpoint bytes drift")
    torch.set_num_threads(manifest["config"]["torch_threads"])
    model = MaskablePPO.load(path, device="cpu")
    require(model.num_timesteps == manifest["num_timesteps"], "checkpoint step count drift")
    return model, manifest


def run(command, run_dir, config_path=CONFIG):
    require(command in {"prepare", "train", "evaluate"}, "unknown command")
    directory = output_path(run_dir)
    if command == "evaluate":
        model, manifest = load_checkpoint(directory)
        result = evaluate_cohort(model, "train", manifest["config"]["seed"])
        print(json.dumps(result["summary"]))
        return result
    config = read_config(config_path)
    # Fail rather than replacing an earlier run or tuning it in place.
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / "config.json", config)
    model = create_model(config)
    callback = MaskAuditCallback()
    try:
        if command == "train":
            model.set_logger(configure(str(directory / "logs"), ["csv"]))
            model.learn(total_timesteps=config["total_timesteps"], callback=callback, use_masking=True)
            require(model.num_timesteps == callback.checked_actions == config["total_timesteps"], "rollout budget mismatch")
        require(all(torch.isfinite(p).all().item() for p in model.policy.parameters()), "non-finite policy weights")
        checkpoint = save_checkpoint(model, directory, config,
                                     "initialized_model.zip" if command == "prepare" else "model.zip")
        reloaded, _ = load_checkpoint(directory)
        before = evaluate_cohort(model, "train", config["seed"])
        after = evaluate_cohort(reloaded, "train", config["seed"])
        require(before == after, "save/reload changed deterministic masked execution")
        # Also exercise the official mask-aware evaluator, never SB3's unmasked one.
        eval_env = Monitor(StaticAFAEnv("train"))
        try:
            eval_env.reset(seed=config["seed"])
            rewards, lengths = evaluate_policy(reloaded, eval_env, n_eval_episodes=2,
                                               deterministic=True, return_episode_rewards=True, warn=False)
        finally:
            eval_env.close()
        result = {"mode": "development_preview", "production_enabled": False, "command": command,
                  "learning_executed": command == "train", "num_timesteps": model.num_timesteps,
                  "collector_mask_checks": callback.checked_actions,
                  "checkpoint": checkpoint.name, "save_reload_equivalent": True,
                  "official_masked_evaluator": {"rewards": rewards, "lengths": lengths},
                  "evaluation": after, "efficiency_claim": False, "independent_evaluation": False}
        write_json(directory / "report.json", result)
        print(json.dumps({k: v for k, v in result.items() if k != "evaluation"}))
        return result
    finally:
        model.get_env().close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "train", "evaluate"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=CONFIG)
    args = parser.parse_args()
    run(args.command, args.run_dir, args.config)


if __name__ == "__main__":
    main()
