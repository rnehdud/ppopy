# PPO-37 — 24턴 파일럿 생성 초안

기준 커밋은 `53a74a013e2e3533c33ec66d3ed80e0a8ce10bc1`, 작업 브랜치는
`data/qlora-v2-dataset`입니다. `development_preview`,
`production_enabled=false`인 합성 개발 실험에만 사용합니다.

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
뜻하지 않습니다. 합성 방해 문장은 기본 동작 확인용으로 실제 공격 입력이나
미지 사례에 대한 일반화 성능을 입증하지 않습니다.

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
현재 작업에서는 커밋·푸시·PR 생성을 하지 않았습니다.

## 수정 이력과 원본 보존

수정 전 입력·응답·사유·해시는 `outputs/pilot_24/`에, 최초 내부 검토의
지적은 `outputs/pilot_24_codex_internal_review_round1.jsonl`에 보관했습니다.
시간 수치 필드의 정성적 설명 수정과 신규 합성 사례 2개의 생각·의도 명시를
구분합니다. 후자는 실제 사용자 의도를 추측한 것이 아니라 합성 설정을 수정한
것입니다. 변경 내용은 새 해시로 재검사했고 이전 승인을 재사용하지 않았습니다.

## 생성 결과

- 24턴: 안내 18턴, 보류 6턴, 네 유형 각각 6턴입니다.
- 고정 검증기의 `--pilot` 형식·구성 검사 오류는 0건입니다.
- 내부 검토는 최초 통과 22턴·수정 필요 2턴에서 수정 후 통과 24턴·수정 필요 0턴으로 바뀌었습니다.
- `--pilot --require-review` 인수 조건은 미통과입니다. 다른 계열 검수는 미실시이고 사람 검수는 0/24턴입니다.

실행·수정 기록과 파일 해시는 `outputs/pilot_24/generation_receipt.json`에 있습니다.
`outputs/`는 Git 제외 대상입니다.
