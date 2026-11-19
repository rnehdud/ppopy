"""Three frozen QLoRA comparisons; selection and test scoring are separate."""
import hashlib
import json
import random
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_tool_decision_mix_v1 import read_jsonl

DATA = ROOT / 'data/processed/tool-split-pilot-v1'
OUT = ROOT / 'output/training/tool-split-pilot-v1'
BASE = ROOT / 'models/ko-decision-roberta-large'
INITIAL = ROOT / 'output/training/kotraj-kaggle-complete-v1/kotraj_choice/kotraj-choice-full-gpu-v1/final_adapter'


def sha(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def main():
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, BitsAndBytesConfig
    from peft import PeftModel, prepare_model_for_kbit_training, set_peft_model_state_dict
    from safetensors.torch import load_file
    if OUT.exists():
        raise FileExistsError('Frozen output directory exists')
    config = json.loads((ROOT / 'configs/tool-split-experiment-v1.json').read_text(encoding='utf8'))
    manifest = json.loads((DATA / 'manifest.json').read_text(encoding='utf8'))
    for name, expected in manifest['files'].items():
        if sha(DATA / name) != expected:
            raise ValueError('Frozen dataset hash changed: ' + name)
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA required')
    OUT.mkdir(parents=True)
    config.update(initial_adapter=str(INITIAL.relative_to(ROOT)), initial_adapter_sha256=sha(INITIAL / 'adapter_model.safetensors'),
                  dataset_manifest_sha256=sha(DATA / 'manifest.json'), review_sha256=sha(DATA / 'pre-scoring-review.json'),
                  device=torch.cuda.get_device_name(0), torch_version=torch.__version__)
    (OUT / 'config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf8')
    torch.backends.cuda.matmul.allow_tf32 = True
    tokenizer = AutoTokenizer.from_pretrained(BASE, local_files_only=True)
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
    base = AutoModelForSequenceClassification.from_pretrained(BASE, local_files_only=True, dtype=torch.float16,
        quantization_config=quant, device_map={'': 0}, attn_implementation='sdpa')
    base = prepare_model_for_kbit_training(base, use_gradient_checkpointing=False)
    model = PeftModel.from_pretrained(base, str(INITIAL), is_trainable=True)
    params = [p for p in model.parameters() if p.requires_grad]
    if not params or any('lora_' not in name for name, p in model.named_parameters() if p.requires_grad):
        raise RuntimeError('Only existing LoRA weights may train')
    initial = load_file(str(INITIAL / 'adapter_model.safetensors'))
    initial_weights = {name: p.detach().cpu().clone() for name, p in model.named_parameters() if p.requires_grad}
    baseline_dir = OUT / 'baseline_adapter'
    model.save_pretrained(baseline_dir, safe_serialization=True)
    probe = read_jsonl(DATA / 'flat_train.jsonl')[0]

    def logits(row):
        batch = tokenizer([row['question'] + ' ' + v for v in row['options'].values()],
                          [row['context']] * len(row['options']), padding=True, truncation=False, return_tensors='pt')
        if batch['input_ids'].shape[1] > config['max_tokens']:
            raise ValueError('No truncation: ' + row['id'])
        with torch.autocast('cuda', dtype=torch.float16):
            return model(**{k: v.to('cuda') for k, v in batch.items()}).logits[:, 0].float()

    result = {'config': config, 'baseline_adapter': str(baseline_dir.relative_to(ROOT)), 'runs': {}, 'production_modified': False}
    overall = time.perf_counter()
    for arm in ['selector', 'flat', 'gate']:
        set_peft_model_state_dict(model, initial)
        model.gradient_checkpointing_disable()
        random.seed(config['seed'])
        torch.manual_seed(config['seed'])
        torch.cuda.manual_seed_all(config['seed'])
        rows = read_jsonl(DATA / (arm + '_train.jsonl'))
        random.shuffle(rows)
        optimizer = torch.optim.AdamW(params, lr=config['learning_rate'], weight_decay=0, foreach=False)
        scaler = torch.amp.GradScaler('cuda')
        log, skipped = [], 0
        started = time.perf_counter()
        print('START', arm, len(rows), 'rows; trainable', sum(p.numel() for p in params), flush=True)
        for cursor in range(0, len(rows), config['effective_batch']):
            chunk = rows[cursor:cursor + config['effective_batch']]
            model.train()
            optimizer.zero_grad(set_to_none=True)
            weighted_loss = 0.
            weight_sum = sum(r.get('replay_weight', 1.) for r in chunk)
            for row in chunk:
                checkpointing = len(row['options']) > 6
                if checkpointing:
                    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
                values = logits(row)
                target = torch.tensor([list(row['options']).index(row['target'])], device='cuda')
                loss = torch.nn.functional.cross_entropy(values.unsqueeze(0), target)
                if not torch.isfinite(loss):
                    raise RuntimeError('Nonfinite loss')
                weight = row.get('replay_weight', 1.) / weight_sum
                scaler.scale(loss * weight).backward()
                weighted_loss += float(loss.detach()) * weight
                if checkpointing:
                    model.gradient_checkpointing_disable()
            scaler.unscale_(optimizer)
            norm = float(torch.nn.utils.clip_grad_norm_(params, 1.))
            scale_before = scaler.get_scale()
            scaler.step(optimizer)
            scaler.update()
            if scaler.get_scale() < scale_before:
                skipped += 1
            seen = cursor + len(chunk)
            step = cursor // config['effective_batch'] + 1
            if step % 10 == 0 or seen == len(rows):
                record = {'step': step, 'seen': seen, 'loss': weighted_loss, 'grad_norm': norm,
                          'seconds': time.perf_counter() - started, 'peak_gib': torch.cuda.max_memory_allocated() / 2**30}
                log.append(record)
                with (OUT / (arm + '-training.jsonl')).open('a', encoding='utf8') as file:
                    file.write(json.dumps(record) + '\n')
                print(arm, seen, '/', len(rows), 'loss', round(weighted_loss, 4), 'sec', round(record['seconds']), flush=True)
            if step % 50 == 0 or seen == len(rows):
                model.save_pretrained(OUT / (arm + '_latest'), safe_serialization=True)
                torch.save({'optimizer': optimizer.state_dict(), 'scaler': scaler.state_dict(), 'seen': seen}, OUT / (arm + '-optimizer.pt'))
        folder = OUT / (arm + '_adapter')
        model.save_pretrained(folder, safe_serialization=True)
        delta = max(float((p.detach().cpu() - initial_weights[name]).abs().max()) for name, p in model.named_parameters() if p.requires_grad)
        model.eval()
        with torch.inference_mode():
            expected = logits(probe).cpu()
        with torch.no_grad():
            params[0].add_(.02)
        set_peft_model_state_dict(model, load_file(str(folder / 'adapter_model.safetensors')))
        with torch.inference_mode():
            difference = float((expected - logits(probe).cpu()).abs().max())
        if delta <= 0 or difference > 1e-4:
            raise RuntimeError('Adapter verification failed')
        result['runs'][arm] = {'adapter': str(folder.relative_to(ROOT)), 'rows': len(rows),
            'seconds': time.perf_counter() - started, 'weight_max_abs_delta': delta,
            'reload_max_abs_logit_difference': difference, 'skipped_steps': skipped,
            'last_loss': log[-1]['loss']}
        (OUT / 'training-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
        print('SAVED', arm, result['runs'][arm], flush=True)
        del optimizer
    if sha(INITIAL / 'adapter_model.safetensors') != config['initial_adapter_sha256']:
        raise RuntimeError('Initial adapter was modified')
    result['seconds'] = time.perf_counter() - overall
    (OUT / 'training-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print('TRAINING COMPLETE', round(result['seconds']), 'seconds', flush=True)


if __name__ == '__main__':
    main()
