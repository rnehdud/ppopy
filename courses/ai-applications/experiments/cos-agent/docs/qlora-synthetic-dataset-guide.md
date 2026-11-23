# Ppopy QLoRA (`Qwen 3.5 4B`) 합성 데이터셋 구축 가이드 (3인 병렬 · 에이전트 실행 명세)

> **문서 목적**: 서로 다른 3명의 팀원 에이전트(Codex 등)가 **이 문서와 공통 기준 커밋의 검증기**만으로 동일한 스키마·판정 근거·품질 기준의 합성 데이터셋을 제작·병합하도록 정의합니다.  
> **기준 아키텍처**: [Ppopy End-to-End Architecture v3](end-to-end-architecture-draft.md) · [v3_contracts.py](../beauty_agent/v3_contracts.py) · [validate_qlora_dataset.py](../scripts/validate_qlora_dataset.py)  
> **필수 경계 (`AGENTS.md`)**: `development_preview`, `production_enabled=false`, **합성 입력 전용**. 실제 사용자 개인정보·설문·연락처·제3자 원문 PDF/게시글 금지. 피부 질환 진단·임상/치료 효과 단정·자동 개선 판정·미공개 농도/pH 추정 금지. `QUESTION_MODE` 데이터는 생성하지 않습니다(0ms Quick Reply 버튼 처리).

---

## 0. 시작 조건 & 6단계 작업 순서 (에이전트 필독)

### 공통 기준 커밋 체크아웃 (3인 전원 동일 기준에서 출발)
이 문서와 `scripts/validate_qlora_dataset.py`가 `main`에 머지된 **기준 커밋 SHA**(PR 머지 후 Linear Parent Issue의 `BASE_COMMIT_SHA` 값 확인)에서 각자 담당 명령을 그대로 복사해 실행합니다. *(로컬 미푸시 커밋이나 문서만 있는 브랜치에서 시작하지 마세요.)*

```bash
# 공통: 원격 최신화 후 Linear Parent Issue에 기입된 실제 main 머지 커밋 SHA를 지정
git fetch origin
BASE_COMMIT_SHA="<PR_머지_후_Linear에_기입된_실제_SHA>"

# 팀원 1 (Shard A)
git checkout -b data/qlora-shard-a "$BASE_COMMIT_SHA"

# 팀원 2 (Shard B)
git checkout -b data/qlora-shard-b "$BASE_COMMIT_SHA"

# 팀원 3 (Shard C)
git checkout -b data/qlora-shard-c "$BASE_COMMIT_SHA"

# 공통 확인: 검증기 존재 확인
test -f courses/ai-applications/experiments/cos-agent/scripts/validate_qlora_dataset.py
```

### 6단계 실행 순서 (**대량 생성 전 반드시 4단계 36턴 파일럿 병합 검증 통과 필수**)

| 단계 | 작업 내용 | 필수 입력 / 실행 명령 | 통과 조건 |
| --- | --- | --- | --- |
| **1. 할당·기준 커밋 확인** | 본인 Shard(`a`/`b`/`c`), `<BASE_COMMIT_SHA>` 체크아웃 | 2절 분담표 + Linear Sub-issue | `main` 직접 작업 금지, `validate_qlora_dataset.py` 존재 확인 |
| **2. 기준 파일 동기화** | `v3_contracts.py`, `KB v0.6.1`, `validate_qlora_dataset.py` 읽기 | `KB/Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json`, `sunscreen_removal_review.json`, `data/action_policy/v67/` | 변수 타입·카드 판정 조건·`source_registry` 원본 메타데이터 확인 |
| **3. 파일럿 생성 (12턴/인)** | `pilot_bucket` 4종 각 3턴씩 **정확히 12턴**(`solution` 9 / `hold` 3) 생성 | ① 시나리오·기대 판정 고정 → ② 답변 생성 (5절 절차) | `data/qlora/v2/shards/shard_*.jsonl` 12줄 기록 |
| **4. 공통 검증 (단독 → 36턴 병합)** | 단독 12턴 검증 후 3개 파일 합쳐 **36턴 병합 검증** | `uv run --locked python scripts/validate_qlora_dataset.py --input ... --merge --pilot` | 빈 파일 0, A/B/C 각 12행·총 36행, `error_count == 0` |
| **5. 교차 검수 & 사람 표본 검수** | 옆 팀원 AI(구조화 Critic) + 고위험 사례(`hold`, 버전 불일치) 10% 이상 사람 검수 | 6절 B Critic Prompt (`SLMRequest` + `chunk_origins` + 기대 판정 함께 전달) | `provenance.critic_status == "PASS"`, 고위험 `human_review == "approved"` ≥ 10% |
| **6. 본 생성 및 PR 제출** | 파일럿 오류 반영 후 목표 수량 생성 → `--merge --enforce-ratios --require-review` 통과 → PR | 7절 최종 검증 명령 | 자동 검증 + 검수 기록 모두 통과, `KB/`·코어 코드 미수정 |

