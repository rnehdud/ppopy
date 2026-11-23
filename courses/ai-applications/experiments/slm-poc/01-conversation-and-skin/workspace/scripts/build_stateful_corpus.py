"""Create and freeze controlled Korean stateful train/validation/holdout data.

Labels come from explicitly authored scenario parameters, not predictions, regex
extraction, or the evaluated model. Trajectories are replayed through real tools.
This is synthetic, template-disjoint evaluation, not independently collected speech.
"""
import copy
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.runtime import Agent,EMPTY_STATE,SYSTEM,TOOLS

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'v2'
DEST = ROOT/'data/stateful'/VERSION
SEED = 20261104
CATEGORIES = ['report','conflicting_events','change_time','change_onset','negation','no_product',
              'missing_information','remove_symptom','search','failed_search','greeting','clarify']
WORDS = {
    'dryness':('피부가 건조해','피부가 건조하지 않아'),
    'stinging':('피부가 따가워','피부가 따갑지는 않아'),
    'itching':('피부가 가려워','피부가 가렵지는 않아'),
    'redness':('피부가 붉어','피부가 붉지는 않아'),
    'breakout':('뾰루지가 생겼어','뾰루지는 없어'),
}
TIMES={'morning':'아침','afternoon':'오후','evening':'저녁'}
DAYS={'today':'오늘','yesterday':'어제','recent':'최근'}
LEVELS={'mild':'경미함','moderate':'중등도','severe':'심함'}
STYLES={
 'train':{
  'report':'{positive}. 증상은 {day} 시작됐어. 제품은 {time}에 사용했어. 정도는 {level}으로 기록해줘.',
  'conflicting_events':'제품은 어제 {time}에 발랐지만 {event} 건 오늘이야.',
  'change_time':'제품 사용 시간은 {old_time}이 아니라 {time}이야. 다른 정보는 그대로 둬.',
  'change_onset':'증상이 시작된 날을 정정할게. {day} 시작됐어. 제품 사용 시간은 바꾸지 마.',
  'negation':'{negative}. 실제로 {positive}. 사용 시점이나 증상 시작일은 말하지 않을게.',
  'no_product':'오늘 {positive}. 화장품은 전혀 안 썼어.',
  'missing_information':'{positive}. 제품 사용 여부, 시점, 증상 시작일은 아직 말하지 않을게.',
  'remove_symptom':'{negative}. "{other_positive}"라는 증상만 남겨줘. 사용 시간은 유지해줘.',
  'search':'현재 기록된 상태로 문서를 검색하고 제목과 문서 ID를 알려줘.',
  'failed_search':'현재 저장된 상태에 관한 자료를 조회하고 문서 ID를 알려줘.',
  'greeting':'안녕하세요. 지금은 인사만 할게요.',
  'clarify':'그걸로 찾아줘. 무엇을 뜻하는지는 아직 말하지 않을게.',
 },
 'validation':{
  'report':'기록 부탁해. {positive}. 시작일은 {day}, 화장품은 {time} 사용, 강도는 {level}이야.',
  'conflicting_events':'어제 {time} 제품을 사용했고, 오늘부터 {positive}. 두 시점을 구분해서 적어줘.',
  'change_time':'사용한 시간대만 고칠게. {old_time} 기록은 취소하고 {time}에 사용했다고 적어줘.',
  'change_onset':'시작 시점만 고쳐줘. 증상은 {day} 시작됐어.',
  'negation':'{positive}. 하지만 {negative}. 나머지 정보는 모르는 상태로 둬.',
  'no_product':'화장품을 바른 적은 없어. 오늘 {positive}.',
  'missing_information':'현재 증상으로 "{positive}"라는 것만 추가해줘.',
  'remove_symptom':'기록에서 그 증상은 지워줘. {negative}. "{other_positive}"라는 말은 맞아.',
  'search':'저장된 최신 조건으로 조회해줘. 검색된 자료의 식별자도 적어줘.',
  'failed_search':'기록된 조건에 맞는 문서를 조회해서 출처 번호를 보여줘.',
  'greeting':'반갑습니다. 상태 변경이나 조회는 필요 없어요.',
  'clarify':'그 상태라는 말을 썼지만 증상 설명은 아직 하지 않았어. 뭘 찾을지 먼저 확인해줘.',
 },
 'holdout':{
  'report':'메모를 새로 남겨줘. {positive}. 발생은 {day}이고, 바른 시간대는 {time}, 정도 표시는 {level}이야.',
  'conflicting_events':'{time}에 제품을 바른 건 어제의 일이야. {event} 건 오늘이고.',
  'change_time':'바른 시각만 정정해줘. {old_time} 기록은 틀렸어. 실제로는 {time}에 발랐어.',
  'change_onset':'사용 시각은 그대로야. 증상이 발생한 날만 바로잡아줘. {day} 시작됐어.',
  'negation':'증상을 구별해서 적어줘. {negative}. "{positive}"라는 게 맞아. 날짜나 제품 이야기는 하지 않았어.',
  'no_product':'화장품 사용은 없었다고 적어줘. {event} 건 오늘이야.',
  'missing_information':'제품을 썼는지나 언제부터인지는 말한 적 없어. "{positive}"라는 점만 기억해줘.',
  'remove_symptom':'다른 항목은 건드리지 마. {negative}. "{other_positive}"라는 것만 증상 목록에 남겨줘.',
  'search':'최신 상태를 조건으로 자료를 찾아봐 줘. 반환된 문서 이름과 ID까지 보여줘.',
  'failed_search':'지금 기록을 기준으로 문서를 찾아서 그 식별자를 답해줘.',
  'greeting':'만나서 반가워요. 오늘은 인사만 하고 갈게요.',
  'clarify':'이것에 대한 자료를 부탁해. 아직 무슨 피부 증상인지는 설명하지 않았어.',
 },
}


