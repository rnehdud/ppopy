# PPO-37 — 24턴 파일럿 생성 초안

기준 커밋은 `53a74a013e2e3533c33ec66d3ed80e0a8ce10bc1`, 작업 브랜치는
`data/qlora-v2-dataset`입니다. `development_preview`,
`production_enabled=false`인 합성 개발 실험에만 사용합니다.

## 2026-11-24 PPO-39 피드백 반영 — 현재 648행

PPO-39의 Gemini 보고서와 기존 고정 기준을 대조해 **275행을 보완**했어요.
작성 담당과 다른 Terra 감사 담당이 실제 입력·응답·전체 카드·저장 출처를 읽었어요.
첫 검수의 216 PASS·59 FAIL과 재수정 이력을 보존하고, 현재 내용 해시로 275 PASS를
확인했어요. 같은 계열 내부 검수이며 수정 행의 새로운 교차계열 검수와 사람 승인은 아직이에요.

- [피드백 처리·275행 수정 전후 raw·원문과 주장 연결](reviews/ppo39_remediation_report.md)
- [재현용 수정 명세와 원문 슬롯 연결](ppo39_revisions.json)
- [현재 275행의 실제 독립 감사](reviews/ppo39_internal_critic.jsonl)
- [Gemini 원래 보고서](reviews/cross_model_critic_report.md) · [파일럿 24행 판정](reviews/pilot_24_gemini_critic.jsonl)

안내 문구 그대로 복사하는 행은 248→0, 35자 초과 `decision_context`는 101→0이에요.
장문을 다른 필드에 통째로 옮기지 않고 원문 관찰별 슬롯에 분리했어요. 새 사실을
추측하지 않고 미상·거절·용도·실제 사용·증상 위치를 구분해요. 최소 글자 수나
성능 개선 기준을 새로 만들지는 않았어요. 기존 0073의 근거 연결과 0281의 미확인
제거 표시 표현도 수정했어요. 과거 입력 부족·명세 질의 전부가 해소됐다는 뜻은 아니에요.

나머지 **373행은 raw 행까지 불변**이고 파일럿 24행·추가 24행은 파일 바이트도 같아요.
KB·시스템 프롬프트·고정 검증기·출처·분할·HN은 변경하지 않았어요.
496 solution / 152 hold, train 569 / val_internal 79, HN 251행,
영어 관련 근거 167/496은 그대로예요. 영어 원문 근거와 기계 식별자를 제외한 새 안내·검토 설명은 한국어예요.

고정 구조·비율 검사 648행 오류 0, 보조 안내 검사 오류 0, 출처 매니페스트 27/27을
확인했어요. 보조 검사의 기존 `syn-sol-0034` 품질 예외는 그대로 기록돼 있어요.
자동 검사는 위의 실제 내용 감사와 별개예요. Gemini의 직접 검수는 변경 없는
파일럿 24행에 유효하며, 전체 648행 직접 검수를 의미하지 않아요. 파일럿 공식 게이트는
사람 승인 **0/24** 때문에 아직 실패해요. v67 재가공은 여전히 3행이고 900행 작업·
사람 검수·팀 확인은 미완료예요. `development_preview`, `production_enabled=false`를 유지해요.

### 현재 재현과 기록

저장소 루트에서 `python courses/ai-applications/experiments/cos-agent/data/qlora/v2/apply_ppo39_feedback.py`로
기준 커밋 `179cc35`와 수정 명세에서 현재 데이터·작성 입력·계획·검수표를 재현해요.
명세 밖 변경이나 사람 승인 기록이 있으면 덮어쓰지 않아요. 이 명령은 감사 판정을 생성하지 않아요.
현재 감사는 각 `reviews/*codex_independent.jsonl`과 위 275행 기록에서 현재 내용 해시로 확인해요.
검증 실행 결과와 변경 전 파일은 `outputs/ppo39_20261124/`에 있어요.
Gemini 보고서 두 파일은 사용자 커밋 `0437d58`에서 받았어요.

아래는 **2026-11-23까지의 역사 기록**이에요. 당시의 ‘현재’ 해시와 불변 범위는
그 시점에 한정돼요. 과거 33행 수정 증거는 바꾸지 않았으며 현재 해시 증거로
소급하지 않아요. 이전 생성·조립 스크립트는 해당 스냅샷 전용이며 PPO-39 재현에는
위 명령을 사용해요. 특히 `assemble_additional_200_terra_reviews.py`는 과거 전용으로
명시 중단하여 옛 승인이 새 내용에 적용되지 않게 해요.

## 과거 기록 — 추가 200턴 원문 확인 뒤 지적 33행 수정

200행을 원문으로 읽은 확인에서 지원 167행, 안내 구체성 15행, HN 분류 불일치
5행, HN 범위 확인 10행, KB 적용 조건 확인 2행, 입력 밖 사실 추가 1행으로
나뉘었어요. 이전 내부 200 PASS가 이 지적을 놓쳤다는 사실을 보존해요.
사용자 요청에 따라 지적 33행만 수정하고 작성 담당과 다른 Terra 담당이 재검수했어요.

- [33행 수정 전후 raw·이유·현재 해시·실제 재검수](corrections_new200_33_20261123.json)
- [현재 33행 독립 재검수](reviews/corrections_new200_33_20261123.jsonl)
- [전체 200행 현재 판정](reviews/additional_200_terra_codex_independent.jsonl)

15행은 검토한다는 말에 머물던 안내를 입력·KB 범위에서 구체화했어요.
HN 분류·범위 지적 15행과 농도 미확인 지적 1행은 관찰을 바꾸지 않고 실제로
무관한 합성 청크를 추가했어요. `rag_distractor_ignore` 16행으로 재설계하고,
`synthetic_defense_probe`·`distractor_refs`에만 배정하여 인용·답변 언급에서 제외했어요.
이는 실제 문헌을 새로 수집·검증했다는 뜻이 아니에요. 현재 HN은 50/200(25%)예요.

