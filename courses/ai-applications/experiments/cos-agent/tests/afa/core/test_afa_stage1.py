"""Data-contract and leakage checks, not policy evaluation."""
from copy import deepcopy
import json

import pytest

from beauty_agent.afa.stage0 import DEFAULT, audit
from beauty_agent.afa.stage1 import (BUNDLE, SPLITS, artifacts, inspect_scenario,
                                    standalone_records, validate_partition, verify_bundle,
                                    world_key, write_bundle)


@pytest.fixture(scope="module")
def prepared():
    contract = json.loads(DEFAULT.read_text(encoding="utf-8"))
    report = audit(contract)
    return contract, report


def source_example(contract):
    return {"card_ids": ["B-C01"], "initial_request": deepcopy(contract["initial_request"]),
            "turns": [{"user_events": {"observations": {
                k: {"variable_id": k, "state": "known", "value": v,
                    "source": "synthetic_fixture", "confirmed_by_user": True}
                for k, v in {"method.body_site": "face", "method.water_temperature": "hot"}.items()}}}]}


def inspect(scenario, prepared):
    contract, report = prepared
    worlds = {world_key(w["card"], w["hidden_synthetic_answers"]): w for w in report["worlds"]}
    return inspect_scenario(scenario, contract, worlds)


def test_missing_response_stays_missing(prepared):
    scenario = source_example(prepared[0])
    assert inspect(scenario, prepared) == []
    del scenario["turns"][0]["user_events"]["observations"]["method.water_temperature"]
    before = deepcopy(scenario)
    assert "missing_response" in inspect(scenario, prepared)
    assert scenario == before


def test_multi_turn_correction_never_becomes_static_profile(prepared):
    scenario = source_example(prepared[0])
    correction = deepcopy(scenario["turns"][0])
    correction["user_events"]["observations"]["method.water_temperature"]["value"] = "cold"
    scenario["turns"].append(correction)
    assert "multiple_turns_need_event_model" in inspect(scenario, prepared)


def test_source_product_identity_is_not_replaced(prepared):
    scenario = source_example(prepared[0])
    scenario["initial_request"]["products"][0]["product_id"] = "train-foam-cleanser-a"
    assert "initial_context_not_stage0_fixture" in inspect(scenario, prepared)
    assert scenario["initial_request"]["products"][0]["product_id"] == "train-foam-cleanser-a"


@pytest.mark.parametrize("state", ["unknown", "declined", "conflicting"])
def test_nonknown_responses_not_promoted(prepared, state):
    scenario = source_example(prepared[0])
    scenario["turns"][0]["user_events"]["observations"]["method.water_temperature"].update(state=state, value=None)
    assert "unsupported_response_state_value_or_time" in inspect(scenario, prepared)


def test_world_and_parent_have_one_split(prepared):
    records = standalone_records(prepared[1])
    assert {s: len(r) for s, r in records.items()} == {"train": 6, "val_internal": 2, "test_internal": 2}
    assert all({r["environment_only"]["card_id"] for r in rows} == {"B-C01", "B-C02"}
               for rows in records.values())
    assert records == standalone_records(prepared[1])
    broken = deepcopy(records)
    copied = deepcopy(broken["train"][0])
    copied["split"] = "test_internal"
    broken["test_internal"].append(copied)
    with pytest.raises(ValueError, match="duplicate response world"):
        validate_partition(broken)


def test_private_answers_cannot_be_initial_observations(prepared):
    records = standalone_records(prepared[1])
    records["train"][0]["initial_visible_observations"] = {"method.body_site": "face"}
    with pytest.raises(ValueError, match="hidden responses"):
        validate_partition(records)


def test_fixed_bundle_reproduces_and_tamper_is_rejected(tmp_path):
    files, report = artifacts()
    assert len(report["scenarios"]) == 1025
    assert sum(report["counts"].values()) == 1025
    verify_bundle(files, BUNDLE)
    write_bundle(files, tmp_path)
    with pytest.raises(ValueError, match="already exists"):
        write_bundle(files, tmp_path)
    path = tmp_path / "train.jsonl"
    path.write_text(path.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="bundle drift"):
        verify_bundle(files, tmp_path)
