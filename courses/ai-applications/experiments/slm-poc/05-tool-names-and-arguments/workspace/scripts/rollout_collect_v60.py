"""Collect actual initial-policy decisions on TRAIN cases only, then label offline."""
import collections,copy,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.rollout_data_v60 import DATA,OUT,START,SEED,verify,read,save,digest
from scripts.result_loop_split_v27 import Engine
from agent.generic_fixture_v41 import Session
from agent.rollout_teacher_v60 import row_for

def draw(pool,n,rng):
    if not pool:raise ValueError('No observed examples in required stage')
    wrong=[r for r in pool if r['wrong']];right=[r for r in pool if not r['wrong']]
    # Every distinct observed wrong input first; fill remaining budget by shuffled
    # rounds of the whole stage. No fabricated post-error states or gold rollout.
    rng.shuffle(wrong);result=copy.deepcopy(wrong[:n])
    while len(result)<n:
        cycle=copy.deepcopy(pool);rng.shuffle(cycle);result+=cycle[:n-len(result)]
    return result

def main():
    verify()
    if (OUT/'collection-complete.json').exists():raise FileExistsError('Collection protected')
    engine=Engine(START);bank=[];excluded=[];traces=[];seen={}
    for i,c in enumerate(read(DATA/'training-cases.json')):
        session=Session(c,engine.score,engine.scorer.tokenizer);trace=session.run(max_steps=3)
        traces.append({'id':c['id'],'trace':trace,'inputs':session.inputs})
        for j,entry in enumerate(session.inputs):
            if 'response' not in entry:excluded.append({'id':c['id'],'step':j,'reason':entry.get('error','no_response')});continue
            row,reason=row_for(c,entry,j)
            if row is None:excluded.append({'id':c['id'],'step':j,'reason':reason});continue
            key=__import__('json').dumps({k:row[k] for k in ('question','options','context')},ensure_ascii=False,sort_keys=True)
            if key in seen:
                if seen[key]!=row['target']:raise ValueError('Conflicting visible labels')
                continue
            seen[key]=row['target'];bank.append(row)
        if (i+1)%20==0:print('V60 COLLECT',i+1,'/120',flush=True)
    save(OUT/'training-rollouts.json',traces);save(OUT/'excluded-labels.json',excluded);save(OUT/'visited-label-bank.json',bank)
    rng=random.Random(SEED);draws=[]
    for stage,n in [('start',60),('continue',70),('end',70)]:draws+=draw([r for r in bank if r['stage']==stage],n,rng)
    rng.shuffle(draws)
    base=ROOT/'data/processed/diverse-sources-v54';core=read(base/'control-groups.json');refs=read(base/'references.json')
    old_groups=read(ROOT/'data/processed/additive-isolation-v57/old_repeat-groups.json')
    assert all(g[:2]==x for g,x in zip(old_groups,core)) and len(core)==len(refs)==len(draws)==200
    save(OUT/'references.json',refs);save(OUT/'R-groups.json',old_groups)
    groups=[copy.deepcopy(g)+[r] for g,r in zip(core,draws)]
    save(OUT/'A-groups.json',groups);save(OUT/'B-groups.json',groups)
    audit={'episodes':len(traces),'unique_verified_decisions':len(bank),'bank_by_stage':dict(collections.Counter(r['stage'] for r in bank)),
        'bank_wrong_by_stage':dict(collections.Counter(r['stage'] for r in bank if r['wrong'])),
        'new_presentations':200,'new_distinct_inputs_presented':len({r['id'] for r in draws}),
        'new_presentation_stages':dict(collections.Counter(r['stage'] for r in draws)),
        'new_presentations_where_initial_wrong':sum(r['wrong'] for r in draws),'excluded':dict(collections.Counter(x['reason'] for x in excluded)),
        'A_B_data_identical':True,'old600_preserved':True,'training_only':True,'max_tokens':engine.max_tokens}
    save(OUT/'collection-complete.json',audit)
    save(OUT/'training-input-manifest.json',{str(p.relative_to(ROOT)):digest(p) for p in [OUT/(x+'-groups.json') for x in ('R','A','B')]+[OUT/'references.json',OUT/'visited-label-bank.json']})
    verify();print(audit,flush=True)
if __name__=='__main__':main()
