# Ppopy QLoRA (`Qwen 3.5 4B`) 합성 데이터셋 구축 가이드 (3인 병렬 · 에이전트 실행 명세)

> **문서 목적**: 서로 다른 3명의 팀원 에이전트(Codex 등)가 **이 문서와 기준 커밋의 공통 검증기**만으로 동일한 스키마·판정 근거·품질 기준의 합성 데이터셋을 제작·병합하도록 정의합니다.  
> **기준 아키텍처**: [Ppopy End-to-End Architecture v3](end-to-end-architecture-draft.md) · [v3_contracts.py](../beauty_agent/v3_contracts.py) · [validate_qlora_dataset.py](../scripts/validate_qlora_dataset.py)  
> **필수 경계 (`AGENTS.md`)**: `development_preview`, `production_enabled=false`, **합성 입력 전용**. 실제 사용자 개인정보·설문·연락처·제3자 원문 PDF/게시글 금지. 피부 질환 진단·임상/치료 효과 단정·자동 개선 판정·미공개 농도/pH 추정 금지. `QUESTION_MODE` 데이터는 생성하지 않습니다(0ms Quick Reply 버튼 처리).

---

## 0. 작업 순서 요약 (6단계 · 에이전트 필독)

모든 팀원 에이전트는 아래 6단계를 순서대로 실행합니다. **대량 생성 전 반드시 3단계(36턴 파일럿 병합 검증)를 통과해야 합니다.**

| 단계 | 작업 내용 | 필수 입력 / 실행 명령 | 통과 조건 |
| --- | --- | --- | --- |
| **1. 할당 확인** | 본인 Shard(`a`/`b`/`c`), 브랜치, 출력 경로 확인 | 2절 분담표 + Linear Sub-issue | `main` 직접 작업 금지, 담당 브랜치 체크아웃 |
| **2. 기준 파일 동기화** | `v3_contracts.py`, `KB v0.6.1`, `validate_qlora_dataset.py` 읽기 | `KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json`, `sunscreen_removal_review.json`, (A만) `data/action_policy/v67/` | 변수 타입·카드 ID·`source_registry` 원본 메타데이터 확인 |
| **3. 파일럿 생성 (12턴/인)** | 정상 안내·보류·정보 미상·방해 근거 각 3턴씩 **12턴** 먼저 생성 | ① 시나리오·기대 판정 고정 → ② 답변 생성 (5절 절차) | `data/qlora/v2/shards/shard_*.jsonl` 12줄 기록 |
| **4. 공통 검증 (단독 + 병합)** | 단독 검증 후 3개 파일 합쳐 **36턴 병합 검증** | `uv run --locked python scripts/validate_qlora_dataset.py --input ... --pilot` | `error_count == 0` (`passed: true`) |
| **5. 교차 검수 (Critic)** | 옆 팀원의 다른 AI 모델로 구조화 Critic 검수 + 고위험 표본 사람 검수 | 6절 B Critic Prompt (`row_id`, `violated_rule`, `offending_span`, `evidence_ref`) | FAIL 0건, 필수 보류·버전 불일치 표본 사람 확인 |
| **6. 본 생성 및 PR 제출** | 파일럿 오류를 반영한 뒤 목표 수량 생성 → 최종 검증 → PR | `--shard {a\|b\|c}` + 최종 `--merge --enforce-ratios` | `error_count == 0`, `KB/`·코어 코드 미수정 |

---

## 1. 목표 규모 및 비율 기준 (분모 명시)

1차 통합 QLoRA 어댑터(`solution-hold-lora`)는 **`solution` 1,600턴 + `hold` 500턴 = 총 2,100턴**을 목표로 합니다. *(2순위 `nlu` Multi-LoRA 1,000~1,500턴은 1차 완료 후 별도 진행)*

| 지표 | 목표 기준 | 정확한 분모 (검증기 계산식) |
| --- | --- | --- |
| **`hold` 비율** | **20% ~ 25%** *(목표 500 / 2,100 = **23.8%**)* | 전체 제출 행(`total_rows`) 대비 `mode == "hold"` 행 비율 |
| **Hard Negative 비율** | **≥ 25%** | 전체 제출 행(`total_rows`) 대비 `is_hard_negative == true` 행 비율 |
| **영어 문헌 청크 비율** | **30% ~ 40%** | `mode == "solution"` 행(`solution_rows`) 중 **실제 `allowed_evidence_refs`에 포함된 영어 청크**를 사용한 행 비율 *(방해 청크만 영어인 행은 제외)* |
| **`v67` 재가공 가용 풀** | `request_draft` 183턴(`train` 145, `val` 38) · `hold` 616턴(`train` 566, `val` 50) | `v67-sft-test-internal.jsonl` 제외 후 재검증 전 후보 수 |

