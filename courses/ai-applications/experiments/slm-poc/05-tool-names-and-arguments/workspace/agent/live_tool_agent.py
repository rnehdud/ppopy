"""Small-model tool loop for the local chat, with explicit injected handlers.

No model-generated executable code or arbitrary argument extraction. Each tool
is bound to this user turn, has an empty input schema and validates its output.
"""
import copy,json,math
from dataclasses import dataclass
from jsonschema import Draft202012Validator
from agent.contract_filter_v34 import readiness
from agent.result_loop_split_v27 import selector_view,gate_view
from agent.result_loop_probe_v26 import STOP,stable


@dataclass
class Tool:
    definition:dict
    handler:object


class ToolRegistry:
    def __init__(self):self._tools={}
    def register(self,definition,handler):
        d=copy.deepcopy(definition);name=d['name']
        if not isinstance(name,str) or not name or name in self._tools or not callable(handler):raise ValueError('Invalid or duplicate tool')
        if not isinstance(d.get('description'),str) or not d['description'].strip():raise ValueError('Tool description required')
        for key in ['inputSchema','outputSchema']:Draft202012Validator.check_schema(d[key])
        if not Draft202012Validator(d['inputSchema']).is_valid({}):raise ValueError('This chat supports turn-bound empty arguments only')
        readiness(d,[]);self._tools[name]=Tool(d,handler)
    def remove(self,name):self._tools.pop(name)
    def definitions(self):return [copy.deepcopy(t.definition) for t in self._tools.values()]
    def invoke(self,name,arguments):
        t=self._tools[name];Draft202012Validator(t.definition['inputSchema']).validate(arguments)
        result=t.handler(**copy.deepcopy(arguments))
        Draft202012Validator(t.definition['outputSchema']).validate(result)
        # JSON roundtrip rejects non-JSON handler outputs before model feedback.
        return json.loads(json.dumps(result,ensure_ascii=False,allow_nan=False))


def _score(fn,role,view):
    r=fn(role,copy.deepcopy(view));scores=r['raw_scores']
    if set(scores)!=set(view['options']) or any(type(v) not in [int,float] or not math.isfinite(v) for v in scores.values()):raise ValueError('Invalid model scores')
    return r


def decide(text,registry,events,history,score,threshold=-1.5):
    definitions=registry.definitions()
    if not definitions:return {'selected':STOP,'raw_selected':STOP,'reason':'no_registered_tools','scores':{},'gates':{}}
    tools=[{'name':d['name'],'description':d['description'],'parameters':d['inputSchema']} for d in definitions]
    order=[t['name'] for t in tools]+[STOP];v=selector_view(text,tools,events,order)
    # Retain bounded real conversation, rather than discard it to change a decision.
    v['context']=v['context'].replace('대화:\n[]','대화:\n'+stable(history),1)
    ranked=_score(score,'selector',v);gates={};approved=[]
    for t in tools:
        g=_score(score,'gate',gate_view(t,v['context']));gates[t['name']]=g
        if g['raw_scores']['yes']-g['raw_scores']['no']>=threshold:approved.append(t['name'])
    raw=max(approved,key=ranked['raw_scores'].get) if approved else STOP
    condition=None;selected=raw;reason='model_stop' if raw==STOP else 'model_choice'
    if raw!=STOP:
        condition=readiness(next(d for d in definitions if d['name']==raw),events)
        if not condition['eligible']:selected=STOP;reason='condition_not_met'
    # No alternative candidate substituted after a failed condition.
    return {'selected':selected,'raw_selected':raw,'reason':reason,'condition':condition,'scores':ranked,'gates':gates,'threshold':threshold}


def run_turn(text,registry,history,score,state_version,max_steps=3):
    events=[];steps=[];seen=set();stop_reason='step_limit';model_stopped=False
    for i in range(max_steps):
        try:d=decide(text,registry,events,history,score)
        except ValueError as exc:
            if 'context' not in str(exc).lower() and 'input exceeds' not in str(exc).lower():raise
            stop_reason='input_limit';break
        st={'index':i,'decision':d,'event':None};steps.append(st)
        if d['selected']==STOP:
            stop_reason=d['reason'];model_stopped=stop_reason=='model_stop';break
        name=d['selected'];key=(name,state_version())
        if key in seen:stop_reason='duplicate_call';break
        seen.add(key)
        try:result=registry.invoke(name,{})
        except Exception:
            # Handler may already have had effects; never retry or claim rollback.
            event={'tool':name,'arguments':{},'executed':True,'result':{'ok':False,'reason':'handler_error','effects_unknown':True}}
            events.append(event);st['event']=copy.deepcopy(event);stop_reason='handler_error';break
        event={'tool':name,'arguments':{},'executed':True,'result':result};events.append(event);st['event']=copy.deepcopy(event)
        if result.get('ok') is not True:stop_reason='tool_error';break
    return {'steps':steps,'events':events,'stop_reason':stop_reason,'model_stopped':model_stopped,
      'complete':False,'completion_note':'Overall task completion is not inferred from one tool done=true.'}
