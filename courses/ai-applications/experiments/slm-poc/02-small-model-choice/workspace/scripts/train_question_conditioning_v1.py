"""Add question-conditioned yes/no/unknown training with retention data.

Every score is local. Tool test and mock pipeline test are frozen and kept out
of checkpoint selection; data and labels are synthetic and unreviewed.
"""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.choice_agent_v1 import ChoiceAgent,TOOL_DESCRIPTIONS
from scripts.compare_korean_decision_pilot import CHECKSUMS
from scripts.train_ko_symptom_6000_v1 import MODEL

DATA=ROOT/'data/processed/choice_agent_v2';EVAL=ROOT/'data/processed/choice_agent_eval_v2'
QUESTION_DATA=ROOT/'data/processed/question_conditioning_v1'
OUT=ROOT/'output/training/question-conditioning-v1';ADAPTER=ROOT/'adapters/question-conditioning-v1'
OLD=ROOT/'adapters/choice-agent-v2/step-0539'

def load_data(folder,name):
    meta=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=meta['files'][name]:raise ValueError('dataset changed')
    text=(folder/name).read_text(encoding='utf-8')
    return [json.loads(line) for line in text.splitlines()] if name.endswith('.jsonl') else json.loads(text)

def main():
    import torch,transformers,peft,bitsandbytes
    from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
    from peft import PeftModel,prepare_model_for_kbit_training,set_peft_model_state_dict
    from safetensors.torch import load_file
    if OUT.exists() or ADAPTER.exists():raise FileExistsError('Existing outputs protected')
    if not torch.cuda.is_available():raise RuntimeError('CUDA required')
    with (MODEL/'model.safetensors').open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=CHECKSUMS['ko']:raise ValueError('model hash mismatch')
    train=load_data(QUESTION_DATA,'train.jsonl');dev=load_data(DATA,'dev.jsonl');test=load_data(DATA,'tool_test.jsonl')
    question_dev=load_data(QUESTION_DATA,'question_dev.jsonl');new_question_test=load_data(QUESTION_DATA,'question_test.jsonl')
    qtest=load_data(EVAL,'question_cases.jsonl');pipeline=load_data(EVAL,'pipeline_cases.json')
    traintexts={r['text'] for r in train}
    if traintexts&{r['text'] for r in dev+test+qtest+question_dev+new_question_test}:raise ValueError('train/eval text overlap')
    if traintexts&{t['input'] for c in pipeline for t in c['turns']}:raise ValueError('pipeline train overlap')
    random.seed(819721);torch.manual_seed(819721);torch.cuda.manual_seed_all(819721)
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False);tok.padding_side='right'
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForSequenceClassification.from_pretrained(MODEL,quantization_config=quant,torch_dtype=torch.float16,
          device_map={'':0},local_files_only=True,trust_remote_code=False)
    base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=False)
    model=PeftModel.from_pretrained(base,str(OLD),is_trainable=True)
    params=[p for p in model.parameters() if p.requires_grad];names=[n for n,p in model.named_parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n in names):raise ValueError('unexpected trainable weights')
    print('loaded; trainable',sum(p.numel() for p in params),'train',len(train),flush=True)

    def logits_for(rows):
        first=[];second=[];sizes=[]
        for row in rows:
            if len(row['options'])<2 or row.get('target',next(iter(row['options']))) not in row['options']:
                raise ValueError('invalid options')
            sizes.append(len(row['options']))
            for desc in row['options'].values():first.append(row['question']+' '+desc);second.append(row['context'])
        batch=tok(first,second,padding=True,truncation=False,return_tensors='pt')
        if batch['input_ids'].shape[1]>512:raise ValueError('No silent truncation')
        scores=model(**{k:v.to('cuda') for k,v in batch.items()}).logits[:,0].float()
        return list(scores.split(sizes))

    def score_one(question,options,context):
        row={'question':question,'options':options,'context':context}
        with torch.inference_mode():logits=logits_for([row])[0]
        probs=torch.softmax(logits.double(),dim=0).tolist()
        return dict(zip(options,probs))

    def check_rows(rows):
        model.eval();outputs=[]
        with torch.inference_mode():
            for i in range(0,len(rows),4):
                batch=rows[i:i+4];scores=logits_for(batch)
                for row,s in zip(batch,scores):
                    keys=list(row['options']);winner=keys[int(s.argmax())]
                    outputs.append({'kind':row['kind'],'text':row['text'],'question':row['question'],
                       'available':keys,'expected':row['target'],'predicted':winner,
                       'raw_scores':dict(zip(keys,s.tolist())),'matches':winner==row['target']})
        return {'n':len(outputs),'correct':sum(r['matches'] for r in outputs),'rows':outputs}

    def check_pipeline():
        model.eval();results=[];callback_events=[]
        def mock_lookup(query,state):
            event={'ok':True,'mock':True,'query':query,'state':state}
            callback_events.append(event);return event
        for case in pipeline:
            agent=ChoiceAgent(score_one,lookup=mock_lookup);turns=[]
            for t in case['turns']:
                try:
                    trace=agent.turn(t['input']);ok=trace['action']==t['expected_action'] and trace['after']==t['expected_state']
                    turns.append({'expected_action':t['expected_action'],'expected_state':t['expected_state'],
                                  'trace':trace,'matches':ok})
                except (ValueError,TypeError,RuntimeError) as e:
                    turns.append({'expected_action':t['expected_action'],'expected_state':t['expected_state'],
                                  'error':str(e),'matches':False})
            results.append({'id':case['id'],'turns':turns,'passes':all(t['matches'] for t in turns)})
        ts=[t for c in results for t in c['turns']]
        return {'cases':len(results),'case_passes':sum(c['passes'] for c in results),'turns':len(ts),
                'turn_matches':sum(t['matches'] for t in ts),
                'action_matches':sum('trace' in t and t['trace']['action']==t['expected_action'] for t in ts),
                'state_matches':sum('trace' in t and t['trace']['after']==t['expected_state'] for t in ts),
                'mock_lookup_calls':len(callback_events),'results':results}

    OUT.mkdir(parents=True);ADAPTER.mkdir(parents=True)
    steps=(len(train)+3)//4
    checkpoints=sorted(set([steps//3,(steps*2)//3,steps]))
    config={'base':'mmetamong/ko-decision-roberta-large@4c38909ebec2e712d7c1d4e578847ad0ff7f6654',
       'initial_adapter':str(OLD.relative_to(ROOT)),'initial_adapter_sha256':hashlib.sha256((OLD/'adapter_model.safetensors').read_bytes()).hexdigest(),
       'quantization':'NF4 double quant, fp16 compute','epochs':1,'train_items':len(train),'batch':4,'steps':steps,
       'learning_rate':0.00003,'checkpoints':checkpoints,'selection':'combined 10 tool dev plus 16 old question probe; tie earlier step; excludes new question test and mock pipeline',
       'tool_eval_cases':len(test),'symptom_question_cases':len(qtest),'pipeline_cases':len(pipeline),
       'scope':'one tool selection per user turn; lookup is explicitly mock; no LLM, STT, real KB or product recommendation',
       'data_caveat':'assistant-authored synthetic labels, no independent human review',
       'versions':{'torch':torch.__version__,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__}}
    (OUT/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    model.eval();dev0=check_rows(dev);qd0=check_rows(question_dev);folder=ADAPTER/'step-0000';model.save_pretrained(folder,safe_serialization=True)
    history=[{'step':0,'seen':0,'dev_correct':dev0['correct']+qd0['correct'],'dev_total':dev0['n']+qd0['n'],'adapter':str(folder.relative_to(ROOT)),'dev':dev0,'question_dev':qd0}]
    print('baseline dev tool',dev0['correct'],'/',dev0['n'],'question',qd0['correct'],'/',qd0['n'],flush=True)
    optimizer=torch.optim.AdamW(params,lr=0.00003,weight_decay=0,foreach=False);model.train();start=time.perf_counter();cursor=0;zeros=0
    for step in range(1,steps+1):
        batch=train[cursor:cursor+4];cursor+=len(batch);scores=logits_for(batch)
        losses=[torch.nn.functional.cross_entropy(s.unsqueeze(0),torch.tensor([list(r['options']).index(r['target'])],device='cuda')) for r,s in zip(batch,scores)]
        loss=torch.stack(losses).mean()
        if not torch.isfinite(loss):raise ValueError('non-finite loss')
        loss.backward();norm=float(torch.nn.utils.clip_grad_norm_(params,1))
        if not torch.isfinite(torch.tensor(norm)):raise ValueError('nonfinite gradient')
        if norm==0:zeros+=1
        optimizer.step();optimizer.zero_grad(set_to_none=True)
        if step%100==0:print('step',step,'seen',cursor,'loss',round(float(loss.detach()),4),'seconds',round(time.perf_counter()-start),flush=True)
        if step in checkpoints:
            check=check_rows(dev);qd=check_rows(question_dev);folder=ADAPTER/f'step-{step:04}';model.save_pretrained(folder,safe_serialization=True)
            history.append({'step':step,'seen':cursor,'dev_correct':check['correct']+qd['correct'],'dev_total':check['n']+qd['n'],'adapter':str(folder.relative_to(ROOT)),'dev':check,'question_dev':qd})
            (OUT/'history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('checkpoint',step,'tool',check['correct'],'/',check['n'],'question',qd['correct'],'/',qd['n'],flush=True);model.train()
    if cursor!=len(train):raise ValueError('not all training rows processed')
    selected=max(history,key=lambda x:(x['dev_correct'],-x['step']))
    experiments={}
    for name,entry in [('before',history[0]),('selected',selected),('last',history[-1])]:
        set_peft_model_state_dict(model,load_file(str(ROOT/entry['adapter']/'adapter_model.safetensors')));model.eval()
        a=check_rows(test);b=check_rows(qtest);c=check_pipeline();d=check_rows(new_question_test)
        experiments[name]={'step':entry['step'],'adapter':entry['adapter'],'tool_test':a,'symptom_questions':b,'pipeline':c,'new_question_test':d}
        print(name,'step',entry['step'],'tool',a['correct'],'/',a['n'],'symptom',b['correct'],'/',b['n'],
              'pipeline',c['case_passes'],'/',c['cases'],'turns',c['turn_matches'],'/',c['turns'],'new questions',d['correct'],'/',d['n'],flush=True)
    result={'selected_step':selected['step'],'seen':cursor,'zero_gradient_steps':zeros,
            'peak_cuda_allocated_gib':torch.cuda.max_memory_allocated()/1024**3,
            'elapsed_seconds_including_tests':time.perf_counter()-start,'experiments':experiments,
            'caveat':'synthetic, unreviewed labels; 8 small mock-pipeline cases; one action per turn; no independent clinical or production validation'}
    (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
