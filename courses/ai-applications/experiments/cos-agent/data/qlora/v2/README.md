# PPO-37 Step 2 — RAG-free QLoRA 신규 합성 900턴 최종 제출

브랜치: `data/qlora-v4-rag-free` · 개인 진행·raw 기록: [PPO-45](https://linear.app/ppopy/issue/PPO-45).

## 최신 검수 상태

팀원이 반영한 `83c6953` 기준으로 **900/900 gemini-cross-critic PASS**, 사람 승인 메타데이터 **900/900 approved**(고위험 295/295)를 확인했어요. 현재 파일과 외부 검수의 내용 해시가 맞고, 공식 `--stage1 --review-file` 최종 게이트도 오류·경고 0건으로 통과했어요. 사람 승인은 제출된 팀원 기록을 대조한 것이며 PR 작성 중 새 사람 검수를 수행한 것은 아니에요.

| 항목 | 결과 |
|---|---:|
| solution / hold | 690 / 210 |
| train / val_internal | 810 / 90 |
| Hard Negative | 391 / 900 (43.44%) |
| 영어 관련 근거 solution | 240 / 690 (34.78%) |
| 사용한 공식 청크 / 전체 풀 | 78 / 151 |

100% `new_synthetic`, v67/구 KB 데이터 재가공 없음, `kb_judgments`·`[kb:...]` 없음, HOLD 문헌·인용 목록 없음. 공식 청크 필드를 보존하고 미상·버전 의미와 `development_preview`, `production_enabled=false`, `requires_approval=true`, `saved=false`를 유지해요. KB·계약·코어·소스 매니페스트 내용은 바꾸지 않았어요.

## 현재 사용할 파일

- 학습 후보: `qlora_solution_hold_v2.jsonl`
- 최종 외부 검수: `reviews/stage1_critic.jsonl`
- 이번 최종 게이트 원문: `validation/stage2_900_final_review_validation.json`
- 실제 파일·검수 해시 및 승인 메타데이터 대조: `validation/stage2_900_final_review_receipt.json`

현재 데이터 SHA-256: `99182590f83bc3dad9e3cb71c9153f418642b6aaf7d97ebcc728ac68d0425cac`

## 검증 재실행

cos-agent 디렉터리에서 실행해요. `uv`가 PATH에 없으면 `python -m uv`를 써요.

```powershell
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/qlora_solution_hold_v2.jsonl --stage1 --review-file data/qlora/v2/reviews/stage1_critic.jsonl --report outputs/qlora_final_validation.json
```

저장소 루트에서 `python tools/verify_source_manifest.py`는 `{"checked":27,"failed":[]}`예요. Windows의 CRLF 체크아웃은 원본 Git blob과 manifest 해시를 먼저 대조한 뒤 원본 LF 바이트로 복원했으며 Git 소스 내용은 수정하지 않았어요.

## 과거 기록·재조립 주의

500턴(486 PASS/14 FAIL), 추가 400턴, 900턴(883 PASS/17 FAIL), 14건·17건 수정 전후 raw와 요청 해시를 보존했어요. `CHECKPOINT_*_README.md`, 과거 `stage2_*_requests`·수정 기록·당시 validation은 **해당 시점의 감사 기록**이에요. 그 안의 재검수 대기·unreviewed·이전 데이터 해시는 현재 최종 결과와 구분해요.

`build_qlora_stage2_900.py`와 체크포인트 조립 스크립트는 **생성 당시 미승인 자료 재현용**이에요. 현재 승인된 파일 위에 실행하면 생성 당시 unreviewed 메타데이터로 재조립하므로, 재현은 반드시 별도 작업 사본에서 진행하고 최종 승인 파일은 덮어쓰지 마세요.

메시지 원문은 `8bedc33`과 900건 모두 같아요. 당시 실제 Qwen3-4B-Instruct-2507 토큰 측정(최대 1,800 / p95 1,534 / 길이 2,048에서 잘림 0건)은 그대로 적용되지만, 당시 token report의 파일 해시는 승인 메타데이터 반영 전 해시예요. 실제 QLoRA 학습·GPU 메모리 검증·main 병합은 이번 제출에 포함하지 않아요.
