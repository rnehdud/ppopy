# Cross-Model Critic 검수 보고서 (`data/qlora-v2-dataset` · 648턴)

- **검수 일시**: 2026-11-24
- **대상 브랜치 / 커밋**: `origin/data/qlora-v2-dataset` (`179cc35`)
- **생성 모델 (Generator)**: `gpt-6.1-sol` (116턴), `gpt-6.1-terra` (532턴)
- **교차 검수 모델 (Cross-Model Critic)**: Gemini 계열 (`gemini-cross-critic`, GPT 계열과 상이)
- **검수 범위 및 방법**:
  1. **전수 자동·의미 스캔 (648턴 전체)**: `validate_qlora_dataset.py --enforce-ratios`, `validate_qlora_guidance_rules.py`, 임상 수치(`%`)·`usage_held` 설명 누락·`hold` 루틴 누출·`distractor_refs` 노출·원문 복붙(`guidance_verbatim_copy`)·`constraints.decision_context` 장문 편법 정량 스캔.
  2. **전수 원문 정밀 검수 (`pilot_24.jsonl` 24턴 전체)**: 24턴 각각의 입력 관찰, KB 판정, `rag_chunks`, `chunk_origins`, `assistant` 응답을 `R1_CITATION`~`R6_FORMAT_TONE` 기준으로 1:1 검수.
  3. **계층 표본 원문 검수 (`additional_*` 624턴 중 18턴 + 특수 플래그 4턴)**: 각 파일의 처음·중간·끝 3행씩(18턴) 및 `%` 수치 포함 3턴(`syn-sol-0103`, `0107`, `0111`), 예외 플래그 1턴(`syn-sol-0034`) 직접 검수.

---

## 1. 종합 판정 요약

| 구분 | 판정 | 핵심 근거 |
| --- | --- | --- |
| **안전·인용·규율 (`R1`~`R4`)** | **매우 우수 (PASS)** | 648턴 전체 `error_count: 0`, 비표준/미제공/방해 청크 인용 **0건**, `hold` 추천 누출 **0건**, 임상 과잉 단정 **0건** (`%` 포함 3건 모두 한계/금지 설명). |
| **`pilot_24.jsonl` (24턴)** | **24 / 24 PASS** | 4개 버킷 모두 충실히 구현, 자연스러운 `~해요` 어조 및 근거·한계 설명 우수. 외부 Critic 파일 `reviews/pilot_24_gemini_critic.jsonl` 생성 완료 (`human_review` 승인만 남음). |
| **`additional_100_terra*` / `additional_200_terra`** | **개선 권고 (품질·다양성 주의)** | 안전 위반은 없으나 **KB `guidance` 문장 그대로 복붙(`guidance_verbatim_copy`)**과 **`constraints.decision_context` 장문 자연어 편법**이 대량 발견됨 (아래 3절 상세). |

---

## 2. `pilot_24.jsonl` (24턴) Cross-Model Critic 결과 — **24/24 PASS**

> 외부 검수 파일 저장 경로: `courses/ai-applications/experiments/cos-agent/data/qlora/v2/reviews/pilot_24_gemini_critic.jsonl`

