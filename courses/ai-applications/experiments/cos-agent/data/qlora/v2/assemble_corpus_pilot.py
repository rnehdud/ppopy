"""개정 2의 고정 입력·별도 응답을 조립하고 변경 이력을 남겨요."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
COS=HERE.parents[2]
sys.path.insert(0,str(COS/'scripts'))
import validate_qlora_dataset as validator
from refresh_corpus_pilot import sha, OUT, CORPUS_COMMIT

def assemble():
    inputs=json.loads((HERE/'pilot_24_inputs.json').read_text(encoding='utf-8'))
    responses=json.loads((HERE/'pilot_24_responses.json').read_text(encoding='utf-8'))
    revision=inputs.get('plan_revision',2)
    archive=COS/inputs.get('previous_archive','outputs/qlora_v3_pilot_20261125/revision_02/before')
    use_local_history=(archive/'pilot_24.jsonl').exists() and '--no-local-history' not in sys.argv
    old_rows={r['id']:r for r in (json.loads(s) for s in (archive/'pilot_24.jsonl').read_text(encoding='utf-8').splitlines())} if use_local_history else {}
    previous_log=json.loads((HERE/'pilot_24_change_log.json').read_text(encoding='utf-8'))
    published_changes={c['id']:c for c in previous_log['changes']}
    assert len(inputs['cases'])==24 and set(responses)=={c['id'] for c in inputs['cases']}
    rows=[]; changes=[]
    for case in inputs['cases']:
        req=case['request']; rid=case['id']
        assert sha(req)==case['input_sha256'],rid
        validator.SLMRequest.model_validate(req)
        row={k:deepcopy(case[k]) for k in ['id','scenario_id','group_id','scenario_family_id','split','mode','pilot_bucket','domains','card_ids','is_hard_negative','hard_negative_type','chunk_origins']}
        row.update({'messages':[{'role':'system','content':validator.SYSTEM_PROMPT_SOLUTION_HOLD},
                                {'role':'user','content':json.dumps(req,ensure_ascii=False)},
                                {'role':'assistant','content':responses[rid]}],
                    'allowed_evidence_refs':req['allowed_evidence_refs'],'distractor_refs':req['distractor_refs'],
                    'provenance':{'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,
                                  'generator_model':'gpt-6','critic_model':None,'critic_status':'unreviewed','human_review':'unreviewed'}})
        old=old_rows.get(rid)
        if old is not None:
            changes.append({'id':rid,'before_input_sha256':sha(json.loads(old['messages'][1]['content'])),
                        'after_input_sha256':case['input_sha256'],
                        'after_assistant_sha256':hashlib.sha256(responses[rid].encode('utf-8')).hexdigest(),
                        'input_changed':json.loads(old['messages'][1]['content'])!=req,
                        'answer_changed':old['messages'][2]['content']!=responses[rid],
                        'reason':'사용자 발화·확인 관찰·시스템 근거를 분리했어요. RAG 문단과 인용은 보존하고 제품 ID·버전 확인은 카탈로그 근거에 두었어요.' if revision>=3 else 'Tier 1 코퍼스 문단을 반영했어요.'})
        else:
            published=published_changes[rid]
            assert published['after_input_sha256']==case['input_sha256'], '공유 변경 이력과 입력이 달라요: '+rid
            assert published['after_assistant_sha256']==hashlib.sha256(responses[rid].encode('utf-8')).hexdigest(), '공유 변경 이력과 응답이 달라요: '+rid
            changes.append(published)
        rows.append(row)
    (HERE/'pilot_24.jsonl').write_bytes((''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)).encode('utf-8'))
    change_log={'revision':revision,'corpus_commit':CORPUS_COMMIT,'official_PPO42_pool_received':False,
                'before_archive':str(archive.relative_to(COS)),'changes':changes}
    (HERE/'pilot_24_change_log.json').write_bytes((json.dumps(change_log,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    lines=[f'# 파일럿 개정 {revision} · 발화·관찰·시스템 근거·응답 raw', '', '개발 미리보기 전용 · production_enabled=false · 사람/Critic 미검수', '',
           '최신 PPO-37의 Step 1 샘플 문헌 허용 범위로 갱신했어요. 아래 자료는 검수 PASS가 아니며 공식 PPO-42 풀 인계 완료도 아니에요.', '',
           '코퍼스 고정 커밋: `'+CORPUS_COMMIT+'` · 대상 학습 모델: `Qwen/Qwen3-4B-Instruct-2507`','']
    for case,row in zip(inputs['cases'],rows):
        lines += [f"## {case['id']} · {case['title']}", '', f"버킷 `{case['pilot_bucket']}` / 분할 `{case['split']}`", '',
                  '### 자연스러운 합성 사용자 발화','',case['scenario_raw'],'',
                  '### 별도 사용자 확인과 관찰 출처 raw','','```json',json.dumps({'prior_user_confirmations':case.get('prior_user_confirmations',[]),'observation_trace':case.get('observation_trace',{}),'system_context':case.get('system_context',{})},ensure_ascii=False,indent=2),'```','',
                  '### 실제 모델 입력 raw','','```json',json.dumps(case['request'],ensure_ascii=False,indent=2),'```','',
                  '입력 SHA-256: `'+case['input_sha256']+'`','','### 생성 응답 raw','',row['messages'][2]['content'],'',
                  '사람 검수: unreviewed / Critic: unreviewed','']
    (HERE/'pilot_24_review.md').write_bytes(('\n'.join(lines)).encode('utf-8'))
    print(f'개정 {revision} 조립 완료: 24턴. 입력 변경 {sum(c["input_changed"] for c in changes)}건 / 답변 변경 {sum(c["answer_changed"] for c in changes)}건. 검수 승인은 부여하지 않았어요.')

def main():
    if len(sys.argv)>1 and sys.argv[1]!='assemble':
        raise SystemExit('고정 입력을 덮어쓸 수 없어요. 재조립은 assemble 명령을 사용해요.')
    assemble()

if __name__=='__main__':
    main()
