from copy import deepcopy
import json

import pytest

from beauty_agent.afa.v67_fixtures import (BUNDLE, V67, FixtureContractError, ResponseBook,
    artifacts, compile_book, derive_candidate_label, derive_fixture, fingerprint, verify)
from data.action_policy.v67.dataset_cli import read_rows


def parents_and_design():
    design = json.loads((BUNDLE/'design.json').read_text(encoding='utf-8'))
    parents = {s['scenario_id']: s for s in read_rows(V67/'canonical-candidates-v67.jsonl')}
    return parents, design


def one_fixture():
    parents, design = parents_and_design()
    f = design['fixtures'][0]
    return derive_fixture(parents[f['parent_scenario_id']], 'train', f['author_defined_additions'])


def test_actual_parent_unknown_is_hidden_then_delivered_unchanged_and_not_reasked():
    f = one_fixture();rows, _ = compile_book([f]);book = ResponseBook([f], rows)
    start = book.initial_public(f['fixture_id'])
    assert set(start['observations']) == {'method.body_site'}
    assert not any(k in start for k in ['fixture_id', 'lineage', 'environment_only'])
    after = book.answer(f['fixture_id'], start, 'method.drying')
    assert after['observations']['method.drying']['state'] == 'unknown'
    assert after['observations']['method.drying']['value'] is None
    assert set(start['observations']) == {'method.body_site'}
    with pytest.raises(FixtureContractError, match='undefined response'):
        book.answer(f['fixture_id'], after, 'method.drying')


def test_missing_response_is_detected_before_rollout_even_if_other_paths_exist():
    f = one_fixture();rows, _ = compile_book([f])
    with pytest.raises(FixtureContractError, match='incomplete'):
        ResponseBook([f], rows[:-1])
    f['environment_only']['response_table'].pop('method.friction')
    with pytest.raises(FixtureContractError, match='domain incomplete'):
        compile_book([f])


def test_key_includes_ordered_history_action_target_focus_and_fixture_identity():
    f = one_fixture();rows, _ = compile_book([f]);book = ResponseBook([f], rows);id_ = f['fixture_id']
    initial = book.initial_public(id_)
    a = book.answer(id_, book.answer(id_, initial, 'method.tools'), 'method.friction')
    b = book.answer(id_, book.answer(id_, initial, 'method.friction'), 'method.tools')
    assert a['observations'] == b['observations'] and fingerprint(a) != fingerprint(b)
    for kwargs in [{'focus': 'time'}, {'action': 'confirm_candidate'}]:
        with pytest.raises(FixtureContractError, match='undefined response'):
            book.answer(id_, initial, 'method.tools', **kwargs)
    with pytest.raises(FixtureContractError, match='undefined response'):
        book.answer('other-world', initial, 'method.tools')


def test_temporal_change_and_explicit_resolution_cannot_be_flattened():
    parents, design = parents_and_design();f = design['fixtures'][0];p = deepcopy(parents[f['parent_scenario_id']])
    changed = deepcopy(p['turns'][1]);changed['user_events']['observations']['method.drying'].update(state='known',value='pat_gently')
    p['turns'].append(changed)
    with pytest.raises(FixtureContractError, match='temporal correction'):
        derive_fixture(p, 'train', f['author_defined_additions'])
    p['turns'].pop();p['turns'][1]['user_events']['resolve_conflicts'] = ['method.drying']
    with pytest.raises(FixtureContractError, match='adapter required'):
        derive_fixture(p, 'train', f['author_defined_additions'])


def test_test_split_and_overwriting_unknown_are_rejected():
    parents, design = parents_and_design();f = design['fixtures'][0];p = parents[f['parent_scenario_id']]
    with pytest.raises(FixtureContractError, match='train lineage'):
        derive_fixture(p, 'test_internal', f['author_defined_additions'])
    with pytest.raises(FixtureContractError, match='never overwrite unknown'):
        derive_fixture(p, 'train', {**f['author_defined_additions'], 'method.drying': 'pat_gently'})


def test_future_initial_visibility_and_mutated_response_are_rejected():
    f = one_fixture();rows, _ = compile_book([f]);altered = deepcopy(rows);altered[0]['response']['value'] = 'fabricated'
    with pytest.raises(FixtureContractError, match='altered'):
        ResponseBook([f], altered)
    f['initial_public']['observations']['method.drying'] = f['environment_only']['response_table']['method.drying']
    with pytest.raises(FixtureContractError, match='future responses'):
        compile_book([f])


def test_derived_label_only_changes_selected_first_turn_and_synchronizes_rationale():
    train = read_rows(V67/'v67-sft-train.jsonl');r = next(r for r in train if r['id']=='luna-v3-train-919-t01')
    original = deepcopy(r)
    review = json.loads((BUNDLE.parent/'v67-review-v1/review-decisions.json').read_text(encoding='utf-8'))['candidate_priority']
    derived = derive_candidate_label(r,review)
    assert r == original and derived['input'] == r['input']
    assert derived['output']['target_id'] == 'clarify:turn1:1'
    assert derived['output']['evidence_refs'] == ['candidate:clarify:turn1:1']
    assert 'burning' in derived['output']['reason_summary'] and 'turn1:0' not in derived['output']['reason_summary']
    assert derived['review']['approved_reference'] is False and derived['review']['training_ready'] is False
    second = next(r for r in train if r['id']=='luna-v3-train-919-t02')
    with pytest.raises(FixtureContractError, match='parent mismatch'):
        derive_candidate_label(second, review)
    r['output']['reason_summary'] = 'changed'
    with pytest.raises(FixtureContractError, match='source drift'):
        derive_candidate_label(r, review)


def test_bundle_reproduces_and_keeps_provenance_separate_from_public_inputs():
    _, manifest = artifacts()
    assert verify() == manifest
    fixtures = read_rows(BUNDLE/'fixtures.jsonl')
    assert len(fixtures) == 4
    for f in fixtures:
        assert f['lineage']['effective_split'] == 'train'
        assert {o['kind'] for o in f['environment_only']['response_provenance'].values()} == {
            'recorded_value_retimed_by_fixture_assumption', 'author_defined_counterfactual'}
    refusal = next(f for f in fixtures if f['lineage']['scenario_id'].endswith('849'))
    assert refusal['environment_only']['response_table']['method.drying']['state'] == 'declined'
