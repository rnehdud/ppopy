"""Fresh Korean, real-file tasks with required arguments and revised requests."""
import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
SPEC = {
    'multiplication': ('정수 자료', [2, 3, 4], 'product', 'sum', {'value': 24}, {'value': 9},
                       'product는 모든 값을 곱하고 sum은 모든 값을 더한다.'),
    'negative_values': ('온도 자료', [-3, 0, 5, -1], 'negative', 'positive', {'values': [-3, -1]}, {'values': [5]},
                       'negative는 음수만, positive는 양수만 원래 순서대로 고른다.'),
    'edge_values': ('측정 자료', [5, 2, 9], 'first', 'last', {'value': 5}, {'value': 9},
                    'first는 첫 번째 값, last는 마지막 값을 고른다.'),
    'word_order': ('단어 자료', ['pear', 'apple', 'banana'], 'ascending', 'descending',
                   {'words': ['apple', 'banana', 'pear']}, {'words': ['pear', 'banana', 'apple']},
                   'ascending은 사전순, descending은 역 사전순으로 정렬한다.'),
    'text_cleanup': ('문자열 자료', [' a ', 'b  '], 'strip', 'upper', {'texts': ['a', 'b']}, {'texts': [' A ', 'B  ']},
                     'strip은 양쪽 공백만 없애고 upper는 공백을 보존하며 대문자로 바꾼다.'),
    'size_stats': ('항목 자료', ['a', 'b', 'a'], 'unique_count', 'total_count', {'count': 2}, {'count': 3},
                   'unique_count는 서로 다른 값의 수, total_count는 전체 항목 수를 계산한다.'),
}


def names(family):
    return {r: 'z' + hashlib.sha256(('v65:' + family + ':' + r).encode()).hexdigest()[:9] for r in 'abc'}


