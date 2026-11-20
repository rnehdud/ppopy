"""Replay authored compound cases through the same runtime with and without question ranking."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from beauty_agent.contracts import ObservationSlot
from beauty_agent.runtime import AgentRuntime, RuleBasedAFAPolicy
from beauty_agent.runtime_contracts import RuntimeTurnRequest


PROJECT = Path(__file__).resolve().parents[2]
ROOT = PROJECT.parents[3]
DATA = PROJECT / "data/afa/compound-v1"
GATE = {"min_question_savings": 1, "new_outcome_errors": 0, "reasked": 0,
        "require_all_ranked_outcomes_correct": True}


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _slot(field, value):
    state = value if value in ("declined", "unknown") else "known"
    return ObservationSlot(variable_id=field, state=state,
                           value=value if state == "known" else None,
                           source="synthetic_fixture", confirmed_by_user=True)


def _case_answers(defaults, case):
    return defaults | case["answers"]


def _effect(response):
    bundle = response.recommendation.model_dump(mode="json") if response.recommendation else None
    if bundle:
        for key, values in bundle.items():
            if isinstance(values, list):
                bundle[key] = sorted(values, key=lambda value: json.dumps(value, sort_keys=True))
    return {"status": response.status, "recommendation": bundle,
            "required_product_evidence": sorted(response.required_product_evidence),
            "hold_reason": response.hold_reason}


def _replay(case, answers, *, ranked, full=False):
    runtime = AgentRuntime(afa_policy=RuleBasedAFAPolicy(), prioritize_question_outcomes=ranked)
    initial = set(answers if full else case["prefilled"])
    request_id = case["id"]
    response = runtime.handle_turn(RuntimeTurnRequest(
        request_id=request_id, message=case["message"],
        observations={field: _slot(field, answers[field]) for field in sorted(initial)},
    ))
    asked = []
    while response.status == "awaiting_user":
        if full or len(response.questions) != 1:
            raise ValueError(f"{request_id}: full reference or turn contract unresolved")
        field = response.questions[0].id
        if field not in answers or field in initial or field in asked:
            raise ValueError(f"{request_id}: unsupported or repeated question {field}")
        asked.append(field)
        response = runtime.handle_turn(RuntimeTurnRequest(
            request_id=request_id, observations={field: _slot(field, answers[field])},
        ))
    return {"effect": _effect(response), "questions": asked,
            "cards": runtime.get_session(request_id).active_cards}


def evaluate(bundle):
    rows = []
    for case in bundle["cases"]:
        answers = _case_answers(bundle["default_answers"], case)
        reference = _replay(case, answers, ranked=False, full=True)
        if reference["effect"]["status"] != case["expected_status"]:
            raise ValueError(f"{case['id']}: authored status and full-input reference differ")
        if not set(case["required_cards"]) <= set(reference["cards"]):
            raise ValueError(f"{case['id']}: authored card scope and full-input route differ")
        row = {"id": case["id"], "family": case["family"], "reference": reference}
        for name, ranked in (("baseline", False), ("ranked", True)):
            trial = _replay(case, answers, ranked=ranked)
            row[name] = {**trial, "matches_reference": trial["effect"] == reference["effect"]
                         and set(case["required_cards"]) <= set(trial["cards"])}
        rows.append(row)
    summaries = {
        name: {
            "correct": sum(row[name]["matches_reference"] for row in rows),
            "questions": sum(len(row[name]["questions"]) for row in rows),
            "status_counts": dict(Counter(row[name]["effect"]["status"] for row in rows)),
        } for name in ("baseline", "ranked")
    }
    savings = summaries["baseline"]["questions"] - summaries["ranked"]["questions"]
    new_errors = sum(row["baseline"]["matches_reference"] and not row["ranked"]["matches_reference"]
                     for row in rows)
    return {"cases": len(rows), "families": len({row["family"] for row in rows}),
            "summary": summaries, "questions_saved": savings, "new_outcome_errors": new_errors,
            "reasked": 0, "adopt": savings >= GATE["min_question_savings"]
            and new_errors <= GATE["new_outcome_errors"]
            and summaries["ranked"]["correct"] == len(rows), "rows": rows}


def _no_overlap(development, heldout):
    def worlds(bundle):
        return {json.dumps(_case_answers(bundle["default_answers"], case), sort_keys=True)
                for case in bundle["cases"]}

    def keys(bundle, field):
        values = {case[field] for case in bundle["cases"]}
        if field == "id" and len(values) != len(bundle["cases"]):
            raise ValueError("duplicate case ID")
        return values

    if (keys(development, "id") & keys(heldout, "id") or
            keys(development, "family") & keys(heldout, "family") or worlds(development) & worlds(heldout)):
        raise ValueError("development and held-out IDs, families, and complete observations must be disjoint")


def _freeze():
    paths = [Path(__file__), PROJECT / "beauty_agent/afa/question_priority.py",
             PROJECT / "beauty_agent/runtime.py", PROJECT / "beauty_agent/runtime_contracts.py",
             PROJECT / "beauty_agent/nlp_layer.py", PROJECT / "beauty_agent/modules/kb_adapter.py",
             ROOT / "skin_engine/kb_preview/rules.json", ROOT / "docs/source-manifest.json",
             DATA / "development.json"]
    return {"sources": {path.relative_to(ROOT).as_posix(): _digest(path) for path in paths}, "gate": GATE}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("development", "freeze", "heldout"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--lock", type=Path)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to(ROOT / "outputs") or output.exists():
        parser.error("use a new output path under outputs/")
    if args.phase == "freeze":
        result = _freeze()
    else:
        development = _read(DATA / "development.json")
        cases = development
        if args.phase == "heldout":
            if args.lock is None or _read(ROOT / args.lock) != _freeze():
                parser.error("runtime, ranking, data, or gate differ from frozen configuration")
            cases = _read(DATA / "heldout.json")
            _no_overlap(development, cases)
        result = {"phase": args.phase, "human_review": "unreviewed", **evaluate(cases)}
        if args.phase == "heldout":
            result["freeze_sha256"] = _digest(ROOT / args.lock)
            result["heldout_sha256"] = _digest(DATA / "heldout.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: val for key, val in result.items() if key not in ("rows", "sources")}))


if __name__ == "__main__":
    main()
