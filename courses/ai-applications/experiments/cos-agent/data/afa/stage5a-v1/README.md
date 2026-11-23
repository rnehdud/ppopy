# Stage 5A-1 — Maskable PPO 연결 준비

해당 버전의 실험 기록이다. 현재 에이전트에서 AFA가 맡는 역할은 [목표 구조](../../../docs/agent-runtime-target.md)를 참고한다.

목적: **기존 정형 환경에 학습기를 연결하고, 다음 단계에서 시험 학습을 실행할 수 있게 한다.** 이번 단계는 의존성 설치·실행 코드·학습 전 초기화 검사다. 시험 학습(Stage 5A-2)이나 성능 개선 실험을 완료한 것이 아니다.

## 전체 진행에서의 위치

Stage 0~4의 범위·응답 자료·환경·전수 검사·기준선 → **현재: PPO 연결 준비** → 짧은 시험 학습 → v2 의미 계약·자료·환경·평가 계획 → 비교 학습 → 독립 평가 → 실제 에이전트 연결.

현재 v1에서는 train 최적 기대 질문 수 2.5, val 2.0에 기존 기준선이 이미 도달했다. 여기서는 학습 연결의 정상 동작을 검사하며 비용 우위·사용자 효용·독립 일반화를 주장하지 않는다. [학습 전 보완](../review-v1/README.md), [v2 요구사항](../benchmark-v2-design/README.md)을 별도로 유지한다.

## 설치와 실행의 분리

기본 `project.dependencies`와 가벼운 `rl` 그룹은 유지한다. 새 선택 그룹 `rl-train`이 `rl`을 포함하며 Torch/SB3/sb3-contrib를 추가한다. 기본 앱 실행이나 Stage 0~4 검사에는 이 그룹이 필요 없다.

| 구성 | 고정 버전/조건 | 이유 |
| --- | --- | --- |
| Python | 그룹 지원 범위 >=3.10,<3.14; 이 PC 3.10.5 | 기본 프로젝트 Python 요구 범위와 학습 그룹 범위를 분리 |
| Gymnasium | 1.2.3 | 기존 환경에서 검증한 버전, SB3 2.7.1의 >=0.29.1,<1.3 범위 |
| Torch | 2.9.1; Windows/Linux CPU index | 소형 정책 연결 점검에 CPU 사용, CUDA 설치 불필요 |
| stable-baselines3 / sb3-contrib | 각각 2.7.1 | 같은 릴리스로 고정하고 실제 import·직렬화 검사 |
| 정책 | MaskablePPO / MlpPolicy; actor·critic 각각 [32,32] | 58차원 공개 관찰과 고정 8개 행동 |

macOS에서는 PyPI Torch를 선택하지만 이 작업에서 검증하지 않았다. `uv.lock`은 간접 의존성까지 기록한다. 새 그룹은 Python 3.14 이상을 지원한다고 주장하지 않는다. 기존 가상환경에서 `uv sync`로 그룹을 바꾸면 선택하지 않은 학습 패키지가 제거될 수 있으므로 실행 시 그룹을 명시한다.

`cos-agent/`에서:

```powershell
uv sync --locked --group rl-train
uv run --locked --group rl-train python -m beauty_agent.afa.ppo prepare --run-dir ../../../../outputs/afa-stage5a-setup-v1
```

`prepare`는 초기 모델 생성·저장·재로드·마스크 기반 예측·train 6세계 실행·공식 mask-aware evaluator 호출만 수행한다. **`learn()` 호출과 optimizer 갱신은 0회**다. 여기서 저장한 `initialized_model.zip`은 학습된 모델이 아니다. 모델 생성 자체는 가중치 초기화를 위한 Torch 연산을 수행한다.

## 세 실행 명령과 요구사항

| 명령 | 입력 | 수행하는 일 | 완료 확인 |
| --- | --- | --- | --- |
| `prepare` | config.json, 새 run-dir | 초기 모델 저장·재로드, 결정적 공개 입력 실행 비교, 공식 masked 평가 경로 검사 | num_timesteps=0, learning_executed=false, 저장/재로드 동등 |
| `train` | config.json, 새 run-dir | train만 수집·학습, 수집 행동의 마스크 감사, CSV 로그·모델 저장·재로드·train 진단 | 지정 step과 감사 수 일치, 유한 가중치, 마스크·전이·단일 dispatch 검사 통과 |
| `evaluate` | 기존 run-dir의 config·체크포인트·manifest | 해시·버전 확인 후 동일 train cohort에 결정적 mask-aware 평가 | 새 학습 없이 저장 모델을 재실행. 초기 모델이면 초기 모델로 표시 |

모든 출력은 루트 `outputs/` 안에만 저장한다. `prepare`/`train`은 기존 폴더를 덮어쓰지 않는다. 새 실행에는 다른 폴더명을 사용한다. `evaluate`는 읽기 전용이며 stdout으로 결과를 반환한다. 이 단계의 평가는 **train 전용**으로 val 기반 선택과 test 성능 측정을 거부한다.

저장 모델은 Python 객체를 포함하므로 이 코드가 생성한 로컬 산출물을 사용한다. 로드 전에 체크포인트 바이트·설정·입력/코드 해시·패키지 버전을 검사한다. 코드를 수정했다면 기존 결과를 보존하고 새 실행을 만든다. 해시는 결과 재현과 변경 탐지 목적이며 외부 파일의 신뢰성을 승인하는 서명이 아니다.

## 다음 단계에서 사용할 학습 명령 — 이번에는 실행하지 않음

