> f2154ab의 900턴 생성·414턴 검수 인계 당시 기록이에요. 현재 상태는 README.md를 보세요.

# PPO-37 Step 2 — 신규 합성 900턴·외부 재검수 인계

공유 브랜치는 `data/qlora-v4-rag-free`예요. v4는 브랜치 이름이며 v3 입력 계약과 `data/qlora/v2/` 경로를 유지해요.

**생성·자동 검증은 완료했고, 수정 14건 + 신규 400건의 외부 검수와 사람 확인은 대기 중이에요. 최종 학습 승인 상태가 아니에요.**

## 실제 분포

| 항목 | 결과 |
|---|---:|
| 전체 | 900 |
| solution / hold | 690 / 210 |
| train / val_internal | 810 / 90 |
| Hard Negative | 391 (43.4%) |
| 영어 관련 근거 solution | 240 (34.78%) |
| 사용한 공식 청크 / 전체 풀 | 78 / 151 |
| human_review=unreviewed | 900 |

모든 행은 `new_synthetic`이고 기존 v67·구 KB 종속 자료·파일럿을 재사용하지 않았어요. 생성은 세 Codex 담당(`gpt-6.2-sol`)이 나눠 했으며 외부 교차 검수를 로컬에서 대신하지 않았어요. 모든 문헌 청크와 인용·방해 ID는 공식 풀과 일치하고, `chunk_origins=reference_excerpt`예요. `kb_judgments`와 `[kb:...]`는 없고 HOLD의 문헌·인용 목록은 비어 있어요. 개발 프리뷰·생산 비활성·승인 필요·무저장 설정을 유지해요.

## 무엇이 바뀌었나요?

- `8ad8ecd`에서 가져온 실제 `gemini-cross-critic` 결과는 486 PASS / 14 FAIL이에요. 원본 500건의 content SHA-256 모두 검수 기록과 대조했어요.
- 14건의 `reason`/`suggested_fix`를 반영해 **답변만** 수정했어요. 입력을 보강해 기존 주장을 정당화하지 않았어요.
- 신규 400건은 solution 305 / hold 95예요. [생성 체크리스트](GENERATION_CHECKLIST.md)의 미제공 시점·제형·위치·수량·증상 양상 금지 조건을 적용했어요.
- 수정 전후 원문·입력·이전/현재 content SHA-256은 `reviews/stage2_14_corrections.jsonl`에 있어요. 기존 PASS 486건은 현재 900건 파일과 해시가 같아요.

## 사용·검수할 파일

- **현재 후보:** `qlora_solution_hold_v2.jsonl` (900행)
- **외부 검수 요청:** `reviews/stage2_414_critic_requests.jsonl` (수정 14 + 신규 400)
- **분할 요청:** `reviews/requests_414/` (29~30행씩 14개 배치)
- **요청 해시:** `reviews/stage2_414_request_manifest.json`
- **추가 생성 원본:** `stage2_remaining_400.jsonl`, `authoring/*remaining*_synthetic_fact_trace.jsonl`
- **과거 배정 계획:** `stage2_checkpoint_plan.json`은 500턴 작성 당시의 계획이에요. 현재 생성 잔여량은 0건이며 검수 잔여량 414건은 위 요청 manifest에 기록해요.
- **원본 감사용:** `qlora_solution_hold_v2_checkpoint_500.jsonl`, `reviews/stage2_500_critic.jsonl`, 기존 `stage2_inputs_500.jsonl`/`stage2_answers_500.json`. **이 500턴 동결본에는 수정 전 FAIL 14건이 남아 있어요. 학습 후보는 반드시 위 900턴 파일을 보세요.**

보조 합성 발화·이전 확인은 실제 사용자 기록이 아니며 모델에 자동 전달되지 않아요. 실제 모델 입력은 각 행의 user JSON이에요.

## 자동 검증·재현

cos-agent 디렉터리에서 실행해요. `uv`가 PATH에 없으면 `python -m uv`를 써요.

```powershell
uv run --locked python scripts/build_qlora_stage2_900.py
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/qlora_solution_hold_v2.jsonl --stage1 --report outputs/qlora_step2_20261125/stage2_900_validator.json
uv run --locked python scripts/check_qlora_stage2_checkpoint.py --input data/qlora/v2/qlora_solution_hold_v2.jsonl --expected-count 900 --report outputs/qlora_step2_20261125/stage2_900_quality.json
```

`--stage1`의 형식·900행·비율·가족/그룹 분할 검사는 `passed=true`, 오류 0건이에요. `validation/stage2_900_validator.json`과 `stage2_900_quality.json`에 원문 결과가 있어요. 입력/전체 답변 중복은 0건이며 이것을 의미적 무결성이나 독립 검수 PASS로 해석하지 않아요. 원본 소스 매니페스트는 저장소 루트에서 `python tools/verify_source_manifest.py`로 27건 확인·실패 0건이에요. KB·manifest·코어는 변경하지 않았어요.

현재 데이터 SHA-256: `23600af503ae1ee4cb177d2646513af5b78ed35d9385a6e88f5308677a7b0b6a`

공식 청크 풀 SHA-256: `29147e4560ca31d532edfdb795773b461043d2c9d60184c78f69cd9d05266001`

## Qwen3-4B-Instruct-2507 길이 측정

실제 고정 리비전 토크나이저와 chat template 기준 최대 1,800토큰, p95 1,534토큰이에요. 길이 2,048에서 잘리는 행은 0건이에요. `validation/stage2_900_token_report.json`에 리비전·환경·행별 길이 경로를 기록했어요. 학습이나 GPU 메모리 검증은 하지 않았고 assistant-only loss 마스킹은 학습 파이프라인에서 별도 확인해야 해요.

## 외부 재검수 후 남은 게이트

검수자는 414건의 실제 입력·답변·허용 근거를 읽고 `row_id`, 실제 `critic_model`, `decision`, 요청 파일과 같은 `content_sha256` 및 문제 시 `violated_rule`, `offending_span`, `evidence_ref`, `reason`, `suggested_fix`를 기록해 주세요. 방해 청크는 부정형·간접 언급까지 금지하며 사용자 사실은 실제 입력과 대조해 주세요.

414건이 실제 PASS하고 내용 해시가 일치하면 기존 486 PASS와 통합해 `reviews/stage1_critic.jsonl`을 만들 수 있어요. 고위험 행 최소 10%의 사람 확인까지 마친 뒤 `--stage1 --review-file data/qlora/v2/reviews/stage1_critic.jsonl` 최종 게이트를 실행해요. **현재 그 결과 파일·PASS·사람 승인을 대신 만들지 않았어요.**
