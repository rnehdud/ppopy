def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    os.replace(tmp,path)


def read_jsonl(path):
    raw=Path(path).read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw,'UTF-8(BOM 없음), LF 파일이 필요해요.'
    return [json.loads(l) for l in raw.decode('utf-8').splitlines() if l.strip()]


def verify_package(root):
    root=Path(root).resolve();manifest=json.loads((root/'bundle_manifest.json').read_text(encoding='utf-8'))
    assert manifest['format']=='ppopy-kaggle-qlora-5epoch-v1'
    for name,expected in manifest['files'].items():
        path=(root/name).resolve();assert path.is_relative_to(root)
        assert sha256(path)==expected,(name,'파일 SHA-256이 달라요.')
    full=read_jsonl(root/'data/full_900.jsonl');train=read_jsonl(root/'data/train.jsonl');val=read_jsonl(root/'data/val.jsonl')
    assert (len(full),len(train),len(val))==(900,810,90)
    assert train==[r for r in full if r['split']=='train']
    assert val==[r for r in full if r['split']=='val_internal']
    assert len({r['id'] for r in full})==900
    for field in ['id','group_id','scenario_family_id']:
        assert not ({r[field] for r in train}&{r[field] for r in val}),field+' 누수가 있어요.'
    for row in full:
        assert row['provenance']['source_origin']=='new_synthetic'
        assert row['mode'] in {'solution','hold'}
        assert [m['role'] for m in row['messages']]==['system','user','assistant']
        request=json.loads(row['messages'][1]['content'])
        assert 'kb_judgments' not in request and '[kb:' not in row['messages'][2]['content'].lower()
    return train,val,manifest


def encode(row,tokenizer,max_length):
    # Qwen 네이티브 template에 generation 블록이 없어도 정확한 prefix 경계로 마스킹해요.
    ids=tokenizer.apply_chat_template(row['messages'],tokenize=True,add_generation_prompt=False)
    prefix=tokenizer.apply_chat_template(row['messages'][:-1],tokenize=True,add_generation_prompt=True)
    assert ids[:len(prefix)]==prefix,(row['id'],'chat prefix 불일치')
    assert len(prefix)<len(ids)<=max_length,(row['id'],len(ids),'잘라 학습하지 않아요.')
    labels=[-100]*len(prefix)+ids[len(prefix):]
    return {'id':row['id'],'input_ids':ids,'labels':labels,'prefix_length':len(prefix),
            'assistant_tokens':len(ids)-len(prefix)}


def prepare_rows(train,val,tokenizer,cfg,out):
    encoded={r['id']:encode(r,tokenizer,cfg['max_seq_length']) for r in train+val}
    longest=max((encoded[r['id']] for r in train),key=lambda x:len(x['input_ids']))
    write_json(Path(out)/'mask_sample.json',{**longest,
        'supervised_text':tokenizer.decode([v for v in longest['labels'] if v!=-100]),
        'all_prompt_labels_minus_100':all(v==-100 for v in longest['labels'][:longest['prefix_length']])})
    receipt={'train_rows':len(train),'val_rows':len(val),'train_ids':[r['id'] for r in train],
        'val_ids':[r['id'] for r in val],'max_tokens':max(len(v['input_ids']) for v in encoded.values()),
        'truncated_rows':0,'overlapping_groups':0,'overlapping_families':0}
    write_json(Path(out)/'tokenization_and_split.json',receipt)
    print(json.dumps({'mask_row':longest['id'],'masked_prompt_tokens':longest['prefix_length'],
        'assistant_targets':longest['assistant_tokens'],'max_tokens':receipt['max_tokens']}),flush=True)
    return encoded


def choose_dtype(setting='auto'):
    # T4/P100처럼 native BF16이 없는 GPU에서는 FP16 + GradScaler를 사용해요.
    native_bf16=torch.cuda.get_device_capability(0)[0]>=8 and torch.cuda.is_bf16_supported()
    if setting=='bf16':assert native_bf16,'이 GPU는 native BF16을 지원하지 않아요.'
    return torch.bfloat16 if setting=='bf16' or (setting=='auto' and native_bf16) else torch.float16


