"""Validate and bind authored direct-reading notes; does not assign semantic ratings."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
P={r['row_id']:r for r in json.loads((H/'common_90_raw_pairs.json').read_text(encoding='utf-8'))}
target=H/'extended_review_60.json'
reviews=json.loads(target.read_text(encoding='utf-8')) if target.exists() else []
seen={r['row_id'] for r in reviews}
notes=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for n in notes:
    p=P[n['row_id']];assert p['exact_messages_equal'] and n['row_id'] not in seen
    a=p['answer_900_epoch2'];b=p['answer_1800_epoch3']
    for q in n['old_quotes']:assert q in a['text'],(n['row_id'],'old quote',q)
    for q in n['new_quotes']:assert q in b['text'],(n['row_id'],'new quote',q)
    raw=p['input_messages_1800'][1]['content']
    for q in n['input_quotes']:assert q in raw,(n['row_id'],'input quote',q)
    assert n['old_rating'] in ['PASS','WARN','FAIL'] and n['new_rating'] in ['PASS','WARN','FAIL']
    assert n['comparison'] in ['improvement','regression','unchanged','mixed']
    n.update({'old_answer_sha256':a['content_sha256'],'new_answer_sha256':b['content_sha256'],
              'input_sha256':hashlib.sha256(raw.encode()).hexdigest(),
              'reviewer':'Codex direct reading; single reviewer, not independent cross-model audit',
              'human_approved':False})
    reviews.append(n);seen.add(n['row_id'])
target.write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Recorded',len(notes),'directly authored notes; total',len(reviews))
