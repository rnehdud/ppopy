"""Write an initial unreviewed input-only shard exactly once."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
DEST = HERE / 'additional_100_terra_part_b_inputs.json'
if DEST.exists():
    raise SystemExit('입력 파일이 이미 있어 덮어쓰지 않아요.')
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards = {x['id']: x for x in kb['baseline_cards']}
sources = {x['id']: x for x in kb['source_registry']}
def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
def obs(k, v, state='known'):
    return {'variable_id': k, 'state': state, 'value': v, 'source': 'synthetic_fixture', 'confirmed_by_user': state == 'known'}
def make(n, title, card, status, vals, guidance, source, chunk, bucket, hn=None, unknown=(), split='train'):
    rid = f'syn-sol-{n:04d}'
    observations = {k: obs(k, v) for k, v in vals.items()}
    observations.update({k: obs(k, None, 'unknown') for k in unknown})
    s = sources[source]
    ch = {'evidence_ref':'ref:'+source, 'text':chunk, 'scope':'general_skincare_practice', 'source_url':s['url'], 'locator':s['locator'], 'checked_on':s['checked_on'], 'limitations':s['limitations']}
    refs = ['kb:'+card+'@0.6.1', 'ref:'+source]
    req = {'mode':'solution', 'confirmed_observations':observations, 'kb_judgments':[{'card_id':card,'status':status,'guidance':guidance}], 'product_evidence':[], 'rag_chunks':[ch], 'allowed_evidence_refs':refs, 'distractor_refs':[]}
    return {'id':rid,'title':title,'pilot_bucket':bucket,'mode':'solution','scenario_id':'terra-b-scenario-'+rid,'group_id':'terra-b-group-'+rid,'scenario_family_id':'terra-b-family-'+rid,'split':split,'domains':['sun_protection'],'card_ids':[card],'is_hard_negative':hn is not None,'hard_negative_type':hn,'chunk_origins':{'ref:'+source:'kb_source_summary'},'request':req,'input_sha256':digest(req),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':guidance},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'새 합성 개발 사례이며 실제 사용자나 제품 기록, 엔진 실행 결과가 아니에요.'}

cases = [
 make(140,'내수성 시간 표시와 SPF 숫자의 구분','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.water_resistance':{'labeled':True,'minutes':80},'sun.outdoor_time':{'planned_outdoor_activity':True}},'내수성 시간 표시는 확인되지만 SPF와 광범위 보호 표시는 확인되지 않아 기본 성능 판단을 보류해요.','S16','Professional sunscreen guidance discusses SPF, broad-spectrum coverage and water resistance. A water-resistance time is not an SPF value.', 'unknown_or_version',hn='unknown_preservation',unknown=('product.spf','product.uva')),
 make(141,'물 접촉은 없지만 장시간 야외 노출 중 재도포 생략','B-P03','difference',{'sun.water_contact':False,'sun.towel_contact':False,'sun.outdoor_time':{'prolonged':True,'context':'야외 행사'},'sun.reapplication':{'reapplied':False}},'물이나 수건 접촉이 없더라도 장시간 야외 노출 중 재도포하지 않은 실제 행동을 확인했어요.','S05','Sunscreen guidance considers continued exposure as well as water, sweat and towel contact. The absence of one loss event does not measure actual ultraviolet exposure.','normal_guidance'),
 make(142,'두 번역본에 SPF가 달라 현재 버전 확인 필요','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','sun.outdoor_time':{'planned_outdoor_activity':True},'product.spf':{'translation_a':30,'translation_b':50,'current_version_confirmed':False}},'서로 다른 번역본의 SPF가 충돌하고 현재 제품 버전과 연결되지 않아 값을 확정하지 않아요.','S16','Sunscreen selection guidance discusses SPF and broad-spectrum protection. Product-specific facts must be checked against the relevant label.','unknown_or_version',hn='version_mismatch_hold'),
 make(143,'실제 노출 없는 계획만으로 재도포 누락 판정 금지','B-P03','unknown',{'sun.outdoor_time':{'planned_outdoor_activity':True},'sun.reapplication':{'intends_to_reapply':False}},'재도포하지 않을 계획은 보고했지만 실제 야외 노출과 행동은 확인되지 않았어요.','S05','자외선차단 안내는 실제 야외 노출과 제품 사용을 함께 살펴요. 계획만으로 실제 행동을 확인할 수는 없어요.','unknown_or_version',hn='unknown_preservation',unknown=('sun.water_contact',)),
 make(144,'보호용 안경으로 눈 주변 보호를 확보한 사용 조정','B-P06','aligned',{'skin.eye_stinging':{'repeated_with_same_product':True},'method.current_routine':{'stopped_near_eye_use':True,'protective_eyewear_used':True}},'같은 방식에서 반복된 눈시림 이후 눈가 사용을 조정하고 보호용 안경을 사용한다고 확인했어요.','S17','눈 주변 자외선차단 안내는 제품 선택과 눈에 흘러드는 상황을 함께 살펴요. 개인의 눈시림 원인을 특정하지 않아요.','normal_guidance'),
 make(145,'재도포 생략 없이 나타난 중첩 밀림','B-I02','exception',{'sun.pilling':{'present':True},'method.current_routine':{'sunscreen_use_reduced_due_to_layering':False,'reapplication_omitted_due_to_layering':False,'separated_application_times':True},'skin.current_discomfort':'none'},'중첩 밀림을 관찰했지만 사용이나 재도포를 줄이지 않아 사용성 검토에 해당해요.','S09','보습제와 선크림의 제한된 중첩 조합을 영상으로 살핀 연구예요. 영상 결과는 실제 야외 보호 성능을 보증하지 않아요.','normal_guidance')]
payload = {'schema_version':'additional-100-terra-part-b-inputs-v1','mode':'development_preview','production_enabled':False,'generator_model':'gpt-6.1-terra','human_review':'unreviewed','validation_status':'unreviewed_candidate','cases':cases}
with DEST.open('x', encoding='utf-8', newline='\n') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
    f.write('\n')
