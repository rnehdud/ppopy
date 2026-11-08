"""App-facing, backend-contract-first handoff. No network, credentials or storage.

UI confirmation binding is a consistency check, never server authentication.
The actual server must revalidate the contract, session, consent and permissions.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import re

from .candidates import map_candidates
from .review import CONTRACT, TOP, validate_snapshot

MAX_PLAINTEXT_BYTES = 4096
SUPPORTED_BACKEND_VERSION = '1.0.0'


def normalize_payload(value):
    if CONTRACT['version'] != SUPPORTED_BACKEND_VERSION:
        return None, ['unsupported_backend_contract']
    errors = validate_snapshot(value)
    if errors:
        return None, errors
    payload = deepcopy(value)
    payload['observed_at'] = datetime.fromisoformat(value['observed_at'].replace('Z', '+00:00')).astimezone(
        timezone.utc).isoformat().replace('+00:00', 'Z')
    encoded = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if len(encoded) > MAX_PLAINTEXT_BYTES:
        return None, ['payload_too_large']
    return payload, []


def payload_digest(payload):
    """UI binding hash, distinct from any backend record/consent reference."""
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def prepare_handoff(features, confirmed_state=None, confirmation=None):
    mapping = map_candidates(features)
    patch = mapping['skin_state_patch']
    revision = features.get('text_revision')
    valid_revision = isinstance(revision, str) and re.fullmatch('[0-9a-f]{64}', revision) is not None
    if 'source_text' in features:
        text = features['source_text']
        valid_revision = valid_revision and isinstance(text, str) and hashlib.sha256(text.encode('utf-8')).hexdigest() == revision
    questions = []
    for field in ('kind', 'observed_at', *CONTRACT['fields']):
        if field not in patch:
            questions.append({'field': field, 'reason': 'explicit_app_input_required',
                'allowed_values': CONTRACT['record_kinds'] if field == 'kind' else
                    CONTRACT['fields'].get(field),
                'format': 'ISO-8601 UTC observation time' if field == 'observed_at' else None})
    extensions = []
    for finding in mapping['findings']:
        if finding.get('issue') == 'no_direct_target_review_required':
            extensions.append('distinct_concern_types')
        if finding.get('no_direct_skin_state_field'):
            extensions.append('symptom_observation_details')
    if features.get('usage_events'):
        extensions.append('product_usage_events')
    blockers = list(mapping['blockers'])
    if not valid_revision:
        blockers.append('source_revision_invalid_or_missing')
    result = {
        'schema_version': 'backend-handoff-0.1',
        'backend_contract_version': CONTRACT['version'],
        'status': 'needs_information',
        'candidate_skin_state': deepcopy(patch),
        'payload': None,
        'confirmation_binding': None,
        'questions': questions,
        'extension_proposals': list(dict.fromkeys(extensions)),
        'errors': blockers,
        'deployment_context': 'development_preview',
        'production_enabled': False,
        'backend_route_enabled': False,
        'authorized_for_storage': False,
    }
    if blockers:
        result['status'] = 'blocked'
        return result
    if confirmed_state is None:
        return result
    payload, errors = normalize_payload(confirmed_state)
    if errors:
        result.update(status='invalid_input', errors=errors)
        return result
    binding = {'source_text_revision': revision, 'payload_sha256': payload_digest(payload),
               'contract_sha256': payload_digest(CONTRACT)}
    result['confirmation_binding'] = binding
    result['questions'] = []
    if not isinstance(confirmation, dict) or confirmation.get('confirmed') is not True:
        result['status'] = 'needs_confirmation'
        return result
    if any(confirmation.get(key) != value for key, value in binding.items()):
        result.update(status='blocked', errors=['confirmation_revision_or_payload_mismatch'])
        return result
    # Only the nine backend contract keys enter payload. Extraction, event and
    # review data stay in the local engine; no user/session IDs are invented.
    assert set(payload) == TOP
    result.update(status='prepared_disabled', payload=payload)
    return result
