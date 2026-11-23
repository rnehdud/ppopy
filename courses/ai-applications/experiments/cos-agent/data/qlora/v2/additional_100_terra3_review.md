# 추가 개발 후보 100턴

기존 348턴을 변경하지 않고 추가한 안내 77턴·보류 23턴입니다. 합계는 448턴입니다.
`development_preview`, `production_enabled=false`이며 실제 사용자 자료나 임상 정답이 아닙니다.
작성 담당과 별도 문맥의 Codex 감사 담당을 분리합니다. 동일 GPT 계열의 감사는 다른 모델 계열의 공식 검수나 사람 승인을 대체하지 않습니다.
사람 검수는 미검수이며, 현재 감사 판정은 `reviews/additional_100_terra3_codex_independent.*`에서 내용 해시와 함께 확인합니다.
합성 방어 청크는 실제 문헌 인용문이 아니며 감사용 출처 분류를 유지합니다. KB 판정 근거는 비교 명세를 대조한 작성 기록이지 엔진 실행 결과가 아닙니다.

## 사례 목록

| ID | 유형 | 사례 | 분할 |
|---|---|---|---|
| syn-sol-0285 | normal_guidance | 화장 제거와 추가 단계 확인 | train |
| syn-sol-0286 | normal_guidance | 친구의 부드러운 세안과 본인의 강한 마찰 | train |
| syn-sol-0291 | normal_guidance | 기기 사용은 확인되고 강도는 미상 | train |
| syn-sol-0297 | normal_guidance | 면도 뒤 크림 반응과 별도 제품 미사용 | train |
| syn-sol-0322 | normal_guidance | 실외 운동 후 계속된 노출과 발한 | val_internal |
| syn-sol-0323 | normal_guidance | 물놀이 뒤 마른 옷으로 갈아입고 계속 야외에 있음 | train |
| syn-sol-0324 | normal_guidance | 실외 근무 중 지속 노출과 휴식 기록 | train |
| syn-sol-0325 | normal_guidance | 야외행사에서 손으로 땀을 닦은 뒤 | train |
| syn-sol-0326 | normal_guidance | 차양이 가능한 긴 야외 대기 | train |
| syn-sol-0327 | normal_guidance | 야외 관람 중 옷차림 선택 가능 | train |
| syn-sol-0328 | normal_guidance | 표시된 정상 이층과 흔든 뒤 상태 | train |
| syn-sol-0329 | normal_guidance | 기한 지난 선크림과 최근 구매일 | train |
| syn-sol-0333 | normal_guidance | 가려진 보관 표시와 알려진 현장 보관 | train |
| syn-sol-0336 | normal_guidance | 원래 용기에 물을 더하려는 계획 | train |
| syn-sol-0338 | normal_guidance | 얼굴 바깥 노출 부위와 제품 범위 | train |
| syn-hold-0084 | hold | 얼굴 세안 후 지속 통증과 사용 제품 미상 | train |
| syn-hold-0085 | hold | 손의 지속 불편과 얼굴 세안 질문 | train |
| syn-hold-0086 | hold | 지속 얼굴 따가움과 제품 버전 확인 거절 | train |
| syn-hold-0087 | hold | 얼굴 세정 뒤 지속 불편과 통증 | train |
| syn-hold-0088 | hold | 세정 기기 사용 뒤 지속 얼굴 통증 | train |
| syn-hold-0089 | hold | 손 씻기 뒤 지속 불편과 친구 경험 | train |
| syn-hold-0090 | hold | 세안 중단 이후에도 지속되는 불편 | train |
| syn-hold-0091 | hold | 두 제품을 함께 쓴 뒤 지속 통증 | train |
| syn-hold-0092 | hold | 면도 부위의 지속 불편 | train |
| syn-hold-0093 | hold | 손에 지속되는 불편 | train |
| syn-hold-0094 | hold | 보습 사용 시 지속 통증 | train |
| syn-hold-0095 | hold | 손 보습제의 새 냄새 변화 | train |
| syn-hold-0096 | hold | 얼굴 보습제의 새 층 분리 | train |
| syn-hold-0097 | hold | 면도 후 제품의 새 색 변화 | train |
| syn-hold-0098 | hold | 보습 제품의 새로운 누출 | train |
| syn-hold-0099 | hold | 수령 뒤 처음 확인한 새 냄새와 누출 | train |
| syn-hold-0100 | hold | 기한 표시가 읽히는 용기의 새 변색 | val_internal |
| syn-hold-0101 | hold | 흔들어 쓰는 선크림에서 새 악취 | val_internal |
| syn-hold-0102 | hold | 같은 이름 두 제품 중 한쪽의 새 입자와 색 변화 | train |
| syn-hold-0103 | hold | 보관 조건 확인 후 발생한 새 질감 변화 | train |
| syn-hold-0104 | hold | 외관 점검 이후 생긴 새 냄새 | train |
| syn-hold-0105 | hold | 개봉 전 용기 팽창과 새 누출 | train |
| syn-hold-0106 | hold | 제조번호 확인 후 별도로 발견한 냄새 변화 | train |
| syn-sol-0274 | unknown_or_version | 손의 거친 수건과 얼굴의 가벼운 건조 | train |
| syn-sol-0278 | unknown_or_version | 내수성 제품의 사용 계획과 미사용 | train |
| syn-sol-0279 | unknown_or_version | 다른 사람의 반복과 본인 행동 미상 | train |
| syn-sol-0280 | unknown_or_version | 얼굴이 아닌 팔에만 내수성 제품 사용 | train |
| syn-sol-0281 | unknown_or_version | 확인되지 않은 제품 버전의 제거 표시 | train |
| syn-sol-0282 | unknown_or_version | 사용한 제품 라벨의 제거 조건 일부 누락 | train |
| syn-sol-0283 | unknown_or_version | 세안 도구 이름과 제거 조건 구분 | train |
| syn-sol-0284 | unknown_or_version | 첫 세정과 재세정의 시점 미상 | val_internal |
| syn-sol-0287 | unknown_or_version | 얼굴에 닿지 않은 도구 | train |
| syn-sol-0288 | unknown_or_version | 사용 제품 내수성 미상과 다른 제품 표시 | train |
| syn-sol-0289 | unknown_or_version | 반복 세안 중단 계획과 실제 행동 | train |
| syn-sol-0290 | unknown_or_version | 손 위생 행사와 얼굴 세안 기록 충돌 | train |
| syn-sol-0292 | unknown_or_version | 땀을 흘린 시간과 세안 횟수 미상 | train |
| syn-sol-0293 | unknown_or_version | 서로 충돌하는 제거 표시 사본 | train |
| syn-sol-0294 | unknown_or_version | 얼굴과 목의 보습 시점 분리 | val_internal |
| syn-sol-0295 | unknown_or_version | 건조 피부 지시가 다른 두 제품 | val_internal |
| syn-sol-0296 | unknown_or_version | 손 씻기 뒤 실제 보습의 주체 | val_internal |
| syn-sol-0298 | unknown_or_version | 보습제 사용과 목의 건조 재발 | train |
| syn-sol-0299 | unknown_or_version | 필요한 손 씻기와 작업 뒤 보습 계획 | train |
| syn-sol-0300 | unknown_or_version | 면도 후 목과 얼굴의 반응 구분 | train |
| syn-sol-0301 | unknown_or_version | 손 보습제 무향료 표시와 향성 오일 정보 | train |
| syn-sol-0302 | unknown_or_version | 면도 후 다른 사람의 반응 | train |
| syn-sol-0303 | unknown_or_version | 얼굴은 편안하고 손은 확인 거절 | train |
| syn-sol-0304 | unknown_or_version | 보습 목표와 사용 경험이 다른 부위 | train |
| syn-sol-0305 | unknown_or_version | 면도 후 제품 지시와 사용 기록의 연결 | train |
| syn-sol-0306 | unknown_or_version | 면도 후 불편의 다른 주체 | train |
| syn-sol-0307 | unknown_or_version | 반응 없는 부위와 반응 미상 부위 | train |
| syn-sol-0308 | unknown_or_version | 제품 변경과 계절 변화의 시점 미상 | train |
| syn-sol-0309 | unknown_or_version | 보습 단계 추가 전 실제 사용 미상 | train |
| syn-sol-0310 | unknown_or_version | 보습제 후 촉촉함과 나중의 느낌 미상 | train |
| syn-sol-0311 | unknown_or_version | 보습 시점과 처방 계획의 적용 범위 미상 | train |
| syn-sol-0312 | unknown_or_version | 향료 목록과 사용 경험이 서로 다른 손 제품 | train |
| syn-sol-0313 | unknown_or_version | 면도 뒤 보습을 했지만 반응 시점 미상 | train |
| syn-sol-0314 | unknown_or_version | 세정 후 피부 물기와 실제 제품 사용 분리 | train |
| syn-sol-0315 | unknown_or_version | 세안 직후 제품을 썼으나 물기 확인 거절 | train |
| syn-sol-0316 | unknown_or_version | 손 진단을 이유로 보습 전체 중단 | train |
| syn-sol-0317 | unknown_or_version | 건조에도 고정 감량을 계획만 한 경우 | train |
| syn-sol-0318 | unknown_or_version | 다른 제품의 성분과 보습감 구분 | train |
| syn-sol-0319 | unknown_or_version | 손 위생 뒤 피부 상태와 제품 반응 구분 | train |
| syn-sol-0320 | unknown_or_version | 두 야외 후보의 표시 일부만 확인 | train |
| syn-sol-0321 | unknown_or_version | 현재 후보가 아닌 예전 후보의 성능표 | train |
| syn-sol-0330 | unknown_or_version | 두 개 중 개봉일이 확인된 선크림 | train |
| syn-sol-0331 | unknown_or_version | 여행 파우치의 현재 보관과 과거 열 노출 | train |
| syn-sol-0332 | unknown_or_version | 두 용기 중 타인 용기의 뜨거운 차 보관 | train |
| syn-sol-0334 | unknown_or_version | 다른 나라 용기의 사용기한 표시 | train |
| syn-sol-0335 | unknown_or_version | 리필 지침의 대상과 실제 용기 연결 미상 | train |
| syn-sol-0337 | unknown_or_version | 서로 다른 용기의 개봉 이력 | val_internal |
| syn-sol-0339 | unknown_or_version | 소량 도포 여부를 다른 제품 기록으로 추정 | train |
| syn-sol-0340 | unknown_or_version | 햇빛 차단 의복의 적용 부위 미상 | val_internal |
| syn-sol-0341 | unknown_or_version | 재도포 알림과 실제 행동을 구분 | val_internal |
| syn-sol-0342 | unknown_or_version | 뚜껑을 열어 둔 제품과 별도 선크림 | train |
| syn-sol-0343 | unknown_or_version | 동일명 선크림 두 버전의 분무 여부 | train |
| syn-sol-0344 | unknown_or_version | 사용기한과 다른 용기의 정상 이층 안내 | train |
| syn-sol-0268 | distractor_or_defense | 손 씻기와 얼굴 반복을 별도 계산 | train |
| syn-sol-0269 | distractor_or_defense | 손 세정 횟수만 확인 | train |
| syn-sol-0270 | distractor_or_defense | 흙 노출 후 별도 얼굴 세정 | train |
| syn-sol-0271 | distractor_or_defense | 땀과 추가 단계의 연결 미상 | val_internal |
| syn-sol-0272 | distractor_or_defense | 기기 보유와 얼굴 사용 구분 | train |
| syn-sol-0273 | distractor_or_defense | 기기는 손에만 쓰고 얼굴은 강한 수건 마찰 | train |
| syn-sol-0275 | distractor_or_defense | 기기 미사용과 수건 압력 미상 | train |
| syn-sol-0276 | distractor_or_defense | 서로 다른 두 제품의 제거 표시 | train |
| syn-sol-0277 | distractor_or_defense | 내수성 표시만을 이유로 연속 세 단계 | train |

