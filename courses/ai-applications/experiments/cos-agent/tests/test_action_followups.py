"""Regression cases for explicit corrections, action responses and planner identity."""
import asyncio
import json
from copy import deepcopy
from pathlib import Path

import pytest

from beauty_agent.actions import ActionProposal
from beauty_agent.action_planner import QuestionPlannerAdapter, SFTActionPlanner
from beauty_agent.contracts import PlannerMetadata, Profile, TurnRequest
from beauty_agent.loop import AgentSession, CandidateConfirmation, run_pipeline_turn
from beauty_agent.modules.jev_adapter import JevExtractorAdapter


@pytest.fixture
def request_data(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "baseline")
    return TurnRequest.model_validate_json(Path("examples/turn.json").read_text(encoding="utf-8"))


def extractor():
    def features(message):
        return {"schema_version": "relations-0.5", "products": [],
                "symptoms": [{"symptom": "stinging", "relations": {}}] if message == "symptom" else [],
                "warnings": [], "clarifications": []}
    return JevExtractorAdapter(extractor=features)


class SyntheticKB:
    def __init__(self, *, holds=False, retrieve=False):
        self.holds, self.retrieve = holds, retrieve

    def evaluate(self, *args):
        return {"raw": {"results": []}, "ask_slots": {},
                "retrieve_slots": ["product.ph"] if self.retrieve else [],
                "hold_signals": ["refer_for_professional_review"] if self.holds else []}


@pytest.mark.parametrize("initial", ["unknown", "declined"])
@pytest.mark.parametrize("corrected", ["affirmed", "denied"])
def test_previously_unresolved_candidate_accepts_explicit_correction(request_data, initial, corrected):
    async def scenario():
        session = AgentSession(request_data, extractor=extractor(), kb=SyntheticKB())
        await session.step("symptom")
        key = next(iter(session.state.pending_clarifications))
        response = await session.step("unresolved", confirmations={key: CandidateConfirmation(
            subject="unknown", state=initial)})
        assert response.trace.execution_status == "held" and response.draft is None
        # No automatic re-questioning or natural-language promotion to confirmed.
        response = await session.step("I can now answer")
        assert response.trace.execution_status == "held" and not response.questions
        assert session.state.confirmed_clarifications[key].state == initial
        assert not session.state.pending_clarifications
        response = await session.step("explicit correction", confirmations={key: CandidateConfirmation(
            subject="self", state=corrected, observed_at="2026-11-08T12:00:00Z")})
        assert response.trace.execution_status == "draft_generated"
        assert session.state.confirmed_clarifications[key].state == corrected
        assert not session.state.confirmed_observations
        assert not session.state.pending_clarifications
    asyncio.run(scenario())


def test_unknown_candidate_id_and_invalid_correction_leave_state_intact(request_data):
    async def scenario():
        session = AgentSession(request_data, extractor=extractor(), kb=SyntheticKB())
        await session.step("symptom")
        key = next(iter(session.state.pending_clarifications))
        await session.step("unknown", confirmations={key: CandidateConfirmation(subject="unknown", state="unknown")})
        before = deepcopy(session.state.model_dump())
        for target, value in [("invented-id", {"subject": "unknown", "state": "unknown"}),
                              (key, {"subject": "self", "state": "affirmed"})]:
            with pytest.raises(ValueError):
                await session.step("invalid correction", confirmations={target: value})
            assert session.state.model_dump() == before
    asyncio.run(scenario())


class Select:
    def __init__(self, action):
        self.action = action

    async def plan_action(self, context):
        offer = next(o for o in context.enabled() if o.action == self.action)
        return ActionProposal(action=offer.action, target_id=offer.target_id)


@pytest.mark.parametrize("action,outcome", [("hold", "held"),
                                            ("retrieve_evidence", "awaiting_product_evidence")])
def test_non_question_actions_preserve_blockers_without_asking_them(request_data, action, outcome):
    async def scenario():
        session = AgentSession(request_data.model_copy(update={"profile": Profile()}),
            extractor=extractor(), kb=SyntheticKB(holds=action == "hold", retrieve=True), planner=Select(action))
        response = await session.step("first")
        assert response.trace.execution_status == outcome
        assert response.questions == [] and response.draft is None
        assert not session.state.profile.confirmed
        session.kb = SyntheticKB()
        session.planner = Select("ask_user")
        following = await session.step("continue")
        assert following.questions[0].id == "confirm_profile"
    asyncio.run(scenario())


