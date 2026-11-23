import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
C_HASH = 'fcecab65f143c53cac3a721af8559c809ba1dd57ef8d54939547e01484125b52'

def answer_c(case):
    req = case['request']
    obs = req['confirmed_observations']['method.current_routine']['value']
    if case['mode'] == 'hold':
        return f'### 개별 권고 보류 안내\n{obs} 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]\n\n### 필요한 다음 단계\n현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.'
    status = req['kb_judgments'][0]['status']
    guide = req['kb_judgments'][0]['guidance']
    if status == 'difference' and ('불편' in obs):
        extra = '반복해서 불편한 해당 제품은 사용 중단이나 대체를 검토해요. 필요한 손 위생은 유지해요.'
    elif status == 'difference':
        extra = '보습 전체를 중단하기보다 견딜 수 있는 손 보습을 검토해요. 필요한 손 위생은 유지해요.'
    elif status == 'exception':
        extra = '현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요.'
    else:
        extra = '확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요.'
    return f'### 핵심 안내\n{obs} {guide} [kb:B-M04@0.6.1]\n\n### 근거 및 이유\n{extra} [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]\n\n### 확인이 필요한 한계\n제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.'

def main():
    p=HERE/'additional_200_terra_part_c_inputs.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == C_HASH
    data=json.loads(p.read_text(encoding='utf-8'))
    for case in data['cases']:
        case['answer']=answer_c(case)
    out=HERE/'additional_200_terra_part_c.json'
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('C',len(data['cases']),hashlib.sha256(out.read_bytes()).hexdigest())

if __name__ == '__main__':
    main()
