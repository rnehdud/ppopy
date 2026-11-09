"""Action selection and execution boundaries; synthetic inputs, no real models."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path

import httpx
import pytest

from beauty_agent.actions import ActionArguments, ActionProposal
from beauty_agent.action_planner import OllamaActionPlanner, SFTActionPlanner
from beauty_agent.action_runtime import decide_action
from beauty_agent.contracts import ObservationSlot, Profile, TurnRequest
from beauty_agent.loop import AgentSession, CandidateConfirmation, run_pipeline_turn
from beauty_agent.modules.jev_adapter import JevExtractorAdapter


def run(value):
    return asyncio.run(value)


@pytest.fixture
def request_data(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "baseline")
    return TurnRequest.model_validate_json(Path("examples/turn.json").read_text(encoding="utf-8"))


def extractor(symptoms=False):
    return JevExtractorAdapter(extractor=lambda _: {"schema_version": "relations-0.5",
        "products": [], "symptoms": [{"symptom": "stinging", "relations": {
            "state": {"value": "affirmed", "status": "candidate", "score": .9},
            "subject": {"value": "self", "status": "candidate", "score": .9}}}] if symptoms else [],
        "warnings": [], "clarifications": []})


class SyntheticKB:
    def __init__(self, ask=None, retrieve=None, holds=None):
        self.ask = ask or {}
        self.retrieve = retrieve or []
        self.holds = holds or []

    def evaluate(self, *args):
        return {"raw": {"results": []}, "ask_slots": self.ask,
                "retrieve_slots": self.retrieve, "hold_signals": self.holds}


class Select(SFTActionPlanner):
    def __init__(self, action, target=None, **kwargs):
        self.action, self.target, self.kwargs = action, target, kwargs
        self.context = None

    async def plan_action(self, context):
        self.context = context
        target = self.target or next(item.target_id for item in context.available_actions if item.action == self.action)
        return ActionProposal(action=self.action, target_id=target, **self.kwargs)


def observed(key, value=None, state="known"):
    return ObservationSlot(variable_id=key, state=state, value=value, confirmed_by_user=True)


def test_model_can_choose_different_actions_under_same_constraints(request_data):
    class Contextual(SFTActionPlanner):
        contexts = []
        async def plan_action(self, context):
            self.contexts.append(context)
            kind = "retrieve_evidence" if "제품" in context.message else "ask_user"
            offer = next(item for item in context.enabled() if item.action == kind)
            return ActionProposal(action=kind, target_id=offer.target_id, reason_summary="Synthetic contextual target")
    planner = Contextual()
    kb = SyntheticKB(ask={"method.water_temperature": "세안할 때 물이 얼마나 따뜻한가요?"}, retrieve=["product.ph"])
    first = run(run_pipeline_turn(request_data.model_copy(update={"message": "내 관찰부터 확인"}),
                                  planner=planner, extractor=extractor(), kb=kb))
    second = run(run_pipeline_turn(request_data.model_copy(update={"message": "제품 자료 먼저 확인"}),
                                   planner=planner, extractor=extractor(), kb=kb))
    assert planner.contexts[0].available_actions == planner.contexts[1].available_actions
    assert first.trace.applied_action["action"] == "ask_user"
    assert first.trace.execution_status == "awaiting_user"
    assert second.trace.applied_action["action"] == "retrieve_evidence"
    assert second.trace.execution_status == "awaiting_product_evidence"
    assert not second.questions and second.draft is None


@pytest.mark.parametrize("kind,outcome", [("confirm_candidate", "awaiting_user"),
    ("resolve_conflict", "awaiting_user"), ("hold", "held"), ("request_draft", "draft_generated")])
def test_distinct_action_outcomes(request_data, kind, outcome):
    observations = {"method.water_temperature": observed("method.water_temperature", state="conflicting")} if kind == "resolve_conflict" else {}
    result = run(run_pipeline_turn(request_data, planner=Select(kind), extractor=extractor(kind == "confirm_candidate"),
                                  kb=SyntheticKB(), observations=observations))
    assert result.trace.proposed_action["action"] == kind
    assert result.trace.applied_action["action"] == kind
    assert result.trace.execution_status == outcome
    assert (result.draft is not None) == (kind == "request_draft")


def test_candidate_request_never_confirms_state(request_data):
    session = AgentSession(request_data, planner=Select("confirm_candidate"), extractor=extractor(True), kb=SyntheticKB())
    result = run(session.step("synthetic symptom"))
    assert result.trace.execution_status == "awaiting_user"
    assert session.state.pending_clarifications
    assert not session.state.confirmed_observations
    assert not session.state.confirmed_clarifications


@pytest.mark.parametrize("output,reason", [
    ("not json", "invalid_action_contract"),
    ({"action": "delete_database", "target_id": "all"}, "invalid_action_contract"),
    ({"action": "ask_user", "target_id": "product.private_ph"}, "action_target_not_offered"),
    ({"action": "request_draft", "target_id": "label_draft", "confirmed": True}, "invalid_action_contract"),
    ({"action": "ask_user", "target_id": "method.water_temperature", "arguments": {"url": "https://invalid.example"}}, "invalid_action_contract"),
    ({"action": "ask_user", "target_id": "method.water_temperature", "evidence_refs": ["invented:approval"]}, "evidence_reference_not_allowed_for_target"),
    ({"action": "retrieve_evidence", "target_id": "https://invalid.example"}, "action_target_not_offered"),
    (None, "proposal_must_be_object"),
])
def test_invalid_proposals_share_deterministic_fallback(request_data, output, reason):
    class Bad:
        async def plan_action(self, context):
            return output
    result = run(run_pipeline_turn(request_data, planner=Bad(), extractor=extractor(),
        kb=SyntheticKB(ask={"method.water_temperature": "물 온도를 알려주세요."})))
    assert result.provider == "baseline_fallback"
    assert result.trace.fallback_reason == reason
    assert result.trace.applied_action["action"] == "ask_user"
    assert result.questions[0].id == "kb:method.water_temperature"


@pytest.mark.parametrize("failure", [RuntimeError, httpx.ReadTimeout])
def test_model_failure_falls_back_without_claiming_execution(request_data, failure):
    class Broken:
        async def plan_action(self, context):
            raise failure("untrusted private error text")
    result = run(run_pipeline_turn(request_data, planner=Broken(), extractor=extractor(True), kb=SyntheticKB()))
    assert result.trace.applied_action["action"] == "confirm_candidate"
    assert result.provider == "baseline_fallback"
    assert "private error" not in result.model_dump_json()


def test_planner_absolute_deadline(request_data):
    class Slow:
        async def plan_action(self, context):
            await asyncio.sleep(1)
    result = run(run_pipeline_turn(request_data, planner=Slow(), extractor=extractor(), kb=SyntheticKB(), planner_timeout=.001))
    assert result.trace.fallback_reason == "planner_timeout"


@pytest.mark.parametrize("blocker", ["candidate", "profile", "products", "conflict", "retrieve", "hold"])
def test_draft_prerequisites_cannot_be_bypassed(request_data, blocker):
    if blocker == "profile":
        request_data = request_data.model_copy(update={"profile": Profile()})
    if blocker == "products":
        request_data = request_data.model_copy(update={"products": []})
    observations = {"method.water_temperature": observed("method.water_temperature", state="conflicting")} if blocker == "conflict" else {}
    result = run(run_pipeline_turn(request_data, planner=Select("request_draft"), extractor=extractor(blocker == "candidate"),
        kb=SyntheticKB(retrieve=["product.ph"] if blocker == "retrieve" else [],
                       holds=["refer_for_professional_review"] if blocker == "hold" else []), observations=observations))
    assert result.trace.proposed_action["action"] == "request_draft"
    assert result.trace.applied_action["action"] != "request_draft"
    assert result.trace.fallback_reason == "execution_conditions_not_met"
    assert result.draft is None


def test_mandatory_hold_blocks_non_hold_actions(request_data):
    result = run(run_pipeline_turn(request_data, planner=Select("ask_user", "method.water_temperature"), extractor=extractor(),
        kb=SyntheticKB(ask={"method.water_temperature": "물 온도?"}, holds=["refer_for_professional_review"])))
    assert result.trace.applied_action["action"] == "hold"
    assert result.trace.execution_status == "held"


def test_context_mutation_cannot_enable_draft(request_data):
    class Mutating:
        async def plan_action(self, context):
            context.pending_clarifications.clear()
            for item in context.available_actions:
                item.enabled = True
                item.blocked_by.clear()
            return ActionProposal(action="request_draft", target_id="label_draft")
    result = run(run_pipeline_turn(request_data, planner=Mutating(), extractor=extractor(True), kb=SyntheticKB()))
    assert result.trace.applied_action["action"] == "confirm_candidate"
    assert result.trace.pending_clarifications and result.draft is None


@pytest.mark.parametrize("state,value", [("known", False), ("known", 0), ("unknown", None),
    ("declined", None), ("not_applicable", None)])
def test_answered_negative_unknown_and_declined_slots_not_reasked(request_data, state, value):
    planner = Select("hold")
    slot = "skin.current_discomfort"
    run(run_pipeline_turn(request_data, planner=planner, extractor=extractor(),
        observations={slot: observed(slot, value, state)}, kb=SyntheticKB(ask={slot: "불편이 있나요?"})))
    assert slot not in planner.context.kb_ask_slots
    assert not any(o.action == "ask_user" and o.target_id == slot for o in planner.context.available_actions)
    assert planner.context.observations[slot].state == state


def test_product_gaps_are_never_ask_actions(request_data):
    planner = Select("retrieve_evidence")
    run(run_pipeline_turn(request_data, planner=planner, extractor=extractor(),
        kb=SyntheticKB(ask={"product.ph": "pH?"}, retrieve=["product.ph", "product.private_concentration"])))
    assert not any(o.action == "ask_user" and o.target_id.startswith("product.") for o in planner.context.available_actions)
    assert planner.context.tools["await_product_evidence"]["implemented"] is False


def test_unverifiable_question_is_replaced_but_action_choice_preserved(request_data):
    result = run(run_pipeline_turn(request_data, planner=Select("ask_user", question_ko="정확한 비공개 농도를 알려주세요."),
        extractor=extractor(), kb=SyntheticKB(ask={"method.water_temperature": "물 온도를 알려주세요."})))
    assert result.message == "물 온도를 알려주세요."
    assert result.trace.proposed_action["question_ko"] != result.trace.applied_action["question_ko"]
    assert result.trace.fallback_reason == "unverified_question_wording"


def test_extraction_labels_are_not_trusted_as_reviewed_questions(request_data):
    unsafe = extractor(True).extract("")
    unsafe["symptoms"][0]["label"] = "비공개 pH 값을 알려주세요"
    unsafe["clarifications"] = ["비공개 농도를 알려주세요"]
    planner = Select("confirm_candidate")
    result = run(run_pipeline_turn(request_data, planner=planner,
        extractor=JevExtractorAdapter(extractor=lambda _: unsafe), kb=SyntheticKB()))
    assert "pH" not in result.message and "농도" not in result.message
    assert all("비공개" not in item.reviewed_text for item in planner.context.available_actions)


def test_code_rendered_contextual_wording_allowed(request_data):
    result = run(run_pipeline_turn(request_data, planner=Select("ask_user", arguments=ActionArguments(wording="contextual")),
        extractor=extractor(), kb=SyntheticKB(ask={"method.water_temperature": "물 온도를 알려주세요."})))
    assert result.message == "앞서 말씀하신 내용과 관련해, 물 온도를 알려주세요."
    assert result.trace.fallback_reason is None


@pytest.mark.parametrize("focus,word", [("subject", "본인"), ("polarity", "없었다"), ("time", "시점")])
def test_model_can_focus_confirmation_on_missing_dimension(request_data, focus, word):
    result = run(run_pipeline_turn(request_data, planner=Select("confirm_candidate",
        arguments=ActionArguments(confirmation_focus=focus)), extractor=extractor(True), kb=SyntheticKB()))
    assert word in result.message and result.trace.execution_status == "awaiting_user"
    assert result.trace.applied_action["arguments"]["confirmation_focus"] == focus


def test_confirmation_arguments_cannot_be_used_for_other_tools(request_data):
    result = run(run_pipeline_turn(request_data, planner=Select("request_draft",
        arguments=ActionArguments(confirmation_focus="time")), extractor=extractor(), kb=SyntheticKB()))
    assert result.trace.fallback_reason == "arguments_not_allowed_for_action"


def test_synthetic_sft_samples_use_runtime_contract_and_unreviewed_targets():
    from beauty_agent.actions import ActionContext
    from beauty_agent.action_runtime import validate_action
    from scripts.build_action_examples import build_examples, OUTPUT
    saved = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert run(build_examples()) == saved
    assert saved["human_review"] == "unreviewed"
    assert saved["claims_about_model_improvement"] is None
    kinds = set()
    for sample in saved["samples"]:
        context = ActionContext.model_validate(sample["input"])
        output = ActionProposal.model_validate(sample["output"])
        applied, replaced = validate_action(output, context)
        assert not replaced and applied == output
        assert sample["provenance"]["approved_reference"] is False
        kinds.add(output.action)
    assert kinds == {"ask_user", "confirm_candidate", "retrieve_evidence", "resolve_conflict", "hold", "request_draft"}
    chain = [sample for sample in saved["samples"] if sample["conversation_id"] == "symptom_to_draft"]
    assert [sample["output"]["action"] for sample in chain] == ["confirm_candidate", "ask_user", "request_draft"]
    assert [len(sample["input"]["history"]) for sample in chain] == [0, 1, 2]


def test_declined_candidate_stays_unknown_without_reasking_or_draft(request_data):
    session = AgentSession(request_data, extractor=extractor(True), kb=SyntheticKB())
    run(session.step("first"))
    key = next(iter(session.state.pending_clarifications))
    session.extractor = extractor()
    result = run(session.step("거절", confirmations={key: CandidateConfirmation(subject="unknown", state="declined")}))
    assert not session.state.pending_clarifications
    assert session.state.confirmed_clarifications[key].state == "declined"
    assert not session.state.confirmed_observations
    assert result.trace.execution_status == "held" and result.draft is None


def test_unknown_candidate_can_record_time_without_inventing_subject():
    value = CandidateConfirmation(subject="unknown", state="unknown", observed_at="2026-11-08T12:00:00Z")
    assert value.subject == "unknown" and value.state == "unknown"


def test_numeric_and_boolean_answers_remain_distinct_conflicting_values(request_data):
    session = AgentSession(request_data, extractor=extractor(), kb=SyntheticKB())
    key = "synthetic.observation"
    run(session.step("first", observations={key: observed(key, 1)}))
    run(session.step("second", observations={key: observed(key, True)}))
    assert session.state.confirmed_observations[key].state == "conflicting"


def test_conflict_resolution_request_requires_explicit_caller_update(request_data):
    session = AgentSession(request_data, extractor=extractor(), kb=SyntheticKB())
    key = "method.water_temperature"
    run(session.step("first", observations={key: observed(key, "hot")}))
    session.planner = Select("resolve_conflict")
    result = run(session.step("second", observations={key: observed(key, "lukewarm")}))
    assert result.trace.execution_status == "awaiting_user"
    assert session.state.confirmed_observations[key].state == "conflicting"
    session.planner = Select("request_draft")
    result = run(session.step("third", observations={key: observed(key, "lukewarm")}, resolve_conflicts=(key,)))
    assert result.status == "draft" and len(session.state.history) == 3


def test_module_failure_leaves_all_staged_updates_unapplied(request_data):
    class BrokenMapping:
        def evaluate(self, *args):
            raise ValueError("synthetic failure")
    session = AgentSession(request_data, extractor=extractor(), mapping=BrokenMapping(), kb=SyntheticKB())
    before = deepcopy(session.state.model_dump())
    with pytest.raises(ValueError):
        run(session.step("failed turn", profile=Profile(),
            observations={"method.body_site": observed("method.body_site", "face")}))
    assert session.state.model_dump() == before


@pytest.mark.parametrize("payload", ["valid", "bad_json", "incomplete", "too_large", "timeout"])
def test_new_ollama_transport_uses_full_action_contract(request_data, monkeypatch, payload):
    original = httpx.AsyncClient
    seen = []
    def handler(req):
        data = json.loads(req.content)
        seen.append(data)
        if payload == "timeout":
            raise httpx.ReadTimeout("mock timeout")
        content = json.dumps({"action": "retrieve_evidence", "target_id": "product.ph", "reason_summary": "Missing product evidence"})
        if payload == "bad_json":
            content = "not JSON"
        if payload == "too_large":
            content = "x" * 65537
        return httpx.Response(200, json={"done": payload != "incomplete", "message": {"content": content}})
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: original(transport=httpx.MockTransport(handler), **kw))
    result = run(run_pipeline_turn(request_data, planner=OllamaActionPlanner("mock-local"), extractor=extractor(),
        kb=SyntheticKB(ask={"method.water_temperature": "물 온도?"}, retrieve=["product.ph"])))
    data = seen[0]
    assert "action" in data["format"]["properties"]
    context = json.loads(data["messages"][1]["content"])
    assert context["schema_version"] == "action-context-0.1"
    assert context["available_actions"] and context["tools"]
    assert context["request_snapshot"] and context["mode"] == "development_preview"
    if payload == "valid":
        assert result.provider == "ollama" and result.model == "mock-local"
        assert result.trace.execution_status == "awaiting_product_evidence"
    else:
        assert result.provider == "baseline_fallback"
        assert result.trace.applied_action["action"] == "ask_user"
