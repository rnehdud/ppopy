"""200-example Qwen3 NF4/LoRA training pilot for KLUE WoS state prediction."""
import gc
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.prepare_klue_experiment import make_messages
from scripts.train_stateful_smoke import supervised_loss,mean_loss
from training.data import tokenize_example

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/klue_wos_pilot_v1'
RUN=ROOT/'output/training/klue-wos-qwen3-pilot-v1'
ADAPTER=ROOT/'adapters/klue-wos-qwen3-pilot-v1'
MODEL=ROOT/'models/qwen3-4b-instruct-2507-nf4'
SEED=20261105


def read_rows(name):
    return [json.loads(line) for line in (DATA/name).read_text(encoding='utf-8').splitlines() if line]


def emit(event,**kwargs):
    record={'event':event,**kwargs}
    with (RUN/'progress.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(event,kwargs,flush=True)


def load_base():
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
    from peft import prepare_model_for_kbit_training
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    tokenizer=AutoTokenizer.from_pretrained(str(ROOT/'models/qwen3-4b-instruct-2507/tokenizer'),local_files_only=True)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',
                             bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype)
    model=AutoModelForCausalLM.from_pretrained(str(MODEL),local_files_only=True,trust_remote_code=False,
          device_map={'':0},torch_dtype=dtype,quantization_config=quant,attn_implementation='sdpa',low_cpu_mem_usage=True)
    model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True)
    model.get_input_embeddings().to(dtype=dtype)
    model.get_output_embeddings().to(dtype=dtype)
    model.config.use_cache=False
    return model,tokenizer,dtype


def probe(model,tokenizer,row,slots):
    import torch
    text=tokenizer.apply_chat_template(make_messages(row,slots,False),tools=[],tokenize=False,add_generation_prompt=True)
    data=tokenizer(text,return_tensors='pt',add_special_tokens=False).to('cuda')
    model.eval()
    with torch.inference_mode(),torch.autocast('cuda',dtype=model.get_input_embeddings().weight.dtype):
        output=model.generate(**data,max_new_tokens=24,do_sample=False,
                pad_token_id=tokenizer.pad_token_id,eos_token_id=tokenizer.eos_token_id,use_cache=True)
    return output[0,data['input_ids'].shape[1]:].tolist()