### Hard Negative 4종 (`hard_negative_type` 고정 enum)
1. `rag_distractor_ignore`: 무관한 문헌 청크를 `distractor_refs`로 섞고 응답에서 절대 인용·언급하지 않음.
2. `clinical_restraint`: 임상 수치·소규모 연구 청크가 들어와도 치료·개선 수치를 단정하지 않고 일반 관리 원리와 한계만 설명.
3. `version_mismatch_or_unknown`: 제품 버전 불일치(`usage_held`)·비공개 농도/pH를 추측하지 않고 `unknown` 또는 보류 유지.
4. `negation_or_other_subject`: 타인 경험(*"친구가 따갑대요"*)·명시적 부정(*"따갑진 않아요"*)에서 오탐 `hold` 금지.

---

## 2. 3인 병렬 작업 분담표 & `v67` 분할 규칙

| 담당 | 브랜치 / 출력 경로 | ID 접두사 | 담당 범위 (`KB v0.6.1`) | 목표량 (`solution` / `hold`) | Critic 담당 |
| --- | --- | --- | --- | --- | --- |
| **팀원 1 (Shard A)** | `data/qlora-shard-a`<br>`data/qlora/v2/shards/shard_a_cleansing.jsonl` | `syn-a-sol-0001`~<br>`syn-a-hold-0001`~ | 세정(`B-C01`~`B-C06`) + `B-I01`(내수성 선크림 세정) + `v67` `request_draft`/`hold` 재가공 | `600` / `200` *(파일럿 9 / 3)* | 팀원 2 AI |
| **팀원 2 (Shard B)** | `data/qlora-shard-b`<br>`data/qlora/v2/shards/shard_b_moisturizing.jsonl` | `syn-b-sol-0001`~<br>`syn-b-hold-0001`~ | 보습(`B-M01`~`B-M05`) + 활성성분/각질 중첩(`B-G13`~`15`, `B-I04`) + 새 제품 도입(`B-G11`~`12`) | `500` / `150` *(파일럿 9 / 3)* | 팀원 3 AI |
| **팀원 3 (Shard C)** | `data/qlora-shard-c`<br>`data/qlora/v2/shards/shard_c_sun_product.jsonl` | `syn-c-sol-0001`~<br>`syn-c-hold-0001`~ | 자외선차단(`B-P01`~`09`, `B-P07` 제외) + 날씨/UV 결합 + 버전 불일치·대체품 + 보관/품질 보류(`B-S*`) | `500` / `150` *(파일럿 9 / 3)* | 팀원 1 AI |

### 분할(`split`) 및 `v67` 누수 차단 규칙 (충돌 해소 확정안)
1. **실제 분할 기준**: `canonical-candidates-v67.jsonl`의 `split` 표기(전원 `train`)를 쓰지 말고, 반드시 **`v67-sft-train.jsonl` / `v67-sft-val-internal.jsonl` / `v67-sft-test-internal.jsonl`의 `scenario_id`·`group_id`**로 실제 분할을 판별합니다.
2. **`test_internal` 절대 금지**: `v67-sft-test-internal.jsonl`에 속한 `scenario_id`·`group_id`는 재가공·변형 시드 모두 0건이어야 합니다.
3. **같은 분할 내 원본–파생 보존 허용**: `v67` `val_internal` 행을 재가공할 때는 `split: "val_internal"`과 원본 `group_id`, `provenance.source_scenario_id`를 그대로 유지합니다. (`val_internal` 원본을 `train`에 넣거나 `train` 원본을 `val_internal`에 넣는 **교차 분할 이동만 차단**합니다.)
4. **신규 합성(`provenance.source_origin == "new_synthetic"`)**: `group_id` 단위로 `train` 90% / `val_internal` 10% 배분하며, 같은 `group_id`·`scenario_id`·정규화 답변이 두 분할에 동시에 나타나면 안 됩니다.

---

## 3. KB에 등록된 출처와 확인 범위 (`KB v0.6.1` `source_registry`)

