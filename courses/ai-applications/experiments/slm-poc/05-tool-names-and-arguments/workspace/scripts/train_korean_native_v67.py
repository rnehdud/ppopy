"""Fixed Korean QLoRA dose comparison. No test-driven tuning or deployment."""
import collections
import copy
import gc
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
DATA=ROOT/'output/korean-native-v67/material-v2'
RUN=ROOT/'output/korean-native-v67/experiment'
from scripts.korean_material_v67 import sha,write,SEED,MODEL,REV
from agent.korean_files_v67 import Files,turn,grade


def read(path):return json.loads(path.read_text(encoding='utf-8'))
def save(name,value):write(RUN/name,value)


def prepare():
    assert read(DATA/'manual-review.json')['approved_for_exploratory_training'] is True
    material=read(DATA/'selected-material.json');assert material['train_presentations']==3000
    train=read(DATA/'train.json');assert len({r['group'] for r in train})==3000
    assert all(r['target'].get('content')=='[]' for r in train if r['bucket']!='call')
    RUN.mkdir(exist_ok=False)
    retention=read(ROOT/'output/reference-reset-v66/language-boundary/cases.json')
    save('retention-cases.json',retention)
    paths=[DATA/n for n in ['train.json','source-dev.json','public-dev.json','public-test.json','file-cases.json','file-tools.json','selected-material.json','manual-review.json']]
    paths += [ROOT/p for p in ['scripts/train_korean_native_v67.py','scripts/korean_material_v67.py','scripts/select_korean_v67.py',
             'agent/korean_files_v67.py','agent/retail_transfer_v65.py','agent/retail_attention_v65.py',
             'scripts/retail_attempt3_v65.py','scripts/retail_attempt2_v65.py','scripts/retail_experiment_v65.py',
             'scripts/rollout_xlam_v60.py','training/retail_native_v65.py','tests/test_korean_native_v67.py']]
    paths += [RUN/'retention-cases.json']
    save('plan.json',{'seed':SEED,'model':MODEL,'revision':REV,'quantization':'NF4 double quantization /FP16 compute',
       'lora':{'r':8,'alpha':16,'dropout':0.05,'target_modules':'all-linear'},
       'training':{'A_lr':3e-5,'B_lr':1e-5,'presentations':3000,'milestones':[1000,3000],'gradient_accumulation':2,
          'epochs':1,'max_tokens':4096,'max_target_tokens':256,'weight_decay':0,'grad_clip':1,
          'loss':'Assistant target only, per-example mean, mean over2 examples; sparse LM head equivalent to masked causal CE.',
          'order':'Frozen interleaved call/non-call pairs. First1000 is a fixed stratified subset. Constant LR within each trial.',
          'B_condition':'Run the same1k/3k schedule at lower LR from the original zero adapter only if neither A checkpoint passes the predefined development health test.',
          'checkpoint_every_presentations':500,'release_cuda_cache_every_updates':50},
       'evaluation':{'max_new_tokens':256,'dev_public':36,'test_public':72,'dev_file_episodes':16,'test_file_episodes':48,
          'english_retention':12,'source_dev_loss_examples':30,'file_max_decisions':6,'file_max_calls':5,
          'file_state':'Turn-start snapshot marked as historical; each actual tool result includes the actual state after the call, for both baseline and all trained candidates.',
          'parser':'Same strict direct JSON array. No JSON/name repair, argument dropping, fallback tool selection or policy keyword gate.',
          'public_args':'Strict reference and reference plus explicitly supplied acceptable alternatives. No LLM judge. Non-call type only, not question wording correctness.'},
       'selection':{'development_only':True,'key':'Healthy first; then mean of public name-call rate, public no-call rate, requested file-save rate, file no-call rate, file completion rate, 1-forbidden-file-write-turn rate, English retention rate. Ties: fewer presentations, lower LR.',
          'healthy':'No forbidden or wrong-mode file writes; requested saves, file goal+stop, file no-call, public call names, public accepted args, public no-call, and English retention not below baseline; no lost baseline-successful dev file episodes.',
          'final_test':'Baseline restored to exact initial adapter vs one selected candidate, once after all development selection. Test outputs not read for selecting candidates.'},
       'final_gate':'At least5 more completed file episodes; no lost baseline-successful file episodes; zero forbidden/wrong-mode writes; required file saves, file no-call, public call names, public accepted args, public no-call and English retention not lower. Research candidate only, never automatic demo replacement.',
       'scope':'Public synthetic Korean teacher data, schema/role checks and assistant review only. Actual-file fixtures are assistant-authored. No independent human gold; no80-90% claim. Source tool catalogs held out from this additional training, not necessarily from original model pretraining.',
       'frozen_files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
    print('V67 fixed experiment plan written before model outcomes',flush=True)


def verify():
    p=read(RUN/'plan.json')
    for name,h in p['frozen_files'].items():assert sha(ROOT/name)==h,name
    return p


def create_model():
    import torch
    from scripts.retail_attempt3_v65 import KernelNative
    from peft import LoraConfig,TaskType,get_peft_model,prepare_model_for_kbit_training
    class Native(KernelNative):
        def generate(self,messages,tools):
            b=self.tokenizer.apply_chat_template(messages,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')
            n=b['input_ids'].shape[1]
            if n+256>self.model.config.max_position_embeddings:raise ValueError('Context overflow; no truncation')
            b={k:v.to('cuda') for k,v in b.items()};started=time.perf_counter()
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):
                out=self.model.generate(**b,max_new_tokens=256,do_sample=False,use_cache=True,pad_token_id=self.tokenizer.eos_token_id)
            ids=out[0,n:];text=self.tokenizer.decode(ids,skip_special_tokens=True)
            return text,{'text':text,'finished':bool(len(ids)) and int(ids[-1])==self.tokenizer.eos_token_id,
               'input_tokens':int(n),'output_tokens':len(ids),'seconds':time.perf_counter()-started,
               'messages':copy.deepcopy(messages),'tools':copy.deepcopy(tools),
               'input_ids_sha256':hashlib.sha256(b['input_ids'].cpu().numpy().tobytes()).hexdigest()}
    native=Native()
    native.model=prepare_model_for_kbit_training(native.model,use_gradient_checkpointing=True,gradient_checkpointing_kwargs={'use_reentrant':False})
    native.model.get_input_embeddings().to(dtype=torch.float16);native.model.get_output_embeddings().to(dtype=torch.float16)
    native.model=get_peft_model(native.model,LoraConfig(task_type=TaskType.CAUSAL_LM,r=8,lora_alpha=16,lora_dropout=0.05,target_modules='all-linear',bias='none'))
    native.model.eval()
    return native


def parsed(info):
    from scripts.rollout_xlam_v60 import parse
    if not info.get('finished'):raise ValueError('unfinished')
    return parse(info['text'])


def public_eval(native,split,label):
    from jsonschema import Draft202012Validator
    rows=[]
    for i,r in enumerate(read(DATA/('public-'+split+'.json'))):
        _,g=native.generate(r['messages'],r['tools']);calls='invalid';good_name=False;exact=False;accepted=False;no_call=False
        try:
            calls=parsed(g);no_call=calls is None or calls==[]
            reference=r['reference'].get('tool_calls') or []
            if reference and calls and len(calls)==len(reference)==1:
                f=reference[0]['function'];args=json.loads(f['arguments']) if isinstance(f['arguments'],str) else f['arguments']
                good_name=calls[0]['name']==f['name']
                exact=good_name and calls[0]['arguments']==args
                alts=r.get('acceptable_arguments')
                if isinstance(alts,str):
                    try:alts=json.loads(alts)
                    except ValueError:alts={}
                alts=alts if isinstance(alts,dict) else {}
                prediction=calls[0]['arguments']
                accepted=good_name and prediction.keys()==args.keys() and all(prediction[k]==v or prediction[k] in (alts.get(k) if isinstance(alts.get(k),list) else []) for k,v in args.items())
                available={t['name']:t for t in r['tools']}
                if good_name:Draft202012Validator(available[f['name']]['parameters']).validate(prediction)
            if not reference:good_name=no_call;exact=no_call;accepted=no_call
        except Exception:
            accepted=False;exact=False
        rows.append({'id':r['id'],'category':r['category'],'family':r['family'],'call_name_correct':good_name,
                 'strict_correct':exact,'accepted_correct':accepted,'no_call':no_call,'calls':calls,'generation':g})
        if (i+1)%12==0:print('V67 public',label,split,i+1,flush=True)
    save(f'{label}/{split}-public.json',rows)
    call=[r for r in rows if r['category']=='CALL'];non=[r for r in rows if r['category']!='CALL']
    return {'n':len(rows),'call_n':len(call),'call_name_correct':sum(r['call_name_correct'] for r in call),
            'call_strict_correct':sum(r['strict_correct'] for r in call),'call_accepted_correct':sum(r['accepted_correct'] for r in call),
            'no_call_n':len(non),'no_call_correct':sum(r['no_call'] for r in non),
            'by_category':{k:{'n':sum(r['category']==k for r in rows),'correct':sum(r['accepted_correct'] for r in rows if r['category']==k)} for k in sorted({r['category'] for r in rows})}}


def file_eval(native,split,label):
    episodes=[]
    selected=[r for r in read(DATA/'file-cases.json') if r['split']==split]
    for i,c in enumerate(selected):
        service=Files(RUN/'work'/label/split/c['id'].replace(':','-'),c['family'],c['payload']);history=[];turns=[]
        for expected in c['turns']:
            trace,history=turn(native,expected['text'],service,c,history)
            turns.append({'input':expected['text'],'expected':expected,'trace':trace,'actual':service.snapshot(),'grade':grade(expected,trace,service)})
        row={'id':c['id'],'kind':c['kind'],'family':c['family'],'turns':turns,'goal_and_stop':all(t['grade']['goal_and_stop'] for t in turns)}
        episodes.append(row);save(f'{label}/{split}-episodes/{c["id"].replace(":","-")}.json',row)
        if (i+1)%8==0:print('V67 files',label,split,i+1,'/',len(selected),flush=True)
    save(f'{label}/{split}-files.json',episodes);ts=[t for r in episodes for t in r['turns']]
    return {'n':len(episodes),'goal_and_stop':sum(r['goal_and_stop'] for r in episodes),
            'required_write_n':sum(t['grade']['required_write'] for t in ts),'required_correct_write':sum(t['grade']['requested_correct_write'] for t in ts),
            'forbidden_write_turns':sum(not t['grade']['required_write'] for t in ts),'unwanted_writes':sum(t['grade']['unwanted_write'] for t in ts),
            'wrong_mode_writes':sum(t['grade']['wrong_mode_write'] for t in ts if t['grade']['required_write']),
            'no_call_n':sum(r['kind'] in ['ask','missing'] for r in episodes),'no_call_correct':sum(r['goal_and_stop'] for r in episodes if r['kind'] in ['ask','missing']),
            'passed_ids':[r['id'] for r in episodes if r['goal_and_stop']]}


def retention_eval(native,label):
    rows=[]
    for r in read(RUN/'retention-cases.json'):
        _,g=native.generate(r['messages'],r['tools'])
        try:
            calls=parsed(g);correct=(calls==r['expected']) if r['expected'] else calls is None or calls==[]
        except Exception:correct=False
        rows.append({'id':r['id'],'kind':r['kind'],'correct':correct,'generation':g})
    save(label+'/english-retention.json',rows)
    return {'n':len(rows),'correct':sum(r['correct'] for r in rows)}


def loss_eval(native,label):
    import torch
    from training.retail_native_v65 import assistant_loss
    values=collections.defaultdict(list)
    for r in read(DATA/'source-dev.json'):
        ids=torch.tensor([r['input_ids']],device='cuda')
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):loss=assistant_loss(native.model,ids,r['target_start'])
        values[r['bucket']].append(float(loss));del ids,loss
    output={k:sum(v)/len(v) for k,v in values.items()};save(label+'/source-dev-loss.json',output)
    return output


def evaluate_dev(native,label):
    native.model.eval()
    result={'files':file_eval(native,'dev',label),'public':public_eval(native,'dev',label),
            'retention':retention_eval(native,label),'source_loss':loss_eval(native,label)}
    save(label+'/dev-summary.json',result)
    print('V67 DEV',label,json.dumps(result),flush=True)
    return result


def health_and_score(r,base):
    f,p,e=r['files'],r['public'],r['retention'];bf,bp,be=base['files'],base['public'],base['retention']
    healthy=(not f['unwanted_writes'] and not f['wrong_mode_writes'] and f['required_correct_write']>=bf['required_correct_write']
      and f['goal_and_stop']>=bf['goal_and_stop'] and f['no_call_correct']>=bf['no_call_correct']
      and p['call_name_correct']>=bp['call_name_correct'] and p['call_accepted_correct']>=bp['call_accepted_correct']
      and p['no_call_correct']>=bp['no_call_correct'] and e['correct']>=be['correct']
      and not (set(bf['passed_ids'])-set(f['passed_ids'])))
    score=(p['call_name_correct']/p['call_n']+p['no_call_correct']/p['no_call_n']+f['required_correct_write']/f['required_write_n']
           +f['no_call_correct']/f['no_call_n']+f['goal_and_stop']/f['n']+1-f['unwanted_writes']/f['forbidden_write_turns']+e['correct']/e['n'])/7
    return healthy,score


def checkpoint(native,label,rows,initial,optimizer,scaler,step,lr,started,forwards):
    import torch
    from safetensors.torch import load_file
    from peft import get_peft_model_state_dict,set_peft_model_state_dict
    dest=RUN/'checkpoints'/label;dest.mkdir(parents=True,exist_ok=False)
    native.model.eval();native.model.save_pretrained(dest,safe_serialization=True)
    saved=load_file(str(dest/'adapter_model.safetensors'));current=get_peft_model_state_dict(native.model)
    assert all(torch.equal(current[k].detach().cpu(),v) for k,v in saved.items())
    delta=max(float((v-initial[k]).abs().max()) for k,v in saved.items());assert delta>0
    ids=torch.tensor([rows[0]['input_ids'][-96:]],device='cuda')
    def probe():
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):return native.model(input_ids=ids,logits_to_keep=2,use_cache=False).logits.detach().float().cpu()
    a=probe();param=next(p for n,p in native.model.named_parameters() if p.requires_grad)
    with torch.no_grad():param.add_(0.01)
    set_peft_model_state_dict(native.model,saved);b=probe();error=float((a-b).abs().max());assert error<=1e-5
    torch.save({'optimizer':optimizer.state_dict(),'scaler':scaler.state_dict(),'step':step,'lr':lr,
                'torch_rng':torch.random.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all(),
                'training_data_sha256':sha(DATA/'train.json'),'plan_sha256':sha(RUN/'plan.json')},dest/'training-state.pt')
    save(f'checkpoints/{label}/verification.json',{'optimizer_updates':step,'presentations':step*2,'forward_presentations':forwards,
            'lr':lr,'seconds_since_trial_start_including_dev':time.perf_counter()-started,'max_weight_change':delta,'reload_error':error,
            'peak_allocated_GiB':torch.cuda.max_memory_allocated()/2**30,'peak_reserved_GiB':torch.cuda.max_memory_reserved()/2**30,
            'adapter_sha256':sha(dest/'adapter_model.safetensors')})
    del saved,current,ids,a,b,param;gc.collect();torch.cuda.empty_cache()


