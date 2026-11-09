import httpx
import pytest

from poc.jev import product_queries as p
from poc.jev import skin_state as s
from poc.jev.mapping_review.backend import prepare_handoff


def envelope():
    return {'auto_confirmed': False, 'candidates': [dict(product_id='synthetic-1', brand='Synthetic',
        name='A cleanser', option='100ml', ingredient_evidence_status='review_required')]}


def setup(monkeypatch):
    text = 'A클렌저로 세안을 하고 B로션을 발랐어.'
    split = text.index('B로션')
    chunks = [{'chunk_id': 'c0', 'start': 0, 'end': split, 'text': text[:split]},
              {'chunk_id': 'c1', 'start': split, 'end': len(text), 'text': text[split:]}]
    def spans(text, chunk):
        name = 'A클렌저' if chunk['chunk_id'] == 'c0' else 'B로션'
        start = text.index(name)
        return [{'text': name, 'start': start, 'end': start + len(name)}]
    monkeypatch.setattr(p, 'noun_candidates', spans)
    def ask(text, questions, key):
        assert set(questions) == {'c0.product_name', 'c1.product_name'}
        return {qid: {'type': 'choice', 'choice': 'n0', 'probabilities': {'n0': .95}} for qid in questions}
    return text, chunks, ask


def test_product_names_map_to_real_search_contract_not_skin_state(monkeypatch):
    text, chunks, ask = setup(monkeypatch)
    rows, errors = p.extract_product_queries(text, chunks, 'synthetic', ask)
    assert not errors
    assert [r['product_name'] for r in rows] == ['A클렌저', 'B로션']
    for row in rows:
        assert row['search_request'] == {'method': 'GET', 'path': '/api/v1/products', 'query': {'query': row['product_name']}}
        assert row['lookup_status'] == 'fallback_pending'
        assert row['product_id'] is None and row['product_version'] is None


def test_default_fallback_never_calls_network_or_claims_no_match(monkeypatch):
    text, chunks, ask = setup(monkeypatch)
    def forbidden(*a, **kw):
        raise AssertionError('fallback called network')
    monkeypatch.setattr(p.httpx, 'get', forbidden)
    rows, errors = p.extract_product_queries(text, chunks, 'synthetic', ask)
    assert not errors
    assert all(r['lookup_status'] == 'fallback_pending' and r['candidates'] == [] for r in rows)


def test_current_engine_and_app_handoff_keep_products_outside_skin_state(monkeypatch):
    text, chunks, _ = setup(monkeypatch)
    monkeypatch.setattr(s, 'chunk_text', lambda _: chunks)
    def ask(text, questions, key):
        return {qid: {'type': 'choice', 'choice': 'n0' if qid.endswith('.product_name') else 'omit',
                      'probabilities': {'n0' if qid.endswith('.product_name') else 'omit': .95}}
                for qid in questions}
    monkeypatch.setattr(s, 'ask', ask)
    extraction = s.extract_skin_state(text, 'synthetic')
    handoff = prepare_handoff(extraction)
    assert handoff['candidate_skin_state'] == {} and handoff['payload'] is None
    assert [q['product_name'] for q in handoff['product_queries']] == ['A클렌저', 'B로션']
    assert all(q['lookup_status'] == 'fallback_pending' and q['product_id'] is None for q in handoff['product_queries'])
    assert all('source' not in q and 'score' not in q for q in handoff['product_queries'])
    assert not handoff['authorized_for_storage']


def test_unique_search_candidate_is_never_auto_confirmed(monkeypatch):
    text, chunks, ask = setup(monkeypatch)
    called = []
    def lookup(name):
        called.append(name)
        return envelope()
    rows, errors = p.extract_product_queries(text, chunks, 'synthetic', ask, lookup)
    assert called == ['A클렌저', 'B로션'] and not errors
    assert all(r['lookup_status'] == 'candidates_found' for r in rows)
    assert all(r['product_id'] is None and r['product_version'] is None and r['auto_confirmed'] is False for r in rows)


