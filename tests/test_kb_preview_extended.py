"""Independent semantic boundaries plus complete executable branch discrimination."""
from copy import deepcopy
import json
import pytest
from skin_engine.kb_preview import PreviewEngine,load_kb
from skin_engine.kb_preview.audit import request,run
from skin_engine.kb_preview.filter_properties import classify_filters
E=PreviewEngine()

def evaluate(facts,card,site='face'):
    q=request(facts,[card]);q['body_site']=site
    return E.evaluate(q)['results'][0]

# Inputs here are independent of the rule configuration and include rejected branches.
@pytest.mark.parametrize('card,facts,status',[
 ('B-C03',{'dose.contact_time':{'range_seconds':[59,61],'phase':'before_rinsing'}},'unknown'),
 ('B-C03',{'dose.contact_time':{'range_seconds':[61,61],'phase':'before_rinsing'},'product.type':'ordinary_rinse_off_cleanser','product.instructions':'no_special_duration'},'unknown'),
 ('B-C03',{'dose.contact_time':{'range_seconds':[180,300],'phase':'before_rinsing'},'product.type':'ordinary_rinse_off_cleanser','product.instructions':'no_special_duration'},'difference'),
 ('B-C03',{'dose.contact_time':{'range_seconds':[180,300],'phase':'whole_shower'},'product.type':'ordinary_rinse_off_cleanser','product.instructions':'no_special_duration'},'unknown'),
 ('B-C03',{'dose.contact_time':{'range_seconds':[300,180]},'product.type':'ordinary_rinse_off_cleanser'},'unknown'),
 ('B-C02',{'method.tools':'hands','method.friction':'gentle'},'unknown'),
 ('B-C02',{'method.tools':'hands','method.friction':'gentle','method.drying':'pat_gently'},'aligned'),
 ('B-C02',{'method.tools':'hands','method.friction':'gentle','method.drying':'rubbing_strongly'},'difference'),
 ('B-C05',{'cleansing.repeat_wash':'habitual_without_reason','cleansing.target_load':'heavy_soiling'},'exception'),
 ('B-C06',{'product.type':'leave_on','method.rinse':'omitted'},'not_applicable'),
 ('B-M01',{'method.skin_wetness':'slightly_damp'},'unknown'),
 ('B-M03',{'skin.dryness':'persistent','method.current_routine':'moisturizing_function_used'},'exception'),
 ('B-P01',{'product.spf':30,'product.uva':'broad_spectrum_confirmed','sun.outdoor_time':'prolonged','sun.sweat':'no','sun.water_contact':'no'},'aligned'),
 ('B-P01',{'product.spf':29,'product.uva':'broad_spectrum_confirmed'},'difference'),
 ('B-P01',{'product.spf':50,'product.uva':'PA++++'},'unknown'),
 ('B-P01',{'product.spf':50,'product.uva':'broad_spectrum_confirmed','sun.sweat':'yes'},'unknown'),
 ('B-P05',{'product.uv_filter_preference_profile':'matches_reviewed_preference','skin.eye_stinging':'recurrent'},'exception'),
 ('B-P05',{'product.uv_filter_preference_profile':'unclassified'},'unknown'),
 ('B-P07',{'product.identity':'한국콜마 브랜드'},'unknown'),
 ('B-S06',{'shaving.method':'manual','shaving.blade_use_history':8,'shaving.care':'replacement_not_reviewed'},'difference'),
 ('B-S06',{'shaving.method':'electric','shaving.blade_use_history':100},'unknown'),
 ('B-S06',{'shaving.method':'manual','shaving.blade_use_history':1,'shaving.blade_condition':'damaged'},'difference'),
 ('B-G11',{'person.known_allergies':'confirmed_product_allergen','introduction.local_trial':'performed_per_label_no_reaction'},'exception'),
 ('B-G16',{'product.regulatory_type':'chemical_depilatory'},'unknown'),
 ('B-G17',{'person.known_allergies':'identity_uncertain'},'exception'),
 ('B-P09',{'product.application_form':'nongas_spray'},'unknown'),
 ('B-I04',{'product.active_care_roles':'ingredient_only_unclassified','method.current_routine':'aha_strengthened_protection_omitted'},'unknown'),
 ('B-L01',{'environment.indirect_products':'no_contact_path'},'not_applicable'),
 ('B-L03',{'environment.friction_gear':'certified_fit_requirement'},'exception'),
])
def test_semantic_boundaries(card,facts,status):
    assert evaluate(facts,card)['comparison_status']==status

