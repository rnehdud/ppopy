# 사용 사건 후보 계약 — relations-0.5

2026-11-08. `products`는 제품의 원문 언급이고 `usage_events`는 그 제품에 연결되는 개별 사건 후보다. 제품 하나에 대해 아침 사용과 저녁 미사용/계획을 각각 표현한다. 기존 제품별 대표 관계는 호환·검토용으로 남지만 여러 사건을 하나의 사용 상태로 확정하는 데 쓰지 않는다.

## 처리와 필드

1. 의미단위 안의 제품 언급과 원문 시간 표현으로 후보를 만든다. 한 단위의 복수 시간은 각각 후보로 만든다. 시간 없는 사용 표현도 후보로 만들고 시간 미언급을 보존한다.
2. 제품이 생략됐으면 같은 문장 앞부분에 유일한 제품 이름이 있을 때만 연결 후보를 만든다. 문장 경계를 넘거나 복수 제품 중 하나를 임의로 고르지 않는다. 후보당 Jev 질문 6개(제품 연결, 상태, 주체, 정정, 날짜, 시간)를 기존 20개 배치에 추가한다. 후보는 최대 32개이고 초과 시 warning을 남긴다.
3. Jev는 전체 원문을 보되 지정 구절·시간의 사건만 판정한다. unlinked 또는 not_mentioned가 확실한 후보는 제외한다. 불확실·API 실패는 미평가 후보와 clarifications로 남긴다. 대표 제품의 사용 상태를 사건 전체에 복사하지 않는다.
4. 기존 명시적 정정으로 취소된 제품 언급은 그 사건도 superseded로 처리한다. 사건별 정정 질문도 별도로 유지한다.

| 필드 | 의미 |
|---|---|
| event_id / product_mention_id | 이번 추출 안의 사건·제품 언급 ID. DB PK 아님 |
| source_scope | 원문의 구절과 Unicode code point 위치 |
| time_anchor | 분리 기준 원문 시간. 실제 사용과의 연결은 usage_time 질문에서 검증 |
| binding_method | 명시된 제품 / 같은 문장에서 생략된 제품 연결 후보 |
| relations.product_link | linked / unlinked / unknown |
| relations.usage_state | affirmed / denied / planned / hypothetical / conflict / unknown / declined / not_mentioned |
| relations.subject | self / other / unknown |
| relations.correction | current / superseded / unknown |
| relations.usage_date / usage_time | 원문 span 또는 미언급·모름·거절·충돌 상태. 절대 시각을 생성하지 않음 |
| confirmation_status | 항상 pending. 사용자 확인 기능 미구현 |
| eligible_for_usage_candidate | 본인 실제 사용·제품 연결·유효 정정과 점수 기준이 충족된 개발 후보. 저장 승인 아님 |

`usage_date`, `usage_time` 최상위 필드는 relations의 값을 복사한 편의 필드다. null이나 미상 문자열일 수 있다. 후보 점수가 낮거나 API 응답이 잘못되면 자동 확정하지 않는다. 실제 사용 후보에는 날짜가 없을 수도 있으므로 이 플래그만으로 DB 필수 시각을 채워 저장하면 안 된다.

예: `A로션을 오늘 아침에는 쓰고 오늘 저녁에는 안 썼어.`

| 사건 | 제품 언급 | 시간 | 상태 | 사용자 확인 |
|---|---|---|---|---|
| e0 | p0 | 오늘 아침 | affirmed | pending |
| e1 | p0 | 오늘 저녁 | denied | pending |

여러 사건이 붙은 제품은 `usage_event_summary=multiple_event_candidates`, 제품 단위 eligible=false로 표시한다. `agent_fields.usage_event_candidates`에도 동일 사건을 복사하고 `event_extraction_status=unit_time_candidates`로 표시한다. 자동 승인·DB 저장은 연결하지 않는다.

## 한계와 검증 범위

후보 생성은 사용 동사 어휘·의미단위 분할·원문 시간 탐지에 의존한다. 문장 간 대명사, 여러 제품의 생략, 지원 어휘 밖 표현, 반복 습관을 실제 개별 사건으로 변환하는 문제는 미해결이다. 같은 시간에 여러 행동이 한 단위에 남으면 압축될 수 있다. 빈 사건 목록은 사용하지 않았다는 확인이 아니다. fallback 분할에서는 맥락이 넓어질 수 있다. 제품 식별·시간 해석·사용자 확인은 후속 단계다.

기존 diverse-v1 기대값과 동결 실행 결과는 변경하지 않았다. 새 사건 결과를 기존 제품별 평가의 통과로 재해석하지 않는다. 추가 합성 테스트는 상태별 후보 자격, 원문 위치, 생략 제품의 경계, API 실패, 정정, 배치 연결을 검사한다. 이는 한국어 추출 정확도에 대한 독립 평가가 아니다. 실제 Jev 합성 개발 예시는 ignored `outputs/`에 기록하며 원래 평가 폴더를 덮어쓰지 않는다.

로컬 전체 실험 테스트는 70 passed다. 실제 Jev API로 혼합 긍정/부정, 계획, 공유 술어의 복수 시점, 복수 제품, 타인/본인, 시간 미언급, 제품 정정 등 7개 합성 개발 입력을 실행했다. 계획의 `쓸` 어휘 누락을 발견해 보완한 뒤 해당 사례를 재실행하여 아침 affirmed / 저녁 planned와 계획의 eligible=false를 확인했다. 결과는 `outputs/usage-events-development.json`, 재확인은 `outputs/usage-events-plan-recheck.json`이다. 최초 파일에는 수정 전 계획 누락도 그대로 남겨 둔다. 이 실행은 모델 선택·점수에 의존하는 개발 관찰이며 검토된 성능 평가나 운영 통합 검증이 아니다.