def load_model(source,cfg,dtype,cache_dir=None,adapter=None):
    from transformers import AutoModelForCausalLM,BitsAndBytesConfig
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training,PeftModel
    local=__import__('pathlib').Path(source).is_dir()
    model=AutoModelForCausalLM.from_pretrained(source,revision=None if local else cfg['model_revision'],
        cache_dir=cache_dir,local_files_only=local,device_map={'':0},dtype=dtype,
        attn_implementation='sdpa',quantization_config=BitsAndBytesConfig(load_in_4bit=True,
        bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype))
    model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True,
        gradient_checkpointing_kwargs={'use_reentrant':False})
    if adapter:model=PeftModel.from_pretrained(model,str(adapter),is_trainable=True)
    else:model=get_peft_model(model,LoraConfig(r=cfg['lora_r'],lora_alpha=cfg['lora_alpha'],
        lora_dropout=cfg['lora_dropout'],target_modules=cfg['target_modules'],bias='none',task_type='CAUSAL_LM'))
    base=model.get_base_model()
    # PEFT의 FP32 준비 후 큰 frozen embedding/head만 compute dtype으로 되돌려 메모리를 절약해요.
    base.model.embed_tokens.to(dtype);base.lm_head.to(dtype);model.config.use_cache=False
    assert all('lora_' in n for n,p in model.named_parameters() if p.requires_grad)
    return model


def autocast(device,dtype):
    return torch.autocast('cuda',dtype=dtype) if device.type=='cuda' else contextlib.nullcontext()


def tensors(item,device):
    ids=torch.tensor([item['input_ids']],device=device)
    return ids,torch.tensor([item['labels']],device=device),torch.ones_like(ids)


def selected_loss(hidden,labels,head,expected_tokens=None):
    # prompt 위치의 거대한 vocab logits만 생략해요. 표준 CE(ignore_index=-100)와 loss/gradient가 같아요.
    targets=labels[:,1:];valid=targets.ne(-100)
    if expected_tokens is None:assert valid.any()
    logits=head(hidden[:,:-1][valid])
    return torch.nn.functional.cross_entropy(logits.float(),targets[valid]),expected_tokens if expected_tokens is not None else int(valid.sum())


def masked_loss(model,item,device):
    # 검증된 입력 tensor를 재사용해 매 epoch의 반복 CPU→GPU 복사·할당을 줄여요.
    ids,labels,attention=item['_cuda_inputs'] if '_cuda_inputs' in item else tensors(item,device)
    base=model.get_base_model()
    hidden=base.model(input_ids=ids,attention_mask=attention,use_cache=False,return_dict=True).last_hidden_state
    return selected_loss(hidden,labels,base.lm_head,item.get('assistant_tokens'))


def memory(device):
    return {'allocated_mib':torch.cuda.max_memory_allocated()/2**20,
            'reserved_mib':torch.cuda.max_memory_reserved()/2**20} if device.type=='cuda' else None


def check_checkpoint(folder,fingerprint):
    folder=Path(folder).resolve()
    complete=json.loads((folder/'COMPLETE.json').read_text(encoding='utf-8'))
    assert complete['fingerprint']==fingerprint,'데이터·코드·설정이 다른 실험은 이어 붙이지 않아요.'
    for name,digest in complete['files'].items():
        path=(folder/name).resolve();assert path.is_relative_to(folder)
        assert sha256(path)==digest,(name,'checkpoint 손상')
    assert (folder/'adapter_model.safetensors').is_file()
    return complete


