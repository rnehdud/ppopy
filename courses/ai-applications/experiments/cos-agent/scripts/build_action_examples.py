"""Capture synthetic runtime contexts with authored, unreviewed action targets.

Run: uv run python -m scripts.build_action_examples
No model inference, download, collection or baseline-generated reference labels.
"""
import asyncio
import json
from pathlib import Path

from beauty_agent.actions import ActionArguments, ActionProposal
from beauty_agent.action_planner import SFTActionPlanner
from beauty_agent.contracts import ObservationSlot, PlannerMetadata, TurnRequest
from beauty_agent.loop import AgentSession, CandidateConfirmation
from beauty_agent.modules.jev_adapter import JevExtractorAdapter

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "examples/action_sft.synthetic.json"


def fixture_features(message):
    return {"schema_version": "relations-0.5", "products": [],
        "symptoms": [{"symptom": "stinging", "relations": {
            "state": {"value": "affirmed", "status": "candidate", "score": .9},
            "subject": {"value": "self", "status": "candidate", "score": .9}}}] if "따가" in message else [],
        "warnings": ["synthetic_fixture_not_jev_inference"], "clarifications": []}


def observation(key, value=None, state="known"):
    return ObservationSlot(variable_id=key, state=state, value=value,
                           source="synthetic_fixture", confirmed_by_user=True)


class CaptureTarget(SFTActionPlanner):
    # Authored fixture generator, not a trained model execution.
    metadata = PlannerMetadata(provider="custom")

    def __init__(self):
        self.samples = []

    def target(self, conversation, turn, kind, reason, updates):
        self.spec = conversation, turn, kind, reason, updates

    async def plan_action(self, context):
        conversation, turn, kind, reason, updates = self.spec
        # A human-reviewable design target, not a RuleBasedActionPlanner label.
        offer = next(item for item in context.enabled() if item.action == kind)
        proposal = ActionProposal(action=kind, target_id=offer.target_id,
            arguments=ActionArguments(wording="contextual"), question_ko=offer.wording("contextual"),
            evidence_refs=offer.evidence_refs[:1], reason_summary=reason)
        self.samples.append({"conversation_id": conversation, "turn_index": turn,
            "provenance": {"input_kind": "synthetic_fixture", "extraction": "synthetic_injected_features",
                "evidence": "unchanged inactive KB source records; not user-specific clinical evidence",
                "target_kind": "authored_design_target", "human_review": "unreviewed",
                "approved_reference": False},
            "user_updates": updates, "input": context.model_dump(mode="json"),
            "output": proposal.model_dump(mode="json")})
        return proposal


async def build_examples():
    request = TurnRequest.model_validate_json((ROOT / "examples/turn.json").read_text(encoding="utf-8"))
    capture = CaptureTarget()
    extract = JevExtractorAdapter(extractor=fixture_features)

    async def step(session, conversation, turn, kind, reason, message, **updates):
        serialized = {key: {k: v.model_dump(mode="json") for k, v in value.items()}
                      if isinstance(value, dict) else value for key, value in updates.items()}
        capture.target(conversation, turn, kind, reason, serialized)
        return await session.step(message, **updates)

    session = AgentSession(request, planner=capture, extractor=extract, card_ids=["B-C01"])
    await step(session, "symptom_to_draft", 1, "confirm_candidate", "증상의 대상·실제 여부와 관찰 시점을 먼저 확인한다.",
               "어제 밤 세안 뒤 볼이 따가워")
    key = next(iter(session.state.pending_clarifications))
    await step(session, "symptom_to_draft", 2, "ask_user", "대상과 시점 확인 후 누락된 물 온도 관찰을 질문한다.",
        "본인 경험이며 어제 관찰한 내용입니다. 세안 부위는 얼굴입니다.",
        confirmations={key: CandidateConfirmation(subject="self", state="affirmed", observed_at="2026-11-08T12:00:00Z")},
        observations={"method.body_site": observation("method.body_site", "face")})
    await step(session, "symptom_to_draft", 3, "request_draft", "확인과 해당 카드의 관찰 조건이 해소되어 표시 사용법 초안을 요청한다.",
        "미온수로 세안했습니다.", observations={"method.water_temperature": observation("method.water_temperature", "lukewarm")})

    session = AgentSession(request, planner=capture, extractor=extract, card_ids=["B-C04"])
    await step(session, "product_evidence", 1, "retrieve_evidence", "제품 자료 공백은 사용자 질문 대신 근거 조회 대기로 분리한다.",
        "제품 자료를 먼저 확인하고 싶습니다. 비공개 제형 값은 모릅니다.",
        observations={"method.body_site": observation("method.body_site", "face")})

    session = AgentSession(request, planner=capture, extractor=extract, card_ids=["B-C01"])
    await step(session, "conflict", 1, "resolve_conflict", "상충하는 관찰은 명시적 충돌 해결 입력을 요청한다.",
        "이전 물 온도 기록과 지금 기록이 달라 확인이 필요합니다.", observations={
            "method.body_site": observation("method.body_site", "face"),
            "method.water_temperature": observation("method.water_temperature", state="conflicting")})

    session = AgentSession(request, planner=capture, extractor=extract, card_ids=["B-B01"])
    await step(session, "safety_hold", 1, "hold", "KB의 개별 검토 신호를 따라 권고를 보류한다.",
        "합성 사례: 새로 심한 통증이 관찰됐습니다.", observations={
            "method.body_site": observation("method.body_site", "face"),
            "skin.pain": observation("skin.pain", "new_severe")})

    session = AgentSession(request, planner=capture, extractor=extract, card_ids=["B-C01"])
    await step(session, "declined_observation", 1, "hold", "거절한 관찰은 재질문하지 않고 판단 한계를 알린다.",
        "세안 물 온도는 답변하지 않겠습니다.", observations={
            "method.body_site": observation("method.body_site", "face"),
            "method.water_temperature": observation("method.water_temperature", state="declined")})
    return {"schema_version": "synthetic-action-sft-0.1", "human_review": "unreviewed",
            "purpose": "runtime contract examples, not an approved training/evaluation dataset",
            "claims_about_model_improvement": None, "samples": capture.samples}


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(asyncio.run(build_examples()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote synthetic, unreviewed action examples: {OUTPUT.name}")
