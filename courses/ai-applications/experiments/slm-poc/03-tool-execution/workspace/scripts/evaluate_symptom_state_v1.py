"""Exploratory untrained Qwen3 test of the isolated three-state tool."""
import json
from pathlib import Path
import sys
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.symptom_state_v1 import PATCH_SCHEMA,SymptomSession,empty_state

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/symptom-state-v1'
TOOLS=[{'type':'function','function':{'name':'update_symptom_status',
    'description':'사용자가 말한 현재 피부 증상만 기록하거나 정정한다. 이번 발화에서 말하지 않은 증상은 그대로 둔다.',
    'parameters':{'type':'object','properties':{'patch':PATCH_SCHEMA},'required':['patch'],'additionalProperties':False}}}]
SYSTEM='''한국어로 대화하는 증상 기록 도우미다. 사용자가 본인의 현재 증상이 있다고 명시하면 present, 없다고 명시하면 absent로 해당 증상만 update_symptom_status에 기록한다.
언급하지 않았으면 unknown이며 없다고 추측하지 않는다. 본인의 상태가 아닌 일반론과 가능성 질문을 현재 증상으로 기록하지 않는다.
사용자가 이전 진술을 정정하거나 현재 상태가 바뀌면 해당 증상만 수정한다. 본인이 상태를 더 이상 확신하지 못한다고 정정하면 unknown으로 기록한다.
증상: dryness=건조, breakout=여드름/뾰루지, redness=붉어짐, stinging=따가움, itching=가려움.
진단이나 치료, 제품 추천은 이 도구의 범위가 아니다. 실제 업데이트 없이 기록했다고 말하지 않는다.
현재 상태: {state}'''

def make(**changes):return {**empty_state(),**changes}
CASES=[
 {'id':'unmentioned','turns':[('안녕하세요. 피부 관리에 관심이 있어요.',make())]},
 {'id':'explicit_absence','turns':[('저는 여드름이 없어요.',make(breakout='absent'))]},
 {'id':'multi_symptom','turns':[('피부가 건조하고 가려운데 여드름은 없어요.',make(dryness='present',itching='present',breakout='absent'))]},
 {'id':'correction_preserve','turns':[('피부가 건조하고 가려워요.',make(dryness='present',itching='present')),
                                    ('이제 건조하지 않아요. 가려움은 그대로예요.',make(dryness='absent',itching='present'))]},
 {'id':'hypothetical','turns':[('화장품을 쓰면 여드름이 생길까요?',make())]},
 {'id':'uncertainty','turns':[('여드름이 있어요.',make(breakout='present')),
                             ('정정할게요. 여드름이 있는지 잘 모르겠어요.',make(breakout='unknown'))]},
]

def request(messages):
    payload={'model':'qwen3-4b-instruct-2507','messages':messages,'tools':TOOLS,'tool_choice':'auto',
             'parallel_tool_calls':False,'temperature':0,'seed':42,'max_tokens':384,'stream':False,'cache_prompt':False}
    req=urllib.request.Request('http://127.0.0.1:18081/v1/chat/completions',
          data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=180) as response:return json.load(response)['choices'][0]

def turn(session,text):
    messages=[{'role':'system','content':SYSTEM.replace('{state}',json.dumps(session.state,ensure_ascii=False))},
              {'role':'user','content':text}]
    calls=[]
    for _ in range(4):
        choice=request(messages)
        if choice.get('finish_reason')=='length':return {'ok':False,'error':'length','calls':calls,'state':session.state}
        msg=choice['message'];tool_calls=msg.get('tool_calls') or []
        if not tool_calls:
            content=msg.get('content') or ''
            return {'ok':bool(content.strip()),'answer':content,'calls':calls,'state':session.state}
        messages.append({'role':'assistant','content':msg.get('content') or '', 'tool_calls':tool_calls})
        for call in tool_calls:
            name=call.get('function',{}).get('name');raw=call.get('function',{}).get('arguments','{}')
            args=raw
            try:
                args=json.loads(raw) if isinstance(raw,str) else raw
                if len(tool_calls)!=1 or name!='update_symptom_status' or set(args)!= {'patch'}:raise ValueError('Invalid tool call')
                result=session.update(args['patch'])
            except (ValueError,TypeError,KeyError) as e:
                result={'ok':False,'error':str(e)}
            calls.append({'name':name,'arguments':args,'result':result})
            messages.append({'role':'tool','tool_call_id':call['id'],'name':name,'content':json.dumps(result,ensure_ascii=False)})
    return {'ok':False,'error':'tool_step_limit','calls':calls,'state':session.state}

def main():
    cfg=json.loads((ROOT/'output/runtime-qwen3/server_config.json').read_text(encoding='utf-8-sig'))
    if cfg.get('adapter') or cfg.get('port')!=18081:raise ValueError('Expected unadapted local Qwen3')
    OUT.mkdir(parents=True,exist_ok=False)
    cases=[]
    for case in CASES:
        session=SymptomSession();turns=[]
        for text,expected in case['turns']:
            before=session.state;result=turn(session,text)
            turns.append({'input':text,'before':before,'expected':expected,'result':result,
                          'matches':result['ok'] and result['state']==expected})
        cases.append({'id':case['id'],'turns':turns,'passes':all(t['matches'] for t in turns)})
        print(case['id'],'matches',[t['matches'] for t in turns],flush=True)
    report={'status':'synthetic exploratory; labels not independently reviewed',
            'scope':'Only symptom states, no time/product/KB/recommendation; separate from existing agent.',
            'server':cfg,'cases':cases}
    (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'scenarios':len(cases),'passed':sum(x['passes'] for x in cases),
                      'turns':sum(len(x['turns']) for x in cases),
                      'matched_turns':sum(t['matches'] for c in cases for t in c['turns'])}))

if __name__=='__main__':main()
