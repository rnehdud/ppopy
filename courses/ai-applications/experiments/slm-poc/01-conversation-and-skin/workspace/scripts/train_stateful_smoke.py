"""Fixed-config 100-example QLoRA smoke run + frozen before/after comparison."""
import argparse
from contextlib import nullcontext
import gc
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import sys
import time
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training.data import load_rows,tokenize_example,verify_freeze
from training.hf_backend import load_base,HFClient
from training.evaluation import evaluate

ROOT=Path(__file__).resolve().parents[1]


def emit(log_path,event,**values):
    with log_path.open('a',encoding='utf-8') as stream:
        stream.write(json.dumps({'event':event,**values},ensure_ascii=False)+'\n')
    print(event,values,flush=True)


def supervised_loss(model,example,dtype):
    import torch
    import torch.nn.functional as F
    ids=torch.tensor([example['input_ids']],device='cuda',dtype=torch.long)
    labels=torch.tensor(example['labels'],device='cuda',dtype=torch.long)
    positions=torch.nonzero(labels!=-100,as_tuple=False).flatten()
    if positions.min()<1:
        raise ValueError('A completion token has no preceding prediction position')
    # Compute the huge vocabulary projection only where a target is supervised.
    # This is identical to masked causal CE, without materializing prompt logits.
    with torch.autocast('cuda',dtype=dtype):
        outputs=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False,
                      logits_to_keep=positions-1)
        loss=F.cross_entropy(outputs.logits[0].float(),labels[positions])
    return loss


def mean_loss(model,examples,dtype):
    import torch
    model.eval()
    values=[]
    with torch.no_grad():
        for example in examples:
            values.append(float(supervised_loss(model,example,dtype)))
    return sum(values)/len(values)


