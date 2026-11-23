"""Save round-two evidence and freeze input corrections before answers."""
import hashlib,json
from pathlib import Path
h=Path(__file__).resolve().parent;p=h/'additional_100_terra_part_b_inputs.json';q=h/'additional_100_terra_part_b.json';review=h/'reviews/additional_100_terra_part_b_codex_independent.jsonl';root=p.parents[7]
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='f49346c0012b853cb01eeffcce38f261fc93fde914a93a4c25035a8fbed7b061'
backup=root/'outputs/additional_100_terra/b/rev3';backup.mkdir(parents=True,exist_ok=True)
for src in (p,q,review):
 with (backup/src.name).open('xb') as f:f.write(src.read_bytes())
d=json.loads(raw.decode('utf-8'));kb=json.loads((root/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'));cards={x['id']:x for x in kb['baseline_cards']}
def obs(k,v):return {'variable_id':k,'state':'known','value':v,'source':'synthetic_fixture','confirmed_by_user':True}
for c in d['cases']:
 i=c['id'];r=c['request'];g=None
 if i=='syn-sol-0158':
  c['title']='다른 버전 SPF와 버전 연결이 미상인 표시';g='광범위 보호와 내수성 표시의 버전 연결은 미상이고 다른 버전의 SPF를 현재 제품 값으로 옮길 수 없어요.'
 if i=='syn-hold-0048':
  g='합성 회수 공지의 대상 로트에는 해당하지 않지만 새 이물이 보고되어 품질 확인 전 개별 재사용 권고를 보류해요.'
 if i=='syn-hold-0046':
  c['title']='합성 제품의 공식 처리 공지와 판매자 반송 요청 충돌';c['card_ids']=['B-Q06']
  r['confirmed_observations']={k:obs(k,v) for k,v in {'storage.sensory_change':{'contents_identity_unknown':True,'quality_concern':True},'commerce.end_of_use':{'seller_requested_return_for_testing':True,'official_current_notice_same_product':'반송하지 않고 안전 처리 및 공식 창구 확인','instruction_conflict':True}}.items()}
  g='내용물이 불명확한 합성 제품에 대해 판매자 반송 요청과 같은 현행 제품의 공식 처리 공지가 달라 개별 재사용 권고를 보류해요.'
  product={'product_id':'syn-terra-b46','version':'v1','synthetic_product':True,'status':'verified','label_guidance':'합성 제품의 현행 공식 처리 공지 예시: 반송하지 않고 안전 처리를 안내하며 공식 창구에 확인해요. 판매자는 검사 목적 반송을 별도로 요청했어요.','evidence_ref':'catalog:syn-terra-b46@v1'}
  r['product_evidence']=[product];r['allowed_evidence_refs']=['kb:B-Q06@0.6.1',product['evidence_ref']];r['kb_judgments']=[{'card_id':'B-Q06','status':'hold','guidance':g}];c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-Q06','comparison_spec':cards['B-Q06']['comparison_spec'],'rationale':g}
 if g is not None:
  r['kb_judgments'][0]['guidance']=g;c['judgment_basis']['rationale']=g;c['input_sha256']=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
d['schema_version']='additional-100-terra-part-b-inputs-round3';d['revision_note']='재감사 지적을 반영한 미검수 입력이에요.'
t=p.with_suffix('.round3.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
t.replace(p);print(hashlib.sha256(p.read_bytes()).hexdigest())
