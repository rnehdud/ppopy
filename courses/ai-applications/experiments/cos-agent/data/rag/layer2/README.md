# 2계층 Reference RAG 입력

2026-11-27. 검증된 독립 요약 92문단(규제·표시 조건 `regulatory` 76, 평가방법 `safety_method` 16)을 ppopy 변환·검색 경로에 연결했다. 8개 공식 문서의 지정 판본 설명이며, 현재 제품의 적법성이나 개인별 안전 판정 자료가 아니다. 기존 1계층 151문단과 합쳐 243문단으로 변환할 수 있다.

## 팀원이 실행할 명령

`courses/ai-applications/experiments/cos-agent`에서 실행한다. 기본 환경은 `uv sync --locked`로 준비한다. 기존 `data/rag/chunks.jsonl`과 1계층 인덱스를 덮어쓰지 않는 명령이다.

```bash
uv run --locked python scripts/export_rag_chunks.py \
  --additional-corpus data/rag/layer2/corpus \
  --output outputs/rag-layer2/chunks.jsonl

uv run --locked python scripts/build_rag_index.py \
  --additional-corpus data/rag/layer2/corpus \
  --chunks outputs/rag-layer2/chunks.jsonl \
  --output outputs/rag-layer2/index

uv run --locked python scripts/query_rag.py 'SCCS systemic exposure dose' \
  --additional-corpus data/rag/layer2/corpus \
  --chunks outputs/rag-layer2/chunks.jsonl \
  --index outputs/rag-layer2/index \
  --source-unit L2U-0001 --threshold=-1
```

마지막 명령의 `--threshold=-1`은 결정적 HashFallback으로 연결을 확인하는 예시다. 실제 관련도 임계값 또는 평가 결과가 아니다. `--source-unit`은 그 단위와 **출처 ID·관할·판본·as_of가 정확히 같은** 문단들을 지정한다. 단일 문단 강제 반환이 아니며 여러 번 지정할 수 있다. 지정하지 않으면 2계층은 검색 결과에서 제외된다. 1계층 문단은 기존 기준으로 검색된다.

2계층만 변환하려면 `--corpus-dir data/rag/layer2/corpus`를 사용한다. 인덱스 생성·질의에서는 `--corpus data/rag/layer2/corpus`로 대응시키고 `--additional-corpus`를 생략한다. 변환 입력과 JSONL이 다르면 색인을 만들지 않는다.

기존 Qwen+FAISS 환경에서는 build/query에 동일한 `--backend qwen`, device, dtype, max-length 설정을 지정하면 된다. [기존 모델 환경 안내](../../../docs/reference-rag-pipeline.md)를 따른다. 코퍼스가 달라졌으므로 기존 151문단 인덱스를 재사용하지 말고 별도 디렉터리에 재생성한다. 이번 작업에서 Qwen 실행·관련도 평가·SLM 답변 평가는 하지 않았다.

## 입력과 보존 규칙

- `corpus/*.md`: 출처·위치·확인일·범위·한계를 포함한 92개 근거 문단. 기존 인계본과 본문이 동일하다.
- [CORPUS_MANIFEST.md](CORPUS_MANIFEST.md): 안정 단위 ID, 출처 ID, 정확한 문단·본문 해시. 작업 정본/검증 원장 열은 원래 로컬 감사 기록의 이름이며 이 공개 패키지의 실행 의존성이 아니다.
- [METADATA.md](METADATA.md): 관할, 판본, 대상, 농도 분모, 노출 경로, 집단, 시행기간, 검증 상태, 이용 근거. 문단 해시로 결합하며 단순 행 순서로 연결하지 않는다. `fixed_input` 행만 내부 작업 포인터로 보관하고 모델 입력에서 제외한다.
- [SOURCES.md](SOURCES.md): 8개 출처의 공식 URL, 판본, 원문 SHA-256과 이용 범위. 원문 PDF는 Git에 포함하지 않는다.

파서는 필수 메타데이터 누락·중복 ID·미등록 문단·본문 변조·정확한 `ready`가 아닌 상태를 거부한다. 청크 ID는 `ref:regulatory-L2U-0032`처럼 고정되며 파일·문단 순서를 바꾸어도 유지된다. 본문과 메타데이터 각각의 위치·한계 표현은 모두 보존한다.

## 사용 범위

2계층은 `source_explanation_only`만 허용한다. 검색에서 출처·관할·판본·as_of를 먼저 대조하고, 조건에 맞는 후보만 reranker로 전달한다. `Layer2Selection`을 생성할 때 현재 적합성 또는 개인 안전 판정 용도를 지정하면 오류가 난다. 규정과 평가방법의 경계를 쿼리 키워드로 추정하지 않는다.

