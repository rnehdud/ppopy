"""Bounded v2 semantic certificate and ordered synthetic events, not a Gym runtime."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from itertools import product, permutations
import json
from pathlib import Path

from pydantic import Field

from beauty_agent.actions import build_action_context
from beauty_agent.contracts import Contract, ObservationSlot, TurnRequest
from beauty_agent.modules.kb_adapter import KBEngineAdapter
from .stage0 import DEFAULT, ROOT, audit, require, signature
from .stage1 import encode

SPEC = DEFAULT.parent.parent / "semantic-v2-v1/contract.json"


class ResponseEvent(Contract):
    event_id: str = Field(min_length=1)
    slot: ObservationSlot
    supersedes: str | None = None


class EventLedger:
    """An ordered, copied event stream. No future answers or flattening across turns."""
    def __init__(self, domains, events=()):
        self._domains = deepcopy(domains)
        self._events = []
        self._latest = {}
        for event in events:
            self._append(event)

    def _append(self, raw):
        event = ResponseEvent.model_validate(raw).model_copy(deep=True)
        slot = event.slot
        require(event.event_id not in {e.event_id for e in self._events}, "duplicate event id")
        require(slot.variable_id in self._domains and not slot.variable_id.startswith("product."), "slot outside declared scope")
        require(slot.source == "synthetic_fixture" and slot.confirmed_by_user, "confirmed synthetic events only")
        require(slot.state in {"known", "unknown", "declined", "conflicting"}, "unsupported response state")
        require((slot.state == "known" and slot.value in self._domains[slot.variable_id]) or
                (slot.state != "known" and slot.value is None), "nonanswer must stay null; known value must be in domain")
        previous = self._latest.get(slot.variable_id)
        require(event.supersedes == (previous.event_id if previous else None), "explicit supersedes of latest slot event required")
        self._events.append(event)
        self._latest[slot.variable_id] = event

    def append(self, event):
        result = EventLedger(self._domains, self.events)
        result._append(event)
        return result

    @property
    def events(self):
        return [e.model_dump() for e in self._events]

    @property
    def observations(self):
        return {key: event.slot.model_copy(deep=True) for key, event in self._latest.items()}


class SemanticInspector:
    """Uses all declared domain completions, never the actual hidden rollout world.

    Domains are technical design assumptions, NOT a fitted train prior or proof
    against out-of-domain values. Results are diagnostic requirements, not actions.
    """
    def __init__(self):
        self.base = json.loads(DEFAULT.read_text(encoding="utf-8"))
        self.spec = json.loads(SPEC.read_text(encoding="utf-8"))
        require(self.spec["mode"] == "development_preview" and self.spec["production_enabled"] is False and
                self.spec["approved_reference"] is False and self.spec["runtime_integrated"] is False and
                self.spec["human_review"] == "unreviewed" and self.spec["training_ready"] is False and
                self.spec["branch_id_is_label"] is False and self.spec["merge_different_action_types"] is False,
                "inactive semantic contract required")
        self.domains = {k: values for task in self.base["tasks"].values() for k, values in task["world_domains"].items()}
        self.adapter = KBEngineAdapter()
        for relative, expected in self.base["source_hashes"].items():
            require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, "source drift: " + relative)
        self._cache = {}

    def ledger(self, events=()):
        return EventLedger(self.domains, events)

    def _evaluate(self, cards, observations):
        key = encode([cards, {k: v.model_dump() for k, v in observations.items()}])
        if key not in self._cache:
            evaluated = self.adapter.evaluate(observations, cards)
            request = TurnRequest.model_validate(self.base["initial_request"])
            features = {"schema_version": "relations-0.3", "products": [], "symptoms": [], "clarifications": [], "warnings": []}
            context = build_action_context(request, features, {"findings": []}, evaluated, {}, observations)
            self._cache[key] = evaluated, context
        return self._cache[key]

    def inspect(self, cards, ledger):
        cards = sorted(set(cards))
        require(cards and set(cards) <= self.base["tasks"].keys(), "only declared C01/C02 diagnostic cards supported")
        observations = self.ledger(ledger.events).observations
        domains = {k: values for card in cards for k, values in self.base["tasks"][card]["world_domains"].items()}
        require(set(observations) <= domains.keys(), "event outside selected card scope")
        evaluated, context = self._evaluate(cards, observations)
        current = signature(evaluated)
        mandatory = [s for s in evaluated["hold_signals"] if s != "unresolved_kb_comparison"]
        conflicts = [k for k, slot in observations.items() if slot.state == "conflicting"]
        visible = {k: slot.value for k, slot in observations.items() if slot.state == "known"}
        keys = sorted(domains)
        completions = []
        for values in product(*( [visible[k]] if k in visible else domains[k] for k in keys)):
            full = dict(zip(keys, values))
            full_slots = {k: ObservationSlot(variable_id=k, state="known", value=v,
                          source="synthetic_fixture", confirmed_by_user=True) for k, v in full.items()}
            full_evaluated, _ = self._evaluate(cards, full_slots)
            completions.append((full, encode(signature(full_evaluated))))
        signatures = {semantic for _, semantic in completions}
        stable = len(signatures) == 1 and encode(current) in signatures and not conflicts
        # Slot relevance: vary it while all other completion values stay fixed.
        # Do not infer influence from correlation under a selected train distribution.
        influencing = []
        for slot in keys:
            if slot in visible:
                continue
            by_other_values = {}
            for full, semantic in completions:
                other = encode({k: v for k, v in full.items() if k != slot})
                by_other_values.setdefault(other, set()).add(semantic)
            if any(len(options) > 1 for options in by_other_values.values()):
                influencing.append(slot)
        asked = set(observations)
        require(set(self.spec["required_slots"]) <= domains.keys(), "required slot outside selected scope")
        required_unresolved = [slot for slot in self.spec["required_slots"] if slot not in visible]
        runtime_questions = sorted(a.target_id for a in context.enabled() if a.action == "ask_user" and a.target_id in domains)
        # Preserve the original body-site gate and suppress repeat questions after nonanswers.
        if "method.body_site" not in visible:
            questions = ["method.body_site"] if "method.body_site" not in asked else []
        else:
            relevant = (set(influencing) | set(runtime_questions)) if not stable else set()
            questions = sorted((relevant | set(required_unresolved)) - asked)
        if conflicts or mandatory:
            questions = []
        runtime_draft = any(a.action == "request_draft" for a in context.enabled())
        permitted = stable and runtime_draft and not (required_unresolved or mandatory)
        disposition = ("mandatory_hold" if mandatory else "conflict_hold" if conflicts else
                       "draft_ready" if permitted else "needs_information" if questions else "insufficient_information_hold")
        return {"mode": "development_preview", "production_enabled": False,
                "cards": cards, "current_signature": current, "public_known_values": visible,
                "response_states": {k: slot.state for k, slot in observations.items()},
                "possible_completion_count": len(completions), "possible_signature_count": len(signatures),
                "semantic_certificate": stable, "runtime_draft_enabled": runtime_draft,
                "draft_permitted_by_contract": permitted, "disposition": disposition,
                "runtime_question_candidates": runtime_questions, "research_question_requirements": questions,
                "adapter_extension_required": sorted(set(questions) - set(runtime_questions)),
                "mandatory_holds": mandatory, "required_unresolved": required_unresolved,
                "public_token": hashlib.sha256(encode([self.spec, cards, ledger.events]).encode()).hexdigest(),
                "scope": "bounded synthetic semantic contract diagnostic; no dispatch or expert label"}

    def require_fresh(self, token, cards, ledger):
        require(self.inspect(cards, ledger)["public_token"] == token, "stale semantic preparation after new event")


def event(event_id, variable, value=None, state="known", supersedes=None):
    return {"event_id": event_id, "supersedes": supersedes,
            "slot": {"variable_id": variable, "state": state, "value": value,
                     "source": "synthetic_fixture", "confirmed_by_user": True}}


def verify_contract():
    inspector = SemanticInspector()
    original = audit(inspector.base)
    checked, extensions = 0, set()
    mixed = []
    for world in original["worlds"]:
        answers = world["hidden_synthetic_answers"]
        for order in permutations([key for key in answers if key != "method.body_site"]):
            ledger = inspector.ledger()
            path = []
            while True:
                result = inspector.inspect([world["card"]], ledger)
                extensions.update(result["adapter_extension_required"])
                if result["draft_permitted_by_contract"]:
                    require(result["current_signature"] == world["reference"], "contract accepted a different final meaning")
                    break
                available = result["research_question_requirements"]
                if not available:
                    # Cold C01 remains a valid unresolved hold, never a fabricated draft.
                    require(result["current_signature"] == world["reference"] and world["reference_terminal"] == "hold",
                            "complete supported world stranded before its reference")
                    break
                key = "method.body_site" if "method.body_site" in available else next(k for k in order if k in available)
                ledger = ledger.append(event(str(len(path)), key, answers[key]))
                path.append(key)
                require(len(path) <= len(answers), "repeated/unbounded acquisition")
            checked += 1
            if not world["eligible"]:
                mixed.append({"world_id": world["world_id"], "question_priority": list(order), "questions": path,
                              "final_signature_matches_original_full": True})
    return {"mode": "development_preview", "production_enabled": False,
            "worlds": len(original["worlds"]), "priority_paths": checked,
            "previously_excluded_worlds": sum(not w["eligible"] for w in original["worlds"]),
            "mixed_world_paths": mixed, "adapter_extension_slots": sorted(extensions),
            "reference_status": "mechanical first-match preservation; unreviewed",
            "runtime_integrated": False, "training_data_generated": False,
            "contract_sha256": hashlib.sha256(SPEC.read_bytes()).hexdigest(),
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    path = args.report.resolve()
    require(ROOT / "outputs" in path.parents and not path.exists(), "new report inside outputs/ required")
    report = verify_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "mixed_world_paths"}))


if __name__ == "__main__":
    main()
