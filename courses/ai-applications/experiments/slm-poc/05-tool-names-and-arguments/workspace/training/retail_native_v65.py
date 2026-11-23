"""Assistant-only causal loss, computing the LM head at supervised positions."""


def assistant_loss(model, input_ids, start):
    import torch
    if input_ids.ndim != 2 or input_ids.shape[0] != 1 or not 0 < start < input_ids.shape[1]:
        raise ValueError('Expected one unpadded sequence with a nonempty assistant target')
    positions = torch.arange(start - 1, input_ids.shape[1] - 1, device=input_ids.device)
    out = model(input_ids=input_ids, attention_mask=torch.ones_like(input_ids), use_cache=False,
                logits_to_keep=positions)
    return torch.nn.functional.cross_entropy(out.logits[0].float(), input_ids[0, start:])
