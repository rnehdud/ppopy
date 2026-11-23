"""Technical retry: explicit FP16 autocast for prepared-NF4 inference.

Attempt1 remains unchanged and invalid: no valid generation was obtained on
the real-file suite. This changes numerical execution, not data or scoring.
"""
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import retail_experiment_v65 as experiment

PARENT = experiment.OUT
CHILD = PARENT / 'attempt2-autocast'


class AutocastNative(experiment.PilotNative):
    def generate(self, messages, tools):
        import torch
        with torch.autocast('cuda', dtype=torch.float16):
            return super().generate(messages, tools)


def main():
    experiment.PilotNative = AutocastNative
    experiment.OUT = CHILD
    if '--prepare' in sys.argv:
        CHILD.mkdir(exist_ok=False)
        for name in ['train.json', 'dev.json', 'source-replay.json', 'source-replay-batch2.json',
                     'data-readiness-expanded.json', 'source-db.json']:
            shutil.copyfile(PARENT / name, CHILD / name)
        old = json.loads((PARENT / 'before-files.json').read_text(encoding='utf-8'))
        traces = [t['trace'] for r in old['episodes'] for t in r['turns']]
        errors = [g.get('error') for t in traces for g in t.get('generations', []) if g.get('error')]
        generated = sum('text' in g for t in traces for g in t.get('generations', []))
        if generated:
            raise ValueError('Do not classify a partial scientific result as a purely technical retry')
        experiment.save('runtime-amendment.json', {
            'parent_attempt': str(PARENT.relative_to(ROOT)), 'valid_generations_in_parent_file_suite': generated,
            'parent_error_count': len(errors), 'parent_errors': sorted(set(errors)),
            'change': 'Wrap generation in torch.autocast(cuda,float16), matching training autocast. '
                      'Prepared NF4 has FP32 normalization outputs and FP16 LM head; explicit autocast aligns operands.',
            'unchanged': '160 teacher examples,24 development examples,48 fresh file episodes,optimizer,LR,steps,LoRA,parser,grading,guard.',
            'driver_sha256': experiment.sha(Path(__file__)),
            'no_training_updates_in_parent': not (PARENT / 'training-log.jsonl').exists()})
        experiment.prepare()
        return
    amendment = experiment.read('runtime-amendment.json')
    if experiment.sha(Path(__file__)) != amendment['driver_sha256']:
        raise ValueError('Retry driver changed')
    experiment.main()
    if experiment.sha(Path(__file__)) != amendment['driver_sha256']:
        raise ValueError('Retry driver changed during run')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import traceback
        if CHILD.exists() and not (CHILD / 'failure.json').exists():
            experiment.save('failure.json', {'type': type(error).__name__, 'message': str(error),
                                             'traceback': traceback.format_exc()})
        raise
