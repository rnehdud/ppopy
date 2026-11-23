"""Inspect complete source prefixes; no training, execution, truncation or translation."""
import collections
import copy
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.build_tool_decision_mix_v1 import toolace_tools,parse_toolace_calls,tools_normalized,Rejected
from agent.generic_fixture_v41 import ASK,NONE
from agent.choice_agent_v1 import TOOL_QUESTION
from agent.decision_context_v37r1 import make_view

OUT=ROOT/'output/diagnostics/trajectory-source-audit-v51'
DATA=ROOT/'data/processed/trajectory-source-audit-v51'

def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def toolace_row(r):
    tools=toolace_tools(r['system']);names=[t['name'] for t in tools]
    marker='Here is a list of functions in JSON format that you can invoke:'
    head,suffix=r['system'].split(marker,1)
    suffix=suffix.lstrip();_,end=json.JSONDecoder().raw_decode(suffix)
    policy=head+suffix[end:]
    messages=[{'role':'system','content':policy}];pending=[];serial=0
    for m in r['conversations']:
        role=m['from'];text=m['value']
        if role=='assistant' and text.strip().startswith('['):
            calls=parse_toolace_calls(text,names)
            if len(calls)!=1:raise Rejected('parallel_calls')
            call=calls[0];serial+=1;cid='source_call_'+str(serial);pending.append(cid)
            messages.append({'role':'assistant','content':'','tool_calls':[{'id':cid,'function':{'name':call['name'],'arguments':call['arguments']}}]})
        elif role=='tool':
            if len(pending)!=1:raise Rejected('ambiguous_tool_result')
            messages.append({'role':'tool','tool_call_id':pending.pop(0),'content':text})
        else:messages.append({'role':role,'content':text})
    return tools,messages

def prefix_packet(messages):
    # Every preceding message survives: user request, policies/text in history,
    # and calls/results in events. No answer from the target message enters input.
    users=[i for i,m in enumerate(messages) if m['role']=='user']
    if not users:raise Rejected('no_user_request')
    current=users[-1];request=messages[current].get('content') or ''
    events=[];history=[];pending={}
    for i,m in enumerate(messages):
        if i==current:continue
        if m['role']=='assistant' and m.get('tool_calls'):
            if len(m['tool_calls'])!=1:raise Rejected('parallel_prefix')
            call=m['tool_calls'][0];fn=call['function'];args=fn['arguments']
            if isinstance(args,str):args=json.loads(args)
            if not isinstance(args,dict):raise Rejected('nonobject_arguments')
            pending[call['id']]={'tool':fn['name'],'arguments':args,'executed':True}
            if m.get('content'):history.append({'role':'assistant','content':m['content']})
        elif m['role']=='tool':
            cid=m.get('tool_call_id')
            if cid not in pending:raise Rejected('unmatched_tool_result')
            event=pending.pop(cid);value=m.get('content')
            try:value=json.loads(value) if isinstance(value,str) else value
            except ValueError:pass
            event['result']=value;events.append(event)
        else:history.append(copy.deepcopy(m))
    if pending:raise Rejected('unfinished_tool_round')
    return {'request':request,'state':{},'observations':{},'pending':{},'events':events,'history':history,'available_actions':[]}

