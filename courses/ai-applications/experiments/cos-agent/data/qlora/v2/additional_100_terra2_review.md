# 추가 개발 후보 100턴

기존 248턴을 변경하지 않고 추가한 안내 76턴·보류 24턴입니다. 합계는 348턴입니다.
`development_preview`, `production_enabled=false`이며 실제 사용자 자료나 임상 정답이 아닙니다.
작성 담당과 별도 문맥의 Codex 감사 담당을 분리합니다. 동일 GPT 계열의 감사는 다른 모델 계열의 공식 검수나 사람 승인을 대체하지 않습니다.
사람 검수는 미검수이며, 현재 감사 판정은 `reviews/additional_100_terra2_codex_independent.*`에서 내용 해시와 함께 확인합니다.
합성 방어 청크는 실제 문헌 인용문이 아니며 감사용 출처 분류를 유지합니다. KB 판정 근거는 비교 명세를 대조한 작성 기록이지 엔진 실행 결과가 아닙니다.

## 사례 목록

| ID | 유형 | 사례 | 분할 |
|---|---|---|---|
| syn-sol-0191 | normal_guidance | 뜨거운 물 체감 | train |
| syn-sol-0192 | normal_guidance | 의도적인 세정제 방치 | train |
| syn-sol-0193 | normal_guidance | 씻어내는 지시와 헹굼 생략 | train |
| syn-sol-0198 | normal_guidance | 수건의 강한 마찰 | train |
| syn-sol-0199 | normal_guidance | 화장 제거 목적의 두 단계 | train |
| syn-sol-0200 | normal_guidance | 현재 보습과 편안함 | val_internal |
| syn-sol-0201 | normal_guidance | 부드러운 손가락 세정 | train |
| syn-sol-0202 | normal_guidance | 헹굼 불필요 표시 | train |
| syn-sol-0219 | normal_guidance | 눈가 제한과 귀 도포 기록 | train |
| syn-sol-0227 | normal_guidance | 내수성 없음이 명시된 수영용 후보 | train |
| syn-sol-0230 | normal_guidance | 발한과 재도포 기록의 순서 미상 | val_internal |
| syn-sol-0233 | normal_guidance | 옷으로 가린 목과 선제품 도포 기록 | train |
| syn-hold-0059 | hold | 변화한 제품에서 입자를 걸러 사용하려는 요청 | train |
| syn-hold-0060 | hold | 색 또는 냄새 변화와 기한 | train |
| syn-hold-0061 | hold | 지속 불편과 통증 미상 | train |
| syn-hold-0062 | hold | 지속 불편과 진료 대체 요청 | train |
| syn-hold-0063 | hold | 피부 관통 장치 사용 계획 | train |
| syn-hold-0064 | hold | 의료진 기기 회피 지시 | train |
| syn-hold-0065 | hold | 변화한 제품의 사용 지속 요청 | train |
| syn-hold-0066 | hold | 지속 불편과 진료 계획 미상 | train |
| syn-hold-0067 | hold | 한 용기의 색 또는 냄새 변화 | val_internal |
| syn-hold-0068 | hold | 기한 전 표시와 층 분리 | train |
| syn-hold-0069 | hold | 이전 판매자 답변과 이후 새 냄새 | train |
| syn-hold-0070 | hold | 품질 의심 용기의 사용 종료와 타인에게 전달 문의 | train |
| syn-hold-0071 | hold | 다른 용기의 정상 흔들림 안내 | train |
| syn-hold-0072 | hold | 기존 정상 냄새와 새 변화 | train |
| syn-hold-0073 | hold | 지속 불편과 타인의 양호한 경험 | train |
| syn-hold-0074 | hold | 회수 공지의 제품과 제조번호 대조 미완료 | train |
| syn-hold-0075 | hold | 회수 공지의 기간과 구매일 미상 | val_internal |
| syn-hold-0076 | hold | 기기 부속품과 허용 제품의 관계 미상 | train |
| syn-hold-0077 | hold | 용기 손상과 내용물 상태 미상 | train |
| syn-hold-0078 | hold | 얼굴 지시와 목 부위의 제품 사용 범위 | train |
| syn-hold-0079 | hold | 반응이 보고된 제품의 다른 기기 재사용 계획 | train |
| syn-hold-0080 | hold | 같은 이름의 두 제품 중 하나에 대한 개별 중지 지시 | train |
| syn-hold-0081 | hold | 회피 원료와 성분표의 버전 불일치 | train |
| syn-hold-0083 | hold | 다른 용기의 정상 분리와 새 냄새 | train |
| syn-sol-0194 | unknown_or_version | 실제 보습과 세정 시간 관계 미상 | train |
| syn-sol-0195 | unknown_or_version | 찬물 체감 | train |
| syn-sol-0196 | unknown_or_version | 경과 시간과 접촉 행동 | train |
| syn-sol-0197 | unknown_or_version | 보습 사용과 시점 미상 | train |
| syn-sol-0203 | unknown_or_version | 보습제 보유와 사용 미상 | train |
| syn-sol-0204 | unknown_or_version | 두 단계의 목적 미확인 | train |
| syn-sol-0205 | unknown_or_version | 수건 사용과 마찰 미상 | val_internal |
| syn-sol-0206 | unknown_or_version | 보습 사용과 반응 미상 | train |
| syn-sol-0207 | unknown_or_version | 헹굼 수행과 지시 미상 | train |
| syn-sol-0208 | unknown_or_version | 물기 상태와 사용 미상 | train |
| syn-sol-0217 | unknown_or_version | 표시 용기와 실제 대상의 연결 미상 | train |
| syn-sol-0222 | unknown_or_version | 제거 지시와 사용 제품의 연결 | train |
| syn-sol-0223 | unknown_or_version | 잘린 표시 사진과 표시 부재 | train |
| syn-sol-0225 | unknown_or_version | 해당 제품의 구체적 제거 지시 | train |
| syn-sol-0229 | unknown_or_version | 판매 페이지와 용기의 수치 | train |
| syn-sol-0232 | unknown_or_version | 밀림 후 초기 사용과 재도포 기록 | train |
| syn-sol-0235 | unknown_or_version | 반복 세안의 이유 미상 | train |
| syn-sol-0236 | unknown_or_version | 수영 계획과 실제 접촉 | train |
| syn-sol-0237 | unknown_or_version | 기한과 개봉 후 기간 | train |
| syn-sol-0240 | unknown_or_version | 과거 버전 지침과 현재 행동 | train |
| syn-sol-0243 | unknown_or_version | 씻어내는 팩에 다른 제품의 밤 사용 지시 적용 | train |
| syn-sol-0244 | unknown_or_version | 다른 상자에서 나온 두 제형의 혼합 | train |
| syn-sol-0245 | unknown_or_version | 같은 용기의 교체된 펌프 헤드 | train |
| syn-sol-0246 | unknown_or_version | 면도 준비 기록의 방식 귀속 미상 | val_internal |
| syn-sol-0247 | unknown_or_version | 일반 주의 문구와 특정 원료 함유 | train |
| syn-sol-0248 | unknown_or_version | 서로 다른 시작 뒤 같은 날 재개 | train |
| syn-sol-0249 | unknown_or_version | 각질관리와 레티놀의 사용 부위 미상 | train |
| syn-sol-0250 | unknown_or_version | 복합 완제품 보유와 별도 관리 사용 | train |
| syn-sol-0251 | unknown_or_version | 처방과 화장품의 시간 관계 미상 | train |
| syn-sol-0252 | unknown_or_version | 성분표와 실제 관리 목적의 구별 | train |
| syn-sol-0253 | unknown_or_version | 의료진 지시의 적용 기간 미상 | val_internal |
| syn-sol-0254 | unknown_or_version | 이전 제형의 국소 확인과 새 제형 | train |
| syn-sol-0255 | unknown_or_version | 향 이름과 각질관리 성분의 혼동 | train |
| syn-sol-0256 | unknown_or_version | 가족의 처방 지시와 본인의 관리 | train |
| syn-sol-0257 | unknown_or_version | 동일 부위 각질관리 사용 기록의 충돌 | train |
| syn-sol-0258 | unknown_or_version | 처방의 중단 계획과 실제 사용 확인 | train |
| syn-sol-0259 | unknown_or_version | 다른 사람의 팩 사용기와 개인 경험 | train |
| syn-sol-0260 | unknown_or_version | 헤드 교체 계획과 현재 토출량 | val_internal |
| syn-sol-0261 | unknown_or_version | 처방명과 같은 이름의 제품 용도 | train |
| syn-sol-0262 | unknown_or_version | 팩 표시 시간과 실제 제거 시각 누락 | train |
| syn-sol-0263 | unknown_or_version | 면도 젤 사용 계획과 다른 면도 기록 | train |
| syn-sol-0264 | unknown_or_version | 같은 제품의 새 포장과 사용시간 표시 | train |
| syn-sol-0265 | unknown_or_version | 이전 성분표와 현재 사용 제품의 버전 | train |
| syn-sol-0266 | unknown_or_version | 제품 이름과 실제 사용 용도의 분리 | train |
| syn-sol-0267 | unknown_or_version | 수면팩의 사용 방식은 확인되고 빈도는 미상 | train |
| syn-sol-0209 | distractor_or_defense | 가족의 뜨거운 물과 본인의 미온수 | train |
| syn-sol-0210 | distractor_or_defense | 타인의 마찰과 본인의 손가락 | train |
| syn-sol-0211 | distractor_or_defense | 본인과 타인의 건조 | val_internal |
| syn-sol-0212 | distractor_or_defense | 미온수 사용 | train |
| syn-sol-0213 | distractor_or_defense | 건조한 피부까지 기다리는 보습 | train |
| syn-sol-0214 | distractor_or_defense | 장갑을 낀 손가락 사용과 마찰 정도 미상 | train |
| syn-sol-0215 | distractor_or_defense | 건조에도 무조건 보습 감량 | train |
| syn-sol-0216 | distractor_or_defense | 과거 체감과 현재 미상 | train |
| syn-sol-0218 | distractor_or_defense | 친구의 재도포와 본인 기록 | train |
| syn-sol-0220 | distractor_or_defense | 본인 활동 종료와 친구의 지속 노출 | train |
| syn-sol-0224 | distractor_or_defense | 수건 접촉과 본인 재도포 기록 | train |
| syn-sol-0226 | distractor_or_defense | 본인의 밀림과 동행인의 사용 감소 | train |
| syn-sol-0228 | distractor_or_defense | 이전 제품의 반복 눈시림 | train |
| syn-sol-0231 | distractor_or_defense | 보습제 누락과 선제품 기록 | train |
| syn-sol-0234 | distractor_or_defense | 다른 날 기록과 야외 계획 | train |
| syn-sol-0238 | distractor_or_defense | 다른 제품의 내수성 표시 | train |
| syn-sol-0239 | distractor_or_defense | 밀림과 별도 일정에 따른 사용 감소 | val_internal |
| syn-sol-0241 | distractor_or_defense | 친구 용기의 냄새 변화 | train |
| syn-sol-0242 | distractor_or_defense | 친구의 눈가 불편과 본인의 경험 | train |

## syn-sol-0191 — 뜨거운 물 체감

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `d47ad65f3d78f7b2b97ecffb2616bf59f742405b42931e9c1b1aa9dde6fd9245`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

뜨겁게 느껴지는 물 사용을 검토하되 정확한 온도는 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "perceived_hot": true,
        "numeric_temperature_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "뜨겁게 느껴지는 물 사용을 검토하되 정확한 온도는 추정하지 않아요."
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
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
뜨겁게 느껴지는 물 대신 뜨겁지 않은 미온수로 세안하는 방향을 살펴요. [kb:B-C01@0.6.1]

### 근거 및 이유
뜨거운 체감은 세안 수온을 검토할 근거예요. 정확한 온도 수치는 확인되지 않았어요.

### 확인이 필요한 한계
별도 의료진 지시가 있다면 함께 확인해요.

## syn-sol-0192 — 의도적인 세정제 방치

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `abe3977c390dfae7a6c86fba34b470e896769b97aeb4bf5c80c9231a12f4e431`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

별도 지시 없이 일부러 오래 올려두는 방법을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "special_contact_time_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "intentionally_left_on_for_long_time": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "별도 지시 없이 일부러 오래 올려두는 방법을 검토해요."
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
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품에 별도 접촉시간 지시가 없다면 일부러 오래 올려두는 행동을 줄여요. [kb:B-C03@0.6.1]

