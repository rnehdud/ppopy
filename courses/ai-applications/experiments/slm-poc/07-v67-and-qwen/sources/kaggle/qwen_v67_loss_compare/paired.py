"""Identical training rows, sampled rivals and order for both objectives."""
import hashlib
import json
import random
from common import SEED,epoch_plan

def paired_epoch_plan(items,epoch):
    original=epoch_plan(items,epoch)
    negatives={i:c for i,c,label in original if label==0}
    rows=[(i,item['positive_index'],negatives.get(i)) for i,item in enumerate(items)]
    random.Random(SEED+10000+epoch).shuffle(rows)
    return rows

def plan_hash(plan):
    return hashlib.sha256(json.dumps(plan,separators=(',',':')).encode()).hexdigest()

def row_loss(positive_logits,negative_logits,objective):
    import torch
    from learning import choice_loss
    if negative_logits is None:
        # No ranking decision exists in single-candidate rows. Keep the same
        # positive calibration term in both conditions, rather than drop rows.
        return choice_loss(positive_logits,1)
    if objective=='pointwise':
        return (choice_loss(positive_logits,1)+choice_loss(negative_logits,0))/2
    if objective=='relative':
        positive=positive_logits[1]-positive_logits[0]
        negative=negative_logits[1]-negative_logits[0]
        return torch.nn.functional.softplus(negative-positive)
    raise ValueError('Unknown objective: '+objective)

def adapter_fingerprint(model):
    """Compare initial trainable tensors without storing extra base weights."""
    h=hashlib.sha256()
    for name,p in sorted(model.named_parameters()):
        if not p.requires_grad:continue
        h.update(name.encode());h.update(str(tuple(p.shape)).encode())
        h.update(p.detach().float().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()
