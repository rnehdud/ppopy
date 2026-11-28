# NLU 파일럿 49건 — 원문·예상 후보·작성 근거

합성 작성본이며 독립 Critic·사람 검수·Base 모델 측정 결과가 아니에요.

## nlu-pilot-0001 · turn1_utterance · train

가족: `nlu-v1-wash_temperature`

### 실제 자유 발화

얼굴은 손으로 미지근한 물에 씻고, 보습제는 세안하고 5분 뒤에 발라요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "얼굴은 손으로 미지근한 물에 씻고, 보습제는 세안하고 5분 뒤에 발라요.",
  "topics": [
    "cleansing_method",
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "얼굴은"
    },
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손으로"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근한 물에"
    },
    {
      "variable_id": "moisturizing.after_wash_delay",
      "value": "5분",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세안하고 5분 뒤에"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보습제",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

부위·도구·물 온도·보습 간격은 각각 원문에 있어요. 5분은 단위까지 보존하고 효과는 추론하지 않아요.

내용 SHA-256: `1c77bc81a7ccc1507deb3677990581ff2e6c0e2068cd3681d1c0394173610f2c`

## nlu-pilot-0002 · turn1_utterance · train

가족: `nlu-v1-removal_steps`

### 실제 자유 발화

워터프루프 선크림을 바른 날에는 그 이유만으로 무조건 두 번 연달아 세안해요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "워터프루프 선크림을 바른 날에는 그 이유만으로 무조건 두 번 연달아 세안해요.",
  "topics": [
    "repeat_cleansing"
  ],
  "slot_candidates": [
    {
      "variable_id": "cleansing.steps",
      "value": "repeated_only_because_water_resistant",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "그 이유만으로 무조건 두 번 연달아 세안해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "워터프루프 선크림",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

B-I01의 원인 조건인 내수성만을 이유로 한 반복을 표준 문자열로 옮겨요. 제품의 실제 내수성 검증이나 변경 권고는 하지 않아요.

내용 SHA-256: `81725ccaacf69f6b028279a9b92ed66151f290eb68793a9b9fc0a6d550f9ecaa`

## nlu-pilot-0003 · turn1_utterance · train

가족: `nlu-v1-outdoor_water_sweat`

### 실제 자유 발화

수영하고 나와서 땀도 많이 났고, 모자는 쓰고 있었어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "수영하고 나와서 땀도 많이 났고, 모자는 쓰고 있었어요.",
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
      "evidence_span": "수영하고 나와서"
    },
    {
      "variable_id": "sun.sweat",
      "value": "yes",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "땀도 많이 났고"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "모자 착용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "모자는 쓰고 있었어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

물 접촉·발한·모자는 별도 후보예요. 재도포 필요성이나 보호 성능을 판단하지 않아요.

내용 SHA-256: `69d6b6c082583eea3f2936888321e2931e34537a2510702e2ab954a15798c929`

## nlu-pilot-0004 · turn1_utterance · train

가족: `nlu-v1-moisture_sensation_delay`

### 실제 자유 발화

로션을 바를 때마다 끈적하고, 매번 두 시간쯤 지나면 다시 건조해져요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "로션을 바를 때마다 끈적하고, 매번 두 시간쯤 지나면 다시 건조해져요.",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.comfort",
      "value": "끈적함",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "끈적하고"
    },
    {
      "variable_id": "moisturizing.dryness_return",
      "value": "두 시간쯤",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "매번 두 시간쯤 지나면 다시 건조해져요"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "매번 두 시간쯤 지나면 다시 건조해져요"
    }
  ],
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

### 원문과 판단의 연결

반복 조건과 대략적 시간은 보존해요. 건조감의 반복과 제품 효능·성분 사실은 구분해요.

내용 SHA-256: `011ea66a4abfcc7b39e7f14b0dd7f9019cd00982ab49072b8823093b3be3fa23`

## nlu-pilot-0005 · turn1_utterance · train

가족: `nlu-v1-storage_light_opened`

### 실제 자유 발화

이 크림은 지난주 토요일에 열었고 욕실 창가에 두고 쓰고 있어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "이 크림은 지난주 토요일에 열었고 욕실 창가에 두고 쓰고 있어요.",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.opened_at",
      "value": "지난주 토요일",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "지난주 토요일에 열었고"
    },
    {
      "variable_id": "storage.light_air",
      "value": "욕실 창가 보관",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "욕실 창가에 두고"
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

### 원문과 판단의 연결

상대 날짜를 실제 달력 날짜로 만들지 않고 보관 위치만 추출해요. 고온·변질·사용기한을 추정하지 않아요.

내용 SHA-256: `c27c30bbee3c197dbe9dada52473d805cb235c74624c92328d806e841ffcac78`

## nlu-pilot-0006 · turn1_utterance · train

가족: `nlu-v1-wash_touch_mechanics`

### 실제 자유 발화

세안할 때 브러시로 세게 문지르고 수건으로도 박박 비벼 닦아요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "세안할 때 브러시로 세게 문지르고 수건으로도 박박 비벼 닦아요.",
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
      "evidence_span": "브러시로"
    },
    {
      "variable_id": "method.friction",
      "value": "strong",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "세게 문지르고"
    },
    {
      "variable_id": "method.drying",
      "value": "rubbing_strongly",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "수건으로도 박박 비벼 닦아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

도구·마찰·물기 마무리를 분리하고 피부 손상이나 증상을 덧붙이지 않아요.

내용 SHA-256: `7ecb86afc6d0c12771812b65ae452d78a4aa61b118dc5c01d723ec2984c13eb0`

## nlu-pilot-0007 · turn1_utterance · train

가족: `nlu-v1-routine_order`

### 실제 자유 발화

저녁에는 보습제를 먼저 바르고 그다음 차단제를 발라요. 이 순서가 맞는지 궁금해요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "저녁에는 보습제를 먼저 바르고 그다음 차단제를 발라요. 이 순서가 맞는지 궁금해요.",
  "topics": [
    "routine_conflict",
    "moisturizing",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.sequence",
      "value": "보습제 다음 차단제",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "보습제를 먼저 바르고 그다음 차단제를 발라요"
    },
    {
      "variable_id": "method.current_routine",
      "value": "저녁 보습제 후 차단제 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저녁에는 보습제를 먼저 바르고 그다음 차단제를 발라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "보습제",
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

### 원문과 판단의 연결

질문의 정답을 설명하지 않고 실제 보고한 순서(method.sequence)와 시간대('저녁에는')가 명시된 사용 루틴(method.current_routine)을 함께 후보로 남겨요.

내용 SHA-256: `20b1cc60f3d4296c82b1dbc0ecb1011e604e58c8e76a8b321214b57ef9ef9607`

## nlu-pilot-0008 · turn2_followup · train

가족: `nlu-v1-wash_temperature`

### 실제 자유 발화

뜨겁지는 않고 미지근해요.

직전 질문: 세안할 때 물 온도는 어떤가요?
대상 슬롯: method.water_temperature

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨겁지는 않고 미지근해요.",
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
      "evidence_span": "뜨겁지는 않고"
    },
    {
      "variable_id": "method.water_temperature",
      "value": "lukewarm",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "미지근해요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

직전 질문으로 물 온도를 해석하되 부정된 hot과 명시된 lukewarm을 구분해요.

내용 SHA-256: `59093c6fa6ece7ea7b2105a5d973784c7bc1f5113d1b25f4612df9f85adcfda0`

## nlu-pilot-0009 · turn2_followup · train

가족: `nlu-v1-removal_steps`

### 실제 자유 발화

한 번만 해요.

직전 질문: 한 번 씻을 때 세정 단계를 몇 번 거치나요?
대상 슬롯: cleansing.steps

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "한 번만 해요.",
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

### 원문과 판단의 연결

질문에 대한 순수 횟수 응답 1을 정수로 추출해요. 표시 준수 심볼(according_to_product_removal_instructions)과 모호하게 겹치지 않도록 분리하고 제품 자체의 제거 성능은 만들지 않아요.

내용 SHA-256: `60020ca5cb404ee78484f5d1c4716168ebdfc26322fd574c368d1fae46a1453b`

## nlu-pilot-0010 · turn2_followup · train

가족: `nlu-v1-moisturizer_site`

### 실제 자유 발화

팔에는 바르는데 다리에는 안 발라요.

직전 질문: 보습제를 어느 부위에 바르나요?
대상 슬롯: moisturizing.coverage

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "팔에는 바르는데 다리에는 안 발라요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "moisturizing.coverage",
      "value": [
        "팔"
      ],
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "팔에는 바르는데"
    },
    {
      "variable_id": "moisturizing.coverage",
      "value": [
        "다리"
      ],
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "다리에는 안 발라요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

같은 질문의 부위별 긍정·부정을 나눠요. 다른 부위까지 사용 여부를 채우지 않아요.

내용 SHA-256: `28f7f7be7ca59d47d938e277b4cba251f74d11d1485c3a223a1e7701f62a5463`

## nlu-pilot-0011 · turn2_followup · train

가족: `nlu-v1-outdoor_duration`

### 실제 자유 발화

점심부터 해 질 때까지 계속 밖에 있어요.

직전 질문: 야외에 머무는 시간은 어느 정도인가요?
대상 슬롯: sun.outdoor_time

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "점심부터 해 질 때까지 계속 밖에 있어요.",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "점심부터 해 질 때까지 계속 밖에 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

장시간 야외라는 범주만 옮기며 지역별 일몰시각이나 숫자 시간을 추정하지 않아요.

내용 SHA-256: `06fe841bd5ef40e0f2bb65d776375bdaa7f261df430079e6ffa42c32d4c90289`

## nlu-pilot-0012 · turn2_followup · train

가족: `nlu-v1-opened_date_unknown`

### 실제 자유 발화

언제 열었는지는 기억이 안 나요.

직전 질문: 지금 쓰는 제품은 언제 개봉했나요?
대상 슬롯: storage.opened_at

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "언제 열었는지는 기억이 안 나요.",
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
      "evidence_span": "언제 열었는지는 기억이 안 나요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

개봉일 미상을 null로 보존해요. 구매일이나 오늘 날짜로 대체하지 않아요.

내용 SHA-256: `081accf6f05cd6fd1bbbeb1cac0a8a784deff5868ed21454d47d320e65987869`

## nlu-pilot-0013 · turn2_followup · train

가족: `nlu-v1-wash_touch_mechanics`

### 실제 자유 발화

손이 아니라 스펀지로 씻어요.

직전 질문: 피부를 씻을 때 어떤 도구를 사용하나요?
대상 슬롯: method.tools

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "손이 아니라 스펀지로 씻어요.",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.tools",
      "value": "hands",
      "polarity": "denied",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "손이 아니라"
    },
    {
      "variable_id": "method.tools",
      "value": "sponge",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "스펀지로 씻어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

도구의 명시적 정정만 반영하고 스펀지의 청결도·강도를 추론하지 않아요.

내용 SHA-256: `b2a44d6786d22091c9c86c61e33390aa8302a4c3db7eef97c295b3e352bd3fcd`

## nlu-pilot-0014 · turn2_followup · train

가족: `nlu-v1-eye_stinging_context`

### 실제 자유 발화

한 번이 아니라 씻을 때마다 눈이 시려요.

직전 질문: 눈이 시린 증상은 한 번 있었나요, 반복되나요?
대상 슬롯: skin.eye_symptom_context

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "한 번이 아니라 씻을 때마다 눈이 시려요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "씻을 때마다",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "씻을 때마다"
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
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

반복되는 눈 시림(eye_stinging)과 발화에 명시된 발생 상황('씻을 때마다', skin.eye_symptom_context)을 함께 추출해요. 눈에 제품이 직접 들어갔다거나 눈 질환이라고 단정하지 않아요.

내용 SHA-256: `7016235d71edad7acd14707bd6fb224688a40da3f2ece1c574465da404c05610`

## nlu-pilot-0015 · denied_polarity · train

가족: `nlu-v1-wash_temperature`

### 실제 자유 발화

뜨거운 물로 씻지 않아요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "뜨거운 물로 씻지 않아요.",
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
      "evidence_span": "뜨거운 물로 씻지 않아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

hot을 부정할 뿐 cold 또는 lukewarm을 긍정하지 않아요.

내용 SHA-256: `d4aee2239cf05fa4f9e569f61eb885059482267eaea68206a72a84b2676fd7c1`

## nlu-pilot-0016 · denied_polarity · train

가족: `nlu-v1-wash_touch_mechanics`

### 실제 자유 발화

브러시는 안 써요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "브러시는 안 써요.",
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
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

브러시 미사용만 추출하며 손이나 수건을 쓴다고 채우지 않아요.

내용 SHA-256: `e83beeca3f775621ac95195ff468418315a1db73d6c75c5be4448a2946b40a83`

## nlu-pilot-0017 · denied_polarity · train

가족: `nlu-v1-wash_touch_mechanics`

### 실제 자유 발화

세게 문지르는 건 아니에요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "세게 문지르는 건 아니에요.",
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
      "evidence_span": "세게 문지르는 건 아니에요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

강한 마찰 부정을 gentle의 실제 확인으로 바꾸지 않아요.

내용 SHA-256: `8a16d8faeb84e6fe3960bfae667d18974ab58af3518643dde18c39dd3c693c79`

## nlu-pilot-0018 · denied_polarity · train

가족: `nlu-v1-wash_touch_mechanics`

### 실제 자유 발화

수건으로 박박 비비지는 않아요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "수건으로 박박 비비지는 않아요.",
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
      "evidence_span": "수건으로 박박 비비지는 않아요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

강하게 닦기 부정을 pat_gently 확인으로 바꾸지 않아요.

내용 SHA-256: `95ed91ad07156e9ae6a57770e41653a6c46d0e4b289ac30301d4d65767e4212d`

## nlu-pilot-0019 · denied_polarity · train

가족: `nlu-v1-outdoor_water_sweat`

### 실제 자유 발화

오늘 야외에서는 물에 닿지 않았어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "오늘 야외에서는 물에 닿지 않았어요.",
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
      "evidence_span": "물에 닿지 않았어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

물 접촉 yes 명제를 부정해요. 다른 시간대의 접촉 이력은 만들지 않아요.

내용 SHA-256: `1fbb7ceceb593d0708a80b7b9cf0e0243ba2d56b61862d1bf68fc5e9570c6272`

## nlu-pilot-0020 · denied_polarity · train

가족: `nlu-v1-outdoor_water_sweat`

### 실제 자유 발화

운동했지만 땀은 나지 않았어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "운동했지만 땀은 나지 않았어요.",
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
      "evidence_span": "땀은 나지 않았어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

운동을 발한으로 자동 변환하지 않고 명시적 부정을 유지해요.

내용 SHA-256: `9d98a9a1c6331c4270bfcaf2ad78e8913c3790dd7d26cd873b77d4f0451eaece`

## nlu-pilot-0021 · denied_polarity · train

가족: `nlu-v1-symptom_negation`

### 실제 자유 발화

따갑거나 가렵지 않아요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "따갑거나 가렵지 않아요.",
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
      "evidence_span": "따갑거나 가렵지 않아요"
    },
    {
      "symptom": "itching",
      "polarity": "denied",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "따갑거나 가렵지 않아요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

두 증상의 부정을 추출하고 모든 불편이 없다고 넓히지 않아요.

내용 SHA-256: `eed03ccd8d040f36a45d92005a7f7f2d142e269aceb87f2f60227c0ce1615db1`

## nlu-pilot-0022 · other_subject · train

가족: `nlu-v1-wash_temperature`

### 실제 자유 발화

동생은 찬물로 얼굴을 씻는대요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "동생은 찬물로 얼굴을 씻는대요.",
  "topics": [
    "cleansing_method"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.water_temperature",
      "value": "cold",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "동생은 찬물로 얼굴을 씻는대요"
    },
    {
      "variable_id": "method.body_site",
      "value": "face",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "동생은 찬물로 얼굴을 씻는대요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

물 온도와 얼굴 부위의 주어를 모두 other로 유지해요.

내용 SHA-256: `7723a8e1a5f5af1fbd16f38e4377d1e65261632adb29be1fb9a9d329aa315dea`

## nlu-pilot-0023 · other_subject · train

가족: `nlu-v1-other_lotion_itch`

### 실제 자유 발화

친구가 로션 B를 바른 뒤 어제부터 가렵다고 해요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "친구가 로션 B를 바른 뒤 어제부터 가렵다고 해요.",
  "topics": [
    "moisturizing",
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "recent",
      "evidence_span": "친구가 로션 B를 바른 뒤 어제부터 가렵다고 해요"
    }
  ],
  "product_mentions": [
    {
      "raw_text": "로션 B",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

친구의 최근 가려움과 제품 언급만 추출해요. 인과관계나 본인의 반응은 판단하지 않아요.

내용 SHA-256: `8b4609347fa6b27f8c8d793554ee9d1e24a28a729053a447ee7415a717e04bb4`

## nlu-pilot-0024 · other_subject · train

가족: `nlu-v1-outdoor_duration`

### 실제 자유 발화

아빠는 하루 종일 밖에서 일하고 챙 넓은 모자를 쓰세요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "아빠는 하루 종일 밖에서 일하고 챙 넓은 모자를 쓰세요.",
  "topics": [
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.outdoor_time",
      "value": "prolonged",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "아빠는 하루 종일 밖에서 일하고"
    },
    {
      "variable_id": "sun.shade_clothing",
      "value": "챙 넓은 모자 착용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "아빠는 하루 종일 밖에서 일하고 챙 넓은 모자를 쓰세요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

다른 사람의 장시간 야외와 모자 사용을 분리하며 사용자 본인의 노출로 저장하지 않아요.

내용 SHA-256: `314175b8fcb08010863d4178ad82708e34f74c94e2827663a2cc353cc7e51de0`

## nlu-pilot-0025 · other_subject · train

가족: `nlu-v1-other_hand_dryness`

### 실제 자유 발화

친구는 손등이 건조하대요. 저는 제 피부 얘기는 아직 안 했어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "친구는 손등이 건조하대요. 저는 제 피부 얘기는 아직 안 했어요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "친구는 손등이 건조하대요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

친구의 건조함만 후보예요. 자기 피부 미보고를 자기 건조함 부정으로 바꾸지 않아요.

내용 SHA-256: `ba3ba846a0d8718a9b097572747b30591ae3fd7300037adfa8554c9b6b53a7f1`

## nlu-pilot-0026 · other_subject · train

가족: `nlu-v1-other_product_routine`

### 실제 자유 발화

엄마는 수분크림 C를 매일 쓰고 계세요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "엄마는 수분크림 C를 매일 쓰고 계세요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "수분크림 C 매일 사용",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "엄마는 수분크림 C를 매일 쓰고 계세요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "수분크림 C",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

루틴 주어와 제품 사용 주체는 엄마예요. 성분·농도는 추출하지 않아요.

내용 SHA-256: `1f431e78f75e57ca64b56219fd2bda6936245ce4c8dd6af430c387730aeed05c`

## nlu-pilot-0027 · other_subject · train

가족: `nlu-v1-other_decanting`

### 실제 자유 발화

룸메이트는 쓰던 화장수를 다른 용기에 덜어 썼대요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "룸메이트는 쓰던 화장수를 다른 용기에 덜어 썼대요.",
  "topics": [
    "storage_label"
  ],
  "slot_candidates": [
    {
      "variable_id": "storage.decanting",
      "value": "다른 용기로 소분",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "룸메이트는 쓰던 화장수를 다른 용기에 덜어 썼대요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "화장수",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

타인의 소분 사실만 추출하고 용기 손상·오염 여부를 추가하지 않아요.

내용 SHA-256: `52d30db6dfde4ab5605ef4d2b362838cde511e9cab6afef9595292f70b556289`

## nlu-pilot-0028 · other_subject · train

가족: `nlu-v1-eye_stinging_context`

### 실제 자유 발화

언니는 선크림을 쓰고 눈이 시리대요. 저는 오늘 실내에서만 지냈어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "언니는 선크림을 쓰고 눈이 시리대요. 저는 오늘 실내에서만 지냈어요.",
  "topics": [
    "discomfort_report",
    "outdoor_sun"
  ],
  "slot_candidates": [
    {
      "variable_id": "sun.outdoor_time",
      "value": "none",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "저는 오늘 실내에서만 지냈어요"
    },
    {
      "variable_id": "skin.eye_symptom_context",
      "value": "선크림을 쓰고",
      "polarity": "affirmed",
      "subject": "other",
      "confidence": "high",
      "evidence_span": "선크림을 쓰고"
    }
  ],
  "symptom_candidates": [
    {
      "symptom": "eye_stinging",
      "polarity": "affirmed",
      "subject": "other",
      "persistence": "unknown",
      "evidence_span": "언니는 선크림을 쓰고 눈이 시리대요"
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

### 원문과 판단의 연결

타인의 눈 시림 및 명시된 발생 상황('선크림을 쓰고', skin.eye_symptom_context/other)과 본인의 실내 체류를 서로 다른 주어로 일관되게 유지해요.

내용 SHA-256: `53e05a6ab0515581dc5cda5fa43956272518d610515d34d3cdc08e5ce7c01318`

## nlu-pilot-0029 · high_risk_symptom · train

가족: `nlu-v1-persistent_redness_pain`

### 실제 자유 발화

며칠째 계속 볼이 붉고 아파요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "며칠째 계속 볼이 붉고 아파요.",
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
      "evidence_span": "며칠째 계속 볼이 붉고 아파요"
    },
    {
      "symptom": "pain",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "persistent",
      "evidence_span": "며칠째 계속 볼이 붉고 아파요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

지속된 붉음과 통증을 별도 후보로 남기고 질환을 진단하지 않아요.

내용 SHA-256: `2e9ec62a60c43028019a4b425bb8cf0f473ee14d8c4cbf0f9521da90ab8c6f30`

## nlu-pilot-0030 · high_risk_symptom · train

가족: `nlu-v1-new_burning`

### 실제 자유 발화

방금 얼굴이 화끈거리기 시작했어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "방금 얼굴이 화끈거리기 시작했어요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "burning",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "방금 얼굴이 화끈거리기 시작했어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

방금 시작된 화끈거림을 recent로 표현하고 원인 제품은 만들지 않아요.

내용 SHA-256: `3b82e426e7230e699af1f06e58035eb0bc0ed9e572d61f0a6a621f159dde3f10`

## nlu-pilot-0031 · high_risk_symptom · val_internal

가족: `nlu-v1-swelling_onset_unknown`

### 실제 자유 발화

입가가 부었는데 언제부터인지는 잘 모르겠어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "입가가 부었는데 언제부터인지는 잘 모르겠어요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "swelling",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "unknown",
      "evidence_span": "입가가 부었는데 언제부터인지는 잘 모르겠어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

붓기는 언급됐지만 시작·지속성은 미상이에요. 최근 발생이라고 바꾸지 않아요.

내용 SHA-256: `569df644d1e153ea92b14bc4f2b0ffec4d937e5e5c3fbf1d1f92de00371f6f79`

## nlu-pilot-0032 · high_risk_symptom · train

가족: `nlu-v1-repeated_peeling`

### 실제 자유 발화

세수할 때마다 피부가 벗겨지는 일이 반복돼요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "세수할 때마다 피부가 벗겨지는 일이 반복돼요.",
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
      "evidence_span": "세수할 때마다 피부가 벗겨지는 일이 반복돼요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

반복이라는 명시적 빈도를 유지하고 한 번의 최근 발생이나 지속 상태로 바꾸지 않아요.

내용 SHA-256: `9eaa02f83b57626561a18423e9dbcfb94978e0a171f1b7305a972e5e156d2306`

## nlu-pilot-0033 · high_risk_symptom · train

가족: `nlu-v1-new_tightness`

### 실제 자유 발화

세수는 평소처럼 했는데, 볼이 당기는 증상은 오늘 처음 시작됐어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "세수는 평소처럼 했는데, 볼이 당기는 증상은 오늘 처음 시작됐어요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "tightness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "recent",
      "evidence_span": "볼이 당기는 증상은 오늘 처음 시작됐어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

증상의 시작 시점이 명시된 당김만 추출하며 장벽 손상이나 원인을 추가하지 않아요.

내용 SHA-256: `8c6b9f5fde5fa2c5099fc129f2c2ff14315439cee99726e2583504dd44c8abd5`

## nlu-pilot-0034 · high_risk_symptom · val_internal

가족: `nlu-v1-persistent_breakout`

### 실제 자유 발화

트러블이 몇 주째 계속 남아 있어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "트러블이 몇 주째 계속 남아 있어요.",
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
      "evidence_span": "트러블이 몇 주째 계속 남아 있어요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

트러블이라는 표준 후보를 사용하고 여드름 진단이나 치료 답변으로 확장하지 않아요.

내용 SHA-256: `9ac665b52a42e18ddff8521f081f8be16c0dc8f03285560523447b80f3bce94a`

## nlu-pilot-0035 · high_risk_symptom · train

가족: `nlu-v1-repeated_discomfort_cluster`

### 실제 자유 발화

최근 들어 씻을 때마다 건조하고 가렵고 따가워요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "최근 들어 씻을 때마다 건조하고 가렵고 따가워요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
  "symptom_candidates": [
    {
      "symptom": "dryness",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "최근 들어 씻을 때마다 건조하고 가렵고 따가워요"
    },
    {
      "symptom": "itching",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "최근 들어 씻을 때마다 건조하고 가렵고 따가워요"
    },
    {
      "symptom": "stinging",
      "polarity": "affirmed",
      "subject": "self",
      "persistence": "repeated",
      "evidence_span": "최근 들어 씻을 때마다 건조하고 가렵고 따가워요"
    }
  ],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

최근이라는 시작 표현보다 '때마다'의 반복 양상을 지속성 분류에 반영해요. 세 증상 모두 후보이며 자동 확인하지 않아요.

내용 SHA-256: `5f5686a806b2fe5eb69894919fd55b2c4ad3626805d07ab74003747356fe63e0`

## nlu-pilot-0036 · product_mention · train

가족: `nlu-v1-known_lotion_using`

### 실제 자유 발화

라임 로션 A를 요즘 매일 쓰고 있어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "라임 로션 A를 요즘 매일 쓰고 있어요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [
    {
      "variable_id": "method.current_routine",
      "value": "라임 로션 A 매일 사용",
      "polarity": "affirmed",
      "subject": "self",
      "confidence": "high",
      "evidence_span": "라임 로션 A를 요즘 매일 쓰고 있어요"
    }
  ],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "라임 로션 A",
      "usage_state": "using",
      "matched_catalog_hint": "syn-catalog:lime-lotion-a@v1"
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

정확히 같은 raw span의 가상 카탈로그 힌트만 연결하고, 빈도('매일')가 명시된 실제 사용이므로 method.current_routine도 0026과 동일하게 병행 추출해요. 이름으로 농도·효능을 추출하지 않아요.

내용 SHA-256: `e5ae69ccebecb22ac17a5749e34f10ee274c25a385be8dcd3e4ed20b3bbf16a9`

## nlu-pilot-0037 · product_mention · train

가족: `nlu-v1-unregistered_cream`

### 실제 자유 발화

크림 Z를 요즘 쓰고 있는데 검색에는 안 나오더라고요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "크림 Z를 요즘 쓰고 있는데 검색에는 안 나오더라고요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "크림 Z",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

현재 사용과 미등록 제품명을 보존하고 catalog hint를 만들어 넣지 않아요.

내용 SHA-256: `3312bbbee6901a6c42444ba95dd63bafc9b8039aeb15fc0c6fb80cf7d49ac8f7`

## nlu-pilot-0038 · product_mention · val_internal

가족: `nlu-v1-product_prefix_collision`

### 실제 자유 발화

지금은 Lotion AB를 써 볼까 생각 중이에요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "지금은 Lotion AB를 써 볼까 생각 중이에요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "Lotion AB",
      "usage_state": "considering",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

Lotion A는 원문 부분 문자열이지만 Lotion AB와 동일 span이 아니므로 matched_catalog_hint는 null이에요.

내용 SHA-256: `beff185e3820cb0adc67622f12acc834f7756805e929e3247fc72f4b64ed717b`

## nlu-pilot-0039 · product_mention · train

가족: `nlu-v1-stopped_lotion`

### 실제 자유 발화

Lotion A는 이제 안 써요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "Lotion A는 이제 안 써요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "Lotion A",
      "usage_state": "stopped",
      "matched_catalog_hint": "syn-catalog:lotion-a@v1"
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

정확한 힌트는 연결하되 사용 상태는 stopped예요. 성분·안전성은 만들지 않아요.

내용 SHA-256: `cb43ae40fec6a133ffe225861308ca929a2f38a4bc96fd0473dabe8a671db0bb`

## nlu-pilot-0040 · product_mention · train

가족: `nlu-v1-other_gel_product`

### 실제 자유 발화

동생이 젤 Q를 쓰고 있어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "동생이 젤 Q를 쓰고 있어요.",
  "topics": [
    "other"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "젤 Q",
      "usage_state": "other_person",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

도포 목적이나 피부 상태는 알 수 없어요. 주체가 타인인 제품 언급만 남겨요.

내용 SHA-256: `adaa2ca50845ae8743fe3bd7f0c939ac3b4dc583a5cfde0ea67a0b5f96004467`

## nlu-pilot-0041 · product_mention · train

가족: `nlu-v1-product_usage_unknown`

### 실제 자유 발화

세럼 R이라는 이름만 들었고 누가 쓰는지는 몰라요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "세럼 R이라는 이름만 들었고 누가 쓰는지는 몰라요.",
  "topics": [
    "other"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "세럼 R",
      "usage_state": "unknown",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

사용 여부·주체가 불명확하므로 using이나 considering으로 추측하지 않아요.

내용 SHA-256: `6bb3e1b5ecde5660c418f0f92e0c7e95374a8d040199e5fe77fa304f3466ca65`

## nlu-pilot-0042 · product_mention · val_internal

가족: `nlu-v1-product_prefix_collision`

### 실제 자유 발화

로션 M은 살까 고민 중이고 지금 바르는 건 로션 MN이에요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "로션 M은 살까 고민 중이고 지금 바르는 건 로션 MN이에요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [
    {
      "raw_text": "로션 M",
      "usage_state": "considering",
      "matched_catalog_hint": "syn-catalog:lotion-m@v1"
    },
    {
      "raw_text": "로션 MN",
      "usage_state": "using",
      "matched_catalog_hint": null
    }
  ],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

M은 정확히 일치하는 힌트가 있지만 MN에는 연결하지 않아요. 두 제품의 사용 상태도 분리해요.

내용 SHA-256: `8a0383881835597107f32734d418dc3b1e3c062392b4d13f661c0151a5f2ea74`

## nlu-pilot-0043 · no_signal_noise · train

가족: `nlu-v1-greeting_only`

### 실제 자유 발화

안녕하세요, 반가워요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "안녕하세요, 반가워요.",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

인사만 있으므로 슬롯·증상·제품 후보가 없어요.

내용 SHA-256: `518a20ff853e8f054f00812b73f6adec47ff6cf7828e2ef09699f1f2ae0678ed`

## nlu-pilot-0044 · no_signal_noise · train

가족: `nlu-v1-unrelated_meal`

### 실제 자유 발화

오늘 점심은 김밥 먹었어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "오늘 점심은 김밥 먹었어요.",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

식사 발화에서 피부 효과·상태를 추론하지 않아요.

내용 SHA-256: `c9c586278c642e2ee83165a3b3dd3a7effe77478e0db7bebfc805fa1dea25cc1`

## nlu-pilot-0045 · no_signal_noise · train

가족: `nlu-v1-filler_only`

### 실제 자유 발화

음… 어…

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "음… 어…",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

추출할 구체적 내용이 없는 머뭇거림이에요.

내용 SHA-256: `ab8e1b3c2adff52290b00509ed0ffd207fe7d4ca79b0e4d6c83ddf685edefa04`

## nlu-pilot-0046 · no_signal_noise · train

가족: `nlu-v1-unrelated_delivery`

### 실제 자유 발화

택배가 내일 온대요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "택배가 내일 온대요.",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

배송 발화만으로 화장품 구매·보유·사용을 만들지 않아요.

내용 SHA-256: `e1fe19947503b49cbd7e8ea6d86cd28b4d3b311fd07b875feedb9a0bab88e32a`

## nlu-pilot-0047 · no_signal_noise · train

가족: `nlu-v1-unrelated_device`

### 실제 자유 발화

휴대폰 배터리가 거의 없어요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "휴대폰 배터리가 거의 없어요.",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

기기 상태는 이 NLU의 피부·제품 후보가 아니에요.

내용 SHA-256: `d047500487b56f90b93a3e65a2cd3591c2f4b6acfe8f4b67780a5314f68fafe5`

## nlu-pilot-0048 · no_signal_noise · val_internal

가족: `nlu-v1-emoji_only`

### 실제 자유 발화

✅

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "✅",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

정형 버튼 탭이 아닌 자유 채팅 문자예요. 추출할 사실이 없어요.

내용 SHA-256: `7fe631cb42492a25d6690e3a9b436fbe0a58796f4d5239fa083187c1fbb247d4`

## nlu-pilot-0049 · no_signal_noise · train

가족: `nlu-v1-missing_chat_context`

### 실제 자유 발화

이어서요.

직전 질문: None
대상 슬롯: None

### 예상 추출 JSON

```json
{
  "schema_version": "v3.0",
  "source_text": "이어서요.",
  "topics": [],
  "slot_candidates": [],
  "symptom_candidates": [],
  "product_mentions": [],
  "confirmed_by_user": false
}
```

### 원문과 판단의 연결

직전 질문이 없는 단독 발화이므로 대상 슬롯을 임의로 정하지 않아요.

내용 SHA-256: `397f211d519a1a349aa457169d7aa8c0efb9bd824cc85bd81314f1dc0295744b`
