"""Build auditable choice-ranking candidates; never execute a dataset tool call.

Labels from synthetic sources are not independent human gold. Missing behavior
labels are NOT reconstructed from question marks or refusal keywords.
"""
import argparse
import ast
import collections
import csv
import hashlib
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/tool-decision-mix-v1'
DEST = ROOT / 'data/processed/tool-decision-mix-v1'
REVIEW = ROOT / 'configs/tool-decision-mix-v1-review.json'
SEED = 20261107
QUESTION = '대화와 사용 가능한 도구를 보고, 지금 할 다음 동작 하나를 선택하세요.'
PREF_QUESTION = '대화와 사용 가능한 도구를 보고, 제시된 두 응답 중 더 적절한 다음 응답을 선택하세요.'
ASK = '지금 도구를 호출하지 않는다. 요청에 필요한 정보가 빠져 있어 사용자에게 그 정보를 묻는다.'
NONE = '지금 도구를 호출하지 않는다. 사용 가능한 도구로 요청을 수행할 수 없거나 도구가 필요하지 않다.'

def stable(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(value):
    return hashlib.sha256((value if isinstance(value, str) else stable(value)).encode('utf8')).hexdigest()

def norm(value):
    return re.sub(r'\W+', '', unicodedata.normalize('NFKC', value).casefold())

def read_jsonl(path):
    with path.open(encoding='utf8') as f:
        return [json.loads(line) for line in f if line.strip()]

class Rejected(ValueError):
    pass

def tools_normalized(items):
    if not isinstance(items, list):
        raise Rejected('tools_not_list')
    result = []
    for tool in items:
        tool = json.loads(tool) if isinstance(tool, str) else tool
        tool = tool.get('function', tool)
        if not isinstance(tool.get('name'), str) or not tool['name'].strip() or not tool.get('description'):
            raise Rejected('tool_missing_name_or_description')
        params = tool.get('parameters') or {'type': 'object', 'properties': {}}
        params = dict(params)
        if 'required' not in params and isinstance(tool.get('required'), list):
            params['required'] = tool['required']
        result.append({'name': tool['name'], 'description': tool['description'], 'parameters': params})
    if len({t['name'] for t in result}) != len(result):
        raise Rejected('duplicate_tool_names')
    return result

def toolace_tools(system):
    marker = 'Here is a list of functions in JSON format that you can invoke:'
    if marker not in system:
        raise Rejected('toolace_schema_marker_missing')
    suffix = system.split(marker, 1)[1].lstrip()
    value, _ = json.JSONDecoder().raw_decode(suffix)
    return tools_normalized(value)

def literal(node):
    # No eval/exec and no function execution, including in nested arguments.
    if isinstance(node, ast.Name) and node.id in ('true', 'false', 'null'):
        return {'true': True, 'false': False, 'null': None}[node.id]
    if isinstance(node, ast.List):
        return [literal(x) for x in node.elts]
    if isinstance(node, ast.Dict):
        return {literal(k): literal(v) for k, v in zip(node.keys, node.values)}
    try:
        value = ast.literal_eval(node)
        stable(value)  # Refuse tuples/sets/non-JSON literals below.
        if isinstance(value, (tuple, set, bytes, complex)):
            raise Rejected('non_json_literal')
        return value
    except (ValueError, TypeError, SyntaxError) as exc:
        raise Rejected('unsafe_or_nonliteral_argument') from exc

def parse_toolace_calls(text, names):
    text = text.strip()
    if not text.startswith('[') or not text.endswith(']'):
        raise Rejected('not_call_syntax')
    pos = 1
    calls = []
    while True:
        while pos < len(text) - 1 and text[pos] in ' \n\r\t,':
            pos += 1
        if pos >= len(text) - 1:
            break
        matches = [name for name in names if text.startswith(name, pos) and text[pos + len(name):].lstrip().startswith('(')]
        if len(matches) != 1:
            raise Rejected('unknown_or_ambiguous_call_name')
        name = matches[0]
        opening = pos + len(name)
        while text[opening].isspace():
            opening += 1
        depth, quote, escaped, closing = 0, None, False, None
        for i in range(opening, len(text) - 1):
            c = text[i]
            if quote:
                if escaped:
                    escaped = False
                elif c == '\\':
                    escaped = True
                elif c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    closing = i
                    break
        if closing is None:
            raise Rejected('unbalanced_call')
        try:
            tree = ast.parse('f' + text[opening:closing + 1], mode='eval').body
        except SyntaxError as exc:
            raise Rejected('call_syntax_error') from exc
        if not isinstance(tree, ast.Call) or tree.args or any(k.arg is None for k in tree.keywords):
            raise Rejected('positional_or_expanded_arguments')
        if len({k.arg for k in tree.keywords}) != len(tree.keywords):
            raise Rejected('duplicate_argument')
        calls.append({'name': name, 'arguments': {k.arg: literal(k.value) for k in tree.keywords}})
        pos = closing + 1
        if pos < len(text) - 1 and text[pos] not in ' \n\r\t,':
            raise Rejected('unexpected_call_suffix')
    if not calls:
        raise Rejected('empty_call')
    return calls

def validate_value(value, schema):
    if not isinstance(schema, dict):
        raise Rejected('bad_schema')
    typ = str(schema.get('type', '')).lower().replace(', optional', '').strip()
    if typ.startswith('list['):
        typ = 'array'
    types = {'dict': 'object', 'str': 'string', 'int': 'integer', 'float': 'number', 'bool': 'boolean', 'list': 'array'}
    typ = types.get(typ, typ)
    if 'enum' in schema and value not in schema['enum']:
        raise Rejected('invalid_enum')
    checks = {'object': lambda v: isinstance(v, dict), 'string': lambda v: isinstance(v, str),
              'integer': lambda v: isinstance(v, int) and not isinstance(v, bool),
              'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
              'boolean': lambda v: isinstance(v, bool), 'array': lambda v: isinstance(v, list)}
    if typ and typ not in checks:
        raise Rejected('unsupported_schema_type')
    if typ and not checks[typ](value):
        raise Rejected('argument_type_mismatch')
    if isinstance(value, dict):
        props = schema.get('properties') or {}
        if not set(schema.get('required') or []).issubset(value):
            raise Rejected('missing_required_argument')
        if props and any(k not in props for k in value):
            raise Rejected('unknown_argument')
        for key, item in value.items():
            if key in props:
                validate_value(item, props[key])
    if isinstance(value, list) and isinstance(schema.get('items'), dict):
        for item in value:
            validate_value(item, schema['items'])

def validate_calls(calls, tools):
    if len(calls) != 1:
        raise Rejected('multiple_calls_not_single_selection')
    mapping = {t['name']: t for t in tools}
    for call in calls:
        if call['name'] not in mapping:
            raise Rejected('undefined_tool_call')
        validate_value(call['arguments'], mapping[call['name']]['parameters'])

def native_calls(message):
    result = []
    for call in message.get('tool_calls') or []:
        f = call.get('function', {})
        args = f.get('arguments', {})
        args = json.loads(args) if isinstance(args, str) else args
        if not isinstance(args, dict):
            raise Rejected('arguments_not_object')
        result.append({'name': f['name'], 'arguments': args})
    return result

def clean_message(message):
    result = {'role': message['role'], 'content': message.get('content')}
    if message.get('tool_calls'):
        result['tool_calls'] = native_calls(message)
    return result

def tool_result_error(text):
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return False
    def check(value):
        if isinstance(value, list):
            return any(check(x) for x in value)
        if not isinstance(value, dict):
            return False
        if value.get('error') or value.get('ok') is False or value.get('success') is False or str(value.get('status', '')).lower() in ('error', 'failed', 'failure'):
            return True
        return isinstance(value.get('results'), (dict, list)) and check(value['results'])
    return check(data)

def make_row(source, source_index, messages, tools, target_name=None, decision=None, calls=None, suffix='', note=None):
    # Input contains only messages BEFORE the decision. Never the gold decision.
    if not messages or not any(m['role'] == 'user' for m in messages):
        raise Rejected('missing_user_context')
    opts, tool_keys = {}, {}
    for i, tool in enumerate(tools):
        key = f'tool_{i:03d}'
        opts[key] = '도구 호출: ' + tool['name'] + ' — ' + tool['description']
        tool_keys[key] = tool['name']
    opts.update(ask=ASK, no_tool=NONE)
    target = decision if decision else next(k for k, name in tool_keys.items() if name == target_name)
    row = {'id': f'{source}:{source_index}{suffix}', 'source': source, 'source_index': source_index,
           'kind': 'tool_selection', 'question': QUESTION, 'context': stable({'tools': tools, 'messages': messages}),
           'input': next(m['content'] for m in reversed(messages) if m['role'] == 'user'),
           'options': opts, 'target': target, 'tool_keys': tool_keys, 'tools': tools,
           'messages': messages, 'reference_calls': calls or [],
           'label_status': 'assistant_reviewed_not_independent_human_gold' if note else 'synthetic_source_structural_checks_only',
           'review_note': note}
    row['group'] = digest([messages[0], tools, source, source_index])
    return row

def pref_call_text(content):
    if content.startswith('<TOOLCALL>') and content.endswith('</TOOLCALL>'):
        calls = json.loads(content[len('<TOOLCALL>'):-len('</TOOLCALL>')])
        return calls
    return None

def build_rows(review):
    rows, rejected = [], []
    def skip(source, index, reason, **other):
        rejected.append({'source': source, 'source_index': index, 'reason': reason, **other})
    data = json.loads((RAW / 'toolace.json').read_text(encoding='utf8'))
    for index, record in enumerate(data):
        if str(index) in review.get('toolace_excluded_indices', {}):
            skip('toolace', index, review['toolace_excluded_indices'][str(index)])
            continue
        try:
            tools = toolace_tools(record['system'])
            conv = record['conversations']
            prefix = []
            for turn, message in enumerate(conv):
                role, value = message['from'], message['value']
                if role not in ('user', 'assistant', 'tool'):
                    raise Rejected('unknown_message_role')
                if role == 'assistant':
                    if value.strip().startswith('['):
                        try:
                            calls = parse_toolace_calls(value, [t['name'] for t in tools])
                            validate_calls(calls, tools)
                            if turn + 1 < len(conv) and conv[turn + 1]['from'] == 'tool' and tool_result_error(conv[turn + 1]['value']):
                                raise Rejected('next_tool_result_reports_error')
                            r = make_row('toolace', index, list(prefix), tools, target_name=calls[0]['name'], calls=calls, suffix=f':turn{turn}',
                                         note=review.get('toolace_reviewed_indices', {}).get(str(index)) if turn == 1 else None)
                            rows.append(r)
                            prefix.append({'role': role, 'content': None, 'tool_calls': calls})
                            continue
                        except (Rejected, ValueError, TypeError, KeyError) as exc:
                            skip('toolace', index, str(exc), turn=turn)
                            # An unparsed call cannot become reliable past context.
                            break
                    if prefix and prefix[-1]['role'] == 'user':
                        skip('toolace', index, 'unlabelled_non_call_needs_review', turn=turn)
                prefix.append({'role': role, 'content': value})
        except (Rejected, ValueError, TypeError, KeyError) as exc:
            skip('toolace', index, str(exc))
    data = read_jsonl(RAW / 'when2call_sft.jsonl')
    for index, record in enumerate(data):
        label = review.get('when2call_sft', {}).get(str(index))
        if not label or label['decision'] == 'exclude':
            skip('when2call_sft', index, 'unlabelled_behavior' if not label else label['reason'])
            continue
        tools = tools_normalized(record['tools'])
        rows.append(make_row('when2call_sft', index, record['messages'][:-1], tools,
                             decision=label['decision'], note=label['reason']))
    # Keep the released chosen-vs-rejected supervision without inventing class labels.
    for index, record in enumerate(read_jsonl(RAW / 'when2call_pref.jsonl')):
        if str(index) in review.get('when2call_pref_excluded_indices', {}):
            skip('when2call_pref', index, review['when2call_pref_excluded_indices'][str(index)])
            continue
        try:
            tools = tools_normalized(record['tools'])
            chosen = record['chosen_response']['content']
            other = record['rejected_response']['content']
            if not chosen or chosen == other:
                raise Rejected('empty_or_equal_preference')
            calls = pref_call_text(chosen)
            if calls is not None:
                validate_calls(calls, tools)
            options = {}
            for key, text in [('response_a', chosen), ('response_b', other)]:
                call = pref_call_text(text)
                options[key] = '다음 응답: ' + (stable({'tool_calls': call}) if call is not None else text)
            rows.append({'id': f'when2call_pref:{index}', 'source': 'when2call_pref', 'source_index': index,
                         'kind': 'behavior_preference', 'question': PREF_QUESTION,
                         'context': stable({'tools': tools, 'messages': record['messages']}),
                         'messages': record['messages'], 'input': record['messages'][-1]['content'],
                         'tools': tools, 'options': options, 'target': 'response_a', 'tool_keys': {},
                         'reference_calls': calls or [], 'group': digest([record['messages'][0], tools]),
                         'label_status': 'synthetic_source_preference_not_generic_action_label', 'review_note': None})
        except (Rejected, ValueError, TypeError, KeyError) as exc:
            skip('when2call_pref', index, str(exc))
    for index, record in enumerate(read_jsonl(RAW / 'nemotron.jsonl')):
        if record.get('uuid') in review.get('nemotron_excluded_uuids', {}):
            skip('nemotron', index, review['nemotron_excluded_uuids'][record['uuid']])
            continue
        try:
            tools = tools_normalized(record['tools'])
            messages = record['messages']
            for turn, message in enumerate(messages):
                if message.get('role') != 'assistant' or not message.get('tool_calls'):
                    continue
                try:
                    calls = native_calls(message)
                    validate_calls(calls, tools)
                    if turn + 1 < len(messages) and messages[turn + 1]['role'] == 'tool':
                        call_id = message['tool_calls'][0].get('id')
                        result_id = messages[turn + 1].get('tool_call_id')
                        if call_id and result_id and call_id != result_id:
                            raise Rejected('tool_response_id_mismatch')
                    if turn + 1 < len(messages) and messages[turn + 1]['role'] == 'tool' and tool_result_error(messages[turn + 1].get('content')):
                        raise Rejected('next_tool_result_reports_error')
                    r = make_row('nemotron', index, [clean_message(m) for m in messages[:turn]], tools,
                                 target_name=calls[0]['name'], calls=calls, suffix=f':turn{turn}',
                                 note=review.get('nemotron_reviewed_uuids', {}).get(record.get('uuid')))
                    r['source_uuid'] = record.get('uuid')
                    rows.append(r)
                except (Rejected, ValueError, TypeError, KeyError) as exc:
                    skip('nemotron', index, str(exc), turn=turn)
        except (Rejected, ValueError, TypeError, KeyError) as exc:
            skip('nemotron', index, str(exc))
    return rows, rejected

class Families:
    def __init__(self):
        self.parent = {}
    def find(self, x):
        self.parent.setdefault(x, x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)
    def tokens(self, tool):
        return ['name:' + norm(tool['name']), 'definition:' + digest([norm(tool['description']), tool['parameters']])]
    def register(self, tool):
        a, b = self.tokens(tool)
        self.union(a, b)
    def family(self, tool):
        return self.find(self.tokens(tool)[0])

def write_jsonl(path, rows):
    with path.open('w', encoding='utf8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

def partition(rows, reserved_questions, overrides=None):
    families = Families()
    for row in rows:
        for tool in row['tools']:
            families.register(tool)
    forced = {}
    for name, split in (overrides or {}).items():
        family = families.find('name:' + norm(name))
        if family in forced and forced[family] != split:
            raise ValueError('Conflicting tool-family split overrides')
        forced[family] = split
    def fold(tool):
        if families.family(tool) in forced:
            return forced[families.family(tool)]
        bucket = int(digest('split-v1:' + families.family(tool))[:8], 16) % 100
        return 'test' if bucket < 7 else 'dev' if bucket < 14 else 'train'
    # All decisions from the same original conversation stay together.
    conversation_folds = collections.defaultdict(set)
    question_folds = collections.defaultdict(set)
    for row in rows:
        folds = {fold(t) for t in row['tools']} - {'train'}
        conversation_folds[(row['source'], row['source_index'])].update(folds)
        question_folds[norm(row['input'])].update(folds)
    identity_targets = collections.defaultdict(set)
    for row in rows:
        key = digest([row['kind'], row['context'], sorted(row['options'].values())])
        identity_targets[key].add(row['options'][row['target']])
    split_rows = {'train': [], 'dev': [], 'test': []}
    dropped, seen = [], set()
    for row in rows:
        folds = conversation_folds[(row['source'], row['source_index'])] | question_folds[norm(row['input'])]
        if norm(row['input']) in reserved_questions:
            dropped.append({'id': row['id'], 'reason': 'official_when2call_test_question_overlap'})
            continue
        if len(folds) > 1:
            dropped.append({'id': row['id'], 'reason': 'dev_test_tool_family_conflict'})
            continue
        split = next(iter(folds)) if folds else 'train'
        identity = digest([row['kind'], row['context'], sorted(row['options'].values())])
        if len(identity_targets[identity]) != 1:
            dropped.append({'id': row['id'], 'reason': 'conflicting_labels_for_same_input'})
            continue
        if identity in seen:
            dropped.append({'id': row['id'], 'reason': 'duplicate_model_input'})
            continue
        seen.add(identity)
        row['tool_families'] = [families.family(t) for t in row['tools']]
        # Prefix labels and chosen/rejected labels must not determine option position.
        items = list(row['options'].items())
        random.Random(SEED + int(digest(row['id'])[:8], 16)).shuffle(items)
        if row['kind'] == 'behavior_preference':
            original_target = row['target']
            row['options'] = {f'response_{i}': value for i, (_, value) in enumerate(items)}
            row['target'] = next(f'response_{i}' for i, (key, _) in enumerate(items) if key == original_target)
        else:
            row['options'] = dict(items)
        row['split'] = split
        row['heldout_gold_tool'] = bool(row['reference_calls']) and any(
            fold(t) == split and split != 'train' and t['name'] in {c['name'] for c in row['reference_calls']}
            for t in row['tools'])
        split_rows[split].append(row)
    return split_rows, dropped

def verify_splits(splits):
    train_tools = {f for r in splits['train'] for f in r['tool_families']}
    groups, questions = {}, {}
    for split, rows in splits.items():
        for row in rows:
            if row['target'] not in row['options'] or len(row['options']) < 2:
                raise AssertionError('invalid choice')
            for key, table in [((row['source'], row['source_index']), groups), (norm(row['input']), questions)]:
                if key in table and table[key] != split:
                    raise AssertionError('conversation/question crosses splits')
                table[key] = split
            if split != 'train' and row['heldout_gold_tool']:
                selected = {norm(c['name']) for c in row['reference_calls']}
                if any(f in train_tools for t, f in zip(row['tools'], row['tool_families']) if norm(t['name']) in selected):
                    raise AssertionError('heldout gold tool leaked into training')
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', type=Path, default=DEST)
    args = parser.parse_args()
    if args.dest.exists():
        raise FileExistsError('Frozen output exists; choose --dest with a new version')
    raw_manifest = json.loads((RAW / 'manifest.json').read_text(encoding='utf8'))
    for item in raw_manifest:
        if digest_bytes(RAW / item['path']) != item['sha256']:
            raise ValueError('Raw input changed: ' + item['path'])
    review = json.loads(REVIEW.read_text(encoding='utf8'))
    rows, rejected = build_rows(review)
    reserved_path = ROOT / 'output/tool-dataset-research-20261107/nvidia__When2Call/when2call_test_mcq.jsonl'
    reserved = {norm(r['question']) for r in read_jsonl(reserved_path)}
    splits, split_rejected = partition(rows, reserved, review.get('heldout_family_overrides'))
    verify_splits(splits)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(ROOT / 'models/ko-decision-roberta-large', local_files_only=True)
    tok.model_max_length = 1000000
    args.dest.mkdir(parents=True)
    summary = {}
    for split, items in splits.items():
        for start in range(0, len(items), 128):
            batch = items[start:start + 128]
            first, second, counts = [], [], []
            for row in batch:
                counts.append(len(row['options']))
                for value in row['options'].values():
                    first.append(row['question'] + ' ' + value)
                    second.append(row['context'])
            encoded = tok(first, second, padding=False, truncation=False)['input_ids'] if first else []
            cursor = 0
            for row, count in zip(batch, counts):
                row['max_input_tokens'] = max(len(x) for x in encoded[cursor:cursor + count])
                cursor += count
        random.Random(SEED).shuffle(items)
        write_jsonl(args.dest / (split + '_all_lengths.jsonl'), items)
        fits = {}
        for limit in [512, 1024, 2048, 4096]:
            limited = [r for r in items if r['max_input_tokens'] <= limit]
            fits[str(limit)] = len(limited)
            if limit == 512:
                # Default selection files must not silently mix a different task.
                write_jsonl(args.dest / (split + '.jsonl'), [r for r in limited if r['kind'] == 'tool_selection'])
                write_jsonl(args.dest / (split + '_all_tasks_512.jsonl'), limited)
                write_jsonl(args.dest / (split + '_tool_selection.jsonl'), [r for r in limited if r['kind'] == 'tool_selection'])
                write_jsonl(args.dest / (split + '_behavior_preference.jsonl'), [r for r in limited if r['kind'] == 'behavior_preference'])
                write_jsonl(args.dest / (split + '_reviewed_selection.jsonl'), [r for r in limited if r['label_status'].startswith('assistant_reviewed')])
        summary[split] = {'total': len(items), 'fits_without_truncation': fits,
                          'by_source': dict(collections.Counter(r['source'] for r in items)),
                          'by_kind': dict(collections.Counter(r['kind'] for r in items)),
                          'heldout_gold_call_rows': sum(r['heldout_gold_tool'] for r in items),
                          'selection_labels': dict(collections.Counter('call' if r['reference_calls'] else r['target'] for r in items if r['kind'] == 'tool_selection')),
                          'reviewed_selection_rows': sum(r['label_status'].startswith('assistant_reviewed') for r in items),
                          'target_positions': dict(collections.Counter(list(r['options']).index(r['target']) for r in items))}
        print(split, json.dumps(summary[split]), flush=True)
    write_jsonl(args.dest / 'rejected.jsonl', rejected + split_rejected)
    fields = ['split', 'id', 'kind', 'max_input_tokens', 'input', 'tools_json', 'context', 'options_json', 'target', 'reference_calls_json', 'label_status', 'review_note', 'human_verdict', 'human_notes']
    with (args.dest / 'review.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for split, items in splits.items():
            for source in ['toolace', 'when2call_sft', 'when2call_pref', 'nemotron']:
                selected = sorted([r for r in items if r['source'] == source and r['max_input_tokens'] <= 512], key=lambda r: digest(r['id']))[:10]
                for row in selected:
                    writer.writerow({k: row.get(k, '') for k in fields} | {'tools_json': stable(row['tools']), 'options_json': stable(row['options']), 'reference_calls_json': stable(row['reference_calls'])})
    manifest = {'version': args.dest.name, 'seed': SEED, 'raw_sources': raw_manifest,
                'summary': summary, 'rejections': dict(collections.Counter(r['reason'] for r in rejected + split_rejected)),
                'input_contract': 'tokenizer(question + space + option_description, context); no truncation',
                'default_length': 512, 'extra_length_files_are_not_context_extension_evidence': True,
                'splits': 'Whole source conversations and matching current utterances kept together. Tool families group normalized names/exact definitions. Held-out gold calls are marked separately; not all eval gold tools are unseen.',
                'split_checks_passed': True,
                'review_config_sha256': digest_bytes(REVIEW),
                'heldout_family_overrides': review.get('heldout_family_overrides'),
                'heldout_override_reason': review.get('heldout_override_reason'),
                'builder_sha256': digest_bytes(Path(__file__)),
                'warnings': ['English source text with Korean task questions; not Korean training data.',
                             'Synthetic source decisions, not independently human verified.',
                             'Behavior preference is a separate task, not a recovered ask/no_tool label.',
                             'Tool-family split is not a semantic-domain split or a guarantee against prior model training overlap.',
                             'No model training or execution success was measured.']}
    manifest['files'] = {p.name: digest_bytes(p) for p in args.dest.iterdir() if p.is_file()}
    (args.dest / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
    print('Saved', args.dest, flush=True)

def digest_bytes(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

if __name__ == '__main__':
    main()
