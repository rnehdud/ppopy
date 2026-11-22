"""Pure-Python Agent Runtime orchestrating NLP, tools, KB, AFA-Policy, and recommendations."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Callable

from .afa.question_priority import (
    MyopicVOIAFAPolicy,
    branch_values,
    rank_questions,
    required_product_evidence,
    select_hold_review_question,
)
from .catalog_adapter import (
    AuroraCatalogAdapter,
    CatalogAdapter,
    DEFAULT_SYNTHETIC_CATALOG,
    SyntheticCatalogAdapter,
)
from .contracts import ObservationSlot, OwnedProduct, Profile
from .followup_choices import observation_choices, symptom_choices
from .modules.kb_adapter import KBEngineAdapter
from .nlp_layer import NLPLayer
from .product_evidence import lookup_product_evidence
from .runtime_contracts import (
    ANSWERED_STATES,
    MANDATORY_HOLD_SIGNALS,
    AFAHandoffResult,
    AFAPolicy,
    AFAStepDecision,
    ExclusionItem,
    NLPExtractionResult,
    QuestionCandidate,
    RecommendationBundle,
    RecommendationItem,
    RuntimeActionKind,
    RuntimeQuestion,
    RuntimeSessionState,
    RuntimeTurnRequest,
    RuntimeTurnResponse,
    ToolLookupResult,
)
from .v3_contracts import AFAStepDecision as V3AFAStepDecision

C02_QUESTION_ORDER = ("method.tools", "method.friction", "method.drying")
TOPIC_TO_CARDS: dict[str, tuple[str, ...]] = {
    "outdoor_sun": ("B-P01",),
    "cleansing_method": ("B-C01", "B-C02"),
    "repeat_cleansing": ("B-C05",),
    "discomfort_report": ("B-B01",),
}
OBSERVATION_TO_CARD = {
    "method.water_temperature": "B-C01",
    **dict.fromkeys(C02_QUESTION_ORDER, "B-C02"),
    "cleansing.target_load": "B-C05",
    "cleansing.repeat_wash": "B-C05",
    "skin.current_discomfort": "B-B01",
    "person.clinician_plan": "B-B01",
    "skin.pain": "B-H01",
}

DEFAULT_SYNTHETIC_CATALOG: dict[str, dict] = {
    "synthetic-cleanser-a": {
        "name": "합성 순한 폼클렌저 A",
        "version": "1.0.0",
        "category": "cleanser",
        "label_guidance": "미온수로 거품을 내어 손으로 부드럽게 세안한 뒤 헹굽니다.",
        "evidence_ref": "catalog:synthetic-cleanser-a@1.0.0",
    },
    "synthetic-moisturizer-a": {
        "name": "합성 장벽 보습 크림 A",
        "version": "1.0.0",
        "category": "moisturizer",
        "label_guidance": "세안 직후 적당량을 피부에 부드럽게 펴 바릅니다.",
        "evidence_ref": "catalog:synthetic-moisturizer-a@1.0.0",
    },
}

DEFAULT_SYNTHETIC_ALTERNATIVES: list[dict] = [
    {
        "product_id": "synthetic-sunscreen-alt-1",
        "title": "합성 대체 자외선 차단제 후보 1",
        "guidance": "라벨에 SPF 30 이상 및 광범위 차단(UVA) 표기가 확인된 합성 후보입니다. 사용 전 성분·민감도 확인이 필요합니다.",
        "evidence_ref": "alternative:synthetic-sunscreen-alt-1",
    }
]


class RuleBasedAFAPolicy:
    """Deterministic baseline implementing the AFAPolicy protocol."""

    def decide_step(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        can_stop_sufficient: bool,
        can_stop_insufficient: bool = True,
    ) -> AFAStepDecision:
        if available_features:
            target = available_features[0].slot_id
            if available_features[0].card_ids == ["B-C02"]:
                ids = {
                    candidate.slot_id
                    for candidate in available_features
                    if candidate.card_ids == ["B-C02"]
                }
                target = next((key for key in C02_QUESTION_ORDER if key in ids), target)
            return AFAStepDecision(
                action="acquire",
                target_feature=target,
                policy_source="rule_baseline",
            )
        if can_stop_sufficient:
            return AFAStepDecision(
                action="stop",
                stop_reason="sufficient",
                policy_source="rule_baseline",
            )
        if can_stop_insufficient:
            return AFAStepDecision(
                action="stop",
                stop_reason="insufficient",
                policy_source="rule_baseline",
            )
        raise ValueError("no available features or permitted stop")


class RoutedAFAPolicy:
    """Routes B-C02-only steps to an injected PPOAFAPolicy and falls back to baseline otherwise."""

    def __init__(self, ppo_policy: AFAPolicy | None = None, baseline: AFAPolicy | None = None):
        self.ppo_policy = ppo_policy
        self.baseline = baseline or RuleBasedAFAPolicy()

    def decide_step(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        can_stop_sufficient: bool,
        can_stop_insufficient: bool = True,
    ) -> AFAStepDecision:
        if self.ppo_policy is not None:
            try:
                return self.ppo_policy.decide_step(
                    observations,
                    available_features,
                    can_stop_sufficient=can_stop_sufficient,
                    can_stop_insufficient=can_stop_insufficient,
                )
            except (ValueError, KeyError, TypeError):
                pass
        return self.baseline.decide_step(
            observations,
            available_features,
            can_stop_sufficient=can_stop_sufficient,
            can_stop_insufficient=can_stop_insufficient,
        )


def default_weather_lookup(query_key: str) -> ToolLookupResult:
    return ToolLookupResult(
        tool_name="weather",
        query_key=query_key,
        status="found",
        source="synthetic_weather_fixture",
        observed_at=datetime.now(timezone.utc).isoformat(),
        data={"uv_index_level": "high", "summary": "합성 맑음 · 야외 자외선 노출 주의"},
    )


def default_product_lookup(product: OwnedProduct) -> ToolLookupResult:
    return SyntheticCatalogAdapter().lookup_by_id(product)


def default_alternative_lookup(query_key: str) -> ToolLookupResult:
    # The offline fixture only covers the demo's missing sunscreen.
    candidates = DEFAULT_SYNTHETIC_ALTERNATIVES if query_key == "synthetic-sunscreen-b" else []
    return ToolLookupResult(
        tool_name="alternative_search",
        query_key=query_key,
        status="found" if candidates else "not_found",
        source="synthetic_alternative_catalog",
        data={"candidates": deepcopy(candidates)},
    )


class AgentRuntime:
    """Stateful, pure-Python runtime supporting pause/resume across CLI and future iOS APIs."""

    def __init__(
        self,
        *,
        nlp_layer: NLPLayer | None = None,
        kb_adapter: KBEngineAdapter | None = None,
        afa_policy: AFAPolicy | None = None,
        weather_lookup: Callable[[str], ToolLookupResult] = default_weather_lookup,
        product_lookup: Callable[[OwnedProduct], ToolLookupResult] | None = None,
        alternative_lookup: Callable[[str], ToolLookupResult] = default_alternative_lookup,
        catalog_adapter: CatalogAdapter | None = None,
        auto_apply_nlp_features: bool = False,
        prioritize_question_outcomes: bool = True,
    ):
        self.nlp_layer = nlp_layer or NLPLayer(use_remote_jev=False)
        self.kb_adapter = kb_adapter or KBEngineAdapter()
        self.afa_policy = afa_policy if afa_policy is not None else RoutedAFAPolicy()
        self.catalog_adapter = catalog_adapter or SyntheticCatalogAdapter()
        self.weather_lookup = weather_lookup
        self.product_lookup = product_lookup or self.catalog_adapter.lookup_by_id
        self.alternative_lookup = alternative_lookup
        self.auto_apply_nlp_features = auto_apply_nlp_features
        self.prioritize_question_outcomes = prioritize_question_outcomes
        self._sessions: dict[str, RuntimeSessionState] = {}

    def get_session(self, request_id: str) -> RuntimeSessionState | None:
        state = self._sessions.get(request_id)
        return state.model_copy(deep=True) if state is not None else None

    def _select_cards(
        self,
        state: RuntimeSessionState,
        topic_hints: list[str],
        observations: dict[str, ObservationSlot],
    ) -> list[str]:
        reasons = {cid: list(state.card_selection_reasons.get(cid, ["session"]))
                   for cid in state.active_cards}
        for topic in topic_hints:
            for cid in TOPIC_TO_CARDS.get(topic, ()):
                reasons.setdefault(cid, []).append(f"topic:{topic}")
        for field, cid in OBSERVATION_TO_CARD.items():
            if field in observations:
                reasons.setdefault(cid, []).append(f"observation:{field}")
        if not reasons:
            non_gate_obs = observations.keys() - {"method.body_site"}
            for cid, card in self.kb_adapter.engine.cards.items():
                if cid == "B-P07":
                    continue
                card_fields = (set(card["observable_inputs"]) | {
                    field for branch in self.kb_adapter.engine.rules[cid] for field in branch["when"]
                }) - {"method.body_site"}
                if card_fields & non_gate_obs:
                    reasons[cid] = [f"observation:{field}" for field in sorted(card_fields & non_gate_obs)]
        if not reasons:
            reasons = {"B-C01": ["default"], "B-C02": ["default"]}
        state.active_cards = list(reasons)
        state.card_selection_reasons = {cid: list(dict.fromkeys(items)) for cid, items in reasons.items()}
        return state.active_cards

    def _merge_observations(
        self,
        state: RuntimeSessionState,
        incoming: dict[str, ObservationSlot],
        resolve_conflicts: tuple[str, ...],
    ) -> None:
        for key, slot in incoming.items():
            validated = ObservationSlot.model_validate(slot)
            if key != validated.variable_id or not validated.confirmed_by_user or key.startswith("product."):
                raise ValueError(f"invalid user observation slot: {key}")
            prev = state.confirmed_observations.get(key)
            if prev and key not in resolve_conflicts and key not in state.unrecognized_fields:
                if prev.state == "conflicting" or (
                    prev.state == "known" and validated.state == "known" and prev.value != validated.value
                ):
                    validated = validated.model_copy(update={"state": "conflicting", "value": None})
            state.confirmed_observations[key] = validated.model_copy(deep=True)
            if key in state.unrecognized_fields:
                state.unrecognized_fields.remove(key)

    def _apply_confirmations(self, state: RuntimeSessionState, confirmations: dict) -> None:
        if not confirmations:
            return
        pending_by_id = {c.candidate_id: c for c in state.pending_candidates}
        for cid, raw_conf in confirmations.items():
            cand = pending_by_id.get(cid)
            if cand is None and cid not in state.confirmed_candidates:
                raise ValueError(f"unknown candidate_id: {cid}")
            state.confirmed_candidates[cid] = raw_conf.model_copy(deep=True)
            state.pending_candidates = [c for c in state.pending_candidates if c.candidate_id != cid]
            if (
                cand is not None
                and raw_conf.subject == "self"
                and raw_conf.state == "affirmed"
                and raw_conf.persistence in ("persistent", "repeated")
            ):
                state.confirmed_observations["skin.current_discomfort"] = ObservationSlot(
                    variable_id="skin.current_discomfort",
                    state="known",
                    value=raw_conf.persistence,
                    source="user_report",
                    confirmed_by_user=True,
                )
                if cand.symptom == "dryness" and raw_conf.persistence == "persistent":
                    state.confirmed_observations["skin.dryness"] = ObservationSlot(
                        variable_id="skin.dryness",
                        state="known",
                        value="persistent",
                        source="user_report",
                        confirmed_by_user=True,
                    )
                if "B-B01" not in state.active_cards:
                    state.active_cards.append("B-B01")
        # If discomfort_report added B-B01 solely for unconfirmed candidates and none
        # turned out to be persistent/repeated self symptoms, drop B-B01 so routine
        # questions can proceed without unrelated clinician_plan prompts.
        if (
            not state.pending_candidates
            and "skin.current_discomfort" not in state.confirmed_observations
            and "B-B01" in state.active_cards
        ):
            state.active_cards = [c for c in state.active_cards if c != "B-B01"]

    def _run_tools(
        self,
        state: RuntimeSessionState,
        nlp_result: NLPExtractionResult | None,
        executed_actions: list[RuntimeActionKind],
    ) -> None:
        hints = set(nlp_result.topic_hints) if nlp_result else set()
        if "outdoor_sun" in hints and "weather:current" not in state.tool_results:
            executed_actions.append("lookup_weather")
            state.tool_results["weather:current"] = self.weather_lookup("current")
        for product in state.products:
            key = f"product:{product.product_id}"
            if key not in state.tool_results:
                executed_actions.append("lookup_product")
                state.tool_results[key] = self.product_lookup(product)
        if nlp_result is not None:
            for query in nlp_result.product_queries:
                qkey = f"product_query:{query.text}"
                if qkey not in state.tool_results:
                    executed_actions.append("lookup_product")
                    state.tool_results[qkey] = self.catalog_adapter.search_by_name(query.text)

    def _build_recommendation(
        self,
        state: RuntimeSessionState,
        evaluated: dict,
        executed_actions: list[RuntimeActionKind],
    ) -> RecommendationBundle:
        lifestyle: list[RecommendationItem] = []
        for g in evaluated["raw"].get("guidance", []):
            lifestyle.append(
                RecommendationItem(
                    category="lifestyle_adjustment",
                    title=", ".join(g["card_ids"]),
                    guidance=g["text"],
                    evidence_refs=[f"kb:{cid}" for cid in g["card_ids"]],
                )
            )

        owned_usage: list[RecommendationItem] = []
        exclusions: list[ExclusionItem] = []
        alternatives: list[RecommendationItem] = []
        excluded_ids = set(state.profile.excluded_product_ids)

        for product in state.products:
            if product.product_id in excluded_ids:
                exclusions.append(
                    ExclusionItem(
                        product_id=product.product_id,
                        disposition="candidate_excluded",
                        reason="사용자 프로필의 제외 제품 목록에 포함되어 있습니다.",
                    )
                )
                continue
            lookup = state.tool_results.get(f"product:{product.product_id}")
            label = lookup.data.get("label_guidance") if lookup else None
            evidence = lookup.data.get("evidence_ref") if lookup else None
            if (
                product.confirmed and lookup and lookup.status == "found"
                and lookup.query_key == product.product_id
                and lookup.version == product.version
                and product.version.strip().casefold() not in {"", "unknown"}
                and isinstance(label, str) and label.strip()
                and isinstance(evidence, str) and evidence.strip()
            ):
                owned_usage.append(
                    RecommendationItem(
                        category="owned_product_usage",
                        title=str(lookup.data.get("name", product.product_id)),
                        guidance=label,
                        product_id=product.product_id,
                        evidence_refs=[evidence],
                    )
                )
            else:
                exclusions.append(
                    ExclusionItem(
                        product_id=product.product_id,
                        disposition="usage_held",
                        reason="사용자 확인과 해당 제품 버전의 표시 사용법 및 출처가 모두 필요합니다.",
                    )
                )
                executed_actions.append("lookup_alternative")
                alt_lookup = self.alternative_lookup(product.product_id)
                state.tool_results[f"alternative:{product.product_id}"] = alt_lookup
                if alt_lookup.status == "found":
                    for cand in alt_lookup.data.get("candidates", []):
                        alternatives.append(
                            RecommendationItem(
                                category="alternative_candidate",
                                title=str(cand["title"]),
                                guidance=str(cand["guidance"]),
                                product_id=str(cand["product_id"]),
                                evidence_refs=[str(cand.get("evidence_ref", "alternative:synthetic"))],
                            )
                        )

        return RecommendationBundle(
            lifestyle_adjustments=lifestyle,
            owned_product_usage=owned_usage,
            exclusions_or_holds=exclusions,
            alternatives=alternatives,
        )

    def _await_question(
        self, state: RuntimeSessionState, question_id: str, question_text: str, action: RuntimeActionKind,
        executed_actions: list[RuntimeActionKind], nlp: NLPExtractionResult | None,
        *, symptom_confirmation: bool = False,
    ) -> RuntimeTurnResponse:
        executed_actions.append(action)
        if action == "confirm_candidate" or symptom_confirmation:
            choices, answers = symptom_choices(compact=symptom_confirmation)
        else:
            choices, answers = observation_choices(
                question_id, branch_values(self.kb_adapter, state.active_cards, question_id),
            )
        state.turn_index += 1
        question = RuntimeQuestion(
            id=question_id, text=question_text, turn_index=state.turn_index, choices=choices,
        )
        state.pending_question = question
        state.pending_choice_answers = answers
        state.pending_action = action
        state.status = "awaiting_user"
        self._sessions[state.request_id] = state
        return RuntimeTurnResponse(
            request_id=state.request_id, status=state.status,
            executed_actions=executed_actions, pending_action=action,
            questions=[question.model_copy(deep=True)], nlp=nlp, tool_results=state.tool_results,
        )

    def _handle_product_evidence(self, request, previous):
        if previous is None:
            raise ValueError("product evidence requires an existing session")
        state = previous.model_copy(deep=True)
        selection = request.product_evidence_selection
        result = lookup_product_evidence(selection, state.products, self.product_lookup)
        confirmed = not (result.status == "unavailable" and result.reason == "product_or_version_not_confirmed")
        if result.status == "unavailable" and confirmed:
            if selection not in state.pending_product_evidence:
                state.pending_product_evidence.append(selection)
        elif selection in state.pending_product_evidence:
            state.pending_product_evidence.remove(selection)
        self._sessions[request.request_id] = state
        return RuntimeTurnResponse(
            request_id=request.request_id, status=state.status,
            executed_actions=["lookup_product_evidence"] if confirmed else [],
            pending_action=state.pending_action, questions=[state.pending_question] if state.pending_question else [],
            product_evidence=result, pending_product_evidence=state.pending_product_evidence,
        )

    def handle_turn(self, request: RuntimeTurnRequest) -> RuntimeTurnResponse:
        prev = self._sessions.get(request.request_id)
        if request.product_evidence_selection is not None:
            return self._handle_product_evidence(request, prev)
        request_fingerprint = sha256(
            json.dumps(request.model_dump(mode="json"), sort_keys=True).encode("utf-8")
        ).hexdigest()
        no_new_input = (
            not request.message.strip() and not request.observations
            and not request.confirmations and not request.resolve_conflicts
            and request.profile is None and request.products is None
            and request.choice_selection is None
        )
        if (
            prev is not None and prev.status == "awaiting_user" and prev.pending_question is not None
            and (no_new_input or request_fingerprint == prev.last_turn_fingerprint)
        ):
            return RuntimeTurnResponse(
                request_id=request.request_id, status="awaiting_user",
                pending_action=prev.pending_action,
                questions=[prev.pending_question.model_copy(deep=True)],
                tool_results=deepcopy(prev.tool_results),
            )
        observations = request.observations
        confirmations = request.confirmations
        resolve_conflicts = request.resolve_conflicts
        selection = request.choice_selection
        if selection is not None:
            if (
                prev is None or prev.status != "awaiting_user" or prev.pending_question is None
                or prev.pending_question.turn_index != selection.turn_index
                or prev.pending_question.id != selection.question_id
                or selection.choice_id not in prev.pending_choice_answers
            ):
                raise ValueError("stale question or invalid choice")
            answer = prev.pending_choice_answers[selection.choice_id]
            if isinstance(answer, ObservationSlot):
                observations = {selection.question_id: answer}
                previous_answer = prev.confirmed_observations.get(selection.question_id)
                if prev.pending_action == "resolve_conflict" or (
                    previous_answer is not None and previous_answer.state == "conflicting"
                ):
                    resolve_conflicts = (selection.question_id,)
            else:
                confirmations = {selection.question_id: answer}
        state = (
            prev.model_copy(deep=True)
            if prev is not None
            else RuntimeSessionState(
                request_id=request.request_id,
                profile=request.profile.model_copy(deep=True) if request.profile else Profile(),
                products=[p.model_copy(deep=True) for p in (request.products or [])],
            )
        )
        state.last_turn_fingerprint = request_fingerprint
        state.pending_question = None
        state.pending_choice_answers = {}
        state.pending_action = None
        state.afa_handoff = None
        state.afa_step_decision = None
        state.afa_question_scores = []
        state.afa_hold_review_slot = None
        if prev is not None:
            if request.profile is not None:
                state.profile = request.profile.model_copy(deep=True)
            if request.products is not None:
                new_products = {product.product_id: product for product in request.products}
                for product in state.products:
                    if new_products.get(product.product_id) != product:
                        state.tool_results.pop(f"product:{product.product_id}", None)
                        state.tool_results.pop(f"alternative:{product.product_id}", None)
                state.products = [p.model_copy(deep=True) for p in request.products]
                state.pending_product_evidence = [
                    item for item in state.pending_product_evidence
                    if (product := new_products.get(item.product_id)) is not None
                    and product.confirmed and product.version == item.version
                ]

        self._merge_observations(state, observations, resolve_conflicts)
        self._apply_confirmations(state, confirmations)
        executed_actions: list[RuntimeActionKind] = []

        nlp_result: NLPExtractionResult | None = None
        if request.message.strip():
            nlp_result = self.nlp_layer.analyze(request.message, namespace=f"t{state.turn_index + 1}")
            existing_ids = {c.candidate_id for c in state.pending_candidates} | set(state.confirmed_candidates)
            for cand in nlp_result.symptom_candidates:
                if cand.state in ("affirmed", "unknown", "conflict") and cand.candidate_id not in existing_ids:
                    state.pending_candidates.append(cand)
            if self.auto_apply_nlp_features:
                for cand in nlp_result.feature_candidates:
                    if cand.slot_id not in state.confirmed_observations:
                        state.confirmed_observations[cand.slot_id] = ObservationSlot(
                            variable_id=cand.slot_id,
                            state=cand.state,
                            value=cand.value,
                            source="user_report",
                            confirmed_by_user=True,
                        )

        self._run_tools(state, nlp_result, executed_actions)

        hints = list(nlp_result.topic_hints) if nlp_result else []
        card_ids = self._select_cards(state, hints, state.confirmed_observations)
        evaluated = self.kb_adapter.evaluate(state.confirmed_observations, card_ids)

        if any(sig in MANDATORY_HOLD_SIGNALS for sig in evaluated["hold_signals"]):
            executed_actions.append("hold")
            state.status = "held"
            state.turn_index += 1
            self._sessions[request.request_id] = state
            return RuntimeTurnResponse(
                request_id=request.request_id,
                status="held",
                executed_actions=executed_actions,
                nlp=nlp_result,
                hold_reason="안전 또는 품질 확인이 필요하여 개별 권고를 보류합니다.",
                tool_results=state.tool_results,
            )

        conflicts = sorted(
            key for key, slot in state.confirmed_observations.items() if slot.state == "conflicting"
        )
        policy = self.afa_policy
        myopic = isinstance(policy, MyopicVOIAFAPolicy)
        if conflicts and not myopic:
            field = conflicts[0]
            return self._await_question(
                state, field, f"{field} 값이 상충합니다. 확인해 주세요.",
                "resolve_conflict", executed_actions, nlp_result,
            )

        if state.pending_candidates and not myopic:
            cand = state.pending_candidates[0]
            return self._await_question(
                state, cand.candidate_id, cand.prompt_ko,
                "confirm_candidate", executed_actions, nlp_result,
            )

        unrecognized = {
            key
            for row in evaluated["raw"].get("results", [])
            for key in row.get("unrecognized_fields", [])
        }
        state.unrecognized_fields = sorted(unrecognized)
        retrieve_slots = required_product_evidence(evaluated)
        answered = {
            key
            for key, slot in state.confirmed_observations.items()
            if slot.state in ANSWERED_STATES and not (slot.state == "known" and key in unrecognized)
        }
        cards_by_slot: dict[str, list[str]] = {}
        for question in evaluated["raw"]["questions"]:
            cards_by_slot.setdefault(question["field"], []).extend(question.get("card_ids", []))
        unique_candidates = [
            QuestionCandidate(
                slot_id=field,
                question_text=text,
                card_ids=list(dict.fromkeys(cards_by_slot[field])),
            )
            for field, text in evaluated["ask_slots"].items()
            if field in cards_by_slot and field not in answered and not field.startswith("product.")
        ]
        if isinstance(policy, RoutedAFAPolicy) and (
            "B-C02" not in card_ids or set(card_ids).difference({"B-C01", "B-C02"})
            or any(candidate.card_ids != ["B-C02"] for candidate in unique_candidates)
        ):
            policy = policy.baseline
        if myopic:
            # Legacy policies can clarify unrecognized known values. This policy
            # treats all reported states as answered, including on fallback.
            unique_candidates = [
                candidate for candidate in unique_candidates
                if candidate.slot_id not in state.confirmed_observations
                or state.confirmed_observations[candidate.slot_id].state not in ANSWERED_STATES
            ]
        evidence_sufficient = (
            not evaluated["hold_signals"] and not retrieve_slots and evaluated["raw"]["overall"] != "hold"
            and not conflicts
        )
        can_stop_sufficient = not unique_candidates and evidence_sufficient
        can_stop_insufficient = not unique_candidates and not evidence_sufficient
        permissions = {
            "can_stop_sufficient": can_stop_sufficient,
            "can_stop_insufficient": can_stop_insufficient,
        }
        # Simulate the same confirmation that a numbered reply would submit.
        # The NLP candidate remains unconfirmed in the live session.
        answer_evaluations = {}
        symptom_questions = []
        if myopic and state.pending_candidates:
            _, answers = symptom_choices(compact=True)
            for cand in state.pending_candidates:
                symptom_questions.append(QuestionCandidate(
                    slot_id=cand.candidate_id,
                    question_text=f"언급한 {cand.label}은 최근 한 번 있었나요, 반복되거나 계속됐나요?",
                    card_ids=["B-B01"],
                ))
                evaluations = []
                for answer in ("recent", "repeated", "persistent"):
                    simulated = state.model_copy(deep=True)
                    self._apply_confirmations(simulated, {cand.candidate_id: answers[answer]})
                    simulated_cards = self._select_cards(simulated, [], simulated.confirmed_observations)
                    evaluations.append(self.kb_adapter.evaluate(
                        simulated.confirmed_observations, simulated_cards,
                    ))
                answer_evaluations[cand.candidate_id] = evaluations
        candidate_by_id = {candidate.slot_id: candidate
                           for candidate in [*unique_candidates, *symptom_questions]}
        try:
            if myopic:
                scores = policy.score_candidates(
                    deepcopy(state.confirmed_observations), deepcopy(list(candidate_by_id.values())),
                    adapter=self.kb_adapter, card_ids=card_ids, evaluated=evaluated,
                    answer_evaluations=answer_evaluations,
                )
                eligible = {score.slot_id for score in scores if score.decision_change_rate > 0}
                can_stop_sufficient = not eligible and evidence_sufficient
                can_stop_insufficient = not eligible and not evidence_sufficient
                decision = policy.decide_scored_step(
                    scores, can_stop_sufficient=can_stop_sufficient,
                    can_stop_insufficient=can_stop_insufficient,
                )
            else:
                eligible = candidate_by_id.keys()
                if self.prioritize_question_outcomes and isinstance(policy, RuleBasedAFAPolicy):
                    unique_candidates = rank_questions(
                        self.kb_adapter, card_ids, state.confirmed_observations, unique_candidates, evaluated,
                    )
                decision = policy.decide_step(
                    deepcopy(state.confirmed_observations), deepcopy(unique_candidates), **permissions,
                )
            if not isinstance(decision, V3AFAStepDecision):
                raise ValueError("unexpected AFA decision")
            if decision.action == "acquire":
                permitted = decision.target_feature in candidate_by_id and decision.target_feature in eligible
            else:
                permitted = (
                    can_stop_sufficient if decision.stop_reason == "sufficient"
                    else can_stop_insufficient
                )
            if not permitted:
                raise ValueError("AFA decision is outside the runtime's permitted actions")
            if myopic:
                state.afa_question_scores = scores
        except (ValueError, TypeError, KeyError, RuntimeError, TimeoutError):
            decision = RuleBasedAFAPolicy().decide_step(
                state.confirmed_observations, unique_candidates, **permissions,
            )

        state.afa_step_decision = decision
        question_slot = decision.target_feature
        if myopic and decision.policy_source == "myopic_voi" and decision.stop_reason == "insufficient":
            try:
                review_slot = select_hold_review_question(
                    self.kb_adapter, card_ids, state.confirmed_observations,
                    (candidate.slot_id for candidate in unique_candidates),
                    evaluated, state.afa_question_scores, policy.stop_lookahead,
                )
            except (ValueError, TypeError, KeyError, RuntimeError, TimeoutError):
                review_slot = None
            if review_slot in candidate_by_id:
                state.afa_hold_review_slot = review_slot
                question_slot = review_slot

        if question_slot is not None:
            chosen = candidate_by_id[question_slot]
            if chosen.slot_id not in state.asked_feature_order:
                state.asked_feature_order.append(chosen.slot_id)
            return self._await_question(
                state, chosen.slot_id, chosen.question_text,
                "ask_user", executed_actions, nlp_result,
                symptom_confirmation=chosen.slot_id in answer_evaluations,
            )

        unanswered = [
            key
            for key, slot in state.confirmed_observations.items()
            if slot.state in ("unknown", "declined")
        ]
        handoff = AFAHandoffResult(
            status=decision.stop_reason or ("sufficient" if can_stop_sufficient else "insufficient"),
            acquired_features=deepcopy(state.confirmed_observations),
            asked_feature_order=list(state.asked_feature_order),
            unanswered_or_declined=unanswered,
            policy_source=decision.policy_source,
        )
        state.afa_handoff = handoff

        if handoff.status == "insufficient":
            executed_actions.append("hold")
            state.status = "held"
            state.turn_index += 1
            self._sessions[request.request_id] = state
            return RuntimeTurnResponse(
                request_id=request.request_id,
                status="held",
                executed_actions=executed_actions,
                nlp=nlp_result,
                afa_handoff=handoff,
                hold_reason=(
                    "확인된 제품 근거가 더 필요하여 개별 권고를 보류합니다."
                    if retrieve_slots else "판단에 필요한 근거가 충분하지 않아 개별 권고를 보류합니다."
                ),
                required_product_evidence=retrieve_slots,
                tool_results=state.tool_results,
            )

        bundle = self._build_recommendation(state, evaluated, executed_actions)
        executed_actions.append("recommend")
        state.status = "completed"
        state.turn_index += 1
        self._sessions[request.request_id] = state
        return RuntimeTurnResponse(
            request_id=request.request_id,
            status="completed",
            executed_actions=executed_actions,
            nlp=nlp_result,
            afa_handoff=handoff,
            recommendation=bundle,
            tool_results=state.tool_results,
        )
