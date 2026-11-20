"""Execute the bounded v67 fixtures through the existing action gate."""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import json
from uuid import uuid4

from beauty_agent.action_runtime import decide_action, dispatch_action, validate_action
from beauty_agent.actions import ActionContext, ActionProposal, build_action_context
from beauty_agent.contracts import ObservationSlot, PlannerMetadata, TurnRequest
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from data.action_policy.v67.dataset_cli import read_rows

from .eda import ROOT, V67, fingerprint
from .stage0 import DEFAULT
from .v67_fixtures import BUNDLE, SLOTS, ResponseBook, require, verify

ACTIONS = tuple(("ask_user", slot) for slot in SLOTS) + (
    ("hold", "insufficient_information"), ("hold", "safety"),
    ("request_draft", "label_draft"),
)
EXPECTED_OUTCOMES = {
    "ask_user": "awaiting_user", "hold": "held", "request_draft": "draft_generated",
}


@dataclass(frozen=True)
class PreparedAction:
    token: str
    payload: str

    @property
    def context(self):
        return ActionContext.model_validate_json(self.payload)

    @property
    def mask(self):
        enabled = {(offer.action, offer.target_id) for offer in self.context.enabled()}
        return tuple(pair in enabled for pair in ACTIONS)


class SelectedAction:
    metadata = PlannerMetadata(provider="custom", adapter_revision="afa-v67-bounded-runtime-0.1")

    def __init__(self, proposal):
        self.proposal = proposal

    async def plan_action(self, context):
        return self.proposal.model_copy(deep=True)


def load_response_book():
    manifest = verify()
    fixtures = read_rows(BUNDLE / "fixtures.jsonl")
    return ResponseBook(fixtures, read_rows(BUNDLE / "responses.jsonl")), [
        fixture["fixture_id"] for fixture in fixtures
    ], manifest


class FixtureSession:
    """In-memory state for one synthetic run. Publish a step after all checks pass."""

    def __init__(self, book, fixture_id):
        self._book, self._fixture_id = book, fixture_id
        self._public = book.initial_public(fixture_id)
        self._request = TurnRequest.model_validate(
            json.loads(DEFAULT.read_text(encoding="utf-8"))["initial_request"]
        ).model_copy(update={"message": self._public["message"]})
        self._kb = KBEngineAdapter()
        self._prepared = None
        self._busy = False
        self._finished = False
        self._dispatch_count = 0

    @property
    def dispatch_count(self):
        return self._dispatch_count

    @property
    def public(self):
        return deepcopy(self._public)

    def _prepare(self, public):
        observations = {key: ObservationSlot.model_validate(value)
                        for key, value in public["observations"].items()}
        evaluated = self._kb.evaluate(observations, ["B-C02"])
        context = build_action_context(
            self._request, {"schema_version": "relations-0.3", "products": [], "symptoms": [],
                            "clarifications": [], "warnings": []},
            {"findings": []}, evaluated, {}, observations, history=deepcopy(public["history"]),
        )
        for offer in context.available_actions:
            if (offer.action, offer.target_id) not in ACTIONS:
                offer.enabled = False
        return PreparedAction(uuid4().hex, context.model_dump_json())

    def prepare_context(self):
        require(not self._busy and not self._finished, "session busy or finished")
        if self._prepared is None:
            self._prepared = self._prepare(self._public)
        return self._prepared

    async def apply_action(self, prepared, proposal):
        require(not self._busy and not self._finished, "session busy or finished")
        require(prepared is not None and prepared is self._prepared, "stale or foreign context")
        self._busy = True
        try:
            proposal = ActionProposal.model_validate(proposal)
            context = prepared.context
            validate_action(proposal, context)
            is_question = proposal.action == "ask_user"
            if is_question:
                public = self._book.answer(self._fixture_id, self._public, proposal.target_id,
                                           focus=proposal.arguments.confirmation_focus)
                following = self._prepare(public)
                disposition = None
            else:
                public, following = self._public, None
                enabled = {offer.action for offer in context.enabled()}
                if proposal.action == "request_draft":
                    disposition = "draft_allowed"
                elif proposal.target_id == "safety":
                    disposition = "required_hold"
                elif "ask_user" in enabled:
                    disposition = "hold_with_question_available"
                elif "request_draft" in enabled:
                    disposition = "hold_with_draft_available"
                else:
                    disposition = "hold_without_available_path"
            decision = await decide_action(context, SelectedAction(proposal))
            require((decision.applied.action, decision.applied.target_id)
                    == (proposal.action, proposal.target_id)
                    and decision.fallback_reason in (None, "unverified_question_wording"),
                    "unexpected fallback")
            response, outcome = await dispatch_action(decision, context, self._request)
            require(outcome == EXPECTED_OUTCOMES[proposal.action], "unexpected dispatch outcome")
            self._public, self._prepared = public, following
            self._finished = not is_question
            self._dispatch_count += 1
            return response, outcome, disposition
        finally:
            self._busy = False


