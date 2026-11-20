"""Two-phase snapshot/dispatch contract without optional Gym dependencies."""
import asyncio
from dataclasses import replace
import json

import pytest

from beauty_agent.afa import runtime
from beauty_agent.afa.runtime import StaticSessionAdapter
from beauty_agent.afa.stage0 import DEFAULT
from beauty_agent.actions import ActionProposal


def adapter():
    return StaticSessionAdapter(json.loads(DEFAULT.read_text(encoding="utf-8")), "B-C02")


def test_prepare_is_staged_and_context_copy_cannot_open_draft_gate():
    session = adapter()
    prepared = session.prepare_context()
    copy = prepared.context
    next(a for a in copy.available_actions if a.action == "request_draft").enabled = True
    assert not next(a for a in prepared.context.available_actions if a.action == "request_draft").enabled
    assert session.dispatch_count == 0 and session.state.turn_index == 0
    assert not session.state.confirmed_observations
    with pytest.raises(ValueError, match="capabilities"):
        asyncio.run(session.apply_action(prepared, ActionProposal(action="request_draft", target_id="label_draft")))


def test_apply_dispatches_once_and_rejects_consumed_snapshot(monkeypatch):
    session = adapter()
    prepared = session.prepare_context()
    original = runtime.dispatch_action
    calls = []

    async def spy(*args):
        calls.append(1)
        return await original(*args)

    monkeypatch.setattr(runtime, "dispatch_action", spy)
    proposal = ActionProposal(action="ask_user", target_id="method.body_site")
    _, _, outcome = asyncio.run(session.apply_action(prepared, proposal))
    assert outcome == "awaiting_user" and calls == [1]
    assert session.dispatch_count == session.state.turn_index == 1
    assert session.state.confirmed_observations == {}  # A request is not an answer.
    with pytest.raises(ValueError, match="stale"):
        asyncio.run(session.apply_action(prepared, proposal))
    assert calls == [1]


def test_response_preparation_does_not_commit_or_execute():
    session = adapter()
    initial = session.prepare_context()
    asyncio.run(session.apply_action(initial, ActionProposal(action="ask_user", target_id="method.body_site")))
    prepared = session.prepare_context({"method.body_site": {
        "variable_id": "method.body_site", "state": "known", "value": "face",
        "source": "synthetic_fixture", "confirmed_by_user": True}})
    assert session.dispatch_count == 1 and session.state.confirmed_observations == {}
    assert prepared.state.confirmed_observations["method.body_site"].value == "face"


def test_stale_and_forged_snapshots_rejected():
    session = adapter()
    old = session.prepare_context()
    current = session.prepare_context()
    proposal = ActionProposal(action="hold", target_id="insufficient_information")
    for invalid in (old, replace(current, payload=current.payload + " ")):
        with pytest.raises(ValueError, match="stale"):
            asyncio.run(session.apply_action(invalid, proposal))
    assert session.dispatch_count == 0


def test_concurrent_apply_cannot_consume_snapshot_twice():
    session = adapter()
    prepared = session.prepare_context()
    proposal = ActionProposal(action="ask_user", target_id="method.body_site")

    async def run():
        return await asyncio.gather(session.apply_action(prepared, proposal),
                                    session.apply_action(prepared, proposal), return_exceptions=True)

    results = asyncio.run(run())
    assert sum(isinstance(r, ValueError) for r in results) == 1
    assert session.dispatch_count == session.state.turn_index == 1


def test_failed_dispatch_leaves_staged_and_committed_state_unchanged(monkeypatch):
    session = adapter()
    prepared = session.prepare_context()
    before = session.state

    async def fail(*args):
        raise ValueError("synthetic dispatch failure")

    monkeypatch.setattr(runtime, "dispatch_action", fail)
    with pytest.raises(ValueError, match="dispatch failure"):
        asyncio.run(session.apply_action(prepared, ActionProposal(action="ask_user", target_id="method.body_site")))
    assert session.state == before and session.dispatch_count == 0
    assert session._prepared == prepared
