"""Versioned C01+C02 research adapter; original KB, gates and v1 stay unchanged."""
from __future__ import annotations

from copy import deepcopy
import json
from uuid import uuid4

from beauty_agent.actions import ActionOffer, ActionProposal
from beauty_agent.action_runtime import decide_action, dispatch_action, validate_action
from beauty_agent.contracts import PlannerMetadata, TurnRequest
from beauty_agent.loop import SessionState
from .runtime import PreparedTurn, _SelectedProposal
from .semantics import SemanticInspector
from .stage0 import require
from .stage1 import encode

CARDS = ["B-C01", "B-C02"]


class _JointProposal(_SelectedProposal):
    metadata = PlannerMetadata(provider="custom", adapter_revision="afa-joint-runtime-0.1")


def diagnostic(prepared):
    return json.loads(prepared.payload)["semantic"]


class JointSessionAdapter:
    def __init__(self, inspector=None):
        self.inspector = inspector or SemanticInspector()
        self.request = TurnRequest.model_validate(self.inspector.base["initial_request"])
        self._state = SessionState(profile=self.request.profile.model_copy(deep=True),
                                   products=[p.model_copy(deep=True) for p in self.request.products])
        self._ledger = self.inspector.ledger()
        self._prepared = self._base = None
        self._applying = False
        self.dispatch_count = 0

    @property
    def state(self):
        return self._state.model_copy(deep=True)

    def fork(self):
        require(not self._applying, "cannot fork during apply")
        clone = JointSessionAdapter(self.inspector)
        clone._state = self.state
        clone._ledger = self.inspector.ledger(self._ledger.events)
        clone._prepared, clone._base = self._prepared, self._base
        clone.dispatch_count = self.dispatch_count
        return clone

    def prepare_context(self, events=()):
        require(not self._applying, "cannot prepare during apply")
        # Append to pending input, so an unsolicited explicit correction can
        # supersede a staged answer without losing its history before dispatch.
        ledger = self.inspector.ledger(json.loads(self._prepared.payload)["events"] if self._prepared else self._ledger.events)
        for event in events:
            ledger = ledger.append(event)
        semantic = self.inspector.inspect(CARDS, ledger)
        evaluated, original = self.inspector._evaluate(CARDS, ledger.observations)
        context = original.model_copy(deep=True)
        wanted = set(semantic["research_question_requirements"])
        for offer in context.available_actions:
            if offer.action == "ask_user":
                offer.enabled = offer.enabled and offer.target_id in wanted
            elif offer.action == "request_draft":
                offer.enabled = offer.enabled and semantic["draft_permitted_by_contract"]
                if not offer.enabled:
                    offer.blocked_by = sorted(set(offer.blocked_by + ["afa-v2:semantic_or_runtime_blocked"]))
            elif offer.action != "hold":
                offer.enabled = False
        existing = {a.target_id for a in context.available_actions if a.action == "ask_user"}
        for slot in sorted(wanted - existing):
            engine = self.inspector.adapter.engine
            require(slot in self.inspector.domains and not slot.startswith("product.") and
                    engine.variables[slot].get("consumer_question_allowed") is True and
                    slot not in ledger.observations and not semantic["mandatory_holds"], "unsafe question extension")
            require(ledger.observations.get("method.body_site") is not None and
                    ledger.observations["method.body_site"].state == "known", "body site must be confirmed first")
            require(any(slot in engine.cards[card]["observable_inputs"] or
                        any(slot in branch["when"] for branch in engine.rules[card]) for card in CARDS),
                    "question outside selected card predicates")
            text = engine.acquisition.get(slot, {}).get("question_example")
            require(isinstance(text, str) and bool(text.strip()), "source question wording required")
            ref = "afa-v2:question:" + slot
            context.evidence[ref] = {"kind": "experimental_question_extension", "variable_id": slot,
                                     "cards": CARDS, "human_review": "unreviewed"}
            context.kb_ask_slots[slot] = text
            context.available_actions.append(ActionOffer(action="ask_user", target_id=slot, tool="request_user_input",
                reviewed_text=text, evidence_refs=[ref] + ["kb:" + card for card in CARDS],
                conditions=["afa-joint-runtime-0.1 semantic disambiguation; not an original KB question offer"]))
        staged = self.state
        staged.confirmed_observations = ledger.observations
        context.history = deepcopy(staged.history)
        self._base = (self._state.model_dump_json(), encode(self._ledger.events))
        prepared = PreparedTurn(uuid4().hex, encode({"context": context.model_dump(), "evaluated": evaluated,
                                                    "staged_state": staged.model_dump(), "events": ledger.events,
                                                    "semantic": semantic}))
        self._prepared = prepared
        return prepared

    async def apply_action(self, prepared, proposal):
        require(not self._applying, "concurrent apply rejected")
        self._applying = True
        try:
            require(prepared is not None and prepared == self._prepared and
                    self._base == (self._state.model_dump_json(), encode(self._ledger.events)), "stale or consumed snapshot")
            proposal = ActionProposal.model_validate(proposal)
            require(proposal.action in {"ask_user", "hold", "request_draft"}, "unsupported joint action")
            context = prepared.context
            validate_action(proposal, context)
            decision = await decide_action(context, _JointProposal(proposal))
            require((decision.applied.action, decision.applied.target_id) == (proposal.action, proposal.target_id) and
                    decision.fallback_reason in (None, "unverified_question_wording"), "unexpected action fallback")
            response, outcome = await dispatch_action(decision, context, self.request)
            staged = prepared.state
            staged.turn_index += 1
            staged.history.append({"action": decision.applied.action, "target_id": decision.applied.target_id,
                                   "execution_status": outcome})
            ledger = self.inspector.ledger(json.loads(prepared.payload)["events"])
            self._state, self._ledger = staged, ledger
            self.dispatch_count += 1
            self._prepared = self._base = None
            return response, decision, outcome
        finally:
            self._applying = False
