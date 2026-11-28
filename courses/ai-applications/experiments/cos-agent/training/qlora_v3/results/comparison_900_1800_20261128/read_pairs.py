"""Read saved evidence and actual answers; never generates semantic verdicts."""
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
pairs=json.loads((HERE/'common_90_raw_pairs.json').read_text(encoding='utf-8'))
pairs=[p for p in pairs if p['exact_messages_equal']]
start=int(sys.argv[1]);end=int(sys.argv[2])
selected=pairs[start:end]
refs={c['evidence_ref']:c for p in selected for c in json.loads(p['input_messages_1800'][1]['content'])['rag_chunks']}
print('SHARED LITERATURE, VERBATIM')
for ref,chunk in refs.items(): print(json.dumps(chunk,ensure_ascii=False))
for i,p in enumerate(selected,start):
    user=json.loads(p['input_messages_1800'][1]['content'])
    obs={k:{key:v[key] for key in ['state','value','confirmed_by_user'] if key in v} for k,v in user['confirmed_observations'].items()}
    print('\nINDEX',i,'ID',p['row_id'])
    print('OBSERVATIONS (selected fields, original values)',json.dumps(obs,ensure_ascii=False))
    print('PRODUCT_EVIDENCE',json.dumps(user['product_evidence'],ensure_ascii=False))
    print('ALLOWED',user['allowed_evidence_refs'],'DISTRACTOR',user['distractor_refs'])
    print('900 E2 RAW\n'+p['answer_900_epoch2']['text'])
    print('1800 E3 RAW\n'+p['answer_1800_epoch3']['text'])