def save_checkpoint(out,epoch,model,tokenizer,optimizer,scheduler,scaler,history,context,updates,attempts):
    out=Path(out);target=out/'checkpoints'/f'epoch-{epoch:02d}'
    temporary=target.with_name(target.name+'.incomplete')
    assert not target.exists() and not temporary.exists(),'기존 checkpoint를 덮어쓰지 않아요.'
    temporary.mkdir(parents=True)
    model.save_pretrained(temporary,safe_serialization=True);tokenizer.save_pretrained(temporary)
    # 직접 생성한 팀 checkpoint만 load해요. optimizer/RNG 때문에 일반 weight 파일과 달라요.
    state={'epoch':epoch,'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
        'scaler':scaler.state_dict(),'history':history,'context':context,'updates':updates,'attempts':attempts,
        'python_rng':random.getstate(),'numpy_rng':np.random.get_state(),'torch_rng':torch.get_rng_state(),
        'cuda_rng':torch.cuda.get_rng_state(0) if torch.cuda.is_available() else None}
    torch.save(state,temporary/'training_state.pt')
    write_json(temporary/'metrics.json',history[-1]);write_json(temporary/'context.json',context)
    write_json(temporary/'COMPLETE.json',{'epoch':epoch,'fingerprint':context['fingerprint'],
        'files':{str(p.relative_to(temporary)).replace('\\','/'):sha256(p) for p in temporary.rglob('*') if p.is_file()},
        'full_backbone_included':False,'human_approved':False})
    temporary.rename(target)
    return target


def load_training_state(folder,optimizer,scheduler,scaler,context):
    check_checkpoint(folder,context['fingerprint'])
    state=torch.load(Path(folder)/'training_state.pt',map_location='cpu',weights_only=False)
    assert state['context']['compute_dtype']==context['compute_dtype'],'동일 compute dtype으로 재개해요.'
    optimizer.load_state_dict(state['optimizer']);scheduler.load_state_dict(state['scheduler'])
    if state['scaler']:scaler.load_state_dict(state['scaler'])
    random.setstate(state['python_rng']);np.random.set_state(state['numpy_rng']);torch.set_rng_state(state['torch_rng'])
    if state['cuda_rng'] is not None:torch.cuda.set_rng_state(state['cuda_rng'],0)
    return state


def copy_previous_run(checkpoint,out,fingerprint):
    # 새 output에서만 재개해요. 이전 학습의 checkpoint와 상세 기록도 복사해 전체 5개를 보존해요.
    checkpoint=Path(checkpoint).resolve();out=Path(out).resolve()
    complete=check_checkpoint(checkpoint,fingerprint);previous=checkpoint.parent.parent
    assert checkpoint.parent.name=='checkpoints' and not out.is_relative_to(previous)
    for epoch in range(1,complete['epoch']+1):
        src=previous/'checkpoints'/f'epoch-{epoch:02d}';dst=out/'checkpoints'/src.name
        check_checkpoint(src,fingerprint)
        assert src.resolve().is_relative_to(previous) and dst.resolve().is_relative_to(out)
        shutil.copytree(src,dst)
        old_history=previous/'history'/src.name
        if old_history.exists():shutil.copytree(old_history,out/'history'/src.name)
    return out/'checkpoints'/checkpoint.name


def evaluate(model,rows,encoded,device,dtype,path):
    model.eval();total=0.;tokens=0;start=time.perf_counter()
    temporary=Path(path).with_suffix('.jsonl.incomplete')
    with temporary.open('w',encoding='utf-8',newline='\n') as f,torch.no_grad(),autocast(device,dtype):
        for row in rows:
            loss,n=masked_loss(model,encoded[row['id']],device)
            assert torch.isfinite(loss),row['id']
            total+=float(loss)*n;tokens+=n
            f.write(json.dumps({'row_id':row['id'],'assistant_token_loss':float(loss),'assistant_tokens':n})+'\n')
    temporary.replace(path)
    return total/tokens,tokens,time.perf_counter()-start


