# Ppopy QLoRA (`Qwen 3.5 4B`) 합성 데이터셋 구축 가이드 (1인 전담 · 에이전트 실행 명세)

> **문서 목적**: 담당 팀원 1명(및 전담 코딩 에이전트)이 **이 문서 + `prepare_v67_qlora_seeds.py` + `validate_qlora_dataset.py`**만으로 일관성 높고 학습–추론 괴리(Train–Inference Skew)가 없는 QLoRA용 합성 데이터셋을 즉시 제작·검수하도록 정의합니다.  
> **기본 프로파일 · rag-free (KB Anchor OFF)**: 앞단 AFA와 Runtime이 질문·충분성·HOLD를 처리합니다. 답변을 쓰는 SLM에는 확정된 사용자 관찰, 확인된 제품 근거, 참고 문헌 청크를 전달합니다. KB 판정을 비교에 넣을 때는 별도 `--profile kb-anchored`와 그 프로파일의 기존 프롬프트를 사용합니다.
> **기준 아키텍처**: [Ppopy End-to-End Architecture v3](end-to-end-architecture-draft.md) · [v3_contracts.py](../beauty_agent/v3_contracts.py) · [validate_qlora_dataset.py](../scripts/validate_qlora_dataset.py) · [prepare_v67_qlora_seeds.py](../scripts/prepare_v67_qlora_seeds.py)  
> **필수 경계 (`AGENTS.md`)**: `development_preview`, `production_enabled=false`, **합성 입력 전용**. 실제 사용자 개인정보·설문·연락처·제3자 원문 PDF/게시글 금지. 피부 질환 진단·임상/치료 효과 단정·자동 개선 판정·미공개 농도/pH 추정 금지. `QUESTION_MODE` 데이터는 생성하지 않습니다(0ms Quick Reply 버튼 처리).

---

## 0. 시작 조건 & 5단계 실행 순서 (에이전트 필독)

### 기준 커밋 체크아웃
이 문서와 검증기가 `main`에 머지된 **기준 커밋 SHA**에서 전용 브랜치를 생성합니다.

```bash
git fetch origin
BASE_COMMIT_SHA="<PR_머지_후_Linear에_기입된_실제_SHA>"
git checkout -b data/qlora-v2-dataset "$BASE_COMMIT_SHA"

# 필수 도구 존재 확인 & v67 안전 시드 즉시 추출 (test_internal / ask_user 자동 제외)
cd courses/ai-applications/experiments/cos-agent
uv run --locked python scripts/prepare_v67_qlora_seeds.py --output outputs/v67_qlora_seeds.jsonl
```

### 5단계 실행 흐름 (**24턴 파일럿 통과 → 900턴 1차 학습·평가 → 오답 보강**)

| 단계 | 작업 내용 | 출력 / 실행 명령 | 통과 조건 |
| --- | --- | --- | --- |
| **1. 기준 파일 동기화** | `v3_contracts.py`, `KB v0.6.1`, `outputs/v67_qlora_seeds.jsonl` 읽기 | 2절 공통 어휘와 3절 문헌의 적용 범위 확인 | 임의 어휘·URL 창작 금지 |
| **2. 24턴 파일럿 생성** | `pilot_bucket` 4종 × 각 6턴 = **정확히 24턴**(`solution` 18 / `hold` 6, 세정·보습·자외선·보류 전 영역 커버) | `data/qlora/v2/pilot_24.jsonl` | `--pilot` 통과 (`error_count == 0`, 입력 중복 0) |
| **3. 교차 Critic & 사람 전수 검수** | 생성 모델과 **다른 AI 모델**로 외부 검수 파일 생성 + 24턴 사람 육안 확인 | `data/qlora/v2/reviews/pilot_24_critic.jsonl` + `--pilot --review-file ...` | 외부 Critic PASS 100%, 고위험 `human_review == "approved"` |
| **4. 1차 본 데이터 900턴 생성** | `v67` 재가공(~300턴) + 신규 3영역 합성(~600턴) = **총 900턴**(`solution` 690 / `hold` 210) | `data/qlora/v2/qlora_solution_hold_v2.jsonl` | `--stage1 --review-file ...` 통과 (`error_count == 0`) |
| **5. 1차 학습·평가 후 2차 보강** | `Qwen 3.5 4B` QLoRA 1차 학습·평가 후 실제 오답 유형만 +300~600턴 집중 보강 | PR 제출 (`KB/`·코어 코드 미수정) | 인용 정확도·방해 청크 무시·HOLD 준수 목표 달성 |