---

## 1. 목표 규모 및 비율 기준 (분모 명시)

1차 통합 QLoRA 어댑터(`solution-hold-lora`)는 **`solution` 1,600턴 + `hold` 500턴 = 총 2,100턴**을 목표로 합니다. *(2순위 `nlu` Multi-LoRA 1,000~1,500턴은 1차 완료 후 별도 진행)*

| 지표 | 목표 기준 | 정확한 분모 (검증기 계산식) |
| --- | --- | --- |
| **`hold` 비율** | **20% ~ 25%** *(목표 500 / 2,100 = **23.8%**)* | 전체 제출 행(`total_rows`) 대비 `mode == "hold"` 행 비율 |
| **Hard Negative 비율** | **≥ 25%** | 전체 제출 행(`total_rows`) 대비 `is_hard_negative == true` 행 비율 |
| **영어 문헌 청크 비율** | **30% ~ 40%** | `mode == "solution"` 행 중 **`allowed_evidence_refs`에 포함되고 `chunk_origins == "kb_source_summary"`인 영어 청크**를 사용한 행 비율 *(방해 청크·합성 방어 청크 제외)* |
| **파일럿 버킷 (`pilot_bucket`)** | 팀원당 12턴 = 4종 × 3턴 / 병합 36턴 | `normal_guidance`, `hold`, `unknown_or_version`, `distractor_or_defense` 각 3행/팀원 (같은 shard 내 입력 `SLMRequest` 중복 금지, `unknown_or_version`은 실제 `unknown`/`usage_held` 신호 포함, `distractor_or_defense`는 실제 `distractor_refs`/`synthetic_defense_probe` 포함) |
| **신규 합성 분할 (`split`)** | `val_internal` 비어있음 금지 (`train` 90% / `val_internal` 10%) | `provenance.source_origin == "new_synthetic"`의 `scenario_family_id`·`group_id` 단위 `val_internal` 비율 **7% ~ 13%** (`--enforce-ratios` 시 자동 검증, `v67` 재가공분은 원본 분할 유지) |
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

### 분할(`split`) 및 `v67` 누수 차단 규칙
1. **실제 분할 기준 필수 로드**: `v67-sft-train.jsonl` / `v67-sft-val-internal.jsonl` / `v67-sft-test-internal.jsonl` 3개 파일이 모두 존재해야 검증이 실행됩니다. (`canonical-candidates-v67.jsonl`의 `split` 표기는 사용하지 않습니다.)
2. **`test_internal` 절대 금지**: `v67-sft-test-internal.jsonl`에 속한 `scenario_id`·`group_id`·`id`(`source_turn_id`)는 0건이어야 합니다.
3. **`v67` 재가공 원본 실존 및 동일 분할 유지**: `provenance.source_origin == "recycled_v67"`인 행은 실제 `v67`에 존재하는 `provenance.source_scenario_id`와 `provenance.source_turn_id`를 모두 기록해야 하며, 원본과 동일한 `split`(`train` 또는 `val_internal`)을 유지해야 합니다.
4. **교차 분할 누수 5중 차단**: 병합 검증 시 `group_id`, `scenario_id`, **`scenario_family_id`**, `source_turn_id`, 정규화 `assistant` 문장이 `train`과 `val_internal`에 동시에 나타나면 즉시 실패합니다. (신규 합성은 `scenario_family_id`·`group_id` 단위로 `train` 90% / `val_internal` 10% 배분.)

---

## 3. KB에 등록된 출처와 확인 범위 (`KB v0.6.1` `source_registry`)

`rag_chunks[]`의 `source_url`, `locator`, `checked_on`, `limitations`는 **절대 손으로 작성하지 말고 `Poppy_KB_seed_v0.6.1.json`의 `source_registry` 원본 값을 그대로 복사**합니다. 또한 `allowed_evidence_refs`의 모든 ID는 실제 입력의 `rag_chunks`·`kb_judgments`·`product_evidence`에 존재해야 합니다.

