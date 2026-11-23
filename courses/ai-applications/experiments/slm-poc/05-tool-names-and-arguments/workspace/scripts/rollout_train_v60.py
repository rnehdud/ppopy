"""Matched-budget current vs expanded encoder LoRA; no final-test reading."""
import gc,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.rollout_data_v60 import DATA,OUT,START,verify,read,save,digest
from scripts.selector_learning_v18 import load
from scripts.result_loop_split_v27 import encode

def validate_data():
    for p,h in read(OUT/'training-input-manifest.json').items():
        if digest(ROOT/p)!=h:raise ValueError('Training input changed')

def expanded(scorer,probe_rows):
    import torch
    from peft import LoraConfig,set_peft_model_state_dict,get_peft_model_state_dict
    m=scorer.model;m.eval()
    def values():
        out=[]
        for r in probe_rows:
            b,_=encode(scorer,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):out+=m(**b).logits[:,0].float().cpu().tolist()
        return out
    before=values();old={k:v.clone() for k,v in get_peft_model_state_dict(m).items()}
    config=LoraConfig(r=8,lora_alpha=16,lora_dropout=.05,bias='none',task_type=None,
        target_modules=r'.*encoder\.layer\.\d+\.(attention\.self\.(query|key|value)|attention\.output\.dense|intermediate\.dense|output\.dense)')
    m.add_adapter('wide',config);set_peft_model_state_dict(m,old,adapter_name='wide');m.set_adapter('wide');m.eval()
    after=values();error=max(abs(a-b) for a,b in zip(before,after))
    if error>1e-5:raise ValueError('Expanded initial outputs changed: '+str(error))
    for n,p in m.named_parameters():p.requires_grad_('lora_' in n and '.wide.' in n)
    targets=sorted(n for n,mod in m.named_modules() if hasattr(mod,'lora_A') and 'wide' in mod.lora_A)
    return {'initial_output_error':error,'modules':targets,'adapter':'wide'}

def train(arm):
    cfg=verify();validate_data();folder=OUT/arm
    if folder.exists():raise FileExistsError(folder)
    folder.mkdir();save(folder/'started.json',{'plan_sha256':digest(OUT/'plan.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(cfg['seed']);torch.manual_seed(cfg['seed']);torch.cuda.manual_seed_all(cfg['seed'])
    s=load(True,START);m=s.model;groups=read(OUT/(arm+'-groups.json'));refs=read(OUT/'references.json')
    setup=expanded(s,[refs[0]]+groups[0]) if arm=='B' else {'adapter':'default','initial_output_error':0}
    save(folder/'setup.json',setup)
    m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    named={n:p for n,p in m.named_parameters() if p.requires_grad}
    if not named or any('lora_' not in n for n in named):raise ValueError('Only adapter weights may train')
    initial={n:p.detach().cpu().clone() for n,p in named.items()};params=list(named.values())
    opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.)
    torch.cuda.reset_peak_memory_stats();started=time.perf_counter();logs=[];retries=[]
    # Inspect all encoded lengths without performing optimization or final scoring.
    maximum=0
    for r in refs+[r for g in groups for r in g]:
        b,_=encode(s,r);maximum=max(maximum,int(b['input_ids'].shape[1]));del b
    for step,(g,ref) in enumerate(zip(groups,refs),1):
        for attempt in range(12):
            m.train();opt.zero_grad(set_to_none=True);loss_values=[]
            # Backward per presentation is algebraically the same CE mean and
            # avoids retaining four expanded-encoder graphs on an8GiB GPU.
            for r in [ref]+g:
                b,keys=encode(s,r)
                with torch.autocast('cuda',dtype=torch.float16):
                    vals=m(**b).logits[:,0].float();loss=torch.nn.functional.cross_entropy(vals[None,:],torch.tensor([keys.index(r['target'])],device='cuda'))
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                loss_values.append(float(loss.detach()));scaler.scale(loss/4).backward()
            scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
            if math.isfinite(norm):scaler.step(opt);scaler.update();break
            old=scaler.get_scale();scaler.step(opt);scaler.update();retries.append({'step':step,'scale':old,'next_scale':scaler.get_scale()})
            if scaler.get_scale()>=old:raise ValueError('Nonfinite step not skipped')
        else:raise ValueError('Repeated nonfinite gradient')
        logs.append({'step':step,'loss':sum(loss_values)/4,'gradient_norm':norm,'ids':[ref['id']]+[r['id'] for r in g]})
        if step%20==0:save(folder/'loss-log.json',logs);print('V60 TRAIN',arm,step,'/200 sec',round(time.perf_counter()-started),flush=True)
    if step!=200:raise ValueError('Budget mismatch')
    target=folder/'final-adapter';m.save_pretrained(target,safe_serialization=True,selected_adapters=[setup['adapter']])
    if arm=='B':target=target/'wide'
    m.eval()
    def probe():
        out=[]
        for r in groups[0]:
            b,_=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):out+=m(**b).logits[:,0].float().cpu().tolist()
        return out
    before=probe();delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in named.items())
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,load_file(str(target/'adapter_model.safetensors')),adapter_name=setup['adapter']);m.eval();after=probe();reload_error=max(abs(a-b) for a,b in zip(before,after))
    if delta<=0 or reload_error>1e-5:raise ValueError('Update/reload not verified')
    save(folder/'complete.json',{'steps':step,'presentations':800,'seconds':time.perf_counter()-started,'peak_GiB':torch.cuda.max_memory_allocated()/2**30,
        'max_tokens':maximum,'trainable_parameters':sum(p.numel() for p in params),'trainable_names':list(named),'initial_output_error':setup['initial_output_error'],
        'max_weight_change':delta,'reload_error':reload_error,'adapter_path':str(target.relative_to(ROOT)),
        'adapter_sha256':digest(target/'adapter_model.safetensors'),'retries':retries})
    del s,m,named,params,initial,opt,b,vals,loss;gc.collect();torch.cuda.empty_cache();verify()

def main():
    cfg=verify();status={'completed':[],'failed':{}}
    for arm in cfg['arms']:
        try:train(arm);status['completed'].append(arm)
        except Exception as exc:
            import traceback
            error={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()};status['failed'][arm]=error
            save(OUT/(arm+'-failed.json'),error);print('V60 FAILED',arm,str(exc),flush=True)
            gc.collect();__import__('torch').cuda.empty_cache()
        save(OUT/'training-status.json',status)
    save(OUT/'finals-frozen.json',{a:read(OUT/a/'complete.json') for a in status['completed']})
    print('V60 ALL FINALS FROZEN',status['completed'],flush=True)
if __name__=='__main__':main()
