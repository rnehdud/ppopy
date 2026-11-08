import pytest

from poc.jev import relations as r
from poc.jev.usage_events import event_candidates, finish_events


def mention(text, name, number=0):
    start = text.index(name)
    return dict(text=name, value=name, start=start, end=start + len(name),
                score=.9, mention_id=f'p{number}', context=text, relations={})


def rel(value, status='candidate'):
    return dict(value=value, score=.9, status=status)


def candidates(text, names=('A로션',)):
    return event_candidates(text, [mention(text, n, i) for i, n in enumerate(names)],
                            r.units(text), r.time_spans)[0]


def test_omitted_product_and_clock_offsets():
    text = 'A로션을 아침에 썼고 저녁에는 안 썼어.'
    events = candidates(text)
    assert [e['time_anchor']['text'] for e in events] == ['아침', '저녁']
    assert all(e['product_mention_id'] == 'p0' for e in events)
    for e in events:
        for s in (e['source_scope'], e['time_anchor']):
            assert text[s['start']:s['end']] == s['text']


def test_future_usage_and_unspecified_clock_are_candidates():
    events = candidates('A로션을 아침에 썼고 저녁에는 쓸 예정이야.')
    assert [e['time_anchor']['text'] for e in events] == ['아침', '저녁']
    event = candidates('A로션을 썼어.')[0]
    assert event['time_anchor'] is None


def test_candidate_limit_is_explicit():
    text = 'A로션을 아침에 썼고 저녁에 썼어'
    events, warning = event_candidates(text, [mention(text, 'A로션')], r.units(text), r.time_spans, limit=1)
    assert len(events) == 1
    assert warning


def test_no_product_carry_across_sentence_or_ambiguous_products():
    assert len(candidates('A로션을 아침에 썼어. 저녁에는 안 썼어.')) == 1
    events = candidates('A로션과 B크림을 아침에 썼고 저녁에는 안 썼어.', ('A로션', 'B크림'))
    assert not any(e['time_anchor']['text'] == '저녁' for e in events)


@pytest.mark.parametrize('state,subject,correction,status,eligible', [
    ('affirmed', 'self', 'current', 'candidate', True),
    ('denied', 'self', 'current', 'candidate', False),
    ('planned', 'self', 'current', 'candidate', False),
    ('hypothetical', 'self', 'current', 'candidate', False),
    ('affirmed', 'other', 'current', 'candidate', False),
    ('affirmed', 'self', 'superseded', 'candidate', False),
    ('affirmed', 'self', 'current', 'unassessed', False),
])
def test_event_eligibility_is_per_event(state, subject, correction, status, eligible):
    text = 'A로션 아침에 썼어'
    event = candidates(text)[0]
    event['relations'] = {k: rel(v, status) for k, v in dict(
        product_link='linked', usage_state=state, subject=subject, correction=correction,
        usage_date='not_mentioned', usage_time=event['time_anchor']).items()}
    result = dict(products=[mention(text, 'A로션')], clarifications=[])
    finish_events(result, [event])
    assert event['eligible_for_usage_candidate'] is eligible
    assert event['confirmation_status'] == 'pending'


def test_cancelled_product_cannot_have_active_event():
    text = 'A로션 아침에 썼어'
    event = candidates(text)[0]
    event['relations'] = {k: rel(v) for k, v in dict(product_link='linked',
        usage_state='affirmed', subject='self', correction='current').items()}
    p = mention(text, 'A로션')
    p['relations']['correction'] = rel('superseded')
    finish_events(dict(products=[p], clarifications=[]), [event])
    assert event['relations']['correction']['value'] == 'superseded'
    assert not event['eligible_for_usage_candidate']


def test_pipeline_independently_classifies_mixed_polarities(monkeypatch):
    text = 'A로션을 아침에 썼고 저녁에는 안 썼어.'
    monkeypatch.setattr(r, 'extract_products', lambda *a, **kw: ([mention(text, 'A로션')], None))
    def ask(text, questions, key):
        answers = {}
        for qid, q in questions.items():
            instruction, choices = q['instructions'], q['criteria']
            if '사용 사건' in instruction:
                if '이 사건의 사용 상태는?' in instruction:
                    value = 'denied' if "'text': '저녁'" in instruction else 'affirmed'
                elif 'product' in choices:  # unused, guard against accidental schema expansion
                    raise AssertionError()
                elif 'linked' in choices:
                    value = 'linked'
                elif 'self' in choices:
                    value = 'self'
                elif 'current' in choices:
                    value = 'current'
                elif 'anchor' in choices:
                    value = 'anchor'
                else:
                    value = 'not_mentioned'
            else:
                value = next((v for v in ('affirmed', 'self', 'current', 'not_mentioned') if v in choices), 'unknown')
            answers[qid] = dict(type='choice', choice=value, probabilities={value: .95})
        return answers
    monkeypatch.setattr(r, 'ask', ask)
    result = r.extract_features(text, 'synthetic')
    events = result['usage_events']
    assert [(e['usage_time']['text'], e['relations']['usage_state']['value']) for e in events] == [
        ('아침', 'affirmed'), ('저녁', 'denied')]
    assert [e['eligible_for_usage_candidate'] for e in events] == [True, False]
    assert not result['products'][0]['eligible_for_usage_candidate']
    assert result['agent_fields']['usage_event_candidates'] == events


def test_api_failure_cannot_fall_back_to_affirmed_events(monkeypatch):
    text = 'A로션 아침에 썼고 저녁에는 안 썼어'
    monkeypatch.setattr(r, 'extract_products', lambda *a, **kw: ([mention(text, 'A로션')], None))
    def fail(*a, **kw):
        raise r.httpx.ConnectError('offline')
    monkeypatch.setattr(r, 'ask', fail)
    result = r.extract_features(text, 'synthetic')
    assert len(result['usage_events']) == 2
    assert all(not e['eligible_for_usage_candidate'] for e in result['usage_events'])
    assert all(e['relations']['usage_state']['status'] == 'unassessed' for e in result['usage_events'])
    assert result['warnings']
