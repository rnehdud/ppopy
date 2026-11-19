"""Compare full vs reranked user-turn blocks in held-out synthetic dialogues.

Uses one 2048-position copy-extended baseline for all scoring; no training.
Compares original <=2048 context to reranked <=1500 context and a latest-turn
control. System messages and the latest complete user turn are always kept;
tool calls and corresponding tool results stay in the same turn block.
An overflow is never silently truncated or counted as a correct action.
"""
import csv,json,random,sys,time
from pathlib import Path
import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
from peft import PeftModel,prepare_model_for_kbit_training

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/kure-multiturn-heldout-v1'
OUT=ROOT/'output/kure-multiturn-heldout-v2'
BASE=ROOT/'models/ko-decision-roberta-large'
RERANK=ROOT/'models/kure-reranker-nano'
ADAPTER=ROOT/'data/processed/context-paired-kaggle-v2/adapter'
QUESTION='사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.'

def read(path):return [json.loads(x) for x in path.read_text(encoding='utf8').splitlines() if x.strip()]
def turns(history):
 systems=[];blocks=[]
 for m in history:
  if m.get('role')=='system':
   if blocks:raise ValueError('system message after a user turn')
   systems.append(m)
  elif m.get('role')=='user':blocks.append([m])
  else:
   if not blocks:raise ValueError('orphan message before first turn')
   blocks[-1].append(m)
 if not systems or len(blocks)<2:raise ValueError('insufficient turns')
 return systems,blocks

