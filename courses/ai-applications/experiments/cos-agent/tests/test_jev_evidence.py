import json
from poc.jev import test_jev_text as jev


def config():
    return json.loads(jev.CONFIG.read_text(encoding='utf-8'))


def test_offsets_and_no_boundary_crossing():
    text = '얼굴이  건조하지 않았어요. 어제 사용했어'
    spans = jev.candidate_spans(text)
    assert any(x['text'] == '건조하지 않았어요.' for x in spans)
    assert all(text[x['start']:x['end']] == x['text'] for x in spans)
    assert not any('않았어요. 어제' in x['text'] for x in spans)


def test_choice_with_abstention_and_complete_product_events(monkeypatch):
    requests = []
    class Response:
        def raise_for_status(self):
            pass
        def json(self):
            answers = {}
            for qid, q in requests[0]['questions'].items():
                if q['type'] == 'choice':
                    answers[qid] = {'type': 'choice', 'choice': 'none', 'probabilities': {'none': .9}}
                else:
                    answers[qid] = {'type': 'noul', 'noul': .9}
            return {'answers': answers}
    def post(url, **kwargs):
        requests.append(kwargs['json'])
        return Response()
    monkeypatch.setattr(jev.httpx, 'post', post)
    text = '어제 A로션을 발랐어, 오늘 건조해.'
    candidates = [{'field': 'product_used', 'value': 'positive_report'},
                  {'field': 'symptom_onset', 'value': 'today'}]
    result, warning = jev.contextual_evidence(text, 'key', config(), candidates)
    assert warning is None
    assert requests[0]['state'] == text
    assert len(requests[0]['questions']) == 3
    assert result['symptom_onset'] == []
    assert result['product_used'][0]['text'] == '어제 A로션을 발랐어,'
    assert '오늘 시작되었다고 명시했다' in requests[0]['questions']['q2']['instructions']


def test_failure_does_not_return_partial_results(monkeypatch):
    def fail(*args, **kwargs):
        raise jev.httpx.ConnectError('offline')
    monkeypatch.setattr(jev.httpx, 'post', fail)
    result, warning = jev.contextual_evidence('건조해요', 'key', config(),
        [{'field': 'skin_condition.dryness', 'value': 'positive_report'}])
    assert result == {}
    assert '미평가' in warning


def test_low_choice_score_preserved_as_uncertain_candidate(monkeypatch):
    class Response:
        def raise_for_status(self):
            pass
        def json(self):
            return {'answers': {'q0': {'type': 'choice', 'choice': 's0',
                                      'probabilities': {'s0': .42}}}}
    monkeypatch.setattr(jev.httpx, 'post', lambda *a, **kw: Response())
    result, warning = jev.contextual_evidence('건조해요', 'key', config(),
        [{'field': 'skin_condition.dryness', 'value': 'positive_report'}])
    assert warning is None
    assert result['skin_condition.dryness'][0]['score'] == .42
    assert result['skin_condition.dryness'][0]['text'] == '건조해요'
