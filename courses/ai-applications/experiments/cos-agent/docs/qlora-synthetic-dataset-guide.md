# Ppopy QLoRA (`Qwen 3.5 4B`) 합성 데이터셋 구축 및 `v67` 재가공 가이드

> **대상**: 합성 데이터 생성·재가공·검수에 참여하는 팀원 전원  
> **기준 아키텍처**: [Ppopy End-to-End Architecture v3](end-to-end-architecture-draft.md) (`3-Stage Schema NLU + Control Plane + Myopic VOI AFA + Local Reference Vector RAG + QLoRA SFT-SLM + Safety Guardrail`)  
> **핵심 전제**: v3에서 추가 질문 턴은 **정형 KB 질문 + 선택지 버튼(0ms Fast Path)**으로 처리하므로, **SLM `QUESTION_MODE` 데이터는 생성하지 않습니다.** QLoRA 학습은 `SOLUTION_MODE`와 `HOLD_MODE`(및 선택적 `NLU_MODE` 어댑터)에만 집중합니다.  
> **필수 경계 (`AGENTS.md`)**: 모든 데이터는 `development_preview`, `production_enabled=false`, **합성 입력 전용**입니다. 실제 사용자 개인정보·설문·연락처·제3자 원문 PDF/게시글을 포함하지 않으며, 임상 승인·피부 진단·자동 개선 판정 표현을 금지합니다.

---

## 1. 왜 공통 기준이 필요한가?

4B급 소형 모델(`Qwen 3.5 4B`)의 QLoRA SFT는 **데이터의 양보다 일관성과 규칙 준수율**이 성능을 좌우합니다.  
팀원들이 각자 다른 AI(GPT, Claude, Gemini 등)로 제각각 말투·인용 형식·보류 기준을 섞어 생성하면 모델이 **스타일 충돌(Style Conflict)과 지시 불이행**을 일으킵니다.

따라서 이 문서의 **공통 스키마 · Teacher Prompt · 교차 검수 · 자동 검증 게이트**를 모든 팀원이 동일하게 적용합니다.

---

## 2. QLoRA 목표 데이터셋 구성 및 권장 규모

총 **2,100 ~ 2,800턴**의 고품질(가드레일 100% 통과) 데이터셋을 1차 목표로 합니다. *(Multi-LoRA로 `NLU_MODE`를 별도 어댑터로 학습할 경우 NLU 1,000~1,500턴 추가)*

| 모드 (`mode`) | 목표 규모 | 모델 입력 (`input`) | 정답 출력 (`assistant`) | RAG 결합 여부 |
| --- | --- | --- | --- | --- |
| **`SOLUTION_MODE`** | **1,500~2,000턴** | 확정 User Context + 정형 KB 판정 + 버전 검증된 제품 표시 + **Reference 논문 RAG 청크(관련 + 방해 청크 혼합)** | 제공된 근거 ID(`[ref:...]`)만 인용한 루틴 제안·습관 조정·대체 후보 + 불확실성(`unknown`) 설명 | **O** |
| **`HOLD_MODE`** | **600~800턴** | 필수 안전 보류 / 정보 부족 / 제품 버전 불일치 / 진단 요청 입력 | 추천을 생략하고 **보류 사유 + 필요한 확인 사항 + 전문가 확인 안내**만 출력 | **X** |
| **`NLU_MODE`** *(별도 Multi-LoRA 어댑터)* | **1,000~1,500턴** | 사용자 자유 발화 + 직전 질문 문맥 + 카탈로그 제품명 힌트 + 활성 슬롯 스키마 | 표준 슬롯 JSON + 원문 근거 구절(`evidence_span`) | **X** |

> **`QUESTION_MODE` 제외**: v3에서 질문 턴은 정형 KB 질문 + 선택지 버튼으로 0ms 응답하므로, 질문 문장 생성용 SFT 데이터는 만들지 않고 그 예산을 `SOLUTION_MODE`·`HOLD_MODE` 품질에 100% 집중합니다.

