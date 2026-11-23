"""Declared tool contracts + observed events only. No goals, gold routes or world access."""
import copy,time
from agent.candidate_loop_v31 import World,public_tools
from agent.result_loop_split_v27 import selector_view,gate_view
from agent.result_loop_probe_v26 import STOP


def _matches(event, rule):
    return event.get('tool') == rule['tool'] and event.get('arguments') == rule['arguments']


def _successful(event):
    return event.get('executed') is True and isinstance(event.get('result'),dict) and event['result'].get('ok') is True


def _validate_rule(rule):
    if set(rule) != {'tool','arguments','field','equals'} or not isinstance(rule['tool'],str) or not isinstance(rule['arguments'],dict) or not isinstance(rule['field'],str) or type(rule['equals']) is not bool:
        raise ValueError('Invalid explicit contract rule')


def readiness(tool, events):
    """Unknown is NOT false; no successful evidence is fabricated. Checks remain callable."""
    contract=tool['execution_contract']
    if set(contract)!={'requires','not_after'}:raise ValueError('Invalid contract')
    details=[]
    for rule in contract['not_after']:
        _validate_rule(rule)
        hits=[(i,e) for i,e in enumerate(events) if _matches(e,rule) and _successful(e) and type(e['result'].get(rule['field'])) is bool and e['result'][rule['field']] is rule['equals']]
        if hits:details.append({'kind':'not_after','status':'completed','rule':copy.deepcopy(rule),'event_index':hits[-1][0]})
    for rule in contract['requires']:
        _validate_rule(rule);hits=[(i,e) for i,e in enumerate(events) if _matches(e,rule)]
        status='unknown';index=None
        if hits:
            index,e=hits[-1]
            if not _successful(e):status='unknown'
            elif type(e['result'].get(rule['field'])) is bool:status='met' if e['result'][rule['field']] is rule['equals'] else 'unmet'
        details.append({'kind':'requires','status':status,'rule':copy.deepcopy(rule),'event_index':index})
    return {'eligible':all(d['status']=='met' for d in details),'evidence':details}


def choose(request, tools, events, order, selector, gate, strategy, threshold):
    """Same raw model scores under either policy; only declared eligibility changes selection.

    The independent scalar encoder does not jointly read a candidate list. Score every
    candidate for raw-proposal accounting, then filter before final argmax. Contracts
    are dispatch metadata, NOT a new prompt or automatic natural-language parser.
    """
    if strategy not in ['baseline','contract_filter']:raise ValueError(strategy)
    started=time.perf_counter();ts=public_tools(tools);v=selector_view(request,ts,events,order);rank=selector(v)
    by={t['name']:t for t in ts};names=list(v['options']);gates={n:gate(gate_view(by[n],v['context'])) for n in names}
    margins={n:r['raw_scores']['yes']-r['raw_scores']['no'] for n,r in gates.items()}
    approved=[n for n in names if margins[n]>=threshold]
    raw=max(approved,key=rank['raw_scores'].get) if approved else STOP
    conditions={n:readiness(by[n],events) for n in names}
    eligible=[n for n in names if conditions[n]['eligible']]
    allowed=approved if strategy=='baseline' else [n for n in approved if n in eligible]
    selected=max(allowed,key=rank['raw_scores'].get) if allowed else STOP
    return {'selected':selected,'raw_model_selected':raw,'raw_model_selected_eligible':raw==STOP or conditions[raw]['eligible'],
      'original_top':max(names,key=rank['raw_scores'].get),'selector':rank,'gates':gates,'margins':margins,
      'approved':approved,'eligible':eligible,'conditions':conditions,'allowed':allowed,'strategy':strategy,'threshold':threshold,
      'observation_payload':copy.deepcopy(events),'logical_gate_judgments':len(names),'decision_seconds':time.perf_counter()-started}


def run(scenario,selector,gate,strategy,threshold):
    w=World(scenario);initial_events=copy.deepcopy(w.events);initial_state=w.state();steps=[];stopped=False
    for i in range(scenario['decision_budget']):
        before=copy.deepcopy(w.events);d=choose(scenario['case']['request'],scenario['tools'],before,scenario['option_order'],selector,gate,strategy,threshold)
        st={'step':i,'observation_before':before,'decision':d,'execution':None};steps.append(st)
        if d['selected']==STOP:stopped=True;break
        st['execution']=w.invoke(d['selected'])
    return {'scenario_id':scenario['id'],'case_id':scenario['case']['id'],'cohort':scenario['cohort'],'variant':scenario['variant'],'condition':scenario['condition'],'strategy':strategy,
      'initial_events':initial_events,'initial_state':initial_state,'steps':steps,'stopped':stopped,'events':copy.deepcopy(w.events),'agent_events':copy.deepcopy(w.events[len(initial_events):]),'final_state':w.state()}
