"""Normalize the downloaded Korean tool-use corpus; never execute dataset tools."""
import os
os.environ.setdefault('USE_TORCH', '0')
os.environ.setdefault('USE_TF', '0')

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import statistics
import unicodedata

from jsonschema import Draft202012Validator, ValidationError, SchemaError

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/raw/glaive-function-calling-v2-ko/train.json'
DEST = ROOT/'data/processed/qwen_tool_use'
TOKENIZER = ROOT/'models/qwen2.5-3b-instruct/tokenizer'


class Reject(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def parse_tools(text):
    if not text.strip():
        return []
    decoder, offset, objects = json.JSONDecoder(), 0, []
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            break
        value, offset = decoder.raw_decode(text, offset)
        objects.extend(value if isinstance(value,list) else [value])
    tools, seen = [], {}
    for item in objects:
        fn = item.get('function') if item.get('type') == 'function' else item
        if not isinstance(fn,dict) or not isinstance(fn.get('name'),str):
            raise Reject('invalid_tool_definition')
        schema = fn.get('parameters', {'type':'object','properties':{}})
        Draft202012Validator.check_schema(schema)
        if fn['name'] in seen:
            if canonical(fn) == seen[fn['name']]:
                continue
            raise Reject('conflicting_tool_definitions')
        seen[fn['name']] = canonical(fn)
        tools.append({'type':'function','function':fn})
    return tools


def parse_call(text):
    """Parse JSON, a literal-only wrapper, or the source's multiline quoted JSON.

    ast.literal_eval never executes expressions. Incomplete wrappers are rejected;
    there is no eval(), inferred function name, or invented argument/result.
    """
    try:
        call = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        try:
            call = ast.literal_eval(text)
        except (SyntaxError,ValueError):
            match = re.fullmatch(
                r'''\s*\{\s*"name"\s*:\s*("(?:\\.|[^"\\])*")\s*,\s*"arguments"\s*:\s*'(.*)'\s*\}\s*''',
                text, flags=re.DOTALL)
            if not match:
                raise Reject('unparseable_call')
            call = {'name':json.loads(match[1]),'arguments':json.loads(match[2])}
    if not isinstance(call,dict) or not isinstance(call.get('name'),str):
        raise Reject('invalid_call_shape')
    arguments = call.get('arguments',{})
    if isinstance(arguments,str):
        arguments = json.loads(arguments)
    if not isinstance(arguments,dict):
        raise Reject('arguments_not_object')
    return {'name':call['name'],'arguments':arguments}


def normalize(row,index):
    tools = parse_tools(row.get('function_description',''))
    by_name = {t['function']['name']:t['function'] for t in tools}
    conversation = row.get('conversations_ko')
    if not isinstance(conversation,list) or not conversation:
        raise Reject('missing_korean_conversation')
    messages = [{'role':'system','content':row.get('system_message') or 'You are a helpful assistant.'}]
    pending, calls = None, 0
    for original in conversation:
        role, content = original.get('role'), original.get('content')
        if not isinstance(content,str):
            raise Reject('content_not_string')
        if role == 'function-call':
            if pending:
                raise Reject('missing_tool_response')
            call = parse_call(content)
            if call['name'] not in by_name:
                raise Reject('undefined_tool')
            fn = by_name[call['name']]
            schema = fn.get('parameters',{'type':'object'})
            if list(Draft202012Validator(schema).iter_errors(call['arguments'])):
                raise Reject('argument_schema_mismatch')
            if 'properties' in schema and set(call['arguments']) - set(schema['properties']):
                raise Reject('undeclared_argument')
            calls += 1
            pending = f'call_{index}_{calls}'
            item = {'id':pending,'type':'function','function':call}
            if messages[-1]['role'] == 'assistant' and not messages[-1].get('tool_calls'):
                messages[-1]['tool_calls'] = [item]
            else:
                messages.append({'role':'assistant','content':'','tool_calls':[item]})
        elif role == 'function-response':
            if not pending:
                raise Reject('orphan_tool_response')
            name = messages[-1]['tool_calls'][0]['function']['name']
            messages.append({'role':'tool','name':name,'tool_call_id':pending,'content':content})
            pending = None
        elif role in {'user','assistant'}:
            if pending:
                raise Reject('missing_tool_response')
            messages.append({'role':role,'content':content})
        else:
            raise Reject('unsupported_role')
    if pending:
        raise Reject('missing_tool_response')
    if messages[1]['role'] != 'user' or messages[-1]['role'] != 'assistant':
        raise Reject('invalid_conversation_boundary')
    normalized_for_dedup = [dict(m) for m in messages]
    for m in normalized_for_dedup:
        m.pop('tool_call_id',None)
        if m.get('tool_calls'):
            m['tool_calls'] = [{'type':v['type'],'function':v['function']} for v in m['tool_calls']]
    # Group by the original (English) dialogue, so translations/copies do not cross splits.
    origin = row.get('conversations') or normalized_for_dedup
    group = digest(origin)
    return {'id':f'glaive-ko-{index:05d}', 'source_index':index,'source_group':group,
            'messages':messages,'tools':tools,'tool_call_count':calls,
            'content_hash':digest({'messages':normalized_for_dedup,'tools':tools})}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=0)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(str(TOKENIZER),local_files_only=True)
    DEST.mkdir(parents=True,exist_ok=True)
    rejects,accepted,lengths,seen,groups = Counter(),Counter(),[],set(),{}
    files = {split:(DEST/f'{split}.jsonl').open('w',encoding='utf-8') for split in ['train','validation','test']}
    rejection_file = (DEST/'rejected.jsonl').open('w',encoding='utf-8')
    total, render_samples = 0, []
    try:
        with SOURCE.open(encoding='utf-8') as source:
            for index,line in enumerate(source):
                if args.limit and index >= args.limit:
                    break
                total += 1
                try:
                    row = normalize(json.loads(line),index)
                    if row['content_hash'] in seen:
                        raise Reject('duplicate_normalized_content')
                    token_ids = tok.apply_chat_template(row['messages'],tools=row['tools'],tokenize=True,add_generation_prompt=False,return_dict=False)
                    if not isinstance(token_ids,list) or len(token_ids)<10:
                        raise RuntimeError('Unexpected tokenizer return shape or implausible token count')
                    row['token_count'] = len(token_ids)
                    row['eligible_2048'] = len(token_ids) <= 2048
                    bucket = int(row['source_group'][:8],16) % 100
                    split = 'train' if bucket < 90 else 'validation' if bucket < 95 else 'test'
                    previous = groups.setdefault(row['source_group'],split)
                    assert previous == split
                    files[split].write(json.dumps(row,ensure_ascii=False)+'\n')
                    seen.add(row['content_hash'])
                    lengths.append(len(token_ids))
                    accepted[split] += 1
                    accepted['with_calls' if row['tool_call_count'] else 'no_call'] += 1
                    accepted['eligible_2048'] += int(row['eligible_2048'])
                    if len(render_samples) < 3 and row['tool_call_count']:
                        rendered = tok.apply_chat_template(row['messages'],tools=row['tools'],tokenize=False,add_generation_prompt=False)
                        render_samples.append({'id':row['id'],'rendered':rendered,'token_count':len(token_ids)})
                except (Reject,ValueError,SyntaxError,TypeError,KeyError,SchemaError) as exc:
                    reason = str(exc) if isinstance(exc,Reject) else type(exc).__name__
                    rejects[reason] += 1
                    rejection_file.write(json.dumps({'source_index':index,'reason':reason},ensure_ascii=False)+'\n')
                if total % 2000 == 0:
                    print(f'Processed {total}: accepted {len(lengths)}, rejected {sum(rejects.values())}',flush=True)
    finally:
        for f in files.values():
            f.close()
        rejection_file.close()
    sorted_lengths = sorted(lengths)
    report = {'source_rows':total,'accepted_rows':len(lengths),'rejected_rows':sum(rejects.values()),
              'counts':dict(accepted),'rejection_reasons':dict(rejects),
              'token_length':{'median':statistics.median(lengths),'p95':sorted_lengths[int((len(lengths)-1)*.95)],'max':max(lengths)},
              'split_policy':'deterministic 90/5/5 by SHA256 of original dialogue; exact normalized duplicates removed',
              'source_manifest':'data/raw/download_manifest.json','tokenizer_manifest':'models/qwen2.5-3b-instruct/manifest.json',
              'truncation':False,'training_started':False,
              'limitations':['Structural validation is not a full semantic/translation audit.',
                             'No explicit skincare state labels are invented for this general tool-use corpus.',
                             'FunctionChat-Bench remains evaluation-only and is not read by this converter.']}
    (DEST/'preparation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (DEST/'rendered_samples.json').write_text(json.dumps(render_samples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__ == '__main__':
    main()
