"""공식 청크 풀 기반 Step 2 체크포인트 검사. 내용의 교차 모델 검수를 대체하지 않아요."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

COS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(COS))
from beauty_agent.v3_contracts import ReferenceChunk, SLMRequest
from validate_qlora_dataset import compute_row_content_sha256

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

def expected_checkpoint_ids():
    groups=[('sol',1,120),('sol',211,220),('sol',231,350),('sol',441,450),('sol',461,575),('sol',671,680),
            ('hold',1,40),('hold',71,100),('hold',131,135),('hold',141,170),('hold',201,210)]
    return {f'syn-{kind}-{i:04d}' for kind,start,end in groups for i in range(start,end+1)}

def inspect(input_path,pool_path,expected_count=500):
    raw=input_path.read_bytes()
    pool_raw=pool_path.read_bytes()
    errors=[]
    if raw.startswith(b'\xef\xbb\xbf'): errors.append('데이터에 UTF-8 BOM이 있어요.')
    if b'\r' in raw: errors.append('데이터에 CR/CRLF가 있어요. LF로 저장해야 해요.')
    lines=raw.decode('utf-8').splitlines()
    if any(not line.strip() for line in lines): errors.append('JSONL 중간에 빈 행이 있어요.')
    rows=[json.loads(line) for line in lines if line.strip()]
    pool_list=[json.loads(line) for line in pool_raw.decode('utf-8').splitlines() if line.strip()]
    pool={c['evidence_ref']:c for c in pool_list}
    assert len(pool)==len(pool_list)==151
    for c in pool.values(): ReferenceChunk.model_validate(c)
    ids=[r['id'] for r in rows]
    if len(rows)!=expected_count: errors.append(f'예상 {expected_count}행, 실제 {len(rows)}행이에요.')
    if len(set(ids))!=len(ids): errors.append('중복 행 ID가 있어요.')
    if expected_count==500 and set(ids)!=expected_checkpoint_ids(): errors.append('500턴 사전 할당 ID와 일치하지 않아요.')
    modes=Counter(); domains=Counter(); hn=Counter(); splits=Counter(); approvals=Counter(); origins=Counter()
    canonical=Counter(); answer_counts=Counter(); used=Counter(); allowed_used=Counter(); high_risk=[]; review_requests=[]
    sentence_rows={}; semantic_candidates=[]
    # 고유한 방해 주제의 표면적 유입을 후보로만 탐지해요. 의미상 완전 무시는 별도 내용 검수가 필요해요.
    concepts=[('재도포',('재도포','reapply','reapplication','덧바르')),('항균',('항균','antibacterial')),
              ('화기',('불꽃','화재','화기','flame','ignition','fire')),('제모',('제모','depilatory')),
              ('염모',('염모','염색','hair dye')),('퍼머',('퍼머','perming')),
              ('파라핀',('파라핀','paraffin')),('샴푸',('샴푸','shampoo')),
              ('살리실산',('살리실산','salicylic')),('레티놀',('레티놀','retinol')),
              ('도구청결',('화장 도구','브러시','brushes','applicator'))]
    for row in rows:
        rid=row['id']; modes[row['mode']]+=1; splits[row['split']]+=1
        for domain in row['domains']: domains[domain]+=1
        if row['is_hard_negative']: hn[row['hard_negative_type']]+=1
        prov=row.get('provenance',{}); approvals[prov.get('human_review')]+=1
        if prov.get('source_origin')!='new_synthetic' or prov.get('source_scenario_id') is not None or prov.get('source_turn_id') is not None:
            errors.append(rid+': 신규 합성 원천/계보 위반')
        if prov.get('critic_status')!='unreviewed' or prov.get('critic_model') is not None or prov.get('human_review')!='unreviewed':
            errors.append(rid+': 로컬 생성 단계에서 미실시 검수 승인이 기록됨')
        invariants=row.get('runtime_invariants',{})
        if invariants!={'mode':'development_preview','production_enabled':False,'requires_approval':True,'saved':False}:
            errors.append(rid+': 런타임 안전 설정 메타데이터 불일치')
        req_dict=json.loads(row['messages'][1]['content'])
        if 'kb_judgments' in req_dict: errors.append(rid+': KB 판정 키 포함')
        req=SLMRequest.model_validate(req_dict)
        assistant=row['messages'][2]['content']
        if '[kb:' in assistant: errors.append(rid+': KB 인용 포함')
        normalized=json.dumps(req.model_dump(mode='json'),ensure_ascii=False,sort_keys=True,separators=(',',':'))
        canonical[hashlib.sha256(normalized.encode()).hexdigest()]+=1
        normalized_answer=re.sub(r'\s+',' ',assistant).strip(); answer_counts[normalized_answer]+=1
        if row['mode']=='hold' and (req.rag_chunks or req.allowed_evidence_refs or req.distractor_refs):
            errors.append(rid+': HOLD 문헌 또는 인용 목록 포함')
        all_refs=req.allowed_evidence_refs+req.distractor_refs
        if any(ref not in pool for ref in all_refs): errors.append(rid+': 공식 풀 이외 허용/방해 ID 포함')
        for chunk in req_dict['rag_chunks']:
            ref=chunk['evidence_ref']; used[ref]+=1
            if ref not in pool or chunk!=pool[ref]: errors.append(rid+': 공식 청크 원문/메타 불일치 '+ref)
            if row['chunk_origins'].get(ref)!='reference_excerpt': errors.append(rid+': 풀 문단 출처 유형 불일치 '+ref)
            origins[row['chunk_origins'].get(ref)]+=1
        allowed_used.update(req.allowed_evidence_refs)
        relevant=' '.join(pool[r]['text'] for r in req.allowed_evidence_refs).casefold()
        context=json.dumps(req_dict['confirmed_observations'],ensure_ascii=False).casefold()+' '+json.dumps(req_dict['product_evidence'],ensure_ascii=False).casefold()
        for ref in req.distractor_refs:
            distractor=pool[ref]['text'].casefold()
            for label,words in concepts:
                if any(w.casefold() in distractor for w in words) and not any(w.casefold() in relevant+' '+context for w in words) and any(w.casefold() in assistant.casefold() for w in words):
                    semantic_candidates.append({'row_id':rid,'distractor_ref':ref,'topic':label,'status':'내용 확인 필요: 표면적 탐지 후보'})
        for sentence in re.split(r'(?<=[.!?])\s+',re.sub(r'\[[^\]]+\]','',assistant)):
            sentence=re.sub(r'### [^\n]+\n?','',sentence).strip()
            if len(sentence)>=25: sentence_rows.setdefault(sentence,set()).add(rid)
        digest=compute_row_content_sha256(req,assistant,card_ids=row.get('card_ids',[]),chunk_origins=row['chunk_origins'],is_hard_negative=row['is_hard_negative'],hard_negative_type=row['hard_negative_type'])
        review_requests.append({'row_id':rid,'content_sha256':digest,'mode':row['mode'],'request':req_dict,'assistant':assistant,
                                'card_ids':row.get('card_ids',[]),'chunk_origins':row['chunk_origins'],
                                'is_hard_negative':row['is_hard_negative'],'hard_negative_type':row['hard_negative_type'],
                                'generator_model':prov['generator_model'],'runtime_invariants':invariants})
        if row['mode']=='hold' or row['hard_negative_type'] in {'version_mismatch_or_unknown','clinical_restraint'}: high_risk.append(rid)
    repeated_inputs=sum(n-1 for n in canonical.values() if n>1)
    repeated_answers=sum(n-1 for n in answer_counts.values() if n>1)
    if repeated_inputs: errors.append(f'정규화 입력 중복 {repeated_inputs}건')
    if repeated_answers: errors.append(f'전체 답변 중복 {repeated_answers}건')
    repeat_sentences=[{'sentence':s,'row_count':len(rs),'row_ids':sorted(rs)} for s,rs in sentence_rows.items() if len(rs)>=5]
    report={'check_scope':'생성·구조·공식 풀 일치·표면적 후보 탐지. 의미 정확성이나 교차 모델 검수 PASS가 아니에요.',
            'rows':len(rows),'modes':dict(modes),'domain_occurrences':dict(domains),'splits':dict(splits),'hard_negative_types':dict(hn),
            'human_review':dict(approvals),'chunk_origins':dict(origins),'pool_rows':len(pool),'pool_sha256':hashlib.sha256(pool_raw).hexdigest(),
            'dataset_sha256':hashlib.sha256(raw).hexdigest(),'unique_used_refs':len(used),'unique_allowed_refs':len(allowed_used),
            'unused_pool_refs':sorted(set(pool)-set(used)),'used_ref_occurrences':dict(sorted(used.items())),
            'duplicate_inputs':repeated_inputs,'duplicate_answers':repeated_answers,'surface_distractor_candidates':semantic_candidates,
            'sentences_repeated_at_least_5_rows':repeat_sentences,'high_risk_rows':high_risk,
            'error_count':len(errors),'errors':errors,'structural_and_pool_checks_passed':not errors,
            'cross_model_critic_performed_locally':False,'final_training_approved':False}
    return report,review_requests

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--pool',type=Path,default=COS/'data/rag/chunks.jsonl')
    parser.add_argument('--expected-count',type=int,default=500)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--review-requests',type=Path)
    args=parser.parse_args()
    report,requests=inspect(args.input,args.pool,args.expected_count)
    write_json(args.report,report)
    if args.review_requests:
        args.review_requests.parent.mkdir(parents=True,exist_ok=True)
        args.review_requests.write_bytes((''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in requests)).encode('utf-8'))
    print(json.dumps({k:v for k,v in report.items() if k not in {'used_ref_occurrences','high_risk_rows','sentences_repeated_at_least_5_rows','surface_distractor_candidates','unused_pool_refs'}},ensure_ascii=False,indent=2))
    print('방해 주제 표면 후보:',len(report['surface_distractor_candidates']),'반복 문장 후보:',len(report['sentences_repeated_at_least_5_rows']))
    return int(bool(report['errors']))

if __name__=='__main__':
    raise SystemExit(main())
