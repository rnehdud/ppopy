"""Verify saved audit integrity, not semantic correctness. Standard library only."""
import hashlib,json
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
hashes=read(H/'file_sha256.json')
for rel,expected in hashes.items():
    assert hashlib.sha256((H/rel).read_bytes()).hexdigest()==expected,rel
assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file() and p.name!='file_sha256.json'}==set(hashes)
pairs={p['row_id']:p for p in read(H/'common_90_raw_pairs.json')}
notes=read(H/'epochs_1_3/review_1800_epochs_1_3.json')
prior=read(H/'extended_review_60.json')
assert len(notes)==180 and len(prior)==60
assert len({(n['row_id'],n['epoch']) for n in notes})==180
for n in notes:
    p=pairs[n['row_id']];raw=p['new_all_epochs'][str(n['epoch'])]
    assert p['exact_messages_equal'] and raw['input_messages']==p['input_messages_1800']
    assert hashlib.sha256(raw['text'].encode()).hexdigest()==raw['content_sha256']==n['answer_sha256']
    assert all(q in raw['text'] for q in n['answer_quotes'])
    assert all(q in p['input_messages_1800'][1]['content'] for q in n['input_quotes'])
    assert n['human_approved'] is False
for n in prior:
    p=pairs[n['row_id']];raw=p['answer_900_epoch2']
    assert hashlib.sha256(raw['text'].encode()).hexdigest()==n['old_answer_sha256']
    assert all(q in raw['text'] for q in n['old_quotes'])
expected=[{'PASS':24,'WARN':24,'FAIL':12},{'PASS':19,'WARN':24,'FAIL':17},{'PASS':18,'WARN':29,'FAIL':13}]
counts=[dict(Counter(n['rating'] for n in notes if n['epoch']==e)) for e in (1,2,3)]
assert counts==expected
assert dict(Counter(n['old_rating'] for n in prior))=={'PASS':29,'WARN':14,'FAIL':17}
print(json.dumps({'files_hashed':len(hashes),'review_cases':60,'answer_hashes_checked':240,'counts_1800':counts,'passed':True},ensure_ascii=False))
