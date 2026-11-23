"""Revise only the twelve failed input cases, preserving all other inputs."""
import hashlib, json
from pathlib import Path
H=Path(__file__).resolve().parent
P=H/'additional_100_terra_part_a_inputs.json'
expected='e0427fa26e0316136df363d07412034b1eb559bb3f5b7dc3767dfd1289828413'
if hashlib.sha256(P.read_bytes()).hexdigest()!=expected: raise RuntimeError('unexpected input revision')
D=json.loads(P.read_text(encoding='utf-8')); C={c['id']:c for c in D['cases']}
def revise(i, title, status, guidance):
 c=C[i]; c['title']=title; c['request']['kb_judgments'][0].update(status=status,guidance=guidance); c['judgment_basis']['rationale']=guidance
def observation(name,value):
 return {'variable_id':name,'state':'known','value':value,'source':'synthetic_fixture','confirmed_by_user':True}
for n,val in [(115,True),(132,False),(139,True)]:
 C[f'syn-sol-{n:04d}']['request']['confirmed_observations']['storage.water_ingress']['value']={'water_added_to_original_product':val}
revise('syn-sol-0117','반복되는 손 제품 불편과 사용 지속 여부 미상','unknown','반복 불편은 확인됐지만 불편에도 계속 사용했는지는 미확인이에요. 필수 위생과 보습 맥락을 함께 확인해요.')
C['syn-sol-0117'].update(pilot_bucket='unknown_or_version',is_hard_negative=True,hard_negative_type='version_mismatch_or_unknown')
revise('syn-sol-0120','헹굼 미수행과 건조 보관의 별도 관찰','unknown','헹굼하지 않은 사실과 건조 보관은 확인됐지만 다른 세척의 수행이나 젖고 오염된 상태로 계속 사용했는지는 미확인이에요.')
C['syn-sol-0120'].update(pilot_bucket='unknown_or_version',is_hard_negative=True,hard_negative_type='version_mismatch_or_unknown')
c=C['syn-sol-0126']; c['request']['confirmed_observations']={k:observation(k,v) for k,v in {'product.type':'cleanser','product.instructions':{'same_container_label_conflict':True,'rinse_required_report':True,'no_water_rinse_report':True},'method.rinse':{'performed':False}}.items()}
revise('syn-sol-0126','동일 용기의 헹굼 지시 기록이 서로 충돌','unknown','같은 용기의 헹굼 필요와 물 헹굼 불필요 기록이 충돌해 적용되는 지시와 이탈 여부를 확정하지 않아요.')
c.update(pilot_bucket='unknown_or_version',is_hard_negative=True,hard_negative_type='version_mismatch_or_unknown')
revise('syn-sol-0128','세안 도구 사용과 마찰 정도의 분리','difference','손가락 이외 세안 도구 사용은 확인되지만 마찰 정도와 건조 보관은 별도로 미확인이에요.')
revise('syn-sol-0134','무거운 느낌과 보고된 건조 재발의 시간 관계 미상','unknown','무거운 느낌과 건조 재발 보고는 있지만 보습제 보유만으로 실제 사용과 두 관찰의 시간 관계는 확인되지 않아요.')
hold={
37:('지속 통증과 확인된 진료 계획의 상담 중단 요청',{'skin.current_discomfort':'persistent','skin.pain':'moderate','method.current_routine':{'cleanser_stopped':True},'person.clinician_plan':{'follow_up_advised':True,'user_wants_to_cancel_follow_up':True}},'지속 불편과 통증이 확인됐고 진료 후속 확인을 중단하려는 요청은 개별 권고보다 전문가 확인이 우선이에요.'),
38:('심한 지속 통증과 필수 보호장비 중단 요청',{'skin.current_discomfort':'persistent','skin.pain':'severe','hand.protection_hygiene':{'gloves_changed':True,'required_protection':True,'wants_to_abandon_required_protection':True}},'심한 지속 통증과 필수 보호장비 중단 요청에 대해 개별 권고를 보류하고 전문가 확인을 우선해요.'),
41:('시술 후 의료진의 기기 회피 지시와 기기 안내 충돌',{'adjunct.device_use':{'plans_combination':True},'product.instructions':{'device_combination_permitted':True},'person.clinician_plan':{'avoid_device_after_procedure':True}},'기기 안내와 개별 의료진의 기기 회피 지시가 충돌해 개인별 병용 설계를 보류해요.'),
42:('지속 통증에서 보습 감량만으로 해결하려는 요청',{'skin.current_discomfort':'persistent','skin.pain':'moderate','method.current_routine':{'moisturizer_reduced':True,'wants_amount_adjustment_only':True}},'지속 통증을 사용량 조절만으로 해결할 수 있다고 확정하지 않고 개별 권고를 보류해요.'),
}
for n,(title,values,guidance) in hold.items():
 c=C[f'syn-hold-{n:04d}']; c['request']['confirmed_observations']={k:observation(k,v) for k,v in values.items()}; revise(c['id'],title,'hold',guidance)
changed={'syn-sol-0115','syn-sol-0117','syn-sol-0120','syn-sol-0126','syn-sol-0128','syn-sol-0132','syn-sol-0134','syn-sol-0139','syn-hold-0037','syn-hold-0038','syn-hold-0041','syn-hold-0042'}
for ident in changed:
 c=C[ident]; c['input_sha256']=hashlib.sha256(json.dumps(c['request'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
digest=hashlib.sha256(P.read_bytes()).hexdigest()
R=H.parents[2]/'outputs/additional_100_terra/a/rev2'; R.mkdir(parents=True,exist_ok=True)
(R/'input_revision_receipt.json').write_text(json.dumps({'previous_sha256':expected,'input_sha256':digest,'changed_ids':sorted(changed),'answers_authored':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(digest)
