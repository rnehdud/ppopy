"""One action-only continuation; no parser changes or live deployment."""
import copy,gc,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.intent_observation_data_v39 import DATA,OUT,OLD_DATA,START,PARSER,SEED,MODEL,read,save,digest,verify
from scripts.selector_learning_v18 import load
from scripts.result_loop_split_v27 import Engine,encode
from scripts.prepared_learning_v38 import grade as previous_grade
from demo.prepared_feedback_v38 import PreparedFeedbackSession
from demo.provided_feedback_v39 import ProvidedFeedbackSession


def session(neural,c,tok,mode):
    return ProvidedFeedbackSession(neural,c,tok) if mode=='provided' else PreparedFeedbackSession(neural,c,tok,mode)


def grade(c,t):
    g=previous_grade(c,t);g['previous_metric_strict']=g['strict']
    terminal=t['steps'][-1]['decision']['domain_decision']['choice'] if t['steps'] else None
    g['terminal_expected']=c['teacher_plan'][-1];g['terminal_observed']=terminal;g['terminal_ok']=terminal==g['terminal_expected']
    g['strict']=g['strict'] and g['terminal_ok']
    return g


def train():
    cfg=verify()
    if not read(OUT/'data-audit.json')['all_passed']:raise ValueError('Data gate closed')
    folder=OUT/'train'
    if folder.exists():raise FileExistsError('Training protected')
    folder.mkdir();save(folder/'started.json',{'plan':digest(OUT/'plan.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    s=load(True,START);m=s.model;m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    named={n:p for n,p in m.named_parameters() if p.requires_grad}
    if not named or any('lora_' not in n for n in named):raise ValueError('Only action LoRA may train')
    params=list(named.values());initial={n:p.detach().cpu().clone() for n,p in named.items()};opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.)
    rows=read(DATA/'train.json');logs=[];overflows=[];fits=[]
    def assess(epoch):
        m.eval();correct=0;ce=0.;preds=[]
        for r in rows:
            b,keys=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):v=m(**b).logits[:,0].float()
            ce+=float(torch.nn.functional.cross_entropy(v.unsqueeze(0),torch.tensor([keys.index(r['target'])],device='cuda')));pred=keys[int(v.argmax())];correct+=pred==r['target'];preds.append({'id':r['id'],'target':r['target'],'prediction':pred,'scores':dict(zip(keys,v.cpu().tolist()))})
        fits.append({'epoch':epoch,'n':len(rows),'correct':correct,'CE':ce/len(rows)});save(folder/'fit.json',fits);save(folder/('fit-'+str(epoch)+'.json'),preds);print('V39 train fit',fits[-1],flush=True)
    def update(group):
        for attempt in range(12):
            opt.zero_grad(set_to_none=True);m.train();total=0.
            for r in group:
                b,keys=encode(s,r)
                with torch.autocast('cuda',dtype=torch.float16):loss=torch.nn.functional.cross_entropy(m(**b).logits[:,0].float().unsqueeze(0),torch.tensor([keys.index(r['target'])],device='cuda'))
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                scaler.scale(loss/len(group)).backward();total+=float(loss.detach())/len(group)
            scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
            if math.isfinite(norm):scaler.step(opt);scaler.update();return total,norm
            before=scaler.get_scale();scaler.step(opt);scaler.update();overflows.append({'scale_before':before,'scale_after':scaler.get_scale()})
            if scaler.get_scale()>=before:raise ValueError('Overflow was not skipped')
        raise ValueError('Repeated gradient overflow')
    assess(0);start=time.perf_counter();step=0
    for epoch in range(1,cfg['epochs']+1):
        order=list(range(len(rows)));random.Random(SEED+epoch).shuffle(order)
        for j in range(0,len(rows),cfg['effective_batch']):
            ids=order[j:j+cfg['effective_batch']];loss,norm=update([rows[i] for i in ids]);step+=1;logs.append({'step':step,'epoch':epoch,'ids':[rows[i]['id'] for i in ids],'loss':loss,'gradient_norm':norm})
            if step%20==0:save(folder/'loss-log.json',logs);print('V39 step',step,'/',cfg['updates'],'seconds',round(time.perf_counter()-start),flush=True)
        save(folder/'loss-log.json',logs)
    if step!=cfg['updates']:raise ValueError('Fixed update budget changed')
    assess(cfg['epochs']);target=folder/'final-adapter';m.save_pretrained(target,safe_serialization=True);m.eval()
    def probe():
        result=[]
        for r in rows[:2]:
            b,_=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):result+=m(**b).logits[:,0].float().cpu().tolist()
        return result
    before=probe();delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in named.items())
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,load_file(str(target/'adapter_model.safetensors')));m.eval();after=probe();err=max(abs(a-b) for a,b in zip(before,after))
    if delta<=0 or err>1e-5:raise ValueError('Update/reload failed')
    save(folder/'complete.json',{'steps':step,'rows':len(rows),'row_exposures':len(rows)*cfg['epochs'],'max_weight_change':delta,'reload_logit_error':err,'overflows':overflows,'seconds':time.perf_counter()-start,'peak_GiB':torch.cuda.max_memory_allocated()/2**30,'adapter_sha256':digest(target/'adapter_model.safetensors')})
    del params,named,opt,m,s;gc.collect();torch.cuda.empty_cache();verify();print('V39 TRAIN COMPLETE',flush=True)


def evaluate():
    verify();trained=OUT/'train/final-adapter';done=read(OUT/'train/complete.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'final_weights_fixed':done['adapter_sha256'],'no_test_selection':True})
    e=Engine(START);e.scorer.tokenizer.model_max_length=1000000;active=START;phase='before'
    def neural(role,v):
        nonlocal active
        needed=PARSER if role=='parser' else START if phase=='before' else trained
        if active!=needed:e.activate(needed);active=needed
        try:return e.score(v)
        except ValueError as exc:
            if str(exc)!='No truncation':raise
            raise ValueError('Input exceeds model context; no truncation') from exc
    packs=[('new',[c for c in read(DATA/'cases.json') if c['split']=='heldout'],['gold','provided','parser']),
      ('seen_retention',[c for c in read(OLD_DATA/'cases.json') if c['split']=='heldout'],['gold','parser'])]
    episodes=[]
    for label in ['before','after']:
        phase=label
        for group,cases,modes in packs:
            for mode in modes:
                for i,c in enumerate(cases):
                    s=session(neural,c,e.scorer.tokenizer,mode);t=s.turn(c['text']);episodes.append({'case_id':c['id'],'phase':phase,'upstream':mode,'group':group,'family':c['family'],'trace':t,'scoring_inputs':s.scoring_inputs,'grade':grade(c,t)})
                    if (i+1)%30==0:save(OUT/'episodes-partial.json',episodes);print('V39 eval',phase,group,mode,i+1,'/',len(cases),flush=True)
    save(OUT/'episodes.json',episodes);save(OUT/'evaluation-complete.json',{'episodes':len(episodes),'actual_forwards':e.calls,'max_tokens':e.max_tokens,'no_deployment':True,'parser_sha256':digest(PARSER/'adapter_model.safetensors'),'start_sha256':digest(START/'adapter_model.safetensors'),'action_sha256':done['adapter_sha256']})
    if len(episodes)!=840:raise ValueError('Evaluation incomplete')
    verify();print('V39 EVALUATION COMPLETE',len(episodes),'episodes',flush=True)


if __name__=='__main__':
    task=sys.argv[1]
    if task=='train':train()
    elif task=='evaluate':evaluate()
    elif task=='all':train();evaluate()
    else:raise ValueError(task)
