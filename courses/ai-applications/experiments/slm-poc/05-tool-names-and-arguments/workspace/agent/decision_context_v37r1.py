"""Flat lossless envelope: keep all V37 facts, remove envelope/array punctuation.

The optional state_table is self-describing; $state still references its entries.
Available action names use a space-separated string only when each name has no
whitespace. Otherwise the original list is retained. Both modes decode exactly.
"""
import copy
from agent.decision_context_v37 import encode as original_encode,decode as original_decode,FIELDS,REVERSE,stable,legacy_context


def encode(packet,pooled=False):
    names=packet['available_actions']
    if not isinstance(names,list) or any(not isinstance(k,str) for k in names):raise ValueError('Available actions must be a string list')
    encoded=original_encode(packet,pooled);result=encoded['data']
    if names and all(k and not any(c.isspace() for c in k) for k in names):result[FIELDS['available_actions']]=' '.join(names)
    if pooled:result['state_table']=encoded['state_table']
    return result


def decode(encoded):
    if set(encoded) not in [set(REVERSE),set(REVERSE)|{'state_table'}]:raise ValueError('Invalid flat envelope')
    data=copy.deepcopy(encoded);pool=data.pop('state_table',None)
    names=data[FIELDS['available_actions']]
    if isinstance(names,str):data[FIELDS['available_actions']]=names.split(' ')
    elif not isinstance(names,list):raise ValueError('Invalid available action list')
    old={'format':'literal' if pool is None else 'pooled','data':data}
    if pool is not None:old['state_table']=pool
    return original_decode(old)


def context(encoded):return stable(encoded)


def make_view(question,options,packet,tokenizer):
    choices=[]
    for pooled in [False,True]:
        encoded=encode(packet,pooled)
        if decode(encoded)!=packet:raise ValueError('Flat encoding lost information')
        ctx=context(encoded);n=max(map(len,tokenizer([question+' '+v for v in options.values()],[ctx]*len(options),truncation=False)['input_ids']))
        choices.append((n,pooled,encoded,ctx))
    n,pooled,encoded,ctx=min(choices,key=lambda x:(x[0],x[1]))
    return {'question':question,'options':copy.deepcopy(options),'context':ctx},{'tokens':n,'format':'pooled' if pooled else 'literal','envelope':'flat-v1','encoded':encoded,'literal_tokens':choices[0][0],'pooled_tokens':choices[1][0]}
