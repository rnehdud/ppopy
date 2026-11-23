"""Freeze native-format source examples without truncation or new gold labels."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/diagnostics/retail-native-v65'
SRC = ROOT / 'output/intent-learning-search-v64/Ziyiii0-0__Retail-3I/train/trajectories'
REPO = 'Salesforce/xLAM-2-1b-fc-r'
REV = '6870fcf102f434bd01819302d85780b8e767925d'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, value):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def native_system(tokenizer, original):
    # Copy the official default format instruction, not a hand-authored format.
    rendered = tokenizer.apply_chat_template([{'role': 'user', 'content': 'probe'}], tools=[], tokenize=False)
    default = rendered.split('<|im_start|>system\n', 1)[1].split('<|im_end|>', 1)[0].strip()
    policy = re.search(r'<policy>(.*?)</policy>', original, re.S)
    if not policy:
        raise ValueError('Source policy not found')
    return default + '\n\nDomain policy (unchanged from source):\n' + policy[1].strip()


def normalize_message(message):
    m = {k: copy.deepcopy(v) for k, v in message.items() if k in ['role', 'content', 'tool_calls', 'name']}
    for call in m.get('tool_calls') or []:
        f = call['function']
        if isinstance(f['arguments'], str):
            f['arguments'] = json.loads(f['arguments'])
    return m


def history_messages(messages, tokenizer):
    output = []
    for m in messages:
        m = normalize_message(m)
        if m['role'] == 'system':
            m['content'] = native_system(tokenizer, m['content'])
        if m.get('tool_calls') and (m.get('content') or '').strip():
            # The official template otherwise silently discards this historical
            # prose. Preserve BOTH observed outputs, in original relative order.
            output.append({'role': 'assistant', 'content': m['content']})
            m['content'] = None
        output.append(m)
    return output


def encode_example(tokenizer, messages, target, tools):
    prompt = tokenizer.apply_chat_template(messages, tools=tools, tokenize=False, add_generation_prompt=True)
    full = tokenizer.apply_chat_template(messages + [target], tools=tools, tokenize=False, add_generation_prompt=False)
    if not full.startswith(prompt):
        raise ValueError('Native template prefix mismatch')
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    full_ids = tokenizer.encode(full, add_special_tokens=False)
    if full_ids[:len(prompt_ids)] != prompt_ids:
        raise ValueError('Token boundary mismatch')
    return full_ids, len(prompt_ids)


def main():
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
    replay = json.loads((OUT / 'source-replay.json').read_text(encoding='utf-8'))
    expanded = '--expanded' in sys.argv
    if expanded:
        replay['results'] += json.loads((OUT / 'source-replay-batch2.json').read_text(encoding='utf-8'))['results']
    raw = {k: [json.loads(x) for x in (SRC / (k + '.jsonl')).read_text(encoding='utf-8').splitlines()]
           for k in ['changing', 'infeasible']}
    candidates = []; skips = collections.Counter()
    for info in replay['results']:
        row = raw[info['kind']][info['source_index']]
        if not info['all_replayed_calls_match'] or not info['group']:
            skips['unverified_or_no_group'] += 1; continue
        # Source policy says one call at a time. Do not teach violating batches
        # or use later prefixes from those conversations in this first pilot.
        if any(len(m.get('tool_calls') or []) > 1 for m in row['messages']):
            skips['source_conversation_has_parallel_batch'] += 1; continue
        group = info['group']
        split = 'dev' if int(hashlib.sha256(('v65:' + group).encode()).hexdigest()[:8], 16) % 5 == 0 else 'train'
        tools = [copy.deepcopy(t['function']) for t in row['tools']]
        for j in info['prefix_verified_assistant_indices']:
            m = row['messages'][j]
            if j <= 1:
                continue
            target = normalize_message(m)
            if target.get('tool_calls'):
                # Decision-only supervision retains full native call+arguments.
                # Current-turn prefatory prose is NOT added as an input hint.
                target['content'] = None
                name = target['tool_calls'][0]['function']['name']
                bucket = 'write' if name.startswith(('modify_', 'cancel_', 'return_', 'exchange_')) else 'read'
            else:
                bucket = 'text'
            messages = history_messages(row['messages'][:j], tok)
            ids, start = encode_example(tok, messages, target, tools)
            if len(ids) > 8192 or len(ids) - start > 192:
                skips['overlength_no_truncation'] += 1; continue
            candidates.append({'id': f"{info['kind']}:{info['source_index']}:{j}", 'source_kind': info['kind'],
                 'source_index': info['source_index'], 'message_index': j, 'group': group, 'split': split,
                 'bucket': bucket, 'messages': messages, 'tools': tools, 'target': target,
                 'input_ids': ids, 'target_start': start})
    # Fixed budget, balanced tool/text, with writes represented separately.
    selected = []; rng = random.Random(650065)
    quotas = {'train': {'write': 24, 'read': 56, 'text': 80}, 'dev': {'write': 4, 'read': 8, 'text': 12}}
    counts = {}
    for split, buckets in quotas.items():
        for bucket, quota in buckets.items():
            rows = [r for r in candidates if r['split'] == split and r['bucket'] == bucket]
            rng.shuffle(rows); per_conversation = collections.Counter(); picked = []
            for r in rows:
                key = (r['source_kind'], r['source_index'])
                if per_conversation[key] >= 4:
                    continue
                picked.append(r); per_conversation[key] += 1
                if len(picked) == quota:
                    break
            counts[split + ':' + bucket] = {'available': len(rows), 'selected': len(picked), 'requested': quota}
            selected.extend(picked)
    train = [r for r in selected if r['split'] == 'train']; dev = [r for r in selected if r['split'] == 'dev']
    save('data-readiness-expanded.json' if expanded else 'data-readiness.json', {'counts': counts, 'skips': dict(skips), 'max_length': max((len(r['input_ids']) for r in selected), default=0),
          'training_groups': sorted({r['group'] for r in train}), 'dev_groups': sorted({r['group'] for r in dev}),
          'normalization': 'Official xLAM format + source policy unchanged; schemas unwrapped; arguments parsed, not repaired. '
                          'Teacher reasoning omitted. Historical mixed prose/calls split into two Assistant messages; '
                          'current prefatory prose omitted from call target and never supplied as a hint. No truncation.'})
    assert not ({r['group'] for r in train} & {r['group'] for r in dev})
    if any(c['selected'] != c['requested'] for c in counts.values()):
        raise ValueError('Predeclared small-data quotas not met; inspect readiness, do not silently rebalance')
    rng.shuffle(train); rng.shuffle(dev)
    save('train.json', train); save('dev.json', dev)
    print('V65 DATA READY', len(train), len(dev), counts, flush=True)


if __name__ == '__main__':
    main()