@pytest.mark.parametrize('cid',list(E.cards))
def test_every_card_unknown_conflict_instruction_and_evidence(cid):
    q=request({},[cid]);out=E.evaluate(q);r=out['results'][0]
    assert r['comparison_status']=='unknown'
    assert r['sources'] and r['evidence']['source_ids']
    assert all(s['id'] in r['evidence']['source_ids'] for s in r['sources'])
    field=E.cards[cid]['observable_inputs'][0]
    q['facts'][field]={'state':'conflicting','value':None,'source':'user_report','reference':'two inconsistent observations'}
    assert E.evaluate(q)['results'][0]['comparison_status']=='conflicting'
    q['facts'].update(request({'context.individual_instruction':True})['facts'])
    assert E.evaluate(q)['results'][0]['comparison_status']=='exception'

BRANCHES=[(cid,b) for cid,bs in E.rules.items() for b in bs if b['when']]
@pytest.mark.parametrize('cid,branch',BRANCHES,ids=[b['branch_id'] for _,b in BRANCHES])
def test_branch_execution_and_missing_antecedents(cid,branch):
    facts={k:v[0] for k,v in branch['when'].items()};q=request(facts,[cid])
    if cid in ('B-M04','B-L02'):q['body_site']='hands'
    if cid in ('B-G13','B-G14','B-G15') and branch['status']=='difference':
        pair=next(p for p in E.kb['combination_policy']['pairs'] if p['card_id']==cid)
        q['facts'].update(request({'product.reviewed_role_pair':[pair['left'],pair['right']]})['facts'])
    result=E.evaluate(q)['results'][0]
    assert result['comparison_status']==branch['status']
    if result['matched_branch_id']!=branch['branch_id']:
        assert (cid,result['reason']) in {
            ('B-C03','product_contact_instruction'),
            ('B-H01','cycle_consent_not_given'),
            ('B-G11','known_allergen_or_severe_history'),
        }
    original=E.cards[cid]['scope'] if branch['kb_clause']=='scope' else E.cards[cid]['comparison_spec'][branch['kb_clause']]
    assert branch['kb_text']==original
    for key in branch['when']:
        missing=deepcopy(q);missing['facts'][key]['state']='unknown'
        after=E.evaluate(missing)['results'][0]
        assert after['matched_branch_id']!=branch['branch_id']


def test_quality_suppression_does_not_leave_maintain_text():
    q=request({'product.fragrance':'fragrance_free','storage.expiry':'confirmed_expired'},['B-G01','B-P08'])
    r=E.evaluate(q)['results'][0]
    assert r['action_types']==['defer_specific_recommendation']
    assert r['suppressed_advice']['by_cards']==['B-P08']
    assert r['recommendation_text']!=r['suppressed_advice']['text']


def test_ask_answer_reevaluate_conflict_resolution_and_decline():
    q=request({},['B-C01']);first=E.evaluate(q)
    assert first['questions'][0]['field']=='method.water_temperature'
    q,second=E.answer(q,request({'method.water_temperature':'hot'})['facts'])
    assert second['overall']=='adjust'
    q,third=E.answer(q,request({'method.water_temperature':'lukewarm'})['facts'])
    assert third['results'][0]['comparison_status']=='conflicting'
    with pytest.raises(ValueError):E.answer(q,request({'method.water_temperature':'lukewarm'})['facts'])
    q,last=E.answer(q,request({'method.water_temperature':'lukewarm'})['facts'],resolve_conflicts=['method.water_temperature'])
    assert last['overall']=='maintain' and 'previous_observation' in q['facts']['method.water_temperature']
    refused=request({},['B-H01']);refused['facts']['cycle.observation_consent']={'state':'declined','source':'user_report','reference':'choice','value':None}
    assert E.evaluate(refused)['questions']==[]


def test_cross_site_and_deduplication():
    assert evaluate({'method.water_temperature':'hot'},'B-C01','hands')['comparison_status']=='not_applicable'
    q=request({},['B-M02','B-G02']);out=E.evaluate(q)
    assert len({q['field'] for q in out['questions']})==len(out['questions'])
    assert len({(tuple(g['action_types']),g['text']) for g in out['guidance']})==len(out['guidance'])
    assert {c for g in out['guidance'] for c in g['card_ids']}=={'B-M02','B-G02'}


