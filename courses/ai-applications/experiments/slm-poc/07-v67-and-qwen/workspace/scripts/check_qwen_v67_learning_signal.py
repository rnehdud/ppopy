"""Data-only check of used fields and changes in saved candidate logits."""
from collections import Counter
import copy
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'kaggle/qwen_v67_reranker'))
from common import prepare,read,read_rows,save,epoch_plan

def main():
    out=ROOT/'output/qwen-v67-kaggle-result-review-20261117'
    data=ROOT/'output/qwen-v67-kaggle-prepared/data'
    checks={}
    for split in ['train','val']:
        rows=read_rows(data/(split+'.jsonl'));unchanged=0
        for source in rows:
            changed=copy.deepcopy(source)
            changed['output']['reason_summary']='COMPLETELY REPLACED LABEL REASON FOR FIELD-USAGE CHECK'
            assert prepare(changed)==prepare(source)
            unchanged+=1
        checks[split]={'rows':len(rows),'prepared_model_inputs_candidates_and_targets_unchanged_after_reason_rewrite':unchanged}
    phases={p:[read(f) for f in (out/'evidence'/p).glob('*.json')] for p in ['baseline','epoch-03']}
    scores={}
    for action in ['ask_user','confirm_candidate','retrieve_evidence','resolve_conflict','hold','request_draft']:
        scores[action]={}
        for phase,rows in phases.items():
            positives=[];negatives=[]
            for row in rows:
                for candidate in row['scores']:
                    if candidate['action']!=action:continue
                    positive=all(candidate[k]==row['gold'][k] for k in ['action','target_id'])
                    (positives if positive else negatives).append(candidate['score'])
            scores[action][phase]={'reference_selected_candidate_n':len(positives),
                'reference_selected_score_median':statistics.median(positives) if positives else None,
                'reference_unselected_candidate_n':len(negatives),
                'reference_unselected_score_median':statistics.median(negatives) if negatives else None}
    result={'reason_field_check':checks,'saved_score_medians':scores,
        'all_reference_scores_are_yes_minus_no_logits_not_probabilities':True,
        'no_new_model_execution':True,'source_data_changed':False,'test_read':False,
        'causal_claim':'Changing reason_summary alone cannot alter the prepared inputs or training targets in this runner. Score movement is observed; the loss causing specific errors is not isolated by this analysis.'}
    save(out/'学習に使った情報とスコア変化.json',result)
    text='''次の作業の判断

先に正解理由を一括書き換えたり、学習回数だけ増やしたりしない。

根拠1：この学習器は正解理由の文章を入力にも損失にも使っていない。
実データ全2201件のreason_summaryをメモリ上だけで全く別の文章に置換し、prepareの結果を比較した。
train1980/1980、val221/221で入力・候補・正解ペアが同じだった。元ファイルは変更していない。
従って、理由文だけを直して同じ学習を実行しても、修正した説明はモデルへ届かない。

根拠2：調査を選ぶ正解候補のスコアが落ちている。
同じval22件の正解retrieve_evidence候補のyes-minus-no値の中央値：4.93359375 → -3.35546875。
非正解の調査候補も下がっているため、単に「調査が全部分からなくなった」とは断定しない。
正解の調査候補も、別の行動候補との順位で負けている状況を確認した。
これは生のスコアで、確率やモデルの内部説明ではない。

次に比較する条件
・対照：現在の「参照正解yes、別候補no」を教える。
・比較：同じ場面の正解候補が、同じ場面の比較候補より高くなるように教える。
・使うtrain、val221、初期モデル、正例と比較候補、順序、学習量をそろえる。
・比較候補の提示方法を組み替える場合は対照も同じ形で再実行し、過去170/221だけを対照として流用しない。
・元データの修正はこの比較に混ぜない。明確な矛盾2件は別途レビュー対象として残す。
・評価は全valの行動＋対象ID、調査22件の一致、正解から不正解へ変わった件数を併記する。
・90%超を目標として残す。ただしこの変更で達成できるとはまだ判断できない。
・testを開かない。Kaggleで比較する場合、アップロードと実行はユーザーが行う。

今回ここで行ったこと
・保存済みデータとスコアの解析のみ。新しいモデルの推論・学習・Kaggle実行はしていない。
・このファイルは比較方針であり、次のKaggle実行コードを作成済みという意味ではない。
'''
    (out/'次の比較を選ぶ根拠.txt').write_text(text,encoding='utf-8-sig')
    print(result['reason_field_check'])
    print('retrieve:',scores['retrieve_evidence'])

if __name__=='__main__':main()
