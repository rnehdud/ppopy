"""개정 3: 자연어 발화·별도 사용자 확인·가상 카탈로그 근거를 분리해요."""
from copy import deepcopy
import json
from pathlib import Path
import sys

from refresh_corpus_pilot import sha

HERE=Path(__file__).resolve().parent
COS=HERE.parents[2]
OUT=COS/'outputs/qlora_v3_pilot_20261125/revision_03'

# 각 문자열은 실제 사용자의 기록이 아니라 사람이 읽을 수 있게 쓴 신규 합성 발화예요.
# 슬롯의 supports는 이 발화에서 어떤 관찰을 구성했는지 추적하는 작성 기록이며 NLU 실행 결과가 아니에요.
def part(text,*supports):
    return {'text':text,'supports':list(supports)}

CONVERSATIONS=[
    [part('세수할 때 볼을 좀 세게 문지르는 편인데, 이렇게 씻어도 괜찮을까요?', 'method.body_site','method.friction','constraints.goals'),
     part('손끝으로 씻고 물은 미지근하게 써요.','method.tools','method.water_temperature'),part('지금 아프거나 불편한 건 없어요.','skin.pain','skin.current_discomfort')],
    [part('얼굴 헹구고 나서 수건으로 빡빡 닦는데, 이건 바꾸는 게 좋을까요?','method.body_site','method.drying'),
     part('세수할 때 얼마나 힘을 줬는지는 잘 기억 안 나요.','method.cleansing_pressure'),part('지금 피부가 아프거나 불편하지는 않아요.','skin.pain','skin.current_discomfort')],
    [part('샤워하고 한참 뒤에 보습제를 바르는데, 바로 바르는 게 나을까요?','method.current_routine','constraints.goals'),
     part('팔이 완전히 마르고 나서 발라요. 팔이 조금 건조한 편이에요.','method.current_routine','skin.dryness'),part('통증이나 다른 불편은 없어요.','skin.pain','skin.current_discomfort')],
    [part('로션 바른 다음에 물로 한 번 씻어내는데, 이렇게 쓰는 거 맞아요?','method.current_routine','constraints.goals'),
     part('지금 따로 아프거나 불편한 데는 없어요.','skin.pain','skin.current_discomfort')],
    [part('밖에서 땀을 많이 흘렸는데 선크림을 다시 발라야 하나요?','sun.activity'),
     part('나오기 전에 발랐고 땀 흘린 뒤에는 아직 안 발랐어요.','sun.activity'),part('물에 얼마나 견디는 제품인지는 안 봤어요.','sun.product_water_resistance'),part('지금 피부 통증이나 불편은 없어요.','skin.pain','skin.current_discomfort')],
    [part('선크림 발랐으니까 팔은 안 가려도 된다고 생각했는데, 괜찮나요?','sun.activity','sun.protection_belief'),
     part('지금 밖에 있고 팔은 드러나 있어요.','sun.activity'),part('피부가 아프거나 불편한 건 아니에요.','skin.pain','skin.current_discomfort')],
    [part('이 젤 세안제, 약산성인지 알 수 있나요?','constraints.goals'),
     part('얼굴 씻을 때 손끝으로 쓰고 있어요.','method.body_site','method.tools'),part('지금 아프거나 불편하지는 않아요.','skin.pain','skin.current_discomfort')],
    [part('이 세안제도 물로 헹구면 되는 건가요?','method.current_removal_instruction'),
     part('전에 쓰던 건 물로 헹구는 거였어요. 지금 것의 사용법은 아직 못 봤어요.','method.current_removal_instruction'),part('현재 피부에 통증이나 불편은 없어요.','skin.pain','skin.current_discomfort')],
    [part('여기 로션이라고 써 있는데, 바르고 두는 거예요, 아니면 씻어내는 거예요?','method.current_routine','constraints.goals','method.product_purpose'),
     part('지금 피부가 아프거나 불편한 상태는 아니에요.','skin.pain','skin.current_discomfort')],
    [part('이 보습제 언제 열었는지 기억이 안 나요. 아직 써도 될까요?','storage.opened_on'),
     part('사용기한 표시는 아직 못 읽었어요.','storage.expiry_label'),part('색이나 냄새가 바뀌거나 층이 나뉜 건 없어요.','storage.sensory_change'),part('피부 통증이나 불편도 없고요.','skin.pain','skin.current_discomfort')],
    [part('내일 나갈 때 이 선크림 쓰려는데, SPF가 얼마인지 알 수 있어요?','sun.activity','sun.current_product_spf'),
     part('지금은 실내에 있고 아직 나간 건 아니에요.','sun.activity'),part('지금 피부가 아프거나 불편한 건 없어요.','skin.pain','skin.current_discomfort')],
    [part('내일 선선하고 흐리다던데, 산책할 때도 자외선 신경 써야 하나요?','sun.activity','environment.forecast'),
     part('아직 얼마나 걸을지랑 길은 안 정했어요. 자외선 지수도 모르겠어요.','sun.planned_exposure_duration','environment.future_uv_index'),part('지금은 실내에 있고 피부 통증이나 불편은 없어요.','sun.activity','environment.current_location','skin.pain','skin.current_discomfort')],
    [part('집에서 손 씻을 비누를 살까 하는데, 항균이라고 쓰인 게 병 예방에 더 좋은가요?','method.body_site','method.current_routine','constraints.goals'),
     part('아직 고르는 중이고 산 건 아니에요. 물로 헹궈 쓰는 비누를 보고 있어요.','method.current_routine'),part('손이 아프거나 불편한 건 없어요.','skin.pain','skin.current_discomfort')],
    [part('이 세안제 얼굴에 바르고 그냥 두는데, 물로 씻어내야 하나요?','method.body_site','method.current_routine'),
     part('지금 얼굴이 아프거나 불편하지는 않아요.','skin.pain','skin.current_discomfort')],
    [part('보습크림 묻은 소매 그대로 가스불 앞에서 요리해도 괜찮을까요?','method.current_routine','environment.flame_exposure'),
     part('소매에 묻은 건 이미 말랐어요. 불 가까이 가려는 거지, 아직 화상을 입은 건 아니에요.','method.current_routine','environment.flame_exposure'),part('지금 피부 통증이나 불편은 없어요.','skin.pain','skin.current_discomfort')],
    [part('손크림 쓰고 있는데 친구는 이 성분에 알레르기가 있대요. 저도 조심해야 할까요?','method.other_person_report'),
     part('친구가 말한 성분은 프로필렌글리콜이에요. 제 알레르기 이력은 잘 모르겠어요.','method.other_person_report','skin.known_allergens'),part('저는 손에만 바르고 있고, 현재 통증이나 불편은 없어요.','method.current_routine','skin.pain','skin.current_discomfort')],
    [part('물놀이하면서 선크림 바른 지 세 시간 됐는데, 다시 발라야 하나요?','sun.activity'),
     part('지금 야외 물놀이 중이고 처음 바른 뒤에는 안 발랐어요.','sun.activity'),part('내수성 표시는 아직 확인 안 했어요.','sun.product_water_resistance'),part('피부가 아프거나 불편하지는 않아요.','skin.pain','skin.current_discomfort')],
    [part('친구는 선크림 바르고 아팠다는데, 저는 얼굴에만 발라도 될까요?','method.other_person_report','sun.activity','constraints.goals'),
     part('저는 지금 통증이나 불편은 없어요.','skin.pain','skin.current_discomfort'),part('지금 밖에 있고 목이랑 귀는 드러나 있는데 얼굴에만 발랐어요.','sun.activity')],
    [part('오늘 세수하고 나서 불편한 게 계속되는데 어떻게 해야 해요?','skin.current_discomfort','method.current_routine'),
     part('지금도 계속 불편하고 살짝 아프기도 해요. 뭐 때문인지는 모르겠어요.','skin.current_discomfort','skin.pain','method.current_routine')],
    [part('팔에 보습제 바른 뒤로 많이 아픈데 어떡하죠?','skin.pain','method.current_routine'),
     part('지금 통증이 심해요. 어떤 성분 때문인지는 모르겠어요.','skin.pain','method.current_routine')],
    [part('선크림 냄새가 전이랑 달라졌는데, 써도 되는 건가요?','storage.sensory_change','storage.change_details','method.current_routine'),
     part('색은 그대로고 층이 나뉜 것도 없어요. 냄새가 바뀐 뒤로는 아직 안 발랐어요.','storage.sensory_change','storage.change_details','method.current_routine'),part('지금 피부가 아프거나 불편한 건 없어요.','skin.pain','skin.current_discomfort')],
    [part('의사 선생님이 정해 준 관리법이 있는데, 세수 횟수는 좀 바꿔도 될까요?','method.clinician_plan','constraints.goals')],
    [part('세수하고 나서 눈 주변이 아픈데 어떻게 해야 하나요?','skin.distribution','method.current_routine'),
     part('지금 중간 정도로 아파요. 제품이 눈 안에 들어갔는지는 잘 모르겠어요.','skin.pain','method.eye_contact')],
    [part('보습제가 원래 안 이랬는데 층이 나뉘었어요. 계속 써도 돼요?','storage.sensory_change','method.current_routine'),
     part('색이랑 냄새는 그대로예요. 왜 나뉜 건지는 모르겠어요.','storage.sensory_change'),part('지금 피부가 아프거나 불편하지는 않아요.','skin.pain','skin.current_discomfort')]
]

