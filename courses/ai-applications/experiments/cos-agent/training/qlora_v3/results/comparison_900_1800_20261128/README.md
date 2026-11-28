# 900건·1,800건 QLoRA raw 답변 비교 및 epoch별 약점 분석

기록일: 2026-11-28. 합성 입력의 실제 Kaggle 모델 출력을 비교한 검토 자료입니다. 모델 가중치·체크포인트·인증 정보는 포함하지 않습니다. 새 학습이나 추론을 실행한 결과가 아니라 저장된 실제 출력을 읽고 검수한 기록입니다.

## 팀원이 먼저 볼 파일

1. [약점·변화 추이 분석](WEAKNESS_ANALYSIS.ko.md): 네 후보의 비교, 분야별 집계, 실제 raw 인용과 해석.
2. [900건 E2 대 1,800건 E3 비교 HTML](extended_review_60.html): 공통 60개 사례별 기존 모델과 새 모델의 입력·답변·판정.
3. [1,800건 E1·E2·E3 비교 HTML](epochs_1_3/report.html): 60개 사례 × 3 epoch, 원본 입력 전체·실제 답변·인용·판정 이유·해시. HTML은 다운로드해서 브라우저로 여세요. GitHub 파일 화면에서는 실행되지 않습니다.
4. [판정 JSON](epochs_1_3/review_1800_epochs_1_3.json), [CSV](epochs_1_3/reviews.csv), [집계·전이](epochs_1_3/summary.json).
5. [실제 입력·raw 출력 묶음](common_90_raw_pairs.json): 공통 ID 90개의 원본 입력과 출력. 이 중 메시지가 완전히 같은 **60개**가 이번 의미 검수 대상입니다. 나머지 30개도 비교 정렬 근거로 보관했지만 이번 판정에 포함하지 않았습니다.

## 핵심 결과

| 판정 | 900건 Epoch 2 | 1,800건 Epoch 1 | Epoch 2 | Epoch 3 |
|---|---:|---:|---:|---:|
| PASS | 29 | 24 | 19 | 18 |
| WARN | 14 | 24 | 24 | 29 |
| FAIL | 17 | 12 | 17 | 13 |

- 이 표본에서 900건 E2는 PASS가 가장 많고, 1,800건 E1은 FAIL이 가장 적습니다. 1,800건 E3가 일괄적으로 더 좋은 것은 아닙니다.
- 1,800건 E1/E2의 120개 답변은 새로 직접 읽었습니다. E3의 60개 판정은 기존 `extended_review_60.json`과 동일한 출력 해시의 검수를 보존했습니다. E3 판정 이유에는 기존 900건 모델과의 비교 설명도 포함돼 있습니다.
- 한 명의 Codex 검수입니다. 독립 Cross-Model Critic, 사람 승인, 임상 정확도 또는 최종 모델 채택 결과로 해석하지 않습니다.
- PASS=검토 범위에서 뚜렷한 문제 없음. WARN=모호함·구체 안내 부족·근거 대응 약함. FAIL=명확한 입력/표시 모순·사실 발명·출처 범위 왜곡. 자동 키워드로 의미 판정을 만든 것이 아닙니다.

## 실제 실행 출처와 비교 한계

- 900건 raw: [Kaggle checkpoint continuation](https://www.kaggle.com/code/linawf/ppopy-raw-checkpoint-continuation), version 2. `answer_900_epoch2`는 실제 Kaggle 출력이며 로컬 vLLM 출력과 혼합하지 않았습니다.
- 1,800건 raw: [Kaggle 1800 QLoRA lr5e5](https://www.kaggle.com/code/linawf/ppopy-1800-qlora-lr5e5), version 1. 원본은 epoch별 검증 184개, 5 epoch 총 920개 출력입니다. 이번 기록은 그 전체의 의미 검수가 아닙니다.
- 비교 기반 모델: `Qwen/Qwen3-4B-Instruct-2507`. 900건 학습률 1e-4, 1,800건 5e-5이며 실행 조건도 달라 데이터 수만의 효과를 분리한 실험이 아닙니다.
- 공통 90개 중 30개는 입력 전송 필드(`timeout_seconds`, `max_response_bytes`)가 달라 동일 메시지 비교에서 제외했습니다. [입력 정렬 기록](input_alignment.json)을 확인하세요.
- 공통 60개는 비무작위 표본입니다. 증상/포장 HOLD, 손 세정, 젤, 로션/화장수, 눈가 표시 중심이며 자외선차단 등 전체 범위를 대표하지 않습니다.
- [학습 지표 원본](training_1800/epoch_metrics.csv)과 [loss 그래프](training_1800/loss_curves.png)는 전체 검증 184건 기준입니다. 의미 판정 60건과 모수가 다릅니다. loss 최저는 E3지만 이 표본의 의미 판정 분포는 E1이 더 좋았습니다.

## 무결성 확인과 재현

표준 Python만 사용합니다. 이 검사는 해시·인용·집계의 무결성을 확인하며 의미적 정답을 자동 판정하지 않습니다.

```bash
python verify_artifacts.py
```

`file_sha256.json`은 이 파일을 포함한 패키지 파일의 SHA-256 목록입니다. `verification.json`은 패키징 시점의 검증 범위를 기록합니다. 공유 파일은 LF로 통일했고 JSON 문자열 안의 원본 모델 출력은 변경하지 않았습니다. 원본 입력·답변의 변경 없이 보고서를 다시 렌더링하려면 다음을 실행할 수 있습니다(`build_extended_report.py`는 추가로 matplotlib이 필요하고, 공유된 렌더링 결과와 해시 목록은 변경됩니다).

```bash
python build_extended_report.py
python build_epoch_report.py
```

`manual_batch_*.json`, `epoch_batch_*.json`은 이미 작성된 검수 메모입니다. `record_*.py`는 메모를 원본 출력 해시에 연결하는 도구이며 판정을 생성하지 않습니다. 완료된 검수 파일에 다시 추가하면 중복 검사로 중단되므로 재실행하지 마세요.

입력의 문헌 인용은 저장소의 선택된 RAG 근거입니다. 원문 PDF나 전체 외부 페이지를 새로 포함하지 않았습니다. 재사용 조건과 출처는 기존 [RAG 출처 등록부](../../../../data/rag/SOURCES.md)를 참고하세요. 이 기록은 development preview이며 production 활성화·실사용자 수집·자동 개선 판정 또는 인간 승인 상태를 변경하지 않습니다.
