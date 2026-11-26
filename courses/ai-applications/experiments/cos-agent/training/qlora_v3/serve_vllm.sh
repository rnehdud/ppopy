#!/usr/bin/env bash
set -euo pipefail
# Weights and adapters stay local; no model upload or public listener.
TASK_MODEL=${1:?Usage: serve_vllm.sh MODEL_DIR ADAPTER_DIR [PORT] [GPU_FRACTION] [SECOND_ADAPTER]}
TASK_ADAPTER=${2:?Adapter directory required}
TASK_PORT=${3:-8018}
TASK_GPU_FRACTION=${4:-0.75}
TASK_MAX_NUM_SEQS=${PPOPY_MAX_NUM_SEQS:-1}
TASK_VLLM_ENV=${PPOPY_VLLM_ENV:-"$HOME/.local/share/ppopy-vllm-v3"}
export PATH="$TASK_VLLM_ENV/bin:$PATH"
TASK_ALIAS=${PPOPY_ADAPTER_ALIAS:-ppopy-qlora-v3}
TASK_LORA_ARGS=(--lora-modules "$TASK_ALIAS=$TASK_ADAPTER")
if [[ -n "${5:-}" ]]; then
  TASK_LORA_ARGS+=("ppopy-epoch-2=$5" --max-loras 2 --max-cpu-loras 2)
fi
# Optional local Python development headers for an existing portable venv.
if [[ -n "${PPOPY_VLLM_BUILD_ROOT:-}" ]]; then
  export CPATH="$PPOPY_VLLM_BUILD_ROOT/python-dev/usr/include/python3.12:$PPOPY_VLLM_BUILD_ROOT/python-dev/usr/include/x86_64-linux-gnu/python3.12:${CPATH:-}"
fi
export VLLM_NO_USAGE_STATS=1
export DO_NOT_TRACK=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
# The v2 runner requires UVA, disabled by default on WSL2. Use the supported
# legacy runner without modifying vLLM packages or forcing host pinning.
export VLLM_USE_V2_MODEL_RUNNER=${VLLM_USE_V2_MODEL_RUNNER:-0}
# Use the supported PyTorch sampler; FlashInfer's optional sampler JIT needs nvcc.
export VLLM_USE_FLASHINFER_SAMPLER=${VLLM_USE_FLASHINFER_SAMPLER:-0}
exec "$TASK_VLLM_ENV/bin/vllm" serve "$TASK_MODEL" \
  --host 127.0.0.1 --port "$TASK_PORT" \
  --served-model-name ppopy-base-nf4 \
  --quantization bitsandbytes --load-format bitsandbytes --dtype bfloat16 \
  --enable-lora --max-lora-rank 16 "${TASK_LORA_ARGS[@]}" \
  --max-model-len 2304 --max-num-seqs "$TASK_MAX_NUM_SEQS" --max-num-batched-tokens 2304 \
  --gpu-memory-utilization "$TASK_GPU_FRACTION" --enforce-eager \
  --generation-config vllm --no-enable-log-requests
