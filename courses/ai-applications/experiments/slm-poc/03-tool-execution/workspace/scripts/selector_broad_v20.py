"""Two same-budget LoRA arms. Fixed original interface, final weights only."""
import gc,json,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_broad_data_v20 import DATA,OUT,SEED,verify,view,read,read_jsonl,save,digest,SELECTOR
from scripts.selector_learning_v18 import load,prediction

def encode(s,r):
    v=view(r,'current_full');keys=list(v['options']);b=s.tokenizer([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(keys),padding=True,truncation=False,return_tensors='pt').to('cuda')
    if b['input_ids'].shape[1]>512:raise ValueError('Refuse truncation')
    return b,keys

def score(s,rows,label):
    import torch
    start=time.perf_counter();p={}
    for i,r in enumerate(rows):
        b,keys=encode(s,r)
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):vals=s.model(**b).logits[:,0].float().cpu().tolist()
        p[r['id']]=prediction(r,keys,vals)
        if (i+1)%100==0:print(label,i+1,'/',len(rows),'seconds',round(time.perf_counter()-start),flush=True)
    return p

def train(arm):
    cfg=verify();folder=OUT/arm
    if folder.exists():raise FileExistsError('Training arm protected')
    folder.mkdir();save(folder/'started.json',{'protocol_sha256':digest(DATA/'protocol.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    rows=read_jsonl(DATA/(arm+'_train.jsonl'));random.Random(SEED).shuffle(rows);s=load(True);m=s.model
    m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    params=[p for p in m.parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n,p in m.named_parameters() if p.requires_grad):raise ValueError('Only LoRA may train')
    initial={n:p.detach().cpu().clone() for n,p in m.named_parameters() if p.requires_grad}
    opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.);retries=[]
    def backward(group):
        for attempt in range(12):
            opt.zero_grad(set_to_none=True);m.train();total=0.
            for r in group:
                b,keys=encode(s,r)
                if len(r['expected'])!=1:raise ValueError('Training needs a single reviewed source positive')
                with torch.autocast('cuda',dtype=torch.float16):loss=torch.nn.functional.cross_entropy(m(**b).logits[:,0].float().unsqueeze(0),torch.tensor([keys.index(r['expected'][0])],device='cuda'))
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                scaler.scale(loss/len(group)).backward();total+=float(loss.detach())/len(group)
            scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
            if math.isfinite(norm):return total,norm
            old=scaler.get_scale();scaler.step(opt);scaler.update()
            if scaler.get_scale()>=old:raise ValueError('Overflow skip failed')
            retries.append({'old':old,'new':scaler.get_scale()})
        raise ValueError('Repeated gradient failure')
    lengths=[]
    for r in rows:b,_=encode(s,r);lengths.append(b['input_ids'].numel());del b
    rng=torch.get_rng_state();crng=torch.cuda.get_rng_state_all();profile=backward([rows[max(range(len(rows)),key=lambda i:lengths[i])]])
    opt.zero_grad(set_to_none=True);scaler=torch.amp.GradScaler('cuda',init_scale=scaler.get_scale());torch.set_rng_state(rng);torch.cuda.set_rng_state_all(crng)
    save(folder/'profile.json',{'no_update':True,'loss':profile[0],'peak_GiB':torch.cuda.max_memory_allocated()/2**30})
    started=time.perf_counter();log=[]
    for step,offset in enumerate(range(0,len(rows),4),1):
        loss,norm=backward(rows[offset:offset+4]);scaler.step(opt);scaler.update();log.append({'step':step,'seen':offset+4,'loss':loss,'gradient_norm':norm})
        if step%10==0:print(arm,step,'/',cfg['steps'],'loss',round(loss,4),'seconds',round(time.perf_counter()-started),flush=True)
        save(folder/'loss-log.json',log)
    if step!=cfg['steps'] or len(rows)!=cfg['train_n']:raise ValueError('Budget mismatch')
    target=folder/'final-adapter';m.save_pretrained(target,safe_serialization=True);m.eval();delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in m.named_parameters() if p.requires_grad)
    before=score(s,rows[:2],'reload probe');weights=load_file(str(target/'adapter_model.safetensors'))
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,weights);m.eval();after=score(s,rows[:2],'reloaded probe')
    error=max(abs(before[k]['scores'][o]-after[k]['scores'][o]) for k in before for o in before[k]['scores'])
    if delta<=0 or error>1e-5:raise ValueError('Update/reload verification failed')
    verify();save(folder/'complete.json',{'steps':step,'seen':len(rows),'seconds':time.perf_counter()-started,'max_abs_weight_change':delta,'reload_logit_error':error,'retries':retries,
        'peak_GiB':torch.cuda.max_memory_allocated()/2**30,'adapter_sha256':digest(target/'adapter_model.safetensors'),'no_test_selection':True})
    del params,opt,m,s;gc.collect();torch.cuda.empty_cache();print('TRAIN COMPLETE',arm,flush=True)

def evaluate():
    verify()
    for arm in ['new','mixed']:read(OUT/arm/'complete.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'protocol_sha256':digest(DATA/'protocol.json')})
    import torch
    fresh=read_jsonl(DATA/'fresh.jsonl');reference=read_jsonl(ROOT/'data/processed/selector-interface-v18/reference.jsonl')
    prior=read(ROOT/'output/diagnostics/selector-interface-v18/current_full-scores.json')
    for arm in ['baseline','new','mixed']:
        s=load(adapter=SELECTOR if arm=='baseline' else OUT/arm/'final-adapter')
        save(OUT/(arm+'-fit-probe.json'),score(s,read_jsonl(DATA/'fit_probe.jsonl'),arm+' fit probe'))
        save(OUT/(arm+'-fresh.json'),score(s,fresh,arm+' fresh'))
        rp=score(s,reference,arm+' reference');save(OUT/(arm+'-reference.json'),rp)
        if arm=='baseline':
            error=max(abs(p['scores'][k]-prior[i]['scores'][k]) for i,p in rp.items() for k in p['scores'])
            changed=[i for i,p in rp.items() if p['predicted']!=prior[i]['predicted']]
            save(OUT/'baseline-replay.json',{'max_raw_logit_difference':error,'changed':changed})
            if error>.05 or changed:raise ValueError('Baseline failed to replay')
        del s;gc.collect();torch.cuda.empty_cache()
    verify();save(OUT/'evaluation-complete.json',{'no_deployment':True,'final_weights_only':True});print('ALL EVALUATION COMPLETE',flush=True)

if __name__=='__main__':
    phase=sys.argv[1]
    if phase=='all':train('new');train('mixed');evaluate()
    elif phase.startswith('train_'):train(phase[6:])
    elif phase=='evaluate':evaluate()
    else:raise ValueError(phase)
