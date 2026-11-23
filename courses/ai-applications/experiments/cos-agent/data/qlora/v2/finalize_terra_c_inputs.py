import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
PATH = HERE / 'additional_100_terra_part_c_inputs.json'
EXPECTED = 'f0ad06d9a9b8fc9b23a9dd335c9a548ba1d2a0f2c09da7b990d33845277f5fb3'
raw = PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED: raise SystemExit('입력 해시가 다릅니다.')
backup = ROOT / 'outputs/additional_100_terra/c/rev4'
backup.mkdir(parents=True, exist_ok=True)
with (backup / PATH.name).open('xb') as f: f.write(raw)
with (backup / 'sha256.txt').open('x', encoding='ascii') as f: f.write(EXPECTED + '  ' + PATH.name + '\n')
data = json.loads(raw)
old = json.loads((ROOT / 'outputs/additional_100_terra/c/rev3' / PATH.name).read_text(encoding='utf8'))
old_by_id = {c['id']: c for c in old['cases']}
for c in data['cases']:
    obs = c['request']['confirmed_observations']
    if 'routine.schedule' in old_by_id[c['id']]['request']['confirmed_observations']:
        entry = obs.pop('routine.change_log')
        entry['variable_id'] = 'routine.co_use_context'
        obs['routine.co_use_context'] = entry
    if c['id'] in ('syn-sol-0189', 'syn-sol-0190'):
        original = old_by_id[c['id']]['request']['confirmed_observations']['product.type']['value']
        obs['product.type'] = {'variable_id': 'product.type', 'state': 'unknown', 'value': None, 'source': 'synthetic_fixture', 'confirmed_by_user': False}
        obs['product.identity'] = {'variable_id': 'product.identity', 'state': 'known', 'value': {'각 제품의 유형': original}, 'source': 'synthetic_fixture', 'confirmed_by_user': True}
    c['input_sha256'] = hashlib.sha256(json.dumps(c['request'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')).hexdigest()
data['input_revision'] = 5
data['revision_note'] = '넷째 입력판을 보존하고 제품별 유형 정보와 병용 맥락의 KB 변수 표현을 바로잡았어요. 답변은 작성하지 않았어요.'
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
