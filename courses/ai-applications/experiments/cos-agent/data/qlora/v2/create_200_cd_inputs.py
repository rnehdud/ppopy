import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]
sys.path.insert(0, str(HERE))
import build_additional_24 as common

KB = json.loads((COS.parents[3] / 'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
CARDS = {c['id']: c for c in KB['baseline_cards']}
PREV = json.loads((HERE / 'additional_100_terra3_part_b_inputs.json').read_text(encoding='utf-8'))
S21 = next(x for c in PREV['cases'] for x in c['request']['rag_chunks'] if x['evidence_ref'] == 'ref:S21')

# 제목, 관찰, 상태, 해당 판단의 범위, hard negative 유형
C = [
 ('손 씻은 뒤 편안한 보습', '손을 씻은 뒤 현재 쓰는 핸드크림을 바르며 이 제품을 바를 때 불편하지 않아요. 필요한 손 위생은 유지하고 있어요.', 'exception', '현재 견딜 수 있는 손 보습을 개별 지시와 함께 살펴요.', None),
 ('동료의 보습은 본인 기록이 아님', '본인은 필요한 손 씻기를 해요. 동료는 손을 씻은 뒤 보습하지만 본인의 보습 여부는 말하지 않았어요.', 'unknown', '동료의 행동으로 본인의 보습 여부를 대신하지 않아요.', 'negation_or_other_subject'),
 ('건조한 손을 일부러 계속 방치', '손이 건조한데도 손 보습을 계속 하지 않고 건조하게 두고 있어요. 손 위생은 유지해요.', 'difference', '손 건조를 계속 방치하는 현재 행동을 검토해요.', None),
 ('특정 핸드크림의 반복 불편', '손에 같은 핸드크림을 바를 때마다 불편하지만 계속 쓰고 있어요. 다른 제품에 대한 반응은 몰라요.', 'difference', '반복 불편이 있는 해당 제품의 사용을 검토해요.', None),
 ('향 표시는 아직 미확인', '손 씻은 뒤 핸드크림을 바르지만 용기의 향료 표시를 읽지 못했어요. 이 제품을 바를 때 불편하지 않아요.', 'exception', '현재 견디는 제품의 유지와 미확인 표시를 구분해요.', 'version_mismatch_or_unknown'),
 ('손 보습 답변 거절', '필요한 손 위생을 유지해요. 손 보습 사용 여부에 관한 답변은 원하지 않아요.', 'unknown', '답변 거절을 보습하지 않는다는 뜻으로 바꾸지 않아요.', 'version_mismatch_or_unknown'),
 ('무향 표시와 개인 반응', '손에 쓰는 핸드크림에 무향료라고 적혀 있지만 바를 때마다 불편해요. 그래도 현재 계속 사용해요.', 'difference', '무향료 표시와 그 제품의 반복 불편을 별도로 고려해요.', 'negation_or_other_subject'),
 ('손 씻기는 유지하고 보습은 미상', '손을 자주 씻으며 필요한 손 위생은 유지해요. 손 보습을 하는지는 확인되지 않았어요.', 'unknown', '손 씻는 사실만으로 손 보습 행동을 판단하지 않아요.', 'version_mismatch_or_unknown'),
 ('가족의 크림과 본인의 미상', '가족은 손 씻은 뒤 보습제를 써요. 본인이 손에 보습제를 쓰는지는 확인되지 않았어요.', 'unknown', '가족의 보습 행동을 본인에게 옮기지 않아요.', 'negation_or_other_subject'),
 ('동료의 보습 시간과 본인', '동료는 근무 뒤 손에 보습제를 바른다고 해요. 본인의 손 보습 시간은 확인되지 않았어요.', 'unknown', '동료의 시간으로 본인의 손 보습을 정하지 않아요.', 'negation_or_other_subject'),
 ('친구의 보습 경험과 본인', '친구는 손을 씻고 크림을 쓴다고 해요. 본인이 손을 씻은 후 보습하는지는 몰라요.', 'unknown', '친구의 사용을 본인의 사용으로 판단하지 않아요.', 'negation_or_other_subject'),
 ('동거인의 손 씻기 뒤 보습', '동거인은 손 씻기 후에 보습해요. 본인은 손 씻기를 하지만 손 보습 여부는 답하고 싶지 않아요.', 'unknown', '동거인의 기록과 본인의 답변 거절을 구분해요.', 'negation_or_other_subject'),
 ('작업 뒤 손 보습의 반응 미상', '젖은 작업을 한 뒤 손에 핸드크림을 발라요. 사용했을 때의 개인 반응은 아직 말하지 않았어요.', 'unknown', '사용과 개인 반응 미확인을 구분해요.', 'version_mismatch_or_unknown'),
 ('무향료 표기와 오일 미상', '손 보습 후보에 무향료라고 적혀 있어요. 향성 에센셜오일 포함 여부는 확인하지 못했어요.', 'unknown', '무향료 표기만으로 향성 에센셜오일 여부를 정하지 않아요.', 'version_mismatch_or_unknown'),
 ('손 위생과 보습 유지', '필요한 손 씻기를 계속하고 씻은 뒤 현재 핸드크림을 발라요. 이 제품 사용에 불편은 없고 진료 지시는 없어요.', 'exception', '견딜 수 있는 현재 손 보습과 필요한 위생을 함께 고려해요.', None),
 ('손 작업 노출과 보습 미상', '손이 물에 자주 닿는 작업을 해요. 작업 후 보습 여부와 제품 반응은 알 수 없어요.', 'unknown', '습식 작업만으로 보습 행동이나 제품 반응을 만들지 않아요.', 'version_mismatch_or_unknown'),
 ('과거 제품 반응과 현재 제품', '이전 핸드크림은 손에 불편했어요. 지금 쓰는 다른 핸드크림은 편안하고 손 씻기 후 사용해요.', 'exception', '이전 제품의 불편과 현재 제품의 관찰을 나누어요.', 'negation_or_other_subject'),
 ('진료 지시 확인 중인 손 보습', '손에 보습제를 쓰고 있어요. 보습에 관한 개별 진료 지시가 있는지는 아직 확인하지 못했어요.', 'unknown', '개별 진료 지시의 유무를 추측하지 않아요.', 'version_mismatch_or_unknown'),
 ('손에 바르지 않는 얼굴 제품', '얼굴 보습제는 편안해요. 손 보습 제품의 사용 여부와 반응은 모른다고 해요.', 'unknown', '얼굴 제품 경험을 손 제품 경험으로 옮기지 않아요.', 'negation_or_other_subject'),
 ('핸드크림 이름과 향료', '손에 바를 후보는 핸드크림이에요. 전성분이나 향료 표시는 확인하지 못했어요.', 'unknown', '제품 이름만으로 향료나 향성 오일을 판정하지 않아요.', 'version_mismatch_or_unknown'),
 ('손 위생 뒤 보습과 작업 미상', '손 씻기 뒤 편안한 핸드크림을 쓰고 있어요. 그 밖의 젖은 작업 여부는 확인되지 않았어요.', 'exception', '현재 견디는 손 보습을 유지하면서 작업 정보는 미상으로 두어요.', None),
 ('반복 불편과 손 위생', '필요한 손 씻기를 유지하며 핸드크림을 사용해요. 해당 크림을 바를 때마다 불편한데도 계속 사용해요.', 'difference', '필요한 손 위생과 특정 제품의 반복 불편을 분리해요.', None),
 ('손 건조와 전면 중단', '손이 건조하다고 느끼는데 보습제를 모두 끊고 손을 계속 건조하게 두어요. 진단받은 질환은 말하지 않았어요.', 'difference', '손을 계속 건조하게 두는 행동을 검토하되 진단은 만들지 않아요.', 'negation_or_other_subject'),
 ('고정유와 향성 오일 구별', '손 보습 후보의 표시에서 미네랄오일을 봤어요. 향료와 향성 에센셜오일은 확인하지 못했어요.', 'unknown', '미네랄오일이라는 표시를 향성 에센셜오일로 바꾸지 않아요.', 'version_mismatch_or_unknown'),
 ('이전 표시와 현재 포장', '손 보습제 예전 포장에는 무향료라고 적혀 있었어요. 현재 포장의 버전과 표시는 확인하지 못했어요.', 'unknown', '이전 표시를 현재 포장에 그대로 옮기지 않아요.', 'version_mismatch_or_unknown'),
 ('손 반응의 주체 구분', '가족은 이 핸드크림을 쓰면 불편하다고 해요. 본인의 손 사용 여부와 반응은 확인되지 않았어요.', 'unknown', '가족의 반응을 본인의 반응으로 판정하지 않아요.', 'negation_or_other_subject'),
]

C_HOLD = [
 ('손 보습 후 지속 불편', '손에 핸드크림을 바른 뒤 불편이 지속돼요.'),
 ('손 씻기와 지속 불편', '손을 씻는 일을 계속해야 하는데 손 불편이 지속돼요.'),
 ('손 보습 제품 변경 뒤 지속 불편', '손 보습 제품을 바꾼 뒤 불편이 계속돼요. 원인은 확인되지 않았어요.'),
 ('손 작업 뒤 지속 불편', '물에 손이 자주 닿는 작업을 한 뒤 손 불편이 지속돼요.'),
 ('손 보습 횟수 질문과 지속 불편', '손 불편이 지속되는 가운데 핸드크림을 몇 번 더 바를지 묻고 있어요.'),
 ('양손의 지속 불편', '양손에 불편이 계속돼요. 손에 바른 제품의 영향인지는 몰라요.'),
 ('손 제품 반응과 지속 불편', '손에 쓰는 제품을 바를 때 불편하고 그 불편이 지속돼요.'),
 ('손 건조와 지속 불편', '손이 건조하다고 느끼며 불편이 지속돼요. 별도 진단은 확인되지 않았어요.'),
]

def make_c(i, row):
    title, observation, status, guidance, hn = row
    rid = f'syn-sol-{396+i:04d}'
    var = 'method.current_routine'
    chunk = dict(S21)
    if i >= 9:
        chunk['text'] = '손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.'
    request = {'mode':'solution', 'confirmed_observations':{var:{'variable_id':var,'state':'known','value':observation,'source':'synthetic_fixture','confirmed_by_user':True}},
       'kb_judgments':[{'card_id':'B-M04','status':status,'guidance':guidance}], 'product_evidence':[],
       'rag_chunks':[chunk], 'allowed_evidence_refs':['kb:B-M04@0.6.1','ref:S21'], 'distractor_refs':[]}
    case = {'id':rid,'title':title,'pilot_bucket':'unknown_or_version' if status=='unknown' else 'normal_guidance','mode':'solution',
       'scenario_id':f'terra200-c-{rid}-scenario','group_id':f'terra200-c-{rid}-group','scenario_family_id':f'terra200-c-{rid}-family','split':'train',
       'domains':['moisturizing'],'card_ids':['B-M04'],'is_hard_negative':bool(hn),'hard_negative_type':hn,'chunk_origins':{'ref:S21':'kb_source_summary'},'request':request,
       'input_sha256':hashlib.sha256(common.canonical(request).encode('utf-8')).hexdigest(),
       'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-M04','comparison_spec':CARDS['B-M04']['comparison_spec'],'rationale':guidance},
       'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'합성 개발 사례이며 실제 사용자 기록이나 엔진 실행 결과가 아니에요.','novelty_note':'손 보습의 관찰과 확인되지 않은 정보를 구분해요.'}
    if i in (1, 8, 9, 10):
        case['group_id'] = 'terra3-b-group-syn-sol-0296'
        case['scenario_family_id'] = 'terra3-b-family-syn-sol-0296'
        case['split'] = 'val_internal'
    common.validator.SLMRequest.model_validate(request)
    return case

def make_hold(i, row):
    title, observation = row
    rid=f'syn-hold-{123+i:04d}'
    var='method.current_routine'
    req={'mode':'hold','confirmed_observations':{
        var:{'variable_id':var,'state':'known','value':observation,'source':'synthetic_fixture','confirmed_by_user':True},
        'skin.current_discomfort':{'variable_id':'skin.current_discomfort','state':'known','value':'persistent','source':'synthetic_fixture','confirmed_by_user':True}},
        'kb_judgments':[{'card_id':'B-B01','status':'hold','guidance':'지속 불편이 보고되어 개별 루틴 권고를 보류해요.'}],
        'product_evidence':[],'rag_chunks':[],'allowed_evidence_refs':['kb:B-B01@0.6.1'],'distractor_refs':[]}
    common.validator.SLMRequest.model_validate(req)
    return {'id':rid,'title':title,'pilot_bucket':'hold','mode':'hold','scenario_id':f'terra200-c-{rid}-scenario','group_id':f'terra200-c-{rid}-group','scenario_family_id':f'terra200-c-{rid}-family','split':'train','domains':['general_safety','moisturizing'],'card_ids':['B-B01'],'is_hard_negative':False,'hard_negative_type':None,'chunk_origins':{},'request':req,'input_sha256':hashlib.sha256(common.canonical(req).encode('utf-8')).hexdigest(),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':'B-B01','comparison_spec':CARDS['B-B01']['comparison_spec'],'rationale':'지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.'},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'합성 개발 사례이며 실제 사용자 기록이나 엔진 실행 결과가 아니에요.','novelty_note':'손의 지속 불편과 확인되지 않은 원인을 구분해요.'}

def save_c():
    data={'schema_version':'additional-pilot-shard-v1','input_revision':1,'revision_note':'응답 작성 전에 고정한 미검수 합성 입력이에요.','mode':'development_preview','production_enabled':False,'cases':[make_c(i,row) for i,row in enumerate(C)] + [make_hold(i,row) for i,row in enumerate(C_HOLD)]}
    path=HERE/'additional_200_terra_part_c_inputs.json'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(len(data['cases']), hashlib.sha256(path.read_bytes()).hexdigest())

if __name__ == '__main__':
    save_c()