`syn-sol-0377`의 미확인 농도를 비공개로 부르던 문구는 제목·판정·답변에서
수정했어요. `syn-sol-0444`는 일반 scope만 보고 difference로 바꾼 중간 수정이
독립 검수에서 FAIL이었어요. 실제 카드 제목과 `combination_pair`의 AHA 한정을
다시 확인해 AHA 해당 여부가 미확인인 이 사례는 `unknown`으로 유지하고,
S32의 일반 주의와 해당 특정 조합의 개별 판정을 구분했어요. KB 자체를 바꾸지
않았으며 일반 scope 문구가 넓게 읽힐 여지는 검수 한계로 남겨요.
`syn-sol-0472`는 손등 사례를 억지로 얼굴 규칙에 넣지 않고 오른쪽 볼 누락이라는
별도의 새 합성 사례로 명시 교체했어요. 원문·이전 입력 해시·이유·기존 가족과 분할을
보존했으며 실제 사용자의 부위를 추정해 바꾼 것이 아니에요.

33행의 첫 독립 재검수는 30 PASS·3 FAIL이었어요. 손 씻기와 관련된 손 보습
청크 두 건을 보관 주제로 바꾸고, 0444를 다시 제한한 뒤 현재 해시로 33 PASS예요.
검수 설명 저장 중 문자 손상을 확인해 판정과 raw를 보존하고 설명을 다시 기록했어요.
초기 지적·중간 실패·손상된 저장본은 삭제하지 않았어요.

기존 448행과 나머지 167행은 그대로예요. 지적 32행의 관찰도 그대로이며
0472만 명시적 새 합성 사례예요. 전체는 여전히 648행(solution 496·hold 152),
추가분은 200행(solution 154·hold 46)이에요. 추가 200행·전체 648행의 구조·비율과
추가 어휘·HOLD 검사는 오류 0건, 소스 매니페스트는 27/27 일치예요.
검사와 내용 재검수는 구분하며 이번에 나머지 167행을 새로 감사했다고 세지 않아요.
실제 검수는 같은 GPT 계열 내부 검수이고 공식 다른 계열·사람 승인은 미완료예요.
`development_preview`, `production_enabled=false`, 공식 검수 `unreviewed`를 유지해요.
커밋·푸시·Linear 갱신은 하지 않았어요.

수정 전 판본·입력 선고정·33행 전후 기록·첫 검수와 재검수·최종 검사·읽기용
HTML/TXT는 Git 제외 경로 `outputs/repair_new200_33_20261123/`에 있어요.
앞선 200행 원문 확인은 `outputs/raw_new200_review_20261123/`에 수정 전 증빙으로
남겨요. 아래 생성 단계의 수치는 당시 이력이며 현재 파일은 위 수정 기록과 현재
내용 해시로 식별해요.

## Terra 추가 200턴 — 33행 수정 전 생성 이력, 당시 합계 648턴

작성 담당과 감사 담당을 분리한 `gpt-6.1-terra` 담당자 3명이 6개 묶음을
교차 검토했어요. 입력을 먼저 고정하고 답변을 작성했으며, 추가분은
**solution 154·hold 46**, 전체는 **solution 496·hold 152**, 총 **648행**이에요.
기존 448행의 6개 데이터 파일은 생성 전후 SHA-256이 모두 같아요.

- [추가 200행 데이터](additional_200_terra.jsonl)
- [200행 입력·답변 전체](additional_200_terra_review.md)
- [고정 입력 계획](additional_200_terra_plan.json), [사람 검수표](additional_200_terra_human_review.csv)
- [행별 독립 검수·raw 근거·주장 연결](reviews/additional_200_terra_codex_independent.jsonl)
- [현재 판정·해시·검사 집계](reviews/additional_200_terra_codex_independent.summary.json)

최초 내용 감사는 **120 PASS·80 FAIL**이었어요. 적용 범위 누락, 인용 범위,
근거 없는 Hard Negative 분류 등을 수정·재검수해 추가 200행은 현재 모두
내부 PASS예요. 초기 데이터·판정은 삭제하지 않았으며, 새 합성 상황으로
교체한 경우 이전 입력 해시와 이유를 남기고 입력을 다시 고정했어요.
`raw_evidence`에는 실제 입력·답변·KB 또는 저장된 청크와 각 주장에 대한
연결 설명을 기록했어요. 저장된 문헌 요약은 외부 출판물의 원문 인용이 아니에요.

추가분은 train 166·val_internal 34행이에요. 새 묶음의 판단 가족 151개 중
검증 가족은 17개(11.26%)이며, 같은 가족·그룹은 분할을 공유해요.
Hard Negative는 실제 유형을 확인한 50/200(25%), 관련 영어 근거는
solution 중 52/154(33.77%)예요. 전체는 train 569·val_internal 79행이에요.
추가 200행과 전체 648행의 고정 구조·비율 검사, 전체 추가 어휘·HOLD 검사는
오류 0건이에요. 입력 완전 중복과 가족·그룹의 분할 간 공유도 없어요.
유사 조건을 대조했지만 모든 쌍의 의미적 비중복을 증명했다고 주장하지 않아요.

이는 **동일 GPT 계열에서 담당·문맥을 분리한 내부 감사**예요. 다른 모델 계열
Critic과 사람 승인은 미완료이며 provenance의 공식 검수 상태는 `unreviewed`예요.
기존 44행 원문 검토의 입력 부족 22·사양 부족 6·내용 지적 2건은 이번 추가로
해결된 것이 아니에요. 전체 648행의 의미적 정답·공식 인수 완료를 뜻하지 않아요.
`development_preview`, `production_enabled=false`를 유지하며 학습 실행,
커밋·푸시·Linear 변경은 하지 않았어요.

`cos-agent`에서 실행한 명령이에요. 원본·수정 이력·보존 확인은 Git 제외 경로
`outputs/additional_200_terra/` 및 `outputs/terra200_*`에 있어요.

