#!/usr/bin/env python3
"""Poppy KB v0.6: static checks and small reference-function tests.

Not a medical/clinical validation, legal compliance engine, INCI parser,
authenticity detector, or production recommendation engine. Standard library only.
Run: python validate_poppy_kb_v0_6.py [path/to/Poppy_KB_seed_v0.6.json]
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

Tri = bool | None

def predicate(expr: dict[str, Any], facts: dict[str, Any]) -> Tri:
    """Three-valued predicate over explicitly supplied historical label inputs."""
    if 'all' in expr or 'any' in expr:
        op = 'all' if 'all' in expr else 'any'
        values = [predicate(x, facts) for x in expr[op]]
        if op == 'all':
            if False in values: return False
            return None if None in values else True
        if True in values: return True
        return None if None in values else False
    actual = facts.get(expr['field'])
    if actual is None: return None
    target, op = expr['value'], expr['op']
    if op == 'eq':
        if isinstance(target, bool) and not isinstance(actual, bool): return None
        return actual == target
    if isinstance(actual, bool): return None
    try:
        a, b = Decimal(str(actual)), Decimal(str(target))
        if not (a.is_finite() and b.is_finite()): return None
        if op == 'gt': return a > b
        if op == 'gte': return a >= b
        if op == 'lt': return a < b
        if op == 'lte': return a <= b
    except (InvalidOperation, ValueError, TypeError):
        return None
    raise ValueError(f'Unsupported predicate operation: {op}')

def regulatory_preview(rule: dict[str, Any], facts: dict[str, Any], *, mode: str='current') -> str:
    """No current-law output is enabled by this release."""
    if mode != 'historical_snapshot': return 'current_version_review_required'
    v = predicate(rule['condition'], facts)
    return 'unknown' if v is None else ('snapshot_matches' if v else 'snapshot_not_matches')

def combination_reference(policy: dict[str, Any], facts: dict[str, Any]) -> str:
    """Branch illustration over pre-reviewed roles; does not analyze ingredients."""
    if facts.get('current_severe_or_worsening_reaction') is True:
        return 'reaction_review_first'
    if facts.get('medical_plan') is True:
        return 'individual_plan_review_no_automatic_medication_change'
    if facts.get('same_site') is False:
        return 'not_same_site_stacking'
    if facts.get('same_site') is not True:
        return 'site_unknown'
    if facts.get('single_finished_product') is True:
        return 'finished_product_specific_review'
    if facts.get('single_finished_product') is not False:
        return 'product_relationship_unknown'
    if facts.get('role_mapping_reviewed') is not True:
        return 'role_unknown'
    left, right = facts.get('left_role'), facts.get('right_role')
    if not left or not right: return 'role_unknown'
    matched = any({left, right} == {p['left'],p['right']} for p in policy['pairs'])
    if not matched: return 'no_listed_pair_not_safety_certificate'
    timing = facts.get('timing')
    if timing == 'same_routine': return 'default_avoid_separate_product_stacking'
    if timing == 'same_day_separated': return 'default_avoid_no_time_gap_safety_guarantee'
    if timing == 'different_days': return 'review_pattern_not_automatically_safe'
    return 'timing_unknown_general_avoidance_guidance'

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kb', nargs='?', type=Path,
                    default=Path(__file__).with_name('Poppy_KB_seed_v0.6.json'))
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    try:
        d=json.loads(args.kb.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        print(f'Cannot read KB: {e}',file=sys.stderr);return 2
    checks=[]
    def check(name: str, condition: bool, detail: Any=None) -> None:
        checks.append({'name':name,'passed':bool(condition),'detail':detail})
    def unique(seq:list[dict],key:str='id')->bool:
        return len(seq)==len({x[key] for x in seq})
    cards={c['id']:c for c in d['baseline_cards']}
    variables={v['id']:v for v in d['variables']}
    sources={s['id']:s for s in d['source_registry']}
    nodes={n['id']:n for n in d['rule_taxonomy']['nodes']}
    regs={r['id']:r for r in d['regulatory_rules']}
    relations={r['id']:r for r in d['relations']}
    stages={s['id'] for s in d['lifecycle_taxonomy']['stages']}
    groups={g['id'] for g in d['variable_groups']}
    for k in ['baseline_cards','variables','source_registry','regulatory_rules','relations','variable_groups']:
        check(f'unique:{k}',unique(d[k]))
    check('unique:taxonomy',len(nodes)==len(d['rule_taxonomy']['nodes']))
    check('release_counts',len(cards)==60 and len(variables)==234 and len(regs)==25)
    check('axes_still_C_M_P',[a['id'] for a in d['axes']]==['C','M','P'])
    check('domain_and_stage_counts',len(d['rule_taxonomy']['domain_order'])==9 and len(stages)==7)
    check('variable_group_references',all(v['group_id'] in groups for v in variables.values()))
    check('all_card_inputs_resolve',all(v in variables for c in cards.values() for v in c['observable_inputs']))
    check('all_card_sources_resolve',all(s in sources for c in cards.values() for s in c['evidence']['source_ids']))
    check('all_card_links_resolve',all(r in cards for c in cards.values() for r in c.get('related_card_ids',[])))
    check('taxonomy_parents',all(n.get('parent_id') is None or n['parent_id'] in nodes for n in nodes.values()))
    ownership=Counter(r for n in nodes.values() for r in n.get('rule_ids',[]))
    check('each_rule_one_primary_owner',set(ownership)==set(cards) and all(v==1 for v in ownership.values()))
    check('primary_classification_matches',all(c['id'] in nodes[c['classification']['primary_category_id']]['rule_ids'] and nodes[c['classification']['primary_category_id']]['parent_id']==c['classification']['primary_domain_id'] for c in cards.values()))
    check('cross_references_bidirectional',all(sorted(c['classification']['referenced_from_category_ids'])==sorted(n['id'] for n in nodes.values() if c['id'] in n.get('referenced_rule_ids',[])) for c in cards.values()))
    check('taxonomy_rule_refs',all(r in cards for n in nodes.values() for r in n.get('rule_ids',[])+n.get('referenced_rule_ids',[])))
    check('taxonomy_variable_refs',all(v in variables for n in nodes.values() for v in n.get('context_variable_ids',[])+n.get('rule_input_variable_ids',[])))
    check('taxonomy_relation_refs',all(r in relations for n in nodes.values() for r in n.get('background_relation_ids',[])))
    check('card_lifecycle_tags',all(c.get('lifecycle_stage_ids') and set(c['lifecycle_stage_ids'])<=stages for c in cards.values()))
    check('lifecycle_views_inverse',all(set(v['card_ids'])=={c['id'] for c in cards.values() if v['stage_id'] in c['lifecycle_stage_ids']} for v in d['lifecycle_views']))
    check('category_views_refs',all(r in cards for v in d['category_views'] for r in v['total_unique_visible_rule_ids']))
    check('acquisition_refs',all(a['variable_id'] in variables and all(c in cards for c in a['baseline_card_refs']) for a in d['acquisition_items']))
    check('input_question_not_all',all(a['ask_all_users'] is False for a in d['acquisition_items']))
    check('no_measurements_or_latent_inputs',all(not v.startswith(('measure.','bio.')) for c in cards.values() for v in c['observable_inputs']))
    check('no_required_unobservable_variables',all(v.get('runtime_required') is not True for v in variables.values() if v['id'].startswith(('measure.','bio.'))))
    check('no_unjustified_probability',all(c['recommendation'].get('estimated_improvement_probability') is None for c in cards.values()))
    check('all_card_execution_disabled',all(c['active'] is False and c['review']['production_enabled'] is False for c in cards.values()))
    check('metadata_production_disabled',d['metadata']['production_enabled'] is False)
    check('regulatory_execution_disabled',all(r['production_enabled'] is False and r['current_legal_application_allowed'] is False and r['current_version_reconciled'] is False for r in regs.values()))
    check('current_regulatory_gate',d['regulatory_version_contract']['current_regulatory_compliance_enabled'] is False)
    check('regulatory_source_and_links',all(r['source_id'] in sources and all(c in cards for c in r['linked_baseline_ids']) for r in regs.values()))
    check('regulatory_page_refs',all(1<=p<=19 for r in regs.values() for p in r['source_locator']['pages']))
    check('source_pages_complete',[p['page'] for p in d['regulatory_source_pages']]==list(range(1,20)))
    check('allergen_snapshot25',len(d['allergen_label_dictionary']['rows'])==25 and not d['allergen_label_dictionary']['is_current_permitted_ingredient_list'])
    check('allergen_cas_unique',unique(d['allergen_label_dictionary']['rows'],'cas'))
    check('allergen_cas_checksums',all(sum((i+1)*int(x) for i,x in enumerate(r['cas'].replace('-','')[:-1][::-1]))%10==int(r['cas'][-1]) for r in d['allergen_label_dictionary']['rows']))
    check('original_40_core_preserved',all(hashlib.sha256(json.dumps({k:v for k,v in cards[cid].items() if k not in d['v0_5_preservation_manifest']['excluded_comparison_fields']},ensure_ascii=False,sort_keys=True).encode()).hexdigest()==digest for cid,digest in d['v0_5_preservation_manifest']['core_sha256_by_id'].items()))
    check('exactly_20_new_cards',len(d['v0_5_preservation_manifest']['new_ids'])==20 and set(cards)==set(d['v0_5_preservation_manifest']['retained_ids'])|set(d['v0_5_preservation_manifest']['new_ids']))
    check('severe_source_wording_not_autoquoted',d['regulatory_integration_contract']['archive_exception']['auto_quotation_in_advice'] is False)
    check('documented_scenarios_are_spec_only',all(s.get('execution_status')=='specification_only_not_engine_executed' for s in d['acceptance_scenarios']))
    check('scenario_card_refs',all(c in cards for s in d['acceptance_scenarios'] for c in s.get('card_ids',[])))
    export=args.kb.with_name('Poppy_KB_규정근거_v0.6.json')
    if export.exists():
        e=json.loads(export.read_text())
        check('regulatory_export_matches',e['rules']==d['regulatory_rules'] and e['allergens']==d['allergen_label_dictionary'] and e['source_pages']==d['regulatory_source_pages'] and e['condition_field_registry']==d['regulatory_condition_field_registry'])
    # Borderline values intentionally distinguish > from >= and keep local exceptions.
    boundary_cases=[
      ('aha_half_excluded','RG24-AHA-02',{'aha_percent':.5},False),
      ('aha_above_half','RG24-AHA-02',{'aha_percent':.5001},True),
      ('aha_unknown','RG24-AHA-02',{},None),
      ('aha_unknown_string','RG24-AHA-02',{'aha_percent':'미확인'},None),
      ('aha_bool_invalid','RG24-AHA-02',{'aha_percent':True},None),
      ('aha_nan_invalid','RG24-AHA-02',{'aha_percent':'NaN'},None),
      ('aha_sun_leave','RG24-AHA-01',{'aha_percent':1,'rinse_off':False,'hair_product':False},True),
      ('aha_rinse_sun_exempt','RG24-AHA-01',{'aha_percent':8,'rinse_off':True,'hair_product':False},False),
      ('aha_rinse_trial_not_exempt','RG24-AHA-02',{'aha_percent':8,'rinse_off':True},True),
      ('aha_hair_sun_exempt','RG24-AHA-01',{'aha_percent':8,'rinse_off':False,'hair_product':True},False),
      ('aha_sun_type_unknown','RG24-AHA-01',{'aha_percent':8},None),
      ('aha_consult_exact_boundaries','RG24-AHA-03',{'aha_percent':10,'ph':3.5},False),
      ('aha_consult_high','RG24-AHA-03',{'aha_percent':10.001},True),
      ('aha_consult_low_ph','RG24-AHA-03',{'aha_percent':1,'ph':3.499},True),
      ('aha_below_parent_excluded','RG24-AHA-03',{'aha_percent':.5,'ph':3},False),
      ('aha_parent_unknown','RG24-AHA-03',{'ph':3},None),
      ('aha_low_unknown_ph','RG24-AHA-03',{'aha_percent':2},None),
      ('aha_hair_consult_not_exempt','RG24-AHA-03',{'aha_percent':12,'hair_product':True},True),
      ('allergen_leave_boundary','RG24-ALLERGEN-01',{'is_listed_fragrance_component':True,'rinse_off':False,'allergen_percent':.001},False),
      ('allergen_leave_above','RG24-ALLERGEN-01',{'is_listed_fragrance_component':True,'rinse_off':False,'allergen_percent':.0011},True),
      ('allergen_rinse_boundary','RG24-ALLERGEN-01',{'is_listed_fragrance_component':True,'rinse_off':True,'allergen_percent':.01},False),
      ('allergen_rinse_above','RG24-ALLERGEN-01',{'is_listed_fragrance_component':True,'rinse_off':True,'allergen_percent':.0101},True),
      ('allergen_unknown_amount','RG24-ALLERGEN-01',{'is_listed_fragrance_component':True,'rinse_off':False},None),
      ('not_fragrance_condition','RG24-ALLERGEN-01',{'is_listed_fragrance_component':False},False),
      ('specific_retinamide_boundary','RG24-RETINAMIDE-01',{'polyethoxylated_retinamide_percent':.2},True),
      ('not_all_retinoids','RG24-RETINAMIDE-01',{'retinol_percent':.5},None),
      ('arbutin_boundary','RG24-ARBUTIN-01',{'arbutin_percent':2},True),
      ('salicylic_immediate_rinse_exception','RG24-SA-01',{'contains_salicylic_or_salt':True,'immediate_rinse_off':True},False),
      ('salicylic_unknown_rinse','RG24-SA-01',{'contains_salicylic_or_salt':True},None),
    ]
    for name,rid,facts,expected in boundary_cases:
        actual=predicate(regs[rid]['condition'],facts)
        check('snapshot_boundary:'+name,actual is expected,{'actual':actual,'expected':expected})
    check('default_mode_blocks_current_application',regulatory_preview(regs['RG24-AHA-02'],{'aha_percent':8})=='current_version_review_required')
    check('explicit_snapshot_mode_required',regulatory_preview(regs['RG24-AHA-02'],{'aha_percent':8},mode='historical_snapshot')=='snapshot_matches')
    base={'left_role':'retinoid','right_role':'aha_exfoliating','same_site':True,'single_finished_product':False,'role_mapping_reviewed':True,'timing':'same_routine'}
    pairs=[
      ('retinoid_aha',{},'default_avoid_separate_product_stacking'),
      ('retinoid_sa',{'right_role':'salicylic_exfoliating'},'default_avoid_separate_product_stacking'),
      ('aha_sa',{'left_role':'aha_exfoliating','right_role':'salicylic_exfoliating'},'default_avoid_separate_product_stacking'),
      ('reverse_pair',{'left_role':'aha_exfoliating','right_role':'retinoid'},'default_avoid_separate_product_stacking'),
      ('different_sites',{'same_site':False},'not_same_site_stacking'),
      ('unknown_site',{'same_site':None},'site_unknown'),
      ('fixed_combination',{'single_finished_product':True},'finished_product_specific_review'),
      ('unknown_product_relation',{'single_finished_product':None},'product_relationship_unknown'),
      ('citric_only_no_role_mapping',{'role_mapping_reviewed':False},'role_unknown'),
      ('unknown_role',{'right_role':None},'role_unknown'),
      ('not_every_salicylate',{'right_role':'salicylate_uv_filter'},'no_listed_pair_not_safety_certificate'),
      ('not_bha_preservative',{'right_role':'butylated_hydroxyanisole'},'no_listed_pair_not_safety_certificate'),
      ('morning_evening',{'timing':'same_day_separated'},'default_avoid_no_time_gap_safety_guarantee'),
      ('different_days',{'timing':'different_days'},'review_pattern_not_automatically_safe'),
      ('unknown_time',{'timing':None},'timing_unknown_general_avoidance_guidance'),
      ('medical_plan',{'medical_plan':True},'individual_plan_review_no_automatic_medication_change'),
      ('adverse_reaction',{'medical_plan':True,'current_severe_or_worsening_reaction':True},'reaction_review_first'),
    ]
    for name,change,expected in pairs:
        actual=combination_reference(d['combination_policy'],base|change)
        check('reference_branch:'+name,actual==expected,{'actual':actual,'expected':expected})
    docs=args.kb.with_name('Poppy_KB_지식구조_v0.6.md')
    if docs.exists():
        text=docs.read_text()
        check('main_document_each_card_once',all(text.count(f'#### {c} · ')==1 for c in cards))
        check('main_document_all_desirable_states',all(c['desirable_state'] in text for c in cards.values()))
    failed=[c for c in checks if not c['passed']]
    report={'kb_file':args.kb.name,'kb_sha256':hashlib.sha256(args.kb.read_bytes()).hexdigest(),
      'generated_at_utc':datetime.now(timezone.utc).isoformat(),
      'basis_date':d['metadata']['revised_on'],'checks_total':len(checks),'passed':len(checks)-len(failed),'failed':len(failed),
      'counts':d['metadata']['current_counts'],'snapshot_condition_cases':len(boundary_cases),
      'combination_reference_cases':len(pairs),
      'limitations':['실제 앱·LLM 추천엔진·제품성분 파서의 실행 테스트가 아님.','명시적으로 부여한 역할/부위/조건을 처리하는 참고함수 테스트.','2024 원문 조건식의 참조 구현 검증이며 2026 현행법 판정 검증이 아님.','임상 효능·위험확률·정품·회수 대상 확인·새 가설 검증을 수행하지 않음.','57개 acceptance_scenarios는 별도 설계 명세이며 엔진에서 통과한 것으로 집계하지 않음.'],
      'checks':checks}
    out=args.report or args.kb.with_name('Poppy_KB_검증보고서_v0.6.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['checks_total','passed','failed','snapshot_condition_cases','combination_reference_cases']},ensure_ascii=False))
    if failed: print(json.dumps(failed,ensure_ascii=False,indent=2),file=sys.stderr)
    return 1 if failed else 0

if __name__=='__main__':
    raise SystemExit(main())