---

## 1. 1차 목표 규모 및 비율 기준 (분모 명시)

1차 통합 QLoRA 어댑터(`solution-hold-lora`)는 **`solution` 690턴 + `hold` 210턴 = 총 900턴**으로 빠르게 1차 학습·평가를 돌린 뒤, 오답 분석을 거쳐 필요한 유형만 보강합니다.

| 항목 | 1차 목표 (900턴) | 검증기 강제 기준 & 정확한 분모 |
| --- | --- | --- |
| **출력 파일 / ID** | `data/qlora/v2/qlora_solution_hold_v2.jsonl` | `syn-sol-0001`~, `syn-hold-0001`~ |
| **`hold` 비율** | **210 / 900 = 23.3%** | 전체 행(`total_rows`) 대비 **20% ~ 25%** (`hold >= 210`, `solution >= 690`) |
| **Hard Negative 비율** | **≥ 25%** (최소 225턴) | 전체 행(`total_rows`) 대비 `is_hard_negative == true` 비율 |
| **영어 문헌 청크 비율** | **30% ~ 40%** (`solution` 중 210~275턴) | `solution` 행 중 **허용 목록에 있는 영어 문헌 청크를 하나 이상 포함한 행**의 비율 (`reference_excerpt` 또는 `kb_source_summary`) |
| **데이터 원천 구성** | `v67` 재가공 ~300턴 (`request_draft` ~120, `hold` ~180) + 신규 합성 ~600턴 (세정·`B-I01` 200 / 보습·중첩 200 / 자외선·버전·보관 200) | `v67`은 `outputs/v67_qlora_seeds.jsonl`에서만 추출 (`test_internal`·`ask_user` 0건) |
| **신규 합성 분할 (`split`)** | `train` 90% / `val_internal` 10% | `new_synthetic`의 `scenario_family_id`·`group_id` 단위 `val_internal` **7% ~ 13%**, 교차 분할 누수 0건 |

### Hard Negative 4종 (`hard_negative_type` 고정 enum)
1. `rag_distractor_ignore`: 무관한 문헌 청크를 `distractor_refs`로 섞고 응답에서 절대 인용·언급하지 않음.
2. `clinical_restraint`: 임상 수치·소규모 연구 청크가 들어와도 치료·개선 수치를 단정하지 않고 일반 관리 원리와 한계만 설명.
3. `version_mismatch_or_unknown`: 제품 버전 불일치(`usage_held`)·비공개 농도/pH를 추측하지 않고 `unknown` 또는 보류 유지.
4. `negation_or_other_subject`: 타인 경험(*"친구가 따갑대요"*)·명시적 부정(*"따갑진 않아요"*)에서 오탐 `hold` 금지.

---

## 2. 공통 어휘 표 (Controlled Vocabulary — 학습–추론 불일치 방지)

1명의 에이전트라도 앞뒤 생성 구간에서 값 표현이 흔들리지 않도록 아래 어휘를 고정합니다. (`kb_judgments[].status`와 `product_evidence[].status`는 `validate_qlora_dataset.py`가 강제합니다.)

