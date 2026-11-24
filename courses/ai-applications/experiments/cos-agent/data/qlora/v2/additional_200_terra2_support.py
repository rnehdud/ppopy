"""새 합성 후보의 출처 복사·입력 동결만 지원해요. 정답·검수 승인은 만들지 않아요."""
from pathlib import Path
import sys,json,hashlib
import build_additional_24 as common
V=Path(__file__).resolve().parent;COS=V.parents[2];ROOT=COS.parents[3]
OUT=COS/'outputs/additional_200_terra2'
KB=json.loads((ROOT/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
CARDS={c['id']:c for c in KB['baseline_cards']}
SOURCES={c['id']:c for c in KB['source_registry']}
VARIABLES={c['id']:c for c in KB['variables']}
def digest(v):return hashlib.sha256(common.canonical(v).encode('utf-8')).hexdigest()
def reference_inventory():
 names=['pilot_24','additional_24','additional_100','additional_100_terra','additional_100_terra2','additional_100_terra3','additional_200_terra']
 result={}
 for name in names:
  for line in (V/(name+'.jsonl')).read_text(encoding='utf-8').splitlines():
   r=json.loads(line);q=json.loads(r['messages'][1]['content'])
   result[r['id']]={k:r[k] for k in ('id','scenario_family_id','group_id','split','card_ids')}|{'observations':q['confirmed_observations'],'judgments':q['kb_judgments'],'answer':r['messages'][2]['content']}
 for p in V.glob('additional_200_terra2_part_?.json'):
  for c in json.loads(p.read_text(encoding='utf-8'))['cases']:
   result[c['id']]={k:c[k] for k in ('id','scenario_family_id','group_id','split','card_ids')}|{'observations':c['request']['confirmed_observations'],'judgments':c['request']['kb_judgments'],'answer':c['answer']}
 return result
def dump(path,obj):path.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def assert_input(req):
 common.validator.SLMRequest.model_validate(req)
 for key,o in req['confirmed_observations'].items():
  assert key in VARIABLES,key
  if o['state']=='known':
   assert common.validator._is_valid_kb_value(VARIABLES[key]['value_type'],o['value']),(key,VARIABLES[key]['value_type'],o['value'])
  else:assert o['value'] is None,key
def slot(key,value=None,state='known'):
 assert key in VARIABLES,key
 return {'variable_id':key,'state':state,'value':value,'source':'synthetic_fixture','confirmed_by_user':state=='known'}
def chunk(sid,text,probe=False):
 s=SOURCES[sid]
 return {'evidence_ref':'ref:'+sid,'text':text,'scope':'non_clinical_only' if probe else 'general_skincare_practice','source_url':s['url'],**{k:s[k] for k in ('locator','checked_on','limitations')}}
def case(rid,title,values,judgments,source_chunks,*,raw,atom_evidence,novelty,closest=(),unknown=(),declined=(),products=(),probe_chunks=(),hn=None,split='train',family=None,domains=()):
 mode='hold' if rid.startswith('syn-hold-') else 'solution'
 observations={k:slot(k,v) for k,v in values.items()}
 observations.update({k:slot(k,None,'unknown') for k in unknown})
 observations.update({k:slot(k,None,'declined') for k in declined})
 ctx=observations.get('constraints.decision_context')
 if ctx and ctx['state']=='known':assert ctx['value'] in ('new_product_selection','current_routine_review')
 assert all(e['raw_span'] in raw and e['connection'] for e in atom_evidence),rid
 assert {e['variable_id'] for e in atom_evidence}==set(observations),rid
 cards=[j['card_id'] for j in judgments]
 assert all(c in CARDS for c in cards)
 chunks=[chunk(s,t) for s,t in source_chunks]+[chunk(s,t,True) for s,t in probe_chunks]
 assert mode!='hold' or not chunks
 refs=['kb:'+c+'@0.6.1' for c in cards]+['ref:'+s for s,t in source_chunks]+[p['evidence_ref'] for p in products if p['status']=='verified']
 req={'mode':mode,'confirmed_observations':observations,'kb_judgments':judgments,'product_evidence':list(products),'rag_chunks':chunks,'allowed_evidence_refs':refs,'distractor_refs':['ref:'+s for s,t in probe_chunks]}
 common.validator.SLMRequest.model_validate(req)
 family=family or 'terra200v2-family-'+rid
 bucket='hold' if mode=='hold' else 'distractor_or_defense' if hn else 'unknown_or_version' if any(j['status']=='unknown' for j in judgments) else 'normal_guidance'
 return {'id':rid,'title':title,'scenario_id':'terra200v2-scenario-'+rid,'group_id':family,'scenario_family_id':family,'split':split,'mode':mode,'pilot_bucket':bucket,'domains':list(domains),'card_ids':cards,'is_hard_negative':hn is not None,'hard_negative_type':hn,'chunk_origins':{'ref:'+s:'kb_source_summary' for s,t in source_chunks}|{'ref:'+s:'synthetic_defense_probe' for s,t in probe_chunks},'request':req,'input_sha256':digest(req),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','cards':{cid:CARDS[cid]['comparison_spec'] for cid in cards},'rationale':' / '.join(j['guidance'] for j in judgments)},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'새 합성 개발 후보이며 실제 사용자·임상 결과·엔진 실행 결과가 아니에요.','generator_model':'gpt-6.1-terra','scenario_raw':raw,'atom_evidence':atom_evidence,'novelty_note':novelty,'closest_existing_ids':list(closest)}
def freeze(part,cases):
 path=V/f'additional_200_terra2_part_{part}_inputs.json'
 assert not path.exists(),'동결 입력 변경은 이전 판본 보존과 재검수 절차로만 해요.'
 assert all('answer' not in c for c in cases)
 for c in cases:assert_input(c['request'])
 dump(path,{'mode':'development_preview','production_enabled':False,'generator_model':'gpt-6.1-terra','human_review':'unreviewed','cases':cases})
def answers(part,byid):
 src=V/f'additional_200_terra2_part_{part}_inputs.json';obj=json.loads(src.read_text(encoding='utf-8'))
 assert set(byid)=={c['id'] for c in obj['cases']}
 for c in obj['cases']:
  a=byid[c['id']]
  expected=['### 핵심 안내','### 근거 및 이유','### 확인이 필요한 한계'] if c['mode']=='solution' else ['### 개별 권고 보류 안내','### 필요한 다음 단계']
  assert [line for line in a.splitlines() if line.startswith('### ')]==expected,c['id']
  assert not any(j['guidance'].strip() in a for j in c['request']['kb_judgments'] if j['guidance'].strip()),c['id']
  c['answer']=a
 dump(V/f'additional_200_terra2_part_{part}.json',obj)
