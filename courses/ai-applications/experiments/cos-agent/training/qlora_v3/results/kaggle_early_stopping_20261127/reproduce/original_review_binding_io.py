"""Review I/O only. Verdicts must be authored after actually reading each raw answer."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/kaggle_raw_review_20261127'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for v in value.values():yield from strings(v)
    elif isinstance(value,list):
        for v in value:yield from strings(v)
def show(start,end,compact=False):
    seen={}
    for path in sorted((OUT/'cases').glob('*.json')):
        case=read(path)
        if case['index']>end:continue
        if case['index']<start:
            if compact:
                for ch in case['request']['rag_chunks']:
                    seen[hashlib.sha256(json.dumps(ch,sort_keys=True,ensure_ascii=False).encode()).hexdigest()]=case['index']
            continue
        req=case['request']
        print('\nCASE',case['index'],case['row_id'],case['mode'])
        print('OBSERVATIONS',json.dumps({k:(v.get('value') if compact and v.get('state')=='known' else {'state':v.get('state'),'value':v.get('value')}) for k,v in req['confirmed_observations'].items()},ensure_ascii=False))
        for k in ['product_evidence','constraints','allowed_evidence_refs','distractor_refs']:
            if k in req:print(k,json.dumps(req[k],ensure_ascii=False))
        for chunk in req['rag_chunks']:
            digest=hashlib.sha256(json.dumps(chunk,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            if digest in seen:print('RAG_IDENTICAL_TO',seen[digest],chunk['evidence_ref'])
            else:print('RAG',json.dumps(chunk,ensure_ascii=False));seen[digest]=case['index']
        for a in case['answers']:
            print('\nMODEL',a['model'],'FINISH',a['finish_reason'])
            print(a['text'])
def bind(batch):
    notes=read(Path(batch));existing=[];path=OUT/'manual_reviews.jsonl'
    if path.exists():existing=[json.loads(l) for l in path.read_text(encoding='utf-8').splitlines()]
    keys={(r['row_id'],r['model']) for r in existing}
    by_id={read(p)['row_id']:read(p) for p in (OUT/'cases').glob('*.json')}
    new=[]
    for n in notes:
        case=by_id[n['row_id']];answers={a['model']:a for a in case['answers']};answer=answers[n['model']]
        assert (n['row_id'],n['model']) not in keys;keys.add((n['row_id'],n['model']))
        assert n['verdict'] in ['PASS','FAIL','UNCERTAIN'] and n['rationale']
        assert n.get('evidence'),'Every verdict needs an actual claim/source pair'
        source_strings=list(strings(case['request']))
        for e in n['evidence']:
            assert e['claim_quote'] and e['claim_quote'] in answer['text'],(n['row_id'],n['model'],e['claim_quote'])
            assert e['source_quote'] and any(e['source_quote'] in s for s in source_strings),(n['row_id'],e['source_quote'])
            assert e['connection']
        n.update(case_index=case['index'],mode=case['mode'],candidate_sha256=answer['content_sha256'],request_sha256=hashlib.sha256(json.dumps(case['request'],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),reviewer='Codex direct reading of raw input/evidence/output; not human approval',human_approved=False,automatic_verdict=False,raw_case_file=f'cases/{case["index"]:03d}_{case["row_id"]}.json')
        new.append(n)
    with path.open('a',encoding='utf-8',newline='\n') as f:
        for n in new:f.write(json.dumps(n,ensure_ascii=False)+'\n')
    print(json.dumps({'added':len(new),'total_reviewed':len(existing)+len(new),'target':450}))
if __name__=='__main__':
    if sys.argv[1] in ['show','compact']:show(int(sys.argv[2]),int(sys.argv[3]),sys.argv[1]=='compact')
    elif sys.argv[1]=='bind':bind(sys.argv[2])
