# AFA 코드 지도

이 폴더는 AFA 질문 실험 코드다. [목표 구조](../../docs/agent-runtime-target.md)에서 전체 런타임과 질문 정책의 책임을 구분한다.

먼저 [AFA 시작 안내](../../docs/afa-policy-guide.md)를 본다. 코드는 역할별 모듈로 유지하고, 이 목차로 현재 v2와 이전 v1을 구분한다. 모듈 경로를 바꾸면 CLI·import·실험 해시에 영향을 주므로 이번 구조 정리에서는 이동하지 않았다.

## 현재 v2 — 두 카드 공동 질문 환경

실험 기록·그래프는 [MLflow 안내](../../docs/afa-mlflow.md)를 본다. [tracking.py](tracking.py)는 과거 결과 가져오기와 향후 기록 인터페이스를 제공하며, 학습·환경을 실행하지 않는다.

| 역할 | 모듈 |
| --- | --- |
| 질문·답 공개·64차원 관찰·비용·종료 | [joint_environment.py](joint_environment.py) |
| 행동 준비·검사·단일 실행 | [joint_runtime.py](joint_runtime.py) |
| 질문 순서에 따른 판단 의미 변화 검사 | [semantics.py](semantics.py) |
| 합성 상황 설계·자료 검증 | [scenario_plan.py](scenario_plan.py), [joint_data.py](joint_data.py) |
| 전이·보상·마스크 검증 | [joint_validation.py](joint_validation.py) |
| 질문 방식 비교 | [joint_baselines.py](joint_baselines.py) |
| 누락 유형 보완·가족별 순환 계획·실행 | [coverage_repair.py](coverage_repair.py), [coverage_folds.py](coverage_folds.py), [fold_baselines.py](fold_baselines.py) |

v2 PPO 학습은 아직 연결하지 않았다. 현재 비교 기준선과 학습 정책을 혼동하지 않는다.

## 전체 v67 데이터 탐색 — E20

[v67_fixtures.py](v67_fixtures.py)는 E22의 작은 train 파생 응답표·공개 이력별 응답 연결을 생성·검증한다. [자료 안내](../../data/afa/v67-fixtures-v1/README.md)에서 출처·정적 가정·미지원 기능을 먼저 확인한다. 기존 v2 Gym 환경의 자료 로더를 교체하지 않는다.

후속 [v67_responses.py](v67_responses.py)는 train에서 선택한 행동과 바로 다음 이벤트를 대조하고, 다른 행동의 응답을 잘못 재사용하지 않도록 사전 검사한다. [라벨 검토·응답 계약 설명](../../docs/afa-v67-response-contract.md)을 함께 본다. 실제 Gym 전이 어댑터는 아니다.

[EDA 설명서](../../docs/afa-v67-eda.md)를 먼저 본다. [eda.py](eda.py)는 원본을 바꾸지 않고 전체 집계·분할·후보 응답 경로·중복과 검토 표본을 추출한다. [eda_views.py](eda_views.py)는 선택 시각화 패키지로 그래프를 만들고 명시적 `--publish`로 MLflow에 기록한다. 정책 학습기나 완성 RL 응답 시뮬레이터가 아니다.

## 이전 v1 — 단일 카드·PPO 연결 진단

| 역할 | 모듈 |
| --- | --- |
| 범위·자료 검사 | [stage0.py](stage0.py), [stage1.py](stage1.py) |
| 기반 실행 어댑터·58차원 환경 | [runtime.py](runtime.py), [environment.py](environment.py) |
| 전이 검증·기준선·개선 여지 | [validation.py](validation.py), [baselines.py](baselines.py), [readiness.py](readiness.py) |
| PPO 초기화·학습·평가·학습 증거 검사 | [ppo.py](ppo.py), [training_audit.py](training_audit.py) |

v2도 일부 v1 기반 계약·유틸리티를 재사용한다. “이전” 표시는 삭제해도 된다는 뜻이 아니다. 학습된 가중치는 소스에 포함하지 않으며 모든 실험은 `development_preview`, `production_enabled=false`다.
