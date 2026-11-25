# PPO-44 · Reference Literature RAG (Step 2–3)

이 구현은 `development_preview`, `production_enabled=false`인 로컬 개발용 검색 모듈입니다. 정형 KB의 판단·HOLD 결정을 문헌 검색으로 대체하지 않으며, 임상 진단·개인별 치료·자동 개선 판정을 수행하지 않습니다. 기존 AFA/Control Plane은 수정하지 않았습니다.

## 실행 경로와 계약

```text
SOLUTION용 SLMRequest
  → build_query(confirmed_observations, product_evidence)  [LLM 호출 0]
  → Qwen3-Embedding-0.6B → L2 정규화 → FAISS CPU IndexFlatIP Top-15
  → Qwen3-Reranker-0.6B yes/no 점수 → 임계값 → 최대 Top-5 (0개 허용)
  → RetrievalResult / 순수 본문 ReferenceChunk
```

- 공개 진입점은 `TwoStageReferenceRetriever.retrieve(query, *, top_k=5)`입니다. `v3_contracts.ReferenceRetriever`와 구조적으로 호환됩니다.
- 요청 단위 진입점 `retrieve_for_request(request)`는 `mode != "solution"`이면 **query builder·embedding·reranker 호출 전에** 빈 결과를 반환합니다. `QUESTION_MODE`는 추가하지 않았습니다. 향후 Control Plane 연결에서도 질문 턴에는 이 검색기를 호출하지 않아야 합니다. 이번 변경 자체가 운영 런타임 통합을 완료했다는 뜻은 아닙니다.
- `top_k`는 1–5입니다. 임계값 미달을 다른 문서로 채우지 않습니다. `index_version`은 제목·본문·출처 메타데이터를 포함한 코퍼스 SHA-256에서 파생합니다.
- 색인 및 검색 대상은 공식 Markdown 파서가 읽은 151개 `CorpusEntry`입니다. 빌드 시 `chunks.jsonl`과 전체 `ReferenceChunk` 동등성을 확인합니다. 임베딩과 리랭킹에는 `entry.embedding_text`(제목 + 줄바꿈 + 본문)를 사용하고, 반환하는 `chunk.text`는 바꾸지 않습니다.
- 벡터와 질의를 모두 L2 정규화한 뒤 `IndexFlatIP`로 검색합니다. FAISS는 **CPU**에서 검색하고, 두 Qwen 모델만 GPU에 올립니다.
- `HashFallback`은 안정적인 해시 기반 단어·문자 bigram 어휘 검색입니다. 의미 기반 다국어 모델이 아니며 Qwen 장애 시 동등한 품질을 보장하지 않습니다. `NoOpReranker`는 기존 cosine 점수만 유지합니다. 계약의 backend enum을 변경하지 않고 이 경로는 `stub`으로 표시합니다.
- 불량 차원·NaN 점수·중복/비표준 참조·코퍼스/모델 불일치 인덱스는 예외로 거부합니다. 임베딩 모델이 실패했다고 Hash로 **조용히 전환하지 않습니다**. 대체 백엔드는 호출자가 명시적으로 선택합니다.

## Deterministic query builder

확인된 `method.*`, `skin.*`, `sun.*`, `cleansing.*`, `environment.*`, `storage.*`와 `constraints.goals`를 정렬해 구성합니다. `known` 값은 `confirmed_by_user=true`일 때만 사용합니다. unknown/not_asked/declined/conflicting은 미확인 상태로 남기며 `none`으로 바꾸지 않습니다. `not_applicable`은 생략합니다.

제품은 `status="verified"`인 레코드의 허용된 표시·성분 필드만 사용합니다. 미확인 버전의 옛 표시, 제품 식별자, 제조사 선호, KB 판단/가이던스는 쿼리에 넣지 않습니다. 최대 길이는 기본 2,000자이며 필드 경계에서만 제한합니다. LLM·네트워크·파일 I/O는 없습니다. 대형 객체 전체의 최악 실행 시간을 0ms로 보장한다는 의미는 아니며, 실제 시간은 평가 결과에 기록합니다.

## 오프라인 실행

COS 디렉터리에서 실행합니다. 기본 환경에는 Torch/FAISS/Transformers가 없어도 됩니다.

```powershell
uv run --locked python scripts/build_rag_index.py --backend hash --output data/rag/index/hash
uv run --locked python scripts/eval_rag_retrieval.py --backend hash --output outputs/rag_pipeline/hash_baseline
uv run --locked pytest -q tests/test_rag_corpus.py tests/test_rag_pipeline.py tests/test_rag_evaluation.py tests/test_v3_contracts.py
```

PowerShell에서는 `tests/test_rag_*.py`를 셸이 파일 목록으로 확장하지 않으므로 위 명시적 목록을 사용합니다. 네트워크와 GPU가 없는 경로에서 모델 다운로드가 발생하지 않습니다.

## Windows CUDA 모델 환경

기존 `.venv`/전역 CPU Torch/`rl-train` 설정을 덮어쓰지 않고 별도 환경을 사용합니다. 아래 모델 패키지는 Python 3.12 기준입니다. `uv` 명령이 PATH에 없으면 `python -m uv`로 실행할 수 있습니다.

```powershell
uv venv --python 3.12 outputs/rag_gpu_env
uv pip install --python outputs/rag_gpu_env/Scripts/python.exe torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
uv pip install --python outputs/rag_gpu_env/Scripts/python.exe -r requirements-rag-models.txt
outputs/rag_gpu_env/Scripts/python.exe scripts/build_rag_index.py --backend qwen --output data/rag/index/qwen --device cuda --dtype float16 --batch-size 2 --max-length 1024
outputs/rag_gpu_env/Scripts/python.exe scripts/eval_rag_retrieval.py --backend all --local-files-only --device cuda --dtype float16 --batch-size 2 --max-length 1024 --output outputs/rag_pipeline/full_baseline
```