def label_review():
    """Check the two disputed groups using only their identical train inputs."""
    rows = {r["id"]: r for r in read_rows(V67 / "v67-sft-train.jsonl")}
    result = []
    for ask_id, hold_id in (("022", "224"), ("306", "327")):
        ask, hold = [rows[f"luna-v3-train-{i}-t01"] for i in (ask_id, hold_id)]
        require(ask["input"] == hold["input"], "disputed group input drift")
        context = ActionContext.model_validate(ask["input"])
        require(not context.hold_signals and not context.observations.get("method.body_site"),
                "acquisition rubric preconditions changed")
        for row, expected in ((ask, ("ask_user", "method.body_site")),
                              (hold, ("hold", "insufficient_information"))):
            proposal = ActionProposal.model_validate(row["output"])
            require((proposal.action, proposal.target_id) == expected, "disputed action drift")
            validate_action(proposal, context)
        result.append({
            "turn_ids": [ask["id"], hold["id"]], "input_sha256": fingerprint(ask["input"]),
            "source_proposal_sha256": [fingerprint(row["output"]) for row in (ask, hold)],
            "allowed_actions": [["ask_user", "method.body_site"], ["hold", "insufficient_information"]],
            "preference_under_active_acquisition": ["ask_user", "method.body_site"],
            "single_label_disposition": "withhold_group_pending_dataset_purpose",
            "rationale": "The required body site can be asked, and no hold signal or refusal is present.",
            "hold_reason_claims_no_relevant_question": hold_id == "327",
        })
    return result


async def audit_runtime():
    book, fixture_ids, manifest = load_response_book()
    trace = []
    for fixture_id in fixture_ids:
        queue = [()]
        while queue:
            prefix = queue.pop(0)
            session = FixtureSession(book, fixture_id)
            for target in prefix:
                await session.apply_action(session.prepare_context(),
                                           ActionProposal(action="ask_user", target_id=target))
            prepared = session.prepare_context()
            enabled = [pair for pair, allowed in zip(ACTIONS, prepared.mask) if allowed]
            require(enabled and session.dispatch_count == len(prefix), "invalid reachable context")
            for action, target in enabled:
                # Each alternative starts at the same prefix and commits once.
                branch = FixtureSession(book, fixture_id)
                for previous in prefix:
                    await branch.apply_action(branch.prepare_context(),
                                              ActionProposal(action="ask_user", target_id=previous))
                before = branch.public
                _, outcome, disposition = await branch.apply_action(
                    branch.prepare_context(), ActionProposal(action=action, target_id=target))
                require(branch.dispatch_count == len(prefix) + 1, "dispatch count mismatch")
                revealed = None
                if action == "ask_user":
                    added = branch.public["observations"].keys() - before["observations"].keys()
                    require(added == {target}, "observation reveal mismatch")
                    revealed = branch.public["observations"][target]["state"]
                    queue.append((*prefix, target))
                else:
                    require(branch.public == before, "terminal action changed observations")
                trace.append({"fixture_id": fixture_id, "prefix": prefix, "choice": [action, target],
                              "outcome": outcome, "disposition": disposition, "revealed_state": revealed})
    return {"entry": "E23", "fixtures": len(fixture_ids),
            "choices": dict(Counter(row["choice"][0] for row in trace)),
            "revealed_states": dict(Counter(row["revealed_state"] for row in trace if row["revealed_state"])),
            "terminal_dispositions": dict(Counter(row["disposition"] for row in trace if row["disposition"])),
            "runtime_contexts": len(fixture_ids) + sum(row["choice"][0] == "ask_user" for row in trace),
            "source_hashes": manifest["source_hashes"], "label_review": label_review(), "trace": trace}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=lambda value: (ROOT / value).resolve(), required=True)
    report = parser.parse_args().report
    require(report.is_relative_to(ROOT / "outputs"), "report must be inside outputs")
    result = asyncio.run(audit_runtime())
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ("fixtures", "runtime_contexts", "choices",
                                                   "revealed_states", "terminal_dispositions")}))


if __name__ == "__main__":
    main()
