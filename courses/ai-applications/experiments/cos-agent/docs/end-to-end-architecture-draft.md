# Ppopy End-to-End AI Agent Architecture (v3 확정본)

> **목적**: 팀원 간 Ppopy 프로젝트의 전체 파이프라인·기술 스택·외부 데이터 연동 경계·개발 순서를 통일하기 위한 최종 확정 아키텍처 문서입니다.  
> **개발 원칙**: 먼저 **CLI MVP(Thin Wrapper)**로 세정·보습·자외선차단 3개 축 전체 흐름을 검증한 뒤, 동일한 1턴 코어(`request_id` Pause/Resume)를 HTTP API로 감싸 **iOS 앱**에 연결합니다.  
> **저장소 경계**: `development_preview`, `production_enabled=false`, 합성 입력 전용을 유지하며 `[Planned]` 항목은 향후 확장 범위입니다.

---

## 1. 최종 확정된 6대 아키텍처 결정

| 항목 | 확정 내용 | 채택 이유 |
| --- | --- | --- |
| **1. NLU Layer** | **3단계 Schema-Constrained NLU** (`Stage 0` 버튼 Fast Path 0ms → `Stage 1` 제품명 사전 힌트 → `Stage 2` SLM 1회 Structured JSON + `evidence_span` → `Stage 3` 화이트리스트·미확정 후보 검증) | 구절 분할 문맥 손실·외부 Jev 다중 호출·정규식 유지보수 제거. **2턴 이후 자유 타이핑도 직전 질문 문맥과 함께 동일 NLU 재사용** |
| **2. Control Plane** | **Deterministic Python State Machine (Central Hub)** | 매 턴 Tool Calling·AFA·RAG·SLM·Guardrail·Pause/Resume을 직접 지휘 |
| **3. AFA Policy** | **Myopic 1-Step Lookahead (VOI / Expected Branch Pruning)** + 정형 KB `v0.6.1` | 재학습 0회, 1ms 미만, 3영역 60카드 즉시 일반화, 100% 설명 가능 *(기존 PPO는 B-C02 비교군)* |
| **4. 질문 턴 UX** | **정형 KB 질문 + 선택지 버튼(Quick Reply) 기본 제공 (0ms)** | 모바일 UX 최상, 질문 턴 SLM·RAG 호출 0회로 응답 지연·비용 최소화 *(버튼 탭=Fast Path, 타이핑=NLU 재사용)* |
| **5. Reference RAG** | **2-Stage 로컬 FAISS (`faiss-cpu`) + `Qwen3-Embedding-0.6B` → `Qwen3-Reranker-0.6B`** *(2-Tier Corpus · 0ms Query Builder)* | Tier 1 공개 가이드라인(Section Chunking) + Tier 2 소규모 논문 7건(KB `review_scope`·`limitations` 요약 전용)으로 과잉 일반화 차단. `Embedder`/`Reranker`/`Retriever` 추상화로 CPU 테스트 및 추후 AWS `pgvector` 1줄 전환. **`SOLUTION_MODE` 전용** |
| **6. SLM 서빙** | **OpenAI-Compatible HTTP 추론 서버 (`vLLM` / `Ollama`, `/v1/chat/completions`)** · **Context + RAG 전용 생성** *(SLM–KB 완전 분리)* | Python 프로세스와 분리(재로딩 0초), URL 변경만으로 로컬 Qwen 3.5 4B QLoRA ↔ AWS GPU 교체, **15초 타임아웃 Baseline Fallback**. 앞단 AFA/Runtime만 KB로 정보 수집·HOLD를 수행하고, `SLMRequest`에서 `kb_judgments` 필드를 완전 제거해 **`confirmed_observations` + `product_evidence` + `rag_chunks`**만으로 솔루션을 생성 |

---

## 2. 전체 아키텍처 다이어그램 (SVG · 발표/문서 공유용)

![Ppopy End-to-End AI Agent Architecture v3](images/end-to-end-architecture-draft.svg)

---

## 3. Hub-and-Spoke 파이프라인 (Mermaid Flowchart)