def train_trial(native,trial,lr,rows,initial,base,rng_state):
    import torch
    from peft import set_peft_model_state_dict
    from training.retail_native_v65 import assistant_loss
    set_peft_model_state_dict(native.model,initial);torch.random.set_rng_state(rng_state[0]);torch.cuda.set_rng_state_all(rng_state[1])
    params=[p for p in native.model.parameters() if p.requires_grad]
    assert all('lora_' in n for n,p in native.model.named_parameters() if p.requires_grad)
    optimizer=torch.optim.AdamW(params,lr=lr,weight_decay=0,foreach=False);scaler=torch.amp.GradScaler('cuda',init_scale=128)
    native.model.config.use_cache=False;torch.cuda.reset_peak_memory_stats();started=time.perf_counter();candidates=[];forwards=0
    for step in range(1,1501):
        pair=rows[(step-1)*2:step*2];native.model.train()
        for retry in range(12):
            optimizer.zero_grad(set_to_none=True);losses=[]
            for r in pair:
                ids=torch.tensor([r['input_ids']],device='cuda')
                with torch.autocast('cuda',dtype=torch.float16):loss=assistant_loss(native.model,ids,r['target_start'])
                if not torch.isfinite(loss):raise ValueError('Nonfinite loss')
                losses.append(float(loss.detach()));scaler.scale(loss/2).backward();forwards+=1;del ids,loss
            scaler.unscale_(optimizer);norm=float(torch.nn.utils.clip_grad_norm_(params,1.0))
            if math.isfinite(norm):scaler.step(optimizer);scaler.update();break
            scaler.step(optimizer);scaler.update()
        else:raise ValueError('Repeated nonfinite gradients')
        entry={'step':step,'presentations':step*2,'ids':[r['id'] for r in pair],'loss':sum(losses)/2,'gradient_norm':norm,
               'retry':retry,'seconds':time.perf_counter()-started,'input_tokens':sum(len(r['input_ids']) for r in pair)}
        with (RUN/(trial+'-training.jsonl')).open('a',encoding='utf-8') as f:f.write(json.dumps(entry)+'\n')
        if step%25==0:print('V67 TRAIN',trial,step*2,'/3000 loss',round(entry['loss'],4),'sec',round(entry['seconds']),flush=True)
        if step%50==0:torch.cuda.empty_cache()
        if step%250==0:
            label=f'{trial}-{step*2}';checkpoint(native,label,rows,initial,optimizer,scaler,step,lr,started,forwards)
            if step in [500,1500]:
                dev=evaluate_dev(native,label);healthy,score=health_and_score(dev,base)
                candidate={'label':label,'trial':trial,'lr':lr,'presentations':step*2,'healthy':healthy,'score':score,'dev':dev}
                candidates.append(candidate);save(label+'/candidate.json',candidate);verify()
    del optimizer,scaler,params;native.model.zero_grad(set_to_none=True);gc.collect();torch.cuda.empty_cache()
    return candidates


