import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import httpx

POC_DIR = Path(__file__).resolve().parent
CONFIG = POC_DIR / 'stt_jev_test_fields.json'
PROJECT_ENV_FILE = POC_DIR.parents[1] / '.env'
REPOSITORY_ROOT = next((p for p in POC_DIR.parents
                        if (p / 'docs' / 'repository-scope.md').is_file()),
                       POC_DIR.parents[1])
ENV_FILE = REPOSITORY_ROOT / '.env'
# Exploratory routing threshold; not a validated probability cutoff.
ROUTING_THRESHOLD = 0.5
EXTRA_QUESTIONS = {
    'product_name_mentioned': '사용자가 특정 화장품을 식별하는 고유한 제품명 또는 브랜드와 제품명을 명시했는가? 로션, 스킨, 크림 같은 일반적인 제품 종류만 말한 것은 고유 제품명이 아니다.',
    'product_planned': '사용자가 본인이 화장품을 앞으로 사용할 계획이나 의도를 명시했는가? 이미 사용했다는 보고와 구분한다.',
    'product_use_denied': '사용자가 본인의 화장품 사용 사실을 명시적으로 부정했는가? 단순 미언급은 부정이 아니다.',
    'symptom_denied': '사용자가 본인에게 특정 피부 증상이 없다고 명시적으로 말했는가? 단순 미언급은 부정이 아니다.',
    'information_refused': '사용자가 피부 상태나 제품 사용 정보 제공을 명시적으로 거절했는가? 단순 미언급이나 모름은 거절이 아니다.',
}


def get_api_key():
    key = os.environ.get('TYPESAFE_API_KEY', '').strip()
    if key:
        return key
    for path in dict.fromkeys((ENV_FILE, PROJECT_ENV_FILE)):
        if not path.is_file():
            continue
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            name, sep, value = line.partition('=')
            if sep and name.strip() in ('jev-key', 'TYPESAFE_API_KEY'):
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                if value.strip():
                    return value.strip()
    return None


def build_questions(config):
    questions = {}
    shared = config['shared_instructions']
    for name, field in config['fields'].items():
        if name == 'intent':
            continue
        if field['type'] == 'multiple_noul':
            for symptom, question in field['questions'].items():
                questions[f'skin_condition.{symptom}'] = {
                    'type': 'noul', 'instructions': f"{shared}\n{field['instructions']}\n{question}"
                }
        else:
            question = {'type': field['type'], 'instructions': f"{shared}\n{field['instructions']}"}
            if field['type'] == 'choice':
                question['criteria'] = field['criteria']
            questions[name] = question
    for name, instruction in EXTRA_QUESTIONS.items():
        questions[name] = {'type': 'noul', 'instructions': f'{shared}\n{instruction}'}
    return questions


FIELD_LABELS = {
    'intent': '의도', 'skin_condition.dryness': '건조함',
    'skin_condition.breakout': '트러블', 'skin_condition.redness': '붉어짐',
    'skin_condition.stinging': '따가움', 'skin_condition.itching': '가려움',
    'severity': '불편감 강도', 'usage_time': '제품 사용 시간',
    'product_used': '제품 사용 보고', 'symptom_onset': '증상 시작',
    'event_recognition_time': '증상 인식 시간',
    'routine_change_requested': '루틴 변경 요청',
    'product_planned': '제품 사용 계획', 'product_use_denied': '제품 사용 명시적 부정',
    'symptom_denied': '증상 명시적 부정', 'information_refused': '정보 제공 거절',
    'product_name_mentioned': '고유 제품명 언급',
}


def print_summary(result):
    labels = FIELD_LABELS
    print('\n--- 전체 문장 필드별 판정 ---')
    for name, answer in result['answers'].items():
        label = labels.get(name, name)
        if answer.get('type') == 'choice':
            choice = answer['choice']
            probability = answer.get('probabilities', {}).get(choice)
            probability_text = f'{probability:.1%}' if probability is not None else '없음'
            candidate = choice not in ('unknown', 'other', None) and (probability or 0) > ROUTING_THRESHOLD
            status = 'SLM 전달 후보' if candidate else '후보 아님 · 미확정'
            print(f'{label} ({name}): {choice} | 선택 점수 {probability_text} | {status}')
        elif answer.get('type') == 'noul':
            score = answer.get('noul', 0)
            candidate = score > ROUTING_THRESHOLD
            status = 'SLM 전달 후보' if candidate else '기준 미달 · 부정 판정 아님'
            print(f'{label} ({name}): 긍정 보고 점수 {score:.1%} | {status}')
    print('점수는 제공자 분류 점수이며 보정된 확률이나 정답 보증이 아닙니다. 근거 문구는 Jev 응답에 포함되지 않습니다.')


