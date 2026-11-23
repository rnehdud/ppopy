"""Retain revision 3 and distinguish the final negative from the prior audit."""
import hashlib
import json
from pathlib import Path
p=Path(__file__).resolve().parent/'additional_100_terra_part_b_inputs.json'
root=p.parents[7]
raw=p.read_bytes()
out=root/'outputs/terra100/b/rev3';out.mkdir(parents=True,exist_ok=True)
with (out/p.name).open('xb') as f:f.write(raw)
with (out/'sha256.txt').open('x',encoding='ascii') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
d=json.loads(raw.decode('utf-8'))
kb=json.loads((root/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
card=next(c for c in kb['baseline_cards'] if c['id']=='B-P02')
c=next(c for c in d['cases'] if c['id']=='syn-sol-0164')
def obs(k,v):return {'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None}
g='친구가 귀를 빼고 바른 사실은 확인되지만 본인의 노출 부위 누락 여부는 미상이에요.'
c['title']='친구의 노출 부위 누락과 본인 기록 구분';c['card_ids']=['B-P02'];c['hard_negative_type']='negation_or_other_subject'
r=c['request'];r['confirmed_observations']={'sun.exposed_sites':obs('sun.exposed_sites',['face','ears']),'sun.coverage_gaps':obs('sun.coverage_gaps',None),'method.current_routine':obs('method.current_routine',{'friend_omits_ears':True})}
r['kb_judgments']=[{'card_id':'B-P02','status':'unknown','guidance':g}];r['allowed_evidence_refs']=['kb:B-P02@0.6.1','ref:S05']
c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-P02','comparison_spec':card['comparison_spec'],'rationale':g}
c['input_sha256']=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
d['schema_version']='additional-100-terra-part-b-inputs-v4';d['revision_note']='중복 우려 사례를 타인과 본인의 노출 부위 관찰 구분으로 교체한 미검수 입력이에요.'
tmp=p.with_suffix('.revision4.tmp')
with tmp.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
tmp.replace(p)