| 필드 / 변수 | 고정 허용 값 | 비고 |
| --- | --- | --- |
| `kb_judgments[].status` | `"aligned"`, `"difference"`, `"unknown"`, `"hold"`, `"exception"` | `kb-anchored`에서 사용. `rag-free`에서는 빈 배열 또는 필드 생략 |
| `product_evidence[].status` | `"verified"`, `"usage_held"`, `"unknown"` | 검증기 강제 (`usage_held`는 버전 불일치) |
| `cleansing.steps` | 정수 `0`, `1`, `2`, `3` | KB `integer` 타입 (문자열 금지) |
| `skin.current_discomfort` | `"none"`, `"mild_transient"`, `"repeated"`, `"persistent"` | KB `categorical` (`persistent` → `B-B01` 보류) |
| `skin.pain` / `skin.stinging` / `skin.dryness` | `"none"`, `"mild"`, `"moderate"`, `"severe"` | KB `ordinal` (한국어·숫자 혼용 금지) |
| `storage.sensory_change` | `{"color_or_odor_change": true/false, "separation": true/false}` | KB `structured` (`true` → `B-S04` 보류) |
| `cleansing.repeat_wash` | `{"automatic_multi_step_for_water_resistant": true/false}` | KB `structured` (`B-I01` 판정용) |
| `product_evidence[]` 키 | `product_id`, `version`, `synthetic_product`, `status`, `label_guidance`, `evidence_ref` | `evidence_ref`는 반드시 `catalog:<product_id>@<version>`과 일치 |

---

## 3. Reference RAG 청크와 검증 프로파일

- `rag-free`의 `card_ids`는 생략하거나 `[]`로 둘 수 있습니다. 카드가 있으면 기존 KB ID 검증과 `B-P07` 금지를 적용합니다.
- `confirmed_observations`에는 사용자에게 확인한 루틴이나 질문 맥락을 추가할 수 있습니다. 기존 KB 관찰 키는 지정된 값 타입을 유지하고, 미등록 `product.*` 관찰은 허용하지 않습니다. 제품 사실은 버전이 확인된 `product_evidence`로 전달합니다.
- 문헌 청크는 `ReferenceChunk` 형식을 사용합니다. `ref:` ID, 본문, URL, 위치(`locator`), 확인일(`checked_on`), 한계(`limitations`)를 적습니다. 새 출처는 실제 원문과 적용 조건을 확인한 뒤 등록하세요. `U*`, `D*`, `F01`, `F02`, `S30`, `S31`은 두 프로파일 모두 금지합니다.
- `chunk_origins`는 청크마다 기록합니다.
  - `reference_excerpt`: `rag-free`에서 사용할 공개 가이드라인·아티클의 확인된 구절입니다. 적용 조건과 한계를 구절과 함께 보존합니다.
  - `kb_source_summary`: 개별 연구 등의 관찰 결과와 한계를 담은 요약입니다. KB 등록 자료를 요약할 때는 `review_scope` 및 `limitations` 범위를 지킵니다.
  - `synthetic_defense_probe`: 시험용 합성 방해 청크입니다. `distractor_refs`에만 두며 인용과 영어 비율 집계에서 제외합니다.
- `rag-free`에서는 `ref:`, `catalog:`, `alternative:` 중 입력으로 뒷받침되고 `allowed_evidence_refs`에 포함된 ID만 인용합니다. `solution`은 이렇게 허용된 근거를 하나 이상 인용합니다. `hold`에는 RAG 청크가 들어가지 않습니다.
- 비교용 `kb-anchored`는 비어 있지 않은 카드 목록, 등록 관찰 키, KB 출처의 기존 메타데이터 검사를 유지합니다. 이전 프롬프트가 포함된 동결 자료는 해당 기준으로 재현할 수 있습니다. 다음 기본 학습 Export에 새 프롬프트를 적용하고 원본과 검수 기록을 보존하세요.

아래 표는 참고할 수 있는 **기존 KB 출처 예시**입니다. 행별 근거의 적용 범위와 실제 출처는 별도로 확인합니다.

