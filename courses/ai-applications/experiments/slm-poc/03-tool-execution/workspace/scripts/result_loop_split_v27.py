"""Fixed two-model comparison and tiny result-conditioned adaptation; no deployment."""
import copy, gc, hashlib, math, random, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from scripts.result_loop_split_data_v27 import DATA, OUT, SEED, MODEL, SELECTOR, LATEST, GATE, verify, read, save, digest, readlines
from scripts.selector_learning_v18 import load
from agent.result_loop_probe_v26 import run_episode, probe_states, grade_episode, stable
from agent.result_loop_split_v27 import dispatch


class Engine:
    def __init__(self, path):
        self.scorer = load(adapter=path); self.cache = {}; self.calls = 0; self.max_tokens = 0
        self.weight = digest(path/'adapter_model.safetensors')

    def activate(self, path):
        from peft import set_peft_model_state_dict
        from safetensors.torch import load_file
        set_peft_model_state_dict(self.scorer.model, load_file(str(path/'adapter_model.safetensors')))
        self.scorer.model.eval(); self.weight = digest(path/'adapter_model.safetensors')

    def score(self, v):
        import torch
        key = self.weight + stable(v)
        if key in self.cache: return copy.deepcopy(self.cache[key])
        b, keys = encode(self.scorer, v)
        with torch.inference_mode(), torch.autocast('cuda', dtype=torch.float16):
            vals = self.scorer.model(**b).logits[:,0].float().cpu().tolist()
        if not all(math.isfinite(x) for x in vals): raise ValueError('Nonfinite logit')
        n = int(b['input_ids'].shape[1]); self.max_tokens = max(n, self.max_tokens); self.calls += 1
        r = {'raw_scores': dict(zip(keys, vals)), 'model_input': v, 'tokens': n,
             'adapter_sha256': self.weight, 'input_ids_sha256': hashlib.sha256(b['input_ids'].cpu().numpy().tobytes()).hexdigest()}
        self.cache[key] = copy.deepcopy(r); return r


def encode(s, v):
    keys = list(v['options'])
    b = s.tokenizer([v['question']+' '+x for x in v['options'].values()], [v['context']]*len(keys), padding=True, truncation=False, return_tensors='pt').to('cuda')
    if b['input_ids'].shape[1] > 512: raise ValueError('No truncation')
    return b, keys


def evaluate_pack(label, cases, selector, gate, threshold):
    # Neither oracle labels nor hidden fixture state is passed into this chooser.
    def choose(request, tools, events, fmt, order):
        return dispatch(request, tools, events, order, selector.score, gate.score, threshold)
    snapshots, episodes = [], []
    for c in cases:
        for state, events in probe_states(c).items():
            snapshots.append({'case_id': c['id'], 'state': state, 'decision': choose(c['request'], [c['check'],c['act']], events, 'json', c['option_order'])})
        for condition in [True, False]: episodes.append(run_episode(c, condition, choose, 'json', 3))
    save(OUT/(label+'-snapshots.json'), snapshots); save(OUT/(label+'-episodes.json'), episodes)
    print('SCORED', label, len(snapshots), 'snapshots', len(episodes), 'episodes', flush=True)


def baseline():
    cfg = verify()
    if (OUT/'baseline-started.json').exists(): raise FileExistsError('Baseline protected')
    save(OUT/'baseline-started.json', {'protocol': digest(DATA/'protocol.json')})
    s, g = Engine(SELECTOR), Engine(GATE); cs = read(DATA/'known-cases.json')
    evaluate_pack('existing_pair-known', cs, s, g, cfg['gate_threshold'])
    s.activate(LATEST)
    evaluate_pack('before-known', cs, s, g, cfg['gate_threshold'])
    # Known-case diagnostic determines only whether adaptation is necessary.
    gold = read(DATA/'oracle.json')['known']; es = read(OUT/'before-known-episodes.json')
    passed = sum(grade_episode(e, gold[e['case_id']]['positive' if e['condition'] else 'negative'])['strict_pass'] for e in es)
    save(OUT/'baseline-complete.json', {'known_strict': passed, 'n':20, 'adapt': passed < 20,
        'selector_max_tokens':s.max_tokens,'gate_max_tokens':g.max_tokens, 'no_fresh_scoring':True})
    del s,g; gc.collect(); __import__('torch').cuda.empty_cache(); verify()


