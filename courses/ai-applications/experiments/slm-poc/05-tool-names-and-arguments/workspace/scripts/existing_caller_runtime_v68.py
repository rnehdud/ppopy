"""Technical adapter: native baseline messages preserved byte-for-byte."""
import copy
import hashlib
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import existing_caller_v68 as run
from scripts.korean_material_v67 import sha,write,MODEL,REV
AMEND=run.P/'runtime-amendment.json'
old_verify=run.verify

def messages_for(messages,old,new,policy):
    ms=copy.deepcopy(messages)
    if ms and ms[0]['role']=='system':
        original=ms[0]['content']
        if original.startswith(old):
            ms[0]['content']=new+('\n\n'+run.POLICY if policy else '')+original[len(old):]
        elif policy:ms[0]['content']=new+'\n\n'+run.POLICY+'\n\n'+original
    elif policy:ms.insert(0,{'role':'system','content':new+'\n\n'+run.POLICY})
    return ms

def generated(native,policy,cache=None):
    from transformers import AutoTokenizer
    small=AutoTokenizer.from_pretrained(MODEL,revision=REV,local_files_only=True)
    old=run.defaults(small);new=run.defaults(native.tokenizer)
    if hasattr(native,'v68_raw_generate'):raw=native.v68_raw_generate
    else:raw=native.generate;native.v68_raw_generate=raw
    def generate(messages,tools):
        ms=messages_for(messages,old,new,policy)
        ids=native.tokenizer.apply_chat_template(ms,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')['input_ids']
        key=hashlib.sha256(ids.numpy().tobytes()).hexdigest()
        if cache is not None and key in cache:
            g=copy.deepcopy(cache[key]);g['exact_input_replay']=True;return g['text'],g
        text,g=raw(ms,tools)
        if cache is not None:cache[key]=copy.deepcopy(g)
        g['exact_input_replay']=False;return text,g
    return generate

def verify():
    p=old_verify();a=run.read(AMEND)
    for name,h in a['files'].items():assert sha(ROOT/name)==h,name
    return p

if __name__=='__main__':
    if '--prepare' in sys.argv:
        old_verify();assert not (run.P/'started-dev.json').exists()
        from transformers import AutoTokenizer
        tok=AutoTokenizer.from_pretrained(MODEL,revision=REV,local_files_only=True);default=run.defaults(tok)
        ab=ROOT/'output/korean-native-v67/experiment/baseline';checked=0
        records=run.read(ab/'dev-public.json')+run.read(ab/'english-retention.json')
        gens=[r['generation'] for r in records]
        gens += [g for e in run.read(ab/'dev-files.json') for t in e['turns'] for g in t['trace']['generations']]
        for g in gens:
            assert messages_for(g['messages'],default,default,False)==g['messages'];checked+=1
        write(run.P/'baseline-message-preservation.json',{'measured_input_messages_checked':checked,
             'result':'Identical full message values, including source-policy trailing whitespace and absent/present system role. No model inference or final test read.'})
        paths=[Path(__file__),run.P/'baseline-message-preservation.json']
        write(AMEND,{'reason':'Before any F generation: preserve the unchanged native baseline exactly. Do not trim source-policy whitespace or insert an explicit system role when original tokenizer would inject it.',
               'F_model_outputs_seen':False,'files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
        print('V68 message-preservation amendment frozen;',checked,'existing inputs checked.')
    else:
        run.verify=verify;run.generated=generated
        if '--dev' in sys.argv:run.dev()
        elif '--final-baseline' in sys.argv:run.final(True)
        elif '--final-selected' in sys.argv:run.final(False)
        else:raise ValueError('Choose a phase')
