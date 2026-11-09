# BeautyLIFE 개인화 화장품 관리 에이전트

**현재 단계: 전체 가이드라인과 개발 틀 정리.** 기능을 한꺼번에 완성하지 않고, 작은 사용 흐름을 하나씩 검증하며 발전시킵니다. 먼저 [프로젝트 개발 가이드](docs/project-guide.md)를 읽으세요. 아래 실행 방법과 코드는 구조를 살펴보기 위한 실험용 골격이며 기술 선택을 확정하지 않습니다.

iOS 앱과 스마트미러가 같은 HTTP API를 호출하는 Python 초기 골격입니다. **현재는 합성 입력 전용·무저장 기술 데모**입니다. 실제 앱 탑재, 학습된 SLM, 실제 제품 추천이 완료된 상태는 아닙니다.

## 먼저 실행하기 — Windows PowerShell

```powershell
cd C:\cos-agent
uv sync --locked
uv run uvicorn beauty_agent.api:app --host 127.0.0.1 --port 8000 --no-access-log
```

서버를 켠 채 다른 터미널에서:

```powershell
cd C:\cos-agent
uv run python scripts/demo.py
uv run pytest -q
```

`http://127.0.0.1:8000/docs`에서 API를 직접 실행할 수 있습니다. `POST /v1/agent/turn`에 [예제 JSON](examples/turn.json)을 넣습니다. `profile.confirmed`를 `false`로 바꾸면 추가 질문, 모두 확인되면 아침/저녁 초안을 반환합니다. 종료는 서버 터미널에서 Ctrl+C입니다.

`uv`가 없는 환경에서는 Python 3.10 이상에서 `python -m venv .venv` 후 `.venv\Scripts\python -m pip install -e . pytest`를 사용할 수 있습니다. 이 환경에는 uv가 설치되어 있습니다.

## 여기서 에이전트란

SLM은 작은 언어 모델이고, 에이전트는 입력을 보고 필요한 질문·도구를 선택하여 작업을 진행하는 프로그램입니다. 모델 자체가 제품 DB나 사용자 계정이 되지는 않습니다. 이 골격은 `입력 검증 → 부족한 정보 찾기 → 질문 선택 → 사용법 기반 초안`을 코드로 연결합니다.

| 구성 | 현재 역할 |
|---|---|
| `contracts.py` | iOS·미러 공통 입출력 형식 |
| `agent.py` | 확인 상태 검사, 제외 제품 적용, 초안 생성 |
| `catalog.py` | 가상 제품 2개와 합성 표시 사용법 |
| `planner.py` | 기준선 질문 선택 또는 Ollama 질문 ID 선택 |
| `actions.py`, `action_planner.py`, `action_runtime.py` | 별도 루프의 액션 제안 계약, 실행 조건 검증·fallback·dispatcher |
| `loop.py` | Python/CLI 다중 턴 세션·정형 확인·트레이스 |
| `api.py` | HTTP 진입점·스키마 문서 |

현재 `concerns`는 수집 형식만 있고 효능·피부별 계산에 사용하지 않습니다. 자유 대화에서 프로필을 추출·저장하지도 않습니다. 초안 hash는 내용 식별자이며 승인 토큰이 아닙니다. `requires_approval`은 향후 승인 절차를 위한 표시이며 저장 API는 아직 없습니다.

## 로컬 SLM 연결 — 선택

이 절의 질문 ID 선택 설명은 기존 HTTP API에 해당합니다. 별도 Python/CLI 루프는 전체 액션 제안을 받는 Ollama 경로와 향후 Qwen SFT 주입 계약을 사용합니다. [액션 중심 루프 문서](docs/modular-agent-loop.md)에 실행 조건, 질문 문구 검증 한계 및 합성 SFT 예제를 정리했습니다.

Ollama를 별도로 설치하고 라이선스·메모리·한국어 품질을 확인한 모델을 로컬에 준비한 뒤 서버 시작 전에 설정합니다. 모델은 자동 다운로드하지 않습니다.

```powershell
$env:AGENT_PROVIDER="ollama"
$env:OLLAMA_MODEL="실제로 설치한 모델의 정확한 태그"
uv run uvicorn beauty_agent.api:app --host 127.0.0.1 --port 8000 --no-access-log
```

