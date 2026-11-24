"""검수 승인과 구분하여 새 합성 후보 200행을 조립해요. 기존 파일을 바꾸지 않아요."""
from collections import Counter
import csv,io,json,re
import additional_200_terra2_support as s
V=s.V;OUT=s.OUT;NAME='additional_200_terra2'
def save(path,data):
 if path.exists() and path.read_bytes()!=data:
  archived=OUT/'superseded'/(path.name+'.'+s.common.sha(path)+'.previous');archived.parent.mkdir(parents=True,exist_ok=True)
  if not archived.exists():archived.write_bytes(path.read_bytes())
 path.write_bytes(data)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 baseline_path=OUT/'baseline.json'
 if not baseline_path.exists():baseline_path=V/(NAME+'_plan.json')
 baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
 for rel,digest in baseline['protected_hashes'].items():assert s.common.sha(s.ROOT/rel)==digest,rel
 human=V/(NAME+'_human_review.csv')
 if human.exists():
  with human.open(encoding='utf-8-sig',newline='') as f:
   assert all(r['human_review']=='unreviewed' and not any(r[k] for k in ('reviewer','reviewed_at','notes')) for r in csv.DictReader(f))
 cases=[]
 for part in 'abc':
  frozen=json.loads((V/f'{NAME}_part_{part}_inputs.json').read_text(encoding='utf-8'))
  authored=json.loads((V/f'{NAME}_part_{part}.json').read_text(encoding='utf-8'))
  byid={c['id']:c for c in frozen['cases']}
  assert len(byid)==len(authored['cases'])
  for c in authored['cases']:
   assert {k:v for k,v in c.items() if k!='answer'}==byid[c['id']],c['id']
   cases.append(c)
 ids={f'syn-sol-{i:04d}' for i in range(499,653)}|{f'syn-hold-{i:04d}' for i in range(153,199)}
 assert len(cases)==200 and {c['id'] for c in cases}==ids
 assert Counter(c['mode'] for c in cases)=={'solution':154,'hold':46}
 assert {c['split'] for c in cases} <= {'train','val_internal'}
 rows=[];hashes={};report=['# 신규 합성 개발 후보 200행','',
  '기존 648행은 변경하지 않았어요. 154 solution·46 hold를 추가한 합계는 848행이에요.',
  '`development_preview`, `production_enabled=false`를 유지해요. 실제 사용자 자료·임상 정답·엔진 실행 결과가 아니에요.',
  '입력을 먼저 동결하고 답변을 작성했어요. 현재 내부 감사 기록은 내용 해시로 연결해요. 다른 모델 계열 검수·사람 승인과 구분해요.',
  '고정 파일럿 승인 게이트를 통과하거나 공식 900행을 완성했다는 뜻이 아니에요. 저장 출처 청크는 등록 범위의 요약이에요.','']
 for c in sorted(cases,key=lambda c:c['id']):
  rid=c['id'];q=c['request'];a=c['answer'];assert c['input_sha256']==s.digest(q),rid
  assert all(e['raw_span'] in c['scenario_raw'] and e['connection'] for e in c['atom_evidence']),rid
  assert {e['variable_id'] for e in c['atom_evidence']}==set(q['confirmed_observations']),rid
  assert c['novelty_note'] and isinstance(c['closest_existing_ids'],list),rid
  assert not any(j['guidance'].strip() in a for j in q['kb_judgments'] if j['guidance'].strip()),rid
  assert not re.search(r'[\u3040-\u30ff]|\ufffd|\?\?',json.dumps(c,ensure_ascii=False)),rid
  ctx=q['confirmed_observations'].get('constraints.decision_context')
  if ctx and ctx['state']=='known':assert ctx['value'] in ('current_routine_review','new_product_selection'),rid
  for key,slot in q['confirmed_observations'].items():
   if slot['state']!='known':assert slot['value'] is None,rid
   assert key in s.VARIABLES
  for ch in q['rag_chunks']:
   if re.search('[\uac00-\ud7a3]',ch['text']):assert 2<=len(re.split(r'(?<=[.!?])\s+',ch['text'].strip()))<=4,(rid,ch['text'])
  expected=['### 핵심 안내','### 근거 및 이유','### 확인이 필요한 한계'] if c['mode']=='solution' else ['### 개별 권고 보류 안내','### 필요한 다음 단계']
  assert [x for x in a.splitlines() if x.startswith('### ')]==expected,rid
  s.assert_input(q)
  req=s.common.validator.SLMRequest.model_validate(q)
  row={k:c[k] for k in s.common.ROW_KEYS}
  row['messages']=[{'role':'system','content':s.common.validator.SYSTEM_PROMPT_SOLUTION_HOLD},{'role':'user','content':json.dumps(q,ensure_ascii=False)},{'role':'assistant','content':a}]
  row.update(allowed_evidence_refs=q['allowed_evidence_refs'],distractor_refs=q['distractor_refs'],provenance={'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'generator_model':'gpt-6.1-terra','critic_model':None,'critic_status':'unreviewed','human_review':'unreviewed'})
  rows.append(row)
  hashes[rid]=s.common.validator.compute_row_content_sha256(req,a,card_ids=c['card_ids'],chunk_origins=c['chunk_origins'],is_hard_negative=c['is_hard_negative'],hard_negative_type=c['hard_negative_type'])
  report+=['## '+rid+' — '+c['title'],'','- 내용 해시: `'+hashes[rid]+'`','- 사람 검수: **미검수**','- 새 조건과 가까운 기존 사례: '+c['novelty_note']+' / '+', '.join(c['closest_existing_ids']),'','### 설계한 시나리오 raw','',c['scenario_raw'],'','### 입력 원문','','```json',json.dumps(q,ensure_ascii=False,indent=2),'```','','### 원문과 슬롯 연결','','```json',json.dumps(c['atom_evidence'],ensure_ascii=False,indent=2),'```','','### 응답 초안 — 미승인','',a,'']
 plan={'schema_version':'additional-200-terra2-plan-v1','mode':'development_preview','production_enabled':False,'generator_model':'gpt-6.1-terra','human_review':'unreviewed','base_commit':baseline['base_commit'],'protected_hashes':baseline['protected_hashes'],'scope':'사용자가 추가 요청한 합성 개발 후보예요. 공식 파일럿 승인·900행 본 데이터 착수·학습 완료가 아니에요.','cases':[{k:v for k,v in c.items() if k!='answer'} for c in cases]}
 save(V/(NAME+'_plan.json'),(json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
 save(V/(NAME+'.jsonl'),(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)).encode('utf-8'))
 save(V/(NAME+'_review.md'),('\n'.join(report).rstrip()+'\n').encode('utf-8'))
 stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=['row_id','content_sha256','pilot_bucket','reviewer','reviewed_at','human_review','notes'],lineterminator='\n');w.writeheader()
 for c in cases:w.writerow({'row_id':c['id'],'content_sha256':hashes[c['id']],'pilot_bucket':c['pilot_bucket'],'reviewer':'','reviewed_at':'','human_review':'unreviewed','notes':''})
 save(human,stream.getvalue().encode('utf-8-sig'))
 s.dump(OUT/'generation_receipt.json',{'new_rows':200,'existing_rows':648,'total_rows':848,'modes':dict(Counter(c['mode'] for c in cases)),'splits':dict(Counter(c['split'] for c in cases)),'content_sha256':hashes,'dataset_sha256':s.common.sha(V/(NAME+'.jsonl')),'human_approved':0,'external_cross_family_gate_satisfied':False})
 print(json.dumps({'new_rows':200,'total_rows':848}))
if __name__=='__main__':main()
