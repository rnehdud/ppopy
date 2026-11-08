# Jev → 피부 상태 저장 전 매핑 검토

합성 데이터 전용 오프라인 검토 도구입니다. `relations-0.2`~`relations-0.5`의 `symptoms`와 사람이 작성한 앱 `skin_state` JSON을 비교해 앱 계약 오류, 후보의 대상 필드·값, 확인이 필요한 항목과 직접 저장할 필드가 없는 정보를 표시합니다. `usage_events`는 별도 검토 결과로 출력합니다. 입력 원문·제품명·근거 구절을 출력하지 않고, 네트워크·DB·암호화·저장 기능은 없습니다. 출력은 승인이나 사용자 확인을 뜻하지 않습니다.

`cos-agent/`에서 Python 3.10+로 실행합니다. 외부 API나 패키지는 필요 없습니다.

```bash
python -m poc.jev.mapping_review.review poc/jev/mapping_review/examples/synthetic_jev.json poc/jev/mapping_review/examples/synthetic_skin_state.json
python -m pytest -q tests/test_jev_mapping_review.py
```

첫 입력은 Jev `--json`의 지원 버전 객체 또는 `features`/`result`로 감싼 평가 결과입니다. 둘째는 앱의 피부 상태 객체 또는 `skin_state` 래퍼입니다. 파일·입력은 **합성 데이터만** 사용하세요. 스키마 오류면 종료 코드 1, 파일 또는 Jev 스키마 오류면 2입니다. 종료 코드 0은 계약 형식이 맞는다는 뜻이며 의미·현재 시점·사용자 확인·저장 권한은 별도 검토입니다. 결과의 `findings`에서 Jev의 인덱스와 제안된 값, 제출 후보에 포함됐는지를 확인합니다. 기존 데이터와 별도 질문에서 얻은 값이 있을 수 있어 미대응 입력은 오류가 아닌 확인 경고로 남깁니다.

- 긍정 + 본인으로 추출된 `stinging`, `itching`, `redness`만 각각 `stinging`, `itching`, `redness_tendency`의 **검토 후보**로 보여줍니다. 0.3~0.5에서는 state/subject가 유효 candidate 또는 출처가 있는 rule_candidate인지도 검사합니다. unassessed/uncertain, 취소된 증상, 불확실한 정정은 제안값을 만들지 않습니다. candidate 점수는 추출기의 실험 기준(0.5 초과)을 따르며 승인 기준이 아닙니다. 후보가 현재의 불편 반응인지와 표현이 정확한지는 사람이 확인해야 합니다.
- 0.2 합성 예시처럼 판정 메타데이터가 없는 이전 자료는 검토만 가능하며 `legacy_assessment_metadata_may_be_missing` 경고를 표시합니다. 최신 버전의 메타데이터 누락을 이 예외로 허용하지 않습니다. 지원 목록 외 버전은 거부합니다.
- 부정·타인·미상·모호는 존재한다고 쓰지 않습니다. 빈 목록은 증상이 없다는 뜻이 아닙니다. `dryness` 등은 단순 치환하지 않습니다.
- 증상별 강도·시작 날짜/시간·인지 시간은 현재 `skin_state`에 직접 대응하지 않아 표시만 합니다. 사용 사건도 피부 상태 필드로 변환하지 않습니다. 사용자 확인 UI, 세션·동의, 저장·복호화는 범위 밖입니다.
- 구조화 입력에 없는 정보는 임의로 채우지 않습니다. `not_asked`, `unknown`, `user_refused`는 각 실제 상황에 맞게 작성합니다. 현재 계약은 자유 텍스트를 허용하지 않습니다.

## PoC 자동 후보 매핑

`test_jev_text.py`의 기존 실행에 매핑이 연결돼 있다. 추가 Jev 호출 없이 `extract_features()`가 `skin_state_mapping`을 생성하고, 기본 화면에는 SKIN STATE MAPPING 카드, `--json`에는 전체 후보 객체가 표시된다. 독립 검토 CLI도 그대로 사용할 수 있다.

`cos-agent/`에서:

```powershell
uv run python poc/jev/test_jev_text.py "나는 피부가 따갑고 가려워." --json
```

예시 출력의 추가 블록(일부):

```json
{
  "skin_state_mapping": {
    "skin_state_patch": {
      "discomfort_presence": "reported",
      "discomfort_types": ["stinging", "itching"]
    },
    "confirmation_status": "pending",
    "complete_payload": false,
    "authorized_for_storage": false
  }
}
```

