"""Verify all100 saved predictions and render the requested50-problem comparison."""
import csv
import json
from collections import Counter
from pathlib import Path
import random
from validate_v67_two_rerankers50_memory import ROOT,OUT,SEARCH,PREPARED,SOURCE,SEED,MODELS,read,save,sha,aggregate

def main():
    protocol=read(OUT/'protocol.json');selection=read(OUT/'selection.json')
    assert sha(ROOT/'scripts/validate_v67_two_rerankers50_memory.py')==protocol['script_sha256']
    assert sha(SOURCE)==selection['source_sha256'] and sha(PREPARED)==selection['prepared_sha256']
    prepared={r['id']:r for r in read(PREPARED)}
    assert random.Random(SEED).sample(sorted(prepared),50)==selection['ids']
    source={r['id']:r for r in [json.loads(line) for line in SOURCE.read_text(encoding='utf-8').splitlines() if line.strip()]}
    flat=[];summaries={};baseline={}
    for repo,dirname,kind,limit in MODELS:
        manifest=read(ROOT/'models'/dirname/'manifest.json')
        assert sha(ROOT/'models'/dirname/'model.safetensors')==manifest['sha256']
        records=[]
        for identifier in selection['ids']:
            result=read(OUT/kind/'cases'/(identifier+'.json'))
            item=prepared[identifier];gold={k:source[identifier]['output'][k] for k in ['action','target_id']}
            assert result['gold']==gold and json.loads(item['context'])==source[identifier]['input']
            if not result.get('error'):
                assert len(result['scores'])==result['candidate_n']==len(item['candidates'])
                assert len(result['candidate_tokens'])==result['candidate_n']
                assert result['all_candidates_fit'] and max(result['candidate_tokens'])<=limit
                for c,s in zip(item['candidates'],result['scores']):
                    assert (c['action'],c['target_id'])==(s['action'],s['target_id'])
                    if kind=='qwen':assert abs((s['details']['yes_logit']-s['details']['no_logit'])-s['score'])<1e-6
                best=max(result['scores'],key=lambda r:r['score'])
                assert result['selected']=={k:best[k] for k in ['action','target_id']}
                assert result['pair_correct']==(result['selected']==gold)
                assert result['action_correct']==(result['selected']['action']==gold['action'])
            else:assert not result['pair_correct'] and not result['action_correct']
            records.append(result)
            flat.append({'model':kind,'id':identifier,'message':source[identifier]['input']['message'],
                'gold_action':gold['action'],'gold_target':gold['target_id'],
                'selected_action':(result.get('selected') or {}).get('action'),
                'selected_target':(result.get('selected') or {}).get('target_id'),
                'pair_correct':result['pair_correct'],'action_correct':result['action_correct'],
                'full_input_fit':result['all_candidates_fit'],'seconds':result['seconds'],
                'peak_torch_allocated_mib':result['peak_torch_allocated_mib'],
                'peak_torch_reserved_mib':result['peak_torch_reserved_mib'],'error':result.get('error','')})
        summary=aggregate(records);saved=read(OUT/kind/'summary.json')
        assert all(saved[k]==v for k,v in summary.items())
        summaries[kind]=saved
    with (OUT/'per-row.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(flat[0]));writer.writeheader();writer.writerows(flat)
    # Same50 reference only; these use a different (window-mean) input method.
    for name in ['public_base_without_our_adapter','old_kotraj_87of120_adapter']:
        rows=[read(ROOT/'output/v67-roberta-internal-val-v1'/name/'cases'/(i+'.json')) for i in selection['ids']]
        baseline[name]={'n':50,'pair_correct':sum(r['pair_correct'] for r in rows),'action_correct':sum(r['action_correct'] for r in rows),
            'scope':'Previously saved window-mean outputs; not new inference and not same input processing as whole-context rerankers.'}
    save(OUT/'verification.json',{'n_per_model':50,'models':2,'source_hashes_verified':True,'weight_hashes_verified':True,
        'seed_selection_verified':True,'saved_score_argmax_and_grades_verified':True,'all_models_same_sample':True,
        'gold_action_distribution':dict(Counter(source[i]['output']['action'] for i in selection['ids'])),
        'same50_old_window_baseline':baseline,'new_training':False,'test_scored':False,
        'notes':'Torch allocator peaks omit CUDA context and non-PyTorch memory. Speed is successful-request latency including all candidate scoring and tokenization.'})
    lines=['v67：同じ任意50件での2モデル検証','',
        'Qwen3-Reranker-0.6Bとdragonkue/bge-reranker-v2-m3-ko。追加学習なし。',
        '内部検証221件のIDを並べ、固定乱数20261116で50件を選択。正解・予測を見て選んでいない。',
        '同じ50件・同じ許可候補を使用。元のinput JSONを全文入力し、分割・切り捨てなし。',
        '各候補1件ずつ、FP16・省メモリSDPA（EFFICIENT_ATTENTION）・同じGPUで順番に採点。Qwenは文章生成せずyes/no出力値を読む。BGEは分類スコアを読む。',
        '正解はデータのaction＋target_idとの完全一致。引数・理由JSONや実ツール実行は対象外。',
        '学習用・test252件は使わず、プロンプト・温度・候補順等を結果で調整していない。','']
    for kind,s in summaries.items():
        lines.extend([s['repo'],f'全文が収まった件数：{s["full_input_fit"]}/50',
            f'行動＋対象ID：{s["pair_correct"]}/50 = {100*s["pair_accuracy"]:.1f}%',
            f'行動名だけ：{s["action_correct"]}/50 = {100*s["action_accuracy"]:.1f}%',
            f'1発言の処理時間中央値：{s["median_seconds_per_request"]:.3f}秒 / 平均：{s["mean_seconds_per_request"]:.3f}秒',
            f'モデル読み込み時間（上記と別）：{s["load_seconds"]:.2f}秒',
            f'ピークGPUメモリ：Torch使用中 {s["peak_torch_allocated_mib"]:.1f}MiB / Torch予約済み {s["peak_torch_reserved_mib"]:.1f}MiB',
            f'エラー：{s["errors"]}件。エラーも分母50に含む。',
            '複数候補のみ：'+str(s['multiple_candidates']),''])
    lines.extend(['GPU：'+protocol['gpu'],
        'メモリの数字はPyTorchの確保量。モデルと推論テンソルを含むが、CUDAコンテキストや他アプリ使用量を含む全VRAMではない。',
        '処理時間はトークン化＋全候補の推論＋CPU転送＋選択。ダウンロード・モデルロード・ディスク記録を除く。',
        '初回v1は7件の後でGPUメモリ逼迫・長時間停滞のため中止。v1は残し、同じ50件を省メモリ設定で全件再採点した。入力・候補・正解・採点規則は変更していない。',
        '同じPCでの一回の測定。GPUの他負荷・温度などを独占制御したベンチマークではない。',
        'Qwen採点開始時にはBGEの重みダウンロード・組立が一部重なった。GPUで2モデルを同時実行してはいない。',
        'このWindowsのTorchにはFlashAttentionがない。QwenのGQAをTransformers標準repeat_kvで等価展開し、省メモリSDPAを利用。FP16の丸め差はあり得る。',
        '最初の7件は旧方式と新方式で選択結果7/7一致。新方式の集計には旧方式の時間・予測を混ぜていない。詳細はinfrastructure-change.json。',
        '', '50件の行動分布：'+json.dumps(dict(Counter(source[i]['output']['action'] for i in selection['ids'])),ensure_ascii=False),
        '', '参考：同じ50件の過去RoBERTa分割入力（別方式・保存結果の再集計）',json.dumps(baseline,ensure_ascii=False,indent=2),
        '', '限界：小さい内部検証サンプル。外部未知会話の精度・医学的正しさ・学習効果・タスク完了率ではない。',
        '全件の入力・候補・正解・生スコア・時間・メモリを残した。個別判定はper-row.csv、元データはselection.jsonから追跡できる。',
        '採点用モデルは終了後にGPUメモリから解放。デモは起動しない。'])
    (OUT/'50件比較_結果と条件.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))
    print('Verified100 judgments, sample and weight hashes; report and per-row CSV saved.')

if __name__=='__main__':main()