| ID | Mode / Bucket | Cards | HN Type | Critic 판정 | 검수 소견 |
| --- | --- | --- | --- | :---: | --- |
| `syn-sol-0001` | `solution` / `normal_guidance` | `B-C01` | - | **PASS** | `v67` 시드 기반 미온수 유지·온도 미추정 정확 |
| `syn-sol-0002` | `solution` / `normal_guidance` | `B-I01` | - | **PASS** | 광보호 유지 미확인(`unknown`)과 합성 제품 표시 구분 명확 |
| `syn-sol-0003` | `solution` / `normal_guidance` | `B-M01` | - | **PASS** | 시간 제한 임의 생성 금지 및 `ref:S04` 한계 준수 |
| `syn-sol-0004` | `solution` / `normal_guidance` | `B-I02` | - | **PASS** | `ref:S09` 영상 대리지표 한계·손바닥 사전 혼합 불가 명시 |
| `syn-sol-0005` | `solution` / `normal_guidance` | `B-P03` | - | **PASS** | 야외·발한 재도포 검토 및 `ref:S16` 실내 일률 적용 금지 |
| `syn-sol-0006` | `solution` / `normal_guidance` | `B-G13` | - | **PASS** | `ref:S32`/`ref:S33` 화장품·의약품 범위 구분 정확 |
| `syn-hold-0001` | `hold` / `hold` | `B-B01` | - | **PASS** | `v67` 지속 불편감 보류, 원인 미추정·추천 누출 0건 |
| `syn-hold-0002` | `hold` / `hold` | `B-B01` | - | **PASS** | 반복 불편감·중등도 통증 보류, 진단/처방 회피 |
| `syn-hold-0003` | `hold` / `hold` | `B-S04` | - | **PASS** | 색·냄새 변화 시 사용 중단 및 오염 확정 회피 |
| `syn-hold-0004` | `hold` / `hold` | `B-Q04` | - | **PASS** | `v67` 누수·개봉 봉인 보류, 가품 확정 회피 |
| `syn-hold-0005` | `hold` / `hold` | `B-B01` | - | **PASS** | 의료진 지시(`apply_on_dry_skin`) 우선 보류 정확 |
| `syn-hold-0006` | `hold` / `hold` | `B-S04` | - | **PASS** | 층 분리 신규/정상 제형 미상 시 보수적 중단 |
| `syn-sol-0007` | `solution` / `unknown_or_version` | `B-C04` | `version_mismatch_or_unknown` | **PASS** | `product.ph` 미상 유지, `ref:S07` 순함 보증 금지 |
| `syn-sol-0008` | `solution` / `unknown_or_version` | `B-P01` | `version_mismatch_or_unknown` | **PASS** | `usage_held` v1→v2 적용 금지 정확 |
| `syn-sol-0009` | `solution` / `unknown_or_version` | `B-P08` | `version_mismatch_or_unknown` | **PASS** | 기한/개봉일 미상 시 만료·SPF 감소율 추정 금지 |
| `syn-sol-0010` | `solution` / `unknown_or_version` | `B-G14` | `version_mismatch_or_unknown` | **PASS** | 처방 레티노이드 + BHA 실제 병용 미확인(`unknown`) |
| `syn-sol-0011` | `solution` / `unknown_or_version` | `B-G11` | `version_mismatch_or_unknown` | **PASS** | `ref:S35` 소부위 확인과 의료 패치테스트 구분 정확 |
| `syn-sol-0012` | `solution` / `unknown_or_version` | `B-G15` | `version_mismatch_or_unknown` | **PASS** | 단일/별도 제품 미상 시 자동 금지·적합 회피 |
| `syn-sol-0013` | `solution` / `distractor_or_defense` | `B-C01` | `rag_distractor_ignore` | **PASS** | 방해 청크 `ref:S21`(손 보습) 완전 무시 |
| `syn-sol-0014` | `solution` / `distractor_or_defense` | `B-G14` | `clinical_restraint` | **PASS** | `ref:S12` *"100% 개선"* 거짓 방어 청크 완전 무시 |
| `syn-sol-0015` | `solution` / `distractor_or_defense` | `B-G01` | `rag_distractor_ignore` | **PASS** | 방해 청크 `ref:S10`(수면 노화) 완전 무시 |
| `syn-sol-0016` | `solution` / `distractor_or_defense` | `B-P06` | `negation_or_other_subject` | **PASS** | `ref:S41`(눈 세척) 방해 청크 무시, 오탐 보류 없음 |
| `syn-sol-0017` | `solution` / `distractor_or_defense` | `B-P02` | `rag_distractor_ignore` | **PASS** | 귀 도포 누락 안내, `ref:S21` 방해 청크 완전 무시 |
| `syn-sol-0018` | `solution` / `distractor_or_defense` | `B-C04` | `version_mismatch_or_unknown` | **PASS** | `ref:S12` *"pH 5.5 확정"* 거짓 방어 청크 완전 무시 |

---

## 3. 나머지 624턴 전체 스캔 및 표본 검수에서 발견된 품질 이슈

자동 검증기(`validate_qlora_dataset.py` & `validate_qlora_guidance_rules.py`)는 **648턴 모두 통과**했으나, QLoRA 학습 품질 관점에서 아래 **2가지 구조·다양성 문제**가 후반 배치(`terra*`, `additional_200_terra`)에 집중되어 있습니다.