```powershell
python data/qlora/v2/build_additional_200_terra.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_200_terra.jsonl --enforce-ratios --report outputs/additional_200_terra/additional_200_terra_structural.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl data/qlora/v2/additional_100_terra3.jsonl data/qlora/v2/additional_200_terra.jsonl --enforce-ratios --report outputs/additional_200_terra/combined_648_structural.json
python scripts/validate_qlora_guidance_rules.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl data/qlora/v2/additional_100_terra3.jsonl data/qlora/v2/additional_200_terra.jsonl --report outputs/additional_200_terra/final_behavior_648.json
python data/qlora/v2/assemble_additional_200_terra_reviews.py
```

## 원문 감사 지적 61행 대응 — 당시 448턴

자동 검사 결과를 내용의 정답으로 간주하지 않고 입력·답변·실제 KB 조건·저장된
인용 요약을 다시 읽은 감사의 지적 61행을 처리했어요. **58행은 수정했고 3행은
감사 오탐으로 원본을 유지했어요.** 오탐은 `syn-sol-0040`(미상은 확인된 부정과
반대 관찰이 아님), `syn-hold-0031`·`syn-hold-0033`(안전상 중단은 새 루틴 추천과
다름)이에요. 지적 내용·이전 원문·수정 사유를 삭제하지 않았어요.

수정 담당과 다른 Terra 담당이 61행을 실제 재검수했어요. 인용 귀속과 사용자에게
보이는 내부 용어 등 추가 지적도 고친 뒤 현재 내용 해시로 61행 모두 PASS예요.
이는 **같은 GPT 계열 내부 검수**이며 외부 계열 Critic이나 사람 승인으로 세지 않아요.

- [행별 대응·전후 해시·원문 근거](raw_fix_61_20261123.json)
- [실제 독립 재검수 61행](reviews/raw_fix_61_20261123.jsonl)
- 로컬 전후 전체 원문·검수 이력: `outputs/fix_61_20261123/report.html`,
  `report.txt`, `before_v2/`, `round1/`, `round2/` (Git 제외 경로)

현재 총수는 안내 342·보류 106, **448행**으로 같아요. 390행은 변경하지 않았고
분할·시나리오·그룹·출처 계보와 RAG·제품 근거를 유지했어요. 관찰의 유일한 상태
정정은 `syn-hold-0086`의 제품 버전 답변 거절을 `unknown`에서 `declined`로
복원한 것이며 null 값과 나머지 관찰은 그대로예요. 새 사실을 보충하지 않았어요.
현재 답변 작성 모델은 `generator_model`, 원래 작성자는 `original_generator_model`,
수정자는 `revision_model`에 구분해 기록했어요.

**이전 원문 감사에서 별도 분류한 미해결 44행은 이번 수정 대상이 아니며 그대로
남아 있어요.** 과거 전체 내부 PASS를 현재 448행의 의미적 정답 보증으로 읽지
마세요. 자동 검사와 원문 내용 검토, 외부 원전 확인, 사람 승인은 서로 달라요.
외부 원전 재방문은 수행하지 않았고 저장된 요약을 출판물의 원문 인용으로 부르지 않아요.

`development_preview`, `production_enabled=false`, 사람 검수 `unreviewed`를
유지했어요. 커밋·푸시·Linear 변경은 하지 않았어요. 아래의 생성 단계·당시 보호
해시·PASS 수치는 수정 전 이력이며 현재 판본은 위 대응표로 식별해요.

## Terra 3회차 추가 100턴 — 수정 전 생성 이력, 당시 합계 448턴

사용자 요청으로 작성 담당 3명과 담당을 교차한 독립 감사 담당을 모두
`gpt-6.1-terra`로 명시 지정했어요. 입력을 먼저 저장·고정한 다음 별도 단계에서
답변을 작성했어요. 기존 수정본 348턴의 파일 해시는 모두 그대로 유지했어요.
추가분은 **안내 77·보류 23**, 전체는 **안내 342·보류 106**, 총 448턴이에요.

- [추가 100턴 JSONL](additional_100_terra3.jsonl)
- [전체 입력·응답 확인 자료](additional_100_terra3_review.md)
- [입력 계획](additional_100_terra3_plan.json), [사람 검수표](additional_100_terra3_human_review.csv)
- [현재 100행 감사](reviews/additional_100_terra3_codex_independent.jsonl), [집계](reviews/additional_100_terra3_codex_independent.summary.json)

초기 고정 검증에서 발견한 값 타입 11개를 고쳤고, 미상·응답 거절과 부위별
원래 보고는 유지했어요. A의 최초 감사 27 PASS·7 FAIL, 재검수 32 PASS·2 FAIL,
B의 최초 감사 29 PASS·4 FAIL을 보존했어요. 잘못된 카드 범위·판정·인용 귀속을
수정하고, 눈 노출에 잘못 연결한 카드 사례는 별도의 새 합성 사례로 교체했어요.
새 품질 변화가 확인되지 않은 세 사례도 이전 사실을 추정한 것으로 처리하지 않고
명시적인 새 합성 사례로 교체·재고정했어요. 기존과 같은 판단 가족은 같은
가족·그룹·분할로 묶었어요. 수정·재검수 후 현재 A 34·B 33·C 33행 모두 PASS예요.

추가분은 학습 89·내부 검증 11행, Hard Negative 49/100, 관련 영어 근거는
안내 중 26/77이에요. 전체 448행은 학습 403·내부 검증 45행이에요.
추가 100행과 전체 448행의 고정 구조·비율 검사 및 추가 어휘·HOLD 검사는
오류 0건이에요. 입력 완전 중복과 가족·그룹 분할 간 공유도 0건이며,
현재 감사 100개의 내용 해시가 모두 일치해요. 의미 중복 검토는 유사 조건과
지적된 형제 사례를 대조한 범위이며 모든 쌍의 의미적 비중복을 증명하지 않아요.

