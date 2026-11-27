"""Kaggle용 조기 종료 판단만 정의해요. import로 학습·다운로드를 시작하지 않아요."""
import math


def early_stopping_settings():
    """최대5 epoch는 유지하되 검증2회 연속 비개선이면 멈춰요."""
    return {
        'early_stopping': True,
        'early_stopping_patience': 2,
        'early_stopping_min_delta': 0.0,
    }


def early_stopping_state(history, cfg):
    """완료된 epoch 이력에서 상태를 복원해 재개 때 patience가 초기화되지 않게 해요.

    중단용 min_delta 기준과 실제 최저 loss checkpoint 선택은 구분해요.
    NaN/무한대나 누락된 epoch는 조용히 통과시키지 않아요.
    """
    enabled = cfg.get('early_stopping', True)
    patience = cfg.get('early_stopping_patience', 2)
    delta = cfg.get('early_stopping_min_delta', 0.0)
    if type(enabled) is not bool:
        raise ValueError('early_stopping은 bool이어야 해요.')
    if type(patience) is not int or patience < 1:
        raise ValueError('patience는1 이상의 정수여야 해요.')
    if type(delta) not in (int, float) or not math.isfinite(delta) or delta < 0:
        raise ValueError('min_delta는 유한한0 이상의 수여야 해요.')
    state = {
        'enabled': enabled, 'monitor': 'val_token_loss', 'mode': 'min',
        'patience': patience, 'min_delta': delta, 'bad_epochs': 0,
        'best_epoch': None, 'best_val_loss': None, 'best_checkpoint': None,
        'reference_best_loss': None, 'last_epoch': None,
        'stopped': False, 'stopped_epoch': None,
    }
    for index, row in enumerate(history):
        epoch, loss = row['epoch'], float(row['val_token_loss'])
        if type(epoch) is not int or epoch != index + 1:
            raise ValueError('완료 이력은 epoch1부터 연속이어야 해요.')
        if not math.isfinite(loss):
            raise ValueError('유한하지 않은 validation loss예요.')
        state['last_epoch'] = epoch
        if state['best_val_loss'] is None or loss < state['best_val_loss']:
            state.update(best_epoch=epoch, best_val_loss=loss,
                         best_checkpoint=f'checkpoints/epoch-{epoch:02d}')
        if state['reference_best_loss'] is None or loss < state['reference_best_loss'] - delta:
            state['reference_best_loss'] = loss
            state['bad_epochs'] = 0
        else:
            state['bad_epochs'] += 1
        if enabled and state['bad_epochs'] >= patience:
            state.update(stopped=True, stopped_epoch=epoch)
            break
    return state
