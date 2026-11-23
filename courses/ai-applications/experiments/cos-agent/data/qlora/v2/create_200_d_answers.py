import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
INPUT_HASH='80776200aa814ff4ca1c1930fb902b609aa48311162ebfefa11f77f7b0fde3a4'

def answer(case):
    r=case['request']
    obs=r['confirmed_observations']['method.current_routine']['value']
    if case['mode']=='hold':
        return f'### 개별 권고 보류 안내\n{obs} 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]\n\n### 필요한 다음 단계\n현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.'
    j=r['kb_judgments'][0]
    card=j['card_id']
    status=j['status']
    if card=='B-G10':
        general='수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]'
        extra={'difference':'불편을 무시하며 강하게 누르거나 반복하는 방법을 조정할 여지를 살펴요.','unknown':'확인되지 않은 동작은 추측하지 않고 필요한 경우 확인해요.','aligned':'확인된 현재 동작에 한정해 살펴요.'}[status]
        limit='날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.'
    elif card=='B-M05':
        general='일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]'
        extra={'difference':'불편을 유발하는 특정 후처리 제품은 중단이나 대체를 검토하고 기본 보습은 함께 고려해요.','unknown':'개인 반응과 실제 보습 여부 중 확인되지 않은 정보는 미상으로 두어요.','aligned':'편안한 보습을 고려하며 별도 애프터셰이브 상품을 필수로 정하지 않아요.'}[status]
        limit='한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.'
    else:
        general='일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]'
        extra={'difference':'별도 제품의 같은 부위 중첩을 줄이고 필요한 관리 한 종류를 우선 검토해요.','unknown':'같은 부위, 관리 목적, 성분 또는 개별 진료 계획 중 확인되지 않은 정보는 미상으로 두어요. 처방약은 임의로 변경하지 않아요.','exception':'서로 다른 부위 또는 단일 복합 완제품이라는 확인된 조건을 별도로 살펴요.'}[status]
        limit='이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.'
    return f'### 핵심 안내\n{obs} {j["guidance"]} [kb:{card}@0.6.1]\n\n### 근거 및 이유\n{extra} [kb:{card}@0.6.1] {general}\n\n### 확인이 필요한 한계\n{limit}'

def main():
    p=HERE/'additional_200_terra_part_d_inputs.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==INPUT_HASH
    data=json.loads(p.read_text(encoding='utf-8'))
    for case in data['cases']:
        case['answer']=answer(case)
    out=HERE/'additional_200_terra_part_d.json'
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(len(data['cases']),hashlib.sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':main()
