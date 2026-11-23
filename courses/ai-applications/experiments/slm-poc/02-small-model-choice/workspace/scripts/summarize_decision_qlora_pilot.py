"""Write a reproducible, explicitly exploratory two-model comparison."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'output/decision-qlora-comparison-v1'
names={'ko':'ko-decision-qlora-v1','exaone':'exaone-jev-qlora-v1'}
reports={}
for key,name in names.items():
    p=ROOT/'output/training'/name
    reports[key]={f:json.loads((p/(f+'.json')).read_text(encoding='utf-8')) for f in ['config','baseline','trained','reload_verification','history']}
DEST.mkdir(parents=True,exist_ok=False)
data=ROOT/'data/processed/ko_decision_qlora_pilot_v1'
manifest=json.loads((data/'manifest.json').read_text(encoding='utf-8'))
labels={'ko':'ko-decision','exaone':'EXAONE-JEV'}
lines=['# QLoRA 症状判断：2モデルの探索的比較','',
 '## 範囲と手順','',
 '韓国語の症状5種類について、現状態と新しい発話から present / absent / unchanged / unknown の4択を予測する。',
 '予測は同一の SymptomSession.update に渡す。JSON生成、ツール選択、製品、時刻、STT、医療判断や実利用の検証ではない。',
 '今回はアシスタントが作成した合成テンプレートを使用し、独立した人手ラベルレビューはない。AI Hub実データは不使用。',
 f"train {manifest['splits']['train']}判断から最初の120判断を学習（60ステップ×2判断）、別テンプレートのvalidation {manifest['splits']['validation']}判断を使用。",
 '候補は20、40、60ステップ。validationの正解数で選び、同点では早いステップを採用。テストは選択に使っていない。',
 '新規holdoutは8シナリオ10ターン。別に過去使用済みdevelopmentは11シナリオ15ターン。',
 '120学習判断は55種類の発話、120 validation判断は32種類の発話で、直前状態を変えた重複が含まれる。',
 'trainとvalidationに発話の完全一致はないが同じ作者の合成文で、表現・タスクは似ている。8シナリオの結果は一般化精度ではない。',
 '同じモデルの前後をNF4量子化・同じテンプレート・同じ固定順序・同じ更新器で比較。',
 '前回報告のCPU FP32 / 正逆順平均とは方式が異なるため、数値を直接比較しない。',
 '一部の複数ターンでは前の誤更新によって学習前後で後続の入力状態が異なる。','',
 '## 結果：新規holdout','','| モデル | 段階 | 全条件合格シナリオ | 状態完全一致ターン | 5症状の一致数 | 不明をなしにした項目 |',
 '|---|---|---:|---:|---:|---:|']
for key in names:
    for phase,obj in [('前',reports[key]['baseline']),('後',reports[key]['trained'])]:
        s=obj['heldout']['summary']
        lines.append(f"| {labels[key]} | {phase} | {s['scenario_passes']}/{s['scenarios']} | {s['state_matches']}/{s['turns']} | {s['field_matches']}/{s['fields']} | {s['unknown_to_absent']} |")
lines+=['','## 以前から使用済みのdevelopment','','| モデル | 全条件合格 前→後 | 状態完全一致ターン 前→後 |', '|---|---:|---:|']
for key in names:
    b=reports[key]['baseline']['development']['summary'];a=reports[key]['trained']['development']['summary']
    lines.append(f"| {labels[key]} | {b['scenario_passes']}/{b['scenarios']} → {a['scenario_passes']}/{a['scenarios']} | {b['state_matches']}/{b['turns']} → {a['state_matches']}/{a['turns']} |")
lines+=['','## validation と選択された重み','','| モデル | 学習前 | 選択時 | 選択ステップ |',
        '|---|---:|---:|---:|']
for key in names:
    r=reports[key];base=r['baseline']['validation'];selected=r['trained']['selected']
    lines.append(f"| {labels[key]} | {base['correct']}/{base['n']} | {selected['validation']['correct']}/{selected['validation']['n']} | {selected['step']} |")
lines+=['','validationは同じ作者が別テンプレートで生成したため、100%は実会話での高性能を意味しない。',
        '両モデルともNF4ダブル量子化、fp16計算、LoRA r=8 / alpha=16、学習率0.0002。',
        'ko-decisionはquery/valueのLoRAと4候補スコアのクロスエントロピー、元の分類ヘッドは固定。',
        'EXAONE-JEVはq_proj/v_projのLoRAとA〜Dの回答トークンのスコアに対するクロスエントロピー。',
        '未学習項目や会話能力の保持、学習率・乱数の違いは測定していない。',
        'EXAONE-JEVの公開モデルは英語のみとされ、独自ライセンスで研究・教育用途に制限される。','',
        '## 失敗した新規holdout例','']
for key in names:
    for c in reports[key]['trained']['heldout']['cases']:
        for t in c['turns']:
            if not t['matches']:
                lines.append(f"- {labels[key]} / {c['id']}: {t['input']} 期待 `{json.dumps(t['expected'],ensure_ascii=False)}` → 実際 `{json.dumps(t['after'],ensure_ascii=False)}`")
lines+=['','## 保存と確認','',
 '2つのアダプターは独立プロセスでNF4ベースに再読込し、保存済みholdout予測と一致。アダプター無効時の基準予測も一致。',
 'モデル重みのSHA-256を検証し、学習はLoRA以外を凍結。勾配が非ゼロかを各ステップ確認。',
 'EXAONEのトークナイザーは公開tokenizer.jsonを同一利用し、train+validation全360プロンプトのID列を別環境と照合。',
 '学習コードは同一の出力先を上書きしない。モデル・データ・アダプターはローカルに保存。','',
 '## 結論','','今回の小規模な合成スキンケア例では、QLoRA後に両モデルの状態完全一致が改善した。',
 'ただし自然な韓国語の実会話、製品使用、開始時期、ツール選択に対する改善や、実用可能性は未確認。',
 '本人と他人の区別・複数症状・曖昧な否定の失敗が残り、無確認の自動保存には使わない。',
 '次は人が確認した正解と未使用会話を用い、教師データ品質と誤更新を検証する。']
(DEST/'結果.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
rows=[]
for key in names:
    b=reports[key]['baseline']['heldout']['cases'];a=reports[key]['trained']['heldout']['cases']
    for bc,ac in zip(b,a,strict=True):
        if bc['id']!=ac['id']:raise ValueError('case mismatch')
        for i,(x,y) in enumerate(zip(bc['turns'],ac['turns'],strict=True),1):
            if x['input']!=y['input'] or x['expected']!=y['expected']:raise ValueError('label mismatch')
            rows.append({'model':labels[key],'case':bc['id'],'turn':i,'text_ko':x['input'],
              'expected_unreviewed':json.dumps(x['expected'],ensure_ascii=False),
              'base_before':json.dumps(x['before'],ensure_ascii=False),'base_after':json.dumps(x['after'],ensure_ascii=False),'base_match':x['matches'],
              'trained_before':json.dumps(y['before'],ensure_ascii=False),'trained_after':json.dumps(y['after'],ensure_ascii=False),'trained_match':y['matches']})
with (DEST/'holdout_turns.csv').open('x',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('Wrote report and',len(rows),'heldout turn records')
