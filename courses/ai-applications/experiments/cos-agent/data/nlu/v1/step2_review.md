# NLU Step 2 980턴 — 원문·예상 후보·작성 근거

독립 Critic·사람 승인 결과가 아니라 합성 작성본 대조표예요. 모든 후보는 미확정이에요.

## nlu-step2-0001 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 0

### 원문 raw

얼굴만 씻어요. 물은 미지근해요. 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴만 씻어요. 물은 미지근해요. 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `af2bac2e0a4b575273a3f55f822ed1587f231da315d633c7b59a5f5f2c357227`

## nlu-step2-0002 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 1

### 원문 raw

세안 부위는 얼굴이에요, 물은 미지근해요, 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 부위는 얼굴이에요, 물은 미지근해요, 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 부위는 얼굴이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7a8b6f37917847161069d00c1e3008a5b04158b291f26335d40c69a44951d1a3`

## nlu-step2-0003 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 2

### 원문 raw

얼굴 씻는 얘기예요
물은 미지근해요
세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴 씻는 얘기예요\n물은 미지근해요\n세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `2a55c5e03a5f4bc96cabe251463e3d35251dbfdaeb4d0fa053264df46b5358a7`

## nlu-step2-0004 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 3

### 원문 raw

얼굴만 씻어요. 미지근한 물 써요. 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴만 씻어요. 미지근한 물 써요. 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7f557a009a4d6f7f9c8bb44e26815a605166c544f23e0df4004927b0526efb67`

## nlu-step2-0005 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 4

### 원문 raw

세안 부위는 얼굴이에요 그리고 미지근한 물 써요 그리고 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 부위는 얼굴이에요 그리고 미지근한 물 써요 그리고 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 부위는 얼굴이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `dd5e5267b60095ee478b02019c5f20bd9d8d5b4ff8cd9832dad7b14fa14a7cf7`

## nlu-step2-0006 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 5

### 원문 raw

얼굴 씻는 얘기예요, 미지근한 물 써요, 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴 씻는 얘기예요, 미지근한 물 써요, 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `ef6b57bbfd7a4b7ef1e5ba666d4e0d0cc6d2fa677524f13de358e4c30e08e87a`

## nlu-step2-0007 · turn1_utterance · train

의미 가족: `nlu-step2-face_warm_hand` / 표현 변형: 6

### 원문 raw

얼굴만 씻어요 / 물 온도 미지근함 / 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴만 씻어요 / 물 온도 미지근함 / 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d574048894faf905d83631c1dc27570bbbb0911a26b1c687786f691f58fc7b62`

## nlu-step2-0008 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 0

### 원문 raw

몸을 씻어요. 찬물 써요. 도구는 세정용 천이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몸을 씻어요. 찬물 써요. 도구는 세정용 천이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세정용 천이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `ab3318c5f22a91a186e395295ea5317651ef2deeab3e4abceb77a51e2c3add6a`

## nlu-step2-0009 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 1

### 원문 raw

몸 씻는 얘기예요, 찬물 써요, 도구는 세정용 천이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몸 씻는 얘기예요, 찬물 써요, 도구는 세정용 천이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세정용 천이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `2711f477cc518fb64c88a356cdc0d3d37054c7dbe1e1574cdc2e4989d30c334c`

## nlu-step2-0010 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 2

### 원문 raw

이번 세정 부위는 몸이에요
찬물 써요
도구는 세정용 천이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이번 세정 부위는 몸이에요\n찬물 써요\n도구는 세정용 천이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이번 세정 부위는 몸이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세정용 천이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `47369c22a5fa590d2e4659be382615816765560e020c88774b32858a1844f288`

## nlu-step2-0011 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 3

### 원문 raw

몸을 씻어요. 물은 차가워요. 씻을 때 세정 천을 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몸을 씻어요. 물은 차가워요. 씻을 때 세정 천을 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때 세정 천을 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `a90baef99473619e54c83e2d1f821dc67d5b18a14be98301399771df72ea950f`

## nlu-step2-0012 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 4

### 원문 raw

몸 씻는 얘기예요 그리고 물은 차가워요 그리고 씻을 때 세정 천을 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몸 씻는 얘기예요 그리고 물은 차가워요 그리고 씻을 때 세정 천을 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때 세정 천을 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9a24e23e533d58bc482068dbc1cee6b575166d9af3dbaf847d94dd544ecd7b60`

## nlu-step2-0013 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 5

### 원문 raw

이번 세정 부위는 몸이에요, 물은 차가워요, 씻을 때 세정 천을 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이번 세정 부위는 몸이에요, 물은 차가워요, 씻을 때 세정 천을 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이번 세정 부위는 몸이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때 세정 천을 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9837447086bf1c2f5a177d68a3d82af4e12fcb2b8b0d28f0331bd3c6d5eca0b8`

## nlu-step2-0014 · turn1_utterance · train

의미 가족: `nlu-step2-body_cold_cloth` / 표현 변형: 6

### 원문 raw

몸을 씻어요 / 차가운 물로 해요 / 세정용 천으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몸을 씻어요 / 차가운 물로 해요 / 세정용 천으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차가운 물로 해요"
    },
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정용 천으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5d68924cec5bdcde02804c8c0b089941708eef73c783e1224ae06bc32e758607`

## nlu-step2-0015 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 0

### 원문 raw

세안 브러시 써요. 세게 문질러요. 수건으로 물기를 박박 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 브러시 써요. 세게 문질러요. 수건으로 물기를 박박 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 물기를 박박 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `45361dd9e89905154946c081b8374ea41d20c5b7d3cf816bd5408e2baaf9b194`

## nlu-step2-0016 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 1

### 원문 raw

도구는 세안용 브러시예요, 세게 문질러요, 수건으로 물기를 박박 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구는 세안용 브러시예요, 세게 문질러요, 수건으로 물기를 박박 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세안용 브러시예요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 물기를 박박 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `3952dbf74cfab124553e68c11f803874e3b77e7c78bd8b5aa513318c1725908b`

## nlu-step2-0017 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 2

### 원문 raw

브러시로 세안해요
세게 문질러요
수건으로 물기를 박박 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시로 세안해요\n세게 문질러요\n수건으로 물기를 박박 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "브러시로 세안해요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 물기를 박박 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `27133ac29459c661f9bc467077a2043d67643cafcb440022c1dc1ba95278daf4`

## nlu-step2-0018 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 3

### 원문 raw

세안 브러시 써요. 문지르는 힘이 세요. 물기 닦을 때 세게 문질러요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 브러시 써요. 문지르는 힘이 세요. 물기 닦을 때 세게 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르는 힘이 세요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 때 세게 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6eb55cf3a7887a2cde3268b91c22b4364612222b2181361830ef87c64baf928d`

## nlu-step2-0019 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 4

### 원문 raw

도구는 세안용 브러시예요 그리고 문지르는 힘이 세요 그리고 물기 닦을 때 세게 문질러요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구는 세안용 브러시예요 그리고 문지르는 힘이 세요 그리고 물기 닦을 때 세게 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세안용 브러시예요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르는 힘이 세요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 때 세게 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4055cb452460316c370891d02efe848818dec1d7c2564512f4b799d4d49e9328`

## nlu-step2-0020 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 5

### 원문 raw

브러시로 세안해여, 문지르는 힘이 세요, 물기 닦을 때 세게 문질러요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시로 세안해여, 문지르는 힘이 세요, 물기 닦을 때 세게 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "브러시로 세안해여"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르는 힘이 세요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 때 세게 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9a9e370317a346ae042ec9ed642d3b20a68675f03b8c816b7301f513487c49aa`

## nlu-step2-0021 · turn1_utterance · train

의미 가족: `nlu-step2-brush_force` / 표현 변형: 6

### 원문 raw

세안 브러시 써요 / 박박 문질러요 / 물기는 수건으로 세게 비벼 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 브러시 써요 / 박박 문질러요 / 물기는 수건으로 세게 비벼 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "박박 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기는 수건으로 세게 비벼 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8e174db2a776daec6f9bf83153480b9140df6d06f1e1726cda2b5add94bd98b2`

## nlu-step2-0022 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 0

### 원문 raw

스펀지로 씻어요. 살살 문질러요. 물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "스펀지로 씻어요. 살살 문질러요. 물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지로 씻어요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `e2b97c4c3c0bc2a7328548b010d116f39875bca8b8e04058dae55561ee4648ce`

## nlu-step2-0023 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 1

### 원문 raw

세정 도구로 스펀지 써요, 살살 문질러요, 물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정 도구로 스펀지 써요, 살살 문질러요, 물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구로 스펀지 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `2fb40c6ae7c152032c4d42982eb077ab75b1e583436c661f76c2d6f5df7becd4`

## nlu-step2-0024 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 2

### 원문 raw

스펀지를 세정에 써요
살살 문질러요
물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "스펀지를 세정에 써요\n살살 문질러요\n물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지를 세정에 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d4b8c3807dffad72ccb71dc9a3cf4e1ada27cb0576d50e96afed892908e96240`

## nlu-step2-0025 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 3

### 원문 raw

스펀지로 씻어요. 문지를 때 힘 약하게 줘요. 문지르지 않고 물기를 톡톡 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "스펀지로 씻어요. 문지를 때 힘 약하게 줘요. 문지르지 않고 물기를 톡톡 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지로 씻어요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르지 않고 물기를 톡톡 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `f7db9746c6b1484a6daaf283e507f9c6d700ae01044918b317005e5fc14639de`

## nlu-step2-0026 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 4

### 원문 raw

세정 도구로 스펀지 써요 그리고 문지를 때 힘 약하게 줘요 그리고 문지르지 않고 물기를 톡톡 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정 도구로 스펀지 써요 그리고 문지를 때 힘 약하게 줘요 그리고 문지르지 않고 물기를 톡톡 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구로 스펀지 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르지 않고 물기를 톡톡 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5e160452a307090fb6cb7678af1443b43c6bb688851c613fb1c654db8ef50e3e`

## nlu-step2-0027 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 5

### 원문 raw

스펀지를 세정에 써요, 문지를 때 힘 약하게 줘요, 문지르지 않고 물기를 톡톡 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "스펀지를 세정에 써요, 문지를 때 힘 약하게 줘요, 문지르지 않고 물기를 톡톡 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지를 세정에 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르지 않고 물기를 톡톡 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `30213ae5b30d5e96ed46cfef9ff6f0b45fd319438992d9b6d4d3076682fad3cf`

## nlu-step2-0028 · turn1_utterance · train

의미 가족: `nlu-step2-sponge_gentle` / 표현 변형: 6

### 원문 raw

스펀지로 씻어요 / 문지르는 힘은 약해요 / 물기는 톡톡 두드려 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "스펀지로 씻어요 / 문지르는 힘은 약해요 / 물기는 톡톡 두드려 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지로 씻어요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르는 힘은 약해요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기는 톡톡 두드려 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `ad93929817ab69182b384feea0759aaec3e9cd06523360f8178bd82d1a1f212b`

## nlu-step2-0029 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 0

### 원문 raw

씻기 전에 피부를 물로 적셔요. 마무리는 물로 헹궈요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 전에 피부를 물로 적셔요. 마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 전에 피부를 물로 적셔요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d22acbb1d9a372b7912f6fc99d8e33f4053ddeba6db82532a458a0248376f27c`

## nlu-step2-0030 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 1

### 원문 raw

씻기 전 피부가 젖어 있어요, 마무리는 물로 헹궈요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 전 피부가 젖어 있어요, 마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 전 피부가 젖어 있어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `01a8d4f03d28b3216d5078dc01076d96fd1ff5bb4a6ecf1b3909595b2b617502`

## nlu-step2-0031 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 2

### 원문 raw

피부를 적신 상태에서 씻어요
마무리는 물로 헹궈요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부를 적신 상태에서 씻어요\n마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부를 적신 상태에서 씻어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `16ae92f7e1ae478e558ebf2af8242900b0d8d3127c9e6d6576faeb7191bdd475`

## nlu-step2-0032 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 3

### 원문 raw

씻기 전에 피부를 물로 적셔요. 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 전에 피부를 물로 적셔요. 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 전에 피부를 물로 적셔요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `88cf7eec33a14b2e612dac23436c8dbddccdc57638b9005d4ce428294e2da5cb`

## nlu-step2-0033 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 4

### 원문 raw

씻기 전 피부가 젖어 있어요 그리고 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 전 피부가 젖어 있어요 그리고 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 전 피부가 젖어 있어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `0ffdddb871a08adbd2ebcfa0d444940ddc9df04b9659f0308e61e875ea175a5b`

## nlu-step2-0034 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 5

### 원문 raw

피부를 적신 상태에서 씻어여, 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부를 적신 상태에서 씻어여, 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부를 적신 상태에서 씻어여"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4f7a5d471cea383e7326a53182ebdde1744edb8f576f356551975bcd48532480`

## nlu-step2-0035 · turn1_utterance · train

의미 가족: `nlu-step2-wet_rinse` / 표현 변형: 6

### 원문 raw

씻기 전에 피부를 물로 적셔요 / 끝에는 물 헹굼 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 전에 피부를 물로 적셔요 / 끝에는 물 헹굼 해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "젖은 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 전에 피부를 물로 적셔요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `f7129c2554518b680dc01aa603591c5c08fa63e9e9ed912d5fd4d9549be3e66f`

## nlu-step2-0036 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 0

### 원문 raw

피부가 마른 상태로 씻기 시작해요. 세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부가 마른 상태로 씻기 시작해요. 세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5b096241236ccfde2064a1d854ca6f5b6835614572c2b61d7ec5e4577d18dde3`

## nlu-step2-0037 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 1

### 원문 raw

씻기 시작할 때 피부는 말라 있어요, 세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 시작할 때 피부는 말라 있어요, 세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `be6d8b4a7c70bc9342daca2533a71ecbe268b73783c4ce223174cfe44088c373`

## nlu-step2-0038 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 2

### 원문 raw

물 적시기 전에 씻기 시작해요
세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 적시기 전에 씻기 시작해요\n세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 적시기 전에 씻기 시작해요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c9c639053544fe00b783a142bdc6cb5c306ac09ed6c4163ece180c3d470665c1`

## nlu-step2-0039 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 3

### 원문 raw

피부가 마른 상태로 씻기 시작해요. 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부가 마른 상태로 씻기 시작해요. 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6e68fc2fb2c2f9f7737d53da8933b070d09edbbbebc36598eea8b87a897c5084`

## nlu-step2-0040 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 4

### 원문 raw

씻기 시작할 때 피부는 말라 있어요 그리고 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻기 시작할 때 피부는 말라 있어요 그리고 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4bf44ba9e38efdd8e10bde479206880a0957f51cbda3ff9596a9a1fe7f43fe96`

## nlu-step2-0041 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 5

### 원문 raw

물 적시기 전에 씻기 시작해여, 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 적시기 전에 씻기 시작해여, 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 적시기 전에 씻기 시작해여"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `0057de6fbb0e42cfd93c72cf5e8894fec35627ad4c1c06c39af3787d88d50c88`

## nlu-step2-0042 · turn1_utterance · train

의미 가족: `nlu-step2-dry_mix` / 표현 변형: 6

### 원문 raw

피부가 마른 상태로 씻기 시작해요 / 두 세정제를 손바닥에서 혼합해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부가 마른 상태로 씻기 시작해요 / 두 세정제를 손바닥에서 혼합해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 세정제를 손바닥에서 혼합해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `3a27efeb7085c84e1ea820576403424240c4ad75ee0a6e13075b65f880642e38`

## nlu-step2-0043 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 0

### 원문 raw

지워야 할 색조 화장이 있어요. 두 번 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지워야 할 색조 화장이 있어요. 두 번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지워야 할 색조 화장이 있어요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `83f6f31e10625cf414ac5c8dd1d8449ff309f05e1be0f20746660538024729f2`

## nlu-step2-0044 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 1

### 원문 raw

제거할 메이크업이 남아 있어요, 두 번 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제거할 메이크업이 남아 있어요, 두 번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제거할 메이크업이 남아 있어요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `068bfa0e06fa7e245231cc99e868d2780e50a896d51358eb604fba52b3ebf5f2`

## nlu-step2-0045 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 2

### 원문 raw

세정 대상은 색조 화장이에요
두 번 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정 대상은 색조 화장이에요\n두 번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 대상은 색조 화장이에요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `bb2ff0ad4a5d2bd1cffa2d9743d161ba3176aba56f28397934c440645fe6a647`

## nlu-step2-0046 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 3

### 원문 raw

지워야 할 색조 화장이 있어요. 세안은 두 차례예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지워야 할 색조 화장이 있어요. 세안은 두 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지워야 할 색조 화장이 있어요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안은 두 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5ef162bfe067d8f02c1ffb72c5627ec1802b7e3f57cc6833d0131a268135ba81`

## nlu-step2-0047 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 4

### 원문 raw

제거할 메이크업이 남아 있어요 그리고 세안은 두 차례예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제거할 메이크업이 남아 있어요 그리고 세안은 두 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제거할 메이크업이 남아 있어요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안은 두 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `530e1ae6a0a28f119610113dbb7f68e2d3c6ad347fe5d3ed5871959f39fdd9a3`

## nlu-step2-0048 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 5

### 원문 raw

세정 대상은 색조 화장이에요, 세안은 두 차례예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정 대상은 색조 화장이에요, 세안은 두 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 대상은 색조 화장이에요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안은 두 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6a93c39ffbf1c40d0edfeda9f6bc3f7b0e6131735ff6efdf09506db69ae349da`

## nlu-step2-0049 · turn1_utterance · train

의미 가족: `nlu-step2-makeup_count` / 표현 변형: 6

### 원문 raw

지워야 할 색조 화장이 있어요 / 세수 두번함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지워야 할 색조 화장이 있어요 / 세수 두번함",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지워야 할 색조 화장이 있어요"
    },
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세수 두번함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8748251411df51ef44afa56440a173347877247750c076a40c2cab650c6ae66f`

## nlu-step2-0050 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 0

### 원문 raw

추가로 지울 건 없어요. 이유 없이 습관으로 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "추가로 지울 건 없어요. 이유 없이 습관으로 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이유 없이 습관으로 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d6d48e8d32073801966c0572d67b0ac1296926a172f057879d47b8ca0e093e77`

## nlu-step2-0051 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 1

### 원문 raw

더 제거할 것은 없어요, 이유 없이 습관으로 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "더 제거할 것은 없어요, 이유 없이 습관으로 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "더 제거할 것은 없어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이유 없이 습관으로 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9b3c8103b5d6daab299d0012f449d7934cd1c951f482640f43c7894f10755779`

## nlu-step2-0052 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 2

### 원문 raw

따로 더 지울 게 없음
이유 없이 습관으로 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따로 더 지울 게 없음\n이유 없이 습관으로 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "따로 더 지울 게 없음"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이유 없이 습관으로 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4b4bbd2e054efbf8326e167e6c64ad68e97488c168abdd5bac0376ff7c5e44f4`

## nlu-step2-0053 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 3

### 원문 raw

추가로 지울 건 없어요. 그냥 습관이라 세안을 반복해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "추가로 지울 건 없어요. 그냥 습관이라 세안을 반복해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그냥 습관이라 세안을 반복해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9f10565033ebbc7c7e4756a4a2ee5cd7a59f1916acf8608fa3c3bb3a867a912f`

## nlu-step2-0054 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 4

### 원문 raw

더 제거할 것은 없어요 그리고 그냥 습관이라 세안을 반복해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "더 제거할 것은 없어요 그리고 그냥 습관이라 세안을 반복해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "더 제거할 것은 없어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그냥 습관이라 세안을 반복해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `a4cdd9bbbe1a1bc2ea0d0c6bc2aae2a1abb3b642ef131325aab531d16830323b`

## nlu-step2-0055 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 5

### 원문 raw

따로 더 지울 게 없음, 그냥 습관이라 세안을 반복해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따로 더 지울 게 없음, 그냥 습관이라 세안을 반복해여",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "따로 더 지울 게 없음"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그냥 습관이라 세안을 반복해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `07d11c71081692fe7b55665c72893768ddcedff85ad4b9686a9f0ba6999148d1`

## nlu-step2-0056 · turn1_utterance · train

의미 가족: `nlu-step2-no_load_habit` / 표현 변형: 6

### 원문 raw

추가로 지울 건 없어요 / 특별한 이유는 없고 반복해서 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "추가로 지울 건 없어요 / 특별한 이유는 없고 반복해서 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "habitual_without_reason",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "특별한 이유는 없고 반복해서 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `3cc847e349635f059285add5ce70391adcc80c177ae2db4c3b91cd9bcd0e43eb`

## nlu-step2-0057 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 0

### 원문 raw

피부에 흙이 많이 묻었어요. 남은 화장 제거하려고 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부에 흙이 많이 묻었어요. 남은 화장 제거하려고 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부에 흙이 많이 묻었어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `16bb4027719a8f74fdc4a3d15f8c85fa8ac4f939e4fb64883bada23e3c3cd84e`

## nlu-step2-0058 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 1

### 원문 raw

피부에 묻은 흙이 많아요, 남은 화장 제거하려고 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부에 묻은 흙이 많아요, 남은 화장 제거하려고 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부에 묻은 흙이 많아요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c0a968472361e801366f84addf9511194adcea3a216339b78fc9257d0498f754`

## nlu-step2-0059 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 2

### 원문 raw

흙이 잔뜩 피부에 묻음
남은 화장 제거하려고 반복 세안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흙이 잔뜩 피부에 묻음\n남은 화장 제거하려고 반복 세안해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "흙이 잔뜩 피부에 묻음"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "남은 화장 제거하려고 반복 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `def554b84907a68b574e7f61402357b5ca895922a42f77837bbe7dfd8ce05413`

## nlu-step2-0060 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 3

### 원문 raw

피부에 흙이 많이 묻었어요. 색조 잔여물 제거가 반복 세안 이유예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부에 흙이 많이 묻었어요. 색조 잔여물 제거가 반복 세안 이유예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부에 흙이 많이 묻었어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `b917da71d06f6c59e45eede5502b62340766e08196eec8dd4d562445a72925b2`

## nlu-step2-0061 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 4

### 원문 raw

피부에 묻은 흙이 많아요 그리고 색조 잔여물 제거가 반복 세안 이유예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부에 묻은 흙이 많아요 그리고 색조 잔여물 제거가 반복 세안 이유예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부에 묻은 흙이 많아요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `2445cd89af7611ee88b2f545c27b685306dcd87f5903c28825313d335e481269`

## nlu-step2-0062 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 5

### 원문 raw

흙이 잔뜩 피부에 묻음, 색조 잔여물 제거가 반복 세안 이유예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흙이 잔뜩 피부에 묻음, 색조 잔여물 제거가 반복 세안 이유예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "흙이 잔뜩 피부에 묻음"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "색조 잔여물 제거가 반복 세안 이유예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `df558c9a4a692fd5525b01e66da753301214a09fed6656300ee08ac0a6242b8d`

## nlu-step2-0063 · turn1_utterance · train

의미 가족: `nlu-step2-soil_matched` / 표현 변형: 6

### 원문 raw

피부에 흙이 많이 묻었어요 / 반복하는 이유는 남은 화장을 지우려는 거예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "피부에 흙이 많이 묻었어요 / 반복하는 이유는 남은 화장을 지우려는 거예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "heavy_soiling",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부에 흙이 많이 묻었어요"
    },
    {
      "variable_id": "cleansing.repeat_wash",
      "value": "purpose_matched",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "반복하는 이유는 남은 화장을 지우려는 거예요"
    },
    {
      "variable_id": "cleansing.target_load",
      "value": "makeup_requires_removal",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "반복하는 이유는 남은 화장을 지우려는 거예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6db64aa612e556509829ff22ad07893739f1e93ba3ab0e6e83eeb3c57f41808e`

## nlu-step2-0064 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 0

### 원문 raw

매일 로션을 써요. 씻고 3분 뒤에 보습해요. 보습하고 나면 편안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요. 씻고 3분 뒤에 보습해요. 보습하고 나면 편안해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `a8912de6e06bb9e20edd776100b153ede75768a7051a5140d429af496d9cab9b`

## nlu-step2-0065 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 1

### 원문 raw

로션은 매일 발라요, 씻고 3분 뒤에 보습해요, 보습하고 나면 편안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션은 매일 발라요, 씻고 3분 뒤에 보습해요, 보습하고 나면 편안해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `169df63bc2f2afbba48647b94bab0702cdfa29f205dda0d6055df5b012fc37bd`

## nlu-step2-0066 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 2

### 원문 raw

매일 로션 바름
씻고 3분 뒤에 보습해요
보습하고 나면 편안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션 바름\n씻고 3분 뒤에 보습해요\n보습하고 나면 편안해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9ec3a19156fc40649f0748e10b5925c852569c05d64e8dbfa1a44e41aaf5d878`

## nlu-step2-0067 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 3

### 원문 raw

매일 로션을 써요. 세안 후 보습까지 3분 걸려요. 보습 뒤 사용감은 편안함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요. 세안 후 보습까지 3분 걸려요. 보습 뒤 사용감은 편안함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 사용감은 편안함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `0536f57f199351fdf1ea5819afe3c38d117b3214182fe8537791148b8c0f707b`

## nlu-step2-0068 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 4

### 원문 raw

로션은 매일 발라요 그리고 세안 후 보습까지 3분 걸려요 그리고 보습 뒤 사용감은 편안함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션은 매일 발라요 그리고 세안 후 보습까지 3분 걸려요 그리고 보습 뒤 사용감은 편안함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 사용감은 편안함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5dfe1a8d77425f735c39f24d1ba3820ede90eb87ef5d8287c1b3d7c1cd6816fa`

## nlu-step2-0069 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 5

### 원문 raw

매일 로션 바름, 세안 후 보습까지 3분 걸려요, 보습 뒤 사용감은 편안함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션 바름, 세안 후 보습까지 3분 걸려요, 보습 뒤 사용감은 편안함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 사용감은 편안함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `ef732fbbaa9458a9e4c2afaaf48661dd3678e7a45ef360e2655b2699646d94c7`

## nlu-step2-0070 · turn1_utterance · train

의미 가족: `nlu-step2-lotion_delay` / 표현 변형: 6

### 원문 raw

매일 로션을 써요 / 보습은 세안하고 삼 분 뒤예요 / 보습 후 느낌은 편해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요 / 보습은 세안하고 삼 분 뒤예요 / 보습 후 느낌은 편해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 세안하고 삼 분 뒤예요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `1217a176a5dcfced429d9e8e648e505eff0ca09dfbd69147f5881d5b687b9f9e`

## nlu-step2-0071 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 0

### 원문 raw

저녁에는 크림을 발라요. 보습은 볼에만 해요. 보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요. 보습은 볼에만 해요. 보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9c6255fb1431e0188669022d9fcfa74f84572137f31e7e094abf0522f086ea42`

## nlu-step2-0072 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 1

### 원문 raw

크림은 저녁에 써요, 보습은 볼에만 해요, 보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "크림은 저녁에 써요, 보습은 볼에만 해요, 보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `3989770b1781eef22f29d43a0b0595dee6aded8355e9cd616bc7e50036b3045a`

## nlu-step2-0073 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 2

### 원문 raw

저녁에 크림 바름
보습은 볼에만 해요
보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에 크림 바름\n보습은 볼에만 해요\n보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `e5415df72d984e5dda76dbded7d6c8c78767dc1a44c9f412fe37da95c24be358`

## nlu-step2-0074 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 3

### 원문 raw

저녁에는 크림을 발라요. 보습 바르는 범위는 볼뿐이에요. 보습 뒤 감촉은 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요. 보습 바르는 범위는 볼뿐이에요. 보습 뒤 감촉은 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `be75c165d0826bb0a33cb33fd69d01546a0236bbbf7f66bd6f95d06cfe116fa3`

## nlu-step2-0075 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 4

### 원문 raw

크림은 저녁에 써요 그리고 보습 바르는 범위는 볼뿐이에요 그리고 보습 뒤 감촉은 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "크림은 저녁에 써요 그리고 보습 바르는 범위는 볼뿐이에요 그리고 보습 뒤 감촉은 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d16c1705fa18be74ca34e7eb298608949e330cbb31564ba6d6c2747bfad30f11`

## nlu-step2-0076 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 5

### 원문 raw

저녁에 크림 바름, 보습 바르는 범위는 볼뿐이에요, 보습 뒤 감촉은 끈적해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에 크림 바름, 보습 바르는 범위는 볼뿐이에요, 보습 뒤 감촉은 끈적해여",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `1916cb5c31f0d75a42457dbb5af12baeb388e20ec0ba7465b94611e390761f1c`

## nlu-step2-0077 · turn1_utterance · train

의미 가족: `nlu-step2-cream_coverage` / 표현 변형: 6

### 원문 raw

저녁에는 크림을 발라요 / 볼만 보습해요 / 보습 후 느낌이 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요 / 볼만 보습해요 / 보습 후 느낌이 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "볼만 보습해요"
    },
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌이 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `437f9796cd217fe2f20337a9ce6197c205533d9250e6c85ebb6f420eacbb132b`

## nlu-step2-0078 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 0

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요. 건조할 때 보습을 덧발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요. 건조할 때 보습을 덧발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조할 때 보습을 덧발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `2fa749c156ac279e382a0cc304676949b3d314a2648310bd626a4de9d23cc4a9`

## nlu-step2-0079 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 1

### 원문 raw

보습하고 두 시간 뒤엔 다시 건조해요, 건조할 때 보습을 덧발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습하고 두 시간 뒤엔 다시 건조해요, 건조할 때 보습을 덧발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조할 때 보습을 덧발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `0ad37cca370165239b59eff5654cec35886245b1fb87dbe30e9a576c86e018f6`

## nlu-step2-0080 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 2

### 원문 raw

보습한 뒤 2시간 지나 건조감 돌아와요
건조할 때 보습을 덧발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습한 뒤 2시간 지나 건조감 돌아와요\n건조할 때 보습을 덧발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조할 때 보습을 덧발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c7c7d89efc51dfc112d4a30e27960273db03d6504e748f634efa2b2e1de6748b`

## nlu-step2-0081 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 3

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요. 건조감 있을 때만 보습 추가해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요. 건조감 있을 때만 보습 추가해요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `fd08ab1aaabb9e68d54e9f9e8059d50494efd2392066943cbea1b535bfa7d025`

## nlu-step2-0082 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 4

### 원문 raw

보습하고 두 시간 뒤엔 다시 건조해요 그리고 건조감 있을 때만 보습 추가해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습하고 두 시간 뒤엔 다시 건조해요 그리고 건조감 있을 때만 보습 추가해요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `79e2bada07d93ce59d7638a64d3e7ddee7a57c72b9957cf4b801f17ec966324a`

## nlu-step2-0083 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 5

### 원문 raw

보습한 뒤 2시간 지나 건조감 돌아와요, 건조감 있을 때만 보습 추가해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습한 뒤 2시간 지나 건조감 돌아와요, 건조감 있을 때만 보습 추가해여",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `71417870e41f7dc64029ce26e6a5a8be01f4971b1d7220777666f1614ad5da50`

## nlu-step2-0084 · turn1_utterance · train

의미 가족: `nlu-step2-dry_return_reapply` / 표현 변형: 6

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요 / 보습 덧바르는 때는 건조할 때예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요 / 보습 덧바르는 때는 건조할 때예요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 덧바르는 때는 건조할 때예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4f6eb85fc300bf74832b69b6531958c328746ec7da8e349344900648758e4371`

## nlu-step2-0085 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 0

### 원문 raw

아침마다 선크림 발라요. 야외에 오래 있었어요. 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요. 야외에 오래 있었어요. 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8e551e27f76452a54a287efb8369404cc483e2fd44ee8dde1100e6f154739e67`

## nlu-step2-0086 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 1

### 원문 raw

선크림은 매일 아침 써요, 야외에 오래 있었어요, 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림은 매일 아침 써요, 야외에 오래 있었어요, 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c9dbd31c8069955b18a5bf155dbd93388535a48094240a512239b13dfd6a28be`

## nlu-step2-0087 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 2

### 원문 raw

매일 아침 선크림 바름
야외에 오래 있었어요
모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 아침 선크림 바름\n야외에 오래 있었어요\n모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `55044eb51320d05d5fafac10842446119e8570da9a18376c1477caa667ffc6bf`

## nlu-step2-0088 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 3

### 원문 raw

아침마다 선크림 발라요. 밖에서 오래 머물렀어요. 모자 착용했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요. 밖에서 오래 머물렀어요. 모자 착용했어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 착용했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `34384bd95bbdc14806dbc08373e8c10e8c3d4c5149a451c0c0c76dcfb17ea66c`

## nlu-step2-0089 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 4

### 원문 raw

선크림은 매일 아침 써요 그리고 밖에서 오래 머물렀어요 그리고 모자 착용했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림은 매일 아침 써요 그리고 밖에서 오래 머물렀어요 그리고 모자 착용했어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 착용했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `b49f69e95605261af91629ca2fcbafbb49a1fd594180ad0c60cc2db270c65a8a`

## nlu-step2-0090 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 5

### 원문 raw

매일 아침 선크림 바름, 밖에서 오래 머물렀어여, 모자 착용했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 아침 선크림 바름, 밖에서 오래 머물렀어여, 모자 착용했어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어여"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 착용했어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7359b8b3fb6c085078a58984f8198db8d59bd014100aeb444954e74885e3a724`

## nlu-step2-0091 · turn1_utterance · train

의미 가족: `nlu-step2-sun_plan` / 표현 변형: 6

### 원문 raw

아침마다 선크림 발라요 / 오랫동안 야외에 있었음 / 모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요 / 오랫동안 야외에 있었음 / 모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "오랫동안 야외에 있었음"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7e5099a522451e755718ffb38bf6066f81c9770bcfc31ff5a38b96aaa3fb6786`

## nlu-step2-0092 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 0

### 원문 raw

물에 들어갔어요. 땀이 났어요. 손등이랑 팔이 드러나 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 들어갔어요. 땀이 났어요. 손등이랑 팔이 드러나 있어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등이랑 팔이 드러나 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `109548e4727ddb30d704d34efc9d6e3e47c231fac07b5772883fdd755074c51b`

## nlu-step2-0093 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 1

### 원문 raw

수영했어요, 땀이 났어요, 손등이랑 팔이 드러나 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수영했어요, 땀이 났어요, 손등이랑 팔이 드러나 있어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수영했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등이랑 팔이 드러나 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8e976accc0647556cf6cc45a469c57d938f9197d08575133900c023fdd8f15f4`

## nlu-step2-0094 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 2

### 원문 raw

물놀이 했어요
땀이 났어요
손등이랑 팔이 드러나 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물놀이 했어요\n땀이 났어요\n손등이랑 팔이 드러나 있어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물놀이 했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등이랑 팔이 드러나 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `29c4fae875946ce72442240eafd62a73628a2a9c4655540e9bd846b01c0196ae`

## nlu-step2-0095 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 3

### 원문 raw

물에 들어갔어요. 땀 흘렸어요. 손등 팔이 노출됐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 들어갔어요. 땀 흘렸어요. 손등 팔이 노출됐어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5b1e235de90ea74a6729db2c940e71d5099cd5633bb961bdf147ddf6878ce386`

## nlu-step2-0096 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 4

### 원문 raw

수영했어요 그리고 땀 흘렸어요 그리고 손등 팔이 노출됐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수영했어요 그리고 땀 흘렸어요 그리고 손등 팔이 노출됐어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수영했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `4242f85ae248ca13f291adcf1c9ca97da85b11305fdcd0edc46b3bd529987add`

## nlu-step2-0097 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 5

### 원문 raw

물놀이 했어여, 땀 흘렸어여, 손등 팔이 노출됐어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물놀이 했어여, 땀 흘렸어여, 손등 팔이 노출됐어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물놀이 했어여"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흘렸어여"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `535a40b9bc1a2de3aac67994be2904a3618ce5e5b657992a930a05b98ffa384d`

## nlu-step2-0098 · turn1_utterance · train

의미 가족: `nlu-step2-water_sweat` / 표현 변형: 6

### 원문 raw

물에 들어갔어요 / 땀이 많이 남 / 노출된 곳은 손등과 팔이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 들어갔어요 / 땀이 많이 남 / 노출된 곳은 손등과 팔이에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "노출된 곳은 손등과 팔이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `02b17d0e344e6a24bb3040a71aa55c34191a743e771de55103f3da5d15473500`

## nlu-step2-0099 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 0

### 원문 raw

차단제 바를 때 귀랑 목은 빼먹었어요. 차단제는 2시간마다 덧발라요. 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "차단제 바를 때 귀랑 목은 빼먹었어요. 차단제는 2시간마다 덧발라요. 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9add62d9428e57ba2ab9403ba8de3d5c106d9238f10d92b7cf6111ae6aa155b9`

## nlu-step2-0100 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 1

### 원문 raw

귀와 목을 차단제 바를 때 빼먹었어요, 차단제는 2시간마다 덧발라요, 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "귀와 목을 차단제 바를 때 빼먹었어요, 차단제는 2시간마다 덧발라요, 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `80547f35bf4a3da3ec5981ba77c6a5c5e545c5009bc0f3e7b22f4c5def473e09`

## nlu-step2-0101 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 2

### 원문 raw

귀 목은 차단제 누락했어요
차단제는 2시간마다 덧발라요
그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "귀 목은 차단제 누락했어요\n차단제는 2시간마다 덧발라요\n그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제는 2시간마다 덧발라요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5d6549733ef8ff4522d6bd8bcbf3af9187e5425c166344b42c74d2f299a4e144`

## nlu-step2-0102 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 3

### 원문 raw

차단제 바를 때 귀랑 목은 빼먹었어요. 차단제 덧바르는 간격은 두 시간이에요. 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "차단제 바를 때 귀랑 목은 빼먹었어요. 차단제 덧바르는 간격은 두 시간이에요. 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8b5285c01fae4774fa53a9cf202a0923fff552dacffef595a3352c751c594219`

## nlu-step2-0103 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 4

### 원문 raw

귀와 목을 차단제 바를 때 빼먹었어요 그리고 차단제 덧바르는 간격은 두 시간이에요 그리고 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "귀와 목을 차단제 바를 때 빼먹었어요 그리고 차단제 덧바르는 간격은 두 시간이에요 그리고 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `80ca7528b7154adaf62782306d762465610102e1b684d3168375b1932be86688`

## nlu-step2-0104 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 5

### 원문 raw

귀 목은 차단제 누락했어여, 차단제 덧바르는 간격은 두 시간이에요, 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "귀 목은 차단제 누락했어여, 차단제 덧바르는 간격은 두 시간이에요, 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어여"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 덧바르는 간격은 두 시간이에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `baf964b9707ab22c3f34e075a6d0b6b4fede6be1f9db6b88ab00e5919019b41c`

## nlu-step2-0105 · turn1_utterance · train

의미 가족: `nlu-step2-gaps_reapply` / 표현 변형: 6

