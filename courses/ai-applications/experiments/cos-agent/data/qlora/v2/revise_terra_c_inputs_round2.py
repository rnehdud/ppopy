import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
PATH = HERE / 'additional_100_terra_part_c_inputs.json'
EXPECTED = '3d12407ca3b66a5eb841dc54c8e69da9ec67abd8b20e9b8c8f812116e33bf0a4'
raw = PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED: raise SystemExit('고정 입력이 예상과 다릅니다.')
data = json.loads(raw)
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf8'))
def walk(x):
    if isinstance(x,dict):
        if x.get('id','').startswith('B-') and 'comparison_spec' in x: yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)
cards = {x['id']: x for x in walk(kb)}
def obs(values):
    return {k: {'variable_id':k,'state':'known','value':v,'source':'synthetic_fixture','confirmed_by_user':True} for k,v in values.items()}
replacements = {
 'syn-sol-0173': ('복합 각질관리와 별도 각질관리의 같은 부위 중첩', 'B-G15', {'product.active_care_roles': {'가': 'AHA와 BHA 기능을 표시한 단일 복합 완제품', '나': '별도 BHA 각질관리 제품'}, 'routine.co_use_context': {'사용': '두 제품을 얼굴 같은 부위에 함께 사용', '가와 나': '별도 완제품'}, 'product.combination_design': {'가': '복합 완제품', '나': '별도 제품'}}, 'difference', '복합 완제품 내부 기능과 별도 BHA 제품을 구분하되, 두 완제품의 같은 부위 실제 중첩을 별도로 검토해요.'),
 'syn-hold-0052': ('제품명 일치 회수 공지와 읽을 수 없는 제조번호', 'B-Q05', {'product.identity': {'제품명': '회수 공지와 합성 제품명이 일치'}, 'storage.batch': {'제조번호': '지워져 읽을 수 없음'}, 'commerce.recall_check': {'공지 범위': '특정 제조번호만 해당', '공지 지시': '번호 확인 전 판매처에 문의', '대상 일치': '확인되지 않음'}}, 'hold', '제품명만으로 대상 로트 일치를 확정하지 않고 해당 용기의 개별 판단을 보류하며 제조번호 확인 경로를 검토해요.'),
 'syn-hold-0053': ('기기 두 모드의 상반된 지시와 실제 모드 미상', 'B-G06', {'product.instructions': {'모드 가': '합성 보습제 병용 허용', '모드 나': '같은 보습제 병용 금지', '적용 기기': '같은 합성 기기'}, 'adjunct.device_use': {'기기와 보습제': '함께 사용했다고 보고', '실제 사용 모드': '확인되지 않음', '질문': '해당 조합을 계속해도 되는지'}}, 'hold', '모드별 지시는 확인됐지만 실제 모드가 미상이므로 해당 기기와 제품 조합의 개인별 판단을 보류해요.'),
 'syn-hold-0054': ('이상 입자 관찰과 서로 상충하는 품질 안내', 'B-S04', {'storage.sensory_change': {'현재 용기': '이전에는 없던 입자 발생'}, 'product.instructions': {'용기 표시': '입자 발생 시 사용하지 말고 문의'}, 'storage.seal_integrity': {'판매 안내': '모든 입자가 정상이라고 안내', '동일 용기 확인 여부': '미상'}}, 'hold', '새 입자와 제품 표시를 확인하고 동일 용기에 적용되는지 불명인 상충 안내를 분리하여 개별 판단을 보류해요.'),
 'syn-hold-0055': ('현재 눈 노출과 심한 통증', 'B-P06', {'skin.eye_symptom_context': {'상황': '합성 선제품이 방금 눈에 직접 들어감', '통증': '심함', '시야 변화': '확인되지 않음'}, 'skin.eye_stinging': {'현재': '심한 눈 통증'}}, 'hold', '직접 눈 노출 뒤 심한 안구 통증이 보고되어 개별 루틴 판단을 보류해요. 시야 변화 여부는 미상으로 남겨요.'),
 'syn-hold-0058': ('현행 성분 일치와 과거 반응 제품 동일성 미상', 'B-G11', {'person.known_allergies': {'의료진 확인 회피 성분': 'Linalool'}, 'product.instructions': {'현행 합성 후보 전성분': 'Linalool 표시'}, 'introduction.local_trial': {'과거': '심한 제품 반응', '과거 제품과 후보의 동일성': '확인되지 않음', '현재 요청': '후보 국소 시험 여부', '시험': '아직 하지 않음'}}, 'hold', '과거 제품과의 동일성은 미상으로 두고 확인된 개인 회피 성분이 현행 후보에 표시된 상황의 국소 시험 판단을 보류해요.'),
}
for c in data['cases']:
    rid = c['id']
    if rid in ('syn-sol-0166','syn-sol-0172','syn-sol-0187','syn-sol-0190'):
        c['request']['kb_judgments'][0]['status'] = 'unknown'
        c['request']['kb_judgments'][0]['guidance'] += ' 전체 비교에 필요한 중복 또는 사용 기간 정보는 미상이므로 전체 정렬 여부는 확정하지 않아요.'
        c['judgment_basis']['rationale'] = c['request']['kb_judgments'][0]['guidance']
    if rid in replacements:
        title, card, values, status, guidance = replacements[rid]
        c['title'] = title
        c['card_ids'] = [card]
        q = c['request']
        q['confirmed_observations'] = obs(values)
        q['kb_judgments'] = [{'card_id':card,'status':status,'guidance':guidance}]
        q['allowed_evidence_refs'] = [f'kb:{card}@0.6.1'] + [x for x in q['allowed_evidence_refs'] if x.startswith('ref:')]
        c['judgment_basis'] = {'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':guidance}
    if rid in replacements or rid in ('syn-sol-0166','syn-sol-0172','syn-sol-0187','syn-sol-0190'):
        c['input_sha256'] = hashlib.sha256(json.dumps(c['request'], ensure_ascii=False, sort_keys=True, separators=(',',':')).encode('utf8')).hexdigest()
data['input_revision'] = 6
data['revision_note'] = '독립 감사에서 실패한 입력 판정과 중복 사례만 수정한 미검토 입력이에요. 답변을 작성하기 전에 고정했어요.'
PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
receipt = ROOT / 'outputs/additional_100_terra/c/round2_input_receipt.json'
with receipt.open('x',encoding='utf8') as f:
    json.dump({'before_sha256':EXPECTED,'after_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),'changed_ids':list(replacements)+['syn-sol-0166','syn-sol-0172','syn-sol-0187','syn-sol-0190']},f,ensure_ascii=False,indent=2)
