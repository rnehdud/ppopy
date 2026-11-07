"""Single TypeSafe Jev call path; validation matches the earlier inline copies."""
import httpx

ENDPOINT = 'https://api.typesafe.ai/v1/systemone'


def ask(text, questions, key, timeout=60.0):
    """Return validated `answers` for `questions`; raises httpx.HTTPError/ValueError/KeyError.

    `httpx.post` is looked up at call time so tests and benchmark tracing can patch it.
    """
    response = httpx.post(ENDPOINT, headers={'Authorization': f'Bearer {key}'},
                          json={'model': 'jev-latest', 'state': text, 'questions': questions}, timeout=timeout)
    response.raise_for_status()
    answers = response.json()['answers']
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise ValueError('응답 질문 불일치')
    return answers
