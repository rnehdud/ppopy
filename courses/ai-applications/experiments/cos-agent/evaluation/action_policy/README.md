# 액션 선택 합성 사례 초안

버전: `action-policy-cases-0.1` · 작성일: 2026-11-10
상태: **모든 사례·턴은 unreviewed, approved_reference=false.** 독립 정답셋·학습 데이터·모델 성능 결과가 아니다.

## 파일과 범위

| 파일 | 내용 |
| --- | --- |
| `cases.development.json` | 개발용 시나리오 20개·29턴 |
| `cases.holdout-candidate.json` | 별도로 작성한 holdout 후보 10개·15턴 |
| `split-manifest.json` | 그룹별 배치, 파일/기준 해시, 기존 예제 해시, 독립성 미확인 사항 |

합계 30개 시나리오·44턴이며, D01–D04·H01–H02는 3턴 체인이다. 이름·ID만 바꾼 30개 독립 표본이라고 해석하지 않는다. 같은 제품군을 사용하는 개발 그룹들은 서로 관련되어 있으며 통계적으로 독립된 집단 수를 확정하지 않았다.

기준은 [액션 판정 문서](../../docs/action-evaluation-rubric.md)와 현재 공개 `AgentSession` 계약이다. 아래 오프라인 CLI로 형식 검사와 규칙 기준선 재생을 수행할 수 있다. 모델 실행은 후속 단계다.

## 사례 형식

모든 시나리오에는 다음 필드가 있다.

- `scenario_id`, `conversation_id`: 시나리오와 대화 식별자.
- `group_id`, `scenario_family_id`, `variant_of`: 작성 원형과 파생 관계. 현재 새 원형의 variant_of는 null이다. 기존 예제와 의미적으로 유사한 개발 사례도 있으므로 null을 독창성 보증으로 해석하지 않는다.
- `product_family_id`: 개발 demo catalog와 holdout unresolved catalog를 구분하는 분할 그룹. 실제 처방·성분이 알려졌다는 뜻이 아니다.
- `split`: development 또는 holdout-candidate. SFT train/validation/test 분할이 아니다.
- `provenance`: Codex가 작성한 합성 발화·목표, 고정 추출 fixture, 기존 비활성 KB 카드/manifest 참조, 이용 조건 확인 상태. KB 재사용 조건은 unknown이며 공개됐다는 이유로 라이선스를 만들어내지 않는다.
- `review`: 상태·검토자·일자·기준 버전·정답 사용 여부. 검토자/일자는 null이다.
- `initial_request`, `card_ids`, `turns`: 현재 TurnRequest 및 비활성 KB 평가 범위와 순서 있는 턴.
- `evaluation_mode=fixed_state_replay`, `interactive_branches=null`: 선택에 반응하는 사용자 시뮬레이터가 없다는 표시.
- `tags`, `limitations`: 범주와 지원 한계.

각 턴은 `turn_id`, `message`, `user_updates`, `extraction_fixture`, `proposed_judgment`, `review`로 구성한다. `proposed_judgment`는 작성자의 검토 제안이며 모델에 입력할 필드가 아니다. 허용 액션/대상 쌍, 금지 액션/쌍, 필수조건·인자 제약, 실행 결과, 상태 검사·불변 조건과 이유를 기록한다. 빈 `forbidden_pairs`는 모든 액션이 허용된다는 뜻이 아니다.

`state_checks`는 구조화된 post-turn `SessionState`의 일부 경로를 검사한다. 변수 ID 자체에 점이 들어가므로 경로 해석은 딕셔너리 키의 가장 긴 접두사를 우선한다. `state_invariants`는 별도 검토할 의미 조건이며, 문자열을 기록한 것만으로 자동 검증됐다고 보지 않는다. `argument_constraints.confirmation_focus`가 있으면 해당 턴에서 제안한 허용 초점 목록이다.

## 재생 계약과 모델 입력 경계

