import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
PATH = HERE / 'additional_100_terra_part_c_inputs.json'
EXPECTED = '77f1cfed988243ee536fe43f51cde7173a6f9bfe25ca70e36ef651c92a51b81b'
raw = PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit('입력 초판 해시가 다릅니다. 덮어쓰지 않습니다.')
backup = ROOT / 'outputs/additional_100_terra/c/rev1'
backup.mkdir(parents=True, exist_ok=True)
old = backup / PATH.name
with old.open('xb') as f:
    f.write(raw)
with (backup / 'sha256.txt').open('x', encoding='ascii') as f:
    f.write(EXPECTED + '  ' + PATH.name + '\n')
data = json.loads(raw)
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf8'))
def walk(node):
    if isinstance(node, dict):
        if node.get('id', '').startswith('B-') and 'comparison_spec' in node:
            yield node
        for v in node.values(): yield from walk(v)
    elif isinstance(node, list):
        for v in node: yield from walk(v)
cards = {c['id']: c for c in walk(kb)}
chunks = {}
for filename in ['pilot_24.jsonl', 'additional_24.jsonl', 'additional_100.jsonl']:
    for line in (HERE / filename).read_text(encoding='utf8').splitlines():
        row = json.loads(line)
        req = json.loads(row['messages'][1]['content'])
        for chunk in req['rag_chunks']:
            if row['chunk_origins'].get(chunk['evidence_ref']) == 'kb_source_summary':
                chunks.setdefault(chunk['evidence_ref'], chunk)

def known(values):
    return {k: {'variable_id': k, 'state': 'known', 'value': v, 'source': 'synthetic_fixture', 'confirmed_by_user': True} for k,v in values.items()}

