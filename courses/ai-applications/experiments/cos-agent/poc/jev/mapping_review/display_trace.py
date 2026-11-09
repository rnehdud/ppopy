"""Compact source / Jev / backend rows for local synthetic tests."""
import textwrap


def _row(label, value):
    prefix = f'   {label:<8} '
    print(textwrap.fill(str(value), width=92, initial_indent=prefix,
                        subsequent_indent=' ' * len(prefix), break_long_words=False,
                        break_on_hyphens=False))


def _source(features, span):
    text = features.get('source_text', '')
    if isinstance(span, dict):
        start, end = span.get('start'), span.get('end')
        if (type(start) is int and type(end) is int and 0 <= start < end <= len(text)
                and text[start:end] == span.get('text')):
            return repr(text[start:end])
    return '[source unavailable]'


def _value(value):
    return str(value.get('text')) if isinstance(value, dict) else str(value)


def _assignments(record, keys):
    jev, rules = [], []
    for key in keys:
        final = record.get('relations', {}).get(key)
        if not isinstance(final, dict):
            continue
        model = final.get('model_prediction') if final.get('method') else final
        if isinstance(model, dict):
            value = model.get('value')
            if model.get('status') == 'unassessed':
                jev.append(f'{key}=unassessed')
            elif value not in (None, 'not_mentioned') and not (key == 'correction' and value == 'current'):
                suffix = ' (?)' if model.get('status') == 'uncertain' else ''
                jev.append(f'{key}={_value(value)}{suffix}')
        if final.get('method') and (not isinstance(model, dict) or final.get('value') != model.get('value')):
            rules.append(f"{key}={_value(final.get('value'))}")
    _row('Jev', ' | '.join(jev) or 'No assessed values')
    if rules:
        _row('Rule', ' | '.join(rules))


def print_handoff(handoff, features):
    print('\nMAPPING RESULT  /  ' + handoff['status'])
    print('-' * 72)
    mapping = features.get('skin_state_mapping', {})
    candidates = mapping.get('candidates', [])
    findings = {f['index']: f for f in mapping.get('findings', [])}
    number = 0

    def heading(span, category):
        nonlocal number
        number += 1
        print(f'\n{number}. {_source(features, span)}  [{category}]')

    for index, symptom in enumerate(features.get('symptoms', [])):
        heading(symptom.get('source_scope'), 'symptom: ' + symptom.get('symptom', 'unknown'))
        _assignments(symptom, ('state', 'subject', 'severity', 'onset_date', 'onset_time', 'recognition_time'))
        matched = [c for c in candidates if c['symptom_index'] == index]
        if matched:
            _row('Backend', ' | '.join(f"{c['field']}={c['value']}" for c in matched))
        else:
            finding = findings.get(index, {})
            reason = finding.get('mapping_issue', finding.get('issue', ''))
            if reason == 'no_direct_target_review_required':
                reason = 'No matching backend field'
            elif reason == 'not_a_confirmed_positive_do_not_map_as_present':
                reason = 'Not a positive self-report'
            elif reason == 'opposed_reports_require_time_and_state_confirmation':
                reason = 'Conflicting reports; confirm time and state'
            else:
                reason = 'Pending review'
            _row('Backend', 'Not mapped - ' + reason)
    products = {p['mention_id']: p for p in features.get('products', [])}
    events = features.get('usage_events', [])
    for event in events:
        product = products.get(event.get('product_mention_id'), {})
        heading(event.get('source_scope'), 'product: ' + str(product.get('value', 'unknown')))
        _assignments(event, ('usage_state', 'subject', 'usage_date', 'usage_time', 'correction'))
        link = event.get('relations', {}).get('product_link', {})
        if link.get('value') != 'linked' or link.get('status') in ('uncertain', 'unassessed'):
            _row('Link', 'Product reference needs review')
        _row('Backend', 'Not mapped - separate usage-event contract needed')
    attached = {e.get('product_mention_id') for e in events}
    for mention_id, product in products.items():
        if mention_id in attached:
            continue
        heading(product, 'product mention')
        previous = product.get('name_model_prediction')
        model_value = previous.get('value') if isinstance(previous, dict) else product.get('value')
        _row('Jev', f'product_name={model_value}')
        if product.get('name_rule'):
            _row('Rule', f"product_name={product.get('value')}")
        _row('Backend', 'Product identification required')
    if not number:
        print('\nNo supported mentions detected; absence is not established.')
    print('\n' + '-' * 72)
    if handoff['candidate_skin_state'].get('discomfort_presence') == 'reported':
        _row('Derived', 'discomfort_presence=reported (adapter)')
    if handoff['questions']:
        _row('Missing', ', '.join(q['field'] for q in handoff['questions']))
    for error in handoff['errors']:
        _row('Review', error)
    if handoff.get('payload') is not None:
        _row('Payload', 'Validated; transmission disabled. See --app-json.')
    confirmation = 'UI confirmation matched.' if handoff.get('payload') is not None else 'Pending user confirmation.'
    print(confirmation + ' Storage disabled. Details: --app-json / --verbose')
