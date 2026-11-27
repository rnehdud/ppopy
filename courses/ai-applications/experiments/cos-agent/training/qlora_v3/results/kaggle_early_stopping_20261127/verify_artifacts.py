"""Integrity/arithmetic checks, NOT an automatic semantic critic. Standard library only."""
import ast,hashlib,json,math
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def lines(p):return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(x):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from leaves(v)
 elif isinstance(x,list):
  for v in x:yield from leaves(v)
def main():
 manifest=read(HERE/'artifact_manifest.json')
 for name,item in manifest['files'].items():
  p=(HERE/name).resolve();assert p.is_relative_to(HERE)
  assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],name
 for item in read(HERE/'copy_receipts.json'):assert sha(HERE/item['file'])==item['source_sha256'],item['file']
 banned={'.safetensors','.bin','.pt','.pth','.ckpt','.gguf'}
 assert not [p for p in HERE.rglob('*') if p.is_file() and p.suffix.lower() in banned]
 dataset=HERE.parents[3]/'data/qlora/v2/qlora_solution_hold_v2.jsonl'
 assert sha(dataset)=='99182590f83bc3dad9e3cb71c9153f418642b6aaf7d97ebcc728ac68d0425cac'
 full=lines(dataset);train=[r for r in full if r['split']=='train'];val=[r for r in full if r['split']=='val_internal']
 assert (len(train),len(val))==(810,90)
 for key in ['id','group_id','scenario_family_id']:assert not ({r[key] for r in train}&{r[key] for r in val})
 assert read(HERE/'local_replay/validation_inputs.json')==val
 cfg1=read(HERE/'training_v1_5epoch/config.json');cfg2=read(HERE/'training_v2_early_stopping/config.json')
 assert cfg1['learning_rate']==cfg2['learning_rate']==1e-4
 assert not cfg1['early_stopping'] and cfg2['early_stopping']
 counts={}
 for folder,epochs in [('training_v1_5epoch',5),('training_v2_early_stopping',4)]:
  history=read(HERE/folder/'epoch_history.json');assert len(history)==epochs
  for e,h in enumerate(history,1):
   for name,role,key in [('train_eval_losses.jsonl',train,'train_eval_token_loss'),('val_losses.jsonl',val,'val_token_loss')]:
    rr=lines(HERE/folder/f'history/epoch-{e:02d}'/name)
    assert len(rr)==len(role) and {r['row_id'] for r in rr}=={r['id'] for r in role}
    assert all(math.isfinite(r['assistant_token_loss']) and r['assistant_tokens']>0 for r in rr)
    weighted=sum(r['assistant_token_loss']*r['assistant_tokens'] for r in rr)/sum(r['assistant_tokens'] for r in rr)
    assert math.isclose(weighted,h[key],abs_tol=1e-8), (folder,e,key,weighted,h[key])
  counts[folder]={'epochs':epochs,'best_val_epoch':min(history,key=lambda r:r['val_token_loss'])['epoch']}
 es=read(HERE/'training_v2_early_stopping/early_stopping.json');assert es['stopped_epoch']==4 and es['best_epoch']==2
 raw=lines(HERE/'local_replay/raw_answers.jsonl');notes=lines(HERE/'local_replay/manual_reviews.jsonl')
 by={(r['row_id'],r['model']):r for r in raw};assert len(raw)==len(by)==len(notes)==133
 assert len({(n['row_id'],n['model']) for n in notes})==133
 cases={c['row_id']:c for c in (read(p) for p in (HERE/'local_replay/cases').glob('*.json'))}
 for n in notes:
  a=by[n['row_id'],n['model']];c=cases[n['row_id']];q=c['request']
  assert sha_text(a['text'])==a['content_sha256']==n['candidate_sha256']
  assert sha_text(json.dumps(q,sort_keys=True,ensure_ascii=False))==n['request_sha256']
  assert n['human_approved'] is False and n['automatic_verdict'] is False
  for e in n['evidence']:
   assert e['claim_quote'] in a['text'] and any(e['source_quote'] in x for x in leaves(q))
 paired={r for r,c in cases.items() if len(c['answers'])==5};assert len(paired)==26
 summary=read(HERE/'local_replay/semantic_summary.json')
 for m in summary['balanced_per_model']:
  nn=[n for n in notes if n['row_id'] in paired and n['model']==m['model']];cc=Counter(n['verdict'] for n in nn)
  assert len(nn)==m['cases']==26
  for v in ['PASS','FAIL','UNCERTAIN']:assert cc[v]==m[v]
 for p in (HERE/'reproduce').glob('*.ipynb'):
  for c in read(p)['cells']:
   if c['cell_type']=='code':ast.parse(''.join(c['source']))
 print(json.dumps({'files_hash_verified':len(manifest['files']),'model_weights_included':False,'dataset_train_val':[810,90],
  'initial_learning_rate_both_runs':cfg1['learning_rate'],'recomputed_training_loss':counts,'local_raw_hash_bound_reviews':133,
  'fully_paired_local_cases':26,'Kaggle_T4_semantic_review_complete':False,'semantic_judgments_reapproved_by_this_script':False},ensure_ascii=False,indent=2))
def sha_text(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()
if __name__=='__main__':main()
