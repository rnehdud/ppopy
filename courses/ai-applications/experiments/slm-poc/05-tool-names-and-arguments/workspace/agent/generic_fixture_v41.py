"""Small local executable fixtures for description-based selection; no external I/O.

Handlers have turn-bound empty arguments. Binding/extraction is NOT learned here.
The controller cannot access authored plans or expected states.
"""
import copy,hashlib,random
from agent.live_tool_agent import ToolRegistry
from agent.choice_agent_v1 import TOOL_QUESTION
from agent.decision_context_v37r1 import make_view,stable

EMPTY={'type':'object','properties':{},'additionalProperties':False}
OUTPUT={'type':'object','required':['ok'],'properties':{'ok':{'type':'boolean'}},'additionalProperties':True}
ASK='요청에 필요한 도구를 사용할 수 없거나 정보가 부족하면 실행하지 않고 사용자에게 확인한다.'
NONE='이번 요청의 작업이 끝났거나 도구를 실행할 요청이 아니면 도구를 더 사용하지 않고 답한다.'


def names(key):
    return {r:'x'+hashlib.sha256((key+':'+r).encode()).hexdigest()[:7] for r in ['a','b','c']}


def tool_definitions(spec,ids,available):
    return [{'name':ids[r],'description':spec['descriptions'][i],'inputSchema':copy.deepcopy(EMPTY),'outputSchema':copy.deepcopy(OUTPUT),'execution_contract':{'requires':[],'not_after':[]}} for i,r in enumerate(['a','b','c']) if r in available]


class World:
    def __init__(self,family,state,binding):self.family=family;self.state=copy.deepcopy(state);self.binding=copy.deepcopy(binding)
    def invoke(self,op):
        s=self.state;b=self.binding;f=self.family
        if op=='a':
            if f=='text':return {'ok':True,'count':len(s['words'])}
            if f=='units':return {'ok':True,'value':copy.deepcopy(s['last'])}
            return {'ok':True,'value':copy.deepcopy(s)}
        if f=='note':
            if op=='b':s['memo']+=b['text']
            else:s['memo']=''
        elif f=='todo':
            if op=='b':s['done']=True
            else:s['completed']=[]
        elif f=='media':
            if op=='b':s['playing']=b['song']
            else:s['queue']=[x for x in s['queue'] if x!=b['song']]
        elif f=='lamp':
            if op=='b':s['brightness']=b['brightness']
            else:s['color']=b['color']
        elif f=='parcel':
            if op=='b':s['place']=b['place']
            else:s['cancelled']=True
        elif f=='printer':
            if op=='b':s['paused']=True
            else:s['job']=None
        elif f=='climate':
            if op=='b':s['target']=b['target']
            else:s['fan']=b['fan']
        elif f=='timer':
            if op=='b':s['minutes']+=5
            else:s['minutes']=0;s['cancelled']=True
        elif f=='library':
            if op=='b':s['due_day']+=7
            else:s['lost']=True
        elif f=='image':
            if op=='b':s['width'],s['height']=s['height'],s['width']
            else:s['height']=round(s['height']*512/s['width']);s['width']=512
        elif f=='units':
            s['last']={'unit':'F','value':s['celsius']*9/5+32} if op=='b' else {'unit':'cm','value':s['meters']*100}
        elif f=='text':
            s['words']=sorted(s['words']) if op=='b' else list(dict.fromkeys(s['words']))
        else:raise ValueError('Unsupported fixture family')
        return {'ok':True,'changed':True}


def public_case(c):
    return {k:copy.deepcopy(c[k]) for k in ['family','request','initial','binding','definitions','ids','available','history','order_seed']}


class Session:
    def __init__(self,c,score,tokenizer):
        self.c=public_case(c);self.score=score;self.tokenizer=tokenizer;self.world=World(self.c['family'],self.c['initial'],self.c['binding']);self.events=[];self.steps=[];self.inputs=[]
        self.registry=ToolRegistry()
        for r in self.c['available']:
            d=next(d for d in self.c['definitions'] if d['name']==self.c['ids'][r])
            self.registry.register(d,lambda r=r:self.world.invoke(r))
    def view(self):
        ds=self.registry.definitions();options={d['name']:d['description']+'\n도구 이름: '+d['name']+'\n입력 정의: '+stable(d['inputSchema']) for d in ds}
        options.update(ask=ASK,none=NONE);keys=list(options);random.Random(self.c['order_seed']).shuffle(keys);options={k:options[k] for k in keys}
        packet={'request':self.c['request'],'state':copy.deepcopy(self.world.state),'observations':{},'pending':{},'events':copy.deepcopy(self.events),'history':self.c['history'],'available_actions':keys}
        v,meta=make_view(TOOL_QUESTION,options,packet,self.tokenizer)
        return v,meta,packet
    def run(self,max_steps=4):
        before=copy.deepcopy(self.world.state);seen=set();reason='step_limit'
        for j in range(max_steps):
            v,meta,packet=self.view();entry={'view':copy.deepcopy(v),'encoding':meta,'packet':packet};self.inputs.append(entry)
            if meta['tokens']>512:entry['error']='input_limit';reason='input_limit';break
            response=self.score(v);entry['response']=copy.deepcopy(response);raw=response['raw_scores']
            if set(raw)!=set(v['options']):raise ValueError('Bad score keys')
            choice=max(v['options'],key=raw.get);self.steps.append({'choice':choice,'scores':raw})
            if choice in ['ask','none']:reason='model_ask' if choice=='ask' else 'model_stop';break
            if choice in seen:reason='duplicate_call';break
            seen.add(choice)
            try:value=self.registry.invoke(choice,{})
            except Exception:value={'ok':False,'reason':'handler_error'}
            self.events.append({'tool':choice,'arguments':{},'executed':True,'result':value})
            if not value.get('ok'):reason='tool_error';break
        return {'before':before,'after':copy.deepcopy(self.world.state),'events':copy.deepcopy(self.events),'steps':copy.deepcopy(self.steps),'stop_reason':reason,'model_stopped':reason in ['model_stop','model_ask']}
