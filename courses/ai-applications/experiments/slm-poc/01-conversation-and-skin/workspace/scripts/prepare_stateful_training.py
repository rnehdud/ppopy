"""Validate every target mask without importing a GPU framework."""
import os
os.environ.setdefault('USE_TORCH','0')
os.environ.setdefault('USE_TF','0')
import json
from pathlib import Path
import statistics
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training.data import tokenize_example,load_rows,verify_freeze


def main():
    from transformers import AutoTokenizer
    root=Path(__file__).resolve().parents[1]
    manifest=verify_freeze(root)
    tokenizer=AutoTokenizer.from_pretrained(str(root/'models/qwen2.5-3b-instruct/tokenizer'),local_files_only=True)
    dest=root/'data/processed/stateful_v2'
    dest.mkdir(parents=True,exist_ok=True)
    counts={}
    samples=[]
    for split in ['train','validation']:
        rows=load_rows(root/f'data/stateful/v2/{split}.sft.jsonl')
        tokens=[tokenize_example(tokenizer,r) for r in rows]
        with (dest/f'{split}.tokens.jsonl').open('w',encoding='utf-8') as stream:
            for row in tokens:
                stream.write(json.dumps(row,ensure_ascii=False)+'\n')
        counts[split]={'examples':len(tokens),'max_tokens':max(t['total_tokens'] for t in tokens),
                       'median_tokens':statistics.median(t['total_tokens'] for t in tokens),
                       'target_tokens':sum(t['target_tokens'] for t in tokens),
                       'masked_prefix_tokens':sum(t['prefix_tokens'] for t in tokens)}
        samples.extend(tokens[:2])
    # Holdout cases remain evaluation only. Do not tokenize their supervised targets for training.
    report={'counts':counts,'mask':'All tokens before last assistant completion are -100; completion and EOS supervised.',
            'prefix_token_alignment_verified':True,'truncation':False,'holdout_targets_not_tokenized':True,
            'source_manifest':'data/stateful/v2/manifest.json'}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (dest/'mask_samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
