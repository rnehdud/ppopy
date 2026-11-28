"""3b8e4ca의 검수 이력과 현재 행 해시를 대조해 재검수 요청을 만들어요.

기존 Gemini 결과를 고치거나 새 PASS를 생성하지 않아요. 변경된 행은
이전 판정과 관계없이 새 해시로 재검수를 요청해요.
"""
from __future__ import annotations
import hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path
COS=Path(__file__).resolve().parents[1]
REPO=COS.parents[3]
sys.path.insert(0,str(COS/'scripts'))
from build_nlu_v1_step2 import content_hash
H=COS/'data/nlu/v1'
PREFIX='courses/ai-applications/experiments/cos-agent/data/nlu/v1/'
BASE='3b8e4ca'
def readlines(raw):return [json.loads(line) for line in raw.decode('utf-8').splitlines()]
def gitfile(rel):return subprocess.check_output(['git','show',BASE+':'+PREFIX+rel],cwd=REPO)
def dump(path,data,jsonl=False):
    path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data) if jsonl else json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def ids(start,end):return {f'nlu-step2-{i:04d}' for i in range(start,end+1)}
def main():
    oldrows={r['id']:r for r in readlines(gitfile('nlu_sft_v1.jsonl'))}
    oldrequests={r['row_id']:r for r in readlines(gitfile('reviews/step2_critic_requests.jsonl'))}
    newrows={r['id']:r for r in readlines((H/'nlu_sft_v1.jsonl').read_bytes())}
    newrequests={r['row_id']:r for r in readlines((H/'reviews/step2_critic_requests.jsonl').read_bytes())}
    criticpath=H/'reviews/step2_cross_model_critic.jsonl'
    assert criticpath.read_bytes()==gitfile('reviews/step2_cross_model_critic.jsonl')
    assert (H/'reviews/step2_cross_model_critic_summary.md').read_bytes()==gitfile('reviews/step2_cross_model_critic_summary.md')
    critic={r['row_id']:r for r in readlines(criticpath.read_bytes())}
    assert len(oldrows)==len(newrows)==len(critic)==len(newrequests)==980
    assert oldrows.keys()==newrows.keys()==critic.keys()==newrequests.keys()
    changed={rid for rid in oldrows if content_hash(oldrows[rid])!=content_hash(newrows[rid])}
    core=ids(414,420)|ids(491,497)|ids(757,763)|{'nlu-step2-0042','nlu-step2-0791'}
    collateral={'nlu-step2-0099','nlu-step2-0102','nlu-step2-0105'}
    accepted=ids(407,413)|ids(533,546)
    assert len(core)==23 and changed==core|collateral
    assert len(accepted)==21 and not accepted&changed
    assert Counter(critic[r]['verdict'] for r in core)=={'FAIL':9,'REVIEW':14}
    assert all(critic[r]['verdict']=='PASS' for r in collateral)
    changes=[];dispositions=[];recheck=[]
    for rid in sorted(oldrows):
        old=oldrows[rid];new=newrows[rid];prior=critic[rid]
        assert content_hash(old)==prior['content_sha256']==oldrequests[rid]['content_sha256']
        assert content_hash(new)==newrequests[rid]['content_sha256']
        assert all(old[k]==new[k] for k in ['id','scenario_family_id','split','primary_bucket','provenance','runtime_invariants'])
        assert json.loads(new['messages'][2]['content'])['confirmed_by_user'] is False
        assert new['provenance']['human_review']=='unreviewed'
        if rid not in changed:
            assert old==new
            if rid in accepted:
                assert prior['verdict']=='REVIEW'
                dispositions.append(dict(row_id=rid,content_sha256=content_hash(new),
                    prior_critic_verdict='REVIEW',disposition='PASS 수용 확정 · 데이터 변경 없음',
                    authority='사용자가 전달한 PPO-46 검수 후속 요청에서 확정',
                    policy='단발 비도포는 unknown' if rid in ids(407,413) else '타인 중단/고려는 stopped/considering 유지',
                    original_critic_file_unchanged=True,human_approved=False))
            continue
        before=json.loads(old['messages'][1]['content']);after=json.loads(new['messages'][1]['content'])
        beforeout=json.loads(old['messages'][2]['content']);afterout=json.loads(new['messages'][2]['content'])
        group='요청한 수정 23행' if rid in core else '공통 atom 원문 정렬로 함께 변경된 기존 PASS 3행'
        reason='손바닥 혼합 원문과 슬롯 값의 범위를 일치시킴' if rid in {'nlu-step2-0042','nlu-step2-0791'} else '도포 중 일부 부위 누락으로 원문·제품 사용 상태를 통일함'
        changes.append(dict(row_id=rid,group=group,reason=reason,prior_critic_verdict=prior['verdict'],
            before_content_sha256=content_hash(old),after_content_sha256=content_hash(new),
            before_request=before,after_request=after,before_expected=beforeout,after_expected=afterout,
            recheck_status='pending',human_approved=False))
        request=dict(newrequests[rid])
        request.update(recheck_reason=reason,recheck_group=group,prior_content_sha256=content_hash(old),
                       prior_critic_verdict=prior['verdict'],critic_status='unreviewed')
        recheck.append(request)
    dump(H/'reviews/step2_recheck_requests.jsonl',recheck,True)
    dump(H/'reviews/step2_recheck_core23.jsonl',[r for r in recheck if r['row_id'] in core],True)
    dump(H/'reviews/step2_recheck_additional3.jsonl',[r for r in recheck if r['row_id'] in collateral],True)
    dump(H/'reviews/step2_corrections_raw.jsonl',changes,True)
    dump(H/'reviews/step2_policy_acceptance.jsonl',dispositions,True)
    matched_pass=sum(r not in changed and c['verdict']=='PASS' for r,c in critic.items())
    assert matched_pass==933
    summary=dict(base_commit=subprocess.check_output(['git','rev-parse',BASE],cwd=REPO,text=True).strip(),
      previous_critic_counts=dict(Counter(c['verdict'] for c in critic.values())),
      previous_critic_file_sha256=hashlib.sha256(criticpath.read_bytes()).hexdigest(),
      previous_critic_file_preserved=True,dataset_sha256=hashlib.sha256((H/'nlu_sft_v1.jsonl').read_bytes()).hexdigest(),
      total_rows=980,changed_rows=26,requested_core_rows=23,additional_shared_atom_rows=3,unchanged_rows=954,
      unchanged_prior_pass_hash_matches=933,unchanged_review_rows_accepted_by_user_policy=21,
      changed_rows_pending_recheck=26,changed_rows_inheriting_previous_pass=0,
      core_changed_ids=sorted(core),additional_changed_ids=sorted(collateral),
      policy_accepted_unchanged_ids=sorted(accepted),current_version_cross_model_recheck_complete=False,human_approved=False)
    dump(H/'validation/step2_correction_manifest.json',summary)
    # 생성기의 false는 현재 버전의 전수 검수 미완료를 뜻해요. 이전 실제 검수 이력은 명시해요.
    for name in ['step2_generation_manifest.json','step2_audit.json']:
        path=H/'validation'/name
        record=json.loads(path.read_text(encoding='utf-8'))
        record['cross_model_critic_scope']='현재 데이터 버전의 전수 재검수 완료 여부'
        record['prior_version_cross_model_critic_received']=True
        record['current_changed_rows_pending_recheck']=26
        record['correction_manifest']='step2_correction_manifest.json'
        dump(path,record)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
