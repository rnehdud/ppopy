from beauty_agent.afa.paired_evaluation import CHALLENGE, POLICY_NAMES, _world_key, evaluate_panel, frozen_cases
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime import RuleBasedAFAPolicy


def test_challenge_panel_uses_distinct_worlds_and_two_disclosure_conditions():
    cases = frozen_cases(KBEngineAdapter())
    historical = [case for case in cases if case.cohort != CHALLENGE]
    challenge = [case for case in cases if case.cohort == CHALLENGE]
    assert len(historical) == 78
    assert len(challenge) == 98
    assert len({_world_key(case) for case in challenge}) == 49
    assert {_world_key(case) for case in historical}.isdisjoint(_world_key(case) for case in challenge)
    assert len({case.family for case in challenge}) == 14


def test_policy_panel_reports_ppo_attribution_and_visible_safety_hold():
    class StubPPO(RuleBasedAFAPolicy):
        def decide_step(self, observations, candidates, **permissions):
            decision = super().decide_step(observations, candidates, **permissions)
            return decision.model_copy(update={"policy_source": "ppo_model"})

    adapter = KBEngineAdapter()
    cases = frozen_cases(adapter)
    chosen = [
        next(case for case in cases if case.id == "B-C02:4:1:cold"),
        next(case for case in cases if case.id == "safety-with-reapplication-1:prefill"),
    ]
    result = evaluate_panel(adapter, chosen, StubPPO())
    assert result["overall"]["reference_errors"] == 0
    assert result["overall"]["ppo_attribution"]["conditions_with_model_questions"] == 1
    assert result["b_c02_only"]["conditions"] == 1
    held = result["rows"][1]
    assert held["reference_mandatory_hold"]
    assert held["ppo_routed"]["stop_source"] == "runtime_hold"
    assert held["current_myopic"]["visible_match"]
    assert not held["current_myopic"]["unsafe_completion"]
    for policy in POLICY_NAMES:
        summary = result["overall"][policy]
        assert summary["product_ask"] == summary["reask"] == summary["hold_miss"] == 0
        assert summary["decision_fidelity"] == summary["exact_matches"] / 2
