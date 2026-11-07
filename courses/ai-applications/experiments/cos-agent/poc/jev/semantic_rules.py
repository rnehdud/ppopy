"""Conservative source-grounded rules; preserve replaced model predictions."""
import re

try:
    from .segmenter import lexicon_hits, anchor_negated, interrogative
except ImportError:
    from segmenter import lexicon_hits, anchor_negated, interrogative


def set_rule(record, field, value, method, uncertain=False):
    previous = record['relations'].get(field)
    if previous and previous.get('status') == 'unassessed':
        return
    record['relations'][field] = {'value': value, 'score': None,
        'status': 'uncertain' if uncertain else 'rule_candidate', 'method': method,
        'model_prediction': previous}


def symptom_scopes(text, clauses, patterns):
    for clause in clauses:
        for name in lexicon_hits(text, clause, patterns):
            yield name, clause


def apply_rules(result, patterns, clauses, time_spans):
    text = result['source_text']
    result['usage_events'] = []
    refusal = re.search(r'피부\s*증상.{0,12}(?:말하고\s*싶지\s*않|말하기\s*싫|답변.{0,4}거절)', text)
    result['intake_status'] = {'symptoms': {'value': 'declined' if refusal else 'not_assessed',
        'method': 'explicit_global_refusal' if refusal else None,
        'evidence': {'text': refusal[0], 'start': refusal.start(), 'end': refusal.end()} if refusal else None}}
    for product in result['products']:
        product['identification_status'] = 'unverified'
        tail = text[product['end']:]
        category = re.match(r'\s+(크림|로션|토너|스킨|세럼|앰플|클렌저|선크림)(?=[은는을를과와이]|\s|[,.!?]|$)', tail)
        if category:
            product['name_model_prediction'] = {k: product[k] for k in ('text', 'value', 'start', 'end')}
            product['end'] += category.end()
            product['text'] = text[product['start']:product['end']]
            product['value'] = ' '.join(product['text'].split())
            product['identification_status'] = 'incomplete'
            product['name_rule'] = 'preserve_adjacent_category'
        if len(result['products']) == 1 and re.search(r'(?:정확한\s*)?제품명.{0,12}(?:모르|몰라)', text):
            product['identification_status'] = 'incomplete'
        if len(result['products']) == 1 and re.search(r'(?:몇\s*시|언제(?!부터)).{0,16}(?:기억\s*안|모르|몰라)', text):
            set_rule(product, 'usage_time', 'unknown', 'explicit_usage_time_unknown')
        if product['identification_status'] == 'incomplete':
            result['clarifications'].append({'target': product['mention_id'], 'field': 'product_name', 'reason': 'incomplete_name'})

        # Only split explicit date+time pairs in a clause naming this product alone.
        context = next((c for c in clauses if c['start'] <= product['start'] < c['end']), None)
        if not context:
            continue
        peers = [p for p in result['products'] if context['start'] <= p['start'] < context['end']]
        dates = time_spans(context['text'], True)
        pairs = []
        for i, date in enumerate(dates):
            stop = dates[i + 1]['start'] if i + 1 < len(dates) else len(context['text'])
            times = time_spans(context['text'][date['end']:stop])
            if len(times) == 1:
                clock = times[0]
                pairs.append(({'text': date['text'], 'start': context['start'] + date['start'], 'end': context['start'] + date['end']},
                    {'text': clock['text'], 'start': context['start'] + date['end'] + clock['start'],
                     'end': context['start'] + date['end'] + clock['end']}))
        rel = product['relations']
        if len(peers) == 1 and len(pairs) >= 2 and len(pairs) == len(dates) and rel.get('usage_state', {}).get('value') == 'affirmed':
            for date, clock in pairs:
                result['usage_events'].append({'event_id': f"e{len(result['usage_events'])}",
                    'product_mention_id': product['mention_id'], 'usage_date': date, 'usage_time': clock,
                    'status': 'rule_candidate', 'method': 'explicit_repeated_date_time',
                    'subject': rel.get('subject', {}).get('value', 'unknown')})
            set_rule(product, 'usage_date', 'multiple_events', 'explicit_repeated_date_time')
            set_rule(product, 'usage_time', 'multiple_events', 'explicit_repeated_date_time')

    for symptom in result['symptoms']:
        scope = symptom.get('source_scope')
        if not scope:
            continue
        local = scope['text']
        anchor = patterns[symptom['symptom']]
        negated = anchor_negated(text, scope, anchor)
        if negated is True:
            if not interrogative(text, scope):
                set_rule(symptom, 'state', 'denied', 'explicit_symptom_negation')
                set_rule(symptom, 'evidence', dict(scope), 'scope_negation_evidence')
        elif negated is None:
            negative = re.search(r'(?:' + anchor + r')[^,.!?]{0,10}?(?:지(?:는|도)?\s*않(?:아|았|습니다)|없(?:어|었|습니다))', local)
            if negative and not re.search(r'혹시|만약|까\?|다면|수\s*있', local):
                set_rule(symptom, 'state', 'denied', 'explicit_symptom_negation')
                set_rule(symptom, 'evidence', dict(scope), 'scope_negation_evidence')
        # Restrict local identity rules to an explicit sentence subject.
        if re.match(r'\s*(?:나는|난|저는|전)\s', local):
            set_rule(symptom, 'subject', 'self', 'explicit_scope_subject')
        elif re.match(r'\s*(?:친구|엄마|아빠|동생|언니|형|누나)(?:는|가|도)\s', local):
            set_rule(symptom, 'subject', 'other', 'explicit_scope_subject')
        following = text[scope['end']:]
        next_clause = re.match(r'\s*([^.!?\n]+)', following)
        if next_clause:
            next_text = next_clause[1]
            if re.search(r'언제부터.{0,20}(?:모르|몰라)', next_text):
                for field in ('onset_date', 'onset_time'):
                    set_rule(symptom, field, 'unknown', 'explicit_following_onset_unknown')
            if re.search(r'(?:얼마나\s*심한지|심한지|강도.{0,6}|정도.{0,6}).{0,16}(?:모르|몰라)', next_text):
                set_rule(symptom, 'severity', 'unknown', 'explicit_following_severity_unknown')
        recognition = symptom['relations'].get('recognition_time', {})
        if isinstance(recognition.get('value'), dict) and not re.search(r'일어나|알아|발견|느꼈|느끼|확인|눈떴', local):
            set_rule(symptom, 'recognition_time', 'unknown', 'no_local_recognition_anchor', uncertain=True)
