# PPO-46 Step 1 — 채팅 자유 입력 NLU SFT 파일럿 49건

## Step 2 신규 작업 · 2026-11-28

`d1e9cbe` 확정 정책을 기준으로 별도 `data/nlu-v1-step2` 브랜치에 **신규 합성 980턴(train882 / val98)**을 작성했어요. 파일럿49건과 아래 Step 1 이력은 보존했어요. 초기 Gemini 전수 검수(936 PASS / 9 FAIL / 35 REVIEW) 지적을 반영했고 **변경된26행(핵심23+공통 atom 추가3) 재검수 대기**예요. [Step 2 안내](STEP2_README.md), [수정 내역](reviews/STEP2_CORRECTIONS.md), [재검수 요청](reviews/STEP2_CROSS_MODEL_HANDOFF.md)을 확인해 주세요. 사람 승인·학습은 아직 미실행이에요.

## 팀원·후속 AI: 여기부터 읽어 주세요

공유 브랜치는 `data/nlu-v1-pilot-critic`이에요.
- 초기 Codex 내부 검수(`5aab0a7`): **PASS 46 / FAIL 0 / REVIEW 3** ([TEAM_HANDOFF.md](reviews/codex_critic_20261127/TEAM_HANDOFF.md), [summary.md](reviews/codex_critic_20261127/summary.md)).
- **확정 정책 반영 및 Cross-Model(Gemini) 전수 검수(2026-11-28)**: 위 3건 및 연관 행(`0007`·`0009`·`0014`·`0028`·`0036`)에 확정 정책을 일관 반영해 재생성했고, **49/49 Cross-Model PASS**를 확인했어요 ([gemini_cross_model_20261128.md](reviews/gemini_cross_model_20261128.md)).
- `confirmed_by_user=false`, `human_review="unreviewed"`, `base_zero_shot_executed=false`, `training_executed=false`는 그대로 유지돼 있어요.

1. [확정 정책 및 Cross-Model 검수 기록 (2026-11-28)](reviews/gemini_cross_model_20261128.md)을 먼저 확인해 주세요.
2. [초기 팀원 전달 요약 (5aab0a7)](reviews/codex_critic_20261127/TEAM_HANDOFF.md)과 [3건 상세 설명·raw 근거](reviews/codex_critic_20261127/summary.md)는 수정 전 해시(`0c4c7877...`) 기준 이력으로 보존돼 있어요.
3. [49건 전행 raw 검수 (5aab0a7)](reviews/codex_critic_20261127/critic_raw.jsonl) 및 [무결성 확인](reviews/codex_critic_20261127/review_integrity.json)도 수정 전 이력으로 유지돼 있어요.

`REVIEW`는 확정 오류가 아니라 추출 정책 확인 요청이에요. 기준을 결정하기 전에 임의로 PASS/FAIL이나 사람 승인으로 바꾸지 마세요.
검수 당시 로컬 전용·push 없음 기록은 당시 사실로 보존했으며, 이번 공유 승인은 아래 전달 요약에 별도로 기록했어요.

최신 `origin/main`의 `1fe228e6f8addadd369e820d938dbfefa99c2838`에서 `data/nlu-v1-pilot` 브랜치를 만들었어요.
PPO-46·PPO-40과 최신 계약·화이트리스트·Wire 빌더·검증기를 읽고 작성한 **신규 합성 자료**예요.
기존 SOLUTION/HOLD 1,800턴과는 별도 데이터셋이며 기존 자료·KB·코어 코드는 수정하지 않았어요.

**완료 범위는 파일럿 제작·자동 검증·팀원 교차 검수 인계예요.** 독립 Cross-Model Critic, 사람 확인, Base Qwen3-4B Zero-Shot 기준선, QLoRA 학습은 아직 실행하지 않았어요. PPO-46 전체 Step 1 검수·기준선 측정 완료를 뜻하지 않아요.

## 분포

| 주 버킷 | 건수 |
|---|---:|
| turn1_utterance | 7 |
| turn2_followup | 7 |
| denied_polarity | 7 |
| other_subject | 7 |
| high_risk_symptom | 7 |
| product_mention | 7 |
| no_signal_noise | 7 |
| 합계 | 49 |

- `train` 44 / `val_internal` 5. 동일 의미 가족과 공백 정규화 발화의 교차 분할 누수는 없어요.
- 실제 채팅 자유 입력만 대상으로 해요. `✅` 사례도 정형 버튼 탭이 아니라 자유 채팅에 입력한 문자예요. 온보딩 폼·Quick Reply Fast Path는 포함하지 않아요.
- 세정/방법, 보습, 자외선, 보관·표시, 사용 순서, B-I01 내수성만을 이유로 한 반복 세안 문맥을 포함해요.
- 표준 증상11종과 지속성4종, 제품 사용 상태5종을 포함해요.
- 각 행에 같은 허용 슬롯34개·증상11종·토픽8종을 제공해요. 정답에 나온 슬롯만 허용 목록으로 주는 방식을 쓰지 않아요. 최종 정답은 실제 원문에서 뒷받침되는 후보만 포함해요.
- 주 버킷은 상호 배타적인 배정이에요. 자동 검증의 버킷은 중복 집계하므로 `turn1_utterance=42`, `turn2_followup=7`, 부정10, 타인7, 증상13, 제품16, noise7이며 합계가49가 아닐 수 있어요.

