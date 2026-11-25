"""Replay all 90 development prompts on one real WSL vLLM NF4 backbone.

Quality evaluation uses a separate 120s ceiling, not the application's 15s SLA.
Application latency/fallback is measured separately by benchmark_http.py.
"""
import argparse,asyncio,hashlib,json,math,statistics,time,sys
from pathlib import Path
from common import read_rows,dump,deterministic_metrics
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1];sys.path.insert(0,str(COS))

async def run(a):
    import httpx
    root=Path(a.run);losses=json.loads((root/'loss_summaries.json').read_text(encoding='utf-8'))
    cfg=json.loads((root/'config.json').read_text(encoding='utf-8'))
    rows=[r for r in read_rows(COS/'data/qlora/v2/qlora_solution_hold_v2.jsonl') if r['split']=='val_internal']
    assert len(rows)==90
    results=[]
    async with httpx.AsyncClient(timeout=120) as client:
        models=(await client.get(a.base_url+'/models')).raise_for_status().json()
        dump(root/'vllm_model_inventory.json',models)
        for model,loss,directory in [('ppopy-base-nf4',losses['base'],root/'base'),
                *[(f"ppopy-epoch-{e['epoch']}",e,root/f"epoch-{e['epoch']}"/'evaluation') for e in losses['epochs']]]:
            directory.mkdir(parents=True,exist_ok=True);path=directory/'predictions.jsonl'
            records=read_rows(path) if path.exists() else []
            assert [r['row_id'] for r in records]==[r['id'] for r in rows[:len(records)]]
            for index,row in enumerate(rows):
                if index<len(records):continue
                started=time.perf_counter()
                response=await client.post(a.base_url+'/chat/completions',json={
                    'model':model,'messages':row['messages'][:-1],'temperature':0.,
                    'max_tokens':cfg['max_new_tokens'],'stream':False})
                response.raise_for_status();payload=response.json();choice=payload['choices'][0]
                text=choice['message']['content'];assert isinstance(text,str)
                record={'row_id':row['id'],'mode':row['mode'],'split':row['split'],'model':model,
                    'text':text,'content_sha256':hashlib.sha256(text.encode()).hexdigest(),
                    'timestamp_ms':int(time.time()*1000),'latency_s':time.perf_counter()-started,
                    'generated_tokens':payload.get('usage',{}).get('completion_tokens'),
                    'finish_reason':choice['finish_reason'],'finished_eos':choice['finish_reason']=='stop',
                    'http_status':response.status_code,'http_quality_timeout_s':120,
                    'usage':payload.get('usage'),'metrics':deterministic_metrics(row,text)}
                with path.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
                records.append(record)
                print(json.dumps({'event':'vllm_quality','model':model,'done':index+1,'total':90,
                    'latency_s':round(record['latency_s'],2)}),flush=True)
            keys=['invalid_citation','kb_citation','distractor_id_citation','solution_missing_citation','hold_instruction_candidate','empty_response']
            lat=sorted(r['latency_s'] for r in records)
            summary={**loss,'counts':{k:sum(r['metrics'][k] for r in records) for k in keys},
                'deterministic_flagged_rows':sum(any(r['metrics'][k] for k in keys) or bool(r['metrics']['guardrail_flags']) for r in records),
                'length_limited_rows':sum(r['finish_reason']=='length' for r in records),
                'solution_rows':60,'hold_rows':30,'distractor_rows':20,
                'latency_s':{'p50':statistics.median(lat),'p95':lat[math.ceil(len(lat)*.95)-1]},
                'generation_backend':'WSL vLLM; same inflight NF4 backbone for all three aliases',
                'generation':{'do_sample':False,'max_new_tokens':cfg['max_new_tokens']},
                'semantic_review_status':'pending actual input/reference/candidate review'}
            dump(directory/'summary.json',summary);results.append(summary)
    best=min(results[1:],key=lambda s:(s['deterministic_flagged_rows'],s['val_token_loss']))
    dump(root/'selection.json',{'checkpoint':f"epoch-{best['epoch']}",'policy':cfg['selection'],
        'base':results[0],'epochs':results[1:],'semantic_review_pending':True,
        'val_internal_used_for_selection':True,'independent_final_test':False,
        'upload_executed':False,'training_executed':True,
        'loss_backend':'Windows Transformers NF4 double quantization',
        'generation_backend':'WSL vLLM inflight NF4; generation backend is distinct from loss backend'})
    print('QUALITY_EVALUATION_COMPLETE',json.dumps({'checkpoint':f"epoch-{best['epoch']}"}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--base-url',default='http://127.0.0.1:8018/v1')
    asyncio.run(run(p.parse_args()))
