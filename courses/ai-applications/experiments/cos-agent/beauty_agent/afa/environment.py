"""Gymnasium environment for the response-complete static Stage 0/1 task only."""
from __future__ import annotations

import argparse
import asyncio
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from beauty_agent.actions import ActionProposal
from .runtime import StaticSessionAdapter
from .stage0 import DEFAULT, ROOT, audit, require, signature, task_offers
from .stage1 import BUNDLE, SPLITS, world_key


def load_split(split, bundle=BUNDLE, contract_path=DEFAULT):
    """Validate selected data without loading another split's hidden responses."""
    require(split in SPLITS, "unknown split")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    report = audit(contract)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    require(manifest["mode"] == "development_preview" and manifest["production_enabled"] is False,
            "inactive bundle required")
    require(manifest["contract_sha256"] == hashlib.sha256(contract_path.read_bytes()).hexdigest(),
            "contract drift")
    for key, filename in [("generator_sha256", "stage1.py"), ("stage0_checker_sha256", "stage0.py")]:
        require(manifest[key] == hashlib.sha256(Path(__file__).with_name(filename).read_bytes()).hexdigest(),
                "bundle generator/checker drift")
    raw = (bundle / (split + ".jsonl")).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == manifest["files"][split + ".jsonl"]["sha256"],
            "split bytes drift")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    require(len(rows) == manifest["split_counts"][split] and rows, "split count mismatch")
    worlds = {world_key(w["card"], w["hidden_synthetic_answers"]): w
              for w in report["worlds"] if w["eligible"]}
    for row in rows:
        require(row["split"] == split and row["initial_visible_observations"] == {}, "split/public input drift")
        hidden = row["environment_only"]
        key = world_key(hidden["card_id"], {k: s["value"] for k, s in hidden["response_table"].items()})
        expected = worlds.get(key)
        require(expected is not None and row["world_fingerprint"] == key and
                hidden["reference"] == expected["reference"] and
                hidden["reference_terminal"] == expected["reference_terminal"], "unsupported world/reference")
    return contract, rows


