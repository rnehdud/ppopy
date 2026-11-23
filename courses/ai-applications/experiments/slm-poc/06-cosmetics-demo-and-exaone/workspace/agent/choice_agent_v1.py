"""Experimental Jev-style decision pipeline; no generative model is invoked.

The injected scorer ranks candidate descriptions. All actions are validated
against the caller's supplied capability set. Knowledge lookup is an injected
callback and is not a real KB implementation. Do not use for clinical records.
"""
from copy import deepcopy
import math
from .symptom_state_v1 import SYMPTOMS,SymptomSession

TOOL_DESCRIPTIONS={
 'record':'사용자가 말한 피부 증상을 기록하고 기존 상태를 갱신한다.',
 'search':'피부 관리에 관한 내용을 지식베이스에서 찾아본다.',
 'show':'이미 저장된 사용자의 피부 상태를 확인하여 보여준다.',
 'ask':'요청이 불분명하거나 필요한 도구가 없어 사용자에게 확인한다.',
 'none':'도구를 실행하지 않고 인사나 일반 대화로 응답한다.'}
TOOL_QUESTION='사용자 발화를 처리할 다음 동작 하나를 선택하세요.'
SYMPTOM_DESCRIPTIONS={
 'present':'사용자 본인에게 이 증상이 현재 있다고 말했다.',
 'absent':'사용자 본인에게 이 증상이 현재 없다고 명확히 말했다.',
 'unchanged':'이 발화에는 사용자 본인의 이 증상 상태를 바꿀 정보가 없다. 일반론, 다른 사람, 가정도 여기에 포함한다.',
 'unknown':'사용자가 본인의 이 증상 여부를 모른다고 직접 정정하거나 말했다.'}
SYMPTOM_QUESTION='대상 증상에 대해 이번 발화에 근거한 상태 업데이트 하나를 고르세요. 언급하지 않은 증상은 그대로 유지하며 추측하지 마세요.'
NAMES={'dryness':'건조함','breakout':'여드름이나 뾰루지','redness':'붉어짐','stinging':'따가움','itching':'가려움'}

def choose(scorer,question,options,context):
    if not isinstance(question,str) or not question.strip():raise ValueError('question required')
    if not isinstance(context,str):raise ValueError('context must be text')
    if not isinstance(options,dict) or len(options)<2:raise ValueError('at least two options required')
    if any(not isinstance(k,str) or not k or not isinstance(v,str) or not v for k,v in options.items()):
        raise ValueError('invalid option')
    values=scorer(question,deepcopy(options),context)
    if not isinstance(values,dict) or set(values)!=set(options):raise ValueError('scorer must return exactly the supplied keys')
    if any(isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) for v in values.values()):
        raise ValueError('invalid model scores')
    winner=max(options,key=lambda k:values[k])
    return {'choice':winner,'scores':dict(values),'score_note':'relative, uncalibrated; not probability of correctness'}

class ChoiceAgent:
    def __init__(self,scorer,lookup=None,available=None):
        self.scorer=scorer;self.session=SymptomSession();self.lookup=lookup
        self.available=tuple(available) if available is not None else tuple(TOOL_DESCRIPTIONS)
        if len(set(self.available))!=len(self.available) or any(k not in TOOL_DESCRIPTIONS for k in self.available):
            raise ValueError('invalid tool list')
        if len(self.available)<2:raise ValueError('at least two options required')
        if 'search' in self.available and lookup is None:raise ValueError('search requires explicit callback')

    def turn(self,text):
        if not isinstance(text,str) or not text.strip():raise ValueError('non-empty utterance required')
        before=self.session.state
        tool_options={k:TOOL_DESCRIPTIONS[k] for k in self.available}
        listing='\n'.join('- '+k for k in tool_options)
        context='현재 기록: '+str(before)+'\n사용자 발화: '+text+'\n사용 가능한 동작:\n'+listing
        choice=choose(self.scorer,TOOL_QUESTION,tool_options,context)
        action=choice['choice'];trace={'before':before,'input':text,'tool_decision':choice,'symptom_decisions':{},'action':action}
        if action=='record':
            patch={}
            for field in SYMPTOMS:
                context='대상 증상: '+NAMES[field]+'\n이전 상태: '+before[field]+'\n이번 사용자 발화: '+text
                decision=choose(self.scorer,SYMPTOM_QUESTION,SYMPTOM_DESCRIPTIONS,context)
                trace['symptom_decisions'][field]=decision
                if decision['choice']!='unchanged':patch[field]=decision['choice']
            # Gather/validate all choices before mutating the session.
            trace['patch']=patch
            trace['tool_result']=self.session.update(patch) if patch else {'ok':False,'reason':'no_symptom_update'}
        elif action=='search':
            trace['tool_result']=self.lookup(query=text,state=deepcopy(before))
        elif action=='show':trace['tool_result']={'ok':True,'state':deepcopy(before)}
        elif action=='ask':trace['tool_result']={'ok':True,'message':'무엇을 원하는지 조금 더 알려 주세요.'}
        else:trace['tool_result']={'ok':True,'message':'안녕하세요.'}
        trace['after']=self.session.state
        return trace
