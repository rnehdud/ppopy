"""Revise only the final failed answer while preserving its fixed input."""
import hashlib,json
from pathlib import Path
h=Path(__file__).resolve().parent;p=h/'additional_100_terra_part_b_inputs.json';q=h/'additional_100_terra_part_b.json';review=h/'reviews/additional_100_terra_part_b_codex_independent.jsonl';root=p.parents[7]
raw=p.read_bytes();expected='4d20e5e887a8cf3c9c4caea16a064c921586b840a1a11da2a6171a2eb6bd11e4';assert hashlib.sha256(raw).hexdigest()==expected
before=q.read_bytes();backup=root/'outputs/additional_100_terra/b/rev4';backup.mkdir(parents=True,exist_ok=True)
for src in (p,q,review):
 with (backup/src.name).open('xb') as f:f.write(src.read_bytes())
d=json.loads(before.decode('utf-8'));inp=json.loads(raw.decode('utf-8'));c=next(x for x in d['cases'] if x['id']=='syn-hold-0046');fixed=next(x for x in inp['cases'] if x['id']==c['id']);assert {k:v for k,v in c.items() if k!='answer'}==fixed
old_answer=c['answer'];c['answer']='### 개별 권고 보류 안내\n내용물이 불명확한 합성 제품의 개별 재사용 권고는 보류해요. [kb:B-Q06@0.6.1]\n\n### 필요한 다음 단계\n합성 현행 공식 안내는 반송하지 않고 안전 처리와 공식 창구 확인을 안내하지만, 판매자는 검사를 위한 반송을 요청했어요. [catalog:syn-terra-b46@v1] 두 안내의 대상과 현행성을 공식 창구에 확인해 주세요. 구체적인 반송·보관·처리 방법은 여기서 정하지 않아요.'
def digest(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
receipt={'row_id':c['id'],'input_file_sha256':expected,'old_answer_sha256':digest(old_answer),'new_answer_sha256':digest(c['answer']),'old_shard_sha256':hashlib.sha256(before).hexdigest()}
t=q.with_suffix('.round4.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
t.replace(q)
receipt['new_shard_sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
with (backup/'receipt.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(receipt,ensure_ascii=False))
