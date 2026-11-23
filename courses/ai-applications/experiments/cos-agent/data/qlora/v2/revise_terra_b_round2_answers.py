"""Regenerate only failed answers against the separately frozen revised inputs."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;p=HERE/'additional_100_terra_part_b_inputs.json';target=HERE/'additional_100_terra_part_b.json'
expected='9cf10f7a3132210ac78c6b6722babad6c86439ecb8f3d46f951c416e3aab6456'
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected
d=json.loads(raw.decode('utf-8'));before=json.loads(target.read_text(encoding='utf-8'))
old={c['id']:c for c in before['cases']}
review=HERE/'reviews/additional_100_terra_part_b_codex_independent.jsonl'
failed={x['row_id'] for x in (json.loads(line) for line in review.read_text(encoding='utf-8').splitlines()) if x['decision']=='FAIL'}
assert len(failed)==22
limits={
'syn-sol-0141':'물과 수건 접촉이 없다는 보고는 다른 손실 계기나 개인의 실제 보호율을 확정하지 않아요.',
'syn-sol-0142':'두 번역의 숫자 중 어느 것이 현재 제품에 해당하는지는 미상이에요.',
'syn-sol-0143':'실제 야외 활동과 실제 재도포 여부는 확인되지 않았어요.',
'syn-sol-0144':'같은 제품이라는 사실만 확인됐고 매번 같은 방식으로 사용했는지는 미상이에요.',
'syn-sol-0145':'제품 지침에 따른 부위 제한을 일반적인 누락과 구분해요.',
'syn-sol-0147':'내수성 시간은 SPF 숫자가 아니며, 수건 접촉 후 재도포 면제를 뜻하지 않아요.',
'syn-sol-0148':'이전 야외 구간의 재도포 여부는 미상이므로 당시 행동을 단정하지 않아요.',
'syn-sol-0149':'표시 부재는 시험된 내수성 실패나 개인의 실제 보호 결과가 아니에요.',
'syn-sol-0150':'색인지 냄새인지와 기존 제형 대비 변화인지는 확인이 필요해요.',
'syn-sol-0151':'보이는 숫자의 의미가 확인되기 전에는 어떤 표시 값으로도 바꾸지 않아요.',
'syn-sol-0152':'현행 용기의 SPF는 미상이며 다른 버전의 수치를 대신 사용하지 않아요.',
'syn-sol-0153':'기록들이 같은 외출을 다루는지도 실제 재도포 여부도 아직 미상이에요.',
'syn-sol-0158':'현재 버전의 SPF는 미상이고 다른 버전의 값을 옮길 수 없어요.',
'syn-sol-0160':'해당 제품의 구체적 재도포 지침이나 실제 보호 수준은 확인되지 않았어요.',
'syn-sol-0161':'눈가를 피한 사실만으로 대체 보호 여부나 개인 증상의 원인을 확정하지 않아요.',
'syn-sol-0164':'친구의 사용 행동은 본인의 도포 상태를 확인해 주지 않아요.'}
for c in d['cases']:
 i=c['id'];r=c['request'];j=r['kb_judgments'][0];ref='kb:'+j['card_id']+'@0.6.1'
 assert hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()==c['input_sha256']
 if i not in failed:
  assert {k:v for k,v in old[i].items() if k!='answer'}==c
  c['answer']=old[i]['answer'];continue
 if c['mode']=='solution':
  if i not in limits: raise ValueError(i)
  c['answer']='### 핵심 안내\n'+j['guidance']+' ['+ref+']\n\n### 근거 및 이유\n확인된 관찰과 해당 비교 조건을 구분해 살펴요. ['+ref+']\n\n### 확인이 필요한 한계\n'+limits[i]
 else:
  if i in {'syn-hold-0044','syn-hold-0046'}:
   next_step='통증 관련 기록의 차이와 지속되는 불편을 의료 전문가에게 설명해 확인해 주세요. 원인은 여기서 확정하지 않아요.'
  elif i in {'syn-hold-0045','syn-hold-0047','syn-hold-0048','syn-hold-0049'}:
   next_step='관찰된 품질 이상과 해당 용기 정보를 제조·판매처에 전달해 확인해 주세요. 확인 전에는 실제 품질이나 원인을 확정할 수 없어요.'
  else: raise ValueError(i)
  c['answer']='### 개별 권고 보류 안내\n'+j['guidance']+' ['+ref+']\n\n### 필요한 다음 단계\n'+next_step
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
tmp=target.with_suffix('.round2.tmp')
with tmp.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
tmp.replace(target)
print('revised',len(failed),'unchanged',len(d['cases'])-len(failed),'sha256',hashlib.sha256(target.read_bytes()).hexdigest())
