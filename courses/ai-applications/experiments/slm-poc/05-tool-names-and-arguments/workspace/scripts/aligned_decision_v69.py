"""Align one decision-only output contract across preprocessing and inference.

Reuses the pinned V67 material, native tokenizer, PEFT trainer and actual tools.
Only the system output contract changes; no tool/task/keyword-specific routing.
"""
import copy
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import train_korean_native_v67 as exp
from scripts.korean_material_v67 import write,sha,MODEL,REV,SEED
from scripts.retail_data_v65 import encode_example
OLD=exp.DATA
P=ROOT/'output/aligned-decision-v69'
DATA=P/'material'
CONTRACT='''You are a tool-decision model. Select the next action from the supplied tools, conversation and actual tool results.
Output only a JSON array: [{"name": "tool_name", "arguments": {"argument_name": "value"}}].
Output [] when no call is appropriate now: information or confirmation is missing, no supplied tool fits, no tool is needed, or the requested work is complete. Do not invent missing argument values. Do not output explanations, questions or answers. Source instructions still govern allowed actions, but instructions to speak or ask a question mean [] in this decision-only output. Use actual tool results before choosing subsequent calls. The available tools are:'''


def read(p):return json.loads(p.read_text(encoding='utf-8'))


def native_default(tok):
    s=tok.apply_chat_template([{'role':'user','content':'probe'}],tools=[],tokenize=False)
    return s.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()


def messages_for(messages,default):
    result=copy.deepcopy(messages)
    if result and result[0]['role']=='system':
        text=result[0]['content']
        if text.startswith(CONTRACT):return result
        if not text.startswith(default):raise ValueError('Unrecognized system prefix; do not discard source policy')
        result[0]['content']=CONTRACT+text[len(default):]
    else:result.insert(0,{'role':'system','content':CONTRACT})
    return result


def prepare():
    from transformers import AutoTokenizer
    from scripts.resume_existing_caller_v68 import verify as prior_verify
    prior_verify();assert not P.exists(),'Protected new experiment'
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REV,local_files_only=True)
    default=native_default(tok);P.mkdir();DATA.mkdir();stats={}
    for name in ['train','source-dev']:
        source=read(OLD/(name+'.json'));output=[];lengths=[]
        for r in source:
            a=copy.deepcopy(r);a['messages']=messages_for(r['messages'],default)
            ids,start=encode_example(tok,a['messages'],a['target'],a['tools'])
            assert len(ids)<=4096 and len(ids)-start<=256,(a['id'],len(ids))
            assert a['messages'][1:]==r['messages'][1:]
            assert a['messages'][0]['content'][len(CONTRACT):]==r['messages'][0]['content'][len(default):]
            assert a['target']==r['target'] and a['tools']==r['tools']
            a.update(input_ids=ids,target_start=start,tokens=len(ids));lengths.append(len(ids));output.append(a)
        assert [r['id'] for r in output]==[r['id'] for r in source]
        write(DATA/(name+'.json'),output)
        stats[name]={'n':len(output),'max_tokens':max(lengths),'mean_tokens':sum(lengths)/len(lengths),'truncated':0,'targets_or_order_changed':0}
    # Keep evaluator inputs exactly as V67. The same messages_for function
    # changes their system prefix at inference, including file-turn histories.
    for name in ['public-dev.json','public-test.json','file-cases.json','file-tools.json']:
        (DATA/name).write_bytes((OLD/name).read_bytes())
    write(P/'retention-cases.json',read(exp.RUN/'retention-cases.json'))
    source_paths=[OLD/n for n in ['train.json','source-dev.json','public-dev.json','public-test.json','file-cases.json','file-tools.json']]
    source_paths += [ROOT/'scripts/train_korean_native_v67.py',ROOT/'scripts/retail_data_v65.py',ROOT/'agent/korean_files_v67.py',
        ROOT/'output/existing-caller-v68/summary.json',ROOT/'output/existing-caller-v68/instruction-format-audit.json',Path(__file__)]
    material=list(DATA.glob('*.json'))+[P/'retention-cases.json']
    write(P/'plan.json',{'model':MODEL,'revision':REV,'seed':SEED,'contract':CONTRACT,'material':stats,
        'change':'One generic output contract, identically used in training and inference. No new data, relabeling, tool-name dispatch or keyword gates.',
        'reference':'Existing pinned Transformers native template, PEFT quantization and V67 assistant-target loss; no new model implementation. https://huggingface.co/docs/peft/developer_guides/quantization ; https://huggingface.co/docs/trl/sft_trainer',
        'arms':{'aligned-base':'Fresh zero-adapter1B with aligned contract; isolates instruction-only effect',
            'old-A3000-aligned':'Previously saved A3000 weights with aligned contract; diagnostic, zero new updates',
            'aligned-1000':'Fresh zero-adapter1B trained on same first1000 under aligned contract',
            'aligned-3000':'Same fresh aligned run continued through same3000, one pass'},
        'training':'Identical V67 A recipe: NF4/FP16, LoRA all-linear r8 alpha16 dropout0.05, LR3e-5, accumulation2, checkpoints every500 examples; evaluate at1000/3000. Do not train from failed old A weights.',
        'comparison':'Retain original native baseline as primary preservation reference. Also compare new training to aligned-base to separate learning from prompt-only effects. Existing V67 strict parser, native executor and goal grader unchanged. Actual results/errors only; no gold-driven selection.',
        'selection':'Original development health and score, same gates, among four fixed arms. A candidate must preserve original baseline and have no forbidden/wrong-mode saves; preserve aligned-base metrics as well for a training-effect claim. Select before any final outcomes.',
        'final':'Only if an arm passes the original health gate, evaluate once: exact original native baseline vs selected aligned arm on reserved48 file episodes and72 public examples. Original final adoption gate (+5 completions, no lost successes, zero unwanted/wrong-mode writes, names/args/no-call/saves not lower). Otherwise final remains unused.',
        'limits':'Fixing an observed instruction mismatch is not proof that it caused V67 failure. No universal unknown-domain80-90% claim. Whole project remains incomplete until real goal conditions are verified. No demo/production change.',
        'frozen_files':{str(p.relative_to(ROOT)):sha(p) for p in source_paths+material}})
    print('V69 prepared',json.dumps(stats),flush=True)


