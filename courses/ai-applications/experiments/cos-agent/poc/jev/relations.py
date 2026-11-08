"""Jev-only, candidate-based semantic extraction. Never writes app data."""
import hashlib
import json
import re

import httpx

try:
    from .agent_fields import build_agent_fields
    from .usage_events import event_candidates, finish_events
    from .context_evidence import candidate_spans, clause_spans
    from .jev_client import ask
    from .product_mentions import extract_products
    from .segmenter import noun_candidates, segmentation_method, units
    from .semantic_rules import apply_rules, symptom_scopes
except ImportError:
    from agent_fields import build_agent_fields
    from usage_events import event_candidates, finish_events
    from context_evidence import candidate_spans, clause_spans
    from jev_client import ask
    from product_mentions import extract_products
    from segmenter import noun_candidates, segmentation_method, units
    from semantic_rules import apply_rules, symptom_scopes

SUBJECT = {'self': '사용자 본인', 'other': '타인의 경험 또는 인용', 'unknown': '누구인지 불명확'}
STATE = {'affirmed': '실제 사용 또는 증상을 긍정하여 보고', 'denied': '명시적으로 부정',
         'planned': '앞으로 사용할 계획', 'hypothetical': '가정 또는 일반 질문일 뿐 실제 보고 아님',
         'conflict': '정정으로 해소되지 않은 상충하는 보고', 'unknown': '모름 또는 불확실',
         'declined': '정보 제공 거절', 'not_mentioned': '해당 정보 언급 없음'}
SYMPTOMS = {'dryness': '건조함', 'breakout': '트러블', 'redness': '붉어짐',
            'stinging': '따가움', 'itching': '가려움'}
SYMPTOM_ANCHORS = {'dryness': r'건조|당기|땅기|푸석', 'breakout': r'트러블|여드름|뾰루지|좁쌀',
                   'redness': r'붉|빨개|빨갛|홍조', 'stinging': r'따가|따갑|따끔|화끈|쓰라',
                   'itching': r'가려|가렵|간지'}
MISSING = {'not_mentioned': '해당 관계의 시점을 말하지 않음', 'unknown': '모르거나 연결 불명확',
           'declined': '해당 시점 답변 거절', 'conflict': '서로 충돌하거나 여러 시점을 하나로 고를 수 없음'}


def time_spans(text, date=False):
    pattern = (r'그저께|어제|오늘|내일|모레|최근|요 며칠|\d+일 전|\d{4}[-./]\d{1,2}[-./]\d{1,2}'
               if date else r'오전\s*\d+(?:시)?|오후\s*\d+(?:시)?|아침|오전|점심|낮|오후|저녁|밤|새벽|\d+시(?:\s*\d+분)?')
    return [{'text': m[0], 'start': m.start(), 'end': m.end()} for m in re.finditer(pattern, text)]


