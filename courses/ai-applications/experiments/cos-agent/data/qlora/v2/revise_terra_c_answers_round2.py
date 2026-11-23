import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'additional_100_terra_part_c_inputs.json'
OUT = HERE / 'additional_100_terra_part_c.json'
EXPECTED = 'a8a2f03a010c19487d516eb5fd42ca0d51984dbfbb102ca175ffa0e59b9c635b'
raw = SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED: raise SystemExit('고정 입력이 예상과 다릅니다.')
fixed = json.loads(raw)
old = json.loads(OUT.read_text(encoding='utf8'))
old_by_id = {c['id']:c for c in old['cases']}
answers = {
 'syn-sol-0166': '### 핵심 안내\n확인된 수면팩의 밤 사용은 표시된 방법과 일치해요. [kb:B-G05@0.6.1]\n\n### 근거 및 이유\n제품 지침과 실제 사용을 비교하되 다른 관리의 중복은 확인되지 않았어요. [kb:B-G05@0.6.1]\n\n### 확인이 필요한 한계\n전체 관리의 정렬 여부는 미상이며 사용법의 일치가 안전성 보증은 아니에요.',
 'syn-sol-0172': '### 핵심 안내\n레티놀과 AHA 관리가 서로 다른 날 이뤄졌지만 전체 중첩 비교는 미상이에요. [kb:B-G13@0.6.1]\n\n### 근거 및 이유\n날짜 분리만으로 겹치는 사용기간이나 적합성을 자동 확정하지 않아요. [kb:B-G13@0.6.1]\n\n### 확인이 필요한 한계\n구체적인 빈도와 기간이 확인되지 않았고, 처방 변경이나 무자극을 추정하지 않아요.',
 'syn-sol-0173': '### 핵심 안내\n복합 완제품과 별도의 BHA 제품이 같은 부위에 사용돼 별도 제품 간 중첩을 검토해요. [kb:B-G15@0.6.1]\n\n### 근거 및 이유\n하나의 복합 완제품 안의 두 기능과 추가된 별도 제품의 실제 중첩을 구분해요. [kb:B-G15@0.6.1]\n\n### 확인이 필요한 한계\n중첩은 개인 위해나 임상 결과를 확정하지 않으며 제품별 지시와 개인 상황을 확인해요.',
 'syn-sol-0187': '### 핵심 안내\n동거인의 다른 제품 반응을 본인의 팩 반응으로 옮기지 않아요. [kb:B-G05@0.6.1]\n\n### 근거 및 이유\n본인의 팩 사용은 표시 시간과 일치하지만 유사 관리 중복 여부는 확인되지 않았어요. [kb:B-G05@0.6.1]\n\n### 확인이 필요한 한계\n전체 정렬 여부는 미상이고 현재 불편이 없다는 보고는 앞으로의 무반응을 보증하지 않아요.',
 'syn-sol-0190': '### 핵심 안내\n사용한 수면팩에는 확인된 해당 제품의 밤 사용 지시를 적용해요. [kb:B-G05@0.6.1]\n\n### 근거 및 이유\n사용하지 않은 다른 팩의 제거 지시를 수면팩에 옮기지 않아요. [kb:B-G05@0.6.1]\n\n### 확인이 필요한 한계\n유사 관리의 다른 중복은 미상이므로 전체 정렬 여부와 개인 안전성을 확정하지 않아요.',
 'syn-hold-0052': '### 개별 권고 보류 안내\n제품명은 공지와 일치하지만 제조번호가 읽히지 않아 해당 용기의 회수 대상 여부와 개별 판단을 보류해요. [kb:B-Q05@0.6.1]\n\n### 필요한 다음 단계\n특정 번호에만 적용되는 공지 범위를 유지하고 안내된 판매처에 제조번호 확인 방법을 문의해요.',
 'syn-hold-0053': '### 개별 권고 보류 안내\n기기의 두 모드에 대한 병용 지시가 다르고 실제 사용 모드는 미상이어서 해당 조합의 개별 판단을 보류해요. [kb:B-G06@0.6.1]\n\n### 필요한 다음 단계\n실제 모드와 같은 제품에 적용되는 지시를 기기 제조사에 확인해요. 다른 일반 관리의 상태까지 추정하지 않아요.',
 'syn-hold-0054': '### 개별 권고 보류 안내\n새 입자와 입자 발생 시 문의하라는 용기 표시가 확인되어 해당 제품의 개별 판단을 보류해요. [kb:B-S04@0.6.1]\n\n### 필요한 다음 단계\n상충하는 판매 안내가 이 용기에 적용되는지 제조·판매처에 확인해요. 변질의 원인이나 제품 전체의 안전성을 확정하지 않아요.',
 'syn-hold-0055': '### 개별 권고 보류 안내\n제품의 직접 눈 노출 뒤 심한 눈 통증이 보고되어 개별 루틴 안내를 보류해요. [kb:B-P06@0.6.1]\n\n### 필요한 다음 단계\n지체하지 말고 의료진의 확인을 받아요. 시야 변화 여부는 미상이며 원인을 진단하지 않아요.',
 'syn-hold-0058': '### 개별 권고 보류 안내\n현행 후보에 개인이 회피하도록 안내받은 성분이 표시돼 국소 시험에 관한 개별 권고를 보류해요. [kb:B-G11@0.6.1]\n\n### 필요한 다음 단계\n확인된 성분과 과거 반응 정보를 의료 전문가에게 전달해 확인해요. 과거 제품과 현재 후보가 같은 제품인지는 미상이에요.',
}
failed = {'syn-sol-0166','syn-sol-0172','syn-sol-0173','syn-sol-0174','syn-sol-0175','syn-sol-0178','syn-sol-0179','syn-sol-0181','syn-sol-0183','syn-sol-0184','syn-sol-0185','syn-sol-0186','syn-sol-0187','syn-sol-0189','syn-sol-0190','syn-hold-0052','syn-hold-0053','syn-hold-0054','syn-hold-0055','syn-hold-0058'}
for c in fixed['cases']:
    rid = c['id']
    answer = old_by_id[rid]['answer']
    if rid in answers:
        answer = answers[rid]
    elif rid in failed:
        kb = c['request']['allowed_evidence_refs'][0]
        for ref in c['request']['allowed_evidence_refs'][1:]:
            answer = answer.replace('['+ref+']','['+kb+']')
    c['answer'] = answer
OUT.write_text(json.dumps(fixed,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
