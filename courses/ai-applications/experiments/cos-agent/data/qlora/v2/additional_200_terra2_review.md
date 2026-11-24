# 신규 합성 개발 후보 200행

기존 648행은 변경하지 않았어요. 154 solution·46 hold를 추가한 합계는 848행이에요.
`development_preview`, `production_enabled=false`를 유지해요. 실제 사용자 자료·임상 정답·엔진 실행 결과가 아니에요.
입력을 먼저 동결하고 답변을 작성했어요. 현재 내부 감사 기록은 내용 해시로 연결해요. 다른 모델 계열 검수·사람 승인과 구분해요.
고정 파일럿 승인 게이트를 통과하거나 공식 900행을 완성했다는 뜻이 아니에요. 저장 출처 청크는 등록 범위의 요약이에요.

## syn-hold-0153 — 세정제 후 지속 불편과 통증

- 내용 해시: `5f9876dfa44c229cd965a3ae75f184ed2b0339e261bf5314258d5fdd81fe10ba`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 사용 후 지속 불편과 통증을 시간상 연결하되 원인은 확정하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 세정제 사용 직후부터 중간 정도로 아프고 지금도 불편해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_used": true,
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "cleanser_use",
          "reported_timing": "pain_from_immediately_after_use",
          "ongoing_discomfort_reported": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편과 통증으로 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "사용 직후부터 중간 정도로 아프고 지금도 불편해요",
    "connection": "현재까지 이어지는 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "중간 정도로 아프고",
    "connection": "통증 정도다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세정제 사용 직후부터",
    "connection": "사용 후 시간적 연결이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "사용 직후부터 중간 정도로 아프고 지금도 불편해요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정제 사용 후 불편이 이어지고 통증도 있어 개별 루틴이나 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 제품 사용을 잠시 중단하고 전문가의 확인을 받아 주세요. 시간상 연결만으로 원인을 확정할 수 없어요.

## syn-hold-0154 — 세안마다 반복 통증

- 내용 해시: `db83799ed7714f68aa18417378541af216da13796141147af5d39c8a144d1e99`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 통증 대신 세안 때마다 반복되는 통증을 다룬다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴을 씻을 때마다 중간 정도 통증이 반복돼요. 세정제는 계속 쓰고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "repeated",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_used": true,
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "face_washing",
          "reported_timing": "pain_repeats_during_each_wash"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "세안할 때마다 반복되는 통증에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴을 씻을 때마다 중간 정도 통증이 반복돼요",
    "connection": "세안 중 반복 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "중간 정도 통증이 반복돼요",
    "connection": "통증 정도다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "세정제는 계속 쓰고 있어요",
    "connection": "현재 제품 사용이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴을 씻을 때마다 중간 정도 통증이 반복돼요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세안할 때마다 통증이 반복돼 개별 루틴과 제품 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 세정제 사용은 잠시 중단하고 전문가에게 통증을 확인받아 주세요. 원인이나 진단은 이 정보만으로 정할 수 없어요.

## syn-hold-0155 — 기기 제품 병용 후 불편

- 내용 해시: `d22df2aa104be696687ddf6be26cbe9f3029bb2b71574efa887bfeddf16fc49e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 불편과 병용 이력을 보존하며 원인을 기기나 제품으로 특정하지 않는다. / syn-hold-0031

### 설계한 시나리오 raw

얼굴 세정 브러시와 세정제를 함께 쓰고 난 뒤 불편이 계속돼요. 어느 쪽 때문인지는 모르고 병용 지침도 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_used": true,
        "used_with_cleanser": true,
        "device_type": "cleansing_brush"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "brush_and_cleanser_combination",
          "reported_timing": "discomfort_after_combination_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 개별 권고를 보류해요."
    },
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기 병용의 지침은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1",
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "쓰고 난 뒤 불편이 계속돼요",
    "connection": "병용 후 지속 불편이다."
  },
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "세정 브러시와 세정제를 함께 쓰고",
    "connection": "실제 기기와 제품 병용이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "병용 지침도 확인하지 못했어요",
    "connection": "병용 지침 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "세정 브러시와 세정제를 함께 쓰고 난 뒤 불편이 계속돼요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  },
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "세정 브러시와 세정제를 함께 쓰고",
    "connection": "브러시 유형과 세정제의 실제 병용이 보고됐다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정 브러시와 제품을 함께 쓴 뒤 불편이 계속되어 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 병용은 잠시 중단하고 전문가의 확인을 받아 주세요. 기기와 제품 중 어느 쪽이 원인인지 확인되지 않았어요 [kb:B-G06@0.6.1].

## syn-hold-0156 — 세정 중 심한 통증

- 내용 해시: `dc8ba9c0cec95e81bacf0ec77c5ae447e9e007222eb07146ab91e12d3fbf75d0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 사용 중 심한 통증과 현재 불편 여부 답변 거절을 분리한다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴에 씻어내는 세정제를 쓰는 중 심하게 아팠어요. 지금도 아픈지는 답변하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_past_pain": {
          "subject": "self",
          "severity": "severe",
          "timing": "during_cleanser_use",
          "current_pain_status": "declined"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "세정 중 심한 통증이 보고되어 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "씻어내는 세정제를 쓰는 중",
    "connection": "실제 제품 사용이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "지금도 아픈지는 답변하고 싶지 않아요",
    "connection": "현재 통증에 대한 답변 거절이다."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "씻어내는 세정제를 쓰는 중 심하게 아팠어요",
    "connection": "세정제 사용 중 과거의 심한 통증이며 현재 상태는 거절이다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정제 사용 중 심한 통증이 보고되어 개별 루틴이나 제품 안내를 보류해요 [kb:B-B01@0.6.1]. 현재 통증 여부는 답변을 원하지 않으셨어요.

### 필요한 다음 단계
통증과 연결된 제품 사용을 잠시 중단하고 전문가에게 확인받아 주세요. 현재 상태를 임의로 없거나 계속된다고 추정하지 않아요.

## syn-hold-0157 — 개별 진료 계획과 일반 세정 시간

- 내용 해시: `cecb78ece6436781b6d058268b86c4eaed117b8320ffd83a00e8cdc3931e82db`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 반복 따가움 사례를 대체한 별개의 신규 합성: 증상을 만들지 않고 개별 진료 계획을 일반 조언으로 대체하려는 요청을 보류한다. / syn-hold-0030

### 설계한 시나리오 raw

의료진이 얼굴 세정 시간을 따로 정해 줬어요. 일반적인 세안 시간으로 그 지시를 바꿔도 될지 알려 주세요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "face_washing_timing_specified": true,
        "requested_override_by_general_advice": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "개별 진료에서 정한 세정 시간을 일반 권고로 대체하는 판단을 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "의료진이 얼굴 세정 시간을 따로 정해 줬어요",
    "connection": "의료진이 정한 세정 시간이다."
  },
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "일반적인 세안 시간으로 그 지시를 바꿔도 될지",
    "connection": "개별 지시를 일반 조언으로 대체하려는 요청이다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
의료진이 정한 얼굴 세정 시간을 일반적인 안내로 대체하는 개별 권고는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지시를 바꾸기 전에 그 계획을 정한 의료진에게 확인해 주세요. 현재 정보만으로 지시의 이유를 추정하거나 변경을 결정하지 않아요.

## syn-hold-0158 — 헹굼 이행 후 지속 불편

- 내용 해시: `426f7c21ad94ce7599ddd17fc629587dea7b55f2b87a7fb733d1935679f814b0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 이행이 확인되어도 지속 불편에 대한 보류를 해제하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 세안 후 불편이 지속돼요. 세정제 표시에는 물로 헹구라고 되어 있고 저는 헹궜어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "face_washing",
          "reported_timing": "discomfort_after_washing_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "헹굼을 수행했더라도 지속 불편에 대한 개별 권고는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 세안 후 불편이 지속돼요",
    "connection": "현재 지속 불편이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "세정제 표시에는 물로 헹구라고 되어 있고",
    "connection": "제품의 헹굼 표시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "저는 헹궜어요",
    "connection": "헹굼을 실행했다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세안 후 불편이 지속돼요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세안 후 불편이 지속되므로 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1]. 표시된 헹굼을 수행했다는 사실이 이 보류를 없애지는 않아요.

### 필요한 다음 단계
불편과 연결된 세정제 사용은 잠시 중단하고 전문가의 확인을 받아 주세요. 헹굼 준수만으로 원인이나 안전을 확정할 수 없어요.

## syn-hold-0159 — 세안 중 통증 악화

- 내용 해시: `69299fb98645f2df1cfc542a6cee7ccd0bb49431d6c951bf22c2250e012ebb38`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 심해진 통증과 수온 미상을 분리하고 원인을 추정하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 세안할 때 통증이 더 심해져 지금은 심한 통증이고 불편도 이어져요. 평소 쓰는 물이 뜨거운지 아닌지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "severe",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "face_washing",
          "reported_timing": "pain_worsened_during_washing",
          "current_pain": "severe"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "악화된 심한 통증과 지속 불편에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "불편도 이어져요",
    "connection": "현재까지 이어지는 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "지금은 심한 통증이고",
    "connection": "현재 심한 통증이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "평소 쓰는 물이 뜨거운지 아닌지는 기억나지 않아요",
    "connection": "수온 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세안할 때 통증이 더 심해져 지금은 심한 통증이고 불편도 이어져요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
심한 통증과 이어지는 불편이 보고되어 개별 루틴이나 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
전문가에게 현재 통증을 확인받아 주세요. 물 온도는 기억나지 않으므로 통증의 원인으로 추정하지 않아요.

## syn-hold-0160 — 지속 불편과 pH 미상

- 내용 해시: `db101df46ed2a8cb96132db4fcfed03874a6a73019598df9fad2d3097861e798`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 불편과 제품 pH 미상을 분리하고 원인을 추정하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴에 세정 제품을 쓴 부위가 계속 불편해요. 그 제품의 pH 정보는 확인되지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "쓴 부위가 계속 불편해요",
    "connection": "사용 부위의 지속 불편이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴에 세정 제품을 쓴 부위",
    "connection": "제품의 실제 사용 부위다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "제품의 pH 정보는 확인되지 않았어요",
    "connection": "pH 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정 제품을 쓴 부위의 불편이 계속돼 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 제품은 잠시 사용을 중단하고 전문가에게 확인받아 주세요. 제품 pH는 미상이며 불편의 원인으로 단정하지 않아요.

## syn-hold-0161 — 기기 사용 뒤 지속 통증

- 내용 해시: `028f322d3d47316c83175e05ed738ed9b61236f58565e1b22681e8b5184010c0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 기기 사용 뒤 통증을 다루되 제품과 병용 자체는 가정하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 세안 기기를 쓴 후 중간 정도 통증이 있고 지금도 이어져요. 기기의 제품 병용 지침은 몰라요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "cleansing_device_use",
          "reported_timing": "pain_after_device_use_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 통증에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "통증이 있고 지금도 이어져요",
    "connection": "지속되는 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "중간 정도 통증이 있고",
    "connection": "통증 정도다."
  },
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "얼굴 세안 기기를 쓴 후",
    "connection": "기기 실제 사용이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "기기의 제품 병용 지침은 몰라요",
    "connection": "기기 지침 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세안 기기를 쓴 후 중간 정도 통증이 있고 지금도 이어져요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세안 기기 사용 후 통증이 이어져 개별 루틴과 제품 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 기기 사용을 잠시 중단하고 전문가의 확인을 받아 주세요. 제품과 실제 병용했는지는 확인되지 않았어요.

## syn-hold-0162 — 세정제 색 변화와 층 분리

- 내용 해시: `0dba62545d4894a9e72e31018161d073c3db8a4b9cbfca925acdc13b73b54c7c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 중 반복 통증 사례를 대체한 신규 합성: 품질 이상을 관찰한 뒤 아직 사용하지 않은 별도 안전 판단이다. / syn-hold-0003, syn-hold-0006

### 설계한 시나리오 raw

얼굴 세정제의 색이 전과 달라지고 층도 분리됐어요. 변화를 본 뒤에는 그 제품을 쓰지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true,
        "separation": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_after_change": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "세정제의 색 또는 냄새 변화와 층 분리가 보고되어 제품 사용을 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "색이 전과 달라지고 층도 분리됐어요",
    "connection": "색 변화와 층 분리다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "변화를 본 뒤에는 그 제품을 쓰지 않았어요",
    "connection": "변화 이후 미사용이다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정제의 색 또는 냄새 변화와 층 분리가 보고되어 제품 사용과 개별 루틴 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
변화 이후 사용하지 않았다고 하셨으니 해당 제품의 사용을 계속 보류하고 표시·보관 이력을 확인해 주세요. 필요한 경우 제조·판매처에 문의해 품질 상태를 확인해요.

## syn-hold-0163 — 증상 위치 일치 미상

- 내용 해시: `c945ffd26150037429044f616db5c81a9868ccb3c73777ee99f5f86b3214a22a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 불편 위치와 물이 닿은 위치의 일치를 추정하지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

세안 후 불편이 계속돼요. 물이 닿은 곳과 불편한 곳이 같은지는 잘 모르겠어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "same_as_water_contact_site": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "washing",
          "reported_timing": "discomfort_after_washing_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "세안 후 불편이 계속돼요",
    "connection": "지속 불편이다."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "물이 닿은 곳과 불편한 곳이 같은지는 잘 모르겠어요",
    "connection": "노출 위치와 불편 위치의 일치 여부 미상이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "세안 후 불편이 계속돼요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세안 후 불편이 계속되어 개별 루틴이나 제품 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지속되는 불편에 대해 전문가의 확인을 받아 주세요. 물이 닿은 위치와 불편한 위치가 같은지는 미상이라 일치한다고 추정하지 않아요.

## syn-hold-0164 — 패드 뒤 지속 통증

- 내용 해시: `dda1451ea3866daf421844cf1cf1965899e784be50ee6d300b43ca7d4507da4a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 패드 사용 뒤 지속 통증과 제품 병용 미상을 구별한다. / syn-hold-0031

### 설계한 시나리오 raw

얼굴에 클렌징 패드를 쓴 다음부터 중간 정도로 아프고 지금까지 통증이 이어져요. 세정제를 함께 썼는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "cleansing_pad"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_used_with_pad": "unknown",
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "cleansing_pad_use",
          "reported_timing": "pain_from_after_pad_use_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "도구 사용 후 통증이 지속되어 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "지금까지 통증이 이어져요",
    "connection": "지속 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "중간 정도로 아프고",
    "connection": "통증 정도다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "얼굴에 클렌징 패드를 쓴 다음부터",
    "connection": "실제 사용 도구다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "세정제를 함께 썼는지는 기억나지 않아요",
    "connection": "제품 병용 여부 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "클렌징 패드를 쓴 다음부터 중간 정도로 아프고 지금까지 통증이 이어져요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
클렌징 패드 사용 뒤 통증이 이어져 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
통증과 연결된 패드 사용을 잠시 중단하고 전문가에게 확인받아 주세요. 세정제를 함께 썼는지는 기억나지 않으므로 병용했다고 추정하지 않아요.

## syn-hold-0165 — 제거 후 불편과 제품 거절

- 내용 해시: `107bb3315426b0889f03cde8f18cd7ad7a14a84649dde336e48ddb7590a1486c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제거 목적과 실제 세정제 정보 거절을 구별한다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 선크림을 지우고 나서 불편이 계속돼요. 어떤 세정제를 썼는지는 답변하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "sunscreen": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "sunscreen_removal",
          "reported_timing": "discomfort_after_removal_and_continues"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "제거 후 불편이 지속되어 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "지우고 나서 불편이 계속돼요",
    "connection": "제거 후 지속 불편이다."
  },
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "얼굴 선크림을 지우고 나서",
    "connection": "제거 대상이다."
  },
  {
    "variable_id": "product.type",
    "raw_span": "어떤 세정제를 썼는지는 답변하고 싶지 않아요",
    "connection": "실제 제품 정보 응답 거절이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림을 지우고 나서 불편이 계속돼요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
선크림을 지운 뒤 불편이 계속되어 개별 루틴이나 제품 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지속되는 불편에 대해 전문가에게 확인받아 주세요. 사용한 세정제 정보는 답변을 원하지 않으셨으므로 특정 제품을 추정하지 않아요.

## syn-hold-0166 — 친구 경험과 본인 증상

- 내용 해시: `3e6cf7527e5ba9d9be2d905a9090610ccf28ae9d83f3d3f836690b20ac7f059c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 타인의 무불편 경험으로 본인의 지속 불편과 통증을 덮지 않는다. / syn-hold-0001

### 설계한 시나리오 raw

저는 얼굴 세안 후 불편감이 계속되고 중간 정도 통증도 있어요. 친구가 같은 제품을 문제없이 쓴 경험은 제 상태와 달라요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "reported_use_symptom_relation": {
          "subject": "self",
          "event": "face_washing",
          "reported_timing": "discomfort_after_washing_and_continues",
          "pain": "moderate"
        },
        "other_subject_report": {
          "subject": "friend",
          "same_product": true,
          "reported_experience": "no_problem"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "본인의 지속 불편과 통증으로 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "저는 얼굴 세안 후 불편감이 계속되고",
    "connection": "본인의 지속 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "중간 정도 통증도 있어요",
    "connection": "본인의 통증 정도다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세안 후 불편감이 계속되고 중간 정도 통증도 있어요",
    "connection": "실제 사용·세안과 보고된 불편의 정성적 시간 관계이며, 경과 시간 수치나 인과를 확정하지 않는다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "친구가 같은 제품을 문제없이 쓴 경험은 제 상태와 달라요",
    "connection": "친구의 제품 사용 경험이며 본인의 증상이 아니다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
본인의 불편이 계속되고 통증도 있어 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편과 통증을 전문가에게 확인받아 주세요. 친구가 같은 제품을 문제없이 쓴 경험으로 본인의 증상을 판단하지 않아요.

## syn-hold-0167 — 반복 통증과 미사용일 불편

- 내용 해시: `a3a0b92a8b632fe0a42a3ae54e78f53e9338479abb1a0da76fa42018f60dc968`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 세정 시 반복 통증과 현재 미사용일의 지속 불편을 구분한다. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 세정할 때 반복해서 중간 정도로 아프고 오늘은 세안하지 않았는데도 불편이 이어져요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleansing_today": false,
        "pain_repeated_during_cleansing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "반복 통증과 현재 지속 불편으로 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "오늘은 세안하지 않았는데도 불편이 이어져요",
    "connection": "미사용일에도 이어지는 현재 불편이다."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "반복해서 중간 정도로 아프고",
    "connection": "세정 때 통증 정도다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세정할 때 반복해서 중간 정도로 아프고 오늘은 세안하지 않았는데도",
    "connection": "반복 통증과 오늘 미사용이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
세정할 때 반복되는 통증과 현재 이어지는 불편 때문에 개별 루틴이나 제품 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
반복 통증과 오늘 세안하지 않았는데도 이어지는 불편을 전문가에게 설명하고 확인받아 주세요. 그 시간적 관계만으로 원인을 단정하지 않아요.

## syn-hold-0168 — 지속 통증과 새 제품 선택 요청 및 원인 미상

- 내용 해시: `69a85c0b85da0ca7abbe6877d64f9cd18daf97333e2a801572ffa832f257581a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 0022도 지속 불편과 중간 통증을 다루지만, 이 후보는 새 제품 선택 요청과 원인 미상을 함께 다뤄요. / syn-hold-0022

### 설계한 시나리오 raw

얼굴의 불편이 계속되고 통증도 중간 정도예요. 새 제품을 살지 묻지만 원인은 확인되지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "site": "face",
        "cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편과 통증 때문에 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴의 불편이 계속되고",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "통증도 중간 정도예요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴의 불편이 계속되고 통증도 중간 정도예요. 새 제품을 살지 묻지만 원인은 확인되지 않았어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "새 제품을 살지 묻지만",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되고 중간 정도의 통증도 있어 새 제품 선택을 포함한 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
증상에 관해 피부과 등 전문가에게 확인받아 주세요. 현재 정보만으로 원인을 진단할 수 없어요.

## syn-hold-0169 — 제품 사용 전 통증과 증량 질문

- 내용 해시: `edf4a63a78a0236d456760f33cc79514a96f0d620f0b841748f2b10e7027342b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 사용 전 통증과 증량 질문 / syn-hold-0116

### 설계한 시나리오 raw

보습제를 바르기 전부터 피부 통증이 계속돼요. 보습제 양을 늘리면 해결되는지 궁금해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "pain_preceded_moisturizer": true,
        "increase_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "보습 전부터 지속된 통증을 양 조정만으로 해결하려 하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "보습제를 바르기 전부터 피부 통증이 계속돼요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "보습제를 바르기 전부터 피부 통증이 계속돼요. 보습제 양을 늘리면 해결되는지 궁금해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
보습제 사용 이전부터 통증이 계속되고 있어 양을 늘려 해결하자는 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
통증의 경과와 시작 시점을 전문가에게 설명하고 확인받아 주세요. 이 시간 관계만으로 원인을 알 수 없어요.

## syn-hold-0170 — 면도 없는 날에도 통증 지속

- 내용 해시: `b2e81e23a0350d746d87a87f766981af6107ea812e943f49aaa4772cc47923ac`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 면도 없는 날에도 통증 지속 / syn-hold-0131

### 설계한 시나리오 raw

면도 부위가 계속 아파요. 면도하지 않은 날에도 통증이 이어졌고 원인은 몰라요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "pain_continued_on_nonshaving_day": true,
        "cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "면도하지 않은 날에도 통증이 지속되어 개별 조정은 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "면도 부위가 계속 아파요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "shaving.reaction",
    "raw_span": "면도하지 않은 날에도 통증이 이어졌고 원인은 몰라요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
면도하지 않은 날에도 통증이 이어져 개별 면도나 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
통증의 지속 경과를 피부과 등 전문가에게 상담해 주세요. 면도가 원인인지 현재 정보로 확정하지 않아요.

## syn-hold-0171 — 갈라짐과 심한 통증 및 필요한 손 위생

- 내용 해시: `a39b5b449bf5ec53134db33118d8ab36a7c87507d08592e0602d7001d0d550bf`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 갈라짐과 심한 통증 및 필요한 손 위생 / syn-hold-0009

### 설계한 시나리오 raw

손에 갈라짐과 심한 통증이 있어요. 작업 때문에 손을 씻어야 하지만 어떤 크림이 좋은지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.hand_observation": {
      "variable_id": "skin.hand_observation",
      "state": "known",
      "value": {
        "fissures": true,
        "severe_pain": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "severe",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.wet_work": {
      "variable_id": "hand.wet_work",
      "state": "known",
      "value": {
        "handwashing_required_for_work": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "심한 손 통증과 갈라짐이 있어 개별 제품 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.hand_observation",
    "raw_span": "손에 갈라짐과 심한 통증이 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "손에 갈라짐과 심한 통증이 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "hand.wet_work",
    "raw_span": "작업 때문에 손을 씻어야 하지만",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손의 갈라짐과 심한 통증이 있어 크림 선택을 포함한 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
작업상 손 씻기가 필요하다는 사정과 현재 손 상태를 의료 전문가에게 알려 확인받아 주세요.

## syn-hold-0172 — 지속 따가움과 처방 횟수 변경 요청

- 내용 해시: `6439d8542f5ceecc5b1bb182236565e296002d8137abf3333b776a2eaeb5f34f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 따가움과 처방 횟수 변경 요청 / syn-hold-0035

### 설계한 시나리오 raw

피부과에서 정한 사용 계획이 있어요. 따가움이 계속되는데 제 판단으로 처방 횟수를 바꿔도 되는지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "present": true,
        "frequency_change_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 따가움과 개별 처방 계획이 있어 자의적 변경을 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "피부과에서 정한 사용 계획이 있어요. 따가움이 계속되는데 제 판단으로 처방 횟수를 바꿔도 되는지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "따가움이 계속되는데",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
따가움이 계속되는 가운데 개별 진료 계획이 있어 처방 횟수 변경을 안내하지 않아요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 따가움과 사용 계획을 처방한 의료진에게 알려 변경 필요성을 상담해 주세요.

## syn-hold-0173 — 새 제품 미사용과 단일 성분 회피 해결 가정

- 내용 해시: `f01339a757bb780da5b34fbdbe217c39c4c54d484b0fc563cbb2e964ad1a0002`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 제품 미사용과 단일 성분 회피 해결 가정 / syn-hold-0019

### 설계한 시나리오 raw

새 제품을 쓰지 않았는데도 얼굴 불편이 계속돼요. 향료가 든 제품을 사지 않으면 해결될지 궁금해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "new_product_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "향료가 든 제품을 사지 않으면 해결될지 질문"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편은 향료 회피만으로 해결된다고 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "routine.change_log",
    "raw_span": "새 제품을 쓰지 않았는데도",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 불편이 계속돼요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.goals",
    "raw_span": "향료가 든 제품을 사지 않으면 해결될지 궁금해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 제품을 쓰지 않았더라도 얼굴 불편이 계속되어 제품 선택 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지속되는 불편의 경과를 피부과 등 전문가에게 확인받아 주세요. 향료 회피만으로 해결된다고 단정할 수 없어요.

## syn-hold-0174 — 동시 사용 후 지속 불편과 관련 제품 미상

- 내용 해시: `521df658e3b40bdea4e2a9678ba887117e215a44a027b939c1aa5ca5222044a6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 동시 사용 후 지속 불편과 관련 제품 미상 / syn-hold-0118

### 설계한 시나리오 raw

얼굴에 두 제품을 같이 사용한 뒤 불편이 계속돼요. 어느 제품이 불편과 관련되는지 모르겠어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "two_products_used_on_face": true,
        "cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "불편이 지속되고 관련 제품은 확인되지 않아 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴에 두 제품을 같이 사용한 뒤 불편이 계속돼요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "얼굴에 두 제품을 같이 사용한 뒤 불편이 계속돼요. 어느 제품이 불편과 관련되는지 모르겠어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
두 제품 사용 뒤 불편이 계속되어 개별 루틴과 제품 추천을 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
제품 사용 시점과 불편이 이어진 경과를 전문가에게 설명해 주세요. 어느 제품이 관련됐는지는 아직 미상이에요.

## syn-hold-0175 — 중단 이후 통증 지속과 대체 선택 요청

- 내용 해시: `f21e86279b16baf7bad9c18cbea98e19a5c524fd4dc3f6bb35a42c5d32547b5a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 중단 이후 통증 지속과 대체 선택 요청 / syn-hold-0117

### 설계한 시나리오 raw

불편이 계속되어 사용하던 제품은 이미 중단했어요. 중단 후에도 통증이 이어져 다른 제품을 고를지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_stopped": true,
        "pain_continues": true,
        "replacement_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "중단 뒤에도 통증이 이어져 대체 제품 안내를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "불편이 계속되어 사용하던 제품은 이미 중단했어요. 중단 후에도 통증이 이어져",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "불편이 계속되어 사용하던 제품은 이미 중단했어요. 중단 후에도 통증이 이어져 다른 제품을 고를지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
사용하던 제품을 이미 중단했는데도 통증이 이어져 대체 제품 선택을 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
중단 시점과 그 후의 통증을 피부과 등 전문가에게 알려 확인받아 주세요.

## syn-hold-0176 — 증상 부위와 제품 용도 및 사용 미상 분리

- 내용 해시: `486f4f640a1f0d8151e03336eafe3d8c5057369e5dfc74d8125e8f3e01ff3257`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 증상 부위와 제품 용도 및 사용 미상 분리 / syn-hold-0001

### 설계한 시나리오 raw

눈가에 불편이 계속되고 통증도 있어요. 눈가용으로 표시된 제품은 가지고 있지만 실제 그 부위에 썼는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "eye_area",
        "pain": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "눈가용으로 표시된 보유 제품"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "눈가의 지속 불편과 통증이 있어 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "눈가에 불편이 계속되고",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "눈가에 불편이 계속되고 통증도 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.available_products",
    "raw_span": "눈가용으로 표시된 제품은 가지고 있지만",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "실제 그 부위에 썼는지는 기억나지 않아요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
눈가 불편이 지속되고 통증도 있어 제품 사용에 관한 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
눈가 증상과 경과를 의료 전문가에게 확인받아 주세요. 눈가용 제품을 보유했다는 사실만으로 실제 그 부위에 사용했다고 보지 않아요.

## syn-hold-0177 — 제품 목록 거절과 심한 따가움 및 순서 질문

- 내용 해시: `a66bcb163c6ef89d55f23d73089f60f6cddfcfa3e25f14992a46459bd41ff505`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 목록 거절과 심한 따가움 및 순서 질문 / syn-hold-0122

### 설계한 시나리오 raw

얼굴 불편이 계속되고 따가움이 심해요. 제품 목록을 밝히고 싶지 않지만 순서를 바꾸면 되는지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.stinging": {
      "variable_id": "skin.stinging",
      "state": "known",
      "value": "severe",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": {
        "change_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편과 심한 따가움으로 순서 조정 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 불편이 계속되고",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.stinging",
    "raw_span": "따가움이 심해요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.sequence",
    "raw_span": "순서를 바꾸면 되는지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.available_products",
    "raw_span": "제품 목록을 밝히고 싶지 않지만",
    "connection": "원문에서 해당 답변 거절"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되고 따가움이 심해 제품 순서 조정은 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
증상의 정도와 지속 기간을 의료 전문가에게 상담해 주세요. 제품 목록을 밝히지 않겠다는 선택은 그대로 존중해요.

## syn-hold-0178 — 과거 편안함과 현재 진물 상태 분리

- 내용 해시: `a8e2523bd7d286593ccfe0118ce7fd29311f9936ec04ae86cc584f2229858727`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 과거 편안함과 현재 진물 상태 분리 / syn-hold-0009

### 설계한 시나리오 raw

손 불편이 계속되고 진물이 나요. 이전에 편했던 제품을 그대로 쓰면 되는지 궁금해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.hand_observation": {
      "variable_id": "skin.hand_observation",
      "state": "known",
      "value": {
        "oozing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "previously_comfortable_product_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 손 불편과 진물이 있어 과거 경험만으로 제품 사용을 권하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "손 불편이 계속되고",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.hand_observation",
    "raw_span": "손 불편이 계속되고 진물이 나요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "이전에 편했던 제품을 그대로 쓰면 되는지 궁금해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손 불편이 지속되고 진물이 나므로 과거에 편했던 제품이라도 지금 사용하도록 권하지 않아요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
손의 현재 상태와 경과를 의료 전문가에게 확인받아 주세요. 과거의 사용 경험만으로 현재 상태를 판단할 수 없어요.

## syn-hold-0179 — 지속 통증과 개별 계획 대체 요청

- 내용 해시: `5c6d91e0262b5f46315afb6047e061a5b7ff97c86a31b9ae53ecd1764087c179`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 통증과 개별 계획 대체 요청 / syn-hold-0005

### 설계한 시나리오 raw

의료진이 특정 부위에 대한 관리 계획을 줬어요. 지속되는 통증이 있는데 인터넷 일반 안내로 그 계획을 대신하고 싶어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "present": true,
        "wants_general_guidance_instead": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 통증과 개별 관리 계획이 있어 일반 안내로 대체하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "의료진이 특정 부위에 대한 관리 계획을 줬어요. 지속되는 통증이 있는데 인터넷 일반 안내로 그 계획을 대신하고 싶어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "지속되는 통증이 있는데",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
지속되는 통증이 있고 개별 관리 계획도 있어 일반 안내로 그 계획을 대체하는 권고는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
계획을 준 의료진에게 현재 통증과 계획에 대한 의문을 알려 확인받아 주세요.

## syn-hold-0180 — 지속 따가움과 버전 미상 및 감량 요청

- 내용 해시: `f4c05f3bce836580a25a18a2a4c16e793cde204e868801a84f10fcca36556561`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지속 따가움과 버전 미상 및 감량 요청 / syn-hold-0119

### 설계한 시나리오 raw

얼굴 제품을 바른 후 계속 따가워요. 사용한 제품의 버전을 기억하지 못하고 양을 반으로 줄여 계속 써도 될지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_face_product": true,
        "halve_amount_continue_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "제품 사용 후 지속 따가움이 있어 감량 후 계속 사용하도록 권하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 제품을 바른 후 계속 따가워요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 제품을 바른 후 계속 따가워요. 사용한 제품의 버전을 기억하지 못하고 양을 반으로 줄여 계속 써도 될지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.version",
    "raw_span": "사용한 제품의 버전을 기억하지 못하고",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 제품 사용 뒤 따가움이 계속되어 양을 반으로 줄여 계속 쓰는 방안은 안내하지 않아요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
불편과 연결된 해당 제품의 사용을 중단하고 전문가에게 증상과 사용 경과를 상담해 주세요. 제품 버전은 미상이에요.

## syn-hold-0181 — 타인 경험과 본인 지속 불편 분리

- 내용 해시: `358faa8c8ccc57b1ee113e1db6ffc9dfea3f9b1c42bba4914022f601778fe1a8`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 타인 경험과 본인 지속 불편 분리 / syn-hold-0113

### 설계한 시나리오 raw

얼굴 불편이 계속되는 중 다른 사람은 같은 제품이 편하다고 했어요. 그 경험만 믿고 계속 사용해도 되는지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "other_person_comfortable": true,
        "continue_based_on_other_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "타인의 편안함은 본인의 지속 불편을 대신하지 못해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 불편이 계속되는 중",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "다른 사람은 같은 제품이 편하다고 했어요. 그 경험만 믿고 계속 사용해도 되는지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
다른 사람이 편하게 썼다는 경험과 별개로 본인의 얼굴 불편이 지속되어 계속 사용하도록 권하지 않아요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
본인의 증상과 사용 경과를 전문가에게 상담해 주세요. 타인의 반응을 본인의 반응으로 옮겨 판단할 수 없어요.

## syn-hold-0182 — 자료 수집이 상담 선결 조건인지 질문

- 내용 해시: `84b188e4abd6d4c9033f8939c5efb22c1f4e090aa7380a2a74685d2e067706c4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 자료 수집이 상담 선결 조건인지 질문 / syn-hold-0020

### 설계한 시나리오 raw

지속적인 피부 통증이 있어요. 제품을 바꾸기 전에 먼저 성분표를 다 모아야만 상담받을 수 있는지 궁금해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "collect_all_before_consult_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 통증에 대한 상담을 자료 완비까지 미루지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "지속적인 피부 통증이 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.inci",
    "raw_span": "제품을 바꾸기 전에 먼저 성분표를 다 모아야만 상담받을 수 있는지 궁금해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
피부 통증이 지속되어 제품 변경과 개별 루틴 안내를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
성분표를 모두 모을 때까지 상담을 미루지 말고 현재 통증을 의료 전문가에게 알려 주세요.

## syn-hold-0183 — 예정 진료와 보습 횟수 변경 요청

- 내용 해시: `c7f4e34d1e015b7d5fb2e3924cb3dad43e66e9b5eb69d0363ccc5d030de590d8`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 예정 진료와 보습 횟수 변경 요청 / syn-hold-0037

### 설계한 시나리오 raw

피부 불편이 계속돼서 예정된 진료가 있어요. 불편의 원인은 알 수 없는데 진료를 취소하고 보습 횟수만 바꿀지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "visit_scheduled": true,
        "cancel_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "known",
      "value": {
        "moisturizing_change_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 있어 예정 진료를 보습 횟수 변경으로 대신하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "피부 불편이 계속돼서 예정된 진료가 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "피부 불편이 계속돼서 예정된 진료가 있어요. 불편의 원인은 알 수 없는데 진료를 취소하고 보습 횟수만 바꿀지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "dose.frequency",
    "raw_span": "보습 횟수만 바꿀지 묻고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
불편이 계속되는 상황에서 예정 진료를 취소하고 보습 횟수만 바꾸는 방식은 권하지 않아요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
예정된 진료에서 지속된 불편과 원인이 아직 불명확하다는 점을 말씀해 주세요.

## syn-hold-0184 — 품질 변화와 원제품에 실제 물 첨가

- 내용 해시: `7eb216293b1a8c034e79e94337cf001005687e7c098affbb6941a96077bda3dd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0003은 감각 변화만 관찰한 데 비해 원제품 물 첨가가 실제로 있었고, 인과를 정하지 않은 채 품질과 취급을 함께 확인해요. / syn-hold-0003

### 설계한 시나리오 raw

제품에 평소 없던 냄새와 색 변화가 생겼어요. 그 전에 제품에 물을 직접 넣었어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": {
        "water_added_to_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화는 일반 루틴과 분리해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "제품에 평소 없던 냄새와 색 변화가 생겼어요.",
    "connection": "새 냄새와 색을 보고했으며 분리 여부는 미상이에요."
  },
  {
    "variable_id": "storage.water_ingress",
    "raw_span": "그 전에 제품에 물을 직접 넣었어요.",
    "connection": "원제품에 물을 넣은 실제 행동을 보고했어요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품에 평소 없던 색 또는 냄새 변화가 있어 개별 루틴 안내를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 사용을 중단하고 물을 넣은 이력과 변화를 제조·판매처에 확인해 주세요. 물 첨가가 변화의 원인이라고 단정하지 않아요.

## syn-hold-0185 — 표시된 정상 분리와 새 냄새

- 내용 해시: `678f98c89ae78d96ac6603bbfb0272f70b62e65daf74bfa60ab6e9bb68767309`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 흔들어 쓰라는 제품 표시와 층 분리를 함께 기록하고 별도의 색 또는 냄새 변화는 품질 확인 대상으로 구분해요. 표시만으로 분리의 정상 여부를 확정하지 않아요. / syn-hold-0006

### 설계한 시나리오 raw

표시에는 흔들어 쓰는 제형이라고 적혀 있고 원래도 층이 분리돼요. 이번에는 평소 없던 냄새가 새로 났어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "shake_before_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "separation": true,
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화는 일반 루틴과 분리해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "표시에는 흔들어 쓰는 제형이라고 적혀 있고 원래도 층이 분리돼요.",
    "connection": "제품의 흔들어 사용하라는 표시만 확인했으며 분리를 정상으로 명시한 표시는 확인되지 않아요."
  },
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "이번에는 평소 없던 냄새가 새로 났어요.",
    "connection": "층 분리와 색 또는 냄새 변화가 보고됐지만 해당 구조화 값은 변화 종류를 각각 확정하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
흔들어 쓰라는 표시가 있는 제품에서 색 또는 냄새 변화가 보고되어 개별 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품 사용을 멈추고 관찰된 변화와 제품의 원래 특성을 제조·판매처에 확인해 주세요. 흔들어 쓰라는 표시만으로 층 분리가 정상이라고 확정하지 않아요.

## syn-hold-0186 — 새 냄새 뒤 냉장 계획과 사용 중단

- 내용 해시: `9a731e995b8b434c720d7b21bde24624a13feba93267945e28d17ea0483473d2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0047의 손상 용기·감량 요청과 달리 타인의 냉장 주장, 미실행 보관 변경과 변화 후 사용 중단을 분리해요. / syn-hold-0047

### 설계한 시나리오 raw

제품에 이전에 없던 냄새가 나요. 친구가 냉장하면 괜찮다고 해서 그렇게 할까 생각하지만 아직 옮기지 않았어요. 냄새를 확인한 뒤로 해당 제품은 쓰지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "refrigeration_planned": true,
        "refrigeration_performed": false,
        "other_person_claimed_resolves": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "stopped_after_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화는 일반 루틴과 분리해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "제품에 이전에 없던 냄새가 나요.",
    "connection": "새 냄새가 확인돼요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "친구가 냉장하면 괜찮다고 해서 그렇게 할까 생각하지만 아직 옮기지 않았어요.",
    "connection": "타인의 품질 주장은 증거가 아니며 보관 변경은 미실행 계획이에요."
  },
  {
    "variable_id": "storage.handling",
    "raw_span": "냄새를 확인한 뒤로 해당 제품은 쓰지 않았어요.",
    "connection": "변화 이후 해당 제품을 사용하지 않았어요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 냄새가 생긴 제품의 개별 사용 안내를 보류해요 [kb:B-S04@0.6.1]. 냉장하면 괜찮다는 친구의 말은 품질 확인이 아니에요.

### 필요한 다음 단계
현재 해당 제품을 사용하지 않는 상태에서 표시와 이력을 확인하고 필요하면 제조·판매처에 문의해 주세요. 냉장 이동은 아직 계획일 뿐이에요.

## syn-hold-0187 — 두 용기 중 A에 새 냄새

- 내용 해시: `61b1bb424256eeff3ac710a2a5e6fa2daa14ead37cd23ce1e39fa4d2d55dbb37`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 두 용기 중 확인된 A에만 품질 변화를 연결해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-hold-0149

### 설계한 시나리오 raw

같은 제품 A와 B 중 확인한 A에서 이전에 없던 냄새가 나요. 지금 확인하는 용기는 A예요. B의 상태는 아직 살펴보지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-a",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "containers": [
          "A",
          "B"
        ],
        "container_b_not_examined": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "A의 새로운 냄새는 확인됐지만 B의 품질은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "같은 제품 A와 B 중 확인한 A에서 이전에 없던 냄새가 나요.",
    "connection": "확인된 품질 변화는 용기 A에 연결돼요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "지금 확인하는 용기는 A예요.",
    "connection": "대상 용기 A를 명시해요."
  },
  {
    "variable_id": "product.identity",
    "raw_span": "B의 상태는 아직 살펴보지 않았어요.",
    "connection": "B에 대한 품질은 미상이므로 A의 판단을 이전하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
용기 A의 새로운 냄새 때문에 개별 권고를 보류해요 [kb:B-S04@0.6.1]. B는 상태를 확인하지 않아 같은 판단을 적용하지 않아요.

### 필요한 다음 단계
A 사용을 중단하고 해당 용기의 표시와 이력을 확인해 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0188 — 새 분리 이후 이미 사용

- 내용 해시: `13f4dee4825fdc59e9737051bb16821d49bc59435577f8c98b36d560e07ac640`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 품질 변화 후 사용 이력이 있어도 원인이나 결과는 단정하지 않아요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-hold-0006

### 설계한 시나리오 raw

제품이 원래와 달리 층이 분리됐어요. 분리된 상태에서 이미 사용했어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "separation": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "used_after_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 분리와 그 후의 실제 사용이 보고돼 품질 확인이 필요해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "제품이 원래와 달리 층이 분리됐어요.",
    "connection": "평소와 다른 분리를 확인해요."
  },
  {
    "variable_id": "storage.handling",
    "raw_span": "분리된 상태에서 이미 사용했어요.",
    "connection": "변화 뒤 이미 사용한 이력을 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품의 새로운 분리와 그 이후 사용 이력이 있어 개별 루틴 안내를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 추가 사용을 중단하고 표시와 제형 정보를 제조·판매처에 확인해 주세요. 이 이력만으로 원인이나 결과를 단정하지 않아요.

## syn-hold-0189 — A 품질 변화와 B 기한 정보 분리

- 내용 해시: `3dee3920b98293b802a0c8d870ff34e4616d98eee46360d7ae874215a12ddb67`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0138은 동일 용기의 기한 내 품질 변화이나, 이 합성 대체는 A의 색 변화·A 기한 미상·B 기한 잔여를 분리해요. / syn-hold-0138

### 설계한 시나리오 raw

A 용기의 제품 색이 전과 달라졌어요. A의 표시 기한은 확인하지 못했어요. 같은 제품 B 용기는 표시 기한이 남았지만 B의 내용물 상태는 보지 않았어요. 변화가 보고된 용기는 A예요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "containers": [
          "A",
          "B"
        ],
        "container_b_within_expiry": true,
        "container_b_sensory_unchecked": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-a",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화는 일반 루틴과 분리해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "A 용기의 제품 색이 전과 달라졌어요.",
    "connection": "A에서만 확인한 색 변화를 기록해요."
  },
  {
    "variable_id": "storage.expiry",
    "raw_span": "A의 표시 기한은 확인하지 못했어요.",
    "connection": "A의 표시 기한은 미상이에요."
  },
  {
    "variable_id": "product.identity",
    "raw_span": "같은 제품 B 용기는 표시 기한이 남았지만 B의 내용물 상태는 보지 않았어요.",
    "connection": "B의 기한과 미확인 품질을 A의 정보로 옮기지 않아요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "변화가 보고된 용기는 A예요.",
    "connection": "품질 변화와 A를 연결해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
A 용기의 색 변화로 개별 제품 안내를 보류해요 [kb:B-S04@0.6.1]. B의 기한이 남은 사실은 A의 기한이나 품질을 알려 주지 않아요.

### 필요한 다음 단계
A의 사용을 중단하고 A의 표시와 변화 이력을 확인해 필요하면 제조·판매처에 문의해 주세요. B의 내용물 상태와 A의 기한은 미상이에요.

## syn-hold-0190 — 새 냄새와 사용 중단

- 내용 해시: `130de3a9026691cce27bc1bb98ef4b0e46f16030fb006104d32dfd9cd32b09d4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 사용 중단 후 대체 제품 요청에도 일반 추천을 보류해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-hold-0036

### 설계한 시나리오 raw

제품에서 평소 없던 냄새가 나요. 그 제품은 현재 사용을 멈췄어요. 대신 쓸 제품을 추천받고 싶어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "currently_stopped": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "alternative_product"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 냄새가 있는 제품에 대한 품질 확인 전 개별 제품 추천은 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "제품에서 평소 없던 냄새가 나요.",
    "connection": "새 냄새를 확인해요."
  },
  {
    "variable_id": "storage.handling",
    "raw_span": "그 제품은 현재 사용을 멈췄어요.",
    "connection": "현재 해당 제품을 사용하지 않아요."
  },
  {
    "variable_id": "constraints.goals",
    "raw_span": "대신 쓸 제품을 추천받고 싶어요.",
    "connection": "대체 추천 요청을 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품에 새 냄새가 생겨 대체 제품을 포함한 개별 추천을 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이미 사용을 멈춘 해당 제품의 표시와 이력을 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0191 — 지속 얼굴 불편과 제품 목록 거절

- 내용 해시: `3d1e315880dccf861771607a0d09e4cde8bc77e785b0591969fa320d9f0621b6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0001의 지속 불편과 달리 친구의 부정 및 사용자 제품 목록 거절을 함께 보존하고 상담을 목록 제출에 종속시키지 않아요. / syn-hold-0001

### 설계한 시나리오 raw

제 얼굴 불편감이 계속돼요. 친구는 눈이 아프지 않다고 했어요. 제가 쓰는 제품 목록은 말하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "other_subject_eye_pain_absent": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "제 얼굴 불편감이 계속돼요.",
    "connection": "본인의 지속 불편을 확인해요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "제 얼굴 불편감이 계속돼요.",
    "connection": "본인의 증상 부위를 얼굴로 확인해요."
  },
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "친구는 눈이 아프지 않다고 했어요.",
    "connection": "친구의 눈 상태를 본인 증상으로 옮기지 않아요."
  },
  {
    "variable_id": "constraints.available_products",
    "raw_span": "제가 쓰는 제품 목록은 말하고 싶지 않아요.",
    "connection": "본인의 제품 목록 답변을 거절해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
본인의 얼굴 불편이 계속되어 개별 루틴과 제품 안내를 보류해요 [kb:B-B01@0.6.1]. 친구의 눈 통증 부정은 본인의 상태가 아니에요.

### 필요한 다음 단계
제품 목록을 밝히고 싶지 않다는 선택을 존중하며, 지속되는 얼굴 불편과 경과에 관해 전문가의 확인을 받아 주세요.

## syn-hold-0192 — 얼굴 증상과 머리 제품 접촉

- 내용 해시: `97b528ecb56b7707a0e3462df977c15a29da2418a9b37123448741dc67fee344`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0001과 달리 머리 제품의 얼굴 접촉을 실제로 확인하지만 어느 제품이 원인인지는 미상으로 유지해요. / syn-hold-0001

### 설계한 시나리오 raw

얼굴 불편감이 계속되고 있어요. 머리 제품이 그 얼굴 부위에 실제 닿았지만 어떤 제품이 원인인지는 몰라요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "environment.indirect_products": {
      "variable_id": "environment.indirect_products",
      "state": "known",
      "value": {
        "hair_product_touched_symptom_site": true,
        "product_cause_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴 불편감이 계속되고 있어요.",
    "connection": "지속되는 본인의 불편이에요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴 불편감이 계속되고 있어요.",
    "connection": "증상 부위는 얼굴이에요."
  },
  {
    "variable_id": "environment.indirect_products",
    "raw_span": "머리 제품이 그 얼굴 부위에 실제 닿았지만 어떤 제품이 원인인지는 몰라요.",
    "connection": "실제 얼굴 접촉과 제품별 원인 미상을 접촉 맥락에 분리해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 권고를 보류해요 [kb:B-B01@0.6.1]. 머리 제품의 얼굴 접촉과 불편의 원인은 별개의 문제예요.

### 필요한 다음 단계
머리 제품이 닿은 사실과 증상 경과를 전문가에게 설명하고 확인받아 주세요. 어느 제품이 원인인지 단정하지 않아요.

## syn-hold-0193 — 제품 중단 뒤 지속 얼굴 불편

- 내용 해시: `2a3967f7165af18f8db4505674650e375d04e0ac01a6ff1ca05371216b07020c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0117과 같은 중단 후 지속 증상 가족이나 새 제품 선택 대신 중단한 동일 제품의 재사용을 묻고 이전 재도포 이력은 미상이에요. / syn-hold-0117

### 설계한 시나리오 raw

얼굴에 불편함이 계속돼요. 그 전에 쓰던 선제품은 이미 중단했지만 다시 써도 될지 궁금해요. 중단 전 재도포 여부는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_stopped": true,
        "resume_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴에 불편함이 계속돼요.",
    "connection": "얼굴의 지속 불편이에요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴에 불편함이 계속돼요.",
    "connection": "본인의 증상 부위를 확인해요."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "그 전에 쓰던 선제품은 이미 중단했지만 다시 써도 될지 궁금해요.",
    "connection": "이전에 쓰던 제품은 실제 중단됐고 재사용은 질문일 뿐이에요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "중단 전 재도포 여부는 기억나지 않아요.",
    "connection": "중단 전 재도포 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
선제품을 중단한 뒤에도 얼굴 불편이 계속되어 해당 제품의 재사용을 포함한 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
제품 중단 시점과 지속되는 불편을 전문가에게 설명해 주세요. 중단 전 재도포 여부는 기억나지 않는 상태예요.

## syn-hold-0194 — 최근 시술과 타인의 눈 상태

- 내용 해시: `55182100f2592506d5c74cc13d14b192af966ee9f90cbc53807f4b1a02ed32ce`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0001의 지속 불편에 최근 시술의 실제 이력과 관련성 미상, 타인 눈 상태를 분리하는 상담 맥락을 추가한 새 합성이에요. / syn-hold-0001

### 설계한 시나리오 raw

제 피부 불편감은 계속되고 있어요. 최근 피부 시술을 받았지만 불편과의 관련성은 몰라요. 친구는 눈이 편해졌다고 해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.recent_procedure": {
      "variable_id": "person.recent_procedure",
      "state": "known",
      "value": {
        "recent_procedure_reported": true,
        "relationship_to_discomfort_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "other_subject_reports_eye_comfort": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "제 피부 불편감은 계속되고 있어요.",
    "connection": "본인의 불편이 지속돼요."
  },
  {
    "variable_id": "person.recent_procedure",
    "raw_span": "최근 피부 시술을 받았지만 불편과의 관련성은 몰라요.",
    "connection": "시술이 있었으나 증상과의 관련성은 미상이에요."
  },
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "친구는 눈이 편해졌다고 해요.",
    "connection": "친구의 눈 경험을 본인의 증상에 이전하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
본인의 지속 불편과 별개로 친구가 눈이 편해졌다는 경험을 본인에게 옮기지 않아요. 개별 권고는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
최근 시술 이력과 불편이 이어진 경과를 전문가에게 알려 확인받아 주세요. 시술과 불편의 관련성은 미상이에요.

## syn-hold-0195 — 통증 부정과 예정 진료

- 내용 해시: `d7f4c87d12086e5a49c9d147a6a36c76f701da7093b94c5353aaaef5fd602016`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0037의 진료 취소 질문에 명시적 통증 부정과 지속 얼굴 불편의 분리라는 결정 경계를 더해요. / syn-hold-0037

### 설계한 시나리오 raw

얼굴이 계속 불편해요. 통증은 없어요. 진료가 예정돼 있는데 통증이 없으니 취소해도 되는지 궁금해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "visit_scheduled": true,
        "cancel_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴이 계속 불편해요.",
    "connection": "본인의 지속 불편이에요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴이 계속 불편해요.",
    "connection": "불편 부위는 얼굴이에요."
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "통증은 없어요.",
    "connection": "통증 부정은 지속 불편을 지우지 않아요."
  },
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "진료가 예정돼 있는데 통증이 없으니 취소해도 되는지 궁금해요.",
    "connection": "진료는 예정돼 있고 취소는 질문이에요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
