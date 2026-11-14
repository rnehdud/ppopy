# 팀 공용 v67 액션 데이터셋 — AFA / QLoRA

이 자료는 **현재 상태를 보고 다음 행동 하나를 고르는** 합성 개발 데이터입니다. AFA(Active Feature Acquisition)는 무엇을 먼저 물을지 배우는 데, QLoRA는 `ActionContext → ActionProposal` 대응 관계를 학습하는 데 사용합니다. 최종 공유 검토일: 2026-11-14.

## 처음 사용하는 팀원은 여기부터

1. 이 PR 브랜치 또는 병합된 저장소를 내려받습니다. Python 3.10 이상이면 아래 무결성 검사·변환을 실행할 수 있습니다. GPU와 추가 패키지는 필요 없습니다.
2. 저장소 루트에서 아래 명령으로 파일 해시·분할·액션 제약을 검사합니다.
3. QLoRA 담당자는 `messages`, AFA 담당자는 `afa-scenarios` 형식으로 **train / val_internal / test_internal을 각각** 내보냅니다. test는 최종 설정을 고정한 후 평가할 때 사용합니다.

```powershell
cd courses/ai-applications/experiments/cos-agent/data/action_policy/v67
python -X utf8 dataset_cli.py verify
python -m unittest discover -s . -p test_dataset_cli.py
New-Item -ItemType Directory -Force exports
python -X utf8 dataset_cli.py export --split train --format messages --output exports/qlora-train.jsonl
python -X utf8 dataset_cli.py export --split val_internal --format messages --output exports/qlora-val.jsonl
python -X utf8 dataset_cli.py export --split test_internal --format messages --output exports/qlora-test.jsonl
python -X utf8 dataset_cli.py export --split train --format afa-scenarios --output exports/afa-train.jsonl
python -X utf8 dataset_cli.py export --split val_internal --format afa-scenarios --output exports/afa-val.jsonl
python -X utf8 dataset_cli.py export --split test_internal --format afa-scenarios --output exports/afa-test.jsonl
```

출력 파일이 이미 있으면 덮어쓰지 않습니다. 새 이름을 사용하세요. Linux/Colab에서는 `New-Item ...` 대신 `mkdir -p exports`를 사용합니다. 이 폴더의 `exports/`는 Git에서 제외합니다.

## 들어 있는 자료와 규모

| 파일 | 역할 |
| --- | --- |
| `v67-sft-train.jsonl` | 학습 1,980턴: `input`은 전체 ActionContext, `output`은 ActionProposal |
| `v67-sft-val-internal.jsonl` | 내부 검증 221턴: 하이퍼파라미터 선택·개발 오류 분석용 |
| `v67-sft-test-internal.jsonl` | 내부 테스트 252턴: 설정을 고정한 뒤 최종 비교용. 학습·체크포인트 선택에 사용하지 않음 |
| `canonical-candidates-v67.jsonl` | 1,025개 시나리오의 초기 요청·턴별 정형 이벤트·보존 조건. AFA 환경 개발 재료 |
| `v67-sft-manifest.json` | 원본·학습·검증 파일 SHA-256, 라벨 출처, 액션 분포, 기존 생성 감사 결과 |
| `v67-excluded-scenarios-r1.jsonl` | 생성 과정에서 제외된 76개 시나리오 ID와 사유. 학습에 다시 섞지 않음 |
| `FINAL_REVIEW.md` | 이번 공유 검토의 결과와 확인 한계 |
| `dataset_cli.py` | 표준 라이브러리만 사용하는 검사·변환 도구 |

총 2,453턴 / KB 카드 58종입니다. 액션은 `ask_user` 711, `confirm_candidate` 442, `retrieve_evidence` 204, `resolve_conflict` 208, `hold` 665, `request_draft` 223턴입니다. 작성된 제안 라벨 1,925턴과 결정론적 기준선에 한국어 이유를 붙인 라벨 528턴이 섞여 있습니다. 모든 라벨을 독립적인 전문가 정답으로 해석하지 마세요.

## QLoRA에서 쓰는 방법

`messages` 출력 한 줄은 `id`와 system/user/assistant 메시지 3개입니다. user 메시지는 현재 턴의 **전체 정형 컨텍스트 JSON**, assistant 메시지는 **다음 액션 JSON**입니다. 이 자료는 자유 발화만으로 증상·시각을 추출하는 학습셋이 아닙니다.

```python
import json
from pathlib import Path

rows = [json.loads(line) for line in Path('exports/qlora-train.jsonl').read_text(encoding='utf-8').splitlines()]
messages = rows[0]['messages']  # tokenizer의 chat template에 전달
target = json.loads(messages[-1]['content'])
print(target['action'], target['target_id'])
```

학습 담당자가 준비할 순서는 다음과 같습니다.

