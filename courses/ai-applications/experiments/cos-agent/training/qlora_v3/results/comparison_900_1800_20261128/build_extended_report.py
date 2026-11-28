"""Render authored 60-pair reviews. Counts/quote integrity only are automated."""
import base64
from collections import Counter
import csv
from datetime import datetime,timezone
import hashlib
import html
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H=Path(__file__).resolve().parent
reviews=json.loads((H/'extended_review_60.json').read_text(encoding='utf-8'))
pairs={p['row_id']:p for p in json.loads((H/'common_90_raw_pairs.json').read_text(encoding='utf-8'))}
alignment=json.loads((H/'input_alignment.json').read_text(encoding='utf-8'))
assert len(reviews)==len({n['row_id'] for n in reviews})==60
assert set(n['row_id'] for n in reviews)==set(alignment['exact_messages_equal_ids'])
for n in reviews:
    p=pairs[n['row_id']]
    assert n['old_answer_sha256']==p['answer_900_epoch2']['content_sha256']
    assert n['new_answer_sha256']==p['answer_1800_epoch3']['content_sha256']
    assert n['input_sha256']==hashlib.sha256(p['input_messages_1800'][1]['content'].encode()).hexdigest()
    assert all(q in p['answer_900_epoch2']['text'] for q in n['old_quotes'])
    assert all(q in p['answer_1800_epoch3']['text'] for q in n['new_quotes'])
    assert all(q in p['input_messages_1800'][1]['content'] for q in n['input_quotes'])
old=Counter(n['old_rating'] for n in reviews);new=Counter(n['new_rating'] for n in reviews)
changes=Counter(n['comparison'] for n in reviews)
transition=Counter((n['old_rating'],n['new_rating']) for n in reviews)
summary={'reviewed_pairs':60,'actual_answers_read':120,'comparison':'900 E2 vs 1800 E3',
         'exact_input_match':True,'old_ratings':dict(old),'new_ratings':dict(new),
         'comparative_judgments':dict(changes),
         'rating_transition':{f'{a}->{b}':transition[a,b] for a in ['PASS','WARN','FAIL'] for b in ['PASS','WARN','FAIL']},
         'new_fail_ids':[n['row_id'] for n in reviews if n['new_rating']=='FAIL'],
         'reviewer':'Codex direct reading, one reviewer; not independent cross-model or human approval',
         'sampling':'All 60 byte-identical shared inputs. Cleansing/moisturizing and two HOLD families; not random or representative.',
         'excluded_shared_rows':30,'excluded_reason':'Transport fields differ; same task facts, different token input. Not silently mixed.',
         'new_epoch3_unreviewed_rows':124,'new_other_epochs_semantic_review':'not performed in this 60-pair audit',
         'interpretation':'Fewer clear FAILs but fewer issue-free PASSs and more WARNs. No unqualified superiority or accuracy claim.',
         'human_approved':False,'checked_utc':datetime.now(timezone.utc).isoformat()}
(H/'extended_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (H/'extended_review_60.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['row_id','old_rating','new_rating','comparison','reason','old_answer_sha256','new_answer_sha256'])
    w.writeheader();w.writerows({k:n[k] for k in w.fieldnames} for n in reviews)
fig,ax=plt.subplots(figsize=(7.3,3.7));bottom=[0,0]
for status,color in [('PASS','#16a34a'),('WARN','#eab308'),('FAIL','#dc2626')]:
    vals=[old[status],new[status]]
    bars=ax.bar(['900 / Epoch 2','1800 / Epoch 3'],vals,bottom=bottom,label=status,color=color,width=.55)
    ax.bar_label(bars,labels=[str(v) for v in vals],label_type='center',color='white' if status!='WARN' else '#111',fontweight='bold')
    bottom=[a+b for a,b in zip(bottom,vals)]
