# 백엔드 기준 엔진 전달 계약과 필드 제안

현재 기본 엔진은 [백엔드 필드 직접 추출](../poc/jev/BACKEND_FIELDS.md)로 전환했다. 아래 source 확인·백엔드 필드·확장 제안은 유효하지만, 중간 PoC 후보를 변환하는 설명은 과거 재현 경로다. 기본 경로에서는 map_candidates를 호출하지 않으며 6개 백엔드 필드를 Jev가 직접 판정한다. kind/observed_at은 앱 입력으로 남긴다.

2026-11-08. 앱 전달 데이터의 정본은 SkinAnalysis의 `validate_skin_state`와 `miray_skin_state.json`이다. Jev 관계명은 추출 내부 계약이며 앱 요청 본문으로 전달하지 않는다. 기존 결과·평가 재현을 위한 `--json`은 디버그 출력으로 유지하고 앱용 경로는 `--app-json`으로 분리한다.

## 실제 소스 확인

GitHub에서 아래 두 파일을 읽고 피부 상태 필드·허용값·교차 필드 검증·UTC 정규화를 현재 검토 스냅샷과 대조했다. 전체 소스를 복사하거나 운영 데이터를 가져오지 않았다.

- [백엔드 검증/저장 코드](https://github.com/rnehdud/SkinAnalysis/blob/main/skin_engine/miray_skin_state.py): 확인한 Git blob SHA `2b6b7169b7238b63738c040e2607c2a8fbf87a80`.
- [백엔드 설정](https://github.com/rnehdud/SkinAnalysis/blob/main/skin_engine/config/miray_skin_state.json): 확인한 Git blob SHA `1bcf14b64ecce86fef26d5393c5b461c41515b60`.

소스 계약은 1.0.0이며 아래 9개 키를 정확히 요구한다. HTTP 경로는 POST `/api/v1/app/skin-state`로 준비돼 있지만 runtime_enabled=false다. 평문 최대 크기는 4096 bytes, HTTP 최대 요청 크기는 8192 bytes다. 저장 함수는 서버 참여자 문맥·접근 권한·민감정보 및 별도 이력 동의를 검사한 뒤 암호화하고 이력 레코드를 저장한다. ppopy에서 이 경로나 함수를 호출하지 않는다. 배포된 서버의 최신 소스와 동일하다는 검증은 아직 아니다.

## 백엔드 필드별 판정

| 백엔드 필드 | 전달 기준 | PoC에서 처리하는 방식 |
|---|---|---|
| version | 정확히 1.0.0 | 고정된 지원 버전 검사. 다른 버전은 보류 |
| kind | baseline/checkin | 앱 흐름 또는 명시적 입력으로 선택. 임의 기본값 없음 |
| observed_at | 실제 관찰의 ISO-8601 UTC 시각 | 앱의 확인 입력 필요. 전송 시각이나 모델 추정으로 대체하지 않음 |
| concern_presence | reported/none_reported/unknown/not_asked/user_refused | 명시적 앱 입력 필요. 피부 불편 있음과 전체 고민 있음을 자동 동일시하지 않음 |
| persistence | recent/recurring/persistent 및 허용 누락 상태 | 추가 질문/앱 입력. 시작 날짜를 지속성으로 자동 환산하지 않음 |
| recent_change | better/worse/unchanged/fluctuating 및 허용 누락 상태 | 사용자의 직접 보고 필요. 엔진의 개선 판정 금지 |
| discomfort_presence | reported/none_reported/unknown/not_asked/user_refused | 유효한 본인 긍정 증상의 reported만 후보로 제안. 일부 증상 부정을 전체 none_reported로 확대하지 않음 |
| discomfort_types | 설정의 7개 허용 enum, 중복 없는 배열 | stinging→stinging, itching→itching, redness→redness_tendency는 확인 전 후보. 나머지는 아래 참조 |
| sensitivity_history | reported/none_reported/unknown/not_asked/user_refused | 현재 불편 반응으로 과거 민감 이력을 추정하지 않고 별도 입력 |

각 누락 상태는 실제 답변 맥락에 맞춰 앱이 명시적으로 제공해야 한다. 미구현/누락을 자동으로 not_asked·unknown으로 채우지 않는다. 최종 계약에서 reported discomfort이면 비어 있지 않은 types가 필요하고 다른 presence 값이면 빈 배열이어야 한다. concern_presence가 reported가 아니면 persistence/recent_change에 실질적인 긍정 값을 넣지 않는다.

## 기존 PoC 필드의 역할

| 입력 정보 | 분류 | 처리 |
|---|---|---|
| 따가움·가려움·붉음의 유효한 본인 보고 | 변환 후 확인 | 백엔드 discomfort 후보로 제안 |
| 단순 건조함·트러블 | 백엔드 확장 검토 | 아래 distinct_concern_types 제안. 건조함을 tightness로 치환하지 않음 |
| 명시적 당김·화끈거림·각질 증가 | 기존 백엔드 지원, 추출기 부족 | backend tightness/burning/increased_scaling 사용 가능. 추출 어휘/대상 분리를 보완해야 하며 백엔드 신규 enum 제안 사유가 아님 |
| 강도·시작·발견 시점·부위·지속시간 | 백엔드 확장 검토 | 아래 symptom_observation_details. 현재 payload에 추가하지 않음 |
| 제품명·제품 식별·사용 사건 | 별도 도메인 계약 | 아래 product_usage_events. skin_state에 삽입하지 않음 |
| 원문·span·모델 점수·모델/규칙 결과 | 내부 전용 | 로컬 디버그/추출 검증. 앱 payload에 포함하지 않음 |
| 인증 계정·참여자·동의·암호화 키 | 서버 전용 | 모델 생성 금지. 기존 백엔드 문맥과 권한 검사 유지 |

## 제안할 백엔드 확장 — 승인/구현 전

| 제안 ID | 우선순위·필요성 | 제안 범위·보류점 |
|---|---|---|
| product_usage_events | P1: 실제 사용 이력과 루틴 시각 추정에 필요 | 별도 버전 계약. 검증 제품 ID/version, 사건별 사용/부정/계획·주체·정정·사용자 확인, 원문 시간 정밀도와 정규화 가능한 시각을 분리. 미상 시각을 DB NOT NULL 때문에 추정하지 않음. 저장 위치/보관·동의/멱등성/철회 연결은 서버 담당자와 결정 |
| distinct_concern_types | P1: 건조/트러블 등 고민별 질문과 KB 검토에 필요 | 기존 concern_presence는 존재 여부만 표현. 고민 종류와 보고 상태를 표현할 별도 enum/버전 확장 검토. 어떤 종류를 지원할지는 KB·앱 요구를 대조해 합의. 현재 dryness/breakout을 자동 승인하지 않음 |
| symptom_observation_details | P2: 증상별 질문·후속 기록이 기능상 필요할 때 | 종류별 사용자 보고 강도·부위·시작/발견 시점과 그 정밀도·정정/확인을 표현. 임상 중증도나 제품 인과관계로 해석하지 않음. 모든 항목을 필수로 수집하지 않고 질문 효용·보관 필요성 검토 |

앱 출력의 extension_proposals에는 이 ID만 표시한다. 제안이 필요하다는 것이 운영 스키마가 변경됐다는 뜻은 아니다. 기존 backend enum이 이미 지원하는 항목은 추출기 보완 사항으로 분리한다.

## 앱용 전달 생성기

`mapping_review/backend.py`의 `prepare_handoff(features, confirmed_state=None, confirmation=None)`는 네트워크·DB 없는 함수다.

1. 후보와 필요한 앱 입력을 backend 필드 기준으로 반환한다. 관찰 시각 등 없는 값은 질문으로 남기고 payload=null이다.
2. 앱이 완성한 9키 객체를 제공하면 enum·형식·상호 제약·UTC·크기를 검증하고 정규화한다. 유효하지 않으면 invalid_input, payload=null이다.
3. 유효하면 원문 revision·정규화 payload hash·계약 hash에 묶인 confirmation_binding을 반환한다. 확인 전 payload는 null이다.
4. 앱이 명시적 확인을 완료해 동일 binding과 confirmed=true를 제공하면 payload에 백엔드 9키만 반환한다. 수정된 원문·확인 내용·계약은 이전 확인을 무효화한다. 후보를 수정한 값도 사용자가 명시적으로 확인한 완성 입력으로 취급한다.
5. status=prepared_disabled도 저장 허가가 아니다. production_enabled=false, backend_route_enabled=false, authorized_for_storage=false를 유지한다. UI confirmation은 일관성 검사이며 보안 자격 증명이 아니다. 실제 서버는 세션·권한·동의와 payload를 다시 검증해야 한다.

`candidate_skin_state`는 부분 후보이고 `payload`만 완성된 백엔드 입력이다. 앱은 전체 envelope나 내부 --json 결과를 POST body로 보내면 안 된다. 이 구현은 확인 UI·인증·HTTP 전송·암호화·저장·철회를 제공하지 않는다.

합성 개발 예시 (`cos-agent/`에서):

```powershell
uv run python poc/jev/test_jev_text.py "나는 피부가 따갑고 가려워." --app-json
uv run python poc/jev/test_jev_text.py "나는 피부가 따갑고 가려워." --app-json --confirmed-state poc/jev/mapping_review/examples/synthetic_skin_state.json
```

두 번째 예시는 합성 파일을 사용한 확인 준비 예시이며 사용자 확인 완료를 주장하지 않는다. --confirmation 파일은 앞 단계의 confirmation_binding에 confirmed=true를 추가한 합성 UI 응답이다. 원문과 확인 데이터는 외부 Jev 처리 동의·앱 세션을 갖춘 통합 전까지 합성 데이터만 사용한다. --app-json은 기존 참고용 classify 호출을 건너뛰고 실제 관계 추출과 오프라인 전달 검증만 실행한다. --json은 기존 평가용 내부 출력을 유지한다.

## 검증 결과와 실제 앱 통합 전 남은 작업

실험 테스트 142 passed. 9키 제한, enum·교차 필드·UTC·크기 검증, 누락/미상/거절 구분, 수정된 원문·payload·계약의 확인 무효화, 입력 불변성, 앱 출력의 내부 정보 제외 및 참고용 classify 호출 제외를 확인했다. 실제 Jev 합성 문장의 --app-json 결과와, 이전 합성 추출 결과를 사용한 완성 입력→확인 binding→prepared_disabled 흐름도 실행했다. 산출물은 ignored `outputs/backend-handoff/`에 있다. 실제 서버 코드 자체를 실행한 교차 검증은 아니며 최신 배포 확인이나 통합 완료를 뜻하지 않는다.

원본 스냅샷 해시 27/27, KB 구조 95/95, 확장/현재 명세 테스트 371 passed. 엄격 원본 검증의 62 passed/5 failed와 감사 52/57은 유지했다. coverage와 합성 CLI의 production_enabled=false도 확인했다. 생성 보고서는 outputs/에 두었다.

다음 앱 통합은 별도 작업이다: 실제 앱의 관찰 문맥·추가 질문·확인 UI, 서버 최신 validator와의 교차 테스트, 로그인 세션·민감정보/외부 모델 처리·이력 동의, 요청 크기와 전체 실행 시간 제한·재시도 정책, 기존 암호화 저장 경로와 철회·멱등성 연결. 테스트 계약을 통과했다고 runtime_enabled를 활성화하지 않는다.
