"""Conditional choice views using existing labels, never parsing prose as gold."""
import json
from scripts.build_tool_decision_mix_v1 import stable
from scripts.when2call_operational_data_v1 import action_row

SELECT_QUESTION = '사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.'
GATE_QUESTION = '사용자 요청, 대화, 도구 정의를 보고 이 도구를 지금 호출해야 하는지 선택하세요.'
YES = '지금 이 도구를 호출한다.'
NO = '지금 이 도구를 호출하지 않는다. 요청과 맞지 않거나 필요한 정보가 없으면 호출하지 않는다.'


def selector_view(original):
    row, reason = action_row(original)
    if reason:
        raise ValueError(reason)
    row['options'] = {k: v for k, v in row['options'].items() if k != 'no_tool'}
    row['question'] = SELECT_QUESTION
    return row


def gate_view(original, tool_index, target=None):
    row = selector_view(original)
    tool_key = f'tool_{tool_index:03d}'
    definition = row['options'][tool_key]
    return {**row, 'question': GATE_QUESTION,
            'options': {'yes': YES + '\n' + definition, 'no': NO + '\n' + definition},
            'target': target, 'conditioned_tool_key': tool_key,
            'conditioned_tool_name': row['tool_keys'][tool_key],
            'label_scope': 'Source-preferred native call vs ordinary response; missing-information and irrelevance not separately inferred.'}


def gold_index(row):
    calls = row.get('reference_calls') or []
    if len(calls) != 1:
        raise ValueError('Expected one existing source call')
    names = [t['name'] for t in row['tools']]
    return names.index(calls[0]['name'])


def fits(row, tokenizer, limit=512):
    encoded = tokenizer([row['question'] + ' ' + v for v in row['options'].values()],
                        [row['context']] * len(row['options']), truncation=False, padding=False)
    return max(map(len, encoded['input_ids'])) <= limit


def canonical(row):
    return stable([row['messages'], sorted((stable(t) for t in row['tools']))])
