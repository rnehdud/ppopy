"""Morpheme-based semantic units for the Jev PoC (Kiwi).

A unit is a predicate-centred span split at sentence endings, clause punctuation
and selected connective endings. Offsets are Unicode code points of the source
text, matching the existing `relations-0.x` contract. Boundaries are deterministic
development heuristics, not a validated Korean parser. When `kiwipiepy` is not
installed every helper falls back to the earlier punctuation/eojeol behaviour and
reports `segmentation_method='punctuation_fallback'`.

Usage (offline, no API): python -m poc.jev.segmenter --dump poc/jev/evaluation_data/diverse-v1.json
"""
import json
import re
import sys
from collections import namedtuple
from functools import lru_cache

try:
    from kiwipiepy import Kiwi
except ImportError:  # pragma: no cover - exercised only without the dependency
    Kiwi = None

Token = namedtuple('Token', 'form tag start end')

# Connective endings that join two predicates describing separate states/events.
SPLIT_EC = {'지만', '는데', '은데', '\u11ab데', '던데', '고', '어서', '아서', '여서', '다가', '면서', '으면서',
            '니까', '으니까', '\u11ab니까', '더니', '길래'}
# Without punctuation Kiwi often reads a final -어/-아 as a connective (E20/E24 STT form).
RUNON_EC = {'어', '아', '여'}
NOUNISH = {'NNG', 'NNP', 'SL', 'SN', 'SH', 'XR', 'XPN', 'XSN'}
# Candidate pruning only. Removing a word here never decides that a product is absent.
TIME_WORDS = {'오늘', '어제', '그저께', '내일', '모레', '아침', '오전', '점심', '낮', '오후', '저녁', '밤', '새벽', '최근', '요즘', '지금'}
STOP_NOUNS = {'피부', '얼굴', '증상', '제품', '제품명', '화장품', '이야기', '날씨', '답변', '거절', '기억', '정도',
              '예정', '실제', '정확', '시작', '약간', '친구', '엄마', '아빠', '동생', '언니', '오빠', '형', '누나',
              '건조', '트러블', '여드름', '뾰루지', '좁쌀', '홍조', '말', '세안', '세수', '이중세안'}
GENERIC_CATEGORIES = {
    '크림', '로션', '토너', '세럼', '앰플', '에센스', '미스트', '오일', '폼',
    '클렌징', '클렌저', '클렌징폼', '클렌징오일', '클렌징워터', '선크림', '선세럼',
    '선스틱', '선젤', '패드', '팩', '마스크', '마스크팩', '젤', '수딩젤', '밤', '워시',
    '스킨', '필링', '스크럽', '아이크림', '수분크림', '시카크림', '겔크림'
}
NEGATORS = (('VX', '않'), ('VX', '못하'), ('VA', '없'))

COSMETIC_WORDS = (
    # Categories / Types
    ('클렌징밤', 'NNG'), ('클렌징오일', 'NNG'), ('클렌징워터', 'NNG'), ('클렌징폼', 'NNG'),
    ('선세럼', 'NNG'), ('선크림', 'NNG'), ('선스틱', 'NNG'), ('선젤', 'NNG'), ('선베이스', 'NNG'),
    ('수딩젤', 'NNG'), ('토너패드', 'NNG'), ('수분크림', 'NNG'), ('시카크림', 'NNG'),
    ('세럼', 'NNG'), ('앰플', 'NNG'), ('미스트', 'NNG'), ('토너', 'NNG'), ('에센스', 'NNG'),
    ('패드', 'NNG'), ('아이크림', 'NNG'), ('나이트크림', 'NNG'), ('겔크림', 'NNG'),
    # Ingredients / Brand roots / Modifiers
    ('수딩', 'NNG'), ('블레미쉬', 'NNG'), ('어니언', 'NNG'), ('다이브인', 'NNP'),
    ('노스카나인', 'NNP'), ('어성초', 'NNG'), ('시카', 'NNP'), ('판테놀', 'NNG'),
    ('히알루론산', 'NNG'), ('나이아신아마이드', 'NNG'), ('레티놀', 'NNG'), ('세라마이드', 'NNG'),
    ('약산성', 'NNG'), ('여드름성', 'NNG'), ('화농성', 'NNG'), ('붉은기', 'NNG'),
)