def train(role):
    cfg = verify()
    if not read(OUT/'baseline-complete.json')['adapt']: raise ValueError('No diagnostic need to adapt')
    folder = OUT/role
    if folder.exists(): raise FileExistsError('Training protected')
    folder.mkdir(); save(folder/'started.json', {'protocol': digest(DATA/'protocol.json')})
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    rows = read(DATA/(role+'-train.json')); s = load(True, LATEST if role=='selector' else GATE); m=s.model
    m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    named = {n:p for n,p in m.named_parameters() if p.requires_grad}
    if not named or any('lora_' not in n for n in named): raise ValueError('Only LoRA may train')
    params = list(named.values()); initial = {n:p.detach().cpu().clone() for n,p in named.items()}
    opt = torch.optim.AdamW(params, lr=cfg['lr'], weight_decay=0, foreach=False)
    scaler = torch.amp.GradScaler('cuda', init_scale=128.); logs=[]; curves=[]; retries=[]
    def assess(epoch):
        m.eval(); correct=0; policy_correct=0; loss_sum=0.; preds=[]
        for r in rows:
            b,keys=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16): vals=m(**b).logits[:,0].float()
            target=keys.index(r['target']); loss_sum+=float(torch.nn.functional.cross_entropy(vals.unsqueeze(0),torch.tensor([target],device='cuda')))
            vs=vals.cpu().tolist(); sc=dict(zip(keys,vs)); pred=max(keys,key=sc.get)
            policy=('yes' if sc['yes']-sc['no']>=cfg['gate_threshold'] else 'no') if role=='gate' else pred
            correct+=pred==r['target']; policy_correct+=policy==r['target']; preds.append({'id':r['id'],'target':r['target'],'predicted':pred,'policy':policy,'scores':sc})
        entry={'epoch':epoch,'n':len(rows),'argmax_correct':correct,'policy_correct':policy_correct,'mean_CE':loss_sum/len(rows)}
        curves.append(entry);save(folder/'curve.json',curves);save(folder/('own-epoch-'+str(epoch)+'.json'),preds);print(role,entry,flush=True)
    assess(0)
    def update(group):
        for _ in range(12):
            opt.zero_grad(set_to_none=True);m.train();total=0.
            for r in group:
                b,keys=encode(s,r)
                with torch.autocast('cuda',dtype=torch.float16): loss=torch.nn.functional.cross_entropy(m(**b).logits[:,0].float().unsqueeze(0),torch.tensor([keys.index(r['target'])],device='cuda'))
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                scaler.scale(loss/len(group)).backward();total+=float(loss.detach())/len(group)
            scaler.unscale_(opt);norm=float(torch.nn.utils.clip_grad_norm_(params,1.))
            if math.isfinite(norm):scaler.step(opt);scaler.update();return total,norm
            before=scaler.get_scale();scaler.step(opt);scaler.update();retries.append({'before':before,'after':scaler.get_scale()})
            if scaler.get_scale()>=before:raise ValueError('Overflow not skipped')
        raise ValueError('Repeated nonfinite gradient')
    start=time.perf_counter();step=0
    for epoch in range(1,cfg['epochs']+1):
        schedule=rows.copy();random.Random(SEED+epoch).shuffle(schedule)
        for offset in range(0,len(schedule),cfg['logical_batch']):
            group=schedule[offset:offset+cfg['logical_batch']];loss,norm=update(group);step+=1
            logs.append({'step':step,'epoch':epoch,'ids':[r['id'] for r in group],'loss':loss,'gradient_norm':norm})
        save(folder/'loss-log.json',logs)
        print(role,'epoch',epoch,'step',step,'seconds',round(time.perf_counter()-start),flush=True)
        if epoch in cfg['read_epochs']:assess(epoch)
    if step!=cfg['steps'][role]:raise ValueError('Training budget mismatch')
    target=folder/'final-adapter';m.save_pretrained(target,safe_serialization=True);m.eval()
    def probe():
        results=[]
        for r in rows[:2]:
            b,_=encode(s,r)
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):results.extend(m(**b).logits[:,0].float().cpu().tolist())
        return results
    before=probe();delta=max(float((p.detach().cpu()-initial[n]).abs().max()) for n,p in named.items())
    with torch.no_grad():params[0].add_(.01)
    set_peft_model_state_dict(m,load_file(str(target/'adapter_model.safetensors')));m.eval();after=probe();err=max(abs(x-y) for x,y in zip(before,after))
    if delta<=0 or err>1e-5:raise ValueError('Weight update/reload failed')
    save(folder/'complete.json',{'steps':step,'seen':len(rows)*cfg['epochs'],'unique_training_rows':len(rows),'max_weight_change':delta,'reload_logit_error':err,'overflows':retries,'seconds':time.perf_counter()-start,'adapter_sha256':digest(target/'adapter_model.safetensors'),'peak_GiB':torch.cuda.max_memory_allocated()/2**30})
    del params,named,opt,m,s;gc.collect();torch.cuda.empty_cache();verify();print('TRAIN COMPLETE',role,flush=True)


