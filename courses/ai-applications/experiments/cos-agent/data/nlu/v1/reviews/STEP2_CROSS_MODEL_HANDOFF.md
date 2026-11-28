# Cross-Model 검수 요청 — PPO-46 NLU Step 2 980턴

## 최신 요청 — 수정 후26행만 새 해시로 재검수

초기 전수 검수는 `3b8e4ca`에 수신했고 기존 `step2_cross_model_critic.jsonl`은 이전 해시의 원본 이력으로 보존했어요. 이번에는 [step2_recheck_requests.jsonl](step2_recheck_requests.jsonl)의 **26행**을 검수해 주세요. [핵심23행](step2_recheck_core23.jsonl)과 [공통 atom 정렬로 바뀐 기존 PASS 3행](step2_recheck_additional3.jsonl)을 구분해 두었어요. 변경 행은 이전 판정과 관계없이 모두 새 해시로 검수해야 해요.

반환 결과는 **`step2_cross_model_recheck.jsonl`** 같은 새 파일에 기록해 주세요. 기존980행 결과를 덮어쓰거나 변경 전 PASS를 변경 후 해시에 복사하지 마세요. [수정 전후 raw](step2_corrections_raw.jsonl)와 [수정 설명](STEP2_CORRECTIONS.md)을 함께 확인해 주세요. 아래 초기980행 인계 절차는 이력과 전체 계약 참조용이에요.

## 대상과 상태

- 작업 브랜치: `data/nlu-v1-step2`.
- 기준: `origin/data/nlu-v1-pilot-critic@d1e9cbe`의 확정 정책.
- 대상: `data/nlu/v1/nlu_sft_v1.jsonl`, **980턴**, train882 / val98.
- 요청: `step2_critic_requests.jsonl` 또는 `step2_batches/batch_01.jsonl`~`batch_14.jsonl` (각70행).
- 초기 상태 이력: 작성 당시 독립 교차 검수 미실행이었어요. 현재 초기980행 검수는 수신했고 변경26행 재검수 대기·사람 미승인이에요. `confirmed_by_user=false`, `human_review=unreviewed`.
- 표본만 보지 말고980행 전부 검수해 주세요. 배치마다 같은 가족의7개 변형이 함께 있어 어미·축약 변경에 라벨이 흔들렸는지도 볼 수 있어요.

## 검수 프롬프트

> 확정 정책 `gemini_cross_model_20261128.md`와 `v3_contracts.py`, `nlu_schema.py`, `SYSTEM_PROMPT_NLU`를 먼저 읽어 주세요. source_text와 previous_question/target_slot_id, catalog_hints를 근거로 예상 JSON의 각 후보를 검수해 주세요. 작성자 rationale은 정답 근거가 아니므로 독립적으로 판정한 뒤 보조 설명으로만 보세요. 자동 검증 통과나 기존 파일럿 PASS를 이번 행의 의미적 PASS로 재사용하지 마세요.
>
> ① 횟수 정수/표시 심볼/동시 언급 정수 우선, ② 눈시림 발생 상황과 동일 주체 병행 추출, ③ 명시적 빈도·시간대 실제 사용의 current_routine 병행, ④ yes/denied 부정 및 부정 범위, ⑤ 전체 제품명 span이 일치하는 catalog hint만 연결을 우선 확인해 주세요.
>
> 발화에 없는 제품 속성·증상·시점·지속성·부위를 만들지 않았는지, 자기/타인/불명확 주체를 구분했는지, 증상·제품·슬롯을 빠뜨리지 않았는지 확인해 주세요. 후속 질문을 거부하거나 엉뚱한 내용을 답하면 질문한 값을 추정하지 않아야 해요. 근거 span은 현재 source_text의 정확한 부분 문자열이어야 해요. 모든 후보는 미확정이고 product.* 슬롯과 조언·진단·추천은 금지예요.
>
> 문제가 있으면 원문 raw 인용, 문제 후보 raw, 왜 맞지 않는지, 최소 수정안을 적어 주세요. 입력을 고쳐 정답을 정당화하지 마세요. 정책 자체가 미정이면 REVIEW로 표시하고 확정 PASS를 만들지 마세요.

## 특별히 확인할 해석 경계

1. **확정:** `선크림 안바름`은 단발 비도포와 과거 사용 중단을 구별해 제품 usage_state=`unknown`을 유지해요. 명시적인 사용 중단만 `stopped`예요. 해당7행은 입력·출력을 변경하지 않았어요.
2. **확정:** 타인이 명시적으로 사용을 중단/고려한 경우 `stopped`/`considering`, 실제 사용인 경우 `other_person`이에요. 별도 product subject 필드가 없는 현 계약에서 비사용 상태를 보존해요. 해당14행은 입력·출력을 변경하지 않았어요.
3. 공통 슬롯 어휘/의미 단위는 train/val에서 공유될 수 있지만 동일 조합의7개 변형은 한 분할에만 있어요. 가족140개·검증 가족14개인 통제된 조합 합성으로,980개의 독립 사용자 사례라고 평가하지 말아 주세요.

## 반환 JSONL 형식

아래는 **형식 예시일 뿐 실제 PASS가 아니에요.** `verdict`는 실제 검수 후 PASS/FAIL/REVIEW 중 선택해 주세요. `content_sha256`은 해당 요청의 값을 그대로 가져오고 실제 reviewer model/version을 기록해 주세요.

```json
{"row_id":"nlu-step2-0001","content_sha256":"<요청에 기록된 실제 SHA-256>","reviewer_model":"<실제 실행 모델/버전>","verdict":"<PASS|FAIL|REVIEW>","source_quotes":[],"candidate_quotes":[],"reason":"<원문과 판정의 연결>","suggested_fix":null,"human_approved":false}
```

초기 결과는 `reviews/step2_cross_model_critic.jsonl`에 보존돼 있어요. **이번 반환 위치는 `reviews/step2_cross_model_recheck.jsonl`을 권장해요.** 검수 후 후보 내용이 바뀌면 생성기의 `content_hash(row)`와 요청 해시를 재계산하고 변경 행을 다시 검수해 주세요. 이전 해시의 PASS를 변경 후 행에 재사용하면 안 돼요. 실제 사용자 승인과 학습 실행 여부는 검수 결과와 별도로 기록해 주세요.