통증은 없다고 하셨지만 얼굴 불편은 계속되어 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
예정된 진료에서 지속 불편과 통증이 없다는 관찰을 함께 말씀해 주세요. 통증 부정만으로 다른 불편이 없다고 판단하지 않아요.

## syn-hold-0196 — 의료진 계획이 있는 새 후보 선택

- 내용 해시: `4e77df505860ab0cecadb569b2da38f49f032700733a375561aab9aafa0a16eb`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0168의 신규 선택과 지속 불편에 현재 의료진 계획 및 그 계획 대신 선택하려는 맥락을 추가해요. / syn-hold-0168

### 설계한 시나리오 raw

피부 불편이 계속되고 있어요. 피부과에서 현재 관리에 관한 개별 계획을 받았어요. 그 계획 대신 새 선제품을 사려고 하지만 아직 사용하지 않았어요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "present": true,
        "replace_plan_with_new_sunscreen_planned": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "new_sunscreen_used": false,
        "selection_planned": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "피부 불편이 계속되고 있어요.",
    "connection": "본인의 불편이 지속돼요."
  },
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "피부과에서 현재 관리에 관한 개별 계획을 받았어요. 그 계획 대신 새 선제품을 사려고 하지만 아직 사용하지 않았어요.",
    "connection": "의료진 계획의 존재와 이를 새 선제품 선택으로 대신하려는 미실행 계획을 연결해요."
  },
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "그 계획 대신 새 선제품을 사려고 하지만 아직 사용하지 않았어요.",
    "connection": "새 후보 선택은 계획이며 실제 사용은 아니에요."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "그 계획 대신 새 선제품을 사려고 하지만 아직 사용하지 않았어요.",
    "connection": "신규 제품 계획과 미사용을 분리해요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
불편이 지속되고 현재 의료진의 개별 계획이 있어 새 제품 선택을 포함한 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편과 새 후보에 관한 질문을 계획을 세운 의료진에게 상담해 주세요. 새 선제품은 아직 사용하지 않은 계획이에요.

## syn-hold-0197 — 지속 얼굴 불편과 A 품질 변화

- 내용 해시: `d4ec9f8ec63494f79175a185c451fa5ff3c70d26bfc2f650aa917b88f6fab945`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 기존 0001의 지속 얼굴 불편과 별도로 A의 새 냄새는 확인됐지만 A가 얼굴에 사용됐는지는 미상이라 증상과 품질 조치를 구분해요. / syn-hold-0001

### 설계한 시나리오 raw

얼굴의 불편이 계속돼요. A 용기에는 평소 없던 냄새가 나요. 변화가 확인된 용기는 A예요. A를 얼굴에 사용했는지 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-a",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    },
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화는 일반 루틴과 분리해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1",
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "얼굴의 불편이 계속돼요.",
    "connection": "본인의 불편이 지속돼요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴의 불편이 계속돼요.",
    "connection": "본인의 증상 부위는 얼굴이에요."
  },
  {
    "variable_id": "storage.sensory_change",
    "raw_span": "A 용기에는 평소 없던 냄새가 나요.",
    "connection": "A의 새로운 냄새가 확인돼요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "변화가 확인된 용기는 A예요.",
    "connection": "품질 변화를 용기 A에 연결해요."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "A를 얼굴에 사용했는지 기억나지 않아요.",
    "connection": "증상과 A의 실제 사용 연결은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되고 별도로 A 용기에서 새로운 색 또는 냄새 변화가 확인돼 개별 루틴과 제품 안내를 보류해요 [kb:B-B01@0.6.1] [kb:B-S04@0.6.1].

### 필요한 다음 단계
A의 사용을 중단하고 품질 변화는 제조·판매처에, 지속 불편은 전문가에게 각각 확인해 주세요. A를 얼굴에 썼는지는 미상이므로 증상 원인으로 단정하지 않아요.

## syn-hold-0198 — 얼굴 불편과 손에만 쓴 제품

- 내용 해시: `867763f16ac68b942dd89509a557bf5c50aa35a5cc700613c718dbf17a2b723c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 친구의 얼굴 사용과 무불편, 본인의 손 사용, 본인의 지속 얼굴 불편을 나누어 타인의 반응이나 본인 사용 부위를 추정하지 않아요. / syn-hold-0001

### 설계한 시나리오 raw

제 얼굴은 계속 불편해요. 저는 그 제품을 손에만 썼어요. 친구는 같은 제품을 얼굴에 쓰고 불편이 없다고 해요.

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "symptom_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "hands",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "other_person_face_product_no_discomfort": true,
        "self_product_hands_only": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편에 대한 개별 루틴과 제품 안내는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "제 얼굴은 계속 불편해요.",
    "connection": "본인의 얼굴 불편이 지속돼요."
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "제 얼굴은 계속 불편해요.",
    "connection": "본인의 증상 부위를 얼굴로 확인해요."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "저는 그 제품을 손에만 썼어요.",
    "connection": "본인의 제품 사용 부위는 손이며 얼굴 증상 부위와 달라요."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "저는 그 제품을 손에만 썼어요. 친구는 같은 제품을 얼굴에 쓰고 불편이 없다고 해요.",
    "connection": "본인의 사용은 손으로 한정되고 친구의 얼굴 사용과 경험은 별개예요."
  }
]
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
본인의 얼굴 불편이 계속되어 개별 권고를 보류해요 [kb:B-B01@0.6.1]. 친구의 얼굴 사용 경험은 본인의 반응이 아니에요.

### 필요한 다음 단계
본인은 해당 제품을 손에만 썼다는 사실과 얼굴 불편의 경과를 전문가에게 설명해 주세요. 제품을 본인의 얼굴에 썼다고 추정하지 않아요.

## syn-sol-0499 — 시간대별 수온과 손 세정

- 내용 해시: `b8929f892e8ea81743496428b324737f626adec01852543e4cb0671f775a48b9`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 저녁 물 온도 차이와 아침의 미상 및 건조 방식 미확인을 분리한다. / syn-sol-0013, syn-sol-0001

### 설계한 시나리오 raw

저녁에는 얼굴을 뜨겁게 느껴지는 물로 씻고, 손가락으로 부드럽게 세정해요. 아침 물 온도는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "evening": "hot",
        "morning": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "저녁의 뜨거운 물은 미온수 기본과 달라요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "건조 방식은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Lukewarm water and fingertips are suggested for facial cleansing. Avoid scrubbing and pat the skin dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "저녁에는 얼굴을 뜨겁게 느껴지는 물로 씻고",
    "connection": "저녁 수온 보고이며 아침 온도는 별도로 미상이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "아침 물 온도는 기억나지 않아요",
    "connection": "아침 수온을 미상으로 보존한다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "손가락으로 부드럽게 세정해요",
    "connection": "실제 세정에 사용한 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "손가락으로 부드럽게 세정해요",
    "connection": "세정 중 마찰 강도다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
저녁에는 뜨겁게 느껴지는 물 대신 미온수를 사용해 보세요 [kb:B-C01@0.6.1].

### 근거 및 이유
손가락으로 부드럽게 씻은 점은 확인됐고 저녁에는 뜨겁게 느껴지는 물을 사용했어요 [kb:B-C01@0.6.1].

### 확인이 필요한 한계
건조 방식은 확인되지 않았고 아침 수온도 미상이므로 저녁과 같다고 가정하지 않아요 [kb:B-C02@0.6.1].

## syn-sol-0500 — 찬물과 건조 마찰

- 내용 해시: `349e24d75adf77855753afd8f7a894be5b33a9e4b4a132334ed932b42c85aa53`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 찬물을 위험으로 분류하지 않으면서 강한 건조 마찰과 세정 도구 미상을 분리한다. / syn-sol-0198

### 설계한 시나리오 raw

찬물로 얼굴을 헹구고 수건으로 물기를 세게 문질러 닦아요. 세정할 때 무엇을 썼는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "cold",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "strong_towel_rubbing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "찬물은 뜨거운 물 차이로 판정하지 않아요."
    },
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "물기를 수건으로 강하게 비비는 건조 방식이 확인돼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use lukewarm water for facial cleansing and pat the skin dry. Avoid scrubbing the skin.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "찬물로 얼굴을 헹구고",
    "connection": "헹굼에 사용한 물의 체감이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "수건으로 물기를 세게 문질러 닦아요",
    "connection": "건조할 때의 마찰이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "세정할 때 무엇을 썼는지는 기억나지 않아요",
    "connection": "세정 도구를 알 수 없다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
수건으로 세게 비비는 대신 물기를 가볍게 눌러 닦아 보세요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 세안 안내는 미온수와 부드러운 건조를 제시해요 [ref:S03].

### 확인이 필요한 한계
찬물만으로 위험을 판정하지 않고 세정 도구도 기억나지 않아요 [kb:B-C01@0.6.1].

## syn-sol-0501 — 손 세정과 미온수

- 내용 해시: `c5e9b554bed9ab9128f49fd8a79ff2f7bc33a5ea1235e417e35fb145215ceb57`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 손가락 사용·부드러운 세정·건조 방식과 수온을 모두 확인한다. / syn-sol-0001, syn-sol-0037

### 설계한 시나리오 raw

얼굴을 손가락으로 가볍게 씻어요. 물은 뜨겁지 않은 미온수이고 수건도 톡톡 눌러요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "미온수로 세안해요."
    },
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "손가락으로 부드럽게 씻고 가볍게 눌러 말려요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Wash with lukewarm water and fingertips without scrubbing. Gently pat the skin dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "물은 뜨겁지 않은 미온수이고",
    "connection": "본인의 사용 수온이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "얼굴을 손가락으로 가볍게 씻어요",
    "connection": "사용한 세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "얼굴을 손가락으로 가볍게 씻어요",
    "connection": "세정 중 강도다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "수건도 톡톡 눌러요",
    "connection": "물기를 닦는 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 미온수와 손가락을 이용한 부드러운 세정, 가볍게 누르는 건조 방식을 유지할 수 있어요 [kb:B-C01@0.6.1] [kb:B-C02@0.6.1].

### 근거 및 이유
일반 얼굴 세안 안내도 손가락과 부드러운 건조를 다뤄요 [ref:S03].

### 확인이 필요한 한계
이 항목의 일치가 제품 전체의 적합성을 보장하는 것은 아니에요.

## syn-sol-0502 — 브러시와 수건 사용 분리

- 내용 해시: `4d547e309d2b2a7315d03ab1be69f43d7ad61ed8f3203eef35625628ea566552`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 세정 도구, 부드러운 움직임과 강한 건조 마찰을 구분한다. / syn-sol-0037, syn-sol-0198

### 설계한 시나리오 raw

세정 브러시를 써요. 움직임은 부드럽지만 물기를 닦을 때는 수건으로 세게 비벼요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "cleansing_brush"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "strong_towel_rubbing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "손가락 외 도구 사용과 강한 수건 마찰이 각각 확인돼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Facial cleansing guidance favors fingertips and avoiding scrubbing. Pat the skin dry rather than rubbing it.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.tools",
    "raw_span": "세정 브러시를 써요",
    "connection": "실제로 사용하는 세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "움직임은 부드럽지만",
    "connection": "브러시 움직임의 강도다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "물기를 닦을 때는 수건으로 세게 비벼요",
    "connection": "건조 때 수건 마찰 강도다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
건조할 때 수건으로 비비는 대신 가볍게 눌러 보세요 [kb:B-C02@0.6.1].

### 근거 및 이유
브러시 사용은 손가락 외 도구라는 별도 차이이고 세정 중 움직임은 부드럽다고 했어요.

### 확인이 필요한 한계
도구 사용만으로 강한 세정 마찰을 추정하지 않으며 일반 안내는 손가락과 부드러운 건조를 권해요 [ref:S03].

## syn-sol-0503 — 도구 사용 응답 거절

- 내용 해시: `78fcf2acf8a0be0d281ee88ea0924e24429b62187909832399c9a077e57c928b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 도구 보유와 실제 사용 여부 응답 거절, 별도로 확인된 건조를 분리한다. / syn-sol-0047

### 설계한 시나리오 raw

클렌징 패드를 가지고 있지만 얼굴에 사용했는지는 말하고 싶지 않아요. 세안 후 수건으로는 가볍게 눌러 닦아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "owns_cleansing_pad": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "보유한 패드의 사용 여부를 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Facial cleansing guidance recommends fingertips and avoiding scrubbing. Gently pat the face dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "클렌징 패드를 가지고 있지만",
    "connection": "보유 사실만 확인한다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "얼굴에 사용했는지는 말하고 싶지 않아요",
    "connection": "실제 사용 여부에 대한 응답 거절이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "세안 후 수건으로는 가볍게 눌러 닦아요",
    "connection": "확인된 건조 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 가벼운 수건 건조는 유지할 수 있어요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 얼굴 세안 안내는 손가락 사용과 부드러운 건조를 다뤄요 [ref:S03].

### 확인이 필요한 한계
패드 보유만으로 실제 사용을 판단하지 않아요. 사용 여부는 답변을 원하지 않으셨고 세정 방법 전체의 일치 여부는 미상이에요.

## syn-sol-0504 — 오래 문지르는 세정

- 내용 해시: `3b2eff95715caca41136774beb48117f618af9456b2141ef5a71c1e9bbcdc2d2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 시간 숫자 대신 오래 문지르는 행위와 별도 지시 부재를 확인하고 마찰 강도 및 의도 미보고를 분리한다. / syn-sol-0192, syn-sol-0030

### 설계한 시나리오 raw

씻어내는 세정제를 오래 문질러요. 해당 제품에 따로 접촉시간을 정한 지시는 없고 세게 문지르지는 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "specific_contact_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "rubs_for_long_time": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "별도 접촉 지시 없이 오래 문질러요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "씻어내는 세정제를",
    "connection": "실제 세정제 유형이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "오래 문질러요",
    "connection": "오래 문지르는 실제 행위이며 의도는 보고되지 않았다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "해당 제품에 따로 접촉시간을 정한 지시는 없고",
    "connection": "별도 접촉시간 지시가 없다는 보고다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "세게 문지르지는 않아요",
    "connection": "세정 중 강한 마찰에 대한 명시적 부정이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
별도 접촉시간 지시가 없다면 세정제를 오래 문지르는 방식을 줄여 보세요 [kb:B-C03@0.6.1].

### 근거 및 이유
세게 문지르지 않는다는 보고와 오래 문지르는 시간은 서로 다른 사실이에요.

### 확인이 필요한 한계
특정 초를 임의로 정하거나 이 행동이 현재 피부 상태의 원인이라고 단정하지 않아요.

## syn-sol-0505 — 접촉 지시 미확인

- 내용 해시: `4cc04a6a9f10b76ecddaac6ab10316758c5e543f4fe6db4175cbd6dc6a81360a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 짧고 부드러운 사용은 확인하되 지시 일치 여부는 미확인으로 남긴다. / syn-sol-0030, syn-sol-0039

### 설계한 시나리오 raw

씻어내는 세정제를 짧게 부드럽게 사용해요. 그 제품의 접촉시간 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "brief_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "제품 접촉시간 지시는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "씻어내는 세정제를",
    "connection": "사용 제품 유형이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "짧게 부드럽게 사용해요",
    "connection": "짧게 사용한 행위다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "짧게 부드럽게 사용해요",
    "connection": "사용 강도가 부드럽다는 보고다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "그 제품의 접촉시간 지시는 확인하지 못했어요",
    "connection": "지시가 없는 것이 아니라 미확인이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
짧고 부드러운 사용은 확인되지만 제품의 접촉시간 지시와 일치하는지는 아직 판단하지 않아요 [kb:B-C03@0.6.1].

### 근거 및 이유
제품별 접촉 지시의 확인 여부가 실제 사용과의 일치 판단에 필요해요 [kb:B-C03@0.6.1].

### 확인이 필요한 한계
지시를 확인하지 못한 것은 별도 지시가 없다는 뜻이 아니에요. 필요하면 해당 제품의 표시를 확인해 주세요.

## syn-sol-0506 — 현재 제품 pH 미상과 뜨거운 세안수

- 내용 해시: `1ff545b747e59831696c0285a9729598218fb4041191a75c4171a01c4e8f0247`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 0357의 장시간 방치 사례를 대체한 신규 합성: 현재 제품 pH 미상과 실제 뜨거운 수온을 서로 다른 판단축으로 결합한다. / syn-sol-0007, syn-sol-0013

### 설계한 시나리오 raw

지금 쓰는 얼굴 세정제의 pH는 모르겠어요. 현재 불편은 없지만 세안할 때 물은 뜨겁게 느껴져요. 현재 루틴을 검토해 주세요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "hot",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "얼굴을 뜨겁게 느껴지는 물로 씻어요."
    },
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "현재 세정제 pH가 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Facial cleansing guidance suggests lukewarm water and avoiding scrubbing. Dry the skin gently after washing.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C04@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "현재 루틴을 검토해 주세요",
    "connection": "현재 루틴 검토 요청이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴 세정제",
    "connection": "보고된 얼굴 세정 맥락이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "세안할 때 물은 뜨겁게 느껴져요",
    "connection": "본인의 실제 세안수 체감이다."
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "현재 불편은 없지만",
    "connection": "현재 불편 부정이다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "얼굴 세정제의 pH는 모르겠어요",
    "connection": "pH 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
뜨겁게 느껴지는 세안수는 미온수로 바꿔 볼 수 있어요 [kb:B-C01@0.6.1]. 현재 세정제의 pH는 확인되지 않았어요 [kb:B-C04@0.6.1].

### 근거 및 이유
미온수 사용은 일반 얼굴 세안 안내의 한 항목이에요 [ref:S03]. 현재 불편이 없다는 보고와 세안수 온도는 별개예요.

### 확인이 필요한 한계
pH를 모른다는 이유만으로 제품을 즉시 교체해야 한다고 단정하지 않아요. 물 온도가 불편의 원인이라고 추정하지도 않아요.

## syn-sol-0507 — 헹굼 여부 기억 불가

- 내용 해시: `9f5f0be40866243dfd4e06c9dc6b2399201759977284eea445ce88d56109d94d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 요구와 실행 미상을 구별하고 손 세정 강도만으로 건조를 추정하지 않는다. / syn-sol-0038

### 설계한 시나리오 raw

씻어내라고 표시된 세정제를 썼어요. 물로 헹궜는지는 기억나지 않고 손가락으로 부드럽게 씻은 것은 기억나요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "필요한 헹굼의 실행 여부가 미상이에요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "건조 방법은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "씻어내라고 표시된 세정제를 썼어요",
    "connection": "사용한 씻어내는 세정제다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "씻어내라고 표시된",
    "connection": "제품의 헹굼 지시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 헹궜는지는 기억나지 않고",
    "connection": "실제 헹굼 여부 미상이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "손가락으로 부드럽게 씻은 것은 기억나요",
    "connection": "실제 세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "손가락으로 부드럽게 씻은 것은 기억나요",
    "connection": "세정 중 강도다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
이 제품은 씻어내라는 표시가 있지만 실제 헹궜는지는 기억나지 않아 실행 여부를 판정할 수 없어요 [kb:B-C06@0.6.1].

### 근거 및 이유
씻어내라는 제품 표시와 손가락을 이용한 부드러운 세정은 확인됐어요 [kb:B-C06@0.6.1].

### 확인이 필요한 한계
헹굼 여부는 기억나지 않고 물기 건조 방법도 별도로 미상이에요 [kb:B-C02@0.6.1]. 이후 사용할 때는 해당 표시를 확인해 주세요.

## syn-sol-0508 — 무헹굼 표시와 건조 마찰

- 내용 해시: `2491174617b56a58716436c4c26205feb5f8aa7ebefbff82ee2d092c1cc819b4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 무헹굼 제품의 예외와 별개의 강한 건조 마찰을 구분한다. / syn-sol-0055, syn-sol-0198

### 설계한 시나리오 raw

물로 헹굴 필요가 없다고 표시된 세정제를 쓰고 물로 헹구지 않았어요. 건조할 때는 수건으로 세게 문질렀어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "no_rinse_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "water_rinse_required": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "strong_towel_rubbing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "exception",
      "guidance": "물 헹굼이 필요 없다는 제품 표시가 있어요."
    },
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "건조할 때 수건으로 세게 문질러요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Avoid scrubbing when washing the face. Gently pat the skin dry after washing.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "물로 헹굴 필요가 없다고 표시된 세정제",
    "connection": "무헹굼 표시 제품이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "물로 헹굴 필요가 없다고 표시된",
    "connection": "물 헹굼 불필요 표시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 헹구지 않았어요",
    "connection": "실제 물 헹굼을 하지 않았다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "건조할 때는 수건으로 세게 문질렀어요",
    "connection": "건조 시 마찰이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
이 제품에는 물 헹굼이 필요 없다는 표시가 있으므로 미헹굼만으로 표시 이탈로 판단하지 않아요 [kb:B-C06@0.6.1]. 수건은 세게 비비지 말고 가볍게 눌러 보세요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 얼굴 관리 안내는 문지르지 않고 부드럽게 건조하는 방법을 다뤄요 [ref:S03].

### 확인이 필요한 한계
헹굼 조건과 건조 마찰은 별개의 판단이며 무헹굼 표시는 다른 제품에 일반화할 수 없어요.

## syn-sol-0509 — 제품 지시에 따른 후속 세정과 찬물

- 내용 해시: `942cb128d52eba5e02f0706302400bded59a0a9c138bbe06f7ff56f339ac94d9`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 0019 발한 예외를 대체한 신규 합성: 제품별 후속 세정 지시 이행과 찬물 체감을 별도 판단한다. / syn-sol-0129

### 설계한 시나리오 raw