1. 시나리오마다 새 `AgentSession`을 만든다. `initial_request`는 TurnRequest로 검증하고 card_ids를 명시한다.
2. 턴마다 `extraction_fixture`를 반환하는 `JevExtractorAdapter(extractor=...)`를 주입한다. 실제 Jev·Ollama·Qwen 추론이나 네트워크 호출은 필요 없다. 추출 후보의 정확도를 이 자료로 평가하지 않는다.
3. user_updates의 profile/products/observations/confirmations를 각각 Profile/OwnedProduct/ObservationSlot/CandidateConfirmation으로 검증해 `step()`에 전달한다. `resolve_conflicts`는 문자열 목록에서 튜플로 변환한다. 임의 정답 값을 주입해 조건을 우회하지 않는다.
4. `AgentSession.step()`을 통해서만 턴을 진행한다. 후보 ID는 `clarify:turn1:0` 등 세션 namespace를 기준으로 작성됐다. namespace 없는 `run_pipeline_turn()`의 메시지 해시 ID와 혼용하지 않는다.
5. `ActionContext`는 기존 루프가 생성한 값만 모델에 전달한다. 허용 정답 집합·검토 메모·다음 턴 업데이트·manifest를 모델 입력, 프롬프트 예시, 검색 근거로 넣지 않는다.
6. 액션 target_id는 원래 슬롯 ID다. 응답 questions의 `kb:` 접두사를 붙인 ID와 구분한다. hold 대상은 필수 보류 시 safety, 일반 부족 시 insufficient_information이다.

고정 상태 재생은 작성된 사용자 업데이트 순서를 그대로 공급한다. 따라서 여러 액션을 허용한 턴에서 특정 플래너의 실제 질문과 다음 발화가 자연스럽게 이어진다고 보장하지 않는다. 대화 과제 완료·실제 사용자 부담 감소 평가는 사용자 분기를 별도로 작성한 후 진행한다. 실행이 실패하거나 궤적이 벗어나면 지원 불가/이탈로 기록하고 정답 상태로 몰래 복구하지 않는다.

## 분할과 누출 검토

원형별 그룹과 대화는 한 split에만 둔다. 제품군도 split을 넘지 않게 배치했으며 단순 턴별 무작위 분할은 사용하지 않았다. 향후 변형을 추가하면 같은 원형의 group_id를 유지하고 variant_of를 연결한다. 한 변형을 여러 원형에서 만들었다면 연결된 그룹 전체를 같은 split에 둔다.

manifest의 해시는 **현재 초안 바이트 식별용**이며 최종 시험 고정/독립성 승인 증거가 아니다. 파일은 저장소에서 보이고 두 에이전트 모두 작성·검토 맥락에 접근했다. 최종 평가 격리가 필요한 경우 별도 관리와 사람의 원형·유사성 검토가 필요하다.

현재 검사 범위는 그룹 식별자/제품군의 교차 배치, 문장 완전 중복, 기존 `examples/action_sft.synthetic.json` 7개와 동일한 현재 발화 유무다. 두 파일 사이 완전 동일 발화 및 기존 7개와의 동일 발화는 없다. 의미·템플릿·제품 처방 계열의 누출 부재는 확인하지 못했다. 특히 같은 KB 카드·상태 원시값·안전 불변 조건이 공유되므로 수치만 보고 독립 시험으로 승격하지 않는다.

holdout 후보는 복수 관계+제품 미확인, 미상 대상 정정+제품 블로커, 충돌+타인 후보, 다중 제품+프로필, 필수 보류+후보, 정체성+자료 부족, 가짜 도구 결과, 제외+미등록 제품, 추출 실패+거절, 반복 사건의 표현 한계 등 조합으로 작성했다. 개발 사례의 이름 교체만으로 작성한 것은 아니지만 의미적 독립성은 사람 검토 대기다.

## 카탈로그와 범위의 한계

