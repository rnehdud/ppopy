"""Load audited Markdown sidecars; no network or private source files required."""

from __future__ import annotations

import re
from hashlib import sha256
from pathlib import Path

from beauty_agent.v3_contracts import Layer2Metadata

LAYER2_DOMAINS = frozenset({"regulatory", "safety_method"})
ROW = re.compile(
    r"^\| (L2U-\d{4}) \| `(corpus/[^`]+)` \| `([^`]+)` \| `([^`]+)` \| "
    r"`([^`]+)` \| `([0-9a-f]{64})` \| `([0-9a-f]{64})` \|$",
    re.MULTILINE,
)
BLOCK = re.compile(r"^## (L2U-\d{4})\n(.*?)(?=\n## L2U-|\Z)", re.MULTILINE | re.DOTALL)


def load_layer2_bindings(corpus_dir: Path) -> dict[str, Layer2Metadata]:
    """Join unit identity to the exact section bytes, rejecting extras and drift.

    Original work/ledger paths in the manifest are provenance labels only. They
    are never opened. All inputs required for conversion ship in this package.
    """
    package = corpus_dir.parent
    manifest = (package / "CORPUS_MANIFEST.md").read_text(encoding="utf-8")
    metadata = (package / "METADATA.md").read_text(encoding="utf-8")
    rows = ROW.findall(manifest)
    if not rows or len(rows) != sum(
        line.startswith("| L2U-") for line in manifest.splitlines()
    ):
        raise ValueError("invalid layer2 manifest rows")
    units = {}
    for unit, block in BLOCK.findall(metadata):
        pairs = re.findall(r"^\| ([a-z_0-9]+) \| (.*?) \|$", block, re.MULTILINE)
        values = {k: v.strip("`") for k, v in pairs}
        if unit in units or len(pairs) != len(values) or values.get("unit_id") != unit:
            raise ValueError("duplicate/mismatched layer2 unit or field")
        # Administrative audit pointers are not evidence sent to the SLM.
        values.pop("fixed_input", None)
        units[unit] = values
    if len(rows) != len(units) or {r[0] for r in rows} != set(units):
        raise ValueError("layer2 manifest/metadata unit set mismatch")
    bindings = {}
    expected_sections: dict[str, set[str]] = {}
    for unit, rel, _origin, _ledger, source_id, section_hash, body_hash in rows:
        path = (package / rel).resolve()
        if not path.is_relative_to(corpus_dir.resolve()) or path.suffix != ".md":
            raise ValueError("unsafe layer2 corpus path")
        meta = Layer2Metadata(
            **units[unit], section_sha256=section_hash, body_sha256=body_hash
        )
        if source_id != meta.source_id or section_hash in bindings:
            raise ValueError("layer2 source mismatch or duplicate section")
        bindings[section_hash] = meta
        expected_sections.setdefault(rel, set()).add(section_hash)
    if {p.relative_to(package).as_posix() for p in corpus_dir.rglob("*.md")} != set(
        expected_sections
    ):
        raise ValueError("layer2 manifest/corpus file set mismatch")
    for rel, expected in expected_sections.items():
        raw = (package / rel).read_text(encoding="utf-8")
        sections = re.split(r"(?m)(?=^## )", raw)[1:]
        hashes = [sha256(s.strip().encode()).hexdigest() for s in sections]
        if len(hashes) != len(expected) or set(hashes) != expected:
            raise ValueError("layer2 section checksum or count mismatch")
    return bindings
