#!/usr/bin/env bash
set -euo pipefail
# Weights and adapters stay local; no model upload or public listener.
TASK_MODEL=${1:?Usage: serve_vllm.sh MODEL_DIR ADAPTER_DIR [PORT] [GPU_FRACTION]}
TASK_ADAPTER=${2:?Adapter directory required}
TASK_PORT=${3:-8018}
TASK_GPU_FRACTION=${4:-0.75}
TASK_VLLM_ENV=${PPOPY_VLLM_ENV:-"$HOME/.local/share/ppopy-vllm-v3"}
export VLLM_NO_USAGE_STATS=1
export DO_NOT_TRACK=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
exec "$TASK_VLLM_ENV/bin/vllm" serve "$TASK_MODEL" \
  --host 127.0.0.1 --port "$TASK_PORT" \
  --served-model-name ppopy-base-nf4 \
  --quantization bitsandbytes --dtype bfloat16 \
  --enable-lora --max-lora-rank 16 --lora-modules "ppopy-qlora-v3=$TASK_ADAPTER" \
  --max-model-len 2304 --max-num-seqs 1 --max-num-batched-tokens 2304 \
  --gpu-memory-utilization "$TASK_GPU_FRACTION" --enforce-eager \
  --generation-config vllm --disable-log-requests
