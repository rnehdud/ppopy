"""Real Transformers/NF4 inference with strict Qwen tool-call parsing."""
import copy
import json
import re
import time
import uuid


def parse_output(text):
    text=text.replace('<|im_end|>','').replace('<|endoftext|>','').strip()
    blocks=list(re.finditer(r'<tool_call>\s*(.*?)\s*</tool_call>',text,flags=re.DOTALL))
    calls=[]
    for match in blocks:
        value=json.loads(match[1])
        if not isinstance(value,dict) or not isinstance(value.get('name'),str) or not isinstance(value.get('arguments'),dict):
            raise ValueError('Invalid native tool call')
        calls.append({'id':'call_'+uuid.uuid4().hex[:12],'type':'function',
                      'function':{'name':value['name'],'arguments':json.dumps(value['arguments'],ensure_ascii=False)}})
    content=re.sub(r'<tool_call>.*?</tool_call>','',text,flags=re.DOTALL).strip()
    if '<tool_call>' in content or '</tool_call>' in content:
        raise ValueError('Truncated native tool call')
    message={'role':'assistant','content':content}
    if calls:
        message['tool_calls']=calls
    return message


class HFClient:
    def __init__(self,model,tokenizer,max_new_tokens=160):
        self.model=model
        self.tokenizer=tokenizer
        self.max_new_tokens=max_new_tokens
        self.dtype=model.get_input_embeddings().weight.dtype

    def __call__(self,payload):
        import torch
        messages=copy.deepcopy(payload['messages'])
        for message in messages:
            for call in message.get('tool_calls',[]):
                args=call['function'].get('arguments',{})
                if isinstance(args,str):
                    call['function']['arguments']=json.loads(args)
        rendered=self.tokenizer.apply_chat_template(messages,tools=payload['tools'],tokenize=False,add_generation_prompt=True)
        inputs=self.tokenizer(rendered,return_tensors='pt',add_special_tokens=False).to('cuda')
        if inputs['input_ids'].shape[1]+self.max_new_tokens>4096:
            raise ValueError('Context limit exceeded; no silent truncation')
        self.model.eval()
        with torch.inference_mode(),torch.autocast('cuda',dtype=self.dtype):
            output=self.model.generate(**inputs,max_new_tokens=self.max_new_tokens,do_sample=False,
                         pad_token_id=self.tokenizer.pad_token_id,eos_token_id=self.tokenizer.eos_token_id,
                         use_cache=True)
        completion=output[0,inputs['input_ids'].shape[1]:]
        raw=self.tokenizer.decode(completion,skip_special_tokens=False)
        try:
            message=parse_output(raw)
        except ValueError as exc:
            raise ValueError(f'Invalid native output: {raw[:300]}') from exc
        ended_with_eos=len(completion)>0 and int(completion[-1])==self.tokenizer.eos_token_id
        return {'choices':[{'message':message,'finish_reason':'length' if len(completion)>=self.max_new_tokens and not ended_with_eos else 'stop'}],
                'usage':{'prompt_tokens':inputs['input_ids'].shape[1],'completion_tokens':len(completion)},
                'raw_generation':raw}


def load_base(root):
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
    from peft import prepare_model_for_kbit_training
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA PyTorch is required; CPU-only PyTorch is not a training environment')
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    tokenizer=AutoTokenizer.from_pretrained(str(root/'models/qwen2.5-3b-instruct/tokenizer'),local_files_only=True)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype)
    model=AutoModelForCausalLM.from_pretrained(str(root/'models/qwen2.5-3b-nf4'),local_files_only=True,
              trust_remote_code=False,device_map={'':0},torch_dtype=dtype,quantization_config=quant,
              attn_implementation='sdpa',low_cpu_mem_usage=True)
    model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True)
    # Frozen large tied embeddings do not need fp32; keep norms in fp32.
    # The identical policy is used for baseline, training and adapter reload.
    model.get_input_embeddings().to(dtype=dtype)
    model.get_output_embeddings().to(dtype=dtype)
    model.config.use_cache=False
    return model,tokenizer,dtype
