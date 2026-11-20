"""Evaluate a B-C02 draft-stability check without changing the preview engine."""
from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations, product
import json
from pathlib import Path

from beauty_agent.actions import ActionOffer
from beauty_agent.contracts import ObservationSlot

from .eda import ROOT, fingerprint
from .partial_context_eval import ToolsFirst, run_case, summarize
from .policy_adapter import PPOAFAPolicy
from .ppo_preflight import DRYING, FRICTION, TOOLS, MaskedC02Env, response
from .stage0 import signature
from .v67_fixtures import SLOTS
from .v67_runtime import FixtureSession


DOMAINS = dict(zip(SLOTS, (TOOLS, FRICTION, DRYING)))
CARD = ["B-C02"]


def draft_stability(adapter, observations, compare=signature):
    """Find unasked slots whose supported answers can change the KB result."""
    unresolved = [key for key in SLOTS if key not in observations]
    current = fingerprint(compare(adapter.evaluate(observations, CARD)))
    completions = {}
    for values in product(*(DOMAINS[key] for key in unresolved)):
        completed = {
            key: ObservationSlot.model_validate(response(key, value))
            for key, value in zip(unresolved, values)
        }
        completions[values] = fingerprint(
            compare(adapter.evaluate({**observations, **completed}, CARD))
        )
    stable = all(outcome == current for outcome in completions.values())
    influential = []
    for index, key in enumerate(unresolved):
        alternatives = defaultdict(set)
        for values, outcome in completions.items():
            alternatives[values[:index] + values[index + 1:]].add(outcome)
        if any(len(outcomes) > 1 for outcomes in alternatives.values()):
            influential.append(key)
    return stable, influential


class GuardedFixtureSession(FixtureSession):
    """Research-only extension of the existing draft and user-question gate."""

    comparison = staticmethod(signature)

    def _prepare(self, public):
        prepared = super()._prepare(public)
        context = prepared.context
        draft = next((item for item in context.enabled() if item.action == "request_draft"), None)
        if draft is None:
            return prepared
        stable, influential = draft_stability(self._kb, context.observations, self.comparison)
        if stable:
            return prepared
        site_only = {"method.body_site": context.observations["method.body_site"]}
        kb_prompts = self._kb.evaluate(site_only, CARD)["ask_slots"]
        draft.enabled = False
        draft.blocked_by.append("e31:unstable_under_supported_answers")
        for key in influential:
            # Reuse the preview question allowed by the KB schema.
            if key in kb_prompts:
                context.available_actions.append(ActionOffer(
                    action="ask_user", target_id=key, tool="request_user_input",
                    reviewed_text=kb_prompts[key],
                    evidence_refs=["kb:B-C02"], conditions=["e31:unstable_under_supported_answers"],
                ))
        return type(prepared)(prepared.token, context.model_dump_json())


class GuardedEnv(MaskedC02Env):
    def reset(self, *, seed=None, options=None):
        initial = super().reset(seed=seed, options=options)
        self.session = GuardedFixtureSession(self.book, self.fixture_id)
        return initial


def keyed(row):
    return row["policy"], row["fixture_id"], tuple(row["prefilled"])


def compare(model_path, baseline_path):
    previous = json.loads(baseline_path.read_text(encoding="utf-8"))
    policies = {"tools_first": ToolsFirst(), "ppo": PPOAFAPolicy(model_path)}
    prior = {keyed(row): row for row in previous["cases"]}
    subsets = [slots for count in range(len(SLOTS) + 1) for slots in combinations(SLOTS, count)]
    results = {}
    for split in ("val_internal", "train"):
        env = GuardedEnv(split)
        if split == "val_internal" and fingerprint(env.rows) != previous["base_fixture_fingerprint"]:
            raise ValueError("E30 validation fixtures changed")
        split_policies = policies if split == "val_internal" else {"tools_first": policies["tools_first"]}
        cases = [
            {"policy": name, **run_case(env, index, slots, policy)}
            for index in range(len(env.rows)) for slots in subsets
            for name, policy in split_policies.items()
        ]
        if split == "val_internal" and {keyed(row) for row in cases} != prior.keys():
            raise ValueError("E30 and E31 cases do not align")
        cohorts = {}
        for name in split_policies:
            rows = [row for row in cases if row["policy"] == name]
            item = {"prefilled": summarize([row for row in rows if row["prefilled"]])}
            if split == "val_internal":
                prior_correct_free = [
                    row for row in rows if prior[keyed(row)]["initially_sufficient_reference"]
                ]
                item.update({
                    "prior_initially_sufficient": summarize(prior_correct_free),
                    "still_correct_without_questions": sum(
                        row["correct_terminal"] and row["questions"] == 0 for row in prior_correct_free
                    ),
                    "corrected_prior_failures": sum(
                        row["correct_terminal"] and not prior[keyed(row)]["correct_terminal"] for row in rows
                    ),
                    "new_failures": sum(
                        not row["correct_terminal"] and prior[keyed(row)]["correct_terminal"] for row in rows
                    ),
                })
            cohorts[name] = item
        results[split] = {"unique_scenarios": len(env.rows), "cohorts": cohorts, "cases": cases}
    return {
        "entry": "E31", "mode": "development_preview", "production_enabled": False,
        "test_internal_evaluated": False, "new_training_steps": 0,
        "answer_domains": DOMAINS, "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("model", "baseline", "report"):
        parser.add_argument("--" + argument, type=Path, required=True)
    args = parser.parse_args()
    model, baseline, report = [(ROOT / getattr(args, key)).resolve()
                               for key in ("model", "baseline", "report")]
    if any(not path.is_relative_to(ROOT / "outputs") for path in (model, baseline, report)):
        parser.error("all paths must be under outputs/")
    if report.exists():
        parser.error("report path must be new")
    data = compare(model, baseline)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k: result["cohorts"] for k, result in data["results"].items()}))


if __name__ == "__main__":
    main()
