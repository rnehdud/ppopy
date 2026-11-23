"""Evaluate the saved v67 QLoRA adapter on internal val only.

Run from the POC07 workspace. No test reader, no fine-tuning, no calls to real
tools. Source policy JSON, prompt template and yes-minus-no match Kaggle.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'kaggle/qwen_v67_reranker'))
from common import prepare,read_rows,encode,sha,summarize

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--limit',type=int,default=221)
    p.add_argument('--output',type=Path,default=ROOT/'output/v67-poc-evaluation.json')
    p.add_argument('--verify-only',action='store_true')
    args=p.parse_args()
    data=ROOT/'data/v67/val_internal.jsonl'
    assert sha(data)=='c93110715e72b3dd925a7707fad53bc4648c585a1d78691c406592a24e6a4a67'
    rows=[prepare(r) for r in read_rows(data)]
    assert len(rows)==221 and 1<=args.limit<=221
    model_dir=ROOT/'models/qwen3-reranker-0.6b-e61197ed'
    adapter=ROOT/'adapters/qwen-v67-epoch03'
    for path in [model_dir/'model.safetensors',model_dir/'config.json',model_dir/'tokenizer.json',adapter/'adapter_model.safetensors',adapter/'adapter_config.json']:
        if not path.is_file():raise FileNotFoundError(str(path))
    if args.verify_only:
        print(json.dumps({'inputs_present':True,'val_rows':221,'weights_present':True,'model_not_loaded':True,'test_read':False},indent=2));return
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
    from peft import PeftModel,prepare_model_for_kbit_training
    from torch.nn.attention import sdpa_kernel,SDPBackend
    import transformers.integrations.sdpa_attention as sdpa_integration
    sdpa_integration.use_gqa_in_sdpa=lambda attention_mask,key:False
    if not torch.cuda.is_available():raise RuntimeError('CUDA GPU is required; no CPU fallback')
    tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForCausalLM.from_pretrained(model_dir,quantization_config=quant,torch_dtype=torch.float16,
        device_map={'':0},attn_implementation='sdpa',local_files_only=True,trust_remote_code=False)
    base.config.use_cache=False;base=prepare_model_for_kbit_training(base,use_gradient_checkpointing=False)
    model=PeftModel.from_pretrained(base,adapter,is_trainable=False).eval()
    no=tokenizer.convert_tokens_to_ids('no');yes=tokenizer.convert_tokens_to_ids('yes')
    records=[]
    with torch.inference_mode(),sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION):
        for i,row in enumerate(rows[:args.limit],1):
            scores=[]
            for j,candidate in enumerate(row['candidates']):
                ids=encode(tokenizer,row,j)
                if len(ids)>8192:raise ValueError('Input exceeds8192, not truncated: '+row['id'])
                x=torch.tensor([ids],device='cuda')
                with torch.autocast('cuda',dtype=torch.float16):
                    y=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False,logits_to_keep=1).logits[0,-1,[no,yes]].float().cpu().tolist()
                scores.append({'action':candidate['action'],'target_id':candidate['target_id'],'score':y[1]-y[0]})
                del x;torch.cuda.empty_cache()
            chosen=max(scores,key=lambda x:x['score']);selected={k:chosen[k] for k in ['action','target_id']}
            records.append({'id':row['id'],'gold':row['gold'],'selected':selected,'scores':scores,'candidate_n':len(scores),
                'pair_correct':selected==row['gold'],'action_correct':selected['action']==row['gold']['action']})
            if i%10==0:print('val',i,'/',args.limit,'correct',sum(r['pair_correct'] for r in records),flush=True)
    previous50=set(json.loads((ROOT/'data/v67/previous50.json').read_text(encoding='utf8'))['ids'])
    summary=summarize(records,previous50)
    if args.limit!=221:summary['val_exceeds_90_percent']=None
    result={'summary':summary,'rows':records,'test_read':False,
            'note':'Validation label agreement only; no actual tool execution or independent clinical judgment.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print('SAVED',args.output,flush=True)

if __name__=='__main__':main()
