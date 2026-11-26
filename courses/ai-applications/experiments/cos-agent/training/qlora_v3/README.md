# Qwen3-4B RAG-free QLoRA · 로컬 학습/WSL vLLM 평가

기준: 최신 main `dbef374`, 승인된 Zero-Base 900턴. 810건만 학습하고 90건은 epoch별 개발 검증·체크포인트 선택에만 사용해요. 독립 최종 test는 아니에요.

**가중치·어댑터는 로컬 `outputs/`에만 저장하고 Hugging Face/Drive/Git에 업로드하지 않아요.** Git에는 코드·설정·검사·비교 리포트만 넣어요. 개발 프리뷰이며 실제 사용자 수집·운영·자동 개선 판정을 활성화하지 않아요.

2026-11-26 팀원 검수용 공유: [로컬 2 epoch 결과 패키지](results/local_2epoch_20261126/README.md)에 전체 270개 생성 답변, 실제 입력·근거, 학습 로그, 그래프와 체크포인트 설정·가중치 해시를 보존했어요. 사용자 최신 지시에 따라 가중치는 Git에 포함하지 않고 별도 전달해요. 모델 출력 의미 전수 검수와 최종 checkpoint 승인은 미완료예요.

## 실행 환경

- 학습: CUDA PyTorch 2.9.1, Transformers 4.57.3, PEFT 0.17.1, bitsandbytes 0.48.2 (`requirements.txt`). CUDA torch는 공식 cu128 인덱스에서 설치해요. CPU 전용 torch로 실행하지 않아요.
- 서빙: 사용자가 지정한 **WSL2 vLLM** (`requirements-vllm.txt`), 학습 환경과 분리해요.
- 원본 모델: `Qwen/Qwen3-4B-Instruct-2507`, revision `cdbee75f17c01a7cc42f958dc650907174af0554`. 모델 라이선스/설명은 [공식 모델 카드](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)를 확인해요.

## 학습 전 확인

```powershell
python -m pytest training/qlora_v3/tests -q
python training/qlora_v3/train.py --model-path <로컬 원본 모델 폴더> --output outputs/qlora_v3_training/preflight --prepare-only
python training/qlora_v3/train.py --model-path <로컬 원본 모델 폴더> --output outputs/qlora_v3_training/smoke_longest --smoke
```

`mask_sample.json`에는 실제 한 샘플의 전체 input_ids/labels가 있어요. system·user와 assistant 역할 헤더는 -100, assistant 내용과 종료 토큰만 목표예요. max_seq_length=2048을 넘으면 잘라 쓰지 않고 실패해요. prepare-only와 한 optimizer step smoke는 전체 학습 완료를 뜻하지 않아요.

메모리를 줄이기 위해 decoder의 assistant 예측 위치만 vocabulary head에 투영해요. 이는 masked prompt logits만 생략하는 방식이며 표준 `cross_entropy(ignore_index=-100)`와 loss·gradient가 같음을 수치 테스트해요. 입력/문헌을 줄이거나 감독 토큰을 바꾸는 방식이 아니에요.

## 학습·평가

```powershell
python training/qlora_v3/train.py --model-path <로컬 원본 모델 폴더> --output outputs/qlora_v3_training/run_20261125
```

`config.json`: NF4 double quant, bf16 지원 시 bf16, LoRA r16/alpha32/dropout0.05, q/k/v/o/gate/up/down, lr=1e-4, cosine, 2 epoch, batch1/gradient accumulation8, gradient checkpointing. 같은 NF4 backbone의 어댑터 비활성 Base와 각 epoch를 동일한 90건·greedy·최대384토큰 조건으로 비교해요.

체크포인트 선택은 deterministic 안전/인용 flag 행 수를 우선하고 이후 val token loss를 비교해요. regex·ID 검사만으로 사실 충실성·간접 방해 주제 유출이 없다고 판정하지 않아요. 실제 입력·문헌·응답의 내용 검수는 `review_pack.py`로 묶어 별도로 기록해요. 재실행 시 같은 평가 폴더에 이미 완료된 행은 ID를 대조해 이어가지만, 학습된 체크포인트가 있는 폴더에서 처음부터 다시 학습해 덮어쓰지는 않아요.

`--defer-generation`을 쓰면 Windows에서는 Base·epoch별 assistant-token loss와 학습만 측정해요. 이후 `evaluate_vllm.py --run <실제 학습 폴더>`가 WSL vLLM의 `ppopy-base-nf4`, `ppopy-epoch-1`, `ppopy-epoch-2` 별칭으로 각각 90건을 생성하고 선택 파일을 만들어요. 품질 생성은 120초 상한이고 앱의 15초 SLA 시험과 구분해요. loss는 Transformers NF4 double-quant, 생성은 vLLM inflight NF4이므로 서로 다른 백엔드이며 이를 결과에 명시해요.

## WSL vLLM

```bash
bash training/qlora_v3/serve_vllm.sh /mnt/c/.../원본모델 /mnt/c/.../선택한어댑터 8018 0.75
```

