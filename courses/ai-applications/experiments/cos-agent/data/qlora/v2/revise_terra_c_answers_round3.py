import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'additional_100_terra_part_c_inputs.json'
OUT = HERE / 'additional_100_terra_part_c.json'
EXPECTED = '3a102c24f2cff5a6b929e0f00a809414b04d10ef809f1932686eabc02f1f6293'
raw = INPUT.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED: raise SystemExit('고정 입력 해시가 다릅니다.')
data = json.loads(raw)
previous = {c['id']:c['answer'] for c in json.loads(OUT.read_text(encoding='utf8'))['cases']}
replacement = {
 'syn-hold-0055': '### 개별 권고 보류 안내\n화장품 성분이 비슷하다는 정보만으로 개인에게 맞는 처방 의약품의 이름·용량·시작 절차를 정하는 요청은 보류해요. [kb:B-G03@0.6.1]\n\n### 필요한 다음 단계\n개인별 의약품 선택과 사용 계획은 의료 전문가와 상담해요. 현재 개인 진료 계획은 확인되지 않았어요.',
 'syn-hold-0058': '### 개별 권고 보류 안내\n현행 합성 후보의 표시가 확인된 개인 회피 성분의 포함 가능성과 확인 전 사용 보류를 안내하므로 국소 시험에 관한 개별 권고를 보류해요. [kb:B-G11@0.6.1] [catalog:syn-terra-c58@1.0]\n\n### 필요한 다음 단계\n표시된 성분 관련 정보를 제조·판매처와 의료 전문가에게 확인해요. 실제 함유 여부와 전성분은 미상이며 포함됐다고 확정하지 않아요.',
}
for c in data['cases']:
    c['answer'] = replacement.get(c['id'],previous[c['id']])
OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
