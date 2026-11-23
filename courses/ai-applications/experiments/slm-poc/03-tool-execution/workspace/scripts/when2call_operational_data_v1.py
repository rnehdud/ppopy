"""Read source chosen tool calls as actions; ordinary chosen text means no call.

No refusal/RFI keyword classification and no invented examples. Coarse no-call
includes both asking and declining; it does NOT distinguish those two actions.
"""
import collections
import hashlib
import json
from scripts.build_tool_decision_mix_v1 import stable

def action_row(row):
    if not row['tools']:
        return None, 'no_available_tool_deterministic_non_call'
    if len(row['tools']) > 7:
        return None, 'more_than_seven_tools'
    options, mapping = {}, {}
    for i, tool in enumerate(row['tools']):
        key = f'tool_{i:03d}'
        options[key] = tool['description'] + ' 필수 인자: ' + stable(tool['parameters'].get('required') or []) + '\n인자 정의: ' + stable(tool['parameters']) + '\n도구 이름: ' + tool['name']
        mapping[key] = tool['name']
    options['no_tool'] = '지금은 도구를 호출하지 않고 사용자에게 직접 답하거나 필요한 정보를 확인한다.'
    calls = row.get('reference_calls') or []
    if calls:
        if len(calls) != 1:
            return None, 'multiple_source_calls'
        target = next(k for k, name in mapping.items() if name == calls[0]['name'])
        group = 'call'
    else:
        target = 'no_tool'
        # Only preserve an existing explicit diagnostic label. Never infer it
        # from source response wording or punctuation.
        group = row['target'] if row['target'] in ('ask', 'no_tool') else 'no_call'
    messages = row['messages']
    if messages[-1]['role'] == 'user':
        context = '대화:\n' + stable(messages[:-1]) + '\n이번 사용자 발화: ' + messages[-1]['content']
    else:
        context = '대화:\n' + stable(messages)
    return {**row, 'kind': 'operational_choice', 'question': '사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.',
            'options': options, 'target': target, 'context': context, 'tool_keys': mapping,
            'original_target': row['target'], 'metric_group': group,
            'action_label_provenance': 'Exact selected source tool-call name, or no native tool call in the chosen source response. Asking and declining merged.'}, None

def convert(rows, tokenizer):
    converted, skipped = [], collections.Counter()
    for row in rows:
        transformed, reason = action_row(row)
        if transformed is None:
            skipped[reason] += 1
            continue
        encoded = tokenizer([transformed['question'] + ' ' + value for value in transformed['options'].values()],
                            [transformed['context']] * len(transformed['options']), padding=False, truncation=False)
        n = max(map(len, encoded['input_ids']))
        if n > 512:
            skipped['over_512_no_truncation'] += 1
            continue
        transformed['max_input_tokens'] = n
        converted.append(transformed)
    groups = collections.defaultdict(list)
    for row in converted:
        key = hashlib.sha256(stable([row['question'], row['context'], sorted(row['options'].values())]).encode('utf8')).hexdigest()
        groups[key].append(row)
    result = []
    for items in groups.values():
        labels = {r['options'][r['target']] for r in items}
        if len(labels) != 1:
            skipped['conflicting_source_action_labels'] += len(items)
        else:
            result.append(items[0])
            skipped['duplicate_action_input'] += len(items) - 1
    return result, dict(skipped)