기존 venv를 재사용하면 `PPOPY_VLLM_ENV=/경로/venv`를 지정해요. vLLM 0.28.0에서는 `vllm-bnb-plugin==0.0.2`를 포함하며 설치된 환경의 CLI·실제 로딩 결과로 호환성을 확인해요.

두 epoch 비교는 `PPOPY_ADAPTER_ALIAS=ppopy-epoch-1`을 설정하고 다섯 번째 인자로 epoch-2 경로를 전달해요. 최종 HTTP 시험은 `benchmark_http.py --adapter-model ppopy-epoch-N`으로 선택한 별칭을 지정해요. 임시 환경의 Python 개발 헤더가 필요할 때만 `PPOPY_VLLM_BUILD_ROOT`를 사용해요.

완료된 학습은 `run_local_pipeline.py`로 평가만 재개할 수 있어요. 이때 `training_complete.json`과 실제 두 어댑터 파일을 확인하며, 종료된 학습 PID를 다시 요구하거나 재학습하지 않아요. WSL2의 UVA 기본 제한 때문에 고정 버전 0.28.0에서는 `VLLM_USE_V2_MODEL_RUNNER=0`으로 model runner를 선택해요(V1 엔진 자체는 그대로예요). 최신 버전 전체에 적용되는 설정으로 일반화하지 않아요. `--client-in-wsl` 측정은 **WSL 내부 loopback** 경로이며 Windows 호스트의 localhost forwarding 성공을 뜻하지 않아요. Windows 연결은 별도 확인해야 해요.

평가 일괄 처리에는 `--concurrency 4`를 사용할 수 있어요. 서버도 `max_num_seqs=4`로 시작하고 클라이언트는 최대 네 요청을 동시에 보내요. 입력·문헌·384토큰 상한은 줄이지 않아요. 1건씩 처리한 이전 결과는 별도 archive로 보존하고, 세 모델은 같은 새 프로파일로 평가해요. batch 수치 연산에 따라 greedy 출력도 달라질 수 있어 동일 출력을 보장하지 않아요. 각 응답에 실제 concurrency를 기록하고 완료 순서가 달라도 원래 ID 순서로 원자적 저장·재개해요.

`--speed-probe-baseline <보존한 sequential predictions.jsonl>`은 기존 17~24번째의 고정된 8개 입력을 병렬로 재실행해 실제 처리량·raw 출력 차이를 기록해요. 초기 어댑터 로딩 프로브와 겹친 첫 행들은 피하며, 결과가 나올 때까지 배속을 확정하지 않아요. 이 실험은 서로 다른 시간의 공유 PC 측정이므로 통제된 하드웨어 벤치마크는 아니에요. 전체 평가 처리량과 앱의 단일 요청 15초 SLA는 별개이며 후자는 `benchmark_http.py`로 1건씩 별도 측정해요.

## 실제 내용 검수·메모리·로컬 기록

`compile_semantic_review.py`는 사람이 승인한 것으로 표시하지 않으며, Codex가 실제 읽고 작성한 `manual_review_notes.jsonl`만 raw 요청·응답 해시에 묶어요. 후보 문구와 근거 문구가 원문에 있는지도 대조해요. 검토하지 않은 행에 PASS를 채우지 않고 고유 상황 수와 모델 응답 수를 따로 집계해요. `summarize_vram.py`는 실제 구간 timestamp와 GPU CSV 표본을 연결해요. PyTorch allocated/reserved와 다른 앱까지 포함한 GPU 전체 점유를 구분하며, RAG 동시 상주는 직접 시험하지 않았다면 미실시로 남겨요.

실측 결과를 로컬 MLflow에 가져올 때의 검증된 명령은 `uv run --locked --group tracking --with "SQLAlchemy==2.0.44" python training/qlora_v3/log_mlflow.py --run <실제 실행 폴더> --report <실제 보고서 폴더>`예요. 현재 lock의 SQLAlchemy 2.1.9는 MLflow 3.6.0의 `FallbackAsyncAdaptedQueuePool` import와 맞지 않아, lock·코어 변경 없이 호환 버전을 임시 overlay로 사용했어요. 이 명령은 이미 끝난 측정의 사후 등록이지 새 학습이 아니며 가중치는 기록·업로드하지 않아요. `outputs/afa-mlflow/`의 로컬 SQLite·artifact만 사용해요.

같은 서버에서 `ppopy-base-nf4`와 `ppopy-qlora-v3`를 요청해요. 127.0.0.1에만 바인딩하고 모델/usage 업로드를 활성화하지 않아요. `benchmark_http.py`는 실제 저장소의 OpenAICompatSLMClient를 통해 15초·64KiB 상한과 fallback을 측정해요. fallback을 모델 성공으로 집계하지 않아요. RAG 동시 상주 시험은 `coload_rag.py`로 실제 두 모델을 유지한 상태에서 별도 수행해요.

참고: [PEFT quantization](https://huggingface.co/docs/peft/developer_guides/quantization), [vLLM bitsandbytes](https://docs.vllm.ai/en/v0.28.0/features/quantization/bnb/), [vLLM LoRA](https://docs.vllm.ai/en/v0.28.0/features/lora/). 실제 실행 결과와 제약은 비교 리포트에 기록하며 미실행 항목을 0/PASS로 채우지 않아요.
