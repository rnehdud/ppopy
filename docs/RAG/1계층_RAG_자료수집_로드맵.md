# 1계층 RAG 자료 수집·정리 로드맵

기준일 2026-11-24. 고정한 82개 작업의 자료 수집과 판정을 마감했다. [검수결과](1계층_준비/검수결과.json)에서 작업별 결과와 9개 분야의 남은 제약을 확인할 수 있다. 최초 계획의 분모와 작업 ID는 `1계층_준비/명세.json`과 `1계층_준비/고정_작업목록.jsonl`에 보존했다.

## 목적과 고정 범위

1계층은 관리 방향을 뒷받침하는 권고와 필수 적용 조건을 제공한다. 독성 평가·성분 사전·기전 자료는 2계층으로 연결하며 이 작업에서 대량 추가 수집하지 않는다. 제조사 선호는 사용자 승인 서비스 정책으로 표시하고, 검증된 제조 역량이 없는 회사의 이름을 외부 과학 근거로 삼지 않는다.

**총 82개 작업: 추가 원문 19개 + 카드별 근거 묶음 61개 + 통합 색인 1개 + 검수 1개.** 기존 v0.6.2 기준 카드 60개와 B-G18 보강판을 고정한다. 61개는 독립 과학 주장 개수가 아니며 한 카드에 복수 근거가 연결될 수 있다. 기존 Goal 214개와 별도이며 이 문서 작성으로 재개하지 않는다. 새 주제·신규 카드·제조사 비교연구 수집은 자동 추가하지 않는다.

## 1단계: 추가 원문 19개 확보

L1-S01~09를 먼저, S10~19를 다음으로 수행한다. 제목과 주소는 기존 KB 출처 등록부에서 고정했다. 새 URL로 이동하면 공식 리다이렉트 또는 공식 탐색 경로를 기록한다. 기존에 별도 사본이 발견되면 해시와 판본을 확인해 재사용한다.

