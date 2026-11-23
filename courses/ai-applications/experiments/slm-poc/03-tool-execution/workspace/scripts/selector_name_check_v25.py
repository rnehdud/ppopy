"""Read-only metadata diagnostic on known TRAINING rows, not new validation."""
import copy,gc,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_transfer_data_v24 import verify as previous_verify,OUT as V24,read,read_jsonl,save,digest,SELECTOR,MODEL,view
from scripts.selector_broad_v20 import score
from scripts.selector_learning_v18 import load
DATA=ROOT/'data/processed/selector-name-check-v25';OUT=ROOT/'output/diagnostics/selector-name-check-v25'
CONDITIONS=['original','masked_1','rotated_1','masked_2','rotated_2']
ADAPTERS={'baseline':SELECTOR,'new':V24/'new/final-adapter','mixed':V24/'mixed/final-adapter'}

def transform(source,condition):
    r=copy.deepcopy(source);r['source_id']=source['id'];r['id']=source['id']+'|'+condition;r['diagnostic_condition']=condition
    if condition=='original':r['canonical_map']={t['name']:t['name'] for t in r['tools']};return r
    mode,seed=condition.split('_');tools=source['tools'];n=len(tools)
    if n<2:raise ValueError('Need alternatives')
    ids=['fn_'+hashlib.sha256(('v25|'+seed+'|'+source['id']+'|'+str(i)).encode()).hexdigest()[:10] for i in range(n)]
    new=[];canonical={}
    for i in range(n):
        semantic=(i+1)%n if mode=='rotated' else i;t=copy.deepcopy(tools[semantic]);canonical[ids[i]]=t['name'];t['name']=ids[i];new.append(t)
    r['tools']=new;r['canonical_map']=canonical;r['expected']=[k for k,v in canonical.items() if v in source['expected']]
    if len(r['expected'])!=1 or len(set(ids))!=n:raise ValueError('Bad mapping')
    return r

