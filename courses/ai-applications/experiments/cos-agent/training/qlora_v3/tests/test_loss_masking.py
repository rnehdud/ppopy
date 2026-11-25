import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from common import selected_position_loss,encode

def test_compacted_ce_equals_full_ce_and_gradients():
    torch.manual_seed(42)
    hidden=torch.randn(2,9,7,requires_grad=True)
    head=torch.nn.Linear(7,19,bias=False)
    labels=torch.tensor([[-100]*5+[1,2,3,4],[-100]*6+[5,6,-100]])
    full=torch.nn.functional.cross_entropy(head(hidden)[:,:-1].reshape(-1,19),labels[:,1:].reshape(-1),ignore_index=-100)
    compact,n=selected_position_loss(hidden,labels,head)
    assert n==6
    a=torch.autograd.grad(full,[hidden,head.weight],retain_graph=True)
    b=torch.autograd.grad(compact,[hidden,head.weight])
    torch.testing.assert_close(full,compact)
    for x,y in zip(a,b):torch.testing.assert_close(x,y)
    assert torch.count_nonzero(b[0][:,:4])==0

def test_prefix_mask_no_truncation():
    class TinyTokenizer:
        def apply_chat_template(self,messages,tokenize,add_generation_prompt):return [11,12,13] if add_generation_prompt else [11,12,13,14,15]
    row={'id':'synthetic','messages':[{'role':'user','content':'입력'},{'role':'assistant','content':'응답'}]}
    item=encode(row,TinyTokenizer(),5)
    assert item['labels']==[-100,-100,-100,14,15]
    import pytest
    with pytest.raises(AssertionError):encode(row,TinyTokenizer(),4)
