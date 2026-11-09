# Repository scope and reuse

Snapshot date: 2026-11-05.

Use **SkinAnalysis as the existing application and operational source**, and **ppopy as the course collaboration repository**. Reuse selected implementation and knowledge assets here, then develop course-specific specifications, evaluation tools, and experiments here. Keep the boundary visible to avoid maintaining two divergent production applications.

| Location | Responsibility |
| --- | --- |
| Existing private SkinAnalysis repository | Application implementation, catalogs, runtime policies, deployment, operational evidence and approval history |
| This public ppopy repository | Shared project overview, course specifications, imported inactive KB, local preview, synthetic cases, evaluation plans and reproducible course results |
| Existing private research repositories | Earlier experiments and restricted team records; no bulk publication or implied migration |

The export takes selected current working files, including uncommitted files. It does not copy Git history or claim the imported files all existed at the recorded source commit. Each exact copied file has its own SHA-256 in [source-manifest.json](source-manifest.json). The package initializer and public instructions are new so the preview can run independently.

## What was reused

- The complete v0.6 KB text/JSON bundle and its static validator.
- The standard-library v0.6 preview engine, rule branches, question handling, product-context adapter, coverage tools, and isolated comparison examples.
- Existing strict tests, boundary tests, the frozen original 57-case audit, and a synthetic CLI input.

A separate [sanitized app source snapshot](../app-snapshot/README.md) was added on 2026-11-09 for local UI and iOS project review. It does not replace the operational application. The operational backend, infrastructure, catalog XLSX, Google Sheets snapshots, credentials, user records, feedback, raw posts, product images, third-party PDFs, and earlier private model experiments are not copied. The course overview and smart mirror/AI evaluation documents are newly written summaries, not claims of newly implemented features.

## Continuing work

1. Put CSE 406 requirements and implementation decisions under `courses/software-engineering/`; put ITE 351 research protocols and experiments under `courses/ai-applications/`.
2. Use a branch such as `codex/describe-change` or a team feature branch and a pull request for changes. Keep source evidence, synthetic examples, and reviewed reference judgments distinct.
3. Change the imported snapshot only with an explicit version and change record. Keep the import hashes as historical provenance; do not regenerate them to hide drift.
4. Bring useful course work back to the application through a reviewed integration. Course test success does not activate production or approve new data use.

Existing team names, emails, roles, and proposal text in the root README were retained. This export does not grant access, invite collaborators, change repository visibility, or assign new team responsibilities.