def write_history(out,history,cfg,context):
    out=Path(out);write_json(out/'epoch_history.json',history)
    with (out/'epoch_metrics.csv').open('w',encoding='utf-8',newline='') as f:
        keys=[k for k in history[0] if k not in {'train_memory','eval_memory'}]
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(history)
    best=min(history,key=lambda x:x['val_token_loss'])
    write_json(out/'best_by_val_loss.json',{'epoch':best['epoch'],
        'checkpoint':f"checkpoints/epoch-{best['epoch']:02d}",'val_token_loss':best['val_token_loss'],
        'selection_scope':'validation CE only; semantic quality unreviewed','human_approved':False})
    base=next((x for x in history if x['epoch']==3),None);signals=[]
    if base:
        for row in history:
            if row['epoch']>3:
                signals.append({'epoch':row['epoch'],'val_loss_change_vs_epoch3':row['val_token_loss']-base['val_token_loss'],
                    'train_eval_loss_change_vs_epoch3':row['train_eval_token_loss']-base['train_eval_token_loss'],
                    'heuristic_signal':row['val_token_loss']>base['val_token_loss']+cfg['overfit_delta'] and
                        row['train_eval_token_loss']<base['train_eval_token_loss']-cfg['overfit_delta']})
    write_json(out/'overfit_observations.json',{'hypothesis':'epoch > 3 may overfit; not an established fact',
        'delta_threshold':cfg['overfit_delta'],'comparisons':signals,'statistical_test_performed':False,
        'validation_reused_for_selection':True,'independent_test':False})
    write_json(out/'run_status.json',{'completed_epochs':len(history),'target_epochs':cfg['epochs'],
        'training_complete':history[-1]['epoch']==cfg['epochs'],'run_kind':context['run_kind'],
        'model_quality_approved':False,'external_upload_performed':False})
    # 표준 폰트에서 깨지지 않도록 그림 축은 영어, 해설은 한국어 README에 둬요.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.plot([r['epoch'] for r in history],[r['train_eval_token_loss'] for r in history],'o-',label='Train CE (eval mode, full train split)')
    ax.plot([r['epoch'] for r in history],[r['val_token_loss'] for r in history],'o-',label='Validation CE (held-out split)')
    ax.axvline(3,color='gray',linestyle='--',label='Hypothesis boundary, not proven')
    ax.set(xlabel='Epoch',ylabel='Assistant-token cross entropy',xticks=list(range(1,cfg['epochs']+1)))
    ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'loss_curves.png',dpi=160);plt.close(fig)