class StaticAFAEnv(gym.Env):
    """Strict masked actions: invalid actions raise without committing a transition."""
    metadata = {"render_modes": []}

    def __init__(self, split="train", *, bundle=BUNDLE, contract_path=DEFAULT):
        self._contract, self._records = load_split(split, bundle, contract_path)
        self._pairs = [tuple(p) for p in self._contract["action_dictionary"]]
        self.action_space = spaces.Discrete(len(self._pairs))
        high = np.ones(self._contract["observation_schema"]["dimension"], dtype=np.float32)
        high[-1] = self._contract["objective"]["max_questions"]
        self.observation_space = spaces.Box(np.zeros_like(high), high, dtype=np.float32)
        self._runtime = self._prepared = self._world = None
        self._remaining = self._contract["objective"]["max_questions"]
        self._done = True
        self._stepping = False

    @property
    def visible_observations(self):
        require(self._prepared is not None, "reset required")
        return {k: v.model_dump() for k, v in self._prepared.state.confirmed_observations.items()}

    @property
    def dispatch_count(self):
        return 0 if self._runtime is None else self._runtime.dispatch_count

    def _mask(self, prepared, remaining, done=False):
        if done:
            return np.zeros(len(self._pairs), dtype=bool)
        valid = {(a.action, a.target_id) for a in task_offers(self._contract, prepared.context)}
        return np.array([p in valid and (p[0] != "ask_user" or remaining > 0)
                         for p in self._pairs], dtype=bool)

    def action_masks(self):
        require(self._prepared is not None, "reset required")
        return self._mask(self._prepared, self._remaining, self._done)

    def _encode(self, prepared, remaining, done=False):
        schema = self._contract["observation_schema"]
        observations = prepared.state.confirmed_observations
        vector = []
        for key in schema["slot_order"]:
            state = observations[key].state if key in observations else "not_asked"
            vector.extend(float(state == s) for s in schema["state_order"])
        for key in schema["slot_order"]:
            value = observations[key].value if key in observations and observations[key].state == "known" else None
            require(value in schema["value_order"][key], "unencodable value")
            vector.extend(float(value == v) for v in schema["value_order"][key])
        vector.extend(float(self._runtime_card(prepared) == c) for c in self._contract["tasks"])
        vector.extend(self._mask(prepared, remaining, done).astype(float))
        vector.append(float(remaining))
        observation = np.asarray(vector, dtype=np.float32)
        require(self.observation_space.contains(observation), "observation schema violation")
        return observation

    @staticmethod
    def _runtime_card(prepared):
        return prepared.evaluated["raw"]["results"][0]["card_id"]

    def reset(self, *, seed=None, options=None):
        require(not self._stepping, "cannot reset during a step")
        super().reset(seed=seed)
        options = options or {}
        require(set(options) <= {"world_index"}, "unsupported reset option")
        # Explicit diagnostic selection must not consume the random world's stream.
        index = options["world_index"] if "world_index" in options else int(self.np_random.integers(len(self._records)))
        require(isinstance(index, (int, np.integer)) and not isinstance(index, bool) and
                0 <= index < len(self._records), "invalid world index")
        world = deepcopy(self._records[int(index)]["environment_only"])
        runtime = StaticSessionAdapter(self._contract, world["card_id"])
        prepared = runtime.prepare_context()
        remaining = self._contract["objective"]["max_questions"]
        observation = self._encode(prepared, remaining)
        self._runtime, self._prepared, self._world = runtime, prepared, world
        self._remaining, self._done = remaining, False
        return observation, {"dispatch_count": 0}

    def _answer(self, target):
        require(target in self._world["response_table"], "undefined response; no transition committed")
        return deepcopy(self._world["response_table"][target])

    def step(self, action):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.astep(action))
        raise RuntimeError("use await env.astep(action) inside an existing event loop")

    async def astep(self, action):
        require(not self._stepping, "concurrent step rejected")
        self._stepping = True
        try:
            return await self._step_transaction(action)
        finally:
            self._stepping = False

    async def _step_transaction(self, action):
        require(self._prepared is not None and not self._done, "reset required after termination")
        require(isinstance(action, (int, np.integer)) and not isinstance(action, bool) and
                self.action_space.contains(action), "invalid action index")
        index = int(action)
        require(self.action_masks()[index], "masked action; no transition committed")
        action_kind, target = self._pairs[index]
        context = self._prepared.context
        offer = next(a for a in task_offers(self._contract, context)
                     if (a.action, a.target_id) == (action_kind, target))
        proposal = ActionProposal(action=action_kind, target_id=target, evidence_refs=offer.evidence_refs)
        # Work on a private fork: response/preparation/encoding errors roll back the whole env step.
        working = self._runtime.fork()
        _, decision, outcome = await working.apply_action(self._prepared, proposal)
        reward = 0.0
        remaining = self._remaining
        terminated = action_kind != "ask_user"
        if not terminated:
            reward -= self._contract["objective"]["ask_cost"]
            remaining -= 1
            next_prepared = working.prepare_context({target: self._answer(target)})
            ask_remains = any(a.action == "ask_user" for a in task_offers(self._contract, next_prepared.context))
            if remaining == 0 and ask_remains:
                terminated = True
                reward -= self._contract["objective"]["task_budget_exhausted_loss"]
                outcome = "task_budget_exhausted"
        else:
            exact = signature(self._prepared.evaluated) == self._world["reference"]
            correct = exact and action_kind == self._world["reference_terminal"] and (
                action_kind == "request_draft" or not any(a.action == "ask_user"
                    for a in task_offers(self._contract, context)))
            reward -= self._contract["objective"]["correct_terminal_loss" if correct else "incorrect_terminal_loss"]
            next_prepared = working.prepare_context()
        observation = self._encode(next_prepared, remaining, terminated)
        self._runtime, self._prepared = working, next_prepared
        self._remaining, self._done = remaining, terminated
        # No hidden world ID, reference, future answer or full response table in the policy-facing result.
        info = {"applied_action": [decision.applied.action, decision.applied.target_id],
                "execution_status": outcome, "dispatch_count": working.dispatch_count}
        return observation, float(reward), bool(terminated), False, info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    env = StaticAFAEnv()
    observation, _ = env.reset(seed=0, options={"world_index": 0})
    trace = []
    while True:
        mask = env.action_masks()
        # Scripted engineering smoke only: first allowed question, otherwise draft, otherwise hold.
        enabled = [i for i, allowed in enumerate(mask) if allowed]
        action = min(enabled, key=lambda i: {"ask_user": 0, "request_draft": 1, "hold": 2}[env._pairs[i][0]])
        observation, reward, done, truncated, info = env.step(action)
        trace.append({**info, "reward": reward, "terminated": done, "truncated": truncated,
                      "visible_slot_ids": list(env.visible_observations)})
        if done:
            break
    report = {"mode": "development_preview", "production_enabled": False, "observation_dimension": len(observation),
              "scope": "Stage 2 train-split scripted API smoke; no trained policy or performance evaluation", "trace": trace}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"dimension": len(observation), "dispatches": env.dispatch_count,
                      "terminated": done, "return": sum(t["reward"] for t in trace)}))


if __name__ == "__main__":
    main()
