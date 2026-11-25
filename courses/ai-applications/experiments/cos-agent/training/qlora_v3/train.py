"""Local-only Qwen3 NF4 QLoRA; exact assistant masking, fixed 810/90 split."""
from __future__ import annotations
import argparse,contextlib,hashlib,json,math,os,random,statistics,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1];ROOT=COS.parents[3]
sys.path.insert(0,str(COS))
from common import dump,read_rows,split_and_encode,masked_loss,deterministic_metrics

def tensors(item,device):
    import torch
    ids=torch.tensor([item['input_ids']],device=device)
    return ids,torch.tensor([item['labels']],device=device),torch.ones_like(ids)

def model_load(path,cfg,adapter=None):
    import torch
    from transformers import AutoModelForCausalLM,BitsAndBytesConfig
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training,PeftModel
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype),
        device_map={'':0},dtype=dtype,attn_implementation='sdpa',low_cpu_mem_usage=True)
    if adapter:
        model=PeftModel.from_pretrained(model,adapter,is_trainable=False)
    else:
        model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True,gradient_checkpointing_kwargs={'use_reentrant':False})
        model=get_peft_model(model,LoraConfig(r=cfg['lora_r'],lora_alpha=cfg['lora_alpha'],
            lora_dropout=cfg['lora_dropout'],target_modules=cfg['target_modules'],bias='none',task_type='CAUSAL_LM'))
    # These frozen matrices do not need the fp32 casting performed by PEFT preparation.
    base=model.get_base_model();base.model.embed_tokens.to(dtype);base.lm_head.to(dtype)
    assert not base.lm_head.weight.requires_grad and not base.model.embed_tokens.weight.requires_grad
    model.config.use_cache=False
    return model,dtype

def prepare(cfg,tokenizer,output,dataset):
    rows=read_rows(dataset);train,val,encoded=split_and_encode(rows,tokenizer,cfg['max_seq_length'])
    sample=max((encoded[r['id']] for r in train),key=lambda r:len(r['input_ids']))
    dump(output/'mask_sample.json',{**sample,'supervised_text':tokenizer.decode([x for x in sample['labels'] if x!=-100]),
         'prompt_tokens_masked':sample['prefix_length'],'native_generation_blocks':'{% generation' in tokenizer.chat_template})
    print('MASK_SAMPLE_ROW',sample['id'],'LABELS',sample['labels'],flush=True)
    dump(output/'split_receipt.json',{'dataset_sha256':hashlib.sha256(Path(dataset).read_bytes()).hexdigest(),
        'train_ids':[r['id'] for r in train],'validation_ids':[r['id'] for r in val],
        'train_rows':810,'val_rows':90,'max_tokens':max(len(x['input_ids']) for x in encoded.values()),
        'truncated_rows':0,'family_group_overlap':0,'assistant_mask_verified':True})
    return train,val,encoded

def validate_loss(model,rows,encoded,dtype):
    import torch
    model.eval();total=0.;count=0
    with torch.no_grad(),torch.autocast('cuda',dtype=dtype):
        for row in rows:
            ids,labels,mask=tensors(encoded[row['id']],model.device)
            loss,n=masked_loss(model,ids,labels,mask);total+=loss.item()*n;count+=n
    return total/count

