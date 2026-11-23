import hashlib,json
from pathlib import Path
h=Path(__file__).resolve().parent;p=h/'additional_100_terra_part_b_inputs.json';q=h/'additional_100_terra_part_b.json';raw=p.read_bytes();expected='4d20e5e887a8cf3c9c4caea16a064c921586b840a1a11da2a6171a2eb6bd11e4';assert hashlib.sha256(raw).hexdigest()==expected
d=json.loads(raw.decode('utf-8'));old={x['id']:x for x in json.loads(q.read_text(encoding='utf-8'))['cases']}
answers={
'syn-sol-0158':'### 핵심 안내\n광범위 보호와 내수성 표시가 보고됐지만 그 표시가 현재 버전에 해당하는지는 미상이에요. 다른 버전의 SPF를 현재 제품 값으로 옮길 수도 없어요. [kb:B-P01@0.6.1]\n\n### 근거 및 이유\n각 표시와 제품 버전의 연결을 확인해야 현재 후보의 기본 성능을 판단할 수 있어요. [kb:B-P01@0.6.1]\n\n### 확인이 필요한 한계\n현재 버전의 SPF와 다른 두 표시의 버전 연결은 확인되지 않았어요.',
'syn-sol-0161':'### 핵심 안내\n같은 제품에서 눈시림이 반복됐고, 눈가 사용 제한이 있는 해당 제품의 눈가 사용을 중단했다고 보고했어요. 대체 광보호 여부는 미상이에요. [kb:B-P06@0.6.1]\n\n### 근거 및 이유\n제품의 눈가 사용 제한과 실제 사용 조정, 대체 보호 여부를 구분해 살펴요. [kb:B-P06@0.6.1]\n\n### 확인이 필요한 한계\n눈시림의 원인과 대체 광보호의 확보 여부는 확정하지 않아요.',
'syn-hold-0046':'### 개별 권고 보류 안내\n내용물이 불명확한 합성 제품에 대해 판매자의 검사 목적 반송 요청과 같은 현행 제품의 공식 처리 공지가 충돌해 개별 재사용 권고를 보류해요. [kb:B-Q06@0.6.1] [catalog:syn-terra-b46@v1]\n\n### 필요한 다음 단계\n두 안내의 대상과 현행성을 공식 창구에 확인해 주세요. 확인되지 않은 반송이나 보관 방법을 여기서 정하지 않아요.',
'syn-hold-0047':'### 개별 권고 보류 안내\n새 냄새와 용기 손상이 보고돼 사용량 조정만으로 해결하는 개별 권고를 보류해요. [kb:B-S04@0.6.1]\n\n### 필요한 다음 단계\n관찰된 냄새와 용기 손상을 제조·판매처에 전달해 품질 확인을 요청해 주세요. 원인은 확정하지 않아요.',
'syn-hold-0048':'### 개별 권고 보류 안내\n합성 회수 공지의 대상 로트에는 해당하지 않지만 별도의 새 이물이 보고되어 품질 확인 전 개별 재사용 권고를 보류해요. [kb:B-S04@0.6.1]\n\n### 필요한 다음 단계\n해당 용기의 새 이물과 로트 정보를 제조·판매처에 전달해 품질을 확인해 주세요. 회수 비대상이라는 사실만으로 품질을 확정하지 않아요.'}
for c in d['cases']:
 i=c['id']
 if i=='syn-sol-0141':
  assert {k:v for k,v in old[i].items() if k!='answer'}==c
  c['answer']=old[i]['answer'].replace('없다는보고은','없다는 보고는')
  assert '없다는보고은' not in c['answer']
 elif i in answers:c['answer']=answers[i]
 else:
  assert {k:v for k,v in old[i].items() if k!='answer'}==c
  c['answer']=old[i]['answer']
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
t=q.with_suffix('.round3.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
t.replace(q);print(hashlib.sha256(q.read_bytes()).hexdigest())
