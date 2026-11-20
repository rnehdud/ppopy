"""Public-input baselines fitted on train only. No RL or test-score selection."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np

from .environment import StaticAFAEnv, load_split
from .stage0 import DEFAULT, ROOT, require
from .stage1 import encode
from .validation import RawReference

PROTOCOL = DEFAULT.parent.parent / "stage4-v1/protocol.json"


def public_state(contract, observation):
    """Decode only the specified public vector; no world/reference/session object."""
    schema = contract["observation_schema"]
    require(observation.shape == (schema["dimension"],), "unexpected public vector")
    offset = 0
    states = {}
    for slot in schema["slot_order"]:
        section = observation[offset:offset + len(schema["state_order"]) ]
        require(np.count_nonzero(section) == 1 and section.max() == 1, "invalid state one-hot")
        states[slot] = schema["state_order"][int(section.argmax())]
        offset += len(section)
    visible = {}
    for slot in schema["slot_order"]:
        values = schema["value_order"][slot]
        section = observation[offset:offset + len(values)]
        require(np.count_nonzero(section) == 1 and section.max() == 1, "invalid value one-hot")
        value = values[int(section.argmax())]
        if states[slot] == "known":
            require(value is not None, "known null public value")
            visible[slot] = value
        offset += len(values)
    tasks = list(contract["tasks"])
    card = tasks[int(observation[offset:offset + len(tasks)].argmax())]
    return card, visible, int(observation[-1])


class RulePolicy:
    """Existing RuleBasedActionPlanner order restricted to the fixed task actions."""
    name = "existing_rule_order"

    def __init__(self, contract):
        self.contract = deepcopy(contract)
        self.pairs = [tuple(p) for p in contract["action_dictionary"]]
        self.fallbacks = 0

    def select(self, observation, mask):
        enabled = list(np.flatnonzero(mask))
        require(enabled, "empty action mask")
        # In this static task, KB question offers are sorted by target, like the existing context builder.
        return int(min(enabled, key=lambda i: ({"ask_user": 0, "request_draft": 1, "hold": 2}[self.pairs[i][0]],
                                              self.pairs[i][1])))


class RandomPolicy(RulePolicy):
    def __init__(self, contract, seed, acquisition_only=False):
        super().__init__(contract)
        self.rng = np.random.default_rng(seed)
        self.acquisition_only = acquisition_only
        self.name = "random_acquisition_fixed_stop" if acquisition_only else "uniform_all_allowed"

    def select(self, observation, mask):
        enabled = list(np.flatnonzero(mask))
        if self.acquisition_only:
            asks = [i for i in enabled if self.pairs[i][0] == "ask_user"]
            if not asks:
                return super().select(observation, mask)
            enabled = asks
        return int(self.rng.choice(enabled))


class GreedyPolicy(RulePolicy):
    """One-step expected terminal-loss reduction/cost; empirical train answer prior."""
    name = "train_prior_greedy_fixed_stop"

    def __init__(self, contract, train_rows):
        super().__init__(contract)
        require(all(r["split"] == "train" for r in train_rows), "greedy fit must be train-only")
        self._training_worlds = [deepcopy(r["environment_only"]) for r in train_rows]
        self._reference = RawReference(contract)

    def select(self, observation, mask):
        asks = [int(i) for i in np.flatnonzero(mask) if self.pairs[i][0] == "ask_user"]
        if not asks:
            return super().select(observation, mask)
        card, visible, _ = public_state(self.contract, observation)
        candidates = [w for w in self._training_worlds if w["card_id"] == card and
                      all(w["response_table"].get(k, {}).get("value") == v for k, v in visible.items())]
        if not candidates:
            self.fallbacks += 1
            return super().select(observation, mask)
        gain = {}
        for index in asks:
            target = self.pairs[index][1]
            successes = 0
            for world in candidates:
                after = {**visible, target: world["response_table"][target]["value"]}
                state = self._reference.evaluate(card, after)
                full = self._reference.evaluate(card, {k: v["value"] for k, v in world["response_table"].items()})
                successes += int(state["semantic"] == full["semantic"] and
                                 (state["draft"] or not state["asks"]))
            gain[index] = (successes / len(candidates) * self.contract["objective"]["incorrect_terminal_loss"] /
                           self.contract["objective"]["ask_cost"])
        return min(asks, key=lambda i: (-gain[i], self.pairs[i][1]))


def state_key(observation, mask):
    return encode({"observation": observation.tolist(), "mask": mask.astype(int).tolist()})


class TabularBC(RulePolicy):
    name = "tabular_bc_rule_teacher"

    def __init__(self, contract, table):
        super().__init__(contract)
        self._table = deepcopy(table)

    def select(self, observation, mask):
        learned = self._table.get(state_key(observation, mask))
        if learned is not None and mask[learned]:
            return learned
        self.fallbacks += 1
        return super().select(observation, mask)


def fit_bc(contract, train_rows):
    """Supervised exact-state lookup, deduplicated across train worlds and question orders."""
    require(all(r["split"] == "train" for r in train_rows), "BC fit must be train-only")
    reference = RawReference(contract)
    teacher = RulePolicy(contract)
    table = {}
    for record in train_rows:
        world = record["environment_only"]
        card = world["card_id"]
        visited = set()

        def visit(visible, remaining):
            local = encode({"visible": visible, "remaining": remaining})
            if local in visited:
                return
            visited.add(local)
            mask = reference.mask(reference.evaluate(card, visible), remaining)
            observation = reference.observation(card, visible, remaining)
            key = state_key(observation, mask)
            target = teacher.select(observation, mask)
            require(key not in table or table[key] == target, "teacher label conflict")
            table[key] = target
            for index in np.flatnonzero(mask):
                action, slot = reference.pairs[int(index)]
                if action == "ask_user":
                    visit({**visible, slot: world["response_table"][slot]["value"]}, remaining - 1)

        visit({}, contract["objective"]["max_questions"])
    return table


def describe_episodes(episodes):
    questions = [e["questions"] for e in episodes]
    drafts = [e for e in episodes if e["terminal"] == "request_draft"]
    n = len(episodes)
    return {"episode_count": n, "distinct_worlds": len({e["world_fingerprint"] for e in episodes}),
            "mean_questions": float(np.mean(questions)), "median_questions": float(np.median(questions)),
            "p95_questions": float(np.percentile(questions, 95)),
            "mean_cost": float(np.mean([e["cost"] for e in episodes])),
            "mean_return": float(np.mean([e["return"] for e in episodes])),
            "correct_terminal_rate": sum(e["correct_terminal"] for e in episodes) / n,
            "semantic_match_rate": sum(e["semantic_match"] for e in episodes) / n,
            "draft_rate": len(drafts) / n, "hold_rate": sum(e["terminal"] == "hold" for e in episodes) / n,
            "wrong_hold_rate": sum(e["terminal"] == "hold" and not e["correct_terminal"] for e in episodes) / n,
            "error_among_drafts": (sum(not e["correct_terminal"] for e in drafts) / len(drafts)) if drafts else None,
            "policy_fallbacks": sum(e["policy_fallbacks"] for e in episodes),
            "runtime_rejects": 0, "runtime_fallbacks": 0}


def hindsight_cost(reference, world):
    """Evaluator-only, hidden-world lower bound. Never used by a baseline select()."""
    memo = {}

    def visit(visible, remaining):
        key = encode({"visible": visible, "remaining": remaining})
        if key in memo:
            return memo[key]
        costs = []
        state = reference.evaluate(world["card_id"], visible)
        for index in np.flatnonzero(reference.mask(state, remaining)):
            after, left, _, done, _, correct = reference.transition(world, visible, remaining, int(index))
            acquisition = reference.contract["objective"]["ask_cost"] if reference.pairs[int(index)][0] == "ask_user" else 0
            if done:
                if correct:
                    costs.append(acquisition)
            else:
                costs.append(acquisition + visit(after, left))
        require(costs, "no quality-preserving reference path")
        memo[key] = min(costs)
        return memo[key]

    return visit({}, reference.contract["objective"]["max_questions"])


def compare(seeds=(0, 1, 2), evaluation_splits=("train", "val_internal"), env_factory=StaticAFAEnv):
    require(set(evaluation_splits) <= {"train", "val_internal"} and evaluation_splits, "Stage 4 does not score test_internal")
    require(seeds and len(set(seeds)) == len(seeds), "distinct nonempty seeds required")
    contract, training = load_split("train")
    table = fit_bc(contract, training)
    reference = RawReference(contract)
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8-sig"))
    require(protocol["mode"] == "development_preview" and protocol["production_enabled"] is False and
            protocol["fit_split"] == "train" and protocol["test_internal_scoring"] is False, "baseline protocol boundary")
    rows = []
    bounds = {}
    for split in evaluation_splits:
        env = env_factory(split)
        bounds[split] = float(np.mean([hindsight_cost(reference, r["environment_only"]) for r in env._records]))
        for seed in seeds:
            policies = [RulePolicy(contract), RandomPolicy(contract, seed),
                        RandomPolicy(contract, seed, acquisition_only=True),
                        GreedyPolicy(contract, training), TabularBC(contract, table)]
            for policy in policies:
                for world_index, record in enumerate(env._records):
                    observation, _ = env.reset(seed=seed, options={"world_index": world_index})
                    world = record["environment_only"]  # Evaluator only, never passed to select().
                    visible = {}
                    remaining = contract["objective"]["max_questions"]
                    total = 0.0
                    questions = 0
                    fallback_before = policy.fallbacks
                    trace = []
                    while True:
                        mask = env.action_masks()
                        index = policy.select(observation.copy(), mask.copy())
                        require(isinstance(index, int) and mask[index], "baseline invalid action")
                        expected = reference.transition(world, visible, remaining, index)
                        observation, reward, done, truncated, info = env.step(index)
                        require((reward, done, truncated) == (expected[2], expected[3], False), "baseline transition mismatch")
                        total += reward
                        action, target = reference.pairs[index]
                        questions += int(action == "ask_user")
                        trace.append({"action": action, "target": target, "reward": reward})
                        visible, remaining = expected[0], expected[1]
                        if done:
                            full = reference.evaluate(world["card_id"], {k: v["value"] for k, v in world["response_table"].items()})
                            semantic_match = reference.evaluate(world["card_id"], visible)["semantic"] == full["semantic"]
                            rows.append({"split": split, "seed": seed, "policy": policy.name,
                                         "world_fingerprint": record["world_fingerprint"], "card": world["card_id"],
                                         "questions": questions, "cost": questions * contract["objective"]["ask_cost"],
                                         "return": total, "terminal": action, "correct_terminal": bool(expected[5]),
                                         "semantic_match": semantic_match,
                                         "policy_fallbacks": policy.fallbacks - fallback_before, "trace": trace})
                            break
    summaries = []
    for split in evaluation_splits:
        for policy in sorted({r["policy"] for r in rows}):
            selected = [r for r in rows if r["split"] == split and r["policy"] == policy]
            summaries.append({"split": split, "policy": policy, **describe_episodes(selected),
                              "per_card": [{"card": card, **describe_episodes([r for r in selected if r["card"] == card])}
                                           for card in sorted({r["card"] for r in selected})],
                              "per_seed": [{"seed": seed, **describe_episodes([r for r in selected if r["seed"] == seed])}
                                           for seed in seeds]})
    headroom = []
    for split in evaluation_splits:
        candidates = [s for s in summaries if s["split"] == split and s["correct_terminal_rate"] == 1]
        best = min(candidates, key=lambda s: (s["mean_cost"], s["policy"]))
        headroom.append({"split": split, "strongest_quality_preserving_policy": best["policy"],
                         "baseline_mean_cost": best["mean_cost"], "hindsight_lower_bound": bounds[split],
                         "gap_to_hindsight": best["mean_cost"] - bounds[split],
                         "interpretation": "gap is an upper bound on possible improvement; hindsight may not be attainable from public information"})
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "Stage 4 train/val development baselines; no RL or test scoring",
            "seeds": list(seeds), "evaluation_splits": list(evaluation_splits),
            "protocol": protocol, "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(DEFAULT.read_bytes()).hexdigest(),
            "fit": {"split": "train", "worlds": len(training), "bc_unique_public_states": len(table),
                    "bc_teacher": "existing static-task rule order, not human/expert/optimal labels",
                    "greedy_model": "uniform empirical distribution over matching train worlds only",
                    "fitted_world_fingerprints": [r["world_fingerprint"] for r in training],
                    "bc_table_sha256": hashlib.sha256(encode(table).encode()).hexdigest(),
                    "bc_action_table": table},
            "summaries": summaries, "episodes": rows,
            "headroom_analysis_evaluator_only": headroom,
            "limitations": ["6/2 tiny pre-inspected design worlds; not an independent generalization result",
                            "greedy uses fixed gate stopping, optimizing acquisition order only; not Bayes-optimal VOI/stopping",
                            "BC memorizes teacher state/action table and logs unseen-state rule fallback",
                            "repeated deterministic policies/seeds are not independent samples",
                            "low question count without matching quality/coverage is not improvement"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    report = compare()
    report["runner_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{k: r[k] for k in ("split", "policy", "mean_questions", "correct_terminal_rate", "policy_fallbacks")}
                      for r in report["summaries"]]))


if __name__ == "__main__":
    main()
