"""Run a frozen synthetic evaluation; never tunes extraction during a run.

Usage: python -m poc.jev.benchmark
"""
import hashlib
import json
import platform
import statistics
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

from .relations import extract_features
from .test_jev_text import get_api_key

ROOT = Path(__file__).resolve().parent


def scalar(value):
    return value.get('text') if isinstance(value, dict) else value


def score_case(expected, actual):
    checks = []
    def check(field, want, got):
        checks.append({'field': field, 'expected': want, 'actual': got, 'passed': want == got})
    for kind, identity in [('products', 'name'), ('symptoms', 'type')]:
        if kind not in expected:
            continue
        rows = actual.get(kind, [])
        check(kind + '.count', len(expected[kind]), len(rows))
        for i, want in enumerate(expected[kind]):
            matches = [row for row in rows if row.get('value' if kind == 'products' else 'symptom') == want[identity]
                       and ('scope_contains' not in want or want['scope_contains'] in row.get('source_scope', {}).get('text', ''))]
            check(f'{kind}[{i}].unique_match', 1, len(matches))
            row = matches[0] if len(matches) == 1 else {}
            for attr, value in want.items():
                if attr in (identity, 'scope_contains'):
                    continue
                if attr == 'eligible':
                    got = row.get('eligible_for_usage_candidate')
                elif attr == 'identification':
                    got = row.get('identification_status')
                else:
                    got = scalar(row.get('relations', {}).get(attr, {}).get('value'))
                check(f'{kind}[{i}].{attr}', value, got)
    if 'intake' in expected:
        check('intake.symptoms', expected['intake'], actual.get('intake_status', {}).get('symptoms', {}).get('value'))
    if 'event_pairs' in expected:
        check('event_pairs', expected['event_pairs'], [[e['usage_date']['text'], e['usage_time']['text']] for e in actual.get('usage_events', [])])
    check('api_warnings', [], actual.get('warnings', []))
    return checks


