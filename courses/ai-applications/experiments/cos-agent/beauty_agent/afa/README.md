# AFA 코드 지도

이 폴더는 AFA 질문 실험 코드다. [목표 구조](../../docs/agent-runtime-target.md)에서 전체 런타임과 질문 정책의 책임을 구분한다.

먼저 [AFA 시작 안내](../../docs/afa-policy-guide.md)를 본다. 코드는 역할별 모듈로 유지하고, 이 목차로 현재 v2와 이전 v1을 구분한다. 모듈 경로를 바꾸면 CLI·import·실험 해시에 영향을 주므로 이번 구조 정리에서는 이동하지 않았다.

## 런타임용 Myopic VOI

```python
from beauty_agent.afa.question_priority import MyopicVOIAFAPolicy
from beauty_agent.runtime import AgentRuntime

runtime = AgentRuntime(afa_policy=MyopicVOIAFAPolicy())
```

런타임에서 선택된 전체 카드 집합과 현재 관찰을 고정하고, 각 질문에 KB 분기 값 하나씩 가상 대입한다. `decision_change_rate`는 현재 결과와 달라진 답의 비율이고, `expected_pruned`는 그 답으로 사라지는 다른 열린 질문 수의 평균이다. `distinct_outcomes`는 가상 답들이 만든 고유한 결과 수다. 답의 가중치는 균등하다. 질문별 `question_costs`와 `safety_weights`는 기본값 1이며, 각 점수의 우선순위에 안전 가중치 / 비용 비율을 곱한다. 종료는 유효한 후보가 없을 때 런타임의 현재 근거 및 보류 상태에 따른다.

`score_candidates(...)`의 `AFACandidateScore` 모델과 `runtime.get_session(request_id).afa_question_scores`에서 질문의 선택·제외 사유를 조회할 수 있다. 정책을 단독 호출할 때는 `card_ids`를 생성자에 지정하면 질문을 만들지 않는 카드의 판정도 비교에 포함된다.

1단계 AFA는 한 답으로 판정이 바뀌는 후보만 선택한다. AFA가 `stop(insufficient)`를 반환하면 Control Plane이 현재 답과 양립하는 KB 분기를 최대 두 답까지 별도로 확인한다. 가상 답 순서가 실제 질문 후보를 따라갈 수 있고 최종 판정이 바뀌면 첫 질문만 제시한다. 실제 답을 받아 다시 평가한다. 세션의 `afa_hold_review_slot`은 이 단계에서 제시한 질문을 나타내며 같은 턴의 1단계 점수는 `zero_impact`를 유지한다. `stop_lookahead=1`로 Control Plane의 보류 전 확인을 끌 수 있고, `stop_lookahead=3`으로 세 답까지 시험할 수 있다. 비교 명령에 `--dependency-lookahead 2 --dependency-lookahead 3`을 붙이면 두 변형을 같은 사례에 추가한다.

```powershell
uv run --locked pytest -q -s tests/afa/core/test_myopic_voi.py -k synthetic_comparison
uv run --locked python -m beauty_agent.afa.myopic_evaluation --output ../../../../outputs/myopic-comparison.json
```

확장 비교는 KB 분기에서 만든 조건, 여러 카드가 함께 활성화되는 합성 조건, v67 E22의 train 파생 4건을 사용한다. 같은 환경에서 고정 순서와 Myopic VOI의 질문 수 및 최종 판정 일치율을 비교한다. 보고서에는 전체 합성 응답을 처음부터 공개했을 때의 KB 판정도 담긴다.

기존 PPO까지 비교하려면 `uv run --locked --group rl-train python -m beauty_agent.afa.myopic_evaluation --ppo-model <checkpoint.zip> --output ../../../../outputs/myopic-ppo-comparison.json`을 실행한다. 기존 B-C02 라우터가 허용하는 턴에만 신뢰할 수 있는 로컬 체크포인트를 사용한다. 보고서는 모델이 선택한 질문, 지원 범위 밖 규칙 선택, 모델 시도 후 규칙 복구를 구분한다.

E51의 4정책 비교는 기존 78조건과 추가 합성 98조건을 따로 집계한다. 실험 폴더에서 다음 명령을 실행한다.

```powershell
uv run --locked python -m beauty_agent.afa.paired_evaluation --freeze --fixtures ../../../../outputs/paired-fixtures.json
uv run --locked --group rl-train python -m beauty_agent.afa.paired_evaluation --fixtures ../../../../outputs/paired-fixtures.json --ppo-model <checkpoint.zip> --output ../../../../outputs/paired-report.json
```

보고서는 전체 합성 답을 처음부터 알려 준 기준과의 사용자 응답·내부 KB 판정 일치, 질문 수, 필수 보류, 로컬 턴 처리 시간과 PPO 사용 범위를 기록한다.

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