## 파일

- **학습 후보**: `pilot_nlu_v1.jsonl`.
- **원문·JSON 예상 후보·원문과 판단의 연결**: `pilot_nlu_v1_review.md`.
- **독립 Critic 요청**: `reviews/pilot_nlu_v1_critic_requests.jsonl` (49행, 내용 SHA-256 포함).
- **생성 원본**: [build_nlu_v1_pilot.py](../../../scripts/build_nlu_v1_pilot.py).
- 자동 검증: `validation/structure.json`. 원천·분포·행별 해시: `validation/generation_manifest.json`.
- 전체 Wire·범위·버킷·분할·접두사 대조: `validation/pilot_audit.json`. 실제 토크나이저 길이: `validation/token_lengths.json`.

## 계약 적용

`messages[0]`과 `messages[1]`은 모두 실제 `build_nlu_messages(NLURequest)`로 만들었어요.
`messages[2]`는 `NLUExtractionResult` JSON이에요. 인사·잡담을 포함한 모든 출력에서 원문 `source_text`를 보존하고 `confirmed_by_user=false`로 두었어요.
허용하지 않은 `product.*` 슬롯, 전송용 timeout/응답 크기 키, 조언·진단·제품 추천은 출력에 넣지 않아요.

예를 들어 `Lotion A`가 `Lotion AB` 안에 부분 문자열로 있어 Stage 1 힌트에 들어와도, 두 제품명 전체가 정확히 같지 않으면 AB에는 힌트를 연결하지 않아요.
부정된 `hot`을 임의로 `cold`나 `lukewarm`으로 바꾸지 않아요. 타인 증상을 자기 증상으로 바꾸지 않아요. 미상 슬롯 값은 null이에요.
피부 상태·제품 언급은 모델의 **미확정 후보**이며 실제 제품 확인·사용자 승인으로 취급하지 않아요. 등장하는 제품명과 카탈로그 힌트는 가상이에요.

## 재현

cos-agent에서 실행해요. `uv`가 PATH에 없으면 `python -m uv`를 사용해요.

```powershell
python -m uv run --locked python scripts/build_nlu_v1_pilot.py
python -m uv run --locked python scripts/validate_nlu_dataset.py --input data/nlu/v1/pilot_nlu_v1.jsonl --min-rows 40 --enforce-buckets --report data/nlu/v1/validation/structure.json
python -m uv run --locked pytest -q tests/test_nlu_step0.py tests/test_v3_contracts.py
```

저장소 루트에서 `python tools/verify_source_manifest.py`를 실행해요. 검증기나 KB의 허용 값을 바꿔 데이터를 통과시키지 않았어요.
현재 테스트 결과는11개 통과예요. 이 결과는 의미 정확성·독립 Critic PASS나 모델 성능 점수가 아니에요.
Qwen3-4B-Instruct-2507 고정 리비전 토크나이저 기준 최대697토큰이고 길이2,048을 넘는 행은 없어요. 토크나이저만 실행했으며 Base Zero-Shot 추론·모델 학습은 아니에요.
생성기는 작성본 재현 도구예요. 향후 Critic 수정·사람 검수 후에는 현재 승인 파일을 덮어쓰지 말고 별도 사본에서 재현해요.

## 독립 Critic 인계

49행을 전부 읽고 다음을 확인해 주세요.

1. 발화에 명시되지 않은 값·부위·시점·제품 사실을 추가하지 않았는지.
2. 부정의 범위·타인 주어·불명확한 주어를 바르게 보존했는지.
3. 증상11종 및 recent/repeated/persistent/unknown의 판단이 실제 표현에 맞는지.
4. 후속 발화가 직전 질문을 이용하되, 근거 구절은 현재 `source_text` 안에 있는지.
5. 제품명 raw span 전체 일치와 사용 상태5종이 맞는지. hint는 제품 사실·신원 확정이 아닌 후보인지.
6. noise에서 슬롯·증상·제품을 만들지 않았는지. 같은 가족·발화가 다른 분할에 섞이지 않았는지.

검수 결과에는 실제 모델명, row_id, 요청에 있는 content_sha256, PASS/FAIL, 문제 원문, 수정 이유를 적어 주세요.
내용 해시는 `id`, `scenario_family_id`, `split`, `primary_bucket`, 시스템 프롬프트, 파싱된 Wire request와 예상 output을 키 정렬·공백 없는 UTF-8 JSON으로 만든 SHA-256이에요. 재계산 함수는 생성기의 `content_hash(row)`예요.
요청 파일의 작성자 근거는 교차 검수 결과가 아니에요. 같은 모델의 자체 점검을 외부 Critic으로 기록하지 않았어요.

## 다음 단계

파일럿 교차 검수와 Base Qwen3-4B Zero-Shot 측정 후에만 Step 2를 검토해요.
Step 2는 핵심 고빈도30~40개 슬롯·증상11종·7개 버킷에 집중한800~1,000턴 범위예요. 이번 작업에서는 생성하거나 학습하지 않았어요.
