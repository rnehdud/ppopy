"""Create a frozen, local-only 2k/2k/1k+1k comparison set.

SNS: one authentic adjacent turn pair per two-speaker beauty conversation.
Skin: the published question and answer, excluding image-dependent examples.
Neither set is represented as state or tool-call labels. No images, speaker
metadata, structured CoT, or fabricated labels enter the training examples.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from transformers import AutoTokenizer
from training.data import tokenize_example

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/raw/aihub'
DEST=ROOT/'data/processed/aihub_ablation_v1'
TOKENIZER=ROOT/'models/qwen3-4b-instruct-2507/tokenizer'
SEED=20261105
MAX_LENGTH=2048
SYSTEM='당신은 한국어 대화 도우미입니다. 사용자의 말에 알맞게 응답하세요.'
IMAGE_FILTER=re.compile(r'사진|이미지|영상|촬영|화면|이미징')
SENSITIVE_SLOT={'인물','연락처'}


def key(seed,value): return hashlib.sha256(f'{seed}:{value}'.encode('utf-8')).hexdigest()
def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def messages(row,target=True):
    result=[{'role':'system','content':SYSTEM},{'role':'user','content':row['user']}]
    if target:result.append({'role':'assistant','content':row['assistant']})
    return result


def parse_sources():
    sns=next(p for p in SOURCE.iterdir() if p.name.startswith('012.'))
    skin=next(p for p in SOURCE.iterdir() if p.name.startswith('03.'))
    result={'sns':{'train':[],'validation':[]},'skin':{'train':[],'validation':[]}}
    archives=[]
    for kind,dataset in [('sns',sns),('skin',skin)]:
        for zpath in sorted(dataset.rglob('*.zip')):
            if not zpath.name.startswith(('TL_','VL_')):continue
            split='train' if zpath.name.startswith('TL_') else 'validation'
            if kind=='sns' and '4.' not in zpath.name:continue
            archives.append({'path':str(zpath.relative_to(ROOT)),'sha256':digest(zpath),'size':zpath.stat().st_size})
            with zipfile.ZipFile(zpath) as z:
                for name in sorted(z.namelist()):
                    if not name.endswith(('.json','.jsonl')):continue
                    txt=z.read(name).decode('utf-8-sig')
                    obj=json.loads(txt if name.endswith('.json') else txt.splitlines()[0])
                    if kind=='sns':
                        utterances=obj.get('utterances',[])
                        if len({v.get('speaker') for v in utterances if v.get('speaker')})!=2:continue
                        pairs=[]
                        for i in range(1,len(utterances)):
                            a,b=utterances[i-1],utterances[i]
                            if a.get('speaker')==b.get('speaker') or not a.get('text') or not b.get('text'):continue
                            if any(s.get('key') in SENSITIVE_SLOT for t in [a,b] for s in (t.get('slot') or [])):continue
                            pairs.append(i)
                        if not pairs:continue
                        source_id=obj['info']['id']
                        index=pairs[int(key(SEED,source_id),16)%len(pairs)]
                        user=utterances[index-1]['text'];assistant=utterances[index]['text']
                    else:
                        info=obj.get('info',{});user=info.get('question','');assistant=info.get('answer','')
                        if not user or not assistant or IMAGE_FILTER.search(user+' '+assistant):continue
                        source_id=info.get('source_survey_id') or info.get('id')
                        if not source_id:raise ValueError('Missing skin source identity')
                    if not isinstance(user,str) or not isinstance(assistant,str):raise ValueError('Non-string text')
                    result[kind][split].append({'id':kind+'-'+split+'-'+str(source_id),
                              'source_id':str(source_id),'source_archive':str(zpath.relative_to(ROOT)),
                              'member':name,'user':user,'assistant':assistant})
    return result,archives


def main():
    if DEST.exists():raise FileExistsError('Frozen data exists; do not overwrite')
    sources,archives=parse_sources()
    tokenizer=AutoTokenizer.from_pretrained(str(TOKENIZER),local_files_only=True)
    chosen={};stats={}
    for kind in ['sns','skin']:
        selected_ids={}
        for split,needed in [('train',2000),('validation',40)]:
            candidates=sources[kind][split]
            candidates.sort(key=lambda r:key(SEED,r['id']))
            selected=[];seen=set();skip=Counter();lengths=[]
            for row in candidates:
                if row['source_id'] in seen:skip['duplicate_source_id']+=1;continue
                ex={'id':row['id'],'scenario_id':row['source_id'],'category':kind,
                    'messages':messages(row),'tools':[]}
                try: tokens=tokenize_example(tokenizer,ex,max_length=MAX_LENGTH)
                except ValueError as e:
                    if 'too long' in str(e):skip['overlength']+=1;continue
                    raise
                row['token_count']=tokens['total_tokens'];row['target_tokens']=tokens['target_tokens']
                selected.append(row);seen.add(row['source_id']);lengths.append(tokens['total_tokens'])
                if len(selected)==needed:break
            if len(selected)!=needed:raise ValueError(f'Insufficient {kind}/{split} rows: {len(selected)}/{needed}')
            selected_ids[split]=seen;chosen[(kind,split)]=selected
            stats[kind+'_'+split]={'available':len(candidates),'selected':len(selected),'skipped':dict(skip),
                    'tokens_total':sum(lengths),'tokens_mean':sum(lengths)/len(lengths),'tokens_max':max(lengths),
                    'target_tokens_total':sum(r['target_tokens'] for r in selected)}
        if selected_ids['train'] & selected_ids['validation']:
            raise ValueError(f'{kind} train and validation share source IDs')
    # The combined condition reuses exact halves of the two single-source sets.
    conditions={'sns_only':chosen['sns','train'],'skin_only':chosen['skin','train'],
                'mixed':chosen['sns','train'][:1000]+chosen['skin','train'][:1000]}
    DEST.mkdir(parents=True)
    for name,rows in conditions.items():
        with (DEST/(name+'.jsonl')).open('w',encoding='utf-8',newline='\n') as f:
            for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
        stats[name+'_condition']={'examples':len(rows),'sources':dict(Counter(r['id'].split('-')[0] for r in rows)),
                                  'tokens_total':sum(r['token_count'] for r in rows),
                                  'target_tokens_total':sum(r['target_tokens'] for r in rows)}
    for kind in ['sns','skin']:
        with (DEST/(kind+'_validation.jsonl')).open('w',encoding='utf-8',newline='\n') as f:
            for row in chosen[kind,'validation']:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    manifest={'seed':SEED,'max_length':MAX_LENGTH,'unit':'one user-to-assistant response pair per source conversation/record',
              'dataset':'AI Hub; local use only; follow source usage terms','archives':archives,'stats':stats,
              'selection':'source-level disjoint split; deterministic sha-based sampling; common 1000-row subsets',
              'preprocessing':['SNS: beauty/fashion two-speaker, one real adjacent speaker change, exclude person/contact slots.',
                               'Skin: use original question and answer only; exclude explicit image references.',
                               'Skip instead of truncating >2048-token examples.',
                               'No image files, demographics metadata, structured CoT, synthesized skin state, or tool-call labels.'],
              'limitations':['Answers may contain demographic details in the text; data remains local.',
                             'Tasks and target lengths differ; result is not a controlled comparison of domain content alone.',
                             'SNS utterance slot annotations and skincare metadata are not the Agent state gold labels.']}
    manifest['files']={p.name:digest(p) for p in DEST.iterdir() if p.is_file()}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
