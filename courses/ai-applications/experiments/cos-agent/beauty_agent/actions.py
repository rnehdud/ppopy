"""Model proposal contracts and code-owned action capabilities. No side effects."""
from typing import Literal

from pydantic import ConfigDict, Field

from .contracts import Contract, ObservationSlot, Question

ActionKind = Literal["ask_user", "confirm_candidate", "retrieve_evidence",
                     "resolve_conflict", "hold", "request_draft"]
ToolName = Literal["request_user_input", "await_product_evidence", "hold_guidance", "generate_label_draft"]


class ActionArguments(Contract):
    model_config = ConfigDict(extra="forbid", strict=True)
    # A finite, code-rendered wording option; never a URL, observation or permission.
    wording: Literal["reviewed", "contextual"] = "reviewed"
    confirmation_focus: Literal["all", "subject", "polarity", "time"] = "all"


class ActionProposal(Contract):
    model_config = ConfigDict(extra="forbid", strict=True)
    action: ActionKind
    target_id: str = Field(min_length=1, max_length=160)
    arguments: ActionArguments = Field(default_factory=ActionArguments)
    question_ko: str | None = Field(default=None, min_length=1, max_length=500)
    evidence_refs: list[str] = Field(default_factory=list, max_length=128)
    reason_summary: str = Field(default="", max_length=500)


class ActionOffer(Contract):
    action: ActionKind
    target_id: str
    tool: ToolName
    enabled: bool = True
    conditions: list[str] = Field(default_factory=list)
    blocked_by: list[str] = Field(default_factory=list)
    reviewed_text: str
    evidence_refs: list[str] = Field(default_factory=list)

    def wording(self, style="reviewed", confirmation_focus="all"):
        text = self.reviewed_text
        if self.action == "confirm_candidate":
            text = {"subject": "앞선 증상·관계 언급은 본인의 경험인가요, 다른 사람의 경험인가요?",
                    "polarity": "앞선 증상이 실제로 있었다는 뜻인가요, 없었다는 뜻인가요?",
                    "time": "앞선 증상·관계를 관찰한 시점을 확인해 주세요."}.get(confirmation_focus, text)
        if style == "contextual" and self.tool == "request_user_input":
            return "앞서 말씀하신 내용과 관련해, " + text
        return text


class ActionContext(Contract):
    schema_version: Literal["action-context-0.1"] = "action-context-0.1"
    mode: Literal["development_preview"] = "development_preview"
    production_enabled: Literal[False] = False
    message: str
    request_snapshot: dict
    observations: dict[str, ObservationSlot]
    confirmed_candidates: dict = Field(default_factory=dict)
    pending_clarifications: dict[str, str]
    jev_summary: dict
    mapping_findings: list[dict]
    blockers: list[Question]
    kb_ask_slots: dict[str, str]
    forbidden_retrieve_slots: list[str]
    hold_signals: list[str]
    evidence: dict[str, dict]
    available_actions: list[ActionOffer]
    tools: dict[str, dict]
    history: list[dict] = Field(default_factory=list)
    design_defaults: dict = Field(default_factory=lambda: {
        "population": "adult", "data_kind": "synthetic",
        "note": "KB adapter design scope, not inferred user facts"})

    def enabled(self):
        return [offer for offer in self.available_actions if offer.enabled]