| 영역 | 허용 `evidence_ref` | KB 등록 출처 요약 (`source_registry`) |
| --- | --- | --- |
| **세정 (C)** | `ref:S03`, `ref:S07`, `ref:S08` | AAD 세안 기본(`S03`), 세정제 pH·조성(`S07`), 20명 선크림 세정 비교(`S08`) |
| **보습 (M)** | `ref:S04`, `ref:S20`, `ref:S21`, `ref:S23`~`S25`, `ref:S29` | AAD 건조 피부·손 보습·습식 면도·무향료 선택 |
| **자외선차단 (P)** | `ref:S05`, `ref:S09`, `ref:S14`, `ref:S16`~`S18` | FDA/AAD SPF 30+·광범위·재도포·비제품 광보호, 보습+선크림 UV 반사 영상(`S09`), 눈가·폐기 |
| **공통·병용·도입 (G/I)** | `ref:S15`, `ref:S26`, `ref:S32`~`S35` | FDA 알레르겐(`S15`), 팩/레티노이드 각질 중첩(`S26`,`S32`), DailyMed 병용 자극(`S33`,`S34`), 소부위 확인(`S35`) |
| **임상 절제 방어 시험** | `ref:S10`~`S13` | 수면(`S10`)·스트레스(`S11`)·저혈당식이 32명 RCT(`S12`)·아토피 설명(`S13`) |
| **보관·품질·안전 (S/L/H)** | `ref:S06`, `ref:S27`, `ref:S36`~`S41` | FDA 보관·미생물 안전, HPRA/식약처 가품·회수 보류, 접촉 마찰, 눈 노출 세척(`S41`) |

> **금지 ID**: `U01`~`U09`, `D01`~`D04`, `F01`, `F02`, `S30`, `S31`, `B-P07`.

---

## 4. 고정 시스템 프롬프트 & 검증 통과 기준 예제 3종

