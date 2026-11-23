"""Frozen v79 ablations: saved 8000 weights, ratio-only, target-only, no test access."""
import argparse
import collections
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from shared import Native, MODEL, REV, SEED, sha, atomic_json, valid_journal
from training.kotraj_reproduction_v76 import grade, summarize, passes
from training.retail_native_v65 import assistant_loss

ARMS = ('control', 'ratio_1_to_1', 'short_no_call')


class BudgetReached(Exception):
    pass


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def rows(path):
    with Path(path).open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def verify(root):
    manifest = read(root/'manifest.json')
    for name, expected in manifest['files'].items():
        assert 'test.jsonl' not in name, 'Test data forbidden in this experiment'
        assert sha(root/name) == expected, name
    assert manifest['model'] == MODEL and manifest['revision'] == REV
    assert manifest['additional_examples'] == 3000
    return manifest


def make_order(pool, arm):
    assert arm in ARMS
    calls = [r for r in pool if r['kind'] == 'call']
    stops = [r for r in pool if r['kind'] == 'no_call']
    assert len(calls) == 2000 and len(stops) == 1500
    if arm == 'ratio_1_to_1':
        return [r for pair in zip(calls[:1500], stops[:1500]) for r in pair]
    return [r for i in range(1000) for r in (calls[2*i], calls[2*i+1], stops[i])]


def sequence(row, arm):
    if arm == 'short_no_call' and row['kind'] == 'no_call':
        return row['short_ids'], row['start']
    return row['input_ids'], row['start']


def diagnostic(expected, result):
    g = result['grade']
    if g['correct']:
        return 'correct'
    if not result['generation']['finished']:
        return 'unfinished_message'
    if g['error']:
        return 'parse_error'
    if not expected:
        return 'extra_call'
    if not g['predicted']:
        return 'missing_call'
    names = lambda c: collections.Counter(x['name'] for x in c)
    return 'arguments_differ' if names(expected) == names(g['predicted']) else 'names_or_count_differ'


def improved(candidate, baseline):
    # Never reward simply replacing required calls with no-call.
    return (candidate['all']['correct'] > baseline['all']['correct']
            and candidate['call']['correct'] >= baseline['call']['correct']
            and candidate['no_call']['correct'] >= baseline['no_call']['correct'])


def choose(results):
    baseline = results['saved_8000']
    eligible = ['saved_8000']
    for arm in ARMS:
        if improved(results[arm], baseline):
            eligible.append(arm)
    return max(eligible, key=lambda label: (results[label]['all']['correct'],
                    results[label]['call']['correct'], label == 'saved_8000'))


