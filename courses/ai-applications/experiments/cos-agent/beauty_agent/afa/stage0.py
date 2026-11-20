"""Audit the Stage 0 contract against the existing KB/action gate. Not a Gym env."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

from beauty_agent.actions import build_action_context, ActionProposal
from beauty_agent.action_runtime import validate_action
from beauty_agent.contracts import ObservationSlot, TurnRequest
from beauty_agent.modules.kb_adapter import KBEngineAdapter

EXPERIMENT = Path(__file__).resolve().parents[2]
ROOT = EXPERIMENT.parents[3]
DEFAULT = EXPERIMENT / "data/afa/stage0-v1/contract.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def signature(evaluated):
    """Mechanical equality, not expert labels or blanket branch equivalence."""
    raw = evaluated["raw"]
    return {
        "cards": [{"card_id": row["card_id"], "status": row["comparison_status"],
                   "actions": sorted(row["action_types"]), "text": row["recommendation_text"]}
                  for row in raw["results"]],
        "hold_signals": sorted(evaluated["hold_signals"]), "overall": raw["overall"],
    }


def snapshot(contract, card, values, adapter):
    observations = {key: ObservationSlot(variable_id=key, state="known", value=value,
                    source="synthetic_fixture", confirmed_by_user=True)
                    for key, value in values.items()}
    evaluated = adapter.evaluate(observations, [card])
    request = TurnRequest.model_validate(contract["initial_request"])
    features = {"schema_version": "relations-0.3", "products": [], "symptoms": [],
                "clarifications": [], "warnings": []}
    context = build_action_context(request, features, {"findings": []}, evaluated,
                                   {}, observations)
    return context, evaluated


def task_offers(contract, context):
    """An explicit research capability restriction, never a widened runtime gate."""
    pairs = {tuple(pair) for pair in contract["action_dictionary"]}
    return [a for a in context.enabled() if (a.action, a.target_id) in pairs]


def audit(contract):
    require(contract["mode"] == "development_preview" and contract["production_enabled"] is False,
            "inactive preview required")
    require(contract["provenance"]["human_review"] == "unreviewed" and
            contract["provenance"]["approved_reference"] is False, "reference review boundary")
    for relative, expected in contract["source_hashes"].items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected,
                "source drift: " + relative)
    pairs = [tuple(pair) for pair in contract["action_dictionary"]]
    require(len(pairs) == len(set(pairs)), "duplicate action index")
    require(set(contract["tasks"]) == {"B-C01", "B-C02"}, "fixed Stage 0 card scope")
    expected_pairs = {("ask_user", key) for task in contract["tasks"].values()
                      for key in task["world_domains"]}
    expected_pairs |= {("hold", "safety"), ("hold", "insufficient_information"),
                       ("request_draft", "label_draft")}
    require(set(pairs) == expected_pairs, "action dictionary must cover fixed schema")
    require(contract["initial_observations"] == {}, "initial observations must be empty")
    schema = contract["observation_schema"]
    slots = schema["slot_order"]
    require(set(slots) == {k for a, k in pairs if a == "ask_user"}, "observation slot coverage")
    dimension = (len(slots) * len(schema["state_order"]) +
                 sum(len(schema["value_order"][k]) for k in slots) +
                 len(contract["tasks"]) + len(pairs) + 1)
    require(schema["dimension"] == dimension, "numeric schema dimension")
    reward = contract["objective"]
    require(reward["gamma"] == 1 and reward["shaping_beta"] == 0, "total cost objective")
    max_questions = max(len(t["world_domains"]) for t in contract["tasks"].values())
    require(reward["max_questions"] == max_questions, "budget must cover every supported slot")
    require(reward["ask_cost"] > 0 and
            reward["incorrect_terminal_loss"] > max_questions * reward["ask_cost"],
            "wrong exit must cost more than any supported acquisition path")
    adapter = KBEngineAdapter()
    summary = Counter()
    records = []
    for card, task in contract["tasks"].items():
        require(task["world_domains"]["method.body_site"] == ["face"], "face-only scope")
        require(all(not k.startswith("product.") for k in task["world_domains"]),
                "no product evidence injection")
        for key, domain in task["world_domains"].items():
            require(domain and adapter.engine.variables[key]["consumer_question_allowed"] is True,
                    "supported consumer variable required")
        keys = list(task["world_domains"])
        for index, answers in enumerate(product(*(task["world_domains"][k] for k in keys))):
            world = dict(zip(keys, answers))
            full_context, full = snapshot(contract, card, world, adapter)
            reference = signature(full)
            ref_draft = any(a.action == "request_draft" for a in full_context.enabled())
            leaves = []
            mismatches = []

            def visit(visible, path):
                context, evaluated = snapshot(contract, card, visible, adapter)
                offers = task_offers(contract, context)
                for a in offers:
                    validate_action(ActionProposal(action=a.action, target_id=a.target_id,
                                                   evidence_refs=a.evidence_refs), context)
                ask = [a.target_id for a in offers if a.action == "ask_user"]
                require(all(k in world and k not in visible for k in ask),
                        "undefined or repeated response")
                require(len(path) <= reward["max_questions"], "budget exceeded")
                # All available supported question orders, without taking terminal exits.
                draft = any(a.action == "request_draft" for a in offers)
                if draft or not ask:
                    same = signature(evaluated) == reference and draft == ref_draft
                    if not same:
                        mismatches.append(path)
                    leaves.append({"questions": path, "terminal": "request_draft" if draft else "hold",
                                   "signature_matches_full": same,
                                   "cost": len(path) * reward["ask_cost"]})
                    return
                for key in ask:
                    visit({**visible, key: world[key]}, path + [key])

            visit({}, [])
            eligible = not mismatches
            summary["eligible" if eligible else "excluded_semantic_variation"] += 1
            summary[card + (":eligible" if eligible else ":excluded")] += 1
            records.append({"world_id": f"{card}-grid-{index:02d}", "card": card,
                            "hidden_synthetic_answers": world, "eligible": eligible,
                            "exclusion_reason": None if eligible else "reachable_terminal_signature_differs",
                            "reference": reference, "reference_terminal": "request_draft" if ref_draft else "hold",
                            "paths": leaves})
    require(summary["eligible"] > 0 and summary["excluded_semantic_variation"] > 0,
            "need eligible and explicitly excluded worlds")
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "Stage 0 mechanical contract audit; no Gym, learning, v67 split or expert labels",
            "contract_sha256": hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest(),
            "summary": dict(summary), "worlds": records}


def check_examples(contract, report, examples):
    """Check authored technical expectations against actual offers and signatures."""
    adapter = KBEngineAdapter()
    for example in examples["examples"]:
        world = next((w for w in report["worlds"] if w["card"] == example["card"] and
                      w["hidden_synthetic_answers"] == example["world"]), None)
        require(world is not None, "example outside world grid: " + example["id"])
        if example.get("eligibility") is False:
            require(not world["eligible"], "example exclusion not reproduced")
            continue
        require(world["eligible"], "ambiguous example cannot be a reference")
        visible = {}
        for question in example["questions"]:
            context, _ = snapshot(contract, example["card"], visible, adapter)
            offers = {(a.action, a.target_id) for a in task_offers(contract, context)}
            require(("ask_user", question) in offers, "example question is not available")
            visible[question] = example["world"][question]
        context, evaluated = snapshot(contract, example["card"], visible, adapter)
        offers = task_offers(contract, context)
        terminal = example["terminal"]
        require(any(a.action == terminal for a in offers), "example terminal gate rejected")
        exact = signature(evaluated) == world["reference"]
        no_questions = not any(a.action == "ask_user" for a in offers)
        correct = exact and terminal == world["reference_terminal"] and (
            terminal == "request_draft" or no_questions)
        loss = 0 if correct else contract["objective"]["incorrect_terminal_loss"]
        result = -len(example["questions"]) * contract["objective"]["ask_cost"] - loss
        require(result == example["expected_return"], "example return mismatch: " + example["id"])
    return len(examples["examples"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = audit(json.loads(args.contract.read_text(encoding="utf-8")))
    examples = args.contract.with_name("examples.synthetic.json")
    report["authored_examples_verified"] = check_examples(
        json.loads(args.contract.read_text(encoding="utf-8")), report,
        json.loads(examples.read_text(encoding="utf-8")))
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
