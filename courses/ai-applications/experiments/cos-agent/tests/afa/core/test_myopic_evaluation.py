from collections import Counter

from beauty_agent.afa.myopic_evaluation import evaluate, replay, structured_case
from beauty_agent.afa.question_priority import MyopicVOIAFAPolicy
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime import RuleBasedAFAPolicy


def test_expanded_myopic_comparison_preserves_lineage_and_reports_early_holds():
    report = evaluate()
    rows = report["rows"]
    assert len({row["id"] for row in rows}) == report["summary"]["cases"] == 78
    assert report["summary"]["families"] < len(rows)
    assert report["summary"]["worlds"] < len(rows)
    assert set(report["by_axis"]) == {"C", "M", "P", "I"}
    assert report["multi_axis"]["cases"] == 8
    assert report["production_enabled"] is False
    assert all(row["full_input_effect"]["status"] in {"held", "completed"} for row in rows)
    assert all(not slot.startswith("product.") and slot not in row["initial"]
               for row in rows for policy in ("baseline", "myopic") for slot in row[policy]["questions"])
    assert all(row["myopic"]["fallback_steps"] == 0 for row in rows)

    train = [row for row in rows if row["cohort"] == "v67_e22_train"]
    assert len(train) == 4
    assert all(row["lineage"]["effective_split"] == "train" and len(row["lineage"]["parent_sha256"]) == 64
               for row in train)
    states = Counter(obs["state"] for row in train for obs in row["answers"].values())
    assert states == {"known": 8, "unknown": 3, "declined": 1}

    paired = next(row for row in rows if row["id"] == "B-I02:2:1:cold")
    assert not paired["agreement"]
    assert paired["baseline"]["matches_full_input"]
    assert paired["myopic"]["effect"]["status"] == "held"
    assert paired["myopic"]["questions"] == []

    mandatory = next(row for row in rows if row["id"] == "hold-preempts-sun:prefill")
    for policy in ("baseline", "myopic"):
        assert mandatory[policy]["effect"]["status"] == "held"
        assert "refer_for_professional_review" in mandatory[policy]["effect"]["hold_signals"]
        assert not mandatory[policy]["questions"]


def test_routed_ppo_comparison_reports_executed_policy_and_fallback():
    class StubPPO:
        def decide_step(self, observations, candidates, **permissions):
            drying = observations.get("method.drying")
            if drying is not None and drying.value == "pat_gently":
                raise ValueError("simulated model failure")
            decision = RuleBasedAFAPolicy().decide_step(observations, candidates, **permissions)
            return decision.model_copy(update={"policy_source": "ppo_model"})

    report = evaluate(ppo_policy=StubPPO())
    rows = report["rows"]
    coverage = report["ppo_coverage"]
    assert report["summary"]["cases"] == 78
    assert report["pairwise_agreements"]["baseline_vs_ppo_routed"] == 78
    assert coverage["cases_with_ppo_questions"] > 0
    assert coverage["question_sources"]["rule_after_ppo_attempt"] > 0
    assert coverage["question_sources"]["rule_outside_ppo_scope"] > 0
    assert sum(coverage["question_sources"].values()) == report["summary"]["ppo_routed"]["questions"]
    assert sum(coverage["stop_sources"].values()) == len(rows)
    assert all(row["cards"] == ("B-C02",)
               for row in rows if "ppo_model" in row["ppo_routed"]["question_sources"])
    mandatory = next(row for row in rows if row["id"] == "hold-preempts-sun:prefill")
    assert mandatory["ppo_routed"]["stop_source"] == "runtime_hold"


def test_dependency_variants_recover_the_two_and_three_answer_cases():
    report = evaluate(dependency_depths=(2, 3))
    assert report["summary"]["cases"] == 78
    assert report["summary"]["myopic"]["matches_full_input"] == 67
    assert report["summary"]["myopic_stop_2"]["matches_full_input"] == 74
    assert report["summary"]["myopic_stop_2"]["questions"] <= 140
    assert report["summary"]["myopic_stop_3"]["matches_full_input"] == 75
    incomplete = next(row for row in report["rows"] if row["id"] == "B-P03:6:1:prefill")
    assert not incomplete["myopic_stop_2"]["matches_full_input"]
    assert incomplete["myopic_stop_3"]["matches_full_input"]


def test_dependency_check_recovers_on_an_additional_mixed_card_fixture():
    adapter = KBEngineAdapter()
    case = structured_case("additional-light-layering", "mixed", "regression", ("B-C01", "B-I02"), {
        "method.water_temperature": "hot",
        "sun.pilling": "present",
        "sun.reapplication": "reduced_due_to_layering",
    })
    reference = replay(case, adapter, RuleBasedAFAPolicy(), full=True)
    original = replay(case, adapter, MyopicVOIAFAPolicy(stop_lookahead=1))
    updated = replay(case, adapter, MyopicVOIAFAPolicy())
    assert original["effect"]["status"] == "held"
    assert updated["effect"] == reference["effect"]
    assert updated["effect"]["status"] == "completed"
