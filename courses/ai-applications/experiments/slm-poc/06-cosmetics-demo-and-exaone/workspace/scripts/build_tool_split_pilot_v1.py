"""Freeze small multi-tool selector/gate experiments and new source test rows."""
import collections
import csv
import hashlib
import json
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_tool_decision_mix_v1 import read_jsonl, norm, stable, tools_normalized
from scripts.when2call_operational_data_v1 import action_row
from scripts.tool_split_data_v1 import selector_view, gate_view, gold_index, fits, canonical

OUT = ROOT / 'data/processed/tool-split-pilot-v1'
PREVIOUS = ROOT / 'data/processed/tool-decision-mix-v4'


def paired_fit(row, tokenizer):
    try:
        flat, reason = action_row(row)
        if reason or not fits(flat, tokenizer):
            return False
        return all(fits(gate_view(row, i), tokenizer) for i in range(len(row['tools'])))
    except (ValueError, KeyError, StopIteration):
        return False


def write(name, rows):
    (OUT / (name + '.jsonl')).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf8')


def unique(rows):
    grouped = collections.defaultdict(list)
    for row in rows:
        grouped[canonical(row)].append(row)
    result = []
    for items in grouped.values():
        labels = {tuple(c['name'] for c in r.get('reference_calls', [])) for r in items}
        if len(labels) == 1:
            result.append(items[0])
    return result


def pool(split, tokenizer, multi_calls=True):
    rows = read_jsonl(PREVIOUS / (split + '_all_lengths.jsonl'))
    eligible = [r for r in rows if 1 <= len(r['tools']) <= 7 and len(r.get('reference_calls', [])) <= 1 and paired_fit(r, tokenizer)]
    eligible = unique(eligible)
    calls = [r for r in eligible if len(r['reference_calls']) == 1 and (len(r['tools']) >= 2 or not multi_calls)]
    stops = [r for r in eligible if not r['reference_calls'] and (
        r['source'] == 'when2call_pref' or r.get('target') in ('ask', 'no_tool'))]
    return calls, stops, {'original': len(rows), 'all_views_fit_unique': len(eligible), 'multi_call': len(calls), 'stop': len(stops)}


