"""Small observable loop. Tools are in-memory fixtures; chooser alone picks actions."""
import copy,json

STOP='no_tool'
QUESTION='사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.'
STOP_TEXT='지금은 도구를 호출하지 않고 사용자에게 직접 답하거나 필요한 정보를 확인한다.'

def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

class Fixture:
    def __init__(self,case,condition):
        self.case=case;self.condition=bool(condition);self.last_check=None;self.done=False;self.events=[]

    def state(self):
        return {'condition':self.condition,'last_check':self.last_check,'done':self.done}

    def invoke(self,name):
        """Validate the chosen operation; never substitute a different tool."""
        before=self.state()
        if name==self.case['check']['name']:
            self.last_check=self.condition;result={'ok':True,self.case['predicate']:self.condition};executed=True
        elif name==self.case['act']['name']:
            if self.done:result={'ok':False,'error':'already_done'};executed=False
            elif self.last_check is not True or self.condition is not True:result={'ok':False,'error':'precondition_not_met'};executed=False
            else:
                self.done=True
                if self.case['consumes_condition']:self.condition=False
                result={'ok':True,'done':True};executed=True
        else:raise ValueError('Unknown tool: '+str(name))
        e={'tool':name,'arguments':{},'result':result,'executed':executed};self.events.append(copy.deepcopy(e))
        return {'event':copy.deepcopy(e),'world_before':before,'world_after':self.state()}

def model_view(request,tools,events,fmt,option_order):
    """No world truth, expected label, target step or evaluator state enters here."""
    from scripts.selector_interface_data_v18 import full
    options={t['name']:full(t) for t in tools};options[STOP]=STOP_TEXT;options={k:options[k] for k in option_order}
    context='대화:\n[]\n이번 사용자 발화: '+request
    if fmt=='json':context+='\n도구 실행 기록:\n'+stable(events)
    elif fmt=='labeled':
        context+='\n도구 실행 기록:\n'
        if not events:context+='[]'
        for i,e in enumerate(events,1):
            context+='\n기록 '+str(i)+'\n도구: '+e['tool']+'\n인자: '+stable(e['arguments'])+'\n실행됨: '+stable(e['executed'])+'\n결과: '+stable(e['result'])
    else:raise ValueError('Unknown format')
    return {'question':QUESTION,'options':options,'context':context}

def run_episode(case,condition,chooser,fmt,max_steps=3):
    """No oracle argument, no scripted check->act branch and no corrective rerouting."""
    fixture=Fixture(case,condition);steps=[];stopped=False
    for i in range(max_steps):
        decision=chooser(case['request'],[case['check'],case['act']],copy.deepcopy(fixture.events),fmt,case['option_order'])
        choice=decision['selected'];record={'step':i,'observation_before':copy.deepcopy(fixture.events),'decision':decision}
        if choice==STOP:
            record['execution']=None;steps.append(record);stopped=True;break
        record['execution']=fixture.invoke(choice);steps.append(record)
    return {'case_id':case['id'],'condition':condition,'format':fmt,'steps':steps,'stopped':stopped,'events':copy.deepcopy(fixture.events),'final_state':fixture.state()}

def probe_states(case):
    """Observer probes: fixture actions are injected here, NOT agent successes."""
    positive=Fixture(case,True);positive.invoke(case['check']['name']);after_true=copy.deepcopy(positive.events);positive.invoke(case['act']['name'])
    negative=Fixture(case,False);negative.invoke(case['check']['name'])
    return {'initial':[],'after_true':after_true,'after_false':copy.deepcopy(negative.events),'after_done':copy.deepcopy(positive.events)}

def grade_episode(trace,oracle):
    choices=[s['decision']['selected'] for s in trace['steps']];blocked=sum(not e['executed'] for e in trace['events']);seen=set();repeated=0
    for e in trace['events']:
        if e['tool'] in seen:repeated+=1
        seen.add(e['tool'])
    state_ok=trace['final_state']['done']==oracle['final_done']
    return {'strict_pass':choices==oracle['choices'] and trace['stopped'] and state_ok and blocked==0,'choices':choices,'state_ok':state_ok,'blocked_attempts':blocked,'repeated_calls':repeated,'stopped':trace['stopped']}
