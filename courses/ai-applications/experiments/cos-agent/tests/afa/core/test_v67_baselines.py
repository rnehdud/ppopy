import asyncio

from beauty_agent.afa.v67_baselines import compare_baselines, context_key
from beauty_agent.afa.v67_runtime import FixtureSession, load_response_book


def test_policies_use_shared_initial_context_and_comparable_scores():
    book, fixture_ids, _ = load_response_book()
    assert len({context_key(FixtureSession(book, fid).prepare_context().context)
                for fid in fixture_ids}) == 1

    report = asyncio.run(compare_baselines())
    random_rows = [r for r in report["episodes"] if r["policy"] == "random_enabled"]
    for seed in report["seeds_by_policy"]["random_enabled"]:
        first_actions = {r["prefix"][0] if r["prefix"] else tuple(r["choice"])
                         for r in random_rows if r["seed"] == seed}
        assert len(first_actions) == 1

    rule = report["summary"]["runtime_rule"]
    fitted = report["summary"]["fitted_public_tree"]
    assert fitted["correct_terminal_rate"] == rule["correct_terminal_rate"] == 1
    assert fitted["mean_questions"] < rule["mean_questions"]
    assert fitted["mean_return"] == report["fitted_public_tree_expected_return"]
    assert report["summary"]["random_enabled"]["premature_holds"] > 0
