"""Thin terminal CLI wrapper around pure-Python AgentRuntime."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from uuid import uuid4
import warnings
from zipfile import BadZipFile

from .catalog_adapter import AuroraCatalogAdapter, SyntheticCatalogAdapter
from .contracts import ObservationSlot, OwnedProduct, Profile
from .nlp_layer import (
    NLPLayer,
    interpret_candidate_confirmation,
    interpret_slot_answer,
    load_jev_api_key,
)
from .runtime import AgentRuntime, RoutedAFAPolicy
from .runtime_contracts import CandidateConfirmationInput, RuntimeTurnRequest, RuntimeTurnResponse


def _demo_cleanser() -> OwnedProduct:
    return OwnedProduct(product_id="synthetic-cleanser-a", version="1.0.0", confirmed=True)


def _make_observation(variable_id: str, raw_value: str) -> ObservationSlot:
    cleaned = raw_value.strip()
    if cleaned in ("unknown", "declined", "not_applicable"):
        return ObservationSlot(
            variable_id=variable_id,
            state=cleaned,
            value=None,
            source="user_report",
            confirmed_by_user=True,
        )
    return ObservationSlot(
        variable_id=variable_id,
        state="known",
        value=cleaned,
        source="user_report",
        confirmed_by_user=True,
    )


def format_response(resp: RuntimeTurnResponse) -> str:
    lines = [f"[상태: {resp.status}] (실행: {', '.join(resp.executed_actions) or 'none'})"]
    if resp.nlp and resp.nlp.product_queries:
        names = ", ".join(p.text for p in resp.nlp.product_queries)
        lines.append(f"  - NLP 제품 후보({resp.nlp.source_mode}): {names}")
    query_hits = [
        f"{res.query_key}={res.status}({res.source})"
        for key, res in resp.tool_results.items()
        if key.startswith("product_query:")
    ]
    if query_hits:
        lines.append(f"  - 카탈로그 검색 결과: {', '.join(query_hits)}")
    if resp.nlp and resp.nlp.feature_candidates:
        feats = ", ".join(f"{f.slot_id}={f.value}" for f in resp.nlp.feature_candidates)
        lines.append(f"  - NLP 반영된 상태 후보: {feats}")
    if resp.nlp and resp.nlp.symptom_candidates:
        syms = ", ".join(f"{s.label}({s.state})" for s in resp.nlp.symptom_candidates)
        lines.append(f"  - NLP 증상 후보(미확정): {syms}")
    if resp.questions:
        for q in resp.questions:
            lines.append(f"  ? 질문 [{q.id}]: {q.text}")
    if resp.hold_reason:
        lines.append(f"  ! 보류: {resp.hold_reason}")
    if resp.recommendation:
        rec = resp.recommendation
        if rec.lifestyle_adjustments:
            lines.append("  [생활습관 / 사용법 안내]")
            for item in rec.lifestyle_adjustments:
                lines.append(f"    - ({item.title}) {item.guidance}")
        if rec.owned_product_usage:
            lines.append("  [보유 제품 활용]")
            for item in rec.owned_product_usage:
                lines.append(f"    - {item.title}: {item.guidance}")
        if rec.exclusions_or_holds:
            lines.append("  [제외 / 보류 제품]")
            for ex in rec.exclusions_or_holds:
                lines.append(f"    - {ex.product_id} ({ex.disposition}): {ex.reason}")
        if rec.alternatives:
            lines.append("  [대체 제품 후보]")
            for alt in rec.alternatives:
                lines.append(f"    - {alt.title}: {alt.guidance}")
    return "\n".join(lines)


def build_runtime(ppo_model_path: Path | None = None, *, use_remote_jev: bool = True) -> AgentRuntime:
    ppo_policy = None
    if ppo_model_path is not None:
        from .afa.policy_adapter import PPOAFAPolicy

        try:
            ppo_policy = PPOAFAPolicy(ppo_model_path)
        except (ImportError, OSError, ValueError, RuntimeError, BadZipFile, EOFError) as error:
            warnings.warn(
                f"PPO checkpoint unavailable ({type(error).__name__}); using rule-based AFA.",
                RuntimeWarning,
                stacklevel=2,
            )
    aurora = AuroraCatalogAdapter()
    catalog = aurora if aurora.is_configured() else SyntheticCatalogAdapter()
    nlp = NLPLayer(use_remote_jev=use_remote_jev and load_jev_api_key() is not None)
    return AgentRuntime(
        nlp_layer=nlp,
        afa_policy=RoutedAFAPolicy(ppo_policy=ppo_policy),
        catalog_adapter=catalog,
        auto_apply_nlp_features=True,
    )


def run_scripted_demo(runtime: AgentRuntime) -> None:
    req_id = f"demo-{uuid4().hex[:8]}"
    first = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id=req_id,
            message="오늘 야외에 오래 있는데 어제 쓴 세안제 루틴 확인해 주세요.",
            profile=Profile(confirmed=True),
            products=[
                _demo_cleanser(),
                OwnedProduct(product_id="synthetic-sunscreen-b", version="unknown", confirmed=False),
            ],
            observations={
                "method.body_site": ObservationSlot(
                    variable_id="method.body_site",
                    state="known",
                    value="face",
                    source="synthetic_fixture",
                    confirmed_by_user=True,
                ),
            },
        )
    )
    print("--- Turn 1 ---")
    print(format_response(first))

    answers = {
        "method.water_temperature": "lukewarm",
        "method.tools": "hands",
        "method.friction": "gentle",
        "method.drying": "pat_gently",
    }
    resp = first
    turn = 2
    while resp.status == "awaiting_user" and resp.questions and turn <= 6:
        qid = resp.questions[0].id
        val = answers.get(qid, "unknown")
        resp = runtime.handle_turn(
            RuntimeTurnRequest(
                request_id=req_id,
                observations={qid: _make_observation(qid, val)},
            )
        )
        print(f"\n--- Turn {turn} (답변: {qid}={val}) ---")
        print(format_response(resp))
        turn += 1


def run_interactive(runtime: AgentRuntime) -> None:
    req_id = f"cli-{uuid4().hex[:8]}"
    last_question_id: str | None = None
    first_turn = True
    print("Ppopy 로컬 통합 CLI (합성 개발 프리뷰 · 무저장)")
    print("명령어: /state (현재 세션 상태), /quit (종료), 또는 질문에 대한 값 입력 (예: face, hands, lukewarm, unknown)")
    while True:
        raw = input("\n나 > ").strip()
        if not raw:
            continue
        if raw == "/quit":
            return
        if raw == "/state":
            state = runtime.get_session(req_id)
            print(state.model_dump_json(indent=2) if state else "{}")
            continue

        observations: dict[str, ObservationSlot] = {}
        confirmations: dict[str, CandidateConfirmationInput] = {}
        message = raw
        if "=" in raw and "." in raw.split("=", 1)[0]:
            key, val = raw.split("=", 1)
            observations[key.strip()] = _make_observation(key.strip(), val.strip())
            message = ""
        elif last_question_id and not first_turn and last_question_id.startswith("clarify:"):
            conf = interpret_candidate_confirmation(
                raw,
                api_key=runtime.nlp_layer.api_key,
            )
            if conf is None:
                print("\n에이전트 > 본인 경험 여부와 최근/지속 여부를 조금 더 명확히 답해 주세요 (예: 네 어제부터 계속 그래요 / 아니요).")
                continue
            confirmations[last_question_id] = conf
            message = ""
        elif last_question_id and not first_turn:
            mapped = interpret_slot_answer(
                last_question_id,
                raw,
                api_key=runtime.nlp_layer.api_key,
            )
            if mapped is None:
                print(f"\n에이전트 > 답변을 '{last_question_id}' 값으로 이해하지 못했습니다. 조금 더 명확히 답해 주세요 (또는 모름/거절).")
                continue
            state_kind, mapped_val = mapped
            observations[last_question_id] = ObservationSlot(
                variable_id=last_question_id,
                state=state_kind,
                value=mapped_val,
                source="user_report",
                confirmed_by_user=True,
            )
            # Clear raw message so a reply to e.g. method.drying ("수건으로...")
            # is not re-interpreted by upfront extraction as method.tools=washcloth.
            message = ""

        req = RuntimeTurnRequest(
            request_id=req_id,
            message=message,
            profile=Profile(confirmed=True) if first_turn else None,
            products=[_demo_cleanser()] if first_turn else None,
            observations=observations,
            confirmations=confirmations,
        )
        first_turn = False
        resp = runtime.handle_turn(req)
        print("\n에이전트 >")
        print(format_response(resp))
        last_question_id = resp.questions[0].id if resp.questions else None
        if resp.status in ("completed", "held"):
            print("\n[요청이 종료되었습니다. 새 요청을 시작하려면 /quit 후 다시 실행하거나 새 발화를 입력하세요.]")
            req_id = f"cli-{uuid4().hex[:8]}"
            first_turn = True
            last_question_id = None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true", help="Run a fixed 2-turn synthetic demo.")
    parser.add_argument("--ppo-model", type=Path, default=None, help="Optional trained B-C02 PPO .zip path.")
    parser.add_argument("--offline-nlp", action="store_true", help="Force offline Kiwi NLP fallback.")
    args = parser.parse_args()
    runtime = build_runtime(args.ppo_model, use_remote_jev=not args.offline_nlp)
    if args.scripted:
        run_scripted_demo(runtime)
    else:
        run_interactive(runtime)


if __name__ == "__main__":
    main()
