"""Local-only MLflow publication of recorded AFA results; never runs learning."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[6]
DEFAULT_STORE = ROOT / 'outputs/afa-mlflow'
METRICS = ('mean_questions', 'mean_cost', 'mean_return', 'correct_terminal_rate',
           'semantic_match_rate', 'wrong_hold_rate', 'error_among_drafts', 'policy_fallbacks')


def receipt(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def numeric_metrics(values):
    """Null is absent, never zero; reject nonfinite values before a write."""
    result = {}
    for key, value in values.items():
        if value is None or isinstance(value, bool):
            continue
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError('nonfinite or nonnumeric metric: ' + key)
        result[key] = float(value)
    return result


class LocalTracker:
    """Explicit run lifecycle usable by future PPO/EDA code, with no global autolog."""
    def __init__(self, directory=DEFAULT_STORE):
        from mlflow import MlflowClient
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.uri = 'sqlite:///' + (self.directory / 'tracking.db').as_posix()
        self.client = MlflowClient(tracking_uri=self.uri)

    def experiment(self, name):
        existing = self.client.get_experiment_by_name(name)
        return existing.experiment_id if existing else self.client.create_experiment(
            name, artifact_location=(self.directory / 'artifacts' / name).as_uri())

    def start(self, experiment, name, *, tags=None, params=None):
        experiment_id = self.experiment(experiment)
        run = self.client.create_run(experiment_id, tags={
            **(tags or {}), 'mlflow.runName': name, 'mode': 'development_preview',
            'production_enabled': 'false', 'human_review': 'unreviewed',
            'independent_evaluation': 'false'})
        for key, value in (params or {}).items():
            self.client.log_param(run.info.run_id, key, json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value))
        return run.info.run_id

    def log(self, run_id, metrics, step=0):
        if type(step) is not int or step < 0:
            raise ValueError('step must be a nonnegative integer')
        values = numeric_metrics(metrics)
        from mlflow.entities import Metric
        self.client.log_batch(run_id, metrics=[Metric(k, v, int(time.time()*1000), step) for k,v in values.items()])

    def finish(self, run_id, *, failed=False):
        self.client.set_terminated(run_id, status='FAILED' if failed else 'FINISHED')

    def publish(self, experiment, name, *, metrics, params, sources, tags=None, curves=None, figures=None):
        """Content-addressed import: retries reuse a completed run; failed runs remain visible."""
        values = numeric_metrics(metrics)
        sources = [Path(p) for p in sources]
        receipts = [receipt(p) for p in sources]
        payload = {'import_schema': 1, 'experiment': experiment, 'name': name, 'metrics': values,
                   'params': params, 'sources': receipts, 'curves': curves or [], 'figures': figures or []}
        key = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        eid = self.experiment(experiment)
        found = self.client.search_runs([eid], filter_string=f"tags.import_key = '{key}' and attributes.status = 'FINISHED'")
        if found:
            return found[0].info.run_id
        run_id = self.start(experiment, name, params=params, tags={
            **(tags or {}), 'import_key': key, 'record_kind': 'historical_import',
            'imported_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'mlflow.note.content': 'Historical results imported; no new learning/evaluation. See source receipts and scope. Null metrics omitted.'})
        try:
            self.log(run_id, values)
            for step, row in curves or []:
                self.log(run_id, row, step)
            with tempfile.TemporaryDirectory() as temporary:
                folder = Path(temporary)
                (folder / 'source-receipts.json').write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding='utf-8')
                self.client.log_artifact(run_id, str(folder / 'source-receipts.json'))
                for filename, title, labels, numbers, ylabel in figures or []:
                    import matplotlib
                    matplotlib.use('Agg')
                    from matplotlib import pyplot as plt
                    fig, ax = plt.subplots(figsize=(9, 4.8), layout='constrained')
                    ax.bar(labels, numbers, color='#3677b5')
                    ax.set(title=title, ylabel=ylabel)
                    ax.tick_params(axis='x', labelrotation=15)
                    ax.bar_label(ax.containers[0], fmt='%.3f')
                    fig.savefig(folder / filename, dpi=150)
                    plt.close(fig)
                    self.client.log_artifact(run_id, str(folder / filename), 'charts')
            for path in sources:
                self.client.log_artifact(run_id, str(path), 'sources/' + path.parent.name)
            self.finish(run_id)
            return run_id
        except BaseException:
            self.finish(run_id, failed=True)
            raise


def import_history(directory=DEFAULT_STORE):
    """Import frozen E07/E13 reports without loading a checkpoint or running an env."""
    trial = ROOT / 'outputs/afa-stage5a-trial-v1'
    folds = ROOT / 'outputs/afa-fold-baselines-v1'
    audit = json.loads((trial / 'audit.json').read_text(encoding='utf-8'))
    report = json.loads((folds / 'comparison.json').read_text(encoding='utf-8'))
    groups = json.loads((folds / 'subgroup-diagnostics.json').read_text(encoding='utf-8'))
    if any(x.get('production_enabled') is not False for x in [audit, report]):
        raise ValueError('only inactive synthetic reports may be imported')
    if groups['source_report_sha256'] != receipt(folds / 'comparison.json')['sha256']:
        raise ValueError('subgroup report/source mismatch')
    tracker = LocalTracker(directory)
    result = []
    rows = list(csv.DictReader((trial / 'logs/progress.csv').open(encoding='utf-8', newline='')))
    curves = [(int(row['time/total_timesteps']), {k: float(v) for k,v in row.items() if v and k != 'time/total_timesteps'}) for row in rows]
    for phase in ['before', 'after']:
        data = audit[phase + '_train_diagnostic']
        result.append(tracker.publish('AFA-v1-PPO-connection', phase + '-256step-train-only',
            metrics={k: data[k] for k in METRICS if k in data},
            params={'seed': 0, 'fit_worlds': 6, 'evaluation_split': 'same_train', 'phase': phase,
                    'training_steps': 256 if phase == 'after' else 0},
            tags={'environment_version': 'v1', 'evidence_entry': 'E07'},
            sources=[trial / 'audit.json', trial / 'config.json', trial / 'logs/progress.csv'],
            curves=curves if phase == 'after' else None))
    # Each cost/policy has its own comparable run; seeds/folds remain repetitions.
    for summary in report['summaries']:
        cost, policy = summary['cost_protocol'], summary['policy']
        metrics = {k: summary[k] for k in METRICS if k in summary}
        run_id = tracker.publish('AFA-v2-family-fold-baselines', cost + '--' + policy,
            metrics=metrics, params={'cost_protocol': cost, 'policy': policy, 'folds': 16,
                'unique_worlds': 48, 'seeds': [0,1,2], 'fit_worlds_per_fold': 45},
            tags={'environment_version': 'v2', 'evidence_entry': 'E13', 'scope': 'internal_family_cv_not_final_test'},
            sources=[folds / 'comparison.json', folds / 'subgroup-diagnostics.json'])
        extras = {}
        for group in groups['groups']:
            if group['cost_protocol'] == cost and group['policy'] == policy:
                for key in ('mean_questions', 'mean_cost', 'correct_terminal_rate', 'distinct_worlds'):
                    extras[group['structural_group'] + '/' + key] = group[key]
        recorded = tracker.client.get_run(run_id).data.metrics
        tracker.log(run_id, {k: v for k,v in extras.items() if recorded.get(k) != v})
        result.append(run_id)
    figures = []
    aliases = {'existing_rule_order': 'Rule order', 'uniform_all_allowed': 'Random all',
               'random_acquisition_fixed_stop': 'Random asks', 'joint_train_greedy': 'Greedy',
               'joint_train_multistep': 'Multistep'}
    for cost in report['protocol']['cost_protocols']:
        selected = [s for s in report['summaries'] if s['cost_protocol'] == cost]
        for key in ('mean_questions', 'mean_cost', 'correct_terminal_rate'):
            figures.append((cost + '-' + key + '.png', cost + ': ' + key + ' (internal synthetic CV)',
                [aliases[s['policy']] for s in selected], [s[key] for s in selected], key))
        selected = [g for g in groups['groups'] if g['cost_protocol'] == cost]
        figures.append((cost + '-subgroups.png', cost + ': subgroup questions (lower is better at equal quality)',
            [aliases[g['policy']] + '\n' + g['structural_group'] for g in selected],
            [g['mean_questions'] for g in selected], 'Mean questions; check quality separately'))
    result.append(tracker.publish('AFA-00-Overview', 'E07-E13-recorded-results',
        metrics={'v2_unique_synthetic_worlds': 48, 'v2_families': 16},
        params={'scope': 'historical_internal_only', 'v2_PPO_trained': False,
                'quality_warning': 'Random all stops early; low cost is not success',
                'subgroup_warning': 'Hands: multistep 4.75 vs rule 4.50; tools drive average gain'},
        sources=[folds / 'comparison.json', folds / 'subgroup-diagnostics.json', trial / 'audit.json'],
        figures=figures))
    software = ROOT / 'outputs/afa-layout-v1/verification.json'
    verified = json.loads(software.read_text(encoding='utf-8'))
    result.append(tracker.publish('AFA-software-verification', 'E16-relocation-regression',
        metrics={'tests_passed': verified['full_experiment_tests_passed'],
                 'protected_files_unchanged': verified['protected_source_data_files_unchanged']},
        params={'evidence_entry': 'E16', 'scope': 'software_only_not_policy_quality',
                'original_strict_known_failures': 5, 'original_strict_rerun_in_E16': False},
        sources=[software, ROOT / 'outputs/afa-layout-v1/experiment-tests-full.txt']))
    current_tests = ROOT / 'outputs/afa-mlflow-v1/regression-result.json'
    if current_tests.exists():
        record = json.loads(current_tests.read_text(encoding='utf-8'))
        log = current_tests.with_name('tests.txt')
        if record['exit_code'] != 0 or receipt(log)['sha256'] != record['log_sha256']:
            raise ValueError('regression log/receipt mismatch')
        result.append(tracker.publish('AFA-software-verification', 'E17-MLflow-regression',
            metrics={'tests_passed': record['tests_passed']},
            params={'evidence_entry': 'E17', 'scope': 'software_only_not_policy_quality'},
            sources=[current_tests, log]))
    return {'tracking_uri': tracker.uri, 'run_ids': result, 'run_count': len(result), 'new_learning': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['import-history', 'serve'])
    args = parser.parse_args()
    if args.command == 'import-history':
        print(json.dumps(import_history(), indent=2))
    else:
        store = LocalTracker()
        subprocess.run([sys.executable, '-m', 'mlflow', 'server', '--host', '127.0.0.1', '--port', '5000',
                        '--backend-store-uri', store.uri, '--default-artifact-root',
                        (store.directory / 'artifacts').as_uri(), '--workers', '1'], check=True)


if __name__ == '__main__':
    main()