def sha(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def seed_state(i):
    kinds=list(WORDS)
    return {'skin_condition':[kinds[i%5]],'usage_time':list(TIMES)[(i//5)%3],
            'product_used':'yes',
            'symptom_onset':['today','yesterday','recent','unknown'][(i//3)%4],
            'severity':['unknown','mild','moderate','severe'][(i//7)%4]}


def make_case(split,category,i):
    kinds=list(WORDS)
    offset={'train':0,'validation':41,'holdout':83}[split]
    j=i+offset
    symptom=kinds[j%5]
    other=kinds[(j+2)%5]
    time=list(TIMES)[(j//5+j)%3]
    old_time=list(TIMES)[(list(TIMES).index(time)+1)%3]
    day=list(DAYS)[(j//2+j)%3]
    level=list(LEVELS)[j%3]
    params={'positive':WORDS[symptom][0],'negative':WORDS[other][1],
            'other_positive':WORDS[symptom][0],'time':TIMES[time],'old_time':TIMES[old_time],
            'day':DAYS[day],'level':LEVELS[level],
            'event':{'dryness':'건조함이 생기기 시작한','stinging':'따가움이 생기기 시작한',
                     'itching':'가려움이 생기기 시작한','redness':'붉어짐이 생기기 시작한','breakout':'뾰루지가 생기기 시작한'}[symptom]}
    initial=copy.deepcopy(EMPTY_STATE)
    patch=None
    if category=='report':
        patch={'skin_condition':[symptom],'usage_time':time,'product_used':'yes','symptom_onset':day,'severity':level}
    elif category=='conflicting_events':
        patch={'skin_condition':[symptom],'usage_time':time,'product_used':'yes','symptom_onset':'today'}
    elif category=='change_time':
        initial=seed_state(j)
        initial['usage_time']=old_time
        patch={'usage_time':time}
    elif category=='change_onset':
        initial=seed_state(j)
        initial['symptom_onset']=next(d for d in ['today','yesterday','recent'] if d!=day)
        patch={'symptom_onset':day}
    elif category=='negation':
        patch={'skin_condition':[symptom]}
    elif category=='no_product':
        patch={'skin_condition':[symptom],'product_used':'no','symptom_onset':'today'}
    elif category=='missing_information':
        patch={'skin_condition':[symptom]}
    elif category=='remove_symptom':
        initial=seed_state(j)
        initial['skin_condition']=sorted([symptom,other])
        patch={'skin_condition':[symptom]}
    elif category in {'search','failed_search','greeting','clarify'}:
        initial=seed_state(j)
        if category=='clarify':
            initial['skin_condition']=[]
    utterance=STYLES[split][category].format(**params)
    result_state={**copy.deepcopy(initial),**copy.deepcopy(patch or {})}
    result_state['skin_condition']=sorted(result_state['skin_condition'])
    step={'input':utterance,'expected':result_state}
    if patch is not None:
        step['oracle_actions']=[{'name':'update_session_state','arguments':{'patch':patch}}]
        step['required_tool']='update_session_state'
        step['final_response']='기록을 반영했습니다.'
    elif category in {'search','failed_search'}:
        step['oracle_actions']=[{'name':'search_knowledge_base','arguments':{
            'query':'현재 상태 문서 조회','skin_condition':initial['skin_condition'],'usage_time':initial['usage_time']}}]
        step['required_tool']='search_knowledge_base'
        step['search_arguments']={'skin_condition':initial['skin_condition'],'usage_time':initial['usage_time']}
    else:
        step['oracle_actions']=[]
        step['no_tools']=True
        step['final_response']='안녕하세요.' if category=='greeting' else '어떤 피부 증상을 조회할까요?'
    steps=[step]
    # Make registration/correction -> query a genuine multi-turn stateful trajectory.
    if category in {'report','conflicting_events','change_time','change_onset','remove_symptom'}:
        steps.append({'input':STYLES[split]['search'], 'expected':copy.deepcopy(result_state),
                      'required_tool':'search_knowledge_base',
                      'search_arguments':{'skin_condition':result_state['skin_condition'],'usage_time':result_state['usage_time']},
                      'oracle_actions':[{'name':'search_knowledge_base','arguments':{
                          'query':'기록된 상태 문서 조회','skin_condition':result_state['skin_condition'],'usage_time':result_state['usage_time']}}]})
    case={'id':f'{split}-{category}-{i:03d}','category':category,'split':split,
          'surface_template_family':f'{split}/{category}',
          'initial':initial,'fail_search':category=='failed_search','turns':steps,
          'provenance':'parameterized synthetic scenario authored for this experiment, not human collected'}
    return case


def compile_case(case,folder):
    agent=Agent(Path(folder)/f'{case["id"]}.jsonl',initial=case['initial'],fail_search=case['fail_search'])
    examples=[]
    for turn_index,step in enumerate(case['turns']):
        history=[{'role':'user','content':step['input']}]
        def example(target):
            system=SYSTEM.replace('{state}',json.dumps({'version':agent.session.version,**agent.session.state},ensure_ascii=False))
            examples.append({'id':f'{case["id"]}-t{turn_index}-d{len(examples)}',
                             'scenario_id':case['id'],'split':case['split'],'category':case['category'],
                             'surface_template_family':case['surface_template_family'],
                             'messages':[{'role':'system','content':system}]+copy.deepcopy(history)+[copy.deepcopy(target)],
                             'tools':copy.deepcopy(TOOLS),'loss_target':'last_assistant_only'})
        last_result=None
        for action_index,action in enumerate(step['oracle_actions']):
            callid=f'call_{case["id"]}_{turn_index}_{action_index}'
            target={'role':'assistant','content':'','tool_calls':[{'id':callid,'type':'function','function':copy.deepcopy(action)}]}
            example(target)
            history.append(target)
            actual=agent._execute(action['name'],copy.deepcopy(action['arguments']))
            if action['name']=='update_session_state' and not actual.get('ok'):
                raise ValueError(f'Invalid oracle patch: {case["id"]}: {actual}')
            if action['name']=='search_knowledge_base':
                if case['fail_search']:
                    assert not actual['ok']
                    step['expect_search_failure']=True
                    step['final_response']='조회 도구 오류로 문서를 가져오지 못했습니다.'
                elif actual['documents']:
                    document=actual['documents'][0]
                    step['document_id']=document['id']
                    step['final_response']=f'조회 문서: {document["title"]}. 출처: {document["id"]}'
                else:
                    step['final_response']='현재 조건에 해당하는 모의 문서가 없습니다.'
            history.append({'role':'tool','tool_call_id':callid,'name':action['name'],
                            'content':json.dumps(actual,ensure_ascii=False)})
            last_result=actual
        assert agent.session.state==step['expected'], (case['id'],agent.session.state,step['expected'])
        target={'role':'assistant','content':step['final_response']}
        example(target)
    return examples


def main():
    if DEST.exists():
        raise SystemExit(f'{DEST} already exists. Frozen data is not overwritten. Use a new version directory for changes.')
    split_cases={}
    for split in ['train','validation','holdout']:
        cases=[]
        for n,category in enumerate(CATEGORIES):
            count=25 if split=='train' else (3 if n<6 else 2) if split=='validation' else 5
            cases.extend(make_case(split,category,i) for i in range(count))
        random.Random(SEED).shuffle(cases)
        split_cases[split]=cases
    all_rows={}
    draft_counts={s:len(v) for s,v in split_cases.items()}
    for split,cases in split_cases.items():
        seen=set()
        unique=[]
        for case in cases:
            signature=sha({'initial':case['initial'],'fail_search':case['fail_search'],
                           'turns':[{k:v for k,v in t.items() if k!='final_response'} for t in case['turns']]})
            if signature not in seen:
                seen.add(signature)
                unique.append(case)
        split_cases[split]=unique
    with tempfile.TemporaryDirectory(prefix='stateful-oracle-') as folder:
        for split,cases in split_cases.items():
            all_rows[split]=[row for case in cases for row in compile_case(case,folder)]
    # Reject surface-text leakage between train, validation and evaluation.
    utterances={s:{t['input'] for c in cs for t in c['turns']} for s,cs in split_cases.items()}
    for a,b in [('train','validation'),('train','holdout'),('validation','holdout')]:
        overlap=utterances[a]&utterances[b]
        if overlap:
            raise ValueError(f'Cross-split utterance overlap {a}/{b}: {overlap}')
    duplicate_decisions={}
    for split,rows in all_rows.items():
        seen=set()
        unique=[]
        for row in rows:
            messages=copy.deepcopy(row['messages'])
            for message in messages:
                message.pop('tool_call_id',None)
                for call in message.get('tool_calls',[]):
                    call.pop('id',None)
            signature=sha({'messages':messages,'tools':row['tools']})
            if signature not in seen:
                seen.add(signature)
                unique.append(row)
        duplicate_decisions[split]=len(rows)-len(unique)
        all_rows[split]=unique
    DEST.mkdir(parents=True)
    files={}
    for split in split_cases:
        for suffix,value in [('cases.json',split_cases[split]),('sft.jsonl',all_rows[split])]:
            path=DEST/f'{split}.{suffix}'
            text=json.dumps(value,ensure_ascii=False,indent=2)+'\n' if suffix.endswith('json') else ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in value)
            path.write_text(text,encoding='utf-8')
            files[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    metadata={'version':VERSION,'seed':SEED,'synthetic':True,'human_collected':False,
              'supersedes':'v1 (pre-training author review: grammar and consistency of seeded product-use state)',
              'draft_scenarios':draft_counts,'duplicate_decisions_removed':duplicate_decisions,
              'counts':{s:{'scenarios':len(split_cases[s]),'decision_examples':len(all_rows[s]),
                           'turns':sum(len(c['turns']) for c in split_cases[s])} for s in split_cases},
              'freeze_policy':'Holdout created before model training; do not use for prompt tuning/checkpoint selection.',
              'separation':'Disjoint authored surface template families and no exact user-utterance overlap. Semantic categories are shared.',
              'validation':'Every oracle action executed against the actual Session/tool implementation; full state checked after each turn.',
              'limitations':['Structural/execution validation does not replace independent human semantic review.',
                             'Synthetic controlled language, not real speech or broad Korean generalization.',
                             'Tool documents are synthetic and fixed, not clinical evidence.'],
              'runtime_sha256':hashlib.sha256((ROOT/'agent/runtime.py').read_bytes()).hexdigest(),
              'system_and_tools_sha256':sha({'system':SYSTEM,'tools':TOOLS}), 'files':files}
    (DEST/'manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(metadata,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
