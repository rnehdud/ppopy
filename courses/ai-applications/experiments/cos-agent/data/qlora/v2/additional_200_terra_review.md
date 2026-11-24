# PPO-39 보완 — additional_200_terra

`development_preview`, `production_enabled=false`, 합성 개발 후보이며 공식 인수·사람 승인이 아니에요.
원문 관찰을 정형 슬롯과 연결하고 사례별 설명을 보완했어요. 전체 판단과 과거 기록은 README 및 `ppo39_revisions.json`을 확인해요.
KB 판정은 비교 명세에 대한 작성 기록이며 엔진 실행이나 임상 결과가 아니에요. 저장 문헌 청크는 요약이며 외부 원전의 직접 인용이 아니에요.

## syn-sol-0346

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bb86b4478014ec6d8c2ca4b2e377b1e51067fd56cfd05c37fd4b93058908a4eb`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
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
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "additional_consecutive_repetition": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face_washes": [
          {
            "timing": "before_exercise",
            "count": 1
          },
          {
            "timing": "after_exercise_and_sweating",
            "count": 1
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "aligned",
      "guidance": "운동 뒤 땀을 씻는 목적은 운동 전의 세안과 구분해요."
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
운동 전 한 번 씻고 땀이 난 운동 뒤 다시 한 번 씻은 것은 별도 상황의 세안이에요. 다른 연속 반복은 하지 않았다고 보고됐어요. [kb:B-C05@0.6.1]

### 근거 및 이유
운동 전 세안과 운동 후 땀이 난 뒤의 세안은 시간상 별도로 기록됐어요. 세안 목적은 명시되지 않았어요. 일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
이 기록만으로 개인의 결과를 확정하지 않아요.

## syn-sol-0351

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8f84b631f086a0555d63a2a43e24988845aa911b335feacc2a38e4e18e340a72`
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
        "face_cleansing": {
          "tool": "천",
          "friction_intensity": "unknown",
          "context": "일상"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "천"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "unknown",
        "reason": "기억나지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "얼굴에 천을 쓴 점을 살펴보되 강한 마찰까지 단정하지 않아요."
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
일상 얼굴 세안에 천을 사용하셨어요. 손가락 외 도구 사용은 살펴볼 수 있지만 힘을 기억하지 못하므로 강하게 문질렀다고 단정하지 않아요 [kb:B-C02@0.6.1].

### 근거 및 이유
얼굴 세정에서는 도구 사용과 강한 마찰을 별개로 비교해요 [kb:B-C02@0.6.1]. 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
문지르는 힘은 기억나지 않아 미상이며 개인에게 나타날 결과도 확정할 수 없어요.

## syn-sol-0352

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cc7309131b3662ca6e52e1a38f8814bb95169e964264f01955cab46578ca72f2`
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
        "장갑 낀 손가락"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "intensity": "strong",
        "repeated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "context": "일상 얼굴 세안",
        "symptoms": "보고하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "얼굴에 강한 반복 마찰을 주는 현재 방법을 부드럽게 바꾸는 것을 검토해요."
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
일상 세안 때 장갑 낀 손가락으로 얼굴을 강하게 반복 문지른다고 하셨어요. 강한 마찰을 줄이고 손으로 부드럽게 씻는 방법을 살펴봐요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
증상은 보고되지 않았으며 현재 방법만으로 개인의 결과를 확정하지 않아요.

## syn-sol-0357

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `4ef2144591b65441fb9e98a917a264dc6e30a06032fe38d55919d616423e62c6`
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
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "separate_contact_time_instruction": false
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "intentional_long_contact": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "별도 접촉시간 지시가 없는 이 헹굼형 세정제는 일부러 오래 올려두지 말고 부드럽게 사용한 뒤 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
별도 접촉시간 지시가 없는 헹굼형 얼굴 세정제는 일부러 오래 올려두지 않고 부드럽게 사용한 뒤 헹궈요. [kb:B-C03@0.6.1]

### 근거 및 이유
현재는 일부러 오래 올려둔 후 헹군다고 보고됐어요. 일반 세안 자료도 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
기록에 없는 접촉 시간이나 개인의 결과는 추정하지 않아요.

## syn-sol-0361

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4f5ea30c8cc5be3ff11565edaf770be983beb4e2704b6b99b714e747ff8e5be7`
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
        "cleanser": {
          "type": "일반 헹굼형",
          "separate_contact_time_instruction": false
        },
        "face_cleansing": {
          "deliberate_prolonged_rubbing": true,
          "purpose": "충분히 작용시키기",
          "rinsed_after": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "deliberate_prolonged_rubbing": true,
        "purpose": "충분히 작용시키기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "rinsed_after_rubbing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "일부러 오래 문지르기보다 세정제를 부드럽게 사용한 뒤 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
일반 헹굼형 세정제가 충분히 작용하도록 일부러 오래 문지른다고 하셨어요. 별도 시간 지시가 없다면 오래 문지르기보다 부드럽게 사용하고 헹구는 쪽을 검토해요 [kb:B-C03@0.6.1].

### 근거 및 이유
일반 세정제 사용에서는 별도 지시 없이 일부러 오래 문지르거나 올려두는 경우를 다루며 경과 시간만으로 차이를 만들지 않아요 [kb:B-C03@0.6.1]. 일반 자료도 부드러운 세정과 헹굼을 설명해요 [ref:S03].

### 확인이 필요한 한계
정확한 접촉 시간은 보고되지 않았고 개인의 결과를 예측할 수 없어요.

## syn-sol-0362

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1b55caa375f26d3490c371a136d95b583fecc39387687b5d4fdc9cb4f05897fe`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "씻어내기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": false,
        "reason": "시간을 줄이기 위해"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product": "일반 얼굴 세정제",
        "used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "시간을 줄이려고 헹굼을 생략하지 말고 이 제품의 표시대로 사용 후 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
씻어내도록 표시된 얼굴 세정제를 사용한 뒤 시간을 줄이려 헹굼을 생략하고 계시군요. 이 제품은 표시대로 사용 후 헹구는 방법을 살펴봐요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반 얼굴 세안 안내에서도 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
제품별 용법은 다를 수 있으며 이 행동만으로 개인의 결과를 확정하지 않아요.

## syn-sol-0365

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4c7c7aacc9073957207db7c1cac8cc53a21c56e4de18d52680a602c5ca340c6c`
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
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true,
        "consistent_with_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "other_cleanser_used_after": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "확인된 그 제품의 헹굼은 표시와 일치해요. 다른 제품 사용 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
얼굴에 사용한 헹굼형 세정제 하나는 표시대로 헹군 것으로 확인됐어요. 그 제품에 관한 헹굼을 유지해요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
이후 다른 세정제를 사용했는지는 기억하지 못하므로 미상이에요.

## syn-sol-0366

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `034a244dc42f8811f46cc18dd3688b460c5c2b97e8f84ef9dced9db6e99adac4`
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
        "sunscreen": {
          "application_amount": "표시 사용량보다 극소량",
          "reason": "저녁 제거가 번거로움",
          "actual_removal_method": "unknown"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "relative_to_label_amount": "극소량"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "제거를 편하게 하려고 도포량을 극소량으로 줄이기보다 표시된 사용량 등 광보호 요건을 유지하고 해당 제품의 제거 지시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
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
저녁에 지우기 번거로워 얼굴 선크림을 표시보다 극소량만 쓴다고 하셨어요. 제거 편의 때문에 광보호에 필요한 사용량을 줄이기보다 해당 제품의 표시와 제거 방법을 확인해요 [kb:B-I01@0.6.1].

### 근거 및 이유
광보호와 제거를 함께 살필 때는 세안 부담 때문에 선크림을 극소량 쓰는 상황을 별도로 살펴요 [kb:B-I01@0.6.1]. 제한된 조합의 소규모 연구는 제거 결과가 방법에 따라 달랐지만 모든 제품에 특정 단계를 일반화하지 않아요 [ref:S08].

### 확인이 필요한 한계
실제 제거 방법은 미상이며 개인 보호 수준은 이 기록으로 계산할 수 없어요.

## syn-sol-0367

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4bc8c650b6d05fb138a7af0a8fbb5d7b6925b691d3189dfb9ef980c5603d4cac`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": true,
        "frequency": "매번",
        "count": 3,
        "additional_removal_instruction": false,
        "additional_soiling": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product": "내수성 얼굴 선크림",
        "used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "내수성 표시만으로 세 번 반복하기보다 광보호 사용을 유지하면서 해당 제품의 제거 지시와 실제 제거 필요에 맞춰 세안 단계를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
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
내수성 표시만을 이유로 매번 세 번 연속 세안하고 계시군요. 광보호는 유지하면서 실제 제거 필요에 맞게 반복 단계를 검토해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품을 비교한 소규모 연구에서 결과는 세정법에 따라 달랐고, 모든 내수성 제품에 특정 단계 수를 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
별도 제거 지시나 추가 오염은 보고되지 않았으며 특정 횟수가 언제나 충분하다고 볼 수 없어요.

## syn-sol-0382

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `cee4e713faee09414e23f5a64e9ff5862df9b77f67ef9125dc5c32fcef294ffd`
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
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "two_lotions_premixed_in_same_container": true,
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "mixing_instructions_confirmed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "clinician_mixing_instruction": "not_reported"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "확인되지 않은 사전 혼합을 기본 사용법으로 삼지 않도록 검토해요."
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
얼굴용 로션 두 개를 한 용기에 미리 섞어 쓰는 방식을 검토해요. 확인된 혼합 지시가 없는 상태라 사전 혼합을 기본 사용법으로 삼지 않아요. [kb:B-G04@0.6.1]

### 근거 및 이유
두 제품의 혼합 사용 지시는 확인되지 않았고 의료진 지시는 보고되지 않았어요.

### 확인이 필요한 한계
성분 농도나 혼합 후 개인 반응은 추정하지 않아요.

## syn-sol-0383

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `340e7741cb5bc5f7817c2e05870836fcbf7e4cdde215462d21dbabd8420a3b4a`
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
        "product_a": {
          "synthetic": true,
          "label": {
            "mix_with": "제품 B",
            "timing": "사용 직전"
          }
        },
        "actual_use": {
          "mixed": [
            "제품 A",
            "제품 B"
          ],
          "timing": "얼굴 사용 직전"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "products": [
          "제품 A",
          "제품 B"
        ],
        "timing": "사용 직전",
        "actual": true,
        "reported_label_directs_mixing": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "exception",
      "guidance": "확인된 해당 제품의 혼합 지시와 실제 사용을 함께 살펴요."
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
합성 제품 A의 확인된 표시는 지정 제품 B와 사용 직전에 섞으라는 내용이고 실제 얼굴 사용도 그 범위와 일치해요. 이 확인된 지시를 고려해요 [kb:B-G04@0.6.1].

### 근거 및 이유
제품 혼합에서는 근거 없는 사전 혼합·희석과 확인된 제품별 혼합 지시가 있는 경우를 구분해요 [kb:B-G04@0.6.1].

### 확인이 필요한 한계
이 예외를 다른 제품이나 다른 혼합 시점으로 확장할 수 없고 개인 반응도 알 수 없어요.

## syn-sol-0384

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6a8a20976e12e9aa095bd31c184e7ebb95a5536e62dd512d8b21cec34211199e`
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
        "product": "얼굴에 바르도록 만들어진 로션",
        "actual_use": "분사 용기에 옮겨 얼굴에 분사",
        "spray_conversion_instruction": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "분사 용기로 바꿔 쓰기보다 확인된 원래 제품의 도포 용법에 맞춰 사용해요."
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
바르도록 만들어진 얼굴 로션을 분사 용기에 옮겨 사용하고 계시군요. 분사 전환 지시가 확인되지 않았으므로 원래 도포 용법을 따르는 방향을 살펴봐요. [kb:B-G04@0.6.1]

### 근거 및 이유
용기를 바꿔 분사하는 것은 확인된 원래 사용 형태와 달라 별도의 근거 확인이 필요해요.

### 확인이 필요한 한계
해당 제품의 분사 전환 지시는 확인되지 않았고 개인에게 미친 결과도 알 수 없어요.

## syn-sol-0386

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `de8c316d52786d08bd38fd2a6ce82eb4daeaf6d1839767764a50e3e4d314a1a9`
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
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_and_lotion_used_together": true,
        "device_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "device_label_prohibits_this_lotion": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_despite_device_label_restriction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "difference",
      "guidance": "확인된 기기의 병용 제한을 따르도록 사용 방법을 재검토해요."
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

### 핵심 안내
얼굴용 기기와 로션을 함께 사용한 기록이 있지만 기기 표시에는 해당 로션을 병용하지 말라고 되어 있어요. 이 제한을 따르도록 사용을 재검토해요. [kb:B-G06@0.6.1]

### 근거 및 이유
실제 병용과 확인된 표시가 서로 달라요.

### 확인이 필요한 한계
이 기록만으로 개인의 반응이나 제품 성분 농도를 추정하지 않아요.

## syn-sol-0389

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `78c2baa06e96543cd5f8c7fe2f5c3a104a1f0d2876cca38ed22a75805f7ade6e`
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
        "device": {
          "type": "얼굴용 미용기기",
          "confirmed_label": {
            "compatible_gel": "해당 합성 얼굴용 젤",
            "body_site": "face"
          }
        },
        "actual_use": {
          "device_with_gel": true,
          "body_site": "face"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_and_named_gel_used_together": true,
        "actual_use_matches_confirmed_face_and_gel_instruction": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "aligned",
      "guidance": "확인된 해당 기기와 젤의 얼굴 사용은 표시된 지시와 일치하므로 그 지시 범위에서 유지할 수 있어요."
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

### 핵심 안내
얼굴용 기기와 합성 젤을 실제로 함께 쓰고 있으며, 확인된 기기 표시도 그 젤과 얼굴 사용을 명시해요. 확인된 지시 범위에서 유지할 수 있어요 [kb:B-G06@0.6.1].

### 근거 및 이유
기기 사용에서는 기기 지시를 벗어난 제품·부위 등의 사용을 비교하므로 해당 기기의 표시와 실제 조합을 함께 살펴요 [kb:B-G06@0.6.1].

### 확인이 필요한 한계
이 일치는 다른 젤이나 부위에도 적용된다는 뜻이 아니며 개인 반응을 보증하지 않아요.

## syn-sol-0390

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a07623691512029271604c1fdb24c82260e2ad9ce74fc591519c24347b23e975`
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_selection": "얼굴용 제품 선택 중",
        "label": "향료 표시",
        "belief": "모든 사람에게 금지해야 한다고 생각",
        "personal_allergy": "unknown",
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시에 있다는 이유만으로 모든 사람에게 금지된다고 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
향료가 표시된 얼굴 제품을 고르는 중이시군요. 표시가 있다는 사실만으로 모든 사람에게 금지된다고 판단하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
표시 자체가 개인에게 알레르기 반응이 생긴다는 증거는 아니에요. [ref:S15]

### 확인이 필요한 한계
본인의 알레르기 여부는 알려지지 않았고 개인별 회피가 필요한지는 별도 정보가 필요해요.

## syn-sol-0391

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `07c6801eeb9eac6765159a96459dcb9c254c9808ae5048e891b9b0400e0d4648`
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
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "named_fragrance_visible": false,
        "list_scope": "unknown",
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "asserted_fragrance_absent": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시에서 보이지 않는 사실만으로 성분이 전혀 없다고 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품의 확인된 목록에서 특정 향료명이 보이지 않더라도 그 물질이 전혀 없다고 확정할 수는 없어요. [kb:B-G17@0.6.1]

### 근거 및 이유
목록이 어떤 범위를 다루는지 확인되지 않았어요. 향료와 알레르겐 자료는 표시와 개인별 회피를 다뤄요. [ref:S15]

### 확인이 필요한 한계
성분 농도나 개인의 알레르기 반응은 이 기록으로 알 수 없어요.

## syn-sol-0396

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3b1c8342104ccc4b599ca6e8bd99dfda6545cdfd119e14d7a328b3205b58b9a3`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손을 씻은 뒤 현재 쓰는 핸드크림을 바르며 이 제품을 바를 때 불편하지 않아요. 필요한 손 위생은 유지하고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견딜 수 있는 손 보습을 개별 지시와 함께 살펴요."
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
손 씻은 뒤 현재 핸드크림을 쓰고 그때 불편하지 않다고 하셨어요. 필요한 손 위생을 유지하면서 현재 편안한 보습을 살필 수 있어요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습에서는 손을 계속 건조하게 두거나 반복적으로 불편한 특정 제품을 계속 쓰는 경우를 구분해요 [kb:B-M04@0.6.1]. 일반 손 관리 자료는 손 씻은 후 보습과 무향료 크림·연고를 다뤄요 [ref:S21].

### 확인이 필요한 한계
현재 편안하다는 보고가 앞으로의 반응이나 제품 전체의 안전성을 보장하지는 않아요.

## syn-sol-0398

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `69ddf1bee444da48455c44b55d9b841e96e8e5f4af5cb93c8a9bbc24267cd149`
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
        "site": "hands",
        "dryness": "있음",
        "moisturizing": "계속 하지 않음",
        "hand_hygiene": "유지"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "손 건조를 계속 방치하는 현재 행동을 검토해요."
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
손이 건조한데 보습을 계속하지 않고 계시군요. 필요한 손 위생은 유지하면서 견딜 수 있는 손 보습을 검토해요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 안내는 손을 씻은 뒤 보습을 다루며 필요한 손 위생을 대체하지 않아요. [ref:S21]

### 확인이 필요한 한계
어떤 제품을 견딜 수 있는지는 확인되지 않았어요.

## syn-sol-0399

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bde309ce51b194faae15d65b088e0162e88d7b182be79110b5b45e3a4b332713`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
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
      "value": "repeated",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "hand_cream": "continued_use",
        "other_products_reaction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "반복 불편이 있는 해당 제품의 사용을 검토해요."
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
손에 같은 핸드크림을 바를 때마다 불편한데 계속 사용하고 있어요. 반복해 불편한 그 제품의 사용 중단이나 대체를 검토해요. [kb:B-M04@0.6.1]

### 근거 및 이유
필요한 손 위생은 별도로 유지해요. 일반 손 관리 자료는 손 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
다른 제품에 대한 반응은 미상이고 불편의 원인도 확정하지 않아요.

## syn-sol-0400

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `61f945e6b764d3a34b8575523266b1ade11592c494ff659c9aff6e25608154da`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 씻은 뒤 핸드크림을 바르지만 용기의 향료 표시를 읽지 못했어요. 이 제품을 바를 때 불편하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견디는 제품의 유지와 미확인 표시를 구분해요."
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
손 씻은 후 쓰는 핸드크림은 현재 불편하지 않지만 향료 표시는 읽지 못했어요. 개인의 관찰과 표시 미확인을 구분해요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습에서는 손 보습을 유지하면서 제품별 불편을 살펴요 [kb:B-M04@0.6.1]. 일반 손 관리 자료는 무향료 크림·연고와 세정 후 보습을 다루지만 개인별 편안함을 보장하지 않아요 [ref:S21].

### 확인이 필요한 한계
향료 함유 여부는 표시를 읽기 전까지 미상이며 편안하다는 경험만으로 무향료라고 할 수 없어요.

## syn-sol-0402

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5cc7cce9e67a2c2c484737f14cecf0fffc7cbc9af19e9f7e3a76abff9133f8ae`
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
        "site": "hands",
        "product": "핸드크림",
        "label": "무향료",
        "reaction": "바를 때마다 불편",
        "use": "계속"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "무향료 표시와 그 제품의 반복 불편을 별도로 고려해요."
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
무향료로 표시된 핸드크림이지만 바를 때마다 불편하다면 그 제품의 중단과 견딜 수 있는 대안을 검토해요. 보습 전체를 그만두라는 뜻은 아니에요. [kb:B-M04@0.6.1]

### 근거 및 이유
무향료 선택에 관한 일반 안내가 있어도 개인의 제품 내성을 보장하지는 않아요. [ref:S21]

### 확인이 필요한 한계
불편의 원인과 대안에 대한 반응은 확인되지 않았어요.

## syn-sol-0410

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `36930f9a1e748db0c77b689e670afa28c3d6e9623ecf32e2511dc190e9db0f3d`
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
        "necessary_handwashing": "continued",
        "current_handcream": "after_washing",
        "clinician_instructions": "none",
        "current_handcream_discomfort": false,
        "handcream_intended_site": "hands"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "견딜 수 있는 현재 손 보습과 필요한 위생을 함께 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
필요한 손 씻기와 씻은 뒤 불편 없이 쓰는 현재 핸드크림을 함께 유지하는 방향으로 살펴요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 자료는 손 씻은 뒤 보습을 다루며 필요한 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
별도 진료 지시는 없다고 보고됐으며, 현재의 편안함이 모든 제품의 반응을 보증하지는 않아요.

## syn-sol-0412

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `448d7bc0a9acfab089b4be309432c49fcd0c9b4ebc61807db44c7b414d8d4fe6`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "이전 핸드크림은 손에 불편했어요. 지금 쓰는 다른 핸드크림은 편안하고 손 씻기 후 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "이전 제품의 불편과 현재 제품의 관찰을 나누어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
이전 핸드크림의 불편과 지금 사용하는 다른 제품의 편안함은 서로 다른 관찰이에요. 현재 손 씻기 후 보습을 살피되 이전 반응을 현재 제품에 옮기지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습에서는 특정 제품의 반복 불편과 손 보습 유지 여부를 함께 살펴요 [kb:B-M04@0.6.1]. 일반 손 관리 자료는 씻은 뒤 보습과 무향료 제품 선택을 다뤄요 [ref:S21].

### 확인이 필요한 한계
이전 제품의 불편 원인은 확인되지 않았고 현재 제품의 미래 반응을 보증할 수 없어요.

## syn-sol-0416

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6d1668ddae388d315fe4f13ca111b0666b95071c7860652ddcf1f32fe1d8f084`
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
        "handwashing_after": "편안한 핸드크림 사용",
        "other_wet_work": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견디는 손 보습을 유지하면서 작업 정보는 미상으로 두어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손을 씻은 뒤 편안하게 쓰는 핸드크림은 유지해요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 안내는 손 씻기 후 보습을 다루며 필요한 손 위생을 줄이라는 뜻이 아니에요. [ref:S21]

### 확인이 필요한 한계
다른 젖은 작업이 있는지는 아직 확인되지 않았어요.

## syn-sol-0417

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `de2fbd24b7f08c97c1e52e2df498c9e610bf61091b5a4c83f8908bac52ee5bae`
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
        "necessary_handwashing": "continued",
        "handcream": "continued_despite_discomfort",
        "discomfort_when_using_handcream": "repeated"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "필요한 손 위생과 특정 제품의 반복 불편을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
핸드크림을 바를 때마다 불편했다면 그 제품의 중단이나 대체를 검토해요. 필요한 손 씻기는 계속해요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 위생과 특정 크림의 반복 불편은 분리해서 살펴요. 손 관리 자료는 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
이 기록만으로 불편의 원인을 확정하지 않아요.

## syn-sol-0418

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4264ddc7391d25aeae16b8b0bf6f74d5bd41f0fe7eae3439e303d0f5228441d5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 건조하다고 느끼는데 보습제를 모두 끊고 손을 계속 건조하게 두어요. 진단받은 질환은 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "손을 계속 건조하게 두는 행동을 검토하되 진단은 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손이 건조하게 느껴지는데 보습제를 모두 끊고 계속 건조하게 두고 계세요. 견딜 수 있는 손 보습을 다시 검토할 수 있어요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습 기준은 손을 계속 건조하게 두는 행동과 특정 제품에 반복되는 불편을 구분해요 [kb:B-M04@0.6.1]. 일반 손 관리 안내는 씻은 뒤 보습과 무향료 크림·연고를 다뤄요 [ref:S21].

### 확인이 필요한 한계
진단받은 질환은 보고되지 않았으며 건조감만으로 원인이나 진단을 확정하지 않아요.

## syn-sol-0422

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `b260ec50e9cc5a214947b8373116b96cda844ac9817cad8caaea572fe5e89b0e`
- 사람 검수: **미검수**

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
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "type": "수동 날면도",
        "direction": "털 방향",
        "repeat_passes": "줄임",
        "movement": "가볍게"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 부드러운 수동 면도 방법을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 면도 때 털 방향으로 가볍게 움직이고 반복 통과를 줄이는 현재 방법을 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
수동 면도 안내도 털 방향과 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
확인한 면도 방법만으로 도구 상태나 개인의 결과를 보장하지 않아요.

## syn-sol-0423

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `08ed037382737ccc259e9e23d9fc02215e17ebeb82c10d2da23a18bf15038413`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "manual_razor"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "pressure": "not_strong",
        "direction": "with_hair_growth",
        "same_area_repeated": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 압력과 방향, 반복 관리에 한정해 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 수동 날면도할 때 강하게 누르지 않고 털 방향으로 움직이며 같은 곳을 반복하지 않는 확인된 동작을 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
일반 수동 면도 자료도 털이 자라는 방향과 부드러운 면도를 다뤄요. [ref:S23]

### 확인이 필요한 한계
날 개수나 모든 사람의 면도 빈도를 정하는 안내는 아니에요.

## syn-sol-0424

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `1c264b3d86965a63caa8b2b75a1ba16f05c24c054bf4f2496b255ed5d2c68104`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴의 턱을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 같은 곳의 반복 통과를 줄여요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 얼굴 수동 면도 방법을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
턱을 수동 날면도할 때 털 방향으로 가볍게 움직이고 같은 곳의 반복 통과를 줄인다고 하셨어요. 확인된 이 방법을 유지할 수 있어요 [kb:B-G10@0.6.1].

### 근거 및 이유
면도 기준은 강한 역방향·압력이나 반복 통과를 고수하며 불편을 무시하는 상황을 살펴요 [kb:B-G10@0.6.1]. 일반 수동 면도 안내도 털 방향과 부드러운 동작을 다뤄요 [ref:S23].

### 확인이 필요한 한계
이 관찰만으로 개인의 모든 면도 반응이나 적절한 빈도를 확정하지 않아요.

## syn-sol-0427

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8983777a11ab3ed95d8f72d1eba23a3fbdcdce046a2833af1d26c4a7b2f18160`
- 사람 검수: **미검수**

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
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "type": "수동 날면도",
        "pressure": "강하게",
        "repeat_passes": "같은 곳 여러 번",
        "purpose": "매끈함",
        "discomfort": "있어도 계속"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "difference",
      "guidance": "불편을 무시한 강한 압력과 반복 통과를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
불편해도 매끈함을 위해 강하게 누르고 같은 곳을 여러 번 면도하고 계시군요. 압력과 반복 통과를 줄일 여지를 살펴봐요. [kb:B-G10@0.6.1]

### 근거 및 이유
수동 면도 안내는 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
면도 방향이나 날 상태는 확인되지 않았고 불편의 원인을 단정하지 않아요.

## syn-sol-0428

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `90d285c4f0ade2cb5564184c24d154cf1d60770ae980af6ca78723ef2d5de8cb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "manual_razor"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "shaving_direction": "against_hair_growth",
        "continued_despite_discomfort": true,
        "purpose": "smoothness",
        "shaving_intensity": "strong"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "difference",
      "guidance": "불편을 무시한 강한 역방향 면도를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 면도할 때 불편을 무시하며 강하게 역방향으로 미는 방법을 조정해요. [kb:B-G10@0.6.1]

### 근거 및 이유
매끈함을 위해 계속한 동작이에요. 일반 수동 면도 안내는 털이 자라는 방향과 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
이 기록으로 원인이나 개인 결과를 확정하지 않아요.

## syn-sol-0430

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `94092f656d44c9fb2b85a97c49db1e3fe69032c903ec11366d2138ccc264e4b3`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "예전에 얼굴 수동 날면도에서 강하게 눌렀어요. 현재는 털 방향으로 가볍게 움직이고 반복 통과를 줄여요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "이전 동작과 확인된 현재 동작을 나누어 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
과거에는 날면도 시 강하게 눌렀지만 현재는 털 방향으로 가볍게 움직이고 반복 통과를 줄인다고 하셨어요. 확인된 현재 동작을 기준으로 살펴요 [kb:B-G10@0.6.1].

### 근거 및 이유
면도 방법에서는 매끈함을 위해 강한 압력이나 반복 통과를 고수하면서 불편을 무시하는 경우를 비교해요 [kb:B-G10@0.6.1]. 일반 수동 면도 안내도 털 방향과 부드러운 동작을 다뤄요 [ref:S23].

### 확인이 필요한 한계
과거 행동을 현재 습관으로 간주하지 않으며 면도 빈도나 날 개수를 일률적으로 정하지 않아요.

## syn-sol-0431

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `0ee3ed5bd6f8144a4f413f9c7e5d0d72cc3e98749d66d2e534b5adfd7a53a4fc`
- 사람 검수: **미검수**

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
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "type": "수동 날면도",
        "direction": "털 방향",
        "repeat_passes": "줄임",
        "blade_count": "unknown",
        "movement": "가볍게"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 방법을 살피며 날 개수를 추측하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "수동 날면도 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. 준비와 면도날 관리도 함께 안내해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 털 방향으로 가볍게 면도하고 반복 통과를 줄이는 방법을 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
수동 면도 안내는 털 방향과 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날 개수는 확인하지 못했으므로 추측하지 않아요.

## syn-sol-0432

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `9637743970dbacc149e4b9be88f4df2c9b7f878fc043e5c062c15cd9a114a569`
- 사람 검수: **미검수**

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
        "current_moisturizer": "after_shaving",
        "response": "comfortable",
        "separate_aftershave_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "견딜 수 있는 면도 후 보습을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
얼굴 면도 뒤 편안하게 사용하는 현재 보습을 유지해요. 별도 애프터셰이브를 반드시 추가할 필요는 없어요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 피부 관리 자료는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
현재 제품에 편안한 경험을 다른 제품 전체에 확대하지 않아요.

## syn-sol-0433

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `085795c25191c97cfabb5c3e5ee4535ab1db93965bbfb92328c4886fc3bd30b6`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 후처리 제품을 바를 때마다 따갑지만 흡수되는 느낌이라며 계속 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "difference",
      "guidance": "반복 따가움을 흡수 효과로 해석해 계속 사용하는 행동을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
목 면도 후 제품을 바를 때마다 따가운데 흡수되는 느낌이라며 계속 쓰고 있어요. 그 반복 반응을 효과로 해석하기보다 해당 후처리 제품의 중단이나 대체를 검토해요 [kb:B-M05@0.6.1].

### 근거 및 이유
면도 후 관리에서는 반복 따가움을 흡수나 소독 효과로 여기며 견디는 경우를 살펴요 [kb:B-M05@0.6.1]. 일반 자료는 면도 후 보습을 다뤄요 [ref:S25].

### 확인이 필요한 한계
이 제품의 반응만으로 모든 보습 제품이나 면도 자체가 원인이라고 할 수 없어요.

## syn-sol-0437

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5247f02552ec4e19f03d31485b9a68e6579013ca91b965a8c4eed5380f862ae8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "after_shave": "보습 필요 느낌",
        "specific_aftercare": "따가움",
        "all_moisturizing": "중단"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "difference",
      "guidance": "특정 후처리 제품의 반응과 보습 전체 중단을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
목 면도 뒤 보습이 필요하지만 한 후처리 제품이 따가워 모든 보습을 중단하셨군요. 불편을 주는 제품과 보습 전체를 구분해 견딜 수 있는 보습을 살펴봐요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 안내는 면도 후 보습과 무향료 제품 선택을 다뤄요. [ref:S25]

### 확인이 필요한 한계
따가움의 원인과 다른 제품에 대한 반응은 확인되지 않았어요.

## syn-sol-0438

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `dd12c3266cb1cc66a23c49c3d76beaa100939f30faca9f8091b0dc0b5082ccc6`
- 사람 검수: **미검수**

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
        "past_aftercare_product": {
          "timing": "after_shaving",
          "response": "stinging"
        },
        "different_current_moisturizer": {
          "response": "comfortable"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "예전 후처리 제품과 현재 견디는 보습제를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
예전 후처리 제품의 따가움과 현재 다른 보습제의 편안한 사용 경험은 구분해요. 현재 견디는 보습은 유지할 수 있어요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 피부 관리 자료는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
예전 반응의 원인이나 다른 모든 제품의 반응을 확정하지 않아요.

## syn-sol-0439

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `edda4472cc5c1b6326ec4f005c6e22ffe9e3d3f40701a7b5fbef3c11cd3fbc96`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 보습제를 사용해 편안해요. 별도 애프터셰이브는 사용하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "확인된 편안한 보습을 살피며 별도 상품을 강제하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
목 면도 후 보습제가 편안하고 별도 애프터셰이브는 쓰지 않는다고 하셨어요. 편안한 보습을 유지하며 별도 상품을 필수로 추가하지 않아도 돼요 [kb:B-M05@0.6.1].

### 근거 및 이유
면도 후 관리에서는 반복 따가움을 견디거나 모든 보습을 중단하는 행동을 살펴요 [kb:B-M05@0.6.1]. 일반 자료는 면도 후 보습을 설명해요 [ref:S25].

### 확인이 필요한 한계
현재 제품의 편안함이 다른 제품의 반응이나 향후 결과를 보증하지 않아요.

## syn-sol-0440

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3d606bf1eb7b2789d5a97f1141b5e1107613e9fcc056225aa371b8c1b73c78d2`
- 사람 검수: **미검수**

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
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "products": [
          {
            "purpose": "레티놀 관리",
            "type": "화장품"
          },
          {
            "purpose": "AHA 각질관리",
            "type": "화장품"
          }
        ],
        "timing": "같은 저녁 루틴",
        "site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "같은 부위의 별도 관리제품 중첩을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
레티놀 관리제와 AHA 각질관리제를 같은 저녁 얼굴에 따로 겹쳐 쓰고 계시군요. 중첩을 줄이고 필요한 관리 한 가지를 우선할지, 사용 경험과 제품 표시를 함께 살펴봐요. [kb:B-G13@0.6.1]

### 근거 및 이유
일반 안내는 레티놀 사용 중 추가 각질관리에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
개인의 반응이나 위해 확률은 이 정보로 알 수 없어요.

## syn-sol-0441

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ecc0f314a4bb8179d2b9ba461ce9f64b15df174bbd62329c179b961b8129e834`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "products": [
          "retinol_skincare_cosmetic",
          "aha_exfoliating_cosmetic"
        ],
        "same_period": true,
        "same_use_days": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "같은 부위와 겹치는 사용기간을 확인하고 날짜 분리만으로 적합하다고 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
목에 쓰는 레티놀과 AHA 화장품은 사용일이 달라도 같은 기간에 겹쳐요. 두 제품의 중첩을 줄이고 필요한 관리 한 종류를 우선 검토해요. [kb:B-G13@0.6.1]

### 근거 및 이유
일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 추가 각질제거에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이 보수적 안내는 절대 금기나 개인의 위해 확률을 뜻하지 않아요.

## syn-sol-0445

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `940b0362e0663f23d3f34312940485bf69d5b14dd97e58badb1e2408c417dc55`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "레티놀 관리용 화장품은 얼굴에, AHA 각질관리용 별도 화장품은 손에 같은 기간 사용해요. 두 제품의 실제 접촉 부위는 겹치지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "exception",
      "guidance": "확인된 다른 부위에 동일 부위 중첩을 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
레티놀 제품은 얼굴, 별도 AHA 각질관리 제품은 손에 사용하며 접촉 부위가 겹치지 않아요. 이 사실에 같은 부위 중첩 판단을 적용하지 않아요 [kb:B-G13@0.6.1].

### 근거 및 이유
중첩을 살피는 기본 대상은 같은 부위의 별도 레티노이드와 AHA 각질관리 제품이에요 [kb:B-G13@0.6.1]. 일반 각질관리 자료는 레티놀·처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요 [ref:S32].

### 확인이 필요한 한계
이것은 개인별 위해 확률이나 절대 금기를 확정하는 판단이 아니에요.

## syn-sol-0446

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ac0c1e1066f0086c98e2ce48011088a038166fdf4a58de91fd689405c4b4daae`
- 사람 검수: **미검수**

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
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "single_product": "레티놀과 AHA 복합 완제품",
        "other_same_purpose_products": "미사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "exception",
      "guidance": "단일 복합 완제품은 별도 제품 중첩과 나누어 제품별로 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 사용하는 것은 레티놀과 AHA가 함께 든 하나의 완제품이고 같은 목적의 별도 제품은 사용하지 않아요. 별도 제품 중첩과 구분해 이 제품의 표시와 사용 경험을 살펴봐요. [kb:B-G13@0.6.1]

### 근거 및 이유
각질관리 안내는 레티놀 사용 중 추가 관리에 주의를 권하지만 모든 조합의 개인별 결과를 정하지는 않아요. [ref:S32]

### 확인이 필요한 한계
복합 제품이라는 이유만으로 무자극이나 부적합을 확정하지 않아요.

## syn-sol-0449

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a1fa777dea67829902b9702e1c04a0b0a6eadea1151328251a18258ffb25cf96`
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
        "broad_spectrum_labeled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "planned_activity": "outdoor_swimming",
        "candidate_label_water_resistance": "not_water_resistant"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "difference",
      "guidance": "수영용 후보의 내수성 없음 표시가 선택 기본값과 달라요."
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
야외 수영용 새 후보에는 SPF 50과 광범위 보호가 표시됐지만 내수성은 없다고 표시돼 있어요. 수영 상황에 맞는 내수성 표시를 확인하며 후보를 비교해요. [kb:B-P01@0.6.1]

### 근거 및 이유
일반 야외용 선택 안내는 SPF, 광범위 보호, 내수성 표시를 함께 다뤄요. [ref:S16]

### 확인이 필요한 한계
표시만으로 개인의 실제 보호 수준을 보증할 수 없어요.

## syn-sol-0455

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `85cfd3e4fdc0dcf1240fd1150f5ecb96d345282e523158561eeff3a8b7b5c261`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 달리기용 새 합성 자외선차단제의 현재 용기에는 SPF 15, 광범위 보호 및 내수성이 표시돼 있어요. 실제 사용은 아직 하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "difference",
      "guidance": "표시된 SPF 15는 야외 후보의 SPF 30 선택 기본값보다 낮아요."
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
아직 사용하지 않은 야외 달리기용 합성 후보의 SPF 15 표시는 야외 선택 기본값보다 낮아요. 후보 선택을 다시 검토할 수 있어요 [kb:B-P01@0.6.1].

### 근거 및 이유
일반 야외 광보호 안내는 SPF 30 이상과 광범위 보호·내수성 표시를 함께 확인하도록 권해요 [ref:S16]. 이 후보에는 광범위 보호와 내수성 표시가 있어요.

### 확인이 필요한 한계
표시만으로 개인의 실제 보호 결과나 제품 전체의 안전성을 보증할 수 없어요.

## syn-sol-0456

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1a50ac638f504db1aa43f186397d1747afed89b1f1d69922f0bce595b6b553b4`
- 사람 검수: **미검수**

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
        "activity": "야외 산책",
        "product_label_sites": [
          "face",
          "ears"
        ],
        "applied": [
          "face"
        ],
        "intentionally_omitted": [
          "exposed ears"
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "제품 표시 범위에 포함된 노출 귀를 빠뜨리지 않도록 표시된 용법에 맞춰 발라요."
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
야외 산책 때 얼굴에는 바르고 노출된 귀는 일부러 빼셨군요. 제품이 귀에도 사용 가능하다고 표시되어 있으므로 표시 용법에 맞춰 누락된 부위도 살펴봐요. [kb:B-P02@0.6.1]

### 근거 및 이유
노출 부위의 의도적인 누락은 사용 범위와 함께 확인할 항목이에요.

### 확인이 필요한 한계
이 정보만으로 실제 보호 수준을 계산할 수 없어요.

## syn-sol-0458

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `460a05814c0c434c789a170470d16b4f715cea2ff707f3e0eb07b475641c408d`
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
      "guidance": "확인된 사용 제한과 노출 부위를 함께 살펴요."
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
야외에서 얼굴과 귀가 노출됐지만 사용 제품은 귀를 제외하도록 표시돼 있어요. 이 제한을 무시하고 귀에 바르라고 권하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
귀에 바르지 않은 이유를 제품 표시의 사용 범위와 연결해 살펴요.

### 확인이 필요한 한계
이 정보로 실제 보호 수준이나 다른 제품의 적합성을 계산하지 않아요.

## syn-sol-0459

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d95d3d48252c9c42edca54778859ec28c0d741e86beb3cf567e6e46b46615806`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 얼굴에 사용할 합성 자외선차단제를 쓰면서 노출된 얼굴의 이마는 끈적임을 피하려고 일부러 빼고 발랐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "얼굴용 제품의 표시된 용법에 맞춰 노출된 이마를 빠뜨리지 않도록 발라요."
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
끈적임을 피하려고 야외에서 노출된 이마를 의도적으로 빼고 발랐다고 하셨어요. 노출된 이마의 누락을 살피고 해당 제품이 이 부위에 사용 가능한지 표시를 확인해요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 범위를 살필 때는 노출 부위를 의도적으로 빼거나 아주 적게 바르는 행동을 비교해요 [kb:B-P02@0.6.1].

### 확인이 필요한 한계
이마 외의 실제 도포량은 기록되지 않았고 개인의 보호 수준을 계산할 수 없어요.

## syn-sol-0467

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `bb6895880c2af28ae5a116ef0e3fd806d64424302ea1d0509688412342e1dde3`
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
        "context": "야외",
        "exposed_site": "neck",
        "label_includes": "neck",
        "intentionally_omitted": "neck",
        "reason": "옷에 묻는 것이 싫음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "제품의 표시 사용 범위에 포함된 노출 목을 빠뜨리지 않도록 표시된 용법에 맞춰 발라요."
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
야외에서 목이 노출됐지만 옷에 묻는 것이 싫어 일부러 바르지 않으셨군요. 목이 표시된 사용 범위에 들어가므로 해당 용법에 맞는 광보호를 살펴봐요. [kb:B-P02@0.6.1]

### 근거 및 이유
표시된 노출 부위의 누락과 사용상 불편을 함께 고려해요.

### 확인이 필요한 한계
이 기록만으로 실제 보호 수준은 알 수 없어요.

## syn-sol-0472

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9238c630e990c73068c86354a381a39cc18ea8291f1897140a17cf8dbf09cb78`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 얼굴용 합성 자외선차단제를 얼굴에 사용하면서 노출된 오른쪽 볼은 사용감 때문에 일부러 빼고 발랐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "얼굴용 제품을 바를 때 노출된 오른쪽 볼을 의도적으로 제외한 행동을 살펴요."
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
얼굴용 제품을 얼굴에 바를 때 노출된 오른쪽 볼을 빠뜨리지 않도록 표시된 용법에 맞춰 발라요. [kb:B-P02@0.6.1]

### 근거 및 이유
얼굴의 노출 부위를 의도적으로 제외한 사용을 제품의 표시 범위와 함께 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동이나 개인의 실제 보호 수준은 추정하지 않아요.

## syn-sol-0473

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9565337288fffde9a11697d0f03e8e0e176771156a983e5f65754817917a54cb`
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
        "past_hot_car": true,
        "temperature": "unknown",
        "duration": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "current_direct_sunlight_avoided": true,
        "currently_closed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "과거의 뜨거운 차 보관과 현재의 보관을 구분하고 현재 품질은 따로 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
과거 뜨거운 차에 둔 기록과 현재 닫아서 직사광선을 피하는 보관을 구분해요. 현재 품질은 별도로 확인이 필요해요. [kb:B-S01@0.6.1]

### 근거 및 이유
화장품 보관 자료는 열과 빛, 공기와 취급이 품질에 관련될 수 있다고 설명해요. [ref:S06]

### 확인이 필요한 한계
차 안의 정확한 온도와 시간은 미상이며 이 이력만으로 안전성이나 남은 기한을 계산할 수 없어요.

## syn-sol-0475

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a9857013c43ec3f3d58a27cbc7e0f437a5d49b261bf02771b1c10e903ac7723d`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 햇빛은 피해서 보관했지만 뚜껑을 지속적으로 열어 두었어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "직사광선을 피한 보관은 유지하고 지속적으로 열어 둔 용기는 제품 보관 지침에 맞춰 닫아 보관해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
햇빛을 피해 보관한 점은 유지하고 계속 열어 둔 합성 화장품 용기는 제품 지침에 맞춰 닫아 보관하는 것을 검토해요 [kb:B-S01@0.6.1].

### 근거 및 이유
보관 상태를 살필 때는 지속적으로 열린 용기를 보관 상태의 비교 대상으로 삼아요 [kb:B-S01@0.6.1]. 화장품 보관 자료는 열·빛·공기와 취급이 품질에 관련될 수 있다고 설명해요 [ref:S06].

### 확인이 필요한 한계
이 보관 이력만으로 실제 변질, 안전성이나 남은 사용기한을 확정할 수 없어요.

## syn-sol-0479

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8cb6cc45896bca9c2c16a66d465924e07f23bf07a6e3346f2707a9426e7130ea`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "가": "뚜껑 계속 열림",
        "나": "뚜껑 닫힘"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "가의 내용물 상태": "미확인",
        "나의 내용물 상태": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "열려 있던 가의 용기는 보관 지침에 맞춰 닫아 두고 이미 닫혀 있던 나와 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
계속 열려 있던 가의 용기는 보관 지침에 맞춰 닫고, 이미 닫혀 있던 나와 구분해서 살펴봐요. [kb:B-S01@0.6.1]

### 근거 및 이유
화장품 보관 안내는 공기 노출과 용기 및 취급 방식을 함께 다뤄요. [ref:S06]

### 확인이 필요한 한계
두 제품 모두 내용물 상태가 확인되지 않아 현재 품질이나 사용 가능 여부를 확정하지 않아요.

## syn-sol-0481

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ac96c9a7c830ddb27aec5eef2b195c5e0743287d133b00331cf11098418e1009`
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
        "continuous_direct_sunlight_at_window": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.temperature_history": {
      "variable_id": "storage.temperature_history",
      "state": "known",
      "value": {
        "temperature_measured": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "current_product_stability_measured": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "제품 보관 지침을 확인하고 직사광선을 피해 보관해요. 현재 내용물의 안정성은 별도로 미확인 상태예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
창가의 직사광선 아래에 계속 두었다면 해당 제품의 보관 지침을 확인하고 직사광선을 피해 보관해요. [kb:B-S01@0.6.1]

### 근거 및 이유
빛과 온도는 화장품 보관에서 살펴볼 조건이에요. [ref:S06]

### 확인이 필요한 한계
온도와 내용물의 현재 안정성은 측정되지 않아 이 이력만으로 품질을 확정하지 않아요.

## syn-hold-0107

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `fc693e95eeeedb2581dc1db88b61495754665ef267abd73c208f448dd6a5c4da`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "cleanser": {
          "new": true,
          "used_on_face": true
        },
        "discomfort_after_use": true,
        "other_product_use": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 새 세정제 사용 후 불편이 지속되지만 다른 제품의 사용은 기억나지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0108

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `4f8a0d5a40a54fa7ac2ffe8d77f4b6260435f5a24ab878eed053f7a3a2ccf2d6`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
    "routine.change_log": {
      "variable_id": "routine.change_log",
      "state": "known",
      "value": {
        "product": "얼굴 세정제",
        "change": "변경",
        "timing": "지속 불편 중 변경",
        "discomfort_onset": "변경 전"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴의 불편은 세정제를 바꾸기 전부터 계속됐다고 하셨어요. 지속되는 상태이므로 개별 루틴 판단을 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
불편이 시작된 때와 세정제를 바꾼 시점을 의료진에게 알려 확인받아 주세요. 시간 순서만으로 원인은 알 수 없어요.

## syn-hold-0109

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `5f0583604ce3b7d3dadbf89b2de133cfb58e7897185c2947aa8c0ace3b6708ea`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "cleanser",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser_stopped_after_discomfort": true,
        "discomfort_continues_after_stop": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 해당 세정제를 중단한 뒤에도 불편이 지속돼요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0110

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `d6ef86a2c842ec93f8c167fd6b2df7783dc06c1b1abfb479af3dfa00f7862ac3`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "face_cleansing": {
          "question": "횟수만 줄이면 되는지",
          "cleanser_used": "unknown"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 불편이 지속되는 상황에서 세안 횟수만 줄여 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0111

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9c6cbfde9d089918ea8f500f6e30ce3cefe6382a8c507af9ec100f2ec165d83e`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "event": "얼굴 세안 뒤 지속 불편",
        "cause": "세안 때문인지 미상",
        "new_product_use": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 세안 뒤 불편이 계속되고 있어 개인별 루틴 결정은 미뤄요. 세안이 원인인지는 아직 몰라요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편과 경과를 의료진에게 확인받아 주세요. 새 제품을 사용했는지도 확인되지 않았어요.

## syn-hold-0112

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f04419db8c59419fc98975c6fcdd94b6150427307f11f58b5ca36ea3358273fa`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "asked_whether_to_change_cleansing_tool": true,
        "tool_as_cause": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 도구를 바꾸는 것만으로 지속 불편이 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0113

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `95549ebca72653833e63cd3297d6822d0b47fe2cd93eafe49d958036c1f5f4dc`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "family": {
          "experience": "세안 뒤 편안함"
        },
        "self": {
          "question": "가족과 같은 방법을 따라도 되는지"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 가족의 편안한 경험과 본인의 지속 불편을 구분해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0114

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `faa5276e49978ff4e2c22e2c555924220bf37a8abafe4edb4d366c7030b1e1eb`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_use": "사용 제품 있음"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 계속되고 있어 개별 루틴 판단을 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편과 경과에 대해 의료진에게 확인받아 주세요. 제품 버전에 대한 답변을 원하지 않으신 점을 존중하며 버전을 추정하지 않아요.

## syn-hold-0115

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `35421ff2b59afb8e4ef72a30b535c7c6d3072587d14ac537f3c9822b8d2313b0`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "lotion",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "lotion_used_before_persistent_discomfort": true,
        "product_version": "unknown",
        "product_intended_site": "face"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 로션 사용 뒤 지속되었지만 정확한 제품 버전은 모르고 있어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0116

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `210edde7fe11d67954074ebf53743515b6035affdbe84e148af0e6187e470cc5`
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
        "face_device": {
          "used": true,
          "discomfort_preceded_use": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_used": true,
        "discomfort_existed_before_device_use": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "current_discomfort": {
          "site": "face"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 불편은 기기를 사용하기 전부터 지속됐어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0117

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `64db2d92d0defb4573cb8b965b04acae234de9f71d8688f3d4f69da15b21958a`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
        "product": "얼굴용 제품",
        "used": true,
        "discomfort": "사용 후 불편",
        "stopped": true,
        "after_stopping": "얼굴 불편 지속",
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴용 제품을 쓰고 불편해 중단했지만 불편은 계속되고 있군요. 개별 루틴 판단은 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
제품 사용과 중단, 불편의 경과를 의료진에게 알려 확인받아 주세요. 원인은 아직 확인되지 않았어요.

## syn-hold-0118

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `592cb4645a0ece297b3e0409072889f298e21de01965e74afa4f4fd152a1a0a7`
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
        "face_products_used_same_day": 2,
        "cause_product": "unknown",
        "products_intended_site": "face"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 두 제품을 사용했지만 어느 제품이 원인인지는 알 수 없어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0119

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `ffd86832732caa0e1719d2aff844162e771c86ca0c151583b69a4007774486c3`
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
        "face_product": {
          "used_during_discomfort": true,
          "question": "양을 절반으로 줄여 계속 써도 되는지"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
불편이 지속되어 개별 루틴 판단을 보류해요. 사용량을 절반으로 줄이는 것만으로 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0120

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `18fc0e664a37a1f637be38d4f7ba120c0b3d9bb488e96e503734e6f207e82e40`
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
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
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
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": {
        "question": "얼굴용 제품 순서를 바꾸면 되는지",
        "cause": "순서가 원인인지 unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되는 동안 제품 순서를 바꾸면 되는지 물으셨군요. 지금은 순서를 설계하거나 원인으로 단정하지 않고 판단을 미뤄요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속된 불편과 제품 사용 경과를 의료진에게 확인받아 주세요.

## syn-hold-0121

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `167c19d3cefc004d60cce9be785ffcd8c58e5d5874a8b74f18bd514872fd380d`
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
        "used_before_persistent_discomfort": true,
        "device_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "co_used_product": "not_remembered"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 기기 사용 뒤 불편이 지속되지만 함께 쓴 제품은 기억나지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0122

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `71de05271427743cf68ea7ce614023ba7d075d2793b2e9df09534631556a2e07`
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
        "face_product": {
          "ingredient_list_response": "declined",
          "used": true
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.distribution": {
      "variable_id": "skin.distribution",
      "state": "known",
      "value": {
        "current_discomfort": {
          "site": "face"
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
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
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
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 성분표에 대한 답변을 거절하신 점을 그대로 존중해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0123

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `40cb2ee4f215df030da5ecf39da2db4a1523f1d8a5dda38ae04c205cb0fc40cf`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 핸드크림을 바른 뒤 불편이 지속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손에 핸드크림을 바른 뒤 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0124

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `b12116a15011dd32e76a4d257d53c58a7d8d28fe104ab844c5b4221e97746396`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손을 씻는 일을 계속해야 하는데 손 불편이 지속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손을 씻는 일을 계속해야 하는데 손 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0125

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `be194f5dc7bba917b57f7665b3aed3250449ad325f8c1c1ec5d9fd5ab2640d58`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습 제품을 바꾼 뒤 불편이 계속돼요. 원인은 확인되지 않았어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손 보습 제품을 바꾼 뒤 불편이 계속돼요. 원인은 확인되지 않았어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0126

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9fcd830cd258e1de1cb31a56648ffeb6f8357333f93d3e7c344b6d196baa4ee8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "물에 손이 자주 닿는 작업을 한 뒤 손 불편이 지속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
물에 손이 자주 닿는 작업을 한 뒤 손 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0127

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `20b9b4452127551ff4cc04d8973ef42cb1da7795922ac4465708b9fc4de874c5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 불편이 지속되는 가운데 핸드크림을 몇 번 더 바를지 묻고 있어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손 불편이 지속되는 가운데 핸드크림을 몇 번 더 바를지 묻고 있어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0128

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `60d9a38927e9b75d25ef88fb3f6362f90c2734cef69ed4261ac0b1a23831afd3`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "양손에 불편이 계속돼요. 손에 바른 제품의 영향인지는 몰라요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
양손에 불편이 계속돼요. 손에 바른 제품의 영향인지는 몰라요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0129

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `301520718295c395377becac4e301bcc2ff14814e5a2a2c3bd58f09865108fdc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 쓰는 제품을 바를 때 불편하고 그 불편이 지속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손에 쓰는 제품을 바를 때 불편하고 그 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0130

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `3300e8db4f37b6acfce34e908ce67734579ecf8f890e6b2e6b2f1151eef9c095`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 건조하다고 느끼며 불편이 지속돼요. 별도 진단은 확인되지 않았어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
손이 건조하다고 느끼며 불편이 지속돼요. 별도 진단은 확인되지 않았어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0131

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `c595732b6d72b40e7c5492e15e18e80ebceb694769e7e4c1545d0eddd1062312`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 부위의 불편이 지속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
얼굴 면도 부위의 불편이 지속돼요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0132

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `c929610d78d59dbb44c9cd2367d7d1b962262a8b7544a38a7290a479ab968311`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 불편이 계속돼요. 원인은 확인되지 않았어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
목 면도 후 불편이 계속돼요. 원인은 확인되지 않았어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0133

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `08406bc88227a81d82fd45e28ebbfd30862583a9843777e6903faff803554b8f`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 제품을 바른 뒤 불편이 계속돼요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
얼굴 면도 후 제품을 바른 뒤 불편이 계속돼요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0134

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `61518998a4a8204d062e6d63aa063067ec25840bf7f451b589363d7bb96f57a8`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "수동 날면도하는 얼굴 부위에 불편이 지속돼서 압력을 어떻게 바꿀지 묻고 있어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
수동 날면도하는 얼굴 부위에 불편이 지속돼서 압력을 어떻게 바꿀지 묻고 있어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0135

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `c803fab6a85c2704c2eeeeedbcb72f53e5dcdf6ebedf5e30d3ba7490ae5e3518`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 부위에 불편이 지속되어 보습 횟수를 묻고 있어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
목 면도 부위에 불편이 지속되어 보습 횟수를 묻고 있어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0136

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `170337443c2877e844c7c7c9670d6600982661b2c7fcf895604a9afeea58cb68`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 쓰는 두 관리 제품의 사용 기간 중 불편이 지속돼요. 어느 제품 때문인지는 몰라요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
얼굴에 쓰는 두 관리 제품의 사용 기간 중 불편이 지속돼요. 어느 제품 때문인지는 몰라요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0137

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `09362317557e0caf5390d9ddc3f30e60b158458605cbdd531adafcad5b26ae67`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 불편이 계속돼요. 면도와 제품 중 원인은 확인되지 않았어요.",
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
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
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
얼굴 면도 후 불편이 계속돼요. 면도와 제품 중 원인은 확인되지 않았어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0138

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `60976ebdb93418a47b3c3f45eadfe5711ffaa0a42d58312a2e60c5c021eda380`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 표시기한은 남았지만 원래 흰 내용물이 이번에 노랗게 변했어요. 계속 사용해도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
표시기한이 남아 있어도 이 합성 자외선차단제에서 새로 나타난 변색은 별도 확인이 필요해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 용기의 사용을 멈추고 표시와 보관 이력을 확인해 주세요. 변색의 원인이나 차단 성능은 이 기록으로 확정할 수 없어요.

## syn-hold-0139

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `a81eb1a64e873ac1b326597375c77a64c8abb7710bb1fb60495638be3d452be1`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "흔들어 쓰도록 표시된 합성 자외선차단제는 원래 두 층이에요. 최근 이전에 없던 악취가 새로 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
원래 표시된 두 층과 최근 새로 생긴 악취는 서로 다른 관찰이에요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이 용기의 사용을 멈추고 냄새 변화에 관해 제조·판매처에 확인해 주세요. 정상적인 두 층이라는 사실만으로 새 냄새의 원인이나 제품 안전성을 확정하지 않아요.

## syn-hold-0140

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `13ac2eba6cbf002866514948e7367aef255e187d3d83506841086819da187518`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 번호는 확인한 회수 목록에 없어요. 그러나 이 용기에서 전에 없던 냄새가 새로 나요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
확인한 회수 목록에 번호가 없다는 사실과 새 냄새는 별개예요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
냄새가 달라진 해당 용기의 사용을 멈추고 제조·판매처에 확인해 주세요. 목록 확인만으로 현재 품질이 확인되는 것은 아니에요.

## syn-hold-0141

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `78fd5cf53180878ba491e95e36cbf0a1229e3fdb2331287b0fc3ca453ed00194`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 사용기한은 남았어요. 최근 뚜껑 주변에 없던 균열과 누출이 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
기한이 남아 있어도 용기의 새 균열과 누출은 확인이 필요해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
누출된 해당 용기의 사용을 멈추고 제조·판매처에 상태를 확인해 주세요. 누출만으로 내용물 오염을 확정할 수는 없어요.

## syn-hold-0142

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `f85c5ac91d161959a45be2c19b5d4737296fa34fbee8213407692e1779519fa4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제 두 용기 중 가에서 이전에 없던 분리가 새로 생겼어요. 나의 상태는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
가 용기의 새 분리는 별도로 확인해야 해요. 나 용기의 상태는 아직 몰라요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
가 용기의 사용을 멈추고 제품 표시와 제조·판매처에 확인해 주세요. 나도 변질됐거나 안전하다고 단정하지 않아요.

## syn-hold-0143

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `6353a8356148ff95519d64e83aae038e8370b7c58c86d78ba0d090b547d5c383`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제에 전에 없던 알갱이가 생겼어요. 양을 줄여서 계속 써도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
이전에 없던 알갱이가 생긴 제품은 사용량 조절로 해결됐다고 볼 수 없어요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품 사용을 멈추고 표시와 제조·판매처에 품질을 확인해 주세요. 입자의 정체는 확인되지 않았어요.

## syn-hold-0144

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `baba512aebb6049ccbe5e1a07d6048388015b538e13c25aebf671f0a98105109`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제 용기의 제조번호를 확인했지만 원래 없던 이물이 새로 보였어요. 이물의 정체는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
제조번호를 확인한 사실과 새로 발견된 이물은 별개로 살펴야 해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이물이 보인 해당 제품 사용을 멈추고 제조·판매처에 확인해 주세요. 이물의 정체와 원인을 추정하지 않아요.

## syn-hold-0145

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9a405cb32d24d90a242e7b5247158a0150eb7ebcf2e94959e5d0a071b4316930`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제에서 이전에 없던 냄새가 새로 나요. 보관 장소만 옮기고 계속 써도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
새 냄새가 생긴 제품은 보관 장소만 옮겨 품질이 회복됐다고 볼 수 없어요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품 사용을 멈추고 표시와 제조·판매처에 냄새 변화를 확인해 주세요. 원인이나 오염 여부는 미상이에요.

## syn-hold-0146

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `c18ff88d202b7610a468df69940dbc4eee8f094369f3c0989f7cdd297af992f0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "흔들어 쓰는 정상 두 층이 표시된 합성 화장품에서 최근 원래 없던 악취가 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
정상적으로 표시된 두 층과 새로 생긴 악취는 구분해서 확인해야 해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
악취가 생긴 용기의 사용을 멈추고 제조·판매처에 확인해 주세요. 원래 두 층이라는 표시가 새 냄새의 안전성을 증명하지는 않아요.

## syn-hold-0147

- 모드·분할: `hold` / `val_internal`
- 현재 내용 해시: `abdb36d5cc87871bf89d54f88d22518c47feccd67eef4bed7bd20ac51d0fe82e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 기한은 남았지만 내용물이 최근 원래 색과 다르게 변했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
인쇄 기한이 남았어도 새로 변한 내용물의 색은 별도 확인이 필요해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 용기의 사용을 멈추고 제품 표시와 제조·판매처에 확인해 주세요. 변색의 원인이나 안전성은 이 기록만으로 알 수 없어요.

## syn-hold-0148

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `436e50b93dc34df731acd2049be4fdec43ab7e701f96f17d84dd7d37bc7b2578`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 용기에 최근 새 균열과 누출이 생겼어요. 내용물의 오염 여부는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
최근 생긴 용기 균열과 누출을 확인하기 전 개별 사용 안내를 보류해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
누출된 용기의 사용을 멈추고 제조·판매처에 상태를 확인해 주세요. 오염 여부는 아직 확인되지 않았어요.

## syn-hold-0149

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `9dc0ddbe2d1587eec52af25f2af95f8539c1dba0b05788e46d8c66edbdaf1017`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품 두 용기 중 가에서 최근 원래 없던 분리가 생겼어요. 나의 상태는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
가 용기에서 새 분리가 관찰됐지만 나 용기의 상태는 확인되지 않았어요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
가의 사용을 멈추고 그 용기의 표시와 제조·판매처에 확인해 주세요. 나도 이상이 있거나 안전하다고 추정하지 않아요.

## syn-hold-0150

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `a1d52254c51bc1c7372070fd1ae0e9cb8156a592cda43a6af297da6ddcd26e96`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품에 최근 원래 없던 입자가 생겼어요. 걸러서 계속 쓰는 방법을 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
새로 생긴 입자를 걸러내는 것으로 제품 상태가 확인되지는 않아요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 사용을 멈추고 제조·판매처에 새 입자를 확인해 주세요. 입자의 정체와 원인은 미상이에요.

## syn-hold-0151

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `87a29e6ed522a9f1072a2d3a7bf4852ca2a40fbbf8b5245a476114aebf3a31d5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "확인한 합성 회수 목록에 해당 번호는 없지만 해당 화장품에서 최근 원래 없던 이물이 보였어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
회수 목록에 해당 번호가 없는 것과 새 이물의 관찰은 별개예요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이물이 나타난 제품의 사용을 멈추고 제조·판매처에 확인해 주세요. 목록 확인만으로 현재 품질이나 이물의 정체를 확정하지 않아요.

## syn-hold-0152

- 모드·분할: `hold` / `train`
- 현재 내용 해시: `3945b9a3895c932663287d885668495d1789d5cadf1a865ee5a8954b706c1090`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품에서 전에 없던 악취가 최근 생겼어요. 서늘한 곳으로 옮겨 계속 쓰고 싶어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
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
새로 생긴 악취는 서늘한 곳으로 옮기는 것만으로 해결됐다고 볼 수 없어요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 사용을 멈추고 냄새 변화에 관해 제조·판매처에 확인해 주세요. 원인이나 오염 여부는 아직 몰라요.

## syn-sol-0345

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `60942a48d0c8ca5533162c762acc78b8a5dd5bdf1a7cdc71781cf134b3af0ee5`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.makeup": {
      "variable_id": "cleansing.makeup",
      "state": "known",
      "value": {
        "분장": "이미 지워짐"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "additional_washes": 2,
        "consecutive": true,
        "reason": "잔여감 걱정",
        "additional_soiling": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.sequence": {
      "variable_id": "method.sequence",
      "state": "known",
      "value": {
        "events": [
          {
            "action": "얼굴 분장 제거를 위해 세정",
            "result": "분장 이미 지워짐"
          },
          {
            "action": "같은 얼굴 세안 두 번 더 연속",
            "reason": "잔여감 걱정",
            "additional_soiling": false
          }
        ]
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "추가 세안은 확인되지만 한 번의 기록만으로 습관적인 반복이라고 단정하지 않아요."
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
분장을 지운 뒤 추가 오염이 없는데 잔여감이 걱정돼 두 번 더 연속 세안하셨군요. 이 한 번의 기록만으로 습관적 반복으로 판단하지 않고 제거 필요와 걱정을 함께 살펴봐요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
다른 날에도 반복하는지와 실제 잔여물은 확인되지 않았어요.

## syn-sol-0347

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3bf1b6f3801d4ed3d6599851595cffc192cd14b8656d6e08ec604fb40db23073`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "consecutive": true,
        "reason": "declined",
        "consecutive_face_wash_count": 2
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "연속 세안의 이유를 알 수 없어 목적 없는 반복으로 단정하지 않아요."
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
얼굴을 연속 두 번 씻었다는 사실만으로 목적 없는 반복이었다고 단정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
이유에 대한 답변을 거절하셨으므로 이유를 추정하지 않아요.

## syn-sol-0355

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f8740ed25c7b80cb98c6890a209966a923da144caec9d0acea8888b0b6daf20b`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face_washing": {
          "frequency": "daily",
          "water_feel_recalled": false,
          "temperature_measured": false
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "물의 느낌과 온도가 확인되지 않아 얼굴 물 온도를 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
매일 얼굴을 씻지만 물이 뜨거웠는지 미온이었는지 기억하지 못해요. 뜨거운 물 사용으로 판정하지 않아요 [kb:B-C01@0.6.1].

### 근거 및 이유
물 온도 기준은 뜨겁게 느껴지는 물을 사용했다고 보고된 경우를 살펴요 [kb:B-C01@0.6.1]. 제공된 일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
물의 체감은 미상이고 온도 측정도 하지 않았어요. 숫자를 추정하지 않아요.

## syn-sol-0356

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ff8226c6c03d13c25d741b08770abf84d8767eb0478c2ebc99df913f188c6288`
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
      "value": {
        "perceived_cold": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "context": "일상 세안",
        "clinician_instruction": "별도 지시 보고하지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "차가운 물을 썼다는 사실만으로 위험하거나 뜨거운 물을 쓴 것으로 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
일상 얼굴 세안에 차갑게 느껴지는 물을 사용하신다고 하셨어요. 이 사실만으로 뜨거운 물 사용이나 위험으로 판단하지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
정확한 온도는 알 수 없고 별도 의료진 지시는 보고되지 않았어요.

## syn-sol-0359

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9da0b5aba8a7cbc14179f40aeab72ee481b76e31eaead7769bfcd8463d64f6e9`
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
      "state": "known",
      "value": {
        "contact_time_instruction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "placed_briefly_before_rinse": true,
        "intentional_long_contact": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "사용 시간의 뜻과 제품 지시가 확인되지 않아 오래 둔 행동으로 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
얼굴 세정제를 잠시 두고 헹궜다는 기록만으로 일부러 오래 두었다고 판단하지 않아요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
제품의 접촉시간 지시와 의도적으로 오래 두었는지는 미상이에요.

## syn-sol-0364

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `2dbf3e4b78d022f79c78a6ce26a10f73eff44a5d6d73d7b39e1fea24b39e0f23`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "actual_rinsing": "unknown",
        "reason_unknown": "기억하지 못함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleanser": {
          "type": "일반 세정제",
          "used_on_face": true,
          "reported_label": {
            "rinse_with_water": true
          }
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "표시와 실제 헹굼 여부를 구분하고 사용 행동은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
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
얼굴 세정제의 표시에는 물로 씻어내라고 되어 있지만 실제로 헹궜는지는 기억나지 않아요. 헹굼을 생략했다고 판단하지 않아요 [kb:B-C06@0.6.1].

### 근거 및 이유
헹굼 기준은 씻어내는 제품을 헹구지 않은 행동이 확인되는지 살펴요 [kb:B-C06@0.6.1]. 제공된 일반 얼굴 세안 자료도 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
실제 사용 뒤 헹굼은 미상이며 제품 표시와 실제 행동을 혼동하지 않아요.

## syn-sol-0369

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9e9fd6e6fbbda8fdeb88b8275203e655cbf8170f4136e7d414d32f1f28af13d8`
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
        "used_product": {
          "type": "선크림",
          "removal": "지우기 어려움",
          "water_resistance": "unknown",
          "removal_instruction": "unknown"
        },
        "other_product": {
          "owned": true,
          "used": false,
          "water_resistance_label": true
        },
        "request": "세안 단계 검토"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "사용하지 않은 제품의 표시를 실제 사용 제품에 옮기지 않고 제거 지시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
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
실제 쓴 선크림을 지우기 어려워 단계를 살펴보고 계시군요. 사용한 제품의 제거 지시와 내수성 표시를 확인해 주세요. 쓰지 않은 다른 제품의 표시를 옮겨 판단하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
소규모 비교는 제한된 제품과 세정법에 관한 것으로 모든 제품에 같은 단계를 정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 내수성과 제거 지시는 미상이에요.

## syn-sol-0374

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `c009276c5785fa6fd04c04d686975c82b2586cf9d674699e462b69aee4780841`
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
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "morning_presses": 1,
        "evening_presses": 2,
        "mass_per_press_measured": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "same_pump_product_morning_and_evening": true,
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "누른 횟수는 구분하되 질량으로 환산하지 않아요."
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
같은 얼굴용 펌프 제품을 아침에 한 번, 저녁에 두 번 눌렀어요. 이 횟수를 배출된 질량으로 환산하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
한 번의 배출 질량은 측정하지 않았기 때문이에요.

### 확인이 필요한 한계
횟수만으로 사용 질량이나 성분 농도를 알 수 없어요.

## syn-sol-0379

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `768f3828e0fb8de2fa47c6765c9f10f79d2a81147bb8b8c88fbcc20eccde047a`
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
        "face_product": {
          "current_label": {
            "specific_fragrance_name_confirmed": true
          }
        },
        "personal_allergy_response": "declined"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "확인된 표시와 답변을 거절한 개인 알레르기 여부를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품의 현행 성분표에서 특정 향료명을 확인했지만 개인 알레르기에 관한 답변은 거절하셨어요. 표시를 개인의 알레르기 반응으로 바꾸지 않아요 [kb:B-G17@0.6.1].

### 근거 및 이유
표시된 성분과 개인 알레르기는 별개의 정보예요 [kb:B-G17@0.6.1]. 향료 표시 자료도 표시만으로 개인의 알레르기 반응이 확정되지 않는다고 설명해요 [ref:S15].

### 확인이 필요한 한계
답변 거절을 존중하며 알레르기가 있다거나 없다고 추정하지 않아요.

## syn-sol-0380

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5c6b1b23b2cec05828dcf7fd5814b5ed26b0afb9c307bb550f05de6e79078c21`
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
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "A": "특정 향료명 표시",
        "B": "성분표 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "선택 대상": "제품 B",
        "products_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "제품 A의 표시를 제품 B의 표시로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
제품 A에 표시된 향료명을 선택 중인 제품 B에도 있다고 옮겨 판단하지 않아요. B의 해당 버전 성분표를 확인해 주세요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료 표시와 개인 반응은 서로 다른 정보예요. [ref:S15]

### 확인이 필요한 한계
제품 B의 성분표가 미확인이라 해당 향료의 함유 여부는 알 수 없어요.

## syn-sol-0387

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `396a31f33358a1da9e455417172d85bdb14c6241f6908e4704e7f83a9f5557d0`
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
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_and_lotion_used_together": true,
        "device_and_lotion_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "device_lotion_co_use_instruction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기와 로션을 함께 쓴 사실은 확인됐지만 병용 적합성은 미확인이에요. 해당 조합의 사용을 추천하기는 보류하고 기기의 공개 사용 지침을 확인해요."
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

### 핵심 안내
얼굴용 기기와 로션을 함께 사용했지만 그 조합이 적합한지는 확인되지 않았어요. 병용을 추천하는 것은 보류하고 기기의 공개 사용 지침을 확인해요. [kb:B-G06@0.6.1]

### 근거 및 이유
실제로 함께 사용했다는 사실과 기기 지침에서 허용하는지는 별개예요.

### 확인이 필요한 한계
제품 반응이나 적합성을 추정하지 않아요.

## syn-sol-0393

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0ab34b78176a34169d1ca6e7ffcfe26b8966f9cecec56f887fbdb9d9ad9fd0b8`
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
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "face_product_fragrance": "avoid"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "medically_confirmed_allergy": "not_disclosed"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "향을 피하고 싶은 선호는 존중하되 알레르기 진단으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품에서 향을 피하고 싶은 선호를 존중해요. 그 선호를 의학적 알레르기 진단으로 바꾸지 않아요 [kb:B-G17@0.6.1].

### 근거 및 이유
향에 대한 선호와 개인 알레르기는 구분해야 해요 [kb:B-G17@0.6.1]. 향료 표시 자료에서도 표시만으로 개인의 알레르기 반응을 확정하지 않아요 [ref:S15].

### 확인이 필요한 한계
의학적으로 확인된 알레르기 여부는 밝히지 않았어요.

## syn-sol-0395

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e8bddb3198ba01ad009f269f2909de8137e83a6f1747b90b165635d0ad87e5f2`
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
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "현재 확인된 성분표": "향료 표시",
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "해당 성분 알레르기": "unknown",
        "해당 성분 반응": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "확인된 표시는 기록하되 개인의 반응이나 알레르기는 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품의 현재 성분표에는 향료가 표시되어 있어요. 다만 그 표시만으로 본인의 알레르기나 반응을 판단하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
표시 사실은 개인에게 알레르기 반응이 발생했다는 증거가 아니에요. [ref:S15]

### 확인이 필요한 한계
해당 성분에 대한 본인의 반응과 알레르기는 미상이에요.

## syn-sol-0397

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `85cc30982133a5d9f10fbab4c5c79bc93929d111fa2a7142046f3835b3c0a199`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 필요한 손 씻기를 해요. 동료는 손을 씻은 뒤 보습하지만 본인의 보습 여부는 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동료의 행동으로 본인의 보습 여부를 대신하지 않아요."
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
필요한 손 씻기는 본인이 하고, 씻은 뒤 보습은 동료가 한 행동이에요. 본인의 보습 여부는 미상이에요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 안내는 손 씻은 뒤 보습을 다루지만 필요한 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
동료의 행동을 본인의 기록으로 옮기지 않아요.

## syn-sol-0401

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `24fc514d48e4b29014917a2406b6a6f6258bd788ac5f51470cde3e1d952c30b9`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "필요한 손 위생을 유지해요. 손 보습 사용 여부에 관한 답변은 원하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "답변 거절을 보습하지 않는다는 뜻으로 바꾸지 않아요."
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
필요한 손 위생을 유지하고 계세요. 손 보습에 관한 답변을 원하지 않으셨으므로 보습을 하지 않는다고 기록하지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 관리 기준은 손을 계속 건조하게 두는 행동이나 특정 제품의 반복 불편을 살펴요 [kb:B-M04@0.6.1]. 일반 안내는 손 씻은 뒤 보습과 무향료 제품을 다뤄요 [ref:S21].

### 확인이 필요한 한계
보습 여부는 답변을 거절한 상태로 남기며 필요한 손 위생을 줄이라는 뜻이 아니에요.

## syn-sol-0403

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `498c138806b6d284e23e1f273d8b74984a69635491887ee334ae2547c096d3a0`
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
        "handwashing": "자주 씻고 필요한 손 위생 유지",
        "hand_moisturizing": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "손 씻는 사실만으로 손 보습 행동을 판단하지 않아요."
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
손을 자주 씻고 필요한 위생은 유지하고 계시군요. 손 보습 여부는 확인되지 않아 하지 않는다고 판단하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 안내는 손 씻기 뒤 보습을 다루며 필요한 손 위생을 대신하지 않아요. [ref:S21]

### 확인이 필요한 한계
현재 보습 행동과 사용 경험은 미상이에요.

## syn-sol-0404

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `43048b135d6ad522e54d8ef05bde1ed4abf6ba1bc7894b881626a58d2226b263`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가족은 손 씻은 뒤 보습제를 써요. 본인이 손에 보습제를 쓰는지는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "가족의 보습 행동을 본인에게 옮기지 않아요."
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
가족이 손 씻은 뒤 보습제를 쓴 사실은 본인의 손 보습 여부를 알려주지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 자료는 손 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
본인의 사용 여부는 미상이므로 사용했거나 하지 않았다고 정하지 않아요.

## syn-sol-0405

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `9c6f147b2a6860c153db8da6076cbadd96649826e6fefc0ffc64798718f0c5fb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "동료는 근무 뒤 손에 보습제를 바른다고 해요. 본인의 손 보습 시간은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동료의 시간으로 본인의 손 보습을 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
근무 뒤 손에 보습제를 바르는 사람은 동료예요. 그 시간을 본인의 보습 시간으로 옮기지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 관리 기준은 본인의 보습 행동과 특정 제품의 반복 불편을 살펴요 [kb:B-M04@0.6.1]. 일반 안내는 손 씻은 뒤 보습을 다뤄요 [ref:S21].

### 확인이 필요한 한계
본인의 손 보습 시간은 아직 확인되지 않았어요.

## syn-sol-0406

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `c6ae713515cbb0d515f704b6cc48cf2b952de9a375f5ab8645dde18a311211aa`
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
        "friend": "손을 씻고 크림 사용",
        "self_after_handwashing": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "친구의 사용을 본인의 사용으로 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
친구는 손을 씻은 뒤 크림을 쓰지만 본인의 보습 여부는 모르신다고 하셨어요. 친구의 행동을 본인에게 적용하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 안내는 손 씻기 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
본인의 사용 여부와 제품 반응은 확인되지 않았어요.

## syn-sol-0407

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `17ff1f42e613061327b714d22dc1a25483fed48135a67305a1ca2e6ee87aa4d3`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "동거인은 손 씻기 후에 보습해요. 본인은 손 씻기를 하지만 손 보습 여부는 답하고 싶지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동거인의 기록과 본인의 답변 거절을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
동거인의 손 씻기 후 보습과 본인의 손 씻기를 구분해요. 본인의 보습 여부는 답하고 싶지 않다고 하셨어요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 자료는 손 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
답변 거절을 보습을 하지 않았다는 뜻으로 바꾸지 않아요.

## syn-sol-0408

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1f65b6375e409944fb13e08fdacf30d469938820ba96243ceaaa837b092a8146`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "젖은 작업을 한 뒤 손에 핸드크림을 발라요. 사용했을 때의 개인 반응은 아직 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "사용과 개인 반응 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
젖은 작업 뒤 핸드크림을 사용한다고 하셨어요. 사용 사실만으로 그 제품이 편안하거나 불편하다고 판단하지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 관리 기준은 보습 유지와 특정 제품에서 반복되는 불편을 함께 살펴요 [kb:B-M04@0.6.1]. 일반 안내는 손 씻기 후 보습과 무향료 제품을 다뤄요 [ref:S21].

### 확인이 필요한 한계
이 제품을 썼을 때 개인 반응은 아직 보고되지 않았어요.

## syn-sol-0409

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `fbfbdc647129e4128f121a32f91f635d269ce5301c780224c1ed0606c81bba12`
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
        "candidate_label": "무향료",
        "aromatic_essential_oils": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "candidate": "손 보습제"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "무향료 표기만으로 향성 에센셜오일 여부를 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손 보습 후보에 무향료라고 적혀 있지만 향성 에센셜오일 포함 여부는 확인되지 않았어요. 필요하면 해당 성분표를 살펴봐요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 안내는 무향료 제품 선택을 다루지만 개인에게 편안하다고 보장하지 않아요. [ref:S21]

### 확인이 필요한 한계
현재 표시만으로 향성 에센셜오일의 포함이나 부재를 확정하지 않아요.

## syn-sol-0411

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8605617f4df6aed06f30174fbfc965db418efee08aabe7bf8bcb2b0489ce1340`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 물에 자주 닿는 작업을 해요. 작업 후 보습 여부와 제품 반응은 알 수 없어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "습식 작업만으로 보습 행동이나 제품 반응을 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손이 물에 자주 닿는 작업을 한다고 해서 작업 후 보습을 했는지나 제품에 어떤 반응이 있는지 알 수는 없어요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 자료는 손 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
작업 후 보습 여부와 제품 반응은 미상이에요.

## syn-sol-0413

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e420999346501cf5a51614a25a36e11e9a66b665e6a5132a10aa18b4c7f12869`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 보습제를 쓰고 있어요. 보습에 관한 개별 진료 지시가 있는지는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "개별 진료 지시의 유무를 추측하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손에 보습제를 쓰고 있지만 보습에 관한 개별 진료 지시가 있는지는 미상이에요. 지시가 없다고 가정하지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습의 일반 기준은 개인별 지시와 반복 불편을 함께 고려해요 [kb:B-M04@0.6.1]. 손 관리 자료는 씻은 뒤 보습을 설명해요 [ref:S21].

### 확인이 필요한 한계
개별 지시의 유무와 내용은 확인되지 않았고 일반 안내가 이를 대체하지 않아요.

## syn-sol-0414

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `99414dd677d62b8f6943d3cbfb8e7ab743a76add76dac3e047307724101b8753`
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
        "face_moisturizer": "편안함",
        "hand_product_use": "unknown",
        "hand_product_reaction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "얼굴 제품 경험을 손 제품 경험으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
얼굴 보습제는 편안하지만 손 보습 제품의 사용 여부와 반응은 모르신다고 하셨어요. 확인된 경험을 손에서의 사용 경험으로 옮기지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 보습에 관한 일반 안내가 개인의 제품 내성을 보장하지는 않아요. [ref:S21]

### 확인이 필요한 한계
두 언급이 같은 제품인지, 손 제품의 사용 여부와 반응, 얼굴 보습제를 실제 어느 부위에 썼는지는 확인되지 않았어요.

## syn-sol-0415

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `722a3b902d088dfb4bf3432f3a161312b2393c50f80e0547bd7271f87ac953c6`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 바를 후보는 핸드크림이에요. 전성분이나 향료 표시는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "제품 이름만으로 향료나 향성 오일을 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손에 바를 후보가 핸드크림이라는 이름만으로 향료나 향성 오일의 유무를 판단할 수 없어요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 자료는 무향료 제품 선택을 다뤄요. [ref:S21]

### 확인이 필요한 한계
후보의 전성분과 향료 표시는 아직 확인되지 않았어요.

## syn-sol-0419

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `39a8a4e1008c7ec66ed090459e5fc90e569cd9f1c7c4684c2f99fa110aff2e34`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습 후보의 표시에서 미네랄오일을 봤어요. 향료와 향성 에센셜오일은 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "미네랄오일이라는 표시를 향성 에센셜오일로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
손 보습 후보에서 미네랄오일 표시를 확인했지만 향료와 향성 에센셜오일은 확인하지 못했어요. 미네랄오일 표시를 향성 에센셜오일로 바꾸지 않아요 [kb:B-M04@0.6.1].

### 근거 및 이유
손 보습 기준은 제품별 반응과 향료·향성 에센셜오일 정보를 구분해 살펴요 [kb:B-M04@0.6.1]. 일반 안내는 무향료 크림·연고를 다뤄요 [ref:S21].

### 확인이 필요한 한계
해당 후보의 향료 및 향성 에센셜오일 여부와 개인 반응은 미상이에요.

## syn-sol-0420

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `17829a8be431f8d8b16337269892e9ace21ce43d82317f78fc325be4ab543da9`
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
        "old_package": "무향료 표시",
        "current_package": "표시 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "current": "미확인",
        "old_to_current_match": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product": "손 보습제"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "이전 표시를 현재 포장에 그대로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
예전 포장에는 무향료라고 적혀 있었지만 현재 포장의 버전과 표시는 확인되지 않았어요. 현재 제품을 확인해 주세요. [kb:B-M04@0.6.1]

### 근거 및 이유
손 관리 안내는 무향료 선택을 다루지만 예전 표시가 지금 제품에 그대로 적용되는지는 별개예요. [ref:S21]

### 확인이 필요한 한계
현재 버전과 표시는 미상이에요.

## syn-sol-0421

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `8119a6b7c30584d8d01f057f3621c3076333788d75ff4a6df32553a1df18a28e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가족은 이 핸드크림을 쓰면 불편하다고 해요. 본인의 손 사용 여부와 반응은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "가족의 반응을 본인의 반응으로 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
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
가족이 이 핸드크림에 불편을 느낀 경험과 본인의 반응을 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
일반 손 관리 자료는 손 씻은 뒤 보습을 다뤄요. [ref:S21]

### 확인이 필요한 한계
본인이 이 제품을 손에 썼는지와 반응은 미상이에요.

## syn-sol-0425

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `06f59ee62f267a9af59d0ecea46c96b17c4cafbdfe6dddb965e9ec49ab3f4f14`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 볼을 수동 날면도해요. 이때 본인의 방향과 압력은 기억나지 않아요. 직장 동료는 다른 날 목을 수동 날면도할 때 강하게 누른다고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "동료의 목 면도 압력을 본인의 볼 면도 압력으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 볼을 수동 면도하지만 방향과 압력은 기억나지 않아요. 다른 날 동료가 목을 강하게 누른 경험을 본인의 행동으로 옮기지 않아요 [kb:B-G10@0.6.1].

### 근거 및 이유
면도 기준은 강한 압력이나 반복 통과를 고수하며 불편을 무시하는 상황을 살펴요 [kb:B-G10@0.6.1]. 일반 수동 면도 안내는 털 방향과 부드러운 동작을 다뤄요 [ref:S23].

### 확인이 필요한 한계
본인의 실제 방향과 압력은 미상이에요.

## syn-sol-0426

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `34a8dec36bcadd5d44c4a0e79b6fd1c89f5011962ecc1361ceb84fb13dff0fb9`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "type": "수동 날면도",
        "direction": "unknown",
        "pressure": "unknown",
        "repeat_passes": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "사용 부위와 도구는 알려져 있으나 세부 동작은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목에 수동 날면도를 하고 계시지만 방향과 압력, 반복 통과는 확인되지 않았어요. 현재 동작이 적절하거나 잘못됐다고 판단하지 않아요. [kb:B-G10@0.6.1]

### 근거 및 이유
수동 면도 안내는 털 방향과 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
실제 면도 동작의 세부 사항은 미상이에요.

## syn-sol-0429

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5148eaf097e457b31fcd028ee3f63011b9ca1c3ead99b1a5e7168149afc909dc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴을 수동 날면도로 깎아요. 면도 압력과 방향에 대해서는 답하고 싶지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "답변 거절을 강한 면도로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 수동 날면도하는 것은 확인됐지만 압력과 방향은 답변을 원하지 않으셨어요. 강하게 면도한다고 추정하지 않아요. [kb:B-G10@0.6.1]

### 근거 및 이유
일반 수동 면도 안내는 털이 자라는 방향과 부드러운 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
거절된 동작 정보를 임의로 채우지 않아요.

## syn-sol-0434

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d8c97524c61b1ebcab5a115551bed3098c59b6461e8ec620fa5508d6f77ed93a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 보습제를 발라요. 바른 뒤의 반응은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "보습 사용 사실과 사용 반응의 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
얼굴 면도 후 보습제를 사용한 것은 확인됐지만 바른 뒤 반응은 미상이에요. 편안했다거나 따가웠다고 채우지 않아요 [kb:B-M05@0.6.1].

### 근거 및 이유
면도 후 관리 기준은 반복 따가움을 효과로 여기며 견디거나 모든 보습을 중단하는 경우를 살펴요 [kb:B-M05@0.6.1]. 일반 안내는 면도 후 보습을 다뤄요 [ref:S25].

### 확인이 필요한 한계
해당 제품을 사용한 뒤의 개인 반응이 확인되지 않았어요.

## syn-sol-0435

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `988cf7c2f3f52cca3240a41ecf98d3f25bc44f1bcdd95477f7297e3e306ea422`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "neck",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "action": "면도"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.aftercare": {
      "variable_id": "shaving.aftercare",
      "state": "declined",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "답변 거절을 보습 중단으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
목을 면도하신다고 하셨고 면도 후 보습에 관한 답변은 원하지 않으셨어요. 그 선택을 존중하며 보습을 중단한 것으로 판단하지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반적인 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
본인의 면도 후 보습 여부는 확인되지 않았어요.

## syn-sol-0436

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c8e335386d2d1b71ada88ce2f4f4862388d100f44a4e389b9cc08ce026c1a02d`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 목을 면도해요. 목 면도 후의 보습 사용 여부와 반응은 확인되지 않았어요. 동거인은 별도로 얼굴 면도 후 사용한 후처리 제품이 따갑다고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "동거인의 얼굴 제품 반응을 본인의 목 면도 후 반응으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
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
본인은 목을 면도하고 동거인은 얼굴 면도 후 제품에 따가움을 보고했어요. 이 경험을 본인의 목 반응으로 옮기지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
본인의 목 면도 후 보습 여부와 반응은 미상이에요.

## syn-sol-0442

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9808b3f6f9b1af44180ea952b6cb77d6fd7fac896d791d18373876ad7dc8d9fb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 각각 바르는 부위는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "같은 부위에 접촉하는지 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
레티놀 관리 제품과 별도 AHA 각질관리 제품을 같은 기간에 쓰지만 각각의 사용 부위는 미상이에요. 같은 부위 중첩이라고 확정하지 않아요 [kb:B-G13@0.6.1].

### 근거 및 이유
이 기준은 같은 부위의 별도 레티노이드와 AHA 각질관리 제품의 중첩을 다뤄요 [kb:B-G13@0.6.1]. 일반 각질관리 자료는 레티놀 사용 중 각질제거 추가에 주의를 권해요 [ref:S32].

### 확인이 필요한 한계
각 제품의 실제 접촉 부위를 확인해야 하며 개인 위해 확률은 알 수 없어요.

## syn-sol-0443

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `13a8d98a16b25768efc978764373e9b5344c8bcffb251de94a8417b0c8e537fb`
- 사람 검수: **미검수**

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
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "retinol_product": "관리 목적 사용",
        "other_cosmetic": "같은 기간 사용, AHA 포함",
        "other_purpose": "각질관리 목적 미상"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "성분 포함과 각질관리 목적을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
얼굴에 레티놀 관리 제품과 AHA가 든 별도 화장품을 같은 기간 사용하지만, 두 번째 제품의 각질관리 목적은 확인되지 않았어요. 해당 제품의 용도를 살펴봐요. [kb:B-G13@0.6.1]

### 근거 및 이유
일반 안내는 레티놀 사용 중 각질제거를 추가할 때 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
성분 포함만으로 그 제품의 관리 목적이나 개인별 위해를 확정하지 않아요.

## syn-sol-0444

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c47f0d553bb22d0c5812aada624199a1b9e266fc3df7d0717f0357cc52f163f3`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 레티놀 관리 제품과 별도 각질관리 제품을 같은 기간에 사용해요. 각질관리 제품의 성분은 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "각질관리 제품의 AHA 해당 여부가 미확인이므로 레티노이드와 AHA 특정 조합의 개별 판정은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
얼굴에 별도 레티놀 관리 제품과 각질관리 제품을 사용하는 목적은 확인됐지만, 각질관리 제품이 AHA에 해당하는지는 미확인이에요. 따라서 이 레티노이드와 AHA 특정 조합의 개별 판정은 미상이에요. [kb:B-G13@0.6.1]

### 근거 및 이유
관리 목적과 성분 확인은 서로 달라요. 일반 각질관리 자료는 레티놀 사용 중 추가 각질관리에 주의를 안내하지만, 이 제품의 AHA 함유 여부를 확인해 주지는 않아요. [ref:S32]

### 확인이 필요한 한계
제품 성분과 필요한 자료를 확인하기 전에는 AHA를 포함한다고 단정하지 않아요. 이 정보만으로 개인별 안전성이나 위해 확률을 확정하거나 처방을 자동 변경하지 않아요.

## syn-sol-0447

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `99739a7425ea776416118f10329188dc62de22ec61855fe00cd997ec16ae454a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 처방 레티노이드와 별도 AHA 각질관리 화장품을 같은 기간 사용해요. 의료진의 병용 지시 여부는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "처방 여부와 미확인 병용 지시를 구분하고 처방을 임의 변경하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
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
얼굴에 처방 레티노이드와 별도 AHA 화장품을 같은 기간 쓰고 있어요. 처방은 임의로 바꾸지 말고 병용 지시를 처방 의료진에게 확인해요. [kb:B-G13@0.6.1]

### 근거 및 이유
일반 각질관리 자료는 레티노이드 사용 중 추가 각질제거에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
의료진의 병용 지시는 미상이며 절대 금기나 개인 위해 확률을 확정하지 않아요.

## syn-sol-0448

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e2742a71549b85467a1c0cf83f16815671288502af6290096ad52cce43bc1a80`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 SPF 30과 내수성 표시는 읽히지만 접힌 사진 때문에 광범위 표시는 보이지 않아요. 내일 야외 걷기에 쓸 새 후보를 고르고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "광범위 보호 표시가 가려져 있어 이 항목은 미상이에요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
내일 야외 걷기용 새 후보의 SPF 30과 내수성 표시는 보이지만 광범위 보호 표시는 접힌 사진에 가려졌어요. 표시가 없다고 단정하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
야외 후보를 고를 때 일반 안내는 SPF 30 이상과 광범위 보호·내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
가려진 부분을 확인하기 전 광범위 보호 표시와 개인의 실제 보호 결과는 미상이에요.

## syn-sol-0450

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4b5b49d28051b326e8d08cca41a793e26e3d49be4851ebf1ab13c4c813053412`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.spf": {
      "variable_id": "product.spf",
      "state": "known",
      "value": {
        "container": 30,
        "sales_page": 50,
        "same_version": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "container": "광범위 보호 표시"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "container": "표시 읽지 못함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "product_purpose": "야외 등산용",
        "actual_hiking": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "판매 페이지와 용기의 버전 연결 및 용기의 내수성은 미상이에요."
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
등산용 용기에는 SPF 30과 광범위 보호가 표시됐지만 내수성은 읽지 못했어요. 판매 페이지의 SPF 50이 같은 버전인지도 확인한 뒤 비교해요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택 안내는 SPF, 광범위 보호, 내수성을 각각 확인하도록 다뤄요. [ref:S16]

### 확인이 필요한 한계
페이지와 용기의 버전 연결 및 내수성은 미상이에요.

## syn-sol-0451

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5cd5df5b43d74e6d5f36ebf58c0cac6b4bb6fb09fc6d78b3d99f5cc4cb40ff02`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 물놀이용 합성 자외선차단제 가는 SPF 30과 광범위 표시가 보이지만 내수성 표시는 가려져 있어요. 나의 내수성 표시는 보이지만 SPF와 광범위 표시는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "가의 내수성과 나의 SPF·광범위 표시는 각각 미상이에요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외 물놀이 후보 가는 SPF 30과 광범위 표시가 보이지만 내수성 표시는 가려졌어요. 나는 내수성 표시가 보이지만 SPF와 광범위 표시는 미상이에요. [kb:B-P01@0.6.1]

### 근거 및 이유
일반 야외용 선택 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요. [ref:S16]

### 확인이 필요한 한계
한 후보의 표시를 다른 후보에 옮기지 않으며, 표시만으로 개인의 보호 수준을 보증하지 않아요.

## syn-sol-0452

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f77d973dc81a8e3a786ca0d44a2a34abbe1a5aaae1d57764150f90c626799ffd`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 산책용 합성 자외선차단제의 SPF 50과 광범위 표시는 보이나 내수성 문구는 포장 접힌 부분에 가려졌어요. 아직 제품을 선택하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "가려진 내수성 표시는 없다고 단정하지 않아요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외 산책용 후보에서 SPF 50과 광범위 표시는 보이지만 내수성 문구는 접힌 부분에 가려졌어요. 아직 후보를 선택하지 않았고 표시가 없다고도 단정하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
일반 야외 선택 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
내수성 표시가 실제 있는지 확인되지 않았으며 표시가 개인의 보호 결과를 보증하지 않아요.

## syn-sol-0453

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3125c4a4e972a403446a3d8d3e0c7eb29519c5645a985a6bf732330b75ffaf15`
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
        "activity": "야외 자전거",
        "status": "후보"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.spf": {
      "variable_id": "product.spf",
      "state": "known",
      "value": {
        "current_container": "표시 닳아 읽지 못함",
        "old_same_name_container": 50,
        "version_match": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "이전 용기의 수치를 현재 후보에 자동 적용할 수 없어요."
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
자전거 활동용 후보의 현재 용기는 SPF 표시가 닳아 읽히지 않아요. 예전 같은 이름 용기의 SPF 50을 현재 버전에 자동 적용하지 말고 현재 표시를 확인해요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택 안내에서는 SPF와 광범위 보호, 내수성을 따로 확인해요. [ref:S16]

### 확인이 필요한 한계
두 용기의 버전 일치와 현재 SPF는 미상이에요.

## syn-sol-0454

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c0c99405e0a3fe3cabd95ec919ed5a8499ad384d9d2a572263ab8d9cdc429819`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 수영을 위해 새 합성 자외선차단제를 고르고 있어요. 후보 용기에 내수성은 표시됐지만 SPF와 광범위 보호 표시를 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "확인한 내수성과 미확인 SPF·광범위 보호를 구분해요."
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
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
야외 수영용 후보에 내수성 표시는 확인됐지만 SPF와 광범위 보호 표시는 아직 미상이에요. [kb:B-P01@0.6.1]

### 근거 및 이유
일반 야외용 선택 안내는 세 표시를 함께 확인하도록 권해요. [ref:S16]

### 확인이 필요한 한계
나머지 표시를 확인하기 전에는 후보의 조건을 확정하지 않아요.

## syn-sol-0457

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `0e0994ab6b68a6e5d1214d6de3fa230bc05b7f3c5270e3d41efad78219dca5fc`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "어제 저녁 합성 보습제는 소량 사용했어요. 오늘 야외에서 얼굴에 합성 자외선차단제를 바른 것은 기억하지만 그 도포량은 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "보습제의 어제 사용량으로 오늘 자외선차단제의 양을 판단하지 않아요."
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
어제 보습제를 소량 쓴 사실로 오늘 얼굴 선크림의 도포량을 판단하지 않아요. 오늘 사용은 기억하지만 양은 기록되지 않았어요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 기준은 노출 부위를 의도적으로 빼거나 아주 적게 바른 행동이 확인됐는지 살펴요 [kb:B-P02@0.6.1]. 다른 제품의 전날 사용량은 그 증거가 아니에요.

### 확인이 필요한 한계
오늘 선크림 도포량과 실제 개인 보호 수준은 미상이에요.

## syn-sol-0460

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `de41a93344c57eda50341130d9f5e6f2411241978c9dbf70d27125018ad5cf13`
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
        "오늘": "야외",
        "내일": "야외 계획"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "오늘": {
          "product": "합성 자외선차단제",
          "applied_sites": "기록 없음",
          "amount": "기록 없음"
        },
        "내일": {
          "plan": "고르게 바를 계획"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "계획을 실제 도포 기록으로 바꾸지 않아요."
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
내일 야외에서 고르게 바를 계획은 있지만 오늘 바른 부위와 양은 기록되지 않았어요. 계획을 오늘의 실제 도포로 판단하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
적용 부위와 양은 실제 행동을 확인해 살펴야 해요.

### 확인이 필요한 한계
오늘의 도포 부위와 양은 미상이에요.

## syn-sol-0461

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `fbf15c269333e530be10f328df313673b6bd446d9fbf8b4f493a666f6210eebe`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 쓴 합성 자외선차단제의 예전 용기 한 펌프 양은 기록돼 있어요. 새 펌프의 토출량과 실제 도포 부위는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "예전 펌프 기록만으로 새 펌프의 양이나 도포 범위를 확정하지 않아요."
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
예전 용기의 펌프 한 번 양을 새 펌프에 그대로 적용할 수 없어요. 실제로 바른 부위도 확인되지 않았어요. [kb:B-P02@0.6.1]

### 근거 및 이유
기록된 토출량의 펌프와 실제 도포 범위는 별도로 살펴요.

### 확인이 필요한 한계
새 펌프의 양이나 개인 보호 수준을 추정하지 않아요.

## syn-sol-0462

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `224a47ccf9173d4ed6189b92cf6cf361d0c0cc8b05489bedaa1ed7013b46d96e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 운동 중 합성 자외선차단제를 발랐고 땀도 났어요. 땀이 난 때와 다시 바른 때의 순서는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "발한과 재도포의 순서를 확인할 수 없어요."
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
야외 운동 중 선크림을 썼고 땀도 났지만 발한과 재도포의 순서는 기억나지 않아요. 땀 뒤에 다시 바르지 않았다고 단정하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
야외 활동과 발한에 맞춘 재도포를 살필 때 실제 순서와 제품 지침을 함께 고려해요 [kb:B-P03@0.6.1].

### 확인이 필요한 한계
땀과 재도포의 시간 순서 및 해당 제품의 지침은 확인되지 않았어요.

## syn-sol-0463

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `3ce4bc482a324285e07c81e5e066ca6bbb3e6ce132b9bbe06aa27d5ce569d94f`
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
        "실제": "야외 체류"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "reminder": "받음",
        "actual": "기록 없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림은 실제 재도포 기록이 아니에요."
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
야외에서 재도포 알림을 받았지만 실제로 다시 발랐는지는 기록되지 않았어요. 알림만으로 행동을 확정하지 않아요. [kb:B-P03@0.6.1]

### 근거 및 이유
재도포 검토에는 실제 야외 일정과 제품 지침을 함께 살펴요.

### 확인이 필요한 한계
실제 재도포 여부는 미상이에요.

## syn-sol-0464

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `01b7b8311d2850da734028a37a493651b78083b19a2de7004826f84ccb474d9a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 운동 중 합성 자외선차단제를 사용한 뒤 땀이 났고 야외 활동은 계속돼요. 다시 바를 계획은 있지만 실행 여부는 아직 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "계획과 실제 재도포 여부를 구별해요."
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
야외 운동 중 선제품을 쓴 뒤 땀이 났고 활동이 계속되고 있어요. 다시 바를 계획은 있지만 실제 실행은 확인되지 않았어요. [kb:B-P03@0.6.1]

### 근거 및 이유
계획과 실제 행동은 구분해 살펴요.

### 확인이 필요한 한계
재도포했거나 하지 않았다고 단정하지 않아요.

## syn-sol-0465

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `b58d5e83d60148c56739619b1a6275c678e627407e9ab25474c9f04692472bcb`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 긴소매를 입고 합성 자외선차단제를 사용해요. 모자나 그늘을 이용하는지는 기록되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "확인된 긴소매와 기록되지 않은 다른 수단을 분리해요."
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
야외에서 긴소매와 선크림을 사용한 사실은 확인돼요. 모자나 그늘 사용은 기록되지 않았으므로 사용하지 않았다고 판단하지 않아요 [kb:B-P04@0.6.1].

### 근거 및 이유
광보호 기준은 장시간 노출에서 실행 가능한 보완 수단을 모두 배제하는 상황을 살펴요 [kb:B-P04@0.6.1]. 긴소매 사용과 다른 수단의 미확인은 별개예요.

### 확인이 필요한 한계
모자와 그늘의 실제 이용 여부 및 가능 여부는 알려지지 않았어요.

## syn-sol-0466

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f560c724493422515cbb14c55d3edcbe17b24d6375f749e083d3148c1f0d1502`
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
        "activity": "야외 산책"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "self": {
          "product": "합성 자외선차단제",
          "used": true,
          "amount": "기억 못함",
          "sites": "기억 못함"
        },
        "friend": {
          "product": "친구 자신의 차단제",
          "amount": "극소량",
          "timing": "같은 날"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "친구의 행동을 본인의 도포량으로 옮기지 않아요."
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
본인은 산책 때 차단제를 썼지만 양과 부위는 기억나지 않고, 친구는 자기 제품을 극소량 썼다고 했어요. 친구의 양을 본인에게 옮기지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
사용량과 도포 부위는 각각 실제 사용자의 기록으로 확인해야 해요.

### 확인이 필요한 한계
본인의 도포량과 부위는 미상이에요.

## syn-sol-0468

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `6ab9b4d579d7f12c795b76340893a1199b836a7096d802959fc6e3e27607726e`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "오늘 야외에 머무르며 합성 자외선차단제를 처음 바른 뒤 재도포 알림을 받았어요. 알림 이후 실제로 다시 발랐는지는 기억하지 못해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림을 받은 사실과 실제 재도포 여부를 구분해요."
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
야외에서 처음 바른 뒤 재도포 알림을 받았지만 알림 이후 실제로 다시 발랐는지는 기억하지 못해요. [kb:B-P03@0.6.1]

### 근거 및 이유
알림 수신은 재도포 실행과 다른 기록이에요.

### 확인이 필요한 한계
확인되지 않은 행동과 개인의 보호 수준은 추정하지 않아요.

## syn-sol-0469

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `95e82e6de9a218c7948805a7f7f78ce4dc7a5b97723bdfe90960bfee599c00c4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 모자를 착용하고 합성 자외선차단제를 썼어요. 도포량과 귀에 발랐는지는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "모자 착용만으로 도포량이나 귀 도포를 확정하지 않아요."
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
야외에서 모자를 쓰고 선크림을 사용했지만 도포량과 귀 도포 여부는 기록되지 않았어요. 모자 착용만으로 이를 채우지 않아요 [kb:B-P02@0.6.1].

### 근거 및 이유
도포 기준은 노출 부위를 의도적으로 빼거나 아주 적게 바른 것이 확인됐는지 비교해요 [kb:B-P02@0.6.1].

### 확인이 필요한 한계
귀에 발랐는지와 도포량은 미상이며 실제 보호 수준을 계산할 수 없어요.

## syn-sol-0470

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `6d669e25bb19445d100a8038bd18a10753573634cd8edfb7e4767bd5b870b866`
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
        "context": "야외"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_use": "기록 없음",
        "clothing_coverage": "기록 없음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.shade_clothing": {
      "variable_id": "sun.shade_clothing",
      "state": "known",
      "value": {
        "shade_used": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "그늘 이용과 다른 보호 수단의 미확인을 구분해요."
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
야외에서 그늘을 이용한 것은 기억하지만 차단제 사용과 의복 범위는 기록되지 않았군요. 그늘 이용과 다른 수단의 미확인을 구분해요. [kb:B-P04@0.6.1]

### 근거 및 이유
노출 상황에서는 가능한 광보호 수단을 함께 살펴요.

### 확인이 필요한 한계
다른 수단을 사용했거나 배제했다고 추정할 수 없어요.

## syn-sol-0471

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `9b40348335daa1e66d9e96e9533ca1c3882bd66d987cd3fbac9219a631ea2545`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 활동 중 합성 자외선차단제 재도포 알림을 껐어요. 알림을 끈 뒤 실제 도포했는지는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림 해제는 도포 실행을 증명하지 않아요."
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
야외 활동 중 재도포 알림을 끈 사실만으로 이후 실제 도포 여부를 알 수 없어요. [kb:B-P03@0.6.1]

### 근거 및 이유
알림 설정과 몸에 바른 행동은 별개예요.

### 확인이 필요한 한계
이후 실행 여부는 기억나지 않으므로 미상으로 남아요.

## syn-sol-0474

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `5619d48a54b1a8e261ded03d1d9f61d5c9edfe288a0f639e4bff83548635d85a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "친구의 합성 화장품 용기는 뜨거운 차에 있었어요. 본인 용기의 과거 운송 온도는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "친구의 보관 이력을 본인 제품에 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
뜨거운 차에 있었던 것은 친구의 화장품 용기예요. 본인 용기의 운송 온도는 미상이므로 같은 열 노출을 받았다고 판단하지 않아요 [kb:B-S01@0.6.1].

### 근거 및 이유
보관 기준은 뜨거운 차 등 실제 부적절 보관을 살펴요 [kb:B-S01@0.6.1]. 일반 화장품 자료는 열·빛·공기와 취급을 품질 관련 요소로 다뤄요 [ref:S06].

### 확인이 필요한 한계
본인 용기의 과거 운송 조건과 개별 안정성은 확인되지 않았어요.

## syn-sol-0476

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e455577aaecd0486b28d96d88ec80267ba0cba7e4d6697b33477613ee8f66599`
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
        "배송 중": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "현재": "뚜껑 닫힘"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "현재": "직사광선 없는 곳"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 보관과 미확인 배송 온도를 구별해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
현재는 뚜껑을 닫고 직사광선이 없는 곳에 두고 계시군요. 배송 중 온도는 별도로 미상이에요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 안내는 온도와 빛, 공기 및 용기 상태를 함께 다뤄요. [ref:S06]

### 확인이 필요한 한계
현재 보관만으로 과거 배송 온도나 제품의 안정성을 확정할 수 없어요.

## syn-sol-0477

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `619c500d60c978569db62ef258ecba27054e2836d83d74b83d13f53ce422331a`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 보관 표시가 가려져 읽히지 않아요. 운반 중 열에 노출됐는지도 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "가려진 표시와 운반 이력은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
화장품의 보관 표시가 가려져 있고 운반 중 열 노출 여부도 확인되지 않았어요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 자료는 열과 빛, 공기 및 취급이 품질에 관련될 수 있다고 설명해요. [ref:S06]

### 확인이 필요한 한계
읽지 못한 지침이나 운반 이력을 추정해 제품 안정성을 확정하지 않아요.

## syn-sol-0478

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9c86bd54553dca40effbc2bfabe4fa7c63571f4bc66f3e087926e3e051e89f91`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 지금은 서랍에 닫아 보관해요. 지난 여행 중 뜨거운 차에 둔 적이 있는지는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 서랍 보관이 과거 노출 여부를 증명하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
지금은 합성 화장품을 닫아 서랍에 두지만 지난 여행 중 뜨거운 차에 있었는지는 기억나지 않아요. 현재 상태로 과거 노출을 확정하지 않아요 [kb:B-S01@0.6.1].

### 근거 및 이유
보관 기준은 뜨거운 차나 지속적으로 열린 용기 등 확인된 상태를 살펴요 [kb:B-S01@0.6.1]. 일반 자료는 온도와 용기·취급을 함께 다뤄요 [ref:S06].

### 확인이 필요한 한계
여행 중 보관은 미상이고 현재 보관 상태만으로 제품 안정성을 인증할 수 없어요.

## syn-sol-0480

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `6d6a3d50f8c3bf28df6b6a0344439678a4a707f0471a88094fb66db7e0cbf396`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "현재": "닫힘"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.light_air": {
      "variable_id": "storage.light_air",
      "state": "known",
      "value": {
        "과거 직사광선 노출": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "보관 표시 내용": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 닫힌 상태로 과거 이력이나 표시를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
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
용기는 지금 닫혀 있지만 과거 직사광선 노출 여부와 표시된 보관법은 확인되지 않았어요. 제품 표시를 확인해 보세요. [kb:B-S01@0.6.1]

### 근거 및 이유
빛과 용기 상태는 보관을 볼 때 따로 고려하는 요소예요. [ref:S06]

### 확인이 필요한 한계
현재 닫혀 있다는 사실로 과거 이력이나 품질을 정할 수 없어요.

## syn-sol-0482

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `5f2e03b03ec2f20644552f5dbe4a6bac113f35456de687a4bb0630cce8f624df`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품 가는 지난달 개봉했어요. 나의 개봉일은 모르며 가의 날짜를 나에게 적용하려고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 날짜와 나의 미확인 개봉일을 분리해요."
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
같은 이름이라도 지난달 개봉한 것은 제품 가예요. 그 날짜를 개봉일이 미상인 나에 적용하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
개봉 이력은 개별 용기에 연결해야 해요.

### 확인이 필요한 한계
나의 남은 사용기간이나 안전성은 이 기록으로 계산할 수 없어요.

## syn-sol-0483

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `adecd5a7e60d591f20c50039d9183eaa3cd72c42fd8459cacc240a388b1622aa`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 기한은 읽혔지만 개봉 날짜와 개봉 후 사용기간 표시는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "인쇄 기한으로 미확인 개봉 후 기간을 대신하지 않아요."
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
인쇄된 기한은 읽었지만 개봉 날짜와 개봉 후 사용기간 표시는 확인하지 못했어요. 인쇄 기한만으로 개봉 후 기간을 대신하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
사용기한 기준은 표시된 기한 경과와 명시된 개봉 후 안내와의 불일치를 각각 살펴요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
개봉일과 해당 안내가 미상이므로 개봉 후 사용 기간의 적합성을 확정할 수 없어요.

## syn-sol-0484

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `e161901c43accc44839a34a20d27dcf1dfd5e4daba161cbea02977b9633d5fe1`
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
        "개봉일": "기록함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.pao": {
      "variable_id": "storage.pao",
      "state": "known",
      "value": {
        "표시": "가려짐"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "표시기한": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "알려진 개봉일과 가려진 사용기간 표시를 구분해요."
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
개봉일은 기록됐지만 개봉 후 사용기간 표시는 가려졌고 표시기한도 확인하지 않았어요. 제품별 표시를 확인해 주세요. [kb:B-S02@0.6.1]

### 근거 및 이유
개봉일과 표시된 기간은 각각 필요한 정보예요.

### 확인이 필요한 한계
표시 기간을 읽기 전에는 기간 적합성을 판단할 수 없어요.

## syn-sol-0485

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `7864ae91efe4c8f409b101d40eeb457f43ff301e2655b5e69995ed21c33d19c0`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 구매일은 알지만 개봉일은 기록하지 않았어요. 구매일부터 개봉 후 기간을 계산하려고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "구매일을 개봉일로 바꾸지 않아요."
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
화장품의 구매일을 알아도 개봉일은 기록되지 않았어요. 구매일부터 개봉 후 기간을 계산하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
구매와 개봉은 서로 다른 사건이에요.

### 확인이 필요한 한계
개봉일과 그에 따른 경과 기간은 미상이에요.

## syn-sol-0486

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `6b3ac20625525c25a566850db31655141da0f5437d4f6d6240ecb44143d1e48c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "이전에 다 쓴 합성 화장품 용기의 개봉 날짜는 알아요. 새로 산 같은 이름의 용기 개봉 날짜는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "이전 용기의 개봉일을 새 용기에 적용하지 않아요."
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
이전에 다 쓴 용기의 개봉일은 알지만 새로 산 같은 이름의 용기는 기록하지 않았어요. 이전 날짜를 새 용기에 적용하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
사용기한과 개봉 후 안내는 실제 해당 용기의 이력과 비교해야 해요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
새 용기의 개봉일은 미상이며 같은 이름만으로 두 용기의 이력을 합칠 수 없어요.

## syn-sol-0487

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `2abab15b0740f792cdf9458f2debe2f20faf900427706bf89124b15995d84329`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.purchased_at": {
      "variable_id": "storage.purchased_at",
      "state": "known",
      "value": {
        "날짜": "확인 가능"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "표시기한": "확인 가능"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "개봉 여부": "기억나지 않음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "기억나지 않는 개봉 여부를 미개봉으로 단정하지 않아요."
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
구매 날짜와 표시기한은 보이지만 개봉했는지는 기억나지 않으시는군요. 미개봉으로 단정하지 않고 이력을 확인해요. [kb:B-S02@0.6.1]

### 근거 및 이유
구매일과 표시기한은 실제 개봉 여부를 대신하지 않아요.

### 확인이 필요한 한계
개봉 여부와 시점은 미상이에요.

## syn-sol-0488

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `01f3204b4f209f3aa12a4c0963073a9679d98ed81d48b7a878d69c98f70deeb5`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "친구가 같은 이름의 합성 화장품을 지난주 개봉했다고 말했어요. 본인 용기의 개봉일은 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "친구의 개봉일은 본인 용기의 기록이 아니에요."
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
친구가 지난주 개봉한 같은 이름의 제품과 본인 용기는 구분해요. [kb:B-S02@0.6.1]

### 근거 및 이유
다른 사람 용기의 날짜는 본인 용기의 개봉 기록이 아니에요.

### 확인이 필요한 한계
본인 용기의 개봉일은 미상이라 개봉 후 경과 기간을 계산할 수 없어요.

## syn-sol-0489

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `40c24ca39990805dd05e921f4970e6fbd94e97d61b84e7a7c8833d17dc8dd2da`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 가의 해외 용기에 기한이 적혀 있어요. 국내에서 보유한 나의 표시와 두 버전의 일치는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "해외 용기의 기한을 현재 보유품에 자동으로 옮기지 않아요."
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
해외 용기에는 기한이 보이지만 국내 보유품의 표시와 두 버전의 일치는 미상이에요. 해외 기한을 보유품에 자동으로 옮기지 않아요 [kb:B-Q03@0.6.1].

### 근거 및 이유
제품 확인 기준은 국가나 버전이 다른 제품의 정보를 현재 보유품에 덮어쓰지 않도록 구분해요 [kb:B-Q03@0.6.1].

### 확인이 필요한 한계
현재 국내 용기의 표시와 버전 일치를 확인하기 전 기한은 미상이에요.

## syn-sol-0490

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3e20c78b7f637db7316e09464f53ec2a0941657999b078693672ddbcf9ee2d67`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "대용량과 소용량 일치": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.container": {
      "variable_id": "storage.container",
      "state": "known",
      "value": {
        "대용량": "보관 지침 표시 확인",
        "소용량": "보유품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "제품 관계": "같은 이름"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "대용량 지침과 소용량 보유품의 버전 연결은 미상이에요."
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
같은 이름의 대용량 용기에는 보관 지침이 있지만, 보유한 소용량이 같은 버전인지는 확인되지 않았어요. 소용량 포장과 버전을 확인해 주세요. [kb:B-Q03@0.6.1]

### 근거 및 이유
이름이 같다는 사실만으로 서로 다른 용기의 정보가 같다고 볼 수 없어요.

### 확인이 필요한 한계
대용량 지침을 소용량에 그대로 적용할 근거는 아직 없어요.

## syn-sol-0491

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a2ab7b4f1362f9332d26ca2a0b725438d8e25e343ae2a2389c77f0fd1ab51772`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 이전 포장 사진에는 사용 안내가 보여요. 새 포장 보유품의 버전과 같은지 모르고 현재 표시를 아직 읽지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "예전 포장 안내를 현재 보유품에 자동 적용하지 않아요."
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
이전 포장 사진의 사용 안내가 현재 보유한 새 포장에 적용되는지는 미상이에요. [kb:B-Q03@0.6.1]

### 근거 및 이유
두 포장의 버전이 같은지 확인되지 않았으므로 예전 지시를 자동으로 옮기지 않아요.

### 확인이 필요한 한계
현재 용기의 표시와 버전 연결을 확인해요.

## syn-sol-0492

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `475f12d836752ac2fa80ddd32e859b995845cf649a214b250020ae5df696870c`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 판매 페이지와 실제 용기에 서로 다른 사용 안내가 있어요. 두 자료가 같은 버전인지 모르겠어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "기록의 차이와 동일 버전 여부 미확인을 구별해요."
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
판매 페이지와 실제 용기의 사용 안내가 다르지만 같은 버전인지 몰라요. 어느 한 안내를 임의로 현재 버전의 것으로 확정하지 않아요 [kb:B-Q03@0.6.1].

### 근거 및 이유
제품 확인 기준은 동명이나 리뉴얼 전후 제품을 자동으로 같은 것으로 취급하지 않아요 [kb:B-Q03@0.6.1].

### 확인이 필요한 한계
두 자료의 버전과 현재 용기에 적용되는 안내를 확인해야 해요.

## syn-sol-0493

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `94d1be0ddd97f210b65d81cdbf06bb6815adcdda3a897243add93518f83a0616`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "이전과 재구매품 일치": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "이전 용기": "성분표 남음",
        "새 용기": "표시 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "same_name_repurchase": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "같은 이름만으로 이전 성분표를 새 제품에 옮기지 않아요."
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
같은 이름의 제품을 다시 샀지만 이전 성분표만 남아 있고 새 용기 표시는 확인하지 못했어요. 새 제품의 표시와 버전을 확인해 주세요. [kb:B-Q03@0.6.1]

### 근거 및 이유
동일한 이름만으로 이전 성분표가 새 제품에도 적용된다고 정할 수 없어요.

### 확인이 필요한 한계
새 제품의 성분과 이전 버전과의 일치는 미상이에요.

## syn-sol-0494

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `c54d9d7204d7525c9ebde39581654c3ee9147a063bfcf2fa16de5aec271cd777`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "해외에서 산 합성 화장품 용기의 날짜를 국내 보유 용기 기록에 옮길 계획이에요. 아직 옮기지는 않았고 두 용기의 버전 일치는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "계획과 실행을 구분하고 버전 연결은 미상으로 남겨요."
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
해외 용기의 날짜를 국내 보유 용기 기록에 옮길 계획은 있지만 아직 실행하지 않았어요. 두 용기의 버전 일치도 미상이에요. [kb:B-Q03@0.6.1]

### 근거 및 이유
개별 용기와 제품 버전을 확인하기 전에는 날짜를 다른 용기에 옮기지 않아요.

### 확인이 필요한 한계
현재 기록만으로 두 용기의 날짜가 같다고 판단하지 않아요.

## syn-sol-0495

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `98cb7273ae1c379f2e7ab9f0e2a386454e162a2bbf02958c81bb8bca8b2ee872`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 날짜 중 연도가 가려져 있어요. 개봉일도 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "날짜의 보이는 부분만으로 기한 경과를 확정하지 않아요."
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
합성 화장품에 인쇄된 날짜의 연도가 가려져 있고 개봉일도 기록되지 않았어요. 보이는 부분만으로 기한이 지났다고 판단하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
사용기한 기준은 표시 기한의 경과나 개봉 후 안내와의 불일치가 확인됐는지 살펴요 [kb:B-S02@0.6.1].

### 확인이 필요한 한계
가려진 연도와 개봉일을 확인하기 전에는 기한 상태를 확정할 수 없어요.

## syn-sol-0496

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `468227a277490c697a17f57ff7dccf1ea92a9c84e4f8b7ea5736e044d80a49ca`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.purchased_at": {
      "variable_id": "storage.purchased_at",
      "state": "known",
      "value": {
        "가": "알고 있음",
        "나": "모름"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.opened_at": {
      "variable_id": "storage.opened_at",
      "state": "known",
      "value": {
        "가": "미확인",
        "나": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 구매일과 두 용기의 미확인 개봉일을 분리해요."
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
가의 구매일은 알지만 나의 구매일과 두 용기의 개봉일은 확인되지 않았어요. 각 용기의 이력과 표시를 따로 살펴봐요. [kb:B-S02@0.6.1]

### 근거 및 이유
구매일은 개봉일과 다르고 한 용기의 기록이 다른 용기의 기록을 대신하지 않아요.

### 확인이 필요한 한계
두 제품의 개봉일과 나의 구매일은 미상이에요.

## syn-sol-0497

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `be818348da6663d4ffda4c1981252bd6e67dde34483015b9f29dace6bc7bba05`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 현재 용기는 닫혀 있어요. 예전 포장 사진의 보관 문구가 현재 버전에 적용되는지 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 닫힌 상태와 옛 보관 지침의 버전 미확인을 구분해요."
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
현재 용기가 닫혀 있다는 사실과 예전 포장의 보관 문구가 현재 버전에 적용되는지는 별개예요. [kb:B-S01@0.6.1]

### 근거 및 이유
옛 문구와 현재 보유품의 버전 연결이 확인되지 않았어요.

### 확인이 필요한 한계
현재 제품의 보관 지침을 확인하기 전에는 옛 문구를 그대로 적용하지 않아요.

## syn-sol-0498

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `4f21b696e0dc766d2cf975f50fff599965ded48eccc48da9cf4891280b5223f4`
- 사람 검수: **미검수**

### 입력 원문

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 상자와 판매 페이지에 서로 다른 사용기한이 표시돼 있어요. 같은 버전인지 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "두 기록의 차이를 남기고 어느 쪽이 현재 버전인지 확인해요."
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
합성 화장품 상자와 판매 페이지의 사용기한이 서로 다르고 같은 버전인지 확인되지 않았어요. 어느 날짜가 현재 제품에 맞는지 임의로 정하지 않아요 [kb:B-Q03@0.6.1].

### 근거 및 이유
제품 확인 기준은 동명 제품이나 다른 버전의 정보를 자동으로 동일시하지 않아요 [kb:B-Q03@0.6.1].

### 확인이 필요한 한계
두 기록의 버전과 실제 보유 제품의 표시를 확인해야 해요.

## syn-sol-0348

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `05ec6d678aaf7c79b950cb7c4c4e28cab092091019eb65c8de0d2a359fb59dd0`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.time_of_day": {
      "variable_id": "method.time_of_day",
      "state": "known",
      "value": "evening",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "self": {
          "count": 1,
          "additional_wash": false,
          "purpose": "말하지 않음"
        },
        "housemate": {
          "count": 2,
          "consecutive": true
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
      "guidance": "본인의 한 번과 동거인의 반복을 구분하고 본인의 세안 목적은 미상으로 남겨요."
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
저녁에 본인은 얼굴을 한 번 씻고 추가로 씻지 않았으며, 두 번 연속 씻은 사람은 동거인이에요. 동거인의 행동을 본인에게 옮기지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
본인의 첫 세안 목적은 말씀하지 않아 알 수 없어요.

## syn-sol-0349

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `835e88a2e86ec4e2e9b16640579470c755a6a73835343580c4811f1ce8d5acdf`
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
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "water_rinses": "multiple"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "cleanser_reapplied": false,
        "first_use_purpose": "unknown",
        "cleanser_use_count": 1
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "여러 차례 물로 헹군 사실을 세정제의 반복 사용으로 바꾸지 않아요."
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
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
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
얼굴 세정제를 한 번 사용한 뒤 물로 여러 차례 헹군 것은 세정제를 반복해서 바른 행동과 달라요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 세안 자료는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
첫 사용의 목적은 알려지지 않았으므로 추정하지 않아요.

## syn-sol-0350

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `d902a9cb3bd36486c1616146e10fdef032a1fd04e451e50a3cb06f9cc0234301`
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
        "손가락"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.friction": {
      "variable_id": "method.friction",
      "state": "known",
      "value": {
        "face": "부드럽게",
        "arm": "거친 수건으로 강하게"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.drying": {
      "variable_id": "method.drying",
      "state": "known",
      "value": "수건으로 가볍게 눌러 말림",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face": {
          "washing": "손가락으로 부드럽게",
          "drying": "수건으로 가볍게 누름"
        },
        "arm": {
          "rubbing": "거친 수건으로 강하게"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "얼굴의 부드러운 세안과 가벼운 건조를 팔의 마찰과 구분해요."
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
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
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
얼굴은 손가락으로 부드럽게 씻고 가볍게 눌러 말린다고 하셨어요. 팔에서의 강한 수건 마찰을 얼굴 행동으로 옮기지 않고 확인된 얼굴 방법을 살펴요 [kb:B-C02@0.6.1].

### 근거 및 이유
얼굴 세정 기준은 도구 사용과 강한 마찰을 구분해요 [kb:B-C02@0.6.1]. 일반 얼굴 세안 자료도 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
팔의 행동과 얼굴의 행동은 별개이며 개인 결과를 보증하지 않아요.

## syn-sol-0353

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `6b2a8770884f3a536aef8a05666b70383071351e314f7b89a1e7968f83184598`
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
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "손 씻기": "뜨겁게 느낌",
        "얼굴 일상 세안": "뜨겁지 않은 미온수"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "손과 얼굴의 물 온도 경험을 구분하고 확인된 얼굴 세안의 미온수를 유지할 수 있어요."
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
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 씻는 물은 뜨겁게 느꼈지만 얼굴 세안은 뜨겁지 않은 미온수였다고 하셨어요. 얼굴의 확인된 방법을 유지할 수 있어요. [kb:B-C01@0.6.1]

### 근거 및 이유
손과 얼굴에서의 물 온도 경험은 구분해 살펴요.

### 확인이 필요한 한계
이 느낌만으로 정확한 온도나 개인의 결과는 알 수 없어요.

## syn-sol-0354

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f3c5ed80ca33bf7f8502917211018fae0adcb9141b87fd8400a9350a5d83bf13`
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
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "face_cleansing": "perceived_hot",
        "body_shower": "lukewarm"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "얼굴에 뜨겁게 느껴지는 물 대신 미온수 사용을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세안에 뜨겁게 느껴지는 물 대신 미온수 사용을 검토해요. [kb:B-C01@0.6.1]

### 근거 및 이유
몸 샤워의 미지근한 물과 얼굴 세안의 뜨거운 체감은 별도 상황이에요. 일반 얼굴 세안 자료를 참고해요. [ref:S03]

### 확인이 필요한 한계
정확한 온도나 개인의 결과는 기록만으로 알 수 없어요.

## syn-sol-0358

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `9f0918c7a58fada079727f6d483799db101968e14c8d66ea708a70444c2252c6`
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
        "face_cleansing": "부드럽게",
        "additional_face_rubbing_after_rinse": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "face_cleanser": "바로 헹굼"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face_cleanser": {
          "type": "일반 헹굼형",
          "separate_contact_time_instruction": false
        },
        "after_face_rinse": {
          "hands_washed_for_long_time": true,
          "additional_face_rubbing": false
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "aligned",
      "guidance": "얼굴 세정제를 부드럽게 사용한 것과 이후의 손 씻기를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세정제는 부드럽게 쓰고 바로 헹군 뒤 얼굴을 더 문지르지 않았어요. 이후 오래 씻은 부위는 손이므로 얼굴의 장시간 마찰로 보지 않아요 [kb:B-C03@0.6.1].

### 근거 및 이유
별도 지시 없이 얼굴 세정제를 일부러 오래 문지르거나 올려두는지 살펴요 [kb:B-C03@0.6.1]. 일반 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요 [ref:S03].

### 확인이 필요한 한계
별도 접촉시간 지시는 없다고 보고됐으며 개인 결과는 예측할 수 없어요.

## syn-sol-0360

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `f9c62915520e3b087577e3e5eb211d2217b5f52a6f4578c4c28b475f70d660ee`
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
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "cleanser": "부드럽게 바로 씻어냄",
        "instructions": "따름"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "mask": "별도 얼굴 팩을 오래 둠",
        "product_relation": "세정제와 다른 제품",
        "products_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "aligned",
      "guidance": "세정제 사용과 별도 팩의 시간을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세정제는 표시대로 부드럽게 바로 씻어내고 계시군요. 오래 두는 별도 팩의 시간을 세정제에 적용하지 않아요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반 세안 안내는 부드러운 세정과 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
팩의 구체적인 지시나 적합성은 여기서 확인되지 않았어요.

## syn-sol-0363

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `1cc86a8475cbed797f8bdd474b4f8e66c04556d0f9ed2faed2d8394c1dd2b600`
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
    "method.body_site": {
      "variable_id": "method.body_site",
      "state": "known",
      "value": "face",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "face_cleanser_rinsed_as_labeled": true,
        "body_rinse_off_product_rinsed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "얼굴 제품에서 확인된 헹굼과 바디 제품의 사용을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 헹굼형 세정제는 표시대로 사용하고 헹군 것으로 확인됐어요. 바디 제품은 헹구지 않은 별도 기록이에요. [kb:B-C06@0.6.1]

### 근거 및 이유
얼굴 제품의 확인된 헹굼을 다른 제품의 행동과 구분해요. 일반 얼굴 세안 자료도 헹굼을 다뤄요. [ref:S03]

### 확인이 필요한 한계
바디 제품의 기록을 얼굴 제품의 헹굼 누락으로 바꾸지 않아요.

## syn-sol-0368

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `03d214b19adb4c53e0a6b7e7ddd65c30e5fbe32ef12311f4cbd3eb343fc4d27a`
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
        "sunscreen": {
          "used_on_face": true,
          "removal_instruction": "unknown",
          "application_amount_reduced": false
        },
        "question": "사용한 선크림 제거 방법 검토"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "제거 지시가 미확인인 채 특정 제거법의 충분성을 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
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
얼굴에 사용한 선크림을 어떻게 지울지 살피고 계세요. 도포량은 줄이지 않았고 해당 제품의 제거 지시는 미상이므로 특정 제거법이 충분하다고 단정하지 않아요 [kb:B-I01@0.6.1].

### 근거 및 이유
제거 편의 때문에 광보호를 줄이거나 내수성 표시만 보고 무조건 반복하는 행동을 구분해 살펴요 [kb:B-I01@0.6.1]. 제한된 제품 조합의 소규모 비교를 모든 제품의 제거법으로 일반화할 수 없어요 [ref:S08].

### 확인이 필요한 한계
해당 제품의 제거 지시와 실제 제거 결과는 확인되지 않았어요.

## syn-sol-0370

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `07188ce1c8b518c0d95c6fca4c480005cb7052d8e9c783fc33b880f4e114f985`
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
        "self": {
          "sunscreen": "표시량대로 도포",
          "removal": "검토"
        },
        "family": {
          "sunscreen": "극소량 도포",
          "reason": "세안 번거로움"
        },
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "aligned",
      "guidance": "본인의 광보호 사용 유지와 가족의 행동을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
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
본인은 얼굴 선크림을 표시량대로 바르며 제거법을 검토하고 계시군요. 광보호 사용은 유지하고, 가족의 극소량 사용을 본인 행동으로 옮기지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 비교만으로 모든 내수성 제품에 특정 제거 단계를 정할 수 없어요. [ref:S08]

### 확인이 필요한 한계
본인이 사용하는 제품의 구체적인 제거 지시는 확인되지 않았어요.

## syn-sol-0371

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `16b8611a757e0ba7c2fbf06a6a9942ba1525dd9dc9c6b10ca74ddb7bfffb3618`
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
      "value": "rinse_off_mask",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "container_version": "2.0",
        "reported_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "version_1_0_rinse_after_minutes": 5,
        "version_2_0_contact_time": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "unknown",
      "guidance": "현재 2.0 용기에 이전 1.0의 시간을 그대로 적용하지 않고 해당 버전의 표시를 확인해요."
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
실제로 쓰는 얼굴 팩은 2.0인데 5분 지시는 보관한 1.0 표시에 있어요. 2.0의 사용시간을 해당 버전 표시에서 확인해요. [kb:B-G03@0.6.1]

### 근거 및 이유
이전 버전의 시간을 현재 용기에 자동 적용할 수 없어요.

### 확인이 필요한 한계
2.0의 사용시간은 아직 미상이에요.

## syn-sol-0372

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `614c68f50a71273b650322c729bf2e1e6280851196f5617664ea6a00dc6c989e`
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "candidate_cleanser": {
          "type": "얼굴용 씻어내는 세정제",
          "synthetic_ingredient_list_checked": true,
          "ph_disclosed": false,
          "used": false
        },
        "question": "표시만으로 약산성인지"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "성분표만으로 공개되지 않은 pH나 약산성 여부를 확정하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
새로 고를 얼굴용 씻어내는 세정제의 합성 성분표는 확인했지만 pH는 공개되지 않았어요. 표시만으로 약산성이라고 확정하지 않아요 [kb:B-C04@0.6.1].

### 근거 및 이유
약산성 여부를 비교하려면 완제품의 확인된 pH가 필요하며 미확인은 차이로 판정하지 않아요 [kb:B-C04@0.6.1].

### 확인이 필요한 한계
제품은 아직 사용하지 않았고 pH나 개인 반응을 성분표에서 추측할 수 없어요.

## syn-sol-0373

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `991a5446b71523f04b62d69b5ab825da65f2a5fa7bc3eba0baf741fba101d734`
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
        "products": "얼굴용 로션 두 개",
        "container_sizes": "다름",
        "actual_amounts": "기록 없음",
        "name_based_purpose_or_order": "결정하지 않음",
        "products_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "용기 크기만으로 실제 사용량이나 순서를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "습식 면도 전에는 털을 물에 적시고 준비할 수 있어요. 면도할 때 털이 난 방향을 따르고 날을 헹구는 방법이 안내돼요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": [
    "ref:S23"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
두 얼굴 로션의 용기 크기는 다르지만 실제 사용량은 기록되지 않았어요. 용기 크기만으로 양이나 사용 순서를 추정하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
제품 용기와 실제 사용량·용도는 별개로 살펴야 해요.

### 확인이 필요한 한계
상품명만으로 용도나 순서를 결정하지 않았고 실제 사용량은 미상이에요.

## syn-sol-0375

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `edacf4948732cd50ea822b54722058e0d6ae5aa129a510614a65f8bc08ac1683`
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
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "relative_use_amount": "double"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "believed_double_use_doubles_formula_concentration": true,
        "use_amount_increased": true,
        "ingredient_concentration": "not_disclosed"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "사용량을 두 배로 늘려도 제품 제형의 성분 농도가 두 배가 되는 것은 아니에요. 사용량과 공개되지 않은 농도는 별개로 살펴요."
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
얼굴 세정제의 사용량을 두 배로 늘려도 제형 속 성분 농도가 두 배가 되는 것은 아니에요. [kb:B-G02@0.6.1]

### 근거 및 이유
제품을 쓰는 양과 제형의 농도는 서로 다른 정보예요.

### 확인이 필요한 한계
농도는 공개되지 않았으므로 수치를 추정하지 않아요.

## syn-sol-0376

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3c7e9df41c69219d29accb85f643384c984741aabfc2b9a2ca928de14321babd`
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
        "self": {
          "face_product": {
            "follows_current_label_amount_and_frequency": true,
            "considering_amount_change": true
          }
        },
        "friend": {
          "face_product": {
            "increased_amount_without_instruction": true,
            "reason": "많이 바를수록 좋다"
          }
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "aligned",
      "guidance": "본인의 표시 사용과 사용량 검토를 친구의 임의 증량과 구분해요."
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
본인은 얼굴 제품의 현재 표시된 양과 빈도를 따르면서 사용량 변경을 검토하고 있어요. 친구의 임의 증량을 본인의 행동으로 옮기지 않아요 [kb:B-G02@0.6.1].

### 근거 및 이유
제품별 양과 빈도는 각각의 표시와 실제 행동을 비교하며, 많이 바를수록 좋다는 이유만으로 임의 증량하는 경우를 구분해요 [kb:B-G02@0.6.1].

### 확인이 필요한 한계
본인이 앞으로 양을 바꿀지는 아직 결정되지 않았고 표시량이 개인 결과를 보증하지 않아요.

## syn-sol-0377

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `ae77bc93adafe6b259af08f94ffb8905253962903e2cf414a275102ce7a2e1ee`
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
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "현재 사용량": "unknown",
        "검토": "줄일지 검토"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "제품 성분 농도": "unknown",
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "현재 사용량과 미확인 농도를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
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
얼굴 제품의 양을 줄일지 고민 중이지만 현재 양은 알려지지 않았어요. 해당 제품의 현재 사용량과 표시된 용법을 먼저 살펴봐요. [kb:B-G02@0.6.1]

### 근거 및 이유
사용량과 제품에 들어 있는 성분 농도는 다른 정보예요.

### 확인이 필요한 한계
현재 양과 성분 농도는 모두 미상이며 어느 쪽도 추정하지 않아요.

## syn-sol-0378

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `881db17465f2d5296f57517f7a782065949a29eab5d92fead3074e398d948600`
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
    "product.type": {
      "variable_id": "product.type",
      "state": "known",
      "value": "lotion",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "pumps_per_use": 2
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "plans_change_amount": true,
        "ingredient_concentration": "not_disclosed",
        "data_for_pumps_to_concentration": false,
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "사용량 변경과 공개되지 않은 성분 농도를 구분하고 농도 수치를 추정하지 않아요."
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
얼굴 로션을 현재 두 펌프 쓰고 양을 바꾸려는 계획과 제품 속 성분 농도는 구분해요. [kb:B-G02@0.6.1]

### 근거 및 이유
펌프 수는 제형의 농도를 알려주지 않아요.

### 확인이 필요한 한계
농도는 공개되지 않았고 펌프 수에서 계산할 자료도 없어 수치를 추정하지 않아요.

## syn-sol-0381

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `a65d04a4bd3aef2962c9373bea924b90a8bc71932ebeb54f275268ef76a24177`
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
        "rinse_off_pack": {
          "used": true,
          "container_version": "unknown",
          "intended_use": "얼굴용"
        },
        "web_other_version": {
          "usage_time_matches_container": "unknown"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "unknown",
      "guidance": "다른 버전의 지시를 현재 용기에 그대로 적용하지 않아요."
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
얼굴용 헹굼형 팩을 사용했지만 용기의 판을 확인하지 못했어요. 웹에서 본 다른 판의 사용 시간을 이 용기에 그대로 적용하지 않아요 [kb:B-G03@0.6.1].

### 근거 및 이유
제품별 용법은 일반 세안제와 팩 등을 구분하고 해당 제품의 지시를 살펴야 해요 [kb:B-G03@0.6.1].

### 확인이 필요한 한계
현재 용기 버전과 웹에서 본 시간의 일치 여부는 미상이에요.

## syn-sol-0385

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `3e0b01170f95d6cb89e6405580b42b4df5abaf32aee85d40c2a402a12e6e7b8e`
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
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "actual_device": "2.0",
        "actual_combination": "얼굴용 젤",
        "device_1.0_label": "그 젤과 병용 가능",
        "device_2.0_instruction": "미확인",
        "device_and_gel_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "이전 1.0의 병용 지시를 실제 사용 중인 2.0 기기에 그대로 적용하지 않아요."
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

### 핵심 안내
얼굴용 기기 2.0과 젤을 함께 사용하고 계시군요. 1.0의 병용 표시를 2.0에 그대로 적용하지 않고 실제 기기의 지침을 확인해요. [kb:B-G06@0.6.1]

### 근거 및 이유
기기별 지침과 실제 병용이 일치하는지 따로 살펴야 해요.

### 확인이 필요한 한계
2.0의 병용 지시는 아직 미확인이라 해당 조합의 적합성을 정하지 않아요.

## syn-sol-0388

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `1a20634e7368b7e05dbaceae2c4d486e1e93b7a0540de2defe2d3b2429aa69a6`
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
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "device_and_gel_used_together": true,
        "device_and_gel_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_gel_version": "unknown",
        "match_to_permitted_gel": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "실제 병용 사실과 허용된 제품 버전의 일치 여부를 구분해요."
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

### 핵심 안내
얼굴 기기와 젤을 함께 사용했지만 사용한 젤이 기기에 허용된 것과 같은지는 확인되지 않았어요. [kb:B-G06@0.6.1]

### 근거 및 이유
실제 병용과 허용된 제품 버전의 일치는 별도 정보예요.

### 확인이 필요한 한계
젤의 버전이 미상이므로 병용 적합성을 확정하지 않아요.

## syn-sol-0392

- 모드·분할: `solution` / `val_internal`
- 현재 내용 해시: `f0f9d914734329ca2456e1290928557869f544c8c9653bf12c2950a573c5f632`
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
    "constraints.preferences": {
      "variable_id": "constraints.preferences",
      "state": "known",
      "value": {
        "face_product_fragrance": "fragrance_free_preferred"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "family": {
          "specific_fragrance_allergy_reported": true
        },
        "self": {
          "allergy": "unknown"
        }
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "가족의 알레르기와 본인의 향 선호를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
가족이 특정 향료 알레르기를 말했고 본인은 향 없는 얼굴용 제품을 선호해요. 가족의 알레르기를 본인의 진단으로 옮기지 않아요 [kb:B-G17@0.6.1].

### 근거 및 이유
개인의 선호와 알레르기, 다른 사람의 경험은 구분해야 해요 [kb:B-G17@0.6.1]. 향료 표시만으로도 개인의 알레르기 반응이 확정되지는 않아요 [ref:S15].

### 확인이 필요한 한계
본인의 알레르기 여부는 미상이며 특정 향료명은 주어지지 않았어요.

## syn-sol-0394

- 모드·분할: `solution` / `train`
- 현재 내용 해시: `82462f1afaefc179bae3d9860f998faec7590e76209545e85eb13eb2c2f58d0e`
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
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "이전 버전 성분표": "향료명 확인",
        "현재 용기": "성분표 미확인",
        "product_intended_site": "face"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.version": {
      "variable_id": "product.version",
      "state": "known",
      "value": {
        "현재 용기": "미확인",
        "관계": "같은 이름의 이전 버전 표시"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "이전 성분표의 표시를 현재 용기의 성분으로 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
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

### 응답 초안 — 미승인

### 핵심 안내
선택 중인 얼굴 제품과 이름이 같은 이전 버전에서 향료명을 보셨군요. 현재 용기의 버전과 성분표를 확인하기 전에는 이전 표시를 그대로 적용하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
성분 표시와 개인의 알레르기 반응은 별개의 정보예요. [ref:S15]

### 확인이 필요한 한계
현재 용기의 성분과 버전은 미상이에요.
