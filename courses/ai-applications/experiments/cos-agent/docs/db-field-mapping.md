# Jev 후보와 기존 DB의 매핑 초안

2026-11-08. 서울 리전 테스트 Aurora PostgreSQL의 Data API에서 `information_schema.columns`, `pg_constraint`를 조회했다. `SET TRANSACTION READ ONLY` 후 `transaction_read_only=on`을 확인했다. 사용자 행·암호문·Secret 값은 조회하지 않았다. 이는 현재 테스트 DB의 선택된 테이블에 관한 확인이며 운영 DB 동등성이나 저장 통합 승인이 아니다. AWS 식별자와 접속 비밀은 이 문서에 보관하지 않는다.

기준: [필드 요구사항 검토](agent-field-review.md), [Linear ERD](https://linear.app/ppopy/document/skinanalysis-db-아키텍처-crows-foot-erd-261106-a263885a7d6c). 아래는 명세 초안이며 실행 가능한 쓰기 adapter는 아니다.

| 논리 입력 | 확인된 DB 대상 | 매핑·검증 요건 |
|---|---|---|
| context.actor | identity.app_account.account_ref | 서버 인증에서 결정. 모델이나 요청 body로 권한 결정 금지 |
| participant 연결 | service.app_account_participant.account_ref / participant_id | 계정과 참여자는 다른 식별자. 기존 서버 연결 검증 재사용 |
| context.consent | service.app_history_consent의 account_ref + consent_ref | 복합 PK/FK를 함께 참조. ACTIVE 여부는 서버 확인 필요 |
| 제품 언급 이름 | catalog.product_fact.public_brand_name / public_product_name / public_search_aliases | 검색 입력으로만 사용. 이름을 product_id로 직접 대입하지 않음 |
| product_id | catalog.product_fact.product_id | 제품 식별 확인 후 사용 |
| product_version | catalog.product_fact.product_version | 실제 컬럼 존재 확인. catalog.revision.revision_id와 구분 |
| 카탈로그 고정 버전 | catalog.release_item.release_id / product_id / revision_id | release/revision FK 존재. product_id 자체의 product_fact FK는 미선언 |
| 보유 제품 | service.user_product.participant_id + product_id | 복합 PK. product_id의 product_fact FK는 미선언; 서버에서 일치 검증. 보유와 실제 사용 구별 |
| 추출·확인 전 후보 | care_sensitive.intake_draft.payload_ciphertext | 저장 후보일 뿐 기존 payload 계약 확인 전 확정 금지. participant_id PK라 참여자당 한 행; 대화 이력 append 테이블로 사용 불가 |
| 사용·증상 기록 | care_sensitive.app_history_record.payload_ciphertext 또는 checkin_event.payload_ciphertext | 논리 필드를 암호화 payload 내부에서 표현해야 함. 두 저장 경로의 용도·중복 방지·보관 계약을 백엔드에서 확인 후 선택 |
| 실제 사건 시각 | checkin_event.occurred_at | NOT NULL timestamptz. 원문이 아침뿐이면 임의 시각을 만들어 채우지 않음. 이 컬럼의 기존 서비스 의미부터 확인 |
| 최초 수집 시각 | app_history_record.first_collected_at | 실제 사용 시각과 별개. 서버 수집 시각 계약에 맞춤 |
| 후속·정정 연결 | app_closed_loop_event / app_closed_loop_parent | 기존 kind·decision 연결 규칙 확인 후 변환; 자유 enum 삽입 금지 |
| 점수·원문 span·revision·추출 출처 | 별도 직접 컬럼은 이번 대상에서 미확인 | 기존 payload에 포함 가능한지 확인. 임의 신규 컬럼 추가하지 않음 |

## 실제 제약조건이 만드는 경계

- `app_history_record.category`는 questionnaire/current_sensitive_profile/checkin/product_usage_feedback/personalized_result만 허용한다. `usage_event`나 `jev_candidate`를 임의로 새 category로 넣을 수 없다.
- `app_history_record.record_ref`와 consent_ref는 `sha256:` + 64자리 소문자 hex 형식이다. 형식만 맞춰 임의 생성하지 않고 기존 canonicalization·hash 생성 계약을 재사용해야 한다.
- history의 state는 ACTIVE/PENDING_DELETE다. ACTIVE는 delete_after=NULL, PENDING_DELETE는 delete_after 필수다. 별도 intake_draft/checkin_event는 delete_after NOT NULL이므로 하나의 보관 기본값으로 통합하면 안 된다.
- `checkin_event`는 payload_ciphertext와 encryption_key_ref가 함께 NULL이거나 함께 존재해야 한다. `intake_draft`와 `app_history_record`는 둘 다 필수다. 평문 JSON을 bytea로 바꾸는 것은 암호화가 아니다.
- `app_closed_loop_event.kind`는 snapshot/decision/recommendation_response/actual_use_response/actual_action/followup이다. decision_ref는 종류별 NULL/필수 조건이 다르다. 모델의 intent와 동일 enum으로 취급하지 않는다.
- `catalog.revision.revision_id`는 접두어 없는 64자리 소문자 hex다. product_version, text_revision, record_ref는 각각 다른 계약이다.
- `product_fact.verified_by_owner`는 카탈로그 메타데이터다. 사용자 보유 확인이나 사용 기록 승인을 뜻하지 않는다. `user_product.option_confirmed`도 text 컬럼이라는 사실만 확인됐으며 boolean 확인값으로 추정하지 않는다.

## 구현 전 남은 확인

1. 기존 백엔드의 암호화 payload schema, serializer, 키 참조·무결성 및 저장 서비스 확인.
2. 후보 draft와 확정 history/checkin의 상태 전이, 거절·정정·철회·멱등성 계약 확인.
3. 다중 사용 사건 분리, 시간 미상/정밀도 표현을 합성 사례로 검증. DB 필수 timestamp가 있다고 사용 시각을 추정하지 않음.
4. 서버 adapter에서 사용자·동의·제품 ID/version을 결합한 뒤 개발 환경에서 암호화·저장·재조회 검증.

현재 ppopy에는 DB 쓰기나 실사용 수집을 연결하지 않는다. development_preview와 production_enabled=false를 유지한다.

접속 점검 중 자동 일시중지에서 재개 응답을 받아 재시도했다. 첫 조회의 종료 호출은 CLI 인자 오류로 명시적 rollback에 실패했으며 쓰기는 없었고 Data API의 유휴 트랜잭션 만료 대상이다. 이후 제약조건 조회는 별도 읽기 전용 트랜잭션에서 수행하고 `Rollback complete`를 확인했다.
