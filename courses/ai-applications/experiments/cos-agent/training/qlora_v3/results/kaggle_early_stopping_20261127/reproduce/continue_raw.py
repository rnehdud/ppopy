"""Kaggle inference-only continuation. No training or automatic semantic approval."""
import argparse,contextlib,hashlib,json,os,shutil,subprocess,sys,time,zipfile
from pathlib import Path
REV='cdbee75f17c01a7cc42f958dc650907174af0554'
MODELS=['kaggle-base']+[f'kaggle-epoch-{e}' for e in range(1,5)]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp')
 t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');os.replace(t,p)
def lines(p):return [json.loads(l) for l in Path(p).read_text(encoding='utf-8').splitlines() if l.strip()] if Path(p).exists() else []
def unpack(z,target):
 with zipfile.ZipFile(z) as f:
  root=target.resolve()
  for item in f.infolist():
   if not (root/item.filename).resolve().is_relative_to(root):raise ValueError('Unsafe ZIP member')
  f.extractall(target)
def worker(bundle,adapters,out,models):
 # CUDA_VISIBLE_DEVICES is assigned before this subprocess imports torch.
 os.environ.update(TOKENIZERS_PARALLELISM='false',USE_TF='0',USE_FLAX='0')
 import torch
 from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
 from peft import PeftModel
 assert torch.cuda.is_available(),'GPU required; CPU fallback is forbidden'
 torch.manual_seed(20261127)
 tokenizer=AutoTokenizer.from_pretrained(adapters/'checkpoints/epoch-02',local_files_only=True)
 rows=read(bundle/'validation_inputs.json');assert len(rows)==90
 local=lines(bundle/'local_archive/raw_answers.jsonl');lk={(r['row_id'],r['model']):r for r in local}
 reviews=lines(bundle/'local_archive/manual_reviews.jsonl')
 for n in reviews:assert n['candidate_sha256']==lk[n['row_id'],n['model']]['content_sha256']
 input_ids={}
 for row in rows:
  assert row['split']=='val_internal' and [m['role'] for m in row['messages']]==['system','user','assistant']
  ids=tokenizer.apply_chat_template(row['messages'][:-1],tokenize=True,add_generation_prompt=True)
  assert len(ids)+768<=3072,'Never truncate inputs or answers silently'
  ids_sha=hashlib.sha256(json.dumps(ids).encode()).hexdigest()
  for m in MODELS:
   old=lk.get((row['id'],m))
   if old:assert old['prompt_ids_sha256']==ids_sha,('Tokenizer input differs',row['id'],m)
  input_ids[row['id']]=ids
 plan=read(bundle/'evaluation_plan.json')
 for e in range(1,5):
  for name in ['adapter_model.safetensors','adapter_config.json']:
   assert digest(adapters/f'checkpoints/epoch-{e:02d}'/name)==plan['checkpoint_file_hashes_verified'][f'epoch-{e}/{name}']
 model=AutoModelForCausalLM.from_pretrained('Qwen/Qwen3-4B-Instruct-2507',revision=REV,
  quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16),
  torch_dtype=torch.float16,device_map={'':0},attn_implementation='sdpa')
 model.eval();pad=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
 gpu=os.environ['CUDA_VISIBLE_DEVICES'];raw=out/f'raw_gpu{gpu}.jsonl'
 prior=lines(raw);done={(r['row_id'],r['model']) for r in prior}
 for r in prior:assert hashlib.sha256(r['text'].encode()).hexdigest()==r['content_sha256']
 # Finish missing local answers first. Replay the 133 local entries afterward,
 # because T4 FP16 / Transformers outputs must not be merged with BF16 vLLM as one cohort.
 jobs=[(row,m) for row in rows for m in models if (row['id'],m) not in done]
 jobs.sort(key=lambda j:((j[0]['id'],j[1]) in lk,models.index(j[1])))
 attached=False;loaded=set();last=None
 save(out/f'worker_gpu{gpu}_context.json',{'GPU':torch.cuda.get_device_name(0),'models':models,'torch':torch.__version__,
  'generation_backend':'Transformers+PEFT NF4/FP16 SDPA','training_performed':False,'production_enabled':False,
  'manual_review':'pending; local notes are retained only for their original content hashes'})
 for row,m in jobs:
  if m!='kaggle-base' and m!=last:
   ep=int(m.rsplit('-',1)[1]);path=adapters/f'checkpoints/epoch-{ep:02d}'
   if not attached:model=PeftModel.from_pretrained(model,path,adapter_name=m,is_trainable=False);attached=True;loaded.add(m)
   elif m not in loaded:model.load_adapter(path,adapter_name=m,is_trainable=False);loaded.add(m)
   model.set_adapter(m);model.eval()
  last=m;ids=input_ids[row['id']];x=torch.tensor([ids],dtype=torch.long,device='cuda:0')
  torch.cuda.synchronize();start=time.perf_counter()
  with torch.inference_mode(),(model.disable_adapter() if m=='kaggle-base' and attached else contextlib.nullcontext()):
   generated=model.generate(input_ids=x,attention_mask=torch.ones_like(x),max_new_tokens=768,
    do_sample=False,num_beams=1,pad_token_id=pad,use_cache=True)
  torch.cuda.synchronize();elapsed=time.perf_counter()-start;tail=generated[0,len(ids):].tolist()
  text=tokenizer.decode(tail,skip_special_tokens=True);sha=hashlib.sha256(text.encode()).hexdigest()
  old=lk.get((row['id'],m))
  record={'row_id':row['id'],'mode':row['mode'],'model':m,'text':text,'content_sha256':sha,
   'prompt_ids_sha256':hashlib.sha256(json.dumps(ids).encode()).hexdigest(),'prompt_tokens':len(ids),
   'generated_tokens':len(tail),'finish_reason':'length' if len(tail)==768 and tail[-1]!=tokenizer.eos_token_id else 'stop',
   'latency_s':elapsed,'timestamp_ms':int(time.time()*1000),'semantic_review':'pending','human_approved':False,
   'generation_cohort':'kaggle_transformers_nf4_fp16_20261127','phase':'replay_local' if old else 'missing_local',
   'local_content_sha256':old['content_sha256'] if old else None,
   'matches_local_text_exactly':sha==old['content_sha256'] if old else None}
  with raw.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
  done.add((row['id'],m));save(out/f'progress_gpu{gpu}.json',{'completed':len(done),'total_worker':90*len(models),'last_id':row['id'],'last_model':m})
  print(json.dumps({'gpu':gpu,'completed':len(done),'model':m,'row_id':row['id'],'tokens':len(tail),'seconds':round(elapsed,2)},ensure_ascii=False),flush=True)
