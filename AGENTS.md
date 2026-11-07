# Ppopy course repository

Read the root README, `docs/repository-scope.md`, and the relevant course README before changing this repository.

- Make every commit and push on a separate task branch. Never commit, push, or merge directly to `main`; the developer decides whether to merge.

- This public repository serves CSE 406 and ITE 351. Preserve the existing team information and proposal history.
- The imported KB and engine are a dated development snapshot. `docs/source-manifest.json` records the original file hashes, including files that were uncommitted in SkinAnalysis. Do not describe them as a historical release.
- Keep `development_preview` and `production_enabled=false`. Do not enable real-user collection, production, payment, face analysis, or automatic improvement judgments.
- Keep observations, evidence, design defaults, hypotheses, and human judgments distinct. Unknown values must remain unknown. Do not invent labels, concentrations, pH, performance, review approvals, or clinical results.
- Preserve source-blind operational behavior. Manufacturer preferences in the imported snapshot are isolated development examples, not product quality scores or approved ranking rules.
- The original 57-scenario audit has five documented mismatches. Preserve the strict original tests and frozen audit. Do not hide failures with skip/xfail, rewrite expectations, or call current-spec trace tests proof of original acceptance.
- Do not commit credentials, personal questionnaires, feedback, contacts, raw third-party posts/PDFs, or private spreadsheet snapshots. Use synthetic inputs for shared examples.
- Do not copy more of SkinAnalysis by bulk add, mirror, or history push. Select and review files explicitly. Do not overwrite its human-maintained catalog or operational records.
- Run the documented verification commands. Send KB validator reports to `outputs/` using `--report`; its default overwrites the bundled historical report.
