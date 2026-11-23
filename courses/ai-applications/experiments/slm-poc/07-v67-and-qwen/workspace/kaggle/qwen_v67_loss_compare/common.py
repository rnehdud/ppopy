"""Frozen candidate formatting and data handling; standard-library only."""
import hashlib
import json
from pathlib import Path
import random

SEED = 20261116
CANDIDATE_SEED = 1667
MODEL_ID = 'Qwen/Qwen3-Reranker-0.6B'
REVISION = 'e61197ed45024b0ed8a2d74b80b4d909f1255473'
WEIGHT_SHA = '27cd75a405b9c1b46b59abfd88aaa209e6fed2a1972cde9b70e7659537c5e65b'
INSTRUCTION = 'Given the complete state and user request, judge whether the proposed action and target are the appropriate next action. Do not invent facts or re-ask confirmed information.'
PREFIX = '<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
SUFFIX = '<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
QUESTION = '현재 상태와 사용자 발화를 읽고 지금 실행할 다음 행동 하나를 선택하세요. 확인되지 않은 사실을 확정하거나 이미 답한 내용을 다시 묻지 마세요.'
DESCRIPTIONS = {
    'ask_user':'판단에 필요한 미확인 정보를 사용자에게 질문한다.',
    'confirm_candidate':'추출된 후보의 본인 여부와 의미를 확인한다.',
    'retrieve_evidence':'제품 또는 규칙의 근거 자료를 조회한다.',
    'resolve_conflict':'서로 상충하는 관찰을 정리한다.',
    'hold':'필수 정보가 없거나 보류 신호가 있어 판단을 보류한다.',
    'request_draft':'필수 확인을 마친 뒤 사용법 초안 생성을 요청한다.'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()

def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))

def save(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)

def read_rows(path):
    return [json.loads(s) for s in Path(path).read_text(encoding='utf-8').splitlines() if s.strip()]

def prepare(row):
    # Gold, IDs, review, provenance and split metadata are not put in context.
    ctx=row['input']
    assert ctx['production_enabled'] is False
    candidates=[{k:o.get(k) for k in ['action','target_id','reviewed_text']}
                for o in ctx['available_actions'] if o['enabled']]
    pairs=[(c['action'],c['target_id']) for c in candidates]
    assert candidates and len(set(pairs))==len(pairs)
    rng=random.Random(CANDIDATE_SEED+int(hashlib.sha256(row['id'].encode()).hexdigest()[:8],16))
    rng.shuffle(candidates)
    context=json.dumps(ctx,ensure_ascii=False,separators=(',',':'))
    first_texts=[QUESTION+'\n사용자 발화: '+ctx['message']+'\n후보 행동: '+c['action']+' / 대상: '+c['target_id']+'\n'+DESCRIPTIONS[c['action']]+'\n'+(c['reviewed_text'] or '') for c in candidates]
    gold={k:row['output'][k] for k in ['action','target_id']}
    positive=[i for i,c in enumerate(candidates) if all(c[k]==gold[k] for k in gold)]
    assert len(positive)==1, 'Gold is not exactly one enabled candidate'
    return {'id':row['id'],'group_id':row['group_id'],'scenario_id':row['scenario_id'],
            'context':context,'candidates':candidates,'first_texts':first_texts,
            'gold':gold,'positive_index':positive[0]}

def encode(tokenizer, item, candidate_index):
    text=f'<Instruct>: {INSTRUCTION}\n<Query>: {item["first_texts"][candidate_index]}\n<Document>: {item["context"]}'
    return (tokenizer.encode(PREFIX,add_special_tokens=False)
            +tokenizer.encode(text,add_special_tokens=False,truncation=False)
            +tokenizer.encode(SUFFIX,add_special_tokens=False))

def epoch_plan(items, epoch):
    """One positive and one uniform negative per multi-candidate row/epoch.

    A single-candidate row contributes its positive once. Thus every train row
    appears; multi-candidate rows have balanced yes/no labels. Sampling uses
    train IDs only, not validation or current model scores.
    """
    rng=random.Random(SEED+epoch)
    plan=[]
    for row_index,item in enumerate(items):
        pos=item['positive_index'];plan.append((row_index,pos,1))
        neg=[i for i in range(len(item['candidates'])) if i!=pos]
        if neg:plan.append((row_index,rng.choice(neg),0))
    rng.shuffle(plan)
    return plan

def summarize(records, selected50):
    def part(rows):
        n=len(rows);correct=sum(r.get('pair_correct',False) for r in rows)
        return {'n':n,'correct':correct,'accuracy':correct/n if n else None,
                'action_correct':sum(r.get('action_correct',False) for r in rows),
                'errors':sum(bool(r.get('error')) for r in rows)}
    answer=part(records)
    answer['val_exceeds_90_percent']=answer['correct']*10>9*answer['n']
    answer['same_previous50']=part([r for r in records if r['id'] in selected50])
    answer['multiple_candidates']=part([r for r in records if r['candidate_n']>1])
    answer['by_gold_action']={a:part([r for r in records if r['gold']['action']==a])
                              for a in sorted({r['gold']['action'] for r in records})}
    return answer
