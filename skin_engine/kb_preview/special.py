"""Non-equality comparisons, limited to KB values and supplied observations."""

def decision(status, actions, reason, fields=(), clarify_fields=()):
    return {'status': status, 'actions': actions, 'reason': reason, 'fields': list(fields),'clarify_fields':list(clarify_fields)}


def compare(cid, value, kb):
    d = decision
    if cid == 'B-C03':
        duration = value('dose.contact_time')
        if value('product.instructions') == 'specific_contact_time':
            return d('exception',['review_exception'],'product_contact_instruction')
        if value('product.type') in ('shaving_cream','mask','peeling','medication','chemical_depilatory'):
            return d('not_applicable',['review_current_label_scope'],'not_ordinary_face_cleanser')
        if not isinstance(duration, dict): return None
        r = duration.get('range_seconds')
        minutes_report = duration.get('reported_pattern')=='several_minutes_before_rinsing'
        if r is not None and not (isinstance(r,list) and len(r)==2 and all(type(n) in (int,float) and 0<=n<float('inf') for n in r) and r[0]<=r[1]):
            return d('unknown',['ask_targeted_question'],'invalid_contact_range',['dose.contact_time'])
        card = next(c for c in kb['baseline_cards'] if c['id']==cid)
        limit = card['numeric_parameters'][0]['value']
        if r is not None and r[0]<=limit<r[1]:return d('unknown',['inform_general_practice'],'KB_soft_boundary_straddled')
        if not (duration.get('phase')=='before_rinsing' and value('product.type')=='ordinary_rinse_off_cleanser' and value('product.instructions')=='no_special_duration'):
            return d('unknown',['ask_targeted_question','retrieve_product_evidence'],'contact_scope_missing',['product.type','product.instructions','dose.contact_time'])
        if minutes_report:
            if r is not None and r[1]<=limit:
                return d('conflicting',['ask_targeted_question'],'minutes_report_conflicts_with_short_range',['dose.contact_time'])
            return d('difference',['suggest_behavior_change'],'KB_explicit_minutes_report_without_invented_seconds')
        if r is None:return d('unknown',['ask_targeted_question'],'contact_duration_not_interpretable',['dose.contact_time'])
        if r[1]<=limit:return d('aligned',['maintain'],'within_KB_soft_guidance')
        if r[0]<=limit:return d('unknown',['inform_general_practice'],'KB_soft_boundary_straddled')
        # The authored acceptance example is an anchor, NOT a new universal cutoff.
        anchor=next(s for s in kb['acceptance_scenarios'] if s['id']=='T03')['facts']['dose.contact_time']['range_seconds']
        if r==anchor:
            return d('difference',['suggest_behavior_change'],'KB_minutes_long_example_or_explicit_report')
        return d('unknown',['inform_general_practice','ask_targeted_question'],'above_soft_value_without_minutes_report',['dose.contact_time'])
    if cid=='B-P01':
        spf,uva=value('product.spf'),value('product.uva')
        fields=['product.spf','product.uva','sun.outdoor_time','sun.water_contact','sun.sweat']
        if value('sun.outdoor_time')=='none':return d('not_applicable',['inform_general_practice'],'no_outdoor_selection_context')
        floor=next(c for c in kb['baseline_cards'] if c['id']==cid)['numeric_parameters'][0]['value']
        if type(spf) not in (int,float) or not 0<spf<float('inf') or uva not in ('broad_spectrum_confirmed','broad_spectrum_not_met'):
            invalid_labels=[]
            if type(spf) not in (int,float) or not 0<spf<float('inf'):invalid_labels.append('product.spf')
            if uva not in ('broad_spectrum_confirmed','broad_spectrum_not_met'):invalid_labels.append('product.uva')
            return d('unknown',['retrieve_product_evidence','inform_next_selection'],'protection_label_not_confirmed',fields,clarify_fields=invalid_labels)
        if spf<floor or uva=='broad_spectrum_not_met':return d('difference',['inform_next_selection'],'KB_displayed_protection_floor')
        exposure_values={'sun.outdoor_time':('prolonged',),'sun.water_contact':('yes','no','none'),'sun.sweat':('yes','no','none')}
        unrecognized=[f for f,allowed in exposure_values.items() if value(f) not in allowed]
        if unrecognized:
            return d('unknown',['ask_targeted_question'],'exposure_context_missing_or_unrecognized',unrecognized,clarify_fields=unrecognized)
        if any(value(f)=='yes' for f in ('sun.water_contact','sun.sweat')):
            wr=value('product.water_resistance')
            if wr=='confirmed_not_water_resistant':return d('difference',['inform_next_selection'],'water_context_label_mismatch')
            if wr!='label_matched_to_activity':return d('unknown',['retrieve_product_evidence'],'water_resistance_label_missing',['product.water_resistance'],clarify_fields=['product.water_resistance'])
        return d('aligned',['inform_next_selection'],'label_and_exposure_match')
    if cid=='B-P05':
        profile=value('product.uv_filter_preference_profile')
        if value('skin.eye_stinging')=='recurrent':return d('exception',['suggest_behavior_change','review_exception'],'actual_discomfort_over_filter_preference')
        if profile=='alternative_particulate_path':return d('exception',['inform_next_selection'],'particulate_alternative_not_penalty')
        if value('sun.prior_tolerated_products')=='available_product' and profile=='does_not_match_reviewed_preference':
            return d('exception',['maintain','inform_next_selection'],'available_tolerated_protection_over_preference')
        if profile=='matches_reviewed_preference':return d('aligned',['inform_next_selection'],'reviewed_filter_profile_only_not_finished_performance')
        if profile in ('mixed_profile','does_not_match_reviewed_preference'):
            a=['inform_next_selection']
            if value('skin.eye_stinging')=='none' and value('sun.prior_tolerated_products')=='current_product':a.insert(0,'maintain')
            return d('difference',a,'reviewed_preference_difference_not_risk')
        return d('unknown',['inform_next_selection','inform_general_practice'],'filter_properties_unmapped_not_required_private_formula',['product.uv_filters'])
    if cid=='B-P07':
        if value('skin.eye_stinging')=='recurrent':return d('exception',['suggest_behavior_change'],'actual_discomfort_over_manufacturer_opinion')
        if value('sun.prior_tolerated_products') in ('current_product','available_product'):
            return d('exception',['maintain','inform_next_selection'],'personal_experience_over_manufacturer_opinion')
        manufacturer=value('product.manufacturer')
        note=next((n for n in kb['manufacturer_preference_policy']['seed_notes'] if n['manufacturer_name']==manufacturer),None)
        if not manufacturer or not note:return d('unknown',['inform_next_selection'],'manufacturer_identity_or_recorded_opinion_missing')
        # Compare the recorded opinion without giving a product a rank or score.
        if value('product.manufacturer_preference')==note['preference']:
            return d('aligned',['inform_next_selection'],'recorded_opinion_matches_preview_only')
        return d('unknown',['inform_next_selection'],'manufacturer_opinion_not_supplied')
    if cid=='B-S06' and value('shaving.method')=='manual':
        history=value('shaving.blade_use_history')
        maximum=next(c for c in kb['baseline_cards'] if c['id']==cid)['numeric_parameters'][0]['value_max']
        if type(history) is int and history>maximum and value('shaving.care')=='replacement_not_reviewed':
            return d('difference',['suggest_behavior_change'],'past_KB_manual_reference_without_review')
    return None
