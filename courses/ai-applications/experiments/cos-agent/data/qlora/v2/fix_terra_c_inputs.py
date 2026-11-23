import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
PATH = HERE / 'additional_100_terra_part_c_inputs.json'
EXPECTED = '817462655621409bb93f8d2092aef67cf6e71bb8b39491bf880b70be27aa8bb1'
raw = PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit('입력 해시가 달라 갱신하지 않습니다.')
backup = ROOT / 'outputs/additional_100_terra/c/rev3'
backup.mkdir(parents=True, exist_ok=True)
if not (backup / PATH.name).exists():
    with (backup / PATH.name).open('xb') as f: f.write(raw)
    with (backup / 'sha256.txt').open('x', encoding='ascii') as f: f.write(EXPECTED + '  ' + PATH.name + '\n')
elif (backup / PATH.name).read_bytes() != raw:
    raise SystemExit('보존된 초판이 다릅니다.')
data = json.loads(raw)
ko = {}
for name in ['pilot_24.jsonl', 'additional_24.jsonl', 'additional_100.jsonl']:
    for line in (HERE / name).read_text(encoding='utf8').splitlines():
        row = json.loads(line)
        for chunk in json.loads(row['messages'][1]['content'])['rag_chunks']:
            if not chunk['text'][:1].isascii() and row['chunk_origins'].get(chunk['evidence_ref']) == 'kb_source_summary':
                ko.setdefault(chunk['evidence_ref'], chunk['text'])
seen = 0
ko.setdefault('ref:S26', '얼굴 팩은 제품별 접촉시간과 사용 빈도 안내를 따르도록 설명해요. 비슷한 각질 관리의 중복은 자극을 늘릴 수 있어 사용 맥락을 함께 살펴요. 모든 팩에 같은 시간이나 빈도를 적용한다는 뜻은 아니에요.')
for case in data['cases']:
    req = case['request']
    observations = req['confirmed_observations']
    for old, new in [('routine.schedule', 'routine.change_log'), ('commerce.recall_status', 'commerce.recall_check')]:
        if old in observations:
            entry = observations.pop(old)
            entry['variable_id'] = new
            observations[new] = entry
    if case['id'] in ('syn-sol-0189', 'syn-sol-0190'):
        entry = observations['product.type']
        entry['value'] = '서로 다른 두 제품 유형'
    for chunk in req['rag_chunks']:
        if chunk['text'][:1].isascii() and chunk['text'][:1].isalpha():
            seen += 1
            if seen > 8:
                chunk['text'] = ko[chunk['evidence_ref']]
    case['input_sha256'] = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')).hexdigest()
data['input_revision'] = 4
data['revision_note'] = '셋째 입력판을 보존하고 KB 변수 유형과 영문 청크 비율을 조정했어요. 답변은 작성하지 않았어요.'
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
