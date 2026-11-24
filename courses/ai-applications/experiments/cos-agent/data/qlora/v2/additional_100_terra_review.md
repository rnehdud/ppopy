# PPO-39 보완 — additional_100_terra

`development_preview`, `production_enabled=false`, 합성 개발 후보이며 공식 인수·사람 승인이 아니에요.
원문 관찰을 정형 슬롯과 연결하고 사례별 설명을 보완했어요. 전체 판단과 과거 기록은 README 및 `ppo39_revisions.json`을 확인해요.
KB 판정은 비교 명세에 대한 작성 기록이며 엔진 실행이나 임상 결과가 아니에요. 저장 문헌 청크는 요약이며 외부 원전의 직접 인용이 아니에요.

## syn-sol-0114

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0fb5aa4e76081233a26a8b285c2732ef16511d33dbf3a8bf8070e2675d8e196b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "currently_away_from_sunlight": true,
        "container_left_open": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "직사광선을 피하더라도 용기를 지속적으로 열어 둔 보관은 별도로 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "온도와 빛, 공기 및 취급이 화장품의 보관과 품질에 관련되는 자료예요. 개별 제품의 안정성 시험이나 모든 화장품에 공통인 사용기한을 대신하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
용기를 계속 열어 둔 보관 상태를 검토해요. [kb:B-S01@0.6.1]

### 근거 및 이유
직사광선을 피하는 것과 공기에 노출되는 보관은 별도로 살펴요.

### 확인이 필요한 한계
현재 상태만으로 제품의 품질이나 변질 여부를 확정할 수 없어요.

