"""Render human-readable evidence from authored judgments, never assign judgments."""
import csv, hashlib, html, json
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent
D=H/'epochs_1_3'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
notes=read(D/'review_1800_epochs_1_3.json')
pairs={p['row_id']:p for p in read(H/'common_90_raw_pairs.json')}
ids=sorted({n['row_id'] for n in notes})
assert len(ids)==60 and len(notes)==180
index={(n['row_id'],n['epoch']):n for n in notes}
assert len(index)==180
for rid in ids:
    p=pairs[rid]
    assert p['exact_messages_equal']
    for e in (1,2,3):
        n=index[rid,e];raw=p['new_all_epochs'][str(e)]
        assert raw['input_messages']==p['input_messages_1800']
        assert hashlib.sha256(raw['text'].encode()).hexdigest()==n['answer_sha256']==raw['content_sha256']
        assert all(q in raw['text'] for q in n['answer_quotes'])
        assert all(q in p['input_messages_1800'][1]['content'] for q in n['input_quotes'])
loss=[1.0537188550960817,.9893467762190546,.9877520854747801]
counts={str(e):dict(Counter(index[r,e]['rating'] for r in ids)) for e in (1,2,3)}
transitions={f'{a}_to_{b}':dict(Counter(index[r,a]['rating']+' → '+index[r,b]['rating'] for r in ids)) for a,b in [(1,2),(2,3),(1,3)]}
summary={'scope':'Same 60 exact-input cases from 1800 run; 180 answers; not all validation cases',
 'new_direct_reviews':120,'preserved_exact_content_epoch3_reviews':60,'counts':counts,'transitions':transitions,
 'validation_loss_epochs_1_2_3':loss,'human_approved':False,'cross_model_critic':False,
 'method':'Single Codex reviewer directly read inputs, product evidence, RAG and raw answers. Hash/quote assertions are integrity checks, not semantic grading.'}
