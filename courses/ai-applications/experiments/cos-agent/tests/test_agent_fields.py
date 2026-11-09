from poc.jev.agent_fields import FIELDS, build_agent_fields
from poc.jev import relations


def test_inventory_never_invents_missing_values_or_authorization():
    result = build_agent_fields({'products': [{'mention_id': 'p0'}],
                                 'symptoms': [{'symptom_id': 's0'}]})
    scopes = [result['request'], result['context'], result['decision'],
              result['products'][0]['fields'], result['symptoms'][0]['fields'],
              result['event_field_requirements']]
    assert sum(map(len, scopes)) == sum(map(len, FIELDS.values()))
    assert all(f['value'] is None and f['evidence_status'] == 'unassessed'
               for scope in scopes for f in scope.values())
    assert result['write_authorized'] is False
    assert result['production_enabled'] is False
    assert result['readiness'] == 'incomplete'


def test_partial_events_are_lossless_and_cannot_mutate_source():
    source = {'products': [], 'symptoms': [],
              'usage_events': [{'usage_date': {'text': '오늘'}, 'usage_state': 'denied'}]}
    result = build_agent_fields(source)
    assert result['usage_event_candidates'] == source['usage_events']
    result['usage_event_candidates'][0]['usage_date']['text'] = '내일'
    assert source['usage_events'][0]['usage_date']['text'] == '오늘'
    assert result['event_extraction_status'] == 'partial_rules_only'


def test_extraction_emits_inventory_without_extra_model_calls(monkeypatch):
    monkeypatch.setattr(relations, 'extract_products', lambda *a, **kw: ([], None))
    def unexpected(*a, **kw):
        raise AssertionError('inventory must not call model')
    monkeypatch.setattr(relations, 'ask', unexpected)
    result = relations.extract_features('안녕하세요', 'synthetic-key')
    assert result['schema_version'] == 'relations-0.5'
    assert result['agent_fields']['supported_symptoms']
    assert result['agent_fields']['unsupported_symptoms_status'] == 'unassessed'
    assert result['agent_fields']['usage_event_candidates'] == []