def run_epochs(model,tokenizer,train,val,encoded,cfg,out,context,optimizer,scheduler,scaler,device,dtype,
               resume=None,stop_after_epoch=None):
    out=Path(out);history=[];updates=0;attempts=0;start_epoch=1
    if resume:
        state=load_training_state(resume,optimizer,scheduler,scaler,context)
        history=state['history'];updates=state['updates'];attempts=state['attempts'];start_epoch=state['epoch']+1
    trainable=[p for p in model.parameters() if p.requires_grad]
    for epoch in range(start_epoch,cfg['epochs']+1):
        folder=out/'history'/f'epoch-{epoch:02d}';folder.mkdir(parents=True)
        if device.type=='cuda':torch.cuda.reset_peak_memory_stats()
        model.train();order=train.copy();random.Random(cfg['seed']+epoch).shuffle(order)
        optimizer.zero_grad(set_to_none=True);total=0.;tokens=0;skipped=0;start=time.perf_counter()
        with (folder/'train_steps.jsonl').open('w',encoding='utf-8',newline='\n') as log:
            for index,row in enumerate(order):
                group=index//cfg['gradient_accumulation_steps']*cfg['gradient_accumulation_steps']
                divisor=min(cfg['gradient_accumulation_steps'],len(order)-group)
                with autocast(device,dtype):loss,n=masked_loss(model,encoded[row['id']],device)
                assert torch.isfinite(loss),row['id']
                scaler.scale(loss/divisor).backward();total+=float(loss.detach())*n;tokens+=n
                if (index+1)%cfg['gradient_accumulation_steps']==0 or index+1==len(order):
                    scaler.unscale_(optimizer)
                    norm=torch.nn.utils.clip_grad_norm_(trainable,cfg['gradient_clip_norm'],error_if_nonfinite=not scaler.is_enabled())
                    previous_scale=scaler.get_scale();scaler.step(optimizer);scaler.update();attempts+=1
                    did_skip=scaler.is_enabled() and scaler.get_scale()<previous_scale
                    if did_skip:skipped+=1
                    else:scheduler.step();updates+=1
                    optimizer.zero_grad(set_to_none=True)
                    record={'epoch':epoch,'microbatches':index+1,'optimizer_attempts':attempts,'optimizer_updates':updates,
                        'fp16_update_skipped':did_skip,'grad_scale':scaler.get_scale(),
                        'grad_norm':float(norm) if torch.isfinite(norm) else None,
                        'running_train_token_loss':total/tokens,'lr':scheduler.get_last_lr()[0],
                        'elapsed_epoch_s':time.perf_counter()-start,'timestamp_ms':int(time.time()*1000)}
                    log.write(json.dumps(record,allow_nan=False)+'\n');log.flush();print(json.dumps(record),flush=True)
        train_seconds=time.perf_counter()-start;train_memory=memory(device)
        if device.type=='cuda':torch.cuda.reset_peak_memory_stats()
        # dropout을 끄고 epoch 말의 같은 가중치로 train 810/val 90을 각각 전수 평가해요.
        train_loss,train_tokens,train_eval_s=evaluate(model,train,encoded,device,dtype,folder/'train_eval_losses.jsonl')
        val_loss,val_tokens,val_s=evaluate(model,val,encoded,device,dtype,folder/'val_losses.jsonl')
        metrics={'epoch':epoch,'online_train_token_loss':total/tokens,'train_eval_token_loss':train_loss,
            'val_token_loss':val_loss,'val_minus_train_eval':val_loss-train_loss,
            'train_rows':len(train),'val_rows':len(val),'train_assistant_tokens':train_tokens,'val_assistant_tokens':val_tokens,
            'optimizer_attempts':attempts,'optimizer_updates':updates,'fp16_skipped_updates_this_epoch':skipped,
            'learning_rate':scheduler.get_last_lr()[0],'train_seconds':train_seconds,
            'train_eval_seconds':train_eval_s,'val_seconds':val_s,'compute_dtype':str(dtype),
            'train_memory':train_memory,'eval_memory':memory(device)}
        history.append(metrics);write_json(folder/'metrics.json',metrics)
        save_checkpoint(out,epoch,model,tokenizer,optimizer,scheduler,scaler,history,context,updates,attempts)
        write_history(out,history,cfg,context)
        print('EPOCH_COMPLETE',json.dumps(metrics),flush=True)
        if stop_after_epoch and epoch>=stop_after_epoch:break
    return history