- `skin_state_patch`는 완전한 skin_state 객체가 아닌 **부분 후보**다. version은 target_version에 별도로 기록한다. kind·observed_at·지속성·변화·민감 이력 등은 원문에서 구현된 추출이 없으므로 자동으로 채우지 않고 missing_fields에 남긴다. 현재 시각을 관찰 시각으로 넣거나 not_asked를 임의 부여하지 않는다.
- candidates의 symptom_index는 원본 symptoms 배열을 가리키며 확인 전까지 원문 revision과 함께 관리한다. 같은 discomfort 종류는 patch에서 중복 제거하되 후보 근거 인덱스는 모두 남긴다. reported는 해당 후보 목록에서 파생된 제안값이다.
- 기존 검토 규칙을 공유해 따가움/가려움/붉어짐의 유효한 본인 긍정 보고만 제안한다. 건조함·트러블·강도 등은 대응 가능한 피부 상태 값으로 추정하지 않고 findings에 남긴다. 빈 patch는 무증상이 아니다.
- 추출 warning, 전역 증상 정보 거절, 판정 메타데이터가 부족한 이전 0.2 입력은 blockers로 표시하고 patch를 생성하지 않는다. 같은 종류의 유효한 긍정/부정·미상·충돌 보고가 공존하면 시간과 상태 확인 전 해당 종류를 제안하지 않는다.
- 사용 사건은 usage_event_findings로 분리한다. 제품 사용으로 피부 불편이나 개선 상태를 생성하지 않는다. patch를 DB에 직접 전달하지 않고, 앱에서 후보와 관찰 문맥을 확인하고 빠진 필드를 보완한 뒤 완성된 객체를 기존 서버 validate_skin_state로 검증해야 한다. 확인 UI·서버 저장 연결은 미구현이다.

2026-11-08 검증: 실험 전체 122 passed. 기존 CLI를 실제 Jev로 합성 입력 3개에 실행하여 (1) 따가움+가려움 후보와 아침 사용/저녁 미사용 분리, (2) 따가움 부정의 빈 patch, (3) 건조함의 빈 patch를 확인했다. 산출물은 ignored `outputs/poc-skin-state-mapping/`에 있다. 모두 authorized_for_storage=false이며 DB 쓰기나 실제 사용자 데이터는 사용하지 않았다. 외부 모델의 일반 정확도를 검증한 결과는 아니다.

## 사용 사건 검토 출력

출력은 `mapping-review-0.2`이며 `source_schema_version`을 기록합니다. 증상 결과 `findings`와 사건 결과 `usage_event_findings`는 서로 별도입니다.

- 사건의 state/subject/correction/product_link를 각각 검사합니다. 추출기의 eligible 플래그를 저장 권한으로 신뢰하지 않습니다.
- 본인의 유효한 실제 사용 보고는 `actual_use_report_requires_confirmation_and_separate_contract`로 표시합니다. 계획·부정·타인·취소·미평가는 실제 사용으로 표시하지 않습니다.
- 구버전의 relations 없는 사건은 `legacy_or_malformed_event_requires_review`입니다. 대표 제품의 상태를 가져와 채우지 않습니다.
- 모든 사건의 `target=null`, `authorized_for_storage=false`를 유지합니다. 별도 사용 사건 계약, 제품 ID/version 확인, 시간 정밀도 검토, 사용자 확인 및 서버 권한 검증이 필요합니다. DB의 저장 위치나 암호화 payload 형식을 확정하지 않습니다.
- 원문·시간 span·제품명·제품 ID는 검토 출력에 복사하지 않습니다. 이벤트는 입력 배열의 인덱스로 찾습니다. 알 수 없는 증상 enum은 내용을 그대로 출력하지 않습니다.

예를 들어 아침 사용/저녁 미사용은 별도 사건 두 개로 검토되지만, 피부 상태에 `discomfort_types`를 추가하지 않습니다. 제품 사용만으로 증상이나 피부 개선을 추론하지 않습니다.

실행 예시(추출기는 별도 Jev 호출을 사용하므로 합성 문장만 사용):

```powershell
python poc/jev/test_jev_text.py "A로션을 아침에 썼고 저녁에는 안 썼어." --json > synthetic-events.json
python -m poc.jev.mapping_review.review synthetic-events.json poc/jev/mapping_review/examples/synthetic_skin_state.json
```

출력 파일의 인코딩은 UTF-8을 사용하세요. 위 두 단계 중 검토 명령 자체는 오프라인이며 합성 skin_state는 사용자가 확인한 실제 상태를 뜻하지 않습니다. 통합 테스트는 API 실패 경로에서도 미평가 사건이 제안·저장으로 승격되지 않는지 확인합니다.

2026-11-08 로컬 검증: 실험 전체 106 passed. 지원 버전·최신 판정 메타데이터·구버전 경고·미평가/불확실/정정·사용/미사용/계획/타인·출력 원문 제외·CLI 래퍼·현재 추출기의 API 실패 통합 경로를 확인했다. 이전 실제 Jev 실행에서 생성한 합성 relations-0.5 결과로도 아침 affirmed/저녁 denied의 별도 검토 결과를 확인했다. 신규 실제 사용자 데이터나 DB 쓰기는 사용하지 않았다.

## 앱 계약의 출처

`contract.json`은 2026-11-08 SkinAnalysis 작업 트리의 `skin_engine/config/miray_skin_state.json`과 `skin_engine/miray_skin_state.py`에서 **피부 상태 필드·허용값만 발췌한 검토용 스냅샷**입니다. 원본 파일 SHA-256이 함께 기록되어 있습니다. 실제 배포 DB나 최신 계약을 조회한 결과가 아닙니다. 앱 계약이 바뀌면 원본과 대조해 갱신해야 합니다. 최종 저장 전에는 앱 서버의 `validate_skin_state`, 인증·민감정보 동의 및 기존 암호화 경로가 정본입니다. 이 도구를 서버 경로나 실제 사용자 데이터에 연결하지 않았습니다.
