"""Thin terminal CLI wrapper around pure-Python AgentRuntime."""
from __future__ import annotations

import argparse
from pathlib import Path
from uuid import uuid4
import warnings
from zipfile import BadZipFile

from .afa.question_priority import MyopicVOIAFAPolicy
from .catalog_adapter import AuroraCatalogAdapter, SyntheticCatalogAdapter
from .contracts import ObservationSlot, OwnedProduct, Profile
from .nlp_layer import NLPLayer, load_jev_api_key
from .runtime import AgentRuntime, RoutedAFAPolicy
from .runtime_contracts import (
    ChoiceSelection, ProductEvidenceSelection, RuntimeQuestion, RuntimeTurnRequest, RuntimeTurnResponse,
)


EVIDENCE_CHOICES = (
    ("product.instructions", "표시 사용법"),
    ("product.spf", "SPF 표시"),
    ("product.uva", "UVA 표시"),
)


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
            lines.extend(f"    {number}. {choice.label}" for number, choice in enumerate(q.choices, 1))
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
        afa_policy=(
            MyopicVOIAFAPolicy() if ppo_model_path is None else RoutedAFAPolicy(ppo_policy=ppo_policy)
        ),
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
    pending: RuntimeQuestion | None = None
    print("Ppopy 로컬 통합 CLI (합성 개발 프리뷰 · 무저장)")
    if isinstance(runtime.afa_policy, MyopicVOIAFAPolicy):
        print("질문 정책: Myopic VOI")
    print("첫 요청은 문장으로 입력하고, 후속 질문에는 선택지 번호를 입력하세요. /state (세션 상태), /quit (종료)")
    print("/evidence (보유 제품의 표시 자료 조회)")
    while True:
        try:
            raw = input("\n선택 번호 > " if pending else "\n나 > ").strip()
        except EOFError:
            return
        if not raw:
            continue
        if raw == "/quit":
            return
        if raw == "/state":
            state = runtime.get_session(req_id)
            print(state.model_dump_json(indent=2) if state else "{}")
            continue
        if raw == "/evidence":
            state = runtime.get_session(req_id)
            choices = [
                (product, target, label)
                for product in (state.products if state else [_demo_cleanser()]) if product.confirmed
                for target, label in EVIDENCE_CHOICES
            ]
            if not choices:
                print("먼저 보유 제품과 버전을 확인해 주세요.")
                continue
            for number, (product, _, label) in enumerate(choices, 1):
                print(f"{number}. {product.product_id} ({product.version}) — {label}")
            try:
                selected = input("제품·항목 번호 (0: 취소) > ").strip()
            except EOFError:
                return
            allowed = {str(number): choice for number, choice in enumerate(choices, 1)}
            if selected not in allowed:
                print("표시 자료 조회를 실행하지 않았습니다.")
                continue
            if state is None:
                initial = runtime.handle_turn(RuntimeTurnRequest(
                    request_id=req_id, profile=Profile(confirmed=True), products=[_demo_cleanser()],
                ))
                pending = initial.questions[0] if initial.questions else None
            product, target, _ = allowed[selected]
            resp = runtime.handle_turn(RuntimeTurnRequest(
                request_id=req_id,
                product_evidence_selection=ProductEvidenceSelection(
                    product_id=product.product_id, version=product.version, target_id=target,
                ),
            ))
            evidence = resp.product_evidence
            if evidence.status == "found":
                print(f"{evidence.label_text}\n출처: {evidence.evidence_ref}")
            else:
                print(f"이 제품 버전의 표시 자료를 확인하지 못했습니다. ({evidence.reason})")
            if pending:
                print(f"이전 질문 [{pending.id}]: {pending.text}")
                for number, option in enumerate(pending.choices, 1):
                    print(f"{number}. {option.label}")
            continue

        if pending is not None:
            choices = {str(number): choice.id for number, choice in enumerate(pending.choices, 1)}
            if raw not in choices:
                print(f"화면에 나온 선택지 번호(1~{len(choices)})를 입력하세요.")
                continue
            req = RuntimeTurnRequest(
                request_id=req_id,
                choice_selection=ChoiceSelection(
                    turn_index=pending.turn_index, question_id=pending.id, choice_id=choices[raw],
                ),
            )
        else:
            req = RuntimeTurnRequest(
                request_id=req_id, message=raw, profile=Profile(confirmed=True), products=[_demo_cleanser()],
            )
        resp = runtime.handle_turn(req)
        print("\n에이전트 >")
        print(format_response(resp))
        pending = resp.questions[0] if resp.questions else None
        if resp.status in ("completed", "held"):
            print("\n[요청이 종료되었습니다. 새 요청을 시작하려면 /quit 후 다시 실행하거나 새 발화를 입력하세요.]")
            req_id = f"cli-{uuid4().hex[:8]}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true", help="Run a fixed 2-turn synthetic demo.")
    parser.add_argument("--ppo-model", type=Path, default=None,
                        help="Use a trained B-C02 PPO .zip for comparison (default: Myopic VOI).")
    parser.add_argument("--offline-nlp", action="store_true", help="Force offline Kiwi NLP fallback.")
    args = parser.parse_args()
    runtime = build_runtime(args.ppo_model, use_remote_jev=not args.offline_nlp)
    if args.scripted:
        run_scripted_demo(runtime)
    else:
        run_interactive(runtime)


if __name__ == "__main__":
    main()
