"""Independent real-file services for fixed V60 development/final episodes."""
import copy,hashlib,json
from pathlib import Path
from agent.live_tool_agent import ToolRegistry
from agent.goal_file_tools_v58 import EMPTY,OUTPUT
from agent.generic_fixture_v41 import Session

# Handlers see session file contents only, never request text or grading labels.
SPECS={
 'sum':('금액 목록','금액을 모두 더한 합계를 저장한다.'),
 'range':('측정값 목록','최솟값과 최댓값을 저장한다.'),
 'positive':('정수 목록','양수만 원래 순서대로 골라 저장한다.'),
 'sort':('날짜 목록','날짜를 이른 순서로 정렬해 저장한다.'),
 'reverse':('문자 목록','목록의 순서를 거꾸로 바꿔 저장한다.'),
 'lengths':('단어 목록','각 단어의 글자 수를 같은 순서로 저장한다.'),
 'squares':('숫자 목록','각 숫자의 제곱을 같은 순서로 저장한다.'),
 'unique':('항목 목록','중복을 제거하고 처음 나온 순서로 저장한다.')}

def names(f):return {r:'u'+hashlib.sha256(('v60:'+f+':'+r).encode()).hexdigest()[:7] for r in ('a','b','c')}

def definitions(f):
    noun,op=SPECS[f];ids=names(f)
    texts=[f'현재 대화의 {noun} 파일 내용을 읽어 작업 메모리에 보관하고 반환한다. 파일은 변경하지 않는다.',
        f'읽은 {noun}으로 {op} 먼저 {ids["a"]}로 읽어야 한다. 이전 발언에서 읽은 자료도 쓸 수 있다. 원본은 변경하지 않는다.',
        f'{noun}의 원본 항목 수만 센다. 작업 메모리에 내용을 읽거나 결과를 저장하지 않는다.']
    return [{'name':ids[r],'description':d,'inputSchema':copy.deepcopy(EMPTY),'outputSchema':copy.deepcopy(OUTPUT),'execution_contract':{'requires':[],'not_after':[]}} for r,d in zip(('a','b','c'),texts)]

def calculate(f,x):
    if f=='sum':return {'sum':sum(x)}
    if f=='range':return {'min':min(x),'max':max(x)}
    if f=='positive':return {'positive':[n for n in x if n>0]}
    if f=='sort':return {'dates':sorted(x)}
    if f=='reverse':return {'reversed':x[::-1]}
    if f=='lengths':return {'lengths':[len(n) for n in x]}
    if f=='squares':return {'squares':[n*n for n in x]}
    if f=='unique':return {'unique':list(dict.fromkeys(x))}
    raise ValueError(f)

class Files:
    def __init__(self,root,family,payload):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=False)
        self.family=family;self.input=self.root/'input.json';self.output=self.root/'result.json'
        self.input.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8');self.original=self.input.read_bytes();self.cache=None
    @property
    def state(self):return {'loaded':self.cache is not None,'saved':self.output.exists()}
    def read(self):
        self.cache=json.loads(self.input.read_text(encoding='utf-8'));return {'ok':True,**copy.deepcopy(self.cache)}
    def process(self):
        if self.cache is None:return {'ok':False,'reason':'read_required'}
        if not self.cache['items']:return {'ok':False,'reason':'empty'}
        value=calculate(self.family,self.cache['items']);self.output.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
        return {'ok':True,'saved':True,**value}
    def count(self):return {'ok':True,'count':len(json.loads(self.input.read_text(encoding='utf-8'))['items'])}
    def registry(self,available,order):
        by={d['name']:d for d in definitions(self.family)};ids=names(self.family);reg=ToolRegistry()
        assert set(order)==set(available)
        for role in order:reg.register(by[ids[role]],{'a':self.read,'b':self.process,'c':self.count}[role])
        return reg
    def snapshot(self):return {'state':self.state,'input_unchanged':self.input.read_bytes()==self.original,'output':json.loads(self.output.read_text(encoding='utf-8')) if self.output.exists() else None}

class FileSession:
    def __init__(self,service,case,score,tokenizer):self.service=service;self.case=case;self.score=score;self.tokenizer=tokenizer;self.history=[]
    def session(self,text):
        c=self.case;reg=self.service.registry(c['available'],c['order'])
        public={'family':c['family'],'request':text,'initial':{},'binding':{},'definitions':reg.definitions(),
            'ids':names(c['family']),'available':c['order'],'history':copy.deepcopy(self.history[-2:]),'order_seed':c['order_seed']}
        s=Session(public,self.score,self.tokenizer);s.world=self.service;s.registry=reg;return s
    def turn(self,text):
        s=self.session(text);trace=s.run(max_steps=3);trace['model_inputs']=s.inputs
        self.history.append({'role':'user','content':text,'actual_tools':[{'tool':e['tool'],'ok':e['result'].get('ok')} for e in trace['events']]})
        return trace

def grade(turn,trace,service):
    snap=service.snapshot();events=trace.get('events',[]);ids=names(service.family);inverse={n:r for r,n in ids.items()}
    roles=[inverse.get(e['tool'],'unknown') for e in events];expected=turn['roles'];calls_ok=all(e['result'].get('ok') is True for e in events)
    # Evaluator only: mandatory operations in order; extra read-only calls are
    # counted separately, rather than erasing a correct final result.
    pos=0
    for role in roles:
        if pos<len(expected) and role==expected[pos]:pos+=1
    mandatory=pos==len(expected)
    no_call_ok=not events if not expected else True
    effect=snap['input_unchanged'] and snap['output']==turn['output']
    unwanted=bool(snap['output'] is not None and turn['output'] is None)
    selected=[s['choice'] for s in trace.get('steps',[])]
    illegal_attempt=False
    if not expected:illegal_attempt=any(n not in ('ask','none') for n in selected)
    # Duplicate attempted calls/handler errors remain failures even if the saved
    # value is right. Pure optional successful reads are an efficiency cost.
    goal=bool(trace.get('steps')) and mandatory and no_call_ok and effect and calls_ok and not illegal_attempt
    return {'goal_ok':goal,'goal_and_stop':goal and trace.get('model_stopped') is True,
        'path_and_stop':goal and roles==expected and trace.get('model_stopped') is True,
        'roles':roles,'file_correct':effect,'unwanted_write':unwanted,'input_unchanged':snap['input_unchanged'],
        'required_save':turn['output'] is not None,'saved_correctly':turn['output'] is not None and effect,
        'extra_calls':max(0,len(roles)-len(expected)),'stop':trace.get('stop_reason')}
