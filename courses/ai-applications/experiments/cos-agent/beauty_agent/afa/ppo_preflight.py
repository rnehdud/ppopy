"""Family-separated C02 experiment, with a preflight before PPO learning."""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
from itertools import product
import json
from pathlib import Path
from statistics import mean

import gymnasium as gym
import numpy as np
from sb3_contrib import MaskablePPO

from beauty_agent.actions import ActionProposal
from beauty_agent.modules.kb_adapter import KBEngineAdapter

from .eda import ROOT, fingerprint
from .v67_fixtures import SLOTS, ResponseBook, compile_book, require, slot
from .v67_reward import RewardProtocol, observed_signature, score_stop
from .v67_runtime import ACTIONS, FixtureSession

TOOLS = ("hands", "scrub_brush", "unknown", "declined")
FRICTION = ("gentle", "strong", "unknown", "declined")
DRYING = ("pat_gently", "rubbing_strongly", "unknown", "declined")
SPLITS = ("train", "val_internal", "test_internal")
ALLOCATIONS = {
    # Previously inspected E22 families and the E24 priority probe stay in train.
    "hands": ("train", "val_internal", "test_internal", "train"),
    "scrub_brush": ("train", "train", "val_internal", "test_internal"),
    "unknown": ("train", "train", "test_internal", "val_internal"),
    "declined": ("val_internal", "test_internal", "train", "train"),
}
PROTOCOL = RewardProtocol()
PPO_SETTINGS = dict(n_steps=64, batch_size=32, n_epochs=4, gamma=1.0,
                    learning_rate=0.0003, device="cpu", policy_kwargs=dict(net_arch=[32, 32]))
TRIAL_STEPS = 4096


def response(slot_id, value):
    return slot(slot_id, value, None) if value in {"unknown", "declined"} else slot(slot_id, "known", value)


def dataset():
    """Balance four tools strata before observing a reward or baseline score."""
    splits = {split: [] for split in SPLITS}
    for tool in TOOLS:
        for friction_index, friction in enumerate(FRICTION):
            split = ALLOCATIONS[tool][friction_index]
            family = f"{tool}:{friction}"
            for drying in DRYING:
                values = (tool, friction, drying)
                fixture = {
                    "fixture_id": f"e26:{family}:{drying}",
                    # The E22 response book requires the legacy development-record flag.
                    # The outer allocation, not this flag, governs actual split membership.
                    "split": "train", "production_enabled": False,
                    "training_ready": False, "approved_reference": False,
                    "initial_public": {"message": "합성 세안 상황입니다.", "history": [],
                                       "observations": {"method.body_site": slot("method.body_site", "known", "face")}},
                    "environment_only": {"stationarity_assumed": True, "question_slots": list(SLOTS),
                                         "response_table": {key: response(key, value)
                                                            for key, value in zip(SLOTS, values)}},
                }
                splits[split].append({"family": family, "split": split, "fixture": fixture})
    families = [{r["family"] for r in splits[s]} for s in SPLITS]
    require(sum(map(len, families)) == len(set.union(*families)), "cross-split family overlap")
    fingerprints = [fingerprint(r["fixture"]["environment_only"]["response_table"])
                    for rows in splits.values() for r in rows]
    require(len(set(fingerprints)) == len(fingerprints), "duplicate response worlds")
    return splits


def verify_development_overlap(splits):
    from .v67_runtime import load_response_book

    old_book, ids, _ = load_response_book()
    prior_families = {"scrub_brush:strong"}  # Separately authored E24 probe.
    for fixture_id in ids:
        public = old_book.initial_public(fixture_id)
        for key in SLOTS[:2]:
            public = old_book.answer(fixture_id, public, key)
        states = [public["observations"][key] for key in SLOTS[:2]]
        prior_families.add(":".join(row["value"] if row["state"] == "known" else row["state"]
                                    for row in states))
    train_families = {row["family"] for row in splits["train"]}
    require(prior_families <= train_families, "previously inspected family outside train")
    return sorted(prior_families)


def make_book(rows):
    fixtures = [r["fixture"] for r in rows]
    transitions, _ = compile_book(fixtures)
    return ResponseBook(fixtures, transitions)


