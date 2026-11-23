"""Common real-file execution evaluation, oracle harness kept separate."""
import copy,gc,json,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.rollout_data_v60 import DATA,OUT,START,verify,read,save,digest
from agent.rollout_files_v60 import Files,FileSession,names,grade

class Oracle:
    def __init__(self,ids):self.ids=ids;self.plan=[];self.index=0
    def score(self,v):
        role=self.plan[self.index] if self.index<len(self.plan) else 'none';self.index+=1
        target=self.ids.get(role,role);return {'raw_scores':{k:10. if k==target else -10. for k in v['options']}}

def public(c):return {k:copy.deepcopy(c[k]) for k in ('id','family','payload','available','order','order_seed')}

def harness_audit(rows,tok):
    parent=Path(tempfile.mkdtemp(prefix='rollout60-harness-',dir=ROOT/'tmp'));maximum=0;checks=[]
    for c in rows:
        service=Files(parent/c['id'].replace(':','-'),c['family'],c['payload']);oracle=Oracle(names(c['family']))
        agent=FileSession(service,public(c),oracle.score,tok)
        for t in c['turns']:
            oracle.plan=t['roles'];oracle.index=0;trace=agent.turn(t['text']);g=grade(t,trace,service)
            maximum=max(maximum,max(x['encoding']['tokens'] for x in trace['model_inputs']))
            checks.append({'case':c['id'],'pass':g['goal_and_stop'],'stop':trace['stop_reason']})
    return {'cases':len(rows),'turns':len(checks),'all_goals_and_model_stop':all(x['pass'] for x in checks),'failures':[x for x in checks if not x['pass']],
        'max_tokens':maximum,'oracle_is_harness_only':True}

def evaluate_files(label,engine):
    path=OUT/(label+'-files.json')
    if path.exists():raise FileExistsError(path)
    results=[];started=time.perf_counter()
    for i,c in enumerate(read(DATA/'file-cases.json')):
        service=Files(OUT/'work'/label/c['id'].replace(':','-'),c['family'],c['payload'])
        agent=FileSession(service,public(c),engine.score,engine.scorer.tokenizer);turns=[]
        for t in c['turns']:
            trace=agent.turn(t['text']);g=grade(t,trace,service)
            turns.append({'text':t['text'],'expected_roles':t['roles'],'expected_output':t['output'],'trace':trace,'grade':g,'actual':service.snapshot()})
        results.append({'id':c['id'],'family':c['family'],'split':c['split'],'kind':c['kind'],'style':c['style'],'turns':turns,
            'goal_and_stop':all(t['grade']['goal_and_stop'] for t in turns),'goal_ok':all(t['grade']['goal_ok'] for t in turns)})
        if (i+1)%40==0:print('V60 FILES',label,i+1,'/160 seconds',round(time.perf_counter()-started),flush=True)
    save(path,{'label':label,'adapter_sha256':engine.weight,'episodes':results,'seconds':time.perf_counter()-started})

def evaluate_retention(label,engine):
    from agent.generic_fixture_v41 import Session
    from scripts.generic_pair_learning_v41 import generic_grade
    path=OUT/(label+'-retention.json')
    if path.exists():raise FileExistsError(path)
    old=[]
    for r in read(ROOT/'data/processed/description-pairs-v41/train.json')[:360]:
        scores=engine.score({k:r[k] for k in ('question','options','context')});pred=max(r['options'],key=scores['raw_scores'].get)
        old.append({'id':r['id'],'correct':pred==r['target'],'prediction':pred,'target':r['target']})
    prior=[]
    for folder,group in [('read-continue-v45','matched'),('description-pairs-v41','previous')]:
        for c in read(ROOT/'data/processed'/folder/'cases.json'):
            if c['split']!='test':continue
            s=Session(c,engine.score,engine.scorer.tokenizer);trace=s.run();prior.append({'id':c['id'],'group':group,'trace':trace,'grade':generic_grade(c,trace)})
    # Source fit is a diagnostic only, never fresh accuracy.
    fit=[]
    for r in read(OUT/'visited-label-bank.json'):
        score=engine.score({k:r[k] for k in ('question','options','context')});pred=max(r['options'],key=score['raw_scores'].get)
        fit.append({'id':r['id'],'stage':r['stage'],'initially_wrong':r['wrong'],'correct':pred==r['target']})
    save(path,{'label':label,'old360':old,'previous':prior,'training_fit':fit,'adapter_sha256':engine.weight})

def main():
    plan=verify();finals=read(OUT/'finals-frozen.json')
    if (OUT/'evaluation-started.json').exists():raise FileExistsError('Evaluation protected')
    save(OUT/'evaluation-started.json',{'frozen_finals':{k:v['adapter_sha256'] for k,v in finals.items()}})
    from scripts.result_loop_split_v27 import Engine
    completed=[];failures={}
    paths={'initial':START,'v57_reference':ROOT/'output/diagnostics/additive-isolation-v57/old_plus_new/final-adapter'}
    paths.update({k:ROOT/v['adapter_path'] for k,v in finals.items()})
    for label,path in paths.items():
        engine=None
        try:
            engine=Engine(path);evaluate_files(label,engine);evaluate_retention(label,engine);completed.append(label)
        except Exception as exc:
            import traceback
            error={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()};failures[label]=error;save(OUT/(label+'-evaluation-failed.json'),error)
        finally:
            del engine;gc.collect();__import__('torch').cuda.empty_cache()
    verify();save(OUT/'ranker-evaluation-complete.json',{'completed':completed,'failed':failures,'no_deployment':True})
    print('V60 RANKER EVAL COMPLETE',completed,flush=True)
if __name__=='__main__':main()
