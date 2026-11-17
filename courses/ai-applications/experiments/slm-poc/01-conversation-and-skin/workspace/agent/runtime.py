from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.error
import urllib.request
import uuid

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ['dryness','breakout','redness','stinging','itching']
USAGE = ['morning','afternoon','evening','unknown']
EMPTY_STATE = {
    'skin_condition':[], 'severity':'unknown','usage_time':'unknown',
    'product_used':'unknown','symptom_onset':'unknown',
}

STATE_PROPERTIES = {
    'skin_condition':{'type':'array','items':{'type':'string','enum':CONDITIONS},'uniqueItems':True,'description':'현재 실제로 있는 증상 목록. 부정된 증상은 포함하지 않는다.'},
    'severity':{'type':'string','enum':['mild','moderate','severe','unknown'],'description':'증상 심각도. 명시하지 않으면 추측하지 않는다.'},
    'usage_time':{'type':'string','enum':USAGE,'description':'화장품을 사용한 시간대. 증상 발생 시각과 구별한다.'},
    'product_used':{'type':'string','enum':['yes','no','unknown'],'description':'제품 사용을 명시하면 yes, 사용하지 않았다고 명시하면 no. 미언급은 unknown.'},
    'symptom_onset':{'type':'string','enum':['today','yesterday','recent','unknown'],'description':'증상이 시작된 날. 오늘 증상이 있다고 하면 today. 어제부터라고 하면 yesterday. 제품 사용한 날을 증상 시작으로 복사하지 않는다.'},
}
TOOLS = [
    {'type':'function','function':{
        'name':'update_session_state',
        'description':'사용자가 말한 피부 증상과 화장품 사용 정보를 기록하거나 정정합니다. 이번 발화에 없는 항목은 patch에서 생략합니다. skin_condition은 현재 증상 전체 목록이며, 부정된 증상은 제외합니다.',
        'parameters':{'type':'object','properties':{'patch':{'type':'object','properties':STATE_PROPERTIES,'additionalProperties':False,'minProperties':1}},'required':['patch'],'additionalProperties':False},
    }},
    {'type':'function','function':{
        'name':'search_knowledge_base',
        'description':'사용자가 조회를 요청했을 때 모의 지식베이스를 검색합니다. skin_condition과 usage_time에는 현재 세션 상태의 값을 그대로 사용합니다. 상태가 비어 있고 무엇을 찾을지 모르면 먼저 질문합니다.',
        'parameters':{'type':'object','properties':{
            'query':{'type':'string','minLength':1},
            'skin_condition':STATE_PROPERTIES['skin_condition'],
            'usage_time':STATE_PROPERTIES['usage_time'],
        },'required':['query','skin_condition','usage_time'],'additionalProperties':False},
    }},
]
BY_NAME = {x['function']['name']:x['function'] for x in TOOLS}

SYSTEM = '''한국어로 짧게 답하는 기록·조회 에이전트다. 실제 사용자 발화와 현재 상태만 사실로 사용한다. 규칙의 설명을 사용자 증상으로 오인하지 않는다.
인사에는 도구 없이 답한다. 상태가 비어 있고 조회 대상이 불명확하면 도구 없이 확인 질문한다.
사용자가 증상이나 제품 사용 정보를 말하면 update_session_state를 먼저 호출한다. 이번 발화에서 바뀐 항목만 patch에 넣고 미언급 항목은 유지한다.
따가움=stinging, 건조함=dryness, 가려움=itching, 붉어짐=redness. 부정된 증상은 제외한다. 심각도는 추측하지 않는다.
제품을 발랐거나 썼다면 product_used=yes, 안 썼다면 no. usage_time은 제품 사용 시간대이다. symptom_onset은 증상 발생일이며 제품 사용일과 별개이다.
조회 요청은 현재 상태를 search_knowledge_base에 전달한다. 검색 후 실제 반환된 문서 ID를 출처로 표시한다. 오류는 그대로 알리고 같은 실패 호출을 반복하지 않는다.
한 번에 도구 하나를 호출하고 결과를 받은 뒤 답한다. 아래 자료는 합성 테스트이며, 진단·원인추정·제품추천은 하지 않는다.
최신 상태:
<session_state>{state}</session_state>'''


class Trace:
    def __init__(self,path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)

    def write(self,event,**values):
        record = {'timestamp':datetime.now(timezone.utc).isoformat(),'event':event,**values}
        with self.path.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(record,ensure_ascii=False)+'\n')


class Session:
    def __init__(self,session_id=None,initial=None):
        self.id = session_id or uuid.uuid4().hex
        self.state = deepcopy(EMPTY_STATE)
        self.version = 0
        self.history = []
        if initial:
            self.update(initial)

    def update(self,patch):
        schema = TOOLS[0]['function']['parameters']['properties']['patch']
        errors = sorted(Draft202012Validator(schema).iter_errors(patch),key=lambda e:str(e.path))
        if errors:
            raise ValueError('; '.join(e.message for e in errors))
        new_state = {**deepcopy(self.state),**deepcopy(patch)}
        new_state['skin_condition'] = sorted(new_state['skin_condition'])
        self.state = new_state
        self.version += 1
        return {'ok':True,'version':self.version,'state':deepcopy(self.state)}


