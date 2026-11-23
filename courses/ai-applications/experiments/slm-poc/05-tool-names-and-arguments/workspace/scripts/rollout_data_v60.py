"""Freeze actual-visited-state experiment and held-out executable tasks."""
import copy,collections,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.retention_options_data_v50 import read,save,digest
from scripts.diverse_sources_data_v54 import START
from agent.rollout_files_v60 import SPECS,definitions,names
DATA=ROOT/'data/processed/rollout-v60';OUT=ROOT/'output/diagnostics/rollout-v60';SEED=590059

def make_files():
    # Manually authored expected values, not calculate() reused as its own oracle.
    examples={
      'sum':([4,7,2],{'sum':13}), 'range':([4,7,2],{'min':2,'max':7}),
      'positive':([-2,4,0,7],{'positive':[4,7]}),'sort':(['2026-11-03','2026-11-01'],{'dates':['2026-11-01','2026-11-03']}),
      'reverse':(['a','b','c'],{'reversed':['c','b','a']}),'lengths':(['ab','c'],{'lengths':[2,1]}),
      'squares':([2,-3],{'squares':[4,9]}),'unique':(['a','b','a'],{'unique':['a','b']})}
    rows=[]
    for family,(items,answer) in examples.items():
        noun,op=SPECS[family];verb=op.removesuffix('한다.');verb=verb.removesuffix('다.')
        # Use complete Korean clauses; suffixing the noun phrases is not a parser.
        action=op.replace('저장한다.','저장해 주세요.')
        split='dev' if family in ('squares','unique') else 'final'
        for kind in ('read','read_process','conditional','no_call','two_turns'):
            for style in range(4):
                prefix=['','부탁해요. ','이번에는 ','지금 '][style]
                empty=kind=='conditional' and style>=2
                available=['a','b','c'];payload={'items':[] if empty else items};out=copy.deepcopy(answer)
                if kind=='read':texts=[prefix+noun+' 파일 내용을 읽어 보여 주세요. 결과는 저장하지 마세요.'];roles=[['a']];outputs=[None]
                elif kind=='read_process':texts=[prefix+'먼저 '+noun+' 파일을 읽고, 읽은 자료로 '+action];roles=[['a','b']];outputs=[out]
                elif kind=='conditional':
                    # Empty/nonempty paired wording is exactly equal within each style pair.
                    prefix=['','부탁해요. '][style%2]
                    texts=[prefix+'먼저 '+noun+' 파일을 읽고 항목이 있으면 '+action+' 항목이 없으면 저장하지 말고 끝내 주세요.']
                    roles=[['a'] if empty else ['a','b']];outputs=[None if empty else out]
                elif kind=='no_call':
                    texts=[prefix+[
                        noun+'라는 말의 뜻만 설명해 주세요. 도구는 실행하지 마세요.',
                        noun+' 원본 파일을 삭제해 주세요. 삭제 도구가 없으면 아무 작업도 하지 마세요.',
                        action+' 저장 도구가 없으면 다른 도구도 실행하지 마세요.',
                        '제가 원하는 작업을 아직 정하지 않았어요. 먼저 무엇을 할지 물어봐 주세요.'][style]]
                    if style==2:available=['a','c']
                    roles=[[]];outputs=[None]
                else:
                    texts=[prefix+noun+' 파일 내용을 읽어 주세요. 지금은 저장하지 마세요.','방금 읽은 자료로 '+action]
                    roles=[['a'],['b']];outputs=[None,out]
                order=available.copy();random.Random(SEED+len(rows)).shuffle(order)
                rows.append({'id':f'v60:{split}:{family}:{kind}:{style}','split':split,'family':family,'kind':kind,'style':style,
                    'payload':payload,'available':available,'order':order,'order_seed':SEED+len(rows),
                    'turns':[{'text':t,'roles':r,'output':o} for t,r,o in zip(texts,roles,outputs)],
                    'label_source':'assistant-authored, frozen before model scoring; not independently reviewed'})
    return rows

def training_cases():
    old=read(ROOT/'data/processed/description-pairs-v41/cases.json');paired=read(ROOT/'data/processed/read-continue-v45/cases.json')
    rows=[]
    for family in ('note','todo','media','lamp','parcel','printer'):
        rows += [c for c in paired if c['split']=='train' and c['family']==family]
        pool=[c for c in old if c['split']=='train' and c['family']==family]
        random.Random(SEED).shuffle(pool);rows+=pool[:12]
    assert len(rows)==120 and all(c['split']=='train' for c in rows)
    return copy.deepcopy(rows)

def prepare():
    if DATA.exists() or OUT.exists():raise FileExistsError('V60 protected')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    rows=make_files();train=training_cases();save(DATA/'file-cases.json',rows);save(DATA/'training-cases.json',train)
    save(DATA/'file-tools.json',{f:definitions(f) for f in SPECS})
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True);tok.model_max_length=1000000
    from scripts.rollout_eval_v60 import harness_audit
    audit=harness_audit(rows,tok);save(OUT/'harness-audit.json',audit)
    if not audit['all_goals_and_model_stop']:raise ValueError('Harness cannot execute every authored task')
    if audit['max_tokens']>512:raise ValueError('Predeclared short-input comparison exceeds512; no model inference started')
    files=list(DATA.glob('*.json'))+[ROOT/'output/research-plan-v59/plan.json',START/'adapter_model.safetensors']
    for f in ('agent/rollout_files_v60.py','agent/rollout_teacher_v60.py','scripts/rollout_data_v60.py','scripts/rollout_collect_v60.py','scripts/rollout_train_v60.py','scripts/rollout_eval_v60.py','agent/generic_fixture_v41.py','tests/test_rollout_v60.py'):
        p=ROOT/f
        if not p.is_file():raise FileNotFoundError(p)
        files.append(p)
    save(OUT/'plan.json',{'seed':SEED,'lr':3e-5,'updates':200,'arms':['R','A','B'],'start':str(START.relative_to(ROOT)),
        'source':'Existing120 training-side fixture episodes only, no V58 or final episodes used for collection/labels.',
        'collect':'Save actual visited input; label only verified recoverable prefixes offline. New200 presentations60start70continue70end; within each stage wrong predictions sampled before correct examples; exact unique/repetition counts audited.',
        'training':'R=old600+old200; A/B=identical old600+new200, 4CE/4 per update. B preserves q/v adapter and initializes extra encoder linear LoRA outputs to zero. No classifier/base updates.',
        'scope':'Training uses original in-memory fixtures with prebound arguments. Dev/final use real local zero-argument session files. New names, operation families and all case labels are assistant-authored. No independent human accuracy claim.',
        'counts':{'collection':120,'dev':40,'final':120,'final_turns':144},
        'evaluation':'Freeze all successful final adapters before final scoring; report all arms, no best-checkpoint/prompt/rate search. R initial,V57 reference also scored. C native generator no local training, same registry/results/3 decisions, separate parsing costs.',
        'guard':'A/B vsR full goal+self-stop +12/120; save success and empty/nonempty and no-call not belowR; zero unwanted writes; old360 not belowinitial. Passing only triggers second seed and30 fresh human conversations, never auto-deploy.',
        'no_deployment':True,'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files}})
    print('V60 protocol frozen;120 collection,40dev,120final/144turns; harness max',audit['max_tokens'],flush=True)

def verify():
    p=read(OUT/'plan.json')
    for f,h in p['frozen_files'].items():
        if digest(ROOT/f)!=h:raise ValueError('Frozen file changed: '+f)
    return p
if __name__=='__main__':prepare()