def evaluate(model,tokenizer,rows,encoded,dtype,cfg,out,tag,base=False):
    import torch
    evaluation_started_ms=int(time.time()*1000)
    model.eval();out.mkdir(parents=True,exist_ok=True)
    predictions=out/'predictions.jsonl'
    records=read_rows(predictions) if predictions.exists() else []
    assert [r['row_id'] for r in records]==[r['id'] for r in rows[:len(records)]],'prediction resume IDs differ'
    context=model.disable_adapter() if base else contextlib.nullcontext()
    with context:
        val_loss=validate_loss(model,rows,encoded,dtype)
        with torch.inference_mode(),torch.autocast('cuda',dtype=dtype):
            for index,row in enumerate(rows):
                if index<len(records):continue
                item=encoded[row['id']];prefix=item['input_ids'][:item['prefix_length']]
                ids=torch.tensor([prefix],device=model.device);mask=torch.ones_like(ids)
                torch.cuda.reset_peak_memory_stats();torch.cuda.synchronize();start=time.perf_counter()
                result=model.generate(input_ids=ids,attention_mask=mask,max_new_tokens=cfg['max_new_tokens'],
                    do_sample=False,use_cache=True,logits_to_keep=1,pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id)
                torch.cuda.synchronize();elapsed=time.perf_counter()-start
                completion=result[0,len(prefix):];text=tokenizer.decode(completion,skip_special_tokens=True)
                record={'row_id':row['id'],'mode':row['mode'],'split':row['split'],'text':text,
                    'timestamp_ms':int(time.time()*1000),
                    'generated_tokens':len(completion),'latency_s':elapsed,'peak_allocated_mib':torch.cuda.max_memory_allocated()/2**20,
                    'peak_reserved_mib':torch.cuda.max_memory_reserved()/2**20,'finished_eos':int(completion[-1])==tokenizer.eos_token_id,
                    'metrics':deterministic_metrics(row,text)}
                records.append(record)
                with (out/'predictions.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
                print(json.dumps({'event':'evaluation','tag':tag,'done':index+1,'total':len(rows),'row_id':row['id'],'latency_s':round(elapsed,2)},ensure_ascii=False),flush=True)
    keys=['invalid_citation','kb_citation','distractor_id_citation','solution_missing_citation','hold_instruction_candidate','empty_response']
    counts={k:sum(r['metrics'][k] for r in records) for k in keys}
    hard=sum(any(r['metrics'][k] for k in keys) or bool(r['metrics']['guardrail_flags']) for r in records)
    lat=sorted(r['latency_s'] for r in records)
    summary={'tag':tag,'rows':len(records),'val_token_loss':val_loss,'counts':counts,'deterministic_flagged_rows':hard,
        'evaluation_started_ms':evaluation_started_ms,'evaluation_finished_ms':int(time.time()*1000),
        'solution_rows':sum(r['mode']=='solution' for r in rows),'hold_rows':sum(r['mode']=='hold' for r in rows),
        'distractor_rows':sum(bool(r['distractor_refs']) for r in rows),
        'length_limited_rows':sum(not r['finished_eos'] for r in records),
        'latency_s':{'p50':statistics.median(lat),'p95':lat[math.ceil(len(lat)*.95)-1]},
        'peak_allocated_mib':max(r['peak_allocated_mib'] for r in records),
        'semantic_faithfulness_and_indirect_distractors':'requires actual content review; not certified by regex',
        'generation':{'do_sample':False,'max_new_tokens':cfg['max_new_tokens'],'quantization':'same NF4 backbone'}}
    dump(out/'summary.json',summary);return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default=str(HERE/'config.json'));p.add_argument('--model-path',required=True)
    p.add_argument('--output',required=True);p.add_argument('--dataset',default=str(COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl'))
    p.add_argument('--prepare-only',action='store_true');p.add_argument('--smoke',action='store_true')
    p.add_argument('--evaluate-adapter',help='Evaluate an existing local adapter without training or uploading.')
    p.add_argument('--defer-generation',action='store_true',help='Compute epoch losses here; run all quality generations later on WSL vLLM.')
    a=p.parse_args()
    import torch
    from transformers import AutoTokenizer,get_cosine_schedule_with_warmup
    cfg=json.loads(Path(a.config).read_text(encoding='utf-8'));out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    if out.resolve().is_relative_to(ROOT.resolve()):
        assert out.resolve().is_relative_to((COS/'outputs').resolve()),'model artifacts inside repository must stay under ignored outputs/'
    assert cfg['max_seq_length']>=2048 and cfg['upload_weights'] is False
    random.seed(cfg['seed']);torch.manual_seed(cfg['seed']);torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(a.model_path,local_files_only=True);tokenizer.pad_token=tokenizer.eos_token
    train,val,encoded=prepare(cfg,tokenizer,out,a.dataset)
    dump(out/'config.json',cfg)
    if a.prepare_only:return
    assert torch.cuda.is_available(),'CUDA required'
    model,dtype=model_load(a.model_path,cfg,adapter=a.evaluate_adapter)
    if a.evaluate_adapter:
        evaluate(model,tokenizer,val,encoded,dtype,cfg,out/'evaluation','local-adapter');return
    assert not list(out.glob('epoch-*/adapter_model.safetensors')),'trained checkpoints exist; choose a new output directory'
    assert all('lora_' in name for name,param in model.named_parameters() if param.requires_grad)
    from bitsandbytes.optim import AdamW8bit
    opt=AdamW8bit((p for p in model.parameters() if p.requires_grad),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    dump(out/'environment.json',{'torch':torch.__version__,'gpu':torch.cuda.get_device_name(),
        'cuda':torch.version.cuda,'dtype':str(dtype),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
        'NF4':True,'double_quantization':True,'gradient_checkpointing':True,'upload_executed':False})
    if a.smoke:
        model.train();item=max((encoded[r['id']] for r in train),key=lambda r:len(r['input_ids']))
        ids,labels,mask=tensors(item,model.device);torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
        with torch.autocast('cuda',dtype=dtype):loss,n=masked_loss(model,ids,labels,mask)
        assert torch.isfinite(loss),'nonfinite smoke loss'
        loss.backward();grad=torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip_norm'])
        assert torch.isfinite(grad),'nonfinite smoke gradient'
        opt.step();torch.cuda.synchronize()
        receipt={'row_id':item['id'],'sequence_length':len(item['input_ids']),'assistant_targets':n,'loss':loss.item(),
            'elapsed_s':time.perf_counter()-start,'peak_allocated_mib':torch.cuda.max_memory_allocated()/2**20,
            'peak_reserved_mib':torch.cuda.max_memory_reserved()/2**20,'optimizer_step_executed':True,
            'adapter_saved':False,'full_training_executed':False}
        dump(out/'smoke.json',receipt);print(json.dumps(receipt),flush=True);return
    # Baseline and all epochs see exactly the same 90 development-only rows/settings.
    if a.defer_generation:
        with model.disable_adapter():baseline={'tag':'base','rows':90,'val_token_loss':validate_loss(model,val,encoded,dtype)}
        dump(out/'loss_summaries.json',{'base':baseline,'epochs':[],'generation_backend':'pending WSL vLLM'})
        print(json.dumps({'event':'base_loss',**baseline}),flush=True)
    else:baseline=evaluate(model,tokenizer,val,encoded,dtype,cfg,out/'base','base',base=True)
    steps_per_epoch=math.ceil(len(train)/cfg['gradient_accumulation_steps']);steps=steps_per_epoch*cfg['epochs']
    scheduler=get_cosine_schedule_with_warmup(opt,math.ceil(steps*cfg['warmup_ratio']),steps)
    summaries=[];global_step=0
    for epoch in range(1,cfg['epochs']+1):
        torch.cuda.reset_peak_memory_stats()
        model.train();order=train.copy();random.Random(cfg['seed']+epoch).shuffle(order)
        opt.zero_grad(set_to_none=True);start_epoch=time.perf_counter();loss_total=0.;tokens=0
        for index,row in enumerate(order):
            ids,labels,mask=tensors(encoded[row['id']],model.device)
            group_start=index//cfg['gradient_accumulation_steps']*cfg['gradient_accumulation_steps']
            divisor=min(cfg['gradient_accumulation_steps'],len(order)-group_start)
            with torch.autocast('cuda',dtype=dtype):loss,n=masked_loss(model,ids,labels,mask)
            assert torch.isfinite(loss),row['id']
            (loss/divisor).backward();loss_total+=loss.item()*n;tokens+=n
            if (index+1)%cfg['gradient_accumulation_steps']==0 or index+1==len(order):
                grad=torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip_norm'])
                assert torch.isfinite(grad),'nonfinite gradient'
                opt.step();scheduler.step();opt.zero_grad(set_to_none=True);global_step+=1
                log={'event':'train','epoch':epoch,'microbatches':index+1,'global_step':global_step,
                    'timestamp_ms':int(time.time()*1000),
                    'token_loss_so_far':loss_total/tokens,'lr':scheduler.get_last_lr()[0],
                    'elapsed_epoch_s':time.perf_counter()-start_epoch,
                    'peak_allocated_mib':torch.cuda.max_memory_allocated()/2**20,
                    'peak_reserved_mib':torch.cuda.max_memory_reserved()/2**20}
                with (out/'training_log.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(log)+'\n')
                print(json.dumps(log),flush=True)
        checkpoint=out/f'epoch-{epoch}';model.save_pretrained(checkpoint,safe_serialization=True);tokenizer.save_pretrained(checkpoint)
        summary=({'tag':f'epoch-{epoch}','rows':90,'val_token_loss':validate_loss(model,val,encoded,dtype)} if a.defer_generation
                 else evaluate(model,tokenizer,val,encoded,dtype,cfg,checkpoint/'evaluation',f'epoch-{epoch}'))
        summary['epoch']=epoch;summary['train_token_loss']=loss_total/tokens;summaries.append(summary)
        dump(out/'epoch_summaries.json',summaries)
        if a.defer_generation:dump(out/'loss_summaries.json',{'base':baseline,'epochs':summaries,'generation_backend':'pending WSL vLLM'})
    if a.defer_generation:
        dump(out/'training_complete.json',{'training_executed':True,'optimizer_steps':global_step,
            'generation_evaluation_complete':False,'selection_pending':True,'upload_executed':False})
        print('TRAINING_COMPLETE_GENERATION_PENDING',flush=True);return
    best=min(summaries,key=lambda s:(s['deterministic_flagged_rows'],s['val_token_loss']))
    dump(out/'selection.json',{'checkpoint':f"epoch-{best['epoch']}",'policy':cfg['selection'],'base':baseline,'epochs':summaries,
        'semantic_review_pending':True,'val_internal_used_for_selection':True,'independent_final_test':False,
        'upload_executed':False,'training_executed':True})
    print('TRAINING_COMPLETE',json.dumps({'best_epoch':best['epoch'],'steps':global_step}),flush=True)

if __name__=='__main__':main()
