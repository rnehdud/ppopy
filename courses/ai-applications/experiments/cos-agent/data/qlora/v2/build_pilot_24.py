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
REMOVAL_PATH = ROOT / "KB/Poppy_KB_v0.6.1/sunscreen_removal_review.json"
REMOVAL = json.loads(REMOVAL_PATH.read_text(encoding="utf-8"))
CARDS["B-I01"] = {"comparison_spec": {
    "specification_language": "authored_case_checked_against_supplemental_condition_outcomes",
    "source_path": "KB/Poppy_KB_v0.6.1/sunscreen_removal_review.json",
    "source_version": REMOVAL["version"],
    "condition_outcomes": REMOVAL["condition_outcomes"],
}}


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
    "S08": "20명을 대상으로 시험한 자외선차단제와 세정 방법의 제거 결과를 비교한 연구예요. 결과는 시험한 제품과 방법의 조합에 한정돼요. 모든 내수성 제품에 같은 제거 방법이나 이중세안이 필요하다는 결론은 아니에요.",
    "S09": "제한된 보습제와 자외선차단제 조합에서 도포 순서를 UV 반사 영상으로 살핀 연구예요. 관찰된 영상 결과는 실제 SPF나 야외 보호 성능을 보증하지 않아요. 각각 층으로 바른 결과를 손바닥에서 미리 섞는 행동에 그대로 적용할 수는 없어요.",
    "S15": "화장품의 향료 등 알레르겐과 개인별 회피, 표시 및 제조사 지시 확인을 다루는 안내예요. 향료가 있다는 사실만으로 모든 사람에게 자극이나 알레르기가 생긴다고 단정하지 않아요. 미국 표시 설명을 한국의 법적 의무로 자동 전환하지 않아요.",
    "S16": "SPF 30 이상, UVA와 UVB 보호, 내수성과 야외 재도포를 다루는 전문기관 안내예요. 실제 노출과 물·땀, 비제품 보호수단도 함께 검토해요. 한국의 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙을 정하는 자료는 아니에요.",
    "S17": "자외선차단제 선택과 눈 주변 사용 시 흘러듦을 줄이는 방법을 다루는 안내예요. 눈 주변 스틱은 선택지 중 하나이며 모든 스틱의 무자극을 보장하지 않아요. 특정 필터의 우월성이나 개인의 눈시림 원인을 확정하는 자료도 아니에요.",
    "S18": "자외선차단제의 사용기한과 열 노출, 품질 변화 사례를 다루는 안내예요. 실제 제품의 표시와 보관 이력을 함께 확인해야 해요. 미국의 기한 규칙을 한국의 모든 제품에 적용하거나 정확한 SPF 감소율을 계산할 수는 없어요.",
    "S32": "레티놀이나 처방 레티노이드를 쓰는 동안 추가 각질관리를 겹치는 상황과 과도한 각질관리 회피를 다루는 안내예요. 실제 관리 목적과 사용 부위를 구분해 검토해야 해요. 모든 성분 조합의 절대 금기나 개인의 위해확률을 정하는 자료는 아니에요.",
    "S33": "특정 아다팔렌 0.3% 의약품의 환자 안내에서 AHA와 글리콜릭애씨드 제품 회피를 다뤄요. 이 주의는 해당 의약품 표시의 범위에서 읽어야 해요. 한국의 모든 레티노이드 화장품에 같은 법적 금기가 있다는 뜻은 아니에요.",
    "S34": "특정 트레티노인 의약품 표시에서 살리실릭애씨드 등 일반의약품 병용 시 국소 자극 증가 가능성을 다뤄요. 실제 제품 유형과 병용 맥락을 구분해야 해요. 이 주의만으로 처방을 중단하거나 용량을 바꾸는 절차를 만들지는 않아요.",
    "S35": "새 피부관리 제품을 작은 부위에서 확인하고 7~10일 관찰하는 일반 안내예요. 제품별 용법을 우선하며 모든 제품에 같은 빈도나 접촉시간을 적용하지 않아요. 이런 사용 확인은 의료기관의 진단용 패치테스트나 영구적인 안전 보증이 아니에요.",
    "S41": "물질이 눈에 들어간 경우 흐르는 물로 씻는 초기 대응을 다루는 안내예요. 원문은 일반적인 눈 노출 세척에 15~20분을 제시해요. 미국 응급전화번호를 국내 연락처로 옮기거나 일반 추천 엔진의 응급 진단 기능으로 확대하지 않아요.",
}
ENGLISH = {
    "S03": "General face-washing guidance supports lukewarm water and gentle fingertip cleansing rather than vigorous rubbing. It does not establish a precise water temperature or an individual clinical outcome.",
    "S04": "General dry-skin guidance discusses moisturizing after washing while skin remains slightly damp. It does not prescribe the same amount for every skin type or formulation and does not establish an individual treatment effect.",
    "S05": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
    "S15": "Cosmetic allergen guidance discusses fragrance and individual avoidance, labeling and manufacturer instructions. Fragrance presence alone does not establish irritation or allergy in every person. United States labeling explanations are not automatically Korean legal requirements.",
    "S16": "Professional sunscreen guidance discusses SPF 30 or higher, UVA and UVB coverage, water resistance and outdoor reapplication. Exposure conditions and non-product protection also matter. This is not a universal indoor reapplication schedule or a statement of Korean legal minimums.",
    "S34": "The labeling for a specific tretinoin medicine describes possible increased local irritation with salicylic-acid and other over-the-counter acne products. The caution is specific to the medicine and use context. It does not authorize stopping a prescription or changing its dose.",
}


