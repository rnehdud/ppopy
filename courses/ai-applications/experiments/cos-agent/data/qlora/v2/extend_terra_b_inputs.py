"""Extend the unreviewed input-only shard; preserve its prior revision."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
DEST = HERE / 'additional_100_terra_part_b_inputs.json'
BACKUP = ROOT / 'outputs/terra100/b/rev1'
BACKUP.mkdir(parents=True, exist_ok=True)
raw = DEST.read_bytes()
old = BACKUP / DEST.name
with old.open('xb') as f:
    f.write(raw)
with (BACKUP / 'sha256.txt').open('x', encoding='ascii') as f:
    f.write(hashlib.sha256(raw).hexdigest() + '\n')
data = json.loads(raw.decode('utf-8'))
assert len(data['cases']) == 6
for case in data['cases']:
    if case['id'] in {'syn-sol-0140', 'syn-sol-0142', 'syn-sol-0143'}:
        case['hard_negative_type'] = 'version_mismatch_or_unknown'
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards = {x['id']:x for x in kb['baseline_cards']}
src = {x['id']:x for x in kb['source_registry']}
def hashobj(x):
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def obs(k,v):
    return {'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None}
def add(n,title,card,status,values,guidance,bucket,source='S05',english=False,hn=None,hold=False,val=False):
    rid = f"syn-{'hold' if hold else 'sol'}-{n:04d}"
    chunks=[]; origins={}; refs=['kb:'+card+'@0.6.1']
    if not hold:
        s=src[source]
        texts={'S05':('자외선차단 안내는 노출과 물, 땀, 닦임 및 표시 사용법을 함께 살펴요. 개인이 받은 자외선량은 이 자료로 계산할 수 없어요.','Sun protection guidance considers exposure, water, sweat, towel contact and product directions. It does not calculate an individual ultraviolet dose.'), 'S16':('자외선차단제 선택 안내는 SPF, 광범위 보호와 내수성 표시를 함께 다뤄요. 확인하지 못한 표시를 다른 숫자로 대신할 수 없어요.','Sunscreen selection guidance discusses SPF, broad-spectrum protection and water resistance. One label feature does not establish another.'), 'S18':('제품의 사용기한과 보관 이력은 따로 확인해야 해요. 겉모습만으로 남은 보호 성능을 계산할 수 없어요.','Sunscreen guidance discusses expiry and storage conditions. Appearance alone cannot calculate remaining protection.'), 'S08':('선택된 제품과 세정 방법을 비교한 제한된 연구예요. 모든 제품에 같은 제거 방법을 일반화하지 않아요.','A limited study compared selected sunscreen formulations and cleansing methods. Its findings do not prescribe the same removal method for every product.'), 'S09':('제한된 제품 중첩을 영상으로 관찰한 연구예요. 실제 야외 보호 성능이나 개인별 결과를 보증하지 않아요.','A limited imaging study examined selected product layering. It does not guarantee individual outdoor protection.'), 'S17':('눈 주변 자외선차단과 제품 사용 상황을 다루는 안내예요. 특정 개인의 불편 원인을 확정하지 않아요.','Guidance considers sunscreen use around the eyes. It does not determine an individual cause of discomfort.')}
        t=texts[source][int(english)]
        chunks=[{'evidence_ref':'ref:'+source,'text':t,'scope':'general_skincare_practice','source_url':s['url'],'locator':s['locator'],'checked_on':s['checked_on'],'limitations':s['limitations']}]
        origins={'ref:'+source:'kb_source_summary'}; refs.append('ref:'+source)
    req={'mode':'hold' if hold else 'solution','confirmed_observations':{k:obs(k,v) for k,v in values.items()},'kb_judgments':[{'card_id':card,'status':status,'guidance':guidance}],'product_evidence':[],'rag_chunks':chunks,'allowed_evidence_refs':refs,'distractor_refs':[]}
    data['cases'].append({'id':rid,'title':title,'pilot_bucket':bucket,'mode':req['mode'],'scenario_id':'terra-b-scenario-'+rid,'group_id':'terra-b-group-'+rid,'scenario_family_id':'terra-b-family-'+rid,'split':'val_internal' if val else 'train','domains':['general_safety' if hold else 'sun_protection'],'card_ids':[card],'is_hard_negative':hn is not None,'hard_negative_type':hn,'chunk_origins':origins,'request':req,'input_sha256':hashobj(req),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':guidance},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'새 합성 개발 사례이며 실제 사용자나 제품 기록, 엔진 실행 결과가 아니에요.'})

# Distinct synthetic observations and time/evidence interactions; all remain unreviewed.
rows = [
(146,'비가 그친 뒤에도 이어지는 야외 노출','B-P03','difference',{'sun.water_contact':True,'sun.outdoor_time':{'prolonged':True,'continues_after_rain':True},'sun.reapplication':{'reapplied':False}},'비에 젖은 뒤에도 야외 노출이 계속되지만 다시 바르지 않았어요.','normal_guidance','S05',True,None),
(147,'땀 뒤 닦지 않았지만 재도포도 하지 않음','B-P03','difference',{'sun.water_contact':{'heavy_sweat':True},'sun.towel_contact':False,'sun.reapplication':{'reapplied':False},'sun.outdoor_time':{'prolonged':True}},'심하게 땀 흘린 뒤 닦지 않았어도 재도포하지 않은 행동이 확인됐어요.','normal_guidance','S05',True,None),
(148,'장시간 야외 활동이 끝난 뒤 재도포 시점','B-P03','exception',{'sun.outdoor_time':{'prolonged':True,'outdoor_exposure_ended':True},'sun.reapplication':{'after_going_inside':False}},'야외 노출이 끝난 시점의 정보만으로 지속 노출 중 누락을 확정할 수 없어요.','normal_guidance','S05',True,'negation_or_other_subject'),
(149,'현재 표시의 내수성 부재와 수영 후보','B-P01','difference',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':50,'product.uva':{'broad_spectrum_uva_uvb':True},'product.water_resistance':{'labeled':False},'sun.outdoor_time':{'planned_swimming':True}},'수영용 새 후보에 내수성 표시가 없는 것으로 확인됐어요.','normal_guidance','S16',True,None),
(150,'선크림 사용 후 새 냄새와 기한 전 표시','B-P08','difference',{'storage.expiry':{'label_expired':False},'storage.sensory_change':{'color_or_odor_change':True},'method.current_routine':{'continues_using':True}},'기한 전이라도 새로운 냄새 변화가 보고되어 품질 확인이 필요해요.','normal_guidance','S18',True,None),
(151,'표시 시간 숫자의 의미가 잘린 야외 후보','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.water_resistance':{'visible_number':80,'meaning':'미상'},'sun.outdoor_time':{'planned_outdoor_activity':True},'product.spf':None,'product.uva':None},'잘린 숫자만으로 SPF나 내수성 시간을 정할 수 없어요.','unknown_or_version','S16',True,'version_mismatch_or_unknown'),
(152,'현재 용기와 판매 페이지의 국가 버전 연결 미상','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':{'website':50,'container_version_match':False},'product.uva':None,'sun.outdoor_time':{'planned_outdoor_activity':True}},'판매 페이지와 현재 용기의 버전 일치가 확인되지 않아 현재 표시를 확정하지 않아요.','unknown_or_version','S16',True,'version_mismatch_or_unknown'),
(153,'장시간 외출 중 도포 기록 두 개가 충돌','B-P03','unknown',{'sun.outdoor_time':{'prolonged':True},'sun.reapplication':{'record_a':'재도포함','record_b':'재도포하지 않음'}},'같은 외출에 대한 두 기록이 충돌해 실제 재도포 여부가 미상이에요.','unknown_or_version','S05',True,'version_mismatch_or_unknown'),
(154,'수영을 계획했지만 실제 입수 여부 미상','B-P03','unknown',{'sun.water_contact':None,'sun.outdoor_time':{'planned_swimming':True},'sun.reapplication':{'intended_after_swimming':True}},'수영과 재도포 계획은 있지만 실제 입수와 재도포는 확인되지 않았어요.','unknown_or_version','S05',False,'version_mismatch_or_unknown'),
(155,'용기 색 변화가 원래 제형인지 미상','B-P08','unknown',{'storage.sensory_change':{'color_change_observed':True,'original_appearance_known':False},'storage.expiry':None},'색이 원래 상태와 달라진 것인지 및 사용기한이 확인되지 않았어요.','unknown_or_version','S18',False,'version_mismatch_or_unknown'),
(156,'눈 가까이 쓰지 않은 제품의 사용 경험','B-P06','unknown',{'method.current_routine':{'used_on_face':True,'used_near_eyes':False},'skin.eye_stinging':None},'얼굴 사용 경험만으로 눈 주변에서 반복 눈시림이 없는지 확정할 수 없어요.','unknown_or_version','S17',False,'version_mismatch_or_unknown'),
(157,'보습제와 선크림의 중첩 뒤 기록 누락','B-I02','unknown',{'sun.pilling':{'present':True},'method.current_routine':{'sunscreen_use_reduced_due_to_layering':None,'reapplication_omitted_due_to_layering':None}},'밀림은 관찰됐지만 그 때문에 실제 사용이나 재도포가 줄었는지 미상이에요.','unknown_or_version','S09',False,'version_mismatch_or_unknown'),
(158,'제품 숫자 하나로 자외선 보호 전체 추정 거절','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':30,'product.uva':None,'product.water_resistance':None,'sun.outdoor_time':{'planned_outdoor_activity':True}},'SPF만 확인되어 광범위 보호와 물 접촉 적합성은 미상이에요.','distractor_or_defense','S16',False,'clinical_restraint'),
(159,'가족의 재도포 이력을 본인 기록으로 대체하지 않기','B-P03','unknown',{'sun.outdoor_time':{'prolonged':True},'sun.reapplication':{'family_member_reapplied':True,'own_reapplication':None}},'가족의 행동은 확인됐지만 본인의 재도포는 미상이에요.','distractor_or_defense','S05',False,'negation_or_other_subject'),
(160,'제품의 수영용 표시가 개인 보호 결과를 보장하지 않음','B-P01','aligned',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':50,'product.uva':{'broad_spectrum_uva_uvb':True},'product.water_resistance':{'labeled':True},'sun.outdoor_time':{'planned_swimming':True}},'야외 수영 후보의 기본 표시는 확인됐지만 개인의 실제 보호 결과는 별개예요.','distractor_or_defense','S16',False,'clinical_restraint'),
(161,'시험 평균과 개인의 눈가 반응을 혼동하지 않기','B-P06','unknown',{'method.current_routine':{'used_near_eyes':False},'skin.eye_stinging':None},'집단 자료나 타인의 경험으로 본인의 눈가 반응을 확정하지 않아요.','distractor_or_defense','S17',False,'clinical_restraint'),
(162,'실내 보관 기록으로 과거 차량 보관 부정 불가','B-P08','unknown',{'storage.expiry':{'label_expired':False},'storage.sensory_change':{'color_or_odor_change':False},'method.current_routine':{'currently_stored_indoors':True,'past_hot_car_storage':None}},'현재 실내 보관 사실만으로 과거 열 노출 여부를 확정하지 않아요.','distractor_or_defense','S18',False,'version_mismatch_or_unknown'),
(163,'실제 도포와 제품 구매 의도의 구분','B-P03','unknown',{'sun.outdoor_time':{'prolonged':True},'sun.reapplication':{'new_product_purchase_planned':True,'reapplied':None}},'제품 구매 계획은 실제 재도포 행동을 확인해 주지 않아요.','distractor_or_defense','S05',False,'negation_or_other_subject'),
(164,'선크림과 보습제의 별도 층 도포와 혼합 구분','B-I02','aligned',{'method.sequence':['moisturizer','sunscreen'],'method.mixing':{'premixed_in_palm':False},'sun.pilling':{'present':False},'method.current_routine':{'sunscreen_use_reduced_due_to_layering':False,'reapplication_omitted_due_to_layering':False},'skin.current_discomfort':'none'},'별도로 바르고 불편이나 광보호 행동 감소가 보고되지 않았어요.','distractor_or_defense','S09',False,'clinical_restraint'),
(165,'친구가 느낀 밀림과 자신의 사용 행동 분리','B-I02','unknown',{'sun.pilling':{'friend_reported':True,'own_experience':None},'method.current_routine':{'own_sunscreen_use_reduced':None}},'친구의 경험으로 본인의 밀림이나 실제 사용 감소를 판단하지 않아요.','distractor_or_defense','S09',False,'negation_or_other_subject')]
for i,r in enumerate(rows):
    add(*r[:7],source=r[7],english=r[8],hn=r[9],val=i in (4,9,15))
holds=[
(44,'반복된 안구 통증과 도포 시점 미확인','B-B01',{'skin.pain':{'site':'눈','persistent':True},'method.current_routine':{'application_timing_known':False}},'원인과 도포 시점이 불명확해도 지속 통증에 대한 개별 권고를 보류해요.'),
(45,'품질 의심 선제품의 판매처 확인 전 재사용 요청','B-S04',{'storage.sensory_change':{'new_odor':True,'separation':True},'method.current_routine':{'wants_to_reuse_before_seller_reply':True}},'새 냄새와 분리의 품질 확인 전에 재사용을 전제로 한 개별 권고를 보류해요.'),
(46,'야외 노출 후 지속 통증과 기한 확인','B-B01',{'skin.pain':{'persistent':True,'after_outdoor_exposure':True},'storage.expiry':{'label_expired':False}},'기한이 남았다는 정보로 지속 통증의 원인을 정하지 않고 개별 권고를 보류해요.'),
(47,'뚜껑 파손과 새 냄새를 양으로 해결하려는 요청','B-S04',{'storage.sensory_change':{'new_odor':True,'container_damage':True},'method.current_routine':{'wants_to_use_smaller_amount':True}},'품질 이상 의심을 사용량 조정만으로 해결하는 개별 권고를 보류해요.'),
(48,'눈가 제품 중단 후에도 이어지는 통증','B-B01',{'skin.pain':{'site':'눈 주변','persistent_after_discontinuation':True},'method.current_routine':{'stopped_product':True}},'제품 사용을 멈춘 뒤에도 지속되는 통증의 원인을 추정하지 않고 개별 권고를 보류해요.'),
(49,'표시가 같은 두 용기 중 한 용기의 새로운 분리','B-S04',{'storage.sensory_change':{'one_container_new_separation':True,'other_container_unchanged':True},'method.current_routine':{'wants_to_mix_containers':True}},'한 용기에 새로운 분리가 관찰돼 두 용기를 섞는 개별 권고를 보류해요.'),
(50,'사용 중 지속 부종과 상충하는 일반 사용 지침','B-B01',{'skin.current_discomfort':{'persistent_swelling':True},'method.current_routine':{'wants_to_follow_general_label_despite_symptoms':True}},'지속되는 부종을 일반 사용 지침만으로 해결하는 개별 권고를 보류해요.')]
for n,title,card,values,guidance in holds:
    add(n,title,card,'hold',values,guidance,'hold',hold=True)
for case in data['cases']:
    bucket_updates = {'syn-sol-0156':'distractor_or_defense', 'syn-sol-0157':'distractor_or_defense', 'syn-sol-0160':'normal_guidance'}
    if case['id'] in bucket_updates:
        case['pilot_bucket'] = bucket_updates[case['id']]
assert len(data['cases']) == 33
data['schema_version']='additional-100-terra-part-b-inputs-v2'
data['revision_note']='입력 후보 확장본이며 모든 사례는 검토 전입니다.'
temp=DEST.with_suffix('.revision2.tmp')
with temp.open('x',encoding='utf-8',newline='\n') as f:
    json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
temp.replace(DEST)
