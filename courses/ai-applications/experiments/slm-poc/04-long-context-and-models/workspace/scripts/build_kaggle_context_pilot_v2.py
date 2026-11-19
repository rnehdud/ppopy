"""Build paired short/long examples from the previously reserved kotraj splits.

The original dialogue, options and generated source action are retained. The
only change is an unrelated document before or after the complete dialogue.
No label is represented as independently human-verified.
"""
import csv,hashlib,json,random,zipfile
from pathlib import Path
from transformers import AutoTokenizer

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/processed/kotraj-200-v1'
DEST=ROOT/'data/processed/context-paired-kaggle-v2'
ADAPTER=ROOT/'output/training/kotraj-kaggle-complete-v1/kotraj_choice/kotraj-choice-full-gpu-v1/final_adapter'
ZIP=ROOT/'output/context-paired-kaggle-input-v2.zip'
FILLERS={
 'train':['바닷가의 하늘에는 구름이 있었고 파도가 모래 위에 부서졌다. ', '산길에 나무가 서 있었고 바람에 잎사귀가 조금씩 흔들렸다. ', '도서관 창문으로 빛이 들어오고 탁자에는 오래된 책이 놓여 있었다. '],
 'dev':['먼 산의 돌 사이로 작은 새들이 날아가고 아침 안개가 걷혔다. ', '공원의 벤치 곁에서 노란 잎이 바람을 따라 천천히 떨어졌다. '],
 'test':['강가의 다리 아래로 맑은 물이 흐르고 하얀 구름이 비쳤다. ', '낮은 언덕 너머로 해가 지고 들판에는 그림자가 길게 드리웠다. ']}

def main():
 if DEST.exists() or ZIP.exists():raise FileExistsError('Output already exists; choose a new version.')
 tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True);tok.model_max_length=1000000
 rng=random.Random(739018);splits={};all_groups=set();stats={}
 for split in ('train','dev','test'):
  data=[json.loads(x) for x in (SRC/(split+'.jsonl')).read_text(encoding='utf8').splitlines() if x.strip()]
  group={x['group'] for x in data}
  if len(group)!=len(data) or group&all_groups:raise ValueError('Source group overlap')
  all_groups|=group;built=[]
  for r in data:
   if r['target'] not in r['options']:raise ValueError('missing target')
   opts=r['options'];question=r['question'];old=r['context']
   longest=max(opts.values(),key=lambda v:len(tok(question+' '+v,add_special_tokens=False)['input_ids']))
   def length(text):return len(tok(question+' '+longest,text,truncation=False)['input_ids'])
   if length(old)>512:raise ValueError('unexpected long source')
   filler=rng.choice(FILLERS[split]);goal=rng.randint(790,1010);placement=rng.choice(('before','after'))
   def context(n):return '별도 문서:\n'+filler*n+'\n\n'+old
   lo,hi=0,256
   while lo<hi:
    mid=(lo+hi+1)//2
    if length(context(mid))<=goal:lo=mid
    else:hi=mid-1
   long=context(lo);n=length(long)
   if not (512<n<=1024) or not (long.endswith(old) or long.startswith(old)):raise ValueError('invalid augmented input')
   base={'id':r['id'],'group':r['group'],'question':question,'options':opts,'target':r['target'],
    'input':r['input'],'source':'kotraj synthetic observed action; not independently human verified'}
   built.append(base|{'short_context':old,'long_context':long,'short_max_tokens':length(old),'long_max_tokens':n,'added_filler':filler,'filler_repetitions':lo,'filler_placement':placement})
  splits[split]=built;stats[split]={'groups':len(built),'short_no_tool':sum(x['target']=='no_tool' for x in built),
   'long_min_tokens':min(x['long_max_tokens'] for x in built),'long_max_tokens':max(x['long_max_tokens'] for x in built)}
 DEST.mkdir(parents=True);(DEST/'adapter').mkdir()
 for n in ('adapter_config.json','adapter_model.safetensors'):
  (DEST/'adapter'/n).write_bytes((ADAPTER/n).read_bytes())
 for split,data in splits.items():
  (DEST/(split+'.jsonl')).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf8')
 with (DEST/'review_sample.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['split','id','input','target','options_json','short_context','long_context','human_verdict','notes']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for split in ('train','dev','test'):
   samples=splits[split][:10]
   for r in samples:w.writerow({k:({'split':split,'options_json':json.dumps(r['options'],ensure_ascii=False)}|r).get(k,'') for k in fields})
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 files={str(p.relative_to(DEST)).replace('\\','/'):sha(p) for p in DEST.rglob('*') if p.is_file()}
 manifest={'version':'context-paired-kaggle-v2','seed':739018,'source_splits':'data/processed/kotraj-200-v1',
  'stats':stats,'files':files,'warning':'Synthetic observed actions; human review incomplete; dev/test have been inspected in earlier work. Same meaning under filler is an assumption requiring review. No claim of independent generalization.'}
 (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
 ZIP.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in DEST.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(DEST).as_posix())
 print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True);print('bundle',ZIP,flush=True)
if __name__=='__main__':main()
