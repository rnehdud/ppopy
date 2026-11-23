"""One frozen native xLAM QLoRA pilot, with real required-argument file tests."""
import copy
import gc
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.retail_data_v65 import OUT, REPO, REV, sha
from scripts.rollout_xlam_v60 import Native, turn, parse
from agent.retail_transfer_v65 import cases, Files, definitions, names, evaluate_turn, SPEC


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def save(name, value):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def verify():
    plan = read('plan.json')
    for path, expected in plan['frozen_files'].items():
        if sha(ROOT / path) != expected:
            raise ValueError('Frozen input changed: ' + path)
    return plan


def prepare():
    # Must be called only after source readiness and meaningful unit checks pass.
    assert len(read('train.json')) == 160 and len(read('dev.json')) == 24
    save('fresh-cases.json', cases())
    save('fresh-tools.json', {f: definitions(f) for f in SPEC})
    paths = [ROOT / p for p in ['scripts/retail_experiment_v65.py', 'scripts/retail_data_v65.py',
             'scripts/retail_replay_v65.py', 'agent/retail_transfer_v65.py', 'training/retail_native_v65.py',
             'tests/test_retail_native_v65.py', 'scripts/rollout_xlam_v60.py']]
    paths += [OUT / p for p in ['train.json', 'dev.json', 'source-replay.json', 'source-replay-batch2.json',
              'data-readiness-expanded.json', 'fresh-cases.json', 'fresh-tools.json', 'source-db.json']]
    save('plan.json', {'seed': 650065, 'repo': REPO, 'revision': REV,
         'training': {'steps': 80, 'presentations': 160, 'lr': 3e-5, 'lora_r': 8, 'lora_alpha': 16,
                      'lora_dropout': 0.05, 'target_modules': 'all-linear', 'max_tokens': 8192,
                      'quantization': 'NF4 double quantization / float16 compute', 'grad_clip': 1.0,
                      'loss': 'assistant target tokens only; exact standard masked causal loss via sparse LM head',
                      'checkpoint_selection': 'final step80 only; no selection from evaluation results'},
         'evaluation': {'primary': '48 fresh Korean real-file episodes, 54 turns, six new tool families, required mode argument',
             'source_dev': '24 user-group-disjoint recorded-prefix decisions; exact call arrays vs text/call type only, not dialogue success',
             'max_new_tokens': 192, 'max_calls_per_turn': 3, 'max_decisions_per_turn': 3,
             'parser': 'unchanged strict native array; no JSON repair, name repair, argument dropping or fallback tool substitution'},
         'gate': {'minimum_primary_gain_episodes': 5, 'unwanted_writes': 0,
                  'required_correct_write_not_lower_than_base': True, 'no_call_not_lower_than_base': True,
                  'base_successful_episodes_must_remain_successful': True},
         'scope': 'Assistant-authored fresh evaluation, no independent human labels. New source held out from this additional training, '
                  'not claimed absent from original pretraining. No Qwen response or skin-state pipeline evaluation. No deployment.',
         'amendment_before_model_scoring': 'Initial 80 source trajectories left15 eligible training writes, below24. '
                  'Expanded to next disjoint80 in same fixed source order; no class quota/rate changed and no model outcomes seen.',
         'frozen_files': {str(p.relative_to(ROOT)): sha(p) for p in paths}})
    print('V65 PLAN FROZEN: one pilot, no model outcomes seen', flush=True)


class PilotNative(Native):
    def generate(self, messages, tools):
        import torch
        b = self.tokenizer.apply_chat_template(messages, tools=tools, add_generation_prompt=True,
                                               return_dict=True, return_tensors='pt')
        n = b['input_ids'].shape[1]
        if n + 192 > self.model.config.max_position_embeddings:
            raise ValueError('Context overflow; no truncation')
        b = {k: v.to('cuda') for k, v in b.items()}
        started = time.perf_counter()
        with torch.inference_mode():
            out = self.model.generate(**b, max_new_tokens=192, do_sample=False, use_cache=True,
                                      pad_token_id=self.tokenizer.eos_token_id)
        tokens = out[0, n:]; text = self.tokenizer.decode(tokens, skip_special_tokens=True)
        return text, {'text': text, 'input_tokens': int(n), 'output_tokens': len(tokens),
               'finished': bool(len(tokens)) and int(tokens[-1]) == self.tokenizer.eos_token_id,
               'seconds': time.perf_counter() - started, 'messages': copy.deepcopy(messages), 'tools': copy.deepcopy(tools),
               'input_ids_sha256': hashlib.sha256(b['input_ids'].cpu().numpy().tobytes()).hexdigest()}


