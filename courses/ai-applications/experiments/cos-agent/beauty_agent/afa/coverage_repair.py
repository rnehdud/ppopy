"""Audit structural coverage and build a separately versioned internal repair."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .joint_data import BUNDLE as SOURCE, SPLITS, load_joint_split
from .scenario_plan import digest, validate_membership
from .stage0 import DEFAULT, ROOT, require
from .stage1 import encode

BUNDLE = DEFAULT.parent.parent / "coverage-repair-v1"
PARTITION = BUNDLE / "partition.json"


def family_values(row):
    return {key: row["environment_only"]["response_table"][key]["value"]
            for key in ("method.tools", "method.friction", "method.drying")}


def stratum(values):
    return "hands" if values["method.tools"] == "hands" else "tool_difference"


def coverage_audit(records):
    validate_membership([{**row, "effective_response_table": row["environment_only"]["response_table"]} for row in records])
    families = {}
    for row in records:
        values = family_values(row)
        require(row["family_id"] == digest(values), "family identity drift")
        families[row["family_id"]] = {"values": values, "split": row["split"]}
    result = {}
    for split in SPLITS:
        rows = [row for row in records if row["split"] == split]
        groups = [row for row in families.values() if row["split"] == split]
        counts = Counter(stratum(row["values"]) for row in groups)
        result[split] = {"worlds": len(rows), "families": len(groups),
            "stratum_families": {name: counts[name] for name in ("hands", "tool_difference")},
            "tools_world_counts": dict(sorted(Counter(row["environment_only"]["response_table"]["method.tools"]["value"] for row in rows).items())),
            "water_values": sorted({row["environment_only"]["response_table"]["method.water_temperature"]["value"] for row in rows}),
            "missing_required_strata": [name for name in ("hands", "tool_difference") if counts[name] == 0]}
    # Necessary feasibility checks only; do not pretend they solve all allocation constraints.
    aligned = [key for key, row in families.items() if row["values"] == {
        "method.tools": "hands", "method.friction": "gentle", "method.drying": "pat_gently"}]
    feasibility = {
        "every_tool_value_in_every_split": {"feasible": all(result[s]["families"] >= 4 for s in SPLITS),
            "reason": "four distinct tools need at least four indivisible families per split; val/test have three"},
        "aligned_method_family_in_every_split": {"feasible": len(aligned) >= len(SPLITS),
            "family_count": len(aligned), "current_splits": sorted({families[key]["split"] for key in aligned}),
            "reason": "one indivisible aligned-method family cannot be placed in three disjoint splits"}}
    return {"splits": result, "feasibility_checks": feasibility,
            "required_strata_present_everywhere": all(not row["missing_required_strata"] for row in result.values()),
            "independent_evaluation": False, "scope": "structural coverage, not policy accuracy or clinical difficulty"}


def repaired_records(records, partition):
    require(partition["mode"] == "development_preview" and partition["production_enabled"] is False and
            partition["independent_evaluation"] is False and partition["approved_reference"] is False and
            partition["same_48_preinspected_worlds"] is True and not partition["cost_or_gate_changes"],
            "internal-only unchanged-world coverage repair required")
    require(partition["strata"] == {"hands": {"train": 2, "val_internal": 1, "test_internal": 1},
        "tool_difference": {"train": 8, "val_internal": 2, "test_internal": 2}}, "fixed structural quotas required")
    require(partition["split_family_counts"] == {"train": 10, "val_internal": 3, "test_internal": 3}, "fixed family totals")
    require(not partition["performance_protocol_frozen"] and not partition["policy_scoring_authorized_in_this_step"] and
            not partition["learning_executed"], "partition construction is not a performance experiment")
    coverage_audit(records)
    families = {row["family_id"]: family_values(row) for row in records}
    assignments = {}
    for name in ("hands", "tool_difference"):
        selected = sorted((key for key, values in families.items() if stratum(values) == name),
                          key=lambda key: digest([partition["assignment_salt"], name, key]))
        quotas = partition["strata"][name]
        require(sum(quotas.values()) == len(selected), "family quota infeasible")
        offset = 0
        for split in SPLITS:
            for key in selected[offset:offset + quotas[split]]:
                assignments[key] = split
            offset += quotas[split]
    result = []
    for source in records:
        row = deepcopy(source)
        row["prior_split"] = source["split"]
        row["origin_bundle"] = "joint-v2-v1"
        row["partition_revision"] = partition["version"]
        row["split"] = assignments[row["family_id"]]
        result.append(row)
    require(len(result) == 48 and len(assignments) == 16, "complete 48-world/16-family scope required")
    require(coverage_audit(result)["required_strata_present_everywhere"], "repair missed a required stratum")
    return result


def artifacts():
    partition = json.loads(PARTITION.read_text(encoding="utf-8"))
    original = [row for split in SPLITS for row in load_joint_split(split)]
    repaired = repaired_records(original, partition)
    files = {split + ".jsonl": "".join(encode(row) + "\n" for row in sorted(repaired, key=lambda row: row["root_world_id"]) if row["split"] == split)
             for split in SPLITS}
    original_manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    hashes = dict(original_manifest["source_hashes"])
    for path in [PARTITION, Path(__file__), SOURCE / "manifest.json"] + [SOURCE / (split + ".jsonl") for split in SPLITS]:
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    families = {row["family_id"]: {"family_id": row["family_id"], "values": family_values(row), "split": row["split"]} for row in repaired}
    manifest = {"version": partition["version"], "mode": "development_preview", "production_enabled": False,
        "source_hashes": hashes, "split_counts": {s: sum(row["split"] == s for row in repaired) for s in SPLITS},
        "family_assignment": [families[key] for key in sorted(families)],
        "preinspected_synthetic_domains": True, "independent_evaluation": False,
        "human_review": "unreviewed", "approved_reference": False,
        "scope": "new internal partition of the same inspected worlds; response/reference values unchanged; no policy scoring",
        "files": {name: hashlib.sha256(content.encode()).hexdigest() for name, content in files.items()}}
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    report = {"mode": "development_preview", "production_enabled": False,
        "before": coverage_audit(original), "after": coverage_audit(repaired),
        "preservation": {"root_ids": {r["root_world_id"] for r in original} == {r["root_world_id"] for r in repaired},
            "unchanged_responses_and_references": all(next(r for r in repaired if r["root_world_id"] == source["root_world_id"])["environment_only"] == source["environment_only"] for source in original)},
        "moved_worlds": sum(row["prior_split"] != row["split"] for row in repaired),
        "learning_executed": False, "policy_performance_evaluated": False,
        "independent_evaluation_ready": False,
        "remaining_gaps": ["same preinspected product/rules/worlds; new split is not unseen",
            "singleton aligned-method family cannot cover all three splits",
            "all four tool identities cannot fit in three-family val/test splits",
            "unknown/refusal/correction remain engineering probes, not a performance cohort",
            "exact planning may remain optimal; a better-balanced split does not create PPO superiority"],
        "partition_sha256": hashlib.sha256(PARTITION.read_bytes()).hexdigest(),
        "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return files, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report_path = args.report.resolve()
    require(ROOT / "outputs" in report_path.parents and not report_path.exists(), "new report inside outputs/ required")
    files, report = artifacts()
    if args.command == "build":
        require(not any((BUNDLE / name).exists() for name in files), "repair bundle already exists")
        for name, text in files.items():
            with (BUNDLE / name).open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
    for name, text in files.items():
        require((BUNDLE / name).read_bytes() == text.encode(), "repair bundle drift: " + name)
    # Verify compatibility with the existing loader without changing runtime/costs.
    for split in SPLITS:
        load_joint_split(split, BUNDLE)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"before": report["before"]["splits"], "after": report["after"]["splits"],
                      "preservation": report["preservation"], "moved_worlds": report["moved_worlds"],
                      "independent_evaluation_ready": False}))


if __name__ == "__main__":
    main()
