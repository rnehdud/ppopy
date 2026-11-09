# 현재 Jev 엔진: 백엔드 필드 직접 추출

제품도 [기존 제품 검색 계약](PRODUCT_FIELDS.md)으로 별도 처리한다. 최신 추출 메타데이터는 1.2이며, 아래 1.1의 chunk별 피부 상태 필드에 product_queries를 추가한 것이다. 피부 상태 6개 필드는 그대로이고 제품을 이 필드에 넣지 않는다. 카탈로그는 기본 offline fallback_pending 상태다.

현재 기본 실행은 `skin_state.py`의 `extract_skin_state`다. 기존 `relations.py`, 임시 STT 필드 설정, 증상 5종/제품 사건 중간 스키마를 호출하거나 읽지 않는다. Jev에 백엔드 `skin_state` 필드를 직접 질문하고 백엔드의 허용값을 후보로 받는다. 앱 계약은 `mapping_review/contract.json`의 SkinAnalysis 1.0.0이다.

| 백엔드 필드 | 값의 출처 |
|---|---|
| version | 지원하는 계약 버전 1.0.0 |
| kind | 앱의 baseline/checkin 입력. Jev가 추정하지 않음 |
| observed_at | 앱에서 확인한 실제 관찰 UTC 시각. Jev가 추정하지 않음 |
| concern_presence | Jev 직접 판정: reported/none_reported/unknown/not_asked/user_refused |
| persistence | Jev 직접 판정: recent/recurring/persistent/not_applicable/unknown/not_asked/user_refused |
| recent_change | Jev 직접 판정: better/worse/unchanged/fluctuating/not_applicable/unknown/not_asked/user_refused |
| discomfort_presence | Jev 직접 판정: reported/none_reported/unknown/not_asked/user_refused |
| discomfort_types | Jev 직접 판정: stinging/burning/itching/tightness/increased_scaling/redness_tendency/other_no_free_text 중 배열 |
| sensitivity_history | Jev 직접 판정: reported/none_reported/unknown/not_asked/user_refused |

## 실행과 출력

현재 추출 메타데이터 버전은 `skin-state-extraction-1.1`이다. 코드가 원문을 chunk로 나눈 뒤 **각 chunk마다 6개 백엔드 필드를 Jev에 별도로 질문**한다. 전체 원문을 공통 문맥으로 제공하되 지정 chunk 자체가 표현하는 정보만 배정하도록 요청한다. 전체 문장을 근거 선택지로 넣어 다시 묶는 경로는 없다. 출력은 모든 chunk를 원문 순서로 보여주며, 배정 없음·낮은 점수로 보류·API 실패·필드 병합 충돌도 구분한다.

예시(합성 입력):

```text
[1] A클렌저로 세안을 하고
    No backend field assigned.

[2] B로션을 발랐는데
    No backend field assigned.

[3] 아침에 일어나니까
    No backend field assigned.

[4] 피부가 가려워
    discomfort_presence      = reported
    discomfort_types         = itching
```

형태소 단위 경계에 지원 연결어미/문장부호 경계를 보완한다. Kiwi가 없는 일반 python에서도 같은 연결어미 분할을 사용한다. 원문 위치는 정확한 slice로 보존하며 공백만 경계에서 제거한다. 이 분할은 한국어 전체 구문 분석의 완성을 뜻하지 않는다. 마침표가 숫자 사이에 있으면 날짜/소수점 내부를 자르지 않는다.

`cos-agent/`에서 `uv run python poc/jev/test_jev_text.py`만 실행하면 영어 입력 프롬프트가 열린다. 기본 화면은 Jev가 선택한 원문 구절 아래에 **백엔드 필드명과 값**만 보여준다. 예:

```text
'피부가 당기고 각질이 늘었어.'
Jev -> discomfort_types = tightness, increased_scaling
```

`--json`은 현재 추출기의 백엔드 후보와 근거 메타데이터, `--app-json`은 현재 추출 결과의 앱용 전달 준비 상태, `--verbose`는 화면과 상세 추출 결과를 출력한다. 추가 질문은 필수 백엔드 필드를 기준으로 생성한다. 완성된 사용자 입력과 동일 원문/payload/계약 확인이 있어야 검증된 9키 payload를 생성하며 HTTP·저장은 비활성이다.

## 미언급과 실패 처리

