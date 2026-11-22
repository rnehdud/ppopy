"""Keep the new design reproducible and prevent derivative/effective-table leakage."""
from copy import deepcopy
import json

import pytest

from beauty_agent.afa.scenario_plan import PLAN, build_design, validate_membership


@pytest.fixture(scope="module")
def design():
    return build_design()


def test_joint_world_design_and_cost_limits(design):
    assert design["world_count"] == 48 and design["family_count"] == 16
    assert design["split_world_counts"] == {"train": 30, "val_internal": 9, "test_internal": 9}
    for split in design["split_world_counts"]:
        worlds = [w for w in design["world_designs"] if w["split"] == split]
        assert {w["environment_only_design_answers"]["method.water_temperature"] for w in worlds} == {"cold", "lukewarm", "hot"}
    assert design["plan"]["cost_protocols"]["unit_primary"]["max_acquisition_cost"] == 5
    assert design["plan"]["cost_protocols"]["weighted_sensitivity"]["max_acquisition_cost"] == 7
    assert not design["training_ready"] and not design["independent_evaluation"]


def test_split_is_stable_under_dictionary_field_reordering(design):
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    plan["split_family_counts"] = dict(reversed(list(plan["split_family_counts"].items())))
    repeated = build_design(plan)
    assert repeated["families"] == design["families"]
    assert repeated["world_designs"] == design["world_designs"]


def test_probes_cover_nonanswers_correction_and_stay_outside_splits(design):
    assert len(design["probe_results"]) == 9
    assert {r["disposition"] for r in design["probe_results"]} == {
        "draft_ready", "needs_information", "insufficient_information_hold", "conflict_hold"}
    assert all(r["split"] is None and not r["training_use"] and not r["scoring_use"] for r in design["probe_results"])


def test_derived_world_cannot_move_to_another_split(design):
    parent = deepcopy(design["world_designs"][0])
    derivative = deepcopy(parent)
    derivative["split"] = "train" if parent["split"] != "train" else "test_internal"
    with pytest.raises(ValueError, match="parent crossed"):
        validate_membership([parent, derivative])


def test_water_variants_in_same_method_family_cannot_cross_splits(design):
    parent = deepcopy(design["world_designs"][0])
    variant = next(deepcopy(w) for w in design["world_designs"] if w["family_id"] == parent["family_id"] and w["root_world_id"] != parent["root_world_id"])
    variant["split"] = "train" if parent["split"] != "train" else "test_internal"
    with pytest.raises(ValueError, match="family crossed"):
        validate_membership([parent, variant])


def test_hidden_different_answers_do_not_hide_duplicate_effective_responses(design):
    a = deepcopy(design["world_designs"][0])
    b = next(deepcopy(w) for w in design["world_designs"] if w["split"] != a["split"])
    a["effective_response_table"] = {"method.tools": {"state": "unknown", "value": None}}
    b["effective_response_table"] = deepcopy(a["effective_response_table"])
    b["cards"] = list(reversed(b["cards"]))
    with pytest.raises(ValueError, match="duplicate response table"):
        validate_membership([a, b])


def test_wrong_exit_cost_cannot_be_cheaper_than_full_acquisition():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    plan["cost_protocols"]["unit_primary"]["incorrect_terminal_loss"] = 1
    with pytest.raises(ValueError, match="wrong-exit"):
        build_design(plan)


def test_design_cannot_be_presented_as_ready_for_training():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    plan["readiness"]["training_bundle_generated"] = True
    with pytest.raises(ValueError, match="not an implemented"):
        build_design(plan)
