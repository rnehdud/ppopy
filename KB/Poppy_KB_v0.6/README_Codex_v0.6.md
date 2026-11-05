# Poppy KB v0.6 — Codex 인계

## 먼저 읽기

`Poppy_KB_분류표_v0.6.md`에서 전체 위치를 보고, `Poppy_KB_변경사항_v0.6.md`에서 새 범위를 확인한다. `Poppy_KB_seed_v0.6.json`이 전체 구조화 명세이고 `Poppy_KB_지식구조_v0.6.md`는 사람이 검토하는 전체 문서다.

`Poppy_KB_규정근거_v0.6.json/.md`는 첨부 **2024년판**의 선택 근거와 원문을 담은 별도 뷰다. 2026년 최신 개정의 존재/요지는 확인했으나 현행 전문 대조는 끝나지 않았다. 현재 법률 판정으로 실행하지 말 것.

## 주요 데이터 진입점

- `baseline_cards`: 60개의 조건부 기본 권장 상태. 원본은 ID별 한 번만 저장.
- `rule_taxonomy`, `category_views`: 9개 대분류와 소분류/참조.
- `lifecycle_taxonomy`, `lifecycle_views`: 기능과 독립된 7개 사용 단계.
- `combination_policy`: 레티노이드/AHA/살리실릭애씨드 별도 제품 병용 기본 비권장. 실제 역할·부위·시간·복합 완제품·진료계획 구분.
- `commerce_contract`: 공식/확인 가능한 실제 판매자 선호, 정품·품질·개인 적합성 분리. 실제 조회/인증 기능 아님.
- `regulatory_rules`, `allergen_label_dictionary`, `regulatory_source_pages`: 2024 원문 및 선택 조건. 현행 판정 비활성.
- `regulatory_version_contract`: 최신 공고 확인 범위 및 대조 미완료 작업.
- `input_policy`, `acquisition_items`: 기존 정보를 재사용하고 필요한 항목만 질문. 목록 전체가 설문이 아님.

## 검증 실행

Python 3.10 이상, 외부 패키지 불필요.

```bash
python validate_poppy_kb_v0_6.py
```

선택한 파일과 보고서 위치를 지정할 수 있다.

```bash
python validate_poppy_kb_v0_6.py Poppy_KB_seed_v0.6.json --report check.json
```

이 스크립트는 정적 참조 검사와 작은 참고함수의 경계/분기 테스트다. `combination_reference`에 들어가는 역할과 부위는 이미 검토된 값이라는 가정이다. 실제 전성분/자연어 입력을 판별하는 모델이나 제품 추천 엔진이 아니다. `acceptance_scenarios`는 아직 실행되지 않은 별도 명세이며 통과한 실험 결과로 보고하지 말 것.

## 배포·데이터 경계

모든 카드·정책의 운영 활성화는 꺼져 있다. 이 파일 전달은 앱 배포, 기존 저장소 변경, 사용자의 민감정보 외부 전송, AFA 학기 연구 데이터 결합을 승인하는 것이 아니다. 일반 성인 얼굴 및 제한적 손 관리 범위를 제모/염모/영유아 법정 조항 때문에 자동 확대하지 말 것.

## 출처 처리

원문·기관 안내·사용자 기본값·서비스 추론을 구분한다. 근거 없이 농도·pH·흡수율·개인 자극확률·정품확률·제조업자 점수를 생성하지 않는다. 첨부 원문을 현재 법령이나 작성자의 숨은 의도로 바꿔 기록하지 않는다.
