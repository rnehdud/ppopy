import numpy as np
import pytest

from beauty_agent.afa.ppo_preflight import MaskedC02Env, dataset, verify_development_overlap
from beauty_agent.afa.v67_runtime import ACTIONS


def test_split_keeps_prior_probe_families_and_variants_together():
    splits = dataset()
    assert [len(rows) for rows in splits.values()] == [32, 16, 16]
    assert [len({row["family"] for row in rows}) for rows in splits.values()] == [8, 4, 4]
    assert set(verify_development_overlap(splits)) == {
        "hands:gentle", "scrub_brush:gentle", "scrub_brush:strong",
        "unknown:gentle", "unknown:strong",
    }


def test_masked_environment_rejects_draft_and_observation_excludes_fixture_identity():
    env = MaskedC02Env("train")
    first, _ = env.reset(options={"index": 0})
    second, _ = env.reset(options={"index": 1})
    np.testing.assert_array_equal(first, second)
    draft = ACTIONS.index(("request_draft", "label_draft"))
    with pytest.raises(ValueError, match="masked action"):
        env.step(draft)
    assert env.session.dispatch_count == 0
    hold = ACTIONS.index(("hold", "insufficient_information"))
    _, reward, terminated, truncated, info = env.step(hold)
    assert (reward, terminated, truncated, info["reason"]) == (-4, True, False, "premature_hold")
    assert not env.action_masks().any()
