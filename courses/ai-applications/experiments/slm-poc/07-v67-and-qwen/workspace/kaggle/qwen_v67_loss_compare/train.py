"""Kaggle-only QLoRA reranker experiment. No final-test reader exists."""
import argparse
import contextlib
import gc
import json
import math
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile

from common import (SEED,MODEL_ID,REVISION,WEIGHT_SHA,read,save,sha,read_rows,
                    prepare,encode,epoch_plan,summarize)
from learning import choice_logits
from paired import paired_epoch_plan,plan_hash,row_loss,adapter_fingerprint

def checked_data(root):
    manifest=read(root/'bundle_manifest.json')
    for name,digest in manifest['files'].items():
        path=(root/name).resolve();path.relative_to(root.resolve())
        assert sha(path)==digest, 'Bundle file hash mismatch: '+name
    train=[prepare(r) for r in read_rows(root/'data/train.jsonl')]
    val=[prepare(r) for r in read_rows(root/'data/val.jsonl')]
    assert len(train)==1980 and len(val)==221
    for key in ['id','group_id','scenario_id']:
        assert not ({r[key] for r in train}&{r[key] for r in val}),key+' overlap'
    assert len({r['id'] for r in train+val})==2201
    assert not any('test' in Path(n).name.lower() for n in manifest['files'])
    return manifest,train,val

def pack(out, bundle_sha):
    result=out.parent/(out.name+'-results.zip')
    files={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*')
           if p.is_file() and not p.name.endswith('.tmp') and p.name!='worker.stdout.log'}
    # The log is concurrently appended by the launcher; include it without a
    # resume hash so restoration never trusts a moving file's stale digest.
    marker={'bundle_sha256':bundle_sha,'files':files,
            'artifact_type':'training-or-evaluation-output' if (out/'baseline/summary.json').exists() else 'setup-diagnostics',
            'test_used':False}
    tmp=result.with_suffix('.zip.tmp')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for name in files:z.write(out/name,name)
        log=out/'worker.stdout.log'
        if log.exists():z.write(log,'worker.stdout.log')
        z.writestr('qwen-v67-resume.json',json.dumps(marker,indent=2))
    tmp.replace(result)
    print('SAVE OUTPUT:',result,'bytes:',result.stat().st_size,flush=True)

