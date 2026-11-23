import collections
import hashlib
import json
from pathlib import Path
import build_additional_24 as common

HERE=Path(__file__).resolve().parent
OUT=common.COS/'outputs/additional_200_cd_revision2'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
receipt={'mode':'development_preview','production_enabled':False,'human_review':'unreviewed','external_cross_family_gate_satisfied':False,'parts':{}}
for part in 'cd':
    pi=HERE/f'additional_200_terra_part_{part}_inputs.json'
    pa=HERE/f'additional_200_terra_part_{part}.json'
    ins=json.loads(pi.read_text(encoding='utf-8'))
    ans=json.loads(pa.read_text(encoding='utf-8'))
    assert len(ins['cases'])==len(ans['cases'])
    for x,y in zip(ins['cases'],ans['cases']):
        assert x=={k:v for k,v in y.items() if k!='answer'}
        req=common.validator.SLMRequest.model_validate(x['request'])
        row={k:y[k] for k in common.ROW_KEYS}
        row['messages']=[{'role':'system','content':common.validator.SYSTEM_PROMPT_SOLUTION_HOLD},{'role':'user','content':json.dumps(x['request'],ensure_ascii=False)},{'role':'assistant','content':y['answer']}]
        row['allowed_evidence_refs']=req.allowed_evidence_refs
        row['distractor_refs']=req.distractor_refs
        row['provenance']={'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'generator_model':'gpt-6.1-terra','critic_model':None,'critic_status':'unreviewed','human_review':'unreviewed'}
        rows.append(row)
    receipt['parts'][part]={'input_sha256':hashlib.sha256(pi.read_bytes()).hexdigest(),'answer_sha256':hashlib.sha256(pa.read_bytes()).hexdigest(),'cases':len(ins['cases']),'modes':dict(collections.Counter(x['mode'] for x in ins['cases'])),'hard_negatives':sum(x['is_hard_negative'] for x in ins['cases']),'val_rows':sum(x['split']=='val_internal' for x in ins['cases']),'val_families':len({x['scenario_family_id'] for x in ins['cases'] if x['split']=='val_internal'}),'val_groups':len({x['group_id'] for x in ins['cases'] if x['split']=='val_internal'}),'english_solution_chunks':sum(x['mode']=='solution' and any(ch['text'].isascii() for ch in x['request']['rag_chunks']) for x in ins['cases'])}
(OUT/'author_rows.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
(OUT/'author_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