def main():
 if OUT.exists():raise FileExistsError(OUT)
 source=read(DATA/'over512.jsonl')
 source=[r for r in source if 1024<r['full_tokens']<=2048 and sum(m.get('role')=='user' for m in r['history'])>=2]
 rng=random.Random(740912);call=[r for r in source if r['target']!='no_tool'];none=[r for r in source if r['target']=='no_tool']
 if min(len(call),len(none))<30:raise ValueError('insufficient stratified examples')
 sample=rng.sample(call,30)+rng.sample(none,30);rng.shuffle(sample)
 # Fix sample before running any model.
 OUT.mkdir(parents=True)
 (OUT/'sample.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2),encoding='utf8')
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True);tok.model_max_length=2048;tok.padding_side='right'
 rt=AutoTokenizer.from_pretrained(RERANK,local_files_only=True)
 ranker=AutoModelForSequenceClassification.from_pretrained(RERANK,local_files_only=True,torch_dtype=torch.float16).to('cuda').eval()
 q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
 base=AutoModelForSequenceClassification.from_pretrained(BASE,quantization_config=q,torch_dtype=torch.float16,device_map={'':0},local_files_only=True)
 base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=True)
 model=PeftModel.from_pretrained(base,str(ADAPTER)).eval();emb=model.get_base_model().roberta.embeddings;old=emb.position_embeddings
 new=torch.nn.Embedding(2050,old.embedding_dim,padding_idx=old.padding_idx,device='cuda',dtype=old.weight.dtype)
 with torch.no_grad():
  new.weight[:514].copy_(old.weight)
  for i in range(514,2050,512):new.weight[i:i+512].copy_(old.weight[2:514])
 emb.position_embeddings=new;emb.register_buffer('position_ids',torch.arange(2050,device='cuda').expand((1,-1)),persistent=False)
 emb.register_buffer('token_type_ids',torch.zeros((1,2050),dtype=torch.long,device='cuda'),persistent=False)
 model.get_base_model().config.max_position_embeddings=2050
 def make_context(r,systems,blocks,indices):
  history=systems+[m for i in sorted(indices) for m in blocks[i]]
  return '대화:\n'+json.dumps(history,ensure_ascii=False)+'\n이번 사용자 발화: '+r['input']
 def tokens(r,context):
  return max(len(tok(QUESTION+' '+v,context,truncation=False)['input_ids']) for v in r['options'].values())
 def inference(r,ctx,max_tokens):
  n=tokens(r,ctx)
  if n>max_tokens:return {'predicted':None,'match':False,'error':'preserved_context_exceeds_budget','tokens':n}
  # Small option batches cap VRAM, without changing scores or dropping tokens.
  values=list(r['options'].values());logits=[]
  with torch.inference_mode():
   for j in range(0,len(values),2):
    v=values[j:j+2];b=tok([QUESTION+' '+x for x in v],[ctx]*len(v),padding=True,truncation=False,return_tensors='pt')
    logits.extend(model(**{k:x.to('cuda') for k,x in b.items()}).logits[:,0].float().cpu().tolist())
  pred=list(r['options'])[max(range(len(logits)),key=lambda i:logits[i])]
  return {'predicted':pred,'match':pred==r['target'],'error':None,'tokens':n}
 records=[];start=time.perf_counter()
 for j,r in enumerate(sample):
  systems,blocks=turns(r['history']);latest=len(blocks)-1
  full=make_context(r,systems,blocks,range(len(blocks)))
  if tokens(r,full)!=r['full_tokens']:raise ValueError('unexpected serialized history change')
  recent=make_context(r,systems,blocks,[latest]);ranked=[]
  older=blocks[:-1]
  if older:
   docs=[json.dumps(turn,ensure_ascii=False) for turn in older]
   b=rt([r['input']]*len(docs),docs,padding=True,truncation=False,return_tensors='pt')
   if b['input_ids'].shape[1]>8192:raise ValueError('reranker input too long')
   with torch.inference_mode():s=ranker(**{k:v.to('cuda') for k,v in b.items()}).logits[:,0].float().cpu().tolist()
   ranked=sorted(range(len(older)),key=lambda i:(-s[i],i))
  keep=[latest]
  for k in ranked:
   trial=sorted(keep+[k])
   if tokens(r,make_context(r,systems,blocks,trial))<=1500:keep=trial
  filtered=make_context(r,systems,blocks,keep)
  record={'id':r['id'],'expected':r['target'],'user_input':r['input'],'n_turns':len(blocks),'selected_turns':keep,
    'ranking':ranked,'full_history':r['history'],'selected_history':systems+[m for i in keep for m in blocks[i]],
    'full_2048':inference(r,full,2048),'recent_1500':inference(r,recent,1500),'kure_1500':inference(r,filtered,1500)}
  records.append(record)
  if (j+1)%10==0:
   print('evaluated',j+1,'/',len(sample),'seconds',round(time.perf_counter()-start),flush=True)
   (OUT/'partial.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
 summary={}
 for mode in ('full_2048','recent_1500','kure_1500'):
  a=[{'expected':r['expected']}|r[mode] for r in records]
  summary[mode]={'n':len(a),'eligible':sum(x['error'] is None for x in a),'correct':sum(x['match'] for x in a),
   'overflow':sum(x['error'] is not None for x in a),'call_n':sum(x['expected']!='no_tool' for x in a),
   'call_correct':sum(x['match'] and x['expected']!='no_tool' for x in a),
   'no_tool_n':sum(x['expected']=='no_tool' for x in a),'no_tool_correct':sum(x['match'] and x['expected']=='no_tool' for x in a),
   'mean_tokens':round(sum(x['tokens'] for x in a)/len(a),1)}
 result={'summary':summary,'records':records,'design':{'seed':740912,'sample':'30 tool and 30 no_tool verified synthetic labels; not natural prevalence',
  'original_model':'ko-decision-roberta-large with original kotraj adapter; copied position embeddings extended to 2048 without new training',
  'filter':'KURE ranks complete older user-turn blocks; system and latest full block mandatory; maximum 1500 tokens',
  'caution':'Previously unobserved group per available logs, but shared synthetic data source and catalog. Next actions are not independently human reviewed; filtering can delete needed past state. No actual tools executed.'}}
 (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 fields=['id','user_input','expected','n_turns','selected_turns','full_prediction','recent_prediction','kure_prediction','full_tokens','recent_tokens','kure_tokens','recent_error','kure_error','human_verdict','notes']
 with (OUT/'review.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in records:
   row={k:r.get(k,'') for k in fields};row['selected_turns']=json.dumps(r['selected_turns'])
   for mode,alias in [('full_2048','full'),('recent_1500','recent'),('kure_1500','kure')]:
    for key in ('predicted','tokens','error'):row[alias+'_'+('prediction' if key=='predicted' else key)]=r[mode][key]
   w.writerow({k:row.get(k,'') for k in fields})
 print('SUMMARY',json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
