"""Broader fixed training after fit-only checks; new20 primary, prior tests references."""
import copy,hashlib,json,random,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_fit_data_v23 import verify as previous_verify
from scripts.selector_korean_data_v22 import DATA as V22,SOURCE,MATERIAL,MODEL,SELECTOR,read,read_jsonl,save,digest,identities,groups,view
DATA=ROOT/'data/processed/selector-transfer-v24';OUT=ROOT/'output/diagnostics/selector-transfer-v24';SEED=240020
TRAIN_HOLDS={'toolace:7804:turn1':'Responsive design versus Korean website response mismatch; original responsive ambiguous.'}
REPLAY_HOLDS={'when2call_pref:5393':'Tool explicitly simulates a query; source asks for actual orders. Execution capability mismatch unresolved.', 'toolace:7128:turn1':'Dental cleaning versus specifically surgical procedure scope not established by descriptions; held rather than assuming equivalence.'}
FRESH_HOLDS={'toolace:8197:turn1':'Meaning of surgical medical fixtures insufficiently clear for confident Korean wording; held before scoring.'}

def translation_flags(source,korean):
    import re
    from scripts.review_korean_material_v22 import flags
    fs=flags(source,korean)
    # English text deliberately quoted for translation/sentiment is data, not an
    # outer condition that must itself be translated. Literal equality still checked.
    outer=re.sub(r'"[^"\n]*"','',source)
    if not re.search(r'\bif\b',outer,re.I):fs=[x for x in fs if x!='condition_unverified']
    return fs

def select():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V24 protected')
    a=read_jsonl(V22/'new_train.jsonl');old=[r for r in read_jsonl(V22/'mixed_train.jsonl') if r['task_kind']=='legacy_replay']
    # All80+40 full utterance pairs and every candidate purpose reread, not just samples.
    a=[r for r in a if r['id'] not in TRAIN_HOLDS][:76];old=[r for r in old if r['id'] not in REPLAY_HOLDS][:38]
    if len(a)!=76 or len(old)!=38:raise ValueError('Reviewed material shortage')
    known=set()
    prior=read_jsonl(SOURCE/'new_train.jsonl')+read_jsonl(SOURCE/'mixed_train.jsonl')+read_jsonl(SOURCE/'fresh.jsonl')+read_jsonl(V22/'fresh.jsonl')
    for r in prior:known|=identities(r)
    rv=read(MATERIAL/'source-review.json')['decisions'];pool=[r for r in read_jsonl(MATERIAL/'candidates.jsonl') if rv[r['id']]['accept'] and not identities(r)&known]
    pool=[r for r in pool if r['id'] not in FRESH_HOLDS];pool.sort(key=lambda r:hashlib.sha256(('fresh24'+r['id']).encode()).hexdigest());fresh=pool[:20]
    if len(fresh)!=20 or len(groups(fresh))!=20:raise ValueError('Not20 separated source groups')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    save(DATA/'selection.json',{'new':a,'legacy':old,'fresh':fresh})
    save(DATA/'review.json',{'reviewer':'assistant; not independent human gold','scope':'Reread original and Korean requests + every candidate purpose for all80 new and40 replay source rows; all24 remaining unscored source requests/candidate purposes read. Source labels not rewritten.',
        'train_holds':TRAIN_HOLDS,'replay_holds':REPLAY_HOLDS,'fresh_holds':FRESH_HOLDS,'budget':'Use76 of79 retained new rows in existing fixed order;38new+38old as replay arm. Remaining3 new not promoted into evaluation.',
        'labels':'Source preferred first calls + assistant review. Not complete equivalence gold or real execution. Full schema retained; only capability selection scored.'})
    save(DATA/'plan.json',{'seed':SEED,'selection_sha256':digest(DATA/'selection.json'),'train_n':76,'test_n':20,'epochs':10,'logical_batch':4,'steps':190,'lr':1e-4,'checkpoint_epochs':[0,1,10],
        'hypothesis':'After a train-only fit diagnostic, does stronger fixed learning on broader reviewed Korean requests improve choice on20 previously unscored tool groups while retaining prior selection?',
        'arms':'Original SELECTOR independently for new76 vs sharednew38+reviewedold38. Same total760 exposures,190updates,lr1e-4,question,current_full JSON, NF4 FP16 q/v LoRA only. Do not start from15-row V23 overfit adapter.',
        'scope':'Korean user utterances, complete English source tool definitions unchanged. All examples have a corresponding source preferred tool. No rejection/argument/execution/state/response test.',
        'evaluation':'Both final arms complete before scoring new20 Korean, parallelEnglish20, previously seen V22 Korean40 and older Korean reference600. Only new20 is primary previously-unscored evaluation.20 is exploratory, not population90 proof.',
        'guards':'New20 strictly better than original baseline and>=18/20; no drop by new task kind; previous40>=baseline25; FunctionChat>=278/400,V16>=175/200,needed>=70/80. No deployment regardless; report once and stop.',
        'quality':'Assistant source/Korean/candidate-purpose review; quoted data and names preserved. Ambiguous correspondence held, not target-driven rewritten. Any >512 input stops freeze; no truncation.',
        'stop':'Fixed final10 epochs, no checkpoint selection or another round from validation/test scores. No data relabel based on model predictions. No production/demo changes.'})
    print('SELECTED new76 replay38 fresh20',flush=True)