### 원문 raw

차단제 바를 때 귀랑 목은 빼먹었어요 / 차단제 두 시간 간격으로 덧바름 / 그늘에 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "차단제 바를 때 귀랑 목은 빼먹었어요 / 차단제 두 시간 간격으로 덧바름 / 그늘에 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    },
    {
      "variable_id": "sun.reapplication",
      "value": "2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 두 시간 간격으로 덧바름"
    },
    {
      "variable_id": "method.current_routine",
      "value": "차단제 2시간마다 덧바름",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 두 시간 간격으로 덧바름"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9e5d55009b91266e9b22f9a23eb4e8dcae9764ef5a209bcf8f91c823c84af4c0`

## nlu-step2-0106 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 0

### 원문 raw

지난 금요일에 열었어요. 창가에 두고 있어요. 이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지난 금요일에 열었어요. 창가에 두고 있어요. 이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "창가에 두고 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8c5917f0bf1bd45bf3d69872c4aef0c56dda5f3943d7ff995208646c9c3b5a6e`

## nlu-step2-0107 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 1

### 원문 raw

개봉한 날은 지난 금요일이에요, 창가에 두고 있어요, 이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉한 날은 지난 금요일이에요, 창가에 두고 있어요, 이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉한 날은 지난 금요일이에요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "창가에 두고 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c2d26f3648d354dd3d6b2649182c8406e5ee27011f11ca2e3814868ac81992c7`

## nlu-step2-0108 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 2

### 원문 raw

지난주 금욜에 개봉함
창가에 두고 있어요
이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지난주 금욜에 개봉함\n창가에 두고 있어요\n이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난주 금욜에 개봉함"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "창가에 두고 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `86a3aa178392350c0e7775e7c8efc4a528f2dcd1c7f0e6f3410a578476acc6b2`

## nlu-step2-0109 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 3

### 원문 raw

지난 금요일에 열었어요. 보관 장소는 창가예요. 상담 앱 메뉴 위치 알고 싶어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지난 금요일에 열었어요. 보관 장소는 창가예요. 상담 앱 메뉴 위치 알고 싶어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6e3cb7a7203ebcc62e8850686025f8c2faba631d5264a1a862efa2d7835d6716`

## nlu-step2-0110 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 4

### 원문 raw

개봉한 날은 지난 금요일이에요 그리고 보관 장소는 창가예요 그리고 상담 앱 메뉴 위치 알고 싶어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉한 날은 지난 금요일이에요 그리고 보관 장소는 창가예요 그리고 상담 앱 메뉴 위치 알고 싶어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉한 날은 지난 금요일이에요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8a1c217824f7afb60ecb62d9a7e790030aceeb850be557ca27ec70e4ef7d579b`

## nlu-step2-0111 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 5

### 원문 raw

지난주 금욜에 개봉함, 보관 장소는 창가예요, 상담 앱 메뉴 위치 알고 싶어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지난주 금욜에 개봉함, 보관 장소는 창가예요, 상담 앱 메뉴 위치 알고 싶어여",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난주 금욜에 개봉함"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `c4e03cf5718d51cba179a5c4d6e2b42bc0b40a9dd755b7bd6560f13eddcb0176`

## nlu-step2-0112 · turn1_utterance · train

의미 가족: `nlu-step2-opened_window` / 표현 변형: 6

### 원문 raw

지난 금요일에 열었어요 / 창 옆에 보관 중이에요 / 이 상담 화면의 메뉴가 궁금해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지난 금요일에 열었어요 / 창 옆에 보관 중이에요 / 이 상담 화면의 메뉴가 궁금해요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "창 옆에 보관 중이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d4b07731b8abaac1453cad79bffb0ed94b918a8e70949dc42f4493b1d0613141`

## nlu-step2-0113 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 0

### 원문 raw

작은 공병에 덜어뒀어요. 용기는 단지형이에요. 이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 공병에 덜어뒀어요. 용기는 단지형이에요. 이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `cfcbdb5fb29b9a2cb59e0a9a8f23cc0e3927f078177ccf85f3aee774f5bf3c73`

## nlu-step2-0114 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 1

### 원문 raw

작은 공병으로 소분했어요, 용기는 단지형이에요, 이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 공병으로 소분했어요, 용기는 단지형이에요, 이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6d809c0aadef11bb52b96e6e2b3db7d6692b70ac4b83baa9c2c20a6a9da1f3c8`

## nlu-step2-0115 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 2

### 원문 raw

작은 빈 병에 나눠 담음
용기는 단지형이에요
이 서비스 화면 메뉴를 찾고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 빈 병에 나눠 담음\n용기는 단지형이에요\n이 서비스 화면 메뉴를 찾고 있어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 빈 병에 나눠 담음"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `3aa2be004a0f3aadf2b029f5d5e11252b13ff57bd49cde2b9fb9dc48878730c2`

## nlu-step2-0116 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 3

### 원문 raw

작은 공병에 덜어뒀어요. 단지 형태 용기예요. 상담 앱 메뉴 위치 알고 싶어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 공병에 덜어뒀어요. 단지 형태 용기예요. 상담 앱 메뉴 위치 알고 싶어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `5680a2038dfd59b28d9fe74319186a185bfa440636d79de3a3614b31e5f3ec11`

## nlu-step2-0117 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 4

### 원문 raw

작은 공병으로 소분했어요 그리고 단지 형태 용기예요 그리고 상담 앱 메뉴 위치 알고 싶어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 공병으로 소분했어요 그리고 단지 형태 용기예요 그리고 상담 앱 메뉴 위치 알고 싶어요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `84725150238a13d16bc66be8469676bb18b2def12d1da3b3bcc35c54ac5ea841`

## nlu-step2-0118 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 5

### 원문 raw

작은 빈 병에 나눠 담음, 단지 형태 용기예요, 상담 앱 메뉴 위치 알고 싶어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 빈 병에 나눠 담음, 단지 형태 용기예요, 상담 앱 메뉴 위치 알고 싶어여",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 빈 병에 나눠 담음"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `739c0a03cdd4d8b6566a025f3688998d3c437e5c2721db8980f99a66860ae400`

## nlu-step2-0119 · turn1_utterance · train

의미 가족: `nlu-step2-decant_jar` / 표현 변형: 6

### 원문 raw

작은 공병에 덜어뒀어요 / 통 모양은 단지형임 / 이 상담 화면의 메뉴가 궁금해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "작은 공병에 덜어뒀어요 / 통 모양은 단지형임 / 이 상담 화면의 메뉴가 궁금해요",
  "topics": [
    "storage_label",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 모양은 단지형임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `809a5594e377b60fb1856abef91f7601f5ffd23b13d275a7cf37c507e83d5651`

## nlu-step2-0120 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 0

### 원문 raw

사용기한은 2027년 8월로 적혀요. 개봉 후 6개월 표시예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사용기한은 2027년 8월로 적혀요. 개봉 후 6개월 표시예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `df4a6ca1dfebdef311a6b513a62980e1448ef97dac702923237181e8528e7a57`

## nlu-step2-0121 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 1

### 원문 raw

2027년 8월이 사용기한이에요, 개봉 후 6개월 표시예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "2027년 8월이 사용기한이에요, 개봉 후 6개월 표시예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7bedec5f4d2202405f42e14f6d0eaba644f53b9b652ae3c3852d53d939399263`

## nlu-step2-0122 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 2

### 원문 raw

사용기한 표시 2027년 8월임
개봉 후 6개월 표시예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사용기한 표시 2027년 8월임\n개봉 후 6개월 표시예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `8f88e3b68fc6591946e47bc638ad9c361dcacec2a4eeb59ce10274ff720774e3`

## nlu-step2-0123 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 3

### 원문 raw

사용기한은 2027년 8월로 적혀요. 개봉 뒤 여섯 달이라고 써 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사용기한은 2027년 8월로 적혀요. 개봉 뒤 여섯 달이라고 써 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `f4a25f6cc1161f28aa61c68257e09b5cb1e541cb404e7c442978f9f7c3673bb4`

## nlu-step2-0124 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 4

### 원문 raw

2027년 8월이 사용기한이에요 그리고 개봉 뒤 여섯 달이라고 써 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "2027년 8월이 사용기한이에요 그리고 개봉 뒤 여섯 달이라고 써 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `6ef9a2638e6167b76c9ad66bea4a855881e9558f98aff35daa59b17722d447ef`

## nlu-step2-0125 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 5

### 원문 raw

사용기한 표시 2027년 8월임, 개봉 뒤 여섯 달이라고 써 있어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사용기한 표시 2027년 8월임, 개봉 뒤 여섯 달이라고 써 있어여",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `efb4bef342011536790fb41bc14434a27ebf791dcebf219e78bfe17fcc9aec4e`

## nlu-step2-0126 · turn1_utterance · train

의미 가족: `nlu-step2-expiry_pao` / 표현 변형: 6

### 원문 raw

사용기한은 2027년 8월로 적혀요 / 열고 6개월 이내라고 적혀요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사용기한은 2027년 8월로 적혀요 / 열고 6개월 이내라고 적혀요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `188bd8a00578ec73a817dc3e54a9576e87b93bc2f55449edcae54f329b93d69b`

## nlu-step2-0127 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 0

### 원문 raw

용기 안에 물이 들어갔어요. 용기는 펌프형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물이 들어갔어요. 용기는 펌프형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물이 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 펌프형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `858078855a079fa34e064cd7e09d7864e608132b1879d546ea746f5c94308dd1`

## nlu-step2-0128 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 1

### 원문 raw

안으로 물이 유입됐어요, 용기는 펌프형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "안으로 물이 유입됐어요, 용기는 펌프형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "안으로 물이 유입됐어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 펌프형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `b40e867a1599a16dd775e1858a28b110516211b2d8edfa245610989c903680e5`

## nlu-step2-0129 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 2

### 원문 raw

통 안에 물 들어감
용기는 펌프형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통 안에 물 들어감\n용기는 펌프형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 안에 물 들어감"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 펌프형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `0aa8da8538ca0e7f6d2b3a179151ef409bbb513697e2d78ae9d4a90b17b80c0b`

## nlu-step2-0130 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 3

### 원문 raw

용기 안에 물이 들어갔어요. 펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물이 들어갔어요. 펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물이 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `d7072bc089acb3a40675a603d7b1433895d188b936db4ad008614d9d597a7d51`

## nlu-step2-0131 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 4

### 원문 raw

안으로 물이 유입됐어요 그리고 펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "안으로 물이 유입됐어요 그리고 펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "안으로 물이 유입됐어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9ff1c6047019f85adac900560b2f2ba4dec41100674fa74cc158fdf48bfaa799`

## nlu-step2-0132 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 5

### 원문 raw

통 안에 물 들어감, 펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통 안에 물 들어감, 펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 안에 물 들어감"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `1ec1211e751c5f6b59f739ff98ee3ffdf6708ab18dcd18f46228630781023591`

## nlu-step2-0133 · turn1_utterance · val_internal

의미 가족: `nlu-step2-ingress_pump` / 표현 변형: 6

### 원문 raw

용기 안에 물이 들어갔어요 / 통에 펌프가 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물이 들어갔어요 / 통에 펌프가 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물이 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통에 펌프가 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `9bbb5fb00ad2792a5943228d02b138823a8a82346db5573343b055c03633da00`

## nlu-step2-0134 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 0

### 원문 raw

전이랑 냄새가 달라졌어요. 서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "전이랑 냄새가 달라졌어요. 서랍 안에 둬요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `7010bf52e786e137650fa4de80212044237d6bd201b73ecba5f1f2face5a8869`

## nlu-step2-0135 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 1

### 원문 raw

이전과 다른 냄새가 나요, 서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이전과 다른 냄새가 나요, 서랍 안에 둬요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이전과 다른 냄새가 나요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `a4790fabafbbf0d3d418b6e9acec09c65bc20dcf2f6445b57e662d5be28c7168`

## nlu-step2-0136 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 2

### 원문 raw

냄새가 예전과 달라짐
서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "냄새가 예전과 달라짐\n서랍 안에 둬요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "냄새가 예전과 달라짐"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `e5c724bc046cf547b08b1f333e9f1a522a4dac58adedcc9bcb9247f6f6d4bdc0`

## nlu-step2-0137 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 3

### 원문 raw

전이랑 냄새가 달라졌어요. 서랍 안쪽에 보관해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "전이랑 냄새가 달라졌어요. 서랍 안쪽에 보관해요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `e96b47a8eeee7875d3655acec787fafea800185b1b34275b5ad86ae729ef4f73`

## nlu-step2-0138 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 4

### 원문 raw

이전과 다른 냄새가 나요 그리고 서랍 안쪽에 보관해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이전과 다른 냄새가 나요 그리고 서랍 안쪽에 보관해요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이전과 다른 냄새가 나요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `22debaf3608f6b159b622232c84d92612cad7b674dc9022a865faa017d31e07b`

## nlu-step2-0139 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 5

### 원문 raw

냄새가 예전과 달라짐, 서랍 안쪽에 보관해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "냄새가 예전과 달라짐, 서랍 안쪽에 보관해여",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "냄새가 예전과 달라짐"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `fa124adbd9b49a4448a419d1934a5aced2c7e9366c970e6a8426e419490c4697`

## nlu-step2-0140 · turn1_utterance · val_internal

의미 가족: `nlu-step2-odor_dark` / 표현 변형: 6

### 원문 raw

전이랑 냄새가 달라졌어요 / 보관하는 곳은 서랍 안이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "전이랑 냄새가 달라졌어요 / 보관하는 곳은 서랍 안이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보관하는 곳은 서랍 안이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

원문에 명시된 의미만 후보로 남겨요.

내용 SHA-256: `dcec2d53fae8ce9313ece7c18fb0c0bf4e1ee938aaa3276f5ed3d895f4ab2273`

## nlu-step2-0141 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 0

### 원문 raw

한 번만 해요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "한 번만 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "한 번만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `1eb0b46b1438a9026c62dc6b14640845db48d97fe71310645c0415e3f9c90a67`

## nlu-step2-0142 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 1

### 원문 raw

세안은 한 차례예요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안은 한 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안은 한 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `94bd2b2962837ea3ab5ce7163310e0aa34451cb3441a34bf1836511c477be55d`

## nlu-step2-0143 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 2

### 원문 raw

세수 한번함

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세수 한번함",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세수 한번함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `4f19a349ac3acfa7fed3789f4d29cbfb5a0e475955f1dd982b57f1f1ffe67271`

## nlu-step2-0144 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 3

### 원문 raw

씻는 횟수는 1회요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻는 횟수는 1회요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻는 횟수는 1회요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `2239b6b5ed4ec96e33be8fdcce673a18a1dccc89db2fc52c93b70388c88df6fd`

## nlu-step2-0145 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 4

### 원문 raw

딱 한 번 씻어요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "딱 한 번 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "딱 한 번 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `b1d7f11dc5ecf6ed066deb7df5e7624fd7abd26bd00997d71a6eaf7522e5e545`

## nlu-step2-0146 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 5

### 원문 raw

한 번으로 끝내요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "한 번으로 끝내요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "한 번으로 끝내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `947218e25eb814917f68a1fb173db844ae2291bf1a051450209fa904da06874e`

## nlu-step2-0147 · turn2_followup · train

의미 가족: `nlu-step2-pure_one` / 표현 변형: 6

### 원문 raw

세안 1번만 해요

직전 질문: 세안은 몇 번 하세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 1번만 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 1,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 1번만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `82800f9bfd11bb80cd602f324c1ac30294a8af18c9c939e334d58baa5cb664d3`

## nlu-step2-0148 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 0

### 원문 raw

두 번 해요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "두 번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `64a63441f9bf544e9f105c67381149e4d39773befa7acbf41e3690343d1579be`

## nlu-step2-0149 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 1

### 원문 raw

세안은 두 차례예요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안은 두 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안은 두 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `ffabe0452d018accff17c6ac001cff338b77cc93327f509989ac0a97b00dbd26`

## nlu-step2-0150 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 2

### 원문 raw

세수 두번함

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세수 두번함",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세수 두번함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `8d5ec9c31ee74ad92be09d438025f2f19b6078a9af193c4374a6a5fe103e8419`

## nlu-step2-0151 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 3

### 원문 raw

씻는 횟수는 2회요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻는 횟수는 2회요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻는 횟수는 2회요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `2d937acf6279dea9c216f6241f3f992d9007ed7f29ed72e8915955246351e90b`

## nlu-step2-0152 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 4

### 원문 raw

딱 두 번 씻어요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "딱 두 번 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "딱 두 번 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `06bd0bd265efe46028c618b39e240d9a3a1ba8bba929fd9e9c8214262827bf92`

## nlu-step2-0153 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 5

### 원문 raw

두 번으로 끝내요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "두 번으로 끝내요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 번으로 끝내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `e2e161da8add348d695cd6f14914f37601e5e4a577a00d3a58e78da8730aeb95`

## nlu-step2-0154 · turn2_followup · train

의미 가족: `nlu-step2-pure_two` / 표현 변형: 6

### 원문 raw

세안 2번 해요

직전 질문: 세안을 몇 차례 하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 2번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 2번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `40329a3f2017e7756375f217af81a95f858c92126761f6106af13127dd47f6cf`

## nlu-step2-0155 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 0

### 원문 raw

제품 표시대로 해요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 표시대로 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 표시대로 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `ce11756e83f1b07f5d6939418c3d8adf31ceed9d6535a338aa719b3ea8832e93`

## nlu-step2-0156 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 1

### 원문 raw

제품에 적힌 제거 방법대로 씻어요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품에 적힌 제거 방법대로 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품에 적힌 제거 방법대로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `b747692f273091152a492443bf6e4aea772debc058aaab06721673fb08af62e0`

## nlu-step2-0157 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 2

### 원문 raw

횟수는 안 정하고 제거 안내를 따라요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "횟수는 안 정하고 제거 안내를 따라요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "횟수는 안 정하고 제거 안내를 따라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9a9ca5b42851245a54263f2343ea22f240870235c35f7d068b1afdd3bb20600a`

## nlu-step2-0158 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 3

### 원문 raw

표시된 세정 순서대로만 해요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표시된 세정 순서대로만 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "표시된 세정 순서대로만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `cfbf677d204ffefc4e017a84cc845374b247b2b9b56f29530b6763f0a2e34a89`

## nlu-step2-0159 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 4

### 원문 raw

제품의 제거 지시에 맞춰요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품의 제거 지시에 맞춰요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품의 제거 지시에 맞춰요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `c54f3cdbc7769d6eca051dddad06e812e6d5aa0899da417a17ea891c9db878d5`

## nlu-step2-0160 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 5

### 원문 raw

제거 방법은 제품 표시를 따름

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제거 방법은 제품 표시를 따름",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제거 방법은 제품 표시를 따름"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `94cd8b0f23101eaf9cb30eb3fdc19ed3215f17364ea2c158b5e170b08fd06e1e`

## nlu-step2-0161 · turn2_followup · train

의미 가족: `nlu-step2-label_only` / 표현 변형: 6

### 원문 raw

제품 표시의 제거법 그대로 해요

직전 질문: 제거 단계는 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 표시의 제거법 그대로 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 표시의 제거법 그대로 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `eb7f00ce94a3e73a4319e73603444bbe6df18fc646dd797d7736f8fe852e7848`

## nlu-step2-0162 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 0

### 원문 raw

제품 표시대로 하고 두 번 씻어요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 표시대로 하고 두 번 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 표시대로 하고 두 번 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `b0be820340dd8afe01175686cbd77335a8bb5a8b04a133704651dcb13ded2dd7`

## nlu-step2-0163 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 1

### 원문 raw

제거 안내를 따르는데 횟수는 두 번이에요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제거 안내를 따르는데 횟수는 두 번이에요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제거 안내를 따르는데 횟수는 두 번이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `e5c6d88e5bc62a35d584abcab652c5f67c8addeb003f9ae14423d2d5a10e1a7a`

## nlu-step2-0164 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 2

### 원문 raw

표시 준수해서 세수 두번함

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표시 준수해서 세수 두번함",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "표시 준수해서 세수 두번함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9f481c6606bbac6f41b842dd61e2ec06e6a7fd995e6b457b4e63712ca88f5ffb`

## nlu-step2-0165 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 3

### 원문 raw

제품 제거법 따르고 총 2회 씻어요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 제거법 따르고 총 2회 씻어요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 제거법 따르고 총 2회 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `92e32c5ea38738bef6c4bbba205eba9bae2b86c8b83f98f1410184778afd1123`

## nlu-step2-0166 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 4

### 원문 raw

제품 표시대로 하되 두 차례예요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 표시대로 하되 두 차례예요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 표시대로 하되 두 차례예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `b9a89e4dae34563a7f3daa1d3e5ac8d05e755e74d443a43ecf1725eae0371636`

## nlu-step2-0167 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 5

### 원문 raw

표시 보고 씻는데 두 번으로 끝내요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표시 보고 씻는데 두 번으로 끝내요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "표시 보고 씻는데 두 번으로 끝내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `f6b7ac8e489a3c8a75e4783d1d4f9c3a588876430c5e541870cfcfec1c8a4ae2`

## nlu-step2-0168 · turn2_followup · train

의미 가족: `nlu-step2-explicit_over_label` / 표현 변형: 6

### 원문 raw

제품 지시를 따르며 세안 2번 해요

직전 질문: 몇 번 씻는지 알려 주세요.
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 지시를 따르며 세안 2번 해요",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": 2,
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "제품 지시를 따르며 세안 2번 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `fca00c6736be7cd4e6d440c7aa5029f095c6411968ae744032332f72a7e7b3db`

## nlu-step2-0169 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 0

### 원문 raw

물은 미지근해요. 살살 문질러요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물은 미지근해요. 살살 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `a3f3210aa04e87f15d20159ec11cf1421e34ce15adb85e40d715ff593159a978`

## nlu-step2-0170 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 1

### 원문 raw

미지근한 물 써요, 살살 문질러요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "미지근한 물 써요, 살살 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `0fcadafefe1e755d3546974f17440112248cddb09fa095680b2494ff5f410a25`

## nlu-step2-0171 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 2

### 원문 raw

물 온도 미지근함
살살 문질러요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 온도 미지근함\n살살 문질러요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `31a54a0c23e588394f8b30104a6d941a172e23d24394a127ec8a930df60052f6`

## nlu-step2-0172 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 3

### 원문 raw

물은 미지근해요. 문지를 때 힘 약하게 줘요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물은 미지근해요. 문지를 때 힘 약하게 줘요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `34011db9af9cf7757ae0a475efe9ed443d0826c89449ae6ab5eacc17f2fef25b`

## nlu-step2-0173 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 4

### 원문 raw

미지근한 물 써요 그리고 문지를 때 힘 약하게 줘요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "미지근한 물 써요 그리고 문지를 때 힘 약하게 줘요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `5af4462d957452542a9d10f35cf7c62f0d1283f831bfe421dee26b710ab872e8`

## nlu-step2-0174 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 5

### 원문 raw

물 온도 미지근함, 문지를 때 힘 약하게 줘요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 온도 미지근함, 문지를 때 힘 약하게 줘요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `5b025422f4557c1dad11d0c74dbcfc28733405fda9b99491f46a48b768220d91`

## nlu-step2-0175 · turn2_followup · train

의미 가족: `nlu-step2-warm_answer` / 표현 변형: 6

### 원문 raw

물은 미지근해요 / 문지르는 힘은 약해요

직전 질문: 쓰는 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물은 미지근해요 / 문지르는 힘은 약해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르는 힘은 약해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `ff4da09aa2d975f4df379ae191047323b8aa95535786f11bf36471cd0ffefc01`

## nlu-step2-0176 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 0

### 원문 raw

세정용 천으로 씻어요. 마무리는 물로 헹궈요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정용 천으로 씻어요. 마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정용 천으로 씻어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `dd44edb89fd2e961430542be50a8fab2b068c5229aba1c6b8a3783e43d711d15`

## nlu-step2-0177 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 1

### 원문 raw

도구는 세정용 천이에요, 마무리는 물로 헹궈요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구는 세정용 천이에요, 마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세정용 천이에요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7b895058c4ea20e9e5f9de96150b1e4801725029adcebc33e78e6de19671eba7`

## nlu-step2-0178 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 2

### 원문 raw

씻을 때 세정 천을 써요
마무리는 물로 헹궈요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻을 때 세정 천을 써요\n마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때 세정 천을 써요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `641b58b33feed23a1457a68cfc41dbe1b5cc12e4d12f124054e3897d2755c03a`

## nlu-step2-0179 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 3

### 원문 raw

세정용 천으로 씻어요. 마지막에 물로 씻어내요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정용 천으로 씻어요. 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정용 천으로 씻어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7af939d654dc63d6b84cb787316749a1903f90646fabb9499f03bbc837e9331a`

## nlu-step2-0180 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 4

### 원문 raw

도구는 세정용 천이에요 그리고 마지막에 물로 씻어내요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구는 세정용 천이에요 그리고 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구는 세정용 천이에요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `0f841c6accedf9082de288efd2ad121c35a8e9bb16b8b0af38c268b25c769131`

## nlu-step2-0181 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 5

### 원문 raw

씻을 때 세정 천을 써요, 마지막에 물로 씻어내요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻을 때 세정 천을 써요, 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때 세정 천을 써요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9582156e95dd3883c2c6a39c79e11d1cb7761cae41d2f5123396a0c5e2d2c878`

## nlu-step2-0182 · turn2_followup · train

의미 가족: `nlu-step2-tools_answer` / 표현 변형: 6

### 원문 raw

세정용 천으로 씻어요 / 끝에는 물 헹굼 해요

직전 질문: 어떤 도구로 씻나요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세정용 천으로 씻어요 / 끝에는 물 헹굼 해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "washcloth",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정용 천으로 씻어요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9d7f03de068ef4142cb20c34a90e5b11ea64649402d757350b429ba9eee2ae87`

## nlu-step2-0183 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 0

### 원문 raw

씻고 3분 뒤에 보습해요. 보습은 볼에만 해요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻고 3분 뒤에 보습해요. 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `5007274ef240b14ccbe13b1b24c6dbb2f9cdeb9295b6587ce0ffedfbe41eea7a`

## nlu-step2-0184 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 1

### 원문 raw

세안 후 보습까지 3분 걸려요, 보습은 볼에만 해요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 후 보습까지 3분 걸려요, 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `28a66392ce984ebb783427ee356032866199538b384bd79a1add73c3f26c4b9f`

## nlu-step2-0185 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 2

### 원문 raw

보습은 세안하고 삼 분 뒤예요
보습은 볼에만 해요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습은 세안하고 삼 분 뒤예요\n보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 세안하고 삼 분 뒤예요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `8eb473d21847184b3b20f67b834f3716ac6423f770df08d8ebd6aa18bb819692`

## nlu-step2-0186 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 3

### 원문 raw

씻고 3분 뒤에 보습해요. 보습 바르는 범위는 볼뿐이에요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻고 3분 뒤에 보습해요. 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `201717c2928fe7ba1a843272ff881ab241acae942f18cb68c919b208304b248e`

## nlu-step2-0187 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 4

### 원문 raw

세안 후 보습까지 3분 걸려요 그리고 보습 바르는 범위는 볼뿐이에요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 후 보습까지 3분 걸려요 그리고 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `f010ab7e633c05b44bbc61c31810cc45ac36c675d9756df661bf216cd22da5e8`

## nlu-step2-0188 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 5

### 원문 raw

보습은 세안하고 삼 분 뒤예요, 보습 바르는 범위는 볼뿐이에요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습은 세안하고 삼 분 뒤예요, 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 세안하고 삼 분 뒤예요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `4d7db4dcabbda2ab84a94baa8a193b58b29a78768f4a77092de6999a2a1a35b7`

## nlu-step2-0189 · turn2_followup · train

의미 가족: `nlu-step2-delay_answer` / 표현 변형: 6

### 원문 raw

씻고 3분 뒤에 보습해요 / 볼만 보습해요

직전 질문: 씻고 얼마 뒤 보습하나요?
질문 대상: moisturizing.after_wash_delay

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻고 3분 뒤에 보습해요 / 볼만 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "볼만 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `199535bef7e28152bbcf52c8e53a091b608e64e5caed5c9f9c70f6a7c6753e47`

## nlu-step2-0190 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 0

### 원문 raw

물이 닿지는 않았어요. 모자를 썼어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `484c1cd85e4419b9d747c61d1978cbc2fa28d68125a7748b0d97a18bb11e77c3`

## nlu-step2-0191 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 1

### 원문 raw

물 접촉은 없었어요, 모자를 썼어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요, 모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `6c6674b2a86cfd95d45fc24d384024de0410fffc179756bfb885bb4895639b89`

## nlu-step2-0192 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 2

### 원문 raw

물에 닿은 적 없음
모자를 썼어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음\n모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `dc5a42c84e1b92fc52b930b4b51cdf96488b5e8c08cec6d3c3809b16051fd4de`

## nlu-step2-0193 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 3

### 원문 raw

물이 닿지는 않았어요. 모자 쓰고 있었어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `69ab0f2faf259655e10674a9813c01feee016a08f50a6ba073226f9d329f5fab`

## nlu-step2-0194 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 4

### 원문 raw

물 접촉은 없었어요 그리고 모자 쓰고 있었어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요 그리고 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `c3306e295668683d507a3b93ab7830c202f8b48217fc39be8545eed1c7b12729`

## nlu-step2-0195 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 5

### 원문 raw

물에 닿은 적 없음, 모자 쓰고 있었어여

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음, 모자 쓰고 있었어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7ce7592894ebaf3b4a0eeb6bd1566b6359d9730e4ebcadb45abb741085cac90b`

## nlu-step2-0196 · turn2_followup · train

의미 가족: `nlu-step2-sun_answer` / 표현 변형: 6

### 원문 raw

물이 닿지는 않았어요 / 모자 착용했어요

직전 질문: 물에 들어간 적 있나요?
질문 대상: sun.water_contact

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요 / 모자 착용했어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 착용했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `0a0ff1eaf070d0433197087c030d7c109c5b5c369d6bdeaec87c21350bf7e99b`

## nlu-step2-0197 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 0

### 원문 raw

언제 열었는지 몰라요. 용기는 단지형이에요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "언제 열었는지 몰라요. 용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "언제 열었는지 몰라요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `45422a5dc33c8647657ec060d99c0d8c847585db5cdedc6661012cd1295c16a4`

## nlu-step2-0198 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 1

### 원문 raw

개봉한 날짜는 기억 안 나요, 용기는 단지형이에요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉한 날짜는 기억 안 나요, 용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉한 날짜는 기억 안 나요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `487447452bde23fbf2bfc3737864a5ce5777da7012e81ec27af3e43c3fb91b04`

## nlu-step2-0199 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 2

### 원문 raw

개봉일 잘 모르겠어요
용기는 단지형이에요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉일 잘 모르겠어요\n용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉일 잘 모르겠어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `86edf68cb72397838a9eeb8029304a40574eb5f36c14bb690f671c211d893be7`

## nlu-step2-0200 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 3

### 원문 raw

언제 열었는지 몰라요. 단지 형태 용기예요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "언제 열었는지 몰라요. 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "언제 열었는지 몰라요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `6718bc01c9c6bcd0266ec69e028576b781ec550417e2a7faa476b192627691cf`

## nlu-step2-0201 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 4

### 원문 raw

개봉한 날짜는 기억 안 나요 그리고 단지 형태 용기예요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉한 날짜는 기억 안 나요 그리고 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉한 날짜는 기억 안 나요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `74780a9b54b1d7d907e499ab1effaa85198a63052bf7ba81a6f7d8ca14e73807`

## nlu-step2-0202 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 5

### 원문 raw

개봉일 잘 모르겠어여, 단지 형태 용기예요

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉일 잘 모르겠어여, 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉일 잘 모르겠어여"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `53c6e7a15f44a3f69cfaf6507d9e854bb1fa8d6b0355f634f4b32712e45d7ba2`

## nlu-step2-0203 · turn2_followup · train

의미 가족: `nlu-step2-opened_unknown` / 표현 변형: 6

### 원문 raw

언제 열었는지 몰라요 / 통 모양은 단지형임

직전 질문: 언제 개봉했나요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "언제 열었는지 몰라요 / 통 모양은 단지형임",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "언제 열었는지 몰라요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 모양은 단지형임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `25a173922f90e5b07c054292c5e886e42bc38c8bcc2d628933af9bd300c4f797`

## nlu-step2-0204 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 0

### 원문 raw

횟수는 잘 모르겠어요. 손으로 씻어요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "횟수는 잘 모르겠어요. 손으로 씻어요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "횟수는 잘 모르겠어요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `157108b15839e19514fc0191fee11aae77fd3e28e56f5cd0f131ef3392399ab0`

## nlu-step2-0205 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 1

### 원문 raw

몇 번 씻는지는 기억 안 나요, 손으로 씻어요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몇 번 씻는지는 기억 안 나요, 손으로 씻어요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몇 번 씻는지는 기억 안 나요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `75a9b3c3df969cfa576f7a5342d4dc32e41f02fcb5a70e6db30242e8465a5d0d`

## nlu-step2-0206 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 2

### 원문 raw

세안 횟수는 모르겠음
손으로 씻어요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 횟수는 모르겠음\n손으로 씻어요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 횟수는 모르겠음"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `37a7a0104bb3b70dd1ec4f4d298acdda83056c29e460232b07f6b0b58ef171e9`

## nlu-step2-0207 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 3

### 원문 raw

횟수는 잘 모르겠어요. 세정 도구는 손이에요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "횟수는 잘 모르겠어요. 세정 도구는 손이에요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "횟수는 잘 모르겠어요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `dbf4cd0e480d41e8054ee5718ddc68af366639c44bf8b0d014045cc22b2d03be`

## nlu-step2-0208 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 4

### 원문 raw

몇 번 씻는지는 기억 안 나요 그리고 세정 도구는 손이에요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "몇 번 씻는지는 기억 안 나요 그리고 세정 도구는 손이에요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몇 번 씻는지는 기억 안 나요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `3c2375cf292b5d948a9216411ab5e2c286e063ff719bedce814c135e3c3cfcb2`

## nlu-step2-0209 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 5

### 원문 raw

세안 횟수는 모르겠음, 세정 도구는 손이에요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 횟수는 모르겠음, 세정 도구는 손이에요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 횟수는 모르겠음"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `2639fd30928acee8cb5c9e69f578b5860135a7c35afb29448a014161f755e759`

## nlu-step2-0210 · turn2_followup · train

의미 가족: `nlu-step2-count_unknown` / 표현 변형: 6

### 원문 raw

횟수는 잘 모르겠어요 / 손만 도구로 써요

직전 질문: 몇 번 세안하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "횟수는 잘 모르겠어요 / 손만 도구로 써요",
  "topics": [
    "repeat_cleansing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "횟수는 잘 모르겠어요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `12d75a075a9fd6fbd5364611fffeb9d80b4253ba86af2ee240f19698df9d11f6`

## nlu-step2-0211 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 0

### 원문 raw

보라 크림 B는 끊었어요. 보습 후 느낌이 끈적해요

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 보습 후 느낌이 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌이 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `ef2859b5525f1120b79ae0adb3076fd4a4104be1d32aae9b3e7ef3e1a709f561`

## nlu-step2-0212 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 1

### 원문 raw

보라 크림 B 사용 중단했어요, 보습 후 느낌이 끈적해요

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요, 보습 후 느낌이 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌이 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `d5a6dbae73b78aa3527efa8d2432596f400e86aaf515fac2b251e0dad104ef42`

## nlu-step2-0213 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 2

### 원문 raw

보라 크림 B 이제 안 써요
보습 후 느낌이 끈적해요

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요\n보습 후 느낌이 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌이 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `1b30720ea15c19f84bbd7d4031ad7d0a92f48fa7ec1f27e7d4685851772faa4b`

## nlu-step2-0214 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 3

### 원문 raw

보라 크림 B는 끊었어요. 보습하고 나면 끈적함

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `dba3bab1858963222d7a83360545aa627adb0af5df953b8a7d69815bff4e1bee`

## nlu-step2-0215 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 4

### 원문 raw

보라 크림 B 사용 중단했어요 그리고 보습하고 나면 끈적함

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요 그리고 보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `e4e22be313d8a41b58f22ee795bba96f22493d927330b2cb97244c465522e405`

## nlu-step2-0216 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 5

### 원문 raw

보라 크림 B 이제 안 써요, 보습하고 나면 끈적함

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요, 보습하고 나면 끈적함",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `02099e0fc12e2b6bca165938e735f3dffce846405058a7af7a246028abd0b7e2`

## nlu-step2-0217 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_temperature` / 표현 변형: 6

### 원문 raw

보라 크림 B는 끊었어요 / 보습 뒤 감촉은 끈적해요

직전 질문: 물 온도는 어떤가요?
질문 대상: method.water_temperature

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요 / 보습 뒤 감촉은 끈적해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `3db3735e36d88d96f30b2b77d9852ac75340f79a2f47a6a1c91236abdf6b54e9`

## nlu-step2-0218 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 0

### 원문 raw

방금 처음 가려워요. 아프지는 않아요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 가려워요. 아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 가려워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `e21b541507892a50e2bdc22b6b5d9a95a12453dc2cf07280ecb246433dc487f2`

## nlu-step2-0219 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 1

### 원문 raw

조금 전에 처음 가려움, 아프지는 않아요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 가려움, 아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 가려움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `f99beac49d250868027bee618b40d806087b04c16de3d7f172a8eca6e3992f3d`

## nlu-step2-0220 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 2

### 원문 raw

아까 처음 가려워서 말해요
아프지는 않아요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 가려워서 말해요\n아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 가려워서 말해요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `1fb5606b49c8c8b7e9b223975f2927a72978362e7a0898e376947d90c90e3bd9`

## nlu-step2-0221 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 3

### 원문 raw

방금 처음 가려워요. 통증은 없어요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 가려워요. 통증은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 가려워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `0c73bfb477790b4cff9d33aa5b273cd371129fa62f4021a85fd2e9341189bb54`

## nlu-step2-0222 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 4

### 원문 raw

조금 전에 처음 가려움 그리고 통증은 없어요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 가려움 그리고 통증은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 가려움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7581b7f1e1308b4263cb3242a3d43b1c3763b93517e5341eadd702206ff0bf4a`

## nlu-step2-0223 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 5

### 원문 raw

아까 처음 가려워서 말해여, 통증은 없어여

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 가려워서 말해여, 통증은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 가려워서 말해여"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7f2b97a9e2a6504b538ed3cdf70354371fe1c18f03cfa863dc43e413bc271c71`

## nlu-step2-0224 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_symptom` / 표현 변형: 6

### 원문 raw

방금 처음 가려워요 / 아픈 건 아님

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 가려워요 / 아픈 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 가려워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아픈 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `2bba2700c2731e0a1d703d7e208264be034a108751b26aea2ec5e9f0456d149c`

## nlu-step2-0225 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 0

### 원문 raw

개봉 후 6개월 표시예요. 사용기한은 2027년 8월로 적혀요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉 후 6개월 표시예요. 사용기한은 2027년 8월로 적혀요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `223beac17667e62305fffd863ff4296aee4ce070c2ea83bc6294d23930415cc2`

## nlu-step2-0226 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 1

### 원문 raw

개봉 뒤 여섯 달이라고 써 있어요, 사용기한은 2027년 8월로 적혀요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉 뒤 여섯 달이라고 써 있어요, 사용기한은 2027년 8월로 적혀요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `8359e4f789746f06802b0fe0fdd4ecd5a3a255a9606a3d2dc21488bcd39f8aba`

## nlu-step2-0227 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 2

### 원문 raw

열고 6개월 이내라고 적혀요
사용기한은 2027년 8월로 적혀요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열고 6개월 이내라고 적혀요\n사용기한은 2027년 8월로 적혀요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `76282542b5e80953d19ce4e962abd3dfc27fa8aebe7801dd851f8eb41e3c8ac3`

## nlu-step2-0228 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 3

### 원문 raw

개봉 후 6개월 표시예요. 2027년 8월이 사용기한이에요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉 후 6개월 표시예요. 2027년 8월이 사용기한이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `1c3ba303f141ccfa7d3b9bf87f7b7eaae8a66b8bcca83af53413b8a6db8ca51a`

## nlu-step2-0229 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 4

### 원문 raw

개봉 뒤 여섯 달이라고 써 있어요 그리고 2027년 8월이 사용기한이에요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉 뒤 여섯 달이라고 써 있어요 그리고 2027년 8월이 사용기한이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `fca3a4772fdeba6a1346a58272fa9a458548f6fa5feb6e6132d19ef8f62c77e9`

## nlu-step2-0230 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 5

### 원문 raw

열고 6개월 이내라고 적혀요, 2027년 8월이 사용기한이에요

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열고 6개월 이내라고 적혀요, 2027년 8월이 사용기한이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `75fe19a5f7469352dc6a6c3ca085bdc3c41fe6423ca384f940a7bc7fefdb3544`

## nlu-step2-0231 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_storage` / 표현 변형: 6

### 원문 raw

개봉 후 6개월 표시예요 / 사용기한 표시 2027년 8월임

직전 질문: 땀이 났나요?
질문 대상: sun.sweat

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "개봉 후 6개월 표시예요 / 사용기한 표시 2027년 8월임",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `42a910669b918776580e0a136084431bc6e54a453fd52bdcc196c19053567ec9`

## nlu-step2-0232 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 0

### 원문 raw

다온 젤 C 살까 고민해요. 물은 미지근해요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요. 물은 미지근해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `72bd87094a0ece99e8d32abb8966ebd743802526587d8f5a921771692efe308a`

## nlu-step2-0233 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 1

### 원문 raw

다온 젤 C 써볼까 생각 중, 물은 미지근해요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 써볼까 생각 중, 물은 미지근해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `317a6d624516cb9c38ffab2beca8b5fc10b39f23f8db8707085ba7606536b6f5`

## nlu-step2-0234 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 2

### 원문 raw

다온 젤 C 구매 고려 중이에요
물은 미지근해요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 구매 고려 중이에요\n물은 미지근해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `2665202bdf11a9581382f77039b957cc7afcb1975a747766ee8b2d2e6f1fc4d2`

## nlu-step2-0235 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 3

### 원문 raw

다온 젤 C 살까 고민해요. 미지근한 물 써요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요. 미지근한 물 써요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `4f28562ee84925d6de73b1328e73fdd741c0df2221e7b474123a84c9ecf16c71`

## nlu-step2-0236 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 4

### 원문 raw

다온 젤 C 써볼까 생각 중 그리고 미지근한 물 써요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 써볼까 생각 중 그리고 미지근한 물 써요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `839fb6f73e65f75599688eb602e15dfdf3ce360ef9fdbb97a3f8aa622cd74187`

## nlu-step2-0237 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 5

### 원문 raw

다온 젤 C 구매 고려 중이에요, 미지근한 물 써요

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 구매 고려 중이에요, 미지근한 물 써요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `c579cff18db271600bfedeb7a307ba3a3af3ccaf16f82ce62baaec34ef7810cc`

## nlu-step2-0238 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_product` / 표현 변형: 6

### 원문 raw

다온 젤 C 살까 고민해요 / 물 온도 미지근함

직전 질문: 언제 열었는지 알려 주세요.
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요 / 물 온도 미지근함",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `38322672803ea438930b839c42992a0cb8a4428fbf77b4882da13132c4ef6f53`

## nlu-step2-0239 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 0

### 원문 raw

땀이 흐를 때마다 눈이 시려요. 야외에 오래 있었어요

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요. 야외에 오래 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `f86e38a1a9917e227ed6636a1e5f63e295e60abef26446047eb0ad2047f9b472`

## nlu-step2-0240 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 1

### 원문 raw

땀 흐르면 매번 눈따가움, 야외에 오래 있었어요

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 흐르면 매번 눈따가움, 야외에 오래 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9c1473d8f5a69b3f99b38fdd2d2c9524c979f7d7391fb5317d530e37b4edf0cd`

## nlu-step2-0241 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 2

### 원문 raw

땀이 흘러내릴 때마다 눈이 따가워요
야외에 오래 있었어요

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흘러내릴 때마다 눈이 따가워요\n야외에 오래 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `330e8d7791b500f02c52d756e6f10d6f3cf634c150109a29269f0854c3a2a081`

## nlu-step2-0242 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 3

### 원문 raw

땀이 흐를 때마다 눈이 시려요. 밖에서 오래 머물렀어요

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요. 밖에서 오래 머물렀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `746d1a75dc0e0bdc7746594bc75fdb8afe3afe8623bb4f72d405e7643d9e24ea`

## nlu-step2-0243 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 4

### 원문 raw

땀 흐르면 매번 눈따가움 그리고 밖에서 오래 머물렀어요

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 흐르면 매번 눈따가움 그리고 밖에서 오래 머물렀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `d4fbb2ce2d23563f930e7cb1e2a3d30b5b43884c5ce315dc8ffba7baad32bbaa`

## nlu-step2-0244 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 5

### 원문 raw

땀이 흘러내릴 때마다 눈이 따가워요, 밖에서 오래 머물렀어여

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흘러내릴 때마다 눈이 따가워요, 밖에서 오래 머물렀어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `9bb696fb77153ac6e41df698d829c4214ac92bf16ba79ffa50fab58abac45e02`

## nlu-step2-0245 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_eye` / 표현 변형: 6

### 원문 raw

땀이 흐를 때마다 눈이 시려요 / 오랫동안 야외에 있었음

직전 질문: 어디에 보습제를 바르나요?
질문 대상: moisturizing.coverage

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요 / 오랫동안 야외에 있었음",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "오랫동안 야외에 있었음"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `f7ffa96c0e7b186724889355bdfb3670e2d6463270f2a4c66e65ed75a4188a9e`

## nlu-step2-0246 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 땀이 났어요. 그늘에 머물렀어요

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 났어요. 그늘에 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `709f8f93568589aac03df80a09f03107d98f2c65ce2cf1c8042fdf2b48d59287`

## nlu-step2-0247 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 땀 흘렸어요, 그늘에 머물렀어요

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀 흘렸어요, 그늘에 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7ee1d556b5b7bc0dc903d1508dff1f211b0fb822a37ca9188d2dfec7ee0b4a78`

## nlu-step2-0248 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 땀이 많이 남
그늘에 머물렀어요

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 많이 남\n그늘에 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `4736b493b8b183383b3628093bcb0d5f6cbdc6d0f0d239b724cea4ba301f50b1`

## nlu-step2-0249 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 땀이 났어요. 그늘에서 있었어요

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 났어요. 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `7808b0f8b81fb9f82815ee3359d0f135d1c5fd2ac728f80ad0f17ac066424307`

## nlu-step2-0250 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 땀 흘렸어요 그리고 그늘에서 있었어요

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀 흘렸어요 그리고 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `616ef402530c864977bfb842d4fe80326022c3b4efb01e73d688612bd12181eb`

## nlu-step2-0251 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 땀이 많이 남, 그늘에서 있었어여

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 많이 남, 그늘에서 있었어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `5e71fa3d5fa4bd8fccb1375b92430bdd61bc9d4b63e54e13b79f67fc806369e3`

## nlu-step2-0252 · turn2_followup · train

의미 가족: `nlu-step2-offtopic_other` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 땀이 났어요 / 그늘에 있었음

직전 질문: 세정 도구는 뭔가요?
질문 대상: method.tools

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 났어요 / 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.

내용 SHA-256: `a8c5744effccc7b97fbaa84767bb470a043a4188f4474b536843cfc7f64bc15b`

## nlu-step2-0253 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 0

### 원문 raw

그 질문은 패스할게요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그 질문은 패스할게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `0d13093cc1d02c141f7f35518634ce297771e022d493e121a7be5ce648cb3ed9`

## nlu-step2-0254 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 1

### 원문 raw

이건 답하고 싶지 않아요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이건 답하고 싶지 않아요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `65f1363b65d1b542058a294f18419ff369cd0f1b817fe3513e95e6ebb124516a`

## nlu-step2-0255 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 2

### 원문 raw

이번 질문은 건너뛸게요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이번 질문은 건너뛸게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `bd69cae9750af2f85e86c9af4aac994b3860f541226015fb9e54c365625c3af8`

## nlu-step2-0256 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 3

### 원문 raw

이 질문엔 응답 안 할게요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이 질문엔 응답 안 할게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `5b65fa42d746c1854335806bfc6c5f79654fb7736eb0276e7114fd201f2e38e3`

## nlu-step2-0257 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 4

### 원문 raw

대답은 안 할래요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "대답은 안 할래요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `ca2447abb911102f31e899952bc7b613ffaaf642df1321b1981103fc07f9e74c`

## nlu-step2-0258 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 5

### 원문 raw

지금 질문은 넘어가요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지금 질문은 넘어가요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `1490bc2e9f41f92fa441abd5691c5eae2b312695c358f6df5c73adabcdec751a`

## nlu-step2-0259 · turn2_followup · train

의미 가족: `nlu-step2-refuse` / 표현 변형: 6

### 원문 raw

이건 말하지 않을게요

직전 질문: 개봉일은 언제인가요?
질문 대상: storage.opened_at

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이건 말하지 않을게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `7930c78d21e7207ff90499b8f5160dfb17e5e12432c6ce5fa043db075ed5501e`

## nlu-step2-0260 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 0

### 원문 raw

잘 모르겠어요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "잘 모르겠어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "잘 모르겠어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `f81a94db6a88605dc107c68f6ddc249f9c2141008f85eec5a6fa2e90ee79c6af`

## nlu-step2-0261 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 1

### 원문 raw

그건 기억 안 나요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그건 기억 안 나요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그건 기억 안 나요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `af3f511f1315be47a277411f24dea4587c97ae0f89e8efe3aa39b134acc7d6d1`

## nlu-step2-0262 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 2

### 원문 raw

확실히는 몰라요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "확실히는 몰라요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "확실히는 몰라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `ba544fa41b7dd5f2f024ee6c0288da026b707ec3fca165f581ba6891b07cd515`

## nlu-step2-0263 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 3

### 원문 raw

잘 생각이 안 나네요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "잘 생각이 안 나네요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "잘 생각이 안 나네요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `1b90d4b436156304338b20c72dbaaf5356c7b81569b4db7a6ff4e7c8bb610854`

## nlu-step2-0264 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 4

### 원문 raw

답을 모르겠네요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "답을 모르겠네요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "답을 모르겠네요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `1e3fb1c4f626f7848b89dc840b090de29a073cec4ff95c72e02e7d5f50c68904`

## nlu-step2-0265 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 5

### 원문 raw

그건 모르겠음

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그건 모르겠음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그건 모르겠음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `609121477ecb3c29c0079a9537d8fc62fdb1d6d9eb43c66e18373b3abf1ac4b7`

## nlu-step2-0266 · turn2_followup · train

의미 가족: `nlu-step2-uncertain_bare` / 표현 변형: 6

### 원문 raw

정확히 기억 못 해요

직전 질문: 차단제는 언제 덧발랐나요?
질문 대상: sun.reapplication

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "정확히 기억 못 해요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.reapplication",
      "value": null,
      "polarity": "unknown",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "정확히 기억 못 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `75b7ee15f113f329edfe03cd2854d54a1614ba538b5107b3c682df6331da493e`

## nlu-step2-0267 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 0

### 원문 raw

기차가 또 늦었네요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 또 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `5662d4cd1c420669dc7853a27457c194b57884c7776b46c3669e5fbc613d08f7`

## nlu-step2-0268 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 1

### 원문 raw

방금 노래가 끝났어요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 노래가 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `3d9711597c0965337dec91f367f3e8b0d88df3008a3a783c7a7abccb16eb5fb9`

## nlu-step2-0269 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 2

### 원문 raw

저 지금 표 예매 중이에요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저 지금 표 예매 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `ace5b5fcb1912e103d0479ed3f8f3d31b81c090b535288c56e8d5520d4bf0951`

## nlu-step2-0270 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 3

### 원문 raw

영화표 예약했어요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화표 예약했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `3c6658a8fa185083bbea5e00204b891b7663bfe67486ba05949de9fea7232dda`

## nlu-step2-0271 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 4

### 원문 raw

벽시계 멈춘 거 같네요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계 멈춘 거 같네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `322395514241b9bffc65009f64b5a1547b8b06470c7ac92064b86d0e27a829fd`

## nlu-step2-0272 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 5

### 원문 raw

키보드가 고장났어여

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드가 고장났어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `dc89695775cbf7bcde1876ac4254310c44141c25478e6671d45c57456ea24c64`

## nlu-step2-0273 · turn2_followup · val_internal

의미 가족: `nlu-step2-topic_drift` / 표현 변형: 6

### 원문 raw

택배 조회하고 있었어요

직전 질문: 몇 번 씻으세요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배 조회하고 있었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `dcf39c32b057ea54248b27e588decebc8fc62611b19a7f703001d53531b8b5dd`

## nlu-step2-0274 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 0

### 원문 raw

그건 비공개로 할게요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그건 비공개로 할게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `0076967c2908f96c1c57facff7475cf7649179b06be564a72156a0c79fa9f63b`

## nlu-step2-0275 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 1

### 원문 raw

그 내용은 공유 안 할래요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그 내용은 공유 안 할래요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `7793f9b1f4b97be73a0b1480c9288fe077e44179e2a1d4310f8108a7e7078154`

## nlu-step2-0276 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 2

### 원문 raw

사적인 답은 보류할게요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "사적인 답은 보류할게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `b723870559564d607a43b2492efba22556ee53f74db90c47ea79b5116066b1ba`

## nlu-step2-0277 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 3

### 원문 raw

그 질문은 개인적으로 남길게요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그 질문은 개인적으로 남길게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `a90e43889635704333de15dbb71d3fa062b64ce9ecbfa6fc4ece224b4369ba90`

## nlu-step2-0278 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 4

### 원문 raw

이 답은 공개하고 싶지 않아요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이 답은 공개하고 싶지 않아요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `fe9d7c6645dada62183483fc61291877ca87007111e8f1e1bfe2d357ad1500f8`

## nlu-step2-0279 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 5

### 원문 raw

이 부분은 알려드리지 않을게요

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이 부분은 알려드리지 않을게요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `c17ad845ad62ed7100e66570b7a7dcfde71d6f68576b1f38020f193c55de87fc`

## nlu-step2-0280 · turn2_followup · val_internal

의미 가족: `nlu-step2-refuse_val` / 표현 변형: 6

### 원문 raw

그 정보는 말하지 않겠습니다

직전 질문: 지금 루틴을 알려 주세요.
질문 대상: method.current_routine

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "그 정보는 말하지 않겠습니다",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.

내용 SHA-256: `14a9523426ba00b7fdd1dfa156579bedc863e1e8ee5e6d18a6c53238956184c5`

## nlu-step2-0281 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 0

### 원문 raw

물이 닿지는 않았어요. 야외에 오래 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 야외에 오래 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `afbebba206ccfcfb9dc347568bd6d798db33fe95f3cf12a2a79a322d1717ffe9`

## nlu-step2-0282 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 1

### 원문 raw

물 접촉은 없었어요, 야외에 오래 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요, 야외에 오래 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `49603c961b1d0f1d3c58dee0429d01d1a1dcf2e0fc72645a6155f94141e82a60`

## nlu-step2-0283 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 2

### 원문 raw

물에 닿은 적 없음
야외에 오래 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음\n야외에 오래 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "야외에 오래 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `f1e48e82f81bf3cee80783f5b6d14ddb87e67ddece5cc7a7f91058dbbf3680ba`

## nlu-step2-0284 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 3

### 원문 raw

물이 닿지는 않았어요. 밖에서 오래 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 밖에서 오래 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `3d5f54e8a365c789d066cb6f7c69f5a75ae9332dca9020cc0f8ab404ffecbfd5`

## nlu-step2-0285 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 4

### 원문 raw

물 접촉은 없었어요 그리고 밖에서 오래 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요 그리고 밖에서 오래 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `7be818df2d91edd9251bfc999fe725fe72a9de7e023996e7f0453b236306b19e`

## nlu-step2-0286 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 5

### 원문 raw

물에 닿은 적 없음, 밖에서 오래 머물렀어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음, 밖에서 오래 머물렀어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "밖에서 오래 머물렀어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `f54cc8361d320d6949e20170588b0e7c8a663b4a1b2aba7b3b6147a8103ec8f8`

## nlu-step2-0287 · denied_polarity · train

의미 가족: `nlu-step2-water_negative` / 표현 변형: 6

### 원문 raw

물이 닿지는 않았어요 / 오랫동안 야외에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요 / 오랫동안 야외에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "오랫동안 야외에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `1487612d57c8c46972d33d1d6294916a1055aa037adf762f9aa6974a8b0713ac`

## nlu-step2-0288 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 0

### 원문 raw

땀은 안 났어요. 모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀은 안 났어요. 모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ef28f8561d69afd546e9e282430cb30b757577a6496ee96e2b865ca842cb049b`

## nlu-step2-0289 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 1

### 원문 raw

땀 안 흘렸어요, 모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 안 흘렸어요, 모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `fd5df5bf86469511d92a2a0e5dfd2a813ed8560c60373b12afd69ecf0011677e`

## nlu-step2-0290 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 2

### 원문 raw

땀난 건 아니에요
모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀난 건 아니에요\n모자를 썼어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `496d1cc92be300d5f2729eba0f78881933739f21fb6708baee8a3ba94e6b09ff`

## nlu-step2-0291 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 3

### 원문 raw

땀은 안 났어요. 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀은 안 났어요. 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9f6849d96e8fd2400952cef12161e08e35a6ec7a2f328139400dbd0a9231e716`

## nlu-step2-0292 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 4

### 원문 raw

땀 안 흘렸어요 그리고 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 안 흘렸어요 그리고 모자 쓰고 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `eb1b2e80768dc273ae4e6bd94ba5f00d8cae1fa34c74adf4bb3731394da4f787`

## nlu-step2-0293 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 5

### 원문 raw

땀난 건 아니에요, 모자 쓰고 있었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀난 건 아니에요, 모자 쓰고 있었어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `3bb657b6cf08269129d0ff03fc8ac8d0a2a91cb003798ef8ad26ed8293a0a1fc`

## nlu-step2-0294 · denied_polarity · train

의미 가족: `nlu-step2-sweat_negative` / 표현 변형: 6

### 원문 raw

땀은 안 났어요 / 모자 착용했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀은 안 났어요 / 모자 착용했어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자 착용했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `339b8b4de033b37d198616ee3d7fc8cf7928a84ea7e77c10fb8dbb5a801649ac`

## nlu-step2-0295 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 0

### 원문 raw

물이 닿지는 않았어요. 땀은 안 났어요. 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 땀은 안 났어요. 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ea11fe56eaa3becd7cf276e82402824b58ba6f3e2e8a43ef63f9b24e6a99186b`

## nlu-step2-0296 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 1

### 원문 raw

물 접촉은 없었어요, 땀은 안 났어요, 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요, 땀은 안 났어요, 그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `325a549d4cd9ebc90d0d181a3a894fae149d5be8549ec43a2e4951cc068d4c8f`

## nlu-step2-0297 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 2

### 원문 raw

물에 닿은 적 없음
땀은 안 났어요
그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음\n땀은 안 났어요\n그늘에서 있었어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9085ffa2751c412bbcd6ee5a441e9e417a3334cc3fa6cce5c8a776105579cb5c`

## nlu-step2-0298 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 3

### 원문 raw

물이 닿지는 않았어요. 땀 안 흘렸어요. 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 땀 안 흘렸어요. 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `10129f6c0aad6313fdbe2e4a77a71bdd520926cae368eb3e38bd03eac53ac6a1`

## nlu-step2-0299 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 4

### 원문 raw

물 접촉은 없었어요 그리고 땀 안 흘렸어요 그리고 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요 그리고 땀 안 흘렸어요 그리고 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `572ab23c80daa2cee1401e59933ec3653c99d2ad75e0720161e2596c8715fe24`

## nlu-step2-0300 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 5

### 원문 raw

물에 닿은 적 없음, 땀 안 흘렸어여, 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음, 땀 안 흘렸어여, 그늘에 있었음",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어여"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `169fadc9d30a117afc60151ae181bc1ab8237d621f8e8787b08b8a8a604b82e6`

## nlu-step2-0301 · denied_polarity · train

의미 가족: `nlu-step2-two_negatives` / 표현 변형: 6

### 원문 raw

물이 닿지는 않았어요 / 땀난 건 아니에요 / 그늘에 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요 / 땀난 건 아니에요 / 그늘에 머물렀어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9d420c77182bfa86ffb67b6b1232a13b3eabdb905da9eb3fb9f1981769bd8824`

## nlu-step2-0302 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 0

### 원문 raw

뜨거운 물은 안 써요. 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨거운 물은 안 써요. 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "뜨거운 물은 안 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b948a0dd9af50dd4cbc643fc0d19e2f43acc2b3989f47d0ade463ed39015f4ea`

## nlu-step2-0303 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 1

### 원문 raw

물은 뜨겁지는 않아요, 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물은 뜨겁지는 않아요, 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 뜨겁지는 않아요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4268a40768072ab5957cab8f5d712a2abb5632741dd07db2563234bfced3bfc3`

## nlu-step2-0304 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 2

### 원문 raw

뜨겁게는 안 해요
손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨겁게는 안 해요\n손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "뜨겁게는 안 해요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `2d0d2e816db614ae1b641be0ece60ee04167ae13200b94b786a1569f54931c17`

## nlu-step2-0305 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 3

### 원문 raw

뜨거운 물은 안 써요. 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨거운 물은 안 써요. 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "뜨거운 물은 안 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b8a411300fa1176ab789ea87956821c31994923e72c09b2d36b3c023fc52ead6`

## nlu-step2-0306 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 4

### 원문 raw

물은 뜨겁지는 않아요 그리고 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물은 뜨겁지는 않아요 그리고 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 뜨겁지는 않아요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d17170ce06bf7b44aa869768c61a0236506605e767541c5f4170a0b27cd79cf4`

## nlu-step2-0307 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 5

### 원문 raw

뜨겁게는 안 해여, 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨겁게는 안 해여, 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "뜨겁게는 안 해여"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `57c59fb28db3b96897d642cd57b2a1eb3f45271abc3573641e566c07255a60d7`

## nlu-step2-0308 · denied_polarity · train

의미 가족: `nlu-step2-not_hot_hand` / 표현 변형: 6

### 원문 raw

뜨거운 물은 안 써요 / 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨거운 물은 안 써요 / 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "hot",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "뜨거운 물은 안 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `96a6d469642d721adb7c1031c1acf9df17d19ca6c459727b9af315196d233c01`

## nlu-step2-0309 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 0

### 원문 raw

브러시는 안 써요. 물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시는 안 써요. 물은 미지근해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "브러시는 안 써요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `fe26dc66e05019be2e1ca3037152fbdb3e67ff4c53fcef41cf9917a6e1410c8c`

## nlu-step2-0310 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 1

### 원문 raw

세안 브러시 안 씀, 물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 브러시 안 씀, 물은 미지근해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 브러시 안 씀"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ca23f30150e1ba3d45854eef1496968b340b88c51be6f5156db344796e5af56c`

## nlu-step2-0311 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 2

### 원문 raw

도구로 브러시 쓰진 않아요
물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구로 브러시 쓰진 않아요\n물은 미지근해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구로 브러시 쓰진 않아요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `e19ad39ff544fca7733747ee87c24daaead4da6f5b22fd41b39504694c9e72c3`

## nlu-step2-0312 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 3

### 원문 raw

브러시는 안 써요. 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시는 안 써요. 미지근한 물 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "브러시는 안 써요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `503997ce266cee59d6c1ece101a7cdeae3e40046ff950a2a95b99eee08460d74`

## nlu-step2-0313 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 4

### 원문 raw

세안 브러시 안 씀 그리고 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안 브러시 안 씀 그리고 미지근한 물 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 브러시 안 씀"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `c8d1e5b6b4ed0f1eeaad9fcaad549a610193c6ff61bcc5c0d8540a718a595f2a`

## nlu-step2-0314 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 5

### 원문 raw

도구로 브러시 쓰진 않아요, 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "도구로 브러시 쓰진 않아요, 미지근한 물 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "도구로 브러시 쓰진 않아요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `96082485de720d9cafee86e9c2f5f32e7b74ab0a16ba124d3c5adedbe70a2706`

## nlu-step2-0315 · denied_polarity · train

의미 가족: `nlu-step2-not_brush_warm` / 표현 변형: 6

### 원문 raw

브러시는 안 써요 / 물 온도 미지근함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시는 안 써요 / 물 온도 미지근함",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "브러시는 안 써요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `7a8eb41add11fd5af6de509dfaf158c87dd77c0f52b0a5868ddcaa859dc90f6f`

## nlu-step2-0316 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 0

### 원문 raw

세게 문지르진 않아요. 얼굴만 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세게 문지르진 않아요. 얼굴만 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문지르진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `1017061605301707bfd864ec74018eedc39e8abac97bd6bf0443076fd76afed5`

## nlu-step2-0317 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 1

### 원문 raw

박박 비비는 건 아니에요, 얼굴만 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "박박 비비는 건 아니에요, 얼굴만 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "박박 비비는 건 아니에요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `982369012fae029ea45925f480b75293ed7d52422fd4d4c95e38162859313281`

## nlu-step2-0318 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 2

### 원문 raw

강하게 문지르는 건 안 해요
얼굴만 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "강하게 문지르는 건 안 해요\n얼굴만 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "강하게 문지르는 건 안 해요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴만 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b033bc6374532c2db5c7fc2b7ffc94f2234248f68e449633da4b91a08935febf`

## nlu-step2-0319 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 3

### 원문 raw

세게 문지르진 않아요. 세안 부위는 얼굴이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세게 문지르진 않아요. 세안 부위는 얼굴이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문지르진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 부위는 얼굴이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `22675537ec3f9f976806a908682f003fd5ad38e45dc0da1ef57114e725744648`

## nlu-step2-0320 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 4

### 원문 raw

박박 비비는 건 아니에요 그리고 세안 부위는 얼굴이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "박박 비비는 건 아니에요 그리고 세안 부위는 얼굴이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "박박 비비는 건 아니에요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 부위는 얼굴이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `68f0ff4e72dc730b23c4b128c95d1b7eda9daee6930a86a49498c3bfa0e8eb0d`

## nlu-step2-0321 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 5

### 원문 raw

강하게 문지르는 건 안 해여, 세안 부위는 얼굴이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "강하게 문지르는 건 안 해여, 세안 부위는 얼굴이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "강하게 문지르는 건 안 해여"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 부위는 얼굴이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4d897098411945afd372abf3f88a4ec79d0e501c882e99772ca651fde578a236`

## nlu-step2-0322 · denied_polarity · train

의미 가족: `nlu-step2-not_force_face` / 표현 변형: 6

### 원문 raw

세게 문지르진 않아요 / 얼굴 씻는 얘기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세게 문지르진 않아요 / 얼굴 씻는 얘기예요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문지르진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴 씻는 얘기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `545108dd0bc89541ed80ce99c425fea3fdfc8e9c7105c1d6ed2d60e74fd2e5dc`

## nlu-step2-0323 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 0

### 원문 raw

수건으로 세게 비비진 않아요. 몸을 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 세게 비비진 않아요. 몸을 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 세게 비비진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0d761447d381fa9f831928ed91656922aa8f8e1b24da5a56b0c1b781c51651b5`

## nlu-step2-0324 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 1

### 원문 raw

물기 닦을 때 박박 문지르지 않아요, 몸을 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물기 닦을 때 박박 문지르지 않아요, 몸을 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 때 박박 문지르지 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4706c25ac3c9c7331dd6fe8d51c836384443903048c33b895eab2013ce142b79`

## nlu-step2-0325 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 2

### 원문 raw

수건으로 강하게 문지르진 않음
몸을 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 강하게 문지르진 않음\n몸을 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 강하게 문지르진 않음"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸을 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `be81988e4be77d8709d147b4059cf809da7d655b39d6667f4a3648b605f236c0`

## nlu-step2-0326 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 3

### 원문 raw

수건으로 세게 비비진 않아요. 몸 씻는 얘기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 세게 비비진 않아요. 몸 씻는 얘기예요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 세게 비비진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸 씻는 얘기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `a738c80173d5dfbf8dfed65f306bd69432000447cd6d41fe97e54e7f1bcef991`

## nlu-step2-0327 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 4

### 원문 raw

물기 닦을 때 박박 문지르지 않아요 그리고 몸 씻는 얘기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물기 닦을 때 박박 문지르지 않아요 그리고 몸 씻는 얘기예요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 때 박박 문지르지 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸 씻는 얘기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0a5ef39e4b38589238dae30c2a65c9f9109fa4cf15e724a0d7715c6c9c969eb4`

## nlu-step2-0328 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 5

### 원문 raw

수건으로 강하게 문지르진 않음, 몸 씻는 얘기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 강하게 문지르진 않음, 몸 씻는 얘기예요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 강하게 문지르진 않음"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "몸 씻는 얘기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `2ef5398124cd7eeed0532497345444f73bf003ca998d716b6b78d73dba734b86`

## nlu-step2-0329 · denied_polarity · train

의미 가족: `nlu-step2-not_rubbing` / 표현 변형: 6

### 원문 raw

수건으로 세게 비비진 않아요 / 이번 세정 부위는 몸이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 세게 비비진 않아요 / 이번 세정 부위는 몸이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로 세게 비비진 않아요"
    },
    {
      "variable_id": "method.body_site",
      "value": "body",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이번 세정 부위는 몸이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9df5fefef0883030eeb0929d233216099ebf0eeb3d7a4bbc75d5f61b649ea733`

## nlu-step2-0330 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 0

### 원문 raw

용기 안에 물은 안 들어갔어요. 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물은 안 들어갔어요. 용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물은 안 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `26034371fc5f85df860380ae0ff874831b7035e2c068044c66dc5b5425cc619b`

## nlu-step2-0331 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 1

### 원문 raw

안으로 물이 들어간 건 아니에요, 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "안으로 물이 들어간 건 아니에요, 용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "안으로 물이 들어간 건 아니에요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `c16e4ca4c7e471a799a3ce364417fc8ddff480b4f9fba8c20775cfcb3596693b`

## nlu-step2-0332 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 2

### 원문 raw

통 안 물 유입은 없어요
용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통 안 물 유입은 없어요\n용기는 단지형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 안 물 유입은 없어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0f26729c2100c48e0fe49c18809748f0026efb216b33874bf2fca778f7be9b49`

## nlu-step2-0333 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 3

### 원문 raw

용기 안에 물은 안 들어갔어요. 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물은 안 들어갔어요. 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물은 안 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `31c6710c4e18d80db60b5226256e660e7e11bc92659fac8cd198f85976f429c5`

## nlu-step2-0334 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 4

### 원문 raw

안으로 물이 들어간 건 아니에요 그리고 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "안으로 물이 들어간 건 아니에요 그리고 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "안으로 물이 들어간 건 아니에요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `287b921c39719fe7f20964060e7be01a9464cafb5b8a86c3a6fe08e4df75cca3`

## nlu-step2-0335 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 5

### 원문 raw

통 안 물 유입은 없어여, 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통 안 물 유입은 없어여, 단지 형태 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 안 물 유입은 없어여"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `445fb5d8b4aec825ab618fec393d3376eca9451849a7ad9b4942585921acfbc8`

## nlu-step2-0336 · denied_polarity · train

의미 가족: `nlu-step2-not_ingress` / 표현 변형: 6

### 원문 raw

용기 안에 물은 안 들어갔어요 / 통 모양은 단지형임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "용기 안에 물은 안 들어갔어요 / 통 모양은 단지형임",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기 안에 물은 안 들어갔어요"
    },
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 모양은 단지형임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ad4176567fa6bd861e614624c0d64cecfb306e48e4ae33f444ec3dbfa4e1b35c`

## nlu-step2-0337 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 0

### 원문 raw

아프지는 않아요. 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아프지는 않아요. 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `92f74b923af85553ac9d3102f892a08d0c072fef5cde3b52df9c493f246e3fe8`

## nlu-step2-0338 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 1

### 원문 raw

통증은 없어요, 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통증은 없어요, 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `daf80bb439d35b43d3b9c66667763a427f2d295831370a939f983a0569957e4e`

## nlu-step2-0339 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 2

### 원문 raw

아픈 건 아님
가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아픈 건 아님\n가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아픈 건 아님"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `2666228fbd1af84373b88f1cb576979134737045965d42039505e6584c0d3e15`

## nlu-step2-0340 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 3

### 원문 raw

아프지는 않아요. 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아프지는 않아요. 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9ec8dac92b5495dc543b118ea4d1e377ea08fa65b5e13c905d5307cd08ff5351`

## nlu-step2-0341 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 4

### 원문 raw

통증은 없어요 그리고 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통증은 없어요 그리고 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `e069c064e9693e087c038f380be01fe6c2ceb55bff6bd3c4ae4ab0a4b88cbc32`

## nlu-step2-0342 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 5

### 원문 raw

아픈 건 아님, 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아픈 건 아님, 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아픈 건 아님"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `da470acbb19c0f7206ec7688e4514728ffeefef9d021b3b4b26d4cd259d45775`

## nlu-step2-0343 · denied_polarity · train

의미 가족: `nlu-step2-pain_not_itch` / 표현 변형: 6

### 원문 raw

아프지는 않아요 / 지금 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아프지는 않아요 / 지금 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `704da95f9eb40d6a09d3a68ed2cc8aa07c37adc5153cc9bdc11cda4f6d8b3790`

## nlu-step2-0344 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 0

### 원문 raw

가렵지는 않아요. 방금 처음 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가렵지는 않아요. 방금 처음 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `8232c51f7bba1c804ba8ca48faa234102c3048363486de682d9d4a77e463845f`

## nlu-step2-0345 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 1

### 원문 raw

가려움은 없어요, 방금 처음 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가려움은 없어요, 방금 처음 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움은 없어요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0a172801aaad2214ecc60758fce7f667304a30f58a1cf714d12c7a482438c163`

## nlu-step2-0346 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 2

### 원문 raw

가려운 건 아님
방금 처음 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가려운 건 아님\n방금 처음 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려운 건 아님"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `297494c3438c2bcab927fb396ed93874e569e2b0fd1dc0897b8a91745e7edcd8`

## nlu-step2-0347 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 3

### 원문 raw

가렵지는 않아요. 조금 전에 처음 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가렵지는 않아요. 조금 전에 처음 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d34671f8393e5c890c04cd2209738cc1351aba2ce973d0fec464e0d6ef4733fa`

## nlu-step2-0348 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 4

### 원문 raw

가려움은 없어요 그리고 조금 전에 처음 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가려움은 없어요 그리고 조금 전에 처음 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움은 없어요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `fd3466923257b05d256386409e2da4d694845d02a27d62fb738142c7968cd014`

## nlu-step2-0349 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 5

### 원문 raw

가려운 건 아님, 조금 전에 처음 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가려운 건 아님, 조금 전에 처음 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려운 건 아님"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4e02034b1340a52bc9038d0fa040f3254418cef2e7b0cd8488bce7acc2f7fc8c`

## nlu-step2-0350 · denied_polarity · train

의미 가족: `nlu-step2-itch_not_red` / 표현 변형: 6

### 원문 raw

가렵지는 않아요 / 아까 처음 붉어져서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가렵지는 않아요 / 아까 처음 붉어져서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 붉어져서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `512d3552b2d4924be6c3d88f209ec3770acded1e97247666930b1fefa49daa80`

## nlu-step2-0351 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 0

### 원문 raw

붉어지지 않았어요. 자꾸 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어지지 않았어요. 자꾸 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `1e32a36bd1c7f97bcb9ccf8418c3e599bc9b99fad7a8a892e5072b81cbf33721`

## nlu-step2-0352 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 1

### 원문 raw

붉어짐은 없어요, 자꾸 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어짐은 없어요, 자꾸 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐은 없어요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `6599e1ae8264150c08f8f4ad968ea9a8e745f61faabfa88270edd7f48838cba8`

## nlu-step2-0353 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 2

### 원문 raw

붉어진 건 아님
자꾸 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어진 건 아님\n자꾸 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어진 건 아님"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `10bd30ef4e0ba8ee876fdaa83c0e8915eed686f2dcb47b98b7c46353c7860ecf`

## nlu-step2-0354 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 3

### 원문 raw

붉어지지 않았어요. 반복해서 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어지지 않았어요. 반복해서 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `40ee08615b72e78dccf443617f67bfb49aac9df43f9ea84c88d71fdb3e1cda8e`

## nlu-step2-0355 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 4

### 원문 raw

붉어짐은 없어요 그리고 반복해서 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어짐은 없어요 그리고 반복해서 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐은 없어요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `e92c1b03e82d0d839d0603857f469893690c77a62e83b24409d0222952cb5504`

## nlu-step2-0356 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 5

### 원문 raw

붉어진 건 아님, 반복해서 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어진 건 아님, 반복해서 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어진 건 아님"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `819b6cb95659698048455d7fcea0e83c0dba1752d72869973d06a937bacd7999`

## nlu-step2-0357 · denied_polarity · train

의미 가족: `nlu-step2-red_not_dry` / 표현 변형: 6

### 원문 raw

붉어지지 않았어요 / 괜찮다가 또 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붉어지지 않았어요 / 괜찮다가 또 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `c93fdf1d5290daaba812fbf244a97a88272298eadd60028a5345a298c445a681`

## nlu-step2-0358 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 0

### 원문 raw

건조하지 않아요. 며칠째 계속 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조하지 않아요. 며칠째 계속 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조하지 않아요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `271ada42f64b2ee8cf4516d352cca933a9bdeec9a11376f4320a9c88dc0fbb19`

## nlu-step2-0359 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 1

### 원문 raw

건조함은 없어요, 며칠째 계속 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조함은 없어요, 며칠째 계속 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조함은 없어요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `6061646f0080a526e7c5482f5ef1dd2aa0a2bf7526ae9c84ddbf0c6494c95610`

## nlu-step2-0360 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 2

### 원문 raw

건조한 건 아님
며칠째 계속 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조한 건 아님\n며칠째 계속 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조한 건 아님"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `f973a49d7d54ac9e5ea2c2df2e8f07aa8a1b8d8c00737cf88ff82eafe4c6f65c`

## nlu-step2-0361 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 3

### 원문 raw

건조하지 않아요. 며칠 동안 내내 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조하지 않아요. 며칠 동안 내내 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조하지 않아요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b25090be9719e9bb2bdcbedf45b1753aa9721cd5da7d3acd54d06f002b9092da`

## nlu-step2-0362 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 4

### 원문 raw

건조함은 없어요 그리고 며칠 동안 내내 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조함은 없어요 그리고 며칠 동안 내내 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조함은 없어요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `7911e66789b3143e71be0f83d12ed166be729b186272d76210186558a3855fc9`

## nlu-step2-0363 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 5

### 원문 raw

건조한 건 아님, 며칠 동안 내내 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조한 건 아님, 며칠 동안 내내 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조한 건 아님"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0e01336b34af3fb3cd77e47f1d0644ef71c83b970058c1205972137e8c5214d0`

## nlu-step2-0364 · denied_polarity · train

의미 가족: `nlu-step2-dry_not_tight` / 표현 변형: 6

### 원문 raw

건조하지 않아요 / 며칠째 끊이지 않고 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "건조하지 않아요 / 며칠째 끊이지 않고 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조하지 않아요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `1c1765c890c85e3af03cd625f775f7d0cff449f8a43b71a1dff80f5c17a10c14`

## nlu-step2-0365 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 0

### 원문 raw

당기지는 않아요. 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당기지는 않아요. 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `014c040a315405c94e6d701ca1739e398062c086a6b43a4a4b588ebef35384d6`

## nlu-step2-0366 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 1

### 원문 raw

당김은 없어요, 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당김은 없어요, 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `794f1f0dfa2c2025129ee081f484f9c145b388def6e52c615a901ef30dffc05e`

## nlu-step2-0367 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 2

### 원문 raw

당기는 건 아님
따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당기는 건 아님\n따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기는 건 아님"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `78e4d3411facc312d50310aacfe8dc3cbff4bc8fc97cd087d8a96dd0285b0e9a`

## nlu-step2-0368 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 3

### 원문 raw

당기지는 않아요. 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당기지는 않아요. 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0aeaf70d1a41a29e9658c453bb28b4031a021a5f54c7629bec0cb82a8b731afa`

## nlu-step2-0369 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 4

### 원문 raw

당김은 없어요 그리고 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당김은 없어요 그리고 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `12d55c53a145e91168db6bbfe8479e214520979e6071ff53356af0795b275bd4`

## nlu-step2-0370 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 5

### 원문 raw

당기는 건 아님, 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당기는 건 아님, 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기는 건 아님"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `5e1f6de8b55bf0da2ef398d19efe4521acf979919d44e96c81f05b35c0358cfc`

## nlu-step2-0371 · denied_polarity · train

의미 가족: `nlu-step2-tight_not_sting` / 표현 변형: 6

### 원문 raw

당기지는 않아요 / 지금 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "당기지는 않아요 / 지금 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `793d95c01c172b0026c0451e0539c36edc3aba069053156f2a496f382121062a`

## nlu-step2-0372 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 0

### 원문 raw

따갑지는 않아요. 방금 처음 화끈거려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑지는 않아요. 방금 처음 화끈거려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑지는 않아요"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 화끈거려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `afb6d9c2e2117f273379197ae7ce29e87c68e785ed06716a96e0d54c30b732a7`

## nlu-step2-0373 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 1

### 원문 raw

따가움은 없어요, 방금 처음 화끈거려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따가움은 없어요, 방금 처음 화끈거려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가움은 없어요"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 화끈거려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `7d0fd47fc30bc3352b4c2db8392c2ada8d75c6f543369e5334c91f6bfd022e37`

## nlu-step2-0374 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 2

### 원문 raw

따갑진 않음
방금 처음 화끈거려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑진 않음\n방금 처음 화끈거려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑진 않음"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 화끈거려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b0f701c84aa4a699a3f2a3cc3d1e1fe2293cf1d63e9377e908e3f4ab801dbc44`

## nlu-step2-0375 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 3

### 원문 raw

따갑지는 않아요. 조금 전에 처음 화끈거림

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑지는 않아요. 조금 전에 처음 화끈거림",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑지는 않아요"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 화끈거림"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `5ddc76d6978a21b91a8519477487a9ececaaa6010207062590b1c004257a71e4`

## nlu-step2-0376 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 4

### 원문 raw

따가움은 없어요 그리고 조금 전에 처음 화끈거림

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따가움은 없어요 그리고 조금 전에 처음 화끈거림",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따가움은 없어요"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 화끈거림"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `0530840d58210c14d941b95371526eefcdca13fef6ec8bbdf372f7d5527191fa`

## nlu-step2-0377 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 5

### 원문 raw

따갑진 않음, 조금 전에 처음 화끈거림

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑진 않음, 조금 전에 처음 화끈거림",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑진 않음"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 화끈거림"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `83154996daa519e7c622e7b30cba3826102b3a5a605792f870f97d5aa4b01d5d`

## nlu-step2-0378 · denied_polarity · train

의미 가족: `nlu-step2-sting_not_burn` / 표현 변형: 6

### 원문 raw

따갑지는 않아요 / 아까 처음 화끈거려서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑지는 않아요 / 아까 처음 화끈거려서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑지는 않아요"
    },
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 화끈거려서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d3bba400d1c2577601530647dfc2ff48303e76773b0ce6b77812b68ac8ba8de0`

## nlu-step2-0379 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 0

### 원문 raw

화끈거리지 않아요. 자꾸 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거리지 않아요. 자꾸 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `33b65d0f3f77d730a1bb4056d40b395c869c5b512a3c89fbc15e5a543867afe1`

## nlu-step2-0380 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 1

### 원문 raw

화끈거림은 없어요, 자꾸 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거림은 없어요, 자꾸 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림은 없어요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `805fdb455f6a8c52c2531a687d1f9a87ff21b7bc051718c2bc1ea7b305cef826`

## nlu-step2-0381 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 2

### 원문 raw

화끈거린 건 아님
자꾸 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거린 건 아님\n자꾸 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거린 건 아님"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ba31a318bc7f7cc31d45f799f025457c0a9baa01680b2724a4e74f548a77e70d`

## nlu-step2-0382 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 3

### 원문 raw

화끈거리지 않아요. 반복해서 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거리지 않아요. 반복해서 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `de03b6a907c3179b68225e0d27cd70b668a3af5963fa1c1f9fed1c152250dab8`

## nlu-step2-0383 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 4

### 원문 raw

화끈거림은 없어요 그리고 반복해서 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거림은 없어요 그리고 반복해서 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림은 없어요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `5c45c6df8e675aead19e21d7eea7318b08f5b63ba818e78aef01aad50be490fc`

## nlu-step2-0384 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 5

### 원문 raw

화끈거린 건 아님, 반복해서 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거린 건 아님, 반복해서 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거린 건 아님"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `f5ec49f60a8e97d4abfd02dda41f0db40aaf5562060b7ce8c702b1555caf6593`

## nlu-step2-0385 · denied_polarity · train

의미 가족: `nlu-step2-burn_not_swollen` / 표현 변형: 6

### 원문 raw

화끈거리지 않아요 / 괜찮다가 또 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거리지 않아요 / 괜찮다가 또 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9454dbe54605337d6ad3bdd2cc790bb607c971bab924d6b51c852905bdcada93`

## nlu-step2-0386 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 0

### 원문 raw

부어오르진 않았어요. 며칠째 계속 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "부어오르진 않았어요. 며칠째 계속 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d9ee16c98ea942995f6d00db58277ef40a9958912c2e786bb87ca9ddc9952e23`

## nlu-step2-0387 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 1

### 원문 raw

부어오름은 없어요, 며칠째 계속 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "부어오름은 없어요, 며칠째 계속 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름은 없어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `39b33b8a83c7cc4f1465c6fbb5d7d0640e9b8d9be8812ca631edbcd48b686b0a`

## nlu-step2-0388 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 2

### 원문 raw

붓지는 않았어요
며칠째 계속 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붓지는 않았어요\n며칠째 계속 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붓지는 않았어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `c283096fec8e83058e68a839dc7a3f9370714f207e2a71ed4b9c038ee108f4f1`

## nlu-step2-0389 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 3

### 원문 raw

부어오르진 않았어요. 며칠 동안 내내 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "부어오르진 않았어요. 며칠 동안 내내 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9f2d3f3a99c38f007eac5411648eae23165f63b4fd226db08e48281f85e23292`

## nlu-step2-0390 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 4

### 원문 raw

부어오름은 없어요 그리고 며칠 동안 내내 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "부어오름은 없어요 그리고 며칠 동안 내내 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름은 없어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b0c8c90e4ca613797dbc9450bab30197eef7fa2326bde74ee9d4af6cd06606b5`

## nlu-step2-0391 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 5

### 원문 raw

붓지는 않았어여, 며칠 동안 내내 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "붓지는 않았어여, 며칠 동안 내내 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붓지는 않았어여"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `cf51c6e44a34a1ca74df28c4448e486b55dcee00edfea8fa977db3756e6cfc4e`

## nlu-step2-0392 · denied_polarity · train

의미 가족: `nlu-step2-swollen_not_pain` / 표현 변형: 6

### 원문 raw

부어오르진 않았어요 / 며칠째 끊이지 않고 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "부어오르진 않았어요 / 며칠째 끊이지 않고 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4b6beb70bab2fda484d21bea5ea7cd13c49807a7fe83736c7b6e291ca4cab72f`

## nlu-step2-0393 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 0

### 원문 raw

트러블은 안 났어요. 방금 처음 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블은 안 났어요. 방금 처음 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블은 안 났어요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d13de3dc5960ca727301d8ade350c2fcfd1037eb42e7b8da48ee5fc1d844e69a`

## nlu-step2-0394 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 1

### 원문 raw

트러블 난 건 아니에요, 방금 처음 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블 난 건 아니에요, 방금 처음 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블 난 건 아니에요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `25ac2907eaa9d4d287451c8124954e18a63387ae1fe47ddd3b002d8aef7ed94e`

## nlu-step2-0395 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 2

### 원문 raw

트러블은 없어요
방금 처음 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블은 없어요\n방금 처음 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블은 없어요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b96e4b6faa23b4af9ba32aabb1639a057a257f2e20d6f7678ae64525a9f386ec`

## nlu-step2-0396 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 3

### 원문 raw

트러블은 안 났어요. 조금 전에 처음 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블은 안 났어요. 조금 전에 처음 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블은 안 났어요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `8cfe92a91a067873a3d9125ae0a105ba2755d3aa4fdc053075db63a75c7f95e8`

## nlu-step2-0397 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 4

### 원문 raw

트러블 난 건 아니에요 그리고 조금 전에 처음 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블 난 건 아니에요 그리고 조금 전에 처음 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블 난 건 아니에요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `15696b9fa4b42b8016ac113668390f21ba8f930e38cb173b33c1ae4a64ebf55c`

## nlu-step2-0398 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 5

### 원문 raw

트러블은 없어여, 조금 전에 처음 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블은 없어여, 조금 전에 처음 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블은 없어여"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ace5e63c1c9e67bbe90cfe72a727e022c79b1b6e68dba08065cc922844ea78b9`

## nlu-step2-0399 · denied_polarity · train

의미 가족: `nlu-step2-breakout_not_peel` / 표현 변형: 6

### 원문 raw

트러블은 안 났어요 / 아까 처음 각질이 벗겨져서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블은 안 났어요 / 아까 처음 각질이 벗겨져서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "트러블은 안 났어요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 각질이 벗겨져서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `1a03ed231091641f1e692813c454b1a9bc690a5efed3380c7414016f2b74cebb`

## nlu-step2-0400 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 0

### 원문 raw

각질은 벗겨지지 않아요. 눈이 시려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질은 벗겨지지 않아요. 눈이 시려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9ceecd1bc125964dae66ee12e440bb5d083dac41e0090cfee7ab8c2219877eaf`

## nlu-step2-0401 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 1

### 원문 raw

각질 벗겨짐은 없어요, 눈이 시려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질 벗겨짐은 없어요, 눈이 시려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 벗겨짐은 없어요"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `eeb5e45848f97dd42a73232be86a77906dd0ef840f4ccd04e70de913d3af8a92`

## nlu-step2-0402 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 2

### 원문 raw

각질 일어난 건 아님
눈이 시려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질 일어난 건 아님\n눈이 시려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 일어난 건 아님"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d79201a9f33f1451c6e96be720b368bcad33ec0240dcc082cdb1e1ac7c58a520`

## nlu-step2-0403 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 3

### 원문 raw

각질은 벗겨지지 않아요. 눈따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질은 벗겨지지 않아요. 눈따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `3f60a48ce614710e9e7ae3758464ee6eeb070197289c58aa309f41bcacd8a3f8`

## nlu-step2-0404 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 4

### 원문 raw

각질 벗겨짐은 없어요 그리고 눈따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질 벗겨짐은 없어요 그리고 눈따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 벗겨짐은 없어요"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ae5a20bed572b447b170680220daf3576dd041bfdb2b1ecd108af31bd782e966`

## nlu-step2-0405 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 5

### 원문 raw

각질 일어난 건 아님, 눈따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질 일어난 건 아님, 눈따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 일어난 건 아님"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `3468fb557f01171985b106106423a9de06e2f5fb9bdc687422c7e7a9c0fc2a3b`

## nlu-step2-0406 · denied_polarity · train

의미 가족: `nlu-step2-peel_not_eye` / 표현 변형: 6

### 원문 raw

각질은 벗겨지지 않아요 / 지금 눈이 시려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "각질은 벗겨지지 않아요 / 지금 눈이 시려요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    },
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `b4498696d15a3ebcbb91eabe3440175c129485dbcd4451d29fe1621ee6151126`

## nlu-step2-0407 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 0

### 원문 raw

눈은 시리지 않아요. 선크림 안 발랐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈은 시리지 않아요. 선크림 안 발랐어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈은 시리지 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ef5b04d99db32db705010d41c14826cb41eef01953cb49cc02bf596c6f759e52`

## nlu-step2-0408 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 1

### 원문 raw

눈따가움은 없어요, 선크림 안 발랐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈따가움은 없어요, 선크림 안 발랐어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈따가움은 없어요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `cbeb06f47d561d819b4c1b64b8ebb7f2df9c19541115869e4e06f48cd76816d3`

## nlu-step2-0409 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 2

### 원문 raw

눈시림은 아님
선크림 안 발랐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈시림은 아님\n선크림 안 발랐어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈시림은 아님"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `cd0d020ad7df928e43081199887061564c1b3795f34b1ce0783c9ffec2172a7f`

## nlu-step2-0410 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 3

### 원문 raw

눈은 시리지 않아요. 선크림은 안 바른 상태예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈은 시리지 않아요. 선크림은 안 바른 상태예요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈은 시리지 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `ca581cbe6e9e426a165401bc4d0d073f286a359bc580767ae2cc582f35e855f5`

## nlu-step2-0411 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 4

### 원문 raw

눈따가움은 없어요 그리고 선크림은 안 바른 상태예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈따가움은 없어요 그리고 선크림은 안 바른 상태예요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈따가움은 없어요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `17f5eb387118432280e3e7c72d215c6ffcdd3ec5afc8e7bfecd033cd44ab9212`

## nlu-step2-0412 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 5

### 원문 raw

눈시림은 아님, 선크림은 안 바른 상태예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈시림은 아님, 선크림은 안 바른 상태예요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈시림은 아님"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d326be612248857f054d9581e44b7de594e09ee654af955a5c111b65a1eb4a64`

## nlu-step2-0413 · denied_polarity · val_internal

의미 가족: `nlu-step2-eye_not_sun` / 표현 변형: 6

### 원문 raw

눈은 시리지 않아요 / 선크림 안바름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈은 시리지 않아요 / 선크림 안바름",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "눈은 시리지 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `3c731f3346c120bf6fe5a41d5f3d49b5c0357a7eeca987c710964b1abf43e6e8`

## nlu-step2-0414 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 0

### 원문 raw

물이 닿지는 않았어요. 아침저녁 젤 세정제 써요. 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 아침저녁 젤 세정제 써요. 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `41138a98ec169a72e07c1d0210c8ab7eeed837504517b27b6c0c2f83aafc3544`

## nlu-step2-0415 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 1

### 원문 raw

물 접촉은 없었어요, 아침저녁 젤 세정제 써요, 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요, 아침저녁 젤 세정제 써요, 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `4ab404739b7bc061d81bb5a538abcac94a0c468d344203a31fe7f89ee9511409`

## nlu-step2-0416 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 2

### 원문 raw

물에 닿은 적 없음
아침저녁 젤 세정제 써요
귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음\n아침저녁 젤 세정제 써요\n귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `d4bbb06edc007818786b64b6baf38d38e6391f95b37660c7607bc8031b8c3c2b`

## nlu-step2-0417 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 3

### 원문 raw

물이 닿지는 않았어요. 젤 세정제는 아침저녁으로 써요. 귀 목은 차단제 누락했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요. 젤 세정제는 아침저녁으로 써요. 귀 목은 차단제 누락했어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `27daef6fe4b8da39b8660e2bc66354eaa82308fd7ece7a8ae1d89947dde53aa7`

## nlu-step2-0418 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 4

### 원문 raw

물 접촉은 없었어요 그리고 젤 세정제는 아침저녁으로 써요 그리고 귀 목은 차단제 누락했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물 접촉은 없었어요 그리고 젤 세정제는 아침저녁으로 써요 그리고 귀 목은 차단제 누락했어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `f98ac3329c753b452da7a5c44d3cfe183d9e7c7c9187f29f34c8e1e557808f46`

## nlu-step2-0419 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 5

### 원문 raw

물에 닿은 적 없음, 젤 세정제는 아침저녁으로 써요, 귀 목은 차단제 누락했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물에 닿은 적 없음, 젤 세정제는 아침저녁으로 써요, 귀 목은 차단제 누락했어여",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `9027db0e6f0a9a65bacacb5c99b65cd7abd54cb46de9228abc63d360510aead4`

## nlu-step2-0420 · denied_polarity · val_internal

의미 가족: `nlu-step2-neg_water_routine` / 표현 변형: 6

### 원문 raw

물이 닿지는 않았어요 / 아침과 저녁에 젤 세정제 씀 / 차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿지는 않았어요 / 아침과 저녁에 젤 세정제 씀 / 차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침과 저녁에 젤 세정제 씀"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.

내용 SHA-256: `57c1e2d7df543eff481c7cf2fab7fd551f8a739fbc371eb7ebc6013f0a6b2f98`

## nlu-step2-0421 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 손만 씻는 중이에요. 찬물 써요. 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 손만 씻는 중이에요. 찬물 써요. 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 씻는 중이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `03b402717db7f769e6aa724ff332a97819cfdacc8119147590e84842ad9cdc4a`

## nlu-step2-0422 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 손 씻는 얘기예요, 찬물 써요, 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 손 씻는 얘기예요, 찬물 써요, 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b8887b27b5e6944b82d324e2062f654e47a41aa41fc61ac3ae57ad1291933571`

## nlu-step2-0423 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 이번엔 손을 씻어요
찬물 써요
세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 이번엔 손을 씻어요\n찬물 써요\n세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "이번엔 손을 씻어요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `74d9063853b2cfd8968b60b08a0e908a40a2e4b0c40a889feb2ec24590c6e1d6`

## nlu-step2-0424 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 손만 씻는 중이에요. 물은 차가워요. 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 손만 씻는 중이에요. 물은 차가워요. 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 씻는 중이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7149cbc86180f7de2d82dc620610891620f66a8d766a9ed9823409a21d950dfc`

## nlu-step2-0425 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 손 씻는 얘기예요 그리고 물은 차가워요 그리고 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 손 씻는 얘기예요 그리고 물은 차가워요 그리고 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손 씻는 얘기예요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c896d1d463ae6a074a389290e30271cdf09ad7ea9c16f463fc3e74cb017ddde7`

## nlu-step2-0426 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 이번엔 손을 씻어여, 물은 차가워요, 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 이번엔 손을 씻어여, 물은 차가워요, 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "이번엔 손을 씻어여"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1944d37a07db37949772b34840054a117861b785ec256a3e067645f5d9bf5dff`

## nlu-step2-0427 · other_subject · train

의미 가족: `nlu-step2-other_wash` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 손만 씻는 중이에요 / 차가운 물로 해요 / 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 손만 씻는 중이에요 / 차가운 물로 해요 / 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손만 씻는 중이에요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "차가운 물로 해요"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `055c4804fdc73b8f68e9656effe14a0a5f7506fee1cc810e7357430ad9c78a41`

## nlu-step2-0428 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 세안 브러시 써요. 살살 문질러요. 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세안 브러시 써요. 살살 문질러요. 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `139f8b804ccabb2bfb3c8e9a0bd8c4864a6e8888c2cc29563304df89c11af169`

## nlu-step2-0429 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 도구는 세안용 브러시예요, 살살 문질러요, 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 도구는 세안용 브러시예요, 살살 문질러요, 마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "도구는 세안용 브러시예요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `329d7aa3f03dee40f83b3cc035c119ef5adaa1352247144c2be866fa3f3338e1`

## nlu-step2-0430 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 브러시로 세안해요
살살 문질러요
마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 브러시로 세안해요\n살살 문질러요\n마지막에 물로 씻어내요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "브러시로 세안해요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "살살 문질러요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `0c9cdb8f4d8362942bf9868d98afd25b5b87112a8d50ebb2392b2413ac6e971f`

## nlu-step2-0431 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 세안 브러시 써요. 문지를 때 힘 약하게 줘요. 끝에는 물 헹굼 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세안 브러시 써요. 문지를 때 힘 약하게 줘요. 끝에는 물 헹굼 해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1f1bb0a4edd8b3966f3ce9b044563a737bb185fbdfd7ce9eee2eb75c687bcc0d`

## nlu-step2-0432 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 도구는 세안용 브러시예요 그리고 문지를 때 힘 약하게 줘요 그리고 끝에는 물 헹굼 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 도구는 세안용 브러시예요 그리고 문지를 때 힘 약하게 줘요 그리고 끝에는 물 헹굼 해요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "도구는 세안용 브러시예요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1ac5910cc045bac140dfc6a11bac26e0d102919eb8a4ca10ea5bacf2d989e5f1`

## nlu-step2-0433 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 브러시로 세안해여, 문지를 때 힘 약하게 줘요, 끝에는 물 헹굼 해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 브러시로 세안해여, 문지를 때 힘 약하게 줘요, 끝에는 물 헹굼 해여",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "브러시로 세안해여"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "문지를 때 힘 약하게 줘요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b6b6f35fe66ff0de9bfeb02ac04779bb7cc6c0d04ebbe6da217251766ad0b6c2`

## nlu-step2-0434 · other_subject · train

의미 가족: `nlu-step2-other_tool` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 세안 브러시 써요 / 문지르는 힘은 약해요 / 마무리는 물로 헹궈요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세안 브러시 써요 / 문지르는 힘은 약해요 / 마무리는 물로 헹궈요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "scrub_brush",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 브러시 써요"
    },
    {
      "variable_id": "method.friction",
      "value": "gentle",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "문지르는 힘은 약해요"
    },
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e84ecf251cfeb24c26b5ceb3dd85d17d447175cda49d504a0bcc8f5082790644`

## nlu-step2-0435 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 매일 로션을 써요. 보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 로션을 써요. 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `acb3e9044b555b4a3c5793342b161a67f11634ce8af48d94fa0c5da82f1dd04e`

## nlu-step2-0436 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 로션은 매일 발라요, 보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 로션은 매일 발라요, 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `be51eeefde2fd456dcd21748544600d10cfff4f94d811fed6e334ef75552630e`

## nlu-step2-0437 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 매일 로션 바름
보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 로션 바름\n보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `ed4e8bd95446ad5245c61ddd6cace47c3404ea6010237a2bf102f46451edd256`

## nlu-step2-0438 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 매일 로션을 써요. 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 로션을 써요. 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1ed1662838544370bdd4c7e6c35bd10dc1cbd70b9cc0ae2ad4e5ecd831dec52e`