def definitions(family):
    noun, _, main, alternate, _, _, description = SPEC[family]
    ids = names(family)
    return [
        {'name': ids['a'], 'description': f'현재 대화의 {noun} 파일을 읽어 작업 메모리에 넣고 전체 내용을 반환한다. 저장 파일은 만들지 않는다.',
         'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
        {'name': ids['b'], 'description': f'작업 메모리에 읽어 둔 {noun}을 mode에 따라 처리하여 결과 파일에 저장한다. {description} '
                      f'먼저 {ids["a"]}로 읽어야 한다. 이전 발언에서 읽은 자료도 쓸 수 있다. 원본은 바꾸지 않는다.',
         'inputSchema': {'type': 'object', 'properties': {'mode': {'type': 'string', 'enum': [main, alternate]}},
                         'required': ['mode'], 'additionalProperties': False}},
        {'name': ids['c'], 'description': f'원본 {noun}의 항목 수만 반환한다. 작업 메모리에 읽어 두거나 결과를 저장하지 않는다.',
         'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    ]


class Registry:
    def __init__(self, definitions, handlers):
        self.ds = copy.deepcopy(definitions); self.handlers = handlers
        self.schemas = {d['name']: d['inputSchema'] for d in self.ds}

    def definitions(self):
        return copy.deepcopy(self.ds)

    def invoke(self, name, arguments):
        if name not in self.schemas:
            raise ValueError('unregistered_tool')
        Draft202012Validator(self.schemas[name]).validate(arguments)
        return self.handlers[name](**arguments)


class Files:
    def __init__(self, root, family, payload):
        self.root = Path(root).resolve(); self.root.mkdir(parents=True, exist_ok=False)
        self.family = family; self.cache = None
        self.input = self.root / 'input.json'; self.output = self.root / 'result.json'
        self.input.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        self.original = self.input.read_bytes()

    @property
    def state(self):
        return {'loaded': self.cache is not None, 'saved': self.output.exists()}

    def registry(self, available, order):
        ds = {d['name']: d for d in definitions(self.family)}; ids = names(self.family)
        handlers = {ids['a']: self.read, ids['b']: self.process, ids['c']: self.count}
        return Registry([ds[ids[r]] for r in order], handlers)

    def read(self):
        self.cache = json.loads(self.input.read_text(encoding='utf-8'))
        return {'ok': True, **copy.deepcopy(self.cache)}

    def count(self):
        return {'ok': True, 'count': len(json.loads(self.input.read_text(encoding='utf-8'))['items'])}

    def process(self, mode):
        if self.cache is None:
            return {'ok': False, 'reason': 'read_required'}
        x = self.cache['items']
        if not x:
            return {'ok': False, 'reason': 'empty'}
        if mode == 'product':
            import math
            value = {'value': math.prod(x)}
        elif mode == 'sum': value = {'value': sum(x)}
        elif mode == 'negative': value = {'values': [v for v in x if v < 0]}
        elif mode == 'positive': value = {'values': [v for v in x if v > 0]}
        elif mode == 'first': value = {'value': x[0]}
        elif mode == 'last': value = {'value': x[-1]}
        elif mode == 'ascending': value = {'words': sorted(x)}
        elif mode == 'descending': value = {'words': sorted(x, reverse=True)}
        elif mode == 'strip': value = {'texts': [s.strip() for s in x]}
        elif mode == 'upper': value = {'texts': [s.upper() for s in x]}
        elif mode == 'unique_count': value = {'count': len(set(x))}
        elif mode == 'total_count': value = {'count': len(x)}
        else: raise ValueError('unsupported_mode')
        self.output.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        return {'ok': True, 'saved': True, **value}

    def snapshot(self):
        return {'state': self.state, 'input_unchanged': self.input.read_bytes() == self.original,
                'output': json.loads(self.output.read_text(encoding='utf-8')) if self.output.exists() else None}


def cases():
    import random
    result = []
    for family, (noun, values, main, alternate, answer, alternative, _) in SPEC.items():
        specs = [
            ('read', [f'{noun} 파일 내용을 읽어서 보여 주세요. 저장은 하지 마세요.'], [['a']], [None], values, 'abc'),
            ('main', [f'먼저 {noun}을 읽고 mode를 {main}으로 지정해서 결과를 저장해 주세요.'], [['a', 'b']], [answer], values, 'abc'),
            ('alternate', [f'{noun}을 읽은 뒤 {alternate} 방식으로 처리해서 저장해 주세요.'], [['a', 'b']], [alternative], values, 'abc'),
            ('nonempty', [f'{noun}을 먼저 읽고, 항목이 있으면 {main}으로 처리해 저장하세요. 비어 있으면 저장하지 마세요.'], [['a', 'b']], [answer], values, 'abc'),
            ('empty', [f'{noun}을 먼저 읽고, 항목이 있으면 {main}으로 처리해 저장하세요. 비어 있으면 저장하지 마세요.'], [['a']], [None], [], 'abc'),
            ('ask', ['아직 무엇을 할지 결정하지 않았어요. 먼저 제게 원하는 작업을 물어보세요. 도구는 실행하지 마세요.'], [[]], [None], values, 'abc'),
            ('missing', [f'{noun}을 {main}으로 처리해서 저장하고 싶어요. 저장 도구가 없으면 다른 도구는 실행하지 마세요.'], [[]], [None], values, 'ac'),
            ('revise', [f'{noun}을 읽어 주세요. {main} 처리를 고려 중이지만 지금은 절대 저장하지 마세요.',
                        f'앞서 말한 {main} 방식은 쓰지 않을게요. 방금 읽은 자료를 {alternate} 방식으로 처리하고 지금 저장해 주세요.'],
                        [['a'], ['b']], [None, alternative], values, 'abc'),
        ]
        for kind, texts, roles, outputs, payload, available in specs:
            order = list(available); seed = 650065 + len(result); random.Random(seed).shuffle(order)
            result.append({'id': 'v65:' + family + ':' + kind, 'family': family, 'kind': kind,
                'payload': {'items': copy.deepcopy(payload)}, 'available': list(available), 'order': order, 'order_seed': seed,
                'turns': [{'text': t, 'roles': r, 'output': copy.deepcopy(o)} for t, r, o in zip(texts, roles, outputs)],
                'labels': 'assistant-authored Korean controlled tasks; manual numeric/string expected outputs; not independent human review'})
    return result


def evaluate_turn(expected, trace, service):
    # Reuse outcome scoring but use this version's registered identifiers.
    snapshot = service.snapshot(); events = trace.get('events', []); ids = names(service.family)
    inverse = {n: r for r, n in ids.items()}; roles = [inverse.get(e['tool'], '?') for e in events]
    required = expected['roles']; position = 0
    for role in roles:
        if position < len(required) and role == required[position]: position += 1
    successful = all(e['result'].get('ok') is True for e in events)
    no_call_ok = bool(required) or not events
    correct = snapshot['input_unchanged'] and snapshot['output'] == expected['output']
    goal = position == len(required) and successful and no_call_ok and correct and bool(trace.get('steps'))
    writes = [e for e in events if e['tool'] == ids['b'] and e.get('executed')]
    return {'goal_and_stop': goal and trace.get('model_stopped') is True, 'goal_ok': goal,
            'roles': roles, 'file_correct': correct,
            'required_save': expected['output'] is not None,
            'requested_correct_write': expected['output'] is not None and correct and any(e['result'].get('saved') for e in writes),
            'unwanted_write': expected['output'] is None and any(e['result'].get('saved') for e in writes),
            'unwanted_write_attempt': expected['output'] is None and any(s['choice'] == ids['b'] for s in trace.get('steps', []))}
