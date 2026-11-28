# PPO-46 NLU Step 2 — 신규 합성 980턴

## 현재 상태

`origin/data/nlu-v1-pilot-critic`의 `d1e9cbecad9741ed014013876c3fc4a8c8472a67`에서 새 `data/nlu-v1-step2` 브랜치를 만들었어요. 확정 라벨링 정책과 요청/출력 계약·화이트리스트·실제 Wire 빌더를 적용했어요.

**초기 980턴은 외부 Gemini 전수 검수를 받았고(936 PASS / 9 FAIL / 35 REVIEW), 지적 사항 수정 후 새 해시 26행의 재검수를 기다리는 학습 후보예요.** 요청한 23행과 공통 atom 원문 정렬로 함께 바뀐 기존 PASS 3행을 모두 재검수 대상으로 분리했어요. 변경하지 않은 REVIEW 21행은 전달받은 확정 정책에 따라 현행 유지/PASS 수용으로 기록했으며, 원본 Gemini 판정 파일을 수정하지 않았어요. 사람 승인·Base Zero-Shot 측정·학습·모델 배포는 실행하지 않았어요. 모든 행의 `confirmed_by_user=false`, `critic_status=unreviewed`, `human_review=unreviewed`는 유지했어요.

## 파일과 재현

- [신규 데이터셋](nlu_sft_v1.jsonl): system/user/assistant 메시지 980행. Wire는 `build_nlu_messages(NLURequest)`로 만들었어요.
- [전체 교차 검수 요청](reviews/step2_critic_requests.jsonl): 원본 입력·예상 출력·작성 근거·내용 해시 980개예요.
- [검수 인계](reviews/STEP2_CROSS_MODEL_HANDOFF.md): 외부 검수 방법·집중 확인 사항이에요.
- [수정 내역과 재검수 범위](reviews/STEP2_CORRECTIONS.md), [전체 26행 새 해시 요청](reviews/step2_recheck_requests.jsonl), [핵심23행](reviews/step2_recheck_core23.jsonl), [추가3행](reviews/step2_recheck_additional3.jsonl).
- [수정 전후 raw](reviews/step2_corrections_raw.jsonl), [확정 경계21행 현행 유지 기록](reviews/step2_policy_acceptance.jsonl), [해시·범위 대조](validation/step2_correction_manifest.json).
- [분할 배치](reviews/step2_batches): 70개씩 14개 배치예요. 같은 의미 가족은 배치 경계에서도 쪼개지지 않아요.
- [분포/정책 경계 감사](validation/step2_audit.json), [공식 구조 검증](validation/step2_structure.json), [생성 원천·행별 해시](validation/step2_generation_manifest.json).
- [원문·예상 후보 대조표](step2_review.md): 각 행의 원문과 후보, 작성 근거를 펼쳐 볼 수 있어요.
- 생성기: [build_nlu_v1_step2.py](../../../scripts/build_nlu_v1_step2.py). 추가 감사: [audit_nlu_v1_step2.py](../../../scripts/audit_nlu_v1_step2.py).

cos-agent에서 실행해요. `uv`가 PATH에 없다면 아래처럼 `python -m uv`로 같은 CLI를 실행해요.

```powershell
python -m uv run --locked python scripts/validate_nlu_dataset.py --input data/nlu/v1/nlu_sft_v1.jsonl --min-rows 800 --enforce-buckets --report data/nlu/v1/validation/step2_structure.json
python -m uv run --locked python scripts/audit_nlu_v1_step2.py
python -m uv run --locked python scripts/prepare_nlu_v1_step2_recheck.py
python -m uv run --locked pytest -q tests/test_nlu_step0.py tests/test_v3_contracts.py
```

저장소 루트:

```powershell
python tools/verify_source_manifest.py
```

생성기를 재실행하면 Step 2 후보와 검수 요청을 재작성해요. Critic 수정 후에는 현재 검수 대상 파일을 덮어쓰지 말고 별도 작업 사본에서 재현해 주세요. 파일럿·검증기·코어·KB는 수정하지 않았어요.

## 규모와 독립 단위

| 주 버킷 | train | val_internal | 합계 |
|---|---:|---:|---:|
| turn1_utterance | 126 | 14 | 140 |
| turn2_followup | 126 | 14 | 140 |
| denied_polarity | 126 | 14 | 140 |
| other_subject | 126 | 14 | 140 |
| high_risk_symptom | 126 | 14 | 140 |
| product_mention | 126 | 14 | 140 |
| no_signal_noise | 126 | 14 | 140 |
| 합계 | **882** | **98** | **980** |

