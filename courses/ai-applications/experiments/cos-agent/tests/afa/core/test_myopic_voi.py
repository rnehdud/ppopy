import json

import pytest

from beauty_agent.afa.question_priority import MyopicVOIAFAPolicy, decision_signature, rank_questions
from beauty_agent.contracts import ObservationSlot
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime import AgentRuntime, RuleBasedAFAPolicy
from beauty_agent.runtime_contracts import AFAStepDecision, ChoiceSelection, QuestionCandidate, RuntimeTurnRequest
from beauty_agent import v3_contracts


def observation(slot, value=None, *, state="known"):
    return ObservationSlot(variable_id=slot, state=state, value=value,
                           source="synthetic_fixture", confirmed_by_user=True)


def observations(values):
    return {slot: observation(slot, value) for slot, value in values.items()}


def candidate(slot, *cards):
    return QuestionCandidate(slot_id=slot, question_text=slot, card_ids=list(cards))


@pytest.fixture
def adapter():
    return KBEngineAdapter()


@pytest.mark.parametrize(("card", "initial", "target"), [
    ("B-C02", {}, "method.tools"),
    ("B-M01", {}, "method.current_routine"),
    ("B-P02", {"sun.outdoor_time": "prolonged"}, "skin.eye_stinging"),
    ("B-I01", {}, "cleansing.steps"),
    ("B-I02", {"sun.pilling": "present"}, "sun.reapplication"),
    ("B-I03", {}, "moisturizing.comfort"),
])
def test_uses_branch_values_across_domains(adapter, card, initial, target):
    state = observations({"method.body_site": "face", **initial})
    evaluated = adapter.evaluate(state, [card])
    candidates = [candidate(slot, card) for slot in evaluated["ask_slots"]]
    policy = MyopicVOIAFAPolicy(adapter)
    decision = policy.decide_step(state, candidates, can_stop_sufficient=False)
    assert decision.target_feature == target
    assert decision.policy_source == "myopic_voi"
    scores = {s.slot_id: s for s in policy.score_candidates(state, candidates)}
    assert scores[target].reason == "selected"
    assert scores[target].decision_change_rate > 0
    assert scores[target].expected_pruned > 0


def test_branch_pruning_and_zero_impact_are_explained(adapter):
    state = observations({"method.body_site": "face"})
    card = "B-I01"
    evaluated = adapter.evaluate(state, [card])
    candidates = [candidate(slot, card) for slot in evaluated["ask_slots"]]
    policy = MyopicVOIAFAPolicy(adapter)
    scores = {s.slot_id: s.model_dump(mode="json") for s in policy.score_candidates(state, candidates)}
    assert scores["cleansing.steps"] == {
        "slot_id": "cleansing.steps", "answer_count": 2, "decision_change_rate": 0.5,
        "expected_pruned": 1.0, "distinct_outcomes": 2, "reason": "selected",
        "question_cost": 1.0, "safety_weight": 1.0,
    }
    assert scores["dose.proxy_amount"]["reason"] == "zero_impact"
    assert scores["dose.proxy_amount"]["distinct_outcomes"] == 1
    assert scores["sun.outdoor_time"]["decision_change_rate"] == 0
    assert rank_questions(adapter, [card], state, list(reversed(candidates)), evaluated)[0].slot_id == "cleansing.steps"
    assert set(state) == {"method.body_site"}


def test_default_tie_break_and_optional_weights(adapter):
    state = observations({"method.body_site": "face", "method.tools": "hands"})
    card = "B-C02"
    features = [candidate("method.friction", card), candidate("method.drying", card)]
    default = MyopicVOIAFAPolicy(adapter)
    for order in (features, list(reversed(features))):
        assert default.decide_step(state, order, can_stop_sufficient=False).target_feature == "method.drying"
    weighted = MyopicVOIAFAPolicy(adapter, question_costs={"method.drying": 2})
    assert weighted.decide_step(state, features, can_stop_sufficient=False).target_feature == "method.friction"


