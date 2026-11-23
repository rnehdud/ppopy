"""Fixed-budget action-only QLoRA + separate gold/frozen-parser evaluations."""
import copy,gc,math,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.prepared_learning_plan_v38 import TEACH,OUT,INITIAL,SEED,verify,read,save,digest
from scripts.selector_learning_v18 import load
from scripts.result_loop_split_v27 import Engine,encode
from demo.prepared_feedback_v38 import PreparedFeedbackSession
from agent.decision_context_v37r1 import decode


def interface_preflight():
    verify();cases={c['id']:c for c in read(TEACH/'cases.json')};rows=read(TEACH/'train.json')+read(TEACH/'heldout.json');from transformers import AutoTokenizer
    from scripts.prepared_learning_plan_v38 import MODEL
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;checked=0
    for c in cases.values():
        expected=sorted([r for r in rows if r['case_id']==c['id']],key=lambda r:r['step']);index=0
        def teacher(role,v):
            nonlocal index,checked
            if role!='action':raise ValueError('Gold preflight must not call symptom model')
            row=expected[index];index+=1;checked+=1
            if v!={k:row[k] for k in ['question','options','context']}:raise ValueError('Training/inference input mismatch')
            return {'raw_scores':{k:5. if k==row['target'] else 0. for k in v['options']}}
        s=PreparedFeedbackSession(teacher,c,tok,'gold');t=s.turn(c['text'])
        if index!=len(expected) or not t['model_stopped'] or t['after']!={**c['initial'],**c['expected_stored_patch']}:raise ValueError('Interface teaching replay incomplete')
    save(OUT/'interface-preflight.json',{'all_passed':True,'judgments_checked':checked,'conversations_checked':len(cases),'no_model_predictions':True,'teacher_only':True})
    print('V38 training/inference interface verified',checked,'judgments',flush=True)


def train():
    cfg=verify()
    if not read(OUT/'interface-preflight.json')['all_passed']:raise ValueError('Interface gate closed')
    folder=OUT/'train'
    if folder.exists():raise FileExistsError('Training protected')
    folder.mkdir();save(folder/'started.json',{'plan':digest(OUT/'plan.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    s=load(True,INITIAL);m=s.model;m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    named={n:p for n,p in m.named_parameters() if p.requires_grad}
    if not named or any('lora_' not in n for n in named):raise ValueError('Only action LoRA may train')
    params=list(named.values());initial={n:p.detach().cpu().clone() for n,p in named.items()};opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128.)
    rows=read(TEACH/'train.json');logs=[];overflows=[];fits=[]
    def assess(epoch):
        m.eval();correct=0;ce=0.;preds=[]
        for r in rows:
            b,keys=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):v=m(**b).logits[:,0].float()
            ce+=float(torch.nn.functional.cross_entropy(v.unsqueeze(0),torch.tensor([keys.index(r['target'])],device='cuda')));pred=keys[int(v.argmax())];correct+=pred==r['target'];preds.append({'id':r['id'],'target':r['target'],'prediction':pred,'scores':dict(zip(keys,v.cpu().tolist()))})
        fits.append({'epoch':epoch,'n':len(rows),'correct':correct,'CE':ce/len(rows)});save(folder/'fit.json',fits);save(folder/('fit-'+str(epoch)+'.json'),preds);print('V38 train fit',fits[-1],flush=True)
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
            if step%20==0:save(folder/'loss-log.json',logs);print('V38 step',step,'/',cfg['updates'],'seconds',round(time.perf_counter()-start),flush=True)
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
    del params,named,opt,m,s;gc.collect();torch.cuda.empty_cache();verify();print('V38 TRAIN COMPLETE',flush=True)


def grade(c,t):
    names={'record':'record_skin_symptoms','show':'read_skin_record'};expected=[names[k] for k in c['teacher_plan'] if k in names];actual=[e['tool'] for e in t['events']]
    expected_state={**c['initial'],**c['expected_stored_patch']};state=t['after']==expected_state;stopped=t['stop_reason']=='model_stop' if expected else t['stop_reason'] in ['model_stop','model_ask']
    writes=sum(e['tool']=='record_skin_symptoms' and e['result'].get('ok') is True for e in t['events']);strict=actual==expected and state and stopped and all(e['result'].get('ok') is True for e in t['events'])
    return {'strict':bool(strict),'state_ok':state,'actual_tools':actual,'expected_tools':expected,'required_write':bool(c['expected_stored_patch']),'required_write_completed':bool(c['expected_stored_patch'] and writes and state),'unwanted_write':bool(writes and not c['expected_stored_patch']),'stop_reason':t['stop_reason']}


def evaluate():
    cfg=verify();trained=OUT/'train/final-adapter';done=read(OUT/'train/complete.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'final_weights_fixed':done['adapter_sha256'],'no_test_selection':True})
    e=Engine(INITIAL);e.scorer.tokenizer.model_max_length=1000000;active='before';phase='before'
    def neural(role,v):
        nonlocal active
        needed='before' if role=='parser' else phase
        if active!=needed:e.activate(INITIAL if needed=='before' else trained);active=needed
        try:return e.score(v)
        except ValueError as exc:
            if str(exc)!='No truncation':raise
            raise ValueError('Input exceeds model context; no truncation') from exc
    cases=[c for c in read(TEACH/'cases.json') if c['split']=='heldout'];results=[];prefix=[]
    for label in ['before','after']:
        phase=label
        for upstream in ['gold','parser']:
            for i,c in enumerate(cases):
                s=PreparedFeedbackSession(neural,c,e.scorer.tokenizer,upstream);t=s.turn(c['text']);results.append({'case_id':c['id'],'phase':phase,'upstream':upstream,'family':c['family'],'trace':t,'scoring_inputs':s.scoring_inputs,'grade':grade(c,t)})
                if (i+1)%10==0:save(OUT/'episodes-partial.json',results);print('V38 eval',phase,upstream,i+1,'/30',flush=True)
        if active!=phase:e.activate(INITIAL if phase=='before' else trained);active=phase
        for r in read(TEACH/'heldout.json'):
            d=e.score({k:r[k] for k in ['question','options','context']});pred=max(d['raw_scores'],key=d['raw_scores'].get);prefix.append({'id':r['id'],'case_id':r['case_id'],'phase':phase,'target':r['target'],'prediction':pred,'correct':pred==r['target'],'score':d})
    save(OUT/'episodes.json',results);save(OUT/'gold-prefix.json',prefix);save(OUT/'evaluation-complete.json',{'episodes':len(results),'prefix_judgments':len(prefix),'actual_forwards':e.calls,'max_tokens':e.max_tokens,'no_deployment':True,'parser_sha256':digest(INITIAL/'adapter_model.safetensors'),'action_sha256':done['adapter_sha256']})
    verify();print('V38 EVALUATION COMPLETE',len(results),'episodes',flush=True)


if __name__=='__main__':
    action=sys.argv[1]
    if action=='preflight':interface_preflight()
    elif action=='train':train()
    elif action=='evaluate':evaluate()
    elif action=='all':interface_preflight();train();evaluate()
    else:raise ValueError(action)