def encode(context):
    observations = context.observations
    vector = []
    for key, domain in zip(SLOTS, (TOOLS, FRICTION, DRYING)):
        observation = observations.get(key)
        value = ("not_asked" if observation is None else
                 observation.value if observation.state == "known" else observation.state)
        require(value in (*domain, "not_asked"), "observation outside declared domain")
        vector.extend(float(value == option) for option in ("not_asked", *domain))
    return np.asarray(vector, dtype=np.float32)


def reference(book, fixture_id, adapter):
    public = book.initial_public(fixture_id)
    for key in SLOTS:
        public = book.answer(fixture_id, public, key)
    return observed_signature(adapter, public)


class MaskedC02Env(gym.Env):
    def __init__(self, split):
        self.rows = dataset()[split]
        self.book = make_book(self.rows)
        self.adapter = KBEngineAdapter()
        self.references = {r["fixture"]["fixture_id"]: reference(
            self.book, r["fixture"]["fixture_id"], self.adapter) for r in self.rows}
        self.action_space = gym.spaces.Discrete(len(ACTIONS))
        self.observation_space = gym.spaces.Box(0.0, 1.0, shape=(15,), dtype=np.float32)
        self.session = None
        self.finished = True

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        index = options["index"] if options and "index" in options else int(self.np_random.integers(len(self.rows)))
        require(type(index) is int and 0 <= index < len(self.rows), "invalid fixture index")
        self.fixture_id = self.rows[index]["fixture"]["fixture_id"]
        self.session = FixtureSession(self.book, self.fixture_id)
        self.finished = False
        self.questions = 0
        return encode(self.session.prepare_context().context), {}

    def action_masks(self):
        if self.finished:
            return np.zeros(len(ACTIONS), dtype=bool)
        return np.asarray(self.session.prepare_context().mask, dtype=bool)

    def step(self, action):
        require(self.action_space.contains(action) and self.action_masks()[action], "masked action")
        prepared = self.session.prepare_context()
        kind, target = ACTIONS[action]
        _, _, disposition = asyncio.run(self.session.apply_action(
            prepared, ActionProposal(action=kind, target_id=target)))
        if disposition is None:
            self.questions += 1
            return encode(self.session.prepare_context().context), -PROTOCOL.question_cost, False, False, {}
        self.finished = True
        same = self.references[self.fixture_id] == observed_signature(self.adapter, self.session.public)
        score = score_stop(disposition, same, self.questions, PROTOCOL)
        return encode(prepared.context), -score["terminal_loss"], True, False, {
            "correct_terminal": score["correct_terminal"], "reason": score["reason"], "questions": self.questions,
        }


def evaluate(env, select):
    results = []
    for i in range(len(env.rows)):
        obs, _ = env.reset(seed=0, options={"index": i})
        total = 0
        for _ in range(len(SLOTS) + 1):
            obs, reward, terminated, truncated, info = env.step(select(obs, env.action_masks()))
            total += reward
            require(not truncated, "unexpected truncation")
            if terminated:
                results.append({**info, "return": total, "family": env.rows[i]["family"]})
                break
        else:
            raise ValueError("episode did not terminate")
    return {"episodes": len(results), "mean_questions": mean(r["questions"] for r in results),
            "correct_terminal_rate": mean(r["correct_terminal"] for r in results),
            "mean_return": mean(r["return"] for r in results),
            "reasons": dict(Counter(r["reason"] for r in results)), "cases": results}


def fixed_policy(order):
    pairs = [("ask_user", key) for key in order] + [
        ("request_draft", "label_draft"), ("hold", "safety"), ("hold", "insufficient_information")]
    indices = [ACTIONS.index(pair) for pair in pairs]
    return lambda obs, mask: next(i for i in indices if mask[i])


