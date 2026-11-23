import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
PATH = HERE / 'additional_100_terra_part_c_inputs.json'
EXPECTED = 'db2f803111c30f34b241998e74e36c578895aae5432bf84c27bd336c1ffa9eed'
raw = PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit('입력 해시가 달라 갱신하지 않습니다.')
backup = ROOT / 'outputs/additional_100_terra/c/rev2'
backup.mkdir(parents=True, exist_ok=True)
with (backup / PATH.name).open('xb') as f: f.write(raw)
with (backup / 'sha256.txt').open('x', encoding='ascii') as f: f.write(EXPECTED + '  ' + PATH.name + '\n')
english = {}
for name in ['pilot_24.jsonl', 'additional_24.jsonl', 'additional_100.jsonl']:
    for line in (HERE / name).read_text(encoding='utf8').splitlines():
        row = json.loads(line)
        for chunk in json.loads(row['messages'][1]['content'])['rag_chunks']:
            if chunk['text'][:1].isascii() and chunk['text'][:1].isalpha() and row['chunk_origins'].get(chunk['evidence_ref']) == 'kb_source_summary':
                english.setdefault(chunk['evidence_ref'], chunk)
data = json.loads(raw)
for case in data['cases']:
    req = case['request']
    req['rag_chunks'] = [english.get(chunk['evidence_ref'], chunk) for chunk in req['rag_chunks']]
    case['input_sha256'] = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')).hexdigest()
data['input_revision'] = 3
data['revision_note'] = '둘째 입력판을 보존하고 기존 검토 자료의 동일 근거 영문 청크와 메타데이터를 사용했어요. 답변은 작성하지 않았어요.'
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
