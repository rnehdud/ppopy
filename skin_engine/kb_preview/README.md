# KB development preview

This is a selected, runnable snapshot of the existing SkinAnalysis v0.6 preview. It uses the standard library and the bundled KB; it does not require the private application, product spreadsheet, cloud services, API keys, or a language model.

```bash
python3 -m skin_engine.kb_preview tests/fixtures/kb_preview/hot_water.json
mkdir -p outputs
python3 -m skin_engine.kb_preview.coverage --output outputs/card-coverage.json
python3 -m skin_engine.kb_preview.audit --output outputs/original-acceptance57.json
```

The audit currently returns exit code **1**: 52 of the 57 original scenarios satisfy their expectations; five retain documented input, expectation, or policy conflicts. This is preserved behavior, not a successful acceptance result. See [verification](../../docs/verification.md).

`engine.py` validates explicit observations, selects relevant cards, produces comparison states, handles exceptions and follow-up questions, and tracks sources. `rules.json` contains the structured branches. `adapter.py` separates product contexts. `filter_properties.py` uses explicitly reviewed records. `revisions.py` preserves separate revised synthetic cases. The default manufacturer comparison is source-blind; the explicit development comparison is not an operational policy.

All responses remain `development_preview` with `production_enabled=false`. The code does not infer undisclosed concentrations, diagnose skin, validate clinical effectiveness, or provide a trained AI agent. Natural-language interpretation and reviewed source judgments are separate work.

The original private product ingestion adapters, Google Sheets snapshot, v0.7 UI, and production application are outside this export. Their original README commands are not dependencies of this subset. File-level provenance is in [source-manifest.json](../../docs/source-manifest.json).
