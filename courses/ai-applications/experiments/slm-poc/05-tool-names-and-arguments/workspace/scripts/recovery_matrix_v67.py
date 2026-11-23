"""A-dose comparison plus existing JSON protocol/error-feedback controls.

The original frozen A/B driver is not edited. Stop its OWN process only after
the verified A-3000 checkpoint; B is deferred until controls have been tested.
Final test is untouched until all development choices are locked here.
"""
import copy
import gc
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import train_korean_native_v67 as exp
from scripts.protocol_control_v67 import rewrite,PROMPT
from scripts.korean_material_v67 import sha,write,SEED
from agent import korean_files_v67 as original
from agent import recovery_loop_v67 as recovery
AB=ROOT/'output/korean-native-v67/experiment'
OUT=ROOT/'output/korean-native-v67/recovery-matrix'

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def prepare():
    assert not (AB/'checkpoints/A-3000/verification.json').exists(),'Declare before A completes'
    assert not (AB/'baseline/test-files.json').exists(),'Final test not seen'
    OUT.mkdir(exist_ok=False)
    files=[Path(__file__),ROOT/'agent/recovery_loop_v67.py',ROOT/'tests/test_recovery_loop_v67.py',
           ROOT/'scripts/protocol_control_v67.py',PROMPT,ROOT/'scripts/stop_after_checkpoint_v67.ps1',
           AB/'plan.json',AB/'baseline/dev-summary.json']
    write(OUT/'plan.json',{
      'reason':'User updated goal emphasizes one dynamic logic. Observed baseline writer returns read_required, but the original executor terminates immediately and disallows retry after a read. Test existing result/error feedback before paying for another whole training run.',
      'supersedes':'C-only global selection plan is superseded before C executes. Original A/B plan/code/data remain unmodified; A completes3000, B is deferred rather than automatically run.',
      'arms':{'A-1000':'Original Korean QLoRA / native prompt / original stop-on-error loop',
              'A-3000':'Same training run at3000 / native prompt / original loop',
              'C':'Zero additional training / published JSON-only prompt / original loop',
              'D':'Zero additional training / native prompt / generic error-feedback loop',
              'E':'Zero additional training / published JSON-only prompt / generic error-feedback loop'},
      'B_condition':'Only if none of A1000/A3000/C/D/E satisfies the original development health requirements, run the original lower-LR B1k/B3k schedule from fresh zero adapter with the same seed/recipe in a new process. No additional recipes are chosen using final test.',
      'feedback':'No special branch for read_required, individual tool names or user keywords. Return every actual result/error to the same model. Repeat of same call+arguments allowed only if observed state differs. Same6 decisions/5 attempts per turn.',
      'goal_scoring':'Safe failed attempts may be recovered only when their before/after snapshots are identical, required successful actions occur, final files match, and model explicitly stops. All failed attempts remain logged. No-call requests forbid even failed attempts. Any wrong successful write or successful conditional write before observing read result fails. Original loop cannot recover errors, so its existing goal results are unchanged.',
      'first_choice_accuracy':'Public first-choice name/argument scores remain separate; executor recovery is not called better first-choice inference.',
      'caching':'For the untrained controls only, exact token-input-SHA matches can replay deterministic measured dev generations. Namespace separated by prompt; no gold-based lookup. Every actual tool still executes anew. Final test never replays development outputs.',
      'selection':'Original healthy/score key across all dev candidates, ties fewer training examples then lower LR. Lock before any final model results are read. Final compare baseline vs one dev-selected arm once.',
      'adoption':'Must be healthy on dev AND pass original final gate (+5 completed file episodes, none of baseline successes lost, zero unwanted/wrong-mode writes, necessary saves/no-call/public names/public args/English retention not reduced). Research only, no demo switch.',
      'references':['references/langgraph-provenance.json','references/langgraph-agent-provenance.json','references/manifest.json'],
      'files':{str(p.relative_to(ROOT)):sha(p) for p in files},
      'final_test_read':False,'production_changed':False})
    print('V67 expanded matrix frozen BEFORE A3000 and final test',flush=True)

