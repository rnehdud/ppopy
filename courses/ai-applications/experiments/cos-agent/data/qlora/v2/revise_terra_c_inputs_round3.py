import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
ROOT = HERE.parents[6]
INPUT = HERE / 'additional_100_terra_part_c_inputs.json'
ANSWER = HERE / 'additional_100_terra_part_c.json'
REVIEW = HERE / 'reviews/additional_100_terra_part_c_codex_independent.jsonl'
EXPECTED = 'a8a2f03a010c19487d516eb5fd42ca0d51984dbfbb102ca175ffa0e59b9c635b'
raw = INPUT.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED: raise SystemExit('입력 해시가 달라 중단합니다.')
backup = PROJECT / 'outputs/additional_100_terra/c/rev3'
backup.mkdir(parents=True, exist_ok=True)
for path in (INPUT, ANSWER, REVIEW):
    with (backup / path.name).open('xb') as f: f.write(path.read_bytes())
data = json.loads(raw)
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf8'))
def walk(node):
    if isinstance(node,dict):
        if node.get('id','').startswith('B-') and 'comparison_spec' in node: yield node
        for value in node.values(): yield from walk(value)
    elif isinstance(node,list):
        for value in node: yield from walk(value)
cards = {c['id']: c for c in walk(kb)}
def known(key, value): return {'variable_id':key,'state':'known','value':value,'source':'synthetic_fixture','confirmed_by_user':True}
def unknown(key): return {'variable_id':key,'state':'unknown','value':None,'source':'synthetic_fixture','confirmed_by_user':False}
for c in data['cases']:
    if c['id'] == 'syn-hold-0055':
        card = 'B-G03'
        guidance = '화장품의 성분 유사성만으로 개인의 처방 의약품 이름·용량·시작 절차를 설계하는 요청은 일반 제품 안내의 범위를 벗어나 보류해요.'
        c['title'] = '화장품 성분 유사성에서 개인 처방 설계 요청'
        c['card_ids'] = [card]
        q = c['request']
        q['confirmed_observations'] = {'product.type':known('product.type','일반 화장품'), 'method.current_routine':known('method.current_routine',{'질문':'이 화장품과 비슷한 성분이라는 이유로 처방 의약품의 이름과 용량 및 시작 절차를 정해 달라는 요청','현재 증상':'없음'}), 'person.clinician_plan':unknown('person.clinician_plan')}
        q['kb_judgments'] = [{'card_id':card,'status':'hold','guidance':guidance}]
        q['allowed_evidence_refs'] = ['kb:B-G03@0.6.1']
    elif c['id'] == 'syn-hold-0058':
        card = 'B-G11'
        guidance = '확인된 개인 회피 성분에 대해 현행 후보 표시가 포함 가능성과 확인 전 사용 보류를 명시하므로 국소 시험 판단을 보류해요. 실제 함유 여부는 미상이에요.'
        c['title'] = '개인 회피 성분 가능성 표시와 실제 함유 미상'
        q = c['request']
        q['confirmed_observations'] = {'person.known_allergies':known('person.known_allergies',{'의료진 확인 회피 성분':'Linalool'}), 'product.label_warnings':known('product.label_warnings',{'현행 표시':'Linalool을 포함할 가능성이 있으므로 확인 전 사용을 보류','대상':'합성 후보 현행 버전'}), 'product.inci':unknown('product.inci'), 'introduction.local_trial':known('introduction.local_trial',{'요청':'해당 후보의 국소 시험 여부','실제 시험':'아직 하지 않음'})}
        q['kb_judgments'] = [{'card_id':card,'status':'hold','guidance':guidance}]
        q['product_evidence'] = [{'product_id':'syn-terra-c58','version':'1.0','synthetic_product':True,'status':'verified','label_guidance':'합성 제품 표시 예시: Linalool을 포함할 가능성이 있으므로 확인 전 사용을 보류해요.','evidence_ref':'catalog:syn-terra-c58@1.0'}]
        q['allowed_evidence_refs'] = ['kb:B-G11@0.6.1','catalog:syn-terra-c58@1.0']
    else:
        continue
    c['judgment_basis'] = {'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':cards[card]['comparison_spec'],'rationale':guidance}
    c['input_sha256'] = hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()
data['input_revision'] = 7
data['revision_note'] = '두 번째 독립 감사에서 중복 판정된 두 입력만 교체해 답변 작성 전에 고정했어요.'
INPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
with (backup / 'receipt.json').open('x',encoding='utf8') as f:
    json.dump({'before_sha256':EXPECTED,'after_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'changed_ids':['syn-hold-0055','syn-hold-0058'],'preserved':{p.name:hashlib.sha256((backup/p.name).read_bytes()).hexdigest() for p in (INPUT,ANSWER,REVIEW)}},f,ensure_ascii=False,indent=2)
