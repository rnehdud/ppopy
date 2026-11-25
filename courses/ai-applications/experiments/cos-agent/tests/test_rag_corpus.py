"""Offline unit tests for Ppopy v3 Reference Literature corpus parsing & export."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import pytest

from beauty_agent.rag.corpus import (
    export_chunks_jsonl,
    load_chunks_jsonl,
    load_corpus_entries,
    parse_markdown_corpus_file,
    validate_evidence_ref_not_kb_id,
)
from beauty_agent.v3_contracts import ReferenceChunk

EXP_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = EXP_ROOT / "data" / "rag" / "corpus"
CHUNKS_JSONL = EXP_ROOT / "data" / "rag" / "chunks.jsonl"


def test_load_real_corpus_151_chunks() -> None:
    entries = load_corpus_entries(CORPUS_DIR)
    assert len(entries) == 151

    counts = Counter(entry.domain for entry in entries)
    assert dict(counts) == {
        "cleansing": 39,
        "moisturizing": 38,
        "sun_protection": 31,
        "storage_label": 43,
    }

    refs = [entry.chunk.evidence_ref for entry in entries]
    assert len(set(refs)) == 151
    assert refs[0] == "ref:cleansing-001"
    assert any(ref == "ref:storage_label-043" for ref in refs)

    for entry in entries:
        assert isinstance(entry.chunk, ReferenceChunk)
        assert entry.embedding_text == f"{entry.title}\n{entry.chunk.text}"
        validate_evidence_ref_not_kb_id(entry.chunk.evidence_ref)


def test_committed_chunks_jsonl_matches_corpus_and_no_bom() -> None:
    raw = CHUNKS_JSONL.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")

    chunks = load_chunks_jsonl(CHUNKS_JSONL)
    entries = load_corpus_entries(CORPUS_DIR)
    assert len(chunks) == 151
    assert chunks == [entry.chunk for entry in entries]


@pytest.mark.parametrize(
    "bad_ref",
    [
        "ref:U01",
        "ref:D12",
        "ref:F01",
        "ref:F02",
        "ref:S30",
        "ref:S31",
        "kb:cleansing-001",
        "ref:",
    ],
)
def test_validate_evidence_ref_blocks_kb_ids(bad_ref: str) -> None:
    with pytest.raises(ValueError):
        validate_evidence_ref_not_kb_id(bad_ref)


def test_validate_evidence_ref_allows_valid_ref() -> None:
    validate_evidence_ref_not_kb_id("ref:cleansing-001")
    validate_evidence_ref_not_kb_id("ref:storage_label-043")


def test_parse_rejects_missing_metadata_or_empty_body(tmp_path: Path) -> None:
    missing_meta = tmp_path / "missing_meta.md"
    missing_meta.write_text(
        "## [cleansing] Test Title\n"
        "- source_url: https://example.com\n"
        "- locator: p.1\n"
        "- checked_on: 2026-11-24\n"
        "- scope: general_skincare_practice\n\n"
        "Body paragraph.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="limitations"):
        parse_markdown_corpus_file(missing_meta)

    empty_body = tmp_path / "empty_body.md"
    empty_body.write_text(
        "## [cleansing] Test Title\n"
        "- source_url: https://example.com\n"
        "- locator: p.1\n"
        "- checked_on: 2026-11-24\n"
        "- scope: general_skincare_practice\n"
        "- limitations: None.\n\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="empty paragraph body"):
        parse_markdown_corpus_file(empty_body)

    bad_domain = tmp_path / "bad_domain.md"
    bad_domain.write_text(
        "## [clinical_diagnosis] Bad Domain\n"
        "- source_url: https://example.com\n"
        "- locator: p.1\n"
        "- checked_on: 2026-11-24\n"
        "- scope: general_skincare_practice\n"
        "- limitations: None.\n\n"
        "Body paragraph.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="invalid domain"):
        parse_markdown_corpus_file(bad_domain)


def test_export_and_load_roundtrip_tmp(tmp_path: Path) -> None:
    sample_md = tmp_path / "sample.md"
    sample_md.write_text(
        "# Sample\n\n"
        "## [moisturizing] Emollient basics\n"
        "- source_url: https://example.com/moist\n"
        "- locator: Sec 2\n"
        "- checked_on: 2026-11-24\n"
        "- scope: general_skincare_practice\n"
        "- limitations: General overview only.\n\n"
        "Moisturizers help reduce transepidermal water loss.\n",
        encoding="utf-8",
    )
    entries = parse_markdown_corpus_file(sample_md)
    out_path = tmp_path / "chunks.jsonl"
    written = export_chunks_jsonl(entries, out_path)
    assert written == 1
    assert not out_path.read_bytes().startswith(b"\xef\xbb\xbf")

    reloaded = load_chunks_jsonl(out_path)
    assert len(reloaded) == 1
    assert reloaded[0] == entries[0].chunk
    assert reloaded[0].evidence_ref == "ref:moisturizing-001"