def retention(label, selector, gate, threshold):
    from scripts.selector_broad_v20 import score
    from scripts.when2call_operational_data_v1 import action_row
    from scripts.tool_split_data_v1 import gate_view as legacy_gate, gold_index
    refs=readlines(ROOT/'data/processed/selector-interface-v18/reference.jsonl')
    p=score(selector.scorer,refs,label+' selector retention');save(OUT/(label+'-reference600.json'),p)
    if label=='before':
        old=read(ROOT/'output/diagnostics/selector-transfer-v24/new-reference.json')
        changed=[id_ for id_ in p if p[id_]['predicted']!=old[id_]['predicted']]
        err=max(abs(p[i]['scores'][k]-old[i]['scores'][k]) for i in p for k in p[i]['scores'])
        save(OUT/'before-retention-replay.json',{'changed':changed,'max_logit_error':err})
        if changed or err>.05:raise ValueError('Known selector replay mismatch')
    rows=readlines(ROOT/'data/processed/tool-split-pilot-v1/korean_seen_control.jsonl');es=[]
    for r in rows:
        v,reason=action_row(r)
        if reason:raise ValueError(reason)
        v={k:v[k] for k in ['question','options','context']};v['options']={k:x for k,x in v['options'].items() if k!='no_tool'}
        rank=selector.score(v);chosen=max(v['options'],key=rank['raw_scores'].get)
        gv=legacy_gate(r,int(chosen.split('_')[1]));gv={k:gv[k] for k in ['question','options','context']};checked=gate.score(gv)
        margin=checked['raw_scores']['yes']-checked['raw_scores']['no'];pred=chosen if margin>=threshold else 'no_tool'
        expected=f'tool_{gold_index(r):03d}' if r['reference_calls'] else 'no_tool'
        es.append({'id':r['id'],'expected':expected,'predicted':pred,'correct':expected==pred,'selector':rank,'gate':checked,'margin':margin})
    save(OUT/(label+'-korean30.json'),es)


def evaluate():
    cfg=verify();trained=read(OUT/'baseline-complete.json')['adapt']
    if trained:
        for role in ['selector','gate']:read(OUT/role/'complete.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'protocol':digest(DATA/'protocol.json'),'both_weights_fixed_before_fresh':True})
    s,g=Engine(LATEST),Engine(GATE)
    arms=[('before',LATEST,GATE)]
    if trained:
        arms += [('selector_only',OUT/'selector/final-adapter',GATE),('gate_only',LATEST,OUT/'gate/final-adapter'),('both',OUT/'selector/final-adapter',OUT/'gate/final-adapter')]
    for label,sp,gp in arms:
        s.activate(sp);g.activate(gp)
        evaluate_pack(label+'-fresh',read(DATA/'fresh-cases.json'),s,g,cfg['gate_threshold'])
        if label!='before':evaluate_pack(label+'-known',read(DATA/'known-cases.json'),s,g,cfg['gate_threshold'])
        if label in ['before','both']:retention(label,s,g,cfg['gate_threshold'])
    save(OUT/'evaluation-complete.json',{'arms':[a[0] for a in arms],'selector_actual_forwards':s.calls,'gate_actual_forwards':g.calls,'selector_max_tokens':s.max_tokens,'gate_max_tokens':g.max_tokens,'no_deployment':True,'no_test_based_tuning':True})
    verify();del s,g;gc.collect();__import__('torch').cuda.empty_cache();print('V27 EVALUATION COMPLETE',flush=True)


if __name__=='__main__':
    phase=sys.argv[1]
    if phase=='baseline':baseline()
    elif phase=='evaluate':evaluate()
    elif phase in ['selector','gate']:train(phase)
    elif phase=='all':
        baseline()
        if read(OUT/'baseline-complete.json')['adapt']:train('selector');train('gate')
        evaluate()
    else:raise ValueError(phase)
