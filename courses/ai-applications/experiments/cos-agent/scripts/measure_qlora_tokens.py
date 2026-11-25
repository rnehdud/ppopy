"""가중치나 학습 없이 지정 모델의 실제 토크나이저로 JSONL 길이를 측정해요."""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import statistics

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--model',default='Qwen/Qwen3-4B-Instruct-2507')
    parser.add_argument('--revision',default='cdbee75f17c01a7cc42f958dc650907174af0554')
    args=parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(args.model,revision=args.revision,trust_remote_code=False)
    raw=args.input.read_bytes(); digest=hashlib.sha256(raw).hexdigest()
    rows=[json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    measurements=[]
    for row in rows:
        messages=row['messages']
        rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=False)
        tokens=tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=False,return_dict=False)
        prefix=tokenizer.apply_chat_template(messages[:-1],tokenize=True,add_generation_prompt=True,return_dict=False)
        assert tokens[:len(prefix)]==prefix,row['id']
        assert all(message['content'] in rendered for message in messages),row['id']
        measurements.append({'row_id':row['id'],'mode':row['mode'],'split':row['split'],'total_tokens':len(tokens),
                             'prompt_tokens':len(prefix),'assistant_with_end_tokens':len(tokens)-len(prefix),
                             'end_marker_present':rendered.endswith('<|im_end|>\n')})
    lengths=sorted(r['total_tokens'] for r in measurements)
    p95=lengths[max(0,(len(lengths)*95+99)//100-1)]
    result={'model':args.model,'revision':args.revision,'dataset_sha256':digest,'rows':len(rows),
            'libraries':{name:importlib.metadata.version(name) for name in ['transformers','tokenizers','huggingface_hub']},
            'total_tokens':{'min':min(lengths),'p50':statistics.median(lengths),'p95':p95,'max':max(lengths),'sum':sum(lengths)},
            'assistant_tokens_sum':sum(r['assistant_with_end_tokens'] for r in measurements),
            'all_template_prefixes_match':True,'all_content_preserved':True,
            'all_end_markers_present':all(r['end_marker_present'] for r in measurements),
            'native_template_has_generation_blocks':'{% generation' in tokenizer.chat_template or '{%generation' in tokenizer.chat_template,
            'truncation':{str(n):{'exceeding':sum(r['total_tokens']>n for r in measurements),
                                  'losing_entire_assistant':sum(r['prompt_tokens']>=n for r in measurements)} for n in [1024,2048,4096,8192]},
            'longest_rows':sorted(measurements,key=lambda r:r['total_tokens'],reverse=True)[:10],
            'weights_downloaded':False,'training_executed':False,'GPU_memory_tested':False}
    assert args.input.read_bytes()==raw
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'token_report.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    with (args.output/'per_row_tokens.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(measurements[0]),lineterminator='\n');writer.writeheader();writer.writerows(measurements)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