# title, card, observation, status, authored rationale, supporting source, hard negative
normal = [
('처방 변경 없이 제품 지시가 허용하는 분리 사용', 'B-G13', {'product.active_care_roles': {'가': '일반 레티놀 관리 화장품', '나': 'AHA 각질관리 화장품'}, 'routine.schedule': {'실제': '서로 다른 날 사용', '처방 변경': '없음'}, 'method.body_site': '얼굴'}, 'aligned', '서로 다른 날의 실제 사용을 같은 시간 중첩으로 바꾸지 않아요. 개인 반응과 제품 지시는 별도로 확인해요.', 'ref:S32', None),
('한 제품에서 표시된 두 기능과 별도 제품 중첩 구분', 'B-G15', {'product.active_care_roles': {'가': 'AHA와 BHA 기능을 함께 표시한 단일 완제품', '나': '일반 보습제'}, 'routine.schedule': {'실제': '동일한 저녁에 사용'}, 'product.adjunct_functions': {'가': '복합 각질관리', '나': '보습'}}, 'aligned', '단일 복합 완제품의 두 기능을 별도 각질관리 제품 두 개의 중첩으로 계산하지 않아요.', 'ref:S32', None),
]
unknown = [
('처방 성분명은 확인되나 같은 부위 여부 미상','B-G14',{'product.active_care_roles': {'가': '처방 레티노이드', '나': '살리실릭애씨드 각질관리 화장품'}, 'routine.schedule': {'같은 날 사용': True, '접촉 부위': '확인되지 않음'}, 'person.clinician_plan': {'변경 지시': '확인되지 않음'}},'unknown','같은 날이라는 정보만으로 같은 부위 병용을 확정하지 않고 처방은 자동 변경하지 않아요.','ref:S34','version_mismatch_or_unknown'),
('성분 역할이 기재된 예전 판과 현행 판 대조 미완료','B-G13',{'product.identity': {'현행 제품': '합성 세럼 나', '자료': '구버전의 기능 표시'}, 'product.active_care_roles': {'구버전': 'AHA 각질관리', '현행 버전': '확인되지 않음'}, 'routine.schedule': {'실제 사용': '현행 제품 사용'}},'unknown','구버전 역할을 현행 제품의 확인된 역할로 옮기지 않아요.','ref:S32','version_mismatch_or_unknown'),
('팩 시간 표시는 있으나 실제 제거 시간 미상','B-G05',{'product.instructions': {'표시': '10분 후 제거'}, 'adjunct.care_events': {'실제': '팩 사용은 확인', '제거 시각': '기억하지 못함'}, 'skin.current_discomfort': '불편 없음'},'unknown','확인된 표시만으로 실제 접촉시간 초과를 만들지 않아요.','ref:S26','version_mismatch_or_unknown'),
('스포이드 중량은 있으나 용기 교체 후 토출량 미상','B-G08',{'product.identity': {'제품': '동일 합성 세럼', '용기': '스포이드 교체'}, 'product.dispensing_unit_context': {'이전 용기 측정': '있음', '교체 용기 측정': '없음'}, 'dose.proxy_amount': {'실제': '교체 용기 세 방울'}},'unknown','이전 용기의 측정값을 교체된 용기에 자동 적용하지 않아요.',None,'version_mismatch_or_unknown'),
('면도젤 사용계획과 실제 사용의 구별','B-G09',{'shaving.method': {'확인': '습식 수동 날면도'}, 'shaving.preparation': {'계획': '다음 면도에 젤을 사용', '이번 실제 준비': '미상'}, 'product.instructions': {'젤': '습식 면도에 사용'}},'unknown','미래 계획은 이번 면도에서의 준비를 확인해 주지 않아요.','ref:S23',None),
('제품 목적 표시만 있고 실제 성분표는 확인되지 않음','B-G13',{'product.active_care_roles': {'표시 목적': '각질관리', '성분표': '확인되지 않음'}, 'product.inci': {'현행 목록': '확인되지 않음'}, 'routine.schedule': {'사용': '저녁에 사용'}},'unknown','관리 목적만으로 특정 성분의 존재나 농도를 확정하지 않아요.','ref:S32',None),
('처방 지시의 적용 대상 제품이 불명확','B-G14',{'person.clinician_plan': {'문구': '저녁 관리 조정', '대상 제품': '확인되지 않음'}, 'product.active_care_roles': {'가': '처방 레티노이드', '나': '살리실릭애씨드 관리 화장품'}, 'routine.schedule': {'동일 부위 실제 중첩': '확인되지 않음'}},'unknown','대상 불명의 진료 지시를 새 제품에 적용하거나 처방을 임의 변경하지 않아요.','ref:S34',None),
('동일 제품 재구매 후 새 용기의 표시 이력 미상','B-G05',{'product.identity': {'현재': '새로 구입한 합성 팩', '이전': '같은 이름의 예전 용기'}, 'product.instructions': {'이전 용기': '저녁 사용 허용', '현재 용기': '확인되지 않음'}, 'adjunct.care_events': {'현재 용기': '아직 사용하지 않음'}},'unknown','동일 상품명만으로 현재 용기의 표시와 실제 사용을 확정하지 않아요.','ref:S26',None),
('얼굴 국소 확인 결과와 목 사용 여부의 빈칸','B-G11',{'introduction.local_trial': {'얼굴 일부': '합성 신제품의 국소 확인 후 불편 없음', '목 사용': '확인되지 않음'}, 'product.instructions': {'대상': '얼굴과 목'}, 'skin.current_discomfort': '현재 보고된 불편 없음'},'unknown','한 부위의 관찰을 다른 부위의 실제 사용 또는 무반응으로 확장하지 않아요.','ref:S35',None),
]
defense = [
('향 이름의 acid와 각질관리 목적 구별','B-G15',{'product.inci': {'향 성분': 'Benzyl Salicylate'}, 'product.adjunct_functions': {'합성 제품': '향을 위한 성분 표기', '각질관리 목적': '확인되지 않음'}, 'routine.schedule': {'실제': '한 제품 사용'}},'unknown','이름 일부가 비슷하다는 이유만으로 각질관리 역할이나 중첩을 만들지 않아요.','ref:S32','negation_or_other_subject'),
('동거인의 약 사용을 본인의 처방으로 전환하지 않기','B-G14',{'product.medication_status': {'본인 처방': '보고되지 않음', '동거인': '처방 레티노이드 사용'}, 'product.active_care_roles': {'본인': '살리실릭애씨드 각질관리 화장품'}, 'routine.schedule': {'본인': '저녁 사용'}},'unknown','타인의 처방을 본인의 실제 병용으로 취급하지 않아요.','ref:S34','negation_or_other_subject'),
('미개봉 후보의 각질관리 역할을 현재 중첩으로 오인','B-G15',{'product.active_care_roles': {'현재 제품': 'AHA 각질관리', '미개봉 후보': 'BHA 각질관리'}, 'routine.schedule': {'현재': 'AHA 사용', '후보': '소유만 하고 사용하지 않음'}},'unknown','보유 사실을 실제 동시 사용으로 바꾸지 않아요.','ref:S32','negation_or_other_subject'),
('처방 중단 계획과 실제 중단 구분','B-G14',{'product.medication_status': {'현재': '처방 레티노이드 사용 중', '계획': '스스로 중단을 생각함'}, 'product.active_care_roles': {'추가 후보': '살리실릭애씨드 각질관리', '실제 사용': '아직 시작하지 않음'}, 'person.clinician_plan': {'중단 지시': '확인되지 않음'}},'unknown','중단 계획을 실제 중단이나 의료진 지시로 취급하지 않아요.','ref:S34','negation_or_other_subject'),
('다른 사람의 팩 반응을 본인의 반응으로 해석하지 않기','B-G05',{'adjunct.care_events': {'본인': '합성 팩을 표시 시간에 사용', '동거인': '다른 제품 사용 중 따가움'}, 'product.instructions': {'본인 팩': '10분 후 제거'}, 'skin.current_discomfort': '본인 불편 없음'},'aligned','동거인의 다른 제품 반응을 본인의 반응으로 옮기지 않아요.','ref:S26','negation_or_other_subject'),
('예정된 용기 교체를 실제 사용량 변화로 환산하지 않기','B-G08',{'product.dispensing_unit_context': {'현재': '원래 스포이드', '계획': '다음 달 새 스포이드 사용'}, 'dose.proxy_amount': {'현재 기록': '원래 용기 두 방울', '새 용기 토출량': '미상'}, 'product.identity': {'대상': '같은 합성 제품'}},'unknown','계획된 교체를 이미 발생한 토출량 변화로 다루지 않아요.',None,'negation_or_other_subject'),
('처방 약품과 같은 이름의 화장품 역할 혼동','B-G13',{'product.type': {'가': '일반 화장품', '나': '이름이 비슷한 처방 의약품'}, 'product.active_care_roles': {'가': '레티놀 관리 화장품', '나': '본인 사용 미확인'}, 'routine.schedule': {'가': '실제 사용', '나': '사용 미확인'}},'unknown','비슷한 상품명은 처방 상태나 두 제품의 실제 병용을 입증하지 않아요.','ref:S33','negation_or_other_subject'),
('씻어내는 팩의 지시를 남겨두는 제품에 이전하지 않기','B-G05',{'product.type': {'가': '씻어내는 팩', '나': '남겨두는 수면팩'}, 'product.instructions': {'가': '10분 후 제거', '나': '밤새 사용 가능'}, 'adjunct.care_events': {'실제': '나를 표시대로 밤새 사용', '가': '사용하지 않음'}},'aligned','서로 다른 제품의 지시와 실제 사용 대상을 분리해요.','ref:S26','negation_or_other_subject'),
]
holds = [
('회수 대상 용기 확인과 다른 용기의 대상 미상 분리','B-Q05',{'commerce.recall_status': {'용기 가': '공식 회수 대상 일치 확인', '용기 나': '대상 여부 미확인'}, 'product.identity': {'가': '합성 제품 가 현행 로트', '나': '다른 합성 제품'}},'hold','확인된 회수 대상에 대한 보류와 다른 용기의 미확인을 분리해요.'),
('사용 전 확인된 봉인 파손과 내용물 사용 계획','B-Q04',{'commerce.received_condition': {'합성 제품': '배송 당시 내용물이 새고 봉인이 훼손됨', '사용': '아직 하지 않음'}, 'product.identity': {'대상': '같은 배송 용기'}},'hold','배송 시 품질 이상이 확인된 해당 용기의 사용 판단을 보류해요.'),
('지속되는 광범위 불편과 일시 반응의 구분','B-B01',{'skin.current_discomfort': '얼굴 여러 부위에서 반복되고 지속되는 불편', 'skin.pain': '있음', 'routine.change_log': {'과거': '다른 제품의 일시적 국소 반응', '현재': '반복되는 넓은 부위 불편'}},'hold','과거 일시 반응과 현재 반복되는 불편을 구분하고 개별 권고를 보류해요.'),
('현행 진료 지시가 적용되는 부위의 별도 판단','B-B01',{'person.clinician_plan': {'대상': '현재 치료 중인 얼굴 부위', '지시': '진료 계획 외 새 제품을 적용하지 않음'}, 'method.current_routine': {'질문': '치료 부위에 새 합성 제품을 추가해도 되는지', '사용': '계획만 있음'}},'hold','확인된 진료 지시가 적용되는 부위의 새 제품 판단을 보류해요.'),
('제품 사용 후 눈의 지속 통증과 시야 변화','B-P06',{'skin.eye_symptom_context': {'현재': '제품 사용 후 눈 통증이 지속되고 시야 변화가 보고됨', '원인': '확인되지 않음'}, 'skin.eye_stinging': {'지속': True}},'hold','원인은 단정하지 않고 지속 통증과 시야 변화에 대한 전문가 확인을 우선해요.'),
('반응 제품을 기기와 다시 쓰려는 계획','B-G06',{'adjunct.device_use': {'이전': '합성 피부 기기와 제품을 함께 사용', '현재': '같은 조합 재사용 계획'}, 'skin.current_discomfort': '사용 뒤 지속되는 통증', 'person.clinician_plan': {'개별 기기 사용 지시': '확인되지 않음'}},'hold','지속 통증이 있는 기기 병용의 개별 사용 지시를 보류해요.'),
('기존 정상 분리 표시와 새 냄새 변화의 구분','B-S04',{'storage.sensory_change': {'정상 표시': '사용 전 흔드는 2층 제형', '새 관찰': '이전과 다른 강한 냄새 발생'}, 'product.instructions': {'표시': '흔들어 사용'}, 'storage.expiry': {'표시 기한': '남음'}},'hold','정상 2층 표시와 별개로 새 냄새 변화가 있어 해당 제품 판단을 보류해요.'),
('심한 과거 반응의 같은 현행 제품 재시험 계획','B-G11',{'introduction.local_trial': {'과거': '같은 현행 합성 제품 사용 후 심한 반응', '현재': '다시 시험하려는 계획', '재시험': '아직 하지 않음'}, 'product.identity': {'일치': '제품과 버전이 과거 반응 기록과 일치'}},'hold','과거 심한 반응을 겪은 동일 제품의 재시험 지시는 보류해요.'),
]