백엔드가 받지 않는 임시 증상·강도·사용 상태 값은 기본 경로에서 반환하지 않는다. 제품 사용이나 정확한 증상 강도처럼 현재 계약 밖 정보는 피부 상태 필드로 억지 변환하지 않는다. 필요한 백엔드 확장은 [계약 검토](../../docs/backend-contract-review.md)의 제안으로 별도 합의해야 한다.

미언급을 unknown/not_asked로 채우지 않는다. Jev의 내부 선택지 `omit`은 반환할 근거가 없다는 보류 수단이며 백엔드 값이 아니다. 질문 ID의 c0/c1은 코드가 만든 chunk 식별자이며 payload 필드가 아니다. 실제 후보에는 백엔드 허용값만 들어간다. unknown/not_asked/user_refused도 해당 필드에 대한 직접 보고가 있어야 한다.

각 chunk의 6개 필드값을 Choice로 질문한다. discomfort_types는 현재 7개 허용값의 128개 부분집합 중 하나를 선택하고 실제 배열로 반환한다. API 요청은 최대 18질문(3 chunks)씩 묶는다. 입력은 2000자/16 chunks로 제한하며 초과 시 미평가로 남긴다. 점수 0.5 초과는 개발용 보류 기준이며 검증된 확률·승인이 아니다. 낮은 점수, 잘못된 응답, API 실패는 값을 확정하지 않는다. 서로 다른 chunk의 scalar 값이 다르면 임의로 최종 값을 고르지 않고 충돌로 보류한다. 불편 종류는 긍정 목록끼리만 합치고 명시적 빈 목록과 충돌하면 보류한다. 로컬 Jev 판정은 표시한 채 집계에서 제외된 필드는 not merged로 구분한다. 현재 불편으로 과거 민감 이력을 추정하지 않는다.

원문은 Jev에 전송된다. public 저장소의 개발 실험은 합성 데이터만 사용하며 source/evidence는 모델 내부 토큰 기여도를 뜻하지 않는다. 모델 판정 후보와 사용자 확인·서버 권한은 별개다.

## 과거 코드의 위치

`--legacy-poc`에서만 기존 중간 필드 기반 CLI 경로가 실행된다. 과거 코드와 diverse-v1 산출물은 재현용으로 남기며 현재 엔진 설계나 성능 평가로 사용하지 않는다. 기존 테스트의 CLI 재현 호출은 legacy=True를 명시하도록 변경했고, 원본 KB 테스트·감사·평가 기대값은 바꾸지 않았다.

## 검증 기록

chunk별 추출 전환 후 실험 전체 160 passed. 5개 chunk의 원문 slice, Kiwi 없는 환경의 분할, 각 chunk별 독립 질문, 무배정 chunk의 화면 표시, chunk 간 충돌 보류를 추가로 검증했다. 대화에서 제공된 테스트 문장의 실제 Jev 실행에서도 5개 chunk와 각 필드 배정을 확인했다. 앞의 제품 사용/시각 구절 3개는 무배정으로 표시됐고 건조/가려움 구절은 각각 피부 상태 필드로 배정됐다. 결과는 ignored outputs/per-chunk-backend-fields.json에 있다. 원문 테스트 문장은 public 예제/테스트에 복사하지 않고 합성 제품명으로 경계 테스트를 작성했다. 아래 실행 기록은 chunk별 전환 전의 개발 이력이다.

실험 테스트 157 passed. 기본 실행에서 기존 classify/extract_features 및 임시 필드 설정 파일이 사용되지 않음, Jev 질문 필드가 백엔드 계약에 한정됨, 배열 값·누락·거절·실패·근거·필드 간 충돌·입력 제한·버전 불일치를 검사했다. 실제 Jev 합성 입력 6개를 실행하고, 다른 필드로 모름/부정이 번지는 초기 오판을 확인해 필드별 시제·대상·근거 질문을 수정했다. 해당 3개 입력을 재실행하여 반복/변화·현재 불편 부정·과거 이력 모름이 각각 해당 백엔드 필드만 반환하는 것을 관찰했다.

초기 실행과 재확인은 ignored `outputs/direct-backend-fields.json`, `outputs/direct-backend-fields-recheck.json`에 각각 남아 있다. 이 결과는 개발 사례 관찰이며 독립 평가·실제 사용자 적용·배포/저장 완료가 아니다. 기존 다양한 입력 성능 수치는 이 새 엔진에 적용하지 않는다.
