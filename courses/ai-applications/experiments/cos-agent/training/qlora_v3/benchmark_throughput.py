"""Paired local throughput probe against preserved sequential raw measurements.

This measures bulk evaluation speed, not single-user latency or semantic quality.
"""
import argparse,asyncio,hashlib,json,time,sys
from pathlib import Path
from common import read_rows,dump,deterministic_metrics
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1];sys.path.insert(0,str(COS))

async def run(a):
    import httpx
    baseline=read_rows(a.baseline)[16:24] # Fixed eight; exclude early adapter-loading probes.
    assert len(baseline)==8 and all(r['model']=='ppopy-base-nf4' for r in baseline)
    rows={r['id']:r for r in read_rows(COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl')}
    semaphore=asyncio.Semaphore(a.concurrency)
    async with httpx.AsyncClient(timeout=120,trust_env=False) as client:
        async def generate(prior):
            row=rows[prior['row_id']];assert row['split']=='val_internal'
            async with semaphore:
                start=time.perf_counter()
                response=await client.post(a.base_url+'/chat/completions',json={
                    'model':'ppopy-base-nf4','messages':row['messages'][:-1],
                    'temperature':0,'max_tokens':384,'stream':False})
                response.raise_for_status();payload=response.json();choice=payload['choices'][0]
                text=choice['message']['content']
                return {'row_id':row['id'],'text':text,'content_sha256':hashlib.sha256(text.encode()).hexdigest(),
                    'exact_text_match':text==prior['text'],'generated_tokens':payload['usage']['completion_tokens'],
                    'latency_s':time.perf_counter()-start,'finish_reason':choice['finish_reason'],
                    'metrics':deterministic_metrics(row,text),'baseline_text':prior['text'],
                    'baseline_generated_tokens':prior['generated_tokens'],'baseline_latency_s':prior['latency_s']}
        start=time.perf_counter();records=await asyncio.gather(*(generate(r) for r in baseline));elapsed=time.perf_counter()-start
    old_time=sum(r['latency_s'] for r in baseline);old_tokens=sum(r['generated_tokens'] for r in baseline)
    new_tokens=sum(r['generated_tokens'] for r in records)
    result={'rows':8,'concurrency':a.concurrency,'max_new_tokens':384,'temperature':0,
        'baseline_file_sha256':hashlib.sha256(Path(a.baseline).read_bytes()).hexdigest(),
        'dataset_sha256':hashlib.sha256((COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl').read_bytes()).hexdigest(),
        'baseline_concurrency':1,'baseline_summed_request_s':old_time,'parallel_wall_s':elapsed,
        'baseline_tokens_per_s':old_tokens/old_time,'parallel_tokens_per_s':new_tokens/elapsed,
        'token_throughput_ratio':(new_tokens/elapsed)/(old_tokens/old_time),
        'same_eight_prompts_wall_speedup':old_time/elapsed,
        'exact_text_matches':sum(r['exact_text_match'] for r in records),
        'semantic_quality_certified':False,'single_user_latency_SLA_measured':False,
        'limitations':'Same eight prompts, different times/shared desktop workload. Batch numerics and outputs may differ; no guarantee of identical text or future speed.',
        'records':records}
    dump(a.output,result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',required=True);p.add_argument('--output',required=True)
    p.add_argument('--concurrency',type=int,default=4);p.add_argument('--base-url',default='http://127.0.0.1:8018/v1')
    asyncio.run(run(p.parse_args()))
