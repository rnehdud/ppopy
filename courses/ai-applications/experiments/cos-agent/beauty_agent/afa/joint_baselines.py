"""Train-only public-input joint-task baselines and evaluator-only headroom."""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from .baselines import RulePolicy, RandomPolicy, describe_episodes
from .joint_data import BUNDLE, load_joint_split
from .joint_environment import JointAFAEnv
from .joint_runtime import JointSessionAdapter
from .semantics import SemanticInspector, event
from .stage0 import DEFAULT, ROOT, require, signature
from .stage1 import encode

PROTOCOL = DEFAULT.parent.parent / "joint-baselines-v1/protocol.json"


def public_input(base, observation, mask):
    require(observation.shape == (64,) and mask.shape == (8,) and np.isfinite(observation).all(), "joint public input schema")
    visible, offset = {}, 0
    states = {}
    schema = base["observation_schema"]
    for slot in schema["slot_order"]:
        values = observation[offset:offset + len(schema["state_order"])]
        require(set(values) <= {0, 1} and values.sum() == 1, "invalid public state one-hot")
        states[slot] = schema["state_order"][int(values.argmax())]
        offset += len(values)
    for slot in schema["slot_order"]:
        choices = schema["value_order"][slot]
        values = observation[offset:offset + len(choices)]
        require(set(values) <= {0, 1} and values.sum() == 1, "invalid public value one-hot")
        value = choices[int(values.argmax())]
        if states[slot] == "known":
            require(value is not None, "known null public answer")
            visible[slot] = value
        else:
            require(value is None, "nonanswer must stay null")
        offset += len(choices)
    require(np.array_equal(observation[47:49], [1, 1]) and np.array_equal(observation[49:57], mask), "public task/mask mismatch")
    costs = dict(zip(schema["slot_order"], observation[58:63].tolist()))
    require(all(value in (1, 2) for value in costs.values()), "unsupported public costs")
    require(observation[57] == int(observation[57]) and 0 <= observation[57] <= 5 and
            observation[63] == int(observation[63]) and 0 <= observation[63] <= 7, "invalid public budgets")
    return visible, {k: int(v) for k, v in costs.items()}, states


class _PlanningCore:
    """Finite planning model. It never receives the actual evaluation-world ID."""
    def __init__(self, worlds):
        require(bool(worlds), "nonempty response support required")
        self.worlds = deepcopy(worlds)
        self.inspector = SemanticInspector()
        self._states, self._solutions, self._hindsight = {}, {}, {}

    def state(self, visible):
        key = encode(visible)
        if key not in self._states:
            ledger = self.inspector.ledger([event(slot, slot, value) for slot, value in visible.items()])
            self._states[key] = self.inspector.inspect(["B-C01", "B-C02"], ledger)
        return self._states[key]

    def matching(self, visible):
        return [w for w in self.worlds if all(w[k] == value for k, value in visible.items())]

    def solve(self, visible, costs):
        key = encode([visible, costs])
        if key in self._solutions:
            return self._solutions[key]
        worlds = self.matching(visible)
        require(worlds, "planning state outside response support")
        questions = self.state(visible)["research_question_requirements"]
        if not questions:
            result = Fraction(0), None
        else:
            options = []
            for slot in questions:
                answers = defaultdict(int)
                for world in worlds:
                    answers[world[slot]] += 1
                expected = Fraction(costs[slot])
                for answer, count in sorted(answers.items()):
                    expected += Fraction(count, len(worlds)) * self.solve({**visible, slot: answer}, costs)[0]
                options.append((expected, slot))
            result = min(options)
        self._solutions[key] = result
        return result

    def hindsight(self, world, costs, visible=None):
        visible = {} if visible is None else visible
        key = encode([world, costs, visible])
        if key not in self._hindsight:
            questions = self.state(visible)["research_question_requirements"]
            self._hindsight[key] = min((costs[slot] + self.hindsight(world, costs, {**visible, slot: world[slot]})
                                       for slot in questions), default=0)
        return self._hindsight[key]


class TrainModel(_PlanningCore):
    def __init__(self, records):
        require(records and all(row["split"] == "train" for row in records), "baseline fit must be train-only")
        super().__init__([{key: slot["value"] for key, slot in row["environment_only"]["response_table"].items()} for row in records])
        self.fit_roots = [row["root_world_id"] for row in records]