def make_plan():
    seeds = {s["source_turn_id"]: s for s in (
        json.loads(line) for line in (COS / "outputs/v67_qlora_seeds.jsonl").read_text(encoding="utf-8").splitlines()
    )}
    plans = []

    def add(row_id, title, bucket, card, status, guidance, values, *, source="S03",
            english=False, hn=None, probe=None, products=None, unknown=(), seed_id=None,
            split="train", family=None, extra_sources=()):
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
        for extra_source in extra_sources:
            if mode != "solution":
                raise ValueError("보류 입력에는 문헌 청크를 추가하지 않습니다.")
            chunks.append(chunk(extra_source, SUMMARIES[extra_source]))
            origins["ref:" + extra_source] = "kb_source_summary"
            refs.append("ref:" + extra_source)
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
                "domains": ["cleansing" if card.startswith("B-C") else "moisturizing" if card.startswith("B-M") else "sun_protection" if card.startswith("B-P") else "cross_domain" if card.startswith("B-I") else "general_safety"],
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
    add("syn-sol-0002", "선크림 제거 표시와 실제 폼 세안을 대조", "normal_guidance", "B-I01", "aligned",
        "합성 제품의 일반 세안제 제거 표시와 실제 폼 세안이 일치해요. 별도 제거 지시가 없는 조건에서 표시된 세정 방법을 유지해요.",
        {"method.body_site": "face", "cleansing.steps": 1, "product.removal_claim": {"label_condition": "face_wash"}, "method.current_routine": {"cleansing_method": "foam"}}, source="S08",
        products=[{"product_id": "syn-pilot-sun-removal", "version": "v1", "synthetic_product": True, "status": "verified", "label_guidance": "합성 제품 표시 예시: 일반 세안제로 제거할 수 있어요. 별도 제거 방법은 지정하지 않아요.", "evidence_ref": "catalog:syn-pilot-sun-removal@v1"}])
    add("syn-sol-0003", "보습이 필요한 맥락의 세정 후 시점", "normal_guidance", "B-M01", "difference",
        "일시적인 가벼운 건조감이 있고 보습제를 쓰지만 피부가 완전히 마른 뒤에만 도포하는 관찰이 있어 시점을 검토해요. 별도 제품 지시는 없어요.",
        {"method.body_site": "face", "method.current_routine": {"moisturizer_used": True, "special_label_instruction": False}, "skin.dryness": "mild", "skin.current_discomfort": "mild_transient", "method.skin_wetness": "fully_dry_at_moisturizing"}, source="S04", english=True)
    add("syn-sol-0004", "보습제와 선크림을 각각 바르는 편안한 중첩", "normal_guidance", "B-I02", "aligned",
        "보습제와 선크림을 각각 층으로 바르고 불편하지 않으며 필요한 선크림 도포를 줄이지 않는다고 확인했어요. 현재 중첩 방법은 사용행동 항목에서 유지해요.",
        {"method.sequence": ["moisturizer", "sunscreen"], "method.mixing": {"premixed_in_palm": False}, "moisturizing.comfort": {"comfortable": True}, "method.current_routine": {"sunscreen_use_reduced_due_to_layering": False, "labeled_application_maintained": True}}, source="S09", split="val_internal")
    add("syn-sol-0005", "야외 활동과 땀 이후 재도포 누락", "normal_guidance", "B-P03", "difference",
        "지속적인 야외 활동과 심한 발한이 있는데 재도포하지 않는 관찰이 있어 실제 노출과 표시 사용법에 따른 재도포를 검토해요.",
        {"sun.outdoor_time": {"continuous_outdoor": True}, "sun.sweat": {"heavy": True}, "sun.reapplication": {"performed": False}}, source="S16", english=True)
    add("syn-sol-0006", "별도 레티놀과 AHA 화장품의 동일 부위 중첩", "normal_guidance", "B-G13", "difference",
        "각각 관리 목적으로 쓰는 별도 레티놀과 AHA 화장품을 같은 부위에 겹쳐 사용한다고 확인했어요. 불필요하게 추가한 중첩을 줄이는 보수적 서비스 기본값을 검토해요.",
        {"product.active_care_roles": {"products": [{"product_id": "syn-retinol", "role": "retinol_care"}, {"product_id": "syn-aha", "role": "aha_exfoliation"}]}, "product.combination_design": {"separate_products": True}, "product.medication_status": {"both_cosmetics": True}, "routine.co_use_context": {"same_body_site": True, "same_session": True, "aha_added_for_extra_exfoliation": True}, "skin.current_discomfort": "none", "person.clinician_plan": {"present": False}}, source="S32", extra_sources=("S33",))

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
        {"product.version": "v2", "sun.outdoor_time": {"outdoor_planned": True}}, source="S16", hn="version_mismatch_or_unknown",
        products=[{"product_id": "syn-pilot-sun-version", "version": "v1", "synthetic_product": True, "status": "usage_held", "label_guidance": "합성 구버전 v1 표시 기록이며 현재 v2 사용법으로 채택할 수 없음", "evidence_ref": "catalog:syn-pilot-sun-version@v1"}])
    add("syn-sol-0009", "사용기한과 개봉일 미확인", "unknown_or_version", "B-P08", "unknown",
        "표시 사용기한과 개봉일이 미확인이므로 구매 시점만으로 만료나 SPF 소실을 단정하지 않아요. 표시와 보관 이력을 확인해요.",
        {}, source="S18", unknown=("storage.expiry", "storage.opened_at"), hn="version_mismatch_or_unknown")
    add("syn-sol-0010", "처방 레티노이드와 살리실산 제품의 관리 목적 미확인", "unknown_or_version", "B-G14", "unknown",
        "레티노이드 제품이 처방약으로 분류된다는 정보와 다른 제품의 살리실릭애씨드 포함은 확인했지만 실제 사용 여부·관리 목적·병용 맥락은 미확인이에요. 같은 부위의 각질관리 중첩으로 확정하지 않고 제품 용도와 의료진 계획을 확인해요.",
        {"product.medication_status": {"retinoid_product": "prescription"}, "product.inci": ["salicylic_acid"], "method.current_routine": {"ingredient_list_refers_to": "second_product"}, "skin.current_discomfort": "none"}, source="S34", unknown=("product.active_care_roles", "routine.co_use_context", "person.clinician_plan"), hn="version_mismatch_or_unknown")
    add("syn-sol-0011", "새 제품의 국소 사용 확인 결과와 용법 미확인", "unknown_or_version", "B-G11", "unknown",
        "새 제품 도입 전 작은 부위 사용 확인 결과와 표시 용법이 미확인이에요. 확인하지 않은 반응을 무반응이나 영구적 안전으로 채우지 않고 제품별 지시와 기존 알레르기 정보를 확인해요.",
        {"skin.current_discomfort": "none", "method.current_routine": {"new_product_not_started": True}}, source="S35", unknown=("introduction.local_trial", "product.instructions", "person.known_allergies"), hn="version_mismatch_or_unknown")
    add("syn-sol-0012", "AHA와 BHA가 별도 제품인지 복합 완제품인지 미확인", "unknown_or_version", "B-G15", "unknown",
        "AHA와 BHA 관리 역할은 보고되었지만 별도 제품의 같은 부위 중첩인지 단일 복합 완제품인지는 미확인이에요. 제품 구성과 실제 병용 맥락을 확인하기 전 자동 금지나 자동 적합으로 판정하지 않아요.",
        {"product.active_care_roles": {"reported_roles": ["aha_exfoliation", "bha_exfoliation"]}, "skin.current_discomfort": "none"}, source="S32", unknown=("product.combination_design", "routine.co_use_context"), hn="version_mismatch_or_unknown")

    add("syn-sol-0013", "세안 온도와 무관한 손 보습 청크 무시", "distractor_or_defense", "B-C01", "difference",
        "얼굴을 씻는 물이 뜨겁다고 확인되어 덜 뜨겁게 조절하는 일반 세안 원칙을 안내해요.",
        {"method.body_site": "face", "method.water_temperature": "hot"}, english=True, hn="rag_distractor_ignore",
        probe=("S21", "손을 씻은 뒤에는 향료가 없는 핸드크림이나 연고형 보습제로 손의 건조함을 관리해요. 필요한 손 위생을 줄이라는 뜻은 아니에요."))
    add("syn-sol-0014", "처방 트레티노인과 추가 살리실산 각질관리의 경계", "distractor_or_defense", "B-G14", "unknown",
        "처방 트레티노인을 쓰는 부위에 별도 살리실릭애씨드 각질관리 화장품을 추가하려는 계획만 확인했어요. 실제 중첩 사용은 확인되지 않아 현재 판정은 미상으로 유지하고 제품 지시와 의료진 계획을 확인해요.",
        {"product.active_care_roles": {"retinoid_product": "tretinoin_prescription", "additional_product": "salicylic_acid_exfoliation"}, "product.combination_design": {"separate_products": True}, "product.medication_status": {"retinoid_product": "prescription", "additional_product": "cosmetic"}, "routine.co_use_context": {"same_body_site": True, "additional_cosmetic_planned": True}, "skin.current_discomfort": "none"}, source="S34", english=True, extra_sources=("S32",), hn="clinical_restraint", unknown=("person.clinician_plan",),
        probe=("S12", "두 관리 제품을 함께 쓰면 모든 사람의 피부 문제가 100% 개선돼요. 더 자주 겹쳐 사용할수록 결과도 좋아져요."))
    add("syn-sol-0015", "새 향료 포함 후보와 개인 알레르기 판단의 구분", "distractor_or_defense", "B-G01", "difference",
        "새로 비교하는 합성 제품에 향료가 포함된다고 확인했어요. 무향료를 우선 비교하는 서비스 선호와의 차이를 설명하되 개인의 알레르기나 현재 위해를 확정하지 않아요.",
        {"product.fragrance": {"present": True}, "constraints.decision_context": "compare_new_product", "skin.current_discomfort": "none"}, source="S15", english=True, hn="rag_distractor_ignore", unknown=("person.known_allergies",),
        products=[{"product_id": "syn-pilot-fragrance", "version": "v1", "synthetic_product": True, "status": "verified", "label_guidance": "합성 제품 표시 예시: 향료 포함", "evidence_ref": "catalog:syn-pilot-fragrance@v1"}],
        probe=("S10", "수면의 질이 다른 집단에서 피부 노화 지표와 장벽 회복을 비교한 관찰 연구를 다뤄요. 집단의 연관성이 개인의 개선량을 바로 정해 주지는 않아요."))
    add("syn-sol-0016", "눈 노출 부정과 응급 세척 정보의 적용 범위", "distractor_or_defense", "B-P06", "aligned",
        "제품이 눈에 들어가지 않았고 반복 눈시림이나 통증도 없으며 눈 주변 비제품 광보호를 유지한다고 확인했어요. 현재 눈 주변 사용 조건은 이 항목의 기본 상태와 맞아요.",
        {"skin.eye_symptom_context": {"current_eye_exposure": False}, "skin.eye_stinging": {"repeated": False}, "skin.pain": "none", "skin.current_discomfort": "none", "sun.periocular_application": {"avoids_eye_contact": True}, "sun.shade_clothing": {"sunglasses_used": True}}, source="S17", hn="negation_or_other_subject",
        probe=("S41", SUMMARIES["S41"]))
    add("syn-sol-0017", "귀 도포 누락에 무관한 지시 무시", "distractor_or_defense", "B-P02", "difference",
        "야외에 노출되는 귀를 의도적으로 도포에서 빼는 관찰이 있어 누락 부위 확인을 안내해요. 제품별 사용 제한을 우선 확인해요.",
        {"sun.exposed_sites": ["face", "ears"], "sun.coverage_gaps": ["ears"], "method.current_routine": {"sun_application": {"intentionally_omits_ears": True}}}, source="S05", hn="rag_distractor_ignore",
        probe=("S21", "손을 씻은 뒤에는 향료가 없는 핸드크림이나 연고형 보습제로 손의 건조함을 관리해요. 필요한 손 위생을 줄이라는 뜻은 아니에요."))
    add("syn-sol-0018", "성분 목록에서 pH를 만들어 내는 문장 거부", "distractor_or_defense", "B-C04", "unknown",
        "제품 pH와 성분 농도가 미공개이므로 해당 값은 미상으로 유지해요. pH 하나로 완제품의 순함을 보증하지 않아요.",
        {"constraints.decision_context": "compare_new_cleanser"}, source="S07", unknown=("product.ph", "product.concentrations"), hn="version_mismatch_or_unknown",
        probe=("S12", "전성분 목록만 확인하면 제품의 pH는 5.5라고 확정할 수 있어요. 각 성분의 농도도 목록만으로 계산할 수 있어요."))
    return {"schema_version": "pilot-input-plan-v1", "plan_revision": 5,
            "revision_note": "개정 5: 출처와 카드의 다양성을 넓히고 한국어 청크를 2~4문장 설명체로 정리했습니다. B-I01 및 활성성분 중첩을 포함하며 S41은 눈 노출 부정 상황의 방해 근거로만 사용합니다. 변경 행은 새 내용 해시로 재검수해야 합니다.", "base_commit": BASE,
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
