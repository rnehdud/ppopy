# 결과 요약

**36개 입력·12개 유형을 평가했고, 29개 입력이 사전에 작성한 핵심 조건을 모두 충족했습니다.** 동일 6개를 1회씩 추가 실행해 총 42회 평가했습니다. 기대값은 에이전트 작성·사람 미검토 상태이며 독립 평가셋이 아닙니다.

- 실행 모델: Jev 응답 `jev-1.14.0`. 추출 코드·질문·규칙·기대값을 실행 중 바꾸지 않았습니다.
- 관계 추출 지연: p50 **0.698초**, p95 **1.190초**(36건, nearest-rank). STT·최초 전체 문장 분류·DB·앱 통신은 제외합니다.
- 전체 42회에서 요청 105회·질문 416개. 사용량: 입력 161,927 / 출력 30,128 토큰. 금액 비용은 계산하지 않았습니다.
- 불확실/미평가 관계 12개(최초 36건). 값이 맞으면 점수가 낮아도 조건 충족으로 계산하므로 자동 확정 가능한 비율은 아닙니다.
- 반복 6건의 채점 대상 값은 6/6 동일했습니다. 점수·전체 JSON 동일성이나 장기 안정성을 의미하지 않습니다.

## 우선 개선할 사항

| 우선순위 | 사례 | 실제로 확인한 문제 |
| --- | --- | --- |
| 1 | E16 | Jev는 건조함을 affirmed로 맞혔지만 코드 부정 규칙이 뒤의 가려움 부정까지 읽어 dryness=denied로 덮어씀 |
| 2 | E09 | 여러 문장에 걸친 정정에서 최종 제품 B까지 superseded로 판단 |
| 3 | E34 / E35 | 공백 없는 A로션썼어는 제품 누락, A로션은요는 조사·종결 표현이 제품명에 남음 |
| 4 | E20 | 후속 문장의 강도 모름을 앞선 증상에 연결하지 못함 |

## 해석에 주의할 두 사례

- **E12:** 아침 사용·저녁 미사용은 논리적 모순이 아니라 서로 다른 사건입니다. 현재 기대값은 대표 필드 `conflict`라는 임시 표현을 사용했습니다. 기대 계약 자체를 사건 2개로 바꾸는 검토가 필요합니다. 이번 29/36 집계에서는 사전 기대값을 그대로 유지했습니다.
- **E33:** 쓰라고의 쓰라가 따가움 탐지 어휘와 겹쳐 불필요한 stinging 레코드를 생성했습니다. 하지만 Jev의 증상 상태는 `not_mentioned`로 올바르게 기각했습니다. 피부 증상을 긍정으로 오분류한 사례와 구분해야 합니다. 기대 symptom 레코드 수 0과 실제 1의 구조 차이로 미충족 처리했습니다.

규칙을 더 늘리는 것뿐 아니라 **규칙의 적용 범위와 다른 증상·사건 경계**를 먼저 검증해야 합니다. 이번 요청은 평가이므로 발견한 오류를 숨기기 위한 추출 코드 수정·재채점은 하지 않았습니다.

## 재현

```powershell
.venv\Scripts\python.exe -m poc.jev.benchmark
```

- 데이터: `poc/jev/evaluation_data/diverse-v1.json`
- 원시 결과: 이 폴더의 `E01-r1.json` 등. 원문·기대값·실제 JSON·조건별 판정·API 사용량 포함.
- 코드/데이터 해시·환경·모델·시각: `manifest.json`, `summary.json`. 실행 전후 파일 해시 일치 확인.
- 기대값은 수치·필드의 부분 조건이며 전체 의미 정답률·Exact Match·인간 검토 완료를 뜻하지 않습니다. 단순 구조 조건도 분모에 포함됩니다.

---

# 다양한 입력 평가

- 핵심 조건 전체 충족: 29/36건. 조건별: 217/227.
- 사람이 검토하지 않은 합성 기대값 기반 개발 평가. 독립 평가셋·일반 정확도가 아님.
- 조건 전체 충족은 전체 JSON의 Exact Match가 아님. 불확실 후보도 값 일치면 조건 충족으로 계산.
- 실행 중 추출 코드/프롬프트 수정 없음. STT·DB·기존 전체 문장 분류는 측정 범위 밖.