(D/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
with (D/'reviews.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['row_id','epoch','rating','reason','input_quotes','answer_quotes','answer_sha256','human_approved'])
    for rid in ids:
        for e in (1,2,3):
            n=index[rid,e];w.writerow([rid,e,n['rating'],n['reason'],json.dumps(n['input_quotes'],ensure_ascii=False),json.dumps(n['answer_quotes'],ensure_ascii=False),n['answer_sha256'],False])
esc=lambda s:html.escape(str(s))
dump=lambda o:json.dumps(o,ensure_ascii=False,indent=2)
table='<table><tr><th>판정</th><th>Epoch 1</th><th>Epoch 2</th><th>Epoch 3</th></tr>'
for rating in ('PASS','WARN','FAIL'):
    table+='<tr><th>'+rating+'</th>'+''.join(f'<td>{counts[str(e)].get(rating,0)}</td>' for e in (1,2,3))+'</tr>'
table+='<tr><th>전체 검증 loss (184건)</th>'+''.join(f'<td>{v:.6f}</td>' for v in loss)+'</tr></table>'
cards=[]
for rid in ids:
    p=pairs[rid];ratings=[index[rid,e]['rating'] for e in (1,2,3)]
    content=f'<article data-id="{rid}" data-ratings="{" ".join(ratings)}"><h2>{rid} · {" → ".join(ratings)}</h2>'
    content+='<details><summary>공통 입력 raw 전체 (system + user JSON · 제품 표시 · RAG 원문 포함)</summary><pre>'+esc(dump(p['input_messages_1800']))+'</pre></details><div class="epochs">'
    for e in (1,2,3):
        n=index[rid,e];raw=p['new_all_epochs'][str(e)]
        content+=f'<section><h3>Epoch {e} <span class="{n["rating"]}">{n["rating"]}</span></h3><h4>실제 모델 답변 raw</h4><pre>{esc(raw["text"])}</pre><h4>입력 raw 인용</h4>'
        content+=''.join('<blockquote>'+esc(q)+'</blockquote>' for q in n['input_quotes'])
        content+='<h4>답변 raw 인용</h4>'+''.join('<blockquote>'+esc(q)+'</blockquote>' for q in n['answer_quotes'])
        content+='<h4>근거와 판정의 연결</h4><p>'+esc(n['reason'])+'</p><details><summary>해시 · 검수 출처 · 실행 메타데이터</summary><pre>'+esc(dump({'review':n,'raw_metadata':{k:v for k,v in raw.items() if k not in ('input_messages','text','reference_teacher_answer')}}))+'</pre></details></section>'
    cards.append(content+'</div></article>')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>1,800건 Epoch 1–3 실제 답변 검수</title><style>
body{font-family:system-ui,sans-serif;margin:24px;background:#f5f7fa;color:#17212e;line-height:1.6}main{max-width:1600px;margin:auto}table{border-collapse:collapse;background:white}th,td{padding:10px 24px;border:1px solid #cbd5e1}article{background:white;padding:20px;margin:24px 0;border:1px solid #cbd5e1;border-radius:12px}.epochs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}section{min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-family:ui-monospace,monospace;background:#f1f5f9;padding:12px;font-size:13px}blockquote{border-left:3px solid #64748b;margin:8px 0;padding-left:12px;overflow-wrap:anywhere}.PASS{color:#176b38}.WARN{color:#915c00}.FAIL{color:#b42318}summary{cursor:pointer}input,select{padding:10px;margin:8px}nav{position:sticky;top:0;background:#edf2f7;padding:8px;z-index:2}[hidden]{display:none!important}@media(max-width:1000px){.epochs{grid-template-columns:1fr}} </style><main>
<h1>1,800건 학습 · Epoch 1·2·3 실제 답변 비교</h1>
<p>동일 입력 60개 × 3 epoch = 180개 답변. Epoch 1·2의 120개는 새로 직접 읽었고, Epoch 3의 60개는 동일 해시의 기존 검수를 보존했습니다. 각 입력·제품 표시·인용 문헌과 실제 답변을 비교해 판정했습니다. 자동 키워드 검사로 판정하지 않았습니다.</p>
<p><b>범위와 한계:</b> 비교 가능한 공통 60개는 비무작위 표본이며 세정·보습과 증상/포장 HOLD 중심입니다. 전체 검증 184건 또는 전체 1,800건 검수가 아닙니다. 단일 Codex 검수이며 사람 승인·독립 Cross-Model Critic이 아닙니다. PASS도 배포/임상 승인 뜻이 아닙니다. Epoch 3의 설명에는 이전 900건 모델과의 비교가 포함돼 있습니다.</p>
<p><b>기준:</b> PASS=검토 범위에서 뚜렷한 오류 없음. WARN=모호함·구체 안내 부족·근거 대응 약함. FAIL=명확한 입력/표시 모순·사실 발명·출처 범위 왜곡. 단순 조건문을 실제 사실 발명으로 취급하지 않았습니다.</p>'''+table+'''
<p>loss는 전체 검증 184건 값이고 위 판정은 공통 60건 값이므로 같은 모수의 점수는 아닙니다. 가장 낮은 loss가 곧 가장 좋은 의미 품질을 뜻하지 않습니다. epoch별 변화는 사례별로 비단조적입니다. 확증을 위해서는 익명화된 추가 검수와 전체 검증셋 평가가 필요합니다.</p>
<nav><label>사례 검색 <input id="q" placeholder="예: 0222"></label><label>포함 판정 <select id="rating"><option value="">전체</option><option>PASS</option><option>WARN</option><option>FAIL</option></select></label><span id="count"></span></nav>'''+''.join(cards)+'''</main><script>
function filter(){let n=0;const q=document.querySelector('#q').value.toLowerCase(),r=document.querySelector('#rating').value;document.querySelectorAll('article').forEach(a=>{a.hidden=!(a.dataset.id.includes(q)&&(!r||a.dataset.ratings.split(' ').includes(r)));if(!a.hidden)n++});document.querySelector('#count').textContent=n+' / 60 사례'}document.querySelector('#q').addEventListener('input',filter);document.querySelector('#rating').addEventListener('change',filter);filter();</script></html>'''
(D/'report.html').write_text(page,encoding='utf-8',newline='\n')
lines=['# 1,800건 Epoch 1·2·3 실제 답변 검수','',
'동일 입력 60개 × 3 epoch = 180개 답변. E1/E2 신규 직접 검수 120개, E3 동일 해시 기존 검수 60개. 단일 Codex 검수이며 사람 승인/독립 교차 검수가 아닙니다. 전체 184건 검증셋의 전수 검수가 아닙니다.','',
'| 판정 | Epoch 1 | Epoch 2 | Epoch 3 |','|---|---:|---:|---:|']
for r in ('PASS','WARN','FAIL'):lines.append('| '+r+' | '+' | '.join(str(counts[str(e)].get(r,0)) for e in (1,2,3))+' |')
lines+=['','전체 검증 loss (184건): '+', '.join(f'E{e+1}={v:.6f}' for e,v in enumerate(loss))+'. 판정 표본과 loss의 모집단은 다릅니다.','',
'기준: PASS 뚜렷한 문제 없음 / WARN 모호함·안내 부족·근거 대응 약함 / FAIL 명확한 입력·표시 모순, 발명, 출처 왜곡.','',
'`report.html`에서 모든 사례의 원본 입력과 3개 실제 답변, 원문 인용, 판정 이유, 해시를 볼 수 있습니다. `reviews.csv`는 180개 판정이며 `summary.json`에는 전이 집계가 있습니다. E3 원문 이유에는 과거 900건 비교가 포함됩니다.','',
'변화 예: 0222는 손등 시험을 E2에서 얼굴 시험으로 바꾸었다가 E3에서 관찰 왜곡을 해소하지만 안내 부족이 남습니다. 0454는 E1에서 올바르게 읽은 눈가 표시를 E2에서 부정하고 E3에서 회복합니다. 0062·0070의 통증 시점 혼동은 E1부터 지속됩니다.','',
'의미 품질의 최적 epoch는 loss만으로 확정할 수 없습니다. 이 60개 표본의 판정 분포를 참고하되, 전체 검증셋의 익명 검수와 독립 검수 전에는 최종 모델 선택을 확정하지 않는 것이 타당합니다.']
(D/'REPORT.ko.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
files=[p for p in D.iterdir() if p.is_file() and p.name!='sha256.json']
(D/'sha256.json').write_text(dump({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})+'\n',encoding='utf-8',newline='\n')
print(dump(summary))
print('Integrity checked: 180 unique reviews; 180 answer hashes; exact quoted input/output substrings; 60 identical inputs.')