`rag_chunks[]`의 `source_url`, `locator`, `checked_on`, `limitations`는 **절대 손으로 작성하지 말고 `KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json`의 `source_registry` 원본 값을 그대로 복사**합니다. (`validate_qlora_dataset.py`가 4개 필드를 원본과 문자열 단위로 대조합니다.)

### 청크 출처 이중 분류 (`chunk_origins` 필수 필드)
에이전트가 작성한 방어 시험 문장이 실제 문헌의 검증된 주장으로 섞이지 않도록, 모든 `rag_chunks[].evidence_ref`에 대해 행의 `chunk_origins`에 아래 둘 중 하나를 명시합니다:
- **`kb_source_summary`**: `source_registry`의 `review_scope`·`limitations` 범위 안에서만 요약한 근거 청크.
- **`synthetic_defense_probe`**: 방해 청크(`distractor_refs`) 또는 임상 과잉 주장 차단(`clinical_restraint`) 등 **모델의 방어 행동을 시험하기 위한 합성 청크**. 이 청크에 포함된 문장이나 수치는 실제 문헌의 검증된 효능으로 인용·단정하지 않습니다.

| 영역 | 허용 `evidence_ref` | KB 등록 출처 요약 (`source_registry`) |
| --- | --- | --- |
| **세정 (C)** | `ref:S03`, `ref:S07`, `ref:S08` | AAD 세안 기본(`S03`), 세정제 pH·조성(`S07`), 20명 선크림 세정 비교(`S08`) |
| **보습 (M)** | `ref:S04`, `ref:S20`, `ref:S21`, `ref:S23`~`S25`, `ref:S29` | AAD 건조 피부·손 보습·습식 면도·무향료 선택 |
| **자외선차단 (P)** | `ref:S05`, `ref:S09`, `ref:S14`, `ref:S16`~`S18` | FDA/AAD SPF 30+·광범위·재도포·비제품 광보호, 보습+선크림 UV 반사 영상(`S09`), 눈가·폐기 |
| **공통·병용·도입 (G/I)** | `ref:S15`, `ref:S26`, `ref:S32`~`S35` | FDA 알레르겐(`S15`), 팩/레티노이드 각질 중첩(`S26`,`S32`), DailyMed 병용 자극(`S33`,`S34`), 소부위 확인(`S35`) |
| **임상 절제 방어 시험** | `ref:S10`~`S13` | 수면(`S10`)·스트레스(`S11`)·저혈당식이 32명 RCT(`S12`)·아토피 설명(`S13`) — 인과·진단·개선 수치 단정 차단 전용 |
| **보관·품질·안전 (S/L/H)** | `ref:S06`, `ref:S27`, `ref:S36`~`S41` | FDA 보관·미생물 안전, HPRA/식약처 가품·회수 보류, 접촉 마찰, 눈 노출 세척(`S41`) |

> **금지 ID**: `U01`~`U09`, `D01`~`D04`, `F01`, `F02`, `S30`, `S31`, `B-P07`.

---

## 4. 고정 시스템 프롬프트 & 공통 검증을 통과한 기준 예제

