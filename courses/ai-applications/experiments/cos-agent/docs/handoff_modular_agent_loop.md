# Handoff: 모듈형 에이전트 파이프라인 및 대화 루프 구현 (BeautyAgent)

> 이 문서는 최초 구현 단계의 인수인계 이력입니다. 현재 PR #13은 같은 작업 브랜치에서 액션 중심 플래너로 확장했습니다. 현재 계약·다이어그램·검증 방법은 [최종 구조 문서](modular-agent-loop.md)를 참조하세요. 아래의 베이스 브랜치·테스트 수·Section 5는 당시 체크리스트입니다.

다른 에이전트(Codex 등)나 새 작업 세션에서 이어서 바로 작업을 진행할 수 있도록 정리된 인수인계(Handoff) 문서입니다.

---

## 1. 프로젝트 컨텍스트 및 환경

- **작업 디렉토리**: `courses/ai-applications/experiments/cos-agent/` (저장소 루트: `C:\Users\mms12\orca\workspaces\cos-agent\ppopy-antigravity`)
- **현재 베이스 브랜치**: `codex/jev-skin-state-mapping-review` (commit `df70ca9`)
  > [!IMPORTANT]
  > **작업 시작 시 브랜치 규칙**: `main`에 직접 커밋/푸시하지 마시고, 반드시 새 작업 브랜치(`codex/modular-agent-loop` 등)를 생성하여 작업해야 합니다 (`AGENTS.md`).
- **Python 가상환경**: `courses/ai-applications/experiments/cos-agent/.venv` (Python 3.10.5, `uv` 패키지 매니저 관리)
- **사전 검증 통과 상태**:
  - `uv run pytest` -> 58/58 passed
  - `python tools/verify_source_manifest.py` -> 27/27 passed

---

## 2. 합의된 핵심 목표 및 요구사항

1. **모델 학습(QLoRA) 보류 및 에이전트 골격/루프 선(先)구현**:
   - 질문 생성 SLM 모델 학습에 앞서, **에이전트의 전체적인 틀과 단일/다중 턴 대화 루프(Loop)**를 먼저 모듈화하여 완성합니다.
   - 각 하위 단계가 독립적인 어댑터와 프로토콜 인터페이스로 격리되어, 지금은 규칙 기반(`baseline`)과 `ollama`로 완벽히 동작하고, 추후 학습된 **SFT-SLM 가중치만 `QuestionPlanner` 슬롯에 플러그인처럼 교체**할 수 있는 구조입니다.
2. **에이전트 루프가 연결할 4대 모듈**:
   - **Step 1: JevExtractorAdapter** (`poc/jev/relations.py`): Kiwi 형태소 분석 기반 의미단위 분할 및 제품/증상/시점/불확실성 관계 추출
   - **Step 2: MappingReviewAdapter** (`poc/jev/mapping_review/review.py`): 피부 상태 계약(`contract.json`) 검증 및 미확정 후보(`candidate_requires_user_and_time_confirmation`) 도출
   - **Step 3: KBEngineAdapter** (`skin_engine/kb_preview/engine.py`): Poppy KB v0.6 룰 엔진 평가, 사용자 질문 가능 슬롯(`ASK`)과 제품 DB 조회 슬롯(`RETRIEVE`) 엄격 분리
   - **Step 4: Pluggable QuestionPlanner** (`beauty_agent/planner.py`): 컨텍스트를 종합해 맥락 맞춤형 질문 생성 (규칙 기반 / Ollama / 향후 SFT-SLM)

---

## 3. 저장소 불변 규칙 및 제약사항 (`AGENTS.md`)