얼굴 제거 제품 표시에는 후속 세정제를 쓰라고 되어 있어 그대로 두 단계로 씻어요. 헹굴 때 물은 차갑게 느껴져요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 2,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "subsequent_cleanser_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "follows_subsequent_cleansing_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "cold",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "exception",
      "guidance": "제거 제품의 후속 세정 지시에 따라 두 단계로 사용해요."
    },
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "찬물을 사용했다는 사실만으로 뜨거운 물 차이를 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴 제거 제품",
    "connection": "제품 사용 부위다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "표시에는 후속 세정제를 쓰라고 되어 있어",
    "connection": "표시된 후속 세정 지시다."
  },
  {
    "variable_id": "cleansing.steps",
    "raw_span": "그대로 두 단계로 씻어요",
    "connection": "실제 두 세정 단계다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "후속 세정제를 쓰라고 되어 있어 그대로",
    "connection": "표시된 후속 세정의 이행이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "헹굴 때 물은 차갑게 느껴져요",
    "connection": "헹굼 수온 체감이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 제거 제품에 후속 세정 지시가 있고 그에 따라 두 단계로 사용한 상황은 단계 수만으로 불필요한 반복이라 보지 않아요 [kb:B-C05@0.6.1]. 찬물 사용만으로 뜨거운 물 차이를 판정하지 않아요 [kb:B-C01@0.6.1].

### 근거 및 이유
제품별 지시는 세정 단계의 목적을 검토할 때 고려할 수 있어요. 헹굼 때의 수온 체감은 후속 세정 지시와 다른 정보예요.

### 확인이 필요한 한계
이 제품의 지시를 다른 제품에도 적용할 수 있다고 가정하지 않아요. 찬물이라는 보고만으로 피부 상태나 위해를 판단하지 않아요.

## syn-sol-0510 — 이유 없는 저녁 반복 세정

- 내용 해시: `5586853e2569536ff4949a911f1c01c521bca8e56cf4ffdaccde46f465f2e665`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 두 번째 단계 목적이 미상인 사례와 달리 습관적 반복과 추가 오염 부재가 확인된다. / syn-sol-0129

### 설계한 시나리오 raw

저녁에 한 번 세정한 뒤에도 별다른 오염이나 메이크업 없이 습관적으로 같은 세정제를 다시 써요. 단계는 두 번이에요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 2,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "habitual_reasonless_repetition": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "additional_soiling": false,
        "makeup": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "difference",
      "guidance": "추가 제거 이유 없이 같은 세정제를 습관적으로 반복해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Facial cleansing guidance includes washing after sweating. Avoid scrubbing and gently pat the face dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "cleansing.steps",
    "raw_span": "단계는 두 번이에요",
    "connection": "해당 세안의 단계 수다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "습관적으로 같은 세정제를 다시 써요",
    "connection": "습관적 반복 사용이다."
  },
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "별다른 오염이나 메이크업 없이",
    "connection": "보고된 추가 오염과 메이크업 부재다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
첫 세정 뒤 별다른 추가 제거 목적 없이 습관적으로 같은 제품을 다시 쓰는 단계를 줄일 여지를 살펴보세요 [kb:B-C05@0.6.1].

### 근거 및 이유
추가 오염과 메이크업이 없다는 보고에 따른 판단이에요.

### 확인이 필요한 한계
땀을 흘린 뒤처럼 별도 세정 목적이 있는 경우와 구별해야 해요 [ref:S03].

## syn-sol-0511 — 물세안과 반복 미상

- 내용 해시: `ee6a58e6bc05bb05d9035fc00a0db7170b0a3189dc32d8c9543c54240fd9bf60`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 아침 물세안과 저녁 제품 사용은 확인하지만 저녁 반복 여부는 미상이다. / syn-sol-0061

### 설계한 시나리오 raw

아침에는 물로 씻고 저녁에는 세정제를 써요. 저녁 세정제를 두 번 쓰는지 기억이 나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "known",
      "value": {
        "morning_water_wash": true,
        "evening_cleanser_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "저녁 세정제 반복 여부를 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 무향 핸드크림이나 연고를 바르는 관리법이 있어요. 이는 손 관리에 관한 내용이에요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.frequency",
    "raw_span": "아침에는 물로 씻고 저녁에는 세정제를 써요",
    "connection": "물세안과 세정제 세안의 시간대를 구별한다."
  },
  {
    "variable_id": "cleansing.repeat_wash",
    "raw_span": "저녁 세정제를 두 번 쓰는지 기억이 나지 않아요",
    "connection": "저녁 반복 사용 여부가 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
아침 물세안과 저녁 세정제 사용을 별개로 기록하고, 저녁에 제품을 반복 사용했는지는 미상으로 두어요 [kb:B-C05@0.6.1].

### 근거 및 이유
서로 다른 시간대의 세안만으로 한 번의 세안에서 제품을 반복했다고 판단할 수 없어요.

### 확인이 필요한 한계
필요할 때 저녁 사용 단계를 확인해 주세요.

## syn-sol-0512 — 헹굼과 추가 세정 구분

- 내용 해시: `b628198edd4c454671ed953b30cd9f6453ea67953cc51ef36119723aef63d565`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 물 헹굼과 추가 세정제 사용 여부를 분리하며 제품 지시는 미상이다. / syn-sol-0129, syn-sol-0284

### 설계한 시나리오 raw

메이크업 제거용 세정제 뒤에 물로 한 번 헹궈요. 이후 다른 세정제를 또 썼는지는 기억나지 않아요. 제품의 헹굼 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "makeup_remover",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "후속 세정제 사용은 확인되지 않았어요."
    },
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "제품의 헹굼 지시가 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "kb:B-C06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "메이크업 제거용",
    "connection": "제거 대상이다."
  },
  {
    "variable_id": "product.type",
    "raw_span": "메이크업 제거용 세정제",
    "connection": "사용 제품 유형이다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 한 번 헹궈요",
    "connection": "헹굼 행위다."
  },
  {
    "variable_id": "cleansing.repeat_wash",
    "raw_span": "이후 다른 세정제를 또 썼는지는 기억나지 않아요",
    "connection": "추가 세정제 사용 여부 미상이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품의 헹굼 지시는 확인하지 못했어요",
    "connection": "제품별 지시가 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
메이크업 제거 후 물로 헹군 사실과 다른 세정제를 추가했는지는 구분해요. 후자의 여부는 기억나지 않아 반복 필요성을 판정하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
물로 헹구는 행위 자체는 추가 세정제 단계와 달라요 [kb:B-C05@0.6.1].

### 확인이 필요한 한계
추가 세정제 사용과 제품별 헹굼 지시는 미확인이므로 표시와 실제 사용을 확인해야 해요 [kb:B-C06@0.6.1].

## syn-sol-0513 — 내수성 표시만으로 세 단계

- 내용 해시: `6eed067826c5b3ddacb037b4c7e3354ed0218dffbb5057a961761823afd62dc0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 내수성 표시만으로 자동 반복한다는 조건과 건조 방식을 분리한다. / syn-sol-0002

### 설계한 시나리오 raw

내수성 표시가 있는 선크림을 바른 날엔 표시만 보고 늘 세 단계로 세안해요. 세정 후에는 가볍게 물기를 눌러요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 3,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "내수성 표시만 보고 자동으로 세 단계 세안해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "A small study compared removal of tested sunscreens using different cleansing methods. Its findings do not establish a universal multi-step requirement.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.water_resistance",
    "raw_span": "내수성 표시가 있는 선크림",
    "connection": "표시된 제품 특성이다."
  },
  {
    "variable_id": "cleansing.steps",
    "raw_span": "늘 세 단계로 세안해요",
    "connection": "세안 단계 수다."
  },
  {
    "variable_id": "cleansing.repeat_wash",
    "raw_span": "표시만 보고 늘 세 단계로 세안해요",
    "connection": "내수성 표시만에 따른 자동 반복이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "세정 후에는 가볍게 물기를 눌러요",
    "connection": "세정 후 건조 방식이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
내수성 표시만을 이유로 항상 세 단계로 세정하는 습관은 재검토해 보세요 [kb:B-I01@0.6.1]. 선크림 사용을 줄이는 대신 해당 제품의 제거 지시를 확인하는 것이 중요해요.

### 근거 및 이유
제한된 제품 비교에서 제거 결과는 시험한 제품과 세정 방법에 따라 검토됐어요 [ref:S08].

### 확인이 필요한 한계
소규모 연구는 모든 내수성 제품에 다단계 세안이 필요하다고 확정하지 않아요. 가벼운 건조 방식은 별개의 사실이에요.

## syn-sol-0514 — 제거 걱정으로 도포량 축소

- 내용 해시: `e88ad7a78371b627731408b000fc99329444107efae986af89f82d97791aefa5`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 자동 반복 세정이 아니라 제거 우려에 따른 도포량 축소를 다룬다. / syn-sol-0002

### 설계한 시나리오 raw

선크림을 지우기 힘들까 봐 얼굴에 아주 조금만 발라요. 그 제품의 제거 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "very_small_amount_due_to_removal_difficulty": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "제거가 걱정되어 선크림을 극소량 발라요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "The tested removal outcomes depended on the sunscreen and cleansing method. The small comparison does not establish one removal method for every product.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "선크림을 지우기 힘들까 봐 얼굴에 아주 조금만 발라요",
    "connection": "제거 우려와 소량 도포의 연결이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "그 제품의 제거 지시는 확인하지 못했어요",
    "connection": "제품 제거 지시 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제거가 걱정된다는 이유로 선크림을 아주 적게 바르는 방식은 재검토해 주세요 [kb:B-I01@0.6.1]. 해당 제품의 제거 지시를 확인하면서 광보호를 유지하는 방향으로 살펴봐요.

### 근거 및 이유
제거가 어렵다는 우려 때문에 선크림 도포량을 줄였다는 보고가 이번 판단의 이유예요 [kb:B-I01@0.6.1].

### 확인이 필요한 한계
제품의 제거 지시는 아직 미상이고 제한된 제품 비교 결과만으로 모든 제품의 제거법을 정할 수 없어요 [ref:S08].

## syn-sol-0515 — 버전 미상의 제거 지시 조회

- 내용 해시: `07bdabaa6ea6e87c09ffa7f35c173ea03e534d9e6341dc3eee7b0abccf6db978`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 확인 계획과 실제 제거법은 다르며 제품 버전도 미상이다. / syn-sol-0025

### 설계한 시나리오 raw

선크림을 평소 양대로 바르고 제품에 적힌 제거법을 보려 해요. 현재 제품의 버전은 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_used": true,
        "amount": "usual",
        "intends_to_check_removal_instructions": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "현재 제품 버전과 해당 제거 지시는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림을 평소 양대로 바르고 제품에 적힌 제거법을 보려 해요",
    "connection": "도포와 제거법 확인 계획을 분리한 보고다."
  },
  {
    "variable_id": "product.version",
    "raw_span": "현재 제품의 버전은 확인하지 못했어요",
    "connection": "현재 버전 미상이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품에 적힌 제거법을 보려 해요",
    "connection": "제거법 확인은 계획으로 아직 확인된 지시가 아니다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제품에 적힌 제거법을 확인하려는 계획은 아직 확인된 사용법이 아니에요 [kb:B-I01@0.6.1]. 먼저 현재 사용하는 제품 버전을 확인해 주세요.

### 근거 및 이유
평소 양대로 선크림을 바른 사실과 제거법을 확인하려는 계획은 구별해요 [kb:B-I01@0.6.1].

### 확인이 필요한 한계
버전과 제거 지시가 미상이므로 특정 세정법이나 단계 수를 단정할 수 없어요.

## syn-sol-0516 — 새 후보의 pH와 헹굼 표시

- 내용 해시: `62d3d28726bcaa77f1da2ba397844e9b2212d92d90f838b2cd83c7003398a7d6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 후보 pH 미상과 헹굼 지시 확인, 사용 전 상태를 분리한다. / syn-sol-0018, syn-sol-0038

### 설계한 시나리오 raw

새 세정제 후보의 pH 자료는 없어요. 사용 전 제품 표시를 봤는데 씻어내라는 지시는 확인했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "candidate_not_yet_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "후보의 pH 자료가 없어요."
    },
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "사용 전이어서 실제 헹굼은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1",
    "kb:B-C06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "새 세정제 후보",
    "connection": "새 제품 선택 맥락이다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "pH 자료는 없어요",
    "connection": "pH 미확인이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "씻어내라는 지시는 확인했어요",
    "connection": "합성 후보의 헹굼 지시다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "사용 전 제품 표시를 봤는데",
    "connection": "아직 사용 전임을 나타낸다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 후보의 pH 자료가 없으므로 약산성 여부는 미상이에요 [kb:B-C04@0.6.1]. 씻어내라는 표시가 있다는 것과 실제 헹군 경험은 별개예요 [kb:B-C06@0.6.1].

### 근거 및 이유
새 후보의 pH 자료와 헹굼 표시, 실제 사용 여부는 서로 다른 정보예요 [kb:B-C04@0.6.1] [kb:B-C06@0.6.1].

### 확인이 필요한 한계
아직 사용 전이므로 표시 이행 여부는 판단하지 않아요. pH 자료가 없다는 것만으로 부적합이나 성능을 확정할 수 없어요.

## syn-sol-0517 — pH 미상과 건조 마찰

- 내용 해시: `1103787ad2dd30db83673a75ce0a569b1208d073df2e61b020a2c5dfd74b10c4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 현재 제품 pH 미상과 증상 부정, 건조 마찰 차이는 별개다. / syn-sol-0007, syn-sol-0198

### 설계한 시나리오 raw

지금 쓰는 세정제의 pH는 몰라요. 현재 불편감은 없고 세안 뒤 수건으로 강하게 비벼요. 현재 루틴을 검토하고 싶어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "strong_towel_rubbing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "현재 세정제의 pH가 확인되지 않았어요."
    },
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "건조 중 수건으로 강하게 비벼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1",
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "현재 루틴을 검토하고 싶어요",
    "connection": "현재 루틴 검토 맥락이다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "지금 쓰는 세정제의 pH는 몰라요",
    "connection": "현재 제품 pH 미상이다."
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "현재 불편감은 없고",
    "connection": "현재 불편의 명시적 부정이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "세안 뒤 수건으로 강하게 비벼요",
    "connection": "건조 시 수건 마찰이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
수건으로 강하게 비비는 대신 가볍게 물기를 눌러 보세요 [kb:B-C02@0.6.1]. 현재 제품의 pH는 확인되지 않았어요 [kb:B-C04@0.6.1].

### 근거 및 이유
현재 불편이 없다는 보고와 건조 방식은 별개예요.

### 확인이 필요한 한계
pH를 모르거나 기본 선호와 다를 가능성만으로 지금 제품을 교체해야 한다고 단정하지 않아요.

## syn-sol-0518 — 친구와 본인의 세안수

- 내용 해시: `10f5cedd429dbf5ecd48411a86a93933139407c9c9dd9c05ffa42654dcb6dec5`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 친구의 수온 보고를 본인에게 이전하지 않고 건조와 세정 방법을 구별한다. / syn-sol-0001

### 설계한 시나리오 raw

친구가 세안수가 뜨겁다고 했지만 제 얼굴 세안수는 미온수예요. 저는 세안 뒤 수건으로 가볍게 눌러요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "본인은 미온수로 세안해요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "세정 도구와 마찰은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "제 얼굴 세안수는 미온수예요",
    "connection": "본인의 수온이며 친구의 보고가 아니다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "저는 세안 뒤 수건으로 가볍게 눌러요",
    "connection": "본인의 건조 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
본인의 세안수는 미온수로 확인됐어요 [kb:B-C01@0.6.1]. 건조할 때 가볍게 누른 사실도 확인되지만 세정 도구나 마찰 강도는 알 수 없어요 [kb:B-C02@0.6.1].

### 근거 및 이유
친구가 뜨겁다고 한 물을 본인이 사용한 물로 옮겨 판단하지 않아요.

### 확인이 필요한 한계
확인되지 않은 세정 방법은 미상으로 남겨요.

## syn-sol-0519 — 세정 도구 응답 거절

- 내용 해시: `8ec71e315dc1b063ae8a47fede7aa2a8e0cd9a7f6b8ddc7fe00206a343d27191`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 도구 사용 답변 거절과 건조 및 수온 확인을 구분한다. / syn-sol-0047

### 설계한 시나리오 raw

미온수로 얼굴을 씻어요. 세정에 사용한 도구는 답변하고 싶지 않고 수건은 문지르지 않고 눌러요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "미온수를 사용해요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "세정 도구 사용 여부에 대한 답변이 거절됐어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use lukewarm water and fingertips for washing the face. Avoid scrubbing and gently pat dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "미온수로 얼굴을 씻어요",
    "connection": "본인의 수온이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "세정에 사용한 도구는 답변하고 싶지 않고",
    "connection": "도구 응답 거절이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "수건은 문지르지 않고 눌러요",
    "connection": "건조 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
미온수 사용과 수건으로 가볍게 누르는 건조는 확인됐어요 [kb:B-C01@0.6.1] [kb:B-C02@0.6.1].

### 근거 및 이유
일반 얼굴 세안 안내는 손가락과 부드러운 건조를 다뤄요 [ref:S03].

### 확인이 필요한 한계
세정 도구에 대한 답변은 원하지 않으셨으므로 실제 도구 사용 여부를 추측하지 않아요.

## syn-sol-0520 — 뜨거운 수온과 가벼운 건조

- 내용 해시: `773fd92b859772c9c22bba69082675dc4043329f30123611691645eb53ed1d4d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 뜨거운 수온과 헹굼 및 건조 강도를 분리한다. / syn-sol-0013

### 설계한 시나리오 raw

세안할 때 물이 뜨거워요. 제품을 씻어낸 뒤 물기를 세게 문지르지 않고 눌러 닦아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "hot",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "뜨겁게 느껴지는 물을 사용해요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "세정 도구와 세정 중 마찰은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use lukewarm water for facial cleansing. Pat the skin dry rather than rubbing.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "세안할 때 물이 뜨거워요",
    "connection": "본인의 세안수 체감이다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "제품을 씻어낸 뒤",
    "connection": "헹굼 실행 보고다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "물기를 세게 문지르지 않고 눌러 닦아요",
    "connection": "건조 방식이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
뜨겁게 느껴지는 세안수는 미온수로 바꾸어 볼 수 있어요 [kb:B-C01@0.6.1]. 확인된 가벼운 건조는 별도로 유지할 수 있어요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 안내에서도 미온수와 부드러운 건조를 제시해요 [ref:S03].

### 확인이 필요한 한계
세정 도구와 세정 중 강도는 확인되지 않았어요.

## syn-sol-0521 — 장시간 문지름과 표시 미상

- 내용 해시: `304288550f3cf39b82dca0c5daea84e2ed2105e182c3f7510d648b48474ebd44`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 자체는 확인됐지만 장시간 문지름과 제품 지시는 미상이다. / syn-sol-0030

### 설계한 시나리오 raw

씻어내는 클렌저를 쓰고 헹궈요. 일부러 오래 문질렀는지는 기억나지 않고 제품 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "장시간 문지름과 접촉 지시가 미상이에요."
    },
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "제품의 헹굼 지시는 확인하지 못했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "kb:B-C06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "씻어내는 클렌저",
    "connection": "제품 유형이다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "쓰고 헹궈요",
    "connection": "헹굼 실행이다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "일부러 오래 문질렀는지는 기억나지 않고",
    "connection": "문지른 방식에 대한 미상이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품 지시는 확인하지 못했어요",
    "connection": "표시 지시 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
실제로 헹군 사실은 확인되지만 제품 지시와 일치하는지는 아직 미상이에요 [kb:B-C06@0.6.1]. 오래 문질렀는지와 접촉 지시도 확인하지 못했어요 [kb:B-C03@0.6.1].

### 근거 및 이유
헹굼 실행과 제품 표시의 지시, 접촉 방식은 별도로 확인해야 하는 정보예요 [kb:B-C06@0.6.1] [kb:B-C03@0.6.1].

### 확인이 필요한 한계
기억나지 않는 행위를 했거나 하지 않았다고 단정하지 않아요. 필요하면 제품 표시와 실제 사용 방식을 확인해 주세요.

## syn-sol-0522 — 헹굼 요구와 실행 차이

- 내용 해시: `a3582bf5f6031f2caeec3bb5e32cfa8690bba3014480590c3e3a27a555b8f9ef`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 생략 이유는 가정하지 않고 수온 미상을 결합한다. / syn-sol-0038

### 설계한 시나리오 raw

세정제 표시는 씻어내라고 되어 있는데 실제로는 헹구지 않고 수건으로 닦아요. 물 온도는 모릅니다.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "헹굼이 필요한 제품을 헹구지 않았어요."
    },
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "물 온도는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "세정제 표시는 씻어내라고 되어 있는데",
    "connection": "씻어내는 제품이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "세정제 표시는 씻어내라고 되어 있는데",
    "connection": "헹굼 요구 표시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "실제로는 헹구지 않고",
    "connection": "헹굼을 실행하지 않았다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "물 온도는 모릅니다",
    "connection": "수온 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
씻어내라는 표시가 있는 세정제라면 수건으로만 닦고 헹굼을 생략하는 대신 표시된 헹굼을 따라 주세요 [kb:B-C06@0.6.1].

### 근거 및 이유
제품 표시의 헹굼 요구와 실제 헹굼 생략이 서로 달라요 [kb:B-C06@0.6.1].

### 확인이 필요한 한계
헹굼을 생략한 이유와 물 온도는 확인되지 않았어요 [kb:B-C01@0.6.1]. 시간을 절약하려 한 것이라고 가정하지 않아요.

## syn-sol-0523 — 부드러운 사용과 접촉 지시

- 내용 해시: `258680fae546bb58c148ddf6717f5007989fa04fec5ccb3075d77cb1261fb5ca`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 별도 지시 부재 상황에서 손 세정과 장시간 방치 부재를 함께 확인한다. / syn-sol-0039

### 설계한 시나리오 raw

얼굴을 부드럽게 손가락으로 씻고 물기를 가볍게 눌러요. 세정제의 별도 접촉 지시는 없으며 일부러 오래 올려두지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "specific_contact_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "intentionally_left_on_for_long_time": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "손가락으로 부드럽게 세정하고 가볍게 눌러요."
    },
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "장시간 문지름 여부와 세정제 유형은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use fingertips to wash the face and avoid scrubbing. Pat the skin dry with a soft towel.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.tools",
    "raw_span": "손가락으로 씻고",
    "connection": "사용 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "부드럽게 손가락으로 씻고",
    "connection": "세정 강도다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "물기를 가볍게 눌러요",
    "connection": "건조 방식이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "세정제의 별도 접촉 지시는 없으며",
    "connection": "별도 지시 부재다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "일부러 오래 올려두지 않아요",
    "connection": "장시간 방치 부정이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 손가락 세정과 가벼운 건조는 유지할 수 있어요 [kb:B-C02@0.6.1]. 세정제를 오래 올려두지 않았다는 사실만으로 오래 문질렀는지는 알 수 없어요 [kb:B-C03@0.6.1].

### 근거 및 이유
일반 얼굴 세안 안내는 손가락을 쓰고 부드럽게 건조하는 방법을 다뤄요 [ref:S03]. 올려두는 시간과 문지르는 행위는 구분해야 해요.

### 확인이 필요한 한계
세정제 유형과 장시간 문지름 여부가 확인되지 않아 접촉 방식 전체가 기준에 맞는지는 판정하지 않아요.

## syn-sol-0524 — 패드 사용과 마찰 미상

- 내용 해시: `d3bbc1c0106d49b53ac285859a609d2ad56249afacfb9ba355615fef812db627`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 패드 사용 차이를 강한 마찰로 바꾸지 않고 건조도 미상으로 둔다. / syn-sol-0037

### 설계한 시나리오 raw

세안 때 실리콘 패드를 사용해요. 얼마나 세게 움직였는지와 이후 수건으로 어떻게 닦았는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "silicone_pad"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "손가락 외 세정 도구를 사용해요. 마찰 강도는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use fingertips rather than a cleansing tool for face washing. Avoid scrubbing the skin.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.tools",
    "raw_span": "세안 때 실리콘 패드를 사용해요",
    "connection": "실제 세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "얼마나 세게 움직였는지",
    "connection": "마찰 강도를 기억하지 못한다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "이후 수건으로 어떻게 닦았는지는 기억나지 않아요",
    "connection": "건조 방법 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
실리콘 패드 사용은 손가락 외 도구를 사용한 차이로 확인돼요 [kb:B-C02@0.6.1]. 손가락으로 부드럽게 씻는 방법을 고려할 수 있어요 [ref:S03].

### 근거 및 이유
패드 사용은 실제 보고된 도구에 관한 정보예요. 일반 얼굴 세안 안내는 손가락을 사용하고 문지름을 피하도록 설명해요 [ref:S03].

### 확인이 필요한 한계
패드의 부드러움이나 세정 강도, 수건 건조 방식은 확인되지 않았어요. 패드 사용만으로 강한 마찰이나 손상을 단정하지 않아요.

## syn-sol-0525 — 현재 제품 pH 미상

- 내용 해시: `c62e918f3124d805a2fef2542f7080a5cf4be12724f411485ffcfae6c24b8742`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: pH 미상과 현재 불편 부재를 분리하고 교체 실익을 추정하지 않는다. / syn-sol-0007, syn-sol-0056

### 설계한 시나리오 raw

사용 중인 얼굴 세정제는 약산성인지 확인되지 않았어요. 불편은 없고 교체하지 않고 현재 사용을 검토하려고 해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "current_cleanser_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "현재 제품의 pH 자료가 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "현재 사용을 검토하려고 해요",
    "connection": "현재 루틴 검토다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "약산성인지 확인되지 않았어요",
    "connection": "pH 범주 미상이다."
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "불편은 없고",
    "connection": "현재 불편 부정이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "사용 중인 얼굴 세정제",
    "connection": "현재 사용 중인 세정제다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
현재 쓰는 세정제가 약산성인지는 확인되지 않았어요 [kb:B-C04@0.6.1]. 불편이 없다는 보고만으로 제품 성능을 확정하거나 pH 미상만으로 교체를 요구하지 않아요.

### 근거 및 이유
pH 범주와 완제품의 순함은 같은 정보가 아니에요 [kb:B-C04@0.6.1].

### 확인이 필요한 한계
현재 제품의 pH는 미상이고 판단에 필요할 때 자료를 확인할 수 있어요.

## syn-sol-0526 — 충돌하는 pH 자료

- 내용 해시: `1989015d0392a5490db61a7cbfa92aad646ea2e28980caaa0b06b26ead01c971`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 단순 pH 자료 부재가 아닌 충돌과 미사용을 결합한다. / syn-sol-0018

### 설계한 시나리오 raw

새 세정제를 고르는데 후보의 pH 자료가 서로 달라 어느 쪽이 맞는지 몰라요. 사용 경험은 아직 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "known",
      "value": {
        "conflicting_sources": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "candidate_not_yet_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "후보의 상충하는 pH 자료를 확인해야 해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "새 세정제를 고르는데",
    "connection": "새 제품 선택이다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "후보의 pH 자료가 서로 달라 어느 쪽이 맞는지 몰라요",
    "connection": "pH 자료 충돌이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "사용 경험은 아직 없어요",
    "connection": "후보 사용 경험이 없다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 후보의 pH 자료가 서로 충돌해 어느 쪽이 맞는지 판단을 보류해요 [kb:B-C04@0.6.1]. 정확한 제품 자료를 확인하기 전에는 약산성 여부를 정하지 않아요.

### 근거 및 이유
pH 자료가 서로 충돌하므로 어느 자료가 현재 후보를 설명하는지 확인이 필요해요 [kb:B-C04@0.6.1].

### 확인이 필요한 한계
아직 사용 경험이 없으므로 사용감이나 적합성을 추정할 수 없어요. pH만으로 완제품의 순함도 확정하지 않아요.

## syn-sol-0527 — pH 미상과 헹굼 생략

- 내용 해시: `86830f8c0b9056cfda90c4746d2427f555d95a1eb24094dda6bf9ea373e2e0ba`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: pH 미상과 별개로 필요한 헹굼 생략을 확인한다. / syn-sol-0038, syn-sol-0007

### 설계한 시나리오 raw

현재 루틴을 검토해요. 현재 쓰는 세정제는 pH 자료가 없어요. 헹굼이 필요한 제품인데 실제로는 세정 뒤 헹구지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "제품 pH가 미상이에요."
    },
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "헹굼이 필요한 제품을 헹구지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1",
    "kb:B-C06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "현재 루틴을 검토해요",
    "connection": "현재 루틴 검토다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "pH 자료가 없어요",
    "connection": "pH 자료 미상이다."
  },
  {
    "variable_id": "product.type",
    "raw_span": "헹굼이 필요한 제품인데",
    "connection": "씻어내는 제품이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "헹굼이 필요한 제품인데",
    "connection": "헹굼 요구가 확인된다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "실제로는 세정 뒤 헹구지 않아요",
    "connection": "실제 헹굼 생략이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
헹굼이 필요한 제품을 사용했다면 세정 후 표시된 헹굼을 수행해 주세요 [kb:B-C06@0.6.1]. 제품 pH 자료는 미상이에요 [kb:B-C04@0.6.1].

### 근거 및 이유
헹굼 실행과 pH는 독립된 정보예요.

### 확인이 필요한 한계
pH를 모르기 때문에 현재 제품을 바로 교체해야 한다고 판단하지 않아요.

## syn-sol-0528 — 발한 후 세정과 접촉 미상

- 내용 해시: `c791a32f8b9afc5fe4936f2e89a3ba188883566397c9d3366cfc7947378ea46d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 추가 세안 목적과 접촉 방식 미확인을 결합한다. / syn-sol-0019

### 설계한 시나리오 raw

운동 뒤 땀을 많이 흘려 얼굴을 한 번 더 씻어요. 세정제를 오래 문질렀는지와 접촉 지시는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "heavy_sweat_after_exercise": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "extra_wash_reason": "after_heavy_sweat"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "exception",
      "guidance": "심한 발한 후 추가 세안 목적이 확인돼요."
    },
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "세정제 접촉 방식은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "kb:B-C03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "운동 뒤 땀을 많이 흘려",
    "connection": "심한 발한이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴을 한 번 더 씻어요",
    "connection": "추가 세안이다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "세정제를 오래 문질렀는지",
    "connection": "장시간 문지름 여부를 기억하지 못한다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "접촉 지시는 기억나지 않아요",
    "connection": "제품 접촉 지시 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
운동 후 심한 발한은 추가 세안의 확인된 목적이므로 횟수만으로 불필요한 반복이라고 보지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
운동 뒤 심한 발한은 추가 세안의 목적이 될 수 있어요 [kb:B-C05@0.6.1].

### 확인이 필요한 한계
오래 문질렀는지와 제품 접촉 지시는 기억나지 않아 별도 판정을 보류해요 [kb:B-C03@0.6.1]. 필요하면 제품 표시와 사용 방식을 확인해 주세요.

## syn-sol-0529 — 선크림 세정 후 습관 반복

- 내용 해시: `89298db0438c9af63dd2092c69846c03a4388cb7058e0f7db2bce77a4ac95d9d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 첫 제거 목적과 목적 없는 반복, 수온을 분리한다. / syn-sol-0129, syn-sol-0001

### 설계한 시나리오 raw

저녁에 얼굴의 선크림을 지우고 나서 다른 오염이나 화장은 없는데 습관적으로 한 번 더 세정해요. 물은 미온수예요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_removed": true,
        "habitual_reasonless_repetition": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "additional_soiling": false,
        "makeup": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "difference",
      "guidance": "첫 제거 세정 뒤 추가 목적 없이 반복해요."
    },
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "미온수를 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use lukewarm water for facial cleansing. Washing after sweating is discussed separately from unnecessary scrubbing.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "물은 미온수예요",
    "connection": "실제 세안수 체감이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림을 지우고 나서",
    "connection": "첫 세정의 목적이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "습관적으로 한 번 더 세정해요",
    "connection": "추가 세정 행위다."
  },
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "다른 오염이나 화장은 없는데",
    "connection": "추가 오염과 화장 부재다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
선크림을 지운 뒤 별다른 추가 오염이나 화장 없이 습관적으로 한 번 더 세정하는 단계는 줄일 여지를 살펴보세요 [kb:B-C05@0.6.1]. 미온수 사용은 확인됐어요 [kb:B-C01@0.6.1].

### 근거 및 이유
첫 세정의 제거 목적과 후속 반복의 목적을 구분해요.

### 확인이 필요한 한계
일반 세안 안내의 미온수 원칙이 모든 제품의 제거 방법을 정하는 것은 아니에요 [ref:S03].

## syn-sol-0530 — 내수성 제품 제거 미확정

- 내용 해시: `2a22352f51f3d47f9b61db7f97919a0dc96155e8746082f0fd9b6b4b3258b24b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 세정 계획이 미결정이므로 이미 자동 반복한 것으로 추정하지 않는다. / syn-sol-0025

### 설계한 시나리오 raw

얼굴에 내수성 선크림을 썼지만 제거 방법을 아직 확인하지 않았어요. 얼굴을 몇 단계로 씻을지는 정하지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_used": true,
        "cleansing_steps_not_decided": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "제거 지시와 향후 세정 단계가 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.water_resistance",
    "raw_span": "내수성 선크림",
    "connection": "내수성 표시 제품이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림을 썼지만",
    "connection": "선크림의 실제 사용이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "몇 단계로 씻을지는 정하지 않았어요",
    "connection": "향후 세정 계획 미결정이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제거 방법을 아직 확인하지 않았어요",
    "connection": "제거 지시 미상이다."
  },
  {
    "variable_id": "cleansing.steps",
    "raw_span": "몇 단계로 씻을지는 정하지 않았어요",
    "connection": "단계 미결정이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
내수성 선크림의 제거 지시는 아직 확인하지 못했고, 앞으로 몇 단계로 씻을지는 정하지 않았어요 [kb:B-I01@0.6.1]. 해당 제품 표시를 확인해 주세요.

### 근거 및 이유
제품 제거 지시를 확인하는 일과 본인이 세정 단계를 결정하는 일은 서로 달라요. 내수성 표시만으로 특정 제거법을 확정하지 않아요.

### 확인이 필요한 한계
이미 여러 단계로 세안했거나 반드시 그렇게 해야 한다고 가정하지 않아요. 확인되지 않은 제거 성능도 추정하지 않아요.

## syn-sol-0531 — 도포량 축소와 헹굼 준수

- 내용 해시: `bd5d36791cd6f80f690ea71f6880be2c920af3191d8ab6a63707a9e4f42a91ed`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제거 편의에 따른 도포량 감소와 세정제 헹굼 준수를 분리한다. / syn-sol-0002, syn-sol-0038

### 설계한 시나리오 raw

얼굴 선크림 제거가 번거로워 평소보다 극히 적게 발랐어요. 그날 헹굼이 필요한 세정제는 사용 후 물로 헹궜어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "very_small_amount_due_to_removal_difficulty": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "제거 편의 때문에 선크림을 극히 적게 발라요."
    },
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "헹굼이 필요한 제품을 사용 후 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "The small comparison studied removal of tested sunscreen formulations by several cleansing methods. It cannot establish a universal removal method.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "kb:B-C06@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "선크림 제거가 번거로워 평소보다 극히 적게 발랐어요",
    "connection": "제거 우려와 적은 도포량이다."
  },
  {
    "variable_id": "product.type",
    "raw_span": "헹굼이 필요한 세정제",
    "connection": "씻어내는 제품 유형이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "헹굼이 필요한 세정제",
    "connection": "헹굼 요구다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "사용 후 물로 헹궜어요",
    "connection": "실제 헹굼이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제거가 번거롭다는 이유로 선크림을 극히 적게 바르는 방식을 재검토하고 제품의 제거 지시를 확인해 주세요 [kb:B-I01@0.6.1]. 세정제의 물 헹굼은 수행한 것으로 확인돼요 [kb:B-C06@0.6.1].

### 근거 및 이유
제거가 번거로워 도포량을 줄인 사실과 세정제 헹굼 이행은 별개의 관찰이에요 [kb:B-I01@0.6.1] [kb:B-C06@0.6.1].

### 확인이 필요한 한계
소규모 제품 비교를 모든 선크림으로 일반화할 수 없어요 [ref:S08]. 확인되지 않은 특정 제거법을 지어내지 않아요.

## syn-sol-0532 — 타인의 반복 세안

- 내용 해시: `93abe8dbe774572f011b14ed9dc2ba800996364a357d0a3fc08fadfe07e9db6f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 친구의 자동 반복을 본인에게 귀속하지 않고 지시 미상을 보존한다. / syn-sol-0002

### 설계한 시나리오 raw

친구는 내수성 표시만 보고 얼굴을 세 단계 세안하지만 저는 그렇게 반복하지 않아요. 제 선크림의 제거 지시는 아직 못 봤어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "본인의 제거 지시가 미상이고 타인의 세안은 본인의 행동이 아니에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "cleansing.repeat_wash",
    "raw_span": "저는 그렇게 반복하지 않아요",
    "connection": "본인의 자동 반복 부정이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제 선크림의 제거 지시는 아직 못 봤어요",
    "connection": "본인 제품 지시 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 친구처럼 자동으로 반복하지 않는다고 했고, 선크림 제거 지시는 아직 확인되지 않았어요 [kb:B-I01@0.6.1]. 현재 제품의 지시를 확인해 주세요.

### 근거 및 이유
친구의 세정 행동을 본인의 행동으로 옮겨 판단하지 않아요.

### 확인이 필요한 한계
내수성 표시만으로 본인의 세정 단계를 확정하지도 않아요.

## syn-sol-0533 — 보유 도구와 현재 손 세안

- 내용 해시: `214327278a269b1db80883001d1d49590e41240df175383ea7ea394dca838512`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 기기 보유 및 계획과 현재 손 세정을 분리한다. / syn-sol-0047, syn-sol-0037

### 설계한 시나리오 raw

얼굴 세정 도구를 쓰려고 보관하지만 아직 사용하지 않았어요. 현재는 손가락으로 부드럽게 씻고 물기를 눌러요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "owns_cleansing_tool": true,
        "tool_use_planned": true,
        "tool_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "현재는 손가락으로 부드럽게 씻고 물기를 눌러요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세정 도구를 쓰려고 보관하지만 아직 사용하지 않았어요",
    "connection": "도구 보유·계획과 미사용이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "손가락으로 부드럽게 씻고",
    "connection": "현재 세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "손가락으로 부드럽게 씻고",
    "connection": "현재 세정 강도다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "물기를 눌러요",
    "connection": "건조 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
현재 확인된 손가락 세정과 부드러운 움직임, 물기를 눌러 닦는 방식은 유지할 수 있어요 [kb:B-C02@0.6.1].