ax.set(ylabel='Directly reviewed answers (count)',ylim=(0,65),title='60 identical-input pairs | one Codex reviewer')
ax.spines[['top','right']].set_visible(False);ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,-.12))
fig.tight_layout();fig.savefig(H/'extended_review_counts.png',dpi=170,bbox_inches='tight');plt.close(fig)
esc=lambda s:html.escape(str(s),quote=True)
code=lambda s:'<pre>'+esc(s)+'</pre>'
labels={'improvement':'개선','regression':'악화','unchanged':'실질 변화 없음','mixed':'혼합 변화'}
cards=[]
for n in reviews:
    p=pairs[n['row_id']];request=json.loads(p['input_messages_1800'][1]['content'])
    quotes=''.join('<li>'+esc(q)+'</li>' for q in n['input_quotes'])
    cards.append(f'''<article data-case="{esc(n['row_id'])}" data-change="{n['comparison']}" data-rating="{n['new_rating']}">
<h2>{esc(n['row_id'])} <small>{n['old_rating']} → {n['new_rating']} · {labels[n['comparison']]}</small></h2>
<p class="reason">{esc(n['reason'])}</p>
<div class="columns"><section><h3>900건 · Epoch 2 실제 raw</h3>{code(p['answer_900_epoch2']['text'])}</section>
<section><h3>1,800건 · Epoch 3 실제 raw</h3>{code(p['answer_1800_epoch3']['text'])}</section></div>
<h3>판정에 사용한 입력 원문 구절</h3><ul>{quotes}</ul>
<details><summary>입력 JSON 전체 — 두 모델 동일</summary>{code(json.dumps(request,ensure_ascii=False,indent=2))}</details>
<details><summary>출처 해시·검토자·주의사항</summary>{code(json.dumps(n,ensure_ascii=False,indent=2))}</details></article>''')
rows=''.join(f'<tr><td>{s}</td><td>{old[s]}</td><td>{new[s]}</td></tr>' for s in ['PASS','WARN','FAIL'])
img=base64.b64encode((H/'extended_review_counts.png').read_bytes()).decode()
content=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>900 / 1800 · 동일 입력 60건 raw 직접 대조</title><style>
body{{font:16px/1.65 system-ui,sans-serif;background:#f1f5f9;color:#172033;margin:0}}main{{max-width:1200px;margin:auto;padding:28px}}
h1{{line-height:1.3}}h2{{font-size:21px}}h3{{font-size:16px}}small{{font-size:14px;font-weight:400;color:#475569}}
.notice{{background:#fff7dd;border-left:5px solid #ca8a04;padding:16px}}article,.panel{{background:white;padding:22px;margin:20px 0;border-radius:12px}}
.columns{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f8fafc;padding:14px;font:14px/1.7 ui-monospace,monospace}}
.reason{{border-left:4px solid #2563eb;padding-left:14px}}table{{border-collapse:collapse;width:100%;max-width:560px}}td,th{{padding:8px 14px;border-bottom:1px solid #cbd5e1;text-align:left}}
.filters{{position:sticky;top:0;background:#e2e8f0;padding:12px;border-radius:8px;display:flex;gap:10px;flex-wrap:wrap}}select,input{{padding:9px;font:inherit;max-width:100%}}img{{max-width:100%;height:auto}}summary{{cursor:pointer;padding:8px}}
@media(max-width:760px){{main{{padding:12px}}.columns{{grid-template-columns:1fr}}article{{padding:15px}}}}</style>
<main><h1>900건 vs 1,800건<br>동일 입력 60건 · 실제 답변 120개 직접 대조</h1>
<p>900건 Epoch 2와 1,800건 Epoch 3 · 기존 10건을 포함해 총 60건 · 모델/데이터 수정이나 추가 GPU 실행 없음</p>
<div class="notice"><strong>단일 Codex 검토자의 판정이며 사람 승인·Cross-Model Critic PASS가 아닙니다.</strong><br>
PASS = 이번 범위에서 뚜렷한 내용 오류나 중요한 설명 문제가 보이지 않음.<br>
WARN = 모호함·불필요한 조건/주제·구체 안내 부족·해석 여지가 있는 표현. 명확한 사실 오류와 별도.<br>
FAIL = 입력·표시와의 명확한 충돌, 미제공 사실 단정, 근거 없는 추가 행동, 인용 근거 연결 실패.<br>
원문을 읽고 판정했습니다. 스크립트는 해시·인용 문자열 일치·건수·표 렌더링만 검사합니다.</div>
<section class="panel"><h2>핵심 결과</h2><table><thead><tr><th>판정</th><th>900 E2</th><th>1800 E3</th></tr></thead><tbody>{rows}</tbody></table>
<p>사례별 변화: 개선 {changes['improvement']} · 악화 {changes['regression']} · 실질 변화 없음 {changes['unchanged']} · 혼합 {changes['mixed']}.</p>
<p><strong>명확한 FAIL은 17→13건으로 줄었지만 PASS도 29→18건으로 줄었습니다.</strong> 큰 오류 일부가 줄고 모호함이 늘어난 혼합 결과입니다. WARN과 FAIL은 같은 심각도가 아니며, 변화 건수만으로 순위를 정하지 않습니다.</p>
<img src="data:image/png;base64,{img}" alt="60개 동일 입력의 단일 검토자 판정 건수 비교"></section>
<section class="panel"><h2>비교 범위와 한계</h2><ul>
<li>공통 ID 90개 중 입력 문자열까지 동일한 60개 전부를 검토했습니다. 세정/보습 및 증상·포장 보류 사례에 해당합니다. 자외선차단과 의료진 지침 충돌 사례는 이 60건에 포함되지 않습니다.</li>
<li>나머지 공통 30개는 timeout_seconds/max_response_bytes 유무만 달라 의미상 사실은 같지만 토큰 입력이 다릅니다. 이번 집계에 섞지 않았습니다.</li>
<li>신규 Epoch 3의 184건 중 124건과 다른 4개 epoch의 raw는 이번 의미 검토 대상이 아닙니다. 총 920개 전수 검수 완료라고 주장하지 않습니다.</li>
<li>검증 loss 최저 Epoch 3을 비교 후보로 썼으나 의미 품질의 최적 epoch로 확정하지 않았습니다.</li>
<li>초기 LR 1e-4→5e-5, 학습 데이터·검증 분포와 DDP 등도 달라, 차이를 데이터 수만의 효과로 해석할 수 없습니다.</li>
<li>표본·단일 검토자 판정의 건수이며 일반화 정확도, 임상 정확도 또는 사람 승인율이 아닙니다. 세부 판정은 아래 raw를 보고 재검토할 수 있습니다.</li></ul></section>
<div class="filters"><input id="query" placeholder="ID 검색" aria-label="사례 ID 검색"><select id="change" aria-label="변화 필터"><option value="">모든 변화</option>{''.join(f'<option value="{k}">{v}</option>' for k,v in labels.items())}</select>
<select id="rating" aria-label="신규 판정 필터"><option value="">신규 판정 전체</option><option>PASS</option><option>WARN</option><option>FAIL</option></select><span id="count">60 / 60건</span></div>
{''.join(cards)}<footer>검토 원본: extended_review_60.json · CSV: extended_review_60.csv · 원본 대조: common_90_raw_pairs.json · 무결성: sha256.json</footer></main>
<script>const controls=['query','change','rating'].map(x=>document.getElementById(x));function filter(){{const[q,c,r]=controls.map(x=>x.value.trim());let n=0;document.querySelectorAll('article').forEach(a=>{{const yes=(!q||a.dataset.case.includes(q))&&(!c||a.dataset.change===c)&&(!r||a.dataset.rating===r);a.hidden=!yes;if(yes)n++;}});document.getElementById('count').textContent=n+' / 60건';}}controls.forEach(x=>x.addEventListener('input',filter));</script></html>'''
(H/'extended_review_60.html').write_text(content,encoding='utf-8',newline='\n')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in H.iterdir() if p.is_file() and p.name!='sha256.json'}
(H/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print(H/'extended_review_60.html')
