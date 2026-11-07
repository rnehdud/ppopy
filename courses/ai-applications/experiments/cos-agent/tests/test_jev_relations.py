from poc.jev import relations as r


def relation(value, status='candidate'):
    return {'value': value, 'status': status, 'score': .9}


def product(text, name, correction='current'):
    start = text.index(name)
    return {'text': name, 'start': start, 'end': start + len(name), 'score': .9,
            'mention_id': name, 'relations': {'usage_state': relation('affirmed'),
            'subject': relation('self'), 'correction': relation(correction)}}


def test_correction_rule_preserves_model_and_excludes_cancelled_product():
    text = 'A로션이 아니라 B크림을 썼어'
    result = {'source_text': text, 'products': [product(text, 'A로션'), product(text, 'B크림', 'superseded')],
              'symptoms': [], 'clarifications': []}
    r.finalize(result)
    a, b = result['products']
    assert not a['eligible_for_usage_candidate']
    assert b['eligible_for_usage_candidate']
    assert b['relations']['correction']['model_prediction']['value'] == 'superseded'
    assert b['relations']['correction']['score'] is None


def test_plans_others_and_uncertainty_are_not_actual_self_usage():
    text = 'A크림'
    for attr, value, status in [('usage_state', 'planned', 'candidate'), ('subject', 'other', 'candidate'),
                                ('usage_state', 'affirmed', 'uncertain')]:
        p = product(text, text)
        p['relations'][attr] = relation(value, status)
        result = {'source_text': text, 'products': [p], 'symptoms': [], 'clarifications': []}
        r.finalize(result)
        assert not p['eligible_for_usage_candidate']


def test_recognition_is_not_automatically_onset():
    text = '아침에 일어나니 피부가 건조했어'
    symptom = {'symptom': 'dryness', 'relations': {
        'onset_time': relation({'text': '아침', 'start': 0, 'end': 2}),
        'recognition_time': relation({'text': '아침', 'start': 0, 'end': 2})}}
    result = {'source_text': text, 'products': [], 'symptoms': [symptom], 'clarifications': []}
    r.finalize(result)
    assert symptom['relations']['onset_time']['value'] == 'unknown'
    assert symptom['relations']['recognition_time']['value']['text'] == '아침'


def test_time_candidates_refer_to_original_offsets():
    text = 'A는 내일 오후 3시, B는 어제 아침'
    for date in (True, False):
        assert all(text[s['start']:s['end']] == s['text'] for s in r.time_spans(text, date))


def test_failure_is_unassessed_and_unmentioned_symptoms_not_invented(monkeypatch):
    monkeypatch.setattr(r, 'extract_products', lambda *a, **kw: ([], None))
    def fail(*a, **kw):
        raise r.httpx.ConnectError('offline')
    monkeypatch.setattr(r.httpx, 'post', fail)
    result = r.extract_features('건조하지만 안 가려워', 'key')
    assert {s['symptom'] for s in result['symptoms']} == {'dryness', 'itching'}
    assert result['warnings']
    assert all(s['relations']['state']['status'] == 'unassessed' for s in result['symptoms'])


def test_each_product_has_independent_time_questions(monkeypatch):
    text = 'A로션은 아침 B크림은 저녁'
    ps = [dict(product(text, name), value=name, context=text) for name in ('A로션', 'B크림')]
    monkeypatch.setattr(r, 'extract_products', lambda *a, **kw: (ps, None))
    requests = []
    class Response:
        def raise_for_status(self):
            pass
        def json(self):
            return {'answers': {qid: {'type': 'choice', 'choice': 'unknown', 'probabilities': {'unknown': .9}}
                                for qid in requests[-1]['questions']}}
    def post(*a, **kw):
        requests.append(kw['json'])
        return Response()
    monkeypatch.setattr(r.httpx, 'post', post)
    result = r.extract_features(text, 'key')
    assert not result['warnings']
    instructions = [q['instructions'] for req in requests for q in req['questions'].values()]
    assert any("제품 'A로션'" in q and '하루 중 시간은' in q for q in instructions)
    assert any("제품 'B크림'" in q and '하루 중 시간은' in q for q in instructions)
