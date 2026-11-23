"""Resource retry with an existing cuDNN long-query kernel and preflight."""
import json
from pathlib import Path
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import retail_experiment_v65 as experiment
from scripts.retail_attempt2_v65 import AutocastNative
from agent.retail_attention_v65 import install

PARENT = experiment.OUT
CHILD = PARENT / 'attempt3-cudnn'


class KernelNative(AutocastNative):
    def __init__(self):
        super().__init__()
        self.model.set_attn_implementation(install())


def preflight(native):
    import torch
    from training.retail_native_v65 import assistant_loss
    row = max(experiment.read('train.json'), key=lambda r: len(r['input_ids']))
    cpu_rng = torch.random.get_rng_state(); gpu_rng = torch.cuda.get_rng_state_all()
    native.model.train(); native.model.zero_grad(set_to_none=True)
    torch.cuda.reset_peak_memory_stats(); started = time.perf_counter()
    ids = torch.tensor([row['input_ids']], device='cuda')
    with torch.autocast('cuda', dtype=torch.float16):
        loss = assistant_loss(native.model, ids, row['target_start'])
    loss.backward()
    finite = all(bool(torch.isfinite(p.grad).all()) for p in native.model.parameters() if p.grad is not None)
    torch.cuda.synchronize()
    experiment.save('long-input-preflight.json', {'tokens': ids.shape[1], 'loss': float(loss.detach()),
        'finite_gradients': finite, 'optimizer_updates': 0,
        'peak_allocated_GiB': torch.cuda.max_memory_allocated() / 2**30,
        'seconds': time.perf_counter() - started, 'rng_restored': True})
    if not finite: raise ValueError('Preflight has nonfinite gradients')
    native.model.zero_grad(set_to_none=True); native.model.eval()
    del ids, loss
    torch.random.set_rng_state(cpu_rng); torch.cuda.set_rng_state_all(gpu_rng)
    torch.cuda.empty_cache()
    print('V65 longest-input forward/backward preflight passed', flush=True)


def main():
    experiment.OUT = CHILD
    experiment.PilotNative = KernelNative
    if '--prepare' in sys.argv:
        CHILD.mkdir(exist_ok=False)
        for name in ['train.json', 'dev.json', 'source-replay.json', 'source-replay-batch2.json',
                     'data-readiness-expanded.json', 'source-db.json']:
            shutil.copyfile(PARENT / name, CHILD / name)
        experiment.save('runtime-amendment.json', {
            'previous_attempt': 'attempt2-autocast; baseline48 retained, source-dev aborted before training',
            'reason': 'Flash attention unavailable in installed Windows torch. Default long-query SDPA saturated VRAM. '
                      'Existing cuDNN SDPA tested at8192 with finite backward and0.29GiB attention-only allocation.',
            'change': 'Unmodified Transformers SDPA operation with CUDNN_ATTENTION for query length>256, '
                      'MATH for short query/decoding. No input shortening or model parameter/attention-equation change. '
                      'Both baseline and trained model evaluated anew through this same kernel route.',
            'unchanged': '160 examples,24 development prefixes,48 Korean file episodes,all LoRA/optimizer settings,grading/guard.',
            'frozen_runtime_files': {str(p.relative_to(ROOT)): experiment.sha(p) for p in
                 [Path(__file__), ROOT / 'agent/retail_attention_v65.py', ROOT / 'scripts/retail_attempt2_v65.py']}})
        experiment.prepare(); return
    amendment = experiment.read('runtime-amendment.json')
    for p, h in amendment['frozen_runtime_files'].items():
        assert experiment.sha(ROOT / p) == h, p
    old_evaluate = experiment.evaluate
    def checked_evaluate(native, label):
        if label == 'before': preflight(native)
        return old_evaluate(native, label)
    experiment.evaluate = checked_evaluate
    experiment.main()
    for p, h in amendment['frozen_runtime_files'].items():
        assert experiment.sha(ROOT / p) == h, p


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import traceback
        if CHILD.exists() and not (CHILD / 'failure.json').exists():
            experiment.save('failure.json', {'type': type(error).__name__, 'message': str(error),
                                             'traceback': traceback.format_exc()})
        raise
