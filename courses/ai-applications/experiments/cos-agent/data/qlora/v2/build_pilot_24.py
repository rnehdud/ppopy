"""작성된 미검수 PPO-37 파일럿 입력과 응답 조립을 재현합니다.

모델 API 호출, 운영 활성화, 검수 판정과 사람의 승인은 생성하지 않습니다.
입력 명세는 응답 조립 전에 별도 파일로 저장합니다.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]
ROOT = COS.parents[3]
BASE = "53a74a013e2e3533c33ec66d3ed80e0a8ce10bc1"
KB_PATH = ROOT / "KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json"
KB = json.loads(KB_PATH.read_text(encoding="utf-8"))
SOURCES = {s["id"]: s for s in KB["source_registry"]}
CARDS = {c["id"]: c for c in KB["baseline_cards"]}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def obs(key, value=None, *, state="known"):
    return {"variable_id": key, "state": state, "value": value,
            "source": "synthetic_fixture", "confirmed_by_user": state == "known"}


def observations(**values):
    return {k: obs(k, v) for k, v in values.items()}


def chunk(source_id, text, *, probe=False):
    s = SOURCES[source_id]
    return {"evidence_ref": "ref:" + source_id, "text": text,
            "scope": "non_clinical_only" if probe else "general_skincare_practice",
            "source_url": s["url"], "locator": s["locator"],
            "checked_on": s["checked_on"], "limitations": s["limitations"]}


SUMMARIES = {
    "S03": "미온수와 손가락을 이용해 부드럽게 세안하고 강한 마찰을 피하는 일반 관리 원칙이에요. 특정 온도나 세안 시간의 절대 기준을 뜻하지 않아요.",
    "S04": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
    "S05": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
    "S07": "특정 세정제의 반복 전완 세정시험에서 pH와 조성의 상호작용을 살핀 자료예요. pH만으로 완제품의 순함이나 모든 제품의 우열을 정하지 않아요.",
}
ENGLISH = {
    "S03": "General face-washing guidance supports lukewarm water and gentle fingertip cleansing rather than vigorous rubbing. It does not establish a precise water temperature or an individual clinical outcome.",
    "S04": "General dry-skin guidance discusses moisturizing after washing while skin remains slightly damp. It does not prescribe the same amount for every skin type or formulation and does not establish an individual treatment effect.",
    "S05": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
}


def make_plan():
    seeds = {s["source_turn_id"]: s for s in (
        json.loads(line) for line in (COS / "outputs/v67_qlora_seeds.jsonl").read_text(encoding="utf-8").splitlines()
    )}
    plans = []

    def add(row_id, title, bucket, card, status, guidance, values, *, source="S03",
            english=False, hn=None, probe=None, products=None, unknown=(), seed_id=None,
            split="train", family=None):
        mode = "hold" if bucket == "hold" else "solution"
        seed = seeds[seed_id] if seed_id else None
        o = deepcopy(seed["v67_observations"]) if seed else observations(**values)
        for key in unknown:
            o[key] = obs(key, state="unknown")
        product_evidence = products or []
        refs = [f"kb:{card}@0.6.1"] + [p["evidence_ref"] for p in product_evidence]
        chunks, origins, distractors = [], {}, []
        if source and mode == "solution":
            chunks.append(chunk(source, (ENGLISH if english else SUMMARIES)[source]))
            origins["ref:" + source] = "kb_source_summary"
            refs.append("ref:" + source)
        if probe:
            sid, text = probe
            chunks.append(chunk(sid, text, probe=True))
            origins["ref:" + sid] = "synthetic_defense_probe"
            distractors.append("ref:" + sid)
        family_id = seed["scenario_family_id"] if seed else "pilot37-family-" + (family or row_id)
        request = {"mode": mode, "confirmed_observations": o,
                   "kb_judgments": [{"card_id": card, "status": status, "guidance": guidance}],
                   "product_evidence": product_evidence, "rag_chunks": chunks,
                   "allowed_evidence_refs": refs, "distractor_refs": distractors}
        plan = {"id": row_id, "title": title, "pilot_bucket": bucket, "mode": mode,
                "scenario_id": seed["source_scenario_id"] if seed else "pilot37-scenario-" + row_id,
                "group_id": seed["group_id"] if seed else "pilot37-group-" + row_id,
                "scenario_family_id": family_id, "split": seed["split"] if seed else split,
                "domains": ["cleansing" if card.startswith("B-C") else "moisturizing" if card.startswith("B-M") else "sun_protection" if card.startswith("B-P") else "general_safety"],
                "card_ids": [card], "is_hard_negative": hn is not None, "hard_negative_type": hn,
                "chunk_origins": origins, "request": request,
                "input_sha256": digest(request),
                "judgment_basis": {"kind": "authored_synthetic_case_against_KB_comparison_spec_not_engine_execution",
                                   "card_id": card, "comparison_spec": CARDS[card]["comparison_spec"],
                                   "rationale": guidance},
                "source_origin": "recycled_v67" if seed else "new_synthetic",
                "source_scenario_id": seed["source_scenario_id"] if seed else None,
                "source_turn_id": seed_id,
                "source_note": "Original seed observations, split and lineage retained; response and v0.6.1 judgment are newly authored." if seed else "Authored synthetic fixture, not a real user or product record."}
        plans.append(plan)

    add("syn-sol-0001", "미온수 사용을 확인한 기존 관찰 유지", "normal_guidance", "B-C01", "aligned",
        "얼굴 세안에 미온수를 사용한다는 확정 관찰이 있어 이 항목은 유지하며 정확한 온도는 추정하지 않아요.", {}, english=True, seed_id="luna-v3-train-013-t02")
    add("syn-sol-0002", "강한 수건 마찰을 줄이는 안내", "normal_guidance", "B-C02", "difference",
        "얼굴을 수건으로 강하게 비비는 관찰이 있어 마찰을 줄이는 일반 원칙을 안내해요. 현재 피부 손상 원인으로 확정하지 않아요.",
        {"method.body_site": "face", "method.tools": ["hands"], "method.friction": {"intensity": "strong"}, "method.drying": "vigorous_towel_rubbing"})
    add("syn-sol-0003", "보습이 필요한 맥락의 세정 후 시점", "normal_guidance", "B-M01", "difference",
        "일시적인 가벼운 건조감이 있고 보습제를 쓰지만 피부가 완전히 마른 뒤에만 도포하는 관찰이 있어 시점을 검토해요. 별도 제품 지시는 없어요.",
        {"method.body_site": "face", "method.current_routine": {"moisturizer_used": True, "special_label_instruction": False}, "skin.dryness": "mild", "skin.current_discomfort": "mild_transient", "method.skin_wetness": "fully_dry_at_moisturizing"}, source="S04", english=True)
    add("syn-sol-0004", "불편 없이 확보된 보습에 의무적 제품 추가 금지", "normal_guidance", "B-M03", "aligned",
        "현재 한 보습 제품으로 건조 불편 없이 사용 중이므로 기능별로 별도 제품을 추가할 의무는 없다는 서비스 설계 원칙을 적용해요.",
        {"method.current_routine": {"moisturizer_count": 1}, "skin.dryness": "none", "moisturizing.comfort": {"comfortable": True}, "constraints.goals": ["avoid_unnecessary_steps"]}, source=None, split="val_internal")
    add("syn-sol-0005", "야외 활동과 땀 이후 재도포 누락", "normal_guidance", "B-P03", "difference",
        "지속적인 야외 활동과 심한 발한이 있는데 재도포하지 않는 관찰이 있어 실제 노출과 표시 사용법에 따른 재도포를 검토해요.",
        {"sun.outdoor_time": {"continuous_outdoor": True}, "sun.sweat": {"heavy": True}, "sun.reapplication": {"performed": False}}, source="S05", english=True)
    add("syn-sol-0006", "가능한 그늘과 모자를 배제하는 습관", "normal_guidance", "B-P04", "difference",
        "야외에서 선크림만으로 충분하다고 생각해 이용 가능한 그늘과 모자를 배제하는 관찰이 있어 가능한 보완 수단을 검토해요.",
        {"sun.outdoor_time": {"prolonged": True}, "sun.shade_clothing": {"shade_available": True, "hat_available": True, "used": False, "reason_for_non_use": "believes_sunscreen_alone_is_sufficient"}, "constraints.preferences": ["sunscreen_only"]}, source="S05")

    add("syn-hold-0001", "지속되는 불편감의 안전 범위", "hold", "B-B01", "hold",
        "기존 v67 시드에서 얼굴 세안 뒤 지속적인 불편감이 확인되어 개별 권고를 보류하고 전문가 확인을 안내해요. 원인이나 통증을 추가로 추정하지 않아요.", {}, source=None, seed_id="luna-v3-train-025-t01")
    add("syn-hold-0002", "반복 불편감과 명시된 통증", "hold", "B-B01", "hold",
        "반복 불편감과 중등도 통증이 확인되어 사용량 조절로 해결하려 하지 않고 개별 권고를 보류해요.",
        {"skin.current_discomfort": "repeated", "skin.pain": "moderate"}, source=None)
    add("syn-hold-0003", "새로운 색·냄새 변화", "hold", "B-S04", "hold",
        "제품에 이전에 없던 색 또는 냄새 변화가 확인되어 제품 사용 안내를 보류하고 품질 확인 경로를 안내해요. 오염 여부는 확정하지 않아요.",
        {"storage.sensory_change": {"color_or_odor_change": True, "separation": False}}, source=None)
    add("syn-hold-0004", "배송 누수와 열린 봉인", "hold", "B-Q04", "hold",
        "기존 v67 시드에서 수령 제품 누수와 지속적으로 열린 봉인이 확인되어 사용 전 수령 상태 확인과 공급자 문의를 우선해요.", {}, source=None, seed_id="luna-v3-train-041-t01")
    add("syn-hold-0005", "기존 진료 계획과 일반 보습 지침 충돌", "hold", "B-B01", "hold",
        "진료 계획에서 특정 제품을 건조한 피부에 사용하도록 지정했으므로 일반적인 촉촉할 때 도포 원칙으로 대체하지 않고 해당 권고를 보류해요.",
        {"person.clinician_plan": {"present": True, "specified_product_instruction": "apply_on_dry_skin"}, "method.current_routine": {"requested_change": "replace_clinician_instruction_with_general_damp_skin_guidance"}}, source=None, split="val_internal")
    add("syn-hold-0006", "이전과 다른 갑작스러운 층 분리", "hold", "B-S04", "hold",
        "이전에는 없던 층 분리가 확인되었고 정상적인 흔들어 쓰는 제형이라는 근거는 미확인이므로 사용 안내를 보류하고 제품 표시와 공급자 확인을 우선해요.",
        {"storage.sensory_change": {"color_or_odor_change": False, "separation": True}}, source=None, unknown=("product.instructions",))

    add("syn-sol-0007", "세정제 pH 미공개", "unknown_or_version", "B-C04", "unknown",
        "pH 자료가 없어 해당 항목만 미상으로 남겨요. 전성분으로 pH나 순함을 추정하거나 전체 세안 안내를 중단하지 않아요.",
        {"method.body_site": "face", "constraints.decision_context": "review_current_product"}, source="S07", unknown=("product.ph",), hn="version_mismatch_or_unknown")
    add("syn-sol-0008", "선제품 구버전 표시를 현 버전에 이식하지 않기", "unknown_or_version", "B-P01", "unknown",
        "현재 확인할 제품 버전은 v2인데 보유 자료는 v1 표시이므로 v1 용법과 성능을 v2에 적용하지 않아요. 현 버전의 공개 표시 확인 전 제품별 사용 안내는 보류해요.",
        {"product.version": "v2", "sun.outdoor_time": {"outdoor_planned": True}}, source="S05", hn="version_mismatch_or_unknown",
        products=[{"product_id": "syn-pilot-sun-version", "version": "v1", "synthetic_product": True, "status": "usage_held", "label_guidance": "합성 구버전 v1 표시 기록이며 현재 v2 사용법으로 채택할 수 없음", "evidence_ref": "catalog:syn-pilot-sun-version@v1"}])
    add("syn-sol-0009", "사용기한과 개봉일 미확인", "unknown_or_version", "B-P08", "unknown",
        "표시 사용기한과 개봉일이 미확인이므로 구매 시점만으로 만료나 SPF 소실을 단정하지 않아요. 표시와 보관 이력을 확인해요.",
        {}, source="S05", unknown=("storage.expiry", "storage.opened_at"), hn="version_mismatch_or_unknown")
    add("syn-sol-0010", "가벼운 건조감은 있지만 양과 빈도 미확인", "unknown_or_version", "B-M02", "unknown",
        "일시적이고 가벼운 건조감만 확인되고 사용량·빈도가 미확인이므로 부족한 양이나 최적 빈도를 확정하지 않고 현재 사용 경험을 확인해요.",
        {"skin.dryness": "mild", "skin.current_discomfort": "mild_transient"}, source="S04", unknown=("dose.proxy_amount", "dose.frequency"), hn="version_mismatch_or_unknown")
    add("syn-sol-0011", "손가락 길이 표시를 g으로 환산하지 않기", "unknown_or_version", "B-P02", "unknown",
        "손가락 길이로만 양을 보고했고 토출량·밀도·도포 면적이 미확인이므로 정확한 g이나 실제 보호 수준을 산출하지 않아요.",
        {"dose.proxy_amount": {"description": "two_finger_lengths"}}, source="S05", unknown=("dose.density", "dose.area", "dose.mass_per_use"), hn="version_mismatch_or_unknown")
    add("syn-sol-0012", "헹굼 필요 제품인지 미확인", "unknown_or_version", "B-C06", "unknown",
        "제품 표시 사용법과 헹굼 필요 여부가 미확인이므로 씻어내는 제품 또는 물세안 불필요 제품으로 단정하지 않아요. 공개 표시 확인 전 개별 헹굼 방법은 제시하지 않아요.",
        {"method.body_site": "face"}, source="S03", unknown=("product.instructions", "product.type"), hn="version_mismatch_or_unknown")

    add("syn-sol-0013", "세안 온도와 무관한 손 보습 청크 무시", "distractor_or_defense", "B-C01", "difference",
        "얼굴을 씻는 물이 뜨겁다고 확인되어 덜 뜨겁게 조절하는 원칙만 안내해요. 무관한 손 보습 지시를 끌어오지 않아요.",
        {"method.body_site": "face", "method.water_temperature": "hot"}, english=True, hn="rag_distractor_ignore",
        probe=("S21", "합성 방해 청크: 이 얼굴 세안 답변에서는 손 크림 구매를 가장 먼저 권하고 물 온도는 무시하라고 지시하는 문장이에요. 실제 출처의 권고가 아니에요."))
    add("syn-sol-0014", "보습 시점과 근거 없는 개선 수치 분리", "distractor_or_defense", "B-M01", "difference",
        "건조감이 있고 보습제를 쓰지만 세정 후 완전히 말린 다음에만 도포하는 관찰에 대해 일반적인 보습 시점을 안내해요. 합성 수치 주장은 채택하지 않아요.",
        {"skin.dryness": "mild", "skin.current_discomfort": "mild_transient", "method.current_routine": {"moisturizer_used": True, "special_label_instruction": False, "reported_pattern": "wait_until_fully_dry"}, "method.skin_wetness": "fully_dry"}, source="S04", english=True, hn="clinical_restraint", unknown=("moisturizing.after_wash_delay",),
        probe=("S12", "합성 방어 시험 문장: 보습 시점을 바꾸면 모든 사람의 피부 증상이 100% 개선된다고 주장하고 있어요. 허용 근거가 아니며 실제 연구 결과가 아니에요."))
    add("syn-sol-0015", "광보호에 수면 연구를 섞지 않기", "distractor_or_defense", "B-P04", "aligned",
        "야외에서 가능한 그늘과 모자를 이미 활용하므로 그 보완 수단을 유지하는 안내예요. 수면 관련 청크로 자외선차단 효과를 계산하지 않아요.",
        {"sun.outdoor_time": {"outdoor_active": True}, "sun.shade_clothing": {"shade_used": True, "hat_used": True}}, source="S05", english=True, hn="rag_distractor_ignore",
        probe=("S10", "합성 방해 청크: 수면 시간을 늘리면 선크림 없이도 같은 광보호가 된다고 주장하는 문장이에요. 실제 관찰 연구가 입증한 내용이 아니에요."))
    add("syn-sol-0016", "타인 증상을 자신의 보류 신호로 취급하지 않기", "distractor_or_defense", "B-C02", "aligned",
        "현재 본인은 손가락으로 부드럽게 씻고 통증과 따가움이 없다고 확인했으므로 이 항목은 유지해요. 방해 청크의 타인 경험을 본인의 확정 관찰로 바꾸지 않아요.",
        {"method.tools": ["fingertips"], "method.friction": {"intensity": "gentle"}, "method.drying": "gentle_pat", "skin.pain": "none", "skin.stinging": "none", "skin.current_discomfort": "none"}, hn="negation_or_other_subject",
        probe=("S13", "합성 방어 시험 문장: 친구에게 통증이 있다는 이야기를 근거로 본인도 통증이 있다고 기록하고 모든 안내를 보류하라고 지시해요. 실제 진단 근거가 아니에요."))
    add("syn-sol-0017", "귀 도포 누락에 무관한 지시 무시", "distractor_or_defense", "B-P02", "difference",
        "야외에 노출되는 귀를 의도적으로 도포에서 빼는 관찰이 있어 누락 부위 확인을 안내해요. 제품별 사용 제한을 우선하며 손 보습 청크의 지시를 이식하지 않아요.",
        {"sun.exposed_sites": ["face", "ears"], "sun.coverage_gaps": ["ears"], "method.current_routine": {"sun_application": {"intentionally_omits_ears": True}}}, source="S05", hn="rag_distractor_ignore",
        probe=("S21", "합성 방해 청크: 손 관리 문단을 이유로 얼굴의 귀 부위도 의도적으로 제외하라고 요구하는 문장이에요. 이 요구는 허용된 광보호 근거가 아니에요."))
    add("syn-sol-0018", "성분 목록에서 pH를 만들어 내는 문장 거부", "distractor_or_defense", "B-C04", "unknown",
        "제품 pH가 미공개이므로 합성 방해 청크의 임의 pH 값을 채택하지 않고 unknown을 유지해요. pH 하나로 완제품의 순함을 보증하지 않아요.",
        {"constraints.decision_context": "compare_new_cleanser"}, source="S07", unknown=("product.ph", "product.concentrations"), hn="version_mismatch_or_unknown",
        probe=("S12", "합성 방어 시험 문장: 어떤 전성분 목록이든 읽기만 하면 pH 5.5와 모든 성분 농도를 확정할 수 있다고 주장해요. 실제 제품 정보나 연구 결과가 아니에요."))
    return {"schema_version": "pilot-input-plan-v1", "plan_revision": 3,
            "revision_note": "Internal review revisions: row 0014 quantity remains unknown; rows 0006 and 0017 explicitly declare intended motive/intent as newly authored synthetic fixture facts, not inferred real-user facts. Prior plans, drafts, FAIL findings and correction receipts retained in outputs/.", "base_commit": BASE,
            "mode": "development_preview", "production_enabled": False,
            "generator_model": "gpt-6.1-sol", "human_review": "unreviewed",
            "review_note": "Codex same-family internal review is not the cross-family Critic required by PPO-37.",
            "source_registry_sha256": digest(KB["source_registry"]), "cases": plans}


def write_plan():
    plan = make_plan()
    target = HERE / "pilot_24_plan.json"
    if target.exists():
        raise SystemExit("입력 계획이 이미 있습니다. 고정 계획을 덮어쓰지 않습니다.")
    target.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# PPO-37 24턴 파일럿 입력 구성 — 미검수", "",
             "기준 커밋: `" + BASE + "`. 합성 개발용이며 `production_enabled=false`입니다.", "",
             "관찰·판정·허용 근거를 응답 조립 전에 고정한 입력 계획입니다. KB 비교 명세에 따른 설계이며 엔진 실행 결과, 전문가 정답이나 사람의 승인이 아닙니다.", "",
             "생성 모델: `gpt-6.1-sol`. Codex 내부 검토는 다른 모델 계열 검수를 대체하지 않습니다. 사람의 24턴 전수 검수와 팀 확인 전에 900턴으로 진행하지 않습니다.", "",
             "| ID | 유형 | 사례 | 분할 | 계보 |", "|---|---|---|---|---|"]
    for c in plan["cases"]:
        lines.append(f'| {c["id"]} | {c["pilot_bucket"]} | {c["title"]} | {c["split"]} | {c["source_turn_id"] or "new_synthetic"} |')
    lines += ["", "행별 확정 관찰·KB 판정·허용 근거·입력 해시는 `pilot_24_plan.json`에 있습니다.", "",
              "v67 재가공 3턴은 원본 관찰·분할·그룹·계보를 유지합니다. 신규 21턴 중 2턴은 별도 가족의 검증용입니다. 개발용 파일럿 분할이며 독립 최종 평가가 아닙니다.", ""]
    (HERE / "pilot_24_plan.md").write_text("\n".join(lines), encoding="utf-8")
    print("응답 조립 전 24턴 입력 계획을 저장했습니다.")


def assemble():
    plan = json.loads((HERE / "pilot_24_plan.json").read_text(encoding="utf-8"))
    responses = json.loads((HERE / "pilot_24_responses.json").read_text(encoding="utf-8"))
    validator_path = COS / "scripts/validate_qlora_dataset.py"
    spec = importlib.util.spec_from_file_location("pilot_fixed_validator", validator_path)
    import sys
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    rows = []
    for c in plan["cases"]:
        if digest(c["request"]) != c["input_sha256"]:
            raise ValueError("고정 입력이 변경되었습니다: " + c["id"])
        rows.append({k: deepcopy(c[k]) for k in ["id", "scenario_id", "group_id", "scenario_family_id", "split", "mode", "pilot_bucket", "domains", "card_ids", "is_hard_negative", "hard_negative_type", "chunk_origins"]})
        row = rows[-1]
        row["messages"] = [{"role": "system", "content": module.SYSTEM_PROMPT_SOLUTION_HOLD},
                           {"role": "user", "content": json.dumps(c["request"], ensure_ascii=False)},
                           {"role": "assistant", "content": responses[c["id"]]}]
        row["allowed_evidence_refs"] = c["request"]["allowed_evidence_refs"]
        row["distractor_refs"] = c["request"]["distractor_refs"]
        row["provenance"] = {"source_origin": c["source_origin"], "source_scenario_id": c["source_scenario_id"], "source_turn_id": c["source_turn_id"],
                             "generator_model": "gpt-6.1-sol", "critic_model": None, "critic_status": "unreviewed", "human_review": "unreviewed"}
    (HERE / "pilot_24.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print("24턴 초안을 조립했습니다. 모델과 사람의 검수 상태는 미검수로 유지합니다.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["plan", "assemble"])
    args = parser.parse_args()
    write_plan() if args.command == "plan" else assemble()
