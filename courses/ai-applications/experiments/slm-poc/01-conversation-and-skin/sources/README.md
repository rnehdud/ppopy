# 韓国語Qwen Stateful Agent MVP

## 実験履歴・現在地（2026-11-13更新）

このREADMEの下部は初期Qwen試作の記録です。以後の選択モデル、長文、2モデル、連続実行、xLAM、固定kotrajの結果は、次の履歴にまとめています。

- [実験履歴：変更・結果・制限・根拠を検索](output/experiment-history-20261113/index.html)
- [比較表CSV](output/experiment-history-20261113/comparison.csv) / [説明TXT](output/experiment-history-20261113/history.txt) / [資料とハッシュの索引](output/experiment-history-20261113/sources.json)
- 更新：`.\.venv-train\Scripts\python.exe scripts/build_experiment_history.py`。報告ファイルの追加・変更・消失を記録します。モデルの学習・推論・API呼び出しはしません。

現在の判定対象は固定kotrajの**ツール名と引数値の完全一致**です。監視val240の対照は111/240、呼ぶ95/160、呼ばない16/80。全val6365判断は556判断までの途中結果、固定test5871判断は未採点。全valとtestで90%を超える条件は未達です。

旧選択モデルの87/120、症状19/20、限定した連続実行28/30（正しい症状情報を渡す条件は30/30）は、採点対象が異なります。同じ正解率の推移としてつなぎません。EXAONE API用Webデモの機能検査も、学生自身が学習したモデルの精度とは分けています。

---

> 第1段階のGGUF最小Agentと、次段階のNF4 QLoRA実験は別構成です。
> 以下の旧GGUF評価値を、新しいNF4モデルの学習前後差として比較しないでください。

追加学習前の **Qwen2.5-3B-Instruct** で、韓国語の会話から状態を更新し、
ツールを実行して結果を回答へ反映する最小実験です。
別途構築中のスキンケアKBとは独立して動き、検索先には明示的な合成fixtureを使います。
STT・Jev・QLoRA学習・製品DBは、この段階では実装していません。

## 構成

```text
韓国語入力 + 最新session_state + tools
    -> Qwen2.5-3B-Instruct（公式GGUF / Q4_K_M / LoRAなし）
    -> 構造化tool call
    -> 引数検証 -> Python関数実行 -> 状態更新 / 合成KB検索
    -> tool結果と最新状態をQwenへ戻す -> 韓国語回答
```

- `update_session_state`：明示された症状・重症度・使用時点・使用有無・症状開始をpatch更新。
- `search_knowledge_base`：Qwenが生成したquery・症状・使用時点で合成文書を検索。
- バックエンドに韓国語から正解ラベルを作るルールや正解引数の代入処理はありません。
- 状態はセッション内メモリで保持。会話、モデル応答、実際の引数・結果、状態差分はJSONLへ保存します。
- 推論には最新の明示状態と現在ターン内の会話・tool結果を渡します。古い値が残る全履歴はトレースに保持しますが、毎回の推論へ再投入しません。このMVPでは状態にない長期的な会話内容は保持しません。
- 検証器は型・許可ツール等を確認しますが、モデルの意味理解が正しいかは独立した期待値で評価します。
- 2つのツールに絞るため、元の7項目のうちintent・routine_change_requestedは未実装です。

## 環境

実装時のPCはWindows、Python 3.14、RTX 4070 Laptop（VRAM 8GB）です。
CPU版PyTorchを変更せず、既存のJan同梱GPU対応`llama-server.exe`を利用します。
他環境では、信頼できるllama.cppのWindows CUDA実行ファイルを`-ServerPath`で指定してください。

```powershell
python -m pip install -r requirements.txt
python scripts/download_agent_data.py
python scripts/setup_qwen.py
python scripts/prepare_qwen_data.py
```

ダウンロードは公開URLを使用し、APIキーは不要です。モデル約2.1GBとデータ約65MBを取得します。
取得元revision、モデルSHA256、データSHA256はローカルmanifestに記録します。
モデル・原データ・整形データは`.gitignore`で除外しています。

