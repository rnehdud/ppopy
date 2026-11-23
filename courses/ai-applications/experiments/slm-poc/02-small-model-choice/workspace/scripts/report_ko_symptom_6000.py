"""Summarize frozen experiment; AI Hub text remains in its private directory."""
import csv,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/ko_symptom_6000_v2'
RUN=ROOT/'output/training/ko-symptom-6000-v1'
DEST=ROOT/'output/ko-symptom-6000-report-v1'
manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
result=json.loads((RUN/'results.json').read_text(encoding='utf-8'))
history=json.loads((RUN/'history.json').read_text(encoding='utf-8'))
reload=json.loads((RUN/'reload_verification.json').read_text(encoding='utf-8'))
private=json.loads((ROOT/'data/processed/aihub_ko6000_local_review_v1/summary.json').read_text(encoding='utf-8'))
rows=[json.loads(x) for x in (DATA/'train.jsonl').read_text(encoding='utf-8').splitlines()]
if DEST.exists():raise FileExistsError('Existing report protected')
DEST.mkdir(parents=True)
qs=sum('?' in r['text'] and bool(re.search('건조|여드름|뾰루지|붉|빨갛|따가|따갑|가려|가렵|간지럽',r['text'])) for r in rows)
lines=['# 韓国語・複数ターン症状記録：6,000判断QLoRA実験','',
 '## 結論','',
 '事前に固定した合成20会話では、6,000判断を最後まで学習したモデルが19/20シナリオに合格し、今回の探索的な90%基準（18/20）を超えた。',
 'これは、人手で独立確認されていない同一作者の小規模な合成会話での結果であり、実会話で90%に達したことは示さない。',
 '発話の意味が似た例もある。実際の会話における独立検証が必要。','',
 '## 学習データ','',
 f"- 6,000判断、発話の種類は{manifest['unique_utterances']}。同じ発話でも対象症状や直前状態を変えた判断を含む。",
 '- 症状に関する合成5,000判断（単一4,000、複数症状500、他人500）。',
 '- KLUE-WoS trainのユーザー発話1,000判断は、キーワードを使った暫定的な「症状を更新しない」例。WoSには症状の正解ラベルはない。',
 '- [KLUE/WoS公開元](https://huggingface.co/datasets/klue/klue)。訓練データの人手レビューは未実施。AI Hubの会話は訓練に使っていない。',
 '- 上記に加えて、開始時アダプターは以前の合成120判断を学習済み。','',
 '## 比較設計','',
 '- 初期モデル：前回のko-decisionアダプター step 60。NF4量子化ベースにQLoRAを継続。',
 '- 6,000判断を1回ずつ学習。4判断/ステップ、1500ステップ。',
 '- 以前から見た11会話を開発用として使い、0・500・1000・1500ステップを評価。シナリオ合格、ターン一致、早いステップの順に選択。',
 '- 新たに用意した20会話45ターンをテスト。過去の学習・開発・今回の学習と発話の完全一致なし。',
 '- 同じ作者の合成文で意味や構文が似る可能性は残る。会話が進むとモデルの状態が変わり、その状態が次ターンに影響する。',
 '- 90%は「20会話のうち全ターンで5症状が完全一致した会話が18以上」と定義。','',
 '## 結果','', '| モデル | 学習した判断 | 全ターン一致会話 | 全症状一致ターン | 症状ごとの一致 |',
 '|---|---:|---:|---:|---:|']
for name,label in [('before','以前のモデル'),('selected','開発用11会話で選択'),('all_6000','6,000判断の最終モデル')]:
    exp=result['experiments'][name];s=exp['heldout']['summary']
    lines.append(f"| {label} | {exp['step']*4} | {s['scenario_passes']}/{s['scenarios']} | {s['state_matches']}/{s['turns']} | {s['field_matches']}/{s['fields']} |")
lines+=['','開発用11会話では、追加前5/11、2,000判断時10/11、4,000判断時9/11、6,000判断時10/11。',
 '同点では早い時点を選ぶ事前ルールにより、開発用で選択されたのは2,000判断時（500ステップ）。',
 'その選択モデルは新しい20会話で15/20、最後まで学習したモデルは19/20だった。',
 '最終モデルも予め比較対象に含まれていたが、この小さなテストでどちらが一般に優れるかは確定できない。','',
 '## 最終モデルの失敗','',
 '「만약 피부가 가렵다면 어떻게 해야 하나요?（もし肌がかゆかったら、どうすればいいですか？）」を、かゆみが現在あると記録した。',
 f'追加学習6,000判断のうち「症状語＋?」に合致する例は{qs}件。症状についての仮定・質問を教える例の欠落が原因候補だが、それだけが原因とは証明できない。',
 '今後は仮定・可能性・一般的説明・本人ではない人の症状を含む例を、人が正解確認したうえで補う。','',
 '## AI Hubでの補助確認（正答率ではない）','',
 '以前に選んだ12会話16ターンで、独立レビュー前の暫定判断と比べた。元会話の相手の発話はモデルに与えていない。',
 f"- 暫定的に必要とされた更新が欠けたターン：追加前 {private['before']['draft_missing_turns']}/16、最終 {private['all_6000']['draft_missing_turns']}/16。",
 f"- 暫定的に許可されていない更新があったターン：追加前 {private['before']['draft_unsupported_turns']}/16、最終 {private['all_6000']['draft_unsupported_turns']}/16。",
 'これは偏って選んだ未確認ラベルとの比較であり、AI Hubにおける正答率ではない。原文入り結果はローカル限定。','',
 '## 保存と制限','',
 'モデルのSHA-256とデータのハッシュを照合し、全6,000判断を処理。別プロセスでアダプターを再読込し、各ターンの判断を再現。',
 '製品使用、使用時刻、症状開始日、STT、ツール選択、回答生成、実運用における安全性は対象外。',
 '90%を実会話の成績として言う前に、人が確認した新しい複数ターン会話で評価する。']
(DEST/'結果.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
variants=result['experiments'];csvrows=[]
for b,s,f in zip(variants['before']['heldout']['cases'],variants['selected']['heldout']['cases'],variants['all_6000']['heldout']['cases'],strict=True):
    if not b['id']==s['id']==f['id']:raise ValueError('case mismatch')
    for index,(x,y,z) in enumerate(zip(b['turns'],s['turns'],f['turns'],strict=True),1):
        if not x['input']==y['input']==z['input'] or not x['expected']==y['expected']==z['expected']:raise ValueError('label mismatch')
        csvrows.append({'case':b['id'],'turn':index,'input_ko':x['input'],'expected_not_human_reviewed':json.dumps(x['expected'],ensure_ascii=False),
          'before':json.dumps(x['after'],ensure_ascii=False),'before_match':x['matches'],
          'selected_2000':json.dumps(y['after'],ensure_ascii=False),'selected_match':y['matches'],
          'final_6000':json.dumps(z['after'],ensure_ascii=False),'final_match':z['matches']})
with (DEST/'synthetic_test_turns.csv').open('x',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=csvrows[0].keys());w.writeheader();w.writerows(csvrows)
print('Created report:',len(csvrows),'turns')
