"""Execute the fixed family-fold baseline protocol with isolated fitting and checking."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np

from .baselines import RandomPolicy, describe_episodes
from .coverage_folds import PLAN, build_plan, validate_plan
from .coverage_repair import family_values
from .joint_baselines import JointRule, JointGreedy, JointMultistep, TrainModel, evaluate_episode
from .joint_data import BUNDLE as SOURCE, SPLITS, load_joint_split
from .joint_environment import JointAFAEnv
from .stage0 import DEFAULT, ROOT, require

PROTOCOL = DEFAULT.parent.parent / "fold-baselines-v1/protocol.json"
POLICIES = ["existing_rule_order", "uniform_all_allowed", "random_acquisition_fixed_stop",
            "joint_train_greedy", "joint_train_multistep"]


def read_protocol():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    require(protocol["mode"] == "development_preview" and protocol["production_enabled"] is False and
            protocol["independent_evaluation"] is False and protocol["approved_reference"] is False,
            "inactive internal protocol required")
    require(protocol["folds"] == 16 and protocol["fit_worlds_per_fold"] == 45 and
            protocol["check_worlds_per_fold"] == 3 and protocol["seeds"] == [0, 1, 2] and
            protocol["cost_protocols"] == ["unit_primary", "weighted_sensitivity"] and protocol["policies"] == POLICIES,
            "fixed fold/seed/cost/policy protocol required")
    require(protocol["fresh_response_model_per_fold"] is True and protocol["fresh_policy_per_cost_and_seed"] is True and
            protocol["cross_fold_model_or_checkpoint_carryover"] is False, "fold isolation required")
    return protocol


def load_schedule():
    records = [row for split in SPLITS for row in load_joint_split(split)]
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    expected, _ = build_plan()
    require(plan == expected, "frozen fold plan drift")
    validate_plan(plan, records)
    require([fold["fold_id"] for fold in plan["folds"]] == list(range(16)), "unique ordered fold IDs required")
    return records, plan


def project_fold(records, fold):
    roots = {row["root_world_id"]: row for row in records}
    require(len(roots) == len(records) == 48, "verified 48-world source required")
    fit, check = set(fold["fit_root_ids"]), set(fold["check_root_ids"])
    require(len(fit) == len(fold["fit_root_ids"]) == 45 and len(check) == len(fold["check_root_ids"]) == 3 and
            not fit & check and fit | check == set(roots), "fold root overlap or omission")
    fit_families = {roots[key]["family_id"] for key in fit}
    check_families = {roots[key]["family_id"] for key in check}
    require(not fit_families & check_families and check_families == {fold["held_family_id"]} and
            len(fit_families) == 15, "held family entered fitting data")

    def copy_rows(ids, role):
        result = []
        for key in sorted(ids):
            row = deepcopy(roots[key])
            row["source_split"] = row["split"]
            row["split"] = role
            row["fold_id"] = fold["fold_id"]
            result.append(row)
        return result

    return copy_rows(fit, "train"), copy_rows(check, "fold_check")


class FoldCheckEnv(JointAFAEnv):
    """Versioned dataset binding, with the unchanged 64-feature runtime and costs."""
    def __init__(self, check_records, cost_protocol):
        require(len(check_records) == 3 and all(row["split"] == "fold_check" for row in check_records),
                "fold environment accepts only three projected check records")
        require(len({row["family_id"] for row in check_records}) == 1 and
                len({row["root_world_id"] for row in check_records}) == 3, "one complete held family required")
        # Parent initialization sets up the unchanged schema/runtime/costs. It
        # dispatches nothing. Replace the historical table before the first reset.
        super().__init__("train", cost_protocol, bundle=SOURCE)
        require(self._prepared is None and self.dispatch_count == 0, "initialization dispatched")
        self._records = deepcopy(check_records)


def run_fold(records, fold, protocol):
    fit, check = project_fold(records, fold)
    # Deliberately local: a new response prior and new planning caches per fold.
    model = TrainModel(fit)
    require(set(model.fit_roots) == set(fold["fit_root_ids"]) and
            not set(model.fit_roots) & set(fold["check_root_ids"]), "fitted prior contains held records")
    episodes = []
    for cost in protocol["cost_protocols"]:
        env = FoldCheckEnv(check, cost)
        try:
            for seed in protocol["seeds"]:
                base = model.inspector.base
                policies = [JointRule(base), RandomPolicy(base, seed), RandomPolicy(base, seed, acquisition_only=True),
                            JointGreedy(base, model), JointMultistep(base, model)]
                require([policy.name for policy in policies] == protocol["policies"], "policy protocol drift")
                for policy in policies:
                    for index in range(3):
                        row = evaluate_episode(env, index, policy, seed)
                        require(row["world_fingerprint"] in fold["check_root_ids"] and
                                row["family_id"] == fold["held_family_id"], "non-held record was scored")
                        episodes.append({"fold_id": fold["fold_id"], "cost_protocol": cost, **row})
        finally:
            env.close()
    return {"fold_id": fold["fold_id"], "held_family_id": fold["held_family_id"],
            "held_method_values": family_values(check[0]), "fit_root_ids": model.fit_roots,
            "check_root_ids": fold["check_root_ids"], "fit_worlds": 45, "check_worlds": 3,
            "fit_check_overlap": False, "response_prior_rebuilt": True, "episodes": episodes}


def summarize(episodes):
    groups = {}
    for row in episodes:
        groups.setdefault((row["cost_protocol"], row["fold_id"], row["seed"], row["world_fingerprint"]), []).append(row)
    for rows in groups.values():
        require(len(rows) == 5 and {row["policy"] for row in rows} == set(POLICIES), "unpaired policy cohort")
    native = {key: next(row for row in rows if row["policy"] == "existing_rule_order") for key, rows in groups.items()}
    result = []
    for cost in sorted({row["cost_protocol"] for row in episodes}):
        for name in POLICIES:
            selected = [row for row in episodes if row["cost_protocol"] == cost and row["policy"] == name]
            pairs = [(row, native[(cost, row["fold_id"], row["seed"], row["world_fingerprint"])]) for row in selected]
            same_quality = all(row["correct_terminal"] and reference["correct_terminal"] for row, reference in pairs)
            result.append({"cost_protocol": cost, "policy": name, **describe_episodes(selected),
                "distinct_families": len({row["family_id"] for row in selected}),
                "median_cost": float(np.median([row["cost"] for row in selected])),
                "p95_cost": float(np.percentile([row["cost"] for row in selected], 95)),
                "matched_quality_to_native": same_quality,
                "paired_mean_cost_saved_vs_native": float(np.mean([reference["cost"] - row["cost"] for row, reference in pairs])) if same_quality else None,
                "per_fold": [{"fold_id": fold, **describe_episodes([row for row in selected if row["fold_id"] == fold])}
                             for fold in sorted({row["fold_id"] for row in selected})],
                "per_seed": [{"seed": seed, **describe_episodes([row for row in selected if row["seed"] == seed])}
                             for seed in sorted({row["seed"] for row in selected})]})
    return result


def compare():
    protocol = read_protocol()
    records, plan = load_schedule()
    folds = []
    for fold in plan["folds"]:
        folds.append(run_fold(records, fold, protocol))
        print("checked held family " + str(fold["fold_id"] + 1) + "/16", flush=True)
    episodes = [row for fold in folds for row in fold["episodes"]]
    require(len(episodes) == 1440, "incomplete fixed fold experiment")
    for cost in protocol["cost_protocols"]:
        for seed in protocol["seeds"]:
            for name in POLICIES:
                roots = [row["world_fingerprint"] for row in episodes if
                         (row["cost_protocol"], row["seed"], row["policy"]) == (cost, seed, name)]
                require(len(roots) == len(set(roots)) == 48, "each root must be scored exactly once per condition")
    paths = [Path(__file__), PROTOCOL, PLAN, SOURCE / "manifest.json"]
    paths += [SOURCE / (split + ".jsonl") for split in SPLITS]
    paths += [Path(__file__).with_name(name) for name in
              ("coverage_folds.py", "joint_baselines.py", "joint_data.py", "joint_runtime.py", "joint_environment.py")]
    return {"mode": "development_preview", "production_enabled": False, "protocol": protocol,
            "scope": "16-family internal CV on preinspected synthetic worlds; held data excluded within each fold",
            "folds": folds, "episodes": episodes, "summaries": summarize(episodes),
            "fit_models_rebuilt": 16, "distinct_checked_roots": 48,
            "ppo_or_neural_learning_executed": False, "policy_performance_evaluated": True,
            "independent_evaluation": False, "configuration_selected_from_scores": False,
            "limitations": ["reuse across folds is CV, not 16 independent datasets; original split labels are provenance only here",
                            "every model/prior fits only its 45 records; each check family is excluded in that fold",
                            "one old source-test record can be fit in other folds; no claim of an untouched final test",
                            "no claim of clinical validity or PPO superiority; fixed finite known-answer task only",
                            "old fixed-split optimal-cost bounds are not asserted as bounds on fold-specific fitted policies"],
            "sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    path = args.report.resolve()
    require(ROOT / "outputs" in path.parents and not path.exists(), "new report inside outputs/ required")
    report = compare()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{k: row[k] for k in ("cost_protocol", "policy", "mean_questions", "mean_cost", "correct_terminal_rate", "policy_fallbacks", "paired_mean_cost_saved_vs_native")}
                      for row in report["summaries"]]))


if __name__ == "__main__":
    main()