### 필수 포함 비율: Hard Negative(방어 학습) **최소 25% 이상**
정상 케이스만 학습하면 실전에서 4B 모델이 쉽게 환각을 일으킵니다. 전체의 25% 이상은 반드시 아래 4종을 포함합니다:
1. **RAG 방해 청크(Distractor) 무시**: 관련 없는 논문 청크 2~3개를 일부러 섞어 넣고, 관련 없는 청크 ID는 인용하지 않게 학습.
2. **임상 수치 과잉 해석 차단**: 논문 청크에 *"8주 임상 40% 개선"* 같은 내용이 있어도 **치료·개선 효과를 단정하지 않고 일반 관리 원리로만 설명**.
3. **미상(`unknown`)·버전 불일치 보존**: 제품 버전이 안 맞거나 농도·pH가 비공개일 때 추측하지 않고 `unknown`·보류 유지.
4. **타인 경험·부정 표현 구분**: *"친구가 따갑대요"*, *"따갑진 않아요"*에서 오탐 보류하지 않는 사례.

---

## 3. 기존 `v67` 데이터셋 재가공(Recycling) 전략

기존 [data/action_policy/v67/](../data/action_policy/v67/README.md)의 자산은 **버리지 않고 100% 재활용**합니다.  
구 아키텍처의 `output`(액션 ID JSON)만 새 모드에 맞게 다시 생성(Re-labeling)하고, **1,025개 시나리오·발화·관찰·KB 근거·3분할 계보는 그대로 보존**합니다.

| 기존 `v67` 파일 / 턴 유형 | 재가공 대상 모드 | 재가공 방법 |
| --- | --- | --- |
| `canonical-candidates-v67.jsonl` (1,025 시나리오, KB 58종) | **`NLU_MODE`** + 신규 시나리오 시드 | 기존 `turns[].message`(발화)에서 상위 AI로 `표준 슬롯 JSON + evidence_span`을 추출하고, 기존 `user_events`·`must_preserve`와 자동 대조 검증 |
| `v67-sft-*.jsonl` 중 `ask_user` / `confirm_candidate` / `resolve_conflict` 턴 | *(QLoRA 학습 제외)* **Myopic AFA 평가 전용** | QLoRA 질문 문장 재라벨링을 하지 않고, Myopic AFA의 질문 선택·질문 수 절감 평가 및 버튼 UX 테스트에만 활용 |
| `v67-sft-*.jsonl` 중 `request_draft`(223턴) & `hold`(665턴) | **`SOLUTION_MODE`** & **`HOLD_MODE`** | 기존 `input.evidence`(KB 판정·출처 요약 `source:S03` 등)에 **Reference 논문 청크 + 보유 제품 표시**를 보강해 자연어 솔루션·보류 안내문 생성 |

> **분할 보존 절대 원칙 (Data Leakage 방지)**  
> `v67`에 이미 정의된 `split` (`train` / `val_internal` / `test_internal`)과 `group_id` · `scenario_family_id` · `product_family_id` 계보를 **절대 섞지 마세요.**  
> `test_internal`에 속한 시나리오는 학습 데이터 생성·프롬프트 튜닝에 절대 사용하지 않습니다.

---

## 4. 신규 추가 생성 집중 영역 (`v67`에 부족한 부분)

팀원들의 AI를 투입해 아래 4가지 영역을 신규 생성하여 3개 축 균형을 맞춥니다:

1. **세정(C)·보습(M)·자외선차단(P) 3영역 균형 + 교차 시나리오**
   - `KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json` 및 `sunscreen_removal_review.json` 기반
   - 특히 **`B-I01` 내수성 선크림 세정**, 레티노이드·각질관리 중첩(`B-G13`~`B-G15`, `B-I04`), 세안 후 보습 연계(`B-M01`~`B-M03`)
2. **외부 데이터(날씨·자외선 지수) 결합 시나리오**
   - 고자외선·장시간 야외 체류·땀/물놀이(`B-P01`~`B-P04`)와 보유 제품 조합