class Experiment:
    def __init__(self, root, out, deadline, native_factory=Native):
        self.root, self.out, self.deadline = root, out, deadline
        self.manifest = verify(root)
        self.out.mkdir(parents=True, exist_ok=True)
        identity = {'input_manifest_sha256': sha(root/'manifest.json'),
                    'additional_examples': 3000, 'test_read': False}
        if (out/'identity.json').exists():
            assert read(out/'identity.json') == identity, 'Different experiment in output directory'
        else:
            atomic_json(out/'identity.json', identity)
        self.native_factory = native_factory
        self.native = None
        self.torch = None
        self.model_label = None
        self.val = rows(root/'data/val.jsonl')
        by_id = {r['id']: r for r in self.val}
        ids = read(root/'data/val-monitor-ids.json')
        self.monitor = [by_id[i] for i in ids]
        assert len(self.monitor) == 240

    def budget(self):
        if time.time() >= self.deadline or (self.out.parent/'STOP').exists():
            raise BudgetReached('Time budget reached; saved progress can resume')

    def load(self, directory, label):
        import torch
        from safetensors.torch import load_file
        from peft import set_peft_model_state_dict
        self.torch = torch
        if self.native is None:
            assert torch.cuda.is_available()
            assert torch.cuda.mem_get_info()[0] > 4*2**30, 'GPU busy; no training process is stopped'
            random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
            self.native = self.native_factory()
            atomic_json(self.out/'environment.json', self.native.environment)
        expected = read(directory/'weights.json')
        assert expected['sha256'] == sha(directory/'adapter_model.safetensors')
        state = load_file(str(directory/'adapter_model.safetensors'))
        actual = set_peft_model_state_dict(self.native.model, state)
        assert not actual.unexpected_keys
        assert not [k for k in actual.missing_keys if 'lora_' in k], 'Missing adapter tensors'
        self.model_label = label
        self.native.model.eval()

    def evaluate(self, label, full=False):
        self.budget()
        directory = self.out/(label+('-full-val' if full else '-val240'))
        directory.mkdir(parents=True, exist_ok=True)
        data = self.val if full else self.monitor
        weights = self.weights(label)
        identity = {'weights_sha256': sha(weights/'adapter_model.safetensors'),
                    'input_manifest_sha256': sha(self.root/'manifest.json'),
                    'full_val': full, 'test_read': False, 'max_new_tokens': 1024}
        if (directory/'identity.json').exists():
            assert read(directory/'identity.json') == identity
        else:
            atomic_json(directory/'identity.json', identity)
        saved = valid_journal(directory/'predictions.jsonl')
        assert len(saved) <= len(data)
        for record, row in zip(saved, data):
            assert record['id'] == row['id']
            assert record['grade'] == grade(row['expected_calls'], record['generation'])
        if len(saved) != len(data):
            if self.model_label != label:
                self.load(weights, label)
            self.native.model.eval()
            with (directory/'predictions.jsonl').open('a', encoding='utf-8') as f:
                for row in data[len(saved):]:
                    self.budget()
                    g = self.native.generate_row(row)
                    if row['id'] in self.manifest['monitor_input_hashes']:
                        assert g['input_ids_sha256'] == self.manifest['monitor_input_hashes'][row['id']]
                    record = {'id': row['id'], 'generation': g, 'grade': grade(row['expected_calls'], g)}
                    f.write(json.dumps(record, ensure_ascii=False)+'\n'); f.flush()
                    saved.append(record)
                    if len(saved)%10 == 0:
                        print(label, len(saved), '/', len(data), json.dumps(summarize(saved)), flush=True)
        summary = summarize(saved)
        summary['categories'] = dict(collections.Counter(diagnostic(row['expected_calls'], r) for row, r in zip(data, saved)))
        summary.update(full_val=full, test_read=False, score='Exact reference next-call batch, not API task completion')
        atomic_json(directory/'summary.json', summary)
        return summary

    def train(self, arm):
        directory = self.out/arm
        directory.mkdir(parents=True, exist_ok=True)
        if (directory/'trained.json').exists():
            return
        self.budget()
        pool = rows(self.root/'data/train-pool.jsonl')
        order = make_order(pool, arm)
        atomic_json(directory/'order.json', [r['id'] for r in order])
        state_path = directory/'state.json'
        state = read(state_path) if state_path.exists() else {'count': 0, 'updates': 0, 'overflow_updates': 0}
        checkpoint = directory/state['checkpoint'] if state['count'] else self.root/'start'
        self.load(checkpoint if state['count'] else self.root/'start', arm)
        torch = self.torch
        model = self.native.model
        parameters = [p for p in model.parameters() if p.requires_grad]
        # Reset equally for ALL arms. This is a controlled continuation, not exact v76 resume.
        optimizer = torch.optim.AdamW(parameters, lr=1e-5, weight_decay=0)
        scaler = torch.amp.GradScaler('cuda', init_scale=1024)
        if state['count']:
            prior = torch.load(checkpoint/'training-state.pt', map_location='cpu', weights_only=True)
            optimizer.load_state_dict(prior['optimizer']); scaler.load_state_dict(prior['scaler'])
            random.setstate(prior['python_rng']); torch.random.set_rng_state(prior['torch_rng'])
            torch.cuda.set_rng_state_all(prior['cuda_rng'])
        else:
            random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
        model.enable_input_require_grads()
        optimizer.zero_grad(set_to_none=True)

        def save():
            # Alternate immutable checkpoint directories; state is committed last.
            assert state['count']%4 == 0
            dest = directory/('saved-'+str(state['count']))
            dest.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(dest, safe_serialization=True)
            torch.save({'optimizer': optimizer.state_dict(), 'scaler': scaler.state_dict(),
                        'python_rng': random.getstate(), 'torch_rng': torch.random.get_rng_state(),
                        'cuda_rng': torch.cuda.get_rng_state_all()}, dest/'training-state.pt')
            atomic_json(dest/'weights.json', {'sha256': sha(dest/'adapter_model.safetensors')})
            # Small pointer, not directory renames/deletion; preserve all saved weights.
            atomic_json(directory/'state.json', {**state, 'checkpoint': dest.name})
            return dest

        # Previous checkpoint has an explicit directory name rather than a mutable symlink.
        segment = str(time.time_ns())
        resume_count = state['count']
        with (directory/'training-log.jsonl').open('a', encoding='utf-8') as log:
            for row in order[state['count']:]:
                if state['count']%4 == 0 and (time.time() >= self.deadline or (self.out.parent/'STOP').exists()):
                    save(); raise BudgetReached('Training saved at optimizer boundary')
                ids, start = sequence(row, arm)
                assert len(ids) <= 8192 and len(ids)-start <= 1024
                model.train()
                b = torch.tensor([ids], device='cuda')
                with torch.autocast('cuda', dtype=torch.float16):
                    loss = assistant_loss(model, b, start)
                assert bool(torch.isfinite(loss)), 'Non-finite loss; preserve diagnostics'
                scaler.scale(loss/4).backward()
                state['count'] += 1
                update = None
                if state['count']%4 == 0:
                    scaler.unscale_(optimizer)
                    norm = torch.nn.utils.clip_grad_norm_(parameters, 1.0)
                    finite = bool(torch.isfinite(norm))
                    scale_before = scaler.get_scale()
                    scaler.step(optimizer); scaler.update(); optimizer.zero_grad(set_to_none=True)
                    if finite:
                        state['updates'] += 1
                    else:
                        state['overflow_updates'] += 1
                    update = {'finite_norm': finite, 'scale_before': scale_before, 'scale_after': scaler.get_scale()}
                record = {**state, 'segment': segment, 'resume_count': resume_count,
                          'id': row['id'], 'kind': row['kind'], 'loss': float(loss.detach()),
                          'tokens': len(ids), 'target_tokens': len(ids)-start, 'update': update}
                log.write(json.dumps(record)+'\n'); log.flush()
                del b, loss
                if state['count']%20 == 0:
                    print(arm, state['count'], '/ 3000', flush=True)
                if state['count']%200 == 0:
                    save(); torch.cuda.empty_cache()
        dest = save()
        atomic_json(directory/'trained.json', {**state, 'checkpoint': dest.name,
                    'optimizer_reset_common_to_all_arms': True})
        del optimizer, scaler, parameters
        model.eval(); torch.cuda.empty_cache()

    def weights(self, label):
        if label == 'saved_8000':
            return self.root/'start'
        state = read(self.out/label/'state.json')
        return self.out/label/state['checkpoint']

    def run(self, evaluate_only=False):
        results = {'saved_8000': self.evaluate('saved_8000')}
        before = read(self.root/'reference/examples-3000-summary.json')
        old = rows(self.root/'reference/examples-3000-predictions.jsonl')
        new = rows(self.out/'saved_8000-val240/predictions.jsonl')
        paired = collections.Counter()
        with (self.out/'8000-versus-3000-all240.csv').open('w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=['id','expected_calls','before_correct','after_correct',
                    'before_output','after_output','difference_category'])
            writer.writeheader()
            for source,a,b in zip(self.monitor,old,new):
                assert source['id']==a['id']==b['id']
                assert a['generation']['input_ids_sha256']==b['generation']['input_ids_sha256']
                paired[str(int(a['grade']['correct']))+'->'+str(int(b['grade']['correct']))]+=1
                writer.writerow({'id':source['id'],'expected_calls':json.dumps(source['expected_calls'],ensure_ascii=False),
                        'before_correct':a['grade']['correct'],'after_correct':b['grade']['correct'],
                        'before_output':a['generation']['text'],'after_output':b['generation']['text'],
                        'difference_category':diagnostic(source['expected_calls'],b)})
        atomic_json(self.out/'8000-versus-3000.json', {'examples_3000': before,
                    'examples_8000': results['saved_8000'], 'test_read': False,
                    'paired_changes':dict(paired),
                    'same_input_hashes_required': True,
                    'note': 'Check environment.json before interpreting hardware differences.'})
        if evaluate_only:
            return
        if passes(results['saved_8000']):
            full = self.evaluate('saved_8000',full=True)
            if passes(full):
                atomic_json(self.out/'conclusion.json',{'selected':'saved_8000','full_val':full,
                            'full_val_passes':True,'test_read':False,'goal_achieved':False,
                            'note':'Full val passes; no extra training needed. Test is NOT included or executed.'})
                return
        for arm in ARMS:
            self.train(arm)
            # Resolve immutable checkpoint for evaluation.
            self.model_label = None
            results[arm] = self.evaluate(arm)
        selected = choose(results)
        atomic_json(self.out/'comparison.json', {'val240': results, 'selected': selected,
                    'selection_rule': 'More total exact matches without call/no-call regression vs saved8000; ties keep saved8000',
                    'ablation_effect_vs_control': {arm: {
                        k: results[arm][k]['correct']-results['control'][k]['correct'] for k in ['all','call','no_call']}
                        for arm in ARMS[1:]} if len(results)>1 else {}, 'test_read': False})
        # Spend full-val compute only on an improved candidate or a passing baseline.
        if selected != 'saved_8000' or passes(results[selected]):
            full = self.evaluate(selected, full=True)
            atomic_json(self.out/'conclusion.json', {'selected': selected, 'full_val': full,
                        'full_val_passes': passes(full), 'test_read': False,
                        'goal_achieved': False, 'note': 'Final test is not included or executed by v79.'})
        else:
            atomic_json(self.out/'conclusion.json', {'selected': selected, 'improvement_confirmed': False,
                        'test_read': False, 'goal_achieved': False})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--hours', type=float, default=9)
    parser.add_argument('--evaluate-only', action='store_true')
    args = parser.parse_args()
    try:
        experiment = Experiment(args.root, args.out, time.time()+args.hours*3600)
        experiment.run(args.evaluate_only)
    except BudgetReached as e:
        atomic_json(args.out/'paused.json', {'reason': str(e), 'test_read': False})
        print(str(e), flush=True)
    except Exception as e:
        import traceback
        args.out.mkdir(parents=True, exist_ok=True)
        atomic_json(args.out/'error.json', {'type': type(e).__name__, 'message': str(e), 'traceback': traceback.format_exc()})
        raise


if __name__ == '__main__':
    main()