def main(argv=None,default_package_dir=None,runtime_code_fingerprint=None,runtime_code_snapshot=None):
    # CLI와 Notebook 내장 코드에서 같은 진입점을 사용해요. Notebook에서는 __file__이 필요 없어요.
    default_package_dir=default_package_dir or Path(__file__).resolve().parent
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package-dir',default=str(default_package_dir))
    p.add_argument('--output',required=True);p.add_argument('--config')
    p.add_argument('--cache-dir',default='/tmp/ppopy_hf_cache')
    p.add_argument('--model-path',help='고급/오프라인: 직접 준비한 로컬 원본 모델 폴더')
    p.add_argument('--resume-from',help='이 패키지의 이전 전체 Output 안 checkpoints/epoch-XX')
    p.add_argument('--compute-dtype',choices=['auto','bf16','fp16'])
    p.add_argument('--verify-only',action='store_true');p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--smoke',action='store_true',help='가장 긴 train 1건의 실제 GPU optimizer step만 검사해요.')
    p.add_argument('--stop-after-epoch',type=int,help='세션 분할 시 이번 실행만 N epoch 뒤 정지. 총 목표/scheduler는 여전히 5예요.')
    a=p.parse_args(argv);root=Path(a.package_dir).resolve();out=Path(a.output).resolve()
    train,val,manifest=verify_package(root)
    if a.verify_only:
        print(json.dumps({'package_verified':True,'train':810,'val':90,'group_and_family_overlap':0}));return
    cfg=json.loads(Path(a.config or root/'config.json').read_text(encoding='utf-8'))
    if a.compute_dtype:cfg['compute_dtype']=a.compute_dtype
    assert cfg['epochs']==5 and cfg['max_seq_length']>=2048 and cfg['batch_size']==1
    assert cfg['production_enabled'] is False and cfg['push_to_hub'] is False and cfg['early_stopping'] is False
    assert not out.is_relative_to(root),'읽기 전용 입력 패키지 밖에 결과를 저장해요.'
    if not a.prepare_only:assert not out.exists() or not any(out.iterdir()),'기존 Output을 덮어쓰지 않아요. 새 output 폴더로 실행/재개하세요.'
    out.mkdir(parents=True,exist_ok=True)
    if runtime_code_snapshot is not None:
        (out/'notebook_training_source.py').write_text(runtime_code_snapshot,encoding='utf-8',newline='\n')
    os.environ['HF_HUB_DISABLE_TELEMETRY']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
    os.environ['USE_TF']='0';os.environ['USE_FLAX']='0'  # Torch 전용. TensorFlow의 별도 CUDA 경고와 구분해요.
    import numpy as np
    import torch
    from transformers import AutoTokenizer,get_cosine_schedule_with_warmup
    random.seed(cfg['seed']);np.random.seed(cfg['seed']);torch.manual_seed(cfg['seed'])
    source=a.model_path or cfg['model_id'];local=Path(source).is_dir()
    tokenizer=AutoTokenizer.from_pretrained(source,revision=None if local else cfg['model_revision'],
        cache_dir=a.cache_dir,local_files_only=local)
    tokenizer.pad_token=tokenizer.eos_token
    encoded=prepare_rows(train,val,tokenizer,cfg,out);write_json(out/'config.json',cfg)
    if a.prepare_only:return
    assert torch.cuda.is_available(),'GPU/CUDA가 필요해요. Kaggle Notebook의 Accelerator를 GPU로 설정하세요.'
    assert tuple(int(n) for n in torch.__version__.split('+')[0].split('.')[:2])>=(2,6),'torch>=2.6이 필요해요.'
    dtype=choose_dtype(cfg['compute_dtype']);device=torch.device('cuda:0')
    if cfg.get('cache_inputs_on_gpu',False):
        for item in encoded.values():item['_cuda_inputs']=tensors(item,device)
    cfg_fingerprint={'config':cfg,'manifest_sha256':sha256(root/'bundle_manifest.json'),
                     'model_source':str(Path(source).resolve()) if local else source}
    if runtime_code_fingerprint is not None:cfg_fingerprint['notebook_code_sha256']=runtime_code_fingerprint
    context={'fingerprint':hashlib.sha256(json.dumps(cfg_fingerprint,sort_keys=True).encode()).hexdigest(),
        'bundle_manifest_sha256':cfg_fingerprint['manifest_sha256'],'compute_dtype':str(dtype),
        'execution_mode':'notebook_inline' if runtime_code_fingerprint is not None else 'packaged_python_cli',
        'notebook_code_sha256':runtime_code_fingerprint,
        'run_kind':'one_step_gpu_smoke' if a.smoke else 'qwen3_4b_5epoch_training',
        'model_id':cfg['model_id'],'model_revision':cfg['model_revision'],'local_model_override':local,
        'dataset_sha256':manifest['files']['data/full_900.jsonl'],
        'loss_objective':'mean of per-example assistant-token CE within each accumulation group',
        'validation_role':'development checkpoint selection; not an independent final test'}
    resume=copy_previous_run(a.resume_from,out,context['fingerprint']) if a.resume_from else None
    assert not (a.smoke and resume),'smoke 검사와 학습 재개는 별도 실행해요.'
    model=load_model(source,cfg,dtype,a.cache_dir,resume)
    parameter_devices=sorted({str(q.device) for q in model.parameters()})
    assert all(q.device.type=='cuda' for q in model.parameters()),'CPU offload 없이 GPU에 모델을 올려야 해요.'
    assert all(q.device.type=='cuda' for q in model.parameters() if q.requires_grad)
    print('GPU_MODEL_CONFIRMED',json.dumps({'devices':parameter_devices,'gpu':torch.cuda.get_device_name(0),
        'dtype':str(dtype),'allocated_mib':torch.cuda.memory_allocated()/2**20,
        'input_cache_enabled':cfg.get('cache_inputs_on_gpu',False)}),flush=True)
    from bitsandbytes.optim import AdamW8bit
    optimizer=AdamW8bit([q for q in model.parameters() if q.requires_grad],lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    steps=math.ceil(len(train)/cfg['gradient_accumulation_steps'])*cfg['epochs']
    scheduler=get_cosine_schedule_with_warmup(optimizer,math.ceil(steps*cfg['warmup_ratio']),steps)
    scaler=torch.amp.GradScaler('cuda',enabled=dtype==torch.float16,init_scale=cfg.get('fp16_initial_scale',16384))
    env={'python':platform.python_version(),'torch':torch.__version__,'cuda':torch.version.cuda,
        'gpu_name':torch.cuda.get_device_name(0),'visible_gpu_count':torch.cuda.device_count(),'used_device':'cuda:0',
        'compute_dtype':str(dtype),'trainable_parameters':sum(q.numel() for q in model.parameters() if q.requires_grad),
        'libraries':{name:version(name) for name in ['transformers','peft','accelerate','bitsandbytes','safetensors']},
        'planned_optimizer_attempts':steps,'training_rows':810,'validation_rows':90,'external_upload_performed':False}
    write_json(out/'environment.json',env);write_json(out/'run_context.json',context)
    if a.smoke:
        # scheduler의 step-0 warmup LR=0과 구분해, 실제 비영(非零) LR의 업데이트를 검사해요.
        for group in optimizer.param_groups:group['lr']=cfg['learning_rate']
        probe=next(q for name,q in model.named_parameters() if q.requires_grad and 'lora_B' in name)
        before=probe.detach().clone()
        model.train();item=max((encoded[r['id']] for r in train),key=lambda x:len(x['input_ids']))
        torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
        # FP16의 초기 scale overflow는 skip 기록 후 scale을 줄여 최대 8회 재시도해요.
        attempts=0;updated=False
        while attempts<8 and not updated:
            optimizer.zero_grad(set_to_none=True)
            with autocast(device,dtype):loss,n=masked_loss(model,item,device)
            assert torch.isfinite(loss)
            scaler.scale(loss).backward();scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip_norm'],error_if_nonfinite=not scaler.is_enabled())
            old=scaler.get_scale();scaler.step(optimizer);scaler.update();attempts+=1
            updated=not scaler.is_enabled() or scaler.get_scale()>=old
        assert updated,'FP16 scale 감소 후에도 optimizer 업데이트가 되지 않았어요.'
        changed=not torch.equal(probe.detach(),before)
        assert changed,'optimizer step 후에도 LoRA B tensor가 바뀌지 않았어요.'
        write_json(out/'smoke.json',{'row_id':item['id'],'tokens':len(item['input_ids']),'assistant_targets':n,
            'loss':float(loss.detach()),'compute_dtype':str(dtype),'optimizer_attempts':attempts,
            'optimizer_update_executed':updated,'adapter_tensor_changed':changed,'memory':memory(device),'elapsed_s':time.perf_counter()-start,
            'five_epoch_training_executed':False,'adapter_saved':False})
        print('GPU_SMOKE_COMPLETE_NOT_FIVE_EPOCH_TRAINING',flush=True);return
    run_epochs(model,tokenizer,train,val,encoded,cfg,out,context,optimizer,scheduler,scaler,device,dtype,
        resume=resume,stop_after_epoch=a.stop_after_epoch)
