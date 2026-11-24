"""사람이 아닌 독립 담당자의 실제 행별 감사를 내용 해시로 연결해요."""
import json,re
from collections import Counter
import additional_200_terra2_support as s
V=s.V;OUT=s.OUT;NAME='additional_200_terra2'
RULES={'R1_CITATION','R2_CLINICAL','R3_UNKNOWN_VERSION','R4_HOLD_LEAK','R5_INPUT_JUDGMENT','R6_FORMAT_TONE'}
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
def save(p,records):
 data=(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records)).encode('utf-8')
 if p.exists() and p.read_bytes()!=data:
  prev=OUT/'superseded'/(p.name+'.'+s.common.sha(p)+'.previous');prev.parent.mkdir(parents=True,exist_ok=True)
  if not prev.exists():prev.write_bytes(p.read_bytes())
 p.write_bytes(data)
def main():
 rows=jl(V/(NAME+'.jsonl'));byid={r['id']:r for r in rows};latest={};history=[];reviewed_cases={};reviewed_neighbors={}
 references=s.reference_inventory()
 authored={c['id']:c for part in 'abc' for c in json.loads((V/f'{NAME}_part_{part}.json').read_text(encoding='utf-8'))['cases']}
 for part in 'abc':
  files=sorted((p for p in OUT.glob(f'critic_{part}_round*.jsonl') if re.fullmatch(r'critic_'+part+r'_round[0-9]+\.jsonl',p.name)),key=lambda p:int(p.stem.split('round')[-1]))
  assert files,part
  for p in files:
   records=jl(p);number=int(p.stem.split('round')[-1])
   packet=json.loads((OUT/f'review_packet_{part}_round{number}.json').read_text(encoding='utf-8'))
   packet_cases={x['case']['id']:x for x in packet}
   assert {r['row_id'] for r in records}==set(packet_cases),p.name
   for r in records:
    assert r['content_sha256']==packet_cases[r['row_id']]['content_sha256']
    reviewed_cases[r['row_id']]=packet_cases[r['row_id']]['case']
    reviewed_neighbors[r['row_id']]=packet_cases[r['row_id']]['closest_existing_rows']
   preliminary=part=='a' and number==1
   shared=V/'reviews'/(NAME+'_'+p.stem+('_preliminary_raw' if preliminary else '')+'.jsonl')
   save(shared,records)
   history.append({'file':shared.name,'sha256':s.common.sha(shared),'source_file':'outputs/additional_200_terra2/'+p.name,'source_sha256':s.common.sha(p),'counts':dict(Counter(r['decision'] for r in records)),'formatting_note':'원본 레코드의 판정·근거·발췌는 그대로 두고 공유 JSONL을 UTF-8/LF로 저장했어요. 원본 바이트 해시는 source_sha256로 구분해요.','audit_quality':'incomplete_preliminary' if preliminary else 'case_specific_internal_review','scope':'A 첫 기록은 문자 손상 복구 뒤 영어 공통 근거만 남은 불완전 초안이라 완결된 감사로 세지 않아요. 전체 67행을 다음 라운드에서 한국어 원문 연결로 다시 검수했어요.' if preliminary else '당시 패킷 내용에 대한 실제 내부 감사 기록이에요.'})
   for r in records:latest[r['row_id']]=r
 assert len(latest)==200 and set(latest)==set(byid)
 for rid,r in latest.items():
  row=byid[rid];q=s.common.validator.SLMRequest.model_validate_json(row['messages'][1]['content'])
  actual=s.common.validator.compute_row_content_sha256(q,row['messages'][2]['content'],card_ids=row['card_ids'],chunk_origins=row['chunk_origins'],is_hard_negative=row['is_hard_negative'],hard_negative_type=row['hard_negative_type'])
  assert r['content_sha256']==actual,rid
  assert s.digest(reviewed_cases[rid])==s.digest(authored[rid]),rid
  neighbors=[references[x] for x in authored[rid]['closest_existing_ids']]
  assert s.digest(reviewed_neighbors[rid])==s.digest(neighbors),rid+' 가까운 사례가 감사 후 변경됐어요.'
  r['reviewed_case_sha256']=s.digest(reviewed_cases[rid])
  r['reviewed_neighbors_sha256']=s.digest(neighbors)
  assert r['critic_model']=='gpt-6.1-terra' and r['review_kind']=='codex_same_family_independent'
  assert r['external_cross_family_gate_satisfied'] is False and r['human_review_performed'] is False
  assert r['decision']=='PASS' and set(r['rule_checks'])==RULES,rid
  assert all(v['decision']=='PASS' and v['grounds'] for v in r['rule_checks'].values()),rid
  assert r['raw_evidence'] and all(e['raw'] and e['connection'] for e in r['raw_evidence']),rid
  assert '??' not in json.dumps(r,ensure_ascii=False) and '\ufffd' not in json.dumps(r)
 save(V/'reviews'/(NAME+'_codex_independent.jsonl'),[latest[rid] for rid in sorted(latest)])
 summary={'dataset':NAME+'.jsonl','dataset_sha256':s.common.sha(V/(NAME+'.jsonl')),'total_rows':200,'pass_count':200,'fail_count':0,'critic_model':'gpt-6.1-terra','review_kind':'codex_same_family_independent','external_cross_family_gate_satisfied':False,'human_review_performed':False,'review_history':history,'scope':'작성 담당과 다른 담당이 raw·입력·응답·실제 카드·등록 청크를 대조한 내부 감사예요. 자동 검사는 판정을 생성하지 않아요. 이전 FAIL은 이력에 보존해요.'}
 s.dump(V/'reviews'/(NAME+'_codex_independent.summary.json'),summary)
 print(json.dumps({'current_pass':200,'history_files':len(history)}))
if __name__=='__main__':main()
