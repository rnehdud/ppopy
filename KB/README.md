# Shared knowledge base

The [v0.6 draft](Poppy_KB_v0.6/README_Codex_v0.6.md) is the shared design asset for cleansing, moisturizing, and sun protection. It includes 60 baseline cards, 234 variable definitions, nine functional domains, and seven lifecycle stages. These are design and knowledge structures, not participant counts or validated recommendation rules.

- [Structured seed](Poppy_KB_v0.6/Poppy_KB_seed_v0.6.json): canonical imported snapshot.
- [Taxonomy](Poppy_KB_v0.6/Poppy_KB_분류표_v0.6.md): navigation and card ownership.
- [Knowledge structure](Poppy_KB_v0.6/Poppy_KB_지식구조_v0.6.md): reviewable narrative.
- [Source manifest](../docs/source-manifest.json): source file hashes and export boundaries.

All operational activation remains off. The regulatory section preserves a **historical 2024 snapshot**; current full-text reconciliation is incomplete. Its source text and reference predicates are not current legal conclusions or personal safety thresholds. Manufacturer opinions remain labeled development material and do not establish quality rankings.

The bundle includes source metadata and original review states. It excludes the social-post corpus, PDF attachments, private product spreadsheet, and user records. The empty original `Cleansing.md` was not treated as a finished cleanser KB.

Validate without overwriting the bundled historical report:

```bash
mkdir -p outputs
python3 KB/Poppy_KB_v0.6/validate_poppy_kb_v0_6.py --report outputs/kb-structure.json
```

The 95 checks cover structure, references, inactive flags, and small reference-function boundaries. They do not establish clinical validity, current legal compliance, LLM quality, or completion of the engine's 57 original acceptance scenarios.
