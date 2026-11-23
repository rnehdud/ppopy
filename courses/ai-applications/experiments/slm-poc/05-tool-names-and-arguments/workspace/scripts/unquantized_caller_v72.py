"""Same pinned xLAM/native inputs without NF4 weight compression; no training."""
import copy
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import train_korean_native_v67 as exp
from scripts import recovery_matrix_v67 as matrix
from scripts.resume_existing_caller_v68 import summarize
from scripts.korean_material_v67 import write,sha,MODEL,REV,SEED
P=ROOT/'output/unquantized-caller-v72'
DATA=exp.DATA


def read(p):return json.loads(p.read_text(encoding='utf-8'))


def prepare():
    from scripts.aligned_decision_v69 import verify as old_verify
    old_verify();assert not P.exists(),'Protected new control'
    P.mkdir();write(P/'retention-cases.json',read(matrix.AB/'retention-cases.json'))
    paths=[Path(__file__),ROOT/'scripts/train_korean_native_v67.py',ROOT/'agent/retail_attention_v65.py',
        ROOT/'agent/korean_files_v67.py',ROOT/'agent/recovery_loop_v67.py',P/'retention-cases.json',
        matrix.AB/'baseline/dev-summary.json',matrix.AB/'baseline/dev-public.json',matrix.AB/'baseline/dev-files.json',matrix.AB/'baseline/english-retention.json']
    paths += [DATA/n for n in ['public-dev.json','public-test.json','file-cases.json','file-tools.json']]
    write(P/'plan.json',{'model':MODEL,'revision':REV,'additional_training':0,
        'reason':'V67/V69 tested NF4 weight loading. Same native model in uncompressed FP16 has not been evaluated. Check this before assuming more data or longer context is required.',
        'precision':'Base linear weights FP16, RMSNorm weights FP32, zero-B LoRA r8 alpha16 as previous untrained control; same FP16 compute/autocast, native tokenizer, cuDNN-long/math-short attention and256-token greedy generation. Main changed weight representation is NF4 versus FP16.',
        'profiles':{'P-native':'Uncompressed original model, native prompt, original executor','P-feedback':'Same weights/prompt, existing generic result/error feedback executor'},
        'resources':'Do not start while V69 Python worker is live. No CPU FP32 model alongside training: observed available RAM only6.7GiB. Use free GPU after training exits.',
        'selection':'Same original dev health/score across these2 profiles; public first-choice/English shared because inputs/weights identical. Real file operations re-executed. No final if both fail.',
        'final':'Only healthy selected profile: original NF4 native baseline vs FP16 selected profile on original reserved48 file cases/72 public examples, once. Same original final adoption gate. No inference results from final used to choose profiles.',
        'limits':'A practical precision/control comparison, not proof every output difference has a unique cause. Not a QLoRA improvement, not deployment or universal unseen-domain guarantee.',
        'files':{str(x.relative_to(ROOT)):sha(x) for x in paths}})
    print('V72 uncompressed native control frozen before outputs.')


def verify():
    p=read(P/'plan.json')
    for name,h in p['files'].items():assert sha(ROOT/name)==h,name
    return p


def ensure_no_training():
    command="Get-CimInstance Win32_Process -Filter \"name = 'python.exe'\" | Where-Object { $_.CommandLine -match 'scripts[\\/]aligned_decision_v69\\.py' } | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
    output=subprocess.check_output(['powershell.exe','-NoProfile','-Command',command],
        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),text=True).strip()
    if output:raise RuntimeError('V69 worker still live; do not allocate another GPU model: '+output)


class Native:
    def __init__(self):
        import torch
        from transformers import AutoModelForCausalLM,AutoTokenizer
        from transformers.models.qwen2.modeling_qwen2 import Qwen2RMSNorm
        from peft import LoraConfig,TaskType,get_peft_model,get_peft_model_state_dict
        from agent.retail_attention_v65 import install
        torch.set_num_threads(4);self.torch=torch
        self.tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REV,local_files_only=True,trust_remote_code=False)
        self.model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REV,local_files_only=True,trust_remote_code=False,
            torch_dtype=torch.float16,device_map={'':0},attn_implementation='sdpa')
        self.model.set_attn_implementation(install())
        assert not getattr(self.model,'is_loaded_in_4bit',False)
        for module in self.model.modules():
            if isinstance(module,Qwen2RMSNorm):module.float()
        self.model.requires_grad_(False)
        self.model=get_peft_model(self.model,LoraConfig(task_type=TaskType.CAUSAL_LM,r=8,lora_alpha=16,lora_dropout=.05,target_modules='all-linear',bias='none'))
        assert all(torch.count_nonzero(v).item()==0 for k,v in get_peft_model_state_dict(self.model).items() if 'lora_B' in k)
        self.model.eval()

    def generate(self,messages,tools):
        torch=self.torch
        b=self.tokenizer.apply_chat_template(messages,tools=tools,add_generation_prompt=True,return_dict=True,return_tensors='pt')
        n=b['input_ids'].shape[1]
        if n+256>self.model.config.max_position_embeddings:raise ValueError('Context overflow; no truncation')
        key=hashlib.sha256(b['input_ids'].numpy().tobytes()).hexdigest()
        b={k:v.to('cuda') for k,v in b.items()};started=time.perf_counter()
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.float16):
            out=self.model.generate(**b,max_new_tokens=256,do_sample=False,use_cache=True,pad_token_id=self.tokenizer.eos_token_id)
        ids=out[0,n:];text=self.tokenizer.decode(ids,skip_special_tokens=True)
        return text,{'text':text,'finished':bool(len(ids)) and int(ids[-1])==self.tokenizer.eos_token_id,
            'input_tokens':int(n),'output_tokens':len(ids),'seconds':time.perf_counter()-started,
            'messages':copy.deepcopy(messages),'tools':copy.deepcopy(tools),'input_ids_sha256':key}