### A. 고정 `messages[0].content` (`SYSTEM_PROMPT_SOLUTION_HOLD`) — 1글자도 변경 금지
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON(confirmed_observations, kb_judgments, product_evidence, rag_chunks, allowed_evidence_refs)만 근거로 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, distractor_refs는 무시하세요. 피부 질환 진단, 임상·치료 효과 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 "hold"이면 개별 루틴이나 제품 추천 없이 보류 사유와 필요한 확인·전문가 상담 안내만 작성하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요.
```

### B. 기준 예제 1 — `solution` 완성 행 (`validate_qlora_dataset.py` 단위 테스트 연동)
- `cleansing.steps`는 KB `value_type: "integer"`에 맞춰 정수 `1`을 사용하며, 세안 대상·방식은 `cleansing.target_load`(`structured`)에 기록합니다.
- 제품 정보는 실제 제품 시험을 임의로 적지 않고 `"synthetic_product": true` 합성 제품 표시 예시로 한정합니다.
- `S08`, `S21`의 `source_url`, `locator`, `checked_on`, `limitations`는 `Poppy_KB_seed_v0.6.1.json` 원본 값입니다.

```json
{
  "id": "syn-a-sol-0001",
  "scenario_id": "new-bi01-001",
  "group_id": "new-group-bi01-001",
  "scenario_family_id": "bi01-water-resistant-sunscreen",
  "split": "train",
  "mode": "solution",
  "domains": ["cleansing", "sun_protection"],
  "card_ids": ["B-I01", "B-C05"],
  "is_hard_negative": true,
  "hard_negative_type": "rag_distractor_ignore",
  "chunk_origins": {
    "ref:S08": "kb_source_summary",
    "ref:S21": "synthetic_defense_probe"
  },
  "messages": [
    {
      "role": "system",
      "content": "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON(confirmed_observations, kb_judgments, product_evidence, rag_chunks, allowed_evidence_refs)만 근거로 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, distractor_refs는 무시하세요. 피부 질환 진단, 임상·치료 효과 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 \"hold\"이면 개별 루틴이나 제품 추천 없이 보류 사유와 필요한 확인·전문가 상담 안내만 작성하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요."
    },
    {
      "role": "user",
      "content": "{\"mode\":\"solution\",\"confirmed_observations\":{\"cleansing.steps\":{\"variable_id\":\"cleansing.steps\",\"state\":\"known\",\"value\":1,\"source\":\"user_report\",\"confirmed_by_user\":true},\"cleansing.target_load\":{\"variable_id\":\"cleansing.target_load\",\"state\":\"known\",\"value\":{\"water_resistant_sunscreen\":true,\"method\":\"cleansing_water_only\"},\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[{\"card_id\":\"B-I01\",\"status\":\"difference\",\"guidance\":\"내수성 자외선차단제를 1단계 클렌징 워터로만 닦으면 잔여물이 남을 수 있습니다.\"}],\"product_evidence\":[{\"product_id\":\"syn-sun-001\",\"version\":\"1.0\",\"synthetic_product\":true,\"label_guidance\":\"합성 제품 표시 예시: 폼 클렌저 1회 세안 확인\",\"evidence_ref\":\"catalog:syn-sun-001@1.0\"}],\"rag_chunks\":[{\"evidence_ref\":\"ref:S08\",\"text\":\"In a 20-subject imaging study comparing water, facial cleanser, and cleansing oil, water alone left more sunscreen residue than cleanser or cleansing oil.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995\",\"locator\":\"Abstract: Methods / Results / Conclusion\",\"checked_on\":\"2026-11-04\",\"limitations\":\"제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호.\"},{\"evidence_ref\":\"ref:S21\",\"text\":\"Apply fragrance-free hand cream or ointment immediately after hand washing to help relieve dry hands.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands\",\"locator\":\"손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.\",\"checked_on\":\"2026-11-04\",\"limitations\":\"다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다.\"}],\"allowed_evidence_refs\":[\"kb:B-I01@0.6.1\",\"catalog:syn-sun-001@1.0\",\"ref:S08\"],\"distractor_refs\":[\"ref:S21\"]}"
    },
    {
      "role": "assistant",
      "content": "### 핵심 안내\n내수성 선크림을 1단계 클렌징 워터로만 닦으면 잔여물이 남을 수 있어요. 저녁에는 합성 제품 표시 예시에서 확인된 클렌징폼 1회 세안으로 조정해 보실 수 있어요 [kb:B-I01@0.6.1] [catalog:syn-sun-001@1.0].\n\n### 근거 및 이유\n20명 대상 제한된 제품 조합 영상 비교 연구에서도 물 세안만으로는 자외선차단제 잔여가 더 남고 세정제나 클렌징 오일 사용 시 제거가 나아지는 경향이 보고됐어요 [ref:S08].\n\n### 확인이 필요한 한계\n위 문헌은 소규모 제한 조합 기준이며 모든 내수성 제품에 일반화되지는 않아요. 세안 후 당김이나 자극이 반복되면 세정 방식을 줄이고 확인이 필요해요."
    }
  ],
  "allowed_evidence_refs": ["kb:B-I01@0.6.1", "catalog:syn-sun-001@1.0", "ref:S08"],
  "distractor_refs": ["ref:S21"],
  "provenance": {
    "source_origin": "new_synthetic",
    "source_scenario_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "human_review": "unreviewed"
  }
}
```

### C. 기준 예제 2 — `hold` 완성 행 (`validate_qlora_dataset.py` 단위 테스트 연동)
```json
{
  "id": "syn-a-hold-0001",
  "scenario_id": "new-bb01-001",
  "group_id": "new-group-bb01-001",
  "scenario_family_id": "bb01-persistent-pain",
  "split": "train",
  "mode": "hold",
  "domains": ["general_safety"],
  "card_ids": ["B-B01"],
  "is_hard_negative": false,
  "hard_negative_type": null,
  "chunk_origins": {},
  "messages": [
    {
      "role": "system",
      "content": "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON(confirmed_observations, kb_judgments, product_evidence, rag_chunks, allowed_evidence_refs)만 근거로 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, distractor_refs는 무시하세요. 피부 질환 진단, 임상·치료 효과 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 \"hold\"이면 개별 루틴이나 제품 추천 없이 보류 사유와 필요한 확인·전문가 상담 안내만 작성하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요."
    },
    {
      "role": "user",
      "content": "{\"mode\":\"hold\",\"confirmed_observations\":{\"skin.current_discomfort\":{\"variable_id\":\"skin.current_discomfort\",\"state\":\"known\",\"value\":\"persistent\",\"source\":\"user_report\",\"confirmed_by_user\":true},\"skin.pain\":{\"variable_id\":\"skin.pain\",\"state\":\"known\",\"value\":\"moderate\",\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[{\"card_id\":\"B-B01\",\"status\":\"hold\",\"guidance\":\"지속적인 불편감과 통증이 있어 개별 루틴 권고를 보류하고 전문가 확인을 우선 안내합니다.\"}],\"product_evidence\":[],\"rag_chunks\":[],\"allowed_evidence_refs\":[\"kb:B-B01@0.6.1\"],\"distractor_refs\":[]}"
    },
    {
      "role": "assistant",
      "content": "### 개별 권고 보류 안내\n현재 지속적인 불편감과 통증이 확인되어 개별 루틴 조정이나 제품 안내는 보류해요 [kb:B-B01@0.6.1].\n\n### 필요한 다음 단계\n불편감이 나타난 제품 사용은 잠시 중단하시고, 증상이 이어지거나 심해지면 피부과 전문의 등 전문가의 확인을 받아 주세요. 현재 상태의 원인 진단이나 처방은 안내해 드릴 수 없어요."
    }
  ],
  "allowed_evidence_refs": ["kb:B-B01@0.6.1"],
  "distractor_refs": [],
  "provenance": {
    "source_origin": "new_synthetic",
    "source_scenario_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "human_review": "unreviewed"
  }
}
```

### D. 추가 출력 스타일 참고 (임상 절제 · 버전 불일치 · 부정/타인)
- **임상 절제 (`clinical_restraint`, `chunk_origins["ref:S12"] = "synthetic_defense_probe"`)**: `S12`(경증–중등도 여드름 환자 32명 10주 식이중재 초록)와 방어 시험 청크가 함께 입력되어도 개선 수치를 인용·보장하지 않고 *"특정 질환·기간의 소규모 연구이며 개인별 원인 단정이나 치료 근거가 아니다"*로 제한하고 기본 세안 안내(`ref:S03`)만 제시합니다.
- **버전 불일치 (`version_mismatch_or_unknown`)**: 보유 제품 버전이 카탈로그와 다르면(`usage_held`) 개별 사용법을 보류하고, 비공개 농도·pH는 `unknown`으로 명시합니다.
- **부정/타인 경험 (`negation_or_other_subject`)**: 타인 증상(`subject="other"`)이나 본인의 명시적 부정(`denied`)에서는 불필요한 `hold`를 걸지 않고 정상 `solution`으로 진행합니다.

---

## 5. 2단계 생성 절차 (판정 오류 전파 차단)

입력 `mode`나 `kb_judgments`가 틀린 채로 답변만 생성하면 Critic이 통과시켜도 잘못된 학습 데이터가 됩니다. 반드시 아래 **2단계 순서**를 지킵니다:

1. **1단계 — 시나리오 및 기대 판정 고정**:
   - `KB v0.6.1`의 `baseline_cards` / `acceptance_scenarios` 또는 `v67-sft-{train|val-internal}.jsonl`의 검토된 사례를 근거로 `confirmed_observations`(KB 변수 타입 준수), `mode`, `kb_judgments`, `allowed_evidence_refs`, `rag_chunks`(`source_registry` 원본 복사)를 먼저 JSON으로 조립합니다.
2. **2단계 — 답변 문장 생성 및 즉시 검증**:
   - 확정된 1단계 입력 JSON과 4절 기준 예제를 Teacher Prompt에 넣어 `assistant` 응답만 생성하고, 바로 `validate_qlora_dataset.py`를 돌려 통과한 행만 저장합니다.

---

## 6. 공통 Teacher & 구조화 Critic Prompt

### A. `solution` / `hold` 답변 생성용 Teacher Prompt
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'의 학습 데이터 생성기입니다.
이미 확정된 입력 JSON(SLMRequest)만 보고 한국어 assistant 응답을 작성하세요.

[절대 규칙]
1. 입력의 allowed_evidence_refs에 포함된 ID만 [ID] 형식으로 인용하고, distractor_refs와 미제공 ID는 절대 인용하지 마세요.
2. chunk_origins가 synthetic_defense_probe인 청크의 문장·수치를 실제 검증된 임상 효능으로 단정하지 마세요.
3. 피부 질환 진단, 치료/임상 효과 단정, 미공개 성분 농도·pH 추측을 금지합니다.
4. 확인되지 않은 정보나 제품 버전 불일치는 미상(unknown) 또는 보류로 명시하세요.
5. mode="solution"은 '### 핵심 안내' → '### 근거 및 이유' → '### 확인이 필요한 한계' 3단 구조로 작성하세요.
6. mode="hold"는 개별 루틴/제품 추천·대체 후보를 절대 작성하지 말고 '### 개별 권고 보류 안내' → '### 필요한 다음 단계' 2단 구조로만 작성하세요.
7. 어조는 차분한 '~해요' 존댓말로 통일하세요.
```

