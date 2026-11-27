"""Aggregate authored raw-reading notes; never infer a PASS from automatic checks."""
import csv,hashlib,html,json
from collections import Counter
from pathlib import Path
O=Path(__file__).parent/'kaggle_raw_review_20261127'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
models=['kaggle-base']+[f'kaggle-epoch-{i}' for i in range(1,5)]
cases=[load(p) for p in sorted((O/'cases').glob('*.json'))]
notes=[json.loads(l) for l in (O/'manual_reviews.jsonl').read_text(encoding='utf-8').splitlines()]
by={(n['row_id'],n['model']):n for n in notes}
assert len(by)==len(notes)
nonlogical={'citation_missing','citation_format','missing_required_guidance','ambiguous_sequence'}
def hard(n):return n['verdict']=='FAIL' and bool(set(n['categories'])-nonlogical)
for c in cases:
 for a in c['answers']:
  n=by.get((c['row_id'],a['model']))
  if n:
   assert n['candidate_sha256']==hashlib.sha256(a['text'].encode()).hexdigest()
   a['review']=n
history=load(O/'kaggle_v2/qlora_early_stopping_lr1e4_20261127/epoch_history.json')
complete=len(notes)==450 and len(cases)==90
paired=[c for c in cases if len(c['answers'])==5 and all((c['row_id'],m) in by for m in models)]
paired_ids={c['row_id'] for c in paired}
summary={'status':'complete' if complete else 'INCOMPLETE — no final sweet spot conclusion',
 'reviewed_answers':len(notes),'target_answers':450,'paired_cases_generated':len(cases),
 'review_scope':'Local WSL vLLM NF4/BF16 replay of actual Kaggle v2 weights; NOT Kaggle T4 output review',
 'fully_paired_cases_reviewed':len(paired),'partial_cases':len(cases)-len(paired),
 'actual_semantic_reader':'Codex direct raw reading, not human or cross-model approval',
 'source_manifest':{'checked':27,'failed':[]},'human_approved':False,
 'loss_best_epoch':min(history,key=lambda x:x['val_token_loss'])['epoch'],
 'caveats':['Same 90 validation cases are used for model selection; not independent test results.',
 'Epochs 1–4 are actual Kaggle v2 adapters; epoch 5 was not trained in this run.',
 'Newly replayed outputs on WSL vLLM NF4/BF16, not original Kaggle FP16 generation logs.',
 'All conditions use the same serving profile; this does not isolate quantization/precision effects.',
 'Cases are clustered in scenario families; row counts are not independent scenario counts.',
 'PASS means no issue found under the recorded rubric, not proof of safety or human approval.',
 'FAIL includes separately reported utility and citation-format defects, not only logical contradictions.'],
 'per_model':[],'balanced_per_model':[]}
for m in models:
 ns=[n for n in notes if n['model']==m]
 counts=Counter(n['verdict'] for n in ns)
 summary['per_model'].append(dict(model=m,reviewed=len(ns),PASS=counts['PASS'],FAIL=counts['FAIL'],UNCERTAIN=counts['UNCERTAIN'],
  logical_or_source_FAIL=sum(hard(n) for n in ns),
  utility_or_format_only_FAIL=sum(n['verdict']=='FAIL' and not hard(n) for n in ns),
  categories=dict(Counter(k for n in ns for k in n['categories'] if n['verdict']!='PASS')),
  modes={mode:dict(Counter(n['verdict'] for n in ns if n['mode']==mode)) for mode in ['solution','hold']}))
 balanced=[n for n in ns if n['row_id'] in paired_ids];bc=Counter(n['verdict'] for n in balanced)
 summary['balanced_per_model'].append({'model':m,'cases':len(balanced),**{v:bc[v] for v in ['PASS','FAIL','UNCERTAIN']},
  'logical_or_source_FAIL':sum(hard(n) for n in balanced),'utility_or_format_only_FAIL':sum(n['verdict']=='FAIL' and not hard(n) for n in balanced)})
progression=[]
for c in cases:
 ns=[by.get((c['row_id'],m)) for m in models]
 row=dict(case_index=c['index'],row_id=c['row_id'],mode=c['mode'])
 row.update({m:n['verdict'] if n else 'PENDING' for m,n in zip(models,ns)})
 row['base_logical_failure']=hard(ns[0]) if ns[0] else None
 row['first_adapted_logical_failure_epoch']=next((i for i,n in enumerate(ns[1:],1) if n and hard(n)),None)
 row['first_adapted_failure_interpretation']='pre-existing Base failure' if row['base_logical_failure'] else 'first observed saved epoch; onset within epoch unknown'
 progression.append(row)
