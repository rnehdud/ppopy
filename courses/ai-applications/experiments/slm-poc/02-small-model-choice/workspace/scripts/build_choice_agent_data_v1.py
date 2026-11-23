"""Question-conditioned, multi-option synthetic training/evaluation set.

Tool labels are authored rules, not model predictions or human-reviewed gold.
Raw AI Hub data is never read. A local symptom set is sampled for retention.
"""
import hashlib,json,random,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.choice_agent_v1 import TOOL_DESCRIPTIONS,TOOL_QUESTION,SYMPTOM_DESCRIPTIONS,SYMPTOM_QUESTION,NAMES
from agent.symptom_state_v1 import SYMPTOMS,empty_state
from scripts.analyze_symptom_score_margins_v1 import authored_cases

DEST=ROOT/'data/processed/choice_agent_v2'
SOURCE=ROOT/'data/processed/ko_symptom_6000_v2/train.jsonl'
TOOL_TRAIN={
 'record':['제 피부가 건조해요. 증상을 기록해 주세요.','제 얼굴이 가려워요. 피부 상태를 저장해 주세요.',
           '뺨이 빨갛습니다. 제 기록을 갱신해 주세요.','여드름이 없다고 제 상태에 적어 주세요.',
           '피부가 따갑다는 내용을 제 기록에 남겨 주세요.','가려운 증상을 지금 상태에 추가해 주세요.'],
 'search':['보습에 관한 정보를 지식베이스에서 검색해 주세요.','피부 진정 성분을 자료에서 찾아 주세요.',
           '스킨케어 성분 정보를 찾아봐 주세요.','건조한 피부에 대한 자료를 검색해 주세요.',
           '피부 관리 성분 정보를 조회해 주세요.','보습 성분이 무엇인지 자료를 찾아 주세요.'],
 'show':['저장된 제 피부 기록을 보여 주세요.','제 현재 상태를 확인해 주세요.',
         '지금까지 기록한 증상을 알려 주세요.','내 피부 상태 기록을 보여 줘요.',
         '제 증상 기록을 확인하고 싶어요.','제 현재 기록을 읽어 주세요.'],
 'ask':['이거 좀 해 주세요.','그거 어떻게 하면 좋을까요?','좀 도와주세요.',
        '그걸 바꿔 주시겠어요?','이렇게 하면 될까요?','제가 뭘 해야 할까요?'],
 'none':['안녕하세요.','오늘은 기분이 좋네요.','반갑습니다.','좋은 하루 보내세요.',
         '저는 차를 마시고 있어요.','오늘은 날씨가 맑네요.']}
TAILS=['',' 오늘은 월요일이에요.',' 조금 전에 집에 왔어요.',' 오늘은 바빴어요.',
       ' 내일은 쉬어요.',' 잠시 이야기하고 싶어요.',' 평소에 산책을 합니다.',
       ' 점심을 먹었어요.',' 나중에 다시 올게요.',' 지금 시간이 있어요.']
TOOL_QUESTIONS=[TOOL_QUESTION,'사용자 요청에 맞는 실행 동작을 하나 고르세요.',
                '이 발화에 대해 어떤 기능을 실행해야 하나요?',
                '현재 사용할 도구를 선택하세요.']
STATE_QUESTIONS=[SYMPTOM_QUESTION,'이 증상에 대한 기록을 어떻게 바꿔야 하나요?',
                 '사용자 발화에 맞는 대상 증상의 상태 변경을 고르세요.',
                 '현재 문장에서 이 증상의 업데이트 결과를 선택하세요.']
DEV_TOOL=[
 ('제 피부가 빨개요. 기록해 주세요.','record'),('가려운 증상을 저장해 줘요.','record'),
 ('진정 성분을 지식 자료에서 찾아줘요.','search'),('보습에 대한 자료를 검색해요.','search'),
 ('지금 제 기록을 알려 주세요.','show'),('기록한 상태를 보여줘요.','show'),
 ('이거 어떻게 하죠?','ask'),('뭔가 해줘요.','ask'),('안녕하세요 반가워요.','none'),('오늘 점심은 맛있었어요.','none')]
TEST_TOOL=[
 ('지금 제 얼굴이 건조한 걸 적어 주세요.','record'),('피부가 가려우니 기록을 남겨 주세요.','record'),
 ('뾰루지가 없다고 제 상태에 써 주세요.','record'),('제 얼굴이 따가운 상태를 저장해 주세요.','record'),
 ('피부 진정에 쓰이는 성분을 자료에서 검색해 줘요.','search'),('건조한 피부 관리에 관한 문서를 찾아봐 주세요.','search'),
 ('보습 성분에 대해 지식베이스를 조회해 주세요.','search'),('스킨케어 원료 관련 정보를 자료에서 찾아 줘요.','search'),
 ('지금까지 남긴 제 증상 목록을 볼 수 있을까요?','show'),('제가 기록해 둔 피부 상태를 보여 주세요.','show'),
 ('현재 저장된 증상 정보를 알려주세요.','show'),('내 기록은 지금 어떻게 돼 있나요?','show'),
 ('그거 해줘.','ask'),('이거 좀 바꾸고 싶은데요.','ask'),('어떻게 해야 할까요?','ask'),('저것 좀 처리해 줄래요?','ask'),
 ('좋은 아침이에요.','none'),('반갑습니다. 오늘 처음 왔어요.','none'),('커피가 맛있네요.','none'),('오늘은 비가 옵니다.','none')]

