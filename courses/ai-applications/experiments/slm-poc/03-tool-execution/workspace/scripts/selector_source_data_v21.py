"""Source-language fallback after the Korean translation gate failed.

English held-out selection and Korean reference retention are separate metrics.
Never present this as a fresh Korean evaluation.
"""
import collections,copy,csv,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_broad_data_v20 import MATERIAL,identities,groups,OLD_HOLD_INDICES
from scripts.selector_interface_data_v18 import MODEL,SELECTOR,view,read,read_jsonl,save,digest,verify as previous_verify
DATA=ROOT/'data/processed/selector-source-v21';OUT=ROOT/'output/diagnostics/selector-source-v21';SEED=210081

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('Source-language trial protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    review=read(MATERIAL/'source-review.json')['decisions'];oldrows=read_jsonl(MATERIAL/'legacy-english.jsonl');prior=read_jsonl(ROOT/'data/processed/tool-split-pilot-v1/selector_train.jsonl')
    refs=read_jsonl(ROOT/'data/processed/selector-interface-v18/reference.jsonl');known=set()
    for r in prior+refs:
        if r.get('tools'):known|=identities(r)
    for r in read_jsonl(MATERIAL/'legacy-candidates.jsonl'):known|=identities(r)
    def fits(r):
        v=view(r,'current_full');n=max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
        r['max_tokens']=n;return n<=512
    new=[];rejected=[]
    for r in read_jsonl(MATERIAL/'candidates.jsonl'):
        if not review[r['id']]['accept']:continue
        if identities(r)&known:rejected.append({'id':r['id'],'reason':'known_tool_or_shallow_alias'});continue
        r['task_kind']=review[r['id']]['task_kind'];r['language']='original_English';r['cohort']='source_v21'
        if fits(r):new.append(r)
    old=[]
    for i,r in enumerate(oldrows):
        if i in OLD_HOLD_INDICES:continue
        r['task_kind']='legacy_replay';r['language']='original_English';r['cohort']='source_v21'
        if fits(r):old.append(r)
    if len(old)<60 or len(new)<200:raise ValueError(('Insufficient source material',len(new),len(old)))
    components=groups(new);components.sort(key=lambda g:hashlib.sha256(('source21'+min(r['id'] for r in g)).encode()).hexdigest());test=[];pool=[]
    for g in components:
        if len(test)+len(g)<=80:test+=g
        else:pool+=g
    pool.sort(key=lambda r:hashlib.sha256(('train21'+r['id']).encode()).hexdigest());a=pool[:120];b=a[:60]+old[:60]
    if len(a)!=120 or len(test)!=80:raise ValueError('Group split shortage')
    for r in a+test+old:random.Random(SEED+int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)).shuffle(r['tools'])
    probes=[]
    for kind,rs in [('new_training',a[:60]),('legacy_training',old[:60])]:
        for r in sorted(rs,key=lambda r:hashlib.sha256(('probe21'+r['id']).encode()).hexdigest())[:24]:c=copy.deepcopy(r);c['fit_probe_kind']=kind;probes.append(c)
    sets={'new_train':a,'mixed_train':b,'fresh':test,'fit_probe':probes}
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for n,rs in sets.items():(DATA/(n+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    save(DATA/'review.json',{'new_pool_n':len(new),'legacy_pool_n':len(old),'rejected':rejected,'review':'Assistant original-query, candidate-purpose and native-call review; no independent human gold. Ordered requests preserved completely; only source-first tool selection measured.',
        'translation_gate':'Failed. No Qwen-translated field is used. Fresh80 is original English, not a Korean validation.',
        'korean_goal_status':'Fresh Korean tool generalization remains untested; the previously seen Korean reference600 measures retention only.'})
    files=list(DATA.glob('*'))+[MATERIAL/'source-review.json',MATERIAL/'exposure-audit.json',MATERIAL/'legacy-english.jsonl',MATERIAL/'candidates.jsonl']
    files += [ROOT/p for p in ['scripts/selector_source_data_v21.py','scripts/selector_source_v21.py','scripts/report_selector_source_v21.py','scripts/selector_broad_v20.py','scripts/selector_broad_data_v20.py','scripts/selector_learning_v18.py','scripts/audit_selector_source_v21.py','tests/test_selector_source_v21.py','data/processed/tool-split-pilot-v1/selector_train.jsonl']]
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'train_n':120,'test_n':80,'steps':30,'lr':1e-5,'logical_batch':4,'condition':'current_full','gradient_checkpointing':{'use_reentrant':False,'enabled':True},
        'summary':{n:{'n':len(rs),'kinds':dict(collections.Counter(r['task_kind'] for r in rs)),'candidate_counts':dict(collections.Counter(len(r['tools']) for r in rs))} for n,rs in sets.items()},
        'hypothesis':'Does broad original-language supervision improve choice on original-English held-out tools, and retain existing Korean reference performance? This does NOT test fresh Korean generalization. Same original question/schema representation and initial selector, equal examples/updates, no translation.',
        'adoption':'No deployment. Report each final arm once; English fresh strictly improves and>=72/80, no loss by fresh task kind; Korean FunctionChat>=278/400, V16>=175/200 and needed>=70/80. Passing permits more validation, not a claim of Korean80-90 percent.',
        'stop':'Both fixed final arms trained before any fresh inference; do not tune/checkpoint/prompt select on test, do not relabel test from predictions. State, reply model and demo unchanged.'})
    print('V21 FROZEN',json.dumps(read(DATA/'protocol.json')['summary'],ensure_ascii=False),flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V21 frozen file changed: '+rel)
    return p
if __name__=='__main__':prepare()
