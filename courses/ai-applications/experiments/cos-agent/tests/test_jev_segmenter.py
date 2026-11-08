from poc.jev import segmenter as s
from poc.jev import relations as r
from poc.jev import semantic_rules as sr


def test_segmenter_available():
    assert s.available() is True
    assert s.segmentation_method() == 'kiwi_morpheme'


def test_e16_dryness_affirmed_itching_denied_offline():
    text = '건조하지만 가렵지는 않아.'
    units = s.units(text)
    assert len(units) == 2
    assert units[0]['text'] == '건조하지만'
    assert units[1]['text'] == '가렵지는 않아.'

    # Check anchor negation per unit
    assert s.anchor_negated(text, units[0], r.SYMPTOM_ANCHORS['dryness']) is False
    assert s.anchor_negated(text, units[1], r.SYMPTOM_ANCHORS['itching']) is True


def test_e34_noun_candidates_without_spaces():
    text = 'A로션썼어 피부건조해'
    units = s.units(text)
    cands = s.noun_candidates(text, units[0])
    cand_texts = {c['text'] for c in cands}
    assert 'A로션' in cand_texts
    assert 'A로션썼어' not in cand_texts


def test_e35_particles_and_endings_stripped():
    text = '어.. A로션은요 어제 밤에 발랐구요 ㅠㅠ 피부가 좀 가려워요'
    units = s.units(text)
    # Finding the unit containing A로션
    unit_product = next(u for u in units if 'A로션' in u['text'])
    cands = s.noun_candidates(text, unit_product)
    cand_texts = {c['text'] for c in cands}
    assert 'A로션' in cand_texts
    assert 'A로션은요' not in cand_texts


def test_e33_ssirago_does_not_trigger_stinging():
    text = '친구가 A로션을 쓰라고 권했지만 나는 아직 안 썼어.'
    units = s.units(text)
    hits = []
    for u in units:
        hits.extend(s.lexicon_hits(text, u, r.SYMPTOM_ANCHORS))
    assert 'stinging' not in hits


def test_stt_noisy_inputs_preserve_units():
    # Sentences without punctuation
    text1 = '피부가 가려워 얼마나 심한지는 모르겠어'
    u1 = s.units(text1)
    assert len(u1) == 2

    text2 = '피부가 건조해 언제부터인지는 모르겠어'
    u2 = s.units(text2)
    assert len(u2) == 2


def test_e09_discourse_correction():
    text = 'A로션을 썼다고 했는데 잘못 말했어. 실제로는 B크림만 썼어.'
    p1 = {'text': 'A로션', 'start': 0, 'end': 4, 'value': 'A로션', 'score': 0.9, 'mention_id': 'p0',
          'relations': {'correction': {'value': 'current', 'score': 0.8, 'status': 'candidate'},
                        'usage_state': {'value': 'affirmed', 'score': 0.8, 'status': 'candidate'},
                        'subject': {'value': 'self', 'score': 0.8, 'status': 'candidate'}}}
    p2 = {'text': 'B크림', 'start': 26, 'end': 30, 'value': 'B크림', 'score': 0.9, 'mention_id': 'p1',
          'relations': {'correction': {'value': 'superseded', 'score': 0.8, 'status': 'candidate'},
                        'usage_state': {'value': 'affirmed', 'score': 0.8, 'status': 'candidate'},
                        'subject': {'value': 'self', 'score': 0.8, 'status': 'candidate'}}}
    result = {'source_text': text, 'products': [p1, p2], 'symptoms': [], 'clarifications': []}
    r.finalize(result)
    assert p1['relations']['correction']['value'] == 'superseded'
    assert p2['relations']['correction']['value'] == 'current'
    assert p2['eligible_for_usage_candidate'] is True


def test_compound_product_containing_stop_noun():
    text = '노스카나인 트러블 세럼을 썼어'
    units = s.units(text)
    cands = s.noun_candidates(text, units[0])
    cand_texts = {c['text'] for c in cands}
    assert '노스카나인 트러블 세럼' in cand_texts
    assert '트러블' not in cand_texts


def test_cosmetic_user_words_registered():
    text = '클렌징밤과 선세럼을 쓰고 수딩젤을 발랐어'
    toks = [t.form for t in s.tokens(text)]
    assert '클렌징밤' in toks
    assert '선세럼' in toks
    assert '수딩젤' in toks


def test_cause_connective_endings_split():
    text = '아침에 일어나니까 건조해'
    units = s.units(text)
    assert len(units) == 2
    assert units[0]['text'] == '아침에 일어나니까'
    assert units[1]['text'] == '건조해'
