"""Response-complete synthetic development bundle and conservative v67 reuse audit."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from data.action_policy.v67.dataset_cli import SPLIT_FILES, read_rows, verify as verify_v67
from .stage0 import DEFAULT, EXPERIMENT, ROOT, audit, require

V67 = EXPERIMENT / "data/action_policy/v67"
BUNDLE = EXPERIMENT / "data/afa/stage1-v1"
SPLITS = ("train", "val_internal", "test_internal")


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def world_key(card, answers):
    return sha(encode({"card": card, "answers": answers}))


def inspect_scenario(scenario, contract, worlds):
    """Never merge later events or rewrite source product/profile identities."""
    reasons = set()
    cards = scenario["card_ids"]
    if len(cards) != 1 or cards[0] not in contract["tasks"]:
        return ["outside_fixed_single_card_scope"]
    card = cards[0]
    request = scenario["initial_request"]
    initial = contract["initial_request"]
    if (request.get("profile") != initial["profile"] or
            request.get("products") != initial["products"] or
            request.get("deployment_context") != "synthetic_test"):
        reasons.add("initial_context_not_stage0_fixture")
    turns = scenario["turns"]
    if len(turns) != 1:
        reasons.add("multiple_turns_need_event_model")
        return sorted(reasons)
    turn = turns[0]
    fixture = turn.get("extraction_fixture", {})
    if turn.get("candidate_aliases") or any(fixture.get(k) for k in ("symptoms", "products", "clarifications")):
        reasons.add("candidate_or_extraction_contract_required")
    events = turn.get("user_events", {})
    if set(events) - {"observations"}:
        reasons.add("unsupported_non_observation_event")
    observations = events.get("observations", {})
    domains = contract["tasks"][card]["world_domains"]
    if set(observations) - set(domains):
        reasons.add("observations_outside_task_scope")
    answers = {}
    for key, domain in domains.items():
        slot = observations.get(key)
        if slot is None:
            reasons.add("missing_response")
        elif (slot.get("variable_id") != key or slot.get("state") != "known" or
              slot.get("confirmed_by_user") is not True or slot.get("source") != "synthetic_fixture" or
              slot.get("value") not in domain or "observed_at" in slot):
            reasons.add("unsupported_response_state_value_or_time")
        else:
            answers[key] = slot["value"]
    if len(answers) == len(domains):
        match = worlds.get(world_key(card, answers))
        if match is None or not match["eligible"]:
            reasons.add("branch_semantic_variation")
    return sorted(reasons)


def v67_audit(contract, stage0_report):
    integrity = verify_v67(V67)
    sources = read_rows(V67 / "canonical-candidates-v67.jsonl")
    membership = {}
    for split, filename in SPLIT_FILES.items():
        for row in read_rows(V67 / filename):
            sid = row["scenario_id"]
            require(sid not in membership or membership[sid] == split, "parent crosses source splits")
            membership[sid] = split
    worlds = {world_key(w["card"], w["hidden_synthetic_answers"]): w for w in stage0_report["worlds"]}
    rows = []
    counts = Counter()
    by_split = {split: Counter() for split in SPLITS}
    fingerprint_splits = {}
    for scenario in sources:
        reasons = inspect_scenario(scenario, contract, worlds)
        split = membership[scenario["scenario_id"]]
        row = {"scenario_id": scenario["scenario_id"], "source_pool_split": scenario["split"],
               "effective_split": split, "group_id": scenario["group_id"],
               "scenario_family_id": scenario["scenario_family_id"],
               "product_family_id": scenario["product_family_id"],
               "derived_from": scenario.get("derived_from", []),
               "eligible_unchanged": not reasons, "reasons": reasons}
        if not reasons:
            card = scenario["card_ids"][0]
            obs = scenario["turns"][0]["user_events"]["observations"]
            key = world_key(card, {k: obs[k]["value"] for k in contract["tasks"][card]["world_domains"]})
            row["world_fingerprint"] = key
            fingerprint_splits.setdefault(key, set()).add(split)
        rows.append(row)
        key = "eligible_unchanged" if not reasons else "excluded"
        counts[key] += 1
        by_split[split][key] += 1
    reason_counts = Counter(reason for row in rows for reason in row["reasons"])
    return {"integrity": integrity, "counts": dict(counts),
            "by_effective_split": {s: dict(c) for s, c in by_split.items()},
            "reason_counts_nonexclusive": dict(sorted(reason_counts.items())),
            "cross_split_supported_world_collisions": sum(len(s) > 1 for s in fingerprint_splits.values()),
            "scope": "Unchanged-source compatibility only. Multi-turn events are not flattened. No v67 rows exported to the standalone grid bundle.",
            "scenarios": rows}


def standalone_records(stage0_report):
    """Split complete design worlds, not turns/paths; no source v67 lineage claim."""
    result = {s: [] for s in SPLITS}
    cards = sorted({w["card"] for w in stage0_report["worlds"]})
    for card in cards:
        eligible = [w for w in stage0_report["worlds"] if w["eligible"] and w["card"] == card]
        eligible.sort(key=lambda w: world_key(card, w["hidden_synthetic_answers"]))
        require(len(eligible) >= 3, "need at least three worlds per card")
        # Frozen rule: first hash -> val, second -> test, remaining -> train.
        # Outcome/action labels and source v67 test membership are not consulted.
        for i, world in enumerate(eligible):
            split = "val_internal" if i == 0 else "test_internal" if i == 1 else "train"
            fingerprint = world_key(card, world["hidden_synthetic_answers"])
            result[split].append({
                "id": "afa-static-v1-" + fingerprint, "split": split,
                "parent_world_id": world["world_id"], "world_fingerprint": fingerprint,
                "lineage": {"source": "stage0-v1-synthetic-design-grid", "v67_parent": None,
                            "note": "No source scenario events or product identity were rewritten."},
                "initial_visible_observations": {},
                "environment_only": {
                    "card_id": card,
                    "response_table": {key: {"variable_id": key, "state": "known", "value": value,
                                             "source": "synthetic_fixture", "confirmed_by_user": True}
                                       for key, value in world["hidden_synthetic_answers"].items()},
                    "reference": world["reference"], "reference_terminal": world["reference_terminal"]},
                "provenance": {"synthetic": True, "human_review": "unreviewed",
                               "approved_reference": False, "training_ready": False,
                               "purpose": "response-complete environment development; not an independent holdout"}})
    validate_partition(result)
    return result


def validate_partition(records):
    owners = {}
    parents = {}
    for split, rows in records.items():
        require(split in SPLITS, "unknown split")
        for row in rows:
            require(row["split"] == split, "record split mismatch")
            env = row["environment_only"]
            fingerprint = world_key(env["card_id"], {k: v["value"] for k, v in env["response_table"].items()})
            require(row["world_fingerprint"] == fingerprint, "world fingerprint mismatch")
            require(fingerprint not in owners, "duplicate response world across records/splits")
            require(row["parent_world_id"] not in parents, "parent duplicated across records/splits")
            owners[fingerprint] = split
            parents[row["parent_world_id"]] = split
            require(row["initial_visible_observations"] == {}, "hidden responses initially exposed")


def artifacts(contract_path=DEFAULT):
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    stage0_report = audit(contract)
    source_report = v67_audit(contract, stage0_report)
    records = standalone_records(stage0_report)
    files = {split + ".jsonl": "".join(encode(r) + "\n" for r in records[split]) for split in SPLITS}
    manifest = {
        "version": "afa-stage1-v1", "mode": "development_preview", "production_enabled": False,
        "contract_sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "stage0_checker_sha256": hashlib.sha256(Path(__file__).with_name("stage0.py").read_bytes()).hexdigest(),
        "source_audit_inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                [V67 / "canonical-candidates-v67.jsonl", V67 / "v67-sft-manifest.json"] +
                                [V67 / f for f in SPLIT_FILES.values()]},
        "origin": "standalone_stage0_design_grid_not_v67_derived",
        "split_rule": "within each card sort canonical response-world SHA256; first=val, second=test, rest=train",
        "split_unit": "whole world; all future question orders/repetitions/variants inherit parent split",
        "split_counts": {s: len(rows) for s, rows in records.items()},
        "split_cards": {s: dict(Counter(r["environment_only"]["card_id"] for r in rows)) for s, rows in records.items()},
        "files": {name: {"sha256": sha(content), "bytes": len(content.encode("utf-8"))} for name, content in files.items()},
        "stage0_eligibility": stage0_report["summary"],
        "v67_unchanged_compatibility": {k: v for k, v in source_report.items() if k != "scenarios"},
        "review": {"human_review": "unreviewed", "approved_reference": False, "training_ready": False},
        "limitations": ["10 small pre-inspected design worlds, not an unseen external test",
                        "No guarantee of semantic-family/product-family separation; same rule/product/template pool",
                        "No model selection or generalization claim from this bundle",
                        "environment_only responses/reference/IDs/provenance must not enter policy observations",
                        "No Gym environment, NLP, product retrieval or RL training implemented"]}
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return files, source_report


def write_bundle(files, destination):
    require(not any((destination / name).exists() for name in files), "bundle already exists; verify or use a new path")
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        with (destination / name).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)


def verify_bundle(files, destination):
    for name, expected in files.items():
        require((destination / name).read_bytes() == expected.encode("utf-8"), "bundle drift: " + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--bundle", type=Path, default=BUNDLE)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    files, report = artifacts()
    if args.command == "build":
        write_bundle(files, args.bundle)
    verify_bundle(files, args.bundle)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"v67": report["counts"], "standalone_splits": json.loads(files["manifest.json"])["split_counts"]}))


if __name__ == "__main__":
    main()
