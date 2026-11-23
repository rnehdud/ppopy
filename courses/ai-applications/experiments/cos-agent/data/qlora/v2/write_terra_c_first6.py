import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
OUT = HERE / 'additional_100_terra_part_c_inputs.json'
if OUT.exists():
    raise SystemExit('입력 파일이 이미 있어 덮어쓰지 않습니다.')
kb = json.loads((ROOT / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))

def find_cards(node):
    if isinstance(node, dict):
        if node.get('id', '').startswith('B-') and 'comparison_spec' in node:
            yield node
        for value in node.values():
            yield from find_cards(value)
    elif isinstance(node, list):
        for value in node:
            yield from find_cards(value)

cards = {c['id']: c for c in find_cards(kb)}

def obs(values):
    return {key: {'variable_id': key, 'state': 'known', 'value': value, 'source': 'synthetic_fixture', 'confirmed_by_user': True} for key, value in values.items()}

items = [
 ('B-G05','취침 사용을 허용한 팩의 실제 용법', {'adjunct.care_events': {'사용': '합성 수면팩을 밤에 표시된 방식으로 사용', '중복 관리': '확인되지 않음'}, 'product.instructions': {'확인된 표시': '밤에 바르고 다음 날 아침 씻어내는 사용을 허용'}, 'skin.current_discomfort': '사용 중 불편 없음'}, 'aligned', '해당 제품은 표시에서 밤새 사용하는 방법을 허용하고 실제 방식도 일치해요. 취침 사용이라는 이유만으로 임의 사용 차이를 만들지 않아요.'),
 ('B-G04','명시된 희석법과 다른 실제 비율', {'product.instructions': {'확인된 표시': '합성 세정액 한 부분에 물 네 부분을 섞어 사용'}, 'method.mixing': {'실제': '세정액 한 부분에 물 한 부분을 섞음', '대상': '같은 표시 제품'}, 'product.type': '희석해 쓰는 합성 세정액'}, 'difference', '제조사가 희석을 명시했지만 실제 비율은 그 지시와 달라요. 희석 자체의 허용과 확인된 비율 준수 여부를 구분해요.'),
 ('B-G08','서로 다른 스포이드의 방울 수 환산', {'product.identity': {'제품 가': '합성 세럼 가', '제품 나': '합성 세럼 나'}, 'product.dispensing_unit_context': {'용기': '서로 다른 스포이드', '방울 질량 확인': False}, 'dose.proxy_amount': {'주장': '가의 두 방울과 나의 두 방울은 같은 질량'}, 'product.instructions': {'나의 표시': '적당량 사용'}}, 'difference', '서로 다른 용기의 같은 방울 수를 같은 질량으로 환산할 근거는 없어요. 제품별 표시와 기록을 분리해요.'),
 ('B-G09','건식 기기와 습식 날면도 지시의 대상', {'shaving.method': {'얼굴': '건식 전용 전기면도기', '목': '습식 수동 날면도'}, 'shaving.preparation': {'얼굴': '물과 크림 없이 사용', '목': '적시고 면도용 젤 사용'}, 'shaving.schedule_sites': {'시점': '같은 날', '부위': '얼굴과 목'}, 'product.instructions': {'전기면도기': '건식 전용', '면도용 젤': '습식 날면도에 사용'}}, 'aligned', '같은 날이어도 각 부위의 실제 방식과 해당 지시를 따로 대조해요. 습식 준비를 건식 전용 기기에 이식하지 않아요.'),
 ('B-G17','개인 알레르겐과 현행 성분표의 정확 일치', {'person.known_allergies': {'확인된 회피 성분': 'Linalool', '확인': '의료진에게 해당 성분 회피 안내를 받음'}, 'product.inci': {'대상': '합성 후보의 현행 버전', '확인된 표기': 'Linalool'}, 'product.fragrance': {'일반 선호': '향의 유무는 중요하지 않음'}, 'product.label_warnings': {'성분표 버전': '현행 버전과 일치'}}, 'aligned', '확인된 개인 회피 성분과 현행 성분표의 정확한 일치를 일반적인 향 선호와 구분해요. 모든 사람의 금지 성분이나 농도는 추정하지 않아요.'),
 ('B-G12','서로 다른 시작일과 겹친 관찰 기간', {'introduction.change_scope': {'첫 변경': '월요일 합성 보습제 도입', '둘째 변경': '수요일 합성 세정제 도입'}, 'routine.change_log': {'관찰': '두 변경 후 토요일에 당김을 느낌', '변경 전후 기록': '두 제품의 관찰 기간이 겹침'}, 'method.current_routine': {'실제 사용': '두 제품을 계속 사용함', '원인 주장': '나중에 시작한 세정제가 반드시 원인'}}, 'unknown', '시작일이 달라도 관찰 기간이 겹치므로 이후 느낌의 원인을 어느 한 제품으로 확정할 수 없어요. 차이를 자동으로 판정하거나 고정 대기 기간을 만들지 않아요.'),
]

cases = []
for i, (card, title, values, status, guidance) in enumerate(items, 166):
    rid = f'syn-sol-{i:04d}'
    req = {'mode': 'solution', 'confirmed_observations': obs(values), 'kb_judgments': [{'card_id': card, 'status': status, 'guidance': guidance}], 'product_evidence': [], 'rag_chunks': [], 'allowed_evidence_refs': [f'kb:{card}@0.6.1'], 'distractor_refs': []}
    digest = hashlib.sha256(json.dumps(req, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    cases.append({'id': rid, 'title': title, 'pilot_bucket': 'normal_guidance', 'mode': 'solution', 'scenario_id': 'terra-c-' + rid + '-scenario', 'group_id': 'terra-c-' + rid + '-group', 'scenario_family_id': 'terra-c-' + rid + '-family', 'split': 'train', 'domains': ['general_safety'], 'card_ids': [card], 'is_hard_negative': False, 'hard_negative_type': None, 'chunk_origins': {}, 'request': req, 'input_sha256': digest, 'judgment_basis': {'kind': 'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution', 'card_id': card, 'comparison_spec': cards[card]['comparison_spec'], 'rationale': guidance}, 'source_origin': 'new_synthetic', 'source_scenario_id': None, 'source_turn_id': None, 'source_note': '새 합성 개발 후보이며 실제 사용자·제품 기록이나 엔진 실행 결과가 아니에요. 독립 검토와 사람 검토는 아직 이루어지지 않았어요.'})

data = {'schema_version': 'additional-pilot-shard-v1', 'input_revision': 1, 'revision_note': '여섯 건의 미검토 입력 후보를 먼저 고정했어요. 답변은 작성하지 않았어요.', 'mode': 'development_preview', 'production_enabled': False, 'cases': cases}
with OUT.open('x', encoding='utf-8', newline='\n') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
    file.write('\n')