def main():
    dataset_path = ROOT / 'evaluation_data/diverse-v1.json'
    dataset = json.loads(dataset_path.read_text(encoding='utf-8'))
    key = get_api_key()
    if not key:
        raise SystemExit('API key missing')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = ROOT / 'evaluation_runs' / ('diverse-v1-' + stamp)
    output.mkdir(parents=True)
    files = [ROOT / name for name in ('relations.py', 'semantic_rules.py', 'product_mentions.py',
                                      'context_evidence.py', 'segmenter.py', 'jev_client.py', 'benchmark.py')]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files + [dataset_path]}
    manifest = {'started_at': stamp, 'python': platform.python_version(), 'httpx': httpx.__version__,
        'review_status': dataset['review_status'], 'scope': 'relation_extraction_only_no_STT_or_DB', 'code_and_data_sha256': hashes}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    original_post = httpx.post
    requests = []
    def traced_post(*args, **kwargs):
        started = time.perf_counter()
        metadata = {'questions': len(kwargs.get('json', {}).get('questions', {}))}
        try:
            response = original_post(*args, **kwargs)
            metadata['http_status'] = response.status_code
            try:
                data = response.json()
                metadata.update(model=data.get('model'), usage=data.get('usage'))
            except ValueError:
                pass
            return response
        finally:
            metadata['elapsed_s'] = time.perf_counter() - started
            requests.append(metadata)
    records = []
    repeats = {'E06', 'E14', 'E16', 'E23', 'E26', 'E34'}
    scheduled = [(case, 1) for case in dataset['cases']] + [(case, 2) for case in dataset['cases'] if case['id'] in repeats]
    httpx.post = traced_post
    try:
        for index, (case, run) in enumerate(scheduled, 1):
            requests.clear()
            started = time.perf_counter()
            try:
                result = extract_features(case['input'], key)
            except Exception as exc:
                result = {'products': [], 'symptoms': [], 'warnings': [type(exc).__name__]}
            checks = score_case(case['expected'], result)
            record = {'case': case, 'run': run, 'result': result, 'checks': checks,
                'passed': all(c['passed'] for c in checks), 'elapsed_s': time.perf_counter() - started, 'requests': list(requests)}
            records.append(record)
            (output / f"{case['id']}-r{run}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"{index}/{len(scheduled)} {case['id']} r{run}: {'PASS' if record['passed'] else 'FAIL'} ({record['elapsed_s']:.2f}s)", flush=True)
    finally:
        httpx.post = original_post
    primary = [r for r in records if r['run'] == 1]
    groups = defaultdict(list)
    for record in primary:
        groups[record['case']['group']].append(record)
    timing = sorted(r['elapsed_s'] for r in primary)
    summary = {'cases': len(primary), 'cases_passed': sum(r['passed'] for r in primary),
        'checks': sum(len(r['checks']) for r in primary), 'checks_passed': sum(c['passed'] for r in primary for c in r['checks']),
        'p50_s': statistics.median(timing), 'p95_s_nearest_rank': timing[max(0, int(len(timing) * .95 + .999) - 1)],
        'requests_all_runs': sum(len(r['requests']) for r in records),
        'questions_all_runs': sum(q['questions'] for r in records for q in r['requests']),
        'models': sorted({q['model'] for r in records for q in r['requests'] if q.get('model')}),
        'uncertain_relations_primary': sum(v.get('status') in ('uncertain', 'unassessed') for r in primary
            for row in r['result'].get('products', []) + r['result'].get('symptoms', []) for v in row.get('relations', {}).values()),
        'token_usage_all_runs': {kind: sum((q.get('usage') or {}).get(kind, 0) for r in records for q in r['requests'])
                                 for kind in ('input_tokens', 'output_tokens')},
        'groups': {g: {'passed': sum(r['passed'] for r in rows), 'total': len(rows)} for g, rows in groups.items()}}
    changes = []
    for record in records:
        if record['run'] == 2:
            first = next(r for r in primary if r['case']['id'] == record['case']['id'])
            changed = [a['field'] for a, b in zip(first['checks'], record['checks']) if a['actual'] != b['actual']]
            changes.append({'id': record['case']['id'], 'first_pass': first['passed'], 'second_pass': record['passed'], 'changed_scored_fields': changed})
    summary['repeat_consistency'] = changes
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    manifest['files_unchanged'] = all(hashlib.sha256(p.read_bytes()).hexdigest() == hashes[str(p.relative_to(ROOT))] for p in files + [dataset_path])
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# 다양한 입력 평가', '',
        f"- 핵심 조건 전체 충족: {summary['cases_passed']}/{len(primary)}건. 조건별: {summary['checks_passed']}/{summary['checks']}.",
        '- 사람이 검토하지 않은 합성 기대값 기반 개발 평가. 독립 평가셋·일반 정확도가 아님.',
        '- 조건 전체 충족은 전체 JSON의 Exact Match가 아님. 불확실 후보도 값 일치면 조건 충족으로 계산.',
        '- 실행 중 추출 코드/프롬프트 수정 없음. STT·DB·기존 전체 문장 분류는 측정 범위 밖.', '',
        '| 유형 | 조건 전체 충족 |', '| --- | --- |']
    lines += [f"| {g} | {v['passed']}/{v['total']} |" for g, v in summary['groups'].items()]
    lines += ['', '## 미충족 조건', '']
    for record in primary:
        failed = [c for c in record['checks'] if not c['passed']]
        if failed:
            lines += [f"### {record['case']['id']} · {record['case']['group']}", '', '> ' + record['case']['input'], '', '| 조건 | 기대 | 실제 |', '| --- | --- | --- |']
            lines += [f"| {c['field']} | {c['expected']} | {c['actual']} |" for c in failed]
            lines += ['']
    lines += ['## 성능·반복 결과', '', '```json', json.dumps(summary, ensure_ascii=False, indent=2), '```']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'output': str(output), **summary}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
