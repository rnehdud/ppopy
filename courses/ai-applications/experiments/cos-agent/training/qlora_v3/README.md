# Qwen3-4B RAG-free QLoRA · 로컬 학습/WSL vLLM 평가

기준: 최신 main `dbef374`, 승인된 Zero-Base 900턴. 810건만 학습하고 90건은 epoch별 개발 검증·체크포인트 선택에만 사용해요. 독립 최종 test는 아니에요.

**가중치·어댑터는 로컬 `outputs/`에만 저장하고 Hugging Face/Drive/Git에 업로드하지 않아요.** Git에는 코드·설정·검사·비교 리포트만 넣어요. 개발 프리뷰이며 실제 사용자 수집·운영·자동 개선 판정을 활성화하지 않아요.

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

## WSL vLLM

```bash
bash training/qlora_v3/serve_vllm.sh /mnt/c/.../원본모델 /mnt/c/.../선택한어댑터 8018 0.75
```

같은 서버에서 `ppopy-base-nf4`와 `ppopy-qlora-v3`를 요청해요. 127.0.0.1에만 바인딩하고 모델/usage 업로드를 활성화하지 않아요. `benchmark_http.py`는 실제 저장소의 OpenAICompatSLMClient를 통해 15초·64KiB 상한과 fallback을 측정해요. fallback을 모델 성공으로 집계하지 않아요. RAG 동시 상주 시험은 `coload_rag.py`로 실제 두 모델을 유지한 상태에서 별도 수행해요.

참고: [PEFT quantization](https://huggingface.co/docs/peft/developer_guides/quantization), [vLLM bitsandbytes](https://docs.vllm.ai/en/v0.11.2/features/quantization/bnb/), [vLLM LoRA](https://docs.vllm.ai/en/v0.11.2/features/lora/). 실제 실행 결과와 제약은 비교 리포트에 기록하며 미실행 항목을 0/PASS로 채우지 않아요.