@pytest.mark.parametrize("state", ["known", "unknown", "declined", "not_applicable"])
def test_answered_and_product_candidates_are_never_asked(adapter, state):
    obs = observations({"method.body_site": "face"})
    field = "method.water_temperature"
    obs[field] = observation(field, "unrecognized" if state == "known" else None, state=state)
    features = [candidate(field, "B-C01"), candidate("product.spf", "B-P01")]
    policy = MyopicVOIAFAPolicy(adapter)
    scores = {s.slot_id: s.reason for s in policy.score_candidates(obs, features)}
    assert scores == {field: "already_answered", "product.spf": "product_evidence"}
    assert policy.decide_step(obs, features, can_stop_sufficient=False).stop_reason == "insufficient"


def test_zero_impact_respects_stop_permissions(adapter):
    state = observations({"method.body_site": "face", "method.water_temperature": "lukewarm"})
    features = [candidate("cleansing.repeat_wash", "B-C05")]
    policy = MyopicVOIAFAPolicy(adapter)
    for sufficient in (True, False):
        result = policy.decide_step(state, features, can_stop_sufficient=sufficient)
        assert result.action == "stop"
        assert result.stop_reason == ("sufficient" if sufficient else "insufficient")
    with pytest.raises(ValueError, match="permitted stop"):
        policy.decide_step(state, features, can_stop_sufficient=False, can_stop_insufficient=False)


def test_myopic_outputs_validate_directly_as_v3_contracts(adapter):
    policy = MyopicVOIAFAPolicy(adapter, card_ids=["B-C02"])
    state = observations({"method.body_site": "face"})
    features = [candidate("method.tools", "B-C02"), candidate("product.spf", "B-P01")]
    scores = policy.score_candidates(state, features)
    acquire = policy.decide_step(state, features, can_stop_sufficient=False)
    for score in scores:
        assert v3_contracts.AFACandidateScore.model_validate(score) == score
        assert v3_contracts.AFACandidateScore.model_validate(score.model_dump()) == score
    assert {score.slot_id: score.reason for score in scores} == {
        "method.tools": "selected", "product.spf": "product_evidence",
    }
    assert v3_contracts.AFAStepDecision.model_validate(acquire).target_feature == "method.tools"
    stop = policy.decide_step(state, features[1:], can_stop_sufficient=False)
    assert v3_contracts.AFAStepDecision.model_validate(stop).stop_reason == "insufficient"
    for decision in (acquire, stop):
        validated = v3_contracts.AFAStepDecision.model_validate(decision.model_dump())
        assert validated.model_dump() == decision.model_dump()
        assert validated.policy_source == "myopic_voi"
    trace = v3_contracts.TurnTrace(request_id="myopic-v3", turn_index=1, afa_decision=acquire, afa_scores=scores)
    assert trace.afa_scores == scores


def test_legacy_afa_conversion_enforces_v3_product_boundary():
    stop = AFAStepDecision.from_legacy_action("hold", "insufficient_information")
    assert v3_contracts.AFAStepDecision.model_validate(stop).policy_source == "rule_baseline"
    with pytest.raises(ValueError, match=r"product\.\*"):
        AFAStepDecision.from_legacy_action("ask_user", "product.spf", policy_source="ppo_model")


class FixedCardsRuntime(AgentRuntime):
    """Run the normal Control Plane with the same active card set for both policies."""

    def __init__(self, cards, **kwargs):
        super().__init__(**kwargs)
        self.cards = cards

    def _select_cards(self, state, topic_hints, observations):
        state.active_cards = list(self.cards)
        return state.active_cards


def test_runtime_accepts_policy_returning_the_v3_decision_directly():
    class V3Policy:
        def decide_step(self, observations, candidates, **permissions):
            return v3_contracts.AFAStepDecision(action="acquire", target_feature="method.drying")

    runtime = FixedCardsRuntime(["B-C02"], afa_policy=V3Policy())
    result = runtime.handle_turn(RuntimeTurnRequest(
        request_id="v3-policy", observations=observations({"method.body_site": "face"}),
    ))
    assert result.questions[0].id == "method.drying"
    state = runtime.get_session(result.request_id)
    assert state.afa_step_decision.policy_source == "myopic_voi"


