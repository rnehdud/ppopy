"""Actual v2 dispatch, pending input and original-gate preservation."""
import asyncio
from dataclasses import replace
import json

import pytest

from beauty_agent.actions import ActionProposal
from beauty_agent.afa import joint_runtime
from beauty_agent.afa.joint_runtime import JointSessionAdapter, diagnostic
from beauty_agent.afa.scenario_plan import PROBES
from beauty_agent.afa.semantics import event


def friction_first():
    runtime = JointSessionAdapter()
    prepared = runtime.prepare_context([event("site", "method.body_site", "face"),
        event("water", "method.water_temperature", "hot"), event("friction", "method.friction", "strong")])
    return runtime, prepared


def test_tools_extension_dispatches_and_original_context_is_unchanged():
    runtime, prepared = friction_first()
    assert diagnostic(prepared)["adapter_extension_required"] == ["method.tools"]
    assert not runtime.state.confirmed_observations
    assert not any(a.action == "ask_user" and a.target_id == "method.tools" for a in
                   runtime.inspector._evaluate(["B-C01", "B-C02"], prepared.context.observations)[1].enabled())
    with pytest.raises(ValueError, match="conditions"):
        asyncio.run(runtime.apply_action(prepared, ActionProposal(action="request_draft", target_id="label_draft")))
    offer = next(a for a in prepared.context.enabled() if a.action == "ask_user")
    response, decision, outcome = asyncio.run(runtime.apply_action(prepared,
        ActionProposal(action="ask_user", target_id="method.tools", evidence_refs=offer.evidence_refs)))
    assert outcome == "awaiting_user" and response.questions[0].id == "kb:method.tools"
    assert decision.applied_planner.adapter_revision == "afa-joint-runtime-0.1"
    assert runtime.dispatch_count == 1 and "method.tools" not in runtime.state.confirmed_observations
    after = runtime.prepare_context([event("tools", "method.tools", "hands")])
    response, _, outcome = asyncio.run(runtime.apply_action(after, ActionProposal(action="request_draft", target_id="label_draft")))
    assert outcome == "draft_generated" and not response.draft.saved and response.draft.requires_approval
    assert runtime.dispatch_count == runtime.state.turn_index == 2


def test_pending_correction_invalidates_old_snapshot_and_retains_history():
    runtime, prepared = friction_first()
    old = runtime.prepare_context([event("tools1", "method.tools", "scrub_brush")])
    current = runtime.prepare_context([event("tools2", "method.tools", "hands", supersedes="tools1")])
    with pytest.raises(ValueError, match="stale"):
        asyncio.run(runtime.apply_action(old, ActionProposal(action="hold", target_id="insufficient_information")))
    assert len(json.loads(current.payload)["events"]) == 5
    assert current.state.confirmed_observations["method.tools"].value == "hands"
    assert runtime.dispatch_count == 0
    altered = replace(current, payload=current.payload + " ")
    with pytest.raises(ValueError, match="stale"):
        asyncio.run(runtime.apply_action(altered, ActionProposal(action="hold", target_id="insufficient_information")))


def test_dispatch_failure_does_not_commit_pending_answer(monkeypatch):
    runtime, prepared = friction_first()
    before = runtime.state

    async def fail(*args):
        raise ValueError("synthetic dispatch failure")

    monkeypatch.setattr(joint_runtime, "dispatch_action", fail)
    with pytest.raises(ValueError, match="dispatch failure"):
        asyncio.run(runtime.apply_action(prepared, ActionProposal(action="ask_user", target_id="method.tools")))
    assert runtime.state == before and runtime.dispatch_count == 0 and runtime._prepared == prepared


def test_concurrent_dispatch_cannot_consume_snapshot_twice():
    runtime, prepared = friction_first()

    async def run():
        proposal = ActionProposal(action="ask_user", target_id="method.tools")
        return await asyncio.gather(runtime.apply_action(prepared, proposal), runtime.apply_action(prepared, proposal), return_exceptions=True)

    results = asyncio.run(run())
    assert sum(isinstance(result, ValueError) for result in results) == 1
    assert runtime.dispatch_count == 1


@pytest.mark.parametrize("example", json.loads(PROBES.read_text(encoding="utf-8"))["examples"], ids=lambda row: row["id"])
def test_all_nine_public_probes_reach_a_real_dispatch(example):
    runtime = JointSessionAdapter()
    prepared = runtime.prepare_context([event(row[0], row[1], row[2], row[3] if len(row) > 3 else "known",
        row[4] if len(row) > 4 else None) for row in example["events"]])
    result = diagnostic(prepared)
    assert all(result[key] == value for key, value in example["expected"].items())
    action = "request_draft" if result["draft_permitted_by_contract"] else "ask_user" if result["research_question_requirements"] else "hold"
    offer = next(a for a in prepared.context.enabled() if a.action == action)
    _, _, outcome = asyncio.run(runtime.apply_action(prepared, ActionProposal(action=action, target_id=offer.target_id)))
    assert outcome == {"request_draft": "draft_generated", "ask_user": "awaiting_user", "hold": "held"}[action]
    for row in example["events"]:
        if len(row) > 3 and row[3] in {"unknown", "declined", "conflicting"}:
            assert runtime.state.confirmed_observations[row[1]].state == row[3]

