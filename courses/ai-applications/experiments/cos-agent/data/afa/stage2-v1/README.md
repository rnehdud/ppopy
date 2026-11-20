# AFA Stage 2 — 모델 없이 실행되는 정적 환경

해당 버전의 실험 기록이다. 현재 에이전트에서 AFA가 맡는 역할은 [목표 구조](../../../docs/agent-runtime-target.md)를 참고한다.

목적: **질문 하나 → 해당 답만 공개 → 다음 상태/행동 목록**을 만드는 실행 경계를 검증한다. 전체 순서는 Stage 0 명세 → Stage 1 응답/분할 → **Stage 2 환경** → Stage 3 전이/목적 검증 → 기준선/RL이다. 이번 단계는 학습 성과를 평가하지 않는다.

## 만든 것과 재사용한 것

| 구성 | 위치 / 역할 |
| --- | --- |
| 두 단계 adapter | `beauty_agent/afa/runtime.py`: 관찰 준비와 선택 제안 실행 분리 |
| Gymnasium 환경 | `beauty_agent/afa/environment.py`: reset/step/astep/action_masks, 58차원 상태 |
| 기존 코드 재사용 | SessionState·Context 조립·KB adapter·validate/decide/dispatch |
| 응답/참조 | Stage 1의 선택한 split 파일만 읽음. 숨겨진 응답은 환경 내부 보관 |
| 선택 의존성 | `rl` 그룹의 Gymnasium 1.2.3·NumPy. 기본 project.dependencies 유지 |

원본 AgentSession·HTTP API·실행 게이트·KB는 수정하지 않았다. 범용 Session 리팩터링이 아니라 Stage 0의 정적 known-answer 과제에 한정한 얇은 adapter다. 후보·정정·실제 근거 조회·자유 발화·실사용은 지원하지 않는다.

## 실제 한 턴

```text
reset(seed, world_index)
  선택한 split의 세계 하나 선택
  → prepare_context: 초기 공개 상태/게이트/마스크 준비
  → 관찰 반환 (dispatch 0회)

step(고정 행동 번호)
  현재 snapshot·마스크로 정확한 행동/대상 검증
  → 사본 작업 공간에서 apply_action: 선택 제안만 1회 dispatch
  → 질문이면 그 슬롯의 합성 답만 가져옴
  → prepare_context: 다음 입력을 임시 반영해 다음 관찰 준비
  → 점수·종료·58차원 인코딩까지 성공하면 환경 작업 공간 교체
```

prepare_context는 planner·dispatch·turn 증가를 수행하지 않는다. apply_action은 이미 선택한 제안을 1회 반환하는 adapter로 기존 decide_action/validator/dispatcher를 통과시킨다. 환경은 잘못된 action을 기준선의 정상 학습 transition으로 바꾸지 않고 hard error로 거부한다.

**반 턴의 의미:** adapter의 committed SessionState는 마지막 실행 턴까지다. 그 질문에 대한 합성 응답은 다음 PreparedTurn에 staged input으로 보관한다. 환경의 `visible_observations`와 반환 벡터는 이 staged 답을 포함하며 다음 행동이 같은 snapshot을 사용한다. 준비 단계에서 입력을 실행 턴으로 중복 커밋하거나 history/후보 ID를 두 번 증가시키지 않는다. 새 과제는 NLP/동적 후보를 사용하지 않는다.

환경 step 전체는 private fork에서 처리한다. 응답 생성·다음 Context·인코딩이 실패하면 원래 환경 상태/예산/유효 snapshot을 교체하지 않는다. 성공한 transition의 dispatch_count는 커밋된 실행 횟수다. 실패한 작업 공간에서 synthetic dispatch가 한 번 시도됐을 수 있으나 외부 저장·조회·네트워크 효과는 없다. 향후 실제 도구를 붙일 때 이 메모리 롤백을 외부 작업 취소 보장으로 해석하면 안 된다.

## 공개 정보와 상태

58차원 float32 벡터는 Stage 0 schema의 순서대로 다음을 포함한다.

1. 슬롯 5개의 상태 one-hot: 미질문·known·모름·거절·미해당·충돌 (30차원)
2. 슬롯별 값 one-hot: 미관찰 null 포함 (17차원)
3. 공개 task 카드 one-hot (2차원)
4. 현재 지원 행동 마스크 (8차원)
5. 잔여 질문 예산 scalar 0~4 (1차원)

현재 응답 격자는 known 값만 지원한다. 상태 구분을 인코딩했다고 모든 unknown/거절/정정 시나리오를 지원하는 것은 아니다. world ID·참조·미래 답·전체 응답표·리뷰 메타데이터는 관찰과 반환 info에서 제외한다. `_`로 시작하는 환경 내부 객체는 evaluator/debug용 구현 상태이며 정책 입력 API가 아니다.

`action_masks()`는 현재 Context의 enabled 쌍과 Stage 0 지원 사전/잔여 예산의 교집합이다. raw KB에 일시적인 제품 조회 요청이 있어도 해결된 것으로 바꾸지 않는다. 동일 카드에서 아직 답을 공개하지 않은 서로 다른 세계는 같은 공개 상태/마스크를 낸다.

