"""자외선·보관 개별 작성 사례를 공식 계약과 청크로 조립한다. 검수 승인은 만들지 않는다."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parents[1]
COS=HERE.parents[3]
sys.path.insert(0,str(COS))
from beauty_agent.v3_contracts import SLMRequest
from scripts.validate_qlora_dataset import SYSTEM_PROMPT_SOLUTION_HOLD, compute_row_content_sha256

spec=importlib.util.spec_from_file_location('sun_authored',Path(__file__).with_name('sun_storage_build.py'))
src=importlib.util.module_from_spec(spec)
spec.loader.exec_module(src)
reason_spec=importlib.util.spec_from_file_location('sun_reasons',Path(__file__).with_name('sun_storage_case_reasons.py'))
reason_src=importlib.util.module_from_spec(reason_spec)
reason_spec.loader.exec_module(reason_src)

PRODUCT_FACT_KEYS={
 'sun.spf_seen','sun.compared_spf','sun.label_claim','sun.product_warning',
 'sun.delivery_type','sun.ingredient_name','sun.ingredient_percent_confirmed',
 'sun.aha_percent_confirmed','sun.ph_confirmed','sun.label_country',
 'sun.water_resistance_confirmed','method.ingredient','method.ingredient_name',
 'method.product_type','method.rinse_status','method.product_use',
 'storage.paraffin_claim','storage.packaging_claim','storage.packaging',
 'storage.special_label','storage.label_claim','storage.label_type',
 'storage.preservative_information','storage.formula_type','storage.manufacture_date',
 'storage.label_observation',
}

def split_product_facts(facts,rid):
 product_facts={k:v for k,v in facts.items() if k in PRODUCT_FACT_KEYS}
 observations={k:v for k,v in facts.items() if k not in PRODUCT_FACT_KEYS}
 compared=product_facts.pop('sun.compared_spf',None)
 if compared is not None:
  products=[]
  for n,spf in enumerate(compared,1):
   pid=f'a900-sun-fixture-{rid.rsplit("-",1)[1]}-comparison-{n}'
   products.append({'product_id':pid,'version':'fixture-1','synthetic_product':True,'status':'verified','label_guidance':f'신규 합성 비교 제품 {n}: SPF {spf}','confirmed_label_facts':{'sun.spf_seen':spf},'evidence_ref':f'catalog:{pid}@fixture-1'})
  assert not product_facts
  return observations,products
 if not product_facts: return observations,[]
 pid='a900-sun-fixture-'+rid.rsplit('-',1)[1]
 # 이 레코드는 실제 상용품의 라벨이 아니라 입력을 먼저 설계한 신규 합성 표시다.
 product={'product_id':pid,'version':'fixture-1','synthetic_product':True,
          'status':'unknown' if all(v is None for v in product_facts.values()) else 'verified',
          'label_guidance':'신규 합성 제품 표시 예시: '+json.dumps(product_facts,ensure_ascii=False),
          'confirmed_label_facts':product_facts,
          'evidence_ref':f'catalog:{pid}@fixture-1'}
 return observations,[product]

def slot(key,value):
 return {'variable_id':key,'state':'unknown' if value is None else 'known','value':value,'source':'user_report','confirmed_by_user':value is not None}

def write_jsonl(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8',newline='\n')

def main():
 assert len(src.FAMILIES)==46,len(src.FAMILIES)
 assert len(src.HOLD_FAMILIES)==14,len(src.HOLD_FAMILIES)
 solutions=[]; holds=[]; traces=[]
 known_val={'flammable-sunscreen-location','uncovered-dynamic-map'}
 for fam in src.FAMILIES:
  for i,(facts,action,limit) in enumerate(fam['cases']):
   rid=f"syn-sol-{1151+len(solutions):04d}"
   split='val_internal' if fam['name'] in known_val else 'train'
   ref=fam['ref']; chunk=src.POOL[ref]
   distractor=src.POOL[['ref:cleansing-002','ref:cleansing-030','ref:moisturizing-017'][(len(solutions)+i)%3]]
   # Clinical-restraint cases actually discuss available study design/results.
   # Ordinary weather/SPF misconceptions are NOT symptom negation hard negatives.
   hn=fam['hn'] if fam['hn']=='clinical_restraint' else None
   if any(v is None for v in facts.values()): hn='version_mismatch_or_unknown'
   use_distractor=hn is None and (i%2==0 or fam['hn']=='rag_distractor_ignore')
   if use_distractor: hn='rag_distractor_ignore'
   observations,products=split_product_facts(facts,rid)
   extra_refs=['ref:sun_protection-011'] if fam['name']=='fda-exposure-schedule' and i in (0,1,4) else []
   req=SLMRequest(mode='solution',confirmed_observations={k:slot(k,v) for k,v in observations.items()},product_evidence=products,rag_chunks=[chunk]+[src.POOL[x] for x in extra_refs]+([distractor] if use_distractor else []),allowed_evidence_refs=[ref]+extra_refs+[p['evidence_ref'] for p in products],distractor_refs=[distractor['evidence_ref']] if use_distractor else [])
   reason=reason_src.REASONS[fam['name']][i]
   action_refs=[p['evidence_ref'] for p in products]+extra_refs
   product_citation=' '+''.join('['+x+']' for x in action_refs) if action_refs else ''
   answer=f"### 핵심 안내\n{action}{product_citation}\n\n### 근거 및 이유\n{reason} [{ref}].\n\n### 확인이 필요한 한계\n{limit}"
   row=make_row(rid,split,'solution',fam['name'],i,req,answer,hn)
   solutions.append(row)
   traces.append(trace(row,facts,action,reason,limit,chunk))
 for fam in src.HOLD_FAMILIES:
  for i,(facts,reason,nextstep) in enumerate(fam['cases']):
   rid=f"syn-hold-{351+len(holds):04d}"
   req=SLMRequest(mode='hold',confirmed_observations={k:slot(k,v) for k,v in facts.items()})
   answer=f"### 개별 권고 보류 안내\n{reason}\n\n### 필요한 다음 단계\n{nextstep}"
   row=make_row(rid,'val_internal' if fam['val'] else 'train','hold',fam['name'],i,req,answer,None)
   holds.append(row); traces.append(trace(row,facts,reason,nextstep,None,None))
 assert len(solutions)==230 and len(holds)==70
 for b in range(10):
  batch=solutions[b*23:(b+1)*23]+holds[b*7:(b+1)*7]
  assert len(batch)==30
  write_jsonl(HERE/'batches'/f'sun_storage_{b+1:02d}.jsonl',batch)
 write_jsonl(HERE/'authoring'/'sun_storage_fact_trace.jsonl',traces)
 print(json.dumps({'solution':len(solutions),'hold':len(holds),'val':sum(r['split']=='val_internal' for r in solutions+holds),'hard_negative':sum(r['is_hard_negative'] for r in solutions),'english':sum(len(re.findall(r'[A-Za-z]{2,}',src.POOL[r['allowed_evidence_refs'][0]]['text']))>=8 for r in solutions)},ensure_ascii=False))

def make_row(rid,split,mode,family,i,req,answer,hn):
 domain='sun_protection' if mode=='solution' and any('sun_protection' in x.evidence_ref for x in req.rag_chunks if x.evidence_ref in req.allowed_evidence_refs) else 'general_safety'
 return {'id':rid,'scenario_id':f'a900-sun-{family}-{i+1}','group_id':f'a900-sun-group-{family}','scenario_family_id':f'a900-sun-family-{family}','scenario_concept':family,'split':split,'mode':mode,'domains':[domain],'card_ids':[],'is_hard_negative':hn is not None,'hard_negative_type':hn,'chunk_origins':{x.evidence_ref:'reference_excerpt' for x in req.rag_chunks},'messages':[{'role':'system','content':SYSTEM_PROMPT_SOLUTION_HOLD},{'role':'user','content':req.model_dump_json()},{'role':'assistant','content':answer}],'allowed_evidence_refs':req.allowed_evidence_refs,'distractor_refs':req.distractor_refs,'provenance':{'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'generator_model':'gpt-6','critic_model':None,'critic_status':'unreviewed','human_review':'unreviewed'},'runtime_invariants':{'mode':'development_preview','production_enabled':False,'requires_approval':True,'saved':False}}

def trace(row,facts,action,reason,limit,chunk):
 req=SLMRequest.model_validate_json(row['messages'][1]['content'])
 return {'row_id':row['id'],'scenario_concept':row['scenario_concept'],'family_id':row['scenario_family_id'],'split':row['split'],'authoring_order':'confirmed_facts_then_response','synthetic_confirmed_facts_raw':facts,'input_raw':req.model_dump(mode='json'),'assistant_raw':row['messages'][2]['content'],'content_sha256':compute_row_content_sha256(req,row['messages'][2]['content'],card_ids=[],chunk_origins=row['chunk_origins'],is_hard_negative=row['is_hard_negative'],hard_negative_type=row['hard_negative_type']),'claims':[{'claim_raw':action,'basis_kind':'actual_request_observations','basis_raw':facts,'connection':'개별 안내의 사용자 사실은 이 입력 슬롯의 확인값으로 제한했어요. 미확인 슬롯은 값이 없음을 유지해요.'},{'claim_raw':reason,'basis_kind':'allowed_reference_chunk' if chunk else 'confirmed_hold_condition','basis_raw':chunk if chunk else facts,'connection':'일반 원리는 해당 청크의 범위에서 설명하고 사용자에게 실제 발생한 결과와 구분해요.' if chunk else '확인된 문제와 제품·의료 확인 주체만 연결하며 개별 사용 지시는 만들지 않아요.'}],'scope_limit_raw':limit,'review_status':'unreviewed','human_review':'unreviewed'}

if __name__=='__main__': main()
