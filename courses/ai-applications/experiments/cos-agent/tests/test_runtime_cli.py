"""Tests for pure-Python AgentRuntime, pause/resume, PPO routing, and CLI."""
import pytest

from beauty_agent.cli import build_runtime, run_interactive, run_scripted_demo
from beauty_agent.contracts import ObservationSlot, OwnedProduct, Profile
from beauty_agent.nlp_layer import interpret_candidate_confirmation
from beauty_agent.runtime import AgentRuntime, RoutedAFAPolicy, RuleBasedAFAPolicy
from beauty_agent.runtime_contracts import (
    AFAStepDecision,
    CandidateConfirmationInput,
    ChoiceSelection,
    QuestionCandidate,
    RuntimeTurnRequest,
)


def _obs(variable_id: str, value: str, state: str = "known") -> ObservationSlot:
    return ObservationSlot(
        variable_id=variable_id,
        state=state,
        value=value if state == "known" else None,
        source="user_report",
        confirmed_by_user=True,
    )


def test_two_turn_outdoor_and_products_pause_resume_completes_with_bundle():
    runtime = AgentRuntime()
    req_id = "test-outdoor-1"
    products = [
        OwnedProduct(product_id="synthetic-cleanser-a", version="1.0.0", confirmed=True),
        OwnedProduct(product_id="synthetic-sunscreen-b", version="unknown", confirmed=False),
    ]

    first = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="오늘 야외 일정은 없어요. 세안이랑 가진 제품 루틴을 어떻게 조정할까요?",
            profile=Profile(confirmed=True),
            products=products,
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "sun.outdoor_time": _obs("sun.outdoor_time", "none"),
            },
        )
    )

    assert first.status == "awaiting_user"
    assert "lookup_weather" in first.executed_actions
    assert "lookup_product" in first.executed_actions
    assert first.tool_results["weather:current"].status == "found"
    assert first.tool_results["product:synthetic-cleanser-a"].status == "found"
    assert first.tool_results["product:synthetic-sunscreen-b"].status == "not_found"
    assert len(first.questions) == 1

    # Answer open questions until the runtime completes with a RecommendationBundle.
    resp = first
    answers = {
        "method.water_temperature": "lukewarm",
        "method.tools": "scrub_brush",
        "method.drying": "pat_gently",
        "method.friction": "gentle",
    }
    for _ in range(8):
        if resp.status != "awaiting_user":
            break
        qid = resp.questions[0].id
        val = answers.get(qid, "unknown")
        resp = runtime.handle_turn(
            RuntimeTurnRequest(
                request_id=req_id,
                observations={qid: _obs(qid, val, state="unknown" if val == "unknown" else "known")},
            )
        )

    assert resp.status == "completed", f"unexpected status={resp.status}, questions={resp.questions}, hold={resp.hold_reason}"
    assert resp.afa_handoff is not None
    assert resp.afa_handoff.status == "sufficient"
    assert resp.recommendation is not None
    assert any(item.product_id == "synthetic-cleanser-a" for item in resp.recommendation.owned_product_usage)
    assert any(
        ex.product_id == "synthetic-sunscreen-b" and ex.disposition == "usage_held"
        for ex in resp.recommendation.exclusions_or_holds
    )
    assert len(resp.recommendation.alternatives) >= 1


