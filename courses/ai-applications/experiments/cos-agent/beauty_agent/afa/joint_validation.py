"""Exhaustively check joint-task state transitions, not policy performance."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .joint_data import BUNDLE, SPLITS
from .joint_environment import JointAFAEnv
from .joint_runtime import diagnostic
from .semantics import SemanticInspector
from .stage0 import ROOT, require, signature
from .stage1 import encode


def verify_world(env, world_index, inspector, public_states):
    env.reset(seed=0, options={"world_index": world_index})
    require(env.dispatch_count == 0 and env.visible_observations == {}, "reset exposed responses or dispatched")
    reference = env._world["reference"]
    reference_terminal = env._world["reference_terminal"]
    seen = set()
    counts = {"states": 0, "valid_transitions": 0, "masked_rejections": 0, "terminal_transitions": 0}

    def visit(current):
        # Contract-derived expected actions, independent of the env mask/encoder/reward.
        events = json.loads(current._prepared.payload)["events"]
        semantic = inspector.inspect(["B-C01", "B-C02"], inspector.ledger(events))
        allowed = {("hold", "safety" if semantic["mandatory_holds"] else "insufficient_information")}
        allowed |= {("ask_user", slot) for slot in semantic["research_question_requirements"]
                    if current._remaining > 0 and current._cost["ask_costs"][slot] <= current._remaining_cost}
        if semantic["draft_permitted_by_contract"]:
            allowed.add(("request_draft", "label_draft"))
        mask = np.array([pair in allowed for pair in current._pairs], dtype=bool)
        np.testing.assert_array_equal(current.action_masks(), mask)
        # Numeric layout calculated here, not by calling _encode for expectations.
        public = current.visible_observations
        expected = np.zeros(64, dtype=np.float32)
        offset = 0
        for slot in current._schema["slot_order"]:
            states = current._schema["state_order"]
            expected[offset + states.index(public[slot]["state"] if slot in public else "not_asked")] = 1
            offset += len(states)
        for slot in current._schema["slot_order"]:
            values = current._schema["value_order"][slot]
            expected[offset + values.index(public[slot]["value"] if slot in public else None)] = 1
            offset += len(values)
        expected[47:49], expected[49:57], expected[57] = 1, mask, current._remaining
        expected[58:63] = [current._cost["ask_costs"][slot] for slot in current._schema["slot_order"]]
        expected[63] = current._remaining_cost
        actual = current._encode(current._prepared, current._remaining, current._remaining_cost)
        np.testing.assert_array_equal(actual, expected)
        # Exclude the mask from the grouping key: including it would hide a
        # bug where identical public answers receive hidden-world-dependent masks.
        key = encode([public, current._remaining, current._remaining_cost, current._cost["ask_costs"]])
        # Same public input, irrespective of actual hidden world, has the same mask.
        value = (actual.tobytes(), mask.tobytes())
        require(key not in public_states or public_states[key] == value, "hidden world affected public observation/mask")
        public_states[key] = value
        if key in seen:
            return
        seen.add(key)
        counts["states"] += 1
        for index, enabled in enumerate(mask):
            if not enabled:
                before, dispatches = current._prepared, current.dispatch_count
                try:
                    current.step(index)
                except ValueError:
                    pass
                else:
                    raise ValueError("masked joint action was accepted")
                require(current._prepared == before and current.dispatch_count == dispatches, "rejected action committed")
                counts["masked_rejections"] += 1
                continue
            child = current._fork_for_validation()
            kind, target = current._pairs[index]
            observation, reward, done, truncated, info = child.step(index)
            require(not truncated and child.observation_space.contains(observation), "unexpected truncation/encoding")
            require(info == {"applied_action": [kind, target], "execution_status": info["execution_status"],
                             "dispatch_count": current.dispatch_count + 1}, "info leak or dispatch mismatch")
            counts["valid_transitions"] += 1
            if kind == "ask_user":
                require(set(child.visible_observations) == set(public) | {target} and target not in public,
                        "wrong answer disclosed or duplicate question")
                require(all(child.visible_observations[k] == v for k, v in public.items()), "prior answer changed")
                require(child.visible_observations[target] == current._world["response_table"][target], "simulator answer mismatch")
                require(reward == -current._cost["ask_costs"][target] and not done, "known core acquisition cost/termination mismatch")
                require(child._remaining == current._remaining - 1 and
                        child._remaining_cost == current._remaining_cost + reward, "budget mismatch")
                require(info["execution_status"] == "awaiting_user", "wrong question execution status")
                visit(child)
                np.testing.assert_array_equal(observation, child._encode(child._prepared, child._remaining, child._remaining_cost))
            else:
                correct = (signature(current._prepared.evaluated) == reference and kind == reference_terminal and
                           (kind == "request_draft" or not semantic["research_question_requirements"]))
                loss = current._cost["correct_terminal_loss"] if correct else current._cost["incorrect_terminal_loss"]
                require(reward == -loss and done and not child.action_masks().any(), "terminal loss/mask mismatch")
                require(info["execution_status"] == ("draft_generated" if kind == "request_draft" else "held"), "wrong terminal status")
                require(child.visible_observations == public, "terminal disclosed new answers")
                terminal_expected = actual.copy()
                terminal_expected[49:57] = 0
                np.testing.assert_array_equal(observation, terminal_expected)
                counts["terminal_transitions"] += 1

    visit(env)
    return counts


def verify():
    rows, public_states = [], {}
    inspector = SemanticInspector()
    for cost in ("unit_primary", "weighted_sensitivity"):
        for split in SPLITS:
            env = JointAFAEnv(split, cost)
            for index, record in enumerate(env._records):
                counts = verify_world(env, index, inspector, public_states)
                rows.append({"cost_protocol": cost, "split": split, "root_world_id": record["root_world_id"], **counts})
            print("checked " + cost + "/" + split, flush=True)
    return {"mode": "development_preview", "production_enabled": False,
            "scope": "all 48 preinspected core worlds under two costs; mechanics only, not test policy scoring",
            "world_cost_cases": len(rows), "distinct_public_vectors": len(public_states),
            "totals": {key: sum(row[key] for row in rows) for key in ("states", "valid_transitions", "masked_rejections", "terminal_transitions")},
            "cases": rows, "shared_reference": "uses the same separately-tested v2 semantic contract; not independent domain validation",
            "learning_executed": False, "policy_performance_evaluated": False,
            "sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                       [Path(__file__), Path(__file__).with_name("joint_environment.py"),
                        Path(__file__).with_name("joint_runtime.py"), BUNDLE / "manifest.json"]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    path = args.report.resolve()
    require(ROOT / "outputs" in path.parents and not path.exists(), "new report inside outputs/ required")
    report = verify()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"cases", "sha256"}}))


if __name__ == "__main__":
    main()