def main():
    assert not (OUT/'context_change_record.json').exists(),'이미 고정한 개정 3을 덮어쓰지 않아요.'
    plan=json.loads((HERE/'pilot_24_inputs.json').read_text(encoding='utf-8'))
    assert len(plan['cases'])==len(CONVERSATIONS)==24
    changes=[]
    for case,parts in zip(plan['cases'],CONVERSATIONS):
        before=deepcopy(case)
        req=case['request']; obs=req['confirmed_observations']
        routine=obs.get('method.current_routine')
        if routine:
            if routine['value'].get('actual_site')=='forearms':
                routine['value']['actual_site']='arms'
            for key in ['product_id','held_product_id','version','label_version_matches','current_version_confirmed','actual_application_not_reported']:
                routine['value'].pop(key,None)
            if not routine['value']:
                del obs['method.current_routine']
        not_collected=[]
        if case['id']=='syn-sol-0009':
            obs['method.actual_application']={'variable_id':'method.actual_application','state':'not_asked','value':None,'source':'synthetic_fixture','confirmed_by_user':False}
            not_collected.append('method.actual_application')
        if case['id']=='syn-hold-0004':
            obs['method.clinician_plan']['value'].pop('full_plan_provided',None)
            obs['method.clinician_plan_details']={'variable_id':'method.clinician_plan_details','state':'not_asked','value':None,'source':'synthetic_fixture','confirmed_by_user':False}
            not_collected.append('method.clinician_plan_details')
        case['scenario_raw']=parts[0]['text']
        case['user_utterance']=parts[0]['text']
        case['prior_user_confirmations']=[{'id':f'prior-{i:02d}',**p} for i,p in enumerate(parts[1:],1)]
        trace={}
        for key,observation in obs.items():
            if key in not_collected:
                trace[key]={'origin':'not_collected','evidence':[],'note':'사용자에게서 수집하지 않은 정보이며 없음으로 바꾸지 않아요.'}
            elif key=='product.ph':
                trace[key]={'origin':'synthetic_catalog_lookup_fixture','evidence':[{'product_id':p['product_id'],'label_guidance':p['label_guidance']} for p in req['product_evidence']],
                            'note':'사용자 발화에서 pH를 확정한 것이 아니라 제품 자료에 수치가 없는 상태예요.'}
            else:
                evidence=[{'origin':'synthetic_initial_utterance' if i==0 else 'synthetic_prior_confirmation','text':p['text']} for i,p in enumerate(parts) if key in p['supports']]
                assert evidence,(case['id'],key)
                trace[key]={'origin':'synthetic_user_context','evidence':evidence,'normalized_state':observation['state']}
        case['observation_trace']=trace
        case['system_context']={'notice':'실제 카탈로그 조회·AFA 실행 기록이 아니라 합성 입력 제작용 설정이에요.',
            'product_evidence_source':'synthetic_catalog_lookup_fixture','product_match_records':[]}
        for p in req['product_evidence']:
            match='verified' if p['status']=='verified' else 'unconfirmed'
            case['system_context']['product_match_records'].append({'product_id':p['product_id'],'catalog_record_version':p['version'],'current_container_match':match,
                'label_guidance':p['label_guidance'],'status':p['status'],'origin':'synthetic_catalog_lookup_fixture','real_lookup_executed':False})
        case['input_sha256']=sha(req)
        changes.append({'id':case['id'],'before_user_text':before['scenario_raw'],'after_user_text':case['user_utterance'],
                        'before_request_raw':before['request'],'after_request_raw':req,'observation_trace':trace,
                        'reason':'사용자 발화·이전 사용자 확인·카탈로그 확인·미수집 상태를 구분해요. 합성 배경을 실제 자연어 입력이나 실제 조회 결과로 부르지 않아요.'})
    plan['plan_revision']=3
    plan['revision_output_dir']='outputs/qlora_v3_pilot_20261125/revision_03'
    plan['previous_archive']='outputs/qlora_v3_pilot_20261125/revision_03/before'
    plan['authoring_note']='사용자 발화와 별도 확인, 가상 카탈로그 근거를 분리한 개정 3이에요. 자연어 발화·추적표는 검토용이고 SLMRequest에는 계약대로 정형 관찰·제품·문헌만 넣어요. 실제 NLU/AFA·제품 조회·사람 승인은 실행하지 않았어요.'
    write=lambda path,value:path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    write(HERE/'pilot_24_inputs.json',plan)
    write(OUT/'context_change_record.json',{'revision':3,'changes':changes})
    write(OUT/'inputs_frozen.json',{'inputs_sha256':sha(plan),'input_hashes':{c['id']:c['input_sha256'] for c in plan['cases']}})
    print('자연어 발화 24건, 별도 사용자 확인 및 관찰 출처 추적, 카탈로그 메타데이터 분리 완료.')

