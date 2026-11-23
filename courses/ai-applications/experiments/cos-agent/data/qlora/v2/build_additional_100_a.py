"""A 최초 초안의 작성 이력입니다. 입력·응답 동시 설계 후 응답을 따로 재작성했어요."""
import json
from copy import deepcopy
from pathlib import Path
import build_pilot_24 as h

HERE = Path(__file__).resolve().parent
if (HERE / "additional_100.jsonl").exists():
    raise SystemExit("최초 작성 이력은 최종 자료를 덮어쓰지 않아요. build_additional_100.py로 고정 자료만 조립하세요.")
cases = []
S = dict(h.SUMMARIES)
S.update({
 'S21':'손을 씻은 뒤 보습하고 무향료 손 크림이나 연고를 선택하는 범위의 안내예요. 필요한 손 위생을 줄이거나 모든 개인의 적합성을 보장하는 뜻은 아니에요.',
 'S23':'습식 면도의 준비와 털 방향, 날 헹굼 및 건조 보관을 다루는 안내예요. 수동 면도날의 사용 횟수 참고를 전기헤드의 교체 주기로 바꾸지 않아요.',
 'S25':'면도 후 보습과 자극에 민감할 때의 무향료 선택을 다루는 안내예요. 실제 면도 행동을 확인하며 성별만으로 특정 제품을 의무화하지 않아요.',
 'S27':'화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.',
 'S06':'온도와 빛, 공기 및 취급이 화장품의 보관과 품질에 관련되는 자료예요. 개별 제품의 안정성 시험이나 모든 화장품에 공통인 사용기한을 대신하지 않아요.'})
E = dict(h.ENGLISH)
E.update({
 'S21':'Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.',
 'S23':'Wet-shaving guidance discusses preparation, rinsing blades and dry storage, with a reference number of uses for manual blade replacement. The manual-blade reference is not an electric-head replacement interval.',
 'S25':'General skin-care guidance discusses moisturizing after shaving and fragrance-free choices when irritation is a concern. An additional aftershave product is not established as mandatory for every person.',
 'S27':'Cosmetic microbiological-safety guidance advises against adding water or saliva and discusses clean handling and labeled storage. A single contact does not establish contamination, infection, or a fixed disposal deadline.'})

