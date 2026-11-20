# 뽀피 · Ppopy

뽀피는 **내가 가진 화장품과 실제로 쓰는 아침·저녁 루틴을 바탕으로, 무엇을 그대로 쓰고 무엇을 바꿀지 점검하는 iPhone 앱**입니다. 세정·보습·자외선차단 기준을 사용하며, 답에 따라 안내가 달라질 때 포포가 한 번에 한 가지를 묻습니다.

## 앱에서는 무엇을 할 수 있나요?

| 화면 | 사용자 흐름 |
| --- | --- |
| 탐색 | 제품명·브랜드 또는 제품 사진으로 후보를 찾습니다. 제품 상세에서 용량과 확인된 전성분을 봅니다. |
| 내 화장품 | 보유한 제품을 모으고 관리합니다. 아직 쓰지 않는 제품도 보관할 수 있습니다. |
| 내 루틴 | 보유 제품 중 실제 쓰는 제품을 골라 아침·저녁 사용 순서를 정합니다. |
| 루틴 점검 | 평소 루틴과 현재 불편감을 확인하고 필요한 질문에 답합니다. 이전 답을 고치면 관련 안내도 다시 계산합니다. |
| 저장한 점검 | 사용자가 저장한 결과를 다시 열어 당시의 안내를 확인합니다. |

## 질문과 결과가 만들어지는 과정

| 구성 | 맡은 일 |
| --- | --- |
| iOS 앱 (React · Capacitor) | 제품 검색·촬영, 루틴 편집, 선택형 질문과 답변 수정, 결과 표시 |
| 제품 카탈로그 | 제품 ID와 버전으로 검색 결과·전성분·루틴 항목을 연결합니다. 전성분이 비었거나 서로 충돌해도 제품은 찾을 수 있고 해당 성분 판단은 보류합니다. |
| 지식 기준(KB)과 판단 엔진 | 등록 제품, 확인된 사용 행동, 사용자 상태를 세 축의 기준 및 예외와 비교해 유지·조정·보류 가능한 행동을 구합니다. |
| 적응형 질문 선택(AFA) | 가능한 답을 비교해 다음 행동을 바꿀 질문을 고릅니다. 더 물어볼 실익이 없으면 그때까지 확인한 내용으로 마칩니다. |
| 서버와 저장소 (AWS HTTP API · Lambda · PostgreSQL) | 계정과 동의를 확인하고 점검 요청·답변·저장을 처리합니다. 카탈로그에서 찾기 어려운 제품은 외부 검색이나 사진 인식으로 탐색할 수 있습니다. |

**예시** · 최근 트러블을 점검할 때 사용자가 무엇이 바뀌었는지 모르겠다고 답하면, 다른 답에 따라 안내가 달라지는 경우 반복해서 피부를 문지르는지 확인합니다. 이전 답을 수정해 그 질문이 필요 없어지면 연결된 안내도 사라집니다. 트러블의 원인을 특정 제품으로 단정하지 않습니다.

## 어디까지 확인했나요?

2026-11-19 기준, iPhone에서 **1,977개 제품 카탈로그**의 검색과 루틴 화면 연결을 확인했습니다. 다음 통합 출시 후보에는 센카 브랜드 검색, 로벡틴 클렌징 워터의 전성분 표시 개선, 루틴 전체를 살피는 AFA v4를 묶었습니다. 이 후보는 iOS 빌드와 로컬 서버를 통한 답변 수정·저장·재열람 검증을 마쳤고, 공개 서버 전환과 설치 후 실기기 확인이 남아 있습니다.

## 저장소 둘러보기