### 근거 및 이유
의도적 방치가 확인된 점을 제품 지시와 함께 살펴요.

### 확인이 필요한 한계
이 관찰만으로 손상이나 특정한 적정 초 수를 확정하지 않아요.

## syn-sol-0193 — 씻어내는 지시와 헹굼 생략

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `c6d861e0f46626c05216dcf5f47aac507d311a38f57e1fb9be1d03e451f6dbcc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

씻어내라는 제품 지시와 헹굼 생략을 비교해요.

### 입력

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
        "reason": "save_time"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "씻어내라는 제품 지시와 헹굼 생략을 비교해요."
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
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
씻어내라는 해당 제품 지시에 따라 헹굼을 생략하지 않는 방향을 살펴요. [kb:B-C06@0.6.1]

### 근거 및 이유
시간을 아끼려고 헹굼을 생략한 행동이 확인된 표시 지시와 달라요.

### 확인이 필요한 한계
다른 제품의 헹굼 지시까지 같다고 추정하지 않아요.

## syn-sol-0198 — 수건의 강한 마찰

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `12466b383d9a3e3b0c20e31eb3ce90630a1e9ed74d903985b6c97a76624646f6`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

도구 사용과 별개로 수건으로 강하게 비비는 행동을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "towel_rubbing_strong": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "도구 사용과 별개로 수건으로 강하게 비비는 행동을 검토해요."
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
수건으로 강하게 비비기보다 물기를 가볍게 눌러 닦는 방향을 살펴요. [kb:B-C02@0.6.1]

### 근거 및 이유
확인된 강한 수건 마찰을 세안 도구 사용 여부와 구분해요.

### 확인이 필요한 한계
마찰 관찰만으로 피부 손상이나 원인을 단정하지 않아요.

## syn-sol-0199 — 화장 제거 목적의 두 단계

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `e30f8dd31373b865dd689cc193980874ca6abc0b52a540fe947bdc1b7e142e17`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

두 단계의 추가 목적이 화장 제거로 확인돼요.

### 입력

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
        "second_step_for_makeup_removal": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "aligned",
      "guidance": "두 단계의 추가 목적이 화장 제거로 확인돼요."
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
화장 제거라는 추가 목적이 확인됐으므로 두 단계라는 수만으로 불필요한 반복이라고 판단하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
단계의 목적과 제거 필요를 함께 살펴요.

### 확인이 필요한 한계
이 정보만으로 모든 상황에 두 단계가 필요하다고 일반화하지 않아요.

## syn-sol-0200 — 현재 보습과 편안함

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `28e06695afa7dbecfcf64f662ee9f8e8b5d8c635ed987a800e6cf214f00975e8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 실제 보습 사용과 편안한 상태가 확인돼요.

### 입력

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
      "guidance": "현재 실제 보습 사용과 편안한 상태가 확인돼요."
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
현재 보습 사용이 편안하고 건조가 없다는 보고는 이 카드의 부합 조건에 맞아요. [kb:B-M02@0.6.1]

### 근거 및 이유
실제 사용과 현재 경험을 확인했으므로 무조건 사용량을 바꿀 이유를 만들지 않아요.

### 확인이 필요한 한계
이 관찰은 미래의 불편이 없다는 보증이 아니에요.

## syn-sol-0201 — 부드러운 손가락 세정

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `63f9a8acc374b1babcb29975758cce6d778a139ce766635e566e07d727d05e37`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손가락으로 부드럽게 씻고 물기를 가볍게 닦는 관찰이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "gentle_fingertip_cleansing": true,
        "towel_patted_gently": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "손가락으로 부드럽게 씻고 물기를 가볍게 닦는 관찰이 확인돼요."
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
손가락으로 부드럽게 씻고 수건으로 가볍게 닦는 현재 방법은 이 카드에 부합해요. [kb:B-C02@0.6.1]

### 근거 및 이유
손가락 세정과 가벼운 닦기가 각각 확인됐어요.

### 확인이 필요한 한계
제품별 지시나 의료진 계획이 있다면 함께 확인해요.

## syn-sol-0202 — 헹굼 불필요 표시

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `52038a118839a7936b3d30b0820cc10f9b6ccaeeef6dbaf9a9f3e466e1ed1b8b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 물 헹굼 불필요 표시를 제품별 예외로 살펴요.

### 입력

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
        "no_water_rinse_required": true
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
      "guidance": "확인된 물 헹굼 불필요 표시를 제품별 예외로 살펴요."
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
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 물 헹굼 불필요 표시를 제품별 예외로 살펴요. [kb:B-C06@0.6.1]

### 근거 및 이유
확인된 관찰과 해당 카드의 조건을 구분해 살펴요.

### 확인이 필요한 한계
별도 제품 지시나 의료진 계획이 있다면 함께 확인해 주세요. 이 내용만으로 원인이나 효과를 확정하지 않아요.

## syn-sol-0219 — 눈가 제한과 귀 도포 기록

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `7d1db3c6bd67d9d82078599a404bceeb4b0e83072a4383698b2a49a8e313772c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

귀에 선제품을 바르지 않은 기록이 있지만 의도적인 누락인지는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "forehead",
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
        "eye_area": "avoid",
        "ears": "no_restriction_reported"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "귀에 선제품을 바르지 않은 기록이 있지만 의도적인 누락인지는 미상이에요."
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
귀에 선제품을 바르지 않은 기록은 있지만 의도적인 누락인지는 미상이에요. [kb:B-P02@0.6.1]

### 근거 및 이유
눈가 제한은 귀에 대한 지침과는 별개예요.

### 확인이 필요한 한계
귀의 도포 상황과 이유를 확인하기 전에는 의도적 누락으로 판단하지 않아요.

## syn-sol-0227 — 내수성 없음이 명시된 수영용 후보

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `f57546e52d7a5f69088ad4ecd0418fd5cc658fd4c6910029a79167a191da8771`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현행 합성 제품의 내수성 없음 표시가 수영 예정이라는 후보 조건과 달라요. 실제 측정 성능은 확인되지 않았어요.

### 입력

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
      "value": "broad_spectrum",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true,
        "label_statement": "not_water_resistant"
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
      "status": "difference",
      "guidance": "현행 합성 제품의 내수성 없음 표시가 수영 예정이라는 후보 조건과 달라요. 실제 측정 성능은 확인되지 않았어요."
    }
  ],
  "product_evidence": [
    {
      "product_id": "syn-terra2-b227",
      "version": "v1",
      "synthetic_product": true,
      "status": "verified",
      "label_guidance": "합성 현행 제품 표시: SPF 50, 광범위 보호, 내수성 없음이 명시돼 있어요.",
      "evidence_ref": "catalog:syn-terra2-b227@v1"
    }
  ],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "The American Academy of Dermatology recommends choosing broad-spectrum, water-resistant sunscreen with SPF 30 or higher.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "catalog:syn-terra2-b227@v1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현행 제품에는 내수성 없음이 명시돼 있어 수영 예정이라는 후보 조건과 달라요. [catalog:syn-terra2-b227@v1] [kb:B-P01@0.6.1]

### 근거 및 이유
미국 피부과학회는 광범위 보호, 내수성과 SPF 30 이상을 갖춘 제품을 권장해요. [ref:S16]

### 확인이 필요한 한계
이 표시와 조건의 차이만으로 실제 측정 성능이나 개인에게 생길 결과를 확정하지 않아요.

## syn-sol-0230 — 발한과 재도포 기록의 순서 미상

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `2d8edf24c376fb4e83e8203558ec15305533add3f8c8934580ef667828ec8cb7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

심한 발한과 재도포하지 않은 기록은 확인되지만 둘의 시간 순서는 미상이에요.

### 입력

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
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "outdoors": true,
        "heavy_sweating": true
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
      "status": "unknown",
      "guidance": "심한 발한과 재도포하지 않은 기록은 확인되지만 둘의 시간 순서는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "FDA guidance recommends reapplying sunscreen at least every two hours and more often after swimming or sweating.",
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
심한 발한과 재도포하지 않은 기록은 확인됐지만 두 사실의 시간 순서는 미상이에요. [kb:B-P03@0.6.1]

### 근거 및 이유
미국 식품의약국은 수영이나 땀을 흘린 뒤 더 자주 재도포하도록 안내해요. [ref:S05]

### 확인이 필요한 한계
물 접촉이 없었다는 사실로 발한 전후의 재도포 행동을 확정할 수 없어요.

## syn-sol-0233 — 옷으로 가린 목과 선제품 도포 기록

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `e8cbd9d01e98e72123eeaf4da2f8b2f9769e3e1364892e2128128f8de2678208`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

목은 옷으로 가려졌고 선제품은 이마에 바른 것으로 보고됐지만 목에 바르지 않은 이유는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
        "forehead"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.coverage_gaps": {
      "variable_id": "sun.coverage_gaps",
      "state": "known",
      "value": [
        "neck"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "neck_covered_by_clothing": true,
        "sunscreen_applied_forehead": true,
        "neck_sunscreen_omission_reason": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "목은 옷으로 가려졌고 선제품은 이마에 바른 것으로 보고됐지만 목에 바르지 않은 이유는 미상이에요."
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
목은 옷으로 가려졌고 선제품은 이마에 바른 것으로 보고됐지만 목에 바르지 않은 이유는 미상이에요. [kb:B-P02@0.6.1]

### 근거 및 이유
목의 도포 기록과 이마의 사용 기록은 각각의 부위에 연결해 살펴요.

### 확인이 필요한 한계
이 기록만으로 선제품 전체를 쓰지 않았거나 목을 의도적으로 누락했다고 판단하지 않아요.

## syn-hold-0059 — 변화한 제품에서 입자를 걸러 사용하려는 요청

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `4ce4ecd808ac805e10257b37f05c5d30622d93814844886c30a22a4fd6683b79`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

색 또는 냄새 변화와 입자가 보고돼 걸러서 계속 사용하기보다 해당 제품 사용과 개별 권고를 보류해요.

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
        "separation": false,
        "new_particles": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "wants_filter_particles_and_continue": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "색 또는 냄새 변화와 입자가 보고돼 걸러서 계속 사용하기보다 해당 제품 사용과 개별 권고를 보류해요."
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
색 또는 냄새 변화와 입자가 보고돼 해당 제품의 사용과 개별 권고를 보류해요. 입자를 걸러 계속 사용해도 품질이 확인되는 것은 아니에요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
제품 표시와 관찰된 변화를 제조·판매처에 확인해 주세요. 변화의 원인이나 현재 안전성은 확정하지 않아요.

## syn-hold-0060 — 색 또는 냄새 변화와 기한

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `1b22b8a151ee86701b60cc3a1f0ec81195229e60b3003336ac3c115c3d8a1abb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기한 이내라도 색 또는 냄새 변화가 보고돼 품질 확인 전 해당 제품 사용과 개별 권고를 보류해요.

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
      "guidance": "기한 이내라도 색 또는 냄새 변화가 보고돼 품질 확인 전 해당 제품 사용과 개별 권고를 보류해요."
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
사용기한 이내라도 색 또는 냄새 변화가 보고돼 해당 제품 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
제품 표시와 관찰된 변화를 제조·판매처에 확인해 주세요. 색과 냄새 중 어느 변화인지는 확인되지 않았어요.

## syn-hold-0061 — 지속 불편과 통증 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `bf7ce73f0d9e0af6ff6978ce09ae7d0b6ae2b0835200eaf300326871416b94d2`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편이 보고되어 개별 권고를 보류해요. 통증의 정도는 미상이에요.

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
      "guidance": "지속 불편이 보고되어 개별 권고를 보류해요. 통증의 정도는 미상이에요."
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
지속 불편이 보고되어 개별 권고를 보류해요. 통증의 정도는 미상이에요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
관련 상황과 확인된 지시를 전문가에게 전달하고 상담해 주세요. 원인이나 진단은 여기서 확정할 수 없어요.