## nlu-step2-0439 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 로션은 매일 발라요 그리고 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 로션은 매일 발라요 그리고 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `28e1971fa5377f08c179bcd5a29ed5f3ec4da58f609be12511fb22fd0e186b44`

## nlu-step2-0440 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 매일 로션 바름, 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 로션 바름, 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `dbd2c07a160338acd23deaaab0b7a6962a4de19ede8ff9e8456173720a403d81`

## nlu-step2-0441 · other_subject · train

의미 가족: `nlu-step2-other_routine` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 매일 로션을 써요 / 볼만 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 로션을 써요 / 볼만 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "볼만 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9fdfb8c5ccbafdc0cd1a17df633a9d28724359076e62e12655c26e476f3cc8f1`

## nlu-step2-0442 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 저녁마다 로션 다음 선크림 발라요. 씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁마다 로션 다음 선크림 발라요. 씻고 3분 뒤에 보습해요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `3e57361c6fada085fa8b0c67bd40447aa59a44f294cd446571794bfb3ce3b1c0`

## nlu-step2-0443 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 로션을 바른 뒤 선크림을 저녁마다 써요, 씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 로션을 바른 뒤 선크림을 저녁마다 써요, 씻고 3분 뒤에 보습해요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `d5bf5d1f86f5677204fd4a39612d7f6452703d4d25bfbeefad808ae30552ab46`