## 종료·점수·오류

- 질문은 비용 1, 답변 뒤에는 자동 초안을 실행하지 않는다. 별도 유효 초안/보류 action을 선택한다.
- 게이트를 통과한 올바른 초안 또는 정당한 보류는 종료 손실 0. 성급한 보류는 5.
- 마지막 질문이 예산을 소진했더라도 이미 가능한 무료 완료 action을 막지 않는다.
- 과제 예산이 소진되고 지원 질문이 남으면 과제 종료 손실 5를 적용한다. 현재 격자는 최대 네 질문으로 지원 경로를 덮으므로 이 분기는 정상 자료에서 통상 발생하지 않는다. 일반 예산 환경 검증은 Stage 3에서 확장한다.
- 기본 env는 외부 시간 상한을 만들지 않아 truncated=False다. 필요하면 Gymnasium TimeLimit wrapper를 사용한다. 미완료 외부 중단의 마지막 관찰과 task termination을 구분한다.
- 종료 후 추가 step, 범위 밖/마스킹된 action, stale/소비된/변조된 snapshot, 동시 apply/step은 오류다. 새로운 정상 transition으로 기록하지 않는다.
- JSON 제안·허용 근거·초안 조건 검증은 기존 코드를 재사용한다. 자유 문구 검토와 원안/실제 적용 구분도 유지한다.

Gym/SB3의 일반 check_env는 마스크를 무시해 임의 action을 전달할 수 있다. 이 과제는 masked action에서 명시적 오류를 내므로 일반 check_env 전체 통과를 주장하지 않는다. 유효 마스크 경로의 공간·반환형·seed·종료·롤백을 별도 검사했다. 이후 SB3 연결 시 같은 strict action 계약을 유지한다.

## 실행

`cos-agent/`에서:

```powershell
uv sync --group rl
uv run --group rl python -m beauty_agent.afa.environment --report ../../../../outputs/afa-stage2/smoke.json
uv run --group rl pytest -q tests rl_tests
```

기본 `uv run pytest`는 기존 tests/만 수집한다. Gym 전용 검사는 `rl_tests/`에 분리해 rl 그룹을 설치하지 않은 기본 환경에 새 의존성을 강요하지 않는다. 원본 엄격 테스트의 실패를 숨기는 skip/xfail이나 기대값 변경은 하지 않았다.

```python
from beauty_agent.afa.environment import StaticAFAEnv

env = StaticAFAEnv(split="train")
obs, info = env.reset(seed=0)
mask = env.action_masks()
action = next(i for i, enabled in enumerate(mask) if enabled)
obs, reward, terminated, truncated, info = env.step(action)
```

이미 asyncio loop 안에서 호출할 때는 `await env.astep(action)`을 사용한다. 동기 step은 기존 loop를 중첩 실행하지 않고 명시적 오류를 낸다. 테스트/환경 무작위 액션 재현이 필요하면 별도로 action_space.seed도 설정한다.

## 검증 범위와 다음 단계

검사는 초기 숨은 실행 0회·선택 답만 공개·한 action당 한 dispatch·변조/재사용/동시 실행 거부·실패 시 롤백·같은 공개 정보의 관찰 일치·지원 세계의 유효 종료·외부 TimeLimit 반환을 다룬다. 내부 val/test 경로 실행은 엔지니어링 API 점검이며 미열람 holdout 성능을 주장하지 않는다. Stage 1의 독립성 한계는 그대로다.

환경 설치는 Python 3.10.5, Gymnasium 1.2.3, NumPy 2.2.6에서 확인했다. Gymnasium 1.4.0은 이 Python 환경에서 import 단계의 typing 오류가 발생해 검증된 버전을 고정했다. 다른 플랫폼/인터프리터의 실행 성공은 아직 확인하지 않았다. torch/SB3·학습 가중치는 설치/실행하지 않았다.

**다음 Stage 3의 목적**은 환경 API가 돈다는 것에서 더 나아가, 모든 지원 질문 순서의 비용·판정·종료와 보상 편법을 전수/수작업 기준으로 대조하는 것이다. 이번 scripted smoke의 return은 모델 성능이 아니다. 모든 실행은 synthetic `development_preview`, `production_enabled=false`다.

공식 계약 참고: [Gymnasium Env](https://gymnasium.farama.org/api/env/), [Time limits](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/).

## 실행 확인 — 2026-11-16

`uv run --group rl pytest -q tests rl_tests`: 336개 통과(새 adapter/env 검사 22개), 기존 Starlette/httpx 경고 1건. train split의 scripted smoke는 58차원, dispatch 3회, return -2로 질문 2개 후 정당한 보류를 확인했다. 이는 학습 정책 점수가 아니다. Stage 1 번들·v67 무결성 재현도 통과했다.

원본 source manifest 27/27, KB 구조 95/95, 경계·현재 명세 371개 통과. coverage·합성 KB CLI 실행. 엄격 원본은 62 통과/기존 5 실패, 동결 감사는 52/57과 종료 코드 1을 유지한다. 보고서는 루트 outputs/afa-stage2/에 있다. 원본 스냅샷·기존 런타임·데이터 분할을 수정하지 않았다.
