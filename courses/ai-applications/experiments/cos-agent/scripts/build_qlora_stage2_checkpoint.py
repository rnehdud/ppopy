"""독립 작성된 생성 배치를 500턴 체크포인트와 외부 검수 묶음으로 조립해요."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

COS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(COS/'scripts'))
from check_qlora_stage2_checkpoint import inspect,write_json

def jsonl(path,items):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in items)).encode('utf-8'))

def assemble_from_sources(data):
    inputs=[json.loads(l) for l in (data/'stage2_inputs_500.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    answers=json.loads((data/'stage2_answers_500.json').read_text(encoding='utf-8'))
    assert len(inputs)==len(answers)==500
    rows=[]
    for frozen in inputs:
        row=dict(frozen['row_without_assistant'])
        assert frozen['row_id']==row['id']
        assert hashlib.sha256(row['messages'][1]['content'].encode('utf-8')).hexdigest()==frozen['user_message_sha256']
        row['messages']=row['messages']+[{'role':'assistant','content':answers[row['id']]}]
        rows.append(row)
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,default=COS/'data/qlora/v2')
    parser.add_argument('--shard-root',type=Path,help='작성 배치를 처음 병합할 때만 지정해요. 재조립에는 공개된 고정 입력·답변을 사용해요.')
    parser.add_argument('--report-dir',type=Path,default=COS/'outputs/qlora_step2_20261125/merged')
    args=parser.parse_args();data=args.data_dir.resolve();data.mkdir(parents=True,exist_ok=True)
    destination=data/'qlora_solution_hold_v2_checkpoint_500.jsonl'
    shard_receipts=[]
    if args.shard_root:
        rows=[]
        quotas={'cleansing':170,'moisturizing':165,'sun_protection':165}
        for owner,n in quotas.items():
            source=args.shard_root/owner/'rows.jsonl'
            raw=source.read_bytes()
            assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw,owner
            shard=[json.loads(l) for l in raw.decode('utf-8').splitlines() if l.strip()]
            assert len(shard)==n,(owner,len(shard))
            rows.extend(shard)
            shard_receipts.append({'owner':owner,'rows':n,'sha256':hashlib.sha256(raw).hexdigest()})
        rows.sort(key=lambda r:(r['mode']=='hold',int(r['id'].rsplit('-',1)[1])))
        source_records=[];answers={}
        for row in rows:
            assert len(row['messages'])==3
            record=dict(row);record['messages']=row['messages'][:2]
            source_records.append({'row_id':row['id'],'user_message_sha256':hashlib.sha256(row['messages'][1]['content'].encode('utf-8')).hexdigest(),
                                   'row_without_assistant':record})
            answers[row['id']]=row['messages'][2]['content']
        jsonl(data/'stage2_inputs_500.jsonl',source_records)
        write_json(data/'stage2_answers_500.json',answers)
        # 작성 당시의 합성 발화·확인 기록은 학습 입력과 구분하여 보존해요.
        traces={'cleansing':'authoring_sidecar.jsonl','moisturizing':'synthetic_fact_traces.jsonl','sun_protection':'fact_trace.jsonl'}
        trace_index=[]
        for owner,name in traces.items():
            source=args.shard_root/owner/name
            records=[json.loads(l) for l in source.read_text(encoding='utf-8').splitlines() if l.strip()]
            owner_ids={r['id'] for r in rows if r['id'] in {x['id'] for x in records}}
            assert len(records)==quotas[owner] and {x['id'] for x in records}==owner_ids,owner
            target=data/'authoring'/f'{owner}_synthetic_fact_trace.jsonl'
            jsonl(target,records)
            trace_index.append({'owner':owner,'rows':len(records),'file':str(target.relative_to(data)).replace('\\','/'),
                                'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
        write_json(data/'authoring/fact_trace_manifest.json',{'scope':'합성 작성 기록이며 실제 사용자 기록이나 검수 승인 증거가 아니에요. 모델에 전달되는 정보는 stage2_inputs_500.jsonl에 있어요.',
                   'files':trace_index})
    else:
        rows=assemble_from_sources(data)
    jsonl(destination,rows)
    report,requests=inspect(destination,COS/'data/rag/chunks.jsonl',500)
    write_json(args.report_dir/'checkpoint_quality.json',report)
    if report['errors']:
        print(json.dumps({'error_count':len(report['errors']),'errors':report['errors'][:50]},ensure_ascii=False,indent=2))
        return 1
    # 여기는 검수 요청이지, decision/PASS가 들어 있는 검수 결과 파일이 아니에요.
    review_dir=data/'reviews'
    jsonl(review_dir/'stage2_500_critic_requests.jsonl',requests)
    batches=[]
    offset=0
    for i,size in enumerate([30]*7+[29]*10,1):
        batch=requests[offset:offset+size];assert len(batch)==size
        name=f'checkpoint_500_batch_{i:02d}.jsonl'
        jsonl(review_dir/'requests_500'/name,batch)
        batches.append({'file':name,'rows':size,'row_ids':[r['row_id'] for r in batch],
                        'sha256':hashlib.sha256((review_dir/'requests_500'/name).read_bytes()).hexdigest()})
        offset+=size
    assert offset==500
    write_json(review_dir/'stage2_500_critic_request_manifest.json',{'status':'awaiting_external_cross_model_critic',
        'dataset_sha256':report['dataset_sha256'],'pool_sha256':report['pool_sha256'],'rows':500,'batches':batches,
        'content_hash_function':'validate_qlora_dataset.compute_row_content_sha256',
        'local_critic_performed':False,'human_approval_fabricated':False})
    receipt={'checkpoint_rows':500,'stage2_target_rows':900,'remaining_rows':400,
             'dataset_sha256':report['dataset_sha256'],'pool_sha256':report['pool_sha256'],
             'generation_model':'gpt-6.2-sol','cross_model_critic_location':'다른 팀원의 디바이스',
             'local_cross_model_critic':False,'human_review':'unreviewed','final_training_approved':False,
             'modes':dict(Counter(r['mode'] for r in rows)),'splits':dict(Counter(r['split'] for r in rows)),
             'shards':shard_receipts,'check_scope':'이 조립 명령은 입력·풀 일치 검사예요. 공통 비율 검증과 외부 내용 검수는 별도로 실행해야 해요.'}
    # 재조립 시에는 최초 작성 배치 해시를 그대로 보존해요.
    receipt_file=data/'validation/stage2_500_handoff_receipt.json'
    if not shard_receipts and receipt_file.exists():
        previous=json.loads(receipt_file.read_text(encoding='utf-8'));receipt['shards']=previous.get('shards',[])
    write_json(receipt_file,receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k!='shards'},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