이는 **같은 GPT 계열의 내부 감사**예요. 다른 계열 Critic, 파일럿 사람 전수 검수,
팀 인수와 본 데이터 사람 표본 검수는 미완료예요. 공식 provenance는 미검수로
유지했으며 900턴 공식 본 데이터 완료·학습 실행을 뜻하지 않아요.
`development_preview`, `production_enabled=false`를 유지해요.
커밋·푸시·Linear 갱신은 하지 않았어요.

`cos-agent`에서 실행한 재현 명령이에요.

```powershell
python data/qlora/v2/build_additional_100_terra3.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_100_terra3.jsonl --enforce-ratios --report outputs/additional_100_terra3/additional_100_terra3_structural.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl data/qlora/v2/additional_100_terra3.jsonl --enforce-ratios --report outputs/additional_100_terra3/combined_448_structural.json
python scripts/validate_qlora_guidance_rules.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl data/qlora/v2/additional_100_terra3.jsonl --report outputs/additional_100_terra3/final_strict.json
python data/qlora/v2/assemble_additional_100_terra3_reviews.py
```

데이터 SHA-256: `30d5687d25486af2ac3ec050c0dbf7517c03bd3b93f9f44c2da552d3f828766c`.
실행 보고서·수정 전 판본·최종 보존 확인은 Git 제외 경로
`outputs/additional_100_terra3/`와 `outputs/terra3_*`에 있어요.
시스템 Python으로 실행했으며 잠금 환경 재현은 주장하지 않아요.

## 2026-11-23 명시적 사양 수정 — 당시 348턴

현재 판본은 **안내 265턴·보류 83턴**이에요. 아래 생성 단계의 수치와 보존
기록은 이 수정 이전 시점의 이력이에요. 당시 유지했던 기존 파일도 이번 사용자
요청에 따라 명시적으로 수정했으며, 이전 해시와 판정은 삭제하지 않았어요.

- CSV의 통제 어휘 25개 값(24행)을 정규화했어요. 지속·반복 여부가 불명확한
  2개 값은 `unknown`으로 두고, 원래 증상 문장은 실제 입력의
  `skin.distribution.reported_symptom_statements`에 보존했어요.
- `syn-sol-0150` → `syn-hold-0082`, `syn-sol-0221` → `syn-hold-0083`으로
  바꾸고 HOLD 답변을 새로 작성했어요. 관찰·시나리오·그룹·분할은 유지했어요.
- 전체 348행 키워드 검색에서 147개 일치를 기록하고 주요 후보를 대조했어요.
  추가로 확정된 HOLD 오분류는 없었어요. 정상적인 이층 제형과 새 변화가 없는
  `syn-sol-0034`는 유지했어요. 검색만으로 모든 의미적 위험을 증명하지 않아요.
- 고정 구조·비율 검사는 오류 0건, 추가 통제 어휘·HOLD 검사는 수정 전
  27건에서 수정 후 0건이에요. 마니페스트 대상 27개 파일만 LF로 통일했고
  원본 해시 엄격 검사를 통과했어요. 고정 검증기·마니페스트는 바꾸지 않았어요.
- 변경 26행은 작성 담당과 다른 문맥의 `gpt-6.1-terra`가 재검수하여 모두
  PASS예요. **같은 GPT 계열 내부 감사**이며 다른 계열 Critic이나 사람 승인을
  대체하지 않아요. 사람 검수는 여전히 `unreviewed`예요.

[수정·해시·ID 대응 기록](corrections_20261123.json),
[변경 행 재검수](reviews/corrections_20261123_reviews.jsonl),
[수정 전 판정 보존본](reviews/corrections_20261123_before.jsonl)을 참조하세요.
상세 검색·전후 검증 보고서는 Git 제외 경로 `outputs/corrections_20261123/`에 있어요.

고정 구조 검사와 함께 추가 사양 검사를 실행해요(`cos-agent` 기준).

```powershell
python scripts/validate_qlora_guidance_rules.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl --report outputs/corrections_20261123/strict_final.json
```

## Terra 2회차 추가 100턴 — 수정 전 생성 이력, 당시 합계 348턴

사용자 요청에 따라 작성·독립 감사 자식 모델에 모두 `gpt-6.1-terra`를 명시
지정했어요. 기존 248턴의 파일 해시는 유지하고 새 안내 77턴·보류 23턴을
별도 파일로 추가했어요. 전체는 안내 267턴·보류 81턴, 총 348턴이에요.

- [새 100턴 데이터](additional_100_terra2.jsonl)
- [입력과 답변을 읽는 확인 자료](additional_100_terra2_review.md)
- [고정 입력 계획](additional_100_terra2_plan.json), [사람 전수 검수표](additional_100_terra2_human_review.csv)
- [현재 감사 요약](reviews/additional_100_terra2_codex_independent.summary.json), [행별 판정](reviews/additional_100_terra2_codex_independent.jsonl)

### 실제 작성·검수 결과

입력을 먼저 저장·고정하고 다음 작업 단계에서 답변을 작성했어요. 일부 중간
파일의 문자 손상은 `outputs/`로 격리하고 UTF-8 소스로 복구했어요. 최초 전체
구조 검사에서 발견한 보류 제목 16건의 오류도 원본 보고서에 남겼어요.

첫 독립 의미 감사는 **62 PASS·38 FAIL**이었어요. 작성 담당과 다른 문맥의
Terra 감사 담당자가 입력·답변·실제 KB 비교 명세와 출처를 확인했어요.
미확인 의도·시간·변화 종류의 단정, 실제 판정 방향 누락, 의미 중복과
보류 제목을 고쳤고, 최종 입력 재고정 이후 변경 행을 재검수했어요.
최초 PASS 62턴의 내용은 변경하지 않았어요. 보존한 판정 단계는
**62/38 → 96/4 → 99/1 → 100/0**이며 현재 **100 PASS·0 FAIL**이에요.
초기·중간 기록은 `reviews/additional_100_terra2_round1.jsonl`,
`reviews/additional_100_terra2_round2.jsonl`, `reviews/additional_100_terra2_round3.jsonl`에
남기고 현재 기록에서 이전·새 내용 해시와 연결했어요.

