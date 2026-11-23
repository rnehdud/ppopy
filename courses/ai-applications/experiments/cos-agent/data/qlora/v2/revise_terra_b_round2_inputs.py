"""Freeze revised input candidates before creating any revised answers."""
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/'additional_100_terra_part_b_inputs.json'
root=p.parents[7]; raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='e6b7c362536f570c97869271a061ddfce8746a683cc8a83b0b356734a994ad41'
out=root/'outputs/additional_100_terra/b_round2_inputs';out.mkdir(parents=True,exist_ok=True)
with (out/'before.json').open('xb') as f:f.write(raw)
d=json.loads(raw.decode('utf-8'))
kb=json.loads((root/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards={x['id']:x for x in kb['baseline_cards']};sources={x['id']:x for x in kb['source_registry']}
def obs(k,v):return {'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None}
def judge(c,status,g):
    c['request']['kb_judgments'][0].update(status=status,guidance=g);c['judgment_basis']['rationale']=g
def replace(c,title,card,status,values,g,source,english):
    c['title']=title;c['card_ids']=[card];r=c['request'];r['confirmed_observations']={k:obs(k,v) for k,v in values.items()};r['kb_judgments']=[{'card_id':card,'status':status,'guidance':g}]
    s=sources[source];t={'S05':('자외선차단 안내는 야외 노출과 물 접촉, 제품 사용 지침을 함께 살펴요. 실제 노출량이나 개인의 보호율은 이 자료로 계산하지 않아요.','Sun protection guidance considers outdoor exposure, water contact and product instructions. It does not calculate individual ultraviolet exposure or protection.'),'S16':('자외선차단제 선택 안내는 SPF와 광범위 보호, 내수성 표시를 살펴요. 표시 항목 하나만으로 다른 항목을 확정할 수 없어요.','Sunscreen guidance discusses SPF, broad-spectrum coverage and water resistance. One label attribute does not establish another.'),'S17':('눈 주변 사용을 살펴보는 자외선차단 안내예요. 개인의 불편 원인은 이 안내만으로 확정할 수 없어요.','Guidance discusses sunscreen use around the eyes. It does not identify the cause of an individual symptom.')}[source][int(english)]
    r['rag_chunks']=[{'evidence_ref':'ref:'+source,'text':t,'scope':'general_skincare_practice','source_url':s['url'],'locator':s['locator'],'checked_on':s['checked_on'],'limitations':s['limitations']}];r['allowed_evidence_refs']=['kb:'+card+'@0.6.1','ref:'+source];r['distractor_refs']=[];c['chunk_origins']={'ref:'+source:'kb_source_summary'}
    c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':g}
for c in d['cases']:
    rid=c['id'];o=c['request']['confirmed_observations']
    if rid=='syn-sol-0144':judge(c,'aligned','같은 제품에서 반복된 눈시림 이후 눈가 사용을 조정하고 보호용 안경을 사용한다고 보고했어요.')
    if rid=='syn-sol-0148':judge(c,'unknown','야외 노출이 끝난 뒤 재도포하지 않았다는 정보만으로 그 이전 야외 활동 중 행동을 알 수 없어요.')
    if rid=='syn-sol-0149':judge(c,'unknown','수영용 후보에 내수성 표시가 없지만 표시 부재만으로 실제 성능 미충족을 확정하지 않아요.')
    if rid=='syn-sol-0150':judge(c,'unknown','색 또는 냄새 변화로 기록됐지만 어떤 변화인지와 원래 제형과의 차이는 미상이에요.')
    if rid=='syn-sol-0151':judge(c,'unknown','보이는 숫자 80의 뜻을 알 수 없어 SPF나 내수성 시간으로 정하지 않아요.')
    if rid=='syn-sol-0152':judge(c,'unknown','판매 페이지와 현재 용기의 버전이 일치하지 않아 페이지의 SPF를 현재 제품 값으로 채택하지 않아요.')
    if rid=='syn-sol-0153':judge(c,'unknown','재도포 기록의 내용이 서로 다르지만 같은 외출의 기록인지는 확인되지 않았어요.')
    if rid in {'syn-hold-0044','syn-hold-0046'}:
        judge(c,'hold','지속 불편이 보고됐고 통증의 별도 항목과 맥락 기록이 일치하지 않아 개별 권고를 보류해요.')
    if rid=='syn-sol-0147':replace(c,'제품의 물 접촉 후 재도포 지침과 실제 야외 행동','B-P03','difference',{'sun.water_contact':True,'sun.outdoor_time':{'continues_after_water':True},'product.instructions':{'reapply_after_water':True},'sun.reapplication':{'after_water':False}},'물 접촉 후 야외 노출이 이어졌지만 확인된 제품 지침과 달리 재도포하지 않았어요.','S05',True)
    if rid=='syn-sol-0158':replace(c,'다른 버전의 SPF와 현재 버전 광범위 보호 표시','B-P01','unknown',{'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':{'other_version':50,'matches_current_version':False},'product.uva':{'broad_spectrum_uva_uvb':True},'product.water_resistance':{'labeled':True},'sun.outdoor_time':{'planned_outdoor_activity':True}},'현행 버전의 광범위 보호와 내수성 표시는 확인됐지만 다른 버전의 SPF는 현행 값으로 옮길 수 없어요.','S16',False)
    if rid=='syn-sol-0160':replace(c,'재도포 제품 지침 확인 전 물 접촉 이후 실제 재도포','B-P03','aligned',{'sun.outdoor_time':{'outdoor_exposure_continues':True},'sun.water_contact':True,'sun.reapplication':{'after_water':True},'product.instructions':None},'물 접촉 후 야외 노출이 이어지는 중 실제 재도포했지만 해당 제품의 구체적 지침은 미상이에요.','S05',False)
    if rid=='syn-sol-0161':replace(c,'반복 눈시림과 개인별 의료진 지시의 우선 확인','B-P06','exception',{'skin.eye_stinging':{'repeated_with_same_product':True},'method.current_routine':{'clinician_individual_eye_area_plan':True,'plan_details_known':False}},'반복 눈시림과 개인별 의료진 계획이 보고됐지만 계획 내용은 미상이라 일반 기준으로 덮어쓰지 않아요.','S17',False)
    if rid=='syn-hold-0048':
        c['title']='기존 진료 계획의 임의 변경 요청';r=c['request'];r['confirmed_observations']={'method.current_routine':obs('method.current_routine',{'clinician_individual_plan':True,'wants_replace_with_general_guidance':True,'plan_details_known':False})};judge(c,'hold','내용이 확인되지 않은 개인별 진료 계획을 일반 기준으로 대체하는 개별 권고를 보류해요.')
    c['input_sha256']=hashlib.sha256(json.dumps(c['request'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
d['schema_version']='additional-100-terra-part-b-inputs-round2';d['revision_note']='독립 감사의 입력 판단 지적을 반영한 미검수 수정 후보예요.'
tmp=p.with_suffix('.round2.tmp')
with tmp.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
tmp.replace(p)
print(hashlib.sha256(p.read_bytes()).hexdigest())
