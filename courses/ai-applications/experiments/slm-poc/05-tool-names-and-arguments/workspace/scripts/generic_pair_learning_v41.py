"""Equal-data CE vs CE+.2JS; fixed final checkpoints, frozen-family evaluation."""
import copy,gc,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.generic_pair_data_v41 import DATA,OUT,OLD_DATA,START,PARSER,MODEL,SEED,read,save,digest,verify,units
from scripts.selector_learning_v18 import load
from scripts.result_loop_split_v27 import Engine,encode
from agent.generic_fixture_v41 import Session,World
from demo.prepared_feedback_v38 import PreparedFeedbackSession
from scripts.intent_observation_learning_v39 import grade as skin_grade


def objective(logits,rows,weight):
    import torch
    ce=sum(torch.nn.functional.cross_entropy(v.float().unsqueeze(0),torch.tensor([list(r['options']).index(r['target'])],device=v.device)) for v,r in zip(logits,rows))/len(rows)
    js=ce*0
    if len(rows)==2 and rows[0].get('pair_id') and rows[0]['pair_id']==rows[1].get('pair_id'):
        roles=[k for k in ['a','b','c','ask','none'] if k in rows[0]['semantic_keys'].values()];ps=[]
        for v,r in zip(logits,rows):
            keys=list(r['options']);mapping={sem:keys.index(k) for k,sem in r['semantic_keys'].items()};ps.append(v.float().softmax(-1)[[mapping[k] for k in roles]])
        p=torch.stack(ps);mid=p.mean(0);js=(p*(p.clamp_min(1e-8).log()-mid.clamp_min(1e-8).log())).sum(-1).mean().clamp_min(0)
    return ce+weight*js,ce,js


def train(arm):
    cfg=verify();weight=cfg['arms'][arm];folder=OUT/arm
    if folder.exists():raise FileExistsError('Training arm protected')
    folder.mkdir();save(folder/'started.json',{'plan':digest(OUT/'plan.json'),'arm':arm,'js_weight':weight})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    s=load(True,START);m=s.model;m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    named={n:p for n,p in m.named_parameters() if p.requires_grad}
    if not named or any('lora_' not in n for n in named):raise ValueError('Only LoRA can train')
    params=list(named.values());initial={n:p.detach().cpu().clone() for n,p in named.items()};opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.)
    rows=read(DATA/'train.json');logs=[];retries=[]
    def probes():
        m.eval();ans=[]
        for r in rows[:2]:
            b,_=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):ans+=m(**b).logits[:,0].float().cpu().tolist()
        return ans
    save(folder/'initial-probe.json',probes());start=time.perf_counter();step=0
    for epoch in range(1,cfg['epochs']+1):
        for group in units(rows,SEED+epoch):
            for attempt in range(12):
                opt.zero_grad(set_to_none=True);m.train();vs=[]
                with torch.autocast('cuda',dtype=torch.float16):
                    for r in group:
                        b,_=encode(s,r);vs.append(m(**b).logits[:,0])
                    loss,ce,js=objective(vs,group,weight)
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                scaler.scale(loss).backward();scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
                if math.isfinite(norm):scaler.step(opt);scaler.update();break
                before=scaler.get_scale();scaler.step(opt);scaler.update();retries.append({'step':step+1,'attempt':attempt,'old_scale':before,'new_scale':scaler.get_scale()})
                if scaler.get_scale()>=before:raise ValueError('Overflow not skipped')
            else:raise ValueError('Repeated overflow')
            step+=1;logs.append({'step':step,'epoch':epoch,'ids':[r['id'] for r in group],'loss':float(loss.detach()),'ce':float(ce.detach()),'js':float(js.detach()),'norm':norm})
            if step%20==0:save(folder/'loss-log.json',logs);print('V41',arm,step,'/',cfg['updates'],'seconds',round(time.perf_counter()-start),flush=True)
    if step!=cfg['updates']:raise ValueError('Fixed budget changed')
    save(folder/'loss-log.json',logs);target=folder/'final-adapter';m.save_pretrained(target,safe_serialization=True);before=probes();delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in named.items())
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,load_file(str(target/'adapter_model.safetensors')));after=probes();error=max(abs(a-b) for a,b in zip(before,after))
    if delta<=0 or error>1e-5:raise ValueError('Update/reload check failed')
    m.eval();correct=0;fit=[]
    for r in rows:
        b,keys=encode(s,r)
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):vals=m(**b).logits[:,0].float().cpu().tolist()
        scores=dict(zip(keys,vals));pred=max(keys,key=scores.get);correct+=pred==r['target'];fit.append({'id':r['id'],'prediction':pred,'target':r['target'],'scores':scores})
    save(folder/'training-fit.json',{'n':len(rows),'correct':correct,'predictions':fit})
    save(folder/'complete.json',{'steps':step,'rows':len(rows),'exposures':len(rows)*cfg['epochs'],'max_weight_change':delta,'reload_error':error,'retries':retries,'seconds':time.perf_counter()-start,'peak_GiB':torch.cuda.max_memory_allocated()/2**30,'adapter_sha256':digest(target/'adapter_model.safetensors')})
    del loss,ce,js,vs,params,named,opt,m,s;gc.collect();torch.cuda.empty_cache();verify();print('V41 TRAIN COMPLETE',arm,flush=True)


