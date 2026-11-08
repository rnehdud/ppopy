"""Offline event inspection; never converts events into skin_state or writes."""
import math


def usable(relation, legacy=False):
    if not isinstance(relation, dict):
        return False
    status = relation.get('status')
    if legacy and status is None:
        return True  # historical 0.2 fixtures lack assessment metadata
    if status == 'rule_candidate':
        return bool(relation.get('method'))
    score = relation.get('score')
    return (status == 'candidate' and not isinstance(score, bool)
            and isinstance(score, (int, float)) and math.isfinite(score) and .5 < score <= 1)


def review_events(features):
    events = features.get('usage_events', [])
    if not isinstance(events, list):
        return [{'issue': 'malformed_usage_events'}]
    findings = []
    for index, event in enumerate(events):
        item = {'index': index, 'target': None, 'authorized_for_storage': False}
        if not isinstance(event, dict) or not isinstance(event.get('relations'), dict):
            findings.append({**item, 'issue': 'legacy_or_malformed_event_requires_review'})
            continue
        rel = event['relations']
        values = {key: rel.get(key, {}).get('value') if isinstance(rel.get(key), dict) else None
                  for key in ('usage_state', 'subject', 'correction', 'product_link')}
        # Output enum values only, not source text, product names/IDs or spans.
        allowed = {'usage_state': ('affirmed', 'denied', 'planned', 'hypothetical', 'conflict', 'unknown', 'declined', 'not_mentioned'),
                   'subject': ('self', 'other', 'unknown'),
                   'correction': ('current', 'superseded', 'unknown'),
                   'product_link': ('linked', 'unlinked', 'unknown')}
        item.update({k: v if v in allowed[k] else None for k, v in values.items()})
        if not all(usable(rel.get(k)) and values[k] in allowed[k] for k in allowed):
            issue = 'unassessed_or_uncertain_event_do_not_map'
        elif values['correction'] == 'superseded':
            issue = 'superseded_event_do_not_map'
        elif values['product_link'] != 'linked':
            issue = 'unresolved_product_link_do_not_map'
        elif values['subject'] != 'self':
            issue = 'not_self_usage_do_not_map'
        elif values['usage_state'] == 'affirmed':
            issue = 'actual_use_report_requires_confirmation_and_separate_contract'
        else:
            issue = 'not_actual_use_do_not_map_as_used'
        item['issue'] = issue
        item['no_direct_skin_state_field'] = True
        item['requires'] = ['usage_event_contract', 'verified_product_and_version',
                            'event_time_precision_review', 'user_confirmation', 'server_authorization']
        findings.append(item)
    return findings
