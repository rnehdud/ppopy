"""Compare public-context policies on the bounded train-derived C02 fixtures."""
from __future__ import annotations

import argparse
import asyncio
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from random import Random
from statistics import mean

from beauty_agent.action_planner import RuleBasedActionPlanner
from beauty_agent.actions import ActionProposal

from .eda import ROOT, fingerprint
from .v67_fixtures import SLOTS, require
from .v67_reward import check_rewards
from .v67_runtime import FixtureSession, load_response_book

FIXED_ORDERS = {
    "tools_first": SLOTS,
    "friction_first": ("method.friction", "method.tools", "method.drying"),
}
SEEDS = tuple(range(32))


async def choose(context, policy, rng):
    """The selector sees only the current public ActionContext and its RNG."""
    if policy == "runtime_rule":
        return await RuleBasedActionPlanner().plan_action(context)
    offers = context.enabled()
    if policy != "random_enabled":
        questions = [offer for offer in offers if offer.action == "ask_user"]
        drafts = [offer for offer in offers if offer.action == "request_draft"]
        offers = questions or drafts or offers

    if policy in FIXED_ORDERS and offers[0].action == "ask_user":
        offer = min(offers, key=lambda item: FIXED_ORDERS[policy].index(item.target_id))
    else:
        offer = rng.choice(offers) if policy.startswith("random_") else offers[0]
    return ActionProposal(action=offer.action, target_id=offer.target_id)


async def run_episode(session, selector):
    questions = []
    while True:
        prepared = session.prepare_context()
        proposal = await selector(prepared.context)
        _, _, disposition = await session.apply_action(prepared, proposal)
        if disposition is not None:
            return tuple(questions), (proposal.action, proposal.target_id), disposition
        questions.append(proposal.target_id)
        require(len(questions) <= len(SLOTS), "question budget exceeded")


def summarize(rows):
    return {"episodes": len(rows), "mean_questions": mean(r["question_count"] for r in rows),
            "correct_terminal_rate": mean(r["correct_terminal"] for r in rows),
            "mean_return": mean(r["return"] for r in rows),
            "premature_holds": sum(r["reason"] == "premature_hold" for r in rows),
            "missed_drafts": sum(r["reason"] == "missed_draft" for r in rows),
            "reference_mismatches": sum(r["reason"] == "reference_mismatch" for r in rows)}


def context_key(context):
    return fingerprint(context.model_dump(mode="json"))


async def fit_public_tree(book, fixture_ids, terminal_scores):
    """Fit an exact finite tree to these four development worlds.

    Worlds with identical context share one choice. Hidden answers are only
    used to simulate training branches and compute their empirical values.
    """
    choices = {}

    async def context_for(fixture_id, prefix):
        session = FixtureSession(book, fixture_id)
        for target in prefix:
            await session.apply_action(session.prepare_context(),
                                       ActionProposal(action="ask_user", target_id=target))
        return session.prepare_context().context

    async def solve(worlds, prefix):
        groups = defaultdict(list)
        contexts = {}
        for world in worlds:
            context = await context_for(world, prefix)
            key = context_key(context)
            groups[key].append(world)
            contexts[key] = context

        total = 0
        for key, group in groups.items():
            candidates = []
            for offer in contexts[key].enabled():
                pair = (offer.action, offer.target_id)
                if offer.action == "ask_user":
                    value = await solve(group, (*prefix, offer.target_id))
                else:
                    value = sum(terminal_scores[world, prefix, pair]["return"] for world in group)
                candidates.append((value, pair))
            value, pair = max(candidates)
            require(key not in choices or choices[key] == pair, "conflicting public tree decision")
            choices[key] = pair
            total += value
        return total

    total = await solve(fixture_ids, ())
    return choices, total / len(fixture_ids)


async def compare_baselines():
    reward = await check_rewards()
    book, fixture_ids, _ = load_response_book()
    terminal_scores = {
        (row["fixture_id"], tuple(row["prefix"]), tuple(row["choice"])): row
        for row in reward["terminal_trace"]
    }
    seeds_by_policy = {name: (0,) for name in ("runtime_rule", *FIXED_ORDERS)}
    seeds_by_policy.update(random_questions=SEEDS, random_enabled=SEEDS)
    tree, tree_value = await fit_public_tree(book, fixture_ids, terminal_scores)
    seeds_by_policy["fitted_public_tree"] = (0,)
    rows = []
    summaries = {}
    for name, seeds in seeds_by_policy.items():
        per_fixture = defaultdict(list)
        for seed in seeds:
            for fixture_id in fixture_ids:
                # Equal seeds use identical random streams regardless of fixture identity.
                rng = Random(seed)

                async def select(context):
                    if name == "fitted_public_tree":
                        action, target = tree[context_key(context)]
                        return ActionProposal(action=action, target_id=target)
                    return await choose(context, name, rng)

                questions, stop, disposition = await run_episode(
                    FixtureSession(book, fixture_id), select)
                score = terminal_scores[(fixture_id, questions, stop)]
                require(disposition == score["disposition"], "runtime/scoring contract drift")
                result = {**score, "policy": name, "seed": seed, "split": "train"}
                rows.append(result)
                per_fixture[fixture_id].append(result)
        summaries[name] = {**summarize([r for cases in per_fixture.values() for r in cases]),
                           "per_fixture": {fid: summarize(cases) for fid, cases in per_fixture.items()}}
    require(summaries["fitted_public_tree"]["mean_return"] == tree_value,
            "tree fit and rollout scores differ")
    return {"entry": "E25", "mode": "development_preview", "production_enabled": False,
            "human_review": "unreviewed", "independent_evaluation": False,
            "scope": "same four train-derived fixtures across policies; repeats are not independent cases",
            "fixture_ids": fixture_ids, "seeds_by_policy": seeds_by_policy,
            "fixed_question_orders": FIXED_ORDERS, "protocol": reward["protocol"], "gamma": reward["gamma"],
            "shaping_beta": reward["shaping_beta"], "new_policy_training_runs": 0,
            "posthoc_per_fixture_upper_bound": reward["best_reachable_valid_stop_by_fixture"],
            "fitted_public_tree_expected_return": tree_value,
            "fitted_public_tree_choices": {k: list(v) for k, v in tree.items()},
            "source_hashes": reward["source_hashes"], "summary": summaries, "episodes": rows,
            "comparison_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=lambda value: (ROOT / value).resolve(), required=True)
    path = parser.parse_args().report
    require(path.is_relative_to(ROOT / "outputs"), "report must be inside outputs")
    result = asyncio.run(compare_baselines())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({policy: {k: v for k, v in values.items() if k != "per_fixture"}
                      for policy, values in result["summary"].items()}))


if __name__ == "__main__":
    main()
