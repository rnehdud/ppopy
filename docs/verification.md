# Verification of the course snapshot

Executed locally on 2026-11-05 using Python 3.14 and pytest 8.4.2. The code uses Python 3.10+ syntax; other interpreter versions have not been tested in this export.

| Check | Observed result | What it establishes |
| --- | --- | --- |
| Source manifest | 27 exact file hashes match | Imported bytes match the selected source snapshot |
| KB validator | 95 passed, 0 failed | Structural references, inactive flags and reference-function checks |
| Extended boundary and current-spec trace tests | 371 passed | Existing branch behavior and exact preservation of all original audit signatures |
| Strict original test module | 62 passed, 5 failed | The original acceptance gaps remain visible |
| Original scenario audit | 52 of 57 satisfied | Two input conflicts, two expectation conflicts, one isolated policy case remain |
| Coverage tool | 60 cards; 213 conditional branches; 180 shared boundary cases | Execution coverage under explicitly structured inputs |
| Synthetic CLI fixture | Completed; `production_enabled=false` | Standalone preview runs without private data or cloud access |

The counts describe different checks and must not be added into a dataset size or a clinical/AI quality score. Trace tests verify that known discrepancies are preserved; they do not turn those discrepancies into satisfied original requirements.

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
mkdir -p outputs
python3 tools/verify_source_manifest.py
python3 KB/Poppy_KB_v0.6/validate_poppy_kb_v0_6.py --report outputs/kb-structure.json
python3 -m pytest -q tests/test_kb_preview_extended.py tests/test_kb_preview_current_spec.py
python3 -m skin_engine.kb_preview.coverage --output outputs/card-coverage.json
python3 -m skin_engine.kb_preview tests/fixtures/kb_preview/hot_water.json
```

`--report` is intentional: the original validator defaults to replacing its bundled historical report. Generated reports belong in ignored `outputs/`; the frozen source manifest and baseline stay unchanged.

Run the strict original checks separately. Both commands currently exit **1**:

```bash
python3 -m pytest -q tests/test_kb_preview.py
python3 -m skin_engine.kb_preview.audit --output outputs/original-acceptance57.json
```

Running all tests with `python3 -m pytest -q` also exposes those five failures. No skip/xfail or changed original expectation is used to make the full suite green.

## Open original acceptance mismatches

| Scenario | Recorded category | Preserved handling |
| --- | --- | --- |
| T17 | Input specification conflict | Original facts stay unchanged; complete-input synthetic revision is separate |
| T20 | Isolated policy case | Operational comparison stays source-blind; explicit development comparison is separate |
| T37 | Expectation conflict | Separate mixed-by-card revision preserves original per-card outputs |
| T45 | Expectation conflict | Separate mixed-by-card revision preserves original per-card outputs |
| V06-T04 | Input specification conflict | Original facts stay unchanged; complete-input synthetic revision is separate |

The frozen original audit is retained under `docs/launch_evidence/ledger/P3-A05-kb-ai-first-followup-20261105/original_acceptance57.json`. That path is imported provenance, not evidence of a new production approval.

## Limits

These checks do not validate natural-language understanding, clinical effectiveness, current legal compliance, a trained agent, an independent evaluation set, private product ingestion, the mobile application, or smart mirror integration. The KB and every preview result remain inactive for production.
