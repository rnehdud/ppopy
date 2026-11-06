# Ppopy: Skincare Routine Support

Ppopy explores how product information, user-reported context, and reviewed evidence can support decisions about an existing skincare routine. The project is shared across two courses: **ITE 351: AI & Applications** and **CSE 406: Software Engineering**.

The broader knowledge base (KB) is planned around three areas: cleansing, moisturizing, and sun protection. The initial AI research prototype focuses on facial cleansers. The three-area KB is under development; candidate evidence and AI outputs require review before they can become application rules.

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

## Scope and Limitations

Ppopy is intended to support informed routine decisions. It does not diagnose skin conditions, automatically judge skin improvement, or establish clinical effectiveness. Missing evidence and uncertainty should remain visible. Ingredient lists alone do not establish undisclosed concentrations or finished-product performance.

## Course Materials and Runnable Snapshot

The 2026-11-05 import reuses selected KB and development-preview files from the existing SkinAnalysis project. This public repository is the course workspace; the operational application remains separate. Team information and proposals above are retained.

| Start here | Contents |
| --- | --- |
| [Software Engineering](courses/software-engineering/README.md) | System responsibilities, smart mirror requirements and verification scope |
| [AI & Applications](courses/ai-applications/README.md) | Cleanser-agent research question, available assets and proposed evaluation |
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