def test_routed_ppo_policy_short_circuits_b_c02_and_falls_back_cleanly():
    class FakePPOPolicy:
        def decide_step(self, observations, available_features, *, can_stop_sufficient, can_stop_insufficient=True):
            slot_ids = [c.slot_id for c in available_features]
            if any(s not in ("method.tools", "method.friction", "method.drying") for s in slot_ids):
                raise ValueError("outside B-C02 scope")
            if can_stop_sufficient:
                return AFAStepDecision(action="stop", stop_reason="sufficient", policy_source="ppo_model")
            if "method.tools" in slot_ids:
                return AFAStepDecision(action="acquire", target_feature="method.tools", policy_source="ppo_model")
            if slot_ids:
                return AFAStepDecision(action="acquire", target_feature=slot_ids[0], policy_source="ppo_model")
            return AFAStepDecision(action="stop", stop_reason="insufficient", policy_source="ppo_model")

    runtime = AgentRuntime(afa_policy=RoutedAFAPolicy(ppo_policy=FakePPOPolicy()))
    req_id = "test-ppo-c02"

    # Turn 1: cleansing_method triggers B-C01 + B-C02; water_temperature is answered upfront,
    # so only B-C02 slots remain and FakePPOPolicy handles the step.
    t1 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="세안 방법 확인하고 싶어요",
            profile=Profile(confirmed=True),
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "method.water_temperature": _obs("method.water_temperature", "lukewarm"),
            },
        )
    )
    assert t1.status == "awaiting_user"
    assert t1.questions[0].id == "method.tools"

    # Turn 2: answering scrub_brush resolves B-C02 immediately, skipping friction and drying.
    t2 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            observations={"method.tools": _obs("method.tools", "scrub_brush")},
        )
    )
    assert t2.status == "completed"
    assert t2.afa_handoff is not None
    assert t2.afa_handoff.policy_source == "ppo_model"
    assert t2.afa_handoff.asked_feature_order == ["method.tools"]


@pytest.mark.parametrize("invalid", [
    AFAStepDecision(action="acquire", target_feature="unsupported", policy_source="ppo_model"),
    AFAStepDecision(action="stop", stop_reason="sufficient", policy_source="ppo_model"),
    AFAStepDecision(action="stop", stop_reason="insufficient", policy_source="ppo_model"),
])
def test_runtime_asks_an_allowed_question_when_policy_proposes_invalid_action(invalid):
    class InvalidPolicy:
        def decide_step(self, observations, available_features, **permissions):
            assert not permissions["can_stop_sufficient"]
            assert not permissions["can_stop_insufficient"]
            available_features.clear()
            observations.clear()
            return invalid

    runtime = AgentRuntime(afa_policy=InvalidPolicy())
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id="invalid-policy-action",
        message="세안 방법 확인하고 싶어요",
        observations={
            "method.body_site": _obs("method.body_site", "face"),
            "method.water_temperature": _obs("method.water_temperature", "lukewarm"),
        },
    ))
    assert response.status == "awaiting_user"
    assert response.questions[0].id in {"method.tools", "method.friction", "method.drying"}
    assert "method.body_site" in runtime.get_session("invalid-policy-action").confirmed_observations


def test_runtime_holds_unresolved_cleansing_after_declined_answers():
    runtime = AgentRuntime()
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id="declined-cleansing",
        message="세안 방법 확인하고 싶어요",
        observations={
            "method.body_site": _obs("method.body_site", "face"),
            "method.water_temperature": _obs("method.water_temperature", "lukewarm"),
            **{key: _obs(key, None, "declined")
               for key in ("method.tools", "method.friction", "method.drying")},
        },
    ))
    assert response.status == "held"
    assert response.recommendation is None
    assert set(response.afa_handoff.unanswered_or_declined) == {
        "method.tools", "method.friction", "method.drying",
    }


def test_missing_checkpoint_uses_rule_policy(tmp_path):
    with pytest.warns(RuntimeWarning, match="using rule-based AFA"):
        runtime = build_runtime(tmp_path / "absent.zip", use_remote_jev=False)
    assert runtime.afa_policy.ppo_policy is None


def test_ppo_is_not_called_for_another_kb_card():
    class MustNotRun:
        def decide_step(self, *args, **kwargs):
            pytest.fail("B-C02 PPO was called for an outdoor request")

    runtime = AgentRuntime(afa_policy=RoutedAFAPolicy(ppo_policy=MustNotRun()))
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id="outside-c02", message="오늘 야외에 오래 있을 거예요",
        observations={"method.body_site": _obs("method.body_site", "face")},
    ))
    assert "B-P01" in runtime.get_session("outside-c02").active_cards
    assert response.status == "held"
    assert response.required_product_evidence == ["product.spf", "product.uva"]
    assert response.afa_handoff.policy_source == "rule_baseline"