추가분은 학습용 90턴·내부 검증용 10턴, Hard Negative 34/100,
관련 영어 청크는 안내 중 26/77이에요. 유형은 실제 불확실성을 반영해 일반
안내 13·미상/버전 45·방해/방어 19·보류 23턴이며 24턴 파일럿의 균등 분배를
100턴에 억지로 적용하지 않았어요. 추가 100턴과 전체 348턴의 고정 구조·비율
검사는 모두 오류 0건이에요. 최종 문자 손상·일본어 검사도 0건이에요.

의미 중복 검토는 카드·관찰 유사 후보와 개별 사례 대조 범위이며 모든 쌍의
의미 중복 전수 증명을 주장하지 않아요. 같은 GPT 계열의 독립 문맥 감사이지
다른 모델 계열 공식 Critic이나 사람 승인은 아니에요. 공식 provenance의
`critic_status`·`human_review`는 `unreviewed`이며 임상 정답·성능 비교나
900턴 본 데이터 공식 인수로 취급하지 않아요.

`cos-agent`에서 최종 조립·검사한 명령이에요.

```powershell
python data/qlora/v2/build_additional_100_terra2.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_100_terra2.jsonl --enforce-ratios --report outputs/additional_100_terra2/additional_100_terra2_structural.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl data/qlora/v2/additional_100_terra2.jsonl --enforce-ratios --report outputs/additional_100_terra2/combined_348_structural.json
python data/qlora/v2/assemble_additional_100_terra2_reviews.py
```

상세 판본·실행 증빙은 Git 제외 경로 `outputs/additional_100_terra2/`,
`outputs/terra2_c/` 등에 있고 최종 보존 확인 결과는
`outputs/additional_100_terra2/final_verification_receipt.json`이에요.
`uv` 부재로 시스템 Python을 사용했으며 잠금 환경 재현을 주장하지 않아요.
커밋·푸시·Linear 변경은 하지 않았어요.

## Terra 첫 추가 100턴 — 당시 합계 248턴

사용자 요청으로 작성·감사 자식 모델을 모두 **`gpt-6.1-terra`로 명시 지정**했어요.
기존 148턴은 그대로 두고 [Terra 초안 100턴](additional_100_terra.jsonl)을 별도로
저장했어요. 안내 77턴·보류 23턴, 학습용 90턴·내부 검증용 10턴이에요.
이제 전체 후보는 안내 190턴·보류 58턴으로 248턴이에요.

- [입력과 답변을 읽는 확인 자료](additional_100_terra_review.md)
- [고정 입력 계획](additional_100_terra_plan.json), [사람 검수표](additional_100_terra_human_review.csv)
- [행별 독립 감사](reviews/additional_100_terra_codex_independent.jsonl), [감사 요약](reviews/additional_100_terra_codex_independent.summary.json)

### 생성·수정·재감사 — 공식 인수와는 별개예요

입력 후보를 소단위로 작성하고 이전 판본을 보관하며 KB 변수·타입과 비율을
수정한 뒤 파일로 고정했어요. 답변은 고정 입력만 읽는 별도 작업 단계에서
작성했고, 각 담당 34·33·33턴의 비답변 필드가 고정 입력과 일치해요.
감사는 작성 담당과 별도 문맥의 Terra 담당자 3명이 수행했어요.

**첫 독립 감사는 46 PASS·54 FAIL**이에요. A는 22/12, B는 11/22,
C는 13/20이에요. 제공된 청크 밖의 내용을 출처에 귀속하는 문제,
입력에 없는 시점·사용 사실, KB 판정 불일치와 의미 중복 등을 기록했어요.
이는 Critic의 검토 판정이지 임상 정답이나 사람의 최종 재판정이 아니에요.
사용자가 Terra 수정·재검수를 승인한 뒤, 입력에 없는 표현은 답변에서 좁히고
판정의 불확실성은 유지했으며 중복은 다른 확인 조건으로 교체했어요.
입력 수정이 필요한 경우 입력을 먼저 재고정한 뒤 답변을 작성했어요.
이전 PASS 46턴은 그대로 보존하고 변경 행은 작성 담당과 다른 Terra가
R1–R6로 다시 확인했어요. 보존한 단계별 기록은 **46/54 → 91/9 → 99/1**이며,
현재 판정은 **100 PASS·0 FAIL**이에요. 수치는 통과/실패 순서예요.
첫 실패와 재지적은 `reviews/additional_100_terra_round1.jsonl`,
`reviews/additional_100_terra_round2.jsonl`, `reviews/additional_100_terra_round3.jsonl`에
있고, 현재 판정의 이전·새 내용 해시와 연결돼요.
일부 경계 판단은 사람의 최종 확인 대상이며, 이 기록을 Sol과 Terra의
통제된 성능 비교나 임상 정확도 측정으로 해석하지 않아요.

구조·어휘·비율 검사는 추가 100턴과 전체 248턴 모두 오류 0건이에요.
구조 통과와 별도로 54 FAIL의 수정·재검수를 수행했어요. 추가분 Hard Negative는 49/100,
관련 영어 청크는 안내 중 25/77이에요. 형식 검사와 의미 검토를 구분해요.

모든 행의 공식 `critic_status`와 `human_review`는 `unreviewed`예요.
같은 GPT 계열인 Terra끼리의 독립 문맥 감사이므로 원래의 다른 모델 계열
공식 Critic 조건을 충족했다고 기록하지 않아요. 사람 승인도 없어요.
`development_preview`, `production_enabled=false`를 유지하고 900턴 본 데이터
착수나 파일럿 공식 인수로 취급하지 않아요.

`cos-agent`에서 실행한 구조 검사 명령은 다음과 같아요.

