"""One-step information gain and the KB simulation used by pre-hold review."""
from __future__ import annotations

from collections.abc import Mapping
from itertools import permutations, product
import json
from math import isfinite

from beauty_agent.contracts import ObservationSlot
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from beauty_agent.runtime_contracts import (
    ANSWERED_STATES,
    MANDATORY_HOLD_SIGNALS,
    AFAStepDecision,
    QuestionCandidate,
)
from beauty_agent.v3_contracts import AFACandidateScore


# Predicates implemented by PreviewEngine and special.compare outside rules.json.
# These represent rule cases and do not supply facts to the live session.
_SITE_VALUES = ("face", "hands", "body", "scalp")
_EXPOSURE_VALUES = {
    "sun.outdoor_time": ("none", "prolonged"),
    "sun.water_contact": ("yes", "no", "none"),
    "sun.sweat": ("yes", "no", "none"),
}


def _json_key(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def required_product_evidence(evaluated):
    """Return the product evidence the Control Plane needs before a recommendation."""
    return sorted(
        set(evaluated["retrieve_slots"])
        | {
            item["field"]
            for row in evaluated["raw"].get("results", [])
            if row.get("comparison_status") in ("unknown", "conflicting", "exception")
            for item in row.get("evidence_requests", [])
            if item.get("route") == "retrieve_product_evidence" and item["field"].startswith("product.")
        }
    )


def decision_signature(evaluated):
    """Compare order-independent KB effects, including control-plane retrieval."""
    guidance = tuple(sorted({
        (row["text"], tuple(sorted(row.get("action_types", []))),
         tuple(sorted(row.get("card_ids", []))), tuple(sorted(row["source_ids"])))
        for row in evaluated["raw"]["guidance"]
    }))
    return (
        evaluated["raw"]["overall"], tuple(sorted(evaluated["hold_signals"])),
        tuple(required_product_evidence(evaluated)), guidance,
    )


def branch_values(adapter, cards, slot):
    values = [
        value for card in cards for branch in adapter.engine.rules[card]
        for value in branch["when"].get(slot, []) if value is not None
    ]
    if slot == "method.body_site" and cards:
        values.extend(_SITE_VALUES)
    if "B-P01" in cards:
        values.extend(_EXPOSURE_VALUES.get(slot, ()))
    if (slot == "dose.contact_time" and "B-C03" in cards) or (
        slot == "shaving.blade_use_history" and "B-S06" in cards
    ):
        values.extend(
            scenario["facts"][slot]
            for scenario in adapter.engine.kb["acceptance_scenarios"]
            if slot in scenario["facts"] and set(scenario["card_ids"]).intersection(cards)
            and scenario["facts"][slot] is not None
        )
    return list({_json_key(value): value for value in values}.values())


def _priority(score):
    weight = score.safety_weight / score.question_cost
    return (score.expected_pruned * weight, score.decision_change_rate * weight, score.distinct_outcomes)


def _hypothetical(slot, value):
    return ObservationSlot(variable_id=slot, state="known", value=value,
                           confirmed_by_user=True, source="synthetic_fixture")


def _missing_branch_answers(predicates, observations, open_slots):
    missing = {}
    for slot, values in predicates.items():
        observation = observations.get(slot)
        if slot in open_slots:
            missing[slot] = [value for value in values if value is not None]
        elif not (
            observation and observation.confirmed_by_user and observation.state == "known"
            and observation.value in values
        ):
            return {}
    return missing


def _dependency_first_slots(adapter, cards, observations, open_slots, current, depth):
    """Find current questions that can reach a decision-changing authored branch."""
    options = {}
    simulated = {}

    def evaluate(answers):
        key = tuple(sorted((slot, _json_key(obs.value)) for slot, obs in answers.items()))
        if key not in simulated:
            simulated[key] = adapter.evaluate({**observations, **answers}, cards)
        return simulated[key]

    for card in cards:
        for branch in adapter.engine.rules[card]:
            missing = _missing_branch_answers(branch["when"], observations, open_slots)
            if not 2 <= len(missing) <= depth:
                continue
            for values in product(*missing.values()):
                answers = {slot: _hypothetical(slot, value) for slot, value in zip(missing, values, strict=True)}
                outcome = evaluate(answers)
                if not any(row.get("matched_branch_id") == branch["branch_id"]
                           for row in outcome["raw"]["results"]):
                    continue
                signature = decision_signature(outcome)
                if signature == current:
                    continue
                # With the same evidence still missing, continue only for a
                # separately actionable exception or a mandatory safety hold.
                if (current[2] and signature[2] == current[2]
                    and "review_exception" not in branch["actions"]
                    and not MANDATORY_HOLD_SIGNALS.intersection(outcome["hold_signals"])):
                    continue
                for order in permutations(answers):
                    for index in range(1, len(order)):
                        progress = evaluate({slot: answers[slot] for slot in order[:index]})
                        if (order[index] not in progress["ask_slots"]
                            or MANDATORY_HOLD_SIGNALS.intersection(progress["hold_signals"])):
                            break
                    else:
                        options.setdefault(order[0], set()).add((len(order), signature))
    return options


def select_hold_review_question(adapter, cards, observations, eligible_slots, evaluated, scores, depth):
    """Find one permitted question for the Control Plane's pre-hold review."""
    open_slots = {
        slot for slot in eligible_slots
        if not slot.startswith("product.")
        and (slot not in observations or observations[slot].state not in ANSWERED_STATES)
    }
    if min(depth, len(open_slots)) < 2 or MANDATORY_HOLD_SIGNALS.intersection(evaluated["hold_signals"]):
        return None
    options = _dependency_first_slots(
        adapter, cards, observations, open_slots, decision_signature(evaluated), depth,
    )
    if not options:
        return None
    shortest = min(length for outcomes in options.values() for length, _ in outcomes)
    counts = {slot: sum(length == shortest for length, _ in outcomes) for slot, outcomes in options.items()}
    selected = max(
        (score for score in scores if counts.get(score.slot_id)),
        key=lambda score: counts[score.slot_id] * score.safety_weight / score.question_cost,
        default=None,
    )
    return selected.slot_id if selected else None


class MyopicVOIAFAPolicy:
    """Select only questions with immediate one-answer impact."""

    def __init__(
        self,
        adapter: KBEngineAdapter | None = None,
        *,
        card_ids: list[str] | None = None,
        question_costs: Mapping[str, float] | None = None,
        safety_weights: Mapping[str, float] | None = None,
        stop_lookahead: int = 2,
    ):
        self.adapter = adapter
        self.card_ids = tuple(dict.fromkeys(card_ids)) if card_ids is not None else None
        self.question_costs = dict(question_costs or {})
        self.safety_weights = dict(safety_weights or {})
        if type(stop_lookahead) is not int or not 1 <= stop_lookahead <= 3:
            raise ValueError("stop_lookahead must be 1, 2, or 3")
        # AgentRuntime reads this separately after a valid insufficient stop.
        self.stop_lookahead = stop_lookahead
        for value in (*self.question_costs.values(), *self.safety_weights.values()):
            if not isfinite(value) or value <= 0:
                raise ValueError("question costs and safety weights must be finite and positive")

    def _policy_cards(self, candidates):
        if self.card_ids is not None:
            return list(self.card_ids)
        return sorted({card for candidate in candidates for card in candidate.card_ids}) or None

    def score_candidates(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        adapter: KBEngineAdapter | None = None,
        card_ids: list[str] | None = None,
        evaluated: dict | None = None,
        answer_evaluations: Mapping[str, list[dict]] | None = None,
    ) -> list[AFACandidateScore]:
        """Return per-slot scores and reasons in slot ID order for this snapshot."""
        adapter = adapter or self.adapter or KBEngineAdapter()
        if card_ids is None:
            card_ids = self._policy_cards(available_features)
        if evaluated is None:
            evaluated = adapter.evaluate(observations, card_ids)
        if card_ids is None:
            card_ids = [row["card_id"] for row in evaluated["raw"]["results"]]
        mandatory_hold = bool(MANDATORY_HOLD_SIGNALS.intersection(evaluated["hold_signals"]))
        current = decision_signature(evaluated)
        answered = {field for field, obs in observations.items() if obs.state in ANSWERED_STATES}
        slots = {candidate.slot_id for candidate in available_features}
        open_slots = {slot for slot in slots - answered if not slot.startswith("product.")}
        projected_answers = answer_evaluations or {}
        scores = []
        for slot in sorted(slots):
            fields = {
                "slot_id": slot,
                "question_cost": self.question_costs.get(slot, 1.0),
                "safety_weight": self.safety_weights.get(slot, 1.0),
            }
            if slot.startswith("product."):
                scores.append(AFACandidateScore(**fields, reason="product_evidence"))
                continue
            if slot in answered:
                scores.append(AFACandidateScore(**fields, reason="already_answered"))
                continue
            if mandatory_hold:
                scores.append(AFACandidateScore(**fields, reason="mandatory_hold"))
                continue
            answers = projected_answers.get(slot)
            if answers is None:
                answers = [
                    adapter.evaluate({**observations, slot: _hypothetical(slot, value)}, card_ids)
                    for value in branch_values(adapter, card_ids, slot)
                ]
            if not answers:
                scores.append(AFACandidateScore(**fields, reason="no_branch_values"))
                continue

            changed = skipped = 0
            outcomes = set()
            remaining = open_slots - {slot}
            for result in answers:
                signature = decision_signature(result)
                outcomes.add(signature)
                changed += signature != current
                if MANDATORY_HOLD_SIGNALS.intersection(result["hold_signals"]):
                    skipped += len(remaining)
                else:
                    skipped += len(remaining - result["ask_slots"].keys() - projected_answers.keys())
            scores.append(AFACandidateScore(
                **fields, answer_count=len(answers), expected_pruned=skipped / len(answers),
                decision_change_rate=changed / len(answers), distinct_outcomes=len(outcomes),
                reason="lower_priority" if changed else "zero_impact",
            ))

        # Scores are already sorted by slot ID, so max keeps the first on a tie.
        selected = max((score for score in scores if score.decision_change_rate > 0),
                       key=_priority, default=None)
        if selected is not None:
            selected.reason = "selected"
        return scores

    def decide_step(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        can_stop_sufficient: bool,
        can_stop_insufficient: bool = True,
    ) -> AFAStepDecision:
        adapter = self.adapter or KBEngineAdapter()
        cards = self._policy_cards(available_features)
        evaluated = adapter.evaluate(observations, cards)
        return self.decide_scored_step(
            self.score_candidates(observations, available_features, adapter=adapter,
                                  card_ids=cards, evaluated=evaluated),
            can_stop_sufficient=can_stop_sufficient,
            can_stop_insufficient=can_stop_insufficient,
            mandatory_hold=bool(MANDATORY_HOLD_SIGNALS.intersection(evaluated["hold_signals"])),
        )

    @staticmethod
    def decide_scored_step(
        scores: list[AFACandidateScore], *, can_stop_sufficient: bool,
        can_stop_insufficient: bool, mandatory_hold: bool = False,
    ) -> AFAStepDecision:
        if mandatory_hold:
            can_stop_sufficient = False
        else:
            selected = next((score for score in scores if score.reason == "selected"), None)
            if selected is not None:
                return AFAStepDecision(action="acquire", target_feature=selected.slot_id,
                                       policy_source="myopic_voi")
        if can_stop_sufficient or can_stop_insufficient:
            return AFAStepDecision(action="stop", stop_reason="sufficient" if can_stop_sufficient
                                   else "insufficient", policy_source="myopic_voi")
        raise ValueError("no information-gain candidate or permitted stop")


def rank_questions(adapter, cards, observations, candidates, evaluated):
    """Order questions across active cards for callers that retain baseline STOP rules."""
    if len(candidates) < 2:
        return candidates
    scores = MyopicVOIAFAPolicy(stop_lookahead=1).score_candidates(
        observations, candidates, adapter=adapter, card_ids=cards, evaluated=evaluated,
    )
    by_slot = {score.slot_id: score for score in scores}
    unrecognized = {
        slot for row in evaluated["raw"].get("results", [])
        for slot in row.get("unrecognized_fields", [])
    }
    return sorted(
        candidates,
        key=lambda candidate: (candidate.slot_id in unrecognized, *_priority(by_slot[candidate.slot_id])),
        reverse=True,
    )
