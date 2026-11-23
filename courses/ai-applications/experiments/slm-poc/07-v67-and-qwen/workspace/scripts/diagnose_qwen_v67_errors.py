"""Explain observed mismatches using source inputs and training coverage.

Read-only data analysis, not a causal ablation or model-thought trace.
"""
from collections import Counter
import json
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'kaggle/qwen_v67_reranker'))
from common import prepare,epoch_plan,read,read_rows,save,sha

def main():
    out=ROOT/'output/qwen-v67-kaggle-result-review-20261117'
    data=ROOT/'output/qwen-v67-kaggle-prepared/data'
    train=read_rows(data/'train.jsonl');val=read_rows(data/'val.jsonl')
    bad={r['id']:r for r in read(out/'remaining51.json')}
    by_id={r['id']:r for r in val};assert len(bad)==51 and len(val)==221
    positives=Counter((r['output']['action'],r['output']['target_id']) for r in train)
    candidate_presence=Counter((a['action'],a['target_id']) for r in train for a in r['input']['available_actions'] if a['enabled'])
    prepared=[prepare(r) for r in train];training_counts=Counter();seen_negatives=set()
    for epoch in [1,2,3]:
        for i,c,label in epoch_plan(prepared,epoch):
            candidate=prepared[i]['candidates'][c]
            training_counts[(candidate['action'],candidate['target_id'],label)]+=1
            if not label:seen_negatives.add((prepared[i]['id'],c))
    confusion=Counter((r['gold']['action'],r['selected']['action']) for r in bad.values())
    unseen=[r for r in val if positives[(r['output']['action'],r['output']['target_id'])]==0]
    unseen_wrong=[r['id'] for r in unseen if r['id'] in bad]
    draft_mismatches=[];explicit_disabled=[];details=[]
    for identifier,e in bad.items():
        source=by_id[identifier];ctx=source['input'];gold=e['gold'];selected=e['selected']
        gold_offer=next(a for a in ctx['available_actions'] if all(a[k]==gold[k] for k in ['action','target_id']))
        selected_offer=next(a for a in ctx['available_actions'] if all(a[k]==selected[k] for k in ['action','target_id']))
        assert gold_offer['enabled'] and selected_offer['enabled']
        item={'id':identifier,'message':ctx['message'],'gold':gold,'selected':selected,
              'gold_label_reason_NOT_model_reason':source['output']['reason_summary'],
              'training_positive_rows_for_exact_pair':positives[(gold['action'],gold['target_id'])],
              'training_enabled_candidate_occurrences_for_pair':candidate_presence[(gold['action'],gold['target_id'])],
              'gold_offer':gold_offer,'selected_offer':selected_offer,
              'all_allowed_pairs':[{k:a[k] for k in ['action','target_id','reviewed_text']} for a in ctx['available_actions'] if a['enabled']],
              'blockers':ctx['blockers'],'hold_signals':ctx['hold_signals'],'kb_ask_slots':ctx['kb_ask_slots'],
              'source_input':ctx,'source_output':source['output'],'candidate_scores':e['scores']}
        details.append(item)
        if gold['action']=='hold' and selected['action']=='request_draft':
            assert selected_offer['enabled'] and not selected_offer['blocked_by']
            assert not ctx['blockers'] and not ctx['hold_signals']
            draft_mismatches.append(identifier)
            reason=source['output']['reason_summary'].lower()
            if 'not enabled' in reason or 'disabled' in reason:explicit_disabled.append(identifier)
    retrieve_rows=[r for r in val if r['output']['action']=='retrieve_evidence']
    multi_retrieve=[r for r in retrieve_rows if sum(a['enabled'] and a['action']=='retrieve_evidence' for a in r['input']['available_actions'])>1]
    assert all(len({a['reviewed_text'] for a in r['input']['available_actions'] if a['enabled'] and a['action']=='retrieve_evidence'})==1 for r in multi_retrieve)
    margins=[max(x['score'] for x in e['scores'])-next(x['score'] for x in e['scores'] if all(x[k]==e['gold'][k] for k in ['action','target_id'])) for e in bad.values()]
    report={'source_val_sha256':sha(data/'val.jsonl'),'source_train_sha256':sha(data/'train.jsonl'),
        'mistakes':51,'observed_confusions':[{'gold_action':a,'selected_action':b,'n':n} for (a,b),n in confusion.items()],
        'errors_with_no_positive_train_pair':len(unseen_wrong),
        'errors_with_one_or_two_positive_train_rows':sum(1<=positives[(e['gold']['action'],e['gold']['target_id'])]<=2 for e in bad.values()),
        'all_val_no_positive_train_pair':{'n':len(unseen),'wrong':len(unseen_wrong),'correct':len(unseen)-len(unseen_wrong)},
        'hold_to_draft_allowed_in_input_ids':draft_mismatches,
        'label_reason_explicitly_says_disabled_while_input_enables_ids':explicit_disabled,
        'multi_retrieve_rows_with_identical_candidate_descriptions':len(multi_retrieve),
        'retrieve_target_training':[{'target':t,'positive_train_rows':positives[('retrieve_evidence',t)],
            'candidate_train_occurrences':candidate_presence[('retrieve_evidence',t)],
            'actual_positive_exposures':training_counts[('retrieve_evidence',t,1)],
            'actual_negative_exposures':training_counts[('retrieve_evidence',t,0)]}
            for t in sorted({r['output']['target_id'] for r in retrieve_rows})],
        'training_negative_coverage':{'seen':len(seen_negatives),'possible':sum(len(r['candidates'])-1 for r in prepared)},
        'median_wrong_score_margin_not_probability':statistics.median(margins),
        'model_explanation_generated':False,'causal_ablations_run':False,'scores_changed':False,'source_data_changed':False,'test_read':False,
        'interpretation_limits':['Enabled does not mean uniquely optimal: alternative enabled questions are exact-label mismatches, not automatically semantically approved.',
                                 'Coverage and wording are observed risk factors, not isolated proven causes of any individual neural score.',
                                 'The legacy forbidden_retrieve_slots field actually contains product facts needing retrieval, per actions.py and planner.py; it is not a retrieval prohibition.']}
    save(out/'error-diagnosis.json',report);save(out/'51件の入力と判定根拠.json',details)
    lines=['残った51件：何が違い、何まで原因として確認できたか','',
        'モデルは理由文を生成していない。記録は各候補のyes/noスコア。内部の思考理由を再現した説明ではない。',
        '以下は元入力・正解ラベル・候補スコア・実際の学習計画との照合。因果関係を分離した追加実験はしていない。','',
        '観測された違い']
    for (a,b),n in confusion.items():lines.append(f'{a} → {b}: {n}件')
    lines.extend(['','入力と正解理由の食い違い',
        f'保留が正解なのに下書きを選んだ11件では、全件で入力の下書き候補がenabled=true、blocked_by=[]、blockers=[]、hold_signals=[]。',
        f'そのうち{len(explicit_disabled)}件では正解理由が明示的に「not enabled / disabled」と書いている。該当ID：'+', '.join(explicit_disabled),
        '例362-t03：正解理由「根拠未解決なので下書きは許可されない」。実入力は下書きを許可。',
        '例370-t03：発言「資料はまだ来ていない。下書きは保留して」。モデルは下書きを選択。発言に従えない誤りと、状態の不整合が重なっている。',
        '', '学習での対象の偏り',
        f'51件中、正解の行動＋対象IDがtrainの正解例0件だったもの{len(unseen_wrong)}件、1〜2件だったもの{report["errors_with_one_or_two_positive_train_rows"]}件。',
        f'ただし正解例0のvalは計{len(unseen)}件あり、そのうち{len(unseen)-len(unseen_wrong)}件は正解した。「未見なら解けない」とは言えない。',
        'SPF/UVAの照会はtrainの正解例にも有効候補にも0件。成分表などは候補にあっても正解例0件。正負の実露出数はerror-diagnosis.json。',
        '', '候補の説明と一つだけの正解',
        f'複数の調査対象があるval {len(multi_retrieve)}件では、対象が違っても韓国語の説明文は同一。対象ID等から区別する必要がある。',
        '例965-t03：UVA資料も調べてほしいという発言に、モデルはSPF照会を選択。両候補の説明文は同一。対象の読み分けに失敗している。',
        '例990-t01：正解は刃の使用回数の質問、モデルは刃の傷みの質問。両方とも未回答・許可候補。一つの指定順以外を誤りとする採点上の不一致。モデルの質問が実用上不適切とは、この一致採点だけでは確定しない。',
        '', '学習方法の確認',
        '各trainターンにつき正解候補1個、誤候補はepochごとに無作為1個。誤候補同士を全組み合わせで比較する学習ではない。',
        f'3周で実際に使われた異なる誤候補は{len(seen_negatives)}/'+str(sum(len(r['candidates'])-1 for r in prepared))+'個。これがどれだけ誤りを引き起こしたかは未検証。',
        '', '点数は変更しない。170/221のまま。追加学習やtest採点、元データの変更は実行していない。'])
    (out/'間違いの内容と確認できた理由.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
    print(json.dumps({k:v for k,v in report.items() if k not in ['interpretation_limits','retrieve_target_training']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
