"""Verify CUDA and a real NF4 forward/backward operation in the isolated env."""
import importlib.metadata
import json
from pathlib import Path
import sys


def main():
    import torch
    import bitsandbytes as bnb
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA unavailable')
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    layer=bnb.nn.Linear4bit(16,16,bias=False,compute_dtype=dtype,quant_type='nf4').cuda()
    inputs=torch.randn(2,16,device='cuda',dtype=dtype,requires_grad=True)
    loss=layer(inputs).float().square().mean()
    loss.backward()
    assert inputs.grad is not None and torch.isfinite(inputs.grad).all()
    report={'python':sys.version,'executable':sys.executable,
            'packages':{p:importlib.metadata.version(p) for p in ['torch','transformers','peft','bitsandbytes','accelerate']},
            'cuda_runtime':torch.version.cuda,'cuda_available':True,'gpu':torch.cuda.get_device_name(0),
            'bf16_supported':torch.cuda.is_bf16_supported(),'nf4_forward_backward_passed':True}
    root=Path(__file__).resolve().parents[1]
    out=root/'output/training/environment.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
