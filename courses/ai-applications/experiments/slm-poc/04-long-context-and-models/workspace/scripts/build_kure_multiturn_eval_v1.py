"""Find held-out verified kotraj multi-turn decisions, preserving full history.

The baseline training split was hash-partitioned by group; use its test bucket
and exclude groups from previous 120-item and paired-context evaluations.
Source is synthetic; source next-action labels are not human-verified.
"""
import collections,hashlib,json,random,sys
from pathlib import Path
import pyarrow.parquet as pq
from transformers import AutoTokenizer

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/raw/kotraj-v02/train-00000-of-00001.parquet'
OUT=ROOT/'data/processed/kure-multiturn-heldout-v1'
OLD=ROOT/'output/training/kotraj-kaggle-complete-v1/kotraj_choice/kotraj-choice-full-gpu-v1/after.json'
QUESTION='사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.'
NO_TOOL='지금은 도구를 호출하지 않고 사용자에게 직접 답하거나 필요한 정보를 확인한다.'

def main():
 if OUT.exists():raise FileExistsError(OUT)
 expected='e2ce7225896347da30c297f7d7de5219f4447272590a9c890778543b54b6f0eb'
 with SRC.open('rb') as f:
  if hashlib.file_digest(f,'sha256').hexdigest()!=expected:raise ValueError('source mismatch')
 source=pq.read_table(SRC,columns=['id','pair_id','domain','verify_status','tools','messages']).to_pylist()
 group_by_id={r['id']:r.get('pair_id') or r['id'] for r in source}
 prev=json.loads(OLD.read_text(encoding='utf8'))
 excluded=set()
 for part in ('new_test','previous_test'):
  for r in prev[part]['rows']:
   source_id=r['id'].rsplit(':',1)[0]
   if source_id in group_by_id:excluded.add(group_by_id[source_id])
 for split in ('train','dev','test'):
  f=ROOT/'data/processed/kotraj-200-v1'/f'{split}.jsonl'
  for line in f.read_text(encoding='utf8').splitlines():
   if line.strip():excluded.add(json.loads(line)['group'])
 tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True);tok.model_max_length=1000000
 rng=random.Random(147321);rng.shuffle(source);seen=set();counts=collections.Counter();fits=[];longs=[]
 for row in source:
  group=row.get('pair_id') or row['id'];bucket=int(hashlib.sha256(('kotraj-2026:'+group).encode()).hexdigest()[:8],16)%100
  if bucket>=10 or row.get('verify_status')!='verified':continue
  if group in excluded or group in seen:continue
  try:
   tools=json.loads(row['tools']);messages=json.loads(row['messages'])
   options={t['function']['name']:t['function'].get('description','').strip()+' 필수 인자: '+json.dumps(t['function'].get('parameters',{}).get('required',[]),ensure_ascii=False) for t in tools}
   assert len(options)==len(tools) and len(options)>1 and 'no_tool' not in options
  except (ValueError,KeyError,TypeError,AssertionError):counts['malformed']+=1;continue
  options['no_tool']=NO_TOOL
  positions=[i for i,m in enumerate(messages[:-1]) if m.get('role')=='user' and messages[i+1].get('role')=='assistant' and sum(x.get('role')=='user' for x in messages[:i])>=1]
  rng.shuffle(positions)
  for i in positions:
   calls=messages[i+1].get('tool_calls') or []
   if len(calls)>1:counts['parallel_excluded']+=1;continue
   target=calls[0].get('function',{}).get('name') if calls else 'no_tool'
   if target not in options:counts['target_not_in_tools']+=1;continue
   text=messages[i].get('content')
   if not isinstance(text,str) or not text.strip():continue
   prior=messages[:i]
   if not any(x.get('role')=='system' for x in prior):counts['no_system']+=1;continue
   context='대화:\n'+json.dumps(prior,ensure_ascii=False)+'\n이번 사용자 발화: '+text
   longest=max(options.values(),key=lambda x:len(tok(QUESTION+' '+x,add_special_tokens=False)['input_ids']))
   n=len(tok(QUESTION+' '+longest,context,truncation=False)['input_ids'])
   if n>2048:counts['over_2048_excluded']+=1;continue
   item={'id':row['id']+':'+str(i),'source_id':row['id'],'group':group,'domain':row['domain'],
    'verify_status':row['verify_status'],'history':prior,'input':text,'options':options,'target':target,'full_tokens':n,
    'label_provenance':'verified synthetic source next action; independent human review pending'}
   (fits if n<=512 else longs).append(item);seen.add(group);counts['accepted']+=1
   break
 rng.shuffle(fits);rng.shuffle(longs)
 OUT.mkdir(parents=True)
 for name,values in [('fits512',fits),('over512',longs)]:
  (OUT/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in values),encoding='utf8')
 stats={'seed':147321,'source_sha256':expected,'verified_only':True,'test_bucket':'sha256(kotraj-2026:group) %100 < 10',
  'excluded_groups_previously_observed':len(excluded),'counts':dict(counts),
  'fits512':{'n':len(fits),'call':sum(x['target']!='no_tool' for x in fits),'no_tool':sum(x['target']=='no_tool' for x in fits)},
  'over512':{'n':len(longs),'call':sum(x['target']!='no_tool' for x in longs),'no_tool':sum(x['target']=='no_tool' for x in longs)},
  'caution':'Previously unused source groups according to recorded exclusion, but source patterns, tool catalog, and synthetic generation may overlap; labels not independently verified.'}
 (OUT/'manifest.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(stats,ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':main()
