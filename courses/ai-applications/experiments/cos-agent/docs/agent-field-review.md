# DB 매핑 전 에이전트 필드 검토

2026-11-08. 로컬 `relations-0.3` 구현, 개발 가이드, CSE 406 최신 제출 방향을 대조했다. AWS DDL이나 운영 백엔드는 확인하지 않았다. 아래는 논리 계약이며 운영 테이블 설계나 사람 검토 승인이 아니다.

검토 결과: 현재 분류만으로 에이전트 운용 요건을 모두 충족하지 않는다. 추출 후보가 존재한다는 것과 에이전트가 판단·저장·표시할 준비가 됐다는 것은 다르다. `relations-0.4`는 기존 관계를 유지하고 `agent_fields`에 누락 필드의 수집 책임과 미평가 상태를 추가한다. 새 필드 자동 추출, DB 저장, 승인 API는 구현하지 않았다.

## 현재 분류와 부족한 의미

| 범주 | 현재 표현 | 검토 결과·수정 방향 |
|---|---|---|
| 요청 | 초기 분류에 intent 제외, 관계 결과에는 없음 | `intents[]`로 복수 요청 보존. 기록·질문·루틴 검토·수정 요청 구별. 요청 대상/변경 동작은 별도 `requested_change`. 자동 실행 금지 |
| 제품 | 원문 이름·위치, ID/version=null | 이름 언급·실제 제품 식별·보유·사용자 확인·사용법 근거를 분리 |
| 사용 상태 | affirmed/denied/planned/hypothetical/conflict/unknown/declined/not_mentioned | 유지. planned를 실제 사용 이력으로 변환 금지. 본인/타인/미상 주체를 별도로 유지 |
| 사용 사건 | 제품 언급당 대표 날짜/시간, 일부 규칙의 usage_events | 한 제품의 아침 사용/저녁 미사용은 서로 다른 사건. 사건별 상태·주체·정정·시점·확인 필요. 현재 일반 사건 추출은 미완성 |
| 시간 | 원문 date/time span | raw 표현과 정규화 구간·정밀도·기준 발화 시각·시간대 분리. 아침을 임의 시각으로 바꾸지 않음 |
| 사용 방식 | 없음 | 실제/계획 빈도, 양과 단위, 부위, 순서. 누락이라고 매번 모두 질문하지 않고 판단에 필요한 항목만 질문 |
| 증상 | 5종, 상태·대상·강도·근거·시작 날짜/시간·발견 시간 | 관찰 시각, 발견 날짜, 지속기간, 부위, 사용 사건 연결, 정정, 확인 상태 추가 필요 |
| 증상 범위 | 건조·트러블·붉음·따가움·가려움 어휘 관문 | 지원 어휘 밖의 부종·통증 등의 미탐지 가능. 빈 목록은 무증상·안전 판정이 아님. unsupported는 unassessed |
| 증상 변화 | 없음 | improving/worsening/unchanged는 사용자 보고로만 수집. 자동 개선 판정·제품 인과 추정 금지 |
| 프로필 | confirmed, concerns, excluded_product_ids | 기존 beauty_agent 골격은 별도 계약. 확인한 고민·선호·제외 이유·거절/미상·수정 시점은 상세화 필요 |
| 서버 문맥 | 없음 | actor·권한·동의·요청 ID·대화 revision은 서버 검증 대상. 모델 출력에서 부여 금지 |
| 판단 근거 | 후보 score와 규칙 method | 실제 모델/질문 버전·KB/제품/입력 revision·검토된 evidence ID·미충족 조건 필요. score는 승인이나 임상 확신이 아님 |
| 결과·승인 | 전체 candidate | ask_user/retrieve_evidence/hold/draft/no_action 구분. 초안 hash·승인 범위·유효기간 필요 |
| 미러 | 실험 입력에는 device 가능 | 최신 CSE 방향은 출력 전용. 허가된 기기·명령 만료·수신·표시 확인은 별도 서버 기록. STT 구현 완료로 간주하지 않음 |

## 필드 값의 상태와 출처

새 요구 필드의 기본값은 `value=null,evidence_status=unassessed`다. 추출하지 않은 값을 not_mentioned로 표시하지 않는다. 이후 adapter에서는 다음 축을 별도로 검증해야 한다.

- 근거 상태: explicit_positive / explicit_negative / not_mentioned / unknown / declined / ambiguous / conflict / unassessed. `not_applicable`은 명시적 적용 조건에 한해서만 사용한다.
- 추출 상태: candidate / uncertain / unassessed / rule_candidate. 기존 relations 값은 변경하지 않는다.
- 확인 상태: pending / confirmed / rejected / superseded. confirmed는 앱의 명시적 확인과 대상 revision이 있어야 한다. 현재 자동 생성하지 않는다.
- 출처: 사용자 보고 / 모델 후보 / 코드 규칙 / 카탈로그·검토 근거 / 서버 검증. 서로 대체할 수 없다.