```powershell
python data/qlora/v2/build_additional_100_terra.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_100_terra.jsonl --enforce-ratios --report outputs/additional_100_terra/additional_100_terra_structural.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl data/qlora/v2/additional_100_terra.jsonl --enforce-ratios --report outputs/additional_100_terra/combined_248_structural.json
python data/qlora/v2/assemble_additional_100_terra_reviews.py
```

조립기는 고정 소배치를 합칠 뿐 모델 호출·검수 승인을 하지 않아요.
`uv`가 없어 시스템 Python을 사용했으며 잠금 환경 재현이라고 주장하지 않아요.
중간 입력과 해시는 `outputs/additional_100_terra/`, `outputs/terra100/`에 있어요.
커밋·푸시·Linear 변경은 하지 않았어요.

## 추가 개발 후보 100턴 — 현재 합계 148턴

사용자 요청에 따라 기존 48턴을 변경하지 않고 [추가 100턴](additional_100.jsonl)을
별도 파일로 작성했어요. 안내 77턴·보류 23턴이며, 현재 합계는 안내 113턴·보류
35턴이에요. 추가분의 학습용은 90턴, 내부 검증용은 10턴이에요.

- [사람이 읽는 입력·응답 확인 자료](additional_100_review.md)
- [입력 계획](additional_100_plan.json), [사람 전수 검수표](additional_100_human_review.csv)
- [독립 Codex 감사 요약](reviews/additional_100_codex_independent.summary.json)

### 실제 진행과 검수 결과

입력 작성 3개 소배치(34·33·33턴), 응답 작성, 별도 문맥 감사 담당을 분리했어요.
A·B 최초 초안은 입력과 답변 문장을 함께 설계했으므로 엄격한 입력 선행으로
표현하지 않아요. 해당 답변은 원문을 읽지 않는 새 담당자가 고정 입력만 보고
다시 작성했어요. C는 입력을 물리적으로 고정한 뒤 응답을 작성했어요.

초기 독립 감사는 **83턴 PASS·17턴 FAIL**이었어요. 9턴은 의미 중복,
5턴은 KB 변수·값의 타입 문제, 3턴은 입력에 없는 구체적 표현 문제였어요.
중복은 사용자 확인에 따라 다른 판단 조건으로 교체했고, 알 수 없는 시간은
임의 수치가 아니라 `unknown`으로 보존했어요. 이후 B82 교체 입력의 문자 손상을
추가 발견해 실패 이력을 보존하고 입력 재고정·응답 재작성·재검수를 했어요.
검수 전 발견한 용기 팽창 중복 교체도 별도 기록했어요.

현재는 변경 행 재검수 후 **100턴 PASS·0턴 FAIL**이에요. 초기 FAIL과 새 해시는
`reviews/additional_100_part_*_codex_history.jsonl` 및
`reviews/additional_100_part_c_codex_independent.history.json`에 보존했어요.
이는 같은 `gpt-6.1-sol` 계열의 독립 문맥 감사이며, **다른 모델 계열 공식 검수와
사람 승인은 미완료**예요. 데이터 행의 공식 `critic_status`·`human_review`는
`unreviewed`로 유지해요. 900턴 본 데이터 착수나 공식 인수를 뜻하지 않아요.

고정 검증기의 추가 100턴과 전체 148턴 `--enforce-ratios` 검사는 모두 오류 0건이에요.
추가분 Hard Negative는 45/100, 관련 영어 청크는 안내 중 27/77이에요.
한국어 청크는 2~4문장 설명체이며 일본어·문자 손상 검사는 0건이에요.
분할 검사는 등록 ID·내용 중복과 가족/그룹을 검사하고, 의미 중복은 별도 감사로
보완했어요. 미노출 최종 평가셋이나 누수 가능성 전체의 수학적 증명은 아니에요.

`cos-agent`에서 다음 명령으로 고정 자료를 조립·확인할 수 있어요.

```powershell
python data/qlora/v2/build_additional_100.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_100.jsonl --enforce-ratios --report outputs/additional_100/additional_100_structural.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl data/qlora/v2/additional_100.jsonl --enforce-ratios --report outputs/additional_100/combined_148_structural.json
python data/qlora/v2/assemble_additional_100_reviews.py
```

`build_additional_100.py`는 현재 고정한 소배치 입력·응답을 조립할 뿐 모델을
호출하거나 새 검수 승인을 만들지 않아요. `build_additional_100_a/b/c.py`와
개별 작성·수정 스크립트는 단계별 작성 이력이므로 최종 자료 복원 명령이 아니에요.
최초 작성기는 최종 데이터가 있으면 실행을 거부해요. 상세 원본·실행 증빙은
Git 제외 경로 `outputs/additional_100/`에 있어요. `uv` 부재로 시스템 Python을
사용했으며 잠금 환경 재현이라고 주장하지 않아요. 커밋·푸시·Linear 변경은 하지 않았어요.

## 추가 개발 후보 24턴 — 기존 자료와 합계 48턴

기존 `pilot_24.jsonl`은 변경하지 않고 `additional_24.jsonl`에 신규 합성
24턴을 추가했습니다. 기존 파일럿의 검수 완료나 900턴 본 학습셋 작업 착수를
뜻하지 않습니다. 각 파일은 안내 18턴·보류 6턴, 네 유형 각각 6턴입니다.
두 파일의 합계는 안내 36턴·보류 12턴으로 총 48턴입니다.

후속 독립 Codex 검수 결과는 `reviews/README.md`에 있습니다. 기존 24턴은
24턴 통과, 추가분도 수정·재검수 후 24턴 통과입니다. `syn-sol-0036`의 관리
역할을 실제 성분 함유 확인으로 확대하는 표현을 표시 목적 범위로 좁혔습니다.
입력과 다른 47턴은 보존했으며 최초 FAIL 이력도 별도로 남겼습니다. 같은 GPT 계열의
검수이므로 다른 모델 계열의 공식 검수와 사람 승인은 여전히 미완료입니다.

