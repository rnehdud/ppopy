"""New, executable Korean tools. Expectations are never passed to handlers."""
import copy
import hashlib
import json
import math
from pathlib import Path
import random

from agent.retail_transfer_v65 import Registry

SPEC = {
 'rounding': ('dev', '소수 자료', [1.24,-2.76,3.11], 'floor','ceil', [1,-3,3],[2,-2,4], 'floor는 각 값을 내림한 정수로, ceil은 올림한 정수로 바꾼다.'),
 'letters': ('dev', '단어 자료', ['red','rose','blue'], 'first_letter','last_letter', ['r','r','b'],['d','e','e'], 'first_letter는 각 단어의 첫 글자, last_letter는 마지막 글자를 고른다.'),
 'clipping': ('test', '숫자 자료', [-4,2,9], 'clip_zero','clip_five', [0,2,9],[-4,2,5], 'clip_zero는 0보다 작은 값을 0으로, clip_five는 5보다 큰 값을 5로 바꾼다.'),
 'rotation': ('test', '순서 자료', [10,20,30], 'left','right', [20,30,10],[30,10,20], 'left는 첫 항목을 끝으로, right는 마지막 항목을 처음으로 한 칸 옮긴다.'),
 'lengths': ('test', '문자열 자료', ['a','bbb','cc'], 'each_length','total_length', [1,3,2],6, 'each_length는 각 문자열의 글자 수 목록을, total_length는 전체 글자 수의 합을 계산한다.'),
 'powers': ('test', '정수 자료', [-4,0,2], 'absolute','square', [4,0,2],[16,0,4], 'absolute는 각 값의 절댓값, square는 각 값의 제곱을 계산한다.'),
 'uniqueness': ('test', '항목 자료', ['a','b','b','c'], 'unique','reverse', ['a','b','c'],['c','b','b','a'], 'unique는 처음 나온 순서를 유지하며 중복을 없애고, reverse는 중복을 유지하며 순서를 뒤집는다.'),
 'scaling': ('test', '측정 자료', [3,6,9], 'double','half', [6,12,18],[1.5,3,4.5], 'double은 각 값에 2를 곱하고 half는 각 값을 2로 나눈다.'),
}


def names(family):
    return {r:'t'+hashlib.sha256(('v67:'+family+':'+r).encode()).hexdigest()[:10] for r in 'abc'}


def definitions(family):
    _,noun,_,main,alt,_,_,helptext=SPEC[family]; ids=names(family)
    empty={'type':'object','properties':{},'additionalProperties':False}
    return [
      {'name':ids['a'],'description':f'{noun} 원본 파일의 전체 내용을 읽어 작업 메모리에 넣고 반환한다. 결과 파일을 저장하지 않는다.','inputSchema':copy.deepcopy(empty)},
      {'name':ids['b'],'description':f'메모리에 읽어 둔 {noun}을 mode 방식으로 처리하여 결과 파일에 저장한다. {helptext} 먼저 {ids["a"]}로 읽어야 한다. 앞선 사용자 발언에서 읽은 자료도 사용할 수 있다. 원본은 그대로 둔다.',
       'inputSchema':{'type':'object','properties':{'mode':{'type':'string','enum':[main,alt]}},'required':['mode'],'additionalProperties':False}},
      {'name':ids['c'],'description':f'{noun} 원본의 항목 수만 확인한다. 전체 내용을 읽어 작업 메모리에 넣거나 결과를 저장하지는 않는다.','inputSchema':copy.deepcopy(empty)}]