### 청크 출처 이중 분류 (`chunk_origins` 필수 필드)
- **`kb_source_summary`**: `source_registry`의 `review_scope`·`limitations` 범위 안에서만 요약한 근거 청크. `allowed_evidence_refs`에 포함·인용 가능하며 영어 청크 비율 집계 대상입니다.
- **`synthetic_defense_probe`**: 방해 청크(`distractor_refs`) 또는 임상 과잉 주장 차단 시험용 합성 청크. **`allowed_evidence_refs` 포함 금지, 인용 금지, 영어 청크 비율 집계 제외**입니다.

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

### B. 기준 예제 1 — `solution` 완성 행 (`B-I01` 실제 판정 조건 충족)
- **판정 근거 (`Poppy_KB_seed_v0.6.1.json` `B-I01` `comparison_spec.difference_when`)**: *"내수성 표시만 보고 무조건 반복 세안함"* 조건에 해당하도록 `cleansing.steps: 3`(정수형) 및 `cleansing.repeat_wash: {"automatic_multi_step_for_water_resistant": true}`를 관찰로 고정하고, 합성 제품 표시(`"synthetic_product": true`)에서 폼 클렌저 1회 세안 가능을 확인한 분기입니다.
- `ref:S08`은 `kb_source_summary`(허용·인용), `ref:S21`은 `synthetic_defense_probe`(`distractor_refs` 전용, 인용·영어 집계 제외)입니다.

```json
{
  "id": "syn-a-sol-0001",
  "scenario_id": "new-a-bi01-001",
  "group_id": "new-group-a-bi01-001",
  "scenario_family_id": "fam-a-bi01-001",
  "split": "train",
  "mode": "solution",
  "pilot_bucket": "distractor_or_defense",
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
      "content": "{\"mode\":\"solution\",\"confirmed_observations\":{\"cleansing.steps\":{\"variable_id\":\"cleansing.steps\",\"state\":\"known\",\"value\":3,\"source\":\"user_report\",\"confirmed_by_user\":true},\"cleansing.repeat_wash\":{\"variable_id\":\"cleansing.repeat_wash\",\"state\":\"known\",\"value\":{\"automatic_multi_step_for_water_resistant\":true},\"source\":\"user_report\",\"confirmed_by_user\":true}},\"kb_judgments\":[{\"card_id\":\"B-I01\",\"status\":\"difference\",\"guidance\":\"내수성 표시만 보고 무조건 반복 세안하면 피부 부담이 커질 수 있어, 광보호를 유지하면서 제품에 맞는 세정 단계를 검토합니다.\"}],\"product_evidence\":[{\"product_id\":\"syn-sun-001\",\"version\":\"1.0\",\"synthetic_product\":true,\"label_guidance\":\"합성 제품 표시 예시: 폼 클렌저 1회 세안 가능\",\"evidence_ref\":\"catalog:syn-sun-001@1.0\"}],\"rag_chunks\":[{\"evidence_ref\":\"ref:S08\",\"text\":\"In a 20-subject imaging study comparing water, facial cleanser, and cleansing oil, cleanser removal performance varied by formulation rather than requiring mandatory multi-step washing for every water-resistant product.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995\",\"locator\":\"Abstract: Methods / Results / Conclusion\",\"checked_on\":\"2026-11-04\",\"limitations\":\"제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호.\"},{\"evidence_ref\":\"ref:S21\",\"text\":\"Apply fragrance-free hand cream or ointment immediately after hand washing to help relieve dry hands.\",\"scope\":\"general_skincare_practice\",\"source_url\":\"https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands\",\"locator\":\"손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.\",\"checked_on\":\"2026-11-04\",\"limitations\":\"다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다.\"}],\"allowed_evidence_refs\":[\"kb:B-I01@0.6.1\",\"catalog:syn-sun-001@1.0\",\"ref:S08\"],\"distractor_refs\":[\"ref:S21\"]}"
    },
    {
      "role": "assistant",
      "content": "### 핵심 안내\n내수성 표시만 보고 무조건 3단계로 반복 세안할 필요는 없어요. 자외선차단제 도포량은 유지하면서 합성 제품 표시 예시의 클렌징폼 1회 세안으로 단계를 줄여 보실 수 있어요 [kb:B-I01@0.6.1] [catalog:syn-sun-001@1.0].\n\n### 근거 및 이유\n20명 대상 제한된 제품 조합 영상 비교 연구에서도 제형에 따라 세정 결과가 달라지며 모든 내수성 제품에 이중세안을 일률적으로 확정하지는 않아요 [ref:S08].\n\n### 확인이 필요한 한계\n위 문헌은 소규모 제한 조합 기준이며 모든 내수성 제품에 일반화되지는 않아요. 세안 후 당김이나 자극이 반복되면 단계를 더 줄이고 확인이 필요해요."
    }
  ],
  "allowed_evidence_refs": ["kb:B-I01@0.6.1", "catalog:syn-sun-001@1.0", "ref:S08"],
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

### C. 기준 예제 2 — `hold` 완성 행 (`B-B01` 지속 불편감·통증 필수 보류)
```json
{
  "id": "syn-a-hold-0001",
  "scenario_id": "new-a-bb01-001",
  "group_id": "new-group-a-bb01-001",
  "scenario_family_id": "fam-a-bb01-001",
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
    "source_turn_id": null,
    "generator_model": "gpt-5.4",
    "critic_model": "claude-sonnet-4",
    "critic_status": "PASS",
    "human_review": "approved"
  }
}
```

---

## 5. 2단계 생성 절차 (판정 오류 전파 차단)

1. **1단계 — 시나리오 및 기대 판정 고정**: `KB v0.6.1`의 `baseline_cards`(`comparison_spec` 조건 직접 대조)·`acceptance_scenarios` 또는 `v67-sft-{train|val-internal}.jsonl`의 검토된 사례를 근거로 `confirmed_observations`, `mode`, `kb_judgments`, `allowed_evidence_refs`, `rag_chunks`, `chunk_origins`를 먼저 조립합니다.
2. **2단계 — 답변 생성 및 즉시 검증**: 1단계 입력 JSON과 4절 기준 예제를 Teacher Prompt에 넣어 `assistant` 응답만 생성하고, 바로 `validate_qlora_dataset.py`를 통과한 행만 저장합니다.

---

## 6. 공통 Teacher & 구조화 Critic Prompt

### A. `solution` / `hold` 답변 생성용 Teacher Prompt
```text
당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'의 학습 데이터 생성기입니다.
이미 확정된 입력 JSON(SLMRequest)만 보고 한국어 assistant 응답을 작성하세요.

