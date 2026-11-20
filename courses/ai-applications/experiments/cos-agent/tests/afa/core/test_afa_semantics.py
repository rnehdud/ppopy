"""V2 contract diagnostics do not change KB semantics or dispatch new actions."""
from copy import deepcopy

import pytest

from beauty_agent.afa.semantics import EventLedger, SemanticInspector, event, verify_contract


@pytest.fixture(scope="module")
def inspector():
    return SemanticInspector()


def face(inspector):
    return inspector.ledger([event("site", "method.body_site", "face")])


def test_friction_shortcut_requires_tool_precedence_check(inspector):
    ledger = face(inspector).append(event("friction", "method.friction", "strong"))
    result = inspector.inspect(["B-C02"], ledger)
    assert result["runtime_draft_enabled"] is True
    assert result["semantic_certificate"] is False
    assert not result["draft_permitted_by_contract"]
    assert result["possible_signature_count"] == 2
    assert result["research_question_requirements"] == ["method.tools"]
    assert result["adapter_extension_required"] == ["method.tools"]
    known = ledger.append(event("tools", "method.tools", "hands"))
    assert inspector.inspect(["B-C02"], known)["draft_permitted_by_contract"]


def test_dominating_tools_difference_needs_no_irrelevant_answers(inspector):
    ledger = face(inspector).append(event("tools", "method.tools", "scrub_brush"))
    result = inspector.inspect(["B-C02"], ledger)
    assert result["draft_permitted_by_contract"]
    assert result["current_signature"]["cards"][0]["actions"] == ["inform_general_practice"]
    assert result["research_question_requirements"] == []
    assert result["possible_completion_count"] == 4


@pytest.mark.parametrize("state", ["unknown", "declined"])
def test_nonanswer_preserved_without_reask_or_false_value(inspector, state):
    ledger = face(inspector).append(event("friction", "method.friction", "strong"))
    ledger = ledger.append(event("tools", "method.tools", state=state))
    result = inspector.inspect(["B-C02"], ledger)
    assert result["response_states"]["method.tools"] == state
    assert "method.tools" not in result["public_known_values"]
    assert result["research_question_requirements"] == []
    assert result["disposition"] == "insufficient_information_hold"
    assert not result["draft_permitted_by_contract"]


def test_irrelevant_decline_does_not_manufacture_a_required_question(inspector):
    ledger = face(inspector).append(event("tools", "method.tools", "scrub_brush"))
    ledger = ledger.append(event("friction", "method.friction", state="declined"))
    assert inspector.inspect(["B-C02"], ledger)["draft_permitted_by_contract"]
    assert ledger.observations["method.friction"].value is None


def test_body_site_gate_and_conflict_never_open_draft(inspector):
    result = inspector.inspect(["B-C02"], inspector.ledger())
    assert result["research_question_requirements"] == ["method.body_site"]
    declined = inspector.ledger([event("site", "method.body_site", state="declined")])
    assert inspector.inspect(["B-C02"], declined)["research_question_requirements"] == []
    conflict = face(inspector).append(event("tools", "method.tools", "scrub_brush"))
    conflict = conflict.append(event("friction", "method.friction", state="conflicting"))
    result = inspector.inspect(["B-C02"], conflict)
    assert result["disposition"] == "conflict_hold" and not result["draft_permitted_by_contract"]


def test_correction_invalidates_old_token_and_preserves_prior_event(inspector):
    ledger = face(inspector).append(event("tools1", "method.tools", "scrub_brush"))
    ledger = ledger.append(event("friction", "method.friction", "strong"))
    before = inspector.inspect(["B-C02"], ledger)
    corrected = ledger.append(event("tools2", "method.tools", "hands", supersedes="tools1"))
    after = inspector.inspect(["B-C02"], corrected)
    with pytest.raises(ValueError, match="stale"):
        inspector.require_fresh(before["public_token"], ["B-C02"], corrected)
    assert after["current_signature"]["cards"][0]["actions"] == ["suggest_behavior_change"]
    assert ledger.observations["method.tools"].value == "scrub_brush"
    assert corrected.events[-1]["supersedes"] == "tools1"
    assert len(corrected.events) == len(ledger.events) + 1


def test_ledger_rejects_silent_correction_undefined_nonanswer_and_products(inspector):
    ledger = face(inspector)
    for invalid in [event("site2", "method.body_site", "face"),
                    event("other", "method.tools", "hands", state="unknown"),
                    event("product", "product.instructions", "anything")]:
        with pytest.raises(ValueError):
            ledger.append(invalid)
    assert len(ledger.events) == 1


def test_no_external_ledger_can_inject_out_of_domain_fact(inspector):
    forged = EventLedger({"method.body_site": ["unrecognized"]}, [event("x", "method.body_site", "unrecognized")])
    with pytest.raises(ValueError, match="domain"):
        inspector.inspect(["B-C02"], forged)


def test_public_certificate_invariant_to_question_order(inspector):
    first = face(inspector).append(event("t", "method.tools", "hands")).append(event("f", "method.friction", "strong"))
    second = face(inspector).append(event("f", "method.friction", "strong")).append(event("t", "method.tools", "hands"))
    one, two = (inspector.inspect(["B-C02"], ledger) for ledger in [first, second])
    assert one["draft_permitted_by_contract"] == two["draft_permitted_by_contract"] == True
    assert one["current_signature"] == two["current_signature"]
    assert one["public_token"] != two["public_token"]  # event identity still invalidates stale snapshots


def test_joint_card_means_all_card_signatures_not_one_success(inspector):
    ledger = face(inspector).append(event("tools", "method.tools", "scrub_brush"))
    result = inspector.inspect(["B-C01", "B-C02"], ledger)
    assert not result["draft_permitted_by_contract"]
    assert result["research_question_requirements"] == ["method.water_temperature"]
    ledger = ledger.append(event("water", "method.water_temperature", "hot"))
    assert inspector.inspect(["B-C02", "B-C01"], ledger)["draft_permitted_by_contract"]


def test_explicit_required_information_cannot_be_skipped(inspector):
    other = SemanticInspector()
    other.spec["required_slots"] = ["method.friction"]  # test-only structural requirement, no clinical label
    ledger = face(other).append(event("tools", "method.tools", "scrub_brush"))
    result = other.inspect(["B-C02"], ledger)
    assert result["semantic_certificate"]
    assert not result["draft_permitted_by_contract"]
    assert result["research_question_requirements"] == ["method.friction"]
    ledger = ledger.append(event("friction", "method.friction", state="declined"))
    assert other.inspect(["B-C02"], ledger)["disposition"] == "insufficient_information_hold"


def test_original_grid_including_nine_exclusions_keeps_exact_full_meaning():
    result = verify_contract()
    assert result["worlds"] == 19 and result["priority_paths"] == 99
    assert result["previously_excluded_worlds"] == 9
    assert len(result["mixed_world_paths"]) == 54
    assert not result["runtime_integrated"] and not result["training_data_generated"]
