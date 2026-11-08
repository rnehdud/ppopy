"""Source-bound event candidates. Model relations remain unconfirmed reports."""
import re


def event_candidates(text, products, scopes, time_spans, limit=32):
    events = []
    for scope in scopes:
        local = [p for p in products if scope['start'] <= p['start'] < scope['end']]
        binding = 'explicit_mention'
        if not local:
            # Carry only a single named product within the same sentence. Never
            # guess which of multiple products an omitted name refers to.
            start = max((m.end() for m in re.finditer(r'[.!?。！？\n]', text[:scope['start']])), default=0)
            prior = [p for p in products if start <= p['start'] < scope['start']]
            if len({p['value'] for p in prior}) != 1:
                continue
            local = prior[-1:]
            binding = 'omitted_product_candidate'
        # A clock in a symptom-only clause is not a usage event. This lexical
        # candidate gate has known omissions, and is not an absence judgement.
        if not re.search(r'썼|쓰|쓸|사용|발랐|바르|바를|바른|발라|했|할|안\s*발', scope['text']):
            continue
        clocks = [{**s, 'start': scope['start'] + s['start'],
                   'end': scope['start'] + s['end']} for s in time_spans(scope['text'])]
        for product in local:
            for clock in clocks or [None]:
                if len(events) >= limit:
                    return events, '사용 사건 후보 한도 도달 · 추가 사건은 미평가'
                events.append({'event_id': f'e{len(events)}',
                    'product_mention_id': product['mention_id'],
                    'source_scope': {k: scope[k] for k in ('start', 'end', 'text')},
                    'time_anchor': clock, 'binding_method': binding, 'relations': {},
                    'status': 'candidate', 'confirmation_status': 'pending',
                    'eligible_for_usage_candidate': False})
    return events, None


def finish_events(result, candidates):
    products = {p['mention_id']: p for p in result['products']}
    events = []
    for event in candidates:
        rel = event['relations']
        if any(rel.get(k, {}).get('value') == v and rel[k].get('status') == 'candidate'
               for k, v in [('product_link', 'unlinked'), ('usage_state', 'not_mentioned')]):
            continue
        product = products[event['product_mention_id']]
        # A cancelled mention cannot become an active event, even if its local
        # model answer missed a correction in the surrounding discourse.
        correction = product['relations'].get('correction', {})
        if correction.get('value') == 'superseded':
            rel['correction'] = {**correction}
        event['eligible_for_usage_candidate'] = (
            product['score'] > .5 and product.get('identification_status') != 'incomplete'
            and all(rel.get(k, {}).get('value') == v
                    and rel[k].get('status') in ('candidate', 'rule_candidate')
                    for k, v in [('product_link', 'linked'), ('usage_state', 'affirmed'),
                                 ('subject', 'self'), ('correction', 'current')]))
        for k, relation in rel.items():
            if relation.get('status') in ('uncertain', 'unassessed') or relation.get('value') in ('unknown', 'conflict'):
                result['clarifications'].append({'target': event['event_id'], 'field': k,
                                                  'reason': relation['status']})
        # Compatibility time fields contain raw spans or explicit missing states,
        # never fabricated timestamps. State/subject remain event-specific.
        for k in ('usage_date', 'usage_time'):
            event[k] = rel.get(k, {}).get('value')
        events.append(event)
    result['usage_events'] = events
    result['event_extraction_status'] = 'unit_time_candidates'
    for product in products.values():
        attached = [e for e in events if e['product_mention_id'] == product['mention_id']]
        if len(attached) > 1:
            product['usage_event_summary'] = 'multiple_event_candidates'
            # The old single-mention eligibility must not authorize a mixed event
            # aggregate. Consumers should inspect each event instead.
            product['eligible_for_usage_candidate'] = False