def audit_paths(env):
    """Replay each reachable masked path and validate mechanical scoring."""
    questions = []
    terminals = Counter()
    for i in range(len(env.rows)):
        valid_question_counts = []
        pending = [()]
        while pending:
            path = pending.pop()
            obs, _ = env.reset(options={"index": i})
            for action in path:
                obs, reward, done, truncated, _ = env.step(action)
                require(reward == -PROTOCOL.question_cost and not done and not truncated,
                        "invalid question transition")
            require(env.observation_space.contains(obs) and env.action_masks().any(),
                    "invalid reachable context")
            for action in np.flatnonzero(env.action_masks()).tolist():
                if ACTIONS[action][0] == "ask_user":
                    require(len(path) < len(SLOTS) and action not in path, "repeated or unbounded question")
                    pending.append((*path, action))
                    continue
                env.reset(options={"index": i})
                for prefix in path:
                    env.step(prefix)
                _, reward, done, truncated, info = env.step(action)
                require(done and not truncated and info["questions"] == len(path) and
                        reward == (0 if info["correct_terminal"] else -PROTOCOL.incorrect_stop_loss),
                        "terminal scoring drift")
                terminals[info["reason"]] += 1
                if info["correct_terminal"]:
                    valid_question_counts.append(len(path))
        require(valid_question_counts, "fixture has no correct reachable stop")
        questions.append(min(valid_question_counts))
    return {"worlds_with_valid_stop": len(questions), "terminal_paths": sum(terminals.values()),
            "reasons": dict(terminals), "mean_min_questions_with_fixture_known": mean(questions)}


def preflight(seed):
    prior_families = verify_development_overlap(dataset())
    envs = {split: MaskedC02Env(split) for split in SPLITS}
    policy_orders = {"runtime_question_order": tuple(sorted(SLOTS)), "tools_first": SLOTS,
                     "friction_first": (SLOTS[1], SLOTS[0], SLOTS[2])}
    baselines = {split: {name: evaluate(env, fixed_policy(order))
                         for name, order in policy_orders.items()}
                 for split, env in envs.items()}
    paths = {split: audit_paths(env) for split, env in envs.items()}
    train = envs["train"]
    model = MaskablePPO("MlpPolicy", train, seed=seed, **PPO_SETTINGS)
    obs, info = train.reset(seed=seed)
    mask = train.action_masks()
    action, _ = model.predict(obs, action_masks=mask, deterministic=True)
    require(not info and mask[int(action)] and model.num_timesteps == 0, "invalid PPO initialization")
    return {"entry": "E26", "mode": "development_preview", "production_enabled": False,
            "human_review": "unreviewed", "independent_evaluation": False,
            "source": "new authored C02 factorial fixture grid; separate from v67 and the 48-world bundle",
            "seed": seed, "action_catalog": ACTIONS, "observation_shape": [15],
            "dataset_fingerprint": fingerprint(dataset()), "settings": PPO_SETTINGS,
            "previously_inspected_families_kept_in_train": prior_families,
            "families": {split: sorted({r["family"] for r in env.rows}) for split, env in envs.items()},
            "baseline": baselines, "path_audit": paths, "ppo_num_timesteps": model.num_timesteps,
            "trial_steps": TRIAL_STEPS, "reward": {"question_cost": PROTOCOL.question_cost,
                "incorrect_stop_loss": PROTOCOL.incorrect_stop_loss, "shaping_beta": 0},
            "initial_mask": mask.tolist(), "initial_action": int(action)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=lambda s: (ROOT / s).resolve(), required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=0)
    parser.add_argument("--model", type=lambda s: (ROOT / s).resolve())
    args = parser.parse_args()
    require(args.report.is_relative_to(ROOT / "outputs") and not args.report.exists(), "new outputs report required")
    require(args.train_steps >= 0, "negative training steps")
    require(not args.train_steps or (args.train_steps % PPO_SETTINGS["n_steps"] == 0 and args.model is not None
            and args.model.suffix == ".zip" and args.model.is_relative_to(ROOT / "outputs")
            and not args.model.exists()), "training requires rollout multiples and a new outputs .zip")
    report = preflight(args.seed)
    if args.train_steps:
        train = MaskedC02Env("train")
        model = MaskablePPO("MlpPolicy", train, seed=args.seed, **PPO_SETTINGS)
        model.learn(total_timesteps=args.train_steps)
        report["ppo_num_timesteps"] = model.num_timesteps
        report["ppo"] = {split: evaluate(MaskedC02Env(split),
            lambda obs, mask: int(model.predict(obs, action_masks=mask, deterministic=True)[0]))
                         for split in ("train", "val_internal")}
        args.model.parent.mkdir(parents=True, exist_ok=True)
        model.save(args.model)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    print(json.dumps({"ppo_num_timesteps": report["ppo_num_timesteps"],
                      "families": {s: len(f) for s, f in report["families"].items()}}))


if __name__ == "__main__":
    main()
