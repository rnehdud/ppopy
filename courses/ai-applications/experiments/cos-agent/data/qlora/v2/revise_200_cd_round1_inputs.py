import hashlib
import json
from pathlib import Path
import shutil
import build_additional_24 as common

HERE=Path(__file__).resolve().parent
OUT=common.COS/'outputs/additional_200_cd_revision1'
OUT.mkdir(parents=True,exist_ok=True)
names=[f'additional_200_terra_part_{p}{s}.json' for p in 'cd' for s in ('_inputs','')]
for name in names:
    source=HERE/name
    archive=OUT/name
    if not archive.exists():
        shutil.copyfile(source,archive)
    else:
        assert archive.read_bytes()==source.read_bytes(), '원본 보관물이 이미 존재하고 현재 파일이 달라요.'

def family(case, group, fam, split):
    case['group_id']=group; case['scenario_family_id']=fam; case['split']=split

def clear_hn(case):
    case['is_hard_negative']=False;case['hard_negative_type']=None

def revision(part):
    path=HERE/f'additional_200_terra_part_{part}_inputs.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    data['input_revision']=2
    data['revision_note']='독립 내부 검토에 따라 분할·방어 유형을 정정하고 적용 범위가 없는 두 합성 사례를 명시적으로 교체한 뒤 응답 수정 전에 고정했어요.'
    for case in data['cases']:
        rid=case['id']; n=int(rid.rsplit('-',1)[1]); changes=[]
        if case['mode']=='solution' and part=='c':
            if n in (397,404,405,406,407):
                family(case,'terra3-b-group-syn-sol-0296','terra3-b-family-syn-sol-0296','val_internal');changes.append('타인의 보습과 본인 미상의 기존 가족·분할 재사용')
            if n in (396,400,410,416):
                family(case,'terra200-c-syn-sol-0396-group','terra200-c-syn-sol-0396-family','train');changes.append('손 씻기 후 견디는 현재 보습 가족 통합')
            if n in (398,418):
                family(case,'terra200-c-syn-sol-0398-group','terra200-c-syn-sol-0398-family','train');changes.append('건조한 손 방치 가족 통합')
            if n in (399,417):
                family(case,'terra200-c-syn-sol-0399-group','terra200-c-syn-sol-0399-family','train');changes.append('특정 제품의 반복 불편과 계속 사용 가족 통합')
            if n in (400,401,402,403,408,409,411,412,413,414,415,418,419):
                clear_hn(case);changes.append('지정된 네 방어 유형에 맞지 않는 HN 표기 삭제')
        if case['mode']=='solution' and part=='d':
            if n in (422,423,424,430,431):
                family(case,'add24-group-wet-shaving-technique','add24-family-wet-shaving-technique','val_internal');changes.append('기존 수동 면도 기술 가족·분할 재사용')
            if n in (432,439):
                family(case,'add100-a-group-syn-sol-0045','add100-a-family-면도 후 편안한 보습에 별도 상품 의무 없음','val_internal');changes.append('기존 면도 후 편안한 보습 가족·분할 재사용')
            if n in (426,429,430,431,434,435,438,442,443,444,447):
                clear_hn(case);changes.append('지정된 네 방어 유형에 맞지 않는 HN 표기 삭제')
            if n in (425,436):
                old=case['input_sha256']
                obs=case['request']['confirmed_observations']['method.current_routine']
                if n==425:
                    obs['value']='본인은 얼굴을 수동 날면도로 깎지만 압력과 방향은 확인되지 않았어요. 친구는 얼굴 수동 날면도에서 강하게 역방향으로 깎아요.'
                else:
                    obs['value']='본인은 얼굴을 면도해요. 친구는 얼굴 면도 후 쓰는 제품이 따갑다고 하지만 본인의 면도 후 제품과 반응은 알려지지 않았어요.'
                case['input_sha256']=hashlib.sha256(common.canonical(case['request']).encode('utf-8')).hexdigest()
                case['replaced_case']={'previous_input_sha256':old,'reason':'이전 합성 사례는 본인의 실제 면도 적용 범위가 확인되지 않아 명시된 새 합성 사례로 교체했어요. 누락 사실을 추론한 것이 아니에요.'}
                changes.append('범위 불명 사례를 본인 실제 면도가 명시된 새 합성 입력으로 교체')
        if changes:
            case['revision_history']=[{'revision':'200-cd-round1','reason':' '.join(changes),'human_review':'unreviewed'}]
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(part,len(data['cases']),hashlib.sha256(path.read_bytes()).hexdigest(),sum(x['is_hard_negative'] for x in data['cases']))

if __name__=='__main__':
    revision('c');revision('d')
