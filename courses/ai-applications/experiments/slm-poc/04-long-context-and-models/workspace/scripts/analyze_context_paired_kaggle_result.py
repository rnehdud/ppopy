"""Import final weights and analyse the Kaggle paired-context result archive."""
import collections,csv,hashlib,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=Path.home()/'Downloads/context-paired-kaggle-v2-results.zip'
INPUT=ROOT/'data/processed/context-paired-kaggle-v2/test.jsonl'
DEST=ROOT/'output/training/context-paired-kaggle-v2-import'
REPORT=ROOT/'output/context-paired-kaggle-v2-analysis.json'
CSV=ROOT/'output/context-paired-kaggle-v2-case-analysis.csv'

def main():
 if DEST.exists() or REPORT.exists() or CSV.exists():raise FileExistsError('Existing import protected.')
 source={r['id']:r for r in (json.loads(x) for x in INPUT.read_text(encoding='utf8').splitlines() if x.strip())}
 with zipfile.ZipFile(ARCHIVE) as z:
  if z.testzip() is not None:raise ValueError('corrupt ZIP')
  result=json.loads(z.read('results.json'));config=json.loads(z.read('run_config.json'))
  assert config['source_manifest_sha256']=='4cf5710c64b566e52915de5f16a78aff3fc7c360b27e439aa9fbccfb7c18e72c'
  final_files=['baseline.json','summary.json','results.json','run_config.json','test_predictions.csv']
  for arm in ('short_only','short_and_long'):
   final_files += [arm+'/final/adapter/adapter_config.json',arm+'/final/adapter/adapter_model.safetensors',arm+'/final/training_state.pt']
  DEST.mkdir(parents=True)
  for name in final_files:
   out=DEST/name;out.parent.mkdir(parents=True,exist_ok=True)
   with z.open(name) as src,out.open('wb') as dst:
    while chunk:=src.read(1024*1024):dst.write(chunk)
 arms=('baseline','short_only','short_and_long');entries={}
 for arm in arms:
  rows=result[arm]['test']['rows'];assert len(rows)==120
  for r in rows:
   src=source[r['id']]
   assert src['target']==r['expected'] and src['group']==r['group'] and src['input']==r['input']
   key=(r['id'],r['variant']);assert (arm,key) not in entries
   entries[(arm,key)]=r
 cases=[]
 for id,src in source.items():
  d={'id':id,'user_input':src['input'],'source_context':src['short_context'],'options':src['options'],
     'expected':src['target'],'filler_placement':src['filler_placement']}
  for variant in ('short','long'):
   for arm in arms:
    r=entries[(arm,(id,variant))];d[f'{arm}_{variant}']=r['predicted'];d[f'{arm}_{variant}_match']=r['match']
  cases.append(d)
 a=collections.Counter();b=collections.Counter();c=collections.Counter()
 for r in cases:
  prev=r['baseline_long'];new=r['short_and_long_long'];gold=r['expected']
  label='no_tool' if gold=='no_tool' else 'call'
  a[(label,'baseline_right' if prev==gold else 'baseline_wrong','mixed_right' if new==gold else 'mixed_wrong')]+=1
  b[(label,'no_tool' if prev=='no_tool' else 'tool','no_tool' if new=='no_tool' else 'tool')]+=1
  c[(label,prev,new)]+=1
 summary={'archive_sha256':hashlib.file_digest(ARCHIVE.open('rb'),'sha256').hexdigest(),
  'outcome_transitions':{' | '.join(k):v for k,v in sorted(a.items())},
  'predicted_call_transitions':{' | '.join(k):v for k,v in sorted(b.items())},
  'most_common_prediction_changes':[{'expected_type':k[0],'from':k[1],'to':k[2],'n':v} for k,v in c.most_common()],
  'warnings':'Synthetic source labels not human verified; short and long split groups were previously observed in project; long filler is artificial.'}
 REPORT.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
 fields=['id','user_input','expected','filler_placement']+[f'{arm}_{v}' for v in ('short','long') for arm in arms]+['source_context','options']
 with CSV.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in cases:w.writerow({k:(json.dumps(r[k],ensure_ascii=False) if k=='options' else r[k]) for k in fields})
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
 print('saved',DEST,REPORT,CSV,flush=True)
if __name__=='__main__':main()
