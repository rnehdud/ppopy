"""Jev-style Korean choice NF4+LoRA pilot, matching the ko-decision data split."""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import SYMPTOMS,SymptomSession
from scripts.evaluate_symptom_state_v1 import CASES
from scripts.compare_korean_decision_pilot import EXTRA_CASES,QUESTION,OPTIONS,CHECKSUMS,ENGLISH_SYSTEM
from scripts.evaluate_jev_style_qwen_pilot import NAMES,DESCRIPTIONS
from scripts.train_ko_decision_qlora_pilot import NEW_CASES,read_rows

MODEL=ROOT/'models/exaone-4-1.2b-jev-v03'
OUT=ROOT/'output/training/exaone-jev-qlora-v1'
ADAPTER=ROOT/'adapters/exaone-jev-qlora-v1'

def main():
    import torch,transformers,peft,bitsandbytes
    from transformers import AutoModelForCausalLM,BitsAndBytesConfig
    from scripts.exaone_tokenizer_compat import load as load_tokenizer
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training,set_peft_model_state_dict
    from safetensors.torch import load_file
    if OUT.exists() or ADAPTER.exists():raise FileExistsError('Existing run is protected')
    if not torch.cuda.is_available():raise RuntimeError('CUDA required')
    with (MODEL/'model.safetensors').open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=CHECKSUMS['exaone']:raise ValueError('Model hash mismatch')
    train=read_rows('train');val=read_rows('validation')
    if {r['text'] for r in train}&{r['text'] for r in val}:raise ValueError('data split leak')
    if {t[0] for c in NEW_CASES for t in c['turns']}&{r['text'] for r in train+val}:raise ValueError('holdout leak')
    torch.manual_seed(271828);torch.cuda.manual_seed_all(271828);random.seed(271828)
    tok=load_tokenizer(MODEL)
    if tok.pad_token is None:tok.pad_token=tok.eos_token
    tok.padding_side='left'
    letter_ids=[tok.encode(x,add_special_tokens=False) for x in 'ABCD']
    if any(len(x)!=1 for x in letter_ids) or len({x[0] for x in letter_ids})!=4:raise ValueError('Invalid answer tokenization')
    letter_ids=[x[0] for x in letter_ids]
    q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForCausalLM.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False,
       quantization_config=q,torch_dtype=torch.float16,device_map={'':0})
    base.config.use_cache=False
    base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=True,gradient_checkpointing_kwargs={'use_reentrant':False})
    model=get_peft_model(base,LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,target_modules=['q_proj','v_proj'],bias='none',task_type='CAUSAL_LM'))
    params=[p for p in model.parameters() if p.requires_grad]
    names=[n for n,p in model.named_parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n in names):raise ValueError('Unexpected trainable weights')
    print('loaded exaone nf4; lora params',sum(p.numel() for p in params),flush=True)

    def logits_for(rows):
        prompts=[]
        for r in rows:
            situation='대상 증상: '+NAMES[r['field']]+'\n이전 상태: '+r['previous']+'\n이번 사용자 발화: '+r['text']
            task={'state':situation,'question':QUESTION,'options':[{'label':'ABCD'[i],'key':key,'description':DESCRIPTIONS[key]} for i,key in enumerate(OPTIONS)]}
            prompts.append(tok.apply_chat_template([{'role':'system','content':ENGLISH_SYSTEM},
                 {'role':'user','content':json.dumps(task,ensure_ascii=False)}],tokenize=False,
                 add_generation_prompt=True,enable_thinking=False))
        encoded=tok(prompts,padding=True,return_tensors='pt',add_special_tokens=False).to('cuda')
        if encoded['input_ids'].shape[1]>2048:raise ValueError('input too long')
        positions=(encoded['attention_mask'].cumsum(-1)-1).clamp(min=0)
        return model(**encoded,position_ids=positions,use_cache=False,logits_to_keep=1).logits[:,-1,letter_ids].float()

    def validate():
        model.eval();correct=0;losses=[];confusion={k:{v:0 for v in OPTIONS} for k in OPTIONS}
        with torch.inference_mode():
            for i in range(0,len(val),4):
                rows=val[i:i+4];logits=logits_for(rows);target=torch.tensor([OPTIONS.index(r['decision']) for r in rows],device='cuda')
                losses.append((len(rows),float(torch.nn.functional.cross_entropy(logits,target))))
                for r,p in zip(rows,logits.argmax(-1).tolist()):
                    confusion[r['decision']][OPTIONS[p]]+=1;correct+=OPTIONS[p]==r['decision']
        return {'n':len(val),'correct':correct,'accuracy':correct/len(val),
                'loss':sum(n*x for n,x in losses)/len(val),'confusion':confusion}

    def scenarios(cases):
        model.eval();res=[]
        for case in cases:
            session=SymptomSession();turns=[]
            for text,expected in case['turns']:
                before=session.state
                rows=[{'field':f,'previous':before[f],'text':text} for f in SYMPTOMS]
                with torch.inference_mode():logits=logits_for(rows)
                decisions={f:OPTIONS[i] for f,i in zip(SYMPTOMS,logits.argmax(-1).tolist())}
                patch={f:d for f,d in decisions.items() if d!='unchanged'}
                execution=session.update(patch) if patch else None
                turns.append({'input':text,'before':before,'expected':expected,'decisions':decisions,'patch':patch,
                              'tool_result':execution,'after':session.state,'matches':session.state==expected})
            res.append({'id':case['id'],'passes':all(t['matches'] for t in turns),'turns':turns})
        turns=[t for c in res for t in c['turns']]
        summary={'scenarios':len(res),'scenario_passes':sum(c['passes'] for c in res),'turns':len(turns),
                 'state_matches':sum(t['matches'] for t in turns),
                 'field_matches':sum(t['after'][f]==t['expected'][f] for t in turns for f in SYMPTOMS),
                 'fields':len(turns)*len(SYMPTOMS),
                 'unknown_to_absent':sum(t['expected'][f]=='unknown' and t['after'][f]=='absent' for t in turns for f in SYMPTOMS)}
        return {'summary':summary,'cases':res}

    OUT.mkdir(parents=True);ADAPTER.mkdir(parents=True)
    config={'seed':271828,'base':'carrtesy/EXAONE-4.0-1.2B-JEV@bc5012eabb1c5231cafec849843e51bbb5fb9630',
      'quantization':'NF4 double quant, fp16 compute','task':'cross entropy over four answer-label logits',
      'lora':{'r':8,'alpha':16,'dropout':0.05,'targets':['q_proj','v_proj'],'gradient_checkpointing':True},
      'train_items':len(train),'validation_items':len(val),'steps':60,'items_per_step':2,'lr':0.0002,
      'checkpoints':[20,40,60],'checkpoint_selection':'validation accuracy; ties earlier',
      'evaluation':'same NF4 base, model-specific prompt, forward option order; no heldout used for checkpoint selection',
      'libraries':{'torch':torch.__version__,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__},
      'tokenizer_compat':'360 formatted train/validation prompts and A-D token IDs match Transformers 5.14 reference SHA256 2988a75ebf1312cc1a005c3d0f366dc6f64c7ad2378cd0eda27815aaa9bbe428',
      'disclaimer':'synthetic labels, no independent human review; no real personal data'}
    (OUT/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    baseline_val=validate();base_dev=scenarios(CASES+EXTRA_CASES);base_hold=scenarios(NEW_CASES)
    (OUT/'baseline.json').write_text(json.dumps({'validation':baseline_val,'development':base_dev,'heldout':base_hold},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('baseline',baseline_val['accuracy'],base_dev['summary'],base_hold['summary'],flush=True)
    model.eval()
    with torch.inference_mode():initial=logits_for(train[:1]).cpu()
    model.train();optimizer=torch.optim.AdamW(params,lr=0.0002,weight_decay=0,foreach=False);history=[];cursor=0;start=time.perf_counter()
    for step in range(1,61):
        optimizer.zero_grad(set_to_none=True);loss_sum=0
        for _ in range(2):
            row=train[cursor];cursor+=1;logits=logits_for([row])
            target=torch.tensor([OPTIONS.index(row['decision'])],device='cuda')
            loss=torch.nn.functional.cross_entropy(logits,target)
            if not torch.isfinite(loss):raise ValueError('nonfinite loss')
            (loss/2).backward();loss_sum+=float(loss.detach())/2
        norm=float(torch.nn.utils.clip_grad_norm_(params,1))
        if not (norm>0 and torch.isfinite(torch.tensor(norm))):raise ValueError('bad adapter gradient')
        optimizer.step()
        if step%10==0:print('step',step,'loss',round(loss_sum,4),'sec',round(time.perf_counter()-start),'peak',round(torch.cuda.max_memory_allocated()/1024**3,2),flush=True)
        if step in [20,40,60]:
            validation=validate();folder=ADAPTER/f'step-{step}';model.save_pretrained(folder,safe_serialization=True)
            history.append({'step':step,'train_examples_seen':cursor,'validation':validation,'adapter':str(folder.relative_to(ROOT))})
            (OUT/'history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('snapshot',step,'val',validation['accuracy'],'loss',validation['loss'],flush=True);model.train()
    selected=max(history,key=lambda x:(x['validation']['accuracy'],-x['step']))
    weights=ROOT/selected['adapter']/'adapter_model.safetensors';set_peft_model_state_dict(model,load_file(str(weights)))
    model.eval()
    with torch.inference_mode():after=logits_for(train[:1]).cpu()
    delta=float((after-initial).abs().max())
    if delta<1e-6:raise ValueError('No adapter change')
    with torch.no_grad():params[0].add_(0.01)
    set_peft_model_state_dict(model,load_file(str(weights)))
    with torch.inference_mode():reloaded=logits_for(train[:1]).cpu()
    reload_delta=float((after-reloaded).abs().max())
    if reload_delta>1e-4:raise ValueError('reload mismatch')
    post_dev=scenarios(CASES+EXTRA_CASES);post_hold=scenarios(NEW_CASES)
    report={'selected':selected,'probe_logit_change':delta,'reload_max_abs_difference':reload_delta,
      'development':post_dev,'heldout':post_hold,'peak_cuda_allocated_gib':torch.cuda.max_memory_allocated()/1024**3,
      'train_seconds_including_validation':time.perf_counter()-start}
    (OUT/'trained.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('selected',selected['step'],'heldout',post_hold['summary'],'reload_difference',reload_delta,flush=True)

if __name__=='__main__':main()
