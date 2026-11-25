> 과거 500턴 생성 직후의 기록이에요. 현재 제출 안내는 README.md를 보세요.

# PPO-37 Step 2 — 500턴 중간 인계

공유 브랜치는 `data/qlora-v4-rag-free`예요. v4는 브랜치 이름이며, 기존 v3 입력 계약과 `data/qlora/v2/` 저장 경로는 변경하지 않았어요.

900턴 목표 중 **500턴을 신규 작성한 체크포인트**예요. 사용자의 요청에 따라 여기서 멈추고 다른 팀원의 기기에서 교차 모델 검수를 진행해요. 남은 **400턴(안내 305 / 보류 95)**은 재개 후 작성하며, 이 묶음은 최종 학습 승인 자료가 아니에요.

## 생성 결과

| 항목 | 실제 건수 |
|---|---:|
| 전체 | 500 |
| solution / hold | 385 / 115 |
| train / val_internal | 455 / 45 |
| Hard Negative | 218 (43.6%) |
| 영어 관련 근거가 있는 solution | 130 / 385 (33.77%) |
| 사용한 공식 청크 / 전체 풀 | 50 / 151 |
| 사람 검수 unreviewed | 500 |

- 생성 담당: Codex의 `gpt-6.2-sol` 세 담당. 로컬 교차 모델 검수는 하지 않았어요.
- `source_origin=new_synthetic` 100%이며 기존 v67·파일럿 답변을 재사용하지 않았어요.
- 공식 풀 `data/rag/chunks.jsonl`의 청크 사전을 그대로 사용했고 `chunk_origins=reference_excerpt`예요. 모든 151개를 사용했다는 뜻은 아니에요.
- `kb_judgments` 및 `[kb:...]` 인용은 없고, HOLD에는 청크·허용 인용·방해 인용을 넣지 않았어요.
- 미확인 값과 출처를 구분하고 `development_preview`, `production_enabled=false`, `requires_approval=true`, `saved=false`를 유지해요.
- 작성 후 입력에서 빠진 시간·상태를 답변만 단정하는 표현을 수정했고, 단순 개봉일 미상을 버전 불일치 Hard Negative로 분류한 10건을 일반 사례로 변경했어요. 이것은 작성 품질 점검이며 독립 Critic PASS가 아니에요.

## 파일

- `qlora_solution_hold_v2_checkpoint_500.jsonl`: 실제 학습 후보 500행이에요.
- `stage2_inputs_500.jsonl`, `stage2_answers_500.json`: 현재 입력·답변의 고정 재조립 자료예요. 초기 작성 이력 전체를 뜻하지 않아요.
- `authoring/*_synthetic_fact_trace.jsonl`: 합성 발화·이전 확인과 슬롯 출처 기록이에요. **모델 입력은 JSONL의 user 메시지**이며 이 보조 기록을 모델이 읽었다고 가정하면 안 돼요.
- `reviews/stage2_500_critic_requests.jsonl`: 각 행의 실제 입력·답변·근거·content SHA-256을 담은 **검수 요청**이에요. 검수 결과가 아니에요.
- `reviews/requests_500/`: 29~30행씩 17개 외부 검수 배치예요.
- `reviews/stage2_500_critic_request_manifest.json`: 배치·데이터·풀의 해시예요.
- `validation/`: 자동 검증, 토큰 측정, 인계 기록이에요.
- `stage2_checkpoint_plan.json`: 전체 목표와 이번 ID 배정, 재개할 잔여 범위예요.

## 자동 검증

cos-agent 디렉터리에서 실행해요. `uv`가 PATH에 없으면 `python -m uv`를 사용할 수 있어요.

```powershell
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/qlora_solution_hold_v2_checkpoint_500.jsonl --enforce-ratios --report outputs/qlora_step2_20261125/merged/validator.json
uv run --locked python scripts/check_qlora_stage2_checkpoint.py --input data/qlora/v2/qlora_solution_hold_v2_checkpoint_500.jsonl --expected-count 500 --report outputs/qlora_step2_20261125/merged/checkpoint_quality.json
uv run --locked python scripts/build_qlora_stage2_checkpoint.py
```

첫 명령의 결과는 `passed=true`, `error_count=0`, 경고 0건이에요. 입력·답변 전체 중복과 표면적 방해 주제 후보도 0건이지만, **의미적 정확성이나 교차 모델 검수 통과를 증명하지 않아요**. 900턴 미만이므로 `--stage1` 최종 게이트는 실행하지 않았어요. 외부 검수 전이므로 `--review-file` 승인 게이트도 아직 미충족이에요.

저장소 루트의 `python tools/verify_source_manifest.py`는 `{"checked":27,"failed":[]}`예요. Windows 체크아웃의 CRLF 차이만 원본 Git blob과 27개 manifest 해시를 먼저 대조한 뒤 원본 LF 바이트로 복원했어요. KB·코어·manifest의 Git 내용 변경은 없어요.

### Qwen 토큰 길이

`Qwen/Qwen3-4B-Instruct-2507`의 고정 리비전 토크나이저로 실제 chat template을 적용했어요. 최대 1,773토큰, p95 1,527토큰으로 이 파일은 2,048 길이에서 잘리지 않아요. 1,024에서는 244행이 잘리고 172행은 답변 시작까지 도달하지 못해요. 실제 QLoRA 학습·GPU 메모리 시험은 하지 않았어요. 네이티브 템플릿에는 generation 블록이 없으므로 학습 시 assistant-only loss 마스킹은 별도로 확인해야 해요.

## 다른 기기의 Critic에게

1. 위 데이터·검수 요청과 동일한 공식 청크 풀을 전달하고 manifest의 해시를 대조해요.
2. 생성 모델과 구분되는 실제 검수 모델명을 기록하고, 입력·답변·허용 근거를 전부 읽어 주세요.
3. 방해 청크는 인용뿐 아니라 주제의 간접 언급·부정형 언급도 금지해요. 입력에도 있는 독립적인 사실과 방해 문헌에서만 가져온 주제를 구분해요.
4. 용도≠실제 행동, 증상 부위≠사용 부위, unknown≠없음, 제품 미상≠다른 버전을 확인해요. 문헌의 범위를 제품 성능·진단·치료 효과로 확대하지 않아요. HOLD에서 루틴·제품·행동 안내가 새어 나오지 않는지 확인해요.
5. 각 결과는 `row_id`, `critic_model`, `decision`, `content_sha256`을 기록하고, 문제 시 `violated_rule`, `offending_span`, `evidence_ref`, 이유와 수정 제안을 함께 남겨 주세요. `content_sha256`은 검수 요청 값에 연결해요.
6. FAIL 수정 후에는 내용 해시를 다시 계산하고 바뀐 행을 다시 검수해요. 사람이 확인하기 전 `human_review=approved`로 바꾸지 않아요.

이 체크포인트에는 Critic 결과·사람 승인·900턴 완료 PR이나 완료 Archive를 만들지 않았어요. 남은 생성과 최종 게이트는 goal 재개 후 이어가요.