def generic_grade(c,t):
    expected=[c['ids'][r] for r in c['teacher_plan'] if r in ['a','b','c']];actual=[e['tool'] for e in t['events']];w=World(c['family'],c['initial'],c['binding'])
    for r in c['teacher_plan']:
        if r in ['a','b','c']:w.invoke(r)
    state=t['after']==w.state;stop=t['stop_reason']==('model_ask' if c['teacher_plan'][-1]=='ask' else 'model_stop');ok=all(e['result'].get('ok') for e in t['events'])
    return {'strict':bool(actual==expected and state and stop and ok),'state_ok':state,'tools_match':actual==expected,'expected_tools':expected,'actual_tools':actual,
      'required_tools':bool(expected),'required_tools_completed':bool(expected and actual==expected and state and ok),'unrequested_state_change':c['intent'] in ['a','no_tool','missing_b'] and t['after']!=c['initial'],
      'two_operation':len(expected)==2,'stop_reason':t['stop_reason']}


def evaluate():
    cfg=verify();paths={'baseline':START,**{a:OUT/a/'final-adapter' for a in cfg['arms']}}
    for arm in cfg['arms']:read(OUT/arm/'complete.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'fixed_models':{k:digest(v/'adapter_model.safetensors') for k,v in paths.items()},'no_test_selection':True})
    e=Engine(START);e.scorer.tokenizer.model_max_length=1000000;active=START;phase='baseline';episodes=[];snapshots=[]
    def neural(role,v):
        nonlocal active
        needed=PARSER if role=='parser' else paths[phase]
        if active!=needed:e.activate(needed);active=needed
        try:return e.score(v)
        except ValueError as exc:
            if str(exc)!='No truncation':raise
            raise ValueError('Input exceeds model context') from exc
    cs=read(DATA/'cases.json');old=[c for c in read(OLD_DATA/'cases.json') if c['split']=='heldout'];natural=read(ROOT/'output/diagnostics/natural-read-v39/cases.json')
    for phase in paths:
        for split in ['dev','test']:
            pack=[c for c in cs if c['split']==split]
            for i,c in enumerate(pack):
                s=Session(c,lambda v:neural('action',v),e.scorer.tokenizer);t=s.run();episodes.append({'case_id':c['id'],'group':split,'phase':phase,'pair_id':c['pair_id'],'family':c['family'],'trace':t,'scoring_inputs':s.inputs,'grade':generic_grade(c,t)})
            for r in read(DATA/(split+'.json')):
                v={k:r[k] for k in ['question','options','context']};sc=neural('action',v);pred=max(v['options'],key=sc['raw_scores'].get);snapshots.append({'id':r['id'],'case_id':r['case_id'],'pair_id':r['pair_id'],'split':split,'phase':phase,'target':r['target'],'prediction':pred,'correct':pred==r['target'],'score':sc})
            save(OUT/'episodes-partial.json',episodes);print('V41 eval',phase,split,len(pack),'episodes',flush=True)
        for group,pack,modes in [('seen_skin',old,['gold','parser']),('seen_plain_read',natural,['parser'])]:
            for mode in modes:
                for c in pack:
                    s=PreparedFeedbackSession(neural,c,e.scorer.tokenizer,mode);t=s.turn(c['text']);episodes.append({'case_id':c['id'],'group':group,'phase':phase,'upstream':mode,'trace':t,'scoring_inputs':s.scoring_inputs,'grade':skin_grade(c,t)})
                save(OUT/'episodes-partial.json',episodes);print('V41 eval',phase,group,mode,len(pack),'episodes',flush=True)
    save(OUT/'episodes.json',episodes);save(OUT/'snapshots.json',snapshots);save(OUT/'evaluation-complete.json',{'episodes':len(episodes),'snapshots':len(snapshots),'actual_forwards':e.calls,'max_tokens':e.max_tokens,'no_deployment':True})
    if len(episodes)!=552 or len(snapshots)!=504:raise ValueError('Incomplete evaluation')
    verify();print('V41 EVALUATION COMPLETE',flush=True)


if __name__=='__main__':
    task=sys.argv[1]
    if task in ['regular','consistent']:train(task)
    elif task=='evaluate':evaluate()
    elif task=='all':train('regular');train('consistent');evaluate()
    else:raise ValueError(task)