## syn-hold-0062 — 지속 불편과 진료 대체 요청

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `b3c3735f3383fc85976f4ee4a8ef0b9e46244804c5c1ead42ba6904ee59937b3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편이 있고 통증 여부는 미상이에요. 안내받은 진료 확인을 제품 조정만으로 대체하려는 요청에 개별 권고를 보류해요.

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
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "follow_up_advised": true,
        "wants_product_adjustment_instead": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 있고 통증 여부는 미상이에요. 안내받은 진료 확인을 제품 조정만으로 대체하려는 요청에 개별 권고를 보류해요."
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
지속 불편이 있어 개별 권고를 보류해요. 통증 여부는 미상이에요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
안내받은 진료 확인을 제품 조정으로 대체하지 말고 관련 상황을 전문가에게 전달해 주세요. 원인은 확정할 수 없어요.

## syn-hold-0063 — 피부 관통 장치 사용 계획

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `ff1d0f48ec9b0fafc71863eea956c32cc7d41893f31d5659c1756d5cbbf97319`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

피부 관통 장치의 개인 시술 절차 안내를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "skin_penetrating": true,
        "planned": true,
        "already_used": false,
        "cleaning_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "피부 관통 장치의 개인 시술 절차 안내를 보류해요."
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
피부 관통 장치의 개인 시술 절차 안내를 보류해요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
관련 상황과 확인된 지시를 전문가에게 전달하고 상담해 주세요. 원인이나 진단은 여기서 확정할 수 없어요.

## syn-hold-0064 — 의료진 기기 회피 지시

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `d9dcfe791418abd69df23753b5ca6d5e9902e5cc495141a5631fb1c09afe5588`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

의료진의 기기 회피 지시가 있는 상태에서 개인 병용 설계를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "adjunct.device_use": {
      "variable_id": "adjunct.device_use",
      "state": "known",
      "value": {
        "plans_combination": true,
        "already_used": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "avoid_device": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "의료진의 기기 회피 지시가 있는 상태에서 개인 병용 설계를 보류해요."
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
의료진의 기기 회피 지시가 있는 상태에서 개인 병용 설계를 보류해요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
관련 상황과 확인된 지시를 전문가에게 전달하고 상담해 주세요. 원인이나 진단은 여기서 확정할 수 없어요.

## syn-hold-0065 — 변화한 제품의 사용 지속 요청

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `aff34f79a6a02ecbb04f3f767dc65110d77dc42cf596392b3c31db82c109e004`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

색 또는 냄새 변화가 보고된 제품의 사용과 개별 권고를 품질 확인 전 보류해요.

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
    "storage.handling": {
      "variable_id": "storage.handling",
      "state": "known",
      "value": {
        "wants_to_continue_despite_new_odor": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "색 또는 냄새 변화가 보고된 제품의 사용과 개별 권고를 품질 확인 전 보류해요."
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
색 또는 냄새 변화가 보고된 해당 제품은 품질 확인 전 사용과 개별 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
계속 사용하기 전 표시와 관찰된 변화를 제조·판매처에 확인해 주세요. 원인이나 안전성을 확정하지 않아요.

## syn-hold-0066 — 지속 불편과 진료 계획 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `330db9f8ce102fa10c6815f0aa8edddcbdee70f4446eb8a677fe8acf61e4be50`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편에 대한 개별 권고를 보류해요. 진료 계획과 따가움 여부는 미상이에요.

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
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "skin.stinging": {
      "variable_id": "skin.stinging",
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
      "guidance": "지속 불편에 대한 개별 권고를 보류해요. 진료 계획과 따가움 여부는 미상이에요."
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
지속 불편에 대한 개별 권고를 보류해요. 진료 계획과 따가움 여부는 미상이에요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
관련 상황과 확인된 지시를 전문가에게 전달하고 상담해 주세요. 원인이나 진단은 여기서 확정할 수 없어요.

## syn-hold-0067 — 한 용기의 색 또는 냄새 변화

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `cf7da15be409e56efc87736e9bb6bddf989782bad7a7560b95699d86a43ed911`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

용기 A에서 보고된 색 또는 냄새 변화에 대해 개별 재사용 권고를 보류하고 품질 확인을 진행해요.

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "affected_container": "A",
        "other_container": "B",
        "wants_to_reuse_A": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "container_B_normal_scent_confirmed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "용기 A에서 보고된 색 또는 냄새 변화에 대해 개별 재사용 권고를 보류하고 품질 확인을 진행해요."
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
용기 A의 색 또는 냄새 변화에 대한 개별 재사용 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
다른 용기의 정상 향과 구분해 용기 A의 상태를 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0068 — 기한 전 표시와 층 분리

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `67cf5cc962b82f9dd5eb273c724c067927afcb2e04dccc1e6a57b7c2d4eb9987`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기한 전 표시가 있어도 보고된 층 분리의 정상 여부가 확인되지 않아 개별 재사용 권고를 보류해요.

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
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "printed_date_not_passed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "normal_separation": "not_indicated_on_confirmed_label"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_reuse": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "기한 전 표시가 있어도 보고된 층 분리의 정상 여부가 확인되지 않아 개별 재사용 권고를 보류해요."
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
기한 전 표시가 있지만 관찰된 층 분리의 정상 여부가 확인되지 않아 개별 재사용 권고를 보류해요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
제품의 상태와 표시를 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0069 — 이전 판매자 답변과 이후 새 냄새

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `3c6f3583f7f32fe8d65a08b901ed20990c1f5756d4507bfc906f8ea9a37318a1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

