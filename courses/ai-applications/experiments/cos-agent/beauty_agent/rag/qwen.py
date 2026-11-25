"""Optional Qwen3 model backends; no downloads/imports at package import time.

Uses last-token pooling, query-only instructions and yes/no logit scoring as
documented by Qwen. Custom task/system prompts are versioned in signatures.
"""

from __future__ import annotations

import json
from typing import Sequence

TASK = "Retrieve relevant non-clinical skincare reference passages."
RERANK_SYSTEM = 'Determine whether the Document answers the Query under the Instruct. Answer only "yes" or "no".'


def _device_dtype(torch, device: str, dtype: str):
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA requested but unavailable; install CUDA PyTorch or explicitly select --device cpu"
        )
    if dtype not in {"float16", "bfloat16", "float32"}:
        raise ValueError("unsupported dtype")
    if device == "cpu" and dtype != "float32":
        raise ValueError("CPU backend requires float32")
    return getattr(torch, dtype)


class QwenEmbedder:
    model_name = "Qwen/Qwen3-Embedding-0.6B"

    def __init__(
        self,
        *,
        device="cuda",
        dtype="float16",
        batch_size=2,
        max_length=1024,
        revision=None,
        local_files_only=False,
    ):
        import torch
        from transformers import AutoModel, AutoTokenizer

        if batch_size < 1 or max_length < 64:
            raise ValueError("invalid batch size/max_length")
        selected = _device_dtype(torch, device, dtype)
        self.torch = torch
        self.device = device
        self.batch_size = batch_size
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            revision=revision,
            padding_side="left",
            local_files_only=local_files_only,
            trust_remote_code=False,
        )
        self.model = (
            AutoModel.from_pretrained(
                self.model_name,
                revision=revision,
                torch_dtype=selected,
                attn_implementation="sdpa",
                local_files_only=local_files_only,
                trust_remote_code=False,
            )
            .to(device)
            .eval()
        )
        self.revision = getattr(self.model.config, "_commit_hash", None) or revision
        self.signature = json.dumps(
            {
                "model": self.model_name,
                "revision": self.revision,
                "dtype": dtype,
                "max_length": max_length,
                "pooling": "last-token-left-v1",
                "query_task": TASK,
            },
            sort_keys=True,
        )
        self.truncated_inputs = 0

    def encode(
        self, texts: Sequence[str], *, is_query: bool = False
    ) -> list[list[float]]:
        torch = self.torch
        prepared = [
            f"Instruct: {TASK}\nQuery: {text}" if is_query else text for text in texts
        ]
        result = []
        with torch.inference_mode():
            for start in range(0, len(prepared), self.batch_size):
                batch = prepared[start : start + self.batch_size]
                lengths = [
                    len(x)
                    for x in self.tokenizer(
                        batch, add_special_tokens=True, truncation=False
                    )["input_ids"]
                ]
                self.truncated_inputs += sum(n > self.max_length for n in lengths)
                tensors = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt",
                ).to(self.device)
                hidden = self.model(**tensors, use_cache=False).last_hidden_state
                # Left padding ensures each final token is an actual document token.
                pooled = torch.nn.functional.normalize(
                    hidden[:, -1, :].float(), p=2, dim=1
                )
                result.extend(pooled.cpu().tolist())
        return result


class QwenReranker:
    model_name = "Qwen/Qwen3-Reranker-0.6B"

    def __init__(
        self,
        *,
        device="cuda",
        dtype="float16",
        batch_size=2,
        max_length=1024,
        revision=None,
        local_files_only=False,
    ):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if batch_size < 1 or max_length < 128:
            raise ValueError("invalid batch size/max_length")
        selected = _device_dtype(torch, device, dtype)
        self.torch = torch
        self.device = device
        self.batch_size = batch_size
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            revision=revision,
            padding_side="left",
            local_files_only=local_files_only,
            trust_remote_code=False,
        )
        self.model = (
            AutoModelForCausalLM.from_pretrained(
                self.model_name,
                revision=revision,
                torch_dtype=selected,
                attn_implementation="sdpa",
                local_files_only=local_files_only,
                trust_remote_code=False,
            )
            .to(device)
            .eval()
        )
        self.revision = getattr(self.model.config, "_commit_hash", None) or revision
        self.yes = self.tokenizer.convert_tokens_to_ids("yes")
        self.no = self.tokenizer.convert_tokens_to_ids("no")
        if self.yes == self.no or self.yes is None or self.no is None:
            raise ValueError("model lacks distinct yes/no tokens")
        prefix = f"<|im_start|>system\n{RERANK_SYSTEM}<|im_end|>\n<|im_start|>user\n"
        suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        self.prefix = self.tokenizer.encode(prefix, add_special_tokens=False)
        self.suffix = self.tokenizer.encode(suffix, add_special_tokens=False)
        self.signature = json.dumps(
            {
                "model": self.model_name,
                "revision": self.revision,
                "dtype": dtype,
                "max_length": max_length,
                "system": RERANK_SYSTEM,
                "task": TASK,
                "score": "softmax-no-yes-v1",
            },
            sort_keys=True,
        )
        self.truncated_inputs = 0

    def score(
        self, query: str, documents: Sequence[str], prior_scores: Sequence[float]
    ) -> list[float]:
        if len(documents) != len(prior_scores):
            raise ValueError("document/score count mismatch")
        torch = self.torch
        budget = self.max_length - len(self.prefix) - len(self.suffix)
        result = []
        with torch.inference_mode():
            for start in range(0, len(documents), self.batch_size):
                texts = [
                    f"<Instruct>: {TASK}\n<Query>: {query}\n<Document>: {doc}"
                    for doc in documents[start : start + self.batch_size]
                ]
                raw = self.tokenizer(texts, add_special_tokens=False, truncation=False)[
                    "input_ids"
                ]
                self.truncated_inputs += sum(len(ids) > budget for ids in raw)
                ids = [self.prefix + row[:budget] + self.suffix for row in raw]
                tensors = self.tokenizer.pad(
                    {"input_ids": ids}, padding=True, return_tensors="pt"
                ).to(self.device)
                # Only the final vocabulary slice is needed. Avoid an L*V logit
                # allocation on the 8GB laptop; Transformers Qwen3 supports this.
                logits = (
                    self.model(**tensors, use_cache=False, logits_to_keep=1)
                    .logits[:, -1, :]
                    .float()
                )
                scores = torch.softmax(logits[:, [self.no, self.yes]], dim=-1)[:, 1]
                result.extend(scores.cpu().tolist())
        return result
