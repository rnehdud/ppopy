"""Revise twelve answers after the input-only revision was frozen."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; P=H/'additional_100_terra_part_a_inputs.json'; O=H/'additional_100_terra_part_a.json'
if hashlib.sha256(P.read_bytes()).hexdigest()!='8e3e43114d8b615e86595904d0f9536fb5f437d71871b3b6710ff86dcfeb22c0': raise RuntimeError('input changed')
if hashlib.sha256(O.read_bytes()).hexdigest()!='bd421c73158479d549266dca2e4b0afebf29c6b7e7e8353383ce647a510e953d': raise RuntimeError('answer revision changed')
D=json.loads(P.read_text(encoding='utf-8')); old={c['id']:c for c in json.loads(O.read_text(encoding='utf-8'))['cases']}
S={
115:('원제품에 지침 없이 물을 넣은 취급을 검토해요.','임의 첨가와 제품별 지시에 따른 사용을 구분해요.','물 첨가만으로 오염이나 감염을 확정할 수 없어요.'),
117:('반복된 손 제품 불편을 기록하고 위생과 보습 맥락을 함께 확인해요.','불편이 반복됐어도 그 뒤 사용을 계속했는지는 확인되지 않았어요.','그 사실만으로 사용 방식의 차이나 불편의 원인을 확정하지 않아요.'),
120:('면도 도구를 헹구지 않은 사실과 건조 보관을 따로 살펴요.','헹굼이 없었다는 기록은 다른 세척의 수행 여부를 알려주지 않아요.','젖고 오염된 상태로 계속 사용했는지도 미확인이에요.'),
126:('동일 용기의 헹굼 지시 기록이 충돌해 적용할 지시를 확인해요.','물 헹굼이 필요하다는 기록과 필요 없다는 기록이 함께 있어요.','어느 지시가 맞는지 미상이라 실제 사용을 이탈로 확정하지 않아요.'),
128:('손가락 이외의 세안 도구를 사용한 사실을 기본 방법과 구분해요.','도구 사용 자체와 강한 마찰 여부는 서로 다른 관찰이에요.','마찰 정도와 도구의 건조 보관은 확인되지 않았어요.'),
132:('제품별로 확인된 희석 지시와 원제품에 임의로 물을 넣는 행동을 구분해요.','이 사례에서는 희석 지시를 따랐다는 관찰이 있어요.','다른 제품에도 같은 희석이 허용된다고 추정할 수 없어요.'),
134:('무거운 느낌과 건조 재발 보고를 각각 기록해요.','보습제 보유만으로 실제 사용이나 두 관찰의 시간 관계를 알 수 없어요.','사용 후 불편이나 보습 방법의 차이는 현재 정보로 확정하지 않아요.'),
139:('외관이 같아도 원제품에 지침 없이 물을 넣은 취급을 별도로 검토해요.','색이나 냄새 변화가 없다는 관찰은 현재 품질 전체를 보증하지 않아요.','물 혼입이나 외관만으로 오염 여부를 확정할 수 없어요.'),
}
T={
37:('지속 불편과 통증이 확인돼 개별 권고를 보류해요.','확인된 진료 후속 계획과 상담을 전문가에게 확인해 주세요. 세안제 중단과 통증의 전후 관계는 알 수 없어요.'),
38:('심한 지속 통증이 확인돼 개별 권고를 보류해요.','필수 보호장비에 관한 작업 지침과 현재 통증은 관련 전문가에게 확인해 주세요. 장갑 변경과 통증의 전후 관계는 미상이에요.'),
41:('기기 안내와 개별 의료진의 기기 회피 지시가 충돌해 병용 설계를 보류해요.','의료진에게 개인 지시의 적용 범위를 확인해 주세요.'),
42:('지속 통증에 대해 사용량 조절만으로 해결한다고 판단하지 않고 개별 권고를 보류해요.','통증과 감량의 전후 관계나 원인은 확인되지 않았어요. 의료 전문가에게 확인해 주세요.'),
}
for c in D['cases']:
 n=int(c['id'].rsplit('-',1)[1]); ref=c['request']['allowed_evidence_refs'][0]
 if c['mode']=='solution' and n in S:
  a,b,z=S[n]; c['answer']=f'### 핵심 안내\n{a} [{ref}]\n\n### 근거 및 이유\n{b}\n\n### 확인이 필요한 한계\n{z}'
 elif c['mode']=='hold' and n in T:
  a,b=T[n]; c['answer']=f'### 개별 권고 보류 안내\n{a} [{ref}]\n\n### 필요한 다음 단계\n{b}'
 else:
  prior=old[c['id']]; assert {k:v for k,v in prior.items() if k!='answer'}==c; c['answer']=prior['answer']
O.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(O.read_bytes()).hexdigest())
