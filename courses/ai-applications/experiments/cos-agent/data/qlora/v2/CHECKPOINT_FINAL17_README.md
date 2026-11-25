> 8bedc33의 최종 17건 수정·재검수 대기 당시 기록이에요. 최신 제출 상태는 README.md를 보세요.

# PPO-37 Step 2 — 900턴·최종 17건 답변 수정 및 재검수 인계

브랜치: `data/qlora-v4-rag-free`. 개인 진행·raw 누적 기록: [PPO-45](https://linear.app/ppopy/issue/PPO-45).

**900턴 중 기존 PASS 883건은 현재 내용 해시가 같아요. 마지막 FAIL 17건은 답변만 수정했고 외부 재검수를 기다려요. 900/900 PASS나 사람 승인 완료 상태는 아니에요.**

## 실제 변경 범위

- 기준: `9eb1d30`의 통합 `reviews/stage1_critic.jsonl` (883 PASS / 17 FAIL).
- solution 11건·hold 6건의 `reason`/`suggested_fix`를 입력과 대조해 미제공 제형·용기·접촉 강도·자세·시간·상태와 타인 제품 사용 전제를 제거했어요.
- **900건 모두 user JSON 문자열과 비메시지 메타데이터가 기준 커밋 그대로**예요. assistant 답변만 정확히 17건 달라요.
- 이전 수정 14건의 실제 PASS를 포함한 나머지 883건의 content SHA-256은 기존 검수와 같아요.
- `human_review=unreviewed` 900건 유지. 고위험 295건 중 최소 30건의 사람 확인은 아직 0건이며 추후 사람이 진행해요.

## 현재 파일과 감사 기록

| 용도 | 파일 |
|---|---|
| 현재 900턴 후보 | `qlora_solution_hold_v2.jsonl` |
| **17건 재검수 요청·재계산 해시** | `reviews/stage2_17_critic_requests.jsonl` |
| 요청 ID·파일/데이터 해시 | `reviews/stage2_17_request_manifest.json` |
| 이전 Critic 원문·입력·수정 전후·전후 해시 | `reviews/stage2_17_corrections.jsonl` |
| 답변만 수정하는 재조립용 패치 | `reviews/stage2_17_answer_revisions.json` |
| 변경 범위·사람 확인 대기 증빙 | `validation/stage2_17_change_verification.json` |

`stage1_critic.jsonl`은 **수정 전 900턴에 대한 실제 외부 검수 원본**이에요. 현재 수정 17건에는 이전 FAIL/해시가 남아 있으므로, 재검수 결과를 받기 전까지 최종 PASS 파일로 취급하지 않아요. 결과를 대신 변경하거나 PASS를 만들지 않았어요.

이 기준 검수의 LF 동결 복사본은 `reviews/stage2_900_critic_before_final17.jsonl`이에요. 재조립은 이 동결본에 연결하므로 나중에 `stage1_critic.jsonl`이 실제 재검수 결과로 갱신되어도 이번 수정 이력을 재현할 수 있어요.

이전 500턴·414턴 요청·14건 수정 기록과 `stage2_remaining_400.jsonl`은 당시 생성/검수 원본으로 보존해요. 재조립 스크립트가 이 원본에 14건 수정과 최종 17건 답변 패치를 순서대로 적용해요. 현재 후보와 과거 요청의 데이터 해시가 다른 것은 이 수정 이력을 구분하기 위해서예요. 당시 안내는 `CHECKPOINT_500_README.md`, `CHECKPOINT_900_README.md`에 있어요.

## 분포와 검증

- 900턴 = solution 690 / hold 210, train 810 / val_internal 90.
- Hard Negative 391 (43.44%), 영어 관련 근거 solution 240/690 (34.78%).
- 100% `new_synthetic`, KB 판정 미포함, 공식 151개 풀 중 78개 사용·포함된 모든 청크 필드 일치. HOLD 청크·인용 목록 없음.
- 미상·버전 의미와 `development_preview`, `production_enabled=false`, `requires_approval=true`, `saved=false`를 유지해요. KB·계약·코어·소스 매니페스트는 바꾸지 않았어요.
- 공식 `--profile rag-free --stage1` 자동 검증: passed=true, 오류·경고 0건. 원문은 `validation/stage2_900_validator.json`에 있어요.
- 구조·풀 일치 결과는 `validation/stage2_900_quality.json`에 있어요. 자동 검사 합격은 의미적 정확성·외부 PASS·사람 승인과 달라요.
- 원본 소스 매니페스트 검증: `{"checked":27,"failed":[]}`.
- 현재 파일의 Qwen 토큰 측정은 `validation/stage2_900_token_report.json`과 행별 CSV에 있어요. 실제 QLoRA 학습·GPU 메모리 시험은 하지 않았어요.

## 재조립

cos-agent 디렉터리에서 실행해요. `uv`가 PATH에 없으면 `python -m uv`를 써요.

```powershell
uv run --locked python scripts/build_qlora_stage2_900.py
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/qlora_solution_hold_v2.jsonl --stage1 --report outputs/qlora_step2_20261125/final17_validator.json
```

17건 요청은 앞선 소배치 생성 분포를 맞추기 위한 파일이 아니라 **이번 FAIL 17건만 대상으로 하는 최종 재검수 파일**이에요. 검수자는 실제 입력·수정 답변·허용 근거를 읽고 요청에 있는 `content_sha256`으로 결과를 연결해 주세요.

실제 17건 PASS와 해시가 확인되면 기존 883 PASS와 통합하고, 고위험 사람 확인 30/295 이상을 기록한 뒤 `--stage1 --review-file data/qlora/v2/reviews/stage1_critic.jsonl` 최종 게이트·PR·머지를 진행해요. 그 전에는 `human_review=unreviewed`를 유지해요.

현재 데이터 SHA-256: `162a8f251020a3dbda250f0a401a673df0427a8d1508e58aaed2cf589dbadf2c`
