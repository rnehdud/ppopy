"""One fixed selector-only experiment. Final test is read after both arms finish."""
import gc,hashlib,json,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_interface_data_v18 import DATA,OUT,MODEL,SELECTOR,view,verify,read,read_jsonl,save,digest
from scripts.selector_followup_data_v18 import FOLLOW,verify_followup
RUN=OUT/'learning';SEED=180081

def verify_plan():
    verify();verify_followup();p=read(RUN/'plan.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Learning frozen file changed: '+rel)
    return p

def prepare():
    verify();verify_followup()
    if read(OUT/'reference-choice.json')['selected'] is not None:raise ValueError('Wrong experiment branch')
    if RUN.exists():raise FileExistsError('Learning protected')
    RUN.mkdir()
    files=[Path(__file__),ROOT/'tests/test_selector_learning_v18.py',OUT/'reference-choice.json',FOLLOW/'protocol.json',ROOT/'scripts/report_selector_learning_v18.py']
    save(RUN/'plan.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'lr':1e-5,'logical_batch':4,'epochs':1,'steps':50,
        'condition':'capability_full','gradient_checkpointing':False,'clip_norm':1.,'weight_decay':0,'grad_scaler':128.,
        'scope':'Same initial scalar selector, only query/value LoRA trainable. Random vs confusable negatives, matched200 queries/targets. Full tool definitions and paired context, no truncation. Only capability choice, not argument/execution/no-match.',
        'readout':'Both final adapters must exist before test scoring. Fresh baseline current_full/capability_full and both final capability_full;600 reference scored for final arms. No checkpoint/prompt/threshold search. See followup protocol guards.'})
    print('LEARNING PLAN FROZEN',flush=True)

def load(train=False,adapter=SELECTOR):
    import torch
    from agent.local_choice_scorer_v1 import LocalChoiceScorer
    from peft import prepare_model_for_kbit_training
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=True
    s=LocalChoiceScorer(MODEL,adapter);prepare_model_for_kbit_training(s.model,use_gradient_checkpointing=False)
    for n,p in s.model.named_parameters():p.requires_grad_(train and 'lora_' in n)
    s.model.train(train)
    return s

