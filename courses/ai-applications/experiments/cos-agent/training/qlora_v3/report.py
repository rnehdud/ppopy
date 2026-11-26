"""Render only actual measured training/evaluation records; missing reviews stay missing."""
import argparse,json,hashlib,shutil
from pathlib import Path
from common import dump,read_rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--output',required=True)
    p.add_argument('--http',help='Directory containing actual HTTP benchmark summary');a=p.parse_args()
    run=Path(a.run);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    selected=json.loads((run/'selection.json').read_text(encoding='utf-8'))
    logs=read_rows(run/'training_log.jsonl');cfg=json.loads((run/'config.json').read_text(encoding='utf-8'))
    base=selected['base'];epochs=selected['epochs']
    for name in ['config.json','environment.json','split_receipt.json','mask_sample.json','training_log.jsonl']:
        shutil.copyfile(run/name,out/name)
    for name in ['throughput_probe.json','windows_host_connectivity.json','vllm_startup.json','vram_summary.json','evaluation_execution_receipt.json']:
        if (run/name).exists():shutil.copyfile(run/name,out/name)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.5))
    for epoch in epochs:
        points=[r for r in logs if r['epoch']==epoch['epoch']]
        ax.plot([r['global_step'] for r in points],[r['token_loss_so_far'] for r in points],label=f"Train epoch {epoch['epoch']} running mean")
    points=[max(r['global_step'] for r in logs if r['epoch']==e['epoch']) for e in epochs]
    ax.plot(points,[e['val_token_loss'] for e in epochs],'o-',label='Validation assistant-token CE')
    ax.axhline(base['val_token_loss'],linestyle='--',color='gray',label='NF4 Base validation CE')
    ax.set(xlabel='Optimizer steps',ylabel='Assistant-token loss (lower is better)',title='Actual QLoRA training: fixed 810/90 split')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'loss_curve.png',dpi=170);plt.close(fig)
    body='# Qwen3-4B RAG-free QLoRA 학습·개발 검증 결과\n\n'
    body+='실제 실행 로그를 집계했어요. 810건만 학습하고 90건은 epoch 선택에 재사용한 개발 검증이에요. 독립 최종 test나 임상 성능 평가가 아니에요. 가중치는 로컬에만 보관하며 업로드하지 않았어요.\n\n'
    body+='![실제 loss 곡선](loss_curve.png)\n\n'
    body+='| 모델 | val token loss | 인용 허용 목록 위반/90 | solution 인용 누락/60 | KB 인용/90 | 방해 ID 인용/20 | HOLD 지시 regex 후보/30 | 길이 제한 도달/90 |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
    for row in [base,*epochs]:
        c=row['counts'];body+=f"| {row['tag']} | {row['val_token_loss']:.5f} | {c['invalid_citation']} | {c['solution_missing_citation']} | {c['kb_citation']} | {c['distractor_id_citation']} | {c['hold_instruction_candidate']} | {row['length_limited_rows']} |\n"
    body+=f"\n자동 지표와 val loss 기준 선택: **{selected['checkpoint']}**. 선택 규칙: `{cfg['selection']}`.\n\n"
    body+='## 해석의 경계\n\nID/regex 검사는 인용의 의미 정합성, 방해 내용의 간접 언급, 사실 발명·비진단 준수를 완전히 판정하지 못해요. `semantic_review.jsonl`의 실제 내용 검수와 raw 응답을 함께 봐야 해요. 검수가 없으면 해당 지표는 미검수이며 0%/PASS로 채우지 않아요. runtime fallback은 모델의 정답으로 세지 않아요.\n\n'
    review=run/'semantic_review.jsonl'
    if review.exists():
        shutil.copyfile(review,out/'semantic_review.jsonl');body+='실제 기록된 내용 검수는 `semantic_review.jsonl`에 있어요. 검수 범위·근거·불확실성을 각 행에서 확인해요.\n'
        summary_path=run/'semantic_review_summary.json'
        if summary_path.exists():
            shutil.copyfile(summary_path,out/summary_path.name)
            s=json.loads(summary_path.read_text(encoding='utf-8'))
            body+=f"\n**내용 검수: 모델 응답 {s['reviewed_model_responses']}/270개, 고유 상황 {s['distinct_cases_reviewed']}/90개. 전수 검수 완료: {s['review_complete']}. 사람 승인: false.**\n\n"
            body+='| 모델 | 실제 내용 검수 | PASS | FAIL | 미확정 | 남은 응답 |\n|---|---:|---:|---:|---:|---:|\n'
            for tag,counts in s['by_model'].items():body+=f"| {tag} | {counts['reviewed']} | {counts['pass']} | {counts['fail']} | {counts['uncertain']} | {counts['pending']} |\n"
            body+='\n초기 일부 행의 결과를 전체 오류율로 일반화하지 않아요. 안내와 근거의 모순도 검출돼 자동 지표만으로 최종 checkpoint를 승인하지 않아요.\n'
    else:body+='**내용 검수 기록은 아직 없어요. 사실 충실성·간접 방해 무시율은 미확정이에요.**\n'
    for row,path in [(base,run/'base/predictions.jsonl'),*[(e,run/f"epoch-{e['epoch']}/evaluation/predictions.jsonl") for e in epochs]]:
        shutil.copyfile(path,out/(row['tag']+'_predictions.jsonl'))
    if a.http:
        http=Path(a.http)
        for name in ['http_records.json','http_summary.json']:shutil.copyfile(http/name,out/name)
        body+='\n## 실제 HTTP 서빙 측정\n\n상세 지연·timeout·fallback 및 백엔드는 `http_summary.json`과 raw 기록을 보세요. 클라이언트 상한은 15초/64KiB이며 fallback을 모델 성공에 포함하지 않아요.\n'
        measured=json.loads((http/'http_summary.json').read_text(encoding='utf-8'))
        body+='\n| 모델 | 실제 모델 응답/9 | timeout/9 | 클라이언트 p50 초 | 클라이언트 p95 초 |\n|---|---:|---:|---:|---:|\n'
        for model,s in measured['summaries'].items():body+=f"| {model} | {s['actual_model_response_count']} | {s['timeout_count']} | {s['p50_s']:.3f} | {s['p95_s']:.3f} |\n"
        body+='\n시간제한 fallback의 약 15초를 성공한 모델 응답시간으로 해석하지 않아요. 이 9건은 전체 90건이나 사용자 모집단의 지연 보장이 아니에요.\n'
    if (run/'vram_summary.json').exists():
        v=json.loads((run/'vram_summary.json').read_text(encoding='utf-8'))
        body+=f"\n## 실제 GPU 메모리 표본\n\n학습 PyTorch allocated 최고 {v['training_torch_peak_allocated_mib']:.1f} MiB, reserved 최고 {v['training_torch_peak_reserved_mib']:.1f} MiB예요. 아래는 모델 단독이 아니라 다른 앱·데스크톱도 포함한 GPU 전체 2초 표본이에요. 순간 최고를 보장하지 않아요.\n\n"
        body+='| 구간 | 표본 수 | 전체 GPU 메모리 중앙값 MiB | 표본 최고 MiB |\n|---|---:|---:|---:|\n'
        for phase,s in v['phases'].items():
            m=s['whole_gpu_memory_used_mib']
            if m:body+=f"| {phase} | {s['sample_count']} | {m['median']:.1f} | {m['max']:.1f} |\n"
        body+='\nRAG 두 모델과의 동시 상주 시험은 이 기록에 없어요.\n'
    dump(out/'run_summary.json',selected)
    (out/'README.md').write_text(body,encoding='utf-8',newline='\n')
    dump(out/'artifact_receipts.json',{'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='artifact_receipts.json'},'weights_included':False})
if __name__=='__main__':main()
