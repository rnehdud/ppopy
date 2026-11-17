"""Freeze a small KLUE-WoS teacher-forced state-tracking experiment.

No synthetic skin labels or tool calls are invented. State labels come solely
from the public KLUE corpus. Only the previous user-turn gold state and the
preceding system utterance are inputs; the current gold state is output only.
"""
import hashlib
import json
from pathlib import Path
import random
import sys
import pyarrow.parquet as pq
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from transformers import AutoTokenizer
from training.data import tokenize_example

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/processed/klue_wos_pilot_v1'
SEED=20261105


def state_map(values):
    result={}
    for value in values:
        parts=value.split('-',2)
        if len(parts)!=3:
            raise ValueError('Malformed source state')
        key='-'.join(parts[:2])
        if key in result and result[key]!=parts[2]:
            raise ValueError('Conflicting source state values')
        result[key]=parts[2]
    return dict(sorted(result.items()))


def make_examples(dialogue):
    prior={}
    system_text=''
    examples=[]
    for i,t in enumerate(dialogue['dialogue']):
        if t['role']=='sys':
            system_text=t['text']
            continue
        if t['role']!='user':
            raise ValueError('Unknown source role')
        current=state_map(t['state'])
        examples.append({'id':f'{dialogue["guid"]}-turn-{i}', 'dialogue_id':dialogue['guid'],
                         'previous_state':prior,'previous_system_utterance':system_text,
                         'user_utterance':t['text'],'target_state':current,
                         'state_changed':current!=prior})
        prior=current
    return examples


def make_messages(row,slots,with_target):
    system=('한국어 대화 상태 추적기다. 이전 상태, 직전 시스템 응답, 현재 사용자 발화를 읽고 '
            '현재 상태 전체를 JSON 객체 하나로 출력한다. 설명, 코드블록, 도구 호출은 출력하지 않는다. '
            '키는 허용 슬롯 이름, 값은 문자열이다. 이전 값을 유지하거나 정정할 수 있다. '
            '언급되지 않은 새 값은 추측하지 말고, 없는 슬롯은 생략한다. '
            '가능 슬롯: '+json.dumps(slots,ensure_ascii=False,separators=(',',':')))
    user=json.dumps({'이전_상태':row['previous_state'],'직전_시스템_응답':row['previous_system_utterance'],
                     '현재_사용자_발화':row['user_utterance']},ensure_ascii=False,sort_keys=True)
    msgs=[{'role':'system','content':system},{'role':'user','content':user}]
    if with_target:
        msgs.append({'role':'assistant','content':json.dumps(row['target_state'],ensure_ascii=False,sort_keys=True,separators=(',',':'))})
    return msgs


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    if OUT.exists():
        raise FileExistsError('Frozen experiment exists; do not overwrite')
    source=ROOT/'data/raw/klue_wos'
    train=pq.read_table(source/'train-00000-of-00001.parquet').to_pylist()
    validation=pq.read_table(source/'validation-00000-of-00001.parquet').to_pylist()
    ids_train={r['guid'] for r in train}; ids_val={r['guid'] for r in validation}
    if ids_train & ids_val:
        raise ValueError('Source splits overlap')
    slots=sorted({k for d in train for e in make_examples(d) for k in e['target_state']})
    rng=random.Random(SEED)
    rng.shuffle(train); rng.shuffle(validation)
    def choose(rows,count):
        selected=[]
        for dialogue in rows[:count]:
            candidates=make_examples(dialogue)
            if not candidates:
                raise ValueError('No user turns')
            selected.append(rng.choice(candidates))
        return selected
    # One user turn per distinct conversation; no split contamination.
    train_rows=choose(train,200)
    val_loss=choose(validation[:40],40)
    val_eval=choose(validation[40:100],60)
    if {x['dialogue_id'] for x in val_loss}&{x['dialogue_id'] for x in val_eval}:
        raise ValueError('Validation loss and evaluation dialogue overlap')
    tokenizer=AutoTokenizer.from_pretrained(str(ROOT/'models/qwen3-4b-instruct-2507/tokenizer'),local_files_only=True)
    lengths={}
    for name,rows in [('train',train_rows),('validation_loss',val_loss),('validation_eval',val_eval)]:
        lens=[]
        for row in rows:
            ex={'id':row['id'],'scenario_id':row['dialogue_id'],'category':'klue_wos',
                'messages':make_messages(row,slots,True),'tools':[]}
            item=tokenize_example(tokenizer,ex,max_length=2048)
            lens.append(item['total_tokens'])
        lengths[name]={'examples':len(rows),'max_tokens':max(lens)}
    OUT.mkdir(parents=True)
    (OUT/'slots.json').write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('train',train_rows),('validation_loss',val_loss),('validation_eval',val_eval)]:
        with (OUT/(name+'.jsonl')).open('w',encoding='utf-8',newline='\n') as f:
            for row in rows:
                f.write(json.dumps(row,ensure_ascii=False)+'\n')
    manifest={'source':'klue/klue wos','source_revision':'349481ec73fff722f88e0453ca05c77a447d967c',
              'source_license':'CC BY-SA 4.0','source_sha256':{'train':sha(source/'train-00000-of-00001.parquet'),
              'validation':sha(source/'validation-00000-of-00001.parquet')},
              'seed':SEED,'selection':'one randomly sampled user turn per conversation',
              'counts':lengths,'slots_count':len(slots),'teacher_forcing':True,
              'schema':'full state JSON; not skincare fields and not a tool call',
              'limits':['Synthetic model input/output derived from original dialogue state labels.',
                        'Validation loss and evaluation are disjoint by conversation.',
                        'No human semantic audit of transformed labels.']}
    manifest['files']={p.name:sha(p) for p in OUT.iterdir() if p.is_file()}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