증상 severity는 사용자가 표현한 불편 강도이며 임상 중증도가 아니다. 거절한 항목은 단순 누락 질문으로 반복 요청하지 않는다. "건조해"에서 onset을 만들지 않고, "바른 뒤 따가워"에서 제품 원인을 확정하지 않는다.

`agent_fields.py`의 `FIELDS`가 추가 요구 필드의 기계 판독 가능한 목록이다. `owner=app`은 앱 확인 입력으로 보완할 책임을 뜻하며 추출 구현 여부를 뜻하지 않는다. `shape`는 설계 설명이며 타입 검증기는 아니다. 서버 문맥이나 앱의 실제 확인 데이터를 주입하는 adapter는 아직 없다.

## 작업별 최소 요건과 차단 조건

| 작업 | 필요한 조건 | 부족할 때 |
|---|---|---|
| 후보 표시 | 유효 원문 revision·span, 추출 상태/오류 표시 | 실패를 빈 사실 목록으로 확정하지 않음 |
| 실제 사용 기록 | 검증된 사용자·권한·목적 동의, 제품 ID/version, 사건별 본인 실제 사용, 시점 정밀도, 현재 revision 확인, 멱등 키 | 미해결 후보 유지; 확인 질문 또는 보류 |
| 루틴 검토 | 위 정보 중 판단에 필요한 확인 관찰·우선순위, 검토된 제품 사용법/KB 버전 | 사용자 정보는 ASK, 제품/근거 정보는 RETRIEVE, 해결 불가는 HOLD |
| 다음 루틴 시각 추정 | 사용자 확인된 실제 사용 시각, 시간대, 충분한 이력 기준 | 계획·표시 시각으로 대체 금지. 아침/저녁만 있으면 정확한 시각으로 처리 금지 |
| 초안 저장/미러 표시 | 동일 입력 revision과 초안 hash의 명시적 승인, 서버 권한, 유효기간·중복 명령 검사 | 저장/표시 보류 |

이 표는 서버 정책 구현 요구사항이다. 이번 출력의 `readiness=incomplete`, `write_authorized=false`는 고정된 개발 표시이며 실제 권한 검사 결과가 아니다. 필드가 있다는 이유로 준비 완료로 바꾸지 않는다.

## 이번 변경과 다음 구현 경계

추가한 것은 필드 목록·책임·미평가 placeholder 및 기존 제한적 사건 후보의 복사다. 기존 products/symptoms의 값과 부정·정정·오류 처리는 보존한다. Jev 질문·호출 수를 늘리지 않는다. `usage_event_candidates`에는 기존 규칙의 산출물만 있고, 사건별 필수 항목은 `event_field_requirements`로 명시한다. 일반 사건 분리·새 분류값 예측이 구현됐다는 뜻이 아니다.

다음 순서는 (1) 사건별 다중 사용·부정·계획 분리와 근거 span 검증, (2) 앱 확인 입력과 서버 문맥 adapter의 타입/교차 필드 검증, (3) 작업별 readiness 정책, (4) 실제 DDL 매핑이다. 기존 diverse-v1 기대값·실행 결과는 동결한다. 새 필드와 사건 분리는 별도 평가셋으로 검증해야 하며 기존 성능 수치를 새 계약의 정확도로 재사용하지 않는다.

`development_preview`, `production_enabled=false`를 유지한다. 실사용 수집·운영 DB 쓰기·결제·얼굴 분석·자동 개선 판정은 활성화하지 않는다.

## 로컬 검증

Python 3.10, `uv run --locked pytest -q`: 실험 전체 52 passed (신규 3개 포함). 외부 Jev 호출 없이 누락 필드가 사실로 생성되지 않음, 제한적 사건 후보 복사의 독립성, 출력 연결과 추가 호출 없음 등을 확인했다. 새 운용 필드의 추출 정확도나 서버 정책 검증 결과는 아니다.

저장소 검증: 원본 해시 27/27 일치, KB 구조 95/95 통과, 확장/현재 명세 371 passed. 엄격 원본 테스트는 기존 62 passed/5 failed, 감사는 52/57 충족으로 기존 다섯 불일치를 유지했다. 커버리지 60 cards/213 branches/180 shared cases, 합성 CLI의 production_enabled=false를 확인했다. 생성 보고서는 `outputs/`에 두었다.
