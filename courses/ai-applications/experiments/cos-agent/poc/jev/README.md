# Jev backend skin-state field extraction

The default engine asks Jev for the **actual backend skin_state fields and allowed values**. It does not extract the old PoC symptom/product fields and map them afterward.

From `cos-agent/`:

```powershell
uv run python poc/jev/test_jev_text.py
```

Enter synthetic text at `Text>`. Each result shows the selected source phrase followed by backend field/value assignments in English. `/quit` exits.

The six Jev fields are `concern_presence`, `persistence`, `recent_change`, `discomfort_presence`, `discomfort_types`, and `sensitivity_history`. `kind` and `observed_at` come from explicit app input; `version` comes from the backend contract. Missing evidence withholds a field instead of inventing a value.

- `--json`: direct backend-field extraction and evidence metadata.
- `--app-json`: app handoff, missing backend inputs and confirmation state.
- `--verbose`: readable field output plus detailed extraction JSON.
- `--legacy-poc`: explicitly opt into the old experimental pipeline for historical reproduction only.

The key is read from `TYPESAFE_API_KEY`, then repository-root `.env`, then `cos-agent/.env`. Files support `jev-key` or `TYPESAFE_API_KEY`. Input is sent to the external TypeSafe API; use synthetic data without personal information.

[Current field definitions, behavior and verification](BACKEND_FIELDS.md) · [Backend contract and proposed extensions](../../docs/backend-contract-review.md) · [Historical PoC notes](LEGACY_POC.md)

All results require app confirmation and server authorization. HTTP transmission and DB storage remain disabled; development_preview and production_enabled=false are preserved.