### A. 고정 `messages[0].content` (`SYSTEM_PROMPT_SOLUTION_HOLD`) — 1글자도 변경 금지
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, 허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. 문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 "hold"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요.
```

### B. 기준 예제 1 — `solution` (`B-I01` 내수성 무조건 반복 세안 + 방해 청크 무시)
```json
{
  "id": "syn-sol-0001",
  "scenario_id": "new-bi01-001",
  "group_id": "new-group-bi01-001",
  "scenario_family_id": "fam-bi01-001",
  "split": "train",
  "mode": "solution",
  "pilot_bucket": "distractor_or_defense",
  "domains": ["cleansing", "sun_protection"],
  "card_ids": [],
  "is_hard_negative": true,
  "hard_negative_type": "rag_distractor_ignore",
  "chunk_origins": {
    "ref:S08": "kb_source_summary",
    "ref:S21": "reference_excerpt"
  },
  "messages": [
    {
      "role": "system",
      "content": "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, 허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. 문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 \"hold\"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요."
    },
    {
      "role": "user",
      "content": "{\"mode\":\"solution\",\"confirmed_observations\":{\"cleansing.steps\":{\"variable_id\":\"cleansing.steps\",\"state\":\"known\",\"value\":3,\"source\":\"user_report\",\"confirmed_by_user\":true},\"cleansing.repeat_wash\":{\"variable_id\":\"cleansing.repeat_wash\",\"state\":\"known\",\"value\":{\"automatic_multi_step_for_water_resistant\":true},\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[],\"product_evidence\":[{\"product_id\":\"syn-sun-001\",\"version\":\"1.0\",\"synthetic_product\":true,\"status\":\"verified\",\"label_guidance\":\"합성 제품 표시 예시: 폼 클렌저 1회 세안 가능\",\"evidence_ref\":\"catalog:syn-sun-001@1.0\"}],\"rag_chunks\":[{\"evidence_ref\":\"ref:S08\",\"text\":\"In a 20-subject imaging study comparing water, facial cleanser, and cleansing oil, cleanser removal performance varied by formulation rather than requiring mandatory multi-step washing for every water-resistant product.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995\",\"locator\":\"Abstract: Methods / Results / Conclusion\",\"checked_on\":\"2026-11-04\",\"limitations\":\"제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호.\"},{\"evidence_ref\":\"ref:S21\",\"text\":\"Apply fragrance-free hand cream or ointment immediately after hand washing to help relieve dry hands.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands\",\"locator\":\"손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.\",\"checked_on\":\"2026-11-04\",\"limitations\":\"다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다.\"}],\"allowed_evidence_refs\":[\"catalog:syn-sun-001@1.0\",\"ref:S08\"],\"distractor_refs\":[\"ref:S21\"]}"
    },
    {
      "role": "assistant",
      "content": "### 핵심 안내\n지금 쓰는 합성 제품의 표시에는 클렌징폼 1회 세안이 가능하다고 나와 있어요. 현재의 3단계 세안은 이 제품 표시를 기준으로 다시 살펴볼 수 있어요 [catalog:syn-sun-001@1.0].\n\n### 근거 및 이유\n20명 대상 제한된 제품 조합 영상 비교 연구에서도 제형에 따라 세정 결과가 달라지며 모든 내수성 제품에 이중세안을 일률적으로 확정하지는 않아요 [ref:S08].\n\n### 확인이 필요한 한계\n위 문헌은 소규모 제한 조합 기준이며 모든 내수성 제품에 일반화되지는 않아요. 다른 제품을 쓰는 경우에는 그 제품의 표시를 따로 확인해 주세요."
    }
  ],
  "allowed_evidence_refs": ["catalog:syn-sun-001@1.0", "ref:S08"],
  "distractor_refs": ["ref:S21"],
  "provenance": {
    "source_origin": "new_synthetic",
    "source_scenario_id": null,
    "source_turn_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "critic_status": "PASS",
    "human_review": "unreviewed"
  }
}
```

### C. 기준 예제 2 — `hold` (`B-B01` 지속 불편감·통증 필수 보류)
```json
{
  "id": "syn-hold-0001",
  "scenario_id": "new-bb01-001",
  "group_id": "new-group-bb01-001",
  "scenario_family_id": "fam-bb01-001",
  "split": "train",
  "mode": "hold",
  "pilot_bucket": "hold",
  "domains": ["general_safety"],
  "card_ids": ["B-B01"],
  "is_hard_negative": false,
  "hard_negative_type": null,
  "chunk_origins": {},
  "messages": [
    {
      "role": "system",
      "content": "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, 허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. 문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 \"hold\"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요."
    },
    {
      "role": "user",
      "content": "{\"mode\":\"hold\",\"confirmed_observations\":{\"skin.current_discomfort\":{\"variable_id\":\"skin.current_discomfort\",\"state\":\"known\",\"value\":\"persistent\",\"source\":\"user_report\",\"confirmed_by_user\":true},\"skin.pain\":{\"variable_id\":\"skin.pain\",\"state\":\"known\",\"value\":\"moderate\",\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[],\"product_evidence\":[],\"rag_chunks\":[],\"allowed_evidence_refs\":[],\"distractor_refs\":[]}"
    },
    {
      "role": "assistant",
      "content": "### 개별 권고 보류 안내\n지속적인 불편감과 통증이 확인되어 개별 루틴 조정이나 제품 안내는 보류해요.\n\n### 필요한 다음 단계\n불편감과 통증을 전문가에게 확인받아 주세요."
    }
  ],
  "allowed_evidence_refs": [],
  "distractor_refs": [],
  "provenance": {
    "source_origin": "new_synthetic",
    "source_scenario_id": null,
    "source_turn_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "critic_status": "PASS",
    "human_review": "approved"
  }
}
```

### D. 기준 예제 3 — `hold` (`B-S04` 제품 변질·품질 이상 의심 보류)
```json
{
  "id": "syn-hold-0002",
  "scenario_id": "new-bs04-001",
  "group_id": "new-group-bs04-001",
  "scenario_family_id": "fam-bs04-001",
  "split": "train",
  "mode": "hold",
  "pilot_bucket": "hold",
  "domains": ["general_safety"],
  "card_ids": ["B-S04"],
  "is_hard_negative": false,
  "hard_negative_type": null,
  "chunk_origins": {},
  "messages": [
    {
      "role": "system",
      "content": "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. 입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, 허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. 문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, 미공개 성분 농도·pH 추측은 금지합니다. 확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. mode가 \"hold\"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. 어조는 차분한 '~해요' 존댓말을 사용하세요."
    },
    {
      "role": "user",
      "content": "{\"mode\":\"hold\",\"confirmed_observations\":{\"storage.sensory_change\":{\"variable_id\":\"storage.sensory_change\",\"state\":\"known\",\"value\":{\"color_or_odor_change\":true,\"separation\":true},\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[],\"product_evidence\":[],\"rag_chunks\":[],\"allowed_evidence_refs\":[],\"distractor_refs\":[]}"
    },
    {
      "role": "assistant",
      "content": "### 개별 권고 보류 안내\n제품의 색이나 냄새가 달라지고 층이 분리되어, 현재 제품 상태를 확인하기 전까지 개별 안내를 보류해요.\n\n### 필요한 다음 단계\n제품 상태와 표시를 제품 품질 담당자에게 확인해 주세요."
    }
  ],
  "allowed_evidence_refs": [],
  "distractor_refs": [],
  "provenance": {
    "source_origin": "new_synthetic",
    "source_scenario_id": null,
    "source_turn_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "critic_status": "PASS",
    "human_review": "approved"
  }
}
```

---

## 5. Teacher & 외부 Critic Prompt (별도 검수 파일 기록)

### A. 답변 생성용 Teacher Prompt
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'의 학습 데이터 생성기입니다.
기본 rag-free에서는 확정 사용자 관찰, 확인된 제품 정보와 허용된 참고 문헌을 연결해 한국어 응답을 작성하세요. 연구나 가이드라인의 적용 범위가 다르면 한계를 밝혀 주세요.

[절대 규칙]
1. 입력의 allowed_evidence_refs에 포함된 ID만 [ID] 형식으로 인용하고, distractor_refs와 미제공 ID는 절대 인용하지 마세요.
2. synthetic_defense_probe 청크는 인용하지 말고 그 수치·문장을 임상 효능으로 단정하지 마세요.
3. 피부 질환 진단, 치료/임상 효과 단정, 미공개 성분 농도·pH 추측을 금지합니다.
4. 확인되지 않은 정보나 제품 버전 불일치는 미상(unknown) 또는 보류로 명시하세요.
5. mode="solution"은 '### 핵심 안내' → '### 근거 및 이유' → '### 확인이 필요한 한계' 3단 구조로 작성하세요.
6. mode="hold"는 개별 루틴·제품·세안/도포 지시·대체 후보를 절대 작성하지 말고 '### 개별 권고 보류 안내' → '### 필요한 다음 단계' 2단 구조로만 작성하세요.
7. 어조는 차분한 '~해요' 존댓말로 통일하세요.
```

