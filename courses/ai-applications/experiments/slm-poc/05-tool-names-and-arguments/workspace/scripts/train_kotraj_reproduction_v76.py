"""Kotraj-only native-format LoRA; val selection and one protected final test."""
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.korean_material_v67 import MODEL, REV, sha, stable
from scripts.unquantized_caller_v72 import Native as OriginalNative
from scripts.retail_data_v65 import encode_example
from training.retail_native_v65 import assistant_loss
from training.kotraj_reproduction_v76 import grade, summarize, passes

DATA = ROOT / 'data/processed/kotraj-reproduction-v76'
OUT = ROOT / 'output/kotraj-reproduction-v76'
SEED = 760076
MILESTONES = [3000, 9000, 18000]


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def jsonl(path):
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def prepare():
    d = read(DATA/'plan.json')
    for p, h in d['files'].items():
        assert sha(ROOT/p) == h, p
    OUT.mkdir(parents=True, exist_ok=False)
    frozen = [Path(__file__), DATA/'plan.json', ROOT/'scripts/unquantized_caller_v72.py',
              ROOT/'agent/retail_attention_v65.py', ROOT/'scripts/retail_data_v65.py',
              ROOT/'training/retail_native_v65.py', ROOT/'training/kotraj_reproduction_v76.py',
              ROOT/'tests/test_kotraj_reproduction_v76.py']
    write(OUT/'plan.json', {
        'model': MODEL, 'revision': REV, 'seed': SEED, 'dataset': 'kotraj-v02 only',
        'weights': 'Fresh original cached xLAM base, uncompressed FP16, RMSNorm FP32, zero-B LoRA r8/alpha16/dropout0.05/all-linear. No old local trained adapter.',
        'training': {'learning_rate': 1e-5, 'milestones_presentations': MILESTONES,
                     'gradient_accumulation': 4, 'max_train_tokens': 8192, 'max_target_tokens': 1024,
                     'optimizer': 'AdamW weight_decay0, constant LR, clip1, FP16 GradScaler',
                     'sampling': 'Fixed source decision order:2 call-required to1 no-call, each independently seed-shuffled, without replacement. Limits are accepted training examples. Over-length examples skipped with IDs; no truncation. Val/test retain all examples.',
                     'target': 'Original source call arrays or native source no-call text. Native format instruction plus unchanged original system policy; no [] remapping.'},
        'inference': {'max_new_tokens':1024, 'greedy':True, 'input_truncation':False,
                      'attention':'Existing cuDNN long-query/math short-query kernels'},
        'selection': 'Evaluate fixed240 val-monitor before training and at3000/9000/18000 presentations. If all/call accuracies each exceed90%, evaluate ALL val decisions. Only after both full-val metrics exceed90%, freeze candidate and run test ONCE. Final failure stops this run without test-driven adjustment.',
        'acceptance': 'Both full val and final test: all-decision exact calls/no-call accuracy >90% and call-required exact names+arguments batch accuracy >90%. No new deployment/skin/general unseen-domain conditions.',
        'evaluation_scope': 'Source-prefix reproduction, not free-running actual external API execution. Prior history/results are source data; only next assistant decision is generated.',
        'raw_first_pass_noncall_format': 'Natural language is allowed, empty/malformed JSON or unfinished output fail. No call/argument repair.',
        'reproducibility': 'Fixed source hashes, group splits, model revision, tool order, seed, training order, raw outputs/input-ID hashes and checkpoint/optimizer/RNG state. Cross-hardware bitwise identity is not assumed.',
        'test_read_before_candidate_frozen':False,
        'frozen_files': {str(p.relative_to(ROOT)):sha(p) for p in frozen},
    })
    print('V76 training/evaluation contract frozen. No model loaded.', flush=True)


def verify():
    p = read(OUT/'plan.json')
    for name, h in p['frozen_files'].items():
        assert sha(ROOT/name) == h, name
    for name, h in read(DATA/'plan.json')['files'].items():
        assert sha(ROOT/name) == h, name
    return p


