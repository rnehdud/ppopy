"""Exhaustive engineering audit, using a raw-engine reference separate from env logic."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np

from .environment import StaticAFAEnv
from .stage0 import DEFAULT, ROOT, require
from .stage1 import SPLITS, encode
from skin_engine.kb_preview.engine import PreviewEngine

MANDATORY = {"refer_for_professional_review", "defer_specific_recommendation",
             "pause_specific_cosmetic_due_to_discomfort", "pause_specific_product_pending_quality_check"}


class RawReference:
    """Fixed static task only; no env encoder/mask/reward or adapter signature reuse."""
    def __init__(self, contract):
        self.contract = contract
        self.engine = PreviewEngine()
        self.pairs = [tuple(p) for p in contract["action_dictionary"]]

    def evaluate(self, card, visible):
        facts = {k: {"state": "known", "value": v, "source": "synthetic_fixture",
                     "reference": "Stage 3 mechanical reference"} for k, v in visible.items()}
        raw = self.engine.evaluate({"mode": "development_preview", "project": "Poppy",
                                   "data_kind": "synthetic", "population": "adult",
                                   "card_ids": [card], "facts": facts})
        asks = {q["field"] for q in raw["questions"] if not q["field"].startswith("product.") and
                self.engine.variables[q["field"]].get("consumer_question_allowed") is True and
                q["field"] not in visible}
        retrieves = {f for row in raw["results"] for f in row["missing_fields"]
                     if f.startswith("product.") and "retrieve_product_evidence" in row["action_types"]}
        mandatory = {a for row in raw["results"] for a in row["action_types"] if a in MANDATORY}
        unresolved = any(r["comparison_status"] in ("unknown", "conflicting", "exception") for r in raw["results"])
        holds = set(mandatory)
        if not asks and not retrieves and unresolved:
            holds.add("unresolved_kb_comparison")
        draft = not (mandatory or asks or retrieves or unresolved)
        semantic = {"cards": [{"card_id": r["card_id"], "status": r["comparison_status"],
                               "actions": sorted(r["action_types"]), "text": r["recommendation_text"]}
                              for r in raw["results"]],
                    "hold_signals": sorted(holds), "overall": raw["overall"]}
        return {"raw": raw, "semantic": semantic, "asks": asks, "mandatory": mandatory,
                "draft": draft, "hold_target": "safety" if mandatory else "insufficient_information"}

    def mask(self, state, remaining, done=False):
        allowed = {( "hold", state["hold_target"])}
        if not state["mandatory"] and remaining > 0:
            allowed.update(("ask_user", q) for q in state["asks"])
        if state["draft"]:
            allowed.add(("request_draft", "label_draft"))
        return np.asarray([not done and pair in allowed for pair in self.pairs], dtype=bool)

    def observation(self, card, visible, remaining, done=False):
        schema = self.contract["observation_schema"]
        # Explicit offsets, independently of StaticAFAEnv._encode.
        result = np.zeros(schema["dimension"], dtype=np.float32)
        offset = 0
        for key in schema["slot_order"]:
            state = "known" if key in visible else "not_asked"
            result[offset + schema["state_order"].index(state)] = 1
            offset += len(schema["state_order"])
        for key in schema["slot_order"]:
            values = schema["value_order"][key]
            result[offset + values.index(visible.get(key))] = 1
            offset += len(values)
        cards = list(self.contract["tasks"])
        result[offset + cards.index(card)] = 1
        offset += len(cards)
        result[offset:offset + len(self.pairs)] = self.mask(self.evaluate(card, visible), remaining, done)
        result[-1] = remaining
        return result

    def transition(self, world, visible, remaining, index):
        card = world["card_id"]
        current = self.evaluate(card, visible)
        require(self.mask(current, remaining)[index], "reference action invalid")
        action, target = self.pairs[index]
        objective = self.contract["objective"]
        after = dict(visible)
        correct = None
        if action == "ask_user":
            after[target] = world["response_table"][target]["value"]
            remaining -= 1
            following = self.evaluate(card, after)
            done = remaining == 0 and bool(following["asks"]) and not following["mandatory"]
            reward = -objective["ask_cost"] - (objective["task_budget_exhausted_loss"] if done else 0)
            outcome = "task_budget_exhausted" if done else "awaiting_user"
        else:
            full = {k: v["value"] for k, v in world["response_table"].items()}
            full_state = self.evaluate(card, full)
            reference_action = "request_draft" if full_state["draft"] else "hold"
            correct = (current["semantic"] == full_state["semantic"] and action == reference_action and
                       (action == "request_draft" or not current["asks"]))
            reward = -(objective["correct_terminal_loss"] if correct else objective["incorrect_terminal_loss"])
            done = True
            outcome = "draft_generated" if action == "request_draft" else "held"
        return after, remaining, float(reward), bool(done), outcome, correct


def verify_world(env, index, reference, public_states):
    world = deepcopy(env._records[index]["environment_only"])
    card = world["card_id"]
    budget = reference.contract["objective"]["max_questions"]
    transitions = []
    terminals = []
    state_count = 0
    invalid_checks = 0
    branch_pairs = set()

    def check_state(observation, visible, remaining, done=False):
        np.testing.assert_array_equal(observation, reference.observation(card, visible, remaining, done))
        np.testing.assert_array_equal(env.action_masks(), reference.mask(reference.evaluate(card, visible), remaining, done))
        require({k: v["value"] for k, v in env.visible_observations.items()} == visible, "visible-answer leak/mismatch")
        require(env.observation_space.contains(observation), "space mismatch")
        if not done:
            key = encode({"card": card, "visible": visible, "remaining": remaining})
            value = observation.tobytes(), env.action_masks().tobytes()
            require(key not in public_states or public_states[key] == value, "private state affected public observation/mask")
            public_states[key] = value

    def replay(prefix):
        observation, info = env.reset(seed=17, options={"world_index": index})
        require(info == {"dispatch_count": 0} and env.dispatch_count == 0, "reset dispatched")
        visible, remaining = {}, budget
        check_state(observation, visible, remaining)
        for step, action in enumerate(prefix):
            after, left, score, done, outcome, _ = reference.transition(world, visible, remaining, action)
            observation, reward, actual_done, truncated, info = env.step(action)
            require((reward, actual_done, truncated) == (score, done, False), "prefix reward/termination mismatch")
            require(info["dispatch_count"] == step + 1 and info["execution_status"] == outcome, "prefix dispatch mismatch")
            check_state(observation, after, left, done)
            require(not done, "prefix must be nonterminal")
            visible, remaining = after, left
        return visible, remaining

    def visit(prefix):
        nonlocal state_count, invalid_checks
        visible, remaining = replay(prefix)
        state_count += 1
        state = reference.evaluate(card, visible)
        expected_mask = reference.mask(state, remaining)
        # All task dictionary actions, including every masked proposal, at every reachable prefix.
        for action, enabled in enumerate(expected_mask):
            if not enabled:
                token, count = env._prepared, env.dispatch_count
                before = env._encode(env._prepared, env._remaining)
                try:
                    env.step(action)
                except ValueError:
                    pass
                else:
                    raise ValueError("masked action accepted")
                require(env._prepared == token and env.dispatch_count == count, "invalid action committed")
                np.testing.assert_array_equal(before, env._encode(env._prepared, env._remaining))
                invalid_checks += 1
        for action in np.flatnonzero(expected_mask):
            action = int(action)
            visible, remaining = replay(prefix)
            after, left, score, done, outcome, correct = reference.transition(world, visible, remaining, action)
            observation, reward, actual_done, truncated, info = env.step(action)
            require((reward, actual_done, truncated) == (score, done, False), "reward/termination mismatch")
            require(info == {"applied_action": list(reference.pairs[action]), "execution_status": outcome,
                             "dispatch_count": len(prefix) + 1}, "dispatch/info mismatch")
            check_state(observation, after, left, done)
            transitions.append({"prefix": prefix, "action": action, "reward": reward,
                                "terminated": done, "correct_terminal": correct})
            if done:
                # Prefix contains acquisitions only; the terminal move itself is cost-free apart from loss.
                total = -len(prefix) * reference.contract["objective"]["ask_cost"] + reward
                terminals.append({"actions": prefix + [action], "return": total,
                                  "correct": correct, "terminal": reference.pairs[action][0]})
                full = reference.evaluate(card, {k: v["value"] for k, v in world["response_table"].items()})
                partial_branch = state["raw"]["results"][0]["matched_branch_id"]
                full_branch = full["raw"]["results"][0]["matched_branch_id"]
                if correct and partial_branch != full_branch:
                    branch_pairs.add((partial_branch, full_branch))
                try:
                    env.step(action)
                except ValueError:
                    pass
                else:
                    raise ValueError("step accepted after terminal")
            else:
                require(len(prefix) < budget, "unbounded acquisition loop")
                visit(prefix + [action])

    visit([])
    good = [t["return"] for t in terminals if t["correct"]]
    bad = [t["return"] for t in terminals if not t["correct"]]
    require(good and bad and max(bad) < min(good), "wrong-exit reward loophole")
    return {"card": card, "world_fingerprint": env._records[index]["world_fingerprint"],
            "prefix_states": state_count, "allowed_transitions": len(transitions),
            "masked_rejections": invalid_checks, "terminal_paths": len(terminals),
            "correct_terminal_paths": len(good), "incorrect_terminal_paths": len(bad),
            "hindsight_best_valid_return": max(good), "worst_valid_return": min(good),
            "best_wrong_exit_return": max(bad), "best_valid_vs_wrong_margin": max(good) - max(bad),
            "worst_valid_vs_wrong_margin": min(good) - max(bad),
            "branch_trace_differences_with_same_semantics": [list(p) for p in sorted(branch_pairs)],
            "transitions": transitions, "terminals": terminals}


def boundary_probes():
    """Controlled internal budget injection + out-of-task safety gate probe, not new data."""
    env = StaticAFAEnv("train")
    index = next(i for i, r in enumerate(env._records) if r["environment_only"]["card_id"] == "B-C01")
    env.reset(options={"world_index": index})
    env._remaining = 1  # Isolated fault/edge probe; does not change the frozen contract/bundle.
    observation, reward, done, truncated, info = env.step(0)
    require(reward == -6 and done and not truncated and info["execution_status"] == "task_budget_exhausted",
            "under-budget boundary incorrect")
    require(env.observation_space.contains(observation) and not env.action_masks().any(), "budget terminal observation")
    env.reset(options={"world_index": index})
    env._remaining = 2
    env.step(0)
    _, _, done, truncated, _ = env.step(1)
    require(not done and not truncated and env._remaining == 0, "last acquisition blocked valid completion")
    action = 7 if env.action_masks()[7] else 5
    _, reward, done, truncated, _ = env.step(action)
    require(reward == 0 and done and not truncated and env.dispatch_count == 3, "free terminal action lost")

    from beauty_agent.actions import build_action_context, ActionProposal
    from beauty_agent.action_runtime import validate_action
    from beauty_agent.contracts import ObservationSlot, TurnRequest
    from beauty_agent.modules.kb_adapter import KBEngineAdapter
    contract = json.loads(DEFAULT.read_text(encoding="utf-8"))
    observed = {k: ObservationSlot(variable_id=k, state="known", value=v,
                 source="synthetic_fixture", confirmed_by_user=True)
                for k, v in {"method.body_site": "face", "skin.pain": "new_severe"}.items()}
    evaluated = KBEngineAdapter().evaluate(observed, ["B-C02", "B-B01"])
    context = build_action_context(TurnRequest.model_validate(contract["initial_request"]),
                                  {}, {"findings": []}, evaluated, {}, observed)
    require([(a.action, a.target_id) for a in context.enabled()] == [("hold", "safety")],
            "mandatory safety gate did not override other actions")
    try:
        validate_action(ActionProposal(action="request_draft", target_id="label_draft"), context)
    except ValueError:
        pass
    else:
        raise ValueError("draft bypassed safety gate")
    return {"normal_budget_exhaustion_reachable": False,
            "under_budget_injected_probe": {"remaining_questions": 1, "expected_return": -6, "passed": True},
            "last_affordable_answer_then_free_completion": True,
            "out_of_scope_B_B01_existing_safety_gate": True,
            "note": "Engineering edge probes only; no contract/data expansion or clinical validation."}


def validate_all(env_factory=StaticAFAEnv, progress=None):
    contract = json.loads(DEFAULT.read_text(encoding="utf-8"))
    reference = RawReference(contract)
    shared_public = {}
    worlds = []
    for split in SPLITS:
        env = env_factory(split)
        for index in range(len(env._records)):
            result = verify_world(env, index, reference, shared_public)
            worlds.append({"split": split, **result})
            if progress:
                progress(split, index)
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "Stage 3 exhaustive engineering diagnostics on pre-inspected design worlds, not policy performance",
            "reference": "raw PreviewEngine plus separate public mask/encoder/score calculation; shared KB is not independently validated",
            "worlds": worlds,
            "boundary_probes": boundary_probes(),
            "summary": {"worlds": len(worlds), "distinct_public_states": len(shared_public),
                        **{key: sum(w[key] for w in worlds) for key in
                           ("prefix_states", "allowed_transitions", "masked_rejections", "terminal_paths")},
                        "minimum_best_valid_vs_wrong_margin": min(w["best_valid_vs_wrong_margin"] for w in worlds)},
            "limitations": ["per-world best path knows hidden answers; hindsight bound only",
                            "all internal splits inspected for API correctness, not an unseen final test",
                            "no independent expert labels, clinical safety proof or learned policy",
                            "normal budget exhaustion unreachable in supported complete grid; stress probes are separate"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(ROOT / "outputs" in args.report.resolve().parents, "report must be inside root outputs/")
    report = validate_all(progress=lambda split, index: print(f"checked {split} world {index}", flush=True))
    report["validator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"]))


if __name__ == "__main__":
    main()