### B. Cross-Model 구조화 `Critic` Prompt (교차 검수)
자기 모델 편향을 막기 위해 `provenance.critic_model`은 반드시 `provenance.generator_model`과 **다른 모델**을 사용하며, 아래 JSON 배열 형식으로 위반 근거를 반환받습니다. 필수 보류(`hold`)와 버전 불일치(`version_mismatch_or_unknown`) 사례는 팀원이 최소 10% 표본을 직접 육안 검수합니다.

```text
당신은 Ppopy 합성 데이터 품질 감사관입니다. 입력 JSON(SLMRequest)의 판정 정합성과 assistant 응답을 아래 6개 규칙으로 검수하고, 각 행마다 JSON으로 반환하세요:
{"row_id": "...", "decision": "PASS" | "FAIL", "violated_rule": null | "R1_CITATION" | "R2_CLINICAL" | "R3_UNKNOWN_VERSION" | "R4_HOLD_LEAK" | "R5_INPUT_JUDGMENT" | "R6_FORMAT_TONE", "offending_span": "...", "evidence_ref": "..."}

- R1_CITATION: 미제공·비표준([S99] 등) 인용 또는 distractor_refs 인용
- R2_CLINICAL: 피부 질환 진단, 임상/치료 효과 단정, synthetic_defense_probe 수치의 효능화
- R3_UNKNOWN_VERSION: 미공개 농도/pH 추측 또는 버전 불일치 제품 사용법 채택
- R4_HOLD_LEAK: mode="hold"에서 루틴/제품/대체 후보 추천 누출
- R5_INPUT_JUDGMENT: confirmed_observations와 mode/kb_judgments 자체의 모순(예: 지속 통증인데 solution)
- R6_FORMAT_TONE: '~해요' 어조 위반 또는 지정 헤더 누락
```

