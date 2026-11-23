"""Read-only recorded-next-event checks, not a counterfactual user simulator."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from beauty_agent.actions import ActionContext, ActionProposal
from beauty_agent.action_runtime import validate_action
from beauty_agent.contracts import ObservationSlot
from beauty_agent.loop import CandidateConfirmation
from .eda import ROOT, BASE, V67, fingerprint
from data.action_policy.v67.dataset_cli import read_rows


class MissingRecordedResponse(ValueError):
    """Dataset/adapter limitation. Never a fabricated unknown or Gym truncation."""


def alias_targets(turns):
    """Bind declared aliases to their exact extraction positions and turn namespace."""
    targets = {}
    for index, turn in enumerate(turns):
        symptoms = turn.get('extraction_fixture', {}).get('symptoms', [])
        for item in turn.get('candidate_aliases', []):
            pos = item['feature_index']
            if (not isinstance(pos, int) or isinstance(pos, bool) or not 0 <= pos < len(symptoms)
                    or symptoms[pos].get('symptom') != item['expected_symptom']):
                raise ValueError('candidate alias does not match extraction fixture')
            name = item['alias']
            if name in targets:
                raise ValueError('duplicate candidate alias')
            targets[name] = f'clarify:turn{index + 1}:{pos}'
    return targets


def action_key(proposal):
    """Wording/reason do not select a new response; confirmation focus can."""
    return (proposal['action'], proposal['target_id'],
            proposal.get('arguments', {}).get('confirmation_focus', 'all'))


def inspect_next_event(proposal, next_turn, aliases):
    """Check the immediate next record only. Presence is not a causal validity claim."""
    action, target, _ = action_key(proposal)
    if action in {'hold', 'request_draft'}:
        return {'status': 'terminal_label_needs_separate_judgment'}
    if next_turn is None:
        return {'status': 'no_next_record'}
    events = next_turn.get('user_events', {})
    observations = events.get('observations', {})
    if action == 'ask_user' and target in observations:
        slot = ObservationSlot.model_validate(observations[target])
        if slot.variable_id != target or not slot.confirmed_by_user or target.startswith('product.'):
            raise ValueError('not an explicitly confirmed user observation')
        return {'status': 'target_event_recorded', 'response_kind': 'observation',
                'response': slot.model_dump()}
    if action == 'confirm_candidate':
        for item in events.get('confirmations', []):
            alias = item['candidate_alias']
            if alias not in aliases:
                raise ValueError('confirmation alias has no declared target')
            if aliases[alias] == target:
                value = CandidateConfirmation.model_validate(item['value'])
                return {'status': 'target_event_recorded', 'response_kind': 'candidate_confirmation',
                        'response': {'target_id': target, 'value': value.model_dump()}}
    if action == 'resolve_conflict' and target in observations and target in events.get('resolve_conflicts', []):
        slot = ObservationSlot.model_validate(observations[target])
        if slot.variable_id != target or not slot.confirmed_by_user or target.startswith('product.'):
            raise ValueError('not an explicitly confirmed conflict resolution')
        return {'status': 'target_event_recorded', 'response_kind': 'conflict_resolution',
                'response': slot.model_dump()}
    if action == 'retrieve_evidence':
        return {'status': 'product_evidence_adapter_required'}
    if action == 'ask_user' and (target in {'confirm_profile', 'add_products', 'all_excluded'}
                                or target.startswith(('confirm:', 'resolve:'))):
        return {'status': 'profile_product_adapter_required'}
    return {'status': 'next_record_has_no_target_response'}


def require_recorded_response(recorded, selected, next_turn, aliases):
    """Reject an unsupported path before a caller dispatches anything.

    This helper does not execute, commit, calculate a reward, or assert RL readiness.
    Return the whole next event too, so unsolicited updates are not silently dropped.
    """
    if action_key(recorded) != action_key(selected):
        raise MissingRecordedResponse('unrecorded_action_or_confirmation_focus')
    result = inspect_next_event(selected, next_turn, aliases)
    if result['status'] != 'target_event_recorded':
        raise MissingRecordedResponse(result['status'])
    return {**result, 'next_record': deepcopy(next_turn),
            'scope': 'recorded immediate response presence; not a counterfactual response guarantee'}


def train_audit(scenarios, rows):
    """Train-only follow-up to E20. No label or canonical event is rewritten."""
    by_sid = {s['scenario_id']: s for s in scenarios}
    counts = Counter()
    by_action = defaultdict(Counter)
    transitions = []
    groups = defaultdict(list)
    for row in rows:
        if row['split'] != 'train':
            raise ValueError('follow-up review is train-only')
        scenario = by_sid[row['scenario_id']]
        # IDs are metadata for alignment only, never policy input.
        index = int(row['id'].rsplit('-t', 1)[1]) - 1
        turns = scenario['turns']
        if not 0 <= index < len(turns) or turns[index]['message'] != row['input']['message']:
            raise ValueError('canonical/SFT turn alignment failed')
        aliases = alias_targets(turns[:index + 1])
        next_turn = turns[index + 1] if index + 1 < len(turns) else None
        result = inspect_next_event(row['output'], next_turn, aliases)
        counts[result['status']] += 1
        by_action[row['output']['action']][result['status']] += 1
        transitions.append({'turn_id': row['id'], 'action': row['output']['action'],
                            'target_id': row['output']['target_id'], **result})
        groups[fingerprint(row['input'])].append(row)
    alternatives = []
    for input_hash, group in groups.items():
        if len({action_key(r['output'])[:2] for r in group}) <= 1:
            continue
        labels = []
        for row in group:
            applied, _ = validate_action(ActionProposal.model_validate(row['output']),
                                         ActionContext.model_validate(row['input']))
            labels.append({'turn_id': row['id'], 'action': applied.action, 'target_id': applied.target_id,
                           'runtime_gate_valid': True, 'reason_summary': row['output']['reason_summary']})
        alternatives.append({'input_sha256': input_hash, 'labels': labels})
    return {'mode': 'development_preview', 'production_enabled': False, 'split': 'train',
            'turns': len(rows), 'scenarios': len({r['scenario_id'] for r in rows}),
            'status_counts': dict(counts), 'statuses_by_action': {k: dict(v) for k, v in by_action.items()},
            'same_input_different_choices': alternatives, 'transitions': transitions,
            'scope': 'next-record target event presence only; not RL eligible count or label correctness',
            'human_review': 'unreviewed', 'new_policy_training_runs': 0}


def run(output):
    output = Path(output).resolve()
    if not output.is_relative_to(ROOT/'outputs') or output.exists():
        raise ValueError('choose a new directory inside repository outputs')
    paths = list(V67.glob('*.jsonl')) + [V67/'v67-sft-manifest.json']
    sources = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    r = train_audit(read_rows(V67/'canonical-candidates-v67.jsonl'), read_rows(V67/'v67-sft-train.jsonl'))
    assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest() == v for k, v in sources.items())
    r['source_sha256'] = sources
    r['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output.mkdir(parents=True)
    (output/'report.json').write_text(json.dumps(r, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: r[k] for k in ['turns', 'scenarios', 'status_counts']}, ensure_ascii=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output)