def encode(s,row,condition='capability_full'):
    v=view(row,condition);keys=list(v['options'])
    b=s.tokenizer([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(keys),padding=True,truncation=False,return_tensors='pt').to('cuda')
    if b['input_ids'].shape[1]>512:raise ValueError('No truncation')
    return b,keys

def target_index(row,keys):
    if len(row['expected'])!=1:raise ValueError('Training single positive required')
    return keys.index(row['expected'][0])

def prediction(row,keys,vals):
    scores=dict(zip(keys,vals));allowed={t['name'] for t in row['tools']};tools=[k for k in keys if k in allowed]
    pred=max(tools,key=scores.get)
    return {'predicted':pred,'correct':pred in row['expected'],'scores':scores,'tied_top':[k for k in tools if scores[k]==scores[pred]]}

def train(arm):
    cfg=verify_plan();folder=RUN/arm
    if folder.exists():raise FileExistsError('Arm protected')
    folder.mkdir();save(folder/'started.json',{'plan_sha256':digest(RUN/'plan.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    rows=read_jsonl(FOLLOW/(arm+'_train.jsonl'));random.Random(SEED).shuffle(rows)
    s=load(True);m=s.model;params=[p for p in m.parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n,p in m.named_parameters() if p.requires_grad):raise ValueError('Only LoRA may train')
    initial={n:p.detach().cpu().clone() for n,p in m.named_parameters() if p.requires_grad}
    opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.)
    retries=[];logs=[]
    def backward(group):
        nonlocal scaler
        for attempt in range(12):
            opt.zero_grad(set_to_none=True);m.train();total=0.
            for r in group:
                batch,keys=encode(s,r);target=target_index(r,keys)
                with torch.autocast('cuda',dtype=torch.float16):
                    logits=m(**batch).logits[:,0].float().unsqueeze(0)
                    loss=torch.nn.functional.cross_entropy(logits,torch.tensor([target],device='cuda'))
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                scaler.scale(loss/len(group)).backward();total+=float(loss.detach())/len(group)
            scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
            if math.isfinite(norm):return total,norm
            old=scaler.get_scale();scaler.step(opt);scaler.update()
            if scaler.get_scale()>=old:raise ValueError('Overflow not skipped')
            retries.append({'old_scale':old,'new_scale':scaler.get_scale()});save(folder/'retries.json',retries)
        raise ValueError('Repeated nonfinite gradients')
    # Check largest actual candidate batch, without an optimizer update.
    lengths=[]
    for r in rows:
        b,_=encode(s,r);lengths.append(int(b['input_ids'].shape[1]));del b
    rng=torch.get_rng_state();crng=torch.cuda.get_rng_state_all()
    profile=backward([rows[max(range(len(rows)),key=lambda i:lengths[i])]])
    opt.zero_grad(set_to_none=True);scaler=torch.amp.GradScaler('cuda',init_scale=scaler.get_scale())
    torch.set_rng_state(rng);torch.cuda.set_rng_state_all(crng)
    save(folder/'profile.json',{'max_tokens':max(lengths),'peak_GiB':torch.cuda.max_memory_allocated()/2**30,'loss':profile[0],'no_optimizer_update':True})
    start=time.perf_counter();seen=0
    for step,offset in enumerate(range(0,len(rows),4),1):
        group=rows[offset:offset+4];loss,norm=backward(group);scaler.step(opt);scaler.update();seen+=len(group)
        logs.append({'step':step,'seen':seen,'loss':loss,'gradient_norm':norm})
        if step%10==0:print(arm,step,'/50 loss',round(loss,4),'seconds',round(time.perf_counter()-start),flush=True)
        save(folder/'loss-log.json',logs)
    if seen!=200 or step!=50:raise ValueError('Wrong training budget')
    adapter=folder/'adapter-step-50';m.save_pretrained(adapter,safe_serialization=True);m.eval()
    delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in m.named_parameters() if p.requires_grad)
    def probe():
        vals=[]
        for r in rows[:2]:
            b,_=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):vals.extend(m(**b).logits[:,0].float().cpu().tolist())
        return vals
    before=probe();weights=load_file(str(adapter/'adapter_model.safetensors'))
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,weights);m.eval();after=probe();error=max(abs(x-y) for x,y in zip(before,after))
    if delta<=0 or error>1e-5:raise ValueError(('Update/reload failure',delta,error))
    verify_plan();save(folder/'complete.json',{'seen':seen,'steps':step,'max_abs_weight_change':delta,'reload_logit_error':error,'seconds':time.perf_counter()-start,
        'peak_GiB':torch.cuda.max_memory_allocated()/2**30,'overflows':retries,'adapter_sha256':digest(adapter/'adapter_model.safetensors'),
        'query_schedule_sha256':hashlib.sha256(json.dumps([r['id'] for r in rows]).encode()).hexdigest()})
    del opt,params,m,s;gc.collect();torch.cuda.empty_cache();print('TRAIN COMPLETE',arm,flush=True)

def score(s,rows,condition,label):
    import torch
    results={};start=time.perf_counter()
    for j,r in enumerate(rows):
        batch,keys=encode(s,r,condition)
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):vals=s.model(**batch).logits[:,0].float().cpu().tolist()
        results[r['id']]=prediction(r,keys,vals)
        if (j+1)%100==0:print(label,j+1,'/',len(rows),'seconds',round(time.perf_counter()-start),flush=True)
    return results

def evaluate():
    verify_plan()
    for arm in ['control','focused']:read(RUN/arm/'complete.json')
    if (RUN/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(RUN/'evaluation-started.json',{'plan_sha256':digest(RUN/'plan.json')})
    import torch
    rows=read_jsonl(FOLLOW/'fresh.jsonl');refs=read_jsonl(DATA/'reference.jsonl');s=load()
    for c in ['current_full','capability_full']:save(RUN/('baseline-'+c+'-fresh.json'),score(s,rows,c,'baseline '+c))
    del s;gc.collect();torch.cuda.empty_cache()
    for arm in ['control','focused']:
        s=load(adapter=RUN/arm/'adapter-step-50')
        save(RUN/(arm+'-fresh.json'),score(s,rows,'capability_full',arm+' fresh'))
        save(RUN/(arm+'-reference.json'),score(s,refs,'capability_full',arm+' reference'))
        del s;gc.collect();torch.cuda.empty_cache()
    verify_plan();save(RUN/'evaluation-complete.json',{'no_deployment':True,'fixed_final_step':50});print('EVALUATION COMPLETE',flush=True)

if __name__=='__main__':
    phase=sys.argv[1]
    if phase=='prepare':prepare()
    elif phase.startswith('train_'):train(phase.removeprefix('train_'))
    elif phase=='evaluate':evaluate()
    elif phase=='all':
        prepare();train('control');train('focused');evaluate()
    else:raise ValueError(phase)
