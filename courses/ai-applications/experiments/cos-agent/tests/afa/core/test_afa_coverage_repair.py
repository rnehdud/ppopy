"""Coverage repair is deterministic, disjoint and explicitly not an unseen test."""
from copy import deepcopy
import json
import shutil

import pytest

from beauty_agent.afa.coverage_repair import (BUNDLE, PARTITION, artifacts, coverage_audit, repaired_records)
from beauty_agent.afa.joint_data import BUNDLE as ORIGINAL, SPLITS, load_joint_split


@pytest.fixture(scope="module")
def records():
    return [row for split in SPLITS for row in load_joint_split(split)]


@pytest.fixture(scope="module")
def partition():
    return json.loads(PARTITION.read_text(encoding="utf-8"))


def test_original_gap_is_detected_without_hiding_it(records):
    report = coverage_audit(records)
    assert report["splits"]["train"]["stratum_families"]["hands"] == 4
    assert report["splits"]["val_internal"]["missing_required_strata"] == ["hands"]
    assert report["splits"]["test_internal"]["missing_required_strata"] == ["hands"]
    assert not report["required_strata_present_everywhere"]


def test_repaired_partition_has_both_structural_types_everywhere(records, partition):
    report = coverage_audit(repaired_records(records, partition))
    assert report["required_strata_present_everywhere"]
    assert {s: report["splits"][s]["worlds"] for s in SPLITS} == {"train": 30, "val_internal": 9, "test_internal": 9}
    assert {s: report["splits"][s]["stratum_families"]["hands"] for s in SPLITS} == {"train": 2, "val_internal": 1, "test_internal": 1}
    assert all(report["splits"][s]["water_values"] == ["cold", "hot", "lukewarm"] for s in SPLITS)


def test_responses_references_and_roots_are_not_reinvented(records, partition):
    repaired = {r["root_world_id"]: r for r in repaired_records(records, partition)}
    assert len(repaired) == len(records) == 48
    for row in records:
        revised = repaired[row["root_world_id"]]
        assert revised["environment_only"] == row["environment_only"]
        assert revised["family_id"] == row["family_id"]
        assert revised["prior_split"] == row["split"]
        assert revised["origin_bundle"] == "joint-v2-v1"


def test_impossible_full_coverage_is_reported_instead_of_duplicating_singleton(records, partition):
    report = coverage_audit(repaired_records(records, partition))
    checks = report["feasibility_checks"]
    assert not checks["every_tool_value_in_every_split"]["feasible"]
    assert not checks["aligned_method_family_in_every_split"]["feasible"]
    assert checks["aligned_method_family_in_every_split"]["family_count"] == 1
    assert len(checks["aligned_method_family_in_every_split"]["current_splits"]) == 1
    assert report["independent_evaluation"] is False


def test_assignment_does_not_depend_on_input_or_dictionary_order(records, partition):
    expected = {r["root_world_id"]: r["split"] for r in repaired_records(records, partition)}
    changed = deepcopy(partition)
    changed["strata"] = dict(reversed(list(changed["strata"].items())))
    for key in changed["strata"]:
        changed["strata"][key] = dict(reversed(list(changed["strata"][key].items())))
    actual = {r["root_world_id"]: r["split"] for r in repaired_records(list(reversed(records)), changed)}
    assert actual == expected


def test_rebuild_matches_files_and_existing_loader_accepts_new_version():
    files, report = artifacts()
    for name, text in files.items():
        assert (BUNDLE / name).read_bytes() == text.encode()
    assert all(report["preservation"].values())
    assert not report["independent_evaluation_ready"] and not report["policy_performance_evaluated"]
    assert {s: len(load_joint_split(s, BUNDLE)) for s in SPLITS} == {"train": 30, "val_internal": 9, "test_internal": 9}
    assert ORIGINAL != BUNDLE


def test_corrupt_new_partition_file_is_rejected(tmp_path):
    shutil.copytree(BUNDLE, tmp_path / "bundle")
    path = tmp_path / "bundle/val_internal.jsonl"
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="bytes drift"):
        load_joint_split("val_internal", tmp_path / "bundle")


def test_repair_cannot_claim_policy_scoring_or_independent_evaluation(records, partition):
    modified = deepcopy(partition)
    modified["independent_evaluation"] = True
    with pytest.raises(ValueError, match="internal-only"):
        repaired_records(records, modified)
    modified = deepcopy(partition)
    modified["policy_scoring_authorized_in_this_step"] = True
    with pytest.raises(ValueError, match="not a performance experiment"):
        repaired_records(records, modified)


def test_changing_declared_quota_requires_new_design(records, partition):
    modified = deepcopy(partition)
    modified["strata"]["hands"] = {"train": 4, "val_internal": 0, "test_internal": 0}
    with pytest.raises(ValueError, match="fixed structural quotas"):
        repaired_records(records, modified)

