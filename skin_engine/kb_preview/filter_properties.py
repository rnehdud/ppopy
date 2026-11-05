"""Reviewed per-filter records only. No molecular-weight cutoff or INCI guesses."""
from copy import deepcopy
from .engine import load_kb

def classify_filters(identities, records):
    categories=load_kb()[0]['uv_filter_knowledge_contract']['controlled_categories']
    if not isinstance(identities,list) or not all(isinstance(i,str) and i for i in identities):raise ValueError('Exact filter identities required')
    if len({r['filter_id'] for r in records})!=len(records):raise ValueError('Duplicate filter record')
    index={r['filter_id']:r for r in records};details=[]
    for identity in identities:
        r=index.get(identity)
        reviewed=bool(r and r.get('reviewed_on') and r.get('reviewed_by') and r.get('solubility_source_ids') and r.get('size_classification_version'))
        if not reviewed:details.append({'filter_id':identity,'state':'unmapped_or_unreviewed','record':deepcopy(r)});continue
        tag=r.get('relative_size_tag');oil=r.get('oil_solubility_class');form=r.get('particle_or_dispersion_form')
        if any(r.get(field) not in allowed for field,allowed in categories.items() if field!='water_solubility_class'):
            state='unknown_properties'
        elif form=='particulate_dispersion':state='particulate'
        elif tag=='unclassified' or oil in (None,'unknown','not_established') or form in (None,'unknown','grade_dependent'):state='unknown_properties'
        elif not (type(r.get('molecular_mass_g_mol')) in (int,float) and 0<r['molecular_mass_g_mol']<float('inf')
                  and r.get('molecular_mass_source_ids') and r.get('relative_size_tag_basis') and r.get('oil_solubility_conditions')):
            state='unknown_properties'
        elif form=='molecular_dissolution' and tag=='higher_relative_reviewed' and oil=='oil_soluble_under_reported_conditions':state='preferred'
        elif form=='molecular_dissolution' and tag in ('higher_relative_reviewed','lower_relative_reviewed'):state='other_reviewed'
        else:state='unknown_properties'
        details.append({'filter_id':identity,'state':state,'record':deepcopy(r)})
    states={d['state'] for d in details}
    if not states or states & {'unmapped_or_unreviewed','unknown_properties'}:profile='unclassified'
    elif states=={'preferred'}:profile='matches_reviewed_preference'
    elif states=={'particulate'}:profile='alternative_particulate_path'
    elif 'preferred' in states or 'particulate' in states:profile='mixed_profile'
    else:profile='does_not_match_reviewed_preference'
    return {'profile':profile,'filters':details,'production_enabled':False,'finished_product_performance_inferred':False}
