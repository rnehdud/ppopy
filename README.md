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
| [Natural-language feature extraction PoC](courses/ai-applications/experiments/cos-agent/README.md) | Isolated Jev experiments, synthetic cases, regression tests and exploratory evaluation |
| [Knowledge base](KB/README.md) | v0.6.1 KB, sunscreen removal rules and worked case 6 |
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

## Product update (November 19, 2026)

Ppopy is an iPhone app that helps people decide what to keep or change in their skincare routine. Users choose the products they actually use in the morning and evening. Ppopy reviews that routine against guidance on cleansing, moisturizing, and sun protection. Popo, the in-app guide, asks one question at a time when the answer could change the advice.

### What users can do

| Screen | What happens there |
| --- | --- |
| Explore | Search by brand or product name, or take a photo of the packaging. Open a match to see its size and full ingredient list when available. |
| My Products | Keep an inventory of products, including ones the user owns but has yet to start using. |
| My Routine | Choose products from the inventory and arrange them in morning and evening application order. |
| Routine Check | Review the routine, report any discomfort, and answer relevant questions. Editing an earlier answer updates the guidance that depended on it. |
| Saved Checks | Reopen a saved check and read the guidance from that session. |

### How a routine becomes guidance

| Component | Responsibility |
| --- | --- |
| iOS app (React and Capacitor) | Captures product photos, displays search results, and lets users edit routines, answer questions, and review results. |
| Product catalog | Links search results, ingredient lists, and routine entries by product ID and version. Products with missing or conflicting labels stay searchable while ingredient-specific judgments remain on hold. |
| Knowledge base (KB) and decision engine | Compare confirmed product use and user observations with rules and exceptions for cleansing, moisturizing, and sun protection. Identify which steps to keep, adjust, or defer. |
| Adaptive question selection (AFA) | Compares what each possible answer would change, selects a useful follow-up, and stops when further questions would leave the guidance unchanged. |
| Backend (AWS HTTP API, Lambda, PostgreSQL) | Checks account access and consent, processes answers, and saves results. External search and photo recognition help identify products the catalog alone cannot match. |

For example, someone reporting a recent breakout may be unsure what changed. Ppopy can ask about repeated rubbing if the answer would change its advice. If the user revises an earlier answer and that question no longer applies, the related guidance disappears. The check leaves the cause of the breakout open.

### Release candidate status

As of November 19, 2026, the team had checked product search against the **1,977-product catalog** and opened the linked routine screen on an iPhone. The next candidate combines Senka brand search, an updated ingredient display for Rovectin cleansing water, and whole-routine AFA v4. It passed iOS builds and a local server test covering answer revision, saving, and reopening. Public API rollout and an on-device check of this combined candidate are pending.

### Explore the repository

Start with the [local KB preview](skin_engine/kb_preview/README.md) to run a synthetic routine check. The [app source snapshot](https://github.com/rnehdud/ppopy/tree/codex/ios-app-source-share/app-snapshot) shows selected iOS app screens. The [verification guide](docs/verification.md) documents what the public preview tests and where its results differ from the original expectations.