### 근거 및 이유
보관 중인 도구를 앞으로 쓰려는 계획과 실제 사용은 달라요.

### 확인이 필요한 한계
아직 그 도구를 사용하지 않았다는 보고를 그대로 반영해요.

## syn-sol-0534 — 사용 전 기기 지침 미상

- 내용 해시: `47735d7abf3406dbf5492a259cca5933e981eb25861e2a24757bf59124cd0f94`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 명시적 병용 금지 계획 사례를 대체한 신규 합성: 기기는 미사용이고 병용 가능 여부는 확인하지 못한 상태다. / syn-hold-0010

### 설계한 시나리오 raw

얼굴 세정 기기를 샀지만 아직 사용하지 않았고 현재 불편도 없어요. 세정제와 함께 써도 되는지 기기 지침을 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "owns_device": true,
        "device_not_yet_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기의 제품 병용 지침은 확인되지 않았고 아직 기기를 사용하지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴 세정 기기",
    "connection": "예정된 기기의 얼굴 세정 용도다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "기기를 샀지만 아직 사용하지 않았고",
    "connection": "보유와 실제 미사용을 구분한다."
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "현재 불편도 없어요",
    "connection": "현재 불편 부정이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "세정제와 함께 써도 되는지 기기 지침을 확인하지 못했어요",
    "connection": "병용 지침 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세정 기기는 아직 사용하지 않았고 세정제와의 병용 지침도 확인되지 않았어요 [kb:B-G06@0.6.1]. 병용을 검토할 때는 해당 기기와 제품의 지침을 확인해 주세요.

### 근거 및 이유
기기를 가지고 있는 것과 실제 사용하는 것은 달라요. 현재 불편이 없다는 보고도 병용 지침 확인을 대신하지 않아요.

### 확인이 필요한 한계
병용 가능 여부와 적절한 설정은 제공된 정보만으로 판단할 수 없어요. 이미 사용한 것처럼 반응이나 손상을 추정하지 않아요.

## syn-sol-0535 — 기기 사용 응답 거절

- 내용 해시: `cc92d57376dbe074ea03cc23321185749e57c44136b451467a66b6050815a846`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 기기 여부 거절과 세정 도구 미상, 현재 불편 부정을 각각 보존한다. / syn-hold-0010, syn-sol-0047

### 설계한 시나리오 raw

얼굴 세정할 때 기기를 사용하는지 답하고 싶지 않아요. 손가락 세정 여부도 확인되지 않았고 현재 불편은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기 사용은 응답 거절로 확인되지 않았어요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "손가락 세정 여부도 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1",
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "기기를 사용하는지 답하고 싶지 않아요",
    "connection": "기기 사용 답변 거절이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "손가락 세정 여부도 확인되지 않았고",
    "connection": "세정 도구 미상이다."
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "현재 불편은 없어요",
    "connection": "현재 불편 부정이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
기기 사용 여부에 대한 답변은 원하지 않으셨으므로 미사용으로 간주하지 않아요 [kb:B-G06@0.6.1]. 손가락 세정 여부도 미상이에요 [kb:B-C02@0.6.1].

### 근거 및 이유
현재 불편이 없다는 사실과 기기 사용 여부는 별도 정보예요 [kb:B-G06@0.6.1].

### 확인이 필요한 한계
답변을 원하지 않은 기기 사용 여부와 확인되지 않은 손가락 세정 여부를 추정하지 않아요.

## syn-sol-0536 — 기기 보유와 병용 미상

- 내용 해시: `eb131bb45156b6fae66435e43f8bf03213cdaa1f86e7504f111f3165e180e6f5`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 기기 보유와 실제 병용 미상 및 지침 미상을 구분한다. / syn-hold-0010

### 설계한 시나리오 raw

얼굴 세정 기기를 가지고 있으나 세정제와 함께 사용했는지 기억나지 않아요. 기기 사용 지침도 아직 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "owns_device": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기 보유만으로 실제 병용이나 지침 일치를 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 세정 기기를 가지고 있으나",
    "connection": "기기 보유다."
  },
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "세정제와 함께 사용했는지 기억나지 않아요",
    "connection": "병용 여부 미상이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "기기 사용 지침도 아직 확인하지 못했어요",
    "connection": "지침 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
기기를 가지고 있다는 것만으로 세정제와 실제 병용했다고 판단하지 않아요 [kb:B-G06@0.6.1]. 병용 여부와 기기 지침은 확인되지 않았어요.

### 근거 및 이유
기기 보유와 세정제 병용은 서로 다른 사실이에요 [kb:B-G06@0.6.1].

### 확인이 필요한 한계
병용 여부와 지침이 미확인이므로 임의의 강도나 병용 방식을 제안하지 않아요. 병용을 검토할 때는 해당 지침을 확인해 주세요.

## syn-sol-0537 — 부드러운 세정과 강한 건조

- 내용 해시: `1d33fab6312acda664661dc464960e59b3548db597c64a5ef263decb9da952a6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 부드러운 세정 중 마찰과 강한 건조 마찰을 분리한다. / syn-sol-0001, syn-sol-0198

### 설계한 시나리오 raw

얼굴에 닿는 물은 미온수이고 손가락으로 가볍게 씻어요. 물기를 닦을 때는 수건으로 강하게 비벼요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "fingers"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "gentle"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "strong_towel_rubbing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "미온수를 사용해요."
    },
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "세정은 부드럽지만 건조할 때 강하게 비벼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Wash the face with lukewarm water and fingertips. Avoid scrubbing and pat dry gently.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "물은 미온수이고",
    "connection": "사용 수온이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "손가락으로 가볍게 씻어요",
    "connection": "세정 도구다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "손가락으로 가볍게 씻어요",
    "connection": "세정 강도다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "물기를 닦을 때는 수건으로 강하게 비벼요",
    "connection": "건조 시 마찰이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
미온수와 부드러운 손가락 세정은 확인됐어요 [kb:B-C01@0.6.1]. 건조할 때는 강하게 비비는 대신 물기를 가볍게 눌러 보세요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 세안 안내는 문지름을 피하고 부드럽게 건조하는 방법을 다뤄요 [ref:S03].

### 확인이 필요한 한계
세정 중 강도와 건조 중 강도는 서로 다른 행위로 구분해요.

## syn-sol-0538 — 접촉 지시 미상과 세정 중 강한 마찰

- 내용 해시: `a5ab957bc6354ab7a9a49d736ee1983f123dc43d1788e6469fc41a268f83bae1`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 0039의 지시 준수 예외를 대체한 신규 합성: 강도는 확인되지만 기간과 지시가 미상인 별도 판단이다. / syn-sol-0030, syn-sol-0037

### 설계한 시나리오 raw

얼굴에 씻어내는 세정제를 세게 문질러 쓰고 물로 헹궈요. 오래 문질렀는지와 접촉시간 지시는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "strong"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "dose.contact_time": {
      "variable_id": "dose.contact_time",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "세정할 때 강하게 문질러요."
    },
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "제품 접촉 지시와 장시간 문지름 여부는 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "Use fingertips to wash the face and avoid scrubbing. Gently pat the skin dry.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴에 씻어내는",
    "connection": "실제 세정 부위다."
  },
  {
    "variable_id": "product.type",
    "raw_span": "씻어내는 세정제",
    "connection": "씻어내는 제품이다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "세게 문질러 쓰고",
    "connection": "강한 마찰이다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 헹궈요",
    "connection": "실제 헹굼이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "접촉시간 지시는 기억나지 않아요",
    "connection": "접촉 지시 미상이다."
  },
  {
    "variable_id": "dose.contact_time",
    "raw_span": "오래 문질렀는지",
    "connection": "장시간 여부 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세정제를 세게 문지르는 대신 부드럽게 씻는 방식을 고려해 보세요 [kb:B-C02@0.6.1]. 접촉 지시와 장시간 문지름 여부는 미상이에요 [kb:B-C03@0.6.1].

### 근거 및 이유
강한 마찰은 보고됐고 일반 얼굴 세안 안내는 문지름을 피하도록 설명해요 [ref:S03]. 사용 뒤 물로 헹군 사실도 별도로 확인됐어요.

### 확인이 필요한 한계
강하게 문질렀다는 것만으로 오래 문질렀다고 단정할 수 없어요. 제품의 접촉 지시는 필요한 경우 확인해 주세요.

## syn-sol-0539 — 수온 기억 불가

- 내용 해시: `fa9ee69db0130951794c928645fcc502004c0a6a61ad52826b714c432182f0f7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 감각 자체를 기억하지 못하며 건조 방식만 확인한다. / syn-sol-0125

### 설계한 시나리오 raw