class Agent:
    def __init__(self,trace_path,base_url='http://127.0.0.1:18080',initial=None,fail_search=False,
                 model_client=None,model_id='qwen2.5-3b-instruct',model_description=None,additional_training=False):
        self.session = Session(initial=initial)
        self.base_url = base_url.rstrip('/')
        self.trace = Trace(trace_path)
        self.fail_search = fail_search
        self.max_steps = 6
        self.turn_start = 0
        self.model_client = model_client
        self.model_id = model_id
        self.trace.write('session_start',session_id=self.session.id,state=self.session.state,
                         model=model_description or 'Qwen2.5-3B-Instruct official Q4_K_M',additional_training=additional_training,
                         context_policy='latest explicit state + current-turn messages; full history retained in trace')

    def _request(self):
        system = SYSTEM.replace('{state}',json.dumps({'version':self.session.version,**self.session.state},ensure_ascii=False))
        payload = {'model':self.model_id,'messages':[{'role':'system','content':system}]+self.session.history[self.turn_start:],
                   'tools':TOOLS,'tool_choice':'auto','parallel_tool_calls':False,
                   'temperature':0,'seed':42,'max_tokens':384,'stream':False,'cache_prompt':False}
        started = time.perf_counter()
        if self.model_client is not None:
            result = self.model_client(payload)
        else:
            request = urllib.request.Request(self.base_url+'/v1/chat/completions',
                        data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=180) as response:
                result = json.load(response)
        elapsed = time.perf_counter()-started
        message = result['choices'][0]['message']
        self.trace.write('model_response',message=message,raw_generation=result.get('raw_generation'),usage=result.get('usage'),seconds=elapsed,
                         finish_reason=result['choices'][0].get('finish_reason'))
        if result['choices'][0].get('finish_reason')=='length':
            raise ValueError('Model output reached token limit; response is incomplete')
        return message

    def _execute(self,name,arguments):
        if name not in BY_NAME:
            return {'ok':False,'error':'unknown_tool'}
        errors = list(Draft202012Validator(BY_NAME[name]['parameters']).iter_errors(arguments))
        if errors:
            return {'ok':False,'error':'invalid_arguments','details':[e.message for e in errors]}
        if name == 'update_session_state':
            return self.session.update(arguments['patch'])
        if self.fail_search:
            return {'ok':False,'error':'fixture_kb_unavailable','documents':[]}
        documents = json.loads((ROOT/'data/fixtures/knowledge_base.json').read_text(encoding='utf-8'))
        selected = [d for d in documents if set(d['tags']) & set(arguments['skin_condition'])]
        return {'ok':True,'fixture':True,'received_arguments':arguments,'documents':selected,
                'notice':'합성 테스트 문서이며 의료 지식베이스가 아닙니다.'}

    def turn(self,text):
        before = deepcopy(self.session.state)
        self.trace.write('user',text=text,state_before=before,session_id=self.session.id)
        self.turn_start = len(self.session.history)
        self.session.history.append({'role':'user','content':text})
        events, attempted, started = [],set(),time.perf_counter()
        for step in range(self.max_steps):
            try:
                message = self._request()
            except (urllib.error.URLError,TimeoutError,ValueError,KeyError) as exc:
                self.trace.write('model_error',error=str(exc))
                return {'ok':False,'error':'model_request_failed','details':str(exc),'state':deepcopy(self.session.state),'calls':events}
            calls = message.get('tool_calls') or []
            clean = {'role':'assistant','content':message.get('content') or ''}
            if calls:
                clean['tool_calls'] = calls
            self.session.history.append(clean)
            if not calls:
                if not clean['content'].strip():
                    self.trace.write('empty_model_response')
                    return {'ok':False,'error':'empty_model_response','state':deepcopy(self.session.state),'calls':events}
                output = {'ok':True,'answer':clean['content'],'state':deepcopy(self.session.state),
                          'calls':events,'seconds':time.perf_counter()-started}
                self.trace.write('turn_complete',**output)
                return output
            if len(calls) > 1:
                self.trace.write('parallel_call_emitted',count=len(calls))
            for call in calls:
                fn = call.get('function',{})
                name = fn.get('name','')
                raw_args = fn.get('arguments','{}')
                try:
                    arguments = json.loads(raw_args) if isinstance(raw_args,str) else raw_args
                    if not isinstance(arguments,dict):
                        raise ValueError('arguments must be an object')
                    signature = json.dumps([name,arguments],sort_keys=True,ensure_ascii=False)
                    if len(calls) > 1:
                        result = {'ok':False,'error':'parallel_calls_not_allowed','hint':'한 번에 하나의 도구만 호출하세요.'}
                    elif signature in attempted:
                        result = {'ok':False,'error':'duplicate_call_blocked'}
                    else:
                        attempted.add(signature)
                        result = self._execute(name,arguments)
                except (ValueError,TypeError) as exc:
                    arguments,result = raw_args,{'ok':False,'error':'invalid_arguments','details':str(exc)}
                event = {'name':name,'arguments':arguments,'result':result,'state_after':deepcopy(self.session.state)}
                events.append(event)
                self.trace.write('tool_execution',**event)
                self.session.history.append({'role':'tool','tool_call_id':call.get('id',f'local_{step}'),
                                             'name':name,'content':json.dumps(result,ensure_ascii=False)})
        self.trace.write('step_limit',state=self.session.state)
        return {'ok':False,'error':'step_limit','state':deepcopy(self.session.state),'calls':events}
