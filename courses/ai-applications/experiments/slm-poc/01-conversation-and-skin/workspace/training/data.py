"""Prefix-checked assistant-only supervision for Qwen's tool template."""
import hashlib
import json


def tokenize_example(tokenizer,row,max_length=2048):
    messages=row['messages']
    if messages[-1]['role']!='assistant':
        raise ValueError('The final supervised message must be assistant')
    prefix=tokenizer.apply_chat_template(messages[:-1],tools=row['tools'],tokenize=False,add_generation_prompt=True)
    full=tokenizer.apply_chat_template(messages,tools=row['tools'],tokenize=False,add_generation_prompt=False)
    if not full.startswith(prefix):
        raise ValueError('Rendered completion does not extend the inference prefix')
    prefix_ids=tokenizer.encode(prefix,add_special_tokens=False)
    full_ids=tokenizer.encode(full,add_special_tokens=False)
    if full_ids[:len(prefix_ids)]!=prefix_ids:
        raise ValueError('Tokenizer changes prefix at completion boundary')
    if len(full_ids)>max_length:
        raise ValueError(f'Example is too long; never silently truncate: {len(full_ids)}>{max_length}')
    labels=[-100]*len(prefix_ids)+full_ids[len(prefix_ids):]
    if not any(x!=-100 for x in labels):
        raise ValueError('No assistant target tokens')
    return {'id':row['id'],'scenario_id':row['scenario_id'],'category':row['category'],
            'input_ids':full_ids,'labels':labels,'prefix_tokens':len(prefix_ids),
            'target_tokens':len(full_ids)-len(prefix_ids),'total_tokens':len(full_ids),
            'target_text':full[len(prefix):]}


def load_rows(path):
    with open(path,encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def verify_freeze(root,dataset='data/stateful/v2'):
    directory=root/dataset
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    for name,record in manifest['files'].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest()!=record['sha256']:
            raise ValueError(f'Frozen dataset was changed: {name}')
    return manifest