def files(n,split,label,recover):
    matrix.engine(recover);exp.file_eval(n,split,label)
    return summarize(read(P/label/(split+'-files.json')))


def check_inputs(n):
    original=read(matrix.AB/'baseline/dev-public.json')+read(matrix.AB/'baseline/english-retention.json')
    original += [c['turns'][0]['trace']['generations'][0] for c in read(matrix.AB/'baseline/dev-files.json')]
    gs=[r.get('generation',r) for r in original]
    for g in gs:
        b=n.tokenizer.apply_chat_template(g['messages'],tools=g['tools'],add_generation_prompt=True,return_dict=True,return_tensors='pt')
        assert hashlib.sha256(b['input_ids'].numpy().tobytes()).hexdigest()==g['input_ids_sha256']
    write(P/'input-equivalence.json',{'token_inputs_checked':len(gs),'all_match_original_NF4_inputs':True})


def dev():
    verify();ensure_no_training();assert not (P/'started-dev.json').exists(),'Protected dev control'
    write(P/'started-dev.json',{'final_read':False});exp.RUN=P
    import torch
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    assert torch.cuda.mem_get_info()[0]>4*2**30,'Not enough free GPU memory for this control'
    n=Native();check_inputs(n)
    write(P/'model-setup.json',{'model':n.model.config._name_or_path,'revision':REV,'quantized':False,'additional_training':0,
        'gpu':torch.cuda.get_device_name(),'allocated_GiB':torch.cuda.memory_allocated()/2**30,
        'norm_dtype':str(n.model.base_model.model.model.norm.weight.dtype)})
    base=read(matrix.AB/'baseline/dev-summary.json');candidates=[];pub=ret=None
    for label,recover in [('P-native',False),('P-feedback',True)]:
        f=files(n,'dev',label,recover)
        if not recover:pub=exp.public_eval(n,'dev',label);ret=exp.retention_eval(n,label)
        r={'files':f,'public':pub,'retention':ret};write(P/label/'dev-summary.json',r)
        healthy,score=exp.health_and_score(r,base)
        candidates.append({'label':label,'healthy':healthy,'score':score,'dev':r,'presentations':0})
        print('V72 DEV',label,json.dumps(r),flush=True)
    chosen=max(candidates,key=lambda c:(c['healthy'],c['score']))
    write(P/'development-selection.json',{'selected':chosen,'candidates':candidates,'final_read':False})
    if not chosen['healthy']:write(P/'no-healthy-candidate.json',{'reason':'Both precision controls fail original dev preservation conditions. Final not run.'})
    verify();print('V72 DEV DONE',chosen['label'],'healthy',chosen['healthy'],flush=True)


def final(baseline):
    verify();ensure_no_training();chosen=read(P/'development-selection.json')['selected'];assert chosen['healthy']
    label='baseline' if baseline else chosen['label'];dest='final-'+label
    assert not (P/dest/'started.json').exists(),'Protected final arm'
    write(P/dest/'started.json',{'selection_sha256':sha(P/'development-selection.json')});exp.RUN=P
    import torch
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    n=exp.create_model() if baseline else Native()
    r={'files':files(n,'test',dest,not baseline and label=='P-feedback'),'public':exp.public_eval(n,'test',dest)}
    write(P/dest/'summary.json',r);verify();print('V72 FINAL DONE',label,flush=True)


if __name__=='__main__':
    try:
        if '--prepare' in sys.argv:prepare()
        elif '--final-baseline' in sys.argv:final(True)
        elif '--final-selected' in sys.argv:final(False)
        else:dev()
    except Exception as e:
        import traceback
        if P.exists() and not (P/'failure.json').exists():write(P/'failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
        raise
