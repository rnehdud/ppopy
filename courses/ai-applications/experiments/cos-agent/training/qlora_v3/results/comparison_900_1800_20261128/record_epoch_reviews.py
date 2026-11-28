"""Bind authored per-epoch notes to actual raw hashes; no automatic semantic rating."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
OUT=H/'epochs_1_3';OUT.mkdir(exist_ok=True)
P={p['row_id']:p for p in json.loads((H/'common_90_raw_pairs.json').read_text(encoding='utf-8'))}
file=OUT/'review_1800_epochs_1_3.json'
if file.exists(): reviews=json.loads(file.read_text(encoding='utf-8'))
else:
    prior=json.loads((H/'extended_review_60.json').read_text(encoding='utf-8'))
    reviews=[{'row_id':n['row_id'],'epoch':3,'rating':n['new_rating'],'answer_quotes':n['new_quotes'],
              'input_quotes':n['input_quotes'],'reason':n['reason'],
              'answer_sha256':n['new_answer_sha256'],'input_sha256':n['input_sha256'],
              'review_origin':'Exact-content review preserved from extended_review_60.json; reason includes prior 900 comparison',
              'reviewer':n['reviewer'],'human_approved':False} for n in prior]
seen={(n['row_id'],n['epoch']) for n in reviews}
notes=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for entry in notes:
    rid=entry['row_id'];p=P[rid];assert p['exact_messages_equal']
    source=p['input_messages_1800'][1]['content']
    assert all(q in source for q in entry['input_quotes'])
    for epoch in [1,2]:
        n=entry[str(epoch)];raw=p['new_all_epochs'][str(epoch)]
        assert (rid,epoch) not in seen
        assert raw['input_messages']==p['input_messages_1800']
        assert n['rating'] in ['PASS','WARN','FAIL']
        assert all(q in raw['text'] for q in n['quotes']),(rid,epoch,n['quotes'])
        assert hashlib.sha256(raw['text'].encode()).hexdigest()==raw['content_sha256']
        reviews.append({'row_id':rid,'epoch':epoch,'rating':n['rating'],'answer_quotes':n['quotes'],
              'input_quotes':entry['input_quotes'],'reason':n['reason'],
              'answer_sha256':raw['content_sha256'],'input_sha256':hashlib.sha256(source.encode()).hexdigest(),
              'review_origin':'Direct reading of saved Kaggle raw output and original input',
              'reviewer':'Codex single reviewer; not independent cross-model or human approval','human_approved':False})
        seen.add((rid,epoch))
file.write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Bound newly authored',len(notes)*2,'epoch reviews; total including preserved E3:',len(reviews))