```powershell
uv run --locked --group rl-train python -m beauty_agent.afa.ppo train --run-dir ../../../../outputs/afa-stage5a-trial-v1
uv run --locked --group rl-train python -m beauty_agent.afa.ppo evaluate --run-dir ../../../../outputs/afa-stage5a-trial-v1
```

`config.json`의 256 step·seed 0·32 step rollout·batch 16·epoch 4는 **연결 시험용 설계 설정**이다. 최적 하이퍼파라미터나 충분한 학습량으로 검증한 값이 아니다. gamma=1, shaping=0, 비용·보상·행동 사전·데이터 분할은 v1을 유지한다. 업데이트할 경우 설정 파일과 새 실행 기록으로 남긴다. SB3의 rollout 단위 초과 수집을 피하도록 총 step은 n_steps의 배수이며 batch는 rollout을 나누도록 검증한다.

## 마스크·종료·정보 경계

- 수집은 `MaskablePPO.learn(use_masking=True)`를 사용하고 callback이 실제 collector의 mask/action을 검사한다. 환경의 invalid action hard error도 유지한다.
- 직접 평가는 매 step `predict(..., action_masks=mask)`를 호출한다. 라이브러리 평가 helper는 `sb3_contrib.common.maskable.evaluation.evaluate_policy`만 사용한다.
- 일반 SB3 `evaluate_policy`나 마스크를 무시하는 무작위 `check_env`를 대신 사용하지 않는다. 향후 학습 중 평가 callback이 필요하면 `MaskableEvalCallback`을 사용한다. 현재는 학습 중 val 평가·모델 선택 callback이 없다.
- 원본 환경의 terminated/truncated 계약을 그대로 사용한다. 정적 과제에 외부 TimeLimit이나 보상 정규화를 추가하지 않는다. 마지막 무료 종료·예산 실패·안전 게이트는 기존 전수 검증 대상이다.
- 정책은 공개 관찰과 마스크만 받는다. 전체 응답표·세계 ID·참조는 evaluator 영역에 남는다. 학습 로그의 기술 지표와 도메인 정답·임상 판단을 구분한다.

## 산출물과 검사

실행 폴더에는 `config.json`, `checkpoint.json`, 초기/학습 모델 zip, `report.json`을 기록한다. 학습 실행만 `logs/progress.csv`를 추가한다. manifest는 패키지·Python 버전, 주요 코드·계약·train 자료 해시, 모델 해시·학습 step 수를 포함한다. 보고서는 마스크 적용·저장/재로드 동등성·실행 범위와 학습 여부를 명시한다.

선택 검사 위치를 `ppo_tests/`로 분리해 기본 검사에서 Torch import를 요구하지 않는다.

```powershell
uv run --locked --group rl-train pytest -q tests rl_tests ppo_tests
```

신규 검사는 prepare에서 learn 호출 금지, 비활성 행동 확률 0, 저장/재로드, 변조·코드 변경 거부, 설정 계약, train 전용 평가, collector mask 오류, 기존 폴더 덮어쓰기 방지를 다룬다. 실제 optimizer 갱신·학습 안정성·collector 통합 학습 검사는 다음 시험 학습에서 확인한다.

## 근거

- [SB3-contrib 2.7.1 Maskable PPO](https://sb3-contrib.readthedocs.io/en/v2.7.1/modules/ppo_mask.html): mask-aware 평가와 predict, 환경 action_masks 계약
- [uv의 PyTorch index 구성](https://docs.astral.sh/uv/guides/integration/pytorch/): explicit CPU index와 플랫폼별 source 설정
- [SB3 2.7.1 의존성](https://pypi.org/project/stable-baselines3/2.7.1/), [Torch 2.9.1](https://pypi.org/project/torch/2.9.1/): 호환 범위와 Windows Python 3.10 배포물 확인

`development_preview`, `production_enabled=false`를 유지한다. 실제 앱·사용자 수집·전문가 승인·제품 추천 정책을 활성화하지 않는다.

## 실행 확인 — 2026-11-16

Windows / Python 3.10.5 / torch 2.9.1+cpu / SB3·sb3-contrib 2.7.1 / Gymnasium 1.2.3 / NumPy 2.2.6에서 설치·초기화·저장·재로드·평가 명령을 실행했다. `uv pip check`, `uv lock --check` 통과. 기본 프로젝트 의존성 목록은 변경하지 않았다.

- 신규 PPO 준비 검사 13개, 전체 실험·RL·PPO 검사 **369개 통과**. 기존 Starlette/httpx 경고 1건.
- 준비 실행 `num_timesteps=0`, `learning_executed=false`, collector 학습 감사 횟수 0. `learn()` 미호출과 저장/재로드 실행 동등성을 확인했다.
- train 고유 6세계의 결정적 실행에서 마스크·전이·step당 dispatch·유한 수치·종료 검사 통과. 별도 공식 평가 helper 2 episode는 API 경로 점검이며 새 독립 사례 2개가 아니다.
- 초기 정책은 평균 return -5.333, 종료 계약 충족 1/6, 초안 0건이었다. 무학습 초기 정책의 진단이며 성능 통과 기준이나 학습 개선 결과가 아니다.
- 원본 manifest 27/27, KB 구조 95/95, 현재 명세 검사 371개 통과. 엄격 원본은 62 통과/기존 5 실패, 감사 52/57 및 종료 코드 1 유지. coverage 60카드/213분기/180경계 및 합성 CLI inactive 확인.

실행 산출물은 루트 `outputs/afa-stage5a-setup-v1/`에 있으며 커밋 대상이 아니다. 학습 명령의 실제 rollout·optimizer 갱신·로그 안정성 검증은 **다음 Stage 5A-2**에 남아 있다.