1. 사용할 기반 모델·리비전·토크나이저·라이브러리 버전을 고정합니다. 이 PR은 모델 다운로드나 GPU 학습을 실행하지 않습니다.
2. 토크나이저의 chat template로 전체 자료의 토큰 길이를 먼저 측정합니다. manifest의 길이는 **문자 수**이며 토큰 수가 아닙니다. 긴 문맥을 조용히 잘라서 보류·거절·근거를 잃지 않도록 합니다.
3. 학습 loss는 assistant 응답과 종료 토큰에만 적용하고 system/user 토큰은 마스킹합니다. 토크나이저별 prefix 정렬과 마스크를 직접 확인합니다.
4. train으로만 가중치를 갱신하고 val_internal은 개발 선택에 사용합니다. test_internal은 모델·프롬프트·보상·체크포인트 선택을 모두 고정한 뒤 평가합니다. `review`, ID, 라벨 출처 같은 메타데이터를 모델 프롬프트에 추가하지 않습니다.
5. 학습 전 모델과 학습 후 모델을 같은 분할·입력·게이트에서 비교합니다. JSON 성공, 실행 계약 위반, 재질문, 필수 보류 누락, 초안 선행조건, 질문 부담을 따로 기록합니다.

기존 `scripts/qwen35_qlora_smoke.py`가 로컬에 있더라도 지정된 소수 fixture를 위한 기술 점검용입니다. v67 전체 학습 명령으로 사용할 수 없습니다. 이 PR이 제공하는 것은 입력 변환까지이며, 전체 학습 runner·학습 성능은 포함하지 않습니다.

## AFA에서 쓰는 방법

`afa-scenarios`는 실제 SFT 분할에 해당하는 시나리오만 내보내며, `initial_request`, `turns[].user_events`, `must_preserve` 등을 유지합니다. 원본 canonical의 `split`은 모두 `train` 생성 풀을 뜻합니다. **canonical의 split 필드로 3분할을 직접 나누지 마세요.** 변환기는 SFT 파일의 시나리오 소속으로 split을 지정하고 기존 값은 `source_pool_split`에 보존합니다. AFA와 QLoRA에서 동일한 분할을 사용하세요.

| AFA 구성요소 | 사용할 재료 / 주의점 |
| --- | --- |
| 정책 입력 | 현재까지 공개된 ActionContext만 제공. 이후 턴의 user_events·숨겨진 프로필·전체 시나리오를 보여주지 않음 |
| 행동 마스크 | `available_actions`의 `enabled=true`인 정확한 `(action, target_id)` 쌍 |
| 사용자 시뮬레이터 | 정형 이벤트를 참고하되 시점·정정·거절을 보존. 없는 값을 known으로 만들지 않음 |
| 상태 전이 | 질문 요청 자체로 관찰 확정·제품 근거 획득이 이루어지지 않음. 검토된 정형 응답을 별도로 적용 |
| 오라클 | KB 규칙에 따른 판정. 의학적 진실·제품 품질 정답과 구분 |
| 평가 | 판정 유지와 질문 비용을 함께 비교. 필수 보류 누락·재질문·성급한 보류도 기록 |

이 자료는 기록된 대화 경로입니다. **질문 순서를 바꿨을 때의 모든 답변·다음 상태·보상이 들어 있는 RL replay buffer는 아닙니다.** 시나리오 전체를 하나의 정적인 숨겨진 프로필로 단순 합치면, 나중의 정정이나 타인의 경험이 처음부터 알려진 값처럼 섞일 수 있습니다. 시간에 따른 이벤트와 정보 공개 규칙을 갖춘 시뮬레이터·환경을 별도로 구현해야 합니다. 본 PR에는 RL 환경이나 확정된 보상값이 없습니다.

설계 배경: [PPO-23 — AFA 청사진](https://linear.app/ppopy/issue/PPO-23).

## 검토 표시와 사용 범위

`review_mode=agent_policy_audit_with_user_authorization`은 사용자가 요청한 **AI 에이전트 정책 감사**입니다. export의 `approved_reference=true` / `training_ready=true`는 이 합성 개발 SFT에 대한 기존 작성 파이프라인의 표시이며, 사람·도메인 검토 완료나 임상 승인, 독립 평가 적합성을 뜻하지 않습니다. canonical의 `human_review=unreviewed`와 별개입니다.

이번 최종 공유 점검은 전수 무결성·계약·명시적 정책 검사이며, 모든 자유 문구의 의미나 모든 상황에서의 최적 액션을 독립적으로 승인한 것은 아닙니다. 규칙 감사 0건과 모델 성능 100%는 다릅니다. 다른 타당한 다음 액션도 있을 수 있습니다.

내부 validation/test는 기록된 group/family/product/정규화 발화 중복이 없지만, 같은 생성·제품 풀에서 나왔습니다. 기존 개발 자료를 다시 나눈 내부 분할이므로 완전히 미노출된 외부 평가셋은 아닙니다. 의미적 유사성·외부 일반화까지 보장하지 않으며 독립 holdout 성능으로 보고하지 않습니다. 기존 `data/action_policy/v1` 격리 자료는 이번 공유 번들에 포함하지 않습니다.

항상 `development_preview`, `production_enabled=false`를 유지합니다. 실제 사용자 수집·얼굴 분석·자동 개선 판정·운영 추천으로 연결하지 않습니다. 원본 57시나리오 감사의 5개 불일치는 [저장소 검증 안내](../../../../../../../docs/verification.md)에 기록되어 있습니다.
