"""Preserve revision 2 and correct unreviewed input candidates before answers."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
path=HERE/'additional_100_terra_part_b_inputs.json'
raw=path.read_bytes()
backup=ROOT/'outputs/terra100/b/rev2'
backup.mkdir(parents=True,exist_ok=True)
with (backup/path.name).open('xb') as f: f.write(raw)
with (backup/'sha256.txt').open('x',encoding='ascii') as f: f.write(hashlib.sha256(raw).hexdigest()+'\n')
d=json.loads(raw.decode('utf-8'))
assert len(d['cases'])==33 and d['schema_version'].endswith('v2')
kb=json.loads((ROOT/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards={x['id']:x for x in kb['baseline_cards']}
src={x['id']:x for x in kb['source_registry']}
def obs(k,v):
    return {'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None}
def change(c,card,status,title,values,guidance):
    c['title']=title;c['card_ids']=[card]
    r=c['request'];r['confirmed_observations']={k:obs(k,v) for k,v in values.items()};r['kb_judgments']=[{'card_id':card,'status':status,'guidance':guidance}]
    s=src['S05']; r['rag_chunks']=[{'evidence_ref':'ref:S05','text':'자외선차단 안내는 제품 지침과 노출 상황을 함께 살펴요. 개인의 실제 자외선량이나 보호율을 이 자료로 계산하지 않아요.','scope':'general_skincare_practice','source_url':s['url'],'locator':s['locator'],'checked_on':s['checked_on'],'limitations':s['limitations']}]
    r['allowed_evidence_refs']=['kb:'+card+'@0.6.1','ref:S05'];r['distractor_refs']=[];c['chunk_origins']={'ref:S05':'kb_source_summary'}
    c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':guidance}
for c in d['cases']:
    r=c['request']; o=r['confirmed_observations']; rid=c['id']
    if rid in {'syn-hold-0044','syn-hold-0046','syn-hold-0048'}:
        facts=o['skin.pain']['value'];o['skin.pain']=obs('skin.pain',None)
        o['skin.current_discomfort']=obs('skin.current_discomfort','persistent')
        routine=o.get('method.current_routine',obs('method.current_routine',{}))
        routine['value']['reported_pain_context']=facts
        o['method.current_routine']=routine
    if rid=='syn-hold-0050':
        o['skin.current_discomfort']=obs('skin.current_discomfort','persistent_swelling')
    if rid=='syn-sol-0145':
        change(c,'B-P02','exception','도포 지침과 노출 부위의 상충',{'sun.exposed_sites':['face','ears'],'sun.coverage_gaps':['ears'],'product.instructions':{'excluded_site':'ears'},'method.current_routine':{'ear_omission_due_to_label_restriction':True}},'노출된 귀를 빼는 이유가 확인된 제품의 사용 제한과 연결되어 일반 도포 기준의 예외를 검토해요.')
    if rid=='syn-sol-0164':
        change(c,'B-P03','aligned','제품별 수건 접촉 후 재도포 지침과 실제 행동',{'sun.outdoor_time':{'outdoor_exposure_continues':True},'sun.towel_contact':True,'product.instructions':{'reapply_after_towel':True},'sun.reapplication':{'after_towel':True,'followed_product_instruction':True}},'수건 접촉 후 야외 노출이 이어지고 확인된 제품 지침에 따라 실제 재도포했어요.')
        c['is_hard_negative']=True;c['hard_negative_type']='clinical_restraint'
    c['input_sha256']=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
d['schema_version']='additional-100-terra-part-b-inputs-v3'
d['revision_note']='통제 변수 타입과 중복 의심 후보를 수정한 미검수 입력이에요.'
temp=path.with_suffix('.revision3.tmp')
with temp.open('x',encoding='utf-8',newline='\n') as f: json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
temp.replace(path)
