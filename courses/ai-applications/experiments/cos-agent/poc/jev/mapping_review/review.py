"""Offline, synthetic-only mapping inspection. Never authorizes a write."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from .event_review import review_events, usable

CONTRACT = json.loads((Path(__file__).with_name('contract.json')).read_text(encoding='utf-8'))
TOP = {'version', 'kind', 'observed_at', 'concern_presence', 'persistence',
       'recent_change', 'discomfort_presence', 'discomfort_types', 'sensitivity_history'}
# A proposal for review, not an authoritative semantic equivalence or confirmation.
DIRECT = {'stinging': 'stinging', 'itching': 'itching', 'redness': 'redness_tendency'}
UNREPRESENTED = ('severity', 'onset_date', 'onset_time', 'recognition_time')
SUPPORTED_SCHEMAS = ('relations-0.2', 'relations-0.3', 'relations-0.4', 'relations-0.5')


def validate_snapshot(value):
    errors = []
    if not isinstance(value, dict) or set(value) != TOP:
        return ['skin_state_keys_mismatch']
    if value['version'] != CONTRACT['version'] or value['kind'] not in CONTRACT['record_kinds']:
        errors.append('version_or_kind_invalid')
    try:
        if not isinstance(value['observed_at'], str):
            raise ValueError
        stamp = datetime.fromisoformat(value['observed_at'].replace('Z', '+00:00'))
        if stamp.tzinfo is None or stamp.utcoffset() != timedelta(0):
            raise ValueError
    except (ValueError, TypeError, OverflowError):
        errors.append('observed_at_invalid_utc')
    for key, allowed in CONTRACT['fields'].items():
        v = value[key]
        if key == 'discomfort_types':
            if not isinstance(v, list) or any(not isinstance(x, str) or x not in allowed for x in v):
                errors.append('discomfort_types_invalid')
            elif len(set(v)) != len(v):
                errors.append('discomfort_types_duplicate')
            elif (value['discomfort_presence'] == 'reported') != bool(v):
                errors.append('discomfort_presence_mismatch')
        elif not isinstance(v, str) or v not in allowed:
            errors.append(key + '_invalid')
    if value['concern_presence'] != 'reported':
        for key in ('persistence', 'recent_change'):
            if value[key] not in ('not_applicable', 'unknown', 'not_asked', 'user_refused'):
                errors.append(key + '_requires_concern')
    return errors


def symptom_findings(features, proposed=None):
    if not isinstance(features, dict) or features.get('schema_version') not in SUPPORTED_SCHEMAS:
        raise ValueError('supported relations-0.2 through relations-0.5 features required')
    legacy = features['schema_version'] == 'relations-0.2'
    symptoms = features.get('symptoms')
    if not isinstance(symptoms, list):
        raise ValueError('symptoms list required')
    findings = []
    for index, symptom in enumerate(symptoms):
        if not isinstance(symptom, dict) or not isinstance(symptom.get('relations'), dict):
            findings.append({'index': index, 'issue': 'malformed_symptom'}); continue
        relations = symptom['relations']
        def val(key):
            item = relations.get(key)
            return item.get('value') if isinstance(item, dict) else None
        name, state, subject = symptom.get('symptom'), val('state'), val('subject')
        if not isinstance(name, str) or not isinstance(state, str) or not isinstance(subject, str):
            findings.append({'index': index, 'issue': 'missing_symptom_state_or_subject'}); continue
        if name not in ('dryness', 'breakout', 'redness', 'stinging', 'itching') or state not in (
                'affirmed', 'denied', 'negated', 'hypothetical', 'conflict', 'unknown', 'declined', 'not_mentioned') or subject not in ('self', 'other', 'unknown'):
            findings.append({'index': index, 'issue': 'unsupported_symptom_value'}); continue
        item = {'index': index, 'symptom': name, 'state': state, 'subject': subject}
        correction = relations.get('correction', {})
        assessed = all(usable(relations.get(k), legacy) for k in ('state', 'subject'))
        if not assessed:
            item['issue'] = 'unassessed_or_uncertain_symptom_do_not_map'
        elif isinstance(correction, dict) and correction.get('value') == 'superseded':
            item['issue'] = 'superseded_symptom_do_not_map'
        elif isinstance(correction, dict) and correction and (
                correction.get('value') != 'current' or not usable(correction, legacy)):
            item['issue'] = 'uncertain_correction_do_not_map'
        elif state == 'affirmed' and subject == 'self' and name in DIRECT:
            target = DIRECT[name]
            item.update(issue='candidate_requires_user_and_time_confirmation', target='discomfort_types',
                        suggested_value=target,
                        present_in_proposed=isinstance(proposed, dict) and isinstance(proposed.get('discomfort_types'), list) and target in proposed['discomfort_types'])
        elif state == 'affirmed' and subject == 'self':
            item['issue'] = 'no_direct_target_review_required'
        else:
            item['issue'] = 'not_a_confirmed_positive_do_not_map_as_present'
        extra = [key for key in UNREPRESENTED if val(key) not in (None, 'not_mentioned', 'unknown')]
        if extra:
            item['no_direct_skin_state_field'] = extra
        findings.append(item)
    return findings


def review(features, proposed):
    findings = symptom_findings(features, proposed)
    legacy = features['schema_version'] == 'relations-0.2'
    symptoms = features['symptoms']
    errors = validate_snapshot(proposed)
    warnings = []
    if legacy:
        warnings.append('legacy_assessment_metadata_may_be_missing')
    if features.get('warnings'):
        warnings.append('jev_warnings_present')
    if features.get('clarifications'):
        warnings.append('jev_clarifications_present')
    if not symptoms:
        warnings.append('no_detected_symptoms_does_not_mean_none')
    # A declared detail must have an eligible matching candidate; extra values may
    # come from other sources, so request review rather than asserting invalidity.
    candidate_values = {x['suggested_value'] for x in findings if 'suggested_value' in x}
    if isinstance(proposed, dict) and isinstance(proposed.get('discomfort_types'), list):
        if any(x not in candidate_values for x in proposed['discomfort_types']):
            warnings.append('proposed_detail_has_no_eligible_jev_candidate_review_other_sources')
    return {'schema_version': 'mapping-review-0.2',
            'source_schema_version': features['schema_version'],
            'mode': 'synthetic_offline_review_only', 'contract_snapshot': CONTRACT['snapshot'],
            'contract_errors': errors, 'findings': findings, 'warnings': warnings,
            'usage_event_findings': review_events(features),
            'user_confirmation_verified': False, 'authorized_for_storage': False}


def main():
    parser = argparse.ArgumentParser(description='Review synthetic Jev features and proposed skin_state JSON; no storage or network.')
    parser.add_argument('jev_json', help='synthetic relations-0.2 through 0.5 JSON, or features/result wrapper')
    parser.add_argument('skin_state_json', help='synthetic proposed skin_state object or {"skin_state": object}')
    args = parser.parse_args()
    try:
        source = json.loads(Path(args.jev_json).read_text(encoding='utf-8'))
        target = json.loads(Path(args.skin_state_json).read_text(encoding='utf-8'))
        source = source.get('features', source.get('result', source)) if isinstance(source, dict) else source
        target = target.get('skin_state', target) if isinstance(target, dict) else target
        result = review(source, target)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        parser.exit(2, 'Invalid input file or unsupported Jev schema. No input content printed.\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['contract_errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
