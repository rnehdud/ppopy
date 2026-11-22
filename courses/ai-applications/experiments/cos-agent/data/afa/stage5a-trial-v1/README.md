# Stage 5A-2 — 256 step 시험 학습 결과

해당 버전의 실험 기록이다. 현재 에이전트에서 AFA가 맡는 역할은 [목표 구조](../../../docs/agent-runtime-target.md)를 참고한다.

목적: **실제 PPO 수집·업데이트·저장·재로드 경로가 기존 환경에서 동작하는지 확인한다.** Stage 5A-1은 학습하지 않은 초기화 검사였고, 이번 단계에서 처음 `learn()`을 실행했다. 연구 성능 우위나 실제 사용자 효용을 검증한 단계는 아니다.

## 전체 진행에서의 위치

Stage 0~4 환경·보상·기준선 → Stage 5A-1 학습 연결 준비 → **현재: Stage 5A-2 실제 시험 학습 완료** → v2 의미 계약·과제/응답 세계·평가 계획 → 기준선·개선 여지 확인 → 본 비교 학습 → 독립 평가 → 에이전트 연결.

## 변경하지 않은 실험 조건

| 항목 | 이번 실행 |
| --- | --- |
| 설정 | `../stage5a-v1/config.json` 그대로 사용 |
| 자료 | train 6개 합성 세계, 한 사례당 B-C01/B-C02 중 카드 1개 |
| 학습 | MaskablePPO/MlpPolicy, CPU, seed 0, 총 256 step |
| rollout / batch / epoch | 32 / 16 / 4, 총 8 rollout |
| 목적함수 | gamma=1, shaping=0, 기존 질문 비용·종료 손실·안전 게이트 유지 |
| 평가 | 동일 train 6세계에 결정적 마스크 적용 실행; val/test 점수 계산 안 함 |
| 조정 | 결과를 보고 seed·학습량·보상·분할을 바꾸거나 추가 학습하지 않음 |

`256 step`은 환경 행동 256회이며 독립 사례 256개가 아니다. 학습·진단은 같은 작은 train 자료를 사용한다. 모든 참조는 기존 엔진의 합성 기계적 결과이며 사람/전문가 승인 정답이 아니다.

## 실제로 확인한 것

- collector가 수집한 **256개 행동 모두 당시 마스크를 준수**했다. invalid action hard error는 유지했다.
- **32 epoch update, 파라미터별 Adam step 64회**를 저장된 optimizer에서 확인했다. rollout 8개 × epoch 4 × batch 2의 실행 예산과 일치한다.
- 초기 모델과 비교해 **12/12 파라미터 텐서가 변경**됐다. 최대 절대 변화 약 0.023922. 가중치와 기록된 로그 수치는 모두 유한했다.
- CSV에는 32~256 step의 rollout 기록 8행이 있다. SB3는 최적화 전에 로그를 dump하므로 마지막 CSV의 update 수를 최종 optimizer 횟수로 오해하지 않는다. 최종 횟수는 모델에서 별도 확인했다.
- 저장 직전/직후 및 **별도 프로세스 재로드 후** train 실행 결과가 같았다. 전이·보상·마스크·step당 dispatch 1회·유한 수치·종료를 검사했다.
- 공식 mask-aware evaluator도 실행했다. helper의 추가 2 episode는 API 점검이며 새 독립 세계가 아니다.

## 작은 train 진단 결과

| 지표 | 학습 전 초기 정책 | 256 step 학습 후 |
| --- | ---: | ---: |
| 종료 계약 충족 | 1/6 | **6/6** |
| 평균 질문 수 | 1.167 | **2.500** |
| 평균 return | -5.333 | **-2.500** |
| 성급한 보류 | 5/6 | **0/6** |
| 초안 / 보류 | 0 / 6 | **5 / 1** |

초기 정책은 성급히 보류해서 질문 수가 적었다. 학습 후 질문 수가 늘어도 올바른 초안/보류로 끝내므로 종료 손실이 줄었다. 6/6은 KB 기반 종료 계약 충족이며 임상 정확도나 독립 평가 정확도가 아니다. 마지막 1개 보류는 v1이 정의한 올바른 보류다.

기존 Stage 4 train 기준선은 규칙 3.333회, 탐욕 2.500회였다. 이번 PPO의 2.500회는 **가장 강한 기존 탐욕 기준선과 같고**, 사전에 계산한 train 공개 정보 기반 최적 비용에도 도달한다. 따라서 PPO의 질문 효율 우위를 입증한 결과로 표현하지 않는다. val/test 결과는 계산하지 않았다.

## 산출물과 재현

`cos-agent/`에서:

```powershell
# 실제 완료한 학습 명령. 기존 폴더는 덮어쓰지 않으므로 재실행 시 새 이름 사용.
uv run --locked --group rl-train python -m beauty_agent.afa.ppo train --run-dir ../../../../outputs/afa-stage5a-trial-v1

# 추가 학습 없이 저장 모델 실행
uv run --locked --group rl-train python -m beauty_agent.afa.ppo evaluate --run-dir ../../../../outputs/afa-stage5a-trial-v1

# 초기 모델 대비 업데이트·로그·optimizer·재로드 진단을 재현. 보고서는 새 이름 사용.
uv run --locked --group rl-train python -m beauty_agent.afa.training_audit --trained-dir ../../../../outputs/afa-stage5a-trial-v1 --initial-dir ../../../../outputs/afa-stage5a-setup-v1 --report ../../../../outputs/afa-stage5a-trial-v1/audit-recheck.json
```

최초 실행 결과는 루트 `outputs/afa-stage5a-trial-v1/`에 보존한다. `model.zip`, `checkpoint.json`, `config.json`, `report.json`, `logs/progress.csv`, `audit.json`이 핵심 산출물이다. 코드·입력·패키지·모델 해시를 기록하며 가중치는 커밋하지 않는다. 초기 준비 실행은 `outputs/afa-stage5a-setup-v1/`에 그대로 남긴다.

## 다음 단계의 목적과 남은 한계

**다음은 v2 의미 계약을 확정하는 단계**다. 현재 v1의 가장 강한 기준선에 개선 여지가 없다는 사실을 보존한다. 추가 학습량을 늘려 우위를 찾기보다 [v2 요구사항](../benchmark-v2-design/README.md)의 혼합 권고·다중 카드·필수 안전 정보·선택 정보·모름/거절·중단 계약을 먼저 구체화한다.

1개 seed·6개 train 세계·256 step으로 학습 안정성 전체나 일반화를 결론내릴 수 없다. 이번 완료 범위는 실제 학습 연결의 기술 검증이다. 제품 조회·NLP·후보 정정·앱 연동·독립 평가·전문가 검토는 완료하지 않았다. `development_preview`, `production_enabled=false`를 유지한다.

## 검증 기록 — 2026-11-16

실제 학습 명령과 별도 프로세스 재로드·감사 명령이 모두 성공했다. 감사 코드는 `beauty_agent/afa/training_audit.py`에 남겼다. PPO 준비 회귀 검사 13개를 다시 실행해 통과했고, 원본 source manifest 27/27 및 `git diff --check`를 확인했다. 기존 학습 코드·설정·KB·v1 분할은 수정하지 않았다.

이전 단계의 전체 369개 검사 및 원본 엄격 검사 5개 실패 기록은 당시 결과로 보존한다. 이번에는 전체 검사를 재실행했다고 표시하지 않는다. 이전 준비 실행의 해시를 확인하고 이번 실행·감사·문서의 해시는 `outputs/afa-stage5a-trial-v1/verification-index.json`에 별도로 기록한다.