@pytest.mark.parametrize(("cards", "initial", "slot", "choice_label", "expected"), [
    (["B-C02"], {}, "method.tools", "세안 브러시", "scrub_brush"),
    (["B-M01"], {}, "method.current_routine", "보습이 필요함", "moisturizing_needed"),
    (["B-P02"], {"sun.outdoor_time": "prolonged"}, "skin.eye_stinging", "반복해서 따가움", "recurrent"),
    (["B-I01"], {}, "cleansing.steps", "제품에 표시된 제거 방법을 따름",
     "according_to_product_removal_instructions"),
])
def test_runtime_quick_replies_resume_with_confirmed_kb_value(cards, initial, slot, choice_label, expected):
    runtime = FixedCardsRuntime(cards, afa_policy=MyopicVOIAFAPolicy())
    request_id = "quick-replies"
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        observations=observations({"method.body_site": "face", **initial}),
    ))
    question = response.questions[0]
    assert question.id == slot and not question.id.startswith("product.")
    assert {"unknown", "declined"} <= {choice.id for choice in question.choices}
    choice = next(choice for choice in question.choices if choice.label == choice_label)
    selection = ChoiceSelection(turn_index=question.turn_index, question_id=question.id, choice_id=choice.id)
    before = runtime.get_session(request_id)
    for invalid in [
        selection.model_copy(update={"turn_index": selection.turn_index + 1}),
        selection.model_copy(update={"question_id": "product.spf"}),
        selection.model_copy(update={"choice_id": "forged"}),
    ]:
        with pytest.raises(ValueError, match="stale question or invalid choice"):
            runtime.handle_turn(RuntimeTurnRequest(request_id=request_id, choice_selection=invalid))
        assert runtime.get_session(request_id) == before

    resumed = runtime.handle_turn(RuntimeTurnRequest(request_id=request_id, choice_selection=selection))
    actual = runtime.get_session(request_id).confirmed_observations[slot]
    assert (actual.state, actual.value, actual.confirmed_by_user) == ("known", expected, True)
    assert resumed.nlp is None and all(q.id != slot for q in resumed.questions)


def test_runtime_stops_with_open_zero_impact_questions_and_preserves_retrieve(adapter):
    runtime = FixedCardsRuntime(["B-I04"], kb_adapter=adapter, afa_policy=MyopicVOIAFAPolicy())
    body = observations({"method.body_site": "face"})
    result = runtime.handle_turn(RuntimeTurnRequest(request_id="ivo", observations=body))
    state = runtime.get_session("ivo")
    assert result.status == "held"
    assert result.afa_handoff.policy_source == "myopic_voi"
    assert result.afa_handoff.status == "insufficient"
    assert "product.active_care_roles" in result.required_product_evidence
    assert state.afa_question_scores
    assert any(s.reason == "zero_impact" for s in state.afa_question_scores)
    assert not state.asked_feature_order
    assert result.mode == "development_preview"
    assert result.production_enabled is False


@pytest.mark.parametrize("answer_state", ["known", "declined"])
def test_dependency_check_asks_once_and_reassesses_actual_answer(adapter, answer_state):
    policy = MyopicVOIAFAPolicy(adapter)
    initial = observations({"method.body_site": "face"})
    features = [candidate(slot, "B-I02") for slot in adapter.evaluate(initial, ["B-I02"])["ask_slots"]]
    for depth in (1, 2, 3):
        core_decision = MyopicVOIAFAPolicy(adapter, stop_lookahead=depth).decide_step(
            initial, features, can_stop_sufficient=False,
        )
        assert core_decision.action == "stop"
        assert core_decision.stop_reason == "insufficient"
    runtime = FixedCardsRuntime(["B-I02"], kb_adapter=adapter, afa_policy=policy)
    request_id = "joint-dependency"
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, observations=initial,
    ))
    first = response.questions[0].id
    assert first in {"sun.pilling", "sun.reapplication"}
    session = runtime.get_session(request_id)
    trace = {score.slot_id: score for score in session.afa_question_scores}
    assert session.afa_hold_review_slot == first
    assert session.afa_step_decision == AFAStepDecision(
        action="stop", stop_reason="insufficient", policy_source="myopic_voi",
    )
    assert trace[first].reason == "zero_impact"
    assert trace[first].decision_change_rate == 0
    assert set(runtime.get_session(request_id).confirmed_observations) == {"method.body_site"}
    aligned = {"sun.pilling": "none", "sun.reapplication": "matched_to_exposure_and_label"}
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        observations={first: observation(first, aligned[first] if answer_state == "known" else None,
                                         state=answer_state)},
    ))
    if answer_state == "declined":
        assert response.status == "held"
        assert not response.questions
        return
    second, = set(aligned) - {first}
    assert response.questions[0].id == second
    assert runtime.get_session(request_id).afa_hold_review_slot is None
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, observations=observations({second: aligned[second]}),
    ))
    assert response.status == "completed"
    assert response.afa_handoff.asked_feature_order == [first, second]


