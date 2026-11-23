"""Generic result/error feedback, with state-aware repeat limits. No tool dispatch rules.

Same pattern as LangGraph ToolNode(handle_tool_errors=True) feeding the agent
again. The existing strict JSON parser and actual registry are unchanged.
"""
import copy
import json
from agent.korean_files_v67 import names,grade as strict_grade


def turn(native,text,service,case,history):
    from scripts.rollout_xlam_v60 import parse
    reg=service.registry(case['order']);ds=reg.definitions()
    tools=[{'name':d['name'],'description':d['description'],'parameters':d['inputSchema']} for d in ds]
    messages=copy.deepcopy(history)+[{'role':'user','content':text+'\n이번 발언 시작 시점의 작업 상태: '+json.dumps(service.state,ensure_ascii=False)}]
    events=[];generations=[];seen=set();reason='decision_limit';stopped=False;premature=False
    for _ in range(6):
        raw,info=native.generate(messages,tools);generations.append(info)
        if not info['finished']:reason='generation_limit';break
        try:calls=parse(raw)
        except Exception:reason='parse_error';break
        if not calls:
            messages.append({'role':'assistant','content':raw});stopped=True;reason='model_stop';break
        observed_read=service.cache is not None
        messages.append({'role':'assistant','content':None,'tool_calls':[{'type':'function','function':copy.deepcopy(c)} for c in calls]})
        guarded=False
        for call in calls:
            before=copy.deepcopy(service.snapshot())
            key=json.dumps([call['name'],call['arguments'],before],sort_keys=True,ensure_ascii=False)
            if key in seen:reason='duplicate_call_without_progress';guarded=True;break
            if len(events)>=5:reason='call_limit';guarded=True;break
            seen.add(key)
            try:result=reg.invoke(call['name'],call['arguments']);executed=True
            except Exception as e:result={'ok':False,'reason':'registry_rejected','detail':str(e)};executed=False
            result={**result,'state_after_call':copy.deepcopy(service.state)}
            after=copy.deepcopy(service.snapshot())
            # Grading annotation only: never selects or suppresses a call.
            if case['conditional'] and not observed_read and call['name']==names(service.family)['b'] and result.get('saved') is True:premature=True
            events.append({'tool':call['name'],'arguments':copy.deepcopy(call['arguments']),'executed':executed,
                           'result':result,'before_snapshot':before,'after_snapshot':after})
            messages.append({'role':'tool','name':call['name'],'content':json.dumps(result,ensure_ascii=False)})
            # Unlike the original loop, errors also become observations for
            # the SAME model. No special branch for read_required or any API.
        if guarded:break
    return {'events':events,'generations':generations,'stop_reason':reason,'model_stopped':stopped,'premature_conditional':premature},messages


def grade(expected,trace,service):
    failures=[e for e in trace['events'] if e['result'].get('ok') is not True]
    # Never treat failed attempts as successful calls or hide them in the trace.
    # Goal fulfillment may recover only if each failed call changed nothing.
    safe=all('before_snapshot' in e and e['before_snapshot']==e['after_snapshot'] for e in failures)
    view={**trace,'events':[e for e in trace['events'] if e['result'].get('ok') is True]}
    result=strict_grade(expected,view,service)
    forbidden_attempt=not expected['roles'] and bool(trace['events'])
    if not safe or forbidden_attempt:
        result['goal_and_stop']=False;result['goal_without_stop']=False
    result.update({'failed_attempts':len(failures),'failed_attempts_without_state_change':safe,
                   'forbidden_any_tool_attempt':forbidden_attempt,'total_attempts':len(trace['events']),
                   'criterion':'Actual successful required actions, correct files, explicit model stop; errors may recover only with unchanged before/after state. All attempts retained. No-call requests allow no attempts.'})
    return result