```mermaid
flowchart TD
    subgraph Client["1. Client Channels (CLI MVP -> iOS App)"]
        ONB["초기 상태: Onboarding & Baseline Routine\n보유 제품 · 생활/식습관 · 루틴 입력"]
        NLQ["대화 턴 (Chat & Quick Reply)\n1턴: 자유 자연어 질문\n2턴+: 선택지 버튼(우선) 또는 자유 타이핑"]
        MIR["Smart Mirror (Planned · Output-Only)\n승인된 루틴 사전 안내 표시 · ACK"]
    end

    subgraph Ingress["2. Ingress & 3-Stage Schema-Constrained NLU"]
        ROUTER["Stage 0: Input Router (API Gateway / Auth)\n선택형 버튼 -> 0ms Fast Path (NLU 우회)\n자유 타이핑 -> Stage 1 진입"]
        NLU["Stage 1~3: Hybrid NLU (재사용)\n① 제품명 사전/Fuzzy 힌트 (~2ms)\n② SLM 1회 Structured JSON + evidence_span\n③ 화이트리스트 · 원문 대조 · 고위험 confirmed=False"]
    end

    subgraph ControlPlane["3. Agent Orchestrator / Control Plane (Central Hub)"]
        CP["Python State Machine (CLI / AWS Lambda)\n① Parallel Tool Calling & Context Hydration\n② Myopic VOI AFA 호출 및 분기 제어\n③ 질문 턴: 정형 버튼(0ms) / 솔루션 턴: RAG+SLM 1회\n④ Hard Guardrail 검증 · Pause/Resume · Fallback"]
    end

    subgraph DataExt["4. Data Stores, Tools & Local Reference RAG"]
        DB["AWS Aurora PostgreSQL (RDS Data API)\nuser_observations(EAV) · user_products\nVersioned INCI Catalog · 정형 KB v0.6.1"]
        WAPI["External Data APIs\nWeather/UV API · Optional Product OCR"]
        RAG["Local Reference Literature RAG (2-Tier Corpus)\nTier 1 가이드라인 섹션 + Tier 2 논문 KB 요약\n0ms Query Builder -> Qwen3-Embedding-0.6B -> FAISS\n-> Qwen3-Reranker-0.6B + Threshold (추후 pgvector 전환)"]
    end

    subgraph Workers["5. Decision, Local GPU Generation & Safety Workers"]
        AFA["5A. Myopic 1-Step Lookahead AFA\n60카드 전체 가상 분기 시뮬레이션\nacquire(feature) / stop(sufficient | hold)"]
        SLM["5B. Qwen 3.5 4B QLoRA Server\nOpenAI-Compatible HTTP (vLLM / Ollama)\nContext + Product + RAG 기반 유연 생성\n(Optional KBPolicyAnchorAdapter: 기본 OFF)\n15초 타임아웃 시 Rule Baseline Fallback"]
        GRD["5C. Deterministic Safety Guardrail (Python)\n필수 HOLD · 비임상/비진단 · 인용·버전 검증"]
    end

    subgraph Feedback["6. State Commit & Closed-Loop Feedback (Planned)"]
        COMMIT["Explicit User Approval & Context Commit\n승인 시 Aurora 갱신 (saved=True)"]
        SCHED["Async Follow-up Scheduler (EventBridge)\nN일 후 솔루션 만족도 피드백 프롬프트"]
        COHORT["Context-Cohort Social Proof [Planned]\n유사 맥락 설문 만족도 (N>=30, 비임상 고지)"]
    end

    ONB --> ROUTER
    NLQ --> ROUTER
    ROUTER -->|"선택형 버튼 (Fast Path 0ms)"| CP
    ROUTER -->|"자유 자연어 발화"| NLU
    NLU -->|"정규화된 후보 JSON"| CP

    CP <-->|"① Parallel Lookup"| DB
    CP <-->|"① Parallel Tool Call"| WAPI
    CP <-->|"② Decision Call"| AFA
    CP <-->|"③ Stop(sufficient) 시 검색"| RAG
    CP <-->|"③ HTTP /v1/chat/completions"| SLM
    CP <-->|"④ 출력 검증"| GRD

    CP -->|"ASK (정형 질문+버튼 · 0ms Pause)"| NLQ
    CP -->|"HOLD (held · 종료)"| NLQ
    CP -->|"RECOMMEND (승인 대기)"| COMMIT
    COMMIT --> DB
    COMMIT -.->|"Planned"| MIR
    COMMIT -.-> SCHED
    SCHED -.->|"긍정/부정 피드백 로그"| DB
    DB -.-> COHORT
    COHORT -.->|"검증된 집계 통계만 역주입"| CP
```