def run(args):
    root=args.root.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    manifest,train,val=checked_data(root)
    assert args.out.name==args.objective
    config=read(root/'config.json');selected50=set(read(root/'data/previous50.json')['ids'])
    assert len(selected50)==50 and selected50<={r['id'] for r in val}
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(root/'tokenizer',local_files_only=True,trust_remote_code=False)
    tokenized={}
    lengths={}
    for split,rows in [('train',train),('val',val)]:
        values=[]
        for item in rows:
            inputs=[encode(tokenizer,item,j) for j in range(len(item['candidates']))]
            assert all(len(x)<=config['max_length'] for x in inputs), 'No truncation permitted: '+item['id']
            tokenized[item['id']]=inputs;values.extend(map(len,inputs))
        lengths[split]={'rows':len(rows),'candidate_pairs':len(values),'min':min(values),'max':max(values),'all_fit':True}
    save(out/'lengths.json',lengths)
    if args.verify_only:
        print(json.dumps({'verified':True,'lengths':lengths,'train_pairs_per_epoch':[len(paired_epoch_plan(train,e)) for e in range(1,config['epochs']+1)],'test_read':False},indent=2));return
    import torch
    import peft
    import transformers
    import bitsandbytes
    from transformers import AutoModelForCausalLM,BitsAndBytesConfig,get_linear_schedule_with_warmup
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training,PeftModel
    from torch.nn.attention import sdpa_kernel,SDPBackend
    import transformers.integrations.sdpa_attention as sdpa_integration
    sdpa_integration.use_gqa_in_sdpa=lambda attention_mask,key:False
    if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable. Set Kaggle Accelerator to GPU T4 x2; no CPU fallback.')
    assert 0<=args.gpu<torch.cuda.device_count()
    torch.cuda.set_device(args.gpu);torch.cuda.init();torch.set_num_threads(2);torch.manual_seed(SEED);torch.cuda.manual_seed(SEED);random.seed(SEED)
    save(out/'runtime.json',{'python':sys.version,'torch':torch.__version__,'torch_cuda':torch.version.cuda,
        'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__,
        'gpu':torch.cuda.get_device_name(args.gpu),'gpu_total_mib':torch.cuda.get_device_properties(args.gpu).total_memory/2**20,
        'CUDA_VISIBLE_DEVICES':os.environ.get('CUDA_VISIBLE_DEVICES'),'seed':SEED,
        'quantization':'NF4 double quantization; float16 computation, trainable LoRA only',
        'attention':'EFFICIENT_ATTENTION SDPA, Transformers built-in repeat_kv branch',
        'objective':args.objective,'assigned_gpu_index':args.gpu,'test_used':False})
    from huggingface_hub import snapshot_download
    model_path=Path(snapshot_download(MODEL_ID,revision=REVISION,
        allow_patterns=['config.json','model.safetensors']))
    assert sha(model_path/'model.safetensors')==WEIGHT_SHA
    save(out/'model-source.json',{'id':MODEL_ID,'revision':REVISION,'weight_sha256':WEIGHT_SHA})
    bundle_sha=sha(root/'bundle_manifest.json')
    identity={'bundle_sha256':bundle_sha,'config':config,'objective':args.objective,
              'paired_plan_hashes':{str(e):plan_hash(paired_epoch_plan(train,e)) for e in range(1,config['epochs']+1)},'train_file_sha':sha(root/'data/train.jsonl'),
              'val_file_sha':sha(root/'data/val.jsonl'),'worker_sha':sha(Path(__file__))}
    if (out/'identity.json').exists():assert read(out/'identity.json')==identity,'Refusing incompatible resume'
    save(out/'identity.json',identity)
    last=read(out/'last_checkpoint.json') if (out/'last_checkpoint.json').exists() else None
    checkpoint=out/last['path'] if last else None
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForCausalLM.from_pretrained(model_path,quantization_config=quant,torch_dtype=torch.float16,
         device_map={'':args.gpu},attn_implementation='sdpa',local_files_only=True,trust_remote_code=False)
    base.config.use_cache=False
    base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=True,
        gradient_checkpointing_kwargs={'use_reentrant':False})
    if checkpoint:model=PeftModel.from_pretrained(base,checkpoint/'adapter',is_trainable=True)
    else:model=get_peft_model(base,LoraConfig(task_type='CAUSAL_LM',r=config['lora_r'],lora_alpha=config['lora_alpha'],
                       lora_dropout=config['lora_dropout'],target_modules='all-linear',bias='none'))
    model.peft_config['default'].base_model_name_or_path=MODEL_ID
    model.peft_config['default'].revision=REVISION
    if checkpoint is None:
        save(out/'initial-adapter.json',{'sha256_fp32_trainable_tensors':adapter_fingerprint(model)})
    else:assert (out/'initial-adapter.json').exists(),'Missing initial adapter identity on resume'
    tokenizer.save_pretrained(out/'tokenizer')
    assert all('lora_' in name for name,p in model.named_parameters() if p.requires_grad)
    save(out/'trainable-parameters.json',{'trainable':sum(p.numel() for p in model.parameters() if p.requires_grad),
          'all_parameters_reported':sum(p.numel() for p in model.parameters()),'names':[n for n,p in model.named_parameters() if p.requires_grad]})
    no=tokenizer.convert_tokens_to_ids('no');yes=tokenizer.convert_tokens_to_ids('yes')
    assert no!=yes and tokenizer.encode('no',add_special_tokens=False)==[no] and tokenizer.encode('yes',add_special_tokens=False)==[yes]
    def forward(ids):
        x=torch.tensor([ids],device='cuda')
        # No labels/input-token LM loss: only the final yes/no logits are used.
        with sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION),torch.autocast('cuda',dtype=torch.float16):
            return choice_logits(model,x,no,yes)
    def evaluate(label,disable_adapter=False):
        folder=out/label;folder.mkdir(parents=True,exist_ok=True)
        if (folder/'summary.json').exists():return read(folder/'summary.json')
        records=[];model.eval()
        with (model.disable_adapter() if disable_adapter else contextlib.nullcontext()),torch.inference_mode():
            for index,item in enumerate(val,1):
                path=folder/'cases'/(item['id']+'.json')
                if path.exists():records.append(read(path));continue
                r={'id':item['id'],'gold':item['gold'],'candidate_n':len(item['candidates']),
                   'pair_correct':False,'action_correct':False,'selected':None}
                torch.cuda.synchronize();t=time.perf_counter()
                try:
                    scores=[]
                    for candidate,ids in zip(item['candidates'],tokenized[item['id']]):
                        logits=forward(ids).cpu().tolist()
                        score=logits[1]-logits[0]
                        assert math.isfinite(score)
                        scores.append({**{k:candidate[k] for k in ['action','target_id']},'score':score,'no_logit':logits[0],'yes_logit':logits[1],'tokens':len(ids)})
                        torch.cuda.empty_cache()
                    best=max(scores,key=lambda x:x['score']);selected={k:best[k] for k in ['action','target_id']}
                    r.update(scores=scores,selected=selected,pair_correct=selected==item['gold'],action_correct=selected['action']==item['gold']['action'])
                except torch.OutOfMemoryError as e:
                    r['error']=type(e).__name__+': '+str(e);torch.cuda.empty_cache()
                torch.cuda.synchronize();r['seconds']=time.perf_counter()-t
                save(path,r);records.append(r)
                if index%20==0:print(label,index,'/221','correct',sum(x['pair_correct'] for x in records),flush=True)
        answer=summarize(records,selected50);save(folder/'summary.json',answer);pack(out,bundle_sha)
        print('EVALUATION',label,json.dumps(answer),flush=True);return answer
    baseline=evaluate('baseline',disable_adapter=True)
    if not (out/'best.json').exists():save(out/'best.json',{'epoch':0,'correct':baseline['correct'],'n':221,'adapter':None,'label':'baseline'})
    plans={epoch:paired_epoch_plan(train,epoch) for epoch in range(1,config['epochs']+1)}
    steps_per_epoch={e:math.ceil(len(p)/config['rows_per_update']) for e,p in plans.items()}
    total_steps=sum(steps_per_epoch.values())
    optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=config['learning_rate'],weight_decay=0.01)
    scheduler=get_linear_schedule_with_warmup(optimizer,math.ceil(total_steps*0.05),total_steps)
    scaler=torch.amp.GradScaler('cuda')
    epoch=1;cursor=0;step=0
    if checkpoint:
        state=torch.load(checkpoint/'trainer.pt',map_location='cpu',weights_only=True)
        optimizer.load_state_dict(state['optimizer']);scheduler.load_state_dict(state['scheduler']);scaler.load_state_dict(state['scaler'])
        epoch=state['epoch'];cursor=state['cursor'];step=state['step']
        random.setstate(state['python_rng']);torch.set_rng_state(state['torch_rng']);torch.cuda.set_rng_state(state['cuda_rng_current'])
        print('RESUME epoch',epoch,'cursor',cursor,'optimizer step',step,flush=True)
    def checkpoint_now(epoch,cursor):
        folder=out/'checkpoints'/f'step-{step:06d}'
        folder.mkdir(parents=True,exist_ok=True);model.save_pretrained(folder/'adapter',safe_serialization=True)
        state={'epoch':epoch,'cursor':cursor,'step':step,'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
               'scaler':scaler.state_dict(),'python_rng':random.getstate(),'torch_rng':torch.get_rng_state(),'cuda_rng_current':torch.cuda.get_rng_state()}
        torch.save(state,folder/'trainer.pt.tmp');(folder/'trainer.pt.tmp').replace(folder/'trainer.pt')
        save(out/'last_checkpoint.json',{'path':folder.relative_to(out).as_posix(),'epoch':epoch,'cursor':cursor,'step':step})
        # Keep two complete resume checkpoints, not many copies of optimizer
        # tensors. Epoch-best adapters are outside this directory and retained.
        checkpoint_root=(out/'checkpoints').resolve()
        saved=sorted([p for p in checkpoint_root.iterdir() if p.is_dir() and not p.is_symlink()
                      and re.fullmatch(r'step-\d{6}',p.name) and (p/'trainer.pt').is_file()])
        for stale in saved[:-2]:
            stale.resolve().relative_to(checkpoint_root)
            assert stale.resolve()!=checkpoint_root and stale.resolve()!=folder.resolve()
            shutil.rmtree(stale)
        pack(out,bundle_sha)
    train_started=time.perf_counter()
    session_start_step=step
    for current_epoch in range(epoch,config['epochs']+1):
        plan=plans[current_epoch];start=cursor if current_epoch==epoch else 0
        assert start==len(plan) or start%config['rows_per_update']==0
        model.train()
        for group_start in range(start,len(plan),config['rows_per_update']):
            if time.time()>=args.deadline:
                checkpoint_now(current_epoch,group_start)
                save(out/'status.json',{'status':'partial_time_budget','epoch':current_epoch,'cursor':group_start,'step':step,'test_used':False})
                return
            group=plan[group_start:group_start+config['rows_per_update']]
            optimizer.zero_grad(set_to_none=True);loss_sum=0.0
            for row_index,positive_index,negative_index in group:
                choices=tokenized[train[row_index]['id']]
                positive_logits=forward(choices[positive_index])
                negative_logits=forward(choices[negative_index]) if negative_index is not None else None
                loss=row_loss(positive_logits,negative_logits,args.objective)
                if not torch.isfinite(loss):raise RuntimeError('Non-finite training loss; abort instead of silently skipping')
                loss_sum+=float(loss.detach())
                # Checkpoint recomputation must use the same attention backend.
                with sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION):scaler.scale(loss/len(group)).backward()
            scaler.unscale_(optimizer);torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.0)
            old_scale=scaler.get_scale();scaler.step(optimizer);scaler.update()
            applied=scaler.get_scale()>=old_scale
            if applied:scheduler.step()
            step+=1;cursor=group_start+len(group)
            progress={'epoch':current_epoch,'epochs':config['epochs'],'rows_completed_this_epoch':cursor,'rows_this_epoch':len(plan),
                'optimizer_groups':step,'total_groups':total_steps,'loss_last_group':loss_sum/len(group),
                'optimizer_step_applied':applied,'amp_scale':scaler.get_scale(),'seconds_training_loop':time.perf_counter()-train_started}
            # Use this session's measured rate, including checkpoint/evaluation
            # time already incurred. Future validation and ZIP time are unknown.
            completed_here=step-session_start_step
            if completed_here>=5:
                remaining_seconds=max(0,(time.perf_counter()-train_started)/completed_here*(total_steps-step))
                from datetime import datetime,timezone,timedelta
                finish=datetime.now(timezone.utc)+timedelta(seconds=remaining_seconds)
                progress['estimated_remaining_training_seconds']=round(remaining_seconds)
                progress['estimated_training_finish_utc']=finish.isoformat(timespec='seconds')
                progress['estimated_training_finish_korea_japan']=finish.astimezone(timezone(timedelta(hours=9))).isoformat(timespec='seconds')
                progress['eta_scope']='Training estimate only; future validation, checkpoint and final ZIP time may extend completion.'
            save(out/'progress.json',progress)
            with (out/'training-history.jsonl').open('a',encoding='utf8') as log:log.write(json.dumps(progress)+'\n')
            if step%10==0:print('TRAIN',current_epoch,'rows',cursor,'/',len(plan),'group',step,'/',total_steps,'loss',round(loss_sum/len(group),4),'ETA Korea/Japan',progress.get('estimated_training_finish_korea_japan','calculating'),'remaining minutes',round(progress.get('estimated_remaining_training_seconds',0)/60,1),'(validation and final save not included)',flush=True)
            if step%config['save_every_groups']==0:checkpoint_now(current_epoch,cursor)
        checkpoint_now(current_epoch,len(plan))
        result=evaluate(f'epoch-{current_epoch:02d}')
        best=read(out/'best.json')
        if result['correct']>best['correct']:
            folder=out/f'epoch-{current_epoch:02d}'/'adapter';model.save_pretrained(folder,safe_serialization=True)
            save(out/'best.json',{'epoch':current_epoch,'correct':result['correct'],'n':221,'adapter':folder.relative_to(out).as_posix(),'label':f'epoch-{current_epoch:02d}'})
        cursor=0
    model.save_pretrained(out/'final_adapter',safe_serialization=True)
    best=read(out/'best.json')
    result={'baseline':baseline,'epochs':{str(e):read(out/f'epoch-{e:02d}/summary.json') for e in plans},
            'best':best,'improved_on_val':best['correct']>baseline['correct'],
            'val_exceeds_90_percent':best['correct']*10>9*221,
            'claim_scope':'Internal synthetic val label equality only. Not final-test accuracy, tool arguments, tool execution or clinical truth.',
            'objective':args.objective,'previous170_is_not_this_control':True,'test_used':False}
    save(out/'comparison.json',result)
    save(out/'status.json',{'status':'completed','test_used':False,'trained_adapter_saved':True,'best_epoch':best['epoch']})
    print('COMPLETED',json.dumps(result),flush=True)
    del model,base;gc.collect();torch.cuda.empty_cache()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--objective',choices=['pointwise','relative'],default='pointwise');parser.add_argument('--gpu',type=int,default=0)
    parser.add_argument('--verify-only',action='store_true');parser.add_argument('--deadline',type=float,default=float('inf'))
    args=parser.parse_args()
    try:run(args)
    except Exception as error:
        save(args.out/'error.json',{'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'completed':False})
        raise
    finally:
        if not args.verify_only and (args.root/'bundle_manifest.json').exists():pack(args.out,sha(args.root/'bundle_manifest.json'))

if __name__=='__main__':main()
