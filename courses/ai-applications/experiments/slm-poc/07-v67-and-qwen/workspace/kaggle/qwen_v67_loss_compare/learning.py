"""Final-token two-class objective shared by the runner and small CPU checks."""
def choice_logits(model, input_ids, no_id, yes_id):
    import torch
    result=model(input_ids=input_ids,attention_mask=torch.ones_like(input_ids),use_cache=False,logits_to_keep=1)
    return result.logits[0,-1,[no_id,yes_id]].float()

def choice_loss(logits,label):
    import torch
    return torch.nn.functional.cross_entropy(logits.unsqueeze(0),torch.tensor([label],device=logits.device))
