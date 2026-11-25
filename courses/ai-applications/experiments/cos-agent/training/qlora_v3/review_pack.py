"""Bind generated outputs to actual validation inputs; never invent review verdicts."""
import argparse,hashlib,json
from pathlib import Path
from common import read_rows
COS=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--predictions',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    source=COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl';rows={r['id']:r for r in read_rows(source)}
    preds=read_rows(a.predictions);assert len(preds)==90 and len({p['row_id'] for p in preds})==90
    output=Path(a.output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf-8',newline='\n') as f:
        for pred in preds:
            row=rows[pred['row_id']];assert row['split']=='val_internal'
            record={'row_id':row['id'],'dataset_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'request':json.loads(row['messages'][1]['content']),'teacher_answer':row['messages'][2]['content'],
                'candidate':pred['text'],'candidate_sha256':hashlib.sha256(pred['text'].encode()).hexdigest(),
                'automatic_candidates':pred['metrics'],'review_status':'unreviewed',
                'rubric':['unsupported citations','indirect distractor topic leakage','hold instruction leakage',
                          'unsupported factual claims or loss of unknown','clinical/diagnostic assertion']}
            f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps({'rows':90,'status':'review_requested_not_PASS'}))
if __name__=='__main__':main()