def public_decisions(config):
    """Use only the already prepared public TRAIN split, never its test rows."""
    count=config.get('general_tool_decision_examples',0)
    if not count:
        return []
    rows=load_rows(ROOT/'data/processed/qwen_tool_use/train.jsonl')
    candidates={'call':[],'answer':[]}
    for row in rows:
        if not row['eligible_2048']:
            continue
        for i,message in enumerate(row['messages']):
            if message['role']=='assistant':
                candidates['call' if message.get('tool_calls') else 'answer'].append((row,i))
    chosen=[]
    rng=random.Random(config['seed'])
    for kind,amount in [('call',count//2),('answer',count-count//2)]:
        choices=candidates[kind]
        rng.shuffle(choices)
        for source,index in choices[:amount]:
            chosen.append({'id':f'public-{source["id"]}-assistant-{index}',
                           'scenario_id':'public-'+source['source_group'],'category':'general_tool_use',
                           'messages':source['messages'][:index+1],'tools':source['tools']})
    return chosen


def select_stateful_rows(rows,count,seed):
    buckets=defaultdict(list)
    for row in rows:
        buckets[row['category']].append(row)
    rng=random.Random(seed)
    for values in buckets.values():
        rng.shuffle(values)
    selected=[]
    while len(selected)<count:
        progressed=False
        for category in sorted(buckets):
            if buckets[category] and len(selected)<count:
                selected.append(buckets[category].pop())
                progressed=True
        if not progressed:
            raise ValueError('Not enough unique stateful decisions')
    return selected


def train(model,examples,config,dtype,log_path):
    import torch
    params=[p for p in model.parameters() if p.requires_grad]
    if any('lora_' not in name for name,p in model.named_parameters() if p.requires_grad):
        raise ValueError('Unexpected trainable base parameter')
    optimizer=torch.optim.AdamW(params,lr=config['learning_rate'],weight_decay=0,foreach=False)
    model.train()
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.config.use_cache=False
    model.enable_input_require_grads()
    order=list(range(len(examples)))
    rng=random.Random(config['seed'])
    rng.shuffle(order)
    cursor=0
    optimizer.zero_grad(set_to_none=True)
    started=time.perf_counter()
    losses=[]
    for step in range(config['optimizer_steps']):
        values=[]
        for micro in range(config['gradient_accumulation']):
            if cursor==len(order):
                rng.shuffle(order)
                cursor=0
            example=examples[order[cursor]]
            cursor+=1
            loss=supervised_loss(model,example,dtype)
            if not torch.isfinite(loss):
                raise ValueError('Non-finite training loss')
            (loss/config['gradient_accumulation']).backward()
            values.append(float(loss.detach()))
            del loss
        torch.nn.utils.clip_grad_norm_(params,1.0)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        avg=sum(values)/len(values)
        losses.append(avg)
        if step==0 or (step+1)%5==0:
            emit(log_path,'train_step',step=step+1,loss=round(avg,6),elapsed_seconds=round(time.perf_counter()-started,2),
                 peak_cuda_gib=round(torch.cuda.max_memory_allocated()/1024**3,3))
    model.eval()
    model.gradient_checkpointing_disable()
    model.config.use_cache=True
    return {'optimizer_steps':len(losses),'micro_batches':len(losses)*config['gradient_accumulation'],
            'first_loss':losses[0],'last_loss':losses[-1],'losses':losses,
            'seconds':time.perf_counter()-started,'peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated()}


def probe(model,tokenizer,row):
    import torch
    text=tokenizer.apply_chat_template(row['messages'][:-1],tools=row['tools'],tokenize=False,add_generation_prompt=True)
    data=tokenizer(text,return_tensors='pt',add_special_tokens=False).to('cuda')
    model.eval()
    with torch.inference_mode(),torch.autocast('cuda',dtype=model.get_input_embeddings().weight.dtype):
        output=model.generate(**data,max_new_tokens=24,do_sample=False,pad_token_id=tokenizer.pad_token_id,
                              eos_token_id=tokenizer.eos_token_id,use_cache=True)
    return output[0,data['input_ids'].shape[1]:].tolist()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',default='configs/qlora_smoke.json')
    parser.add_argument('--run-name',default='qlora-smoke-v1')
    args=parser.parse_args()
    import torch
    from peft import LoraConfig,get_peft_model,PeftModel
    config=json.loads((ROOT/args.config).read_text(encoding='utf-8'))
    manifest=verify_freeze(ROOT,config['dataset'])
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA is unavailable in this Python environment')
    run=ROOT/'output/training'/args.run_name
    run.mkdir(parents=True,exist_ok=False)
    log=run/'progress.jsonl'
    random.seed(config['seed'])
    torch.manual_seed(config['seed'])
    torch.cuda.manual_seed_all(config['seed'])
    environment={'python':sys.version,'packages':{p:importlib.metadata.version(p) for p in
                 ['torch','transformers','peft','bitsandbytes','accelerate']},
                 'cuda_runtime':torch.version.cuda,'gpu':torch.cuda.get_device_name(0),
                 'gpu_total_bytes':torch.cuda.get_device_properties(0).total_memory}
    metadata={'config':config,'config_sha256':hashlib.sha256((ROOT/args.config).read_bytes()).hexdigest(),
              'dataset_manifest':manifest,'environment':environment,
              'base_manifest':json.loads((ROOT/'models/qwen2.5-3b-nf4/download_manifest.json').read_text(encoding='utf-8')),
              'public_train_sha256':hashlib.sha256((ROOT/'data/processed/qwen_tool_use/train.jsonl').read_bytes()).hexdigest(),
              'runtime_sources':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
                  ['agent/runtime.py','training/hf_backend.py','training/data.py','training/evaluation.py','scripts/train_stateful_smoke.py']},
              'comparison_policy':'NF4 validation loss before/after; closed-loop evaluation uses the same official Q4_K_M GGUF, template, tools, generation settings and frozen holdout, without/with the NF4-trained LoRA. Not comparable to old development scores.'}
    (run/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit(log,'environment',**environment)
    model,tokenizer,dtype=load_base(ROOT)
    lora=LoraConfig(r=config['lora_r'],lora_alpha=config['lora_alpha'],lora_dropout=config['lora_dropout'],
                    target_modules=config['target_modules'],bias='none',task_type='CAUSAL_LM')
    model=get_peft_model(model,lora)
    trainable=sum(p.numel() for p in model.parameters() if p.requires_grad)
    emit(log,'model_loaded',trainable_parameters=trainable,cuda_allocated_bytes=torch.cuda.memory_allocated())
    raw_train=load_rows(ROOT/config['dataset']/'train.sft.jsonl')
    selected=select_stateful_rows(raw_train,config['train_decision_examples'],config['seed'])+public_decisions(config)
    examples=[tokenize_example(tokenizer,r,config['max_length']) for r in selected]
    validation_rows=load_rows(ROOT/config['dataset']/'validation.sft.jsonl')[:config['validation_loss_examples']]
    validation=[tokenize_example(tokenizer,r,config['max_length']) for r in validation_rows]
    (run/'selected_training_ids.json').write_text(json.dumps([r['id'] for r in selected],indent=2)+'\n',encoding='utf-8')
    holdout=json.loads((ROOT/config['dataset']/'holdout.cases.json').read_text(encoding='utf-8'))
    if config['eval_limit']:
        holdout=holdout[:config['eval_limit']]
    model.gradient_checkpointing_disable()
    client=HFClient(model,tokenizer,config['generation_max_new_tokens'])
    skip_agent_eval=config.get('evaluation_backend','').startswith('llama_cpp')
    with model.disable_adapter():
        before_loss=mean_loss(model,validation,dtype)
        emit(log,'baseline_validation_loss',loss=before_loss)
        before=None if skip_agent_eval else evaluate(client,holdout,run/'before','before',False)
    # No hyperparameters or examples are selected using the holdout results.
    emit(log,'baseline_finished',scenarios=0 if skip_agent_eval else len(holdout),
         note='Closed-loop evaluation uses identical GGUF engine before/after.' if skip_agent_eval else '')
    torch.cuda.reset_peak_memory_stats()
    initial_b={name:p.detach().cpu().clone() for name,p in model.named_parameters() if 'lora_B' in name}
    training=train(model,examples,config,dtype,log)
    changed=any(not torch.equal(initial_b[name],p.detach().cpu()) for name,p in model.named_parameters() if name in initial_b)
    if not changed:
        raise RuntimeError('LoRA B weights did not change')
    after_loss=mean_loss(model,validation,dtype)
    adapter=ROOT/'adapters'/args.run_name
    adapter.mkdir(parents=True,exist_ok=False)
    model.save_pretrained(str(adapter),safe_serialization=True,save_embedding_layers=False)
    tokenizer.save_pretrained(str(adapter))
    expected_probe=probe(model,tokenizer,selected[0])
    emit(log,'adapter_saved',path=str(adapter),weights_changed=changed)
    # Release the entire first model before loading a second copy on an 8GB GPU.
    del client,model,initial_b
    gc.collect()
    torch.cuda.empty_cache()
    model,tokenizer,dtype=load_base(ROOT)
    model=PeftModel.from_pretrained(model,str(adapter),is_trainable=False)
    model.gradient_checkpointing_disable()
    model.config.use_cache=True
    actual_probe=probe(model,tokenizer,selected[0])
    reload_equal=actual_probe==expected_probe
    if not reload_equal:
        raise RuntimeError('Saved/reloaded adapter changed deterministic probe output')
    emit(log,'adapter_reloaded',probe_token_ids_match=True)
    client=HFClient(model,tokenizer,config['generation_max_new_tokens'])
    after=None if skip_agent_eval else evaluate(client,holdout,run/'after','after',True)
    report={'environment':environment,'training':training,'training_examples':len(examples),
            'stateful_decision_examples':config['train_decision_examples'],
            'public_tool_decision_examples':config.get('general_tool_decision_examples',0),
            'training_source_scenarios':len({r['scenario_id'] for r in selected}),
            'trainable_parameters':trainable,'validation_loss_before':before_loss,'validation_loss_after':after_loss,
            'adapter_path':str(adapter.relative_to(ROOT)),'adapter_weights_changed':changed,
            'adapter_reload_probe_equal':reload_equal,
            'before':None if before is None else {k:v for k,v in before.items() if k!='results'},
            'after':None if after is None else {k:v for k,v in after.items() if k!='results'},
            'closed_loop_evaluation_backend':config.get('evaluation_backend','transformers_nf4'),
            'scenario_pass_delta':None if before is None else after['passed_scenarios']-before['passed_scenarios'],
            'holdout_hash_before':manifest['files']['holdout.cases.json']['sha256'],
            'holdout_hash_after':hashlib.sha256((ROOT/config['dataset']/'holdout.cases.json').read_bytes()).hexdigest(),
            'limitations':['Synthetic template-disjoint holdout, not broad Korean or clinical accuracy.',
                           '100 decision examples and a fixed small smoke run; no hyperparameter search.',
                           'Single seed and run; any observed difference is exploratory.']}
    if report['holdout_hash_before']!=report['holdout_hash_after']:
        raise ValueError('Holdout changed during experiment')
    (run/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit(log,'complete',before_scenarios=None if before is None else before['passed_scenarios'],
         after_scenarios=None if after is None else after['passed_scenarios'],
         validation_loss_before=before_loss,validation_loss_after=after_loss)


if __name__=='__main__':
    try:
        main()
    except Exception:
        import traceback
        failure=ROOT/'output/training/last_failure.txt'
        failure.parent.mkdir(parents=True,exist_ok=True)
        failure.write_text(traceback.format_exc(),encoding='utf-8')
        raise