def main():
    from transformers import AutoTokenizer
    if OUT.exists():
        raise FileExistsError('Frozen dataset already exists')
    config = json.loads((ROOT / 'configs/tool-split-experiment-v1.json').read_text(encoding='utf8'))
    rng = random.Random(config['seed'])
    tokenizer = AutoTokenizer.from_pretrained(ROOT / 'models/ko-decision-roberta-large', local_files_only=True)
    tokenizer.model_max_length = 1000000
    stats = {}
    calls, stops, stats['train_pool'] = pool('train', tokenizer)
    rng.shuffle(calls)
    rng.shuffle(stops)
    if len(calls) < config['call_examples'] or len(stops) < config['stop_examples']:
        raise ValueError(('Insufficient auditable examples', stats))
    selected_calls = calls[:config['call_examples']]
    selected_stops = stops[:config['stop_examples']]
    train = selected_calls + selected_stops
    replay = read_jsonl(ROOT / 'data/processed/kotraj-200-v1/train.jsonl')[:config['legacy_replay_examples']]
    replay = [dict(r, replay_weight=2., replay_source='existing kotraj training split') for r in replay]
    # No class names are fixed outputs: current supplied tool definitions become options.
    selector = [dict(selector_view(r), target=f'tool_{gold_index(r):03d}') for r in selected_calls] + replay
    flat = [action_row(r)[0] for r in train] + replay
    gate = [gate_view(r, gold_index(r), 'yes') for r in selected_calls]
    gate += [gate_view(r, rng.randrange(len(r['tools'])), 'no') for r in selected_stops]
    gate += replay
    training_names = {norm(t['name']) for r in train for t in r['tools']}
    training_names.update(norm(k) for r in replay for k in r['options'] if k not in ('ask', 'none', 'no_tool'))
    train_questions = {norm(r['input']) for r in train}
    train_questions.update(norm(r['context']) for r in replay)
    for split in ['dev', 'test']:
        yes, no, stats[split + '_pool'] = pool(split, tokenizer)
        yes = [r for r in yes if not training_names & {norm(t['name']) for t in r['tools']} and norm(r['input']) not in train_questions]
        no = [r for r in no if not training_names & {norm(t['name']) for t in r['tools']} and norm(r['input']) not in train_questions]
        rng.shuffle(yes)
        rng.shuffle(no)
        if split == 'dev':
            # Development-only source preference labels; no stop subtype guessed.
            dev = yes[:80] + no[:80]
        else:
            previously_scored = {r['id'] for r in read_jsonl(PREVIOUS / 'test.jsonl')}
            transfer = [r for r in yes if r['id'] not in previously_scored][:80]
    # Existing official MCQ labels, never teachers. Exclude all 150 old source groups.
    previous_rows = read_jsonl(ROOT / 'output/training/when2call-action-replay-v1/official-evaluation-input.jsonl')
    old_groups = {r['original_source_group'] for r in previous_rows}
    official_pool = collections.defaultdict(list)
    source_path = ROOT / 'output/tool-dataset-research-20261107/nvidia__When2Call/when2call_test_mcq.jsonl'
    for original in read_jsonl(source_path):
        try:
            tools = tools_normalized(original['tools'])
            group = original['source'] + ':' + norm(original.get('orig_question') or original['question'])
            if group in old_groups or not 2 <= len(tools) <= 7 or norm(original['question']) in train_questions:
                continue
            if training_names & {norm(t['name']) for t in tools}:
                continue
            answer = original['correct_answer']
            calls = []
            if answer == 'tool_call':
                call = original['answers']['tool_call']
                call = json.loads(call) if isinstance(call, str) else call
                if isinstance(call, list):
                    if len(call) != 1:
                        continue
                    call = call[0]
                calls = [{'name': call['name'], 'arguments': call.get('arguments') or {}}]
                if calls[0]['name'] not in {t['name'] for t in tools}:
                    continue
            row = {'id': 'official:' + original['uuid'], 'source': 'official_when2call',
                   'input': original['question'], 'tools': tools,
                   'messages': [{'role': 'user', 'content': original['question']}], 'reference_calls': calls,
                   'target': 'ask' if answer == 'request_for_info' else 'no_tool',
                   'metric_group': answer, 'original_source_group': group,
                   'source_held_out_param': original.get('held_out_param'),
                   'source_target_tool': original.get('target_tool')}
            if paired_fit(row, tokenizer):
                official_pool[answer].append(row)
        except (KeyError, ValueError, TypeError):
            continue
    official, groups = [], set()
    for category in ['tool_call', 'request_for_info', 'cannot_answer']:
        candidates = official_pool[category]
        rng.shuffle(candidates)
        accepted = []
        for row in candidates:
            if row['original_source_group'] in groups:
                continue
            groups.add(row['original_source_group'])
            accepted.append(row)
            if len(accepted) == 40:
                break
        if len(accepted) < 25:
            raise ValueError(('Too few fresh official examples', category, len(accepted)))
        official.extend(accepted)
    OUT.mkdir(parents=True)
    for name, rows in {'train_source': train, 'selector_train': selector, 'flat_train': flat,
                       'gate_train': gate, 'dev': dev, 'fresh_official_test': official,
                       'fresh_multitool_test': transfer,
                       'old_dev': read_jsonl(ROOT / 'data/processed/kotraj-200-v1/dev.jsonl'),
                       'old_test': read_jsonl(ROOT / 'data/processed/kotraj-200-v1/test.jsonl')}.items():
        write(name, rows)
    stats.update(train_call_sources=dict(collections.Counter(r['source'] for r in selected_calls)),
                 train_stop_sources=dict(collections.Counter(r['source'] for r in selected_stops)),
                 train_call_tool_counts=dict(collections.Counter(len(r['tools']) for r in selected_calls)),
                 train_stop_tool_counts=dict(collections.Counter(len(r['tools']) for r in selected_stops)),
                 dev={'call': sum(bool(r['reference_calls']) for r in dev), 'stop': sum(not r['reference_calls'] for r in dev)},
                 fresh_official=dict(collections.Counter(r['metric_group'] for r in official)),
                 fresh_official_available={k: len(v) for k, v in official_pool.items()},
                 fresh_multitool=len(transfer), excluded_old_official_groups=len(old_groups),
                 training_tool_names=len(training_names))
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.jsonl')}
    (OUT / 'manifest.json').write_text(json.dumps({'config': config, 'stats': stats, 'files': files,
        'label_scope': 'Existing synthetic source labels. No guessed missing-information subtype for source preference texts. Fresh official rows retain original source gold, subject to review before scoring.',
        'novelty_scope': 'Tool names absent from this added training, not guaranteed absent from pretraining/old adapter or semantically novel.'}, ensure_ascii=False, indent=2), encoding='utf8')
    with (OUT / 'official-review.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'category', 'input', 'tools', 'source_held_out_param', 'review'])
        writer.writeheader()
        for row in official:
            writer.writerow({'id': row['id'], 'category': row['metric_group'], 'input': row['input'],
                             'tools': stable(row['tools']), 'source_held_out_param': row['source_held_out_param'],
                             'review': 'source_label_not_independent_human_gold'})
    print(json.dumps(stats, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