def without_name(tool):return {k:v for k,v in tool.items() if k!='name'}

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V25 protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    rows=read_jsonl(ROOT/'data/processed/selector-fit-v23/train.jsonl');screen=[]
    for r in rows:
        specification_text=json.dumps([without_name(t) for t in r['tools']],ensure_ascii=False)
        for t in r['tools']:
            name=t['name']
            if name in r['messages'][-1]['content'] or name in specification_text:screen.append({'id':r['id'],'name':name,'reason':'identifier also supplies context/reference; manual hold needed'})
    if len(rows)!=15 or screen:raise ValueError(('Do not mask referenced identifiers without review',screen))
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);sets={};lengths={}
    for condition in CONDITIONS:
        rs=[transform(r,condition) for r in rows]
        for r in rs:
            v=view(r,'current_full');n=max(map(len,tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
            if n>512:raise ValueError(('No truncation',r['id'],n))
            r['max_tokens']=n;lengths[r['id']]=n
        sets[condition]=rs;(DATA/(condition+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    paths=list(DATA.glob('*'))+[ROOT/'scripts/selector_name_check_v25.py',ROOT/'tests/test_selector_name_check_v25.py',ROOT/'data/processed/selector-fit-v23/train.jsonl']
    for p in ADAPTERS.values():paths.extend([p/'adapter_model.safetensors',p/'adapter_config.json'])
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'source_n':15,'conditions':CONDITIONS,'seeds':2,'max_tokens':max(lengths.values()),
        'purpose':'Is name-only masking sufficient to disturb learned choice? Do predictions track complete capability blocks when anonymous IDs stay in fixed slots but full descriptions+schemas move?',
        'material_review':'Same15 V23 reviewed training rows. Candidate purposes sufficient to distinguish preferred work without name labels. Original7804 mismatch already excluded. No identifier references in requests or own specifications. Assistant review, not independent gold.',
        'controls':'Question,current_full format,utterance,parameter names/types/defaults/descriptions remain unchanged. Name-only masks for2 fixed hash seeds. Rotation moves COMPLETE description+schema blocks between fixed opaque IDs, updates expected mapping, preserves candidate order of IDs; does not swap descriptions while leaving incompatible schemas.',
        'limits':'TRAINING-ONLY diagnostic.15 examples with5 variants are NOT75 independent validation examples. Does not prove descriptions alone matter because parameter fields are retained. Changing name tokens also changes tokenization/positions. No general unseen-tool accuracy or causal explanation of V24 test failures.',
        'stop':'Score original selector and bothV24 final adapters once. No training, no optimizer, no replacement of demo weights, no fresh20 or previous40/600 model scoring. No prompt/checkpoint selection.',
        'refs':['https://arxiv.org/html/2410.04587','https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html','https://aclanthology.org/2024.lrec-main.1413/']})
    print('V25 FROZEN:15 known training rows,5 variants,3 adapters; read-only',flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V25 frozen file changed:'+rel)
    return p

def run():
    cfg=verify()
    if (OUT/'started.json').exists():raise FileExistsError('Scoring protected')
    save(OUT/'started.json',{'protocol_sha256':digest(DATA/'protocol.json')})
    import torch
    for arm,path in ADAPTERS.items():
        s=load(adapter=path)
        for condition in CONDITIONS:
            rows=read_jsonl(DATA/(condition+'.jsonl'));p=score(s,rows,arm+' '+condition)
            for r in rows:p[r['id']]['canonical_predicted']=r['canonical_map'][p[r['id']]['predicted']]
            save(OUT/(arm+'-'+condition+'.json'),p);print(arm,condition,sum(v['correct'] for v in p.values()),'/15',flush=True)
            if condition=='original':
                old=read(ROOT/'output/diagnostics/selector-korean-v22/baseline-fit-probe.json') if arm=='baseline' else read(V24/arm/'own-epoch-10-scores.json')
                err=max(abs(v['scores'][k]-old[r['source_id']]['scores'][k]) for r in rows for v in [p[r['id']]] for k in v['scores']);changes=[r['source_id'] for r in rows if p[r['id']]['predicted']!=old[r['source_id']]['predicted']]
                save(OUT/(arm+'-replay.json'),{'max_logit_error':err,'changes':changes})
                if err>.05 or changes:raise ValueError('Named-input baseline failed to replay')
        del s;gc.collect();torch.cuda.empty_cache()
    verify();save(OUT/'complete.json',{'no_training':True,'no_deployment':True});report()

def report():
    verify();read(OUT/'complete.json');summary={};checks={};cases=[]
    source=read_jsonl(DATA/'original.jsonl');by_source={r['source_id']:r for r in source}
    for arm in ADAPTERS:
        named=read(OUT/(arm+'-original.json'));baseline={r['source_id']:named[r['id']]['canonical_predicted'] for r in source};summary[arm]={}
        for condition in CONDITIONS:
            rows=read_jsonl(DATA/(condition+'.jsonl'));p=read(OUT/(arm+'-'+condition+'.json'));summary[arm][condition]={'n':len(rows),'correct':sum(v['correct'] for v in p.values()),'canonical_choice_changed':[r['source_id'] for r in rows if p[r['id']]['canonical_predicted']!=baseline[r['source_id']]]}
            checks[arm+'_'+condition]=set(p)=={r['id'] for r in rows} and all(p[r['id']]['correct']==(p[r['id']]['predicted'] in r['expected']) and p[r['id']]['canonical_predicted'] in {t['name'] for t in by_source[r['source_id']]['tools']} and all(__import__('math').isfinite(v) for v in p[r['id']]['scores'].values()) for r in rows)
            for r in rows:
                if condition!='original' and p[r['id']]['canonical_predicted']!=baseline[r['source_id']]:cases.append({'arm':arm,'condition':condition,'id':r['source_id'],'request':r['messages'][-1]['content'],'source_preferred':by_source[r['source_id']]['expected'],'original_choice':baseline[r['source_id']],'changed_to':p[r['id']]['canonical_predicted'],'correct':p[r['id']]['correct']})
        for seed in ['1','2']:
            masked=read(OUT/(arm+'-masked_'+seed+'.json'));rot=read(OUT/(arm+'-rotated_'+seed+'.json'));mr=read_jsonl(DATA/('masked_'+seed+'.jsonl'));rr=read_jsonl(DATA/('rotated_'+seed+'.jsonl'))
            summary[arm]['spec_following_seed'+seed]={'n':15,'canonical_choice_stable':sum(masked[a['id']]['canonical_predicted']==rot[b['id']]['canonical_predicted'] for a,b in zip(mr,rr))}
        replay=read(OUT/(arm+'-replay.json'));checks[arm+'_replay']=replay['max_logit_error']<=.05 and not replay['changes']
    for c in CONDITIONS[1:]:
        rs=read_jsonl(DATA/(c+'.jsonl'));checks[c+'_specs_preserved']=all(sorted([json.dumps(without_name(t),sort_keys=True) for t in r['tools']])==sorted([json.dumps(without_name(t),sort_keys=True) for t in by_source[r['source_id']]['tools']]) for r in rs)
    save(OUT/'results.json',{'conditions':summary,'scope':read(DATA/'protocol.json')['limits']});save(OUT/'changed-cases.json',cases);save(OUT/'audit.json',{'checks':checks,'passed':sum(checks.values()),'n':len(checks),'all_passed':all(checks.values())})
    if not all(checks.values()):raise ValueError('Diagnostic audit failed')
    print(json.dumps(summary,ensure_ascii=False,indent=2));print('AUDIT',sum(checks.values()),'/',len(checks),flush=True)
if __name__=='__main__':
    {'prepare':prepare,'run':run,'report':report}[sys.argv[1]]()