## syn-sol-0115

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `16045de1786596d716810f9621c8244433da825d6ac11435916c4b0ebe4719aa`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": {
        "water_added_to_original_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "water_added_without_instructions": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "difference",
      "guidance": "원제품에 임의로 물을 넣은 취급을 검토하되 이 사실만으로 오염 여부를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    },
    {
      "evidence_ref": "ref:S11",
      "text": "손이 한 번 닿으면 화장품은 정확히 사흘 뒤에 감염을 일으켜요. 스트레스 관리만 하면 그 기간이 두 배로 늘어요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/11511309/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "급성 실험과 테이프 스트리핑 후 회복 지표. 만성 스트레스 점수로 개인 발진의 원인을 확정할 수 없음. 연구별 군/프로토콜을 분리."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": [
    "ref:S11"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
원제품에 지침 없이 물을 넣은 취급을 검토해요. [kb:B-S03@0.6.1]

### 근거 및 이유
임의 첨가와 제품별 지시에 따른 사용을 구분해요.

### 확인이 필요한 한계
물 첨가만으로 오염이나 감염을 확정할 수 없어요.

## syn-sol-0116

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f3099bcfddd51bcf3faf513251aab9c05bfa0f4c17e036a698350400583956ef`
- 사람 검수: **미검수**

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
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "dry",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "apply_to_dry_skin": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "follows_product_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "exception",
      "guidance": "해당 제품의 건조 피부 도포 지시를 일반 보습 시점보다 함께 우선 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
해당 제품의 건조한 피부 도포 지시를 함께 우선 검토해요. [kb:B-M01@0.6.1]

### 근거 및 이유
일반적인 세정 후 보습 시점에는 제품별 지시에 따른 예외가 있어요.

### 확인이 필요한 한계
이 지시를 다른 제품에 일반화할 수 없어요.

## syn-sol-0121

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `076d4f15d96e09250d631ba235355150438bcf5f17d42f147959e4df2db22548`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.aftercare": {
      "variable_id": "shaving.aftercare",
      "state": "known",
      "value": {
        "continued_despite_stinging": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "repeated_stinging": true,
        "persistent_problem": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "반복 따가움에도 후처리를 계속했지만 그 이유와 모든 보습 중단 여부는 미확인이라 차이를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "General skin-care guidance discusses moisturizing after shaving and fragrance-free choices when irritation is a concern. An additional aftershave product is not established as mandatory for every person.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
후처리 제품 사용을 계속하는 가운데 반복 따가움이 보고됐어요. 이를 효과의 증거로 단정하지 않아요 [kb:B-M05@0.6.1].

### 근거 및 이유
따가움을 견디는 이유와 보습 중단 여부는 확인되지 않아 KB의 차이 조건 충족을 확정하지 않아요 [kb:B-M05@0.6.1].

### 확인이 필요한 한계
반복 반응과 후처리·보습 경험을 확인해요. 원인이나 치료 효과는 이 기록으로 확정할 수 없어요.

## syn-sol-0122

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `53f1569b4cb1e1f65a50906a591bf7f7fdfb8efc2693bd61d646667eab42696e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "topping_up_authorized": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sharing_refill": {
      "variable_id": "storage.sharing_refill",
      "state": "known",
      "value": {
        "refill_allowed": true,
        "topped_up_remaining_contents": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "difference",
      "guidance": "리필 허용 표시와 남은 내용물 위 덧붓기 지침은 별개로 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "Cosmetic microbiological-safety guidance advises against adding water or saliva and discusses clean handling and labeled storage. A single contact does not establish contamination, infection, or a fixed disposal deadline.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S07@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
리필 허용과 남은 내용물 위에 덧붓는 방법을 구분해요. [kb:B-S07@0.6.1]

### 근거 및 이유
확인된 리필 허용이 곧 덧붓기 허용을 뜻하지는 않아요.

### 확인이 필요한 한계
이 사실만으로 현재 오염 여부나 품질을 확정할 수 없어요.

## syn-sol-0127

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `acb208725ff8841f9f94203244f494eaf777b79835a669a1fa2aa5bd45dddf33`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.tightness": {
      "variable_id": "skin.tightness",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "comfortable": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "considering_other_person_amount": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "aligned",
      "guidance": "본인에게 편안한 현재 사용과 다른 사람의 정량 기준을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "General dry-skin guidance discusses moisturizing after washing while skin remains slightly damp. It does not prescribe the same amount for every skin type or formulation and does not establish an individual treatment effect.",
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

### 응답 초안 — 미승인

### 핵심 안내
현재 보습이 편안하다면 다른 사람의 정량을 그대로 맞출 필요는 없어요. [kb:B-M02@0.6.1]

### 근거 및 이유
현재 건조감과 당김이 없고 사용이 편안하다는 본인 관찰을 반영해요.

### 확인이 필요한 한계
현재 충족 상태는 제품 전체의 효과나 안전성 보증이 아니에요.

## syn-sol-0141

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `345adc8ff6072aa061a3aa3413c560006eb732b7c8eb17f5b57732db9c7c168f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": false,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": false,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true,
        "context": "야외 행사"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "reapplied": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "물이나 수건 접촉이 없더라도 장시간 야외 노출 중 재도포하지 않은 실제 행동을 확인했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sunscreen guidance considers continued exposure as well as water, sweat and towel contact. The absence of one loss event does not measure actual ultraviolet exposure.",
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

### 응답 초안 — 미승인

### 핵심 안내
야외 행사에 오래 머무는 동안 다시 바르지 않았다고 하셨어요. 물이나 수건 접촉이 없더라도 야외 일정과 제품 지침에 맞춰 재도포 시점을 살펴봐요. [kb:B-P03@0.6.1]

### 근거 및 이유
지속되는 노출도 광보호 안내에서 고려하는 요소예요. [ref:S05]

### 확인이 필요한 한계
물과 수건 접촉이 없다는 보고만으로 다른 손실 계기나 실제 받은 자외선량을 알 수는 없어요.

## syn-sol-0144

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1763e3ef58e6f6fe6f901d947a3336cca7a02f77f1d67a7b8f1e949025a33cb8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated_with_same_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "stopped_near_eye_use": true,
        "protective_eyewear_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "눈가 사용 중단과 보호용 안경 사용이 보고됐지만 안경의 자외선 차단 여부가 미확인이라 대체 광보호 확보를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변 자외선차단 안내는 제품 선택과 눈에 흘러드는 상황을 함께 살펴요. 개인의 눈시림 원인을 특정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
같은 제품에서 반복 눈시림이 보고됐고 눈가 사용을 멈추며 보호용 안경을 사용한다고 해요. 안경의 자외선 차단 여부는 미상이에요 [kb:B-P06@0.6.1].

### 근거 및 이유
KB의 대체 광보호 확보 조건이 충족됐는지 확인되지 않아 이 항목을 적합으로 확정하지 않아요 [kb:B-P06@0.6.1].

### 확인이 필요한 한계
안경의 광보호 여부와 사용 조건을 확인해요. 같은 제품이라는 사실만으로 매번 같은 방식으로 사용했는지는 알 수 없어요.

## syn-sol-0145

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `056bac32f471416041c4808ff8e21bfc8883017a2e6db7777600103acf83de67`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face",
        "ears"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "known",
      "value": [
        "ears"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "excluded_site": "ears"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "ear_omission_due_to_label_restriction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "exception",
      "guidance": "노출된 귀를 빼는 이유가 확인된 제품의 사용 제한과 연결되어 일반 도포 기준의 예외를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 제품 지침과 노출 상황을 함께 살펴요. 개인의 실제 자외선량이나 보호율을 이 자료로 계산하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
귀는 노출되지만 이 제품은 귀 사용이 제한되어 있어요. 확인된 제한을 무시하고 귀에 바르도록 권하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
귀를 뺀 행동은 제품 표시와 연결된 예외로 살펴요.

### 확인이 필요한 한계
이 정보만으로 다른 제품의 적합성이나 보호 정도는 알 수 없어요.

## syn-sol-0146

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f88610a7df02eaf2f5d0ce747f1a14d56b0f00de131c384ab604410e83132138`
- 사람 검수: **미검수**

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
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true,
        "continues_after_rain": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "reapplied": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "비에 젖은 뒤에도 야외 노출이 계속되지만 다시 바르지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun protection guidance considers exposure, water, sweat, towel contact and product directions. It does not calculate an individual ultraviolet dose.",
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

### 응답 초안 — 미승인

### 핵심 안내
비에 젖은 뒤에도 야외 활동이 계속됐고 재도포하지 않은 것으로 보고됐어요. 야외 일정과 제품 지침에 맞춰 재도포 시점을 검토해요 [kb:B-P03@0.6.1].

### 근거 및 이유
재도포 안내에서는 지속되는 야외 노출이나 물 접촉과 실제 재도포 행동을 함께 비교해요 [kb:B-P03@0.6.1]. 제공된 일반 안내도 물·땀과 야외 노출을 제품 표시 및 다른 보호 수단과 함께 살펴요 [ref:S05].

### 확인이 필요한 한계
해당 제품의 개별 지침은 제공되지 않았어요. 이 기록만으로 개인의 자외선 노출량이나 보호율을 계산할 수 없어요.

## syn-sol-0147

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `7d0edb6260fc529789ac7df53116816871f0889153159927bf2afc792161edea`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true,
        "minutes": 80
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
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
        "continues_after_towel": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "after_towel": false,
        "reason": "내수성 시간 표시가 재도포를 면제한다고 생각함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "내수성 시간 표시를 재도포 면제로 오해해 수건 접촉 후 야외 노출 중 다시 바르지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun protection guidance considers outdoor exposure, water contact and product instructions. It does not calculate individual ultraviolet exposure or protection.",
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

### 응답 초안 — 미승인

### 핵심 안내
수건을 사용한 뒤에도 야외 활동이 이어졌다면 제품 지침과 함께 재도포를 살펴봐요. 표시된 내수성 80분을 수건 접촉 후 재도포가 필요 없다는 뜻으로 해석하지 않아요. [kb:B-P03@0.6.1]

### 근거 및 이유
광보호 안내는 야외 노출, 물 접촉과 제품 지침을 함께 고려해요. [ref:S05] 수건으로 닦인 경우에도 재도포를 살펴볼 필요가 있어요. [kb:B-P03@0.6.1]

### 확인이 필요한 한계
표시된 시간만으로 개인이 실제 받은 자외선량이나 보호율은 계산할 수 없어요.

## syn-sol-0148

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6d4d13c47fe8072ef8339a612ec4cc63af0d8aac4ed22717bd2357b4d6f02ca2`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "prolonged": true,
        "outdoor_exposure_ended": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "after_going_inside": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "야외 노출이 끝난 뒤 재도포하지 않았다는 정보만으로 그 이전 야외 활동 중 행동을 알 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun protection guidance considers exposure, water, sweat, towel contact and product directions. It does not calculate an individual ultraviolet dose.",
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

### 응답 초안 — 미승인

### 핵심 안내
실내에 들어간 뒤 재도포하지 않은 기록만으로 긴 야외 활동 중의 행동을 판정할 수 없어요. [kb:B-P03@0.6.1]

### 근거 및 이유
야외 노출 종료 전과 종료 후의 행동은 다른 시간대예요.

### 확인이 필요한 한계
야외에서 재도포했는지는 미상이므로 필요하면 그 구간을 확인해요.

## syn-sol-0149

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `95e9a873b973ce589863c309277e80a568cc8263991f02f0676c496b0e67d8f2`
- 사람 검수: **미검수**

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
      "state": "known",
      "value": 50,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "broad_spectrum_uva_uvb": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_swimming": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "수영용 후보에 내수성 표시가 없지만 표시 부재만으로 실제 성능 미충족을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Sunscreen selection guidance discusses SPF, broad-spectrum protection and water resistance. One label feature does not establish another.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
수영을 계획하며 살펴본 후보에는 내수성 표시가 없어요. 표시가 없다는 사실만으로 시험상 내수성 실패를 확정하지 않고 제품 선택 판단을 유보해요 [kb:B-P01@0.6.1].

### 근거 및 이유
야외용 제품 선택에서는 새 야외용 후보의 성능이 부족한 것으로 확인됐을 때와 정보가 부족한 경우를 구분해요 [kb:B-P01@0.6.1]. SPF 50과 UVA·UVB 표시가 있다는 사실도 물에서의 성능을 대신 확인해 주지는 않아요.

### 확인이 필요한 한계
이 후보의 실제 내수성 시험 결과와 개인에게 나타날 보호 결과는 알려지지 않았어요.

## syn-sol-0160

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `457400e1bb983108c9a43d07cd5206dfcc0f5ffefc363464e26160062d1180d7`
- 사람 검수: **미검수**

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
      "state": "known",
      "value": 15,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "broad_spectrum_uva_uvb": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "difference",
      "guidance": "새 야외 후보는 광범위 보호와 내수성 표시가 있지만 SPF 15로 확인돼 기본 SPF 기준과 차이가 있어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "자외선차단제 선택 안내는 SPF 30 이상과 광범위 보호 및 내수성을 다뤄요. 표시 항목 하나로 다른 항목을 대신 확인하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외용 새 후보를 비교할 때 SPF 15 표시를 확인했어요. 광범위 보호와 내수성 표시가 있더라도 SPF가 더 높은 후보도 비교해 보세요. [kb:B-P01@0.6.1]

### 근거 및 이유
일반 선택 안내는 SPF 30 이상, 광범위 보호와 내수성을 각각 살펴요. 한 표시가 다른 표시를 대신하지 않아요. [ref:S16]

### 확인이 필요한 한계
표시는 개인의 실제 보호율이나 사용 적합성을 측정한 결과가 아니에요.

## syn-sol-0166

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b09d1e39bc32e092fe3dd3b14f0363accf4fae16664d5cbd3e93a66a765c3a2e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "사용": "합성 수면팩을 밤에 표시된 방식으로 사용",
        "중복 관리": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "확인된 표시": "밤에 바르고 다음 날 아침 씻어내는 사용을 허용"
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
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "사용 중 불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "해당 제품은 표시에서 밤새 사용하는 방법을 허용하고 실제 방식도 일치해요. 취침 사용이라는 이유만으로 임의 사용 차이를 만들지 않아요. 전체 비교에 필요한 중복 또는 사용 기간 정보는 미상이므로 전체 정렬 여부는 확정하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
확인된 수면팩의 밤 사용은 표시된 방법과 일치해요. [kb:B-G05@0.6.1]

### 근거 및 이유
제품 지침과 실제 사용을 비교하되 다른 관리의 중복은 확인되지 않았어요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
전체 관리의 정렬 여부는 미상이며 사용법의 일치가 안전성 보증은 아니에요.

## syn-sol-0167

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b55e319641a7a8f794251be971975b386993fb501617ac105d6c2a53df60d403`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "확인된 표시": "합성 세정액 한 부분에 물 네 부분을 섞어 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "실제": "세정액 한 부분에 물 한 부분을 섞음",
        "대상": "같은 표시 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "희석해 쓰는 합성 세정액",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "제조사가 희석을 명시했지만 실제 비율은 그 지시와 달라요. 희석 자체의 허용과 확인된 비율 준수 여부를 구분해요."
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

### 응답 초안 — 미승인

### 핵심 안내
실제 희석 비율이 확인된 제품 표시와 달라요. 해당 제품의 표시 비율을 확인해 사용법을 검토해요. [kb:B-G04@0.6.1]

### 근거 및 이유
제조사의 희석 허용과 실제 비율이 지시에 맞는지는 별개예요. [kb:B-G04@0.6.1]

### 확인이 필요한 한계
이 차이만으로 위해나 특정 피부 반응을 확정하지 않아요.

## syn-sol-0168

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1dc1a6d7f548411ccc206698c1990f47269dc6caaa028f1a430a1a36ef013bcf`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품 가": "합성 세럼 가",
        "제품 나": "합성 세럼 나"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.dispensing_unit_context": {
      "variable_id": "product.dispensing_unit_context",
      "state": "known",
      "value": {
        "용기": "서로 다른 스포이드",
        "방울 질량 확인": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "주장": "가의 두 방울과 나의 두 방울은 같은 질량"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "나의 표시": "적당량 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "difference",
      "guidance": "서로 다른 용기의 같은 방울 수를 같은 질량으로 환산할 근거는 없어요. 제품별 표시와 기록을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
서로 다른 스포이드의 같은 방울 수를 같은 질량으로 환산하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
방울 크기는 용기와 제품 맥락에 따라 다를 수 있어요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
현재 각 용기의 방울 질량과 밀도가 확인되지 않아 정량 환산은 보류해요.

## syn-sol-0169

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4802eb2d3c5926046f969f73ec99d3e783f6c5052c382b1b178eabb4d5d5a839`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "얼굴": "건식 전용 전기면도기",
        "목": "습식 수동 날면도"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.preparation": {
      "variable_id": "shaving.preparation",
      "state": "known",
      "value": {
        "얼굴": "물과 크림 없이 사용",
        "목": "적시고 면도용 젤 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.schedule_sites": {
      "variable_id": "shaving.schedule_sites",
      "state": "known",
      "value": {
        "시점": "같은 날",
        "부위": "얼굴과 목"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "전기면도기": "건식 전용",
        "면도용 젤": "습식 날면도에 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G09",
      "status": "aligned",
      "guidance": "같은 날이어도 각 부위의 실제 방식과 해당 지시를 따로 대조해요. 습식 준비를 건식 전용 기기에 이식하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G09@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
건식 전용 전기면도기와 습식 수동 면도의 준비를 각 지시에 맞게 구분할 수 있어요. [kb:B-G09@0.6.1]

### 근거 및 이유
목의 습식 준비를 얼굴의 건식 기기에 그대로 적용하지 않아요. [kb:B-G09@0.6.1]

### 확인이 필요한 한계
방식별 지침과의 일치는 전체 안전성이나 개인 적합성 보증이 아니에요.

## syn-sol-0170

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d00ccd41ce2f7d22adcea4b2c551181e59f8ede02cd195860876a55855a6cd66`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "확인된 회피 성분": "Linalool",
        "확인": "의료진에게 해당 성분 회피 안내를 받음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "대상": "합성 후보의 현행 버전",
        "확인된 표기": "Linalool"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "일반 선호": "향의 유무는 중요하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.label_warnings": {
      "variable_id": "product.label_warnings",
      "state": "known",
      "value": {
        "성분표 버전": "현행 버전과 일치"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "aligned",
      "guidance": "확인된 개인 회피 성분과 현행 성분표의 정확한 일치를 일반적인 향 선호와 구분해요. 모든 사람의 금지 성분이나 농도는 추정하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
확인된 개인 회피 성분 Linalool이 현행 후보 성분표와 일치해요. 개인의 회피 지시를 우선해 해당 후보를 검토해요. [kb:B-G17@0.6.1]

### 근거 및 이유
개인에게 확인된 알레르겐과 일반적인 향 선호는 다른 정보예요. [kb:B-G17@0.6.1]

### 확인이 필요한 한계
이를 모든 사람에게 금지되는 성분이나 특정 농도·반응의 확정으로 확대하지 않아요.

## syn-sol-0171

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c67d971f0ba006920b9acace808131923167ef91fc1e66843ddc5a4bba49fba4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "introduction.change_scope": {
      "variable_id": "introduction.change_scope",
      "state": "known",
      "value": {
        "첫 변경": "월요일 합성 보습제 도입",
        "둘째 변경": "수요일 합성 세정제 도입"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "관찰": "두 변경 후 토요일에 당김을 느낌",
        "변경 전후 기록": "두 제품의 관찰 기간이 겹침"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "실제 사용": "두 제품을 계속 사용함",
        "원인 주장": "나중에 시작한 세정제가 반드시 원인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G12",
      "status": "unknown",
      "guidance": "시작일이 달라도 관찰 기간이 겹치므로 이후 느낌의 원인을 어느 한 제품으로 확정할 수 없어요. 차이를 자동으로 판정하거나 고정 대기 기간을 만들지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
시작일이 달라도 두 제품의 관찰 기간이 겹쳐 한 제품을 원인으로 단정할 수 없어요. [kb:B-G12@0.6.1]

### 근거 및 이유
변경 시점과 실제 사용 기록은 원인 판단의 맥락이지만 인과관계의 증명은 아니에요. [kb:B-G12@0.6.1]

### 확인이 필요한 한계
당김의 원인은 미상이며 확인되지 않은 고정 대기기간이나 재노출을 만들지 않아요.

## syn-sol-0172

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fc157e35ae8dfeba282e35cb8d27c59a9d92b9fad2af2b8e1b6d23297e5d602b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "가": "일반 레티놀 관리 화장품",
        "나": "AHA 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "얼굴",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제": "서로 다른 날 사용",
        "처방 변경": "없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "서로 다른 날의 실제 사용을 같은 시간 중첩으로 바꾸지 않아요. 개인 반응과 제품 지시는 별도로 확인해요. 전체 비교에 필요한 중복 또는 사용 기간 정보는 미상이므로 전체 정렬 여부는 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about additional exfoliation while using retinol or prescription retinoids. Product purpose and application context matter. It does not establish a universal prohibition for every ingredient combination or an individual risk probability.",
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

### 응답 초안 — 미승인

### 핵심 안내
레티놀과 AHA 관리가 서로 다른 날 이뤄졌지만 전체 중첩 비교는 미상이에요. [kb:B-G13@0.6.1]

### 근거 및 이유
날짜 분리만으로 겹치는 사용기간이나 적합성을 자동 확정하지 않아요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
구체적인 빈도와 기간이 확인되지 않았고, 처방 변경이나 무자극을 추정하지 않아요.

## syn-sol-0173

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `951369dc95c1a09d75fe7c70bd5bdfe3b76e2607af07a650ce6d394a569912db`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "가": "AHA와 BHA 기능을 표시한 단일 복합 완제품",
        "나": "별도 BHA 각질관리 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "사용": "두 제품을 얼굴 같은 부위에 함께 사용",
        "가와 나": "별도 완제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "가": "복합 완제품",
        "나": "별도 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "difference",
      "guidance": "복합 완제품 내부 기능과 별도 BHA 제품을 구분하되, 두 완제품의 같은 부위 실제 중첩을 별도로 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about additional exfoliation while using retinol or prescription retinoids. Product purpose and application context matter. It does not establish a universal prohibition for every ingredient combination or an individual risk probability.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
복합 완제품과 별도의 BHA 제품이 같은 부위에 사용돼 별도 제품 간 중첩을 검토해요. [kb:B-G15@0.6.1]

### 근거 및 이유
하나의 복합 완제품 안의 두 기능과 추가된 별도 제품의 실제 중첩을 구분해요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
중첩은 개인 위해나 임상 결과를 확정하지 않으며 제품별 지시와 개인 상황을 확인해요.

## syn-hold-0036

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `c6f03806db5707af2c28767ff3bd469e1654f23f81e18d22256df998a111d9a5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_odor": true,
        "previously_no_odor": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "odor_change_normal": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "기존 기록과 달라진 새 냄새는 품질 확인 전 사용과 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
기존과 다른 새 냄새가 확인돼 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
품질 확인 전 해당 제품의 사용을 우선 멈춰 주세요 [kb:B-S04@0.6.1]. 제품의 표시와 변화 이력을 확인하고 필요하면 제조·판매처에 품질을 문의해요.

## syn-hold-0037

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `bb401f986cf827d9bd1a1d63a066b1b0cef37e69c058d42922e318068fd2152e`
- 사람 검수: **미검수**

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
        "cleanser_stopped": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "follow_up_advised": true,
        "user_wants_to_cancel_follow_up": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편과 통증이 확인됐고 진료 후속 확인을 중단하려는 요청은 개별 권고보다 전문가 확인이 우선이에요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
지속 불편과 통증이 확인돼 개별 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
확인된 진료 후속 계획과 상담을 전문가에게 확인해 주세요. 세안제 중단과 통증의 전후 관계는 알 수 없어요.

## syn-hold-0038

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `b3a7f60b8101e0de6be24305e904930c029668cc732a9b338cbc52fbeb9e2159`
- 사람 검수: **미검수**

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
    "hand.protection_hygiene": {
      "variable_id": "hand.protection_hygiene",
      "state": "known",
      "value": {
        "gloves_changed": true,
        "required_protection": true,
        "wants_to_abandon_required_protection": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "심한 지속 통증과 필수 보호장비 중단 요청에 대해 개별 권고를 보류하고 전문가 확인을 우선해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
심한 지속 통증이 확인돼 개별 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
필수 보호장비에 관한 작업 지침과 현재 통증은 관련 전문가에게 확인해 주세요. 장갑 변경과 통증의 전후 관계는 미상이에요.

## syn-hold-0039

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `22b5b82de629f9458782a838ba4987b4218983a9d9d7265212385300fb143c5a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_leakage": true,
        "container_damage": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "expiry_not_passed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "기한이 남은 사실만으로 새 누출과 용기 손상에 대한 품질을 확인할 수 없어 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 누출과 용기 손상이 확인돼 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
품질 확인 전 해당 제품의 사용을 우선 멈춰 주세요 [kb:B-S04@0.6.1]. 기한이 남았다는 사실만으로 품질을 확정할 수 없어요. 표시와 용기 상태를 확인하고 필요하면 제조·판매처에 문의해요.

## syn-hold-0040

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `3890aaaa5c5f68c3c01bc8ab0ed3c03570a72e6782e66ce7bc05f6430aae8973`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "skin_penetrating": true,
        "cleaning_done": true,
        "requests_reuse_protocol": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "세척 여부와 관계없이 피부 관통 기기의 개인 시술 절차 안내를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
피부 관통 기기의 개인별 시술이나 재사용 절차 안내를 보류해요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
세척 여부만으로 시술의 안전성을 확정할 수 없어요. 적절한 전문가에게 확인해 주세요.

## syn-hold-0041

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `41ed2df795d517138b8f7c1539fea17b75cbc42d72f10d80087e4ea3fa9882b5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "plans_combination": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "device_combination_permitted": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "avoid_device_after_procedure": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "제품 안내와 개별 의료진의 기기 회피 지시가 충돌해 개인별 병용 설계를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품 안내와 개별 의료진의 기기 회피 지시가 충돌해 병용 설계를 보류해요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
의료진에게 개인 지시의 적용 범위를 확인해 주세요.

## syn-hold-0042

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `72b4d558f691c3ef8892c57883fbf220c1f94982d01aab9defe7c4fe908431af`
- 사람 검수: **미검수**

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
        "moisturizer_reduced": true,
        "wants_amount_adjustment_only": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 통증을 사용량 조절만으로 해결할 수 있다고 확정하지 않고 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
지속 통증에 대해 사용량 조절만으로 해결한다고 판단하지 않고 개별 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
통증과 감량의 전후 관계나 원인은 확인되지 않았어요. 의료 전문가에게 확인해 주세요.

## syn-hold-0043

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `7c2d37cbe6dd66a2400b0169534be5fc9c435b71b17fa2c59695329d047b1377`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_particles": true,
        "color_or_odor_change": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.decanting": {
      "variable_id": "storage.decanting",
      "state": "known",
      "value": {
        "planned": true,
        "already_done": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 입자와 색 또는 냄새 변화가 있어 용기 이동 계획보다 품질 확인을 우선해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 입자와 색 또는 냄새 변화가 확인돼 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
품질 확인 전 해당 제품의 사용을 우선 멈춰 주세요 [kb:B-S04@0.6.1]. 변화 이력과 제품 표시를 확인하고 필요하면 제조·판매처에 품질을 문의해요.

## syn-hold-0044

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `8d87e133b9c94d20676ac18909ab0d62f9b124ddf750f8d81edcbcbc428cf60c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "application_timing_known": false,
        "reported_pain_context": {
          "site": "눈",
          "persistent": true
        }
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
      "guidance": "지속 불편이 보고됐고 통증의 별도 항목과 맥락 기록이 일치하지 않아 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
지속 불편이 보고됐지만 별도의 통증 항목은 미상이고 맥락에는 지속적인 눈 통증이 기록되어 있어요. 개별 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
이 기록 차이와 지속되는 불편을 의료 전문가에게 설명해 확인해 주세요. 원인은 확정하지 않아요.

## syn-hold-0045

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `08a3036f575f452c81489b4696293db0a628f7b514a5b452c1d077a52b86c890`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_odor": true,
        "separation": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_reuse_before_seller_reply": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 냄새와 분리의 품질 확인 전에 재사용을 전제로 한 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 냄새와 분리가 보고되어 개별 권고를 보류해요. 해당 제품은 우선 사용을 멈춰 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
관찰된 품질 변화와 용기 정보를 제조·판매처에 전달해 확인해 주세요. 실제 품질이나 원인은 확정하지 않아요.

## syn-hold-0046

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `e14fab9977757ccb30a5ee991cdb1b1f05378bd4e5d6e2e66274cb161dba1f7c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "contents_identity_unknown": true,
        "quality_concern": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.end_of_use": {
      "variable_id": "commerce.end_of_use",
      "state": "known",
      "value": {
        "seller_requested_return_for_testing": true,
        "official_current_notice_same_product": "반송하지 않고 안전 처리 및 공식 창구 확인",
        "instruction_conflict": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q06",
      "status": "hold",
      "guidance": "내용물이 불명확한 합성 제품에 대해 판매자 반송 요청과 같은 현행 제품의 공식 처리 공지가 달라 개별 재사용 권고를 보류해요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-terra-b46",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품의 현행 공식 처리 공지 예시: 반송하지 않고 안전 처리를 안내하며 공식 창구에 확인해요. 판매자는 검사 목적 반송을 별도로 요청했어요.",
      "evidence_ref": "catalog:syn-terra-b46@v1"
    }
  ],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q06@0.6.1",
    "catalog:syn-terra-b46@v1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
내용물이 불명확한 해당 제품은 사용하지 말고 개별 권고를 보류해요. [kb:B-Q06@0.6.1]

### 필요한 다음 단계
합성 현행 공식 안내는 반송하지 않고 안전 처리와 공식 창구 확인을 안내하지만 판매자는 검사 목적 반송을 요청했어요. [catalog:syn-terra-b46@v1] 두 안내의 대상과 현행성을 공식 창구에 확인해 주세요. 구체적인 반송·보관·처리 방법은 여기서 정하지 않아요.

## syn-hold-0047

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `26e8e0b6301c860681601ad100abb96f0bda5f7d226259d584cf77e1197e6f24`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_odor": true,
        "container_damage": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_use_smaller_amount": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "품질 이상 의심을 사용량 조정만으로 해결하는 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 냄새와 용기 손상이 보고되어 개별 권고를 보류해요. 양을 줄여 계속 쓰지 말고 해당 제품의 사용을 우선 멈춰 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
관찰된 냄새와 용기 손상을 제조·판매처에 전달해 품질 확인을 요청해 주세요. 원인은 확정하지 않아요.

## syn-hold-0048

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `231d7df628014c968d6b5b15363da9a4fcac2771e72d40926d507abcaffe7b7f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "new_particles": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "synthetic_recall_lot_match": false,
        "wants_resume_because_not_recalled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "합성 회수 공지의 대상 로트에는 해당하지 않지만 새 이물이 보고되어 품질 확인 전 개별 재사용 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
합성 회수 공지의 대상 로트에는 해당하지 않지만 별도의 새 이물이 보고되어 개별 권고를 보류해요. 해당 용기의 사용을 우선 멈춰 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
새 이물과 로트 정보를 제조·판매처에 전달해 품질을 확인해 주세요. 회수 비대상이라는 사실만으로 품질을 확정하지 않아요.

## syn-hold-0049

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `82866f3d16761747e38981abc419c4ea71f0a6ef8c5a0641c83e7e5d1137bb75`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "one_container_new_separation": true,
        "other_container_unchanged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_mix_containers": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "한 용기에 새로운 분리가 관찰돼 두 용기를 섞는 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
한 용기에 새로운 분리가 관찰되어 개별 권고를 보류해요. 분리가 관찰된 용기의 사용을 우선 멈춰 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
관찰된 변화와 해당 용기 정보를 제조·판매처에 전달해 확인해 주세요. 실제 품질이나 원인은 확정하지 않아요.

## syn-hold-0050

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `00fa57325b170a7d40635818bbebd1bac5bdbe897b5f017f5a52f5c61e880136`
- 사람 검수: **미검수**

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
        "wants_to_follow_general_label_despite_symptoms": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "persistent_swelling"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 부종을 일반 사용 지침만으로 해결하는 개별 권고를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
부종이 지속된다고 하셨으므로 일반 표시만 따라 해결하는 개별 사용 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지속된 부종과 현재 상황을 의료 전문가에게 설명하고 확인받아 주세요. 원인과 개인별 대응은 여기서 확정할 수 없어요.

## syn-hold-0051

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `31bd0f80cbdc78ef127cc3d869e488b0f1e904b015fb9d5ae05ba0c2fd3a3e9f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 제품 가 현행 로트",
        "나": "다른 합성 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "용기 가": "공식 회수 대상 일치 확인",
        "용기 나": "대상 여부 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "확인된 회수 대상에 대한 보류와 다른 용기의 미확인을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
용기 가는 공식 회수 대상과 일치한다고 확인되어 개별 제품 판단을 보류해요. [kb:B-Q05@0.6.1]

### 필요한 다음 단계
용기 가는 해당 공식 회수 절차를 확인해 따라 주세요. 다른 용기 나는 대상 여부가 미상이므로 별도로 확인해 주세요. [kb:B-Q05@0.6.1]

## syn-hold-0052

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `323dcfe11f10a39a58d627809fd80af9c3175e50a25da5c922d60b20f37313c2`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품명": "회수 공지와 합성 제품명이 일치"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.batch": {
      "variable_id": "storage.batch",
      "state": "known",
      "value": {
        "제조번호": "지워져 읽을 수 없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "공지 범위": "특정 제조번호만 해당",
        "공지 지시": "번호 확인 전 판매처에 문의",
        "대상 일치": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "제품명만으로 대상 로트 일치를 확정하지 않고 해당 용기의 개별 판단을 보류하며 제조번호 확인 경로를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품명은 공지와 일치하지만 제조번호가 읽히지 않아 해당 용기의 회수 대상 여부와 개별 판단을 보류해요. [kb:B-Q05@0.6.1]

### 필요한 다음 단계
특정 번호에만 적용되는 공지 범위를 유지하고 안내된 판매처에 제조번호 확인 방법을 문의해요.

## syn-hold-0053

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `f329242f6f663cd270a6c3456848096bfa57dd258aa8d0da6bcb821f73c907a0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "모드 가": "합성 보습제 병용 허용",
        "모드 나": "같은 보습제 병용 금지",
        "적용 기기": "같은 합성 기기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "기기와 보습제": "함께 사용했다고 보고",
        "실제 사용 모드": "확인되지 않음",
        "질문": "해당 조합을 계속해도 되는지"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "모드별 지시는 확인됐지만 실제 모드가 미상이므로 해당 기기와 제품 조합의 개인별 판단을 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
기기의 두 모드에 대한 병용 지시가 다르고 실제 사용 모드는 미상이어서 해당 조합의 개별 판단을 보류해요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
실제 모드와 같은 제품에 적용되는 지시를 기기 제조사에 확인해요. 다른 일반 관리의 상태까지 추정하지 않아요.

## syn-hold-0054

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `b4ef5dc224885b5531fb6afaa5f372265f6f15fe5f72d0396dffe1d7c429e26b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "현재 용기": "이전에는 없던 입자 발생"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "용기 표시": "입자 발생 시 사용하지 말고 문의"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.seal_integrity": {
      "variable_id": "storage.seal_integrity",
      "state": "known",
      "value": {
        "판매 안내": "모든 입자가 정상이라고 안내",
        "동일 용기 확인 여부": "미상"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 입자와 제품 표시를 확인하고 동일 용기에 적용되는지 불명인 상충 안내를 분리하여 개별 판단을 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 입자가 보고되어 개별 판단을 보류해요. 용기 표시는 입자가 생기면 사용하지 말고 문의하도록 안내하므로 해당 제품을 사용하지 말아 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
상충하는 판매 안내가 이 용기에 적용되는지 제조·판매처에 확인해 주세요. 변질 원인이나 제품 전체의 안전성은 확정하지 않아요.

## syn-hold-0055

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `a57371e6d69dfc5724105bcf52863044d0128541e17e2ce17564fdfb4507bd89`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "일반 화장품",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "질문": "이 화장품과 비슷한 성분이라는 이유로 처방 의약품의 이름과 용량 및 시작 절차를 정해 달라는 요청",
        "현재 증상": "없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "hold",
      "guidance": "화장품의 성분 유사성만으로 개인의 처방 의약품 이름·용량·시작 절차를 설계하는 요청은 일반 제품 안내의 범위를 벗어나 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
화장품 성분이 비슷하다는 정보만으로 개인에게 맞는 처방 의약품의 이름·용량·시작 절차를 정하는 요청은 보류해요. [kb:B-G03@0.6.1]

### 필요한 다음 단계
개인별 의약품 선택과 사용 계획은 의료 전문가와 상담해요. 현재 개인 진료 계획은 확인되지 않았어요.

## syn-hold-0056

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `1559da2df1bf4a571ea2ddba1aeac01b5b9b2d491ee0c77b5b235871bc45495b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "이전": "합성 피부 기기와 제품을 함께 사용",
        "현재": "같은 조합 재사용 계획"
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
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "개별 기기 사용 지시": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "사용 뒤 지속되는 통증"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "지속 통증이 있는 기기 병용의 개별 사용 지시를 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
기기와 제품을 함께 사용한 뒤 지속되는 통증이 보고되어 개별 기기 사용이나 제품 권고를 보류해요. 해당 병용은 중단해 주세요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
현재 불편을 의료 전문가에게 확인받고 기존 사용 상황을 전달해 주세요. 원인이나 적절한 기기 설정은 추정하지 않아요.

## syn-hold-0057

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `ec735dd940a3c05c25df2b72e7a10eb0410d10a95f6c5f14b9e514743313413d`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "정상 표시": "사용 전 흔드는 2층 제형",
        "새 관찰": "이전과 다른 강한 냄새 발생"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "흔들어 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "표시 기한": "남음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "정상 2층 표시와 별개로 새 냄새 변화가 있어 해당 제품 판단을 보류해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제품에서 이전과 다른 강한 냄새가 관찰되어 해당 제품에 대한 개별 권고를 보류해요. 해당 제품의 사용을 우선 멈춰 주세요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
제품 상태와 표시를 제조·판매처에 확인해 주세요. 정상적인 두 층 표시와 새 냄새 변화는 별도로 살펴요.

## syn-hold-0058

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `5f424dadd61630e0e7220c698ecf93ea0699dbdf6f1bfe00fb7d09f448803479`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "의료진 확인 회피 성분": "Linalool"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.label_warnings": {
      "variable_id": "product.label_warnings",
      "state": "known",
      "value": {
        "현행 표시": "Linalool을 포함할 가능성이 있으므로 확인 전 사용을 보류",
        "대상": "합성 후보 현행 버전"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "introduction.local_trial": {
      "variable_id": "introduction.local_trial",
      "state": "known",
      "value": {
        "요청": "해당 후보의 국소 시험 여부",
        "실제 시험": "아직 하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "hold",
      "guidance": "확인된 개인 회피 성분에 대해 현행 후보 표시가 포함 가능성과 확인 전 사용 보류를 명시하므로 국소 시험 판단을 보류해요. 실제 함유 여부는 미상이에요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-terra-c58",
      "version": "1.0",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: Linalool을 포함할 가능성이 있으므로 확인 전 사용을 보류해요.",
      "evidence_ref": "catalog:syn-terra-c58@1.0"
    }
  ],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G11@0.6.1",
    "catalog:syn-terra-c58@1.0"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
현행 합성 후보의 표시가 확인된 개인 회피 성분의 포함 가능성과 확인 전 사용 보류를 안내하므로 국소 시험에 관한 개별 권고를 보류해요. [kb:B-G11@0.6.1] [catalog:syn-terra-c58@1.0]

### 필요한 다음 단계
표시된 성분 관련 정보를 제조·판매처와 의료 전문가에게 확인해요. 실제 함유 여부와 전성분은 미상이며 포함됐다고 확정하지 않아요.

## syn-hold-0082

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `0de763d43876e8be7c7f446c774a982715b6cfedb2fba964822163b360995291`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "label_expired": false
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "continues_using": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "hold",
      "guidance": "표시 기한이 남아 있어도 색 또는 냄새 변화가 보고되어 해당 제품의 품질 확인 전 개별 사용 권고를 보류해요. 어느 변화인지, 원인과 실제 보호 수준은 확정하지 않아요."
    },
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "표시 기한이 남아 있어도 색 또는 냄새 변화가 보고되어 해당 제품의 품질 확인 전 개별 사용 권고를 보류해요. 어느 변화인지, 원인과 실제 보호 수준은 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1",
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
표시 기한이 남아 있지만 색 또는 냄새의 변화가 보고되었고 계속 사용하고 있어요. 어떤 변화인지와 그 원인, 실제 보호 수준은 확인되지 않았어요. 품질을 확인하기 전까지 이 제품에 대한 개별 사용 권고를 보류해요. [kb:B-P08@0.6.1] [kb:B-S04@0.6.1]

### 필요한 다음 단계
품질이 확인될 때까지 해당 제품의 사용을 일시 보류해요. 제품 표시를 확인하고 제조판매업자 문의 창구에 보고된 변화를 알려 품질을 확인해요.

## syn-sol-0117

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `15c950863bda98542977d0bc14dcd7eb2e7227a54c46982347ac73ee392e7689`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "after_washing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "repeated_discomfort": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.protection_hygiene": {
      "variable_id": "hand.protection_hygiene",
      "state": "known",
      "value": {
        "required_hygiene_maintained": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "반복 불편은 확인됐지만 불편에도 계속 사용했는지는 미확인이에요. 필수 위생과 보습 맥락을 함께 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
반복된 손 제품 불편을 기록하고 위생과 보습 맥락을 함께 확인해요. [kb:B-M04@0.6.1]

### 근거 및 이유
불편이 반복됐어도 그 뒤 사용을 계속했는지는 확인되지 않았어요.

### 확인이 필요한 한계
그 사실만으로 사용 방식의 차이나 불편의 원인을 확정하지 않아요.

## syn-sol-0118

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `648de586891d0ef13d898a515da8ac70a8c15ec38b1d1547104e485d61539681`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "container_closed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "label_storage_conditions_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 밀폐 여부만으로 제품별 보관 지침의 충족이나 이전 온도 이력을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "온도와 빛, 공기 및 취급이 화장품의 보관과 품질에 관련되는 자료예요. 개별 제품의 안정성 시험이나 모든 화장품에 공통인 사용기한을 대신하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
현재 용기를 닫아 둔 상태는 기록하되 보관 지침 충족 여부는 미상으로 남겨요. [kb:B-S01@0.6.1]

### 근거 및 이유
현재 밀폐 여부만으로 해당 제품의 지침이나 이전 온도 이력을 알 수 없어요.

### 확인이 필요한 한계
품질이나 과거 열 손상을 확정할 수 없어요.

## syn-sol-0119

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2c5d1586711b99f38dc4cc09beaf460541b29a4bcaf5a1fbe9b9470a5a5b46b1`
- 사람 검수: **미검수**

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "plans_moisturizer_after_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "세정 뒤 보습할 계획만으로 실제 도포나 피부 물기 상태를 확인할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
세정 뒤 보습할 계획과 실제 도포 여부를 구분해요. [kb:B-M01@0.6.1]

### 근거 및 이유
계획만으로 실제 사용이나 도포 당시 피부 물기를 알 수 없어요.

### 확인이 필요한 한계
실제 도포와 피부 상태가 확인되기 전에는 시점의 차이를 판단하지 않아요.

## syn-sol-0120

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `7087112623e9a6370f646ec397476afe0aef66d592e83a027f25abe98f84ef14`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.care": {
      "variable_id": "shaving.care",
      "state": "known",
      "value": {
        "rinse_after_use": false,
        "dry_storage": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "tool.care_state": {
      "variable_id": "tool.care_state",
      "state": "known",
      "value": {
        "type": "manual_razor",
        "visible_residue": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S05",
      "status": "unknown",
      "guidance": "헹굼하지 않은 사실과 건조 보관은 확인됐지만 다른 세척의 수행이나 젖고 오염된 상태로 계속 사용했는지는 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Wet-shaving guidance discusses preparation, rinsing blades and dry storage, with a reference number of uses for manual blade replacement. The manual-blade reference is not an electric-head replacement interval.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S05@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
면도 도구를 헹구지 않은 사실과 건조 보관을 따로 살펴요. [kb:B-S05@0.6.1]

### 근거 및 이유
헹굼이 없었다는 기록은 다른 세척의 수행 여부를 알려주지 않아요.

### 확인이 필요한 한계
젖고 오염된 상태로 계속 사용했는지도 미확인이에요.

## syn-sol-0123

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2777c30bfe723e631a8098dc98fff2dc716d46db591a5f68fb8b85c9b43280e7`
- 사람 검수: **미검수**

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
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
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
      "status": "unknown",
      "guidance": "개봉 이력을 알아도 해당 제품의 개봉 후 안내가 없으면 사용 가능 기간을 계산하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "온도와 빛, 공기 및 취급이 화장품의 보관과 품질에 관련되는 자료예요. 개별 제품의 안정성 시험이나 모든 화장품에 공통인 사용기한을 대신하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
개봉 이력은 기록하되 개봉 후 사용 가능 기간은 미상으로 남겨요. [kb:B-S02@0.6.1]

### 근거 및 이유
해당 제품의 개봉 후 안내가 확인되지 않아 기간을 계산할 수 없어요.

### 확인이 필요한 한계
용기 이력만으로 현재 품질도 보증할 수 없어요.

## syn-sol-0124

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b052d9b891847436068c1c97a9a0f8e71ce7dcffe0bf17af432a15a71c715999`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "shaving.blade_use_history": {
      "variable_id": "shaving.blade_use_history",
      "state": "known",
      "value": {
        "uses": 6
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.blade_condition": {
      "variable_id": "shaving.blade_condition",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S06",
      "status": "unknown",
      "guidance": "도구 유형과 상태가 확인되지 않아 수동 날 참고 횟수를 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "습식 면도의 준비와 털 방향, 날 헹굼 및 건조 보관을 다루는 안내예요. 수동 면도날의 사용 횟수 참고를 전기헤드의 교체 주기로 바꾸지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S06@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
면도 도구 유형과 상태를 확인하기 전에는 교체 기준을 정하지 않아요. [kb:B-S06@0.6.1]

### 근거 및 이유
사용 횟수만으로 수동 날에 관한 참고를 해당 도구에 적용할 수 없어요.

### 확인이 필요한 한계
도구 유형과 상태는 미상이에요.

## syn-sol-0125

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0aa3add3a5a35b332db95f4b1474596df7f1d0ed36fe26aa322f4151a1294b52`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "tap_position_known": true,
        "perceived_temperature_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "수도꼭지 위치만으로 실제 물의 체감 온도를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "미온수와 손가락을 이용해 부드럽게 세안하고 강한 마찰을 피하는 일반 관리 원칙이에요. 특정 온도나 세안 시간의 절대 기준을 뜻하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
수도꼭지 위치로 세안수의 체감 온도를 추정하지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
온도가 뜨거웠는지 미온이었는지는 확인되지 않았어요.

### 확인이 필요한 한계
위치만으로 정확한 온도나 차이를 판단할 수 없어요.

## syn-sol-0126

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `90213efd52d721050d88d9b1b0ec5abafc9e55f170d945d0019f546c50cea430`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "same_container_label_conflict": true,
        "rinse_required_report": true,
        "no_water_rinse_report": true
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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "같은 용기의 헹굼 필요와 물 헹굼 불필요 기록이 충돌해 적용되는 지시와 이탈 여부를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance supports lukewarm water and gentle fingertip cleansing rather than vigorous rubbing. It does not establish a precise water temperature or an individual clinical outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
동일 용기의 헹굼 지시 기록이 충돌해 적용할 지시를 확인해요. [kb:B-C06@0.6.1]

### 근거 및 이유
물 헹굼이 필요하다는 기록과 필요 없다는 기록이 함께 있어요.

### 확인이 필요한 한계
어느 지시가 맞는지 미상이라 실제 사용을 이탈로 확정하지 않아요.

## syn-sol-0128

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `75f26798671bf0e9b5ce46d772d6a70a103b3857282ce5da955a0458236a6c0e`
- 사람 검수: **미검수**

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
    "tool.care_state": {
      "variable_id": "tool.care_state",
      "state": "known",
      "value": {
        "cleaned_after_use": true,
        "drying_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "손가락 이외 세안 도구 사용은 확인되지만 마찰 정도와 건조 보관은 별도로 미확인이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "미온수와 손가락을 이용해 부드럽게 세안하고 강한 마찰을 피하는 일반 관리 원칙이에요. 특정 온도나 세안 시간의 절대 기준을 뜻하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
손가락 이외의 세안 도구를 사용한 사실을 기본 방법과 구분해요. [kb:B-C02@0.6.1]

### 근거 및 이유
도구 사용 자체와 강한 마찰 여부는 서로 다른 관찰이에요.

### 확인이 필요한 한계
마찰 정도와 도구의 건조 보관은 확인되지 않았어요.

## syn-sol-0129

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `71cbec24ea9a2da1723af7a0ce43826ef92bb4ff8f63a73a3c9aaf53b96e918a`
- 사람 검수: **미검수**

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
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "second_step_purpose_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup_removed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "화장 제거 목적과 별도로 두 번째 단계의 목적은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "미온수와 손가락을 이용해 부드럽게 세안하고 강한 마찰을 피하는 일반 관리 원칙이에요. 특정 온도나 세안 시간의 절대 기준을 뜻하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
두 번째 세안 단계의 목적을 확인하기 전에는 불필요한 반복으로 확정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
화장 제거 목적과 추가 단계의 목적은 각각 살펴야 해요.

### 확인이 필요한 한계
단계 수만으로 과도한 세안이나 피부 손상을 진단할 수 없어요.

## syn-sol-0130

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `1e937924ab0bad787f8da63754275e37b4f7c1be0291723689f2f0c14eb305e6`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "heavy_feel": true,
        "dryness_relief_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "pumps": 1
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "무거운 느낌이나 펌프 횟수만으로 건조 불편이 충족됐는지 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
무거운 느낌과 별도로 건조 불편이 충족됐는지 확인해요. [kb:B-M02@0.6.1]

### 근거 및 이유
펌프 횟수나 사용감만으로 건조 관리의 충족 여부를 정할 수 없어요.

### 확인이 필요한 한계
건조 상태와 실제 충족 여부는 미상이에요.

## syn-sol-0131

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b49e08e79c76bbacbebc10ea8fac220e32ec43da869dfad0c3fd09c94229e6e5`
- 사람 검수: **미검수**

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
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "refill_allowed": true,
        "topping_up_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
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
      "guidance": "리필 표시만으로 잔량 위 덧붓기와 용기 적합성이 확인되지는 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
리필 표시와 잔량 위 덧붓기 및 용기 적합성을 따로 확인해요. [kb:B-S03@0.6.1]

### 근거 및 이유
리필이 허용된다는 사실만으로 모든 용기와 방법이 허용되지는 않아요.

### 확인이 필요한 한계
아직 계획 단계이며 용기 적합성과 덧붓기 허용은 미상이에요.

## syn-sol-0140

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b26a33163d1f64da77c0879cbb9ce63c1321ec24eb6e5d742a1982d4106f9303`
- 사람 검수: **미검수**

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
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true,
        "minutes": 80
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
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
      "guidance": "내수성 시간 표시는 확인되지만 SPF와 광범위 보호 표시는 확인되지 않아 기본 성능 판단을 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Professional sunscreen guidance discusses SPF, broad-spectrum coverage and water resistance. A water-resistance time is not an SPF value.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
새 야외용 후보의 80분 내수성 표시는 확인됐지만 SPF와 광범위 보호 표시는 아직 알 수 없어요. 구매 비교 전에 두 표시를 각각 확인해 주세요. [kb:B-P01@0.6.1]

### 근거 및 이유
선택 안내는 SPF, 광범위 보호, 내수성을 별도로 다루며 내수성 시간은 SPF 수치가 아니에요. [ref:S16]

### 확인이 필요한 한계
표시를 못 본 것은 기준에 못 미친다는 뜻이 아니에요.

## syn-sol-0142

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f1cfd614b988860d81c7d5ef5ab69840ea88dd633653916ab7662dddf8e30860`
- 사람 검수: **미검수**

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
        "planned_outdoor_activity": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.spf": {
      "variable_id": "product.spf",
      "state": "known",
      "value": {
        "translation_a": 30,
        "translation_b": 50,
        "current_version_confirmed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "서로 다른 번역본의 SPF가 충돌하고 현재 제품 버전과 연결되지 않아 값을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Sunscreen selection guidance discusses SPF and broad-spectrum protection. Product-specific facts must be checked against the relevant label.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외용 후보의 두 번역본에 SPF 30과 50이 적혀 있지만 현재 버전과 연결되지 않아 어느 쪽도 해당 제품 값으로 확정할 수 없어요. [kb:B-P01@0.6.1]

### 근거 및 이유
서로 다른 수치의 출처를 현재 제품 버전과 대조해야 해요.

### 확인이 필요한 한계
현재 버전의 확인된 표시가 없으므로 SPF는 미상이에요.

## syn-sol-0143

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1d870e4d0025df59ff1bb80aa3193ac6f76c11c5e6ed60d28ba36371eea33bc4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "intends_to_reapply": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
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
      "guidance": "재도포하지 않을 계획은 보고했지만 실제 야외 노출과 행동은 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 실제 야외 노출과 제품 사용을 함께 살펴요. 계획만으로 실제 행동을 확인할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
야외 활동과 재도포하지 않을 계획은 알려졌지만 실제로 나갔는지와 그때의 행동은 확인되지 않았어요. 이미 재도포를 빠뜨린 것으로 판단하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
재도포의 행동 차이를 살피는 조건은 장시간 야외 노출 등과 재도포 미실시가 확인된 경우예요. 계획만으로 실제 행동을 대신하지 않아요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
실제 활동과 재도포 여부, 물 접촉은 아직 미상이에요.

## syn-sol-0151

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1e00f881fbe8984663cb524645f294ef7f20ae4985bd8b4ad83a4680abec829f`
- 사람 검수: **미검수**

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
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "visible_number": 80,
        "meaning": "미상"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
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
      "guidance": "보이는 숫자 80의 뜻을 알 수 없어 SPF나 내수성 시간으로 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Sunscreen selection guidance discusses SPF, broad-spectrum protection and water resistance. One label feature does not establish another.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외용 후보에서 보이는 숫자 80이 무엇을 뜻하는지 먼저 확인해 주세요. SPF나 내수성 시간으로 단정하지 않고 나머지 표시도 확인한 뒤 비교해요. [kb:B-P01@0.6.1]

### 근거 및 이유
SPF와 광범위 보호, 내수성은 각각 살펴야 하는 항목이에요. [ref:S16]

### 확인이 필요한 한계
현재 숫자의 의미와 SPF 및 광범위 보호 여부는 미상이에요.

## syn-sol-0152

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2b343903ba1a56f13e6070570775d663572bcea2e9545939f14a68f9f541aaa7`
- 사람 검수: **미검수**

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
      "state": "known",
      "value": {
        "website": 50,
        "container_version_match": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "판매 페이지와 현재 용기의 버전이 일치하지 않아 페이지의 SPF를 현재 제품 값으로 채택하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Sunscreen selection guidance discusses SPF, broad-spectrum protection and water resistance. One label feature does not establish another.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
판매 페이지의 SPF 50은 현재 용기와 버전이 일치하지 않아 현재 제품의 수치로 사용할 수 없어요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외 활동용 비교에서는 실제 용기에 해당하는 버전의 표시가 필요해요.

### 확인이 필요한 한계
현재 용기의 SPF와 UVA 정보는 미상이므로 확인 전에는 비교를 확정하지 않아요.

## syn-sol-0153

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e2229ef9d8afa56e16fce70b5e83d7adeea8993ab00a3dc7bafc3c9cc57ea70e`
- 사람 검수: **미검수**

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
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "record_a": "재도포함",
        "record_b": "재도포하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "재도포 기록의 내용이 서로 다르지만 같은 외출의 기록인지는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun protection guidance considers exposure, water, sweat, towel contact and product directions. It does not calculate an individual ultraviolet dose.",
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

### 응답 초안 — 미승인

### 핵심 안내
오래 야외에 있었지만 재도포했다는 기록과 하지 않았다는 기록이 있어 실제 행동은 미상이에요 [kb:B-P03@0.6.1].

### 근거 및 이유
재도포를 살필 때는 지속 노출과 재도포 행동을 함께 비교하며 필요한 관찰이 상충하면 차이를 확정하지 않아요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
두 기록이 같은 외출을 가리키는지부터 확인해야 해요. 서로 다른 외출이라면 그 맥락을 구분해야 해요.

## syn-sol-0154

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ae65ee4bee78d1b1667c044e4d4c248c449c065965196f38b4e35abc488e1a64`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_swimming": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "intended_after_swimming": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "수영과 재도포 계획은 있지만 실제 입수와 재도포는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 노출과 물, 땀, 닦임 및 표시 사용법을 함께 살펴요. 개인이 받은 자외선량은 이 자료로 계산할 수 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
수영과 그 뒤 재도포를 계획하셨군요. 실제로 물에 들어갔는지와 다시 발랐는지는 아직 확인되지 않아 실행 여부를 판단하지 않아요. [kb:B-P03@0.6.1]

### 근거 및 이유
광보호 안내는 노출과 물 접촉, 제품 사용법을 함께 고려해요. [ref:S05]

### 확인이 필요한 한계
계획은 완료된 행동의 증거가 아니며 개인의 자외선 노출량도 알 수 없어요.

## syn-sol-0155

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `527552f6c0696e0b6fb05e01dcb10d2b74b7b772cbba81ddc2bfc1d7f9dc7640`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_change_observed": true,
        "original_appearance_known": false
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
      "card_id": "B-P08",
      "status": "unknown",
      "guidance": "색이 원래 상태와 달라진 것인지 및 사용기한이 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S18",
      "text": "제품의 사용기한과 보관 이력은 따로 확인해야 해요. 겉모습만으로 남은 보호 성능을 계산할 수 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/replace-makeup-sunscreen",
      "locator": "Sunscreen has an expiration date 및 품질 변화 예시",
      "checked_on": "2026-11-04",
      "limitations": "사용기한·열·품질 변화 관리에 참고. 한국 전제품에 미국의 기한 규칙을 자동 적용하지 않고 정확한 SPF 감소율을 추정하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1",
    "ref:S18"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
색 변화가 관찰됐다고 보고됐지만 원래 모습은 알려져 있지 않아 변화 여부를 독립적으로 비교하기 어려워요. 사용기한도 미상이에요. [kb:B-P08@0.6.1]

### 근거 및 이유
사용기한과 보관 상태는 각각 확인할 정보예요. [ref:S18]

### 확인이 필요한 한계
색 변화 보고와 원래 모습 미확인을 함께 남겨요. 겉모습만으로 남은 보호 성능이나 변질을 확정하지 않아요.

## syn-sol-0174

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f5d53c753d6ad0d4da89bfe90df82378c2914dd8ca0f0d7230d2aaf6b73f5ea7`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "가": "처방 레티노이드",
        "나": "살리실릭애씨드 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "변경 지시": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "같은 날 사용": true,
        "접촉 부위": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "같은 날이라는 정보만으로 같은 부위 병용을 확정하지 않고 처방은 자동 변경하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S34",
      "text": "The labeling for a specific tretinoin medicine describes possible increased local irritation with salicylic-acid and other over-the-counter acne products. The caution is specific to the medicine and use context. It does not authorize stopping a prescription or changing its dose.",
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

### 응답 초안 — 미승인

### 핵심 안내
두 제품을 같은 날 썼어도 같은 부위에 사용했는지는 미상이에요. [kb:B-G14@0.6.1]

### 근거 및 이유
같은 날이라는 사실만으로 같은 부위 병용을 확정하지 않아요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
처방을 임의로 변경하지 않고 필요하면 사용 부위와 의료진 지시를 확인해요.

## syn-sol-0175

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `be81d5e434a1c79443e514f3cc036773c13de911063821e1a222194bd6176104`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "현행 제품": "합성 세럼 나",
        "자료": "구버전의 기능 표시"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "구버전": "AHA 각질관리",
        "현행 버전": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": "현행 제품 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "구버전 역할을 현행 제품의 확인된 역할로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about additional exfoliation while using retinol or prescription retinoids. Product purpose and application context matter. It does not establish a universal prohibition for every ingredient combination or an individual risk probability.",
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

### 응답 초안 — 미승인

### 핵심 안내
구버전의 AHA 관리 역할을 현행 제품에 자동 적용하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 기능 표시는 이전 판의 정보예요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
현행 버전의 관리 역할과 표시를 확인하기 전에는 병용 판정을 보류해요.

## syn-sol-0176

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c61fd39feb4c1f2039b65fb7235242e392d75f999e1b17505e8792c9246d83c7`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "10분 후 제거"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "실제": "팩 사용은 확인",
        "제거 시각": "기억하지 못함"
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
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "확인된 표시만으로 실제 접촉시간 초과를 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S26",
      "text": "Facial-mask guidance advises following each product's directions for contact time and frequency and checking for overlap with existing exfoliating care. It does not prescribe one duration for every mask or authorize mixing arbitrary products.",
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

### 응답 초안 — 미승인

### 핵심 안내
팩의 표시 시간은 10분이지만 실제 제거 시각은 기억하지 못해요. 따라서 시간을 넘겼는지는 판단하지 않아요. [kb:B-G05@0.6.1]

### 근거 및 이유
일반적으로 제품별 접촉 시간 지침을 확인하는 것이 중요해요. [ref:S26]

### 확인이 필요한 한계
기억하지 못하는 시간을 추정하지 않아요.

## syn-sol-0177

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ab7ef4298fb80eb3d29a8749935645bc993fa9694611cd7d6ad42f18e65d46eb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "동일 합성 세럼",
        "용기": "스포이드 교체"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.dispensing_unit_context": {
      "variable_id": "product.dispensing_unit_context",
      "state": "known",
      "value": {
        "이전 용기 측정": "있음",
        "교체 용기 측정": "없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "실제": "교체 용기 세 방울"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "이전 용기의 측정값을 교체된 용기에 자동 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 스포이드의 측정값을 교체한 용기의 세 방울에 그대로 적용하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
용기가 바뀌면 기존 토출량이 현재 용기에도 적용되는지 별도 확인이 필요해요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
교체 용기의 방울 질량은 미상이므로 정량을 계산하지 않아요.

## syn-sol-0178

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `92c046e77574980f58f0def59787c8484e566de48deb64426ad47070bc6d2f66`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "확인": "습식 수동 날면도"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.preparation": {
      "variable_id": "shaving.preparation",
      "state": "known",
      "value": {
        "계획": "다음 면도에 젤을 사용",
        "이번 실제 준비": "미상"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "젤": "습식 면도에 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G09",
      "status": "unknown",
      "guidance": "미래 계획은 이번 면도에서의 준비를 확인해 주지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Wet-shaving guidance discusses preparation, rinsing blades and dry storage, with a reference number of uses for manual blade replacement. The manual-blade reference is not an electric-head replacement interval.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G09@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
다음 면도의 젤 사용 계획은 이번 면도의 실제 준비를 알려주지 않아요. [kb:B-G09@0.6.1]

### 근거 및 이유
계획과 실제 행동을 구분해요. [kb:B-G09@0.6.1]

### 확인이 필요한 한계
이번 준비가 미상이므로 표시 위반이나 적절한 준비를 어느 쪽으로도 확정하지 않아요.

## syn-sol-0179

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `40907dcdc31f1f41de97a587fd49351e47b9c32b61fcd839fe88c3596d572d73`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "표시 목적": "각질관리",
        "성분표": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "현행 목록": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "사용": "저녁에 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "관리 목적만으로 특정 성분의 존재나 농도를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about additional exfoliation while using retinol or prescription retinoids. Product purpose and application context matter. It does not establish a universal prohibition for every ingredient combination or an individual risk probability.",
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

### 응답 초안 — 미승인

### 핵심 안내
각질관리 목적 표시만으로 특정 성분이 있다고 단정하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
제품의 관리 목적과 실제 성분 목록은 서로 다른 정보예요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
현행 성분표와 농도는 미상이며 이름이나 양을 추측하지 않아요.

## syn-sol-0180

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4ddeb94c2b86e6632e0c2b4be2261d2289237f693d863be4151a2ddc456add36`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "문구": "저녁 관리 조정",
        "대상 제품": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "가": "처방 레티노이드",
        "나": "살리실릭애씨드 관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "동일 부위 실제 중첩": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "대상 불명의 진료 지시를 새 제품에 적용하거나 처방을 임의 변경하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S34",
      "text": "The labeling for a specific tretinoin medicine describes possible increased local irritation with salicylic-acid and other over-the-counter acne products. The caution is specific to the medicine and use context. It does not authorize stopping a prescription or changing its dose.",
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

### 응답 초안 — 미승인

### 핵심 안내
진료 지시의 대상 제품과 같은 부위에서 실제로 중첩했는지는 확인되지 않았어요. 지시를 두 제품 중 하나에 임의 적용하지 않아요. [kb:B-G14@0.6.1]

### 근거 및 이유
특정 트레티노인 의약품 표시에는 살리실릭애씨드와 병용 시 주의가 안내돼요. [ref:S34] 이 자료만으로 해당 처방이 그 의약품이라고 확인할 수는 없어요.

### 확인이 필요한 한계
지시의 대상과 사용 부위를 확인하고 처방은 임의로 변경하지 않아요.

## syn-sol-0181

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `62ca4ff9c22c8db1f4e202ea271de146b23c2bed99bf1416e52448613212ea8f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "현재": "새로 구입한 합성 팩",
        "이전": "같은 이름의 예전 용기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "이전 용기": "저녁 사용 허용",
        "현재 용기": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "현재 용기": "아직 사용하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "동일 상품명만으로 현재 용기의 표시와 실제 사용을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S26",
      "text": "얼굴 팩은 제품별 접촉시간과 사용 빈도 안내를 따르도록 설명해요. 비슷한 각질 관리의 중복은 자극을 늘릴 수 있어 사용 맥락을 함께 살펴요. 모든 팩에 같은 시간이나 빈도를 적용한다는 뜻은 아니에요.",
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

### 응답 초안 — 미승인

### 핵심 안내
예전 용기의 밤 사용 허용을 새 용기의 지시로 자동 옮기지 않아요. [kb:B-G05@0.6.1]

### 근거 및 이유
같은 상품명만으로 현재 용기의 표시가 확인된 것은 아니에요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
새 용기는 아직 사용하지 않았고 현행 표시가 미상이므로 이를 확인해요.

## syn-sol-0182

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `915836a08106ea3f99de0e00fe47a687834f906310e69cdedcfef7ab809190ab`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "introduction.local_trial": {
      "variable_id": "introduction.local_trial",
      "state": "known",
      "value": {
        "얼굴 일부": "합성 신제품의 국소 확인 후 불편 없음",
        "목 사용": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "대상": "얼굴과 목"
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
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "현재 보고된 불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "한 부위의 관찰을 다른 부위의 실제 사용 또는 무반응으로 확장하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "새 피부관리 제품을 작은 부위에서 확인하고 7~10일 관찰하는 일반 안내예요. 제품별 용법을 우선하며 모든 제품에 같은 빈도나 접촉시간을 적용하지 않아요. 이런 사용 확인은 의료기관의 진단용 패치테스트나 영구적인 안전 보증이 아니에요.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴 일부의 확인 결과를 목의 사용 결과로 확장하지 않아요. 목 사용과 반응은 미상이에요. [kb:B-G11@0.6.1]

### 근거 및 이유
국소 확인은 영구적인 안전을 보장하지 않아요. [ref:S35]

### 확인이 필요한 한계
얼굴의 결과가 전체 무반응이나 알레르기 검사 결과는 아니에요.

## syn-sol-0132

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0a79e64286f6ccf96d5b18feb10f3870617f040c39b899a309d525af2d58cf0e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "followed_dilution_instructions": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": {
        "water_added_to_original_product": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "dilution_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "exception",
      "guidance": "확인된 제품별 희석 지시와 원제품에 임의로 물을 넣는 행동을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    },
    {
      "evidence_ref": "ref:S11",
      "text": "손이 한 번 닿으면 화장품은 정확히 사흘 뒤에 감염을 일으켜요. 스트레스 관리만 하면 그 기간이 두 배로 늘어요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/11511309/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "급성 실험과 테이프 스트리핑 후 회복 지표. 만성 스트레스 점수로 개인 발진의 원인을 확정할 수 없음. 연구별 군/프로토콜을 분리."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": [
    "ref:S11"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품별로 확인된 희석 지시와 원제품에 임의로 물을 넣는 행동을 구분해요. [kb:B-S03@0.6.1]

### 근거 및 이유
이 사례에서는 희석 지시를 따랐다는 관찰이 있어요.

### 확인이 필요한 한계
다른 제품에도 같은 희석이 허용된다고 추정할 수 없어요.

## syn-sol-0133

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `568a25b1e55a57d333bff02db26b38b079bd4e05eddabc1e4b62dbabb187c274`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.frequency": {
      "variable_id": "dose.frequency",
      "state": "known",
      "value": {
        "cleanser_events": 2
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
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_repeat": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "one_event_after_sweating": true,
        "extra_step_reason_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "운동 후 세안 필요와 그 세안에서 추가 단계가 필요한지는 별도로 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "미온수와 손가락을 이용해 부드럽게 세안하고 강한 마찰을 피하는 일반 관리 원칙이에요. 특정 온도나 세안 시간의 절대 기준을 뜻하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S15",
      "text": "물만 닿아도 세정제 한 단계와 같아요. 모든 사람은 그날 남은 세정을 생략해야 향료 알레르기를 피할 수 있어요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S15"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
땀을 흘린 뒤 세안한 이유와 추가 단계의 필요성은 따로 살펴요. [kb:B-C05@0.6.1]

### 근거 및 이유
활동 후 세안 목적이 있어도 추가 단계의 목적까지 자동으로 확인되는 것은 아니에요.

### 확인이 필요한 한계
추가 단계가 필요한지 현재 정보만으로 확정하지 않아요.

## syn-sol-0134

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b26d7d7b614577c7c46fb8306d4cfae8be90b430ce680702d89749f406420c42`
- 사람 검수: **미검수**

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
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.stinging": {
      "variable_id": "skin.stinging",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "heavy_feel": true,
        "dryness_return_reported": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_available": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "무거운 느낌과 건조 재발 보고는 있지만 보습제 보유만으로 실제 사용과 두 관찰의 시간 관계는 확인되지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/dry/dermatologists-tips-relieve-dry-skin",
      "locator": "보습 시점, 건조 피부 관리, 상담 조건",
      "checked_on": "2026-11-04",
      "limitations": "건조 피부 관리의 일반 권고. 모든 피부타입·모든 제형에 동일한 양을 정하지 않음."
    },
    {
      "evidence_ref": "ref:S12",
      "text": "32명 규모의 식이 연구 결과를 모든 보습제 사용자에게 적용해요. 보습량을 늘리면 이 사람의 건조가 90퍼센트 치료돼요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.medicaljournals.se/acta/content/abstract/10.2340/00015555-1346",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "특정 질환·식이패턴·기간의 소규모 연구. 한 번의 음식 섭취와 다음날 증상을 연결하거나 모든 피부 건조·민감 반응에 확장하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M02@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": [
    "ref:S12"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
무거운 느낌과 건조 재발 보고를 각각 기록해요. [kb:B-M02@0.6.1]

### 근거 및 이유
보습제 보유만으로 실제 사용이나 두 관찰의 시간 관계를 알 수 없어요.

### 확인이 필요한 한계
사용 후 불편이나 보습 방법의 차이는 현재 정보로 확정하지 않아요.

## syn-sol-0135

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `295228575fe00b8b5d899c37b446fcbece42bf78fffb83503c045e6379815cbd`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.ph": {
      "variable_id": "product.ph",
      "state": "known",
      "value": {
        "candidate_mildly_acidic": true
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "existing_cleanser_tolerated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "exception",
      "guidance": "약산성 후보라는 정보만으로 기존에 잘 쓰는 제품의 교체 실익이 확정되지는 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S07",
      "text": "특정 세정제의 반복 전완 세정시험에서 pH와 조성의 상호작용을 살핀 자료예요. pH만으로 완제품의 순함이나 모든 제품의 우열을 정하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/full/10.1111/ics.12721",
      "locator": "Methods / Results / Discussion",
      "checked_on": "2026-11-04",
      "limitations": "시험 제형·전완·강화된 세정 조건에 제한. 중성·약알칼리 제품의 일반적 우월성이나 모든 음이온 계면활성제의 서열을 뜻하지 않음. 산업체 소속/지원 맥락을 보존."
    },
    {
      "evidence_ref": "ref:S12",
      "text": "모든 알칼리성 세정제는 사용자 반응과 무관하게 즉시 버려야 해요. 저혈당 식단 연구를 따르면 약산성 제품만 항상 안전해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.medicaljournals.se/acta/content/abstract/10.2340/00015555-1346",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "특정 질환·식이패턴·기간의 소규모 연구. 한 번의 음식 섭취와 다음날 증상을 연결하거나 모든 피부 건조·민감 반응에 확장하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1",
    "ref:S07"
  ],
  "distractor_refs": [
    "ref:S12"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
약산성 후보라는 이유만으로 기존 제품의 교체를 확정하지 않아요. [kb:B-C04@0.6.1]

### 근거 및 이유
현재 제품을 잘 견디는 경험과 새 후보의 특성은 서로 다른 정보예요.

### 확인이 필요한 한계
약산성만으로 제품의 순함이나 개인 적합성을 보증하지 않아요.

## syn-sol-0136

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `449dedbbbaad323fbeacdc21ca896deafb6771626e468276ab7e79398d007c0a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "separate_hydration_occlusion_barrier_products_required": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "comfortable": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "difference",
      "guidance": "보습 기능을 무조건 각각 별도 제품으로 채울 필요는 없으며 현재 충족 상태를 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S04",
      "text": "건조 피부 관리에서 세정 후 보습 시점과 사용 경험을 검토하는 일반 안내예요. 모든 피부와 제품에 동일한 사용량을 정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
보습 기능을 각각 반드시 별도 제품으로 채울 필요는 없어요. [kb:B-M03@0.6.1]

### 근거 및 이유
현재 보습에 편안하다는 관찰을 먼저 살펴요.

### 확인이 필요한 한계
이 판단은 모든 사람에게 같은 제품 구성을 보장하지 않아요.

## syn-sol-0137

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `018ca8bb4e803ae321887bd3a63de7d65dd5970ce8589d921c1920f809aa29cf`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "hand.protection_hygiene": {
      "variable_id": "hand.protection_hygiene",
      "state": "known",
      "value": {
        "required_hygiene_maintained": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "discomfort": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "after_washing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "fragrance_free": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "aligned",
      "guidance": "향료 표시만으로 현재 본인의 반응을 확정하지 않고 필수 위생과 사용 경험을 함께 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 보습하고 무향료 손 크림이나 연고를 선택하는 범위의 안내예요. 필요한 손 위생을 줄이거나 모든 개인의 적합성을 보장하는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
필수 손 위생과 현재의 보습 경험을 함께 살펴요. [kb:B-M04@0.6.1]

### 근거 및 이유
향료 표시 여부와 개인이 실제로 느낀 반응은 구분해요.

### 확인이 필요한 한계
현재 불편이 없다는 관찰만으로 앞으로의 모든 반응을 보증할 수 없어요.

## syn-sol-0138

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `295c1c1aeee24413166935634e3fb4501b3183e73ddbdc8804e0b43defc83258`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "shared_noncontact_pump": true,
        "shared_skin_contact_tool": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "difference",
      "guidance": "펌프의 비접촉 공유와 피부에 직접 닿는 도구 공유를 구분해 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S07@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
비접촉 펌프 공유와 피부에 직접 닿는 도구 공유를 구분해 검토해요. [kb:B-S07@0.6.1]

### 근거 및 이유
두 경우는 실제 접촉 경로가 달라 같은 취급으로 보지 않아요.

### 확인이 필요한 한계
공유 사실만으로 감염이나 개인의 위해를 확정하지 않아요.

## syn-sol-0139

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4cb8d4946aa8276b7fe1417dd54bd452e4a7521916f8992015ae7fda116f5580`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.water_ingress": {
      "variable_id": "storage.water_ingress",
      "state": "known",
      "value": {
        "water_added_to_original_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "water_added_without_instructions": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": false,
        "separation": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "difference",
      "guidance": "외관이 같다는 관찰은 임의 물 혼입 취급이나 현재 품질을 보증하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S27",
      "text": "화장품에 물이나 침을 넣지 않고 손과 용기를 깨끗하게 관리하며 표시 보관조건을 따르는 안내예요. 한 번의 접촉만으로 오염이나 감염을 확정하거나 폐기일까지 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/microbiological-safety-and-cosmetics",
      "locator": "제품에 물/침 첨가를 피하고 손·용기를 깨끗하게 관리하며 표시 보관조건 준수.",
      "checked_on": "2026-11-04",
      "limitations": "단일 접촉 후 오염 확정, 물기=3일 후 폐기 등의 수치를 제공하지 않는다."
    },
    {
      "evidence_ref": "ref:S11",
      "text": "손이 한 번 닿으면 화장품은 정확히 사흘 뒤에 감염을 일으켜요. 스트레스 관리만 하면 그 기간이 두 배로 늘어요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/11511309/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "급성 실험과 테이프 스트리핑 후 회복 지표. 만성 스트레스 점수로 개인 발진의 원인을 확정할 수 없음. 연구별 군/프로토콜을 분리."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1",
    "ref:S27"
  ],
  "distractor_refs": [
    "ref:S11"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
외관이 같아도 원제품에 지침 없이 물을 넣은 취급을 별도로 검토해요. [kb:B-S03@0.6.1]

### 근거 및 이유
색이나 냄새 변화가 없다는 관찰은 현재 품질 전체를 보증하지 않아요.

### 확인이 필요한 한계
물 혼입이나 외관만으로 오염 여부를 확정할 수 없어요.

## syn-sol-0156

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5302a86645b8b7317eceb29114d6771b98cd0744a2e4b53c07b6a880908daf00`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_on_face": true,
        "used_near_eyes": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "얼굴 사용 경험만으로 눈 주변에서 반복 눈시림이 없는지 확정할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변 자외선차단과 제품 사용 상황을 다루는 안내예요. 특정 개인의 불편 원인을 확정하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴에는 사용했지만 눈 가까이는 사용하지 않았어요. 이를 눈 주변의 반복적인 눈시림이 없었다는 증거로 삼을 수 없어요 [kb:B-P06@0.6.1].

### 근거 및 이유
눈 주변 사용을 검토할 때는 같은 제품·방식에서 반복 눈시림이 있거나 회피로 눈 주변 보호가 빠지는 상황을 살펴요 [kb:B-P06@0.6.1]. 제공된 눈 주변 안내는 제품 선택과 사용 상황에 관한 일반 자료예요 [ref:S17].

### 확인이 필요한 한계
눈시림 경험 자체는 미상이고 개인의 반응이나 원인을 예측할 수 없어요.

## syn-sol-0157

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ba2b6ec3ea265f20788cc7d9e981058aa26189362a7bce75e8860860e7774a4e`
- 사람 검수: **미검수**

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
        "sunscreen_use_reduced_due_to_layering": null,
        "reapplication_omitted_due_to_layering": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "밀림은 관찰됐지만 그 때문에 실제 사용이나 재도포가 줄었는지 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "제한된 제품 중첩을 영상으로 관찰한 연구예요. 실제 야외 보호 성능이나 개인별 결과를 보증하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/phpp.12745",
      "locator": "Methods 2.4 / Results / Discussion",
      "checked_on": "2026-11-04",
      "limitations": "실험실 조건 및 영상 대리지표. 유의한 차이가 없다는 결과는 모든 조합의 동등성 입증이 아니며, 실제 SPF나 야외 성능의 보증도 아님. 손바닥 사전 혼합과 개별 층 도포는 다름."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1",
    "ref:S09"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품이 밀리는 현상은 있었지만 그 때문에 선크림 사용이나 재도포를 줄였는지는 아직 몰라요. 실제 사용에 불편이 있었는지 확인해 보세요. [kb:B-I02@0.6.1]

### 근거 및 이유
밀림만으로 사용 행동이 달라졌다고 볼 수 없어요. 제한된 제품 중첩을 영상으로 관찰한 연구도 개인의 야외 보호 결과를 보장하지 않아요. [ref:S09]

### 확인이 필요한 한계
사용량과 재도포 변화는 확인되지 않았어요.

## syn-sol-0158

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `43e460499760379ab67159b67a650481d133eb3c3b56c6b0f29dd63dae250bc2`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "compare_new_outdoor_sunscreen",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.spf": {
      "variable_id": "product.spf",
      "state": "known",
      "value": {
        "other_version": 50,
        "matches_current_version": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "broad_spectrum_uva_uvb": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "광범위 보호와 내수성 표시의 버전 연결은 미상이고 다른 버전의 SPF를 현재 제품 값으로 옮길 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "자외선차단제 선택 안내는 SPF와 광범위 보호, 내수성 표시를 살펴요. 표시 항목 하나만으로 다른 항목을 확정할 수 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
광범위 보호와 내수성 표시가 보고됐지만 그 표시가 현재 버전에 해당하는지는 미상이에요. 다른 버전의 SPF를 현재 제품 값으로 옮길 수도 없어요. [kb:B-P01@0.6.1]

### 근거 및 이유
각 표시와 제품 버전의 연결을 확인해야 현재 후보의 기본 성능을 판단할 수 있어요. [kb:B-P01@0.6.1]

### 확인이 필요한 한계
현재 버전의 SPF와 다른 두 표시의 버전 연결은 확인되지 않았어요.

## syn-sol-0159

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cab1d20f8d1df90401067cfb417d9c0aca353e0015f19b801063a07d7811c8f1`
- 사람 검수: **미검수**

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
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "family_member_reapplied": true,
        "own_reapplication": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "가족의 행동은 확인됐지만 본인의 재도포는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 노출과 물, 땀, 닦임 및 표시 사용법을 함께 살펴요. 개인이 받은 자외선량은 이 자료로 계산할 수 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
긴 야외 활동에서 가족이 재도포한 기록은 있지만 본인이 재도포했는지는 미상이에요. [kb:B-P03@0.6.1]

### 근거 및 이유
일반 안내에서는 야외 노출과 물·땀 상황 및 제품 지침을 살펴요. [ref:S05]

### 확인이 필요한 한계
가족의 행동을 본인의 행동으로 옮기거나 개인 보호율을 계산하지 않아요.

## syn-sol-0161

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `88e8089e0aff4e9392e187b4444c0c412fd080301fe30ee1251c7cc1cd531a75`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "repeated_with_same_product": true
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
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "stopped_near_eye_use": true,
        "alternative_eye_protection": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "해당 제품은 눈가 사용 제한이 있고 사용도 중단했지만 대체 보호 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "눈 주변 사용을 살펴보는 자외선차단 안내예요. 개인의 불편 원인은 이 안내만으로 확정할 수 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
같은 제품에서 눈시림이 반복됐고, 눈가 사용 제한이 있는 해당 제품의 눈가 사용을 중단했다고 보고했어요. 대체 광보호 여부는 미상이에요. [kb:B-P06@0.6.1]

### 근거 및 이유
제품의 눈가 사용 제한과 실제 사용 조정, 대체 보호 여부를 구분해 살펴요. [kb:B-P06@0.6.1]

### 확인이 필요한 한계
눈시림의 원인과 대체 광보호의 확보 여부는 확정하지 않아요.

## syn-sol-0162

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4888f477ee58c710a1ca39732c4c1c798ffddf09ec339c3dceb48debe23082ae`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "label_expired": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "known",
      "value": {
        "color_or_odor_change": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "currently_stored_indoors": true,
        "past_hot_car_storage": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "unknown",
      "guidance": "현재 실내 보관 사실만으로 과거 열 노출 여부를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S18",
      "text": "제품의 사용기한과 보관 이력은 따로 확인해야 해요. 겉모습만으로 남은 보호 성능을 계산할 수 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/replace-makeup-sunscreen",
      "locator": "Sunscreen has an expiration date 및 품질 변화 예시",
      "checked_on": "2026-11-04",
      "limitations": "사용기한·열·품질 변화 관리에 참고. 한국 전제품에 미국의 기한 규칙을 자동 적용하지 않고 정확한 SPF 감소율을 추정하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1",
    "ref:S18"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재는 실내에 있고 표시 기한 경과나 색·냄새 변화는 보고되지 않았어요. 다만 과거 뜨거운 차 안에 두었는지는 미상이에요 [kb:B-P08@0.6.1].

### 근거 및 이유
보관과 품질을 살필 때는 기한 경과나 정상과 다른 품질 변화가 확인된 경우를 다루며 오래 보유했다는 사실만으로 성능 소실을 확정하지 않아요 [kb:B-P08@0.6.1]. 제공된 자료에서도 기한과 보관을 함께 고려해요 [ref:S18].

### 확인이 필요한 한계
이전 열 노출을 기억하는 범위에서 확인할 수 있지만 겉모습이나 보관 이력만으로 남은 보호 성능을 계산할 수 없어요.

## syn-sol-0163

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a20a65bd77e331a21be1858212faf81a0abf6887ae2c1e7e02148e48111b6fbc`
- 사람 검수: **미검수**

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
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "new_product_purchase_planned": true,
        "reapplied": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "제품 구매 계획은 실제 재도포 행동을 확인해 주지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 노출과 물, 땀, 닦임 및 표시 사용법을 함께 살펴요. 개인이 받은 자외선량은 이 자료로 계산할 수 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
오래 야외에 머문 상황에서 새 제품 구매 계획은 확인되지만, 실제 재도포 여부는 알 수 없어요. 당시 사용을 확인한 뒤 야외 일정과 제품 지침에 맞는 시점을 살펴봐요. [kb:B-P03@0.6.1]

### 근거 및 이유
광보호 안내는 지속 노출과 제품 사용법을 함께 고려해요. [ref:S05]

### 확인이 필요한 한계
구매 계획만으로 다시 발랐거나 바르지 않았다고 결론낼 수 없어요.

## syn-sol-0164

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `37d0060b614aaec3e23c1e5e61633b1a4391ed9655f5a01c9f016440a6a6afb9`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face",
        "ears"
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
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "friend_omits_ears": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "친구가 귀를 빼고 바른 사실은 확인되지만 본인의 노출 부위 누락 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단 안내는 제품 지침과 노출 상황을 함께 살펴요. 개인의 실제 자외선량이나 보호율을 이 자료로 계산하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴과 귀가 노출됐지만 친구가 귀를 빼고 바른 사실로 본인의 도포 누락을 판단할 수 없어요. [kb:B-P02@0.6.1]

### 근거 및 이유
친구와 본인의 사용 기록은 구분해요.

### 확인이 필요한 한계
본인의 귀 도포 여부는 미상이에요.

## syn-sol-0165

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `154d39a824780747e189a031121c4a89b17a29f15824c8f597de6183a3435a97`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "friend_reported": true,
        "own_experience": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "own_sunscreen_use_reduced": null
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "친구의 경험으로 본인의 밀림이나 실제 사용 감소를 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "제한된 제품 중첩을 영상으로 관찰한 연구예요. 실제 야외 보호 성능이나 개인별 결과를 보증하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/phpp.12745",
      "locator": "Methods 2.4 / Results / Discussion",
      "checked_on": "2026-11-04",
      "limitations": "실험실 조건 및 영상 대리지표. 유의한 차이가 없다는 결과는 모든 조합의 동등성 입증이 아니며, 실제 SPF나 야외 성능의 보증도 아님. 손바닥 사전 혼합과 개별 층 도포는 다름."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I02@0.6.1",
    "ref:S09"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
밀림을 경험한 사람은 친구예요. 본인에게도 밀림이 있거나 그 때문에 선크림을 줄였다고 옮겨 적지 않아요 [kb:B-I02@0.6.1].

### 근거 및 이유
중첩 사용을 살필 때는 중첩의 불편 때문에 본인이 실제 사용이나 재도포를 줄였는지 살펴요 [kb:B-I02@0.6.1]. 제공된 중첩 연구는 제한된 제품 조합의 영상 관찰이에요 [ref:S09].

### 확인이 필요한 한계
본인의 밀림 경험과 사용 변화는 미상이며 연구 결과가 개인의 보호 성능을 보증하지 않아요.

## syn-sol-0183

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `862d6cd139bd8a8be5ed9f58d29e526efe28550d98d911a060e2c3de18ee240c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "향 성분": "Benzyl Salicylate"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.adjunct_functions": {
      "variable_id": "product.adjunct_functions",
      "state": "known",
      "value": {
        "합성 제품": "향을 위한 성분 표기",
        "각질관리 목적": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제": "한 제품 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "이름 일부가 비슷하다는 이유만으로 각질관리 역할이나 중첩을 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "레티놀이나 처방 레티노이드를 쓰는 동안 추가 각질관리를 겹치는 상황과 과도한 각질관리 회피를 다루는 안내예요. 실제 관리 목적과 사용 부위를 구분해 검토해야 해요. 모든 성분 조합의 절대 금기나 개인의 위해확률을 정하는 자료는 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
Benzyl Salicylate라는 이름만으로 이 제품을 각질관리 제품으로 판정하지 않아요. [kb:B-G15@0.6.1]

### 근거 및 이유
성분명 일부가 비슷한 것과 확인된 관리 목적은 달라요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
각질관리 목적이 확인되지 않아 다른 관리와의 중첩도 확정하지 않아요.

## syn-sol-0184

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `718f86f2590f9458b33067a520b4e9923d318b22252d7bf3cdfeefd775ed4ea5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.medication_status": {
      "variable_id": "product.medication_status",
      "state": "known",
      "value": {
        "본인 처방": "보고되지 않음",
        "동거인": "처방 레티노이드 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "본인": "살리실릭애씨드 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "본인": "저녁 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "타인의 처방을 본인의 실제 병용으로 취급하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S34",
      "text": "특정 트레티노인 의약품 표시에서 살리실릭애씨드 등 일반의약품 병용 시 국소 자극 증가 가능성을 다뤄요. 실제 제품 유형과 병용 맥락을 구분해야 해요. 이 주의만으로 처방을 중단하거나 용량을 바꾸는 절차를 만들지는 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
동거인의 처방을 본인의 처방 사용으로 기록하지 않아요. [kb:B-G14@0.6.1]

### 근거 및 이유
동거인의 사용과 본인의 실제 관리 제품은 서로 다른 관찰이에요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
본인의 처방 사용은 보고되지 않았으며 두 제품의 본인 병용을 확정하지 않아요.

## syn-sol-0185

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `49a21a36f148b4c1aec0f6a7be5c67047ed371a12f67b9893aed0a12320d3f9f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "현재 제품": "AHA 각질관리",
        "미개봉 후보": "BHA 각질관리"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "현재": "AHA 사용",
        "후보": "소유만 하고 사용하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "보유 사실을 실제 동시 사용으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "레티놀이나 처방 레티노이드를 쓰는 동안 추가 각질관리를 겹치는 상황과 과도한 각질관리 회피를 다루는 안내예요. 실제 관리 목적과 사용 부위를 구분해 검토해야 해요. 모든 성분 조합의 절대 금기나 개인의 위해확률을 정하는 자료는 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
미개봉 BHA 후보를 현재 AHA 제품과 함께 사용 중이라고 세지 않아요. [kb:B-G15@0.6.1]

### 근거 및 이유
소유와 실제 사용은 다른 상태예요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
후보 사용은 확인되지 않았고 실제 중첩이나 그 결과를 추정하지 않아요.

## syn-sol-0186

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1895d3089ce4a30b9d21ba9d8323ea58bd04e491bfe86c83a1f5452eb3c462ba`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.medication_status": {
      "variable_id": "product.medication_status",
      "state": "known",
      "value": {
        "현재": "처방 레티노이드 사용 중",
        "계획": "스스로 중단을 생각함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "추가 후보": "살리실릭애씨드 각질관리",
        "실제 사용": "아직 시작하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "중단 지시": "확인되지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "중단 계획을 실제 중단이나 의료진 지시로 취급하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S34",
      "text": "특정 트레티노인 의약품 표시에서 살리실릭애씨드 등 일반의약품 병용 시 국소 자극 증가 가능성을 다뤄요. 실제 제품 유형과 병용 맥락을 구분해야 해요. 이 주의만으로 처방을 중단하거나 용량을 바꾸는 절차를 만들지는 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
처방 중단을 생각하는 것과 실제 중단이나 의료진 지시는 달라요. [kb:B-G14@0.6.1]

### 근거 및 이유
처방 제품은 현재 사용 중이고 추가 후보는 아직 시작하지 않았어요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
처방은 임의로 변경하지 않으며 의료진 지시가 필요한 사항은 별도로 확인해요.

## syn-sol-0187

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `e5b98490bd89e928bedb3c21cfce3fd9443250edb1b333a3533d854583a6a169`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "본인": "합성 팩을 표시 시간에 사용",
        "동거인": "다른 제품 사용 중 따가움"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "본인 팩": "10분 후 제거"
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
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "본인 불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "동거인의 다른 제품 반응을 본인의 반응으로 옮기지 않아요. 전체 비교에 필요한 중복 또는 사용 기간 정보는 미상이므로 전체 정렬 여부는 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S26",
      "text": "얼굴 팩은 제품별 접촉시간과 사용 빈도 안내를 따르도록 설명해요. 비슷한 각질 관리의 중복은 자극을 늘릴 수 있어 사용 맥락을 함께 살펴요. 모든 팩에 같은 시간이나 빈도를 적용한다는 뜻은 아니에요.",
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

### 응답 초안 — 미승인

### 핵심 안내
동거인의 다른 제품 반응을 본인의 팩 반응으로 옮기지 않아요. [kb:B-G05@0.6.1]

### 근거 및 이유
본인의 팩 사용은 표시 시간과 일치하지만 유사 관리 중복 여부는 확인되지 않았어요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
전체 정렬 여부는 미상이고 현재 불편이 없다는 보고는 앞으로의 무반응을 보증하지 않아요.

## syn-sol-0188

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `342153d26de38e3783ff12fd38782b533e5e15a03ed8709fa9b4711006aec4c4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.dispensing_unit_context": {
      "variable_id": "product.dispensing_unit_context",
      "state": "known",
      "value": {
        "현재": "원래 스포이드",
        "계획": "다음 달 새 스포이드 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "현재 기록": "원래 용기 두 방울",
        "새 용기 토출량": "미상"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "대상": "같은 합성 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "계획된 교체를 이미 발생한 토출량 변화로 다루지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
다음 달의 스포이드 교체를 이미 일어난 사용량 변화로 계산하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
현재의 두 방울 기록은 기존 용기의 기록이에요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
새 용기의 토출량은 미상이고 같은 질량으로 환산할 수 없어요.

## syn-sol-0189

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a2b4bc49a3e0f7dc571f518df06bfafb161ad5c9a5d5e00133e27e8e3a8eef2f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "가": "레티놀 관리 화장품",
        "나": "본인 사용 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "가": "실제 사용",
        "나": "사용 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "각 제품의 유형": {
          "가": "일반 화장품",
          "나": "이름이 비슷한 처방 의약품"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "비슷한 상품명은 처방 상태나 두 제품의 실제 병용을 입증하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S33",
      "text": "특정 아다팔렌 0.3% 의약품의 환자 안내에서 AHA와 글리콜릭애씨드 제품 회피를 다뤄요. 이 주의는 해당 의약품 표시의 범위에서 읽어야 해요. 한국의 모든 레티노이드 화장품에 같은 법적 금기가 있다는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=c448eab6-c054-4c8b-9319-556b7e1be3cf",
      "locator": "17항 및 환자 안내: alpha hydroxy/glycolic acid 제품 회피",
      "checked_on": "2026-11-05",
      "limitations": "특정 미국 아다팔렌 의약품 표시. 한국의 모든 화장품 레티노이드에 동일한 법정 금기가 있다는 뜻은 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S33"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이름이 비슷한 처방 의약품의 사용을 본인의 실제 사용으로 추정하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 실제 사용은 일반 레티놀 화장품이고 다른 제품 사용은 미확인이에요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
상품명 유사성만으로 두 제품의 처방 상태나 병용을 확정하지 않아요.

## syn-sol-0190

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1b561a5a2eb5f7c4d41af4d67cb84e1459dc371f1d9cd51ca3d8cf5c9a3162b8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "가": "10분 후 제거",
        "나": "밤새 사용 가능"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "실제": "나를 표시대로 밤새 사용",
        "가": "사용하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "각 제품의 유형": {
          "가": "씻어내는 팩",
          "나": "남겨두는 수면팩"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "서로 다른 제품의 지시와 실제 사용 대상을 분리해요. 전체 비교에 필요한 중복 또는 사용 기간 정보는 미상이므로 전체 정렬 여부는 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S26",
      "text": "얼굴 팩은 제품별 접촉시간과 사용 빈도 안내를 따르도록 설명해요. 비슷한 각질 관리의 중복은 자극을 늘릴 수 있어 사용 맥락을 함께 살펴요. 모든 팩에 같은 시간이나 빈도를 적용한다는 뜻은 아니에요.",
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

### 응답 초안 — 미승인

### 핵심 안내
사용한 수면팩에는 확인된 해당 제품의 밤 사용 지시를 적용해요. [kb:B-G05@0.6.1]

### 근거 및 이유
사용하지 않은 다른 팩의 제거 지시를 수면팩에 옮기지 않아요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
유사 관리의 다른 중복은 미상이므로 전체 정렬 여부와 개인 안전성을 확정하지 않아요.
