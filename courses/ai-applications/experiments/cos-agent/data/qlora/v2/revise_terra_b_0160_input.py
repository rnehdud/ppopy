"""Replace a duplicated candidate and freeze the input before its answer."""
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/'additional_100_terra_part_b_inputs.json';root=p.parents[7];raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='9cf10f7a3132210ac78c6b6722babad6c86439ecb8f3d46f951c416e3aab6456'
out=root/'outputs/additional_100_terra/b_round2_inputs'
with (out/'before_0160_replacement.json').open('xb') as f:f.write(raw)
d=json.loads(raw.decode('utf-8'));kb=json.loads((root/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'));card=next(x for x in kb['baseline_cards'] if x['id']=='B-P01');s=next(x for x in kb['source_registry'] if x['id']=='S16')
c=next(x for x in d['cases'] if x['id']=='syn-sol-0160');c['title']='광범위 보호 표시와 별개인 낮은 SPF 야외 후보';c['card_ids']=['B-P01'];r=c['request']
def obs(k,v):return {'variable_id':k,'state':'known','value':v,'source':'synthetic_fixture','confirmed_by_user':True}
r['confirmed_observations']={k:obs(k,v) for k,v in {'constraints.decision_context':'compare_new_outdoor_sunscreen','product.spf':15,'product.uva':{'broad_spectrum_uva_uvb':True},'product.water_resistance':{'labeled':True},'sun.outdoor_time':{'planned_outdoor_activity':True}}.items()}
g='새 야외 후보는 광범위 보호와 내수성 표시가 있지만 SPF 15로 확인돼 기본 SPF 기준과 차이가 있어요.';r['kb_judgments']=[{'card_id':'B-P01','status':'difference','guidance':g}]
r['rag_chunks']=[{'evidence_ref':'ref:S16','text':'자외선차단제 선택 안내는 SPF 30 이상과 광범위 보호 및 내수성을 다뤄요. 표시 항목 하나로 다른 항목을 대신 확인하지 않아요.','scope':'general_skincare_practice','source_url':s['url'],'locator':s['locator'],'checked_on':s['checked_on'],'limitations':s['limitations']}];r['allowed_evidence_refs']=['kb:B-P01@0.6.1','ref:S16'];c['chunk_origins']={'ref:S16':'kb_source_summary'}
c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-P01','comparison_spec':card['comparison_spec'],'rationale':g};c['input_sha256']=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
t=p.with_suffix('.r2_0160.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
t.replace(p);print(hashlib.sha256(p.read_bytes()).hexdigest())
