"""Append eight unreviewed hold inputs exactly once."""
import copy, hashlib, json
from pathlib import Path
H=Path(__file__).resolve().parent; P=H/'additional_100_terra_part_a_inputs.json'
D=json.loads(P.read_text(encoding='utf-8'))
if len(D['cases']) != 26: raise RuntimeError('Unexpected input revision')
K=json.loads((H.parents[6]/'KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json').read_text(encoding='utf-8'))
cards={c['id']:c for c in K['baseline_cards']}
old={c['id']:c for f in H.glob('additional_100_part_*_inputs.json') for c in json.loads(f.read_text(encoding='utf-8'))['cases']}
def case(n,base,title,values,guidance,split='train'):
 c=copy.deepcopy(old[base]); ident=f'syn-hold-{n:04d}'; card=c['card_ids'][0]
 c.update(id=ident,title=title,scenario_id='terra-a-scenario-'+ident,group_id='terra-a-group-'+ident,scenario_family_id=f'terra-a-hold-family-{n:04d}',split=split)
 req=c['request']; req['confirmed_observations']={k:{'variable_id':k,'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','confirmed_by_user':v is not None} for k,v in values.items()}
 req['kb_judgments'][0]['guidance']=guidance
 c['judgment_basis'].update(comparison_spec=cards[card]['comparison_spec'],rationale=guidance)
 c['input_sha256']=hashlib.sha256(json.dumps(req,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
 return c
D['cases'].extend([
 case(36,'syn-hold-0013','정상 외관 기록 이후 새로 생긴 악취',{'storage.sensory_change':{'new_odor':True,'previously_no_odor':True},'product.instructions':{'odor_change_normal':False}},'기존 기록과 달라진 새 냄새는 품질 확인 전 사용과 개별 권고를 보류해요.'),
 case(37,'syn-hold-0016','세안제를 중단했는데도 통증이 계속됨',{'skin.current_discomfort':'persistent','skin.pain':'moderate','method.current_routine':{'cleanser_stopped':True}},'제품을 중단한 뒤에도 지속되는 통증은 루틴 조정보다 전문가 확인을 우선해요.'),
 case(38,'syn-hold-0019','손 보호 장갑 교체 후에도 심한 통증 지속',{'skin.current_discomfort':'persistent','skin.pain':'severe','hand.protection_hygiene':{'gloves_changed':True}},'보호 장갑 변경 여부와 별도로 심한 통증에 대한 개별 권고를 보류해요.'),
 case(39,'syn-hold-0013','사용기한 전인데 용기에서 새로운 누출',{'storage.sensory_change':{'new_leakage':True,'container_damage':True},'product.instructions':{'expiry_not_passed':True}},'기한이 남은 사실만으로 새 누출과 용기 손상에 대한 품질을 확인할 수 없어 보류해요.'),
 case(40,'syn-hold-0017','피부를 관통하는 장치의 세척 뒤 재사용 절차 요청',{'device.use':{'skin_penetrating':True,'cleaning_done':True,'requests_reuse_protocol':True}},'세척 여부와 관계없이 피부 관통 기기의 개인 시술 절차 안내를 보류해요.'),
 case(41,'syn-hold-0018','사용설명서가 금지한 제품과 미용기기 병용',{'device.use':{'plans_combination':True},'product.instructions':{'device_combination_prohibited':True}},'확인된 금지 지시와 충돌하는 기기 병용 설계를 보류해요.'),
 case(42,'syn-hold-0016','보습제를 줄인 뒤에도 지속되는 새 통증',{'skin.current_discomfort':'persistent','skin.pain':'moderate','method.current_routine':{'moisturizer_reduced':True}},'사용량을 줄인 사실로 통증의 원인을 확정하지 않고 개별 권고를 보류해요.','val_internal'),
 case(43,'syn-hold-0013','품질 이상 의심 뒤 원래 용기에 옮겨 담으려는 계획',{'storage.sensory_change':{'new_particles':True,'color_or_odor_change':True},'storage.decanting':{'planned':True,'already_done':False}},'새 입자와 색 또는 냄새 변화가 있어 용기 이동 계획보다 품질 확인을 우선해요.'),
])
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('34 candidate inputs; no answers')
