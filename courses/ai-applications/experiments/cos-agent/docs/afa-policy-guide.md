# AFA Policy — 어디서부터 볼까?

**역할부터 알고 싶다면 [Ppopy 목표 구조](agent-runtime-target.md)를 먼저 읽는다.** AFA는 런타임이 호출하는 질문 선택 모듈이다.

**처음에는 [누적 진행 문서](afa-policy-progress.md)를 읽는다.** 전체 목적·진행 상황·실험 결과·한계가 들어 있다. 이 문서는 코드를 찾거나 검사를 실행할 때 사용하는 길잡이다.

## 목적별로 볼 파일

| 알고 싶은 것 | 파일 | 읽을 부분 |
| --- | --- | --- |
| 합성 데이터와 PPO가 어떻게 연결되나? | [AFA Policy RL 한 페이지 설명](afa-ppo-data-flow.md) | 질문 한 번의 흐름, 자료별 용도, 코드와 외부 기술 |
| 첫 B-C02 PPO를 어떻게 재현하나? | [학습 전 검증 안내](../data/afa/ppo-preflight-v1/README.md) | 가족 분할, 보상, 기준선과 실행 명령 |
| 무엇을 만들고 어디까지 했나? | [afa-policy-progress.md](afa-policy-progress.md) | 1절 전체 흐름 → 3절 결과 → 8절 다음 단계 |
| 전체 합성 데이터 EDA를 배우고 싶다 | [v67 EDA 보고서](afa-v67-eda.md) | 분석 절차 → 분포 → 응답 경로 → 내용 검토 → 다음 결정 |
| 작은 train 파생 응답 자료를 보고 싶다 | [E22 자료 안내](../data/afa/v67-fixtures-v1/README.md) | 원본/가상 응답 구분·전체 순서 검사·별도 라벨 파생 |
| EDA 발견 사항을 어떻게 처리했나? | [라벨·응답 연결 후속 검토](afa-v67-response-contract.md) | 5항목 검토 → train 다음 이벤트 집계 → 응답 재사용 사전 검증 |
| 그래프로 결과를 비교하고 싶다 | [MLflow 대시보드 안내](afa-mlflow.md) | 로컬 주소·실험별 화면·지표 뜻·시작/종료 |
| 호출·설정·결과 숫자는 무슨 뜻인가? | [afa-policy-progress.md](afa-policy-progress.md#technical-guide) | 9절 개발자 해설 |
| 현재 질문 한 번이 어떻게 진행되나? | [joint_environment.py](../beauty_agent/afa/joint_environment.py) | `reset`, `action_masks`, `step`/`astep` |
| 선택한 행동을 어떻게 검사·실행하나? | [joint_runtime.py](../beauty_agent/afa/joint_runtime.py) | v2 실행 어댑터. 기반 계약은 [runtime.py](../beauty_agent/afa/runtime.py) |
| 질문을 더 해야 할지 어떻게 판단하나? | [semantics.py](../beauty_agent/afa/semantics.py) | 공개된 답과 가능한 나머지 답 사이의 판단 의미 검사 |
| 어떤 질문 방식과 비교했나? | [joint_baselines.py](../beauty_agent/afa/joint_baselines.py), [fold_baselines.py](../beauty_agent/afa/fold_baselines.py) | 기존 순서·무작위·계산 기준선, 가족별 순환 비교 |
| 최신 PPO 연결은 어디서 확인하나? | [ppo_preflight.py](../beauty_agent/afa/ppo_preflight.py) | E26의 B-C02 환경·관찰·행동 마스크·학습 초기화 |
| 과거 PPO 시험은 어디서 확인하나? | [ppo.py](../beauty_agent/afa/ppo.py), [E07 설정](../data/afa/stage5a-v1/config.json) | v1의 `prepare`/`train`/`evaluate` 및 256스텝 시험 |
| 자료·단계별 상세 설계는? | [data/afa/README.md](../data/afa/README.md) | 현재 v2와 이전 v1을 구분한 목차 |
| 원본 결과를 확인하고 싶다 | [afa-policy-evidence.json](afa-policy-evidence.json) | E번호별 원본 보고서 경로·수치·해시. 원본 `outputs/`는 로컬 보관 |

**AFA Policy라는 단일 완성 파일은 없다.** 환경, 선택 방법, 실행 검사, 학습 및 평가 코드가 역할별로 나뉜다. 지금 실제로 비교한 v2 선택 방법은 기준선들이다. 학습된 v2 PPO 정책은 아직 없으며, v1 시험 모델은 소스 파일이 아니라 로컬 `outputs/afa-stage5a-trial-v1/model.zip`에 있다.

## 폴더는 이렇게 나눈다

```text
cos-agent/
├─ beauty_agent/afa/          실행·선택·학습·평가 코드
│  └─ README.md              모듈별 역할과 현재/이전 버전 안내
├─ data/afa/                 버전별 계약·합성 입력·실험 명세
│  └─ README.md              단계별 자료 목차
├─ docs/
│  ├─ afa-policy-guide.md    이 길잡이
│  ├─ afa-policy-progress.md 누적 설명·결과·다음 단계
│  └─ afa-policy-evidence.json 공유용 수치와 증빙 해시
└─ tests/afa/
   ├─ core/                  기본 의존성으로 확인하는 계약·자료·런타임
   ├─ gym/                   Gym/NumPy를 사용하는 환경·기준선 검사
   └─ ppo/                   Torch/MaskablePPO 연결·저장·재로드 검사
```

저장소 루트의 `outputs/`는 실행 보고서·로그·모델 보관 장소다. 공유 저장소에서 제외된다. `skin_engine/`와 `KB/`는 기존 규칙·지식 자료이며 AFA 폴더로 옮기지 않는다. `.venv/`, `__pycache__/`, `.pytest_cache/`는 도구가 관리하는 환경·캐시다.

## 검사는 어디서 실행하나?

아래 명령의 작업 위치는 이 실험 폴더, 즉 `courses/ai-applications/experiments/cos-agent/`다. 경로와 의존성별 전체 설명은 [테스트 안내](../tests/afa/README.md)를 본다.

```powershell
# 기본 기능 + AFA 계약·자료·런타임 검사
uv run --locked pytest -q

# Gym 환경·기준선까지
uv run --locked --group rl pytest -q -o "norecursedirs=ppo tracking" tests

# PPO 연결 검사까지 전체 실험 검사
uv run --locked --group rl-train --group tracking pytest -q -o norecursedirs= tests
```

기본 수집은 선택 의존성 디렉토리 `gym/`, `ppo/`, `tracking/`로 내려가지 않는다. `-o "norecursedirs=ppo tracking"`는 PPO·MLflow를 제외하고, `-o norecursedirs=`는 제외 목록을 비워 전체를 수집한다. PPO 검사는 연결·초기화 검사이며 새 학습을 자동 시작하는 명령이 아니다. 저장소 루트의 KB 원본 엄격 검사는 별개이며 기존 5개 불일치는 그대로 남는다.

## 이전 경로와의 대응 — 2026-11-17 E16

| 이전 위치 | 현재 위치 |
| --- | --- |
| `tests/test_afa_*.py` | `tests/afa/core/test_afa_*.py` |
| `rl_tests/` | `tests/afa/gym/` |
| `ppo_tests/` | `tests/afa/ppo/` |

테스트 19개 파일은 내용을 바꾸지 않고 이동했다. 이전 단계 README와 실행 보고서는 당시 기록이므로 옛 명령이 남아 있다. 예전 전체 검사 명령의 `pytest -q tests rl_tests ppo_tests`는 현재 모든 선택 그룹을 설치한 뒤 `pytest -q -o norecursedirs= tests`로 읽는다. Gym까지의 옛 명령 `pytest -q tests rl_tests`는 현재 `pytest -q -o "norecursedirs=ppo tracking" tests`다. 원본 증빙 파일·수치·해시를 새 경로에 맞춰 덮어쓰지 않는다. 실행 모듈·자료·원본 결과 경로는 유지했다.
