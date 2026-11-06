from poc.jev.semantic_rules import apply_rules, symptom_scopes
from poc.jev.relations import SYMPTOM_ANCHORS, time_spans, finalize
from poc.jev.context_evidence import clause_spans


def rel(value):
    return {'value': value, 'score': .9, 'status': 'candidate'}


def base(text):
    return {'source_text': text, 'products': [], 'symptoms': [], 'clarifications': []}


def apply(data):
    apply_rules(data, SYMPTOM_ANCHORS, clause_spans(data['source_text']), time_spans)
    finalize(data)


def test_same_symptom_has_separate_source_scopes():
    text = '친구는 따갑대. 나는 따갑지 않아.'
    scopes = list(symptom_scopes(text, clause_spans(text), SYMPTOM_ANCHORS))
    assert len(scopes) == 2
    assert scopes[0][1]['end'] <= scopes[1][1]['start']


def test_explicit_negation_subject_and_provenance():
    text = '나는 따갑지 않아.'
    data = base(text)
    record = {'symptom': 'stinging', 'symptom_id': 's0', 'source_scope': clause_spans(text)[0],
              'relations': {'state': rel('affirmed'), 'subject': rel('other')}}
    data['symptoms'] = [record]
    apply(data)
    assert record['relations']['state']['value'] == 'denied'
    assert record['relations']['subject']['value'] == 'self'
    assert record['relations']['state']['model_prediction']['value'] == 'affirmed'
    assert record['relations']['state']['score'] is None


def test_hypothetical_not_forced_to_denied():
    text = '혹시 따갑지 않을까?'
    data = base(text)
    s = {'symptom': 'stinging', 'source_scope': clause_spans(text)[0], 'relations': {'state': rel('hypothetical')}}
    data['symptoms'] = [s]
    apply(data)
    assert s['relations']['state']['value'] == 'hypothetical'


def test_partial_name_and_global_refusal_and_unknown_time():
    text = '어제 일리윤 크림을 발랐어. 몇 시에 발랐는지 기억 안 나. 피부 증상은 말하고 싶지 않아.'
    start = text.index('일리윤')
    data = base(text)
    p = {'text': '일리윤', 'value': '일리윤', 'start': start, 'end': start + 3,
         'score': .9, 'mention_id': 'p0', 'relations': {'usage_state': rel('affirmed'),
         'subject': rel('self'), 'correction': rel('current')}}
    data['products'] = [p]
    apply(data)
    assert p['value'] == '일리윤 크림'
    assert text[p['start']:p['end']] == p['text']
    assert not p['eligible_for_usage_candidate']
    assert p['relations']['usage_time']['value'] == 'unknown'
    assert data['intake_status']['symptoms']['value'] == 'declined'


def test_explicit_repeated_pairs_are_separate_events():
    text = 'A로션을 어제 아침이랑 오늘 저녁에 썼어.'
    data = base(text)
    p = {'text': 'A로션', 'value': 'A로션', 'start': 0, 'end': 3, 'score': .9, 'mention_id': 'p0',
         'relations': {'usage_state': rel('affirmed'), 'subject': rel('self'), 'correction': rel('current')}}
    data['products'] = [p]
    apply(data)
    assert [(e['usage_date']['text'], e['usage_time']['text']) for e in data['usage_events']] == [('어제', '아침'), ('오늘', '저녁')]
    assert p['relations']['usage_date']['value'] == 'multiple_events'


def test_unknown_onset_propagates_but_usage_time_is_not_recognition():
    text = '오늘 저녁 피부가 건조했어. 언제부터 그랬는지는 모르겠어.'
    data = base(text)
    s = {'symptom': 'dryness', 'source_scope': clause_spans(text)[0], 'relations': {
        'recognition_time': rel({'text': '저녁', 'start': 3, 'end': 5})}}
    data['symptoms'] = [s]
    apply(data)
    assert s['relations']['recognition_time']['value'] == 'unknown'
    assert s['relations']['onset_date']['value'] == 'unknown'
    assert s['relations']['onset_time']['value'] == 'unknown'


def test_symptom_onset_unknown_does_not_replace_known_product_usage_time():
    text = 'A로션을 저녁에 썼어. 건조한데 언제부터인지 모르겠어.'
    data = base(text)
    data['products'] = [{'text': 'A로션', 'value': 'A로션', 'start': 0, 'end': 3, 'score': .9,
        'mention_id': 'p0', 'relations': {'usage_state': rel('affirmed'), 'subject': rel('self'),
        'correction': rel('current'), 'usage_time': rel({'text': '저녁', 'start': 5, 'end': 7})}}]
    apply(data)
    assert data['products'][0]['relations']['usage_time']['value']['text'] == '저녁'
