"""Same random50 v67 internal-val rows; pinned rerankers; no training/test use."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import gc
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import statistics
import subprocess
import time

import requests

ROOT=Path(__file__).resolve().parents[1]
SEARCH=ROOT/'output/v67-model-search-20261116'
OUT=ROOT/'output/v67-two-rerankers-val50-v2-memory'
PREPARED=ROOT/'output/v67-roberta-internal-val-v1/prepared-inputs.json'
SOURCE=ROOT.parent/'ppopy/courses/ai-applications/experiments/cos-agent/data/action_policy/v67/v67-sft-val-internal.jsonl'
SEED=20261116
INSTRUCTION='Given the complete state and user request, judge whether the proposed action and target are the appropriate next action. Do not invent facts or re-ask confirmed information.'
PREFIX='<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
SUFFIX='<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
MODELS=[('Qwen/Qwen3-Reranker-0.6B','qwen3-reranker-0.6b-e61197ed','qwen',32768),
        ('dragonkue/bge-reranker-v2-m3-ko','dragon-bge-reranker-v2-m3-ko-2aca5884','bge',8192)]

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()
def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)

def setup(spec):
    repo,dirname,kind,limit=spec
    meta=read(SEARCH/repo.replace('/','__')/'metadata.json');revision=meta['revision']
    dest=ROOT/'models'/dirname;dest.mkdir(exist_ok=True)
    origin=SEARCH/repo.replace('/','__')
    for source in origin.iterdir():
        if source.name in ['config.json','tokenizer_config.json','tokenizer.json','vocab.json','merges.txt','special_tokens_map.json','sentencepiece.bpe.model']:
            target=dest/source.name
            if target.exists():assert sha(target)==sha(source)
            else:shutil.copyfile(source,target)
    session=requests.Session();session.trust_env=False
    response=session.get(f'https://huggingface.co/api/models/{repo}/revision/{revision}?blobs=true',timeout=40);response.raise_for_status()
    file=next(r for r in response.json()['siblings'] if r['rfilename']=='model.safetensors')
    expected=file['lfs']['sha256'];size=file['size']
    weight=dest/'model.safetensors'
    if weight.exists():assert weight.stat().st_size==size and sha(weight)==expected
    else:
        partial=dest/'model.safetensors.partial';last_report=0
        for attempt in range(1,4):
            start=partial.stat().st_size if partial.exists() else 0
            if start==size:break
            try:
                headers={'Range':f'bytes={start}-'} if start else {}
                url=f'https://huggingface.co/{repo}/resolve/{revision}/model.safetensors?download=true&v67validate=50'
                with session.get(url,headers=headers,stream=True,timeout=(15,45)) as r:
                    r.raise_for_status()
                    if start and r.status_code!=206:start=0
                    if r.status_code==206:assert r.headers.get('Content-Range','').startswith(f'bytes {start}-')
                    with partial.open('ab' if start else 'wb') as f:
                        count=start
                        for chunk in r.iter_content(chunk_size=2**20):
                            if not chunk:continue
                            f.write(chunk);count+=len(chunk)
                            if count-last_report>=128*2**20:
                                print('DOWNLOAD',kind,round(100*count/size,1),'%',flush=True);last_report=count
                if partial.stat().st_size==size:break
            except requests.RequestException as exc:
                print('DOWNLOAD retry',kind,attempt,type(exc).__name__,flush=True)
                if attempt==3:raise
        assert partial.stat().st_size==size and sha(partial)==expected,'Weight size/hash mismatch; no load'
        partial.replace(weight)
    manifest={'repo':repo,'revision':revision,'filename':'model.safetensors','sha256':expected,'bytes':size,
        'additional_training':False,'config_sha256':sha(dest/'config.json'),'tokenizer_sha256':sha(dest/'tokenizer.json')}
    save(dest/'manifest.json',manifest)
    print('VERIFIED MODEL',kind,size,'bytes',flush=True)
    return kind,manifest

def aggregate(rows):
    valid=[r for r in rows if not r.get('error')]
    times=[r['seconds'] for r in valid]
    return {'n':len(rows),'pair_correct':sum(r['pair_correct'] for r in rows),'action_correct':sum(r['action_correct'] for r in rows),
        'full_input_fit':sum(r['all_candidates_fit'] for r in rows),'errors':sum(bool(r.get('error')) for r in rows),
        'median_seconds_per_request':statistics.median(times) if times else None,
        'mean_seconds_per_request':statistics.mean(times) if times else None,
        'peak_torch_allocated_mib':max((r.get('peak_torch_allocated_mib',0) for r in rows),default=0),
        'peak_torch_reserved_mib':max((r.get('peak_torch_reserved_mib',0) for r in rows),default=0),
        'multiple_candidates':{'n':sum(r['candidate_n']>1 for r in rows),'pair_correct':sum(r['pair_correct'] for r in rows if r['candidate_n']>1)}}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['all','qwen','bge'],default='all')
    args=parser.parse_args()
    selected_specs=[spec for spec in MODELS if args.model=='all' or spec[2]==args.model]
    OUT.mkdir(parents=True,exist_ok=True)
    prepared={r['id']:r for r in read(PREPARED)}
    ids=random.Random(SEED).sample(sorted(prepared),50)
    assert len(set(ids))==50
    source={r['id']:r for r in [json.loads(line) for line in SOURCE.read_text(encoding='utf-8').splitlines() if line.strip()]}
    selection={'method':'Uniform random.sample(sorted(all221 IDs),50); no gold labels or outputs used to choose rows.',
        'seed':SEED,'ids':ids,'source_sha256':sha(SOURCE),'prepared_sha256':sha(PREPARED),'test_used':False}
    if (OUT/'selection.json').exists():assert read(OUT/'selection.json')==selection
    save(OUT/'selection.json',selection)
    gold={i:{k:source[i]['output'][k] for k in ['action','target_id']} for i in ids}
    save(OUT/'gold-not-model-input.json',gold)
    import torch
    import transformers
    from torch.nn.attention import sdpa_kernel, SDPBackend
    # This Windows build has no FlashAttention; fused efficient SDPA cannot
    # directly process GQA. Use Transformers' own repeat_kv branch instead.
    # Repeated K/V are mathematically the same heads; no weights/input changes.
    import transformers.integrations.sdpa_attention as sdpa_integration
    sdpa_integration.use_gqa_in_sdpa = lambda attention_mask, key: False
    from transformers import AutoTokenizer,AutoModelForCausalLM,AutoModelForSequenceClassification
    torch.set_num_threads(4);torch.manual_seed(SEED)
    if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable, not silently substituting CPU')
    protocol={'script_sha256':sha(Path(__file__)),'selection':selection,'n':50,
        'models':[{'repo':repo,'revision':read(SEARCH/repo.replace('/','__')/'metadata.json')['revision'],'kind':kind,'limit':limit} for repo,dirname,kind,limit in MODELS],
        'input': 'Same full source input JSON and same enabled action/target candidate headers from previous prepared set. No fields dropped or truncated.',
        'instruction':INSTRUCTION,'qwen_prefix':PREFIX,'qwen_suffix':SUFFIX,
        'qwen_score':'One prefill, no generated text. Last-token yes-minus-no logit. logits_to_keep=1 and use_cache=False.',
        'bge_score':'One prefill scalar classification logit per candidate.',
        'selection_rule':'Argmax score over all enabled candidates. Fixed input-independent candidate shuffle inherited from prepared inputs.',
        'metric':'Exact dataset (action,target_id) equality; action-only also counted. Arguments/reasons/tool execution not scored.',
        'precision':'Both unquantized float16 on same GPU, forced EFFICIENT_ATTENTION SDPA, candidate batch1. Transformers repeat_kv branch replaces direct GQA for Windows kernel compatibility. Clear unused allocator cache after each candidate. No adapters or training.',
        'timing':'After a separate warmup, per request wall time includes all candidates tokenization + CUDA scoring + CPU result transfer and argmax. Excludes model load/download/disk logs.',
        'memory':'Torch peak allocated and reserved GPU memory, loaded model included. Excludes CUDA context/non-PyTorch allocations; not total device usage.',
        'versions':{'torch':torch.__version__,'transformers':transformers.__version__},'gpu':torch.cuda.get_device_name(0),
        'limits':'50 previously seen internal-val inputs; not independent external test or clinical correctness. One fixed input instruction, not best-of prompt tuning.'}
    if (OUT/'protocol.json').exists():assert read(OUT/'protocol.json')==protocol,'Frozen protocol changed'
    save(OUT/'protocol.json',protocol)
    manifests=read(OUT/'weight-manifests.json') if (OUT/'weight-manifests.json').exists() else {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(setup,spec) for spec in selected_specs]):
            kind,manifest=future.result();manifests[kind]=manifest;save(OUT/'weight-manifests.json',manifests)
    all_summaries=read(OUT/'summary.json') if (OUT/'summary.json').exists() else {}
    for repo,dirname,kind,limit in selected_specs:
        folder=ROOT/'models'/dirname
        tokenizer=AutoTokenizer.from_pretrained(folder,local_files_only=True,trust_remote_code=False)
        started=time.perf_counter()
        cls=AutoModelForCausalLM if kind=='qwen' else AutoModelForSequenceClassification
        model=cls.from_pretrained(folder,torch_dtype=torch.float16,device_map={'':0},attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).eval()
        load_seconds=time.perf_counter()-started
        yes=tokenizer.convert_tokens_to_ids('yes') if kind=='qwen' else None
        no=tokenizer.convert_tokens_to_ids('no') if kind=='qwen' else None
        prefix=tokenizer.encode(PREFIX,add_special_tokens=False) if kind=='qwen' else None
        suffix=tokenizer.encode(SUFFIX,add_special_tokens=False) if kind=='qwen' else None
        def encode(first,context):
            if kind=='qwen':
                formatted=f'<Instruct>: {INSTRUCTION}\n<Query>: {first}\n<Document>: {context}'
                values=prefix+tokenizer.encode(formatted,add_special_tokens=False,truncation=False)+suffix
                return {'input_ids':values,'attention_mask':[1]*len(values)}
            return tokenizer(INSTRUCTION+'\n'+first,context,truncation=False,add_special_tokens=True,return_token_type_ids=False)
        def score(batch):
            with torch.inference_mode(), sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION):
                outputs=model(**batch,use_cache=False,logits_to_keep=1) if kind=='qwen' else model(**batch)
                if kind=='qwen':
                    values=outputs.logits[0,-1,[no,yes]].float().cpu().tolist()
                    return values[1]-values[0],{'no_logit':values[0],'yes_logit':values[1]}
                return float(outputs.logits[0,0].float().cpu()),None
        warm=encode('synthetic candidate: no action','synthetic state: no request')
        warm_batch={k:torch.tensor([v],device='cuda') for k,v in warm.items()}
        score(warm_batch);del warm_batch
        torch.cuda.synchronize();torch.cuda.empty_cache()
        results=[];evaluation_started=time.perf_counter()
        print('READY',kind,'loaded seconds',round(load_seconds,1),flush=True)
        try:
            for index,identifier in enumerate(ids,1):
                path=OUT/kind/'cases'/(identifier+'.json')
                if path.exists():
                    r=read(path);assert r['gold']==gold[identifier];results.append(r);continue
                item=prepared[identifier]
                assert json.loads(item['context'])==source[identifier]['input']
                torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
                t0=time.perf_counter()
                result={'id':identifier,'gold':gold[identifier],'candidate_n':len(item['candidates']),
                    'all_candidates_fit':False,'pair_correct':False,'action_correct':False}
                try:
                    encoded=[encode(first,item['context']) for first in item['first_texts']]
                    lengths=[len(batch['input_ids']) for batch in encoded]
                    result['candidate_tokens']=lengths
                    result['all_candidates_fit']=max(lengths)<=limit
                    if not result['all_candidates_fit']:raise ValueError('Input over limit; no truncation or candidate removal')
                    scores=[]
                    for candidate,encoding in zip(item['candidates'],encoded):
                        batch={k:torch.tensor([v],device='cuda') for k,v in encoding.items()}
                        value,details=score(batch);del batch;torch.cuda.empty_cache()
                        scores.append({'action':candidate['action'],'target_id':candidate['target_id'],'score':value,'details':details})
                    assert all(torch.isfinite(torch.tensor(r['score'])).item() for r in scores)
                    chosen=max(range(len(scores)),key=lambda k:scores[k]['score'])
                    selected={k:scores[chosen][k] for k in ['action','target_id']}
                    result.update({'selected':selected,'scores':scores,'pair_correct':selected==gold[identifier],
                        'action_correct':selected['action']==gold[identifier]['action']})
                except Exception as exc:
                    result['error']=type(exc).__name__+': '+str(exc)
                    if 'out of memory' in str(exc).lower():torch.cuda.empty_cache()
                torch.cuda.synchronize();result['seconds']=time.perf_counter()-t0
                result['peak_torch_allocated_mib']=torch.cuda.max_memory_allocated()/2**20
                result['peak_torch_reserved_mib']=torch.cuda.max_memory_reserved()/2**20
                save(path,result);results.append(result)
                save(OUT/'progress.json',{'model':kind,'completed':index,'total':50,'summary':aggregate(results)})
                if index%5==0 or result.get('error'):print(kind,index,'/50','pair',sum(r['pair_correct'] for r in results),'errors',sum(bool(r.get('error')) for r in results),'seconds',round(time.perf_counter()-evaluation_started),flush=True)
        finally:
            del model;gc.collect();torch.cuda.empty_cache();torch.cuda.synchronize()
        summary=aggregate(results);summary.update({'repo':repo,'load_seconds':load_seconds,'evaluation_seconds':time.perf_counter()-evaluation_started,
            'pair_accuracy':summary['pair_correct']/50,'action_accuracy':summary['action_correct']/50})
        save(OUT/kind/'summary.json',summary);all_summaries[kind]=summary
        print('FINISHED',kind,json.dumps(summary,ensure_ascii=False),flush=True)
    save(OUT/'summary.json',all_summaries)
    print('DONE selected models released; no demo started or training run.',flush=True)

if __name__=='__main__':main()
