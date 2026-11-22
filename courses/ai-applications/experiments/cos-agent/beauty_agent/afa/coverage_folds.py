"""A fixed leave-one-family-out coverage schedule, not an executed evaluation."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from .coverage_repair import BUNDLE, PARTITION, family_values
from .joint_data import BUNDLE as SOURCE, SPLITS, load_joint_split
from .stage0 import ROOT, require

PLAN = BUNDLE / "fold-plan.json"


def validate_plan(plan, records):
    roots = {row["root_world_id"]: row for row in records}
    all_roots = set(roots)
    test_counts = Counter()
    require(len(plan["folds"]) == 16 and len(all_roots) == 48, "complete 16-family/48-world schedule required")
    held_families = set()
    for fold in plan["folds"]:
        train, test = set(fold["fit_root_ids"]), set(fold["check_root_ids"])
        require(len(train) == len(fold["fit_root_ids"]) == 45 and len(test) == len(fold["check_root_ids"]) == 3,
                "fold record count mismatch")
        require(not train & test and train | test == all_roots, "fold root overlap or omission")
        fit_families = {roots[key]["family_id"] for key in train}
        check_families = {roots[key]["family_id"] for key in test}
        require(not fit_families & check_families and check_families == {fold["held_family_id"]}, "fold family leakage")
        require(len(fit_families) == 15 and fold["held_family_id"] not in held_families, "duplicate or missing held family")
        held_families.add(fold["held_family_id"])
        test_counts.update(test)
    require(set(test_counts) == all_roots and all(count == 1 for count in test_counts.values()), "each world must be checked exactly once")
    require(plan["fresh_model_per_fold"] is True and plan["checkpoint_carryover"] is False and
            plan["aggregate_scores_for_tuning"] is False and plan["learning_executed"] is False and
            plan["policy_performance_evaluated"] is False and plan["independent_evaluation"] is False,
            "schedule is fixed, fold-isolated and not an executed independent evaluation")


def build_plan():
    records = [row for split in SPLITS for row in load_joint_split(split)]
    families = sorted({row["family_id"] for row in records})
    folds = []
    for index, family in enumerate(families):
        folds.append({"fold_id": index, "held_family_id": family,
            "fit_root_ids": sorted(row["root_world_id"] for row in records if row["family_id"] != family),
            "check_root_ids": sorted(row["root_world_id"] for row in records if row["family_id"] == family)})
    plan = {"version": "afa-family-coverage-schedule-0.1", "mode": "development_preview", "production_enabled": False,
        "strategy": "leave-one-method-family-out; fixed before any fold policy score",
        "scope": "internal diagnostic reuse of all 48 already inspected synthetic worlds; not an unseen test",
        "fresh_model_per_fold": True, "checkpoint_carryover": False, "aggregate_scores_for_tuning": False,
        "configuration": "one common model/fit/evaluation configuration must be frozen before executing folds; not selected in this step",
        "fitting": "fit prior/model on the 45 fit_root_ids only; never use check_root_ids as fit data in that fold",
        "cross_fold_reuse": "normal CV reuse across folds; independence is required within each fold, not across all folds",
        "learning_executed": False, "policy_performance_evaluated": False, "independent_evaluation": False,
        "human_review": "unreviewed", "approved_reference": False, "folds": folds,
        "source_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in [Path(__file__), PARTITION, SOURCE / "manifest.json"]}}
    validate_plan(plan, records)
    aligned_roots = [row["root_world_id"] for row in records if family_values(row) == {
        "method.tools": "hands", "method.friction": "gentle", "method.drying": "pat_gently"}]
    report = {"folds": 16, "fit_worlds_per_fold": 45, "check_worlds_per_fold": 3,
        "distinct_checked_roots": 48, "each_family_checked_once": True,
        "aligned_method_roots_checked": len(aligned_roots), "fold_scores_computed": False,
        "independent_evaluation_ready": False}
    return plan, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report_path = args.report.resolve()
    require(ROOT / "outputs" in report_path.parents and not report_path.exists(), "new report inside outputs/ required")
    plan, report = build_plan()
    text = json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.command == "build":
        with PLAN.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    require(PLAN.read_bytes() == text.encode(), "fold plan drift")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
