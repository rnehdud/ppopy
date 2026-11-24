"""대화별 이미지 아래에 실제 raw 근거를 표시해요. 데이터·이미지는 수정하지 않아요."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import zipfile

COS = Path(__file__).resolve().parents[1]

def make_gallery(inputs, rows, images):
    def raw(value):
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
        return '<pre>' + html.escape(text) + '</pre>'

    def detail(title, value, expanded=False):
        return '<details' + (' open' if expanded else '') + '><summary>' + title + '</summary>' + raw(value) + '</details>'

    common = {k:v for k,v in rows[0].items() if k != 'messages' and all(r.get(k) == v for r in rows)}
    prompts = [r['messages'][0]['content'] for r in rows]
    assert len(set(prompts)) == 1
    cards = []
    for i, (case, row, pic) in enumerate(zip(inputs['cases'], rows, images), 1):
        assert case['id'] == row['id'] == pic['id']
        req = json.loads(row['messages'][1]['content'])
        metadata = {k:v for k,v in row.items() if k != 'messages' and k not in common}
        evidence = []
        for chunk in req['rag_chunks']:
            evidence.append('<li><code>' + html.escape(chunk['evidence_ref']) + '</code> · <a href="' + html.escape(chunk['source_url'], quote=True) + '" target="_blank" rel="noopener noreferrer">출처 원문</a> · ' + html.escape(chunk['locator']) + '</li>')
        links = '<ul>' + ''.join(evidence) + '</ul>' if evidence else '<p>이 HOLD 입력에는 RAG 청크가 없어요.</p>'
        panels = detail('자연스러운 합성 사용자 발화', case['scenario_raw'])
        if case.get('observation_trace'):
            confirmations=case.get('prior_user_confirmations',[])
            panels += '<h4>별도로 확인한 사용자 응답 · 합성 설정</h4><ul>'+''.join('<li>'+html.escape(p['text'])+'</li>' for p in confirmations)+'</ul>'
            panels += '<p>아래 기록은 합성 입력의 출처를 분리한 작성 자료예요. 실제 NLU·AFA 실행이나 실제 사용자 확인 로그가 아니에요.</p>'
            panels += detail('관찰이 나온 발화 raw · 슬롯별 출처 추적',case['observation_trace'])
            panels += detail('시스템 제품 확인 raw · 사용자 발화와 분리',case.get('system_context',{}))
        panels += detail('사례별 메타데이터 · 분할 · Hard Negative · 인용 통제', metadata, True)
        panels += detail('실제 모델 입력 JSON 전체', req)
        panels += detail('관찰 슬롯 raw · 값 / 미상 상태 / 출처 / 확인 여부', req['confirmed_observations'])
        panels += detail('제품 근거 raw · 버전 / 표시 / 사용 근거 보류 상태', req['product_evidence'])
        panels += '<details><summary>문헌 청크 raw · 본문 / URL / 위치 / 확인일 / 한계</summary>' + links + raw(req['rag_chunks']) + '</details>'
        panels += detail('생성 응답 raw · 줄바꿈과 Markdown 포함', row['messages'][2]['content'])
        panels += detail('원본 user 메시지 문자열 · 직렬화 원문', row['messages'][1]['content'])
        registry=inputs.get('sources',{}).get('sources',{})
        if registry:
            selected={c['evidence_ref']:registry[c['evidence_ref']] for c in req['rag_chunks']}
            panels += detail('코퍼스 출처 추적 raw · 커밋 / 파일 / 문단 / 본문 해시',selected)
        cards.append(f'''<article id="{case['id']}"><h2>{i:02d} · {html.escape(case['title'])}</h2>
<a href="{pic['file']}" target="_blank" rel="noopener"><img loading="lazy" src="{pic['file']}" alt="{html.escape(case['title'])}"></a>
<section class="raw-panel"><h3>이 대화의 개별 raw 근거</h3><p>노란 말풍선은 자연어 합성 사용자 발화예요. 별도 사용자 확인·제품 근거와 분리했으며, 실제 SLM 입력은 아래 정형 JSON이에요.</p>
<dl><dt>입력 SHA-256</dt><dd><code>{case['input_sha256']}</code></dd></dl>{panels}</section></article>''')
    common_panel = detail('고정 시스템 프롬프트 raw', prompts[0]) + detail('24행 전체에서 동일한 메타데이터 raw · 생성 이력과 미검수 상태', common)
    if inputs.get('plan_revision'):
        common_panel = '<p><strong>개정 '+str(inputs['plan_revision'])+' · '+html.escape(inputs.get('target_training_model',''))+'</strong><br>최신 PPO-37의 Step 1 샘플 문헌으로 갱신했어요. Tier 2 논문은 사용하지 않았어요. 공식 PPO-42 청크 풀은 미인계 상태이며 900턴과 학습은 진행하지 않았어요.</p>' + detail('샘플 코퍼스와 작업 기준 raw', {'base_commit':inputs.get('base_commit'),'initial_base_commit':inputs.get('initial_base_commit'),'requirements_updated_at':inputs.get('requirements_updated_at'),**{k:v for k,v in inputs['sources'].items() if k!='sources'}}) + common_panel
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ppopy 파일럿 24개 대화와 raw 근거</title><style>
body{margin:0;background:#f1f5f9;color:#243448;font-family:system-ui,sans-serif}header{max-width:1450px;margin:auto;padding:36px 24px}h1{font-size:30px}p{line-height:1.8}main{max-width:1500px;margin:auto;padding:0 20px 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,560px),1fr));gap:28px;align-items:start}article{min-width:0;background:white;border-radius:20px;padding:18px;box-shadow:0 3px 15px #172a4310}h2{font-size:20px;line-height:1.5}img{width:100%;height:auto;display:block;border-radius:12px}a{color:#255f95}.raw-panel{margin-top:24px;border-top:2px solid #dce5ee;padding-top:8px}h3{font-size:19px}details{background:#f8fafc;border:1px solid #dce5ee;border-radius:10px;margin:12px 0;padding:12px}summary{cursor:pointer;font-weight:650;line-height:1.6}pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font:13px/1.8 Consolas,monospace;background:white;padding:14px;border-radius:8px;tab-size:2}code,dd{overflow-wrap:anywhere}dd{margin:8px 0 16px;font-size:13px}dt{font-weight:650}li{margin:10px 0;line-height:1.7}.common{background:white;border:1px solid #dce5ee;border-radius:14px;padding:16px;margin-top:20px}section p{font-size:14px}
</style></head><body><header><h1>Ppopy · 합성 파일럿 24개 대화와 raw 근거</h1><p>각 이미지 아래에 해당 사례의 실제 입력·제품·참고 문헌·메타데이터를 넣었어요. 제목을 누르면 raw 내용을 펼칠 수 있어요.<br>실제 카카오톡 기록이 아니며 모든 사례는 Critic·사람 미검수 상태예요. 구조 검사 통과는 내용 검수 승인이 아니에요. development_preview · production_enabled=false.</p><div class="common"><h2>모든 대화에 공통인 내용 · 여기서 한 번만 표시</h2>''' + common_panel + '''<p>solution 공통 제목: 핵심 안내 / 근거 및 이유 / 확인이 필요한 한계<br>hold 공통 제목: 개별 권고 보류 안내 / 필요한 다음 단계</p></div></header><main>''' + '\n'.join(cards) + '</main></body></html>'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--gallery',type=Path,default=COS/'outputs/qlora_v3_pilot_20261125/chat_images_v2')
    out=parser.parse_args().gallery.resolve()
    data=COS/'data/qlora/v2'
    paths=[data/'pilot_24_inputs.json',data/'pilot_24.jsonl']
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    image_before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}
    inputs=json.loads(paths[0].read_text(encoding='utf-8'))
    rows=[json.loads(line) for line in paths[1].read_text(encoding='utf-8').splitlines()]
    manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    assert len(rows)==len(inputs['cases'])==len(manifest['images'])==len(image_before)==24
    page=make_gallery(inputs,rows,manifest['images'])
    (out/'index.html').write_bytes(page.encode('utf-8'))
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert image_before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}
    # 각 실제 user 문자열과 응답 문자열이 HTML escaping 외의 변환 없이 들어갔는지 확인해요.
    for row in rows:
        assert html.escape(row['messages'][1]['content']) in page
        assert html.escape(row['messages'][2]['content']) in page
    assert page.count('<article id=')==24
    manifest.setdefault('original_render_source_sha256',dict(manifest.get('source_sha256',{})))
    manifest['source_sha256']={Path(k).name:v for k,v in before.items()}
    manifest['source_sha256']['pilot_24_responses.json']=hashlib.sha256((data/'pilot_24_responses.json').read_bytes()).hexdigest()
    manifest['gallery_has_per_case_raw']=True
    (out/'manifest.json').write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    archive=out.parent/(out.name+'.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.iterdir()):
            z.write(p,arcname='chat_images/'+p.name)
    print(json.dumps({'case_panels':24,'raw_user_and_assistant_preserved':True,'dataset_and_images_unchanged':True,'html':str(out/'index.html'),'zip':str(archive)},ensure_ascii=False))

if __name__=='__main__':
    main()
