"""Offline contract checks for the frozen seed. They do not call member APIs."""

import hashlib
import json
import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "KB/Poppy_KB_v0.6.2"
SEED = "Poppy_KB_seed_v0.6.2.json"
PIN = "9460048519930f62dccb0143ea4ba061cf903a71096703ee12ca78e473b44a8d"
evaluate_episode = runpy.run_path(str(RELEASE / "postwash_reference.py"))["evaluate_episode"]
POSTWASH = "after_wash_before_leave_on"
CONTACT = "method.cleanser_contact_mode"
ORDINARY = {
    "population_scope": "adult_face",
    "confirmed_current_face_episode": True,
    "safety_disposition": "ordinary_confirmed",
}
LABEL = {"product.type": "ordinary_rinse_off_cleanser", "product.instructions": "no_special_duration"}
HABIT = {"cleansing.repeat_wash": "same_session_habit_after_removal",
         "cleansing.target_load": "necessary_removal_completed", "product.instructions": "no_extra_cleanse_instruction"}


@pytest.fixture(scope="module")
def seed():
    return json.loads((RELEASE / SEED).read_bytes())


def test_versioned_inputs():
    manifest = json.loads((RELEASE / "MANIFEST.json").read_bytes())
    assert manifest["files"][SEED] == PIN
    for filename, digest in manifest["files"].items():
        assert hashlib.sha256((RELEASE / filename).read_bytes()).hexdigest() == digest
    for role in ("parent", "legacy_comparison"):
        source = manifest[role]
        assert hashlib.sha256((ROOT / source["file"]).read_bytes()).hexdigest() == source["sha256"]


def test_cleanser_diff_and_references(seed):
    manifest = json.loads((RELEASE / "MANIFEST.json").read_bytes())
    parent = json.loads((ROOT / manifest["parent"]["file"]).read_bytes())
    cards = {r["id"]: r for r in seed["baseline_cards"]}
    originals = {r["id"]: r for r in parent["baseline_cards"]}
    assert cards.keys() == originals.keys() and len(cards) == 60
    assert {k for k in cards if cards[k] != originals[k]} == {
        "B-C02", "B-C03", "B-C04", "B-C05", "B-I01", "B-I03", "B-M02"
    }
    assert not seed["metadata"]["production_enabled"]
    assert all(not card["active"] and not card["review"]["production_enabled"] for card in cards.values())
    variables = {r["id"] for r in seed["variables"]}
    assert len(variables) == len(seed["variables"]) == seed["metadata"]["current_counts"]["variables"] == 236
    sources = {r["id"] for r in seed["source_registry"]}
    contract = seed["dryness_concern_contract"]
    assert set(contract["evidence_source_ids"]) <= sources
    for question in contract["candidate_questions"]:
        assert question["card"] in cards
        assert set(question["field_refs"]) <= variables
        assert set(question["sources"]) <= sources
    for change in contract["supported_changes"]:
        assert change["card"] in cards
        fields = set(change["requires"])
        if "skin.dryness_pattern.same_cleanser_recurrence" in fields:
            fields.remove("skin.dryness_pattern.same_cleanser_recurrence")
            pattern = next(v for v in seed["variables"] if v["id"] == "skin.dryness_pattern")
            assert "reported_repeatedly" in pattern["value_shape"]["same_cleanser_recurrence"]
        assert fields <= variables
    original_cases = {c["id"]: c for c in parent["acceptance_scenarios"]}
    cases = {c["id"]: c for c in seed["acceptance_scenarios"]}
    assert cases.keys() - original_cases.keys() == {f"DRY-T{i:02}" for i in range(1, 8)}
    assert set(original_cases) <= cases.keys()
    for key, original in original_cases.items():
        if key == "T03":
            assert cases[key]["facts"] == {**original["facts"], CONTACT: "prolonged_rubbing"}
            assert {**original, "facts": cases[key]["facts"]} == cases[key]
        else:
            assert original == cases[key]
    assert "dose.contact_time" not in cards["B-C03"]["observable_inputs"]
    assert not cards["B-C03"]["numeric_parameters"]
    questions = {q["variable_id"]: q for q in seed["acquisition_items"]}
    assert "B-C03" not in questions["dose.contact_time"]["baseline_card_refs"]
    assert questions[CONTACT]["baseline_card_refs"] == ["B-C03"]
    for feature in (CONTACT, "skin.dryness_pattern"):
        assert questions[feature]["unknown_allowed"] and not questions[feature]["ask_all_users"]


