"""Refine three candidate inputs before generating revision answers."""
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/'additional_100_terra_part_b_inputs.json';root=p.parents[7];raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='a440d0737b0ef583f1c9e17b6e747e4b7ec1171bd0d48572b0c2547fc18c1417'
out=root/'outputs/additional_100_terra/b_round2_inputs'
with (out/'intermediate.json').open('xb') as f:f.write(raw)
d=json.loads(raw.decode('utf-8'));k=json.loads((root/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'));cards={c['id']:c for c in k['baseline_cards']}
def obs(k,v):return {'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None}
for c in d['cases']:
 r=c['request'];i=c['id']
 if i=='syn-sol-0147':
  c['title']='내수성 시간 표시를 수건 후 재도포 면제로 오해한 행동';r['confirmed_observations']={k:obs(k,v) for k,v in {'product.water_resistance':{'labeled':True,'minutes':80},'sun.water_contact':True,'sun.towel_contact':True,'sun.outdoor_time':{'continues_after_towel':True},'sun.reapplication':{'after_towel':False,'reason':'내수성 시간 표시가 재도포를 면제한다고 생각함'}}.items()};g='내수성 시간 표시를 재도포 면제로 오해해 수건 접촉 후 야외 노출 중 다시 바르지 않았어요.';r['kb_judgments'][0]['guidance']=g;c['judgment_basis']['rationale']=g
 if i=='syn-sol-0161':
  c['title']='눈가 제한 표시와 반복 불편 뒤 대체 보호 미확인';r['confirmed_observations']={k:obs(k,v) for k,v in {'skin.eye_stinging':{'repeated_with_same_product':True},'product.instructions':{'avoid_eye_area':True},'method.current_routine':{'stopped_near_eye_use':True,'alternative_eye_protection':None}}.items()};g='해당 제품은 눈가 사용 제한이 있고 사용도 중단했지만 대체 보호 여부는 미상이에요.';r['kb_judgments'][0].update(status='unknown',guidance=g);c['judgment_basis']['rationale']=g
 if i=='syn-hold-0048':
  c['title']='회수 비대상 확인과 별도 새 이물의 품질 보류';c['card_ids']=['B-S04'];g='합성 회수 공지의 대상 로트에는 해당하지 않지만 별도의 새 이물이 보고되어 품질 확인을 보류해요.'
  r['confirmed_observations']={k:obs(k,v) for k,v in {'storage.sensory_change':{'new_particles':True},'method.current_routine':{'synthetic_recall_lot_match':False,'wants_resume_because_not_recalled':True}}.items()};r['kb_judgments']=[{'card_id':'B-S04','status':'hold','guidance':g}];r['allowed_evidence_refs']=['kb:B-S04@0.6.1'];c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-S04','comparison_spec':cards['B-S04']['comparison_spec'],'rationale':g}
 c['input_sha256']=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
tmp=p.with_suffix('.r2final.tmp')
with tmp.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
tmp.replace(p);print(hashlib.sha256(p.read_bytes()).hexdigest())
