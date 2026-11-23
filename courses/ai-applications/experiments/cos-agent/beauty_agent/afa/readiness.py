"""Evaluator-only readiness diagnostics; never a policy, fit input or test score."""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from math import inf, isfinite
from pathlib import Path
import statistics
from time import perf_counter

import numpy as np

from .baselines import GreedyPolicy, RulePolicy, hindsight_cost
from .environment import load_split
from .runtime import StaticSessionAdapter
from .stage0 import DEFAULT, ROOT, audit, require, signature, snapshot
from .stage1 import encode
from .validation import RawReference


def public_information_optimum(contract, worlds):
    """Exact zero-error expected acquisition cost under a declared uniform support.

    One action is chosen per (card, visible answers, remaining budget, posterior).
    Future answers may partition the posterior; actual hidden world IDs cannot
    choose the action. This knows the evaluation distribution, so it is an
    evaluator-only feasibility diagnostic, NOT a deployable/train-fitted baseline.
    """
    require(bool(worlds), "nonempty support required")
    reference = RawReference(contract)
    groups = defaultdict(list)
    for world in deepcopy(worlds):
        groups[world["card_id"]].append(world)
    tree = []
    total = 0.0
    for card, support in sorted(groups.items()):
        memo = {}

        def visit(indices, visible, remaining):
            key = encode([list(indices), visible, remaining])
            if key in memo:
                return memo[key]
            state = reference.evaluate(card, visible)
            candidates = []
            for index in np.flatnonzero(reference.mask(state, remaining)):
                index = int(index)
                action, target = reference.pairs[index]
                outcomes = [(i, reference.transition(support[i], visible, remaining, index)) for i in indices]
                if action != "ask_user":
                    if all(result[5] is True for _, result in outcomes):
                        candidates.append((0.0, index))
                    continue
                # A forced budget failure cannot satisfy the zero-error constraint.
                if any(result[3] for _, result in outcomes):
                    continue
                partitions = defaultdict(list)
                for i, result in outcomes:
                    partitions[encode(result[0])].append(i)
                expected = contract["objective"]["ask_cost"]
                for answers, members in partitions.items():
                    expected += len(members) / len(indices) * visit(tuple(members), json.loads(answers), remaining - 1)
                candidates.append((expected, index))
            cost, chosen = min(candidates, default=(inf, None))
            memo[key] = cost
            tree.append({"card": card, "visible": dict(visible), "remaining": remaining,
                         "posterior_world_count": len(indices), "action_index": chosen,
                         "expected_acquisition_cost": cost if isfinite(cost) else None})
            return cost

        value = visit(tuple(range(len(support))), {}, contract["objective"]["max_questions"])
        require(isfinite(value), "no common zero-error public-information policy")
        total += len(support) / len(worlds) * value
    return {"mean_cost": total, "prior": "uniform over this diagnostic split's worlds; card is public",
            "constraint": "correct terminal in every supported world", "states": tree,
            "policy_training_use": False, "independent_generalization_evidence": False}


def semantic_witnesses(contract):
    """Preserve conflicting terminal meanings instead of declaring equivalence."""
    adapter = StaticSessionAdapter(contract, "B-C02").kb
    result = []
    for world in audit(contract)["worlds"]:
        if world["eligible"]:
            continue
        paths = []
        for path in world["paths"]:
            visible = {slot: world["hidden_synthetic_answers"][slot] for slot in path["questions"]}
            _, evaluated = snapshot(contract, world["card"], visible, adapter)
            paths.append({"questions": path["questions"], "semantic": signature(evaluated),
                          "branch_ids": [r["matched_branch_id"] for r in evaluated["raw"]["results"]]})
        result.append({"world_id": world["world_id"], "answers": world["hidden_synthetic_answers"],
                       "full_information_reference": world["reference"], "terminal_paths": paths,
                       "resolution": "pending semantic contract review; excluded from v1"})
    return result


