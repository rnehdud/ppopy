"""Korean utterances, unmodified source tool definitions; fixed small comparison."""
import copy,hashlib,json,random,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_source_data_v21 import verify as previous_verify,read,read_jsonl,save,digest,identities,groups,view,MODEL,SELECTOR,MATERIAL
SOURCE=ROOT/'data/processed/selector-source-v21';DATA=ROOT/'data/processed/selector-korean-v22';OUT=ROOT/'output/diagnostics/selector-korean-v22';SEED=220040

def select():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V22 material protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    a=read_jsonl(SOURCE/'new_train.jsonl');ids={r['id'] for r in a};old=[r for r in read_jsonl(SOURCE/'mixed_train.jsonl') if r['id'] not in ids];seen=set()
    for r in a+old+read_jsonl(SOURCE/'fresh.jsonl'):seen|=identities(r)
    rv=read(MATERIAL/'source-review.json')['decisions']
    fresh=[r for r in read_jsonl(MATERIAL/'candidates.jsonl') if rv[r['id']]['accept'] and not identities(r)&seen]
    def fit(r):
        r=copy.deepcopy(r);r['cohort']='korean_v22';v=view(r,'current_full')
        n=max(map(len,tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
        return n<=420
    def order(rs,prefix):return sorted([r for r in rs if fit(r)],key=lambda r:hashlib.sha256((prefix+r['id']).encode()).hexdigest())
    a=order(a,'train22')[:80];old=order(old,'replay22')[:40];fresh=order(fresh,'fresh22')[:40]
    if (len(a),len(old),len(fresh))!=(80,40,40):raise ValueError(('Insufficient source rows',len(a),len(old),len(fresh)))
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    selection={'new':a,'legacy':old,'fresh':fresh}
    save(DATA/'selection.json',selection)
    save(DATA/'plan.json',{'selection_sha256':digest(DATA/'selection.json'),'seed':SEED,'train_n':80,'test_n':40,'steps':20,'lr':1e-5,'logical_batch':4,'max_tokens':512,'english_prefilter':420,
        'question_and_tools':'Original current_full question; complete tool definitions unchanged English. Only user-message text becomes Korean. No summary, source-response or label in input.',
        'evaluation':'Korean40 as main held-out input, same original-English40 as language control, existing Korean reference600 as retention. Fresh source and all candidate identity groups excluded from both V21 training and V21 scoring. No claim of base-pretraining absence.',
        'learning':'Start original SELECTOR, not V21 weights. New80 vs common40new+40actualold. Both fixed final arms completed before any V22 inference. One epoch,20 updates, same seed, NF4 FP16 LoRA query/value. No post-test tuning.',
        'quality':'Assistant translates the full original utterance without seeing targets in the translation worksheet, then checks request/actor/object/order/conditions/negation/names/numbers against source. Tools/schemas untouched bytewise structurally. Not independently human-verified. No V20 machine-translated cache reused.',
        'gate':'Any meaning failure or >512 input prevents freeze/training; do not silently truncate. Baseline raw reference replay matches prior. Both final arms >=36/40 and strictly above baseline; no loss by task kind; FunctionChat>=278/400, V16>=175/200, needed>=70/80. No deployment even on pass; further validation required.',
        'stop':'Finish fixed comparison once; do not move evaluation rows into training or choose checkpoint/prompt from scores. State, execution, argument checks and response model unchanged.'})
    # Deliberately omit labels, expected calls, source responses and tool descriptions.
    with (DATA/'translation-worksheet.jsonl').open('w',encoding='utf8') as f:
        for split,rs in selection.items():
            for r in rs:f.write(json.dumps({'id':r['id'],'split':split,'source':r['messages'][-1]['content']},ensure_ascii=False)+'\n')
    print('SELECTED', {k:len(v) for k,v in selection.items()},flush=True)

def freeze():
    previous_verify();plan=read(DATA/'plan.json')
    if digest(DATA/'selection.json')!=plan['selection_sha256']:raise ValueError('Selection changed')
    if (DATA/'protocol.json').exists():raise FileExistsError('Already frozen')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    src=read(DATA/'selection.json');translations=read(DATA/'translations.json');review=read(DATA/'language-review.json');expected_ids={r['id'] for rs in src.values() for r in rs}
    if set(translations)!=expected_ids or set(review['rows'])!=expected_ids:raise ValueError('Incomplete translation/review')
    if review['translation_sha256']!=digest(DATA/'translations.json') or not all(x['accepted'] for x in review['rows'].values()):raise ValueError('Language review stale or held')
    rows={};english=[]
    for split,rs in src.items():
        rows[split]=[]
        for original in rs:
            r=copy.deepcopy(original);r['cohort']='korean_v22';r['language']='Korean_utterance_English_tools';r['original_messages']=copy.deepcopy(r['messages']);r['original_tools']=copy.deepcopy(r['tools']);r['messages'][-1]['content']=translations[r['id']]
            if any(m['role']!='user' for m in r['messages']) or len(r['messages'])!=1:raise ValueError('Unexpected prefix: no silent partial translation')
            if r['tools']!=original['tools'] or r['expected']!=original['expected']:raise ValueError('Tools or labels changed')
            if not any('\uac00'<=c<='\ud7a3' for c in translations[r['id']]):raise ValueError('Korean missing')
            r['task_kind']=read(MATERIAL/'source-review.json')['decisions'][r['id']]['task_kind'] if split!='legacy' else 'legacy_replay'
            random.Random(SEED+int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)).shuffle(r['tools'])
            v=view(r,'current_full');n=max(map(len,tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
            if n>512:raise ValueError(('Korean would truncate',r['id'],n))
            r['max_tokens']=n;rows[split].append(r)
            if split=='fresh':e=copy.deepcopy(r);e['messages']=copy.deepcopy(r['original_messages']);e['language']='original_English';english.append(e)
    sets={'new_train':rows['new'],'mixed_train':rows['new'][:40]+rows['legacy'],'fresh':rows['fresh'],'fresh_english':english}
    probes=[]
    for kind,rs in [('new_training',rows['new'][:40]),('legacy_training',rows['legacy'])]:
        for r in sorted(rs,key=lambda r:hashlib.sha256(('fit22'+r['id']).encode()).hexdigest())[:16]:c=copy.deepcopy(r);c['fit_probe_kind']=kind;probes.append(c)
    sets['fit_probe']=probes
    for name,rs in sets.items():(DATA/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    files=list(DATA.glob('*'))+[ROOT/p for p in ['scripts/selector_korean_data_v22.py','scripts/selector_korean_v22.py','scripts/report_selector_korean_v22.py','scripts/audit_selector_korean_v22.py','scripts/review_korean_material_v22.py','tests/test_selector_korean_v22.py','scripts/selector_broad_v20.py','scripts/selector_learning_v18.py']]
    save(DATA/'protocol.json',{**plan,'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'summary':{k:{'n':len(rs),'kind':dict(collections.Counter(r['task_kind'] for r in rs)),'max_tokens':max(r['max_tokens'] for r in rs)} for k,rs in sets.items()}})
    print('V22 FROZEN',read(DATA/'protocol.json')['summary'],flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V22 frozen file changed: '+rel)
    return p
if __name__=='__main__':select() if sys.argv[1]=='select' else freeze()