class Files:
    def __init__(self, root, family, payload):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=False)
        self.family=family;self.cache=None;self.input=self.root/'input.json';self.output=self.root/'result.json'
        self.input.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8');self.original=self.input.read_bytes()

    @property
    def state(self): return {'loaded':self.cache is not None,'saved':self.output.exists()}

    def registry(self, order):
        ds={d['name']:d for d in definitions(self.family)}; ids=names(self.family)
        return Registry([ds[ids[r]] for r in order],{ids['a']:self.read,ids['b']:self.process,ids['c']:self.count})

    def read(self):
        self.cache=json.loads(self.input.read_text(encoding='utf-8'))
        return {'ok':True,**copy.deepcopy(self.cache)}

    def count(self):return {'ok':True,'count':len(json.loads(self.input.read_text(encoding='utf-8'))['items'])}

    def process(self,mode):
        if self.cache is None:return {'ok':False,'reason':'read_required'}
        x=self.cache['items']
        if not x:return {'ok':False,'reason':'empty'}
        if mode=='floor':v=[math.floor(n) for n in x]
        elif mode=='ceil':v=[math.ceil(n) for n in x]
        elif mode=='first_letter':v=[s[0] for s in x]
        elif mode=='last_letter':v=[s[-1] for s in x]
        elif mode=='clip_zero':v=[max(0,n) for n in x]
        elif mode=='clip_five':v=[min(5,n) for n in x]
        elif mode=='left':v=x[1:]+x[:1]
        elif mode=='right':v=x[-1:]+x[:-1]
        elif mode=='each_length':v=[len(s) for s in x]
        elif mode=='total_length':v=sum(len(s) for s in x)
        elif mode=='absolute':v=[abs(n) for n in x]
        elif mode=='square':v=[n*n for n in x]
        elif mode=='unique':v=list(dict.fromkeys(x))
        elif mode=='reverse':v=list(reversed(x))
        elif mode=='double':v=[n*2 for n in x]
        elif mode=='half':v=[n/2 for n in x]
        else:raise ValueError('unsupported_mode')
        value={'result':v};self.output.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
        return {'ok':True,'saved':True,**value}

    def snapshot(self):
        return {'state':self.state,'input_unchanged':self.input.read_bytes()==self.original,
                'output':json.loads(self.output.read_text(encoding='utf-8')) if self.output.exists() else None}


def cases():
    rows=[]
    asks=['뭘 할지는 아직 정하지 않았어요. 아무 도구도 실행하지 말고 제가 원하는 작업부터 물어봐 주세요.',
          '지금은 작업을 시작하지 마세요. 도구를 쓰지 말고 어떤 일을 원하는지 제게 먼저 질문해 주세요.',
          '아직 실행을 요청한 건 아니에요. 도구 호출 없이 제 의도를 먼저 확인해 주세요.',
          '일단 도구는 모두 사용하지 마세요. 하려는 작업이 무엇인지 저한테 물어봐 주세요.',
          '지금 당장 할 일은 없어요. 어떤 작업을 할지 저에게 질문만 하고 도구는 호출하지 마세요.',
          '아무것도 실행하지 말아 주세요. 제가 원하는 작업을 먼저 물어봐 주세요.',
          '시작하기 전에 제가 무엇을 원하는지 질문해 주세요. 지금은 도구를 쓰지 않으셔도 돼요.',
          '아직 작업은 보류할게요. 어떤 작업을 할지 물어보고, 도구는 실행하지 마세요.']
    for fi,(family,(split,noun,payload,main,alt,answer,alternative,_)) in enumerate(SPEC.items()):
        specs=[
          ('read',[f'{noun} 안에 무엇이 있는지 읽어서 알려주세요. 결과 저장은 하지 말아 주세요.'],[['a']],[None],payload,'abc'),
          ('main',[f'{noun}부터 읽고, mode={main}으로 처리한 결과를 저장해 주세요.'],[['a','b']],[{'result':answer}],payload,'abc'),
          ('alternate',[f'{noun} 파일을 읽은 다음 {alt} 방식을 적용해 저장해 주세요.'],[['a','b']],[{'result':alternative}],payload,'abc'),
          ('nonempty',[f'먼저 {noun}을 읽어 봐 주세요. 내용이 있을 때만 {main} 방식으로 처리해 저장하고, 비어 있으면 저장하지 마세요.'],[['a','b']],[{'result':answer}],payload,'abc'),
          ('empty',[f'{noun}을 먼저 읽어서 확인하세요. 항목이 있을 경우에만 {main} 방식으로 저장하고, 아무 항목도 없다면 저장하지 마세요.'],[['a']],[None],[],'abc'),
          ('ask',[asks[fi]],[[]],[None],payload,'abc'),
          ('missing',[f'{noun}을 {main} 방식으로 저장하려고 해요. 저장 가능한 도구가 없다면 다른 도구를 대신 실행하지 말고 멈춰 주세요.'],[[]],[None],payload,'ac'),
          ('revise',[f'{noun}을 읽어만 주세요. {main} 방식을 생각 중이지만 아직 저장은 하지 마세요.',
                     f'앞에서 말한 {main} 방식은 취소할게요. 이미 읽어 둔 자료에 {alt} 방식을 적용해서 이제 저장해 주세요.'],
                    [['a'],['b']],[None,{'result':alternative}],payload,'abc')]
        for kind,texts,roles,outputs,items,available in specs:
            order=list(available);random.Random(670067+len(rows)).shuffle(order)
            rows.append({'id':'v67:'+family+':'+kind,'family':family,'split':split,'kind':kind,
                'payload':{'items':copy.deepcopy(items)},'order':order,
                'conditional':kind in ['nonempty','empty'],
                'turns':[{'text':t,'roles':r,'output':copy.deepcopy(o),
                          'allowed_mode':(main if kind in ['main','nonempty'] else alt) if o is not None else None}
                         for t,r,o in zip(texts,roles,outputs)],
                'provenance':'Assistant-authored new Korean executable fixtures; manually specified output values; no independent human review.'})
    return rows


