"""Summarize measured, paired frozen-holdout runs; never modify their labels."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def metrics(report):
    turns = [t for c in report['results'] for t in c['turns']]
    times = sorted(t['result']['seconds'] for t in turns if 'seconds' in t['result'])
    fields = {}
    for field in turns[0]['expected_state']:
        fields[field] = sum(t['result']['state'][field] == t['expected_state'][field] for t in turns)
    category = defaultdict(lambda: {'passed': 0, 'total': 0})
    for c in report['results']:
        category[c['category']]['total'] += 1
        category[c['category']]['passed'] += int(c['passed'])
    return {**{k: v for k, v in report.items() if k != 'results'},
            'field_exact_hits': fields,
            'completed_turns': sum(t['checks']['completed'] for t in turns),
            'category': dict(category),
            'failed_checks': dict(Counter(k for t in turns for k, v in t['checks'].items() if not v)),
            'completed_turn_latency': {'n': len(times), 'mean_seconds': statistics.mean(times) if times else None,
                                      'p95_seconds': times[math.ceil(len(times)*0.95)-1] if times else None},
            'latency_note': 'Only turns carrying seconds; early runtime failures have no recorded total seconds.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-name', default='qlora-smoke-v3')
    args = parser.parse_args()
    before = read('output/training/gguf-holdout-before/results.json')
    after = read('output/training/gguf-holdout-after/results.json')
    bm = read('output/training/gguf-holdout-before/metadata.json')
    am = read('output/training/gguf-holdout-after/metadata.json')
    keys = ['model_manifest', 'holdout_sha256', 'system', 'tools', 'generation', 'runtime_sha256', 'evaluation_sha256']
    for key in keys:
        if bm[key] != am[key]:
            raise ValueError('Non-comparable evaluation metadata: ' + key)
    for key in ['engine', 'context', 'model', 'port']:
        if bm['server'][key] != am['server'][key]:
            raise ValueError('Different server setting: ' + key)
    train = read(f'output/training/{args.run_name}/comparison.json')
    if not train['adapter_weights_changed'] or not train['adapter_reload_probe_equal']:
        raise ValueError('Missing actual training / reload evidence')
    ids_before = {c['id']: c for c in before['results']}
    ids_after = {c['id']: c for c in after['results']}
    if ids_before.keys() != ids_after.keys():
        raise ValueError('Different scenarios')
    paired = Counter(('pass' if ids_before[k]['passed'] else 'fail') + '_to_' +
                     ('pass' if ids_after[k]['passed'] else 'fail') for k in ids_before)
    failures = []
    seen = set()
    for case in after['results']:
        if case['passed'] or case['category'] in seen:
            continue
        seen.add(case['category'])
        t = next(t for t in case['turns'] if not t['passed'])
        failures.append({'id': case['id'], 'category': case['category'], 'input': t['input'],
                         'failed_checks': [k for k, v in t['checks'].items() if not v],
                         'expected_state': t['expected_state'], 'actual_state': t['result']['state'],
                         'error': t['result'].get('error'), 'answer': t['result'].get('answer', ''),
                         'calls': t['result']['calls']})
    converter_commit = '4c4ca5b18854c973655a62a6164a3ae930ee76b0'
    report = {'training': train, 'before': metrics(before), 'after': metrics(after),
              'paired_scenarios': dict(paired), 'comparable_metadata_verified': keys,
              'adapter_gguf_sha256': am['adapter_sha256'], 'converter_commit': converter_commit,
              'representative_after_failures': failures,
              'limitations': ['Synthetic authored Korean, no independent human semantic audit.',
                              '59 template-disjoint controlled scenarios, not broad or clinical performance.',
                              'One fixed seed, 120 decisions and 60 steps; no checkpoint selection on holdout.',
                              'Adapter trained on NF4; closed-loop before/after both official Q4_K_M GGUF.',
                              'External skincare KB, STT, Jev, real product mapping are not evaluated.']}
    out = ROOT / 'output/stateful_qlora_comparison.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    b, a = report['before'], report['after']
    delta = a['passed_scenarios'] - b['passed_scenarios']
    text = f'''목적

한국어 입력을 받은 Qwen이 외부 세션 상태를 읽고, 상태 갱신/KB 검색 도구를 선택·호출하는
최소 Stateful Agent를 구현하고, 소규모 QLoRA 학습·저장·재로딩 및 학습 전후 비교를 검증합니다.
STT → Jev의 7개 필드 분류 PoC와는 별도 실험입니다.

팀원용 한눈에 보기

한국어 입력 + 현재 상태 → Qwen → 도구 호출 JSON → Python 검증/실행 → 상태 저장
                                    ↘ 검색 결과 → Qwen 답변
고정 평가 59개 시나리오(84턴) → 학습 전/후 동일 조건 비교

모델과 런타임의 역할

- Qwen: 입력과 상태를 해석하여 도구/인자 또는 답변을 생성합니다.
- Python: 세션 상태 보관, 스키마 검증, 실제 도구 실행을 담당합니다.
- 모델 가중치에 사용자별 상태를 저장하거나, 모델이 직접 DB를 변경하지 않습니다.
- 매 턴 현재 상태를 명시적으로 전달합니다. 과거 전체 대화 이력을 재투입하는 방식은 아닙니다.

범위

상태 5개: skin_condition, severity, usage_time, product_used, symptom_onset
도구 2개: update_session_state, search_knowledge_base
KB는 합성 fixture 태그 검색이며 실제 스킨케어 KB/RAG 성능 평가가 아닙니다.
intent, routine_change_requested를 포함한 원래 7필드 Jev 평가를 완료한 것은 아닙니다.

데이터

- 공개 한국어 도구 데이터: 정형화 14,609개(train 13,074 / validation 812 / test 723).
- 신규 합성 Stateful 데이터: train 209시나리오/529판단예, validation 30/80, holdout 59/143.
- 실제 이번 학습: Stateful 100판단예 + 공개 train의 도구호출/응답 20판단예 = 120개.
- 100개의 완전한 대화를 모두 학습했다는 의미가 아닙니다.
- 모든 정답 궤적을 실제 도구 구현으로 실행 검증. 첫 100개 궤적도 재검증했습니다.
- 데이터 분할 간 표면 템플릿 계열과 완전히 같은 사용자 문장을 분리했습니다.
- 사람 수집 음성·AIHub 데이터가 아닌 합성 한국어 데이터입니다. 독립 한국어 라벨 검수는 미실시입니다.

구현 체크리스트

[x] Qwen 공식 템플릿에 맞춘 messages/tools 변환
[x] assistant 최종 판단 위치만 학습하는 손실 마스크
[x] 잘못된 도구/인자, 반복 호출, 비정상 응답 처리
[x] 세션별 외부 상태, 수정/부정/누락/검색 실패 시나리오
[x] 고정 holdout과 학습 데이터 분리, 파일 hash 보존
[x] CUDA NF4 forward/backward 및 실제 LoRA 가중치 변경
[x] 어댑터 저장 후 베이스 모델부터 재로딩, 결정적 probe 토큰 일치
[x] 학습 전후 동일 GGUF 실행계로 59개 평가
[ ] 실제 한국어 사용자/음성 데이터에 대한 일반화 검증
[ ] 별도 구축 중인 실제 knowledge base 연동

학습 설정 및 실행 결과

GPU: {train['environment']['gpu']}
학습: Qwen2.5-3B NF4 frozen base + q_proj/v_proj LoRA r=8, alpha=16, dropout=0.05
학습 가능 파라미터: {train['trainable_parameters']:,}
optimizer steps: {train['training']['optimizer_steps']}, microbatches: {train['training']['micro_batches']}
learning rate: 0.0002, seed: 20261104
NF4 검증 loss(20판단예의 평균): {train['validation_loss_before']:.6f} → {train['validation_loss_after']:.6f}
가중치 변경: {train['adapter_weights_changed']}; 저장/재로딩 probe 일치: {train['adapter_reload_probe_equal']}
재로딩 검증 범위: 저장된 어댑터를 두 번 독립 로딩하여 최대 24토큰 probe를 비교했습니다.
저장 직후 로깅 인자 충돌로 프로세스가 종료되어, 저장 전 메모리 출력과의 비교는 남아 있지 않습니다.
저장된 가중치와 완료된 60스텝 로그로 검증만 재개했으며 재학습하지 않았습니다.
어댑터: {train['adapter_path']}

평가 설계

A: 공식 Q4_K_M GGUF, 어댑터 없음, 고정 59시나리오
B: 동일 GGUF + NF4로 학습한 LoRA를 F32 GGUF로 변환해 적용, 동일 59시나리오
두 실험의 모델·평가 hash, system/tools, 생성 설정, 엔진 경로를 자동 대조했습니다.
학습은 NF4, Agent 비교는 두 단계 모두 Q4_K_M입니다. 이전 개발 10건과 직접 비교하지 않습니다.
정답/정답 도구는 모델 입력에 전달하지 않습니다.

평가 결과

시나리오 전체 성공: {b['passed_scenarios']}/59 ({b['passed_scenarios']/59:.1%}) → {a['passed_scenarios']}/59 ({a['passed_scenarios']/59:.1%}), 차이 {delta:+d}개
턴 전체 성공: {b['passed_turns']}/84 → {a['passed_turns']}/84
5필드 상태 완전 일치: {b['state_exact_turns']}/84 → {a['state_exact_turns']}/84
실제 실행 턴: {b['executed_turns']}/84 → {a['executed_turns']}/84
paired 시나리오: {json.dumps(dict(paired), ensure_ascii=False)}

중요: 시나리오 성공 증가와 상태 추출 개선은 같은 의미가 아닙니다.
응답/실행 완료는 {b['completed_turns']}/84 → {a['completed_turns']}/84로 늘었지만,
상태 완전 일치는 {b['state_exact_turns']}/84 → {a['state_exact_turns']}/84로 악화했습니다.
특히 product_used 누락과 usage_time 오분류가 남아 있습니다. 전체 품질 향상으로 단정하지 않습니다.

필드별 일치(실행 턴 기준; 미실행 턴이 있으면 별도 확인 필요)
'''
    for field in b['field_exact_hits']:
        text += f"- {field}: {b['field_exact_hits'][field]}/{b['executed_turns']} → {a['field_exact_hits'][field]}/{a['executed_turns']}\n"
    text += '\n완료 시간 기록이 있는 턴의 지연시간(조기 실패는 제외)\n'
    for phase, m in [('학습 전', b), ('학습 후', a)]:
        lat = m['completed_turn_latency']
        text += f"- {phase}: n={lat['n']}, 평균 {lat['mean_seconds']:.3f}초, P95 {lat['p95_seconds']:.3f}초\n"
    text += '\n호출 비용: 로컬 실행이므로 API 청구는 없음. 전력/하드웨어 비용은 측정하지 않았습니다.\n\n대표 잔존 실패 사례\n'
    for i, f in enumerate(failures[:8], 1):
        text += f"\n{i}. {f['id']} / {f['category']}\n입력: {f['input']}\n실패 조건: {', '.join(f['failed_checks'])}\n"
        text += '정답 상태: '+json.dumps(f['expected_state'], ensure_ascii=False)+'\n'
        text += '실제 상태: '+json.dumps(f['actual_state'], ensure_ascii=False)+'\n'
        text += f"오류/답변: {f['error'] or f['answer']}\n"
    text += '''
산출물 / 완료 조건

[x] README 실행 방법 및 환경 분리
[x] 상태 정의/합성 라벨/원본 hash
[x] 테스트별 정답·예측·도구 호출·실패 판정·시간 JSON/CSV
[x] 학습/저장/재로딩 증거 및 학습 전후 결과
[x] 대표 실패와 제한사항 기록

결론과 다음 단계

Stateful 도구 Agent와 QLoRA 파이프라인의 실제 실행 가능성은 확인했습니다.
도구 호출/응답 완료는 개선되었으나 상태 추출은 악화했으므로, 현 어댑터를 기본 품질 개선판으로 채택하지 않습니다.
도구 선택과 인자 의미 정확도를 분리해 보고, product_used 누락·시간·증상 혼동을 먼저 보강해야 합니다.
기존 3턴 데모도 실행은 완료했지만 첫 턴에서 product_used=yes를 빠뜨렸습니다.
이 데모를 3/3 의미 정확도로 집계하지 않으며, 로그는 output/runs/qlora-demo-final/에 있습니다.
위 수치는 고정된 소규모 합성 평가 결과이며 일반 한국어/스킨케어 서비스 정확도가 아닙니다.
다음은 독립 사람이 작성·검수한 한국어 대화와 실제 KB 도구 계약을 먼저 고정한 뒤,
수정·부정·미언급 및 검색 응답을 중심으로 별도 미사용 평가를 실행하는 단계입니다.
현 holdout은 이미 결과를 관찰했으므로 반복 튜닝용 개발셋으로 쓸 경우 새 test를 마련해야 합니다.
이 결과만으로 Jev 대체, 의료적 안전성 또는 QLoRA의 일반적 우월성을 단정하지 않습니다.

주요 파일

- output/stateful_qlora_comparison.json
- output/training/gguf-holdout-before/results.json, turns.csv, metadata.json
- output/training/gguf-holdout-after/results.json, turns.csv, metadata.json
- output/training/qlora-smoke-v3/comparison.json, progress.jsonl, metadata.json
- data/stateful/v2/README.md, manifest.json
- adapters/qlora-smoke-v3/adapter_model.safetensors, adapter-f32.gguf
'''
    (ROOT/'output/stateful_qlora_results_ko.txt').write_text(text, encoding='utf-8-sig')
    print(json.dumps({'before': b['passed_scenarios'], 'after': a['passed_scenarios'],
                      'paired': dict(paired), 'representative_failure_categories': len(failures),
                      'report': str(out)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