### B. 외부 Cross-Model Critic Prompt (`reviews/*_critic.jsonl` 별도 저장)
1인 전담 시 자기 모델 편향을 막기 위해 **생성 모델과 다른 AI 모델**(예: 생성 GPT ↔ 검수 Claude/Gemini)로 아래 JSON을 생성해 **별도 파일(`data/qlora/v2/reviews/*_critic.jsonl`)**에 저장합니다. 검증기(`--review-file`)가 `row_id` 중복을 금지하고, 각 행의 정규화 내용 해시(`content_sha256` = `validate_qlora_dataset.compute_row_content_sha256(req, assistant, card_ids=..., chunk_origins=..., is_hard_negative=..., hard_negative_type=...)`)를 대조해 검수 후 입력·답변·`card_ids`·`chunk_origins` 무단 수정을 모두 차단합니다. 또한 정규화 `SLMRequest` 입력 중복 검사는 파일럿·배치·`--stage1` 전체에 적용되며, 파일럿(`--pilot --review-file`)은 **24행 100% `human_review == "approved"`**를 요구합니다.

```text
당신은 Ppopy 합성 데이터 품질 감사관입니다.
함께 전달된 [1] SLMRequest 입력 JSON, [2] chunk_origins, [3] card_ids(있을 경우), 모드와 실제 근거, [4] assistant 응답을 아래 6개 규칙으로 검수하고, 행별 JSON을 반환하세요:
{"row_id": "...", "content_sha256": "<compute_row_content_sha256 값>", "critic_model": "실제_검수_모델명", "decision": "PASS" | "FAIL", "violated_rule": null | "R1_CITATION" | "R2_CLINICAL" | "R3_UNKNOWN_VERSION" | "R4_HOLD_LEAK" | "R5_INPUT_JUDGMENT" | "R6_FORMAT_TONE", "offending_span": "...", "evidence_ref": "..."}

- R1_CITATION: 입력에 없는 근거·비표준([S99] 등)·distractor_refs·synthetic_defense_probe 인용
- R2_CLINICAL: 피부 질환 진단, 임상/치료 효과 단정, 소규모 연구 수치의 효능화
- R3_UNKNOWN_VERSION: 미공개 농도/pH 추측 또는 버전 불일치 제품 사용법 채택
- R4_HOLD_LEAK: mode="hold"에서 루틴·제품·세안/도포 지시·대체 후보 누출
- R5_INPUT_JUDGMENT: 확정 사용자 관찰·제품 근거·문헌의 적용 범위와 답변의 모순, 모드 불일치 또는 파일럿 버킷 실질 시나리오 부재/복붙 중복. Anchor ON이면 제공된 KB 판정도 대조
- R6_FORMAT_TONE: '~해요' 어조 위반 또는 지정 헤더 누락
```