## syn-sol-0285 — 화장 제거와 추가 단계 확인

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `90543131551d69e15894166d17cd0d0fade655ac061fe1f267e785dca69948df`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

화장 제거 목적이 확인돼 두 단계라는 수만으로 차이를 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 화장 제거를 위해 세정 단계 두 가지를 사용했다고 보고했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
화장 제거 목적이 확인돼 두 단계라는 수만으로 차이를 판정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0286 — 친구의 부드러운 세안과 본인의 강한 마찰

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `77fa89de13e2ad0dca6cdbff29b371e24e972061b1169d6851f2c0f60819de93`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 사람의 습관과 구분해 본인의 강한 마찰을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "친구는 손끝으로 부드럽게 씻지만 본인은 얼굴을 거친 천으로 강하게 문지릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
다른 사람의 습관과 구분해 본인의 강한 마찰을 검토해요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0291 — 기기 사용은 확인되고 강도는 미상

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `102ed019908ef019f80acb48f0ae1fca384f565e4adf0a57ab9594bb99bdb12c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴에 손가락 외 기기를 사용하는 차이는 확인됐지만 압력이나 마찰의 세기는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "본인이 얼굴 세정 기기를 사용하지만 압력과 마찰의 세기는 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "face_device_used": true,
        "friction": "unknown"
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
얼굴에 손가락 외 기기를 사용하는 차이는 확인됐지만 압력이나 마찰의 세기는 미상이에요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴 마찰의 강도는 추정하지 않아요.

## syn-sol-0297 — 면도 뒤 크림 반응과 별도 제품 미사용

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `453c9074291e57f7edb06a20dd52d60f474d6061b74909b9ba65da6a07c35730`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

면도 후 견딜 수 있는 보습을 사용하며 별도 후처리 제품은 필수가 아니에요.

### 입력

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

## syn-sol-0322 — 실외 운동 후 계속된 노출과 발한

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `0e0e4f1a3cecc3ec42464e1465bf176549fea5fd9f4571f1a8613516295b3926`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

발한 이후 노출이 이어진 상황을 반영해 재도포를 고려해요.

### 입력

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

## syn-sol-0323 — 물놀이 뒤 마른 옷으로 갈아입고 계속 야외에 있음

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `6f62cce18fcb8c2d5fa9fc0f1cc0758ecd941b877912bfd96be89be3f83e67cc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

