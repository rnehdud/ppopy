"""Prioritize eligible questions using known branch values for supported cleansing cards."""
from fractions import Fraction

from beauty_agent.contracts import ObservationSlot


CLEANSING_SCOPE = frozenset({"B-C01", "B-C02", "B-C05"})


def _effect(evaluated):
    raw = evaluated["raw"]
    guidance = tuple(sorted((row["text"], tuple(sorted(row["source_ids"]))) for row in raw["guidance"]))
    return (raw["overall"], tuple(sorted(evaluated["hold_signals"])),
            tuple(sorted(evaluated["retrieve_slots"])), guidance)


def rank_questions(adapter, cards, observations, candidates, evaluated):
    """Prefer questions whose known answers can change outcomes and close other questions.

    Branch values are weighted equally for this ranking. They do not represent a user distribution.
    """
    if len(candidates) < 2 or len(cards) < 2 or "B-C05" not in cards or not set(cards) <= CLEANSING_SCOPE:
        return candidates
    current = _effect(evaluated)
    open_slots = {candidate.slot_id for candidate in candidates}
    answers_by_slot = {
        slot: sorted({
            value for card in cards for branch in adapter.engine.rules[card]
            for value in branch["when"].get(slot, []) if isinstance(value, str)
        }) for slot in open_slots
    }

    def score(candidate):
        slot = candidate.slot_id
        answers = answers_by_slot[slot]
        if not answers:
            return (0, 0, 0)
        changed = skipped = 0
        outcomes = set()
        for value in answers:
            hypothetical = ObservationSlot(
                variable_id=slot, state="known", value=value,
                confirmed_by_user=True, source="synthetic_fixture",
            )
            result = adapter.evaluate({**observations, slot: hypothetical}, cards)
            effect = _effect(result)
            if effect != current:
                changed += 1
                skipped += len(open_slots - {slot} - result["ask_slots"].keys())
                outcomes.add(effect)
        return Fraction(skipped, len(answers)), Fraction(changed, len(answers)), len(outcomes)

    return sorted(candidates, key=score, reverse=True)