### C. Subagent 병렬 배치 실행 절차 (권장 실행 패턴)
대량 생성(900턴) 시 단일 긴 컨텍스트에서 발생하는 템플릿 반복(Context Rot)을 막기 위해, 메인 에이전트(**Coordinator**)가 **소배치(25~40턴/배치) 단위로 Generator Subagent 3~4개를 병렬 실행**하고 **전담 Verifier/Critic Subagent 1개**로 배치별 게이트를 통과한 행만 병합합니다.

```text
[Coordinator] 전역 ID 대역 · 담당 카드/v67 시드 · split(90/10) · HN/EN 할당 선분배
   ├─▶ [Gen Subagent 1~4 (병렬, 25~40턴/배치)] → outputs/batches/batch_XX.jsonl
   └─▶ [Verifier/Critic Subagent (전담 · 다른 모델 계열)]
         ① validate_qlora_dataset.py 배치 검증
         ② 독립 Critic 검수 → outputs/batches/batch_XX_critic.jsonl (content_sha256 포함)
         ③ PASS 행만 마스터(qlora_solution_hold_v2.jsonl + reviews/stage1_critic.jsonl)에 병합, FAIL만 재생성
```

1. **ID·가족·시드 선분배**: Generator Subagent는 Coordinator가 할당한 ID 범위(`syn-sol-0001~0030` 등), `scenario_family_id` 접두사, `split`, `v67` 시드 슬라이스만 사용합니다.
2. **배치 크기 제한**: 1회 배치당 **25~40턴**을 넘기지 않습니다(900턴 = 약 25~30개 소배치).
3. **Critic Subagent 모델 분리**: Critic Subagent는 Generator와 **다른 모델 계열**로 실행해 자기 편향을 방지하고 `critic_model != generator_model` 규칙을 충족합니다.
4. **최종 전체 검증**: 모든 배치 병합 후 Coordinator가 마스터 파일 전체에 `--stage1 --review-file`을 실행해 교차 배치 중복·`scenario_family_id` 누수·전체 비율을 최종 확인합니다.

