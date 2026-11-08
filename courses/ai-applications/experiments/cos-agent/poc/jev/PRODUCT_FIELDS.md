# 제품 chunk → 기존 제품 검색 계약

현재 엔진은 피부 상태와 제품을 별도 백엔드 계약으로 처리한다. `skin-state-extraction-1.2`의 `candidate_skin_state`는 기존 6개 피부 상태 필드만 포함한다. 제품은 `product_queries`에서 `product_name`과 기존 검색 요청을 별도로 준비한다. 원문 chunk 순서는 유지한다.

## 확인한 기존 계약

- [frontend/src/careApi.ts](https://github.com/rnehdud/SkinAnalysis/blob/main/frontend/src/careApi.ts), 읽은 blob `0166b922b4e60aac9917dc70c830abf9dfd139a5`: searchProducts(query)는 GET `/api/v1/products?query=...`. 제품 처리 요청은 별도 POST `/api/v1/products/resolution`의 `{product_name}`. 이번 구현에서는 POST를 호출하지 않는다.
- [skin_engine/consumer_api.py](https://github.com/rnehdud/SkinAnalysis/blob/main/skin_engine/consumer_api.py), 읽은 blob `54fd1c2a4a3e3876a40376aeb0183583cae9de8f`: `search_catalog_products`는 auto_confirmed=false와 candidates를 반환한다. 후보에는 product_id, brand, name, option, ingredient_evidence_status 등이 있다. product_version은 응답의 보장 필드가 아니다.
- [skin_engine/product_entry.py](https://github.com/rnehdud/SkinAnalysis/blob/main/skin_engine/product_entry.py), 읽은 blob `ea3513f42caefb72e05f70267820a006f6b185cb`: 완전한 이름의 유일 후보도 SKU 자동 확정이 아니며, routine_observation은 confirmed product IDs와 정확히 대응해야 한다.

위 소스는 읽기만 했고 배포 API에 연결하지 않았다. 별도 DB 테이블이나 피부 상태 필드를 추가하지 않는다. 제품 이름 선택을 사용·보유·빈도 보고의 확정으로 해석하지 않는다.

## 처리

1. 코드의 명사/원문 span 생성기를 사용해 chunk별 이름 선택지를 만든다. 이는 어휘 경계 도구 재사용이며 과거 증상/사용 사건 스키마를 재활성화하는 것이 아니다.
2. Jev는 각 chunk의 product_name을 원문 선택지에서 고른다. 브랜드·종류를 보존하고 조사·동사·시간을 제외한다. 한 chunk에 여러 제품이 있으면 겹치지 않는 범위에서 최대 4회 선택한다. chunk당 후보 범위는 최대 96개이며 한도·API 실패는 product_warnings에 남긴다.
3. 일반 종류만 있거나 특정 이름이 없으면 omit. 낮은 점수의 이름은 withheld로 표시하고 검색 요청을 만들거나 실행하지 않는다. 점수 기준은 개발용이며 사용자 확인을 대신하지 않는다.
4. 유효한 이름을 GET `/api/v1/products`의 query 파라미터에 대응한다. 이름을 product_id로 대입하지 않는다. 부정·계획·타인·정정 속 이름도 검색 후보일 뿐 실제 사용으로 확정하지 않는다.

## 기본 카탈로그 fallback

사용자 요청에 따라 실제 카탈로그 연결 전까지 기본값은 `PendingProductSearch`다. 외부 API/DB를 호출하지 않고 `lookup_status=fallback_pending`, candidates=[], product_id=null, product_version=null을 유지한다. 빈 candidates는 실제 검색 결과 0건을 뜻하지 않는다. 실제 검색이 실행된 no_match와 구분한다.

기본 화면 예시(합성):

```text
[1] A클렌저로 세안을 하고
    product_name             = A클렌저
    catalog_search.query     = A클렌저
    catalog_match            = fallback_pending
```

피부 상태에 관한 chunk는 동일 화면에 기존 6개 필드로 표시한다. 제품 정보를 skin_state payload에 섞지 않는다. `--app-json`에서도 product_queries는 별도이며 source/score는 제외한다. 후보는 사용자 확인 전 상태이고 어떤 경우에도 보유품 등록·실제 사용 기록을 저장하지 않는다.

## 나중에 연결할 지점

`extract_skin_state(text, key, product_lookup=callback)`에 기존 서버 검색 함수를 주입하면 된다. callback 입력은 제품 검색어 문자열, 출력은 기존 auto_confirmed=false/candidates envelope다. `ProductSearchClient`는 명시적 HTTPS origin에서 고정 GET 경로만 호출하며 redirect를 따르지 않고 timeout=10초를 사용한다. 주소는 앱 설정에서 제공하며 Jev가 결정하지 않는다.

향후 합성 TEST 서버에서 CLI 연결을 검증할 때만 다음과 같이 지정할 수 있다.

```powershell
uv run python poc/jev/test_jev_text.py --product-api-base https://your-test-backend.example
```

현재는 이 옵션 없이 fallback을 사용한다. 실사용/운영 수집을 활성화하지 않는다. 검색 응답의 자동 확정, 잘못된 ID·필드·evidence 상태·중복 ID는 거부한다. 유일 후보여도 product_id/version을 자동 선택하지 않는다. 제품 버전 확인, 사용자 선택 UI, 인증·보유품 등록은 기존 앱에서 별도로 통합해야 한다. ingredient_evidence_status는 제품 식별 확인이나 개인 적합성의 승인이 아니다.

## 검증

실험 전체 174 passed, 확장/현재 명세 371 passed, source manifest 27/27 및 KB 구조 95/95를 확인했다. 원본 감사의 기존 5개 불일치는 그대로 남아 있다. 제품 경로와 피부 상태 payload 분리도 통합 테스트로 확인했다.

Jev를 실제 실행해 제공된 테스트 문장의 두 제품 이름이 각각의 chunk에서 추출되는 것을 관찰했다. 원문은 public 예제에 복사하지 않고 ignored outputs/per-chunk-product-search.json에만 남겼다. 당시 검색은 연결되지 않은 상태였다. 이후 기본 상태를 명시적인 offline fallback_pending으로 변경했다. 테스트에서는 GET 경로/파라미터, 유일 후보 미확정, 낮은 점수의 검색 방지, 잘못된 응답·접속 실패, 기본 fallback의 네트워크 미호출을 검증한다. 실제 카탈로그 매칭 성공이나 DB 쓰기를 검증한 결과가 아니다.
