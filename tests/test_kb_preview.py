import json
from copy import deepcopy
import pytest
from skin_engine.kb_preview import PreviewEngine, load_kb
from skin_engine.kb_preview.engine import STATUSES, DEFAULT_KB

KB,_=load_kb()
SCENARIOS=KB['acceptance_scenarios']
ENGINE=PreviewEngine()

def request(facts=None, cards=None):
    result={'mode':'development_preview','project':'Poppy','data_kind':'synthetic','population':'adult','body_site':(facts or {}).get('method.body_site','face'),
        'product_instance_id':'TEST-ONLY','facts':{k:{'state':'unknown' if v is None else 'known','value':v,
        'source':'synthetic_fixture','reference':'test input'} for k,v in (facts or {}).items()}}
    if cards is not None:result['card_ids']=cards
    return result

@pytest.mark.parametrize('scenario',SCENARIOS,ids=lambda s:s['id'])
def test_acceptance(scenario):
    from skin_engine.kb_preview.audit import assess
    out=ENGINE.evaluate(request(scenario['facts'],scenario['card_ids']))
    assert out['production_enabled'] is False
    assert all(r['comparison_status'] in STATUSES for r in out['results'])
    result=assess(scenario,out)
    assert result['category']=='expected_satisfied', result


def test_input_conflict_and_instruction_precedence():
    r=request({'method.water_temperature':'hot'},['B-C01'])
    r['facts']['method.water_temperature']['state']='conflicting'
    assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='conflicting'
    r['facts']['context.individual_instruction']={'state':'known','value':True,'source':'user_report','reference':'local report'}
    assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='exception'


def test_no_default_literature_or_unknown_value_becomes_user_fact():
    for source in ['service_default','literature']:
        r=request({'method.water_temperature':'hot'},['B-C01'])
        r['facts']['method.water_temperature']['source']=source
        assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='unknown'


def test_schema_and_environment_rejections(tmp_path):
    for change in [{'project':'AFA'},{'mode':'production'},{'population':'infant'}]:
        r=request({'method.water_temperature':'hot'},['B-C01']);r.update(change)
        if 'population' in change:assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='not_applicable'
        else:
            with pytest.raises(ValueError):ENGINE.evaluate(r)
    r=request({'method.water_temperature':'hot'},['B-C01']);r['data_kind']='local_review'
    with pytest.raises(ValueError):ENGINE.evaluate(r)
    for mutate in [lambda k:k['baseline_cards'].append(k['baseline_cards'][0]),
                   lambda k:k['metadata'].update(production_enabled=True),
                   lambda k:k['baseline_cards'][0]['evidence']['source_ids'].append('MISSING')]:
        k=deepcopy(KB);mutate(k);p=tmp_path/'bad.json';p.write_text(json.dumps(k))
        with pytest.raises(ValueError):load_kb(p)


def test_generalization_selection_questions_and_followup():
    out=ENGINE.evaluate(request({'method.water_temperature':'hot'}))
    assert next(r for r in out['results'] if r['card_id']=='B-C01')['comparison_status']=='difference'
    out=ENGINE.evaluate(request({},['B-C01']))
    assert any(q['field']=='method.water_temperature' for q in out['questions'])
    out=ENGINE.evaluate(request({'method.water_temperature':'lukewarm'},['B-C01']))
    assert out['overall']=='maintain' and out['questions']==[]
    assert out['results'][0]['sources'] and out['kb_sha256']


def test_reviewed_combination_and_no_inci_guess():
    facts={'routine.co_use_context':'same_area_same_session','product.combination_design':'separate_products','product.active_care_roles':'reviewed_pair','product.reviewed_role_pair':['retinoid','aha_exfoliating']}
    out=ENGINE.evaluate(request(facts,['B-G13']))
    assert out['results'][0]['comparison_status']=='difference'
    facts['product.active_care_roles']='ingredient_only_unclassified'
    assert ENGINE.evaluate(request(facts,['B-G13']))['results'][0]['comparison_status']=='unknown'


def test_spray_requires_actual_use_and_scope():
    facts={'product.application_form':'nongas_spray','sun.application_method':'direct_face_spray'}
    assert ENGINE.evaluate(request(facts,['B-P09']))['results'][0]['comparison_status']=='difference'
    r=request({'method.water_temperature':'hot'},['B-C01']);r['body_site']='hands'
    assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='not_applicable'


def test_adapter_isolates_products_and_keeps_catalog_gaps():
    from skin_engine.kb_preview.adapter import evaluate_routine, catalog_observations
    obs=catalog_observations({'product':{'product_id':'x','name':'test','ph':None}},reference='fixture')
    assert obs['product.ph']['state']=='unknown' and 'product.active_care_roles' not in obs
    context=request({},['B-G01'])
    products=[{'product_instance_id':pid,'kind':'test','facts':request({'product.fragrance':value})['facts']}
              for pid,value in [('a','fragrance_free'),('b','declared_present')]]
    out=evaluate_routine(context,products)
    assert [o['results'][0]['comparison_status'] for o in out]==['aligned','difference']
    with pytest.raises(ValueError):evaluate_routine(context,[products[0],products[0]])


def test_refused_questions_and_unknown_cards():
    r=request({},['B-C01']);r['facts']['method.water_temperature']={'state':'declined','value':None,'source':'user_report','reference':'local'}
    assert ENGINE.evaluate(r)['questions']==[]
    with pytest.raises(ValueError):ENGINE.evaluate(request({},['invented-rule']))


def test_quality_priority_and_incomplete_combination():
    out=ENGINE.evaluate(request({'commerce.authenticity_concern':'specific_concern'},['B-Q06','B-G11']))
    assert out['results'][1]['action_types']==['defer_specific_recommendation']
    out=ENGINE.evaluate(request({'routine.co_use_context':'same_area_same_session','product.combination_design':'separate_products','product.active_care_roles':'reviewed_pair'},['B-G13']))
    assert out['results'][0]['comparison_status']=='unknown'


def test_contradictory_scope_is_not_silently_applied():
    r=request({'method.body_site':'face','method.water_temperature':'hot'},['B-C01'])
    r['body_site']='hands'
    assert ENGINE.evaluate(r)['results'][0]['comparison_status']=='conflicting'