@pytest.mark.parametrize("answer_state", ["known", "unknown", "declined", "not_applicable"])
def test_runtime_does_not_reask_an_answered_slot(adapter, answer_state):
    runtime = FixedCardsRuntime(["B-C01"], kb_adapter=adapter, afa_policy=MyopicVOIAFAPolicy())
    state = observations({"method.body_site": "face"})
    field = "method.water_temperature"
    state[field] = observation(field, "warm" if answer_state == "known" else None, state=answer_state)
    result = runtime.handle_turn(RuntimeTurnRequest(request_id="known", observations=state))
    assert result.status == "held"
    assert result.afa_handoff.status == "insufficient"
    assert not result.questions


def test_runtime_hands_off_sufficient_after_a_known_answer(adapter):
    runtime = FixedCardsRuntime(["B-C01"], kb_adapter=adapter, afa_policy=MyopicVOIAFAPolicy())
    first = runtime.handle_turn(RuntimeTurnRequest(
        request_id="sufficient", observations=observations({"method.body_site": "face"}),
    ))
    assert first.questions[0].id == "method.water_temperature"
    session = runtime.get_session("sufficient")
    assert session.afa_step_decision == AFAStepDecision(
        action="acquire", target_feature=first.questions[0].id, policy_source="myopic_voi",
    )
    assert session.afa_question_scores[0].reason == "selected"
    assert session.pending_question == first.questions[0]
    assert first.questions[0].choices
    retry = runtime.handle_turn(RuntimeTurnRequest(request_id="sufficient"))
    assert retry.questions == first.questions
    assert runtime.get_session("sufficient").afa_step_decision == session.afa_step_decision
    second = runtime.handle_turn(RuntimeTurnRequest(
        request_id="sufficient", observations=observations({"method.water_temperature": "lukewarm"}),
    ))
    assert second.status == "completed"
    assert second.afa_handoff.status == "sufficient"
    assert second.afa_handoff.policy_source == "myopic_voi"
    assert runtime.get_session("sufficient").afa_step_decision == AFAStepDecision(
        action="stop", stop_reason="sufficient", policy_source="myopic_voi",
    )


@pytest.mark.parametrize(("card", "field", "value", "signal"), [
    ("B-H01", "skin.pain", "new_severe", "refer_for_professional_review"),
    ("B-P08", "storage.expiry", "confirmed_expired", "pause_specific_product_pending_quality_check"),
    ("B-M05", "shaving.reaction", "aftershave_stings", "pause_specific_cosmetic_due_to_discomfort"),
])
def test_mandatory_hold_preempts_policy_and_cannot_be_sufficient(adapter, card, field, value, signal):
    state = observations({"method.body_site": "face", field: value})
    cards = [card, "B-C02"]
    assert signal in adapter.evaluate(state, cards)["hold_signals"]
    policy = MyopicVOIAFAPolicy(adapter, card_ids=cards)
    result = policy.decide_step(state, [candidate("method.tools", "B-C02")], can_stop_sufficient=True)
    assert result.stop_reason == "insufficient"

    class MustNotRun(MyopicVOIAFAPolicy):
        def score_candidates(self, *args, **kwargs):
            pytest.fail("mandatory hold must preempt AFA")

    runtime = FixedCardsRuntime(cards, kb_adapter=adapter, afa_policy=MustNotRun())
    result = runtime.handle_turn(RuntimeTurnRequest(request_id="mandatory", observations=state))
    assert result.status == "held"
    assert result.executed_actions == ["hold"]
    assert result.afa_handoff is None
    assert runtime.get_session("mandatory").afa_step_decision is None


