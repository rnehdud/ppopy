from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from poc.jev.mapping_review import backend
from poc.jev import test_jev_text as cli


def inputs():
    text = 'synthetic input'
    features = {'schema_version': 'relations-0.5', 'source_text': text,
                'text_revision': hashlib.sha256(text.encode()).hexdigest(), 'symptoms': [], 'usage_events': [], 'warnings': []}
    path = Path(__file__).parents[1] / 'poc/jev/mapping_review/examples/synthetic_skin_state.json'
    return features, json.loads(path.read_text())


def confirmed(features, state):
    pending = backend.prepare_handoff(features, state)
    return {'confirmed': True, **pending['confirmation_binding']}


def test_no_default_state_or_timestamp_and_no_raw_debug_content():
    features, _ = inputs()
    result = backend.prepare_handoff(features)
    assert result['status'] == 'needs_information'
    assert result['payload'] is None and result['candidate_skin_state'] == {}
    assert 'observed_at' in [q['field'] for q in result['questions']]
    assert 'synthetic input' not in json.dumps(result)
    assert not result['authorized_for_storage'] and not result['backend_route_enabled']


def test_normalization_exact_keys_confirmation_and_no_mutation():
    features, state = inputs()
    state['observed_at'] = '2026-11-08T00:00:00+00:00'
    before = deepcopy((features, state))
    pending = backend.prepare_handoff(features, state)
    assert pending['status'] == 'needs_confirmation' and pending['payload'] is None
    result = backend.prepare_handoff(features, state, confirmed(features, state))
    assert result['status'] == 'prepared_disabled'
    assert set(result['payload']) == backend.TOP
    assert result['payload']['observed_at'] == '2026-11-08T00:00:00Z'
    assert (features, state) == before
    assert not result['production_enabled'] and not result['authorized_for_storage']


@pytest.mark.parametrize('change', ['state', 'source', 'binding', 'boolean'])
def test_stale_confirmation_cannot_release_payload(change):
    features, state = inputs()
    confirmation = confirmed(features, state)
    if change == 'state':
        state['sensitivity_history'] = 'user_refused'
    elif change == 'source':
        features['source_text'] = 'changed synthetic input'
        features['text_revision'] = hashlib.sha256(features['source_text'].encode()).hexdigest()
    elif change == 'binding':
        confirmation['payload_sha256'] = '0' * 64
    else:
        confirmation['confirmed'] = 'true'
    result = backend.prepare_handoff(features, state, confirmation)
    assert result['payload'] is None
    assert result['status'] in ('blocked', 'needs_confirmation')


@pytest.mark.parametrize('field,value', [
    ('kind', 'usage_event'), ('version', 'future'), ('observed_at', '2026-11-08T09:00:00+09:00'),
    ('observed_at', '2026-11-08'), ('concern_presence', None),
    ('discomfort_types', ['stinging', 'stinging']), ('discomfort_presence', 'none_reported'),
    ('recent_change', 'better'), ('source_text', 'must not enter payload'),
])
def test_invalid_backend_fields_never_produce_payload(field, value):
    features, state = inputs()
    state[field] = value
    result = backend.prepare_handoff(features, state, {'confirmed': True})
    assert result['status'] == 'invalid_input'
    assert result['errors'] and result['payload'] is None


def test_missing_unknown_and_refused_have_distinct_contract_meanings():
    features, state = inputs()
    del state['persistence']
    assert backend.prepare_handoff(features, state)['status'] == 'invalid_input'
    for value in ('unknown', 'not_asked', 'user_refused'):
        state['persistence'] = value
        result = backend.prepare_handoff(features, state, confirmed(features, state))
        assert result['payload']['persistence'] == value


def test_source_revision_and_extraction_failures_block_handoff():
    features, state = inputs()
    features['text_revision'] = '0' * 64
    assert backend.prepare_handoff(features, state)['status'] == 'blocked'
    features, state = inputs()
    features['warnings'] = ['synthetic failure']
    assert backend.prepare_handoff(features, state)['payload'] is None


def test_size_limit_and_exact_payload_digest(monkeypatch):
    _, state = inputs()
    normalized, errors = backend.normalize_payload(state)
    assert not errors
    assert backend.payload_digest(normalized) == backend.payload_digest(dict(reversed(list(normalized.items()))))
    monkeypatch.setattr(backend, 'MAX_PLAINTEXT_BYTES', 1)
    assert backend.normalize_payload(state) == (None, ['payload_too_large'])


def test_contract_change_invalidates_ui_binding(monkeypatch):
    features, state = inputs()
    confirmation = confirmed(features, state)
    changed = deepcopy(backend.CONTRACT)
    changed['snapshot'] = 'changed synthetic snapshot'
    monkeypatch.setattr(backend, 'CONTRACT', changed)
    assert backend.prepare_handoff(features, state, confirmation)['payload'] is None
    changed['version'] = 'future'
    assert backend.normalize_payload(state) == (None, ['unsupported_backend_contract'])


def test_app_mode_excludes_internal_fields_and_preserves_cli_debug_mode(monkeypatch, capsys):
    features, _ = inputs()
    features['internal_debug'] = 'PRIVATE-SENTINEL'
    def unused(*a, **kw):
        raise AssertionError('app path must not call the debug classifier')
    monkeypatch.setattr(cli, 'classify', unused)
    monkeypatch.setattr(cli, 'extract_features', lambda *a, **kw: deepcopy(features))
    assert cli.run_input('synthetic', 'synthetic-key', {}, app_json=True, legacy=True) == 0
    app = json.loads(capsys.readouterr().out)
    assert 'PRIVATE-SENTINEL' not in json.dumps(app)
    assert 'classification' not in app and 'symptoms' not in app
    monkeypatch.setattr(cli, 'classify', lambda *a, **kw: {'answers': {}})
    assert cli.run_input('synthetic', 'synthetic-key', {}, as_json=True, legacy=True) == 0
    assert json.loads(capsys.readouterr().out)['internal_debug'] == 'PRIVATE-SENTINEL'
