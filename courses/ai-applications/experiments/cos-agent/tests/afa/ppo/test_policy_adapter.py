from types import SimpleNamespace

import pytest

from beauty_agent.afa.policy_adapter import AFAOptions, PPOAFAPolicy, run_acquisition
from beauty_agent.afa.v67_fixtures import SLOTS
from beauty_agent.afa.v67_runtime import ACTIONS
from beauty_agent.contracts import ObservationSlot
from beauty_agent.runtime_contracts import AFAStepDecision, QuestionCandidate


def candidate(key):
    return QuestionCandidate(slot_id=key, question_text="fixture question")


def observation(key, value=None, state="known"):
    return ObservationSlot(variable_id=key, state=state, value=value,
                           source="synthetic_fixture", confirmed_by_user=True)


class FakeModel:
    observation_space = SimpleNamespace(shape=(15,))
    action_space = SimpleNamespace(n=len(ACTIONS))

    def __init__(self, selection):
        self.selection = selection

    def predict(self, vector, *, action_masks, deterministic):
        assert vector.shape == (15,)
        assert deterministic
        self.mask = action_masks.tolist()
        return ACTIONS.index(self.selection), None


@pytest.mark.parametrize("selection,sufficient,insufficient,expected", [
    (("ask_user", SLOTS[1]), False, False, ("acquire", SLOTS[1], None)),
    (("request_draft", "label_draft"), True, False, ("stop", None, "sufficient")),
    (("hold", "insufficient_information"), False, True, ("stop", None, "insufficient")),
])
def test_load_predict_and_map_with_confirmed_slots_masked(
    monkeypatch, tmp_path, selection, sufficient, insufficient, expected,
):
    contrib = pytest.importorskip("sb3_contrib")
    model = FakeModel(selection)
    path = tmp_path / "trusted.zip"

    def load(model_path, *, device):
        assert model_path == path
        assert device == "cpu"
        return model

    monkeypatch.setattr(contrib.MaskablePPO, "load", load)
    policy = PPOAFAPolicy(path)
    decision = policy.decide_step(
        {SLOTS[0]: observation(SLOTS[0], "hands"), SLOTS[2]: observation(SLOTS[2], state="declined")},
        [candidate(key) for key in SLOTS],
        can_stop_sufficient=sufficient, can_stop_insufficient=insufficient,
    )
    assert (decision.action, decision.target_feature, decision.stop_reason) == expected
    assert decision.policy_source == "ppo_model"
    assert model.mask == [False, True, False, insufficient, False, sufficient]


@pytest.mark.parametrize("selection", [
    ("ask_user", SLOTS[0]),
    ("hold", "safety"),
    ("request_draft", "label_draft"),
])
def test_rejects_masked_predictions(monkeypatch, tmp_path, selection):
    contrib = pytest.importorskip("sb3_contrib")
    monkeypatch.setattr(contrib.MaskablePPO, "load", lambda *a, **kw: FakeModel(selection))
    policy = PPOAFAPolicy(tmp_path / "trusted.zip")
    with pytest.raises(ValueError, match="masked or invalid"):
        policy.decide_step({}, [candidate(SLOTS[1])],
                           can_stop_sufficient=False, can_stop_insufficient=False)
    with pytest.raises(ValueError, match="no permitted"):
        policy.decide_step({}, [], can_stop_sufficient=False, can_stop_insufficient=False)


def test_wrap_rechecks_context_and_preserves_unanswered():
    first, second, third = SLOTS
    initial = {first: observation(first, "hands")}
    seen = []

    def options(observations):
        seen.append(set(observations))
        return AFAOptions([candidate(key) for key in SLOTS], third in observations)

    class ScriptedPolicy:
        def decide_step(self, observations, available_features, *, can_stop_sufficient,
                        can_stop_insufficient=True):
            if available_features:
                return AFAStepDecision(action="acquire", target_feature=available_features[0].slot_id)
            assert can_stop_sufficient
            return AFAStepDecision(action="stop", stop_reason="sufficient")

    handoff = run_acquisition(
        ScriptedPolicy(), initial, options,
        lambda key: observation(third, "pat_gently") if key == third else None,
        max_questions=2,
    )
    assert handoff.status == "sufficient"
    assert handoff.asked_feature_order == [second, third]
    assert handoff.unanswered_or_declined == [second]
    assert set(handoff.acquired_features) == {third}
    assert seen == [{first}, {first}, {first, third}]
    assert set(initial) == {first}


def test_wrap_rejects_unauthorized_stop_and_misaddressed_answer():
    def options(_):
        return AFAOptions([candidate(SLOTS[0])], False)

    class ScriptedPolicy:
        def decide_step(self, *args, **kwargs):
            return self.decision

    policy = ScriptedPolicy()
    policy.decision = AFAStepDecision(action="stop", stop_reason="sufficient")
    with pytest.raises(ValueError, match="disallowed stop"):
        run_acquisition(policy, {}, options, lambda _: None, max_questions=1)
    policy.decision = AFAStepDecision(action="acquire", target_feature=SLOTS[0])
    with pytest.raises(ValueError, match="match the selected feature"):
        run_acquisition(policy, {}, options, lambda _: observation(SLOTS[1], "gentle"), max_questions=1)


def test_legacy_catalog_maps_all_six_indices():
    steps = [AFAStepDecision.from_legacy_action(*pair, policy_source="ppo_model") for pair in ACTIONS]
    assert [step.target_feature for step in steps[:3]] == list(SLOTS)
    assert [step.stop_reason for step in steps[3:]] == ["insufficient", "insufficient", "sufficient"]
