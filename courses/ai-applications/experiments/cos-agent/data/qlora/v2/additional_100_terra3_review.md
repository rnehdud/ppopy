# PPO-39 보완 — additional_100_terra3

`development_preview`, `production_enabled=false`, 합성 개발 후보이며 공식 인수·사람 승인이 아니에요.
원문 관찰을 정형 슬롯과 연결하고 사례별 설명을 보완했어요. 전체 판단과 과거 기록은 README 및 `ppo39_revisions.json`을 확인해요.
KB 판정은 비교 명세에 대한 작성 기록이며 엔진 실행이나 임상 결과가 아니에요. 저장 문헌 청크는 요약이며 외부 원전의 직접 인용이 아니에요.

## syn-sol-0285

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `dd456470a76abcc16d5011214831ce790a4186dc29bf06164f5e984bb6318583`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "second_step_reason": "얼굴 화장 제거",
        "automatic_repeat": false
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
    "cleansing.steps": {
      "variable_id": "cleansing.steps",
      "state": "known",
      "value": 2,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup_removal": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "aligned",
      "guidance": "화장 제거 목적이 확인돼 두 단계라는 수만으로 차이를 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
얼굴 화장을 지우기 위해 두 세정 단계를 사용했어요. 단계 수만으로 불필요한 반복이라고 판단하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
세정 단계를 살필 때는 메이크업 제거 같은 이유 없이 습관적으로 반복하는 경우를 비교해요 [kb:B-C05@0.6.1]. 제공된 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
두 단계의 구체적인 제품과 행동은 알려지지 않았고 이 자료가 개인의 세정 결과를 확정하지는 않아요.

## syn-sol-0286

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fe52b15716e4b8605b515d15c98ab8caa275ed94d4b75d8376f2c948c873cc9f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "self_face_friction": "strong",
        "other_person": "gentle"
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
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "거친 천"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "self_face": "strong",
        "other_person": "gentle_fingertips"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "다른 사람의 습관과 구분해 본인의 강한 마찰을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
친구의 부드러운 세안과 달리 본인은 얼굴을 거친 천으로 강하게 문지른다고 하셨어요. 강한 마찰을 줄이고 손으로 부드럽게 씻는 방법을 살펴봐요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
친구의 행동을 본인의 행동으로 옮기지 않으며 현재 피부 문제의 원인을 단정하지 않아요.

## syn-sol-0291

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `82f4f70d6ef6e205782671d2909a66f836804c8ef676e6c2a3b09b981c5b4a6b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "friction": "unknown",
        "pressure": "unknown",
        "device_intended_site": "face",
        "device_used": true,
        "face_device_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "cleansing_device"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "pressure": "unknown",
        "friction_intensity": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "얼굴에 손가락 외 기기를 사용하는 차이는 확인됐지만 압력이나 마찰의 세기는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
기록된 얼굴 세정 기기 사용을 손가락 외 도구 사용이라는 기준과 함께 살펴요. 압력과 마찰 강도는 확인되지 않았어요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 강도를 추정하거나 개인의 결과를 확정하지 않아요.

## syn-sol-0297

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `453c9074291e57f7edb06a20dd52d60f474d6061b74909b9ba65da6a07c35730`
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
        "moisturizer": "used",
        "aftershave": "not_used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "moisturizer": "comfortable"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "면도 후 견딜 수 있는 보습을 사용하며 별도 후처리 제품은 필수가 아니에요."
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
면도 뒤 편안한 보습을 유지할 수 있어요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 면도 관리 안내는 면도 후 보습을 다뤄요. [ref:S25] 별도 후처리 제품은 반드시 필요하지 않아요. [kb:B-M05@0.6.1]

### 확인이 필요한 한계
이 기록만으로 제품의 모든 안전성을 보장하지 않아요.

## syn-sol-0322

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `0e0e4f1a3cecc3ec42464e1465bf176549fea5fd9f4571f1a8613516295b3926`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 운동으로 심하게 땀을 흘린 뒤에도 한동안 야외에 있었고 재도포는 하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "발한 이후 노출이 이어진 상황을 반영해 재도포를 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
심하게 땀을 흘린 뒤에도 야외에 머무는 상황을 반영해 재도포를 고려해요. [kb:B-P03@0.6.1]

### 근거 및 이유
일반 선안전 안내는 땀을 흘린 뒤 재도포를 다뤄요. [ref:S05] [kb:B-P03@0.6.1]

### 확인이 필요한 한계
개인의 실제 노출량과 보호 수준은 측정되지 않았어요.

## syn-sol-0323

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6f62cce18fcb8c2d5fa9fc0f1cc0758ecd941b877912bfd96be89be3f83e67cc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "물놀이 후 옷을 갈아입고 야외에 더 머물렀어요. 물놀이 전 바른 선크림을 그 뒤 다시 바르지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "물 접촉 후에도 야외에 머문 점을 반영해 재도포를 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
물놀이 뒤에도 야외에 머무는 상황을 반영해 재도포를 고려해요. [kb:B-P03@0.6.1]

### 근거 및 이유
일반 선안전 안내는 수영 후 재도포를 다뤄요. [ref:S05] [kb:B-P03@0.6.1]

### 확인이 필요한 한계
옷을 갈아입은 사실만으로 모든 부위의 도포 상태를 알 수 없어요.

## syn-sol-0324

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `29136bbc0041c2137f228a49ff68ac9d028af46001ab23db4c3c54975b313ecb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "실외 근무가 길게 이어졌고 점심 휴식도 야외에서 보냈어요. 아침 이후 재도포는 하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "지속된 야외 노출에 맞춰 재도포할 기회를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
길게 이어진 야외 근무에 맞춰 재도포할 기회를 검토해요. [kb:B-P03@0.6.1]

### 근거 및 이유
일반 선안전 안내는 지속적인 노출 중 재도포를 다뤄요. [ref:S05] [kb:B-P03@0.6.1]

### 확인이 필요한 한계
휴식 기록만으로 실제 보호 수준을 계산할 수 없어요.

## syn-sol-0325

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6ab5da6e62e4f636bd816ccb147538549cdb627eac531ede00b437d65f200169`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외행사에서 얼굴의 땀을 손으로 자주 닦았고 이후에도 야외에 머물렀어요. 재도포는 하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "difference",
      "guidance": "닦임과 이어지는 노출을 반영해 재도포를 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
땀을 닦은 뒤에도 야외에 머무는 상황을 반영해 재도포를 고려해요. [kb:B-P03@0.6.1]

### 근거 및 이유
지속적인 야외 노출과 땀에 맞춘 재도포를 살펴봐요. [ref:S05] [kb:B-P03@0.6.1]

### 확인이 필요한 한계
손으로 닦아 제품이 얼마나 제거됐는지는 알 수 없어요.

## syn-sol-0326

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `65f14ff89c5c6a385bdfc72ff06f52a045ac5eece1930bf88d5db32308603123`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "긴 야외 대기에서 선크림만 있으면 충분하다고 생각해 바로 옆 차양 아래 대기를 일부러 피했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "difference",
      "guidance": "가능한 차양을 함께 활용하는 방안을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
긴 야외 대기 중 이용할 수 있는 차양을 함께 활용해요. [kb:B-P04@0.6.1]

### 근거 및 이유
선크림 외에 그늘을 활용하는 방법도 광보호 안내에 포함돼요. [ref:S05] [kb:B-P04@0.6.1]

### 확인이 필요한 한계
그늘 이용만으로 개인의 실제 노출량을 계산할 수는 없어요.

## syn-sol-0327

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e94652ae0e7791434ec79eb4a2a721a39d6e9d672fc9097bfb6fe9e58ad08320`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 관람이 오래 이어지고 얇은 긴소매를 입을 수 있지만 선크림만 있으면 된다며 보완 수단을 모두 제외했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "difference",
      "guidance": "가능한 의복을 광보호에 함께 활용하는 방안을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "Sun-safety guidance advises reapplying sunscreen at least every two hours and more often after swimming or sweating. It also discusses using shade and protective clothing as complementary measures.",
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
야외 관람 중 가능한 긴소매를 함께 활용하는 방안을 검토해요. [kb:B-P04@0.6.1]

### 근거 및 이유
선크림 외 의복도 보완 수단으로 살펴볼 수 있어요. [ref:S05] [kb:B-P04@0.6.1]

### 확인이 필요한 한계
이 기록만으로 보호 수준을 확정할 수는 없어요.

## syn-sol-0328

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9118e07af8a6586c612635aa7375968a62df319c6dfde17debba29dc266ce573`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림의 표시에는 보관 중 두 층이 생겨 사용 전에 흔들라고 적혀 있어요. 이 제품은 그 안내대로 두 층이 생겼고 새 냄새나 색 변화는 없어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "exception",
      "guidance": "표시된 정상 분리를 곧바로 품질 이상으로 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시된 정상 이층을 곧바로 변질로 판단하지 않아요. [kb:B-P08@0.6.1]

### 근거 및 이유
해당 제품에 흔들어 사용하라는 정상 분리 안내가 확인됐어요. [kb:B-P08@0.6.1]

### 확인이 필요한 한계
이 관찰은 내부 안정성이나 실제 SPF의 인증이 아니에요.

## syn-sol-0329

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `428a890970626b4b5f2cfef02cdeedf4d6e1630cb360208cfbf794ce44a09c93`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림을 최근 구입했지만 용기에 표시된 사용기한은 이미 지났어요. 새 냄새나 색 변화는 보고되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "difference",
      "guidance": "구매가 최근이어도 표시 기한이 지난 선크림은 사용하지 않는 방향으로 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시 기한이 지난 선크림은 사용하지 않는 방향으로 확인해요. [kb:B-P08@0.6.1]

### 근거 및 이유
최근 구입한 사실과 용기의 표시 기한은 서로 다른 정보예요. [kb:B-P08@0.6.1]

### 확인이 필요한 한계
새 냄새나 색 변화가 없어도 현재 품질이 보증되지는 않아요.

## syn-sol-0333

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5d4de8682ce597de43a7b41d212ef026374311580dae0241fd6dfe9cc4b9ddf0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "선크림의 보관 지시 글자는 가려져 있어요. 하지만 며칠 동안 뜨거운 자동차 안에 계속 둔 사실은 확인됐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "과도한 열을 피하는 쪽으로 보관을 조정해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
뜨거운 차 안에 계속 두는 보관을 피하는 방향으로 조정해요. [kb:B-S01@0.6.1]

### 근거 및 이유
별도 표시를 읽지 못해도 확인된 과도한 열 노출은 보관 검토에 반영해요. [kb:B-S01@0.6.1]

### 확인이 필요한 한계
해당 제품의 별도 지침과 내부 안정성은 미상이에요.

## syn-sol-0336

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8df09e907aef3455b0713a40c4b783c0561d8cf1caee37154b40729a31bf11ac`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림이 뻑뻑하게 느껴져 원래 용기에 물을 넣었어요. 제조사의 희석 지시는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S03",
      "status": "difference",
      "guidance": "제조사 지시 없이 원제품에 물을 섞지 않는 방향을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제조사 지시 없이 원제품에 물을 섞는 행동을 중단하고 제품 정보를 확인해요. [kb:B-S03@0.6.1]

### 근거 및 이유
원래 용기에 임의로 물을 더한 취급은 별도로 검토할 차이예요. [kb:B-S03@0.6.1]

### 확인이 필요한 한계
섞인 제품의 실제 성능과 오염 여부는 미상이에요.

## syn-sol-0338

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `b250f0dcb08a04749f181053c7a34696968037eb2f6c5ac94e17126d1b34d47f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림은 얼굴과 귀에 사용할 수 있다고 표시돼 있어요. 야외에서 얼굴에는 바르지만 노출된 귀는 의도적으로 바르지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "표시된 사용 범위 안에서 노출된 귀의 누락을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴과 귀에 사용 가능하다는 합성 제품 표시가 있는데 야외에서 노출된 귀는 의도적으로 제외했다고 하셨어요. 표시된 범위 안에서 빠진 부위를 함께 검토해요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 범위를 살필 때는 실제 노출 부위를 의도적으로 빼거나 아주 적게 바르는 행동을 비교해요 [kb:B-P02@0.6.1]. 제품 표시의 사용 범위와 실제 행동을 구분해 살펴요.

### 확인이 필요한 한계
얼굴에 바른 양과 개인의 실제 보호 수준은 측정되지 않았어요.

## syn-hold-0084

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `8a981cd5e635987fb0c381055f6832d2de47e61bde624fe556ff010ea21b1446`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
        "event": "얼굴 세안",
        "after_event": "불편감과 통증 지속",
        "product": "기억하지 못함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
얼굴 세안 후 불편감과 통증이 계속되고 사용 제품도 기억나지 않는다고 하셨어요. 지금은 개별 루틴 결정을 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편과 그 경과를 의료진에게 확인받아 주세요. 제품과 원인은 확인되지 않았어요.

## syn-hold-0085

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `386a7f6f0d89b2b0915e43c14c1469be217450ac9bd9aab5887c517f2acafa6c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "손에 불편감이 계속되는데 얼굴 세안 단계 조정을 요청합니다.",
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.pain": {
      "variable_id": "skin.pain",
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
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
손의 불편감이 지속되는 상황이 확인됐어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0086

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9270cc1540cb931c2ef1d6c4e7916fba88cb0be1705284da9c31e49e5c1e9ab8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
    "skin.stinging": {
      "variable_id": "skin.stinging",
      "state": "known",
      "value": "moderate",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
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
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
얼굴의 따가움과 불편감이 지속되어 개별 루틴과 제품 안내는 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 제품 버전 답변은 원하지 않으셨으며 버전 값은 확인되지 않았어요. 원인은 단정하지 않아요.

## syn-hold-0087

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `1e72b3c3f8f3fdbf304df21b1cac7fccb3713bfc6c956511f996d378524ecd66`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
        "cleansing": {
          "body_site": "face",
          "timing_relative_to_discomfort": "before"
        },
        "cause_of_discomfort": "unknown",
        "pain_persistence": "persistent"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
얼굴 세정 뒤 불편감과 통증이 지속되어 개별 루틴과 제품 안내는 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인은 확인되지 않았어요.

## syn-hold-0088

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `5bf2494dad6d5c9a34f35b046e693f56d0465de37801d6aaa42391a797cf259a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
        "site": "face",
        "used": true,
        "after_use": "불편감과 통증 지속",
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
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
얼굴에 기기를 쓴 뒤 불편감과 통증이 계속된다고 하셨어요. 개별 루틴 결정은 지금 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
기기 사용과 반응의 경과를 의료진에게 알려 확인받아 주세요. 시간상 순서만으로 원인은 정할 수 없어요.

## syn-hold-0089

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `10429dd6de3f42ab83afcc710a3fd176877f558c397ca814e954d6d781aa5c4c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "hands",
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
        "friend_using_same_soap_has_discomfort": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
손의 불편감이 지속되고 있어요. 친구의 경험으로 본인 상태를 판단할 수 없어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0090

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `2b4e0c8f3de13d7808026d551efc40f51384d2f59c853821b60ee69a80cb1049`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
        "cleansing": {
          "status": "stopped",
          "discomfort_persisted_after_stopping": true
        },
        "product_causation": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
세안을 중단한 뒤에도 얼굴 불편감이 지속돼요. 원인은 확인되지 않았어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0091

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `8f1bfee774d153c154cea1e99e36c08911a8f7df27f9465d30ac85984744014e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
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
      "value": "face",
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
        "products_used_together": 2,
        "after_use": "통증과 불편감 지속",
        "cause_product": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "discomfort_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요."
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
두 제품을 함께 쓴 뒤 얼굴의 통증과 불편감이 계속되어 개별 루틴 판단은 미뤄요. 어느 제품이 원인인지는 알 수 없어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
함께 사용한 제품과 반응이 이어진 경과를 의료진에게 알려 확인받아 주세요.

## syn-hold-0092

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f5732a625874297a32146dad74d9d12e08e60884c1f7eaa33330f46a1fbd3c50`
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
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "site": "neck",
        "discomfort": "persistent"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "면도 부위의 지속 불편이 보고되어 개별 권고를 보류해요."
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
지속 불편이 확인되어 개별 루틴 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
상태와 기존 진료 계획을 전문가에게 확인해 주세요.

## syn-hold-0093

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9ea5b1de8cc2e949caa4ac1a3dbf3a4f3065aaca269ed7325a62cfdfaa923ce1`
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
    "skin.hand_observation": {
      "variable_id": "skin.hand_observation",
      "state": "known",
      "value": {
        "discomfort": "persistent"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "손의 지속 불편이 보고되어 개별 권고를 보류해요."
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
손의 지속 불편 때문에 개별 루틴 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태를 전문가에게 확인해 주세요.

## syn-hold-0094

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `118abffc263ed60d722b5bc09f7918048239129e57aa58aa9e330663f6cbb8c6`
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
        "moisturizer": "used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편과 통증이 보고되어 개별 권고를 보류해요."
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
지속 불편과 통증이 확인되어 개별 루틴 권고를 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태를 전문가에게 확인해 주세요.

## syn-hold-0095

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `7563749d2340caa07ef443cad44dc0dce2fa2516877700aa32073c4eb72be42a`
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
        "color_or_odor_change": true,
        "separation": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.roles": {
      "variable_id": "product.roles",
      "state": "known",
      "value": [
        "hand_moisturizer"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습제에서 이전에 없던 냄새 변화가 새로 확인되었어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 냄새 변화가 확인된 손 보습제 사용과 개별 안내를 보류해요."
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
새 냄새 변화가 확인되어 해당 제품 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
표시와 제품 상태를 확인하고 필요하면 제조사에 문의해 주세요.

## syn-hold-0096

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `5d87ef5a7d8cc0c0672eb5b93c11a8507e5a362cde7561b071451224dff4f8ac`
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
        "separation": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.roles": {
      "variable_id": "product.roles",
      "state": "known",
      "value": [
        "face_moisturizer"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 보습제에서 이전에 없던 층 분리가 생겼으며 흔들어 쓰는 정상 제형이라는 표시는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 층 분리가 확인된 얼굴 보습제 사용과 개별 안내를 보류해요."
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
새 층 분리가 확인되어 해당 제품 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
정상 제형 여부는 미상이므로 제품 표시와 상태를 확인하고 필요하면 제조사에 문의해 주세요.

## syn-hold-0097

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `83bda63ef8f4d68e4cc46218c12b1320d3e14cec603771557361c6395d171f42`
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
        "color_or_odor_change": true,
        "separation": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.aftercare": {
      "variable_id": "shaving.aftercare",
      "state": "known",
      "value": {
        "product": "aftercare"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "면도 후 제품에서 이전에 없던 색 변화가 새로 확인되었어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 색 변화가 확인된 면도 후 제품 사용과 개별 안내를 보류해요."
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
새 색 변화가 확인되어 해당 제품 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
제품 표시와 상태를 확인하고 필요하면 제조사에 문의해 주세요.

## syn-hold-0098

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f618ec32aff94b477c4d740bcbdeaf5a2ec36c903364de84fd9f3e85d0c5d496`
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
        "new_leakage": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.roles": {
      "variable_id": "product.roles",
      "state": "known",
      "value": [
        "moisturizer"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "보습 제품의 새로운 누출이 보고되어 해당 제품 사용을 보류해요."
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
새로운 누출이 보고되어 해당 제품 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
용기와 표시를 확인하고 필요하면 제조사에 문의해 주세요.

## syn-hold-0099

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `91aaa6f275efdec00b2706496e5bf65167453d80d0116fa84c778d93a67424d1`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림 수령 후 용기에서 내용물이 새고 이전에 사용하던 같은 버전과 다른 새 냄새가 확인됐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "품질 이상 의심 제품의 사용과 개별 안내를 보류해요."
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
수령한 제품의 누출과 새로운 냄새 때문에 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 용기 상태와 확인 내용을 문의해요.

## syn-hold-0100

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `309d52601db7a4af9ed28c2ca20865a2c80ce76fabf8d84003215ce6de41e54f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "기한이 남은 합성 선크림에서 이전에 없던 색 변화가 확인됐어요. 냄새 변화는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 색 변화가 있는 제품의 사용과 개별 안내를 보류해요."
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
기한이 남은 표시가 있어도 새 색 변화가 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 변화와 기한 표시를 확인해요.

## syn-hold-0101

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `caf3597fe534d2bf8af07a92d7b9edb1c8c6f481f36c6c5178f4df98b01d2bad`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림은 흔들어 쓰는 정상 이층 제형이에요. 최근 원래 없던 악취가 추가로 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "정상 이층과 별개인 새 냄새 변화로 사용과 개별 안내를 보류해요."
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
정상 이층 안내와 별개로 새 악취가 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 냄새 변화와 표시를 확인해요.

## syn-hold-0102

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `375697ef4254bdb87ab97b951786f86077caddcec795ae7b245a2f296fb12615`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 선크림 두 개 중 가에서만 원래 없던 입자와 색 변화가 확인됐어요. 나의 외관은 확인하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "변화가 확인된 가의 사용과 개별 안내를 보류해요."
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
가 용기의 새 입자와 색 변화가 확인돼 가에 대한 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
가의 사용을 중단하고 제조·판매처에 확인된 변화를 문의해요. 나의 상태는 미상이에요.

## syn-hold-0103

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `fe630825d007585ecfb726353602d27912aa7350aa859164646bb7882f456772`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림은 표시된 보관 조건에 맞춰 두었어요. 그 후 전에 없던 덩어리와 색 변화가 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 변화가 확인돼 사용과 개별 안내를 보류해요."
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
보관 이력이 있어도 새 덩어리와 색 변화가 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 변화와 보관 이력을 확인해요.

## syn-hold-0104

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `b42d1c9ee162492560440114e334fa84ae57622c2eb0844ddd9608eec38a6174`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "지난주에는 냄새 변화가 없었지만 오늘 같은 선크림에서 새 냄새 변화가 확인됐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "이전 점검과 별개로 새 변화가 확인돼 사용과 개별 안내를 보류해요."
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
지난주 관찰과 별개로 오늘 새 냄새 변화가 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 변화 시점과 상태를 문의해요.

## syn-hold-0105

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `7c1fb420772a24d2ed78e3b640251eaddb07320edaf7f6930d56fdce5ec68166`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "미개봉 선크림 용기가 부풀고 내용물이 새는 상태가 확인됐어요. 원래 포장 상태는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "확인된 누출을 품질 이상 의심으로 보고 사용과 개별 안내를 보류해요."
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
미개봉 용기의 누출이 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조·판매처에 누출과 팽창 상태를 문의해요.

## syn-hold-0106

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `8677491a3b2cb1be2cc9c7019c7dea864c8ecbad1ff432be715216009547e981`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 선크림의 제조번호는 확인했지만 회수 대상 여부는 아직 조회하지 않았어요. 내용물에서는 원래 없던 냄새 변화가 확인됐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "회수 조회와 별개로 확인된 새 냄새 때문에 사용과 개별 안내를 보류해요."
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
회수 대상 조회와 별개로 새 냄새 변화가 확인돼 개별 안내를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
해당 제품의 사용을 중단하고 제조번호와 변화 내용을 제조·판매처에 확인해요. 회수 대상 여부는 미상이에요.

## syn-sol-0274

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0f3294f1e25611b7da7db49a41be3fd4da505be942cd9c56d3b9eca620ecfc6f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "face_towel": "pat_dry",
        "hands_towel": "rub"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "얼굴 건조는 가볍게 하지만 세안 도구와 마찰은 미상이므로 전체 세안 방법은 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴은 수건으로 문지르지 않고 가볍게 눌러 말리지만 손은 수건으로 문질러요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
얼굴을 말리는 행동만으로 세안 도구나 세안 중 마찰을 판단하지 않아요.

## syn-sol-0278

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3c7f67438f1587e0c1d7a1774090c392f5131b8a7b817ce722a63e5347703acc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "water_resistant_product": {
          "planned_use": "next_week",
          "used_today": false
        },
        "today_removal": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "계획을 실제 사용이나 반복 행동으로 취급하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
내수성 제품은 다음 주에 쓸 계획이고 오늘은 쓰지 않았어요. 오늘 제거 행동은 알려지지 않아 반복 세안이 있었다고 판단하지 않아요 [kb:B-I01@0.6.1].

### 근거 및 이유
광보호와 세정을 함께 살필 때는 제거 부담 때문에 광보호를 희생하거나 내수성 표시만으로 무조건 반복 세안하는 행동을 살펴요 [kb:B-I01@0.6.1]. 제한된 제품 조합의 소규모 영상 연구도 모든 내수성 제품에 하나의 제거 방법을 확정하지 않아요 [ref:S08].

### 확인이 필요한 한계
실제 사용할 제품의 표시와 버전, 사용 후 제거 행동은 확인되지 않았어요.

## syn-sol-0279

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `19186d8494a14d0e77cda524172b847c225acdb80860816d8500f2e1440dcf77`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "other_person": "동거인",
        "other_person_reason": "내수성 표시만 보고",
        "other_person_automatic_repeat": true,
        "self_repeat": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "다른 사람의 행동으로 본인의 판정을 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
동거인은 내수성 표시만 보고 반복 세안하지만 본인의 제거 행동은 확인되지 않았어요. 동거인의 습관을 본인의 행동으로 판단하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품과 방법을 비교한 소규모 연구만으로 모든 내수성 제품의 제거법을 정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
본인의 실제 제거 행동과 해당 제품 지침은 미상이에요.

## syn-sol-0280

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8ec5c887486c5480de00a602ab32376541bae48c6deb098bec7c8373012752f4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "used_site": "arms",
        "face_removal": "unknown",
        "water_resistant_product_used_site": "arms"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "팔의 사용을 얼굴의 반복 세안으로 옮겨 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
내수성 제품은 팔에만 사용한 것으로 기록됐어요. 이를 얼굴에서 자동으로 반복 세안한 사실로 옮기지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
소규모 연구의 제한된 제품 조합만으로 모든 내수성 제품에 일률적 제거법을 확정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
얼굴 제거 행동은 미상이에요.

## syn-sol-0281

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f05b606464a9b62bcf87b0350de234ce57234c9ef08f002390060f20cff4bd6b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "label_photo_product_version_matches_current_product": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "버전 일치가 확인되기 전에는 해당 표시를 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
표시 사진과 현재 사용 중인 제품이 같은 버전인지 확인되지 않았어요. 사진의 내용을 현재 용기에 적용하기는 보류해요.

### 근거 및 이유
세정 방법을 살필 때는 내수성 표시만 보고 무조건 반복 세안하는 행동을 검토해요 [kb:B-I01@0.6.1]. 제공된 소규모 영상 연구도 제한된 제형의 비교여서 모든 제품에 일률적인 제거법을 정하지 않아요 [ref:S08].

### 확인이 필요한 한계
현재 사용하는 제품의 버전과 사진의 판이 일치하는지 확인하기 전에는 사진을 현재 제품의 근거로 쓸 수 없어요.

## syn-sol-0282

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ac127e8890c0deb79d1028e445fff3d7378492c732bed7c5dd49b960abc2b8e0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "removal_instruction": "partially_obscured",
        "required_cleansing_method": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "보이지 않는 제거 조건을 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
제품의 제거 안내 일부가 가려져 필요한 세정법을 읽지 못했어요. 해당 제품의 온전한 안내를 확인해 주세요. [kb:B-I01@0.6.1]

### 근거 및 이유
일부 제품을 비교한 소규모 연구만으로 모든 내수성 제품의 제거 방법을 정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
가려진 부분에 어떤 지시가 있는지는 현재 알 수 없어요.

## syn-sol-0283

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2104b90abb1b936098e21879c920a4c38f08740a7f2d4e3a1f2480bed949a465`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "cleansing_method": "foam",
        "removal_instruction": "unknown",
        "repeat_reason": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "폼 사용만으로 표시 일치나 불일치를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
폼을 사용한 사실만으로 제품 제거 표시와의 일치 여부를 판정할 수 없어요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 연구를 모든 제품의 일률적 제거법으로 일반화하지 않아요. [ref:S08]

### 확인이 필요한 한계
해당 제품의 제거 표시와 반복 이유는 미상이에요.

## syn-sol-0284

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `bc67002e45cd38be300e20368726002c20efa10f9b7a396bcad6e33d7f99e427`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "cleanser_uses": 2,
        "same_event": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "세정 횟수와 한 번의 단계 수를 구분해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
세정제를 두 번 썼지만 한 세안의 두 단계였는지 서로 다른 시간의 사용인지는 미상이에요. 두 단계 반복 세안으로 확정하지 않아요 [kb:B-C05@0.6.1].

### 근거 및 이유
세정 횟수를 살필 때는 제거 목적 없이 습관적으로 반복하는지 비교해요 [kb:B-C05@0.6.1]. 제공된 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
두 사용의 시간 관계와 세정 목적이 확인되지 않았어요.

## syn-sol-0287

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1be06f080c6edd28cc2aecaf578ca39d21dc366dd267e6a50d07c17a43234809`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "device_site": "hands",
        "face_method": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "site": "hands",
        "only": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "손에만 쓴 기기로 얼굴 세안 방법을 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
기기는 손에만 사용한다고 하셨고 얼굴을 어떻게 씻는지는 확인되지 않았어요. 손에서의 사용을 얼굴 세안에 적용하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. [ref:S03]

### 확인이 필요한 한계
얼굴에서 실제 쓴 도구나 마찰 정도는 미상이에요.

## syn-sol-0288

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `512fab1eac4d068d1f04542010de6b42ff7128e317663176312eb03ba38fad43`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "used_product_water_resistance": "unknown",
        "other_product_labeled": true,
        "other_product_location": "bag"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "다른 제품의 내수성 표시를 사용 제품에 이전하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
가방 속 다른 제품에 내수성 표시가 있어도 실제 사용한 제품의 표시로 옮길 수 없어요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 연구로 모든 내수성 제품의 제거법을 확정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 내수성 표시는 미상이에요.

## syn-sol-0289

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1c21f7074de9c2e9ccf59461aff84ed827d0db0f8fba8bf0c886408e4c836db5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "plan": "반복 세안 중단",
        "today_actual_behavior": "unknown",
        "previous_repeat_reason": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "계획만으로 행동 변경을 확인하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
반복 세안을 멈추려는 계획은 있지만 오늘 실제 행동과 이전에 반복한 이유는 미상이에요. 계획을 이미 실행했다고 판단하지 않아요 [kb:B-I01@0.6.1].

### 근거 및 이유
광보호와 제거를 살필 때는 내수성 표시만으로 무조건 반복하거나 제거 편의를 위해 광보호를 줄이는 실제 행동을 살펴요 [kb:B-I01@0.6.1]. 소규모 영상 연구도 제한된 제품 조합으로 모든 내수성 제품의 제거법을 정하지 않아요 [ref:S08].

### 확인이 필요한 한계
오늘의 실제 행동과 반복 이유, 사용 제품의 표시가 확인되지 않았어요.

## syn-sol-0290

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `91f84dbfed225ed312c3a749e6a036ecbba95f0bd4e9a79db9677fe2f844ccc8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "face_wash_records": [
          "한 번",
          "두 번"
        ],
        "reconciled": "unknown"
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
      "status": "unknown",
      "guidance": "서로 충돌하는 기록으로 세안 횟수 차이를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
얼굴 세안 기록이 한 번과 두 번으로 엇갈려요. 어느 쪽이 맞는지 확인하기 전에는 반복 세안 여부를 정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
세안 횟수와 함께 반복의 목적도 살펴야 해요.

### 확인이 필요한 한계
기록의 충돌과 세안 목적이 해결되지 않았어요.

## syn-sol-0292

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `da392a317e98828ed547d74fd56622ffac17cddb28acc593e5d045501a511593`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "sweat": true,
        "face_wash_events": "unknown",
        "steps": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "sweat_during_exercise": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "땀이 있었다는 사실만으로 세정 횟수를 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 설명해요. 개인의 결과나 특정 제품의 성능을 확정하지는 않아요.",
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
운동 중 땀이 난 사실은 확인됐지만 얼굴을 몇 번, 몇 단계로 씻었는지는 미상이에요. [kb:B-C05@0.6.1]

### 근거 및 이유
땀 자체가 세안 횟수나 단계를 알려주지는 않아요. 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 세정 행동을 추정하지 않아요.

## syn-sol-0293

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cdafdcd64b6afc4e77c6de5bcf898b2b5086165086f8188fb50c075733a2b923`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "label_copies": {
          "identified_as_same_product": true,
          "removal_instructions": "conflict"
        },
        "current_version": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "상충하는 표시 중 하나를 임의로 현재 제품의 지시로 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
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

### 응답 초안 — 미승인

### 핵심 안내
같은 제품이라고 적힌 두 표시 사본의 제거 방법이 달라요. 현재 버전이 확인되지 않아 어느 쪽도 현재 용기의 지시로 채택하지 않아요.

### 근거 및 이유
제거 방법을 살필 때는 내수성 표시만으로 무조건 반복 세안하는 행동을 살펴요 [kb:B-I01@0.6.1]. 제공된 소규모 연구는 제한된 제품 조합을 비교했으며 모든 제품에 하나의 제거법을 정하지 않아요 [ref:S08].

### 확인이 필요한 한계
현재 제품의 판과 그 판에 해당하는 표시를 확인하기 전에는 두 사본 중 하나를 적용할 수 없어요.

## syn-sol-0294

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `07fdd35b03e9fcdc6dc609d18adbeb160dd3c8b98686ee8711db1297685af530`
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
        "face": "moisturizes_after_wash",
        "neck": "moisturizes_after_wash",
        "neck_skin_wetness": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "slightly_damp",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "피부 물기의 관찰 부위는 명시되지 않았고 목의 물기는 미상이라 부위별 시점을 판정하지 않아요."
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
    "kb:B-M01@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴과 목 모두 세정 후 보습한다고 보고됐어요. 피부가 약간 촉촉하다는 관찰의 부위는 명시되지 않았고 목의 물기는 미상이에요.

### 근거 및 이유
일반적으로 보습제를 사용하는 경우 세정 후 피부가 아직 촉촉할 때 바르는 원칙이 있어요. [ref:S04] 부위별 시점이 확인되지 않아 해당 기준과의 차이는 판단하지 않아요. [kb:B-M01@0.6.1]

### 확인이 필요한 한계
얼굴이나 목의 물기와 제품별 지시를 추정하지 않아요.

## syn-sol-0295

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `97e508f7f09eecca3acff05f0409ea798c9dc3311f1f606aee585defb8ddef1e`
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
        "product_a": "after_wash",
        "product_b": "after_wash"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "product_a": "apply_to_dry_skin",
        "product_b": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "exception",
      "guidance": "건조한 피부에 바르라는 제품 A의 지시를 우선 검토하며 B의 지시는 미상이에요."
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
    "kb:B-M01@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 A는 확인된 건조 피부 지시를 우선해요. [kb:B-M01@0.6.1]

### 근거 및 이유
일반적인 촉촉한 피부 보습 안내를 모든 제품에 일괄 적용하지 않아요. [ref:S04]

### 확인이 필요한 한계
제품 B의 지시는 확인되지 않았어요.

## syn-sol-0296

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `0e2da2fdba2adb8c772cdb1bbad2ee395f04d2b0ed1c60b30002d8ca7700cfcc`
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
        "self": "handwashing",
        "colleague": "handwashing"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "self": "unknown",
        "colleague": "after_washing"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동료의 보습 기록으로 본인의 손 보습 여부를 판단하지 않아요."
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
본인의 손 보습 여부는 미상이며 동료의 기록과 구분해요. 확인 전 본인의 차이를 단정하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 안내는 손을 씻은 후 보습을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
동료의 기록으로 본인의 보습 여부를 대신하지 않아요.

## syn-sol-0298

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `44e2f0be1e73a45ce8fcbc53b71b38ee843dee74fc87033b3f4d544e19432c1b`
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
        "face_moisturizer": "used",
        "neck_moisturizer": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.dryness_return": {
      "variable_id": "moisturizing.dryness_return",
      "state": "known",
      "value": {
        "face": "none_reported",
        "neck": "reported"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "목에 보습제를 실제 사용했는지 미상이라 그 부위의 보습 방법을 판정하지 않아요."
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
목에 건조 경험이 보고됐지만 목의 보습제 사용 여부는 미상이에요. 해당 부위의 사용 방법 차이는 판단하지 않아요. [kb:B-M02@0.6.1]

### 근거 및 이유
일반적으로 피부가 아직 촉촉할 때 보습하는 안내가 있어요. [ref:S04]

### 확인이 필요한 한계
건조의 원인이나 적절한 사용량을 이 기록만으로 확정하지 않아요.

## syn-sol-0299

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `43a2c52124e937b06810bd0b98dfd1f193bab9453883e72ae56d0eb8a4403f8c`
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
        "necessary_handwashing": "maintained"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "after_work": "planned",
        "actual_use": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "작업 뒤 보습 계획은 실제 사용의 확인이 아니며 필요한 손 위생은 유지해요."
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
계획과 실제 손 보습은 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
필요한 손 씻기는 유지하면서 실제 보습 여부를 확인할 수 있어요. [ref:S21]

### 확인이 필요한 한계
현재 보습 충족이나 불편 여부는 미상이에요.

## syn-sol-0300

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9fa7e3fb7f3fbf974df0157c358a4be0ff39e5fa0df3ee59b56a324279f39817`
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
        "face": "moisturizer_used",
        "neck": "moisturizer_used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "face": "comfortable",
        "neck": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "얼굴의 편안함으로 목의 제품 반응을 대신하지 않아요."
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
얼굴은 편안했다고 보고됐지만 목의 반응은 미상이에요. 부위별 경험을 구분해요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
목의 반응을 임의로 정상으로 채우지 않아요.

## syn-sol-0301

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8314ecf569249448ddd4fd1d5907ed932f74dfb1e894d9dbdaa614f369c5ab49`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "label": "fragrance_free"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.essential_oils": {
      "variable_id": "product.essential_oils",
      "state": "known",
      "value": {
        "label": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "self": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "무향료 표시는 확인됐지만 향성 에센셜오일과 개인 반응은 미상이에요."
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
무향료 표시와 향성 오일 정보는 별도로 확인해요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 보습 선택에서 개인 반응도 함께 살펴봐요. [ref:S21]

### 확인이 필요한 한계
표시만으로 개인에게 반응이 없다고 보장할 수 없어요.

## syn-sol-0302

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a44d551cfda123e768e36b20bd3123ee5a6d64d1f728cbfd7ba256c004c58f40`
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
        "self": "moisturizer_used",
        "friend": "aftershave_used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "friend": "stinging",
        "self": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "친구의 따가움은 본인의 반응이 아니며 본인의 반응은 미상이에요."
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
친구의 따가움과 본인의 반응을 구분해요. 본인의 면도 후 보습 반응은 확인되지 않았어요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
친구의 경험으로 본인 제품의 적합성을 결정하지 않아요.

## syn-sol-0303

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ab123041ca7b181f9c10c01f307e36337fcc77b3ae6130c767aa4833d460c76f`
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
        "self": "declined_to_answer"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "face": "comfortable",
        "hands": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "얼굴의 편안함을 손의 보습 충족으로 대체하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 보습 정보는 확인되지 않았어요. [kb:B-M04@0.6.1]

### 근거 및 이유
얼굴의 편안함과 손의 상태는 서로 구분해요. [kb:B-M04@0.6.1]

### 확인이 필요한 한계
답변을 원하지 않은 내용을 정상이나 이탈로 바꾸지 않아요.

## syn-sol-0304

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3d9c8687f8a2cd5f59815e378159fff4cd03ba4e44102e31cd158e4a7e81a3ee`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "face_comfort",
        "hands_comfort"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face": "moisturizer_used",
        "hands": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "face": "comfortable",
        "hands": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "unknown",
      "guidance": "얼굴의 보습 충족 경험으로 손의 사용이나 충족을 추정하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
보습 목표는 부위별 경험과 함께 살펴봐요. [kb:B-M03@0.6.1]

### 근거 및 이유
얼굴은 편안하지만 손의 사용과 편안함은 미상이에요. [kb:B-M03@0.6.1]

### 확인이 필요한 한계
제품 수나 성분만으로 손의 보습 충족을 확정하지 않아요.

## syn-sol-0305

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `909bba4a302a88501f83b2d26f83dcafee38d8058eefc04122b2064b0659d235`
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
        "labelled_product": "moisturizer",
        "actually_used_product": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "labelled_product": "after_shaving"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "면도 후 사용 표시가 있는 제품과 실제 사용한 제품이 같은지 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시를 확인한 제품과 실제 사용 제품의 연결은 미상이에요. [kb:B-M05@0.6.1]

### 근거 및 이유
두 제품이 같다고 가정해 사용 경험을 판정하지 않아요. [kb:B-M05@0.6.1]

### 확인이 필요한 한계
실제 제품과 그 반응을 별도로 확인할 수 있어요.

## syn-sol-0306

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d82956bc30648dfc07b4eacb347e13c9ec499f8e770b07f1c7be3803c7cfac11`
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
        "self": "unknown",
        "friend": "moisturizer_used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "self": "unknown",
        "friend": "comfortable"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "친구의 편안한 경험은 본인의 면도 후 사용과 반응을 알려주지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 편안함을 본인에게 적용하지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
본인의 면도 후 사용과 반응은 미상이에요. [kb:B-M05@0.6.1]

### 확인이 필요한 한계
확인되지 않은 내용을 근거로 제품 적합성을 단정하지 않아요.

## syn-sol-0307

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c30e1c58a3416e3306243bdf767fe6d8154fdca55ad069337a619af65ff37743`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.post_use_timing": {
      "variable_id": "skin.post_use_timing",
      "state": "known",
      "value": {
        "face": "no_discomfort_reported",
        "neck": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "face_product": "changed",
        "neck_product": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I03",
      "status": "unknown",
      "guidance": "얼굴에 불편이 없다는 보고는 목의 반응이나 변경 이력을 확인해 주지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴과 목의 관찰을 분리해요. [kb:B-I03@0.6.1]

### 근거 및 이유
목의 사용 변화와 반응은 미상이에요. [kb:B-I03@0.6.1]

### 확인이 필요한 한계
확인되지 않은 변화의 원인이나 안전성을 단정하지 않아요.

## syn-sol-0308

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8ba068a62e7e04fea0933c6ee7b28a5639102ba8a1b05b5cf27e5729931baf73`
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
        "moisturizer": "changed",
        "relative_timing": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "environment.season_change": {
      "variable_id": "environment.season_change",
      "state": "known",
      "value": {
        "reported": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "change": "reported",
        "onset": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I03",
      "status": "unknown",
      "guidance": "제품과 계절의 변화가 보고됐지만 사용감 변화와의 시간 관계는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 변경과 계절 변화를 각각 기록해요. [kb:B-I03@0.6.1]

### 근거 및 이유
사용감 변화의 시점이 미상이어서 어느 하나를 원인으로 확정하지 않아요. [kb:B-I03@0.6.1]

### 확인이 필요한 한계
필요한 시간 관계만 확인할 수 있어요.

## syn-sol-0309

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `84a6c8062162ee4b4f90629c07927df75db260e6863eb7c7845b253b0a3dfd37`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.available_products": {
      "variable_id": "constraints.available_products",
      "state": "known",
      "value": [
        "moisturizer_owned"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "actual_use": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "constraints.goals": {
      "variable_id": "constraints.goals",
      "state": "known",
      "value": [
        "considering_separate_hydration_step"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "unknown",
      "guidance": "보유와 실제 사용은 다르며 현재 보습 충족은 미상이에요."
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

### 응답 초안 — 미승인

### 핵심 안내
보습제를 보유한 사실과 실제 사용을 구분해요. [kb:B-M03@0.6.1]

### 근거 및 이유
현재 사용과 편안함을 확인하기 전 추가 단계의 필요를 확정하지 않아요. [kb:B-M03@0.6.1]

### 확인이 필요한 한계
제품을 보유했다는 사실만으로 보습 충족을 선언하지 않아요.

## syn-sol-0310

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d1199c3aa4f52319f98422084b05024da6e76fabba5100f87f6bf305a2acc6fb`
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
        "immediately_after": "comfortable",
        "later": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "moisturizer": "unchanged"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I03",
      "status": "unknown",
      "guidance": "직후의 편안함은 이후의 건조감이나 반응을 대신하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-I03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
직후의 느낌과 이후 경험을 구분해요. [kb:B-I03@0.6.1]

### 근거 및 이유
나중의 상태는 확인되지 않았어요. [kb:B-I03@0.6.1]

### 확인이 필요한 한계
촉촉한 느낌을 흡수량이나 피부 상태 측정치로 환산하지 않아요.

## syn-sol-0311

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `960236b5a0f6a17405560227248883cecf1dddd70bfa6b9e19bdb61cbb01b79d`
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
        "exists": true,
        "applies_to_moisturizer": "unknown"
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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "진료 계획의 보습제 적용 범위와 사용 시 피부 물기는 미상이에요."
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

### 응답 초안 — 미승인

### 핵심 안내
개별 진료 계획의 적용 범위를 먼저 확인해요. [kb:B-M01@0.6.1]

### 근거 및 이유
사용 시 피부 물기도 미상이어서 일반 기준과의 차이를 만들지 않아요. [kb:B-M01@0.6.1]

### 확인이 필요한 한계
기존 진료 지시를 일반 안내로 대체하지 않아요.

## syn-sol-0312

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2a6e356bbe6755c6274079a154fc4141aa8defa931520c08a566107470797854`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "product_a": "fragrance_free",
        "product_b": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "product_a": "unknown",
        "product_b": "comfortable"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "A의 표시와 B의 편안한 경험을 한 제품에 합치지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 A의 표시와 제품 B의 경험을 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
A의 반응과 B의 향료 정보는 미상이에요. [kb:B-M04@0.6.1]

### 확인이 필요한 한계
어느 제품의 개인 적합성도 다른 제품의 기록으로 확정하지 않아요.

## syn-sol-0313

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `46941329c3ae66b3fb4760c5dd2374d02d265e00083efc39a03e4dcd16339253`
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
        "moisturizer": "used"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.reaction": {
      "variable_id": "shaving.reaction",
      "state": "known",
      "value": {
        "discomfort": "reported",
        "timing_relative_to_product": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "불편이 보고됐지만 제품 사용과의 시간 관계는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
보고된 불편을 존중하고 제품 사용과의 시점을 확인해요. [kb:B-M05@0.6.1]

### 근거 및 이유
현재 정보만으로 면도나 제품 중 어느 것이 원인인지 확정하지 않아요. [kb:B-M05@0.6.1]

### 확인이 필요한 한계
지속하거나 악화하는 불편은 전문가 확인이 필요해요.

## syn-sol-0314

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9a8ef1e0b0f4f96d4c39224d917500849e10e20296fc2bec1b1e6df23e1c4ae1`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "slightly_damp",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_actual_use": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "피부가 촉촉하다는 관찰만으로 보습제 사용이나 관찰 시점을 확인할 수 없어요."
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

### 응답 초안 — 미승인

### 핵심 안내
피부가 약간 촉촉하다는 관찰과 보습제 사용을 구분해요. 실제 보습제 사용은 미상이에요.

### 근거 및 이유
사용과 시점이 확인되지 않아 보습 시점의 차이를 판단하지 않아요. [kb:B-M01@0.6.1]

### 확인이 필요한 한계
물기 관찰의 시점은 추정하지 않아요.

## syn-sol-0315

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `62710673774d19a19810398284449018842710f5447ae5ab5ea44381713beeaa`
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
        "moisturizer": "used_after_wash"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "세정 후 보습제 사용은 확인됐지만 피부 물기 정보는 제공되지 않았어요."
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

### 응답 초안 — 미승인

### 핵심 안내
세정 후 사용과 피부 물기를 구분해요. [kb:B-M01@0.6.1]

### 근거 및 이유
피부 물기 정보가 없어 기준과의 차이는 미상이에요. [kb:B-M01@0.6.1]

### 확인이 필요한 한계
답변하지 않은 값을 임의로 채우지 않아요.

## syn-sol-0316

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `dbbf8ff3f293506389abd6568e0aef21e690ade3a8a341ab60901023761447c9`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.diagnosed_conditions": {
      "variable_id": "person.diagnosed_conditions",
      "state": "known",
      "value": {
        "hand_eczema": "diagnosed"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.moisturizing_pattern": {
      "variable_id": "hand.moisturizing_pattern",
      "state": "known",
      "value": {
        "all_moisturizing": "stopped_due_to_diagnosis"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "moisturizing_instruction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "손 습진 진단을 이유로 모든 보습을 중단했으며 개별 진료 지시는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 진단만으로 모든 보습을 중단해야 한다고 일반화하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
필요한 손 위생과 보습을 함께 살펴보되 진료 지시는 우선 확인해요. [kb:B-M04@0.6.1]

### 확인이 필요한 한계
미확인 진료 계획을 추정하거나 치료를 변경하지 않아요.

## syn-sol-0317

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6a54896c98adca5348c100b75be548d8c3f37491eda49bd5a41f05618d27de82`
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
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "reduction": "planned",
        "actual_reduction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "unknown",
      "guidance": "건조와 감량 계획이 보고됐지만 실제 감량은 미상이에요."
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

### 응답 초안 — 미승인

### 핵심 안내
건조감과 감량 계획을 구분해요. [kb:B-M02@0.6.1]

### 근거 및 이유
계획만으로 실제 감량이 있었다고 판단하지 않아요. [kb:B-M02@0.6.1]

### 확인이 필요한 한계
필요한 보습과 사용 경험을 함께 확인해요.

## syn-sol-0318

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d215a7210d766820053090eca33042ef46fc8c9d87a00071db1fcfd21412616e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.roles": {
      "variable_id": "product.roles",
      "state": "known",
      "value": [
        "product_a_moisturizer"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "product_a": "unknown",
        "product_b": "comfortable"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_b_role": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "unknown",
      "guidance": "B의 편안함으로 A의 실제 보습 충족을 판단하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
두 제품의 역할과 경험을 분리해요. [kb:B-M03@0.6.1]

### 근거 및 이유
A의 실제 편안함은 미상이에요. [kb:B-M03@0.6.1]

### 확인이 필요한 한계
제품 역할만으로 보습 충족이나 추가 필요를 확정하지 않아요.

## syn-sol-0319

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a9ba1cd633de031df01661e101a17d005106646c0b5e69a25d46eb96a6f98c5c`
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
        "handwashing": "maintained"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.hand_observation": {
      "variable_id": "skin.hand_observation",
      "state": "known",
      "value": {
        "dryness": "reported"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "hand.product_reaction": {
      "variable_id": "hand.product_reaction",
      "state": "known",
      "value": {
        "moisturizer": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "손 건조 보고와 특정 보습제 반응은 별도이며 반응은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
필요한 손 위생은 유지해요. [kb:B-M04@0.6.1]

### 근거 및 이유
손의 건조와 보습제 사용 반응을 구분해 확인해요. [kb:B-M04@0.6.1]

### 확인이 필요한 한계
건조만으로 특정 제품이 원인이라고 단정하지 않아요.

## syn-sol-0320

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `50898504ef793e203e5e94fa8fccd06b2f3f9c15181d3d462ba6b2736ff3d08d`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가 후보는 SPF 30과 광범위 표시를 확인했으나 물놀이에 필요한 내수성 표시는 가려져 있어요. 나 후보의 표시는 아직 읽지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "가의 내수성 및 나의 기본 성능은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
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
가의 내수성과 나의 표시는 확인 후 판단해요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선제품은 SPF, 광범위 보호와 필요한 내수성 표시를 함께 살펴봐요. [ref:S16] [kb:B-P01@0.6.1]

### 확인이 필요한 한계
가려진 표시는 내수성이 없다는 뜻이 아니며 나의 성능도 미상이에요.

## syn-sol-0321

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `277bc01274f46b8fd20e4f0c4ce126f979d788e3cd0f6d8538f8616393402506`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "현재 야외용 후보의 버전은 새 포장이에요. 광범위와 SPF 30 표시는 같은 이름의 이전 버전 자료에서만 확인됐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "이전 버전의 표시를 현재 후보에 옮기지 않고 현재 표시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
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
현재 버전의 표시를 확인해요. [kb:B-P01@0.6.1]

### 근거 및 이유
이전 버전의 자료만으로 현재 제품의 보호 표시를 확정하지 않아요. 야외용 후보는 필요한 표시를 살펴봐요. [ref:S16] [kb:B-P01@0.6.1]

### 확인이 필요한 한계
현재 버전의 SPF와 광범위 표시는 미상이에요.

## syn-sol-0330

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `32ad01a194f05ae19c7c6737a2bfc81eea3e9ae0d1d45f6ecc6b54aa69ba3014`
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
        "가": "확인됨",
        "나": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.pao": {
      "variable_id": "storage.pao",
      "state": "known",
      "value": {
        "가": "읽지 못함",
        "나": "읽지 못함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 개봉일만으로 두 제품의 기간 적합성을 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
두 선크림 중 가의 개봉일만 확인했고 개봉 후 사용기간 표시는 둘 다 읽지 못했어요. 각 제품의 표시와 이력을 따로 확인해 주세요. [kb:B-S02@0.6.1]

### 근거 및 이유
한 제품의 개봉일은 다른 제품의 이력이나 두 제품의 표시 기간을 대신하지 않아요.

### 확인이 필요한 한계
나의 개봉일과 두 제품의 개봉 후 사용기간은 확인되지 않아 기간 적합성을 정할 수 없어요.

## syn-sol-0331

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `dc855ed5f0bfc0f8bf6551b68c83e5cbe3e1d861858eb6c2824679480415abcc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "현재는 파우치를 직사광선 없는 곳에 두고 있어요. 이전 여행에서 뜨거운 차량에 두었는지는 기억하지 못해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 보관과 별개로 과거 열 노출 여부는 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 보관과 과거 여행 중 이력을 구분해요. [kb:B-S01@0.6.1]

### 근거 및 이유
현재 직사광선 없는 보관 기록은 과거 차량 내 보관 여부를 알려주지 않아요. [kb:B-S01@0.6.1]

### 확인이 필요한 한계
과거 열 노출은 미상이며 없었다고 단정하지 않아요.

## syn-sol-0332

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `11794559ac216a194e320690f49e5622f7ccb87595e9d852f3587e7c2876de3c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가족의 선크림은 뜨거운 차에 보관했어요. 본인의 선크림은 그 차에 있었는지 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "가족 용기의 이력을 본인 용기에 그대로 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가족 용기와 본인 용기의 보관 이력을 구분해요. [kb:B-S01@0.6.1]

### 근거 및 이유
가족 제품의 차량 보관 이력을 본인 제품에 옮기지 않아요. [kb:B-S01@0.6.1]

### 확인이 필요한 한계
본인 용기가 차 안에 있었는지는 미상이에요.

## syn-sol-0334

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `53111306901f8604e81bef39e103dc4bfb06014dce4d4d6fd61e2a6552f7c1ec`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "현재 가진 용기에는 사용기한이 지워졌어요. 같은 이름의 다른 국가 용기에 적힌 날짜를 현재 용기의 날짜로 기록하려 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "difference",
      "guidance": "다른 국가 용기의 날짜를 현재 보유품에 복사하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 용기의 기한을 별도로 확인해요. [kb:B-Q03@0.6.1]

### 근거 및 이유
다른 국가 용기의 날짜를 현재 보유품의 날짜로 복사하지 않아요. [kb:B-Q03@0.6.1]

### 확인이 필요한 한계
현재 용기의 기한은 미상이에요.

## syn-sol-0335

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d105f9b5e9e405dbb641ac396d6b90a9e54684802fc6e02725aa60d7907e93d0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "판매 페이지의 리필 허용 문구는 확인했어요. 그 페이지가 현재 보유한 용기 버전에 해당하는지는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S07",
      "status": "unknown",
      "guidance": "현재 용기에 해당하는 리필 지침인지 먼저 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S07@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 용기 버전에 적용되는 리필 지침을 먼저 확인해요. [kb:B-S07@0.6.1]

### 근거 및 이유
판매 페이지가 현재 용기에 해당하는지 확인되지 않았어요. [kb:B-S07@0.6.1]

### 확인이 필요한 한계
해당 문구를 현재 용기의 허용 지침으로 확정할 수 없어요.

## syn-sol-0337

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `1d60ef7c535a6f2599832effa2420163d891c04a617349e6c445b571f85906cf`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가 용기는 개봉일과 안내 기간이 확인돼요. 나 용기는 같은 제품명이나 개봉일을 알 수 없어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 개봉 이력을 나에 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
나 용기의 개봉 이력과 안내를 별도로 확인해요. [kb:B-S02@0.6.1]

### 근거 및 이유
같은 제품명이어도 가의 개봉 이력을 나의 이력으로 대신하지 않아요. [kb:B-S02@0.6.1]

### 확인이 필요한 한계
나의 개봉 후 기간 적합성은 미상이에요.

## syn-sol-0339

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `789b1bb787539a59ddf77a0d3fdf98f7e343acc9a6e6c963c956c2cea7dc6ce0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "보습제는 아주 적게 발랐다고 기록했어요. 선크림 도포량은 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "보습제 기록만으로 선크림을 적게 발랐다고 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
선크림 도포량은 별도로 확인해요. [kb:B-P02@0.6.1]

### 근거 및 이유
보습제를 적게 바른 기록은 다른 제품인 선크림의 도포량을 알려주지 않아요. [kb:B-P02@0.6.1]

### 확인이 필요한 한계
선크림 도포량은 미상이에요.

## syn-sol-0340

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `313d1a11e0611a71126d864ab8dbf33d28ad9ac114023b04ec33222a4e9efc19`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 긴소매를 입었다고 했지만 다른 노출 부위와 차양 이용 가능 여부는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "기록된 긴소매 외 보완 수단의 적합성은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
기록된 긴소매와 다른 광보호 수단의 이용 가능성을 구분해요. [kb:B-P04@0.6.1]

### 근거 및 이유
긴소매 이용만으로 다른 노출 부위의 상태를 확정하지 않아요. [kb:B-P04@0.6.1]

### 확인이 필요한 한계
다른 노출 부위와 차양 이용 가능 여부는 미상이에요.

## syn-sol-0341

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `7e70e131ecfa856dfcedb4694c9ec9421dc0293b11f3309933ad227e6241d2bc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 활동 중 재도포 알림이 울렸어요. 알림 이후 실제로 발랐는지는 기록되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림 기록을 실제 재도포로 간주하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
알림 이후 실제 재도포 여부를 확인해요. [kb:B-P03@0.6.1]

### 근거 및 이유
알림이 울린 기록은 실제로 발랐다는 기록과 달라요. [kb:B-P03@0.6.1]

### 확인이 필요한 한계
재도포 여부는 미상이에요.

## syn-sol-0342

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `aab9fb16258725cb8f181d345b75fed5f9a8f1821603b9407dbc20a414fe396b`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "보습제 뚜껑은 밤새 열려 있었어요. 선크림 용기가 열려 있었는지는 확인하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "보습제의 보관 이력을 선크림에 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
선크림 용기가 열려 있었는지 별도로 확인해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보습제의 용기 상태를 선크림에 적용하지 않아요. [kb:B-S01@0.6.1]

### 확인이 필요한 한계
선크림의 당시 용기 상태는 미상이에요.

## syn-sol-0343

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e499777dbc334a985aee9d273d4e23cb8a0ddc1b475ed0a1d6a0ee234cdf7fdc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "예전 버전은 분무형이었어요. 같은 이름의 현재 버전이 분무형인지 용기 사진에서 확인되지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P09",
      "status": "unknown",
      "guidance": "현재 용기의 형태를 확인하기 전 예전 버전의 사용법을 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P09@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 용기의 제품 형태와 사용 지침을 확인해요. [kb:B-P09@0.6.1]

### 근거 및 이유
이전 버전이 분무형이었다는 사실만으로 현재 제품 형태를 정하지 않아요. [kb:B-P09@0.6.1]

### 확인이 필요한 한계
현재 버전의 형태는 미상이에요.

## syn-sol-0344

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `509194900e665569883413aefaa134615126b57a65f940499ebde753a75ac1a9`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가 선크림의 사용기한은 보이지 않아요. 나 선크림에는 정상 이층 안내가 있지만 가의 제형 안내는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "unknown",
      "guidance": "나의 제형 안내를 가에 적용하지 않고 가의 기한과 안내를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가 용기의 사용기한과 제형 안내를 확인해요. [kb:B-P08@0.6.1]

### 근거 및 이유
나 용기의 정상 이층 안내를 가에 옮겨 적용하지 않아요. [kb:B-P08@0.6.1]

### 확인이 필요한 한계
가의 기한과 정상 외관은 미상이에요.

## syn-sol-0268

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4a26a5b73b8aaf3412fa2bdd134e776a357784b627199f0e4b8f44d79d67d262`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_repeat": true,
        "reason": "단순한 잔여감 해소",
        "additional_removal_purpose": false,
        "consecutive_face_wash_count": 2
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "handwashing_for_work": "separate",
        "face_additional_contamination_removal_purpose": false,
        "face_makeup_removal_purpose": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "difference",
      "guidance": "필요한 손 위생은 유지하면서 단순 잔여감 해소를 위한 얼굴 반복을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
업무상 필요한 손 씻기는 유지하고, 얼굴을 잔여감 때문에 연속 두 차례 씻는 부분을 따로 살펴봐요. [kb:B-C05@0.6.1]

### 근거 및 이유
추가 오염이나 화장 제거 목적은 없다고 보고됐어요. 얼굴의 반복을 줄일 수 있는지 검토할 수 있어요. 일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
손 위생과 얼굴 세안을 같은 행동으로 묶지 않으며 개인의 결과를 예측하지 않아요.

## syn-sol-0269

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `dc3ae059199f9b237fd3bf2673566b237ab908ae5706c7832a5808b3bcf4ca20`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
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
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "hand_washing": {
          "frequency": "여러 번",
          "context": "업무상"
        },
        "face_washing": {
          "frequency": "unknown",
          "purpose": "unknown"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "손 세정 횟수만으로 얼굴 세안의 차이를 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
업무상 손을 여러 번 씻는다는 사실을 얼굴의 반복 세안으로 옮기지 않아요. 얼굴 세안 횟수와 목적은 미상이에요 [kb:B-C05@0.6.1].

### 근거 및 이유
얼굴 세정에서는 얼굴 세안에서 제거 이유 없는 습관적 반복을 비교해요 [kb:B-C05@0.6.1]. 제공된 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
필요한 손 위생을 줄이라는 뜻이 아니며 얼굴의 실제 횟수와 목적을 확인해야 해요.

## syn-sol-0270

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `39843b696f9b6e39cb01dcb263fd79adf2bc91e8a0b46f6743cc9af96f3cfbfd`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "extra_wash_reason": "얼굴의 흙",
        "automatic_repeat": false,
        "context": "실외 작업 중 평소 세안 외 추가"
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
      "status": "aligned",
      "guidance": "흙 제거라는 별도 목적을 고려하며 횟수만으로 차이를 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
실외 작업 중 얼굴에 흙이 묻어 평소 세안 외에 씻으셨군요. 추가 세정의 맥락을 살피며 횟수만으로 불필요한 반복이라고 보지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
흙이 실제로 완전히 제거됐는지는 확인되지 않았어요.

## syn-sol-0271

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `2d55d1d8ca91aa8c51e21a578aee9760a44ed0384f481e0c090ebafb8595a7bd`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "extra_step_reason": "unknown",
        "second_step_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "sweat_after_exercise": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "운동 후 세안과 추가 단계의 이유를 구분해 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
운동 후 땀이 난 것은 확인됐지만 같은 세안의 두 번째 단계가 어떤 목적이었는지는 미상이에요. [kb:B-C05@0.6.1]

### 근거 및 이유
운동 후 세안과 추가 단계의 목적은 별도로 살펴요. 일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
추가 단계가 불필요했다고 단정하지 않아요.

## syn-sol-0272

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5c17abd19f09d0702d3bfc04a5ccd478be09cfe399c1c1043ff5cd994e9f4069`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "cleansing_device": {
          "owned": true,
          "used_on_face": "unknown",
          "pressure": "unknown"
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
      "guidance": "기기 보유만으로 얼굴 마찰을 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
세정 기기를 갖고 있지만 얼굴에 사용했는지와 힘은 미상이에요. 소유만으로 얼굴에 강한 마찰이 있었다고 판단하지 않아요 [kb:B-C02@0.6.1].

### 근거 및 이유
얼굴 세정에서는 손가락 외 도구의 사용과 강한 마찰을 구분해요 [kb:B-C02@0.6.1]. 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
얼굴 사용 여부와 사용했다면 압력을 확인해야 해요.

## syn-sol-0273

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ce2309227408089a96184f8671761f92b162744d7934a672b914397a7b86120a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "face_towel_rubbing": "strong",
        "device_site": "hands"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "site": "hands",
        "purpose": "세정"
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
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "site": "face",
        "tool": "수건",
        "intensity": "strong",
        "timing": "세안 후"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "손의 기기 사용과 별개로 얼굴의 강한 수건 마찰을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
손에 사용하는 세정 기기와 별개로, 얼굴은 세안 뒤 수건으로 강하게 문지른다고 하셨어요. 얼굴의 강한 마찰을 줄이고 물기를 가볍게 닦는 방법을 살펴봐요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 세안 안내는 부드러운 세정과 헹굼을 설명해요. [ref:S03]

### 확인이 필요한 한계
손의 기기를 얼굴에도 사용했다고 추정하거나 피부 문제의 원인을 단정하지 않아요.

## syn-sol-0275

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2d4d77d9f86f32f728c33ad7f11efe64266cf9ed63bb952868677f17a7066dd7`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "device_used_on_face": false,
        "towel_pressure": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "기기를 쓰지 않는 사실만으로 수건 마찰까지 확인된 것은 아니에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 기기를 쓰지 않더라도 수건으로 말릴 때의 압력은 알 수 없어요. [kb:B-C02@0.6.1]

### 근거 및 이유
기기 사용 여부와 건조할 때의 접촉은 다른 행동이에요. 일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
기억하지 못하는 압력을 추정하지 않아요.

## syn-sol-0276

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `49934636fc21a22c6d276a4f6757475754780bec5deb7912580986280a18f780`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "used_water_resistant_product": {
          "removal_instruction": "unknown"
        },
        "other_product": {
          "removal_instruction": "confirmed"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "다른 제품의 표시를 사용 제품에 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "소규모 영상 연구는 제한된 선크림과 세정 방법의 제거를 비교했어요. 그 결과로 모든 내수성 제품의 제거 방법을 일률적으로 정할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
사용한 내수성 제품의 제거 표시는 확인되지 않았고 확인된 표시는 다른 제품의 것이에요. 그 표시를 사용 제품에 그대로 적용하지 않아요.

### 근거 및 이유
선크림 제거에서는 내수성 표시만으로 무조건 반복 세안하는 행동을 검토해요 [kb:B-I01@0.6.1]. 소규모 영상 연구의 제한된 조합으로 모든 제품의 제거법을 일률적으로 정할 수 없어요 [ref:S08].

### 확인이 필요한 한계
사용한 제품의 해당 버전과 제거 지시가 여전히 미상이에요.

## syn-sol-0277

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d72e0888dcec31fea882257655073c4f7b3a2e1a8e9d326cf69836c47b24563e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
        "automatic_multi_step_for_water_resistant": true
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
        "automatic_multi_step_for_water_resistant": true,
        "frequency": "매번",
        "reason": "실제 사용 제품의 내수성 표시만"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "내수성 표시만을 근거로 고정한 반복 단계를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "A small imaging study compared removal across a limited set of sunscreen and cleansing methods. Its findings do not establish a universal removal method for every water-resistant product.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습을 고려하는 일반 안내가 있어요. 필요한 손 위생을 줄이라는 뜻은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
실제 사용한 제품의 내수성 표시만 보고 매번 세 단계로 씻고 계시군요. 광보호는 유지하면서 해당 제품의 제거 지시와 실제 필요를 살펴 단계가 필요한지 검토해요. [kb:B-I01@0.6.1]

### 근거 및 이유
소규모 비교는 제한된 제품과 세정법만 다뤄 모든 내수성 제품에 같은 제거법을 정하지 않아요. [ref:S08]

### 확인이 필요한 한계
이 정보만으로 특정 단계 수가 모든 제품에 충분하다고 단정할 수 없어요.
