"""Notebook의 실제 run_epochs를 작은 CPU 모델로 검사해 저장/중단/재개를 확인해요."""
import ast
import contextlib
import csv
import json
import math
import random
import time
from pathlib import Path

import pytest
import torch


LOSSES = [1.1898424282777467, 1.1321674500351582,
          1.1517600863773587, 1.220122238341485, 1.2742315510398496]


def notebook_namespace(tmp_path, resumed_epochs=0):
    notebook = Path(__file__).resolve().parents[1] / 'kaggle_early_stopping.ipynb'
    cells = json.loads(notebook.read_text(encoding='utf-8'))['cells']
    ns = dict(Path=Path, csv=csv, json=json, math=math, random=random, time=time, torch=torch)
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        tree = ast.parse(''.join(cell['source']))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {
            'early_stopping_settings', 'early_stopping_state', 'write_history', 'run_epochs'}]
        if functions:
            exec(compile(ast.Module(body=functions, type_ignores=[]), str(notebook), 'exec'), ns)
    events = []
    def write_json(path, value):
        Path(path).write_text(json.dumps(value), encoding='utf-8')
    def checkpoint(out, epoch, model, tokenizer, optimizer, scheduler, scaler, history, context, updates, attempts):
        events.append(('checkpoint', epoch))
        folder = Path(out) / 'checkpoints' / f'epoch-{epoch:02d}'
        folder.mkdir(parents=True)
        write_json(folder / 'metrics.json', history[-1])
    evaluations = []
    def evaluate(model, rows, encoded, device, dtype, path):
        epoch = resumed_epochs + len(evaluations) // 2 + 1
        evaluations.append(str(path))
        events.append(('evaluate', epoch))
        return (LOSSES[epoch - 1] if rows[0]['id'] == 'val' else .8 / epoch), 1, .001
    restored = [{'epoch':i + 1, 'val_token_loss':v, 'train_eval_token_loss':.8/(i+1),
                 'val_minus_train_eval':v-.8/(i+1)} for i, v in enumerate(LOSSES[:resumed_epochs])]
    ns.update(write_json=write_json, save_checkpoint=checkpoint, evaluate=evaluate,
              memory=lambda device:None, autocast=lambda device,dtype:contextlib.nullcontext(),
              masked_loss=lambda model,item,device:(model.weight.square().mean(), 1),
              load_training_state=lambda *args:{'history':restored, 'epoch':resumed_epochs,
                                                'updates':resumed_epochs, 'attempts':resumed_epochs})
    actual_writer = ns['write_history']
    def writer(out, history, cfg, context):
        if history[-1]['epoch'] > resumed_epochs:
            assert events[-1] == ('checkpoint', history[-1]['epoch'])
        return actual_writer(out, history, cfg, context)
    ns['write_history'] = writer
    return ns, events, evaluations


@pytest.mark.parametrize('resumed_epochs,expected_saved', [(0,[1,2,3,4]), (3,[4]), (4,[])])
def test_notebook_stops_after_saving_and_restores_patience(tmp_path, resumed_epochs, expected_saved):
    ns, events, evaluations = notebook_namespace(tmp_path, resumed_epochs)
    model = torch.nn.Linear(1, 1, bias=False)
    optimizer = torch.optim.SGD(model.parameters(), lr=.01)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda step:1.)
    scaler = torch.amp.GradScaler('cpu', enabled=False)
    cfg = {'epochs':5, 'seed':1, 'gradient_accumulation_steps':1,
           'gradient_clip_norm':1., 'overfit_delta':.01, **ns['early_stopping_settings']()}
    result = ns['run_epochs'](model, None, [{'id':'train'}], [{'id':'val'}], {'train':{}},
                              cfg, tmp_path, {'run_kind':'unit_test'}, optimizer, scheduler,
                              scaler, torch.device('cpu'), torch.float32,
                              resume='synthetic_checkpoint' if resumed_epochs else None)
    assert [e for kind,e in events if kind=='checkpoint'] == expected_saved
    assert len(result) == 4
    assert len(evaluations) == len(expected_saved) * 2
    best = json.loads((tmp_path/'best_by_val_loss.json').read_text())
    status = json.loads((tmp_path/'run_status.json').read_text())
    assert best['checkpoint'] == 'checkpoints/epoch-02'
    assert status['stopped_early'] and status['training_complete']
    assert status['completed_epochs'] == 4 and not status['max_epochs_reached']
    assert status['model_quality_approved'] is False
