# AFA 자료·단계별 문서 목차

[목표 구조](../../docs/agent-runtime-target.md)의 첫 버전은 Python 런타임과 질문 선택 AFA를 분리한다. 아래 자료는 제한된 합성 실험별 증빙이다.

[시작 안내](../../docs/afa-policy-guide.md) · [누적 진행·결과](../../docs/afa-policy-progress.md) · [실행 코드 지도](../../beauty_agent/afa/README.md)

각 하위 폴더는 특정 버전의 계약·합성 입력·실험 설계를 보관한다. 폴더 수는 작업 이력에 해당하며 전부 실행할 필요는 없다. 현재 자료와 이전 진단 자료를 구분해서 읽는다. 경로·원본 내용은 보존했다.

## 현재 v2: 먼저 볼 문서

첫 B-C02 PPO 실험의 64개 합성 상황, 가족 분할, 기준선과 실행 명령은 [PPO 학습 전 검증](ppo-preflight-v1/README.md)에 있다. 이 비교 환경의 입력은 15차원이다.

E22의 작은 train 파생 응답 자료·검증은 [v67-fixtures-v1](v67-fixtures-v1/README.md)에 있다. 기존 v2 48개 자료와 별개이며 실제 Gym 환경에 아직 연결하지 않았다.

전체 v67 EDA 후속 자료는 [v67-review-v1](v67-review-v1/README.md)에 있다. 라벨 검토 결정·수정 제안·응답 연결 계약이며, 기존 v2 48개 환경을 교체하거나 전체 v67 학습을 시작한 자료가 아니다.

| 순서 | 폴더 | 내용 |
| --- | --- | --- |
| 1 | [semantic-v2-v1](semantic-v2-v1/README.md) | 분기 의미·미상·거절·정정·종료 계약 |
| 2 | [scenario-plan-v2-v1](scenario-plan-v2-v1/README.md) | 48개 공동 상황, 질문·비용·분할 설계 |
| 3 | [joint-v2-v1](joint-v2-v1/README.md) | 실제 질문 환경·공개 관찰·종료 구현 |
| 4 | [joint-baselines-v1](joint-baselines-v1/README.md) | 고정 분할에서 기존 방식 비교, 누락 발견 |
| 5 | [coverage-repair-v1](coverage-repair-v1/README.md) | 손세안 포함 배치·순환 평가 계획 |
| 6 | [fold-baselines-v1](fold-baselines-v1/README.md) | 16가족 순환 비교 결과와 부분군 반례 |

E26에서는 별도로 구성한 B-C02 범위의 PPO 학습 전 검사를 완료했다. 서비스 설계에서 다음으로 할 일은 런타임의 행동과 상태 전이를 정의하는 것이다. 이름 끝의 `v1`은 그 자료 묶음의 첫 버전을 가리킨다. v2 공동 상황의 기존 방식 비교는 기준선 결과다.

## 초기 v1과 설계 이력

| 단계 | 폴더 | 내용 |
| --- | --- | --- |
| Stage 0 | [stage0-v1](stage0-v1/README.md) | 첫 범위·행동·종료·비용 |
| Stage 1 | [stage1-v1](stage1-v1/README.md) | v67 감사·별도 응답표·분할 |
| Stage 2 | [stage2-v1](stage2-v1/README.md) | 58차원 질문 환경 |
| Stage 3 | [stage3-v1](stage3-v1/README.md) | 전수 전이·보상·마스크 검사 |
| Stage 4 | [stage4-v1](stage4-v1/README.md) | 기존 질문 방식 비교 |
| 보완 | [review-v1](review-v1/README.md) | 개선 여지·실행 비용 분석 |
| Stage 5A-1 | [stage5a-v1](stage5a-v1/README.md) | PPO 연결 준비·설정 |
| Stage 5A-2 | [stage5a-trial-v1](stage5a-trial-v1/README.md) | 256 step 시험 학습·재로드 결과 |
| v2 초기 제안 | [benchmark-v2-design](benchmark-v2-design/README.md) | 확장 요구사항·미결정 이력 |

**옛 명령 주의:** 2026-11-17 E16에서 테스트만 재배치했다. 당시 README·실행 기록 속 `rl_tests/`, `ppo_tests/`는 각각 현재 `tests/afa/gym/`, `tests/afa/ppo/`에 해당한다. 최신 실행 명령은 [테스트 안내](../../tests/afa/README.md)를 사용한다. 옛 보고서·해시는 과거 증빙으로 유지한다.
