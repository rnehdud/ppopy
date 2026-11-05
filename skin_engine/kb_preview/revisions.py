"""User-authorized development revisions; raw KB acceptance is never overwritten."""
from copy import deepcopy
from .engine import PreviewEngine
from .audit import request,assess
from .manufacturer_preview import compare_candidates

def revised_cases():
    engine=PreviewEngine(); source={s['id']:s for s in engine.kb['acceptance_scenarios']}
    changes={
      'T17':{'product.spf':30,'product.uva':'broad_spectrum_confirmed',
             'sun.outdoor_time':'prolonged','sun.water_contact':'none','sun.sweat':'none'},
      'V06-T04':{'product.combination_design':'separate_products','product.active_care_roles':'reviewed_pair',
                'product.reviewed_role_pair':['retinoid','aha_exfoliating']},
      'T37':{},'T45':{}}
    results=[]
    for sid,extra in changes.items():
        case=deepcopy(source[sid]);case['facts'].update(extra)
        if sid in ('T37','T45'):case['expected_comparison']='mixed_by_card'
        out=engine.evaluate(request(case['facts'],case['card_ids']))
        row=assess(case,out)
        # Assess normally labels signatures of the ORIGINAL failures only.
        row.update(revision_of=sid,revision_id=sid+'-DEV-20261105',synthetic=True,
                   original_facts_preserved=True,facts_unchanged=not bool(extra),added_synthetic_facts=extra,
                   aggregate_comparison=out['aggregate_comparison'],result=out)
        results.append(row)
    return results

def manufacturer_example():
    common={'category':'sunscreen','spf':30,'uva':'broad_spectrum_confirmed','activity_protection':'met',
      'quality':'no_known_problem','personal_discomfort':'none','personal_successful_use':'none',
      'clinician_plan':'none','essential_functions':'met','manufacturer_verified':True,
      'manufacturer_evidence':'synthetic label fixture','formula_version':'synthetic-v1'}
    candidates=[dict(common,id='SYN-A',manufacturer='한국콜마'),dict(common,id='SYN-B',manufacturer='synthetic_other')]
    return {'revision_of':'T20','single_card_result':PreviewEngine().evaluate(request({
        'product.manufacturer':'한국콜마','product.manufacturer_preference':'qualitative_favorable_tiebreaker',
        'constraints.decision_context':'new_selection'},['B-P07'])),
        'candidates':candidates,'production_policy_result':compare_candidates(candidates),
        'development_result':compare_candidates(candidates,mode='development_qualitative_tiebreaker')}
