"""Lossless decision-input renderer; no truncation, labels, action inference or scoring.

Repeated complete skin-state dictionaries may share a table entry. Every other
value, including errors, versions, arguments, history and unknown states survives.
The shortest of literal/pooled encodings is selected by the same tokenizer that
will be used for learning. This is a mechanical token budget choice, not a prompt
or model-output search. Both encodings decode into exactly the source packet.
"""
import copy,json
from collections import Counter
from agent.symptom_state_v1 import SYMPTOMS,VALUES

FIELDS={'request':'요청','state':'기록','observations':'판정','pending':'미반영','events':'실행','history':'이전','available_actions':'도구'}
REVERSE={v:k for k,v in FIELDS.items()}
MARKER='$state'


def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def full_state(x):return isinstance(x,dict) and set(x)==set(SYMPTOMS) and all(type(v) is str and v in VALUES for v in x.values())


def validate(packet):
    if set(packet)!=set(FIELDS):raise ValueError('Unexpected decision packet fields')
    # Fail rather than reinterpret literal data using the reserved reference key.
    def walk(x):
        if isinstance(x,dict):
            if MARKER in x:raise ValueError('Reserved state-reference key in source data')
            if any(type(k) is not str for k in x):raise ValueError('JSON object keys must be strings')
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(packet)
    if json.loads(stable(packet))!=packet:raise ValueError('Source packet must be JSON-compatible')


def encode(packet,pooled=False):
    validate(packet);data={FIELDS[k]:copy.deepcopy(v) for k,v in packet.items()}
    if not pooled:return {'format':'literal','data':data}
    counts=Counter()
    def count(x):
        if full_state(x):counts[stable(x)]+=1
        elif isinstance(x,dict):
            for v in x.values():count(v)
        elif isinstance(x,list):
            for v in x:count(v)
    count(data);keys=sorted(k for k,n in counts.items() if n>1);indices={k:i for i,k in enumerate(keys)}
    def pack(x):
        if full_state(x) and stable(x) in indices:return {MARKER:indices[stable(x)]}
        if isinstance(x,dict):return {k:pack(v) for k,v in x.items()}
        if isinstance(x,list):return [pack(v) for v in x]
        return copy.deepcopy(x)
    return {'format':'pooled','state_table':[json.loads(k) for k in keys],'data':pack(data)}


def decode(encoded):
    fmt=encoded.get('format')
    if fmt not in ['literal','pooled']:raise ValueError('Unknown decision input format')
    if set(encoded)!=(set(['format','data','state_table']) if fmt=='pooled' else set(['format','data'])):raise ValueError('Invalid encoded envelope')
    pool=encoded.get('state_table',[])
    if not isinstance(pool,list) or any(not full_state(s) for s in pool):raise ValueError('Invalid state table')
    def unpack(x):
        if isinstance(x,dict):
            if MARKER in x:
                i=x[MARKER]
                if set(x)!={MARKER} or fmt!='pooled' or type(i) is not int or not 0<=i<len(pool):raise ValueError('Invalid state reference')
                return copy.deepcopy(pool[i])
            return {k:unpack(v) for k,v in x.items()}
        if isinstance(x,list):return [unpack(v) for v in x]
        return copy.deepcopy(x)
    data=unpack(encoded['data'])
    if set(data)!=set(REVERSE):raise ValueError('Invalid data field mapping')
    return {REVERSE[k]:v for k,v in data.items()}


def context(encoded):return stable(encoded)


def make_view(question,options,packet,tokenizer):
    choices=[]
    for pooled in [False,True]:
        encoded=encode(packet,pooled)
        if decode(encoded)!=packet:raise ValueError('Lossless roundtrip failed')
        ctx=context(encoded)
        n=max(map(len,tokenizer([question+' '+v for v in options.values()],[ctx]*len(options),truncation=False)['input_ids']))
        choices.append((n,pooled,encoded,ctx))
    n,pooled,encoded,ctx=min(choices,key=lambda x:(x[0],x[1]))
    return {'question':question,'options':copy.deepcopy(options),'context':ctx}, {'tokens':n,'format':'pooled' if pooled else 'literal','encoded':encoded,'literal_tokens':choices[0][0],'pooled_tokens':choices[1][0]}


def legacy_context(packet):
    # Used only to prove that packet construction retained the old runtime facts.
    return '현재 기록: '+stable(packet['state'])+'\n사용자 발화: '+packet['request']+'\n이번 발화의 증상 판정: '+stable(packet['observations'])+'\n아직 반영되지 않은 변경: '+stable(packet['pending'])+'\n이번 요청의 실제 실행 결과: '+stable(packet['events'])+'\n최근 사용자 발화: '+stable(packet['history'])+'\n사용 가능한 동작:\n'+'\n'.join('- '+k for k in packet['available_actions'])