def main():
 inp=Path('/kaggle/input');out=Path('/kaggle/working/ppopy_raw_continuation');out.mkdir(parents=True,exist_ok=True)
 manifests=[p for p in inp.rglob('resume_manifest.json') if read(p).get('format')=='ppopy-raw-resume-v1']
 if manifests:
  assert len(manifests)==1,manifests
  bundle=manifests[0].parent
 else:
  bundles=list(inp.rglob('ppopy_raw_resume_20261127.zip'));assert len(bundles)==1,bundles
  bundle=out/'resume_bundle';unpack(bundles[0],bundle)
 manifest=read(bundle/'resume_manifest.json')
 for name,sha in manifest['files'].items():assert digest(bundle/name)==sha,name
 sources=[p.parent for p in inp.rglob('run_context.json') if (p.parent/'checkpoints/epoch-04/adapter_model.safetensors').exists()]
 assert len(sources)==1,('Attach linawf/5epoch-qlora v2 outputs',sources)
 adapters=sources[0]
 shutil.copytree(bundle/'local_archive',out/'local_archive',dirs_exist_ok=True)
 save(out/'continuation_plan.json',{'local_answers':manifest['local_answers'],'local_manual_reviews':manifest['local_manual_reviews'],
  'target_new_cohort':450,'missing_local_first':450-manifest['local_answers'],'replay_local_afterward':manifest['local_answers'],
  'training_performed':False,'human_approved':False,'precision_change':'Local NF4/BF16 vLLM -> Kaggle NF4/FP16 Transformers; cohorts remain separate',
  'selection':'No semantic sweet spot is claimed until each new answer is actually reviewed.'})
 import torch
 assert torch.cuda.is_available();ngpu=torch.cuda.device_count();assert ngpu>=1
 groups=[['kaggle-base'],MODELS[1:]] if ngpu>=2 else [MODELS]
 procs=[]
 for gpu,ms in enumerate(groups):
  env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(gpu),USE_TF='0',USE_FLAX='0',TOKENIZERS_PARALLELISM='false')
  log=(out/f'worker_gpu{gpu}.log').open('a',encoding='utf-8')
  p=subprocess.Popen([sys.executable,__file__,'--worker','--bundle',str(bundle),'--adapters',str(adapters),'--output',str(out),'--models',*ms],env=env,stdout=log,stderr=subprocess.STDOUT)
  procs.append((p,log,gpu));print('started GPU',gpu,ms,flush=True)
 # Stream worker progress while leaving each record durable for another resume.
 while any(p.poll() is None for p,_,_ in procs):
  for _,_,gpu in procs:
   path=out/f'progress_gpu{gpu}.json'
   if path.exists():print(json.dumps(read(path),ensure_ascii=False),flush=True)
  time.sleep(30)
 for p,log,gpu in procs:
  log.close()
  if p.returncode:
   print((out/f'worker_gpu{gpu}.log').read_text(encoding='utf-8')[-10000:],flush=True)
   raise RuntimeError(f'GPU worker {gpu} failed: {p.returncode}; partial raw files retained')
 rows=read(bundle/'validation_inputs.json');answers=[r for p in out.glob('raw_gpu*.jsonl') for r in lines(p)]
 by={(r['row_id'],r['model']):r for r in answers};assert len(by)==len(answers)==450
 with (out/'raw_answers_kaggle.jsonl').open('w',encoding='utf-8',newline='\n') as f:
  for row in rows:
   for m in MODELS:f.write(json.dumps(by[row['id'],m],ensure_ascii=False)+'\n')
 for i,row in enumerate(rows,1):save(out/f'cases/{i:03d}_{row["id"]}.json',{'index':i,'row_id':row['id'],'mode':row['mode'],
  'request':json.loads(row['messages'][1]['content']),'reference_teacher_answer':row['messages'][2]['content'],
  'answers':[by[row['id'],m] for m in MODELS],'review_state':'pending; do not reuse local PASS for different content hashes'})
 save(out/'generation_complete.json',{'answers':450,'cases':90,'semantic_review_complete':False,'training_performed':False,
  'local_raw_preserved':manifest['local_answers'],'local_manual_reviews_preserved':manifest['local_manual_reviews'],
  'matches_local_text_exactly':sum(r['matches_local_text_exactly'] is True for r in answers),'human_approved':False})
 print('450 raw answers generated. Content review and semantic sweet spot decision are still pending.',flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');parser.add_argument('--bundle',type=Path);parser.add_argument('--adapters',type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--models',nargs='+');args=parser.parse_args()
 if args.worker:worker(args.bundle,args.adapters,args.output,args.models)
 else:main()
