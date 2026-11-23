# AFA 테스트

검사 대상은 AFA의 개발 환경과 연결 계약이다. [전체 에이전트 및 AFA 범위](../../docs/agent-runtime-target.md)를 참고한다.

테스트는 의존성과 검사 역할에 따라 묶었다. 모든 명령은 실험 폴더 `courses/ai-applications/experiments/cos-agent/`에서 실행한다.

| 폴더 | 검사 대상 | 추가 의존성 그룹 |
| --- | --- | --- |
| `core/` | 자료·계약·의미·런타임 | 기본 개발 환경 |
| `gym/` | 질문 환경·마스크·보상·기준선 | `rl` |
| `ppo/` | 실제 PPO 라이브러리 연결·저장·재로드 | `rl-train` |
| `tracking/` | MLflow 저장·재등록·누락값·실패 기록 | `tracking` |

```powershell
# 기존 일반 기능 검사와 core/를 함께 실행
uv run --locked pytest -q

# AFA core/만 실행
uv run --locked pytest -q tests/afa/core

# 일반 기능 + AFA core/ + gym/
uv run --locked --group rl pytest -q -o "norecursedirs=ppo tracking" tests

# 전체 실험 검사: 일반 기능 + core/ + gym/ + ppo/ + tracking/
uv run --locked --group rl-train --group tracking pytest -q -o norecursedirs= tests
```

`pyproject.toml`의 `norecursedirs`는 기본 수집에서 `gym/`, `ppo/`, `tracking/`를 제외한다. `-o "norecursedirs=ppo tracking"`는 PPO·MLflow를 제외하고, `-o norecursedirs=`는 제외 목록을 비워 모든 선택 검사까지 수집한다. 부모 `tests` 경로를 함께 넘기면 하위 경로만 명시해도 제외 설정이 유지될 수 있으므로 위 명령을 사용한다. 이 구분은 선택 패키지가 없는 환경의 기본 검사를 유지하기 위한 것이다. skip/xfail을 추가하거나 테스트 기대값을 바꾸지 않았다. 저장소 루트의 원본 KB 엄격 검사와 알려진 5개 실패는 별도 범위다.

2026-11-17 E16: 기존 `tests/test_afa_*.py` 9개, `rl_tests/*.py` 9개, `ppo_tests/*.py` 1개를 각각 이 폴더 아래로 이동했다. 테스트 내용은 바꾸지 않았다. 과거 명령·원본 보고서는 당시 경로로 보존하며, 새 명령은 이 안내를 따른다.