def add(rid, item, bucket, split):
    if bucket == 'hold':
        title, card, values, status, guidance = item
        ref = hn = None
    else:
        title, card, values, status, guidance, ref, hn = item
    mode = 'hold' if bucket == 'hold' else 'solution'
    rag = [chunks[ref]] if ref else []
    refs = [f'kb:{card}@0.6.1'] + ([ref] if ref else [])
    req = {'mode': mode, 'confirmed_observations': known(values), 'kb_judgments': [{'card_id': card, 'status': status, 'guidance': guidance}], 'product_evidence': [], 'rag_chunks': rag, 'allowed_evidence_refs': refs, 'distractor_refs': []}
    sha = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')).hexdigest()
    data['cases'].append({'id': rid, 'title': title, 'pilot_bucket': bucket, 'mode': mode, 'scenario_id': 'terra-c-'+rid+'-scenario', 'group_id': 'terra-c-'+rid+'-group', 'scenario_family_id': 'terra-c-'+rid+'-family', 'split': split, 'domains': ['general_safety'], 'card_ids': [card], 'is_hard_negative': bool(hn), 'hard_negative_type': hn, 'chunk_origins': {ref: 'kb_source_summary'} if ref else {}, 'request': req, 'input_sha256': sha, 'judgment_basis': {'kind': 'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution', 'card_id': card, 'comparison_spec': cards[card]['comparison_spec'], 'rationale': guidance}, 'source_origin': 'new_synthetic', 'source_scenario_id': None, 'source_turn_id': None, 'source_note': '새 합성 개발 후보이며 실제 사용자·제품 기록이나 엔진 실행 결과가 아니에요. 독립 검토와 사람 검토는 아직 이루어지지 않았어요.'})

for i, item in enumerate(normal + unknown + defense, 172):
    bucket = 'normal_guidance' if i < 174 else 'unknown_or_version' if i < 183 else 'distractor_or_defense'
    add(f'syn-sol-{i:04d}', item, bucket, 'val_internal' if i in (178, 187) else 'train')
for i, item in enumerate(holds, 51):
    add(f'syn-hold-{i:04d}', item, 'hold', 'val_internal' if i in (53, 57) else 'train')
assert len(data['cases']) == 33
data['input_revision'] = 2
data['revision_note'] = '초판 여섯 입력을 보존하고 미검토 입력 후보를 서른세 건으로 늘렸어요. 답변은 작성하지 않았어요.'
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
