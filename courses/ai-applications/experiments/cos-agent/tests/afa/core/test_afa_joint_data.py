"""Frozen synthetic answers, response completeness, family boundaries and hashes."""
import shutil

import pytest

from beauty_agent.afa.joint_data import BUNDLE, SPLITS, artifacts, load_joint_split
from beauty_agent.afa.scenario_plan import validate_membership


def test_bundle_rebuilds_byte_for_byte_and_all_families_stay_together():
    for name, text in artifacts().items():
        assert (BUNDLE / name).read_bytes() == text.encode()
    rows = [row for split in SPLITS for row in load_joint_split(split)]
    assert len(rows) == len({r["root_world_id"] for r in rows}) == 48
    validate_membership([{**r, "effective_response_table": r["environment_only"]["response_table"]} for r in rows])
    assert {s: len(load_joint_split(s)) for s in SPLITS} == {"train": 30, "val_internal": 9, "test_internal": 9}
    assert all(len(r["environment_only"]["response_table"]) == 5 and not r["initial_visible_observations"] for r in rows)


def test_corrupt_response_file_fails_before_environment_use(tmp_path):
    shutil.copytree(BUNDLE, tmp_path / "bundle")
    path = tmp_path / "bundle/train.jsonl"
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="bytes drift"):
        load_joint_split("train", tmp_path / "bundle")