물 접촉 후에도 야외에 머문 점을 반영해 재도포를 고려해요.

### 입력

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

## syn-sol-0324 — 실외 근무 중 지속 노출과 휴식 기록

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `29136bbc0041c2137f228a49ff68ac9d028af46001ab23db4c3c54975b313ecb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속된 야외 노출에 맞춰 재도포할 기회를 검토해요.

### 입력

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

## syn-sol-0325 — 야외행사에서 손으로 땀을 닦은 뒤

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `6ab5da6e62e4f636bd816ccb147538549cdb627eac531ede00b437d65f200169`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

닦임과 이어지는 노출을 반영해 재도포를 고려해요.

### 입력

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

## syn-sol-0326 — 차양이 가능한 긴 야외 대기

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `65f14ff89c5c6a385bdfc72ff06f52a045ac5eece1930bf88d5db32308603123`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가능한 차양을 함께 활용하는 방안을 검토해요.

### 입력

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

## syn-sol-0327 — 야외 관람 중 옷차림 선택 가능

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `e94652ae0e7791434ec79eb4a2a721a39d6e9d672fc9097bfb6fe9e58ad08320`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가능한 의복을 광보호에 함께 활용하는 방안을 검토해요.

### 입력

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

## syn-sol-0328 — 표시된 정상 이층과 흔든 뒤 상태

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `9118e07af8a6586c612635aa7375968a62df319c6dfde17debba29dc266ce573`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시된 정상 분리를 곧바로 품질 이상으로 판정하지 않아요.

### 입력

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

## syn-sol-0329 — 기한 지난 선크림과 최근 구매일

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `428a890970626b4b5f2cfef02cdeedf4d6e1630cb360208cfbf794ce44a09c93`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

구매가 최근이어도 표시 기한이 지난 선크림은 사용하지 않는 방향으로 확인해요.

### 입력

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

## syn-sol-0333 — 가려진 보관 표시와 알려진 현장 보관

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `5d4de8682ce597de43a7b41d212ef026374311580dae0241fd6dfe9cc4b9ddf0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

과도한 열을 피하는 쪽으로 보관을 조정해요.

### 입력

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

## syn-sol-0336 — 원래 용기에 물을 더하려는 계획

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `8df09e907aef3455b0713a40c4b783c0561d8cf1caee37154b40729a31bf11ac`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제조사 지시 없이 원제품에 물을 섞지 않는 방향을 검토해요.

### 입력

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

## syn-sol-0338 — 얼굴 바깥 노출 부위와 제품 범위

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `acd6a67e0f7bd9b9028a3e5d3fce383ee37b1479efec92e86337213572452986`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시된 사용 범위 안에서 노출된 귀의 누락을 검토해요.

### 입력

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
표시된 사용 범위 안에서 노출된 귀의 누락을 검토해요. [kb:B-P02@0.6.1]

### 근거 및 이유
얼굴과 귀에 사용 가능하다는 표시가 있고 귀는 의도적으로 제외됐어요. [kb:B-P02@0.6.1]

### 확인이 필요한 한계
실제 도포량과 보호 수준은 측정되지 않았어요.

