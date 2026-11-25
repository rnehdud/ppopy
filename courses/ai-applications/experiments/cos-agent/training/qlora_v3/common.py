"""Exact chat-prefix masking and assistant-position-only CE for memory-bounded QLoRA."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def read_rows(path):return [json.loads(l) for l in Path(path).read_text(encoding='utf-8').splitlines() if l.strip()]

def encode(row,tokenizer,max_length=2048):
    full=tokenizer.apply_chat_template(row['messages'],tokenize=True,add_generation_prompt=False)
    prefix=tokenizer.apply_chat_template(row['messages'][:-1],tokenize=True,add_generation_prompt=True)
    assert full[:len(prefix)]==prefix,row['id']
    assert len(full)<=max_length,(row['id'],len(full),'truncation forbidden')
    labels=[-100]*len(prefix)+full[len(prefix):]
    assert len(prefix)<len(full) and all(x==-100 for x in labels[:len(prefix)])
    return {'id':row['id'],'input_ids':full,'labels':labels,'prefix_length':len(prefix)}

def split_and_encode(rows,tokenizer,max_length):
    assert len(rows)==900 and len({r['id'] for r in rows})==900
    train=[r for r in rows if r['split']=='train'];val=[r for r in rows if r['split']=='val_internal']
    assert len(train)==810 and len(val)==90 and not({r['id'] for r in train}&{r['id'] for r in val})
    for field in ['scenario_family_id','group_id']:
        assert not({r[field] for r in train}&{r[field] for r in val}),field
    return train,val,{r['id']:encode(r,tokenizer,max_length) for r in rows}

def selected_position_loss(hidden,labels,head):
    """Exactly normal next-token CE(ignore_index=-100), without prompt-position vocab logits."""
    import torch.nn.functional as F
    shifted=labels[:,1:];valid=shifted.ne(-100)
    assert valid.any(),'no assistant targets'
    logits=head(hidden[:,:-1,:][valid])
    return F.cross_entropy(logits.float(),shifted[valid]),int(valid.sum().item())

def masked_loss(model,input_ids,labels,attention_mask):
    base=model.get_base_model() if hasattr(model,'get_base_model') else model
    hidden=base.model(input_ids=input_ids,attention_mask=attention_mask,use_cache=False,return_dict=True).last_hidden_state
    return selected_position_loss(hidden,labels,base.lm_head)

def deterministic_metrics(row,text):
    """Deterministic candidates only: absence of flags is NOT semantic fidelity proof."""
    req=json.loads(row['messages'][1]['content'])
    refs=set(re.findall(r'\[((?:ref|kb|catalog|alternative):[^\]\s]+)\]',text))
    allowed=set(req['allowed_evidence_refs']);distractors=set(req['distractor_refs'])
    from beauty_agent.v3_contracts import SLMRequest,SLMResponse
    from beauty_agent.guardrail.hard_guardrail import HardSafetyGuardrail
    response=SLMResponse(mode=row['mode'],content=text or '빈 응답',cited_evidence_refs=sorted(refs))
    flags=HardSafetyGuardrail().validate(SLMRequest.model_validate(req),response).flags
    return {'invalid_citation':bool(refs-allowed),'kb_citation':any(r.startswith('kb:') for r in refs),
            'distractor_id_citation':bool(refs&distractors),'solution_missing_citation':row['mode']=='solution' and not refs,
            'hold_instruction_candidate':row['mode']=='hold' and 'hold_recommendation' in flags,
            'guardrail_flags':flags,'empty_response':not text.strip(),
            'semantic_review_status':'pending; ID/regex checks cannot exclude indirect distractor leakage or fact invention'}
