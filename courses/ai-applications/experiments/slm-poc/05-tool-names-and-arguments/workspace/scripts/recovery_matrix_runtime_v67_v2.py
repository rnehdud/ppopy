"""Avoid automatic extra training/final tests of already rejected candidates.

If the five dev arms all fail, retain the untouched final test and inspect the
already published 3B caller before spending another full lower-LR training run.
"""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import recovery_matrix_runtime_v67 as runtime
from scripts import recovery_matrix_v67 as matrix
from scripts.korean_material_v67 import write,sha
AMEND=matrix.OUT/'runtime-amendment-v2.json'

class ContinueWithPublicModel(Exception):pass

def verify():
    p=runtime.verify();a=matrix.read(AMEND)
    for name,h in a['files'].items():assert sha(ROOT/name)==h,name
    return p

def defer_b(*args,**kwargs):
    verify()
    candidates=[matrix.read(matrix.AB/'A-1000/candidate.json')]
    base=matrix.read(matrix.AB/'baseline/dev-summary.json')
    for label,count,lr in [('A-3000',3000,3e-5),('C',0,0),('D',0,0),('E',0,0)]:
        r=matrix.read(matrix.OUT/label/'dev-summary.json');healthy,score=matrix.exp.health_and_score(r,base)
        candidates.append({'label':label,'presentations':count,'lr':lr,'healthy':healthy,'score':score,'dev':r})
    assert not any(c['healthy'] for c in candidates)
    write(matrix.OUT/'controls-rejected-before-final.json',{
       'candidates':candidates,'final_test_read':False,'B_training_updates':0,
       'reason':'All five arms fail the predeclared dev gate. Do not run a final test of a known rejected candidate. Before repeating training, test the same actual tools with the already public non-gated xLAM3B caller, which uses the same native JSON interface.',
       'next_model':matrix.read(ROOT/'output/korean-native-v67/references/xlam3b-metadata.json')})
    raise ContinueWithPublicModel()

if __name__=='__main__':
    if '--prepare' in sys.argv:
        runtime.verify();assert not (matrix.OUT/'started.json').exists()
        assert not (matrix.AB/'baseline/test-files.json').exists()
        paths=[Path(__file__),ROOT/'output/korean-native-v67/references/xlam3b-metadata.json']
        write(AMEND,{'reason':'Before any control/final outcomes: if all current dev arms fail, keep final test untouched and audit the existing public3B caller before another full lower-LR run. A remains the same complete3000-example experiment. This is a pre-final research continuation, not a negative universal conclusion or a paused goal.',
           'model_interface':'Same xLAM native JSON tools and existing Transformers inference, no new model architecture or dataset invented.',
           'files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
        print('V67 continuation rule frozen before control outcomes; final test stays untouched when all dev candidates fail.')
    else:
        matrix.verify=verify;matrix.exp.verify=verify;matrix.exp.train_trial=defer_b
        try:matrix.main()
        except ContinueWithPublicModel:
            print('V67 CONTROLS REJECTED: final untouched; continue with the pinned existing public3B caller before lower-LR training.',flush=True)