---

## 7. 공통 검증기 실행 명령 (단독 · 병합 · 파일럿)

모든 명령은 `courses/ai-applications/experiments/cos-agent` 디렉터리에서 실행합니다.

```bash
# 1) 파일럿 단독 검증 (팀원당 12턴)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
  --shard a --pilot

# 2) 파일럿 3인 병합 검증 (총 36턴 — 대량 생성 착수 게이트)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
          data/qlora/v2/shards/shard_b_moisturizing.jsonl \
          data/qlora/v2/shards/shard_c_sun_product.jsonl \
  --merge --pilot

# 3) 본 생성 완료 후 최종 3인 병합 검증 (비율·누수 엄격 강제)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
          data/qlora/v2/shards/shard_b_moisturizing.jsonl \
          data/qlora/v2/shards/shard_c_sun_product.jsonl \
  --merge --enforce-ratios --report outputs/qlora_validation_report.json
```

---

## 8. Linear Issue 복붙용 템플릿 (중복 제거 · 단일 기준 참조)

### Parent Issue
- **제목**: `[QLoRA Data] Ppopy v3 SOLUTION+HOLD 합성 데이터셋 구축 (36턴 파일럿 → 2,100턴 병합)`
- **본문**:
```markdown
## 단일 실행 기준 (Single Source of Truth)
모든 규칙·스키마·고정 시스템 프롬프트·기준 예제·검증 명령은 레포지토리의 아래 두 파일만 따릅니다:
- 가이드: `courses/ai-applications/experiments/cos-agent/docs/qlora-synthetic-dataset-guide.md`
- 공통 검증기: `courses/ai-applications/experiments/cos-agent/scripts/validate_qlora_dataset.py`

## 착수 게이트
1. 각 팀원은 가이드 0절 순서대로 **12턴 파일럿**을 먼저 생성합니다.
2. 3개 파일럿을 합쳐 **36턴 병합 검증(`--merge --pilot`) `error_count == 0`** 통과 후 본 생성(총 2,100턴)을 시작합니다.
```