[절대 규칙]
1. 입력의 allowed_evidence_refs에 포함된 ID만 [ID] 형식으로 인용하고, distractor_refs와 미제공 ID는 절대 인용하지 마세요.
2. synthetic_defense_probe 청크는 인용하지 말고 그 수치·문장을 임상 효능으로 단정하지 마세요.
3. 피부 질환 진단, 치료/임상 효과 단정, 미공개 성분 농도·pH 추측을 금지합니다.
4. 확인되지 않은 정보나 제품 버전 불일치는 미상(unknown) 또는 보류로 명시하세요.
5. mode="solution"은 '### 핵심 안내' → '### 근거 및 이유' → '### 확인이 필요한 한계' 3단 구조로 작성하세요.
6. mode="hold"는 개별 루틴·제품·세안/도포 지시·대체 후보를 절대 작성하지 말고 '### 개별 권고 보류 안내' → '### 필요한 다음 단계' 2단 구조로만 작성하세요.
7. 어조는 차분한 '~해요' 존댓말로 통일하세요.
```

### B. Cross-Model 구조화 `Critic` Prompt (검수 완료 기록 분리)
교차 검수 시 Critic 모델에는 `SLMRequest`뿐 아니라 **`chunk_origins`, `card_ids`, 기대 판정 근거(`kb_judgments`)를 함께 전달**합니다. 자동 검증(`validate_qlora_dataset.py`) 통과와 별개로, 최종 제출(`--require-review`) 시에는 모든 행의 `provenance.critic_status == "PASS"`(다른 모델)와 고위험 사례(`hold`·`version_mismatch_or_unknown`) 10% 이상의 `provenance.human_review == "approved"` 기록이 필요합니다.

```text
당신은 Ppopy 합성 데이터 품질 감사관입니다.
함께 전달된 [1] SLMRequest 입력 JSON, [2] chunk_origins, [3] card_ids 및 기대 판정 근거, [4] assistant 응답을 아래 6개 규칙으로 검수하고, 행별 JSON을 반환하세요:
{"row_id": "...", "decision": "PASS" | "FAIL", "violated_rule": null | "R1_CITATION" | "R2_CLINICAL" | "R3_UNKNOWN_VERSION" | "R4_HOLD_LEAK" | "R5_INPUT_JUDGMENT" | "R6_FORMAT_TONE", "offending_span": "...", "evidence_ref": "..."}