def test_b_c05_uses_rule_questions_and_b_b01_preserves_the_mandatory_hold():
    class MustNotRun:
        def decide_step(self, *args, **kwargs):
            pytest.fail("B-C02 PPO was called outside its scope")

    runtime = AgentRuntime(afa_policy=RoutedAFAPolicy(ppo_policy=MustNotRun()))
    first = runtime.handle_turn(RuntimeTurnRequest(
        request_id="repeat-washing", observations={
            "method.body_site": _obs("method.body_site", "face"),
            "cleansing.target_load": _obs("cleansing.target_load", "no_additional_removal_need"),
        },
    ))
    assert "B-C05" in runtime.get_session("repeat-washing").active_cards
    assert first.status == "awaiting_user"
    assert first.questions[0].id == "cleansing.repeat_wash"
    held = runtime.handle_turn(RuntimeTurnRequest(
        request_id="persistent-discomfort", observations={
            "method.body_site": _obs("method.body_site", "face"),
            "skin.current_discomfort": _obs("skin.current_discomfort", "persistent"),
        },
    ))
    assert "B-B01" in runtime.get_session("persistent-discomfort").active_cards
    assert held.status == "held"
    assert held.recommendation is None


@pytest.mark.parametrize("send_repeat_on_resume", [False, True])
def test_cleansing_topic_keeps_repeat_washing_in_the_same_request(send_repeat_on_resume):
    runtime = AgentRuntime()
    request_id = "cleansing-plus-repeat"
    repeat_load = {"cleansing.target_load": _obs("cleansing.target_load", "no_additional_removal_need")}
    tools = {"method.tools": _obs("method.tools", "scrub_brush")}
    first = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        message="세안 방법을 확인해 주세요",
        observations={
            "method.body_site": _obs("method.body_site", "face"),
            "method.water_temperature": _obs("method.water_temperature", "lukewarm"),
            **({} if send_repeat_on_resume else {**tools, **repeat_load}),
        },
    ))
    if send_repeat_on_resume:
        assert first.status == "awaiting_user"
        assert [q.id for q in first.questions] == ["method.tools"]
        first = runtime.handle_turn(RuntimeTurnRequest(
            request_id=request_id, observations={**tools, **repeat_load},
        ))
    session = runtime.get_session(request_id)
    assert set(session.active_cards) == {"B-C01", "B-C02", "B-C05"}
    assert session.card_selection_reasons["B-C05"] == ["observation:cleansing.target_load"]
    assert [q.id for q in first.questions] == ["cleansing.repeat_wash"]

    final = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        observations={"cleansing.repeat_wash": _obs("cleansing.repeat_wash", "habitual_without_reason")},
    ))
    assert final.status == "completed"
    assert {"kb:B-C02", "kb:B-C05"} <= {
        ref for item in final.recommendation.lifestyle_adjustments for ref in item.evidence_refs
    }


def test_persistent_discomfort_preempts_cleansing_recommendation():
    runtime = AgentRuntime()
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id="cleansing-plus-discomfort",
        message="세안 방법을 확인해 주세요",
        observations={
            "method.body_site": _obs("method.body_site", "face"),
            "method.water_temperature": _obs("method.water_temperature", "lukewarm"),
            "method.tools": _obs("method.tools", "scrub_brush"),
            "skin.current_discomfort": _obs("skin.current_discomfort", "persistent"),
        },
    ))
    assert "B-B01" in runtime.get_session("cleansing-plus-discomfort").active_cards
    assert response.status == "held"
    assert response.recommendation is None and not response.questions