## syn-hold-0084 — 얼굴 세안 후 지속 통증과 사용 제품 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `34d2b601dd7fca0152b5a14833eafb8d391d7c30c3342c9c83a07fb22a720eec`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 세안 후 불편감과 통증이 지속되지만 사용 제품은 기억하지 못합니다.",
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
얼굴 세안 후 불편감과 통증이 지속되고 사용 제품은 확인되지 않았어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0085 — 손의 지속 불편과 얼굴 세안 질문

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `386a7f6f0d89b2b0915e43c14c1469be217450ac9bd9aab5887c517f2acafa6c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

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

## syn-hold-0086 — 지속 얼굴 따가움과 제품 버전 확인 거절

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `1c6214b208ffa21d01236d6d48da01ade066fcaeaab99f43f0de0834e1931d81`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴의 따가움과 불편감이 지속되며 사용 제품의 버전 답변은 원하지 않습니다.",
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

## syn-hold-0087 — 얼굴 세정 뒤 지속 불편과 통증

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `cee2cbe58a9b801bca6524302d05e54a94f3c56edd6fb738992df7bc9a21daf5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 세정 뒤 불편과 통증이 지속되며 원인은 확인되지 않았습니다.",
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

## syn-hold-0088 — 세정 기기 사용 뒤 지속 얼굴 통증

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `53118eac9d4f882772cba0e29f153fb7ed4a105fdf23c019b3d3222e34f51593`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 기기를 사용한 뒤 불편감과 통증이 지속되지만 원인은 확인되지 않았습니다.",
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
기기 사용 뒤 얼굴의 불편감과 통증이 지속되지만 원인은 확인되지 않았어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0089 — 손 씻기 뒤 지속 불편과 친구 경험

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `624f43b9865ff2264c557ca5e04f940b2f9db10651985c9938f1d222b47985c3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "손의 불편감이 지속되지만 같은 비누를 쓰는 친구는 불편이 없습니다.",
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
손의 불편감이 지속되고 있어요. 친구의 경험으로 본인 상태를 판단할 수 없어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0090 — 세안 중단 이후에도 지속되는 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `fd784fb18f51b3cb6dde4b79abe6d736ec54c30fb940f4f4386ae801596b43e6`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "세안을 중단한 뒤에도 얼굴 불편감이 계속되며 제품의 원인 여부는 모릅니다.",
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
세안을 중단한 뒤에도 얼굴 불편감이 지속돼요. 원인은 확인되지 않았어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0091 — 두 제품을 함께 쓴 뒤 지속 통증

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `1e1acc795b64cba79dad5174e9c12972eb4293054f660a3c75c736e2bc02dbcb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재의 불편 또는 통증을 확인해 개별 루틴 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "두 제품을 함께 사용한 뒤 얼굴 통증과 불편감이 계속되며 어느 제품이 원인인지는 모릅니다.",
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
두 제품 사용 뒤 얼굴 통증과 불편감이 지속되지만 원인은 확인되지 않았어요. 개별 루틴과 제품 안내는 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
현재 불편감과 경과에 관해 의료 전문가의 확인을 받아 주세요. 원인을 단정하거나 대체 루틴을 제시하지 않아요.

## syn-hold-0092 — 면도 부위의 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `f5732a625874297a32146dad74d9d12e08e60884c1f7eaa33330f46a1fbd3c50`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

면도 부위의 지속 불편이 보고되어 개별 권고를 보류해요.

### 입력

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

## syn-hold-0093 — 손에 지속되는 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `9ea5b1de8cc2e949caa4ac1a3dbf3a4f3065aaca269ed7325a62cfdfaa923ce1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손의 지속 불편이 보고되어 개별 권고를 보류해요.

### 입력

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

## syn-hold-0094 — 보습 사용 시 지속 통증

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `118abffc263ed60d722b5bc09f7918048239129e57aa58aa9e330663f6cbb8c6`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편과 통증이 보고되어 개별 권고를 보류해요.

### 입력

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

## syn-hold-0095 — 손 보습제의 새 냄새 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `7563749d2340caa07ef443cad44dc0dce2fa2516877700aa32073c4eb72be42a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 냄새 변화가 확인된 손 보습제 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0096 — 얼굴 보습제의 새 층 분리

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `5d87ef5a7d8cc0c0672eb5b93c11a8507e5a362cde7561b071451224dff4f8ac`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 층 분리가 확인된 얼굴 보습제 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0097 — 면도 후 제품의 새 색 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `83bda63ef8f4d68e4cc46218c12b1320d3e14cec603771557361c6395d171f42`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 색 변화가 확인된 면도 후 제품 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0098 — 보습 제품의 새로운 누출

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `f618ec32aff94b477c4d740bcbdeaf5a2ec36c903364de84fd9f3e85d0c5d496`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습 제품의 새로운 누출이 보고되어 해당 제품 사용을 보류해요.

### 입력

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

## syn-hold-0099 — 수령 뒤 처음 확인한 새 냄새와 누출

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `91aaa6f275efdec00b2706496e5bf65167453d80d0116fa84c778d93a67424d1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

품질 이상 의심 제품의 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0100 — 기한 표시가 읽히는 용기의 새 변색

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `309d52601db7a4af9ed28c2ca20865a2c80ce76fabf8d84003215ce6de41e54f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 색 변화가 있는 제품의 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0101 — 흔들어 쓰는 선크림에서 새 악취

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `caf3597fe534d2bf8af07a92d7b9edb1c8c6f481f36c6c5178f4df98b01d2bad`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

정상 이층과 별개인 새 냄새 변화로 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0102 — 같은 이름 두 제품 중 한쪽의 새 입자와 색 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `375697ef4254bdb87ab97b951786f86077caddcec795ae7b245a2f296fb12615`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

변화가 확인된 가의 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0103 — 보관 조건 확인 후 발생한 새 질감 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `fe630825d007585ecfb726353602d27912aa7350aa859164646bb7882f456772`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 변화가 확인돼 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0104 — 외관 점검 이후 생긴 새 냄새

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `b42d1c9ee162492560440114e334fa84ae57622c2eb0844ddd9608eec38a6174`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 점검과 별개로 새 변화가 확인돼 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0105 — 개봉 전 용기 팽창과 새 누출

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `7c1fb420772a24d2ed78e3b640251eaddb07320edaf7f6930d56fdce5ec68166`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 누출을 품질 이상 의심으로 보고 사용과 개별 안내를 보류해요.