첫 빌드에는 공식 Hugging Face 모델의 다운로드가 필요합니다. 이후 `--local-files-only`로 캐시만 사용합니다. 모델 revision, 프롬프트, pooling, dtype, 최대 길이는 모델 signature에 기록됩니다. signature가 달라지면 이전 인덱스 재사용을 거부하므로 별도 디렉터리에서 재빌드해야 합니다. `float16`/`bfloat16`과 SDPA를 지원하며 CPU 모델 실행은 `--device cpu --dtype float32`로 명시합니다. CPU 모델 실행도 가벼운 Hash 테스트와는 다릅니다.

쿼리 전용 instruction, left padding, last-token pooling, yes/no logits 방식은 [Qwen Embedding 모델 카드](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)와 [Qwen Reranker 모델 카드](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B)를 따릅니다. 작업 instruction과 reranker system 문구는 비임상 피부관리 문헌 검색용 **사용자 정의 프롬프트**이며 코드/모델 signature에 명시합니다. 공식 프롬프트 그대로의 성능 측정이라고 주장하지 않습니다. cosine와 inner product의 관계는 [FAISS 문서](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)를 참고합니다.

모델별 최대 입력 1,024 토큰, batch=2를 기본으로 하며 잘린 입력 수를 보고합니다. Reranker는 prefix/suffix를 보존하고 최종 토큰 logits만 계산해 불필요한 전체 시퀀스 vocabulary logits 메모리를 피합니다. Softmax 점수는 **관련도 모델 점수이지 안전 확률이 아닙니다**.

## 인덱스·메타데이터 보관

`data/rag/index/`는 기존 `.gitignore`로 제외되어 있습니다. FAISS 바이너리, 모델 가중치, NumPy 벡터는 커밋하지 않습니다. Python fallback 벡터도 같은 무시 경로에 저장합니다. 매니페스트는 코퍼스 SHA, 순서화된 참조, 모델 signature, 차원·행 수, 벡터 파일 SHA를 확인합니다. 출처가 불명확한 외부 FAISS 바이너리를 로드하는 용도가 아닙니다.

## 평가 설계와 해석

`data/rag/evaluation/queries.jsonl`은 합성 질의 40개입니다. 각 영역의 양성 8개씩 총 32개와 범위 밖/원문으로 확정할 수 없는 질의 8개를 포함합니다. calibration/evaluation은 각각 양성 16개 + 음성 4개입니다. 질의·qrel·임계값 후보를 모델 실행 전에 `frozen_protocol.json`에 기록합니다. qrel은 작성자의 잠정 판정이며 **독립 전문가/사람 검수 승인 아님**을 명시합니다.

- Recall@15, Recall@5, MRR@5, binary nDCG@5는 양성 질의에서 계산합니다.
- Threshold별 무관 유입은 **음성 질의에서 문서가 1개 이상 나온 비율**로 측정합니다. 양성 질의의 qrel은 전수 관련도 판정이 아니므로 비-qrel 문서는 `unjudged`로 보고하고 전부 무관하다고 단정하지 않습니다.
- 임계값은 calibration에서만 결정합니다. 가능한 경우 positive hit rate ≥90%를 먼저 보존하고, `MRR - 0.5×음성 유입률 - 0.1×미판정 문서 비율`을 최적화합니다. 동률이면 hit rate, 높은 threshold 순입니다. 이 가중치는 운영 승인 정책이 아닌 사전 고정된 실험 규칙입니다. evaluation sweep은 진단용이며 임계값 재선택에 쓰지 않습니다.
- 모델 로드·인덱스 빌드는 startup으로 따로 기록합니다. 두 calibration 질의 워밍업 후 순차 질의 단일 실행의 p50/p95를 계산합니다. GPU 결과의 `.cpu()` 전송으로 동기화되므로 완료 시간을 포함합니다. 서버 동시 부하/SLM 생성 지연은 포함하지 않습니다.
- Qwen dense-only 수치는 동일 실행의 Stage 1 trace에서 계산합니다. 독립 모델 로드 실험이나 전체 2-Stage 지연이 아닙니다.
- GPU `max_allocated`는 Torch tensor peak이고 `max_reserved`는 Torch allocator peak입니다. 다른 앱·드라이버까지 포함한 전체 GPU 점유율과 구분합니다.
- [rank-bm25](https://github.com/dorianbrown/rank_bm25)의 BM25Okapi(k1=1.5, b=0.75) 비교도 제공합니다. 문서와 질의를 NFKC·casefold한 단어/문자 bigram으로 동일하게 토큰화하며, 점수를 `max(0,score)/(1+max(0,score))`로 고정 변환해 같은 threshold 후보를 사용합니다. 확률 보정이 아니고 Hash와도 별개입니다. BM25 trace의 `dense_ms`는 어휘 검색 시간입니다.
- 평가가 40개(held-out 양성16/음성4)에 불과하므로 임계값의 일반화나 임상/운영 품질을 보장하지 않습니다. 독립 qrel 전수 판정은 추가 평가 범위로 남깁니다.

측정 결과 및 원시 candidate 점수는 같은 디렉터리의 보고 파일과 이 문서의 결과 절에 기록합니다. 결과 파일은 UTF-8(BOM 없음), LF입니다.