class Native(OriginalNative):
    def __init__(self):
        super().__init__()
        rendered = self.tokenizer.apply_chat_template([{'role':'user','content':'probe'}], tools=[], tokenize=False)
        self.default = rendered.split('<|im_start|>system\n', 1)[1].split('<|im_end|>', 1)[0].strip()

    def history(self, source):
        result = copy.deepcopy(source)
        policies = [m.get('content') or '' for m in result if m['role'] == 'system']
        return [{'role':'system','content':self.default+'\n\nSource instructions:\n'+'\n\n'.join(policies)}] + [m for m in result if m['role'] != 'system']

    def generate_row(self, row):
        torch = self.torch
        b = self.tokenizer.apply_chat_template(self.history(row['messages']), tools=row['tools'],
               add_generation_prompt=True, return_dict=True, return_tensors='pt')
        length = int(b['input_ids'].shape[1])
        digest = hashlib.sha256(b['input_ids'].numpy().tobytes()).hexdigest()
        info = {'input_tokens':length, 'input_ids_sha256':digest, 'text':'', 'finished':False}
        if length+1024 > self.model.config.max_position_embeddings:
            return {**info, 'error':'context_overflow_no_truncation'}
        b = {k:v.to('cuda') for k,v in b.items()}
        started = time.perf_counter()
        with torch.inference_mode(), torch.autocast('cuda', dtype=torch.float16):
            out = self.model.generate(**b, max_new_tokens=1024, do_sample=False, use_cache=True,
                                      pad_token_id=self.tokenizer.eos_token_id)
        ids = out[0,length:]
        info.update(text=self.tokenizer.decode(ids, skip_special_tokens=True),
                    finished=bool(len(ids)) and int(ids[-1]) == self.tokenizer.eos_token_id,
                    output_tokens=len(ids), seconds=time.perf_counter()-started)
        return info


def evaluate(native, label, split='val', monitor=False):
    assert split in ['val','test']
    if split == 'test':
        assert (OUT/'selected-before-test.json').exists()
        assert passes(read(OUT/'selected-before-test.json')['full_val'])
    directory = OUT/label
    directory.mkdir(exist_ok=False)
    write(directory/'started.json', {'split':split, 'monitor':monitor, 'test':split=='test'})
    selected = set(read(DATA/'val-monitor-ids.json')) if monitor else None
    # The test file is opened only here, after the candidate is frozen.
    data = jsonl(DATA/(split+'.jsonl'))
    if selected is not None:
        by = {r['id']:r for r in data}
        data = [by[k] for k in read(DATA/'val-monitor-ids.json')]
        assert len(data) == 240
    results = []
    native.model.eval()
    with (directory/'predictions.jsonl').open('x', encoding='utf-8') as f:
        for i, r in enumerate(data):
            g = native.generate_row(r)
            result = {'id':r['id'], 'generation':g, 'grade':grade(r['expected_calls'], g)}
            results.append(result)
            f.write(json.dumps(result, ensure_ascii=False)+'\n')
            f.flush()
            if (i+1)%10 == 0:
                print(label, i+1, '/', len(data), json.dumps(summarize(results)), flush=True)
    summary = summarize(results)
    summary.update(split=split, monitor_only=monitor, evaluation='source_prefix_reproduction')
    write(directory/'summary.json', summary)
    return summary


def checkpoint(native, optimizer, scaler, count, cursor):
    torch = native.torch
    path = OUT/'checkpoints'/('examples-'+str(count))
    assert not path.exists()
    native.model.save_pretrained(path, safe_serialization=True)
    torch.save({'optimizer': optimizer.state_dict() if optimizer else None,
                'scaler':scaler.state_dict() if scaler else None, 'presentations':count, 'cursor':cursor,
                'python_rng':random.getstate(), 'torch_rng':torch.random.get_rng_state(),
                'cuda_rng':torch.cuda.get_rng_state_all()}, path/'training-state.pt')
    write(path/'manifest.json', {'model':MODEL, 'revision':REV, 'presentations':count,
              'adapter_sha256':sha(path/'adapter_model.safetensors'), 'training_state_sha256':sha(path/'training-state.pt')})
    return path


def consider_final(native, label, monitor, checkpoint_path):
    if not passes(monitor):
        return False
    full = evaluate(native, label+'-full-val')
    if not passes(full):
        return False
    write(OUT/'selected-before-test.json', {'label':label, 'checkpoint':str(checkpoint_path.relative_to(ROOT)),
            'adapter_sha256':sha(checkpoint_path/'adapter_model.safetensors'), 'full_val':full,
            'plan_sha256':sha(OUT/'plan.json'), 'test_read':False})
    test = evaluate(native, label+'-final-test', split='test')
    write(OUT/'result.json', {'full_val':full, 'test':test, 'threshold_exceeded':passes(full) and passes(test),
             'selected':label, 'scope':'kotraj source-prefix call reproduction only',
             'test_tuned':False, 'production_changed':False})
    verify()
    print('V76 FINAL', json.dumps(read(OUT/'result.json')), flush=True)
    return True  # A failed final is not reused to select a new candidate.