def build_action_context(request, features, reviewed, evaluated, pending, observations,
                         confirmed_candidates=None, history=None):
    from .agent import missing_information

    observations = {key: ObservationSlot.model_validate(slot) for key, slot in observations.items()}
    conflicts = {key for key, slot in observations.items() if slot.confirmed_by_user and slot.state == "conflicting"}
    answered = {key for key, slot in observations.items() if slot.confirmed_by_user and slot.state in
                ("known", "unknown", "declined", "not_applicable")}
    ask = {key: text for key, text in evaluated["ask_slots"].items()
           if key not in answered | conflicts and not key.startswith("product.")}
    blockers = missing_information(request)
    evidence = {}
    for row in evaluated["raw"]["results"]:
        evidence["kb:" + row["card_id"]] = {
            "kind": "inactive_kb_evaluation", "card_id": row["card_id"],
            "comparison_status": row.get("comparison_status"),
            "reason": row.get("reason"), "evidence": row.get("evidence", {})}
        for source in row.get("sources", []):
            evidence["source:" + source["id"]] = {"kind": "source_record", "record": source}
    for key, slot in observations.items():
        evidence["observation:" + key] = {"kind": "synthetic_session_observation", **slot.model_dump()}
    for key in pending:
        evidence["candidate:" + key] = {"kind": "unconfirmed_extraction", "target_id": key}
    for q in blockers:
        evidence["blocker:" + q.id] = {"kind": "structural_blocker", "target_id": q.id}

    # A generic unresolved signal does not prevent requesting conflict resolution.
    mandatory = [signal for signal in evaluated["hold_signals"] if signal != "unresolved_kb_comparison"]
    offers = []

    def add(action, target, text, refs=(), conditions=()):
        tool = {"ask_user": "request_user_input", "confirm_candidate": "request_user_input",
                "resolve_conflict": "request_user_input", "retrieve_evidence": "await_product_evidence",
                "hold": "hold_guidance", "request_draft": "generate_label_draft"}[action]
        offers.append(ActionOffer(action=action, target_id=target, tool=tool,
            reviewed_text=text, evidence_refs=list(refs), conditions=list(conditions),
            enabled=not mandatory or action == "hold", blocked_by=list(mandatory) if action != "hold" else []))

    for key in sorted(conflicts):
        if not key.startswith("product."):
            add("resolve_conflict", key, f"{key}에 서로 다른 정보가 있습니다. 현재 관찰을 확인하고 명시적으로 충돌을 해결해 주세요.",
                ["observation:" + key], ["explicit resolve_conflicts plus user-reviewed observation required"])
    for key, text in pending.items():
        add("confirm_candidate", key, text, ["candidate:" + key],
            ["request only; explicit subject, polarity and UTC observation time required"])
    for q in blockers:
        add("ask_user", q.id, q.text, ["blocker:" + q.id], ["request only; caller-reviewed profile/products required"])
    kb_refs = [key for key in evidence if key.startswith("kb:")]
    for key, text in ask.items():
        add("ask_user", key, text, kb_refs, ["consumer-observable slot; no answered/declined slot"])
    for key in evaluated["retrieve_slots"]:
        add("retrieve_evidence", key, "제품 근거 조회가 필요하여 초안을 보류합니다. 비공개 제형 정보는 미상으로 유지합니다.",
            kb_refs, ["request only; product retrieval is not implemented"])
    unresolved = [r["card_id"] for r in evaluated["raw"]["results"]
                  if r.get("comparison_status") in ("unknown", "conflicting", "exception")]
    blocked = list(mandatory) + list(pending) + [q.id for q in blockers] + sorted(conflicts)
    blocked += ["unresolved_candidate:" + key for key, value in (confirmed_candidates or {}).items()
                if value.get("state") in ("unknown", "declined") or value.get("subject") == "unknown"]
    blocked += list(ask) + list(evaluated["retrieve_slots"]) + unresolved
    add("request_draft", "label_draft", "합성 제품의 표시 사용법 기반 초안 생성을 요청합니다.", kb_refs,
        ["no holds, pending candidates, structural blockers, conflicts or unresolved KB comparisons"])
    draft = offers[-1]
    draft.enabled = not blocked
    draft.blocked_by = sorted(set(blocked))
    add("hold", "safety" if mandatory else "insufficient_information",
        "현재 개별 권고를 보류합니다. 심한 통증이나 불편은 전문가와 확인해 주세요." if mandatory else
        "정보가 충분하지 않거나 제공되지 않아 개별 권고를 보류합니다. 미상·거절 상태를 유지합니다.", kb_refs,
        ["no diagnosis, no automatic improvement judgment"])
    return ActionContext(message=request.message, request_snapshot=request.model_dump(),
        observations=observations, confirmed_candidates=confirmed_candidates or {},
        pending_clarifications=pending, jev_summary=features, mapping_findings=reviewed["findings"],
        blockers=blockers, kb_ask_slots=ask, forbidden_retrieve_slots=evaluated["retrieve_slots"],
        hold_signals=evaluated["hold_signals"], evidence=evidence, available_actions=offers,
        history=history or [], tools={
            "request_user_input": {"effect": "awaiting_user; never confirms facts"},
            "await_product_evidence": {"effect": "awaiting_product_evidence", "implemented": False},
            "hold_guidance": {"effect": "held; no recommendation execution"},
            "generate_label_draft": {"effect": "draft_generated; unsaved, requires approval"}})
