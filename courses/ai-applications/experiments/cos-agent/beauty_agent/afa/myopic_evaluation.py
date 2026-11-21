"""Compare fixed-order, Myopic VOI and optionally routed PPO on the same cases."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from beauty_agent.afa.question_priority import MyopicVOIAFAPolicy, decision_signature
from beauty_agent.contracts import ObservationSlot
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime import AgentRuntime, RoutedAFAPolicy, RuleBasedAFAPolicy
from beauty_agent.runtime_contracts import RuntimeTurnRequest
from .v67_fixtures import BUNDLE, read_rows, verify


ROOT = Path(__file__).resolve().parents[6]
BRANCH_CARDS = (
    "B-C01", "B-C02", "B-C05", "B-M01", "B-M02", "B-P02", "B-P03",
    "B-I01", "B-I02", "B-I03",
)


@dataclass(frozen=True)
class Case:
    id: str
    family: str
    cohort: str
    cards: tuple[str, ...]
    initial: dict[str, ObservationSlot]
    answers: dict[str, ObservationSlot]
    lineage: dict


def synthetic_observation(field, value=None, state="known"):
    return ObservationSlot(variable_id=field, value=value, state=state,
                           source="synthetic_fixture", confirmed_by_user=True)


def branch_worlds(adapter):
    """Enumerate authored clauses with consumer-answerable predicates only."""
    for card in BRANCH_CARDS:
        for branch in adapter.engine.rules[card]:
            predicates = branch["when"]
            if not predicates or any(
                field.startswith("product.")
                or not adapter.engine.variables.get(field, {}).get("consumer_question_allowed")
                for field in predicates
            ):
                continue
            fields = sorted(predicates)
            for index, values in enumerate(product(*(predicates[field] for field in fields)), 1):
                yield card, branch["branch_id"], index, dict(zip(fields, values, strict=True))


def branch_cases(adapter):
    for card, branch, world, values in branch_worlds(adapter):
        # Compare cold starts with one dependency already supplied in multivariate clauses.
        reveal_options = [None, next(iter(values))] if len(values) > 1 else [None]
        for reveal in reveal_options:
            yield structured_case(
                f"{branch}:{world}:{'prefill' if reveal else 'cold'}", branch, "kb_branch",
                (card,), values, initial_fields=[reveal] if reveal else [],
                lineage={"kb_branch": branch, "value_combination": world},
            )


def structured_case(case_id, family, cohort, cards, values, *, initial_fields=(), lineage=None):
    initial = {"method.body_site": synthetic_observation("method.body_site", "face")}
    answers = {field: synthetic_observation(field, value) for field, value in values.items()}
    for field in initial_fields:
        initial[field] = answers.pop(field)
    return Case(case_id, family, cohort, cards, initial, answers, lineage or {})


def boundary_cases():
    rows = (
        ("sun-label-unavailable", ("B-P01",), {"sun.outdoor_time": "prolonged"}),
        ("aha-evidence-unavailable", ("B-I04",), {
            "method.current_routine": "aha_strengthened_protection_omitted",
        }),
        ("routine-cross-domain", ("B-C01", "B-M01", "B-P03", "B-I02"), {
            "method.water_temperature": "lukewarm",
            "method.current_routine": "moisturizing_not_needed_no_discomfort",
            "sun.reapplication": "matched_to_exposure_and_label", "sun.pilling": "none",
        }),
        ("layering-with-reapplication", ("B-P03", "B-I02"), {
            "sun.outdoor_time": "prolonged", "sun.reapplication": "matched_to_exposure_and_label",
            "sun.pilling": "present",
        }),
        ("sunscreen-removal", ("B-C05", "B-P02", "B-I01"), {
            "cleansing.target_load": "makeup_requires_removal",
            "cleansing.steps": "repeated_only_because_water_resistant",
            "sun.coverage_gaps": "intentional_exposed_gaps",
        }),
        ("hold-preempts-sun", ("B-M02", "B-P03"), {
            "moisturizing.comfort": "persistent_stinging",
            "sun.reapplication": "matched_to_exposure_and_label",
        }),
    )
    for name, cards, values in rows:
        # These paired conditions share one scenario family across reveal variants.
        for reveal in ((), (next(iter(values)),)):
            yield structured_case(
                f"{name}:{'prefill' if reveal else 'cold'}", name, "authored_boundary", cards, values,
                initial_fields=reveal,
            )


def v67_cases():
    verify()
    for row in read_rows(BUNDLE / "fixtures.jsonl"):
        yield Case(
            row["fixture_id"], row["lineage"]["scenario_family_id"], "v67_e22_train", ("B-C02",),
            {field: ObservationSlot.model_validate(value)
             for field, value in row["initial_public"]["observations"].items()},
            {field: ObservationSlot.model_validate(value)
             for field, value in row["environment_only"]["response_table"].items()},
            {**row["lineage"], "response_provenance": {
                field: origin["kind"] for field, origin in row["environment_only"]["response_provenance"].items()
            }},
        )


class FixedCardsRuntime(AgentRuntime):
    """Freeze the active cards so the comparison isolates question selection."""

    def __init__(self, cards, **kwargs):
        super().__init__(**kwargs)
        self.cards = cards

    def _select_cards(self, state, topic_hints, observations):
        state.active_cards = list(self.cards)
        return state.active_cards


class TracedRoutedPolicy(RoutedAFAPolicy):
    """Observe the existing router without changing policy decisions or permissions."""

    last_decision = None
    called = False

    def decide_step(self, *args, **kwargs):
        self.called = True
        self.last_decision = super().decide_step(*args, **kwargs)
        return self.last_decision

    def source_for(self, response):
        if not self.called:
            return "rule_outside_ppo_scope"
        decision = self.last_decision
        if decision is not None and decision.policy_source == "ppo_model":
            if response.pending_action == "ask_user":
                if decision.action == "acquire" and decision.target_feature == response.questions[0].id:
                    return "ppo_model"
            elif response.afa_handoff is not None and response.afa_handoff.policy_source == "ppo_model":
                return "ppo_model"
        return "rule_after_ppo_attempt"


def replay(case, adapter, policy, *, full=False, observe_turn=None):
    myopic = isinstance(policy, MyopicVOIAFAPolicy)
    traced = isinstance(policy, TracedRoutedPolicy)
    runtime = FixedCardsRuntime(case.cards, kb_adapter=adapter, afa_policy=policy,
                                prioritize_question_outcomes=False)
    initial = case.initial | case.answers if full else case.initial
    def turn(observations):
        if traced:
            policy.called = False
            policy.last_decision = None
        request = RuntimeTurnRequest(request_id=case.id, observations=observations)
        if observe_turn is not None:
            return observe_turn(runtime, request)
        return runtime.handle_turn(request)

    response = turn(initial)
    asked = []
    sources = []
    fallbacks = 0
    while response.pending_action == "ask_user":
        field = response.questions[0].id
        if field in initial or field in asked or field.startswith("product."):
            raise ValueError(f"{case.id}: repeated or non-acquirable slot: {field}")
        if myopic and not runtime.get_session(case.id).afa_question_scores:
            fallbacks += 1
        asked.append(field)
        if traced:
            sources.append(policy.source_for(response))
        answer = case.answers.get(field)
        if answer is None:
            if case.cohort == "v67_e22_train":
                raise ValueError(f"{case.id}: no E22 response for {field}")
            answer = synthetic_observation(field, state="unknown")
        response = turn({field: answer})
    handoff = response.afa_handoff
    if myopic and handoff is not None and handoff.policy_source != "myopic_voi":
        fallbacks += 1
    if response.status == "awaiting_user":
        raise ValueError(f"{case.id}: unexpected conversational action: {response.pending_action}")
    observed = runtime.get_session(case.id).confirmed_observations
    overall, holds, retrieve, guidance = decision_signature(adapter.evaluate(observed, list(case.cards)))
    result = {
        "questions": asked, "fallback_steps": fallbacks,
        "effect": {"status": response.status, "overall": overall, "hold_signals": holds,
                   "retrieve_slots": retrieve, "guidance": guidance,
                   "runtime_required_product_evidence": response.required_product_evidence},
    }
    if traced:
        stop_source = policy.source_for(response) if handoff is not None else "runtime_hold"
        result.update(question_sources=sources, stop_source=stop_source,
                      fallback_steps=sources.count("rule_after_ppo_attempt")
                      + int(stop_source == "rule_after_ppo_attempt"))
    return result


def summarize(rows, policies=("baseline", "myopic")):
    count = len(rows)
    summary = {
        "cases": count, "families": len({(row["cohort"], row["family"]) for row in rows}),
        "worlds": len({json.dumps([row["cards"], row["initial"] | row["answers"]], sort_keys=True)
                       for row in rows}),
        "agreement_count": sum(row["agreement"] for row in rows),
        "status_agreement_count": sum(row["status_agreement"] for row in rows),
    }
    for policy in policies:
        total = sum(len(row[policy]["questions"]) for row in rows)
        summary[policy] = {
            "questions": total, "mean_questions": total / count,
            "matches_full_input": sum(row[policy]["matches_full_input"] for row in rows),
            "fallback_steps": sum(row[policy]["fallback_steps"] for row in rows),
            "statuses": dict(Counter(row[policy]["effect"]["status"] for row in rows)),
        }
    return summary


def evaluate(adapter=None, *, ppo_policy=None, dependency_depths=()):
    adapter = adapter or KBEngineAdapter()
    cases = [*branch_cases(adapter), *boundary_cases(), *v67_cases()]
    if len({case.id for case in cases}) != len(cases):
        raise ValueError("duplicate fixture ID")
    baseline, myopic = RuleBasedAFAPolicy(), MyopicVOIAFAPolicy(stop_lookahead=1)
    policies = {"baseline": baseline, "myopic": myopic}
    if ppo_policy is not None:
        policies["ppo_routed"] = TracedRoutedPolicy(ppo_policy, baseline=baseline)
    if any(depth not in (2, 3) for depth in dependency_depths):
        raise ValueError("dependency comparison depths must be 2 or 3")
    policies.update({f"myopic_stop_{depth}": MyopicVOIAFAPolicy(stop_lookahead=depth)
                     for depth in dependency_depths})
    rows = []
    for case in cases:
        reference = replay(case, adapter, baseline, full=True)
        results = {name: replay(case, adapter, policy) for name, policy in policies.items()}
        left, right = results["baseline"], results["myopic"]
        for result in results.values():
            result["matches_full_input"] = result["effect"] == reference["effect"]
        rows.append({
            "id": case.id, "family": case.family, "cohort": case.cohort, "cards": case.cards,
            "initial": {field: obs.model_dump(mode="json") for field, obs in case.initial.items()},
            "answers": {field: obs.model_dump(mode="json") for field, obs in case.answers.items()},
            "lineage": case.lineage, "full_input_effect": reference["effect"],
            "full_input_unknown_questions": reference["questions"], **results,
            "agreement": left["effect"] == right["effect"],
            "status_agreement": left["effect"]["status"] == right["effect"]["status"],
        })

    sources = [Path(__file__), Path(__file__).with_name("question_priority.py"),
               Path(__file__).with_name("v67_fixtures.py"),
               Path(__file__).parents[1] / "runtime.py", Path(__file__).parents[1] / "runtime_contracts.py",
               Path(__file__).parents[1] / "modules/kb_adapter.py", BUNDLE / "manifest.json",
               BUNDLE / "fixtures.jsonl", ROOT / "skin_engine/kb_preview/rules.json",
               ROOT / "skin_engine/kb_preview/engine.py", ROOT / "skin_engine/kb_preview/special.py"]
    if ppo_policy is not None:
        sources.append(Path(__file__).with_name("policy_adapter.py"))
    report = {
        "mode": "development_preview", "production_enabled": False, "independent_evaluation": False,
        "sampling": "deterministic KB clauses, authored boundaries, and v67 E22 train-derived cases",
        "response_assumption": "fixed answer table, unlisted generated answers are unknown",
        "reference": "same runtime with all scripted responses initially supplied; subsequent unlisted answers unknown",
        "seed": None, "repetitions_per_case_per_policy": 1, "kb_sha256": adapter.engine.sha,
        "source_sha256": {file.relative_to(ROOT).as_posix(): sha256(file.read_bytes()).hexdigest()
                          for file in sources},
        "summary": summarize(rows, policies),
        "by_cohort": {cohort: summarize([row for row in rows if row["cohort"] == cohort], policies)
                      for cohort in sorted({row["cohort"] for row in rows})},
        "by_axis": {axis: summarize([row for row in rows if {card[2] for card in row["cards"]} == {axis}], policies)
                    for axis in ("C", "M", "P", "I")},
        "multi_axis": summarize([row for row in rows if len({card[2] for card in row["cards"]}) > 1], policies),
        "rows": rows,
    }
    if len(policies) > 2:
        report["pairwise_agreements"] = {
            f"{a}_vs_{b}": sum(row[a]["effect"] == row[b]["effect"] for row in rows)
            for a, b in combinations(policies, 2)
        }
    if ppo_policy is not None:
        model_questions = [row for row in rows if "ppo_model" in row["ppo_routed"]["question_sources"]]
        report["ppo_coverage"] = {
            "question_sources": dict(Counter(source for row in rows
                                            for source in row["ppo_routed"]["question_sources"])),
            "stop_sources": dict(Counter(row["ppo_routed"]["stop_source"] for row in rows)),
            "cases_with_ppo_questions": len(model_questions),
            "cases_with_ppo_activity": sum("ppo_model" in row["ppo_routed"]["question_sources"]
                                           or row["ppo_routed"]["stop_source"] == "ppo_model" for row in rows),
            "ppo_question_cases_only": summarize(model_questions, policies) if model_questions else None,
        }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ppo-model", type=Path, help="Trusted local B-C02 PPO checkpoint.")
    parser.add_argument("--dependency-lookahead", action="append", type=int, choices=(2, 3), default=[],
                        help="Add a stop-only dependency lookahead comparison arm. Repeat to compare depths.")
    args = parser.parse_args()
    if args.ppo_model is None:
        report = evaluate(dependency_depths=args.dependency_lookahead)
    else:
        from .policy_adapter import PPOAFAPolicy

        checkpoint = args.ppo_model.read_bytes()
        report = evaluate(ppo_policy=PPOAFAPolicy(args.ppo_model), dependency_depths=args.dependency_lookahead)
        report["ppo_checkpoint"] = {
            "filename": args.ppo_model.name, "sha256": sha256(checkpoint).hexdigest(), "bytes": len(checkpoint),
            "inference": "deterministic CPU", "route": "existing B-C02 runtime route; fixed-order rules elsewhere",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(json.dumps(report["summary"], indent=2))
    if "ppo_coverage" in report:
        print(json.dumps(report["ppo_coverage"], indent=2))


if __name__ == "__main__":
    main()