def routing_candidates(result):
    candidates = []
    for name, answer in result['answers'].items():
        if answer.get('type') == 'choice':
            value = answer.get('choice')
            probability = answer.get('probabilities', {}).get(value, 0) or 0
            if value not in ('unknown', 'other', None) and probability > ROUTING_THRESHOLD:
                candidates.append({'field': name, 'value': value, 'probability': probability, 'status': 'candidate'})
        elif answer.get('type') == 'noul' and (answer.get('noul', 0) or 0) > ROUTING_THRESHOLD:
            if name == 'product_name_mentioned':
                candidates.append({'field': 'product_name', 'value': '추출 필요', 'probability': answer['noul'], 'status': 'candidate'})
            else:
                candidates.append({'field': name, 'value': 'positive_report', 'probability': answer['noul'], 'status': 'candidate'})
    return candidates


def classify(utterance, key, config, verbose=False):
    payload = {'model': 'jev-latest', 'state': utterance, 'questions': build_questions(config)}
    started = time.perf_counter()
    try:
        response = httpx.post('https://api.typesafe.ai/v1/systemone', headers={'Authorization': f'Bearer {key}'}, json=payload, timeout=60.0)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or not isinstance(result.get('answers'), dict) or set(result['answers']) != set(payload['questions']):
            raise ValueError('응답의 answers가 요청한 질문과 일치하지 않습니다.')
    except (httpx.HTTPError, ValueError) as exc:
        print(f'Jev 호출 실패: {type(exc).__name__} (HTTP 상태 또는 응답 형식을 확인하세요.)', file=sys.stderr)
        return 1
    if verbose:
        print('\n--- 원시 응답 ---')
        print(json.dumps({'schema_version': config['schema_version'], 'elapsed_ms': round((time.perf_counter() - started) * 1000), 'evidence_status': 'unassessed', 'response': result}, ensure_ascii=False, indent=2))
    return result


EVIDENCE_THRESHOLD = 0.5


try:
    from .context_evidence import candidate_spans, select_evidence
    from .product_mentions import extract_products
    from .relations import extract_features, print_features
except ImportError:
    from context_evidence import candidate_spans, select_evidence
    from product_mentions import extract_products
    from relations import extract_features, print_features


def contextual_evidence(utterance, key, config, candidates, progress=None):
    return select_evidence(utterance, key, build_questions(config), candidates, progress)


def print_input_mapping(utterance, candidates, spans, warning=None, verbose=False):
    print('\n=== 입력 → 필드 배정 후보 ===')
    print(f'입력: {utterance}')
    grouped = {}
    missing = []
    for candidate in candidates:
        field = candidate['field']
        label = FIELD_LABELS.get(field, field)
        value = candidate['value']
        suffix = '' if value in ('positive_report', '추출 필요') else f' = {value}'
        display = f'{label} ({field}){suffix}'
        matches = [x for x in spans.get(field, [])
                   if x['mode'] != '사용 사건 점수' or x['score'] > EVIDENCE_THRESHOLD]
        if not matches:
            missing.append(display)
        for match in matches:
            key = (match['start'], match['end'])
            status = ' [선택 불확실]' if match['score'] <= EVIDENCE_THRESHOLD else ''
            detail = f" · 분류 {candidate['probability']:.0%} / {match['mode']} {match['score']:.0%}" if verbose else ''
            product_value = f" = {match['value']}" if field == 'product_used' else ''
            grouped.setdefault(key, []).append(display + product_value + status + detail)
    for index, ((start, end), fields) in enumerate(sorted(grouped.items()), 1):
        print(f'\n  {index}. 「{utterance[start:end]}」')
        for field in fields:
            print(f'     → {field}')
    if not candidates:
        print('\n  분류 기준을 넘은 필드 없음')
    if missing:
        heading = '근거 판정 실패 · 미평가 필드' if warning else '원문 구절에 연결하지 못한 필드'
        print(f'\n  {heading}:')
        for field in missing:
            print(f'     ? {field}')
    if warning:
        print(f'\n  {warning}')
    print('\n※ 별도 Jev 질문으로 연결한 후보입니다. 전체 점수는 --verbose로 확인하세요.')


