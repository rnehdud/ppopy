"""Controlled Qwen3 stateful-only vs stateful+AI Hub pilot; all data stays local."""
import argparse
import hashlib
import json
import random
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training.data import load_rows,tokenize_example,verify_freeze
from scripts.train_klue_pilot import load_base
from scripts.train_stateful_smoke import supervised_loss,mean_loss,select_stateful_rows
from scripts.prepare_aihub_ablation import messages

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/aihub_ablation_v1'
OUT=ROOT/'output/training/agent-audit-v1'
SEED=20261106

def main():
    import torch
    from peft import LoraConfig,get_peft_model,get_peft_model_state_dict,set_peft_model_state_dict
    p=argparse.ArgumentParser();p.add_argument('--condition',choices=['stateful','mixed'],required=True);args=p.parse_args()
    verify_freeze(ROOT)
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name in ['sns_only.jsonl','skin_only.jsonl']:
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=manifest['files'][name]: raise ValueError('AI Hub hash mismatch')
    condition=args.condition
    run=OUT/condition;run.mkdir(parents=True,exist_ok=True)
    if (run/'done.json').exists():raise FileExistsError('Completed run is preserved')
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    model,tokenizer,dtype=load_base()
    model=get_peft_model(model,LoraConfig(r=8,lora_alpha=16,lora_dropout=.05,target_modules=['q_proj','v_proj'],bias='none',task_type='CAUSAL_LM'))
    raw=load_rows(ROOT/'data/stateful/v2/train.sft.jsonl')
    state=select_stateful_rows(raw,200,SEED)
    if condition=='stateful':rows=state
    else:
        rows=state[:100]
        for src in ['sns','skin']:
            available=load_rows(DATA/(src+'_only.jsonl'))
            for row in available[:50]:
                rows.append({'id':'aihub-'+row['id'],'scenario_id':row['source_id'],'category':'aihub-'+src,
                    'messages':messages(row),'tools':[]})
    if len(rows)!=200:raise ValueError('Expected exactly 200 examples')
    examples=[tokenize_example(tokenizer,r,2048) for r in rows]
    val=[tokenize_example(tokenizer,r,2048) for r in load_rows(ROOT/'data/stateful/v2/validation.sft.jsonl')]
    order=list(range(200));random.Random(SEED).shuffle(order)
    cfg={'seed':SEED,'condition':condition,'examples':200,'stateful':200 if condition=='stateful' else 100,
         'aihub_sns':0 if condition=='stateful' else 50,'aihub_skin':0 if condition=='stateful' else 50,
         'updates':100,'gradient_accumulation':2,'lr':.0002,'lora_r':8,'lora_alpha':16,'lora_dropout':.05,
         'target_modules':['q_proj','v_proj'],'snapshots':[25,50,100],
         'stateful_manifest_sha256':hashlib.sha256((ROOT/'data/stateful/v2/manifest.json').read_bytes()).hexdigest(),
         'aihub_manifest_sha256':hashlib.sha256((DATA/'manifest.json').read_bytes()).hexdigest(),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    fp=hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()
    meta=run/'metadata.json'
    if meta.exists():
        if json.loads(meta.read_text(encoding='utf-8'))['fingerprint']!=fp:raise ValueError('Config mismatch')
    else:meta.write_text(json.dumps({'fingerprint':fp,'config':cfg,'training_ids':[r['id'] for r in rows]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    params=[p for p in model.parameters() if p.requires_grad]
    optimizer=torch.optim.AdamW(params,lr=.0002,weight_decay=0,foreach=False)
    cursor=step=0;history=[]
    saved_path=run/'checkpoint.pt'
    if saved_path.exists():
        saved=torch.load(saved_path,map_location='cpu',weights_only=False)
        if saved['fingerprint']!=fp:raise ValueError('Checkpoint mismatch')
        set_peft_model_state_dict(model,saved['adapter']);optimizer.load_state_dict(saved['optimizer'])
        cursor=saved['cursor'];step=saved['step'];history=saved['history'];torch.set_rng_state(saved['torch_rng']);torch.cuda.set_rng_state_all(saved['cuda_rng'])
        print('resumed',condition,step,flush=True)
    else:
        baseline=mean_loss(model,val,dtype)
        history.append({'step':0,'validation_loss':baseline})
        print('baseline',condition,baseline,flush=True)
    model.train();model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.enable_input_require_grads();model.config.use_cache=False;optimizer.zero_grad(set_to_none=True)
    start=time.perf_counter()
    while step<100:
        losses=[]
        for _ in range(2):
            loss=supervised_loss(model,examples[order[cursor]],dtype);cursor+=1
            if not torch.isfinite(loss):raise ValueError('Non-finite loss')
            (loss/2).backward();losses.append(float(loss.detach()))
        torch.nn.utils.clip_grad_norm_(params,1.0);optimizer.step();optimizer.zero_grad(set_to_none=True);step+=1
        if step%10==0:print(condition,'step',step,'loss',round(sum(losses)/2,4),'sec',round(time.perf_counter()-start),flush=True)
        if step in [25,50,100]:
            model.gradient_checkpointing_disable();model.config.use_cache=True
            validation=mean_loss(model,val,dtype)
            adapter=ROOT/'adapters'/f'agent-audit-v1-{condition}-step{step}'
            if adapter.exists():raise FileExistsError('Snapshot exists: '+str(adapter))
            adapter.mkdir(parents=True);model.save_pretrained(str(adapter),safe_serialization=True,save_embedding_layers=False)
            history.append({'step':step,'examples':cursor,'validation_loss':validation,'adapter':str(adapter.relative_to(ROOT))})
            model.train();model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False});model.config.use_cache=False
            print(condition,'snapshot',step,'validation',validation,flush=True)
        if step%10==0 or step in [25,50,100]:
            checkpoint={'fingerprint':fp,'adapter':get_peft_model_state_dict(model),'optimizer':optimizer.state_dict(),
              'cursor':cursor,'step':step,'history':history,'torch_rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all()}
            tmp=saved_path.with_suffix('.partial');torch.save(checkpoint,tmp);tmp.replace(saved_path)
    (run/'done.json').write_text(json.dumps({'history':history,'config':cfg},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('done',condition,flush=True)

if __name__=='__main__':main()