def test_product_specific_removal_attachment(seed):
    card = next(c for c in seed["baseline_cards"] if c["id"] == "B-I01")
    reference = card["removal_reference"]
    content = (RELEASE / reference["file"]).read_bytes()
    assert hashlib.sha256(content).hexdigest() == reference["sha256"]
    removal = json.loads(content)
    assert removal["version"] == reference["version"] == "B-I01-removal-v1"
    drg = removal["reviewed_labels"]["SHEET-SUNSCREEN-SUN-0051-adb1c24a1bbd6b21"]
    assert drg["version"] == "adb1c24a1bbd6b2119303d31f728ff6cea2a393829cb531a4cdbc38ce3acaaf2"
    assert drg["condition"] == "foam_test"


def eligible_changes(seed, facts, *, scope=ORDINARY, phases=(POSTWASH,), product_revision=None):
    target = dict(zip(("id", "version"), product_revision or ()))
    product = {**target, **{k: v for k, v in facts.items() if k.startswith("product.")}}
    report = {"skin.dryness_pattern": {"reported_phases": phases}, **facts}
    result = evaluate_episode(seed, {"scope": scope, "facts": report, "product_ref": target}, product)
    return set(result["actions"])


@pytest.mark.parametrize(("facts", "action"), [
    ({"method.water_temperature": "hot"}, "reduce_hot_water"),
    ({"method.water_temperature": "cold"}, None),
    ({"method.friction": "strong"}, "reduce_rubbing"),
    ({"method.drying": "rub_with_towel"}, "pat_dry"),
    ({"method.drying": "uses_towel"}, None),
    ({**LABEL, CONTACT: "intentional_wait"}, "gently_spread_then_rinse"),
    ({**LABEL, CONTACT: "prolonged_rubbing"}, "gently_spread_then_rinse"),
    ({**LABEL, CONTACT: "spread_then_rinse"}, None),
    ({**LABEL, "dose.contact_time": 180}, None),
    ({"product.type": "special_use_product", "product.instructions": "specific_contact_time", CONTACT: "intentional_wait"}, None),
    ({"product.type": "ordinary_rinse_off_cleanser", CONTACT: "intentional_wait"}, None),
    (HABIT, "omit_habitual_extra_step"),
    ({**HABIT, "cleansing.target_load": "sunscreen_still_to_remove"}, None),
    ({**HABIT, "cleansing.repeat_wash": "after_sweating"}, None),
    ({"cleansing.steps": 2}, None),
    ({"product.ph": 9, "skin.tightness": True}, None),
])
def test_one_episode_action_table(seed, facts, action):
    assert eligible_changes(seed, facts, product_revision=("synthetic-cleanser", "r1")) == ({action} if action else set())


@pytest.mark.parametrize("context", [
    {"scope": {**ORDINARY, "safety_disposition": "hold"}},
    {"scope": {**ORDINARY, "safety_disposition": "unknown"}},
    {"scope": {**ORDINARY, "confirmed_current_face_episode": False}},
    {"scope": {**ORDINARY, "population_scope": "out_of_scope"}},
    {"phases": ("later_in_day",)},
])
def test_observation_alone_cannot_authorize_a_change(seed, context):
    assert not eligible_changes(seed, {"method.water_temperature": "hot"}, **context)


def test_product_label_requires_matched_revision(seed):
    assert not eligible_changes(seed, {**LABEL, CONTACT: "intentional_wait"})
    assert not eligible_changes(seed, HABIT)


def test_relief_preserves_postwash_observation_and_correction_retracts_change(seed):
    case = next(c for c in seed["acceptance_scenarios"] if c["id"] == "DRY-T01")
    facts = case["facts"]
    phases = facts["skin.dryness_pattern"]["reported_phases"]
    assert facts["skin.dryness_pattern"]["after_moisturizer"] == "relieved"
    assert eligible_changes(seed, facts, phases=phases, scope=case["scope_preconditions"]) == {"reduce_hot_water"}
    assert not eligible_changes(seed, {**facts, "method.water_temperature": "lukewarm"}, phases=phases)


@pytest.mark.parametrize("case_id", ["DRY-T04", "DRY-T05", "DRY-T06", "DRY-T07"])
def test_frozen_cross_factor_cases(seed, case_id):
    case = next(c for c in seed["acceptance_scenarios"] if c["id"] == case_id)
    episode = {"scope": case["scope_preconditions"], "facts": case["facts"], "product_ref": case["product_ref"]}
    result = evaluate_episode(seed, episode, case["catalog_fixture"])
    assert result["actions"] == case["expected_candidate_actions"]
    assert result["candidate_fields"] == case["expected_candidate_fields"]
    assert result["product_ph"]["state"] == case["expected_ph_state"]