- `additional_24_plan.json`: 응답 작성 전에 저장한 두 입력 명세를 대조한 통합 계획입니다.
- `additional_24.jsonl`: 추가 학습 데이터 후보 24턴입니다.
- `additional_24_review.md`: 추가 24턴의 전체 입력·판정 근거·응답을 읽는 자료입니다.
- `additional_24_human_review.csv`: 추가분의 실제 사람 검수 기록을 작성하는 미검수 표입니다.
- `additional_24_part_a_inputs.json`, `additional_24_part_b_inputs.json`: 응답보다 먼저 고정한 입력입니다.
- `additional_24_part_a.json`, `additional_24_part_b.json`: 두 생성 담당자가 작성한 입력·응답 원본입니다.
- `build_additional_24.py`: 입력 고정본을 대조해 추가분과 확인 자료를 조립합니다. 기존 24턴을 덮어쓰지 않습니다.

운동 후 추가 세안의 목적, 손바닥 사전 혼합, 고온 보관, 여러 제품의 동시 변경,
면도·작업 환경과 반복 접촉, 제거 표시의 버전 충돌, 실제 도포 감량, 다른 적용
부위, 정상 이층 제형, 의료진 개별 계획, 단일 복합제품 등을 구별했습니다.
회수·가품 의심 등의 사례도 합성 설정이며 실제 제품의 회수나 진위를 주장하지 않습니다.

추가분의 한국어 청크 18개는 각각 2~3문장이고, 관련 영어 근거는 안내 18턴 중
6턴입니다. 학습용 22턴과 내부 검증용 2턴으로 나누며 면도와 작업 접촉의
검증용 시나리오 가족을 학습용과 공유하지 않습니다. 이 분할은 개발 검증용이지
미노출 최종 성능을 측정한 결과가 아닙니다.

검증 결과는 추가분 24턴의 구조 검사 오류 0건, 합계 48턴의 중복 입력·분할
누수·비율 검사 오류 0건입니다. 별도 문맥의 Codex 내부 확인에서도 차단할
의미상 문제는 발견하지 않았습니다. 이후 새 독립 Codex 검수에서는 위의
수정 필요 1건을 발견했고 해당 응답 수정 뒤 재검수에서 통과했습니다. 두 검토는 모두 같은 모델 계열이며 다른 모델
계열의 공식 검수나 사람의 승인이 아닙니다. 데이터 검수 상태는 미검수로 유지합니다.

`cos-agent` 디렉터리에서 다음 명령을 실행합니다.

```powershell
python data/qlora/v2/build_additional_24.py
python scripts/validate_qlora_dataset.py --input data/qlora/v2/additional_24.jsonl --pilot --report outputs/additional_24/structural_validation.json
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl data/qlora/v2/additional_24.jsonl --enforce-ratios --report outputs/additional_24/combined48_validation.json
```

`--pilot`은 24행 형식 검사를 재사용하는 것이며 추가분의 공식 인수 승인을
뜻하지 않습니다. 48턴을 한꺼번에 검사할 때는 24행 전용인 `--pilot` 대신
위와 같이 일반 다중 파일 검사와 비율 검사를 사용합니다. 검증기와 원래의
파일럿 기준은 수정하지 않았습니다.

추가 생성·검증의 원본 해시와 결과는 `outputs/additional_24/`에 있습니다.
이번 추가 작업은 커밋·푸시·Linear 변경을 하지 않았습니다.

## 수록 파일

- `pilot_24_plan.md`, `pilot_24_plan.json`: 입력 구성·근거·계보와 입력 해시입니다. 내부 검토에 따른 변경은 이전 버전과 사유를 보존했습니다.
- `pilot_24_responses.json`: Codex가 작성한 응답 초안 24개입니다.
- `pilot_24.jsonl`: 고정 시스템 프롬프트, 입력과 응답을 결합한 학습 데이터 후보입니다.
- `pilot_24_review.md`: 사람이 전체 입력과 응답을 읽는 확인 자료입니다.
- `pilot_24_human_review.csv`: 실제 검수자·날짜·판정·의견을 기록하는 미검수 표입니다. 작성 전 승인은 없습니다.
- `render_pilot_24_review.py`: 확인 자료를 UTF-8로 생성합니다. 원본 데이터와 사람의 기록은 변경하지 않습니다.
- `build_pilot_24.py`: 작성된 입력과 응답을 조립합니다. 모델 API나 학습을 실행하지 않습니다.

## 구성과 사용 범위

총 24턴으로 안내 18턴, 보류 6턴입니다. 일반 안내, 보류, 미확인·버전 불일치,
방해 근거·과잉 주장 방어를 각각 6턴씩 담았습니다. 식별자는
`normal_guidance`, `hold`, `unknown_or_version`, `distractor_or_defense`입니다.
v67 재가공 3턴은 원본 관찰·분할·계보를 보존하고 신규 합성은 21턴입니다.
`test_internal`은 학습 예제로 사용하지 않습니다.

KB 판정은 비교 명세에 따른 합성 설계이며 엔진 실행 결과, 전문가 정답이나
임상 결과가 아닙니다. 출처 정보는 기존 KB 등록값으로 새로운 문헌 확인을
뜻하지 않습니다. 개정 4에서는 방해 문장 본문과 KB 안내에서 정답을 직접 알려주는
메타 힌트를 제거했습니다. 감사용 `synthetic_defense_probe` 분류는 유지하며,
그 본문을 실제 문헌의 원문 인용이나 효능 주장으로 취급하지 않습니다.
실제 공격 입력이나 미지 사례에 대한 일반화 성능을 입증한 자료도 아닙니다.

설명과 확인 자료는 한국어로 제공합니다. 고정 계약의 영문 키·식별자·원본 계보
메모와 과제에서 요구하는 영어 근거 요약은 원문을 보존합니다. 영어 근거를
번역하면 영어 비율과 검수 대상 내용이 달라지므로 변경하지 않습니다.

