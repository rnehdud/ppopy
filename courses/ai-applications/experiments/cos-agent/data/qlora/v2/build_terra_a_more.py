"""Append independently authored solution inputs once."""
import copy, hashlib, json
from pathlib import Path
H = Path(__file__).resolve().parent
P = H / 'additional_100_terra_part_a_inputs.json'
D = json.loads(P.read_text(encoding='utf-8'))
if len(D['cases']) != 12: raise RuntimeError('Unexpected input revision')
K = json.loads((H.parents[6] / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards = {x['id']:x for x in K['baseline_cards']}
old = {c['id']:c for f in H.glob('additional_100_part_*_inputs.json') for c in json.loads(f.read_text(encoding='utf-8'))['cases']}

def case(n, base, title, values, status, guidance, bucket, split='train'):
    c=copy.deepcopy(old[base]); ident=f'syn-sol-{n:04d}'; card=c['card_ids'][0]
    c.update(id=ident,title=title,scenario_id='terra-a-scenario-'+ident,group_id='terra-a-group-'+ident,scenario_family_id=f'terra-a-family-{n:04d}',split=split,pilot_bucket=bucket)
    req=c['request']; req['confirmed_observations']={k:{'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None} for k,v in values.items()}
    req['kb_judgments'][0].update(status=status,guidance=guidance)
    c['judgment_basis'].update(comparison_spec=cards[card]['comparison_spec'],rationale=guidance)
    c['input_sha256']=hashlib.sha256(json.dumps(req,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    return c

D['cases'].extend([
 case(126,'syn-sol-0038','별도 헹굼 지시를 알고도 물을 닦기만 함',{'product.type':'rinse_off_cleanser','product.instructions':{'rinse_required':True},'method.rinse':{'performed':False,'wiped_off_only':True}},'difference','씻어내라는 제품의 지시와 닦아내기만 한 실제 사용을 구분해요.','normal_guidance'),
 case(127,'syn-sol-0040','현재 보습으로 편안하지만 타인의 정량을 따르려 함',{'skin.dryness':'none','skin.tightness':'none','moisturizing.comfort':{'comfortable':True},'method.current_routine':{'moisturizer_used':True,'considering_other_person_amount':True}},'aligned','본인에게 편안한 현재 사용과 다른 사람의 정량 기준을 구분해요.','normal_guidance'),
 case(128,'syn-sol-0047','도구를 물로 씻었는지 확인되지만 건조 여부는 미상',{'method.tools':['cleansing_brush'],'tool.care_state':{'cleaned_after_use':True,'drying_unknown':True}},'unknown','씻은 사실만으로 건조 보관 여부나 실제 피부 마찰을 확정하지 않아요.','unknown_or_version'),
 case(129,'syn-sol-0048','두 세안 단계 수는 알지만 한 단계의 목적은 미상',{'cleansing.steps':2,'cleansing.repeat_wash':{'second_step_purpose_unknown':True},'cleansing.target_load':{'makeup_removed':True}},'unknown','화장 제거 목적과 별도로 두 번째 단계의 목적은 확인되지 않았어요.','unknown_or_version'),
 case(130,'syn-sol-0050','보습 뒤 무거운 느낌은 알지만 건조 충족은 미상',{'moisturizing.comfort':{'heavy_feel':True,'dryness_relief_unknown':True},'skin.dryness':None,'dose.proxy_amount':{'pumps':1}},'unknown','무거운 느낌이나 펌프 횟수만으로 건조 불편이 충족됐는지 판단하지 않아요.','unknown_or_version','val_internal'),
 case(131,'syn-sol-0053','리필 표시가 있으나 잔량 위 덧붓기 허용은 미확인',{'storage.decanting':{'planned':True,'already_done':False},'product.instructions':{'refill_allowed':True,'topping_up_unknown':True},'storage.container':None},'unknown','리필 표시만으로 잔량 위 덧붓기와 용기 적합성이 확인되지는 않아요.','unknown_or_version'),
 case(132,'syn-sol-0060','표시된 희석 지시와 원제품 임의 물 혼입 구분',{'storage.handling':{'followed_dilution_instructions':True},'storage.water_ingress':False,'product.instructions':{'dilution_required':True}},'exception','확인된 제품별 희석 지시와 원제품에 임의로 물을 넣는 행동을 구분해요.','distractor_or_defense'),
 case(133,'syn-sol-0061','운동 후 필요한 세안과 습관적 추가 단계 구분',{'dose.frequency':{'cleanser_events':2},'cleansing.steps':2,'cleansing.repeat_wash':{'automatic_repeat':True},'cleansing.target_load':{'one_event_after_sweating':True,'extra_step_reason_unknown':True}},'unknown','운동 후 세안 필요와 그 세안에서 추가 단계가 필요한지는 별도로 확인해요.','distractor_or_defense'),
 case(134,'syn-sol-0062','보습 후 무거움과 건조 지속을 별개로 확인',{'skin.dryness':'mild','skin.pain':'none','skin.stinging':'none','moisturizing.comfort':{'heavy_feel':True,'dryness_return_reported':True},'method.current_routine':{'moisturizer_available':True}},'difference','무거운 느낌과 남은 건조 불편을 함께 검토하되 수치로 효과를 약속하지 않아요.','distractor_or_defense'),
 case(135,'syn-sol-0056','약산성 후보와 기존 제품 반응의 별도 판단',{'product.ph':{'candidate_mildly_acidic':True},'skin.current_discomfort':'none','method.current_routine':{'existing_cleanser_tolerated':True}},'exception','약산성 후보라는 정보만으로 기존에 잘 쓰는 제품의 교체 실익이 확정되지는 않아요.','distractor_or_defense'),
 case(136,'syn-sol-0057','별도 보습 기능 세 가지를 세 통으로 반드시 채우려 함',{'method.current_routine':{'separate_hydration_occlusion_barrier_products_required':True},'moisturizing.comfort':{'comfortable':True},'skin.dryness':'none'},'difference','보습 기능을 무조건 각각 별도 제품으로 채울 필요는 없으며 현재 충족 상태를 살펴요.','distractor_or_defense'),
 case(137,'syn-sol-0058','필수 위생은 유지하며 향료 표시와 개인 반응 구분',{'hand.protection_hygiene':{'required_hygiene_maintained':True},'hand.product_reaction':{'discomfort':False},'hand.moisturizing_pattern':{'after_washing':True},'product.instructions':{'fragrance_free':False}},'aligned','향료 표시만으로 현재 본인의 반응을 확정하지 않고 필수 위생과 사용 경험을 함께 살펴요.','distractor_or_defense'),
 case(138,'syn-sol-0059','비접촉 용기와 피부에 직접 닿는 도구 동시 공유',{'storage.handling':{'shared_noncontact_pump':True,'shared_skin_contact_tool':True}},'difference','펌프의 비접촉 공유와 피부에 직접 닿는 도구 공유를 구분해 검토해요.','distractor_or_defense','val_internal'),
 case(139,'syn-sol-0060','원제품 물 혼입과 제품의 외관 정상은 별개',{'storage.water_ingress':True,'storage.handling':{'water_added_without_instructions':True},'storage.sensory_change':{'color_or_odor_change':False,'separation':False}},'difference','외관이 같다는 관찰은 임의 물 혼입 취급이나 현재 품질을 보증하지 않아요.','distractor_or_defense'),
])
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('26 candidate inputs; no answers')
