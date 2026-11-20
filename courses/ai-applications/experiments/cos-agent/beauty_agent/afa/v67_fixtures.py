"""Bounded train-derived response fixtures, not a Gym runtime or new gold labels."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from beauty_agent.actions import ActionContext, ActionProposal
from beauty_agent.action_runtime import validate_action
from beauty_agent.contracts import ObservationSlot
from .eda import ROOT, BASE, V67, fingerprint
from data.action_policy.v67.dataset_cli import SPLIT_FILES, read_rows

BUNDLE = BASE/'data/afa/v67-fixtures-v1'
SLOTS = ('method.tools', 'method.friction', 'method.drying')


class FixtureContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise FixtureContractError(message)


def slot(variable, state, value):
    require(state in {'known', 'unknown', 'declined'}, 'unsupported bounded response state')
    require(state == 'known' or value is None, 'nonanswer must retain null')
    return ObservationSlot(variable_id=variable, state=state, value=deepcopy(value),
                           source='synthetic_fixture', confirmed_by_user=True).model_dump()


def derive_fixture(parent, effective_split, additions):
    require(effective_split == 'train', 'train lineage required')
    require(parent.get('synthetic') is True and parent['card_ids'] == ['B-C02'], 'bounded synthetic C02 parent required')
    turns = parent['turns']
    initial = turns[0].get('user_events', {}).get('observations', {})
    require(set(initial) == {'method.body_site'} and initial['method.body_site']['state'] == 'known'
            and initial['method.body_site']['value'] == 'face', 'explicit initial face observation required')
    seen, origins = {}, {}
    for index, turn in enumerate(turns):
        events = turn.get('user_events', {})
        require(not any(v for k, v in events.items() if k != 'observations'), 'temporal/product/candidate adapter required')
        require(not turn.get('candidate_aliases') and not turn.get('extraction_fixture', {}).get('symptoms'),
                'candidate adapter required')
        for key, raw in events.get('observations', {}).items():
            require(key in set(SLOTS) | {'method.body_site'}, 'slot outside bounded scope')
            parsed = ObservationSlot.model_validate(raw)
            require(parsed.variable_id == key and parsed.confirmed_by_user, 'unconfirmed or misaddressed source observation')
            require(parsed.state in {'known', 'unknown', 'declined'}, 'conflict/temporal adapter required')
            value = (parsed.state, parsed.value)
            if key in seen:
                require(seen[key] == value, 'temporal correction must not be flattened')
            seen[key] = deepcopy(value)
            origins.setdefault(key, {'kind': 'recorded_value_retimed_by_fixture_assumption',
                'source_turn_index': index, 'source_observation': deepcopy(raw)})
    require(set(additions) == set(SLOTS) - seen.keys(), 'additions must fill exactly unrecorded slots; never overwrite unknown')
    table = {}
    for key in SLOTS:
        if key in seen:
            state, value = seen[key]
        else:
            state, value = 'known', additions[key]
            origins[key] = {'kind': 'author_defined_counterfactual', 'not_inferred_from_parent': True}
        table[key] = slot(key, state, value)
    return {'fixture_id': 'e22:'+parent['scenario_id'], 'version': 'v67-bounded-responses-0.1',
        'split': 'train', 'mode': 'development_preview', 'production_enabled': False,
        'human_review': 'unreviewed', 'approved_reference': False, 'training_ready': False,
        'lineage': {**{k: parent.get(k) for k in ['scenario_id', 'group_id', 'scenario_family_id', 'product_family_id']},
                    'parent_sha256': fingerprint(parent), 'effective_split': effective_split},
        'initial_public': {'message': turns[0]['message'],
            'observations': {'method.body_site': slot('method.body_site', 'known', 'face')}, 'history': []},
        'environment_only': {'stationarity_assumed': True, 'question_slots': list(SLOTS),
                             'response_table': table, 'response_provenance': {k: origins[k] for k in SLOTS}},
        'scope': 'structured acquisition only; no replay of future prose, runtime permission, terminal label or reward'}


def response_key(fixture_id, public, target, action='ask_user', focus='all'):
    return fingerprint([fixture_id, fingerprint(public), action, target, focus])


def following(public, response, target):
    result = deepcopy(public)
    result['observations'][target] = deepcopy(response)
    result['history'].append({'action': 'ask_user', 'target_id': target, 'confirmation_focus': 'all',
                              'response': deepcopy(response)})
    return result


def compile_book(fixtures):
    rows, nodes, leaves = [], 0, 0
    require(len({f['fixture_id'] for f in fixtures}) == len(fixtures), 'duplicate fixture id')
    for fixture in fixtures:
        require(fixture['split'] == 'train' and fixture['production_enabled'] is False
                and fixture['training_ready'] is False and fixture['approved_reference'] is False,
                'inactive train fixture required')
        public_initial = fixture['initial_public']
        require(set(public_initial) == {'message', 'observations', 'history'} and public_initial['history'] == []
                and public_initial['observations'] == {'method.body_site': slot('method.body_site', 'known', 'face')},
                'initial public state must not contain future responses or hidden metadata')
        hidden = fixture['environment_only']
        require(hidden['stationarity_assumed'] is True and set(hidden['question_slots']) == set(SLOTS)
                and set(hidden['response_table']) == set(SLOTS), 'response domain incomplete')
        queue = [deepcopy(fixture['initial_public'])]
        while queue:
            public = queue.pop(0)
            nodes += 1
            pending = sorted(set(SLOTS) - public['observations'].keys())
            if not pending:
                leaves += 1
            for target in pending:
                raw = hidden['response_table'][target]
                checked = slot(target, raw['state'], raw['value'])
                require(raw == checked, 'invalid response identity/state/source')
                after = following(public, raw, target)
                rows.append({'key': response_key(fixture['fixture_id'], public, target),
                    'fixture_id': fixture['fixture_id'], 'public_history_sha256': fingerprint(public),
                    'action': 'ask_user', 'target_id': target, 'confirmation_focus': 'all',
                    'response': deepcopy(raw), 'next_public_sha256': fingerprint(after)})
                queue.append(after)
    rows.sort(key=lambda r: r['key'])
    require(len({r['key'] for r in rows}) == len(rows), 'duplicate response key')
    return rows, {'public_history_nodes': nodes, 'response_edges': len(rows), 'complete_question_orders': leaves}


class ResponseBook:
    """Fail on absent paths before dispatch; never manufacture an unknown response."""
    def __init__(self, fixtures, rows):
        expected, self.counts = compile_book(fixtures)
        require(sorted(rows, key=lambda r: r['key']) == expected, 'response book incomplete or altered')
        self._fixtures = {f['fixture_id']: deepcopy(f) for f in fixtures}
        self._rows = {r['key']: deepcopy(r) for r in rows}

    def initial_public(self, fixture_id):
        return deepcopy(self._fixtures[fixture_id]['initial_public'])

    def answer(self, fixture_id, public, target, *, action='ask_user', focus='all'):
        key = response_key(fixture_id, public, target, action, focus)
        require(key in self._rows, 'undefined response path; no dispatch or state commit')
        row = self._rows[key]
        after = following(public, row['response'], target)
        require(fingerprint(after) == row['next_public_sha256'], 'next public history mismatch')
        return after


def derive_candidate_label(row, review):
    require(row['split'] == 'train' and row['id'] == review['turn_id'], 'patch parent mismatch')
    require(fingerprint(row['input']) == review['source_input_sha256']
            and fingerprint(row['output']) == review['original_proposal_sha256'], 'conditional patch source drift')
    output = deepcopy(row['output'])
    for change in review['proposed_changes']:
        key = change['field'].removeprefix('output.')
        require(key in {'target_id', 'evidence_refs'} and output[key] == change['before'], 'patch precondition mismatch')
        output[key] = deepcopy(change['after'])
    output['reason_summary'] = '사용자가 먼저 확인하도록 요청한 burning 후보(clarify:turn1:1)의 본인 여부·실제 발생·시점을 확인한다.'
    validate_action(ActionProposal.model_validate(output), ActionContext.model_validate(row['input']))
    return {'id': 'e22:'+row['id'], 'split': 'train', 'parent_turn_id': row['id'],
        'parent_scenario_id': row['scenario_id'], 'group_id': row['group_id'],
        'scenario_family_id': row.get('scenario_family_id'), 'product_family_id': row['product_family_id'],
        'source_input_sha256': fingerprint(row['input']), 'source_proposal_sha256': fingerprint(row['output']),
        'input': deepcopy(row['input']), 'output': output,
        'review': {'synthetic': True, 'human_review': 'unreviewed', 'approved_reference': False,
                  'training_ready': False, 'kind': 'agent_proposed_conditional_label_derivative'},
        'scope': 'one derived label; not loaded by current training; candidate response worlds deferred'}


def serialized(rows):
    return ''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n' for r in rows)


def artifacts():
    design = json.loads((BUNDLE/'design.json').read_text(encoding='utf-8'))
    require(design['source_split'] == 'train' and design['production_enabled'] is False
            and design['training_ready'] is False, 'inactive train design required')
    parents = {s['scenario_id']: s for s in read_rows(V67/'canonical-candidates-v67.jsonl')}
    splits = {k: read_rows(V67/v) for k, v in SPLIT_FILES.items()}
    memberships = {}
    for split, records in splits.items():
        for r in records:
            require(r['scenario_id'] not in memberships or memberships[r['scenario_id']] == split, 'cross split parent')
            memberships[r['scenario_id']] = split
    fixtures = [derive_fixture(parents[f['parent_scenario_id']], memberships[f['parent_scenario_id']],
                               f['author_defined_additions']) for f in design['fixtures']]
    domains = json.loads((BASE/'data/afa/stage0-v1/contract.json').read_text(encoding='utf-8'))['tasks']['B-C02']['world_domains']
    for fixture in fixtures:
        for key, raw in fixture['environment_only']['response_table'].items():
            require(raw['state'] != 'known' or raw['value'] in domains[key], 'answer outside frozen bounded domain')
    book, counts = compile_book(fixtures)
    review = json.loads((BASE/'data/afa/v67-review-v1/review-decisions.json').read_text(encoding='utf-8'))['candidate_priority']
    row = next(r for r in splits['train'] if r['id'] == design['label_derivation']['parent_turn_id'])
    label = derive_candidate_label(row, review)
    label['scenario_family_id'] = parents[row['scenario_id']]['scenario_family_id']
    files = {'fixtures.jsonl': serialized(fixtures), 'responses.jsonl': serialized(book), 'derived-labels.jsonl': serialized([label])}
    sources = list(V67.glob('*.jsonl'))+[V67/'v67-sft-manifest.json', BUNDLE/'design.json',
        BASE/'data/afa/stage0-v1/contract.json', BASE/'data/afa/v67-review-v1/review-decisions.json', Path(__file__)]
    origins = Counter(o['kind'] for f in fixtures for o in f['environment_only']['response_provenance'].values())
    manifest = {'version': design['version'], 'mode': 'development_preview', 'production_enabled': False,
        'human_review': 'unreviewed', 'approved_reference': False, 'training_ready': False,
        'fixture_count': len(fixtures), 'response_origin_counts': dict(origins), **counts,
        'source_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        'files': {k: hashlib.sha256(v.encode()).hexdigest() for k, v in files.items()},
        'derived_label_count': 1, 'source_labels_changed': 0, 'current_training_input_changed': False,
        'scope': design['scope'], 'independent_evaluation': False}
    files['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)+'\n'
    return files, manifest


def verify():
    expected, manifest = artifacts()
    for name, text in expected.items():
        require((BUNDLE/name).read_bytes() == text.encode(), 'bundle/source drift: '+name)
    book = ResponseBook(read_rows(BUNDLE/'fixtures.jsonl'), read_rows(BUNDLE/'responses.jsonl'))
    require(book.counts == {k: manifest[k] for k in book.counts}, 'count mismatch')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['build', 'verify'])
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    if args.report:
        report = args.report.resolve()
        require(report.is_relative_to(ROOT/'outputs') and not report.exists(), 'new report inside outputs required')
    if args.command == 'build':
        files, _ = artifacts()
        require(not any((BUNDLE/name).exists() for name in files), 'bundle already exists; create a new version')
        for name, text in files.items():
            (BUNDLE/name).write_bytes(text.encode())
    result = verify()
    if args.report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['fixture_count', 'response_edges', 'public_history_nodes', 'complete_question_orders', 'response_origin_counts', 'derived_label_count']}))
