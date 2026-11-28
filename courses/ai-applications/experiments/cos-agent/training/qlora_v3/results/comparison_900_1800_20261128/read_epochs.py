"""Print real Epoch 1/2 outputs and their identical input; no semantic scoring."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
pairs=[p for p in json.loads((H/'common_90_raw_pairs.json').read_text(encoding='utf-8')) if p['exact_messages_equal']]
start,end=map(int,sys.argv[1:3])
refs={c['evidence_ref']:c for p in pairs[start:end] for c in json.loads(p['input_messages_1800'][1]['content'])['rag_chunks']}
for c in refs.values():print('LITERATURE',json.dumps(c,ensure_ascii=False))
for i,p in enumerate(pairs[start:end],start):
    request=json.loads(p['input_messages_1800'][1]['content'])
    print('\nINDEX',i,p['row_id'])
    print('OBS',json.dumps({k:{'state':v['state'],'value':v['value']} for k,v in request['confirmed_observations'].items()},ensure_ascii=False))
    print('PRODUCT',json.dumps(request['product_evidence'],ensure_ascii=False))
    print('ALLOWED',request['allowed_evidence_refs'],'DISTRACTOR',request['distractor_refs'])
    for e in [1,2]:
        r=p['new_all_epochs'][str(e)]
        assert r['input_messages']==p['input_messages_1800']
        print('EPOCH',e,'RAW\n'+r['text'])
