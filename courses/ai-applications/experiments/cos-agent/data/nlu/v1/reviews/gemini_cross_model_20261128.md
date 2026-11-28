# PPO-46 NLU 파일럿 49건 — Cross-Model(Gemini) 검수 및 확정 정책 반영 기록 (2026-11-28)

## 개요

- **기준 커밋**: `5aab0a7fc325c33372c0a1140845f913040ed36e` (`data/nlu-v1-pilot-critic`)
- **검수 주체**: Gemini (Antigravity, GPT/Codex와 별도 모델 계열 Cross-Model 전수 검수)
- **수정 전 `pilot_nlu_v1.jsonl` SHA-256**: `0c4c7877c9d26dbb4d7daf09f2a00e30df9eeb479413809919cd374263e1f1e7`
- **수정 후 `pilot_nlu_v1.jsonl` SHA-256**: `c5f96332f52c6ad5e5a5e36e0a1249c55cc04f3818f352fd42388cb4ef443cbe`
- **미수정 경계**: `beauty_agent/v3_contracts.py`, `beauty_agent/nlu_schema.py`, `beauty_agent/slm/prompt_builder.py`, `scripts/validate_nlu_dataset.py`, KB 파일은 수정하지 않았습니다.
- **메타데이터 유지**: `confirmed_by_user=false`, `human_review="unreviewed"`, `base_zero_shot_executed=false`, `training_executed=false`를 그대로 유지합니다.

---

## 확정된 라벨링 정책 (Step 1 파일럿 반영 + Step 2 공통 기준)

1. **`cleansing.steps` 정수 vs 규칙 심볼 분리 (`nlu-pilot-0009`)**
   - 횟수 질문 응답은 순수 횟수 발화(`"한 번만 해요."` → `1`)로 정리해 `according_to_product_removal_instructions` 규칙 심볼과의 모호성을 제거한다.
   - 한 발화에 횟수와 표시 준수가 모두 언급되면 **명시적 횟수(정수) 우선**으로 추출하고, `according_to_product_removal_instructions` 전용 발화는 Step 2에서 별도 추가한다.
2. **눈시림 발생 상황 `skin.eye_symptom_context` 병행 추출 (`nlu-pilot-0014`, `nlu-pilot-0028`)**
   - 눈시림 발생 상황(세안/물/땀/선크림 등)이 발화에 명시된 경우, `symptom_candidates`(`eye_stinging`)와 `slot_candidates`의 `skin.eye_symptom_context`를 주체(`self`/`other`)에 맞춰 함께 추출한다.
3. **빈도·시간대 포함 사용 루틴 `method.current_routine` 병행 추출 (`nlu-pilot-0007`, `nlu-pilot-0026`, `nlu-pilot-0036`)**
   - `"매일"`, `"저녁에는"`, `"아침저녁"` 등 빈도·시간대가 명시된 실제 사용 표현은 `product_mentions` 및 기타 루틴 슬롯(`method.sequence` 등)과 함께 `method.current_routine`을 일관되게 병행 추출한다.
   - 빈도·시간대가 없는 단순 사용 표현(`0037`, `0040`, `0042` 등)은 `product_mentions`만 추출한다.
4. **기존 검증 정책 유지**
   - `sun.water_contact` / `sun.sweat` 부정 발화(`0019`, `0020`)는 이중부정 없이 `("yes", polarity="denied")`로 통일한다.
   - 부분 문자열 카탈로그 힌트(`0038`, `0042`)는 전체 제품명 span이 정확히 일치할 때만 `matched_catalog_hint`를 연결하고, 아니면 `null`을 유지한다.

---

## 변경된 5건 요약

| ID | 변경 내용 |
| --- | --- |
| `nlu-pilot-0007` | `"저녁에는 보습제를 먼저 바르고 그다음 차단제를 발라요"`에 `method.current_routine` (`"저녁 보습제 후 차단제 사용"`) 병행 추가 |
| `nlu-pilot-0009` | 원문을 `"한 번만 해요."`로 정리해 `cleansing.steps = 1`과 표시 준수 심볼 간 모호성 제거 |
| `nlu-pilot-0014` | `skin.eye_symptom_context` (`"씻을 때마다"`, `subject="self"`) 병행 추가 |
| `nlu-pilot-0028` | `skin.eye_symptom_context` (`"선크림을 쓰고"`, `subject="other"`) 병행 추가 |
| `nlu-pilot-0036` | `method.current_routine` (`"라임 로션 A 매일 사용"`, `subject="self"`) 병행 추가 |

---

## 최종 판정 및 검증

- **Cross-Model(Gemini) 49건 전수 검수**: **49/49 PASS** (계약 위반 0건, 정책 일관성 불일치 0건)
- `scripts/validate_nlu_dataset.py --min-rows 40 --enforce-buckets`: `passed=true`, `error_count=0`, `warnings=[]`
- `scripts/check_nlu_v1_pilot.py`: 49행 · 7버킷×7건 · 분할 누수 0건 · 해시 49/49 일치
- `pytest -q tests/test_nlu_step0.py tests/test_v3_contracts.py`: 통과
- `python tools/verify_source_manifest.py`: `{"checked": 27, "failed": []}`
