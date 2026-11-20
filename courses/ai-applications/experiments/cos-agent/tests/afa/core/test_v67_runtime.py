import asyncio

import pytest

from beauty_agent.actions import ActionProposal
from beauty_agent.afa import v67_runtime as runtime
from beauty_agent.afa.v67_fixtures import FixtureContractError


@pytest.fixture(scope="module")
def bundle():
    return runtime.load_response_book()[:2]


def proposal(action, target):
    return ActionProposal(action=action, target_id=target)


def test_refusal_reveals_one_slot_and_closes_repeat(bundle):
    book, ids = bundle
    session = runtime.FixtureSession(book, next(i for i in ids if i.endswith("849")))
    prepared = session.prepare_context()
    assert session.dispatch_count == 0
    assert set(prepared.context.observations) == {"method.body_site"}
    drying = proposal("ask_user", "method.drying")
    response, outcome, _ = asyncio.run(session.apply_action(prepared, drying))
    assert response.questions[0].id == "kb:method.drying"
    assert outcome == "awaiting_user"
    current = session.prepare_context()
    assert set(current.context.observations) == {"method.body_site", "method.drying"}
    assert current.context.observations["method.drying"].state == "declined"
    with pytest.raises(ValueError, match="action_target_not_offered"):
        asyncio.run(session.apply_action(current, drying))
    with pytest.raises(FixtureContractError, match="stale"):
        asyncio.run(session.apply_action(prepared, drying))
    assert session.dispatch_count == 1


@pytest.mark.parametrize("failure", ["missing_response", "dispatch"])
def test_failed_step_keeps_context_and_state_reusable(bundle, monkeypatch, failure):
    book, ids = bundle
    session = runtime.FixtureSession(book, ids[0])
    prepared, before = session.prepare_context(), session.public
    action = proposal("ask_user", "method.tools")
    calls = []

    async def fail_dispatch(*args):
        calls.append("dispatch")
        raise RuntimeError("dispatch failed")

    def fail_answer(*args, **kwargs):
        raise FixtureContractError("response missing")

    with monkeypatch.context() as patch:
        patch.setattr(runtime, "dispatch_action", fail_dispatch)
        if failure == "missing_response":
            patch.setattr(book, "answer", fail_answer)
        with pytest.raises((FixtureContractError, RuntimeError)):
            asyncio.run(session.apply_action(prepared, action))
    assert calls == (["dispatch"] if failure == "dispatch" else [])
    assert session.public == before and session.dispatch_count == 0
    assert session.prepare_context() is prepared
    asyncio.run(session.apply_action(prepared, action))
    assert session.dispatch_count == 1


def test_existing_gate_blocks_draft_until_kb_branch_resolves(bundle):
    book, ids = bundle
    session = runtime.FixtureSession(book, next(i for i in ids if i.endswith("849")))
    draft = proposal("request_draft", "label_draft")
    with pytest.raises(ValueError, match="execution_conditions_not_met"):
        asyncio.run(session.apply_action(session.prepare_context(), draft))
    asyncio.run(session.apply_action(session.prepare_context(), proposal("ask_user", "method.tools")))
    current = session.prepare_context()
    assert not any(offer.action == "ask_user" for offer in current.context.enabled())
    response, outcome, disposition = asyncio.run(session.apply_action(current, draft))
    assert outcome == "draft_generated" and disposition == "draft_allowed"
    assert response.draft.requires_approval and not response.draft.saved
    with pytest.raises(FixtureContractError, match="finished"):
        session.prepare_context()


def test_historical_label_alternatives_remain_distinct_from_rubric():
    groups = runtime.label_review()
    assert len(groups) == 2
    for group in groups:
        assert ["hold", "insufficient_information"] in group["allowed_actions"]
        assert group["preference_under_active_acquisition"] == ["ask_user", "method.body_site"]
        assert group["single_label_disposition"] == "withhold_group_pending_dataset_purpose"