def verify():
    p=read(P/'plan.json')
    for name,h in p['frozen_files'].items():assert sha(ROOT/name)==h,name
    return p


def install_contract(native):
    default=native_default(native.tokenizer);raw=native.generate
    def generate(messages,tools):return raw(messages_for(messages,default),tools)
    native.generate=generate


def evaluate(native,label,base):
    r=exp.evaluate_dev(native,label);healthy,score=exp.health_and_score(r,base)
    c={'label':label,'lr':0,'presentations':0,'healthy':healthy,'score':score,'dev':r}
    write(P/label/'candidate.json',c);return c


def main():
    verify();assert not (P/'started.json').exists(),'Protected run; inspect actual process and checkpoints before any restart'
    write(P/'started.json',{'plan_sha256':sha(P/'plan.json'),'final_read':False})
    import torch
    from peft import get_peft_model_state_dict,set_peft_model_state_dict
    from safetensors.torch import load_file
    exp.DATA=DATA;exp.RUN=P;exp.verify=verify
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    n=exp.create_model();initial={k:v.detach().cpu().clone() for k,v in get_peft_model_state_dict(n.model).items()}
    assert all(torch.count_nonzero(v).item()==0 for k,v in initial.items() if 'lora_B' in k)
    install_contract(n);base=read(ROOT/'output/korean-native-v67/experiment/baseline/dev-summary.json')
    write(P/'model-setup.json',{'model':MODEL,'revision':REV,'gpu':torch.cuda.get_device_name(),
         'trainable_parameters':sum(p.numel() for p in n.model.parameters() if p.requires_grad),
         'torch':torch.__version__,'quantization':'NF4 double /FP16 compute','training_from':'Fresh original zero adapter'})
    candidates=[evaluate(n,'aligned-base',base)]
    old=load_file(str(ROOT/'output/korean-native-v67/experiment/checkpoints/A-3000/adapter_model.safetensors'))
    set_peft_model_state_dict(n.model,old);n.model.eval()
    candidates.append(evaluate(n,'old-A3000-aligned',base));del old
    set_peft_model_state_dict(n.model,initial);n.model.eval()
    # Same fixed seed for the actual training/dropout as the old recipe.
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    rng=(torch.random.get_rng_state(),torch.cuda.get_rng_state_all())
    candidates+=exp.train_trial(n,'aligned',3e-5,read(DATA/'train.json'),initial,base,rng)
    chosen=max(candidates,key=lambda c:(c['healthy'],c['score'],-c['presentations'],-c['lr']))
    write(P/'development-selection.json',{'selected':chosen,'candidates':candidates,'final_read':False})
    verify()
    if not chosen['healthy']:
        write(P/'no-healthy-candidate.json',{'reason':'All four fixed development arms fail original preservation/adoption conditions. Final not run.','best_for_diagnosis':chosen['label']})
        print('V69 DEV COMPLETE: no healthy candidate; final untouched',flush=True);return
    # Final is a new worker phase, so selection and saved weights are inspected
    # before loading either final arm. Never automatically deploy.
    print('V69 DEV COMPLETE: healthy candidate',chosen['label'],'ready for frozen final comparison',flush=True)


if __name__=='__main__':
    try:
        if '--prepare' in sys.argv:prepare()
        else:main()
    except Exception as e:
        import traceback
        if P.exists() and not (P/'failure.json').exists():write(P/'failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
        raise
