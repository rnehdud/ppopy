# Jev → 피부 상태 저장 전 매핑 검토

합성 데이터 전용 오프라인 검토 도구입니다. `relations-0.2`의 `symptoms`와 사람이 작성한 앱 `skin_state` JSON을 비교해 앱 계약 오류, 후보의 대상 필드·값, 확인이 필요한 항목과 직접 저장할 필드가 없는 정보를 표시합니다. 입력 원문·제품명·근거 구절을 출력하지 않고, 네트워크·DB·암호화·저장 기능은 없습니다. 출력은 승인이나 사용자 확인을 뜻하지 않습니다.

`cos-agent/`에서 Python 3.10+로 실행합니다. 외부 API나 패키지는 필요 없습니다.

```bash
python -m poc.jev.mapping_review.review poc/jev/mapping_review/examples/synthetic_jev.json poc/jev/mapping_review/examples/synthetic_skin_state.json
python -m pytest -q tests/test_jev_mapping_review.py
```

첫 입력은 Jev `--json`의 `relations-0.2` 객체 또는 `features`로 감싼 평가 결과입니다. 둘째는 앱의 피부 상태 객체 또는 `skin_state` 래퍼입니다. 파일·입력은 **합성 데이터만** 사용하세요. 스키마 오류면 종료 코드 1, 파일 또는 Jev 스키마 오류면 2입니다. 종료 코드 0은 계약 형식이 맞는다는 뜻이며 의미·현재 시점·사용자 확인·저장 권한은 별도 검토입니다. 결과의 `findings`에서 Jev의 인덱스와 제안된 값, 제출 후보에 포함됐는지를 확인합니다. 기존 데이터와 별도 질문에서 얻은 값이 있을 수 있어 미대응 입력은 오류가 아닌 확인 경고로 남깁니다.

- 긍정 + 본인으로 추출된 `stinging`, `itching`, `redness`만 각각 `stinging`, `itching`, `redness_tendency`의 **검토 후보**로 보여줍니다. 후보가 현재의 불편 반응인지와 표현이 정확한지는 사람이 확인해야 합니다. 모델 점수는 승인 기준이 아닙니다.
- 부정·타인·미상·모호는 존재한다고 쓰지 않습니다. 빈 목록은 증상이 없다는 뜻이 아닙니다. `dryness` 등은 단순 치환하지 않습니다.
- 증상별 강도·시작 날짜/시간·인지 시간은 현재 `skin_state`에 직접 대응하지 않아 표시만 합니다. 제품 ID·사용 이력 매핑, 사용자 확인 UI, 세션·동의, 저장·복호화는 범위 밖입니다.
- 구조화 입력에 없는 정보는 임의로 채우지 않습니다. `not_asked`, `unknown`, `user_refused`는 각 실제 상황에 맞게 작성합니다. 현재 계약은 자유 텍스트를 허용하지 않습니다.

## 기준과 한계

`contract.json`은 2026-11-08 SkinAnalysis 작업 트리의 `skin_engine/config/miray_skin_state.json`과 `skin_engine/miray_skin_state.py`에서 **피부 상태 필드·허용값만 발췌한 검토용 스냅샷**입니다. 원본 파일 SHA-256이 함께 기록되어 있습니다. 실제 배포 DB나 최신 계약을 조회한 결과가 아닙니다. 앱 계약이 바뀌면 원본과 대조해 갱신해야 합니다. 최종 저장 전에는 앱 서버의 `validate_skin_state`, 인증·민감정보 동의 및 기존 암호화 경로가 정본입니다. 이 도구를 서버 경로나 실제 사용자 데이터에 연결하지 않았습니다.