def evaluate(native, label):
    native.model.eval(); episodes = []; started = time.perf_counter()
    for index, case in enumerate(read('fresh-cases.json')):
        service = Files(OUT / 'work' / label / case['id'].replace(':', '-'), case['family'], case['payload'])
        public = {k: case[k] for k in ['available', 'order', 'order_seed']}
        history = []; turns = []
        for expected in case['turns']:
            trace, history = turn(native, expected['text'], service, public, history)
            result = evaluate_turn(expected, trace, service)
            branch = case['kind'] in ['nonempty', 'empty'] and any(
                names(case['family'])['b'] in batch['names'] and not batch['cache_before_generation']
                for batch in trace['batches'])
            result['premature_conditional_batch'] = branch
            if branch: result['goal_and_stop'] = False; result['goal_ok'] = False
            turns.append({'input': expected['text'], 'expected': expected, 'trace': trace,
                          'grade': result, 'actual': service.snapshot()})
        item = {'id': case['id'], 'family': case['family'], 'kind': case['kind'], 'turns': turns,
                'goal_and_stop': all(t['grade']['goal_and_stop'] for t in turns)}
        episodes.append(item); save(label + '-episodes/' + case['id'].replace(':', '-') + '.json', item)
        if (index + 1) % 6 == 0:
            print('V65 EVAL', label, index + 1, '/48 sec', round(time.perf_counter() - started), flush=True)
    save(label + '-files.json', {'episodes': episodes, 'seconds': time.perf_counter() - started})
    decisions = []
    for index, row in enumerate(read('dev.json')):
        raw, generation = native.generate(row['messages'], row['tools'])
        try:
            calls = parse(raw) if generation['finished'] else 'unfinished'
            reference = [c['function'] for c in row['target'].get('tool_calls') or []]
            correct = (calls == reference) if reference else calls is None or calls == []
        except Exception:
            correct = False
        decisions.append({'id': row['id'], 'bucket': row['bucket'], 'correct': correct,
                          'generation': generation, 'target': row['target']})
        if (index + 1) % 8 == 0: print('V65 SOURCE DEV', label, index + 1, '/24', flush=True)
    save(label + '-dev.json', decisions)


def train(native, plan):
    import torch
    from peft import get_peft_model_state_dict, set_peft_model_state_dict
    from safetensors.torch import load_file
    from training.retail_native_v65 import assistant_loss
    model = native.model; rows = read('train.json')
    calls = [r for r in rows if r['bucket'] != 'text']; texts = [r for r in rows if r['bucket'] == 'text']
    rng = random.Random(plan['seed']); rng.shuffle(calls); rng.shuffle(texts)
    params = {n: p for n, p in model.named_parameters() if p.requires_grad}
    assert params and all('lora_' in n for n in params)
    initial = {n: p.detach().cpu().clone() for n, p in params.items()}
    optimizer = torch.optim.AdamW(list(params.values()), lr=plan['training']['lr'], weight_decay=0, foreach=False)
    scaler = torch.amp.GradScaler('cuda', init_scale=128.0)
    model.config.use_cache = False
    torch.cuda.reset_peak_memory_stats(); started = time.perf_counter(); logs = []
    for step, pair in enumerate(zip(calls, texts), 1):
        model.train()
        for attempt in range(12):
            optimizer.zero_grad(set_to_none=True); losses = []
            for row in pair:
                ids = torch.tensor([row['input_ids']], device='cuda')
                with torch.autocast('cuda', dtype=torch.float16):
                    loss = assistant_loss(model, ids, row['target_start'])
                if not torch.isfinite(loss): raise ValueError('Nonfinite loss')
                losses.append(float(loss.detach())); scaler.scale(loss / 2).backward()
                del ids, loss
            scaler.unscale_(optimizer)
            norm = float(torch.nn.utils.clip_grad_norm_(list(params.values()), 1.0))
            if math.isfinite(norm):
                scaler.step(optimizer); scaler.update(); break
            scaler.step(optimizer); scaler.update()
        else: raise ValueError('Repeated nonfinite gradients')
        entry = {'step': step, 'loss': sum(losses) / 2, 'gradient_norm': norm,
                 'ids': [r['id'] for r in pair], 'seconds': time.perf_counter() - started}
        logs.append(entry)
        with (OUT / 'training-log.jsonl').open('a', encoding='utf-8') as f: f.write(json.dumps(entry) + '\n')
        if step % 8 == 0: print('V65 TRAIN', step, '/80 loss', round(entry['loss'], 4), 'sec', round(entry['seconds']), flush=True)
    assert len(logs) == 80
    model.eval(); target = OUT / 'final-adapter'; model.save_pretrained(target, safe_serialization=True)
    probe_ids = torch.tensor([rows[0]['input_ids'][-128:]], device='cuda')
    def probe():
        with torch.inference_mode(): return model(input_ids=probe_ids, logits_to_keep=2, use_cache=False).logits.detach().float().cpu()
    before = probe()
    change = max(float((p.detach().cpu() - initial[n]).abs().max()) for n, p in params.items())
    with torch.no_grad(): next(iter(params.values())).add_(0.01)
    set_peft_model_state_dict(model, load_file(str(target / 'adapter_model.safetensors')))
    after = probe(); error = float((before - after).abs().max())
    if change <= 0 or error > 1e-5: raise ValueError('Adapter update/reload not verified')
    save('training-complete.json', {'steps': 80, 'presentations': 160, 'seconds': time.perf_counter() - started,
         'trainable_parameters': sum(p.numel() for p in params.values()), 'max_weight_change': change,
         'reload_error': error, 'peak_allocated_GiB': torch.cuda.max_memory_allocated() / 2**30,
         'adapter_sha256': sha(target / 'adapter_model.safetensors')})
    del optimizer, scaler, initial, params, probe_ids, before, after
    gc.collect(); torch.cuda.empty_cache()