---

## 4. 멀티턴 시퀀스 (버튼 Fast Path + 자유 타이핑 NLU 재사용)

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자 (CLI / iOS App)
    participant RT0 as Stage 0 Router + NLU
    participant CP as Control Plane (Python Hub)
    participant TOOLS as Aurora DB + Weather API
    participant AFA as Myopic VOI AFA
    participant RAG as Local Vector DB RAG
    participant SLM as Qwen 3.5 4B (HTTP Server)
    participant GRD as Safety Guardrail

    User->>RT0: 1턴 자유 발화: "내수성 선크림이 잘 안 지워져서 세안을 두 번 해요"
    RT0->>RT0: Stage 1(제품 힌트) → Stage 2(SLM JSON + evidence_span) → Stage 3(검증)
    RT0->>CP: request_id + 정규화 후보 JSON

    par Step 1. Parallel Context Hydration
        CP->>TOOLS: User Context(EAV) & 보유제품 버전별 전성분 조회
        CP->>TOOLS: Weather/UV API 조회
    end
    TOOLS-->>CP: Hydrated Context 반환

    CP->>AFA: 현재 Context + 정형 KB v0.6.1 조건 전달
    AFA-->>CP: acquire(required_feature="cleansing.method")

    Note over CP,User: 질문 턴은 RAG·SLM 생략(0ms) → 정형 질문 + 선택지 버튼(Quick Reply) 반환
    CP-->>User: status="awaiting_user" (버튼: 클렌징워터 / 폼 / 오일 / 잘 모름)

    alt 사용자가 버튼 탭 (Fast Path · 0ms)
        User->>CP: 정형 선택 ("클렌징 폼만 사용") — NLU 완전 우회
    else 사용자가 자유 텍스트 타이핑 (NLU 재사용)
        User->>RT0: "그냥 폼클렌저로만 두 번 씻어요"
        RT0->>CP: 직전 질문 맥락 포함 NLU 재추출 결과 전달
    end

    CP->>AFA: 갱신된 확정 Context 전달
    AFA-->>CP: stop(reason="sufficient")

    Note over CP,SLM: 최종 솔루션 턴에서만 0ms Query Builder + 2-Stage Vector RAG + OpenAI-Compatible HTTP SLM 1회 호출
    CP->>RAG: 확정 Context 기반 0ms Query -> Bi-Encoder(Top-15) -> Reranker+Threshold(Top-3~5)
    RAG-->>CP: 검증된 문헌 청크(Scope/Limitations 포함) + Citation ID 반환
    CP->>SLM: POST /v1/chat/completions [SOLUTION_MODE] Context + Product + RAG 청크 (KB Anchor 기본 OFF)
    SLM-->>CP: 최종 루틴 Solution + [ref:ID] 인용 + 불확실성 설명
    CP->>GRD: 필수 HOLD · 비임상 주장 · 미제공 ID · 제품 버전 검증
    GRD-->>CP: 통과 (requires_approval=True, saved=False)
    CP-->>User: status="completed" (승인 대기)
