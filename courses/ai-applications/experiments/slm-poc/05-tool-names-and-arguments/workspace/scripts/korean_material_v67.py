"""Source-preserving native xLAM material audit. No model inference/training."""
import ast
import collections
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'output/korean-native-v67'
if '--material-v2' in sys.argv: OUT = OUT / 'material-v2'
SEED = 670067
MODEL = 'Salesforce/xLAM-2-1b-fc-r'
REV = '6870fcf102f434bd01819302d85780b8e767925d'
SOURCES = {
    'glaive_ko': ROOT / 'data/raw/glaive-function-calling-v2-ko/train.json',
    'kotraj': ROOT / 'data/raw/kotraj-v02/train-00000-of-00001.parquet',
    'kofunction': ROOT / 'data/raw/kofunctioncall/train-00000-of-00005.parquet',
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''): h.update(b)
    return h.hexdigest()


def stable(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f: json.dump(value, f, ensure_ascii=False, indent=2)


def object_text(text):
    """Parse JSON or a literal container; never execute source expressions."""
    if not isinstance(text, str): return copy.deepcopy(text)
    try: return json.loads(text)
    except (ValueError, TypeError): return ast.literal_eval(text)


def declarations(text):
    """The source serializes adjacent complete JSON declarations, not a list."""
    if isinstance(text, list): return copy.deepcopy(text)
    decoder = json.JSONDecoder(); pos = 0; output = []
    while pos < len(text):
        if text[pos].isspace(): pos += 1; continue
        item, end = decoder.raw_decode(text, pos); pos = end
        output.extend(item if isinstance(item, list) else [item])
    return output


def norm_call(call):
    f = copy.deepcopy(call.get('function', call))
    args = object_text(f.get('arguments', {}))
    if not isinstance(f.get('name'), str) or not isinstance(args, dict): raise ValueError('invalid_call')
    result = {'type': 'function', 'function': {'name': f['name'], 'arguments': args}}
    if 'id' in call: result['id'] = call['id']
    return result


def glaive(row):
    tools = declarations(row['function_description'])
    ms = [{'role': 'system', 'content': row.get('system_message') or ''}]; pending = None
    for i, m in enumerate(row['conversations_ko']):
        role = m['role']; content = m.get('content')
        if role == 'function-call':
            if pending is not None: raise ValueError('unanswered_call')
            call = norm_call(object_text(content)); call['id'] = 'src_' + str(i)
            # Glaive represents a single assistant turn as a prose prefix and
            # then function-call. The prefix is NOT a no-call/stop example.
            if ms[-1]['role'] == 'assistant' and not ms[-1].get('tool_calls'):
                ms[-1]['tool_calls'] = [call]
            else:
                ms.append({'role': 'assistant', 'content': None, 'tool_calls': [call]})
            pending = call
        elif role == 'function-response':
            if pending is None: raise ValueError('orphan_result')
            ms.append({'role': 'tool', 'name': pending['function']['name'], 'tool_call_id': pending['id'], 'content': content})
            pending = None
        elif role in ['user', 'assistant']:
            if pending is not None: raise ValueError('result_missing')
            if role == 'assistant' and ms[-1]['role'] == 'assistant' and not ms[-1].get('tool_calls'):
                ms[-1]['content'] = (ms[-1].get('content') or '') + '\n' + (content or '')
            else:
                ms.append({'role': role, 'content': content})
        else: raise ValueError('unknown_role')
    if pending: raise ValueError('result_missing')
    group = 'glaive:' + stable(row['conversations'])
    return ms, tools, group


def kotraj(row):
    if row['verify_status'] != 'verified': raise ValueError('source_not_verified')
    ms = json.loads(row['messages']); tools = [t.get('function', t) for t in json.loads(row['tools'])]
    for m in ms:
        if m.get('tool_calls'): m['tool_calls'] = [norm_call(c) for c in m['tool_calls']]
    return ms, tools, 'kotraj:' + str(row.get('pair_id') or row['id'])


def kofunction(row):
    tools = json.loads(row['functions']); call = norm_call(json.loads(row['function_call']))
    ms = [{'role': 'user', 'content': '참고 자료:\n' + row['context'] + '\n\n사용자 요청:\n' + row['question']},
          {'role': 'assistant', 'content': None, 'tool_calls': [call]}]
    return ms, tools, 'kofunction:' + stable(row['context'])


def validate_conversation(ms, tools):
    from jsonschema import Draft202012Validator
    by_name = {t['name']: t for t in tools}
    if not tools or len(by_name) != len(tools): raise ValueError('empty_or_duplicate_catalog')
    for t in tools:
        Draft202012Validator.check_schema(t.get('parameters', {'type':'object'}))
    pending = {}
    for m in ms:
        if m['role'] == 'assistant':
            for call in m.get('tool_calls') or []:
                f = call['function']
                if f['name'] not in by_name: raise ValueError('unregistered_source_call')
                Draft202012Validator(by_name[f['name']].get('parameters', {})).validate(f['arguments'])
                pending[call.get('id') or f['name']] = f['name']
        elif m['role'] == 'tool':
            key = m.get('tool_call_id')
            if key and key not in pending: raise ValueError('orphan_tool_id')
            if key: m['name'] = pending.pop(key)
            elif len(pending) == 1: m['name'] = pending.pop(next(iter(pending)))
            else: raise ValueError('ambiguous_tool_result')


def records():
    import pyarrow.parquet as pq
    with SOURCES['glaive_ko'].open(encoding='utf-8') as f:
        for index, line in enumerate(f): yield 'glaive_ko', index, json.loads(line), glaive
    for batch in pq.ParquetFile(SOURCES['kotraj']).iter_batches(batch_size=512):
        for row in batch.to_pylist(): yield 'kotraj', row['id'], row, kotraj
    pf = pq.ParquetFile(SOURCES['kofunction'])
    picked = set(random.Random(SEED).sample(range(pf.metadata.num_rows), min(6000, pf.metadata.num_rows)))
    index = 0
    for batch in pf.iter_batches(batch_size=1024):
        for row in batch.to_pylist():
            if index in picked: yield 'kofunction', index, row, kofunction
            index += 1


def normalize_history(messages, default_system):
    output = []; policies = [m.get('content') or '' for m in messages if m['role'] == 'system']
    policy = '\n\n'.join(p for p in policies if p.strip())
    output.append({'role': 'system', 'content': default_system + ('\n\nSource instructions:\n' + policy if policy else '')})
    for source in messages:
        if source['role'] == 'system': continue
        m = {k: copy.deepcopy(v) for k,v in source.items() if k in ['role','content','name','tool_calls','tool_call_id']}
        if m.get('tool_calls') and (m.get('content') or '').strip():
            output.append({'role': 'assistant','content':m['content']}); m['content'] = None
        output.append(m)
    return output


def main():
    OUT.mkdir(exist_ok=False)
    from transformers import AutoTokenizer
    from scripts.retail_data_v65 import encode_example
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV, local_files_only=True)
    rendered = tok.apply_chat_template([{'role':'user','content':'probe'}],tools=[],tokenize=False)
    default = rendered.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()
    counts = collections.defaultdict(collections.Counter); tool_frequency = collections.Counter(); reviews = collections.defaultdict(list)
    corpus_path = OUT / 'candidate-pool.jsonl'; decisions = 0
    with corpus_path.open('x', encoding='utf-8') as corpus:
        for source, index, raw, converter in records():
            c = counts[source]; c['rows_checked'] += 1
            try:
                ms, tools, group = converter(raw)
                validate_conversation(ms, tools)
                if any(len(m.get('tool_calls') or []) > 1 for m in ms):
                    c['parallel_conversation_excluded'] += 1; continue
                text = ' '.join(str(m.get('content') or '') for m in ms if m['role']=='user')
                if not any('\uac00' <= ch <= '\ud7a3' for ch in text): raise ValueError('no_korean_user')
            except Exception as e:
                c['bad_conversation'] += 1; c['bad:' + type(e).__name__ + ':' + str(e).splitlines()[0][:90]] += 1; continue
            c['conversations_format_valid'] += 1
            # Fixed source-only tool order shuffle: target position carries no label.
            tools = copy.deepcopy(tools); random.Random(SEED ^ int(stable([source,str(index)])[:12],16)).shuffle(tools)
            for name in {t['name'] for t in tools}: tool_frequency[name] += 1
            for j,m in enumerate(ms):
                if m['role'] != 'assistant' or j == 0: continue
                calls = m.get('tool_calls') or []
                if not calls and not (m.get('content') or '').strip(): continue
                previous = ms[j-1]['role']
                if previous not in ['user','tool']: continue
                bucket = 'call' if calls else 'post_tool' if previous=='tool' else 'user_text'
                target = {k:copy.deepcopy(v) for k,v in m.items() if k in ['role','content','tool_calls']}
                if calls: target['content'] = None
                history = normalize_history(ms[:j], default)
                c['candidate:' + bucket] += 1
                try: ids,start = encode_example(tok,history,target,tools)
                except Exception as e: c['encode:' + type(e).__name__] += 1; continue
                if len(ids)>4096: c['over4096:' + bucket] += 1; continue
                if len(ids)-start>256: c['target_over256:' + bucket] += 1; continue
                item = {'id':f'{source}:{index}:{j}','source':source,'source_index':str(index),'message_index':j,
                        'group':group,'bucket':bucket,'messages':history,'tools':tools,'target':target,
                        'tokens':len(ids),'target_start':start,'input_ids':ids}
                corpus.write(json.dumps(item,ensure_ascii=False)+'\n'); decisions += 1; c['eligible:' + bucket] += 1
                key=source+':'+bucket
                if len(reviews[key])<10: reviews[key].append({k:v for k,v in item.items() if k!='input_ids'})
            if c['rows_checked']%1000==0: print('V67 audit',source,c['rows_checked'],'decisions',decisions,flush=True)
    summary = {'seed':SEED,'max_tokens':4096,'max_target_tokens':256,'decisions':decisions,
               'counts':{k:dict(v) for k,v in counts.items()},'tool_frequency':dict(tool_frequency),
               'sources':{k:{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for k,p in SOURCES.items()},
               'scope':'Source call schemas and roles validated; not an independent semantic or backend execution verification. Ko-functioncall uses6000 sampled rows from local shard0 only. No truncation, no argument repair, no invented function definitions or labels.',
               'normalization':'Source system instructions preserved after native format instruction. Historical mixed assistant prose/calls split; current prefatory prose omitted, never input as hint. Tool definitions shuffled independently of target.'}
    write(OUT/'audit.json',summary); write(OUT/'review-samples.json',dict(reviews))
    print(json.dumps({k:dict(v) for k,v in counts.items()},ensure_ascii=True),flush=True)


if __name__=='__main__': main()
