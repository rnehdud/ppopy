"""Masked 64-feature Gym environment for the response-complete C01+C02 task."""
from __future__ import annotations

import asyncio
from copy import deepcopy
import json

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from beauty_agent.actions import ActionProposal
from .joint_data import BUNDLE, load_joint_split
from .joint_runtime import JointSessionAdapter
from .scenario_plan import PLAN
from .stage0 import DEFAULT, require, signature


class JointAFAEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, split="train", cost_protocol="unit_primary", *, bundle=BUNDLE):
        self._records = load_joint_split(split, bundle)
        self._plan = json.loads(PLAN.read_text(encoding="utf-8"))
        require(cost_protocol in self._plan["cost_protocols"], "unsupported cost protocol")
        self._cost = deepcopy(self._plan["cost_protocols"][cost_protocol])
        base = json.loads(DEFAULT.read_text(encoding="utf-8"))
        self._schema = base["observation_schema"]
        self._pairs = [tuple(pair) for pair in base["action_dictionary"]]
        self.action_space = spaces.Discrete(len(self._pairs))
        high = np.ones(64, dtype=np.float32)
        high[57], high[58:63], high[63] = 5, 2, 7
        self.observation_space = spaces.Box(np.zeros_like(high), high, dtype=np.float32)
        self._inspector = JointSessionAdapter().inspector
        self._runtime = self._prepared = self._world = None
        self._remaining, self._remaining_cost = 5, self._cost["max_acquisition_cost"]
        self._done, self._stepping = True, False

    @property
    def dispatch_count(self):
        return self._runtime.dispatch_count if self._runtime else 0

    @property
    def visible_observations(self):
        require(self._prepared is not None, "reset required")
        return {k: v.model_dump() for k, v in self._prepared.state.confirmed_observations.items()}

    def _mask(self, prepared, remaining, cost_left, done=False):
        enabled = {(a.action, a.target_id) for a in prepared.context.enabled()}
        return np.array([not done and pair in enabled and (pair[0] != "ask_user" or
            (remaining > 0 and self._cost["ask_costs"][pair[1]] <= cost_left)) for pair in self._pairs], dtype=bool)

    def action_masks(self):
        require(self._prepared is not None, "reset required")
        return self._mask(self._prepared, self._remaining, self._remaining_cost, self._done)

    def _encode(self, prepared, remaining, cost_left, done=False):
        observations = prepared.state.confirmed_observations
        vector = []
        for slot in self._schema["slot_order"]:
            state = observations[slot].state if slot in observations else "not_asked"
            vector.extend(float(state == item) for item in self._schema["state_order"])
        for slot in self._schema["slot_order"]:
            value = observations[slot].value if slot in observations and observations[slot].state == "known" else None
            vector.extend(float(value == item) for item in self._schema["value_order"][slot])
        vector.extend([1.0, 1.0])  # both cards are public task configuration
        vector.extend(self._mask(prepared, remaining, cost_left, done).astype(float))
        vector.append(float(remaining))
        vector.extend(float(self._cost["ask_costs"][slot]) for slot in self._schema["slot_order"])
        vector.append(float(cost_left))
        result = np.asarray(vector, dtype=np.float32)
        require(self.observation_space.contains(result), "joint observation schema violation")
        return result

    def reset(self, *, seed=None, options=None):
        require(not self._stepping, "reset during step rejected")
        super().reset(seed=seed)
        options = options or {}
        require(set(options) <= {"world_index"}, "unsupported reset option")
        index = options["world_index"] if "world_index" in options else int(self.np_random.integers(len(self._records)))
        require(type(index) is int or isinstance(index, np.integer) and not isinstance(index, np.bool_), "invalid world index")
        require(0 <= index < len(self._records), "invalid world index")
        runtime = JointSessionAdapter(self._inspector)
        prepared = runtime.prepare_context()
        remaining, left = self._cost["max_questions"], self._cost["max_acquisition_cost"]
        observation = self._encode(prepared, remaining, left)
        self._runtime, self._prepared = runtime, prepared
        self._world = deepcopy(self._records[int(index)]["environment_only"])
        self._remaining, self._remaining_cost, self._done = remaining, left, False
        return observation, {"dispatch_count": 0}

    def _answer(self, target):
        require(target in self._world["response_table"], "undefined response; no transition committed")
        slot = deepcopy(self._world["response_table"][target])
        require(slot["variable_id"] == target, "response target mismatch")
        return {"event_id": "answer:" + target, "slot": slot}

    def _fork_for_validation(self):
        """Private in-memory branch for exhaustive mechanics checks, never a policy input."""
        require(not self._stepping and self._prepared is not None, "cannot fork an active/uninitialized step")
        clone = object.__new__(type(self))
        clone.__dict__ = self.__dict__.copy()
        clone._runtime = self._runtime.fork()
        clone._world = deepcopy(self._world)
        clone._np_random = deepcopy(self.np_random)
        return clone

    def step(self, action):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.astep(action))
        raise RuntimeError("use await env.astep(action) inside an existing event loop")

    async def astep(self, action):
        require(not self._stepping, "concurrent step rejected")
        self._stepping = True
        try:
            require(self._prepared is not None and not self._done, "reset required after termination")
            require(isinstance(action, (int, np.integer)) and not isinstance(action, (bool, np.bool_)) and
                    self.action_space.contains(action), "invalid action index")
            index = int(action)
            require(self.action_masks()[index], "masked action; no transition committed")
            kind, target = self._pairs[index]
            offer = next(a for a in self._prepared.context.enabled() if (a.action, a.target_id) == (kind, target))
            working = self._runtime.fork()
            _, _, outcome = await working.apply_action(self._prepared,
                ActionProposal(action=kind, target_id=target, evidence_refs=offer.evidence_refs))
            remaining, left, reward = self._remaining, self._remaining_cost, 0.0
            done = kind != "ask_user"
            if not done:
                price = self._cost["ask_costs"][target]
                remaining, left = remaining - 1, left - price
                reward -= price
                following = working.prepare_context([self._answer(target)])
                asks = [a for a in following.context.enabled() if a.action == "ask_user"]
                if asks and not any(remaining > 0 and self._cost["ask_costs"][a.target_id] <= left for a in asks):
                    done, outcome = True, "task_budget_exhausted"
                    reward -= self._cost["incorrect_terminal_loss"]
            else:
                same = signature(self._prepared.evaluated) == self._world["reference"]
                no_questions = not any(a.action == "ask_user" for a in self._prepared.context.enabled())
                correct = same and kind == self._world["reference_terminal"] and (kind == "request_draft" or no_questions)
                reward -= self._cost["correct_terminal_loss"] if correct else self._cost["incorrect_terminal_loss"]
                following = working.prepare_context()
            observation = self._encode(following, remaining, left, done)
            self._runtime, self._prepared = working, following
            self._remaining, self._remaining_cost, self._done = remaining, left, done
            return observation, float(reward), bool(done), False, {
                "applied_action": [kind, target], "execution_status": outcome, "dispatch_count": working.dispatch_count}
        finally:
            self._stepping = False
