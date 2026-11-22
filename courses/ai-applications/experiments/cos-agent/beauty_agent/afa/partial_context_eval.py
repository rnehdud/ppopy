"""Compare fixed B-C02 policies with controlled initial observations."""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
from statistics import mean

from beauty_agent.contracts import ObservationSlot
from beauty_agent.runtime_contracts import AFAStepDecision, QuestionCandidate

from .eda import ROOT, fingerprint
from .policy_adapter import AFAOptions, PPOAFAPolicy, run_acquisition
from .ppo_preflight import PROTOCOL, MaskedC02Env
from .tracking import receipt
from .v67_fixtures import SLOTS
from .v67_reward import observed_signature, score_stop


class ToolsFirst:
    def decide_step(self, observations, available_features, *,
                    can_stop_sufficient, can_stop_insufficient=True):
        available_ids = {feature.slot_id for feature in available_features}
        for key in SLOTS:
            if key in available_ids:
                return AFAStepDecision(action="acquire", target_feature=key)
        if can_stop_sufficient:
            return AFAStepDecision(action="stop", stop_reason="sufficient")
        if can_stop_insufficient:
            return AFAStepDecision(action="stop", stop_reason="insufficient")
        raise ValueError("baseline has no permitted decision")


def run_case(env, index, prefilled, policy, *, outcome_signature=None):
    env.reset(seed=0, options={"index": index})
    fixture_id = env.fixture_id
    public = env.session.public
    # The book walks a prefix solely to expose selected recorded values and
    # locate later synthetic replies. The probe never exposes prefix history.
    for key in prefilled:
        public = env.book.answer(fixture_id, public, key)
    initial = {key: ObservationSlot.model_validate(value)
               for key, value in public["observations"].items()}

    def options(observations):
        context = env.session._prepare({
            "message": public["message"], "history": [],
            "observations": {key: slot.model_dump() for key, slot in observations.items()},
        }).context
        allowed = context.enabled()
        if any(offer.action == "hold" and offer.target_id == "safety" for offer in allowed):
            raise ValueError("mandatory safety stop is outside this bounded policy comparison")
        return AFAOptions(
            [QuestionCandidate(slot_id=offer.target_id, question_text=offer.reviewed_text)
             for offer in allowed if offer.action == "ask_user"],
            any(offer.action == "request_draft" for offer in allowed),
            any(offer.action == "hold" and offer.target_id == "insufficient_information"
                for offer in allowed),
        )

    def answer(key):
        nonlocal public
        public = env.book.answer(fixture_id, public, key)
        return ObservationSlot.model_validate(public["observations"][key])

    outcome_reference = env.references[fixture_id]
    if outcome_signature is None:
        observe = observed_signature
    else:
        def observe(adapter, state):
            typed = {key: ObservationSlot.model_validate(value)
                     for key, value in state["observations"].items()}
            return outcome_signature(adapter.evaluate(typed, ["B-C02"]))

        complete = env.book.initial_public(fixture_id)
        for key in SLOTS:
            complete = env.book.answer(fixture_id, complete, key)
        outcome_reference = observe(env.adapter, complete)
    opening = options(initial)
    initial_signature = observe(env.adapter, public)
    if set(prefilled).intersection(feature.slot_id for feature in opening.features):
        raise ValueError("engine reoffered an initially observed feature")
    handoff = run_acquisition(policy, initial, options, answer, max_questions=len(SLOTS))
    final = options({key: ObservationSlot.model_validate(value)
                     for key, value in public["observations"].items()})
    if handoff.status == "sufficient":
        disposition = "draft_allowed"
    elif final.features:
        disposition = "hold_with_question_available"
    elif final.can_stop_sufficient:
        disposition = "hold_with_draft_available"
    else:
        disposition = "hold_without_available_path"
    same = outcome_reference == observe(env.adapter, public)
    score = score_stop(disposition, same, len(handoff.asked_feature_order), PROTOCOL)
    return {
        "fixture_id": fixture_id, "family": env.rows[index]["family"],
        "prefilled": {key: initial[key].state for key in prefilled},
        "initially_sufficient_allowed": opening.can_stop_sufficient,
        "initially_sufficient_reference": (
            opening.can_stop_sufficient and outcome_reference == initial_signature
        ),
        "questions": len(handoff.asked_feature_order),
        "asked_feature_order": handoff.asked_feature_order,
        "reasked": sorted(set(prefilled).intersection(handoff.asked_feature_order)),
        "unanswered_or_declined": handoff.unanswered_or_declined,
        "handoff": handoff.status, **score,
    }


def summarize(rows):
    return {
        "cases": len(rows), "correct": sum(row["correct_terminal"] for row in rows),
        "questions_total": sum(row["questions"] for row in rows),
        "mean_questions": mean(row["questions"] for row in rows),
        "mean_return": mean(row["return"] for row in rows),
        "reasked": sum(len(row["reasked"]) for row in rows),
        "reasons": dict(Counter(row["reason"] for row in rows)),
    }


def evaluate(model_path):
    env = MaskedC02Env("val_internal")
    policies = {"tools_first": ToolsFirst(), "ppo": PPOAFAPolicy(model_path)}
    subsets = [keys for count in range(len(SLOTS) + 1) for keys in combinations(SLOTS, count)]
    cases = [
        {"policy": name, **run_case(env, index, keys, policy)}
        for index in range(len(env.rows)) for keys in subsets for name, policy in policies.items()
    ]
    cohorts = {}
    for name in policies:
        rows = [row for row in cases if row["policy"] == name]
        cohorts[name] = {
            "per_initial_count": {
                str(count): summarize([row for row in rows if len(row["prefilled"]) == count])
                for count in range(len(SLOTS) + 1)
            },
            "partial_context": summarize([row for row in rows if row["prefilled"]]),
            "partial_with_nonanswer": summarize([
                row for row in rows if {"unknown", "declined"}.intersection(row["prefilled"].values())
            ]),
            "initially_sufficient": summarize([row for row in rows if row["initially_sufficient_reference"]]),
        }
    return {
        "entry": "E30", "split": "val_internal", "unique_scenarios": len(env.rows),
        "families": sorted({row["family"] for row in env.rows}), "subsets_per_scenario": len(subsets),
        "base_fixture_fingerprint": fingerprint(env.rows), "new_training_steps": 0,
        "test_internal_evaluated": False, "model": receipt(model_path), "cohorts": cohorts,
        "cases": cases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    model = (ROOT / args.model).resolve()
    report = (ROOT / args.report).resolve()
    if not model.is_relative_to(ROOT / "outputs") or not report.is_relative_to(ROOT / "outputs"):
        parser.error("model and report must be under outputs/")
    if report.exists():
        parser.error("report path must be new")
    data = evaluate(model)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    print(json.dumps(data["cohorts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
