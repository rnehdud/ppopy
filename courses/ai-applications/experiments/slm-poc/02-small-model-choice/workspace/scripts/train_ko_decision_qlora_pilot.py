"""Single-GPU NF4+LoRA experiment for Korean symptom decisions, local only.

The original scalar scoring head is frozen. Four option scores are trained
jointly using cross entropy, matching the model card's pair-scoring protocol.
No generative or tool-calling capability is trained here.
"""
import hashlib
import json
import random
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import SYMPTOMS,SymptomSession
from scripts.evaluate_symptom_state_v1 import CASES,make
from scripts.compare_korean_decision_pilot import EXTRA_CASES,QUESTION,OPTIONS,CHECKSUMS
from scripts.evaluate_jev_style_qwen_pilot import NAMES,DESCRIPTIONS

DATA=ROOT/'data/processed/ko_decision_qlora_pilot_v1'
OUT=ROOT/'output/training/ko-decision-qlora-v1'
ADAPTER=ROOT/'adapters/ko-decision-qlora-v1'
MODEL=ROOT/'models/ko-decision-roberta-large'
NEW_CASES=[
 {'id':'holdout_greeting','turns':[('처음 뵙겠습니다. 상담을 받아보고 싶습니다.',make())]},
 {'id':'holdout_dry','turns':[('요즘 제 얼굴이 건조해요.',make(dryness='present'))]},
 {'id':'holdout_absent','turns':[('제 얼굴에는 여드름이 전혀 없어요.',make(breakout='absent'))]},
 {'id':'holdout_other','turns':[('동생 얼굴은 빨갛지만 제 피부는 붉지 않아요.',make(redness='absent'))]},
 {'id':'holdout_double','turns':[('피부가 가렵고 따가워요.',make(itching='present',stinging='present'))]},
 {'id':'holdout_preserve','turns':[('피부가 건조해요.',make(dryness='present')),
                               ('오늘은 비가 오네요.',make(dryness='present'))]},
 {'id':'holdout_correction','turns':[('얼굴에 여드름이 있어요.',make(breakout='present')),
                                 ('이제 여드름이 없어졌어요.',make(breakout='absent'))]},
 {'id':'holdout_question','turns':[('만약 화장품이 따갑다면 중단해야 하나요?',make())]},
]

def read_rows(name):
    path=DATA/(name+'.jsonl');manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest['sha256'][path.name]:raise ValueError('Dataset hash mismatch')
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines()]