얼굴 세정수 온도가 뜨거운지 미온수인지 기억나지 않아요. 수건으로는 물기를 가볍게 눌렀어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "pat_dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "수온이 미상이에요."
    },
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "세정 도구와 마찰이 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.water_temperature",
    "raw_span": "얼굴 세정수 온도가 뜨거운지 미온수인지 기억나지 않아요",
    "connection": "세안수 체감 미상이다."
  },
  {
    "variable_id": "method.drying",
    "raw_span": "수건으로는 물기를 가볍게 눌렀어요",
    "connection": "건조 방식이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
세안수 온도가 기억나지 않으므로 뜨겁거나 미온수라고 단정하지 않아요 [kb:B-C01@0.6.1]. 가볍게 눌러 건조한 사실은 확인됐어요 [kb:B-C02@0.6.1].

### 근거 및 이유
물기를 가볍게 눌렀다는 건조 방식은 확인됐어요 [kb:B-C02@0.6.1].

### 확인이 필요한 한계
수온과 세정 도구 및 마찰은 미상이어서 건조 방식만으로 확정할 수 없어요. 필요할 때 각각 확인해 주세요.

## syn-sol-0540 — 제품 유형과 헹굼 지시

- 내용 해시: `19eec58d81c0d932e792135aa109394750f4462bfac568b242fa5b2bd550a80a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 유형과 실제 미헹굼을 확인하지만 표시 지시를 미상으로 둔다. / syn-sol-0126

### 설계한 시나리오 raw

얼굴에 쓴 제품은 씻어내는 세정제지만 표시된 헹굼 지시를 확인하지 못했어요. 물로 헹구지는 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "씻어내는 세정제를 사용 후 물로 헹구지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "씻어내는 세정제",
    "connection": "보고된 제품 유형이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "표시된 헹굼 지시를 확인하지 못했어요",
    "connection": "표시 지시 미상이다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 헹구지는 않았어요",
    "connection": "물 헹굼 미실행이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
씻어내는 세정제를 사용하고 물로 헹구지 않은 점은 세정 후 헹굼 기본과 달라요 [kb:B-C06@0.6.1]. 해당 제품의 표시를 확인하고 필요한 헹굼을 따라 주세요.

### 근거 및 이유
사용한 제품의 유형과 실제 미헹굼은 각각 보고됐어요. 씻어내는 제품의 헹굼 여부를 제품 접촉시간과 별개로 살펴봐요.

### 확인이 필요한 한계
구체적인 표시 문구는 아직 확인하지 못했으므로 표시의 상세 절차나 이유는 추정하지 않아요.

## syn-sol-0541 — 오래 문지름 부정과 지시 미상

- 내용 해시: `49e79eb8666b29e89dff0d7f21d8bfac5fcc686729ee8368c6141a907b0d7108`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 장시간 문지름의 부정과 지시 미상을 구별하고 수온을 별도로 확인한다. / syn-sol-0030

### 설계한 시나리오 raw

얼굴 세안제를 일부러 오래 문지르지는 않아요. 접촉 지시는 확인하지 못했고 그 후 미온수로 헹궈요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "intentionally_rubs_for_long_time": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "lukewarm",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "제품 접촉 지시가 미확인이에요."
    },
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "미온수로 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "일부러 오래 문지르지는 않아요",
    "connection": "의도적 장시간 문지름 부정이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "접촉 지시는 확인하지 못했고",
    "connection": "접촉 지시 미상이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "미온수로 헹궈요",
    "connection": "헹굼 물 온도다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "미온수로 헹궈요",
    "connection": "헹굼 실행이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
일부러 오래 문지르지 않았다는 보고와 미온수 헹굼은 확인됐어요 [kb:B-C01@0.6.1]. 접촉 지시는 미확인이므로 제품 표시와의 일치는 판정하지 않아요 [kb:B-C03@0.6.1].

### 근거 및 이유
일부러 오래 문지르지 않았다는 보고와 제품별 접촉 안내는 별개예요 [kb:B-C03@0.6.1].

### 확인이 필요한 한계
지시를 모르는 것이 지시가 없다는 뜻은 아니에요. 필요하면 제품의 접촉 안내를 확인해 주세요.

## syn-sol-0542 — 후속 세정 표시

- 내용 해시: `41ce7bd0821d53ae1a7ce1ca0741fc2ff8546c0660c66cbf05c41a216d3f0069`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 두 번째 단계 목적 미상이 아니라 제품의 후속 세정 지시가 확인된다. / syn-sol-0129

### 설계한 시나리오 raw

얼굴 메이크업을 지운 뒤 세정제를 한 번 더 쓰는데 그 제거 제품 사용 지시에 후속 세정이 명시돼 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 2,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "subsequent_cleanser_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "follows_subsequent_cleansing_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "exception",
      "guidance": "후속 세정에 대한 해당 제품 지시가 확인돼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "얼굴 메이크업을 지운 뒤",
    "connection": "제거 대상이다."
  },
  {
    "variable_id": "cleansing.steps",
    "raw_span": "메이크업을 지운 뒤 세정제를 한 번 더 쓰는데",
    "connection": "두 세정 단계다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제거 제품 사용 지시에 후속 세정이 명시돼 있어요",
    "connection": "제품의 후속 세정 지시다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "지운 뒤 세정제를 한 번 더 쓰는데",
    "connection": "실제 후속 세정이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
메이크업 제거 뒤 후속 세정에 관한 제품 지시가 있는 상황이므로 단계 수만으로 불필요한 반복이라고 판단하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
확인된 목적과 해당 제거 제품의 지시를 함께 고려해요.

### 확인이 필요한 한계
다른 제품에도 같은 후속 단계가 필요하다고 일반화하지 않아요.

## syn-sol-0543 — 일시적 당김과 뜨거운 물

- 내용 해시: `ac35dfa11d8aaa5da51c94d771d919a6cd333e5ac4c784de30289d673a7cb458`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 일시적 경험과 물 온도를 함께 제시하되 인과관계는 모른다. / syn-sol-0013

### 설계한 시나리오 raw

얼굴 세안 뒤 당김이 잠깐 있었다가 사라져요. 뜨겁게 느껴지는 물로 씻었지만 그 물이 원인인지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "mild_transient",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": "hot",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "뜨겁게 느껴지는 물을 사용해요. 당김의 원인은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "당김이 잠깐 있었다가 사라져요",
    "connection": "일시적 경험이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "뜨겁게 느껴지는 물로 씻었지만",
    "connection": "수온 체감이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
뜨겁게 느껴진 물 대신 미온수로 세안해 볼 수 있어요 [kb:B-C01@0.6.1]. 당김은 잠깐 있었다가 사라졌다는 보고로 기록해요.

### 근거 및 이유
뜨겁게 느껴지는 물은 미온수 기본과 다른 관찰이에요 [kb:B-C01@0.6.1].

### 확인이 필요한 한계
물 온도가 당김의 원인이라고 확인된 것은 아니에요. 불편이 반복되거나 지속되면 필요시 전문가에게 상담해 주세요.

## syn-sol-0544 — 친구 반응과 본인 손 세정

- 내용 해시: `eff84e0dca82760713d324426b8eb31be3f79fe9f2f7614349cda77cf07263f7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 타인의 증상과 브러시 사용을 본인에게 이전하지 않는다. / syn-sol-0037

### 설계한 시나리오 raw

저는 얼굴에 불편하지 않아요. 친구는 클렌징 브러시를 쓸 때 따갑다고 하지만 저는 브러시를 쓰지 않고 손으로 씻어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "hands"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "other_subject_report": {
          "subject": "friend",
          "action": "uses_cleansing_brush",
          "experience": "stinging"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "본인의 세정 강도와 건조 방법은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "저는 얼굴에 불편하지 않아요",
    "connection": "본인 현재 불편 부정이다."
  },
  {
    "variable_id": "method.tools",
    "raw_span": "저는 브러시를 쓰지 않고 손으로 씻어요",
    "connection": "본인 실제 세정 도구다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "친구는 클렌징 브러시를 쓸 때 따갑다고",
    "connection": "본인이 아니라 친구가 기기 사용 시 따가움을 겪었다는 보고다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 브러시 대신 손으로 씻었고 불편하지 않다고 했어요 [kb:B-C02@0.6.1]. 세정 강도와 건조 방법은 확인되지 않았어요.

### 근거 및 이유
본인이 보고한 세정 도구와 친구가 보고한 경험은 서로 다른 사람의 정보예요. 손 사용만 확인됐으며 손가락 사용 여부까지 지정하지 않아요.

### 확인이 필요한 한계
친구의 따가움을 본인의 증상으로 옮겨 해석하지 않아요. 손 사용만으로 전체 세정 방법이 모두 일치한다고도 단정하지 않아요.

## syn-sol-0545 — 선크림 제거 계획과 실제 사용 구별

- 내용 해시: `8355b1e30d87cd5b6f8cc810d8d4b724ad54d9418918f0ed8a2f30b658a011fd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 0513의 실제 사용 후 자동 반복을 대체한 신규 합성: 아직 제품을 쓰지 않았고 제거 계획도 미결정이다. / syn-sol-0025

### 설계한 시나리오 raw

얼굴에 내수성 선크림을 바를 예정이지만 아직 바르지는 않았어요. 제거법도 고르지 않았고 제품의 제거 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_planned": true,
        "sunscreen_used": false,
        "removal_method_not_chosen": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "내수성 제품은 아직 사용하지 않았고 제거법도 결정되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "A small study compared removal of tested sunscreens with different cleansing methods. It does not establish a universal method for every product.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴에 내수성 선크림을 바를 예정",
    "connection": "선크림의 계획된 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "바를 예정이지만 아직 바르지는 않았어요",
    "connection": "미래 계획과 현재 미사용이다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "제거법도 고르지 않았고",
    "connection": "제거 계획 미결정이다."
  },
  {
    "variable_id": "product.water_resistance",
    "raw_span": "내수성 선크림",
    "connection": "후보 제품의 내수성 표시다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품의 제거 지시는 확인하지 못했어요",
    "connection": "제거 지시 미상이다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
내수성 선크림은 아직 얼굴에 사용하지 않았고 제거법도 정하지 않았어요 [kb:B-I01@0.6.1]. 나중에 사용할 제품의 제거 지시를 확인해 주세요.

### 근거 및 이유
제품을 바를 계획과 실제 사용은 다르며, 내수성 표시만으로 특정 제거 단계를 정하지 않아요. 시험한 제품의 제거 방법 비교는 제한된 범위의 결과예요 [ref:S08].

### 확인이 필요한 한계
제품 지시가 아직 미상이므로 특정 세정제나 단계 수를 단정하지 않아요. 사용하지 않은 제품의 실제 제거 성능도 알 수 없어요.

## syn-sol-0546 — 친구 미헹굼과 본인 헹굼

- 내용 해시: `eba6209c95eb1bdac49587f4f961711d892b2a765470b6fdd2b2148a453952a2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 친구의 미헹굼을 본인 행위로 전이하지 않고 본인 표시 준수를 확인한다. / syn-sol-0038, syn-sol-0363

### 설계한 시나리오 raw

친구는 세정제를 헹구지 않지만 저는 제 얼굴 세정제의 씻어내라는 표시를 확인하고 물로 헹궈요. 세안수 온도는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "other_subject_report": {
          "subject": "friend",
          "cleanser_rinsed": false
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "본인은 씻어내라는 표시를 확인하고 헹궈요."
    },
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "본인 세안수 온도는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "제 얼굴 세정제의 씻어내라는 표시",
    "connection": "본인의 씻어내는 세정제다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "씻어내라는 표시를 확인하고",
    "connection": "본인 제품 표시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "물로 헹궈요",
    "connection": "본인의 실제 헹굼이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "세안수 온도는 기억나지 않아요",
    "connection": "본인 세안수 온도 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "친구는 세정제를 헹구지 않지만",
    "connection": "친구의 헹굼 행동이며 본인의 행동이 아니다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 씻어내라는 표시를 확인하고 물로 헹궜어요 [kb:B-C06@0.6.1]. 본인의 물 온도는 기억나지 않아 미상이에요 [kb:B-C01@0.6.1].

### 근거 및 이유
본인의 제품 표시와 실제 헹굼은 서로 일치한다고 보고됐어요 [kb:B-C06@0.6.1].

### 확인이 필요한 한계
친구의 미헹굼을 본인의 행동으로 취급하지 않고 확인되지 않은 본인 물 온도도 추정하지 않아요.

## syn-sol-0547 — 두 독립된 미상

- 내용 해시: `b490d1a755f1873f9482d10fecdd5912b40d0ac255dec9eb64dc14758ab1400f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: pH와 접촉 지시 및 실제 문지름 미상을 각각 보존한다. / syn-sol-0007, syn-sol-0030

### 설계한 시나리오 raw

현재 얼굴 세정 루틴을 검토해요. 쓰는 세정제의 약산성 여부는 몰라요. 접촉 지시도 확인하지 못했고 일부러 오래 문질렀는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.ph": {
      "variable_id": "product.ph",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "현재 제품 pH는 미상이에요."
    },
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "접촉 지시와 장시간 문지름 여부가 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1",
    "kb:B-C03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "현재 얼굴 세정 루틴을 검토해요",
    "connection": "현재 루틴 검토다."
  },
  {
    "variable_id": "product.ph",
    "raw_span": "약산성 여부는 몰라요",
    "connection": "pH 범주 미상이다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "접촉 지시도 확인하지 못했고",
    "connection": "접촉 지시 미상이다."
  },
  {
    "variable_id": "method.friction",
    "raw_span": "일부러 오래 문질렀는지는 기억나지 않아요",
    "connection": "장시간 마찰 여부 미상이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
현재 세정제의 pH와 접촉 지시는 모두 확인되지 않았어요 [kb:B-C04@0.6.1] [kb:B-C03@0.6.1]. 일부러 오래 문질렀는지도 기억나지 않아 해당 행동을 단정하지 않아요.

### 근거 및 이유
제품 pH, 접촉 지시, 실제 문지름은 각각 별도로 판단해야 하는 정보예요 [kb:B-C04@0.6.1] [kb:B-C03@0.6.1].

### 확인이 필요한 한계
각 항목은 미상이므로 다른 항목의 부재나 차이로 바꾸지 않아요. 필요하다면 제품 자료와 실제 사용 방식을 각각 확인해 주세요.

## syn-sol-0548 — 병용 응답 거절

- 내용 해시: `bdb9d3b904f7d80665520a4757628573296fe06cf4e01946e8552ff92867475b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지침 미상과 병용 여부 응답 거절은 서로 다르다. / syn-hold-0010

### 설계한 시나리오 raw

얼굴 세정 기기와 세정제의 병용 지침을 확인하지 못했어요. 실제 병용 여부는 답변하지 않겠어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기 병용 지침이 미상이고 실제 병용 여부는 응답하지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "병용 지침을 확인하지 못했어요",
    "connection": "병용 지침 미상이다."
  },
  {
    "variable_id": "adjunct.device_use",
    "raw_span": "실제 병용 여부는 답변하지 않겠어요",
    "connection": "병용 여부 응답 거절이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
기기와 세정제의 병용 지침은 미확인이고 실제 병용 여부는 답변을 원하지 않으셨어요 [kb:B-G06@0.6.1]. 병용을 검토한다면 관련 제품과 기기의 지침을 먼저 확인해 주세요.

### 근거 및 이유
기기 지침과 실제 제품 병용 여부는 서로 다른 정보예요 [kb:B-G06@0.6.1].

### 확인이 필요한 한계
응답 거절을 병용하지 않았다는 뜻으로 바꾸지 않아요. 현재 정보로 강도나 병용 절차를 정하지 않아요.

## syn-sol-0549 — 헹굼 실행과 수온 거절

- 내용 해시: `5491aedd3ad4e0d318f52ad30458c31aece1bb78008ef7668a09899da42c83ad`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 헹굼 표시 준수와 수온 답변 거절을 결합한다. / syn-sol-0038

### 설계한 시나리오 raw

얼굴 세정제는 헹굼이 필요하다고 표시되어 있고 저는 물로 헹궈요. 다만 물 온도는 답하지 않겠어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "rinse_off_cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "rinse_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "요구된 헹굼을 수행해요."
    },
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "수온에 대한 응답을 원하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "kb:B-C01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "얼굴 세정제는 헹굼이 필요하다고 표시되어 있고",
    "connection": "씻어내는 세정제다."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "헹굼이 필요하다고 표시되어 있고",
    "connection": "표시 지시다."
  },
  {
    "variable_id": "method.rinse",
    "raw_span": "저는 물로 헹궈요",
    "connection": "실제 헹굼이다."
  },
  {
    "variable_id": "method.water_temperature",
    "raw_span": "물 온도는 답하지 않겠어요",
    "connection": "수온 응답 거절이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제품 표시에서 요구한 물 헹굼을 수행하고 있어요 [kb:B-C06@0.6.1]. 물 온도는 답변을 원하지 않으셨으므로 판단하지 않아요 [kb:B-C01@0.6.1].

### 근거 및 이유
헹굼을 했다는 것과 수온은 서로 다른 정보예요.

### 확인이 필요한 한계
수온을 미온수나 뜨거운 물로 추측하지 않아요.

## syn-sol-0550 — 운동 뒤 추가 물세안

- 내용 해시: `dab82e2e8e56b1bd2da0fd23973a4dcd69b1e05c8e63aafbf8441a9d3882b04b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 세정제 사용과 심한 땀 뒤 추가 물세안을 구별한다. / syn-sol-0019, syn-sol-0061

### 설계한 시나리오 raw

얼굴 세정제는 한 번만 쓰고 오후 운동 뒤 물로 다시 씻어요. 심하게 땀을 흘린 날이라서예요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "known",
      "value": {
        "cleanser_washes": 1,
        "additional_water_wash_after_exercise": 1
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "heavy_sweat_after_exercise": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "exception",
      "guidance": "심한 발한 뒤 추가 물세안 목적이 확인돼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.frequency",
    "raw_span": "세정제는 한 번만 쓰고 오후 운동 뒤 물로 다시 씻어요",
    "connection": "세정제 사용과 추가 물세안을 구별한다."
  },
  {
    "variable_id": "cleansing.target_load",
    "raw_span": "심하게 땀을 흘린 날이라서예요",
    "connection": "추가 물세안의 발한 목적이다."
  },
  {
    "variable_id": "method.body_site",
    "raw_span": "얼굴",
    "connection": "명시된 행위 또는 제품 사용 부위다."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
심한 발한 뒤의 추가 물세안에는 확인된 목적이 있어 횟수만으로 불필요한 반복이라 판단하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
세정제 한 번 사용과 운동 뒤 물로 씻는 행위를 구분해요.

### 확인이 필요한 한계
추가 물세안을 자동으로 세정제 반복으로 세지 않아요.

## syn-sol-0551 — 건조 후 보습과 지시 미확인

- 내용 해시: `9cef6242e634314b66f53c329ce583e37e81379aea1258db5781c1a406490d38`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 기존 보습 시점 사례와 달리 당김, 완전히 마를 때까지 기다린 행동 및 제품 지시 미확인을 함께 기록해요. / syn-sol-0003

### 설계한 시나리오 raw

얼굴을 씻고 당김이 있어 보습제를 써요. 피부가 다 마를 때까지 기다렸다가 바르고, 별도 사용 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face_wash": true,
        "moisturizer_used": true,
        "tightness_after_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.after_wash_delay": {
      "variable_id": "moisturizing.after_wash_delay",
      "state": "known",
      "value": {
        "wait_until_dry": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "도포 시 피부가 완전히 마른 것은 확인되지만 오래 방치했는지와 별도 제품 지시는 확인되지 않아 차이를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조한 피부 관리 안내는 씻은 뒤 피부가 아직 약간 촉촉할 때 보습제를 사용하는 방법을 다뤄요. 제품별 지시나 개인 진료 계획은 별도로 확인해야 해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    },
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance discusses applying moisturizer while skin is still slightly damp after washing. It does not prescribe one amount for every person.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M01@0.6.1",
    "ref:S04",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴을 씻고 당김이 있어 보습제를 써요",
    "connection": "얼굴 세정 후 당김과 실제 보습 사용"
  },
  {
    "variable_id": "method.skin_wetness",
    "raw_span": "피부가 다 마를 때까지 기다렸다가 바르고",
    "connection": "도포 시 피부가 완전히 마른 상태"
  },
  {
    "variable_id": "moisturizing.after_wash_delay",
    "raw_span": "피부가 다 마를 때까지 기다렸다가 바르고",
    "connection": "완전히 마를 때까지 기다린 실제 행동"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "별도 사용 지시는 확인하지 못했어요",
    "connection": "제품별 지시 미확인"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
세안 후 피부가 완전히 마를 때 보습했다고 하셨지만 오래 방치했는지는 확인되지 않아 시점의 차이를 확정하지 않아요 [kb:B-M01@0.6.1].

### 근거 및 이유
건조 피부의 일반 안내에는 씻은 뒤 피부가 약간 촉촉할 때 보습하는 방법이 있어요 [ref:S04].

### 확인이 필요한 한계
해당 제품의 별도 지시는 미상이므로 확인해 주세요. 정확한 경과 시간도 추정하지 않아요.

## syn-sol-0552 — 보습 시 물기 미상

- 내용 해시: `51a4481cae4a8bc61393b2500778dbbd8de2369d6051a24c5ae9e1addaf4722e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 보습 필요 불편이 없다는 보고와 물기 및 시간 미확인을 구분해요. / syn-sol-0049

### 설계한 시나리오 raw

세안 뒤 보습제는 쓰지만 바를 때 피부가 촉촉했는지는 기억나지 않아요. 당시 따로 건조한 불편은 없었어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_after_wash": true,
        "dry_discomfort": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "moisturizing.after_wash_delay": {
      "variable_id": "moisturizing.after_wash_delay",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "보습 사용은 확인됐지만 도포 시 물기와 경과 시간이 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance connects washing with moisturizing while the skin is slightly damp. The guidance does not establish a product-specific instruction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M01@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "세안 뒤 보습제는 쓰지만 바를 때 피부가 촉촉했는지는 기억나지 않아요. 당시 따로 건조한 불편은 없었어요",
    "connection": "보습제 실제 사용과 당시 건조 불편 부재"
  },
  {
    "variable_id": "method.skin_wetness",
    "raw_span": "바를 때 피부가 촉촉했는지는 기억나지 않아요",
    "connection": "도포 시 물기 미상"
  },
  {
    "variable_id": "moisturizing.after_wash_delay",
    "raw_span": "세안 뒤 보습제는 쓰지만",
    "connection": "세안 뒤 사용만 말해 경과 시간 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
세안 후 보습제를 사용한다는 사실은 확인됐지만 시점이 적절한지는 아직 판단하기 어려워요 [kb:B-M01@0.6.1].

### 근거 및 이유
일반 건조 피부 안내에서는 씻은 뒤 피부가 약간 촉촉할 때의 보습을 다뤄요 [ref:S04].

### 확인이 필요한 한계
당시 물기와 경과 시간을 기억하지 못하고 별도 건조 불편도 없었어요. 사용 사실만으로 당시 피부 상태를 추정하지 않아요.

## syn-sol-0553 — 본인 보습 시점과 지인 조언

- 내용 해시: `946566ad69d28907b9b62445f6489c0d40647da327dba15d1162f1c44317c439`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지인의 권유를 사용자 실제 행동이나 제품 지시로 바꾸지 않아요. / syn-sol-0003

### 설계한 시나리오 raw

세안 후 아직 약간 촉촉할 때 기존 보습제를 발라요. 지인이 마른 다음에 발라야 한다고 했지만 제 제품에 그런 지시는 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used_after_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "damp",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "apply_to_dry_skin": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "aligned",
      "guidance": "실제 세안 뒤 약간 촉촉할 때 보습하며 마른 피부에 바르라는 제품 지시는 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "General dry-skin guidance discusses applying moisturizer after washing while skin is slightly damp. It does not guarantee a particular product will suit everyone.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M01@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "세안 후 아직 약간 촉촉할 때 기존 보습제를 발라요",
    "connection": "세안 후 실제 보습 사용"
  },
  {
    "variable_id": "method.skin_wetness",
    "raw_span": "아직 약간 촉촉할 때",
    "connection": "실제 도포 시 피부 물기"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제 제품에 그런 지시는 없어요",
    "connection": "마른 후 도포 지시는 없다는 보고"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
세안 뒤 약간 촉촉할 때 보습하는 현재 방식은 이 항목에서 유지할 수 있어요 [kb:B-M01@0.6.1].

### 근거 및 이유
일반 건조 피부 안내도 세정 후 보습 시점을 다뤄요 [ref:S04]. 지인의 조언은 본인의 실제 사용법과 구분해요.

### 확인이 필요한 한계
이 항목의 정렬이 제품 전체의 안전이나 개인에게 맞는 효과를 보증하지는 않아요.

## syn-sol-0554 — 건조 재발과 감량 계획

- 내용 해시: `28be2493d750b884308ff72a4dd19520f552b5626f10c23d426ba104a7d0361b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 건조 재발은 보고됐으나 감량을 실행한 것으로 바꾸지 않아요. / syn-sol-0040

### 설계한 시나리오 raw

보습제를 쓰고도 오후에 건조감이 다시 돌아와요. 무조건 양을 줄이려고 하지만 통증이나 지속적인 불편은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "moisturizing.dryness_return": {
      "variable_id": "moisturizing.dryness_return",
      "state": "known",
      "value": {
        "afternoon_return": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "planned_reduce_amount": true,
        "reduction_executed": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "보습 후 오후 건조감이 돌아오지만 감량은 계획이며 실제 감량이나 방법 검토 회피는 확인되지 않아 차이를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance discusses moisturizer use and reapplication in the context of dryness. It does not set a universal amount for all formulations.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M02@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "moisturizing.dryness_return",
    "raw_span": "보습제를 쓰고도 오후에 건조감이 다시 돌아와요",
    "connection": "사용 후 건조감 재발"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "무조건 양을 줄이려고 하지만",
    "connection": "감량 계획이며 실행 여부를 말하지 않음"
  },
  {
    "variable_id": "skin.pain",
    "raw_span": "통증이나 지속적인 불편은 없어요",
    "connection": "통증 부정"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
보습 후 오후에 건조감이 다시 돌아오는 점을 기록해 두고, 무조건 감량하기 전에 현재 방법을 살펴볼 수 있어요 [kb:B-M02@0.6.1].

### 근거 및 이유
보습 사용과 재발한 건조감은 양과 빈도를 검토할 때 서로 구분할 정보예요 [ref:S04].

### 확인이 필요한 한계
감량은 계획으로만 보고됐고 실제 감량이나 방법 검토를 하지 않았다는 사실은 확인되지 않았어요. 적절한 양을 숫자로 정할 근거도 없어요.

## syn-sol-0555 — 관리되는 건조와 증량 질문

- 내용 해시: `60ae15fa6fcdd4c323d4a2b86e65b588316d90a994b7142cc044cce00bb9e532`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 현재 관리 상태와 추가 증량 질문을 분리해요. / syn-sol-0050

### 설계한 시나리오 raw

현재 보습을 유지하면 일상적인 건조 불편은 없어요. 더 많이 발라야 좋을지 궁금하지만 새 불편은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "daily_dryness_managed": true,
        "no_new_discomfort": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "increase_amount_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "aligned",
      "guidance": "현재 보습으로 일상 건조 불편이 관리되고 새 불편은 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "General dry-skin guidance discusses moisturizer use as part of care. It does not establish a single amount suitable for every person.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M02@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "현재 보습을 유지하면 일상적인 건조 불편은 없어요. 더 많이 발라야 좋을지 궁금하지만 새 불편은 없어요",
    "connection": "일상 건조 불편 관리와 새 불편 없음"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "더 많이 발라야 좋을지 궁금하지만",
    "connection": "증량 질문이지 증량 실행이 아님"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
현재 보습으로 일상적인 건조 불편이 관리된다면 증량을 서두르지 않고 유지할 수 있어요 [kb:B-M02@0.6.1].

### 근거 및 이유
건조 피부 안내는 보습 사용을 다루지만 모든 사람에게 같은 양을 정하지는 않아요 [ref:S04].

### 확인이 필요한 한계
새 불편이 없다는 보고는 다른 모든 불편이 없다는 뜻은 아니에요. 효과나 안전을 보증하지도 않아요.

## syn-sol-0556 — 건조감과 보습 후 변화 미상

- 내용 해시: `aa70e05bef8adb9441b6e97d2739b9e4ff42626886c2a5c1e45679fa4bb8f3b1`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 건조감만으로 현재 보습의 적절성을 판정하지 않아요. / syn-sol-0062

### 설계한 시나리오 raw

가벼운 건조감이 있지만 보습 후 다시 나타나는지는 아직 기록하지 않았어요. 보습 횟수도 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "known",
      "value": "mild",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.dryness_return": {
      "variable_id": "moisturizing.dryness_return",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "건조감은 보고됐으나 사용 후 변화와 실제 빈도는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance discusses moisturizer use and dryness management. It does not determine an individual routine from a single observation.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M02@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.dryness",
    "raw_span": "가벼운 건조감이 있지만",
    "connection": "가벼운 건조감 보고"
  },
  {
    "variable_id": "moisturizing.dryness_return",
    "raw_span": "보습 후 다시 나타나는지는 아직 기록하지 않았어요",
    "connection": "사용 후 재발 미상"
  },
  {
    "variable_id": "dose.frequency",
    "raw_span": "보습 횟수도 기억나지 않아요",
    "connection": "횟수 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
가벼운 건조감만으로 현재 보습의 양이나 횟수가 맞는지 결론 내리지 않아요 [kb:B-M02@0.6.1].

### 근거 및 이유
보습 후 건조감이 다시 나타나는지와 실제 사용 빈도가 방법 검토에 도움이 돼요 [ref:S04].

### 확인이 필요한 한계
두 정보가 미상이라 임의의 횟수나 양을 정할 근거가 없어요.

## syn-sol-0557 — 기능별 별도 구매 가정

- 내용 해시: `45a045a124de4da873f74abedf3b99b97894e48bf2f99b8550976736dd7c92fa`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 사용과 기능별 별도 구매 가정을 구분해요. / syn-sol-0057

### 설계한 시나리오 raw

한 보유 보습제를 실제로 쓰고 있고 건조 불편은 없어요. 수분과 차폐는 각각 새 제품이 반드시 필요하다고 생각해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "dry_discomfort": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "수분과 차폐에 각각 새 제품이 반드시 필요하다고 생각함"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "difference",
      "guidance": "실제 보습으로 건조 불편은 없는데 기능마다 반드시 별도 제품이 필요하다고 생각해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance discusses moisturizer use and formulation choices. It does not require separate products for every moisturizing function.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M03@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "한 보유 보습제를 실제로 쓰고 있고 건조 불편은 없어요",
    "connection": "기존 제품 사용과 건조 불편 부재"
  },
  {
    "variable_id": "constraints.goals",
    "raw_span": "수분과 차폐는 각각 새 제품이 반드시 필요하다고 생각해요",
    "connection": "기능별 별도 구매 필수라는 생각"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
건조 불편이 없는 현재 보습을 살펴보면서 수분과 차폐마다 새 제품이 반드시 필요하다는 가정은 다시 검토해 보세요 [kb:B-M03@0.6.1].

### 근거 및 이유
보유 제품 하나가 여러 보습 기능을 맡을 수 있어 기능마다 별도 단계를 필수로 둘 필요는 없어요. 일반 건조 피부 안내도 보습 사용을 다뤄요 [ref:S04].

### 확인이 필요한 한계
현재 보고는 제품의 모든 기능이나 광보호 요건을 확인해 주지는 않아요.

## syn-sol-0558 — 보습제 보유와 사용 구분

- 내용 해시: `66e1e478612aeba9c0537cddfc418798899a1e7bbf593a3b7538a2e67d858830`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 보유를 사용이나 목표 충족으로 추정하지 않아요. / syn-sol-0136

### 설계한 시나리오 raw

보습제는 가지고 있지만 아직 사용하지 않았어요. 수분과 차폐가 충족되는지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "보유한 보습제"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "unknown",
      "guidance": "제품 보유는 확인됐으나 사용으로 목표가 충족되는지는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.available_products",
    "raw_span": "보습제는 가지고 있지만",
    "connection": "보습제 보유"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "아직 사용하지 않았어요",
    "connection": "보습제 실제 미사용"
  },
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "수분과 차폐가 충족되는지는 몰라요",
    "connection": "기능 충족 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
보습제를 가지고 있다는 사실만으로 현재 보습 목표가 충족됐다고 판단하지 않아요 [kb:B-M03@0.6.1].

### 근거 및 이유
아직 사용하지 않았고 수분과 차폐가 충족되는지도 모른다고 했어요.

### 확인이 필요한 한계
보유와 실제 사용 경험은 달라요. 편안함이나 제품의 성능을 추정할 수 없어요.

## syn-sol-0559 — 남은 건조감과 추가 보습 검토

- 내용 해시: `e684163059fc8a1b6ce325dd66ec470913295ad86efb72ece40ca624addcfc85`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 하나를 쓴다는 사실만으로 추가 보습 불필요를 단정하지 않아요. / syn-sol-0203

### 설계한 시나리오 raw

한 보습제를 사용하지만 여전히 건조한 느낌이 남아요. 별도 보습이 필요한지 검토하고 싶어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "dryness_remains": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "별도 보습 필요성 검토"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "exception",
      "guidance": "기존 제품 사용에도 건조 불편이 남아 별도 보습 필요성을 검토하는 예외예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "Dry-skin guidance discusses moisturizer use and consultation for persistent symptoms. It does not establish an individual diagnosis.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M03@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "한 보습제를 사용하지만",
    "connection": "실제 보습제 사용"
  },
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "여전히 건조한 느낌이 남아요",
    "connection": "건조감이 남는다는 보고"
  },
  {
    "variable_id": "constraints.goals",
    "raw_span": "별도 보습이 필요한지 검토하고 싶어요",
    "connection": "추가 보습 검토 요청"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
기존 보습제를 써도 건조한 느낌이 남는다면 추가 보습 필요성을 따로 검토할 수 있어요 [kb:B-M03@0.6.1].

### 근거 및 이유
한 제품을 사용한다는 사실만으로 보습 목표가 충족됐다고 볼 수 없어요 [ref:S04].

### 확인이 필요한 한계
현재 정보만으로 특정 제품이나 정확한 양을 정할 수 없어요. 불편이 지속되면 전문가 확인이 필요해요.

## syn-sol-0560 — 향료 표시와 알레르기 답변 거절

- 내용 해시: `3b5f6f2a2be37729470dcdfc797f1b3edb5ac4c536cfdc79cc10159477189e7b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 신규 선택과 개인 알레르기 거절을 구분해요. / syn-sol-0015

### 설계한 시나리오 raw

새 제품을 고르는 중이에요. 확인한 합성 후보 표시에는 향료가 들어 있고 제 알레르기 여부는 알려주고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G01",
      "status": "difference",
      "guidance": "신규 후보에 향료가 표시되어 무향료 기본 선호와 차이가 있지만 개인 반응을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "FDA information discusses fragrance allergens and individual avoidance. A fragrance listing does not establish that every user will react.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G01@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "새 제품을 고르는 중이에요",
    "connection": "신규 제품 선택 맥락"
  },
  {
    "variable_id": "product.fragrance",
    "raw_span": "확인한 합성 후보 표시에는 향료가 들어 있고",
    "connection": "후보의 확인된 향료 표시"
  },
  {
    "variable_id": "person.known_allergies",
    "raw_span": "제 알레르기 여부는 알려주고 싶지 않아요",
    "connection": "개인 알레르기 응답 거절"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 후보에 향료 표시가 있어 무향료 기본 선호와는 차이가 있어요 [kb:B-G01@0.6.1]. 선택 시 표시를 살펴볼 수 있어요.

### 근거 및 이유
향료 알레르겐과 개인별 반응은 구분해서 확인해야 해요 [ref:S15].

### 확인이 필요한 한계
알레르기 정보 답변을 원하지 않으셨고, 향료 표시만으로 본인의 반응이나 위해를 확정할 수 없어요.

## syn-sol-0561 — 사용 제품의 향료 미상

- 내용 해시: `437e9eb3cc8f37d9951e66f97b0fd9e64a80ebbfad2b3dbb972ddca118500aa6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 불편 없음과 향료 미상을 별개로 취급해요. / syn-sol-0029

### 설계한 시나리오 raw

지금 쓰는 제품의 향료 정보는 확인하지 못했어요. 제품 사용 후 특별한 불편은 없고 교체할지 묻고 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "current_routine_review",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_used": true,
        "replacement_question": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G01",
      "status": "unknown",
      "guidance": "현재 사용과 불편 부재는 확인됐지만 향료 정보는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "FDA information discusses fragrance allergens and checking labels. Missing fragrance information does not establish either absence or an individual reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G01@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "교체할지 묻고 있어요",
    "connection": "현재 제품 유지 또는 교체 검토"
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "제품 사용 후 특별한 불편은 없고",
    "connection": "현재 특별한 불편 부정"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "지금 쓰는 제품의",
    "connection": "제품 실제 사용"
  },
  {
    "variable_id": "product.fragrance",
    "raw_span": "향료 정보는 확인하지 못했어요",
    "connection": "향료 정보 미확인"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
향료 정보가 확인되지 않아 이 기준만으로 현재 제품을 교체해야 한다고 판단하지 않아요 [kb:B-G01@0.6.1].

### 근거 및 이유
현재 특별한 불편이 없다는 보고와 향료의 포함 여부는 서로 다른 정보예요 [ref:S15].

### 확인이 필요한 한계
향료 정보 미상은 무향료라는 뜻도 아니에요. 제품 표시를 확인하기 전에는 포함 여부를 추정하지 않아요.

## syn-sol-0562 — 제품 지시를 넘는 일괄 증량

- 내용 해시: `8fa792734ff1e1737fdca80933ed9d0916999295f209e92c742a69b5f03ee6b7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 계획이 아니라 두 확인된 지시를 실제로 초과해요. / syn-sol-0103

### 설계한 시나리오 raw

서로 다른 제품 두 가지의 표시 용법을 확인했어요. 더 많이 바르면 무조건 좋다고 생각해서 둘 다 지시보다 많이 쓰고 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "two_products_individual_instructions_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "both_above_instructions": true,
        "reason": "more_is_always_better"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "difference",
      "guidance": "더 많이 바르면 좋다는 이유만으로 두 제품 모두 확인된 지시보다 많이 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "서로 다른 제품 두 가지의 표시 용법을 확인했어요",
    "connection": "두 제품의 지시 확인"
  },
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "더 많이 바르면 무조건 좋다고 생각해서 둘 다 지시보다 많이 쓰고 있어요",
    "connection": "이유와 실제 지시 초과 사용"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 무조건 많이 바르는 대신 각각 확인한 표시 용법을 기준으로 사용량을 다시 살펴보세요 [kb:B-G02@0.6.1].

### 근거 및 이유
서로 다른 제품에 같은 증량 원칙을 적용하면 각각의 지시를 놓칠 수 있어요.

### 확인이 필요한 한계
표시의 구체적인 양은 입력에 없어요. 임의의 양이나 성분 농도를 제시할 수 없어요.

## syn-sol-0563 — 동일 빈도와 양·농도 미상

- 내용 해시: `7909e182e9c45972bab12d89db0dba550f618fb5a483a98737468a7e2c9bd2ed`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 동일 횟수가 동일 양이나 농도를 뜻하지 않아요. / syn-sol-0107

### 설계한 시나리오 raw

두 제품을 한 번씩 쓰지만 한 번에 쓰는 양은 기록하지 않았어요. 표시된 성분 농도도 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "known",
      "value": {
        "each_product": "once"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.concentrations": {
      "variable_id": "product.concentrations",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "각 제품의 한 번 사용은 확인됐지만 사용량과 농도는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.frequency",
    "raw_span": "두 제품을 한 번씩 쓰지만",
    "connection": "제품별 각 1회 사용. 기간은 미상"
  },
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "한 번에 쓰는 양은 기록하지 않았어요",
    "connection": "실제 사용량 미상"
  },
  {
    "variable_id": "product.concentrations",
    "raw_span": "표시된 성분 농도도 확인하지 못했어요",
    "connection": "농도 미확인"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 한 번씩 쓴다는 정보만으로 양이나 성분 농도가 같다고 판단하지 않아요 [kb:B-G02@0.6.1].

### 근거 및 이유
사용 횟수, 한 번의 사용량, 성분 농도는 각각 다른 값이에요.

### 확인이 필요한 한계
양과 농도는 확인되지 않았고 한 번이 어느 기간을 뜻하는지도 알 수 없어요.

## syn-sol-0564 — 팩 지시와 실제 사용 충돌

- 내용 해시: `9c6906cccf9ae445ec377df5515a86b62c647ffa68ddb496d1ff0c916dd6c74d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 팩의 확인된 지시와 실제 일반 세안법 적용 충돌이에요. / syn-sol-0102

### 설계한 시나리오 raw

합성 팩 표시에는 정해진 시간 뒤 제거하라고 적혀 있어요. 일반 세안제처럼 씻어내면 된다고 생각해 표시 시간을 무시하고 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "합성 팩",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "remove_after_indicated_time": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "treats_as_cleanser": true,
        "ignores_indicated_time": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "difference",
      "guidance": "팩의 확인된 시간 지시를 무시하고 일반 세안제 사용법을 적용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "합성 팩 표시에는",
    "connection": "해당 제품 유형"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "정해진 시간 뒤 제거하라고 적혀 있어요",
    "connection": "확인된 제거 지시. 구체적 시간은 미상"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "일반 세안제처럼 씻어내면 된다고 생각해 표시 시간을 무시하고 있어요",
    "connection": "일반 세안법 적용과 지시 무시의 실제 행동"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
팩은 일반 세안제처럼 취급하기보다 확인된 제거 시간 지시를 따라 검토해 주세요 [kb:B-G03@0.6.1].

### 근거 및 이유
제품 유형과 실제 표시 지시를 함께 봐야 일반적인 세안법을 다른 제품에 잘못 적용하지 않아요.

### 확인이 필요한 한계
해당 팩의 구체적인 시간은 입력에 없으므로 임의로 정하지 않아요.

## syn-sol-0565 — 미사용 팩의 버전 지시 미확인

- 내용 해시: `2b18382386b676882edaf82a8b5d6d66401bac14e5b2dde7156849abdf45091d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 사용법을 묻는 계획과 실제 사용을 분리해요. / syn-sol-0104

### 설계한 시나리오 raw

팩을 보유하고 있지만 현재 버전의 표시 지시를 찾지 못했어요. 아직 사용하지 않았고 사용법을 알고 싶어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "보유한 팩"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "팩",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "pack_used": false,
        "instructions_requested": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "unknown",
      "guidance": "현재 버전의 팩 지시가 미확인이고 아직 사용하지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.available_products",
    "raw_span": "팩을 보유하고 있지만",
    "connection": "팩 보유"
  },
  {
    "variable_id": "product.type",
    "raw_span": "팩을 보유하고 있지만",
    "connection": "제품 유형"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "아직 사용하지 않았고 사용법을 알고 싶어요",
    "connection": "미사용과 지시 질문"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "현재 버전의 표시 지시를 찾지 못했어요",
    "connection": "현행 지시 미확인"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
아직 쓰지 않은 팩은 현행 버전의 표시를 확인하기 전 사용법을 정하지 않을게요 [kb:B-G03@0.6.1].

### 근거 및 이유
팩의 지시는 일반 세안제 지시와 다를 수 있어 해당 제품 정보를 확인하는 것이 필요해요.

### 확인이 필요한 한계
사용법이 미상인 상태예요. 제품을 가지고 있다는 사실이 이미 사용했다는 뜻도 아니에요.

## syn-sol-0566 — 로션을 분사형으로 전환

- 내용 해시: `bc90e5ba38595491d5f0722729a28511a5e86dc471284e29cacc8b4f482a07be`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 사전 혼합이 아닌 도포형 제품의 분사형 전환이에요. / syn-sol-0020

### 설계한 시나리오 raw

얼굴에 바르는 로션을 빈 분무기에 옮겨 뿌려 쓰고 있어요. 제조사의 분사 사용 지시는 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "바르는 로션",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "transferred_to_spray_and_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "바르는 로션을 분무기에 옮겨 사용하며 분사 지시는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "얼굴에 바르는 로션을",
    "connection": "바르는 로션이라는 제품 유형"
  },
  {
    "variable_id": "method.mixing",
    "raw_span": "빈 분무기에 옮겨 뿌려 쓰고 있어요",
    "connection": "실제 분사형 전환과 사용"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제조사의 분사 사용 지시는 확인하지 못했어요",
    "connection": "제조사 지시 미확인"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
바르는 로션을 분무기로 옮겨 쓰는 방식은 잠시 재검토하고 제조사의 해당 제품 지시를 확인해 주세요 [kb:B-G04@0.6.1].

### 근거 및 이유
제조사의 분사 지시는 확인되지 않았으며 도포형을 분사형으로 바꾸는 것은 별도 사용 행동이에요.

### 확인이 필요한 한계
지시를 아직 확인하지 못했으므로 분사가 허용되는지나 제품 성능을 단정하지 않아요.

## syn-sol-0567 — 순차 도포와 혼합 구분

- 내용 해시: `799dccc229894aff1120ee5dd17230b33dd5cb88333121c24f97d3fdae2ee31c`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 순차 도포를 사전 혼합으로 취급하지 않아요. / syn-sol-0068

### 설계한 시나리오 raw

두 제품을 손에서 섞는 대신 차례로 발라요. 혼합을 시도할 계획도 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "premixed_in_palm": false,
        "planned_mix": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": {
        "applied_separately_in_order": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "aligned",
      "guidance": "두 제품을 사전 혼합하지 않고 차례로 바르며 혼합할 계획도 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.mixing",
    "raw_span": "두 제품을 손에서 섞는 대신 차례로 발라요. 혼합을 시도할 계획도 없어요",
    "connection": "실제 사전 혼합 부정과 계획 부정"
  },
  {
    "variable_id": "method.sequence",
    "raw_span": "차례로 발라요",
    "connection": "분리하여 순차 도포"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 따로 차례로 바르는 행동은 손에서 사전 혼합하는 행동과 구분해요 [kb:B-G04@0.6.1].

### 근거 및 이유
현재 사전 혼합도 혼합할 계획도 없다고 확인됐어요.

### 확인이 필요한 한계
순차 사용 사실만으로 각 제품의 용법이나 개인 적합성이 확인되는 것은 아니에요.

## syn-sol-0568 — 팩 표시 시간과 밤샘 사용

- 내용 해시: `630012ad73e388332ab79cdbdc30a00aa4f645f274661b64da240bb646d646dd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 확인된 제품별 표시 시간과 취침 중 실제 사용을 비교해요. / syn-sol-0064

### 설계한 시나리오 raw

합성 팩 표시에는 10분 후 제거하라고 되어 있어요. 잠든 사이 계속 붙어 있도록 일부러 밤새 사용했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "remove_after_minutes": 10
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "worn_overnight_intentionally": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "difference",
      "guidance": "표시한 제거 시간과 달리 잠든 동안 밤새 사용했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S26",
      "text": "Face-mask guidance discusses product contact time and following product directions. It does not assign one contact time to all products.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/facial-masks-and-skin-care",
      "locator": "제품별 접촉시간·빈도, 기존 각질관리와 중복 확인, 따갑거나 가려우면 씻어내기.",
      "checked_on": "2026-11-04",
      "limitations": "얼굴 팩/마스크의 안내. 모든 추가관리 제품이나 기기에 동일한 수치를 적용하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G05@0.6.1",
    "ref:S26"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "합성 팩 표시에는 10분 후 제거하라고 되어 있어요",
    "connection": "합성 제품의 표시 시간"
  },
  {
    "variable_id": "adjunct.care_events",
    "raw_span": "잠든 사이 계속 붙어 있도록 일부러 밤새 사용했어요",
    "connection": "실제 밤샘 사용"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
이 합성 팩은 밤새 붙이는 대신 확인된 10분 후 제거 지시를 따라 주세요 [kb:B-G05@0.6.1].

### 근거 및 이유
팩 안내는 제품별 접촉시간과 사용 지시를 확인하도록 다뤄요 [ref:S26].

### 확인이 필요한 한계
10분은 이 사례에 제공된 표시일 뿐 모든 팩에 적용되는 시간이 아니에요.

## syn-sol-0569 — 밀림과 광보호 행동 유지

- 내용 해시: `3355f72f75a3f9512bd96cdc6ac4427b04538bca8ca98abf91f1e01d33a4fb94`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 밀림을 곧바로 광보호 행동 감소로 해석하지 않아요. / syn-sol-0069

### 설계한 시나리오 raw

보습제 뒤 선크림을 바르면 밀리지만 실제 사용량과 재도포는 줄이지 않았어요. 두 제품을 손에서 섞지는 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": [
        "moisturizer",
        "sunscreen"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_amount_reduced": false,
        "reapplication_reduced": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "premixed_in_palm": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "exception",
      "guidance": "밀림은 있지만 선크림 실제 사용량과 재도포를 줄이지 않아 일반 사용성 검토에 해당해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.sequence",
    "raw_span": "보습제 뒤 선크림을 바르면",
    "connection": "확인된 도포 순서"
  },
  {
    "variable_id": "sun.pilling",
    "raw_span": "선크림을 바르면 밀리지만",
    "connection": "밀림 존재"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "실제 사용량과 재도포는 줄이지 않았어요",
    "connection": "두 광보호 행동의 감소 부정"
  },
  {
    "variable_id": "method.mixing",
    "raw_span": "두 제품을 손에서 섞지는 않아요",
    "connection": "사전 혼합 부정"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
밀림이 있지만 선크림 사용량과 재도포는 줄이지 않았으므로 광보호 행동 감소로 판단하지 않아요 [kb:B-I02@0.6.1].

### 근거 및 이유
제품을 따로 바를 때의 밀림은 실제 사용량 감소와 구별해 사용성 측면에서 살펴볼 수 있어요.

### 확인이 필요한 한계
밀림 보고만으로 제품 성능이나 피부 반응의 원인을 확정하지 않아요.

## syn-sol-0570 — 답답함과 재도포 생략

- 내용 해시: `9ef52a0586f7a24d444fb44ed15554e5f939ffce8c6a1f23d64cde6ce2fa2f01`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 최초 도포량과 오후 재도포 행동을 분리해요. / syn-sol-0078

### 설계한 시나리오 raw

보습제와 선크림을 차례로 바를 때 답답해서 오후 재도포를 실제로 빼고 있어요. 처음 도포량을 줄였는지는 기억하지 못해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": [
        "moisturizer",
        "sunscreen"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "uncomfortable_texture": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "omitted_due_to_layering": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "difference",
      "guidance": "중첩의 답답함 때문에 오후 재도포를 실제로 생략해요. 최초 도포량 변화는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.sequence",
    "raw_span": "보습제와 선크림을 차례로 바를 때",
    "connection": "확인된 순차 사용"
  },
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "차례로 바를 때 답답해서",
    "connection": "중첩 사용의 답답함"
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "답답해서 오후 재도포를 실제로 빼고 있어요",
    "connection": "답답함에 따른 실제 재도포 생략"
  },
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "처음 도포량을 줄였는지는 기억하지 못해요",
    "connection": "최초 도포량 변화 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
답답함 때문에 오후 재도포를 생략하고 있어 광보호 행동을 유지할 수 있도록 중첩 방식의 불편을 검토해 보세요 [kb:B-I02@0.6.1].

### 근거 및 이유
이 사례에서는 단순한 사용감뿐 아니라 실제 재도포 생략이 확인됐어요.

### 확인이 필요한 한계
처음 도포량을 줄였는지는 미상이므로 줄였다고 단정하지 않아요.

## syn-sol-0571 — 밀림과 재도포 응답 거절

- 내용 해시: `9156d8c8c71e82c2f1defe4749cd1cc7e784c38e5dbc9a9b14e65c4717f11e0b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 밀림과 행동 변화 응답 거절을 구별해요. / syn-sol-0004

### 설계한 시나리오 raw

선크림과 보습제를 바를 때 밀림이 있어요. 밀림 때문에 재도포를 줄였는지는 답하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_and_sunscreen_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "밀림은 확인되나 재도포 행동 변화는 답변을 원하지 않아 판단할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.pilling",
    "raw_span": "선크림과 보습제를 바를 때 밀림이 있어요",
    "connection": "중첩 시 밀림"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림과 보습제를 바를 때",
    "connection": "두 제품 실제 사용"
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "밀림 때문에 재도포를 줄였는지는 답하고 싶지 않아요",
    "connection": "재도포 행동에 대한 응답 거절"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
밀림이 있다는 사실만으로 재도포를 줄였다고 판단하지 않아요 [kb:B-I02@0.6.1].

### 근거 및 이유
중첩의 사용감과 실제 광보호 행동 변화는 서로 구별해야 해요.

### 확인이 필요한 한계
재도포에 관한 답변을 원하지 않으셨으므로 그 행동은 미확인 상태로 둘게요.

## syn-sol-0572 — 새 제품 두 가지의 광범위 사용

- 내용 해시: `c8b350c4aff24353d152c5a327bcf5da7d69e47f2b8034fe01ddc6028ca1c03e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 광범위 사용과 현재 불편 부재를 함께 기록해요. / syn-sol-0011

### 설계한 시나리오 raw

새 화장품 두 가지를 작은 부위 확인 없이 동시에 얼굴 전체에 사용했어요. 아직 불편은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "introduction.local_trial": {
      "variable_id": "introduction.local_trial",
      "state": "known",
      "value": {
        "trial_before_use": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "introduction.change_scope": {
      "variable_id": "introduction.change_scope",
      "state": "known",
      "value": {
        "new_products": 2,
        "used_simultaneously_on_full_face": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "difference",
      "guidance": "신규 화장품 두 가지를 작은 부위 확인 없이 얼굴 전체에 동시에 사용했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "General guidance discusses trying a new product on a small area and observing for a reaction. Product-specific directions remain relevant.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/test-skin-care-products/",
      "locator": "작은 부위 사용 확인, 7–10일 관찰, 반응 시 씻어내고 재사용하지 않기, 의료 패치테스트와 구분",
      "checked_on": "2026-11-05",
      "limitations": "원문 일반 안내의 하루 2회/워시오프 5분을 모든 제품에 이식하지 않음. 개별 용법과 충돌 시 조건부 적용."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G11@0.6.1",
    "ref:S35"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "introduction.local_trial",
    "raw_span": "작은 부위 확인 없이",
    "connection": "작은 부위 사전 확인 부정"
  },
  {
    "variable_id": "introduction.change_scope",
    "raw_span": "새 화장품 두 가지를 작은 부위 확인 없이 동시에 얼굴 전체에 사용했어요",
    "connection": "두 새 제품의 동시 전면 사용"
  },
  {
    "variable_id": "skin.current_discomfort",
    "raw_span": "아직 불편은 없어요",
    "connection": "현재 불편 없음"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 제품을 여러 개 곧바로 넓게 사용하는 방식은 재검토해 주세요 [kb:B-G11@0.6.1].

### 근거 및 이유
일반 안내에서는 새 제품을 작은 부위에서 확인하는 방법을 다뤄요 [ref:S35].

### 확인이 필요한 한계
현재 불편이 없더라도 영구적인 무반응을 보증하지 않아요. 제품별 별도 지시도 확인해야 해요.

## syn-sol-0573 — 국소 무반응의 영구 안전 확대

- 내용 해시: `1667109fe11a300f9c7fcde75881486e0c0579dc73d9a5fbf5b03a3d90ebc7e7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 국소 무반응과 영구 안전 판단을 구분해요. / syn-sol-0091

### 설계한 시나리오 raw

새 제품을 작은 부위에 써 봤을 때 불편이 없었어요. 그래서 앞으로 어느 부위든 영원히 안전하다고 판단했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "introduction.local_trial": {
      "variable_id": "introduction.local_trial",
      "state": "known",
      "value": {
        "local_trial_done": true,
        "no_discomfort_during_trial": true,
        "inferred_permanent_safety_any_site": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "difference",
      "guidance": "국소 사용 시 불편이 없다는 관찰을 모든 부위의 영구 안전으로 확대했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "A small-area product trial can help identify a reaction during the observation period. It is distinct from medical patch testing.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/test-skin-care-products/",
      "locator": "작은 부위 사용 확인, 7–10일 관찰, 반응 시 씻어내고 재사용하지 않기, 의료 패치테스트와 구분",
      "checked_on": "2026-11-05",
      "limitations": "원문 일반 안내의 하루 2회/워시오프 5분을 모든 제품에 이식하지 않음. 개별 용법과 충돌 시 조건부 적용."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G11@0.6.1",
    "ref:S35"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "introduction.local_trial",
    "raw_span": "새 제품을 작은 부위에 써 봤을 때 불편이 없었어요. 그래서 앞으로 어느 부위든 영원히 안전하다고 판단했어요",
    "connection": "국소 사용 관찰과 사용자의 과도한 해석"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
작은 부위에서 불편이 없었던 경험을 모든 부위의 영구적인 안전으로 확대하지 말아 주세요 [kb:B-G11@0.6.1].

### 근거 및 이유
국소 확인은 관찰 기간의 반응을 살피는 일반 방법이며 의료적 패치테스트와도 달라요 [ref:S35].

### 확인이 필요한 한계
한 번의 관찰은 이후 반응이나 다른 부위의 반응을 보증하지 않아요.

## syn-sol-0574 — 신규 제품 미사용과 지시 미상

- 내용 해시: `2eeb84e40860c3cf05af53f98cb55608631e6cad00a0e54bbc9e7697e1245405`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 소유를 도입한 사실로 바꾸지 않아요. / syn-sol-0011

### 설계한 시나리오 raw

새 제품을 사두었지만 아직 사용하지 않았어요. 작은 부위 확인 방법에 관한 제품 지시도 찾지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "보유한 새 제품"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "new_product_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "신규 제품은 아직 사용하지 않았고 제품 지시도 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "General guidance discusses small-area product trials before wider use. It does not replace the specific directions for a product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/test-skin-care-products/",
      "locator": "작은 부위 사용 확인, 7–10일 관찰, 반응 시 씻어내고 재사용하지 않기, 의료 패치테스트와 구분",
      "checked_on": "2026-11-05",
      "limitations": "원문 일반 안내의 하루 2회/워시오프 5분을 모든 제품에 이식하지 않음. 개별 용법과 충돌 시 조건부 적용."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G11@0.6.1",
    "ref:S35"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.available_products",
    "raw_span": "새 제품을 사두었지만",
    "connection": "제품 보유"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "아직 사용하지 않았어요",
    "connection": "실제 미사용"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "작은 부위 확인 방법에 관한 제품 지시도 찾지 못했어요",
    "connection": "제품 지시 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 제품은 아직 사용하지 않았으므로 이미 넓게 사용했다고 판단하지 않아요 [kb:B-G11@0.6.1].

### 근거 및 이유
일반 안내에는 작은 부위 확인이 있지만 해당 제품의 지시도 확인해야 해요 [ref:S35].

### 확인이 필요한 한계
제품별 지시가 미상이라 정해진 방법을 임의로 제시하지 않아요.

## syn-sol-0575 — 동시 변경 뒤 단일 원인 확정

- 내용 해시: `7a9ec39ef0fd31759ebf6479f7c98bde9daca58317446df3f199f83987a68b7b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 시간 순서와 원인 확정을 구분해요. / syn-sol-0022

### 설계한 시나리오 raw

보습제와 세안제를 같은 날 새 제품으로 바꾼 뒤 건조감을 느꼈어요. 보습제 하나가 원인이라고 확신해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "moisturizer_and_cleanser_changed_same_day": true,
        "dryness_after_change": true,
        "user_attributes_cause_to_moisturizer": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G12",
      "status": "difference",
      "guidance": "제품 두 가지를 동시에 변경한 뒤 건조감의 원인을 한 제품으로 확정했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G12@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "routine.change_log",
    "raw_span": "보습제와 세안제를 같은 날 새 제품으로 바꾼 뒤 건조감을 느꼈어요. 보습제 하나가 원인이라고 확신해요",
    "connection": "동시 변경, 이후 관찰 및 사용자의 원인 추정"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 동시에 바꾼 뒤 느낀 건조감을 보습제 하나의 원인으로 확정하지 말아 주세요 [kb:B-G12@0.6.1].

### 근거 및 이유
변경 시점이 겹치면 어떤 변화가 관찰과 관련되는지 구분하기 어려워요.

### 확인이 필요한 한계
시간상 뒤에 나타났다는 사실만으로 인과관계나 피부 상태를 진단할 수 없어요.

## syn-sol-0576 — 하나의 변경과 결과 미관찰 구분

- 내용 해시: `75e9c81244ff127c33e8c8ab3836a8ada5090ca6158eb5694aa44131e5bfa67d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 하나의 변경과 결과 미관찰 구분 / syn-sol-0092

### 설계한 시나리오 raw

세안제만 새로 바꾸고 보습제는 그대로 썼어요. 바꾼 뒤 편안한지 아직 관찰하지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "cleanser_changed": true,
        "moisturizer_unchanged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G12",
      "status": "aligned",
      "guidance": "변경은 세안제 하나로 구분되고 변경 후 편안함은 관찰되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G12@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "routine.change_log",
    "raw_span": "세안제만 새로 바꾸고 보습제는 그대로 썼어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
세안제만 바꾸고 보습제는 유지한 변경 기록을 구분해 둘 수 있어요 [kb:B-G12@0.6.1].

### 근거 및 이유
한 가지 변경을 구분해 기록하면 나중에 무엇을 바꿨는지 확인하는 데 도움이 돼요.

### 확인이 필요한 한계
바꾼 뒤 편안함은 아직 관찰하지 않았으므로 좋거나 나쁘다고 평가하지 않아요.

## syn-sol-0577 — 날짜와 같은 부위의 별도 제품 사용 분리

- 내용 해시: `191d619391017706c36d703e02f7dc65edaf8de9acd787f6aa2fa23aec0fbb29`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 날짜와 같은 부위의 별도 제품 사용 분리 / syn-sol-0006

### 설계한 시나리오 raw

레티노이드 관리 제품과 AHA 각질관리 제품을 각각 얼굴에 사용해요. 날짜는 달라도 별도 제품을 같은 부위에 쓰는 것이 확인돼요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "separate_products": [
          "retinoid",
          "aha_exfoliating"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "same_site": "face",
        "different_days": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "별도 제품을 같은 부위에 사용하며 날짜 분리만으로 자동 적합 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "Advice on retinoid use discusses caution with additional exfoliation. It does not establish an individual probability of harm.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.active_care_roles",
    "raw_span": "레티노이드 관리 제품과 AHA 각질관리 제품을 각각 얼굴에 사용해요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "날짜는 달라도 별도 제품을 같은 부위에 쓰는 것이 확인돼요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 같은 부위의 레티노이드와 별도 AHA 각질관리 사용을 함께 검토해 주세요 [kb:B-G13@0.6.1].

### 근거 및 이유
레티노이드 사용 중 추가 각질관리에 주의하는 일반 안내가 있어요 [ref:S32]. 날짜가 다르다는 점만으로 자동 적합하다고 보지는 않아요.

### 확인이 필요한 한계
이 기준은 개인의 피해 확률이나 모든 병용의 절대 금지를 뜻하지 않아요.

## syn-sol-0578 — 단일 완제품과 별도 제품 사용 미상

- 내용 해시: `25b04eb6beee465aba60e81d55200a3e89a7c58c76f575396b862427299463a0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 단일 완제품과 별도 제품 사용 미상 / syn-sol-0027

### 설계한 시나리오 raw

레티노이드와 AHA가 한 완제품에 함께 있다는 표시만 확인했어요. 다른 각질관리 제품을 실제로 쓰는지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "single_finished_product": [
          "retinoid",
          "aha"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "단일 복합 완제품과 별도 각질관리 사용 미상은 별도로 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.combination_design",
    "raw_span": "레티노이드와 AHA가 한 완제품에 함께 있다는 표시만 확인했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "다른 각질관리 제품을 실제로 쓰는지는 몰라요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
레티노이드와 AHA가 한 완제품에 있다는 표시만으로 별도 제품 중첩으로 판단하지 않아요 [kb:B-G13@0.6.1].

### 근거 및 이유
복합 완제품과 같은 부위에 별도 제품을 쓰는 상황은 구분해서 검토해요.

### 확인이 필요한 한계
다른 각질관리 제품의 실제 사용은 미상이어서 적합성이나 무자극을 단정하지 않아요.

## syn-sol-0579 — 두 제품의 실제 사용 부위 분리

- 내용 해시: `e55758dd78df0a69bf807ea27cfbf83a6ce30f32e042a7c4344a9352c7e22b94`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 두 제품의 실제 사용 부위 분리 / syn-sol-0010

### 설계한 시나리오 raw

얼굴에 레티노이드 제품을 쓰고 팔에 살리실산 각질관리 제품을 써요. 얼굴에 두 제품을 겹쳐 쓰지는 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "products": [
          "retinoid",
          "salicylic_exfoliating"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "retinoid_site": "face",
        "salicylic_site": "arm",
        "both_on_face": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "exception",
      "guidance": "실제 사용 부위가 달라 동일 부위 중첩 기준의 예외예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S34",
      "text": "A specific medicine label warns that use with certain other topical acne products can increase local irritation. That label is not a universal rule for every cosmetic.",
      "scope": "general_skincare_practice",
      "source_url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=4b6006e3-f7a4-4823-8217-3e5b0f7e58d9",
      "locator": "5.1항: 살리실릭애씨드 등 OTC 여드름 제품 병용 시 국소 자극 증가 가능",
      "checked_on": "2026-11-05",
      "limitations": "특정 의약품 표시의 주의. 처방 중단·용량 변경 알고리즘으로 확대하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1",
    "ref:S34"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.active_care_roles",
    "raw_span": "얼굴에 레티노이드 제품을 쓰고 팔에 살리실산 각질관리 제품을 써요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "얼굴에 레티노이드 제품을 쓰고 팔에 살리실산 각질관리 제품을 써요. 얼굴에 두 제품을 겹쳐 쓰지는 않아요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
레티노이드는 얼굴, 살리실산 각질관리제는 팔에 쓰므로 확인된 행동에 동일 부위 중첩 기준을 적용하지 않아요 [kb:B-G14@0.6.1].

### 근거 및 이유
해당 기준은 별도 제품을 같은 부위에 사용하는지를 살펴요. 특정 의약품 표시의 병용 주의도 그 제품의 범위에서 읽어야 해요 [ref:S34].

### 확인이 필요한 한계
부위가 다르다는 사실만으로 각각의 사용이 모두 무자극이라고 보증하지 않아요.

## syn-sol-0580 — 보유와 실제 각질관리 용도 분리

- 내용 해시: `185b47e22e5f2e0c6e6a3d728499be2ac57e620bca26f008c0d002f6648651bc`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 보유와 실제 각질관리 용도 분리 / syn-sol-0014

### 설계한 시나리오 raw

레티노이드 제품과 살리실산이 든 제품을 갖고 있어요. 살리실산 제품을 각질관리 목적으로 실제 사용하는지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "보유한 레티노이드 제품",
        "보유한 살리실산 포함 제품"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "보유와 성분 포함만으로 각질관리 목적의 실제 병용을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.available_products",
    "raw_span": "레티노이드 제품과 살리실산이 든 제품을 갖고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.active_care_roles",
    "raw_span": "살리실산 제품을 각질관리 목적으로 실제 사용하는지는 몰라요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 보유했다는 사실만으로 얼굴 등에 각질관리 목적으로 병용한다고 판단하지 않아요 [kb:B-G14@0.6.1].

### 근거 및 이유
살리실산 포함 여부와 해당 제품을 실제 각질관리 목적으로 쓰는지는 별개예요.

### 확인이 필요한 한계
사용 목적이 미상이므로 같은 부위 중첩 여부도 확정할 수 없어요.

## syn-sol-0581 — 별도 제품의 같은 부위 사용과 날짜 분리

- 내용 해시: `d86e5478d3518b39f89a16812a9bab9ec301167bdf6eb700315a84ed615814fb`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 별도 제품의 같은 부위 사용과 날짜 분리 / syn-sol-0012

### 설계한 시나리오 raw

별도 AHA 각질관리제와 BHA 각질관리제를 같은 얼굴 부위에 번갈아 사용해요. 다른 날 사용하면 병용 검토가 필요 없다고 생각해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "separate_products": [
          "aha_exfoliating",
          "salicylic_exfoliating"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "site": "face",
        "alternate_days": true,
        "user_assumes_no_review": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "difference",
      "guidance": "별도 제품의 동일 부위 사용을 날짜 분리만으로 적합하다고 보지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.active_care_roles",
    "raw_span": "별도 AHA 각질관리제와 BHA 각질관리제를 같은 얼굴 부위에 번갈아 사용해요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "별도 AHA 각질관리제와 BHA 각질관리제를 같은 얼굴 부위에 번갈아 사용해요. 다른 날 사용하면 병용 검토가 필요 없다고 생각해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
같은 얼굴 부위에 별도 AHA와 BHA 각질관리제를 사용하는 상황은 함께 검토해 주세요 [kb:B-G15@0.6.1].

### 근거 및 이유
서로 다른 날 사용한다는 점만으로 해당 중첩 검토가 자동으로 불필요해지지는 않아요.

### 확인이 필요한 한계
이 기준은 개인의 반응이나 위해 확률을 계산하지 않으며 모든 조합의 절대 금지라는 뜻도 아니에요.

## syn-sol-0582 — 단일 완제품과 추가 별도 사용 미상

- 내용 해시: `df5a848c1c548660012937d963a500c73887a690708ba1ce083065aedb3f77d1`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 단일 완제품과 추가 별도 사용 미상 / syn-sol-0036

### 설계한 시나리오 raw

AHA와 BHA를 함께 담은 단일 완제품의 표시를 확인했어요. 별도의 각질관리제를 더 쓰는지는 기억하지 못해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "single_finished_product": [
          "aha",
          "bha"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "단일 복합 제품과 별도 제품의 사용 미상은 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.combination_design",
    "raw_span": "AHA와 BHA를 함께 담은 단일 완제품의 표시를 확인했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "routine.co_use_context",
    "raw_span": "별도의 각질관리제를 더 쓰는지는 기억하지 못해요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
단일 AHA·BHA 완제품의 표시를 별도 각질관리 제품의 중첩과 구분해요 [kb:B-G15@0.6.1].

### 근거 및 이유
현재 확인된 것은 한 완제품의 표시이고 추가 제품 사용은 기억하지 못한다고 했어요.

### 확인이 필요한 한계
별도 사용이 미상인 만큼 자동 금지나 무자극 판정을 하지 않아요.

## syn-sol-0583 — 얼굴 외 제품의 확인된 접촉 제외와 원인 미상

- 내용 해시: `ddf4be816cafe89aa5e0a0405e09dc069dabbf19acc3597684c7765085e69c22`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 얼굴 외 제품의 확인된 접촉 제외와 원인 미상 기존 648에는 B-L01이나 직접적인 얼굴 외 접촉 경로 관찰이 없어요. 0022는 여러 변화와 원인 확정을 구분하는 기능적 참고일 뿐 접촉 경로의 근접 가족은 아니에요. / syn-sol-0022

### 설계한 시나리오 raw

얼굴 옆쪽에 불편이 생겼고 머리카락에 쓰는 제품이 그 부위에 실제 닿았어요. 얼굴용 제품만 살펴보고 머리 제품은 제외했어요. 원인은 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "environment.indirect_products": {
      "variable_id": "environment.indirect_products",
      "state": "known",
      "value": {
        "hair_product_touched_symptom_area": true,
        "excluded_from_review": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "discomfort_site": "side_of_face",
        "cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-L01",
      "status": "difference",
      "guidance": "확인된 머리 제품 접촉을 검토에서 제외했지만 원인으로 확정할 수도 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-L01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "environment.indirect_products",
    "raw_span": "머리카락에 쓰는 제품이 그 부위에 실제 닿았어요. 얼굴용 제품만 살펴보고 머리 제품은 제외했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴 옆쪽에 불편이 생겼고 머리카락에 쓰는 제품이 그 부위에 실제 닿았어요. 얼굴용 제품만 살펴보고 머리 제품은 제외했어요. 원인은 몰라요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품뿐 아니라 실제로 얼굴 옆에 닿은 머리 제품도 접촉 경로로 함께 살펴보세요 [kb:B-L01@0.6.1].

### 근거 및 이유
이 사례에서는 접촉이 확인됐는데도 해당 경로를 검토에서 제외했어요.

### 확인이 필요한 한계
접촉했다는 사실만으로 그 제품이 불편의 원인이라고 확정할 수 없어요.

## syn-sol-0584 — 증상 부위와 접촉 미상을 분리

- 내용 해시: `ecac6ba5b94850cfabc8db68df7ce468c34de509863bbe5ad41b5ddd341d4f41`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 증상 부위와 접촉 미상을 분리 기존 648에는 B-L01이나 직접적인 얼굴 외 접촉 경로 관찰이 없어요. 0022는 여러 변화와 원인 확정을 구분하는 기능적 참고일 뿐 접촉 경로의 근접 가족은 아니에요. / syn-sol-0022

### 설계한 시나리오 raw

목이 불편하지만 머리 제품이 목에 닿았는지는 모르겠어요. 얼굴용 제품만으로 원인을 판단할 수도 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "discomfort_site": "neck"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "environment.indirect_products": {
      "variable_id": "environment.indirect_products",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-L01",
      "status": "unknown",
      "guidance": "목 불편만으로 머리 제품이 실제로 닿았다고 추론할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-L01@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.distribution",
    "raw_span": "목이 불편하지만",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "environment.indirect_products",
    "raw_span": "머리 제품이 목에 닿았는지는 모르겠어요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
목 불편에 대한 접촉 경로는 아직 확인되지 않았어요 [kb:B-L01@0.6.1].

### 근거 및 이유
머리 제품이 목에 실제 닿았는지 모르므로 증상 위치만으로 접촉을 만들지 않아요.

### 확인이 필요한 한계
얼굴용 제품이나 머리 제품 중 어느 쪽이 원인인지도 현재 정보로 판단할 수 없어요.

## syn-sol-0585 — 접촉시간 대신 동일 목적 관리 중첩

- 내용 해시: `8407b4a45792d01fc0cff7a308ca255c15949c1aff4010d115d62c73f09fb6ce`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 접촉시간 대신 동일 목적 관리 중첩 / syn-sol-0166

### 설계한 시나리오 raw

각질관리 패드와 각질관리 팩을 둘 다 같은 부위에 쓰고 있어요. 별도 이유는 없고 계속 중첩하려고 해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "exfoliating_pad_and_pack_same_site": true,
        "reason": "none"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "difference",
      "guidance": "같은 목적의 추가 관리를 별도 이유 없이 중첩해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "adjunct.care_events",
    "raw_span": "각질관리 패드와 각질관리 팩을 둘 다 같은 부위에 쓰고 있어요. 별도 이유는 없고 계속 중첩하려고 해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
같은 부위에 각질관리 패드와 팩을 이유 없이 중첩하는 방식을 재검토해 주세요 [kb:B-G05@0.6.1].

### 근거 및 이유
두 관리의 목적이 겹치는지 보는 것은 각각의 제품 지시 확인과 함께 필요한 검토예요.

### 확인이 필요한 한계
중첩 사실만으로 피부 손상이나 특정 원인을 진단하지 않아요.

## syn-sol-0586 — 시간 준수와 다른 제품 중첩 미상

- 내용 해시: `f088f399a7e4d7aa7a75ee6119522b7ca126ade82a05cedde9ef2e383ec6029f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 시간 준수와 다른 제품 중첩 미상 / syn-sol-0176

### 설계한 시나리오 raw

합성 팩을 표시한 시간만큼 사용한 후 제거했어요. 다른 각질관리 제품과 중첩했는지는 기억하지 못해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "label_time_followed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "표시 시간 준수는 확인됐지만 추가 각질관리 중첩은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤에는 손의 건조감에 맞는 보습을 고려할 수 있어요. 손 관리에서는 필요한 손 위생을 유지해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G05@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "adjunct.care_events",
    "raw_span": "합성 팩을 표시한 시간만큼 사용한 후 제거했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "다른 각질관리 제품과 중첩했는지는 기억하지 못해요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
합성 팩의 표시 시간은 지켰지만 다른 각질관리와의 중첩은 아직 판단할 수 없어요 [kb:B-G05@0.6.1].

### 근거 및 이유
표시 시간 준수와 다른 제품을 함께 썼는지는 별개의 행동이에요.

### 확인이 필요한 한계
기억하지 못한 중첩 여부를 사용하지 않았다고 처리하지 않아요.

## syn-sol-0587 — 임의 희석과 표시 지시 예외를 구분

- 내용 해시: `c54584c045b1eda925a3342b6d1310817a12f799551e67701aa182737ce5e0d0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 임의 희석과 표시 지시 예외를 구분 / syn-sol-0167

### 설계한 시나리오 raw

합성 제품 설명서에는 물과 희석해서 쓰라고 적혀 있어요. 실제로 그 지시대로 희석해 사용해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "dilution_with_water_instructed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "dilution_per_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "exception",
      "guidance": "확인된 제조사 희석 지시에 따르는 예외예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "합성 제품 설명서에는 물과 희석해서 쓰라고 적혀 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.mixing",
    "raw_span": "실제로 그 지시대로 희석해 사용해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
이 사례의 희석은 확인된 제품 설명서에 따른 사용으로 구분해요 [kb:B-G04@0.6.1].

### 근거 및 이유
제조사가 명시한 희석 지시를 따르는 경우는 근거 없는 임의 희석과 달라요.

### 확인이 필요한 한계
구체적인 희석 비율은 입력에 없고 이 지시를 다른 제품에 적용할 수 없어요.

## syn-sol-0588 — 제품별 지시 준수와 미공개 농도 분리

- 내용 해시: `c1833ca18c121960842d58f54b08a59d46bd0278cb494931fe74430494357860`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품별 지시 준수와 미공개 농도 분리 / syn-sol-0103

### 설계한 시나리오 raw

얼굴에 쓰는 보습제와 선크림의 용법을 각각 확인해 따르고 있어요. 각 성분의 미공개 농도는 알 수 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "moisturizer_and_sunscreen_instructions_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "instructions_followed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.concentrations": {
      "variable_id": "product.concentrations",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "aligned",
      "guidance": "제품별 확인된 지시를 따르지만 미공개 농도는 비교할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "얼굴에 쓰는 보습제와 선크림의 용법을 각각 확인해 따르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴에 쓰는 보습제와 선크림의 용법을 각각 확인해 따르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.concentrations",
    "raw_span": "각 성분의 미공개 농도는 알 수 없어요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
보습제와 선크림 각각의 확인된 용법을 따르는 현재 행동은 이 항목에서 유지할 수 있어요 [kb:B-G02@0.6.1].

### 근거 및 이유
제품별 사용 지시를 따르는 것과 성분 농도를 비교하는 것은 다른 문제예요.

### 확인이 필요한 한계
미공개 농도는 알 수 없으므로 양이나 효과에서 역산하지 않아요.

## syn-sol-0589 — 별도 보습 필요 불편이 없는 예외

- 내용 해시: `b2d30e723eaecf52f9331ea95f3e3e780fd1ff9227e682dff37cd4b2a370cda7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 별도 보습 필요 불편이 없는 예외 / syn-sol-0003

### 설계한 시나리오 raw

별도 보습제 없이 지내고 건조 불편도 없어요. 세안 직후 꼭 별도 제품을 추가해야 하는지 궁금해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "separate_moisturizer_used": false,
        "dry_discomfort": false,
        "question_add_after_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "별도 보습제를 쓰지 않고 건조 불편도 없지만 별도 보습이 불필요한지까지 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "별도 보습제 없이 지내고 건조 불편도 없어요. 세안 직후 꼭 별도 제품을 추가해야 하는지 궁금해요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
별도 보습제 없이 지내고 건조 불편이 없다는 보고만으로 별도 보습의 필요 여부를 확정하지 않아요 [kb:B-M01@0.6.1].

### 근거 및 이유
세정 뒤 보습 시점은 보습이 필요한 맥락과 실제 사용을 함께 살피는 항목이에요.

### 확인이 필요한 한계
현재 정보로 제품 추가가 필요하다거나 불필요하다고 단정할 수 없어요.

## syn-sol-0590 — 보습 충족과 광보호 도포 요건의 구분

- 내용 해시: `c88fb63c28be350c71c148c62d5f8ea6c3808ec042c01569b01ed5a884e71a5f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 보습 충족과 광보호 도포 요건의 구분 / syn-sol-0057

### 설계한 시나리오 raw

보습 기능을 가진 제품을 하나 쓰면서 건조 불편은 없어요. 그 제품의 보습량만으로 선크림의 광보호 도포 요건까지 충족하는지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "one_moisturizing_product_used": true,
        "dry_discomfort": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "exception",
      "guidance": "보습이 편안하더라도 선크림의 광보호 도포 요건은 별도로 살펴야 해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "보습 기능을 가진 제품을 하나 쓰면서 건조 불편은 없어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "그 제품의 보습량만으로 선크림의 광보호 도포 요건까지 충족하는지는 몰라요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
보습 제품 사용으로 건조 불편이 없더라도 선크림의 광보호 도포 요건은 별도로 살펴야 해요 [kb:B-M03@0.6.1].

### 근거 및 이유
보습 기능의 충족과 광보호에 필요한 사용 요건은 같은 판단이 아니에요.

### 확인이 필요한 한계
제공된 정보만으로 선크림의 실제 도포량이나 요건 충족을 확인할 수 없어요.

## syn-sol-0591 — 무향료 선호 충족과 개인 목록 미대조

- 내용 해시: `edac3f97bfb806e9fedb8e2aa8416343341bffcb0ace08452c63db16c1bc7c25`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 무향료 선호 충족과 개인 목록 미대조 / syn-sol-0015

### 설계한 시나리오 raw

무향료라고 확인된 합성 후보를 새로 고르고 있어요. 개인적으로 알고 있는 알레르겐 목록은 아직 대조하지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "fragrance_free_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "personal_list_not_compared": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G01",
      "status": "aligned",
      "guidance": "무향료 기본 선호는 충족하지만 개인 알레르겐 대조는 별개예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "FDA information discusses fragrance allergens and individual avoidance. A fragrance-free description does not replace checking an individual allergen.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G01@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.fragrance",
    "raw_span": "무향료라고 확인된 합성 후보를 새로 고르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "무향료라고 확인된 합성 후보를 새로 고르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "person.known_allergies",
    "raw_span": "개인적으로 알고 있는 알레르겐 목록은 아직 대조하지 않았어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 무향료 후보는 기본 선호에 부합하지만 개인 알레르겐 목록과는 따로 대조해 주세요 [kb:B-G01@0.6.1].

### 근거 및 이유
향료 관련 표시와 개인이 피해야 하는 물질은 구분해 확인해야 해요 [ref:S15].

### 확인이 필요한 한계
무향료라는 말만으로 모든 개인 알레르겐이 없거나 반응하지 않는다고 보증하지 않아요.

## syn-sol-0592 — 표시 목록과 전 사용자 금지 주장 구분

- 내용 해시: `a8d3656882b145f82128593d25569837838b99e9072712703ca62c3f65b61fa9`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 표시 목록과 전 사용자 금지 주장 구분 / syn-sol-0089

### 설계한 시나리오 raw

표시 성분 목록에 알레르겐으로 알려진 이름이 있어요. 제 개인 알레르기는 확인되지 않았는데 모든 사람에게 금지된 성분이라고 생각했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "listed_allergen_name": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "user_assumes_universal_ban": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시된 이름이 모든 사람에게 금지된다는 뜻은 아니며 개인 알레르기는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "FDA information discusses cosmetic allergens and individual sensitivity. A listed allergen is not automatically prohibited for every person.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.inci",
    "raw_span": "표시 성분 목록에 알레르겐으로 알려진 이름이 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "constraints.preferences",
    "raw_span": "모든 사람에게 금지된 성분이라고 생각했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "person.known_allergies",
    "raw_span": "제 개인 알레르기는 확인되지 않았는데",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
표시 목록에 알레르겐으로 알려진 이름이 있다고 해서 모든 사람에게 금지된 성분이라고 판단하지 않아요 [kb:B-G17@0.6.1].

### 근거 및 이유
알레르겐 표시와 개인별 민감성은 구별해야 해요 [ref:S15].

### 확인이 필요한 한계
개인 알레르기는 확인되지 않았으므로 본인에게 안전하다거나 반응할 것이라고도 단정하지 않아요.

## syn-sol-0593 — 미표시와 완전 부재를 구분

- 내용 해시: `88477a2214392d97839036401ac30a7fdfec4fe6e19dbe1b6946e8fcbb4f387e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 미표시와 완전 부재를 구분 / syn-sol-0089

### 설계한 시나리오 raw

표시에서 특정 알레르겐 이름을 찾지 못했어요. 그래서 제품에 그 성분이 전혀 없다고 결론 내렸어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.label_warnings": {
      "variable_id": "product.label_warnings",
      "state": "known",
      "value": {
        "allergen_name_not_found": true,
        "inferred_absence": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시에서 찾지 못한 사실을 성분의 완전 부재로 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.label_warnings",
    "raw_span": "표시에서 특정 알레르겐 이름을 찾지 못했어요. 그래서 제품에 그 성분이 전혀 없다고 결론 내렸어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
표시에서 이름을 찾지 못한 사실을 그 성분의 완전한 부재로 단정하지 말아 주세요 [kb:B-G17@0.6.1].

### 근거 및 이유
표시에서 확인한 내용과 제품에 무엇이 존재하는지에 대한 확정은 다른 범위예요.

### 확인이 필요한 한계
해당 알레르겐의 정확한 정체나 현행 표시의 완전한 대조 여부는 제공되지 않았어요.

## syn-sol-0594 — 동시 변경과 인과 미확정 및 향후 기록 계획

- 내용 해시: `6c6e887dc5473a463d9729840250020ae2eb5d7fe64058ea96d21cf64c5e8d20`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 동시 변경과 인과 미확정 및 향후 기록 계획 / syn-sol-0022

### 설계한 시나리오 raw

두 제품을 동시에 바꿨지만 불편의 원인을 어느 하나로 정하지 않았어요. 다음에는 변경 시점을 구분해 기록하고 싶어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "two_products_changed_together": true,
        "single_cause_assigned": false,
        "plans_separate_tracking": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G12",
      "status": "unknown",
      "guidance": "동시 변경은 확인됐지만 어느 제품이 원인인지는 정하지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G12@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "routine.change_log",
    "raw_span": "두 제품을 동시에 바꿨지만 불편의 원인을 어느 하나로 정하지 않았어요. 다음에는 변경 시점을 구분해 기록하고 싶어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 동시에 바꾼 사실과 원인을 아직 정하지 않은 상태를 그대로 유지해요 [kb:B-G12@0.6.1].

### 근거 및 이유
앞으로 변경 시점을 구분해 기록하려는 계획은 이후 관찰을 정리하는 데 도움이 될 수 있어요.

### 확인이 필요한 한계
계획은 아직 실행된 기록이 아니며 현재 불편의 원인도 확인되지 않았어요.

## syn-sol-0595 — 계획한 시험과 실제 실행 분리

- 내용 해시: `8783563c5fadc9de56a48d13857dfd490aa18085e49c90d05df718560f76ffe9`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 계획한 시험과 실제 실행 분리 / syn-sol-0011

### 설계한 시나리오 raw

신규 제품의 국소 사용을 계획하고 있으나 아직 시행하지 않았어요. 이 제품의 지침은 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "introduction.local_trial": {
      "variable_id": "introduction.local_trial",
      "state": "known",
      "value": {
        "planned": true,
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "국소 사용은 계획일 뿐이며 제품 지침도 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G11@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "introduction.local_trial",
    "raw_span": "신규 제품의 국소 사용을 계획하고 있으나 아직 시행하지 않았어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "이 제품의 지침은 확인하지 못했어요",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
작은 부위 사용은 아직 계획이며 이미 시행했다고 판단하지 않아요 [kb:B-G11@0.6.1].

### 근거 및 이유
새 제품 도입 방법을 검토할 때 해당 제품의 지시도 확인해야 해요.

### 확인이 필요한 한계
지침이 미확인이라 이 제품의 구체적인 적용 방법을 임의로 정하지 않아요.

## syn-sol-0596 — 간접 세탁물 접촉을 제외한 판단과 원인 미상

- 내용 해시: `73a85efdb7c855c6b6d97868bb1e6aa4f21bdc60fa8f25bc6ada6b08e2d3a1c7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 간접 세탁물 접촉을 제외한 판단과 원인 미상 기존 648에는 B-L01이나 직접적인 얼굴 외 접촉 경로 관찰이 없어요. 0022는 여러 변화와 원인 확정을 구분하는 기능적 참고일 뿐 접촉 경로의 근접 가족은 아니에요. / syn-sol-0022

### 설계한 시나리오 raw

얼굴에 닿는 베갯잇을 새 세제로 세탁했어요. 얼굴에도 불편이 있지만 그 세제가 원인인지는 알 수 없어요. 얼굴용 제품만 보고 세탁물 접촉은 무시했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "environment.indirect_products": {
      "variable_id": "environment.indirect_products",
      "state": "known",
      "value": {
        "new_detergent_pillowcase_touched_face": true,
        "contact_excluded_from_review": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "discomfort_site": "face",
        "cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-L01",
      "status": "difference",
      "guidance": "실제 세탁물 접촉 경로를 제외했지만 세제가 원인이라고 확정할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-L01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "environment.indirect_products",
    "raw_span": "얼굴에 닿는 베갯잇을 새 세제로 세탁했어요. 얼굴에도 불편이 있지만 그 세제가 원인인지는 알 수 없어요. 얼굴용 제품만 보고 세탁물 접촉은 무시했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "skin.distribution",
    "raw_span": "얼굴에도 불편이 있지만 그 세제가 원인인지는 알 수 없어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품뿐 아니라 얼굴에 닿는 세탁물의 경로도 검토에 포함해 보세요 [kb:B-L01@0.6.1].

### 근거 및 이유
새 세제로 세탁한 베갯잇이 얼굴에 닿는다고 확인됐지만 이 경로를 제외했어요.

### 확인이 필요한 한계
접촉과 불편이 함께 있다는 사실만으로 세제가 원인이라고 결론 내리지 않아요.

## syn-sol-0597 — 팩 지시 준수와 별도 지시 부재

- 내용 해시: `ab4ec3deb5f8ad3c50f4f17d9e4f4e784853b4aa27ed37797f33765e8724d699`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 팩 지시 준수와 별도 지시 부재 / syn-sol-0102

### 설계한 시나리오 raw

합성 팩 표시의 제거 지시를 따르고 있어요. 의료진이 따로 지시한 것은 없다고 말했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "합성 팩",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "pack_removal_instruction_followed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "separate_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "aligned",
      "guidance": "해당 팩의 제거 지시를 따르고 별도 의료진 지시는 없다고 보고했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.type",
    "raw_span": "합성 팩 표시의 제거 지시를 따르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "합성 팩 표시의 제거 지시를 따르고 있어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "person.clinician_plan",
    "raw_span": "의료진이 따로 지시한 것은 없다고 말했어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인한 합성 팩의 제거 지시를 따르는 현재 행동은 이 항목에서 유지할 수 있어요 [kb:B-G03@0.6.1].

### 근거 및 이유
제품 유형에 맞는 표시를 따르고 별도 의료진 지시는 없다고 보고했어요.

### 확인이 필요한 한계
제거 지시의 구체적인 내용은 제공되지 않았고 다른 제품으로 확대할 수 없어요.

## syn-sol-0598 — 접촉시간과 구분되는 용도 밖 반복 닦기

- 내용 해시: `e6ec9f5ca4282be334abff75b4c4030f9cb23d06fda41152f5ab4a6dceb37f5d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 접촉시간과 구분되는 용도 밖 반복 닦기 / syn-sol-0181

### 설계한 시나리오 raw

닦아내는 관리 제품을 설명된 용도 밖에서 하루 여러 번 사용해요. 사용 목적을 물었더니 특별한 이유는 없다고 했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "out_of_scope_repeated_wiping": true,
        "reason": "none"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "difference",
      "guidance": "설명된 용도 밖의 반복 닦기를 특별한 이유 없이 하고 있어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "adjunct.care_events",
    "raw_span": "닦아내는 관리 제품을 설명된 용도 밖에서 하루 여러 번 사용해요. 사용 목적을 물었더니 특별한 이유는 없다고 했어요",
    "connection": "원문에 명시된 해당 관찰"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
표시된 용도 밖에서 관리 제품으로 여러 번 닦는 행동을 재검토해 주세요 [kb:B-G05@0.6.1].

### 근거 및 이유
확인된 용도와 실제 반복 행동의 차이를 살펴야 하며 별도 이유도 보고되지 않았어요.

### 확인이 필요한 한계
횟수의 정확한 수치나 그 행동으로 인한 개인 반응은 확인되지 않았어요.

## syn-sol-0599 — 계획과 실행을 분리한 용량 검토

- 내용 해시: `23c902691f58b58e4f7b3e577b0ca67512f7e03930f2267d65f184fa52e6cad5`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 계획과 실행을 분리한 용량 검토 / syn-sol-0107

### 설계한 시나리오 raw

제품의 지시를 모르지만 모든 제품을 똑같은 펌프 수로 줄이려고 해요. 아직 양을 바꾸지는 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "uniform_reduction_planned": true,
        "change_executed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "일괄 감량은 계획이고 실행되지 않았으며 제품별 지시는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "dose.proxy_amount",
    "raw_span": "모든 제품을 똑같은 펌프 수로 줄이려고 해요. 아직 양을 바꾸지는 않았어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품의 지시를 모르지만",
    "connection": "원문에서 해당 정보 미상"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
모든 제품을 같은 펌프 수로 줄이기 전 제품별 지시를 확인해 주세요 [kb:B-G02@0.6.1].

### 근거 및 이유
서로 다른 용기와 제품에 일괄 기준을 적용하는 것은 각각의 용법을 반영하지 못할 수 있어요.

### 확인이 필요한 한계
감량은 계획이며 아직 실행하지 않았어요. 현재 지시가 미상이므로 구체적 펌프 수는 정하지 않아요.

## syn-sol-0600 — 최초 도포 유지와 재도포 응답 거절

- 내용 해시: `1c14fcda50dc76facbafe655719360b5133904f3b8557f43c12809949d0c91d4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 최초 도포 유지와 재도포 응답 거절 / syn-sol-0069

### 설계한 시나리오 raw

보습제와 선크림을 따로 바르면 답답하지만 선크림을 처음 바르는 행동은 유지해요. 재도포 행동은 답하기를 거절했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "layering_feels_heavy": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "initial_sunscreen_application_maintained": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "최초 도포는 유지하지만 재도포 행동은 응답을 거절했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "보습제와 선크림을 따로 바르면 답답하지만",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "method.current_routine",
    "raw_span": "선크림을 처음 바르는 행동은 유지해요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "재도포 행동은 답하기를 거절했어요",
    "connection": "원문에서 해당 답변 거절"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
처음 선크림을 바르는 행동은 유지된다고 확인됐지만 재도포 변화는 판단하지 않아요 [kb:B-I02@0.6.1].

### 근거 및 이유
중첩의 답답함, 최초 도포, 재도포는 서로 다른 관찰이에요.

### 확인이 필요한 한계
재도포 답변은 거절하셨으므로 그 행동을 유지 또는 생략으로 추정하지 않아요.

## syn-sol-0601 — 건조감과 보습 후 편안함 응답 거절

- 내용 해시: `84495942d4fce483363aa0f86d07db3d333df9ff081f8eb365c245360f0a554b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 건조감과 보습 후 편안함 응답 거절 / syn-sol-0062

### 설계한 시나리오 raw

보습 후 편안한지 알려주고 싶지 않아요. 가벼운 건조감 자체는 있다고 말했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "known",
      "value": "mild",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "가벼운 건조감은 보고했지만 보습 후 편안함은 답변을 거절했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.dryness",
    "raw_span": "가벼운 건조감 자체는 있다고 말했어요",
    "connection": "원문에 명시된 해당 관찰"
  },
  {
    "variable_id": "moisturizing.comfort",
    "raw_span": "보습 후 편안한지 알려주고 싶지 않아요",
    "connection": "원문에서 해당 답변 거절"
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
가벼운 건조감은 확인됐지만 현재 보습 방법의 적절성은 아직 판단하기 어려워요 [kb:B-M02@0.6.1].

### 근거 및 이유
보습 후 편안함은 건조감 자체와 구별되는 정보예요.

### 확인이 필요한 한계
편안함에 대한 답변을 원하지 않으셨으므로 불편이 없다고 대체하지 않아요.

## syn-sol-0602 — 얼굴 볼 제외와 모자 가림

- 내용 해시: `46b87a99676ae3257c44764f7744a05fe48aa7536c34356700bd1da153ca41dd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 얼굴 내 실제 누락과 모자의 실제 가림 범위를 함께 확인해요. / syn-sol-0017

### 설계한 시나리오 raw

야외에서 얼굴이 노출돼요. 얼굴에 바르면서 볼은 일부러 빼요. 모자를 썼지만 볼은 가리지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "known",
      "value": [
        "cheeks"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "hat_used": true,
        "cheeks_covered": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "얼굴에 도포하면서 노출된 볼을 의도적으로 제외한 차이예요. 모자를 썼다는 사실은 볼이 가려졌다는 뜻이 아니에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "Hand skin can become dry with frequent washing. Hand moisturizers are discussed in general hand-care guidance.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.exposed_sites",
    "raw_span": "야외에서 얼굴이 노출돼요.",
    "connection": "실제 노출 부위를 얼굴로 확인해요."
  },
  {
    "variable_id": "sun.coverage_gaps",
    "raw_span": "얼굴에 바르면서 볼은 일부러 빼요.",
    "connection": "얼굴의 볼을 도포에서 의도적으로 제외해요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "모자를 썼지만 볼은 가리지 않아요.",
    "connection": "모자 사용과 볼 가림의 부재를 구분해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
볼이 노출되는데 일부러 도포에서 빼고 있어요. 제품 지침을 확인해 해당 부위를 빠뜨리지 않는 방향으로 살펴보세요 [kb:B-P02@0.6.1].

### 근거 및 이유
모자를 써도 볼을 가리지 않는다고 하셨으므로 모자 착용만으로 그 부분이 가려졌다고 볼 수 없어요. 광보호에는 도포와 그늘·의복을 함께 고려해요 [ref:S05].

### 확인이 필요한 한계
제품의 부위별 제한과 실제 보호 수준은 확인되지 않았어요.

## syn-sol-0603 — 도포 계획과 아직 미상인 노출

- 내용 해시: `1d57947d34bccad0bc216b7f2824b35920417b618357c616381fcba291d73917`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 야외 노출에 대한 확정 관찰 대신 미실행 계획과 노출 미상을 구분해요. / syn-sol-0017

### 설계한 시나리오 raw

얼굴에 선제품을 바를 계획이지만 아직 바르지 않았어요. 오늘 얼굴의 실제 야외 노출은 아직 알 수 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sun_application": {
          "planned": true,
          "performed": false
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "도포는 계획이며 실제 노출이 아직 미상이어서 도포 누락 여부를 판단할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴에 선제품을 바를 계획이지만 아직 바르지 않았어요.",
    "connection": "계획과 현재까지의 미실행을 구분해요."
  },
  {
    "variable_id": "sun.exposed_sites",
    "raw_span": "오늘 얼굴의 실제 야외 노출은 아직 알 수 없어요.",
    "connection": "미래 노출을 없음으로 단정하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 바를 계획과 실제 야외 노출을 구분해 주세요. 노출이 확인되지 않아 빠진 부위가 있다고 판단하지 않아요 [kb:B-P02@0.6.1].

### 근거 및 이유
선제품 사용을 계획한 것과 실제로 바른 것은 달라요. 광보호는 실제 노출과 제품 지침을 함께 보고 판단해요 [ref:S05].

### 확인이 필요한 한계
오늘의 실제 노출 범위는 아직 미상이에요.

## syn-sol-0604 — 수영 후 닦고 재도포하지 않음

- 내용 해시: `9c77ffd4fda9bbc124776f7fff3f85f7585cb5a356c153e2c7c4bd289efcab31`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 수영과 수건 접촉은 비슷하지만 이후 재도포하지 않은 반대 행동이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0065

### 설계한 시나리오 raw

야외 수영을 했어요. 물에서 나온 뒤 수건으로 닦았어요. 그 후에도 야외에 계속 있었어요. 그 뒤 선제품을 다시 바르지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "continues_after_swimming": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "수영과 수건 접촉 뒤 야외 노출이 이어졌는데 재도포하지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S23",
      "text": "A shaving routine can include attention to the skin before shaving. Shaving tools require appropriate handling.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S23"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.water_contact",
    "raw_span": "야외 수영을 했어요.",
    "connection": "실제 물 접촉을 확인해요."
  },
  {
    "variable_id": "sun.towel_contact",
    "raw_span": "물에서 나온 뒤 수건으로 닦았어요.",
    "connection": "수건 접촉을 확인해요."
  },
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "그 후에도 야외에 계속 있었어요.",
    "connection": "물 접촉 후에도 야외 노출이 이어졌어요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "그 뒤 선제품을 다시 바르지 않았어요.",
    "connection": "접촉 뒤 재도포하지 않은 실제 행동이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
수영 후 닦고도 야외에 머무는 동안 다시 바르지 않았어요. 다음에는 제품 지침을 확인해 물 접촉과 닦임 이후의 재도포를 고려해 주세요 [kb:B-P03@0.6.1].

### 근거 및 이유
수영과 수건 접촉 뒤에도 노출이 이어진 실제 상황을 함께 살펴요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
실제 남은 보호 수준은 측정되지 않았고 제품별 지침도 제공되지 않았어요.

## syn-sol-0605 — 발한 후 야외 노출 종료

- 내용 해시: `09399eb156511354b434e454f9e3464748bbda91c97568ab63e6146136301272`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 발한 뒤 실제 노출 종료와 재도포 미상을 따로 확인해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0005

### 설계한 시나리오 raw

운동 중 땀을 많이 흘렸어요. 그 뒤 실내로 들어와 야외에 다시 나가지 않았어요. 다시 발랐는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.sweat": {
      "variable_id": "sun.sweat",
      "state": "known",
      "value": {
        "heavy": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "continues_after_sweating": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "심한 발한은 있었지만 이후 야외 노출은 끝났고 재도포 행동은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.sweat",
    "raw_span": "운동 중 땀을 많이 흘렸어요.",
    "connection": "실제 심한 발한이 보고됐어요."
  },
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "그 뒤 실내로 들어와 야외에 다시 나가지 않았어요.",
    "connection": "발한 뒤 야외 노출이 이어지지 않았어요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "다시 발랐는지는 기억나지 않아요.",
    "connection": "재도포 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
땀을 많이 흘린 뒤 실내로 들어와 야외에 돌아가지 않았다는 점을 함께 고려해요. 재도포 여부는 기억나지 않으므로 하지 않았다고 판단하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
재도포 검토에는 손실 계기뿐 아니라 이후 노출이 이어지는지도 중요해요 [ref:S05].

### 확인이 필요한 한계
실제로 다시 발랐는지는 미상이에요.

## syn-sol-0606 — 야외 발한 뒤 재도포 미상

- 내용 해시: `49fa257b0ab172507f826774d4694e80beed4c3f96cf9c5c3c073b2fb2faea9b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 같은 발한 상황에서 재도포를 하지 않았다는 사실 대신 행동 미상이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0005

### 설계한 시나리오 raw

오래 야외에 있었어요. 땀이 많이 났어요. 그 뒤 다시 발랐는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.sweat": {
      "variable_id": "sun.sweat",
      "state": "known",
      "value": {
        "heavy": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "오랜 야외 노출과 심한 발한은 확인되지만 재도포 실행 여부는 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "오래 야외에 있었어요.",
    "connection": "장시간 야외 노출을 확인해요."
  },
  {
    "variable_id": "sun.sweat",
    "raw_span": "땀이 많이 났어요.",
    "connection": "실제 심한 발한을 확인해요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "그 뒤 다시 발랐는지는 기억나지 않아요.",
    "connection": "재도포를 하지 않았다고 추정하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
긴 야외 활동 중 땀이 많이 났지만 이후 다시 발랐는지는 미상이에요. 앞으로는 활동 중 재도포 여부와 제품 지침을 함께 확인해 보세요 [kb:B-P03@0.6.1].

### 근거 및 이유
심한 발한은 광보호를 다시 살펴볼 계기지만 그 자체가 재도포하지 않았다는 증거는 아니에요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
기억나지 않는 행동을 없었던 일로 바꾸지 않아요.

## syn-sol-0607 — 야외 발한 때 표시대로 재도포

- 내용 해시: `f890b0108ac993a96a75211503e2331a589579cfc2cca8976eb290cd456a44be`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 심한 발한 후 재도포하지 않은 사례와 달리 재도포 실행을 확인해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0005

### 설계한 시나리오 raw

야외 작업을 오래 했어요. 땀을 많이 흘렸어요. 땀을 많이 흘릴 때마다 제품 표시 지침대로 다시 발랐어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.sweat": {
      "variable_id": "sun.sweat",
      "state": "known",
      "value": {
        "heavy": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "performed": true,
        "follows_label": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "aligned",
      "guidance": "심한 발한이 있는 야외 작업에서 표시 지침에 맞추어 재도포했다고 보고해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S10",
      "text": "Sleep is a subject of health research. Reports about sleep do not establish an individual cosmetic outcome.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/25266053/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "관찰적 집단 비교. 인종·성별·표본·수면 분류가 제한적. 수면 연장의 개인 피부 개선량을 추정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S10"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "야외 작업을 오래 했어요.",
    "connection": "장시간 야외 작업을 확인해요."
  },
  {
    "variable_id": "sun.sweat",
    "raw_span": "땀을 많이 흘렸어요.",
    "connection": "심한 발한을 확인해요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "땀을 많이 흘릴 때마다 제품 표시 지침대로 다시 발랐어요.",
    "connection": "실제 재도포와 표시 지침 준수를 보고했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
야외 작업 중 심하게 땀을 흘릴 때 표시 지침대로 재도포한 방법은 해당 항목에서 유지할 수 있어요 [kb:B-P03@0.6.1].

### 근거 및 이유
지속 노출과 발한 상황에 맞춰 재도포를 확인하는 접근이에요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
이 보고만으로 개인의 실제 보호 수준을 측정하거나 보증할 수는 없어요.

## syn-sol-0608 — 그늘과 모자의 의식적 배제

- 내용 해시: `518c7db9e51fcafcc2acd4edaa393ad1a9cb99815fd739999874b8368ec58c7b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 그늘뿐 아니라 모자도 이용 가능하지만 둘 다 배제한 상황이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0063

### 설계한 시나리오 raw

오랫동안 야외에서 기다렸어요. 그늘과 모자를 쓸 수 있었지만 선크림만 충분하다고 생각해 둘 다 쓰지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "shade_available": true,
        "hat_available": true,
        "shade_used": false,
        "hat_used": false,
        "reason": "선크림만으로 충분"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "difference",
      "guidance": "오랜 야외 노출에서 이용 가능한 그늘과 모자를 선제품만으로 충분하다며 모두 배제했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "오랫동안 야외에서 기다렸어요.",
    "connection": "지속적인 야외 노출을 확인해요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "그늘과 모자를 쓸 수 있었지만 선크림만 충분하다고 생각해 둘 다 쓰지 않았어요.",
    "connection": "이용 가능한 두 수단을 명시적으로 배제했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
오래 기다리는 동안 이용 가능한 그늘이나 모자를 함께 활용하는 방향을 살펴보세요 [kb:B-P04@0.6.1].

### 근거 및 이유
선제품만으로 충분하다는 생각으로 두 수단을 모두 제외했다고 하셨어요. 광보호에는 비제품 수단도 함께 고려할 수 있어요 [ref:S05].

### 확인이 필요한 한계
실제 환경의 변화나 다른 제약은 제공되지 않았어요.

## syn-sol-0609 — 긴 소매 불가와 그늘 휴식

- 내용 해시: `36bc8dbbebf510f7ebc76ff03bc1f335f21c7b6a49a7733868ce6f7a97e92608`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 그늘의 이용 가능성뿐 아니라 실제 이용까지 확인해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0071

### 설계한 시나리오 raw

야외 근무가 오래 이어져요. 근무복 규정 때문에 긴 소매를 입을 수 없어요. 휴식할 때 이용 가능한 그늘에서 실제로 쉬어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.burden": {
      "variable_id": "constraints.burden",
      "state": "known",
      "value": {
        "long_sleeves_not_feasible_due_to_work": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "shade_break_available": true,
        "shade_break_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "aligned",
      "guidance": "긴 소매를 입을 수 없는 제약 속에서 휴식할 때 실제로 그늘을 이용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S11",
      "text": "Stress is discussed in health research. Individual responses are not determined by a general description.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/11511309/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "급성 실험과 테이프 스트리핑 후 회복 지표. 만성 스트레스 점수로 개인 발진의 원인을 확정할 수 없음. 연구별 군/프로토콜을 분리."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S11"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "야외 근무가 오래 이어져요.",
    "connection": "오랜 야외 근무를 확인해요."
  },
  {
    "variable_id": "constraints.burden",
    "raw_span": "근무복 규정 때문에 긴 소매를 입을 수 없어요.",
    "connection": "의복 선택 제약을 확인해요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "휴식할 때 이용 가능한 그늘에서 실제로 쉬어요.",
    "connection": "이용 가능성뿐 아니라 실제 사용을 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
긴 소매를 입기 어려운 근무 조건에서 쉬는 시간에 그늘을 실제로 이용하는 방식은 유지할 수 있어요 [kb:B-P04@0.6.1].

### 근거 및 이유
실행 가능한 보호수단을 활용하는 것이며, 그늘과 의복은 선제품을 보완하는 선택지예요 [ref:S05].

### 확인이 필요한 한계
근무복 제약을 무시해 긴 소매를 강요하지 않아요. 개인의 실제 보호 수준은 미측정이에요.

## syn-sol-0610 — 보완 수단 가능성 답변 거절

- 내용 해시: `5ab75657b8e2dd9968318a533d302144f81b39e7fba1871f1d32440ae1701cfd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 가능한 그늘을 배제한 관찰이 아니라 가능성 자체에 대한 답변 거절이에요. / syn-sol-0063

### 설계한 시나리오 raw

오래 야외에 있었어요. 그늘이나 모자를 쓸 수 있었는지는 답하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "보완 수단의 가능성에 대해 답변을 거절했으므로 이용 가능성이나 배제 여부를 판단할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen is one part of a sun protection approach that also includes shade and protective clothing. The FDA discusses application and reapplication in relation to sun exposure.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "오래 야외에 있었어요.",
    "connection": "장시간 야외 노출을 확인해요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "그늘이나 모자를 쓸 수 있었는지는 답하고 싶지 않아요.",
    "connection": "가능한 수단에 대한 답변 거절이며 사용하지 않았다는 뜻이 아니에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
오래 야외에 있었지만 그늘이나 모자에 관한 답변은 원하지 않으셨으므로 더 묻지 않아도 돼요 [kb:B-P04@0.6.1].

### 근거 및 이유
보완 수단의 가능성과 사용 여부가 확인되지 않아 이를 배제했다고 판단하지 않아요. 그늘과 의복은 일반적인 광보호 선택지예요 [ref:S05].

### 확인이 필요한 한계
답변 거절은 이용할 수 없었다거나 사용하지 않았다는 뜻이 아니에요.

## syn-sol-0611 — 뜨거운 차 보관과 미측정 조건

- 내용 해시: `79b5cc7b237c007bdbc80bfda06cc945859625d380fa853450852d403740b686`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 반복 보관을 추가로 확인하면서 실제 온도와 시간은 미상으로 남겨요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0021

### 설계한 시나리오 raw

선제품을 뜨거운 차 안에 자주 두었지만 실제 온도와 매번 둔 시간은 몰라요. 보관 지침은 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "hot_car_reported": true,
        "repeated": true,
        "measured_temperature": null,
        "duration_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "exception",
      "guidance": "뜨거운 차 보관은 보고됐지만 과거 온도와 기간이 미상이므로 해당 이력의 예외 조건을 따로 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "선제품을 뜨거운 차 안에 자주 두었지만 실제 온도와 매번 둔 시간은 몰라요.",
    "connection": "반복된 뜨거운 차 보관은 확인되나 실제 온도와 시간은 미상이에요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "보관 지침은 확인하지 못했어요.",
    "connection": "제품 보관 지침을 확인하지 못했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
뜨거운 차에 자주 두었던 이력을 확인하고 앞으로는 해당 제품의 보관 지침을 살펴주세요 [kb:B-S01@0.6.1].

### 근거 및 이유
열은 화장품 보관에 영향을 줄 수 있어요 [ref:S06]. 과거 노출의 실제 온도와 시간은 미상이어서 이력의 예외를 따로 고려해요.

### 확인이 필요한 한계
이 정보만으로 현재 제품이 변질됐거나 기능이 사라졌다고 확정하지 않아요.

## syn-sol-0612 — 배송 열 이력 미상

- 내용 해시: `b0b6b900c8837a3d1c7b686241ae6cc2171ec1c4e3c099370ecde9f01662373a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 과거 운송 열 미상과 현재 열린 용기라는 별도 실제 행동을 함께 판단해요. / syn-sol-0051

### 설계한 시나리오 raw

배송 중 열에 노출됐는지 몰라요. 지금은 직사광선을 피하지만 용기를 계속 열어 두어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "transport_history_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "currently_away_from_sunlight": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "left_open": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "과거 운송 열 이력은 미상이지만 현재 용기를 계속 열어 둔 보관 상태는 확인돼요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    },
    {
      "evidence_ref": "ref:S12",
      "text": "Diet has been examined in a small research study. Its findings concern the studied population and conditions.",
      "scope": "non_clinical_only",
      "source_url": "https://www.medicaljournals.se/acta/content/abstract/10.2340/00015555-1346",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "특정 질환·식이패턴·기간의 소규모 연구. 한 번의 음식 섭취와 다음날 증상을 연결하거나 모든 피부 건조·민감 반응에 확장하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": [
    "ref:S12"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "배송 중 열에 노출됐는지 몰라요.",
    "connection": "과거 운송 열 노출을 미상으로 기록해요."
  },
  {
    "variable_id": "storage.light_air",
    "raw_span": "지금은 직사광선을 피하지만 용기를 계속 열어 두어요.",
    "connection": "현재 빛 회피가 과거 온도를 증명하지 않아요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "지금은 직사광선을 피하지만 용기를 계속 열어 두어요.",
    "connection": "현재 열린 용기 상태를 실제 보고해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
용기를 계속 열어 두는 현재 보관을 재검토하고 제품 지침을 확인해 주세요 [kb:B-S01@0.6.1].

### 근거 및 이유
현재 직사광선을 피하는 것과 용기를 열어 둔 행동은 별개예요. 제품 보관과 취급 상태를 함께 살펴봐요 [ref:S06].

### 확인이 필요한 한계
과거 배송 중 열 노출은 미상이며 현재 품질도 확정할 수 없어요.

## syn-sol-0613 — 직사광선과 열린 용기

- 내용 해시: `712d449dac47be11177e28a8cd2cb13f799bc86c60ca669dba8a420cb28594b2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 차량 열 노출 대신 빛과 열린 용기라는 두 조건을 확인해요. / syn-sol-0021

### 설계한 시나리오 raw

제품을 창가 직사광선 아래 계속 두었어요. 뚜껑도 계속 열어 두었어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "direct_sunlight_continuous": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "left_open": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "직사광선 아래 계속 두고 뚜껑도 열어 둔 보관 행동을 확인했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.light_air",
    "raw_span": "제품을 창가 직사광선 아래 계속 두었어요.",
    "connection": "빛에 계속 노출한 사실을 기록해요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "뚜껑도 계속 열어 두었어요.",
    "connection": "용기를 계속 열어 둔 행동이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제품은 직사광선을 피하고 용기 뚜껑을 닫아 보관하는 방향을 확인해 주세요 [kb:B-S01@0.6.1].

### 근거 및 이유
지속적인 빛 노출과 열린 용기는 보관·취급 상태를 살펴볼 이유가 돼요 [ref:S06].

### 확인이 필요한 한계
관찰된 보관 행동만으로 제품이 변질됐다고 확정하지 않아요.

## syn-sol-0614 — 표시 보관 지침 준수

- 내용 해시: `9e4947352c8c85f8c6a6a98d08232dea6fc028b7c8e93ad3fa0028dac9e905fa`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 제품 지침과 현재 보관의 일치가 확인돼요. / syn-sol-0051

### 설계한 시나리오 raw

용기에는 서늘한 곳에 보관하라고 표시돼 있어요. 그 지침에 맞는 서늘한 곳에 두어요. 직사광선은 피하고 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "storage": "cool_place"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "follows_storage_label": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "currently_away_from_sunlight": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "aligned",
      "guidance": "확인된 제품 지침에 맞게 보관하고 직사광선도 피한다고 보고해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    },
    {
      "evidence_ref": "ref:S13",
      "text": "Some skin conditions can involve dryness. A general description does not establish a diagnosis for an individual.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/diseases/eczema/types/atopic-dermatitis/symptoms",
      "locator": "가려움·수면 문제 관련 절",
      "checked_on": "2026-11-04",
      "limitations": "이미 해당 질환 맥락의 설명. 가려움이나 수면 문제로 아토피 피부염을 자동 진단하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": [
    "ref:S13"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "용기에는 서늘한 곳에 보관하라고 표시돼 있어요.",
    "connection": "해당 제품의 보관 지침을 확인해요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "그 지침에 맞는 서늘한 곳에 두어요.",
    "connection": "표시된 조건에 맞춘 현재 보관이에요."
  },
  {
    "variable_id": "storage.light_air",
    "raw_span": "직사광선은 피하고 있어요.",
    "connection": "현재 직사광선 회피를 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 서늘한 장소 지침을 따르고 직사광선을 피하는 현재 보관은 이 항목에서 유지할 수 있어요 [kb:B-S01@0.6.1].

### 근거 및 이유
제품별 지침과 열·빛 노출을 함께 살펴보는 접근이에요 [ref:S06].

### 확인이 필요한 한계
지침에 맞춘 보관만으로 현재 품질이나 안정성이 인증되는 것은 아니에요.

## syn-sol-0615 — 두 용기의 개봉 순서 미상

- 내용 해시: `7c9aed6fe30aa03cd2723e868c7f9598595d8f69235273373500b7174674bba5`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: A는 개봉일 미상이나 B의 밀봉은 실제 확인돼 별도 용기 이력을 구분해요. / syn-sol-0052

### 설계한 시나리오 raw

같은 제품의 A와 B 두 용기가 있어요. 두 용기의 개봉 후 안내는 보여요. A는 이미 열었지만 개봉일이 기억나지 않고 B는 밀봉 상태예요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "containers": [
          "A",
          "B"
        ],
        "same_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "pao_visible": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "storage.seal_integrity": {
      "variable_id": "storage.seal_integrity",
      "state": "known",
      "value": {
        "container_b_sealed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "container_a_opened": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "용기 A는 이미 개봉했지만 개봉일이 미상이고 B는 밀봉 상태여서 각 용기의 이력을 구분해야 해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.identity",
    "raw_span": "같은 제품의 A와 B 두 용기가 있어요.",
    "connection": "동일 제품의 별도 용기 두 개를 확인해요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "두 용기의 개봉 후 안내는 보여요.",
    "connection": "표시가 보인다는 사실만 확인해요."
  },
  {
    "variable_id": "storage.opened_at",
    "raw_span": "A는 이미 열었지만 개봉일이 기억나지 않고 B는 밀봉 상태예요.",
    "connection": "용기별 개봉 순서는 미상이에요."
  },
  {
    "variable_id": "storage.seal_integrity",
    "raw_span": "A는 이미 열었지만 개봉일이 기억나지 않고 B는 밀봉 상태예요.",
    "connection": "B의 밀봉과 A의 미상 개봉일을 구분해요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "A는 이미 열었지만 개봉일이 기억나지 않고 B는 밀봉 상태예요.",
    "connection": "A가 이미 개봉된 사실이며 개봉 날짜를 알고 있다는 뜻은 아니에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
A는 개봉일이 기억나지 않지만 B는 밀봉 상태라고 확인했어요. 두 용기의 이력을 따로 유지해 주세요 [kb:B-S02@0.6.1].

### 근거 및 이유
동일 제품이라도 각 용기의 개봉 이력과 표시를 연결해 판단해요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
A의 개봉일은 미상이며 B가 밀봉됐다는 사실만으로 현재 품질을 인증하지 않아요.

## syn-sol-0616 — 개봉일은 알고 해당 안내는 미상

- 내용 해시: `d4d1b99690237bc32eadf7361458df746dcc7835a7f8e16ae639c61ec282705b`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: A 개봉일은 알지만 발견한 사용 안내가 A의 실제 버전과 일치하지 않아요. / syn-sol-0123

### 설계한 시나리오 raw

용기 A를 언제 열었는지 알아요. 이 용기는 A예요. 현재 A의 버전은 2이고 찾아낸 개봉 후 안내는 이전 버전 1에 해당해요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "known": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-a",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "current_container_version": "2",
        "found_guidance_version": "1",
        "match": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "용기 A의 개봉일은 알지만 해당 버전의 개봉 후 안내가 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    },
    {
      "evidence_ref": "ref:S24",
      "text": "Fragrance-free product selection can be considered in general skin care. A label description is not a universal guarantee.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/razor-bump-remedies",
      "locator": "면도날/전기헤드 지침 구분, 과도한 압력 회피, 면도 후 제품이 따갑거나 화끈거리면 중단/대안, 지속 문제의 상담에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "특정 면도 돌기 대상의 안내. 모든 사용자에게 면도빈도·브러시·1–2분 준비시간·습식 전기면도를 강제하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": [
    "ref:S24"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.opened_at",
    "raw_span": "용기 A를 언제 열었는지 알아요.",
    "connection": "해당 용기의 개봉일이 알려져 있어요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "이 용기는 A예요.",
    "connection": "관찰이 용기 A에 속해요."
  },
  {
    "variable_id": "product.version",
    "raw_span": "현재 A의 버전은 2이고 찾아낸 개봉 후 안내는 이전 버전 1에 해당해요.",
    "connection": "해당 용기와 발견한 안내의 버전 불일치를 확인해요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "현재 A의 버전은 2이고 찾아낸 개봉 후 안내는 이전 버전 1에 해당해요.",
    "connection": "현재 버전의 안내는 확인되지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
용기 A의 현재 버전에 맞는 개봉 후 안내를 확인하기 전에는 찾은 이전 버전 안내를 적용하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
개봉일을 알아도 발견한 안내와 용기 버전이 다르면 해당 용기의 기간과 바로 비교할 수 없어요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
버전 2의 개봉 후 지침은 미상이며 버전 1에서 추정하지 않아요.

## syn-sol-0617 — 미실행 소분 계획

- 내용 해시: `d5b9cc69ffddb3152cf0c0ef70bcbd466d09d58c65a5bb331f47ce4064d81a0a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 소분 전 공병의 물기는 확인되지만 원제품으로 옮기지는 않았어요. / syn-sol-0053

### 설계한 시나리오 raw

다른 공병에 옮길까 생각하지만 아직 옮기지 않았어요. 그 공병에는 물기가 남아 있어요. 제조사의 소분 지침도 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.decanting": {
      "variable_id": "storage.decanting",
      "state": "known",
      "value": {
        "planned": true,
        "already_done": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "visible_water_remaining": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "unknown",
      "guidance": "소분은 아직 계획이며 용기 적합성과 제조사 지침은 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.decanting",
    "raw_span": "다른 공병에 옮길까 생각하지만 아직 옮기지 않았어요.",
    "connection": "소분 계획과 실제 미실행을 구분해요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제조사의 소분 지침도 확인하지 못했어요.",
    "connection": "제조사 지침은 미확인이에요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "그 공병에는 물기가 남아 있어요.",
    "connection": "공병의 실제 물기이며 원제품 물 첨가로 바꾸지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
아직 소분하지 않았고 공병에 물기가 남아 있어요. 옮기기 전 제조사 지침과 공병 적합성을 확인해 주세요 [kb:B-S03@0.6.1].

### 근거 및 이유
공병의 물기와 실제 원제품에 물을 넣은 행동은 다르며 아직 옮기지 않았다고 하셨어요 [kb:B-S03@0.6.1].

### 확인이 필요한 한계
제조사 소분 지침과 공병의 적합성은 미상이에요.

## syn-sol-0618 — 원제품에 물 첨가

- 내용 해시: `88a68b33a986c437b3d05296dd7ddc18a3dccd8529ee00671039ef1943302867`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 물 첨가 부정 사례와 달리 원제품에 실제 물을 첨가했어요. / syn-sol-0060

### 설계한 시나리오 raw

제품에 물을 직접 섞어 묽게 만들었어요. 제조사 희석 지침은 확인하지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": {
        "water_added_to_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "difference",
      "guidance": "제조사 희석 지침을 확인하지 않은 채 제품에 물을 직접 첨가했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    },
    {
      "evidence_ref": "ref:S25",
      "text": "Moisturizer guidance discusses different product forms. Individual preferences can differ.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": [
    "ref:S25"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.water_ingress",
    "raw_span": "제품에 물을 직접 섞어 묽게 만들었어요.",
    "connection": "원제품에 실제로 물을 넣었어요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제조사 희석 지침은 확인하지 않았어요.",
    "connection": "허용된 희석 지침은 미확인이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
원제품에 물을 직접 섞은 행동은 중단하고 해당 제품의 제조사 안내를 확인해 주세요 [kb:B-S03@0.6.1].

### 근거 및 이유
물 첨가와 취급은 제품 관리에서 따로 살펴봐야 해요 [ref:S06].

### 확인이 필요한 한계
희석 지침은 확인되지 않았고 이 관찰만으로 실제 오염이나 위해를 확정하지 않아요.

## syn-sol-0619 — 제조사 지침대로 리필

- 내용 해시: `16edbae888d24ee912a3a23553876ffd81529925f48fa614e4fd7dfac88c93d2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 단순 계획이 아니라 제조사 지침에 따른 실제 리필이에요. / syn-sol-0053

### 설계한 시나리오 raw

제조사가 허용한 리필 지침대로 리필했어요. 용기를 세척하고 완전히 말린 뒤 리필했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.decanting": {
      "variable_id": "storage.decanting",
      "state": "known",
      "value": {
        "refilled": true,
        "follows_manufacturer_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "cleaned_and_dried": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "exception",
      "guidance": "제조사 지침에 따른 리필이며 용기를 세척하고 건조했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Heat and sunlight can affect cosmetic shelf life. Appropriate storage and handling are discussed as factors, not proof of the stability of an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.decanting",
    "raw_span": "제조사가 허용한 리필 지침대로 리필했어요.",
    "connection": "제조사 지침에 따른 리필을 실제 실행했어요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "용기를 세척하고 완전히 말린 뒤 리필했어요.",
    "connection": "리필 전 용기 세척과 건조를 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제조사가 허용한 방식으로 세척·건조한 용기에 리필한 사례이므로 임의 소분과 구분해요 [kb:B-S03@0.6.1].

### 근거 및 이유
용기 취급은 제품별 안내와 연결해서 살펴봐야 해요 [ref:S06].

### 확인이 필요한 한계
이 이력만으로 내용물의 현재 품질이 보증되지는 않아요.

## syn-sol-0620 — 눈가 반복 시림에도 같은 방식

- 내용 해시: `f967910587941d2f9832553d8f4f49f19e789253def598597faa9371937fb4dd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 반복 시림 부정 사례와 달리 실제 반복 시림에도 같은 방식을 유지해요. / syn-sol-0016

### 설계한 시나리오 raw

같은 선제품을 눈 가까이 쓰면 반복해서 눈이 시려요. 그런데 같은 방식으로 계속 눈 가까이에 발라요. 지금 지속적인 눈 통증은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "same_product_near_eye_continued": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "persistent_eye_pain": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "difference",
      "guidance": "같은 사용 방식의 반복 눈시림에도 해당 제품을 눈 가까이 계속 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.eye_stinging",
    "raw_span": "같은 선제품을 눈 가까이 쓰면 반복해서 눈이 시려요.",
    "connection": "본인의 반복적인 눈시림이에요."
  },
  {
    "variable_id": "sun.periocular_application",
    "raw_span": "그런데 같은 방식으로 계속 눈 가까이에 발라요.",
    "connection": "불편을 겪는 동일한 사용 방식을 계속해요."
  },
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "지금 지속적인 눈 통증은 없어요.",
    "connection": "현재 지속 통증의 명시적인 부정이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
반복해 시린 제품을 계속 눈 가까이에 쓰는 방식을 조정하고 눈 주변을 위한 다른 광보호 수단도 확인해 주세요 [kb:B-P06@0.6.1].

### 근거 및 이유
반복되는 불편과 눈 주변 보호를 함께 고려해야 해요. 눈 주변 제품 선택에는 여러 방안이 논의돼요 [ref:S17].

### 확인이 필요한 한계
지속적인 눈 통증은 없다고 하셨지만 원인이나 모든 제품의 사용감을 단정할 수 없어요.

## syn-sol-0621 — 눈가 회피와 선글라스

- 내용 해시: `3c44a340d625119dc269cd4404dfe3f03630074bbb5ea9da28d1a1cb27a099f0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 눈시림이 없던 경우와 달리 반복 불편 후 눈가 사용을 조정하고 대체 보호를 사용해요. / syn-sol-0016

### 설계한 시나리오 raw

선제품을 눈가에 쓸 때마다 눈이 시렸어요. 그 제품의 눈가 사용은 피하고 있어요. 눈 주변은 선글라스를 써서 보호해요. 지금 눈에 지속적인 통증은 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "avoids_problem_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "sunglasses_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "persistent_eye_pain": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "aligned",
      "guidance": "불편한 제품의 눈가 사용을 피하고 선글라스를 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    },
    {
      "evidence_ref": "ref:S29",
      "text": "General skin-care guidance discusses moisturizing. Individual needs can vary.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/news/how-to-treat-eczema-at-home",
      "locator": "보습 유지와 무향료 선택. 향료 이외 성분도 개인 반응을 일으킬 수 있음.",
      "checked_on": "2026-11-04",
      "limitations": "주로 아토피 피부염의 자가관리 안내. 모든 손 피부질환을 같은 질환으로 보지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": [
    "ref:S29"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.eye_stinging",
    "raw_span": "선제품을 눈가에 쓸 때마다 눈이 시렸어요.",
    "connection": "본인의 반복 눈시림을 확인해요."
  },
  {
    "variable_id": "sun.periocular_application",
    "raw_span": "그 제품의 눈가 사용은 피하고 있어요.",
    "connection": "불편한 제품의 눈가 사용을 조정했어요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "눈 주변은 선글라스를 써서 보호해요.",
    "connection": "대체 보호수단의 실제 사용을 확인해요."
  },
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "지금 눈에 지속적인 통증은 없어요.",
    "connection": "현재 지속 통증을 명시적으로 부정해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
불편한 제품의 눈가 사용을 피하면서 선글라스로 눈 주변을 보호하는 현재 조정은 유지할 수 있어요 [kb:B-P06@0.6.1].

### 근거 및 이유
반복 시림을 피하는 것과 대체 광보호를 확보하는 것은 함께 살필 사항이에요 [kb:B-P06@0.6.1].

### 확인이 필요한 한계
현재 지속적인 눈 통증은 없다고 보고했으며, 제품의 원인이나 전체 안전성을 확정하지 않아요.

## syn-sol-0622 — 눈가 회피 후 대체 보호 없음

- 내용 해시: `5d5afee97be2a0461d3ef86dbdaccaeda9afc361fcbb5429f8af13dc9a7c1ea0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 눈가를 피하면서 대체 보호도 없는 상황이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0161

### 설계한 시나리오 raw

선제품을 눈가에 쓰면 반복해서 시려요. 그 제품을 눈가에 쓰지 않아요. 눈 주변에 다른 광보호는 하지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "avoids_problem_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "periocular_protection_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "difference",
      "guidance": "불편한 제품을 피한 뒤 눈 주변의 다른 광보호를 하지 않는다고 보고해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.eye_stinging",
    "raw_span": "선제품을 눈가에 쓰면 반복해서 시려요.",
    "connection": "본인의 반복 눈시림이에요."
  },
  {
    "variable_id": "sun.periocular_application",
    "raw_span": "그 제품을 눈가에 쓰지 않아요.",
    "connection": "해당 제품의 눈가 사용을 피하고 있어요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "눈 주변에 다른 광보호는 하지 않아요.",
    "connection": "눈 주변 대체 광보호의 부재를 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
시린 제품을 피한 뒤에도 눈 주변을 위한 다른 광보호 수단을 확인해 주세요 [kb:B-P06@0.6.1].

### 근거 및 이유
사용 회피만으로 눈 주변 보호가 확보되는 것은 아니에요. 눈 주변의 제품 선택도 개별 불편과 함께 살펴봐요 [ref:S17].

### 확인이 필요한 한계
반복 시림의 원인을 특정 성분으로 단정하지 않아요.

## syn-sol-0623 — 친구의 눈시림과 본인 답변 거절

- 내용 해시: `0f8006cbb85690dea20743939b2bf4096cbd82c7b772ab7ec1fd13a90378d5cd`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 타인 증상과 본인 상태에 대한 응답 거절이에요. / syn-sol-0016

### 설계한 시나리오 raw

눈가가 시렸다는 건 친구 이야기예요. 제 눈이 시린지는 답하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "reported_symptom_subject": "friend"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "친구의 눈시림을 본인의 증상으로 옮기지 않으며 본인 상태는 답변을 거절했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "눈가가 시렸다는 건 친구 이야기예요.",
    "connection": "증상의 주체가 친구임을 구분해요."
  },
  {
    "variable_id": "skin.eye_stinging",
    "raw_span": "제 눈이 시린지는 답하고 싶지 않아요.",
    "connection": "본인의 눈시림 여부에 대한 답변을 거절해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 눈시림을 본인의 증상으로 판단하지 않아요. 본인의 상태를 답하고 싶지 않다는 선택도 존중해요 [kb:B-P06@0.6.1].

### 근거 및 이유
눈 주변 제품 선택은 실제 사용자 경험을 바탕으로 살펴봐야 해요 [ref:S17].

### 확인이 필요한 한계
본인의 눈시림은 없다고 확인된 것이 아니라 답변을 거절한 상태예요.

## syn-sol-0624 — 야외 후보 보호 표시 미확인

- 내용 해시: `981eab9cd2f5dd291731b5e5a059c9f2fcb26af99af9de5e984db03193910540`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 도포가 아닌 새 야외 후보의 표시 미확인 상황이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0075

### 설계한 시나리오 raw

야외에서 쓸 새 제품을 고르고 있어요. 후보의 지수 표시는 아직 확인하지 못했어요. 실제 야외 활동은 아직 계획 중이에요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.spf": {
      "variable_id": "product.spf",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "새 야외용 후보의 보호 지수 표시를 확인하지 못해 기본 성능을 판정할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "야외에서 쓸 새 제품을 고르고 있어요.",
    "connection": "신규 선택 맥락이며 실제 사용이 아니에요."
  },
  {
    "variable_id": "product.spf",
    "raw_span": "후보의 지수 표시는 아직 확인하지 못했어요.",
    "connection": "지수 표시는 미확인이에요."
  },
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "실제 야외 활동은 아직 계획 중이에요.",
    "connection": "계획과 실제 노출을 구분해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
새 야외용 후보의 보호 지수 표시를 먼저 확인해 주세요 [kb:B-P01@0.6.1].

### 근거 및 이유
표시를 아직 확인하지 못한 것은 기본 성능이 부족하다는 뜻이 아니에요. 선제품 선택에는 확인 가능한 제품 정보가 필요해요 [kb:B-P01@0.6.1].

### 확인이 필요한 한계
야외 사용은 계획이며 실제 사용이나 성능은 확인되지 않았어요.

## syn-sol-0625 — 두 보호 표시 모두 미확인

- 내용 해시: `e37b1d6359f1c30dc9560aeae6eee6c3b2a7f25529a1a6ad60f582539d1c7395`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 두 별도 표시가 미확인이며 현재 사용 중 도포 문제와 구분해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0075

### 설계한 시나리오 raw

야외용 새 제품을 고르는 중이에요. 보호 지수 표시를 읽지 못했어요. 광범위 보호 표시도 확인하지 못했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "new_product_selection",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.spf": {
      "variable_id": "product.spf",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "지수와 광범위 보호 표시가 모두 미확인이며 기본 성능 미충족으로 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "constraints.decision_context",
    "raw_span": "야외용 새 제품을 고르는 중이에요.",
    "connection": "새 제품 선택 맥락이에요."
  },
  {
    "variable_id": "product.spf",
    "raw_span": "보호 지수 표시를 읽지 못했어요.",
    "connection": "지수 표시가 확인되지 않았어요."
  },
  {
    "variable_id": "product.uva",
    "raw_span": "광범위 보호 표시도 확인하지 못했어요.",
    "connection": "광범위 보호 표시도 미확인이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
후보의 지수와 광범위 보호 표시를 각각 확인해 주세요 [kb:B-P01@0.6.1].

### 근거 및 이유
두 표시가 미확인이라 현재 기본 보호 조건에 맞는지 판단할 수 없어요 [kb:B-P01@0.6.1].

### 확인이 필요한 한계
표시를 읽지 못했다는 이유로 성능 미충족이라고 단정하지 않아요.

## syn-sol-0626 — 수영 후 노출 종료

- 내용 해시: `667adf6215bb2724aa10cfc11c2bef0161afff27cbb6f75923fe4b4277e492b4`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 수영 뒤 지속 노출한 경우와 달리 이후 야외 노출이 없어요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0065

### 설계한 시나리오 raw

야외 수영을 했어요. 나와서 수건으로 닦았어요. 그날은 이후 실내에 머물러 야외로 돌아가지 않았어요. 수영 후 다시 발랐는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "continues_after_swimming": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "물과 수건 접촉 뒤 야외 노출은 종료됐고 재도포 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S03",
      "text": "Gentle cleansing is discussed in everyday skin-care advice. The guidance is general and does not establish an individual outcome.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S03"
  ]
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.water_contact",
    "raw_span": "야외 수영을 했어요.",
    "connection": "물에 접촉했어요."
  },
  {
    "variable_id": "sun.towel_contact",
    "raw_span": "나와서 수건으로 닦았어요.",
    "connection": "수건 접촉이 있었어요."
  },
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "그날은 이후 실내에 머물러 야외로 돌아가지 않았어요.",
    "connection": "수영 후 야외 노출은 끝났어요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "수영 후 다시 발랐는지는 기억나지 않아요.",
    "connection": "재도포 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
수영과 수건 접촉 후에는 실내에 머물렀고 야외로 돌아가지 않았다고 하셨어요. 기억나지 않는 재도포를 없었다고 판단하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
물과 닦임뿐 아니라 이후 실제 노출이 이어지는지를 함께 살펴봐요 [ref:S05].

### 확인이 필요한 한계
수영 후 재도포 여부는 미상이에요.

## syn-sol-0627 — 물 접촉 없는 재도포

- 내용 해시: `e9115f954b6782aa3e9c525bf79b81dc5e5d8ba7512d42daa52d548464e00f4d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 수영과 닦임 없이 지속 노출 중 재도포했어요. / syn-sol-0065

### 설계한 시나리오 raw

오래 야외에 있었어요. 물에 닿은 일은 없었어요. 제품 표시 지침에 따라 다시 발랐어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": false,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "performed": true,
        "follows_label": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "aligned",
      "guidance": "장시간 노출 중 제품 지침에 따라 재도포했고 물 접촉은 없었다고 보고해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "오래 야외에 있었어요.",
    "connection": "야외 노출이 오래 이어졌어요."
  },
  {
    "variable_id": "sun.water_contact",
    "raw_span": "물에 닿은 일은 없었어요.",
    "connection": "물 접촉을 명시적으로 부정했어요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "제품 표시 지침에 따라 다시 발랐어요.",
    "connection": "실제 재도포와 표시 지침 준수를 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
긴 야외 노출 동안 표시 지침에 맞춰 재도포한 방식은 이 항목에서 유지할 수 있어요 [kb:B-P03@0.6.1].

### 근거 및 이유
물에 닿지 않았더라도 지속 노출을 고려해 제품 지침을 따르는 접근이에요 [ref:S05].

### 확인이 필요한 한계
실제 피부의 보호 수준은 측정되지 않았어요.

## syn-sol-0628 — 그늘 대신 얼굴 보호 모자 제약

- 내용 해시: `3f997fddfb1301112b1bdf33843d470531772797e3c3263e2aa16ca2be5f7ed0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 긴 소매가 아닌 안전모 제약과 실제 그늘 이용을 결합해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0071

### 설계한 시나리오 raw

야외에서 오래 일했어요. 안전모를 써야 해서 챙이 넓은 모자는 쓸 수 없어요. 쉴 때 이용 가능한 그늘에서 쉬었어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.burden": {
      "variable_id": "constraints.burden",
      "state": "known",
      "value": {
        "wide_brim_hat_not_feasible": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "shade_break_available": true,
        "shade_break_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "aligned",
      "guidance": "모자 선택에 제약이 있지만 휴식 중 이용 가능한 그늘을 실제로 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "야외에서 오래 일했어요.",
    "connection": "장시간 야외 근무예요."
  },
  {
    "variable_id": "constraints.burden",
    "raw_span": "안전모를 써야 해서 챙이 넓은 모자는 쓸 수 없어요.",
    "connection": "안전모 착용으로 모자 선택에 제약이 있어요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "쉴 때 이용 가능한 그늘에서 쉬었어요.",
    "connection": "가능한 대체 수단인 그늘을 실제 이용했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
안전모 때문에 챙 넓은 모자가 어려운 조건에서 쉬는 동안 그늘을 이용한 방법을 유지할 수 있어요 [kb:B-P04@0.6.1].

### 근거 및 이유
광보호 수단은 실제 작업 제약 안에서 실행 가능한 것을 함께 살펴봐요 [ref:S05].

### 확인이 필요한 한계
안전모 사용을 포기하도록 권하지 않으며 실제 보호 수준도 알 수 없어요.

## syn-sol-0629 — 모자와 그늘 실제 이용

- 내용 해시: `afe8aebfc77ea5b733436a692ff63f3765fbc324b4bc261b8c29c15b8f58fcbb`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 그늘 배제가 아니라 모자와 그늘의 실제 사용이 확인돼요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0063

### 설계한 시나리오 raw

장시간 야외에 있었어요. 모자를 썼고 쉬는 시간마다 그늘을 이용했어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "hat_used": true,
        "shade_break_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "aligned",
      "guidance": "장시간 야외에 머물며 모자와 그늘을 실제로 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "장시간 야외에 있었어요.",
    "connection": "장시간 노출이 확인돼요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "모자를 썼고 쉬는 시간마다 그늘을 이용했어요.",
    "connection": "모자와 그늘 모두 실제 사용했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
긴 야외 활동 중 모자를 쓰고 쉬는 시간마다 그늘을 이용한 방식을 유지할 수 있어요 [kb:B-P04@0.6.1].

### 근거 및 이유
모자와 그늘은 선제품 외에 함께 활용할 수 있는 보호수단이에요 [ref:S05].

### 확인이 필요한 한계
이 사실만으로 전체 노출이나 개인 보호 수준을 계산할 수는 없어요.

## syn-sol-0630 — 창가 직사광선과 기간 미상

- 내용 해시: `ca0ae0d7c01bade0443d5326992f9f3e0d35cc2c333458d6af2a3ce613df9436`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 차량 열이 아니라 빛에 실제 노출된 조건과 기간 미상이에요. / syn-sol-0021

### 설계한 시나리오 raw

제품을 직사광선이 드는 창가에 두었어요. 그곳에 얼마나 오래 두었는지는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "direct_sunlight_reported": true,
        "duration_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "duration_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "exception",
      "guidance": "과거 직사광선 노출은 확인되지만 기간이 미상인 과거 노출 예외로 보관 적합성은 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.light_air",
    "raw_span": "제품을 직사광선이 드는 창가에 두었어요. 그곳에 얼마나 오래 두었는지는 몰라요.",
    "connection": "빛 노출은 확인하지만 기간은 미상이에요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "그곳에 얼마나 오래 두었는지는 몰라요.",
    "connection": "해당 보관 기간을 확인할 수 없어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
직사광선에 두었던 이력은 기록하되 노출 기간이 미상인 과거 상황으로 따로 살펴요 [kb:B-S01@0.6.1].

### 근거 및 이유
빛은 제품 보관에 영향을 줄 수 있는 요소예요 [ref:S06]. 과거 노출 기간이 확인되지 않아 정확한 조건을 판단할 수 없어요.

### 확인이 필요한 한계
이 이력만으로 제품이 변질되었다고 확정하지 않아요.

## syn-sol-0631 — 닫힌 서랍과 온도 미상

- 내용 해시: `1102b5c4562327e6005eba4bd138059d3e719af628a59b44a6052ae2bdfc415d`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 현재 빛 회피와 온도 미상을 구분해요. / syn-sol-0051

### 설계한 시나리오 raw

제품은 닫은 채 서랍에 보관해요. 빛이 닿지 않는 서랍에 있어요. 서랍 안의 온도는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "closed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "stored_in_drawer": true,
        "away_from_light": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "용기는 닫혀 있고 빛은 피하지만 서랍의 온도는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.container",
    "raw_span": "제품은 닫은 채 서랍에 보관해요.",
    "connection": "용기를 닫았다는 사실이에요."
  },
  {
    "variable_id": "storage.light_air",
    "raw_span": "빛이 닿지 않는 서랍에 있어요.",
    "connection": "현재 빛 회피를 확인해요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "서랍 안의 온도는 몰라요.",
    "connection": "보관 온도를 알 수 없어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
용기를 닫고 빛을 피하고 있지만 서랍 온도는 미상이므로 보관 조건 전체가 적합하다고 단정하지 않아요 [kb:B-S01@0.6.1].

### 근거 및 이유
빛과 온도는 각각 살펴볼 수 있는 보관 요인이에요 [ref:S06].

### 확인이 필요한 한계
제품의 온도 지침과 서랍의 실제 온도는 확인되지 않았어요.

## syn-sol-0632 — 용기별 다른 기한 상태

- 내용 해시: `2976447d065cd827531b4eb7aefc925ae668b7f4c8469cb993261456f0325acb`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 용기 A만 기한 경과가 확인되고 B에 결론을 이전하지 않아요. / syn-sol-0052

### 설계한 시나리오 raw

A 용기의 표시 기한은 지났어요. 용기 B의 기한은 아직 확인하지 못했어요. 지금 확인하는 것은 용기 A예요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "container_a_expired": true,
        "container_b_checked": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "containers": [
          "A",
          "B"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-a",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "difference",
      "guidance": "A의 표시 기한이 지났고 B의 기한은 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.expiry",
    "raw_span": "A 용기의 표시 기한은 지났어요. 용기 B의 기한은 아직 확인하지 못했어요.",
    "connection": "A의 경과와 B의 미확인을 분리해요."
  },
  {
    "variable_id": "product.identity",
    "raw_span": "용기 B의 기한은 아직 확인하지 못했어요.",
    "connection": "두 용기를 구분해요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "지금 확인하는 것은 용기 A예요.",
    "connection": "판정 대상은 A예요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
기한이 지난 A와 기한을 아직 확인하지 않은 B를 따로 다뤄 주세요 [kb:B-S02@0.6.1].

### 근거 및 이유
용기별 표시와 이력을 연결해야 한 용기의 판단을 다른 용기로 잘못 옮기지 않아요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
B의 기한과 두 용기의 실제 품질은 이 정보만으로 알 수 없어요.

## syn-sol-0633 — 기한 유효와 개봉일 미상

- 내용 해시: `91c738dc09993e22f35a796fcfd29ac1e6e9af1269076594e0029b08aa5c9ba2`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 인쇄 기한 확인과 개봉 후 경과의 미상을 구분해요. / syn-sol-0123

### 설계한 시나리오 raw

표시 기한은 아직 지나지 않았어요. 개봉 후 사용 안내가 있어요. 언제 개봉했는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "within_printed_expiry": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.pao": {
      "variable_id": "storage.pao",
      "state": "known",
      "value": {
        "label_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "표시 기한은 남았지만 개봉일을 몰라 개봉 후 안내와 비교할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.expiry",
    "raw_span": "표시 기한은 아직 지나지 않았어요.",
    "connection": "인쇄된 기한이 남았어요."
  },
  {
    "variable_id": "storage.pao",
    "raw_span": "개봉 후 사용 안내가 있어요.",
    "connection": "개봉 후 안내가 있음을 확인해요."
  },
  {
    "variable_id": "storage.opened_at",
    "raw_span": "언제 개봉했는지는 기억나지 않아요.",
    "connection": "개봉일은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
표시 기한은 남았지만 개봉일을 모르므로 개봉 후 안내와의 일치 여부는 미상이에요 [kb:B-S02@0.6.1].

### 근거 및 이유
인쇄된 기한과 개봉 후 사용 안내는 별도로 확인해야 할 정보예요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
개봉일을 추측하거나 미상을 기한 경과로 바꾸지 않아요.

## syn-sol-0634 — 용기 이력과 안내 일치

- 내용 해시: `3fa61ed18e48ca2a23d165bfc39a715ef11392c471a8ce8c4fb3bbfa2322fca3`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 표시 기한과 개봉 후 안내 모두 해당 용기에 연결되어 확인돼요. / syn-sol-0123

### 설계한 시나리오 raw

이 용기의 표시 기한은 지나지 않았어요. 개봉일을 알고 있어요. 그 개봉일은 해당 용기의 개봉 후 안내 기간 안에 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "within_printed_expiry": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "known": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.pao": {
      "variable_id": "storage.pao",
      "state": "known",
      "value": {
        "within_label_period": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "aligned",
      "guidance": "같은 용기의 표시 기한과 개봉 이력이 확인된 안내에 맞아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.expiry",
    "raw_span": "이 용기의 표시 기한은 지나지 않았어요.",
    "connection": "표시 기한이 남았어요."
  },
  {
    "variable_id": "storage.opened_at",
    "raw_span": "개봉일을 알고 있어요.",
    "connection": "개봉일이 확인돼요."
  },
  {
    "variable_id": "storage.pao",
    "raw_span": "그 개봉일은 해당 용기의 개봉 후 안내 기간 안에 있어요.",
    "connection": "같은 용기에 연결된 안내와 이력이 일치해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
해당 용기의 표시 기한과 개봉 이력이 안내에 맞는다는 보고는 이 항목에서 유지할 수 있어요 [kb:B-S02@0.6.1].

### 근거 및 이유
같은 용기에 연결된 개봉일과 안내를 비교한 점이 중요해요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
이력이 맞는다는 사실은 현재 품질을 인증하지 않아요.

## syn-sol-0635 — 잔량 위 보충 계획만 있음

- 내용 해시: `6b314ec91c8439fbcdc013eb414cff2a39889bd9cc0d5a5948f3d755c1fe19d7`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 소분 계획이 아니라 잔량 위 보충 계획과 미실행을 구분해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0053

### 설계한 시나리오 raw

남은 제품에 새 제품을 덧붓기 전 설명서를 확인할 예정이에요. 아직 덧붓지는 않았어요. 리필 지침은 아직 모릅니다.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.sharing_refill": {
      "variable_id": "storage.sharing_refill",
      "state": "known",
      "value": {
        "top_up_planned": true,
        "top_up_performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.decanting": {
      "variable_id": "storage.decanting",
      "state": "known",
      "value": {
        "already_done": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "unknown",
      "guidance": "남은 내용물 위 보충은 아직 계획이며 지침도 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S07@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.sharing_refill",
    "raw_span": "남은 제품에 새 제품을 덧붓기 전 설명서를 확인할 예정이에요.",
    "connection": "덧붓기는 계획이지 실행이 아니에요."
  },
  {
    "variable_id": "storage.decanting",
    "raw_span": "아직 덧붓지는 않았어요.",
    "connection": "현재 실행되지 않았어요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "리필 지침은 아직 모릅니다.",
    "connection": "지침 내용은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
잔량 위에 새 제품을 붓기 전에 제조사의 리필 지침을 확인해 주세요. 아직 실행하지 않은 계획을 실제 행동으로 판단하지 않아요 [kb:B-S07@0.6.1].

### 근거 및 이유
리필과 용기 취급은 제품별 안내를 살펴야 해요 [kb:B-S07@0.6.1].

### 확인이 필요한 한계
제조사 지침은 현재 미상이에요.

## syn-sol-0636 — 원래 용기와 물 미첨가

- 내용 해시: `cfaa0637a5f0f9f1d3aa91d1f18d80ab59ed256e69166663754f9db317e95f17`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 원래 용기 사용과 물 첨가 부정을 함께 확인해요. / syn-sol-0060

### 설계한 시나리오 raw

제조사가 제공한 원래 용기를 사용해요. 사용 후 용기를 닫아요. 사용 후 용기를 닫아요. 제품에 물은 넣지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "original_container": true,
        "closed_after_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "closed_after_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": false,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "aligned",
      "guidance": "원래 용기를 사용하고 물을 넣지 않으며 사용 후 닫아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.container",
    "raw_span": "제조사가 제공한 원래 용기를 사용해요. 사용 후 용기를 닫아요.",
    "connection": "원래 용기와 사용 후 닫기를 확인해요."
  },
  {
    "variable_id": "storage.handling",
    "raw_span": "사용 후 용기를 닫아요.",
    "connection": "사용 후 취급을 확인해요."
  },
  {
    "variable_id": "storage.water_ingress",
    "raw_span": "제품에 물은 넣지 않았어요.",
    "connection": "원제품의 물 첨가를 명시적으로 부정해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
원래 용기를 쓰고 사용 후 닫으며 물을 넣지 않는 현재 취급은 이 항목에서 유지할 수 있어요 [kb:B-S03@0.6.1].

### 근거 및 이유
용기와 물 첨가 여부는 제품 취급을 살펴볼 때 구분할 정보예요 [ref:S06].

### 확인이 필요한 한계
이 관찰만으로 제품이 오염되지 않았거나 안전하다고 보증할 수 없어요.

## syn-sol-0637 — 얼굴 노출과 적용 범위 미상

- 내용 해시: `85e7708023cf245a892d0f54eb655bad1ff3d3408cb6e57c76feb4ad19a64ad0`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 누락이 확인된 사례와 달리 누락 여부가 미상이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0077

### 설계한 시나리오 raw

야외에서 얼굴이 노출됐어요. 얼굴 어디에 선제품을 발랐는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "얼굴이 노출된 것은 확인되지만 도포 범위는 기억나지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.exposed_sites",
    "raw_span": "야외에서 얼굴이 노출됐어요.",
    "connection": "실제 얼굴 노출을 확인해요."
  },
  {
    "variable_id": "sun.coverage_gaps",
    "raw_span": "얼굴 어디에 선제품을 발랐는지는 기억나지 않아요.",
    "connection": "도포 범위나 누락 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴이 노출됐지만 어느 곳에 발랐는지 기억나지 않으므로 누락 부위를 정하지 않아요 [kb:B-P02@0.6.1].

### 근거 및 이유
노출된 부위와 실제 도포 범위는 별도로 확인할 정보예요 [kb:B-P02@0.6.1].

### 확인이 필요한 한계
기억나지 않는 도포 범위를 전부 발랐다거나 빠뜨렸다고 추정하지 않아요.

## syn-sol-0638 — 얼굴 누락과 제품 지침의 부위 제한

- 내용 해시: `e07374f7fbfa1d7ddcad38d4ae1f44e8fc5fd9605737897340b3555c3af7977a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 얼굴 볼 누락과 제품의 눈가 제한을 혼동하지 않아요. / syn-sol-0017

### 설계한 시나리오 raw

선제품을 이마에만 바르고 볼은 의도적으로 빼요. 해당 제품의 사용 지침은 눈가를 피하라고 적혀 있어요. 볼은 야외에 노출돼요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "known",
      "value": [
        "cheeks"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "avoid_eye_area": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "볼의 노출과 의도적 누락이 확인되며 눈가 제한은 별도로 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.coverage_gaps",
    "raw_span": "선제품을 이마에만 바르고 볼은 의도적으로 빼요.",
    "connection": "볼을 의도적으로 도포에서 제외했어요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "해당 제품의 사용 지침은 눈가를 피하라고 적혀 있어요.",
    "connection": "눈가 제한이 볼 전체의 제외를 지시하는지는 별도예요."
  },
  {
    "variable_id": "sun.exposed_sites",
    "raw_span": "볼은 야외에 노출돼요.",
    "connection": "얼굴 볼이 야외에 노출돼요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
노출된 볼을 의도적으로 제외한 점을 살펴보되 눈가를 피하라는 제품 지침은 지켜 주세요 [kb:B-P02@0.6.1].

### 근거 및 이유
얼굴 내 누락과 눈가 사용 제한은 같은 정보가 아니에요 [kb:B-P02@0.6.1].

### 확인이 필요한 한계
제공된 지침만으로 눈가 외 다른 부위의 자세한 용법을 추정하지 않아요.

## syn-sol-0639 — 눈가 사용과 반복 시림 부정

- 내용 해시: `3a3a0099f5445c9ea77a97ba8e27b65252ba2a925f5a2673a1bae344fce89d68`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 반복 시림 부정과 별개로 실제 눈가 사용이 확인된 제품의 제한과 충돌해요. / syn-sol-0016

### 설계한 시나리오 raw

눈가에 선제품을 사용해요. 그때 반복적으로 눈이 시리지는 않아요. 선글라스를 써요. 제품 표시에는 눈가를 피하라고 적혀 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "near_eye_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "sunglasses_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "avoid_eye_area": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "exception",
      "guidance": "반복 눈시림은 부정하지만 실제 눈가 사용은 확인된 제품의 눈가 제한과 충돌하므로 지침을 별도 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.periocular_application",
    "raw_span": "눈가에 선제품을 사용해요.",
    "connection": "본인의 실제 눈가 사용이에요."
  },
  {
    "variable_id": "skin.eye_stinging",
    "raw_span": "그때 반복적으로 눈이 시리지는 않아요.",
    "connection": "반복 시림을 명시적으로 부정해요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "선글라스를 써요.",
    "connection": "실제로 선글라스를 착용해요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "제품 표시에는 눈가를 피하라고 적혀 있어요.",
    "connection": "실제 눈가 사용과 제품별 눈가 제한을 별도로 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
반복 시림은 없지만 눈가에 사용 중인 제품에 눈가 회피 지시가 있어 해당 지침을 먼저 확인하고 사용 방식을 검토해 주세요 [kb:B-P06@0.6.1].

### 근거 및 이유
제품의 눈 주변 사용 제한은 반복 불편의 유무와 별도로 살필 조건이에요 [kb:B-P06@0.6.1].

### 확인이 필요한 한계
반복 시림을 부정한 것이 제품 지침을 대신하지 않으며 선글라스 사용만으로 모든 보호가 보장되지는 않아요.

## syn-sol-0640 — 뜨거운 차 보관 계획

- 내용 해시: `dc0d8390236e6ad087d86175e1c984c21c678c33a3908c569292955c05c5d098`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 확인된 뜨거운 차 보관이 아닌 미실행 계획이에요. / syn-sol-0021

### 설계한 시나리오 raw

제품을 뜨거운 차에 둘까 생각했지만 아직 두지 않았어요. 다른 보관 이력은 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "hot_car_planned": true,
        "hot_car_occurred": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "뜨거운 차에 둔 것은 계획뿐이고 다른 보관 이력은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "제품을 뜨거운 차에 둘까 생각했지만 아직 두지 않았어요.",
    "connection": "미래 계획과 미실행을 구분해요."
  },
  {
    "variable_id": "storage.light_air",
    "raw_span": "다른 보관 이력은 기억나지 않아요.",
    "connection": "다른 보관 이력은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
뜨거운 차에 둘 계획은 아직 실행되지 않았으므로 이미 부적절하게 보관했다고 판단하지 않아요 [kb:B-S01@0.6.1].

### 근거 및 이유
열은 제품 보관 시 고려할 요소이므로 실제 보관 전 제품 지침을 확인해 주세요 [ref:S06].

### 확인이 필요한 한계
다른 보관 이력도 미상이어서 전체 보관 적합성을 확정할 수 없어요.

## syn-sol-0641 — 용기별 다른 개봉 안내

- 내용 해시: `138113a1ade5d64d843ef6ed7f2b653a3fdb4bdb556814d11ad34ba5846c81f1`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 서로 다른 안내와 B의 미상 개봉일을 연결해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0052

### 설계한 시나리오 raw

같은 제품 A와 B의 표시된 개봉 후 안내가 서로 달라요. A의 개봉일은 기록했지만 B는 기록하지 않았고 B를 연 날짜도 기억나지 않아요. 지금은 B를 검토하고 있어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "container_versions_have_different_pao": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "container_a_known": true,
        "container_b_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "known",
      "value": "synthetic-container-b",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "B의 개봉일이 미상이므로 A의 이력이나 다른 버전 안내로 대체할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "같은 제품 A와 B의 표시된 개봉 후 안내가 서로 달라요.",
    "connection": "용기 버전별 안내가 다르다는 사실이에요."
  },
  {
    "variable_id": "storage.opened_at",
    "raw_span": "A의 개봉일은 기록했지만 B는 기록하지 않았고 B를 연 날짜도 기억나지 않아요.",
    "connection": "각 용기의 개봉 이력 확인 수준을 분리해요."
  },
  {
    "variable_id": "storage.instance_id",
    "raw_span": "지금은 B를 검토하고 있어요.",
    "connection": "판정 대상이 B라는 연결이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
용기 B는 개봉 기록이 없고 개봉일도 기억나지 않아 B의 안내와 비교할 수 없어요 [kb:B-S02@0.6.1].

### 근거 및 이유
용기별 안내가 다르므로 A의 이력이나 안내를 B에 옮겨 적용하지 않아요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
B의 개봉일과 현재 품질은 미상이에요.

## syn-sol-0642 — 제조사 지침에 따른 리필

- 내용 해시: `cd74eb2c679e52764431f9d2d8d11962880c63dc65d51356e614cf2956a405d3`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 소분 계획이 아닌 허용된 리필 실행과 잔량 위 덧붓기 부정이에요. / syn-sol-0053

### 설계한 시나리오 raw

제조사가 허용한 방법대로 리필했어요. 남은 내용물 위에 새 제품을 덧붓지는 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.decanting": {
      "variable_id": "storage.decanting",
      "state": "known",
      "value": {
        "refilled": true,
        "follows_manufacturer_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sharing_refill": {
      "variable_id": "storage.sharing_refill",
      "state": "known",
      "value": {
        "topped_up_residue": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "aligned",
      "guidance": "제조사 지침대로 리필했고 남은 내용물 위에 덧붓지는 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S07@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.decanting",
    "raw_span": "제조사가 허용한 방법대로 리필했어요.",
    "connection": "허용된 리필 방법을 실제 실행했어요."
  },
  {
    "variable_id": "storage.sharing_refill",
    "raw_span": "남은 내용물 위에 새 제품을 덧붓지는 않았어요.",
    "connection": "잔량 위 덧붓기를 부정해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
제조사가 허용한 방식대로 리필했고 잔량 위에 덧붓지 않은 이력은 유지할 수 있어요 [kb:B-S07@0.6.1].

### 근거 및 이유
허용된 리필과 지침 없는 잔량 위 보충은 구분해요 [kb:B-S07@0.6.1].

### 확인이 필요한 한계
리필 이력이 현재 제품 품질을 보증하지는 않아요.

## syn-sol-0643 — 발한과 닦임 후 재도포 미상

- 내용 해시: `ccfc810cdd30f6c446261d0970bc2bb68f9c2895d11a151f5e6fb19b63e2643e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 발한과 추가적인 수건 접촉 이후의 실행 여부가 미상이에요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0005

### 설계한 시나리오 raw

오래 야외에 있었고 땀을 많이 흘렸어요. 수건으로 얼굴을 닦았어요. 그 뒤에도 계속 야외에 있었어요. 그 뒤 다시 발랐는지 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.sweat": {
      "variable_id": "sun.sweat",
      "state": "known",
      "value": {
        "heavy": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": true,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true,
        "continues_after_towel": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "발한과 닦임 후 노출은 이어졌으나 재도포 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.sweat",
    "raw_span": "오래 야외에 있었고 땀을 많이 흘렸어요.",
    "connection": "심한 발한이 있었어요."
  },
  {
    "variable_id": "sun.towel_contact",
    "raw_span": "수건으로 얼굴을 닦았어요.",
    "connection": "얼굴에 수건을 접촉했어요."
  },
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "그 뒤에도 계속 야외에 있었어요.",
    "connection": "닦은 후 야외 노출이 이어졌어요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "그 뒤 다시 발랐는지 기억나지 않아요.",
    "connection": "재도포를 하지 않았다고 추정하지 않아요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
땀과 수건 접촉 뒤에도 야외에 있었지만 재도포 여부는 미상이에요. 이후에는 제품 지침과 활동 조건을 함께 확인해 주세요 [kb:B-P03@0.6.1].

### 근거 및 이유
발한과 닦임은 광보호를 다시 살펴볼 계기예요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
기억나지 않는 행동을 하지 않았다고 판단하지 않아요.

## syn-sol-0644 — 모자 제약과 그늘

- 내용 해시: `fa02658f15a80cf539bf8cf07cfdba87af824387d7b7ed9dc67dbf7fcfb37f9a`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 새 합성 대체 사례: 모자 제약은 확인되지만 그늘 가능성에 대한 답변 거절을 미사용과 구분해요. / syn-sol-0071

### 설계한 시나리오 raw

야외 근무가 오래 이어져요. 작업 규정상 모자를 쓸 수 없어요. 휴식할 때 그늘을 이용할 수 있는지는 답하고 싶지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.burden": {
      "variable_id": "constraints.burden",
      "state": "known",
      "value": {
        "hat_prohibited_at_work": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "모자 사용에는 제약이 있으나 다른 보호수단 가능성은 답변을 거절해 판단을 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "야외 근무가 오래 이어져요.",
    "connection": "장시간 야외 근무예요."
  },
  {
    "variable_id": "constraints.burden",
    "raw_span": "작업 규정상 모자를 쓸 수 없어요.",
    "connection": "모자 사용의 실제 제약이에요."
  },
  {
    "variable_id": "sun.shade_clothing",
    "raw_span": "휴식할 때 그늘을 이용할 수 있는지는 답하고 싶지 않아요.",
    "connection": "그늘 이용 가능성과 사용 여부에 대한 답변을 거절했어요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
모자 사용이 어려운 근무 제약은 확인됐지만 그늘에 관해 답하고 싶지 않다는 선택을 존중해요 [kb:B-P04@0.6.1].

### 근거 및 이유
그늘의 가능성과 실제 사용 여부를 거절한 답변에서 추정하지 않아요. 일반적인 광보호에는 그늘과 의복이 포함돼요 [ref:S05].

### 확인이 필요한 한계
그늘을 사용할 수 없었다거나 사용하지 않았다고 판단하지 않아요.

## syn-sol-0645 — 친구 증상과 본인 눈가 미사용

- 내용 해시: `04732f66c5469eaef61a4782e26b9cbc058ebef46e89af0f6e97d1017a6a8892`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 타인의 눈시림을 본인의 제품 경험으로 전환하지 않아요. / syn-sol-0016

### 설계한 시나리오 raw

눈가가 시렸던 사람은 친구예요. 저는 그 선제품을 눈가에 사용한 적이 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "reported_symptom_subject": "friend"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "personally_used_near_eye": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "친구의 경험과 본인의 눈가 미사용을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변의 선제품 선택에는 스틱형 등의 선택지가 논의돼요. 특정 제형이 누구에게나 불편이 없다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/sun-protection/shade-clothing-sunscreen/choosing-right-sunscreen",
      "locator": "Step 1 및 Around your eyes 항목",
      "checked_on": "2026-11-04",
      "limitations": "눈 주변 스틱 사용은 흘러듦을 줄이기 위한 선택지다. 지용성·고분자량 우월성이나 모든 스틱의 무자극 보장을 뒷받침하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1",
    "ref:S17"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "skin.eye_symptom_context",
    "raw_span": "눈가가 시렸던 사람은 친구예요.",
    "connection": "증상은 친구의 경험이에요."
  },
  {
    "variable_id": "sun.periocular_application",
    "raw_span": "저는 그 선제품을 눈가에 사용한 적이 없어요.",
    "connection": "본인의 실제 눈가 미사용을 확인해요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 눈시림을 본인의 경험으로 옮기지 않아요. 본인은 해당 선제품을 눈가에 사용한 적이 없다고 하셨어요 [kb:B-P06@0.6.1].

### 근거 및 이유
눈 주변 사용 경험은 실제 사용자와 사용 조건에 연결해 살펴봐야 해요 [ref:S17].

### 확인이 필요한 한계
본인의 해당 제품 눈가 사용 반응은 미상이에요.

## syn-sol-0646 — 과거 빛 노출 뒤 이동

- 내용 해시: `65c20ade2e49ec48c6853faa93c75a8f0b1c9d1325e058a842dda65d6794824e`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 과거 빛 노출 확인과 현재 이동을 구분해요. / syn-sol-0051

### 설계한 시나리오 raw

제품을 이전에 직사광선 아래 두었어요. 어제부터는 서랍에 옮겼어요. 과거 빛 노출이 얼마나 길었는지 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "past_direct_sunlight": true,
        "now_in_drawer": true,
        "past_duration_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "now_in_drawer": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "duration_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "exception",
      "guidance": "과거 직사광선 노출은 확인되지만 기간이 미상인 과거 노출 예외로 보관 적합성은 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.light_air",
    "raw_span": "제품을 이전에 직사광선 아래 두었어요. 어제부터는 서랍에 옮겼어요. 과거 빛 노출이 얼마나 길었는지 몰라요.",
    "connection": "과거 노출과 현재 보관 위치를 구분해요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "어제부터는 서랍에 옮겼어요.",
    "connection": "현재 장소를 기록해요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "과거 빛 노출이 얼마나 길었는지 몰라요.",
    "connection": "과거 노출 기간을 미상으로 남겨요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
과거 직사광선에 두었던 이력은 기록하되 기간이 미상인 과거 노출로 별도 검토해요 [kb:B-S01@0.6.1].

### 근거 및 이유
지금은 서랍에 옮겼지만 과거 빛 노출의 지속 시간은 확인되지 않았어요. 빛은 보관에 영향을 줄 수 있는 요소예요 [ref:S06].

### 확인이 필요한 한계
이 이력만으로 제품이 변질됐다고 단정하지 않아요.

## syn-sol-0647 — 개봉일 확인과 기한 판독 불가

- 내용 해시: `dc919b48eb9be9e3db8da0e358b9150966b2953332bd54e8a22bc4418b19cee6`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 개봉일을 알아도 표시 기한은 별도로 미상이에요. / syn-sol-0123

### 설계한 시나리오 raw

개봉한 날은 알아요. 표시 기한은 글자가 지워져 읽을 수 없어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "known": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "개봉일은 알지만 표시 기한을 읽을 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.opened_at",
    "raw_span": "개봉한 날은 알아요.",
    "connection": "개봉일을 확인했어요."
  },
  {
    "variable_id": "storage.expiry",
    "raw_span": "표시 기한은 글자가 지워져 읽을 수 없어요.",
    "connection": "표시 기한은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
개봉일은 알지만 표시 기한을 읽을 수 없으므로 해당 정보를 확인할 방법을 찾아보세요 [kb:B-S02@0.6.1].

### 근거 및 이유
개봉일과 표시 기한은 서로 다른 정보예요 [ref:S06].

### 확인이 필요한 한계
읽을 수 없는 기한을 지났거나 남았다고 추정하지 않아요.

## syn-sol-0648 — 손 접촉과 손 세척 여부 미상

- 내용 해시: `9dd9b57271f1fda9b1d8667a75a4dab8cb01c8a84ae45bc88792c36d5c1b6841`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 손 접촉 사실과 세척 여부 미상을 구분해요. 가까운 기존 판단 가족과 분할을 유지한 대응 변형이에요. / syn-sol-0060

### 설계한 시나리오 raw

원래 용기에 손가락을 넣어 덜었어요. 그 전에 손을 씻었는지는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "original_container": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "finger_contact": true,
        "hand_washing_known": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "unknown",
      "guidance": "손 접촉은 있었지만 접촉 전 손 세척 여부를 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "storage.container",
    "raw_span": "원래 용기에 손가락을 넣어 덜었어요.",
    "connection": "원래 용기 사용을 기록해요."
  },
  {
    "variable_id": "storage.handling",
    "raw_span": "원래 용기에 손가락을 넣어 덜었어요. 그 전에 손을 씻었는지는 기억나지 않아요.",
    "connection": "접촉은 확인되나 손 세척 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
원래 용기에 손가락이 닿았지만 손을 씻었는지는 기억나지 않는다고 하셨어요. 이후에는 제품의 취급 지침을 확인해 주세요 [kb:B-S03@0.6.1].

### 근거 및 이유
손 접촉 여부와 접촉 전 세척 여부는 서로 다른 관찰이에요 [kb:B-S03@0.6.1].

### 확인이 필요한 한계
손 세척 여부나 실제 오염은 확인되지 않았어요.

## syn-sol-0649 — 얼굴 도포 보고와 제품 제한 미상

- 내용 해시: `14181a08ffcc3b11854933972f8c28cd96e4e0b5052d959c3a30d4f59398e4dc`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 의도적 누락과 달리 전체 도포 보고 및 지침 미상이에요. / syn-sol-0017

### 설계한 시나리오 raw

얼굴 전체에 바른다고 보고해요. 야외에서 얼굴이 노출돼요. 이 제품의 부위 제한은 아직 읽지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sun_application": {
          "whole_face_reported": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "도포 보고는 있지만 해당 제품의 적용 부위 제한을 확인하지 못했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "method.current_routine",
    "raw_span": "얼굴 전체에 바른다고 보고해요.",
    "connection": "얼굴 전체 도포를 보고했어요."
  },
  {
    "variable_id": "sun.exposed_sites",
    "raw_span": "야외에서 얼굴이 노출돼요.",
    "connection": "실제 얼굴 노출을 확인해요."
  },
  {
    "variable_id": "product.instructions",
    "raw_span": "이 제품의 부위 제한은 아직 읽지 않았어요.",
    "connection": "제품별 적용 부위 제한은 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 전체 도포를 보고했지만 해당 제품의 부위 제한을 확인해 주세요 [kb:B-P02@0.6.1].

### 근거 및 이유
실제 도포 보고와 제품별 사용 지침은 함께 검토해야 해요 [ref:S05].

### 확인이 필요한 한계
지침이 미상이므로 특정 부위가 허용되거나 제한된다고 추정하지 않아요.

## syn-sol-0650 — 친구의 행동과 본인 미상

- 내용 해시: `6a5509cb0a66589590a2d34d729b849b840703ef883c973b1935b4c308fa25c8`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 친구의 미재도포와 본인의 미상을 분리해요. / syn-sol-0005

### 설계한 시나리오 raw

친구가 오래 야외에 있으면서 다시 바르지 않았대요. 저의 재도포 여부는 기억나지 않아요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "reported_person": "friend",
        "prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "친구의 행동은 본인에게 전이하지 않으며 본인의 재도포 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.outdoor_time",
    "raw_span": "친구가 오래 야외에 있으면서 다시 바르지 않았대요.",
    "connection": "야외 행동의 주체는 친구예요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "저의 재도포 여부는 기억나지 않아요.",
    "connection": "본인의 재도포 여부는 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
친구가 재도포하지 않은 행동을 본인에게 적용하지 않아요. 본인의 재도포는 기억나지 않는 상태예요 [kb:B-P03@0.6.1].

### 근거 및 이유
야외 노출과 재도포 이력은 실제 행동한 사람에게 연결해야 해요 [ref:S05].

### 확인이 필요한 한계
본인의 행동을 하지 않았다고 단정하지 않아요.

## syn-sol-0651 — 보관 표시 판독 불가

- 내용 해시: `85ad5aca1fccfccc478b2fadf6a4132008e1b2f729266468b5eed29b157a9003`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 지침과 온도가 모두 미상인 조건이에요. / syn-sol-0051

### 설계한 시나리오 raw

보관 장소에 관한 표시가 있지만 읽을 수 없어요. 용기는 현재 닫혀 있어요. 현재 보관 장소의 온도는 몰라요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "closed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "용기를 닫은 사실만으로 읽을 수 없는 보관 지침의 준수를 확인할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "열과 빛은 화장품의 보관 수명에 영향을 줄 수 있어요. 보관 이력만으로 개별 제품의 안정성을 확정하지는 못해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "product.instructions",
    "raw_span": "보관 장소에 관한 표시가 있지만 읽을 수 없어요.",
    "connection": "제품별 보관 지침이 미상이에요."
  },
  {
    "variable_id": "storage.container",
    "raw_span": "용기는 현재 닫혀 있어요.",
    "connection": "현재 용기가 닫힌 사실만 확인해요."
  },
  {
    "variable_id": "storage.temperature_history",
    "raw_span": "현재 보관 장소의 온도는 몰라요.",
    "connection": "현재 온도도 미상이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
용기가 닫혀 있어도 읽을 수 없는 보관 지침과 미상인 온도를 확인할 필요가 있어요 [kb:B-S01@0.6.1].

### 근거 및 이유
용기를 닫은 사실과 보관 온도 적합성은 다른 정보예요 [ref:S06].

### 확인이 필요한 한계
현재 지침과 온도가 모두 미상이므로 적합하거나 부적합하다고 단정하지 않아요.

## syn-sol-0652 — 계획된 야외 물 접촉

- 내용 해시: `11fcb0fee0600ef172e7811a834f9df99d118a8898a715e217a005c80ad6073f`
- 사람 검수: **미검수**
- 새 조건과 가까운 기존 사례: 실제 수영과 재도포가 확인된 사례와 달리 계획 단계예요. / syn-sol-0065

### 설계한 시나리오 raw

내일 야외 수영을 계획하지만 아직 하지 않았어요. 수영 후 재도포할지 아직 정하지 않았어요.

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": {
        "planned": true,
        "performed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "수영은 미실행 계획이고 재도포는 아직 정해지지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "선제품의 사용과 재도포는 노출 상황을 고려해요. 그늘과 보호 의복도 함께 고려하는 광보호 수단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 원문과 슬롯 연결

```json
[
  {
    "variable_id": "sun.water_contact",
    "raw_span": "내일 야외 수영을 계획하지만 아직 하지 않았어요.",
    "connection": "미래 계획과 실제 물 접촉 부재를 구분해요."
  },
  {
    "variable_id": "sun.reapplication",
    "raw_span": "수영 후 재도포할지 아직 정하지 않았어요.",
    "connection": "미래 재도포는 미정이에요."
  }
]
```

### 응답 초안 — 미승인

### 핵심 안내
내일 수영은 아직 실행되지 않은 계획이며 이후 재도포도 미정이에요. 실제 활동 전 제품 지침을 확인해 주세요 [kb:B-P03@0.6.1].

### 근거 및 이유
물 접촉과 재도포는 계획과 실제 행동을 구분해 살펴봐요 [ref:S05].

### 확인이 필요한 한계
수영을 이미 했거나 재도포를 빠뜨렸다고 판단하지 않아요.