def verify():
    p=read(OUT/'plan.json')
    for name,h in p['files'].items():assert sha(ROOT/name)==h,name
    for name,h in read(AB/'plan.json')['frozen_files'].items():assert sha(ROOT/name)==h,name
    return p

def engine(recover):
    exp.turn=recovery.turn if recover else original.turn
    exp.grade=recovery.grade if recover else original.grade

def files(native,split,label,recover):
    engine(recover);r=exp.file_eval(native,split,label)
    episodes=read(OUT/label/(split+'-files.json'));ts=[t for e in episodes for t in e['turns']]
    r['attempts']=sum(len(t['trace']['events']) for t in ts)
    r['failed_attempts']=sum(e['result'].get('ok') is not True for t in ts for e in t['trace']['events'])
    r['recovered_episodes']=sum(e['goal_and_stop'] and any(x['result'].get('ok') is not True for t in e['turns'] for x in t['trace']['events']) for e in episodes)
    return r

def main():
    if '--prepare' in sys.argv:return prepare()
    verify()
    assert (AB/'checkpoints/A-3000/verification.json').exists()
    assert (OUT/'training-stop.json').exists(),'Run only after verified A checkpoint stop'
    if (OUT/'started.json').exists():raise FileExistsError('Protected matrix already started')
    import torch
    from peft import get_peft_model_state_dict,set_peft_model_state_dict
    from safetensors.torch import load_file
    assert torch.cuda.mem_get_info()[0]>4*2**30,'Wait for stopped training process to release GPU'
    write(OUT/'started.json',{'final_test_read':False})
    exp.RUN=OUT;write(OUT/'retention-cases.json',read(AB/'retention-cases.json'))
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    native=exp.create_model();raw_generate=native.generate
    initial={k:v.detach().cpu().clone() for k,v in get_peft_model_state_dict(native.model).items()}
    rng=(torch.random.get_rng_state(),torch.cuda.get_rng_state_all())
    assert all(torch.count_nonzero(v).item()==0 for k,v in initial.items() if 'lora_B' in k)
    def state(label):
        value=initial if label in ['baseline','C','D','E'] else load_file(str(AB/'checkpoints'/label/'adapter_model.safetensors'))
        set_peft_model_state_dict(native.model,value);native.model.eval()
        actual=get_peft_model_state_dict(native.model);assert all(torch.equal(actual[k].detach().cpu(),v) for k,v in value.items())
    base=read(AB/'baseline/dev-summary.json');candidates=[read(AB/'A-1000/candidate.json')]
    # Finish A3000 development in this process, not its original driver.
    state('A-3000');native.generate=raw_generate;engine(False)
    dev=exp.evaluate_dev(native,'A-3000');healthy,score=exp.health_and_score(dev,base)
    candidates.append({'label':'A-3000','lr':3e-5,'presentations':3000,'healthy':healthy,'score':score,'dev':dev})
    state('baseline');gc.collect();torch.cuda.empty_cache()
    rendered=native.tokenizer.apply_chat_template([{'role':'user','content':'probe'}],tools=[],tokenize=False)
    default=rendered.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()
    prompt=PROMPT.read_text(encoding='utf-8').strip();caches={'native':{},'published':{}}
    for episode in read(AB/'baseline/dev-files.json'):
        for t in episode['turns']:
            for g in t['trace']['generations']:
                if 'input_ids_sha256' in g:caches['native'][g['input_ids_sha256']]=g
    def wrapper(published,cache=True):
        def generate(messages,tools):
            ms=rewrite(messages,prompt,default) if published else copy.deepcopy(messages)
            namespace=caches['published' if published else 'native']
            b=native.tokenizer.apply_chat_template(ms,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')
            key=hashlib.sha256(b['input_ids'].numpy().tobytes()).hexdigest()
            if cache and key in namespace:
                g=copy.deepcopy(namespace[key]);g['exact_input_replay']=True;return g['text'],g
            text,g=raw_generate(ms,tools)
            if cache:namespace[key]=copy.deepcopy(g)
            g['exact_input_replay']=False;return text,g
        return generate
    cpublic=None;cretention=None
    for label,published,recover in [('C',True,False),('D',False,True),('E',True,True)]:
        native.generate=wrapper(published);f=files(native,'dev',label,recover)
        if label=='C':
            cpublic=exp.public_eval(native,'dev',label);cretention=exp.retention_eval(native,label)
        public=cpublic if published else base['public'];retention=cretention if published else base['retention']
        dev={'files':f,'public':public,'retention':retention}
        write(OUT/label/'dev-summary.json',dev);healthy,score=exp.health_and_score(dev,base)
        candidates.append({'label':label,'lr':0,'presentations':0,'healthy':healthy,'score':score,'dev':dev})
        print('V67 MATRIX DEV',label,json.dumps(dev),flush=True)
    if not any(c['healthy'] for c in candidates):
        write(OUT/'B-trigger.json',{'reason':'Neither A dose nor zero-training protocol/feedback controls passed development health; now test the already specified lower LR before final test.'})
        state('baseline');native.generate=raw_generate;engine(False)
        # New label paths are in OUT, never append to an interrupted old B log.
        candidates+=exp.train_trial(native,'B',1e-5,read(exp.DATA/'train.json'),initial,base,rng)
    chosen=max(candidates,key=lambda c:(c['healthy'],c['score'],-c['presentations'],-c['lr']))
    write(OUT/'global-development-selection.json',{'selected':chosen,'candidates':candidates,'test_read':False})
    verify();print('V67 MATRIX SELECTION LOCKED',chosen['label'],flush=True)
    # First final-test outcomes are generated ONLY after the global lock.
    test={}
    for label in ['baseline',chosen['label']]:
        if label.startswith('B-'):
            s=load_file(str(OUT/'checkpoints'/label/'adapter_model.safetensors'));set_peft_model_state_dict(native.model,s);native.model.eval()
        else:state(label)
        published=label in ['C','E'];recover=label in ['D','E']
        native.generate=wrapper(published,cache=False)
        path='final-'+label
        test[label]={'files':files(native,'test',path,recover),'public':exp.public_eval(native,'test',path)}
    b=test['baseline'];a=test[chosen['label']];bf,af=b['files'],a['files'];bp,ap=b['public'],a['public']
    lost=sorted(set(bf['passed_ids'])-set(af['passed_ids']));gained=sorted(set(af['passed_ids'])-set(bf['passed_ids']))
    adopted=(chosen['healthy'] and af['goal_and_stop']>=bf['goal_and_stop']+5 and not lost and not af['unwanted_writes'] and not af['wrong_mode_writes']
       and af['required_correct_write']>=bf['required_correct_write'] and af['no_call_correct']>=bf['no_call_correct']
       and ap['call_name_correct']>=bp['call_name_correct'] and ap['call_accepted_correct']>=bp['call_accepted_correct'] and ap['no_call_correct']>=bp['no_call_correct'])
    verify();write(OUT/'summary.json',{'selected':chosen['label'],'healthy_on_dev':chosen['healthy'],'test':test,
      'gained':gained,'lost':lost,'adoptable_research_candidate':adopted,'production_changed':False,
      'scope':'Dev-selected A dose or already existing prompt/error-feedback mechanism. Real file outcomes with all failed attempts kept. Recovery is not first-call model accuracy. Public first-call name/argument accuracy separate. No universal unknown-domain or independently human-validated guarantee.'})
    print('V67 MATRIX COMPLETE',chosen['label'],'adoptable',adopted,flush=True)

if __name__=='__main__':
    try:main()
    except Exception as e:
        import traceback
        if OUT.exists() and not (OUT/'failure.json').exists():write(OUT/'failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
        raise
