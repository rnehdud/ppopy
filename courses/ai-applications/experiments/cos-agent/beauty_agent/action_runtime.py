"""Validate proposals before a finite dispatcher. Models cannot mutate state."""
import asyncio
from dataclasses import dataclass
import json
import os

from pydantic import ValidationError

from .actions import ActionContext, ActionProposal
from .action_planner import (OllamaActionPlanner, QuestionPlannerAdapter, RuleBasedActionPlanner)
from .contracts import Question, TurnResponse


@dataclass
class ActionDecision:
    proposed: dict | None
    applied: ActionProposal
    validation: list[str]
    fallback_reason: str | None
    provider: str
    model: str | None


def validate_action(proposal, context):
    offer = next((item for item in context.available_actions
                  if (item.action, item.target_id) == (proposal.action, proposal.target_id)), None)
    if offer is None:
        raise ValueError("action_target_not_offered")
    if not offer.enabled:
        raise ValueError("execution_conditions_not_met")
    if not set(proposal.evidence_refs) <= set(offer.evidence_refs):
        raise ValueError("evidence_reference_not_allowed_for_target")
    if proposal.arguments.confirmation_focus != "all" and offer.action != "confirm_candidate":
        raise ValueError("arguments_not_allowed_for_action")
    # Free text is not semantically verified by JSON schema. Only these exact,
    # code-rendered variants may be displayed; everything else is replaced.
    wording = offer.wording(proposal.arguments.wording, proposal.arguments.confirmation_focus)
    replaced = proposal.question_ko is not None and proposal.question_ko != wording
    applied = proposal.model_copy(update={"question_ko": wording})
    return applied, replaced


async def decide_action(context, planner=None, *, timeout=20.0):
    if planner is None:
        provider = os.environ.get("AGENT_PROVIDER", "baseline")
        planner = OllamaActionPlanner() if provider == "ollama" else RuleBasedActionPlanner()
        if provider not in ("baseline", "ollama"):
            # Misconfiguration follows the same deterministic fallback path.
            planner = object()
    if not hasattr(planner, "plan_action") and hasattr(planner, "plan"):
        planner = QuestionPlannerAdapter(planner)
    proposed = None
    validation = []
    provider = "ollama" if isinstance(planner, OllamaActionPlanner) else "baseline"
    model = planner.model if isinstance(planner, OllamaActionPlanner) else None
    try:
        # A custom planner can mutate its copy, never the gate's capability snapshot.
        output = await asyncio.wait_for(planner.plan_action(context.model_copy(deep=True)), timeout=timeout)
        if isinstance(output, ActionProposal):
            output = output.model_dump()
        if isinstance(output, str):
            if len(output.encode("utf-8")) > 65536:
                raise ValueError("proposal_too_large")
            output = json.loads(output)
        if not isinstance(output, dict):
            raise ValueError("proposal_must_be_object")
        if len(json.dumps(output, allow_nan=False).encode("utf-8")) > 65536:
            raise ValueError("proposal_too_large")
        proposed = output.copy()
        proposal = ActionProposal.model_validate(output)
        applied, replaced = validate_action(proposal, context)
        validation.append("contract_and_execution_conditions_valid")
        if replaced:
            validation.append("unverified_question_replaced_with_reviewed_wording")
        if isinstance(planner, QuestionPlannerAdapter):
            provider, model = planner.provider, planner.model
        return ActionDecision(proposed, applied, validation,
            "unverified_question_wording" if replaced else None, provider, model)
    except asyncio.TimeoutError:
        reason = "planner_timeout"
    except (ValidationError, json.JSONDecodeError):
        reason = "invalid_action_contract"
    except ValueError as exc:
        allowed = {"action_target_not_offered", "execution_conditions_not_met",
                   "evidence_reference_not_allowed_for_target", "proposal_too_large", "proposal_must_be_object",
                   "arguments_not_allowed_for_action"}
        reason = str(exc) if str(exc) in allowed else "planner_invalid_output"
    except Exception as exc:
        # Module failures occur before this boundary and still abort the turn.
        # Never expose exception text (may contain remote/user data).
        reason = "planner_error:" + type(exc).__name__
    proposal = await RuleBasedActionPlanner().plan_action(context)
    applied, _ = validate_action(proposal, context)
    return ActionDecision(proposed, applied, ["rejected", "deterministic_baseline_applied"],
                          reason, "baseline_fallback", model)


async def dispatch_action(decision, context: ActionContext, request):
    """Only code-owned handlers; no URLs, arbitrary tools or confirmation writes."""
    applied, _ = validate_action(decision.applied, context)
    action = applied.action
    if action == "request_draft":
        from .agent import missing_information, run_turn
        if missing_information(request):
            raise ValueError("draft prerequisites changed before dispatch")
        result = await run_turn(request)
        if result.status != "draft":
            raise ValueError("draft was not generated")
        return result.model_copy(update={"provider": decision.provider, "model": decision.model}), "draft_generated"
    if action in ("ask_user", "confirm_candidate", "resolve_conflict"):
        # Keep structural blockers visible for compatibility with the old loop.
        qid = "kb:" + applied.target_id if applied.target_id in context.kb_ask_slots else applied.target_id
        questions = [Question(id=qid, text=applied.question_ko)]
        outcome = "awaiting_user"
    elif action == "retrieve_evidence":
        questions, outcome = [], "awaiting_product_evidence"
    elif action == "hold":
        questions, outcome = [], "held"
    else:
        raise ValueError("no dispatcher for action")
    questions.extend(q for q in context.blockers if q.id not in {item.id for item in questions})
    return TurnResponse(status="needs_information", message=applied.question_ko, questions=questions,
                        provider=decision.provider, model=decision.model), outcome