### 입력

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

## syn-hold-0106 — 제조번호 확인 후 별도로 발견한 냄새 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `8677491a3b2cb1be2cc9c7019c7dea864c8ecbad1ff432be715216009547e981`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

회수 조회와 별개로 확인된 새 냄새 때문에 사용과 개별 안내를 보류해요.

### 입력

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

## syn-sol-0274 — 손의 거친 수건과 얼굴의 가벼운 건조

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9d5aebdbbbe4fbea449825cdec20b29dc52aa2f9fc59743fb4a3049ba9d080fd`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴 건조는 가볍게 하지만 세안 도구와 마찰은 미상이므로 전체 세안 방법은 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "손은 수건으로 문지르지만 얼굴은 문지르지 않고 가볍게 눌러 말립니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
얼굴 건조는 가볍게 하지만 세안 도구와 마찰은 미상이므로 전체 세안 방법은 판정하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴 마찰의 강도는 추정하지 않아요.

## syn-sol-0278 — 내수성 제품의 사용 계획과 미사용

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `dd5d8258eb715d724aa55c983c4b0621b2c73630fa937ff485cd4d35df44c730`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

계획을 실제 사용이나 반복 행동으로 취급하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "내수성 제품은 다음 주 사용 계획일 뿐 오늘 사용하지 않았고 오늘 제거 행동은 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "planned_only": true,
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
계획을 실제 사용이나 반복 행동으로 취급하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0279 — 다른 사람의 반복과 본인 행동 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1a97285e880956842ae274ff7ff5456d55237bb5c306cefedfe0f9e41fc9b804`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 사람의 행동으로 본인의 판정을 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "동거인이 내수성 표시만 보고 반복 세안하지만 본인의 제거 행동은 알 수 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
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
다른 사람의 행동으로 본인의 판정을 만들지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0280 — 얼굴이 아닌 팔에만 내수성 제품 사용

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9b07b12039bc39031a887d09ddfe7425882d3880922c4c8102f2a395dc654438`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

팔의 사용을 얼굴의 반복 세안으로 옮겨 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "내수성 제품을 팔에만 사용했고 얼굴 제거 행동은 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_site": "arms",
        "face_removal": "unknown"
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
팔의 사용을 얼굴의 반복 세안으로 옮겨 판단하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0281 — 확인되지 않은 제품 버전의 제거 표시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `14a33b3a421fe83e6fa819eec24cfb11c566d7471112ac4e3b9d58811e8ffa57`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

버전 일치가 확인되기 전에는 해당 제거 표시를 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "표시 사진의 제품 버전과 현재 사용하는 제품의 일치 여부가 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "label_version_match": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "버전 일치가 확인되기 전에는 해당 제거 표시를 적용하지 않아요."
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
버전 일치가 확인되기 전에는 해당 제거 표시를 적용하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0282 — 사용한 제품 라벨의 제거 조건 일부 누락

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a375502646765c5847d27f58160a31e77fc5716a07d94bba0bff46ff79455fc0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보이지 않는 제거 조건을 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "합성 제품의 제거 안내 일부가 가려져 필요한 세정 방법을 읽을 수 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "removal_instruction": "partially_obscured"
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
보이지 않는 제거 조건을 추정하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0283 — 세안 도구 이름과 제거 조건 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `923fdf92fec4068825c32161cea96ffdb830dbcbbc276859ab18db3f9ff1775c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

폼 사용만으로 표시 일치나 불일치를 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "폼을 사용한 것은 확인됐지만 제품의 제거 표시와 반복 이유는 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
폼 사용만으로 표시 일치나 불일치를 확정하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0284 — 첫 세정과 재세정의 시점 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `6b987b15279079efddce629cf3bdc492a9bfecf5d0c8d52b20ad2e46edb376b0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

세정 횟수와 한 번의 단계 수를 구분해 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "세정제 두 번 사용 사실은 있으나 같은 세안의 두 단계인지 다른 시간인지 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
세정 횟수와 한 번의 단계 수를 구분해 확인해요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0287 — 얼굴에 닿지 않은 도구

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `484027886fdcdaf6851a95743e25c71fa4d5711d0a49c907b9195c9994df8b58`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손에만 쓴 기기로 얼굴 세안 방법을 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "소유한 기기를 손에만 사용하며 얼굴의 실제 세안 방법은 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
손에만 쓴 기기로 얼굴 세안 방법을 추정하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0288 — 사용 제품 내수성 미상과 다른 제품 표시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `0c264371d8cd49c64e4ca78ee68934cfd89cabc1a80b5eb7db661687e819016d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 제품의 내수성 표시를 사용 제품에 이전하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "가방 속 다른 제품에는 내수성 표시가 있지만 실제 사용 제품의 표시는 알 수 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_product_water_resistance": "unknown",
        "other_product_labeled": true
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
다른 제품의 내수성 표시를 사용 제품에 이전하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0289 — 반복 세안 중단 계획과 실제 행동

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `7475024aa95f76b51be923bbe2baf3829714c6ba5c1e7e6dd425cf1bfac03dd6`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

계획만으로 행동 변경을 확인하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "반복 세안을 멈추기로 계획했지만 오늘 실제 행동과 기존 반복 이유는 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "plan": "반복 중단",
        "actual_behavior": "unknown",
        "reason": "unknown"
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
계획만으로 행동 변경을 확인하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0290 — 손 위생 행사와 얼굴 세안 기록 충돌

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `77426fcb28cd79530541dd972b6c36b9dc1b938c170a1b98d65bfc3ca4e4d1e8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

서로 충돌하는 기록으로 세안 횟수 차이를 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "한 기록은 얼굴 세안 한 번이고 다른 기록은 두 번이라고 하며 어느 쪽이 맞는지 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "face_wash_records": "conflict"
      },
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
서로 충돌하는 기록으로 세안 횟수 차이를 확정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0292 — 땀을 흘린 시간과 세안 횟수 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `945e8f0d3630b38517d71b3719369ade0dab1a2f25742f9a6e4e998a9488b226`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

땀이 있었다는 사실만으로 세정 횟수를 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "운동 중 땀을 흘렸지만 얼굴 세정의 실제 횟수와 단계는 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
땀이 있었다는 사실만으로 세정 횟수를 만들지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0293 — 서로 충돌하는 제거 표시 사본

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1193ffa622bbd979ed2beeb493e7722482f7c103757125cf9628ded54e78ddd2`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

