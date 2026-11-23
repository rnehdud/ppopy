"""Prepare matched continuation pools without reading the held-out test file."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.retail_data_v65 import encode_example
from scripts.korean_material_v67 import MODEL, REV

DATA = ROOT/'data/processed/kotraj-reproduction-v76'
REVIEW = ROOT/'output/kotraj-v76-kaggle-result-review-20261112'
SEED = 760076


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            h.update(b)
    return h.hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def jsonl(path):
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def main(out):
    from transformers import AutoTokenizer
    import copy
    import numpy as np
    assert not out.exists(), 'Existing prepared data is protected'
    out.mkdir(parents=True)
    frozen = read(DATA/'plan.json')
    # Verify only the files being used; do not open or hash test.jsonl.
    for name in ['train.jsonl', 'val.jsonl', 'val-monitor-ids.json']:
        key = next(k for k in frozen['files'] if Path(k.replace('\\', '/')).name == name)
        assert sha(DATA/name) == frozen['files'][key]
    original_train = jsonl(DATA/'train.jsonl')
    val = jsonl(DATA/'val.jsonl')
    assert not {r['group'] for r in original_train} & {r['group'] for r in val}
    calls = [r for r in original_train if r['kind'] == 'call']
    stops = [r for r in original_train if r['kind'] == 'no_call']
    rng = random.Random(SEED); rng.shuffle(calls); rng.shuffle(stops)
    prior_order = [r for i in range(min(len(calls)//2, len(stops))) for r in (calls[2*i], calls[2*i+1], stops[i])]
    checkpoint = next(c for c in read(REVIEW/'checkpoint-index.json') if c['count'] == 8000)
    consumed = {r['id'] for r in prior_order[:checkpoint['cursor']+1]}
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV, local_files_only=True, trust_remote_code=False)
    default = tok.apply_chat_template([{'role': 'user', 'content': 'probe'}], tools=[], tokenize=False).split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()

    def history(source):
        source = copy.deepcopy(source)
        policies = [m.get('content') or '' for m in source if m['role'] == 'system']
        return [{'role':'system','content': default+'\n\nSource instructions:\n'+'\n\n'.join(policies)}] + [m for m in source if m['role'] != 'system']

    pool = []
    rejected = []
    for kind, candidates, quota in [('call', calls, 2000), ('no_call', stops, 1500)]:
        accepted = 0
        for row in candidates:
            if row['id'] in consumed:
                continue
            messages = history(row['messages'])
            ids, start = encode_example(tok, messages, row['target'], row['tools'])
            # SAME eligibility based on original target for all three arms.
            if len(ids)>8192 or len(ids)-start>1024:
                rejected.append({'id':row['id'], 'tokens':len(ids), 'target_tokens':len(ids)-start})
                continue
            encoded = {'id': row['id'], 'group': row['group'], 'kind': kind, 'input_ids': ids, 'start': start}
            if kind == 'no_call':
                short, short_start = encode_example(tok, messages, {'role':'assistant', 'content':'[]'}, row['tools'])
                assert short_start == start and short[:start] == ids[:start]
                encoded['short_ids'] = short
            pool.append(encoded)
            accepted += 1
            if accepted%250 == 0:
                print('Prepared', kind, accepted, '/', quota, flush=True)
            if accepted == quota:
                break
        assert accepted == quota
    assert len({r['id'] for r in pool}) == 3500
    assert not consumed & {r['id'] for r in pool}
    (out/'data').mkdir()
    with (out/'data/train-pool.jsonl').open('x', encoding='utf-8') as f:
        for row in pool:
            f.write(json.dumps(row, separators=(',', ':'))+'\n')
    for name in ['val.jsonl', 'val-monitor-ids.json']:
        shutil.copyfile(DATA/name, out/'data'/name)
    write(out/'data/pool-audit.json', {'quota':dict(collections.Counter(r['kind'] for r in pool)),
            'rejected':rejected, 'prior_8000_cursor':checkpoint['cursor'],
            'prior_consumed_ids_excluded':len(consumed), 'test_file_opened':False,
            'same_eligibility_all_arms':True, 'train_val_groups_disjoint':True})
    (out/'start').mkdir()
    for name in ['adapter_model.safetensors', 'adapter_config.json']:
        path = REVIEW/'evidence/checkpoint-8000'/name
        assert sha(path) == checkpoint['files'][name]
        shutil.copyfile(path, out/'start'/name)
    write(out/'start/weights.json', {'sha256':checkpoint['files']['adapter_model.safetensors'],
            'source':'User supplied kotraj-v76-results.zip, saved8000, not interrupted8151 in-memory weights'})
    (out/'reference').mkdir()
    shutil.copyfile(REVIEW/'original/examples-3000-val-monitor/summary.json', out/'reference/examples-3000-summary.json')
    shutil.copyfile(REVIEW/'original/examples-3000-val-monitor/predictions.jsonl', out/'reference/examples-3000-predictions.jsonl')
    audit_inputs = read(REVIEW/'all-model-inputs-and-gold.json')
    # Stored audit hashes come from the original Kaggle run, not newly generated hashes.
    records = jsonl(REVIEW/'original/examples-3000-val-monitor/predictions.jsonl')
    hashes = {r['id']:r['generation']['input_ids_sha256'] for r in records}
    by = {r['id']:r for r in val}
    for key, expected in hashes.items():
        row = by[key]
        b = tok.apply_chat_template(history(row['messages']), tools=row['tools'], add_generation_prompt=True, return_dict=True, return_tensors='np')
        assert hashlib.sha256(np.asarray(b['input_ids'],dtype=np.int64).tobytes()).hexdigest() == expected
    write(out/'preparation.json', {'model':MODEL,'revision':REV,'additional_examples':3000,
            'monitor_input_hashes':hashes,'source_data_hashes':{name:sha(DATA/name) for name in ['train.jsonl','val.jsonl','val-monitor-ids.json']},
            'optimizer_reset_common_to_all_arms':True,'learning_rate':1e-5,'initial_grad_scale':1024,
            'grad_scaler_skipped_updates_are_logged':True,
            'selection':'Better total val240 without call/no-call regression against8000; strongest eligible gets fullval. No test included.',
            'arms':{'control':'2 call:1 no-call, original target',
                    'ratio_1_to_1':'1 call:1 no-call, original target',
                    'short_no_call':'same exact examples/order as control, only no-call target replaced with []'},
            'test_read':False})
    print('Prepared v79 inputs, test untouched:',out,flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--out',type=Path,required=True)
    main(p.parse_args().out)