def available():
    return Kiwi is not None


def segmentation_method():
    return 'kiwi_morpheme' if available() else 'punctuation_fallback'


@lru_cache(maxsize=1)
def _kiwi():
    k = Kiwi()
    for word, tag in COSMETIC_WORDS:
        k.add_user_word(word, tag)
    return k


def _base(tag):
    return tag.split('-')[0]


@lru_cache(maxsize=512)
def tokens(text):
    """Kiwi tokens with code-point offsets; contracted morphemes may share offsets."""
    out = []
    for t in _kiwi().tokenize(text):
        start = t.start
        out.append(Token(t.form, _base(t.tag), start, max(start, start + t.len)))
    return tuple(out)


def _punct(tok):
    return tok.tag.startswith('S') and tok.tag not in ('SL', 'SN', 'SH')


def _content(tok):
    return tok.tag[0] in 'NVMX' and tok.tag != 'NP' or tok.tag in ('SL', 'SN', 'SH')


def splits_after(toks, i):
    """True when a connective ending at index i closes a semantic unit."""
    tok = toks[i]
    if tok.tag != 'EC':
        return False
    nxt = next((x for x in toks[i + 1:] if x.tag != 'JX'), None)
    if nxt is None or _punct(nxt) or nxt.tag == 'VX':
        return False
    prev = toks[i - 1] if i else None
    if tok.form == '고' and prev is not None and prev.form == '말' and prev.tag == 'VV':
        return False  # "A 말고 B" correction stays one unit
    if prev is not None and prev.form == '들' and tok.form == '어':
        return False  # "요즘 들어", "최근 들어" temporal phrase stays in unit
    if i >= 2 and toks[i - 2].form in ('반복', '계속', '더', '비') and toks[i - 1].form == '하' and tok.form in ('어서', '여서'):
        return False  # "반복해서 나다", "계속해서 생기다" adverbial stays in unit
    if tok.form in SPLIT_EC:
        return True
    return tok.form in RUNON_EC and nxt.tag not in ('VV', 'VA', 'VX')


def _fallback_units(text):
    try:
        from .context_evidence import clause_spans
    except ImportError:
        from context_evidence import clause_spans
    return [{'unit_id': f'u{i}', **c, 'tokens': []} for i, c in enumerate(clause_spans(text))]


def units(text):
    """Split text into semantic units; trailing punctuation stays with its unit."""
    if not available():
        return _fallback_units(text)
    toks = tokens(text)
    out, current, pending = [], [], False

    def flush():
        body = [t for t in current if not _punct(t) and t.tag != 'IC']
        if body:
            start, end = body[0].start, max(t.end for t in current)
            out.append({'unit_id': f'u{len(out)}', 'start': start, 'end': end, 'text': text[start:end],
                        'tokens': [[t.form, t.tag, t.start, t.end] for t in current]})
        current.clear()

    for i, tok in enumerate(toks):
        if current and '\n' in text[current[-1].end:tok.start]:
            flush()
            pending = False
        if pending:
            if _punct(tok):
                current.append(tok)
                continue
            if tok.tag[0] in 'JE':
                pending = False  # e.g. 가려운지/EF + 는/JX continues the unit
            else:
                flush()
                pending = False
        current.append(tok)
        if tok.tag == 'EF' or tok.tag == 'SF' or (tok.tag == 'SP' and tok.form in ',;，；') or splits_after(toks, i):
            pending = True
    flush()
    return out


def _in(scope, tok):
    return scope['start'] <= tok.start < scope['end']