- **원본 보존**: `docs/source-manifest.json`에 기록된 27개 파일과 `KB/Poppy_KB_v0.6/`의 원본 파일, 57개 KB 감사 테스트는 수정하지 않습니다.
- **`ASK` vs `RETRIEVE` 경계**: 비공개 제품 제형 농도, 정확한 pH 등 사용자가 알 수 없는 제품 정보는 절대 사용자에게 역질문하지 않고 `RETRIEVE`로 라우팅합니다.
- **안전 게이트 및 권한 유지**: Jev 추출값과 Mapping Review 후보는 사용자 확인 전까지 임의로 `confirmed`로 승격하지 않습니다.
- **기존 계약 하위 호환성 100% 보장**: 기존 `POST /v1/agent/turn` 엔드포인트 및 `test_agent.py`의 모든 테스트가 그대로 통과해야 합니다.

---

## 4. 참조 문서 및 상세 구현 계획

- **상세 설계 계획서**: `courses/ai-applications/experiments/cos-agent/docs/sft_slm_qlora_plan.md`
  - 입출력 계약, 시퀀스 다이어그램, 모듈별 인터페이스 코드 스니펫 및 테스트 전략 포함
- **기존 핵심 코드 위치**:
  - 에이전트 코어: `beauty_agent/agent.py`, `contracts.py`, `planner.py`, `api.py`
  - Jev 관계 추출: `poc/jev/relations.py`
  - 매핑 검증: `poc/jev/mapping_review/review.py`
  - KB 프리뷰 엔진: `skin_engine/kb_preview/engine.py`

---

## 5. 다음 에이전트 실행 체크리스트 (Action Items)

다음 에이전트는 아래 순서에 따라 단계별로 구현 및 검증을 진행하면 됩니다:

1. **[Git] 새 작업 브랜치 생성**:
   ```powershell
   git checkout -b codex/modular-agent-loop
   ```
2. **[Contracts] 파이프라인 데이터 모델 확장** (`beauty_agent/contracts.py`):
   - `ObservationSlot`, `PipelineTrace`, `PlannerOutput` 모델 추가 (기존 계약 하위 호환 유지).
3. **[Modules] 3대 어댑터 구현** (`beauty_agent/modules/`):
   - `jev_adapter.py`: `extract_relations` 호출 및 `relations-0.3` -> `relations-0.2` 호환 뷰 브리지.
   - `mapping_adapter.py`: `mapping_review.review` 호출 및 `candidate_requires_user_and_time_confirmation` 추출.
   - `kb_adapter.py`: `PreviewEngine` 인스턴스화, `ask_slots`(`ASK`)과 `retrieve_slots`(`RETRIEVE`), `hold_signals` 도출.
4. **[Planner] Pluggable QuestionPlanner 인터페이스 및 구현** (`beauty_agent/planner.py`):
   - `QuestionPlanner` 프로토콜 정의.
   - `RuleBasedContextualPlanner` 구현 (우선순위: 위험/보류 신호 -> Jev/Mapping 미확정 확인 -> 기본 블로커 -> KB 관찰 질문).
   - 기존 `select_question()` 및 `OllamaContextualPlanner` 유지/연동.
5. **[Loop] 다중 턴 세션 매니저 및 파이프라인 결합** (`beauty_agent/loop.py` & `agent.py`):
   - `AgentSession` 클래스 구현 (`step(message) -> TurnResponse`, `SessionState` 상태 누적 관리).
   - 단일 턴 파이프라인 함수 `run_pipeline_turn(request)` 추가.
   - CLI 대화형 데모 진입점(`uv run python -m beauty_agent.loop --demo`) 추가.
6. **[Tests] 단위 및 통합 테스트 작성 및 회귀 검증**:
   - `tests/test_agent_loop.py` 작성:
     - 복합 발화 단일 턴 파이프라인 트레이스 검증
     - `ASK` vs `RETRIEVE` 분리 및 비공개 제품 정보 질문 금지 검증
     - 다중 턴 세션 상태 전이(`needs_information` -> `draft`) 검증
     - Pluggable Planner 교체 가능 여부 검증
   - 전체 검증 명령어 실행:
     ```powershell
     uv run pytest
     python tools/verify_source_manifest.py
     python tools/run_kb_57_audit.py
     ```