```

---

## 5. 자연어 → DB Field 매핑 구조

자연어를 DB 컬럼에 직접 넣지 않고, **표준 슬롯 사전(Canonical Schema) → PostgreSQL EAV 테이블**로 2단계 매핑합니다:

1. **SLM 정규화**: 자유 발화(*"수건으로 세게 닦아요"*) → 표준 코드값(`{"variable_id": "method.drying", "value": "rubbing_strongly", "evidence_span": "수건으로 세게 닦아요"}`).
2. **Python 검증 및 저장**:
   - **고정 테이블 (`user_products`)**: 확인된 보유 제품(`product_id`, `version`, `confirmed=true`).
   - **관찰 EAV 테이블 (`user_observations`)**: KB의 234개 변수를 컬럼 추가 없이 `(user_id, variable_id, state, value, confirmed_by_user, observed_at)` 행(Row)으로 저장.

---

## 6. 단계별 개발 순서 (Critical Path)

1. **Phase 0 — 계약 고정 (Contract-First PR · `PPO-40`)**: 4개 모듈 간 Pydantic JSON 스키마(`NLU`, `AFA`, `RAG ReferenceChunk`, `SLMRequest/SLMResponse`, `CLI/iOS TurnResponse`) 및 검증 테스트 확정.
2. **Phase 1 — 코어 뼈대 & CLI MVP**: Control Plane + 3영역 `Myopic VOI AFA` + `Hard Safety Guardrail` 완성 (초기엔 Mock/Base SLM으로 전체 CLI 루프 검증).
3. **Phase 2 — 로컬 Reference RAG 청크 풀 선확정 & 3단계 NLU** *(Phase 1·Phase 3 파일럿과 병렬)*: 사용자 투입 2-Tier Corpus(Tier 1 공개 가이드라인 발췌 + Tier 2 소규모 논문 7건 요약) 기반 실제 `ReferenceChunk` 풀 확정 → `Qwen3-Embedding-0.6B` + `faiss-cpu` + `Qwen3-Reranker-0.6B` (`Recall@5 ≥ 90%`) 구축, 3단계 NLU 검증.
4. **Phase 3 — `rag-free` Zero-Base 합성 데이터셋 2단계 생성 (`PPO-37`)**: [qlora-synthetic-dataset-guide.md](qlora-synthetic-dataset-guide.md) 기준으로 ① **Step 1 (즉시 병렬)** 24턴 파일럿으로 병렬 Subagent 생성·`--profile rag-free` 검증·다른 팀원 에이전트 Cross-Model Critic 파이프라인 점검 → ② **Step 2 (Phase 2 실제 RAG 청크 풀 확정 후)** 실제 `ReferenceChunk` 풀을 `rag_chunks` 재료로 사용해 **100% Zero-Base 신규 합성 (`new_synthetic`, `v67` 재가공 없음)** 3영역/Hard Negative(≥25%) 900턴 생성(Zero Chunk Skew).
5. **Phase 4 — QLoRA SFT (`Qwen 3.5 4B`) 학습 & 2×2 Ablation 평가 (ITE 351)**: 로컬 `vLLM`/`Ollama` HTTP 서버로 교체 연결 후 동일 평가셋에서 **`SLM` / `SLM+RAG` / `SLM+SFT` / `SLM+SFT+RAG`** 2×2 Ablation(KB Anchor OFF 기본) 정량 비교.
6. **Phase 5 — iOS 래핑 & AWS 통합 (CSE 406)**: 동일 1턴 코어를 HTTP API로 래핑해 iOS 연동 + 타임아웃 Fallback 검증. 이후 `[Planned]` EventBridge 피드백 Log-only 수집 → 표본 $N \ge 30$ 충족 시 Social Proof 활성화.

---

## 7. RAG & End-to-End 평가 체계 (Hybrid Evaluation)

| 평가 층 | 핵심 지표 | 평가 방식 |
| --- | --- | --- |
| **1층 · Retrieval 평가** (`eval_rag_retrieval.py`) | `Recall@5`, `MRR@5` / `NDCG@5`, `Context Relevance`, `Coverage`, `Negative Rejection` | 40~50문항 골든 질의셋 기반 결정적 비교 (Baseline vs Bi-Encoder vs **+Reranker+Threshold**) |
| **2층 · Generation 안전·규율** (`eval_rag_generation.py`) | `Citation Precision`(100%), `Distractor Rejection`(100%), `HardSafetyGuardrail` 준수율(100%) | Python 결정적 규칙·화이트리스트 자동 검증 (0원, 100% 재현) |
| **2층 · Generation 품질** (`eval_rag_generation.py`) | `Faithfulness`(충실성), `Correctness`(정확성), `Completeness`(완전성) | **LLM-as-a-Judge** (1~5점 루브릭 + `must_not_claim`/`limitations` 감점 규칙, Student와 다른 모델 계열 사용) + 저득점·임상절제 표본 사람 검수 |
