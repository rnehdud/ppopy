# 2계층 변환·검색 호환성

2026-11-27. 기준 main `1fe228e6f8addadd369e820d938dbfefa99c2838`. 기존 변환기의 `regulatory`/`safety_method` 거부와 메타데이터 유실을 해결했다. [입력과 실행 명령](../data/rag/layer2/README.md)을 제공한다.

## 변경 범위

`ReferenceChunk.layer2`에 판본·관할·조건·상태를 담고, 정확한 `ready`만 받아들인다. L2U ID를 ref에 그대로 사용한다. 기존 1계층 청크 ID·JSONL·SLM 입력 직렬화는 유지하며 빈 `layer2: null`을 추가하지 않는다. 변환·index CLI는 `--additional-corpus`로 두 코퍼스를 결합한다. 원문 요약을 새로 작성하거나 재검증했다고 주장하지 않는다.

파서는 Markdown 매니페스트의 문단 해시와 메타데이터 ID를 결합한다. 문단/본문/출처 일치와 필수 필드가 실패하면 중단한다. 추가 파일이나 중복·보류 문단을 조용히 건너뛰지 않는다. 변환한 JSONL은 Pydantic 재로드와 Markdown 대조를 통과해야 인덱스에 들어간다.

`Layer2Selection`은 출처 ID·관할·판본·as_of와 `source_explanation_only` 용도를 명시한다. 기본값은 2계층 제외다. 2계층을 포함한 색인에서는 dense 결과 전체에서 조건에 맞는 후보를 고른 뒤 stage1_k로 자르고 rerank한다. 최종 select에서도 같은 조건을 재확인한다. 전체 검색은 현재 243문단의 소규모 색인을 위한 방식이며 대규모 색인에서는 native metadata filtering이 필요하다. 보존한 시점 문자열을 현행 시행기간으로 자동 해석하지 않는다.

벡터 캐시는 코퍼스 메타데이터와 임베딩 설정이 같을 때만 재사용한다. 선택한 출처 범위는 결과 index_version에도 반영하며, 범위에 관계없이 동일한 벡터 파일은 재사용 가능하다. HOLD/NLU는 기존처럼 쿼리 생성·임베딩·rerank 호출 전 반환한다. SLM에는 상세 조건이 그대로 전달되고, 2계층이 있을 때만 지정 판본 설명에 한정하는 지시를 추가한다.

## 확인 결과

- 2계층 92문단 = regulatory 76 + safety_method 16, 출처 8개. 문단/본문 해시와 안정 ID 보존.
- 1계층 151 + 2계층 92 = 243문단 JSONL 변환·재로드·인덱스 저장·질의 CLI 통과. 기존 151문단 및 동결 JSONL 변경 없음.
- 관련 테스트 **85 passed**: RAG corpus/pipeline/evaluation, v3 contracts, SLM client, 신규 layer2 회귀 23개. 관련 테스트 실패·skip·xfail 0.
- 실제 FAISS에 HashFallback 벡터를 저장·재로드한 뒤 92개 원문 자기조회 **92/92**, 메타데이터 왕복 **92/92**, 범위 미지정 시 2계층 결과 **0**. 임베딩 모델 성능 검사가 아니다.
- 기본 전체 테스트 **574 passed / 9 failed / 14 errors**. 깨끗한 동일 main에서도 **551 passed / 9 failed / 14 errors**; 실패 node ID 23개가 전부 같고 신규 실패 0. 기존 AFA/v67의 `bundle/source drift: manifest.json` 문제를 유지했으며 기대값·동결 파일을 수정하지 않았다.

확인 환경: CPython 3.13.12, uv.lock 의존성. FAISS 검사는 저장소 `requirements-rag-models.txt`의 faiss-cpu 1.16.0으로 수행한다. Qwen 가중치 실행, 관련도/인용 적합성 평가, 임계값 보정, SLM 생성 평가, 서비스 배포는 포함하지 않는다. 기존 1계층 평가 점수를 243문단에 적용하지 않는다.

## 재현

실험 디렉터리에서:

```bash
uv run --locked pytest -q tests/test_rag_layer2.py tests/test_rag_corpus.py \
  tests/test_rag_pipeline.py tests/test_v3_contracts.py \
  tests/test_rag_evaluation.py tests/test_slm_client.py
uv run --locked python scripts/check_rag_layer2.py
# FAISS가 설치된 모델 환경에서:
python scripts/check_rag_layer2.py --faiss
```

검사 결과는 연결과 입력 보존을 확인한다. 자기조회는 미노출 질의에 대한 검색 정확도를 측정하지 않는다. 기존 full source PDF는 지정 Drive에서 별도로 관리하며 이 패키지는 링크·해시·독립 요약을 배포한다.

## 검사 기록 해시

기록 경로는 실험 디렉터리의 `outputs/layer2-compat/`이며 Git 입력이 아니다. 재현 명령으로 다시 생성할 수 있다.

| 기록 | SHA-256 |
|---|---|
| `focused-tests.log` | `4306d478256c3b9396f6e22ca9d659e88fcceb3bc502e0e9e616b855f0fe976f` |
| `full-tests.log` | `a2d2512a0daa56a47c77774de1dc71cbdce7ca48dc7d19690786befa0e9a5ce4` |
| `baseline-comparison.json` | `e684828dde586799cc9804689d90edf8fc558b7ab0cb2ede3cbe4dc9d070165e` |
| `faiss-check.json` | `1eb0f881887e30358eb7d19f1e566365685ee33fe34bd3ad27bac98a5723a90e` |
| `export.json` | `a152c60a59e8ba2d1f532b2ba3dc28d532a4ee8ce1f249a3b3ece338411dd9ad` |
| `build.json` | `2fc5a20b5155928cf4396474f903b0095cb0b0d5c446898558d6fedb290d5eb2` |