def test_exhausted_questions_do_not_turn_missing_product_facts_into_a_recommendation():
    runtime = AgentRuntime()
    request_id = "repeat-without-evidence"
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        products=[OwnedProduct(product_id="synthetic-cleanser-a", version="1.0.0", confirmed=True)],
        observations={
            "method.body_site": _obs("method.body_site", "face"),
            "cleansing.target_load": _obs("cleansing.target_load", "no_additional_removal_need"),
            "cleansing.repeat_wash": _obs("cleansing.repeat_wash", None, "declined"),
            "cleansing.steps": _obs("cleansing.steps", None, "declined"),
            "dose.frequency": _obs("dose.frequency", None, "declined"),
            "method.current_routine": _obs("method.current_routine", None, "declined"),
        },
    ))
    assert response.tool_results["product:synthetic-cleanser-a"].status == "found"
    assert response.required_product_evidence == ["product.instructions"]
    assert response.status == "held" and response.afa_handoff.status == "insufficient"
    assert not response.questions and response.recommendation is None


def test_answer_free_retries_reuse_the_pending_shared_question():
    class RecordingPolicy(RuleBasedAFAPolicy):
        def __init__(self):
            self.candidates = []

        def decide_step(self, observations, available_features, **permissions):
            self.candidates.append(available_features)
            return super().decide_step(observations, available_features, **permissions)

    policy = RecordingPolicy()
    runtime = AgentRuntime(afa_policy=policy)
    request_id = "shared-body-site"
    request = RuntimeTurnRequest(
        request_id=request_id, message="세안 방법을 확인해 주세요",
        observations={"cleansing.target_load": _obs("cleansing.target_load", "no_additional_removal_need")},
    )
    first = runtime.handle_turn(request)
    assert [question.id for question in first.questions] == ["method.body_site"]
    shared = [item for item in policy.candidates[0] if item.slot_id == "method.body_site"]
    assert len(shared) == 1 and set(shared[0].card_ids) == {"B-C01", "B-C02", "B-C05"}
    before = runtime.get_session(request_id)
    for replay in (RuntimeTurnRequest(request_id=request_id, message="  "), request):
        retry = runtime.handle_turn(replay)
        assert retry.status == "awaiting_user" and retry.questions == first.questions
        assert not retry.executed_actions and retry.tool_results == first.tool_results
    assert runtime.get_session(request_id) == before and len(policy.candidates) == 1
    resumed = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        observations={"method.body_site": _obs("method.body_site", "face")},
    ))
    assert len(policy.candidates) == 2 and resumed.questions
    assert all(q.id != "method.body_site" for q in resumed.questions)


def test_pending_question_does_not_hide_a_new_mandatory_hold():
    runtime = AgentRuntime()
    request_id = "updated-while-waiting"
    first = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, message="세안 방법을 확인해 주세요",
        observations={"method.body_site": _obs("method.body_site", "face")},
    ))
    assert first.status == "awaiting_user"
    held = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id,
        observations={"skin.current_discomfort": _obs("skin.current_discomfort", "persistent")},
    ))
    assert held.status == "held" and not held.questions
    assert runtime.get_session(request_id).pending_question is None


def test_default_c02_question_order_prefers_tools():
    candidates = [QuestionCandidate(slot_id=f"method.{key}", question_text="합성 질문", card_ids=["B-C02"])
                  for key in ("drying", "friction", "tools")]
    decision = RuleBasedAFAPolicy().decide_step({}, candidates, can_stop_sufficient=False)
    assert decision.target_feature == "method.tools"


def test_mandatory_safety_hold_stops_immediately():
    runtime = AgentRuntime()
    resp = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id="test-safety",
            message="얼굴이 너무 아파요",
            profile=Profile(confirmed=True),
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "skin.pain": _obs("skin.pain", "new_severe"),
            },
        )
    )
    assert resp.status == "held"
    assert "hold" in resp.executed_actions
    assert resp.hold_reason is not None


def test_conflict_triggers_resolve_conflict_and_resumes():
    runtime = AgentRuntime()
    req_id = "test-conflict"
    t1 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="세안 루틴",
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "method.water_temperature": _obs("method.water_temperature", "hot"),
            },
        )
    )
    assert t1.status == "awaiting_user"

    # Conflicting value without resolve_conflicts triggers resolve_conflict
    t2 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            observations={"method.water_temperature": _obs("method.water_temperature", "lukewarm")},
        )
    )
    assert t2.status == "awaiting_user"
    assert "resolve_conflict" in t2.executed_actions

    # Resolving conflict explicitly clears it
    t3 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            observations={"method.water_temperature": _obs("method.water_temperature", "lukewarm")},
            resolve_conflicts=("method.water_temperature",),
        )
    )
    assert "resolve_conflict" not in t3.executed_actions


