import hashlib
import json
from pathlib import Path
import build_additional_24 as common
import create_200_cd_inputs as c

HERE=Path(__file__).resolve().parent
chunks={}
for f in HERE.glob('*part*_inputs.json'):
    data=json.loads(f.read_text(encoding='utf-8'))
    for case in data['cases']:
        for chunk in case['request']['rag_chunks']:
            if chunk['evidence_ref'] in ('ref:S23','ref:S25','ref:S32'):
                chunks.setdefault(chunk['evidence_ref'],chunk)

# 제목, 관찰, 기준, 상태, 판단 범위, hard negative
D=[
 ('얼굴 수동 면도의 털 방향', '얼굴을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 반복 통과를 줄여요.', 'B-G10','aligned','확인된 부드러운 수동 면도 방법을 유지해요.',None),
 ('목 수동 면도의 압력', '목을 수동 날면도로 깎으며 강하게 누르지 않고 털 방향으로 움직여요. 같은 곳을 반복하지 않아요.', 'B-G10','aligned','확인된 압력과 방향, 반복 관리에 한정해 유지해요.',None),
 ('턱 수동 면도의 반복 통과', '얼굴의 턱을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 같은 곳의 반복 통과를 줄여요.', 'B-G10','aligned','확인된 얼굴 수동 면도 방법을 유지해요.',None),
 ('친구의 역방향과 본인', '친구는 얼굴을 수동 날면도할 때 강하게 역방향으로 깎아요. 본인의 얼굴 수동 날면도 압력과 방향은 확인되지 않았어요.', 'B-G10','unknown','친구의 동작을 본인의 면도 방법으로 옮기지 않아요.','negation_or_other_subject'),
 ('목의 수동 면도 방향 미상', '목을 수동 날면도로 깎아요. 털 방향과 압력, 반복 통과는 확인하지 못했어요.', 'B-G10','unknown','사용 부위와 도구는 알려져 있으나 세부 동작은 미상이에요.','version_mismatch_or_unknown'),
 ('얼굴 면도 불편을 무시한 강한 압력', '얼굴을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강하게 누르고 여러 번 같은 곳을 지나가요.', 'B-G10','difference','불편을 무시한 강한 압력과 반복 통과를 검토해요.',None),
 ('목 면도의 역방향 고수', '목을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강한 역방향 면도를 계속해요.', 'B-G10','difference','불편을 무시한 강한 역방향 면도를 검토해요.',None),
 ('얼굴 면도의 압력 답변 거절', '얼굴을 수동 날면도로 깎아요. 면도 압력과 방향에 대해서는 답하고 싶지 않아요.', 'B-G10','unknown','답변 거절을 강한 면도로 바꾸지 않아요.','version_mismatch_or_unknown'),
 ('이전과 현재 수동 면도 분리', '예전에 얼굴 수동 날면도에서 강하게 눌렀어요. 현재는 털 방향으로 가볍게 움직이고 반복 통과를 줄여요.', 'B-G10','aligned','이전 동작과 확인된 현재 동작을 나누어 살펴요.','negation_or_other_subject'),
 ('면도기 날 개수 미상', '얼굴을 수동 날면도로 깎고 털 방향으로 가볍게 움직이며 반복 통과를 줄여요. 날의 개수는 확인하지 못했어요.', 'B-G10','aligned','확인된 방법을 살피며 날 개수를 추측하지 않아요.','version_mismatch_or_unknown'),
 ('얼굴 면도 후 편안한 보습', '얼굴 면도 후 현재 보습제를 바르고 편안해요. 별도의 애프터셰이브는 쓰지 않아요.', 'B-M05','aligned','견딜 수 있는 면도 후 보습을 유지해요.',None),
 ('목 면도 후 특정 제품의 반복 따가움', '목 면도 후 후처리 제품을 바를 때마다 따갑지만 흡수되는 느낌이라며 계속 사용해요.', 'B-M05','difference','반복 따가움을 흡수 효과로 해석해 계속 사용하는 행동을 검토해요.',None),
 ('얼굴 후처리 반응 미상', '얼굴 면도 후 보습제를 발라요. 바른 뒤의 반응은 확인되지 않았어요.', 'B-M05','unknown','보습 사용 사실과 사용 반응의 미확인을 구분해요.','version_mismatch_or_unknown'),
 ('목 면도 뒤 보습 거절 답변', '목을 면도해요. 면도 뒤 보습 여부에 관한 답변은 원하지 않아요.', 'B-M05','unknown','답변 거절을 보습 중단으로 바꾸지 않아요.','version_mismatch_or_unknown'),
 ('타인의 후처리 따가움', '친구는 얼굴 면도 후 쓰는 제품이 따갑다고 해요. 본인의 얼굴 면도 후 제품과 반응은 알려지지 않았어요.', 'B-M05','unknown','친구의 반응을 본인의 후처리 반응으로 옮기지 않아요.','negation_or_other_subject'),
 ('목 면도 뒤 모든 보습 중단', '목 면도 후 보습이 필요하다고 느끼지만 따가운 후처리 제품 하나 때문에 모든 보습을 중단했어요.', 'B-M05','difference','특정 후처리 제품의 반응과 보습 전체 중단을 분리해요.',None),
 ('얼굴 면도 뒤 예전 제품과 현재 제품', '얼굴 면도 뒤 예전 후처리 제품은 따가웠어요. 다른 현재 보습제는 사용 후 편안해요.', 'B-M05','aligned','예전 후처리 제품과 현재 견디는 보습제를 구분해요.','negation_or_other_subject'),
 ('목 면도 뒤 별도 상품 미사용', '목 면도 후 보습제를 사용해 편안해요. 별도 애프터셰이브는 사용하지 않아요.', 'B-M05','aligned','확인된 편안한 보습을 살피며 별도 상품을 강제하지 않아요.',None),
 ('얼굴 레티놀과 AHA 제품 동시 사용', '얼굴에 레티놀 관리용 화장품과 AHA 각질관리용 화장품을 별도 제품으로 같은 저녁 루틴에 함께 사용해요.', 'B-G13','difference','같은 부위의 별도 관리제품 중첩을 검토해요.',None),
 ('목 레티놀과 AHA 겹치는 기간', '목에 레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 사용하는 날은 달라요.', 'B-G13','difference','같은 부위와 겹치는 사용기간을 확인하고 날짜 분리만으로 적합하다고 정하지 않아요.',None),
 ('레티놀과 AHA 접촉 부위 미상', '레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 각각 바르는 부위는 확인하지 못했어요.', 'B-G13','unknown','같은 부위에 접촉하는지 미상으로 남겨요.','version_mismatch_or_unknown'),
 ('AHA 포함만 확인된 제품', '얼굴에 레티놀 관리 제품과 별도 화장품을 같은 기간에 사용해요. 별도 화장품에는 AHA 성분이 있지만 각질관리 목적인지는 몰라요.', 'B-G13','unknown','성분 포함과 각질관리 목적을 구분해요.','version_mismatch_or_unknown'),
 ('관리 목적만 알려진 제품', '얼굴에 레티놀 관리 제품과 별도 각질관리 제품을 같은 기간에 사용해요. 각질관리 제품의 성분은 확인하지 못했어요.', 'B-G13','unknown','각질관리 목적만으로 AHA 성분을 확인된 사실로 만들지 않아요.','version_mismatch_or_unknown'),
 ('서로 다른 부위의 두 제품', '레티놀 관리용 화장품은 얼굴에, AHA 각질관리용 별도 화장품은 손에 같은 기간 사용해요. 두 제품의 실제 접촉 부위는 겹치지 않아요.', 'B-G13','exception','확인된 다른 부위에 동일 부위 중첩을 적용하지 않아요.','negation_or_other_subject'),
 ('단일 복합 완제품', '레티놀과 AHA가 함께 든 단일 복합 완제품을 얼굴에 사용해요. 같은 관리 목적의 다른 제품은 사용하지 않아요.', 'B-G13','exception','단일 복합 완제품은 별도 제품 중첩과 나누어 제품별로 검토해요.','negation_or_other_subject'),
 ('처방 레티노이드와 AHA의 계획', '얼굴에 처방 레티노이드와 별도 AHA 각질관리 화장품을 같은 기간 사용해요. 의료진의 병용 지시 여부는 아직 확인하지 못했어요.', 'B-G13','unknown','처방 여부와 미확인 병용 지시를 구분하고 처방을 임의 변경하지 않아요.','version_mismatch_or_unknown'),
]

