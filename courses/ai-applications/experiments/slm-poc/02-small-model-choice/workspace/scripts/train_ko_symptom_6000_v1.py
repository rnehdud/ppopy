"""Continue the selected ko-decision adapter over all 6000 decision examples.

Frozen predeclared development is used to select a checkpoint. New multi-turn
test cases are evaluated only after selection (baseline, selected, final).
No AI Hub text leaves the machine; none is used here.
"""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import SYMPTOMS,SymptomSession
from scripts.evaluate_symptom_state_v1 import CASES
from scripts.compare_korean_decision_pilot import EXTRA_CASES,QUESTION,OPTIONS,CHECKSUMS
from scripts.evaluate_jev_style_qwen_pilot import NAMES,DESCRIPTIONS
from scripts.train_ko_decision_qlora_pilot import NEW_CASES,read_rows

DATA=ROOT/'data/processed/ko_symptom_6000_v2'
OUT=ROOT/'output/training/ko-symptom-6000-v1'
ADAPTER=ROOT/'adapters/ko-symptom-6000-v1'
MODEL=ROOT/'models/ko-decision-roberta-large'
OLD=ROOT/'adapters/ko-decision-qlora-v1/step-60'

def main():
    import torch,transformers,peft,bitsandbytes
    from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
    from peft import PeftModel,prepare_model_for_kbit_training,set_peft_model_state_dict
    from safetensors.torch import load_file
    if OUT.exists() or ADAPTER.exists():raise FileExistsError('Outputs already exist; preserve them')
    if not torch.cuda.is_available():raise RuntimeError('CUDA required')
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name,sha in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=sha:raise ValueError('data hash mismatch')
    with (MODEL/'model.safetensors').open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=CHECKSUMS['ko']:raise ValueError('model hash mismatch')
    train=[json.loads(x) for x in (DATA/'train.jsonl').read_text(encoding='utf-8').splitlines()]
    test=json.loads((DATA/'heldout_cases.json').read_text(encoding='utf-8'))
    if len(train)!=6000 or len({(r['text'],r['field'],r['previous']) for r in train})!=6000:raise ValueError('wrong training count')
    dev=[{'id':c['id'],'turns':[{'input':t,'expected':e} for t,e in c['turns']]} for c in CASES+EXTRA_CASES]
    traintxt={r['text'] for r in train};testtxt={t['input'] for c in test for t in c['turns']};devtxt={t['input'] for c in dev for t in c['turns']}
    prior_train={r['text'] for r in read_rows('train')[:120]};old_test={t[0] for c in NEW_CASES+CASES+EXTRA_CASES for t in c['turns']}
    if traintxt&testtxt or traintxt&devtxt or testtxt&prior_train or testtxt&old_test:raise ValueError('exact-text split overlap')
    torch.manual_seed(601106);torch.cuda.manual_seed_all(601106);random.seed(601106)
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False);tok.padding_side='right'
    q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForSequenceClassification.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False,
         quantization_config=q,torch_dtype=torch.float16,device_map={'':0})
    base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=False)
    model=PeftModel.from_pretrained(base,str(OLD),is_trainable=True)
    params=[p for p in model.parameters() if p.requires_grad];names=[n for n,p in model.named_parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n in names):raise ValueError('unexpected trainable parameters')
    print('trainable',sum(p.numel() for p in params),'examples',len(train),flush=True)

    def score(rows):
        first=[];second=[]
        for row in rows:
            context='대상 증상: '+NAMES[row['field']]+'\n이전 상태: '+row['previous']+'\n이번 사용자 발화: '+row['text']
            for key in OPTIONS:first.append(QUESTION+' '+DESCRIPTIONS[key]);second.append(context)
        batch=tok(first,second,padding=True,truncation=False,return_tensors='pt')
        if batch['input_ids'].shape[1]>512:raise ValueError('input over classifier context')
        return model(**{k:v.to('cuda') for k,v in batch.items()}).logits[:,0].float().reshape(len(rows),4)

    def evaluate(cases):
        model.eval();out=[]
        for case in cases:
            session=SymptomSession();turns=[]
            for t in case['turns']:
                text=t['input'];expected=t['expected'];before=session.state
                questions=[{'field':f,'previous':before[f],'text':text} for f in SYMPTOMS]
                with torch.inference_mode():scores=score(questions)
                decisions={f:OPTIONS[x] for f,x in zip(SYMPTOMS,scores.argmax(-1).tolist())}
                patch={f:v for f,v in decisions.items() if v!='unchanged'}
                tool=session.update(patch) if patch else None
                turns.append({'input':text,'before':before,'expected':expected,'decisions':decisions,'patch':patch,
                              'tool_result':tool,'after':session.state,'matches':session.state==expected})
            out.append({'id':case['id'],'turns':turns,'passes':all(t['matches'] for t in turns)})
        turns=[t for c in out for t in c['turns']]
        return {'summary':{'scenarios':len(out),'scenario_passes':sum(c['passes'] for c in out),
                'turns':len(turns),'state_matches':sum(t['matches'] for t in turns),
                'field_matches':sum(t['expected'][f]==t['after'][f] for t in turns for f in SYMPTOMS),'fields':len(turns)*5,
                'unknown_expected':sum(t['expected'][f]=='unknown' for t in turns for f in SYMPTOMS),
                'unknown_to_absent':sum(t['expected'][f]=='unknown' and t['after'][f]=='absent' for t in turns for f in SYMPTOMS)},'cases':out}

    OUT.mkdir(parents=True);ADAPTER.mkdir(parents=True)
    cfg={'seed':601106,'base':'mmetamong/ko-decision-roberta-large@4c38909ebec2e712d7c1d4e578847ad0ff7f6654',
      'initial_adapter':str(OLD.relative_to(ROOT)),'initial_adapter_sha256':hashlib.sha256((OLD/'adapter_model.safetensors').read_bytes()).hexdigest(),
      'dataset_manifest':manifest,'quantization':'NF4 double quant, fp16 compute','decision_task':'four-option scoring',
      'train_examples':6000,'epochs':1,'batch_decisions':4,'optimizer_updates':1500,'learning_rate':0.00005,
      'checkpoints':[0,500,1000,1500],'selection':'development scenario passes, then state matches, then earliest step',
      'primary_metric':'new 20-scenario all-turn exact state; target 18/20; synthetic and independently unreviewed',
      'test_separation':'no exact text overlap with train, development, previous 120 train, or previous cases; same author and synthetic patterns',
      'versions':{'torch':torch.__version__,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__}}
    (OUT/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    history=[];model.eval();dev0=evaluate(dev);folder=ADAPTER/'step-0000';model.save_pretrained(folder,safe_serialization=True)
    history.append({'step':0,'seen':0,'development':dev0,'adapter':str(folder.relative_to(ROOT))})
    print('initial dev',dev0['summary'],flush=True)
    optimizer=torch.optim.AdamW(params,lr=0.00005,weight_decay=0,foreach=False)
    model.train();start=time.perf_counter();zero_grad_steps=0
    for step in range(1,1501):
        rows=train[(step-1)*4:step*4]
        logits=score(rows);target=torch.tensor([OPTIONS.index(r['decision']) for r in rows],device='cuda')
        loss=torch.nn.functional.cross_entropy(logits,target)
        if not torch.isfinite(loss):raise ValueError('nonfinite loss')
        loss.backward();norm=float(torch.nn.utils.clip_grad_norm_(params,1))
        if not torch.isfinite(torch.tensor(norm)):raise ValueError('nonfinite gradient')
        if norm==0:zero_grad_steps+=1
        optimizer.step();optimizer.zero_grad(set_to_none=True)
        if step%100==0:print('step',step,'seen',step*4,'loss',round(float(loss.detach()),5),'elapsed_s',round(time.perf_counter()-start),'peak_gib',round(torch.cuda.max_memory_allocated()/1024**3,2),flush=True)
        if step in [500,1000,1500]:
            report=evaluate(dev);folder=ADAPTER/f'step-{step:04}';model.save_pretrained(folder,safe_serialization=True)
            history.append({'step':step,'seen':step*4,'development':report,'adapter':str(folder.relative_to(ROOT))})
            (OUT/'history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('checkpoint',step,'dev',report['summary'],flush=True);model.train()
    selected=max(history,key=lambda r:(r['development']['summary']['scenario_passes'],r['development']['summary']['state_matches'],-r['step']))
    # Frozen test has not guided optimization or selection; evaluate all three
    # predeclared variants to see actual effects, including possible regression.
    experiments={}
    for label,entry in [('before',history[0]),('selected',selected),('all_6000',history[-1])]:
        set_peft_model_state_dict(model,load_file(str(ROOT/entry['adapter']/'adapter_model.safetensors')))
        experiments[label]={'step':entry['step'],'adapter':entry['adapter'],'heldout':evaluate(test)}
        print(label,entry['step'],experiments[label]['heldout']['summary'],flush=True)
    report={'selected_step':selected['step'],'selected_adapter':selected['adapter'],'zero_gradient_steps':zero_grad_steps,
            'examples_seen':len(train),'elapsed_seconds_including_evaluation':time.perf_counter()-start,
            'peak_cuda_allocated_gib':torch.cuda.max_memory_allocated()/1024**3,'experiments':experiments,
            'caution':'Synthetic, assistant-authored labels not independently reviewed; no real-conversation accuracy.'}
    (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('complete',flush=True)

if __name__=='__main__':main()