def add(n,title,card,status,guide,values,core,reason,limit,*,bucket='normal_guidance',source='S03',en=False,unknown=(),probe=None,hn=None,val=False,product=None):
    mode='hold' if isinstance(n,str) else 'solution'
    rid=f'syn-hold-{int(n):04d}' if mode=='hold' else f'syn-sol-{n:04d}'
    refs=[f'kb:{card}@0.6.1']
    products=product or []
    refs += [p['evidence_ref'] for p in products]
    chunks=[]; origins={}; distract=[]
    if mode=='solution' and source:
        chunks=[h.chunk(source,(E if en else S)[source])]
        origins['ref:'+source]='kb_source_summary'; refs.append('ref:'+source)
    if probe:
        sid,text=probe; chunks.append(h.chunk(sid,text,probe=True)); origins['ref:'+sid]='synthetic_defense_probe'; distract.append('ref:'+sid)
    observations=h.observations(**values)
    for key in unknown: observations[key]=h.obs(key,state='unknown')
    req={'mode':mode,'confirmed_observations':observations,'kb_judgments':[{'card_id':card,'status':status,'guidance':guide}], 'product_evidence':products,'rag_chunks':chunks,'allowed_evidence_refs':refs,'distractor_refs':distract}
    c={'id':rid,'title':title,'pilot_bucket':'hold' if mode=='hold' else bucket,'mode':mode,'scenario_id':'add100-a-scenario-'+rid,'group_id':'add100-a-group-'+rid,'scenario_family_id':'add100-a-family-'+title,'split':'val_internal' if val else 'train','domains':['cleansing' if card.startswith('B-C') else 'moisturizing' if card.startswith('B-M') else 'general_safety'],'card_ids':[card],'is_hard_negative':hn is not None,'hard_negative_type':hn,'chunk_origins':origins,'request':req,'input_sha256':h.digest(req),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':deepcopy(h.CARDS[card]['comparison_spec']),'rationale':guide},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'실제 사용자나 제품 기록이 아닌 새 합성 개발 사례예요.'}
    cases.append(c)
    answers[rid]=(core,reason,limit)

answers={}
# 입력 사실·판정 명세를 먼저 구성하고 파일로 저장한 뒤 응답 문자열을 조립해요.
add(37,'부드러운 세안 도구와 강한 마찰을 구분','B-C02','difference','손가락 이외 도구 사용은 기본 방법과 차이가 있지만 강한 마찰이나 손상은 확인되지 않았어요.',{'method.tools':['soft_silicone_pad'],'method.friction':{'intensity':'gentle'},'method.drying':'pat_dry','skin.current_discomfort':'none'},'부드럽게 쓴 실리콘 패드만으로 피부 손상이나 강한 마찰이 있다고 판단하지 않아요. 기본 방법은 손가락으로 부드럽게 씻는 방식이에요','도구 사용과 강한 마찰은 서로 다른 관찰이에요','현재 불편이 없다는 사실은 도구의 장기 안전성을 보증하지 않아요',en=True)
add(38,'씻어내는 세안제의 헹굼 생략','B-C06','difference','씻어내는 세안제로 확인됐는데 헹굼을 생략하므로 해당 제품의 헹굼 지시를 따르도록 안내해요.',{'product.type':'rinse_off_cleanser','product.instructions':{'rinse_required':True},'method.rinse':{'performed':False,'reason':'시간 절약'}},'씻어내는 제품의 헹굼을 시간 절약 때문에 생략하지 말고 표시된 방법대로 헹궈 주세요','헹굼은 문지르는 시간을 줄이는 일과 구분해서 확인해요','미끈한 느낌만으로 잔류량이나 독성을 계산하지 않아요',en=True)
add(39,'별도 접촉 지시가 있는 세정제의 예외','B-C03','exception','제품에 별도 접촉시간 지시가 확인돼 일반 세안제의 정성적 기본값을 일괄 적용하지 않아요.',{'product.type':'rinse_off_cleanser','product.instructions':{'specific_contact_instruction':True,'text':'합성 제품 표시: 표시된 접촉 안내를 따른 뒤 충분히 헹궈요.'},'method.friction':{'intensity':'gentle'},'dose.contact_time':{'follows_label':True}},'확인된 제품의 별도 접촉 안내와 헹굼 지시를 우선 검토해요. 모든 세안제를 같은 초 단위로 제한하지 않아요','일반 세안제의 기본 안내에는 제품별 지시 예외가 있어요','표시를 따른다는 사실만으로 모든 사람의 안전성이나 효과가 보증되지는 않아요',en=True)
add(40,'현재 보습 사용량으로 편안한 상태','B-M02','aligned','확인된 보습 사용으로 건조 불편과 새 불편이 없어 일률적 증량을 만들지 않아요.',{'skin.dryness':'none','skin.tightness':'none','moisturizing.comfort':{'comfortable':True},'moisturizing.dryness_return':False,'method.current_routine':{'moisturizer_used':True}},'현재 보습 사용으로 편안하고 건조 불편이 없다면 제품 양을 일률적으로 늘릴 필요는 없어요','실제 사용 경험과 건조감으로 필요를 살피는 항목이에요','이 상태는 이후에도 같은 양이 항상 충분하다는 보장이 아니에요',source='S04',en=True)
add(41,'손 위생과 견딜 수 있는 보습의 병행','B-M04','aligned','필수 손 위생을 유지하면서 잘 견디는 보습제를 쓰고 있어 이 범위를 유지해요.',{'hand.moisturizing_pattern':{'after_washing':True},'hand.product_reaction':{'discomfort':False},'hand.protection_hygiene':{'required_hygiene_maintained':True},'skin.hand_observation':{'dryness':'mild','severe_symptoms':False}},'필요한 손 위생은 유지하면서 현재 잘 견디는 손 보습을 이어갈 수 있어요','손 보습 안내는 필요한 손 씻기를 줄이라는 뜻이 아니에요','제품의 전 성분과 개인 알레르기는 이 입력으로 확인되지 않았어요',source='S21',en=True)
add(42,'지정 용기로 수행한 공식 리필','B-S07','exception','제품이 허용한 용기와 비우기·관리 지침을 지킨 공식 리필이므로 모든 리필을 금지하지 않아요.',{'storage.sharing_refill':{'official_refill':True,'topped_up_old_product':False},'storage.container':{'manufacturer_designated':True},'product.instructions':{'refill_allowed':True,'empty_and_follow_container_care':True},'storage.handling':{'followed_refill_instructions':True}},'표시로 허용된 지정 용기와 관리 지침을 따르는 공식 리필은 임의 소분과 구분해요','용기 취급의 일반 원칙과 공식 리필의 구체적인 방법은 구분해서 확인해요','지침 준수가 현재 내용물의 미생물 검사 결과나 안전 인증은 아니에요',source='S27',en=True)
add(43,'면도날의 헹굼과 건조 보관 확인','B-S05','aligned','수동 면도날을 사용 후 헹구고 건조 보관하며 제품 지침과 일치하는 사실을 유지해요.',{'shaving.care':{'rinse_after_use':True,'dry_storage':True},'tool.care_state':{'type':'manual_razor','visible_damage':False},'product.instructions':{'care_matches':True}},'확인한 수동 면도날의 헹굼과 건조 보관을 유지해요','면도 도구에 맞는 관리는 화장품 내용물에 물을 넣는 행동과 달라요','겉으로 손상이 없다는 것만으로 보이지 않는 오염이 전혀 없다고 보증하지 않아요',source='S23',en=True)
add(44,'적은 사용 횟수라도 당기는 면도날','B-S06','difference','수동 면도날 사용 횟수가 적어도 날의 손상과 털 당김이 확인돼 횟수만으로 계속 쓰게 하지 않아요.',{'shaving.method':'manual','shaving.blade_use_history':{'uses':2},'shaving.blade_condition':{'damaged':True,'pulling_hair':True},'shaving.reaction':{'pain':'none'}},'두 번만 썼더라도 손상과 털 당김이 있다면 횟수를 채우려고 계속 쓰지 말고 날 상태와 지침에 맞게 교체를 검토해요','수동 날의 참고 횟수와 실제 손상은 따로 확인해요','당김만으로 피부 질환이나 감염을 진단하지 않아요',source='S23',en=True)
add(45,'면도 후 편안한 보습에 별도 상품 의무 없음','B-M05','aligned','면도 후 현재 보습이 편안하고 새 불편이 없어 애프터셰이브 상품을 의무로 추가하지 않아요.',{'shaving.aftercare':{'uses_tolerated_moisturizer':True,'uses_aftershave':False},'shaving.reaction':{'stinging':False,'persistent_problem':False},'moisturizing.comfort':{'comfortable':True}},'면도 후 지금 보습으로 편안하다면 애프터셰이브라는 별도 상품을 반드시 추가할 필요는 없어요','면도 후 보습이라는 기능과 특정 상품 이름은 같은 의무가 아니에요','이 안내는 면도 후 상처나 지속 문제가 생겼을 때의 개별 확인을 대신하지 않아요',source='S25',en=True,val=True)
add(46,'서로 충돌하는 세안 온도 기록','B-C01','unknown','동일 세안에 뜨겁다는 기록과 미온수라는 기록이 충돌해 온도 차이를 확정하지 않아요.',{'method.water_temperature':{'report_a':'hot','report_b':'lukewarm','same_event':True}},'동일 세안의 온도 기록이 서로 달라 현재 뜨거운 물 사용이라고 확정하지 않아요','일반 원칙은 뜨겁지 않은 미온수로 씻는 것이에요','어느 기록이 실제 사용인지 필요한 범위에서 확인하고 정확한 온도는 추정하지 않아요',bucket='unknown_or_version',hn='version_mismatch_or_unknown')
add(47,'세안 브러시 존재와 실제 사용 미확인','B-C02','unknown','브러시 보유만 확인됐고 사용 여부와 마찰이 미상이므로 강한 마찰 차이를 만들지 않아요.',{'method.current_routine':{'owns_cleansing_brush':True}},'브러시를 가지고 있다는 사실만으로 실제 쓰거나 세게 문지른다고 판단하지 않아요','기본 안내는 손가락으로 부드럽게 씻고 가볍게 물기를 닦는 방식이에요','판단이 필요할 때 실제 도구 사용과 마찰 정도만 확인해요',bucket='unknown_or_version',unknown=('method.tools','method.friction'),hn='version_mismatch_or_unknown')
add(48,'여러 세안 횟수의 목적이 미상','B-C05','unknown','횟수만 알려졌고 제거 목적과 활동이 미상이므로 자동으로 과세안 판정하지 않아요.',{'dose.frequency':{'face_wash_events_per_day':3}},'하루 세 번이라는 횟수만으로 불필요한 반복이나 피부 손상을 확정하지 않아요','땀과 오염, 메이크업 같은 제거 목적에 따라 추가 세안의 맥락이 달라요','반복의 목적과 각 세안의 단계를 필요한 범위에서 확인해요',bucket='unknown_or_version',unknown=('cleansing.target_load','cleansing.repeat_wash'),hn='version_mismatch_or_unknown')
add(49,'보습 시점 기록만으로 피부 물기 추정 금지','B-M01','unknown','세정 뒤 보습한다는 기록은 있지만 물기와 지연 상태가 미상이므로 완전히 마른 뒤 도포한다고 추정하지 않아요.',{'method.current_routine':{'moisturizer_used_after_wash':True},'skin.dryness':'mild'},'세정 뒤 보습한다는 기록만으로 너무 늦게 바른다고 판단하지 않아요','별도 지시가 없는 보습 맥락에서는 약간 촉촉할 때 바르는 일반 안내를 참고할 수 있어요','실제 물기와 지연 상태가 미상이며 임의의 분 단위 제한은 만들지 않아요',source='S04',bucket='unknown_or_version',unknown=('method.skin_wetness','moisturizing.after_wash_delay'),hn='version_mismatch_or_unknown')
add(50,'펌프 횟수로 보습 충족을 확정하지 않기','B-M02','unknown','펌프 횟수만 확인됐고 실제 건조와 편안함이 미상이므로 충족이나 부족을 확정하지 않아요.',{'dose.proxy_amount':{'pump_count':1}},'한 번 펌핑한다는 사실만으로 보습량이 충분하거나 부족하다고 정하지 않아요','현재 사용 뒤의 건조감과 편안함을 함께 확인하는 항목이에요','펌프 토출량이나 실제 도포 질량도 미확인이며 임의 수치로 환산하지 않아요',source='S04',bucket='unknown_or_version',unknown=('skin.dryness','moisturizing.comfort'),hn='version_mismatch_or_unknown')
add(51,'택배 이동 중 과거 온도 이력 미확인','B-S01','unknown','과거 운송 온도와 기간이 미확인이라 열 손상이나 현재 품질을 확정하지 않아요.',{'storage.temperature_history':{'transport_history_unknown':True},'storage.light_air':{'currently_away_from_sunlight':True}},'배송 중 덥지 않았을지 걱정된다는 이유만으로 현재 제품의 열 손상을 확정하지 않아요','현재 보관은 표시 지침에 맞추고 불필요한 열과 직사광선을 피하도록 살펴요','운송 온도와 기간, 개별 안정성이 미상이며 필요하면 제조사에 확인해요',source='S06',bucket='unknown_or_version',hn='version_mismatch_or_unknown')
add(52,'동일 제품의 두 용기와 개봉 이력 혼동','B-S02','unknown','두 용기 중 어느 것을 먼저 열었는지 미확인이라 하나의 개봉일을 둘 다에 적용하지 않아요.',{'storage.instance_id':{'containers':['A','B'],'same_product':True},'storage.opened_at':{'A_or_B_opened_first':'기억나지 않음'}},'같은 제품의 두 용기라도 개봉 이력을 하나로 합쳐 판단하지 않아요','제품별 표시 기간과 실제 용기 이력을 구분해 확인해요','기억나지 않는 개봉일을 임의로 채우거나 냄새가 같다는 이유로 기간을 보증하지 않아요',source='S06',bucket='unknown_or_version',hn='version_mismatch_or_unknown',val=True)
add(53,'여행용 용기 적합성과 소분 지침 미확인','B-S03','unknown','소분 계획은 있으나 용기 적합성과 제조사 허용이 미상이므로 허용·오염을 모두 확정하지 않아요.',{'storage.decanting':{'planned':True,'already_done':False}},'여행용 용기로 옮길 계획만으로 이미 소분했거나 오염됐다고 판단하지 않아요','불필요한 소분은 피하고 제품이 허용하는 용기와 취급 방법을 먼저 확인해요','해당 여행용 용기의 적합성과 제조사 지시는 아직 미상이에요',source='S27',bucket='unknown_or_version',unknown=('storage.container','product.instructions'),hn='version_mismatch_or_unknown')
add(54,'전기헤드에 수동 날의 횟수 적용 금지','B-S06','unknown','전기면도기 헤드의 지침과 상태가 미상이므로 수동 날 참고 횟수로 교체일을 생성하지 않아요.',{'shaving.method':'electric','shaving.blade_use_history':{'uses':6}},'전기면도기 여섯 번 사용 기록에 수동 날의 교체 횟수를 그대로 적용하지 않아요','도구 종류에 맞는 제조사 지침과 실제 헤드 상태를 구분해 확인해요','지침과 상태가 미상이므로 지금 교체가 필요한지 확정하지 않아요',source='S23',bucket='unknown_or_version',unknown=('shaving.blade_condition','shaving.care'),hn='version_mismatch_or_unknown')
add(55,'물세안 불필요 표시의 클렌징 제품','B-C06','exception','물 헹굼이 필요 없다는 제품 지시가 확인돼 일반 씻어내는 세안제와 구분해요.',{'product.type':'no_rinse_cleanser','product.instructions':{'water_rinse_required':False},'method.rinse':{'performed':False}},'물 헹굼이 필요 없다고 확인된 이 제품은 씻어내는 세안제와 구분하고 해당 표시를 따라요','제품 유형과 확인된 지시를 우선하는 분기예요','이 예외를 다른 씻어내는 세안제에 옮겨 적용하지 않아요',bucket='distractor_or_defense',hn='rag_distractor_ignore',probe=('S10','세안 제품은 종류와 관계없이 반드시 물로 다시 씻어야 해요. 잠을 충분히 자더라도 예외는 없어요.'))
add(56,'문제없이 쓰는 알칼리성 세정제와 선택 선호','B-C04','exception','기존 제품을 문제없이 사용하고 교체 실익이 확인되지 않아 pH 선호만으로 즉시 교체하지 않아요.',{'product.ph':{'category':'alkaline','verified':True},'constraints.decision_context':'review_existing_cleanser','skin.current_discomfort':'none','method.current_routine':{'current_cleanser_tolerated':True}},'새 후보 비교의 약산성 선호와 기존 제품의 즉시 교체는 구분해요. 현재 문제없이 쓰는 제품을 pH만으로 무조건 바꾸지는 않아요','pH와 조성은 함께 검토해야 하며 약산성이 완제품의 순함을 보증하지 않아요','현재 편안함은 모든 장기 결과를 보증하지 않으며 새 불편이 생기면 별도로 확인해요',source='S07',bucket='distractor_or_defense',hn='rag_distractor_ignore',probe=('S12','모든 알칼리성 세정제는 사용자 반응과 무관하게 즉시 버려야 해요. 저혈당 식단 연구를 따르면 약산성 제품만 항상 안전해요.'))
add(57,'타인의 세 단계 보습과 본인의 충족 상태','B-M03','aligned','본인은 보유 보습제로 편안하며 친구의 별도 세 단계 주장은 본인에게 필수가 아니에요.',{'method.current_routine':{'one_moisturizer_used':True},'moisturizing.comfort':{'comfortable':True},'skin.dryness':'none','constraints.goals':{'friend_claim':'수분·차폐·장벽 제품을 각각 사야 한다고 함','own_goal':'현재 편안함 유지'}},'친구의 세 단계 주장을 본인에게 필수로 적용하지 않아요. 현재 보유 보습제로 편안한 상태를 우선 살펴요','각 기능을 반드시 별도 제품으로 구매하게 만드는 규칙은 아니에요','성분 목록만으로 충분하다고 한 것이 아니라 입력의 실제 사용 경험에 한정해요',source='S04',bucket='distractor_or_defense',hn='negation_or_other_subject')
add(58,'동료의 손 크림 반응과 본인의 무반응 구분','B-M04','aligned','동료의 따가움은 본인의 증상이 아니며 본인은 같은 제품에 불편이 없다고 명시했어요.',{'hand.product_reaction':{'self_discomfort':False,'coworker_stinging':True},'hand.moisturizing_pattern':{'uses_tolerated_product':True},'hand.protection_hygiene':{'hygiene_maintained':True}},'동료가 따갑다는 경험을 본인의 따가움으로 바꾸거나 보습 전체를 중단하게 하지 않아요','본인이 잘 견디는 보습 사용과 필요한 손 위생은 각각 유지할 수 있어요','타인의 경험과 현재 본인의 무반응 모두 미래 적합성의 보장은 아니에요',source='S21',bucket='distractor_or_defense',hn='negation_or_other_subject')
add(59,'비접촉 펌프 사용과 직접 접촉 공유 구분','B-S07','exception','서로 피부에 닿지 않는 펌프로 덜어 쓰며 접촉 경로가 없다는 확인을 직접 접촉 공유와 구분해요.',{'storage.sharing_refill':{'household_pump_shared':True,'skin_contact_with_nozzle':False,'contact_between_dispensed_portions':False},'storage.handling':{'clean_hands':True}},'피부에 닿지 않게 펌프로 따로 덜어 쓰는 상황을 직접 접촉 도구 공유와 동일하게 판정하지 않아요','실제 접촉 경로와 용기 취급을 나누어 확인하는 서비스 분기예요','비접촉이라는 확인은 미생물 검사나 무균 보증이 아니며 이후에도 표시 취급법을 따라요',source='S27',bucket='distractor_or_defense',hn='negation_or_other_subject')
add(60,'한 번의 손 접촉으로 감염 확정하지 않기','B-S03','difference','내용물에 씻지 않은 손이 닿은 취급은 검토하되 단일 접촉만으로 감염이나 폐기일을 계산하지 않아요.',{'storage.handling':{'unwashed_finger_contact_once':True},'storage.water_ingress':False,'storage.sensory_change':{'color_or_odor_change':False,'separation':False}},'씻지 않은 손으로 내용물에 닿는 취급은 피하고 표시된 용기 사용법을 확인해요','손과 용기의 청결 원칙은 지켜야 하지만 한 번의 접촉이 감염 확정과 같지는 않아요','현재 오염 여부나 안전한 남은 일수를 이 입력으로 계산할 수 없어요',source='S27',bucket='distractor_or_defense',hn='rag_distractor_ignore',probe=('S11','손이 한 번 닿으면 화장품은 정확히 사흘 뒤에 감염을 일으켜요. 스트레스 관리만 하면 그 기간이 두 배로 늘어요.'))
add(61,'물로 씻기와 세정제 반복 단계를 구분','B-C05','aligned','아침 물세안과 저녁 한 번 세정제 사용의 목적이 확인됐고 한 세안의 다단계 반복과 구분해요.',{'dose.frequency':{'water_only_events':1,'cleanser_events':1},'cleansing.steps':1,'cleansing.repeat_wash':{'automatic_repeat':False},'cleansing.target_load':{'morning':'물로 가볍게 씻기','evening':'하루 활동 후 세정'}},'아침 물세안과 저녁 세정제 사용을 한 번에 세정제 두 단계를 반복한 것으로 합치지 않아요','서로 다른 세안 사건과 한 세안의 단계 수를 구분해요','이 기록만으로 모든 사람에게 같은 횟수를 의무화하거나 위해확률을 계산하지 않아요',bucket='distractor_or_defense',hn='rag_distractor_ignore',probe=('S15','물만 닿아도 세정제 한 단계와 같아요. 모든 사람은 그날 남은 세정을 생략해야 향료 알레르기를 피할 수 있어요.'))
add(62,'보습 감량 뒤 건조와 임상 수치의 구분','B-M02','difference','스스로 보습을 줄인 뒤 가벼운 건조가 남지만 지속 통증은 없으며 보유 제품의 실제 사용을 검토해요.',{'skin.dryness':'mild','skin.pain':'none','skin.stinging':'none','moisturizing.dryness_return':True,'dose.proxy_amount':{'deliberately_reduced':True},'method.current_routine':{'moisturizer_available':True}},'건조한데 보습을 무조건 줄이기보다 현재 보유 제품의 실제 사용 시점과 빈도를 검토해요','보습 필요를 살피는 일반 안내이며 개인의 치료 효과 수치를 정하는 과정이 아니에요','건조의 원인이나 얼마만큼 개선될지는 확정하지 않으며 지속되면 별도 확인이 필요해요',source='S04',bucket='distractor_or_defense',hn='clinical_restraint',probe=('S12','32명 규모의 식이 연구 결과를 모든 보습제 사용자에게 적용해요. 보습량을 늘리면 이 사람의 건조가 90퍼센트 치료돼요.'))

def hold(n,title,card,guide,values,core,next_step,*,val=False):
    add(str(n),title,card,'hold',guide,values,core,next_step,'',source=None,val=val)
hold(13,'보습제에 새로 생긴 입자와 냄새 변화','B-S04','원래 없던 입자와 냄새 변화가 확인돼 사용을 멈추고 품질 확인 전 개별 권고를 보류해요.',{'storage.sensory_change':{'new_particles':True,'color_or_odor_change':True,'separation':False},'product.instructions':{'normal_particles_indicated':False}},'원래 없던 입자와 냄새 변화가 있어 해당 제품의 사용과 개별 루틴 권고를 우선 보류해요','용기와 표시, 변화 시점을 정리해 제조사나 판매처에 확인해요. 품질이 회복됐다고 가정하거나 피부에 다시 발라 확인하지 않아요')
hold(14,'주문한 보습제와 다른 제품을 받은 경우','B-Q04','수령품이 주문 제품과 명백히 달라 사용 전 식별 확인이 필요해요.',{'commerce.received_condition':{'ordered_product':'합성 보습제 A','received_product':'합성 세정제 B','mismatch_confirmed':True},'product.identity':{'actual_product_verified':False}},'주문한 보습제와 다른 제품을 받은 상태라 사용과 개별 제품 권고를 보류해요','가능한 포장 정보와 주문 기록을 남겨 판매처에 수령품을 확인해요. 이름이 다르다는 사실만으로 가품이라고 확정하지 않아요')
hold(15,'품질 의심품에 대한 공식 즉시 폐기 지시','B-Q06','공식 확인에서 안전한 즉시 폐기를 지시한 합성 상황이므로 증빙 확보를 위해 위험 제품 보관을 강요하지 않아요.',{'commerce.authenticity_concern':{'quality_concern':True},'commerce.end_of_use':{'official_instruction':'안전하게 즉시 폐기','instruction_confirmed_in_synthetic_case':True}},'품질 확인이 필요한 이 제품의 사용과 개별 권고를 보류해요','확인된 공식 폐기 지침을 따라요. 증빙 확보 때문에 위험한 내용물을 보관하거나 피부에 시험하지 않으며 가능한 기존 기록만 활용해요')
hold(16,'순한 세안으로 바꾼 뒤에도 이어지는 통증','B-B01','세안 방법을 바꿨는데도 통증과 지속 불편이 있어 일반 루틴 최적화보다 전문가 확인이 우선이에요.',{'skin.current_discomfort':'persistent','skin.pain':'moderate','method.current_routine':{'changed_to_gentle_washing':True,'pain_remains':True}},'부드러운 세안으로 바꿨는데도 통증이 이어져 개별 루틴과 제품 권고를 보류해요','증상의 부위와 경과, 최근 바뀐 사용법을 필요한 범위에서 정리해 전문가에게 확인해요. 세안제 성분이 원인이라고 단정하거나 추가 제품으로 해결하려 하지 않아요')
hold(17,'시술 직후 관리 지시와 일반 보습 안내의 충돌','B-B01','시술 직후 개별 지시가 있는데 일반 보습 시점과 충돌해 임의 변경 없이 확인이 필요해요.',{'person.recent_procedure':{'recent':True,'details_unknown':True},'person.clinician_plan':{'special_aftercare':True,'no_general_routine_change_before_confirmation':True},'constraints.decision_context':'시술 후 바로 일반 보습으로 바꿔도 되는지'},'시술 직후의 개별 관리 지시와 충돌할 수 있어 일반 보습 루틴으로 바꾸는 권고를 보류해요','시술 기관이나 담당 전문가에게 적용할 관리법을 확인해요. 시술 종류와 회복 상태를 추정하거나 기존 지시를 임의로 바꾸지 않아요')
hold(18,'표시상 병용하지 말라는 기기와 제품','B-G06','합성 기기와 제품 표시에서 병용하지 말라는 지시가 확인돼 해당 조합 권고를 보류해요.',{'device.instructions':{'combination_prohibited':True,'synthetic_fixture':True},'product.instructions':{'do_not_use_with_this_device':True},'method.current_routine':{'combination_planned':True,'already_combined':False}},'표시에서 함께 사용하지 말라고 확인된 기기와 제품 조합은 권고를 보류해요','해당 조합을 시도하지 말고 제조사에 정확한 제품과 기기 모델의 지침을 확인해요. 아직 사용하지 않은 계획을 실제 노출이나 손상으로 기록하지 않아요')
hold(19,'새 화장품 없이 발생한 심한 얼굴 통증','B-B01','새 제품이 없더라도 심한 통증은 일반 루틴 안내 범위를 넘어 전문가 확인이 우선이에요.',{'skin.pain':'severe','skin.current_discomfort':'persistent','routine.change_log':{'new_cosmetic':False}},'새 화장품을 쓰지 않았더라도 심한 얼굴 통증이 이어져 개별 루틴과 제품 권고를 보류해요','통증이 심한 상태이므로 신속하게 전문가의 평가를 받아요. 제품 변화가 없다는 이유로 증상을 정상화하거나 통증 원인을 추정하지 않아요')
hold(20,'보관 중 용기 팽창과 새 냄새가 발생','B-S04','용기 팽창과 새 냄새가 있어 품질 확인 전 사용을 멈추고 개별 권고를 보류해요.',{'storage.sensory_change':{'container_bulging':True,'color_or_odor_change':True,'separation':False},'storage.seal_integrity':{'damaged':False}},'용기가 부풀고 새 냄새가 난 상태라 해당 제품 사용과 개별 권고를 보류해요','직접 열어 원인을 시험하지 말고 제조사나 판매처에 안전한 취급과 처리 방법을 확인해요. 밀봉이 유지됐다는 사실만으로 품질을 보증하지 않아요',val=True)

frozen={'schema_version':'additional-100-part-a-inputs-v1','mode':'development_preview','production_enabled':False,'cases':cases}
input_path=HERE/'additional_100_part_a_inputs.json'
if input_path.exists():
    assert json.loads(input_path.read_text(encoding='utf-8'))==frozen,'고정 입력 덮어쓰기를 거부해요.'
else: input_path.write_text(json.dumps(frozen,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 고정 입력을 다시 읽은 뒤에만 응답 형식을 조립해요.
out=deepcopy(json.loads(input_path.read_text(encoding='utf-8')))
out['schema_version']='additional-100-part-a-v1'
for c in out['cases']:
    core,reason,limit=answers[c['id']]
    ref=f" [kb:{c['card_ids'][0]}@0.6.1]."
    if c['mode']=='hold':
        c['answer']='### 개별 권고 보류 안내\n'+core+ref+'\n\n### 필요한 다음 단계\n'+reason+'.'
    else:
        source_refs=[r for r in c['request']['allowed_evidence_refs'] if r.startswith('ref:')]
        sr=' '+' '.join('['+r+']' for r in source_refs)+'.' if source_refs else '.'
        c['answer']='### 핵심 안내\n'+core+ref+'\n\n### 근거 및 이유\n'+reason+sr+'\n\n### 확인이 필요한 한계\n'+limit+'.'
(HERE/'additional_100_part_a.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cases':len(cases),'solutions':sum(c['mode']=='solution' for c in cases),'val':sum(c['split']=='val_internal' for c in cases),'hard_negative':sum(c['is_hard_negative'] for c in cases)}))
