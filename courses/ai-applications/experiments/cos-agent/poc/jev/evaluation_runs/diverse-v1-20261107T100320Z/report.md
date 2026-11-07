# 다양한 입력 평가

- 핵심 조건 전체 충족: 35/36건. 조건별: 225/227.
- 사람이 검토하지 않은 합성 기대값 기반 개발 평가. 독립 평가셋·일반 정확도가 아님.
- 조건 전체 충족은 전체 JSON의 Exact Match가 아님. 불확실 후보도 값 일치면 조건 충족으로 계산.
- 실행 중 추출 코드/프롬프트 수정 없음. STT·DB·기존 전체 문장 분류는 측정 범위 밖.

| 유형 | 조건 전체 충족 |
| --- | --- |
| basic | 3/3 |
| plan_negation | 3/3 |
| correction | 3/3 |
| product_time | 2/3 |
| subject | 3/3 |
| symptom_state | 3/3 |
| severity | 3/3 |
| temporal_symptom | 3/3 |
| ambiguity | 3/3 |
| refusal | 3/3 |
| hypothetical | 3/3 |
| noisy_input | 3/3 |

## 미충족 조건

### E12 · product_time

> A로션을 오늘 아침에는 쓰고 오늘 저녁에는 안 썼어.

| 조건 | 기대 | 실제 |
| --- | --- | --- |
| products[0].usage_state | conflict | affirmed |
| products[0].eligible | False | True |

## 성능·반복 결과

```json
{
  "cases": 36,
  "cases_passed": 35,
  "checks": 227,
  "checks_passed": 225,
  "p50_s": 0.40104829997289926,
  "p95_s_nearest_rank": 0.883265400014352,
  "requests_all_runs": 66,
  "questions_all_runs": 373,
  "models": [
    "jev-1.14.0"
  ],
  "uncertain_relations_primary": 7,
  "token_usage_all_runs": {
    "input_tokens": 119738,
    "output_tokens": 20004
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
      "passed": 3,
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
      "passed": 3,
      "total": 3
    },
    "severity": {
      "passed": 3,
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
      "passed": 3,
      "total": 3
    },
    "noisy_input": {
      "passed": 3,
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
      "first_pass": true,
      "second_pass": true,
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
      "first_pass": true,
      "second_pass": true,
      "changed_scored_fields": []
    }
  ]
}
```