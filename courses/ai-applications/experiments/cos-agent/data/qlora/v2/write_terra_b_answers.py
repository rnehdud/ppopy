"""Create answers from the frozen candidate inputs without changing inputs."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = HERE / 'additional_100_terra_part_b_inputs.json'
dest = HERE / 'additional_100_terra_part_b.json'
expected = 'e6b7c362536f570c97869271a061ddfce8746a683cc8a83b0b356734a994ad41'
raw = src.read_bytes()
if hashlib.sha256(raw).hexdigest() != expected:
    raise SystemExit('고정 입력 해시가 일치하지 않아요.')
if dest.exists():
    raise SystemExit('답변 파일이 이미 존재해요.')
d = json.loads(raw.decode('utf-8'))
assert len(d['cases']) == 33
def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
for c in d['cases']:
    r = c['request']
    if hashlib.sha256(canonical(r)).hexdigest() != c['input_sha256']:
        raise SystemExit('행 입력 해시가 일치하지 않아요: ' + c['id'])
    j = r['kb_judgments'][0]
    kb = 'kb:' + j['card_id'] + '@0.6.1'
    assert kb in r['allowed_evidence_refs']
    if c['mode'] == 'hold':
        c['answer'] = ('### 개별 권고 보류 안내\n' + j['guidance'] + ' [' + kb + ']\n\n'
                       '### 필요한 다음 단계\n현재 상태와 확인되지 않은 사항을 전문가에게 설명하고 확인해 주세요. 원인이나 개인별 대응을 여기서 확정하지 않아요.')
    else:
        ref = next(x for x in r['allowed_evidence_refs'] if x.startswith('ref:'))
        source = next(x for x in r['rag_chunks'] if x['evidence_ref'] == ref)
        limits = {
            'ref:S05':'노출과 실제 행동에서 확인되지 않은 부분은 미상으로 남아요. 개인의 실제 자외선량이나 보호율은 계산할 수 없어요.',
            'ref:S16':'확인하지 못한 제품 표시나 개인의 실제 보호 결과는 확정할 수 없어요.',
            'ref:S17':'이 자료만으로 개인의 눈 주변 반응이나 원인을 확정할 수 없어요.',
            'ref:S18':'겉모습이나 보관 정보만으로 남은 보호 성능을 계산할 수 없어요.',
            'ref:S08':'제한된 연구 결과를 모든 제품과 세정 방법에 일반화할 수 없어요.',
            'ref:S09':'제한된 조합의 영상 결과로 개인의 실제 보호 성능을 보증할 수 없어요.',
        }
        summaries = {
            'ref:S05':'일반 자외선차단 안내는 실제 노출과 물·땀·닦임, 제품 지침을 함께 살펴요.',
            'ref:S16':'자외선차단제 선택 안내는 SPF, 광범위 보호와 내수성을 각각 살펴요.',
            'ref:S17':'눈 주변 사용 안내는 제품 선택과 사용 상황을 함께 살펴요.',
            'ref:S18':'사용기한과 보관 상태는 각각 확인할 정보예요.',
            'ref:S08':'연구는 제한된 제품과 세정 방법의 조합을 비교했어요.',
            'ref:S09':'중첩 연구는 제한된 제품 조합을 영상으로 관찰했어요.',
        }
        assert source and ref in summaries
        c['answer'] = ('### 핵심 안내\n' + j['guidance'] + ' [' + kb + ']\n\n'
                       '### 근거 및 이유\n' + summaries[ref] + ' [' + ref + ']\n\n'
                       '### 확인이 필요한 한계\n' + limits[ref])
assert hashlib.sha256(src.read_bytes()).hexdigest() == expected
with dest.open('x',encoding='utf-8',newline='\n') as f:
    json.dump(d,f,ensure_ascii=False,indent=2)
    f.write('\n')
