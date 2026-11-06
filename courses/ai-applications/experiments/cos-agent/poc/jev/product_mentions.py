"""Extract verbatim product-name candidates for a later catalog lookup."""
import json
import re

import httpx


def name_candidates(text, event):
    words = list(re.finditer(r'\S+', text[event['start']:event['end']]))
    spans = {}
    for i in range(len(words)):
        for j in range(i + 1, min(i + 6, len(words)) + 1):
            start = event['start'] + words[i].start()
            end = event['start'] + words[j - 1].end()
            while end > start and text[end - 1] in ',.!?;，。！？':
                end -= 1
            ends = {end}
            # Alternative boundaries only: Jev decides if a suffix is a particle.
            for suffix in ('으로', '에서', '이랑', '하고', '과', '와', '을', '를', '로', '은', '는', '도', '만', '가', '이'):
                if text[start:end].endswith(suffix) and end - len(suffix) > start:
                    ends.add(end - len(suffix))
            for boundary in sorted(ends):
                spans[start, boundary] = {'text': text[start:boundary], 'start': start, 'end': boundary}
    return list(spans.values())


def extract_products(text, key, events, max_rounds=8, include_non_usage=False):
    """Choose multiple nonoverlapping names within affirmed use events."""
    active = {f'e{i}': (event, name_candidates(text, event)) for i, event in enumerate(events)}
    products = []
    for _ in range(max_rounds):
        questions = {}
        options = {}
        for qid, (event, spans) in active.items():
            options[qid] = {f'p{i}': span for i, span in enumerate(spans)}
            questions[qid] = {'type': 'choice', 'instructions': (
                'state는 전체 사용자 원문이다. 지정 사용 사건에서 사용자가 실제 사용했다고 보고한 '
                '제품 하나의 제품명만 선택하라. A로션, B 스킨처럼 사용자가 붙인 임시 이름도 허용한다. '
                '브랜드·수식어·제품 종류가 함께 있어야 이름이 완전하면 모두 포함하라. '
                '제품 여러 개를 한 선택지로 고르지 말고 하나씩 고르라. 조사(과/을/으로 등), 날짜, '
                '사용 동사와 주변 문맥은 제외하라. 단순 로션/크림 같은 일반 종류만 있거나 '
                '사용 부정·계획·타인의 사용만 있으면 none. 원문 밖의 정식 제품명을 추정하지 말라. '
                '이미 선택한 제품과 겹치는 후보는 제거되어 있다. 남은 제품이 없으면 none. 지정 사건: '
                + json.dumps(event['text'], ensure_ascii=False)),
                'criteria': {**{pid: span['text'] for pid, span in options[qid].items()},
                             'none': '선택 가능한 특정 제품명이 더 없음'}}
            if include_non_usage:
                questions[qid]['instructions'] = (
                    '전체 원문 문맥에서 지정 구절에 언급된 화장품 이름 하나를 고르라. '
                    '실제 사용뿐 아니라 사용 부정, 계획, 정정 전 이름, 타인, 가정 속 제품도 추출하라. '
                    'A/B 같은 제품 임시 이름도 허용하되 대명사 그거/이것과 로션/크림 같은 일반 종류는 none. '
                    '이름 전체를 포함하고 조사, 날짜, 동사, 여러 제품의 결합은 제외하라. '
                    '이미 선택한 범위와 겹치는 후보는 제거됐다. 남은 이름이 없으면 none. '
                    '원문에 없는 이름을 추정하지 말라. 지정 구절: '
                    + json.dumps(event['text'], ensure_ascii=False))
        if not questions:
            return products, None
        try:
            response = httpx.post('https://api.typesafe.ai/v1/systemone',
                headers={'Authorization': f'Bearer {key}'},
                json={'model': 'jev-latest', 'state': text, 'questions': questions}, timeout=60.0)
            response.raise_for_status()
            answers = response.json()['answers']
            if not isinstance(answers, dict) or set(answers) != set(questions):
                raise ValueError('응답 질문 불일치')
            next_active, selected = {}, []
            for qid, (event, spans) in active.items():
                answer = answers[qid]
                choice = answer['choice']
                if answer.get('type') != 'choice' or choice not in questions[qid]['criteria']:
                    raise ValueError('잘못된 선택값')
                if choice == 'none':
                    continue
                span = options[qid][choice]
                score = answer['probabilities'][choice]
                if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
                    raise ValueError('잘못된 점수')
                selected.append({**span, 'value': ' '.join(span['text'].split()),
                    'score': score, 'mode': '제품명 선택 점수', 'context': event['text'],
                    'status': 'candidate', 'product_id': None, 'product_version': None,
                    'match_status': 'not_attempted'})
                remaining = [s for s in spans if s['end'] <= span['start'] or s['start'] >= span['end']]
                if remaining:
                    next_active[qid] = (event, remaining)
            products.extend(selected)
            active = next_active
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            return products, '제품명 추출 일부 실패 · 누락 가능'
    return products, '제품명 추출 횟수 한도 도달 · 누락 가능' if active else None