def run_input(utterance, key, config, verbose=False, as_json=False, app_json=False,
              confirmed_state=None, confirmation=None, app_cards=False):
    if app_json:
        features = extract_features(utterance, key)
        try:
            from .mapping_review.backend import prepare_handoff
        except ImportError:
            from mapping_review.backend import prepare_handoff
        handoff = prepare_handoff(features, confirmed_state, confirmation)
        if app_cards:
            try:
                from .mapping_review.display import print_handoff
            except ImportError:
                from mapping_review.display import print_handoff
            print_handoff(handoff)
        else:
            print(json.dumps(handoff, ensure_ascii=False, indent=2))
        return 1 if handoff['status'] in ('invalid_input', 'blocked') else 0
    result = classify(utterance, key, config, verbose=verbose and not as_json)
    if not isinstance(result, dict):
        return 1
    features = extract_features(utterance, key)
    features['classification'] = result
    if as_json:
        print(json.dumps(features, ensure_ascii=False, indent=2))
    else:
        if verbose:
            print_summary(result)
        print_features(features)
        try:
            from .mapping_review.candidates import print_mapping
        except ImportError:
            from mapping_review.candidates import print_mapping
        print_mapping(features['skin_state_mapping'])
        if verbose:
            print(json.dumps(features, ensure_ascii=False, indent=2))
    return 0 if not features['warnings'] else 1


def main():
    parser = argparse.ArgumentParser(description='Jev 한국어 텍스트 분류 실험 (합성 입력 권장)')
    parser.add_argument('text', nargs='?', help='분류할 텍스트; 생략하면 반복 입력')
    parser.add_argument('--verbose', action='store_true', help='기존 추출 카드·원시 응답·전체 필드 확률 표시 (디버그)')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--json', action='store_true', help='내부 디버그용 추출 후보 JSON (앱 요청 본문 아님)')
    output.add_argument('--app-json', action='store_true', help='백엔드 계약 기준 앱 전달 후보만 출력 (저장 비활성)')
    parser.add_argument('--confirmed-state', type=Path, help='합성 사용자 확인 입력 JSON 파일')
    parser.add_argument('--confirmation', type=Path, help='합성 UI 확인 바인딩 JSON 파일; 서버 권한 아님')
    args = parser.parse_args()
    app_mode = args.app_json or not (args.json or args.verbose)
    if (args.confirmed_state or args.confirmation) and (not app_mode or args.text is None):
        parser.error('확인 입력 파일은 앱 출력 모드에서 입력 문장과 함께 사용하세요.')
    confirmed_state = confirmation = None
    try:
        if args.confirmed_state:
            confirmed_state = json.loads(args.confirmed_state.read_text(encoding='utf-8-sig'))
        if args.confirmation:
            confirmation = json.loads(args.confirmation.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        parser.error('확인 입력 파일을 읽을 수 없거나 JSON 형식이 아닙니다. 입력 내용은 출력하지 않습니다.')
    key = get_api_key()
    if not key:
        print(f'API 키가 없습니다. {ENV_FILE} 또는 {PROJECT_ENV_FILE}에 jev-key를 설정하거나 '
              'TYPESAFE_API_KEY 환경변수를 설정하세요.', file=sys.stderr)
        return 1
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    if args.text is not None:
        if not args.text.strip():
            parser.error('빈 텍스트는 사용할 수 없습니다.')
        return run_input(args.text, key, config, verbose=args.verbose, as_json=args.json,
                         app_json=app_mode, confirmed_state=confirmed_state, confirmation=confirmation,
                         app_cards=app_mode and not args.app_json)
    print('Jev 매핑 테스트: 문장을 입력하세요. 종료하려면 /quit을 입력하세요.' if app_mode else
          'Jev 추출 디버그: 문장을 입력하세요. 종료하려면 /quit을 입력하세요.')
    print('입력은 TypeSafe API로 전송됩니다. 개인정보 없는 합성 문장을 사용하세요.')
    while True:
        try:
            utterance = input('\n텍스트> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n종료합니다.')
            return 0
        if utterance.lower() == '/quit':
            print('종료합니다.')
            return 0
        if not utterance:
            print('문장을 입력하세요.')
            continue
        print('\n분류 중...')
        run_input(utterance, key, config, verbose=args.verbose, as_json=args.json, app_json=app_mode,
                  app_cards=app_mode and not args.app_json)


if __name__ == '__main__':
    sys.exit(main())
