"""Run the B-C02 PPO policy with caller-supplied observations and answers."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from beauty_agent.contracts import ObservationSlot
from beauty_agent.runtime_contracts import (
    AFAHandoffResult,
    AFAPolicy,
    AFAStepDecision,
    QuestionCandidate,
)

from .v67_fixtures import SLOTS
from .v67_runtime import ACTIONS

ANSWERED_STATES = frozenset({"known", "unknown", "declined", "not_applicable"})


class PPOAFAPolicy:
    """Adapter for a trusted local E26/E28-format MaskablePPO checkpoint."""

    def __init__(self, model_path: Path):
        from sb3_contrib import MaskablePPO

        self._model = MaskablePPO.load(model_path, device="cpu")
        if self._model.observation_space.shape != (15,) or getattr(
            self._model.action_space, "n", None
        ) != len(ACTIONS):
            raise ValueError("checkpoint does not match the B-C02 experiment spaces")

    def decide_step(
        self,
        observations: dict[str, ObservationSlot],
        available_features: list[QuestionCandidate],
        *,
        can_stop_sufficient: bool,
        can_stop_insufficient: bool = True,
    ) -> AFAStepDecision:
        import numpy as np

        from .ppo_preflight import encode

        confirmed = _confirmed(observations)
        allowed = {candidate.slot_id for candidate in available_features}
        if allowed.difference(SLOTS):
            raise ValueError("question candidate outside the B-C02 checkpoint scope")
        answered = {key for key, slot in confirmed.items() if slot.state in ANSWERED_STATES}
        question_ids = allowed - answered
        # The protocol supplies one generic insufficient flag. Safety is a
        # distinct legacy index with a prerequisite this interface cannot attest.
        enabled = {("ask_user", slot_id) for slot_id in question_ids}
        if can_stop_sufficient:
            enabled.add(("request_draft", "label_draft"))
        if can_stop_insufficient:
            enabled.add(("hold", "insufficient_information"))
        mask = np.asarray([action in enabled for action in ACTIONS], dtype=bool)
        if not mask.any():
            raise ValueError("AFA has no permitted question or stop")
        vector = encode(SimpleNamespace(observations=confirmed))
        action, _ = self._model.predict(vector, action_masks=mask, deterministic=True)
        index = int(action)
        if not 0 <= index < len(ACTIONS) or not mask[index]:
            raise ValueError("model selected a masked or invalid action")
        return AFAStepDecision.from_legacy_action(*ACTIONS[index], policy_source="ppo_model")


def _confirmed(observations: dict[str, ObservationSlot]) -> dict[str, ObservationSlot]:
    """Keep provenance and reject inconsistent slot addressing."""
    if any(key != observation.variable_id for key, observation in observations.items()):
        raise ValueError("observation key does not match its variable ID")
    return {
        key: observation.model_copy(deep=True)
        for key, observation in observations.items()
        if observation.confirmed_by_user
    }


@dataclass(frozen=True)
class AFAOptions:
    """Question candidates and stop permissions for the current public state."""

    features: list[QuestionCandidate]
    can_stop_sufficient: bool
    can_stop_insufficient: bool = True


def run_acquisition(
    policy: AFAPolicy,
    initial_observations: dict[str, ObservationSlot],
    get_options: Callable[[dict[str, ObservationSlot]], AFAOptions],
    get_answer: Callable[[str], ObservationSlot | None],
    *,
    max_questions: int,
) -> AFAHandoffResult:
    """Drive acquisition with provided answers, returning only newly known values.

    Callers own prompting, I/O, and any pause across requests. Here None means
    an unanswered question, and reaching the cap only disables further questions.
    """
    if max_questions < 0:
        raise ValueError("max_questions cannot be negative")
    observations = _confirmed(initial_observations)
    acquired = {}
    asked = []
    unanswered = []
    while True:
        options = get_options(_confirmed(observations))
        blocked = set(asked)
        blocked.update(
            key for key, slot in observations.items()
            if slot.state in ANSWERED_STATES
        )
        candidates = [
            item for item in options.features if item.slot_id not in blocked
        ] if len(asked) < max_questions else []
        available_ids = {item.slot_id for item in candidates}
        decision = policy.decide_step(
            _confirmed(observations),
            candidates,
            can_stop_sufficient=options.can_stop_sufficient,
            can_stop_insufficient=options.can_stop_insufficient,
        )
        if decision.action == "stop":
            permitted = {
                "sufficient": options.can_stop_sufficient,
                "insufficient": options.can_stop_insufficient,
            }
            if not permitted.get(decision.stop_reason):
                raise ValueError("policy selected a disallowed stop")
            return AFAHandoffResult(
                status=decision.stop_reason,
                acquired_features=acquired,
                asked_feature_order=asked,
                unanswered_or_declined=unanswered,
                policy_source=decision.policy_source,
            )

        target = decision.target_feature
        if target is None or target not in available_ids:
            raise ValueError("policy selected a disallowed feature")
        asked.append(target)
        answer = get_answer(target)
        if answer is None:
            unanswered.append(target)
            continue
        if answer.variable_id != target or not answer.confirmed_by_user:
            raise ValueError("answer must be confirmed and match the selected feature")
        observations[target] = answer.model_copy(deep=True)
        if answer.state == "known":
            acquired[target] = observations[target]
        else:
            unanswered.append(target)
