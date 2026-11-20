# Agent Runtime 아키텍처 — 현재 구현(As-Is) vs 청사진(To-Be)

이 문서는 `cos-agent`의 **현재까지 구현된 런타임 구조(As-Is)** 와 **목표 아키텍처 청사진(To-Be)** 을 한눈에 보기 쉽게 정리한 시각 자료입니다.

---

## 1. 현재까지 구현된 아키텍처 (As-Is · 실행 가능)

지금 `uv run --locked python -X utf8 -m beauty_agent.cli` 및 `pytest`(66개 통과)로 실제로 동작하는 구조입니다.

```mermaid
flowchart TD
    User["사용자 (터미널 입력)"] --> CLI["CLI 래퍼 (beauty_agent/cli.py)<br/>얇은 입출력 껍데기 (auto_apply_nlp_features=True)"]

    subgraph NLP["NLP Layer (beauty_agent/nlp_layer.py)"]
        Kiwi["1. Kiwi 형태소·구절 분할"] --> Jev["2. Jev API / 폴백<br/>제품명·증상·관계 추출"]
        Jev --> Map["3. MappingReview<br/>미확정 후보 검증"]
        Map --> SlotMap["4. 선제 Feature 추출 & 한국어 답변 매핑<br/>(얼굴→face, 미온수→lukewarm 등)"]
    end

    CLI -->|"한국어 자연어 발화 / 답변"| NLP
    NLP -->|"RuntimeTurnRequest (후보 + 매핑된 관찰)"| Runtime

    subgraph Runtime["Agent Runtime (beauty_agent/runtime.py)"]
        State["RuntimeSessionState<br/>(대기/재개 · active_cards · unrecognized 추적)"]
        Tools["합성 도구 스텁<br/>• lookup_weather (고정 합성 날씨)<br/>• lookup_product (합성 2종 카탈로그)<br/>• lookup_alternative (합성 대체품 1종)"]
        KB["KBEngineAdapter → PreviewEngine<br/>(Poppy_KB_v0.6 · rules.json)"]
        AFA{{"RoutedAFAPolicy (AFAPolicy 슬롯)<br/>• 기본: RuleBasedAFAPolicy<br/>• --ppo-model: B-C02 PPOAFAPolicy"}}
        Rec["RecommendationBundle 조립<br/>(생활습관 · 보유품 · 보류/제외 · 대체품)"]

        State --> Tools --> KB --> AFA
        AFA -->|"acquire(target_feature)"| Wait["awaiting_user (질문 반환 후 대기)"]
        AFA -->|"stop(sufficient)"| Rec
        AFA -->|"stop(insufficient) / 안전 신호"| Hold["held (보류 종료)"]
    end

    Wait -.->|"다음 턴 답변 시 동일 request_id로 재개"| CLI
    Rec -->|"KB 원문 기반 다중 권고 출력"| CLI
    Hold --> CLI
```

---

## 2. 전체 아키텍처 청사진 (To-Be · 목표 구조)

현재 구현된 코어(실선) 위에 앞으로 단계적으로 붙일 확장 계층(점선)을 합친 목표 구조입니다.

```mermaid
flowchart LR
    subgraph Clients["1. 클라이언트 계층"]
        CLI_Now["로컬 통합 CLI<br/>(구현 완료)"]
        iOS_Future["iOS 앱 / 스마트 미러<br/>(FastAPI api.py 래핑 예정)"]
    end

    subgraph RuntimeWrap["2. 오케스트레이션 (Agent Runtime)"]
        RT["Pure-Python Agent Runtime<br/>(구현 완료)"]
        LG["LangGraph + Checkpointer<br/>(운영/다중서버 복구 필요 시 래핑)"]
        RT -.->|"코드 수정 없이 노드화"| LG
    end

    subgraph AI["3. AI / 규칙 모듈"]
        NLP_Full["NLP Layer (Kiwi → Jev → Mapping)<br/>+ confirm_candidate 증상 확인 (예정)"]
        KB_Now["KB 규칙 엔진 (PreviewEngine)<br/>(구현 완료)"]
        AFA_Full{{"RL-AFA Policy (PPO)<br/>현재: B-C02 1차<br/>목표: 다중 카드 · 선행 Context 확장"}}
        Wording["LLM API / Local SLM<br/>질문·최종 권고 자연어 생성 (예정)"]
    end

    subgraph DataTools["4. 외부 도구 & AWS DB"]
        Weather["실제 날씨 API (예정)"]
        Catalog["AWS Aurora DB<br/>identity/service · catalog · care_sensitive (예정)"]
        Search["DB 미스 시 LLM 외부 검색 (예정)"]
    end

    Clients --> RuntimeWrap
    RuntimeWrap <--> NLP_Full
    RuntimeWrap <--> KB_Now
    RuntimeWrap <--> AFA_Full
    RuntimeWrap --> Wording --> Clients
    RuntimeWrap <-.-> Weather
    RuntimeWrap <-.-> Catalog
    Catalog -.->|"not_found"| Search -.-> RuntimeWrap
```

---

## 3. 구현 완료 vs 남은 청사진 요약

| 계층 | 현재 구현 완료 (`As-Is`) | 청사진 남은 작업 (`To-Be`) |
| --- | --- | --- |
| **인터페이스** | [cli.py](../beauty_agent/cli.py) 로컬 멀티턴 CLI | FastAPI(`api.py`) 연결 → iOS 앱 연동 |
| **NLP** | [nlp_layer.py](../beauty_agent/nlp_layer.py) (`Kiwi→Jev→Mapping`, 선제 추출, 한국어 답변 매핑) | `confirm_candidate` 증상 확인 루프 연결 |
| **Runtime** | [runtime.py](../beauty_agent/runtime.py) (상태·대기/재개·KB·PR#17 보완·`RecommendationBundle`) | `nlp.product_queries` → 제품 조회 연결, 운영 시 LangGraph 래핑 |
| **AFA Policy** | `RuleBasedAFAPolicy` + `B-C02` [policy_adapter.py](../beauty_agent/afa/policy_adapter.py) | 다중 카드 + 선행 Context 확장 PPO 학습 (Codex 병행) |
| **도구 · 출력** | 합성 날씨·카탈로그(2종)·대체품(1종) + KB 원문 출력 | 실제 날씨/Aurora DB/LLM 검색 + LLM/SLM 자연어 문구 생성 |
