"""Check the frozen v2 joint-task plan, family split and public engineering examples."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path

from .semantics import SPEC, SemanticInspector, event
from .stage0 import DEFAULT, ROOT, require
from .stage1 import encode

PLAN = DEFAULT.parent.parent / "scenario-plan-v2-v1/plan.json"
PROBES = PLAN.with_name("probes.json")


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def build_design(plan=None):
    plan = deepcopy(plan) if plan is not None else json.loads(PLAN.read_text(encoding="utf-8"))
    require(plan["mode"] == "development_preview" and plan["production_enabled"] is False and
            plan["approved_reference"] is False and plan["training_ready"] is False and
            plan["independent_evaluation"] is False and plan["preinspected_synthetic_domains"] is True,
            "development-only unreviewed plan required")
    require(plan["core_response_states"] == ["known"] and not plan["probe_training_use"] and not plan["probe_scoring_use"],
            "nonanswer/correction probes are engineering-only in this version")
    require(plan["cards_per_episode"] == ["B-C01", "B-C02"] and plan["initial_visible_observations"] == {},
            "fixed joint-card task with no disclosed hidden responses")
    require(plan["readiness"] == {"plan_frozen": True, "v2_adapter_implemented": False, "v2_gym_implemented": False,
                                  "training_bundle_generated": False, "performance_protocol_frozen": False},
            "plan is not an implemented training benchmark")
    inspector = SemanticInspector()
    domains = inspector.domains
    keys = sorted(domains)
    family_slots = plan["family_slots"]
    require(family_slots == ["method.tools", "method.friction", "method.drying"], "fixed method-family definition")
    require(plan["split_family_counts"] == {"train": 10, "val_internal": 3, "test_internal": 3}, "fixed 10/3/3 family split")
    families = [{"family_id": digest(dict(zip(family_slots, values))), "values": dict(zip(family_slots, values))}
                for values in product(*(domains[k] for k in family_slots))]
    families.sort(key=lambda row: digest([plan["split_order_salt"], row["family_id"]]))
    split_by_family = {}
    offset = 0
    for split in ("train", "val_internal", "test_internal"):
        count = plan["split_family_counts"][split]
        for family in families[offset:offset + count]:
            family["split"] = split
            split_by_family[family["family_id"]] = split
        offset += count
    require(offset == len(families) == 16, "family coverage mismatch")
    worlds = []
    for values in product(*(domains[k] for k in keys)):
        hidden = dict(zip(keys, values))
        family_id = digest({k: hidden[k] for k in family_slots})
        root_id = digest(hidden)
        worlds.append({"root_world_id": root_id, "family_id": family_id, "split": split_by_family[family_id],
                       "cards": plan["cards_per_episode"], "environment_only_design_answers": hidden,
                       "training_bundle": False})
    require(len(worlds) == plan["core_world_count"] == 48, "world coverage mismatch")
    for name, protocol in plan["cost_protocols"].items():
        costs = protocol["ask_costs"]
        require(set(costs) == set(domains) and all(type(v) is int and v > 0 for v in costs.values()), "positive cost for every question required")
        require(protocol["max_questions"] == len(domains) == 5 and
                protocol["max_acquisition_cost"] == sum(costs.values()), "question/cost budget mismatch")
        require(protocol["incorrect_terminal_loss"] == sum(costs.values()) + 1 and
                protocol["correct_terminal_loss"] == 0 and protocol["gamma"] == 1 and protocol["shaping_beta"] == 0,
                "invalid total-cost and wrong-exit protocol: " + name)
    require(set(plan["cost_protocols"]) == {"unit_primary", "weighted_sensitivity"}, "fixed cost cohorts")
    require(all(cost == 1 for cost in plan["cost_protocols"]["unit_primary"]["ask_costs"].values()), "primary cost must be unit")
    require(plan["cost_protocols"]["weighted_sensitivity"]["ask_costs"] ==
            {key: 2 if key in {"method.friction", "method.drying"} else 1 for key in domains}, "fixed sensitivity weights")
    validate_membership(worlds)
    probes = json.loads(PROBES.read_text(encoding="utf-8"))
    probe_results = []
    for example in probes["examples"]:
        ledger = inspector.ledger()
        for row in example["events"]:
            ledger = ledger.append(event(row[0], row[1], row[2], row[3] if len(row) > 3 else "known",
                                         row[4] if len(row) > 4 else None))
        result = inspector.inspect(plan["cards_per_episode"], ledger)
        require(all(result[k] == expected for k, expected in example["expected"].items()), "probe failed: " + example["id"])
        probe_results.append({"id": example["id"], "label_ko": example["label_ko"], "split": None,
                              "training_use": False, "scoring_use": False, "disposition": result["disposition"]})
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "design catalog only; no performance scores or usable training response bundle",
            "families": families, "world_designs": worlds, "probe_results": probe_results,
            "world_count": len(worlds), "family_count": len(families),
            "split_world_counts": {split: sum(w["split"] == split for w in worlds) for split in plan["split_family_counts"]},
            "plan": plan, "training_ready": False, "independent_evaluation": False,
            "input_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [PLAN, PROBES, SPEC, DEFAULT, Path(__file__), Path(__file__).with_name("semantics.py")]}}


def validate_membership(records):
    """Reusable lineage gate for future generated variants; do not silently reassign."""
    roots, families, tables, root_families = {}, {}, {}, {}
    for row in records:
        split = row["split"]
        require(split in {"train", "val_internal", "test_internal"}, "unknown split")
        require(row["root_world_id"] not in root_families or root_families[row["root_world_id"]] == row["family_id"],
                "parent family changed")
        root_families[row["root_world_id"]] = row["family_id"]
        for mapping, key, label in [(roots, row["root_world_id"], "parent"),
                                    (families, row["family_id"], "family")]:
            require(key not in mapping or mapping[key] == split, label + " crossed splits")
            mapping[key] = split
        # Future variants pass the complete effective response table, not latent
        # answers that are never disclosed after a nonanswer.
        table = row.get("effective_response_table", row.get("environment_only_design_answers"))
        require(table is not None, "effective response table required")
        key = digest([sorted(row["cards"]), table])
        require(key not in tables or tables[key] == split, "duplicate response table crossed splits")
        tables[key] = split


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report_path = args.report.resolve()
    require(ROOT / "outputs" in report_path.parents and not report_path.exists(), "new report inside outputs/ required")
    report = build_design()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("world_count", "family_count", "split_world_counts", "training_ready", "independent_evaluation")}))


if __name__ == "__main__":
    main()
