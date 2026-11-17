"""Three comparable local LoRA SFT runs; never sends data or weights externally."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.prepare_aihub_ablation import messages
from scripts.train_klue_pilot import load_base
from scripts.train_stateful_smoke import supervised_loss,mean_loss
from training.data import tokenize_example

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/aihub_ablation_v1'
OUTPUT=ROOT/'output/training/aihub_ablation_v1'
SEED=20261105
CONDITIONS=['sns_only','skin_only','mixed']


def load(name):return [json.loads(line) for line in (DATA/name).read_text(encoding='utf-8').splitlines() if line]


def emit(path,event,**kwargs):
    record={'event':event,**kwargs}
    with path.open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(event,kwargs,flush=True)


def main():
    import torch
    from peft import LoraConfig,get_peft_model,PeftModel,get_peft_model_state_dict,set_peft_model_state_dict
    parser=argparse.ArgumentParser()
    parser.add_argument('--condition',choices=CONDITIONS)
    parser.add_argument('--preflight',action='store_true')
    args=parser.parse_args()
    if args.preflight == bool(args.condition):raise ValueError('Choose --preflight or --condition')
    if not torch.cuda.is_available():raise RuntimeError('CUDA is required')
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name,sha in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=sha:raise ValueError('Data hash mismatch: '+name)
    config={'seed':SEED,'lora_r':8,'lora_alpha':16,'lora_dropout':0.05,
            'target_modules':['q_proj','v_proj'],'lr':0.0002,'optimizer_steps':1000,
            'gradient_accumulation':2,'examples_per_condition':2000,'max_length':2048,
            'checkpoint_every_steps':50,'gradient_checkpointing':True,
            'model_repo':'unsloth/Qwen3-4B-Instruct-2507-bnb-4bit',
            'model_revision':'f12db89cd5156e090618dded9b4367f23f8f3b33',
            'dataset_manifest_sha256':hashlib.sha256((DATA/'manifest.json').read_bytes()).hexdigest(),
            'data_prepare_script_sha256':hashlib.sha256((ROOT/'scripts/prepare_aihub_ablation.py').read_bytes()).hexdigest(),
            'train_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'loss_script_sha256':hashlib.sha256((ROOT/'scripts/train_stateful_smoke.py').read_bytes()).hexdigest(),
            'tokenization_script_sha256':hashlib.sha256((ROOT/'training/data.py').read_bytes()).hexdigest()}
    OUTPUT.mkdir(parents=True,exist_ok=True)
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    model,tokenizer,dtype=load_base()
    model=get_peft_model(model,LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,
                        target_modules=['q_proj','v_proj'],bias='none',task_type='CAUSAL_LM'))
    params=[p for p in model.parameters() if p.requires_grad]
    def convert(row):
        return tokenize_example(tokenizer,{'id':row['id'],'scenario_id':row['source_id'],'category':row['id'].split('-')[0],
            'messages':messages(row),'tools':[]},max_length=config['max_length'])
    if args.preflight:
        all_rows=load('sns_only.jsonl')+load('skin_only.jsonl')
        longest=max(all_rows,key=lambda r:r['token_count'])
        largest=max(all_rows,key=lambda r:r['target_tokens'])
        model.train();model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
        model.enable_input_require_grads();model.config.use_cache=False
        torch.cuda.reset_peak_memory_stats()
        for row in {r['id']:r for r in [longest,largest]}.values():
            model.zero_grad(set_to_none=True);loss=supervised_loss(model,convert(row),dtype)
            if not torch.isfinite(loss):raise ValueError('Non-finite preflight loss')
            loss.backward();del loss
        report={'gpu':torch.cuda.get_device_name(0),'max_sequence_tokens':longest['token_count'],
                'max_target_tokens':largest['target_tokens'],'peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated(),
                'peak_cuda_reserved_bytes':torch.cuda.max_memory_reserved(),'finite_loss':True,
                'note':'Two worst-case examples; not proof against all runtime OOM conditions.'}
        (OUTPUT/'preflight.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2),flush=True);return
    name=args.condition
    config['condition']=name
    run=OUTPUT/name;run.mkdir(exist_ok=True)
    checkpoint=run/'checkpoint.pt';done=run/'comparison.json';meta=run/'metadata.json';log=run/'progress.jsonl'
    if done.exists():raise FileExistsError('This run is complete; refusing to overwrite it')
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    if meta.exists():
        if json.loads(meta.read_text(encoding='utf-8'))['fingerprint']!=fingerprint:raise ValueError('Existing run config differs')
    else:
        meta.write_text(json.dumps({'fingerprint':fingerprint,'config':config,'gpu':torch.cuda.get_device_name(0),
                                   'torch':torch.__version__},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=load(name+'.jsonl')
    if len(rows)!=2000:raise ValueError('Every condition must contain exactly 2000 examples')
    examples=[convert(row) for row in rows]
    val={k:[convert(r) for r in load(k+'_validation.jsonl')] for k in ['sns','skin']}
    optim=torch.optim.AdamW(params,lr=config['lr'],weight_decay=0,foreach=False)
    order=list(range(2000));random.Random(SEED).shuffle(order)
    cursor=0;step=0;before=None;past_seconds=0.0
    if checkpoint.exists():
        saved=torch.load(checkpoint,map_location='cpu',weights_only=False)
        if saved['fingerprint']!=fingerprint:raise ValueError('Checkpoint configuration differs')
        set_peft_model_state_dict(model,saved['adapter']);optim.load_state_dict(saved['optimizer'])
        cursor=saved['cursor'];step=saved['step'];before=saved['validation_before'];past_seconds=saved['training_seconds']
        torch.set_rng_state(saved['torch_rng']);torch.cuda.set_rng_state_all(saved['cuda_rng'])
        emit(log,'resumed',step=step,cursor=cursor)
    else:
        with model.disable_adapter(): before={k:mean_loss(model,v,dtype) for k,v in val.items()}
        emit(log,'validation_before',**before)
    model.train();model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.enable_input_require_grads();model.config.use_cache=False
    optim.zero_grad(set_to_none=True);start=time.perf_counter();torch.cuda.reset_peak_memory_stats()
    while cursor<len(examples):
        losses=[]
        for _ in range(2):
            loss=supervised_loss(model,examples[order[cursor]],dtype);cursor+=1
            if not torch.isfinite(loss):raise ValueError('Non-finite loss')
            (loss/2).backward();losses.append(float(loss.detach()));del loss
        torch.nn.utils.clip_grad_norm_(params,1.0);optim.step();optim.zero_grad(set_to_none=True);step+=1
        if step==1 or step%10==0:
            emit(log,'train_step',step=step,examples=cursor,loss=round(sum(losses)/len(losses),5),
                 seconds=round(past_seconds+time.perf_counter()-start,1),peak_cuda_gib=round(torch.cuda.max_memory_allocated()/1024**3,3))
        if step%config['checkpoint_every_steps']==0 or cursor==len(examples):
            state={'fingerprint':fingerprint,'adapter':get_peft_model_state_dict(model),'optimizer':optim.state_dict(),
                   'cursor':cursor,'step':step,'validation_before':before,
                   'training_seconds':past_seconds+time.perf_counter()-start,
                   'torch_rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all()}
            temporary=checkpoint.with_suffix('.partial');torch.save(state,temporary);os.replace(temporary,checkpoint)
            emit(log,'checkpoint',step=step,examples=cursor)
    train_seconds=past_seconds+time.perf_counter()-start
    model.gradient_checkpointing_disable();model.config.use_cache=True
    after={k:mean_loss(model,v,dtype) for k,v in val.items()}
    adapter=ROOT/'adapters'/('aihub-ablation-v1-'+name)
    if adapter.exists():raise FileExistsError('Adapter path exists; refusing to overwrite')
    adapter.mkdir(parents=True)
    model.save_pretrained(str(adapter),safe_serialization=True,save_embedding_layers=False)
    # A deterministic forward loss is checked before and after a completely fresh model reload.
    reference=mean_loss(model,[val['sns'][0]],dtype)
    del model,optim,params;gc.collect();torch.cuda.empty_cache()
    model,tokenizer,dtype=load_base()
    model=PeftModel.from_pretrained(model,str(adapter),is_trainable=False)
    model.gradient_checkpointing_disable();model.config.use_cache=True
    reloaded=mean_loss(model,[val['sns'][0]],dtype)
    if abs(reference-reloaded)>1e-5:raise ValueError('Reloaded adapter did not reproduce validation loss')
    report={'condition':name,'examples':len(examples),'optimizer_steps':step,'validation_before':before,'validation_after':after,
            'training_seconds':train_seconds,'adapter_path':str(adapter.relative_to(ROOT)),
            'adapter_sha256':hashlib.sha256((adapter/'adapter_model.safetensors').read_bytes()).hexdigest(),
            'reload_loss_equal':True,'reload_reference':reference,'reload_actual':reloaded,'config':config}
    done.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit(log,'complete',validation_after=after,reload_loss_equal=True)


if __name__=='__main__':main()
