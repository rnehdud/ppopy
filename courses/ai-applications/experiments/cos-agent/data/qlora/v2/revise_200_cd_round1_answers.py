import hashlib
import json
from pathlib import Path
import build_additional_24 as common

HERE=Path(__file__).resolve().parent
ARCHIVE=common.COS/'outputs/additional_200_cd_revision1'
INPUT_HASHES={'c':'5931ae1b6b8f4c8287e8d09fe9d4fd1c717e211ef7ecaabcf2a4857994541b21','d':'6fa0c8674e6929c4a9ba70833c1e0af32bc1ad364fe9a573c1f0f0daa7c586a0'}
for part in 'cd':
    p=HERE/f'additional_200_terra_part_{part}_inputs.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==INPUT_HASHES[part]
    data=json.loads(p.read_text(encoding='utf-8'))
    previous=json.loads((ARCHIVE/f'additional_200_terra_part_{part}.json').read_text(encoding='utf-8'))
    old={x['id']:x for x in previous['cases']}
    for case in data['cases']:
        prev=old[case['id']]
        answer=prev['answer']
        if case['id'] in ('syn-sol-0425','syn-sol-0436'):
            oldobs=prev['request']['confirmed_observations']['method.current_routine']['value']
            newobs=case['request']['confirmed_observations']['method.current_routine']['value']
            assert oldobs in answer
            answer=answer.replace(oldobs,newobs)
        if case['id']=='syn-sol-0428':
            oldphrase='불편을 무시하며 강하게 누르거나 반복하는 방법을 조정할 여지를 살펴요.'
            assert oldphrase in answer
            answer=answer.replace(oldphrase,'불편을 무시하며 강한 역방향으로 면도하는 방법을 조정할 여지를 살펴요.')
        case['answer']=answer
    out=HERE/f'additional_200_terra_part_{part}.json'
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(part,len(data['cases']),hashlib.sha256(out.read_bytes()).hexdigest())
