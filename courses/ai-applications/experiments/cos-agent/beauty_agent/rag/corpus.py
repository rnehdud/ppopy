"""Semantic paragraph corpus parser and JSONL exporter for Ppopy v3 Reference RAG."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Sequence

from beauty_agent.v3_contracts import ReferenceChunk

ALLOWED_DOMAINS = frozenset({"cleansing", "moisturizing", "sun_protection", "storage_label"})
REQUIRED_META_KEYS = ("source_url", "locator", "checked_on", "scope", "limitations")
FORBIDDEN_KB_ID_PREFIXES = ("U", "D", "F01", "F02", "S30", "S31")
FORBIDDEN_KB_ID_RE = re.compile(r"^(?:[UD]\d+|F0[12]|S3[01])(?:$|[-_:])", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+\[(?P<domain>[a-z_]+)\]\s+(?P<title>.+?)\s*$")
META_RE = re.compile(r"^-\s+(?P<key>[a-z_]+):\s*(?P<value>.*)$")


@dataclass(frozen=True)
class CorpusEntry:
    """Parsed reference paragraph with domain/title metadata for embedding."""

    domain: str
    title: str
    source_file: str
    chunk: ReferenceChunk

    @property
    def embedding_text(self) -> str:
        """Return title + paragraph body for cross-lingual dense embedding."""
        return f"{self.title}\n{self.chunk.text}"


def validate_evidence_ref_not_kb_id(evidence_ref: str) -> None:
    """Ensure evidence_ref uses the 'ref:' namespace and does not mimic KB IDs."""
    if not evidence_ref.startswith("ref:"):
        raise ValueError(f"evidence_ref must start with 'ref:': {evidence_ref!r}")
    suffix = evidence_ref[len("ref:") :].strip()
    if not suffix:
        raise ValueError(f"evidence_ref suffix must not be empty: {evidence_ref!r}")
    if FORBIDDEN_KB_ID_RE.match(suffix):
        raise ValueError(
            f"evidence_ref must not reference KB card/evidence IDs: {evidence_ref!r}"
        )


def _split_sections(raw_text: str, source_name: str) -> list[list[str]]:
    """Split markdown text on '## ' headings after validating any preamble."""
    lines = raw_text.splitlines()
    sections: list[list[str]] = []
    current: list[str] | None = None

    for line_no, line in enumerate(lines, start=1):
        if line.startswith("## "):
            if current is not None:
                sections.append(current)
            current = [line]
            continue

        if current is None:
            stripped = line.strip()
            if stripped and not stripped.startswith("# "):
                raise ValueError(
                    f"{source_name}:{line_no}: unexpected preamble content before first '## ' heading: {line!r}"
                )
        else:
            current.append(line)

    if current is not None:
        sections.append(current)
    return sections


def parse_markdown_corpus_file(
    path: Path,
    *,
    domain_counters: dict[str, int] | None = None,
) -> list[CorpusEntry]:
    """Parse one Markdown corpus file into validated CorpusEntry objects."""
    if not path.is_file():
        raise FileNotFoundError(f"Corpus file not found: {path}")

    raw_text = path.read_text(encoding="utf-8")
    if raw_text.startswith("\ufeff"):
        raw_text = raw_text.lstrip("\ufeff")

    counters = domain_counters if domain_counters is not None else {}
    sections = _split_sections(raw_text, path.name)
    if not sections:
        raise ValueError(f"No '## [domain] Title' sections found in {path}")

    entries: list[CorpusEntry] = []
    for section_idx, section_lines in enumerate(sections, start=1):
        heading = section_lines[0].strip()
        heading_match = HEADING_RE.match(heading)
        if not heading_match:
            raise ValueError(
                f"{path.name} section {section_idx}: invalid heading format {heading!r}"
            )

        domain = heading_match.group("domain").strip()
        title = heading_match.group("title").strip()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(
                f"{path.name} section {section_idx}: invalid domain {domain!r}; "
                f"expected one of {sorted(ALLOWED_DOMAINS)}"
            )
        if not title:
            raise ValueError(f"{path.name} section {section_idx}: empty section title")

        meta: dict[str, str] = {}
        body_start_idx = len(section_lines)
        for idx in range(1, len(section_lines)):
            line = section_lines[idx]
            stripped = line.strip()
            if not stripped:
                if meta:
                    body_start_idx = idx + 1
                    break
                continue

            meta_match = META_RE.match(stripped)
            if meta_match:
                key = meta_match.group("key").strip()
                value = meta_match.group("value").strip()
                if key in meta:
                    raise ValueError(
                        f"{path.name} section {section_idx}: duplicate metadata key {key!r}"
                    )
                meta[key] = value
                body_start_idx = idx + 1
            else:
                body_start_idx = idx
                break

        missing_keys = [k for k in REQUIRED_META_KEYS if not meta.get(k)]
        if missing_keys:
            raise ValueError(
                f"{path.name} section {section_idx} ({title!r}): missing or empty metadata keys: {missing_keys}"
            )

        body_text = "\n".join(section_lines[body_start_idx:]).strip()
        if not body_text:
            raise ValueError(
                f"{path.name} section {section_idx} ({title!r}): empty paragraph body"
            )

        counters[domain] = counters.get(domain, 0) + 1
        evidence_ref = f"ref:{domain}-{counters[domain]:03d}"
        validate_evidence_ref_not_kb_id(evidence_ref)

        chunk = ReferenceChunk(
            evidence_ref=evidence_ref,
            text=body_text,
            scope=meta["scope"],  # type: ignore[arg-type]
            source_url=meta["source_url"],
            locator=meta["locator"],
            checked_on=meta["checked_on"],
            limitations=meta["limitations"],
        )
        entries.append(
            CorpusEntry(
                domain=domain,
                title=title,
                source_file=path.name,
                chunk=chunk,
            )
        )

    return entries


def load_corpus_entries(corpus_dir: Path) -> list[CorpusEntry]:
    """Load and validate all sorted Markdown files in corpus_dir."""
    if not corpus_dir.is_dir():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    md_files = sorted(corpus_dir.glob("*.md"))
    if not md_files:
        raise ValueError(f"No Markdown corpus files found in {corpus_dir}")

    domain_counters: dict[str, int] = {}
    entries: list[CorpusEntry] = []
    seen_refs: set[str] = set()

    for md_path in md_files:
        file_entries = parse_markdown_corpus_file(md_path, domain_counters=domain_counters)
        for entry in file_entries:
            ref = entry.chunk.evidence_ref
            if ref in seen_refs:
                raise ValueError(f"Duplicate evidence_ref across corpus: {ref!r}")
            seen_refs.add(ref)
            entries.append(entry)

    return entries


def export_chunks_jsonl(entries: Sequence[CorpusEntry], output_path: Path) -> int:
    """Write ReferenceChunk JSONL (UTF-8 without BOM, LF line endings)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(entry.chunk.model_dump(mode="json"), ensure_ascii=False)
        for entry in entries
    ]
    payload = "\n".join(lines) + ("\n" if lines else "")
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    return len(lines)


def load_chunks_jsonl(path: Path) -> list[ReferenceChunk]:
    """Load and validate ReferenceChunk rows from UTF-8 JSONL (rejecting BOM)."""
    if not path.is_file():
        raise FileNotFoundError(f"Chunks JSONL file not found: {path}")

    raw_bytes = path.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not allowed in {path}")

    raw_text = raw_bytes.decode("utf-8")
    chunks: list[ReferenceChunk] = []
    seen_refs: set[str] = set()
    for line_no, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            chunk = ReferenceChunk.model_validate_json(line)
        except Exception as exc:
            raise ValueError(f"{path}:{line_no}: invalid ReferenceChunk JSON: {exc}") from exc
        validate_evidence_ref_not_kb_id(chunk.evidence_ref)
        if chunk.evidence_ref in seen_refs:
            raise ValueError(f"{path}:{line_no}: duplicate evidence_ref {chunk.evidence_ref!r}")
        seen_refs.add(chunk.evidence_ref)
        chunks.append(chunk)

    return chunks