def lexicon_hits(text, scope, patterns):
    """Symptom names whose pattern matches the start of a content morpheme in scope.

    Matching morphemes rather than raw characters keeps 쓰/VV + 라고/EC from
    matching the 쓰라(리) stinging anchor (E33).
    """
    if not available():
        return [name for name, pattern in patterns.items() if re.search(pattern, scope['text'])]
    forms = [t.form for t in tokens(text) if _in(scope, t) and _content(t)]
    return [name for name, pattern in patterns.items() if any(re.match(pattern, f) for f in forms)]


def anchor_negated(text, scope, pattern):
    """Whether an anchor morpheme in scope is negated before the next unit boundary.

    Returns None without Kiwi so the caller keeps its earlier regex rule.
    """
    if not available():
        return None
    toks = tokens(text)
    for i, tok in enumerate(toks):
        if not _in(scope, tok) or not _content(tok) or not re.match(pattern, tok.form):
            continue
        if i and toks[i - 1].tag == 'MAG' and toks[i - 1].form in ('안', '못') and _in(scope, toks[i - 1]):
            return True
        for j in range(i + 1, len(toks)):
            nxt = toks[j]
            if not _in(scope, nxt):
                break
            if (nxt.tag, nxt.form) in NEGATORS or nxt.tag == 'VCN':
                return True
            if nxt.tag == 'EF' or splits_after(toks, j):
                break
    return False


def interrogative(text, scope):
    """Question-like ending (-까) in scope; used only to block the negation rule."""
    if not available():
        return False
    return any(t.tag == 'EF' and t.form.endswith('까') for t in tokens(text) if _in(scope, t))


def noun_candidates(text, event, max_tokens=6):
    """Product-name spans built from noun-like morpheme chunks inside an event.

    Adjacent morphemes without whitespace or connected by symbols (e.g. A-시카 5.5 클렌징폼)
    form candidate spans, while particles/endings without spaces are stripped and
    compound names stay intact.

    Stop nouns, time words, generic categories, and standalone symbols/digits are
    pruned when an entire candidate consists solely of them.
    """
    if not available():
        try:
            from .product_mentions import name_candidates
        except ImportError:
            from product_mentions import name_candidates
        return name_candidates(text, event)
    toks = [t for t in tokens(text) if event['start'] <= t.start < event['end']]
    chunks, cur = [], []
    for tok in toks:
        usable = tok.tag in NOUNISH
        if usable:
            if not cur or cur[-1].end == tok.start:
                cur.append(tok)
            else:
                chunks.append((cur[0].start, cur[-1].end, cur))
                cur = [tok]
        else:
            if cur:
                chunks.append((cur[0].start, cur[-1].end, cur))
                cur = []
    if cur:
        chunks.append((cur[0].start, cur[-1].end, cur))

    spans = {}
    for i in range(len(chunks)):
        for j in range(i, min(i + max_tokens, len(chunks))):
            if all(re.fullmatch(r'[\s\-+./]*', text[chunks[k][1]:chunks[k + 1][0]]) for k in range(i, j)):
                start = chunks[i][0]
                end = chunks[j][1]
                cand_text = text[start:end].strip()
                if len(cand_text) <= 1 or re.fullmatch(r'[\d\s\-+./]+', cand_text):
                    continue
                span_toks = [t for k in range(i, j + 1) for t in chunks[k][2]]
                if all(t.form in STOP_NOUNS or t.form in TIME_WORDS or t.form in GENERIC_CATEGORIES for t in span_toks):
                    continue
                spans[start, end] = {'text': text[start:end], 'start': start, 'end': end,
                                     'candidate_method': 'morpheme'}
    return list(spans.values())


def enclosing(spans, scope):
    """The span (e.g. punctuation clause) that contains scope's start, if any."""
    return next((s for s in spans if s['start'] <= scope['start'] < s['end']), None)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2 or argv[0] != '--dump':
        print('usage: python -m poc.jev.segmenter --dump <dataset.json>', file=sys.stderr)
        return 2
    data = json.loads(open(argv[1], encoding='utf-8').read())
    print(f'segmentation_method={segmentation_method()}')
    for case in data['cases']:
        parts = ' | '.join(u['text'] for u in units(case['input']))
        print(f"{case['id']}: {parts}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
