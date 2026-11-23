"""Strict tool-call accuracy for the fixed kotraj reproduction task."""
from collections import Counter
import json


def canonical_calls(calls):
    return Counter(json.dumps(c, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
                   for c in calls)


def parse_calls(text):
    text = text.strip()
    if not text:
        raise ValueError('Empty response is not a no-call decision')
    if not text.startswith('['):
        if text.startswith(('{', '```', '<tool_call')):
            raise ValueError('Malformed tool-call format')
        return []  # Native format permits normal prose for no-call.
    def invalid_constant(value):
        raise ValueError('Non-JSON constant: '+value)
    def unique_pairs(pairs):
        obj = {}
        for k, v in pairs:
            if k in obj:
                raise ValueError('Duplicate JSON key')
            obj[k] = v
        return obj
    calls = json.loads(text, parse_constant=invalid_constant, object_pairs_hook=unique_pairs)
    if not isinstance(calls, list):
        raise ValueError('Expected array')
    for c in calls:
        if (not isinstance(c, dict) or set(c) != {'name', 'arguments'}
                or not isinstance(c['name'], str) or not isinstance(c['arguments'], dict)):
            raise ValueError('Invalid call object')
    return calls


def grade(expected, generation):
    try:
        if not generation['finished']:
            raise ValueError('Generation did not finish')
        predicted = parse_calls(generation['text'])
        correct = canonical_calls(predicted) == canonical_calls(expected)
        return {'correct': correct, 'expected_call': bool(expected), 'predicted': predicted, 'error': None}
    except Exception as e:
        return {'correct': False, 'expected_call': bool(expected), 'predicted': None, 'error': str(e)}


def summarize(rows):
    def counts(values):
        n = len(values)
        correct = sum(r['grade']['correct'] for r in values)
        return {'n': n, 'correct': correct, 'accuracy': correct/n if n else None}
    return {'all': counts(rows), 'call': counts([r for r in rows if r['grade']['expected_call']]),
            'no_call': counts([r for r in rows if not r['grade']['expected_call']])}


def passes(result):
    return all(result[k]['n'] > 0 and result[k]['correct']*10 > result[k]['n']*9 for k in ['all', 'call'])
