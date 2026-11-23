---
language:
- ko
- en
license: cc-by-sa-4.0
base_model: klue/roberta-large
library_name: transformers
datasets:
- klue/klue
- skt/kobest_v1
- LocalLLaMA/typed-decisions
- jaredpalmer/kev-suites
- castorini/mr-tydi
- google-research-datasets/tydiqa
- AmazonScience/massive
- Davlan/sib200
- fancyzhx/dbpedia_14
- KETI-AIR/kor_dbpedia_14
- gfissore/arxiv-abstracts-2021
- google-research-datasets/go_emotions
- jeanlee/kmhas_korean_hate_speech
- neulab/conala
pipeline_tag: text-classification
inference: false
tags:
- korean
- decision-model
- system-one
- typed-decisions
- choice
- noul
- score
- classification
- reranker
- zero-shot-classification
- nli
- klue
- kobest
- relation-extraction
- roberta
- calibration
---

# ko-decision-roberta-large

A Korean and English **typed-decision model**: given a state, an instruction and a list of options, it returns a probability for every option. It does not generate text. Fine-tuned from `klue/roberta-large` (337M parameters, bidirectional encoder), and loaded with the standard `AutoModelForSequenceClassification` class.

## Versions

| Repository | Base | What it is |
|---|---|---|
| [`ko-decision-roberta-large`](https://huggingface.co/mmetamong/ko-decision-roberta-large) | `klue/roberta-large` | Korean-centred. KLUE and KoBEST tasks, English typed decisions, and note-taking questions (relevance, category, tag). |
| the same repository at git tag `v1.0` | `klue/roberta-large` | The first release, before the note-taking questions were added. |
| [`ko-decision-bge-m3`](https://huggingface.co/mmetamong/ko-decision-bge-m3) | `BAAI/bge-reranker-v2-m3` | Multilingual base, same training data as `ko-decision-roberta-large`. Better on unseen question formats and English notes; lower on Korean inference. |
| [`ko-decision-roberta-large-klue`](https://huggingface.co/mmetamong/ko-decision-roberta-large-klue) | `klue/roberta-large` | KLUE, KoBEST (BoolQ, COPA) and typed-decisions only. The narrowest training data. |

This card describes **`ko-decision-roberta-large`** at its current revision (v2). The previous revision is kept under the git tag `v1.0`.

## 한국어 요약

- **무엇인가:** 글을 쓰지 않고, 주어진 선택지마다 확률을 매기는 판단 모델입니다. 한국어와 영어 입력을 받습니다.
- **잘하는 것 1 (KLUE):** 같은 2,080문항에서 `2nugu/laya-ko`보다 높습니다. NLI 90.7% 대 81.0%, YNAT 86.9% 대 82.0%, STS 오차 0.416 대 0.553. 관계 추출은 82.2% 대 70.8%입니다.
- **잘하는 것 2 (노트 정리용 판단):** 검색 문단이 질의와 관련 있는지, 어느 카테고리인지, 태그가 해당하는지를 묻는 세 가지 질문을 학습했습니다. 학습에 쓰지 않은 문항에서 관련성 91.4%, 카테고리 93.1%, 태그 90.4%입니다.
- **못하는 것:** 학습하지 않은 형식의 질문에는 약합니다. 특히 처음 보는 예/아니오 질문에서 "예"로 쏠립니다(영어 800문항 중 84%를 "예"로 답함, 정답은 42%). 영어 노트에서는 관련 있는 문단을 "관련 없음"으로 놓치는 일이 많아(순위는 맞게 매깁니다), 영어 비중이 크면 다국어 기반 모델이 낫습니다. 일본어는 읽지 못합니다.
- **주의:** 원래 확률은 실제보다 확신이 과합니다. 확신도가 필요하면 `calibration.json`의 과제별 온도로 나눠 쓰세요. 코드 리뷰 같은 코드 판단 데이터는 학습하지 않았습니다.
- **사용법:** 아래 Usage의 코드를 그대로 실행하면 됩니다.

## Results against `2nugu/laya-ko` and Laya multilingual

Fixed 2,080-row KLUE slice (NLI 999 rows / 333 premise groups, YNAT 1,000, STS 81), raw probabilities at temperature 1. All three models were evaluated with the same harness. Intervals are paired cluster bootstrap, 10,000 replicates.

| Metric | Laya multilingual | laya-ko | this model | Δ vs laya-ko, 95% interval | Δ vs Laya, 95% interval |
|---|---:|---:|---:|---|---|
| KLUE-NLI accuracy | 73.67% | 80.98% | **90.69%** | +9.71 pp [+7.41, +12.01] | +17.02 pp [+14.31, +19.62] |
| KLUE-YNAT accuracy | 39.60% | 82.00% | **86.90%** | +4.90 pp [+2.60, +7.30] | +47.30 pp [+43.80, +50.80] |
| KLUE-STS MAE (lower is better) | 1.1285 | 0.5527 | **0.4164** | −0.136 [−0.232, −0.041] | −0.712 [−0.916, −0.516] |

All six intervals exclude zero. `laya-ko` is Laya multilingual fine-tuned on Korean.

This slice is public KLUE validation data that earlier work in this project had looked at; it is not a blind external test. The sample IDs behind the numbers on the laya-ko model card are unpublished, so these figures are not comparable with that card.

## Note-taking decisions

Three question shapes, taken from the open-source Obsidian toolkit [brain-openkit](https://github.com/hyeondata/brain-openkit), were added to training: is a passage useful for a query, which category fits a passage, and does a tag apply.

### Held-out questions in those shapes

Accuracy on rows the model never saw (official test splits or held-out queries of the source datasets). Kev and Laya were not trained on these shapes, so for them this is a zero-shot test; for this model the shape is familiar and the content is new.

| Question | Rows | Laya multilingual | laya-ko | Kev-0.8B | Kev-4B | this model |
|---|---:|---:|---:|---:|---:|---:|
| Passage relevant to the query? (A/B) | 1,718 | 68.5% | 63.7% | 66.9% | 79.5% | **91.4%** |
| Which category? (up to 10, lettered) | 800 | 62.8% | 58.6% | 71.0% | 79.1% | **93.1%** |
| Does the tag apply? (A/B) | 1,200 | 83.4% | 78.2% | 75.2% | 82.2% | **90.4%** |

By source: relevance Mr. TyDi Korean 94.2%, Mr. TyDi English 93.8%, KLUE-MRC 86.5%; category MASSIVE Korean 93.5%, English 92.8%; tag GoEmotions 86.5%, K-MHaS 94.3%. The 95% half-widths are about ±1.5 to ±2 points.

### brain-openkit's own benchmark

brain-openkit's `bilingual-v1` suite, run with its unmodified runner (BM25 picks 8 candidates, the model reranks to the top 3; category and tag questions as the product sends them). Holdout split: 24 queries and 18 notes in Korean and English that none of these models were trained on.

| Model | Parameters | Recall@3 | MRR@3 | Category accuracy | Tag micro-F1 |
|---|---:|---:|---:|---:|---:|
| BM25 only | — | 0.750 | 0.750 | — | — |
| Laya multilingual (the project's published report) | 0.31B | 0.750 | 0.604 | 0.667 | 0.469 |
| Kev-0.8B (brain-openkit's default) | 0.8B | 0.833 | 0.771 | 0.889 | 0.769 |
| Kev-4B | 4B | 0.833 | 0.812 | 0.944 | 0.889 |
| Kev-9B | 9B | 0.833 | 0.833 | 1.000 | 0.894 |
| **this model** | 0.34B | 0.833 | 0.833 | 0.778 | 0.732 |

**Read this table with care: it is tiny.** One note is 5.6 points of category accuracy, and the 95% interval for 14 of 18 correct spans roughly 50% to 90%. It shows that the model works inside the real pipeline (zero request errors, 88 ms median per decision on an Apple M1 Max); it cannot rank models that are a few notes apart. Recall@3 is capped at 0.833 for every model because BM25 never retrieves the right note for four cross-language queries. On tags this model made 3 false positives and missed 8 of 23 tags.

**The A/B relevance decision, as opposed to the ranking.** Taking all 36 queries of the suite and all 24 notes: this model marks the relevant note as A for 21/36 queries and marks 3/828 unrelated query–note pairs as A. By language (query / note): Korean / Korean 12/14, English / English 3/14, Korean / English 3/4, English / Korean 3/4. It is strict, and on English notes it misses most relevant passages at the 0.5 cut while still ranking them first (see the MRR above): use the probability to rank, not the A/B answer to filter, or use [`ko-decision-bge-m3`](https://huggingface.co/mmetamong/ko-decision-bge-m3) for English notes. The first release (`v1.0`) had the opposite fault: it marked 554 of 828 unrelated pairs as A.

## On the benchmarks the laya-ko card reports

Same benchmarks, one harness. The laya-ko author's sample IDs and STS binning are unpublished, so these are not the same rows; the harness lands close to the card for the two Laya models (card values in parentheses). AI-Hub culture MC is not public and was not run.

### Tasks this model was trained on

| Benchmark | Laya multilingual | laya-ko | this model |
|---|---:|---:|---:|
| KLUE-RE, 1,000 rows, 30-way accuracy | 16.4% (13.6%) | 70.8% (70.5%) | **82.2%** |
| KLUE-YNAT, 1,000 rows, accuracy | 39.6% (41.4%) | 82.2% (83.4%) | **86.9%** |
| KLUE-NLI, 999 rows, accuracy | 73.7% (76.1%) | 81.0% (81.5%) | **90.7%** |
| KLUE-STS, 519 rows, 6-level accuracy | 20.6% (21.0%) | 50.7% (50.9%) | **58.8%** |
| typed-decisions EN, 2,000 rows, accuracy | 35.0% (35.0%) | 71.2% (72.5%) | 73.4% |
| KoBEST-HellaSwag, 500 rows | 36.2% | 38.4% | **80.0%** |

KLUE rows are from the validation split; training used the train split. The Laya models were not trained on KoBEST-HellaSwag.

### Tasks this model was not trained on

| Benchmark | Chance | Laya multilingual | laya-ko | this model |
|---|---:|---:|---:|---:|
| Kev transfer suites (EN), 1,928 questions | — | 56.9% | **58.2%** | 45.0% |
| Kev decision-v2 (EN), 1,440 questions | 30.0% | **58.8%** (58.5%) | 57.2% (57.2%) | 52.6% |
| Belebele reading comprehension (KO / EN), 900 rows each | 25.0% | 35.8% / 35.1% | 32.6% / 34.2% | 44.6% / 34.9% |
| KoBEST-WiC, 150 rows | 50.0% | 51.3% | 49.3% | 64.7% |
| JCommonsenseQA (JA), 500 rows | 20.0% | 52.8% (52.6%) | **58.4%** (56.6%) | 20.2% |
| KMMLU, 900 rows | 25.0% | 24.4% (24.4%) | 24.3% (29.8%) | 25.4% |
| MMLU, 560 rows | 25.0% | 27.9% (29.5%) | 27.9% (26.6%) | 25.9% |

The Kev transfer suites (`transfer-v2` and `transfer-r3` test files of `jaredpalmer/kev-suites`) contain only sources that appear in no Kev training file: emotion, offensive-post, paraphrase and sentence-answers-question judgements, science and MMLU questions, and synthetic policy probes. They are the cleanest measure here of transfer to new question formats. Kev decision-v2 is partly in-distribution for this model (four of its ten source datasets were in training, different rows).

**Transfer to unseen question formats is this model's weak point.** On the Kev transfer suites it scores 45.0% against laya-ko's 58.2%, and the same training data on a multilingual base ([`ko-decision-bge-m3`](https://huggingface.co/mmetamong/ko-decision-bge-m3)) scores 14.3 points higher (95% interval [+11.9, +16.8]). Examples: six-way emotion labels 32.0%, offensive-post yes/no 34.6%, sentence-answers-question 68.6%.

- **Yes bias on unseen yes/no questions.** On the 800 yes/no questions of the Kev transfer suites it answers "yes" 84% of the time; the gold rate is 42%. In the trained A/B tag shape this does not happen. If you ask a new kind of yes/no question, check the answers.
- **Letter labels no longer attract the answer.** On letter-labelled KMMLU the model picks `A` in 25% of rows (25% would be even; the first release picked it 81% of the time).
- **Japanese does not work.** The `klue/roberta-large` vocabulary maps 47% of the JCommonsenseQA tokens to the unknown token.
- **Generative decision models transfer much better.** On Belebele, which no model here was trained on, Kev-0.8B scores 51.3% (KO) / 61.6% (EN) and Kev-4B 70.9% / 74.8%. On Korean KLUE tasks the order reverses: Kev-9B reaches 89.0% NLI, 71.3% YNAT and 57.9% RE.
- KMMLU and MMLU test recall of facts, which none of these encoders has.

## Other evaluations

| Evaluation | Rows | Result |
|---|---:|---|
| Project test: KLUE-NLI / KLUE-YNAT accuracy | 600 / 700 | 92.0% / 86.0% |
| Project test: KLUE-STS MAE | 200 | 0.420 |
| Project test: KoBEST-BoolQ / KoBEST-COPA accuracy | 200 / 200 | 89.0% / 87.0% |
| KoBEST-HellaSwag test accuracy, plain / letter-labelled options | 500 / 500 | 80.0% / 81.2% |
| Common slice: STS Pearson / Spearman | 81 | 0.937 / 0.931 |
| English typed-decisions test: choice / noul accuracy | 600 / 600 | 73.8% / 81.7% |
| English typed-decisions test: score MAE | 800 | 0.272 |

## Probability quality — read before using confidences

Raw probabilities are **overconfident**. Per-task temperatures fitted on a held-out calibration split (599 rows) are 2.65–4.7. The table shows their effect on the project test split:

| Task | Temperature | NLL (T=1 → fitted) | ECE10 (T=1 → fitted) |
|---|---:|---|---|
| KLUE-NLI | 4.15 | 0.647 → 0.243 | 0.070 → 0.029 |
| KLUE-YNAT | 3.40 | 1.190 → 0.506 | 0.126 → 0.015 |
| KLUE-STS | 3.30 | 1.436 → 1.016 | — |
| KoBEST-BoolQ | 4.70 | 0.617 → 0.229 | 0.098 → 0.051 |
| KoBEST-COPA | 2.65 | 0.607 → 0.330 | 0.102 → 0.056 |

Divide the scores by the task temperature in `calibration.json` before the softmax when you need calibrated confidence. Temperatures exist for these five tasks only; none was fitted for the note-taking questions, KLUE-RE or the English tasks. Temperature does not change which option ranks first.

## Usage

```bash
pip install "transformers>=4.57" torch huggingface_hub
```

### 1. Load the model

Run this once. The examples below reuse `decide` and `temperatures`.

```python
import json
import torch
from huggingface_hub import hf_hub_download
from transformers import AutoModelForSequenceClassification, AutoTokenizer

repo = "mmetamong/ko-decision-roberta-large"
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(repo)
model = AutoModelForSequenceClassification.from_pretrained(repo).to(device).eval()
temperatures = json.load(open(hf_hub_download(repo, "calibration.json")))["temperatures"]


@torch.inference_mode()
def decide(state, instruction, options, temperature=1.0):
    """Return one probability per option. Each option is one (instruction + option, state) text pair."""
    batch = tokenizer([f"{instruction} {o}" for o in options], [state] * len(options),
                      truncation="only_second", max_length=512, padding=True, return_tensors="pt").to(device)
    scores = model(**batch).logits[:, 0].float()
    return torch.softmax(scores / temperature, dim=0).tolist()


def show(name, probs):
    print(name, [round(p, 3) for p in probs])
```

| Type | Question | Options | How to read the output |
|---|---|---|---|
| Choice | Which one? | Any list of candidates | Highest probability is the answer |
| Noul | Yes or no? | `[false, true]` order | Last probability is P(true) |
| Score | How much? | Ordered levels | Expected level is the score |

### 2. Note-taking questions

The three question shapes of [brain-openkit](https://github.com/hyeondata/brain-openkit): letter-keyed options and an English instruction over a Korean or English passage.

```python
note = ("Note: git-backup.md\nTitle: Git 저장소 백업\nPassage:\n"
        "매주 금요일에 저장소 전체를 git bundle 파일로 묶어 외장 디스크에 복사한다. 분기마다 그 파일로 복원 연습을 한다.")

relevance = dict(instruction="Does the passage contain information useful for the query?",
                 options=["A: Relevant information for the query", "B: Unrelated or insufficient information"])
show("answers query   ", decide(state=f"Query: 저장소 백업은 언제 하나요?\n{note}", **relevance))
show("same topic only ", decide(state=f"Query: 인터넷 없이 저장소를 복원하는 방법\n{note}", **relevance))
show("unrelated query ", decide(state=f"Query: 기차표 환불 규정\n{note}", **relevance))

categories = ["A: software: Implementation, operation, and reliability of software systems or data stores.",
              "B: travel: Planning journeys and protecting travel documents, maps, routes, or photographs.",
              "C: home: Care and organization of a household, its equipment, food, plants, or paper documents."]
show("category        ", decide(state=note, instruction="Which existing category best describes this passage?", options=categories))

tag_options = ["A: The tag applies", "B: The tag does not apply"]
show("tag backup      ", decide(state=note, options=tag_options,
     instruction="Does this passage match the tag backup: Creates or verifies recoverable copies of digital files or databases.?"))
show("tag privacy     ", decide(state=note, options=tag_options,
     instruction="Does this passage match the tag privacy: Protects sensitive or identifying information.?"))
```

```text
answers query    [0.187, 0.813]
same topic only  [0.038, 0.962]
unrelated query  [0.0, 1.0]
category         [0.989, 0.0, 0.011]
tag backup       [0.989, 0.011]
tag privacy      [0.003, 0.997]
```

The note answers the first query, shares only a topic with the second, and has nothing to do with the third. This model gives the answered query only 0.19: it ranks the three correctly but is too strict to mark it A. The "Note-taking decisions" section above measures how often that happens.

### 3. Choice — natural language inference

```python
nli_options = ["entailment: 가설이 전제로부터 반드시 참이다 (함의)",
               "neutral: 가설이 전제로부터 참인지 거짓인지 알 수 없다 (중립)",
               "contradiction: 가설이 전제와 모순된다 (모순)"]
nli = dict(state="전제: 하지만 불편함 없이 이용할 수 있습니다.\n가설: 이용할 때 불편함이 있습니다.",
           instruction="전제에 대해 가설이 갖는 논리적 관계를 판정하세요.",
           options=nli_options)
probs = decide(**nli)
show("nli raw         ", probs)
print("  ->", nli_options[probs.index(max(probs))])
```

```text
nli raw          [0.0, 0.0, 1.0]
  -> contradiction: 가설이 전제와 모순된다 (모순)
```

### 4. Choice — topic classification

```python
topics = ["IT과학", "경제", "사회", "생활문화", "세계", "스포츠", "정치"]
probs = decide(state="한국은행, 기준금리 0.25%p 인하 결정",
               instruction="뉴스 제목의 주제를 7개 후보 중에서 고르라.",
               options=topics)
show("topic           ", probs)
print("  =>", topics[probs.index(max(probs))])
```

```text
topic            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  => 경제
```

### 5. Noul — yes/no question

Options go in `[false, true]` order; the last probability is P(true).

```python
probs = decide(state="문맥: 한라산은 제주도에 있는 산으로, 높이는 1,947m이며 대한민국에서 가장 높다.\n"
                     "판단할 내용: 한라산은 대한민국에서 가장 높은 산이다.",
               instruction="문맥을 근거로 판단할 내용이 참인가? 예 또는 아니오로 판단하라.",
               options=["거짓: 질문의 답은 아니오이다.", "참: 질문의 답은 예이다."])
print(f"boolq            P(true) = {probs[1]:.3f}")
```

```text
boolq            P(true) = 1.000
```

### 6. Score — sentence similarity (0–5)

Ordered levels; the expected level is the score.

```python
probs = decide(state="문장 1: 숙소 위치가 지하철역에서 가까워서 좋았어요.\n문장 2: 숙소가 역 근처라 편리했습니다.",
               instruction="두 문장의 의미 유사도를 0~5 척도로 판단하라. 핵심 내용은 사실·정보·요청·명령·감정이며, "
                           "부차적 내용은 뉘앙스·공손함 등이다. 각 점수의 설명을 적용하라.",
               options=["0: 의미와 주제가 모두 다르다.",
                        "1: 주제만 같고 핵심 내용과 부차적 내용은 다르다.",
                        "2: 핵심 내용은 다르고 일부 부차적 내용만 비슷하다.",
                        "3: 핵심 내용은 비슷하지만 부차적 내용에 무시할 수 없는 차이가 있다.",
                        "4: 의미가 거의 같고 일부 부차적 내용만 다르다.",
                        "5: 핵심 내용과 부차적 내용의 의미가 모두 같다."])
show("sts             ", probs)
print(f"  ~ similarity = {sum(level * p for level, p in enumerate(probs)):.2f} / 5")
```

```text
sts              [0.0, 0.0, 0.0, 0.156, 0.844, 0.0]
  ~ similarity = 3.84 / 5
```

### 7. Calibrated confidence

Pass the task temperature from `calibration.json`. The ranking stays the same; only the confidence changes.

```python
show("nli calibrated  ", decide(**nli, temperature=temperatures["klue_nli"]))
```

```text
nli calibrated   [0.018, 0.016, 0.965]
```

### 8. With `pipeline`

The standard `text-classification` pipeline also works. Pass text pairs and `function_to_apply="none"` to get the raw scores, then take the softmax over one question's options yourself.

```python
from transformers import pipeline

scorer = pipeline("text-classification", model=repo, function_to_apply="none")
pairs = [{"text": f"{nli['instruction']} {o}", "text_pair": nli["state"]} for o in nli_options]
scores = torch.tensor([r["score"] for r in scorer(pairs)])
show("pipeline        ", torch.softmax(scores, dim=0).tolist())
```

```text
pipeline         [0.0, 0.0, 1.0]
```

### Notes

- **Format.** A standard `RobertaForSequenceClassification` with one output (`num_labels=1`), loaded with `AutoModelForSequenceClassification`; no custom code. Each (instruction + option, state) pair gets one score, and a softmax over one question's options gives the distribution. A score on its own, without the other options of the same question, has no fixed meaning.
- **Head.** The model was trained with a single linear layer on the first token. RoBERTa's classification head adds a dense layer and a tanh, so that layer is stored as 0.001 × identity, which makes the head compute the trained linear layer: over the 2,080 common-slice rows the largest probability difference to the training-format checkpoint is below 1e-6 (`eval/export_check.json`).
- **Tokenizer.** Configured not to emit `token_type_ids` (RoBERTa has a single token type). Inputs beyond 512 tokens are truncated on the state side.
- **Hub widget.** Disabled, because it sends single texts, not pairs.
- **Check.** Output from this repository on Apple MPS (float32) picks the same top option as the training-GPU evaluation (BF16) on 2,080 of 2,080 common-slice rows; the largest probability difference is 0.053.
- The `eval/*.json` records name project scripts (`scripts/…`) in their `harness` fields; those scripts are not part of this repository.

## Training

Four stages. Each later stage continues from the previous checkpoint and replays all earlier data while adding new tasks, so the earlier tasks are not forgotten.

### Data

Typed-decision tasks (stages 1 to 3):

| Source | Rows | License |
|---|---:|---|
| KLUE-YNAT | 45,678 | CC BY-SA 4.0 |
| KLUE-RE | 32,170 | CC BY-SA 4.0 |
| KLUE-NLI | 24,993 | CC BY-SA 4.0 |
| KLUE-STS | 11,656 | CC BY-SA 4.0 |
| Kev `public-pool-v6`, 7 open-license sources (English) | 7,000 | open, per source (see License) |
| `LocalLLaMA/typed-decisions` (English) | 6,000 | Apache-2.0 |
| KoBEST-BoolQ | 3,659 | CC BY-SA 4.0 |
| KoBEST-COPA | 3,006 | CC BY-SA 4.0 |
| KoBEST-HellaSwag | 2,029 | CC BY-SA 4.0 |
| **Total** | **136,191** | |

Note-taking question shapes (stage 4):

| Source | Rows | Rendered as | License |
|---|---:|---|---|
| Mr. TyDi (Korean, English) | 13,710 | Passage relevance | Apache-2.0 |
| KLUE-MRC | 13,813 | Passage relevance (unanswerable questions as negatives) | CC BY-SA 4.0 |
| TyDi QA gold passage (Korean, English) | 10,519 | Passage relevance | Apache-2.0 |
| CoNaLa | 4,686 | Relevance of a Python snippet to a request | MIT |
| MASSIVE (Korean, English) | 25,138 | Category and tag | CC BY 4.0 |
| DBpedia-14 (English) and its Korean translation | 14,292 | Category and tag | CC BY-SA 3.0 |
| arXiv abstracts | 11,837 | Category and tag | CC0 1.0 |
| GoEmotions | 9,873 | Tag | Apache-2.0 |
| K-MHaS | 7,923 | Tag | CC BY-SA 4.0 |
| KLUE-YNAT, re-rendered | 5,750 | Category and tag | CC BY-SA 4.0 |
| SIB-200 (Korean, English) | 2,024 | Category and tag | CC BY-SA 4.0 |
| **Total** | **119,565** | | |

Korean KLUE and KoBEST rows come from the official train splits with the evaluation groups excluded. In the note-taking set, relevance and tag questions are balanced on purpose: of the two-option rows, 43% have the positive answer. Tag negatives are other labels of the same dataset. Half of the KoBEST-HellaSwag rows carry letter-labelled options. No row of brain-openkit's own benchmark was used in training or checkpoint selection.

### Setup

| Item | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---|---|---|---|---|
| Starts from | `klue/roberta-large` | Stage 1 | Stage 2 | Stage 3 |
| Adds | Five Korean tasks, English | KLUE-RE | KoBEST-HellaSwag, 7 Kev sources | Note-taking question shapes |
| Rows | 94,992 | 127,162 | 136,191 | 255,756 |
| Epochs / steps | 4 / 11,876 | 2 / 7,948 | 2 / 8,512 | 2 / 15,986 |
| Wall time | 72 minutes | 78 minutes | 85 minutes | 158 minutes |
| Dev tasks used to pick the checkpoint | NLI, YNAT, STS | + KLUE-RE | + Kev decision-v2 development | + 1,500 held-out note-taking rows |
| Selected step | 11,872 | 5,961 | 6,384 | 15,986 |

Common to all stages:

| Item | Value |
|---|---|
| Objective | Soft-target cross-entropy over a row's options; no auxiliary loss |
| Optimiser | AdamW, weight decay 0.01, gradient clip 1.0 |
| Learning rate | Encoder 1e-5, head 1e-4 |
| Schedule | 10% linear warm-up, then linear decay |
| Batch | 32 rows per step (length-sorted micro-batches, gradients accumulated) |
| Seed | 43 |
| Precision / hardware | BF16 autocast, one RTX PRO 6000 |

The checkpoint with the lowest mean dev error is kept (`1 − accuracy` per task, `MAE / 5` for STS).

### What stage 4 changed

| Change on the common slice (paired, 95% interval) | Stage 4 vs stage 3 |
|---|---|
| KLUE-NLI accuracy | +0.20 pp [−1.10, +1.50] |
| KLUE-YNAT accuracy | −0.20 pp [−1.40, +1.00] |
| KLUE-STS MAE | −0.014 [−0.043, +0.014] |

No detectable change on the earlier tasks. On held-out note-taking questions, relevance went from 57.4% to 91.4%, category from 50.7% to 93.1% and tag from 61.4% to 90.4%. On brain-openkit's benchmark the tag false positives fell from 25 to 3. Transfer to unseen formats did not improve (Kev transfer suites 44.1% → 45.0%), and the yes bias on unseen yes/no questions grew from 74% to 84% "yes".

Earlier-stage records are kept under `eval/stage1_*`, `eval/stage2_*` and `eval/stage3_*`; the stage-3 weights are the git tag `v1.0`.

## Limitations

- **Narrow.** Strong on the trained task families and question shapes, weak on unseen ones: Kev transfer suites 45.0% against laya-ko's 58.2%.
- **Yes bias on unseen yes/no questions** (84% "yes" where 42% is right). The trained A/B tag shape is not affected.
- **Reading comprehension is weak**: Belebele 44.6% (KO) / 34.9% (EN), chance 25%.
- **No Japanese**, and no language other than Korean and English was tested. The vocabulary is Korean-centred: English words and code are split into very small pieces.
- **Code:** the only code data is CoNaLa (does a short Python snippet answer a request). No code-review or bug-judgement data was used.
- One forward pass per option: a 10-option question costs ten passes and a 30-way KLUE-RE question costs thirty.
- The comparison slice is public and has been inspected during this project; STS has only 81 rows there. brain-openkit's benchmark has 18 holdout notes.
- Stages 2 to 4 were each run once (one seed). Stage 1 was run with two seeds; the other reached 88.6% NLI on the common slice, so about two points of NLI are within seed-to-seed variation.
- No safety, bias or toxicity evaluation. The tag training data includes hate-speech labels (K-MHaS); that does not make this a moderation model.
- Raw confidences are overconfident (see above).

## License and attribution

Released under **CC BY-SA 4.0**.

- Base model: `klue/roberta-large`. The KLUE repository states "This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License"; neither that repository nor the base model's Hugging Face card states a separate license for the pretrained weights. This release follows the repository's CC BY-SA 4.0 statement.
- Typed-decision data: KLUE and KoBEST are CC BY-SA 4.0 (see `DATA_NOTICE.md`, `DATA_LICENSE_CC-BY-SA-4.0.txt`); `LocalLLaMA/typed-decisions` is Apache-2.0.
- 7,000 rows of `jaredpalmer/kev-suites` (`public-pool-v6`), restricted to the seven sources whose own terms are open, as read on 2026-10-06: Banking77 (CC BY 4.0), BoolQ and DBpedia-14 (CC BY-SA 3.0), ARC (CC BY-SA 4.0), CommonsenseQA (MIT), OpenBookQA (Apache-2.0) and MNLI (OANC and other permissive terms). The pool's other six sources were not used: Yelp, Amazon reviews and AG News (non-commercial or research-only terms) and IMDb, SST-5 and TREC (no stated license).
- Note-taking data, with the license tag each dataset carries on the Hugging Face Hub: Mr. TyDi, TyDi QA and GoEmotions (Apache-2.0), KLUE-MRC, K-MHaS and SIB-200 (CC BY-SA 4.0), MASSIVE (CC BY 4.0), DBpedia-14 and its Korean translation (CC BY-SA 3.0), arXiv abstract metadata (CC0 1.0), CoNaLa (MIT).
- Evaluation only, never trained on: Belebele (CC BY-SA 4.0), the Kev transfer suites, and brain-openkit's `bilingual-v1` benchmark (MIT).

No training data is redistributed here.

Citations:

- KLUE: Park et al., 2021, https://arxiv.org/abs/2105.09680
- KoBEST: Kim et al., 2022, https://arxiv.org/abs/2204.04541
