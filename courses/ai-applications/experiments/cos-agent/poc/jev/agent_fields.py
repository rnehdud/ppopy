"""Versioned field inventory for a future agent adapter, never a write grant.

Unimplemented extraction is unassessed, not not_mentioned. Server and tool
fields must never be filled from language model predictions.
"""
from copy import deepcopy


# scope -> field -> (owner, shape/allowed values). These are contract requirements,
# not new Jev questions or claims that the fields have already been extracted.
FIELDS = {
    'request': {
        'intents': ('app', 'list: record,review_routine,ask_question,modify_routine,other'),
        'requested_change': ('app', 'target,operation,value; explicit request only'),
        'priorities': ('app', 'ordered user-reported concerns'),
        'preferences': ('app', 'user-reported preferences'),
        'exclusions': ('app', 'product IDs and user-reported reasons'),
    },
    'context': {
        'actor': ('server', 'authenticated account reference'),
        'authorization': ('server', 'verified resource/action scope'),
        'consent': ('server', 'purpose,version,status,verified_at'),
        'request_id': ('server', 'idempotency reference'),
        'conversation_revision': ('server', 'session and expected revision'),
        'received_at': ('server', 'timezone-aware timestamp'),
        'timezone': ('app', 'validated IANA timezone; never inferred from language'),
        'input_provenance': ('app', 'text/STT,source revision,STT model if applicable'),
        'extraction_provenance': ('tool', 'actual model,question/rule version,errors'),
    },
    'product': {
        'identity': ('tool', 'product_id,product_version,match_status,source_revision'),
        'ownership': ('app', 'owned,not_owned,unknown,declined'),
        'confirmation': ('app', 'status,confirmed_at,confirmed_revision'),
        'label_instructions': ('tool', 'reviewed instructions,evidence_id,version'),
    },
    'usage_event': {
        'product_reference': ('app', 'resolved mention_id and verified product version'),
        'state': ('extractor', 'affirmed,denied,planned,hypothetical,conflict,unknown,declined,not_mentioned'),
        'subject': ('extractor', 'self,other,unknown'),
        'occurred_at': ('app', 'raw date/time,normalized interval,precision,reference timestamp,timezone'),
        'frequency': ('app', 'count,period,unit; actual versus planned'),
        'amount': ('app', 'value,unit; no inferred concentration'),
        'body_site': ('app', 'explicitly reported anatomical site'),
        'sequence': ('app', 'event references and before/after relation'),
        'correction': ('app', 'current,superseded,unknown; replaces_event_id'),
        'confirmation': ('app', 'status,confirmed_at,confirmed_revision'),
    },
    'symptom': {
        'body_site': ('app', 'explicitly reported anatomical site'),
        'observed_at': ('app', 'observation date/time; separate from onset and recognition'),
        'recognition_date': ('app', 'date first noticed; not onset date'),
        'duration': ('app', 'value,unit or bounded interval'),
        'course': ('app', 'user-reported improving,worsening,unchanged,unknown'),
        'product_association': ('app', 'event reference,user-reported temporal association; not causality'),
        'correction': ('app', 'current,superseded,unknown; replaces_symptom_id'),
        'confirmation': ('app', 'status,confirmed_at,confirmed_revision'),
    },
    'decision': {
        'kb_review': ('tool', 'KB/rule/input revisions,reviewed evidence IDs,missing information'),
        'next_action': ('tool', 'ask_user,retrieve_evidence,hold,draft,no_action'),
        'draft_approval': ('server', 'draft hash,input revision,approval scope,expiry'),
        'delivery': ('server', 'authorized device,command ID,expiry,receipt/display acknowledgement'),
    },
}


def _pending(scope):
    return {name: {'value': None, 'evidence_status': 'unassessed',
                   'owner': owner, 'shape': shape}
            for name, (owner, shape) in FIELDS[scope].items()}


def build_agent_fields(result):
    """Lossless candidate handoff; absent event splitting stays explicitly pending.

    This inventory intentionally does not promote representative product times to
    events. In particular, two times with opposite polarity need separate reports.
    """
    return {
        'schema_version': 'agent-fields-0.1',
        'deployment_context': 'development_preview',
        'production_enabled': False,
        'readiness': 'incomplete',
        'request': _pending('request'),
        'context': _pending('context'),
        'products': [
            {'mention_id': p['mention_id'], 'fields': _pending('product')}
            for p in result['products']],
        'usage_event_candidates': deepcopy(result.get('usage_events', [])),
        'event_field_requirements': _pending('usage_event'),
        'event_extraction_status': result.get('event_extraction_status', 'partial_rules_only'),
        'symptoms': [
            {'symptom_id': s['symptom_id'], 'fields': _pending('symptom')}
            for s in result['symptoms']],
        'decision': _pending('decision'),
        'supported_symptoms': ['dryness', 'breakout', 'redness', 'stinging', 'itching'],
        'unsupported_symptoms_status': 'unassessed',
        'write_authorized': False,
    }
