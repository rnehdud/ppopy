import json
from copy import deepcopy
from pathlib import Path

import pytest
from poc.jev.mapping_review.review import review, validate_snapshot

EXAMPLES = Path(__file__).parents[1] / 'poc/jev/mapping_review/examples'


@pytest.fixture
def examples():
    return (json.loads((EXAMPLES / 'synthetic_jev.json').read_text()),
            json.loads((EXAMPLES / 'synthetic_skin_state.json').read_text()))


def test_review_positive_negative_and_unrepresentable(examples):
    source, target = examples
    result = review(source, target)
    assert result['contract_errors'] == []
    assert result['findings'][0]['suggested_value'] == 'stinging'
    assert result['findings'][0]['present_in_proposed'] is True
    assert result['findings'][0]['no_direct_skin_state_field'] == ['severity']
    assert result['findings'][1]['issue'] == 'not_a_confirmed_positive_do_not_map_as_present'
    assert not result['authorized_for_storage'] and not result['user_confirmation_verified']


@pytest.mark.parametrize('subject,state', [('other', 'affirmed'), ('unknown', 'affirmed'), ('self', 'negated'), ('self', 'unknown')])
def test_no_positive_mapping_for_other_negative_or_unknown(examples, subject, state):
    source, target = examples
    source['symptoms'][0]['relations'].update(subject={'value': subject}, state={'value': state})
    result = review(source, target)
    assert 'suggested_value' not in result['findings'][0]
    assert 'proposed_detail_has_no_eligible_jev_candidate_review_other_sources' in result['warnings']


def test_empty_symptoms_is_not_absence_and_warning_remains(examples):
    source, target = examples
    source.update(symptoms=[], warnings=['failure'], clarifications=['confirm'])
    warnings = review(source, target)['warnings']
    assert 'no_detected_symptoms_does_not_mean_none' in warnings
    assert 'jev_warnings_present' in warnings and 'jev_clarifications_present' in warnings


def test_contract_rejects_extra_fields_and_invalid_combinations(examples):
    _, target = examples
    assert validate_snapshot({**target, 'source_text': 'example'}) == ['skin_state_keys_mismatch']
    invalid = {**target, 'discomfort_presence': 'none_reported', 'observed_at': '2026-11-08T00:00:00+09:00'}
    assert {'discomfort_presence_mismatch', 'observed_at_invalid_utc'} <= set(validate_snapshot(invalid))
    assert 'persistence_requires_concern' in validate_snapshot({**target, 'persistence': 'persistent'})


def test_unknown_schema_and_malformed_data(examples):
    source, target = examples
    with pytest.raises(ValueError):
        review({**source, 'schema_version': 'future'}, target)
    source['symptoms'] = [None, {'symptom': 'dryness', 'relations': {}}]
    result = review(source, target)
    assert [x['issue'] for x in result['findings']] == ['malformed_symptom', 'missing_symptom_state_or_subject']
    assert 'source_text' not in str(result)


def test_matching_is_candidate_and_unknown_types_not_invented(examples):
    source, target = examples
    source['symptoms'][0]['symptom'] = 'dryness'
    result = review(source, target)
    assert result['findings'][0]['issue'] == 'no_direct_target_review_required'
    assert 'suggested_value' not in result['findings'][0]
    original = deepcopy(source)
    review(source, target)
    assert source == original
