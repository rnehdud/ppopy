"""Reference-only2x2 selector interface diagnostic, not an agent benchmark."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.heterogeneous_tool_checker_v1 import SELECTOR,read,read_jsonl,save,digest
from scripts.build_tool_decision_mix_v1 import stable
from scripts.tool_split_data_v1 import SELECT_QUESTION

DATA=ROOT/'data/processed/selector-interface-v18'
OUT=ROOT/'output/diagnostics/selector-interface-v18'
MODEL=ROOT/'models/ko-decision-roberta-large'
V16=ROOT/'output/diagnostics/source-policy-korean-v16'
SOURCE=ROOT/'data/raw/functionchat-bench/data/FunctionChat-Singlecall.jsonl'
CONDITIONS=['current_full','current_readable','capability_full','capability_readable']
CAPABILITY_QUESTION='사용자가 요청한 작업을 담당할 수 있는 도구 하나를 선택하세요. 필요한 인자의 값이 모두 주어졌는지는 판단하지 마세요.'
NO_TOOL='지금은 도구를 호출하지 않고 사용자에게 직접 답하거나 필요한 정보를 확인한다.'


def full(tool):
    return tool['description']+' 필수 인자: '+stable(tool['parameters'].get('required') or [])+'\n인자 정의: '+stable(tool['parameters'])+'\n도구 이름: '+tool['name']


def readable(tool):
    params=tool.get('parameters') or {};required=params.get('required') or [];props=params.get('properties') or {}
    lines=['도구 이름: '+tool['name'],'하는 일: '+tool['description']]
    for key in sorted(props):
        definition=props[key]
        details={k:v for k,v in definition.items() if k not in ['type','description']}
        lines.append('입력 '+key+' ('+('필수' if key in required else '선택')+', '+stable(definition.get('type'))+'): '+definition.get('description','')+(' / '+stable(details) if details else ''))
    # Retain all top-level input constraints, not just descriptions/types.
    other={k:v for k,v in params.items() if k not in ['properties','required']}
    if other:lines.append('입력 조건: '+stable(other))
    if not props:lines.append('정의된 입력 항목 없음')
    missing=[k for k in required if k not in props]
    if missing:lines.append('추가 필수 입력: '+stable(missing))
    extra={k:v for k,v in tool.items() if k not in ['name','description','parameters']}
    if extra:lines.append('추가 도구 정의: '+stable(extra))
    return '\n'.join(lines)


def view(row,condition,reverse=False):
    question=CAPABILITY_QUESTION if condition.startswith('capability_') else SELECT_QUESTION
    formatter=readable if condition.endswith('_readable') else full
    items=[(t['name'],formatter(t)) for t in row['tools']]
    if reverse:items.reverse()
    options=dict(items)
    if row['cohort']=='v16':options['no_tool']=NO_TOOL
    messages=row['messages']
    context='대화:\n'+stable(messages[:-1])+'\n이번 사용자 발화: '+messages[-1]['content']
    return {'question':question,'options':options,'context':context}


def collect():
    result=[]
    for r in read_jsonl(ROOT/'data/processed/source-policy-korean-v16/fresh.jsonl'):
        result.append({'id':r['id'],'cohort':'v16','group':r['case_kind'],'query_group':r['group_id'],'messages':r['messages'],'tools':r['tools'],
            'expected':[r['operation_group']],'was_needed_call':bool(r['reference_calls']),
            'label_scope':'Authored requested operation; target tool exists even when arguments incomplete.'})
    for r in read_jsonl(SOURCE):
        for options in r['tools']:
            if options['type']=='exact':continue
            for q in r['query']:
                result.append({'id':f"functionchat:{r['function_num']}:{q['serial_num']}:{options['type']}",
                    'cohort':'functionchat','group':options['type'],'query_group':'functionchat:'+str(q['serial_num']),
                    'messages':[{'role':'user','content':q['content']}],'tools':[t['function'] for t in options['content']],
                    'expected':[r['function_name']],'was_needed_call':True,
                    'label_scope':'Matches benchmark named target only; not exhaustive alternative-tool validity and not official argument/call benchmark score.'})
    return result


def verify():
    p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen file changed: '+rel)
    return p


def prepare():
    if DATA.exists() or OUT.exists():raise FileExistsError('Existing experiment protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);rows=collect();keep=[];excluded=[];lengths={}
    for r in rows:
        names=[t['name'] for t in r['tools']]
        if len(set(names))!=len(names) or not set(r['expected'])<=set(names):raise ValueError('Invalid task')
        maxima={}
        for c in CONDITIONS:
            v=view(r,c);enc=tok([v['question']+' '+o for o in v['options'].values()],[v['context']]*len(v['options']),truncation=False)
            maxima[c]=max(map(len,enc['input_ids']))
        if max(maxima.values())>512:excluded.append({'id':r['id'],'tokens':maxima,'reason':'same paired exclusion for all4; no truncation'})
        else:keep.append(r);lengths[r['id']]=maxima
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for name,items in [('reference.jsonl',keep),('excluded.jsonl',excluded)]:
        (DATA/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in items),encoding='utf8')
    # Prespecified reversal sample, selected only by cohort/candidate count.
    selected=[]
    for cohort,n in [('v16',2),('functionchat',4),('functionchat',8)]:selected.extend(r['id'] for r in [x for x in keep if x['cohort']==cohort and len(x['tools'])==n][:4])
    paths=[DATA/'reference.jsonl',DATA/'excluded.jsonl',SOURCE,V16/'selector-scores.json',MODEL/'model.safetensors',MODEL/'config.json',
        SELECTOR/'adapter_model.safetensors',SELECTOR/'adapter_config.json']
    paths += [ROOT/p for p in ['scripts/selector_interface_data_v18.py','scripts/selector_interface_v18.py','tests/test_selector_interface_v18.py',
        'agent/local_choice_scorer_v1.py','scripts/heterogeneous_tool_checker_v1.py','scripts/build_tool_decision_mix_v1.py','scripts/tool_split_data_v1.py',
        'output/ツール選択に絞る次の比較-v17.txt']]
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'conditions':CONDITIONS,
        'n':len(keep),'excluded_n':len(excluded),'lengths':lengths,'reversal_ids':selected,
        'scope':'Reference diagnosis only, all V16 authored cases plus previously evaluated FunctionChat Singlecall4/8 candidate views. Single correct listed target; no no-match rejection, argument check/extraction, execution or agent memory. Base-model pretraining/exact train-name overlap not claimed absent.',
        'readout':'Current fixed NF4 selector, same prepare_model_for_kbit_training(false), FP16 autocast, per-case paired encoding. Raw scalar ranks, max over supplied TOOL candidates only; no_tool scored for V16 replay but ignored as before. No calibrated correctness probability. Full baseline must replay200 stored V16 raw tool scores <=.05 and report prediction changes before interpreting other variants.',
        'comparison':'2x2: existing vs capability-only Korean instruction; original full JSON vs semantic-preserving readable representation. Same utterances, tools and correct labels. Candidate order identical, paired exclusion if ANY view exceeds512, no truncation. Arguments and metadata preserved, not purpose-only omission.',
        'selection':'A non-baseline condition eligible only if V16 all-case correct strictly improves, V16 needed80 correct not lower, and FunctionChat total correct not lower than baseline. Choose by mean V16/FunctionChat accuracy, then needed-case accuracy; ties prefer current_readable,capability_full,capability_readable in that order. Reversal sample must not change selected tool. This is reference-only selection, not adoption. Fresh tool-level separated confirmation required.',
        'next':'If eligible, verify selected fixed interface vs baseline on unused tool definitions/utterances before adoption. If none eligible, do not keep editing input; move to one small selector-only learning comparison using purpose-specific positive/confusable-negative teachers and separate held-out tools. Do not train on these reference cases.',
        'stop':'Report all4 and unchanged/changed individual outcomes. No prompt/threshold rewrites or weight changes using this reference trial. No deployment.'})
    print('FROZEN',len(keep),'paired reference cases, excluded',len(excluded),'reversal sample',len(selected),flush=True)

if __name__=='__main__':prepare()
