# Cross-Model(Gemini) 전수 검수 요약 — PPO-46 NLU Step 2 (980턴)

## 개요
- **대상 브랜치 / 기준 커밋**: `data/nlu-v1-step2` (`596a8ebeb8c024517bd65d1e666f5cdde2635fbc`)
- **검수 대상**: `data/nlu/v1/nlu_sft_v1.jsonl` **980턴 전수(배치 01~14, 비표본)**
- **검수 주체**: Gemini (`gemini-cross-model-antigravity`, GPT/Codex와 별도 모델 계열 Cross-Model Critic)
- **전행 결과 JSONL**: [step2_cross_model_critic.jsonl](step2_cross_model_critic.jsonl) (980행, `content_sha256` 980/980 일치)
- **원본 미수정 확인**: `nlu_sft_v1.jsonl`, `build_nlu_v1_step2.py`, 파일럿 49건, 코어 계약·검증기·KB는 일절 수정하지 않았습니다. `human_approved: false` 유지.

---

## 집계 결과

- **PASS**: **936** (95.5%)
- **FAIL**: **9** (0.9%)
- **REVIEW**: **35** (3.6%)

| 배치 | 주 버킷 | 검수 | PASS | FAIL | REVIEW | 비고 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 01–02 (`0001..0140`) | `turn1_utterance` | 140 | 139 | 0 | 1 | `0042` (`손`→`손바닥`) |
| 03–04 (`0141..0280`) | `turn2_followup` | 140 | 140 | 0 | 0 | 100% PASS |
| 05–06 (`0281..0420`) | `denied_polarity` | 140 | 126 | 3 | 11 | `val_internal` FAIL 3 + REVIEW 11 |
| 07–08 (`0421..0560`) | `other_subject` | 140 | 119 | 3 | 18 | FAIL 3 + 경계2 14 + `coverage_gaps` 4 |
| 09–10 (`0561..0700`) | `high_risk_symptom` | 140 | 140 | 0 | 0 | 100% PASS |
| 11–12 (`0701..0840`) | `product_mention` | 140 | 132 | 3 | 5 | FAIL 3 + `coverage_gaps` 4 + `0791` (`손`→`손바닥`) |
| 13–14 (`0841..0980`) | `no_signal_noise` | 140 | 140 | 0 | 0 | 100% PASS |
| **합계** | — | **980** | **936** | **9** | **35** | **확정 정책 5종 위반 0건** |

---

## FAIL 9건 (필수 수정)

모두 동일한 단일 원인(`coverage_gaps` atom의 `"귀와 목을 차단제 바를 때 빼먹었어요"`가 실제 도포 행위를 명시하고 있음에도 `차단제`를 `usage_state: "unknown"`으로 라벨링)입니다.

- **`val_internal` (`denied_polarity`, `self`)**: `nlu-step2-0414`, `0415`, `0416` → `usage_state: "using"`
- **`train` (`other_subject`, `other`)**: `nlu-step2-0494`, `0495`, `0496` → `usage_state: "other_person"`
- **`train` (`product_mention`, `self`)**: `nlu-step2-0760`, `0761`, `0762` → `usage_state: "using"`

---

## REVIEW 35건 (정책 정리 및 권고)

1. **`sun.coverage_gaps` 부분 누락 (`"귀랑 목은 차단제 안 발랐어요"` / `"누락했어요"`, 12건)**
   - 대상: `0417..0420` (`val_internal`), `0491..0493, 0497` (`other_subject`), `0757..0759, 0763` (`product_mention`)
   - **권고 (방안 A)**: FAIL 9건과 동일한 `coverage_gaps` atom이므로, 도포 중 일부 부위 누락으로 통일해 `usage_state`를 `using`(`other`는 `other_person`)으로 정렬하고 `"안 발랐어요"` 변형도 `"바를 때 빼먹었어요"`/`"누락했어요"` 계열로 정리.
2. **해석 경계 1 — 단발 비도포 `"선크림 안 발랐어요"` / `"선크림 안바름"` → `usage_state="unknown"` (7건: `0407..0413`, `val_internal`)**
   - **권고**: **PASS 수용(현행 `unknown` 유지)**. `not_using`이 없는 현재 스키마에서 과거 중단(`stopped`)으로 오분류하지 않는 가장 안전한 선택.
3. **해석 경계 2 — `other_subject` + `stopped` / `considering` (14건: `0533..0539`, `0540..0546`)**
   - **권고**: **PASS 수용(현행 `stopped` / `considering` 유지)**. `ProductMention`에 별도 `subject` 필드가 없는 현재 계약 한계에서 현재 타인 사용(`other_person`)으로 오독되는 위험보다 비사용 상태 보존이 안전.
4. **원문-값 소폭 과명시 (`"두 세정제를 손에서 혼합해요"` → `"두 세정제를 손바닥에서 섞음"`, 2건: `0042`, `0791`)**
   - **권고**: 해당 변형 원문을 `"두 세정제를 손바닥에서 혼합해요"`로 맞추거나 슬롯 값을 `"두 세정제를 손에서 섞음"`으로 정렬.