| 유형 | 조건 전체 충족 |
| --- | --- |
| 기본 사용·제품명 | 3/3 |
| 부정·계획 | 3/3 |
| 제품 정정 | 2/3 |
| 시간 연결·반복 사용 | 2/3 |
| 본인·타인 | 3/3 |
| 증상 긍정·부정 | 2/3 |
| 증상 강도 | 2/3 |
| 증상 시작·발견 시간 | 3/3 |
| 불명확한 이름·모름 | 3/3 |
| 답변 거절 | 3/3 |
| 가정·권유 | 2/3 |
| 구어체·띄어쓰기 오류 | 1/3 |

## 미충족 조건

### E09 · correction

> A로션을 썼다고 했는데 잘못 말했어. 실제로는 B크림만 썼어.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| products[1].correction | current | superseded |

### E12 · product_time

> A로션을 오늘 아침에는 쓰고 오늘 저녁에는 안 썼어.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| products[0].usage_state | conflict | denied |

### E16 · symptom_state

> 건조하지만 가렵지는 않아.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| symptoms[0].state | affirmed | denied |

### E20 · severity

> 피부가 가려워. 얼마나 심한지는 모르겠어.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| symptoms[0].severity | unknown | not_mentioned |

### E33 · hypothetical

> 친구가 A로션을 쓰라고 권했지만 나는 아직 안 썼어.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| symptoms.count | 0 | 1 |

### E34 · noisy_input

> A로션썼어 피부건조해

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| products.count | 1 | 0 |
| products[0].unique_match | 1 | 0 |
| products[0].usage_state | affirmed | None |

### E35 · noisy_input

> 어.. A로션은요 어제 밤에 발랐구요 ㅠㅠ 피부가 좀 가려워요

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| products[0].unique_match | 1 | 0 |
| products[0].usage_time | 밤 | None |

## 성능·반복 결과

```json
{
  "cases": 36,
  "cases_passed": 29,
  "checks": 227,
  "checks_passed": 217,
  "p50_s": 0.6982424499874469,
  "p95_s_nearest_rank": 1.1898766999947838,
  "requests_all_runs": 105,
  "questions_all_runs": 416,
  "models": [
    "jev-1.14.0"
  ],
  "uncertain_relations_primary": 12,
  "token_usage_all_runs": {
    "input_tokens": 161927,
    "output_tokens": 30128
  },
  "groups": {
    "basic": {
      "passed": 3,
      "total": 3
    },
    "plan_negation": {
      "passed": 3,
      "total": 3
    },
    "correction": {
      "passed": 2,
      "total": 3
    },
    "product_time": {
      "passed": 2,
      "total": 3
    },
    "subject": {
      "passed": 3,
      "total": 3
    },
    "symptom_state": {
      "passed": 2,
      "total": 3
    },
    "severity": {
      "passed": 2,
      "total": 3
    },
    "temporal_symptom": {
      "passed": 3,
      "total": 3
    },
    "ambiguity": {
      "passed": 3,
      "total": 3
    },
    "refusal": {
      "passed": 3,
      "total": 3
    },
    "hypothetical": {
      "passed": 2,
      "total": 3
    },
    "noisy_input": {
      "passed": 1,
      "total": 3
    }
  },
  "repeat_consistency": [
    {
      "id": "E06",
      "first_pass": true,
      "second_pass": true,
      "changed_scored_fields": []
    },
    {
      "id": "E14",
      "first_pass": true,
      "second_pass": true,
      "changed_scored_fields": []
    },
    {
      "id": "E16",
      "first_pass": false,
      "second_pass": false,
      "changed_scored_fields": []
    },
    {
      "id": "E23",
      "first_pass": true,
      "second_pass": true,
      "changed_scored_fields": []
    },
    {
      "id": "E26",
      "first_pass": true,
      "second_pass": true,
      "changed_scored_fields": []
    },
    {
      "id": "E34",
      "first_pass": false,
      "second_pass": false,
      "changed_scored_fields": []
    }
  ]
}
```