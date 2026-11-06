from poc.jev.benchmark import score_case


def test_missing_product_fails_instead_of_scoring_only_existing_rows():
    checks = score_case({'products': [{'name': 'A로션', 'usage_state': 'affirmed'}]},
                        {'products': [], 'warnings': []})
    assert not all(c['passed'] for c in checks)
    assert next(c for c in checks if c['field'] == 'products[0].usage_state')['actual'] is None


def test_duplicate_matches_are_not_resolved_optimistically():
    product = {'value': 'A로션', 'relations': {'usage_state': {'value': 'affirmed'}}}
    checks = score_case({'products': [{'name': 'A로션', 'usage_state': 'affirmed'}]},
                        {'products': [product, product], 'warnings': []})
    assert next(c for c in checks if c['field'].endswith('unique_match'))['passed'] is False


def test_same_symptom_matches_specified_subject_scope():
    symptoms = [{'symptom': 'stinging', 'source_scope': {'text': text},
                 'relations': {'state': {'value': value}}}
                for text, value in [('친구는 따갑대.', 'affirmed'), ('나는 따갑지 않아.', 'denied')]]
    checks = score_case({'symptoms': [{'type': 'stinging', 'scope_contains': '친구', 'state': 'affirmed'},
                                    {'type': 'stinging', 'scope_contains': '나는', 'state': 'denied'}]},
                        {'symptoms': symptoms, 'warnings': []})
    assert all(c['passed'] for c in checks)
