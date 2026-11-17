"""Teacher-forced single-turn KLUE state evaluation on local Qwen3 GGUF."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.request
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.prepare_klue_experiment import make_messages

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/klue_wos_pilot_v1'


def load_rows(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phase',required=True,choices=['before','after'])
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    server=json.loads((ROOT/'output/runtime-qwen3/server_config.json').read_text(encoding='utf-8-sig'))
    if bool(server.get('adapter'))!=(args.phase=='after'):
        raise ValueError('Server adapter does not match phase')
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Frozen file changed: '+name)
    rows=load_rows(DATA/'validation_eval.jsonl')
    slots=json.loads((DATA/'slots.json').read_text(encoding='utf-8'))
    dest=ROOT/args.output
    dest.mkdir(parents=True,exist_ok=False)
    results=[]
    t0=time.perf_counter()
    for index,row in enumerate(rows):
        payload={'model':'qwen3-4b-instruct-2507','messages':make_messages(row,slots,False),
                 'temperature':0,'seed':42,'max_tokens':384,'stream':False,'cache_prompt':False}
        req=urllib.request.Request(f'http://127.0.0.1:{server["port"]}/v1/chat/completions',
              data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'})
        start=time.perf_counter(); text=''; error=None; predicted=None
        try:
            with urllib.request.urlopen(req,timeout=180) as response:
                response=json.load(response)
            choice=response['choices'][0]
            text=choice['message'].get('content') or ''
            if choice.get('finish_reason')=='length':
                raise ValueError('truncated_generation')
            predicted=json.loads(text)
            if not isinstance(predicted,dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in predicted.items()):
                raise ValueError('state_must_be_string_map')
            if not set(predicted)<=set(slots):
                raise ValueError('unknown_slot_key')
        except (urllib.error.URLError,TimeoutError,ValueError,KeyError,TypeError) as exc:
            error=str(exc)
            predicted=None
        expected=row['target_state']
        gold=set(expected.items()); pred=set((predicted or {}).items())
        results.append({'id':row['id'],'dialogue_id':row['dialogue_id'],'input':make_messages(row,slots,False)[1]['content'],
                        'expected_state':expected,'predicted_state':predicted,'raw':text,'error':error,
                        'exact':predicted is not None and predicted==expected,
                        'tp':len(gold&pred),'fp':len(pred-gold),'fn':len(gold-pred),
                        'seconds':time.perf_counter()-start})
        if (index+1)%10==0 or index+1==len(rows):
            print(args.phase,'evaluated',index+1,'/',len(rows),flush=True)
    tp=sum(r['tp'] for r in results);fp=sum(r['fp'] for r in results);fn=sum(r['fn'] for r in results)
    report={'phase':args.phase,'n':len(rows),'exact':sum(r['exact'] for r in results),
            'invalid':sum(r['predicted_state'] is None for r in results),'micro_tp':tp,'micro_fp':fp,'micro_fn':fn,
            'micro_f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,
            'seconds':time.perf_counter()-t0,'server':server,'dataset_manifest':manifest,
            'model_manifest':json.loads((ROOT/'models/qwen3-4b-instruct-2507/manifest.json').read_text(encoding='utf-8')),
            'evaluation_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'prompt_script_sha256':hashlib.sha256((ROOT/'scripts/prepare_klue_experiment.py').read_bytes()).hexdigest(),
            'generation':{'temperature':0,'seed':42,'max_tokens':384,'cache_prompt':False},
            'note':'One turn per distinct held-out validation dialogue, using gold previous state; not closed-loop agent evaluation.',
            'results':results}
    if server.get('adapter'):
        report['adapter_sha256']=hashlib.sha256(Path(server['adapter']).read_bytes()).hexdigest()
    (dest/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k in ['phase','n','exact','invalid','micro_f1','seconds']},indent=2),flush=True)


if __name__=='__main__':
    main()
