# Poppy: Skincare Routine Support

Poppy explores how product information, user-reported context, and reviewed evidence can support decisions about an existing skincare routine. The project is shared across two courses: **ITE 351: AI & Applications** and **CSE 406: Software Engineering**.

The broader knowledge base (KB) is planned around three areas: cleansing, moisturizing, and sun protection. The initial AI research prototype focuses on facial cleansers. The three-area KB is under development; candidate evidence and AI outputs require review before they can become application rules.

## ITE 351: AI & Applications — Group Project Proposal

### Team Members

| Name | Organization | Email |
| --- | --- | --- |
| Doyeong Koo | Department of Information Systems | koody1125@hanyang.ac.kr |
| Takgeon Kang | Department of Information Systems | mms123601@gmail.com |
| Geonil Won | Department of Information Systems | To be added |
| Junhyeong Kim | Department of Information Systems | humbahumba605@gmail.com |

### Research Idea

**Title: An AI Agent for Evidence-Based Cleansing Routine Support**

Consumers may encounter cosmetic advice that overlooks their current routine or goes beyond available evidence. We propose an AI agent that uses a curated knowledge base, product information, and user context to support skincare routine decisions.

The broader Poppy knowledge base is planned around cleansing, moisturizing, and sun protection. Our initial research prototype focuses on facial cleansers. It will retrieve relevant evidence, identify information missing for a decision, and ask follow-up questions when needed. It may suggest maintaining or adjusting the current routine or considering an alternative product, while explaining the evidence and uncertainty.

We plan to compare the agent with a general-purpose language model using the same product and user scenarios. Evaluation will examine question relevance, the appropriateness of suggestions, unsupported claims, and agreement with domain-informed reference judgments. The topic, methods, and evaluation design are preliminary. AI outputs and unreviewed evidence will not automatically become approved recommendations.

## CSE 406: Software Engineering — Poppy and Smart Mirror

Team CosMate's software engineering project extends the existing Poppy application with a proposed smart mirror interface. The application is intended to support product search and confirmation, structured user input, routine review, and access to authorized results. The mirror is planned to show time and weather by default and present morning or evening skincare guidance when presence is detected.

The current direction is to develop the knowledge base across cleansing, moisturizing, and sun protection and specify how reviewed evidence, product information, user context, and safety constraints contribute to routine review. The AI research and the software engineering project share the broader Poppy topic, but their deliverables and evaluations are distinct.

The mirror's detailed display behavior, setup, failure handling, and authorization remain to be specified. Presence detection does not establish a person's identity, and personal results require an authorized user context. The usefulness of mirror guidance and the integrated workflow remain to be evaluated.

### Software Engineering Team

| Name | Course roles in the Phase 2 proposal |
| --- | --- |
| Doyeong Koo | Software developer; development manager |
| Kang Takgeon | User; customer; development manager |
| Won Konil | Customer; software developer |

## Project Progress

Project planning and evidence collection are in progress. Planned updates will document the KB structure and review process, datasets, methods, experiments, software specifications, results, and limitations. Plans and candidate evidence should not be interpreted as completed or validated functionality.

## Scope and Limitations

Poppy is intended to support informed routine decisions. It does not diagnose skin conditions, automatically judge skin improvement, or establish clinical effectiveness. Missing evidence and uncertainty should remain visible. Ingredient lists alone do not establish undisclosed concentrations or finished-product performance.
