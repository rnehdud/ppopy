"""Specification checks, not an AFA policy score or independent reference labels."""
from copy import deepcopy
import json

import pytest

from beauty_agent.afa.stage0 import DEFAULT, audit, check_examples, snapshot, task_offers
from beauty_agent.actions import ActionProposal
from beauty_agent.action_runtime import validate_action
from beauty_agent.modules.kb_adapter import KBEngineAdapter


@pytest.fixture(scope="module")
def spec():
    return json.loads(DEFAULT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def report(spec):
    return audit(spec)


def test_branch_order_ambiguity_is_excluded_not_relabeled(report):
    assert report["summary"] == {"eligible": 10, "B-C01:eligible": 3,
                                 "B-C02:eligible": 7, "excluded_semantic_variation": 9,
                                 "B-C02:excluded": 9}
    mixed = next(w for w in report["worlds"] if w["hidden_synthetic_answers"] == {
        "method.body_site": "face", "method.tools": "scrub_brush",
        "method.friction": "strong", "method.drying": "pat_gently"})
    assert not mixed["eligible"]
    assert any(not p["signature_matches_full"] for p in mixed["paths"])


def test_authored_paths_and_premature_hold_cost(spec, report):
    examples = json.loads(DEFAULT.with_name("examples.synthetic.json").read_text(encoding="utf-8"))
    assert check_examples(spec, report, examples) == 8
    broken = deepcopy(examples)
    broken["examples"][6]["expected_return"] = 0
    with pytest.raises(ValueError, match="return mismatch"):
        check_examples(spec, report, broken)


def test_scope_restriction_never_widens_engine_gate(spec):
    adapter = KBEngineAdapter()
    initial, _ = snapshot(spec, "B-C02", {}, adapter)
    assert [(a.action, a.target_id) for a in task_offers(spec, initial)
            if a.action == "ask_user"] == [("ask_user", "method.body_site")]
    with pytest.raises(ValueError, match="execution_conditions_not_met"):
        validate_action(ActionProposal(action="request_draft", target_id="label_draft"), initial)
    face, _ = snapshot(spec, "B-C02", {"method.body_site": "face"}, adapter)
    assert {a.target_id for a in task_offers(spec, face) if a.action == "ask_user"} == {
        "method.tools", "method.friction", "method.drying"}
    assert any(a.action == "retrieve_evidence" for a in face.enabled())
    assert all(a.action != "retrieve_evidence" for a in task_offers(spec, face))


@pytest.mark.parametrize("change,message", [
    (lambda c: c.update(production_enabled=True), "inactive"),
    (lambda c: c["objective"].update(gamma=0.99), "total cost"),
    (lambda c: c["objective"].update(incorrect_terminal_loss=1), "wrong exit"),
    (lambda c: c["observation_schema"].update(dimension=57), "dimension"),
    (lambda c: c["action_dictionary"].pop(), "action dictionary"),
    (lambda c: c["source_hashes"].update({"skin_engine/kb_preview/rules.json": "0" * 64}), "source drift"),
])
def test_contract_cannot_silently_change(spec, change, message):
    modified = deepcopy(spec)
    change(modified)
    with pytest.raises(ValueError, match=message):
        audit(modified)