def candidates(source,source_id,tools,messages,tokenizer):
    if not 2<=len(tools)<=12:raise Rejected('tool_count_outside_2_12')
    options={t['name']:t['description']+'\n도구 이름: '+t['name']+'\n입력 정의: '+stable(t['parameters']) for t in tools}
    if len(options)!=len(tools):raise Rejected('duplicate_tools')
    options.update(ask=ASK,none=NONE)
    for i,m in enumerate(messages):
        if m['role']!='assistant':continue
        if i==0 or messages[i-1]['role'] not in ('user','tool'):continue
        calls=m.get('tool_calls') or []
        if len(calls)>1:continue
        observed=calls[0]['function']['name'] if calls else 'terminal_text'
        if calls and observed not in options:continue
        # A free-text assistant response isn't automatically an END/ASK label.
        # Keep it for review only, and never silently label it as NONE.
        packet=prefix_packet(messages[:i]);keys=list(options)
        rng=random.Random(source+str(source_id)+':'+str(i));rng.shuffle(keys)
        selected={k:options[k] for k in keys};packet['available_actions']=keys
        view,meta=make_view(TOOL_QUESTION,selected,packet,tokenizer)
        typ='after_tool_call' if calls and messages[i-1]['role']=='tool' else 'initial_call' if calls else 'after_tool_text' if messages[i-1]['role']=='tool' else 'user_text'
        yield {'id':source+':'+str(source_id)+':'+str(i),'source':source,'source_id':str(source_id),'position':i,
            'kind':typ,'observed':observed,'question':view['question'],'options':view['options'],'context':view['context'],
            'tokens':meta['tokens'],'packet':packet,'source_target':m,'source_prefix':messages[:i],
            'tools':tools,'status':'source imitation candidate; no independent correctness label'}

def main():
    if OUT.exists() or DATA.exists():raise FileExistsError('V51 audit protected')
    from transformers import AutoTokenizer
    import pyarrow.parquet as pq
    tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True)
    tok.model_max_length=1000000
    OUT.mkdir(parents=True);DATA.mkdir(parents=True)
    sources={
        'toolace':ROOT/'data/raw/tool-decision-mix-v1/toolace.json',
        'nemotron':ROOT/'data/raw/tool-decision-mix-v1/nemotron.jsonl',
        'kotraj':ROOT/'data/raw/kotraj-v02/train-00000-of-00001.parquet'}
    stats={};good=[]
    for source,path in sources.items():
        if source=='toolace':rows=json.loads(path.read_text(encoding='utf-8'))
        elif source=='kotraj':rows=pq.read_table(path).to_pylist()
        else:rows=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s]
        counts=collections.Counter();tool_names=set()
        for index,row in enumerate(rows):
            counts['source_rows']+=1
            try:
                if source=='toolace':tools,messages=toolace_row(row);sid=index
                elif source=='kotraj':
                    if row['verify_status']!='verified':counts['not_source_verified']+=1;continue
                    tools=tools_normalized(json.loads(row['tools']));messages=json.loads(row['messages']);sid=row['id']
                else:tools=tools_normalized(row['tools']);messages=row['messages'];sid=row.get('uuid',index)
                for r in candidates(source,sid,tools,messages,tok):
                    counts[r['kind']]+=1
                    counts[r['kind']+('_within512' if r['tokens']<=512 else '_over512')]+=1
                    if r['tokens']<=512:
                        good.append(r);tool_names.update(t['name'] for t in tools)
            except (Rejected,ValueError,TypeError,KeyError) as exc:counts['rejected:'+str(exc)[:80]]+=1
            if (index+1)%1000==0:print('V51 AUDIT',source,index+1,'/',len(rows),flush=True)
        stats[source]={'counts':dict(counts),'eligible_tool_names':len(tool_names),'source_sha256':sha(path)}
        print(source,stats[source],flush=True)
    with (DATA/'candidates.jsonl').open('w',encoding='utf-8') as f:
        for r in good:f.write(stable(r)+'\n')
    sample=[]
    for source in sources:
        for kind in ('after_tool_call','after_tool_text'):
            pool=sorted([r for r in good if r['source']==source and r['kind']==kind],key=lambda r:hashlib.sha256(r['id'].encode()).hexdigest())
            sample+=pool[:5]
    save(DATA/'review30.json',sample)
    save(OUT/'audit.json',{'sources':stats,'eligible_rows':len(good),'sample_rows':len(sample),
        'conversion':'Same seven-field Korean packet and candidate format as V41; preserve complete source prefix, parameters and policies. State={} means no source state provided, not fabricated state.',
        'limitations':'Observed calls are provisional labels; free text is NOT labelled NONE or ASK. No execution or external effects. English sources not translated. No training.',
        'files':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),DATA/'candidates.jsonl',DATA/'review30.json']}})
    print('V51 AUDIT COMPLETE',len(good),flush=True)

if __name__=='__main__':main()