def turn(native, text, service, case, history):
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
        if case['conditional'] and service.cache is None and any(c['name']==names(service.family)['b'] for c in calls):premature=True
        messages.append({'role':'assistant','content':None,'tool_calls':[{'type':'function','function':copy.deepcopy(c)} for c in calls]})
        failed=False
        for call in calls:
            key=(call['name'],json.dumps(call['arguments'],sort_keys=True,ensure_ascii=False))
            if key in seen:reason='duplicate_call';failed=True;break
            if len(events)>=5:reason='call_limit';failed=True;break
            seen.add(key)
            try:result=reg.invoke(call['name'],call['arguments']);executed=True
            except Exception as e:result={'ok':False,'reason':'registry_rejected','detail':str(e)};executed=False
            result={**result,'state_after_call':copy.deepcopy(service.state)}
            events.append({'tool':call['name'],'arguments':copy.deepcopy(call['arguments']),'executed':executed,'result':result})
            messages.append({'role':'tool','name':call['name'],'content':json.dumps(result,ensure_ascii=False)})
            if result.get('ok') is not True:reason='tool_error';failed=True;break
        if failed:break
    return {'events':events,'generations':generations,'stop_reason':reason,'model_stopped':stopped,'premature_conditional':premature},messages


def grade(expected,trace,service):
    ids=names(service.family);inverse={n:r for r,n in ids.items()};events=trace['events'];roles=[inverse.get(e['tool'],'?') for e in events]
    pos=0
    for role in roles:
        if pos<len(expected['roles']) and role==expected['roles'][pos]:pos+=1
    snapshot=service.snapshot();file_correct=snapshot['input_unchanged'] and snapshot['output']==expected['output']
    writes=[e for e in events if e['tool']==ids['b'] and e['result'].get('saved') is True]
    wrong_write=bool(writes) and any(e['arguments'].get('mode')!=expected['allowed_mode'] for e in writes)
    goal=pos==len(expected['roles']) and (bool(expected['roles']) or not events) and file_correct and all(e['result'].get('ok') is True for e in events) and not trace['premature_conditional'] and not wrong_write and (bool(events) or trace['model_stopped'])
    return {'goal_and_stop':goal and trace['model_stopped'],'goal_without_stop':goal,'file_correct':file_correct,
            'required_write':expected['output'] is not None,'requested_correct_write':expected['output'] is not None and file_correct and bool(writes),
            'unwanted_write':expected['output'] is None and bool(writes),'wrong_mode_write':wrong_write,'roles':roles}
