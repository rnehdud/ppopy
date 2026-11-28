# Cross-Model(Gemini) 재검수 및 사람 승인 완료 보고 — PPO-46 NLU Step 2 (980턴)

## 개요
- **대상 브랜치 / 기준 커밋**: `data/nlu-v1-step2` (`dbd788d36b42f7b4a676ef7dbaa3a8afca8994e2`)
- **검수 주체**: Gemini (`gemini-cross-model-antigravity`, GPT/Codex와 별도 모델 계열 Cross-Model Critic)
- **최종 결과 파일**: [step2_cross_model_critic_final.jsonl](step2_cross_model_critic_final.jsonl) (980행 전수 `PASS`, `content_sha256` 980/980 일치)
- **초기 검수 파일 보존**: [step2_cross_model_critic.jsonl](step2_cross_model_critic.jsonl) (`596a8eb` 기준 936 PASS / 9 FAIL / 35 REVIEW) 원형 유지
- **승인 상태**:
  - `provenance.critic_status = "passed"` (980/980)
  - `provenance.human_review = "approved"` (980/980, 사용자 명시적 승인 반영)
  - `confirmed_by_user = false`, `runtime_invariants` (`development_preview`, `production_enabled=false`, `requires_approval=true`, `saved=false`) 전 행 유지

---

## 재검수 요약 (980 / 980 PASS)
- **변경된 26행 전수 재검수**: **26/26 PASS**
  - `method.mixing` v6 (`0042`, `0791`): `"두 세정제를 손바닥에서 혼합해요"` 원문 정렬 확인
  - `coverage_gaps` (`0414..0420` [val], `0491..0497` [other], `0757..0763` [self], `0099`·`0102`·`0105` [공통 atom]): 전 행 도포 중 누락 표현 + `using`/`other_person` 정렬 확인
- **미변경 954행**:
  - 기존 Cross-Model PASS 933행 해시 100% 일치
  - 정책 확정 21행(`0407..0413` 단발 비도포 `unknown`, `0533..0546` 타인 `stopped`/`considering`) 해시 100% 일치 및 PASS 수용 완료

---

## 최종 검증 통과
- `scripts/validate_nlu_dataset.py --input data/nlu/v1/nlu_sft_v1.jsonl --min-rows 800 --enforce-buckets`: `passed=true`, `error_count=0`, `warnings=[]`
- `scripts/audit_nlu_v1_step2.py`: `passed=true`, `cross_model_critic_performed=true`, `human_approved=true`
- `pytest -q tests/test_nlu_step0.py tests/test_v3_contracts.py`: `11 passed`
- `python tools/verify_source_manifest.py`: `{"checked": 27, "failed": []}`
