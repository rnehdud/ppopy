import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from poc.jev.mapping_review.review import review
from poc.jev import relations

EXAMPLES = Path(__file__).parents[1] / 'poc/jev/mapping_review/examples'


def relation(value, status='candidate', score=.9):
    return dict(value=value, status=status, score=score)


def inputs(version='relations-0.5'):
    source = {'schema_version': version, 'symptoms': [
        {'symptom': 'stinging', 'relations': {'state': relation('affirmed'), 'subject': relation('self')}}]}
    target = json.loads((EXAMPLES / 'synthetic_skin_state.json').read_text())
    return source, target


@pytest.mark.parametrize('version', ['relations-0.2', 'relations-0.3', 'relations-0.4', 'relations-0.5'])
def test_explicit_supported_versions_preserve_input_and_candidate_only(version):
    source, target = inputs(version)
    before = deepcopy((source, target))
    result = review(source, target)
    assert result['source_schema_version'] == version
    assert result['findings'][0]['suggested_value'] == 'stinging'
    assert not result['authorized_for_storage']
    assert (source, target) == before


@pytest.mark.parametrize('version', [None, 'relations-0.6', 'relations-0.20', [], {}])
def test_unknown_or_malformed_versions_are_rejected(version):
    source, target = inputs(version)
    with pytest.raises(ValueError):
        review(source, target)


@pytest.mark.parametrize('status,score', [('unassessed', .9), ('uncertain', .9),
                                         ('candidate', None), ('candidate', True),
                                         ('candidate', .2), ('candidate', float('nan'))])
def test_positive_value_with_unusable_assessment_is_not_mapping_candidate(status, score):
    source, target = inputs()
    source['symptoms'][0]['relations']['state'] = relation('affirmed', status, score)
    finding = review(source, target)['findings'][0]
    assert 'suggested_value' not in finding
    assert finding['issue'] == 'unassessed_or_uncertain_symptom_do_not_map'


def test_only_legacy_schema_allows_missing_assessment_metadata():
    source, target = inputs()
    source['symptoms'][0]['relations'] = {'state': {'value': 'affirmed'}, 'subject': {'value': 'self'}}
    assert 'suggested_value' not in review(source, target)['findings'][0]
    source['schema_version'] = 'relations-0.2'
    result = review(source, target)
    assert result['findings'][0]['suggested_value'] == 'stinging'
    assert 'legacy_assessment_metadata_may_be_missing' in result['warnings']


def test_rule_candidate_retains_provenance_and_superseded_is_blocked():
    source, target = inputs()
    rel = source['symptoms'][0]['relations']
    rel['state'] = dict(value='affirmed', status='rule_candidate', score=None, method='synthetic_rule')
    assert review(source, target)['findings'][0]['suggested_value'] == 'stinging'
    rel['correction'] = relation('superseded')
    assert 'suggested_value' not in review(source, target)['findings'][0]


@pytest.mark.parametrize('state,subject,correction,issue', [
    ('affirmed', 'self', 'current', 'actual_use_report_requires_confirmation_and_separate_contract'),
    ('denied', 'self', 'current', 'not_actual_use_do_not_map_as_used'),
    ('planned', 'self', 'current', 'not_actual_use_do_not_map_as_used'),
    ('affirmed', 'other', 'current', 'not_self_usage_do_not_map'),
    ('affirmed', 'self', 'superseded', 'superseded_event_do_not_map'),
])
def test_usage_events_never_become_skin_state(state, subject, correction, issue):
    source, target = inputs()
    source['symptoms'] = []
    source['usage_events'] = [{'source_scope': {'text': 'PRIVATE-SENTINEL'},
        'eligible_for_usage_candidate': True,  # never trust this as write permission
        'relations': {k: relation(v) for k, v in dict(usage_state=state, subject=subject,
            correction=correction, product_link='linked').items()}}]
    result = review(source, target)
    finding = result['usage_event_findings'][0]
    assert finding['issue'] == issue
    assert finding['target'] is None and not finding['authorized_for_storage']
    assert result['findings'] == []
    assert 'PRIVATE-SENTINEL' not in json.dumps(result)


def test_legacy_and_malformed_usage_events_are_not_promoted():
    source, target = inputs()
    source['usage_events'] = [None, {'usage_date': {'text': 'today'}}]
    assert all(x['issue'] == 'legacy_or_malformed_event_requires_review'
               for x in review(source, target)['usage_event_findings'])
    source['usage_events'] = 'invalid'
    assert review(source, target)['usage_event_findings'] == [{'issue': 'malformed_usage_events'}]


def test_current_extractor_api_failure_can_be_reviewed_without_promoting_values(monkeypatch):
    text = 'A로션을 아침에 썼고 저녁에는 안 썼어.'
    monkeypatch.setattr(relations, 'extract_products', lambda *a, **kw: ([dict(
        text='A로션', value='A로션', start=0, end=3, score=.9, context=text)], None))
    def fail(*a, **kw):
        raise relations.httpx.ConnectError('offline')
    monkeypatch.setattr(relations, 'ask', fail)
    extracted = relations.extract_features(text, 'synthetic-key')
    _, target = inputs()
    result = review(extracted, target)
    assert len(result['usage_event_findings']) == 2
    assert all(x['issue'] == 'unassessed_or_uncertain_event_do_not_map'
               for x in result['usage_event_findings'])
    assert 'jev_warnings_present' in result['warnings']


@pytest.mark.parametrize('wrapper', ['features', 'result', None])
def test_cli_accepts_wrappers_and_redacts_raw_content(tmp_path, wrapper):
    source, target = inputs()
    source['source_text'] = 'PRIVATE-SENTINEL'
    source_path, target_path = tmp_path / 'source.json', tmp_path / 'target.json'
    source_path.write_text(json.dumps({wrapper: source} if wrapper else source))
    target_path.write_text(json.dumps({'skin_state': target}))
    run = subprocess.run([sys.executable, '-m', 'poc.jev.mapping_review.review',
                          str(source_path), str(target_path)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert 'PRIVATE-SENTINEL' not in run.stdout
    assert json.loads(run.stdout)['source_schema_version'] == 'relations-0.5'
