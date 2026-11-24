# PPO-39 보완 — additional_100

`development_preview`, `production_enabled=false`, 합성 개발 후보이며 공식 인수·사람 승인이 아니에요.
원문 관찰을 정형 슬롯과 연결하고 사례별 설명을 보완했어요. 전체 판단과 과거 기록은 README 및 `ppo39_revisions.json`을 확인해요.
KB 판정은 비교 명세에 대한 작성 기록이며 엔진 실행이나 임상 결과가 아니에요. 저장 문헌 청크는 요약이며 외부 원전의 직접 인용이 아니에요.

## syn-sol-0037

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4141e886784de4053492dcaa7ffff932d2a95886cd02b16adf75f4ee2ec0a7ed`
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
        "soft_silicone_pad"
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
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "손가락 이외 도구 사용은 기본 방법과 차이가 있지만 강한 마찰이나 손상은 확인되지 않았어요."
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
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
부드러운 실리콘 패드를 쓰는 점은 손가락 세안이라는 기본 방법과 달라요. 다만 현재 마찰은 부드럽고 물기는 두드려 닦으며 불편감도 없어서, 도구 사용만으로 강한 마찰이나 손상을 판단하지 않아요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반 안내의 기본은 손가락으로 부드럽게 씻는 방법이에요. 이 기본 방법을 검토할 수 있지만, 도구를 쓴다는 사실과 세게 문지른다는 사실은 나눠 봐야 해요 [ref:S03] [kb:B-C02@0.6.1].

### 확인이 필요한 한계
이 기록은 도구의 개별 안전성이나 효과를 검증한 결과가 아니에요. 확인된 차이가 곧 위험이나 변경 필요성을 뜻하지는 않아요.

## syn-sol-0038

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6d24c98a9afc543e7b98fdc4bd1049a6181102d84b53bdac68fec0cd40d2cc8a`
- 사람 검수: **미검수**

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
        "performed": false,
        "reason": "시간 절약"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "씻어내는 세안제로 확인됐는데 헹굼을 생략하므로 해당 제품의 헹굼 지시를 따르도록 안내해요."
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
지금 제품은 헹굼이 필요한 세안제로 확인됐는데 시간을 아끼려고 헹굼을 생략하고 있어요. 해당 제품의 확인된 헹굼 지시를 따르는 방향으로 조정해요 [kb:B-C06@0.6.1].

### 근거 및 이유
씻어내는 제품의 헹굼 생략은 해당 카드의 기본 사용법과 차이가 있어요. 물세안이 필요 없는 제품의 예외를 이 제품에 적용할 근거는 없어요 [kb:B-C06@0.6.1].

### 확인이 필요한 한계
필요한 헹굼 시간이나 물의 양은 입력에 없어서 정하지 않아요. 헹굼을 생략했다는 기록만으로 피부 손상이나 질환을 확정하지 않아요.