def main():
    import torch,transformers,peft,bitsandbytes
    from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
    if OUT.exists() or ADAPTER.exists():raise FileExistsError('Run outputs already exist; preserve them')
    if not torch.cuda.is_available():raise RuntimeError('CUDA required for this experiment')
    with (MODEL/'model.safetensors').open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=CHECKSUMS['ko']:raise ValueError('Model hash mismatch')
    train=read_rows('train');val=read_rows('validation')
    if {x['text'] for x in train}&{x['text'] for x in val}:raise ValueError('train validation overlap')
    heldout_text={t[0] for c in NEW_CASES for t in c['turns']}
    if heldout_text&{r['text'] for r in train+val}:raise ValueError('heldout exact text overlap')
    seed=271828;random.seed(seed);torch.manual_seed(seed);torch.cuda.manual_seed_all(seed)
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False)
    # RoBERTa's classifier reads the first token, therefore left padding is invalid.
    tok.padding_side='right'
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForSequenceClassification.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False,
        quantization_config=quant,torch_dtype=torch.float16,device_map={'':0})
    base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=False)
    model=get_peft_model(base,LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,
        target_modules=['query','value'],bias='none'))
    params=[p for p in model.parameters() if p.requires_grad]
    trainable_names=[n for n,p in model.named_parameters() if p.requires_grad]
    if not params or any('lora_' not in n for n in trainable_names):raise ValueError('Unexpected trainable base/head')
    print('trainable',sum(p.numel() for p in params),'base 4bit, fp16 compute',flush=True)
    model.eval()

    def batch_encode(rows):
        first=[];second=[]
        for row in rows:
            situation='대상 증상: '+NAMES[row['field']]+'\n이전 상태: '+row['previous']+'\n이번 사용자 발화: '+row['text']
            for key in OPTIONS:
                first.append(QUESTION+' '+DESCRIPTIONS[key]);second.append(situation)
        encoded=tok(first,second,padding=True,truncation=False,return_tensors='pt')
        if encoded['input_ids'].shape[1]>512:raise ValueError('input too long')
        return {k:v.to('cuda') for k,v in encoded.items()}

    def logits_for(rows):
        return model(**batch_encode(rows)).logits[:,0].float().reshape(len(rows),4)

    def validate():
        model.eval();correct=0;losses=[];confusion={k:{v:0 for v in OPTIONS} for k in OPTIONS}
        with torch.inference_mode():
            for i in range(0,len(val),4):
                rows=val[i:i+4];logits=logits_for(rows)
                target=torch.tensor([OPTIONS.index(r['decision']) for r in rows],device='cuda')
                losses.append((len(rows),float(torch.nn.functional.cross_entropy(logits,target))))
                for r,p in zip(rows,logits.argmax(-1).tolist()):
                    confusion[r['decision']][OPTIONS[p]]+=1;correct+=OPTIONS[p]==r['decision']
        return {'n':len(val),'correct':correct,'accuracy':correct/len(val),
                'loss':sum(n*x for n,x in losses)/len(val),'confusion':confusion}

    def run_scenarios(cases):
        model.eval();res=[]
        for case in cases:
            session=SymptomSession();turns=[]
            for text,expected in case['turns']:
                before=session.state
                questions=[{'field':field,'previous':before[field],'text':text} for field in SYMPTOMS]
                with torch.inference_mode():logits=logits_for(questions)
                indices=logits.argmax(-1).tolist();decisions={field:OPTIONS[i] for field,i in zip(SYMPTOMS,indices)}
                patch={f:d for f,d in decisions.items() if d!='unchanged'}
                execution=session.update(patch) if patch else None
                turns.append({'input':text,'before':before,'expected':expected,'decisions':decisions,'patch':patch,
                              'tool_result':execution,'after':session.state,'matches':session.state==expected})
            res.append({'id':case['id'],'passes':all(t['matches'] for t in turns),'turns':turns})
        turns=[t for c in res for t in c['turns']]
        s={'scenarios':len(res),'scenario_passes':sum(c['passes'] for c in res),'turns':len(turns),
           'state_matches':sum(t['matches'] for t in turns),
           'field_matches':sum(t['after'][f]==t['expected'][f] for t in turns for f in SYMPTOMS),
           'fields':len(turns)*len(SYMPTOMS),
           'unknown_to_absent':sum(t['expected'][f]=='unknown' and t['after'][f]=='absent' for t in turns for f in SYMPTOMS)}
        return {'summary':s,'cases':res}

    OUT.mkdir(parents=True);ADAPTER.mkdir(parents=True)
    config={'seed':seed,'base':'mmetamong/ko-decision-roberta-large@4c38909ebec2e712d7c1d4e578847ad0ff7f6654',
       'quantization':'NF4 double quant, float16 compute','task':'choice ranking cross-entropy over 4 scores',
       'lora':{'r':8,'alpha':16,'dropout':0.05,'target_modules':['query','value'],'classifier_frozen':True},
       'train_items':len(train),'validation_items':len(val),'steps':60,'items_per_step':2,'lr':0.0002,
       'checkpoints':[20,40,60],'checkpoint_selection':'highest validation accuracy; ties choose earlier checkpoint',
       'training_data_sha256':hashlib.sha256((DATA/'train.jsonl').read_bytes()).hexdigest(),
       'evaluation':'same NF4 base, right padding, forward choice order; heldout not used for selection',
       'library_versions':{'torch':torch.__version__,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__},
       'device':torch.cuda.get_device_name(0),'disclaimer':'synthetic data; labels not independently reviewed; no AI Hub or personal data'}
    (OUT/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    baseline_val=validate();print('baseline validation',json.dumps(baseline_val,ensure_ascii=False),flush=True)
    baseline_dev=run_scenarios(CASES+EXTRA_CASES)
    baseline_hold=run_scenarios(NEW_CASES)
    (OUT/'baseline.json').write_text(json.dumps({'validation':baseline_val,'development':baseline_dev,'heldout':baseline_hold},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('baseline dev/heldout',baseline_dev['summary'],baseline_hold['summary'],flush=True)
    # Seeded fixed order, one example's four option scores per backward pass.
    optimizer=torch.optim.AdamW(params,lr=0.0002,weight_decay=0,foreach=False)
    model.train();optimizer.zero_grad(set_to_none=True);history=[];cursor=0;started=time.perf_counter();initial=None
    probe=train[:1]
    model.eval()
    with torch.inference_mode(): initial=logits_for(probe).cpu()
    model.train()
    for step in range(1,61):
        running=0
        for _ in range(2):
            row=train[cursor];cursor+=1
            logits=logits_for([row]);target=torch.tensor([OPTIONS.index(row['decision'])],device='cuda')
            loss=torch.nn.functional.cross_entropy(logits,target)
            if not torch.isfinite(loss):raise ValueError('non-finite loss')
            (loss/2).backward();running+=float(loss.detach())/2
        norm=float(torch.nn.utils.clip_grad_norm_(params,1.0))
        if not (norm>0 and torch.isfinite(torch.tensor(norm))):raise ValueError('zero or nonfinite LoRA gradients')
        optimizer.step();optimizer.zero_grad(set_to_none=True)
        if step%10==0:print('step',step,'train_loss',round(running,4),'sec',round(time.perf_counter()-started),'peak_gib',round(torch.cuda.max_memory_allocated()/1024**3,2),flush=True)
        if step in [20,40,60]:
            validation=validate();folder=ADAPTER/f'step-{step}';model.save_pretrained(folder,safe_serialization=True)
            history.append({'step':step,'train_examples_seen':cursor,'validation':validation,'adapter':str(folder.relative_to(ROOT))})
            (OUT/'history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('snapshot',step,'val accuracy',validation['accuracy'],'loss',validation['loss'],flush=True)
            model.train()
    selected=max(history,key=lambda x:(x['validation']['accuracy'],-x['step']))
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    selected_file=ROOT/selected['adapter']/'adapter_model.safetensors'
    set_peft_model_state_dict(model,load_file(str(selected_file)))
    model.eval()
    with torch.inference_mode():after=logits_for(probe).cpu()
    delta=float((after-initial).abs().max())
    if delta<1e-6:raise ValueError('Adapter did not change probe logits')
    # Verify saved adapter reloading agrees on a probe after perturbing adapter weights.
    with torch.no_grad():params[0].add_(0.01)
    set_peft_model_state_dict(model,load_file(str(selected_file)))
    with torch.inference_mode():reloaded=logits_for(probe).cpu()
    reload_delta=float((reloaded-after).abs().max())
    if reload_delta>1e-4:raise ValueError('Adapter reload logits mismatch')
    post_dev=run_scenarios(CASES+EXTRA_CASES);post_hold=run_scenarios(NEW_CASES)
    report={'selected':selected,'probe_logit_change':delta,'reload_max_abs_difference':reload_delta,
            'development':post_dev,'heldout':post_hold,'peak_cuda_allocated_gib':torch.cuda.max_memory_allocated()/1024**3,
            'train_seconds_including_validation':time.perf_counter()-started}
    (OUT/'trained.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('selected step',selected['step'],'heldout',post_hold['summary'],'reload difference',reload_delta,flush=True)

if __name__=='__main__':main()
