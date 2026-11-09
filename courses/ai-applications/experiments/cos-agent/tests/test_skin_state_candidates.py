from copy import deepcopy
import json

import pytest

from poc.jev.mapping_review.candidates import map_candidates
from poc.jev import relations as r
from poc.jev import test_jev_text as cli


def symptom(name='stinging', state='affirmed', subject='self', status='candidate'):
    return {'symptom': name, 'relations': {
        'state': {'value': state, 'status': status, 'score': .9},
        'subject': {'value': subject, 'status': status, 'score': .9}}}


def features(*symptoms):
    return {'schema_version': 'relations-0.5', 'text_revision': 'synthetic-revision',
            'symptoms': list(symptoms), 'usage_events': [], 'warnings': []}


def test_partial_patch_deduplicates_and_preserves_source_references():
    source = features(symptom(), symptom(), symptom('itching'), symptom('redness'))
    original = deepcopy(source)
    result = map_candidates(source)
    assert result['skin_state_patch'] == {'discomfort_presence': 'reported',
        'discomfort_types': ['stinging', 'itching', 'redness_tendency']}
    assert [c['symptom_index'] for c in result['candidates']] == [0, 1, 2, 3]
    assert result['source_text_revision'] == 'synthetic-revision'
    assert set(result['missing_fields']) == {'kind', 'observed_at', 'concern_presence',
                                            'persistence', 'recent_change', 'sensitivity_history'}
    assert source == original
    assert not result['complete_payload'] and not result['authorized_for_storage']


@pytest.mark.parametrize('record', [symptom(state='denied'), symptom(state='hypothetical'),
    symptom(subject='other'), symptom(status='uncertain'), symptom(status='unassessed'),
    symptom('dryness'), symptom('breakout')])
def test_no_patch_does_not_become_no_symptoms(record):
    result = map_candidates(features(record))
    assert result['skin_state_patch'] == {}
    assert 'discomfort_presence' in result['missing_fields']
    assert not result['candidates']


def test_empty_input_cannot_invent_observation_time_kind_or_negative():
    result = map_candidates(features())
    assert result['skin_state_patch'] == {}
    assert 'observed_at' in result['missing_fields'] and 'kind' in result['missing_fields']


@pytest.mark.parametrize('blocker', ['warnings', 'declined', 'legacy'])
def test_errors_refusal_and_old_metadata_require_review(blocker):
    source = features(symptom())
    if blocker == 'warnings':
        source['warnings'] = ['synthetic-error']
    elif blocker == 'declined':
        source['intake_status'] = {'symptoms': {'value': 'declined'}}
    else:
        source['schema_version'] = 'relations-0.2'
    result = map_candidates(source)
    assert result['blockers'] and not result['skin_state_patch']


def test_opposite_reports_are_not_collapsed_into_current_state():
    result = map_candidates(features(symptom(), symptom(state='denied'), symptom('itching')))
    assert result['skin_state_patch']['discomfort_types'] == ['itching']
    assert result['findings'][0]['mapping_issue'] == 'opposed_reports_require_time_and_state_confirmation'


def test_source_text_and_usage_events_cannot_create_skin_state():
    source = features()
    source.update(source_text='PRIVATE-SENTINEL', usage_events=[{'usage_state': 'affirmed'}])
    result = map_candidates(source)
    assert result['skin_state_patch'] == {}
    assert len(result['usage_event_findings']) == 1
    assert 'PRIVATE-SENTINEL' not in json.dumps(result)


def test_live_extractor_path_emits_patch_without_extra_model_calls(monkeypatch):
    monkeypatch.setattr(r, 'extract_products', lambda *a, **kw: ([], None))
    count = []
    def ask(text, questions, key):
        count.append(len(questions))
        answers = {}
        for key, question in questions.items():
            choices = question['criteria']
            value = next(v for v in ('affirmed', 'self', 'not_mentioned', 'none') if v in choices)
            answers[key] = {'type': 'choice', 'choice': value, 'probabilities': {value: .95}}
        return answers
    monkeypatch.setattr(r, 'ask', ask)
    result = r.extract_features('나는 따가워.', 'synthetic')
    assert count == [7]  # original symptom questions only; mapping is offline
    assert result['skin_state_mapping']['skin_state_patch']['discomfort_types'] == ['stinging']


def test_existing_cli_shows_mapping_in_json_and_terminal(monkeypatch, capsys):
    extracted = features(symptom())
    extracted['skin_state_mapping'] = map_candidates(extracted)
    monkeypatch.setattr(cli, 'classify', lambda *a, **kw: {'answers': {}})
    monkeypatch.setattr(cli, 'extract_features', lambda *a, **kw: deepcopy(extracted))
    monkeypatch.setattr(cli, 'print_features', lambda *a: None)
    assert cli.run_input('synthetic', 'synthetic', {}, as_json=True, legacy=True) == 0
    assert json.loads(capsys.readouterr().out)['skin_state_mapping']['skin_state_patch']
    assert cli.run_input('synthetic', 'synthetic', {}, legacy=True) == 0
    output = capsys.readouterr().out
    assert 'SKIN STATE MAPPING' in output and 'authorized_for_storage=false' in output