@pytest.mark.parametrize(("observation", "reported"), [
    ({"state": "verified", "source_type": "official_label", "source_ref": "label", "reported_text": "약알칼리성",
      "reported_category": "mildly_alkaline"}, {"state": "reported", "source_type": "official_label",
      "reported_text": "약알칼리성", "category": "mildly_alkaline"}),
    ({"state": "verified", "source_type": "finished_product_test", "source_ref": "test", "reported_text": "6.1",
      "measurement_conditions": "원액 25°C"}, {"state": "reported", "source_type": "finished_product_test",
                                         "reported_text": "6.1", "measurement_conditions": "원액 25°C"}),
    ({"state": "verified", "source_type": "finished_product_test", "source_ref": "test", "reported_text": "6.1"}, {"state": "unknown"}),
    ({"state": "verified", "source_type": "ingredient_guess", "source_ref": "INCI", "reported_text": "약산성"}, {"state": "unknown"}),
    ({"state": "conflict", "reported_text": "약산성"}, {"state": "conflict"}),
    ({"state": "verified", "source_type": "official_label", "reported_text": "약산성"}, {"state": "unknown"}),
])
def test_ph_evidence_and_independent_behavior(seed, observation, reported):
    target = {"id": "cleanser", "version": "r1"}
    facts = {"skin.dryness_pattern": {"reported_phases": [POSTWASH]}, "method.friction": "strong"}
    result = evaluate_episode(seed, {"scope": ORDINARY, "facts": facts, "product_ref": target},
                              {**target, "product.ph": observation})
    assert result["product_ph"] == reported
    assert result["actions"] == ["reduce_rubbing"]


def test_user_who_skipped_contact_is_not_asked_again(seed):
    case = next(c for c in seed["acceptance_scenarios"] if c["id"] == "DRY-T05")
    episode = {"scope": ORDINARY, "facts": case["facts"], "product_ref": case["product_ref"], "answered_features": [CONTACT]}
    result = evaluate_episode(seed, episode, case["catalog_fixture"])
    assert not result["candidate_fields"] and not result["actions"]


@pytest.mark.parametrize("duration", [
    {"phase": "rinsing", "seconds": 120},
    {"phase": "drying", "seconds": 120},
    {"phase": "before_rinsing", "range_seconds": [100, 5]},
    {"phase": "whole_wash", "seconds": None},
])
def test_rinsing_and_unusable_times_do_not_trigger_contact_questions(seed, duration):
    case = next(c for c in seed["acceptance_scenarios"] if c["id"] == "DRY-T05")
    episode = {"scope": ORDINARY, "facts": {**case["facts"], "dose.contact_time": duration},
               "product_ref": case["product_ref"]}
    result = evaluate_episode(seed, episode, case["catalog_fixture"])
    assert not result["candidate_fields"] and not result["actions"]


def test_comparison_follows_user_request(seed):
    case = next(c for c in seed["acceptance_scenarios"] if c["id"] == "DRY-T06")
    facts = {k: v for k, v in case["facts"].items() if k != "constraints.decision_context"}
    episode = {"scope": ORDINARY, "facts": facts, "product_ref": case["product_ref"]}
    result = evaluate_episode(seed, episode, case["catalog_fixture"])
    assert not result["actions"] and result["candidate_fields"] == ["constraints.decision_context"]


@pytest.mark.parametrize(("product_id", "category", "label"), [
    ("SHEET-CLEANSER-CLN-0165-1883bcd3128a5d04", "mildly_acidic", "약산성 5.5"),
    ("SHEET-CLEANSER-CLN-0315-022ac0403c75bc55", "mildly_alkaline", "약알칼리성"),
])
def test_official_korean_labels_match_only_the_reviewed_catalog_version(seed, product_id, category, label):
    record = seed["dryness_concern_contract"]["product_context"]["reviewed_formulations"][product_id]
    assert product_id.endswith(record["version"][:16]) and len(record["version"]) == 64
    facts = {"skin.dryness_pattern": {"reported_phases": [POSTWASH]}, "method.friction": "strong"}
    episode = {"scope": ORDINARY, "facts": facts, "product_ref": {"id": product_id, "version": record["version"]}}
    result = evaluate_episode(seed, episode)
    assert result["product_ph"] == {"state": "reported", "source_type": "official_label",
                                    "reported_text": label, "category": category}
    assert result["actions"] == ["reduce_rubbing"]
    changed = {**episode, "product_ref": {"id": product_id, "version": "different-revision"}}
    assert evaluate_episode(seed, changed)["product_ph"] == {"state": "unknown"}


def test_conflicting_live_evidence_is_not_replaced_with_an_older_label(seed):
    records = seed["dryness_concern_contract"]["product_context"]["reviewed_formulations"]
    record = next(iter(records.values()))
    episode = {"scope": ORDINARY, "facts": {"skin.dryness_pattern": {"reported_phases": [POSTWASH]}},
               "product_ref": {"id": record["id"], "version": record["version"]}}
    result = evaluate_episode(seed, episode, {**record, "product.ph": {"state": "conflict"}})
    assert result["product_ph"] == {"state": "conflict"} and not result["actions"]