def freeze():
    previous_verify();plan=read(DATA/'plan.json')
    if (DATA/'protocol.json').exists():raise FileExistsError('Frozen')
    if digest(DATA/'selection.json')!=plan['selection_sha256']:raise ValueError('Selection changed')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    ss=read(DATA/'selection.json');tr=read(DATA/'fresh-translations.json');ids={r['id'] for r in ss['fresh']}
    if set(tr)!=ids:raise ValueError('Translation coverage')
    new=[];english=[];review={}
    for original in ss['fresh']:
        r=copy.deepcopy(original);r['cohort']='korean_v22';r['task_kind']=read(MATERIAL/'source-review.json')['decisions'][r['id']]['task_kind'];r['language']='Korean_utterance_English_tools';r['original_messages']=copy.deepcopy(r['messages']);r['original_tools']=copy.deepcopy(r['tools'])
        if len(r['messages'])!=1 or r['messages'][0]['role']!='user':raise ValueError('Unexpected prefix')
        text=tr[r['id']];fs=translation_flags(r['messages'][0]['content'],text)
        if fs:raise ValueError((r['id'],fs))
        r['messages'][0]['content']=text;random.Random(SEED+int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)).shuffle(r['tools']);v=view(r,'current_full')
        n=max(map(len,tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
        if n>512:raise ValueError(('Cannot truncate',r['id'],n))
        r['max_tokens']=n;new.append(r);e=copy.deepcopy(r);e['messages']=copy.deepcopy(r['original_messages']);e['language']='original_English';english.append(e)
        review[r['id']]={'accepted_by_assistant':True,'full_source_Korean_and_candidate_purposes_checked':True,'max_tokens':n,'translation_sha256':hashlib.sha256(text.encode()).hexdigest()}
    sets={'new_train':ss['new'],'mixed_train':ss['new'][:38]+ss['legacy'],'fresh':new,'fresh_english':english}
    for name,rs in sets.items():(DATA/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    save(DATA/'language-review.json',{'reviewer':'assistant who authored translation, not independent human review','rows':review,'no_model_inference_used':True,'English_tool_definitions_unchanged':True})
    files=list(DATA.glob('*'))+[ROOT/p for p in ['scripts/selector_transfer_data_v24.py','scripts/selector_transfer_v24.py','scripts/report_selector_transfer_v24.py','scripts/audit_selector_transfer_v24.py','tests/test_selector_transfer_v24.py','scripts/selector_learning_v18.py','scripts/selector_broad_v20.py']]
    save(DATA/'protocol.json',{**plan,'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'summary':{name:{'n':len(rs),'kinds':dict(collections.Counter(r['task_kind'] for r in rs)),'max_tokens':max(r['max_tokens'] for r in rs)} for name,rs in sets.items()}})
    print('V24 FROZEN',read(DATA/'protocol.json')['summary'],flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V24 frozen file changed: '+rel)
    return p
if __name__=='__main__':select() if sys.argv[1]=='select' else freeze()
