"""Local scalar ranker adapter for ChoiceAgent and arbitrary choice questions."""
from pathlib import Path

class LocalChoiceScorer:
    def __init__(self,model_path,adapter_path):
        import torch
        from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
        from peft import PeftModel
        if not torch.cuda.is_available():raise RuntimeError('CUDA GPU required for this NF4 prototype')
        self.torch=torch
        self.tokenizer=AutoTokenizer.from_pretrained(Path(model_path),local_files_only=True,trust_remote_code=False)
        self.tokenizer.padding_side='right'
        quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
        base=AutoModelForSequenceClassification.from_pretrained(Path(model_path),quantization_config=quant,torch_dtype=torch.float16,
             device_map={'':0},local_files_only=True,trust_remote_code=False)
        self.model=PeftModel.from_pretrained(base,str(adapter_path),is_trainable=False).eval()

    def __call__(self,question,options,context):
        first=[question+' '+v for v in options.values()]
        batch=self.tokenizer(first,[context]*len(first),padding=True,truncation=False,return_tensors='pt')
        if batch['input_ids'].shape[1]>512:raise ValueError('Input exceeds context; nothing was saved')
        with self.torch.inference_mode():
            logits=self.model(**{k:v.to('cuda') for k,v in batch.items()}).logits[:,0].double()
        return dict(zip(options,self.torch.softmax(logits,dim=0).tolist()))