class JointRule(RulePolicy):
    """Reconstruct native offer order using public input only, including v2 extensions."""
    def __init__(self, base):
        super().__init__(base)
        self._inspector = SemanticInspector()
        self._orders = {}

    def select(self, observation, mask):
        visible, _, states = public_input(self.contract, observation, mask)
        key = encode([visible, states])
        if key not in self._orders:
            runtime = JointSessionAdapter(self._inspector)
            prepared = runtime.prepare_context([event(slot, slot, visible.get(slot), state)
                                               for slot, state in states.items() if state != "not_asked"])
            priority = {"ask_user": 0, "request_draft": 1, "hold": 2}
            offers = [a for a in prepared.context.enabled() if (a.action, a.target_id) in self.pairs]
            ordered = sorted(offers, key=lambda a: priority[a.action])  # stable sort preserves native tie order
            self._orders[key] = [(a.action, a.target_id) for a in ordered]
        allowed = {self.pairs[int(i)] for i in np.flatnonzero(mask)}
        pair = next((pair for pair in self._orders[key] if pair in allowed), None)
        require(pair is not None, "native public offer order disagrees with mask")
        return self.pairs.index(pair)


class JointGreedy(JointRule):
    name = "joint_train_greedy"

    def __init__(self, base, model):
        super().__init__(base)
        require(isinstance(model, TrainModel), "train-fitted model required")
        self.model = model

    def select(self, observation, mask):
        visible, costs, states = public_input(self.contract, observation, mask)
        asks = [int(i) for i in np.flatnonzero(mask) if self.pairs[i][0] == "ask_user"]
        if not asks:
            return super().select(observation, mask)
        worlds = self.model.matching(visible)
        if not worlds or any(state not in {"known", "not_asked"} for state in states.values()):
            self.fallbacks += 1
            return super().select(observation, mask)
        gains = {}
        for index in asks:
            slot = self.pairs[index][1]
            finishes = sum(not self.model.state({**visible, slot: world[slot]})["research_question_requirements"] for world in worlds)
            gains[index] = Fraction(finishes * (sum(costs.values()) + 1), len(worlds) * costs[slot])
        return min(asks, key=lambda index: (-gains[index], costs[self.pairs[index][1]], self.pairs[index][1]))


class JointMultistep(JointGreedy):
    name = "joint_train_multistep"

    def select(self, observation, mask):
        visible, costs, states = public_input(self.contract, observation, mask)
        asks = [int(i) for i in np.flatnonzero(mask) if self.pairs[i][0] == "ask_user"]
        if not asks:
            return JointRule.select(self, observation, mask)
        if not self.model.matching(visible) or any(state not in {"known", "not_asked"} for state in states.values()):
            self.fallbacks += 1
            return JointRule.select(self, observation, mask)
        _, slot = self.model.solve(visible, costs)
        index = self.pairs.index(("ask_user", slot))
        require(index in asks, "planner disagrees with public runtime mask")
        return index


def evaluate_episode(env, index, policy, seed):
    observation, _ = env.reset(seed=seed, options={"world_index": index})
    record = env._records[index]  # Evaluator only; select() receives public copies.
    before = policy.fallbacks
    total, questions, acquisition_cost, trace = 0.0, 0, 0, []
    for _ in range(6):
        mask = env.action_masks()
        action = policy.select(observation.copy(), mask.copy())
        require(type(action) is int and 0 <= action < 8 and mask[action], "baseline selected invalid action")
        kind, target = env._pairs[action]
        if kind == "ask_user":
            questions += 1
            acquisition_cost += env._cost["ask_costs"][target]
        no_asks = not any(mask[i] and pair[0] == "ask_user" for i, pair in enumerate(env._pairs))
        match_before = signature(env._prepared.evaluated) == record["environment_only"]["reference"]
        observation, reward, done, truncated, info = env.step(action)
        require(not truncated and np.isfinite(reward) and info["dispatch_count"] == len(trace) + 1, "baseline transition error")
        total += reward
        trace.append({"action": kind, "target": target, "reward": reward})
        if done:
            correct = match_before and kind == record["environment_only"]["reference_terminal"] and (kind == "request_draft" or no_asks)
            require(total == -acquisition_cost - (0 if correct else env._cost["incorrect_terminal_loss"]), "return accounting mismatch")
            return {"world_fingerprint": record["root_world_id"], "family_id": record["family_id"], "seed": seed,
                    "policy": policy.name, "questions": questions, "cost": acquisition_cost, "return": total,
                    "terminal": kind, "correct_terminal": correct, "semantic_match": match_before,
                    "policy_fallbacks": policy.fallbacks - before, "trace": trace}
    raise ValueError("baseline exceeded fixed episode bound")


def diagnostic_bounds(records, costs):
    require(records and all(row["split"] in {"train", "val_internal"} for row in records), "headroom does not score test_internal")
    worlds = [{key: value["value"] for key, value in r["environment_only"]["response_table"].items()} for r in records]
    # Full split distribution is known here, separate from all train-fitted policies.
    core = _PlanningCore(worlds)
    return {"public_information_optimum": float(core.solve({}, costs)[0]),
            "hindsight_lower_bound": sum(core.hindsight(world, costs) for world in worlds) / len(worlds),
            "evaluator_only": True, "policy_training_use": False,
            "assumption": "uniform known diagnostic split distribution; fixed semantic/runtime stopping gates"}