def extract_features(text, key):
    units_list = units(text)
    products, product_warning = extract_products(text, key, units_list, include_non_usage=True, candidate_fn=noun_candidates)
    products.sort(key=lambda p: (p['start'], p['end']))
    result = {'schema_version': 'relations-0.5', 'source_text': text,
              'text_revision': hashlib.sha256(text.encode('utf-8')).hexdigest(),
              'offset_unit': 'unicode_codepoint', 'review_status': 'candidate',
              'segmentation_method': segmentation_method(),
              'units': [{'unit_id': u['unit_id'], 'start': u['start'], 'end': u['end'], 'text': u['text']} for u in units_list],
              'symptom_detection': 'lexicon_gated',
              'products': [], 'symptoms': [], 'warnings': [], 'clarifications': []}
    if product_warning:
        result['warnings'].append(product_warning)
    tasks = []

    def question(record, attr, prompt, criteria, options=None):
        tasks.append((record, attr, {'type': 'choice', 'instructions': (
            'state는 전체 원문이다. 부정·계획·정정·타인·시제의 범위를 구분하라. '
            '명시되지 않은 사실을 추정하지 말라. ') + prompt, 'criteria': criteria}, options))

    def temporal(record, attr, prompt, date=False):
        options = {f't{i}': span for i, span in enumerate(time_spans(text, date))}
        question(record, attr, prompt + ' 해당 대상과 관계에 직접 연결되는 원문 시간 표현 하나를 선택하라. '
                 '문장 다른 곳에 시간 단어가 있다는 이유로 연결하지 말라. 표현이 없으면 not_mentioned. '
                 '여러 사건의 시간이 다르면 conflict. 발견 시점을 실제 시작 시점으로 추정하지 말라.',
                 {**{k: f"{v['text']} (위치 {v['start']}:{v['end']})" for k, v in options.items()}, **MISSING}, options)

    for i, mention in enumerate(products):
        record = {**mention, 'mention_id': f'p{i}', 'relations': {}, 'eligible_for_usage_candidate': False}
        result['products'].append(record)
        scope = f"제품 {mention['text']!r}, 원문 위치 {mention['start']}:{mention['end']}, 구절 {mention['context']!r}. "
        question(record, 'usage_state', scope + '이 제품 언급의 최종 사용 상태를 판정하라.', STATE)
        question(record, 'subject', scope + '이 제품을 사용/계획/부정하는 주체는 누구인가?', SUBJECT)
        question(record, 'correction', scope + '이 언급은 정정에 의해 취소된 제품인가? A가 아니라 B라면 A는 superseded, B는 current.',
                 {'current': '취소되지 않은 언급', 'superseded': '정정으로 취소된 언급', 'unknown': '정정 관계 불명확'})
        temporal(record, 'usage_date', scope + '이 제품을 실제 사용/사용 부정/사용 계획한 날짜는?', True)
        temporal(record, 'usage_time', scope + '이 제품을 실제 사용/사용 부정/사용 계획한 하루 중 시간은?')

    spans = {f's{i}': span for i, span in enumerate(candidate_spans(text))}
    for name, source_scope in symptom_scopes(text, units_list, SYMPTOM_ANCHORS):
        label = SYMPTOMS[name]
        anchors = [a for a in re.finditer(SYMPTOM_ANCHORS[name], text)
                   if source_scope['start'] <= a.start() < source_scope['end']]
        if not anchors:
            continue
        record = {'symptom': name, 'symptom_id': f's{len(result["symptoms"])}',
                  'label': label, 'source_scope': source_scope, 'relations': {}}
        result['symptoms'].append(record)
        scope = (f'증상 {label}, 지정 구절 {source_scope["text"]!r}, 위치 {source_scope["start"]}:{source_scope["end"]}. '
                 '이 구절 속 증상 언급만 판정하라. 같은 증상의 다른 구절·대상·시점을 섞지 말라. ')
        question(record, 'state', scope + '이 증상 자체의 언급이 없으면 반드시 not_mentioned. 다른 증상이 있다는 이유로 이 증상도 있다고 판단하지 말라.',
                 {'affirmed': f'{label}이 있다고 명시함', 'denied': f'{label}이 없다고 명시적으로 부정함',
                  'hypothetical': f'{label}에 대한 가정/질문만 있음', 'conflict': f'{label}에 대한 해소되지 않은 충돌',
                  'unknown': f'{label} 여부를 모른다고 표현함', 'declined': f'{label} 여부의 답변을 거절함',
                  'not_mentioned': f'{label} 자체를 언급하지 않음. 다른 증상만 언급한 경우도 여기 해당'})
        question(record, 'subject', scope + '이 증상의 대상은 누구인가?', SUBJECT)
        question(record, 'severity', scope + '이 증상에 명시된 강도는? 다른 증상의 강도를 가져오거나 추정하지 말라.',
                 {'mild': f'{label}이 약간/가볍다고 명시', 'moderate': f'{label}이 중간이라고 명시',
                  'severe': f'{label}이 심하다고 명시',
                  'not_mentioned': f'{label} 강도 표현이 없음. 증상 부정은 강도 거절이 아님',
                  'unknown': f'{label} 강도를 모른다고 명시', 'declined': f'{label} 강도 답변을 거절한다고 명시',
                  'conflict': f'{label} 강도의 상충 표현'})
        anchored_spans = {k: span for k, span in spans.items()
                          if source_scope['start'] <= span['start'] and span['end'] <= source_scope['end']
                          and any(span['start'] <= a.start() < span['end'] for a in anchors)
                          and not any(re.search(pattern, span['text']) for other, pattern in SYMPTOM_ANCHORS.items() if other != name)}
        question(record, 'evidence', scope + '긍정 또는 부정을 직접 표현하는 구절 하나를 고르라. 부정 표현을 가능한 한 포함하라. 언급 없으면 none.',
                 {**{k: v['text'] for k, v in anchored_spans.items()}, 'none': '직접 근거 없음'}, anchored_spans)
        temporal(record, 'onset_date', scope + '이 증상이 실제 시작했다고 명시한 날짜는?', True)
        temporal(record, 'onset_time', scope + '이 증상이 실제 시작했다고 명시한 하루 중 시간은?')
        temporal(record, 'recognition_time', scope + '이 증상을 발견하거나 알아차린 하루 중 시간은?')

    events, event_warning = event_candidates(text, result['products'], units_list, time_spans)
    if event_warning:
        result['warnings'].append(event_warning)
    for event in events:
        product = next(p for p in result['products'] if p['mention_id'] == event['product_mention_id'])
        scope = (f"사용 사건 {event['event_id']}. 제품 {product['text']!r} "
                 f"언급 위치 {product['start']}:{product['end']}, 사건 구절 {event['source_scope']!r}, "
                 f"지정 시간 {event['time_anchor']!r}. "
                 '이 제품과 지정 시간에 해당하는 사건 하나만 판정하라. 다른 시간의 부정/계획을 섞지 말라. '
                 '제품 생략과 주어 변경은 전체 문맥을 확인하되 연결 불명확하면 unknown. ')
        question(event, 'product_link', scope + '이 사건이 지정 제품에 연결되는가?',
                 {'linked': '지정 제품의 사건', 'unlinked': '다른 제품 또는 사용 사건 아님', 'unknown': '연결 불명확'})
        question(event, 'usage_state', scope + '이 사건의 사용 상태는?', STATE)
        question(event, 'subject', scope + '이 사건의 주체는?', SUBJECT)
        question(event, 'correction', scope + '이 사건은 정정으로 취소되었는가?',
                 {'current': '취소되지 않은 사건', 'superseded': '정정으로 취소됨', 'unknown': '불명확'})
        temporal(event, 'usage_date', scope + '이 사건의 날짜는?', True)
        # Keep model verification of the time link; a lexical clock may describe
        # symptom recognition rather than product use.
        options = {'anchor': event['time_anchor']} if event['time_anchor'] else {}
        question(event, 'usage_time', scope + '지정 시간이 이 사용 사건의 시간인가? 없으면 not_mentioned.',
                 {**({'anchor': event['time_anchor']['text']} if options else {}), **MISSING}, options)

    for offset in range(0, len(tasks), 20):
        batch = tasks[offset:offset + 20]
        questions = {f'q{i}': task[2] for i, task in enumerate(batch)}
        try:
            answers = ask(text, questions, key)
            validated = []
            for i, (record, attr, q, options) in enumerate(batch):
                answer = answers[f'q{i}']
                choice = answer['choice']
                score = answer['probabilities'][choice]
                if answer.get('type') != 'choice' or choice not in q['criteria'] or isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
                    raise ValueError('잘못된 선택 응답')
                value = options.get(choice) if options is not None else choice
                validated.append((record, attr, {'value': value if value is not None else choice,
                    'score': score, 'status': 'uncertain' if score <= .5 else 'candidate'}))
            for record, attr, relation in validated:
                record['relations'][attr] = relation
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            result['warnings'].append(f'관계 질문 {offset + 1}~{offset + len(batch)} 실패 · 해당 필드는 미평가')
            for record, attr, _, _ in batch:
                record['relations'][attr] = {'value': None, 'score': None, 'status': 'unassessed'}
    apply_rules(result, SYMPTOM_ANCHORS, units_list, time_spans)
    finalize(result)
    finish_events(result, events)
    result['agent_fields'] = build_agent_fields(result)
    return result