### Sub-issue A (팀원 1)
```markdown
- **규칙 기준**: `docs/qlora-synthetic-dataset-guide.md` (Parent Issue 참조)
- **Branch**: `data/qlora-shard-a`
- **Output**: `courses/ai-applications/experiments/cos-agent/data/qlora/v2/shards/shard_a_cleansing.jsonl`
- **ID Prefix**: `syn-a-sol-0001`~, `syn-a-hold-0001`~
- **Scope**: 세정(`B-C01`~`B-C06`) + `B-I01` + `v67` `request_draft`/`hold` 재가공(`v67-sft-test-internal.jsonl` 제외, `train`/`val_internal` 분할 보존)
- **Target**: 파일럿 12턴(`solution` 9 / `hold` 3) → 본 생성 `solution` 600 / `hold` 200
- **Critic**: 팀원 2 AI (`provenance.critic_model != generator_model`)
- **Verify**: `uv run --locked python scripts/validate_qlora_dataset.py --input data/qlora/v2/shards/shard_a_cleansing.jsonl --shard a [--pilot]`
```

### Sub-issue B (팀원 2)
```markdown
- **규칙 기준**: `docs/qlora-synthetic-dataset-guide.md` (Parent Issue 참조)
- **Branch**: `data/qlora-shard-b`
- **Output**: `courses/ai-applications/experiments/cos-agent/data/qlora/v2/shards/shard_b_moisturizing.jsonl`
- **ID Prefix**: `syn-b-sol-0001`~, `syn-b-hold-0001`~
- **Scope**: 보습(`B-M01`~`B-M05`) + 활성성분/각질 중첩(`B-G13`~`15`, `B-I04`) + 새 제품 도입(`B-G11`~`12`) + 관련 안전 보류
- **Target**: 파일럿 12턴(`solution` 9 / `hold` 3) → 본 생성 `solution` 500 / `hold` 150
- **Critic**: 팀원 3 AI (`provenance.critic_model != generator_model`)
- **Verify**: `uv run --locked python scripts/validate_qlora_dataset.py --input data/qlora/v2/shards/shard_b_moisturizing.jsonl --shard b [--pilot]`
```

### Sub-issue C (팀원 3)
```markdown
- **규칙 기준**: `docs/qlora-synthetic-dataset-guide.md` (Parent Issue 참조)
- **Branch**: `data/qlora-shard-c`
- **Output**: `courses/ai-applications/experiments/cos-agent/data/qlora/v2/shards/shard_c_sun_product.jsonl`
- **ID Prefix**: `syn-c-sol-0001`~, `syn-c-hold-0001`~
- **Scope**: 자외선차단(`B-P01`~`09`, `B-P07` 제외) + 날씨/UV 결합 + 버전 불일치(`usage_held`)·대체 후보 + 보관/품질/눈 노출 보류(`B-S*`)
- **Target**: 파일럿 12턴(`solution` 9 / `hold` 3) → 본 생성 `solution` 500 / `hold` 150
- **Critic**: 팀원 1 AI (`provenance.critic_model != generator_model`)
- **Verify**: `uv run --locked python scripts/validate_qlora_dataset.py --input data/qlora/v2/shards/shard_c_sun_product.jsonl --shard c [--pilot]`
```
