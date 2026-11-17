"""Compare Qwen3 backend parity and checkpoint behavior on validation scenarios only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training.data import verify_freeze
from training.evaluation import evaluate

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/runs'
PAIRS={'base':None,'stateful25':'agent-audit-v1-stateful-step25',
       'stateful50':'agent-audit-v1-stateful-step50','stateful100':'agent-audit-v1-stateful-step100',
       'mixed100':'agent-audit-v1-mixed-step100','aihubmixed':'aihub-ablation-v1-mixed'}

def cases():
    verify_freeze(ROOT)
    path=ROOT/'data/stateful/agent_audit_validation_v1'
    raw=(path/'cases.json').read_bytes()
    manifest=json.loads((path/'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256']:raise ValueError('Corrected validation changed')
    return json.loads(raw)

def subset(all_cases):
    picked=[];seen=set()
    for case in all_cases:
        if case['category'] not in seen:
            seen.add(case['category']);picked.append(case)
        if len(picked)==6:break
    return picked

def ps(script,*args):
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)

def health():
    for _ in range(60):
        try:
            with urllib.request.urlopen('http://127.0.0.1:18081/health',timeout=3) as r:
                if json.load(r).get('status')=='ok':return
        except Exception:pass
        time.sleep(2)
    raise TimeoutError('No server')

def run_hf():
    import gc
    import torch
    from peft import PeftModel
    from scripts.train_klue_pilot import load_base
    from training.hf_backend import HFClient
    model,tokenizer,dtype=load_base()
    model.gradient_checkpointing_disable();model.config.use_cache=True
    selected=subset(cases());client=None
    for name in ['base','stateful100','aihubmixed']:
        if name=='stateful100':model=PeftModel.from_pretrained(model,str(ROOT/'adapters'/PAIRS[name]),is_trainable=False)
        if name=='aihubmixed':
            # Reload cleanly instead of unload/re-wrap: PEFT config may otherwise persist.
            client=None
            del model
            gc.collect();torch.cuda.empty_cache()
            model,tokenizer,dtype=load_base()
            model.gradient_checkpointing_disable();model.config.use_cache=True
            model=PeftModel.from_pretrained(model,str(ROOT/'adapters'/PAIRS[name]),is_trainable=False)
        path=RUN/f'agent-audit-v1-hf-{name}'
        if path.exists():
            if (path/'results.json').exists():print('skip',path,flush=True);continue
            raise FileExistsError(path)
        client=HFClient(model,tokenizer,max_new_tokens=384)
        result=evaluate(client,selected,path,'audit-hf-'+name,name!='base',model_id='qwen3-4b-instruct-2507',
                       model_description='Qwen3 NF4; deterministic HF generation')
        print('HF result',name,result['passed_scenarios'],'/',len(selected),flush=True)

def run_gguf():
    selected=cases()
    for name,folder in PAIRS.items():
        path=RUN/f'agent-audit-v1-gguf-{name}'
        if path.exists():
            if (path/'results.json').exists():print('skip',path,flush=True);continue
            raise FileExistsError(path)
        args=[]
        if folder:
            adapter=ROOT/'adapters'/folder
            gguf=adapter/'adapter-f32.gguf'
            if not gguf.exists():
                with (adapter/'conversion.log').open('w',encoding='utf-8') as log:
                    subprocess.run([str(ROOT/'.venv-train/Scripts/python.exe'),str(ROOT/'tmp/llama-converter/convert_lora_to_gguf.py'),
                      '--base',str(ROOT/'models/qwen3-4b-instruct-2507/tokenizer'),'--outfile',str(gguf),'--outtype','f32',str(adapter)],
                      cwd=ROOT,check=True,stdout=log,stderr=subprocess.STDOUT)
            args=['-LoraPath',str(gguf.relative_to(ROOT))]
        ps('start_qwen3.ps1',*args)
        try:
            health()
            if folder:
                with urllib.request.urlopen('http://127.0.0.1:18081/lora-adapters',timeout=10) as response:loaded=json.load(response)
                if isinstance(loaded,dict):loaded=loaded.get('data',loaded.get('value',[]))
                if not any(Path(x['path']).resolve()==gguf.resolve() and x['scale']==1.0 for x in loaded):raise ValueError('Wrong adapter')
            result=evaluate(None,selected,path,'audit-gguf-'+name,name!='base',model_id='qwen3-4b-instruct-2507',
                            model_description='Qwen3 Q4_K_M + validated LoRA',base_url='http://127.0.0.1:18081')
            print('GGUF result',name,result['passed_scenarios'],'/',len(selected),flush=True)
        finally:ps('stop_qwen3.ps1')
    ps('start_qwen3.ps1');health()

def summary():
    summaries={}
    for name in PAIRS:
        report=json.loads((RUN/f'agent-audit-v1-gguf-{name}'/'results.json').read_text(encoding='utf-8'))
        summaries[name]={k:report[k] for k in ['scenarios','passed_scenarios','executed_turns','planned_turns','state_exact_turns']}
    parity={}
    for name in ['base','stateful100','aihubmixed']:
        hf=json.loads((RUN/f'agent-audit-v1-hf-{name}'/'results.json').read_text(encoding='utf-8'))
        gguf=json.loads((RUN/f'agent-audit-v1-gguf-{name}'/'results.json').read_text(encoding='utf-8'))
        byid={x['id']:x for x in gguf['results']}; details=[]
        for h in hf['results']:
            g=byid[h['id']]
            details.append({'id':h['id'],'hf_pass':h['passed'],'gguf_pass':g['passed'],
                            'hf_states':[x['result']['state'] for x in h['turns']],
                            'gguf_states':[x['result']['state'] for x in g['turns']],
                            'hf_tools':[[c['name'] for c in x['result']['calls']] for x in h['turns']],
                            'gguf_tools':[[c['name'] for c in x['result']['calls']] for x in g['turns']]})
        parity[name]={'cases':len(details),'same_scenario_pass':sum(x['hf_pass']==x['gguf_pass'] for x in details),
                      'same_states':sum(x['hf_states']==x['gguf_states'] for x in details),
                      'same_tool_names':sum(x['hf_tools']==x['gguf_tools'] for x in details),'details':details}
    trains={name:json.loads((ROOT/f'output/training/agent-audit-v1/{name}/done.json').read_text(encoding='utf-8')) for name in ['stateful','mixed']}
    loss=json.loads((ROOT/'output/qlora_audit_real_loss.json').read_text(encoding='utf-8'))
    report={'validation_scenario_sha256':hashlib.sha256((ROOT/'data/stateful/agent_audit_validation_v1/cases.json').read_bytes()).hexdigest(),
            'warning':'Exploratory synthetic validation, no independent language review; not blind holdout; backends differ in quantization and implementation.',
            'gguf_validation':summaries,'hf_vs_gguf_subset':parity,'training':trains,'real_model_loss_audit':loss}
    (ROOT/'output/agent_audit_v1_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'gguf_validation':summaries,'hf_vs_gguf_subset':parity},ensure_ascii=False,indent=2),flush=True)

def run_final():
    directory=ROOT/'data/stateful/agent_audit_final_v1'
    content=(directory/'cases.json').read_bytes()
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256(content).hexdigest()!=manifest['sha256']:raise ValueError('Final cases changed')
    final_cases=json.loads(content)
    # Selection rule is frozen before final evaluation: best validation scenario count, tie -> earlier step.
    candidates=['stateful25','stateful50','stateful100']
    scores={name:json.loads((RUN/f'agent-audit-v1-gguf-{name}'/'results.json').read_text(encoding='utf-8'))['passed_scenarios'] for name in candidates}
    best=max(candidates,key=lambda x:(scores[x],-int(x.replace('stateful',''))))
    print('checkpoint selection (validation only):',scores,'->',best,flush=True)
    selected=['base',best,'mixed100','aihubmixed']
    selection={'validation_scores':scores,'selected':best,'rule':'max validation passed scenarios, tie earliest',
               'final_sha256':manifest['sha256']}
    selection_path=ROOT/'output/agent_audit_v1_selection.json'
    if selection_path.exists() and json.loads(selection_path.read_text(encoding='utf-8'))!=selection:raise ValueError('Selection changed')
    selection_path.write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
    ps('stop_qwen3.ps1')
    try:
        for name in selected:
            path=RUN/f'agent-audit-v1-final-{name}'
            if path.exists():
                if (path/'results.json').exists():print('skip',path,flush=True);continue
                raise FileExistsError(path)
            folder=PAIRS[name];args=[]
            if folder:args=['-LoraPath',str((Path('adapters')/folder/'adapter-f32.gguf'))]
            ps('start_qwen3.ps1',*args)
            try:
                health()
                if folder:
                    with urllib.request.urlopen('http://127.0.0.1:18081/lora-adapters',timeout=10) as response:loaded=json.load(response)
                    if isinstance(loaded,dict):loaded=loaded.get('data',loaded.get('value',[]))
                    target=(ROOT/'adapters'/folder/'adapter-f32.gguf').resolve()
                    if not any(Path(x['path']).resolve()==target and x['scale']==1.0 for x in loaded):raise ValueError('Wrong adapter')
                result=evaluate(None,final_cases,path,'audit-final-'+name,name!='base',model_id='qwen3-4b-instruct-2507',
                    model_description='Qwen3 Q4_K_M + validated LoRA',base_url='http://127.0.0.1:18081')
                print('final result',name,result['passed_scenarios'],'/',len(final_cases),flush=True)
            finally:ps('stop_qwen3.ps1')
    finally:
        ps('start_qwen3.ps1');health()
    comparison={}
    for name in selected:
        r=json.loads((RUN/f'agent-audit-v1-final-{name}'/'results.json').read_text(encoding='utf-8'))
        comparison[name]={k:r[k] for k in ['scenarios','passed_scenarios','executed_turns','planned_turns','state_exact_turns']}
    (ROOT/'output/agent_audit_v1_final.json').write_text(json.dumps({'selection':selection,'results':comparison,'limitations':manifest['limitations']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(comparison,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['hf','gguf','summary','final']);phase=p.parse_args().phase
    {'hf':run_hf,'gguf':run_gguf,'summary':summary,'final':run_final}[phase]()
