"""In-memory, synthetic-only modular agent loop. No storage or approvals."""
from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from typing import Literal

from pydantic import Field, model_validator

from .contracts import (Contract, ObservationSlot, OwnedProduct, PipelineTrace,
                        PipelineTurnResponse, Profile, TurnRequest)
from .modules.jev_adapter import JevExtractorAdapter
from .modules.mapping_adapter import MappingReviewAdapter
from .modules.kb_adapter import KBEngineAdapter
from .actions import build_action_context
from .action_runtime import decide_action, dispatch_action
from poc.jev.relations import SYMPTOMS


class CandidateConfirmation(Contract):
    """Explicit caller-reviewed subject, polarity and observation time, not yes/no NLP."""
    subject: Literal["self", "other", "unknown"]
    state: Literal["affirmed", "denied", "unknown", "declined"]
    observed_at: str | None = None

    @model_validator(mode="after")
    def utc_time(self):
        if self.state in ("unknown", "declined") and self.observed_at is None:
            return self
        if self.observed_at is None or (self.state in ("affirmed", "denied") and self.subject == "unknown"):
            raise ValueError("affirmed/denied confirmation requires subject and time")
        stamp = datetime.fromisoformat(self.observed_at.replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() != timedelta(0):
            raise ValueError("explicit UTC observation time required")
        return self


class SessionState(Contract):
    turn_index: int = 0
    profile: Profile = Field(default_factory=Profile)
    products: list[OwnedProduct] = Field(default_factory=list)
    confirmed_observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    pending_clarifications: dict[str, str] = Field(default_factory=dict)
    confirmed_clarifications: dict[str, CandidateConfirmation] = Field(default_factory=dict)
    history: list[dict] = Field(default_factory=list)


def clarification_candidates(features, message, namespace=None):
    pending = {}
    digest = namespace or hashlib.sha256(message.encode()).hexdigest()[:12]
    for index, item in enumerate(features.get("symptoms", [])):
        key = f"clarify:{digest}:{index}"
        # Extraction labels/clarification text are untrusted, not reviewed wording.
        name = SYMPTOMS.get(item.get("symptom"), "증상")
        pending[key] = f"{name} 언급의 대상이 본인인지, 실제 증상이 있었는지와 관찰 시점을 확인해 주세요."
    for index, text in enumerate(features.get("clarifications", [])):
        key = f"clarify:{digest}:extra:{index}"
        pending[key] = "추출된 관계의 대상·실제 여부·시점을 확인해 주세요."
    if features.get("warnings") and not pending and features.get("extraction_failed"):
        pending[f"clarify:{digest}:failure"] = "추출에 실패했습니다. 본인의 실제 관찰과 시점을 확인해 주세요."
    return pending


async def run_pipeline_turn(request: TurnRequest, *, planner=None,
                            extractor=None, mapping=None, kb=None, observations=None,
                            pending_clarifications=None, confirmed_clarifications=None,
                            card_ids=None, clarification_namespace=None, history=None,
                            planner_timeout=20.0) -> PipelineTurnResponse:
    extractor = extractor or JevExtractorAdapter()
    features = await asyncio.to_thread(extractor.extract, request.message)
    reviewed = (mapping or MappingReviewAdapter()).evaluate(features)
    pending = dict(pending_clarifications or {})
    pending.update(clarification_candidates(features, request.message, clarification_namespace))
    for key in confirmed_clarifications or {}:
        pending.pop(key, None)
    evaluated = (kb or KBEngineAdapter()).evaluate(observations or {}, card_ids)
    trace = PipelineTrace(
        jev_products=[str(p.get("text", "")) for p in features.get("products", [])],
        jev_symptoms=features.get("symptoms", []),
        jev_clarifications=[str(x) for x in features.get("clarifications", [])],
        jev_warnings=features.get("warnings", []),
        mapping_findings=reviewed["findings"], mapping_warnings=reviewed["warnings"],
        kb_evaluated_cards=[r["card_id"] for r in evaluated["raw"]["results"]],
        kb_missing_ask_slots=list(evaluated["ask_slots"]),
        kb_retrieve_slots=evaluated["retrieve_slots"], hold_signals=evaluated["hold_signals"],
        pending_clarifications=pending)
    context = build_action_context(request, features, reviewed, evaluated, pending, observations or {},
        {key: value.model_dump() if isinstance(value, CandidateConfirmation) else value
         for key, value in (confirmed_clarifications or {}).items()}, history)
    decision = await decide_action(context, planner, timeout=planner_timeout)
    response, outcome = await dispatch_action(decision, context, request)
    trace.proposed_action = decision.proposed
    trace.applied_action = decision.applied.model_dump()
    trace.validation_results = decision.validation
    trace.fallback_reason = decision.fallback_reason
    trace.execution_status = outcome
    trace.selected_route = {"hold": "hold_or_escalate", "retrieve_evidence": "retrieve_product",
                            "request_draft": "ready_for_draft"}.get(decision.applied.action, "ask_user")
    return PipelineTurnResponse(**response.model_dump(), trace=trace)


class AgentSession:
    def __init__(self, request: TurnRequest | None = None, *, planner=None, extractor=None,
                 mapping=None, kb=None, card_ids=None):
        self.request = request or TurnRequest(deployment_context="synthetic_test", device="web",
                                             profile=Profile(), products=[])
        self.state = SessionState(profile=self.request.profile.model_copy(deep=True),
                                  products=[p.model_copy(deep=True) for p in self.request.products])
        self.planner, self.extractor, self.mapping, self.kb = planner, extractor, mapping, kb
        self.card_ids = card_ids

    async def step(self, message: str, *, profile: Profile | None = None,
                   products: list[OwnedProduct] | None = None,
                   observations: dict[str, ObservationSlot] | None = None,
                   confirmations: dict[str, CandidateConfirmation] | None = None,
                   resolve_conflicts: tuple[str, ...] = ()) -> PipelineTurnResponse:
        # Stage changes transactionally: invalid input/module failure leaves state intact.
        state = self.state.model_copy(deep=True)
        if profile is not None:
            state.profile = profile.model_copy(deep=True)
        if products is not None:
            state.products = [p.model_copy(deep=True) for p in products]
        request = TurnRequest(**{**self.request.model_dump(), "message": message,
                                 "profile": state.profile, "products": state.products})
        for key, slot in (observations or {}).items():
            slot = ObservationSlot.model_validate(slot)
            if key != slot.variable_id or not slot.confirmed_by_user or key.startswith("product."):
                raise ValueError("only explicitly confirmed user observation slots accepted")
            previous = state.confirmed_observations.get(key)
            if previous and key not in resolve_conflicts:
                if previous.state == "conflicting" or (previous.state == "known" and slot.state == "known"
                        and json.dumps(previous.value, sort_keys=True) != json.dumps(slot.value, sort_keys=True)):
                    slot = slot.model_copy(update={"state": "conflicting", "value": None})
            state.confirmed_observations[key] = slot.model_copy(deep=True)
        for key, confirmation in (confirmations or {}).items():
            if key not in state.pending_clarifications:
                raise ValueError("confirmation must match a pending clarification")
            state.confirmed_clarifications[key] = CandidateConfirmation.model_validate(confirmation)
            state.pending_clarifications.pop(key)
        response = await run_pipeline_turn(
            request, planner=self.planner, extractor=self.extractor, mapping=self.mapping,
            kb=self.kb, observations=state.confirmed_observations,
            pending_clarifications=state.pending_clarifications,
            confirmed_clarifications=state.confirmed_clarifications, card_ids=self.card_ids,
            clarification_namespace=f"turn{state.turn_index + 1}", history=state.history)
        # Confirmations remain separate from KB observations.
        state.pending_clarifications = dict(response.trace.pending_clarifications)
        state.turn_index += 1
        state.history.append({"message": message, "questions": [q.model_dump() for q in response.questions],
                              "trace": response.trace.model_dump()})
        self.state = state
        return response


async def demo(scripted=False):
    from pathlib import Path
    request = TurnRequest.model_validate_json((Path(__file__).resolve().parents[1] / "examples/turn.json").read_text(encoding="utf-8"))
    # Explicit, limited synthetic demo scenario; normal sessions select relevant cards.
    session = AgentSession(request, card_ids=["B-C01"])
    print("합성 입력 전용, 무저장 데모. /quit 종료; /state 상태 확인.")
    print("데모 평가 범위: B-C01. /update {message, profile, products, observations, confirmations} JSON으로 정형 확인.")
    if scripted:
        first = await session.step("어제 밤 폼클렌저 후 볼이 따가워")
        print(first.model_dump_json(indent=2))
        confirmations = {key: CandidateConfirmation(subject="self", state="affirmed",
            observed_at="2026-11-08T12:00:00Z") for key in session.state.pending_clarifications}
        observations = {key: ObservationSlot(variable_id=key, value=value, state="known",
            source="synthetic_fixture", confirmed_by_user=True) for key, value in
            {"method.body_site": "face", "method.water_temperature": "lukewarm"}.items()}
        final = await session.step("합성 관찰을 확인했습니다", confirmations=confirmations, observations=observations)
        print(final.model_dump_json(indent=2))
        return
    while True:
        message = await asyncio.to_thread(input, "> ")
        if message == "/quit":
            return
        if message == "/state":
            print(session.state.model_dump_json(indent=2))
            continue
        if message.startswith("/update "):
            try:
                update = json.loads(message[len("/update "):])
                if "profile" in update:
                    update["profile"] = Profile.model_validate(update["profile"])
                if "products" in update:
                    update["products"] = [OwnedProduct.model_validate(p) for p in update["products"]]
                response = await session.step(**update)
            except (ValueError, TypeError):
                print("정형 확인 입력이 유효하지 않습니다. 상태는 변경되지 않았습니다.")
                continue
        else:
            response = await session.step(message)
        print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--scripted", action="store_true", help="run the fixed two-turn synthetic demo")
    args = parser.parse_args()
    if args.demo:
        asyncio.run(demo(scripted=args.scripted))
