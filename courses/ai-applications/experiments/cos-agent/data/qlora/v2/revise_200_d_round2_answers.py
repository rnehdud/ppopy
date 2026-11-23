import hashlib
import json
from pathlib import Path
import build_additional_24 as common

HERE=Path(__file__).resolve().parent
p=HERE/'additional_200_terra_part_d_inputs.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='e1b624f3c3afe603ae210d873418072f1ce066dda60d5ca63c0f50d21d32ebe6'
data=json.loads(p.read_text(encoding='utf-8'))
old=json.loads((common.COS/'outputs/additional_200_cd_revision2/additional_200_terra_part_d.json').read_text(encoding='utf-8'))
byid={c['id']:c for c in old['cases']}
for case in data['cases']:
    previous=byid[case['id']]
    answer=previous['answer']
    if case['id'] in ('syn-sol-0425','syn-sol-0436'):
        for oldtext,newtext in [
            (previous['request']['confirmed_observations']['method.current_routine']['value'],case['request']['confirmed_observations']['method.current_routine']['value']),
            (previous['request']['kb_judgments'][0]['guidance'],case['request']['kb_judgments'][0]['guidance'])]:
            assert oldtext in answer
            answer=answer.replace(oldtext,newtext)
    case['answer']=answer
out=HERE/'additional_200_terra_part_d.json'
out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(out.read_bytes()).hexdigest())