3. **제품 버전 불일치 & 대체품 후보 제시 시나리오**
   - 카탈로그에 `v1.0`만 있고 사용자 보유품이 `v2.0`일 때 사용 보류(`usage_held`) + 대체 후보(`alternative_candidate`) 안내
4. **Reference 논문 RAG Grounding + Distractor 무시 시나리오**
   - 관련 논문 청크 2개 + 무관한 방해 청크 2개를 함께 입력하고, 관련 청크 ID만 정확히 인용하는 사례

---

## 5. 팀원 공통 JSONL 스키마

모든 팀원이 생성한 데이터는 아래 단일 JSONL 형식으로 제출합니다 (1줄 = 1샘플).

```json
{
  "id": "syn-v2-sol-0001",
  "scenario_id": "new-bi01-001",
  "group_id": "new-group-bi01-001",
  "split": "train",
  "mode": "solution",
  "domains": ["cleansing", "sun_protection"],
  "card_ids": ["B-I01", "B-C05"],
  "is_hard_negative": true,
  "hard_negative_type": "rag_distractor_and_unknown_concentration",
  "messages": [
    {
      "role": "system",
      "content": "(공통 시스템 프롬프트)"
    },
    {
      "role": "user",
      "content": "(구조화된 Context + KB 판정 + 제품 표시 + 제공된 RAG 청크 JSON)"
    },
    {
      "role": "assistant",
      "content": "(정답 자연어 응답 — 제공된 [ref:ID]만 인용, 불확실성 명시)"
    }
  ],
  "allowed_evidence_refs": ["kb:B-I01@0.6.1", "ref:AAD-sunscreen-01", "catalog:cleanser-a@1.0"],
  "distractor_refs": ["ref:unrelated-moisturizer-09"],
  "provenance": {
    "source_origin": "new_synthetic",
    "generator_model": "gpt-5 / claude-sonnet / gemini-2.5-pro 등 실제 모델명",
    "critic_model": "교차 검수한 다른 AI 모델명",
    "passed_python_gate": true,
    "human_review": "unreviewed"
  }
}
```

> **학습 시 주의**: QLoRA 학습 포맷으로 변환할 때는 `messages` 필드만 사용하고, `provenance`·`id`·`is_hard_negative` 같은 메타데이터는 모델 프롬프트에 넣지 않습니다. Loss는 `assistant` 응답 토큰과 종료 토큰에만 적용(User/System 마스킹)합니다.

---

## 6. 팀원 공통 Teacher Prompt 템플릿

팀원마다 다른 AI를 쓰더라도 **아래 프롬프트를 그대로 사용**해 말투·인용 형식·안전 경계를 통일합니다.

### A. `SOLUTION_MODE` / `HOLD_MODE` 생성용 Teacher Prompt
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'의 학습 데이터 생성기입니다.
주어진 JSON 입력(사용자 확정 관찰, 보유 제품 표시 사용법, 정형 KB 판정, 제공된 Reference 문헌 청크)만 사용해 한국어 응답을 작성하세요.

[절대 규칙]
1. 입력의 `allowed_evidence_refs`에 포함된 근거만 사용하고, 문장 끝에 `[ref:ID]` 형식으로 인용하세요. 제공되지 않은 ID는 절대 인용하지 마세요.
2. `distractor_refs`(무관한 방해 청크)의 내용은 무시하고 인용하지 마세요.
3. 피부 질환 진단, 치료/임상 효과 단정("트러블이 40% 개선됩니다" 등), 미공개 성분 농도·pH 추측을 절대 하지 마세요.
4. 확인되지 않은 제품 버전이나 미상(`unknown`) 값은 추측하지 말고 "확인되지 않음"으로 명시하세요.
5. 입력이 `mode="hold"`이거나 필수 안전 보류(통증·지속 불편·품질 이상)인 경우, 개별 루틴/제품 추천을 절대 작성하지 말고 보류 사유와 전문가 확인 안내만 간결하게 작성하세요.
6. 어조는 차분하고 친절한 존댓말(~해요 / ~합니다 중 하나로 일관 유지), 구조는 ① 핵심 안내 → ② 근거 및 이유(`[ref:ID]`) → ③ 확인이 필요한 한계/불확실성 순으로 작성하세요.
```

### B. `NLU_MODE` 생성용 Teacher Prompt (Multi-LoRA 어댑터 학습 시)
```text
당신은 한국어 스킨케어 발화에서 정형 슬롯 후보를 추출하는 NLU 파서입니다.
입력으로 주어진 사용자 발화, 직전 질문 맥락, 카탈로그 제품명 힌트, 허용된 슬롯 스키마(variable_id / enum)만 보고 JSON을 반환하세요.

