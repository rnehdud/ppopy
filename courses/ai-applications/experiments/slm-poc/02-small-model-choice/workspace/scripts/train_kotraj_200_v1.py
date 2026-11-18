"""Exploratory QLoRA comparison using 200 kotraj decisions.

The source is synthetic, labels were reviewed only by the assistant, and
training/dev/test share a fixed catalog of tools. Never deploy automatically.
"""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from agent.choice_agent_v1 import ChoiceAgent
from scripts.train_choice_agent_v1 import MODEL
from evaluate_cosmetics_conversations import CASES

DATA=ROOT/'data/processed/kotraj-200-v1'
OUT=ROOT/'output/training/kotraj-200-v1'
ADAPTER=ROOT/'adapters/kotraj-200-v1'
BASE=ROOT/'adapters/cosmetics-chat-v1/step-0100'
def rows(path):return [json.loads(line) for line in path.read_text(encoding='utf8').splitlines() if line.strip()]
def main():
 import torch
 from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
 from peft import PeftModel,prepare_model_for_kbit_training,set_peft_model_state_dict
 from safetensors.torch import load_file
 if OUT.exists() or ADAPTER.exists():raise FileExistsError('existing outputs protected')
 random.seed(9122026);torch.manual_seed(9122026);torch.cuda.manual_seed_all(9122026)
 train,dev,test=[rows(DATA/(s+'.jsonl')) for s in ('train','dev','test')]
 groups=[{r['group'] for r in split} for split in (train,dev,test)]
 assert all(not groups[i]&groups[j] for i in range(3) for j in range(i))
 tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False);tok.padding_side='right'
 q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
 base=AutoModelForSequenceClassification.from_pretrained(MODEL,quantization_config=q,torch_dtype=torch.float16,device_map={'':0},local_files_only=True,trust_remote_code=False)
 base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=True)
 model=PeftModel.from_pretrained(base,str(BASE),is_trainable=True)
 names=[n for n,p in model.named_parameters() if p.requires_grad]
 if not names or any('lora_' not in n for n in names):raise RuntimeError('unexpected trainable parameters')
 def logits(r):
  options=r['options'];a=[r['question']+' '+v for v in options.values()]
  batch=tok(a,[r['context']]*len(a),padding=True,truncation=False,return_tensors='pt')
  if batch['input_ids'].shape[1]>512:raise ValueError('input too long; no truncation')
  return model(**{k:v.to('cuda') for k,v in batch.items()}).logits[:,0].float()
 def score(question,options,context):
  with torch.inference_mode():s=logits({'question':question,'options':options,'context':context})
  return dict(zip(options,torch.softmax(s.double(),dim=0).tolist()))
 def evaluate(data):
  model.eval();out=[]
  for r in data:
   with torch.inference_mode():s=logits(r)
   predicted=list(r['options'])[int(s.argmax())]
   out.append({'id':r['id'],'input':r['input'],'domain':r['domain'],'expected':r['target'],
      'predicted':predicted,'match':predicted==r['target']})
  return {'n':len(out),'correct':sum(r['match'] for r in out),
          'call':{'n':sum(r['expected']!='no_tool' for r in out),'correct':sum(r['match'] and r['expected']!='no_tool' for r in out)},
          'no_call':{'n':sum(r['expected']=='no_tool' for r in out),'correct':sum(r['match'] and r['expected']=='no_tool' for r in out)},'rows':out}
 def cosmetics_regression():
  model.eval();out=[]
  for name,turns in CASES:
   a=ChoiceAgent(score,available=('record','show','ask','none'));expected=a.session.state
   for text,actions,patch,_reply in turns:
    expected.update(patch);trace=a.turn(text)
    out.append({'scenario':name,'input':text,'action':trace['action'],'expected_actions':actions,
     'state':trace['after'],'expected_state':expected.copy(),
     'action_ok':trace['action'] in actions,'state_ok':trace['after']==expected})
  return {'n':len(out),'action_ok':sum(r['action_ok'] for r in out),'state_ok':sum(r['state_ok'] for r in out),'rows':out}
 OUT.mkdir(parents=True);ADAPTER.mkdir(parents=True)
 old=rows(ROOT/'data/processed/choice_agent_v2/train.jsonl')
 replay=[r for r in old if r['kind']=='symptom' or (r['kind']=='tool' and r['target'] in ('record','show','ask','none'))]
 random.shuffle(replay);replay=replay[:40]
 training=train+replay;random.shuffle(training)
 print('train unique kotraj',len(train),'repeat',1,'replay',len(replay),'dev',len(dev),'test',len(test),flush=True)
 history=[];start=time.perf_counter()
 def checkpoint(step):
  val=evaluate(dev);folder=ADAPTER/f'step-{step:04}';model.save_pretrained(folder,safe_serialization=True)
  history.append({'step':step,'adapter':str(folder.relative_to(ROOT)),'dev':val})
  print('checkpoint',step,'dev',val['correct'],'/',val['n'],'elapsed',round(time.perf_counter()-start),flush=True)
 # Test and regression are measured only after dev-based checkpoint selection.
 checkpoint(0)
 params=[p for p in model.parameters() if p.requires_grad]
 opt=torch.optim.AdamW(params,lr=1e-5,weight_decay=0,foreach=False);model.train()
 step=0;opt.zero_grad(set_to_none=True)
 for j,r in enumerate(training):
  s=logits(r);loss=torch.nn.functional.cross_entropy(s.unsqueeze(0),torch.tensor([list(r['options']).index(r['target'])],device='cuda'))/2
  if not torch.isfinite(loss):raise RuntimeError('non-finite loss')
  loss.backward()
  if j%2==1 or j==len(training)-1:
   norm=torch.nn.utils.clip_grad_norm_(params,1)
   if not torch.isfinite(norm):raise RuntimeError('non-finite gradients')
   opt.step();opt.zero_grad(set_to_none=True);step+=1
   if step%10==0:print('step',step,'loss',round(float(loss.detach())*2,4),flush=True)
   if step==len(training)//4:checkpoint(step);model.train()
 checkpoint(step)
 selected=max(history,key=lambda x:(x['dev']['correct'],-x['step']))
 def load(item):set_peft_model_state_dict(model,load_file(str(ROOT/item['adapter']/'adapter_model.safetensors')));model.eval()
 load(history[0]);before=evaluate(test);reg_before=cosmetics_regression()
 load(selected);after=evaluate(test);reg_after=cosmetics_regression()
 load(history[-1]);final=evaluate(test);reg_final=cosmetics_regression()
 config={'source':'drlee1/kotraj','revision':'dffbf2552bcd6b93ab0a3d50947499a9d688c66d',
  'base':str(BASE.relative_to(ROOT)),'quantization':'NF4 double quant fp16 compute','train_unique':len(train),
  'train_repeat':1,'replay':len(replay),'epochs':1,'lr':1e-5,'gradient_accumulation':2,
  'train_groups':[sorted(x) for x in groups], 'selected_by':'dev exact match, earliest checkpoint on tie',
  'caveat':'synthetic source labels, spot checked only and no independent human review; mostly first-turn examples, fixed tools across splits; no arguments executed; no Qwen evaluation'}
 result={'config':config,'history':history,'selected':selected,'test_before':before,'test_after':after,
         'cosmetics_before':reg_before,'cosmetics_after':reg_after,'test_final':final,'cosmetics_final':reg_final,
         'seconds':round(time.perf_counter()-start,2)}
 (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print('RESULT',json.dumps({'selected_step':selected['step'],'test_before':before['correct'],'test_after':after['correct'],'test_final':final['correct'],
 'cosmetics_before':{k:reg_before[k] for k in ('n','action_ok','state_ok')},
 'cosmetics_after':{k:reg_after[k] for k in ('n','action_ok','state_ok')},
 'cosmetics_final':{k:reg_final[k] for k in ('n','action_ok','state_ok')}},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
