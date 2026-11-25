"""500턴 원본 검수를 보존하고 답변 14건 수정과 신규 400턴을 조립해요."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,sys
from copy import deepcopy
COS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(COS/'scripts'))
from check_qlora_stage2_checkpoint import inspect,write_json
from build_qlora_stage2_checkpoint import jsonl

REPLACEMENTS={
 'syn-sol-0040':[('아침에 두 번 덧발랐다고 밤에 리무버도 두 번 해야 하지는 않아요.','아침에 도포한 뒤 시간차를 두고 차단제를 덧발랐다고 해서 밤에 리무버도 두 번 해야 하지는 않아요.')],
 'syn-sol-0247':[('젤을 남은 근무 주간에 쓰더라도','크림 잔량이 적어 젤을 대신 쓰더라도')],
 'syn-sol-0530':[('아침의 눈부심을','이전에 말한 눈부심을')],
 'syn-hold-0006':[('아침에 알아챈 아래턱의 따가움이 오후를 지나 지금도 남아 있어요.','아침 세안 후 시작된 아래턱의 따가움이 오전과 오후에 이어 지금도 남아 있어요.'),('아침부터 저녁까지 사라지지 않았다고 설명해 주세요.','아침에 시작된 뒤 오전과 오후에도 계속됐고 지금도 남아 있다고 설명해 주세요.')],
 'syn-hold-0020':[('식사할 때 두드러졌지만 식사 때에만 나타난 것이 아니라고 알려 주세요.','이틀째 식사 전후에 가려움이 있었고 말을 하지 않을 때도 이어졌다고 알려 주세요.')],
 'syn-hold-0071':[('쉰내가 병 입구에만 있는 게 아니라 오늘 덜어 낸 로션 자체에서 처음 났으니, 그 용기의 품질 판단은 보류해요.','토출된 내용물에서 이전에는 없던 시큼한 냄새가 처음 났으니, 제품의 품질 판단은 보류해요.')],
 'syn-hold-0072':[('욕실장의 공기 냄새와 달리 손에 덜어 낸 크림에서 갑자기 페인트 같은 냄새가 난 점 때문에 판단을 보류해요.','주변 공간 냄새와 다른 화학적인 냄새가 하루 사이 손에 덜어 낸 내용물에서 생긴 점 때문에 판단을 보류해요.')],
 'syn-hold-0079':[('리필 직후에는 평소와 같았는데 오늘 펌프에서 나온 내용물에 식초 냄새가 새로 나서 보류해요.','리필 후 정상 기간을 거친 뒤 펌프에서 나온 내용물에 식초 같은 냄새가 새로 나서 보류해요.')],
 'syn-hold-0088':[('가운데 흰 띠','새 흰 띠')],
 'syn-hold-0089':[('리필이 같아도 세면대 쪽에 둔 통만 이전과 달리 두 층으로 나뉘었으니 그 통에 대한 판단은 보류해요.','리필에서 나눈 세면대 통만 이전과 달리 층이 새로 나뉘었으니 그 통에 대한 판단은 보류해요.'),('한 리필에서 나온 두 통 가운데 어느 통이 달라졌는지 제조사 품질 상담처에 정확히 전달해 확인받아요.','리필에서 나눈 통 가운데 세면대 통만 달라졌다는 점을 제조사 품질 상담처에 전달해 확인받아요.')],
 'syn-hold-0094':[('보습 크림이 누렇게 변해','제품 색이 하양에서 누런 쪽으로 변해')],
 'syn-hold-0096':[('토출된 처음 부분뿐만 아니라 용기 내의 연보라 로션도 전보다 색이 빠져 보여','토출된 로션과 용기 내 잔량 모두 전보다 색이 빠져 보여')],
 'syn-hold-0159':[('오전과 다르게 지금 여러 점이 갑자기 보인다고 하셨어요.','야외에서 막 돌아온 뒤 갑자기 시야에 여러 점이 보인다고 하셨어요.')],
 'syn-hold-0165':[('밤에 깬 뒤 더 심해진 흐름','밤에 더 심해져 가만히 있어도 심한 흐름')],
}

def read(path):return [json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
def main():
    p=argparse.ArgumentParser();p.add_argument('--shard-root',type=Path);a=p.parse_args()
    data=COS/'data/qlora/v2';reviews=data/'reviews'
    original=data/'qlora_solution_hold_v2_checkpoint_500.jsonl'
    old=read(original);critic=read(reviews/'stage2_500_critic.jsonl')
    assert len(old)==len(critic)==500
    critiques={r['row_id']:r for r in critic};assert len(critiques)==500
    old_report,old_requests=inspect(original,COS/'data/rag/chunks.jsonl',500)
    assert not old_report['errors'],old_report['errors']
    for r in old_requests:assert critiques[r['row_id']]['content_sha256']==r['content_sha256'],r['row_id']
    assert {r['row_id'] for r in critic if r['decision']=='FAIL'}==set(REPLACEMENTS)
    rows=deepcopy(old);corrections=[]
    for row in rows:
        if row['id'] not in REPLACEMENTS:continue
        before=row['messages'][2]['content'];after=before
        for source,target in REPLACEMENTS[row['id']]:
            assert after.count(source)==1,(row['id'],source)
            after=after.replace(source,target)
        row['messages'][2]['content']=after
        corrections.append({'row_id':row['id'],'original_critic':critiques[row['id']],
                            'raw_request':json.loads(row['messages'][1]['content']),
                            'before_answer':before,'after_answer':after,'revision_actor':'Codex coordinator','status':'awaiting_external_recheck'})
    remaining_source=data/'stage2_remaining_400.jsonl'
    if a.shard_root:
        new=[];traces=[]
        for owner,n,trace in [('cleansing_remaining',130,'authoring_sidecar.jsonl'),('moisturizing_remaining',135,'synthetic_fact_traces.jsonl'),('sun_remaining',135,'fact_trace.jsonl')]:
            batch=read(a.shard_root/owner/'rows.jsonl');assert len(batch)==n,(owner,len(batch));new+=batch
            raw_trace=read(a.shard_root/owner/trace)
            assert len(raw_trace)==n and {r['id'] for r in raw_trace}=={r['id'] for r in batch},owner
            jsonl(data/'authoring'/f'{owner}_synthetic_fact_trace.jsonl',raw_trace)
            traces.append({'owner':owner,'rows':n,'source_sha256':hashlib.sha256((a.shard_root/owner/'rows.jsonl').read_bytes()).hexdigest()})
        new.sort(key=lambda r:(r['mode']=='hold',int(r['id'].rsplit('-',1)[1])))
        jsonl(remaining_source,new);write_json(data/'authoring/remaining_400_receipt.json',{'shards':traces,'review_status':'unreviewed'})
    else:new=read(remaining_source)
    assert len(new)==400 and len({r['id'] for r in new})==400
    rows+=new;rows.sort(key=lambda r:(r['mode']=='hold',int(r['id'].rsplit('-',1)[1])))
    expected={f'syn-sol-{i:04d}' for i in range(1,691)}|{f'syn-hold-{i:04d}' for i in range(1,211)}
    assert len(rows)==900 and {r['id'] for r in rows}==expected
    target=data/'qlora_solution_hold_v2.jsonl';jsonl(target,rows)
    report,requests=inspect(target,COS/'data/rag/chunks.jsonl',900)
    write_json(data/'validation/stage2_900_quality.json',report)
    assert not report['errors'],report['errors']
    mapping={r['row_id']:r for r in requests}
    for c in corrections:c['before_content_sha256']=c['original_critic']['content_sha256'];c['after_content_sha256']=mapping[c['row_id']]['content_sha256']
    jsonl(reviews/'stage2_14_corrections.jsonl',corrections)
    todo=set(REPLACEMENTS)|{r['id'] for r in new};assert len(todo)==414
    requests=[r for r in requests if r['row_id'] in todo]
    for request in requests:
        rid=request['row_id']
        request['review_scope']='corrected_fact_distortion' if rid in REPLACEMENTS else 'new_synthetic'
        if rid in REPLACEMENTS:request['previous_critic']=critiques[rid]
    jsonl(reviews/'stage2_414_critic_requests.jsonl',requests)
    batches=[]
    start=0
    for i,size in enumerate([30]*8+[29]*6,1):
        batch=requests[start:start+size];start+=size;name=f'stage2_414_batch_{i:02d}.jsonl'
        path=reviews/'requests_414'/name;jsonl(path,batch)
        batches.append({'file':name,'rows':len(batch),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'row_ids':[r['row_id'] for r in batch]})
    unchanged=[c for c in critic if c['row_id'] not in todo]
    assert len(unchanged)==486
    for c in unchanged:assert c['decision']=='PASS' and c['content_sha256']==mapping[c['row_id']]['content_sha256']
    write_json(reviews/'stage2_414_request_manifest.json',{'status':'awaiting_external_cross_model_critic','total_rows':900,'original_unchanged_PASS':486,
        'generation_remaining_rows':0,'awaiting_external_review_rows':414,
        'changed_rows':14,'corrected_row_ids':sorted(REPLACEMENTS),'new_rows':400,'requested_rows':414,'dataset_sha256':report['dataset_sha256'],
        'original_500_sha256':old_report['dataset_sha256'],'pool_sha256':report['pool_sha256'],'batches':batches,
        'human_review':'unreviewed','final_training_approved':False})
    print(json.dumps({'rows':900,'requests':414,'modes':report['modes'],'splits':report['splits'],'errors':report['errors']},ensure_ascii=False))
if __name__=='__main__':main()