판매자의 이전 외관 답변과 이후 새 냄새를 구분하고 개별 재사용 권고를 보류해요.

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
    "commerce.end_of_use": {
      "variable_id": "commerce.end_of_use",
      "state": "known",
      "value": {
        "seller_confirmed_previous_appearance_normal": true,
        "new_odor_reported_after_reply": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_reuse": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "판매자의 이전 외관 답변과 이후 새 냄새를 구분하고 개별 재사용 권고를 보류해요."
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
판매자의 이전 외관 답변과 이후 새 냄새를 구분하고 개별 재사용 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
제품 상태와 표시를 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0070 — 품질 의심 용기의 사용 종료와 타인에게 전달 문의

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `7ed73b6c1144c2fd55c739cdeb70d19639a89eabb8c740371a3b7e61932934dc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

품질 의심 용기의 본인 사용은 종료됐지만 품질이 확인되지 않아 타인에게 넘기는 개별 권고를 보류하고 제품 확인을 진행해요.

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "self_use_ended": true,
        "same_suspect_container_quality_unconfirmed": true,
        "asks_about_giving_to_another_person": true,
        "prior_skin_contact": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q06",
      "status": "hold",
      "guidance": "품질 의심 용기의 본인 사용은 종료됐지만 품질이 확인되지 않아 타인에게 넘기는 개별 권고를 보류하고 제품 확인을 진행해요."
    },
    {
      "card_id": "B-S07",
      "status": "unknown",
      "guidance": "해당 용기의 직접 피부 접촉 경로는 미상이며 아직 타인에게 전달했다고 보지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q06@0.6.1",
    "kb:B-S07@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
본인 사용이 끝났더라도 품질이 확인되지 않은 같은 용기를 다른 사람에게 넘기는 개별 권고는 보류해요. [kb:B-Q06@0.6.1]

### 필요한 다음 단계
직접 피부 접촉 경로는 미상이므로 공유 이력을 단정하지 말고 제품의 상태와 표시를 확인해 제조·판매처에 문의해 주세요. [kb:B-S07@0.6.1]

## syn-hold-0071 — 다른 용기의 정상 흔들림 안내

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `b8b0bd39c6447cbe7f8e4e8ff96a16f50718a6508bd730ee27fd6d996e11d342`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

한 용기의 흔들어 쓰는 안내로 다른 용기의 새 냄새를 설명하지 않고 개별 재사용 권고를 보류해요.

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
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "container_A_shake_before_use": true,
        "container_B_new_odor": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "wants_to_reuse_container_B": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "한 용기의 흔들어 쓰는 안내로 다른 용기의 새 냄새를 설명하지 않고 개별 재사용 권고를 보류해요."
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
한 용기의 흔들어 쓰는 안내로 다른 용기의 새 냄새를 설명하지 않고 개별 재사용 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
제품 상태와 표시를 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0072 — 기존 정상 냄새와 새 변화

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `30ea1d527fd4e4e2a69c26ac8b32039fcdaafe2e58f5f01deb1e73a355e69bdd`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 정상 냄새와 다른 새 변화가 확인돼 개별 재사용 권고를 보류하고 품질 확인을 진행해요.

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "prior_normal_odor_known": true,
        "odor_newly_changed": true,
        "wants_to_reuse": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "이전 정상 냄새와 다른 새 변화가 확인돼 개별 재사용 권고를 보류하고 품질 확인을 진행해요."
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
이전 정상 냄새와 다른 새 변화가 확인돼 개별 재사용 권고를 보류하고 품질 확인을 진행해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
제품 상태와 표시를 확인하고 필요하면 제조·판매처에 문의해 주세요.

## syn-hold-0073 — 지속 불편과 타인의 양호한 경험

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `8a4838be0e6fd1d8542e8e891deff44d191944037fe253c0fb4cf64dd2cdd9ef`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인의 지속 불편이 있어 다른 사람의 경험과 분리해 개별 권고를 보류해요.

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "friend_no_discomfort": true,
        "wants_self_reuse_advice": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "본인의 지속 불편이 있어 다른 사람의 경험과 분리해 개별 권고를 보류해요."
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
본인의 지속 불편이 있어 다른 사람의 경험과 분리해 개별 권고를 보류해요 [kb:B-B01@0.6.1].

### 필요한 다음 단계
지속되는 불편에 대해 전문가의 확인을 받아 주세요.

## syn-hold-0074 — 회수 공지의 제품과 제조번호 대조 미완료

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `28a727c07e904c03cc7bc7bc48480bff03248f799db68f79ff18bcbdc6cb0266`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제조번호가 확인되지 않아 대상 여부를 보류해요. 공지와 용기 정보를 확인해야 해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "용기": "합성 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "공지": "제품과 특정 제조번호가 대상",
        "용기 번호": "지워져 확인 불가"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "제조번호가 확인되지 않아 대상 여부를 보류해요. 공지와 용기 정보를 확인해야 해요."
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
회수 공지는 특정 제조번호를 대상으로 하지만 용기의 번호를 읽을 수 없어 대상 여부는 미상이에요. 해당 용기의 개별 제품 권고도 보류하며, 미상이라는 사실만으로 회수 대상이나 사용 금지를 확정하지 않아요. [kb:B-Q05@0.6.1]

### 필요한 다음 단계
공식 공지에서 제조번호를 확인할 다른 방법을 살펴요.

## syn-hold-0075 — 회수 공지의 기간과 구매일 미상

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `d49a15454ac41972e4eaab270658635edbe19b7087033e1a854256046b2650a7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

구매 시점이 미상이라 공지의 대상 여부를 보류해요. 공식 공지의 확인 방법을 살펴요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "용기": "합성 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "commerce.recall_check": {
      "variable_id": "commerce.recall_check",
      "state": "known",
      "value": {
        "공지": "특정 판매 기간에 판매된 제품 대상",
        "용기의 구매일": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q05",
      "status": "hold",
      "guidance": "구매 시점이 미상이라 공지의 대상 여부를 보류해요. 공식 공지의 확인 방법을 살펴요."
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
회수 공지의 판매 기간과 구매일을 대조할 정보가 없어 대상 여부가 미상이에요. 해당 제품의 개별 권고를 보류하되 회수 대상이나 사용 금지를 확정하지 않아요. [kb:B-Q05@0.6.1]

### 필요한 다음 단계
공식 공지와 구매 이력을 확인해 적용 범위를 살펴요.

## syn-hold-0076 — 기기 부속품과 허용 제품의 관계 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `c983d125d7003466382b03eda21c6da331dcec19ff96b62df2c794b1d4ebff76`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 부속품의 호환이 확인될 때까지 해당 기기 사용 판단을 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "기기": "합성 피부관리 기기",
        "부속품": "별도 교체 부속품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "기기": "특정 부속품과 함께 사용 안내",
        "현재 부속품의 호환": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "hold",
      "guidance": "현재 부속품의 호환이 확인될 때까지 해당 기기 사용 판단을 보류해요."
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
현재 부속품이 기기에 호환되는지 확인되지 않아 해당 조합에 대한 개별 권고를 보류해요. 미확인만으로 고장이나 위해를 확정하지 않아요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
기기와 부속품 모델을 확인해 제조사 안내를 살펴요.

## syn-hold-0077 — 용기 손상과 내용물 상태 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `dff498e229c4ffa264cd51f5d5a0c33dd251a81c1560fe34026f57a7e807258d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손상된 용기의 내용물 상태를 확인할 수 없어 해당 제품의 사용 판단을 보류해요. 오염을 확정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "storage.seal_integrity": {
      "variable_id": "storage.seal_integrity",
      "state": "known",
      "value": {
        "상태": "용기 뚜껑 손상",
        "내용물 오염": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "손상된 용기의 내용물 상태를 확인할 수 없어 해당 제품의 사용 판단을 보류해요. 오염을 확정하지 않아요."
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
뚜껑이 손상된 용기의 내용물 상태가 미상이어서 해당 제품의 개별 권고를 보류해요. 손상만으로 오염을 확정하지 않아요. [kb:B-S04@0.6.1]

### 필요한 다음 단계
용기 손상 상태와 확인 방법을 제조사에 문의해요.

## syn-hold-0078 — 얼굴 지시와 목 부위의 제품 사용 범위

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `1decfd6ac714aa40345cdc0f1a67f99449aaee89c4753dff1d36b34361464a85`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

해당 제품의 얼굴 사용에 관한 개별 지시는 확인됐지만 목에 적용되는 지시는 미상이에요. 제품 표시를 얼굴의 개별 지시보다 우선하지 않고 목의 개별 권고는 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 얼굴과 목 겸용 관리 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "얼굴과 목에 매일 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "확인된 지시": "이 제품을 얼굴에 사용하지 않도록 안내받음",
        "목에 적용되는 지시": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "hold",
      "guidance": "해당 제품의 얼굴 사용에 관한 개별 지시는 확인됐지만 목에 적용되는 지시는 미상이에요. 제품 표시를 얼굴의 개별 지시보다 우선하지 않고 목의 개별 권고는 보류해요."
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
얼굴에 쓰지 말라는 해당 제품의 개별 의료진 지시는 확인됐고 제품의 일반 표시로 이를 덮어쓰지 않아요. 목에 대한 지시는 미상이므로 목 사용에 관한 개별 권고는 보류해요. [kb:B-G03@0.6.1]

### 필요한 다음 단계
목 부위에도 지시가 적용되는지 해당 의료진에게 확인해요.

## syn-hold-0079 — 반응이 보고된 제품의 다른 기기 재사용 계획

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `ba0eae147bbf8cc79dd3b302fb4e134608580a11a928c0ae8fc14f73d5d38ee8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

반응이 보고된 제품을 기기와 재사용하는 판단은 보류해요. 불편의 원인을 확정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 제품",
        "기기": "별도의 합성 기기"
      },
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
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "계획": "다른 기기와 함께 다시 사용"
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
            "statement": "제품 사용 후 불편 보고"
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
      "guidance": "반응이 보고된 제품을 기기와 재사용하는 판단은 보류해요. 불편의 원인을 확정하지 않아요."
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
제품 사용 뒤 불편이 보고됐고 다른 기기와 다시 사용하는 계획이 있어 해당 조합의 개별 권고를 보류해요. 불편의 원인은 확정하지 않아요. [kb:B-G06@0.6.1]

### 필요한 다음 단계
제품 사용 경험과 불편, 기기 사용 계획을 의료진에게 설명해요.

## syn-hold-0080 — 같은 이름의 두 제품 중 하나에 대한 개별 중지 지시

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `026c574a4ec9b2229080dc74bdfccab5054e525b310edd4673c913e44f1b5384`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 중지 지시는 가에만 귀속해요. 나에 대한 지시는 미상이며 두 제품의 개별 권고를 지시 확인 전 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 제품 가",
        "나": "같은 이름을 가진 별도 합성 제품 나"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "확인된 지시": "가의 사용을 중지하도록 안내받음",
        "나에 대한 지시": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "가와 나의 동일 여부": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "hold",
      "guidance": "확인된 중지 지시는 가에만 귀속해요. 나에 대한 지시는 미상이며 두 제품의 개별 권고를 지시 확인 전 보류해요."
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
의료진의 사용 중지 지시는 제품 가에 대해 확인됐어요. 같은 이름의 별도 제품 나에 대한 지시는 미상이므로 이름만으로 지시를 옮기지 않고 나의 개별 권고도 보류해요. [kb:B-G03@0.6.1]

### 필요한 다음 단계
두 제품의 정확한 식별 정보와 나에 적용되는 지시를 의료진에게 확인해요.

## syn-hold-0081 — 회피 원료와 성분표의 버전 불일치

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `05a52b307144eda302c3508cd3b0ee3d0d4ac67aa69ec8933005335bba33b691`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현행 제품의 회피 원료 함유 여부를 확인하기 전까지 해당 제품의 사용 판단을 보류해요. 이전 표기를 현행 함유의 확정으로 옮기지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "회피 원료": "리날룰"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "이전 성분표": "해당 원료 표기",
        "현행 성분표": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 제품 현행 용기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "hold",
      "guidance": "현행 제품의 회피 원료 함유 여부를 확인하기 전까지 해당 제품의 사용 판단을 보류해요. 이전 표기를 현행 함유의 확정으로 옮기지 않아요."
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
이전 성분표에는 회피 원료가 표시됐지만 현행 제품의 성분표는 확인되지 않았어요. 현행 함유나 부재를 확정하지 않고 해당 제품의 개별 권고를 보류해요. [kb:B-G11@0.6.1]

### 필요한 다음 단계
현행 용기와 일치하는 성분표를 확인해요.

## syn-hold-0083 — 다른 용기의 정상 분리와 새 냄새

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `a163c0ec1016dab21c7dbd5b75ce539977f3371dbe1fef6ec454136959d56af8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

용기 A의 정상 분리 표시는 용기 B의 새로운 비정상 냄새를 설명하지 않아요. 용기 B의 품질 확인 전 개별 사용 권고를 보류하며 용기 A까지 이상하다고 단정하지 않아요.

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
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "container_a": "shake_before_use",
        "container_b": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "container_a_normal_separation": true,
        "container_b_new_unusual_odor": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "hold",
      "guidance": "용기 A의 정상 분리 표시는 용기 B의 새로운 비정상 냄새를 설명하지 않아요. 용기 B의 품질 확인 전 개별 사용 권고를 보류하며 용기 A까지 이상하다고 단정하지 않아요."
    },
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "용기 A의 정상 분리 표시는 용기 B의 새로운 비정상 냄새를 설명하지 않아요. 용기 B의 품질 확인 전 개별 사용 권고를 보류하며 용기 A까지 이상하다고 단정하지 않아요."
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
용기 A의 정상적인 두 층 분리와 용기 B의 새로운 비정상 냄새는 서로 다른 관찰이에요. A의 흔들어 쓰라는 표시는 B의 냄새를 설명하지 않아요. B의 품질을 확인하기 전까지 B에 대한 개별 사용 권고를 보류해요. A가 이상하다거나 안전하다고 단정하지 않아요. [kb:B-P08@0.6.1] [kb:B-S04@0.6.1]

### 필요한 다음 단계
품질이 확인될 때까지 용기 B의 사용을 일시 보류해요. B의 제품 표시를 확인하고 제조판매업자 문의 창구에 새로운 냄새를 알려 품질을 확인해요.

## syn-sol-0194 — 실제 보습과 세정 시간 관계 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `3f7c61acd7cd384c3522c61f7b1ba4bff68f2422b91012cd76e07efa550bb543`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 보습 사용과 도포 당시 물기 상태는 확인됐지만 세정과 도포의 시간 관계는 미확인이에요.

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
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "slightly_damp_at_moisturizing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "special_label_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "실제 보습 사용과 도포 당시 물기 상태는 확인됐지만 세정과 도포의 시간 관계는 미확인이에요."
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
가벼운 건조가 있고 보습제를 바를 때 피부가 약간 촉촉했다는 관찰이 확인돼요 [kb:B-M01@0.6.1].

### 근거 및 이유
실제 사용과 당시 물기 상태는 확인됐지만, 세정과 도포의 시간 관계는 아직 확인되지 않았어요.

### 확인이 필요한 한계
세정 뒤의 보습 시점을 확인하기 전에는 그 시간 관계를 추정하지 않아요.

## syn-sol-0195 — 찬물 체감

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `7d3f95e06f282b2c6fac75da7bea2a39aad5691d270ab98b362a208293427e5d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

차갑다는 보고만으로 뜨거운 물 사용 차이를 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "perceived_cold": true,
        "perceived_hot": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "차갑다는 보고만으로 뜨거운 물 사용 차이를 만들지 않아요."
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
차갑다는 보고만으로 뜨거운 물 사용 차이를 만들지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0196 — 경과 시간과 접촉 행동

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `0a90c288aa796464946a6543959972f3932668e5204239639c77bbe58a76a360`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

경과 시간만으로 일부러 오래 문지르거나 방치했는지 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "contact_time_instruction_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.contact_time": {
      "variable_id": "dose.contact_time",
      "state": "known",
      "value": 60,
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "intentional_long_rubbing_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "경과 시간만으로 일부러 오래 문지르거나 방치했는지 판단하지 않아요."
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
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
경과 시간만으로 일부러 오래 문지르거나 방치했는지 판단하지 않아요. [kb:B-C03@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0197 — 보습 사용과 시점 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1316576ad1e97b583a1982fe43b26677853c6c850c61887615d955849f5fa645`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제 사용은 확인됐지만 도포 당시 물기 상태는 미상이에요.

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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true
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
      "guidance": "보습제 사용은 확인됐지만 도포 당시 물기 상태는 미상이에요."
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
보습제 사용은 확인됐지만 도포 당시 물기 상태는 미상이에요. [kb:B-M01@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0203 — 보습제 보유와 사용 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `33da0c69a023d18722cd5e8cf2bcda49e9e996a1f0c1da2d8cc58021041ec8c5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제 보유만으로 실제 사용이나 목표 충족을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_available": true,
        "actual_use_unknown": true
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
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M03",
      "status": "unknown",
      "guidance": "보습제 보유만으로 실제 사용이나 목표 충족을 확정하지 않아요."
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
보습제 보유만으로 실제 사용이나 목표 충족을 확정하지 않아요. [kb:B-M03@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0204 — 두 단계의 목적 미확인

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `20bb428a6173b41aca6d0ebfcbf3304dc6545e877bb1f60089010b6d5525df80`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

단계 수만으로 추가 목적의 유무를 판단하지 않아요.

### 입력

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
        "purpose_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.target_load": {
      "variable_id": "cleansing.target_load",
      "state": "known",
      "value": {
        "makeup_and_sweat_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "단계 수만으로 추가 목적의 유무를 판단하지 않아요."
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
단계 수만으로 추가 목적의 유무를 판단하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0205 — 수건 사용과 마찰 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `dad22aaab07bb23331b36cee0775a712a38f06ae081456db4080a583814ecdc0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

수건 사용만으로 강한 비빔을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "towel_used": true,
        "rubbing_intensity_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "수건 사용만으로 강한 비빔을 확정하지 않아요."
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
수건 사용만으로 강한 비빔을 확정하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0206 — 보습 사용과 반응 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a09dbc22066f0b36629b8ed5a3b744dcadc1c81630113968e69af28bc24337e4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 사용만으로 건조 불편의 충족을 확인할 수 없어요.

### 입력

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
      "guidance": "실제 사용만으로 건조 불편의 충족을 확인할 수 없어요."
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
실제 사용만으로 건조 불편의 충족을 확인할 수 없어요. [kb:B-M02@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0207 — 헹굼 수행과 지시 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `bfd6fabcad44f2a516aa3dd8f9b3a6c3c1d1a3fee3bf229eed1018301c02d6fa`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

헹굼은 확인됐지만 해당 제품의 지시가 미상이라 부합을 확정하지 않아요.

### 입력

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
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "method.rinse": {
      "variable_id": "method.rinse",
      "state": "known",
      "value": {
        "performed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "헹굼은 확인됐지만 해당 제품의 지시가 미상이라 부합을 확정하지 않아요."
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
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
헹굼은 확인됐지만 해당 제품의 지시가 미상이라 부합을 확정하지 않아요. [kb:B-C06@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0208 — 물기 상태와 사용 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `8096ed9fb43972851d11b632f3ef760bbf47b30296d89e045a3f69504e32b21f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

피부 물기만으로 실제 보습제 사용이나 도포 시점을 추정하지 않아요.

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
        "moisturizer_use_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "unknown",
      "guidance": "피부 물기만으로 실제 보습제 사용이나 도포 시점을 추정하지 않아요."
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
피부 물기만으로 실제 보습제 사용이나 도포 시점을 추정하지 않아요. [kb:B-M01@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0217 — 표시 용기와 실제 대상의 연결 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `7a4c8491842629507a0d1f2c6d3df248e9049515b49221fb0db1ed65008dcc44`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시를 확인한 용기와 실제 비교 대상 용기가 같은지 몰라 대상 제품의 기본 성능은 미상이에요.

### 입력

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
        "container_a": 50,
        "actual_container_binding": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "container_a": "broad_spectrum",
        "actual_container_binding": "unknown"
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
      "guidance": "표시를 확인한 용기와 실제 비교 대상 용기가 같은지 몰라 대상 제품의 기본 성능은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "The American Academy of Dermatology recommends choosing broad-spectrum, water-resistant sunscreen with SPF 30 or higher.",
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
표시를 확인한 용기와 실제 비교 대상 용기가 같은지 몰라 대상 제품의 기본 성능은 미상이에요 [kb:B-P01@0.6.1].

### 근거 및 이유
미국 피부과학회는 광범위 보호, 내수성과 SPF 30 이상을 갖춘 제품을 권장해요 [ref:S16].

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0222 — 제거 지시와 사용 제품의 연결

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d0bfb54522b228e3c01b415f0baffb0ca0fe7ec11ee7aa51b95596539ced0627`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 제품의 제거 지시로 실제 사용한 제품의 지시나 반복 세안 행동을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "product_a": "specific_removal_instruction_confirmed",
        "product_b": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "water_resistant_product_used": "product_b",
        "repeat_wash_behavior": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "다른 제품의 제거 지시로 실제 사용한 제품의 지시나 반복 세안 행동을 확정하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
다른 제품의 제거 지시로 실제 사용한 제품의 지시나 반복 세안 행동을 확정하지 않아요 [kb:B-I01@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0223 — 잘린 표시 사진과 표시 부재

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `fbcbef8068d354cae78b6d6180103379f4598a03e180db2616c5666551e40b7c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사진이 잘려 SPF와 광범위 보호 여부를 확인할 수 없으며 표시가 없다고 단정하지 않아요.

### 입력

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
        "label_photo_cropped": true,
        "label_absence_confirmed": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "label_photo_cropped": true,
        "label_absence_confirmed": false
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
      "guidance": "사진이 잘려 SPF와 광범위 보호 여부를 확인할 수 없으며 표시가 없다고 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "The American Academy of Dermatology recommends choosing broad-spectrum, water-resistant sunscreen with SPF 30 or higher.",
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
사진이 잘려 SPF와 광범위 보호 여부를 확인할 수 없으며 표시가 없다고 단정하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
미국 피부과학회는 광범위 보호, 내수성과 SPF 30 이상을 갖춘 제품을 권장해요 [ref:S16].

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0225 — 해당 제품의 구체적 제거 지시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `b14dd86f68d256e51278a2605a4988172f83e1466a86e693aea7ba60a9cb4120`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 제품의 구체적 제거 지시가 확인돼 반복 행동과 지시의 일치 여부를 따로 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "actual_product": "specific_removal_instruction_confirmed"
      },
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
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "instruction_match": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "exception",
      "guidance": "같은 제품의 구체적 제거 지시가 확인돼 반복 행동과 지시의 일치 여부를 따로 확인해요."
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

### 응답 초안 — 미승인

### 핵심 안내
같은 제품의 구체적 제거 지시가 확인돼 반복 행동과 지시의 일치 여부를 따로 확인해요 [kb:B-I01@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
관련 조건을 따로 확인하고 다른 대상의 정보로 대신하지 않아요.

## syn-sol-0229 — 판매 페이지와 용기의 수치

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c81f93e7a7216e4f2128423851b29e53687c5a34fe8289d7379c16cb55530cea`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시 수치가 충돌하고 동일 버전인지 미상이라 판매 페이지 수치를 현재 용기에 적용하지 않아요.

### 입력

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
        "container": 30,
        "seller_page": 50,
        "same_version": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.uva": {
      "variable_id": "product.uva",
      "state": "known",
      "value": {
        "container": "broad_spectrum"
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
      "guidance": "표시 수치가 충돌하고 동일 버전인지 미상이라 판매 페이지 수치를 현재 용기에 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "The American Academy of Dermatology recommends choosing broad-spectrum, water-resistant sunscreen with SPF 30 or higher.",
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
표시 수치가 충돌하고 동일 버전인지 미상이라 판매 페이지 수치를 현재 용기에 적용하지 않아요 [kb:B-P01@0.6.1].

### 근거 및 이유
미국 피부과학회는 광범위 보호, 내수성과 SPF 30 이상을 갖춘 제품을 권장해요 [ref:S16].

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0232 — 밀림 후 초기 사용과 재도포 기록

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c12369471a3f20da5085f1a05c25d2734985e9bc6bfc6bbabe379369c939ca40`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

처음 사용을 유지한 것은 확인되지만 밀림과 관련된 재도포 행동은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "self_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "initial_use_reduced": false,
        "reapplication_due_to_pilling": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "처음 사용을 유지한 것은 확인되지만 밀림과 관련된 재도포 행동은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "A laboratory study used ultraviolet reflectance photography to examine selected sunscreen and moisturizer application sequences.",
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
처음 사용을 유지한 것은 확인되지만 밀림과 관련된 재도포 행동은 미상이에요 [kb:B-I02@0.6.1].

### 근거 및 이유
제한된 제품 조합을 자외선 반사 영상으로 살핀 실험이 있어요 [ref:S09].

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0235 — 반복 세안의 이유 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `91130b69a475abebd49d68174765f5795df54eeab94a426cbea297ca1968495e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

반복 세안은 보고됐지만 내수성 표시만을 이유로 자동 반복했는지는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "labeled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "cleansing.repeat_wash": {
      "variable_id": "cleansing.repeat_wash",
      "state": "known",
      "value": {
        "automatic_multi_step_for_water_resistant": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "repeat_wash_occurred": true,
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
      "guidance": "반복 세안은 보고됐지만 내수성 표시만을 이유로 자동 반복했는지는 미상이에요."
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

### 응답 초안 — 미승인

### 핵심 안내
반복 세안은 보고됐지만 내수성 표시만을 이유로 자동 반복했는지는 미상이에요 [kb:B-I01@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0236 — 수영 계획과 실제 접촉

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `25d821c56c7e1489906e30ea3001065f72ef4046952fcddf659726e4a7235a9a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

수영과 재도포 계획만으로 실제 접촉이나 행동을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.water_contact": {
      "variable_id": "sun.water_contact",
      "state": "known",
      "value": {
        "planned_swimming": true,
        "actual_water_contact": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "planned": false,
        "actual": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "수영과 재도포 계획만으로 실제 접촉이나 행동을 확정하지 않아요."
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
수영과 재도포 계획만으로 실제 접촉이나 행동을 확정하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0237 — 기한과 개봉 후 기간

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a10d3c2fa450a4c5b427ae3f5b226fcb7b5cbd7f15fe14e1ad0698a486bda5e1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시 기한과 이상 변화 부재는 확인됐지만 개봉 후 사용기간 판단은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "printed_date_not_passed": true,
        "opening_date": "unknown",
        "period_after_opening": "unknown"
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
      "card_id": "B-P08",
      "status": "unknown",
      "guidance": "표시 기한과 이상 변화 부재는 확인됐지만 개봉 후 사용기간 판단은 미상이에요."
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
표시 기한과 이상 변화 부재는 확인됐지만 개봉 후 사용기간 판단은 미상이에요 [kb:B-P08@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0240 — 과거 버전 지침과 현재 행동

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `fc9a02d69b5ff57d3d3b20533baeba393ded60156a3fb4a80a5fa4f6ad07a575`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

과거 버전의 지침과 별개로 현재 용기의 지침과 실제 재도포 행동이 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "self_outdoors": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "behavior": "unknown",
        "old_version_instruction_available": true,
        "current_version_instruction": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "과거 버전의 지침과 별개로 현재 용기의 지침과 실제 재도포 행동이 미상이에요."
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
과거 버전의 지침과 별개로 현재 용기의 지침과 실제 재도포 행동이 미상이에요 [kb:B-P03@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0243 — 씻어내는 팩에 다른 제품의 밤 사용 지시 적용

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `86f832b7e83d204481ce33a4aef5c0f67237482db8fdcd8a7f528f3ab9b2378b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 실제 사용은 가의 표시와 달라요. 나의 사용법을 가에 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 씻어내는 팩",
        "나": "합성 수면팩"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "가": "10분 뒤 씻어냄",
        "나": "밤새 두고 아침에 씻어냄"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "실제": "가를 밤새 둠",
        "중복 관리": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "difference",
      "guidance": "가의 실제 사용은 가의 표시와 달라요. 나의 사용법을 가에 적용하지 않아요."
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
팩 가의 표시는 10분 뒤 씻어내는 것이지만 실제로는 밤새 두었어요. 가의 표시된 시간에 맞춰 사용 방식을 조정해요. [kb:B-G05@0.6.1]

### 근거 및 이유
다른 수면팩 나의 밤 사용 지시를 가에 적용할 수 없어요. 이 차이는 위해나 원인을 확정하지 않아요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
다른 관리의 중복 여부는 확인되지 않았어요.

## syn-sol-0244 — 다른 상자에서 나온 두 제형의 혼합

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `bdefed23dc5c7ef06d105cb833a5ba1dc6b453f327b0b60f5a87124ad5f23e2c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

서로 다른 상자의 조합에도 표시가 적용되는지는 미상이에요. 호환 여부를 확인하기 전에는 차이나 안전성을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 키트 첫 제형",
        "나": "다른 상자의 둘째 제형"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "상자에 포함된 두 제형을 섞어 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.mixing": {
      "variable_id": "method.mixing",
      "state": "known",
      "value": {
        "실제": "다른 상자에서 나온 제형을 섞음",
        "상자 간 호환": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "unknown",
      "guidance": "서로 다른 상자의 조합에도 표시가 적용되는지는 미상이에요. 호환 여부를 확인하기 전에는 차이나 안전성을 확정하지 않아요."
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
서로 다른 상자의 조합에도 표시가 적용되는지는 미상이에요. 호환 여부를 확인하기 전에는 차이나 안전성을 확정하지 않아요. [kb:B-G04@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G04@0.6.1]

### 확인이 필요한 한계
두 상자의 제형을 함께 써도 된다는 해당 제품의 안내가 있는지 확인해요.

## syn-sol-0245 — 같은 용기의 교체된 펌프 헤드

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `304a44c5bc075a0667949625c4d60c07891fb3211aab68d8977592550613c2db`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

용기가 같아도 새 헤드의 토출량은 미상이에요. 이전 수치를 새 헤드에 그대로 적용할 수 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.dispensing_unit_context": {
      "variable_id": "product.dispensing_unit_context",
      "state": "known",
      "value": {
        "용기": "같은 합성 용기",
        "변경": "펌프 헤드 교체",
        "이전 헤드 토출량": "확인됨",
        "새 헤드 토출량": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "주장": "새 헤드의 한 번 토출량도 이전과 같음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "용기가 같아도 새 헤드의 토출량은 미상이에요. 이전 수치를 새 헤드에 그대로 적용할 수 없어요."
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
용기가 같아도 새 헤드의 토출량은 미상이에요. 이전 수치를 새 헤드에 그대로 적용할 수 없어요. [kb:B-G08@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
교체한 헤드의 한 번 토출량을 확인해요.

## syn-sol-0246 — 면도 준비 기록의 방식 귀속 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `c296c6d2cb1df00405963c40b4347074491368b885d8aa26b5e934f20f1a164b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

준비 기록이 어느 방식에 적용됐는지 몰라 적합성은 미상이에요. 각 방식과 지시의 연결을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "가능한 방식": "습식 수동 날면도와 건식 전용 전기면도",
        "기록 대상": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.preparation": {
      "variable_id": "shaving.preparation",
      "state": "known",
      "value": {
        "기록": "물과 면도 젤 사용",
        "어느 방식에 적용했는지": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "전기면도기": "건식 전용",
        "젤": "습식 날면도에 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G09",
      "status": "unknown",
      "guidance": "준비 기록이 어느 방식에 적용됐는지 몰라 적합성은 미상이에요. 각 방식과 지시의 연결을 확인해요."
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
준비 기록이 어느 방식에 적용됐는지 몰라 적합성은 미상이에요. 각 방식과 지시의 연결을 확인해요. [kb:B-G09@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G09@0.6.1]

### 확인이 필요한 한계
물과 젤을 어느 면도 방식에 사용했는지 확인해요.

## syn-sol-0247 — 일반 주의 문구와 특정 원료 함유

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `4148fbb28f7b00e7980402cfc0bb5318ebb8686dab6279f85c48a6e9292e62df`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

일반 주의 문구만으로 특정 원료의 함유나 부재를 확정할 수 없어요. 현행 전성분과 버전을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.known_allergies": {
      "variable_id": "person.known_allergies",
      "state": "known",
      "value": {
        "회피 원료": "리날룰"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "현행 전성분표": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.fragrance": {
      "variable_id": "product.fragrance",
      "state": "known",
      "value": {
        "확인된 문구": "향료 알레르겐 주의",
        "개별 원료 함유": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "일반 주의 문구만으로 특정 원료의 함유나 부재를 확정할 수 없어요. 현행 전성분과 버전을 확인해요."
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
일반 주의 문구만으로 특정 원료의 함유나 부재를 확정할 수 없어요. 현행 전성분과 버전을 확인해요. [kb:B-G17@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G17@0.6.1]

### 확인이 필요한 한계
현행 제품의 전성분표에 회피 원료가 있는지 확인해요.

## syn-sol-0248 — 서로 다른 시작 뒤 같은 날 재개

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c76c216b5fd6914e8231c5ea57f866389a348426fab4cf1d2edefa2e32898c00`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

서로 다른 최초 시작일에도 재개가 겹쳐 변화 원인을 분리할 수 없어요. 특정 제품의 원인으로 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "제품 가": "먼저 시작 후 중단하고 재개",
        "제품 나": "다른 날 시작 후 중단하고 가와 같은 날 재개",
        "관찰": "재개 후 변화 기록",
        "원인": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G12",
      "status": "unknown",
      "guidance": "서로 다른 최초 시작일에도 재개가 겹쳐 변화 원인을 분리할 수 없어요. 특정 제품의 원인으로 확정하지 않아요."
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
서로 다른 최초 시작일에도 재개가 겹쳐 변화 원인을 분리할 수 없어요. 특정 제품의 원인으로 확정하지 않아요. [kb:B-G12@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G12@0.6.1]

### 확인이 필요한 한계
두 제품을 재개한 이력과 관찰 시점을 구분해 기록해요.

## syn-sol-0249 — 각질관리와 레티놀의 사용 부위 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `0337ea2489b0802f21536d97655c4e404ff4966a44f38708d43ec5434d1a29e1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 날 사용만으로 전체 정렬을 확정하지 않아요. 제품 역할과 사용 부위를 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "각질관리": "저녁에 실제 사용",
        "레티놀": "다른 날 저녁에 실제 사용",
        "같은 부위": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "다른 날 사용만으로 전체 정렬을 확정하지 않아요. 제품 역할과 사용 부위를 확인해요."
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
다른 날 사용만으로 전체 정렬을 확정하지 않아요. 제품 역할과 사용 부위를 확인해요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
각 제품의 관리 역할과 같은 부위에 사용했는지 확인해요.

## syn-sol-0250 — 복합 완제품 보유와 별도 관리 사용

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `29b83432632af7dff83d99d2ca5a87050cbde5ed6e8c92fee9dfa30c05e0293c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

미사용 제품을 실제 중첩으로 세지 않아요. 다른 관리의 존재는 별도로 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 복합 관리제",
        "나": "합성 별도 각질관리제"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "가": "보유만 하고 미사용",
        "나": "얼굴에 실제 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "미사용 제품을 실제 중첩으로 세지 않아요. 다른 관리의 존재는 별도로 확인해요."
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
미사용 제품을 실제 중첩으로 세지 않아요. 다른 관리의 존재는 별도로 확인해요. [kb:B-G15@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
현재 실제 사용하는 다른 각질관리가 있는지 확인해요.

## syn-sol-0251 — 처방과 화장품의 시간 관계 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ee4ab38109e76024894f9c3cdf75249ecd5eeb790a8c8e70836923505be8e911`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 부위 사용은 확인됐지만 시간 관계와 처방 지시는 미상이에요. 처방을 변경하지 않고 적용 지시를 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "처방 제품": "얼굴에 실제 사용",
        "화장품": "얼굴에 실제 사용",
        "시간 관계": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "처방": "합성 의약품",
        "화장품": "합성 각질관리 제품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "같은 부위 사용은 확인됐지만 시간 관계와 처방 지시는 미상이에요. 처방을 변경하지 않고 적용 지시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
같은 부위 사용은 확인됐지만 시간 관계와 처방 지시는 미상이에요. 처방을 변경하지 않고 적용 지시를 확인해요. [kb:B-G14@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
제품을 사용한 시간 관계와 해당 처방 지시를 확인해요.

## syn-sol-0252 — 성분표와 실제 관리 목적의 구별

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `31baa7f7a8bc78546d1c220cd2eedfef0ee607095f0cc434b5a9e1c4647d469e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

성분명과 표시 목적은 확인됐지만 실제 관리 역할과 중첩 맥락은 미상이에요. 성분명만으로 농도나 사용 목적을 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "현행 성분표": "살리실릭애씨드 표기"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "표시 목적": "보습",
        "실제 각질관리 목적": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "사용": "실제 사용",
        "다른 각질관리와의 관계": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "성분명과 표시 목적은 확인됐지만 실제 관리 역할과 중첩 맥락은 미상이에요. 성분명만으로 농도나 사용 목적을 정하지 않아요."
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
성분명과 표시 목적은 확인됐지만 실제 관리 역할과 중첩 맥락은 미상이에요. 성분명만으로 농도나 사용 목적을 정하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
실제 사용 목적과 다른 각질관리와의 관계를 확인해요.

## syn-sol-0253 — 의료진 지시의 적용 기간 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `146d806d3f462ae2447ea666a1082b21a62bbe27932f0506b1b0fe2d9ce46885`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

대상 화장품은 확인됐지만 지시가 현재에도 적용되는지는 미상이에요. 처방을 변경하지 않고 적용 기간을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "내용": "합성 설정에서 특정 화장품과 처방을 함께 사용해도 된다는 지시",
        "적용 기간": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "처방": "현재 사용",
        "화장품": "현재 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "대상 화장품은 확인됐지만 지시가 현재에도 적용되는지는 미상이에요. 처방을 변경하지 않고 적용 기간을 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
대상 화장품은 확인됐지만 지시가 현재에도 적용되는지는 미상이에요. 처방을 변경하지 않고 적용 기간을 확인해요. [kb:B-G14@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
의료진 지시가 현재 사용에도 적용되는지 확인해요.

## syn-sol-0254 — 이전 제형의 국소 확인과 새 제형

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `b3684711c767f79d7c7d409a9e3a2d0165582c26331144a0399406d43c2b4fa9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 제형의 기록을 새 제형의 사용 경험으로 옮길 수 없어요. 새 제형의 실제 사용 여부를 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "이전": "합성 제품 이전 제형",
        "현재": "같은 이름의 새 제형"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "이전 제형": "작은 부위 사용 기록",
        "새 제형": "사용 여부 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G11",
      "status": "unknown",
      "guidance": "이전 제형의 기록을 새 제형의 사용 경험으로 옮길 수 없어요. 새 제형의 실제 사용 여부를 확인해요."
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

### 핵심 안내
이전 제형의 기록을 새 제형의 사용 경험으로 옮길 수 없어요. 새 제형의 실제 사용 여부를 확인해요. [kb:B-G11@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G11@0.6.1]

### 확인이 필요한 한계
새 제형의 실제 사용 여부와 해당 제품 지시를 확인해요.

## syn-sol-0255 — 향 이름과 각질관리 성분의 혼동

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `cb51e0f2eddaca6752d57563380198708a82db4d7aa0724263a63ea095d55308`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

향 이름만으로 각질관리 성분의 함유나 역할을 확정하지 않아요. 현행 전성분과 사용 목적을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "확인된 문구": "향 이름에 산이라는 단어가 있음",
        "전성분": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "제품": "실제 사용",
        "각질관리 목적": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "향 이름만으로 각질관리 성분의 함유나 역할을 확정하지 않아요. 현행 전성분과 사용 목적을 확인해요."
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

### 응답 초안 — 미승인

### 핵심 안내
향 이름만으로 각질관리 성분의 함유나 역할을 확정하지 않아요. 현행 전성분과 사용 목적을 확인해요. [kb:B-G15@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
현행 전성분과 실제 관리 목적을 확인해요.

## syn-sol-0256 — 가족의 처방 지시와 본인의 관리

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `532350b94dde20efd54b0463262f0cd199042ca37a1be0f25ad21d1107909d30`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족의 지시는 본인의 처방 지시로 옮길 수 없어요. 본인에게 적용되는 개별 지시는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "본인": "처방 지시 미확인",
        "가족": "각질관리 제품 회피 지시"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "본인": "합성 화장품 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "가족의 지시는 본인의 처방 지시로 옮길 수 없어요. 본인에게 적용되는 개별 지시는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가족의 지시는 본인의 처방 지시로 옮길 수 없어요. 본인에게 적용되는 개별 지시는 미상이에요. [kb:B-G14@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
본인에게 적용되는 개별 지시가 있는지 확인해요.

## syn-sol-0257 — 동일 부위 각질관리 사용 기록의 충돌

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `e83e2264533d5fe45eeb2e061879d91e1d965b90a1c72b487fca16f0985e90f4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

복합 제품의 실제 사용은 확인됐지만 별도 제품의 사용 기록이 상충해 중첩은 미상이에요. 기록을 확인하고 차이를 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 복합 각질관리제",
        "나": "별도 합성 각질관리제"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "가": "얼굴에 실제 사용",
        "나": "얼굴 사용 기록과 미사용 기록이 상충",
        "같은 시기 사용": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G15",
      "status": "unknown",
      "guidance": "복합 제품의 실제 사용은 확인됐지만 별도 제품의 사용 기록이 상충해 중첩은 미상이에요. 기록을 확인하고 차이를 만들지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
복합 각질관리제 가는 얼굴에 실제 사용했지만 별도 제품 나의 사용 기록은 서로 상충해요. 두 제품의 중첩 여부는 미상이에요. [kb:B-G15@0.6.1]

### 근거 및 이유
상충 기록만으로 같은 부위의 중첩이나 차이를 확정하지 않아요. [kb:B-G15@0.6.1]

### 확인이 필요한 한계
나를 얼굴에 실제 사용했는지와 가와 같은 시기였는지 확인해요.

## syn-sol-0258 — 처방의 중단 계획과 실제 사용 확인

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `fd278d9ca4b12c6603d3b8cb137c27178d85236e4bf3898af4681d6e7b77a9ee`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

중단을 생각하는 것과 실제 중단은 달라요. 처방 변경은 의료진과 상의할 사항이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "person.clinician_plan": {
      "variable_id": "person.clinician_plan",
      "state": "known",
      "value": {
        "의료진 지시": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "처방": "중단을 생각 중",
        "실제": "현재까지 사용 중"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G14",
      "status": "unknown",
      "guidance": "중단을 생각하는 것과 실제 중단은 달라요. 처방 변경은 의료진과 상의할 사항이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G14@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
중단을 생각하는 것과 실제 중단은 달라요. 처방 변경은 의료진과 상의할 사항이에요. [kb:B-G14@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G14@0.6.1]

### 확인이 필요한 한계
처방 변경을 생각한다면 본인 처방 의료진에게 확인해요.

## syn-sol-0259 — 다른 사람의 팩 사용기와 개인 경험

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `143895f990aa495a646185b71b4c72f318b929e184b67c92507505d8d5017682`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 사람의 경험을 본인의 반응으로 기록하지 않아요. 본인의 사용 여부와 경험은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "다른 사람": "팩 사용 후 불편을 보고",
        "본인": "같은 제품 사용 경험 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 팩"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "다른 사람의 경험을 본인의 반응으로 기록하지 않아요. 본인의 사용 여부와 경험은 미상이에요."
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
다른 사람의 경험을 본인의 반응으로 기록하지 않아요. 본인의 사용 여부와 경험은 미상이에요. [kb:B-G05@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
본인이 제품을 실제 사용했는지와 경험을 확인해요.

## syn-sol-0260 — 헤드 교체 계획과 현재 토출량

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `a78de75bf2219f73c7592fb36eb942d09d595cedbd5d3f0c5d6a78fee7d005fc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

교체 예정은 실제 교체가 아니에요. 새 헤드의 토출량을 현재 기록에서 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.dispensing_unit_context": {
      "variable_id": "product.dispensing_unit_context",
      "state": "known",
      "value": {
        "현재": "기존 펌프 사용",
        "계획": "새 펌프 헤드로 교체 예정",
        "새 헤드 토출량": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "dose.proxy_amount": {
      "variable_id": "dose.proxy_amount",
      "state": "known",
      "value": {
        "현재": "기존 헤드의 양 기록"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "교체 예정은 실제 교체가 아니에요. 새 헤드의 토출량을 현재 기록에서 추정하지 않아요."
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
교체 예정은 실제 교체가 아니에요. 새 헤드의 토출량을 현재 기록에서 추정하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
헤드를 실제 교체한 뒤에는 해당 헤드의 토출량을 확인해요.

## syn-sol-0261 — 처방명과 같은 이름의 제품 용도

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d5571822315d4c5d5780bda1b8331bb63a2543a9e69f84c25f6c8b0d3496ea17`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이름이 같아도 의약품과 화장품의 역할은 자동으로 같지 않아요. 화장품 성분과 실제 사용은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "가": "합성 처방 의약품",
        "나": "같은 이름을 포함한 합성 화장품"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "나의 현행 성분표": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "가": "사용 중",
        "나": "보유 여부 미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "이름이 같아도 의약품과 화장품의 역할은 자동으로 같지 않아요. 화장품 성분과 실제 사용은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이름이 같아도 의약품과 화장품의 역할은 자동으로 같지 않아요. 화장품 성분과 실제 사용은 미상이에요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
화장품의 현행 성분표와 실제 사용 여부를 확인해요.

## syn-sol-0262 — 팩 표시 시간과 실제 제거 시각 누락

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `3f02466fb90e2d23fc74a0a1f742470dcbb08b58de308e68ec882e305ca558f3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제거 시점이 없어 표시 시간과 실제 사용을 비교할 수 없어요. 중복 관리도 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "제품": "합성 씻어내는 팩",
        "표시": "10분 후 씻어냄"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "도포": "확인됨",
        "제거 시점": "기록하지 않음",
        "다른 관리 중복": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "제거 시점이 없어 표시 시간과 실제 사용을 비교할 수 없어요. 중복 관리도 미상이에요."
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
제거 시점이 없어 표시 시간과 실제 사용을 비교할 수 없어요. 중복 관리도 미상이에요. [kb:B-G05@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
팩을 실제 제거한 시점과 중복 관리 여부를 확인해요.

## syn-sol-0263 — 면도 젤 사용 계획과 다른 면도 기록

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d0b9e7060847d53a670ea932300fd479367b98b7d8d7ea9d743ce5150055c351`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다음 사용 계획은 이번 면도 준비의 증거가 아니에요. 이번 준비를 확인해야 해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "shaving.method": {
      "variable_id": "shaving.method",
      "state": "known",
      "value": {
        "기록": "습식 날면도"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "shaving.preparation": {
      "variable_id": "shaving.preparation",
      "state": "known",
      "value": {
        "젤": "다음 면도 때 사용할 계획",
        "이번 면도 사용": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G09",
      "status": "unknown",
      "guidance": "다음 사용 계획은 이번 면도 준비의 증거가 아니에요. 이번 준비를 확인해야 해요."
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
다음 사용 계획은 이번 면도 준비의 증거가 아니에요. 이번 준비를 확인해야 해요. [kb:B-G09@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G09@0.6.1]

### 확인이 필요한 한계
이번 면도에 사용한 준비 방법을 확인해요.

## syn-sol-0264 — 같은 제품의 새 포장과 사용시간 표시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ed3411ee7d79e516bc2edb83273b65ca594d274726c043531982644906a7f1e7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 포장의 시간을 새 포장의 표시로 확정하지 않아요. 현재 표시와 실제 시간을 확인해야 해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "기존": "합성 팩 이전 포장",
        "현재": "같은 제품명 새 포장"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "이전 포장": "10분",
        "현재 포장": "읽지 못함"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "현재 포장 제품 사용": "확인",
        "사용시간": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "이전 포장의 시간을 새 포장의 표시로 확정하지 않아요. 현재 표시와 실제 시간을 확인해야 해요."
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
이전 포장의 시간을 새 포장의 표시로 확정하지 않아요. 현재 표시와 실제 시간을 확인해야 해요. [kb:B-G05@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
새 포장의 사용시간 표시와 실제 사용시간을 확인해요.

## syn-sol-0265 — 이전 성분표와 현재 사용 제품의 버전

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `af0665049059258e07d228ab64a09c25639c9df1469c5396944343418bc65fbe`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 판의 성분을 현재 버전에 그대로 적용할 수 없어요. 현재 제품과 성분표의 버전을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.inci": {
      "variable_id": "product.inci",
      "state": "known",
      "value": {
        "이전 판": "레티놀 표기",
        "현행 판": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "현재 사용 제품": "합성 제품",
        "성분표와 버전 일치": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제": "현재 제품 사용"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "이전 판의 성분을 현재 버전에 그대로 적용할 수 없어요. 현재 제품과 성분표의 버전을 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 판의 성분을 현재 버전에 그대로 적용할 수 없어요. 현재 제품과 성분표의 버전을 확인해요. [kb:B-G13@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G13@0.6.1]

### 확인이 필요한 한계
현재 용기와 성분표의 버전이 일치하는지 확인해요.

## syn-sol-0266 — 제품 이름과 실제 사용 용도의 분리

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `f7a56a8ef52d5ab1843b32f775ff072a12107796740364fc62937ac09ad297fc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이름의 보호라는 표현만으로 제품 유형이나 실제 사용 용도를 확정하지 않아요. 제품 표시와 실제 사용을 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.identity": {
      "variable_id": "product.identity",
      "state": "known",
      "value": {
        "제품": "합성 제품 이름에 보호라는 표현이 있음",
        "제형과 유형": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "확인된 사용법": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "routine.co_use_context": {
      "variable_id": "routine.co_use_context",
      "state": "known",
      "value": {
        "실제 사용 목적": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "이름의 보호라는 표현만으로 제품 유형이나 실제 사용 용도를 확정하지 않아요. 제품 표시와 실제 사용을 확인해요."
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
제품 이름의 보호라는 표현만으로 제품 유형이나 실제 사용 용도를 정할 수 없어요. [kb:B-G08@0.6.1]

### 근거 및 이유
확인된 제품 사용법과 실제 사용 목적이 없어 이름만으로 기능을 판정하지 않아요. [kb:B-G08@0.6.1]

### 확인이 필요한 한계
제품의 현행 표시와 실제 사용 목적을 확인해요.

## syn-sol-0267 — 수면팩의 사용 방식은 확인되고 빈도는 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `b0bc81b24e70b846611b7316391fbd9f43cd51256d95c5987537c5332357986f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 사용 방식은 표시와 맞아요. 실제 빈도와 중복은 미상이므로 전체 정렬은 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.instructions": {
      "variable_id": "product.instructions",
      "state": "known",
      "value": {
        "표시": "밤에 바르고 아침에 씻어냄",
        "빈도": "표시에 있음"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "adjunct.care_events": {
      "variable_id": "adjunct.care_events",
      "state": "known",
      "value": {
        "실제 방식": "밤에 바르고 아침에 씻어냄",
        "실제 빈도": "미확인",
        "중복 관리": "미확인"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G05",
      "status": "unknown",
      "guidance": "확인된 사용 방식은 표시와 맞아요. 실제 빈도와 중복은 미상이므로 전체 정렬은 확정하지 않아요."
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
확인된 사용 방식은 표시와 맞아요. 실제 빈도와 중복은 미상이므로 전체 정렬은 확정하지 않아요. [kb:B-G05@0.6.1]

### 근거 및 이유
확인된 사용과 표시, 또는 미확인 정보를 구분해 살펴요. [kb:B-G05@0.6.1]

### 확인이 필요한 한계
실제 사용 빈도와 다른 관리의 중복 여부를 확인해요.

## syn-sol-0209 — 가족의 뜨거운 물과 본인의 미온수

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `40afdba39dbf334fd0b140056bdea594e82eba8222213c28709724120a1a243c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족의 체감을 본인의 관찰로 옮기지 않고 본인의 미온수 사용을 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "self_perceived_lukewarm": true,
        "family_member_perceived_hot": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "가족의 체감을 본인의 관찰로 옮기지 않고 본인의 미온수 사용을 살펴요."
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
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인이 미온수를 쓴다는 보고는 이 카드의 수온 기준에 부합해요. [kb:B-C01@0.6.1]

### 근거 및 이유
가족이 뜨겁게 느낀 물을 본인의 관찰로 옮기지 않아요.

### 확인이 필요한 한계
본인의 정확한 물 온도는 확인되지 않았어요.

## syn-sol-0210 — 타인의 마찰과 본인의 손가락

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `be1d64d7eb56dcf45031365dee50ca64c57bba658b6a771ac99b29d2eec163ce`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 사람의 마찰을 본인에게 옮기지 않고 본인의 부드러운 방법을 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "self_gentle_fingertip_cleansing": true,
        "other_person_rubs_strongly": true,
        "self_towel_patted_gently": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "다른 사람의 마찰을 본인에게 옮기지 않고 본인의 부드러운 방법을 살펴요."
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
본인이 손가락으로 부드럽게 씻고 수건으로 가볍게 닦는 방법은 이 카드에 부합해요. [kb:B-C02@0.6.1]

### 근거 및 이유
다른 사람의 강한 마찰을 본인의 행동으로 판단하지 않아요.

### 확인이 필요한 한계
이 관찰만으로 다른 사람이나 본인의 피부 상태를 진단하지 않아요.

## syn-sol-0211 — 본인과 타인의 건조

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `abf2bad37a0d1cb9d35e1dce0051a960790527fd96f9031010fd2b9db652d570`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

타인의 건조를 본인에게 옮기지 않고 본인의 사용 경험을 살펴요.

### 입력

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
    "moisturizing.comfort": {
      "variable_id": "moisturizing.comfort",
      "state": "known",
      "value": {
        "comfortable": true,
        "other_person_dryness": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
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
      "guidance": "타인의 건조를 본인에게 옮기지 않고 본인의 사용 경험을 살펴요."
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
본인은 건조가 없고 보습 사용이 편안하다고 보고해 이 카드의 부합 조건에 맞아요. [kb:B-M02@0.6.1]

### 근거 및 이유
다른 사람의 건조를 본인의 증상으로 옮기지 않아요.

### 확인이 필요한 한계
현재 보고가 미래에도 불편이 없다는 보증은 아니에요.

## syn-sol-0212 — 미온수 사용

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `087f584fb0c5129b97359c55b36a299b977d01ca42e837559571e345809501c5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인의 미온수 사용이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "perceived_lukewarm": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "본인의 미온수 사용이 확인돼요."
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
    },
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
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S15"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인의 미온수 사용은 이 카드의 수온 기준에 부합해요. [kb:B-C01@0.6.1]

### 근거 및 이유
확인된 본인의 체감을 기준으로 판단해요.

### 확인이 필요한 한계
정확한 온도 수치는 확인되지 않았어요.

## syn-sol-0213 — 건조한 피부까지 기다리는 보습

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `db1ae8b6dc1b537f44eac61f6be8e7a9d933d9716d6b4b5457be5870c09e3c11`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

경미한 건조가 있고 세정 후 오래 기다려 완전히 마른 뒤에만 보습해 시점을 검토해요.

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
    "method.skin_wetness": {
      "variable_id": "method.skin_wetness",
      "state": "known",
      "value": "fully_dry_at_moisturizing",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "waits_long_after_cleansing": true,
        "special_label_instruction": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M01",
      "status": "difference",
      "guidance": "경미한 건조가 있고 세정 후 오래 기다려 완전히 마른 뒤에만 보습해 시점을 검토해요."
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
    },
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
    "kb:B-M01@0.6.1",
    "ref:S04"
  ],
  "distractor_refs": [
    "ref:S15"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
가벼운 건조가 있고 세정 후 오래 기다려 완전히 마른 뒤에만 보습한다면, 피부가 약간 촉촉할 때 보습하는 방향을 살펴요. [kb:B-M01@0.6.1]

### 근거 및 이유
실제 사용과 오래 기다리는 습관이 확인됐고 별도 제품 지시는 없다고 보고됐어요.

### 확인이 필요한 한계
개별 의료진 계획이 있다면 함께 확인하며 건조의 원인이나 효과는 단정하지 않아요.

## syn-sol-0214 — 장갑을 낀 손가락 사용과 마찰 정도 미상

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `e6bbe445238ec2544ac25dc963256ed13ea2e3b42362e9620356f84cab46866c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

장갑을 낀 손가락 사용이 확인됐지만 마찰 강도는 미상이에요. 장갑 사용만으로 강한 마찰을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.tools": {
      "variable_id": "method.tools",
      "state": "known",
      "value": [
        "gloves"
      ],
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "cleansing_with_clean_wet_gloved_fingers": true,
        "friction_intensity_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "unknown",
      "guidance": "장갑을 낀 손가락 사용이 확인됐지만 마찰 강도는 미상이에요. 장갑 사용만으로 강한 마찰을 확정하지 않아요."
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
깨끗하고 젖은 장갑을 낀 손가락으로 씻었다는 관찰은 있지만 실제 마찰 강도는 미상이에요 [kb:B-C02@0.6.1].

### 근거 및 이유
장갑 사용 여부와 세정할 때 얼마나 강하게 문질렀는지는 다른 정보예요. 장갑만으로 강한 마찰이나 문지르는 도구 사용을 확정하지 않아요.

### 확인이 필요한 한계
손가락을 어떻게 움직였는지와 마찰 정도를 확인하기 전에는 마찰 항목의 부합이나 차이를 확정하지 않아요.

## syn-sol-0215 — 건조에도 무조건 보습 감량

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `b70637d90568fa014e62054b155a1439a0e0defac27fac25779f326d453acdc8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가벼운 건조가 있지만 따가움은 없고 건조 여부와 관계없이 보습을 줄이고 있어 사용 방법을 검토해요.

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
    "skin.stinging": {
      "variable_id": "skin.stinging",
      "state": "known",
      "value": "none",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "moisturizer_used": true,
        "reduces_regardless_of_dryness": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M02",
      "status": "difference",
      "guidance": "가벼운 건조가 있지만 따가움은 없고 건조 여부와 관계없이 보습을 줄이고 있어 사용 방법을 검토해요."
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
가벼운 건조가 있는데도 무조건 보습을 감량하기보다 현재 건조감과 편안함을 함께 살펴 사용 방법을 검토해요. [kb:B-M02@0.6.1]

### 근거 및 이유
따가움은 없다고 보고했으므로 이를 만들어내지 않아요. 건조 관찰과 무조건 감량 행동은 별도로 확인됐어요.

### 확인이 필요한 한계
건조의 원인이나 필요한 정확한 사용량은 알 수 없어요.

## syn-sol-0216 — 과거 체감과 현재 미상

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `baa0265987259bfa1a8f0fe5b6035938141d7c09f70d2c392236bcc80e06de1d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

과거 체감으로 현재 수온을 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.water_temperature": {
      "variable_id": "method.water_temperature",
      "state": "known",
      "value": {
        "past_perceived_hot": true,
        "current_temperature_unknown": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "과거 체감으로 현재 수온을 추정하지 않아요."
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
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
과거 체감으로 현재 수온을 추정하지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
확인되지 않은 정보를 임의로 채우면 관찰과 다른 판단이 될 수 있어요.

### 확인이 필요한 한계
빠진 정보나 적용되는 제품 지시를 확인하기 전에는 부합 여부를 확정하지 않아요.

## syn-sol-0218 — 친구의 재도포와 본인 기록

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `5f0ea8e16ed57769103959f635c1c28d7d3ba656e15835d8cb62d72b41152dca`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 재도포 기록은 확인되지만 본인의 재도포는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "self_prolonged": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "one_record": "reapplied",
        "record_subject": "friend",
        "self_record": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "친구의 재도포 기록은 확인되지만 본인의 재도포는 미상이에요."
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
친구의 재도포 기록은 확인되지만 본인의 재도포는 미상이에요 [kb:B-P03@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0220 — 본인 활동 종료와 친구의 지속 노출

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `340685b612bc5a9ebc6bef0c8cdaf6516c9da2156ec7fcee2560e2d1f0fe8d72`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인의 활동 중 재도포 여부는 미상이며 친구의 현재 행동으로 대신 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "self_activity": "ended",
        "friend_activity": "ongoing"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "self_during_exposure": "unknown",
        "friend_reapplied": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "본인의 활동 중 재도포 여부는 미상이며 친구의 현재 행동으로 대신 판단하지 않아요."
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
본인의 활동 중 재도포 여부는 미상이며 친구의 현재 행동으로 대신 판단하지 않아요 [kb:B-P03@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0224 — 수건 접촉과 본인 재도포 기록

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `0731664c2baeea5165760e3f143b159c87d5d3a9a86b9910da11caaddb9abbc7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인의 수건 접촉과 재도포하지 않은 기록은 확인되지만 둘의 시간 순서는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "self_outdoors": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.towel_contact": {
      "variable_id": "sun.towel_contact",
      "state": "known",
      "value": {
        "self_contact": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "self_reapplied": false,
        "friend_reapplied": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "본인의 수건 접촉과 재도포하지 않은 기록은 확인되지만 둘의 시간 순서는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S05",
      "text": "FDA guidance recommends reapplying sunscreen at least every two hours and more often after swimming or sweating.",
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
본인은 수건에 접촉했고 재도포하지 않았다고 보고했지만 두 사실의 시간 순서는 미상이에요. [kb:B-P03@0.6.1]

### 근거 및 이유
미국 식품의약국은 수영이나 땀을 흘린 뒤 더 자주 재도포하도록 안내해요. [ref:S05]

### 확인이 필요한 한계
친구의 재도포 기록으로 본인의 접촉 이후 행동을 확정하지 않아요.

## syn-sol-0226 — 본인의 밀림과 동행인의 사용 감소

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `8e6a6bb12520030c1d788213abf290a0c570b0ea8b6c5dfff7b1a684fa03307e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인의 밀림은 사용성 검토 대상이지만 본인의 사용이나 재도포 감소는 확인되지 않았어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "self_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "self_use_reduced": false,
        "companion_use_reduced": true,
        "self_reapplication_omitted": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "exception",
      "guidance": "본인의 밀림은 사용성 검토 대상이지만 본인의 사용이나 재도포 감소는 확인되지 않았어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "A laboratory study used ultraviolet reflectance photography to examine selected sunscreen and moisturizer application sequences.",
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
본인의 밀림은 사용성 검토 대상이지만 본인의 사용이나 재도포 감소는 확인되지 않았어요 [kb:B-I02@0.6.1].

### 근거 및 이유
제한된 제품 조합을 자외선 반사 영상으로 살핀 실험이 있어요 [ref:S09].

### 확인이 필요한 한계
관련 조건을 따로 확인하고 다른 대상의 정보로 대신하지 않아요.

## syn-sol-0228 — 이전 제품의 반복 눈시림

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `17ed6454822c2c680cd67f0cc98cc6c68b70601f65fa562c9bc9c956131ae18f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 제품의 반복 눈시림은 확인되지만 현재 제품의 경험은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "product_a_repeated": true,
        "product_b_experience": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "current_product": "product_b",
        "product_a_discontinued": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "이전 제품의 반복 눈시림은 확인되지만 현재 제품의 경험은 미상이에요."
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

### 핵심 안내
이전 제품의 반복 눈시림은 확인되지만 현재 제품의 경험은 미상이에요 [kb:B-P06@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0231 — 보습제 누락과 선제품 기록

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `9b1bd4ac756e5cb1ee57ecb2ed242ba7ace0b941575e2cb157931398814fa379`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제의 귀 도포 누락만으로 선제품의 귀 도포 여부를 판단할 수 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.exposed_sites": {
      "variable_id": "sun.exposed_sites",
      "state": "known",
      "value": [
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
        "moisturizer_ears_omitted": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "보습제의 귀 도포 누락만으로 선제품의 귀 도포 여부를 판단할 수 없어요."
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
보습제의 귀 도포 누락만으로 선제품의 귀 도포 여부를 판단할 수 없어요 [kb:B-P02@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0234 — 다른 날 기록과 야외 계획

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `3f52089fcb30380be711462a738f785fa2a591ba02060d7f717d8d497d2f2cab`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 날의 재도포 기록만으로 계획된 활동의 실제 노출과 행동을 확인할 수 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.outdoor_time": {
      "variable_id": "sun.outdoor_time",
      "state": "known",
      "value": {
        "planned_outdoor_activity": true,
        "actual_outdoor_exposure": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "sun.reapplication": {
      "variable_id": "sun.reapplication",
      "state": "known",
      "value": {
        "reapplied_on_another_day": true,
        "during_planned_activity": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "다른 날의 재도포 기록만으로 계획된 활동의 실제 노출과 행동을 확인할 수 없어요."
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
다른 날의 재도포 기록만으로 계획된 활동의 실제 노출과 행동을 확인할 수 없어요 [kb:B-P03@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0238 — 다른 제품의 내수성 표시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `5feeeaa50e347f9b3a5284ee666dc27f7b7379feb048fa17e8dec47a5189f314`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 제품의 표시로 실제 사용 제품의 제거 행동을 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "product.water_resistance": {
      "variable_id": "product.water_resistance",
      "state": "known",
      "value": {
        "product_a_labeled": false,
        "product_b_labeled": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "used_product": "product_b",
        "product_b_removal_behavior": "unknown"
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "다른 제품의 표시로 실제 사용 제품의 제거 행동을 판단하지 않아요."
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

### 응답 초안 — 미승인

### 핵심 안내
다른 제품의 표시로 실제 사용 제품의 제거 행동을 판단하지 않아요 [kb:B-I01@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0239 — 밀림과 별도 일정에 따른 사용 감소

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `fa570fafc9f6a9f571e6ed4d9b9c12ae2302119ae386873dc1fc74873606ebef`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

밀림과 사용 감소가 함께 있어도 보고된 감소 이유는 일정이며 밀림 때문이라고 단정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "sun.pilling": {
      "variable_id": "sun.pilling",
      "state": "known",
      "value": {
        "self_present": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "sunscreen_use_reduced": true,
        "reason": "schedule",
        "reduction_due_to_pilling": false
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I02",
      "status": "unknown",
      "guidance": "밀림과 사용 감소가 함께 있어도 보고된 감소 이유는 일정이며 밀림 때문이라고 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S09",
      "text": "A laboratory study used ultraviolet reflectance photography to examine selected sunscreen and moisturizer application sequences.",
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
밀림과 사용 감소가 함께 있어도 보고된 감소 이유는 일정이며 밀림 때문이라고 단정하지 않아요 [kb:B-I02@0.6.1].

### 근거 및 이유
제한된 제품 조합을 자외선 반사 영상으로 살핀 실험이 있어요 [ref:S09].

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0241 — 친구 용기의 냄새 변화

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `93120137ab7349f869d96cbb1aa90ce41d8925ea9207df51dbbd793b42eaf397`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구 용기의 냄새 변화는 확인됐지만 본인 용기의 감각 변화는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "storage.sensory_change": {
      "variable_id": "storage.sensory_change",
      "state": "unknown",
      "value": null,
      "source": "synthetic_fixture",
      "confirmed_by_user": false
    },
    "storage.expiry": {
      "variable_id": "storage.expiry",
      "state": "known",
      "value": {
        "self_container_printed_date_not_passed": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "friend_container_new_odor": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P08",
      "status": "unknown",
      "guidance": "친구 용기의 냄새 변화는 확인됐지만 본인 용기의 감각 변화는 미상이에요."
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
친구 용기의 냄새 변화는 확인됐지만 본인 용기의 감각 변화는 미상이에요 [kb:B-P08@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.

## syn-sol-0242 — 친구의 눈가 불편과 본인의 경험

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `cb0d9db44c23a987265a37cbf7041c4b6f18128891c3a23c3eace4de5a5fd385`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 반복 불편과 보호 행동은 본인의 경험이나 대안을 확인해 주지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "skin.eye_stinging": {
      "variable_id": "skin.eye_stinging",
      "state": "known",
      "value": {
        "self_repeated": "unknown",
        "friend_repeated": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": {
        "protective_eyewear": "unknown",
        "friend_avoids_eye_area": true
      },
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P06",
      "status": "unknown",
      "guidance": "친구의 반복 불편과 보호 행동은 본인의 경험이나 대안을 확인해 주지 않아요."
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

### 핵심 안내
친구의 반복 불편과 보호 행동은 본인의 경험이나 대안을 확인해 주지 않아요 [kb:B-P06@0.6.1].

### 근거 및 이유
확인된 사실과 확인되지 않은 항목을 분리해 살펴요.

### 확인이 필요한 한계
해당 대상에 연결된 정보를 확인하기 전에는 미상으로 남겨요.