def compare(seeds=(0, 1, 2), evaluation_splits=("train", "val_internal"), cost_protocols=("unit_primary", "weighted_sensitivity")):
    require(evaluation_splits and set(evaluation_splits) <= {"train", "val_internal"}, "baseline comparison does not score test_internal")
    require(seeds and len(set(seeds)) == len(seeds), "distinct fixed seeds required")
    require(all(type(seed) is int and 0 <= seed < 2**32 for seed in seeds), "valid integer seeds required")
    require(cost_protocols and set(cost_protocols) <= {"unit_primary", "weighted_sensitivity"}, "fixed cost protocols required")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    require(protocol["mode"] == "development_preview" and protocol["production_enabled"] is False and
            protocol["fit_split"] == "train" and protocol["test_scoring"] is False, "inactive train-only protocol required")
    training = load_joint_split("train")
    model = TrainModel(training)
    base = model.inspector.base
    summaries, episodes, headroom = [], [], []
    for cost in cost_protocols:
        for split in evaluation_splits:
            env = JointAFAEnv(split, cost)
            local = []
            for seed in seeds:
                policies = [JointRule(base), RandomPolicy(base, seed), RandomPolicy(base, seed, acquisition_only=True),
                            JointGreedy(base, model), JointMultistep(base, model)]
                for policy in policies:
                    for index in range(len(env._records)):
                        row = {"cost_protocol": cost, "split": split, **evaluate_episode(env, index, policy, seed)}
                        local.append(row)
            for name in sorted({row["policy"] for row in local}):
                selected = [row for row in local if row["policy"] == name]
                summaries.append({"cost_protocol": cost, "split": split, "policy": name, **describe_episodes(selected),
                                  "median_cost": float(np.median([r["cost"] for r in selected])),
                                  "p95_cost": float(np.percentile([r["cost"] for r in selected], 95)),
                                  "distinct_families": len({r["family_id"] for r in selected}),
                                  "per_seed": [{"seed": seed, **describe_episodes([r for r in selected if r["seed"] == seed])} for seed in seeds]})
            bounds = diagnostic_bounds(env._records, env._cost["ask_costs"])
            candidates = [row for row in summaries if row["cost_protocol"] == cost and row["split"] == split and
                          row["correct_terminal_rate"] == 1 and row["policy"] in {"existing_rule_order", "joint_train_greedy", "joint_train_multistep"}]
            best = min(candidates, key=lambda row: (row["mean_cost"], row["policy"]))
            gap = best["mean_cost"] - bounds["public_information_optimum"]
            require(gap >= -1e-9, "deterministic baseline beat the exact public-information bound")
            headroom.append({"cost_protocol": cost, "split": split, **bounds,
                             "strongest_deterministic_baseline": best["policy"], "baseline_cost": best["mean_cost"],
                             "gap_to_public_optimum": max(0.0, gap)})
            episodes.extend(local)
            print("compared " + cost + "/" + split, flush=True)
    return {"mode": "development_preview", "production_enabled": False, "protocol": protocol,
            "scope": "train/val internal baseline comparison; no test scoring, RL or hyperparameter search",
            "fit": {"split": "train", "worlds": len(training), "root_ids": model.fit_roots,
                    "model": "empirical response prior, not a neural policy or expert labels"},
            "summaries": summaries, "episodes": episodes, "headroom_evaluator_only": headroom,
            "limitations": ["30/9 preinspected synthetic worlds; repeated seeds do not increase independent sample count",
                            "random finite-sample averages may differ from their expectations; headroom bound uses deterministic comparators",
                            "val-distribution planning is diagnostic only, never a fit policy",
                            "planning optimizes order with fixed stopping gates; no probabilistic stopping or v67 use"],
            "sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                       [Path(__file__), PROTOCOL, BUNDLE / "manifest.json", BUNDLE / "train.jsonl", BUNDLE / "val_internal.jsonl",
                        Path(__file__).with_name("joint_environment.py"), Path(__file__).with_name("joint_runtime.py")]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    path = args.report.resolve()
    require(ROOT / "outputs" in path.parents and not path.exists(), "new report inside outputs/ required")
    report = compare()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{k: row[k] for k in ("cost_protocol", "split", "policy", "mean_questions", "mean_cost", "correct_terminal_rate", "policy_fallbacks")}
                      for row in report["summaries"]]))
    print(json.dumps(report["headroom_evaluator_only"]))


if __name__ == "__main__":
    main()