이 공개 저장소에서 바로 실행할 수 있는 범위는 **합성 입력을 사용하는 KB 개발판**입니다. 앱의 화면 구현은 [선별 공개한 앱 소스](https://github.com/rnehdud/ppopy/tree/codex/ios-app-source-share/app-snapshot)에서 볼 수 있습니다.

- [KB 기준](KB/README.md) · [로컬 판단 엔진](skin_engine/kb_preview/README.md) · [실행 방법과 검증 결과](docs/verification.md)
- [소프트웨어공학 설계와 스마트 미러 제안](courses/software-engineering/README.md) · [AI 연구 및 평가 설계](courses/ai-applications/README.md)
- [공개 범위](docs/repository-scope.md) · [공개 파일의 출처](docs/source-manifest.json)

<details>
<summary>과목별 제안서 원문과 팀 구성 (영문)</summary>

## ITE 351: AI & Applications — Group Project Proposal

### Team Members

| Name | Organization | Email |
| --- | --- | --- |
| Doyeong Koo | Department of Information Systems | koody1125@hanyang.ac.kr |
| Takgeon Kang | Department of Information Systems | mms123601@gmail.com |
| Geonil Won | Department of Information Systems | lingsinsillicon12097@gmail.com |
| Junhyeong Kim | Department of Information Systems | humbahumba605@gmail.com |

### Research Idea

**Title: An AI Agent for Evidence-Based Cleansing Routine Support**

Consumers may encounter cosmetic advice that overlooks their current routine or goes beyond available evidence. We propose an AI agent that uses a curated knowledge base, product information, and user context to support skincare routine decisions.

The broader Ppopy knowledge base is planned around cleansing, moisturizing, and sun protection. Our initial research prototype focuses on facial cleansers. It will retrieve relevant evidence, identify information missing for a decision, and ask follow-up questions when needed. It may suggest maintaining or adjusting the current routine or considering an alternative product, while explaining the evidence and uncertainty.

We plan to compare the agent with a general-purpose language model using the same product and user scenarios. Evaluation will examine question relevance, the appropriateness of suggestions, unsupported claims, and agreement with domain-informed reference judgments. The topic, methods, and evaluation design are preliminary. AI outputs and unreviewed evidence will not automatically become approved recommendations.

## CSE 406: Software Engineering — Ppopy and Smart Mirror

### Latest Phase 2 submissions — 2026-11-06

The [Revised A and B LaTeX sources](courses/software-engineering/submissions/phase2/2026-11-06/README.md) specify history-based routine timing, context-dependent KB review and advance guidance on one authorized, output-only mirror. Questions, settings and plan approval remain in the app. This revision uses confirmed actual-use times for proactive delivery rather than a presence sensor.

### Initial proposal concept

Team CosMate's software engineering project extends the existing Poppy application with a proposed smart mirror interface. The application is intended to support product search and confirmation, structured user input, routine review, and access to authorized results. The mirror is planned to show time and weather by default and present morning or evening skincare guidance when presence is detected.

The current direction is to develop the knowledge base across cleansing, moisturizing, and sun protection and specify how reviewed evidence, product information, user context, and safety constraints contribute to routine review. The AI research and the software engineering project share the broader Poppy topic, but their deliverables and evaluations are distinct.

The mirror's detailed display behavior, setup, failure handling, and authorization remain to be specified. Presence detection does not establish a person's identity, and personal results require an authorized user context. The usefulness of mirror guidance and the integrated workflow remain to be evaluated.

### Software Engineering Team

| Roles | Name | Task description |
| --- | --- | --- |
| User | Takgeon Kang, Geonil Won | Review routine workflows, app questions and mirror usability. |
| Customer | Doyeong Koo | Define requirements, feature priorities, budget and acceptance criteria. |
| Software developer | All members | Koo: app/backend, KB and integration; Kang: agent questions and guidance; Won: mirror hardware and display. All: data collection and testing. |
| Development manager | All members (joint) | Share schedule and progress updates, agree on changes and review system integration. |

## Project Progress

Project planning and evidence collection are in progress. Planned updates will document the KB structure and review process, datasets, methods, experiments, software specifications, results, and limitations. Plans and candidate evidence should not be interpreted as completed or validated functionality.

</details>

## Scope and Limitations

Ppopy is intended to support informed routine decisions. It does not diagnose skin conditions, automatically judge skin improvement, or establish clinical effectiveness. Missing evidence and uncertainty should remain visible. Ingredient lists alone do not establish undisclosed concentrations or finished-product performance.

## Course Materials and Runnable Snapshot

The 2026-11-05 import reuses selected KB and development-preview files from the existing SkinAnalysis project. This public repository is the course workspace; the operational application remains separate. Team information and proposals above are retained.

| Start here | Contents |
| --- | --- |
| [Software Engineering](courses/software-engineering/README.md) | System responsibilities, smart mirror requirements and verification scope |
| [AI & Applications](courses/ai-applications/README.md) | Cleanser-agent research question, available assets and proposed evaluation |
| [Natural-language feature extraction PoC](courses/ai-applications/experiments/cos-agent/README.md) | Isolated Jev experiments, synthetic cases, regression tests and exploratory evaluation |
| [Knowledge base](KB/README.md) | Inactive v0.6 draft: cleansing, moisturizing and sun protection |
| [Local preview](skin_engine/kb_preview/README.md) | Runnable structured rule engine, source tracing and follow-up handling |
| [Repository scope](docs/repository-scope.md) | Reuse policy, export boundaries and future integration |
| [Verification](docs/verification.md) | Reproduction commands, observed results and five open acceptance mismatches |
| [Source manifest](docs/source-manifest.json) | Exact provenance and hashes for 27 imported files |

### Quick Start

Python 3.10+ is required. The preview and KB validator use only the standard library. Run from the repository root:

```bash
python3 -m skin_engine.kb_preview tests/fixtures/kb_preview/hot_water.json
mkdir -p outputs
python3 KB/Poppy_KB_v0.6/validate_poppy_kb_v0_6.py --report outputs/kb-structure.json
python3 tools/verify_source_manifest.py
```

The snapshot's KB structure checks pass, but its original 57-case acceptance audit retains five documented mismatches. It is a development preview, not a trained AI agent or a production release. See the verification page before reporting test results.
