import hashlib,json
from pathlib import Path
h=Path(__file__).resolve().parent;p=h/'additional_100_terra_part_b_inputs.json';q=h/'additional_100_terra_part_b.json';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='f49346c0012b853cb01eeffcce38f261fc93fde914a93a4c25035a8fbed7b061'
d=json.loads(raw.decode('utf-8'));old={x['id']:x for x in json.loads(q.read_text(encoding='utf-8'))['cases']}
for c in d['cases']:
 i=c['id']
 if i=='syn-sol-0160':
  c['answer']='### 핵심 안내\n새 야외 후보는 광범위 보호와 내수성 표시가 있지만 SPF 15로 확인돼 기본 SPF 기준과 차이가 있어요. [kb:B-P01@0.6.1]\n\n### 근거 및 이유\n일반 선택 안내에서는 SPF 30 이상과 광범위 보호 및 내수성을 각각 살펴요. [ref:S16]\n\n### 확인이 필요한 한계\n이 표시는 개인의 실제 보호율이나 사용 적합성을 측정한 결과가 아니에요.'
 else:
  assert {k:v for k,v in old[i].items() if k!='answer'}==c
  c['answer']=old[i]['answer']
assert hashlib.sha256(p.read_bytes()).hexdigest()=='f49346c0012b853cb01eeffcce38f261fc93fde914a93a4c25035a8fbed7b061'
t=q.with_suffix('.r2_0160.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
t.replace(q);print(hashlib.sha256(q.read_bytes()).hexdigest())