def main():
    import torch
    from peft import LoraConfig,get_peft_model,PeftModel
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA is required')
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Frozen dataset changed')
    if ADAPTER.exists():
        raise FileExistsError('Adapter already exists; do not overwrite')
    RUN.mkdir(parents=True,exist_ok=False)
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    slots=json.loads((DATA/'slots.json').read_text(encoding='utf-8'))
    rows=read_rows('train.jsonl'); val_rows=read_rows('validation_loss.jsonl')
    environment={'python':sys.version,'gpu':torch.cuda.get_device_name(0),'cuda':torch.version.cuda,
                 'packages':{p:importlib.metadata.version(p) for p in ['torch','transformers','peft','bitsandbytes','accelerate']}}
    config={'seed':SEED,'optimizer_steps':100,'gradient_accumulation':2,'examples':len(rows),
            'validation_loss_examples':len(val_rows),'lr':0.0002,'lora_r':8,'lora_alpha':16,
            'lora_dropout':0.05,'target_modules':['q_proj','v_proj'],'max_length':2048,
            'base_model':json.loads((MODEL/'manifest.json').read_text(encoding='utf-8')),
            'experiment_manifest':manifest,'environment':environment,
            'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                              [Path(__file__),ROOT/'scripts/prepare_klue_experiment.py',ROOT/'scripts/train_stateful_smoke.py',ROOT/'training/data.py']}}
    (RUN/'metadata.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit('environment',**environment)
    model,tokenizer,dtype=load_base()
    model=get_peft_model(model,LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,target_modules=['q_proj','v_proj'],
                                          bias='none',task_type='CAUSAL_LM'))
    def convert(row):
        return tokenize_example(tokenizer,{'id':row['id'],'scenario_id':row['dialogue_id'],'category':'klue_wos',
                  'messages':make_messages(row,slots,True),'tools':[]},max_length=2048)
    examples=[convert(r) for r in rows]
    validation=[convert(r) for r in val_rows]
    params=[p for p in model.parameters() if p.requires_grad]
    trainable_parameters=sum(p.numel() for p in params)
    emit('model_loaded',trainable=trainable_parameters,cuda_allocated=torch.cuda.memory_allocated())
    with model.disable_adapter():
        before_loss=mean_loss(model,validation,dtype)
    emit('validation_before',loss=before_loss)
    before_b={n:p.detach().cpu().clone() for n,p in model.named_parameters() if 'lora_B' in n}
    optim=torch.optim.AdamW(params,lr=config['lr'],weight_decay=0,foreach=False)
    model.train(); model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.enable_input_require_grads(); model.config.use_cache=False
    order=list(range(len(examples)));random.Random(SEED).shuffle(order)
    cursor=0; optim.zero_grad(set_to_none=True);started=time.perf_counter();torch.cuda.reset_peak_memory_stats()
    for step in range(100):
        values=[]
        for _ in range(2):
            loss=supervised_loss(model,examples[order[cursor]],dtype);cursor+=1
            if not torch.isfinite(loss): raise ValueError('Nonfinite training loss')
            (loss/2).backward();values.append(float(loss.detach()));del loss
        torch.nn.utils.clip_grad_norm_(params,1.0);optim.step();optim.zero_grad(set_to_none=True)
        if step==0 or (step+1)%5==0:
            emit('train_step',step=step+1,loss=round(sum(values)/2,6),
                 seconds=round(time.perf_counter()-started,2),peak_cuda_gib=round(torch.cuda.max_memory_allocated()/1024**3,3))
    train_seconds=time.perf_counter()-started
    changed=any(not torch.equal(before_b[n],p.detach().cpu()) for n,p in model.named_parameters() if n in before_b)
    if not changed: raise ValueError('Adapter weights unchanged')
    model.gradient_checkpointing_disable();model.config.use_cache=True
    after_loss=mean_loss(model,validation,dtype)
    ADAPTER.mkdir(parents=True,exist_ok=False)
    model.save_pretrained(str(ADAPTER),safe_serialization=True,save_embedding_layers=False)
    expected=probe(model,tokenizer,rows[0],slots)
    emit('adapter_saved',adapter=str(ADAPTER),weights_changed=changed)
    del model,optim,params,before_b
    gc.collect();torch.cuda.empty_cache()
    model,tokenizer,dtype=load_base()
    model=PeftModel.from_pretrained(model,str(ADAPTER),is_trainable=False)
    model.gradient_checkpointing_disable();model.config.use_cache=True
    actual=probe(model,tokenizer,rows[0],slots)
    if actual!=expected: raise ValueError('Saved adapter reload produced different tokens')
    report={'examples':len(examples),'optimizer_steps':100,'validation_examples':len(validation),
            'validation_loss_before':before_loss,'validation_loss_after':after_loss,
            'training_seconds':train_seconds,'trainable_parameters':trainable_parameters,
            'adapter_path':str(ADAPTER.relative_to(ROOT)),'adapter_weights_changed':changed,'reload_probe_equal':True,
            'adapter_sha256':hashlib.sha256((ADAPTER/'adapter_model.safetensors').read_bytes()).hexdigest(),
            'limits':['Pilot: 200 examples only; single randomly selected turn per training conversation.',
                      'Uses gold prior state, not an autonomous multi-turn agent.',
                      'Training NF4; subsequent evaluation on same Q4_K_M GGUF with and without converted LoRA.',
                      'No skincare-domain data or tool-call supervision in this run.']}
    (RUN/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit('complete',validation_loss_before=before_loss,validation_loss_after=after_loss,reload_probe_equal=True)


if __name__=='__main__':
    try: main()
    except Exception:
        import traceback
        (ROOT/'output/training/klue-pilot-last-failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
