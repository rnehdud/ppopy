import json
from pathlib import Path
import pytest

from poc.jev import skin_state as s
from poc.jev import test_jev_text as cli
from poc.jev.mapping_review.backend import prepare_handoff


def mock_response(monkeypatch, overrides=None, low_evidence=False):
    def ask(text, questions, key):
        selections = {'discomfort_presence': 'reported', 'discomfort_types': 'set5', **(overrides or {})}
        result = {}
        for qid, q in questions.items():
            field = qid
            field = field.split('.', 1)[1] if field.startswith('c') and '.' in field else field
            choice = 's0' if field.startswith('evidence.') else selections.get(field, 'omit')
            score = .4 if low_evidence else .95
            result[qid] = {'type': 'choice', 'choice': choice, 'probabilities': {choice: score}}
        return result
    monkeypatch.setattr(s, 'ask', ask)


def test_jev_questions_are_backend_fields_and_array_values_are_contract_subsets():
    chunk = s.chunk_text('나는 따갑고 가려워.')[0]
    questions, options = s.build_questions(chunk)
    assert set(questions) == set(s.CONTRACT['fields'])
    for field, values in options.items():
        if field == 'discomfort_types':
            assert len(values) == 128
            assert all(set(v) <= set(s.CONTRACT['fields'][field]) for v in values.values())
        else:
            assert set(values.values()) == set(s.CONTRACT['fields'][field])
    assert not {'severity', 'usage_state', 'skin_condition', 'subject'} & set(questions)


def test_direct_backend_values_without_legacy_intermediate_fields(monkeypatch):
    mock_response(monkeypatch)
    result = s.extract_skin_state('나는 따갑고 가려워.', 'synthetic')
    assert result['candidate_skin_state'] == {'discomfort_presence': 'reported', 'discomfort_types': ['stinging', 'itching']}
    assert 'symptoms' not in result and 'products' not in result and 'usage_events' not in result
    assert prepare_handoff(result)['candidate_skin_state'] == result['candidate_skin_state']


def test_silence_is_omitted_not_fabricated_missing_state(monkeypatch):
    mock_response(monkeypatch, {'discomfort_presence': 'omit', 'discomfort_types': 'omit'})
    result = s.extract_skin_state('A로션을 썼어.', 'synthetic')
    assert result['candidate_skin_state'] == {}
    assert set(s.CONTRACT['fields']) <= {q['field'] for q in prepare_handoff(result)['questions']}


@pytest.mark.parametrize('state', ['unknown', 'not_asked', 'user_refused'])
def test_explicit_backend_missing_values_preserved(monkeypatch, state):
    mock_response(monkeypatch, {'sensitivity_history': state})
    assert s.extract_skin_state('민감 반응 이력에 대한 합성 답변.', 'synthetic')['candidate_skin_state']['sensitivity_history'] == state


def test_low_chunk_field_score_is_withheld(monkeypatch):
    mock_response(monkeypatch, low_evidence=True)
    assert s.extract_skin_state('나는 따가워.', 'synthetic')['candidate_skin_state'] == {}


def test_cross_field_conflict_blocks_handoff(monkeypatch):
    mock_response(monkeypatch, {'discomfort_presence': 'none_reported'})
    result = s.extract_skin_state('합성 충돌 보고.', 'synthetic')
    assert result['candidate_skin_state'] == {}
    assert result['warnings']
    assert prepare_handoff(result)['status'] == 'blocked'


def test_api_failure_cannot_create_backend_values(monkeypatch):
    def fail(*a, **kw):
        raise s.httpx.ConnectError('offline')
    monkeypatch.setattr(s, 'ask', fail)
    result = s.extract_skin_state('합성 입력.', 'synthetic')
    assert result['warnings'] and not result['candidate_skin_state']


