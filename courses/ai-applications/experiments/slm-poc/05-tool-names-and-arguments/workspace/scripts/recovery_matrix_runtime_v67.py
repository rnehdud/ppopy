"""Technical launcher: preserve frozen matrix sources and verify both manifests."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import recovery_matrix_v67 as matrix
from scripts.korean_material_v67 import write,sha
AMEND=matrix.OUT/'runtime-amendment.json'
original_verify=matrix.verify

def verify():
    plan=original_verify();a=matrix.read(AMEND)
    for name,h in a['files'].items():assert sha(ROOT/name)==h,name
    return plan

if __name__=='__main__':
    if '--prepare' in sys.argv:
        original_verify();assert not (matrix.OUT/'started.json').exists()
        identity=json.loads((matrix.OUT/'training-process-identity.json').read_text(encoding='utf-8-sig'))
        assert identity['pid']==10024 and 'train_korean_native_v67.py' in identity['CommandLine']
        paths=[Path(__file__),ROOT/'scripts/stop_after_checkpoint_v67_v2.ps1',matrix.OUT/'training-process-identity.json']
        write(AMEND,{'reason':'Before matrix execution: deferred B calls the parent verification hook, which must point to the matrix+parent manifests. The uv venv launcher runs a base-Python child; pin observed actual executable and complete command line instead of mistaking the launcher path for the model process.',
             'matrix_results_observed':False,'final_results_observed':False,
             'training_identity':identity,'files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
        print('V67 runtime amendment frozen; original matrix files unchanged.')
    else:
        matrix.verify=verify
        matrix.exp.verify=verify
        matrix.main()
