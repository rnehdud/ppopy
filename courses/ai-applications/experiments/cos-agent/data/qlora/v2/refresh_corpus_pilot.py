"""PPO-37 개정 2: 고정 코퍼스의 Tier 1 문단을 사용하는 24턴 입력을 먼저 고정해요."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
COS=HERE.parents[2]
sys.path.insert(0,str(COS/'scripts'))
import validate_qlora_dataset as validator
from beauty_agent.v3_contracts import ReferenceChunk

CORPUS_COMMIT='dd418a3185aa94bc3eb118af268b53647c9d73e5'
BASE_COMMIT='2b2063c24bfec5f9c63ce84265d8e0189d48fde2'
OUT=COS/'outputs/qlora_v3_pilot_20261125/revision_02'

def sha(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def write(path,obj):
    path.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

def parse_corpus():
    result=[]
    for domain in ['cleansing','moisturizing','sun_protection','storage_label']:
        path='courses/ai-applications/experiments/cos-agent/data/rag/corpus/'+domain+'.md'
        raw=subprocess.check_output(['git','show',CORPUS_COMMIT+':'+path])
        for ordinal,block in enumerate(re.split(r'(?m)^## ',raw.decode('utf-8'))[1:],1):
            heading,_,rest=block.partition('\n')
            metadata={m.group(1):m.group(2).strip() for m in re.finditer(r'(?m)^- ([a-z_]+): (.*)$',rest)}
            body=re.sub(r'(?m)^- [a-z_]+: .*\n?','',rest).strip()
            key=f'ref:rc-dd418a3-{domain}-{ordinal:03d}'
            chunk={'evidence_ref':key,'text':body,**metadata}
            result.append({'title':heading,'domain':domain,'corpus_commit':CORPUS_COMMIT,'file':path,'paragraph_ordinal':ordinal,
                           'file_sha256':hashlib.sha256(raw).hexdigest(),'body_sha256':hashlib.sha256(body.encode()).hexdigest(),
                           'tier':'tier2' if 'pmc.ncbi.nlm.nih.gov' in metadata['source_url'] else 'tier1',
                           'origin':'kb_source_summary' if re.search('[가-힣]',body) else 'reference_excerpt', 'chunk':chunk})
    return result

def slot(key,value):
    return {'variable_id':key,'state':'known','value':value,'source':'synthetic_fixture','confirmed_by_user':True}

def unknown(key):
    return {'variable_id':key,'state':'unknown','value':None,'source':'synthetic_fixture','confirmed_by_user':False}

def product(pid,label):
    return {'product_id':pid,'version':'fixture-2','synthetic_product':True,'status':'verified','label_guidance':label,
            'evidence_ref':f'catalog:{pid}@fixture-2','fixture_notice':'실재 상품이 아닌 신규 합성 제품 표시 예시'}

def set_gel_case(case):
    case['scenario_raw']='합성 세정제 rf-r2-gel-07의 현재 fixture-2 표시에는 젤형 얼굴 세정제라고 되어 있지만 pH는 자료에 없어요. 약산성인지 알고 싶어요. 손끝으로 씻고 있고 현재 통증과 불편은 없어요.'
    r=case['request']
    r['product_evidence']=[product('rf-r2-gel-07','현재 버전과 일치하는 합성 표시: 젤형 얼굴 세정제. pH 자료 미공개')]
    r['confirmed_observations']['method.current_routine']=slot('method.current_routine',{'product_id':'rf-r2-gel-07','version':'fixture-2','label_version_matches':True})
    r['allowed_evidence_refs']=[r['rag_chunks'][0]['evidence_ref'],r['product_evidence'][0]['evidence_ref']]
    case['input_sha256']=sha(r)

def freeze():
    old=json.loads((OUT/'before/pilot_24_inputs.json').read_text(encoding='utf-8'))
    assert (OUT/'before/archive_sha256.json').exists()
    assert not (OUT/'input_revision_frozen.json').exists(), '개정 입력을 다시 덮어쓰지 않아요.'
    all_sources=parse_corpus()
    # 고정 커밋에서 읽은 문단 순번이며 KB 카드·기존 학습셋의 번호가 아니에요.
    source_indices=[10,10,48,44,89,87,3,0,44,127,93,91,11,1,52,47,84,92]
    distractors={13:108,14:44,15:89,16:87,17:44,18:108}
    selected={}
    cases=deepcopy(old['cases'])
    for n,c in enumerate(cases,1):
        c['scenario_id']='rf25-r2-scenario-'+c['id']
        c['group_id']='rf25-r2-group-'+c['id']
        c['scenario_family_id']='rf25-r2-family-'+c['id']
        if c['mode']=='hold':
            c['input_sha256']=sha(c['request'])
            continue
        r=c['request']
        relevant=all_sources[source_indices[n-1]]
        assert relevant['tier']=='tier1'
        ReferenceChunk.model_validate(relevant['chunk'])
        selected[relevant['chunk']['evidence_ref']]=relevant
        r['rag_chunks']=[deepcopy(relevant['chunk'])]
        r['allowed_evidence_refs']=[relevant['chunk']['evidence_ref']]+[p['evidence_ref'] for p in r['product_evidence'] if p['status']=='verified' and p['evidence_ref']]
        r['distractor_refs']=[]
        c['chunk_origins']={relevant['chunk']['evidence_ref']:relevant['origin']}
        if n in distractors:
            d=all_sources[distractors[n]]
            assert d['tier']=='tier1'
            ReferenceChunk.model_validate(d['chunk'])
            selected[d['chunk']['evidence_ref']]=d
            r['rag_chunks'].append(deepcopy(d['chunk']))
            r['distractor_refs']=[d['chunk']['evidence_ref']]
            c['chunk_origins'][d['chunk']['evidence_ref']]=d['origin']
        if n==3:
            c['title']='샤워 뒤 보습을 한참 미루는 습관'
            c['scenario_raw']='샤워한 뒤 피부가 완전히 마르고 한참 지나서야 팔에 보습제를 발라요. 팔은 약간 건조하고 현재 통증과 불편은 없어요. 샤워와 보습 순서를 점검하고 싶어요.'
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.current_routine':{'actual_site':'forearms','moisturizer_used':True,'application_timing':'long_after_shower_when_fully_dry'},'constraints.goals':['샤워 뒤 보습 순서 점검'],'skin.dryness':'mild','skin.pain':'none','skin.current_discomfort':'none'}.items()}
        elif n==4:
            c['title']='보습 로션을 바른 뒤 다시 씻어내는 행동'
            c['scenario_raw']='합성 로션 rf-r2-lotion-04의 현재 fixture-2 표시에는 피부에 남기는 보습용이라고 되어 있어요. 저는 바른 뒤 물로 씻어내요. 통증이나 불편은 없고, 용도에 맞는지 궁금해요.'
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.current_routine':{'product_id':'rf-r2-lotion-04','version':'fixture-2','label_version_matches':True,'actual_removal':'rinsed_after_application'},'constraints.goals':['보습 로션의 용도와 실제 사용 대조'],'skin.pain':'none','skin.current_discomfort':'none'}.items()}
            r['product_evidence']=[product('rf-r2-lotion-04','현재 버전과 일치하는 합성 표시: 피부에 남기는 보습 로션')]
        elif n==7:
            set_gel_case(c)
        elif n==9:
            c['title']='로션이라는 이름만으로 용도를 판단하지 않기'
            c['scenario_raw']='지금 가진 용기에 로션이라는 이름은 보이지만 용도와 사용 지시는 아직 확인하지 못했어요. 보습용인지 세정용인지 궁금해요. 현재 피부 통증과 불편은 없어요.'
            r['product_evidence']=[{'product_id':'rf-r2-lotion-09','version':None,'synthetic_product':True,'status':'unknown','label_guidance':None,'evidence_ref':None,'fixture_notice':'용도와 버전이 미확인인 합성 제품'}]
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.current_routine':{'observed_package_word':'로션','actual_application_not_reported':True},'constraints.goals':['제품의 표시 용도 확인'],'skin.pain':'none','skin.current_discomfort':'none'}.items()}
            r['confirmed_observations']['method.product_purpose']=unknown('method.product_purpose')
        elif n==12:
            c['title']='선선하고 흐린 날의 산책 계획과 UV 미상'
            c['scenario_raw']='내일 산책할 생각이고 예보는 선선하고 흐림이에요. 시간과 길은 아직 정하지 않았고 현재는 실내에 있어요. 내일의 자외선 지수는 몰라요. 현재 통증과 불편은 없어요.'
            r['confirmed_observations']['environment.forecast']=slot('environment.forecast',{'for':'planned_walk_day','temperature_description':'cool','sky':'cloudy'})
        elif n==13:
            c['title']='가정용 항균 비누의 표시를 효과 보증으로 읽지 않기'
            c['scenario_raw']='집에서 손을 씻을 비누를 고르고 있어요. 항균이라는 표시만으로 일반 비누보다 질병 예방이 더 잘된다고 판단해도 되는지 궁금해요. 지금 손의 통증과 불편은 없어요.'
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.body_site':'hands','method.current_routine':{'setting':'home','product_type_under_consideration':'consumer_rinse_off_antibacterial_soap','purchase_completed':False},'constraints.goals':['항균 표시와 비교 근거 구분'],'skin.pain':'none','skin.current_discomfort':'none'}.items()}
        elif n==15:
            c['title']='파라핀 무첨가 에몰리언트와 옷의 잔여물·불꽃'
            c['scenario_raw']='합성 에몰리언트 rf-r2-emollient-15의 현재 fixture-2 표시는 파라핀 무첨가예요. 이 제품이 소매에 묻어 마른 상태이고, 곧 가스레인지 불 가까이 갈 계획이에요. 지금 화상이나 피부 통증·불편은 없어요.'
            r['product_evidence']=[product('rf-r2-emollient-15','현재 버전과 일치하는 합성 에몰리언트 표시: 파라핀 무첨가')]
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.current_routine':{'product_id':'rf-r2-emollient-15','version':'fixture-2','label_version_matches':True,'dried_residue_on_sleeve':True},'environment.flame_exposure':{'planned_near_gas_stove_flame':True,'burn_occurred':False},'skin.pain':'none','skin.current_discomfort':'none'}.items()}
        elif n==16:
            c['title']='친구의 성분 알레르기를 본인의 사실로 옮기지 않기'
            c['scenario_raw']='현재 fixture-2와 일치하는 합성 제품 rf-r2-hand-16 자료에는 우레아 함유 손발용 크림이라고 되어 있어요. 저는 손에만 쓰고 통증이나 불편은 없어요. 프로필렌글리콜 포함 여부는 몰라요. 친구에게 그 성분 알레르기가 있다는 얘기를 들었지만 제 알레르기 이력은 확인되지 않았어요.'
            r['product_evidence']=[product('rf-r2-hand-16','현재 버전과 일치하는 합성 표시: 우레아 함유 손발용 크림. 프로필렌글리콜 포함 여부 미확인')]
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.current_routine':{'product_id':'rf-r2-hand-16','version':'fixture-2','label_version_matches':True,'actual_site':'hands'},'method.other_person_report':{'subject':'friend','reported_allergen':'propylene_glycol'},'skin.pain':'none','skin.current_discomfort':'none'}.items()}
            r['confirmed_observations']['skin.known_allergens']=unknown('skin.known_allergens')
            c['hard_negative_type']='negation_or_other_subject'
        elif n==17:
            c['title']='물놀이 중 차단제 재도포 없이 세 시간 경과'
            c['scenario_raw']='야외 물놀이 중이고 차단제를 처음 바른 뒤 세 시간이 지났지만 다시 바르지는 않았어요. 제품의 내수성 표시는 아직 못 봤어요. 현재 피부 통증과 불편은 없어요.'
            r['confirmed_observations']={k:slot(k,v) for k,v in {'sun.activity':{'outdoors':True,'water_play':True,'hours_since_sunscreen_application':3,'reapplied':False},'skin.pain':'none','skin.current_discomfort':'none'}.items()}
            r['confirmed_observations']['sun.product_water_resistance']=unknown('sun.product_water_resistance')
        elif n==18:
            c['title']='친구의 통증과 본인의 목·귀 도포 누락 구분'
            c['scenario_raw']='친구는 차단제를 쓴 뒤 아팠다고 했어요. 저는 현재 통증이나 불편은 없어요. 지금 야외에 있고 목과 귀는 드러나 있지만 차단제는 얼굴에만 발랐어요. 빠진 부위를 점검하고 싶어요.'
            r['confirmed_observations']={k:slot(k,v) for k,v in {'method.other_person_report':{'subject':'friend','pain_after_sunscreen':True},'sun.activity':{'outdoors':True,'neck_exposed':True,'ears_exposed':True,'sunscreen_applied_sites':['face']},'constraints.goals':['도포에서 빠진 노출 부위 점검'],'skin.pain':'none','skin.current_discomfort':'none'}.items()}
        # 새 제품 근거와 허용 카탈로그 인용을 다시 일치시켜요.
        r['allowed_evidence_refs']=[relevant['chunk']['evidence_ref']]+[p['evidence_ref'] for p in r['product_evidence'] if p['status']=='verified' and p['evidence_ref']]
        validator.SLMRequest.model_validate(r)
        c['input_sha256']=sha(r)
        c['corpus_link']={'relevant_ref':relevant['chunk']['evidence_ref'],'source_commit':CORPUS_COMMIT,'handoff_status':'pilot_sample_not_official_PPO42_pool'}
    registry={'corpus_commit':CORPUS_COMMIT,'handoff_status':'pilot_sample_not_official_PPO42_pool','tier2_used':False,
              'id_notice':'이 ref ID는 파일럿용 결정적 ID이며 공식 PPO-42 변환기의 ID라고 주장하지 않아요.',
              'sources':selected}
    new={'base_commit':BASE_COMMIT,'plan_revision':2,'mode':'development_preview','production_enabled':False,
         'target_training_model':'Qwen/Qwen3-4B-Instruct-2507','requirements_updated_at':'2026-11-24T15:39:56.847Z',
         'authoring_note':'이전 파일럿의 신규 합성 상황을 갱신해요. aa1bf19·v67 재가공은 없으며 정형 KB 판정도 넣지 않아요. Tier 1 샘플이고 공식 RAG 풀은 미인계 상태예요.',
         'sources':registry,'cases':cases}
    write(HERE/'pilot_24_source_registry.json',registry)
    write(HERE/'pilot_24_inputs.json',new)
    write(OUT/'input_revision_frozen.json',{'revision':2,'inputs_sha256':sha(new),'input_hashes':{c['id']:c['input_sha256'] for c in cases}})
    print('개정 2 입력 24턴 고정 완료. Tier 2 논문은 사용하지 않았어요.')

def align_gel_once():
    inputs=json.loads((HERE/'pilot_24_inputs.json').read_text(encoding='utf-8'))
    assert not (OUT/'gel_alignment_change.json').exists()
    write(OUT/'inputs_before_gel_alignment.json',inputs)
    case=inputs['cases'][6]
    before=deepcopy(case)
    set_gel_case(case)
    write(OUT/'gel_alignment_change.json',{'reason':'젤형 설명 문단을 근거로 쓸 수 있도록, pH를 만들지 않고 합성 제품의 확인된 젤형 표시를 입력에 명시해요. 답변도 변경된 입력으로 다시 작성하고 검수 상태는 미검수로 유지해요.','before_raw':before,'after_raw':case})
    write(HERE/'pilot_24_inputs.json',inputs)
    write(OUT/'input_revision_frozen_after_alignment.json',{'revision':'2.1','inputs_sha256':sha(inputs),'input_hashes':{c['id']:c['input_sha256'] for c in inputs['cases']}})

if __name__=='__main__':
    align_gel_once() if '--align-gel' in sys.argv else freeze()