def main():
    verify()
    assert not (OUT/'started.json').exists(), 'Protected run; preserve existing results'
    write(OUT/'started.json', {'pid':os.getpid(), 'test_read':False})
    import torch
    random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    assert torch.cuda.mem_get_info()[0] > 5*2**30, 'Another GPU model may be running'
    n = Native()
    write(OUT/'environment.json', {'torch':torch.__version__, 'gpu':torch.cuda.get_device_name(),
             'base_allocated_GiB':torch.cuda.memory_allocated()/2**30, 'python':sys.version,
             'model':MODEL, 'revision':REV, 'base_is_4bit':bool(getattr(n.model,'is_loaded_in_4bit',False))})
    baseline = evaluate(n, 'baseline-val-monitor', monitor=True)
    if passes(baseline):
        path = checkpoint(n, None, None, 0, 0)
        if consider_final(n, 'baseline', baseline, path):
            return
    rows = jsonl(DATA/'train.jsonl')
    calls = [r for r in rows if r['expected_calls']]
    noncalls = [r for r in rows if not r['expected_calls']]
    rng = random.Random(SEED)
    rng.shuffle(calls); rng.shuffle(noncalls)
    order = []
    for i in range(min(len(calls)//2, len(noncalls))):
        order.extend([calls[2*i], calls[2*i+1], noncalls[i]])
    write(OUT/'training-order.json', [r['id'] for r in order])
    del rows, calls, noncalls
    n.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    n.model.enable_input_require_grads()
    n.model.train()
    optimizer = torch.optim.AdamW([p for p in n.model.parameters() if p.requires_grad], lr=1e-5, weight_decay=0)
    scaler = torch.amp.GradScaler('cuda')
    optimizer.zero_grad(set_to_none=True)
    accepted = updates = skipped = 0
    started = time.perf_counter()
    with (OUT/'training-log.jsonl').open('x', encoding='utf-8') as log, (OUT/'training-skips.jsonl').open('x', encoding='utf-8') as rejected:
        for cursor, row in enumerate(order):
            history = n.history(row['messages'])
            ids, start = encode_example(n.tokenizer, history, row['target'], row['tools'])
            if len(ids)>8192 or len(ids)-start>1024:
                rejected.write(json.dumps({'id':row['id'], 'tokens':len(ids), 'target_tokens':len(ids)-start})+'\n')
                rejected.flush();skipped += 1
                continue
            n.model.train()
            b = torch.tensor([ids], device='cuda')
            with torch.autocast('cuda', dtype=torch.float16):
                loss = assistant_loss(n.model, b, start)
            if not bool(torch.isfinite(loss)):
                raise ValueError('Non-finite training loss; no silent retry')
            scaler.scale(loss/4).backward()
            accepted += 1
            if accepted%4 == 0:
                scaler.unscale_(optimizer)
                norm = torch.nn.utils.clip_grad_norm_([p for p in n.model.parameters() if p.requires_grad], 1.0)
                if not bool(torch.isfinite(norm)):
                    raise ValueError('Non-finite gradient; no silent skipped update')
                scaler.step(optimizer);scaler.update();optimizer.zero_grad(set_to_none=True);updates += 1
            info = {'presentations':accepted, 'updates':updates, 'cursor':cursor, 'id':row['id'],
                    'kind':row['kind'], 'tokens':len(ids), 'target_tokens':len(ids)-start,
                    'loss':float(loss.detach()), 'seconds':time.perf_counter()-started, 'skipped':skipped}
            log.write(json.dumps(info)+'\n');log.flush()
            del b, loss
            if accepted%20 == 0:
                print('V76 TRAIN', json.dumps(info), flush=True)
            if accepted%200 == 0:
                torch.cuda.empty_cache()
            if accepted in MILESTONES:
                assert accepted%4 == 0
                path = checkpoint(n, optimizer, scaler, accepted, cursor)
                n.model.eval();torch.cuda.empty_cache()
                monitor = evaluate(n, 'examples-'+str(accepted)+'-val-monitor', monitor=True)
                if consider_final(n, 'examples-'+str(accepted), monitor, path):
                    return
                n.model.train()
            if accepted == MILESTONES[-1]:
                break
    verify()
    write(OUT/'not-reached.json', {'presentations':accepted, 'updates':updates, 'skipped':skipped,
              'full_val_and_test_above90':False, 'test_read':False,
              'reason':'Predeclared training milestones did not produce a candidate passing full val; no final test consumed.'})
    print('V76 milestones finished; target not reached. Test untouched.', flush=True)


if __name__ == '__main__':
    if '--prepare' in sys.argv:
        prepare()
    else:
        try:
            main()
        except Exception as e:
            import traceback
            if OUT.exists() and not (OUT/'failure.json').exists():
                write(OUT/'failure.json', {'type':type(e).__name__, 'message':str(e), 'traceback':traceback.format_exc()})
            raise