def state_dict(i):
    s=empty_state()
    if i%3==1:s[SYMPTOMS[i%len(SYMPTOMS)]]='present'
    if i%3==2:s[SYMPTOMS[i%len(SYMPTOMS)]]='absent'
    return s

def tool_row(text,target,available,question,state):
    opts={k:TOOL_DESCRIPTIONS[k] for k in available}
    listing='\n'.join('- '+k for k in opts)
    context='현재 기록: '+str(state)+'\n사용자 발화: '+text+'\n사용 가능한 동작:\n'+listing
    return {'kind':'tool','text':text,'question':question,'options':opts,'context':context,
            'target':target if target in opts else 'ask','requested':target}

def symptom_row(field,previous,text,target,question):
    context='대상 증상: '+NAMES[field]+'\n이전 상태: '+previous+'\n이번 사용자 발화: '+text
    return {'kind':'symptom','text':text,'field':field,'previous':previous,'question':question,
            'options':dict(SYMPTOM_DESCRIPTIONS),'context':context,'target':target}

def main():
    if DEST.exists():raise FileExistsError('Frozen dataset already exists')
    rng=random.Random(819721);tool=[];actions=list(TOOL_DESCRIPTIONS)
    for action,texts in TOOL_TRAIN.items():
        for text in texts:
            for tail in TAILS:
                for i in range(4):
                    # Fixed full candidate list in 3/4 cases; restricted capability
                    # case includes a safe explicit ask option.
                    available=list(actions) if i!=3 else ['ask',action,'none']
                    available=list(dict.fromkeys(available));rng.shuffle(available)
                    tool.append(tool_row(text+tail,action,available,TOOL_QUESTIONS[i],state_dict(i)))
    # Explicitly teach behavior when the requested capability is unavailable.
    for action,texts in TOOL_TRAIN.items():
        if action in ('ask','none'):continue
        for text in texts:
            for tail in TAILS[:5]:
                others=[x for x in actions if x not in (action,'ask')]
                avail=['ask']+rng.sample(others,2);rng.shuffle(avail)
                tool.append(tool_row(text+tail,action,avail,rng.choice(TOOL_QUESTIONS),state_dict(0)))
    rng.shuffle(tool)
    raw=[json.loads(x) for x in SOURCE.read_text(encoding='utf-8').splitlines()]
    rng.shuffle(raw);sym=[]
    for i,row in enumerate(raw[:1600]):
        sym.append(symptom_row(row['field'],row['previous'],row['text'],row['decision'],STATE_QUESTIONS[i%4]))
    # Old stress prompts are development data only and explicitly included here.
    stress=[]
    for case in authored_cases():
        previous=empty_state()
        for turn in case['turns']:
            for field in SYMPTOMS:
                for suffix in ['', ' 오늘 상담을 받고 있어요.', ' 제 기록을 확인해 주세요.']:
                    stress.append(symptom_row(field,previous[field],turn['input']+suffix,
                         turn['gold_patch'].get(field,'unchanged'),rng.choice(STATE_QUESTIONS)))
            previous=turn['expected']
    train=tool+sym+stress;rng.shuffle(train)
    dev=[tool_row(text,key,list(TOOL_DESCRIPTIONS),TOOL_QUESTION,empty_state()) for text,key in DEV_TOOL]
    test=[tool_row(text,key,list(TOOL_DESCRIPTIONS),'이 발화에 대해 다음에 어떤 동작을 해야 하나요?',empty_state()) for text,key in TEST_TOOL]
    # Capability subset checks: missing requested tool must select ask, not a
    # superficially related tool. The request is identical in both variants.
    for text,key in TEST_TOOL[:8:2]:
        options=[x for x in TOOL_DESCRIPTIONS if x!=key]
        test.append(tool_row(text,key,options,'이 발화에 대해 다음에 어떤 동작을 해야 하나요?',empty_state()))
    train_text={r['text'] for r in train};dev_text={r['text'] for r in dev};test_text={r['text'] for r in test}
    # Test examples deliberately repeat for availability counterfactual only.
    if train_text&dev_text or train_text&test_text or dev_text&test_text:raise ValueError('exact text leakage')
    for row in train+dev+test:
        if row['target'] not in row['options'] or len(row['options'])<2:raise ValueError('invalid target')
    DEST.mkdir(parents=True)
    for name,rows in [('train',train),('dev',dev),('tool_test',test)]:
        (DEST/(name+'.jsonl')).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    manifest={'seed':819721,'counts':{'train':len(train),'tool_train':len(tool),'symptom_train':len(sym),
      'previous_stress_in_train':len(stress),'dev':len(dev),'tool_test':len(test)},
      'train_unique_texts':len(train_text),'tool_target_counts':dict(Counter(x['target'] for x in tool)),
      'test_exact_text_overlap':0,'labels':'assistant-authored templates and automatic synthetic labels, no independent review',
      'source':'6000 decision synthetic/KLUE train subset; old stress examples explicitly repurposed as training',
      'files':{name:hashlib.sha256((DEST/name).read_bytes()).hexdigest() for name in ['train.jsonl','dev.jsonl','tool_test.jsonl']}}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