상충하는 표시 중 하나를 임의로 현재 제품의 지시로 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "동일 제품이라고 적힌 두 표시 사본의 제거 방법이 다르고 현재 버전은 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "removal_instructions": "conflict",
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
상충하는 표시 중 하나를 임의로 현재 제품의 지시로 정하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0294 — 얼굴과 목의 보습 시점 분리

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `07fdd35b03e9fcdc6dc609d18adbeb160dd3c8b98686ee8711db1297685af530`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

피부 물기의 관찰 부위는 명시되지 않았고 목의 물기는 미상이라 부위별 시점을 판정하지 않아요.

### 입력

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

## syn-sol-0295 — 건조 피부 지시가 다른 두 제품

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `97e508f7f09eecca3acff05f0409ea798c9dc3311f1f606aee585defb8ddef1e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

건조한 피부에 바르라는 제품 A의 지시를 우선 검토하며 B의 지시는 미상이에요.

### 입력

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

## syn-sol-0296 — 손 씻기 뒤 실제 보습의 주체

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `0e2da2fdba2adb8c772cdb1bbad2ee395f04d2b0ed1c60b30002d8ca7700cfcc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동료의 보습 기록으로 본인의 손 보습 여부를 판단하지 않아요.

### 입력

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

## syn-sol-0298 — 보습제 사용과 목의 건조 재발

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `44e2f0be1e73a45ce8fcbc53b71b38ee843dee74fc87033b3f4d544e19432c1b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

목에 보습제를 실제 사용했는지 미상이라 그 부위의 보습 방법을 판정하지 않아요.

### 입력

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

## syn-sol-0299 — 필요한 손 씻기와 작업 뒤 보습 계획

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `43a2c52124e937b06810bd0b98dfd1f193bab9453883e72ae56d0eb8a4403f8c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

작업 뒤 보습 계획은 실제 사용의 확인이 아니며 필요한 손 위생은 유지해요.

### 입력

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

## syn-sol-0300 — 면도 후 목과 얼굴의 반응 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9fa7e3fb7f3fbf974df0157c358a4be0ff39e5fa0df3ee59b56a324279f39817`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴의 편안함으로 목의 제품 반응을 대신하지 않아요.

### 입력

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

## syn-sol-0301 — 손 보습제 무향료 표시와 향성 오일 정보

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `8314ecf569249448ddd4fd1d5907ed932f74dfb1e894d9dbdaa614f369c5ab49`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

무향료 표시는 확인됐지만 향성 에센셜오일과 개인 반응은 미상이에요.

### 입력

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

## syn-sol-0302 — 면도 후 다른 사람의 반응

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a44d551cfda123e768e36b20bd3123ee5a6d64d1f728cbfd7ba256c004c58f40`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 따가움은 본인의 반응이 아니며 본인의 반응은 미상이에요.

### 입력

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

## syn-sol-0303 — 얼굴은 편안하고 손은 확인 거절

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ab123041ca7b181f9c10c01f307e36337fcc77b3ae6130c767aa4833d460c76f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴의 편안함을 손의 보습 충족으로 대체하지 않아요.

### 입력

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

## syn-sol-0304 — 보습 목표와 사용 경험이 다른 부위

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `3d9c8687f8a2cd5f59815e378159fff4cd03ba4e44102e31cd158e4a7e81a3ee`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴의 보습 충족 경험으로 손의 사용이나 충족을 추정하지 않아요.

### 입력

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

## syn-sol-0305 — 면도 후 제품 지시와 사용 기록의 연결

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `909bba4a302a88501f83b2d26f83dcafee38d8058eefc04122b2064b0659d235`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

면도 후 사용 표시가 있는 제품과 실제 사용한 제품이 같은지 미상이에요.

### 입력

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

## syn-sol-0306 — 면도 후 불편의 다른 주체

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d82956bc30648dfc07b4eacb347e13c9ec499f8e770b07f1c7be3803c7cfac11`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 편안한 경험은 본인의 면도 후 사용과 반응을 알려주지 않아요.

### 입력

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

## syn-sol-0307 — 반응 없는 부위와 반응 미상 부위

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c30e1c58a3416e3306243bdf767fe6d8154fdca55ad069337a619af65ff37743`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴에 불편이 없다는 보고는 목의 반응이나 변경 이력을 확인해 주지 않아요.

### 입력

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

## syn-sol-0308 — 제품 변경과 계절 변화의 시점 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `8ba068a62e7e04fea0933c6ee7b28a5639102ba8a1b05b5cf27e5729931baf73`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제품과 계절의 변화가 보고됐지만 사용감 변화와의 시간 관계는 미상이에요.

### 입력

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

## syn-sol-0309 — 보습 단계 추가 전 실제 사용 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `84a6c8062162ee4b4f90629c07927df75db260e6863eb7c7845b253b0a3dfd37`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보유와 실제 사용은 다르며 현재 보습 충족은 미상이에요.

### 입력

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

## syn-sol-0310 — 보습제 후 촉촉함과 나중의 느낌 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d1199c3aa4f52319f98422084b05024da6e76fabba5100f87f6bf305a2acc6fb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

직후의 편안함은 이후의 건조감이나 반응을 대신하지 않아요.

### 입력

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

## syn-sol-0311 — 보습 시점과 처방 계획의 적용 범위 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `960236b5a0f6a17405560227248883cecf1dddd70bfa6b9e19bdb61cbb01b79d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