def finalize(result):
    # Exact adjacent correction ("A가 아니라 B") or explicit speech correction ("A... 잘못 말했어. 실제로는 B").
    for left, right in zip(result['products'], result['products'][1:]):
        between = result['source_text'][left['end']:right['start']]
        if re.fullmatch(r'(?:이|가)?\s*(?:아니라|말고)\s*', between) or re.search(r'(?:잘못\s*말했|착각했).{0,30}(?:실제로|사실)', between):
            for record, value in [(left, 'superseded'), (right, 'current')]:
                previous = record['relations'].get('correction')
                record['relations']['correction'] = {'value': value, 'score': None,
                    'status': 'rule_candidate', 'method': 'explicit_correction', 'model_prediction': previous}
    for record in result['products']:
        rel = record['relations']
        record['time_applicability'] = ('superseded' if rel.get('correction', {}).get('value') == 'superseded'
                                        else rel.get('usage_state', {}).get('value', 'unknown'))
        record['eligible_for_usage_candidate'] = record['score'] > .5 and record.get('identification_status') != 'incomplete' and all(
            rel.get(attr, {}).get('value') == value and rel[attr]['status'] in ('candidate', 'rule_candidate')
            for attr, value in [('usage_state', 'affirmed'), ('subject', 'self'), ('correction', 'current')])
    for symptom in result['symptoms']:
        relevant = ([symptom['source_scope']['text']] if symptom.get('source_scope') else
                    [c['text'] for c in clause_spans(result['source_text'])
                     if re.search(SYMPTOM_ANCHORS[symptom['symptom']], c['text'])])
        if not any(re.search(r'시작|생겼|생기|발생|부터|나기', clause) for clause in relevant):
            for attr in ('onset_date', 'onset_time'):
                previous = symptom['relations'].get(attr)
                if previous and isinstance(previous['value'], dict):
                    symptom['relations'][attr] = {'value': 'unknown', 'score': None,
                        'status': 'uncertain', 'method': 'no_explicit_onset_anchor', 'model_prediction': previous}
    for record in result['products'] + result['symptoms']:
        for attr, relation in record['relations'].items():
            value = relation['value']
            if relation['status'] in ('uncertain', 'unassessed') or isinstance(value, str) and value in ('unknown', 'conflict'):
                result['clarifications'].append({'target': record.get('mention_id', record.get('symptom_id', record.get('symptom'))),
                    'field': attr, 'reason': relation['status'] if relation['status'] != 'candidate' else value})