| 작업 | 대상 | 기존 연결 카드 | URL |
|---|---|---|---|
| L1-S01 | S04 · Dermatologists’ top tips for relieving dry skin | B-M01, B-M02, B-G01, B-B01 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin) |
| L1-S02 | S35 · How to test skin care products | B-G11 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/test-skin-care-products/) |
| L1-S03 | S32 · How to safely exfoliate at home | B-G13, B-G14, B-G15, B-I04 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home) |
| L1-S04 | S06 · Shelf Life and Expiration Dating of Cosmetics | B-S01, B-S02, B-S03, B-S04 | [공식 출처](https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics) |
| L1-S05 | S27 · Microbiological Safety and Cosmetics | B-S03, B-S05, B-Q04, B-Q05, B-S07 | [공식 출처](https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics) |
| L1-S06 | S05 · Sunscreen: How to Help Protect Your Skin from the Sun | B-P02, B-P03, B-P06, B-P04, B-P08, B-S01, B-I01 | [공식 출처](https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun) |
| L1-S07 | S16 · Sunscreen FAQs | B-P01, B-P02, B-P03, B-P04 | [공식 출처](https://www.aad.org/media/stats-sunscreen) |
| L1-S08 | S17 · How do I know if I’m using the right sunscreen? | B-P06 | [공식 출처](https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen) |
| L1-S09 | S18 · When to toss your makeup and sunscreen | B-P08 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/replace-makeup-sunscreen) |
| L1-S10 | S20 · Dry, scaly, and painful hands could be hand eczema | B-G01, B-M04, B-G07 | [공식 출처](https://www.aad.org/public/diseases/eczema/types/hand-eczema) |
| L1-S11 | S21 · 4 skin care tips for your hands | B-G01, B-M04 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands) |
| L1-S12 | S23 · Hair removal: How to shave | B-S05, B-S06, B-G09, B-G10 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave) |
| L1-S13 | S24 · Razor bump remedies for men with darker skin tones | B-G07, B-S06, B-G09, B-G10, B-M05 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-basics/hair/razor-bump-remedies) |
| L1-S14 | S25 · Skin care tips for men | B-G10, B-M05 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men) |
| L1-S15 | S26 · Do facial masks work, and should I add one to my skin care routine? | B-G05, B-G07 | [공식 출처](https://www.aad.org/public/everyday-care/skin-care-secrets/routine/facial-masks-and-skin-care) |
| L1-S16 | S36 · Tips on how to spot counterfeit make-up and other fake cosmetic products | B-Q02, B-Q04, B-Q06 | [공식 출처](https://www.hpra.ie/safety-information/how-we-monitor-safety/cosmetics/how-we-monitor-the-safety-of-cosmetic-products/tips-on-how-to-spot-counterfeit-cosmetics) |
| L1-S17 | S38 · Are your hair care products causing breakouts? | B-L01 | [공식 출처](https://www.aad.org/public/diseases/acne/causes/hair-products) |
| L1-S18 | S39 · Is sports equipment causing your acne? | B-L03 | [공식 출처](https://www.aad.org/public/diseases/acne/causes/sports-equipment) |
| L1-S19 | S40 · Contact dermatitis | B-L01, B-L02 | [공식 출처](https://www.bad.org.uk/pils/contact-dermatitis) |

각 원문 작업은 다음 7개 항목을 갖춘다: ①제목/기관/문서유형 ②최종 URL·확인시각·게시/개정일 ③허용된 원문 또는 본문 파일과 SHA-256 ④관련 소제목/문단 위치 ⑤일반관리·질환별·검사/치료·제조사 안내 구분 ⑥대상자/제품/행동 범위 ⑦이용 조건과 확보 상태. 제목·링크만 있는 경우 `link_only`로 기록한다.

## 2단계: 기존 원문 재사용 및 61개 카드 근거 묶음

14개 기존 원문을 `1계층_준비/명세.json`의 경로·해시로 재사용한다: AAD 세안/보습제/도포/의료적 첩포검사/아토피 지침 소개, FDA 이상반응/알레르겐, NHS 불편·상담 참고, WHO/CDC 자외선 안내, NICE NG198 지침/근거검토, AAAAI·ACAAI 지침, NICE CG57 근거검토. 기존 AAD 후보 7개와 비타민 C 병용 근거 3개도 재작성 없이 대조·보강한다. 기존 연구는 카드에 직접 필요할 때 보유 전문·초록·검토 기록만 활용한다.

카드마다 다음 필드가 모두 있어야 해당 작업을 마감한다. 비해당은 이유를 적으며 빈값으로 통과시키지 않는다.

- `card_id`, `card_version`, 사용자 상황과 필요한 실제 입력
- 원문이 직접 뒷받침하는 권고와 서비스가 추가한 해석
- `basis_type`: external_guidance / service_policy / mixed / out_of_scope
- 대상자·질환/연령·부위·제품군·사용 조건과 적용 제외 조건
- 원문 파일·URL·판본·해시·정확한 절/문단 또는 페이지
- 원문→사본→요약 계보, 다른 근거와의 중복 여부
- 불확실성·상충·판단 보류 조건, 추가 질문과 제품자료 조회의 구분
- 확인자/시각과 `verification_status`, `layer1_eligible`, 사용권 상태

필수 특별 판정:

1. B-G11: 가정 소부위 사용 시험과 의료적 첩포검사 구분. AAD_첩포검사로 새 제품 사용 시험을 대체하지 않는다.
2. B-C04: pH 단독 우월성으로 일반화하지 않는다. Hawkins 본문 파일 미확보·검토 범위와 Bennett-Kennett 보유 본문을 구분한다.
3. B-I01: 선크림 제거 연구의 제품·내수성·비교조건을 보존. 초록만으로 모든 제품에 이중 세안을 의무화하지 않는다.
4. B-P05: 필터 물성 선호를 개인 눈시림 감소가 입증된 권고로 표시하지 않는다.
5. B-P07: 2026-11-24 제조 역량 정책을 적용. 과거 제조사 선호는 서비스 정책 이력이다. 대상 제품과 연결된 검증 근거가 없으면 회사별 우월성은 unknown이며 이 로드맵에서 제조사 연구를 추가 수집하지 않는다.
6. B-G13~15/B-G18: 제조사·의약품 지침과 일반 화장품 서비스 정책의 범위를 분리. 시간대 분리는 안전 보증 아님.
7. B-S01~07: 사용기한/개봉기간/보관/오염을 구분. 전 제품 공통 냉장·폐기기간을 만들지 않는다.
8. B-Q05: 회수 대응의 절차 근거와 실시간 제품/로트 회수 조회를 구분. 이번 작업은 회수 DB 전수 수집이 아니다.
9. 특정 질환·소아 임상지침은 적용 조건이 실제 입력으로 확인되는 경우의 근거로만 분류한다. 일반 얼굴관리 원칙으로 확대하지 않는다.

## 3단계: 통합 색인 1개 작업 (L1-I01)

산출물은 `1계층_준비/관리권고_근거.jsonl`, `카드별_근거연결.jsonl`, `사용제한_미확보.jsonl`이다. 검색 가능한 근거와 참고/제외 자료를 분리한다. 61개 카드 각각에 근거 연결 또는 외부 근거가 필요 없는 서비스 정책/적용 제외 사유가 있어야 한다. 내부 KB·Threads·요약문을 독립 외부 근거로 중복 인용하지 않는다. 안전·법령 조건은 관련 정본을 참조하되 이 작업에서 법령 전체 검증을 새로 수행하지 않는다.

## 4단계: 검수 1개 작업 (L1-V01)

- 19개 원문 작업과 61개 카드 작업의 ID 중복/누락 0건.
- 확보/재사용한 원문 경로 존재·해시 일치 100%, 근거와 카드의 끊어진 참조 0건.
- 기존 64개 수용 시나리오 각각에 관련 카드·근거 또는 서비스 정책 범위 연결. 기대 결과가 근거보다 강하면 충돌로 표시하고 원래 기대값을 몰래 수정하지 않는다.
- 기본 세안, 건조 관리, 광보호, 새 제품 도입, 사용 후 불편, 병용, 보관/위생, 면도/손/접촉 관리, 구매/회수의 9개 분야를 각각 ready/partial/blocked로 집계.
- `review_candidate`, 구판, 식별 충돌, 권리 미해결 자료가 직접 권고용으로 승격된 건수 0건.
- 최종 `검수결과.json`에 전체 작업 마감 수와 실제 1계층 사용 가능 근거 수를 따로 기록.

## 요청 제한과 종료 기준

작업당 최초에 RAG 경로·URL·해시를 대조한다. 원문이 없을 때 공식 URL 1회, 공식적으로 연결된 대체 경로 최대 2개까지만 확인한다. 같은 실패 URL은 반복 요청하지 않는다. CAPTCHA·401/403·429 등 접근제한 신호는 기존 정책에 따라 중단·기록하며 다른 경로로 우회하지 않는다. 재사용 권리가 명시적으로 제한되면 그 상태와 허용된 범위의 링크·메타데이터를 보존한다. 정책상 허용되는 별도 공개판의 탐색도 위 2개 대체 경로 한도에 포함한다.

원문 작업의 종료 상태: acquired / reused / link_only / unavailable. 카드 작업의 종료 상태: verified / policy_only / partial / excluded. 모든 상태에 사유와 확인 기록을 요구한다. partial·link_only·unavailable은 마감할 수 있으나 확보/검증 성공으로 세지 않는다.

**수집·정리 완료:** 82개 작업에 판정과 산출물이 있고 위 무결성 검수를 통과한 상태.
**1계층 자료 준비 완료:** 서비스가 외부 근거로 제시할 주장 모두가 검증된 근거에 연결되고, 미해결 주장은 검색 대상에서 제외 또는 명시적으로 보류된 상태. 서비스 정책을 과학적 검증으로 세지 않는다.

벡터 DB 생성, 실제 검색기의 필터 적용, LLM/AFA 통합 성능시험, 앱 배포는 이번 자료 수집 로드맵 밖이다. 자료 준비 완료가 운영 RAG 완성을 뜻하지 않는다. 실행 중 신규 주제가 발견되면 별도 backlog로 기록하고 이 82개 범위에는 합산하지 않는다.
