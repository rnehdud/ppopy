"""Evaluate the untrained Qwen3 model against the previously observed frozen cases."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.runtime import SYSTEM,TOOLS
from training.data import verify_freeze
from training.evaluation import evaluate

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='output/runs/qwen3-baseline-v1')
    parser.add_argument('--trained',action='store_true',help='Evaluate the currently loaded project LoRA')
    args=parser.parse_args()
    manifest=verify_freeze(ROOT)
    config=json.loads((ROOT/'output/runtime-qwen3/server_config.json').read_text(encoding='utf-8-sig'))
    if bool(config['adapter']) != args.trained:
        raise ValueError('Adapter presence does not match --trained')
    cases=json.loads((ROOT/'data/stateful/v2/holdout.cases.json').read_text(encoding='utf-8'))
    path=ROOT/args.output
    result=evaluate(None,cases,path,'qwen3-trained' if args.trained else 'qwen3-baseline',args.trained,model_id='qwen3-4b-instruct-2507',
                    model_description='Qwen3-4B-Instruct-2507 Q4_K_M'+(' + project LoRA' if args.trained else ', no project training'),
                    base_url=f'http://127.0.0.1:{config["port"]}')
    metadata={'server':config,'model_manifest':json.loads((ROOT/'models/qwen3-4b-instruct-2507/manifest.json').read_text(encoding='utf-8')),
              'holdout_sha256':manifest['files']['holdout.cases.json']['sha256'],
              'system':SYSTEM,'tools':TOOLS,'generation':{'temperature':0,'seed':42,'max_tokens':384,'cache_prompt':False},
              'runtime_sha256':hashlib.sha256((ROOT/'agent/runtime.py').read_bytes()).hexdigest(),
              'evaluation_sha256':hashlib.sha256((ROOT/'training/evaluation.py').read_bytes()).hexdigest(),
              'note':'Previously observed synthetic holdout; exploratory comparison, not unseen generalization.'}
    if config['adapter']:
        metadata['adapter_sha256']=hashlib.sha256(Path(config['adapter']).read_bytes()).hexdigest()
    (path/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
