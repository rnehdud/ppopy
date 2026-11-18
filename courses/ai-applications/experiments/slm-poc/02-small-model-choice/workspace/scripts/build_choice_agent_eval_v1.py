"""Freeze synthetic multi-question and multi-turn tests before training."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import empty_state
from agent.choice_agent_v1 import SYMPTOM_DESCRIPTIONS,NAMES

DEST=ROOT/'data/processed/choice_agent_eval_v2'
TRAIN=ROOT/'data/processed/choice_agent_v2/train.jsonl'
def state(**values):return {**empty_state(),**values}
def step(text,tool,expected):return {'input':text,'expected_action':tool,'expected_state':expected}
CASES=[
 {'id':'chain-record-show-search','turns':[
  step('지금 제 얼굴이 건조한 걸 적어 주세요.','record',state(dryness='present')),
  step('지금까지 남긴 제 증상 목록을 볼 수 있을까요?','show',state(dryness='present')),
  step('피부 진정에 쓰이는 성분을 자료에서 검색해 줘요.','search',state(dryness='present'))]},
 {'id':'record-greeting','turns':[
  step('피부가 가려우니 기록을 남겨 주세요.','record',state(itching='present')),
  step('좋은 아침이에요.','none',state(itching='present'))]},
 {'id':'absent-show','turns':[
  step('뾰루지가 없다고 제 상태에 써 주세요.','record',state(breakout='absent')),
  step('제가 기록해 둔 피부 상태를 보여 주세요.','show',state(breakout='absent'))]},
 {'id':'stinging-ambiguous','turns':[
  step('제 얼굴이 따가운 상태를 저장해 주세요.','record',state(stinging='present')),
  step('그거 해줘.','ask',state(stinging='present'))]},
 {'id':'dry-correct-show','turns':[
  step('제 볼이 건조해요. 제 기록에 적어 주세요.','record',state(dryness='present')),
  step('이제 볼이 건조하지 않아요. 기록을 바꿔 주세요.','record',state(dryness='absent')),
  step('제 피부에 대해 저장한 것을 볼래요.','show',state(dryness='absent'))]},
 {'id':'symptom-direct','turns':[
  step('제 얼굴이 지금 많이 가려워요.','record',state(itching='present')),
  step('지금 저장된 상태가 뭐예요?','show',state(itching='present'))]},
 {'id':'search-without-symptom','turns':[
  step('만약 가렵다면 어떻게 관리하는지 지식베이스에서 찾아주세요.','search',state()),
  step('현재 저장된 증상 정보를 알려주세요.','show',state())]},
 {'id':'other-person','turns':[
  step('친구는 여드름이 있지만 제 상태는 기록하지 마세요.','none',state()),
  step('내 기록은 지금 어떻게 돼 있나요?','show',state())]},
]

def main():
    if DEST.exists():raise FileExistsError('Evaluation already frozen')
    train={json.loads(x)['text'] for x in TRAIN.read_text(encoding='utf-8').splitlines()}
    for case in CASES:
        for turn in case['turns']:
            if turn['input'] in train:raise ValueError('pipeline test text leaked into training')
    symptom=[]
    examples=[('지금 제 얼굴이 건조한 걸 적어 주세요.','dryness','present'),
              ('지금 제 얼굴이 건조한 걸 적어 주세요.','itching','unchanged'),
              ('뾰루지가 없다고 제 상태에 써 주세요.','breakout','absent'),
              ('뾰루지가 없다고 제 상태에 써 주세요.','dryness','unchanged'),
              ('제 얼굴이 지금 많이 가려워요.','itching','present'),
              ('제 얼굴이 지금 많이 가려워요.','redness','unchanged')]
    for text,field,target in examples:
        context='대상 증상: '+NAMES[field]+'\n이전 상태: unknown\n이번 사용자 발화: '+text
        symptom.append({'kind':'symptom','text':text,'field':field,'question':'이 발화에서 이 증상을 어떻게 기록하나요?',
                        'context':context,'options':dict(SYMPTOM_DESCRIPTIONS),'target':target})
    DEST.mkdir(parents=True)
    (DEST/'pipeline_cases.json').write_text(json.dumps(CASES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (DEST/'question_cases.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in symptom),encoding='utf-8')
    manifest={'cases':len(CASES),'turns':sum(len(c['turns']) for c in CASES),'symptom_questions':len(symptom),
              'caveat':'synthetic assistant-authored expected actions and states; no independent human review; fixed before model training',
              'files':{n:hashlib.sha256((DEST/n).read_bytes()).hexdigest() for n in ['pipeline_cases.json','question_cases.jsonl']}}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
