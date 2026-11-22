"""Reproducible response-complete bundle for the frozen 48-world joint task."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .scenario_plan import PLAN, PROBES, build_design, validate_membership, digest
from .semantics import SPEC, SemanticInspector, event
from .stage0 import DEFAULT, ROOT, require
from .stage1 import encode

BUNDLE = PLAN.parent.parent / "joint-v2-v1"
SPLITS = ("train", "val_internal", "test_internal")


def artifacts():
    design, inspector = build_design(), SemanticInspector()
    rows = {split: [] for split in SPLITS}
    for world in design["world_designs"]:
        answers = world["environment_only_design_answers"]
        ledger = inspector.ledger([event("full:" + slot, slot, value) for slot, value in answers.items()])
        result = inspector.inspect(world["cards"], ledger)
        require(not result["research_question_requirements"], "incomplete full-world reference")
        rows[world["split"]].append({"root_world_id": world["root_world_id"], "family_id": world["family_id"],
            "split": world["split"], "cards": world["cards"], "initial_visible_observations": {},
            "human_review": "unreviewed", "approved_reference": False,
            "environment_only": {"response_table": {slot: row.model_dump() for slot, row in ledger.observations.items()},
                "reference": result["current_signature"],
                "reference_terminal": "request_draft" if result["draft_permitted_by_contract"] else "hold"}})
    files = {split + ".jsonl": "".join(encode(row) + "\n" for row in rows[split]) for split in SPLITS}
    paths = [PLAN, PROBES, SPEC, DEFAULT, Path(__file__), Path(__file__).with_name("semantics.py"),
             Path(__file__).with_name("scenario_plan.py")]
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    hashes.update(inspector.base["source_hashes"])
    manifest = {"version": "afa-joint-response-v2-0.1", "mode": "development_preview", "production_enabled": False,
                "source_hashes": hashes, "split_counts": design["split_world_counts"],
                "family_assignment": design["families"], "preinspected_synthetic_domains": True,
                "independent_evaluation": False, "human_review": "unreviewed", "approved_reference": False,
                "scope": "known-answer synthetic execution bundle; no expert approval or v67 derivation",
                "files": {name: hashlib.sha256(text.encode()).hexdigest() for name, text in files.items()}}
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return files


def load_joint_split(split, bundle=BUNDLE):
    require(split in SPLITS, "unknown joint split")
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    require(manifest["mode"] == "development_preview" and manifest["production_enabled"] is False and
            not manifest["approved_reference"] and not manifest["independent_evaluation"], "inactive development bundle required")
    for relative, expected in manifest["source_hashes"].items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, "bundle source drift: " + relative)
    raw = (bundle / (split + ".jsonl")).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == manifest["files"][split + ".jsonl"], "joint split bytes drift")
    records = [json.loads(line) for line in raw.decode().splitlines() if line]
    require(len(records) == manifest["split_counts"][split], "joint split count mismatch")
    inspector = SemanticInspector()
    family_splits = {row["family_id"]: row["split"] for row in manifest["family_assignment"]}
    for row in records:
        require(row["split"] == split and row["initial_visible_observations"] == {}, "split/public input mismatch")
        table = row["environment_only"]["response_table"]
        require(set(table) == set(inspector.domains), "missing response slot")
        require(all(key == value["variable_id"] for key, value in table.items()), "response key mismatch")
        inspector.ledger([{"event_id": slot, "slot": value} for slot, value in table.items()])
        require(all(slot["state"] == "known" for slot in table.values()), "core bundle must be known-answer")
        values = {key: slot["value"] for key, slot in table.items()}
        require(row["root_world_id"] == digest(values) and
                row["family_id"] == digest({key: values[key] for key in ("method.tools", "method.friction", "method.drying")}) and
                family_splits.get(row["family_id"]) == split and row["cards"] == ["B-C01", "B-C02"], "root/family membership mismatch")
    require(len({row["root_world_id"] for row in records}) == len(records), "duplicate joint world")
    validate_membership([{**r, "effective_response_table": r["environment_only"]["response_table"]} for r in records])
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    args = parser.parse_args()
    files = artifacts()
    if args.command == "build":
        require(not any((BUNDLE / name).exists() for name in files), "joint bundle already exists")
        BUNDLE.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            with (BUNDLE / name).open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
    for name, content in files.items():
        require((BUNDLE / name).read_bytes() == content.encode(), "joint bundle drift: " + name)
    print(json.dumps({"verified": True, "split_counts": {s: len(load_joint_split(s)) for s in SPLITS}}))


if __name__ == "__main__":
    main()