## syn-sol-0039

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `63988fd105a8e393f34e623a31894f3a3077db9ce776a12df86cf50d0c28d558`
- 사람 검수: **미검수**

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
        "specific_contact_instruction": true,
        "text": "합성 제품 표시: 표시된 접촉 안내를 따른 뒤 충분히 헹궈요."
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
    "dose.contact_time": {
      "variable_id": "dose.contact_time",
      "state": "known",
      "value": {
        "follows_label": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "exception",
      "guidance": "제품에 별도 접촉시간 지시가 확인돼 일반 세안제의 정성적 기본값을 일괄 적용하지 않아요."
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
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 합성 사례의 제품에는 별도 접촉 안내가 있고, 그 안내를 따르며 부드럽게 사용한다고 확인됐어요. 일반 세안제의 기준만으로 접촉시간을 줄이라고 하지 않고, 확인된 표시의 접촉 안내 뒤 충분히 헹구는 방법을 존중해요 [kb:B-C03@0.6.1].

### 근거 및 이유
제품별 별도 접촉 지시는 일반 기본값을 일괄 적용하지 않는 예외예요. 일반 세안 자료도 특정 온도나 절대적인 시간 제한을 정해 주는 근거는 아니에요 [kb:B-C03@0.6.1] [ref:S03].

### 확인이 필요한 한계
실제 접촉시간의 숫자는 제공되지 않았어요. 시간을 새로 만들거나 이 합성 표시를 다른 세정제에 그대로 적용하지 않아요.

## syn-sol-0040

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `00bcdb5a607053aed64c5f413a976fa31a312b3cb926e4c64ee07028b529f3cd`
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
        "comfortable": true,
        "dryness_return_reported": false
      },
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "aligned",
      "guidance": "확인된 보습 사용으로 건조 불편과 새 불편이 없어 일률적 증량을 만들지 않아요."
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
현재 보습제를 사용하면서 건조와 당김이 없고 편안하며 건조가 다시 나타나지 않는다고 확인됐어요. 지금의 사용을 유지할 수 있고, 일률적으로 양을 늘릴 이유는 확인되지 않았어요 [kb:B-M02@0.6.1].

### 근거 및 이유
보습량은 실제 건조 불편과 사용 경험을 함께 보며 검토해요. 일반 건조 피부 안내도 모든 피부와 제형에 같은 양을 정하지는 않아요 [kb:B-M02@0.6.1] [ref:S04].

### 확인이 필요한 한계
편안하다는 관찰은 개인의 현재 경험이에요. 특정 성분의 효능이나 장기적인 임상 효과가 입증됐다는 뜻은 아니에요.

## syn-sol-0041

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `17d702e5646fea8755a1f0ba1146d01948298843eb4d1dc6b4aa2895744472b2`
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
        "discomfort": false
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
    },
    "skin.hand_observation": {
      "variable_id": "skin.hand_observation",
      "state": "known",
      "value": {
        "dryness": "mild",
        "severe_symptoms": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "aligned",
      "guidance": "필수 손 위생을 유지하면서 잘 견디는 보습제를 쓰고 있어 이 범위를 유지해요."
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
필수 손 위생을 지키면서 손을 씻은 뒤 보습하고, 해당 제품에 불편감도 없다고 했어요. 현재 잘 견디는 보습과 필요한 손 위생을 함께 유지해요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 관리 자료는 손 씻은 뒤 보습과 무향료 크림·연고 선택을 다뤄요. 이 안내가 필요한 손 위생을 줄이라는 뜻은 아니에요 [ref:S21].

### 확인이 필요한 한계
가벼운 건조가 있다는 관찰은 남겨 두어요. 현재 제품을 잘 견딘다는 사실만으로 모든 제품이나 앞으로의 반응까지 보장하지 않아요.

## syn-sol-0042

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `015e24668710c2e15d62df3ccf03e87b86ebd5edfe9dc636345f0357a72166f8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.sharing_refill": {
      "variable_id": "storage.sharing_refill",
      "state": "known",
      "value": {
        "official_refill": true,
        "topped_up_old_product": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "manufacturer_designated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "refill_allowed": true,
        "empty_and_follow_container_care": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "followed_refill_instructions": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "exception",
      "guidance": "제품이 허용한 용기와 비우기·관리 지침을 지킨 공식 리필이므로 모든 리필을 금지하지 않아요."
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
제조사가 지정한 용기를 비우고 관리 지침을 지킨 공식 리필이며, 남은 내용물 위에 덧채우지 않았다고 확인됐어요. 이 경우를 임의 덧채움과 구분하고 모든 리필을 금지하지 않아요 [kb:B-S07@0.6.1].

### 근거 및 이유
해당 카드에는 제품이 허용한 리필과 용기 관리 지침을 함께 검토하는 예외가 있어요. 위생 자료도 깨끗한 손·용기 취급과 표시 보관조건 준수를 다뤄요 [kb:B-S07@0.6.1] [ref:S27].

### 확인이 필요한 한계
지침 준수는 무균이나 품질을 인증하는 결과가 아니에요. 이 제품의 허용을 다른 용기나 비공식 리필까지 확대하지 않아요.

## syn-sol-0043

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ce3c3c5cd2dac7e5619bd34d7cc93367587ad9cef75100b68c8544ad37a67cd5`
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
        "rinse_after_use": true,
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
        "visible_damage": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "care_matches": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S05",
      "status": "aligned",
      "guidance": "수동 면도날을 사용 후 헹구고 건조 보관하며 제품 지침과 일치하는 사실을 유지해요."
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
수동 면도날을 사용 뒤 헹구고 건조 보관하며 제품 지침과도 일치한다고 확인됐어요. 확인된 관리 방법을 유지해요 [kb:B-S05@0.6.1].

### 근거 및 이유
습식 면도 안내는 날 헹굼과 건조 보관을 다뤄요. 지금의 관리는 이 범위와 맞아요 [ref:S23].

### 확인이 필요한 한계
눈에 보이는 손상이 없다는 관찰이 날의 모든 상태를 보증하지는 않아요. 이 정보만으로 교체 날짜를 정하거나 수동 날의 참고를 전기면도기 헤드에 적용하지 않아요.

## syn-sol-0044

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0acb1d428a15b3e97ce3aa691540e150ab1544be9cd35ab05fe447500376e37a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": "manual",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.blade_use_history": {
      "variable_id": "shaving.blade_use_history",
      "state": "known",
      "value": {
        "uses": 2
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.blade_condition": {
      "variable_id": "shaving.blade_condition",
      "state": "known",
      "value": {
        "damaged": true,
        "pulling_hair": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "pain": "none"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S06",
      "status": "unknown",
      "guidance": "수동 날을 두 번 사용했고 손상과 털 당김이 확인됐어요. 이를 무시하고 계속 썼는지는 미상이에요."
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
    "kb:B-S06@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
수동 면도날을 두 번 썼더라도 손상과 털 당김이 확인됐어요. 사용 횟수가 적다는 이유만으로 계속 쓰기보다 날 교체를 검토해요 [kb:B-S06@0.6.1].

### 근거 및 이유
교체 검토에는 횟수뿐 아니라 실제 날 상태가 중요해요. 수동 날의 참고 사용 횟수는 손상된 날을 그 횟수까지 반드시 사용하라는 뜻이 아니에요 [kb:B-S06@0.6.1] [ref:S23].

### 확인이 필요한 한계
통증은 없다고 확인됐으며 통증이나 감염을 새로 추정하지 않아요. 사용 횟수를 경과 일수나 다른 면도기 부품의 교체 주기로 바꾸지 않아요.
손상이나 당김을 무시하고 계속 사용했는지는 확인되지 않았어요.

## syn-sol-0045

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `55ec0c9730fe63c33ad26ad90d58bb3a88ed76f00fd6efaabccb3e3dabff9553`
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
        "uses_tolerated_moisturizer": true,
        "uses_aftershave": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "stinging": false,
        "persistent_problem": false
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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "면도 후 현재 보습이 편안하고 새 불편이 없어 애프터셰이브 상품을 의무로 추가하지 않아요."
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
면도 뒤 현재 보습제를 편안하게 쓰고 있고 따가움이나 지속적인 문제도 없다고 했어요. 별도 애프터셰이브 상품을 의무로 추가하지 않고 지금의 보습을 유지할 수 있어요 [kb:B-M05@0.6.1].

### 근거 및 이유
면도 후 보습 안내가 모든 사람에게 별도 애프터셰이브를 요구하는 것은 아니에요. 실제 사용 경험을 함께 보는 것이 이 사례의 기준이에요 [ref:S25] [kb:B-M05@0.6.1].

### 확인이 필요한 한계
현재 편안함은 특정 성분이나 모든 면도 후 제품의 적합성을 입증하지 않아요. 전성분이나 미공개 농도는 제공되지 않아 추정하지 않아요.

## syn-sol-0063

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cdfaa58b901d75187fd1b93f5aff91ac239c3ab6034b7f501554276a69fedf39`
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
        "context": "야외 경기 관람"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "shade_available": true,
        "shade_used": false,
        "reason": "선크림만으로 충분하다고 생각함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "장시간 야외에서 이용 가능한 그늘을 선크림만으로 충분하다는 생각에 사용하지 않아요. 다른 실행 가능한 수단을 모두 배제했는지는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
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

### 응답 초안 — 미승인

### 핵심 안내
장시간 야외 경기 관람에서는 선크림만으로 충분하다고 보고 그늘을 배제하기보다, 이용 가능한 그늘을 함께 활용해요 [kb:B-P04@0.6.1].

### 근거 및 이유
일반 광보호 안내는 제품 표시뿐 아니라 야외 노출과 그늘·의복을 함께 검토해요 [ref:S05]. 그늘을 이용할 수 있다는 확인된 상황을 반영한 안내예요.

### 확인이 필요한 한계
그늘 이용이나 선크림 사용만으로 실제 받은 자외선량과 보호 수준을 계산할 수는 없어요. 실행 가능한 보완 수단을 선택하되 보호율을 합산하지 않아요.
다른 실행 가능한 보완 수단을 모두 배제했는지는 확인되지 않았어요.

## syn-sol-0064

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3d1c647b639e381e0ef2082440f755233ed10492305d469280f513bfc0646ca9`
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
        "제품": "합성 얼굴 팩",
        "표시 접촉시간 분": 10,
        "실제 접촉시간 분": 30,
        "취침 중 사용": false,
        "이유": "오래 붙이면 더 효과적이라고 생각함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "얼굴에 10분 사용 후 제거",
        "현재 버전 확인": true
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
      "card_id": "B-G05",
      "status": "difference",
      "guidance": "합성 팩의 확인된 10분 지시보다 실제 30분 사용이 길어 제품별 접촉시간에 맞춘 조정 대상이에요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-64",
      "version": "revision1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 얼굴에 10분 사용 후 제거해요. 취침 중 사용하는 제품이 아니에요.",
      "evidence_ref": "catalog:syn-add100-b-64@revision1"
    }
  ],
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
    "catalog:syn-add100-b-64@revision1",
    "ref:S26"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 합성 팩은 얼굴에 10분 사용 후 제거하도록 표시되어 있는데 실제로는 30분 붙이고 있어요. 오래 쓸수록 더 좋다고 보지 않고 확인된 제품별 접촉시간에 맞춰 조정해요 [kb:B-G05@0.6.1] [catalog:syn-add100-b-64@revision1].

### 근거 및 이유
팩 안내는 각 제품의 접촉시간과 빈도, 기존 각질관리와의 중복을 함께 살펴요. 모든 팩에 같은 시간을 정하는 원칙은 아니에요 [ref:S26].

### 확인이 필요한 한계
현재 불편이 없다는 보고가 긴 접촉시간의 효과나 무해성을 입증하지는 않아요. 이 합성 제품의 10분을 다른 팩이나 기기에 공통 기준으로 적용하지 않아요.

## syn-sol-0065

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a65eb4fd1bcc2b340d635db00de374d5ab9666b6a0b59d6a7ad852d04ce50937`
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
        "after_swim_and_towel": true,
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
      "guidance": "수영 후 수건으로 닦고 야외 노출이 이어지는 상황에서 표시대로 다시 바르고 있어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
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
수영 후 수건으로 닦고 야외 활동이 이어질 때 표시대로 다시 바르는 행동은 유지해요 [kb:B-P03@0.6.1].

### 근거 및 이유
물과 닦임, 계속되는 야외 노출을 함께 반영한 재도포예요. 일반 안내도 제품 표시와 물·땀 등 노출 조건을 함께 검토해요 [ref:S05].

### 확인이 필요한 한계
이는 확인된 행동이 해당 기준과 맞는다는 뜻이에요. 실제 남은 양이나 개인의 보호 성능을 측정한 결과는 아니에요.

## syn-sol-0066

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `7bac431a819ec846d604d111925892a0c956a9a42b52c7f2d251ffb7158f0fdf`
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
      "status": "aligned",
      "guidance": "새 야외용 합성 후보에서 SPF 50, UVA·UVB 보호와 내수성 표시가 확인되어 기본 표시 조건에 맞아요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-66",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: SPF 50, UVA·UVB 광범위 보호, 내수성 표시가 있어요.",
      "evidence_ref": "catalog:syn-add100-b-66@v1"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Professional sunscreen guidance discusses SPF 30 or higher, UVA and UVB coverage, water resistance and outdoor reapplication. Exposure conditions and non-product protection also matter. This is not a universal indoor reapplication schedule or a statement of Korean legal minimums.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "catalog:syn-add100-b-66@v1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
새 야외용 합성 후보의 SPF 50, UVA·UVB 광범위 보호와 내수성 표시는 기본 선택 조건에 맞아요. 이 표시 항목에서는 후보로 검토할 수 있어요 [kb:B-P01@0.6.1] [catalog:syn-add100-b-66@v1].

### 근거 및 이유
제공된 전문기관 안내는 SPF 30 이상, UVA·UVB 보호와 내수성을 일반적인 선택 기준으로 다뤄요 [ref:S16].

### 확인이 필요한 한계
기본 표시 충족이 개인 적합성이나 제품 전체의 안전·효과를 보증하지는 않아요. 이 기준을 한국의 법적 최소치로 해석하지 않아요.

## syn-sol-0067

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `550c0a3aa5327b3e49f597cfcf4944e5c8a6778f7b01c83010aa61cd9899d083`
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
        "label_expired": true
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
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "continues_relying_on_expired_sunscreen": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "difference",
      "guidance": "표시 기한이 지난 것이 확인되어 외관 변화가 없더라도 계속 광보호를 맡기는 사용은 조정 대상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S18",
      "text": "자외선차단제의 사용기한과 열 노출, 품질 변화 사례를 다루는 안내예요. 실제 제품의 표시와 보관 이력을 함께 확인해야 해요. 미국의 기한 규칙을 한국의 모든 제품에 적용하거나 정확한 SPF 감소율을 계산할 수는 없어요.",
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
외관이 그대로여도 표시 기한이 지난 선크림에 계속 광보호를 맡기는 사용은 조정이 필요해요. 기한을 확인할 수 있는 대안과 필요한 광보호 방법을 검토해요 [kb:B-P08@0.6.1].

### 근거 및 이유
사용기한과 품질 변화는 함께 살펴야 하며, 색·냄새 변화가 없다는 관찰이 지난 기한을 무효로 만들지는 않아요 [ref:S18].

### 확인이 필요한 한계
현재 제품의 SPF가 얼마나 감소했는지, 내부 품질이 어떤지는 미상이에요. 외관만으로 정상이나 변질을 확정하지 않아요.

## syn-sol-0068

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `49a4b1e2dce07656b5f80dbec2897c38e49be77ab99e30bef6c7c847a84999fd`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "제조사 지정 2제형 얼굴 팩 키트",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "동일 키트 A제와 B제만 혼합": true,
        "다른 화장품 추가": false,
        "표시 비율 준수": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "동봉 A제 한 포와 B제 한 포를 전량 혼합한 뒤 얼굴에 10분 사용 후 제거",
        "현재 버전 확인": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "표시 접촉시간 준수": true
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
      "card_id": "B-G04",
      "status": "exception",
      "guidance": "동일 키트의 두 제제를 제조사가 명시한 방법대로 혼합하므로 근거 없는 임의 혼합 기본 금지를 강제하지 않는 예외예요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-68",
      "version": "revision1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 동봉 A제 한 포와 B제 한 포를 전량 혼합한 뒤 얼굴에 10분 사용 후 제거해요. 다른 제품을 추가하지 않아요.",
      "evidence_ref": "catalog:syn-add100-b-68@revision1"
    }
  ],
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
    "kb:B-G04@0.6.1",
    "catalog:syn-add100-b-68@revision1",
    "ref:S26"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 합성 키트는 동봉 A제와 B제를 표시대로 혼합하도록 명시되어 있어요. 확인된 두 제제만 표시 비율로 섞는 행동에 임의 혼합 금지를 강제하지 않아요 [kb:B-G04@0.6.1] [catalog:syn-add100-b-68@revision1].

### 근거 및 이유
혼합을 허용하는 근거는 이 키트의 확인된 합성 표시예요. 일반 팩 안내는 제품별 접촉시간과 빈도를 따르도록 하는 범위이며, 임의의 제품 혼합을 승인하는 자료는 아니에요 [catalog:syn-add100-b-68@revision1] [ref:S26].

### 확인이 필요한 한계
이 예외는 같은 키트의 지정된 A제와 B제에만 해당해요. 다른 화장품 추가나 임의 비율 변경으로 확대하지 않으며, 현재 불편이 없다는 보고만으로 개인의 안전성이나 효과를 보증하지 않아요.

## syn-sol-0069

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `63a2a9eefea8acd959ab0b7efa7f7e877861fa1c2db6f2fcb93df69f03822385`
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
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "premixed_in_palm": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_use_reduced_due_to_layering": false,
        "reapplication_omitted_due_to_layering": false
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
      "card_id": "B-I02",
      "status": "exception",
      "guidance": "밀림 때문에 선크림 사용을 줄이거나 재도포를 생략하지 않았다고 보고했어요. 다른 이유에 따른 변화는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "제한된 보습제와 자외선차단제 조합에서 도포 순서를 UV 반사 영상으로 살핀 연구예요. 관찰된 영상 결과는 실제 SPF나 야외 보호 성능을 보증하지 않아요. 각각 층으로 바른 결과를 손바닥에서 미리 섞는 행동에 그대로 적용할 수는 없어요.",
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
밀림은 있지만 중첩 때문에 선크림 사용을 줄이거나 재도포를 생략하지 않았다고 보고됐어요. 다른 이유에 따른 변화는 미상이며, 밀림 자체의 사용성을 따로 검토해요 [kb:B-I02@0.6.1].

### 근거 및 이유
제한된 조합의 도포 순서 연구는 UV 반사 영상 지표를 살폈어요. 밀림이 곧 실제 SPF 저하라는 결론을 주지는 않아요 [ref:S09].

### 확인이 필요한 한계
현재 조합의 실제 보호 성능과 밀림 원인은 미상이에요. 각각 층으로 바른 보고를 손바닥에서 미리 섞었다는 뜻으로 바꾸지 않아요.

## syn-sol-0070

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `9e286152d12b80fe5c5edb33324f59ffc09387e0cfb6fb5479ac9ac29eaf2802`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.application_form": {
      "variable_id": "product.application_form",
      "state": "known",
      "value": "non_gas_spray",
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
        "direct_spray_to_face": true,
        "eyes_closed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P09",
      "status": "difference",
      "guidance": "손에 덜어 얼굴에 바르라는 합성 제품 지시와 달리 눈을 감고 얼굴에 직접 분사하고 있어요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-70",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 얼굴에 직접 분사하지 않고 손에 덜어 얼굴에 발라요.",
      "evidence_ref": "catalog:syn-add100-b-70@v1"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P09@0.6.1",
    "catalog:syn-add100-b-70@v1",
    "ref:S05"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
눈을 감아도 얼굴 직접 분사를 표시 방법의 대안으로 보지 않아요. 이 합성 제품의 지시대로 손에 덜어 얼굴에 바르는 방식으로 조정해요 [kb:B-P09@0.6.1] [catalog:syn-add100-b-70@v1].

### 근거 및 이유
비가스 분무형이라는 사실과 얼굴 직접 분사 행동이 확인됐어요. 조정의 구체적인 근거는 이 제품의 확인된 표시예요 [catalog:syn-add100-b-70@v1].

### 확인이 필요한 한계
방식을 바꾼다고 필요한 도포량을 줄여도 된다는 뜻은 아니에요. 실제 흡입량이나 손상 여부, 보호 성능은 이 입력에서 알 수 없어요.

## syn-sol-0071

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `25b467858e93b0192cc64f557834d182e7e9fa8a13df18be1992abf42bd90535`
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
        "shade_break_available": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "exception",
      "guidance": "작업 제약 때문에 긴소매가 어렵다고 확인되어 그 수단을 강제하지 않고 가능한 그늘 휴식을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S14",
      "text": "햇빛 노출에서 그늘과 의복, 선글라스와 제품 표시를 함께 검토하는 안내예요. 특정 약물의 중단이나 개인별 자외선 손상량을 계산하는 자료는 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/consumers/consumer-updates/tips-stay-safe-sun-sunscreen-sunglasses",
      "locator": "Sun damage / Read Sunscreen Labels / Risk Factors",
      "checked_on": "2026-11-04",
      "limitations": "미국의 표시 규정은 한국 규정과 분리. 관련 약물 유무 확인과 전문가 연결만 고려하며 약물 중단 권고에 쓰지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S14"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
작업 때문에 긴소매가 어렵다는 제약을 존중해요. 긴소매를 강제하는 대신 이용 가능한 그늘 휴식을 광보호 보완 수단으로 검토해요 [kb:B-P04@0.6.1].

### 근거 및 이유
일반 안내는 그늘·의복 등 가능한 보호수단과 제품 표시를 함께 살펴요. 실행할 수 없는 수단을 사용자의 잘못으로 판단하지 않아요 [ref:S14] [kb:B-P04@0.6.1].

### 확인이 필요한 한계
그늘 휴식을 실제로 이용했는지는 아직 확인되지 않았어요. 이 방법만으로 개인의 자외선 노출량이나 손상량을 계산하지 않아요.

## syn-sol-0089

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `66b97c16b28c0e798f914bd1863e3ce5df4dc223ab2bc13bf7e9bc173c64a660`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "기존 보습제 유지 여부",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "현재 제품": "향료 포함"
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
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "현재 제품을 유지하고 싶음"
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
      "card_id": "B-G01",
      "status": "exception",
      "guidance": "향료 포함은 확인됐지만 현재 불편이 없고 기존 제품 유지를 원해요. 새 후보의 무향료 선호를 기존 제품의 의무 교체로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic allergen guidance discusses fragrance and individual avoidance, labeling and manufacturer instructions. Fragrance presence alone does not establish irritation or allergy in every person. United States labeling explanations are not automatically Korean legal requirements.",
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

### 응답 초안 — 미승인

### 핵심 안내
지금 불편 없이 쓰고 있고 유지를 원하는 기존 보습제를 향료 포함만으로 의무 교체하지는 않아요. [kb:B-G01@0.6.1]

### 근거 및 이유
새 후보에서 무향료를 우선하는 서비스 선호와 현재 향료 제품이 개인에게 해롭다는 판단은 달라요. [kb:B-G01@0.6.1] 향료 알레르겐에 관한 일반 정보는 개별 회피 맥락에서 살펴요. [ref:S15]

### 확인이 필요한 한계
현재 편안하다는 관찰도 앞으로의 무반응을 보증하지는 않아요. 새 반응이나 확인된 알레르겐이 생기면 해당 정보를 따로 검토해요.

## syn-sol-0090

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1ed5e21e6051775c0d66c3129bc98562c9a2d399a2cb2fb1bcd92d308771c603`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "비슷한 기능과 실행 가능성의 새 보습제 두 후보 비교",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "선택 후보": "무향료 확인",
        "대조 후보": "향료 포함 확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "무향료 후보 선택"
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
      "card_id": "B-G01",
      "status": "aligned",
      "guidance": "조건이 비슷한 새 후보 중 무향료 확인 후보를 선택해 해당 선호와 일치해요. 개인의 무반응이나 다른 알레르겐 부재까지 보장하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic allergen guidance discusses fragrance and individual avoidance, labeling and manufacturer instructions. Fragrance presence alone does not establish irritation or allergy in every person. United States labeling explanations are not automatically Korean legal requirements.",
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

### 응답 초안 — 미승인

### 핵심 안내
기능과 실행 가능성이 비슷한 새 후보 중 확인된 무향료 후보를 고른 현재 선택은 해당 선호와 일치해요. [kb:B-G01@0.6.1]

### 근거 및 이유
향료 여부는 새 후보를 비교할 한 항목이에요. 향료 포함만으로 모든 사람의 알레르기나 자극을 확정할 수는 없어요. [ref:S15]

### 확인이 필요한 한계
무향료 선택이 개인의 모든 알레르겐 부재나 제품 전체의 무해성을 뜻하지는 않아요.

## syn-sol-0091

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `e29756053c63b7c2743f585e43c9c1af64d02c690f28715340c795179f89b574`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "일반 성인용 씻어내는 세안제",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "내용": "합성 표시: 피부에 오래 두지 않고 헹굼"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "국소 사용 확인": true,
        "매회 표시대로 헹굼": true,
        "현재 관찰 일수": 8
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
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "내용": "확인된 알레르기 없음"
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
            "statement": "관찰 부위 불편 없음"
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
      "guidance": "세안제를 작은 부위에서 표시대로 헹구며 확인 중이지만 처음 사용할 제품인지는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "General guidance describes trying a new skin-care product on a small area for seven to ten days. Product-specific directions still apply, including rinse-off directions. This is not a diagnostic allergy patch test or a guarantee of permanent safety.",
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
세안제를 작은 부위에서 매번 표시대로 헹구며 확인 중이라고 보고했어요. 처음 사용할 제품인지는 확인되지 않았어요 [kb:B-G11@0.6.1].

### 근거 및 이유
새 제품의 작은 부위 확인에 관한 일반 안내도 제품별 씻어내는 지시를 고려해요 [ref:S35].

### 확인이 필요한 한계
관찰 부위의 구체적 위치는 미상이에요. 불편이 없다는 관찰은 진단용 알레르기 검사나 안전 보증이 아니에요.

## syn-sol-0092

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `88e79b3fb4815c6cf77f99b87995432d92268833883143d2812116dfb75fdb0a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "현재 변경": "보습제 하나만 도입",
        "다른 제품": "변경 없음",
        "기록": "실제 사용과 불편 여부 기록 중"
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
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "사용 부담을 늘리지 않기"
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
      "card_id": "B-G12",
      "status": "aligned",
      "guidance": "한 제품의 변경과 실제 사용을 나눠 기록하고 있어요. 모든 사람에게 일주일이나 한 달의 고정 대기기간을 새로 요구하지 않아요."
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
    "kb:B-G12@0.6.1",
    "ref:S35"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
지금처럼 보습제 하나의 변경과 실제 사용·불편 여부를 나눠 기록하는 방향을 유지할 수 있어요. [kb:B-G12@0.6.1]

### 근거 및 이유
새 제품의 작은 부위 확인을 다루는 일반 안내가 있어요. [ref:S35] 변경 이력을 나눠 해석하는 서비스 원칙은 모든 변경에 같은 대기기간을 붙이지 않아요. [kb:B-G12@0.6.1]

### 확인이 필요한 한계
현재 불편이 없다는 기록만으로 특정 성분의 효과를 증명하지는 못해요. 기록 부담을 늘리기 위한 고정 주기나 추가 제품도 만들지 않아요.

## syn-sol-0093

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `43320c24d6ce234fd5cb96b24b82b355004ee59040ed56e75c5e6a94d720b8b9`
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
        "실제 방식": "전기면도기",
        "사용 부위": "얼굴"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.preparation": {
      "variable_id": "shaving.preparation",
      "state": "known",
      "value": {
        "실제 사용": "얼굴과 헤드를 물에 적시고 면도 크림을 함께 사용했어요."
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "제품": "합성 건식 전기면도기",
        "확인된 표시": "건식 전용이며 물과 면도 크림을 함께 사용하지 않도록 표시돼요."
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
            "statement": "현재 불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G09",
      "status": "difference",
      "guidance": "건식 전용 표시가 확인된 전기면도기에 실제로 물과 크림을 사용했으므로 기기별 지시와 현재 준비 방식에 차이가 있어요. 습식 날면도 준비를 그대로 확대하지 않아요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-dry-shaver-c93",
      "version": "1.0",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 기기 표시 예시: 건식 전용. 물과 면도 크림을 함께 사용하지 않아요.",
      "evidence_ref": "catalog:syn-dry-shaver-c93@1.0"
    }
  ],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G09@0.6.1",
    "catalog:syn-dry-shaver-c93@1.0"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
지금 쓰는 합성 전기면도기는 건식 전용으로 확인됐는데 실제로 물과 면도 크림을 함께 사용했어요. 습식 날면도 준비를 이 기기에 적용하지 말고 확인된 건식 전용 지시에 맞게 준비 방식을 바꿔요. [kb:B-G09@0.6.1] [catalog:syn-dry-shaver-c93@1.0]

### 근거 및 이유
면도 준비는 방식에 따라 달라요. 피부와 털을 적시는 습식 날면도 안내가 모든 전기면도기에 물과 크림을 쓰라는 뜻은 아니에요. [kb:B-G09@0.6.1]

### 확인이 필요한 한계
현재 불편이 없다는 관찰만으로 표시와 다른 사용이 적합하다고 보증할 수는 없어요. 이번 차이는 기기별 용법에 관한 것이며 피부 손상이나 질환이 생겼다고 판단한 것은 아니에요.

## syn-sol-0094

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0bf909537022e5281d916ec20489a86d2c17ed40c2b5d9244375fc46065287c0`
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
        "제품 가": "AHA 각질관리 화장품",
        "제품 나": "BHA 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "내용": "별도 두 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": true,
        "두 제품 부위": "양팔의 같은 부위",
        "같은 저녁": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "별도 병용 계획 없음"
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
      "card_id": "B-G15",
      "status": "difference",
      "guidance": "같은 팔 부위에 별도 각질관리 화장품 둘을 실제로 겹쳐 쓰므로 보수적 기본값과 차이가 있어요. 불편이 없다는 사실로 중첩의 개인 안전성을 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about adding exfoliation while using retinol or prescription retinoids. Actual care purpose and contact site matter. This guidance does not establish a universal contraindication or an individual probability of harm.",
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
같은 팔 부위에 별도 AHA·BHA 각질관리 화장품을 같은 저녁 겹쳐 쓰는 점은 보수적 기본값과 달라요. 불필요하게 겹친 관리를 줄이고 필요한 한 종류를 우선 검토해요. [kb:B-G15@0.6.1]

### 근거 및 이유
과도한 각질관리 회피 안내를 바탕으로 별도 관리의 중복을 줄이는 서비스 기준이에요. 모든 조합의 절대 금기를 입증한 비교시험은 아니에요. [ref:S32]

### 확인이 필요한 한계
현재 불편이 없다는 사실로 개인 안전을 확정하거나 나중 반응의 원인을 단정할 수는 없어요. 처방이나 임상 효과에 대한 판단도 아니에요.

## syn-sol-0095

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bd8943e5215189db2b8216e6988ca67be1a2cafb7922eede1bc17c4bed6af709`
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
        "제품 가": "처방 레티노이드",
        "제품 나": "살리실릭애씨드 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": true,
        "제품 가 부위": "얼굴",
        "제품 나 부위": "등",
        "서로 접촉 부위 겹침": false
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
      "card_id": "B-G14",
      "status": "exception",
      "guidance": "실제 접촉 부위가 서로 다르므로 같은 부위의 별도 제품 중첩 규칙을 그대로 적용하지 않아요. 처방 변경이나 전체 병용 안전 보증은 하지 않아요."
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
얼굴의 처방 레티노이드와 등의 살리실릭 관리가 실제로 다른 부위에만 닿는다면 같은 부위 중첩 규칙을 그대로 적용하지 않아요. 처방은 임의로 바꾸지 않아요. [kb:B-G14@0.6.1]

### 근거 및 이유
특정 트레티노인 표시의 병용 주의는 해당 제품과 사용 맥락의 범위에서 읽어야 해요. 다른 부위라는 관찰을 지우고 얼굴 중첩으로 바꾸지는 않아요. [ref:S34]

### 확인이 필요한 한계
같은 부위 규칙의 예외라는 뜻이지 전체 병용의 무자극 보증은 아니에요. 처방 제품의 개별 지시나 새 증상은 별도로 확인해야 해요.

## syn-sol-0096

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `27254b9ffd246a923207139a1d9773fa37351d9cf872bfc2d6a755a01116ce4a`
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
        "제품 가": "AHA 각질관리 화장품",
        "제품 나": "BHA 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "내용": "별도 두 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": true,
        "부위": "얼굴 동일 부위",
        "사용 기간 겹침": true,
        "일정": "하루씩 번갈아 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "별도 병용 계획 없음"
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
      "card_id": "B-G15",
      "status": "difference",
      "guidance": "같은 얼굴 부위의 별도 각질관리를 겹치는 기간에 사용해요. 격일이라는 이유만으로 자동 적합 판정하지 않아요."
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
별도 AHA와 BHA 각질관리를 얼굴 같은 부위에 번갈아 쓰고 있어요. 격일이라는 이유만으로 자동 적합으로 보지 않고, 불필요한 중복을 줄여 필요한 한 종류를 우선 검토해요. [kb:B-G15@0.6.1]

### 근거 및 이유
겹치는 사용기간의 중첩을 보는 서비스 기본값은 달력의 하루 차이만으로 없어지지 않아요. [kb:B-G15@0.6.1] 일반 각질관리 안내는 레티노이드와 추가 각질관리 상황 등을 다루며 개인의 위해확률을 계산하지 않아요. [ref:S32]

### 확인이 필요한 한계
구체적인 새 일정이나 모든 조합의 금기를 만들지는 않아요. 제품 지시와 반응, 개별 병용 계획이 새로 확인되면 그 범위를 다시 검토해요.

## syn-hold-0013

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `eb3fc5b3488232b1fc5debecda3e2812b84bcb7c081be856f20e4b746fe6e04f`
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
        "color_or_odor_change": true,
        "separation": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "normal_particles_indicated": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "원래 없던 입자와 색 또는 냄새 변화가 확인돼 품질 확인 전 사용과 개별 권고를 보류해요. 제품 유형과 변화의 구체적 종류·원인은 확정하지 않아요."
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
제품에 원래 없던 입자와 색 또는 냄새 변화가 보고됐고, 정상 입자라는 표시도 확인되지 않았어요. 품질 확인 전 개별 루틴과 제품 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 정상 제형 특성인지 제조·판매처에 확인할 필요가 있어요. 제품 유형과 변화의 구체적인 종류는 미확인이며, 관찰만으로 미생물 오염이나 원인을 확정하지 않아요.

## syn-hold-0014

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `3c85db949fab0cf0f47560cdfecc00572725a98af59980d720474c6e37e0feb2`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "commerce.received_condition": {
      "variable_id": "commerce.received_condition",
      "state": "known",
      "value": {
        "ordered_product": "합성 보습제 A",
        "received_product": "합성 세정제 B",
        "mismatch_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "actual_product_verified": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q04",
      "status": "hold",
      "guidance": "수령품이 주문 제품과 명백히 달라 사용 전 식별 확인이 필요해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
합성 보습제 A를 주문했지만 합성 세정제 B를 받아 주문과 수령품의 불일치가 확인됐어요. 실제 제품 식별도 검증되지 않아 개별 사용법과 제품 권고를 보류해요 [kb:B-Q04@0.6.1].

### 필요한 다음 단계
수령품의 제품명과 표시를 주문 내역과 대조하고 판매처에 식별·오배송 여부를 확인해야 해요. 주문한 보습제의 사용법을 수령품에 적용하거나 수령품의 성분·용도를 추정하지 않아요.

## syn-hold-0015

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `a7aeaa3bf586f950129dc2c240f60eedfa5d2267fe0e1e661d56398c2a1faf08`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "commerce.authenticity_concern": {
      "variable_id": "commerce.authenticity_concern",
      "state": "known",
      "value": {
        "quality_concern": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.end_of_use": {
      "variable_id": "commerce.end_of_use",
      "state": "known",
      "value": {
        "official_instruction": "안전하게 즉시 폐기",
        "instruction_confirmed_in_synthetic_case": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q06",
      "status": "hold",
      "guidance": "공식 확인에서 안전한 즉시 폐기를 지시한 합성 상황이므로 증빙 확보를 위해 위험 제품 보관을 강요하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
이 합성 상황에서는 품질 우려에 대한 공식 확인에서 안전하게 즉시 폐기하라는 지시가 확인됐어요. 일반적인 제품 사용이나 루틴 권고는 보류해요 [kb:B-Q06@0.6.1].

### 필요한 다음 단계
확인된 공식 폐기 안내를 우선해요. 증빙을 모으려는 이유로 제품 보관을 강요하지 않으며, 폐기 방법이 불명확하면 안내한 공식 창구에 확인해요. 품질 문제의 구체적 원인까지 확정된 것은 아니에요.

## syn-hold-0016

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `3c848a3cf29cb30a68bc1cb2c7694d1c4009cd1a0859dcbffec9560dd265b325`
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
        "changed_to_gentle_washing": true,
        "pain_remains": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "세안 방법을 바꿨는데도 통증과 지속 불편이 있어 일반 루틴 최적화보다 전문가 확인이 우선이에요."
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
부드러운 세안으로 바꾼 뒤에도 중등도 통증과 지속 불편이 남아 있어요. 일반적인 세안 최적화나 개별 제품 권고는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
통증이 이어지는 현재 상태는 피부과 등 전문가의 확인을 우선해요. 언제부터 어떤 통증이 있었는지와 이미 바꾼 방법을 상담 때 전달할 수 있어요. 세안이 원인이라고 진단하거나 다른 방법의 효과를 약속하지 않아요.

## syn-hold-0017

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `650d5062c1fd9abb10cfbb3edb51126d180defd96464347ab795bb62837ab3c6`
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
        "skin_penetrating_device": true,
        "requested_action": "개인별 침투 깊이와 반복 통과 횟수 및 병용 제품을 정해 달라는 요청",
        "procedure_already_performed": false
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
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
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
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "침습시술의 개인별 절차를 만드는 요청은 일반 화장품 도포 안내의 범위를 벗어나 해당 시술·병용 설계를 보류해요. 깊이·반복 횟수나 적합성을 추정하지 않아요."
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
피부를 관통하는 기기의 개인별 깊이·반복 통과 횟수와 병용 제품을 정하는 요청은 일반 화장품 도포 안내의 범위를 벗어나요. 해당 시술 절차와 병용 조합의 개별 설계를 보류해요 [kb:B-G06@0.6.1].

### 필요한 다음 단계
관련 자격을 갖춘 전문가에게 요청한 행위의 적용 범위와 적합성을 확인해야 해요. 제품 지침과 개별 진료 계획은 미상이며, 깊이·횟수·대체 조합을 만들어 안내하지 않아요. 아직 시행하지 않은 계획을 실제 시술이나 발생한 손상으로 바꾸지 않아요.

## syn-hold-0018

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `4950f4849f789244209c05f712982077c6b75b10913ccd08e0e151112c320c9d`
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
        "do_not_use_with_this_device": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "combination_planned": true,
        "already_combined": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "instructions": {
          "combination_prohibited": true,
          "synthetic_fixture": true
        },
        "combination_planned": true,
        "already_combined": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "합성 기기와 제품 표시에서 병용하지 말라는 지시가 확인돼 해당 조합 권고를 보류해요."
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
이 합성 기기와 제품에는 서로 병용하지 말라는 표시가 확인됐어요. 조합은 아직 계획 단계이며 이미 함께 썼다고 보지 않고, 해당 조합의 개별 권고를 보류해요 [kb:B-G06@0.6.1].

### 필요한 다음 단계
기기와 제품의 정확한 표시 및 제조사 안내를 확인해야 해요. 병용 금지의 범위가 불명확하면 해당 안내 주체에 확인하고, 임의의 강도·시간·대체 조합은 제시하지 않아요. 실제 위해가 발생했다고 추정하지도 않아요.

## syn-hold-0019

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `1befb31a7bfe3c47eee63562a7fe1dba13ec7d743ebb40e709c46c2055820827`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "skin.pain": {
      "variable_id": "skin.pain",
      "state": "known",
      "value": "severe",
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
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "new_cosmetic": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "새 제품이 없더라도 심한 통증은 일반 루틴 안내 범위를 넘어 전문가 확인이 우선이에요."
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
새 화장품을 쓰지 않았더라도 심한 통증과 지속 불편이 확인됐어요. 이는 일반적인 루틴 지원 범위를 넘어 개별 루틴과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
심한 통증과 지속 불편이 보고된 상황에서는 지체하지 말고 의료 전문가의 확인을 받아야 해요. 통증의 시작과 경과를 상담 때 전달할 수 있어요. 새 제품이 없다는 사실로 원인을 배제하거나 특정 질환을 진단하지 않아요.

## syn-hold-0020

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `b9ed80dfe1828eb5983dce518482c531559ed3c795bc3cceae988d3b1e936691`
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
    "commerce.authenticity_concern": {
      "variable_id": "commerce.authenticity_concern",
      "state": "known",
      "value": {
        "specific_concern_reported": true,
        "authenticity_confirmed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.receipt_record": {
      "variable_id": "commerce.receipt_record",
      "state": "known",
      "value": {
        "currently_available": false,
        "collection_would_delay_health_consultation": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "seller_evidence": {
          "requested_collection": "모두",
          "planned_relative_to_consultation": "before"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q06",
      "status": "hold",
      "guidance": "지속되는 심한 통증이 있어 개별 제품·루틴 권고는 보류해요. 증빙 수집 때문에 전문가의 도움을 미루지 않도록 하고 제품 진위나 증상의 원인을 확정하지 않아요."
    },
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 심한 통증은 개별 사용법 조정보다 전문가 확인을 우선하는 보류 조건이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q06@0.6.1",
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
심한 통증과 불편이 계속되고 있어 제품이나 루틴에 대한 개별 안내는 보류해요 [kb:B-B01@0.6.1]. 정품인지, 제품이 통증과 관련이 있는지는 확인되지 않았어요.

### 필요한 다음 단계
판매자 증빙을 모으느라 상담을 늦추지 말고 우선 의료 전문가의 확인을 받아 주세요. 현재 영수증이 없어도 건강 문제의 확인을 미룰 이유가 되지는 않아요 [kb:B-Q06@0.6.1].

## syn-hold-0021

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `db6e11cfb06d22b59f18119ac018c3a5632cf7201c139bb8ea96419cc7926d47`
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
        "합성 제품": "확인된 보유품",
        "동일 제품명과 버전 확인": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.batch": {
      "variable_id": "storage.batch",
      "state": "known",
      "value": {
        "보유 제조번호": "SYN-B21"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "합성 공식 공지 1": "SYN-B21은 대상에서 제외",
        "합성 공식 공지 2": "SYN-B21 포함, 범위 확인 전 사용 보류",
        "두 공지의 최신 적용 버전": "미확인",
        "조회일": "2026-11-23"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "어느 공지가 최신인지 확인되지 않은 채 보유품 사용 일정 요청",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "같은 제조번호에 관한 합성 공식 공지가 상충하고 한 공지가 확인 전 사용 보류를 명시해요. 최종 회수 대상 여부는 미상으로 남기고 개별 사용 권고를 보류해요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-hold21",
      "version": "revision1",
      "synthetic_product": true,
      "status": "usage_held",
      "label_guidance": "합성 제품 표시 예시: 합성 회수 자료의 제조번호 범위가 상충해요. 최신 적용 공지를 확인하기 전 사용 보류가 명시되어 있어요.",
      "evidence_ref": "catalog:syn-add100-b-hold21@revision1"
    }
  ],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q05@0.6.1",
    "catalog:syn-add100-b-hold21@revision1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
같은 제조번호에 관한 합성 공식 회수 공지가 상충하고 최신 적용 버전이 확인되지 않았어요. 한 공지가 확인 전 사용 보류를 명시하므로 개별 사용 일정이나 제품 권고는 보류해요. 최종 회수 대상 여부는 미상으로 남겨요 [kb:B-Q05@0.6.1] [catalog:syn-add100-b-hold21@revision1].

### 필요한 다음 단계
제품 식별 정보와 제조번호, 두 공지의 게시·적용 버전을 공식 문의 경로에서 대조해요. 어느 공지가 현재 유효한지와 임시 보류의 해제 조건을 확인하기 전에는 대상 제외나 사용 재개를 확정하지 않아요. 다른 제조번호나 브랜드 전체로 범위를 넓히지 않아요.

## syn-hold-0022

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `4ca95772c3f290cad698f23b6cc65a9611b1f5b1492bc7f9b3a246fa3be2379d`
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
    "skin.stinging": {
      "variable_id": "skin.stinging",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.duration": {
      "variable_id": "skin.duration",
      "state": "known",
      "value": {
        "reported": "사용 후 계속 이어짐"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "solve_by_reducing_sunscreen_amount",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편감과 통증을 도포량 감량만으로 해결하려는 상황이라 개별 루틴 조정을 보류해요."
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
사용 후 지속되는 불편감과 중간 정도의 통증·따가움이 보고됐어요. 양을 줄이면 해결된다고 보지 않고 개별 루틴 조정과 제품 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
증상 시작 시점과 지속 양상, 관련 제품 정보를 정리해 피부과 등 전문가에게 확인을 받아요. 현재 정보만으로 원인을 진단하거나 회복을 보장할 수 없어요.

## syn-hold-0023

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `4273206dc8ca5f213b645b6cf5f083c069a1a6e48eb6cce80aa5db216d73747c`
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
        "color_or_odor_change": false,
        "separation": false,
        "new_gritty_texture": true,
        "previous_texture_was_smooth": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_dilute_and_continue": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "기존에 없던 알갱이와 질감 변화가 확인되어 희석해서 계속 쓰는 개별 사용 안내를 보류해요."
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
이전에는 없던 알갱이와 질감 변화가 확인됐어요. 색·냄새 변화나 층 분리가 없어도 희석해서 계속 쓰는 방법이나 개별 루틴·제품 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
사용기한·개봉과 보관 이력, 변화가 나타난 시점을 확인하고 제조·판매처에 정상 특성인지와 처리 절차를 문의해요. 오염이나 특정 성분 변화를 단정하지 않아요.

## syn-hold-0024

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `613051e8388ce4f7c17c4ac1322ac022f9c01dd0fde31da44801a625c8553fc8`
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
    "storage.seal_integrity": {
      "variable_id": "storage.seal_integrity",
      "state": "known",
      "value": {
        "new_container_swelling": true,
        "previous_shape_normal": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "continue_because_not_expired",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "기한은 남았지만 새 용기 팽창이 보고되어 기한만으로 계속 사용하도록 안내하지 않고 보류해요."
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
표시 기한은 남았지만 이전에 없던 용기 팽창이 보고됐어요. 기한만으로 계속 사용해도 된다고 판단하지 않고 개별 루틴·제품 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
용기의 변화와 보관 이력, 제품 표시를 확인하고 제조·판매처에 처리 절차를 문의해요. 팽창 원인이나 내부 물질의 종류·농도를 추정하지 않아요.

## syn-hold-0025

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f0e6ae4dc4387440b51082c62b606b8ac127cae03f85b5bbfb621c3cce7e45cc`
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
        "synthetic_product": "합성 전 제품 회수 대상 선크림"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "synthetic_notice": true,
        "identity_match": true,
        "scope": "제조번호 구분 없이 해당 제품 전체",
        "instructs_stop_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.batch": {
      "variable_id": "storage.batch",
      "state": "known",
      "value": {
        "readable": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "합성 회수 공지가 제조번호 구분 없는 해당 제품 전체를 대상으로 하며 제품 일치가 확인되어 개별 사용을 보류해요."
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
제공된 합성 회수 공지는 제조번호 구분 없이 해당 제품 전체를 대상으로 하고 제품 일치가 확인됐어요. 제조번호를 읽을 수 없더라도 대상에서 제외하지 않고 개별 사용·제품 권고는 보류해요 [kb:B-Q05@0.6.1].

### 필요한 다음 단계
합성 공지의 사용 중단 안내와 회수 범위에 맞는 절차를 확인해요. 제품 식별 정보와 공지 내용을 바탕으로 판매처 등에 문의하되, 다른 제품이나 브랜드 전체로 회수 범위를 넓히지 않아요.

## syn-hold-0026

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `905612ce70461d3f2eb8ba0f83064d6f0745f79186b21f0e8ec70bec4fb57e4d`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
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
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "severe_eye_pain": true,
        "vision_change": false,
        "direct_eye_exposure": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "switch_filter_to_solve_eye_pain",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "hold",
      "guidance": "반복 눈시림에 심한 눈 통증이 동반되어 필터 선택만으로 해결하는 개별 권고는 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
반복 눈시림에 심한 눈 통증이 동반됐어요. 시야 변화나 직접 눈 노출이 없다는 보고만으로 일반 루틴 문제로 축소하지 않고, 필터 변경을 포함한 개별 루틴·제품 권고는 보류해요 [kb:B-P06@0.6.1].

### 필요한 다음 단계
심한 눈 통증은 일반적인 제품 순위 조정 대신 신속한 전문 진료로 확인할 필요가 있어요. 증상 시작과 지속 양상, 관련 제품 정보를 의료진에게 전달해요. 특정 필터가 원인이라고 단정하지 않아요.

## syn-hold-0027

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `88cea88f14c86bf4a1beb2551d5ebe4a3ead40bf036ec76fbc73412b14d8248f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "storage.seal_integrity": {
      "variable_id": "storage.seal_integrity",
      "state": "known",
      "value": {
        "배송 때 내부 봉인 훼손": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.authenticity_concern": {
      "variable_id": "commerce.authenticity_concern",
      "state": "known",
      "value": {
        "구체적 품질 의심": true,
        "가품 확정": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.receipt_record": {
      "variable_id": "commerce.receipt_record",
      "state": "known",
      "value": {
        "주문 정보 확인 가능": true,
        "제품명과 제조번호 기록": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.end_of_use": {
      "variable_id": "commerce.end_of_use",
      "state": "known",
      "value": {
        "이미 사용 보류": true,
        "요청": "문의하기 전에 용기와 제조번호 표시를 모두 버려도 되는지",
        "공식 즉시 폐기 지시": false,
        "안전하게 미사용 보관 가능": true
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
      "card_id": "B-Q06",
      "status": "hold",
      "guidance": "구체적 품질 의심품을 사용 보류한 상태에서 문의에 필요한 식별 자료까지 버리려 해요. 개별 사용·제품 권고는 보류하고 안전하게 남길 수 있는 문의 정보와 공식 처리 절차를 먼저 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
배송 당시 내부 봉인 훼손이라는 구체적 품질 의심이 있어 이미 사용 보류한 상태예요. 현재 불편이 없어도 개별 사용·제품 권고는 보류하며, 이 정보만으로 가품이나 오염을 확정하지 않아요 [kb:B-Q06@0.6.1].

### 필요한 다음 단계
문의하기 전에 용기와 식별 정보를 모두 버리기보다 안전하게 남길 수 있는 제품명·제조번호 사진이나 주문 기록으로 판매처에 확인·반품·처리 절차를 문의해요. 자료 확보를 위해 위험한 물건을 보관하도록 강제하지 않으며, 공식 폐기 지시가 있다면 그 범위를 우선 확인해요. 피부에 발라 진위를 시험하는 방법은 제시하지 않아요.

## syn-hold-0028

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f2c3cafae94d89782181eb0c07f61f8b19ecccace52ae75d533532d0f99363e5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "내용": "세안제와 보습제를 같은 날 변경"
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
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "붓기와 통증이 계속됨"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_trial": {
          "products": "둘 중 하나씩",
          "purpose": "원인을 시험",
          "status": "희망"
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
      "guidance": "지속되는 붓기와 통증이 있어 재노출 시험이나 개별 루틴 설계를 보류해요. 어느 제품이 원인인지는 확정하지 않아요."
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
붓기와 통증이 계속되는 상황에서는 두 제품을 하나씩 다시 써 보는 시험과 개인별 루틴 결정을 미뤄요. 같은 날 세안제와 보습제를 바꿨다는 사실만으로 어느 쪽이 원인인지 구분할 수 없어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 반응을 의료진에게 확인받고, 두 제품을 바꾼 시점과 반응이 시작되어 이어진 경과를 알려 주세요. 확인되지 않은 원인이나 성분을 미리 결론내리지 않아요.

## syn-hold-0029

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `486ea7426481f3322703852ca56a92d51a64bb0f19571dbbff143a4ca4f94299`
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
        "내용": "의료기관에서 확인된 특정 알레르겐 가"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "내용": "합성 후보에 동일 알레르겐 가 포함 확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_adaptation_schedule": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "hold",
      "guidance": "확인된 개인 알레르겐과 후보 성분이 일치해 일반 국소 확인이나 적응 일정을 제공하지 않아요. 개인별 전문 확인을 우선해요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
의료기관에서 확인한 알레르겐 가가 후보에도 포함되어 있어 적응 일정을 제안하지 않아요. [kb:B-G11@0.6.1]

### 필요한 다음 단계
알레르겐과 후보 성분의 일치 자료를 가지고 담당 의료진에게 확인해 주세요. 작은 부위의 자가 확인으로 안전을 보증할 수 없어요.

## syn-hold-0030

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `5d76e2f89c0b2dc0641a70e219a06569b6d6273a264b94b6150cef62e8266fd0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "상처 부위는 지정된 진료 계획 외 새 화장품을 적용하지 말라는 현재 지시"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "진료 중인 얼굴 상처 부위",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_aha": {
          "body_site": "진료 중인 얼굴 상처",
          "question": "사용 일정"
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
      "guidance": "현재 상처 부위에 대한 진료 지시와 새 각질관리 일정 요청이 충돌해요. 해당 개별 권고를 보류하고 담당 의료진의 적용 범위를 확인해요."
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
진료 중인 얼굴 상처에는 지정된 계획 외 새 화장품을 쓰지 말라는 현재 지시가 있어요. 같은 곳에 AHA를 쓰는 일정은 안내하지 않고 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
담당 의료진에게 그 지시가 적용되는 부위와 새 제품의 사용 가능 여부를 확인해 주세요. 여기서 상처의 원인을 진단하거나 진료 계획을 바꾸지는 않아요.

## syn-hold-0031

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `396e2914b4d575c94ec05915ea42e2d9e95c0bf8a0592e60d9a7af81bdf2be01`
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
        "임의 강도 증가": true,
        "제품과 병용": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "repeated",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "기기 병용 때마다 통증 반복"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_device_combination": {
          "intensity": "더 강한 단계",
          "combination": "같은 병용",
          "status": "요청"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "기기 병용 때마다 통증이 반복되어 강도 증가나 해당 병용 설계를 보류해요. 제품 흡수율이나 통증 원인을 추정하지 않아요."
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
제품과 기기를 함께 쓸 때마다 통증이 반복됐다고 하셨으므로, 요청하신 더 강한 단계의 병용 설계는 미뤄요. 통증의 원인이나 제품 흡수율은 이 관찰만으로 알 수 없어요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
반복 통증이 있는 해당 병용은 중단하고 기기의 공개 지침과 현재 상태를 전문가에게 확인해 주세요. 다른 관리 전체에 대한 판단은 이 보류에 포함되지 않아요.

## syn-hold-0032

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `257e76855e993d7f0d2f1b6caab0e1a4a0c4414bd1f364d102af77e926c68113`
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
        "확인된 표시": "손에만 사용하는 합성 제품이에요."
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.label_warnings": {
      "variable_id": "product.label_warnings",
      "state": "known",
      "value": {
        "확인된 주의사항": "눈과 눈 주변에는 사용하지 않아요."
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "손에 사용하던 제품이 실제로 눈에 들어갔어요.",
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "현재 눈 통증이 있어요."
          },
          {
            "source_variable": "skin.pain",
            "statement": "심한 통증"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_eye_exposure_routine_or_product_supplement": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G16",
      "status": "exception",
      "guidance": "손 전용 제품의 실제 눈 노출과 현재 심한 통증이 확인되어 일반적인 표시 비교와 루틴 최적화 범위를 벗어나요. 개별 사용 지시를 보류하고 전문 확인 경로를 우선해요."
    },
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "심한 현재 통증을 다른 보습 제품이나 루틴으로 해결하는 개별 권고는 보류해요. 원인 진단이나 응급 처치 절차를 생성하지 않아요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-hand-only-c32",
      "version": "1.0",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 손 전용이며 눈과 눈 주변에는 사용하지 않아요.",
      "evidence_ref": "catalog:syn-hand-only-c32@1.0"
    }
  ],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G16@0.6.1",
    "kb:B-B01@0.6.1",
    "catalog:syn-hand-only-c32@1.0"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손 전용이며 눈과 눈 주변에 사용하지 않도록 표시된 합성 제품이 실제로 눈에 들어갔고, 현재 심한 통증이 있다고 확인했어요. 일반적인 표시 비교나 보습 루틴 조정으로 다룰 상황이 아니어서 개별 루틴·제품 권고를 보류해요. [catalog:syn-hand-only-c32@1.0] [kb:B-G16@0.6.1] [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 눈 노출과 심한 통증에 대해 지체 없이 의료기관의 도움을 요청해 주세요. 제품 이름과 버전, 표시 주의사항, 실제 접촉 부위와 증상 내용을 전달해 확인해요. 여기서는 원인이나 손상 정도를 진단하거나 응급 처치 절차를 만들어 안내하지 않아요.

## syn-hold-0033

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `d3cee326f97ba9ab3459b9f8bb54b29be2b665cdc67f2ee6d0840602bd4137f1`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "새 제품 국소 확인": "3일째",
        "현재 반응": "붉음과 가려움이 계속됨",
        "question": {
          "ten_days_completion": true,
          "continued_use_schedule": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "hold",
      "guidance": "국소 확인 중 지속 반응이 있어 확인 기간을 채우기 위한 재사용 일정은 보류해요. 열흘이라는 기간을 반응을 견뎌야 하는 의무로 만들지 않아요."
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

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 제품을 작은 부위에 확인한 지 3일째에도 붉음과 가려움이 이어져, 열흘을 채우기 위한 사용 일정은 보류해요 [kb:B-G11@0.6.1].

### 필요한 다음 단계
반응이 있는 해당 제품의 재사용을 멈추고 지속되는 반응을 의료진에게 확인받아 주세요. 이 정보만으로 알레르기라고 진단할 수 없어요.

## syn-hold-0034

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `1a180624b4bdef36d69877f48ef838665cf9016221c986e460c736858e472a91`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "내용": "면도 뒤 같은 부위에 출혈과 통증이 반복됨",
        "requested_shaving_schedule": {
          "frequency": "매일",
          "change": "날만 바꿈",
          "status": "요청"
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
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "reported_symptom_statements": [
          {
            "source_variable": "skin.current_discomfort",
            "statement": "지속 통증"
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
      "guidance": "반복 출혈과 지속 통증이 있어 매일 면도를 이어 가는 개별 설계는 보류해요. 날 교체만으로 해결된다고 보거나 질환을 진단하지 않아요."
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
면도 뒤 같은 부위에 출혈이 반복되고 통증도 지속된다고 하셨어요. 날만 바꿔 매일 계속하는 일정을 지금 설계하지 않아요. 도구 교체만으로 해결될지 확인되지 않았어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
반복된 출혈과 지속 통증의 경과를 의료진에게 알려 확인받아 주세요. 특정 질환이나 원인을 이 정보만으로 판단할 수 없어요.

## syn-hold-0035

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `e5ce2494c48242a946c2c3d7bd2f89ba18fc93e94bbc7c5603b2757f66f7bcfe`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "처방 피부 의약품",
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
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "용량 변경에 관한 새 지시 없음"
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
            "statement": "사용 중 새로운 통증이 계속됨"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "requested_prescription_dose_change": "half"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "처방 사용 중 지속 통증과 용량 변경 요청이 있어 루틴·용량 권고를 보류해요. 임의 감량이나 중단을 지시하지 않고 처방한 의료진 또는 약사에게 확인해요."
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
처방 피부 의약품 사용 중 새로운 통증이 계속되고 있어 절반으로 줄이는 용량을 제안하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
통증과 현재 처방 사용 상황을 처방 의료진이나 약사에게 알려 확인해 주세요. 새 용량 지시는 확인되지 않았으며 여기서 감량이나 중단을 결정하지 않아요.

## syn-sol-0046

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b10d347decbd29ddd411be70b4ef997eef38d9f7c0675257fba928d13eb32117`
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
        "report_a": "hot",
        "report_b": "lukewarm",
        "same_event": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "동일 세안에 뜨겁다는 기록과 미온수라는 기록이 충돌해 온도 차이를 확정하지 않아요."
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
같은 세안에 대해 뜨거운 물과 미온수라는 기록이 함께 있어 실제 온도 상태는 미상으로 남겨 두어요. 뜨거운 물 사용이라는 차이를 확정하지 않아요 [kb:B-C01@0.6.1].

### 근거 및 이유
일반 안내는 미온수 세안을 다루지만, 서로 충돌하는 기록 중 하나를 사실로 선택해 주지는 않아요 [ref:S03].

### 확인이 필요한 한계
그 세안에서 실제로 물을 어떻게 느꼈는지 기록을 다시 확인해야 해요. 정확한 온도 수치나 피부 영향은 이 입력으로 알 수 없어요.

## syn-sol-0047

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bd8d7e681c4e5851e7f9e42ce35171012c83fb2c8fd7c9e5b9c0aa7e36123e6a`
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
        "owns_cleansing_brush": true
      },
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
    "method.friction": {
      "variable_id": "method.friction",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "브러시 보유만 확인됐고 사용 여부와 마찰이 미상이므로 강한 마찰 차이를 만들지 않아요."
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
세안 브러시를 갖고 있다는 점만 확인됐어요. 실제 사용 여부와 마찰은 미상이므로 도구 사용이나 강한 마찰의 차이를 확정하지 않아요 [kb:B-C02@0.6.1].

### 근거 및 이유
일반적인 기본 방법은 손가락으로 부드럽게 씻는 것이지만, 브러시 보유가 곧 그 브러시로 세안했다는 뜻은 아니에요 [ref:S03] [kb:B-C02@0.6.1].

### 확인이 필요한 한계
최근 세안에 브러시를 실제로 썼는지, 썼다면 어떤 힘으로 문질렀는지 확인이 필요해요. 답이 없으면 강한 마찰이나 손상으로 채우지 않아요.

## syn-sol-0048

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `416d5702faae6e7bbf0e9b7ce622042b0a9037cadfd821c7be2aedd3806ba0f3`
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
        "face_wash_events_per_day": 3
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
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
      "guidance": "횟수만 알려졌고 제거 목적과 활동이 미상이므로 자동으로 과세안 판정하지 않아요."
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
하루 세 번 얼굴을 씻는다는 횟수는 확인됐지만, 각 세안의 목적과 반복 여부는 미상이에요. 횟수만으로 과세안이라고 판단하거나 일괄 감량하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
이 카드는 실제 제거 목적과 반복 세안을 함께 검토해요. 부드러운 세안이라는 일반 원칙도 횟수 하나만으로 개인의 차이를 확정하는 근거는 아니에요 [kb:B-C05@0.6.1] [ref:S03].

### 확인이 필요한 한계
각 세안에서 무엇을 씻어내려 했는지, 활동과 땀 등 맥락이 무엇인지, 같은 세안에서 되풀이했는지 확인이 필요해요. 현재 정보로 제거 필요성을 없다고 가정하지 않아요.

## syn-sol-0049

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `59ef8abc85f25103ac5ed6cd14f774e1f138131de020e18852ef683f1092b3e8`
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
        "moisturizer_used_after_wash": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.dryness": {
      "variable_id": "skin.dryness",
      "state": "known",
      "value": "mild",
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
      "guidance": "세정 뒤 보습한다는 기록은 있지만 물기와 지연 상태가 미상이므로 완전히 마른 뒤 도포한다고 추정하지 않아요."
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
세정 뒤 보습제를 쓰고 가벼운 건조가 있다는 점은 확인됐어요. 다만 바를 때의 물기와 세정 후 지연은 미상이어서 완전히 마른 뒤 바른다고 판단하지 않아요 [kb:B-M01@0.6.1].

### 근거 및 이유
일반 자료는 세정 후 보습 시점과 실제 사용 경험을 검토하는 안내예요. '세정 뒤'라는 기록만으로 구체적인 피부 물기나 지연 상태까지 알 수는 없어요 [ref:S04] [kb:B-M01@0.6.1].

### 확인이 필요한 한계
보습제를 바를 때 피부에 물기가 남았는지와 얼마나 기다렸는지 확인이 필요해요. 현재 건조의 원인을 도포 시점으로 단정하거나 임의의 분 단위 기준을 만들지 않아요.

## syn-sol-0050

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d455e44bfaf9c9c942d92f00595104b46072212bc762af3b1a2df265824c11c6`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "pump_count": 1
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
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "펌프 횟수만 확인됐고 실제 건조와 편안함이 미상이므로 충족이나 부족을 확정하지 않아요."
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
한 번 펌핑했다는 횟수만 확인됐고 대상 제품은 미상이에요. 건조와 편안함도 미상이므로 충분하거나 부족하다고 정하지 않고 증량·감량 판단도 미뤄요 [kb:B-M02@0.6.1].

### 근거 및 이유
보습량 판단에는 사용 뒤의 건조와 편안함을 함께 검토해요 [kb:B-M02@0.6.1]. 일반 자료는 모든 피부와 제품에 동일한 양을 정하지 않아요 [ref:S04].

### 확인이 필요한 한계
펌핑한 제품이 무엇인지와 사용 뒤 건조나 당김, 편안함을 확인해요. 한 번의 펌핑을 일정한 질량이나 개인에게 필요한 양으로 환산하지 않아요.

## syn-sol-0051

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6a7ada475f6216fe67cf023712820f145d71b941211cc9343ef8cfa81623d604`
- 사람 검수: **미검수**

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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "과거 운송 온도와 기간이 미확인이라 열 손상이나 현재 품질을 확정하지 않아요."
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
현재 햇빛을 피해 보관한다는 사실은 확인됐지만, 운송 중 온도와 기간은 미상이에요. 과거 열 손상이나 현재 품질을 확정하지 않아요 [kb:B-S01@0.6.1].

### 근거 및 이유
온도와 빛 등은 보관·품질 검토 요소이지만, 일반 자료가 개별 제품의 안정성 시험을 대신하지는 않아요 [ref:S06].

### 확인이 필요한 한계
제품의 표시 보관조건과 확인 가능한 운송 이력을 살펴볼 필요가 있어요. 과거 이력을 알 수 없다면 미상으로 유지하며, 현재 햇빛을 피한다는 이유만으로 과거 품질까지 보증하지 않아요.

## syn-sol-0052

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `e184386e2eceb65deac795fc43613491aa53c385f4020b825e28282bebb87b2a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.instance_id": {
      "variable_id": "storage.instance_id",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "두 용기 중 어느 것을 먼저 열었는지 미확인이라 하나의 개봉일을 둘 다에 적용하지 않아요."
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
같은 제품의 용기 A와 B가 있어도 용기별 식별자와 개봉일은 미상이에요. 한 용기의 개봉일을 다른 용기에 그대로 적용하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
사용 이력은 제품명뿐 아니라 개별 용기를 구분해 검토해야 해요. 보관 자료가 모든 제품에 공통 사용기한을 정해 주지는 않아요 [kb:B-S02@0.6.1] [ref:S06].

### 확인이 필요한 한계
용기별 표시와 확인 가능한 개봉 기록을 살펴봐요. 확인되지 않는 날짜는 미상으로 두고, 구매일을 개봉일로 바꾸거나 임의의 사용 가능 기간을 계산하지 않아요.

## syn-sol-0053

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `71bdb77608adac62af63e5783b63a2de323cc0807585b7c51eb35a844eabf9b8`
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
    "storage.container": {
      "variable_id": "storage.container",
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
      "card_id": "B-S03",
      "status": "unknown",
      "guidance": "소분 계획은 있으나 용기 적합성과 제조사 허용이 미상이므로 허용·오염을 모두 확정하지 않아요."
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
소분은 계획 단계이고 아직 하지 않았어요. 용기의 적합성과 제품의 소분 지침은 미상이므로 허용된다고 확정하거나 이미 오염됐다고 판단하지 않아요 [kb:B-S03@0.6.1].

### 근거 및 이유
소분 검토에는 용기와 제품 지침 확인이 필요해요. 깨끗한 손·용기를 관리하라는 일반 위생 안내만으로 모든 소분 용기가 적합하다고 볼 수는 없어요 [kb:B-S03@0.6.1] [ref:S27].

### 확인이 필요한 한계
계획을 실행하기 전에 해당 제품의 소분 허용 여부와 사용할 용기에 관한 지침을 확인해요. 지침을 알 수 없다면 적합성 판단을 미상으로 유지해요.

## syn-sol-0054

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ac94f38fe2c8ef620d519467e135c54db761e6a387284a4c92bbd7f17addeae2`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": "electric",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
    },
    "shaving.care": {
      "variable_id": "shaving.care",
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
      "guidance": "전기면도기 헤드의 지침과 상태가 미상이므로 수동 날 참고 횟수로 교체일을 생성하지 않아요."
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
전기면도기를 여섯 번 사용했다는 사실만으로 헤드 교체 시점을 정하지 않아요. 헤드 상태와 관리 정보가 미상이라 교체 필요 여부도 아직 판단하지 않아요 [kb:B-S06@0.6.1].

### 근거 및 이유
제공된 면도 자료의 사용 횟수 참고는 수동 면도날에 관한 것이에요. 이를 전기면도기 헤드의 교체 주기로 바꾸지 않아요 [ref:S23].

### 확인이 필요한 한계
해당 기기의 헤드 관리·교체 지침과 실제 상태를 확인해야 해요. 정보가 없다는 것을 손상 없음이나 교체 불필요로 대입하지 않아요.

## syn-sol-0072

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b67ba8ad52987b83cc2bb18ec67f1aac2995e38481fc8bbdf492c510fe057b21`
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
      "value": 50,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "synthetic_candidate": "표시 일부가 손상된 후보"
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
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
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
      "guidance": "SPF 50은 확인되며 UVA·UVB 보호와 내수성 표시는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "Professional sunscreen guidance discusses SPF 30 or higher, UVA and UVB coverage, water resistance and outdoor reapplication. Exposure conditions and non-product protection also matter. This is not a universal indoor reapplication schedule or a statement of Korean legal minimums.",
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
SPF 50은 확인됐지만 UVA·UVB 보호와 내수성 표시는 미상이에요. 기본 표시 조건을 모두 충족했다거나 충족하지 못했다고 확정하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
일반적인 야외용 선택 안내는 SPF뿐 아니라 UVA·UVB 보호와 내수성도 함께 다뤄요 [ref:S16].

### 확인이 필요한 한계
현재 버전의 읽을 수 있는 포장 표시나 공식 자료로 빠진 항목을 확인해요. 손상된 표시를 근거로 보호 성능이나 안전성을 추정하지 않아요.

## syn-sol-0073

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d831065fa4ce860518cb54f6a8a6a220094b333f983be25d3f718c3a3b5198c8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "continued_after_towel": true
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
      "guidance": "수건 접촉 뒤 야외 노출은 이어졌지만 다시 발랐는지 확인되지 않아 미실시 차이로 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
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
수건에 접촉한 뒤에도 야외에 있었지만, 그 뒤 다시 발랐는지는 알려지지 않았어요. 재도포를 빠뜨렸다고 판단하지 않고 미상으로 남겨요 [kb:B-P03@0.6.1].

### 근거 및 이유
야외 노출이 이어지거나 닦임이 있을 때에는 재도포와 제품 지침을 함께 살피지만, 실제로 다시 바르지 않았는지 확인되지 않으면 행동 차이로 확정하지 않아요 [kb:B-P03@0.6.1]. 제공된 일반 안내는 물과 땀, 야외 노출과 그늘·의복을 함께 고려해요 [ref:S05].

### 확인이 필요한 한계
기억나는 범위에서 수건 접촉 후 재도포 여부와 사용 제품의 지침을 확인할 수 있어요. 기억나지 않으면 미상이며 개인이 받은 자외선량이나 보호량은 이 정보로 계산할 수 없어요.

## syn-sol-0074

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fff35d4f00bd11cca5d04d75b46947004a3bdc955ac4130d717c6bbc1db0f515`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.removal_claim": {
      "variable_id": "product.removal_claim",
      "state": "known",
      "value": {
        "label_condition": "special",
        "label_text": "특정 세정 조건에서 제거 확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleansing_method": "milk"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "합성 후보의 제거 표시는 특정 세정 조건만 언급하고 실제 조건은 없어 현재 밀크 세안과 일치하는지 미상이에요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-74",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 특정 세정 조건에서 제거를 확인했어요. 조건과 구체적 제거 지시는 이 자료에 없어요.",
      "evidence_ref": "catalog:syn-add100-b-74@v1"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "A small imaging study compared removal of selected sunscreen formulations using water, facial cleanser and cleansing oil. Findings are limited to the tested product-method combinations and do not establish mandatory double cleansing for all water-resistant sunscreens.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "catalog:syn-add100-b-74@v1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시에 특정 세정 조건에서 제거를 확인했다고만 적혀 있어, 현재 밀크 세안과 그 조건이 맞는지는 미상이에요. 밀크로 충분하다거나 부족하다고 단정하지 않아요 [kb:B-I01@0.6.1] [catalog:syn-add100-b-74@v1].

### 근거 및 이유
제한된 제거 연구도 시험한 제품과 방법의 조합에 한정돼요. 다른 조합의 제거 성능이나 필요한 단계를 자동으로 확정할 수는 없어요 [ref:S08].

### 확인이 필요한 한계
해당 버전의 구체적인 제거 지시를 공개 표시나 공식 안내에서 확인해요. 조건을 모른다는 이유만으로 오일이나 추가 세안 단계를 임의로 정하지 않아요.

## syn-sol-0075

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `0a6c2c2627649dcc5e120f0bc9c910c36fce19735f562c1cb7e936953b0024f1`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "convert_foreign_uva_label",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "displayed_pa": "PA+++",
        "uva_pf_not_disclosed": true
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
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "exception",
      "guidance": "해외 표시 PA+++를 정확한 UVA-PF 수치로 자동 환산할 확인 근거가 없어 해당 환산을 하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "SPF 30 이상, UVA와 UVB 보호, 내수성과 야외 재도포를 다루는 전문기관 안내예요. 실제 노출과 물·땀, 비제품 보호수단도 함께 검토해요. 한국의 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙을 정하는 자료는 아니에요.",
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
PA+++ 표시는 확인됐지만 정확한 UVA-PF 수치로 자동 환산하지 않아요. 수치가 공개되지 않은 상태는 그대로 남겨요 [kb:B-P01@0.6.1].

### 근거 및 이유
제공된 일반 선택 안내는 SPF와 UVA·UVB 보호, 내수성을 검토하지만 국가별 표시의 정확한 수치 등가성을 제공하지는 않아요 [ref:S16].

### 확인이 필요한 한계
SPF와 내수성도 미상이에요. 해당 제품과 국가 표시 체계에 맞는 확인 자료 없이 수치나 기본 조건 충족 여부를 만들어내지 않아요.

## syn-sol-0076

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3ea2bf42d6faf266cea8b589b58724948d5380e1ee5d73117765e827f22f5d96`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": "2026-10-01",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "printed_expiry": "2027-06-30",
        "label_expired": false
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
    },
    "storage.pao": {
      "variable_id": "storage.pao",
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
      "guidance": "개봉일과 인쇄 기한은 알지만 개봉 후 별도 사용 지침이 미확인이라 모든 기간 조건을 충족한다고 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S18",
      "text": "자외선차단제의 사용기한과 열 노출, 품질 변화 사례를 다루는 안내예요. 실제 제품의 표시와 보관 이력을 함께 확인해야 해요. 미국의 기한 규칙을 한국의 모든 제품에 적용하거나 정확한 SPF 감소율을 계산할 수는 없어요.",
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
개봉일은 2026년 10월 1일이고 인쇄 기한은 2027년 6월 30일로 확인됐어요. 다만 개봉 후 별도 지침이 미상이라 모든 기간 조건을 충족했다고 확정하지 않아요 [kb:B-P08@0.6.1].

### 근거 및 이유
기한과 보관 이력, 품질 변화는 함께 확인해야 해요. 인쇄 기한이 남았고 외관 변화가 없다는 사실만으로 전체 품질을 보증하지 않아요 [ref:S18].

### 확인이 필요한 한계
해당 버전의 개봉 후 사용 지침을 확인해요. 자료에 없는 개봉 후 사용 개월 수나 내부 안정성을 추정하지 않아요.

## syn-sol-0077

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `cad55219c8d0d4fcc2447340b5b10a0c8b68c97241a57d70a427fbb940766e41`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "reported": "한 펌프",
        "measured_mass_known": false
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
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
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
      "card_id": "B-P02",
      "status": "exception",
      "guidance": "한 펌프 사용이라는 보고만으로 토출 질량이나 얼굴 면적당 양을 정확히 계산할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
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
한 펌프를 썼다는 보고만으로 정확한 질량이나 얼굴 면적당 도포량을 계산할 수는 없어요. 충분하거나 부족하다고 수치 판정을 내리지 않아요 [kb:B-P02@0.6.1].

### 근거 및 이유
대략적인 사용량 보고는 행동 확인에 활용할 수 있지만 제품별 환산 근거 없이 정확한 양으로 바꿀 수는 없어요. 일반 안내는 제품 표시와 노출 상황을 함께 검토해요 [kb:B-P02@0.6.1] [ref:S05].

### 확인이 필요한 한계
제품 지침과 누락 부위가 미상이에요. 표시 사용법과 실제 누락 여부를 필요한 범위에서 확인하되, 정확한 얼굴 면적 측정을 필수로 요구하지 않아요.

## syn-sol-0078

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `aefb4b5f4fefd63ec149f7e44594c6ebd3e69d642101ea38ecd7666a237fd126`
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
        "comfortable": false,
        "reported": "답답한 느낌"
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
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "premixed_in_palm": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
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
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "중첩의 답답함은 확인됐지만 선크림 도포나 재도포를 줄였는지는 몰라 행동 감소 차이는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "제한된 보습제와 자외선차단제 조합에서 도포 순서를 UV 반사 영상으로 살핀 연구예요. 관찰된 영상 결과는 실제 SPF나 야외 보호 성능을 보증하지 않아요. 각각 층으로 바른 결과를 손바닥에서 미리 섞는 행동에 그대로 적용할 수는 없어요.",
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
겹쳐 바를 때 답답함은 확인됐지만 그 때문에 선크림 도포나 재도포를 줄였는지는 미상이에요. 사용감과 실제 행동을 분리해서 확인해요 [kb:B-I02@0.6.1].

### 근거 및 이유
제한된 도포 순서 연구는 실제 SPF나 야외 보호 성능을 보증하지 않아요. 답답함만으로 보호 감소나 선크림 생략을 추정하지 않아요 [ref:S09].

### 확인이 필요한 한계
답답해서 실제 사용량이나 재도포가 달라졌는지 확인해요. 보습제 다음 선크림을 각각 바른 보고를 사전 혼합으로 해석하거나 순서 변경만으로 해결을 보장하지 않아요.

## syn-sol-0079

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a28e61318035f9d41ce158e8e24e5a87c1c2b5b4d78007b4a500ffaa84851188`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "compare_new_periocular_candidate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.prior_tolerated_products": {
      "variable_id": "sun.prior_tolerated_products",
      "state": "known",
      "value": {
        "candidate_has_not_been_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "no_current_ocular_symptoms": true,
        "direct_eye_exposure": false
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
      "guidance": "후보를 눈 주변에 써 본 경험이 없어 개인의 눈시림 여부는 미상이며 제형만으로 무자극을 보장하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "Sunscreen guidance considers product choice and avoiding runoff near the eyes. Sticks are one possible option, not a guarantee of no irritation for every person, and the guidance does not identify an individual's cause of eye symptoms.",
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
후보를 눈 주변에 써 본 경험이 없어 본인에게 눈시림이 생길지는 미상이에요. 현재 안구 증상이 없다는 사실과 새 후보의 개인 적합성은 구분해요 [kb:B-P06@0.6.1].

### 근거 및 이유
눈 주변 사용에서는 공개된 사용 지침과 실제 경험을 함께 살펴요. 특정 제형만으로 누구에게나 눈시림이 없다고 보장하지 않아요 [kb:B-P06@0.6.1].

### 확인이 필요한 한계
후보의 눈 주변 사용 제한과 확인 가능한 사용법을 살펴봐요. 비공개 제형이나 원시험 보고서가 없다는 이유로 모든 후보 비교를 중단하지 않아요.

## syn-sol-0097

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `347823cbb83069c3ae78437cd278c16b1cda694b801b21580858a04030dc2022`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "새 로션 후보 비교",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.form_descriptor": {
      "variable_id": "product.form_descriptor",
      "state": "known",
      "value": {
        "내용": "향이 거의 없다는 광고"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "무향료 선호"
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
    },
    "product.inci": {
      "variable_id": "product.inci",
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
      "guidance": "향이 약하다는 광고만 있고 향료와 전성분 자료는 미확인이에요. 무향료 후보로 확정하지 않고 해당 제품 정보를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic allergen guidance discusses fragrance and individual avoidance, labeling and manufacturer instructions. Fragrance presence alone does not establish irritation or allergy in every person. United States labeling explanations are not automatically Korean legal requirements.",
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

### 응답 초안 — 미승인

### 핵심 안내
향이 거의 없다는 광고만으로 무향료 후보라고 확정하지 않아요. 향료와 전성분 정보는 미상이에요 [kb:B-G01@0.6.1].

### 근거 및 이유
일반 자료는 개인별 회피와 제품 정보 확인을 다뤄요 [ref:S15].

### 확인이 필요한 한계
현재 버전의 전성분이나 제조사 향료 정보를 확인해요. 자료가 없다는 이유로 사용자에게 잘못이 있다고 보지 않아요.

## syn-sol-0098

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `905a48d044c8a261ec951acee761df7cd0461326104320327403bf1dbc669d8f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "향성 에센셜오일을 피하고 싶은 새 보습제 선택",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.form_descriptor": {
      "variable_id": "product.form_descriptor",
      "state": "known",
      "value": {
        "내용": "식물 오일 로션"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "향성 에센셜오일은 피하고 싶음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.essential_oils": {
      "variable_id": "product.essential_oils",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "product.inci": {
      "variable_id": "product.inci",
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
      "guidance": "식물 오일이라는 이름만으로 고정유인지 향성 에센셜오일인지 알 수 없어요. 실제 성분과 용도를 확인하기 전에는 해당 차이를 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "화장품의 향료 등 알레르겐과 개인별 회피, 표시 및 제조사 지시 확인을 다루는 안내예요. 향료가 있다는 사실만으로 모든 사람에게 자극이나 알레르기가 생긴다고 단정하지 않아요. 미국 표시 설명을 한국의 법적 의무로 자동 전환하지 않아요.",
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

### 응답 초안 — 미승인

### 핵심 안내
식물 오일 로션이라는 이름만으로 향성 에센셜오일 포함 여부를 확정하지 않아요. 확인된 회피 선호에 맞는지 실제 성분과 용도를 확인해요 [kb:B-G01@0.6.1].

### 근거 및 이유
일반 자료는 개인별 회피와 제품 정보 확인을 다뤄요 [ref:S15].

### 확인이 필요한 한계
전성분과 향성 에센셜오일 정보가 미확인이므로 후보를 적합 또는 부적합으로 확정하지 않아요.

## syn-sol-0099

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f14934fb4812774b27994d41487003d24272b355c55bca8e14fa83e5fd6062d9`
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
        "새 후보의 확인된 이름": "Citric Acid"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "기존 제품": "레티놀 관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "기존 제품 실제 사용": "얼굴",
        "새 후보": "아직 도입 전"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.roles": {
      "variable_id": "product.roles",
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
      "guidance": "시트릭애씨드라는 성분명만으로 새 후보가 AHA 각질관리 제품인지 확정할 수 없어요. 기존 레티놀 사용과 구분하여 새 후보의 관리 목적을 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "General exfoliation guidance cautions about adding exfoliation while using retinol or prescription retinoids. Actual care purpose and contact site matter. This guidance does not establish a universal contraindication or an individual probability of harm.",
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
새 후보에 Citric Acid가 표시돼도 AHA 각질관리 목적의 제품인지는 미상이에요. 기존 레티놀 사용과 후보의 실제 역할을 나눠 확인해요 [kb:B-G13@0.6.1].

### 근거 및 이유
추가 각질관리의 목적과 접촉 부위를 검토하는 일반 안내가 있어요 [ref:S32]. 성분명만으로 관리 역할을 자동 생성하지 않는 것은 KB의 서비스 해석이에요 [kb:B-G13@0.6.1].

### 확인이 필요한 한계
후보는 아직 도입 전이에요. 이미 중첩 사용했다고 기록하지 않고 관리 목적과 지침을 확인하기 전에는 병용 일정을 만들지 않아요.

## syn-sol-0100

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `54de0dabe54778ff975434bb2a4cbd2de04c736cefe98477a2658b29d7326cc4`
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
        "후보 향수의 표기": "Benzyl Salicylate"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "known",
      "value": {
        "기존 제품": "레티노이드 관리"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "후보": "구매 검토 중",
        "기존 제품 실제 사용": "얼굴"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.roles": {
      "variable_id": "product.roles",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.body_site": {
      "variable_id": "method.body_site",
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
      "guidance": "벤질살리실레이트라는 문자열을 살리실릭애씨드 각질관리와 동일시하지 않아요. 후보의 실제 목적과 접촉 부위가 미확인이라 해당 중첩 차이는 확정하지 않아요."
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
    "kb:B-G14@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
Benzyl Salicylate 표기만으로 후보가 살리실릭애씨드 각질관리 제품이라고 판단하지 않아요. 후보 향수의 관리 역할과 접촉 부위는 미상이에요 [kb:B-G14@0.6.1].

### 근거 및 이유
레티노이드와 추가 각질관리 검토에는 실제 관리 목적과 부위를 구분하는 일반 안내가 있어요 [ref:S32]. 원료명과 실제 관리 목적을 구분하는 것은 KB 서비스 해석이에요 [kb:B-G14@0.6.1].

### 확인이 필요한 한계
구매 검토 단계이므로 실제 병용이나 위해를 확정하지 않으며 개인 적합성도 승인하지 않아요.

## syn-sol-0101

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e67f179ed653ad8cfba59e55833831343d5aaae4df6084424ecce120ac5b523a`
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
        "제품 가": "Retinyl Palmitate 표기",
        "제품 나": "Glycolic Acid 표기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "제품 수": 2,
        "도입": "두 후보 검토 단계"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.active_care_roles": {
      "variable_id": "product.active_care_roles",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "dose.co_use": {
      "variable_id": "dose.co_use",
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
      "guidance": "두 성분명은 확인됐지만 제품별 관리 목적과 실제 사용은 미확인이에요. 레티노이드와 AHA 각질관리의 실제 중첩으로 바로 판정하지 않아요."
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
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
두 성분명은 확인됐지만 후보별 관리 목적과 실제 사용은 미상이에요 [kb:B-G13@0.6.1].

### 근거 및 이유
레티놀 사용 중 추가 각질관리에 관한 일반 안내가 있어요 [ref:S32]. 실제 중첩 판정은 제품 역할과 사용을 함께 검토하는 KB 서비스 기준이에요 [kb:B-G13@0.6.1].

### 확인이 필요한 한계
후보별 용도와 실제 사용할 부위를 확인하기 전에는 차이나 개인 안전을 확정하지 않아요. 미공개 함량도 추정하지 않아요.

## syn-sol-0102

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6e4cd9a11b5d57a8b277e3360b0387f9713be96cefbf232934faa8cdc657e0de`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "필링이라는 이름의 합성 화장품",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "내용": "포장 사진의 사용법 부분이 잘림"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "그대로 두는지 헹구는지 결정",
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
      "guidance": "현재 제품의 접촉시간과 헹굼 지시를 읽을 수 없어요. 일반 세안제 지침을 대신 넣지 않고 해당 제품의 온전한 사용법을 확인해요."
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

### 핵심 안내
잘린 사진만으로 이 필링 제품을 헹굴지 그대로 둘지 결정하지 않아요. 현재 제품의 온전한 사용법을 먼저 확인해요. [kb:B-G03@0.6.1]

### 근거 및 이유
일반 세안제 방법을 팩·필링 등 다른 유형에 그대로 옮기지 않는 서비스 기준이에요. [kb:B-G03@0.6.1]

### 확인이 필요한 한계
제품별 접촉시간과 헹굼 지시는 미상이에요. 이름만으로 제품 유형의 세부 용법이나 분 단위 시간을 만들어 제공하지 않아요.

## syn-sol-0103

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3b3d50971a95646bd89fd44c3fc7e0a8f623bcc832d595817a287a8ad6fb5d4a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.form_descriptor": {
      "variable_id": "product.form_descriptor",
      "state": "known",
      "value": {
        "내용": "복합 원료 10%라는 문구"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "AHA 실제 농도 비교",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "내용": "개별 산의 함량은 제공되지 않음"
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
      "status": "unknown",
      "guidance": "복합 원료 비율과 개별 AHA 농도는 같지 않아요. 미공개 개별 농도를 계산하거나 10% AHA 제품으로 부르지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
복합 원료 10%라는 광고를 AHA 실제 농도 10%로 바꾸지 않아요. 개별 산의 농도는 현재 미상이에요. [kb:B-G02@0.6.1]

### 근거 및 이유
원료 혼합물의 배합 비율, 개별 성분 농도, 사용하는 양은 서로 다른 정보예요. 이를 구분하는 서비스 기준을 적용해요. [kb:B-G02@0.6.1]

### 확인이 필요한 한계
별도의 개별 함량 자료가 없으면 산의 농도를 역산하거나 두 제품의 강도를 수치로 서열화하지 않아요.

## syn-sol-0104

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fc6a0b9ed11672a6d6302943704b3b2bd9e6c8cb6301e079369abfe42e1432d7`
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
        "기록": "과거 제품 가에 대한 지시",
        "이번 후보": "다른 제품 나",
        "이번 후보에 적용 확인": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "제품 나의 개별 사용 일정 확인",
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
      "guidance": "과거 제품 가의 지시가 이번 제품 나에도 적용되는지는 확인되지 않았어요. 새 제품의 지침과 진료 계획의 적용 범위를 확인하기 전에는 일정을 만들지 않아요."
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

### 핵심 안내
과거 제품 가에 대한 진료 지시가 이번 제품 나에도 적용되는지는 아직 확인되지 않았어요. 새 제품 지침과 진료 계획의 적용 범위를 확인해요. [kb:B-G03@0.6.1]

### 근거 및 이유
일반 기준이나 다른 제품의 지시로 현재 제품의 개별 용법을 대체하지 않는 원칙이에요. [kb:B-G03@0.6.1]

### 확인이 필요한 한계
제품 나의 지침과 계획 적용 여부가 미상이라 새로운 사용 일정을 만들어 안내하지 않아요. 기존 진료 지시를 임의로 변경하는 뜻도 아니에요.

## syn-sol-0105

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8b1edcdc8be79343e4630d47c55fbe92a7ec3f03fb3cb92f2c9a6ac48eea5176`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "새 일반 보습 화장품",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "작은 부위 확인": "계획만 있음",
        "아직 사용 안 함": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "내용": "확인된 알레르기 없음"
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
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "국소 확인 의도는 있으나 실제 사용과 제품별 빈도는 미확인이에요. 아직 실행한 것으로 기록하거나 횟수를 임의 지정하지 않아요."
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
작은 부위 확인 계획은 실제 실행 기록과 구분해요. 제품별 지침과 빈도는 미상이에요 [kb:B-G11@0.6.1].

### 근거 및 이유
새 제품의 작은 부위 확인에 관한 일반 안내가 있어요 [ref:S35]. 제품별 용법을 우선하고 획일적인 빈도와 접촉시간을 적용하지 않는 것은 KB 서비스 정책이에요 [kb:B-G11@0.6.1].

### 확인이 필요한 한계
계획만으로 무반응을 확인했다고 보지 않아요. 자료를 확인하기 전에는 임의 횟수나 접촉시간을 지정하지 않으며 진단이나 영구 안전을 보증하지 않아요.

## syn-sol-0055

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `acacbff16dd7aa626c76e2508f9a553082c6f5ebb0e842cafcb620dbe2cf3c4d`
- 사람 검수: **미검수**

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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "exception",
      "guidance": "물 헹굼이 필요 없다는 제품 지시가 확인돼 일반 씻어내는 세안제와 구분해요."
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
      "evidence_ref": "ref:S10",
      "text": "세안 제품은 종류와 관계없이 반드시 물로 다시 씻어야 해요. 잠을 충분히 자더라도 예외는 없어요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/25266053/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "관찰적 집단 비교. 인종·성별·표본·수면 분류가 제한적. 수면 연장의 개인 피부 개선량을 추정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S10"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 제품에는 물 헹굼이 필요 없다는 지시가 확인됐어요. 물로 헹구지 않은 사실을 씻어내는 제품의 헹굼 생략과 구분하고 일괄적으로 추가 물세안을 요구하지 않아요 [kb:B-C06@0.6.1].

### 근거 및 이유
제품 유형과 지시를 확인해 필요한 헹굼을 검토해요 [kb:B-C06@0.6.1].

### 확인이 필요한 한계
이 예외는 확인된 제품 지시에 한정되며 다른 제품의 헹굼 필요 여부나 개인의 세정 결과를 보증하지 않아요.

## syn-sol-0056

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `7625172b730428832e2c1186abeade0bc03c4d2adfc833ddcd0f17a58b1f83c7`
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
        "category": "alkaline",
        "verified": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "review_existing_cleanser",
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
        "current_cleanser_tolerated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "exception",
      "guidance": "기존 제품을 문제없이 사용하고 교체 실익이 확인되지 않아 pH 선호만으로 즉시 교체하지 않아요."
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
현재 세정제의 알칼리성 분류가 확인됐지만 불편 없이 사용하고 있어요. 기존 제품 검토라는 맥락에서 pH 선호만으로 즉시 교체하거나 버리라고 하지 않아요 [kb:B-C04@0.6.1].

### 근거 및 이유
제공된 연구는 특정 세정제와 반복 전완 세정 조건에서 pH와 조성을 함께 살핀 자료예요. pH 하나만으로 완제품의 순함이나 모든 제품의 우열을 정하지 않아요 [ref:S07].

### 확인이 필요한 한계
알칼리성이라는 범주 외에 정확한 pH 수치는 주어지지 않았어요. 현재 잘 견딘다는 경험이 장기 안전성의 증명은 아니며, 이 정보로 교체 실익이나 임상 효과를 확정하지 않아요.

## syn-sol-0057

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b15a0206ef0ee6fee0a4117fc5e8b46df9fecb8b2c7c8e3bcc31cf5ce9d22750`
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
        "one_moisturizer_used": true
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
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        {
          "friend_claim": "수분·차폐·장벽 제품을 각각 사야 한다고 함"
        },
        {
          "own_goal": "현재 편안함 유지"
        }
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "aligned",
      "guidance": "본인은 보유 보습제로 편안하며 친구의 별도 세 단계 주장은 본인에게 필수가 아니에요."
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
본인은 보유 보습제 한 가지로 건조 없이 편안하고, 그 편안함을 유지하려고 해요. 친구의 말 때문에 수분·차폐·장벽용 제품을 각각 추가로 살 필요가 있다고 판단하지 않아요 [kb:B-M03@0.6.1].

### 근거 및 이유
이 카드에서는 실제 보습 경험과 충족 상태를 검토해요. 일반 보습 자료도 모든 사람에게 같은 양이나 제형을 일률적으로 정하지 않아요 [kb:B-M03@0.6.1] [ref:S04].

### 확인이 필요한 한계
현재 제품의 전성분이나 각 기능을 담당하는 성분은 제공되지 않았어요. 한 가지로 편안하다는 사실을 특정 성분 구성이나 장벽 회복 효과의 증거로 바꾸지 않아요.

## syn-sol-0058

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cdd0296127b6b2bcaed4e24548a6ec777b4f135e67388d2384b5818264b16e4e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "self_discomfort": false,
        "coworker_stinging": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "uses_tolerated_product": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.protection_hygiene": {
      "variable_id": "hand.protection_hygiene",
      "state": "known",
      "value": {
        "hygiene_maintained": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "aligned",
      "guidance": "동료의 따가움은 본인의 증상이 아니며 본인은 같은 제품에 불편이 없다고 명시했어요."
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
따가움을 말한 사람은 동료이고, 본인은 같은 제품에 불편이 없다고 명시했어요. 본인에게 잘 맞는 현재 보습과 필요한 손 위생을 유지할 수 있으며 동료의 경험 때문에 본인 권고를 보류하지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 관리 안내는 필요한 손 위생과 보습을 함께 다루며 개인마다 같은 반응을 보장하지 않아요. 동료의 반응을 본인의 증상으로 옮겨 판단하지 않아요 [ref:S21] [kb:B-M04@0.6.1].

### 확인이 필요한 한계
본인의 현재 무반응은 동료에게도 맞는다는 뜻이 아니에요. 동료의 따가움 원인이나 본인에게 앞으로 일어날 반응은 이 정보로 알 수 없어요.

## syn-sol-0059

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f67b00e6195efaa76295f92b3776eb606927cce261442339ba7e3b14d93111c4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.sharing_refill": {
      "variable_id": "storage.sharing_refill",
      "state": "known",
      "value": {
        "household_pump_shared": true,
        "skin_contact_with_nozzle": false,
        "contact_between_dispensed_portions": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "clean_hands": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "exception",
      "guidance": "서로 피부에 닿지 않는 펌프로 덜어 쓰며 접촉 경로가 없다는 확인을 직접 접촉 공유와 구분해요."
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
가정에서 펌프를 함께 쓰지만 피부가 노즐에 닿지 않고 덜어낸 내용물끼리도 접촉하지 않으며 손을 깨끗하게 관리한다고 했어요. 이 사용을 피부에 직접 닿는 제품의 공유와 구분해 검토해요 [kb:B-S07@0.6.1].

### 근거 및 이유
이 카드에서는 공유라는 이름뿐 아니라 실제 접촉 경로를 확인해요. 일반 위생 자료는 깨끗한 손·용기 관리와 표시 보관조건 준수를 다뤄요 [kb:B-S07@0.6.1] [ref:S27].

### 확인이 필요한 한계
확인된 접촉 경로가 없다는 것은 무균이나 모든 공유 방식의 안전성을 보장하지 않아요. 이 예외를 노즐이 피부에 닿는 경우까지 넓히지 않아요.

## syn-sol-0060

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `933d940e48c793f2fee0f04341d7e9d930bf76d7e5781f51e08c7d76357d0a07`
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
        "unwashed_finger_contact_once": true
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
      "guidance": "내용물에 씻지 않은 손이 닿은 취급은 검토하되 단일 접촉만으로 감염이나 폐기일을 계산하지 않아요."
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
씻지 않은 손가락이 내용물에 한 번 닿은 취급은 기본 관리와 차이가 있어요. 손과 용기를 깨끗하게 관리하고 표시의 취급·보관 지침을 확인해요 [kb:B-S03@0.6.1] [ref:S27].

### 근거 및 이유
제공된 위생 자료는 깨끗한 취급을 다루며 단일 접촉만으로 오염이나 감염을 확정하지 않아요 [ref:S27]. 입력상 물 유입과 색·냄새 변화, 층 분리는 없다고 보고됐어요.

### 확인이 필요한 한계
이상 징후가 없다는 관찰이 품질 인증은 아니에요. 감염 여부나 정확한 폐기일은 계산하지 않아요.

## syn-sol-0061

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b2619e9feec32d56183291b964dddcbfbb3b97609738a3453d7cf1f01c3b70f2`
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
        "water_only_events": 1,
        "cleanser_events": 1
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 1,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_repeat": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "morning": "물로 가볍게 씻기",
        "evening": "하루 활동 후 세정"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "aligned",
      "guidance": "아침 물세안과 저녁 한 번 세정제 사용의 목적이 확인됐고 한 세안의 다단계 반복과 구분해요."
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
아침에는 물로 가볍게 씻고 저녁에는 하루 활동 뒤 세정제를 한 단계로 사용하며 자동 반복은 없다고 확인됐어요. 이를 한 세안에서 세정제를 여러 단계로 반복하는 경우로 판단하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
세안 검토에서는 각 세안의 목적과 한 번의 세안 안에서 반복하는 단계를 구분해요. 현재 기록은 물세안 한 번과 세정제 사용 한 번이지, 세정제 두 단계 사용이 아니에요 [kb:B-C05@0.6.1].

### 확인이 필요한 한계
이 구분만으로 개별 제품의 제거 성능이나 모든 날의 세정 필요성을 입증하지는 않아요. 현재 정보를 근거로 남은 세정을 무조건 생략하라고 하지 않아요.

## syn-sol-0062

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b1dbad4ea2c7018036d1166f383fa324b9b58192a8b5b53aef6edcc2a54787aa`
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
    "moisturizing.dryness_return": {
      "variable_id": "moisturizing.dryness_return",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "deliberately_reduced": true
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
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "dryness_return_reported": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "difference",
      "guidance": "스스로 보습을 줄인 뒤 가벼운 건조가 남지만 지속 통증은 없으며 보유 제품의 실제 사용을 검토해요."
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
보습량을 의도적으로 줄였고 현재 가벼운 건조와 재건조 경험이 있다고 했어요. 통증과 따가움은 없으므로 보유 보습제의 실제 사용과 감량 여부를 함께 검토해요 [kb:B-M02@0.6.1].

### 근거 및 이유
건조가 있는데도 무조건 감량하기보다 실제 사용 경험과 편안함을 기준으로 조정을 검토할 수 있어요. 일반 건조 피부 안내도 개인별로 동일한 사용량이나 치료 효과를 정하지 않아요 [kb:B-M02@0.6.1] [ref:S04].

### 확인이 필요한 한계
건조가 다시 나타나기까지의 시간은 미상이에요. 감량이 건조의 원인이라고 확정하지 않으며, 현재·이전 사용량과 경험이 확인되기 전 특정 증량 수치나 개선율을 제시하지 않아요.

## syn-sol-0080

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4f540f4604d2032927d46dcae6303486c56cb0e2ffa12643f8096e57a6233db0`
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
        "self_repeated": false,
        "friend_reported": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.eye_symptom_context": {
      "variable_id": "skin.eye_symptom_context",
      "state": "known",
      "value": {
        "subject_of_stinging": "friend",
        "self_ocular_symptoms": false,
        "direct_eye_exposure": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.periocular_application": {
      "variable_id": "sun.periocular_application",
      "state": "known",
      "value": {
        "self_uses_label_consistent_method": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "aligned",
      "guidance": "눈시림을 겪은 사람은 친구이며 본인은 같은 조건에서 반복 눈시림이 없다고 확인되어 본인의 불편으로 전이하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S17",
      "text": "자외선차단제 선택과 눈 주변 사용 시 흘러듦을 줄이는 방법을 다루는 안내예요. 눈 주변 스틱은 선택지 중 하나이며 모든 스틱의 무자극을 보장하지 않아요. 특정 필터의 우월성이나 개인의 눈시림 원인을 확정하는 자료도 아니에요.",
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
눈시림을 겪었다는 사람은 친구이고, 본인은 반복 눈시림 없이 표시대로 사용한다고 확인됐어요. 친구의 경험을 본인의 불편으로 옮기지 않고 현재 확인된 행동은 유지해요 [kb:B-P06@0.6.1].

### 근거 및 이유
이 항목은 본인의 사용 조건과 반복 불편을 함께 살피는 기준이에요. 타인의 경험만으로 본인에게도 같은 반응이 있다고 판단하지 않아요 [kb:B-P06@0.6.1].

### 확인이 필요한 한계
현재 불편이 없다는 보고가 이후에도 무자극임을 보장하지는 않아요. 새로 반복 눈시림이 생기면 해당 제품과 방법을 다시 검토해요.

## syn-sol-0081

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `479feb35ca368880da5d1c575c6fd3e216dd494bfdf525cc22653ebe7998e18e`
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
        "self_follows_labeled_application": true,
        "coworker_omits_sunscreen": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "known",
      "value": [],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face",
        "neck"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "aligned",
      "guidance": "선크림을 생략한다는 발언은 동료의 경험이며 본인은 노출 얼굴과 목에 표시대로 바르고 누락이 없다고 확인했어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
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
본인은 노출되는 얼굴과 목에 표시대로 바르고 누락이 없다고 확인됐어요. 동료가 생략한다는 발언과 분리해 본인의 해당 도포 행동은 유지해요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 여부와 누락은 실제 본인의 보고를 기준으로 확인해요. 일반 광보호 안내도 제품 표시와 노출 상황을 함께 살펴요 [kb:B-P02@0.6.1] [ref:S05].

### 확인이 필요한 한계
행동이 기준과 맞는다는 판단이지 실제 SPF나 개인 보호 수준을 측정한 결과는 아니에요. 동료의 발언을 본인의 사용량 부족 근거로 삼지 않아요.

## syn-sol-0082

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2345087cf70ae39ebf6e7ddb3774d4e293b1e6988151c457ecb95e4997ccb897`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "commerce.purchase_purpose": {
      "variable_id": "commerce.purchase_purpose",
      "state": "known",
      "value": {
        "별도 목적": "직장 세면 공간에 보습제 한 통 비치",
        "집 제품 운반 어려움": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.inventory": {
      "variable_id": "commerce.inventory",
      "state": "known",
      "value": {
        "집 보습제": "개봉품 한 통",
        "직장 보유품": "없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.planned_start": {
      "variable_id": "commerce.planned_start",
      "state": "known",
      "value": {
        "예정": "다음 출근일부터 직장에서 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.budget": {
      "variable_id": "constraints.budget",
      "state": "known",
      "value": {
        "추가 한 통 비용 감당 가능": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.seller": {
      "variable_id": "commerce.seller",
      "state": "known",
      "value": {
        "브랜드 허가 판매자 목록과 실제 판매자 일치 확인": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q01",
      "status": "exception",
      "guidance": "직장 비치라는 별도 사용 목적과 시작 계획이 확인되어 집에 같은 기능 제품이 있다는 이유만으로 불필요한 중복 구매로 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S36",
      "text": "브랜드의 허가 판매자 목록과 실제 판매자를 대조하도록 안내하는 자료예요. 의심되는 제품은 사용하지 않고 공급자에 문의하도록 안내해요. 판매 경로 확인은 개별 제품의 품질이나 개인 적합성 보증과는 다른 판단이에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.hpra.ie/safety-information/how-we-monitor-safety/cosmetics/how-we-monitor-the-safety-of-cosmetic-products/tips-on-how-to-spot-counterfeit-cosmetics",
      "locator": "신뢰 가능한 판매자·브랜드의 허가 판매자 목록 확인; 의심 제품 사용하지 않고 공급자에 문의",
      "checked_on": "2026-11-05",
      "limitations": "EU 주소·신고 연락처를 한국의 필수 표시/국내 신고처로 옮기지 않음. 플랫폼 화이트리스트 보증 근거 아님."
    },
    {
      "evidence_ref": "ref:S12",
      "text": "특정 식이 중재의 결과가 제시되어 있어요. 이를 근거로 집에 보습제가 있으면 직장용 한 통도 피부에 해롭다고 주장해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.medicaljournals.se/acta/content/abstract/10.2340/00015555-1346",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "특정 질환·식이패턴·기간의 소규모 연구. 한 번의 음식 섭취와 다음날 증상을 연결하거나 모든 피부 건조·민감 반응에 확장하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-Q01@0.6.1",
    "ref:S36"
  ],
  "distractor_refs": [
    "ref:S12"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
집의 보습제를 운반하기 어려워 직장 세면 공간에 한 통을 따로 비치하려는 목적과 다음 출근일부터 쓸 계획이 확인됐어요. 같은 기능의 제품을 집에 갖고 있다는 사실만으로 불필요한 중복 구매라고 판정하지 않아요 [kb:B-Q01@0.6.1].

### 근거 및 이유
이 기준은 제품 수만 세기보다 별도 사용 목적·보유 재고·시작 계획과 비용을 함께 검토해요. 추가 한 통의 비용을 감당할 수 있다는 관찰도 있어요 [kb:B-Q01@0.6.1]. 브랜드 허가 판매자 목록과 실제 판매자의 일치를 확인했다는 관찰은 판매 경로 확인에 해당하지만, 제품 품질 전체를 보증하는 것은 아니에요 [ref:S36].

### 확인이 필요한 한계
실제 소진량이나 남은 제품의 사용 가능 기간은 계산할 정보가 없어요. 별도 목적이 있다는 사실을 임상 효과나 개인 적합성의 증거로 바꾸지 않으며, 이 자료로 구매 자체가 피부에 해롭다고 단정하지 않아요.

## syn-sol-0083

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9a64460be52b6ddf571d3916ce76f4ae333a85c5d846ce380b9da701003555ae`
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
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "follows_label": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "follows_label": true
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
    },
    "storage.pao": {
      "variable_id": "storage.pao",
      "state": "known",
      "value": {
        "within_labeled_period": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "aligned",
      "guidance": "확인된 기한과 보관 이력은 표시와 맞고 새로운 외관 변화는 없지만 이를 내부 안정성 인증으로 보지는 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-protection guidance considers labeled sunscreen use, outdoor exposure, water, sweat, shade and clothing together. It does not calculate an individual's received ultraviolet dose or automatically impose a universal indoor schedule.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S10",
      "text": "수면 관련 관찰 자료가 소개되어 있어요. 충분히 잠든 날에는 보관한 선크림의 내부 품질도 완전히 정상이라고 판단할 수 있다고 주장해요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/25266053/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "관찰적 집단 비교. 인종·성별·표본·수면 분류가 제한적. 수면 연장의 개인 피부 개선량을 추정하지 않음."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1",
    "ref:S05"
  ],
  "distractor_refs": [
    "ref:S10"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 사용기한·개봉 후 기간과 보관 이력이 표시에 맞고 새 외관 변화가 없어요. 해당 관리 행동은 유지하되 내부 품질 전체를 인증하지는 않아요 [kb:B-P08@0.6.1].

### 근거 및 이유
기한과 열·빛·공기 노출 등 보관 조건을 표시와 함께 살피는 기준이에요. 정상 외관은 관찰 사실이지 내부 안정성의 측정값이 아니에요 [kb:B-P08@0.6.1].

### 확인이 필요한 한계
현재 제품의 실제 SPF 유지율과 내부 안정성은 미측정이에요. 외관이나 관리 이력만으로 완전한 안전과 성능을 보증하지 않아요.

## syn-sol-0084

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `faf160abfaac062cae989ab5335927aa5bb6b10535e787224689a5ca26b5de0c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.removal_claim": {
      "variable_id": "product.removal_claim",
      "state": "known",
      "value": {
        "label_condition": "plain_water"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleansing_method": "water_rinse"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 1,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "aligned",
      "guidance": "현재 버전의 합성 제품은 물로 제거하도록 표시되어 있고 실제 방법도 물 헹굼으로 일치해요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-add100-b-84",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 물로 헹구어 제거해요. 추가 세정 단계는 지정하지 않아요.",
      "evidence_ref": "catalog:syn-add100-b-84@v1"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "20명을 대상으로 시험한 자외선차단제와 세정 방법의 제거 결과를 비교한 연구예요. 결과는 시험한 제품과 방법의 조합에 한정돼요. 모든 내수성 제품에 같은 제거 방법이나 이중세안이 필요하다는 결론은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 바르는 방법을 다뤄요. 얼굴 선크림도 종류와 관계없이 오일과 폼을 포함한 세 단계를 거쳐야 한다고 제안해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "catalog:syn-add100-b-84@v1",
    "ref:S08"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 합성 제품의 현재 버전은 물로 헹구어 제거하도록 표시되어 있고 실제 방법도 일치해요. 지정되지 않은 추가 단계를 자동으로 늘리지 않아요 [kb:B-I01@0.6.1] [catalog:syn-add100-b-84@v1].

### 근거 및 이유
제거 연구는 시험한 제품과 세정 방법의 조합에 한정되며 모든 선크림에 동일한 반복 세안을 요구하지 않아요 [ref:S08].

### 확인이 필요한 한계
물 헹굼 안내는 제공된 합성 제품의 표시 범위에 한정돼요. 모든 제품이 물만으로 제거된다거나 실제 잔류량이 0이라고 일반화하지 않아요.

## syn-sol-0085

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `290c567d28797fe2f93514f252236c3b3b1fdce48f3865f29d41d796b18d1352`
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
        "prolonged_outdoor_exposure": false,
        "context": "오늘은 실내 체류만 확인"
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
    "sun.sweat": {
      "variable_id": "sun.sweat",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": false,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "exception",
      "guidance": "오늘 확인된 것은 실내 체류이며 물·땀·닦임도 없어 야외 지속 노출의 두 시간 재도포 기준을 자동 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/drugs/understanding-over-counter-medicines/sunscreen-how-help-protect-your-skin-sun",
      "locator": "Sun Safety Tips / How do I apply sunscreen? / How do I store sunscreen?",
      "checked_on": "2026-11-04",
      "limitations": "미국 기관의 안내. 한국 법적 의무나 제품별 사용법으로 자동 전환하지 않음. 피부에 도달한 UV량을 개인별로 계산해 주는 자료가 아님."
    },
    {
      "evidence_ref": "ref:S23",
      "text": "습식 면도의 도구와 피부 접촉을 다루는 안내예요. 면도 시간표를 모든 실내 선크림 사용자에게 두 시간 간격 알림으로 적용하라고 제안해요.",
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

### 응답 초안 — 미승인

### 핵심 안내
오늘은 실내 체류만 확인됐고 물·땀·수건 접촉도 없어요. 야외 지속 노출의 두 시간 재도포 기준을 자동으로 실내 일정에 적용하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
일반 안내는 제품 표시와 실제 야외 노출, 물·땀 등 조건을 함께 검토해요. 하나의 시간표를 모든 환경에 일률적으로 적용하는 기준은 아니에요 [ref:S05].

### 확인이 필요한 한계
실내라는 이유만으로 자외선 노출이 전혀 없다고 확정하지는 않아요. 실제 노출 조건이나 제품 지침이 달라지면 필요한 재도포 안내도 다시 검토해요.

## syn-sol-0086

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `aca47f85ffb8ac320ffc127b86f45aa536a77fe1fad06f46dbe4f8d54e2d0a3c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "compare_imported_candidate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "label_language": "외국어",
        "translation_not_verified": true
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
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
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
      "guidance": "수입 후보의 표시 번역이 확인되지 않아 기본 표시 성능이 미상이며 독성이나 불법으로 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "SPF 30 이상, UVA와 UVB 보호, 내수성과 야외 재도포를 다루는 전문기관 안내예요. 실제 노출과 물·땀, 비제품 보호수단도 함께 검토해요. 한국의 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙을 정하는 자료는 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    },
    {
      "evidence_ref": "ref:S11",
      "text": "스트레스와 피부 상태에 대한 관찰 자료예요. 외국어 선크림 표시를 해석하기 어렵다는 이유만으로 해당 제품을 독성 제품으로 분류하라고 제안해요.",
      "scope": "non_clinical_only",
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/11511309/",
      "locator": "Abstract",
      "checked_on": "2026-11-04",
      "limitations": "급성 실험과 테이프 스트리핑 후 회복 지표. 만성 스트레스 점수로 개인 발진의 원인을 확정할 수 없음. 연구별 군/프로토콜을 분리."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S11"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
외국어 표시의 번역이 확인되지 않아 SPF, UVA 보호와 내수성은 미상이에요. 표시를 읽기 어렵다는 이유로 독성이나 불법 제품으로 판단하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
일반적인 선택 안내는 공개된 SPF와 UVA·UVB 보호, 내수성을 검토해요. 미국 전문기관의 선택 기준이 한국의 법적 최소치를 뜻하지는 않아요 [ref:S16].

### 확인이 필요한 한계
해당 후보의 정확한 버전과 신뢰할 수 있는 표시 번역을 확인해요. 미확인을 성능 부족이나 안전 보증으로 바꾸지 않아요.

## syn-sol-0087

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bfdd885ee51f5dcc3087fe63dfe68a0347a8dd132ff4af6949fbd482b23914a8`
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
    "constraints.burden": {
      "variable_id": "constraints.burden",
      "state": "known",
      "value": {
        "wide_brim_hat_conflicts_with_required_safety_helmet": true
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
      "status": "exception",
      "guidance": "필수 안전모 때문에 챙 넓은 모자가 어렵고 가능한 그늘 휴식을 활용하므로 불가능한 수단을 강제하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S14",
      "text": "햇빛 노출에서 그늘과 의복, 선글라스와 제품 표시를 함께 검토하는 안내예요. 특정 약물의 중단이나 개인별 자외선 손상량을 계산하는 자료는 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/consumers/consumer-updates/tips-stay-safe-sun-sunscreen-sunglasses",
      "locator": "Sun damage / Read Sunscreen Labels / Risk Factors",
      "checked_on": "2026-11-04",
      "limitations": "미국의 표시 규정은 한국 규정과 분리. 관련 약물 유무 확인과 전문가 연결만 고려하며 약물 중단 권고에 쓰지 않음."
    },
    {
      "evidence_ref": "ref:S15",
      "text": "향료 표시와 개인별 회피를 설명해요. 향료가 적은 선크림을 쓴다면 작업용 안전모를 벗어도 된다고 주장해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1",
    "ref:S14"
  ],
  "distractor_refs": [
    "ref:S15"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
필수 안전모와 충돌하는 챙 넓은 모자를 강제하지 않아요. 이미 활용하는 그늘 휴식처럼 가능한 보완 수단은 유지해요 [kb:B-P04@0.6.1].

### 근거 및 이유
광보호는 제품 표시와 그늘·의복 등 실행 가능한 수단을 함께 살피는 안내예요. 작업상 제약은 고려해야 할 조건이에요 [ref:S14] [kb:B-P04@0.6.1].

### 확인이 필요한 한계
광보호를 이유로 필수 안전모를 벗도록 안내하지 않아요. 그늘 휴식만으로 실제 노출량이나 보호 수준을 확정할 수는 없어요.

## syn-sol-0088

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a6d7fd26104aebb33d3d94b7f2a3e459e4e1c18702489a660030da2484bd24f9`
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
        "plan_to_follow_label_tomorrow": true,
        "actual_application_not_reported": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "face",
        "neck"
      ],
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
      "guidance": "내일 표시대로 바르겠다는 계획만 있고 실제 도포 보고는 없어 이미 충분히 바른 상태로 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "자외선차단제의 표시 사용법과 야외 노출, 물과 땀, 그늘과 의복을 함께 검토하는 일반 안내예요. 개인이 실제로 받은 자외선량은 계산하지 않아요.",
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
내일 표시대로 바르겠다는 계획은 확인됐지만 실제 도포 보고는 없어요. 이미 충분히 발랐거나 얼굴·목을 빠짐없이 발랐다고 판단하지 않아요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 항목은 실제 사용과 누락 여부를 확인하는 기준이에요. 제품 표시와 노출 상황을 함께 살피되 계획을 실행 사실로 바꾸지 않아요 [kb:B-P02@0.6.1] [ref:S05].

### 확인이 필요한 한계
실제 사용 후 대략적인 사용량과 얼굴·목의 누락 여부를 필요한 범위에서 확인해요. 확인 전에는 해당 항목을 미상으로 남겨요.

## syn-sol-0106

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1703f7457a0d3adf7ea974c4983dc6d7af1fb6cd1175b1660d12511252c872b3`
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
        "제품 가": "레티놀 관리 화장품",
        "제품 나": "AHA 각질관리 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": true,
        "부위": "목 동일 부위",
        "같은 저녁 사용": true,
        "간격": "30분"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "별도 병용 계획 없음"
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
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "목의 같은 부위에 별도 제품을 실제 중첩해요. 30분 간격이 있다는 사실만으로 중첩 기본값의 차이가 사라지지는 않아요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "두 제품 사이에 30분을 두면 어떤 각질관리 조합도 개인에게 안전하다고 판단해요. 실제 사용 부위와 제품의 관리 목적은 확인하지 않아도 돼요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
입력상 목 같은 부위에 별도 레티놀과 AHA 관리 화장품을 겹쳐 쓰고 있어요. 30분 간격만으로 자동 적합으로 보지 않고 불필요한 중복을 줄이는 방향을 검토해요 [kb:B-G13@0.6.1].

### 근거 및 이유
레티놀 사용 중 추가 각질관리의 일반적인 주의가 있어요 [ref:S32]. 시간 분리만으로 적합을 자동 판정하지 않는 것은 KB의 보수적 서비스 기준이에요 [kb:B-G13@0.6.1].

### 확인이 필요한 한계
개인 위해확률이나 모든 조합의 절대 금기를 뜻하지 않아요. 필요한 보습·광보호까지 일괄 중단하도록 확대하지 않아요.

## syn-sol-0107

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `82276e0b6024fae7e1a7555b153d62cee219214d2f046be2020cc4daf92e4ae0`
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
        "내용": "글리콜릭애씨드가 다섯 번째라는 정보만 제공"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "순서만으로 실제 농도를 수치로 알고 싶음",
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
      "status": "unknown",
      "guidance": "전성분 순서만으로 개별 성분 농도를 계산할 수 없어요. 농도를 미상으로 유지하고 공개된 개별 함량 자료가 있는지 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "글리콜릭애씨드가 전성분 다섯 번째라면 농도를 정확히 5%로 확정해요. 별도 공개 자료 없이도 순서로 숫자를 계산해 답해요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
글리콜릭애씨드가 전성분 다섯 번째라는 사실만으로 농도를 숫자로 계산할 수는 없어요. 실제 함량은 미상으로 남겨요. [kb:B-G02@0.6.1]

### 근거 및 이유
농도와 사용량을 구분하고 미공개 수치를 만들지 않는 서비스 기준이에요. [kb:B-G02@0.6.1]

### 확인이 필요한 한계
공개된 개별 함량 자료가 있으면 그것을 확인하되, 순서에서 5%나 다른 숫자를 새로 만들지는 않아요.

## syn-sol-0108

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `c91afdf8fe08e9f65fa001238345fcb74c5822e68add99d1ff4f3f3ddbd732f3`
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
        "팔 국소 확인": 10,
        "팔의 관찰 결과": "불편 없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "이 결과로 눈꺼풀에도 영구 무자극인지 확인",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "일반 얼굴 보습 화장품",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "내용": "합성 표시: 눈 주변 사용을 피함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "팔의 열흘 국소 무반응이 눈꺼풀의 영구 무반응인지 질문했지만 이를 이미 확정했다고 볼 수 없어요. 눈 주변 회피 표시를 우선해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S35",
      "text": "General guidance describes trying a new skin-care product on a small area for seven to ten days. Product-specific directions still apply, including rinse-off directions. This is not a diagnostic allergy patch test or a guarantee of permanent safety.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/prevent-skin-problems/test-skin-care-products/",
      "locator": "작은 부위 사용 확인, 7–10일 관찰, 반응 시 씻어내고 재사용하지 않기, 의료 패치테스트와 구분",
      "checked_on": "2026-11-05",
      "limitations": "원문 일반 안내의 하루 2회/워시오프 5분을 모든 제품에 이식하지 않음. 개별 용법과 충돌 시 조건부 적용."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "팔에서 열흘간 반응이 없으면 눈꺼풀에서도 평생 알레르기나 자극이 없어요. 눈 주변 회피 표시보다 이 결과를 우선해요.",
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

### 응답 초안 — 미승인

### 핵심 안내
팔에서 열흘간 불편이 없었다고 눈꺼풀에서도 영구 무자극이라고 판단하지 않아요. 현재 확인된 눈 주변 회피 표시를 우선해요. [kb:B-G11@0.6.1]

### 근거 및 이유
작은 부위 확인은 새 제품 사용을 살피는 일반 절차이며 의료기관의 알레르기 진단이나 모든 부위의 안전 보증은 아니에요. [ref:S35]

### 확인이 필요한 한계
다른 부위로 결과를 확대하거나 눈 주변 사용법을 새로 제시하지 않아요. 무반응 관찰과 제품별 적용 범위는 별도로 남겨요.

## syn-sol-0109

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a57a39e9048b3c4ea3f0136819297b02d34a9d88ad1298e67d094c8f1794370f`
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
        "확인된 유상": "합성 제품의 스쿠알란",
        "향성 에센셜오일": "없음으로 확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "내용": "무향료 확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "내용": "향성 에센셜오일은 피하고 싶음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "유상 성분이라는 이유로 현재 보습제를 버릴지 검토",
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
      "card_id": "B-G01",
      "status": "exception",
      "guidance": "확인된 스쿠알란 유상과 향성 에센셜오일을 구분해요. 향성 오일 회피 선호를 모든 유상 보습제의 폐기 의무로 확대하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "화장품의 향료 등 알레르겐과 개인별 회피, 표시 및 제조사 지시 확인을 다루는 안내예요. 향료가 있다는 사실만으로 모든 사람에게 자극이나 알레르기가 생긴다고 단정하지 않아요. 미국 표시 설명을 한국의 법적 의무로 자동 전환하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "성분 이름이 오일이나 유상으로 분류되면 모두 향성 에센셜오일로 취급해요. 현재 편안하게 쓰는 보습제도 일괄 폐기해요.",
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

### 응답 초안 — 미승인

### 핵심 안내
입력상 스쿠알란 유상과 향성 에센셜오일 부재가 확인됐어요. 현재 불편 없이 쓰는 보습제를 유상 성분이라는 이유만으로 버릴 의무는 없어요 [kb:B-G01@0.6.1].

### 근거 및 이유
향성 오일 선택 기준을 모든 보습 유상의 금지로 확대하지 않는 것은 KB 서비스 정책이에요 [kb:B-G01@0.6.1]. 일반 알레르겐 안내도 향료 존재만으로 모든 사람의 반응을 확정하지 않아요 [ref:S15].

### 확인이 필요한 한계
확인된 무향료·향성 에센셜오일 부재는 제품 전체의 무해성 보증과 달라요.

## syn-sol-0110

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `05015b8b2003a7996b81120074218b0793584f4ec6ec6758ea7162b598a8b77f`
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
        "상품명": "합성 토너크림",
        "제품 ID": "syn-tonercream-c110",
        "버전": "1.0"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "얼굴 보습제",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.form_descriptor": {
      "variable_id": "product.form_descriptor",
      "state": "known",
      "value": {
        "확인된 성상": "반고형 크림"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "확인된 표시": "보습 단계에서 세럼 다음에 사용해요."
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "실제 순서": [
          "세안",
          "합성 토너크림",
          "세럼"
        ],
        "이유": "상품명에 토너가 있어 묽은 토너 단계로 판단했어요."
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
            "statement": "현재 불편 없음"
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "difference",
      "guidance": "상품명에 토너가 있다는 이유로 첫 단계에 쓰지만 확인된 용도는 반고형 얼굴 보습제이고 표시는 세럼 다음 사용이에요. 이름이 아니라 해당 제품의 확인된 용도와 순서를 구분해요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-tonercream-c110",
      "version": "1.0",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 제품 표시 예시: 상품명은 토너크림. 반고형 얼굴 보습제이며 세럼 다음의 보습 단계에서 사용해요.",
      "evidence_ref": "catalog:syn-tonercream-c110@1.0"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 무향료 핸드크림이나 연고형 보습제를 사용하는 일반 안내예요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1",
    "catalog:syn-tonercream-c110@1.0"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
합성 토너크림은 이름에 토너가 있지만, 확인된 용도는 반고형 얼굴 보습제이고 표시는 세럼 다음 사용이에요. 이름만 보고 세럼 앞의 묽은 토너 단계에 두었던 순서를 해당 제품 표시와 맞춰 검토해요. [kb:B-G08@0.6.1] [catalog:syn-tonercream-c110@1.0]

### 근거 및 이유
상품명과 실제 용도·성상·사용 순서는 구분해야 해요. 여기서는 확인된 제품별 표시를 따르는 것이며 모든 크림이나 토너에 같은 순서를 정하는 기준은 아니에요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
현재 불편이 없다는 관찰은 그대로 남겨요. 순서의 차이만으로 피부 손상이나 효과 저하를 확정하지 않으며, 보습제라는 용도나 반고형 성상으로 미공개 성분과 농도를 추정하지 않아요.

## syn-sol-0111

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1a7fdc08421b33de7a0c05ceb74d710cead148c4e7f5d84369b861dd8afc6712`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "일반 레티놀 화장품",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "내용": "특정 아다팔렌 의약품 설명서를 함께 가져옴"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "모든 레티놀 화장품의 법적 AHA 금기 여부",
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
      "guidance": "다른 의약품의 주의 문구를 일반 레티놀 화장품 전체의 법적 금기로 옮기지 않아요. 현재 제품 지침과 실제 병용은 미확인으로 남겨요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "특정 아다팔렌 의약품의 문구는 모든 레티놀 화장품에도 동일한 한국 법적 병용 금기로 적용돼요. 제품 유형은 구분하지 않아요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S33"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
특정 아다팔렌 의약품의 문구를 모든 레티놀 화장품의 한국 법적 AHA 금기로 옮기지 않아요. 현재 제품 지침과 실제 병용은 미상이에요. [kb:B-G13@0.6.1]

### 근거 및 이유
해당 자료는 특정 아다팔렌 0.3% 의약품의 환자 안내라는 범위가 있어요. 일반 화장품과 같은 제품으로 취급할 수는 없어요. [ref:S33]

### 확인이 필요한 한계
현재 화장품의 사용 지침과 관리 목적, 실제 병용 정보를 확인해야 해요. 이 자료만으로 처방을 바꾸거나 모든 제품 조합의 금지를 선언하지 않아요.

## syn-sol-0112

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fb3be88e4ae62ff463ba671001fd069eeb4d280de14ad2bb3f660bdb934c2ba1`
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
        "내용": "AHA·BHA 관리 목적의 단일 복합 완제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.combination_design": {
      "variable_id": "product.combination_design",
      "state": "known",
      "value": {
        "같은 제품 두 통": "동일 버전의 재구매 재고",
        "서로 다른 관리 제품": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용": "현재 한 통만 사용",
        "다른 통": "미개봉 재고"
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
      "card_id": "B-G15",
      "status": "exception",
      "guidance": "동일 완제품의 재고 두 통은 별도 AHA와 BHA 관리 제품 두 개의 실제 중첩이 아니에요. 복합 완제품은 제품별 검토로 분리하며 성분 함량이나 무자극을 보증하지 않아요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "같은 복합 완제품을 두 통 보유하면 별도 AHA와 BHA 제품을 동시에 쓰는 것으로 판정해요. 미개봉 재고도 실제 중첩 사용에 넣어요.",
      "scope": "non_clinical_only",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G15@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
입력상 같은 복합 완제품 한 통만 사용하고 다른 한 통은 미개봉 재고예요. 재고를 별도 관리 제품의 실제 중첩으로 세지 않아요 [kb:B-G15@0.6.1].

### 근거 및 이유
별도 제품의 같은 부위 중첩과 단일 복합 완제품의 제품별 검토는 KB에서 구분해요 [kb:B-G15@0.6.1].

### 확인이 필요한 한계
관리 목적만으로 성분 함량이나 무자극을 보증하지 않아요.

## syn-sol-0113

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d006d58f9370daf80a96b6133b2000d74ebd361c65aeba4b604434d15ec86be4`
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
        "내용": "판매 페이지에 fragrance 단어가 없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "내용": "개인에게 확인된 특정 알레르겐이 있음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "전성분 없이 해당 알레르겐 부재를 확정하고 싶음",
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
      "guidance": "판매 문구의 단어 부재는 특정 개인 알레르겐 부재의 증거가 아니에요. 정확한 알레르겐 이름과 현재 제품 전성분을 대조해야 하며 무향료 여부도 아직 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "화장품의 향료 등 알레르겐과 개인별 회피, 표시 및 제조사 지시 확인을 다루는 안내예요. 향료가 있다는 사실만으로 모든 사람에게 자극이나 알레르기가 생긴다고 단정하지 않아요. 미국 표시 설명을 한국의 법적 의무로 자동 전환하지 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "판매 페이지에 fragrance라는 단어가 없으면 모든 개인 알레르겐도 없다고 확정해요. 전성분 대조 없이 개인 안전을 보증해요.",
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

### 응답 초안 — 미승인

### 핵심 안내
판매 페이지에 fragrance라는 단어가 없다는 이유로 개인의 특정 알레르겐이 없다고 확정하지 않아요. 전성분과 향료 여부는 미상이에요 [kb:B-G01@0.6.1].

### 근거 및 이유
일반 자료는 개인별 회피와 제품 정보 확인을 다뤄요 [ref:S15]. 무향료 표기만으로 확인된 특정 알레르겐 문제가 해결되지는 않아요 [kb:B-G01@0.6.1].

### 확인이 필요한 한계
정확한 알레르겐 이름과 현재 제품 전성분의 대조가 필요해요. 단어 부재를 성분 부재나 개인 안전 승인으로 바꾸지 않아요.
