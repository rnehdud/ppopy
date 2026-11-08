"""Build a partial skin-state proposal, not a complete or confirmed payload."""
from .review import CONTRACT, DIRECT, symptom_findings
from .event_review import review_events, usable


def map_candidates(features):
    findings = symptom_findings(features)
    blockers = []
    if features.get('warnings'):
        blockers.append('extraction_warnings_require_review')
    intake = features.get('intake_status', {}).get('symptoms', {})
    if intake.get('value') == 'declined':
        blockers.append('symptom_information_declined')
    if features['schema_version'] == 'relations-0.2':
        blockers.append('legacy_assessment_metadata_requires_review')

    # Positive and negative reports may concern different times. Without a
    # confirmed observation context they must not collapse into a current state.
    opposed = set()
    for symptom in features['symptoms']:
        if not isinstance(symptom, dict):
            continue
        rel = symptom.get('relations', {})
        if not isinstance(rel, dict):
            continue
        state, subject = rel.get('state', {}), rel.get('subject', {})
        if (usable(state) and usable(subject) and subject.get('value') == 'self'
                and state.get('value') in ('denied', 'conflict', 'unknown', 'declined')):
            name = symptom.get('symptom')
            if isinstance(name, str) and name in DIRECT:
                opposed.add(DIRECT[name])

    candidates = []
    for finding in findings:
        value = finding.get('suggested_value')
        if value is None:
            continue
        if value in opposed:
            finding['mapping_issue'] = 'opposed_reports_require_time_and_state_confirmation'
            continue
        if blockers:
            finding['mapping_issue'] = 'blocked_pending_review'
            continue
        candidates.append({'field': 'discomfort_types', 'value': value,
                           'symptom_index': finding['index'], 'confirmation_status': 'pending'})
    values = list(dict.fromkeys(c['value'] for c in candidates))
    patch = {'discomfort_presence': 'reported', 'discomfort_types': values} if values else {}
    missing = [field for field in ('kind', 'observed_at', *CONTRACT['fields']) if field not in patch]
    return {
        'schema_version': 'skin-state-mapping-0.1',
        'source_schema_version': features['schema_version'],
        'source_text_revision': features.get('text_revision'),
        'contract_snapshot': CONTRACT['snapshot'],
        'target_version': CONTRACT['version'],
        'skin_state_patch': patch,
        'candidates': candidates,
        'findings': findings,
        'usage_event_findings': review_events(features),
        'missing_fields': missing,
        'blockers': blockers,
        'confirmation_status': 'pending',
        'requires': ['user_and_observation_time_confirmation', 'complete_skin_state_validation',
                     'server_authorization_and_consent'],
        'complete_payload': False,
        'deployment_context': 'development_preview',
        'production_enabled': False,
        'authorized_for_storage': False,
    }


def print_mapping(mapping):
    print('\nSKIN STATE MAPPING / candidate')
    patch = mapping['skin_state_patch']
    for field, value in patch.items():
        print(f'  {field}: {value} [pending confirmation]')
    if not patch:
        print('  No supported skin-state patch. No absence inferred.')
    for finding in mapping['findings']:
        issue = finding.get('mapping_issue', finding['issue'])
        print(f"  symptom[{finding['index']}]: {issue}")
    print('  missing_fields: ' + ', '.join(mapping['missing_fields']))
    for blocker in mapping['blockers']:
        print('  blocker: ' + blocker)
    print('  complete_payload=false / authorized_for_storage=false')