## Agentを動かす

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_qwen.ps1
# モデルロード後、healthがokになることを確認
Invoke-RestMethod http://127.0.0.1:18080/health
python scripts/run_agent.py --demo
```

`--demo`なしでは対話入力できます。終了は`/quit`です。

```powershell
python scripts/run_agent.py
```

停止してGPUメモリを解放する場合：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen.ps1
```

サーバーは127.0.0.1だけで待ち受けます。ブラウザ操作や外部APIサービスは使いません。
実行エンジンの場所を明示する場合：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_qwen.ps1 -ServerPath 'C:\path\to\llama-server.exe'
```

## データ整形

入力は`data/raw/glaive-function-calling-v2-ko/train.json`。
拡張子はjsonですが、実体はJSON Linesです。

変換内容：

1. `conversations_ko`を使用し、英語会話は分割用の由来IDとして利用。
2. 連結JSONの関数定義を`tools`配列へ変換。
3. `function-call`を`assistant.tool_calls`へ、`function-response`を`tool`へ変換。
4. 文字列のargumentsをJSON object化。閉じたリテラルと既知のラッパーだけを解釈し、`eval`は使用しない。
5. 未定義ツール、不正な型、必須引数欠落、応答欠落等は理由付きで除外。値・結果を推測して補わない。
6. 正規化後の完全重複を除き、原対話のSHA256で90/5/5に分割。
7. 公式Qwen tokenizerの`apply_chat_template(messages, tools=...)`を全採用例で実行。
8. トークン長を記録。長い例は切り捨てず、`eligible_2048`で識別。

出力先：`data/processed/qwen_tool_use/`

- `train.jsonl` / `validation.jsonl` / `test.jsonl`
- `preparation_report.json`：採用・除外・系列長等
- `rejected.jsonl`：元行番号と除外理由
- `rendered_samples.json`：実際のQwenテンプレート出力例

今回の整形結果は採用14,609件、除外561件です。内訳はtrain 13,074件、validation 812件、test 723件。
トークン数の中央値494、P95 1,463、最大2,070。2,048超の2件も切り捨てず保持しています。

出力は`messages + tools`形式です。追加した学習ジョブとassistant-only損失マスクは後述の小規模QLoRA節を参照してください。
構造検証は翻訳・意味の全件監査ではありません。また、元データには独自Agentの状態ラベルはありません。
この一般ツール使用データだけで状態追跡を学習できるとは主張しません。
Kakao FunctionChat-Benchは`data/raw/functionchat-bench/`に分離し、整形・学習へ混ぜません。

## 実モデルの動作評価

```powershell
python scripts/evaluate_agent.py --run-name baseline-new
```

既に使ったrun-nameは上書きせずエラーにします。別の名前を指定してください。
最小3ターンの動作確認だけを行う場合：

```powershell
python scripts/evaluate_agent.py --run-name smoke-new --scenarios data/fixtures/smoke.json
```

10の開発シナリオを実Qwenで実行します。通常入力、訂正、否定、使用なし、複数症状、
ツール不要、曖昧な依頼、同一発話＋異なる初期状態、KB障害を含みます。
期待値は評価器だけが読み、モデルには渡しません。

- `output/runs/<run-name>/results.json`：全ケースの期待値・予測・判定
- `output/runs/<run-name>/turns.csv`：ターン別の結果
- `output/runs/<run-name>/*.events.jsonl`：モデルの生応答と実ツール実行
- `output/runs/<run-name>/run_metadata.json`：プロンプト・ツール仕様・ソースhash・モデルrevision
- `output/runtime/`：サーバー設定・標準出力・標準エラーログ

この10件は開発デモ用です。プロンプト調整にも使用するため、未知データでの一般化精度ではありません。
合成KBの検索が動いても、実KBの検索品質や医学的妥当性を検証したことにはなりません。
将来QLoRAと比較する場合は、同じ量子化・プロンプト・実行基盤を揃えて独立したholdoutを用意します。

### 実行済みの結果（2026-11-04）

| 対象 | 結果 | 記録 |
|---|---|---|
| 最小デモ：記録 → 使用時点訂正 → 最新状態で検索・出典回答 | 3/3ターン成功 | `output/runs/smoke-final/` |
| 広めの開発テスト | 4/10シナリオ、6/14ターンが全条件合格 | `output/runs/verification-final/` |
| データ・状態・実行契約のユニットテスト | 8件成功 | `tests/test_contracts.py` |

結論は「最小ステートフルAgentは実際に動いたが、学習前3Bモデルの意味判断はまだ不安定」です。
確認した失敗は、症状開始日と使用日の混同、否定された症状の誤登録、未言及の開始日の推測、
一部入力での空応答、検索後の文書ID省略です。回答に根拠のない因果表現が混じることもあり、
このMVPの自由文を実際のスキンケア助言として利用しません。

同一発話を異なる初期状態で実行した2ケースは、異なる正しい検索引数が実際に生成されました。
ただし文書IDの回答省略でシナリオ全体は不合格です。部分成功を全成功として数えていません。
最小デモは、複数の日付を含む広めのケースより単純な開発例です。両方の成績を残しています。

過去のpilotやbaselineも残していますが、プロンプトや履歴投入方針が異なり、スコアを単純比較できません。
`verification-final`と`smoke-final`は最初の学習前MVPの記録です。追加実験は後述の固定評価・小規模QLoRA節に分離します。

## 契約のテスト

```powershell
python -m unittest discover -s tests -v
```

安全なデータパース、実行しない不正データ、ツール定義／引数整合、結果の欠落、
状態patchの原子性とセッション分離を確認します。モックモデルを実モデルの成功として数えません。

## 参照先

- 学習パイプラインの参考：<https://github.com/DdingDDing0103/koculture-slm-finetuning>
- 公式モデル：<https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF>
- 韓国語データ：<https://huggingface.co/datasets/heegyu/glaive-function-calling-v2-ko>
- 評価用：<https://github.com/kakao/FunctionChat-Bench>
- Qwen tool calling：<https://qwen.readthedocs.io/en/v2.5/framework/function_call.html>

モデルのライセンス表記はqwen-research、学習候補データのカードはApache-2.0です。
元のREADME・LICENSE・NOTICE等を取得データと一緒に保存しています。

## 次段階：固定評価と小規模QLoRA

データ定義は`data/stateful/v2/README.md`を参照してください。
学習用209シナリオ（529判断例）、検証用30シナリオ、固定評価用59シナリオを用意しています。
これは合成データによる、表現テンプレートを分けた制御実験です。実音声の一般化評価ではありません。

この段階ではUnslothが公開するQwen2.5-3B-InstructのNF4 repackを使います。
UnslothのPython実行パッケージやremote model codeは使用しません。
NF4で学習・検証loss・保存・再読込を確認します。WindowsのNF4生成が低速だったため、
閉ループAgent評価は同一の公式Q4_K_M GGUFと同一llama.cpp実行系で、アダプターなし／ありを比較します。
NF4学習済みLoRAを公式llama.cppの変換器でF32 GGUFへ変換して適用します。
NF4そのものの閉ループ精度評価や、以前の10件の開発スコアとの直接比較ではありません。
元モデルの利用条件が、repackのカード表記だけで変わると解釈しないでください。

```powershell
# 元のCPU版PyTorchは変更せず、Python 3.11の分離環境を作る
powershell -ExecutionPolicy Bypass -File scripts/bootstrap_training.ps1
python scripts/download_nf4_model.py
python scripts/prepare_stateful_training.py
.venv-train/Scripts/python.exe scripts/check_loss_alignment.py

# 最初にアダプターなしで固定59件を評価（出力先は未使用名を指定）
powershell -ExecutionPolicy Bypass -File scripts/start_qwen.ps1
python scripts/evaluate_frozen_gguf.py --phase before --output output/training/gguf-holdout-before-new

# GPUメモリを解放するため、自分の試験用GGUFサーバーだけ停止
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen.ps1
.venv-train/Scripts/python.exe scripts/train_stateful_smoke.py --run-name qlora-smoke-new
```

設定は`configs/qlora_smoke.json`です。状態・行動100判断例と公開韓国語ツール使用20判断例を使い、
固定された小規模の学習・保存・再読込を試します。checkpointやハイパーパラメーターをholdoutで選びません。
全層の重みではなく、NF4の凍結ベース上でq_proj/v_projのLoRAだけを更新します。

マスク付き因果言語損失と等価な、教師位置だけの語彙射影を利用してVRAMを抑えます。
数式の損失値と勾配の等価性は`check_loss_alignment.py`で確認します。

出力先：`output/training/<run-name>/`、アダプター：`adapters/<run-name>/`。
モデルの生出力、実行結果、固定データhash、採用した学習例ID、GPU環境、学習lossを保存します。
学習用環境は`.venv-train`で、既存のPython 3.14の推論環境とは分離しています。

保存済みアダプターを動かす場合：

```powershell
.venv-train/Scripts/python.exe scripts/run_hf_agent.py --adapter adapters/qlora-smoke-new --demo
```

高速GGUF経由で実行・比較する場合（学習プロセス終了後）：

```powershell
# 公式llama.cpp変換器。今回の実行に固定したcommit
git clone --filter=blob:none --sparse https://github.com/ggml-org/llama.cpp.git tmp/llama-converter
git -C tmp/llama-converter checkout 4c4ca5b18854c973655a62a6164a3ae930ee76b0
git -C tmp/llama-converter sparse-checkout set conversion gguf-py
# uvの場所はbootstrap_training.ps1と同じ。ggufはこの固定ソースから導入
$trainingUv = Join-Path $env:LOCALAPPDATA 'Programs/Jan/uv.exe'
& $trainingUv pip install --python .venv-train/Scripts/python.exe ./tmp/llama-converter/gguf-py
.venv-train/Scripts/python.exe tmp/llama-converter/convert_lora_to_gguf.py --base models/qwen2.5-3b-instruct/tokenizer --outfile adapters/qlora-smoke-new/adapter-f32.gguf --outtype f32 adapters/qlora-smoke-new
powershell -ExecutionPolicy Bypass -File scripts/start_qwen.ps1 -LoraPath adapters/qlora-smoke-new/adapter-f32.gguf
python scripts/evaluate_frozen_gguf.py --phase after --output output/training/gguf-holdout-after-new
python scripts/run_agent.py --demo
```

既存の`tmp/llama-converter`があればcloneは不要です。
`run_agent.py`は現在起動中のGGUFサーバーを利用します。学習済みアダプターは自動適用されず、
サーバー起動時の`-LoraPath`で指定します。`output/runtime/server_config.json`で確認できます。

### 追加実験の実測結果（2026-11-04）

| 指標 | 学習前 | 小規模QLoRA後 |
|---|---:|---:|
| 固定59シナリオの全条件合格 | 20/59 (33.9%) | 42/59 (71.2%) |
| 84ターンの全条件合格 | 39/84 | 57/84 |
| 応答・実行の完了 | 55/84 | 84/84 |
| 5フィールド状態の完全一致 | 71/84 | 58/84 |
| product_used一致 | 73/84 | 59/84 |
| usage_time一致 | 84/84 | 76/84 |
| NF4検証loss（20判断例） | 1.592306 | 0.114952 |

**実行可能性は確認できましたが、状態抽出の品質は悪化しました。**
空応答や検索・出典応答の失敗が減ったためシナリオ合格数は増えています。
一方、使用有無の省略や使用時間の誤りが増えており、全体的な品質改善とは結論しません。
同じ59件で27件が不合格→合格、5件が合格→不合格でした。人が収集・検証した一般化評価ではありません。

学習は120判断例・60 optimizer steps、LoRA学習パラメーター1,843,200、所要約298秒でした。
PyTorchが記録した学習ピーク割当メモリは約3.075 GiB（GPU全体の使用量ではありません）。
`qlora-smoke-v3`の保存直後、ログ関数の引数名衝突で終了しました。保存済み重みと60ステップ完了ログから
`scripts/verify_saved_training.py`で検証のみ再開し、再学習はしていません。
保存済みアダプターの独立2回ロードで生成probeが一致しました。保存前メモリとの同一性は未記録です。
`qlora-smoke-v1/v2`は途中失敗・中断の記録で、今回の結果には混ぜていません。

- 韓国語TXT報告：`output/stateful_qlora_results_ko.txt`
- 比較・5カテゴリの失敗詳細：`output/stateful_qlora_comparison.json`
- 全59件の正解・予測・判定・生ログ：`output/training/gguf-holdout-before/` と `gguf-holdout-after/`
- 学習・保存・検証記録：`output/training/qlora-smoke-v3/`
- 保存済みPEFT/F32 GGUFアダプター：`adapters/qlora-smoke-v3/`

韓国語報告を再生成する場合：

```powershell
python scripts/summarize_qlora.py --run-name qlora-smoke-v3
```

次は独立した人の韓国語ラベル検収、使用有無・時点の教師例の見直し、実KBのツール契約接続です。
観測済みholdoutに合わせて調整する場合、次の性能判定には新しい未使用testを用意します。

## Qwen3未学習Agentとラベル点検

Qwen3-4B-Instruct-2507のQ4_K_M GGUF（Unslothによる量子化、追加学習なし）を使用します。
既存の状態管理、2つのツール、入力プロンプト、評価基準は変更しません。
Qwen3用の公式チャットテンプレートを使用するため、以前のQwen2.5用サーバーとは別に起動します。
比較は既に観測済みの合成59シナリオであり、未使用データに対する性能ではありません。

```powershell
# 初回のみ約2.5GBのモデルを取得し、SHA256を検証
python scripts/setup_qwen3.py
# GPUメモリを解放するため、本プロジェクトのQwen2.5サーバーを使用中の場合は停止
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen.ps1
powershell -ExecutionPolicy Bypass -File scripts/start_qwen3.ps1
python scripts/evaluate_qwen3.py --output output/runs/qwen3-baseline-new
python scripts/run_qwen3_agent.py
# 終了時
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen3.ps1
```

実験の記録には、モデルの元レポジトリ・revision・hash、プロンプト・ツール・評価器のhashを保存します。
Qwen2.5 3BとQwen3 4Bは、モデル規模・tokenizer・テンプレート・GGUF提供者が異なります。
同じQ4_K_Mですが、純粋にアーキテクチャだけの比較ではありません。

`output/state_review_v2_ready/`に、train / validation / 観測済みholdoutを分けた人手レビュー表を用意しました。
先に`README.txt`と`priority_review_observed_only.csv`を確認できます。
表は全行「未確認」で、モデルの誤り・文法候補は人間の承認済みラベルではありません。

点検で見つかった要確認点：

- 学習用の製品使用有無を明示的に更新するターンは35件（yes 30 / no 5）。偏りを含みます。
- 韓国語の助詞について、train 18ターン、validation 1ターン、holdout 1ターンに機械的な確認候補があります。
- 「今日症状がある」と「今日発症した」は異なるのに、既存のSYSTEMと一部のno_productラベルは同一視します。
  train 4件・validation 3件を優先レビューとして挙げています。元のラベルは変更していません。

ラベルの最終判断は独立した韓国語話者による確認が必要です。
観測済みholdoutの修正や学習への流用を行う場合は、新しい未使用テストを用意してください。

### Qwen3未学習モデルの実測

| 指標 | Qwen2.5 3B 学習前 | Qwen3 4B 学習前 |
|---|---:|---:|
| 全条件合格シナリオ | 20/59 | 41/59 |
| 実行されたターンでの全条件合格 | 39/84 | 55/83 |
| 実行されたターンでの5項目完全一致 | 71/84 | 56/83 |
| product_used一致 | 73/84 | 69/83 |
| usage_time一致 | 84/84 | 69/83 |
| skin_condition一致 | 82/84 | 66/83 |

Qwen3では1ケースの1ターン目に、ツール結果後のレスポンスがサーバーの構文解析エラー（HTTP 500）となり、
その次のターンは未実行です。実行ターン数の違いを分母に明記しています。
状態一致にはエラー時も含みます。状態が正しく保持されても、そのターンの処理成功を意味しません。
シナリオ全体成功は増えた一方で、状態フィールドの完全一致は減ったため、一律に性能向上とは判断しません。
Qwen3の失敗ターン28件は `output/state_review_v2_ready/qwen3_failures_review.csv`、
全ログは `output/runs/qwen3-baseline-v1/` に保存しています。
値を未言及の場合の扱いや正解ラベル自体に要レビュー点があるため、数字を一般性能と解釈しないでください。

## KLUE-WoSでのQwen3状態追跡 学習実験

公開のKLUE WoSの元データは `data/raw/klue_wos/` に保存しています（CC BY-SA 4.0）。
出典: <https://huggingface.co/datasets/klue/klue>。旅館・飲食店等の状態であり、肌の情報ではありません。
`scripts/prepare_klue_experiment.py` は同一会話から1ユーザーターンを選び、
「直前の正解状態＋直前のシステム応答＋現在のユーザー発話→次の完全状態JSON」に変換します。
教師あり学習用200例、検証損失用40例、動作比較用60例を会話単位で分離しています。
元データの正解状態をそのまま用い、化粧品用ラベルや架空のツール呼び出しは生成しません。
これは**直前の正解状態を与える単一ターン評価**であり、対話全体を自律的に追跡した評価ではありません。

固定例は `data/processed/klue_wos_pilot_v1/`、出典・SHA・分割は同フォルダーの `manifest.json`。
実行済みの固定データを上書きせず、変更には新しいバージョンが必要です。
学習はUnslothによるNF4のQwen3-4B-Instruct-2507でLoRA重みのみ更新します。
同じQ4_K_M GGUFにアダプターを付ける前後の60例で比較します。NF4とは量子化が異なります。

```powershell
python scripts/inspect_klue_wos.py       # 公開原本の取得・SHA検証
python scripts/download_qwen3_nf4.py      # 学習用モデル（約2.65GB）
# prepareは既存の固定出力を上書きしない
python scripts/prepare_klue_experiment.py
powershell -ExecutionPolicy Bypass -File scripts/start_qwen3.ps1
python scripts/evaluate_klue_pilot.py --phase before --output output/training/klue-wos-before-v1
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen3.ps1
# .venv-trainのCUDA環境にpyarrowも必要
& "$env:LOCALAPPDATA/Programs/Jan/uv.exe" pip install --python .venv-train/Scripts/python.exe pyarrow==25.0.0
.venv-train/Scripts/python.exe scripts/train_klue_pilot.py
.venv-train/Scripts/python.exe tmp/llama-converter/convert_lora_to_gguf.py --base models/qwen3-4b-instruct-2507/tokenizer --outfile adapters/klue-wos-qwen3-pilot-v1/adapter-f32.gguf --outtype f32 adapters/klue-wos-qwen3-pilot-v1
powershell -ExecutionPolicy Bypass -File scripts/start_qwen3.ps1 -LoraPath adapters/klue-wos-qwen3-pilot-v1/adapter-f32.gguf
python scripts/evaluate_klue_pilot.py --phase after --output output/training/klue-wos-after-v1
```

学習用データ・モデル・生成物は既定で既存出力を上書きしないため、再実行する場合は別の実験名・パスを用意します。

### 小規模実験の結果

| 指標 | 学習前 | 200例のQLoRA後 |
|---|---:|---:|
| KLUEの60例・完全一致 | 9/60 | 35/60 |
| KLUEのslot-value micro F1 | 0.5993 | 0.9384 |
| KLUEの出力不正・途中切れ等 | 15/60 | 0/60 |
| うち状態が変更される34例・完全一致 | 2/34 | 13/34 |
| 既存のスキンケアAgent合格シナリオ | 41/59 | 30/59 |
| 同Agentの状態5項目完全一致 | 56/83 | 36/84 |

学習は約435秒、validation loss（別の40会話）は0.835804→0.066193でした。
アダプターの重み更新、保存後の再読込と生成probeの一致を確認しました。
KLUE評価は直前の正解状態を与え、検証会話ごとに1ターンだけ測っています。
Q4_K_Mで推論した同じQwen3のモデルを、アダプターなし／ありで比較しました。
学習は別のNF4 repackのため、NF4推論そのものの評価ではありません。
スキンケア評価は以前から観測済みの合成データで、初回はHTTP 500のため1ターン未実行でした。

一般的な状態追跡は限定条件で改善しましたが、スキンケアAgentでは悪化したため、
このアダプターを既存Agentの改善版として採用しません。原因は本実験だけでは特定できません。
全58,792ユーザーターンや人間の自然なスキンケア対話に対する性能を示すものでもありません。

- `output/klue_wos_pilot_report_ja.txt`: 学習・評価報告
- `output/klue_wos_pilot_predictions.csv`: 60例の正解と前後の予測
- `output/klue_wos_pilot_summary.json`: 指標と実験設定
- `adapters/klue-wos-qwen3-pilot-v1/`: 保存済みPEFT / GGUF LoRA

## AI Hubデータ 3条件・各2,000例の比較

`data/raw/aihub/` の提供済みデータをローカルで利用します。外部学習サービスへ送信しません。
SNS美容・ファッション会話から2人の隣接する発話ペアを1会話につき1件、
スキンケアから質問と最終回答を1レコードにつき1件選びます。画像・属性メタデータ・構造化CoTは使用しません。
SNSではそのペア以前の会話履歴を入力に含めず、マルチターン状態追跡を直接学習しません。
画像を明示的に参照する文面は機械的に除外しています（暗黙の参照が残らない保証はありません）。
本文には年齢などが含まれることがあります。派生データも含めて提供元の利用条件を守り、公開しません。

両者に共通する「入力発話→応答」のSFTとして比較します。SNSのスロットや肌の状態・ツール呼び出しを
正解として教えた実験ではありません。したがって、状態追跡データ同士の比較だとは解釈できません。

- SNS単独: 2,000会話から各1ペア（総164,241トークン、教師47,020トークン）。
- スキンケア単独: 2,000レコード（総901,407トークン、教師491,228トークン）。
- 混合: 上記から各1,000件、合計2,000件（総533,903、教師269,938トークン）。

2,000はレコード数です。異なる元IDでも質問・回答文が完全一致する例がスキンケア単独で4組、混合で1組あります。
選択後の学習用と検証用の間には、入力文・応答ペアの完全一致はありませんでした。
スキンケアの選択は層化しておらず、2,000件の学習候補に元「敏感性」カテゴリは0件でした。
またスキンケアValidation 40件中29件が元「美白」カテゴリです。刺激感・乾燥に対する代表性は限定的です。

元のtrainとValidationを分け、評価用として各領域40件を固定しています。
同じ例数・同じoptimizerステップでも、応答長・タスク・総トークン量が大きく異なります。
`data/processed/aihub_ablation_v1/manifest.json` に条件、出典ファイルhash、選択方法を記録します。
学習はQwen3-4B NF4の同一ベースとLoRA設定、各2,000例・1000 optimizerステップ。
50ステップごとにローカルへoptimizer・乱数・位置を含むcheckpointを保存します。
RTX 4070 8GBで実行するためgradient checkpointingを使用し、WindowsのTritonなし環境ではcompileしません。

```powershell
# 既存の固定データは上書きしません
python scripts/prepare_aihub_ablation.py
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen3.ps1
.venv-train/Scripts/python.exe scripts/train_aihub_ablation.py --preflight
.venv-train/Scripts/python.exe scripts/train_aihub_ablation.py --condition sns_only
.venv-train/Scripts/python.exe scripts/train_aihub_ablation.py --condition skin_only
.venv-train/Scripts/python.exe scripts/train_aihub_ablation.py --condition mixed
# 3アダプターをGGUF変換し、同じ59シナリオを順に評価（既存評価は上書きしない）
python scripts/run_aihub_evaluations.py
```

各条件で同じSNS/スキンケア各40件の検証lossと、同じ既存の59シナリオのAgent性能を比較します。
59シナリオは過去に観測済みの合成開発セットであり、新しい未使用テストではありません。
検証lossは各例の教師トークンlossを平均した値なので、同一領域の学習前後で比較します。
データの形式・長さが違うため、結果をデータの種類だけによる純粋な因果効果と断定しません。

### 実測結果（1 seed）

| 条件 | SNS検証loss | スキンケア検証loss | シナリオ全条件合格 | 状態5項目完全一致 |
|---|---:|---:|---:|---:|
| 追加学習前 | 4.797 | 2.102 | 41/59 | 56/83ターン |
| SNS単独 | 2.068 | 1.555 | 15/59 | 19/83ターン |
| スキンケア単独 | 3.795 | 0.584 | 38/59 | 51/84ターン |
| 混合 | 2.186 | 0.701 | 13/59 | 19/84ターン |

学習前とSNS単独は各1ターンがサーバー応答解析エラーで未実行です。
会話応答の検証lossは改善しても、Agentの状態更新やツール利用は改善しませんでした。
混合条件には実行せずに「更新した」と回答した例もあります。これらは単一seedの探索結果です。
Agentの合成正解には発症日など要レビューのラベルがあり、結果の一般化には別途検証が必要です。
集計と制約は `output/aihub_ablation_v1_report_ja.txt`、各条件の合成例は
`output/aihub_ablation_v1_synthetic_examples.csv` を参照してください。
## QLoRAとAgent学習の追加監査

`output/agent_audit_v1_report_ja.txt` に実測結果、データの制約、未解決のエラーを記録しています。
Agent用合成教師200判断（ツール呼び出し87判断を含む）と、Agent用100判断＋AI Hub会話100件を比較しました。
後者はAgent用データを置き換える同じ200件の学習枠の比較です。AI Hub由来のデータや重みはローカルに保存します。

実Qwen3で標準lossと独自lossを2例比較するとlossは一致しましたが、LoRA勾配には約1.0～1.1%の相対L2差がありました。
NF4とGGUFの6シナリオ比較でも状態が一致しないケースがあり、量子化・実装の個別原因は未特定です。
元validationには曖昧な発症日ラベルがあり、シナリオ評価では修正版3件を含む別バージョンを使用しました。

| GGUF評価 | 学習前 | Agent単独100 step | Agent＋AI Hub混合100 step | 旧AI Hub会話のみ |
|---|---:|---:|---:|---:|
| 修正版validation | 20/30 | 22/30 | 21/30 | 7/30 |
| 新規重点テスト | 7/12 | 9/12 | 8/12 | 1/12 |

新規テストは既存データとの発話完全一致はありませんが、既知の失敗を踏まえて作成した合成例で、独立した人手レビューは未実施です。
各条件1 seedの探索的実験であり、独立した実ユーザーへの汎化を示すものではありません。

実行にあたっては、GPU推論サーバーを一時停止し、モデル・元データをすべてローカルに用意してください。
学習・評価済みの出力は上書きせず、既存の途中出力も保護します。再実行時は別名の実験を用意してください。

```powershell
python -m unittest discover -s tests
powershell -ExecutionPolicy Bypass -File scripts/stop_qwen3.ps1
.venv-train/Scripts/python.exe scripts/audit_real_loss.py
.venv-train/Scripts/python.exe scripts/train_agent_audit.py --condition stateful
.venv-train/Scripts/python.exe scripts/train_agent_audit.py --condition mixed
.venv-train/Scripts/python.exe scripts/evaluate_agent_audit.py hf
python scripts/evaluate_agent_audit.py gguf
python scripts/evaluate_agent_audit.py summary
python scripts/evaluate_agent_audit.py final
```
## AI Hub Agent教師データのレビュー

ローカルのAI Hubデータから、元のTrain / Validationを保った150会話・287発話のレビュー候補を作成しました。
SNSは一人の対象話者の発話に投影したシナリオ、スキンケアは単一の質問であり、実際のAgent操作ログではありません。
候補と原文は `data/processed/aihub_agent_review_v4/` に保存し、gitや外部サービスに送信しません。
最初に `data/AI_Hub_Agent教師データ_レビュー手順.md` と、同ディレクトリの `review.xlsx` を確認してください。

AI下書き3件を含め、現在は人間による承認済みラベル0件です。自動候補を正解とみなして学習しません。
承認後、`python scripts/export_aihub_agent_review.py --check` で構造・根拠等を確認できます。
この機械検査は人による意味・プライバシー・利用条件の確認を置き換えません。