질문이 필요한 입력에서만 로컬 `127.0.0.1:11434/api/chat`을 1회 호출합니다. 모델은 허용된 질문 ID 하나만 선택하며, 나머지 누락 질문도 응답에 남습니다. 자유 문장·제품·근거·저장 명령은 모델 출력에서 실행하지 않습니다. 15초 HTTP 타임아웃, 출력 128토큰 설정, 64KiB 응답 상한을 사용합니다. 느리게 계속 오는 응답 전체의 절대 마감은 아직 구현하지 않았습니다. 모델 오류·잘못된 ID/JSON이면 `baseline_fallback`을 반환합니다.

`.env.example`은 설정 안내입니다. `.env` 자동 로딩은 구현하지 않았으므로 PowerShell 환경변수로 설정합니다. 이 PC에서 실제 모델 추론은 검증하지 않았고 MockTransport로 계약·실패 경로를 검증했습니다. 정상 초안 생성은 모델이 필요 없어 `provider=baseline`입니다.

Ollama의 [JSON Schema 출력](https://docs.ollama.com/capabilities/structured-outputs)과 [chat API](https://docs.ollama.com/api/chat)를 따릅니다. API 입력 검증은 [FastAPI/Pydantic](https://fastapi.tiangolo.com/tutorial/body/)을 사용합니다.

## 다음으로 읽을 문서

- [모듈형 에이전트 루프](docs/modular-agent-loop.md) — 기존 API와 별도로 실행하는 합성 다중 턴 프리뷰, 어댑터 및 플래너 교체 계약
- [STT → Jev 테스트 필드 명세](poc/jev/stt-jev-test-fields.md)
- [전체 개발 마일스톤](docs/development-milestones.md)
- [기존 프로젝트 분석과 연결 계획](docs/context-and-integration.md)
- [구조와 기술 선택](docs/architecture.md)
- [MVP 범위와 개발 순서](docs/mvp-scope.md)
- [평가 계획](docs/evaluation-plan.md)

`synthetic_test` 표시는 인증이나 개인정보 탐지 기능이 아닙니다. 이 서버에는 인증·동의·저장·삭제 기능이 없으므로 로컬 합성 데이터 시연에만 사용합니다.

## Jev 텍스트 분류 실험

STT 없이 합성 한국어 문장의 의미별 필드 후보를 Jev로 확인합니다. 실험 코드는 메인 에이전트와 분리된 `poc/jev/`에 있습니다. [필드 명세](poc/jev/stt-jev-test-fields.md)와 [PPO-5](https://linear.app/ppopy/issue/PPO-5)를 참고한 초기 실험이며, 현재 사용자 요청에 따라 `intent`는 테스트에서 제외합니다. 정확도 평가 완료를 뜻하지 않습니다. 프로젝트 루트의 `.env`에서 `jev-key`를 읽으며, `TYPESAFE_API_KEY` 환경변수가 설정되어 있으면 우선 사용합니다. `.env`는 Git에서 제외되어야 합니다. [TypeSafe API 문서](https://docs.typesafe.ai/introduction/quickstart)를 참고하세요.

PowerShell에서 실행합니다:

```powershell
.venv\Scripts\python.exe poc/jev/test_jev_text.py
```

문장을 입력하고 Enter를 누르면 결과가 표시되고 다음 문장을 입력할 수 있습니다. `/quit`으로 종료합니다. 명령 뒤에 따옴표로 문장을 넣으면 한 번만 실행할 수도 있습니다. `--verbose`를 추가하면 각 호출의 원시 응답과 전체 필드 확률을 확인할 수 있습니다. 입력은 외부 TypeSafe API로 전송되므로 처음에는 개인정보가 없는 합성 문장을 사용하세요. Noul은 확률이며 true/false로 확정하지 않습니다. 미언급과 명시적 부정은 별도 평가가 필요해 근거 상태는 `unassessed`입니다. 정확도는 사람이 정한 정답과 비교해야 하며, 이 스크립트는 자동 채점하지 않습니다.

전체 문장과 간단한 규칙으로 나눈 구절을 각각 평가하고, 구절별 `SLM 전달 후보`를 출력합니다. 후보 선택의 0.8 기준은 실험용이며 검증된 임계값이 아닙니다. 구절 분할은 의미 단위 추출을 보장하지 않고 문맥을 잃을 수 있습니다. 제품 사용 계획·사용 부정·증상 부정·정보 제공 거절 질문은 기존 7개 필드에 덧붙인 실험 항목입니다. 결과는 확인되지 않은 후보이며 실제 SLM 연동은 없습니다. 구절마다 별도 API 호출이 발생합니다.