## nlu-step2-0444 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 매일 저녁 로션 먼저 선크림 나중에 발라요
씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 저녁 로션 먼저 선크림 나중에 발라요\n씻고 3분 뒤에 보습해요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c56bfe963188eeed46aff3fcada816bddbacaccfb31879ba7aa3957e11e8146a`

## nlu-step2-0445 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 저녁마다 로션 다음 선크림 발라요. 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁마다 로션 다음 선크림 발라요. 세안 후 보습까지 3분 걸려요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `45b053db973e7b520bc88d1a2ad6d1515153de72541dc6c414af9fb7fd509ddc`

## nlu-step2-0446 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 로션을 바른 뒤 선크림을 저녁마다 써요 그리고 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 로션을 바른 뒤 선크림을 저녁마다 써요 그리고 세안 후 보습까지 3분 걸려요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `6fc5080bc88603fce546f5ca5c8709a6593260fe96aeb3604a737c858c0e339d`

## nlu-step2-0447 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 매일 저녁 로션 먼저 선크림 나중에 발라요, 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 저녁 로션 먼저 선크림 나중에 발라요, 세안 후 보습까지 3분 걸려요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `edd2c36e8c00360de7f33b3fbec3d9b9d1535af8ef8c336e4d042a5b56da66a0`

## nlu-step2-0448 · other_subject · train

의미 가족: `nlu-step2-other_order` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 저녁마다 로션 다음 선크림 발라요 / 보습은 세안하고 삼 분 뒤예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁마다 로션 다음 선크림 발라요 / 보습은 세안하고 삼 분 뒤예요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습은 세안하고 삼 분 뒤예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `fec5cc3a59ce481ce72f478744940b9a91f9721c780e71f6911c0e1612d2279f`

## nlu-step2-0449 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 아침마다 선크림 발라요. 물에 들어갔어요. 땀 흘렸어요. 손등 팔이 노출됐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 아침마다 선크림 발라요. 물에 들어갔어요. 땀 흘렸어요. 손등 팔이 노출됐어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `97c9af0a51ab5dde005c367d135ba04134353d66e1f8a357c6386f5b6c170c12`

## nlu-step2-0450 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 선크림은 매일 아침 써요, 물에 들어갔어요, 땀 흘렸어요, 손등 팔이 노출됐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림은 매일 아침 써요, 물에 들어갔어요, 땀 흘렸어요, 손등 팔이 노출됐어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `d8f4a263a8b65fe2f779656fc5a643c3e6f1a14bf37328ac0747bbade419440b`

## nlu-step2-0451 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 매일 아침 선크림 바름
물에 들어갔어요
땀 흘렸어요
손등 팔이 노출됐어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 아침 선크림 바름\n물에 들어갔어요\n땀 흘렸어요\n손등 팔이 노출됐어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흘렸어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손등 팔이 노출됐어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e91d5345eb77aef50c03680ac633907d8cdb42d392869604b9cab8a1d5e4c443`

## nlu-step2-0452 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 아침마다 선크림 발라요. 수영했어요. 땀이 많이 남. 노출된 곳은 손등과 팔이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 아침마다 선크림 발라요. 수영했어요. 땀이 많이 남. 노출된 곳은 손등과 팔이에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "수영했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "노출된 곳은 손등과 팔이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `cf31331b961809c358594741dc56832a90187d9495c251d9c82441c7710f9a9e`

## nlu-step2-0453 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 선크림은 매일 아침 써요 그리고 수영했어요 그리고 땀이 많이 남 그리고 노출된 곳은 손등과 팔이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림은 매일 아침 써요 그리고 수영했어요 그리고 땀이 많이 남 그리고 노출된 곳은 손등과 팔이에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "수영했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "노출된 곳은 손등과 팔이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `537a52ecd9787b67a3d15c7156c6e657d74f77f38a93e630264bcd2bd79718a6`

## nlu-step2-0454 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 매일 아침 선크림 바름, 수영했어여, 땀이 많이 남, 노출된 곳은 손등과 팔이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 매일 아침 선크림 바름, 수영했어여, 땀이 많이 남, 노출된 곳은 손등과 팔이에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "수영했어여"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 많이 남"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "노출된 곳은 손등과 팔이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `a3a3571e9ba5988c2ed581044d6d43083eae11b316735eb735b2560a0d05bcac`

## nlu-step2-0455 · other_subject · train

