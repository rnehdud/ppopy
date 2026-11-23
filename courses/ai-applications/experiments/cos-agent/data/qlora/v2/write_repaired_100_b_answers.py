"""물리 고정된 B 개정 입력에 대해 다섯 새 응답만 작성해요."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import build_pilot_24 as base

HERE = Path(__file__).resolve().parent
OUT = base.COS / 'outputs/additional_100/revision_b'
FROZEN_SHA = 'c0dbf3608553575ab98c2065b03b90ab6d39a1589b9447a7a54804b777560353'
SECTIONS = {
    'syn-sol-0064': (
        '이 합성 팩은 얼굴에 10분 사용 후 제거하도록 표시되어 있는데 실제로는 30분 붙이고 있어요. 오래 쓸수록 더 좋다고 보지 않고 확인된 제품별 접촉시간에 맞춰 조정해요 [kb:B-G05@0.6.1] [catalog:syn-add100-b-64@revision1].',
        '팩 안내는 각 제품의 접촉시간과 빈도, 기존 각질관리와의 중복을 함께 살펴요. 모든 팩에 같은 시간을 정하는 원칙은 아니에요 [ref:S26].',
        '현재 불편이 없다는 보고가 긴 접촉시간의 효과나 무해성을 입증하지는 않아요. 이 합성 제품의 10분을 다른 팩이나 기기에 공통 기준으로 적용하지 않아요.'),
    'syn-sol-0068': (
        '이 합성 키트는 동봉 A제와 B제를 표시대로 혼합하도록 명시되어 있어요. 확인된 두 제제만 표시 비율로 섞는 행동에 임의 혼합 금지를 강제하지 않아요 [kb:B-G04@0.6.1] [catalog:syn-add100-b-68@revision1].',
        '혼합을 허용하는 근거는 이 키트의 확인된 합성 표시예요. 일반 팩 안내는 제품별 접촉시간과 빈도를 따르도록 하는 범위이며, 임의의 제품 혼합을 승인하는 자료는 아니에요 [catalog:syn-add100-b-68@revision1] [ref:S26].',
        '이 예외는 같은 키트의 지정된 A제와 B제에만 해당해요. 다른 화장품 추가나 임의 비율 변경으로 확대하지 않으며, 현재 불편이 없다는 보고만으로 개인의 안전성이나 효과를 보증하지 않아요.'),
    'syn-sol-0082': (
        '집 보습제와 별도로 직장에 비치할 한 통이 필요하고 다음 출근일부터 쓸 계획이 확인됐어요. 집 재고가 있다는 이유만으로 불필요한 중복 구매라고 단정하지 않고 별도 목적의 예외로 검토해요 [kb:B-Q01@0.6.1].',
        '보유 장소와 실제 사용 계획, 감당 가능한 비용을 함께 보는 재고·비용 설계 판단이에요. 후보 판매자는 브랜드의 공개 허가 판매자 목록에서 확인됐지만, 이런 경로 확인도 전체 품질을 보증하지는 않아요 [kb:B-Q01@0.6.1] [ref:S36].',
        '별도 목적이 있다는 것이 즉시 구매를 강제하거나 임상적 필요성을 확정하는 뜻은 아니에요. 정확한 소진 기간과 미개봉 수명은 미상이며, 무관한 식이 연구로 두 장소의 보유가 피부에 해롭다고 판단하지 않아요.'),
    'syn-hold-0021': (
        '같은 제조번호에 관한 합성 공식 회수 공지가 상충하고 최신 적용 버전이 확인되지 않았어요. 한 공지가 확인 전 사용 보류를 명시하므로 개별 사용 일정이나 제품 권고는 보류해요. 최종 회수 대상 여부는 미상으로 남겨요 [kb:B-Q05@0.6.1] [catalog:syn-add100-b-hold21@revision1].',
        '제품 식별 정보와 제조번호, 두 공지의 게시·적용 버전을 공식 문의 경로에서 대조해요. 어느 공지가 현재 유효한지와 임시 보류의 해제 조건을 확인하기 전에는 대상 제외나 사용 재개를 확정하지 않아요. 다른 제조번호나 브랜드 전체로 범위를 넓히지 않아요.'),
    'syn-hold-0027': (
        '배송 당시 내부 봉인 훼손이라는 구체적 품질 의심이 있어 이미 사용 보류한 상태예요. 현재 불편이 없어도 개별 사용·제품 권고는 보류하며, 이 정보만으로 가품이나 오염을 확정하지 않아요 [kb:B-Q06@0.6.1].',
        '문의하기 전에 용기와 식별 정보를 모두 버리기보다 안전하게 남길 수 있는 제품명·제조번호 사진이나 주문 기록으로 판매처에 확인·반품·처리 절차를 문의해요. 자료 확보를 위해 위험한 물건을 보관하도록 강제하지 않으며, 공식 폐기 지시가 있다면 그 범위를 우선 확인해요. 피부에 발라 진위를 시험하는 방법은 제시하지 않아요.'),
}


def main():
    raw = (HERE / 'additional_100_part_b_inputs.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FROZEN_SHA
    assert (OUT / 'revised_inputs_frozen.json').read_bytes() == raw
    data = json.loads(raw)
    initial = json.loads((OUT / 'initial_additional_100_part_b.json').read_bytes())
    old = {c['id']: c for c in initial['cases']}
    for c in data['cases']:
        if c['id'] not in SECTIONS:
            assert c == {k:v for k,v in old[c['id']].items() if k != 'answer'}
            c['answer'] = old[c['id']]['answer']
        else:
            heads = ['핵심 안내', '근거 및 이유', '확인이 필요한 한계'] if c['mode'] == 'solution' else ['개별 권고 보류 안내', '필요한 다음 단계']
            c['answer'] = '\n\n'.join(f'### {h}\n{s}' for h,s in zip(heads, SECTIONS[c['id']]))
    p = HERE / 'additional_100_part_b.json'
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert all(c == old[c['id']] for c in data['cases'] if c['id'] not in SECTIONS)
    receipt = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
               'process': '물리 고정 입력 해시를 확인한 후 다섯 새 응답을 작성했어요. 나머지 28개 사례는 입력·응답을 그대로 보존했어요.',
               'input_file_sha256': FROZEN_SHA, 'output_file_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
               'changed_ids': sorted(SECTIONS), 'unchanged_cases': 28,
               'formal_critic_status': 'unreviewed', 'human_review': 'unreviewed'}
    (OUT / 'answer_revision_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
