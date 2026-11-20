"""Read-only whole-v67 EDA. Counts records; never fills missing answers or trains."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from data.action_policy.v67.dataset_cli import SPLIT_FILES, read_rows, verify

ROOT=Path(__file__).resolve().parents[6]
BASE=Path(__file__).resolve().parents[2]
V67=BASE/'data/action_policy/v67'


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def overlaps(grouped):
    return sum(len(s)>1 for s in grouped.values())


def profile(scenarios, splits, kb, contract):
    membership={}; by_sid={s['scenario_id']:s for s in scenarios}
    cards=Counter(); actions=Counter(); labels=Counter(); states=Counter(); lengths=Counter()
    observations_per_scenario=Counter(); target_pairs=set(); offered_pairs=set(); action_by_split={}; card_by_split={}
    candidate_sizes=Counter(); enabled_sizes=Counter(); text_lengths=[]
    input_fingerprints=defaultdict(set); input_counts=Counter(); choice_labels=defaultdict(set); input_examples=defaultdict(list)
    scenario_by_split=Counter(); enabled_answer_checks=Counter(); event_changes=[]; known_missing_value=[]
    event_types=Counter(); proposed_pairs_in_v2=0; supported_cards=0; samples=[]; choice_turns=0
    catalog={tuple(p) for p in contract['action_dictionary']}
    variables={v['id'] for v in kb['variables'] if v.get('consumer_question_allowed') is True}
    card_requirements={c['id']:set(c['observable_inputs'])&variables for c in kb['baseline_cards']}
    coverage=[]
    for split,rows in splits.items():
        ac=Counter(); cc=Counter()
        for row in rows:
            sid=row['scenario_id']
            if sid in membership and membership[sid]!=split:raise ValueError('scenario crosses splits')
            membership[sid]=split
            ctx=row['input']; proposal=row['output']; pair=(proposal['action'],proposal['target_id'])
            actions[pair[0]]+=1; ac[pair[0]]+=1; labels[row['review']['label_source']]+=1
            cc.update(set(row['card_ids'])); target_pairs.add(pair)
            enabled=[(a['action'],a['target_id']) for a in ctx['available_actions'] if a['enabled']]
            offered_pairs.update((a['action'],a['target_id']) for a in ctx['available_actions'])
            candidate_sizes[len(ctx['available_actions'])]+=1; enabled_sizes[len(enabled)]+=1
            proposed_pairs_in_v2+=pair in catalog
            public_hash=fingerprint(ctx); input_fingerprints[public_hash].add(split); input_counts[public_hash]+=1
            choice_labels[public_hash].add(pair)
            input_examples[public_hash].append({'turn_id':row['id'],'split':split,'action_target':pair})
            text_lengths.append(len(json.dumps(ctx,ensure_ascii=False,sort_keys=True)))
            for slot,value in ctx['observations'].items():
                states[value['state']]+=1
                if value['state']=='known' and value.get('value') is None:known_missing_value.append(row['id'])
            scenario=by_sid[sid]
            indices=[i for i,t in enumerate(scenario['turns']) if t['message']==ctx['message']]
            asks=[target for action,target in enabled if action=='ask_user' and target in variables]
            choice_turns+=len(asks)>=2
            if len(indices)==1:
                later=set()
                for turn in scenario['turns'][indices[0]+1:]:later.update(turn.get('user_events',{}).get('observations',{}))
                for target in asks:enabled_answer_checks['later_event_present' if target in later else 'not_recorded_later']+=1
            else:enabled_answer_checks['ambiguous_turn_alignment']+=len(asks)
        action_by_split[split]=dict(ac);card_by_split[split]=dict(cc)
    for s in scenarios:
        sid=s['scenario_id'];scenario_by_split[membership[sid]]+=1
        cards.update(set(s['card_ids']));lengths[len(s['turns'])]+=1
        supported_cards+=bool(s['card_ids']) and set(s['card_ids'])<={'B-C01','B-C02'}
        seen=defaultdict(list)
        for index,t in enumerate(s['turns']):
            events=t.get('user_events',{});event_types.update(k for k,v in events.items() if v)
            for slot,value in events.get('observations',{}).items():seen[slot].append((index,value))
        observations_per_scenario[len(seen)]+=1
        for slot,items in seen.items():
            if len({fingerprint({'state':v.get('state'),'value':v.get('value')}) for _,v in items})>1:event_changes.append({'scenario_id':sid,'slot':slot,'turns':[i+1 for i,_ in items]})
        required=set().union(*(card_requirements.get(c,set()) for c in s['card_ids']))
        coverage.append({'scenario_id':sid,'split':membership[sid],'required_consumer_slots':len(required),
            'recorded_observation_slots':len(seen),'unrecorded_card_slots':sorted(required-set(seen)),
            'note':'declared card-input coverage only; not all slots must be asked and this is not RL eligibility'})
    # Train-only stratified deterministic content-review sample. No test-guided tuning.
    for action in sorted(actions):
        pool=sorted((r for r in splits['train'] if r['output']['action']==action),key=lambda r:hashlib.sha256(r['id'].encode()).hexdigest())
        samples.extend(pool[:2])
    return {'scenario_count':len(scenarios),'turn_count':sum(map(len,splits.values())),
        'scenario_splits':dict(scenario_by_split),'turn_splits':{k:len(v) for k,v in splits.items()},
        'action_counts':dict(actions),'actions_by_split':action_by_split,'label_source_counts':dict(labels),
        'card_scenario_memberships':dict(cards),'card_turn_memberships_by_split':card_by_split,
        'unique_cards':len(cards),'kb_cards_not_referenced':sorted(set(card_requirements)-set(cards)),
        'scenario_length_histogram':dict(sorted(lengths.items())),
        'observation_snapshot_state_counts':dict(states),'canonical_observation_slot_histogram':dict(sorted(observations_per_scenario.items())),
        'nonempty_user_event_type_counts':dict(event_types),'changed_observation_records':event_changes,
        'known_null_value_ids':sorted(set(known_missing_value)),
        'candidate_count_histogram':dict(sorted(candidate_sizes.items())),'enabled_count_histogram':dict(sorted(enabled_sizes.items())),
        'unique_proposed_action_target_pairs':len(target_pairs),
        'unique_available_action_target_pairs':len(offered_pairs),
        'exact_input_duplicate_excess':sum(n-1 for n in input_counts.values()),
        'exact_input_cross_split_groups':overlaps(input_fingerprints),
        'exact_input_multilabel_groups':sum(len(v)>1 for v in choice_labels.values()),
        'exact_input_multilabel_examples':[input_examples[k] for k,v in choice_labels.items() if len(v)>1],
        'context_character_lengths':{'min':min(text_lengths),'max':max(text_lengths),'mean':sum(text_lengths)/len(text_lengths),
            'definition':'len(json.dumps(input, ensure_ascii=False, sort_keys=True)); characters, not model tokens'},
        'enabled_consumer_ask_later_observation_occurrences':dict(enabled_answer_checks),
        'turns_with_multiple_enabled_consumer_asks':choice_turns,
        'card_input_record_coverage':coverage,
        'scenarios_with_all_declared_consumer_card_inputs_recorded':sum(not r['unrecorded_card_slots'] for r in coverage),
        'v2_scope_comparison':{'v67_scenarios_only_C01_C02':supported_cards,'v67_proposals_in_v2_8_pair_catalog':proposed_pairs_in_v2,
            'note':'pair/card membership is not runtime compatibility or RL readiness; v2 is a separate 48-world design grid'},
        'review_sample_ids':[r['id'] for r in samples]},samples


def run(output):
    output=Path(output).resolve()
    if not output.is_relative_to(ROOT/'outputs') or output.exists():raise ValueError('choose a new directory inside repository outputs')
    sources=list(V67.glob('*.jsonl'))+[V67/'v67-sft-manifest.json',ROOT/'KB/Poppy_KB_v0.6/Poppy_KB_seed_v0.6.json',BASE/'data/afa/stage0-v1/contract.json']
    before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    integrity=verify(V67)
    scenarios=read_rows(V67/'canonical-candidates-v67.jsonl');splits={k:read_rows(V67/v) for k,v in SPLIT_FILES.items()}
    kb=json.loads(sources[-2].read_text(encoding='utf-8'));contract=json.loads(sources[-1].read_text(encoding='utf-8'))
    result,samples=profile(scenarios,splits,kb,contract)
    result.update(mode='development_preview',production_enabled=False,integrity=integrity,
        source_sha256=before,scope='whole-v67 descriptive diagnostics; internal test inspected for audit, never final unseen evaluation',
        human_review='unreviewed',independent_evaluation=False)
    assert before=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    output.mkdir(parents=True)
    (output/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'review-samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['card_input_record_coverage','source_sha256','changed_observation_records','card_turn_memberships_by_split']},ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