def print_features(result):
    """Plain terminal cards: English schema names, verbatim source values."""
    import shutil
    import unicodedata

    width = max(42, min(shutil.get_terminal_size((88, 24)).columns - 2, 96))

    def wrap(value, limit):
        lines, current, used = [], '', 0
        for char in str(value):
            size = 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1
            if char == '\n' or used + size > limit:
                lines.append(current)
                current, used = '', 0
                if char == '\n':
                    continue
            current += char
            used += size
        lines.append(current)
        return lines

    def row(field, value):
        prefix = f'  {field:<20} : '
        lines = wrap(value, max(12, width - len(prefix)))
        print(prefix + lines[0])
        for line in lines[1:]:
            print(' ' * len(prefix) + line)

    def display(record, attr):
        rel = record['relations'].get(attr, {})
        value = rel.get('value')
        rendered = value.get('text', '') if isinstance(value, dict) else (value if value is not None else 'unassessed')
        status = rel.get('status')
        if status == 'unassessed':
            return 'unassessed [API/check required]'
        if status == 'uncertain':
            return f'{rendered} [review]'
        if status == 'rule_candidate':
            return f'{rendered} [rule]'
        return str(rendered)

    symptoms = [s for s in result['symptoms'] if s['relations'].get('state', {}).get('value') != 'not_mentioned']
    print('\n' + '=' * width)
    print('  FEATURE EXTRACTION  /  candidate')
    print('=' * width)
    row('products', len(result['products']))
    row('symptoms', len(symptoms))
    row('review_fields', len(result.get('clarifications', [])))
    print('\nINPUT')
    print('-' * width)
    for line in wrap(result['source_text'], width - 2):
        print('  ' + line)
    print('\nPRODUCTS')
    if not result['products']:
        print('  No specific product names extracted. 확인이 필요할 수 있습니다.')
    for index, product in enumerate(result['products'], 1):
        print('-' * width)
        print(f"  PRODUCT {index}  |  {product['value']}")
        row('product_name', product['value'] + (' [review]' if product['score'] <= .5 else ''))
        row('source_span', f"[{product['start']}:{product['end']}]")
        for attr in ('usage_state', 'subject', 'correction'):
            row(attr, display(product, attr))
        if product.get('time_applicability') == 'superseded':
            row('usage_date', 'not_applicable [superseded]')
            row('usage_time', 'not_applicable [superseded]')
        else:
            for attr in ('usage_date', 'usage_time'):
                row(attr, display(product, attr))
        row('identification', product.get('identification_status', 'unverified'))
        row('db_match', product.get('match_status', 'not_attempted'))
        for event in result.get('usage_events', []):
            if event['product_mention_id'] == product['mention_id']:
                def event_time(field):
                    value = event.get(field)
                    return value['text'] if isinstance(value, dict) else str(value or 'unassessed')
                state = event.get('relations', {}).get('usage_state', {}).get('value')
                row('usage_event', f"{event_time('usage_date')} / {event_time('usage_time')} / {state} [candidate]")
    print('\nSYMPTOMS')
    if not symptoms:
        print('  No supported symptom expressions detected.')
    for index, symptom in enumerate(symptoms, 1):
        print('-' * width)
        print(f"  SYMPTOM {index}  |  {symptom['symptom']}")
        if symptom.get('source_scope'):
            row('source_scope', symptom['source_scope']['text'])
        for attr in ('evidence', 'state', 'subject', 'severity', 'onset_date', 'onset_time', 'recognition_time'):
            row(attr, display(symptom, attr))
    if result.get('intake_status', {}).get('symptoms', {}).get('value') == 'declined':
        print('\nINTAKE STATUS')
        row('symptom_information', 'declined [rule]')
    if result['warnings']:
        print('\nWARNINGS')
        print('-' * width)
        for warning in result['warnings']:
            row('warning', warning)
    print('\n' + '=' * width)
    print('  [review] 확인 필요  /  [rule] 원문 규칙 적용')
    print('  미확정 추출 후보입니다. 상세 점수·JSON: --verbose / --json')
    print('=' * width)
