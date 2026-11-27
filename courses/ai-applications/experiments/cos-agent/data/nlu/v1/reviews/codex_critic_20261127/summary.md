# Codex 별도 에이전트 내부 검토

49행을 작성자 해설·기존 리뷰·생성 스크립트 없이 직접 읽었습니다. **PASS 46 / FAIL 0 / REVIEW 3**입니다.

- 0009: 횟수와 표시 준수의 표현 우선순위.
- 0014: 눈시림 발생 상황의 symptom-only/context 슬롯 정책.
- 0036: 0026과 매일 사용 current_routine 중복 추출 정책 차이.

확정 오류가 아니라 명세 불확실성이므로 정답을 수정하지 않았습니다. 각 행의 원문·actual expected JSON 인용과 한국어 근거는 critic_raw.jsonl에 있습니다. 같은 GPT-6 계열의 별도 에이전트 검토이며 다른 모델 계열 CrossModelCritic PASS나 사람 승인이 아닙니다. 세부 모델 변형은 확인할 수 없습니다.

## REVIEW raw

### nlu-pilot-0009

```json
{
  "source_text": "제품 표시대로 한 번만 해요.",
  "previous_question": "한 번 씻을 때 세정 단계를 몇 번 거치나요?",
  "target_slot_id": "cleansing.steps"
}
```

```json
{
  "schema_version": "v3.0",
  "source_text": "제품 표시대로 한 번만 해요.",
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

단계 수 질문과 target에 한 번만이라는 답은 정수 1을 지지한다. 그러나 제품 표시대로라는 정보와 동일 슬롯의 according_to_product_removal_instructions 대안 중 무엇을 보존할지 우선순위가 명시되지 않아 REVIEW다.

횟수와 표시 준수의 동시 보존 또는 우선순위 지침을 정한 뒤 검토하세요. 정답은 수정하지 않았습니다.

### nlu-pilot-0014

```json
{
  "source_text": "한 번이 아니라 씻을 때마다 눈이 시려요.",
  "previous_question": "눈이 시린 증상은 한 번 있었나요, 반복되나요?",
  "target_slot_id": "skin.eye_symptom_context"
}
```

```json
{
  "schema_version": "v3.0",
  "source_text": "한 번이 아니라 씻을 때마다 눈이 시려요.",
  "topics": [
    "discomfort_report"
  ],
  "slot_candidates": [],
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

한 번이 아니라 씻을 때마다는 눈시림 존재의 부정이 아닌 repeated의 근거다. 다만 target skin.eye_symptom_context의 발생 상황이 symptom span에만 남고 슬롯은 비었다. symptom만으로 충분한지 별도 context 슬롯도 필요한지 불명확해 REVIEW다.

symptom만으로 발생 상황이 충분히 표현되는지, context 슬롯도 필요한지 지침을 명시한 뒤 검토하세요. 정답은 수정하지 않았습니다.

### nlu-pilot-0036

```json
{
  "source_text": "라임 로션 A를 요즘 매일 쓰고 있어요.",
  "previous_question": null,
  "target_slot_id": null
}
```

```json
{
  "schema_version": "v3.0",
  "source_text": "라임 로션 A를 요즘 매일 쓰고 있어요.",
  "topics": [
    "moisturizing"
  ],
  "slot_candidates": [],
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

라임 로션 A 전체 제품명과 힌트 span이 일치하고 using이 명시적이다. 다만 0026과 달리 매일이라는 빈도가 current_routine 없이 후보에서 빠진다. 중복 추출 정책이 불명확해 확정 FAIL 대신 REVIEW다.

매일 사용을 product mention 외 current_routine에도 담을지 공통 지침을 정해 0026과 함께 검토하세요. 정답은 수정하지 않았습니다.

### nlu-pilot-0026 (0036 comparison)

```json
{
  "request": {
    "source_text": "엄마는 수분크림 C를 매일 쓰고 계세요.",
    "catalog_hints": [],
    "previous_question": null,
    "target_slot_id": null,
    "allowed_variable_ids": [
      "method.body_site",
      "method.water_temperature",
      "method.tools",
      "method.friction",
      "method.drying",
      "cleansing.target_load",
      "cleansing.repeat_wash",
      "cleansing.steps",
      "method.current_routine",
      "method.sequence",
      "method.skin_wetness",
      "method.rinse",
      "method.mixing",
      "moisturizing.after_wash_delay",
      "moisturizing.comfort",
      "moisturizing.coverage",
      "moisturizing.dryness_return",
      "moisturizing.reapplication",
      "sun.outdoor_time",
      "sun.water_contact",
      "sun.sweat",
      "sun.coverage_gaps",
      "sun.exposed_sites",
      "sun.shade_clothing",
      "sun.reapplication",
      "storage.opened_at",
      "storage.decanting",
      "storage.container",
      "storage.sensory_change",
      "storage.expiry",
      "storage.pao",
      "storage.water_ingress",
      "storage.light_air",
      "skin.eye_symptom_context"
    ],
    "allowed_symptoms": [
      "breakout",
      "burning",
      "dryness",
      "eye_stinging",
      "itching",
      "pain",
      "peeling",
      "redness",
      "stinging",
      "swelling",
      "tightness"
    ],
    "allowed_topics": [
      "cleansing_method",
      "discomfort_report",
      "moisturizing",
      "other",
      "outdoor_sun",
      "repeat_cleansing",
      "routine_conflict",
      "storage_label"
    ]
  },
  "expected": {
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
}
```
