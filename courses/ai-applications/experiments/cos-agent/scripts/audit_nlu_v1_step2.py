"""Step 2의 분포·불변식·정책 경계와 검수 요청 해시를 검사해요.

독립 의미 검수 결과가 아니며 기존 validate_nlu_dataset.py를 대체하지 않아요.
"""
from __future__ import annotations
import hashlib,json,re,subprocess,sys
from collections import Counter,defaultdict
from pathlib import Path
COS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(COS));sys.path.insert(0,str(COS/'scripts'))
from build_nlu_v1_step2 import CORE_SLOTS,BASE,content_hash
from beauty_agent.nlu_schema import ALLOWED_SYMPTOMS,ALLOWED_TOPICS,verify_nlu_extraction
from beauty_agent.v3_contracts import NLURequest,NLUExtractionResult
from beauty_agent.slm.prompt_builder import build_nlu_messages
H=COS/'data/nlu/v1'
def lines(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
def main():
    path=H/'nlu_sft_v1.jsonl';raw=path.read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw
    rows=lines(path);reviews=lines(H/'reviews/step2_critic_requests.jsonl')
    assert len(rows)==980 and len(reviews)==980
    byid={r['row_id']:r for r in reviews};assert len(byid)==980
    buckets=Counter();split_buckets=defaultdict(Counter);families=defaultdict(set)
    slot_counts=Counter();syms=Counter();persistence=Counter();usage=Counter();topics=Counter()
    slot_splits=defaultdict(Counter);texts=defaultdict(set);compact=defaultdict(set)
    policy=Counter();complex_rows=0;typo_rows=0;mixed_subjects=0
    for row in rows:
        rid=row['id'];req=NLURequest.model_validate_json(row['messages'][1]['content']);ext=NLUExtractionResult.model_validate_json(row['messages'][2]['content'])
        assert row['messages'][:2]==build_nlu_messages(req)
        verify_nlu_extraction(ext,request=req)
        assert req.allowed_variable_ids==CORE_SLOTS
        assert set(req.allowed_symptoms)==set(ALLOWED_SYMPTOMS) and set(req.allowed_topics)==set(ALLOWED_TOPICS)
        assert ext.confirmed_by_user is False
        assert row['provenance']['source_origin']=='new_synthetic'
        assert row['provenance']['human_review']==row['provenance']['critic_status']=='unreviewed'
        assert row['runtime_invariants']==dict(mode='development_preview',production_enabled=False,requires_approval=True,saved=False)
        review=byid[rid]
        assert content_hash(row)==review['content_sha256']
        assert review['request']==json.loads(row['messages'][1]['content']) and review['expected']==ext.model_dump(mode='json')
        assert review['critic_status']==review['human_review']=='unreviewed'
        buckets[row['primary_bucket']]+=1;split_buckets[row['split']][row['primary_bucket']]+=1
        families[row['scenario_family_id']].add(row['split'])
        texts[row['split']].add(re.sub(r'\s+',' ',req.source_text).strip())
        compact[row['split']].add(re.sub(r'\s+','',req.source_text))
        atoms=set(review['semantic_atoms'])
        complex_rows+=len(ext.slot_candidates)+len(ext.symptom_candidates)+len(ext.product_mentions)>=2
        typo_rows+=bool(re.search('어여|해여',req.source_text))
        mixed_subjects+=set(s.subject for s in ext.slot_candidates+ext.symptom_candidates)>={'self','other'}
        for s in ext.slot_candidates:
            slot_counts[s.variable_id]+=1;slot_splits[row['split']][s.variable_id]+=1
            assert not s.variable_id.startswith('product.')
            if s.variable_id in {'sun.water_contact','sun.sweat'} and s.polarity=='denied':
                assert s.value=='yes';policy['yes_denied']+=1
        for s in ext.symptom_candidates:syms[s.symptom]+=1;persistence[s.persistence]+=1
        for m in ext.product_mentions:
            usage[m.usage_state]+=1
            if m.matched_catalog_hint:
                assert any(h.raw_span==m.raw_text and h.matched_catalog_hint==m.matched_catalog_hint for h in req.catalog_hints)
                policy['exact_hint']+=1
            if any(h.raw_span in m.raw_text and h.raw_span!=m.raw_text for h in req.catalog_hints):
                assert m.matched_catalog_hint is None;policy['partial_hint_blocked']+=1
        topics.update(ext.topics)
        if 'label_steps' in atoms:
            assert any(s.variable_id=='cleansing.steps' and s.value=='according_to_product_removal_instructions' for s in ext.slot_candidates)
            policy['label_only']+=1
        if 'both_steps' in atoms:
            assert [s.value for s in ext.slot_candidates if s.variable_id=='cleansing.steps']==[2]
            policy['explicit_count_over_label']+=1
        for key in ['one','two']:
            if key in atoms:
                assert any(s.variable_id=='cleansing.steps' and s.value=={'one':1,'two':2}[key] and type(s.value) is int for s in ext.slot_candidates)
                policy['pure_count']+=1
        if atoms & {'eye_wash','eye_water','eye_sweat','eye_sun'}:
            assert any(s.symptom=='eye_stinging' for s in ext.symptom_candidates)
            assert any(s.variable_id=='skin.eye_symptom_context' for s in ext.slot_candidates)
            for subject in {s.subject for s in ext.symptom_candidates if s.symptom=='eye_stinging'}:
                assert any(s.variable_id=='skin.eye_symptom_context' and s.subject==subject for s in ext.slot_candidates)
            policy['eye_context_paired']+=1
        if atoms & {'routine_lotion','routine_cream','routine_gel','routine_sun','sequence','sun_reapply'}:
            assert any(s.variable_id=='method.current_routine' for s in ext.slot_candidates)
            assert ext.product_mentions;policy['frequency_routine_paired']+=1
        # 기본 제품 사용 문장에 별도 빈도 정보가 전혀 없을 때 current_routine을 만들지 않아요.
        if atoms & {'p_use','p_exact','p_prefix','generic'} and not atoms & {'routine_lotion','routine_cream','routine_gel','routine_sun','sequence','sun_reapply'}:
            assert not any(s.variable_id=='method.current_routine' for s in ext.slot_candidates)
            policy['no_frequency_no_routine']+=1
        if req.previous_question:
            if not ext.slot_candidates and not ext.symptom_candidates and not ext.product_mentions:policy['followup_refusal_or_drift_empty']+=1
            elif req.target_slot_id not in {s.variable_id for s in ext.slot_candidates}:policy['followup_non_target_answer']+=1
    assert len(families)==140 and all(len(v)==1 for v in families.values())
    assert set(buckets.values())=={140} and len(buckets)==7
    assert set(split_buckets['train'].values())=={126} and set(split_buckets['val_internal'].values())=={14}
    assert set(slot_counts)==set(CORE_SLOTS) and min(slot_counts.values())>=14
    assert set(syms)==set(ALLOWED_SYMPTOMS) and set(persistence)=={'recent','repeated','persistent','unknown'}
    assert set(usage)=={'using','stopped','considering','other_person','unknown'} and set(topics)==set(ALLOWED_TOPICS)
    assert not texts['train']&texts['val_internal'] and not compact['train']&compact['val_internal']
    assert len(texts['train'])+len(texts['val_internal'])==980
    assert len(compact['train'])+len(compact['val_internal'])==980
    pilot_raw=(H/'pilot_nlu_v1.jsonl').read_bytes();pilot_sha=hashlib.sha256(pilot_raw).hexdigest()
    assert pilot_sha=='c5f96332f52c6ad5e5a5e36e0a1249c55cc04f3818f352fd42388cb4ef443cbe'
    pilot_texts={re.sub(r'\s+','',json.loads(r['messages'][1]['content'])['source_text']) for r in lines(H/'pilot_nlu_v1.jsonl')}
    assert not (compact['train']|compact['val_internal'])&pilot_texts
    report=dict(passed=True,scope='구조·분포·원문 span·작성 정책 경계 검사이며 독립 의미 검수/모델 성능 검사가 아니에요.',
      rows=980,splits={k:sum(v.values()) for k,v in split_buckets.items()},primary_buckets=dict(buckets),primary_buckets_by_split={k:dict(v) for k,v in split_buckets.items()},
      semantic_families=140,variants_per_family=7,family_leakage=0,normalized_utterance_leakage=0,all_whitespace_removed_leakage=0,
      all_whitespace_removed_duplicates=0,pilot_source_overlap=0,pilot_sha256=pilot_sha,slot_counts=dict(slot_counts),
      slot_counts_by_split={k:dict(v) for k,v in slot_splits.items()},symptoms=dict(syms),persistence=dict(persistence),product_usage=dict(usage),topics=dict(topics),
      complex_candidate_rows=complex_rows,ending_typo_rows=typo_rows,mixed_self_other_rows=mixed_subjects,policy_boundaries=dict(policy),
      dataset_sha256=hashlib.sha256(raw).hexdigest(),request_hashes_verified=980,cross_model_critic_performed=False,human_approved=False)
    (H/'validation/step2_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    # 외부 검수자는 각 배치에서 모든 입력/예상값/작성 근거를 읽을 수 있어요.
    out=H/'reviews/step2_batches';out.mkdir(exist_ok=True)
    for i in range(14):
        (out/f'batch_{i+1:02d}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in reviews[i*70:(i+1)*70]),encoding='utf-8',newline='\n')
    readable=['# NLU Step 2 980턴 — 원문·예상 후보·작성 근거','',
      '독립 Critic·사람 승인 결과가 아니라 합성 작성본 대조표예요. 모든 후보는 미확정이에요.','']
    for r in reviews:
        readable += [f"## {r['row_id']} · {r['primary_bucket']} · {r['split']}",'',
          f"의미 가족: `{r['scenario_family_id']}` / 표현 변형: {r['variant']}",'',
          '### 원문 raw','',r['request']['source_text'],'',
          f"직전 질문: {r['request']['previous_question']}",f"질문 대상: {r['request']['target_slot_id']}",'',
          '### 예상 JSON raw','','```json',json.dumps(r['expected'],ensure_ascii=False,indent=2),'```','',
          '### 작성 근거 (외부 검수 결과 아님)','',r['author_rationale'],'',
          f"내용 SHA-256: `{r['content_sha256']}`",'']
    (H/'step2_review.md').write_text('\n'.join(readable),encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'slot_counts','slot_counts_by_split'}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
