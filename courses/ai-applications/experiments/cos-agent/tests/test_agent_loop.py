"""Synthetic integration checks; no remote Jev or model execution."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path

import httpx
import pytest

from beauty_agent.contracts import ObservationSlot, OwnedProduct, PlannerOutput, TurnRequest
from beauty_agent.loop import AgentSession, CandidateConfirmation, run_pipeline_turn
from beauty_agent.modules.jev_adapter import JevExtractorAdapter
from beauty_agent.modules.mapping_adapter import MappingReviewAdapter
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.planner import RuleBasedContextualPlanner, OllamaContextualPlanner


def run(awaitable):
    return asyncio.run(awaitable)


@pytest.fixture
def request_data(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "baseline")
    return TurnRequest.model_validate_json(Path("examples/turn.json").read_text(encoding="utf-8"))


def obs(key, value, **kwargs):
    return ObservationSlot(variable_id=key, state="known", value=value,
                           confirmed_by_user=True, **kwargs)


def features(message):
    return {"schema_version": "relations-0.3", "products": [{"text": "폼클렌저"}],
            "symptoms": [{"symptom": "stinging", "relations": {
                "state": {"value": "affirmed", "status": "candidate", "score": .9},
                "subject": {"value": "self", "status": "candidate", "score": .9},
                "severity": {"value": "mild"}}}] if "따가" in message else [],
            "warnings": [], "clarifications": []}


def extractor():
    return JevExtractorAdapter(extractor=features)


def ready_observations():
    return {key: obs(key, value) for key, value in {
        "method.body_site": "face", "method.water_temperature": "lukewarm"}.items()}


def test_compound_turn_trace_and_mapping_bridge(request_data):
    request = request_data.model_copy(update={"message": "어제 밤에 약산성 폼클렌저로 바꾸고 나서 볼이 따가워"})
    source = features(request.message)
    original = deepcopy(source)
    view = JevExtractorAdapter.to_mapping_review_features(source)
    assert view["schema_version"] == "relations-0.3" and source == original
    result = run(run_pipeline_turn(request, extractor=extractor(), card_ids=["B-C01"]))
    assert result.status == "needs_information" and result.draft is None
    assert result.trace.jev_products == ["폼클렌저"]
    finding = result.trace.mapping_findings[0]
    assert finding["issue"] == "candidate_requires_user_and_time_confirmation"
    assert finding["no_direct_skin_state_field"] == ["severity"]
    assert result.trace.kb_evaluated_cards == ["B-C01"]
    assert result.trace.selected_route == "ask_user"
    assert result.questions[0].id.startswith("clarify:")
    assert not result.trace.production_enabled


def test_mapping_invalid_snapshot_and_unknown_schema():
    with pytest.raises(ValueError):
        MappingReviewAdapter().evaluate(features(""), {"version": "bad"})
    with pytest.raises(ValueError):
        JevExtractorAdapter.to_mapping_review_features({"schema_version": "future"})


def test_multiturn_confirmation_then_draft(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    first = run(session.step("어제 밤 폼클렌저 후 따가워"))
    assert first.status == "needs_information"
    assert not session.state.confirmed_observations
    key = next(iter(session.state.pending_clarifications))
    # An unrelated message cannot discard last turn's candidate.
    second = run(session.step("계속해 주세요"))
    assert second.questions[0].id == key
    confirmation = CandidateConfirmation(subject="self", state="affirmed", observed_at="2026-11-08T12:00:00Z")
    final = run(session.step("관찰과 제품을 확인했습니다", observations=ready_observations(),
                             confirmations={key: confirmation}))
    assert final.status == "draft" and final.draft.saved is False
    assert final.trace.selected_route == "ready_for_draft"
    assert not session.state.pending_clarifications
    assert session.state.turn_index == 3 and len(session.state.history) == 3
    assert "skin.stinging" not in session.state.confirmed_observations


def test_plain_yes_cannot_confirm_profile_or_product(request_data):
    session = AgentSession(request_data.model_copy(update={"profile": request_data.profile.model_copy(update={"confirmed": False})}),
                           extractor=extractor(), card_ids=["B-C01"])
    result = run(session.step("네", observations=ready_observations()))
    assert not session.state.profile.confirmed
    assert result.questions[0].id == "confirm_profile"
    assert run(session.step("프로필 확인", profile=request_data.profile)).status == "draft"


def test_ask_and_retrieve_are_separate(request_data):
    adapter = KBEngineAdapter()
    result = adapter.evaluate({"method.body_site": obs("method.body_site", "face")}, ["B-C04"])
    assert result["retrieve_slots"]
    assert all(key.startswith("product.") for key in result["retrieve_slots"])
    assert not any(key.startswith("product.") for key in result["ask_slots"])
    response = run(run_pipeline_turn(request_data, extractor=extractor(), kb=adapter,
                                     observations={"method.body_site": obs("method.body_site", "face")},
                                     card_ids=["B-C04"]))
    assert response.draft is None
    assert all(not q.id.startswith("kb:product.") for q in response.questions)


def test_pluggable_planner_and_unsafe_output_is_bounded(request_data):
    class MockSFT:
        seen = None
        async def plan(self, context):
            self.seen = context
            return context.candidates()[-1].model_copy(update={"question_ko": "제품의 비공개 농도를 알려주세요"})
    planner = MockSFT()
    result = run(run_pipeline_turn(request_data, planner=planner, extractor=extractor(), card_ids=["B-C01"]))
    assert planner.seen is not None
    assert "비공개 농도" not in result.message
    assert result.message in planner.seen.kb_ask_slots.values()


@pytest.mark.parametrize("action", ["refer_for_professional_review", "defer_specific_recommendation"])
def test_hold_beats_untrusted_planner(request_data, action):
    class HoldKB:
        def evaluate(self, *args):
            return {"raw": {"results": []}, "ask_slots": {}, "retrieve_slots": [], "hold_signals": [action]}
    class BadPlanner:
        async def plan(self, context):
            return PlannerOutput(route="ask_user", target_slot="product.private_ph",
                                 question_ko="비공개 pH를 알려주세요")
    result = run(run_pipeline_turn(request_data, kb=HoldKB(), planner=BadPlanner(), extractor=extractor()))
    assert result.trace.selected_route == "hold_or_escalate"
    assert not result.questions and result.draft is None


def test_real_engine_severe_pain_holds(request_data):
    observations = ready_observations()
    observations["skin.pain"] = obs("skin.pain", "new_severe")
    result = run(run_pipeline_turn(request_data, extractor=extractor(), observations=observations,
                                  card_ids=["B-B01"]))
    assert "refer_for_professional_review" in result.trace.hold_signals
    assert result.trace.selected_route == "hold_or_escalate" and result.draft is None


def test_unconfirmed_and_product_facts_rejected(request_data):
    session = AgentSession(request_data, extractor=extractor())
    with pytest.raises(ValueError):
        run(session.step("", observations={"product.ph": obs("product.ph", "5.5")}))
    with pytest.raises(ValueError):
        run(session.step("", observations={"skin.pain": ObservationSlot(variable_id="skin.pain", value="none")}))
    assert session.state.turn_index == 0
    assert not session.state.confirmed_observations


def test_conflicts_require_explicit_resolution(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    assert run(session.step("", observations=ready_observations())).status == "draft"
    key = "method.water_temperature"
    result = run(session.step("", observations={key: obs(key, "hot")}))
    assert result.draft is None and session.state.confirmed_observations[key].state == "conflicting"
    run(session.step("", observations={key: obs(key, "hot")}))
    assert session.state.confirmed_observations[key].state == "conflicting"
    run(session.step("", observations={key: obs(key, "hot")}, resolve_conflicts=(key,)))
    assert session.state.confirmed_observations[key].state == "known"


def test_unresolved_comparison_preserves_explicit_evidence_path_without_draft(request_data):
    observations = ready_observations()
    observations["method.water_temperature"] = obs("method.water_temperature", "cold")
    result = run(run_pipeline_turn(request_data, extractor=extractor(), observations=observations, card_ids=["B-C01"]))
    assert result.trace.execution_status == "awaiting_product_evidence" and result.draft is None


def test_no_acquisition_path_cannot_become_draft(request_data):
    class UnresolvedKB:
        def evaluate(self, *args):
            return {"raw": {"results": [{"card_id": "synthetic:unresolved", "comparison_status": "unknown"}]},
                    "ask_slots": {}, "retrieve_slots": [], "hold_signals": ["unresolved_kb_comparison"]}

    result = run(run_pipeline_turn(request_data, extractor=extractor(), kb=UnresolvedKB()))
    assert result.trace.execution_status == "held" and result.draft is None


def test_declined_slot_not_reasked():
    adapter = KBEngineAdapter()
    result = adapter.evaluate({"method.body_site": obs("method.body_site", "face"),
        "method.water_temperature": ObservationSlot(variable_id="method.water_temperature",
            state="declined", confirmed_by_user=True)}, ["B-C01"])
    assert "method.water_temperature" not in result["ask_slots"]


def test_offline_extraction_has_no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("network forbidden")
    monkeypatch.setattr(httpx, "post", forbidden)
    result = JevExtractorAdapter().extract("따가워")
    assert result["symptoms"][0]["relations"]["state"]["value"] == "unknown"
    assert "offline_candidate_detection_not_jev_inference" in result["warnings"]


@pytest.mark.parametrize("bad_time", ["어제", "2026-11-08T12:00:00", "2026-11-08T12:00:00+09:00"])
def test_confirmation_requires_time(bad_time):
    with pytest.raises(ValueError):
        CandidateConfirmation(subject="self", state="affirmed", observed_at=bad_time)


def test_ollama_context_and_fallback(request_data, monkeypatch):
    import beauty_agent.planner as module
    original = httpx.AsyncClient
    seen = []
    def handler(request):
        data = json.loads(request.content)
        seen.append(json.loads(data["messages"][1]["content"]))
        return httpx.Response(200, json={"done": True, "message": {"content": '{"question_id":"0"}'}})
    monkeypatch.setenv("AGENT_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "synthetic-mock")
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kw: original(transport=httpx.MockTransport(handler), **kw))
    response = run(run_pipeline_turn(request_data, extractor=extractor(), planner=OllamaContextualPlanner(), card_ids=["B-C04"]))
    assert response.provider == "ollama"
    context = json.loads(seen[0]["message"])
    assert "forbidden_retrieve_slots" in context and "mapping_findings" in context
    monkeypatch.delenv("OLLAMA_MODEL")
    fallback = run(run_pipeline_turn(request_data, extractor=extractor(), planner=OllamaContextualPlanner(), card_ids=["B-C04"]))
    assert fallback.provider == "baseline_fallback"


def test_retrieve_route_has_no_consumer_question(request_data):
    class RetrieveKB:
        def evaluate(self, *args):
            return {"raw": {"results": []}, "ask_slots": {},
                    "retrieve_slots": ["product.private_concentration", "product.ph"], "hold_signals": []}
    result = run(run_pipeline_turn(request_data, extractor=extractor(), kb=RetrieveKB()))
    assert result.trace.selected_route == "retrieve_product"
    assert not result.questions and result.draft is None


def test_manufacturer_opinion_card_is_isolated():
    with pytest.raises(ValueError):
        KBEngineAdapter().evaluate({}, ["B-P07"])


def test_module_error_does_not_mutate_session(request_data):
    class BrokenExtractor:
        def extract(self, message):
            raise ValueError("synthetic failure")
    session = AgentSession(request_data, extractor=BrokenExtractor())
    before = session.state.model_dump()
    with pytest.raises(ValueError):
        run(session.step("test", observations=ready_observations()))
    assert session.state.model_dump() == before


def test_scripted_cli_demo(capsys):
    from beauty_agent.loop import demo
    run(demo(scripted=True))
    output = capsys.readouterr().out
    assert '"status": "needs_information"' in output
    assert '"status": "draft"' in output


def test_repeated_utterance_is_a_new_unconfirmed_observation(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    run(session.step("따가워"))
    key = next(iter(session.state.pending_clarifications))
    confirmation = CandidateConfirmation(subject="self", state="affirmed", observed_at="2026-11-08T12:00:00Z")
    run(session.step("확인", confirmations={key: confirmation}, observations=ready_observations()))
    result = run(session.step("따가워"))
    assert result.status == "needs_information"
    assert result.questions[0].id != key
    assert session.state.pending_clarifications


@pytest.mark.parametrize("value", [0, 1, 8, 1.5, True, False, "unknown", ["stinging"],
                                  {"range_seconds": [1, 2.5], "phase": "before_rinsing"}])
def test_observation_json_roundtrip_preserves_value_types(value):
    slot = obs("synthetic.observation", value)
    restored = ObservationSlot.model_validate_json(slot.model_dump_json())
    assert type(restored.value) is type(value)
    assert restored.value == value
    if isinstance(value, dict):
        assert type(restored.value["range_seconds"][0]) is int
        assert type(restored.value["range_seconds"][1]) is float


@pytest.mark.parametrize("card_id,answers,reason", [
    ("B-C03", {"dose.contact_time": {"range_seconds": [20, 30.5], "phase": "before_rinsing"}},
     "contact_scope_missing"),
    ("B-S06", {"shaving.method": "manual", "shaving.blade_use_history": 8,
                "shaving.care": "replacement_not_reviewed"},
     "past_KB_manual_reference_without_review"),
])
def test_session_passes_numeric_and_structured_answers_to_real_kb(request_data, card_id, answers, reason):
    class RecordingKB(KBEngineAdapter):
        def evaluate(self, *args):
            self.result = super().evaluate(*args)
            return self.result

    kb = RecordingKB()
    session = AgentSession(request_data, extractor=extractor(), kb=kb, card_ids=[card_id])
    observations = {key: obs(key, value) for key, value in answers.items()}
    observations["method.body_site"] = obs("method.body_site", "face")
    run(session.step("confirmed synthetic answers", observations=observations))
    row = kb.result["raw"]["results"][0]
    assert row["reason"] == reason
    for key, value in answers.items():
        assert type(session.state.confirmed_observations[key].value) is type(value)
        assert row["observations"][key]["value"] == value
    if card_id == "B-C03":
        assert "product.type" in kb.result["retrieve_slots"]


@pytest.mark.parametrize("length", [92, 93, 100])
def test_valid_long_product_ids_return_resolution_blocker(request_data, length):
    product_id = "x" * length
    request = TurnRequest.model_validate({**request_data.model_dump(), "products": [
        OwnedProduct(product_id=product_id, version="synthetic-v1").model_dump()]})
    result = run(run_pipeline_turn(request, extractor=extractor()))
    assert result.status == "needs_information" and result.draft is None
    assert result.questions[0].id == "resolve:" + product_id
    assert result.message == result.questions[0].text


@pytest.mark.parametrize("version", ["relations-0.2", "relations-0.3", "relations-0.4", "relations-0.5"])
def test_pipeline_accepts_main_jev_schemas_without_downgrade(request_data, version):
    source = {**features("따가워"), "schema_version": version}
    original = deepcopy(source)
    adapter = JevExtractorAdapter(extractor=lambda _: source)
    view = adapter.to_mapping_review_features(source)
    assert view == original and view is not source
    result = run(run_pipeline_turn(request_data, extractor=adapter, card_ids=["B-C01"]))
    assert result.trace.mapping_findings[0]["issue"] == "candidate_requires_user_and_time_confirmation"
    assert source == original


@pytest.mark.parametrize("version", ["relations-0.3", "relations-0.4", "relations-0.5"])
def test_modern_unassessed_relations_do_not_use_legacy_review(version):
    source = {**features("따가워"), "schema_version": version}
    source["symptoms"][0]["relations"]["state"] = {"value": "affirmed"}
    finding = MappingReviewAdapter().evaluate(source)["findings"][0]
    assert finding["issue"] == "unassessed_or_uncertain_symptom_do_not_map"
    assert "suggested_value" not in finding


@pytest.mark.parametrize("card_id", ["B-G06", "B-M04"])
@pytest.mark.parametrize("planner", [None, RuleBasedContextualPlanner()])
def test_information_deferral_allows_missing_user_questions(request_data, card_id, planner):
    session = AgentSession(request_data, planner=planner, extractor=extractor(), card_ids=[card_id])
    result = run(session.step("", observations={"method.body_site": obs("method.body_site", "face")}))
    assert "insufficient_information" in result.trace.hold_signals
    assert result.trace.execution_status == "awaiting_user"
    assert result.trace.applied_action["action"] == "ask_user"
    assert result.questions and result.draft is None


@pytest.mark.parametrize("card_id", ["B-G16", "B-P09"])
def test_unresolved_explicit_evidence_requests_reach_retrieval(request_data, card_id):
    observations = {"method.body_site": obs("method.body_site", "face")}
    evaluated = KBEngineAdapter().evaluate(observations, [card_id])
    row = evaluated["raw"]["results"][0]
    assert "retrieve_product_evidence" not in row["action_types"]
    expected = sorted({item["field"] for item in row["evidence_requests"]})
    assert expected and evaluated["retrieve_slots"] == expected
    session = AgentSession(request_data, extractor=extractor(), card_ids=[card_id])
    result = run(session.step("", observations=observations))
    assert result.trace.execution_status == "awaiting_product_evidence"
    assert result.trace.applied_action["target_id"] in expected
    assert not result.questions and result.draft is None


def test_resolved_card_incidental_evidence_gaps_do_not_block_draft(request_data):
    evaluated = KBEngineAdapter().evaluate(ready_observations(), ["B-C01"])
    assert evaluated["raw"]["results"][0]["evidence_requests"]
    assert not evaluated["retrieve_slots"]
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    assert run(session.step("", observations=ready_observations())).status == "draft"


@pytest.mark.parametrize("state", ["unknown", "declined"])
@pytest.mark.parametrize("polarity", ["affirmed", "denied"])
def test_unresolved_candidate_can_be_explicitly_corrected(request_data, state, polarity):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    run(session.step("따가워", observations=ready_observations()))
    key = next(iter(session.state.pending_clarifications))
    unanswered = CandidateConfirmation(subject="unknown", state=state)
    result = run(session.step("", confirmations={key: unanswered}))
    assert result.trace.execution_status == "held" and result.draft is None
    assert not session.state.pending_clarifications
    assert run(session.step("")).trace.execution_status == "held"
    with pytest.raises(ValueError):
        run(session.step("", confirmations={"clarify:invented": unanswered}))
    with pytest.raises(ValueError):
        run(session.step("", confirmations={key: {"subject": "self", "state": polarity}}))
    assert session.state.confirmed_clarifications[key] == unanswered
    replacement = CandidateConfirmation(subject="self", state=polarity, observed_at="2026-11-08T12:00:00Z")
    result = run(session.step("명시적 수정", confirmations={key: replacement}))
    assert result.trace.execution_status == "draft_generated"
    assert session.state.confirmed_clarifications[key] == replacement
    assert not session.state.pending_clarifications
    assert "skin.stinging" not in session.state.confirmed_observations
    # The previous held result remains visible in history.
    assert session.state.history[1]["trace"]["execution_status"] == "held"


def test_unrecognized_known_answer_is_reasked_until_explicitly_corrected(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])
    observations = ready_observations()
    key = "method.water_temperature"
    observations[key] = obs(key, "warm")
    result = run(session.step("", observations=observations))
    assert result.trace.execution_status == "awaiting_user"
    assert result.trace.applied_action["target_id"] == key
    assert result.questions[0].id == "kb:" + key and result.draft is None
    assert session.state.confirmed_observations[key].value == "warm"
    result = run(session.step("정형 수정", observations={key: obs(key, "lukewarm")}, resolve_conflicts=(key,)))
    assert result.trace.execution_status == "draft_generated"


def test_quality_deferral_without_referral_still_requires_hold(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-G11"])
    observations = {"method.body_site": obs("method.body_site", "face"),
                    "storage.expiry": obs("storage.expiry", "confirmed_expired")}
    result = run(session.step("", observations=observations))
    assert "defer_specific_recommendation" in result.trace.hold_signals
    assert result.trace.applied_action["action"] == "hold"
    assert result.trace.applied_action["target_id"] == "safety"
    assert result.trace.execution_status == "held" and result.draft is None


def test_concurrent_session_turns_preserve_both_updates_and_history(request_data):
    session = AgentSession(request_data, extractor=extractor(), card_ids=["B-C01"])

    async def concurrent():
        return await asyncio.gather(
            session.step("first", observations={"method.body_site": obs("method.body_site", "face")}),
            session.step("second", observations={"method.water_temperature": obs("method.water_temperature", "lukewarm")}))

    first, second = run(concurrent())
    assert first.trace.execution_status == "awaiting_user"
    assert second.trace.execution_status == "draft_generated"
    assert session.state.confirmed_observations == ready_observations()
    assert session.state.turn_index == 2
    assert [item["message"] for item in session.state.history] == ["first", "second"]


def test_failed_concurrent_turn_releases_session_for_next_turn(request_data):
    def fail_first(message):
        if message == "invalid":
            raise ValueError("synthetic extraction failure")
        return features(message)

    session = AgentSession(request_data, extractor=JevExtractorAdapter(extractor=fail_first), card_ids=["B-C01"])

    async def concurrent():
        return await asyncio.gather(
            session.step("invalid", observations={"synthetic.failed_update": obs("synthetic.failed_update", True)}),
            session.step("valid", observations=ready_observations()), return_exceptions=True)

    failed, succeeded = run(concurrent())
    assert isinstance(failed, ValueError)
    assert succeeded.trace.execution_status == "draft_generated"
    assert "synthetic.failed_update" not in session.state.confirmed_observations
    assert session.state.turn_index == 1
    assert [item["message"] for item in session.state.history] == ["valid"]


def test_cancelled_turn_rolls_back_and_releases_session_lock(request_data):
    async def scenario():
        entered, release = asyncio.Event(), asyncio.Event()

        class WaitingPlanner:
            async def plan_action(self, context):
                entered.set()
                await release.wait()

        session = AgentSession(request_data, extractor=extractor(), planner=WaitingPlanner(), card_ids=["B-C01"])
        task = asyncio.create_task(session.step("cancelled", observations=ready_observations()))
        await asyncio.wait_for(entered.wait(), timeout=5)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert session.state.turn_index == 0 and not session.state.confirmed_observations
        session.planner = None
        result = await asyncio.wait_for(session.step("next", observations=ready_observations()), timeout=5)
        assert result.trace.execution_status == "draft_generated"
        assert [item["message"] for item in session.state.history] == ["next"]

    run(scenario())
