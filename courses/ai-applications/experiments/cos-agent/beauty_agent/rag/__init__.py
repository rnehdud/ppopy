"""Reference literature RAG package for Ppopy v3."""

from beauty_agent.rag.corpus import (
    ALLOWED_DOMAINS,
    FORBIDDEN_KB_ID_PREFIXES,
    CorpusEntry,
    export_chunks_jsonl,
    load_chunks_jsonl,
    load_corpus_entries,
    parse_markdown_corpus_file,
    validate_evidence_ref_not_kb_id,
)
from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.query_builder import build_query
from beauty_agent.rag.retriever import TwoStageReferenceRetriever

__all__ = [
    "ALLOWED_DOMAINS",
    "CorpusEntry",
    "FORBIDDEN_KB_ID_PREFIXES",
    "export_chunks_jsonl",
    "load_chunks_jsonl",
    "load_corpus_entries",
    "parse_markdown_corpus_file",
    "validate_evidence_ref_not_kb_id",
    "HashFallback",
    "NoOpReranker",
    "build_query",
    "TwoStageReferenceRetriever",
]
