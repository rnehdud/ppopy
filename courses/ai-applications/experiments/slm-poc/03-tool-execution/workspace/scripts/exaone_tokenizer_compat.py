"""Load the exact published tokenizer.json with Transformers 4.57's fast API."""
import json
from pathlib import Path
from transformers import PreTrainedTokenizerFast

def load(path):
    path=Path(path)
    cfg=json.loads((path/'tokenizer_config.json').read_text(encoding='utf-8'))
    return PreTrainedTokenizerFast(tokenizer_file=str(path/'tokenizer.json'),
      bos_token=cfg['bos_token'],eos_token=cfg['eos_token'],pad_token=cfg['pad_token'],unk_token=cfg['unk_token'],
      additional_special_tokens=cfg['extra_special_tokens'],
      chat_template=(path/'chat_template.jinja').read_text(encoding='utf-8'),
      clean_up_tokenization_spaces=cfg['clean_up_tokenization_spaces'])