- 90/10 분할이며, **140개 의미 조합 가족 × 가족당 7개 표현 변형**이에요. 980개의 독립적인 실제 사용자 대화가 아니에요. Codex가 작성한 의미 단위·구어 표현의 통제된 조합 합성이고 외부 모델을 980회 호출한 것이 아니에요.
- 가족 126개는 train, 14개는 val이에요. 같은 조합의 표현 변형 7개는 모두 같은 분할에 있어요. 개별 의미 단위/슬롯/어휘는 다른 조합의 train과 val에 공유될 수 있어요. 따라서 **미노출 의미 조합 검증**이지 모든 어휘·슬롯의 미노출 검증은 아니에요.
- 가족 ID 교차 분할 누수 0건, 공백 정규화 발화 누수 0건이에요. 모든 공백을 제거한 더 강한 대조에서도 중복/누수 0건이에요. 파일럿 49개 원문과의 공백 제거 중복도 0건이에요.
- 고정 허용 목록은 모든 행에 동일한 슬롯34개·증상11개·토픽8개예요. 정답에 등장한 항목만 허용 목록으로 주지 않았어요.
- 핵심 슬롯34개를 모두 출력하고, 슬롯별 최소14개 후보를 확보했어요. 증상11종·지속성4종·사용 상태5종·토픽8종을 모두 포함해요. 동일 빈도 균등 분포는 아니며 정확한 수는 감사 JSON에 있어요.
- 후보가 2개 이상인 복합 발화 784개(80%), 가벼운 종결어미 오타(`해여`, `어여`) 81개를 포함해요. 이 81개 외에도 `세수 두번함`, `눈따가움`, `선크림 안바름`, 축약·줄바꿈 표현이 있어요. 980개 전부가 실제 모바일 타이핑 기록이라는 뜻은 아니에요.
- 주 버킷은 상호 배타적 배정이고 공식 검증기의 내용 기반 버킷은 중복 집계예요. 예를 들어 타인 경험에 후속 질문도 있는 행은 둘에 집계돼요.

## 확정 정책 적용

1. 순수 횟수는 정수, 표시 준수 전용 발화는 `according_to_product_removal_instructions`예요. 둘이 함께 나오면 명시적 정수 횟수만 추출해요. 순수 횟수21행·표시 전용14행·횟수 우선7행을 경계 검사했어요.
2. 눈시림 발생 상황이 명시된70행은 증상과 `skin.eye_symptom_context`를 동일 주체로 함께 남겨요. 씻는 상황을 미제공 원인이나 질환으로 바꾸지 않아요.
3. 명시적인 빈도·시간대 실제 제품 사용112행은 `method.current_routine`과 제품 후보를 병행해요. 순서 발화는 `method.sequence`도 남겨요. 빈도 없는 기본 제품 사용63행은 루틴 슬롯을 임의로 만들지 않아요.
4. 물 접촉·땀 부정77개 후보는 `yes/denied`예요. 단순히 수영을 안 했다는 말로 모든 물 접촉을 부정하지 않도록, 물 접촉 부재가 직접 명시된 발화로 작성했어요.
5. 부분 제품명 힌트35개 언급은 `null`로 방어하고, 전체 span이 일치하는21개 언급만 가상 catalog hint를 연결해요. 제품의 실제 신원·성분·농도 확정은 하지 않아요.
6. 후속 질문과 다른 슬롯을 답한42행, 거부/완전 잡담으로 빈 후보를 반환한21행을 포함해요. 질문이 있어도 답하지 않은 슬롯의 값을 만들지 않아요. 질문 대상에 대한 단순 모름은 해당 슬롯의 `null/unknown`으로 남겨요.
7. 자기와 타인 경험이 한 발화에 섞인14행도 절별 주체를 구별해요.

## 작성 중 보강 및 외부 검수 집중점

- 문헌/성분 효능을 생성하는 자료가 아니라 발화의 관찰 후보를 추출하는 자료예요. 진단·추천·추가 질문을 예상 출력에 쓰지 않아요.
- 젤 제품명만으로 세정 용도를 만들지 않았어요. 이름만 들은 제품의 사용 여부도 추정하지 않아요.
- 차단제 덧바름에 명시된 주기에서도 루틴을 병행하도록 보강했어요. 같은 제품명에 실제 사용이 확인되면 단순 언급의 `unknown`을 별도 중복 후보로 남기지 않아요.
- **확정 경계1:** `선크림 안바름`은 단일 비도포 보고로는 과거 사용 중단 여부를 알 수 없어 제품명은 남기고 사용 상태를 `unknown`으로 유지해요. `stopped`는 명시적인 중단 표현에만 사용해요. `0407..0413`은 데이터·내용 해시 변경 없이 PASS 수용이 확정됐어요. 이는 행 데이터의 사람 승인과는 달라요.
- **확정 경계2:** 타인의 실제 제품 사용은 `other_person`, 명시적 사용 중단/구매 고려는 각각 `stopped`/`considering`을 보존해요. 별도 product subject 필드가 없는 현 계약에서 비사용 상태를 현재 사용으로 바꾸지 않아요. `0533..0546`도 데이터·내용 해시 변경 없이 PASS 수용이 확정됐어요.
- `coverage_gaps`는 도포 중 일부 부위 누락으로 통일했고, 본인은 `using`, 타인은 `other_person`이에요. 단발 비도포 경계1과 구분해요. `method.mixing`의 모든 변형 원문에는 값과 같은 `손바닥` 부위를 명시했어요.
- 가족별 표현 변형은 독립 사례 수를 늘리지 않아요. 같은 작성자와 통제된 표현의 편향이 있으므로 구조 검사 합격을 의미적 정답 보장이나 학습 성능으로 취급하지 않아요.

파일럿 SHA-256: `c5f96332f52c6ad5e5a5e36e0a1249c55cc04f3818f352fd42388cb4ef443cbe` 그대로 보존했어요. 원본 파일럿 Critic PASS는 이번 980턴의 PASS가 아니에요.