def test_cli_scripted_demo_runs_cleanly(capsys):
    runtime = build_runtime(use_remote_jev=False)
    run_scripted_demo(runtime)
    captured = capsys.readouterr()
    assert "--- Turn 1 ---" in captured.out
    assert "--- Turn 2" in captured.out


def test_cli_default_uses_myopic_with_numbered_answers(monkeypatch, capsys):
    for key in ("AURORA_CLUSTER_ARN", "AURORA_SECRET_ARN", "AURORA_DATABASE"):
        monkeypatch.delenv(key, raising=False)
    dialogue = iter([
        "얼굴을 미온수로 세안해요. 세안 방법을 확인해 주세요.",
        "손으로 세안해요.",
        "99",
        "1",
        "1",
        "1",
        "/quit",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(dialogue))
    runtime = build_runtime(use_remote_jev=False)
    analyzed = []
    analyze = runtime.nlp_layer.analyze

    def track_analysis(message, **kwargs):
        analyzed.append(message)
        return analyze(message, **kwargs)

    monkeypatch.setattr(runtime.nlp_layer, "analyze", track_analysis)
    run_interactive(runtime)
    output = capsys.readouterr().out
    assert "질문 정책: Myopic VOI" in output
    assert output.index("질문 [method.tools]") < output.index("질문 [method.drying]") < output.index(
        "질문 [method.friction]"
    )
    assert "[상태: completed] (실행: recommend)" in output
    assert len(analyzed) == 1
    assert "1. 손으로만 세안" in output
    assert "모르겠어요" in output and "건너뛰기" in output
    assert output.count("화면에 나온 선택지 번호") == 2


@pytest.mark.parametrize(("choice_id", "status"), [("recent", "awaiting_user"), ("repeated", "held")])
def test_myopic_scores_symptom_confirmation_as_a_question(choice_id, status):
    runtime = build_runtime(use_remote_jev=False)
    request_id = "myopic-symptom"
    first = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, message="어제 손으로 세안했는데 아침에 일어나니까 턱에 뾰루지가 났네",
    ))
    question = first.questions[0]
    session = runtime.get_session(request_id)
    assert first.pending_action == "ask_user" and "confirm_candidate" not in first.executed_actions
    assert session.afa_step_decision == AFAStepDecision(
        action="acquire", target_feature=question.id, policy_source="myopic_voi",
    )
    scores = {score.slot_id: score for score in session.afa_question_scores}
    assert scores[question.id].reason == "selected"
    assert scores[question.id].decision_change_rate > 0
    assert "method.drying" in scores
    assert "skin.current_discomfort" not in session.confirmed_observations
    assert len(question.choices) == 5
    assert question.choices[0].id == "recent"
    result = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, choice_selection=ChoiceSelection(
            turn_index=question.turn_index, question_id=question.id, choice_id=choice_id,
        ),
    ))
    assert result.nlp is None and result.status == status
    if status == "held":
        assert not result.questions and runtime.get_session(request_id).afa_step_decision is None
    else:
        assert result.pending_action == "ask_user" and result.questions[0].id == "method.drying"


