from copy import deepcopy

import pytest

from beauty_agent.afa.v67_responses import (MissingRecordedResponse, alias_targets,
    inspect_next_event, require_recorded_response)


def action(kind='ask_user', target='method.tools', focus='all'):
    return {'action': kind, 'target_id': target, 'arguments': {'confirmation_focus': focus}}


def observation(state='unknown', value=None):
    return {'variable_id': 'method.tools', 'state': state, 'value': value,
            'source': 'synthetic_fixture', 'confirmed_by_user': True}


@pytest.mark.parametrize('state', ['unknown', 'declined', 'conflicting'])
def test_recorded_states_and_unsolicited_events_preserved_without_mutation(state):
    turn = {'message': 'record', 'user_events': {'observations': {'method.tools': observation(state)},
                                               'profile': {'confirmed': True}}}
    before = deepcopy(turn)
    r = require_recorded_response(action(), action(), turn, {})
    assert r['response']['state'] == state and r['response']['value'] is None
    assert r['next_record'] == turn == before
    r['next_record']['user_events'].clear()
    assert turn == before


def test_other_allowed_action_cannot_reuse_recorded_response():
    with pytest.raises(MissingRecordedResponse, match='unrecorded_action'):
        require_recorded_response(action(), action(target='method.drying'),
                                  {'user_events': {'observations': {'method.tools': observation()}}}, {})


def test_missing_record_does_not_become_unknown_or_truncation():
    with pytest.raises(MissingRecordedResponse, match='no_next_record'):
        require_recorded_response(action(), action(), None, {})
    with pytest.raises(MissingRecordedResponse, match='no_target_response'):
        require_recorded_response(action(), action(), {'user_events': {}}, {})


def test_confirmation_alias_is_positioned_exactly_and_never_becomes_kb_observation():
    turns = [{'extraction_fixture': {'symptoms': [{'symptom': 'peeling'}, {'symptom': 'burning'}]},
              'candidate_aliases': [{'alias': 'burning_alias', 'expected_symptom': 'burning', 'feature_index': 1}]}]
    aliases = alias_targets(turns)
    event = {'user_events': {'confirmations': [{'candidate_alias': 'burning_alias',
        'value': {'state': 'affirmed', 'subject': 'self', 'observed_at': '2026-11-12T00:15:00Z'}}]}}
    assert aliases == {'burning_alias': 'clarify:turn1:1'}
    assert inspect_next_event(action('confirm_candidate', 'clarify:turn1:0'), event, aliases)['status'] == 'next_record_has_no_target_response'
    a = action('confirm_candidate', 'clarify:turn1:1')
    r = require_recorded_response(a, a, event, aliases)
    assert r['response_kind'] == 'candidate_confirmation' and 'observations' not in r['next_record']['user_events']
    with pytest.raises(MissingRecordedResponse, match='confirmation_focus'):
        require_recorded_response(a, action('confirm_candidate', 'clarify:turn1:1', 'time'), event, aliases)


def test_alias_mismatch_and_duplicate_do_not_fall_back_to_first_candidate():
    t = {'extraction_fixture': {'symptoms': [{'symptom': 'burning'}]},
         'candidate_aliases': [{'alias': 'b', 'expected_symptom': 'peeling', 'feature_index': 0}]}
    with pytest.raises(ValueError, match='does not match'):
        alias_targets([t])
    t['candidate_aliases'][0]['expected_symptom'] = 'burning'
    with pytest.raises(ValueError, match='duplicate'):
        alias_targets([t, t])


def test_conflict_resolution_requires_both_explicit_resolution_and_observation():
    a = action('resolve_conflict')
    t = {'user_events': {'observations': {'method.tools': observation()}}}
    with pytest.raises(MissingRecordedResponse):
        require_recorded_response(a, a, t, {})
    t['user_events']['resolve_conflicts'] = ['method.tools']
    assert require_recorded_response(a, a, t, {})['response_kind'] == 'conflict_resolution'


def test_retrieval_request_and_terminal_label_do_not_fabricate_a_response():
    a = action('retrieve_evidence', 'product.label_instruction')
    with pytest.raises(MissingRecordedResponse, match='product_evidence_adapter_required'):
        require_recorded_response(a, a, {'user_events': {'products': []}}, {})
    assert inspect_next_event(action('hold', 'insufficient_information'), None, {})['status'] == 'terminal_label_needs_separate_judgment'


def test_observation_must_match_target_and_be_confirmed():
    t = {'user_events': {'observations': {'method.tools': observation()}}}
    t['user_events']['observations']['method.tools']['confirmed_by_user'] = False
    with pytest.raises(ValueError, match='explicitly confirmed'):
        require_recorded_response(action(), action(), t, {})
