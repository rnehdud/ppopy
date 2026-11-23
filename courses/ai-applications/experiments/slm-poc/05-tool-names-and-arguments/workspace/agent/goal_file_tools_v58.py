"""New session-local file tools. No labels, user-text routing, or external I/O."""
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from agent.live_tool_agent import ToolRegistry

FAMILIES=('usage','ingredients','symptoms')
EMPTY={'type':'object','properties':{},'additionalProperties':False}
OUTPUT={'type':'object','properties':{'ok':{'type':'boolean'}},'required':['ok'],'additionalProperties':True}

def identifiers(family):
    return {r:'z'+hashlib.sha256(('goal-files-v58:'+family+':'+r).encode()).hexdigest()[:10] for r in ('read','process','count')}

def definitions(family):
    ids=identifiers(family)
    content={
      'usage':[
        '현재 대화의 제품 사용 로그 파일을 읽어 시각 목록과 기준 시각을 작업 메모리에 보관하고 반환한다. 파일을 바꾸지 않는다.',
        '읽어 둔 사용 로그의 마지막 사용부터 기준 시각까지 경과한 분을 계산해 결과 파일에 저장한다.',
        '사용 로그의 원본 항목 수만 세어 반환한다. 상세 읽기나 결과 저장은 하지 않는다.'],
      'ingredients':[
        '현재 대화의 성분 목록 파일을 읽어 원본 목록을 작업 메모리에 보관하고 반환한다. 파일을 바꾸지 않는다.',
        '읽어 둔 성분 목록의 중복을 제거하되 처음 나온 순서를 보존하여 결과 파일에 저장한다.',
        '성분 파일의 원본 항목 수만 세어 반환한다. 상세 읽기나 결과 저장은 하지 않는다.'],
      'symptoms':[
        '현재 대화의 증상 이력 파일을 읽어 날짜별 기록을 작업 메모리에 보관하고 반환한다. 파일을 바꾸지 않는다.',
        '읽어 둔 증상 이력의 마지막 두 기록을 비교하여 값이 바뀐 항목의 전후 값을 결과 파일에 저장한다.',
        '증상 이력 파일의 원본 기록 수만 세어 반환한다. 상세 읽기나 결과 저장은 하지 않는다.']}
    result=[]
    for role,desc in zip(('read','process','count'),content[family]):
        if role=='process':desc+=' 읽은 자료가 없으면 오류이므로 먼저 '+ids['read']+'로 읽어야 한다. 지난 대화에서 읽은 자료도 사용할 수 있다.'
        result.append({'name':ids[role],'description':desc,'inputSchema':copy.deepcopy(EMPTY),'outputSchema':copy.deepcopy(OUTPUT),
            'execution_contract':{'requires':[],'not_after':[]}})
    return result

def derive(family,payload):
    entries=payload['entries']
    if family=='usage':
        latest=max(datetime.fromisoformat(r['at']) for r in entries)
        minutes=int((datetime.fromisoformat(payload['now'])-latest).total_seconds()/60)
        return {'elapsed_minutes':minutes}
    if family=='ingredients':return {'unique':list(dict.fromkeys(entries))}
    before,after=entries[-2:];keys=sorted(set(before['values'])|set(after['values']))
    return {'changes':{k:{'before':before['values'].get(k),'after':after['values'].get(k)} for k in keys if before['values'].get(k)!=after['values'].get(k)}}

class FileTools:
    def __init__(self,root,family,payload):
        if family not in FAMILIES:raise ValueError('Unknown service')
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=False)
        self.family=family;self.cache=None;self.version=0;self.calls=[]
        self.input=self.root/'input.json';self.output=self.root/'result.json'
        self.input.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
        self.initial_bytes=self.input.read_bytes()
    @property
    def state(self):return {'loaded':self.cache is not None,'saved':self.output.exists()}
    def read(self):
        self.calls.append('read');self.cache=json.loads(self.input.read_text(encoding='utf-8'))
        # Actual file content, not expected answers or synthesized model output.
        return {'ok':True,**copy.deepcopy(self.cache)}
    def process(self):
        self.calls.append('process')
        if self.cache is None:return {'ok':False,'reason':'read_required'}
        minimum=2 if self.family=='symptoms' else 1
        if len(self.cache['entries'])<minimum:return {'ok':False,'reason':'insufficient_entries'}
        result=derive(self.family,self.cache)
        self.output.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');self.version+=1
        return {'ok':True,'saved':'result.json',**result}
    def count(self):
        self.calls.append('count');payload=json.loads(self.input.read_text(encoding='utf-8'))
        return {'ok':True,'count':len(payload['entries'])}
    def registry(self,available=('read','process','count'),order=None):
        ids=identifiers(self.family);by={d['name']:d for d in definitions(self.family)}
        registry=ToolRegistry();order=list(available) if order is None else order
        if set(order)!=set(available):raise ValueError('Invalid public order')
        for role in order:registry.register(by[ids[role]],getattr(self,role))
        return registry
    def snapshot(self):
        return {'state':self.state,'input_unchanged':self.input.read_bytes()==self.initial_bytes,
            'output':json.loads(self.output.read_text(encoding='utf-8')) if self.output.exists() else None,
            'actual_handler_calls':list(self.calls)}