- R1_CITATION: 입력에 없는 근거·비표준([S99] 등)·distractor_refs·synthetic_defense_probe 인용
- R2_CLINICAL: 피부 질환 진단, 임상/치료 효과 단정, 소규모 연구 수치의 효능화
- R3_UNKNOWN_VERSION: 미공개 농도/pH 추측 또는 버전 불일치 제품 사용법 채택
- R4_HOLD_LEAK: mode="hold"에서 루틴·제품·세안/도포 지시·대체 후보 누출
- R5_INPUT_JUDGMENT: confirmed_observations와 KB 카드의 실제 comparison_spec·mode 판정 모순, 또는 파일럿 버킷(`unknown_or_version`, `distractor_or_defense`)의 실질 시나리오 부재/복붙 중복
- R6_FORMAT_TONE: '~해요' 어조 위반 또는 지정 헤더 누락
```

---

## 7. 공통 검증기 실행 명령 (단독 · 36턴 파일럿 병합 · 최종 제출)

모든 명령은 `courses/ai-applications/experiments/cos-agent` 디렉터리에서 실행합니다.

```bash
# 1) 파일럿 단독 검증 (정확히 12행: solution 9 / hold 3, pilot_bucket 4종 × 3행)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
  --shard a --pilot

# 2) 파일럿 3인 병합 검증 (A/B/C 3개 파일, 총 36행 — 대량 생성 착수 게이트)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
          data/qlora/v2/shards/shard_b_moisturizing.jsonl \
          data/qlora/v2/shards/shard_c_sun_product.jsonl \
  --merge --pilot --require-review

# 3) 본 생성 완료 후 최종 3인 병합 검증 (비율·누수·교차검수·사람표본검수 모두 강제)
uv run --locked python scripts/validate_qlora_dataset.py \
  --input data/qlora/v2/shards/shard_a_cleansing.jsonl \
          data/qlora/v2/shards/shard_b_moisturizing.jsonl \
          data/qlora/v2/shards/shard_c_sun_product.jsonl \
  --merge --enforce-ratios --require-review --report outputs/qlora_validation_report.json
```

---

## 8. Linear Issue 복붙용 템플릿 (중복 제거 · 단일 기준 참조)

### Parent Issue
- **제목**: `[QLoRA Data] Ppopy v3 SOLUTION+HOLD 합성 데이터셋 구축 (36턴 파일럿 → 2,100턴 병합)`
- **본문**:
```markdown
## 기준 커밋 및 단일 실행 기준 (Single Source of Truth)
- **공통 기준 커밋 SHA**: `<BASE_COMMIT_SHA>` *(PR 머지 후 기입)*
- **가이드**: `courses/ai-applications/experiments/cos-agent/docs/qlora-synthetic-dataset-guide.md`
- **공통 검증기**: `courses/ai-applications/experiments/cos-agent/scripts/validate_qlora_dataset.py`

## 착수 게이트
1. 3인 전원 `<BASE_COMMIT_SHA>`에서 담당 브랜치를 생성하고 12턴 파일럿(`pilot_bucket` 4종 × 3턴)을 작성합니다.
2. 3개 파일럿을 합쳐 **`--merge --pilot --require-review` `error_count == 0`** 통과 후 본 생성(총 2,100턴)을 시작합니다.
```

### Sub-issue A / B / C (팀원별 담당만 기입)
```markdown
- **규칙 기준**: Parent Issue의 `<BASE_COMMIT_SHA>` 및 `docs/qlora-synthetic-dataset-guide.md`
- **Shard A**: `data/qlora-shard-a` · `data/qlora/v2/shards/shard_a_cleansing.jsonl` · `syn-a-` · 세정(`B-C01`~`06`) + `B-I01` + `v67` 재가공 · 목표 `600`/`200` · Critic: 팀원 2 AI
- **Shard B**: `data/qlora-shard-b` · `data/qlora/v2/shards/shard_b_moisturizing.jsonl` · `syn-b-` · 보습(`B-M01`~`05`) + 활성성분 중첩(`B-G13`~`15`, `B-I04`) + 도입(`B-G11`~`12`) · 목표 `500`/`150` · Critic: 팀원 3 AI
- **Shard C**: `data/qlora-shard-c` · `data/qlora/v2/shards/shard_c_sun_product.jsonl` · `syn-c-` · 자외선차단(`B-P01`~`09`, `B-P07` 제외) + 날씨/UV + 버전 불일치 + 보관/품질 보류(`B-S*`) · 목표 `500`/`150` · Critic: 팀원 1 AI
```