---

## 6. 즉시 실행 검증 명령

모든 명령은 `courses/ai-applications/experiments/cos-agent` 디렉터리에서 실행합니다.
아래 명령은 새 프롬프트로 준비한 데이터에 사용합니다. 기존 프롬프트가 들어 있는 동결 파일은 `--profile kb-anchored`로 검증하세요.

```bash
# 0) v67 안전 재가공 시드 추출 (test_internal·ask_user 자동 제외)
uv run --locked python scripts/prepare_v67_qlora_seeds.py \
  --output outputs/v67_qlora_seeds.jsonl

# 1) 24턴 파일럿 검증 (solution 18 / hold 6, 4버킷 × 6행, 외부 Critic 파일 대조)
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free \
  --input data/qlora/v2/pilot_24.jsonl \
  --pilot \
  --review-file data/qlora/v2/reviews/pilot_24_critic.jsonl

# 2) 1차 본 데이터 900턴 최종 검증 (비율·90/10 분할·누수·외부 Critic·고위험 10% 사람 검수 강제)
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free \
  --input data/qlora/v2/qlora_solution_hold_v2.jsonl \
  --stage1 \
  --review-file data/qlora/v2/reviews/stage1_critic.jsonl \
  --report outputs/qlora_validation_report.json
```

---

## 7. Linear Issue 복붙용 템플릿 (1인 전담용)

- **제목**: `[QLoRA Data] Ppopy v3 SOLUTION+HOLD 합성 데이터셋 구축 (24턴 파일럿 → 900턴 1차 학습셋)`
- **본문**:
```markdown
## 단일 실행 기준 (Single Source of Truth)
- **기준 커밋 SHA**: `<PR_머지_후_실제_SHA>`
- **가이드**: `courses/ai-applications/experiments/cos-agent/docs/qlora-synthetic-dataset-guide.md`
- **v67 시드 추출기**: `courses/ai-applications/experiments/cos-agent/scripts/prepare_v67_qlora_seeds.py`
- **공통 검증기**: `courses/ai-applications/experiments/cos-agent/scripts/validate_qlora_dataset.py`

## 작업 범위 (1인 전담)
- **Branch**: `data/qlora-v2-dataset` (`main` 직접 커밋·푸시 금지)
- **Step 1 (파일럿 24턴)**: `data/qlora/v2/pilot_24.jsonl` (`solution` 18 / `hold` 6, 4버킷 × 6턴) + 다른 모델 AI 외부 검수 파일(`reviews/pilot_24_critic.jsonl`) + 사람 전수 확인
- **Step 2 (1차 본 데이터 900턴)**: `data/qlora/v2/qlora_solution_hold_v2.jsonl` (`solution` 690 / `hold` 210 = `v67` 재가공 ~300 + 신규 3영역 합성 ~600) + `reviews/stage1_critic.jsonl`

## 완료 조건 (Definition of Done)
1. 파일럿 24턴 `--pilot --review-file ...` `error_count == 0` 및 팀 확인 완료
2. 1차 900턴 `--stage1 --review-file ...` `error_count == 0` (`hold` 20~25%, HN ≥ 25%, 인용 가능한 영어 문헌 30~40%, 신규 `val_internal` 7~13%, 외부 Critic PASS 100%, 고위험 `human_review == "approved"` ≥ 10%)
3. 기본 학습 Export는 `--profile rag-free`로 검증합니다. `kb_judgments`는 비워 두고 `[kb:...]` 인용을 제거합니다. 허용 근거와 실제 인용을 대조하고, 미상·HOLD·v67 분할 경계를 확인합니다.
4. `KB/`, `docs/source-manifest.json`, `beauty_agent/` 코어 코드 미수정 상태로 PR 제출
```
