"""One quantized base with three frozen role adapters, serialized by server LOCK."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


class ChatModels:
    def __init__(self,research=False):
        import torch
        from peft import prepare_model_for_kbit_training
        from agent.local_choice_scorer_v1 import LocalChoiceScorer
        config=json.loads(Path(__file__).with_name('chat_models.json').read_text(encoding='utf-8'));self.config=config
        for role in (['symptom','selector','gate'] if research else ['symptom']):
            c=config['roles'][role]
            h=hashlib.sha256((ROOT/c['path']/'adapter_model.safetensors').read_bytes()).hexdigest()
            if h!=c['sha256']:raise ValueError('Unexpected adapter: '+role)
        torch.set_num_threads(4);self.torch=torch
        self.base=LocalChoiceScorer(ROOT/config['base'],ROOT/config['roles']['symptom']['path']);prepare_model_for_kbit_training(self.base.model,use_gradient_checkpointing=False)
        self.roles={'symptom':'default'}
        if research:
            self.roles.update(selector='tool_selector',gate='call_gate')
            for role in ['selector','gate']:self.base.model.load_adapter(str(ROOT/config['roles'][role]['path']),adapter_name=self.roles[role],is_trainable=False)
        self.base.model.eval()
    def score(self,role,view):
        self.base.model.set_adapter(self.roles[role]);self.base.model.eval();keys=list(view['options'])
        b=self.base.tokenizer([view['question']+' '+v for v in view['options'].values()],[view['context']]*len(keys),padding=True,truncation=False,return_tensors='pt')
        tokens=int(b['input_ids'].shape[1])
        if tokens>512:raise ValueError('Input exceeds model context; nothing was truncated')
        with self.torch.inference_mode(),self.torch.autocast('cuda',dtype=self.torch.float16):
            vals=self.base.model(**{k:v.to('cuda') for k,v in b.items()}).logits[:,0].float().cpu().tolist()
        return {'raw_scores':dict(zip(keys,vals)),'tokens':tokens,'role':role,'adapter_sha256':self.config['roles'][role]['sha256']}
