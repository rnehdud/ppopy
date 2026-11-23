"""독립 감사에서 실패한 세 사례의 입력을 먼저 고정해요."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]
ROOT = COS.parents[3]
OUT = COS / 'outputs/additional_100/revision_c'
TARGETS = {'syn-sol-0093', 'syn-sol-0110', 'syn-hold-0032'}

def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def obs(k, v):
    return {'variable_id':k, 'state':'known', 'value':v, 'source':'synthetic_fixture', 'confirmed_by_user':True}

def freeze_inputs():
    OUT.mkdir(parents=True, exist_ok=True)
    files = [HERE/'additional_100_part_c_inputs.json', HERE/'additional_100_part_c.json', HERE/'reviews/additional_100_part_c_codex_independent.jsonl']
    hashes = {}
    for p in files:
        raw = p.read_bytes()
        target = OUT/(p.name+'.initial')
        if target.exists():
            assert target.read_bytes() == raw, '최초 보존본을 덮어쓰지 않아요.'
        else:
            target.write_bytes(raw)
        hashes[p.name] = sha(raw)
    save(OUT/'initial_sha256.json', hashes)
    data = json.loads(files[0].read_text(encoding='utf-8'))
    kb = json.loads((ROOT/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
    cards = {x['id']:x for x in kb['baseline_cards']}
    sources = {x['id']:x for x in kb['source_registry']}
    def chunk(sid, text):
        s=sources[sid]
        return {'evidence_ref':'ref:'+sid,'text':text,'scope':'general_skincare_practice','source_url':s['url'],'locator':s['locator'],'checked_on':s['checked_on'],'limitations':s['limitations']}
    def update(c, title, card_ids, values, judgments, products, chunks, allowed, distractors):
        c['title']=title
        c['card_ids']=card_ids
        c['chunk_origins']={x['evidence_ref']:'kb_source_summary' for x in chunks}
        c['request']={'mode':c['mode'],'confirmed_observations':{k:obs(k,v) for k,v in values.items()},'kb_judgments':judgments,'product_evidence':products,'rag_chunks':chunks,'allowed_evidence_refs':allowed,'distractor_refs':distractors}
        c['input_sha256']=sha(canonical(c['request']).encode())
        c['judgment_basis']={'kind':'authored_synthetic_case_against_KB_comparison_spec_not_engine_execution','card_id':card_ids[0],'comparison_spec':copy.deepcopy(cards[card_ids[0]]['comparison_spec']),'rationale':judgments[0]['guidance']}
    byid={c['id']:c for c in data['cases']}
    update(byid['syn-sol-0093'],'건식 전용 전기면도기에 실제 물과 크림을 쓴 경우',['B-G09'],
        {'shaving.method':{'실제 방식':'전기면도기','사용 부위':'얼굴'},'shaving.preparation':{'실제 사용':'얼굴과 헤드를 물에 적시고 면도 크림을 함께 사용했어요.'},'product.instructions':{'제품':'합성 건식 전기면도기','확인된 표시':'건식 전용이며 물과 면도 크림을 함께 사용하지 않도록 표시돼요.'},'skin.current_discomfort':'현재 불편 없음'},
        [{'card_id':'B-G09','status':'difference','guidance':'건식 전용 표시가 확인된 전기면도기에 실제로 물과 크림을 사용했으므로 기기별 지시와 현재 준비 방식에 차이가 있어요. 습식 날면도 준비를 그대로 확대하지 않아요.'}],
        [{'product_id':'syn-dry-shaver-c93','version':'1.0','synthetic_product':True,'status':'verified','label_guidance':'합성 기기 표시 예시: 건식 전용. 물과 면도 크림을 함께 사용하지 않아요.','evidence_ref':'catalog:syn-dry-shaver-c93@1.0'}],[],
        ['kb:B-G09@0.6.1','catalog:syn-dry-shaver-c93@1.0'],[])
    update(byid['syn-sol-0110'],'토너크림이라는 이름과 확인된 보습제 용도 구분',['B-G08'],
        {'product.identity':{'상품명':'합성 토너크림','제품 ID':'syn-tonercream-c110','버전':'1.0'},'product.type':'얼굴 보습제','product.form_descriptor':{'확인된 성상':'반고형 크림'},'product.instructions':{'확인된 표시':'보습 단계에서 세럼 다음에 사용해요.'},'method.current_routine':{'실제 순서':['세안','합성 토너크림','세럼'],'이유':'상품명에 토너가 있어 묽은 토너 단계로 판단했어요.'},'skin.current_discomfort':'현재 불편 없음'},
        [{'card_id':'B-G08','status':'difference','guidance':'상품명에 토너가 있다는 이유로 첫 단계에 쓰지만 확인된 용도는 반고형 얼굴 보습제이고 표시는 세럼 다음 사용이에요. 이름이 아니라 해당 제품의 확인된 용도와 순서를 구분해요.'}],
        [{'product_id':'syn-tonercream-c110','version':'1.0','synthetic_product':True,'status':'verified','label_guidance':'합성 제품 표시 예시: 상품명은 토너크림. 반고형 얼굴 보습제이며 세럼 다음의 보습 단계에서 사용해요.','evidence_ref':'catalog:syn-tonercream-c110@1.0'}],
        [chunk('S21','손을 씻은 뒤 무향료 핸드크림이나 연고형 보습제를 사용하는 일반 안내예요. 필요한 손 위생을 줄이라는 뜻은 아니에요.')],
        ['kb:B-G08@0.6.1','catalog:syn-tonercream-c110@1.0'],['ref:S21'])
    update(byid['syn-hold-0032'],'손 전용 제품의 실제 눈 노출과 심한 통증',['B-G16','B-B01'],
        {'product.instructions':{'확인된 표시':'손에만 사용하는 합성 제품이에요.'},'product.label_warnings':{'확인된 주의사항':'눈과 눈 주변에는 사용하지 않아요.'},'method.body_site':'손에 사용하던 제품이 실제로 눈에 들어갔어요.','skin.pain':'심한 통증','skin.current_discomfort':'현재 눈 통증이 있어요.','constraints.decision_context':'눈에 들어간 제품을 보습 루틴이나 다른 제품으로 보완하는 방법을 요청해요.'},
        [{'card_id':'B-G16','status':'exception','guidance':'손 전용 제품의 실제 눈 노출과 현재 심한 통증이 확인되어 일반적인 표시 비교와 루틴 최적화 범위를 벗어나요. 개별 사용 지시를 보류하고 전문 확인 경로를 우선해요.'},{'card_id':'B-B01','status':'hold','guidance':'심한 현재 통증을 다른 보습 제품이나 루틴으로 해결하는 개별 권고는 보류해요. 원인 진단이나 응급 처치 절차를 생성하지 않아요.'}],
        [{'product_id':'syn-hand-only-c32','version':'1.0','synthetic_product':True,'status':'verified','label_guidance':'합성 제품 표시 예시: 손 전용이며 눈과 눈 주변에는 사용하지 않아요.','evidence_ref':'catalog:syn-hand-only-c32@1.0'}],[],
        ['kb:B-G16@0.6.1','kb:B-B01@0.6.1','catalog:syn-hand-only-c32@1.0'],[])
    data['input_revision']=4
    data['revision_note']='독립 감사에서 의미상 중복으로 실패한 세 입력만 새 결정 조건으로 교체했어요. 최초 입력·응답·감사와 해시는 별도로 보존했으며 응답은 아직 작성하지 않았어요.'
    original=json.loads(files[0].read_text(encoding='utf-8'))
    assert [c for c in data['cases'] if c['id'] not in TARGETS] == [c for c in original['cases'] if c['id'] not in TARGETS]
    save(files[0],data)
    raw=files[0].read_bytes()
    (OUT/'fixed_inputs_before_answers.json').write_bytes(raw)
    save(OUT/'input_freeze_receipt.json',{'고정 입력 SHA-256':sha(raw),'수정 사례':sorted(TARGETS),'응답 작성 전 물리적 고정':True,'다른 사례 입력 동일':30,'최초 파일 해시':hashes})
    print('세 입력을 응답 없이 고정했어요.',sha(raw))

def write_answers():
    frozen_raw=(OUT/'fixed_inputs_before_answers.json').read_bytes()
    receipt=json.loads((OUT/'input_freeze_receipt.json').read_text(encoding='utf-8'))
    assert sha(frozen_raw)==receipt['고정 입력 SHA-256']
    assert (HERE/'additional_100_part_c_inputs.json').read_bytes()==frozen_raw
    data=json.loads(frozen_raw)
    original=json.loads((OUT/'additional_100_part_c.json.initial').read_text(encoding='utf-8'))
    old_byid={c['id']:c for c in original['cases']}
    answers={
        'syn-sol-0093':'### 핵심 안내\n지금 쓰는 합성 전기면도기는 건식 전용으로 확인됐는데 실제로 물과 면도 크림을 함께 사용했어요. 습식 날면도 준비를 이 기기에 적용하지 말고 확인된 건식 전용 지시에 맞게 준비 방식을 바꿔요. [kb:B-G09@0.6.1] [catalog:syn-dry-shaver-c93@1.0]\n\n### 근거 및 이유\n면도 준비는 방식에 따라 달라요. 피부와 털을 적시는 습식 날면도 안내가 모든 전기면도기에 물과 크림을 쓰라는 뜻은 아니에요. [kb:B-G09@0.6.1]\n\n### 확인이 필요한 한계\n현재 불편이 없다는 관찰만으로 표시와 다른 사용이 적합하다고 보증할 수는 없어요. 이번 차이는 기기별 용법에 관한 것이며 피부 손상이나 질환이 생겼다고 판단한 것은 아니에요.',
        'syn-sol-0110':'### 핵심 안내\n합성 토너크림은 이름에 토너가 있지만, 확인된 용도는 반고형 얼굴 보습제이고 표시는 세럼 다음 사용이에요. 이름만 보고 세럼 앞의 묽은 토너 단계에 두었던 순서를 해당 제품 표시와 맞춰 검토해요. [kb:B-G08@0.6.1] [catalog:syn-tonercream-c110@1.0]\n\n### 근거 및 이유\n상품명과 실제 용도·성상·사용 순서는 구분해야 해요. 여기서는 확인된 제품별 표시를 따르는 것이며 모든 크림이나 토너에 같은 순서를 정하는 기준은 아니에요. [kb:B-G08@0.6.1]\n\n### 확인이 필요한 한계\n현재 불편이 없다는 관찰은 그대로 남겨요. 순서의 차이만으로 피부 손상이나 효과 저하를 확정하지 않으며, 보습제라는 용도나 반고형 성상으로 미공개 성분과 농도를 추정하지 않아요.',
        'syn-hold-0032':'### 개별 권고 보류 안내\n손 전용이며 눈과 눈 주변에 사용하지 않도록 표시된 합성 제품이 실제로 눈에 들어갔고, 현재 심한 통증이 있다고 확인했어요. 일반적인 표시 비교나 보습 루틴 조정으로 다룰 상황이 아니어서 개별 루틴·제품 권고를 보류해요. [catalog:syn-hand-only-c32@1.0] [kb:B-G16@0.6.1] [kb:B-B01@0.6.1]\n\n### 필요한 다음 단계\n현재 눈 노출과 심한 통증에 대해 의료 전문가의 확인을 우선 받아 주세요. 제품 이름과 버전, 표시 주의사항, 실제 접촉 부위와 증상 내용을 전달해 확인해요. 여기서는 원인이나 손상 정도를 진단하거나 응급 처치 절차를 만들어 안내하지 않아요.'
    }
    for c in data['cases']:
        if c['id'] in TARGETS:
            c['answer']=answers[c['id']]
        else:
            assert c=={k:v for k,v in old_byid[c['id']].items() if k!='answer'}
            c['answer']=old_byid[c['id']]['answer']
    data['generation_note']='물리적으로 고정한 개정 4 입력을 읽고 세 응답만 새로 작성했어요. 다른 30건의 입력과 응답, 최초 실패 감사는 보존했어요. 재검수와 사람 승인은 아직 완료되지 않았어요.'
    assert [c for c in data['cases'] if c['id'] not in TARGETS]==[c for c in original['cases'] if c['id'] not in TARGETS]
    save(HERE/'additional_100_part_c.json',data)
    save(OUT/'answer_revision_receipt.json',{'고정 입력 SHA-256':sha(frozen_raw),'수정 사례':sorted(TARGETS),'다른 사례 입력과 응답 동일':30,'새 응답 원본 SHA-256':sha((HERE/'additional_100_part_c.json').read_bytes()),'최초 감사 수정':False,'사람 검수 수행':False})
    print('고정 입력을 읽고 세 응답만 작성했어요.')

if __name__=='__main__':
    if '--answers' in sys.argv:
        write_answers()
    else:
        freeze_inputs()
