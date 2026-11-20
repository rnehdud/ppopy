"""Local SQL/artifact integration and import boundary checks; no RL rollout."""
import json
import math

import pytest

from beauty_agent.afa import tracking


def test_missing_values_are_not_reported_as_zero():
    assert tracking.numeric_metrics({'missing': None, 'known': 0, 'flag': False}) == {'known': 0.0}


@pytest.mark.parametrize('bad', [math.nan, math.inf, -math.inf])
def test_nonfinite_metric_is_rejected(bad):
    with pytest.raises(ValueError):
        tracking.numeric_metrics({'metric': bad})


def test_sql_artifact_import_is_idempotent_and_detects_source_changes(tmp_path, monkeypatch):
    monkeypatch.setattr(tracking, 'ROOT', tmp_path)
    source = tmp_path / 'source.json'
    source.write_text('{"synthetic":true}')
    store = tracking.LocalTracker(tmp_path / 'store')
    args = dict(metrics={'quality': 1, 'missing': None}, params={'seed': 0}, sources=[source],
                curves=[(32, {'reward': -5}), (64, {'reward': -3})])
    first = store.publish('unit', 'recorded', **args)
    assert store.publish('unit', 'recorded', **args) == first
    run = store.client.get_run(first)
    assert run.info.status == 'FINISHED' and run.data.metrics['quality'] == 1
    assert 'missing' not in run.data.metrics
    assert [(m.step,m.value) for m in store.client.get_metric_history(first, 'reward')] == [(32,-5),(64,-3)]
    artifact = store.client.download_artifacts(first, 'source-receipts.json', str(tmp_path))
    assert json.loads(open(artifact, encoding='utf-8').read())[0]['sha256'] == tracking.receipt(source)['sha256']
    source.write_text('{"synthetic":true,"revision":2}')
    assert store.publish('unit', 'recorded', **args) != first


def test_failed_import_remains_failed_and_is_not_reused(tmp_path, monkeypatch):
    monkeypatch.setattr(tracking, 'ROOT', tmp_path)
    source = tmp_path / 'source.json'
    source.write_text('{}')
    store = tracking.LocalTracker(tmp_path / 'store')
    with pytest.raises(ValueError):
        store.publish('unit', 'bad', metrics={}, params={}, sources=[source], curves=[(1, {'x': math.nan})])
    runs = store.client.search_runs([store.experiment('unit')])
    assert len(runs) == 1 and runs[0].info.status == 'FAILED'


def test_step_contract_is_checked_before_logging(tmp_path):
    store = tracking.LocalTracker(tmp_path / 'store')
    with pytest.raises(ValueError):
        store.log('unused', {'x': 1}, step=-1)