def summarize():
    summaries = {}
    for label in ['before', 'after']:
        rows = read(label + '-files.json')['episodes']; turns = [t for r in rows for t in r['turns']]
        summaries[label] = {'episodes': len(rows), 'goal_and_stop': sum(r['goal_and_stop'] for r in rows),
             'required_correct_write': sum(t['grade']['requested_correct_write'] for t in turns), 'required_write_turns': 24,
             'unwanted_writes': sum(t['grade']['unwanted_write'] for t in turns),
             'unwanted_write_attempts': sum(t['grade']['unwanted_write_attempt'] for t in turns),
             'no_call_correct': sum(r['goal_and_stop'] for r in rows if r['kind'] in ['ask', 'missing']),
             'no_call_n': 12, 'by_kind': {k: {'n': sum(r['kind'] == k for r in rows),
                    'correct': sum(r['goal_and_stop'] for r in rows if r['kind'] == k)} for k in sorted({r['kind'] for r in rows})},
             'source_dev': {'n': 24, 'correct': sum(d['correct'] for d in read(label + '-dev.json'))}}
    old = {r['id']: r for r in read('before-files.json')['episodes']}; new = {r['id']: r for r in read('after-files.json')['episodes']}
    gained = [k for k in old if not old[k]['goal_and_stop'] and new[k]['goal_and_stop']]
    lost = [k for k in old if old[k]['goal_and_stop'] and not new[k]['goal_and_stop']]
    b = summaries['before']; a = summaries['after']
    accepted = (a['goal_and_stop'] >= b['goal_and_stop'] + 5 and a['unwanted_writes'] == 0
                and a['required_correct_write'] >= b['required_correct_write'] and a['no_call_correct'] >= b['no_call_correct'] and not lost)
    save('summary.json', {'results': summaries, 'gained': gained, 'lost': lost, 'adoptable_research_candidate': accepted,
         'scope': read('plan.json')['scope'], 'production_changed': False})
    print('V65 COMPLETE', json.dumps(summaries), 'ADOPTABLE', accepted, flush=True)


def main():
    if '--prepare' in sys.argv: return prepare()
    plan = verify()
    if (OUT / 'started.json').exists(): raise FileExistsError('V65 experiment protected')
    save('started.json', {'plan_sha256': sha(OUT / 'plan.json')})
    import torch
    from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
    random.seed(plan['seed']); torch.manual_seed(plan['seed']); torch.cuda.manual_seed_all(plan['seed'])
    native = PilotNative()
    native.model = prepare_model_for_kbit_training(native.model, use_gradient_checkpointing=True,
                       gradient_checkpointing_kwargs={'use_reentrant': False})
    native.model.get_input_embeddings().to(dtype=torch.float16)
    native.model.get_output_embeddings().to(dtype=torch.float16)
    native.model = get_peft_model(native.model, LoraConfig(task_type=TaskType.CAUSAL_LM, r=8,
               lora_alpha=16, lora_dropout=0.05, target_modules='all-linear', bias='none'))
    save('model-setup.json', {'trainable_parameters': sum(p.numel() for p in native.model.parameters() if p.requires_grad),
                            'base_model_config': native.model.config.to_dict(),
                            'baseline': 'same prepared NF4 model, zero-initialized LoRA, before optimizer updates'})
    evaluate(native, 'before'); train(native, plan); verify(); evaluate(native, 'after'); summarize(); verify()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import traceback
        if (OUT / 'started.json').exists() and not (OUT / 'failure.json').exists():
            save('failure.json', {'type': type(error).__name__, 'message': str(error), 'traceback': traceback.format_exc()})
        raise