[절대 규칙]
1. 허용된 variable_id와 enum 값만 사용하세요. 목록에 없는 슬롯이나 값을 만들지 마세요.
2. 모든 추출 항목에 원문에서 그대로 복사한 `evidence_span`을 포함하세요.
3. 본인(`self`)과 타인(`other`)의 경험, 긍정(`affirmed`)과 부정(`denied`)을 정확히 구분하세요.
4. 문장에 명시되지 않은 내용은 추측하지 말고 생략하거나 `unknown`으로 두세요.
```

### C. Cross-Model `Critic` (교차 검수용) Prompt
```text
당신은 Ppopy 합성 데이터 품질 감사관입니다. 다른 AI가 생성한 학습 샘플(입력 JSON + assistant 응답)을 아래 6개 항목으로 엄격히 검수하고, PASS/FAIL과 위반 사유를 JSON으로 반환하세요.

1. 미제공 근거 ID 인용 또는 방해 청크(distractor) 인용 여부
2. 피부 질환 진단, 임상/치료 효과 단정, 자동 개선 판정 표현 여부
3. 미공개 농도/pH 추측 또는 버전 불일치 제품 사용법 채택 여부
4. HOLD 조건에서 개별 루틴/제품 추천을 누출했는지 여부
5. (NLU_MODE인 경우) `evidence_span` 원문 불일치 또는 본인/타인·긍정/부정 오분류 여부
6. 한국어 자연스러움 및 지정 어조 일관성

위반이 1건이라도 있으면 반드시 `"decision": "FAIL"`을 반환하세요.
```

---

## 7. 팀 협업 워크플로 (Generator ↔ Critic 교차 배치 + 자동 검증)

```text
[1. 시나리오 배정]   팀원별 영역 분담 (예: A=세정·B-I01, B=보습·중첩, C=자외선·날씨, D=v67 재가공·Hard Negative)
        │
        ▼
[2. 초안 생성]       공통 Teacher Prompt로 각 팀원의 AI(Generator)가 JSONL 생성
        │
        ▼
[3. 교차 AI 검수]    다른 팀원의 AI(Critic — 생성기와 다른 모델 계열 권장)로 6개 항목 검수 → FAIL 폐기/재생성
        │
        ▼
[4. Python 자동 게이트] 병합 전 자동 검증 스크립트 통과분만 채택:
                       ① JSON/Pydantic 스키마 100% 통과
                       ② allowed_evidence_refs 외 ID 인용 0건 / distractor 인용 0건
                       ③ 금지 키워드(진단·치료·농도 단정 등) 0건
                       ④ v67 val_internal / test_internal과 group_id·정규화 발화 중복 0건
        │
        ▼
[5. 버전 고정 병합]  data/qlora/v2/ (train / val / test 분리) + SHA-256 manifest 기록 후 QLoRA 학습 투입
```

### 팀원별 체크리스트 (제출 전 자가 점검)
- [ ] `test_internal` 시나리오가 `train` 생성에 섞이지 않았는가?
- [ ] Hard Negative(방해 청크·임상 수치 절제·버전 불일치·타인/부정)가 최소 25% 이상 포함되었는가?
- [ ] 모든 샘플에 `allowed_evidence_refs`, `provenance(generator_model, critic_model)`가 기록되었는가?
- [ ] 개인정보, 실제 사용자 설문, 제3자 원문 PDF 텍스트가 포함되지 않았는가?