진료 계획의 보습제 적용 범위와 사용 시 피부 물기는 미상이에요.

### 입력

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

## syn-sol-0312 — 향료 목록과 사용 경험이 서로 다른 손 제품

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `2a6e356bbe6755c6274079a154fc4141aa8defa931520c08a566107470797854`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

A의 표시와 B의 편안한 경험을 한 제품에 합치지 않아요.

### 입력

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

## syn-sol-0313 — 면도 뒤 보습을 했지만 반응 시점 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `46941329c3ae66b3fb4760c5dd2374d02d265e00083efc39a03e4dcd16339253`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

불편이 보고됐지만 제품 사용과의 시간 관계는 미상이에요.

### 입력

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

## syn-sol-0314 — 세정 후 피부 물기와 실제 제품 사용 분리

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9a8ef1e0b0f4f96d4c39224d917500849e10e20296fc2bec1b1e6df23e1c4ae1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

피부가 촉촉하다는 관찰만으로 보습제 사용이나 관찰 시점을 확인할 수 없어요.

### 입력

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

## syn-sol-0315 — 세안 직후 제품을 썼으나 물기 확인 거절

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `62710673774d19a19810398284449018842710f5447ae5ab5ea44381713beeaa`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

세정 후 보습제 사용은 확인됐지만 피부 물기 정보는 제공되지 않았어요.

### 입력

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

## syn-sol-0316 — 손 진단을 이유로 보습 전체 중단

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `dbbf8ff3f293506389abd6568e0aef21e690ade3a8a341ab60901023761447c9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손 습진 진단을 이유로 모든 보습을 중단했으며 개별 진료 지시는 미상이에요.

### 입력

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

## syn-sol-0317 — 건조에도 고정 감량을 계획만 한 경우

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `6a54896c98adca5348c100b75be548d8c3f37491eda49bd5a41f05618d27de82`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

건조와 감량 계획이 보고됐지만 실제 감량은 미상이에요.

### 입력

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

## syn-sol-0318 — 다른 제품의 성분과 보습감 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d215a7210d766820053090eca33042ef46fc8c9d87a00071db1fcfd21412616e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

B의 편안함으로 A의 실제 보습 충족을 판단하지 않아요.

### 입력

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

## syn-sol-0319 — 손 위생 뒤 피부 상태와 제품 반응 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a9ba1cd633de031df01661e101a17d005106646c0b5e69a25d46eb96a6f98c5c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손 건조 보고와 특정 보습제 반응은 별도이며 반응은 미상이에요.

### 입력

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

## syn-sol-0320 — 두 야외 후보의 표시 일부만 확인

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `50898504ef793e203e5e94fa8fccd06b2f3f9c15181d3d462ba6b2736ff3d08d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 내수성 및 나의 기본 성능은 미상으로 남겨요.

### 입력

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

## syn-sol-0321 — 현재 후보가 아닌 예전 후보의 성능표

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `277bc01274f46b8fd20e4f0c4ce126f979d788e3cd0f6d8538f8616393402506`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 버전의 표시를 현재 후보에 옮기지 않고 현재 표시를 확인해요.

### 입력

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

## syn-sol-0330 — 두 개 중 개봉일이 확인된 선크림

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `5eb61212184ca7ae6965239f636800fbe299ae4197c75aa3e9f160e869b5217d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 개봉일만으로 두 제품의 기간 적합성을 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "두 선크림 가운데 가의 개봉일만 확인했어요. 개봉 후 사용기간 표시는 가와 나 모두 읽지 못했어요.",
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
각 용기의 개봉 후 안내와 나의 개봉일을 확인해요. [kb:B-S02@0.6.1]

### 근거 및 이유
가의 개봉일만으로 두 제품의 기간 적합성을 정하지 않아요. [kb:B-S02@0.6.1]

### 확인이 필요한 한계
두 제품의 개봉 후 안내와 나의 개봉일은 미상이에요.

## syn-sol-0331 — 여행 파우치의 현재 보관과 과거 열 노출

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `dc855ed5f0bfc0f8bf6551b68c83e5cbe3e1d861858eb6c2824679480415abcc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 보관과 별개로 과거 열 노출 여부는 미상으로 남겨요.

### 입력

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

## syn-sol-0332 — 두 용기 중 타인 용기의 뜨거운 차 보관

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `11794559ac216a194e320690f49e5622f7ccb87595e9d852f3587e7c2876de3c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족 용기의 이력을 본인 용기에 그대로 적용하지 않아요.

### 입력

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

## syn-sol-0334 — 다른 나라 용기의 사용기한 표시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `53111306901f8604e81bef39e103dc4bfb06014dce4d4d6fd61e2a6552f7c1ec`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 국가 용기의 날짜를 현재 보유품에 복사하지 않아요.

### 입력

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

## syn-sol-0335 — 리필 지침의 대상과 실제 용기 연결 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d105f9b5e9e405dbb641ac396d6b90a9e54684802fc6e02725aa60d7907e93d0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 용기에 해당하는 리필 지침인지 먼저 확인해요.

### 입력

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

## syn-sol-0337 — 서로 다른 용기의 개봉 이력

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `1d60ef7c535a6f2599832effa2420163d891c04a617349e6c445b571f85906cf`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 개봉 이력을 나에 적용하지 않아요.

### 입력

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

## syn-sol-0339 — 소량 도포 여부를 다른 제품 기록으로 추정

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `789b1bb787539a59ddf77a0d3fdf98f7e343acc9a6e6c963c956c2cea7dc6ce0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제 기록만으로 선크림을 적게 발랐다고 판정하지 않아요.

### 입력

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

## syn-sol-0340 — 햇빛 차단 의복의 적용 부위 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `313d1a11e0611a71126d864ab8dbf33d28ad9ac114023b04ec33222a4e9efc19`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기록된 긴소매 외 보완 수단의 적합성은 미상으로 남겨요.

