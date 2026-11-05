"""Explicitly isolated MP-01 qualitative candidate comparison. Never a score."""
from .engine import load_kb

REQUIRED=('spf','uva','activity_protection','quality','personal_discomfort',
          'personal_successful_use','clinician_plan','essential_functions')

def compare_candidates(candidates, *, mode='source_blind'):
    out={'production_enabled':False,'mode':mode,'candidate_ids':[c['id'] for c in candidates],
         'preferred_ids':[],'numeric_scores':None,'evidence':['MP-01','B-P07'],'status':'not_applied'}
    if mode=='source_blind':return dict(out,reason='source_blind_no_manufacturer_preference')
    if mode!='development_qualitative_tiebreaker':raise ValueError('Unsupported development policy')
    if len(candidates)<2 or len(set(out['candidate_ids']))!=len(candidates):
        raise ValueError('At least two uniquely identified candidates required')
    for c in candidates:
        if c.get('category')!='sunscreen':return dict(out,reason='outside_sunscreen_scope')
        if any(c.get(k) is None for k in REQUIRED):return dict(out,status='unknown',reason='equivalence_information_missing')
        if (c['quality']!='no_known_problem' or c['personal_discomfort']!='none'
            or c['personal_successful_use']!='none' or c['clinician_plan']!='none'
            or c['uva']!='broad_spectrum_confirmed' or c['activity_protection']!='met'
            or c['essential_functions']!='met'):
            return dict(out,reason='personal_quality_or_required_protection_priority')
    kb,_=load_kb()
    floor=next(c for c in kb['baseline_cards'] if c['id']=='B-P01')['numeric_parameters'][0]['value']
    if any(type(c['spf']) not in (int,float) or not floor<=c['spf']<float('inf') for c in candidates):
        return dict(out,reason='required_spf_not_met')
    if any(any(c[k]!=candidates[0][k] for k in REQUIRED) for c in candidates[1:]):
        return dict(out,reason='major_conditions_not_equal')
    # Unknown manufacturer is never ranked below a known one.
    if any(c.get('manufacturer_verified') is not True or not isinstance(c.get('manufacturer'),str) or not c['manufacturer'].strip()
           or not c.get('manufacturer_evidence') or not c.get('formula_version') for c in candidates):
        return dict(out,status='unknown',reason='manufacturer_version_evidence_missing_no_penalty')
    notes=kb['manufacturer_preference_policy']['seed_notes']
    favored=[c['id'] for c in candidates if any(n['manufacturer_name']==c.get('manufacturer') and
             n['preference']=='qualitative_favorable_tiebreaker' for n in notes)]
    return dict(out,preferred_ids=favored,status='qualitative_preference' if favored else 'no_recorded_preference',
                reason='recorded_opinion_only_not_comparative_quality',opinion_notes=notes)
