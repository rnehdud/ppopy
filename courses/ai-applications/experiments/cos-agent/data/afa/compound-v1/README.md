# 복합 세안 질문 순위 검증

`development.json`의 4상황에서 질문 순위 규칙을 개발했다. `heldout.json`의 12상황은 규칙과 적용 기준을 동결한 뒤 작성했다. 두 묶음의 상황 ID, 가족 ID, 전체 관찰 조합은 서로 겹치지 않는다. 모든 답은 합성 입력이며 사람·도메인 검토 상태는 미검토다.

각 상황에서 `prefilled`에 있는 값은 런타임에 먼저 전달한다. 나머지는 실제로 요청된 질문에만 반환한다. `default_answers`는 자료 작성자가 미리 정한 응답이다. 모름과 거절은 값 없이 해당 상태로 전달한다. 정의하지 않은 질문이나 같은 질문의 반복을 만나면 평가를 중단한다.

기존 순서와 결과 우선 순위는 같은 Python 런타임, KB와 종료 조건에서 비교한다. 모든 값을 미리 제공한 동일 런타임의 권고 또는 보류가 기준이다. 개별 권고·필요한 제품 근거·보류 사유와 카드 범위도 비교한다.

첫 자료 대조에서 `test-sufficient-upfront`의 기대 상태를 바로잡았다. 차가운 물은 현재 KB에서 B-C01을 미해결로 남기므로 기대 상태는 보류다. 초기 원본과 SHA-256 및 근거를 `outputs/afa-e37/`에 보관했다. 상황 입력과 순위 규칙은 첫 등록 상태를 유지했다.

실험 폴더에서 실행한다. 아래 명령은 새로운 이름의 출력 파일을 만든다.

```powershell
uv run --locked python -m beauty_agent.afa.compound_evaluation development --output outputs/afa-e36/dev-replay-new.json
uv run --locked python -m beauty_agent.afa.compound_evaluation heldout --lock outputs/afa-e37/locked-policy.json --output outputs/afa-e37/heldout-replay-new.json
```

원래 동결 파일과 결과 증빙은 `outputs/afa-e37/`에 있다. [AFA 누적 진행 기록](../../../docs/afa-policy-progress.md)
