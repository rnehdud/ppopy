"""Summarize real device samples by actual execution timestamps, never model-only VRAM."""
import argparse,csv,datetime,json,statistics,hashlib
from pathlib import Path
from common import dump,read_rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--samples',required=True)
    p.add_argument('--events',required=True);a=p.parse_args();root=Path(a.run)
    logs=read_rows(root/'training_log.jsonl')
    raw_events=Path(a.events).read_bytes()
    event_text=raw_events.decode('utf-16' if raw_events.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    events=[json.loads(l) for l in event_text.splitlines() if l.startswith('{')]
    samples=list(csv.DictReader(Path(a.samples).open(encoding='utf-8')))
    for s in samples:s['timestamp_ms']=datetime.datetime.fromisoformat(s['time_utc']).timestamp()*1000
    windows={'training_optimizer_interval':(logs[0]['timestamp_ms'],logs[-1]['timestamp_ms'])}
    for i,e in enumerate(events[:-1]):
        if e['stage'] in {'throughput_probe','vllm_quality','http_benchmark'}:
            windows[e['stage']]=(e['timestamp_ms'],events[i+1]['timestamp_ms'])
    results={}
    for stage,(start,end) in windows.items():
        selected=[s for s in samples if start<=s['timestamp_ms']<=end]
        memory=[float(s['memory_used_mib']) for s in selected]
        utilization=[float(s['gpu_util_percent']) for s in selected]
        results[stage]={'sample_count':len(selected),'start_ms':start,'end_ms':end,
            'whole_gpu_memory_used_mib':{'min':min(memory),'median':statistics.median(memory),'max':max(memory)} if memory else None,
            'whole_gpu_util_percent':{'median':statistics.median(utilization),'max':max(utilization)} if utilization else None}
    dump(root/'vram_summary.json',{'measurement_scope':'Entire GPU including desktop/other apps; 2s sampling does not capture every transient peak',
        'phases':results,'training_torch_peak_allocated_mib':max(r['peak_allocated_mib'] for r in logs),
        'training_torch_peak_reserved_mib':max(r['peak_reserved_mib'] for r in logs),
        'sampler_sha256':hashlib.sha256(Path(a.samples).read_bytes()).hexdigest(),
        'rag_two_model_coload_measured':False})
    print(json.dumps({'phases':{k:v['sample_count'] for k,v in results.items()},'model_only_occupancy_claimed':False}))

if __name__=='__main__':main()