### 입력

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

## syn-sol-0341 — 재도포 알림과 실제 행동을 구분

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `7e70e131ecfa856dfcedb4694c9ec9421dc0293b11f3309933ad227e6241d2bc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

알림 기록을 실제 재도포로 간주하지 않아요.

### 입력

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

## syn-sol-0342 — 뚜껑을 열어 둔 제품과 별도 선크림

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `aab9fb16258725cb8f181d345b75fed5f9a8f1821603b9407dbc20a414fe396b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제의 보관 이력을 선크림에 옮기지 않아요.

### 입력

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

## syn-sol-0343 — 동일명 선크림 두 버전의 분무 여부

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `e499777dbc334a985aee9d273d4e23cb8a0ddc1b475ed0a1d6a0ee234cdf7fdc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 용기의 형태를 확인하기 전 예전 버전의 사용법을 적용하지 않아요.

### 입력

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

## syn-sol-0344 — 사용기한과 다른 용기의 정상 이층 안내

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `509194900e665569883413aefaa134615126b57a65f940499ebde753a75ac1a9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

나의 제형 안내를 가에 적용하지 않고 가의 기한과 안내를 확인해요.

### 입력

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

## syn-sol-0268 — 손 씻기와 얼굴 반복을 별도 계산

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `3bfa96f68b32f710e439fb4a2e28093de6fb18d642d85ed58128eee4043fb802`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

필요한 손 위생은 유지하면서 단순 잔여감 해소를 위한 얼굴 반복을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 세안은 단순한 잔여감 해소를 위해 연속 두 차례 반복하고 업무상 손 씻기는 따로 합니다. 추가 오염이나 화장 제거 목적은 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_repeat": true,
        "reason": "단순한 잔여감 해소",
        "additional_removal_purpose": false
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
필요한 손 위생은 유지하면서 단순 잔여감 해소를 위한 얼굴 반복을 검토해요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0269 — 손 세정 횟수만 확인

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `016cb1640424fb8765d70e71dcbb4c3fa2728c2c71bf227ab28f123e4fed39c1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손 세정 횟수만으로 얼굴 세안의 차이를 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "업무상 손을 여러 번 씻지만 얼굴 세안 횟수와 목적은 확인되지 않았습니다.",
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
손 세정 횟수만으로 얼굴 세안의 차이를 판정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0270 — 흙 노출 후 별도 얼굴 세정

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `eb64ebd1688962d387d7b07ca97ed7d40b20b5bd2be2fd08ee042eda9e4a8359`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

흙 제거라는 별도 목적을 고려하며 횟수만으로 차이를 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "실외 작업 중 얼굴에 흙이 묻어 평소 세안 외에 씻었습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "extra_wash_reason": "얼굴의 흙",
        "automatic_repeat": false
      },
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
흙 제거라는 별도 목적을 고려하며 횟수만으로 차이를 만들지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0271 — 땀과 추가 단계의 연결 미상

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `b1829171c5c7a7da0777288f5c4cb8f859f686054788753e5dd546512ebf4816`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

운동 후 세안과 추가 단계의 이유를 구분해 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "운동 후 땀은 확인했지만 같은 세안에서 두 번째 단계의 목적은 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "extra_step_reason": "unknown"
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
운동 후 세안과 추가 단계의 이유를 구분해 확인해요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0272 — 기기 보유와 얼굴 사용 구분

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `0d594eb9d7152d4130a1b681ef11534e29b62569b0af42e9051584c1a2090d2b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기기 보유만으로 얼굴 마찰을 단정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "세정 기기를 보유하지만 얼굴 사용 여부와 압력은 확인되지 않았습니다.",
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
기기 보유만으로 얼굴 마찰을 단정하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0273 — 기기는 손에만 쓰고 얼굴은 강한 수건 마찰

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `d47effb4339f4d8535fb11278f2c4b462b27b7497e123f957964e3d91164d84e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손의 기기 사용과 별개로 얼굴의 강한 수건 마찰을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "손에 세정 기기를 쓰며 얼굴은 세안 후 수건으로 강하게 문지릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
손의 기기 사용과 별개로 얼굴의 강한 수건 마찰을 검토해요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0275 — 기기 미사용과 수건 압력 미상

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `189eb19fff4d78444afcb3690e23d74a5a57b587569161a7d2a451e2d6cc607d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기기를 쓰지 않는 사실만으로 수건 마찰까지 확인된 것은 아니에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 기기는 쓰지 않지만 수건으로 말릴 때의 압력은 기억하지 못합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
기기를 쓰지 않는 사실만으로 수건 마찰까지 확인된 것은 아니에요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개별 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 얼굴의 행동이나 사용 목적은 추정하지 않아요.

## syn-sol-0276 — 서로 다른 두 제품의 제거 표시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `a9b803737f12f0efc1fffe60ea6b4cf0341cc8b023fba47f3de04825d7161892`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 제품의 표시를 사용 제품에 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "사용한 내수성 제품의 제거 표시는 미상이고 다른 제품의 제거 표시만 확인했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_product_removal": "unknown",
        "other_product_removal": "confirmed"
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
다른 제품의 표시를 사용 제품에 적용하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.

## syn-sol-0277 — 내수성 표시만을 이유로 연속 세 단계

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `c0754583c6adc18ac77985e1728c4d511cbea75d527f2869021cec4091eb9ea1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

내수성 표시만을 근거로 고정한 반복 단계를 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "실제 사용한 제품의 내수성 표시만을 이유로 매번 얼굴을 세 단계로 씻습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": true
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
내수성 표시만을 근거로 고정한 반복 단계를 검토해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합을 비교한 소규모 영상 연구는 모든 내수성 제품에 일률적인 제거 방법을 확정하지 않아요. [ref:S08]

### 확인이 필요한 한계
실제 사용 제품의 표시와 버전이 확인되지 않은 부분은 미상으로 남아요.
