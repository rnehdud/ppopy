"""Measure actual localhost completions and the repository's bounded SLM client separately."""
import argparse,asyncio,json,math,statistics,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1];sys.path.insert(0,str(COS))
from common import dump,read_rows,deterministic_metrics

async def run(args):
    import httpx
    from beauty_agent.v3_contracts import SLMRequest
    from beauty_agent.slm.openai_compat_client import OpenAICompatSLMClient
    rows=[r for r in read_rows(COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl') if r['split']=='val_internal']
    # Fixed spread across all nine held-out families, never a training row.
    chosen=rows[::10]
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True);records=[]
    for model in ['ppopy-base-nf4','ppopy-qlora-v3']:
        client=OpenAICompatSLMClient(args.base_url,model,max_tokens=384)
        for row in chosen:
            start=time.perf_counter();response=await client.generate(SLMRequest.model_validate(json.loads(row['messages'][1]['content'])))
            record={'row_id':row['id'],'model':model,'latency_s':time.perf_counter()-start,'provider':response.provider,
                'fallback_reason':response.fallback_reason,'content':response.content,
                'utf8_bytes':len(response.content.encode()),'metrics':deterministic_metrics(row,response.content),
                'timeout_limit_s':15,'response_limit_bytes':65536}
            records.append(record);dump(output/'http_records.json',records)
            print(json.dumps({k:v for k,v in record.items() if k not in ['content','metrics']}),flush=True)
    summaries={}
    for model in ['ppopy-base-nf4','ppopy-qlora-v3']:
        group=[r for r in records if r['model']==model];lat=sorted(r['latency_s'] for r in group)
        successes=sorted(r['latency_s'] for r in group if r['provider']!='rule_baseline_fallback')
        summaries[model]={'n':len(group),'p50_s':statistics.median(lat),'p95_s':lat[math.ceil(len(lat)*.95)-1],
            'successful_model_latency_s':{'n':len(successes),'p50':statistics.median(successes) if successes else None,
                'p95':successes[math.ceil(len(successes)*.95)-1] if successes else None},
            'fallback_count':sum(r['provider']=='rule_baseline_fallback' for r in group),
            'timeout_count':sum(r['fallback_reason']=='timeout' for r in group),
            'actual_model_response_count':sum(r['provider']!='rule_baseline_fallback' for r in group),
            'all_payloads_within_64KiB':all(r['utf8_bytes']<=65536 for r in group)}
    dump(output/'http_summary.json',{'backend':args.backend,'summaries':summaries,
        'measurement':'client-visible latency, including fallback; fallback is not counted as model success',
        'all_rows':'val_internal','production_enabled':False})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base-url',default='http://127.0.0.1:8018/v1');p.add_argument('--output',required=True)
    p.add_argument('--backend',default='vLLM 0.28.0 on WSL2; NF4 base + local LoRA')
    asyncio.run(run(p.parse_args()))
