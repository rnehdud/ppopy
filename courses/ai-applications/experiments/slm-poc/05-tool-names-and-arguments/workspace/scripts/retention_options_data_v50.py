"""Freeze the three selected V49 methods plus a replay control. No prompt changes."""
import copy
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.heterogeneous_tool_checker_v1 import read, save, digest

DATA = ROOT / 'data/processed/retention-options-v50'
OUT = ROOT / 'output/diagnostics/retention-options-v50'
OLD = ROOT / 'data/processed/description-pairs-v41'
V45 = ROOT / 'data/processed/read-continue-v45'
START = ROOT / 'output/diagnostics/read-continue-v45/train/final-adapter'
ARMS = ('control', 'balanced', 'distilled', 'projected')
SEED = 500050


def sample(pool, n, rng):
    if not pool:
        raise ValueError('Empty teaching group')
    result = []
    while len(result) < n:
        order = copy.deepcopy(pool); rng.shuffle(order)
        result += order[:n-len(result)]
    return result


def prepare():
    if DATA.exists() or OUT.exists():
        raise FileExistsError('Frozen V50 protected')
    matrix = read(ROOT / 'output/research-matrix-v49/decision-matrix.json')
    if set(matrix['selected']) != {'preserve_outputs','balanced_stages','constrain_updates'}:
        raise ValueError('Selected methods changed')
    rows = read(OLD / 'train.json'); old = rows[:360]; generic = rows[360:]
    if len(old) != 360 or len(generic) != 336:
        raise ValueError('Source changed')
    rng = random.Random(SEED)
    stages = {}
    stages['start'] = []
    for target in ('a','b','c','none','ask'):
        stages['start'] += sample([r for r in generic if r['step']==0 and r['semantic_target']==target],20,rng)
    stages['after_one'] = sample([r for r in generic if r['step']==1 and r['semantic_target'] in ('a','b','c')],50,rng)
    stages['after_one'] += sample([r for r in generic if r['step']==1 and r['semantic_target']=='none'],50,rng)
    stages['after_two'] = sample([r for r in generic if r['step']==2 and r['semantic_target']=='none'],100,rng)
    stages['old_skin'] = []
    for target in ('record','show','ask','none'):
        stages['old_skin'] += sample([r for r in old if r['target']==target],25,rng)
    balanced = [r for stage in stages.values() for r in stage]; rng.shuffle(balanced)
    balanced_groups = [balanced[i:i+2] for i in range(0,400,2)]
    control_groups = read(V45 / 'training-groups.json')
    if len(balanced_groups)!=200 or len(control_groups)!=200:
        raise ValueError('Wrong budget')
    # Reference examples are TRAIN rows only, shared by ALL four arms.
    refs = []
    for target in ('record','show','ask','none'):
        refs += sample([r for r in old if r['target']==target],25,rng)
    refs += sample([r for r in generic if r['semantic_target'] in ('a','b','c')],50,rng)
    refs += sample([r for r in generic if r['semantic_target'] in ('none','ask')],50,rng)
    rng.shuffle(refs)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(ROOT / 'models/ko-decision-roberta-large',local_files_only=True)
    tok.model_max_length=1000000; lengths=[]
    for r in [r for g in control_groups+balanced_groups for r in g]+refs:
        lengths.append(max(map(len,tok([r['question']+' '+x for x in r['options'].values()],
            [r['context']]*len(r['options']),truncation=False)['input_ids'])))
    if max(lengths)>512:
        raise ValueError('No truncation allowed')
    DATA.mkdir(parents=True); OUT.mkdir(parents=True)
    save(DATA/'control-groups.json',control_groups); save(DATA/'balanced-groups.json',balanced_groups)
    save(DATA/'references.json',refs)
    save(OUT/'data-audit.json',{'start':len(stages['start']),'after_one':len(stages['after_one']),
        'after_two':len(stages['after_two']),'old_skin':len(stages['old_skin']),
        'unique_balanced_row_ids':len({r['id'] for r in balanced}),
        'unique_reference_ids':len({r['id'] for r in refs}),
        'references':len(refs),'max_tokens':max(lengths),'all_source_rows_unchanged':True})
    files=list(DATA.glob('*.json'))+[START/'adapter_model.safetensors', OLD/'train.json',
        OLD/'cases.json', V45/'cases.json', V45/'teacher-rows.json',
        ROOT/'output/research-matrix-v49/decision-matrix.json']+[ROOT/p for p in [
        'scripts/retention_options_data_v50.py','scripts/retention_options_learning_v50.py',
        'agent/retention_updates_v50.py','tests/test_retention_updates_v50.py']]
    save(OUT/'plan.json',{'arms':list(ARMS),'seed':SEED,'initial_adapter':str(START.relative_to(ROOT)),
        'updates':200,'main_rows_per_update':2,'reference_rows_per_update':1,
        'total_presentations_per_arm':600,'lr':1e-5,'clip_norm':1.,'weight_decay':0.,
        'temperature':2.,'distill_weight':1.,'projection_min_norm_sq':1e-20,
        'differences':{'control':'Original400 teaching presentations + shared200 reference CE.',
            'balanced':'Stage-balanced400 presentations + same200 reference CE.',
            'distilled':'Same balanced schedule plus T=2 KL on references that the initial model gets correct; coefficient1/3 after averaging three CE examples.',
            'projected':'Same balanced CE; post-AdamW update projected against reference CE gradient when predicted first-order change is positive. NOT the unmodified SGD A-GEM algorithm.'},
        'controls':'All models start same V45 weights, q/v LoRA only; questions/options/context are original source bytes, no new input format or tool guard. Balanced/distilled/projected same row schedule. All four same reference schedule. Extra computation differs and is timed.',
        'projection_limit':'First-order constraint for one sampled reference at that step, NOT guaranteed nonincreasing actual loss or preserved test accuracy. Zero/nonfinite references are explicitly reported or rejected.',
        'evaluation':'Freeze all4 finals first. Initial and4 finals on matched snapshots, heldout-split24 autonomous episodes, old V41 test56, old360 retention. New independent unknown-tool benchmark is NOT claimed.',
        'adoption':'Relative to control: test matched strict and paired-both choices must improve, continuation cannot drop; prior required-tools-completed/old360 cannot drop; unwanted state changes cannot increase. Also beat initial matched strict without worsening initial prior unnecessary changes. No automatic deployment.',
        'scope':'Authored previously evaluated local fixtures, prebound empty arguments. Public literature is adapted; paper success rates are not transferred.',
        'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files}})
    print('V50 frozen:4 arms; each200 updates,400 teaching+200 shared reference presentations',flush=True)


def verify():
    p=read(OUT/'plan.json')
    for path,sha in p['frozen_files'].items():
        if digest(ROOT/path)!=sha:raise ValueError('Frozen file changed: '+path)
    return p


if __name__=='__main__':prepare()
