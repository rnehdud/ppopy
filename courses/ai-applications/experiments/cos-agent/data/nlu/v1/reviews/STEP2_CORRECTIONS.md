# PPO-46 Step 2 — Gemini 피드백 수정 및 재검수 요청

## 기준과 현재 상태

기준은 `origin/data/nlu-v1-step2@3b8e4ca`예요. 초기 검수는 PASS936 / FAIL9 / REVIEW35였고, 원본 [Gemini980행 결과](step2_cross_model_critic.jsonl)와 [요약](step2_cross_model_critic_summary.md)을 바이트 그대로 보존했어요.

이번 변경은 **요청한23행 + 공통 atom 표현을 공유하는 기존 PASS 3행 = 총26행**이에요. 변경된 행에는 기존 PASS를 하나도 이월하지 않았어요. 내용이 그대로인954행 가운데 이전 Gemini PASS 해시 일치933행과 정책 확정으로 현행 유지/PASS 수용한 REVIEW21행을 구분해 기록했어요. 이것을 새 Gemini 재검수 PASS980으로 표현하지 않아요.

전체 데이터는980행·train882/val98·7개 주 버킷 각140행을 유지해요. 파일럿49행·코어·검증기·KB는 변경하지 않았어요. 모든 데이터의 `confirmed_by_user=false`, `human_review=unreviewed`를 유지해요.

## 1. coverage_gaps 통일 — 핵심21행

대상: `0414..0420`, `0491..0497`, `0757..0763`.

- 도포 중 일부 부위 누락으로 atom을 통일했어요.
- 모호했던 `귀랑 목은 차단제 안 발랐어요` 변형은 `차단제 바를 때 귀랑 목은 빼먹었어요`로 바꿨어요.
- 제품 후보 `차단제`는 본인이면 `using`, 타인이면 `other_person`이에요.
- 귀/목의 누락 범위·다른 슬롯·증상·분할·주체는 보존했어요. 실제 도포와 단발 비도포 경계를 섞지 않아요.

예: `nlu-step2-0414`는 원문에 이미 `귀와 목을 차단제 바를 때 빼먹었어요`가 있어 사용 상태만 고쳤어요.

```json
{"변경전":{"raw_text":"차단제","usage_state":"unknown","matched_catalog_hint":null},"변경후":{"raw_text":"차단제","usage_state":"using","matched_catalog_hint":null}}
```

`nlu-step2-0494`는 같은 도포 상황이 타인 경험이므로 변경 후 `usage_state="other_person"`이에요.

## 2. method.mixing 원문-값 정렬 — 2행

대상: `nlu-step2-0042`, `nlu-step2-0791`.

- 변경 전 원문: `두 세정제를 손에서 혼합해요`
- 변경 후 원문: `두 세정제를 손바닥에서 혼합해요`
- 슬롯 값은 `두 세정제를 손바닥에서 섞음` 그대로예요. `source_text`와 해당 `evidence_span`도 변경 후 원문으로 함께 재생성했어요.

이로써 값에 있는 손바닥이라는 부위를 원문이 직접 뒷받침해요.

## 3. 공통 atom 영향 — 추가3행도 재검수

대상: `nlu-step2-0099`, `nlu-step2-0102`, `nlu-step2-0105`.

이 세 행은 기존에도 같은 발화 안의 명시적 덧바름 때문에 `using`으로 올바르게 라벨링돼 있었어요. 그러나 공통 `gaps` atom의 `안 발랐어요` 변형을 정렬하면서 원문과 근거 span이 달라져 내용 해시도 바뀌었어요. 기존에 PASS였다는 이유로 예외 처리하지 않고 추가 재검수를 요청해요.

원문 통일을 요청한23행에만 국소 적용하면 공통 atom의 같은 변형이 다시 갈라지므로, 공통 생성기를 일관되게 수정하고 추가 영향 범위를 공개했어요.

## 4. 수정 없는 확정 정책 — 21행

- `0407..0413`: 단발 비도포는 `unknown` 유지. `not_using`이 없는 계약에서 과거 중단을 발명하지 않아요.
- `0533..0539`: 타인의 명시적 사용 중단은 `stopped` 유지.
- `0540..0546`: 타인의 명시적 구매 고려는 `considering` 유지.

이21행은 변경 전후 데이터와 해시가 같아요. [정책 수용 기록](step2_policy_acceptance.jsonl)에 전달받은 사용자 확정을 따로 기록했고 원본 Gemini REVIEW를 임의로 편집하지 않았어요. 정책 수용은 행 데이터의 사람 승인과 달라 `human_review=unreviewed`예요.

## 재검수 파일

- [전체26행](step2_recheck_requests.jsonl): 새 content_sha256·현재 입력/예상 출력·이전 해시/판정.
- [핵심23행](step2_recheck_core23.jsonl), [추가3행](step2_recheck_additional3.jsonl): 업무 분담용 부분집합.
- [26행 수정 전후 raw](step2_corrections_raw.jsonl): 모든 요청과 예상 JSON을 변경 전/후 그대로 포함해요.
- [해시·범위 대조](../validation/step2_correction_manifest.json): 이전980행 해시 대조, 변경/불변 행 ID, 원본 Critic 파일 해시.

외부 재검수 반환은 `step2_cross_model_recheck.jsonl` 같은 새 파일에 실제 reviewer_model·새 해시·판정·raw 근거를 적어 주세요. Codex 자체 검사를 Gemini 재검수로 표기하지 않았어요. 새26행에 대해서는 아직 PASS를 주장하지 않아요.

공식 검증기·추가 감사·지정 테스트·source manifest 결과는 [실행 기록](../validation/step2_commands.json)에 있어요.
