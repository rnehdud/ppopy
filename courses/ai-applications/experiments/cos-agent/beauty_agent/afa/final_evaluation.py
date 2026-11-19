"""Freeze B-C02 policy settings, then compare fixed checkpoints on the internal test."""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

from .eda import ROOT, fingerprint
from .outcome_review import OutcomeEnv, runtime_outcome
from .partial_context_eval import ToolsFirst, run_case, summarize
from .policy_adapter import PPOAFAPolicy
from .ppo_preflight import PPO_SETTINGS, TRIAL_STEPS
from .tracking import receipt
from .v67_fixtures import SLOTS


PROTOCOL = {
    "split": "test_internal",
    "primary": "ppo_seed0",
    "check_seeds": [0, 1, 2],
    "reference": "full B-C02 runtime outcome",
    "gate": "B-C02 outcome stability",
    "decision": "keep quality on every baseline-correct case and reduce total questions in both start cohorts",
    "detect_reasks": True,
}


def frozen_manifest():
    out = ROOT / "outputs"
    model_paths = [
        out / "afa-e29/model-seed0.zip",
        out / "afa-e33/model-seed1.zip",
        out / "afa-e33/model-seed2.zip",
    ]
    eval_sources = [
        Path(__file__), Path(__file__).with_name("outcome_review.py"),
        Path(__file__).with_name("termination_check.py"),
        Path(__file__).with_name("partial_context_eval.py"),
        Path(__file__).with_name("ppo_preflight.py"),
        Path(__file__).with_name("policy_adapter.py"),
        Path(__file__).with_name("v67_reward.py"),
        Path(__file__).parents[1] / "actions.py",
        Path(__file__).parents[1] / "modules/kb_adapter.py",
        ROOT / "skin_engine/kb_preview/rules.json",
    ]
    return {
        "protocol": PROTOCOL, "training_settings": PPO_SETTINGS, "training_steps": TRIAL_STEPS,
        "model_receipts": [receipt(path) for path in model_paths],
        "source_receipts": [receipt(path.resolve()) for path in eval_sources],
    }


def assess(rows, baseline):
    if [(r["fixture_id"], r["prefilled"]) for r in rows] != [
        (r["fixture_id"], r["prefilled"]) for r in baseline
    ]:
        raise ValueError("cases must be aligned")
    return {
        "new_incorrect": sum(b["correct_terminal"] and not a["correct_terminal"]
                             for a, b in zip(rows, baseline)),
        "corrected": sum(a["correct_terminal"] and not b["correct_terminal"]
                         for a, b in zip(rows, baseline)),
        "question_delta": sum(a["questions"] - b["questions"] for a, b in zip(rows, baseline)),
        "reasks": sum(len(row["reasked"]) for row in rows),
    }


def evaluate(frozen):
    env = OutcomeEnv(PROTOCOL["split"])
    policies = {"tools_first": ToolsFirst(), **{
        f"ppo_seed{seed}": PPOAFAPolicy(ROOT / model["path"])
        for seed, model in zip(PROTOCOL["check_seeds"], frozen["model_receipts"])
    }}
    subsets = [subset for count in range(len(SLOTS) + 1) for subset in combinations(SLOTS, count)]
    cases = {
        name: [run_case(env, i, subset, policy, outcome_signature=runtime_outcome)
               for i in range(len(env.rows)) for subset in subsets]
        for name, policy in policies.items()
    }
    cohorts = {}
    for label, prefilled in (("unprefilled", False), ("prefilled", True)):
        groups = {
            name: [row for row in rows if bool(row["prefilled"]) is prefilled]
            for name, rows in cases.items()
        }
        cohorts[label] = {
            name: {**summarize(rows), **assess(rows, groups["tools_first"])}
            for name, rows in groups.items()
        }
    adoption = all(
        cohort[name]["correct"] >= cohort["tools_first"]["correct"]
        and cohort[name]["new_incorrect"] == 0 and cohort[name]["question_delta"] < 0
        and cohort[name]["reasks"] == 0
        for cohort in cohorts.values() for name in policies if name != "tools_first"
    )
    return {
        "protocol": PROTOCOL, "mode": "development_preview", "production_enabled": False,
        "independent_external_evaluation": False, "new_training_steps": 0,
        "unique_scenarios": len(env.rows), "families": sorted({r["family"] for r in env.rows}),
        "fixtures_sha256": fingerprint(env.rows), "manifest_sha256": fingerprint(frozen),
        "cohorts": cohorts, "adopt_ppo": adoption, "cases": cases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    freeze = sub.add_parser("freeze")
    verify = sub.add_parser("evaluate")
    for command in (freeze, verify):
        command.add_argument("--manifest", required=True, type=Path)
    verify.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    manifest_path = (ROOT / args.manifest).resolve()
    output = manifest_path if args.command == "freeze" else (ROOT / args.report).resolve()
    if any(not path.is_relative_to(ROOT / "outputs") for path in (manifest_path, output)) or output.exists():
        parser.error("use paths under outputs/ and a new output file")
    frozen = frozen_manifest()
    if args.command == "freeze":
        result = frozen
    else:
        if fingerprint(json.loads(manifest_path.read_text(encoding="utf-8"))) != fingerprint(frozen):
            parser.error("source, settings, or model differ from the frozen manifest")
        result = evaluate(frozen)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(result.get("cohorts", {"frozen": True}), ensure_ascii=False))


if __name__ == "__main__":
    main()