시행·경과가 `unknown`인 22문단은 그 값이 JSONL과 SLM 입력에 그대로 남는다. 보관한 판본의 문구 설명에는 사용할 수 있지만 개별 제품의 시행·경과 적용 근거가 되지 않는다. 대상·제품군·농도 분모·경로·집단 조건도 함께 전달한다. 현재 적법성/제품 안전성 자동 판정은 구현하지 않았으며 SLM 지시만으로 임상 안전성을 보증하지 않는다.

SCCS 성분별 31개·CIR 58개·EU 향료 81개 등 전체 로드맵의 검증 완료를 의미하지 않는다. 보류 자료는 이 입력에 포함하지 않았다. 이번 PR은 검증된 92문단의 변환·검색 호환성을 완성하며 자료 범위를 확대하지 않는다.

## 검증

[실제 검사 결과 및 재현 명령](../../../docs/reference-rag-layer2-compatibility.md)을 참고한다. 모델 평가는 팀원이 별도로 수행한다. 서비스 배포·KB 판단 결합·개인 데이터 입력을 수행하지 않았다.

## SLM 팀에 넘길 검색 입력 만들기

위 변환·색인 명령을 그대로 실행하면 Hash 연결 검사용으로 사용할 수 있다. 실제 모델 실험에는 [Qwen 설치와 GPU 환경](../../../docs/reference-rag-pipeline.md)의 모델 의존성을 설치하고, 색인 생성과 아래 명령 모두 같은 임베딩 설정으로 실행한다. 다음 명령은 COS 디렉터리 기준이며, Qwen 인덱스는 Hash 인덱스와 별도 경로를 사용한다.

```powershell
python scripts/build_rag_index.py --additional-corpus data/rag/layer2/corpus --chunks outputs/rag-layer2/chunks.jsonl --output outputs/rag-layer2/qwen-index --backend qwen
python scripts/export_rag_contexts.py --input data/qlora/v2/qlora_solution_hold_v2.jsonl --chunks outputs/rag-layer2/chunks.jsonl --index outputs/rag-layer2/qwen-index --output outputs/rag-layer2/slm-contexts.jsonl --backend qwen --threshold 0.95
```

`0.95`는 기존 Tier 1 실험의 시작점이다. 합친 코퍼스에서 관련도와 범위 이탈을 평가하고, 임계값은 별도 보정 분할에서 결정한다. Hash 연결 검사는 기존 Hash 색인과 `--backend hash --threshold=-1`로 실행한다.

`--backend`는 임베딩·리랭킹 모델을 지정한다. 기본 저장 형식은 Qwen이면 FAISS, Hash면 Python 인덱스다. 색인 생성 시 `--index-backend faiss` 또는 `--index-backend python`으로 이를 바꿀 수 있다. 조회와 내보내기는 매니페스트에 기록된 저장 형식을 사용하고 모델 서명도 비교한다.

- 산출물은 기존 데이터셋의 `id`와 `split`을 유지한 별도 JSONL이다. `model_messages`에 모델에 보낼 system/user 메시지만, `retrieval`에 청크·출처·색인 버전을 기록한다. 원본 assistant 정답은 그대로 보관한다.
- 기존 답변이 인용한 문헌이 실제로 검색되지 않으면 `missing_target_refs`에 기록한다. `requires_target_review=true`인 행은 답변을 그대로 붙여 학습시키기 전에 검수한다. 인용이 모두 있어도 문헌이 답변의 주장을 지원하는지는 확인해야 한다.
- 일반 SOLUTION은 Tier 1만 검색한다. Tier 2 문서 설명 샘플은 `--source-questions <file.json>`으로 허용된 샘플 ID와 문서 범위를 명시한다. `{"sample-id":{"question":"SCCS 12판은 노출량을 어떻게 평가하나요?","source_unit":"L2U-0001"}}` 형태다. 해당 단위와 같은 출처·관할·판본·기준 시점의 문단만 검색하며 문서 설명 행은 항상 정답 검수 대상으로 표시한다. 근거가 없으면 `source_miss=true`, `model_messages=null`로 남긴다. HOLD에는 검색 근거를 추가하지 않는다.
- 순수 SFT에는 기존 검수 데이터셋을 사용할 수 있다. 이 출력은 실제 검색 입력으로 하는 생성 평가 또는 검색 결과에 맞춰 정답을 검수한 뒤 사용하는 증강 SFT의 재료다.
- 런타임에서는 `beauty_agent.rag.handoff.prepare_rag_input`을 호출해 같은 범위와 인용 규칙을 적용한다. 결과의 `request`가 `None`이면 `source_miss`이고, SLM을 호출하지 않고 지정 문서에서 근거를 찾지 못했다고 안내한다. `request`가 있으면 기존 생성·검증 경로로 전달한다.
