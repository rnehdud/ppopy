# QLoRA 파일럿 · 개정 3 · 사용자 발화와 시스템 근거 분리

## 개정 3에서 바로잡은 내용

24건의 노란 말풍선을 일상적인 질문으로 다시 썼어요. 제품 ID·버전·확인 상태는 사용자가 말하게 하지 않고 카탈로그 근거와 별도 `system_context`에 두었어요. 답변 5건에서도 제작용 ‘합성 제품’ 표현을 제거했으며, 합성 여부는 검토용 메타데이터에 계속 명시해요.

각 사례의 `user_utterance`는 현재 질문, `prior_user_confirmations`는 별도로 확인한 사용자 응답을 나타내는 합성 설정, `observation_trace`는 슬롯과 발화의 연결, `system_context`는 가상 카탈로그 확인의 작성 이력이에요. 실제 사용자 기록·실제 조회·NLU/AFA 실행 결과로 주장하지 않아요.

- 통증·불편이 없다는 값은 초기 질문에 덧붙이지 않고, 그 값을 뒷받침하는 별도 합성 응답에 연결했어요.
- 확인하지 않은 사용 행동·의료진 계획 전문은 `not_asked`로 남겼어요. 사용자에게서 미수집한 정보를 ‘없음’으로 만들지 않았어요.
- 제품 ID·버전·버전 일치 여부는 사용자 관찰 슬롯에서 제거했어요. 사용한 부위가 ‘팔’인 경우 아래팔로 좁혀 단정하지 않았어요.
- 자연어 발화와 출처 추적표는 **표시·검토용 자료**예요. SLM 학습 JSONL의 user 메시지는 공통 계약대로 정형 `SLMRequest`이며, 이 자연어 문장을 직접 입력하는 NLU 학습셋으로 바꾸지 않았어요.
- 현재 파일럿의 관찰 슬롯은 작성자가 구성한 합성 입력이에요. 이 연결표만으로 실제 앱의 추출·확인 흐름 성능을 증명할 수는 없어요.
- 개정 2의 데이터·코드는 `outputs/qlora_v3_pilot_20261125/revision_03/before/`에 보존했어요. 변경 전후 raw와 미수집·시스템 메타데이터 정리는 같은 폴더의 변경 기록에 남겼어요.

## 현재 상태