class SyntheticSFT(SFTActionPlanner):
    metadata = PlannerMetadata(provider="sft", model="synthetic-qwen",
                               revision="synthetic-base-revision", adapter_revision="synthetic-adapter-revision")

    def __init__(self, failure=None):
        self.failure = failure

    async def plan_action(self, context):
        if self.failure == "timeout":
            await asyncio.sleep(1)
        if self.failure == "invalid":
            return {"action": "request_draft", "target_id": "invented"}
        if self.failure == "error":
            raise RuntimeError("synthetic inference failure")
        return ActionProposal(action="request_draft", target_id="label_draft")


@pytest.mark.parametrize("failure", [None, "invalid", "timeout", "error"])
def test_trace_distinguishes_sft_attempt_from_baseline_fallback(request_data, failure):
    response = asyncio.run(run_pipeline_turn(request_data, planner=SyntheticSFT(failure),
        extractor=extractor(), kb=SyntheticKB(), planner_timeout=.01))
    trace = response.trace
    assert trace.requested_planner == SyntheticSFT.metadata
    assert trace.applied_planner == (SyntheticSFT.metadata if failure is None else PlannerMetadata(provider="baseline"))
    assert response.provider == ("baseline" if failure is None else "baseline_fallback")
    if failure is None:
        assert trace.fallback_reason is None
    else:
        assert trace.fallback_reason is not None
    # Identities survive storage in a JSON trace and do not widen the legacy response enum.
    assert json.loads(response.model_dump_json())["trace"]["requested_planner"]["adapter_revision"] == "synthetic-adapter-revision"


def test_unlabelled_custom_planner_is_not_recorded_as_baseline(request_data):
    response = asyncio.run(run_pipeline_turn(request_data, planner=Select("hold"),
        extractor=extractor(), kb=SyntheticKB()))
    assert response.trace.requested_planner.provider == "custom"
    assert response.trace.applied_planner.provider == "custom"


def test_sft_identity_without_configured_revisions_keeps_unknown_values(request_data):
    class UnconfiguredSFT(SFTActionPlanner):
        model = "synthetic-model"
        async def plan_action(self, context):
            return ActionProposal(action="hold", target_id="insufficient_information")
    response = asyncio.run(run_pipeline_turn(request_data, planner=UnconfiguredSFT(),
        extractor=extractor(), kb=SyntheticKB()))
    assert response.trace.applied_planner == PlannerMetadata(provider="sft", model="synthetic-model")


def test_legacy_adapter_distinguishes_internal_fallback_and_later_recovery(request_data):
    class Legacy:
        fallback = True
        async def plan(self, context):
            return context.candidates()[0].model_copy(update={
                "provider": "baseline_fallback" if self.fallback else "baseline"})
    async def scenario():
        legacy = Legacy()
        adapter = QuestionPlannerAdapter(legacy)
        request = request_data.model_copy(update={"profile": Profile()})
        response = await run_pipeline_turn(request, planner=adapter, extractor=extractor(), kb=SyntheticKB())
        assert response.trace.requested_planner.provider == "custom"
        assert response.trace.applied_planner.provider == "baseline"
        legacy.fallback = False
        response = await run_pipeline_turn(request, planner=adapter, extractor=extractor(), kb=SyntheticKB())
        assert response.trace.applied_planner.provider == "custom"
    asyncio.run(scenario())


def test_failed_module_does_not_commit_explicit_candidate_correction(request_data):
    class BrokenMapping:
        def evaluate(self, *args):
            raise ValueError("synthetic mapping failure")
    async def scenario():
        session = AgentSession(request_data, extractor=extractor(), kb=SyntheticKB())
        await session.step("symptom")
        key = next(iter(session.state.pending_clarifications))
        await session.step("decline", confirmations={key: CandidateConfirmation(subject="unknown", state="declined")})
        before = deepcopy(session.state.model_dump())
        session.mapping = BrokenMapping()
        with pytest.raises(ValueError):
            await session.step("correction", confirmations={key: CandidateConfirmation(
                subject="self", state="affirmed", observed_at="2026-11-08T12:00:00Z")})
        assert session.state.model_dump() == before
    asyncio.run(scenario())
