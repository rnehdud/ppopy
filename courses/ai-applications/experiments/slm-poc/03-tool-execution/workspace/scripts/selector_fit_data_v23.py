"""Training-only fitting diagnostic. No held-out scoring or deployment."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_korean_data_v22 import verify as prior_verify,DATA as PRIOR,read,read_jsonl,save,digest,SELECTOR,view
DATA=ROOT/'data/processed/selector-fit-v23';OUT=ROOT/'output/diagnostics/selector-fit-v23';SEED=230015
HELD='toolace:7804:turn1'

def prepare():
    prior_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V23 protected')
    probes=[r for r in read_jsonl(PRIOR/'fit_probe.jsonl') if r['fit_probe_kind']=='new_training']
    rows=[r for r in probes if r['id']!=HELD]
    if len(probes)!=16 or len(rows)!=15:raise ValueError('Wrong reviewed source')
    # Explicit source/tool-purpose review BEFORE diagnostic inference. No relabel.
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    (DATA/'train.jsonl').write_text(''.join(__import__('json').dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    held=next(r for r in probes if r['id']==HELD)
    save(DATA/'review.json',{'reviewer':'assistant, not independent human gold','scope':'All16 source utterances, Korean utterances, every candidate purpose and preferred call reread;15 retained without changing labels, text, tools or order.',
        'held':{'id':HELD,'original':held['original_messages'][-1]['content'],'Korean':held['messages'][-1]['content'],'tools':{t['name']:t['description'] for t in held['tools']},'reason':'Korean asks whether website responds; tool purpose is responsive design. Original responsive is ambiguous. Do not train/relabel the inconsistent Korean pair; preserve frozen V22 records.'},
        'remaining_wrong_at_V22_baseline':['toolace:10142:turn1','toolace:2327:turn1','toolace:7413:turn1'],
        'label_limit':'Source preferred calls + assistant purpose check; no real API execution. Does not certify all V22 translations; one discovered issue is not a prevalence estimate.'})
    files=list(DATA.glob('*'))+[ROOT/p for p in ['scripts/selector_fit_data_v23.py','scripts/selector_fit_v23.py','scripts/report_selector_fit_v23.py','scripts/audit_selector_fit_v23.py','tests/test_selector_fit_v23.py','scripts/selector_broad_v20.py','scripts/selector_learning_v18.py','output/diagnostics/selector-korean-v22/baseline-fit-probe.json']]
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'n':15,'epochs':20,'batch':3,'steps':100,'arms':{'same_rate':1e-5,'larger_rate':1e-4},'read_epochs':[0,1,5,10,20],
        'fixed':'Original SELECTOR, current_full question, complete English source tools and reviewed Korean utterances. Only existing query/value LoRA parameters trainable, NF4 FP16, gradient checkpointing non-reentrant, dropout unchanged, clip1, AdamW weight_decay0. Same data/order/RNG/epochs across arms; only lr differs.',
        'purpose':'Can repeated training change the3 wrong choices on the very same15 training utterances? Fit diagnostic, NOT validation or unknown-tool accuracy. No unseen data is used to select prompt, schedule, checkpoint or arm.',
        'mechanical_checks':'Baseline reproduces saved V22 training-probe scores; labels map to correct candidate indices. Cross entropy checked against logsumexp form and analytic gradient. Record nonzero LoRA gradients, weight changes, final save/reload and reversed candidate order.',
        'stop':'Run both fixed arms through20 epochs, report train curves, corrections and regressions. No fresh40 or old600 model inference, no more rounds chosen from results, no deployment.16/16 is not a target; correctly retained set has15 rows.'})
    print('V23 FROZEN:15 training rows,2 learning rates,20epochs each; no held-out inference',flush=True)

def verify():
    prior_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V23 frozen file changed: '+rel)
    return p
if __name__=='__main__':prepare()