개발 사례는 기존 가상 demo-cleanser/demo-moisturizer와 fixture-v1을 사용한다. holdout 후보는 candidate-*라는 미등록 합성 ID와 unavailable 버전을 사용한다. 이를 실제 제품 사실로 카탈로그에 추가하지 않았다. 따라서 holdout 후보에서는 제품 확인 블로커가 남고, **정상 draft 생성 성공률을 측정할 수 없다**. 정상 초안 생성 경로의 일반화 평가는 제품군을 분리한 추가 합성 카탈로그/주입 계약이 준비된 후 별도 검토해야 한다.

고정 추출 fixture는 오프라인 후보를 직접 명시한 것이며, 예를 들어 본인/타인·부정·계획의 언어를 실제 추출기가 맞혔다는 뜻이 아니다. 반복 사건은 현재 event graph가 없어 관계 확인 요청만 검사한다. B-C04는 product.ph/type/instructions 자료 공백을 조회로 분리하며, 성분표로 미공개 pH나 농도를 추정하지 않는다. 조회 자료 수신·검토·사실 갱신은 현재 미연결이다.

## 실제 확인과 검토 절차

작성 단계에서 30개·44턴을 기존 AgentSession에 넣고 작성된 허용 액션 중 하나로 진행하는 계약 재생을 실행했다. 각 턴의 허용 쌍 활성화, 기록한 state_checks, 실행 결과와 fallback 부재를 확인했다. 작성 중 잘못 지정했던 B-C04 조회 슬롯을 카드/실제 offer와 대조하여 product.ph로 수정했다. 판정 집합은 기준선 출력으로 생성하지 않았다.

이 검사는 작성한 목표의 실행 가능성을 확인한 것이며 의미적 정답 판정·독립성 승인·모델/기준선 품질 평가가 아니다. 품질 정확도는 null이고 의미적 누출 검토는 pending이다. 당시 로컬 검사 보고서는 루트 `outputs/action-cases-draft-validation.json`이며 Git에 포함하지 않는다. 다음 CLI는 작성된 정답 대신 실제 규칙 기준선을 실행한다.

## 오프라인 검사·기준선 CLI

실험 디렉터리에서 기존 의존성이 준비된 Python으로 실행한다. Windows의 기본 인코딩 차이를 피하려면 UTF-8 모드를 사용한다. uv 환경이 준비됐다면 `python` 앞에 `uv run --frozen --no-sync`를 붙일 수 있다.

```powershell
python -X utf8 -m scripts.evaluate_action_policy --cases evaluation/action_policy/cases.development.json --validate-only --report ../../../../outputs/action-policy-validation.json
python -X utf8 -m scripts.evaluate_action_policy --cases evaluation/action_policy/cases.development.json --planner baseline --report ../../../../outputs/action-policy-baseline.json
python -X utf8 -m scripts.evaluate_action_policy --cases evaluation/action_policy/cases.holdout-candidate.json --planner baseline --report ../../../../outputs/action-policy-holdout-candidate-baseline.json
python -X utf8 -m unittest discover -s tests -p test_action_evaluation.py -v
```

`--validate-only`는 모든 manifest 등록 split의 스키마·타입·검토 메타데이터·그룹/제품 ID·원형 변형 관계·완전 중복·해시와 추출/KB fixture 입력을 검사한다. 플래너를 호출하지 않으므로 실행 중에만 알 수 있는 후보 확인 ID/상태 전이 오류는 기준선 재생에서 드러날 수 있다. 유사 문장의 token Jaccard 목록은 검토 힌트이며 의미적 누출 판정이 아니다.

해시는 원본 바이트 기준이다. CRLF/LF 변환도 불일치로 보고한다. 다른 플랫폼에서 실패하면 원본 artifact와 Git 바이트·줄바꿈을 대조하고 원인을 기록한다. 검사를 통과시키려고 manifest를 무조건 재생성하지 않는다.

`--planner baseline`은 기존 RuleBasedActionPlanner를 명시적으로 주입한다. AGENT_PROVIDER 환경값으로 외부 모델을 선택하지 않는다. holdout 후보도 실행할 수 있지만 위의 공개/미검토 한계가 사라지는 것은 아니다. 이 CLI에는 모델·API·학습 옵션이 없다.