| 파일명 | 행 수 | `guidance` 원문 그대로 복붙 | `constraints.decision_context` 장문(>35자) | 단문 응답(<220자) |
| --- | ---: | ---: | ---: | ---: |
| `pilot_24.jsonl` | 24 | **0** | **0** | 6 *(전원 `hold`)* |
| `additional_24.jsonl` | 24 | **0** | **0** | 0 |
| `additional_100.jsonl` | 100 | 7 | 2 | 9 |
| `additional_100_terra.jsonl` | 100 | 24 | 0 | **91** |
| `additional_100_terra2.jsonl` | 100 | 38 | 0 | **96** |
| `additional_100_terra3.jsonl` | 100 | 28 | **32** | **99** |
| `additional_200_terra.jsonl` | 200 | **151 (75.5%)** | **67 (33.5%)** | **125** |

### 발견 이슈 상세
1. **`### 핵심 안내` 앵무새 복붙 및 1줄 상투구 수렴 (248건 / 특히 `additional_200_terra` 75.5%)**
   - `additional_100_terra3.jsonl` 및 `additional_200_terra.jsonl` 표본(`syn-sol-0285`, `0292`, `0346`, `0347`, `0394` 등)에서 `kb_judgments[0].guidance` 문장을 **`### 핵심 안내`에 토씨 하나 안 바꾸고 그대로 복사**하고, `### 근거 및 이유`와 `### 확인이 필요한 한계`도 매 행 거의 동일한 1줄 문장(*"일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요."*)으로 채움.
   - **학습 리스크**: 이 데이터를 그대로 학습하면 `Qwen 3.5 4B`가 자연스러운 설명 대신 `kb_judgments` 문장을 기계적으로 앵무새처럼 되풀이하는 모델로 수렴합니다.
2. **`constraints.decision_context`에 장문 한국어 설명 몰아넣기 (101건 / `terra3` 32%, `200_terra` 33.5%)**
   - `confirmed_observations`의 정형 KB 슬롯(`cleansing.steps`, `method.current_routine` 등)을 채우는 대신 `constraints.decision_context.value`에 `"운동 전 얼굴을 한 번 씻고 운동하여 땀이 난 뒤 다시 얼굴을 씻었습니다..."` 같은 1~2문장 설명을 통째로 넣음.
   - **학습 리스크**: 실제 런타임(`runtime.py`)은 정형 슬롯 dict를 넘기므로 **학습–추론 입력 불일치(Train–Inference Skew)**를 유발합니다.
3. **안전·인용 플래그 (`%` 포함 3건 & `syn-sol-0034`) 확인 결과 — 이상 없음**
   - `syn-sol-0103`(10%), `syn-sol-0107`(5%), `syn-sol-0111`(0.3%)은 모두 *"과장/추측 금지 및 의약품 표시 범위 한정"* 설명으로 **정상 PASS**.
   - `syn-sol-0034` 역시 흔들어 쓰는 이중층 정상 제형 예외 안내로 **정상 PASS**.

---

## 4. Stage-1 (900턴) 완성을 위한 권장 조치

1. **`pilot_24.jsonl` 사람 승인 마무리**: 24행 모두 Gemini Cross-Model Critic PASS 상태이므로, 팀원이 24행 확인 후 `human_review: "approved"`만 반영하면 `--pilot --review-file reviews/pilot_24_gemini_critic.jsonl`이 즉시 통과합니다.
2. **기존 `terra` 계열 151~200건 보강 (선택 또는 권장)**: `additional_100_terra3`·`additional_200_terra`의 `guidance` 그대로 복붙 행(151건)과 장문 `decision_context` 행(101건)을 정형 슬롯 + 자연스러운 2~3문장 안내로 리라이팅하면 4B 모델의 표현력이 크게 좋아집니다.
3. **잔여 +252턴은 `v67` 재가공 중심 확보**: 현재 `recycled_v67`이 3건뿐이므로 `outputs/v67_qlora_seeds.jsonl`에서 **`hold` ~60턴 + `request_draft` ~192턴**을 추가 생성해 900턴을 채우는 것을 권장합니다.
4. **전체 900턴에 대한 Cross-Model Critic 실행**: 최종 병합 파일(`qlora_solution_hold_v2.jsonl`) 완성 후 GPT 외 모델 계열로 전체 검수 파일을 생성해 `--stage1 --review-file`을 최종 통과시킵니다.
