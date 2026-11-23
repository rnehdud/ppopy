"""Frozen-case evaluation. Oracle actions/labels never reach the model client."""
import csv
import hashlib
import json
import re
import time
from agent.runtime import Agent,EMPTY_STATE,SYSTEM,TOOLS


def matches(actual,expected):
    return all(sorted(actual.get(k,[]))==sorted(v) if isinstance(v,list) else actual.get(k)==v for k,v in expected.items())


def evaluate(client,cases,path,phase,trained,model_id='qwen2.5-3b-nf4',model_description=None,
             base_url='http://127.0.0.1:18080'):
    path.mkdir(parents=True,exist_ok=False)
    results=[]
    rows=[]
    total_start=time.perf_counter()
    for i,case in enumerate(cases):
        agent=Agent(path/f'{case["id"]}.events.jsonl',initial=case.get('initial'),fail_search=case.get('fail_search',False),
                    model_client=client,model_id=model_id,base_url=base_url,
                    model_description=model_description or 'Qwen2.5-3B NF4, same base before/after adapter',
                    additional_training=trained)
        turns=[]
        expected={**EMPTY_STATE,**case.get('initial',{})}
        for n,step in enumerate(case['turns']):
            expected={**expected,**step['expected']}
            result=agent.turn(step['input'])
            checks={'completed':result['ok'],'state':matches(result['state'],expected)}
            calls=result['calls']
            if step.get('required_tool'):
                checks['required_tool']=any(e['name']==step['required_tool'] and
                   (e['result'].get('ok') or step.get('expect_search_failure')) for e in calls)
            if step.get('no_tools'):
                checks['no_tools']=not calls
            if step.get('search_arguments'):
                checks['search_arguments']=any(e['name']=='search_knowledge_base' and isinstance(e['arguments'],dict)
                        and matches(e['arguments'],step['search_arguments']) for e in calls)
            if step.get('document_id'):
                checks['source_id']=step['document_id'] in result.get('answer','')
            if step.get('expect_search_failure'):
                checks['error_disclosed']=bool(re.search(r'오류|실패|없|못|불가',result.get('answer','')))
                checks['no_invented_source']='FIXTURE-' not in result.get('answer','')
            passed=all(checks.values())
            turns.append({'turn':n,'input':step['input'],'expected_state':expected,'checks':checks,'passed':passed,'result':result})
            rows.append({'scenario_id':case['id'],'category':case['category'],'turn':n,'passed':passed,
                         'checks':json.dumps(checks),'state':json.dumps(result['state'],ensure_ascii=False),
                         'seconds':result.get('seconds'),'answer':result.get('answer','')})
            if not result['ok']:
                break
        results.append({'id':case['id'],'category':case['category'],
                        'passed':len(turns)==len(case['turns']) and all(t['passed'] for t in turns),'turns':turns})
        if (i+1)%10==0 or i+1==len(cases):
            print(f'{phase}: evaluated {i+1}/{len(cases)} frozen scenarios',flush=True)
    state_hits=sum(t['checks']['state'] for c in results for t in c['turns'])
    report={'phase':phase,'additional_training':trained,'scenarios':len(cases),
            'passed_scenarios':sum(c['passed'] for c in results),'executed_turns':len(rows),
            'planned_turns':sum(len(c['turns']) for c in cases),'passed_turns':sum(r['passed'] for r in rows),
            'state_exact_turns':state_hits,'elapsed_seconds':time.perf_counter()-total_start,
            'results':results}
    (path/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if rows:
        with (path/'turns.csv').open('w',encoding='utf-8-sig',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return report