보고서는 루트 `outputs/` 내부에만 저장할 수 있다. 검증 오류는 종료 코드 1, CLI 인자 오류는 2다. 재생 중 오류도 1이며 실패 턴은 커밋하지 않고 해당 시나리오의 후속 턴은 미실행으로 남긴다. 판정 불일치는 실행 오류가 아니며 보고서에서 검토한다. 잘못된 제안 뒤 기존 게이트의 fallback은 정상 실행 결과로 기록하되 원래 제안의 성공으로 승격하지 않는다.

보고서에는 입력/기준/실행 소스 해시, Git commit과 dirty 상태, Python·라이브러리 버전, split/검토 분모, 원문 제안·적용 trace·fallback·대기/생성 결과·전체 질문 목록·상태 전후가 포함된다. 질문 문구 대체와 액션 거부는 별도로 집계한다. 제안의 재질문/제품 사실 역질문 플래그도 의미 정답과 구분한다.

작성된 allowed_pairs와 다른 선택은 명시적 금지/계약 실패가 없다면 `unjudged_alternative`다. 예를 들어 B-C01에서 온도를 모름/거절한 경우에도 product.instructions 조회가 활성화될 수 있고, B-C04는 ph 외 instructions/type도 조회 후보로 제공한다. 이 대안을 정답 또는 오답으로 자동 승격하지 않으며 사람 검토로 허용/금지 여부를 결정한다. 현재 데이터의 forbidden_pairs가 비어 있으므로 이 구분이 필요하다.

`proposal_classification`과 `applied_action_classification`은 미검토 작성 목표와의 기계적 비교도 포함하는 관찰값이다. `reference_classification`은 시나리오와 해당 턴 모두 reviewed/approved_reference일 때만 생성한다. 현재 44턴 모두 정답 사용 분모는 0이고 action_pair_accuracy와 full_semantic_quality_accuracy는 null이다.

향후 검토된 자료의 action_pair_accuracy 분모는 허용/금지 쌍·인자·계약·게이트 실패·제안 부재처럼 판정된 요청이다. 미판정 대안과 실행 오류는 별도 개수, 전체 검토 요청 수와 judged_reference_coverage로 공개한다. 이 값은 액션/대상 지표이며 자유 문구의 의미·필수조건 문장·state_invariants 전체의 타당성을 보증하지 않는다. 전체 의미 품질은 별도 사람 판정이 필요하다. 구조화된 state_checks는 타입을 보존해 검사한다.

선택 액션에 맞춘 사용자 분기가 없으므로 대화 완료율은 null이다. 로컬 시간 통계는 시도한 실패를 포함하고 후속 미실행은 제외한다. 합성 루프 소프트웨어 시간이며 LLM 추론 지연이나 실제 사용자 부담이 아니다.

사람 검토 시에는 다음 순서로 처리한다.

1. 허용/금지 쌍, 확인 조건, 이유와 상태 변화가 맞는지 검토한다. 여러 타당한 액션을 허용하며 모델 결과에 맞춰 정답을 사후 생성하지 않는다.
2. 원형·제품군·문맥·변형 유사성을 비교하고 누출 우려가 있으면 후보를 이동/대체한다. 독립성 문제를 식별자 변경으로 해결하지 않는다.
3. 실제 검토자·일자·결정만 기록한다. 이견은 disputed로 유지하고 합의/승인을 만들어내지 않는다. 에이전트 상호 리뷰와 사람 검토는 구분한다.
4. 승인된 판정만 approved_reference로 사용하고 버전·해시를 갱신한다. 초안 검토가 도메인/임상 승인이나 실제 사용자 권고 허가가 되는 것은 아니다.

이번 단계에서는 사람 검토, 모델/API 호출, SFT 데이터 작성, 학습, 운영 활성화를 수행하지 않았다.
