"""Review B-C02 termination against the guidance and effects used by the runtime."""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

from .eda import ROOT, fingerprint
from .partial_context_eval import ToolsFirst, run_case, summarize
from .policy_adapter import PPOAFAPolicy
from .ppo_preflight import MaskedC02Env
from .termination_check import GuardedEnv, GuardedFixtureSession
from .tracking import receipt
from .v67_fixtures import SLOTS


ADVICE_ACTIONS = {"suggest_behavior_change", "inform_general_practice"}


def runtime_outcome(evaluated):
    """Collapse the B-C02 advice tags that share one runtime recommendation path."""
    raw = evaluated["raw"]
    cards = []
    for row in raw["results"]:
        actions = set(row["action_types"])
        if row["card_id"] == "B-C02" and len(actions) == 1 and actions <= ADVICE_ACTIONS:
            actions = {"b_c02_lifestyle_advice"}
        cards.append({
            "card_id": row["card_id"], "status": row["comparison_status"],
            "actions": sorted(actions), "text": row["recommendation_text"],
            "sources": sorted(row["evidence"]["source_ids"]),
            "follow_up": row.get("follow_up", []),
            "policy_conflicts": row.get("policy_conflicts", []),
            "replace_product": row.get("automatic_product_replacement"),
            "needs_human_review": row.get("requires_individual_human_review_for_preview"),
        })
    return {
        "cards": cards,
        "guidance": [(g["text"], sorted(g["card_ids"]), sorted(g["source_ids"]))
                     for g in raw["guidance"]],
        "overall": raw["overall"],
        "holds": sorted(evaluated["hold_signals"]),
        "retrieve": sorted(evaluated["retrieve_slots"]),
    }


class OutcomeFixtureSession(GuardedFixtureSession):
    comparison = staticmethod(runtime_outcome)


class OutcomeEnv(MaskedC02Env):
    def reset(self, *, seed=None, options=None):
        initial = super().reset(seed=seed, options=options)
        self.session = OutcomeFixtureSession(self.book, self.fixture_id)
        return initial


def compare(model_path, split):
    policies = {"tools_first": ToolsFirst(), "ppo": PPOAFAPolicy(model_path)}
    subsets = [subset for count in range(len(SLOTS) + 1) for subset in combinations(SLOTS, count)]
    results = {}
    for gate, env_type in (
        ("original", MaskedC02Env), ("strict", GuardedEnv), ("runtime_outcome", OutcomeEnv),
    ):
        env = env_type(split)
        cases = [
            {"policy": name, **run_case(env, i, prefilled, policy, outcome_signature=runtime_outcome)}
            for i in range(len(env.rows)) for prefilled in subsets for name, policy in policies.items()
        ]
        results[gate] = {
            "cases": cases,
            "prefilled": {
                name: summarize([row for row in cases if row["policy"] == name and row["prefilled"]])
                for name in policies
            },
            "unprefilled": {
                name: summarize([row for row in cases if row["policy"] == name and not row["prefilled"]])
                for name in policies
            },
        }
    return {
        "mode": "development_preview", "production_enabled": False, "split": split,
        "unique_scenarios": len(env.rows), "families": sorted({row["family"] for row in env.rows}),
        "dataset_fingerprint": fingerprint(env.rows), "model": receipt(model_path), "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    model, report = [(ROOT / path).resolve() for path in (args.model, args.report)]
    if any(not path.is_relative_to(ROOT / "outputs") for path in (model, report)) or report.exists():
        parser.error("use outputs/ and a new report file")
    result = compare(model, "val_internal")
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: value["prefilled"] for key, value in result["results"].items()}))


if __name__ == "__main__":
    main()
