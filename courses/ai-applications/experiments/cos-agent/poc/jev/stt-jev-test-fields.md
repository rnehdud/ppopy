# STT → Jev 분류 테스트 필드 v0.1

작성일: 2026-11-04. 초기 설계 명세이며 이후 텍스트 API 실험이 추가되었다. 음성 테스트는 아직 수행하지 않았다. [설정 JSON](stt_jev_test_fields.json)은 내부 명세이고, 특정 제공자 API에 그대로 전송하는 요청 본문은 아니다. 현재 실험에서 intent는 제외하며 추가 질문은 실행 스크립트에 있다.

## 테스트 범위

| Field | Type | 분류 값 |
|---|---|---|
| `intent` | Choice | `record`, `recommend`, `question`, `modify_routine`, `other` |
| `skin_condition` | 복수 Noul | `dryness`, `breakout`, `redness`, `stinging`, `itching` 각각 true/false |
| `severity` | Choice | `mild`, `moderate`, `severe`, `unknown` |
| `usage_time` | Choice | `morning`, `afternoon`, `evening`, `unknown` |
| `product_used` | Noul | true/false |
| `symptom_onset` | Choice | `today`, `yesterday`, `recent`, `unknown` |
| `event_recognition_time` | Choice | `morning`, `afternoon`, `evening`, `unknown` |
| `routine_change_requested` | Noul | true/false |

총 8개 필드 그룹이며 정의된 판단 질문은 12개(Choice 5개 + Noul 7개)다. 증상 5개는 서로 배타적이지 않다.

이전 논의에서는 Intent를 향후 SLM의 책임으로 두었다. 이번 사용자 지정에 따라 **이번 Jev 실험에는 intent도 포함**한다. 이 테스트 설정이 최종 SLM/에이전트의 역할을 바꾸는 결정은 아니다.

## 분류 규칙 초안

- 현재 발화가 사용자의 실제 상태·경험·요청인지 확인한다. 부정·정정·인용·타인·가정을 구별한다.
- `intent`: 단일 대표 목적이다. 예를 들어 사용 사실과 함께 기존 루틴 변경을 명시적으로 요청하면 `modify_routine`을 선택한다. 독립적인 복수 요청을 단일 값으로 압축해야 하는 경우는 한계로 기록한다.
- `severity`: 사용자가 표현한 불편감의 강도이며 임상적 중증도가 아니다. 명시적 강도 없이는 추정하지 않는다. 복수 증상의 강도가 충돌하면 `unknown`으로 둔다.
- `usage_time`: 실제로 보고된 제품 사용 시간이다. 아침·저녁 동시 사용 등 하나의 선택지로 표현할 수 없는 경우 `unknown`과 별도의 충돌/모호함 상태를 남긴다. evening에 저녁·밤을 포함하는 것은 이번 초안의 운영 정의다.
- `product_used`: 실제 사용을 긍정하여 보고했는지를 판단한다. 향후 사용 계획, 제품에 대한 질문, 보유만 언급한 경우는 사용 보고와 구분한다. 정확한 제품 ID 추출은 이 필드 범위 밖이다.
- `symptom_onset`: 증상이 시작된 때다. “오늘 건조해”만으로 오늘 시작했다고 추정하지 않는다. “오늘부터 건조해”는 `today`다. `recent`는 날짜 없이 최근 시작을 명시한 경우이며 시간 범위를 임의로 숫자로 정하지 않는다.
- `event_recognition_time`: 사용자가 증상이나 변화를 처음 알아차린 하루 중 시간대다. 증상 시작 날짜(`symptom_onset`)나 제품 사용 시간(`usage_time`)과 구분한다. 인식한 시간대가 명시되지 않으면 `unknown`이다.
- `routine_change_requested`: 기존 루틴을 바꾸라는 요청 여부다. 단순 변경 가능성 질문과 실제 변경 요청은 구분한다.

운영 정의는 첫 라벨링 전에 검토하고 버전 고정한다. 수정하면 기존 정답과 성능 수치의 버전도 구분한다.

## Noul과 정보 누락

Noul은 원시 확률을 유지하고, 앱에서 사용할 true/false로 변환하는 임계값은 검증 사례로 정한다. 현재 임계값은 미설정이며 자동 확정은 하지 않는다.

특히 다음 둘은 다르다.

| 발화 | stinging의 의미 |
|---|---|
| “따갑지는 않아.” | 명시적 부정 |
| “저녁에 로션 썼어.” | 따가움 언급 없음 |

두 발화 모두 “따가움을 긍정 보고하는가?”에는 낮은 확률이 나올 수 있다. 따라서 **false만으로 실제 증상 없음이라고 저장하지 않는다.** `evidence_status`를 별도 관리하며 초기에는 미평가 상태를 유지한다. 이 상태를 자동 생성하려면 별도의 질문/검증 설계가 필요하다. 현재 명세는 이를 자동 구현했다고 가정하지 않는다.

제안 상태: `explicit_positive`, `explicit_negative`, `not_mentioned`, `unknown`, `refused`, `ambiguous`, `conflicting`. 이는 사용자가 지정한 분류값을 바꾸는 것이 아니라 결과 해석을 위한 부가 정보다.

## 합성 정답 예시 — API 실측 결과 아님

입력: “오늘부터 피부가 약간 건조하고 가려워. 저녁에 로션을 발랐어. 기존 루틴을 바꿔줘.”

```json
{
  "intent": "modify_routine",
  "skin_condition": {
    "dryness": true,
    "breakout": false,
    "redness": false,
    "stinging": false,
    "itching": true
  },
  "severity": "mild",
  "usage_time": "evening",
  "product_used": true,
  "symptom_onset": "today",
  "routine_change_requested": true
}
```

여기서 breakout/redness/stinging의 false는 이번 예시의 **긍정 보고 없음**을 뜻하며 증상이 실제로 없다고 확인한 값이 아니다. 정답 메타데이터에서는 `not_mentioned`로 구별한다. 예시 severity는 “약간”을 보고된 불편감 전체에 적용한 라벨링 해석이며, 모호한 문장은 검토 대상으로 둔다.

## 다음 실험의 기록 항목

사례 ID, 녹음 ID, 발화 시각·시간대, 사람이 작성한 기준 텍스트, 실제 STT 출력, 기대 필드값·근거 상태, Jev 원시 응답, 제공자·모델 버전, 질문 명세 버전, 지연·비용, API 오류를 남긴다. 기준 텍스트 → Jev와 녹음 → STT → Jev를 같은 사례로 비교한다. 발화의 개인정보나 음성을 불필요하게 운영 로그에 보존하지 않는다.

첫 테스트는 부정·미언급·정정·복수 증상·복수 시간대·제품 사용 계획·시작일 미언급을 포함한다. 모델과 제공자 선택, 실제 호출 코드는 후속 작업으로 진행한다.
