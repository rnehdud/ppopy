"""Select existing PyTorch SDPA kernels; do not change attention mathematics."""


def install():
    from transformers import AttentionInterface
    from transformers.integrations.sdpa_attention import sdpa_attention_forward
    from torch.nn.attention import sdpa_kernel, SDPBackend

    def attention(module, query, key, value, attention_mask, **kwargs):
        # This Windows wheel has no FlashAttention. The default GQA math kernel
        # materializes long-query quadratic intermediates. cuDNN supports the
        # same operation here; keep the lightweight math path for token decoding.
        backend = SDPBackend.CUDNN_ATTENTION if query.shape[-2] > 256 else SDPBackend.MATH
        with sdpa_kernel(backend):
            return sdpa_attention_forward(module, query, key, value, attention_mask, **kwargs)

    AttentionInterface.register('v65_cudnn_long', attention)
    return 'v65_cudnn_long'