의미 가족: `nlu-step2-other_sun` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 아침마다 선크림 발라요 / 물놀이 했어요 / 땀이 났어요 / 손등이랑 팔이 드러나 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 아침마다 선크림 발라요 / 물놀이 했어요 / 땀이 났어요 / 손등이랑 팔이 드러나 있어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물놀이 했어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 났어요"
    },
    {
      "variable_id": "sun.exposed_sites",
      "value": [
        "손등",
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "손등이랑 팔이 드러나 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c0db30f23378034f168613ab8ed76ae5b2d7a0edb17a7e831023d79c3bbc5403`

## nlu-step2-0456 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 지난 금요일에 열었어요. 작은 공병에 덜어뒀어요. 펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 지난 금요일에 열었어요. 작은 공병에 덜어뒀어요. 펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `80e671347359a79445ddcfea6b90c3c594766ffd31a457dbef15ad0d91ed29b9`

## nlu-step2-0457 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 개봉한 날은 지난 금요일이에요, 작은 공병에 덜어뒀어요, 펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 개봉한 날은 지난 금요일이에요, 작은 공병에 덜어뒀어요, 펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉한 날은 지난 금요일이에요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `98e0c01a81e9478ac5c724a6b58f79cef3f1701caaba0d01aa67aabdd4b507ab`

## nlu-step2-0458 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 지난주 금욜에 개봉함
작은 공병에 덜어뒀어요
펌프가 달린 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 지난주 금욜에 개봉함\n작은 공병에 덜어뒀어요\n펌프가 달린 용기예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "지난주 금욜에 개봉함"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "펌프가 달린 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `dbbd2e3e3241d8c0645449260944106761bdf187e7ec990b8fb02d57948d8a62`

## nlu-step2-0459 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 지난 금요일에 열었어요. 작은 공병으로 소분했어요. 통에 펌프가 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 지난 금요일에 열었어요. 작은 공병으로 소분했어요. 통에 펌프가 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통에 펌프가 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `ef04b7e02f86df9bdc165834d8be8d4e51f9dd32bcd39272ffc92d2eef8c0986`

## nlu-step2-0460 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 개봉한 날은 지난 금요일이에요 그리고 작은 공병으로 소분했어요 그리고 통에 펌프가 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 개봉한 날은 지난 금요일이에요 그리고 작은 공병으로 소분했어요 그리고 통에 펌프가 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉한 날은 지난 금요일이에요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통에 펌프가 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `42095efff7258a6f8b506b2996db55580e5e48e701d45e3df731d8b3928c3636`

## nlu-step2-0461 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 지난주 금욜에 개봉함, 작은 공병으로 소분했어여, 통에 펌프가 있어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 지난주 금욜에 개봉함, 작은 공병으로 소분했어여, 통에 펌프가 있어여",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "지난주 금욜에 개봉함"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어여"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통에 펌프가 있어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `396ff52c67c984f964a05b25f0b400625212a69bf01d748e4df7049a80c26175`

## nlu-step2-0462 · other_subject · train

의미 가족: `nlu-step2-other_storage` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 지난 금요일에 열었어요 / 작은 빈 병에 나눠 담음 / 용기는 펌프형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 지난 금요일에 열었어요 / 작은 빈 병에 나눠 담음 / 용기는 펌프형이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난 금요일",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "지난 금요일에 열었어요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "작은 빈 병에 나눠 담음"
    },
    {
      "variable_id": "storage.container",
      "value": "펌프형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "용기는 펌프형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `8718afce592beb21d06e6aee868d58ea0f849584daab7f16eb4a30d0e6ddaf20`

## nlu-step2-0463 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 사용기한은 2027년 8월로 적혀요. 개봉 후 6개월 표시예요. 보관 장소는 창가예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 사용기한은 2027년 8월로 적혀요. 개봉 후 6개월 표시예요. 보관 장소는 창가예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `a4479b46c691c59d0893a11406244ebfdfb5af0609c796ea7ea0a25dfa290044`

## nlu-step2-0464 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 2027년 8월이 사용기한이에요, 개봉 후 6개월 표시예요, 보관 장소는 창가예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 2027년 8월이 사용기한이에요, 개봉 후 6개월 표시예요, 보관 장소는 창가예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `0ebc731675247adc27a23bfa86a234d771ceaa0379da1d466d1c5b6398330638`

## nlu-step2-0465 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 사용기한 표시 2027년 8월임
개봉 후 6개월 표시예요
보관 장소는 창가예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 사용기한 표시 2027년 8월임\n개봉 후 6개월 표시예요\n보관 장소는 창가예요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보관 장소는 창가예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b4b017800ab55d4eff2f00c112dd20c62898fb632ba078fae39efe2389c51229`

## nlu-step2-0466 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 사용기한은 2027년 8월로 적혀요. 개봉 뒤 여섯 달이라고 써 있어요. 창 옆에 보관 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 사용기한은 2027년 8월로 적혀요. 개봉 뒤 여섯 달이라고 써 있어요. 창 옆에 보관 중이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "창 옆에 보관 중이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9a58e5b1f39c883c644b1471659f1ba7f34a8320769ab2a4f5777b62b2f35b24`

## nlu-step2-0467 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 2027년 8월이 사용기한이에요 그리고 개봉 뒤 여섯 달이라고 써 있어요 그리고 창 옆에 보관 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 2027년 8월이 사용기한이에요 그리고 개봉 뒤 여섯 달이라고 써 있어요 그리고 창 옆에 보관 중이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "창 옆에 보관 중이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `75d05de375e884fa41484079bd5961dd0dc397e76d8844be53e69ca5948ba0a7`

## nlu-step2-0468 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 사용기한 표시 2027년 8월임, 개봉 뒤 여섯 달이라고 써 있어여, 창 옆에 보관 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 사용기한 표시 2027년 8월임, 개봉 뒤 여섯 달이라고 써 있어여, 창 옆에 보관 중이에요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어여"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "창 옆에 보관 중이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `004fae5c6ecc2a99889bd33e2b9168befa31bcebb51f407c4102c355c230f4ec`

## nlu-step2-0469 · other_subject · train

의미 가족: `nlu-step2-other_expiry` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 사용기한은 2027년 8월로 적혀요 / 열고 6개월 이내라고 적혀요 / 창가에 두고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 사용기한은 2027년 8월로 적혀요 / 열고 6개월 이내라고 적혀요 / 창가에 두고 있어요",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    },
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    },
    {
      "variable_id": "storage.light_air",
      "value": "창가 보관",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "창가에 두고 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e8e1f6d2367d9da0059970599e1ed56a0f82073a9f6397e244222a4a8b37fbe0`

## nlu-step2-0470 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 물이 닿지는 않았어요. 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿지는 않았어요. 땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c6b09f1fe8048685f146fea1b6fefd56daabe0c39f3fa652393690136b20e8b5`

## nlu-step2-0471 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 물 접촉은 없었어요, 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물 접촉은 없었어요, 땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `5e69e07791bd3881d9d1b9149bcd7dda3f57477d0c7e39e5e0bb75476384903b`

## nlu-step2-0472 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 물에 닿은 적 없음
땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물에 닿은 적 없음\n땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7a0104adc37c97f66ecae0dd5e146663afa798cea38f504d4d805fd43671155e`

## nlu-step2-0473 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 물이 닿지는 않았어요. 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿지는 않았어요. 땀 안 흘렸어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `48492c7a6861dd19dd93b43729d2e73a2e78dc3edf98ad335631140c53228b54`

## nlu-step2-0474 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 물 접촉은 없었어요 그리고 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물 접촉은 없었어요 그리고 땀 안 흘렸어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7d56b0f31ca06143f2faee680630b08318dde0a727b1010c63361731a9047944`

## nlu-step2-0475 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 물에 닿은 적 없음, 땀 안 흘렸어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물에 닿은 적 없음, 땀 안 흘렸어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f728126cb333ec9a13196e8c20619929664542b9eaa27899faadd9f9afa03645`

## nlu-step2-0476 · other_subject · train

의미 가족: `nlu-step2-other_no_water` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 물이 닿지는 않았어요 / 땀난 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿지는 않았어요 / 땀난 건 아니에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `be6ec0514747bd75cf545c849650d4247bc01dba3275c692319ab2c4815eed1c`

## nlu-step2-0477 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 씻을 때마다 눈이 시려요. 아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 씻을 때마다 눈이 시려요. 아프지는 않아요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `6e0f16141f82319a7549a7d1155bd0eaa69be96243e57e07eeb517bd7bff471d`

## nlu-step2-0478 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 세안할 때마다 눈따가움, 아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세안할 때마다 눈따가움, 아프지는 않아요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안할 때마다 눈따가움"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "세안할 때마다 눈따가움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `834539b29b1b5b05a65c92bae05303cd1a4e313561c08034f519b75fc8aea922`

## nlu-step2-0479 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 세수할 때마다 눈이 따가워요
아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세수할 때마다 눈이 따가워요\n아프지는 않아요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1025a3fa39ada2d87ff4165558acd700360957718455d6ca837b9de0af750053`

## nlu-step2-0480 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 씻을 때마다 눈이 시려요. 통증은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 씻을 때마다 눈이 시려요. 통증은 없어요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `fb774e05385fdb4cecfe24554ab1c0d1b7c1d6f0bc7d91133ce09962faf5f5ba`

## nlu-step2-0481 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 세안할 때마다 눈따가움 그리고 통증은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세안할 때마다 눈따가움 그리고 통증은 없어요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세안할 때마다 눈따가움"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "세안할 때마다 눈따가움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `66a103f41d13168e7dd5bb71b2770998dad148d86b25976c761795a096aa6efc`

## nlu-step2-0482 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 세수할 때마다 눈이 따가워요, 통증은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 세수할 때마다 눈이 따가워요, 통증은 없어여",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "통증은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f7829ef6c75784b8e26dafc56da935ef6d9ed667aaa9159222387faa578146b8`

## nlu-step2-0483 · other_subject · train

의미 가족: `nlu-step2-other_eye_wash` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 씻을 때마다 눈이 시려요 / 아픈 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 씻을 때마다 눈이 시려요 / 아픈 건 아님",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "아픈 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `8be82edf55911af3c664f065012c741cb19c016358633a61acbdfb2af3ae96d5`

## nlu-step2-0484 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 물이 닿을 때마다 눈이 시려요. 모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿을 때마다 눈이 시려요. 모자를 썼어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `09ec8721e394d5c6400e577360c1e1ff43eb5c7e64d4eee3381e312c9b4224a4`

## nlu-step2-0485 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 눈에 물 닿을 때마다 눈따가움, 모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 눈에 물 닿을 때마다 눈따가움, 모자를 썼어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `ad502c5a1a2ea3728946d9be9755bb4cd7b6767c15312b658900048eb760e702`

## nlu-step2-0486 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 물이 닿으면 매번 눈이 따가워요
모자를 썼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿으면 매번 눈이 따가워요\n모자를 썼어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자를 썼어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `ee741681614c9e3bdf8019f38a4f9f7ec46350411af7126df0d6acae6adca37d`

## nlu-step2-0487 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 물이 닿을 때마다 눈이 시려요. 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿을 때마다 눈이 시려요. 모자 쓰고 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9e6e68e0c930761b640357b1f771693eb1eb5f0f35cfa89388125c068edfbc71`

## nlu-step2-0488 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 눈에 물 닿을 때마다 눈따가움 그리고 모자 쓰고 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 눈에 물 닿을 때마다 눈따가움 그리고 모자 쓰고 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9fb6c0d4090e7d1dd7107e6bcc05f571366382cbd2dc41cb37e7b733d007af26`

## nlu-step2-0489 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 물이 닿으면 매번 눈이 따가워요, 모자 쓰고 있었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿으면 매번 눈이 따가워요, 모자 쓰고 있었어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자 쓰고 있었어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `d8d8b9f2d8b4d3d2f20db0c10a3bc29272a900f79d55b2c6fcde4f181f304230`

## nlu-step2-0490 · other_subject · train

의미 가족: `nlu-step2-other_eye_water` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 물이 닿을 때마다 눈이 시려요 / 모자 착용했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 물이 닿을 때마다 눈이 시려요 / 모자 착용했어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "모자 착용했어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f7ac74b4e7b767544bc2b6e1469d1e0833747d6a2432afe010d4c77bdceef0d3`

## nlu-step2-0491 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 땀이 흐를 때마다 눈이 시려요. 차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 흐를 때마다 눈이 시려요. 차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b1e2c1784dd7520b10c3fdd32d019e581aa888ae9960299e35f062fe781d674f`

## nlu-step2-0492 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 땀 흐르면 매번 눈따가움, 차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀 흐르면 매번 눈따가움, 차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c9856f6eeb83ac2b7686ada43e13c97c00cd4775fcb9e4c470666ce309182de1`

## nlu-step2-0493 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 땀이 흘러내릴 때마다 눈이 따가워요
차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 흘러내릴 때마다 눈이 따가워요\n차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b3415e57c95736f36e8e7ce555e677e19cf29264408aae20fc37c33e0593118a`

## nlu-step2-0494 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 땀이 흐를 때마다 눈이 시려요. 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 흐를 때마다 눈이 시려요. 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7c667c74ad8581bfc9deec2a989d2358ef559591cc8e49a35db7e3d7704f2bc2`

## nlu-step2-0495 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 땀 흐르면 매번 눈따가움 그리고 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀 흐르면 매번 눈따가움 그리고 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `546c56f9e25dd0685ca933404c6e4db1e437b77175c37309c6a14bc153823ec9`

## nlu-step2-0496 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 땀이 흘러내릴 때마다 눈이 따가워요, 귀와 목을 차단제 바를 때 빼먹었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 흘러내릴 때마다 눈이 따가워요, 귀와 목을 차단제 바를 때 빼먹었어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `8769182b960eec4e370684c3c886a2f77d006e69f4c4501aa10db55397558c98`

## nlu-step2-0497 · other_subject · train

의미 가족: `nlu-step2-other_eye_sweat` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 땀이 흐를 때마다 눈이 시려요 / 귀 목은 차단제 누락했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 땀이 흐를 때마다 눈이 시려요 / 귀 목은 차단제 누락했어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "차단제",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `4ab13a952367d2a7e6189bb2b0b5b80d731e1a94a5704e03f2c0553267357cdf`

## nlu-step2-0498 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요. 그늘에 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요. 그늘에 머물렀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `3fad259d8dfc6c50d10d0706d1f86e18d0aad053de67a2adf7dd4834acfa2ad0`

## nlu-step2-0499 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 선크림 바르면 매번 눈따가움, 그늘에 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 바르면 매번 눈따가움, 그늘에 머물렀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b4afba41f774d60abe66433fb96110e3d31599ca0e50bfd3a94e3e093f303424`

## nlu-step2-0500 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 선크림 쓸 때마다 눈이 따가워요
그늘에 머물렀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 쓸 때마다 눈이 따가워요\n그늘에 머물렀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 머물렀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7c9db83e267d7e5499d75c71c797c80bfc7744de0bceddb10d35cf5fc26c406a`

## nlu-step2-0501 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요. 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요. 그늘에서 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `70a6d289d3ad72ebb8dbf1e9cfabccc24cd359497b97682f48e7ae9bf817820c`

## nlu-step2-0502 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 선크림 바르면 매번 눈따가움 그리고 그늘에서 있었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 바르면 매번 눈따가움 그리고 그늘에서 있었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `580511a2463b2e4777d4ebd0a7e4fd9ce89feb157350cb1c13ce8e4a208b1d47`

## nlu-step2-0503 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 선크림 쓸 때마다 눈이 따가워요, 그늘에서 있었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 쓸 때마다 눈이 따가워요, 그늘에서 있었어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에서 있었어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f763df5133e89e9308015c0cf7166fbe54be08e43782acfb38d212cbf137dca4`

## nlu-step2-0504 · other_subject · train

의미 가족: `nlu-step2-other_eye_sun` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요 / 그늘에 있었음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 선크림 쓰고 나면 매번 눈이 시려요 / 그늘에 있었음",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "그늘에 머묾",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "그늘에 있었음"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `a0d8212e9753c77d903e5457c9d537a7a13f74fed7dcf85a1eb95d202bf560d8`

## nlu-step2-0505 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 며칠째 계속 건조해요. 보습 후 느낌은 편해요. 건조감 있을 때만 보습 추가해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 건조해요. 보습 후 느낌은 편해요. 건조감 있을 때만 보습 추가해요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1bda93ced7314c378278655851f168a5caefe77fb735b3d0e909c6122506cd41`

## nlu-step2-0506 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 며칠 동안 내내 건조함, 보습 후 느낌은 편해요, 건조감 있을 때만 보습 추가해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠 동안 내내 건조함, 보습 후 느낌은 편해요, 건조감 있을 때만 보습 추가해요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `70681d32dc50ff86eb3c2b41f42853fec9951fb25751f00d6d25c8e90660ce95`

## nlu-step2-0507 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 며칠째 끊이지 않고 건조해요
보습 후 느낌은 편해요
건조감 있을 때만 보습 추가해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 끊이지 않고 건조해요\n보습 후 느낌은 편해요\n건조감 있을 때만 보습 추가해요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "건조감 있을 때만 보습 추가해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `4577842014b1d039467abd048665a6b7c3325ca74dbc772a1bea8e346b71fe09`

## nlu-step2-0508 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 며칠째 계속 건조해요. 보습하고 나면 편안해요. 보습 덧바르는 때는 건조할 때예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 건조해요. 보습하고 나면 편안해요. 보습 덧바르는 때는 건조할 때예요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 덧바르는 때는 건조할 때예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `00f49d94729781f4d117d10990f5bbb15bb8008e635f1c251558272df73c0d63`

## nlu-step2-0509 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 며칠 동안 내내 건조함 그리고 보습하고 나면 편안해요 그리고 보습 덧바르는 때는 건조할 때예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠 동안 내내 건조함 그리고 보습하고 나면 편안해요 그리고 보습 덧바르는 때는 건조할 때예요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 덧바르는 때는 건조할 때예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `a200ece665acefca1fcbc4722abc535e0078f673c114ebcaea90cb6ce22757a2`

## nlu-step2-0510 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 며칠째 끊이지 않고 건조해여, 보습하고 나면 편안해여, 보습 덧바르는 때는 건조할 때예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 끊이지 않고 건조해여, 보습하고 나면 편안해여, 보습 덧바르는 때는 건조할 때예요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해여"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 덧바르는 때는 건조할 때예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 건조해여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `61b96645b504c08a50b610fcdfda27d5989f5e57697b2daefd06fb1daa17eef5`

## nlu-step2-0511 · other_subject · train

의미 가족: `nlu-step2-other_dry` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 며칠째 계속 건조해요 / 보습 뒤 사용감은 편안함 / 건조할 때 보습을 덧발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 건조해요 / 보습 뒤 사용감은 편안함 / 건조할 때 보습을 덧발라요",
  "topics": [
    "discomfort_report",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "보습 뒤 사용감은 편안함"
    },
    {
      "variable_id": "moisturizing.reapplication",
      "value": "건조할 때 덧바름",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "건조할 때 보습을 덧발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `090dc2e49b3246e6d5fe74da43d13781dd113bbf3fe302d6eefc558f504d4643`

## nlu-step2-0512 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 자꾸 트러블이 나요. 추가로 지울 건 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 자꾸 트러블이 나요. 추가로 지울 건 없어요",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "자꾸 트러블이 나요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `5d92ae15aaf1bc5293f76d026c8a71e4d7de8157704d70d8f41276e161c990f3`

## nlu-step2-0513 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 반복해서 트러블 남, 추가로 지울 건 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 반복해서 트러블 남, 추가로 지울 건 없어요",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "반복해서 트러블 남"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `3272afdb8284be89cfeafc8d5ca33fa2f32538a43731fdf32356bb24d079a825`

## nlu-step2-0514 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 괜찮다가 또 트러블이 나요
추가로 지울 건 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 괜찮다가 또 트러블이 나요\n추가로 지울 건 없어요",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "추가로 지울 건 없어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 트러블이 나요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `44431484a13523d99a38fc92b8fcfbe0b1a39d5bf353a218b071b1f05dccb991`

## nlu-step2-0515 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 자꾸 트러블이 나요. 더 제거할 것은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 자꾸 트러블이 나요. 더 제거할 것은 없어요",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "더 제거할 것은 없어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "자꾸 트러블이 나요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `cc7d0a17b2769d775aa059dc01fa1468bea2d11e0c2874fb0e99cee07751de7b`

## nlu-step2-0516 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 반복해서 트러블 남 그리고 더 제거할 것은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 반복해서 트러블 남 그리고 더 제거할 것은 없어요",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "더 제거할 것은 없어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "반복해서 트러블 남"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `c0d218c724ff56378ff0e5179f6603583297fae889617010bf53c8a90a75bda9`

## nlu-step2-0517 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 괜찮다가 또 트러블이 나요, 더 제거할 것은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 괜찮다가 또 트러블이 나요, 더 제거할 것은 없어여",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "더 제거할 것은 없어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 트러블이 나요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `01127631a708228c2a9de9b882f292e0303659480e71ac6c821f46518ea97033`

## nlu-step2-0518 · other_subject · train

의미 가족: `nlu-step2-other_breakout` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 자꾸 트러블이 나요 / 따로 더 지울 게 없음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 자꾸 트러블이 나요 / 따로 더 지울 게 없음",
  "topics": [
    "discomfort_report",
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.target_load",
      "value": "no_additional_removal_need",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "따로 더 지울 게 없음"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "repeated",
      "evidence_span": "자꾸 트러블이 나요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `7a65804c14873bd1a3d8479ed7b68998609a6e0c972abb8cbca90c1ec9525663`

## nlu-step2-0519 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 0

### 원문 raw

저는 방금 처음 붉어져요. 친구는 찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 방금 처음 붉어져요. 친구는 찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `988679ee3892526d41e99e1355e048be5a8ac2b670ef010146cbc88de4b5ce59`

## nlu-step2-0520 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 1

### 원문 raw

저는 조금 전에 처음 붉어짐, 친구는 찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 조금 전에 처음 붉어짐, 친구는 찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 조금 전에 처음 붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9a1878b424b6cda5204e250e30b372668c3171a378db78201ffb23ebe67e90bc`

## nlu-step2-0521 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 2

### 원문 raw

저는 아까 처음 붉어져서 말해요
친구는 찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 아까 처음 붉어져서 말해요\n친구는 찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 아까 처음 붉어져서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `776da9403ca28240a3e07dc8f9b3dbd46edbf6b884d2afbbde7f7a33ad0eba95`

## nlu-step2-0522 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 3

### 원문 raw

저는 방금 처음 붉어져요. 친구는 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 방금 처음 붉어져요. 친구는 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `618cfb98dc3a0fa53bd5d0842a80cc427015d06589b218002f7ec8193201c15e`

## nlu-step2-0523 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 4

### 원문 raw

저는 조금 전에 처음 붉어짐 그리고 친구는 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 조금 전에 처음 붉어짐 그리고 친구는 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 조금 전에 처음 붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9da83bbc40ed3beb3a721e12e53198d7c5a1903f4a6e8c526c3a8691cd89a947`

## nlu-step2-0524 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 5

### 원문 raw

저는 아까 처음 붉어져서 말해여, 친구는 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 아까 처음 붉어져서 말해여, 친구는 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 아까 처음 붉어져서 말해여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `d363efbfdf6b36482f9cc8ba4e0c97e82b5dfc7ecccdcdfc5f64109b115a4c39`

## nlu-step2-0525 · other_subject · train

의미 가족: `nlu-step2-other_red` / 표현 변형: 6

### 원문 raw

저는 방금 처음 붉어져요 / 친구는 차가운 물로 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 방금 처음 붉어져요 / 친구는 차가운 물로 해요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 차가운 물로 해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "저는 방금 처음 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `caaa1f06246f20fda9ef777853d8e05d750b621c92c418c51b569392e262ac92`

## nlu-step2-0526 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 0

### 원문 raw

저는 가려워요. 친구는 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 가려워요. 친구는 용기는 단지형이에요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `943a7d7a5a40b88841f8820266aedc097bfe6bb93720f580680159b2dba8af5f`

## nlu-step2-0527 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 1

### 원문 raw

저는 가려움, 친구는 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 가려움, 친구는 용기는 단지형이에요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e0158c34843127301dd7fa2633c0fd2449c870e1c54a0c54a098caf1ea0ecd75`

## nlu-step2-0528 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 2

### 원문 raw

저는 지금 가려워요
친구는 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 지금 가려워요\n친구는 용기는 단지형이에요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 지금 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9140ee2f5476ae576a86269a05541b71d5949d03d66ce7cac0adf6d281e625d6`

## nlu-step2-0529 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 3

### 원문 raw

저는 가려워요. 친구는 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 가려워요. 친구는 단지 형태 용기예요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `aac9c7ba554613b802030fd8811365811c434b96ff30263718a477a294ba43a2`

## nlu-step2-0530 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 4

### 원문 raw

저는 가려움 그리고 친구는 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 가려움 그리고 친구는 단지 형태 용기예요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `323660bf0bf7347d41349d1f32584b184e05c682e45e2d1d29548815615da23f`

## nlu-step2-0531 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 5

### 원문 raw

저는 지금 가려워요, 친구는 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 지금 가려워요, 친구는 단지 형태 용기예요",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 지금 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `bebb8d706bb56bf23cc5ff93a4c5b47c842916a633d03344738862a6e50091b8`

## nlu-step2-0532 · other_subject · train

의미 가족: `nlu-step2-other_itch` / 표현 변형: 6

### 원문 raw

저는 가려워요 / 친구는 통 모양은 단지형임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저는 가려워요 / 친구는 통 모양은 단지형임",
  "topics": [
    "discomfort_report",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "친구는 통 모양은 단지형임"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "저는 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `285e1d891611672f82d6c271f59686090946ea2d52dc7f5f2fdc00f24bf05339`

## nlu-step2-0533 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 보라 크림 B는 끊었어요. 당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B는 끊었어요. 당기지는 않아요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `33d9e380f59d6a21a55f4a9c5c4f7bdb3743f687c902833c5bd93b5bf565eff0`

## nlu-step2-0534 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 보라 크림 B 사용 중단했어요, 당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B 사용 중단했어요, 당기지는 않아요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `be069305ed8becbf5b7bcaaefaa57f46ed2148ef300ab376538fb0a04b72f1b2`

## nlu-step2-0535 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 보라 크림 B 이제 안 써요
당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B 이제 안 써요\n당기지는 않아요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f7f8be0855af8a31e8e6c2ba4f99ebd4f2c714bed3f0390b30729c30198a6bdc`

## nlu-step2-0536 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 보라 크림 B는 끊었어요. 당김은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B는 끊었어요. 당김은 없어요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `5e47286f37ae4b4ef1df79158fd18940c12a965a95b570026d56941113ee8241`

## nlu-step2-0537 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 보라 크림 B 사용 중단했어요 그리고 당김은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B 사용 중단했어요 그리고 당김은 없어요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f292c5a139d94f564d57faa158d303acb2cb9d1eb6ffb691ef8964a96411eee4`

## nlu-step2-0538 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 보라 크림 B 이제 안 써요, 당김은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B 이제 안 써요, 당김은 없어여",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당김은 없어여"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `9ba2bcd4ec24cd3fa115aea7722791c0b9d45c360bd5b4986d544849bc8d439b`

## nlu-step2-0539 · other_subject · train

의미 가족: `nlu-step2-other_stop` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 보라 크림 B는 끊었어요 / 당기는 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 보라 크림 B는 끊었어요 / 당기는 건 아님",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "당기는 건 아님"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `557da613b82d908ebdf703dbd393db06e2991ea5006de3f17bc2dfeda919250b`

## nlu-step2-0540 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 다온 젤 C 살까 고민해요. 피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 살까 고민해요. 피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `84ca832200f9019f7caca334bbf5bea975abc6b01ee9fa21c9c9738801931eff`

## nlu-step2-0541 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 다온 젤 C 써볼까 생각 중, 피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 써볼까 생각 중, 피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `f03729469c9b301f03eb84ea4c39488fc706ca12e35128a905a403edba51c893`

## nlu-step2-0542 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 다온 젤 C 구매 고려 중이에요
피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 구매 고려 중이에요\n피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e8a2bc762e1386179ef392ac4a6fbcc640d21638590197b632325bb42b9f8271`

## nlu-step2-0543 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 다온 젤 C 살까 고민해요. 씻기 시작할 때 피부는 말라 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 살까 고민해요. 씻기 시작할 때 피부는 말라 있어요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e62230f2f130ab9fb5e94203a9cba7a56ca1359d99980484052c8b1fe446a603`

## nlu-step2-0544 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 다온 젤 C 써볼까 생각 중 그리고 씻기 시작할 때 피부는 말라 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 써볼까 생각 중 그리고 씻기 시작할 때 피부는 말라 있어요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `5c251e6349f6903ea23c5d0cb47dce0c8bee51e6c1fdde4586706256bafbf911`

## nlu-step2-0545 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 다온 젤 C 구매 고려 중이에요, 씻기 시작할 때 피부는 말라 있어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 구매 고려 중이에요, 씻기 시작할 때 피부는 말라 있어여",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `0ea00084cbc7a6fbdbc4aa3396ce451c91b8c13834815488f311b497128783dd`

## nlu-step2-0546 · other_subject · train

의미 가족: `nlu-step2-other_consider` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 다온 젤 C 살까 고민해요 / 물 적시기 전에 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 다온 젤 C 살까 고민해요 / 물 적시기 전에 씻기 시작해요",
  "topics": [
    "other",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "물 적시기 전에 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `06bf2b63b213f0d9141fc58e2b69c9e744f19c40d21e89b65fbb8e2ad8c13c1d`

## nlu-step2-0547 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 며칠째 계속 부어올라요. 방금 처음 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 부어올라요. 방금 처음 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 부어올라요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "방금 처음 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `bd37c0c7263467703024fee6915cec67ff6ef41adce922f6d252c2912cddfcb1`

## nlu-step2-0548 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 며칠 동안 내내 부어오름, 방금 처음 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠 동안 내내 부어오름, 방금 처음 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 부어오름"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "방금 처음 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `a420f268f9a7e27386ddf50858f16b5f492834c4c0a7436225ac674e87753153`

## nlu-step2-0549 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 며칠째 끊이지 않고 부어올라요
방금 처음 아파요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 끊이지 않고 부어올라요\n방금 처음 아파요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 부어올라요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "방금 처음 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `b04ef4f1abd2daf5a583c3ec330415d688339a17638072911c49375a87d1f744`

## nlu-step2-0550 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 며칠째 계속 부어올라요. 조금 전에 처음 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 부어올라요. 조금 전에 처음 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 부어올라요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `69804b5559e7f22fe7f355dbd459504f6ce1e3c387e2e48a2a36cd607ef0d567`

## nlu-step2-0551 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 며칠 동안 내내 부어오름 그리고 조금 전에 처음 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠 동안 내내 부어오름 그리고 조금 전에 처음 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 부어오름"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `78a0b1efa8d832624a10b4058ec41569d4d6751f297d587778f9835a60354220`

## nlu-step2-0552 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 며칠째 끊이지 않고 부어올라요, 조금 전에 처음 통증 있음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 끊이지 않고 부어올라요, 조금 전에 처음 통증 있음",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 부어올라요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 통증 있음"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `56ae6863f6c69cee5fe107ac92c1d593ac739a464e96c1dd1372a283e241d574`

## nlu-step2-0553 · other_subject · val_internal

의미 가족: `nlu-step2-other_symptoms` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 며칠째 계속 부어올라요 / 아까 처음 아파서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 며칠째 계속 부어올라요 / 아까 처음 아파서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 부어올라요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "아까 처음 아파서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `2e3c6637d9e20c34a383512c72025359bfdcea20dfb6c25d6ae514a1170425dc`

## nlu-step2-0554 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 제품 표시대로 해요. 누리 로션 AB 쓰는 중이에요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 제품 표시대로 해요. 누리 로션 AB 쓰는 중이에요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "제품 표시대로 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `dc063909ba43ca1969b9ebf02886930cfad9f690066ca27d787c92184fe3be8d`

## nlu-step2-0555 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 제품에 적힌 제거 방법대로 씻어요, 누리 로션 AB 쓰는 중이에요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 제품에 적힌 제거 방법대로 씻어요, 누리 로션 AB 쓰는 중이에요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "제품에 적힌 제거 방법대로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `e000b68c450093804bdc08f9ade86fa4340aeeb76a0aa7bd220266af9e857f9d`

## nlu-step2-0556 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 횟수는 안 정하고 제거 안내를 따라요
누리 로션 AB 쓰는 중이에요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 횟수는 안 정하고 제거 안내를 따라요\n누리 로션 AB 쓰는 중이에요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "횟수는 안 정하고 제거 안내를 따라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `4634988dd1d7f7e060bbb4ad24682d52ce6167cf752228b2a54f84cf8de2e6ad`

## nlu-step2-0557 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 제품 표시대로 해요. 요즘 누리 로션 AB 써요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 제품 표시대로 해요. 요즘 누리 로션 AB 써요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "제품 표시대로 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `44eca1bd7e73a85d289afab271861a61e25298d24b2a1e8f597cb9457ee84eec`

## nlu-step2-0558 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 제품에 적힌 제거 방법대로 씻어요 그리고 요즘 누리 로션 AB 써요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 제품에 적힌 제거 방법대로 씻어요 그리고 요즘 누리 로션 AB 써요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "제품에 적힌 제거 방법대로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `bf96f06fbb193fc7485d6429bc061a1d0bc33d10d859343a2f8f692601cd487b`

## nlu-step2-0559 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 횟수는 안 정하고 제거 안내를 따라요, 요즘 누리 로션 AB 써요

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 횟수는 안 정하고 제거 안내를 따라요, 요즘 누리 로션 AB 써요",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "횟수는 안 정하고 제거 안내를 따라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `1353e40341565902e1aa19da8acf8e9e21c2f43c605cf5e2d36cc58edfbdeede`

## nlu-step2-0560 · other_subject · val_internal

의미 가족: `nlu-step2-other_label` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 제품 표시대로 해요 / 누리 로션 AB 사용 중임

직전 질문: 친구분은 세안 단계를 어떻게 정하나요?
질문 대상: cleansing.steps

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 제품 표시대로 해요 / 누리 로션 AB 사용 중임",
  "topics": [
    "repeat_cleansing",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "according_to_product_removal_instructions",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "제품 표시대로 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.

내용 SHA-256: `5b99a45c67cf0caaf3125ec0ea89da012a91865654f38c9406e1175dcd18af1c`

## nlu-step2-0561 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 0

### 원문 raw

방금 처음 건조해요. 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 건조해요. 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 건조해요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `fba264aa449b3e2622beb253d750cb875f2bf2f8e4de1cd7dcf3ac31138e6411`

## nlu-step2-0562 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 1

### 원문 raw

조금 전에 처음 건조함, 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 건조함, 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 건조함"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `f271b74e77161dcbd252cd149fa4f32e411ef601d1907292712307f29c8ee881`

## nlu-step2-0563 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 2

### 원문 raw

아까 처음 건조해서 말해요
당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 건조해서 말해요\n당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 건조해서 말해요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0b6878298561d027c1fc58d4f40246c258b17189595b7f2cd83b6861f784dac1`

## nlu-step2-0564 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 3

### 원문 raw

방금 처음 건조해요. 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 건조해요. 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 건조해요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `6b06c57e113950740b703d8b23288a11a3212cde63c870e8dac20ac5ae751f11`

## nlu-step2-0565 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 4

### 원문 raw

조금 전에 처음 건조함 그리고 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 건조함 그리고 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 건조함"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `556cd40fe60be8e79b38150e8c45f98e7ce99f4236164ef691e35185ac9e2cc4`

## nlu-step2-0566 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 5

### 원문 raw

아까 처음 건조해서 말해여, 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 건조해서 말해여, 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 건조해서 말해여"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d9e185e890c531f3691ec044d0ef76516b0866e36275f69a2f9a91c4f354cdab`

## nlu-step2-0567 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_1` / 표현 변형: 6

### 원문 raw

방금 처음 건조해요 / 지금 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 건조해요 / 지금 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 건조해요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `84e518888dfa516cb274aeaf74c32d3f36f07a7a44d7bbae0d0bb10b642f25b9`

## nlu-step2-0568 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 0

### 원문 raw

며칠째 계속 트러블이 나요. 붉어지지 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 트러블이 나요. 붉어지지 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 트러블이 나요"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `f1693a04bd7a765d18ba17e7656696a636870747f6169fa67d6b26dbfb711bee`

## nlu-step2-0569 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 1

### 원문 raw

며칠 동안 내내 트러블 남, 붉어지지 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 트러블 남, 붉어지지 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 트러블 남"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e83ce178b89720aec587629c3fea49c6d98c0182f0dd8e47026849a12d8f0ff4`

## nlu-step2-0570 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 2

### 원문 raw

며칠째 끊이지 않고 트러블이 나요
붉어지지 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 트러블이 나요\n붉어지지 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 트러블이 나요"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어지지 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `fd60ea45f20c6e262411b794372bfe0194e9fe0f7ebdb73a35dbee16c64debf7`

## nlu-step2-0571 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 3

### 원문 raw

며칠째 계속 트러블이 나요. 붉어짐은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 트러블이 나요. 붉어짐은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 트러블이 나요"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `6c3efe6ba0cc81ea302fd00437bf97e64975b9cf1eb8f78781194de87b0fd93a`

## nlu-step2-0572 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 4

### 원문 raw

며칠 동안 내내 트러블 남 그리고 붉어짐은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 트러블 남 그리고 붉어짐은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 트러블 남"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d96774dcf6005714b20ad7e2e51e2ec73ed7abe6aa378ad8afe8bf9fb5c40a00`

## nlu-step2-0573 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 5

### 원문 raw

며칠째 끊이지 않고 트러블이 나요, 붉어짐은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 트러블이 나요, 붉어짐은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 트러블이 나요"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2d13cba062fe055826c2ad2fd33440471f6f8b4fc3f20f5619bd54fae58cb432`

## nlu-step2-0574 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_2` / 표현 변형: 6

### 원문 raw

며칠째 계속 트러블이 나요 / 붉어진 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 트러블이 나요 / 붉어진 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 트러블이 나요"
    },
    {
      "symptom": "redness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어진 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5129a3465cbf9e8990f44b4fcc5dec18c0f536e65763eccb28d0b3e49aab8625`

## nlu-step2-0575 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 0

### 원문 raw

자꾸 붉어져요. 방금 처음 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 붉어져요. 방금 처음 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 붉어져요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e58d8edc2711557406b6ed7134a20e4f24104fe63e144cf204e2125c9c9a142f`

## nlu-step2-0576 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 1

### 원문 raw

반복해서 붉어짐, 방금 처음 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 붉어짐, 방금 처음 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 붉어짐"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bceb26b39f7bf6c40d8ddf742dd93ea3ca7d985fe9ec7262c438ee9c2d130b09`

## nlu-step2-0577 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 2

### 원문 raw

괜찮다가 또 붉어져요
방금 처음 따가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 붉어져요\n방금 처음 따가워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 붉어져요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `da7031ce78273b48b72f54efc2514072fe3ef8696da4ff59619356501bb5a9a2`

## nlu-step2-0578 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 3

### 원문 raw

자꾸 붉어져요. 조금 전에 처음 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 붉어져요. 조금 전에 처음 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 붉어져요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `a4604eafdccf5fc4dd5d8cb5c2aab6648dc3692585d62d4c2212468c6140c5c4`

## nlu-step2-0579 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 4

### 원문 raw

반복해서 붉어짐 그리고 조금 전에 처음 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 붉어짐 그리고 조금 전에 처음 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 붉어짐"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c09341801283cc1f1344037f77ad25f868914513231cf581920cba542b8c87b0`

## nlu-step2-0580 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 5

### 원문 raw

괜찮다가 또 붉어져요, 조금 전에 처음 따가움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 붉어져요, 조금 전에 처음 따가움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 붉어져요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `28202d8c62e46323c59acb2bbd00664c3aa6b54d1efad3dee4bae83298340129`

## nlu-step2-0581 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_3` / 표현 변형: 6

### 원문 raw

자꾸 붉어져요 / 아까 처음 따가워서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 붉어져요 / 아까 처음 따가워서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 붉어져요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 따가워서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7ea7eafb9f7a39fdb20c6628161e61160b267b1466a48bf7c9ca626e68dbeb20`

## nlu-step2-0582 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 0

### 원문 raw

며칠째 계속 따가워요. 아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 따가워요. 아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `6b260d3f344580c70b9d8da0a6b7560e9a0bd9a6ccb4c545940da9e44f458555`

## nlu-step2-0583 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 1

### 원문 raw

며칠 동안 내내 따가움, 아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 따가움, 아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 따가움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ac2d28db612b3047c737b156a2b94478bd707ce3cfecdc4b8e7f696bc358bb6e`

## nlu-step2-0584 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 2

### 원문 raw

며칠째 끊이지 않고 따가워요
아프지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 따가워요\n아프지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아프지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `331f61d661d965060af3f2315f0f7b48a4cd280f899815e822e9f5d5bd61d7c5`

## nlu-step2-0585 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 3

### 원문 raw

며칠째 계속 따가워요. 통증은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 따가워요. 통증은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `be03f84e988145326ccc8291a272dd51b4839866fd8a524d8e2bb2c7efff7e59`

## nlu-step2-0586 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 4

### 원문 raw

며칠 동안 내내 따가움 그리고 통증은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 따가움 그리고 통증은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 따가움"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2ce4102e81bd6d7138f91dd545feb236a1705113b75fdabe24942a3f8e446b96`

## nlu-step2-0587 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 5

### 원문 raw

며칠째 끊이지 않고 따가워요, 통증은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 따가워요, 통증은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `3fde86f74f5a046d176dad6d50a898fa0dbf4b5bd0be531bb329adefd37dfa6c`

## nlu-step2-0588 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_4` / 표현 변형: 6

### 원문 raw

며칠째 계속 따가워요 / 아픈 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 따가워요 / 아픈 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 따가워요"
    },
    {
      "symptom": "pain",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아픈 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `535aa107528ef12339b33813b3769a87076dda6d09e280ff880337490ebbeb6a`

## nlu-step2-0589 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 0

### 원문 raw

자꾸 가려워요. 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 가려워요. 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 가려워요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ac871a4b2045352705c99b56b9c155c4057b91a6d35a5fcde884b373be3f4f5d`

## nlu-step2-0590 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 1

### 원문 raw

반복해서 가려움, 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 가려움, 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 가려움"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0596af306ff4f5d71c2d467500241f63f1e8059b48eb82ae0e038ac07c56aaa7`

## nlu-step2-0591 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 2

### 원문 raw

괜찮다가 또 가려워요
건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 가려워요\n건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 가려워요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `dce847a198a57aad096971b8a40f133743ec2ce1788c11b47d01916bbb1c6ecb`

## nlu-step2-0592 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 3

### 원문 raw

자꾸 가려워요. 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 가려워요. 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 가려워요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `92945f1629fd4bda587415c6dab324b603b4cbd78859edb80f73d79dcabf1076`

## nlu-step2-0593 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 4

### 원문 raw

반복해서 가려움 그리고 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 가려움 그리고 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 가려움"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `435fdff99d3b73e9d0734d9bca25295cfa0b16b50087795d7d5fa6c24c9de4b4`

## nlu-step2-0594 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 5

### 원문 raw

괜찮다가 또 가려워요, 건조함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 가려워요, 건조함",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 가려워요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "건조함"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `3900924b64718e00beafcf364ac0be81f85856e3790d2f327d0f0862d4591229`

## nlu-step2-0595 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_5` / 표현 변형: 6

### 원문 raw

자꾸 가려워요 / 지금 건조해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 가려워요 / 지금 건조해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 가려워요"
    },
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 건조해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5fc413d4c13b7496f929f74ce53e28fb8433bb17fb45d02684e04149764f0062`

## nlu-step2-0596 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 0

### 원문 raw

아파요. 부어오르진 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아파요. 부어오르진 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `54d05b997e81f79177a32eb5f608ee80178d668f363414610a46e0b3b815a706`

## nlu-step2-0597 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 1

### 원문 raw

통증 있음, 부어오르진 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통증 있음, 부어오르진 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증 있음"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0fd8da092b9db7f15a93c7f4c63d09c585d29605eb5bd4edb10799f47c980f28`

## nlu-step2-0598 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 2

### 원문 raw

지금 아파요
부어오르진 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지금 아파요\n부어오르진 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오르진 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `32e42fb5911cc32cf802adca21820e28d46a260158e6f7c256103a23b03476bd`

## nlu-step2-0599 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 3

### 원문 raw

아파요. 부어오름은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아파요. 부어오름은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0509ff449402d990fbb650ba7b74abbe9dd0ac5234881b8d8e7db7a974b73fac`

## nlu-step2-0600 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 4

### 원문 raw

통증 있음 그리고 부어오름은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "통증 있음 그리고 부어오름은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "통증 있음"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `46df7748c4a818d1dd8c7aa04f229e26ed68d90c09ff7dca5274f592e2483512`

## nlu-step2-0601 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 5

### 원문 raw

지금 아파요, 부어오름은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지금 아파요, 부어오름은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `19375292caff03f16521121bc13b78ae9e01c25f885599afc4204ee087c6ae01`

## nlu-step2-0602 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_6` / 표현 변형: 6

### 원문 raw

아파요 / 붓지는 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아파요 / 붓지는 않았어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붓지는 않았어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5f5102a5c1146cbf1b11b1e9dba7d7eb1eabea05eb3084db0149bd52ca59e9a4`

## nlu-step2-0603 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 0

### 원문 raw

며칠째 계속 화끈거려요. 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 화끈거려요. 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 화끈거려요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `679aa25decb354ab6d141ef72e92ca63bc81363d34e16562771f39e5898530e7`

## nlu-step2-0604 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 1

### 원문 raw

며칠 동안 내내 화끈거림, 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 화끈거림, 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 화끈거림"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `15095ef3092c242e6dca71f2a76a27cf04d7e9cadf1ca68beadf0a6e2bcf4cd8`

## nlu-step2-0605 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 2

### 원문 raw

며칠째 끊이지 않고 화끈거려요
붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 화끈거려요\n붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 화끈거려요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `033ac6e6d9cc7615c2cb5a8f8a9ed8cef103cf4967fbb8e006aa3eb73a4af4ba`

## nlu-step2-0606 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 3

### 원문 raw

며칠째 계속 화끈거려요. 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 화끈거려요. 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 화끈거려요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `b75cbc7e5d850ab9d4768c2f9242e98044aa25c37e8ccbcaf344a2ccde501b16`

## nlu-step2-0607 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 4

### 원문 raw

며칠 동안 내내 화끈거림 그리고 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 화끈거림 그리고 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 화끈거림"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7ab5d8cd618afa8a96bd0b1b497597f02bfcb135d4a0c9ca89a25c7f92420f46`

## nlu-step2-0608 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 5

### 원문 raw

며칠째 끊이지 않고 화끈거려요, 붉어짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 화끈거려요, 붉어짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 화끈거려요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "붉어짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d55f45f7f0ce19712aa6ae716aa8b4aac9c932ab012bf5f326295420814c9b9e`

## nlu-step2-0609 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_7` / 표현 변형: 6

### 원문 raw

며칠째 계속 화끈거려요 / 지금 붉어져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 화끈거려요 / 지금 붉어져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 화끈거려요"
    },
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 붉어져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2b65adf79fd507d10cf9a635414ea5e27603dab566924c025a3fd4b350724083`

## nlu-step2-0610 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 0

### 원문 raw

방금 처음 부어올라요. 가렵지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 부어올라요. 가렵지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 부어올라요"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `efeebaab917da6b45edd17e942bfae47c0e1b08a6e17a3ead060467ce2f9299b`

## nlu-step2-0611 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 1

### 원문 raw

조금 전에 처음 부어오름, 가렵지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 부어오름, 가렵지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 부어오름"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `9ac1c183ae0a8f3c5b3428077b51207884a14cf7865b98d5475f5e458059815d`

## nlu-step2-0612 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 2

### 원문 raw

아까 처음 부어올라서 말해요
가렵지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 부어올라서 말해요\n가렵지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 부어올라서 말해요"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가렵지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `a8ef0d5df3e568566e0d49e9a39b2f464a3ef2d621e3687358a69cc7bb1a66b4`

## nlu-step2-0613 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 3

### 원문 raw

방금 처음 부어올라요. 가려움은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 부어올라요. 가려움은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 부어올라요"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2d43693d030a02226f41dcb59d08153ad32a713ca6a25cc0202c8f52b17569dc`

## nlu-step2-0614 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 4

### 원문 raw

조금 전에 처음 부어오름 그리고 가려움은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 부어오름 그리고 가려움은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 부어오름"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `10af826b0b698147ebe3654d52fe42fac17f64e507fedd8c38ffe54047d9a173`

## nlu-step2-0615 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 5

### 원문 raw

아까 처음 부어올라서 말해여, 가려움은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 부어올라서 말해여, 가려움은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 부어올라서 말해여"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려움은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5a7e9ad7476124f9fe1446b8e38d856290c6d7a1f450c596bc3682b55c1c02e2`

## nlu-step2-0616 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_8` / 표현 변형: 6

### 원문 raw

방금 처음 부어올라요 / 가려운 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 부어올라요 / 가려운 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 부어올라요"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "가려운 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e7ffd9cc6698c7ff98d224232990888eaf9f0b0ecc1cbac9bf6d39469342cc8e`

## nlu-step2-0617 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 0

### 원문 raw

며칠째 계속 눈이 시려요. 각질은 벗겨지지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 눈이 시려요. 각질은 벗겨지지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 눈이 시려요"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `cb0cf008c63e4984aa8c9f8cfba5ae3b3a01153721f8ee2313a710c1f17b95ad`

## nlu-step2-0618 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 1

### 원문 raw

며칠 동안 내내 눈따가움, 각질은 벗겨지지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 눈따가움, 각질은 벗겨지지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 눈따가움"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `3efc630af790064e5d33566e8c47abffd5e4afbd1a0aa10df5a8bac492db0943`

## nlu-step2-0619 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 2

### 원문 raw

며칠째 끊이지 않고 눈이 시려요
각질은 벗겨지지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 눈이 시려요\n각질은 벗겨지지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 눈이 시려요"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질은 벗겨지지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bedf6a560c93ac94fefde14bb58f9b208cf2d75248036e5c8f82a00a8ad808f4`

## nlu-step2-0620 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 3

### 원문 raw

며칠째 계속 눈이 시려요. 각질 벗겨짐은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 눈이 시려요. 각질 벗겨짐은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 눈이 시려요"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 벗겨짐은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c23935c9800b38060115cf7fd80451113e643cb9af3f864cfce299d7790482a9`

## nlu-step2-0621 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 4

### 원문 raw

며칠 동안 내내 눈따가움 그리고 각질 벗겨짐은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 눈따가움 그리고 각질 벗겨짐은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 눈따가움"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 벗겨짐은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d9c8d7476890863ef023131c853a749ffc4429fc7ae84b09d12b27e23c6f308c`

## nlu-step2-0622 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 5

### 원문 raw

며칠째 끊이지 않고 눈이 시려요, 각질 벗겨짐은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 눈이 시려요, 각질 벗겨짐은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 눈이 시려요"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 벗겨짐은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `a8d918ffaf6e8b74d792ac5d142cbba26114659a99ff816f953b87f8d0991e25`

## nlu-step2-0623 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_9` / 표현 변형: 6

### 원문 raw

며칠째 계속 눈이 시려요 / 각질 일어난 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 눈이 시려요 / 각질 일어난 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 눈이 시려요"
    },
    {
      "symptom": "peeling",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "각질 일어난 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `860f0f9b186b7ac530c825304e2df2d0e7367c5ac3c94cde355b14839c0acb8c`

## nlu-step2-0624 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 0

### 원문 raw

자꾸 각질이 벗겨져요. 방금 처음 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 각질이 벗겨져요. 방금 처음 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 각질이 벗겨져요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d96b82a179997eb25fedacb960d0c5530b9f1e89830445f77740f444871afbb8`

## nlu-step2-0625 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 1

### 원문 raw

반복해서 각질 벗겨짐, 방금 처음 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 각질 벗겨짐, 방금 처음 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 각질 벗겨짐"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c98515f8ed982a4c10eb7d7ef4ff6fd139ee86feba6ee2651edc332652569393`

## nlu-step2-0626 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 2

### 원문 raw

괜찮다가 또 각질이 벗겨져요
방금 처음 당겨요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 각질이 벗겨져요\n방금 처음 당겨요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 각질이 벗겨져요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 당겨요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `6bd7cf530347633cd149a7c8b6ccea47dd6485f60ce84ddf8ebbe6658cd5c89a`

## nlu-step2-0627 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 3

### 원문 raw

자꾸 각질이 벗겨져요. 조금 전에 처음 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 각질이 벗겨져요. 조금 전에 처음 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 각질이 벗겨져요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bd99724e266d25d86f85a04b6e3e9363f8548885960d00cbe23a205cc8b583de`

## nlu-step2-0628 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 4

### 원문 raw

반복해서 각질 벗겨짐 그리고 조금 전에 처음 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 각질 벗겨짐 그리고 조금 전에 처음 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 각질 벗겨짐"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `86c49191fca772db428991f9b21fa2521c27d318b3808376c73ddabbbbf2e6c8`

## nlu-step2-0629 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 5

### 원문 raw

괜찮다가 또 각질이 벗겨져요, 조금 전에 처음 당김

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 각질이 벗겨져요, 조금 전에 처음 당김",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 각질이 벗겨져요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 당김"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `b6968ae69e1a4030b88073253dcd3bdccc4b2d4d3c2bc41586761c8bfa980524`

## nlu-step2-0630 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_10` / 표현 변형: 6

### 원문 raw

자꾸 각질이 벗겨져요 / 아까 처음 당겨서 말해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 각질이 벗겨져요 / 아까 처음 당겨서 말해요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 각질이 벗겨져요"
    },
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 당겨서 말해요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ce777927172d1cc196f9186c9e766ad7f01680e91c929bedbd4fe966624fd2a9`

## nlu-step2-0631 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 0

### 원문 raw

자꾸 당겨요. 화끈거리지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 당겨요. 화끈거리지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 당겨요"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `cd2c370bda5181f86b48e05d0317ba04f02bf969876f2184ebc03c72ddd9ac13`

## nlu-step2-0632 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 1

### 원문 raw

반복해서 당김, 화끈거리지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 당김, 화끈거리지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 당김"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `56ae9551a3974773bc0a293e127f1a45e06afb09c34225fb2224e2008f310d75`

## nlu-step2-0633 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 2

### 원문 raw

괜찮다가 또 당겨요
화끈거리지 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 당겨요\n화끈거리지 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 당겨요"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거리지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `31059fbaeaae9a9507db65bd6a4255426f4c5ea376d65dfdf2a791802fb1dee0`

## nlu-step2-0634 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 3

### 원문 raw

자꾸 당겨요. 화끈거림은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 당겨요. 화끈거림은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 당겨요"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d9eeaaebb37c0893c43847f58fa0a9a76f61d209c44b7f50d76b72bad88206bb`

## nlu-step2-0635 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 4

### 원문 raw

반복해서 당김 그리고 화끈거림은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 당김 그리고 화끈거림은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 당김"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `59a6cadf541c7f3ad0500106eb8e29f202e3ebbc422dcfe93717cf8873fd35e9`

## nlu-step2-0636 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 5

### 원문 raw

괜찮다가 또 당겨요, 화끈거림은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 당겨요, 화끈거림은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 당겨요"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ccbf2476e65fdf43ff850ef7ea45486b7df4708fb6cb7d89b5479c6eb6f4c5e5`

## nlu-step2-0637 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_11` / 표현 변형: 6

### 원문 raw

자꾸 당겨요 / 화끈거린 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 당겨요 / 화끈거린 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 당겨요"
    },
    {
      "symptom": "burning",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거린 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `f81e95736338c9be81e3b71145896ba2e250bccdb8f10187ddfd35e6bb5d033c`

## nlu-step2-0638 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 0

### 원문 raw

씻을 때마다 눈이 시려요. 아침저녁 젤 세정제 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻을 때마다 눈이 시려요. 아침저녁 젤 세정제 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `aebe6d0fde8b4740ef223dd5b7b622ee373b381577bae1b5a2f02c7f55bd7aff`

## nlu-step2-0639 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 1

### 원문 raw

세안할 때마다 눈따가움, 아침저녁 젤 세정제 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안할 때마다 눈따가움, 아침저녁 젤 세정제 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안할 때마다 눈따가움"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "세안할 때마다 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `10fce5eed6864cec7c35e33fab0cec7c15afbc1a3816484bcd7866cc0c30d140`

## nlu-step2-0640 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 2

### 원문 raw

세수할 때마다 눈이 따가워요
아침저녁 젤 세정제 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세수할 때마다 눈이 따가워요\n아침저녁 젤 세정제 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e1c8ea06aa6d0e519cdeed75394a626ece6416cf0d8bf84ba15d4073bb9cfe99`

## nlu-step2-0641 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 3

### 원문 raw

씻을 때마다 눈이 시려요. 젤 세정제는 아침저녁으로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻을 때마다 눈이 시려요. 젤 세정제는 아침저녁으로 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0f795994777108e12c2bbf29b0351ab7e4ef71e1608d1b45c398c4e7648721f3`

## nlu-step2-0642 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 4

### 원문 raw

세안할 때마다 눈따가움 그리고 젤 세정제는 아침저녁으로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세안할 때마다 눈따가움 그리고 젤 세정제는 아침저녁으로 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안할 때마다 눈따가움"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "세안할 때마다 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `dd0ac9f99e438ed7a1395ea751f1275c9a60b45a76577c5ecc61e4f49f233b4c`

## nlu-step2-0643 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 5

### 원문 raw

세수할 때마다 눈이 따가워요, 젤 세정제는 아침저녁으로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "세수할 때마다 눈이 따가워요, 젤 세정제는 아침저녁으로 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "세수할 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c48aac9bc24b9381195df17ddee72c00faaeb1a6bcfb81f06386cda9d9bd8f35`

## nlu-step2-0644 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_12` / 표현 변형: 6

### 원문 raw

씻을 때마다 눈이 시려요 / 아침과 저녁에 젤 세정제 씀

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "씻을 때마다 눈이 시려요 / 아침과 저녁에 젤 세정제 씀",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침과 저녁에 젤 세정제 씀"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "씻을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `26af7dc76d9ebfafae9f574dfd63aed8c7e85d3a1fb4810b9c5d4136f113793c`

## nlu-step2-0645 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 0

### 원문 raw

물이 닿을 때마다 눈이 시려요. 찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿을 때마다 눈이 시려요. 찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `4ca2d6db8ed487b5935c892010c216a746f7b5f9411447803d11e80749dbc3f4`

## nlu-step2-0646 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 1

### 원문 raw

눈에 물 닿을 때마다 눈따가움, 찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈에 물 닿을 때마다 눈따가움, 찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7d3dd908daad4dc6ad3eaac7aac137e00c07b3994f35b7f9ea99a1bef1e0d071`

## nlu-step2-0647 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 2

### 원문 raw

물이 닿으면 매번 눈이 따가워요
찬물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿으면 매번 눈이 따가워요\n찬물 써요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "찬물 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5bc2b01069b3f6b064c45b2897200125a40e4b5b75927a0ef91a880f48b3713e`

## nlu-step2-0648 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 3

### 원문 raw

물이 닿을 때마다 눈이 시려요. 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿을 때마다 눈이 시려요. 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `3018af0ac62640f4d2f4a915841f564ff7030b2c21f8710171edb46245de4a66`

## nlu-step2-0649 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 4

### 원문 raw

눈에 물 닿을 때마다 눈따가움 그리고 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "눈에 물 닿을 때마다 눈따가움 그리고 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "눈에 물 닿을 때마다 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `670d21a5402248b1f97806277caa6d7e0189f75920bbfc6fb8b1ecf52bac19d3`

## nlu-step2-0650 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 5

### 원문 raw

물이 닿으면 매번 눈이 따가워요, 물은 차가워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿으면 매번 눈이 따가워요, 물은 차가워요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 차가워요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "물이 닿으면 매번 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c35e086b5b38660fdf701cee2aa7d50e12d50fe0eed96fe68b4658f1fd78ead4`

## nlu-step2-0651 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_13` / 표현 변형: 6

### 원문 raw

물이 닿을 때마다 눈이 시려요 / 차가운 물로 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "물이 닿을 때마다 눈이 시려요 / 차가운 물로 해요",
  "topics": [
    "discomfort_report",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "물 닿을 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차가운 물로 해요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "물이 닿을 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e4e6a5a74bcca46c29bc15c11dd1a600a0cfc811a9286a8f6b09cfba704bdc3d`

## nlu-step2-0652 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 0

### 원문 raw

땀이 흐를 때마다 눈이 시려요. 물이 닿지는 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요. 물이 닿지는 않았어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7b54ec809c7293756b242f83f7f31efd47cf2d32e96c3fa03cf89e4bda387f82`

## nlu-step2-0653 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 1

### 원문 raw

땀 흐르면 매번 눈따가움, 물이 닿지는 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 흐르면 매번 눈따가움, 물이 닿지는 않았어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `52c769f713923760fd287731b2598bbd6783188c9a9367c722d2efd1b1d849ae`

## nlu-step2-0654 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 2

### 원문 raw

땀이 흘러내릴 때마다 눈이 따가워요
물이 닿지는 않았어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흘러내릴 때마다 눈이 따가워요\n물이 닿지는 않았어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물이 닿지는 않았어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `367161ca2cc7dd3d5912db04d78469acbcfcc2d830f455028be3dc58cdb9fa5b`

## nlu-step2-0655 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 3

### 원문 raw

땀이 흐를 때마다 눈이 시려요. 물 접촉은 없었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요. 물 접촉은 없었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bf1a927ee592ddb584068862924fc6a12cbe9c707a9c9ff5e2945ab40b3cc203`

## nlu-step2-0656 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 4

### 원문 raw

땀 흐르면 매번 눈따가움 그리고 물 접촉은 없었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀 흐르면 매번 눈따가움 그리고 물 접촉은 없었어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀 흐르면 매번 눈따가움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `18eef8650eb812eda8c64a956cb0f2282d9c5930c2577de29ba0af75d8550a28`

## nlu-step2-0657 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 5

### 원문 raw

땀이 흘러내릴 때마다 눈이 따가워요, 물 접촉은 없었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흘러내릴 때마다 눈이 따가워요, 물 접촉은 없었어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 접촉은 없었어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흘러내릴 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7286339fe4f87388d4761c268b3c0bafb4f0065ca02dc4df7105a3e60ed85c38`

## nlu-step2-0658 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_14` / 표현 변형: 6

### 원문 raw

땀이 흐를 때마다 눈이 시려요 / 물에 닿은 적 없음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "땀이 흐를 때마다 눈이 시려요 / 물에 닿은 적 없음",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "땀 흐를 때",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    },
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 닿은 적 없음"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "땀이 흐를 때마다 눈이 시려요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `f0d7b924a9df1d9452e3c9aa58efa7b1385d0f712dde1457c2c572aee4dfe87f`

## nlu-step2-0659 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 0

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요. 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요. 땀은 안 났어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `29ff7e9d0b3315aee35a005c24511920e4d47a765ef54e92d67db739ca2c37b8`

## nlu-step2-0660 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 1

### 원문 raw

선크림 바르면 매번 눈따가움, 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 바르면 매번 눈따가움, 땀은 안 났어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7948a63a57a7fed9e3f6b09cf6b37be29196040282a29950d6c0fd75e53d0f84`

## nlu-step2-0661 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 2

### 원문 raw

선크림 쓸 때마다 눈이 따가워요
땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓸 때마다 눈이 따가워요\n땀은 안 났어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `21b84f3d84afdce8aca6dd75ad4050aa0d1268118b5ad6737191124e08bc7756`

## nlu-step2-0662 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 3

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요. 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요. 땀 안 흘렸어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `21286daea4e17d93410d815066213ac4fb38797e10c635abbad44b0a72a085f7`

## nlu-step2-0663 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 4

### 원문 raw

선크림 바르면 매번 눈따가움 그리고 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 바르면 매번 눈따가움 그리고 땀 안 흘렸어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c1148fa7ede0e437eb279956cf847fe45135b5324278c6d5a0f689da756478c9`

## nlu-step2-0664 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 5

### 원문 raw

선크림 쓸 때마다 눈이 따가워요, 땀 안 흘렸어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓸 때마다 눈이 따가워요, 땀 안 흘렸어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7d6e72219db58395f741e379f0a6a0bc4f2b80b46c60de54f3f619ec4f392b66`

## nlu-step2-0665 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_15` / 표현 변형: 6

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요 / 땀난 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요 / 땀난 건 아니에요",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `8c292de2073db3f693301883787cf1649dc837f62e9f60b67783f5719b053b8f`

## nlu-step2-0666 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 0

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요. 저녁에는 크림을 발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요. 저녁에는 크림을 발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ce7478a6fc16aea538602c78281eef19363393b1ace2e5a3d3092fe97bf7a84e`

## nlu-step2-0667 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 1

### 원문 raw

보습하고 두 시간 뒤엔 다시 건조해요, 저녁에는 크림을 발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습하고 두 시간 뒤엔 다시 건조해요, 저녁에는 크림을 발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `0113c45dce342441d18f4fbfe2ae34e23aa6632f64620b5b86ec7f5167975a62`

## nlu-step2-0668 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 2

### 원문 raw

보습한 뒤 2시간 지나 건조감 돌아와요
저녁에는 크림을 발라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습한 뒤 2시간 지나 건조감 돌아와요\n저녁에는 크림을 발라요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `de7fd1e315f689b42b8ec792bdae3d24250e4e23d24b7018f53ea308a3cdb6e9`

## nlu-step2-0669 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 3

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요. 크림은 저녁에 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요. 크림은 저녁에 써요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `24ba61477d1dd776214e1b2b112d4d5234523b44035df71fa2c72e3878ad0eea`

## nlu-step2-0670 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 4

### 원문 raw

보습하고 두 시간 뒤엔 다시 건조해요 그리고 크림은 저녁에 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습하고 두 시간 뒤엔 다시 건조해요 그리고 크림은 저녁에 써요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습하고 두 시간 뒤엔 다시 건조해요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `64abc8e398da603217901dbc976eb88e682dc59fdd8b201faa70fe7022e65f43`

## nlu-step2-0671 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 5

### 원문 raw

보습한 뒤 2시간 지나 건조감 돌아와요, 크림은 저녁에 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습한 뒤 2시간 지나 건조감 돌아와요, 크림은 저녁에 써요",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습한 뒤 2시간 지나 건조감 돌아와요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d9e80a5d7fbdbea4a5addf6e31359a83425cf9ece3d8b6b7cea2c20374f9b593`

## nlu-step2-0672 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_16` / 표현 변형: 6

### 원문 raw

보습 후 2시간쯤 지나면 다시 건조해져요 / 저녁에 크림 바름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보습 후 2시간쯤 지나면 다시 건조해져요 / 저녁에 크림 바름",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "2시간",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "보습 후 2시간쯤 지나면 다시 건조해져요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `89cc18ea945df6bb0b651bce44b02492918dd11d6ea9949325d572446a4539fd`

## nlu-step2-0673 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 0

### 원문 raw

방금 처음 트러블이 나요. 며칠째 계속 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 트러블이 나요. 며칠째 계속 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 트러블이 나요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `9b5c3cdc437d72c77b6b01431605bfd6edec01d99dfb118d6ee8efac684c88ec`

## nlu-step2-0674 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 1

### 원문 raw

조금 전에 처음 트러블 남, 며칠째 계속 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 트러블 남, 며칠째 계속 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 트러블 남"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `38475b33532a1bbf2a159509bbd2fbc918bacd488e1f276487977375fbc44335`

## nlu-step2-0675 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 2

### 원문 raw

아까 처음 트러블이 나서 말해요
며칠째 계속 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 트러블이 나서 말해요\n며칠째 계속 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 트러블이 나서 말해요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `c77de5992bc4c0271a2f2e185225a6ec1cc014204894af27a721ab9dde420610`

## nlu-step2-0676 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 3

### 원문 raw

방금 처음 트러블이 나요. 며칠 동안 내내 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 트러블이 나요. 며칠 동안 내내 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 트러블이 나요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2032e198fd88e372d0cccaf78949701a31302d926941b4ec4bfb2de7b565e950`

## nlu-step2-0677 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 4

### 원문 raw

조금 전에 처음 트러블 남 그리고 며칠 동안 내내 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "조금 전에 처음 트러블 남 그리고 며칠 동안 내내 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "조금 전에 처음 트러블 남"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `8448e5e8314a407dc8f149ba46ae6813c18c4eb763f847c274d13bcb6568a222`

## nlu-step2-0678 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 5

### 원문 raw

아까 처음 트러블이 나서 말해여, 며칠 동안 내내 가려움

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아까 처음 트러블이 나서 말해여, 며칠 동안 내내 가려움",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "아까 처음 트러블이 나서 말해여"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 가려움"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `6fb4b236cac648923d83f4ccd49232fff0a955f5fd215018f6d8fd323a977468`

## nlu-step2-0679 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_17` / 표현 변형: 6

### 원문 raw

방금 처음 트러블이 나요 / 며칠째 끊이지 않고 가려워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 처음 트러블이 나요 / 며칠째 끊이지 않고 가려워요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "breakout",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 처음 트러블이 나요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 가려워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `edf223d3d85b1c7646763db6324e409281444c35eb85869d63b8aa8f4b1c54ed`

## nlu-step2-0680 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 0

### 원문 raw

자꾸 아파요. 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 아파요. 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `7c1ce33419a8b0dcd19c9d4b26564e32610c9b87949e29bfcbda237258e270de`

## nlu-step2-0681 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 1

### 원문 raw

반복해서 통증 있음, 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 통증 있음, 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 통증 있음"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bb352dd69e6d02aa517ae6ae5c358ab778cc3a37503da2448b310fe57c6c16e0`

## nlu-step2-0682 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 2

### 원문 raw

괜찮다가 또 아파요
부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 아파요\n부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d3087eea78d25056fbfc794aab159aa8df41db39369153308401455a468e7330`

## nlu-step2-0683 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 3

### 원문 raw

자꾸 아파요. 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 아파요. 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `520827049320ca57572b09628b7cfa518c36dcea7d1c91fa8086181acb01d38c`

## nlu-step2-0684 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 4

### 원문 raw

반복해서 통증 있음 그리고 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반복해서 통증 있음 그리고 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "반복해서 통증 있음"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `689b6edea08b07f825e9d7daa85c8cdc459bda7536fa191fc7a0be2268ca4445`

## nlu-step2-0685 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 5

### 원문 raw

괜찮다가 또 아파요, 부어오름

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "괜찮다가 또 아파요, 부어오름",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "괜찮다가 또 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "부어오름"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `d4b7c484c94fc42a294f26012fece09cc6036b7dab9293c191a319414bfa3ae6`

## nlu-step2-0686 · high_risk_symptom · train

의미 가족: `nlu-step2-symptom_18` / 표현 변형: 6

### 원문 raw

자꾸 아파요 / 지금 부어올라요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "자꾸 아파요 / 지금 부어올라요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "자꾸 아파요"
    },
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 부어올라요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `bd0b7bddcccd2d81257abb785104378faa3075b3a06f6d3573860b1f87c8248a`

## nlu-step2-0687 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 0

### 원문 raw

화끈거려요. 며칠째 계속 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거려요. 며칠째 계속 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거려요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ff0e33df7be73272324655624ce8ac8111e7ac01504c29c6934be6b72bd00796`

## nlu-step2-0688 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 1

### 원문 raw

화끈거림, 며칠째 계속 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거림, 며칠째 계속 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `5e5fa0f42c60bc6ac6f469db3115272f8d338d8925f76b042ece9aa7064d020c`

## nlu-step2-0689 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 2

### 원문 raw

지금 화끈거려요
며칠째 계속 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지금 화끈거려요\n며칠째 계속 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 화끈거려요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `2f1b959a6ebb641d32152a73797cd6243312c7a2c83ca6346b0346830a090541`

## nlu-step2-0690 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 3

### 원문 raw

화끈거려요. 며칠 동안 내내 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거려요. 며칠 동안 내내 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거려요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `3ac60b951c3d2d9cd3755a6b40e510d743c9004aa92031db73b34f03508bf6a1`

## nlu-step2-0691 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 4

### 원문 raw

화끈거림 그리고 며칠 동안 내내 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거림 그리고 며칠 동안 내내 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거림"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `a644eea529686cee289347fbf2634d176098ee993e8b79d41efa36972f1a3250`

## nlu-step2-0692 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 5

### 원문 raw

지금 화끈거려요, 며칠 동안 내내 각질 벗겨짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "지금 화끈거려요, 며칠 동안 내내 각질 벗겨짐",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "지금 화끈거려요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 각질 벗겨짐"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `146f9821f00e269a114fddc8940e3b3c21478c5a53c7a79caf98dd546314310d`

## nlu-step2-0693 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_19` / 표현 변형: 6

### 원문 raw

화끈거려요 / 며칠째 끊이지 않고 각질이 벗겨져요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "화끈거려요 / 며칠째 끊이지 않고 각질이 벗겨져요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "화끈거려요"
    },
    {
      "symptom": "peeling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 각질이 벗겨져요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `e80af21cef045c118a12553f3897588fded722fb4e2d6c98eda0b94290153b69`

## nlu-step2-0694 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 0

### 원문 raw

며칠째 계속 붉어져요. 당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 붉어져요. 당기지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 붉어져요"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `716c7b3761bf70190e97c7ddd7d846c023cef531d3645ae364772026e04fb802`

## nlu-step2-0695 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 1

### 원문 raw

며칠 동안 내내 붉어짐, 당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 붉어짐, 당기지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 붉어짐"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `ae176f0bafb8af7c4e9d1098ce7e32b86f9df55d6b3f72bcee26a38d1680c4bd`

## nlu-step2-0696 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 2

### 원문 raw

며칠째 끊이지 않고 붉어져요
당기지는 않아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 붉어져요\n당기지는 않아요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 붉어져요"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기지는 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `9237f789bf148ab60963b360f1410d1539b98fee543afb771a772cefeb972c37`

## nlu-step2-0697 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 3

### 원문 raw

며칠째 계속 붉어져요. 당김은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 붉어져요. 당김은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 붉어져요"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `91a6ab97c8a2279c7378f9efefd74daba2fa6b40fceb62fe9a8badc16fd91198`

## nlu-step2-0698 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 4

### 원문 raw

며칠 동안 내내 붉어짐 그리고 당김은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠 동안 내내 붉어짐 그리고 당김은 없어요",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠 동안 내내 붉어짐"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김은 없어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `8096c533710ab756d786e1958fd68a2927606213839a102d49a60b033701ddb9`

## nlu-step2-0699 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 5

### 원문 raw

며칠째 끊이지 않고 붉어져요, 당김은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 끊이지 않고 붉어져요, 당김은 없어여",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 끊이지 않고 붉어져요"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당김은 없어여"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `30f3689d3d304721fb67da87dac738058f9f74e6c180f48e382c1bdbd47ccdc2`

## nlu-step2-0700 · high_risk_symptom · val_internal

의미 가족: `nlu-step2-symptom_20` / 표현 변형: 6

### 원문 raw

며칠째 계속 붉어져요 / 당기는 건 아님

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 붉어져요 / 당기는 건 아님",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "redness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 붉어져요"
    },
    {
      "symptom": "tightness",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "당기는 건 아님"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.

내용 SHA-256: `a4a5a4c0c55fb930a48443020e5f73d7f09d6ac4b7f42865204722b81407b7de`

## nlu-step2-0701 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 0

### 원문 raw

요즘 누리 로션 A 써요. 물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요. 물은 미지근해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `76787360aef175fbc6ff3d72c03113ae426b601556c248fb036f897b63859dbc`

## nlu-step2-0702 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 1

### 원문 raw

누리 로션 A 쓰고 있어요, 물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 A 쓰고 있어요, 물은 미지근해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e5ffefd38008ffe4cc940545db0b1b9f64a8e754ffc30f1d27013f38d9dfaa49`

## nlu-step2-0703 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 2

### 원문 raw

현재 누리 로션 A 사용 중
물은 미지근해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 누리 로션 A 사용 중\n물은 미지근해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물은 미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `2ab03d3c1d68adfb53d821f8aa6fae436e046c5dbd3b3abad1a2f4c559419646`

## nlu-step2-0704 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 3

### 원문 raw

요즘 누리 로션 A 써요. 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요. 미지근한 물 써요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `9e0647f51494cbb3f9e6f604323348d8bc3696190bbeab95d927cb6bcd1b5487`

## nlu-step2-0705 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 4

### 원문 raw

누리 로션 A 쓰고 있어요 그리고 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 A 쓰고 있어요 그리고 미지근한 물 써요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `95c200c5f42787e4b7f4dc51f28b4d18fac4815a2494bb2db89e51b076c1ec18`

## nlu-step2-0706 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 5

### 원문 raw

현재 누리 로션 A 사용 중, 미지근한 물 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 누리 로션 A 사용 중, 미지근한 물 써요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c7f87eb290d18e06ab8e6afcd431ab96f69c6d32d639f0849a1a5075e86562d4`

## nlu-step2-0707 · product_mention · train

의미 가족: `nlu-step2-using_no_freq` / 표현 변형: 6

### 원문 raw

요즘 누리 로션 A 써요 / 물 온도 미지근함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요 / 물 온도 미지근함",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 온도 미지근함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e0a78ef89549b66a1ae14f16cbcbfe3b19726533533b87680d403c035700b36c`

## nlu-step2-0708 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 0

### 원문 raw

보라 크림 B는 끊었어요. 전이랑 냄새가 달라졌어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 전이랑 냄새가 달라졌어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e6618cd98f37e45ca9ccec33ae628bac157274bd7d7c873d283fa272d62cdb19`

## nlu-step2-0709 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 1

### 원문 raw

보라 크림 B 사용 중단했어요, 전이랑 냄새가 달라졌어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요, 전이랑 냄새가 달라졌어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7eadeea38514e1354a2e0b39740ea15f879122074e4d57250eae2d671afde4aa`

## nlu-step2-0710 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 2

### 원문 raw

보라 크림 B 이제 안 써요
전이랑 냄새가 달라졌어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요\n전이랑 냄새가 달라졌어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "전이랑 냄새가 달라졌어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `deb0d49d10aa0467c287e1675972c95d0775acac6485233c674fb168c2d1236b`

## nlu-step2-0711 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 3

### 원문 raw

보라 크림 B는 끊었어요. 이전과 다른 냄새가 나요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 이전과 다른 냄새가 나요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이전과 다른 냄새가 나요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c0bff7c3f0bb2ef537f2e23ab7c23b635839f3623fe2c845e24fc3a49f529695`

## nlu-step2-0712 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 4

### 원문 raw

보라 크림 B 사용 중단했어요 그리고 이전과 다른 냄새가 나요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요 그리고 이전과 다른 냄새가 나요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이전과 다른 냄새가 나요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5ffaf222df7a7aed5b9899186a7603c2369f6576275c9026cb17f707b8c2a285`

## nlu-step2-0713 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 5

### 원문 raw

보라 크림 B 이제 안 써요, 이전과 다른 냄새가 나요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요, 이전과 다른 냄새가 나요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "이전과 다른 냄새가 나요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c9c56e61f8d1c432eb7c5ac0a8ff84ea543d23be0f35b44868e71950ae79ba4e`

## nlu-step2-0714 · product_mention · train

의미 가족: `nlu-step2-stopped` / 표현 변형: 6

### 원문 raw

보라 크림 B는 끊었어요 / 냄새가 예전과 달라짐

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요 / 냄새가 예전과 달라짐",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.sensory_change",
      "value": "전과 다른 냄새",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "냄새가 예전과 달라짐"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b26eba38721f6d88db3e21e4ccfb0ecdbeca9118b1cfef4362fd0349d9023d4d`

## nlu-step2-0715 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 0

### 원문 raw

다온 젤 C 살까 고민해요. 보습 후 느낌은 편해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요. 보습 후 느낌은 편해요",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1abad03cbcd20894c39c68b4572c40a86041b2f790133f00acfa1847d7113060`

## nlu-step2-0716 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 1

### 원문 raw

다온 젤 C 써볼까 생각 중, 보습 후 느낌은 편해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 써볼까 생각 중, 보습 후 느낌은 편해요",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `66fcd85a2d40ee2b0c70d01bb36be4517c642908dc402d88b15c9f0fdaf38242`

## nlu-step2-0717 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 2

### 원문 raw

다온 젤 C 구매 고려 중이에요
보습 후 느낌은 편해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 구매 고려 중이에요\n보습 후 느낌은 편해요",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌은 편해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `23c49c1da72e4caf21cca1e19d418425e2651feab485682ffec19e6d3da8c0d0`

## nlu-step2-0718 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 3

### 원문 raw

다온 젤 C 살까 고민해요. 보습하고 나면 편안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요. 보습하고 나면 편안해요",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `6f78777f2475b677e3325da4631b8507c13e41db096dbdab7bf57213c28a9a92`

## nlu-step2-0719 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 4

### 원문 raw

다온 젤 C 써볼까 생각 중 그리고 보습하고 나면 편안해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 써볼까 생각 중 그리고 보습하고 나면 편안해요",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `4f0b7da0e95b720dc254c39e543b5ba84586739590fb8afb9f92d093da4838b0`

## nlu-step2-0720 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 5

### 원문 raw

다온 젤 C 구매 고려 중이에요, 보습하고 나면 편안해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 구매 고려 중이에요, 보습하고 나면 편안해여",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 편안해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `328a0ae3c5c64898e797fb4f413f2db04a600c9120b87621d5c36a64a0ac0a6e`

## nlu-step2-0721 · product_mention · train

의미 가족: `nlu-step2-considering` / 표현 변형: 6

### 원문 raw

다온 젤 C 살까 고민해요 / 보습 뒤 사용감은 편안함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 C 살까 고민해요 / 보습 뒤 사용감은 편안함",
  "topics": [
    "other",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "편안함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 사용감은 편안함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `0f827d1d6437c96c44521faced684e3439c87d28fc3c8c02889e71824b7f812f`

## nlu-step2-0722 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 0

### 원문 raw

해솔 토너 D라는 이름 봤어요. 서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요. 서랍 안에 둬요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `3f79cb9b5761305da279bc254616a655d92e294c2bd73cef2d59d789499bea66`

## nlu-step2-0723 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 1

### 원문 raw

해솔 토너 D 이름만 들었어요, 서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D 이름만 들었어요, 서랍 안에 둬요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ab89f158aefaf0e5e9580e5776721831ec2f374b83ead69911b76e0dbe7b1042`

## nlu-step2-0724 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 2

### 원문 raw

해솔 토너 D라는 이름이 기억나요
서랍 안에 둬요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름이 기억나요\n서랍 안에 둬요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안에 둬요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `19bf5bf7497d1d3c6a6acbadb04267f6fdd46a7ca0000428f3930f73f5da3eb8`

## nlu-step2-0725 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 3

### 원문 raw

해솔 토너 D라는 이름 봤어요. 서랍 안쪽에 보관해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요. 서랍 안쪽에 보관해요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `0df735bd66942a3a2f30a20c420d988236bd44fdc323fb73e5c404976cbf6b6e`

## nlu-step2-0726 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 4

### 원문 raw

해솔 토너 D 이름만 들었어요 그리고 서랍 안쪽에 보관해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D 이름만 들었어요 그리고 서랍 안쪽에 보관해요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `777c88ec98f9c731a7e27a6b3d0f72dbf646c9467c56d5be9c8baa8d74be6dc7`

## nlu-step2-0727 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 5

### 원문 raw

해솔 토너 D라는 이름이 기억나요, 서랍 안쪽에 보관해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름이 기억나요, 서랍 안쪽에 보관해여",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "서랍 안쪽에 보관해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e7787f93e5c35538b5fbd9aced15183c7af7f469c200d80b8b0832011483f66a`

## nlu-step2-0728 · product_mention · train

의미 가족: `nlu-step2-unknown` / 표현 변형: 6

### 원문 raw

해솔 토너 D라는 이름 봤어요 / 보관하는 곳은 서랍 안이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요 / 보관하는 곳은 서랍 안이에요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.light_air",
      "value": "서랍 안 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보관하는 곳은 서랍 안이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c615cef841e79f545a6e0d96ef493f9ac29f03f8f74db244e97b40787de58ba5`

## nlu-step2-0729 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 0

### 원문 raw

누리 로션 AB 쓰는 중이에요. 씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요. 씻고 3분 뒤에 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `f439066aa74ba71fb83f9e1695a3c44c1bce9eb8f285f628f7b37d51a021b87b`

## nlu-step2-0730 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 1

### 원문 raw

요즘 누리 로션 AB 써요, 씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 AB 써요, 씻고 3분 뒤에 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `32e4ebb422c833964bda84a4d6cf0c1855a67e564bf7d9fea8c009d62c0a6192`

## nlu-step2-0731 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 2

### 원문 raw

누리 로션 AB 사용 중임
씻고 3분 뒤에 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 사용 중임\n씻고 3분 뒤에 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻고 3분 뒤에 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `f5189c7ea0603de91f0dbc7a7bdce8c214fdaf7f806b66496a498748fddfeb43`

## nlu-step2-0732 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 3

### 원문 raw

누리 로션 AB 쓰는 중이에요. 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요. 세안 후 보습까지 3분 걸려요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `fb54ad363898e3d522669fa96a722f2ee1276c8667ea482ba01c8a2b8d447ebb`

## nlu-step2-0733 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 4

### 원문 raw

요즘 누리 로션 AB 써요 그리고 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 AB 써요 그리고 세안 후 보습까지 3분 걸려요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `d7f7b4a9fbcf5d54407e43b302a820f66d8f1c6f220c358b66cb734ac9b8aff6`

## nlu-step2-0734 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 5

### 원문 raw

누리 로션 AB 사용 중임, 세안 후 보습까지 3분 걸려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 사용 중임, 세안 후 보습까지 3분 걸려요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안 후 보습까지 3분 걸려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `6ccc26d8bb2edd625256205041f357ffa30d6d3225a8baa81e9733d25cd11e1b`

## nlu-step2-0735 · product_mention · train

의미 가족: `nlu-step2-prefix` / 표현 변형: 6

### 원문 raw

누리 로션 AB 쓰는 중이에요 / 보습은 세안하고 삼 분 뒤예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요 / 보습은 세안하고 삼 분 뒤예요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "3분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 세안하고 삼 분 뒤예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ce42b049ef40346544e919843061fdeea8358ed91bf4a008b5b13d2b922de0f3`

## nlu-step2-0736 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 0

### 원문 raw

가온 크림 E 쓰는 중이에요. 보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가온 크림 E 쓰는 중이에요. 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `44b822dbe30dc059699e54634d3b1725543e9f1a21b9e2fe5281f4e54a1a3022`

## nlu-step2-0737 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 1

### 원문 raw

요즘 가온 크림 E 써요, 보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 가온 크림 E 써요, 보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1fbd3fecab8edd150ea86e6b5d1b0b11758ae2cdac2e2c138bb78dd77369d75b`

## nlu-step2-0738 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 2

### 원문 raw

가온 크림 E 사용 중임
보습은 볼에만 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가온 크림 E 사용 중임\n보습은 볼에만 해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습은 볼에만 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `dd9b8251d5b2ad8f54bfa78ec2744d959f8c35b405425e7ac6ba6ce9251b06e5`

## nlu-step2-0739 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 3

### 원문 raw

가온 크림 E 쓰는 중이에요. 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가온 크림 E 쓰는 중이에요. 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `79d6b64dcabff04ef716c75e2f7f449ffd347f956f2df96bc84fb140062a84de`

## nlu-step2-0740 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 4

### 원문 raw

요즘 가온 크림 E 써요 그리고 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 가온 크림 E 써요 그리고 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `fd558394a40be4a795022cedb4e7ba25d3c9b4e4d2e18892c60d401f93547b3f`

## nlu-step2-0741 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 5

### 원문 raw

가온 크림 E 사용 중임, 보습 바르는 범위는 볼뿐이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가온 크림 E 사용 중임, 보습 바르는 범위는 볼뿐이에요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 바르는 범위는 볼뿐이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1ca680c36376a71b188b9fae0cfee0542efc45eb006df414f9f6a1000f770cd0`

## nlu-step2-0742 · product_mention · train

의미 가족: `nlu-step2-exact` / 표현 변형: 6

### 원문 raw

가온 크림 E 쓰는 중이에요 / 볼만 보습해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "가온 크림 E 쓰는 중이에요 / 볼만 보습해요",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": "볼에만 도포",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "볼만 보습해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e5095594ab218f0bd30cc6ca8ea4a61524ced5c0e49217be47b5b7c890dab042`

## nlu-step2-0743 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 0

### 원문 raw

다온 젤 CC 사볼까 해요. 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 사볼까 해요. 용기는 단지형이에요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ad5498995ebee5175a850f66752e623a4272f83049871c066298fa30e35724f8`

## nlu-step2-0744 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 1

### 원문 raw

다온 젤 CC 구매 고민 중이에요, 용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 구매 고민 중이에요, 용기는 단지형이에요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `73049bdd55d1fc62c9ed4be0646450f0a04c0e9b492f40551a56f27458267d84`

## nlu-step2-0745 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 2

### 원문 raw

다온 젤 CC 써볼까 생각해요
용기는 단지형이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 써볼까 생각해요\n용기는 단지형이에요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "용기는 단지형이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7a14b01a6ae0bf191b9c8c17c98374718c27869c09a807312f5e999dba9092a7`

## nlu-step2-0746 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 3

### 원문 raw

다온 젤 CC 사볼까 해요. 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 사볼까 해요. 단지 형태 용기예요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `30f921524bad8874adc741feaf13e53a6c1614d68e58d84b0a306133478c69f8`

## nlu-step2-0747 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 4

### 원문 raw

다온 젤 CC 구매 고민 중이에요 그리고 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 구매 고민 중이에요 그리고 단지 형태 용기예요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `54a33c37ac09c5e57a3f9386f2f41e329c1dcb270bb2dff398ee1b312859c8d1`

## nlu-step2-0748 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 5

### 원문 raw

다온 젤 CC 써볼까 생각해여, 단지 형태 용기예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 써볼까 생각해여, 단지 형태 용기예요",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "단지 형태 용기예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `696ff6e2ee4c76dc4ab19571dba3506efe9d1d6addbebdc30c34813e07f3de10`

## nlu-step2-0749 · product_mention · train

의미 가족: `nlu-step2-suffix` / 표현 변형: 6

### 원문 raw

다온 젤 CC 사볼까 해요 / 통 모양은 단지형임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다온 젤 CC 사볼까 해요 / 통 모양은 단지형임",
  "topics": [
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.container",
      "value": "단지형 용기",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "통 모양은 단지형임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ba5fe1b36dafd9248975740569042073c1c647d8235446c8001403483a16a364`

## nlu-step2-0750 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 0

### 원문 raw

폼클렌저 쓰고 있어요. 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "폼클렌저 쓰고 있어요. 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `cffddc0b69fb76290395b499a922aa63e9b04f9e5d780e53f1552f0dcfef7d3b`

## nlu-step2-0751 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 1

### 원문 raw

요즘 폼클렌저 써요, 손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 폼클렌저 써요, 손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `206eed23cdb921c688ff6ca14cc10ce4b38e95bebdc66fb0fec39b8c6667290b`

## nlu-step2-0752 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 2

### 원문 raw

현재 폼클렌저 사용 중이에요
손으로 씻어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 폼클렌저 사용 중이에요\n손으로 씻어요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `83fb41e2c3eec05a6f00cc2d176af3bde16686ce612f6d2b2b6ac661f13130a7`

## nlu-step2-0753 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 3

### 원문 raw

폼클렌저 쓰고 있어요. 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "폼클렌저 쓰고 있어요. 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `87d27c5f205d6dc998c9ff06e08c9b00e72d246a275430feeb9befd6a93bcdb9`

## nlu-step2-0754 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 4

### 원문 raw

요즘 폼클렌저 써요 그리고 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 폼클렌저 써요 그리고 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `87d217b8693abdd34cae513257b450e11a3364f6387786efc083800ebb8fe79c`

## nlu-step2-0755 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 5

### 원문 raw

현재 폼클렌저 사용 중이에요, 세정 도구는 손이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 폼클렌저 사용 중이에요, 세정 도구는 손이에요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정 도구는 손이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `4d8ed6630e541dd437c7675232850006e86ca2b6cd02cd2e9f3dc0f6219846a9`

## nlu-step2-0756 · product_mention · train

의미 가족: `nlu-step2-generic` / 표현 변형: 6

### 원문 raw

폼클렌저 쓰고 있어요 / 손만 도구로 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "폼클렌저 쓰고 있어요 / 손만 도구로 써요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손만 도구로 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5c3312eafe9397fb8dbc1a10cd449e158e5ad6c2a50ca759211b40ada93829cd`

## nlu-step2-0757 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 0

### 원문 raw

매일 로션을 써요. 차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요. 차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e30f552e5914befa106db8ed34c3361f06f15434daa1d7be00595e83b53d639e`

## nlu-step2-0758 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 1

### 원문 raw

로션은 매일 발라요, 차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션은 매일 발라요, 차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `fa3e5668ae9fca34160dd8d9ef4d60ae6fa45a2dd875485867bb4d63c0d53bc5`

## nlu-step2-0759 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 2

### 원문 raw

매일 로션 바름
차단제 바를 때 귀랑 목은 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션 바름\n차단제 바를 때 귀랑 목은 빼먹었어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "차단제 바를 때 귀랑 목은 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `845fb14b58501e79646d36bc17d4f83c9c47db6a13fc703309c6a2e1db8db4f0`

## nlu-step2-0760 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 3

### 원문 raw

매일 로션을 써요. 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요. 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `d3a790b286f77f34ea5db4436c0c6a6a1642df257f5d5ff8118a326d49cc8f9a`

## nlu-step2-0761 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 4

### 원문 raw

로션은 매일 발라요 그리고 귀와 목을 차단제 바를 때 빼먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션은 매일 발라요 그리고 귀와 목을 차단제 바를 때 빼먹었어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션은 매일 발라요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `3ba473841975ec561b58804d3068807de78113f1221ec58c117d670b91b49671`

## nlu-step2-0762 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 5

### 원문 raw

매일 로션 바름, 귀와 목을 차단제 바를 때 빼먹었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션 바름, 귀와 목을 차단제 바를 때 빼먹었어여",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션 바름"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀와 목을 차단제 바를 때 빼먹었어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `0b29d79f83a9c06f38675ee368ad38811b2b6cd3085087c75bbbb4bb7836d443`

## nlu-step2-0763 · product_mention · train

의미 가족: `nlu-step2-routine_lotion` / 표현 변형: 6

### 원문 raw

매일 로션을 써요 / 귀 목은 차단제 누락했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 로션을 써요 / 귀 목은 차단제 누락했어요",
  "topics": [
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 로션 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 로션을 써요"
    },
    {
      "variable_id": "sun.coverage_gaps",
      "value": [
        "귀",
        "목"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "귀 목은 차단제 누락했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "차단제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1dabde08250f2c4561781228a18cbae452ea9ad2f81205910960f37514cc271b`

## nlu-step2-0764 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 0

### 원문 raw

저녁에는 크림을 발라요. 피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요. 피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `781590fb8b4f1b1ff06d66a6528de11b1d1f09196fbb644e4e8b0adfc1c03ce8`

## nlu-step2-0765 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 1

### 원문 raw

크림은 저녁에 써요, 피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "크림은 저녁에 써요, 피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b1eb8db6c44690216c3b05119b1f3cb9f385e23a556e816455ddb1d77eca5614`

## nlu-step2-0766 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 2

### 원문 raw

저녁에 크림 바름
피부가 마른 상태로 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에 크림 바름\n피부가 마른 상태로 씻기 시작해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "피부가 마른 상태로 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `21ac1d23a90a999c5e7f1fac5a4bcd2a577abce91edd33f2f61da1886dcd8cf3`

## nlu-step2-0767 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 3

### 원문 raw

저녁에는 크림을 발라요. 씻기 시작할 때 피부는 말라 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요. 씻기 시작할 때 피부는 말라 있어요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `a5d6ad68b92aa95ceda0901fd37eee309e31452a20d731f3ff0e92b107ec6c09`

## nlu-step2-0768 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 4

### 원문 raw

크림은 저녁에 써요 그리고 씻기 시작할 때 피부는 말라 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "크림은 저녁에 써요 그리고 씻기 시작할 때 피부는 말라 있어요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `d4fd7049605c401d9396960576d2923e373ce65e35567c502c27223b465a4605`

## nlu-step2-0769 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 5

### 원문 raw

저녁에 크림 바름, 씻기 시작할 때 피부는 말라 있어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에 크림 바름, 씻기 시작할 때 피부는 말라 있어여",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻기 시작할 때 피부는 말라 있어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c96b0de5d924fb20d14c6ed16115a5d4214a9eabb08fd8b452e5baa05b6cef21`

## nlu-step2-0770 · product_mention · train

의미 가족: `nlu-step2-routine_cream` / 표현 변형: 6

### 원문 raw

저녁에는 크림을 발라요 / 물 적시기 전에 씻기 시작해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 크림을 발라요 / 물 적시기 전에 씻기 시작해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "method.skin_wetness",
      "value": "마른 상태",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물 적시기 전에 씻기 시작해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b1818570e5524475952e099aa19f40f7e4868683e070ac711710045bf1c66346`

## nlu-step2-0771 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 0

### 원문 raw

아침마다 선크림 발라요. 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요. 땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `69c902b0b2d3d42ef4981e742e60f5aee0ad458d13d9b8fe2454ff4b4b7c8c51`

## nlu-step2-0772 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 1

### 원문 raw

선크림은 매일 아침 써요, 땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림은 매일 아침 써요, 땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7c815e723bf6106d556c09a4ff1cb03c592c64f6f7d4e88e1245f463e4a261fb`

## nlu-step2-0773 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 2

### 원문 raw

매일 아침 선크림 바름
땀은 안 났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 아침 선크림 바름\n땀은 안 났어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀은 안 났어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `fe221420b2359d618f8d964df9a2f1b3e41ddcb3fbf9bba9ec2bd768755473a3`

## nlu-step2-0774 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 3

### 원문 raw

아침마다 선크림 발라요. 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요. 땀 안 흘렸어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `9eae93a3d0cfcd66041f688a90ca834fb6bbb74daa440f07cb05aba2ac8fbfab`

## nlu-step2-0775 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 4

### 원문 raw

선크림은 매일 아침 써요 그리고 땀 안 흘렸어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림은 매일 아침 써요 그리고 땀 안 흘렸어요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림은 매일 아침 써요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `bd76baec7c50bfe9d3f838709de1cb83478ef7b2c4cc06a82a48f6ff0278bca5`

## nlu-step2-0776 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 5

### 원문 raw

매일 아침 선크림 바름, 땀 안 흘렸어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 아침 선크림 바름, 땀 안 흘렸어여",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 아침 선크림 바름"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀 안 흘렸어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7adde94e792180ffca048ee2e9aa4a534a0c735b571be6e9e86a7fb70dc9a219`

## nlu-step2-0777 · product_mention · train

의미 가족: `nlu-step2-routine_sun` / 표현 변형: 6

### 원문 raw

아침마다 선크림 발라요 / 땀난 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침마다 선크림 발라요 / 땀난 건 아니에요",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 아침 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침마다 선크림 발라요"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀난 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `25e138e2e5fc5be7de8a00409a5d09639dda9f13ceaa7d02859f39ab0eb242c1`

## nlu-step2-0778 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 0

### 원문 raw

아침저녁 젤 세정제 써요. 물기는 톡톡 두드려 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침저녁 젤 세정제 써요. 물기는 톡톡 두드려 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기는 톡톡 두드려 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b15397e37346b694a4e9c8d10244fc808023ce97d108cc0df3bfc941408aa31f`

## nlu-step2-0779 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 1

### 원문 raw

젤 세정제는 아침저녁으로 써요, 물기는 톡톡 두드려 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "젤 세정제는 아침저녁으로 써요, 물기는 톡톡 두드려 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기는 톡톡 두드려 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `abf93313bffd11335e928c4514a008fdd592ae3ccad9bfbecc372227d207bef6`

## nlu-step2-0780 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 2

### 원문 raw

아침과 저녁에 젤 세정제 씀
물기는 톡톡 두드려 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침과 저녁에 젤 세정제 씀\n물기는 톡톡 두드려 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침과 저녁에 젤 세정제 씀"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기는 톡톡 두드려 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ee825a587fa6929d4f984399fb6dd1a0e793e79b9dd1b4838278235691201ac6`

## nlu-step2-0781 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 3

### 원문 raw

아침저녁 젤 세정제 써요. 물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침저녁 젤 세정제 써요. 물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `cd131952671d40e4daa3d0d2977f9b22eb6fad84e54d96b5f757cfeff0ad3aa6`

## nlu-step2-0782 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 4

### 원문 raw

젤 세정제는 아침저녁으로 써요 그리고 물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "젤 세정제는 아침저녁으로 써요 그리고 물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "젤 세정제는 아침저녁으로 써요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `79e6f36d09cb5e52a91be33cfd5c207804c502140a7058941cbe987721ab0df1`

## nlu-step2-0783 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 5

### 원문 raw

아침과 저녁에 젤 세정제 씀, 물기 닦을 땐 가볍게 두드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침과 저녁에 젤 세정제 씀, 물기 닦을 땐 가볍게 두드려요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침과 저녁에 젤 세정제 씀"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물기 닦을 땐 가볍게 두드려요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `9742bb1daa22a834dfd38cf9f2239fe698687993a2b008288eebbd25a2acaf5d`

## nlu-step2-0784 · product_mention · train

의미 가족: `nlu-step2-routine_gel` / 표현 변형: 6

### 원문 raw

아침저녁 젤 세정제 써요 / 문지르지 않고 물기를 톡톡 닦아요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "아침저녁 젤 세정제 써요 / 문지르지 않고 물기를 톡톡 닦아요",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "아침저녁 젤 세정제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "아침저녁 젤 세정제 써요"
    },
    {
      "variable_id": "method.drying",
      "value": "pat_gently",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "문지르지 않고 물기를 톡톡 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `49b7dba9591a95536f1c895ed2b91ffef1abc50f3fce29e06ee131ace33b2e9a`

## nlu-step2-0785 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 0

### 원문 raw

저녁마다 로션 다음 선크림 발라요. 세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁마다 로션 다음 선크림 발라요. 세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c9ccbf3f3334f6b8715682f91009f25b5f435b848bf29e613a8114e11aea22bd`

## nlu-step2-0786 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 1

### 원문 raw

로션을 바른 뒤 선크림을 저녁마다 써요, 세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션을 바른 뒤 선크림을 저녁마다 써요, 세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1c1f2fb74a0ffe8e2aa3a7051b6bc3a0fb77cb3eee9d27535806190f9c4b03aa`

## nlu-step2-0787 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 2

### 원문 raw

매일 저녁 로션 먼저 선크림 나중에 발라요
세정제 둘을 손바닥에서 섞어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 저녁 로션 먼저 선크림 나중에 발라요\n세정제 둘을 손바닥에서 섞어요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세정제 둘을 손바닥에서 섞어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7477135941b8cbfb8a09643a798773f179d69a13745bfc800cc51dbb330838f9`

## nlu-step2-0788 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 3

### 원문 raw

저녁마다 로션 다음 선크림 발라요. 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁마다 로션 다음 선크림 발라요. 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b26408a2adca9c2e006f32cb17b1979538c2f2424b8c3076e3e1a91a0b2a4fd8`

## nlu-step2-0789 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 4

### 원문 raw

로션을 바른 뒤 선크림을 저녁마다 써요 그리고 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "로션을 바른 뒤 선크림을 저녁마다 써요 그리고 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "로션을 바른 뒤 선크림을 저녁마다 써요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `94ccc04038ee967152267c2a4c0bfe971c88bce63a4149b0632eda9e70f5e092`

## nlu-step2-0790 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 5

### 원문 raw

매일 저녁 로션 먼저 선크림 나중에 발라요, 손바닥에 세정제 두 개 섞어서 써요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "매일 저녁 로션 먼저 선크림 나중에 발라요, 손바닥에 세정제 두 개 섞어서 써요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매일 저녁 로션 먼저 선크림 나중에 발라요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손바닥에 세정제 두 개 섞어서 써요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `96db8637538f7ce0ad2d97289bbb31df20b3eeb174b6929fe4219528f05bb006`

## nlu-step2-0791 · product_mention · train

의미 가족: `nlu-step2-sequence_mix` / 표현 변형: 6

### 원문 raw

저녁마다 로션 다음 선크림 발라요 / 두 세정제를 손바닥에서 혼합해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁마다 로션 다음 선크림 발라요 / 두 세정제를 손바닥에서 혼합해요",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "매일 저녁 로션 후 선크림 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.sequence",
      "value": "로션 다음 선크림",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁마다 로션 다음 선크림 발라요"
    },
    {
      "variable_id": "method.mixing",
      "value": "두 세정제를 손바닥에서 섞음",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "두 세정제를 손바닥에서 혼합해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "세정제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5afe7d196d54fdd0667873e42ac7dfbc7235b2bcd80e1ca06e9c5c920975ee6a`

## nlu-step2-0792 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 0

### 원문 raw

요즘 누리 로션 A 써요. 다온 젤 C 살까 고민해요. 보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요. 다온 젤 C 살까 고민해요. 보습하고 나면 끈적함",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `f12ddd811ddd31aba1b743b206e1a6b8cf0561756d579c0d60fb283707867dad`

## nlu-step2-0793 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 1

### 원문 raw

누리 로션 A 쓰고 있어요, 다온 젤 C 살까 고민해요, 보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 A 쓰고 있어요, 다온 젤 C 살까 고민해요, 보습하고 나면 끈적함",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `60a747b930ff38fbd745380c35d2d39efd2a8dba08f8ee9bb72353ed5caa8cb6`

## nlu-step2-0794 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 2

### 원문 raw

현재 누리 로션 A 사용 중
다온 젤 C 살까 고민해요
보습하고 나면 끈적함

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 누리 로션 A 사용 중\n다온 젤 C 살까 고민해요\n보습하고 나면 끈적함",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습하고 나면 끈적함"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c59e9ef3a0f70196c029e82b9d030bf39b904a6fdd786bf400566954ff9c09e1`

## nlu-step2-0795 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 3

### 원문 raw

요즘 누리 로션 A 써요. 다온 젤 C 써볼까 생각 중. 보습 뒤 감촉은 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요. 다온 젤 C 써볼까 생각 중. 보습 뒤 감촉은 끈적해요",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `72482aaec34b73aeca37546e9532fa2a2d62a07e4231ef458a253367f1f0823b`

## nlu-step2-0796 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 4

### 원문 raw

누리 로션 A 쓰고 있어요 그리고 다온 젤 C 써볼까 생각 중 그리고 보습 뒤 감촉은 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 A 쓰고 있어요 그리고 다온 젤 C 써볼까 생각 중 그리고 보습 뒤 감촉은 끈적해요",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `560661e411359787fa6a00a503f091c635bd602cdccc8c6128747ec4ba6556c2`

## nlu-step2-0797 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 5

### 원문 raw

현재 누리 로션 A 사용 중, 다온 젤 C 써볼까 생각 중, 보습 뒤 감촉은 끈적해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "현재 누리 로션 A 사용 중, 다온 젤 C 써볼까 생각 중, 보습 뒤 감촉은 끈적해여",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 뒤 감촉은 끈적해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `87c298c497dc473f08bcaf5eaa2e7e110482967a5e94c89399a48896c9e8c8a3`

## nlu-step2-0798 · product_mention · train

의미 가족: `nlu-step2-two_products` / 표현 변형: 6

### 원문 raw

요즘 누리 로션 A 써요 / 다온 젤 C 구매 고려 중이에요 / 보습 후 느낌이 끈적해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 A 써요 / 다온 젤 C 구매 고려 중이에요 / 보습 후 느낌이 끈적해요",
  "topics": [
    "moisturizing",
    "other"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습 후 느낌이 끈적해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 C",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `340f291d229349201f190a5fd7defd154428c5bb6c8efaf0f8412c58c444ade4`

## nlu-step2-0799 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 0

### 원문 raw

보라 크림 B는 끊었어요. 다온 젤 CC 사볼까 해요. 2027년 8월이 사용기한이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 다온 젤 CC 사볼까 해요. 2027년 8월이 사용기한이에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `590235c5f97f9bb90f00fef25963810c321046a3b9fdebda654b0ec6516a4b70`

## nlu-step2-0800 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 1

### 원문 raw

보라 크림 B 사용 중단했어요, 다온 젤 CC 사볼까 해요, 2027년 8월이 사용기한이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요, 다온 젤 CC 사볼까 해요, 2027년 8월이 사용기한이에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c193048a1b0b6d5dcde551934dcd88a1964fc6fca09609ab72406033f4605674`

## nlu-step2-0801 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 2

### 원문 raw

보라 크림 B 이제 안 써요
다온 젤 CC 사볼까 해요
2027년 8월이 사용기한이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요\n다온 젤 CC 사볼까 해요\n2027년 8월이 사용기한이에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "2027년 8월이 사용기한이에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `e2103c7945d1476e1c3cb06126f9a9d0bbf9df908e80eb4e92b40332d3ef5065`

## nlu-step2-0802 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 3

### 원문 raw

보라 크림 B는 끊었어요. 다온 젤 CC 구매 고민 중이에요. 사용기한 표시 2027년 8월임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요. 다온 젤 CC 구매 고민 중이에요. 사용기한 표시 2027년 8월임",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `317b0e62110335471ed95cc07addb2df3d117587dcaa501ba8209608ab3653a8`

## nlu-step2-0803 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 4

### 원문 raw

보라 크림 B 사용 중단했어요 그리고 다온 젤 CC 구매 고민 중이에요 그리고 사용기한 표시 2027년 8월임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 사용 중단했어요 그리고 다온 젤 CC 구매 고민 중이에요 그리고 사용기한 표시 2027년 8월임",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `31a521a01c31bca54d6103fe38665a3393db4ea4f813472e8ec334ef90411bb8`

## nlu-step2-0804 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 5

### 원문 raw

보라 크림 B 이제 안 써요, 다온 젤 CC 구매 고민 중이에요, 사용기한 표시 2027년 8월임

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B 이제 안 써요, 다온 젤 CC 구매 고민 중이에요, 사용기한 표시 2027년 8월임",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한 표시 2027년 8월임"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `73871d1b20db760086a4f7a5cf3b6c1626c4863dae68eef85849de54e831560b`

## nlu-step2-0805 · product_mention · train

의미 가족: `nlu-step2-stopped_consider` / 표현 변형: 6

### 원문 raw

보라 크림 B는 끊었어요 / 다온 젤 CC 써볼까 생각해요 / 사용기한은 2027년 8월로 적혀요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "보라 크림 B는 끊었어요 / 다온 젤 CC 써볼까 생각해요 / 사용기한은 2027년 8월로 적혀요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.expiry",
      "value": "2027년 8월",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "사용기한은 2027년 8월로 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보라 크림 B",
      "usage_state": "stopped",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "다온 젤 CC",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5af7265aacfec717b5306741f07c2cd9d7d18f8fd6f13a51688aec572a5625c8`

## nlu-step2-0806 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 0

### 원문 raw

누리 로션 AB 쓰는 중이에요. 가온 크림 E 쓰는 중이에요. 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요. 가온 크림 E 쓰는 중이에요. 마지막에 물로 씻어내요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `3888b85c6af35fe930d81d095eda9fa84e6b6a2b29f07d06d6873ebf7a239e07`

## nlu-step2-0807 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 1

### 원문 raw

요즘 누리 로션 AB 써요, 가온 크림 E 쓰는 중이에요, 마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 AB 써요, 가온 크림 E 쓰는 중이에요, 마지막에 물로 씻어내요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `26786b2aa7f7fe3573e106d827dfb6b2bda248109ddfef77144b96bc02697681`

## nlu-step2-0808 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 2

### 원문 raw

누리 로션 AB 사용 중임
가온 크림 E 쓰는 중이에요
마지막에 물로 씻어내요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 사용 중임\n가온 크림 E 쓰는 중이에요\n마지막에 물로 씻어내요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마지막에 물로 씻어내요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `9836e04dc70908513ff589eda37fea563b20840e6daa9dcd7d49fcff5cdfb1c4`

## nlu-step2-0809 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 3

### 원문 raw

누리 로션 AB 쓰는 중이에요. 요즘 가온 크림 E 써요. 끝에는 물 헹굼 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요. 요즘 가온 크림 E 써요. 끝에는 물 헹굼 해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ee1825d38e710c40ac7dcb20ae7ffdcb60a70c27e292e2d681ccab38fc994c37`

## nlu-step2-0810 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 4

### 원문 raw

요즘 누리 로션 AB 써요 그리고 요즘 가온 크림 E 써요 그리고 끝에는 물 헹굼 해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "요즘 누리 로션 AB 써요 그리고 요즘 가온 크림 E 써요 그리고 끝에는 물 헹굼 해요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `f64912831667484592c3764d9799e5e96298a347cc9ab0c54c9d5bacb3159708`

## nlu-step2-0811 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 5

### 원문 raw

누리 로션 AB 사용 중임, 요즘 가온 크림 E 써요, 끝에는 물 헹굼 해여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 사용 중임, 요즘 가온 크림 E 써요, 끝에는 물 헹굼 해여",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끝에는 물 헹굼 해여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `4e1d816c923fa27f1300900820ceafe468c46481c0f43dc73591cffd1a59d4db`

## nlu-step2-0812 · product_mention · train

의미 가족: `nlu-step2-two_names` / 표현 변형: 6

### 원문 raw

누리 로션 AB 쓰는 중이에요 / 가온 크림 E 사용 중임 / 마무리는 물로 헹궈요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "누리 로션 AB 쓰는 중이에요 / 가온 크림 E 사용 중임 / 마무리는 물로 헹궈요",
  "topics": [
    "moisturizing",
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.rinse",
      "value": "물로 헹굼",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "마무리는 물로 헹궈요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 AB",
      "usage_state": "using",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `7fddd9e6c1927c45fa1f190b921fc46b74ce056fe45dd05410a090d3390b4e47`

## nlu-step2-0813 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 0

### 원문 raw

해솔 토너 D라는 이름 봤어요. 폼클렌저 쓰고 있어요. 수영했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요. 폼클렌저 쓰고 있어요. 수영했어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수영했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `8bd770d6eec98ca1106d9e4bc401104e7e515d7f9d0452e44dbaa7a13a99c0ab`

## nlu-step2-0814 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 1

### 원문 raw

해솔 토너 D 이름만 들었어요, 폼클렌저 쓰고 있어요, 수영했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D 이름만 들었어요, 폼클렌저 쓰고 있어요, 수영했어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수영했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `1664ac1378985e76ca145f9cf727e831fd22a408f021bbf08c1de549e490e613`

## nlu-step2-0815 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 2

### 원문 raw

해솔 토너 D라는 이름이 기억나요
폼클렌저 쓰고 있어요
수영했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름이 기억나요\n폼클렌저 쓰고 있어요\n수영했어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수영했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `2372939b223f50556aaf0b072060179f38317dc2cd227fe978ee1bd2247df9f6`

## nlu-step2-0816 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 3

### 원문 raw

해솔 토너 D라는 이름 봤어요. 요즘 폼클렌저 써요. 물놀이 했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요. 요즘 폼클렌저 써요. 물놀이 했어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물놀이 했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `8b0e9af181639dc619bda04387ffe8f9d0cdaa2c0940bb762828a71ce376d7ee`

## nlu-step2-0817 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 4

### 원문 raw

해솔 토너 D 이름만 들었어요 그리고 요즘 폼클렌저 써요 그리고 물놀이 했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D 이름만 들었어요 그리고 요즘 폼클렌저 써요 그리고 물놀이 했어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물놀이 했어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5a2cb5b210a1b0451d2e3fb39e3b47281ba9a82fad0dc7314a7f41737d60a11d`

## nlu-step2-0818 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 5

### 원문 raw

해솔 토너 D라는 이름이 기억나요, 요즘 폼클렌저 써요, 물놀이 했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름이 기억나요, 요즘 폼클렌저 써요, 물놀이 했어여",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물놀이 했어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `aedb25ae47f7063425bec5093b73fcfbf9a04375a878f856eb1e352940a3c807`

## nlu-step2-0819 · product_mention · train

의미 가족: `nlu-step2-unknown_generic` / 표현 변형: 6

### 원문 raw

해솔 토너 D라는 이름 봤어요 / 현재 폼클렌저 사용 중이에요 / 물에 들어갔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "해솔 토너 D라는 이름 봤어요 / 현재 폼클렌저 사용 중이에요 / 물에 들어갔어요",
  "topics": [
    "other",
    "cleansing_method",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.water_contact",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "물에 들어갔어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "폼클렌저",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `f027363d257c18503207a3f2735dfd300da1b8ae5b4e7718877200f1d3aecab1`

## nlu-step2-0820 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 0

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요. 작은 공병에 덜어뒀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요. 작은 공병에 덜어뒀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `42e81bc8e2c3dc88f8b29be9126cc0fdec3ee2caf4d3200fb5c73b208c933ce6`

## nlu-step2-0821 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 1

### 원문 raw

선크림 바르면 매번 눈따가움, 작은 공병에 덜어뒀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 바르면 매번 눈따가움, 작은 공병에 덜어뒀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5ff921ff185a60df63387c645a5207378764036b5cbc4698b42f00369cabecd3`

## nlu-step2-0822 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 2

### 원문 raw

선크림 쓸 때마다 눈이 따가워요
작은 공병에 덜어뒀어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓸 때마다 눈이 따가워요\n작은 공병에 덜어뒀어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병에 덜어뒀어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `5bbdbf52707da386431ab284592eec08e3ebc53ed0f757d88eea25920f6bf4f9`

## nlu-step2-0823 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 3

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요. 작은 공병으로 소분했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요. 작은 공병으로 소분했어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `506ea8e7a45469a07aa8fe4658206b6be41fdfc96a448ba4ec7ec6570c7646a5`

## nlu-step2-0824 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 4

### 원문 raw

선크림 바르면 매번 눈따가움 그리고 작은 공병으로 소분했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 바르면 매번 눈따가움 그리고 작은 공병으로 소분했어요",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 바르면 매번 눈따가움"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `77e4d76a9cba39869b07666393dcf0e7abe6064de79092a6b35e3cf6bb79185b`

## nlu-step2-0825 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 5

### 원문 raw

선크림 쓸 때마다 눈이 따가워요, 작은 공병으로 소분했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓸 때마다 눈이 따가워요, 작은 공병으로 소분했어여",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 공병으로 소분했어여"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓸 때마다 눈이 따가워요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `3f516c3a95aac9b1540daa6caa72698f82db6fe3a373bcc1b5cd2748b5591365`

## nlu-step2-0826 · product_mention · train

의미 가족: `nlu-step2-eye_product` / 표현 변형: 6

### 원문 raw

선크림 쓰고 나면 매번 눈이 시려요 / 작은 빈 병에 나눠 담음

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "선크림 쓰고 나면 매번 눈이 시려요 / 작은 빈 병에 나눠 담음",
  "topics": [
    "discomfort_report",
    "outdoor_sun",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림 사용 후",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    },
    {
      "variable_id": "storage.decanting",
      "value": "작은 공병으로 소분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "작은 빈 병에 나눠 담음"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "선크림 쓰고 나면 매번 눈이 시려요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `a3af3fb895eedc3b81b997628fe3d92edee321389681ec274035f8ad95a7eab0`

## nlu-step2-0827 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 요즘 누리 로션 A 써요. 가온 크림 E 쓰는 중이에요. 개봉 뒤 여섯 달이라고 써 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 요즘 누리 로션 A 써요. 가온 크림 E 쓰는 중이에요. 개봉 뒤 여섯 달이라고 써 있어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `94d5537f2561f2b6fa799564d85d7b80baaede2b59c78fcb458c071ccde1b681`

## nlu-step2-0828 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 누리 로션 A 쓰고 있어요, 가온 크림 E 쓰는 중이에요, 개봉 뒤 여섯 달이라고 써 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 누리 로션 A 쓰고 있어요, 가온 크림 E 쓰는 중이에요, 개봉 뒤 여섯 달이라고 써 있어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `abda6e5b27d5ea8e0e8f00e02500e285ab693180e27c1b8366f1967798e73829`

## nlu-step2-0829 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 현재 누리 로션 A 사용 중
가온 크림 E 쓰는 중이에요
개봉 뒤 여섯 달이라고 써 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 현재 누리 로션 A 사용 중\n가온 크림 E 쓰는 중이에요\n개봉 뒤 여섯 달이라고 써 있어요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 뒤 여섯 달이라고 써 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `98a84d6ca0c3ea74040ce99c8aa538b3e2bef46c1f744966e80cbe1f4b6c4106`

## nlu-step2-0830 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 요즘 누리 로션 A 써요. 요즘 가온 크림 E 써요. 열고 6개월 이내라고 적혀요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 요즘 누리 로션 A 써요. 요즘 가온 크림 E 써요. 열고 6개월 이내라고 적혀요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ce9b5aa72faa951a30c11e6572b18a36325f3bd18f56ed5d0db635e6e1f33512`

## nlu-step2-0831 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 누리 로션 A 쓰고 있어요 그리고 요즘 가온 크림 E 써요 그리고 열고 6개월 이내라고 적혀요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 누리 로션 A 쓰고 있어요 그리고 요즘 가온 크림 E 써요 그리고 열고 6개월 이내라고 적혀요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `ccfa0c1310db340089ebf9452105017269dba1919b2a8406d6bac593f8e96b06`

## nlu-step2-0832 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 현재 누리 로션 A 사용 중, 요즘 가온 크림 E 써요, 열고 6개월 이내라고 적혀요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 현재 누리 로션 A 사용 중, 요즘 가온 크림 E 써요, 열고 6개월 이내라고 적혀요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "열고 6개월 이내라고 적혀요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c737306575e2cae0a4883fee94d9dc6c8f165179c6b679cf61926b74052114d0`

## nlu-step2-0833 · product_mention · val_internal

의미 가족: `nlu-step2-other_product` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 요즘 누리 로션 A 써요 / 가온 크림 E 사용 중임 / 개봉 후 6개월 표시예요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 요즘 누리 로션 A 써요 / 가온 크림 E 사용 중임 / 개봉 후 6개월 표시예요",
  "topics": [
    "moisturizing",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.pao",
      "value": "개봉 후 6개월",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "개봉 후 6개월 표시예요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "누리 로션 A",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "가온 크림 E",
      "usage_state": "other_person",
      "matched_catalog_hint": "syn-catalog-gaon-e"
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `c3352b007a8e23ddaf994a545f61f94f2a832e4ac28482339a23f29fd14e5ddf`

## nlu-step2-0834 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 0

### 원문 raw

친구 얘기예요. 저녁에는 크림을 발라요. 해솔 토너 D라는 이름 봤어요. 안으로 물이 들어간 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁에는 크림을 발라요. 해솔 토너 D라는 이름 봤어요. 안으로 물이 들어간 건 아니에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "안으로 물이 들어간 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `d720c60f7e2ba8d13c7d496c84506f7c4b1b9f797d15c69d98b61c1738120daf`

## nlu-step2-0835 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 1

### 원문 raw

친구 얘기예요. 크림은 저녁에 써요, 해솔 토너 D라는 이름 봤어요, 안으로 물이 들어간 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 크림은 저녁에 써요, 해솔 토너 D라는 이름 봤어요, 안으로 물이 들어간 건 아니에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "안으로 물이 들어간 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `4bf86ab16dfc87f21725248b22f9d83385503dd46936eb8b23c0ae9b906237f5`

## nlu-step2-0836 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 2

### 원문 raw

친구 얘기예요. 저녁에 크림 바름
해솔 토너 D라는 이름 봤어요
안으로 물이 들어간 건 아니에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁에 크림 바름\n해솔 토너 D라는 이름 봤어요\n안으로 물이 들어간 건 아니에요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "안으로 물이 들어간 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `bdf0ec9ac7621e347b7079d2fe385b4c4325719ca6fea62d8f2594b2fe2cdf70`

## nlu-step2-0837 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 3

### 원문 raw

친구 얘기예요. 저녁에는 크림을 발라요. 해솔 토너 D 이름만 들었어요. 통 안 물 유입은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁에는 크림을 발라요. 해솔 토너 D 이름만 들었어요. 통 안 물 유입은 없어요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통 안 물 유입은 없어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `b1a0b981b419018af9b9f47a92e21e954cebe5f3165989579dd0af674d112c59`

## nlu-step2-0838 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 4

### 원문 raw

친구 얘기예요. 크림은 저녁에 써요 그리고 해솔 토너 D 이름만 들었어요 그리고 통 안 물 유입은 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 크림은 저녁에 써요 그리고 해솔 토너 D 이름만 들었어요 그리고 통 안 물 유입은 없어요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "크림은 저녁에 써요"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통 안 물 유입은 없어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `19be3006698cca850aedd7e8da6848bd5d886293ae79903a95fe1de5788450c5`

## nlu-step2-0839 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 5

### 원문 raw

친구 얘기예요. 저녁에 크림 바름, 해솔 토너 D 이름만 들었어여, 통 안 물 유입은 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁에 크림 바름, 해솔 토너 D 이름만 들었어여, 통 안 물 유입은 없어여",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁에 크림 바름"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "통 안 물 유입은 없어여"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `29c7f66fc4ec6159ac95dcaeabb8a69913b139ed0a1d8acdab6f2245f2d8f191`

## nlu-step2-0840 · product_mention · val_internal

의미 가족: `nlu-step2-other_new` / 표현 변형: 6

### 원문 raw

친구 얘기예요. 저녁에는 크림을 발라요 / 해솔 토너 D라는 이름이 기억나요 / 용기 안에 물은 안 들어갔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "친구 얘기예요. 저녁에는 크림을 발라요 / 해솔 토너 D라는 이름이 기억나요 / 용기 안에 물은 안 들어갔어요",
  "topics": [
    "moisturizing",
    "other",
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "저녁 크림 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "저녁에는 크림을 발라요"
    },
    {
      "variable_id": "storage.water_ingress",
      "value": true,
      "polarity": "denied",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "용기 안에 물은 안 들어갔어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    },
    {
      "raw_text": "해솔 토너 D",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.

내용 SHA-256: `9ad352d3d10ac9f12fb9c781dc60dc9f68bf4d56d015d6ad256422685aeb1b14`

## nlu-step2-0841 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 0

### 원문 raw

처음 뵙겠어요. 고맙네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요. 고맙네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `514b6b14d1a894201441b5ff429e96b51fbca5ed0b2cc9138b2ee5be00b87f84`

## nlu-step2-0842 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 1

### 원문 raw

반갑습니다, 고맙네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반갑습니다, 고맙네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d5da3fc6eb7d45205060b6288bac339b0687755c1523fe373aced095e2f7c3b0`

## nlu-step2-0843 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 2

### 원문 raw

인사드려요
고맙네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "인사드려요\n고맙네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `6ba6fbe83c7d44651476574f53f17977eb6f1e1f690ea6eab0cb86d226e0136c`

## nlu-step2-0844 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 3

### 원문 raw

처음 뵙겠어요. 정말 고마워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요. 정말 고마워요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e0677e3a0f7c5ae3e7412395b40aaa3ccd69744f24c735c8af6a0d486dd51c0c`

## nlu-step2-0845 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 4

### 원문 raw

반갑습니다 그리고 정말 고마워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반갑습니다 그리고 정말 고마워요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `b60b92a26e10a7c1aca969c9e2fcf2f2ba0d4b0fdee1f8b8e2926c4fc63776d9`

## nlu-step2-0846 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 5

### 원문 raw

인사드려요, 정말 고마워요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "인사드려요, 정말 고마워요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `31ad26afae7b10a470294fab3c817dc00aa93d11fb10735715a20649c8129d40`

## nlu-step2-0847 · no_signal_noise · train

의미 가족: `nlu-step2-noise_1` / 표현 변형: 6

### 원문 raw

처음 뵙겠어요 / 감사드려요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요 / 감사드려요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `616682c24869136899ee2108f637ab7cbcffd02df8990f169ba98e8b72d9c159`

## nlu-step2-0848 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 0

### 원문 raw

이만 갈게요. 말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요. 말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e3f3cac6fa592d1cee9b21e9583dfb7d2d034f524e1f8b16549109d21c71497e`

## nlu-step2-0849 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 1

### 원문 raw

나중에 다시 올게요, 말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "나중에 다시 올게요, 말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `cf1d78d016a0f87343ab0a47d2e5c6225af53f5bca54281f9d42e4a2462b6a12`

## nlu-step2-0850 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 2

### 원문 raw

다음에 봬요
말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다음에 봬요\n말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `88d0bc8bd1e275ebef37a7b4e373301f0a3bd6245321d6df27fb84991dec6088`

## nlu-step2-0851 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 3

### 원문 raw

이만 갈게요. 답장이 늦었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요. 답장이 늦었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f8dfc1adb1d3dc10a07e7670de97dc847e04ef2bf734546dbc631ec1b6e873dd`

## nlu-step2-0852 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 4

### 원문 raw

나중에 다시 올게요 그리고 답장이 늦었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "나중에 다시 올게요 그리고 답장이 늦었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f13b43737a05973984c94b9d5e93c883ecf2fa5c3ff5239e4d81728beb92b791`

## nlu-step2-0853 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 5

### 원문 raw

다음에 봬요, 답장이 늦었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다음에 봬요, 답장이 늦었어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0545683c2a62263416bf2ae247601425f6cb162d0d3ad5ff5fc321b61921fc40`

## nlu-step2-0854 · no_signal_noise · train

의미 가족: `nlu-step2-noise_2` / 표현 변형: 6

### 원문 raw

이만 갈게요 / 좀 늦게 왔네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요 / 좀 늦게 왔네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `268ac60072f9f10359decc4523bb0ecfe022bbb201f6b75c324b7913e29b05e5`

## nlu-step2-0855 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 0

### 원문 raw

음 그러니까. 말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까. 말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `2bca68da9aee94fde4a113a546dd5f1f356b8aa3e57814e70d9cfddc49c6a8fb`

## nlu-step2-0856 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 1

### 원문 raw

어 잠깐만요, 말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "어 잠깐만요, 말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `8347e3ea91e658c84b58699651e38a42877e502781d81682887587210de2b16d`

## nlu-step2-0857 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 2

### 원문 raw

흠 뭐였더라
말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흠 뭐였더라\n말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `21d0e3e1a56800ad2a19c9b6e08c705b89ad29f5f15fcea5009c17a2d14d5eeb`

## nlu-step2-0858 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 3

### 원문 raw

음 그러니까. 이야기 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까. 이야기 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ace7054e0e1a092ba1e4685da239b3c4108a72072e7d5a9e891798b983c73e92`

## nlu-step2-0859 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 4

### 원문 raw

어 잠깐만요 그리고 이야기 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "어 잠깐만요 그리고 이야기 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0e6c45789fc9365ae8c46cdea66ce88e6368da699abb933ad737233344decc9c`

## nlu-step2-0860 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 5

### 원문 raw

흠 뭐였더라, 이야기 들었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흠 뭐였더라, 이야기 들었어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `003b3670c163de266473b65c3c10fc6ee58e4375a275a6265c11612787c33c2b`

## nlu-step2-0861 · no_signal_noise · train

의미 가족: `nlu-step2-noise_3` / 표현 변형: 6

### 원문 raw

음 그러니까 / 내용 읽었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까 / 내용 읽었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9251754fda5513354a3e66cd24abf5c611977b6bf63fd49b341f86d8bf6dfff0`

## nlu-step2-0862 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 0

### 원문 raw

기차가 늦네요. 노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요. 노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `b2bb91842a27fc2d961c902ee399a615f0df371687a82d060b3cdac665ac2835`

## nlu-step2-0863 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 1

### 원문 raw

열차가 지연됐어요, 노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열차가 지연됐어요, 노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `338da7796cd306f3ab4d25b31eaafec31a2827c7c7e77d9c3ee80bd0778067e7`

## nlu-step2-0864 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 2

### 원문 raw

기차 기다리는 중이에요
노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차 기다리는 중이에요\n노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a062555ec36ee2994b25216f13fcc0b3b6b59da8a91e52cb26a44b8ecef72912`

## nlu-step2-0865 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 3

### 원문 raw

기차가 늦네요. 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요. 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `607556dc7df1153cfb28d58235a597a1c99f6e0956e6667aca2400afd329d0b3`

## nlu-step2-0866 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 4

### 원문 raw

열차가 지연됐어요 그리고 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열차가 지연됐어요 그리고 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ac6269c9d955bc7082ec965f8d60a8939d99f6e9a53b525d568c0170932e10ee`

## nlu-step2-0867 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 5

### 원문 raw

기차 기다리는 중이에요, 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차 기다리는 중이에요, 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d3212e4c1d9a1852e5f214e4bab676c257f566408aa8592eba43bf95d0c2362f`

## nlu-step2-0868 · no_signal_noise · train

의미 가족: `nlu-step2-noise_4` / 표현 변형: 6

### 원문 raw

기차가 늦네요 / 노래 재생했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요 / 노래 재생했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `7bdc12ae8d29fa47d00c414ec3a4a14c11a02c2a39e9feacce0d762fa3141cac`

## nlu-step2-0869 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 0

### 원문 raw

책 읽는 중이에요. 커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "책 읽는 중이에요. 커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0fe866d654ca157d9b35ce0302f859a640e6088d7608a03b3becbbac32e06727`

## nlu-step2-0870 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 1

### 원문 raw

책장을 넘겼어요, 커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "책장을 넘겼어요, 커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d6fbc37f1b7b912f054dc206b1b754dae254594d09d8ab86c5c30a55645a6cc7`

## nlu-step2-0871 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 2

### 원문 raw

독서하고 있어요
커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "독서하고 있어요\n커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a4df52fbaadf120c706067206e2dfb9aac7391922eea5174c284a116ef86114a`

## nlu-step2-0872 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 3

### 원문 raw

책 읽는 중이에요. 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "책 읽는 중이에요. 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ece69882d6cc5f00d12c2a4383262da71f0e82fe674816402d12b87e3c0cd88d`

## nlu-step2-0873 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 4

### 원문 raw

책장을 넘겼어요 그리고 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "책장을 넘겼어요 그리고 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `baccdd7f89373b9afaacfc4925de99d8312f25eadb150f36b83a118156923919`

## nlu-step2-0874 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 5

### 원문 raw

독서하고 있어여, 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "독서하고 있어여, 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `92c39f4ea5c358ff34707e6541fc0d61bb647f0c71e2ad15e6e6fea7d3d0d717`

## nlu-step2-0875 · no_signal_noise · train

의미 가족: `nlu-step2-noise_5` / 표현 변형: 6

### 원문 raw

책 읽는 중이에요 / 커피 마시고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "책 읽는 중이에요 / 커피 마시고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `865095bf717c7c9197f4e3aff2e626029ebceae7c673fbac18b1bd6aaea2e899`

## nlu-step2-0876 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 0

### 원문 raw

영화 봤어요. 점심 먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 봤어요. 점심 먹었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `aafa08d11a2361b88422de884491632827c581222065956c177d03fa61c3ab3c`

## nlu-step2-0877 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 1

### 원문 raw

영화 보고 왔어요, 점심 먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 보고 왔어요, 점심 먹었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `6deeac4af767c853da2343b85c5e987ca6d3fccc29cc9c247955a28a4da57d5f`

## nlu-step2-0878 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 2

### 원문 raw

영화 한 편 봄
점심 먹었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 한 편 봄\n점심 먹었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `bee79549cdf616fec077bf3ba465e592005e25ef930cac9fd8dc4afd863ca681`

## nlu-step2-0879 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 3

### 원문 raw

영화 봤어요. 점심 식사 했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 봤어요. 점심 식사 했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e64df57c2122905a7e8843a6d6f3433ac0e11be97edac6b899fb4a2e743d5374`

## nlu-step2-0880 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 4

### 원문 raw

영화 보고 왔어요 그리고 점심 식사 했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 보고 왔어요 그리고 점심 식사 했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `5d894cd93b243b1ca24b2a5894666a3c390d4b81bdd4122b24cae57296c77996`

## nlu-step2-0881 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 5

### 원문 raw

영화 한 편 봄, 점심 식사 했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 한 편 봄, 점심 식사 했어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `087ad09ef287004e77b185f01de96ef4f0e03ca315258f0793bab103b0014d11`

## nlu-step2-0882 · no_signal_noise · train

의미 가족: `nlu-step2-noise_6` / 표현 변형: 6

### 원문 raw

영화 봤어요 / 밥 먹고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "영화 봤어요 / 밥 먹고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `b3a0d6a0db6092e24e55072fbe2c7dc1a10f8c4eda47ae5d03fbceabd97a9b22`

## nlu-step2-0883 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 0

### 원문 raw

회의 끝났어요. 집에 도착했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의 끝났어요. 집에 도착했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `3e671c7bdfe90314b08b9916f8d3a02a7caaaef26478346d56402a1225cd551c`

## nlu-step2-0884 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 1

### 원문 raw

회의 마쳤어요, 집에 도착했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의 마쳤어요, 집에 도착했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `bfe2dacf5a7c87d6787480c371d192bcf27f9eca94a3cf4cd1096c16c97bd7ae`

## nlu-step2-0885 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 2

### 원문 raw

회의가 끝났네요
집에 도착했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의가 끝났네요\n집에 도착했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `5e474c8c357f47bbb1a1c159affb7fb989be71271bd9bc7ff59e552c3591173b`

## nlu-step2-0886 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 3

### 원문 raw

회의 끝났어요. 집에 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의 끝났어요. 집에 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d1732257123436ccb8659ed02a8d387bd6ee0058dbbd15902fc482bd59572e77`

## nlu-step2-0887 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 4

### 원문 raw

회의 마쳤어요 그리고 집에 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의 마쳤어요 그리고 집에 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `23a7ec45dec893d4d0d2cfac16f58a80ff4bddb606a4a8a429d85a65b2032ff3`

## nlu-step2-0888 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 5

### 원문 raw

회의가 끝났네요, 집에 왔어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의가 끝났네요, 집에 왔어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `45f157554dae64d1c2c2d80c04748469ce77b467a5df5219a4373c65ad8c0583`

## nlu-step2-0889 · no_signal_noise · train

의미 가족: `nlu-step2-noise_7` / 표현 변형: 6

### 원문 raw

회의 끝났어요 / 방금 귀가했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "회의 끝났어요 / 방금 귀가했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `3835457eed115df038fc0035f7e0fa598afe8b9ff99d005ca757768e9d4fc9bf`

## nlu-step2-0890 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 0

### 원문 raw

택배가 내일 온대요. 휴대폰 배터리가 없네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배가 내일 온대요. 휴대폰 배터리가 없네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `3cae11ae424c5817637e3e81ea71e52f46b70b8095947efa0227c558731ba4f9`

## nlu-step2-0891 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 1

### 원문 raw

내일 배송된대요, 휴대폰 배터리가 없네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "내일 배송된대요, 휴대폰 배터리가 없네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `467a6cdab089cc3f3afff416e1d0de3d523f55a6dee90f0bf124734544c150c5`

## nlu-step2-0892 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 2

### 원문 raw

택배 도착은 내일이래요
휴대폰 배터리가 없네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배 도착은 내일이래요\n휴대폰 배터리가 없네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c264b07e13a730c315dac82c22c4a1c71c075760d8efe423da33dd5edc6c185d`

## nlu-step2-0893 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 3

### 원문 raw

택배가 내일 온대요. 폰 배터리가 거의 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배가 내일 온대요. 폰 배터리가 거의 없어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `85af9e636b235e13d88bb97dee52a667d937031d1c63066f5fd715aec139da47`

## nlu-step2-0894 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 4

### 원문 raw

내일 배송된대요 그리고 폰 배터리가 거의 없어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "내일 배송된대요 그리고 폰 배터리가 거의 없어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ab7f469f017aa6835ef77fe66c502730f653f6702336014f48c0fc2abb16f459`

## nlu-step2-0895 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 5

### 원문 raw

택배 도착은 내일이래요, 폰 배터리가 거의 없어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배 도착은 내일이래요, 폰 배터리가 거의 없어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `073def67ef4095b17cc61ecd2d126ad0e6ecc290b85785de7e9bf7964f283cf2`

## nlu-step2-0896 · no_signal_noise · train

의미 가족: `nlu-step2-noise_8` / 표현 변형: 6

### 원문 raw

택배가 내일 온대요 / 휴대폰 충전이 필요해요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "택배가 내일 온대요 / 휴대폰 충전이 필요해요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `eb6bb36e47399b5d8200ac1e528dd94d799194b5706cc060e546bfece1a93ed6`

## nlu-step2-0897 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 0

### 원문 raw

게임 끝났어요. 표를 예매했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "게임 끝났어요. 표를 예매했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a7cdb9b61d75357b08b5c0948aa983eb980ed49bb824945ddc9b794af1b10cfe`

## nlu-step2-0898 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 1

### 원문 raw

게임 한 판 마쳤어요, 표를 예매했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "게임 한 판 마쳤어요, 표를 예매했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `1ceb49ff4e5b62bf76db80ab0cd655780930b94ff01714365c3c4b0c12256341`

## nlu-step2-0899 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 2

### 원문 raw

한 판 하고 왔어요
표를 예매했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "한 판 하고 왔어요\n표를 예매했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `de631c5d67f3c77279af8cc24c240f8097c192cc8607c154200b27e0274fe7f7`

## nlu-step2-0900 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 3

### 원문 raw

게임 끝났어요. 티켓 예약했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "게임 끝났어요. 티켓 예약했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `1a236c002ed9c06664ef4a03c79cf0b55bae60acbe2e09c4a2d108865002a29a`

## nlu-step2-0901 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 4

### 원문 raw

게임 한 판 마쳤어요 그리고 티켓 예약했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "게임 한 판 마쳤어요 그리고 티켓 예약했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `147222d9eb267a4c1f04af81f81f936f86015f3d4d889f715cd4f00f3177cf94`

## nlu-step2-0902 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 5

### 원문 raw

한 판 하고 왔어여, 티켓 예약했어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "한 판 하고 왔어여, 티켓 예약했어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `422223fe77e34767825b4fb68d1424bdc32ae00322bd598c58f07833e60bc094`

## nlu-step2-0903 · no_signal_noise · train

의미 가족: `nlu-step2-noise_9` / 표현 변형: 6

### 원문 raw

게임 끝났어요 / 예매 완료했네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "게임 끝났어요 / 예매 완료했네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `47d8a78d4ff88af3472c1f2dc3813b36e04275569231e7b1e40a2b652b88f7d4`

## nlu-step2-0904 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 0

### 원문 raw

풍경 사진 봤어요. 창밖이 시끄럽네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "풍경 사진 봤어요. 창밖이 시끄럽네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ef8535f86e88a0d68689806c83a4e66520c01aa9bccb958e5fb279b15faa0669`

## nlu-step2-0905 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 1

### 원문 raw

경치 사진 보고 왔어요, 창밖이 시끄럽네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "경치 사진 보고 왔어요, 창밖이 시끄럽네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `4655366ea4af96a9c93d7bc6cecfa7cc7624af82666beac6557e10f0ef39ff1d`

## nlu-step2-0906 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 2

### 원문 raw

풍경 사진을 구경했어요
창밖이 시끄럽네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "풍경 사진을 구경했어요\n창밖이 시끄럽네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `5f417b7170159a7242cc85ce37607bf708a3a2799e8e41194fbebc32b4eadf3a`

## nlu-step2-0907 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 3

### 원문 raw

풍경 사진 봤어요. 밖에서 소리가 나네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "풍경 사진 봤어요. 밖에서 소리가 나네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d0841ec632db7dc162662639a88ebf931e706e7079c4aa92ff72ef6dbf786e6b`

## nlu-step2-0908 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 4

### 원문 raw

경치 사진 보고 왔어요 그리고 밖에서 소리가 나네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "경치 사진 보고 왔어요 그리고 밖에서 소리가 나네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e9827061625d5ca68bee83a507501baf215c4bc4e8d81bce2d4258c59993dece`

## nlu-step2-0909 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 5

### 원문 raw

풍경 사진을 구경했어여, 밖에서 소리가 나네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "풍경 사진을 구경했어여, 밖에서 소리가 나네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `17643067fa719675de80064a9bf12ee72c939d922e5f00bc480943928d9ed040`

## nlu-step2-0910 · no_signal_noise · train

의미 가족: `nlu-step2-noise_10` / 표현 변형: 6

### 원문 raw

풍경 사진 봤어요 / 창밖 소음이 커요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "풍경 사진 봤어요 / 창밖 소음이 커요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `73cc9da5e2ce50ebd95d1ff68fda6456f43bae86a0715428ad1ba891b0a2f78f`

## nlu-step2-0911 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 0

### 원문 raw

처음 뵙겠어요. 책 읽는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요. 책 읽는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f4386aeee93d807ecf237a1e507263b0aadecf6da8f05efbef95bdd7395551f6`

## nlu-step2-0912 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 1

### 원문 raw

반갑습니다, 책 읽는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반갑습니다, 책 읽는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c42837088ff081a8acdb53010669187cfb0ef5990351e749f6b275bb2d570a57`

## nlu-step2-0913 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 2

### 원문 raw

인사드려요
책 읽는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "인사드려요\n책 읽는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `092ab1a4624ec2f2678d3f01a27978148a11012f05df8c7e7de784a531bf5fbe`

## nlu-step2-0914 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 3

### 원문 raw

처음 뵙겠어요. 책장을 넘겼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요. 책장을 넘겼어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `09d8b8d5252c894f56a7dbb3a75041d87df1d6ac76860caacb2ceb1dd499a9c7`

## nlu-step2-0915 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 4

### 원문 raw

반갑습니다 그리고 책장을 넘겼어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "반갑습니다 그리고 책장을 넘겼어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `37a4fd515aab945eb96d49c6ec24047abfc898be20608963535d21622b302b44`

## nlu-step2-0916 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 5

### 원문 raw

인사드려요, 책장을 넘겼어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "인사드려요, 책장을 넘겼어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0ce587c2017c0580461c2060f6b0b9ab5a763d8e07ffba3ff8f993374a76c067`

## nlu-step2-0917 · no_signal_noise · train

의미 가족: `nlu-step2-noise_11` / 표현 변형: 6

### 원문 raw

처음 뵙겠어요 / 독서하고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "처음 뵙겠어요 / 독서하고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d13e348ac034a2fbe50d40885994d088ce211619e59076228356daa802e31307`

## nlu-step2-0918 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 0

### 원문 raw

고맙네요. 회의 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "고맙네요. 회의 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9e7a3d7703f55564dbcce82def92f39fd269ccf387f9bd27f7ce5b0db8ed252a`

## nlu-step2-0919 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 1

### 원문 raw

정말 고마워요, 회의 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "정말 고마워요, 회의 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c60c03f9d44c5dae436a746d6e6fbf3620a97ca58d23a06271cb65f866fcb474`

## nlu-step2-0920 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 2

### 원문 raw

감사드려요
회의 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "감사드려요\n회의 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `5cc40f4eb85598fdfb71e62a8e4c5f01b1db1d41a1c07a36fb2e7b57fe73bec2`

## nlu-step2-0921 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 3

### 원문 raw

고맙네요. 회의 마쳤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "고맙네요. 회의 마쳤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `fa8f540d957a981668d953b41863544d94c50760abf67ea06a4125b641e0cf61`

## nlu-step2-0922 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 4

### 원문 raw

정말 고마워요 그리고 회의 마쳤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "정말 고마워요 그리고 회의 마쳤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `6e0824f8c89a8bb78fddf27e8887e685ab09544b61aa983f7c0ce1c046badcdb`

## nlu-step2-0923 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 5

### 원문 raw

감사드려요, 회의 마쳤어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "감사드려요, 회의 마쳤어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `68c455282cc80c2ce47431d1377b14931b68196d2b4471cf3bbf1b2c372c005d`

## nlu-step2-0924 · no_signal_noise · train

의미 가족: `nlu-step2-noise_12` / 표현 변형: 6

### 원문 raw

고맙네요 / 회의가 끝났네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "고맙네요 / 회의가 끝났네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `8fe263fb53e1770dbfe6ef677eef777b574b01a98af83d1bbaf59b56cca2b344`

## nlu-step2-0925 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 0

### 원문 raw

이만 갈게요. 영화 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요. 영화 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `b410e9e4ab751fa35d4f3ff4b7dc0ba8e7dc01a808da5f0788816b7397416d22`

## nlu-step2-0926 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 1

### 원문 raw

나중에 다시 올게요, 영화 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "나중에 다시 올게요, 영화 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `08bccc21bf92a366cf79613461b67b727e3e718b4bc5d954fdeb61ec617cae34`

## nlu-step2-0927 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 2

### 원문 raw

다음에 봬요
영화 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다음에 봬요\n영화 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ef274144898120d97c801b6e2979ce667395c04c2ae7b4810c9fd1244e80b4c1`

## nlu-step2-0928 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 3

### 원문 raw

이만 갈게요. 영화 보고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요. 영화 보고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f630aa5f5b200dc569bb01e46a85acbcfcd8f64fc615ae05eea3158d27eb06df`

## nlu-step2-0929 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 4

### 원문 raw

나중에 다시 올게요 그리고 영화 보고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "나중에 다시 올게요 그리고 영화 보고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c2f742e31eafdeeac303f36822435fb6ad869e4dc6dc6b842c012c2325d3fec3`

## nlu-step2-0930 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 5

### 원문 raw

다음에 봬요, 영화 보고 왔어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "다음에 봬요, 영화 보고 왔어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f57a7ee73c51e57e50430ef74b0d82bfb1e07fbbad861530f6b38fe0b2a88c73`

## nlu-step2-0931 · no_signal_noise · train

의미 가족: `nlu-step2-noise_13` / 표현 변형: 6

### 원문 raw

이만 갈게요 / 영화 한 편 봄

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "이만 갈게요 / 영화 한 편 봄",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `27d0ac6b5f12032782f253f95d0bb7442bca950b6c6934fb74fcd1dce33ed8f2`

## nlu-step2-0932 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 0

### 원문 raw

점심 먹었어요. 노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "점심 먹었어요. 노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `7b52949fa819b868da5ad853cc32fd864c9ee8ab99dd4246a9f0e0ef57f0c052`

## nlu-step2-0933 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 1

### 원문 raw

점심 식사 했어요, 노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "점심 식사 했어요, 노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `698f6d6aa0bbdc096eebcf00dede04abc962dbf9042305fe6a95dc9696db4738`

## nlu-step2-0934 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 2

### 원문 raw

밥 먹고 왔어요
노래 듣고 있어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "밥 먹고 왔어요\n노래 듣고 있어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `5ef85e8f2c0f397a73f11d34f3ca5284c9c0aacf1fb7227b1d1783c1d40365fe`

## nlu-step2-0935 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 3

### 원문 raw

점심 먹었어요. 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "점심 먹었어요. 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `59f700fb140eed89d8b2d2b50d492932c09dbc720684163c49b9bcc722059e8b`

## nlu-step2-0936 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 4

### 원문 raw

점심 식사 했어요 그리고 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "점심 식사 했어요 그리고 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d1a25bbdfc57e9495680d3b3fadb74b41bc00cd49c2013d7abbed8d10599360b`

## nlu-step2-0937 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 5

### 원문 raw

밥 먹고 왔어여, 음악 듣는 중이에요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "밥 먹고 왔어여, 음악 듣는 중이에요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `83f80d9d1639f6e20f5ca1ca6cddff35151fd459633e4e58c5e2d71f614a9549`

## nlu-step2-0938 · no_signal_noise · train

의미 가족: `nlu-step2-noise_14` / 표현 변형: 6

### 원문 raw

점심 먹었어요 / 노래 재생했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "점심 먹었어요 / 노래 재생했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `7093095bd5598cc150248f5d1260bc55f1fef9b07dd253f35211c7bb4b8d1ffa`

## nlu-step2-0939 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 0

### 원문 raw

기차가 늦네요. 커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요. 커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `3f536a4cb49ee543661843c2b2ab2dca0174378da2edcec9e5e4cf0b12e79cf2`

## nlu-step2-0940 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 1

### 원문 raw

열차가 지연됐어요, 커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열차가 지연됐어요, 커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `de173cc065b3caeb49fcdb81f69cc058c8abe80042df5774162779b50bc68315`

## nlu-step2-0941 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 2

### 원문 raw

기차 기다리는 중이에요
커피 마셨어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차 기다리는 중이에요\n커피 마셨어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `7354aa4790f657d0b5649eb51c48abced16e7a2b45b01b8b15c2a41df06ca1bb`

## nlu-step2-0942 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 3

### 원문 raw

기차가 늦네요. 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요. 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `139484a7461de8788cc6823a08975d64dd23243eeb19b335ccc8f7adb2735150`

## nlu-step2-0943 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 4

### 원문 raw

열차가 지연됐어요 그리고 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "열차가 지연됐어요 그리고 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `db46814da5d3e6b1f8ade49a1d3eb6f08d91b5db36995b0ce8bc308461eb8b89`

## nlu-step2-0944 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 5

### 원문 raw

기차 기다리는 중이에요, 커피 한 잔 마심

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차 기다리는 중이에요, 커피 한 잔 마심",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `922e9f4db0138c494de437c9184b3f2aefa562ef6c1955086726c62cf25aac23`

## nlu-step2-0945 · no_signal_noise · train

의미 가족: `nlu-step2-noise_15` / 표현 변형: 6

### 원문 raw

기차가 늦네요 / 커피 마시고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "기차가 늦네요 / 커피 마시고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0d71ff15d99dc2bb57ff18e2ef26f43dc0545c9f0d4dbc065f77389920ee06ff`

## nlu-step2-0946 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 0

### 원문 raw

집에 도착했어요. 게임 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "집에 도착했어요. 게임 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9e1f14b71256faf250876d34f32954f8885d83bde017ceaeb294fb2c63de0c64`

## nlu-step2-0947 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 1

### 원문 raw

집에 왔어요, 게임 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "집에 왔어요, 게임 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `2d891362ed2da561e6a35ee224c0224f3790c255d99e58e0e5baf866472fd3a6`

## nlu-step2-0948 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 2

### 원문 raw

방금 귀가했어요
게임 끝났어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 귀가했어요\n게임 끝났어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `29a606c381b38e487d9912d59a0a7c7ed6682075519862a38dd894f82546c350`

## nlu-step2-0949 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 3

### 원문 raw

집에 도착했어요. 게임 한 판 마쳤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "집에 도착했어요. 게임 한 판 마쳤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `d5274dfdde6ce22a940118deaeceee16d2fca9e1212193c24cfd2010497fd350`

## nlu-step2-0950 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 4

### 원문 raw

집에 왔어요 그리고 게임 한 판 마쳤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "집에 왔어요 그리고 게임 한 판 마쳤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `f914987bc9fc3502806170a8ae936193f44bf7885e6826386c920822770dd669`

## nlu-step2-0951 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 5

### 원문 raw

방금 귀가했어여, 게임 한 판 마쳤어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 귀가했어여, 게임 한 판 마쳤어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c9416956ea211d0a220aa7ac1876a35688c8319d76bdbeac231e010a3536206b`

## nlu-step2-0952 · no_signal_noise · train

의미 가족: `nlu-step2-noise_16` / 표현 변형: 6

### 원문 raw

집에 도착했어요 / 한 판 하고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "집에 도착했어요 / 한 판 하고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `62be9abb601b7e25b177ce23d46a881d7dce0b010612d44d1ed872a65012a721`

## nlu-step2-0953 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 0

### 원문 raw

표를 예매했어요. 풍경 사진 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표를 예매했어요. 풍경 사진 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `06a6d663edba10b87d3da9a772a0453fb07825124a38473c63473df6693fa5af`

## nlu-step2-0954 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 1

### 원문 raw

티켓 예약했어요, 풍경 사진 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "티켓 예약했어요, 풍경 사진 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0c8d91b0438d7045665a66a4806e425cfa0bdc009f27d8b881eed0f2f38a73fa`

## nlu-step2-0955 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 2

### 원문 raw

예매 완료했네요
풍경 사진 봤어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "예매 완료했네요\n풍경 사진 봤어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `8d497f456b8d4a30e4c749f48ca6cfd3d910d144bc9038bd4108c14174133ea8`

## nlu-step2-0956 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 3

### 원문 raw

표를 예매했어요. 경치 사진 보고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표를 예매했어요. 경치 사진 보고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `ec2d3081a8e0cbe4c5745479e4db6b77ebf1ce3e8b68087865af6830aa74fdb3`

## nlu-step2-0957 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 4

### 원문 raw

티켓 예약했어요 그리고 경치 사진 보고 왔어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "티켓 예약했어요 그리고 경치 사진 보고 왔어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0d92cb27c5f442312107cc39674722db73a121f15dcd5f86dc00917cc3e7703f`

## nlu-step2-0958 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 5

### 원문 raw

예매 완료했네요, 경치 사진 보고 왔어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "예매 완료했네요, 경치 사진 보고 왔어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a4f2996eba7ecba340a1a1531c14a330d072614421acdca27341a2d6ace51cab`

## nlu-step2-0959 · no_signal_noise · train

의미 가족: `nlu-step2-noise_17` / 표현 변형: 6

### 원문 raw

표를 예매했어요 / 풍경 사진을 구경했어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "표를 예매했어요 / 풍경 사진을 구경했어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9f048ca8c1ae68d80b9b956e86ea4315acbc8d29efa23cf420e037e0342058c4`

## nlu-step2-0960 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 0

### 원문 raw

음 그러니까. 택배가 내일 온대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까. 택배가 내일 온대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e8667ce4767bd984a21bd0c99e4ad21a2fd599a81b4ce355177dc8bb6547c92a`

## nlu-step2-0961 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 1

### 원문 raw

어 잠깐만요, 택배가 내일 온대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "어 잠깐만요, 택배가 내일 온대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9e0ffbd4f6c3f39d238e52317b570bd65bf0f78d73ae2148b99cbc12d84234a7`

## nlu-step2-0962 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 2

### 원문 raw

흠 뭐였더라
택배가 내일 온대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흠 뭐였더라\n택배가 내일 온대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9193d26123c5d62d543c561e66f09d68ed36a0b4e33e3c78f8bb88083a30dc08`

## nlu-step2-0963 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 3

### 원문 raw

음 그러니까. 내일 배송된대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까. 내일 배송된대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a192dd2071389e183cb186950e4f67507efc09486f33d7e67ed121076451d8c6`

## nlu-step2-0964 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 4

### 원문 raw

어 잠깐만요 그리고 내일 배송된대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "어 잠깐만요 그리고 내일 배송된대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `208a9c7eabee8d20b44e3f8f9a6755288980014f60a2500d08f7f4ce5867c824`

## nlu-step2-0965 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 5

### 원문 raw

흠 뭐였더라, 내일 배송된대요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "흠 뭐였더라, 내일 배송된대요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `60933403b1d46b671d91454de5a54c1e310b9d3a807c569e5740d78a413b49ba`

## nlu-step2-0966 · no_signal_noise · train

의미 가족: `nlu-step2-noise_18` / 표현 변형: 6

### 원문 raw

음 그러니까 / 택배 도착은 내일이래요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "음 그러니까 / 택배 도착은 내일이래요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `89a33a48e69c32d8ea36aa040e37e22fe71f02704d2a220c7f76a5619a9bb549`

## nlu-step2-0967 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 0

### 원문 raw

키보드가 안 눌려요. 말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드가 안 눌려요. 말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `b84ed3a5b39f841a76c41a7a48406d4e981b66e6f88f8041c852880bae9bb074`

## nlu-step2-0968 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 1

### 원문 raw

키보드 한 키가 안 먹어요, 말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드 한 키가 안 먹어요, 말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `00552e2bad112440910f173db8ab4c97b2126fed583dedf0dd07e7969bb3e718`

## nlu-step2-0969 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 2

### 원문 raw

키보드 고장났네요
말씀 잘 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드 고장났네요\n말씀 잘 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `1edf2728b9587719a767a6e977bf0d5cd9462cdf50b20c8c8f08f9e3397e2ec4`

## nlu-step2-0970 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 3

### 원문 raw

키보드가 안 눌려요. 이야기 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드가 안 눌려요. 이야기 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `749ae0bf98e6824c0733c99136d02557cb5458ef9194157c7de8b2dc50f6f32d`

## nlu-step2-0971 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 4

### 원문 raw

키보드 한 키가 안 먹어요 그리고 이야기 들었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드 한 키가 안 먹어요 그리고 이야기 들었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `a2ae32346cec068f6ebbc71e1d5b0583629c7999f088b56237fad448eb7c5343`

## nlu-step2-0972 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 5

### 원문 raw

키보드 고장났네요, 이야기 들었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드 고장났네요, 이야기 들었어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `1b76e5c1286295938cb677ce346df464f4f7bad379030cf318bfb8aec0f01a57`

## nlu-step2-0973 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_19` / 표현 변형: 6

### 원문 raw

키보드가 안 눌려요 / 내용 읽었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "키보드가 안 눌려요 / 내용 읽었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `e594e0f79e98e8c20f719aea09f27ecb67df12cf81e2eb5a9de6976a03fceb24`

## nlu-step2-0974 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 0

### 원문 raw

벽시계가 멈췄어요. 말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계가 멈췄어요. 말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `20584db5b4e8b58ab7d4eed65c7c42c542c445c5e98b7c97f1a9fab8beb755af`

## nlu-step2-0975 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 1

### 원문 raw

시계가 안 가네요, 말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "시계가 안 가네요, 말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `0193cce9bbf0fbe5d2351843692d5f0eb627312a1752061fbcc16590711eafb0`

## nlu-step2-0976 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 2

### 원문 raw

벽시계 고장났네요
말이 늦었네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계 고장났네요\n말이 늦었네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `17e799abc12a096706db99a456752abb6bc001814c5a508eadd0224cde6060e6`

## nlu-step2-0977 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 3

### 원문 raw

벽시계가 멈췄어요. 답장이 늦었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계가 멈췄어요. 답장이 늦었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `9f577540982975e0f2a329fe774a474fbaa78db5dfd3972d86fe0eab9aade984`

## nlu-step2-0978 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 4

### 원문 raw

시계가 안 가네요 그리고 답장이 늦었어요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "시계가 안 가네요 그리고 답장이 늦었어요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `91b1d6a92a083ad515be7591542ecb3e88802b0f6e2e50b1936efdbf13836f14`

## nlu-step2-0979 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 5

### 원문 raw

벽시계 고장났네요, 답장이 늦었어여

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계 고장났네요, 답장이 늦었어여",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `c5d0989169379763681118b33506dc176897b7a1a0e8333d7004796a6b89a4d1`

## nlu-step2-0980 · no_signal_noise · val_internal

의미 가족: `nlu-step2-noise_20` / 표현 변형: 6

### 원문 raw

벽시계가 멈췄어요 / 좀 늦게 왔네요

직전 질문: None
질문 대상: None

### 예상 JSON raw

```json
{
  "schema_version": "v3.0",
  "source_text": "벽시계가 멈췄어요 / 좀 늦게 왔네요",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 작성 근거 (외부 검수 결과 아님)

피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.

내용 SHA-256: `486eb58193ca464b9d47f8b23626e7443d4bedfc57685aeb3eab79087ff64923`
