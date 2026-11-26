"""Bind explicitly written Codex reading notes to immutable raw response hashes.

No model judging or inferred PASS: every verdict must already be in the notes.
"""
import argparse,json,hashlib
from pathlib import Path
from common import read_rows,dump

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();root=Path(a.run)
    packs={tag:{r['row_id']:r for r in read_rows(root/(tag+'_review_request.jsonl'))} for tag in ['base','epoch-1','epoch-2']}
    notes=read_rows(root/'manual_review_notes.jsonl');seen=set();records=[]
    for note in notes:
        key=(note['tag'],note['row_id']);assert key not in seen;seen.add(key)
        source=packs[note['tag']][note['row_id']];candidate=source['candidate']
        assert hashlib.sha256(candidate.encode()).hexdigest()==source['candidate_sha256']
        assert note['verdict'] in {'PASS','FAIL','UNCERTAIN'}
        for e in note['evidence']:
            assert e['candidate_quote'] in candidate,(key,'candidate quote mismatch')
            assert e['basis_quote'] in json.dumps(source['request'],ensure_ascii=False),(key,'request basis mismatch')
        records.append({**note,'candidate_sha256':source['candidate_sha256'],
            'dataset_sha256':source['dataset_sha256'],'raw_request':source['request'],'raw_candidate':candidate,
            'reviewer':'Codex content reading; not human approval','human_approved':False,
            'rubric_scope':'source-grounded citations, factual/instruction fidelity, indirect distractor topics, HOLD restraint, nonclinical safety'})
    with (root/'semantic_review.jsonl').open('w',encoding='utf-8',newline='\n') as f:
        for row in records:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    counts={}
    for tag in packs:
        subset=[r for r in records if r['tag']==tag]
        counts[tag]={'reviewed':len(subset),'pending':90-len(subset),
            **{v.lower():sum(r['verdict']==v for r in subset) if subset else None for v in ['PASS','FAIL','UNCERTAIN']}}
    summary={'reviewed_model_responses':len(records),'target_model_responses':270,
        'distinct_cases_reviewed':len({r['row_id'] for r in records}),'target_distinct_cases':90,
        'by_model':counts,'review_complete':len(records)==270,'human_approved':False,
        'notes':'Partial findings are not population error rates. Automatic PASS, Codex reading and human approval are distinct.'}
    dump(root/'semantic_review_summary.json',summary);print(json.dumps(summary))

if __name__=='__main__':main()
