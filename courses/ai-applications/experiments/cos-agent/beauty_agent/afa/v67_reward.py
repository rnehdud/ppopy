"""Exhaustive reward check for the four inactive C02 development fixtures."""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path

from beauty_agent.actions import ActionProposal
from beauty_agent.contracts import ObservationSlot
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from data.action_policy.v67.dataset_cli import read_rows

from .eda import ROOT
from .stage0 import signature
from .v67_fixtures import BUNDLE, SLOTS, ResponseBook, compile_book, require
from .v67_runtime import FixtureSession, audit_runtime, load_response_book


@dataclass(frozen=True)
class RewardProtocol:
    question_cost: int = 1
    incorrect_stop_loss: int = len(SLOTS) + 1

    def __post_init__(self):
        require(type(self.question_cost) is int and self.question_cost > 0,
                "positive integer question cost required")
        require(type(self.incorrect_stop_loss) is int
                and self.incorrect_stop_loss > len(SLOTS) * self.question_cost,
                "incorrect stop must cost more than the entire question budget")


def score_stop(disposition, same_semantics, question_count, protocol):
    require(type(question_count) is int and 0 <= question_count <= len(SLOTS),
            "question count outside bounded task")
    if disposition == "required_hold":
        reason = "required_hold"
    elif disposition == "hold_with_question_available":
        reason = "premature_hold"
    elif disposition == "hold_with_draft_available":
        reason = "missed_draft"
    elif disposition in {"draft_allowed", "hold_without_available_path"}:
        reason = disposition if same_semantics else "reference_mismatch"
    else:
        raise ValueError("unsupported terminal disposition")
    correct = reason in {"draft_allowed", "hold_without_available_path", "required_hold"}
    loss = 0 if correct else protocol.incorrect_stop_loss
    return {"correct_terminal": correct, "reason": reason, "terminal_loss": loss,
            "return": -(question_count * protocol.question_cost + loss)}


def observed_signature(adapter, public):
    observations = {key: ObservationSlot.model_validate(raw)
                    for key, raw in public["observations"].items()}
    return signature(adapter.evaluate(observations, ["B-C02"]))


async def check_branch_priority(protocol, adapter):
    """Exercise the higher-priority tools branch against strong friction."""
    fixture = next(row for row in read_rows(BUNDLE / "fixtures.jsonl")
                   if row["fixture_id"].endswith("849"))
    fixture_id = "e24:branch-priority-check"
    fixture["fixture_id"] = fixture_id
    friction = "method.friction"
    fixture["environment_only"]["response_table"][friction]["value"] = "strong"
    rows, _ = compile_book([fixture])
    book = ResponseBook([fixture], rows)
    public = book.initial_public(fixture_id)
    for slot in SLOTS:
        public = book.answer(fixture_id, public, slot)
    reference = observed_signature(adapter, public)
    paths = {}
    for slot in ("method.tools", friction):
        session = FixtureSession(book, fixture_id)
        await session.apply_action(session.prepare_context(),
                                   ActionProposal(action="ask_user", target_id=slot))
        partial = observed_signature(adapter, session.public)
        _, _, disposition = await session.apply_action(session.prepare_context(),
            ActionProposal(action="request_draft", target_id="label_draft"))
        paths[slot] = {"status": partial["cards"][0]["status"],
                       "actions": partial["cards"][0]["actions"],
                       **score_stop(disposition, partial == reference, 1, protocol)}
    return {"based_on": "849", "authored_override": {friction: "strong"}, "paths": paths}


async def check_rewards(protocol=RewardProtocol()):
    audit = await audit_runtime()
    book, ids, manifest = load_response_book()
    adapter = KBEngineAdapter()
    references = {}
    for fixture_id in ids:
        public = book.initial_public(fixture_id)
        for slot in SLOTS:
            public = book.answer(fixture_id, public, slot)
        references[fixture_id] = observed_signature(adapter, public)

    terminals = []
    by_fixture = defaultdict(list)
    for row in audit["trace"]:
        if row["disposition"] is None:
            continue
        fixture_id, prefix = row["fixture_id"], row["prefix"]
        public = book.initial_public(fixture_id)
        for target in prefix:
            public = book.answer(fixture_id, public, target)
        same = observed_signature(adapter, public) == references[fixture_id]
        scored = {**row, "question_count": len(prefix), "same_semantics": same,
                  **score_stop(row["disposition"], same, len(prefix), protocol)}
        terminals.append(scored)
        by_fixture[fixture_id].append(scored)

    best = {}
    for fixture_id, rows in by_fixture.items():
        valid, invalid = ([row for row in rows if row["correct_terminal"] is correct]
                          for correct in (True, False))
        winner = max(valid, key=lambda row: row["return"], default=None)
        if winner:
            require(not invalid or min(row["return"] for row in valid) >
                    max(row["return"] for row in invalid), "question cost outranks correct stop")
        best[fixture_id] = None if winner is None else {
            "return": winner["return"], "questions": winner["question_count"], "stop": winner["choice"]}
    return {"entry": "E24", "mode": "development_preview", "production_enabled": False,
            "human_review": "unreviewed", "independent_evaluation": False,
            "fixtures": len(ids), "gamma": 1.0, "shaping_beta": 0,
            "protocol": {"question_cost": protocol.question_cost,
                         "incorrect_stop_loss": protocol.incorrect_stop_loss,
                         "max_questions": len(SLOTS)},
            "mechanical_reference": "KB signature with all authored fixture responses, including nonanswers",
            "references": references, "terminal_paths": len(terminals),
            "counts": dict(Counter(row["reason"] for row in terminals)),
            "best_reachable_valid_stop_by_fixture": best, "terminal_trace": terminals,
            "branch_priority_check": await check_branch_priority(protocol, adapter),
            "source_hashes": manifest["source_hashes"], "new_policy_training_runs": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=lambda value: (ROOT / value).resolve(), required=True)
    path = parser.parse_args().report
    require(path.is_relative_to(ROOT / "outputs"), "report must be inside outputs")
    result = asyncio.run(check_rewards())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in
                      ("fixtures", "terminal_paths", "counts", "best_reachable_valid_stop_by_fixture")}))


if __name__ == "__main__":
    main()
