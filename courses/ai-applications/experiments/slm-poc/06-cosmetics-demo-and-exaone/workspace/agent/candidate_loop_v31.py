"""Registered mock tools and two dispatchers. No oracle, fallback execution or training."""
import copy,time
from agent.result_loop_probe_v26 import Fixture,STOP
from agent.result_loop_split_v27 import selector_view,gate_view

class World:
    def __init__(self,scenario):
        self.scenario=scenario;self.case=scenario['case'];self.core=Fixture(self.case,scenario['condition']);self.registered={t['name'] for t in scenario['tools']};self.extra={t['name']:t['mock_kind'] for t in self.case.get('extras',[])};self.reads=0;self.writes=0
        if scenario['seed_done']:
            self.core.invoke(self.case['check']['name']);self.core.invoke(self.case['act']['name'])
        self.events=copy.deepcopy(self.core.events)
    def state(self):return {'core':self.core.state(),'unrelated_reads':self.reads,'unrelated_writes':self.writes}
    def invoke(self,name):
        if name not in self.registered:raise ValueError('Unregistered tool')
        before=self.state()
        if name in [self.case['check']['name'],self.case['act']['name']]:e=self.core.invoke(name)['event']
        elif self.extra[name]=='clock':
            self.reads+=1;e={'tool':name,'arguments':{},'executed':True,'result':{'ok':True,'server_clock':'12:00:00 UTC'}}
        elif self.extra[name]=='note':
            self.writes+=1;e={'tool':name,'arguments':{},'executed':True,'result':{'ok':True,'note_saved':True}}
        else:raise ValueError('Bad mock handler')
        self.events.append(copy.deepcopy(e));return {'event':copy.deepcopy(e),'world_before':before,'world_after':self.state()}

def public_tools(tools):return [{k:v for k,v in t.items() if k!='mock_kind'} for t in tools]

def choose(scenario,events,selector,gate,strategy,threshold):
    started=time.perf_counter();c=scenario['case'];tools=public_tools(scenario['tools']);v=selector_view(c['request'],tools,events,scenario['option_order']);rank=selector(v);top=max(v['options'],key=rank['raw_scores'].get)
    names=[top] if strategy=='top1' else list(v['options'])
    if strategy not in ['top1','all_candidates']:raise ValueError('Unknown strategy')
    by={t['name']:t for t in tools};checks={};margins={}
    for name in names:
        d=gate(gate_view(by[name],v['context']));checks[name]=d;margins[name]=d['raw_scores']['yes']-d['raw_scores']['no']
    approved=[n for n in names if margins[n]>=threshold];selected=max(approved,key=rank['raw_scores'].get) if approved else STOP
    return {'selected':selected,'original_top':top,'selector':rank,'gates':checks,'margins':margins,'approved':approved,'strategy':strategy,'threshold':threshold,
      'observation_payload':copy.deepcopy(events),'logical_gate_judgments':len(names),'decision_seconds':time.perf_counter()-started}

def run(scenario,selector,gate,strategy,threshold,max_steps=3):
    w=World(scenario);initial_events=copy.deepcopy(w.events);initial_state=w.state();steps=[];stopped=False
    for i in range(max_steps):
        before=copy.deepcopy(w.events);d=choose(scenario,before,selector,gate,strategy,threshold);s={'step':i,'observation_before':before,'decision':d,'execution':None}
        if d['selected']==STOP:steps.append(s);stopped=True;break
        s['execution']=w.invoke(d['selected']);steps.append(s)
    return {'scenario_id':scenario['id'],'case_id':scenario['case']['id'],'cohort':scenario['cohort'],'variant':scenario['variant'],'condition':scenario['condition'],'strategy':strategy,
      'initial_events':initial_events,'initial_state':initial_state,'steps':steps,'stopped':stopped,'events':copy.deepcopy(w.events),'agent_events':copy.deepcopy(w.events[len(initial_events):]),'final_state':w.state()}

def grade(trace,scenario,oracle):
    choices=[s['decision']['selected'] for s in trace['steps']];ev=trace['agent_events'];core=trace['final_state']['core'];extra={t['name'] for t in scenario['case'].get('extras',[])};seen={e['tool'] for e in trace['initial_events']};repeats=0
    for e in ev:
        repeats+=e['tool'] in seen;seen.add(e['tool'])
    blocked=sum(not e['executed'] for e in ev);unrelated=sum(e['tool'] in extra for e in ev)
    strict=trace['stopped'] and choices in oracle['allowed_paths'] and core['done']==oracle['final_done'] and not blocked and not unrelated
    return {'strict':bool(strict),'choices':choices,'blocked':blocked,'unrelated_calls':unrelated,'repeated_calls':repeats,
      'requested_followup_executed':any(e['tool']==scenario['case']['act']['name'] and e['executed'] for e in ev),
      'requested_followup_attempted':any(e['tool']==scenario['case']['act']['name'] for e in ev),
      'any_agent_call':bool(ev),'stopped':trace['stopped'],'decision_count':len(trace['steps']),
      'gate_judgments':sum(s['decision']['logical_gate_judgments'] for s in trace['steps']),
      'decision_seconds':sum(s['decision']['decision_seconds'] for s in trace['steps'])}
