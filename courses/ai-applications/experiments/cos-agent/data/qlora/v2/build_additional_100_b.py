"""B 최초 초안의 작성 이력입니다. 입력·응답 동시 설계 후 응답을 따로 재작성했어요."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import build_pilot_24 as base

HERE = Path(__file__).resolve().parent
if (HERE / "additional_100.jsonl").exists():
    raise SystemExit("최초 작성 이력은 최종 자료를 덮어쓰지 않아요. build_additional_100.py로 고정 자료만 조립하세요.")
CASES = []
TEXT = {
    **base.SUMMARIES,
    "S14": "햇빛 노출에서 그늘과 의복, 선글라스와 제품 표시를 함께 검토하는 안내예요. 특정 약물의 중단이나 개인별 자외선 손상량을 계산하는 자료는 아니에요.",
}
EN = {**base.ENGLISH,
      "S08": "A small imaging study compared removal of selected sunscreen formulations using water, facial cleanser and cleansing oil. Findings are limited to the tested product-method combinations and do not establish mandatory double cleansing for all water-resistant sunscreens.",
      "S09": "A limited moisturizer and sunscreen layering study used ultraviolet-reflectance imaging. It does not establish real-world SPF equivalence, and sequential layering is not the same as premixing products in the palm.",
      "S17": "Sunscreen guidance considers product choice and avoiding runoff near the eyes. Sticks are one possible option, not a guarantee of no irritation for every person, and the guidance does not identify an individual's cause of eye symptoms."}


def add(n, title, card, status, values, guidance, next_step, limit, *, source="S05", unknown=(), products=(), hn=None, probe=None, hold=False):
    row_id = f"syn-{'hold' if hold else 'sol'}-{n:04d}"
    bucket = "hold" if hold else "normal_guidance" if n < 72 else "unknown_or_version" if n < 80 else "distractor_or_defense"
    english = not hold and n in {63,65,66,68,70,72,74,79,83}
    refs = [f"kb:{card}@0.6.1"] + [p["evidence_ref"] for p in products]
    observations = base.observations(**values)
    for key in unknown:
        observations[key] = base.obs(key, state="unknown")
    chunks, origins, distractors = [], {}, []
    if not hold:
        chunks.append(base.chunk(source, (EN if english else TEXT)[source]))
        refs.append("ref:" + source)
        origins["ref:" + source] = "kb_source_summary"
    if probe:
        sid, text = probe
        chunks.append(base.chunk(sid, text, probe=True))
        origins["ref:" + sid] = "synthetic_defense_probe"
        distractors.append("ref:" + sid)
    request = {"mode": "hold" if hold else "solution", "confirmed_observations": observations,
               "kb_judgments": [{"card_id": card, "status": status, "guidance": guidance}],
               "product_evidence": list(products), "rag_chunks": chunks,
               "allowed_evidence_refs": refs, "distractor_refs": distractors}
    families = {63:"feasible-nonproduct-protection",71:"feasible-nonproduct-protection",87:"feasible-nonproduct-protection",
                64:"actual-application-versus-reported-other",81:"actual-application-versus-reported-other",88:"actual-application-versus-reported-other",
                65:"reapplication-context",73:"reapplication-context",85:"reapplication-context",
                66:"basic-label-selection",72:"basic-label-selection",86:"basic-label-selection",
                67:"expiry-history-quality",76:"expiry-history-quality",83:"expiry-history-quality",
                68:"removal-label-conditions",74:"removal-label-conditions",84:"removal-label-conditions",
                69:"layering-versus-behavior",78:"layering-versus-behavior",82:"layering-versus-behavior",
                79:"personal-eye-experience",80:"personal-eye-experience"}
    family = families.get(n, row_id) if not hold else row_id
    case = {"id": row_id, "title": title, "pilot_bucket": bucket, "mode": request["mode"],
            "scenario_id": "add100-b-scenario-" + row_id,
            "group_id": "add100-b-group-" + family,
            "scenario_family_id": "add100-b-family-" + family,
            "split": "val_internal" if not hold and n in {70,75,77} else "train",
            "domains": ["sun_protection"] if card.startswith("B-P") else ["cross_domain"] if card.startswith("B-I") else ["general_safety"],
            "card_ids": [card], "is_hard_negative": hn is not None, "hard_negative_type": hn,
            "chunk_origins": origins, "request": request, "input_sha256": base.digest(request),
            "judgment_basis": {"kind": "authored_synthetic_case_against_KB_comparison_spec_not_engine_execution",
                               "card_id": card, "comparison_spec": deepcopy(base.CARDS[card]["comparison_spec"]), "rationale": guidance},
            "source_origin": "new_synthetic", "source_scenario_id": None, "source_turn_id": None,
            "source_note": "새 합성 개발 사례이며 실제 사용자나 제품 기록, 엔진 실행 결과가 아니에요."}
    CASES.append((case, next_step, limit, source))


def product(n, label, version="v1", status="verified"):
    pid = f"syn-add100-b-{n}"
    return {"product_id": pid, "version": version, "synthetic_product": True, "status": status,
            "label_guidance": "합성 제품 표시 예시: " + label, "evidence_ref": f"catalog:{pid}@{version}"}


def define():
    add(63,"그늘을 배제한 장시간 경기 관람", "B-P04","difference",
        {"sun.outdoor_time":{"prolonged":True,"context":"야외 경기 관람"},"sun.shade_clothing":{"shade_available":True,"shade_used":False,"reason":"선크림만으로 충분하다고 생각함"}},
        "장시간 야외 관람 중 이용 가능한 그늘을 선크림만으로 충분하다는 이유로 배제하고 있어요.",
        "선크림 사용을 유지하면서 이용 가능한 그늘을 함께 활용해요.","그늘과 선크림을 함께 써도 개인의 실제 자외선 노출량이나 보호율을 계산할 수는 없어요.")
    add(64,"야외 출퇴근에서 목 뒤 도포 누락", "B-P02","difference",
        {"sun.exposed_sites":["face","back_of_neck"],"sun.coverage_gaps":["back_of_neck"],"method.current_routine":{"intentional_neck_omission":True,"reason":"옷깃에 묻는 것이 싫음"}},
        "야외 출퇴근 때 노출되는 목 뒤를 옷깃에 묻는다는 이유로 의도적으로 빼고 있어요.",
        "노출되는 목 뒤도 제품 지침에 맞게 도포하고 의복으로 가릴 수 있는 방법을 함께 검토해요.","목의 면적과 제품 토출량은 확인되지 않아 정확한 g 수치를 제시하지 않아요.")
    add(65,"수영 후 수건 접촉을 반영한 재도포", "B-P03","aligned",
        {"sun.water_contact":True,"sun.towel_contact":True,"sun.outdoor_time":{"continues_after_swimming":True},"sun.reapplication":{"after_swim_and_towel":True,"follows_label":True}},
        "수영 후 수건으로 닦고 야외 노출이 이어지는 상황에서 표시대로 다시 바르고 있어요.",
        "수영과 수건 접촉 이후 제품 표시를 따르는 재도포 행동을 유지해요.","재도포했다는 보고만으로 물속이나 이후의 실제 SPF를 인증하지 않아요.")
    add(66,"야외용 새 후보의 기본 표시 확인", "B-P01","aligned",
        {"constraints.decision_context":"compare_new_outdoor_sunscreen","product.spf":50,"product.uva":{"broad_spectrum_uva_uvb":True},"product.water_resistance":{"labeled":True},"sun.outdoor_time":{"planned_outdoor_activity":True}},
        "새 야외용 합성 후보에서 SPF 50, UVA·UVB 보호와 내수성 표시가 확인되어 기본 표시 조건에 맞아요.",
        "확인된 기본 표시를 갖춘 후보로 검토하되 제품 지침과 실제 사용 적합성을 함께 살펴요.","기본 표시 조건 충족은 개인에게 무자극이거나 모든 상황에서 충분하다는 보증이 아니에요.",source="S16",products=[product(66,"SPF 50, UVA·UVB 광범위 보호, 내수성 표시가 있어요.")])
    add(67,"기한이 지났지만 외관이 같은 보유 선크림", "B-P08","difference",
        {"storage.expiry":{"label_expired":True},"storage.sensory_change":{"color_or_odor_change":False,"separation":False},"method.current_routine":{"continues_relying_on_expired_sunscreen":True}},
        "표시 기한이 지난 것이 확인되어 외관 변화가 없더라도 계속 광보호를 맡기는 사용은 조정 대상이에요.",
        "기한이 지난 제품에 계속 의존하지 않고 기한을 확인할 수 있는 제품으로 대체하는 방향을 검토해요.","기한 경과만으로 남아 있는 SPF나 분해물 농도를 계산하지 않아요.",source="S18")
    add(68,"오일 제거 지시와 실제 폼 단독 사용", "B-I01","difference",
        {"product.removal_claim":{"label_condition":"oil_required"},"method.current_routine":{"cleansing_method":"foam"},"cleansing.steps":1,"method.body_site":"face"},
        "현재 버전의 합성 선크림은 오일 제거를 지정하지만 실제로는 폼 세안만 하고 있어요.",
        "해당 합성 제품에 확인된 오일 제거 지시를 따르는 방법으로 검토해요. 추가 폼 세안까지 의무라고 덧붙이지 않아요.","한 제품의 제거 표시는 모든 내수성 선크림이나 세정제 조합에 일반화할 수 없어요.",source="S08",products=[product(68,"제거할 때 클렌징 오일을 사용해요. 추가 폼 세안은 별도로 지정하지 않아요.")])
    add(69,"밀림은 있지만 선크림 사용을 줄이지 않음", "B-I02","exception",
        {"sun.pilling":{"present":True},"method.mixing":{"premixed_in_palm":False},"method.sequence":["moisturizer","sunscreen"],"method.current_routine":{"sunscreen_use_reduced_due_to_layering":False,"reapplication_omitted_due_to_layering":False},"skin.current_discomfort":"none"},
        "밀림은 있지만 필요한 선크림 도포와 재도포를 줄이지 않아 행동 감소 차이로 확정하지 않고 사용성을 검토해요.",
        "필요한 선크림 사용은 유지하고 밀림 때문에 부담이 되는 조합과 도포 방법을 제품 지침 안에서 살펴요.","밀림만으로 실제 차단 성능 저하나 특정 감소율을 추정하지 않아요.",source="S09")
    add(70,"비가스 분무형을 얼굴에 직접 뿌리는 사용", "B-P09","difference",
        {"product.application_form":"non_gas_spray","method.body_site":"face","method.current_routine":{"direct_spray_to_face":True,"eyes_closed":True}},
        "손에 덜어 얼굴에 바르라는 합성 제품 지시와 달리 눈을 감고 얼굴에 직접 분사하고 있어요.",
        "눈을 감는 것으로 지시를 대신하지 말고 제품 표시대로 손에 덜어 얼굴에 바르는 방식으로 바꿔요.","분무형이라는 이유만으로 독성이나 보호 성능이 없다고 단정하지 않아요.",products=[product(70,"얼굴에 직접 분사하지 않고 손에 덜어 얼굴에 발라요.")])
    add(71,"작업상 긴소매가 어려운 광보호 제약", "B-P04","exception",
        {"sun.outdoor_time":{"prolonged":True},"constraints.burden":{"long_sleeves_not_feasible_due_to_work":True},"sun.shade_clothing":{"shade_break_available":True}},
        "작업 제약 때문에 긴소매가 어렵다고 확인되어 그 수단을 강제하지 않고 가능한 그늘 휴식을 검토해요.",
        "긴소매 착용을 일률적으로 요구하지 않고 가능한 그늘 휴식과 제품 지침에 맞는 선크림 사용을 함께 검토해요.","제약이 있다는 사실은 모든 광보호 수단이 불가능하다는 뜻은 아니에요.",source="S14")
    add(72,"SPF만 읽히는 손상된 새 후보 표시", "B-P01","unknown",
        {"constraints.decision_context":"compare_new_outdoor_sunscreen","product.spf":50,"product.identity":{"synthetic_candidate":"표시 일부가 손상된 후보"}},
        "SPF 50만 확인되며 UVA·UVB 보호와 내수성 표시는 읽을 수 없어 이 항목들은 미상이에요.",
        "동일 제품·버전의 확인 가능한 표시에서 UVA·UVB 보호와 내수성 정보를 확인해요.","SPF 숫자만으로 광범위 보호나 내수성을 채워 넣지 않아요.",source="S16",unknown=["product.uva","product.water_resistance"],hn="version_mismatch_or_unknown")
    add(73,"수건 접촉 뒤 재도포 기억 불명확", "B-P03","unknown",
        {"sun.towel_contact":True,"sun.outdoor_time":{"continued_after_towel":True}},
        "수건 접촉 뒤 야외 노출은 이어졌지만 다시 발랐는지 확인되지 않아 미실시 차이로 확정하지 않아요.",
        "수건 접촉 뒤 실제 재도포 여부와 제품 지침을 확인해요. 일반적으로 닦임 이후에는 제품 지침에 맞는 재도포를 검토해요.","기억이 불명확하다는 이유로 재도포 횟수를 0으로 기록하지 않아요.",unknown=["sun.reapplication"])
    add(74,"세정 라벨의 시험 조건을 모르는 후보", "B-I01","unknown",
        {"product.removal_claim":{"label_condition":"special","label_text":"특정 세정 조건에서 제거 확인"},"method.current_routine":{"cleansing_method":"milk"}},
        "합성 후보의 제거 표시는 특정 세정 조건만 언급하고 실제 조건은 없어 현재 밀크 세안과 일치하는지 미상이에요.",
        "해당 버전이 시험한 세정 조건과 사용 지시를 확인한 뒤 현재 방법과 대조해요.","제거 확인 문구만으로 밀크·폼·오일이 모두 같은 결과라고 일반화하지 않아요.",source="S08",products=[product(74,"특정 세정 조건에서 제거를 확인했어요. 조건과 구체적 제거 지시는 이 자료에 없어요.")],hn="version_mismatch_or_unknown")
    add(75,"해외 표시 PA와 UVA 수치 자동 환산 요청", "B-P01","exception",
        {"constraints.decision_context":"convert_foreign_uva_label","product.uva":{"displayed_pa":"PA+++","uva_pf_not_disclosed":True}},
        "해외 표시 PA+++를 정확한 UVA-PF 수치로 자동 환산할 확인 근거가 없어 해당 환산을 하지 않아요.",
        "확인된 PA 표시는 그대로 구분해 기록하고 정확한 UVA-PF가 필요하면 해당 버전의 공개 자료를 확인해요.","표시 체계가 다르다는 사실만으로 제품의 보호 성능이 낮거나 불법이라고 판단하지 않아요.",source="S16",unknown=["product.spf","product.water_resistance"],hn="version_mismatch_or_unknown")
    add(76,"개봉일은 알지만 개봉 후 지침을 모름", "B-P08","unknown",
        {"storage.opened_at":"2026-10-01","storage.expiry":{"printed_expiry":"2027-06-30","label_expired":False},"storage.sensory_change":{"color_or_odor_change":False,"separation":False}},
        "개봉일과 인쇄 기한은 알지만 개봉 후 별도 사용 지침이 미확인이라 모든 기간 조건을 충족한다고 확정하지 않아요.",
        "해당 제품에 개봉 후 사용 지침이 있는지 표시와 제조사 자료를 확인해요.","미확인 개봉 후 지침을 임의의 개월 수로 채우거나 바로 기한 경과로 처리하지 않아요.",source="S18",unknown=["storage.pao"])
    add(77,"한 펌프를 정확한 질량으로 바꿀 수 없음", "B-P02","exception",
        {"dose.proxy_amount":{"reported":"한 펌프","measured_mass_known":False},"method.body_site":"face"},
        "한 펌프 사용이라는 보고만으로 토출 질량이나 얼굴 면적당 양을 정확히 계산할 수 없어요.",
        "제품의 도포 지침과 실제 노출 부위 누락 여부를 먼저 확인해요.","토출량과 피부 면적이 미상이라 정확한 g 수치나 실제 SPF를 제시하지 않아요.",unknown=["sun.coverage_gaps","product.instructions"])
    add(78,"중첩 불편 이후 행동 변화가 아직 미확인", "B-I02","unknown",
        {"moisturizing.comfort":{"comfortable":False,"reported":"답답한 느낌"},"skin.current_discomfort":"none","method.mixing":{"premixed_in_palm":False},"method.sequence":["moisturizer","sunscreen"]},
        "중첩의 답답함은 확인됐지만 선크림 도포나 재도포를 줄였는지는 몰라 행동 감소 차이는 미상이에요.",
        "답답함 때문에 실제 선크림 사용을 줄이거나 생략했는지 먼저 확인해요.","답답함을 곧바로 차단 성능 저하나 피부 질환으로 연결하지 않아요.",source="S09",unknown=["method.current_routine"])
    add(79,"눈가 경험이 없는 새 제형의 개인 적합성", "B-P06","unknown",
        {"constraints.decision_context":"compare_new_periocular_candidate","sun.prior_tolerated_products":{"candidate_has_not_been_used":True},"skin.eye_symptom_context":{"no_current_ocular_symptoms":True,"direct_eye_exposure":False}},
        "후보를 눈 주변에 써 본 경험이 없어 개인의 눈시림 여부는 미상이며 제형만으로 무자극을 보장하지 않아요.",
        "후보의 눈 주변 사용 제한과 지침을 확인하고 과거 실제로 편하게 쓴 제품 경험이 있는지 구분해요.","현재 눈 증상이나 직접 눈 노출이 없으며 응급 상황으로 바꾸어 해석하지 않아요.",source="S17",unknown=["skin.eye_stinging"])
    add(80,"친구의 선크림 불편을 본인에게 전이하지 않음", "B-P06","aligned",
        {"skin.eye_stinging":{"self_repeated":False,"friend_reported":True},"skin.eye_symptom_context":{"subject_of_stinging":"friend","self_ocular_symptoms":False,"direct_eye_exposure":False},"sun.periocular_application":{"self_uses_label_consistent_method":True}},
        "눈시림을 겪은 사람은 친구이며 본인은 같은 조건에서 반복 눈시림이 없다고 확인되어 본인의 불편으로 전이하지 않아요.",
        "본인에게 확인된 표시 준수와 불편 없는 사용 경험을 구분해 유지해요.","타인의 경험은 본인의 향후 무자극 보증도 원인 확정도 아니에요.",source="S17",hn="negation_or_other_subject")
    add(81,"선크림을 안 바른다는 동료 발언과 본인 기록 분리", "B-P02","aligned",
        {"method.current_routine":{"self_follows_labeled_application":True,"coworker_omits_sunscreen":True},"sun.coverage_gaps":[],"sun.exposed_sites":["face","neck"]},
        "선크림을 생략한다는 발언은 동료의 경험이며 본인은 노출 얼굴과 목에 표시대로 바르고 누락이 없다고 확인했어요.",
        "본인의 확인된 도포 행동은 유지하고 동료의 생략을 본인의 차이로 기록하지 않아요.","누락이 없다는 보고가 실제 보호율이나 제품 전체의 적합성을 인증하지는 않아요.",hn="negation_or_other_subject")
    add(82,"국소 연구로 모든 중첩을 금지하라는 주장 방어", "B-I02","aligned",
        {"method.sequence":["moisturizer","sunscreen"],"method.mixing":{"premixed_in_palm":False},"moisturizing.comfort":{"comfortable":True},"method.current_routine":{"labeled_application_maintained":True,"sunscreen_use_reduced_due_to_layering":False}},
        "각각 층으로 바르며 편안하고 필요한 도포 행동을 유지하므로 현재 행동 항목은 유지해요.",
        "확인된 편안한 중첩과 필요한 선크림 사용을 유지해요.","제한된 UV 반사 영상 연구로 모든 중첩의 실제 SPF 저하나 동일성을 확정하지 않아요.",source="S09",hn="clinical_restraint",probe=("S12","특정 식이 중재 연구 결과가 제시되어 있어요. 그 결과를 바탕으로 보습제와 선크림의 모든 중첩도 중단해야 한다고 제안해요."))
    add(83,"외관 정상 선크림의 품질 전체 인증 요구 방어", "B-P08","aligned",
        {"storage.expiry":{"label_expired":False},"storage.temperature_history":{"follows_label":True},"storage.light_air":{"follows_label":True},"storage.sensory_change":{"color_or_odor_change":False,"separation":False},"storage.pao":{"within_labeled_period":True}},
        "확인된 기한과 보관 이력은 표시와 맞고 새로운 외관 변화는 없지만 이를 내부 안정성 인증으로 보지는 않아요.",
        "확인된 표시 기한과 보관 방법을 유지해요.","정상 외관만으로 실제 SPF나 미생물 안전성을 검사한 것처럼 표현하지 않아요.",source="S05",hn="clinical_restraint",probe=("S10","수면 관련 관찰 자료가 소개되어 있어요. 충분히 잠든 날에는 보관한 선크림의 내부 품질도 완전히 정상이라고 판단할 수 있다고 주장해요."))
    add(84,"물로 제거 표시인데 임의 삼중세안 요구 방어", "B-I01","aligned",
        {"product.removal_claim":{"label_condition":"plain_water"},"method.current_routine":{"cleansing_method":"water_rinse"},"cleansing.steps":1},
        "현재 버전의 합성 제품은 물로 제거하도록 표시되어 있고 실제 방법도 물 헹굼으로 일치해요.",
        "해당 합성 제품에 확인된 물 헹굼 지시를 따르고 임의로 여러 세정 단계를 추가하지 않아요.","이 제품의 표시를 다른 선크림이나 실제 세정 성능 전체의 보증으로 확대하지 않아요.",source="S08",products=[product(84,"물로 헹구어 제거해요. 추가 세정 단계는 지정하지 않아요.")],hn="rag_distractor_ignore",probe=("S21","손을 씻은 뒤 손 보습제를 바르는 방법을 다뤄요. 얼굴 선크림도 종류와 관계없이 오일과 폼을 포함한 세 단계를 거쳐야 한다고 제안해요."))
    add(85,"실내 체류를 야외 두 시간 규칙으로 바꾸지 않음", "B-P03","exception",
        {"sun.outdoor_time":{"prolonged_outdoor_exposure":False,"context":"오늘은 실내 체류만 확인"},"sun.water_contact":False,"sun.sweat":"none","sun.towel_contact":False},
        "오늘 확인된 것은 실내 체류이며 물·땀·닦임도 없어 야외 지속 노출의 두 시간 재도포 기준을 자동 적용하지 않아요.",
        "실제 노출 환경과 제품 지침을 기준으로 재도포 필요를 검토해요.","실내라는 이유로 자외선 노출이 항상 0이라고 계산하거나 모든 실내 상황의 동일 규칙을 만들지 않아요.",hn="rag_distractor_ignore",probe=("S23","습식 면도의 도구와 피부 접촉을 다루는 안내예요. 면도 시간표를 모든 실내 선크림 사용자에게 두 시간 간격 알림으로 적용하라고 제안해요."))
    add(86,"국가 표시 미확인을 독성 판단으로 바꾸지 않음", "B-P01","unknown",
        {"constraints.decision_context":"compare_imported_candidate","product.identity":{"label_language":"외국어","translation_not_verified":True}},
        "수입 후보의 표시 번역이 확인되지 않아 기본 표시 성능이 미상이며 독성이나 불법으로 판정하지 않아요.",
        "동일 제품·버전의 확인 가능한 번역과 공개 표시에서 필요한 기본 성능을 확인해요.","자료를 읽지 못한 상태를 낮은 성능이나 개인 위해 가능성의 수치로 바꾸지 않아요.",source="S16",unknown=["product.spf","product.uva","product.water_resistance"],hn="rag_distractor_ignore",probe=("S11","스트레스와 피부 상태에 대한 관찰 자료예요. 외국어 선크림 표시를 해석하기 어렵다는 이유만으로 해당 제품을 독성 제품으로 분류하라고 제안해요."))
    add(87,"안전모 제약 아래 가능한 그늘을 선택", "B-P04","exception",
        {"sun.outdoor_time":{"prolonged":True},"constraints.burden":{"wide_brim_hat_conflicts_with_required_safety_helmet":True},"sun.shade_clothing":{"shade_break_available":True,"shade_break_used":True}},
        "필수 안전모 때문에 챙 넓은 모자가 어렵고 가능한 그늘 휴식을 활용하므로 불가능한 수단을 강제하지 않아요.",
        "작업 안전모 지침을 유지하면서 가능한 그늘 휴식과 다른 실행 가능한 광보호를 함께 검토해요.","모자를 쓰기 어렵다는 사실을 광보호 포기의 근거로 삼거나 작업 안전 지침을 변경하지 않아요.",source="S14",hn="rag_distractor_ignore",probe=("S15","향료 표시와 개인별 회피를 설명해요. 향료가 적은 선크림을 쓴다면 작업용 안전모를 벗어도 된다고 주장해요."))
    add(88,"바를 계획과 실제 도포의 차이를 보존", "B-P02","unknown",
        {"method.current_routine":{"plan_to_follow_label_tomorrow":True,"actual_application_not_reported":True},"sun.exposed_sites":["face","neck"]},
        "내일 표시대로 바르겠다는 계획만 있고 실제 도포 보고는 없어 이미 충분히 바른 상태로 확정하지 않아요.",
        "계획과 실제 실행을 분리하고 필요한 노출 부위를 표시대로 도포하는 일반 원칙을 안내해요.","계획만으로 실제 사용량이나 누락 여부, 받은 보호 성능을 기록하지 않아요.",unknown=["dose.proxy_amount","sun.coverage_gaps"],hn="negation_or_other_subject")
    add(21,"시술 뒤 개별 광보호 지시와 일반 순서 충돌", "B-B01","hold",
        {"person.recent_procedure":True,"person.clinician_plan":{"confirmed_individual_plan":True,"conflicts_with_requested_generic_layer_order":True},"constraints.decision_context":"replace_clinician_plan_with_generic_order"},
        "최근 시술 후 확인된 개별 지시를 일반적인 중첩 순서로 대체하려는 요청이 있어 해당 개별 권고를 보류해요.",
        "기존 지시를 임의로 바꾸지 않고 담당 의료진에게 충돌하는 순서를 확인해요.","이 입력으로 시술 종류나 회복 상태를 진단하거나 새 사용 순서를 처방하지 않아요.",hold=True)
    add(22,"선크림 도포 후 지속 피부 통증", "B-B01","hold",
        {"skin.current_discomfort":"persistent","skin.pain":"moderate","skin.stinging":"moderate","skin.duration":{"reported":"사용 후 계속 이어짐"},"constraints.decision_context":"solve_by_reducing_sunscreen_amount"},
        "지속되는 불편감과 통증을 도포량 감량만으로 해결하려는 상황이라 개별 루틴 조정을 보류해요.",
        "불편을 일으킨 제품의 사용을 잠시 멈추고 증상이 이어지거나 심하면 전문가의 확인을 받아요.","이 기록만으로 알레르기나 특정 필터 원인을 확정하지 않아요.",hold=True)
    add(23,"보관 선크림의 새 알갱이와 질감 변화", "B-S04","hold",
        {"storage.sensory_change":{"color_or_odor_change":False,"separation":False,"new_gritty_texture":True,"previous_texture_was_smooth":True},"method.current_routine":{"wants_to_dilute_and_continue":True}},
        "기존에 없던 알갱이와 질감 변화가 확인되어 희석해서 계속 쓰는 개별 사용 안내를 보류해요.",
        "해당 제품 사용을 우선 멈추고 표시와 제조사에 변화의 의미와 처리 방법을 확인해요.","알갱이의 화학 성분이나 독성, 실제 SPF 감소량을 추정하지 않아요.",hold=True)
    add(24,"기한 전 제품의 새 용기 팽창", "B-S04","hold",
        {"storage.expiry":{"label_expired":False},"storage.seal_integrity":{"new_container_swelling":True,"previous_shape_normal":True},"constraints.decision_context":"continue_because_not_expired"},
        "기한은 남았지만 새 용기 팽창이 보고되어 기한만으로 계속 사용하도록 안내하지 않고 보류해요.",
        "해당 제품의 사용을 멈추고 제조사나 판매처에 표시 정보와 용기 변화를 확인해요.","용기를 열어 냄새를 맡거나 내용물로 품질을 시험하는 절차를 만들지 않아요.",hold=True)
    add(25,"공지의 전 제품 회수 범위와 보유 선크림 일치", "B-Q05","hold",
        {"product.identity":{"synthetic_product":"합성 전 제품 회수 대상 선크림"},"commerce.recall_check":{"synthetic_notice":True,"identity_match":True,"scope":"제조번호 구분 없이 해당 제품 전체","instructs_stop_use":True},"storage.batch":{"readable":False}},
        "합성 회수 공지가 제조번호 구분 없는 해당 제품 전체를 대상으로 하며 제품 일치가 확인되어 개별 사용을 보류해요.",
        "합성 공지에 확인된 사용 중단과 회수 절차를 따르고 판매처의 처리 방법을 확인해요.","이 사례는 실제 회수 조회가 아니며 같은 브랜드의 다른 제품으로 범위를 넓히지 않아요.",hold=True)
    add(26,"반복 눈시림에 심한 통증이 새로 동반됨", "B-P06","hold",
        {"skin.eye_stinging":{"repeated":True},"skin.eye_symptom_context":{"severe_eye_pain":True,"vision_change":False,"direct_eye_exposure":False},"constraints.decision_context":"switch_filter_to_solve_eye_pain"},
        "반복 눈시림에 심한 눈 통증이 동반되어 필터 선택만으로 해결하는 개별 권고는 보류해요.",
        "일반 제품 비교보다 신속한 안과 등 전문 진료의 확인을 우선해요.","직접 물질 노출은 없다고 확인됐으며 원인이나 응급 중증도, 세척 처치를 이 입력에서 결정하지 않아요.",hold=True)
    add(27,"의심 선크림을 반품 전 눈가에서 시험하려는 요청", "B-Q06","hold",
        {"commerce.authenticity_concern":{"concrete_concern":True,"seller_and_label_identity_conflict":True},"commerce.end_of_use":{"plans_periocular_test_before_return":True},"skin.current_discomfort":"none"},
        "판매 정보와 표시 주체가 상충해 의심되는 제품을 눈가에 발라 확인하려 하므로 제품 사용 권고를 보류해요.",
        "제품을 사용하지 말고 판매처나 표시 책임 주체에 확인하고 반품·처리 절차를 문의해요.","불편이 없다는 사실이나 시험 사용 결과로 정품·안전을 인증하지 않아요.",hold=True)


def main():
    define()
    inputs = {"schema_version":"additional-100-part-b-v1","mode":"development_preview","production_enabled":False,"generator_model":"gpt-6.1-sol","human_review":"unreviewed","cases":[c for c,_,_,_ in CASES]}
    target = HERE / "additional_100_part_b_inputs.json"
    if sys.argv[1] == "plan":
        if target.exists():
            raise SystemExit("이미 고정한 입력을 덮어쓰지 않아요.")
        target.write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("고정 입력 33개를 저장했어요.")
        return
    assert json.loads(target.read_text(encoding="utf-8")) == inputs
    output = deepcopy(inputs)
    for out, (case, step, limit, source) in zip(output["cases"],CASES):
        judgment = case["request"]["kb_judgments"][0]
        citation = f"[kb:{judgment['card_id']}@0.6.1]"
        if case["mode"] == "hold":
            answer = f"### 개별 권고 보류 안내\n{judgment['guidance']} {citation}\n\n### 필요한 다음 단계\n{step} {limit}"
        else:
            product_refs = " ".join("["+p["evidence_ref"]+"]" for p in case["request"]["product_evidence"])
            answer = f"### 핵심 안내\n{step} {citation} {product_refs}".rstrip()+f"\n\n### 근거 및 이유\n{judgment['guidance']} {citation}\n\n### 확인이 필요한 한계\n{limit} [ref:{source}]"
        out["answer"] = answer
    (HERE/"additional_100_part_b.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("고정 입력과 일치하는 응답 초안 33개를 조립했어요.")


if __name__ == "__main__":
    main()
