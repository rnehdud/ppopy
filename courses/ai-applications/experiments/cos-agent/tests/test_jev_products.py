from poc.jev import product_mentions as products


def test_particle_alternatives_preserve_original_names_and_offsets():
    text = '어제 A로션과 B 스킨을 발랐어.'
    event = {'text': text, 'start': 0, 'end': len(text)}
    spans = products.name_candidates(text, event)
    assert all(text[x['start']:x['end']] == x['text'] for x in spans)
    assert {'A로션', 'A로션과', 'B 스킨', 'B 스킨을'} <= {s['text'] for s in spans}


def test_extracts_multiple_names_then_stops_at_none(monkeypatch):
    text = 'A로션과 B 스킨을 발랐어.'
    event = {'text': text, 'start': 0, 'end': len(text)}
    targets = iter(['A로션', 'B 스킨', None])
    requests = []
    class Response:
        def __init__(self, payload, target):
            self.payload, self.target = payload, target
        def raise_for_status(self):
            pass
        def json(self):
            qid, question = next(iter(self.payload['questions'].items()))
            choice = 'none' if self.target is None else next(
                k for k, v in question['criteria'].items() if v == self.target)
            return {'answers': {qid: {'type': 'choice', 'choice': choice,
                                      'probabilities': {choice: .8}}}}
    def post(url, **kwargs):
        requests.append(kwargs['json'])
        return Response(kwargs['json'], next(targets))
    monkeypatch.setattr(products.httpx, 'post', post)
    result, warning = products.extract_products(text, 'key', [event])
    assert warning is None
    assert [p['value'] for p in result] == ['A로션', 'B 스킨']
    assert all(p['product_id'] is None and p['match_status'] == 'not_attempted' for p in result)
    assert all(p['context'] == text for p in result)
    assert all(r['state'] == text for r in requests)


def test_no_events_skips_api(monkeypatch):
    def fail(*a, **kw):
        raise AssertionError('unexpected API call')
    monkeypatch.setattr(products.httpx, 'post', fail)
    assert products.extract_products('제품 사용 미확인', 'key', []) == ([], None)
