"""PPO-37의 별도 신규 합성 검사와 파일럿 샘플의 Git 원문 일치를 확인해요."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

COS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(COS/'data/qlora/v2'))
from refresh_corpus_pilot import parse_corpus, sha, CORPUS_COMMIT

data=COS/'data/qlora/v2'
rows=[json.loads(line) for line in (data/'pilot_24.jsonl').read_text(encoding='utf-8').splitlines()]
plan=json.loads((data/'pilot_24_inputs.json').read_text(encoding='utf-8'))
registry=json.loads((data/'pilot_24_source_registry.json').read_text(encoding='utf-8'))['sources']
corpus={s['chunk']['evidence_ref']:s for s in parse_corpus()}
failures=[]
occurrences=0
for case,row in zip(plan['cases'],rows):
    rid=row['id']; req=json.loads(row['messages'][1]['content']); provenance=row['provenance']
    if provenance['source_origin']!='new_synthetic' or provenance['source_turn_id'] is not None or provenance['source_scenario_id'] is not None:
        failures.append(rid+': 신규 합성 계보 불일치')
    if case['request']!=req or sha(req)!=case['input_sha256']:
        failures.append(rid+': 고정 입력 불일치')
    if 'kb_judgments' in req or '[kb:' in row['messages'][2]['content']:
        failures.append(rid+': KB 판정 혼입')
    if provenance['human_review']!='unreviewed' or provenance['critic_status']!='unreviewed' or provenance['critic_model'] is not None:
        failures.append(rid+': 미실시 검수 승인')
    for chunk in req['rag_chunks']:
        occurrences+=1
        ref=chunk['evidence_ref']
        if ref not in registry or ref not in corpus or chunk!=registry[ref]['chunk'] or chunk!=corpus[ref]['chunk']:
            failures.append(rid+': 코퍼스 문단 불일치 '+ref)
        elif corpus[ref]['tier']!='tier1':
            failures.append(rid+': Tier 2 문단 사용 '+ref)
    if req['mode']=='hold' and req['rag_chunks']:
        failures.append(rid+': HOLD RAG 포함')
    if plan.get('plan_revision',2)>=3:
        if re.search(r'fixture-\d|rf-(?:r2-|clean-)|버전이 일치|현재 버전과 일치|합성 제품',case['user_utterance']):
            failures.append(rid+': 사용자 발화에 시스템 제작 정보 포함')
        available=[case['user_utterance']]+[p['text'] for p in case['prior_user_confirmations']]
        for key,observation in req['confirmed_observations'].items():
            trace=case['observation_trace'].get(key)
            if not trace:
                failures.append(rid+': 관찰 출처 누락 '+key)
                continue
            for evidence in trace.get('evidence',[]):
                if 'text' in evidence and evidence['text'] not in available:
                    failures.append(rid+': 출처 발화 불일치 '+key)
            if observation['state']=='known' and not trace.get('evidence'):
                failures.append(rid+': 알려진 관찰의 발화 근거 누락 '+key)
            if isinstance(observation['value'],dict) and set(observation['value']) & {'product_id','version','held_product_id','label_version_matches','current_version_confirmed','actual_application_not_reported','full_plan_provided'}:
                failures.append(rid+': 시스템 상태를 사용자 관찰로 혼합 '+key)
        displayed_answer=re.sub(r'\[[^\]]*\]','',row['messages'][2]['content'])
        if re.search(r'(?<![가-힣])합성(?=\s|$)|fixture-\d|rf-r2-',displayed_answer):
            failures.append(rid+': 사용자 응답 본문에 제작용 표현 포함')
    if set(req['allowed_evidence_refs']) & set(req['distractor_refs']):
        failures.append(rid+': 허용·방해 인용 중복')
assert len(rows)==len(plan['cases'])==24
assert not failures, failures
report={'rows':len(rows),'new_synthetic':24,'recycled_v67':0,'unknown_or_legacy_lineage':0,
        'corpus_commit':CORPUS_COMMIT,'selected_paragraphs':len(registry),'chunk_occurrences':occurrences,
        'exact_referencechunk_matches':occurrences,'tier2_occurrences':0,'kb_judgments_keys':0,
        'official_PPO42_pool_received':False,'stage2_ready':False,'critic_reviewed':False,'human_reviewed':False,
        'natural_user_utterances':24 if plan.get('plan_revision',2)>=3 else 0,
        'utterance_and_product_context_separated':plan.get('plan_revision',2)>=3,
        'trace_check_scope':'작성한 합성 발화와 추적표의 연결 검사이며, 실제 NLU/AFA 실행·의미 정확성의 독립 승인이 아니에요.',
        'note':'고정 Markdown 커밋과의 파일럿 샘플 일치 검사예요. 최종 PPO-42 풀 일치·검색 평가·내용 검수 PASS가 아니에요.',
        'error_count':len(failures),'errors':failures}
out=COS/plan.get('revision_output_dir','outputs/qlora_v3_pilot_20261125/revision_02')/'corpus_alignment.json'
out.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(report,ensure_ascii=False,indent=2))