def correct_arm_precision():
    path=HERE/'pilot_24_inputs.json'
    plan=json.loads(path.read_text(encoding='utf-8'))
    changes=[]
    for case in plan['cases']:
        routine=case['request']['confirmed_observations'].get('method.current_routine')
        if routine and routine['value'].get('actual_site')=='forearms':
            before=deepcopy(routine)
            routine['value']['actual_site']='arms'
            case['input_sha256']=sha(case['request'])
            changes.append({'id':case['id'],'before_raw':before,'after_raw':routine,'reason':'사용자는 팔이라고만 말했으므로 아래팔로 좁혀 단정하지 않아요.'})
    path.write_bytes((json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    (OUT/'arm_site_precision_change.json').write_bytes((json.dumps(changes,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('부위 표현 정밀도 수정:',len(changes),'건')

def remove_debug_evidence():
    record=OUT/'debug_metadata_separation.json'
    assert not record.exists()
    path=HERE/'pilot_24_inputs.json'
    plan=json.loads(path.read_text(encoding='utf-8'))
    changes=[]
    for case in plan['cases']:
        for product in case['request']['product_evidence']:
            debug=product.pop('verification_fixture',None)
            if debug:
                changes.append({'id':case['id'],'product_id':product['product_id'],'removed_from_model_input':debug,'reason':'합성 제작·실행 여부는 모델의 제품 사실이 아니라 별도 작성 이력이에요.'})
        for item in case['system_context']['product_match_records']:
            item.update({'origin':'synthetic_catalog_lookup_fixture','real_lookup_executed':False})
        case['input_sha256']=sha(case['request'])
    path.write_bytes((json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    record.write_bytes((json.dumps(changes,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('제작용 메타데이터를 별도 기록으로 이동:',len(changes),'건')

if __name__=='__main__':
    if '--correct-arm-site' in sys.argv:
        correct_arm_precision()
    elif '--remove-debug-evidence' in sys.argv:
        remove_debug_evidence()
    else:
        main()
