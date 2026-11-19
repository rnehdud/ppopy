"""Two-phase static experiment adapter. Leaves AgentSession and source gates unchanged."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from uuid import uuid4

from beauty_agent.actions import ActionContext, ActionProposal
from beauty_agent.action_runtime import decide_action, dispatch_action, validate_action
from beauty_agent.contracts import ObservationSlot, PlannerMetadata, TurnRequest
from beauty_agent.loop import SessionState
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from .stage0 import require, snapshot, task_offers


@dataclass(frozen=True)
class PreparedTurn:
    token: str
    payload: str

    @property
    def context(self):
        return ActionContext.model_validate(json.loads(self.payload)["context"])

    @property
    def evaluated(self):
        return json.loads(self.payload)["evaluated"]

    @property
    def state(self):
        return SessionState.model_validate(json.loads(self.payload)["staged_state"])


class _SelectedProposal:
    metadata = PlannerMetadata(provider="custom", adapter_revision="afa-static-runtime-v1")

    def __init__(self, proposal):
        self.proposal = proposal

    async def plan_action(self, context):
        return self.proposal.model_copy(deep=True)


class StaticSessionAdapter:
    """State + pending input snapshot, restricted to the Stage 0 known-answer task."""
    def __init__(self, contract, card):
        self.contract = deepcopy(contract)
        require(card in contract["tasks"], "unsupported card")
        self.card = card
        self.request = TurnRequest.model_validate(contract["initial_request"])
        self._state = SessionState(profile=self.request.profile.model_copy(deep=True),
                                   products=[p.model_copy(deep=True) for p in self.request.products])
        self._prepared = None
        self._base_state = None
        self._applying = False
        self.dispatch_count = 0
        self.kb = KBEngineAdapter()

    @property
    def state(self):
        return self._state.model_copy(deep=True)

    def fork(self):
        """Private transaction workspace; only publish after the whole env step succeeds."""
        require(not self._applying, "cannot fork during apply")
        clone = StaticSessionAdapter(self.contract, self.card)
        clone._state = self.state
        clone._prepared = self._prepared
        clone._base_state = self._base_state
        clone.dispatch_count = self.dispatch_count
        return clone

    def prepare_context(self, observations=None):
        require(not self._applying, "cannot prepare during apply")
        staged = self.state
        domains = self.contract["tasks"][self.card]["world_domains"]
        for key, raw in (observations or {}).items():
            slot = ObservationSlot.model_validate(raw)
            require(key in domains and slot.variable_id == key, "observation outside task")
            require(slot.state == "known" and slot.confirmed_by_user and
                    slot.source == "synthetic_fixture" and slot.value in domains[key],
                    "unsupported static response")
            previous = staged.confirmed_observations.get(key)
            require(previous is None or previous == slot, "static response correction is unsupported")
            staged.confirmed_observations[key] = slot.model_copy(deep=True)
        values = {k: v.value for k, v in staged.confirmed_observations.items()}
        context, evaluated = snapshot(self.contract, self.card, values, self.kb)
        context.history = deepcopy(staged.history)
        self._base_state = self._state.model_dump_json()
        self._prepared = PreparedTurn(uuid4().hex, json.dumps({
            "context": context.model_dump(), "evaluated": evaluated,
            "staged_state": staged.model_dump()}, sort_keys=True))
        return self._prepared

    async def apply_action(self, prepared, proposal):
        require(not self._applying, "concurrent apply rejected")
        self._applying = True
        try:
            return await self._apply_selected(prepared, proposal)
        finally:
            self._applying = False

    async def _apply_selected(self, prepared, proposal):
        require(prepared == self._prepared and prepared is not None and
                self._state.model_dump_json() == self._base_state, "stale or consumed snapshot")
        context = prepared.context
        proposal = ActionProposal.model_validate(proposal)
        require((proposal.action, proposal.target_id) in
                {(a.action, a.target_id) for a in task_offers(self.contract, context)},
                "action outside current task capabilities")
        # Invalid proposals are hard errors in the experiment, not silent baseline steps.
        validate_action(proposal, context)
        decision = await decide_action(context, _SelectedProposal(proposal))
        require(decision.applied.action == proposal.action and
                decision.applied.target_id == proposal.target_id and
                not (decision.fallback_reason and decision.fallback_reason != "unverified_question_wording"),
                "unexpected action fallback")
        response, outcome = await dispatch_action(decision, context, self.request)
        staged = prepared.state
        staged.turn_index += 1
        staged.history.append({"action": decision.applied.action, "target_id": decision.applied.target_id,
                               "execution_status": outcome})
        self._state = staged
        self._prepared = None
        self._base_state = None
        self.dispatch_count += 1
        return response, decision, outcome