def run_case(adapter, cards, initial, answers, policy):
    runtime = FixedCardsRuntime(cards, kb_adapter=adapter, afa_policy=policy,
                                prioritize_question_outcomes=False)
    request_id = "synthetic-comparison"
    initial = observations({"method.body_site": "face", **initial})
    response = runtime.handle_turn(RuntimeTurnRequest(request_id=request_id, observations=initial))
    asked = []
    while response.status == "awaiting_user":
        assert response.pending_action == "ask_user"
        slot = response.questions[0].id
        assert slot not in asked and slot not in initial and not slot.startswith("product.")
        asked.append(slot)
        answer = observation(slot, answers[slot]) if slot in answers else observation(slot, state="unknown")
        response = runtime.handle_turn(RuntimeTurnRequest(request_id=request_id, observations={slot: answer}))
    current = runtime.get_session(request_id).confirmed_observations
    final = decision_signature(adapter.evaluate(current, list(cards)))
    return asked, (response.status, final)


def test_synthetic_comparison(adapter):
    fixtures = [
        ("C", ["B-C05"], {}, {"cleansing.target_load": "heavy_sweat"}),
        ("M", ["B-M01"], {}, {"method.current_routine": "moisturizing_not_needed_no_discomfort"}),
        ("P", ["B-P02"], {"sun.outdoor_time": "prolonged"}, {"skin.eye_stinging": "recurrent"}),
        ("I01", ["B-I01"], {}, {"cleansing.steps": "repeated_only_because_water_resistant"}),
        ("I02", ["B-I02"], {}, {
            "sun.pilling": "none", "sun.reapplication": "matched_to_exposure_and_label",
        }),
        ("I03", ["B-I03"], {}, {"moisturizing.comfort": "sensory_feel_interpreted_as_absorption"}),
        ("I04", ["B-I04"], {}, {}),
        ("joint", ["B-C05", "B-M01", "B-P02", "B-I01"], {"sun.outdoor_time": "prolonged"}, {
            "cleansing.target_load": "heavy_soiling",
            "method.current_routine": "moisturizing_not_needed_no_discomfort",
            "skin.eye_stinging": "recurrent",
            "cleansing.steps": "repeated_only_because_water_resistant",
        }),
    ]
    rows = []
    for group, cards, initial, answers in fixtures:
        baseline, baseline_final = run_case(adapter, cards, initial, answers, RuleBasedAFAPolicy())
        myopic, myopic_final = run_case(adapter, cards, initial, answers, MyopicVOIAFAPolicy(stop_lookahead=1))
        rows.append({"group": group, "cards": cards, "baseline_questions": baseline,
                     "myopic_questions": myopic, "baseline_status": baseline_final[0],
                     "myopic_status": myopic_final[0], "baseline_overall": baseline_final[1][0],
                     "myopic_overall": myopic_final[1][0], "final_agreement": baseline_final == myopic_final})
    count = len(rows)
    report = {
        "scenario_count": count,
        "baseline_mean_questions": sum(len(r["baseline_questions"]) for r in rows) / count,
        "myopic_mean_questions": sum(len(r["myopic_questions"]) for r in rows) / count,
        "final_agreement_rate": sum(r["final_agreement"] for r in rows) / count,
        "rows": rows,
    }
    print(json.dumps(report, sort_keys=True))
    assert report["baseline_mean_questions"] > report["myopic_mean_questions"]
    # B-I02 needs two answers together. Neither changes the one-step effect.
    assert [r["group"] for r in rows if not r["final_agreement"]] == ["I02"]
    paired = next(row for row in rows if row["group"] == "I02")
    assert paired["baseline_overall"] != "hold"
    assert paired["myopic_overall"] == "hold"
    assert paired["myopic_status"] == "held"