def test_low_confidence_name_does_not_trigger_lookup(monkeypatch):
    text, chunks, _ = setup(monkeypatch)
    def ask(text, questions, key):
        return {qid: {'type': 'choice', 'choice': 'n0', 'probabilities': {'n0': .3}} for qid in questions}
    def lookup(name):
        raise AssertionError('uncertain name searched')
    rows, _ = p.extract_product_queries(text, chunks, 'synthetic', ask, lookup)
    assert all(r['status'] == 'withheld' and r['lookup_status'] == 'not_attempted' for r in rows)
    assert all(r['search_request'] is None for r in rows)


@pytest.mark.parametrize('response', [None, {'auto_confirmed': True, 'candidates': []},
    {'auto_confirmed': False, 'candidates': [{'product_id': 'invented'}]}])
def test_invalid_catalog_response_is_rejected(response):
    with pytest.raises(ValueError):
        p.validate_search_response(response)


def test_product_search_failure_retains_source_without_inventing_identity(monkeypatch):
    text, chunks, ask = setup(monkeypatch)
    def lookup(name):
        raise httpx.ConnectError('offline')
    rows, errors = p.extract_product_queries(text, chunks, 'synthetic', ask, lookup)
    assert 'product_search_failed' in errors
    assert all(r['lookup_status'] == 'failed' and r['product_id'] is None for r in rows)


def test_read_only_client_uses_exact_backend_path_and_query():
    def handle(request):
        assert request.method == 'GET' and request.url.path == '/api/v1/products'
        assert request.url.params['query'] == 'A클렌저'
        return httpx.Response(200, json=envelope())
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        search = p.ProductSearchClient('https://synthetic.invalid', client)
        assert p.validate_search_response(search('A클렌저'))[0]['product_id'] == 'synthetic-1'


@pytest.mark.parametrize('url', ['http://example.com', 'https://user:secret@example.com',
    'https://example.com/path', 'https://example.com?query=x'])
def test_endpoint_is_explicit_configuration_not_model_output(url):
    with pytest.raises(ValueError):
        p.ProductSearchClient(url)


def test_adjacent_fragment_pruned_in_multi_round(monkeypatch):
    text = 'A-시카 5.5 클렌징폼 쓰고 나서 B로션을 발랐어.'
    chunks = [{'chunk_id': 'c0', 'start': 0, 'end': len(text), 'text': text}]
    # Candidate spans including adjacent single char 'A', compound, and second product
    sp1 = 'A'
    sp2 = '시카 5.5 클렌징폼'
    sp3 = 'B로션'
    spans = [
        {'text': sp1, 'start': text.index(sp1), 'end': text.index(sp1) + len(sp1)},
        {'text': sp2, 'start': text.index(sp2), 'end': text.index(sp2) + len(sp2)},
        {'text': sp3, 'start': text.index(sp3), 'end': text.index(sp3) + len(sp3)},
    ]
    monkeypatch.setattr(p, 'noun_candidates', lambda t, c: spans)
    rounds_called = []
    def ask(t, questions, key):
        rounds_called.append(questions)
        qid = 'c0.product_name'
        criteria = questions[qid]['criteria']
        # Round 1: chooses '시카 5.5 클렌징폼'
        if len(rounds_called) == 1:
            choice = [k for k, v in criteria.items() if v == sp2][0]
        elif len(rounds_called) == 2:
            # Round 2: 'A' should be pruned from criteria! Only 'B로션' and 'omit'
            assert sp1 not in criteria.values()
            assert sp3 in criteria.values()
            choice = [k for k, v in criteria.items() if v == sp3][0]
        else:
            choice = 'omit'
        return {qid: {'type': 'choice', 'choice': choice, 'probabilities': {choice: .95}}}

    rows, errors = p.extract_product_queries(text, chunks, 'synthetic', ask)
    assert not errors
    assert [r['product_name'] for r in rows] == [sp2, sp3]
