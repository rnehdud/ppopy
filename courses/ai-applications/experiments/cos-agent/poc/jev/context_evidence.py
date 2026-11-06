"""Experimental evidence selection; scores are not internal attribution."""
import json
import re

import httpx


def clause_spans(text):
    spans = []
    for match in re.finditer(r'[^,，;；.!?。！？\n]+(?:[,，;；.!?。！？]|$)', text):
        start = match.start() + len(match[0]) - len(match[0].lstrip())
        end = match.end() - len(match[0]) + len(match[0].rstrip())
        if start < end:
            spans.append({'text': text[start:end], 'start': start, 'end': end})
    return spans


def candidate_spans(text):
    spans = []
    for clause in clause_spans(text):
        words = list(re.finditer(r'\S+', clause['text']))
        for i in range(len(words)):
            for j in range(i + 1, min(i + 3, len(words)) + 1):
                start = clause['start'] + words[i].start()
                end = clause['start'] + words[j - 1].end()
                spans.append({'text': text[start:end], 'start': start, 'end': end})
    return spans


def select_evidence(text, key, definitions, candidates, progress=None):
    spans = candidate_spans(text)
    questions, mapping = {}, {}
    found = {c['field']: [] for c in candidates}
    for candidate in candidates:
        name = candidate['field']
        original = 'product_name_mentioned' if name == 'product_name' else name
        definition = definitions[original]
        target = definition.get('criteria', {}).get(candidate['value'], '이 질문의 긍정 판정')
        base = (f"필드 정의: {definition['instructions']}\n목표 판정: {target}\n"
                '전체 원문의 부정, 정정, 시제, 대상과 가정을 고려하라. '
                '사용자가 명시한 표현만 근거로 삼고 날짜나 사실을 추가로 추정하지 말라. ')
        if name == 'product_used':
            for clause in clause_spans(text):
                qid = f'q{len(questions)}'
                questions[qid] = {'type': 'noul', 'instructions': base +
                    '지정 구절 자체에 사용자가 제품을 실제 사용했다는 사건이 표현되어 있는가? '
                    '다른 구절의 사용 보고나 증상 보고만으로 긍정하지 말라. 지정 구절: '
                    + json.dumps(clause['text'], ensure_ascii=False)}
                mapping[qid] = (name, clause)
        elif spans:
            qid = f'q{len(questions)}'
            questions[qid] = {'type': 'choice', 'instructions': base +
                '목표 판정을 직접 표현하는 가장 짧고 구체적인 원문 구절 하나를 고르라. '
                '단순 동사나 주변 표현보다 해당 의미를 가진 단어를 포함한 구절을 우선하라. '
                '직접 표현이 없거나 목표가 추정일 뿐이면 none을 선택하라.',
                'criteria': {**{f's{i}': span['text'] for i, span in enumerate(spans)},
                             'none': '목표 판정을 직접 표현하는 구절이 없거나 목표가 명시되지 않음'}}
            mapping[qid] = (name, None)
    if not questions:
        return found, None
    if progress:
        progress(f'후보 비교 및 사용 사건 확인: {len(questions)}질문')
    try:
        response = httpx.post('https://api.typesafe.ai/v1/systemone',
            headers={'Authorization': f'Bearer {key}'},
            json={'model': 'jev-latest', 'state': text, 'questions': questions}, timeout=60.0)
        response.raise_for_status()
        answers = response.json()['answers']
        if not isinstance(answers, dict) or set(answers) != set(questions):
            raise ValueError('응답 질문 불일치')
        for qid, (name, clause) in mapping.items():
            answer = answers[qid]
            if clause is not None:
                score, span, mode = answer['noul'], clause, '사용 사건 점수'
                if answer.get('type') != 'noul':
                    raise ValueError('잘못된 응답 형식')
            else:
                choice = answer['choice']
                if answer.get('type') != 'choice' or choice not in questions[qid]['criteria']:
                    raise ValueError('잘못된 선택값')
                if choice == 'none':
                    continue
                score = answer['probabilities'][choice]
                span, mode = spans[int(choice[1:])], '후보 선택 점수'
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
                raise ValueError('잘못된 점수')
            found[name].append({**span, 'score': score, 'mode': mode})
    except (httpx.HTTPError, ValueError, KeyError, TypeError, IndexError):
        return {}, '근거 판정 실패 · 이번 결과는 미평가입니다.'
    return found, None