H=[
 ('얼굴 면도 부위 지속 불편', '얼굴 면도 부위의 불편이 지속돼요.'),
 ('목 면도 후 지속 불편', '목 면도 후 불편이 계속돼요. 원인은 확인되지 않았어요.'),
 ('면도 후 제품과 지속 불편', '얼굴 면도 후 제품을 바른 뒤 불편이 계속돼요.'),
 ('면도 방법 질문과 지속 불편', '수동 날면도하는 얼굴 부위에 불편이 지속돼서 압력을 어떻게 바꿀지 묻고 있어요.'),
 ('목 보습 질문과 지속 불편', '목 면도 부위에 불편이 지속되어 보습 횟수를 묻고 있어요.'),
 ('얼굴 관리 제품과 지속 불편', '얼굴에 쓰는 두 관리 제품의 사용 기간 중 불편이 지속돼요. 어느 제품 때문인지는 몰라요.'),
 ('면도 후 지속 불편과 원인 미상', '얼굴 면도 후 불편이 계속돼요. 면도와 제품 중 원인은 확인되지 않았어요.'),
]

def make(i,row):
    title,obs,card,status,guide,hn=row
    rid=f'syn-sol-{422+i:04d}'
    ref={'B-G10':'ref:S23','B-M05':'ref:S25','B-G13':'ref:S32'}[card]
    chunk=dict(chunks[ref])
    if card=='B-G10':
        chunk['text']='Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.' if i<9 else '수동 날면도 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. 준비와 면도날 관리도 함께 안내해요.'
    elif card=='B-M05':
        chunk['text']='일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.'
    else:
        chunk['text']='일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.'
    v='method.current_routine'
    req={'mode':'solution','confirmed_observations':{v:{'variable_id':v,'state':'known','value':obs,'source':'synthetic_fixture','confirmed_by_user':True}},'kb_judgments':[{'card_id':card,'status':status,'guidance':guide}],'product_evidence':[],'rag_chunks':[chunk],'allowed_evidence_refs':[f'kb:{card}@0.6.1',ref],'distractor_refs':[]}
    common.validator.SLMRequest.model_validate(req)
    case={'id':rid,'title':title,'pilot_bucket':'unknown_or_version' if status=='unknown' else 'normal_guidance','mode':'solution','scenario_id':f'terra200-d-{rid}-scenario','group_id':f'terra200-d-{rid}-group','scenario_family_id':f'terra200-d-{rid}-family','split':'train','domains':['moisturizing'] if card=='B-M05' else ['cross_domain'],'card_ids':[card],'is_hard_negative':bool(hn),'hard_negative_type':hn,'chunk_origins':{ref:'kb_source_summary'},'request':req,'input_sha256':hashlib.sha256(common.canonical(req).encode('utf-8')).hexdigest(),'judgment_basis':{'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card,'comparison_spec':c.CARDS[card]['comparison_spec'],'rationale':guide},'source_origin':'new_synthetic','source_scenario_id':None,'source_turn_id':None,'source_note':'합성 개발 사례이며 실제 사용자 기록이나 엔진 실행 결과가 아니에요.','novelty_note':'부위와 사용 시점, 제품과 관찰 범위를 구분해요.'}
    if i in (0,1,2):
        case['group_id']='add24-group-wet-shaving-technique'
        case['scenario_family_id']='add24-family-wet-shaving-technique'
        case['split']='val_internal'
    return case

def hold(i,row):
    title,obs=row
    case=c.make_hold(i,(title,obs))
    rid=f'syn-hold-{131+i:04d}'
    case.update(id=rid,scenario_id=f'terra200-d-{rid}-scenario',group_id=f'terra200-d-{rid}-group',scenario_family_id=f'terra200-d-{rid}-family',novelty_note='면도 또는 관리 제품 사용과 지속 불편의 원인을 구분해요.')
    return case

def main():
    data={'schema_version':'additional-pilot-shard-v1','input_revision':1,'revision_note':'응답 작성 전에 고정한 미검수 합성 입력이에요.','mode':'development_preview','production_enabled':False,'cases':[make(i,r) for i,r in enumerate(D)]+[hold(i,r) for i,r in enumerate(H)]}
    path=HERE/'additional_200_terra_part_d_inputs.json'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(len(data['cases']),hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__': main()
