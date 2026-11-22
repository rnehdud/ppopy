"""Paired four-policy software benchmark with a separate synthetic challenge panel."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform
from statistics import median
from time import perf_counter_ns

from beauty_agent.contracts import ObservationSlot
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime import RuleBasedAFAPolicy
from beauty_agent.runtime_contracts import ANSWERED_STATES, MANDATORY_HOLD_SIGNALS

from .myopic_evaluation import (
    ROOT, Case, TracedRoutedPolicy, boundary_cases, branch_cases, replay, structured_case,
    synthetic_observation, v67_cases,
)
from .policy_adapter import PPOAFAPolicy
from .question_priority import MyopicVOIAFAPolicy


POLICY_NAMES = ("current_myopic", "ppo_routed", "old_myopic", "fixed_order")
CHALLENGE = "challenge"


def challenge_cases():
    """Author explicit answer tables. Unspecified answers stay unknown during replay."""
    for tools, friction, drying in product(
        ("hands", "scrub_brush"), ("gentle", "strong"),
        ("pat_gently", "rubbing_strongly", "unknown", "declined"),
    ):
        case = structured_case(
            f"c02-{tools}-{friction}-{drying}", "c02-complete-answers", CHALLENGE, ("B-C02",),
            {"method.tools": tools, "method.friction": friction},
        )
        state = drying if drying in {"unknown", "declined"} else "known"
        case.answers["method.drying"] = synthetic_observation(
            "method.drying", drying if state == "known" else None, state=state,
        )
        yield case, "method.tools"

    panels = (
        ("cleansing-load", ("B-C05",), ("cleansing.target_load", "cleansing.repeat_wash"), (
            ("confirmed_removal_need", "habitual_without_reason"),
            ("no_additional_removal_need", "purpose_matched"),
            ("heavy_sweat", "purpose_matched"),
            ("makeup_requires_removal", "habitual_without_reason"),
        )),
        ("moisture-timing", ("B-M01",), ("method.current_routine", "moisturizing.after_wash_delay", "method.skin_wetness"), (
            ("moisturizing_needed", "until_completely_dry", "slightly_damp"),
            ("moisturizing_function_used", "until_completely_dry", "slightly_damp"),
            ("moisturizing_not_needed_no_discomfort", "prompt_while_slightly_damp", "slightly_damp"),
        )),
        ("moisture-dryness", ("B-M02",), ("moisturizing.comfort", "skin.dryness", "dose.proxy_amount"), (
            ("comfortable", "persistent", "reduced_all_products"),
            ("persistent_pain", "persistent", "reduced_all_products"),
            ("persistent_stinging", "none", "reduced_all_products"),
        )),
        ("sunscreen-label-evidence", ("B-P01",), ("sun.outdoor_time", "sun.water_contact", "sun.sweat"), (
            ("prolonged", "no", "yes"), ("prolonged", "yes", "no"), ("none", "no", "no"),
        )),
        ("coverage-and-dose", ("B-P02",), ("sun.coverage_gaps", "dose.proxy_amount", "sun.outdoor_time"), (
            ("none", "according_to_label", "prolonged"),
            ("none", "deliberately_minimal", "prolonged"),
            ("intentional_exposed_gaps", "deliberately_minimal", "prolonged"),
        )),
        ("reapplication-exposure", ("B-P03",), (
            "sun.outdoor_time", "sun.reapplication", "sun.sweat", "sun.water_contact", "sun.window_context",
        ), (
            ("none", "none", "none", "none", "none_reported"),
            ("none", "none", "yes", "none", "none_reported"),
            ("prolonged", "matched_to_exposure_and_label", "yes", "yes", "none_reported"),
            ("prolonged", "none", "yes", "yes", "none_reported"),
        )),
        ("sunscreen-removal", ("B-I01",), ("cleansing.steps", "dose.proxy_amount", "sun.outdoor_time"), (
            ("according_to_product_removal_instructions", "according_to_label", "prolonged"),
            ("according_to_product_removal_instructions", "deliberately_minimal", "prolonged"),
            ("repeated_only_because_water_resistant", "according_to_label", "prolonged"),
        )),
        ("timing-and-causality", ("B-I03",), ("skin.post_use_timing", "routine.change_log", "moisturizing.comfort"), (
            ("immediate_and_delayed_distinguished", "reviewed_against_onset", "sensory_feel_interpreted_as_absorption"),
            ("cause_assumed_without_timing", "reviewed_against_onset", "sensory_feel_interpreted_as_absorption"),
        )),
        ("aha-missing-evidence", ("B-I04",), ("method.current_routine",), (
            ("needed_moisturizing_and_protection_maintained",), ("core_stopped_due_to_combination",),
        )),
        ("layering-with-cleansing", ("B-C01", "B-I02"), ("sun.pilling", "sun.reapplication", "method.water_temperature"), (
            ("present", "reduced_due_to_layering", "hot"),
            ("none", "matched_to_exposure_and_label", "lukewarm"),
            ("present", "matched_to_exposure_and_label", "lukewarm"),
        )),
        ("layering-with-moisture", ("B-M01", "B-I02"), ("sun.pilling", "sun.reapplication", "method.current_routine"), (
            ("present", "reduced_due_to_layering", "moisturizing_not_needed_no_discomfort"),
            ("none", "matched_to_exposure_and_label", "moisturizing_not_needed_no_discomfort"),
        )),
        ("safety-with-reapplication", ("B-M02", "B-P03"), ("moisturizing.comfort", "sun.reapplication", "sun.outdoor_time"), (
            ("persistent_pain", "matched_to_exposure_and_label", "prolonged"),
            ("persistent_stinging", "none", "prolonged"),
        )),
        ("compound-sunscreen", ("B-P02", "B-I01"), (
            "sun.coverage_gaps", "dose.proxy_amount", "sun.outdoor_time", "cleansing.steps",
        ), (
            ("none", "according_to_label", "prolonged", "according_to_product_removal_instructions"),
            ("intentional_exposed_gaps", "deliberately_minimal", "prolonged", "repeated_only_because_water_resistant"),
        )),
    )
    for family, cards, fields, values in panels:
        for number, row in enumerate(values, 1):
            case = structured_case(
                f"{family}-{number}", family, CHALLENGE, cards, dict(zip(fields, row, strict=True)),
            )
            yield case, fields[0]


def _world_key(case):
    # Card order matters to the runtime, but a reordering does not make a new world.
    values = {field: (obs.state, obs.value) for field, obs in (case.initial | case.answers).items()}
    return json.dumps([sorted(case.cards), values], sort_keys=True)


def frozen_cases(adapter):
    historical = [*branch_cases(adapter), *boundary_cases(), *v67_cases()]
    seen = {_world_key(case) for case in historical}
    new = []
    for case, reveal in challenge_cases():
        world = _world_key(case)
        if world in seen:
            continue
        seen.add(world)
        new.append(replace(case, id=f"{case.id}:cold"))
        new.append(replace(case, id=f"{case.id}:prefill",
                           initial={**case.initial, reveal: case.answers[reveal]},
                           answers={key: obs for key, obs in case.answers.items() if key != reveal}))
    cases = historical + new
    if len({case.id for case in cases}) != len(cases):
        raise ValueError("duplicate case ID")
    return cases


def _case_record(case):
    return {
        "id": case.id, "family": case.family, "cohort": case.cohort, "cards": list(case.cards),
        "initial": {key: obs.model_dump(mode="json") for key, obs in case.initial.items()},
        "answers": {key: obs.model_dump(mode="json") for key, obs in case.answers.items()},
        "lineage": case.lineage,
    }


def _load_case(row):
    return Case(
        row["id"], row["family"], row["cohort"], tuple(row["cards"]),
        {key: ObservationSlot.model_validate(obs) for key, obs in row["initial"].items()},
        {key: ObservationSlot.model_validate(obs) for key, obs in row["answers"].items()}, row["lineage"],
    )


def _visible_effect(response):
    bundle = response.recommendation.model_dump(mode="json") if response.recommendation else None
    if bundle:
        for field, value in bundle.items():
            if isinstance(value, list):
                bundle[field] = sorted(value, key=lambda entry: json.dumps(entry, sort_keys=True))
    return {
        "status": response.status, "hold_reason": response.hold_reason,
        "required_product_evidence": sorted(response.required_product_evidence), "recommendation": bundle,
    }


def measured_replay(case, adapter, policy, *, full=False):
    times, responses = [], []

    def observe(runtime, request):
        start = perf_counter_ns()
        response = runtime.handle_turn(request)
        times.append((perf_counter_ns() - start) / 1_000_000)
        responses.append(response)
        return response

    try:
        result = replay(case, adapter, policy, full=full, observe_turn=observe)
    except ValueError as error:
        # Keep the invalid rollout in its cohort denominator and count any ASK it issued.
        return {"error": str(error), "effect": None, "visible_effect": None, "fallback_steps": None,
                "questions": [res.questions[0].id for res in responses if res.pending_action == "ask_user"],
                "turn_ms": times}
    return {**result, "error": None, "visible_effect": _visible_effect(responses[-1]), "turn_ms": times}


def _latency(samples):
    if not samples:
        return None
    ordered = sorted(samples)
    return {"p50_ms": median(ordered), "p95_ms": ordered[(95 * len(ordered) - 1) // 100]}


def summarize_panel(rows):
    count = len(rows)
    if not count:
        return None
    summary = {
        "conditions": count,
        "worlds": len({_world_key(_load_case(row["case"])) for row in rows}),
        "families": len({(row["case"]["cohort"], row["case"]["family"]) for row in rows}),
        "reference_errors": sum(row["reference"]["error"] is not None for row in rows),
    }
    for policy in POLICY_NAMES:
        results = [row[policy] for row in rows]
        product_ask = reask = 0
        for row in rows:
            seen = {slot for slot, answer in row["case"]["initial"].items() if answer["state"] in ANSWERED_STATES}
            for slot in row[policy]["questions"]:
                product_ask += slot.startswith("product.")
                reask += slot in seen
                seen.add(slot)
        summary[policy] = {
            "questions": sum(len(r["questions"]) for r in results),
            "mean_questions": sum(len(r["questions"]) for r in results) / count,
            "exact_matches": sum(r["exact_match"] for r in results),
            "visible_matches": sum(r["visible_match"] for r in results),
            "decision_fidelity": sum(r["exact_match"] for r in results) / count,
            "product_ask": product_ask,
            "reask": reask,
            "completed": sum((r["effect"] or {}).get("status") == "completed" for r in results),
            "held_when_reference_completed": sum(
                (row[policy]["effect"] or {}).get("status") == "held"
                and (row["reference"]["effect"] or {}).get("status") == "completed" for row in rows
            ),
            "mandatory_hold_references": sum(row["reference_mandatory_hold"] for row in rows),
            "mandatory_holds_returned": sum(r["returned_mandatory_hold"] for r in results),
            "hold_miss": sum(row["reference_mandatory_hold"] and not row[policy]["returned_mandatory_hold"]
                             for row in rows),
            "completed_despite_mandatory_hold_reference": sum(r["unsafe_completion"] for r in results),
            "errors": sum(r["error"] is not None for r in results),
            "fallback_steps": (sum(r["fallback_steps"] for r in results)
                               if all(r["fallback_steps"] is not None for r in results) else None),
            "turn_latency": _latency([ms for r in results for ms in r["turn_ms"]]),
            "case_latency": _latency([sum(r["turn_ms"]) for r in results]),
        }
    summary["exact_pairwise_agreements"] = {
        f"{a}_vs_{b}": sum(row[a]["effect"] is not None and row[a]["effect"] == row[b]["effect"] for row in rows)
        for a, b in combinations(POLICY_NAMES, 2)
    }
    ppo_rows = [row["ppo_routed"] for row in rows]
    summary["ppo_attribution"] = {
        "question_sources": dict(Counter(source for r in ppo_rows for source in r.get("question_sources", ()))),
        "terminal_sources": dict(Counter(r.get("stop_source", "error") for r in ppo_rows)),
        "conditions_with_model_questions": sum("ppo_model" in r.get("question_sources", ()) for r in ppo_rows),
    }
    return summary


def evaluate_panel(adapter, cases, ppo):
    baseline = RuleBasedAFAPolicy()
    policies = {
        "current_myopic": MyopicVOIAFAPolicy(),
        "ppo_routed": TracedRoutedPolicy(ppo, baseline=baseline),
        "old_myopic": MyopicVOIAFAPolicy(stop_lookahead=1),
        "fixed_order": baseline,
    }
    warmup = next((case for case in cases if case.cards == ("B-C02",)), cases[0])
    for policy in policies.values():
        measured_replay(warmup, adapter, policy)
    rows = []
    for index, case in enumerate(cases):
        reference = measured_replay(case, adapter, baseline, full=True)
        names = POLICY_NAMES[index % 4:] + POLICY_NAMES[:index % 4]
        results = {name: measured_replay(case, adapter, policies[name]) for name in names}
        mandatory = bool(MANDATORY_HOLD_SIGNALS.intersection((reference["effect"] or {}).get("hold_signals", ())))
        for result in results.values():
            effect = result["effect"] or {}
            result["exact_match"] = bool(effect) and effect == reference["effect"]
            result["visible_match"] = result["visible_effect"] is not None and result["visible_effect"] == reference["visible_effect"]
            result["returned_mandatory_hold"] = mandatory and effect.get("status") == "held" and bool(
                MANDATORY_HOLD_SIGNALS.intersection(effect.get("hold_signals", ()))
            )
            result["unsafe_completion"] = mandatory and effect.get("status") == "completed"
        rows.append({"case": _case_record(case), "reference": reference, "reference_mandatory_hold": mandatory,
                     **{name: results[name] for name in POLICY_NAMES}})
    history = [row for row in rows if row["case"]["cohort"] != CHALLENGE]
    challenge = [row for row in rows if row["case"]["cohort"] == CHALLENGE]
    return {
        "overall": summarize_panel(rows),
        "historical": summarize_panel(history),
        "challenge": summarize_panel(challenge),
        "by_challenge_family": {
            family: summarize_panel([row for row in challenge if row["case"]["family"] == family])
            for family in dict.fromkeys(row["case"]["family"] for row in challenge)
        },
        "ppo_model_question_conditions": summarize_panel([
            row for row in rows if "ppo_model" in row["ppo_routed"].get("question_sources", ())
        ]),
        "b_c02_only": summarize_panel([row for row in rows if row["case"]["cards"] == ["B-C02"]]),
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--ppo-model", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    adapter = KBEngineAdapter()
    if args.freeze:
        cases = frozen_cases(adapter)
        args.fixtures.parent.mkdir(parents=True, exist_ok=True)
        with args.fixtures.open("x", encoding="utf-8", newline="\n") as file:
            json.dump([_case_record(case) for case in cases], file, ensure_ascii=False, indent=2)
            file.write("\n")
        print(f"Frozen {len(cases)} conditions.")
        return
    if args.ppo_model is None or args.output is None:
        parser.error("--ppo-model and --output are required for evaluation")
    data = args.fixtures.read_bytes()
    cases = [_load_case(row) for row in json.loads(data)]
    if [_case_record(case) for case in frozen_cases(adapter)] != [_case_record(case) for case in cases]:
        raise ValueError("frozen fixtures differ from the current declared panel")
    model_hash = sha256(args.ppo_model.read_bytes()).hexdigest()
    now = evaluate_panel(adapter, cases, PPOAFAPolicy(args.ppo_model))
    sources = [Path(__file__), *[Path(__file__).with_name(name) for name in
               ("myopic_evaluation.py", "question_priority.py", "policy_adapter.py")],
               Path(__file__).parents[1] / "runtime.py", Path(__file__).parents[1] / "modules/kb_adapter.py",
               ROOT / "skin_engine/kb_preview/rules.json", ROOT / "skin_engine/kb_preview/engine.py"]
    report = {
        "mode": "development_preview", "production_enabled": False, "independent_evaluation": False,
        "method": "scripted structured answers, fixed cards, deterministic CPU PPO and rotated execution order",
        "reference": "same runtime with all scripted answers initially provided",
        "latency_scope": "local AgentRuntime.handle_turn wall time; excludes model load and scripted response lookup",
        "python": platform.python_version(), "platform": platform.platform(),
        "kb_sha256": adapter.engine.sha, "fixtures_sha256": sha256(data).hexdigest(),
        "checkpoint_sha256": model_hash,
        "source_sha256": {path.relative_to(ROOT).as_posix(): sha256(path.read_bytes()).hexdigest() for path in sources},
        **now,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(json.dumps({key: report[key] for key in ("overall", "historical", "challenge")}, indent=2))


if __name__ == "__main__":
    main()