def test_default_cli_never_calls_legacy_extractors(monkeypatch, capsys):
    mock_response(monkeypatch)
    def forbidden(*a, **kw):
        raise AssertionError('legacy path executed')
    monkeypatch.setattr(cli, 'classify', forbidden)
    monkeypatch.setattr(cli, 'extract_features', forbidden)
    assert cli.run_input('나는 따가워.', 'synthetic', {}, as_json=True) == 0
    result = json.loads(capsys.readouterr().out)
    assert result['schema_version'] == 'skin-state-extraction-1.2'
    assert set(result['candidate_skin_state']) <= set(s.CONTRACT['fields'])


@pytest.mark.parametrize('text', ['', ' ' , 'x' * 2001])
def test_input_limit(text):
    with pytest.raises(ValueError):
        s.extract_skin_state(text, 'synthetic')


def test_interactive_default_does_not_load_old_field_configuration(monkeypatch):
    monkeypatch.setattr('sys.argv', ['test_jev_text.py'])
    monkeypatch.setattr(cli, 'CONFIG', Path('nonexistent-legacy-configuration.json'))
    monkeypatch.setattr(cli, 'get_api_key', lambda: 'synthetic')
    lines = iter(['synthetic input', '/quit'])
    monkeypatch.setattr('builtins.input', lambda *a: next(lines))
    calls = []
    monkeypatch.setattr(cli, 'run_input', lambda text, key, config, **kw: calls.append((config, kw)))
    assert cli.main() == 0
    assert calls[0][0] == {} and calls[0][1]['legacy'] is False


def test_direct_candidate_version_must_match_backend(monkeypatch):
    mock_response(monkeypatch)
    result = s.extract_skin_state('나는 따가워.', 'synthetic')
    result['backend_contract_version'] = 'future'
    with pytest.raises(ValueError, match='version mismatch'):
        prepare_handoff(result)


def test_chunks_are_visible_exact_source_slices_without_kiwi(monkeypatch):
    text = '내가 어제 A클렌저로 이중세안을 하고 B로션을 발랐는데 아침에 일어나니까 건조하고 피부가 가려워'
    monkeypatch.setattr(s, 'units', lambda text: [{'start': 0, 'end': len(text), 'text': text}])
    chunks = s.chunk_text(text)
    assert [c['text'] for c in chunks] == [
        '내가 어제 A클렌저로 이중세안을 하고', 'B로션을 발랐는데',
        '아침에 일어나니까', '건조하고', '피부가 가려워']
    assert all(text[c['start']:c['end']] == c['text'] for c in chunks)


def test_each_chunk_has_its_own_jev_questions_and_unmapped_chunks_are_printed(monkeypatch, capsys):
    def ask(text, questions, key):
        answers = {}
        for qid in questions:
            choice = 'reported' if qid == 'c1.concern_presence' else 'omit'
            answers[qid] = {'type': 'choice', 'choice': choice, 'probabilities': {choice: .95}}
        return answers
    monkeypatch.setattr(s, 'ask', ask)
    result = s.extract_skin_state('로션을 발랐는데 피부가 건조해.', 'synthetic')
    assert result['candidate_skin_state'] == {'concern_presence': 'reported'}
    assert result['assignments'][0]['chunk_id'] == 'c0'
    s.print_skin_state(result, prepare_handoff(result))
    output = capsys.readouterr().out
    assert '[1] 로션을 발랐는데' in output and '[2] 피부가 건조해.' in output
    assert 'No backend field assigned.' in output and 'concern_presence' in output


def test_contradictory_chunk_values_are_not_silently_merged(monkeypatch):
    def ask(text, questions, key):
        answers = {}
        for qid in questions:
            choice = ('reported' if qid.startswith('c0.') else 'none_reported') if qid.endswith('.concern_presence') else 'omit'
            answers[qid] = {'type': 'choice', 'choice': choice, 'probabilities': {choice: .95}}
        return answers
    monkeypatch.setattr(s, 'ask', ask)
    result = s.extract_skin_state('고민이 있지만 고민이 없어.', 'synthetic')
    assert 'concern_presence' not in result['candidate_skin_state']
    assert 'conflicting_chunks:concern_presence' in result['warnings']