save(O/'semantic_summary.json',summary)
save(O/'case_progression.json',progression)
with (O/'manual_reviews.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['case_index','row_id','mode','model','verdict','categories','rationale','claim_quote','source_quote','connection','candidate_sha256','raw_case_file']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for n in notes:
  for e in n['evidence']:w.writerow({k:(','.join(n[k]) if k=='categories' else n.get(k,e.get(k,''))) for k in fields})
with (O/'case_progression.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(progression[0]));w.writeheader();w.writerows(progression)
data=json.dumps(dict(summary=summary,cases=cases,history=history,progression=progression),ensure_ascii=False).replace('<','\\u003c')
template=r'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kaggle checkpoint raw 검수</title>
<style>body{font:16px system-ui;background:#f1f5f9;color:#172033;margin:0}main{max-width:1500px;margin:auto;padding:24px}h1{font-size:25px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:9px;text-align:left;border:1px solid #cbd5e1}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.65 system-ui}article,section{background:white;border-radius:10px;padding:18px;margin:14px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}.FAIL{border-top:6px solid #c42a39}.PASS{border-top:6px solid #168068}.UNCERTAIN,.PENDING{border-top:6px solid #b87c0b}.warn{background:#fff1cc;padding:14px}blockquote{margin:8px 0;padding:10px;border-left:3px solid #6b8cbb;background:#f1f5f9}label{display:inline-block;margin:8px}select{padding:9px}details{margin:12px 0}small{color:#475569}</style>
<main><h1>동일 입력 × Base / Epoch 1–4: raw 답변 직접 검수</h1><div id="status" class="warn"></div><p>재학습 없이 실제 Kaggle v2 어댑터로 새로 생성한 결과입니다. 자동 검사 결과가 아니라 입력·제품 표시·문헌·답변을 읽은 검수 메모를 연결합니다. 사람 승인 및 Cross-Model Critic 결과가 아닙니다.</p><div id="summary"></div><details><summary>실험 조건과 해석 한계</summary><ul id="caveats"></ul><p>생성: vLLM / NF4 / BF16 / temperature=0 / seed=20261127 / max_tokens=768 / max_model_len=3072. 교사 답변은 모델 입력에 넣지 않았습니다. Loss 기록의 최저 epoch와 자유 생성 답변의 최적 epoch는 별도 지표입니다.</p></details>
<label>사례 <select id="case"></select></label><label>모델 <select id="model"><option value="">전체 5개</option></select></label><label>판정 <select id="verdict"><option value="">전체</option><option>PASS</option><option>FAIL</option><option>UNCERTAIN</option><option>PENDING</option></select></label>
<section id="source"></section><div id="answers" class="grid"></div><p><a href="manual_reviews.csv">검수 CSV</a> · <a href="manual_reviews.jsonl">원문 연결 검수 JSONL</a> · <a href="raw_answers.jsonl">실제 생성 raw JSONL</a> · <a href="case_progression.csv">사례별 epoch 변화</a> · <a href="evaluation_plan.json">가중치 해시·실험 설정</a></p></main>
<script>const D=__DATA__;const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const el=x=>document.getElementById(x);
el('status').textContent=`로컬 WSL 재생 결과입니다 — Kaggle T4 답변 검수 아님. ${D.summary.status} | 직접 검수 ${D.summary.reviewed_answers}/450개 · 완전 비교 가능 사례 ${D.summary.fully_paired_cases_reviewed}/90개 · 부분 사례 ${D.summary.partial_cases}개`;
el('summary').innerHTML='<p>아래 비교표는 5개 답변을 모두 읽은 동일 '+D.summary.fully_paired_cases_reviewed+'개 사례만 사용해요. 누락 모델이 있는 부분 사례는 순위 비교에서 제외해요.</p><table><tr><th>모델</th><th>동일 비교 사례</th><th>PASS</th><th>FAIL</th><th>미확정</th><th>논리·출처 FAIL</th><th>안내누락·형식만 FAIL</th></tr>'+D.summary.balanced_per_model.map(r=>`<tr>${[r.model,r.cases,r.PASS,r.FAIL,r.UNCERTAIN,r.logical_or_source_FAIL,r.utility_or_format_only_FAIL].map(x=>`<td>${esc(x)}</td>`).join('')}</tr>`).join('')+'</table>';
el('caveats').innerHTML=D.summary.caveats.map(x=>`<li>${esc(x)}</li>`).join('');
el('case').innerHTML=D.cases.map(c=>`<option value="${c.index}">${c.index}. ${esc(c.row_id)} (${esc(c.mode)})</option>`).join('');D.summary.per_model.forEach(m=>el('model').add(new Option(m.model,m.model)));
function render(){let c=D.cases.find(c=>c.index==el('case').value);if(!c)return;el('source').innerHTML=`<h2>${esc(c.row_id)} · ${esc(c.mode)}</h2><details open><summary>Raw 입력 / 제품 / 허용 근거 / 방해 문헌</summary><pre>${esc(JSON.stringify(c.request,null,2))}</pre></details><details><summary>교사 답변 (독립 정답 판정 기준 아님)</summary><pre>${esc(c.reference_teacher_answer)}</pre></details>`;
el('answers').innerHTML=c.answers.filter(a=>(!el('model').value||a.model===el('model').value)&&(!el('verdict').value||(a.review?.verdict||'PENDING')===el('verdict').value)).map(a=>{let n=a.review,v=n?.verdict||'PENDING';return `<article class="${v}"><h3>${esc(a.model)} · ${v}</h3><small>finish=${esc(a.finish_reason)} · ${a.generated_tokens} tokens<br>SHA256 ${esc(a.content_sha256)}</small><h4>실제 답변 원문</h4><pre>${esc(a.text)}</pre>${n?`<h4>검수 이유</h4><p>${esc(n.rationale)}</p><p>${esc(n.categories.join(' / '))}</p>`+n.evidence.map(e=>`<b>답변 raw</b><blockquote>${esc(e.claim_quote)}</blockquote><b>입력·문헌 raw</b><blockquote>${esc(e.source_quote)}</blockquote><p>${esc(e.connection)}</p>`).join(''):'<b>아직 직접 읽은 검수 기록 없음 — 자동 PASS 아님</b>'}</article>`}).join('')}
['case','model','verdict'].forEach(id=>el(id).onchange=render);render();</script></html>'''
(O/'review.html').write_text(template.replace('__DATA__',data),encoding='utf-8',newline='\n')
print(json.dumps({'generated_cases':len(cases),'reviewed':len(notes),'complete':complete},ensure_ascii=False))