def main():
    if '--prepare' in sys.argv:return prepare()
    plan=verify()
    if (RUN/'started.json').exists():raise FileExistsError('Protected run already started')
    save('started.json',{'plan_sha256':sha(RUN/'plan.json'),'production_changes':False})
    import torch
    from peft import get_peft_model_state_dict,set_peft_model_state_dict
    from safetensors.torch import load_file
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    native=create_model();rows=read(DATA/'train.json');initial={k:v.detach().cpu().clone() for k,v in get_peft_model_state_dict(native.model).items()}
    assert all(torch.count_nonzero(v).item()==0 for k,v in initial.items() if 'lora_B' in k)
    trainable=sum(p.numel() for p in native.model.parameters() if p.requires_grad)
    save('model-setup.json',{'trainable_parameters':trainable,'gpu':torch.cuda.get_device_name(),'torch':torch.__version__,'config':native.model.config.to_dict()})
    # Verify actual longest full input before a long run; no optimizer update.
    from training.retail_native_v65 import assistant_loss
    cpu_rng=torch.random.get_rng_state();gpu_rng=torch.cuda.get_rng_state_all();longest=max(rows,key=lambda r:len(r['input_ids']))
    native.model.train();ids=torch.tensor([longest['input_ids']],device='cuda');torch.cuda.reset_peak_memory_stats();t=time.perf_counter()
    with torch.autocast('cuda',dtype=torch.float16):loss=assistant_loss(native.model,ids,longest['target_start'])
    loss.backward();finite=all(bool(torch.isfinite(p.grad).all()) for p in native.model.parameters() if p.grad is not None)
    save('preflight.json',{'tokens':len(longest['input_ids']),'finite_gradients':finite,'optimizer_updates':0,
              'peak_allocated_GiB':torch.cuda.max_memory_allocated()/2**30,'seconds':time.perf_counter()-t})
    assert finite;native.model.zero_grad(set_to_none=True);native.model.eval();del ids,loss
    torch.random.set_rng_state(cpu_rng);torch.cuda.set_rng_state_all(gpu_rng);torch.cuda.empty_cache()
    base=evaluate_dev(native,'baseline');rng_state=(torch.random.get_rng_state(),torch.cuda.get_rng_state_all())
    candidates=train_trial(native,'A',plan['training']['A_lr'],rows,initial,base,rng_state)
    if not any(c['healthy'] for c in candidates):
        save('B-trigger.json',{'reason':'Neither A milestone passed predefined development health conditions. Test has not been evaluated.'})
        candidates+=train_trial(native,'B',plan['training']['B_lr'],rows,initial,base,rng_state)
    chosen=max(candidates,key=lambda c:(c['healthy'],c['score'],-c['presentations'],-c['lr']))
    save('development-selection.json',{'selected':chosen,'all_candidates':candidates,'test_used':False})
    # Restore the exact zero-adapter baseline, then the selected saved adapter.
    test={}
    for label,state in [('baseline',initial),(chosen['label'],load_file(str(RUN/'checkpoints'/chosen['label']/'adapter_model.safetensors')))]:
        set_peft_model_state_dict(native.model,state);native.model.eval()
        actual=get_peft_model_state_dict(native.model)
        assert all(torch.equal(actual[k].detach().cpu(),v) for k,v in state.items())
        test[label]={'files':file_eval(native,'test',label),'public':public_eval(native,'test',label)}
    b=test['baseline'];a=test[chosen['label']];bf,af=b['files'],a['files'];bp,ap=b['public'],a['public']
    lost=sorted(set(bf['passed_ids'])-set(af['passed_ids']));gained=sorted(set(af['passed_ids'])-set(bf['passed_ids']))
    adopted=(af['goal_and_stop']>=bf['goal_and_stop']+5 and not lost and not af['unwanted_writes'] and not af['wrong_mode_writes']
          and af['required_correct_write']>=bf['required_correct_write'] and af['no_call_correct']>=bf['no_call_correct']
          and ap['call_name_correct']>=bp['call_name_correct'] and ap['call_accepted_correct']>=bp['call_accepted_correct']
          and ap['no_call_correct']>=bp['no_call_correct'] and chosen['dev']['retention']['correct']>=base['retention']['correct'])
    verify();save('summary.json',{'selected':chosen['label'],'healthy_on_dev':chosen['healthy'],'test':test,'gained':gained,'lost':lost,
            'adoptable_research_candidate':adopted,'production_changed':False,'scope':plan['scope']})
    print('V67 COMPLETE',json.dumps({'selected':chosen['label'],'test':test,'adoptable':adopted}),flush=True)


if __name__=='__main__':
    try:main()
    except Exception as e:
        import traceback
        if RUN.exists() and not (RUN/'failure.json').exists():save('failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
        raise
