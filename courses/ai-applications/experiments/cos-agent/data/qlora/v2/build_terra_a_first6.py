"""Write-once, unreviewed input candidates; no assistant responses."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
OUT = HERE / 'additional_100_terra_part_a_inputs.json'
if OUT.exists():
    raise FileExistsError(OUT)

def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))['cases']

old = {c['id']: c for name in ('additional_100_part_a_inputs.json', 'additional_24_part_a_inputs.json') for c in read(name)}
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards = {c['id']: c for c in kb['baseline_cards']}

def obs(name, value, state='known'):
    return {'variable_id': name, 'state': state, 'value': value, 'source': 'synthetic_fixture', 'confirmed_by_user': state == 'known'}

def make(n, base, title, observations, status, guidance, bucket, hard=False):
    c = copy.deepcopy(old[base]); ident = f'syn-sol-{n:04d}'
    c.update(id=ident, title=title, scenario_id=f'terra-a-scenario-{ident}', group_id=f'terra-a-group-{ident}', scenario_family_id=f'terra-a-family-{n:04d}', split='train', pilot_bucket=bucket, is_hard_negative=hard, hard_negative_type='unsupported_inference' if hard else None)
    req = c['request']; card = c['card_ids'][0]
    req['confirmed_observations'] = {k: obs(k, v) for k, v in observations.items()}
    req['kb_judgments'][0].update(status=status, guidance=guidance)
    c['judgment_basis'].update(comparison_spec=cards[card]['comparison_spec'], rationale=guidance)
    c['input_sha256'] = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    return c

cases = [
 make(114, 'syn-sol-0051', '직사광선은 피하지만 용기를 계속 열어 둔 보관', {'storage.light_air': {'currently_away_from_sunlight': True, 'container_left_open': True}}, 'difference', '직사광선을 피하더라도 용기를 지속적으로 열어 둔 보관은 별도로 검토해요.', 'normal_guidance'),
 make(115, 'syn-sol-0060', '지침 확인 없이 원제품에 물을 넣어 묽게 사용', {'storage.water_ingress': True, 'storage.handling': {'water_added_without_instructions': True}}, 'difference', '원제품에 임의로 물을 넣은 취급을 검토하되 이 사실만으로 오염 여부를 확정하지 않아요.', 'normal_guidance'),
 make(116, 'syn-sol-0049', '피부를 말린 뒤 도포하라는 별도 제품 지시', {'skin.dryness': 'mild', 'method.skin_wetness': 'dry', 'product.instructions': {'apply_to_dry_skin': True}, 'method.current_routine': {'follows_product_instruction': True}}, 'exception', '해당 제품의 건조 피부 도포 지시를 일반 보습 시점보다 함께 우선 검토해요.', 'normal_guidance'),
 make(117, 'syn-sol-0041', '무향료 표시와 개인이 반복해서 느낀 불편', {'hand.moisturizing_pattern': {'after_washing': True}, 'hand.product_reaction': {'repeated_discomfort': True}, 'hand.protection_hygiene': {'required_hygiene_maintained': True}}, 'difference', '무향료 표시만으로 개인의 반복 불편을 무시하지 않고 필요한 손 위생과 보습을 함께 검토해요.', 'normal_guidance'),
 make(118, 'syn-sol-0051', '현재 용기 밀폐는 알지만 과거 보관 지침은 미확인', {'storage.light_air': {'container_closed': True}, 'storage.temperature_history': {'label_storage_conditions_unknown': True}}, 'unknown', '현재 밀폐 여부만으로 제품별 보관 지침의 충족이나 이전 온도 이력을 확정하지 않아요.', 'unknown_or_version'),
 make(119, 'syn-sol-0049', '보습 계획은 있으나 세정 뒤 실제 도포는 미확인', {'skin.dryness': 'mild', 'method.current_routine': {'plans_moisturizer_after_wash': True}}, 'unknown', '세정 뒤 보습할 계획만으로 실제 도포나 피부 물기 상태를 확인할 수 없어요.', 'unknown_or_version'),
]
OUT.write_text(json.dumps({'schema_version':'additional-100-terra-part-a-inputs-v1', 'mode':'development_preview', 'production_enabled':False, 'cases':cases}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(cases)} unreviewed input candidates written: {OUT}')
