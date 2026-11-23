"""Native xLAM function-call comparator; no generated-call repair or training."""
import copy,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.rollout_data_v60 import DATA,OUT,verify,read,save,digest
from scripts.rollout_eval_v60 import public
from agent.rollout_files_v60 import Files,grade,names
REPO='Salesforce/xLAM-2-1b-fc-r';REV='6870fcf102f434bd01819302d85780b8e767925d'

def parse(text):
    # Matches the official non-streaming xLAM parser's direct-array format.
    # Unlike its fallback, a malformed array is an error, not a successful stop.
    text=text.strip()
    if not text:raise ValueError('empty_generation')
    if not text.startswith('['):return None
    calls=json.loads(text)
    if not isinstance(calls,list):raise ValueError('not_array')
    for c in calls:
        if not isinstance(c,dict) or set(c)!={'name','arguments'} or not isinstance(c['name'],str) or not isinstance(c['arguments'],dict):raise ValueError('bad_call_object')
    return calls

def unobserved_branch(trace,family):
    # Reading and counting together is not a premature conditional write.
    writer=names(family)['b']
    return any(writer in b['names'] and not b['cache_before_generation'] for b in trace['batches'])

class Native:
    def __init__(self):
        import torch
        from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
        torch.set_num_threads(4);self.torch=torch
        self.tokenizer=AutoTokenizer.from_pretrained(REPO,revision=REV,local_files_only=True,trust_remote_code=False)
        self.model=AutoModelForCausalLM.from_pretrained(REPO,revision=REV,local_files_only=True,trust_remote_code=False,
            torch_dtype=torch.float16,device_map={'':0},attn_implementation='sdpa',
            quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)).eval()
    def generate(self,messages,tools):
        b=self.tokenizer.apply_chat_template(messages,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')
        n=int(b['input_ids'].shape[1]);b={k:v.to('cuda') for k,v in b.items()}
        if n+128>32768:raise ValueError('input_limit')
        started=time.perf_counter()
        with self.torch.inference_mode():out=self.model.generate(**b,max_new_tokens=128,do_sample=False,use_cache=True,pad_token_id=self.tokenizer.eos_token_id)
        tokens=out[0,n:];text=self.tokenizer.decode(tokens,skip_special_tokens=True)
        finished=bool(tokens.numel()) and int(tokens[-1])==self.tokenizer.eos_token_id
        import hashlib
        return text,{'text':text,'input_tokens':n,'output_tokens':int(tokens.numel()),'finished':finished,'seconds':time.perf_counter()-started,
            'messages':copy.deepcopy(messages),'tools':copy.deepcopy(tools),
            'input_ids_sha256':hashlib.sha256(b['input_ids'].cpu().numpy().tobytes()).hexdigest()}

def turn(native,text,service,case,history):
    reg=service.registry(case['available'],case['order']);ds=reg.definitions()
    # Same relative tool order as the existing scalar Session.view(), which
    # shuffles all tool/ask/none candidates after registry construction.
    display_order=[d['name'] for d in ds]+['ask','none'];random.Random(case['order_seed']).shuffle(display_order)
    ds.sort(key=lambda d:display_order.index(d['name']))
    tools=[{'name':d['name'],'description':d['description'],'parameters':d['inputSchema']} for d in ds]
    # No custom system: preserve downloaded model template and its native format instructions.
    messages=copy.deepcopy(history)+[{'role':'user','content':text+'\n현재 작업 상태: '+json.dumps(service.state,ensure_ascii=False)}]
    events=[];steps=[];seen=set();reason='step_limit';stopped=False;generations=[];batches=[]
    for _ in range(3):
        try:
            raw,info=native.generate(messages,tools);generations.append(info)
            if not info['finished']:reason='generation_limit';break
            calls=parse(raw)
        except Exception as exc:reason='parse_or_generation_error';generations.append({'error':str(exc)});break
        if not calls:
            steps.append({'choice':'none'});reason='model_stop';stopped=True;messages.append({'role':'assistant','content':raw});break
        batches.append({'names':[c['name'] for c in calls],'cache_before_generation':service.cache is not None})
        messages.append({'role':'assistant','content':None,'tool_calls':[{'type':'function','function':copy.deepcopy(c)} for c in calls]})
        failed=False
        for call in calls:
            name=call['name'];steps.append({'choice':name,'arguments':copy.deepcopy(call['arguments'])})
            if name in seen:reason='duplicate_call';failed=True;break
            if len(events)>=3:reason='tool_call_limit';failed=True;break
            seen.add(name)
            try:result=reg.invoke(name,call['arguments'])
            except Exception as exc:result={'ok':False,'reason':'registry_rejected','detail':str(exc)}
            events.append({'tool':name,'arguments':copy.deepcopy(call['arguments']),'executed':result.get('reason')!='registry_rejected','result':result})
            messages.append({'role':'tool','name':name,'content':json.dumps(result,ensure_ascii=False)})
            if result.get('ok') is not True:reason='tool_error';failed=True;break
        if failed:break
    trace={'events':events,'steps':steps,'stop_reason':reason,'model_stopped':stopped,'generations':generations,'batches':batches,
        'native_prompt':{'initial_messages':copy.deepcopy(history)+[{'role':'user','content':text}],'tools':tools}}
    return trace,messages

def prepare():
    if (OUT/'C-plan.json').exists():raise FileExistsError('C plan protected')
    save(OUT/'C-plan.json',{'repo':REPO,'revision':REV,'additional_training':False,'native_template':True,'dtype':'NF4 double quantization; float16 compute and non-quantized layers','max_new_tokens':128,'do_sample':False,
        'max_decisions_per_turn':3,'max_calls_per_turn':3,'parser':'strict direct JSON array; no repair; malformed arrays fail; other nonempty natural text is stop',
        'dependent_batch':'Executed with real validation and logged. For conditional goals, generating read+process together before observing nonempty results fails result-conditioned branch criterion even if output happens correct.',
        'native_history':'actual native user/assistant/tool messages; not same tokenizer/view as scalar ranker; practical alternative, not causal architecture-only comparison',
        'final_gate':'All scalar arm final statuses must be frozen before C sees final cases. No private source APIs, no production changes.',
        'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),ROOT/'tests/test_rollout_xlam_v60.py',DATA/'file-cases.json',DATA/'file-tools.json']}})

def main():
    if '--prepare' in sys.argv:return prepare()
    verify();cfg=read(OUT/'C-plan.json');read(OUT/'finals-frozen.json')
    for p,h in cfg['frozen_files'].items():
        if digest(ROOT/p)!=h:raise ValueError('C frozen changed:'+p)
    if (OUT/'C-files.json').exists() or (OUT/'C-started.json').exists():raise FileExistsError('C evaluation protected')
    save(OUT/'C-started.json',{'plan_sha256':digest(OUT/'C-plan.json')});native=Native();results=[];started=time.perf_counter()
    for i,c in enumerate(read(DATA/'file-cases.json')):
        service=Files(OUT/'work'/'C'/c['id'].replace(':','-'),c['family'],c['payload']);history=[];turns=[]
        for t in c['turns']:
            trace,history=turn(native,t['text'],service,public(c),history);g=grade(t,trace,service)
            # This after-execution grading restriction never selects a tool.
            dependency_violation=c['kind']=='conditional' and unobserved_branch(trace,c['family'])
            g['unobserved_conditional_batch']=dependency_violation
            if dependency_violation:g['goal_and_stop']=False;g['path_and_stop']=False
            turns.append({'text':t['text'],'expected_roles':t['roles'],'expected_output':t['output'],'trace':trace,'grade':g,'actual':service.snapshot()})
        results.append({'id':c['id'],'family':c['family'],'split':c['split'],'kind':c['kind'],'style':c['style'],'turns':turns,
            'goal_and_stop':all(t['grade']['goal_and_stop'] for t in turns),'goal_ok':all(t['grade']['goal_ok'] for t in turns)})
        if (i+1)%10==0:
            save(OUT/'C-progress.json',{'completed_cases':i+1,'total':160,'seconds':time.perf_counter()-started})
            print('V60 C',i+1,'/160 seconds',round(time.perf_counter()-started),flush=True)
        # Crash evidence saved per case, never silently restart the same protected run.
        save(OUT/'C-cases'/c['id'].replace(':','-').__add__('.json'),results[-1]) if (OUT/'C-cases').exists() else _first(c,results[-1])
    save(OUT/'C-files.json',{'label':'C','repo':REPO,'revision':REV,'episodes':results,'seconds':time.perf_counter()-started})
    print('V60 C COMPLETE; no training or deployment',flush=True)

def _first(c,result):
    (OUT/'C-cases').mkdir();save(OUT/'C-cases'/(c['id'].replace(':','-')+'.json'),result)
if __name__=='__main__':main()
