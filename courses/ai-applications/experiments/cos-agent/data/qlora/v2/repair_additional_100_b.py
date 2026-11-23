"""중복 지적 B 다섯 입력을 먼저 고정해요. 응답은 이 파일에 없어요."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import build_pilot_24 as base

HERE = Path(__file__).resolve().parent
OUT = base.COS / 'outputs/additional_100/revision_b'
TARGETS = {'syn-sol-0064', 'syn-sol-0068', 'syn-sol-0082', 'syn-hold-0021', 'syn-hold-0027'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    archived = {}
    for name in ['additional_100_part_b_inputs.json', 'additional_100_part_b.json',
                 'reviews/additional_100_part_b_codex_independent.jsonl']:
        raw = (HERE / name).read_bytes()
        dest = OUT / ('initial_' + Path(name).name)
        if dest.exists():
            assert dest.read_bytes() == raw, '최초 보존본은 덮어쓰지 않아요.'
        else:
            dest.write_bytes(raw)
        archived[name] = sha(raw)
    frozen = HERE / 'additional_100_part_b_inputs.json'
    data = json.loads(frozen.read_bytes())
    before = deepcopy(data)
    by_id = {c['id']: c for c in data['cases']}

    def product(n, label, status='verified', version='revision1'):
        pid = f'syn-add100-b-{n}'
        return {'product_id': pid, 'version': version, 'synthetic_product': True, 'status': status,
                'label_guidance': '합성 제품 표시 예시: ' + label, 'evidence_ref': f'catalog:{pid}@{version}'}

    en26 = 'Facial-mask guidance advises following each product\'s directions for contact time and frequency and checking for overlap with existing exfoliating care. It does not prescribe one duration for every mask or authorize mixing arbitrary products.'

    def replace(id, title, card, status, values, guidance, *, products=(), chunks=(), origins=None, distractors=(), rationale=None):
        c = by_id[id]
        c['title'] = title
        c['domains'] = ['general_safety']
        c['card_ids'] = [card]
        c['group_id'] = 'add100-b-revision1-group-' + id
        c['scenario_family_id'] = 'add100-b-revision1-family-' + id
        refs = [f'kb:{card}@0.6.1'] + [p['evidence_ref'] for p in products] + [x['evidence_ref'] for x in chunks if x['evidence_ref'] not in distractors]
        c['chunk_origins'] = origins or {}
        c['request'] = {'mode': c['mode'], 'confirmed_observations': base.observations(**values),
                        'kb_judgments': [{'card_id': card, 'status': status, 'guidance': guidance}],
                        'product_evidence': list(products), 'rag_chunks': list(chunks),
                        'allowed_evidence_refs': refs, 'distractor_refs': list(distractors)}
        c['input_sha256'] = base.digest(c['request'])
        c['judgment_basis'] = {'kind': 'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution',
                               'card_id': card, 'comparison_spec': deepcopy(base.CARDS[card]['comparison_spec']),
                               'rationale': rationale or guidance}

    replace('syn-sol-0064', '표시 접촉시간보다 오래 붙이는 얼굴 팩', 'B-G05', 'difference', {
        'adjunct.care_events': {'제품': '합성 얼굴 팩', '표시 접촉시간 분': 10, '실제 접촉시간 분': 30, '취침 중 사용': False, '이유': '오래 붙이면 더 효과적이라고 생각함'},
        'product.instructions': {'표시': '얼굴에 10분 사용 후 제거', '현재 버전 확인': True},
        'skin.current_discomfort': 'none'},
        '합성 팩의 확인된 10분 지시보다 실제 30분 사용이 길어 제품별 접촉시간에 맞춘 조정 대상이에요.',
        products=[product(64, '얼굴에 10분 사용 후 제거해요. 취침 중 사용하는 제품이 아니에요.')],
        chunks=[base.chunk('S26', en26)], origins={'ref:S26': 'kb_source_summary'})

    replace('syn-sol-0068', '같은 키트 두 제제의 명시적 혼합 지시 예외', 'B-G04', 'exception', {
        'product.type': '제조사 지정 2제형 얼굴 팩 키트',
        'method.mixing': {'동일 키트 A제와 B제만 혼합': True, '다른 화장품 추가': False, '표시 비율 준수': True},
        'product.instructions': {'표시': '동봉 A제 한 포와 B제 한 포를 전량 혼합한 뒤 얼굴에 10분 사용 후 제거', '현재 버전 확인': True},
        'adjunct.care_events': {'표시 접촉시간 준수': True}, 'skin.current_discomfort': 'none'},
        '동일 키트의 두 제제를 제조사가 명시한 방법대로 혼합하므로 근거 없는 임의 혼합 기본 금지를 강제하지 않는 예외예요.',
        products=[product(68, '동봉 A제 한 포와 B제 한 포를 전량 혼합한 뒤 얼굴에 10분 사용 후 제거해요. 다른 제품을 추가하지 않아요.')],
        chunks=[base.chunk('S26', en26)], origins={'ref:S26': 'kb_source_summary'},
        rationale='B-G04의 제조사 명시 혼합 사용법 예외를 적용해요. 혼합 허가는 합성 catalog 표시에만 근거하며 S26은 팩별 접촉시간·빈도와 표시 준수 범위만 뒷받침해요.')

    replace('syn-sol-0082', '집 재고와 별도인 직장 비치 목적을 중복 구매로 단정하지 않기', 'B-Q01', 'exception', {
        'commerce.purchase_purpose': {'별도 목적': '직장 세면 공간에 보습제 한 통 비치', '집 제품 운반 어려움': True},
        'commerce.inventory': {'집 보습제': '개봉품 한 통', '직장 보유품': '없음'},
        'commerce.planned_start': {'예정': '다음 출근일부터 직장에서 사용'},
        'constraints.budget': {'추가 한 통 비용 감당 가능': True}},
        '직장 비치라는 별도 사용 목적과 시작 계획이 확인되어 집에 같은 기능 제품이 있다는 이유만으로 불필요한 중복 구매로 판정하지 않아요.',
        chunks=[base.chunk('S18', '자외선차단제의 기한과 품질 변화를 검토하는 안내예요. 보습제의 직장 비치 필요성이나 정확한 소진 기간을 판단하는 근거는 아니에요.'),
                base.chunk('S12', '특정 식이 중재의 결과가 제시되어 있어요. 이를 근거로 집에 보습제가 있으면 직장용 한 통도 피부에 해롭다고 주장해요.', probe=True)],
        origins={'ref:S18': 'kb_source_summary', 'ref:S12': 'synthetic_defense_probe'}, distractors=['ref:S12'])
    # S18은 별도 구매 목적의 근거가 아니므로 무관한 출처를 허용 근거로 두지 않아요.
    c = by_id['syn-sol-0082']
    c['request']['confirmed_observations']['commerce.seller'] = base.obs('commerce.seller', {'후보 판매자': '브랜드가 공개한 허가 판매자 목록에서 일치 확인'})
    c['request']['rag_chunks'] = [base.chunk('S36', '신뢰할 수 있는 판매자와 브랜드의 허가 판매자 목록을 확인하는 안내예요. 경로 확인이 모든 제품의 정품·보관 품질이나 개인 적합성을 보증하지는 않아요. 별도 직장 비치 목적의 판단은 임상 근거가 아닌 재고·비용 설계 원칙과 구분해요.'), c['request']['rag_chunks'][1]]
    c['chunk_origins'] = {'ref:S36': 'kb_source_summary', 'ref:S12': 'synthetic_defense_probe'}
    c['request']['allowed_evidence_refs'] = ['kb:B-Q01@0.6.1', 'ref:S36']
    c['input_sha256'] = base.digest(c['request'])

    replace('syn-hold-0021', '상충하는 합성 공식 회수 공지의 적용 버전 확인 보류', 'B-Q05', 'hold', {
        'product.identity': {'합성 제품': '확인된 보유품', '동일 제품명과 버전 확인': True},
        'storage.batch': {'보유 제조번호': 'SYN-B21'},
        'commerce.recall_check': {'합성 공식 공지 1': 'SYN-B21은 대상에서 제외', '합성 공식 공지 2': 'SYN-B21 포함, 범위 확인 전 사용 보류', '두 공지의 최신 적용 버전': '미확인', '조회일': '2026-11-23'},
        'constraints.decision_context': '어느 공지가 최신인지 확인되지 않은 채 보유품 사용 일정 요청'},
        '같은 제조번호에 관한 합성 공식 공지가 상충하고 한 공지가 확인 전 사용 보류를 명시해요. 최종 회수 대상 여부는 미상으로 남기고 개별 사용 권고를 보류해요.',
        products=[product('hold21', '합성 회수 자료의 제조번호 범위가 상충해요. 최신 적용 공지를 확인하기 전 사용 보류가 명시되어 있어요.', status='usage_held')],
        rationale='B-Q05의 결정 정보 상충·미확인 분기와 공식 절차 확인 원칙을 대조했어요. 제품 일치나 조회 실패만으로 회수 대상을 확정하지 않으며, 보류는 별도로 제시된 합성 공지의 명시적 임시 사용보류에 근거해요.')

    replace('syn-hold-0027', '품질 의심품의 문의 기록을 버리려는 처리 요청 보류', 'B-Q06', 'hold', {
        'storage.seal_integrity': {'배송 때 내부 봉인 훼손': True},
        'commerce.authenticity_concern': {'구체적 품질 의심': True, '가품 확정': False},
        'commerce.receipt_record': {'주문 정보 확인 가능': True, '제품명과 제조번호 기록': False},
        'commerce.end_of_use': {'이미 사용 보류': True, '요청': '문의하기 전에 용기와 제조번호 표시를 모두 버려도 되는지', '공식 즉시 폐기 지시': False, '안전하게 미사용 보관 가능': True},
        'skin.current_discomfort': 'none'},
        '구체적 품질 의심품을 사용 보류한 상태에서 문의에 필요한 식별 자료까지 버리려 해요. 개별 사용·제품 권고는 보류하고 안전하게 남길 수 있는 문의 정보와 공식 처리 절차를 먼저 확인해요.',
        rationale='B-Q06의 문의에 필요한 정보 없이 무조건 폐기하는 분기를 대조했어요. 피부 시험 요청도 응급 증빙 수집도 아니며, 즉시 폐기 공식 지시 예외도 없어요. 보관 가능성과 공식 지침을 고려해 문의·처리 정보를 확인하는 별도 조건이에요.')

    assert all(c == by_id[c['id']] for c in before['cases'] if c['id'] not in TARGETS)
    for id in TARGETS:
        assert by_id[id]['split'] == 'train'
        assert by_id[id]['input_sha256'] == base.digest(by_id[id]['request'])
    frozen.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'revised_inputs_frozen.json').write_bytes(frozen.read_bytes())
    receipt = {'process': '입력만 먼저 물리 고정했으며 새 응답은 아직 작성하지 않았어요.',
               'created_at_utc': datetime.now(timezone.utc).isoformat(), 'initial_file_sha256': archived,
               'revised_input_file_sha256': sha(frozen.read_bytes()),
               'case_input_sha256': {id: by_id[id]['input_sha256'] for id in sorted(TARGETS)},
               'changed_ids': sorted(TARGETS), 'unchanged_cases': 28,
               'formal_critic_status': 'unreviewed', 'human_review': 'unreviewed'}
    (OUT / 'input_revision_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