def test_reviewed_filter_records_and_unknown_not_promoted():
    r={'filter_id':'SYNTHETIC-FILTER','reviewed_on':'synthetic-date','reviewed_by':'fixture','solubility_source_ids':['FIXTURE'],'size_classification_version':'fixture',
       'relative_size_tag':'higher_relative_reviewed','oil_solubility_class':'oil_soluble_under_reported_conditions','particle_or_dispersion_form':'molecular_dissolution',
       'molecular_mass_g_mol':123,'molecular_mass_source_ids':['SYNTHETIC-NOT-REAL'],
       'relative_size_tag_basis':'Synthetic reviewed tag, not derived from 123',
       'oil_solubility_conditions':'Synthetic specified conditions, not a real filter property'}
    assert classify_filters(['SYNTHETIC-FILTER'],[r])['profile']=='matches_reviewed_preference'
    assert classify_filters(['SYNTHETIC-FILTER','UNKNOWN'],[r])['profile']=='unclassified'
    r['particle_or_dispersion_form']='particulate_dispersion'
    assert classify_filters(['SYNTHETIC-FILTER'],[r])['profile']=='alternative_particulate_path'
    original=E.kb['uv_filter_property_examples']
    assert classify_filters(['UV-PBSA'],original)['profile']=='unclassified'


def test_original_expectations_not_rewritten_or_xfailed():
    report=run()
    assert len(report['scenarios'])==57
    assert all(r['facts_unchanged'] for r in report['scenarios'])
    assert not any(r['category']=='implementation_failure' for r in report['scenarios'])
    assert report['summary']['expected_satisfied']<57  # Spec/policy gaps are not normal passes.


def test_unrelated_basics_survive_quality_hold_and_stage_filters():
    q=request({'method.water_temperature':'lukewarm','storage.expiry':'confirmed_expired'},['B-C01','B-P08'])
    out=E.evaluate(q)
    assert out['results'][0]['action_types']==['maintain']
    q=request({'method.water_temperature':'hot','commerce.authorized_path':'confirmed'})
    q['lifecycle_stage']='purchase'
    assert all('purchase' in E.cards[r['card_id']]['lifecycle_stage_ids'] for r in E.evaluate(q)['results'])
    q['lifecycle_stage']='invented'
    with pytest.raises(ValueError):E.evaluate(q)


def test_real_product_label_instruction_and_allergen_override():
    q=request({'method.water_temperature':'hot','product.instructions':'specific_instruction_overrides_general'},['B-C01'])
    assert E.evaluate(q)['results'][0]['comparison_status']=='exception'
    q=request({'product.fragrance':'fragrance_free','person.known_allergies':'confirmed_product_allergen'},['B-G01'])
    out=E.evaluate(q)
    assert out['results'][0]['comparison_status']=='exception'
    assert 'maintain' not in out['results'][0]['action_types']


def test_all_documented_enum_values_execute_same_branch_contract():
    for cid,branch in BRANCHES:
        for field,values in branch['when'].items():
            for value in values:
                facts={k:v[0] for k,v in branch['when'].items()};facts[field]=value
                q=request(facts,[cid])
                if cid in ('B-M04','B-L02'):q['body_site']='hands'
                if cid in ('B-G13','B-G14','B-G15') and branch['status']=='difference':
                    pair=next(p for p in E.kb['combination_policy']['pairs'] if p['card_id']==cid)
                    q['facts'].update(request({'product.reviewed_role_pair':[pair['left'],pair['right']]})['facts'])
                assert E.evaluate(q)['results'][0]['comparison_status']==branch['status'],(cid,field,value)


def test_unknown_semantic_value_requests_clarification_not_silent_hold():
    out=E.evaluate(request({'method.water_temperature':'unmapped_free_text'},['B-C01']))
    assert out['results'][0]['comparison_status']=='unknown'
    assert 'method.water_temperature' in out['results'][0]['unrecognized_fields']
    assert any(q['field']=='method.water_temperature' for q in out['questions'])


def test_optional_recent_events_decline_preserves_general_guidance():
    q=request({},['B-H02']);q['facts']['routine.change_log']={'state':'declined','value':None,'source':'user_report','reference':'synthetic explicit choice'}
    out=E.evaluate(q)
    assert out['results'][0]['comparison_status']=='not_applicable'
    assert out['questions']==[]
    assert out['results'][0]['action_types']==['inform_general_practice']


def test_explicit_hand_severity_and_spray_type_boundaries():
    assert evaluate({'skin.hand_observation':'severe_pain'},'B-M04','hands')['action_types']==['refer_for_professional_review']
    assert evaluate({'product.application_form':'aerosol','sun.application_method':'direct_face_spray'},'B-P09')['comparison_status']=='difference'
    assert evaluate({'product.application_form':'cream'},'B-P09')['comparison_status']=='not_applicable'


def test_known_spec_gap_does_not_mask_new_implementation_regression():
    from skin_engine.kb_preview.audit import assess
    scenario=next(s for s in E.kb['acceptance_scenarios'] if s['id']=='T17')
    out=E.evaluate(request(scenario['facts'],scenario['card_ids']))
    out['results'][1]['comparison_status']='conflicting'
    assert assess(scenario,out)['category']=='implementation_failure'
