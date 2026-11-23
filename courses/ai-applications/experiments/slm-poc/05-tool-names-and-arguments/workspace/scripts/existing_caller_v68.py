"""Reuse a pinned public3B caller; no additional training or new tool rules."""
import copy
import gc
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import train_korean_native_v67 as exp
from scripts import recovery_matrix_v67 as matrix
from scripts import recovery_matrix_runtime_v67_v2 as prior
from scripts.korean_material_v67 import sha,write,SEED,MODEL,REV
P=ROOT/'output/existing-caller-v68'
F_MODEL='Salesforce/xLAM-2-3b-fc-r'
F_REV='be83286f6a1a82c8bd4bfb751190271f58693f30'
POLICY=("Only perform actions authorized by the user's request. Respect the scope of each restriction: "
        "a ban on one action does not cancel a different action the user requested. "
        "If the user forbids all tool use, do not call any tool.")

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def prepare():
    prior.verify();rejected=read(matrix.OUT/'controls-rejected-before-final.json')
    assert not any(c['healthy'] for c in rejected['candidates'])
    assert not (matrix.OUT/'global-development-selection.json').exists()
    P.mkdir(exist_ok=False)
    paths=[Path(__file__),matrix.OUT/'controls-rejected-before-final.json',
           ROOT/'output/korean-native-v67/references/xlam3b-metadata.json',matrix.OUT/'plan.json',
           matrix.OUT/'runtime-amendment.json',matrix.OUT/'runtime-amendment-v2.json']
    write(P/'plan.json',{'model':F_MODEL,'revision':F_REV,'additional_training':0,
      'declared_parameters':3085938688,'compute':'Same NF4/FP16/native generation max256 as1B comparison; no external model-code execution.',
      'profiles':{'F-native':'3B native prompt / original executor',
                  'F-feedback':'Same3B native prompt / generic feedback executor',
                  'F-policy':'Same3B and feedback / native default retained plus the same generic authorization rule for every tool'},
      'policy':POLICY,'policy_scope':'No tool names, file kinds, modes or user-keyword dispatch. This is an instruction control, not a per-tool runtime rule.',
      'native_format':'If native defaults differ, replace only the1B default prefix in existing source-system messages with the3B native default; preserve source policy and all conversation content.',
      'selection':'Dev only across the previous5 arms plus these3. Original health/score key; ties fewer training examples. Final remains untouched until selected. Only a healthy candidate advances to final.',
      'interpretation':'Off-the-shelf model replacement and executor/prompt controls, not a causal proof of parameter count alone. Korean1B QLoRA results stay separate. No universal unknown-domain claim.',
      'if_no_healthy_candidate':'Retain untouched final set and report missing dev conditions; lower-LR1B recipe remains a possible next experiment, not automatically declared successful.',
      'files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
    print('V68 public caller profiles frozen before model outputs; final untouched.')

def verify():
    prior.verify();p=read(P/'plan.json')
    for name,h in p['files'].items():assert sha(ROOT/name)==h,name
    return p

def load(repo,rev):
    import torch
    from scripts import rollout_xlam_v60 as native_module
    old=(native_module.REPO,native_module.REV)
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    native_module.REPO=repo;native_module.REV=rev
    try:n=exp.create_model()
    finally:native_module.REPO,native_module.REV=old
    assert n.model.config._name_or_path==repo,n.model.config._name_or_path
    from peft import get_peft_model_state_dict
    assert all(torch.count_nonzero(v).item()==0 for k,v in get_peft_model_state_dict(n.model).items() if 'lora_B' in k)
    n.model.eval();return n

def defaults(tok):
    t=tok.apply_chat_template([{'role':'user','content':'probe'}],tools=[],tokenize=False)
    return t.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()

def generated(native,policy,cache=None):
    from transformers import AutoTokenizer
    small=AutoTokenizer.from_pretrained(MODEL,revision=REV,local_files_only=True)
    old=defaults(small);new=defaults(native.tokenizer);raw=native.generate
    # Callers pass a new object only once; preserve the actual native method.
    if hasattr(native,'v68_raw_generate'):raw=native.v68_raw_generate
    else:native.v68_raw_generate=raw
    def generate(messages,tools):
        ms=copy.deepcopy(messages);suffix=''
        if ms and ms[0]['role']=='system':
            system=ms.pop(0)['content']
            suffix=system[len(old):].strip() if system.startswith(old) else system
        ms=[{'role':'system','content':new+('\n\n'+POLICY if policy else '')+('\n\n'+suffix if suffix else '')}]+ms
        ids=native.tokenizer.apply_chat_template(ms,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')['input_ids']
        key=hashlib.sha256(ids.numpy().tobytes()).hexdigest()
        if cache is not None and key in cache:
            g=copy.deepcopy(cache[key]);g['exact_input_replay']=True;return g['text'],g
        text,g=raw(ms,tools)
        if cache is not None:cache[key]=copy.deepcopy(g)
        g['exact_input_replay']=False;return text,g
    return generate

def dev():
    verify()
    if (P/'started-dev.json').exists():raise FileExistsError('Protected F dev run')
    write(P/'started-dev.json',{'final_read':False});exp.RUN=P
    write(P/'retention-cases.json',read(matrix.AB/'retention-cases.json'))
    n=load(F_MODEL,F_REV)
    import torch
    write(P/'model-setup.json',{'model':n.model.config._name_or_path,'revision':F_REV,
         'config':n.model.config.to_dict(),'additional_training':0,'gpu':torch.cuda.get_device_name(),
         'default_system':defaults(n.tokenizer)})
    candidates=read(matrix.OUT/'controls-rejected-before-final.json')['candidates'];base=read(matrix.AB/'baseline/dev-summary.json')
    cache={};first_public=None;first_retention=None
    for label,recover,policy in [('F-native',False,False),('F-feedback',True,False),('F-policy',True,True)]:
        n.generate=generated(n,policy,cache)
        f=matrix.files(n,'dev',label,recover)
        if label!='F-feedback':
            pub=exp.public_eval(n,'dev',label);ret=exp.retention_eval(n,label)
            if label=='F-native':first_public=pub;first_retention=ret
        else:pub=first_public;ret=first_retention
        r={'files':f,'public':pub,'retention':ret};write(P/label/'dev-summary.json',r)
        healthy,score=exp.health_and_score(r,base)
        candidates.append({'label':label,'model':F_MODEL,'lr':0,'presentations':0,'healthy':healthy,'score':score,'dev':r})
        print('V68 DEV',label,json.dumps(r),flush=True)
    chosen=max(candidates,key=lambda r:(r['healthy'],r['score'],-r['presentations'],-r['lr']))
    write(P/'global-development-selection.json',{'selected':chosen,'candidates':candidates,'final_read':False})
    if not chosen['healthy']:
        write(P/'no-healthy-candidate.json',{'reason':'All eight fixed dev arms failed preservation/permission conditions. No final outcomes generated.','selected_for_diagnosis':chosen['label']})
    verify();print('V68 DEV SELECTION',chosen['label'],'healthy',chosen['healthy'],flush=True)

def final(baseline):
    verify();chosen=read(P/'global-development-selection.json')['selected'];assert chosen['healthy']
    assert chosen['label'].startswith('F-'),'Older five arms were rejected before F'
    label='baseline' if baseline else chosen['label'];dest='final-'+label
    if (P/dest/'started.json').exists():raise FileExistsError('Protected final arm')
    write(P/dest/'started.json',{'selection_sha256':sha(P/'global-development-selection.json')})
    exp.RUN=P;n=load(MODEL,REV) if baseline else load(F_MODEL,F_REV)
    # Baseline has its original1B prompt. F preserves its actual native default.
    n.generate=generated(n,label=='F-policy',None)
    recover=not baseline and label!='F-native'
    r={'files':matrix.files(n,'test',dest,recover),'public':exp.public_eval(n,'test',dest)}
    write(P/dest/'summary.json',r);verify();print('V68 FINAL ARM DONE',label,flush=True)

if __name__=='__main__':
    try:
        if '--prepare' in sys.argv:prepare()
        elif '--dev' in sys.argv:dev()
        elif '--final-baseline' in sys.argv:final(True)
        elif '--final-selected' in sys.argv:final(False)
        else:raise ValueError('Choose --prepare/--dev/--final-baseline/--final-selected')
    except Exception as e:
        import traceback
        if P.exists() and not (P/'failure.json').exists():write(P/'failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
        raise
