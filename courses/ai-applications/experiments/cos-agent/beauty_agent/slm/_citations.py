"""Shared extraction for generation and output validation."""

import re
import unicodedata

_BRACKETED_REF = re.compile(r"\[\s*((?:kb|ref|catalog|alternative):[^\]\r\n]*)\]", re.IGNORECASE)


def extract_citations(content: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", content)
    return list(dict.fromkeys(match.group(1).strip() for match in _BRACKETED_REF.finditer(normalized)))
