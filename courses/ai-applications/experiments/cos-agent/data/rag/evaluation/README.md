# PPO-44 · 검색 평가 기록

이 디렉터리는 합성 질의·작성자의 잠정 qrel·실제 검색 결과를 보관합니다. **독립 전문가 검수나 사람 승인 결과가 아닙니다.** 운영/임상 품질을 확정하는 자료로 사용하지 않습니다.

| 파일 | 내용 |
|---|---|
| [queries.jsonl](queries.jsonl) | 40개 고정 질의: 4영역 양성32 + 음성8, calibration/evaluation 각20 |
| [benchmark_report.json](benchmark_report.json) | 최종 Hash/BM25/Qwen dense-only/Qwen 2-Stage 지표·전체 threshold sweep·환경·메모리 |
| [benchmark_initial_report.json](benchmark_initial_report.json) | FAISS 질의 정규화 최적화 전 최초 GPU 실행. 유리한 지연값만 선택하지 않도록 보존 |
| [hash_scores.json](hash_scores.json), [bm25_scores.json](bm25_scores.json), [qwen_full_scores.json](qwen_full_scores.json) | 질의별 Top-15 candidate, dense/rerank raw 점수·지연. candidate 배열은 Stage 1 순서 |
| [qwen_initial_scores.json](qwen_initial_scores.json) | 최초 Qwen 실행의 raw candidate 기록 |
| [representative_cases.json](representative_cases.json) | C05/L07/N05/N06 raw 질의·반환·top 원문과 출처/한계. N06 유입 실패도 포함 |
| [model_revisions.json](model_revisions.json) | 사용한 두 공식 모델 revision 및 다운로드 후 검증한 가중치 SHA-256 |
| [verification.json](verification.json) | 관련 테스트35 PASS, source manifest27/27, 기존 main과 동일한 전체 테스트 실패 node |
| [result_manifest.json](result_manifest.json) | 결과 파일 SHA-256, 공식 청크 풀 raw SHA, RAG 코드의 LF 정규화 SHA |

해석·실행법·정량 표는 [파이프라인 문서](../../../docs/reference-rag-pipeline.md)를 참고합니다. JSON/JSONL은 UTF-8(BOM 없음)·LF이며, Windows 재체크아웃에서도 LF를 유지하도록 이 폴더에만 `.gitattributes`를 적용합니다. 모델 가중치와 인덱스 바이너리는 포함하지 않습니다.

임계값 선택은 calibration만 사용했습니다. Qwen Full의 선택값은 **0.95**입니다. held-out 양성16개에서 Recall@5/MRR@5/nDCG@5=1.0이지만, 음성4개 중 N06에는 문헌1개가 유입되어 차단율은 **75%**입니다. `non-qrel` 문서를 모두 무관하다고 판정하지 않으며 관련도 미판정 비율을 별도 보고합니다. `query_ms=0` trace 필드는 문자열 질의를 받는 검색기에서는 builder를 실행하지 않았다는 뜻이고, 실제 builder 시간은 보고서의 독립 1,000회 측정에 있습니다.
