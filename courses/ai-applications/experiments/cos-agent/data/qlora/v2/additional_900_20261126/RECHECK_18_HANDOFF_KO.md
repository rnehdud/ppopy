# PPO-37 추가 900턴 — Critic 18건 수정·재검수 인계

기준은 팀원이 푸시한 `e14f625`의 실제 `gemini-cross-critic` 900행 검수예요.
원본 결과는 **882 PASS / 18 FAIL**이에요. 아래 수정은 생성 담당의 보완이며, **18건의 새로운 교차 검수 PASS를 대신 기록하지 않았어요.**
추가 900행의 `human_review`는 모두 `unreviewed`로 유지했어요.

## 팀원이 재검수할 파일

- **18건 현재 입력·답변·메타데이터·새 내용 해시**: `reviews/additional_900_recheck_18_requests.jsonl`.
- 수정 전후 raw 행과 원본 Critic·이전/현재 해시: `reviews/additional_900_18_corrections.jsonl`.
- 변경되지 않은 기존 PASS 882건: `reviews/additional_900_882_preserved_pass.jsonl`. 현재 내용과 원본 검수 해시가 모두 같아요.
- 원본 900행 Critic: `reviews/additional_900_critic.jsonl`. 바이트를 변경하지 않았어요.
- 현재 내용에 맞춘 사람 확인 표본27건: `reviews/human_review_sample_after_18_unreviewed.csv`. 표본만 준비했으며 사람 검수 결과는 아니에요.
- 현재 900턴 전체 검수 요청은 `reviews/critic_requests.jsonl`과 `reviews/requests/`예요. 수정 전 전체 요청·일부 보고서는 `reviews/archive_e14f625/`에도 보존했어요.

## 실제 수정

| 유형 | 행 | 변경 |
|---|---|---|
| 미확인 제품 인용 | sol-1159, 1250, 1263, 1268, 1330, 1331, 1375 | unknown 카탈로그 인용을 해당 행의 실제 허용 문헌 인용으로 교체하고, 미확인 카탈로그는 허용 인용 목록에서 제외했어요. 제품 미상 값은 그대로예요. |
| HN 오분류 | sol-0695 | 일반 계면활성제 오해이므로 `is_hard_negative=false`, `hard_negative_type=null`로 바꿨어요. 입력·답변은 그대로예요. |
| 입력에 없는 제품 | sol-0916 | “현재 세정제”를 특정 제품 함유 여부·품목 정보 미확인의 중립 표현으로 바꿨어요. |
| 관찰 반전 | sol-1044 | “물과 잘 섞이지 않아 보이는” 관찰로 맞췄어요. |
| 미제공 분사 방식 | sol-1157 | 사용자 행동은 “이미 도포를 마쳤다는”으로 맞추고, 근거도 화염 경고와 도포 후 사고 범위로 설명했어요. |
| 미제공 시점·세안 맥락 | hold-0219, 0273, 0274, 0277 | “새로운” 시점이나 “세안”이라는 미제공 맥락을 제거했어요. |
| 문헌 밖 측정 세부 | sol-0997, 1013, 1019 | 기기 단정을 %H 수분 지표 측정으로 바꾸고, 문헌에 없는 시험 부위 단정을 제거했어요. |

행 ID는 모두 `syn-` 접두사예요. 답변 수정은 17행, 분류 메타데이터만 수정한 행은 1행으로 총18행이에요.

## 합본 Wire 입력 1,800행 통일

실제 확인 결과 전송 설정 키는 **기존 900턴의 300행과 추가 900턴의 300행**, 총600행에 있었어요. 각각의 `messages[1].content`에서 두 키만 제거했어요.
원본에서는 sol-0461부터의 자외선 담당 구간, 추가분에서는 sol-1151부터의 자외선 담당 구간에 해당했어요.
현재 1,800행 모두 실제 `build_messages()`와 같은 6개 입력 필드만 포함해요.

- 모든 Wire-only 변경은 정규화된 `SLMRequest`·내용 해시가 같아요. 변경 로그: `validation/wire_normalization_600.jsonl`.
- 기존 승인 900행의 답변·관찰·제품·문헌·분류·분할·승인은 바꾸지 않았어요. 바이트 해시는 직렬화 변화로만 달라졌어요.
- 추가 900행 중 의미 있는 정규화 해시 변경은 정확히 재검수 대상18개예요.
- 900턴 비율은 solution690 / hold210, train806 / val94로 같아요. HN 오분류 1건 제거로 HN은 **401**개예요.
- 합본은 solution1380 / hold420, train1616 / val184예요. 합본 파일을 새 학습 승인본으로 만들지는 않았어요.

## 확인한 결과와 범위

- 추가900·합본1800 공식 구조·비율 검사 오류0: `validation/remediation_18_structure.json`, `remediation_1800_structure.json`.
- 원본 Critic 해시, 기존 PASS882, 원본900 정규화·승인, 현재 Wire1800 대조: `validation/remediation_18_integrity.json`.
- 실제 `HardSafetyGuardrail`을 7개 미확인 카탈로그 사례의 수정 전후에 실행했어요. 수정 전7개는 `product_version_mismatch`, 수정 후7개는 통과했어요. 수정 대상18개도 결정적 안전 검사에서 모두 통과했어요.
- 이 안전·구조 검사는 문헌의 의미 검수나 다른 모델의 재검수를 대신하지 않아요.
- 관련 계약·데이터 검증·HardSafetyGuardrail·SLM client 테스트84개 통과, 소스 매니페스트27건 실패0이에요.
- 수정본의 실제 Qwen3-4B 토크나이저 측정은 최대1,515토큰, 길이2,048 초과0행이에요(`validation/remediation_18_tokens/`). 학습은 실행하지 않았어요.
- 추가900의 현재 SHA-256: `09a5adc0b3325e5a2962cafb7528c9c53aa3a9bccbe9bcd9eb5ab3f9535575f2`.
- 기존900의 Wire 정리 후 SHA-256: `1b1d6b3102b77b7ecb82ea431e454d7cab82898f8454d5882437fc5b311197de`.

## 재현·주의

```powershell
python -m uv run --locked python scripts/remediate_additional_900_critic.py
python -m uv run --locked python scripts/assemble_additional_900.py --nearest
python -m uv run --locked python scripts/verify_additional900_remediation.py
```

`authoring/`의 초기 생성기·과거 동결 해시, `delivery_receipt.json`, 옛 토큰 리포트는 수정 전 기록이에요. 초기 생성기만 현재 파일 위에 실행하면 수정이 사라질 수 있어요. 생성기 재현은 별도 사본에서 진행하고 위 정정 스크립트를 적용한 뒤 확인해요. 새 정정 스크립트는 `e14f625` 원본과 예상된 수정본 외의 변경을 조용히 덮어쓰지 않아요.
팀원이18건을 실제로 재검수한 뒤 새 PASS 결과를 내용 해시와 대조해 주세요. 사람 승인은 자동으로 채우지 않아요.
