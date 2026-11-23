import hashlib
import json
from pathlib import Path
import shutil
import build_additional_24 as common

HERE=Path(__file__).resolve().parent
OUT=common.COS/'outputs/additional_200_cd_revision2'
OUT.mkdir(parents=True,exist_ok=True)
for suffix in ('_inputs',''):
    name=f'additional_200_terra_part_d{suffix}.json'
    archive=OUT/name
    if not archive.exists():shutil.copyfile(HERE/name,archive)
    else:assert archive.read_bytes()==(HERE/name).read_bytes()
p=HERE/'additional_200_terra_part_d_inputs.json'
data=json.loads(p.read_text(encoding='utf-8'))
data['input_revision']=3
data['revision_note']='독립 검토에서 기존 상황에 사실만 덧붙인 두 행을 지적하여 서로 다른 새 합성 상황과 새 식별자로 교체했어요. 응답 작성 전에 고정했어요.'
replacements={
 'syn-sol-0425':('동료의 목 면도와 본인의 볼 면도','본인은 볼을 수동 날면도해요. 이때 본인의 방향과 압력은 기억나지 않아요. 직장 동료는 다른 날 목을 수동 날면도할 때 강하게 누른다고 해요.','동료의 목 면도 압력을 본인의 볼 면도 압력으로 옮기지 않아요.'),
 'syn-sol-0436':('동거인의 얼굴 후처리와 본인의 목 보습','본인은 목을 면도해요. 목 면도 후의 보습 사용 여부와 반응은 확인되지 않았어요. 동거인은 별도로 얼굴 면도 후 사용한 후처리 제품이 따갑다고 해요.','동거인의 얼굴 제품 반응을 본인의 목 면도 후 반응으로 옮기지 않아요.'),
}
for case in data['cases']:
    if case['id'] not in replacements:continue
    rid=case['id']; title,obs,guide=replacements[rid]
    prev=case['input_sha256']; prior=case.get('replaced_case',{}).get('previous_input_sha256')
    case['title']=title
    case['scenario_id']=f'terra200-d-r2-{rid}-scenario'
    case['group_id']=f'terra200-d-r2-{rid}-group'
    case['scenario_family_id']=f'terra200-d-r2-{rid}-family'
    req=case['request']
    req['confirmed_observations']['method.current_routine']['value']=obs
    req['kb_judgments'][0]['guidance']=guide
    case['judgment_basis']['rationale']=guide
    case['input_sha256']=hashlib.sha256(common.canonical(req).encode('utf-8')).hexdigest()
    case['replaced_case']={'previous_input_sha256':prev,'initial_input_sha256':prior,'reason':'이전 수정이 기존 사례에 적용 사실만 추가한 문제를 남겨 실제 면도 주체·부위·다른 사람의 상황이 구별되는 새 합성 상황과 새 가족으로 교체했어요. 이전 관찰의 누락 사실을 추론하지 않았어요.'}
    case['revision_history'].append({'revision':'200-cd-round2','reason':'기존 입력 사실 추가 방식 대신 새 합성 상황 및 식별자로 교체했어요.','human_review':'unreviewed'})
    common.validator.SLMRequest.model_validate(req)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(p.read_bytes()).hexdigest())