def test_interactive_cleansing_answers_without_unrelated_sunscreen(monkeypatch, capsys):
    dialogue = iter([
        "얼굴을 미온수로 씻어요. 세안 방법을 확인해 주세요.",
        "2",
        "/quit",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(dialogue))
    run_interactive(AgentRuntime(auto_apply_nlp_features=True))

    output = capsys.readouterr().out
    assert output.count("  ? 질문") == 1
    assert "질문 [method.tools]" in output
    assert "[상태: completed]" in output
    assert "합성 순한 폼클렌저 A" in output
    assert "대체 자외선 차단제" not in output
    assert "synthetic-sunscreen-b" not in output


def test_korean_slot_answer_mapping_prevents_not_applicable_trap():
    from beauty_agent.nlp_layer import interpret_slot_answer

    assert interpret_slot_answer("method.body_site", "얼굴에 써요") == ("known", "face")
    assert interpret_slot_answer("method.water_temperature", "미온수로 씻어요") == ("known", "lukewarm")
    assert interpret_slot_answer("method.tools", "세안 브러시 써") == ("known", "scrub_brush")
    assert interpret_slot_answer("method.tools", "아니") == ("known", "hands")
    assert interpret_slot_answer("method.tools", "안 써요") == ("known", "hands")
    assert interpret_slot_answer("method.friction", "살살 씻어요") == ("known", "gentle")
    assert interpret_slot_answer("method.drying", "수건으로 톡톡 닦아요") == ("known", "pat_gently")
    assert interpret_slot_answer("method.tools", "모르겠어요") == ("unknown", None)


def test_upfront_nlp_feature_extraction_skips_already_stated_questions():
    runtime = AgentRuntime(auto_apply_nlp_features=True)
    resp = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id="test-upfront",
            message="얼굴에 미온수로 세안 브러시 써서 씻고 있어요",
            profile=Profile(confirmed=True),
        )
    )
    # body_site=face, water_temperature=lukewarm, tools=scrub_brush are all extracted upfront,
    # so B-C01 and B-C02 resolve immediately without re-asking any of them!
    assert resp.status == "completed"
    assert resp.afa_handoff is not None
    assert resp.afa_handoff.asked_feature_order == []
    assert resp.afa_handoff.acquired_features["method.tools"].value == "scrub_brush"


def test_unrecognized_known_value_triggers_reask_and_updates_without_conflict():
    runtime = AgentRuntime()
    req_id = "test-unrecognized"
    t1 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="세안 방법",
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "method.water_temperature": _obs("method.water_temperature", "warm"),
            },
        )
    )
    assert t1.status == "awaiting_user"
    assert any(q.id == "method.water_temperature" for q in t1.questions)

    t2 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            observations={"method.water_temperature": _obs("method.water_temperature", "lukewarm")},
        )
    )
    assert "resolve_conflict" not in t2.executed_actions
    assert runtime.get_session(req_id).confirmed_observations["method.water_temperature"].value == "lukewarm"


@pytest.mark.parametrize("use_choice", [False, True])
def test_confirm_candidate_persistent_symptom_triggers_safety_hold(use_choice):
    runtime = AgentRuntime(auto_apply_nlp_features=True)
    req_id = "test-confirm-persistent"
    t1 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="얼굴에 세안하고 볼이 따가워요",
            profile=Profile(confirmed=True),
        )
    )
    assert t1.status == "awaiting_user"
    assert "confirm_candidate" in t1.executed_actions
    question = t1.questions[0]
    cid = question.id
    assert cid.startswith("clarify:")

    conf = interpret_candidate_confirmation("네 며칠째 계속 따가워요")
    assert conf is not None and conf.persistence == "persistent"
    if use_choice:
        choice = next(option for option in question.choices if option.label == "본인에게 계속 있었음")
        request = RuntimeTurnRequest(request_id=req_id, choice_selection=ChoiceSelection(
            turn_index=question.turn_index, question_id=cid, choice_id=choice.id,
        ))
    else:
        request = RuntimeTurnRequest(request_id=req_id, confirmations={cid: conf})
    t2 = runtime.handle_turn(request)
    assert t2.status == "held"
    assert "hold" in t2.executed_actions
    assert t2.nlp is None


def test_confirm_candidate_denied_or_recent_proceeds_to_afa_completion():
    runtime = AgentRuntime(auto_apply_nlp_features=True)
    req_id = "test-confirm-denied"
    t1 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="얼굴에 미온수로 세안 브러시 쓰고 따가워요",
            profile=Profile(confirmed=True),
        )
    )
    assert t1.status == "awaiting_user"
    assert "confirm_candidate" in t1.executed_actions
    cid = t1.questions[0].id

    conf = interpret_candidate_confirmation("아니요 친구 얘기였어요")
    assert conf is not None and conf.subject == "other"
    t2 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            confirmations={cid: conf},
        )
    )
    assert t2.status == "completed"
    assert t2.recommendation is not None