def profile_runtime(contract, samples=20):
    """Local microbenchmark only; no shared KB or validation bypass."""
    require(isinstance(samples, int) and samples > 0, "positive sample count required")
    session = StaticSessionAdapter(contract, "B-C02")
    session.prepare_context()

    def reload_fork():
        clone = StaticSessionAdapter(contract, session.card)
        clone._state = session.state
        clone._prepared = session._prepared
        clone._base_state = session._base_state
        clone.dispatch_count = session.dispatch_count
        return clone

    factories = {"reload_fork_reference": reload_fork,
                 "isolated_memory_copy": lambda: deepcopy(session), "current_fork": session.fork}
    timings = {key: [] for key in factories}
    for _ in range(samples):
        for name, factory in factories.items():
            start = perf_counter()
            factory()
            timings[name].append((perf_counter() - start) * 1000)
    return {"samples_per_method": samples, "units": "milliseconds", "scope": "local prepared adapter fork only",
            "timings": {k: {"median": statistics.median(v), "p95": float(np.percentile(v, 95))}
                        for k, v in timings.items()},
            "limitations": "not rollout throughput, training speed or a portable performance guarantee"}


def inspect_readiness(profile_samples=20):
    contract, training = load_split("train")
    splits = []
    reference = RawReference(contract)
    for split in ("train", "val_internal"):
        _, records = load_split(split)
        worlds = [row["environment_only"] for row in records]
        optimum = public_information_optimum(contract, worlds)
        baseline_costs = {}
        for policy in (RulePolicy(contract), GreedyPolicy(contract, training)):
            costs = []
            for world in worlds:
                visible, remaining, cost = {}, contract["objective"]["max_questions"], 0
                while True:
                    state = reference.evaluate(world["card_id"], visible)
                    index = policy.select(reference.observation(world["card_id"], visible, remaining),
                                          reference.mask(state, remaining))
                    after, left, _, done, _, correct = reference.transition(world, visible, remaining, index)
                    cost += contract["objective"]["ask_cost"] if reference.pairs[index][0] == "ask_user" else 0
                    if done:
                        require(correct, "baseline failed zero-error comparator")
                        break
                    visible, remaining = after, left
                costs.append(cost)
            baseline_costs[policy.name] = statistics.mean(costs)
        rule_cost = baseline_costs[RulePolicy.name]
        best = min(baseline_costs.values())
        gap = best - optimum["mean_cost"]
        require(gap >= -1e-9, "measured baseline beat public-information optimum")
        splits.append({"split": split, "worlds": len(worlds), "existing_rule_mean_cost": rule_cost,
                       "train_fitted_baseline_costs": baseline_costs,
                       "best_measured_baseline_gap_to_public_optimum": max(0.0, gap),
                       "hindsight_lower_bound": statistics.mean(hindsight_cost(reference, w) for w in worlds),
                       "public_information_optimum": optimum,
                       "rule_gap_to_public_optimum": rule_cost - optimum["mean_cost"]})
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "post-Stage-4 engineering diagnostics; no fitting, RL or test scoring",
            "splits": splits, "semantic_review_queue": semantic_witnesses(contract),
            "runtime_profile": profile_runtime(contract, profile_samples),
            "readiness": {"v1_learning_connection_smoke": True,
                          "v1_question_efficiency_claim": all(r["best_measured_baseline_gap_to_public_optimum"] > 1e-9
                                                              for r in splits),
                          "independent_evaluation": False, "domain_reference_approved": False,
                          "v2_runtime_implemented": False},
            "next_requirements": ["versioned semantic contract for mixed-action worlds",
                                  "response provenance, temporal events, unknown/refusal semantics",
                                  "mandatory safety information versus optional acquisition/stopping",
                                  "predeclared broader benchmark with attainable public-information headroom",
                                  "train-only stronger baselines and independent family-level evaluation"],
            "sha256": {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [DEFAULT, Path(__file__), Path(__file__).with_name('runtime.py'),
                                 Path(__file__).with_name('environment.py'), Path(__file__).with_name('baselines.py'),
                                 Path(__file__).with_name('validation.py'),
                                 DEFAULT.parent.parent / 'stage1-v1/manifest.json',
                                 DEFAULT.parent.parent / 'stage1-v1/train.jsonl',
                                 DEFAULT.parent.parent / 'stage1-v1/val_internal.jsonl']}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--profile-samples", type=int, default=20)
    parser.add_argument("--require-efficiency-headroom", action="store_true",
                        help="write diagnostics, then exit 1 when the fixed task lacks improvement headroom")
    args = parser.parse_args()
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    report = inspect_readiness(args.profile_samples)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"splits": [{k: r[k] for k in ('split', 'existing_rule_mean_cost', 'rule_gap_to_public_optimum')}
                                  for r in report['splits']], "readiness": report['readiness'],
                      "runtime_profile": report['runtime_profile']}))
    if args.require_efficiency_headroom and not report["readiness"]["v1_question_efficiency_claim"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
