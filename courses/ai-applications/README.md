# ITE 351 — AI & Applications

Current proposal: **An AI Agent for Evidence-Based Cleansing Routine Support**. The shared KB covers cleansing, moisturizing, and sun protection; the initial research evaluation focuses on facial cleansers.

The agent is intended to retrieve relevant evidence, identify information needed for a decision, ask useful follow-up questions, and explain uncertainty when maintaining or adjusting a routine or considering a product alternative. This repository does not yet contain a trained agent, an independent labeled dataset, or a completed AI comparison.

## Assets available now

- A [v0.6 draft KB](../../KB/README.md) with explicit source/review states and conditional information requirements.
- A deterministic [local preview](../../skin_engine/kb_preview/README.md) for structured observations, card comparison, follow-up updates, exceptions and evidence tracing.
- Synthetic scenarios and software regression tests. They are development assets, not independent expert labels or clinical results.

The preview is ordinary rule-based code. A passing preview test is not an LLM score, proof that a rule is true, or evidence that an agent benefits users. Earlier claim-verifier/model-comparison work in private repositories is separate historical work; its results are not imported as cleanser-agent results.

## Proposed experimental design

The following is a course plan to finalize before collecting final test judgments.

| Comparison | What it would test |
| --- | --- |
| General-purpose model with the same product/scenario input | Baseline under recorded model, date, search and personalization conditions |
| Same model with a fixed reviewed evidence bundle | Added value of access to evidence |
| Same model with evidence plus explicit question-selection/verification steps | Added value of the agent procedure |

Keep product identity, scenario information and model settings comparable. An application-level comparison against a chat product should be reported separately from a controlled same-model method comparison.

1. Define cleanser scenarios and reviewed product versions. Keep synthetic cases, real product facts, and participant records separate.
2. Record which missing information concerns the user (`ASK`) and which concerns product/source evidence (`RETRIEVE`). Asking a user cannot reveal a private formula.
3. Prepare domain reference judgments independently of generated answers. Keep reviewer identity, review status and unresolved judgments explicit. Do not create a reference label from the model's own answer.
4. Separate product/formulation families across development and final evaluation. Keep final references inaccessible to runtime retrieval and tuning.
5. Record first answers and follow-up interactions, retrieval failures, missing sources and refusals. Define the interaction budget before comparing systems.
6. Report denominators, uncertainty, disagreement and failure examples alongside aggregate metrics.

Candidate metrics are question relevance and burden, appropriateness of maintain/adjust/hold decisions, unsupported or contradictory claims, citation entailment, important omissions, and agreement with reviewed references. Their rubric, sample size, raters and final test split remain to be decided. No performance values are claimed.

## Boundaries

Use public factual product fields and synthetic user context for shared development. Do not publish raw third-party corpora or personal questionnaires. Keep ingredient identity, disclosed ingredient amount, undisclosed active concentration, finished-product performance and personal suitability distinct. Do not infer undisclosed pH/concentrations or score manufacturer quality. Research output does not become an application rule without separate review and integration.
