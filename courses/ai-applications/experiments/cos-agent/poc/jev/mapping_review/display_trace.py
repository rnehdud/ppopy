"""Source-to-field trace for local synthetic tests. Never changes mapping data."""
import textwrap


def _line(value, indent='  '):
    for line in textwrap.wrap(str(value), width=88, initial_indent=indent,
                              subsequent_indent=indent + '  ', break_long_words=False,
                              break_on_hyphens=False) or [indent]:
        print(line)


def _source(features, span):
    text = features.get('source_text', '')
    if isinstance(span, dict):
        start, end = span.get('start'), span.get('end')
        if (type(start) is int and type(end) is int and 0 <= start < end <= len(text)
                and text[start:end] == span.get('text')):
            return f"{text[start:end]!r} [{start}:{end}]"
    return 'unavailable (no verified source span)'


def _value(value):
    if isinstance(value, dict):
        return repr(value.get('text', 'unavailable'))
    return 'unassessed' if value is None else str(value)


def _origin(relation):
    status = relation.get('status', 'unassessed')
    if status == 'unassessed':
        return 'unassessed'
    score = relation.get('score')
    score_text = f', score={score:.2f}' if type(score) in (int, float) else ''
    if relation.get('method'):
        return f"rule:{relation['method']}, {status}"
    return f'Jev, {status}{score_text}'


def _relations(record, prefix, keys):
    for key in keys:
        relation = record.get('relations', {}).get(key)
        if not isinstance(relation, dict):
            continue
        _line(f"-> {prefix}.{key} = {_value(relation.get('value'))} [{_origin(relation)}]", '    ')
        previous = relation.get('model_prediction')
        if isinstance(previous, dict):
            _line(f"Before rule: {_value(previous.get('value'))} [{_origin(previous)}]", '       ')


def print_handoff(handoff, features):
    print('\n' + '=' * 88)
    print('SOURCE -> JEV FIELDS -> BACKEND MAPPING')
    print('=' * 88)
    confirmation = 'UI confirmation matched' if handoff.get('payload') is not None else 'User confirmation required'
    _line(f"Status: {handoff['status']} | {confirmation} | Storage disabled")
    print('\nSYMPTOMS')
    symptoms = features.get('symptoms', [])
    mapping = features.get('skin_state_mapping', {})
    candidates = mapping.get('candidates', [])
    findings = {f['index']: f for f in mapping.get('findings', [])}
    if not symptoms:
        _line('No supported symptom mentions detected. This does not establish absence.')
    for index, symptom in enumerate(symptoms):
        print(f'\n  [{symptom.get("symptom_id", index)}] {symptom.get("symptom", "unknown")}')
        _line('Context (semantic unit): ' + _source(features, symptom.get('source_scope')))
        _line('Symptom type: lexicon-gated detection, not a Jev field assignment.')
        evidence = symptom.get('relations', {}).get('evidence', {})
        if isinstance(evidence.get('value'), dict):
            _line(f"Selected evidence [{_origin(evidence)}]: " + _source(features, evidence['value']))
        _relations(symptom, f'symptoms[{index}]',
                   ('state', 'subject', 'severity', 'onset_date', 'onset_time', 'recognition_time'))
        matched = [c for c in candidates if c['symptom_index'] == index]
        for candidate in matched:
            _line(f"=> backend.{candidate['field']} += {candidate['value']} [adapter; pending confirmation]", '    ')
        if not matched:
            finding = findings.get(index, {})
            reason = finding.get('mapping_issue', finding.get('issue', 'no_eligible_mapping'))
            _line(f'=> backend: NOT MAPPED ({reason})', '    ')
    print('\nPRODUCT MENTIONS')
    products = features.get('products', [])
    if not products:
        _line('No specific product names extracted.')
    for index, product in enumerate(products):
        _line(f"[{product.get('mention_id', index)}] Source: " + _source(features, product))
        name_rule = product.get('name_rule')
        origin = f'rule:{name_rule}' if name_rule else f"Jev name selection; score={product.get('score')}"
        _line(f"-> products[{index}].value = {product.get('value')!r} [{origin}]", '    ')
        if name_rule and product.get('name_model_prediction'):
            _line(f"Before rule: {product['name_model_prediction'].get('value')!r} [Jev name selection]", '       ')
    print('\nUSAGE EVENTS (separate from skin_state)')
    events = features.get('usage_events', [])
    if not events:
        _line('No supported usage events detected.')
    for index, event in enumerate(events):
        _line(f"[{event.get('event_id', index)}] product={event.get('product_mention_id')} | Context: "
              + _source(features, event.get('source_scope')))
        _relations(event, f'usage_events[{index}]',
                   ('product_link', 'usage_state', 'subject', 'correction', 'usage_date', 'usage_time'))
        _line('=> backend.skin_state: NOT MAPPED (separate usage-event contract required)', '    ')
    print('\nBACKEND PAYLOAD (transmission disabled)' if handoff.get('payload') is not None else '\nBACKEND CANDIDATE')
    state = handoff.get('payload') or handoff['candidate_skin_state']
    if not state:
        _line('No field values proposed. No absence inferred.')
    for field, value in state.items():
        rendered = ', '.join(map(str, value)) if isinstance(value, list) else str(value)
        _line(f'{field} = {rendered}')
    if handoff['candidate_skin_state'].get('discomfort_presence') == 'reported':
        _line('discomfort_presence=reported is derived by the adapter from eligible symptom candidates; not a separate Jev answer.')
    if handoff['questions']:
        print('\nREQUIRES APP INPUT')
        _line(', '.join(q['field'] for q in handoff['questions']))
    if handoff['extension_proposals']:
        print('\nBACKEND EXTENSION PROPOSALS')
        _line(', '.join(handoff['extension_proposals']))
    if handoff['errors']:
        print('\nREVIEW REQUIRED')
        for error in handoff['errors']:
            _line(error)
    print('\nSource excerpts are context or selected evidence, not model token attribution.')
    print('App JSON: --app-json | Internal JSON: --json | Full debug: --verbose')
    print('=' * 88)