def test_interpret_candidate_confirmation_variants():
    c1 = interpret_candidate_confirmation("응 어제 잠깐 났어")
    assert c1 == CandidateConfirmationInput(subject="self", state="affirmed", persistence="recent")

    c2 = interpret_candidate_confirmation("자주 반복돼요")
    assert c2 == CandidateConfirmationInput(subject="self", state="affirmed", persistence="repeated")

    c3 = interpret_candidate_confirmation("모르겠어요")
    assert c3 == CandidateConfirmationInput(subject="unknown", state="unknown")


def test_b_c05_korean_slot_answer_mapping():
    from beauty_agent.nlp_layer import interpret_slot_answer

    assert interpret_slot_answer("cleansing.target_load", "땀을 많이 흘렸어요") == ("known", "heavy_sweat")
    assert interpret_slot_answer("cleansing.target_load", "선크림이랑 메이크업을 지워야 해요") == ("known", "makeup_requires_removal")
    assert interpret_slot_answer("cleansing.target_load", "특별히 없어요") == ("known", "no_additional_removal_need")
    assert interpret_slot_answer("cleansing.repeat_wash", "그냥 습관적으로 두 번 씻어요") == ("known", "habitual_without_reason")
    assert interpret_slot_answer("cleansing.repeat_wash", "메이크업 제거 목적이에요") == ("known", "purpose_matched")


def test_c02_question_order_prefers_tools_even_when_b_c05_is_open():
    candidates = [
        QuestionCandidate(slot_id="method.drying", question_text="q1", card_ids=["B-C02"]),
        QuestionCandidate(slot_id="method.friction", question_text="q2", card_ids=["B-C02"]),
        QuestionCandidate(slot_id="method.tools", question_text="q3", card_ids=["B-C02"]),
        QuestionCandidate(slot_id="cleansing.target_load", question_text="q4", card_ids=["B-C05"]),
    ]
    decision = RuleBasedAFAPolicy().decide_step({}, candidates, can_stop_sufficient=False)
    assert decision.target_feature == "method.tools"


def test_conflict_retry_preserves_pending_action_without_reexecuting():
    runtime = AgentRuntime()
    req_id = "test-conflict-retry"
    runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="세안 루틴",
            observations={
                "method.body_site": _obs("method.body_site", "face"),
                "method.water_temperature": _obs("method.water_temperature", "hot"),
            },
        )
    )
    t2 = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            observations={"method.water_temperature": _obs("method.water_temperature", "lukewarm")},
        )
    )
    assert t2.pending_action == "resolve_conflict"
    assert t2.executed_actions == ["resolve_conflict"]

    retry = runtime.handle_turn(RuntimeTurnRequest(request_id=req_id))
    assert retry.status == "awaiting_user"
    assert not retry.executed_actions
    assert retry.pending_action == "resolve_conflict"
    assert retry.questions == t2.questions


def test_rule_policy_subclass_still_uses_outcome_ranking():
    class SubclassedRulePolicy(RuleBasedAFAPolicy):
        def __init__(self):
            self.seen_orders = []

        def decide_step(self, observations, available_features, **permissions):
            self.seen_orders.append([c.slot_id for c in available_features])
            return super().decide_step(observations, available_features, **permissions)

    policy = SubclassedRulePolicy()
    runtime = AgentRuntime(afa_policy=policy, prioritize_question_outcomes=True)
    resp = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id="subclass-rank",
            message="반복 세안과 평소 세안 방법을 같이 점검하고 싶어요.",
            observations={"method.body_site": _obs("method.body_site", "face")},
        )
    )
    assert resp.status == "awaiting_user"
    assert policy.seen_orders[0][0] == "cleansing.target_load"
