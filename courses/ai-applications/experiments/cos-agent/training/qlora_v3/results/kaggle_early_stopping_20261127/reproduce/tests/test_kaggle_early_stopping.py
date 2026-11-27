"""조기 종료 경계·재개 상태 검사. 모델 다운로드나 GPU 학습은 하지 않아요."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kaggle_early_stopping import early_stopping_settings, early_stopping_state


def history(losses):
    return [{'epoch':i + 1, 'val_token_loss':loss} for i, loss in enumerate(losses)]


def test_observed_kaggle_sequence_stops_after_four_and_selects_two():
    rows = history([1.1898424282777467, 1.1321674500351582,
                    1.1517600863773587, 1.220122238341485])
    before = early_stopping_state(rows[:3], early_stopping_settings())
    assert before['bad_epochs'] == 1 and not before['stopped']
    resumed = early_stopping_state(rows, early_stopping_settings())
    assert resumed['stopped'] and resumed['stopped_epoch'] == 4
    assert resumed['best_checkpoint'] == 'checkpoints/epoch-02'


def test_improvement_resets_patience_and_equal_loss_does_not():
    cfg = early_stopping_settings()
    assert not early_stopping_state(history([2., 2., 1.5, 1.5]), cfg)['stopped']
    state = early_stopping_state(history([2., 2., 1.5, 1.5, 1.5]), cfg)
    assert state['stopped_epoch'] == 5 and state['best_epoch'] == 3


def test_small_improvement_can_be_selected_without_resetting_patience():
    cfg = {**early_stopping_settings(), 'early_stopping_min_delta':.1}
    state = early_stopping_state(history([2., 1.95, 1.94]), cfg)
    assert state['stopped_epoch'] == 3
    assert state['best_epoch'] == 3 and state['best_val_loss'] == 1.94


def test_disabled_does_not_stop_and_empty_history_is_safe():
    cfg = {**early_stopping_settings(), 'early_stopping':False}
    assert not early_stopping_state(history([1., 2., 3., 4.]), cfg)['stopped']
    assert early_stopping_state([], cfg)['best_epoch'] is None


@pytest.mark.parametrize('loss', [float('nan'), float('inf'), -float('inf')])
def test_invalid_validation_loss_is_rejected(loss):
    with pytest.raises(ValueError):
        early_stopping_state(history([loss]), early_stopping_settings())


@pytest.mark.parametrize('override', [
    {'early_stopping_patience':0}, {'early_stopping_patience':True},
    {'early_stopping_min_delta':-.1}, {'early_stopping_min_delta':float('nan')},
    {'early_stopping':'true'},
])
def test_invalid_configuration_is_rejected(override):
    with pytest.raises(ValueError):
        early_stopping_state([], {**early_stopping_settings(), **override})
