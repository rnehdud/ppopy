"""Append six candidate inputs once; preserve every earlier candidate."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'additional_100_terra_part_a_inputs.json'
data = json.loads(OUT.read_text(encoding='utf-8'))
if len(data['cases']) != 6 or data['cases'][-1]['id'] != 'syn-sol-0119':
    raise RuntimeError('Unexpected prior input state; refusing to write')
kb = json.loads((HERE.parents[6] / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards = {c['id']: c for c in kb['baseline_cards']}
old = {c['id']: c for c in json.loads((HERE / 'additional_100_part_a_inputs.json').read_text(encoding='utf-8'))['cases']}

def make(n, base, title, observations, status, guidance, bucket):
    c = copy.deepcopy(old[base]); ident = f'syn-sol-{n:04d}'; card = c['card_ids'][0]
    c.update(id=ident, title=title, scenario_id=f'terra-a-scenario-{ident}', group_id=f'terra-a-group-{ident}', scenario_family_id=f'terra-a-family-{n:04d}', split='train', pilot_bucket=bucket, is_hard_negative=bucket == 'unknown_or_version', hard_negative_type='version_mismatch_or_unknown' if bucket == 'unknown_or_version' else None)
    req = c['request']
    req['confirmed_observations'] = {k: {'variable_id': k, 'state': 'unknown' if v is None else 'known', 'value': v, 'source': 'synthetic_fixture', 'confirmed_by_user': v is not None} for k, v in observations.items()}
    req['kb_judgments'][0].update(status=status, guidance=guidance)
    req['distractor_refs'] = []
    req['rag_chunks'] = [z for z in req['rag_chunks'] if z['evidence_ref'] in req['allowed_evidence_refs']]
    c['chunk_origins'] = {k:v for k,v in c['chunk_origins'].items() if k in req['allowed_evidence_refs']}
    c['judgment_basis'].update(comparison_spec=cards[card]['comparison_spec'], rationale=guidance)
    c['input_sha256'] = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    return c

data['cases'].extend([
 make(120, 'syn-sol-0043', '건조 보관만 확인하고 도구 세척은 생략', {'shaving.care': {'rinse_after_use': False, 'dry_storage': True}, 'tool.care_state': {'type': 'manual_razor', 'visible_residue': True}}, 'difference', '건조 보관 사실과 별도로 도구에 잔여물이 남고 세척을 생략한 취급을 검토해요.', 'normal_guidance'),
 make(121, 'syn-sol-0045', '면도 후 반복되는 따가움을 흡수의 증거로 간주', {'shaving.aftercare': {'continued_despite_stinging': True}, 'shaving.reaction': {'repeated_stinging': True, 'persistent_problem': False}}, 'difference', '후처리 제품 사용 때 반복되는 따가움을 효과의 증거로 간주하지 않아요.', 'normal_guidance'),
 make(122, 'syn-sol-0042', '리필 허용 제품이지만 지침 없는 잔량 위 덧붓기', {'storage.refill': {'refill_allowed': True, 'topped_up_remaining_contents': True}, 'product.instructions': {'topping_up_authorized': False}}, 'difference', '리필 허용 표시와 남은 내용물 위 덧붓기 지침은 별개로 확인해요.', 'normal_guidance'),
 make(123, 'syn-sol-0052', '사용기한은 읽히지만 개봉 후 기간 표시는 미상', {'storage.opened_at': {'known': True}, 'product.instructions': None, 'storage.instance_id': {'current_container_known': True}}, 'unknown', '개봉 이력을 알아도 해당 제품의 개봉 후 안내가 없으면 사용 가능 기간을 계산하지 않아요.', 'unknown_or_version'),
 make(124, 'syn-sol-0054', '사용 횟수 기록은 있으나 면도기 유형이 미상', {'shaving.method': None, 'shaving.blade_use_history': {'uses': 6}, 'shaving.blade_condition': None}, 'unknown', '도구 유형과 상태가 확인되지 않아 수동 날 참고 횟수를 적용하지 않아요.', 'unknown_or_version'),
 make(125, 'syn-sol-0046', '세안 온도 느낌은 없고 수도꼭지 위치만 확인', {'method.water_temperature': {'tap_position_known': True, 'perceived_temperature_unknown': True}}, 'unknown', '수도꼭지 위치만으로 실제 물의 체감 온도를 추정하지 않아요.', 'unknown_or_version'),
])
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('12 input candidates; six appended')