- 대상 학습 모델: 사용자가 지정한 `Qwen/Qwen3-4B-Instruct-2507`. QLoRA 학습 자체는 실행하지 않았어요.
- 기준: [PPO-37](https://linear.app/ppopy/issue/PPO-37) 갱신 시각 `2026-11-24T15:39:56.847Z`, [PPO-40](https://linear.app/ppopy/issue/PPO-40), [PPO-42](https://linear.app/ppopy/issue/PPO-42).
- 코드 기반: 최신 `origin/main`의 `2b2063c24bfec5f9c63ce84265d8e0189d48fde2` (PR #30 병합). 작업 중 새 병합을 확인해 작업 브랜치 `data/qlora-v3-rag-free`를 fast-forward했어요. 최초 입력 작성 기반은 `5b67684`였으며 요청 계약·검증기는 두 커밋에서 같아요.
- 코퍼스 기반: `origin/codex/reference-corpus-20261124`의 고정 커밋 `dd418a3185aa94bc3eb118af268b53647c9d73e5`.
- **Step 1용 Tier 1 샘플 문헌이에요. 공식 PPO-42 변환 풀·검색기 인계 완료가 아니에요.** 파일럿의 임시 ref ID를 최종 검색기의 ID라고 부르지 않아요.
- `development_preview`, `production_enabled=false`, 합성 입력 전용이에요. Critic·사람 검수는 전부 미검수 상태예요.

### Git 검수 인계 범위

현재 브랜치는 **제작·구조 검증 완료 / 외부 Critic·사람 검수 대기** 상태의 인계 자료예요. `reviews/pilot_24_critic.jsonl`은 실제 다른 모델 계열의 검수 전에는 만들지 않아요. 사람이 검수하기 전 `human_review=approved`로 바꾸지 않아요. 구조 통과를 학습 승인이나 병합 승인으로 해석하지 않아요.

`validation/`에는 현재 JSONL과 해시가 일치하는 구조·코퍼스 추적·Qwen 토큰 실측 보고서 및 결과 receipt를 공유해요. HTML·PNG·ZIP과 이전 버전 전체 보관본은 Git 제외 경로인 `outputs/`에만 있고, 이 브랜치의 push에 포함되지 않아요.

새 clone에서는 로컬 과거 보관본 없이 고정 입력·응답과 공개 변경 이력의 해시를 대조해 재조립할 수 있어요. 코퍼스 추적 검사는 저장소 역사에 있는 `dd418a3`를 읽으므로 shallow clone에 해당 커밋이 없으면 먼저 fetch해야 해요. 선택적인 이미지 생성에는 Pillow와 코드에 지정한 한국어 폰트가, 토큰 재측정에는 보고서에 기록한 Transformers·tokenizers·huggingface_hub가 별도로 필요해요. 기본 구조·코퍼스 검사는 기존 `uv --locked` 환경을 사용해요.

## 개정 2에서 반영한 코퍼스 변경 · 현재도 유지

개정 2에서 짧게 새로 쓴 요약 대신, 위 코퍼스의 Tier 1 문단을 본문·URL·위치·확인일·범위·한계와 함께 그대로 연결했어요. solution 18건의 입력·답변·인용을 갱신했고, 당시 HOLD 6건은 관찰·응답을 유지했어요. 개정 3에서도 RAG 문단은 바꾸지 않았어요. aa1bf19 및 v67 데이터는 재가공하지 않았어요.

각 문단의 원본 Git 커밋·파일 경로·문단 위치·파일 및 본문 해시는 `pilot_24_source_registry.json`에 있어요. 선택한 문단은 17개, 데이터에 등장하는 청크는 총 24개예요(관련 문헌 18개와 방해 문헌 6개 등장). 이것은 전체 151문단을 최종 청크 풀로 변환했다는 뜻이 아니에요.

- 영어 공식 자료 발췌는 `reference_excerpt`로 구분하고 번역하지 않았어요.
- 한국어 코퍼스 문단은 koody가 출처의 사실을 새로 설명한 내용이므로 `kb_source_summary`로 구분했어요. KB 카드 판정에서 가져온 요약이라는 뜻은 아니에요.
- 출처와 재사용 조건 등록부: [고정 커밋의 SOURCES.md](https://github.com/rnehdud/ppopy/blob/dd418a3185aa94bc3eb118af268b53647c9d73e5/courses/ai-applications/experiments/cos-agent/data/rag/SOURCES.md). 원문 PDF나 전체 페이지 캡처를 추가하지 않았어요.
- 최신 PPO-42의 논문 영어 요약 요구와 기존 코퍼스의 논문 발췌가 다르므로 **이번에는 Tier 2 논문을 사용하지 않았어요.** 다른 팀원의 코퍼스나 정책 파일은 수정하지 않았어요.
- 선택한 문단 길이를 맞추려고 원문을 임의로 늘리지 않았어요. 코퍼스 전체의 분량·문장 수 정합화는 코퍼스 담당 작업이며, 이번 24턴의 구조 검증과 구분해요.

## 구성

| 버킷 | 행 수 | 모드 |
|---|---:|---|
| `normal_guidance` | 6 | solution |
| `unknown_or_version` | 6 | solution |
| `distractor_or_defense` | 6 | solution |
| `hold` | 6 | hold |
| 합계 | 24 | solution 18 / hold 6 |

- solution은 세정·보습·자외선차단 각 6건이에요. 보습 제품의 기한 확인에는 보관·국내표시 문단도 연결했어요.
- 영어 문헌을 허용 근거로 포함한 solution은 6/18건(33.3%)이에요. 방해 청크의 영어는 이 비율에서 제외해요.
- Hard Negative는 8건: 버전 미상 2건, 무관 문헌 무시 4건, 타인 보고 구분 2건이에요.
- 분할은 `train` 22건 / `val_internal` 2건이에요. 이는 내부 파일럿 분할이며 독립 성능 평가 결과는 아니에요.
- 모든 행은 `source_origin=new_synthetic`, 원본 시나리오·턴 계보는 `null`이에요. 기존 신규 합성 파일럿의 개정이며 구 KB-anchored 자료의 재활용이 아니에요.
- 사람 확인은 `human_review=unreviewed`, Critic은 `critic_status=unreviewed`, `critic_model=null`이에요. 생성 모델 표기는 Codex의 공개된 계열 `gpt-6`이며, 학습 대상 모델 이름과 다를 수 있어요.

## 계약 경계

user JSON에는 `kb_judgments` 키를 넣지 않고 assistant에는 `[kb:...]`를 인용하지 않아요. 장문 `decision_context` 대신 관찰·실제 행동·날씨 예보·UV 미상·타인 보고를 정형 슬롯으로 나눠요. 예보는 현재 노출로, 타인 증상은 본인 증상으로, 미상은 없음으로 바꾸지 않아요.

가상 제품은 `synthetic_product=true`로 표시하며 실재 상품의 농도·pH·효능을 만들지 않아요. 현재 버전이 불명확한 이전 자료는 `usage_held`이고, 현재 제품의 근거로 인용하지 않아요. HOLD에는 문헌·루틴·도포·세안·제품 추천을 넣지 않아요.

`KB/`, `docs/source-manifest.json`, `beauty_agent/`, 공통 검증기·가이드·잠금 파일은 수정하지 않았어요.

## 파일·재현·보존

| 파일 | 역할 |
|---|---|
| `pilot_24.jsonl` | 현재 24턴 파일럿 |
| `pilot_24_inputs.json` | 자연어 질문·별도 확인·관찰 출처·카탈로그 이력·고정 입력과 해시 |
| `pilot_24_responses.json` | 입력에 맞춰 작성한 응답 |
| `pilot_24_source_registry.json` | 코퍼스 문단과 ref ID의 추적 정보 |
| `pilot_24_change_log.json` | 행별 변경 여부·이유·변경 전후 입력 해시 |
| `pilot_24_review.md` | 입력·문헌·응답 raw 펼침 자료, 검수 PASS 보고서가 아님 |

이전 파일럿 6개 파일과 해시는 `outputs/qlora_v3_pilot_20261125/revision_02/before/`에 그대로 보존했어요. 코퍼스와 제품 표시를 맞추면서 7번 입력을 보완한 전후 raw도 `revision_02/gel_alignment_change.json`에 남겼어요. 과거 검수 PASS를 재사용하지 않았어요.

다음 명령은 cos-agent 디렉터리 기준이에요.

```powershell
uv run --locked python data/qlora/v2/build_rag_free_pilot.py assemble
uv run --locked python scripts/verify_pilot_corpus_alignment.py
uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/pilot_24.jsonl --pilot --report outputs/qlora_v3_pilot_20261125/revision_03/pilot_structure.json
```

`refresh_corpus_pilot.py`는 보관된 이전 입력에서 개정 입력을 만드는 기록이며 이미 고정된 개정 입력의 재생성을 거부해요. 일반 재현에는 위 조립 명령을 사용해요. 사람 검수용 상황 원문은 실제 모델 입력 JSON을 대신하지 않아요.

`naturalize_pilot_context.py`와 `write_corpus_pilot_responses.py`는 로컬 보관본에 의존하는 제작 이력용 도구예요. 새 clone의 검수·재현에는 실행할 필요가 없어요. 고정 입력과 응답을 수정하지 않고 재조립하려면 `build_rag_free_pilot.py assemble`을 사용해요. 검수 후에는 재조립 스크립트를 무작정 실행해 검수 상태를 초기화하지 말고, 변경 내용으로 다시 검수해야 해요.

## 이후 단계

구조 오류 0건에서 Step 1 생성을 멈춰요. 다른 팀원 모델의 Cross-Model Critic과 사람의 24건 전수 확인이 남아 있어요. 공식 PPO-42 `chunks.jsonl` 인계 후에는 ref ID·본문·URL·한계를 실제 풀과 대조하고 필요하면 파일럿을 다시 갱신해야 해요. 팀 확인·실제 풀 수령 전에는 900턴이나 본 학습을 진행하지 않아요.