## 검증과 승인 구분

`cos-agent` 디렉터리에서 실행합니다.

```powershell
python scripts/validate_qlora_dataset.py --input data/qlora/v2/pilot_24.jsonl --pilot --report outputs/pilot_24_structural.json
python data/qlora/v2/render_pilot_24_review.py
```

정식 절차는 `uv run --locked python ...`이지만 이 환경에서는 `uv`를 찾지 못해
Python을 직접 사용했습니다. 잠금 파일과 같은 의존 환경을 재현했다고 주장하지 않습니다.

**형식 검사 통과는 파일럿의 공식 인수 완료가 아닙니다.** 같은 GPT 계열의
Codex 검토는 내부 검토이며 `outputs/pilot_24_codex_internal_review.jsonl`에
별도로 기록합니다. PPO-37의 다른 모델 계열 공식 검수로 취급하지 않습니다.
외부 검수나 사람의 승인을 만들어 기록하지 않았습니다.

다른 모델 계열 검수, 사람의 24턴 전체 확인과 팀 확인이 필요합니다.
이 조건이 끝나기 전에는 900턴 생성·학습으로 진행하지 않습니다.
이전 초안은 `a15364d`에 커밋되어 있습니다. 개정 4~5의 변경은 아직 커밋·푸시하지 않았습니다.

## 수정 이력과 원본 보존

수정 전 입력·응답·사유·해시는 `outputs/pilot_24/`에, 최초 내부 검토의
지적은 `outputs/pilot_24_codex_internal_review_round1.jsonl`에 보관했습니다.
시간 수치 필드의 정성적 설명 수정과 신규 합성 사례 2개의 생각·의도 명시를
구분합니다. 후자는 실제 사용자 의도를 추측한 것이 아니라 합성 설정을 수정한
것입니다. 변경 내용은 새 해시로 재검사했고 이전 승인을 재사용하지 않았습니다.

## 생성 결과

- 24턴: 안내 18턴, 보류 6턴, 네 유형 각각 6턴입니다.
- 고정 검증기의 `--pilot` 형식·구성 검사 오류는 0건입니다.
- 개정 3의 내부 검토는 최초 통과 22턴·수정 필요 2턴에서 수정 후 통과 24턴·수정 필요 0턴으로 바뀌었습니다. 개정 5의 변경 행에는 과거 판정을 재사용하지 않으며 현재 내용 해시로 재검수가 필요합니다.
- `--pilot --require-review` 인수 조건은 미통과입니다. 다른 계열 검수는 미실시이고 사람 검수는 0/24턴입니다.

실행·수정 기록과 파일 해시는 `outputs/pilot_24/generation_receipt.json`에 있습니다.
`outputs/`는 Git 제외 대상입니다.

## 개정 5 — 출처와 사례의 다양성

관련 근거는 S03·S04·S05·S07에서 S08·S09·S15~S18·S32~S35를 포함한
14종으로 확대했습니다. 출처 ID만 덧붙이지 않고 입력·KB 판정·응답을 함께
설계했습니다. 모든 한국어 청크 본문은 2~4문장 설명체입니다. 관련 영어 근거는
안내 18턴 중 6턴으로 유지합니다.

| 사례 | 관련 근거 | 주요 확인 내용 |
|---|---|---|
| `syn-sol-0002` | S08, B-I01 | 합성 제품의 제거 표시와 실제 폼 세안을 대조하며 이중세안을 보편 규칙으로 만들지 않습니다. |
| `syn-sol-0004` | S09, B-I02 | 각각 층으로 바르는 방법과 손바닥에서 미리 섞는 행동을 구분하고 실제 SPF를 보증하지 않습니다. |
| `syn-sol-0005`, `syn-sol-0008` | S16 | 야외 재도포와 버전별 표시 확인을 구분합니다. |
| `syn-sol-0006` | S32, S33, B-G13 | 별도 레티놀·AHA 화장품의 같은 부위 중첩과 특정 의약품 표시의 범위를 구분합니다. |
| `syn-sol-0009` | S18 | 기한·개봉일 미확인을 만료나 SPF 소실로 단정하지 않습니다. |
| `syn-sol-0010`, `syn-sol-0014` | S34, B-G14 | 포함 성분과 관리 목적, 처방과 추가 화장품을 구분하며 처방을 임의로 변경하지 않습니다. |
| `syn-sol-0011` | S35, B-G11 | 국소 사용 확인을 진단용 패치테스트나 영구 안전 보증과 구분합니다. |
| `syn-sol-0012` | S32, B-G15 | 별도 AHA·BHA 중첩과 단일 복합 완제품을 구분합니다. |
| `syn-sol-0015` | S15, B-G01 | 향료 포함과 개인 알레르기 진단을 구분합니다. |
| `syn-sol-0016` | S17, B-P06 | 눈 노출이 없고 반복 눈시림도 없다는 관찰에 맞춰 일상 사용 범위를 검토합니다. |

S41은 `syn-sol-0016`의 **방해 근거**로만 사용합니다. 눈 노출을 부정한 상황에서
응급 세척 안내를 오적용하지 않는지 확인하는 사례이며 관련 근거 14종에는
포함하지 않습니다. 실제 눈 노출의 응급 안내를 모델로 검증한 결과가 아닙니다.
보류 모드에는 문헌 청크를 넣지 않는 계약을 유지합니다.

B-I01은 `KB/Poppy_KB_v0.6.1/sunscreen_removal_review.json`의
`face_wash` 조건과 `foam` 세정 방법을 대조한 합성 사례입니다. 기존 v0.6
엔진을 v0.6.1로 바꿔 실행한 결과가 아닙니다. 해당 보완 명세의 버전과 해시는
`outputs/pilot_24/source_diversity_rev5/revision_receipt.json`에 기록했습니다.
개정 4 대비 15턴의 내용이 변경되었으며 이전 버전을 보관했습니다.
