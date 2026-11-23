"""Precommitted no-training JSON-protocol control, reusing a published prompt.

Do not inspect A/B test results before locking the global dev-only selection.
Never import or execute the downloaded external Python files.
"""
import copy
import gc
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import train_korean_native_v67 as experiment
from scripts.korean_material_v67 import write,sha,SEED

AB=ROOT/'output/korean-native-v67/experiment'
OUT=ROOT/'output/korean-native-v67/protocol-control'
PROMPT=ROOT/'output/korean-native-v67/references/zihaowu25-configs_prompt_tooluse.txt'

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def rewrite(messages,prompt,default):
    result=copy.deepcopy(messages)
    if result and result[0]['role']=='system':
        original=result.pop(0)['content']
        # Only remove the native format/default instruction, not source policy.
        source=original[len(default):].strip() if original.startswith(default) else original
    else:source=''
    return [{'role':'system','content':prompt+('\n\n'+source if source else '')}]+result

def prepare():
    # These pure assertions check preservation, not an implementation-mirroring
    # model test. All real inputs/tool definitions remain unchanged.
    history=[{'role':'system','content':'NATIVE\n\nSource instructions:\nPOLICY'},
             {'role':'user','content':'REQUEST'},
             {'role':'tool','name':'read','content':'RESULT'}]
    changed=rewrite(history,'PUBLISHED','NATIVE')
    assert changed[1:]==history[1:] and history[0]['content'].startswith('NATIVE')
    assert 'POLICY' in changed[0]['content'] and 'NATIVE' not in changed[0]['content']
    assert rewrite(history[1:],'PUBLISHED','NATIVE')[1:]==history[1:]
    OUT.mkdir(exist_ok=False)
    plan={'arm':'C-published-json-protocol','additional_training_updates':0,'presentations':0,
      'source':'https://github.com/zihaowu25/Function-Calling-SFT-for-Small-LLMs/blob/caa9fbe2ed598c8cfa5396e348cd4ddd1db8fb29/configs/prompt_tooluse.txt',
      'prompt_reused_verbatim':True,'external_code_executed':False,
      'change':'Replace the native default system/format instruction with the downloaded published JSON-only tool-decision prompt. Preserve any additional source policy, all user/assistant/tool history and tool definitions.',
      'scope':'Practical prompt control, not a source-project replication or proof that JSON wording alone caused any difference. No per-tool keyword selection logic.',
      'timing':'Declared after A-1000 development results but before any A/B final-test results are read. Frozen A/B training schedule and exclusive A/B selection are unchanged.',
      'global_selection':'After A/B finishes, evaluate C on development only. Compare C plus all original A/B development candidates using the original healthy/score key, preferring fewer training examples on a tie. Lock selection before reading any A/B test files. If C is selected, evaluate C on final test once. Otherwise never evaluate C on final test.',
      'adoption':'Selected candidate must also be healthy on dev, and pass the original final gate. A/B exclusive test results are auxiliary if C wins global selection; never use them to select C.',
      'baseline_plan_sha256':sha(AB/'plan.json'),
      'files':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),PROMPT,AB/'plan.json',AB/'baseline/dev-summary.json']}}
    write(OUT/'plan.json',plan)
    print('V67 C protocol-only comparison frozen; no model run or test outputs read.')

def verify():
    p=read(OUT/'plan.json')
    for name,h in p['files'].items():assert sha(ROOT/name)==h,name
    return p

def main():
    if '--prepare' in sys.argv:return prepare()
    verify()
    # Parent process must have completed. Never load its test metrics here.
    assert (AB/'summary.json').exists(),'Finish the protected A/B run first'
    if (OUT/'started.json').exists():raise FileExistsError('Protected C run already started')
    import torch
    assert torch.cuda.mem_get_info()[0]>5*2**30,'Wait for the A/B model process to release GPU memory'
    write(OUT/'started.json',{'test_results_read':False})
    write(OUT/'retention-cases.json',read(AB/'retention-cases.json'))
    experiment.RUN=OUT
    random.seed(SEED);torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED)
    native=experiment.create_model()
    rendered=native.tokenizer.apply_chat_template([{'role':'user','content':'probe'}],tools=[],tokenize=False)
    default=rendered.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0].strip()
    generate=native.generate;prompt=PROMPT.read_text(encoding='utf-8').strip()
    def controlled(messages,tools):return generate(rewrite(messages,prompt,default),tools)
    native.generate=controlled;native.model.eval()
    dev={'files':experiment.file_eval(native,'dev','C'),'public':experiment.public_eval(native,'dev','C'),
         'retention':experiment.retention_eval(native,'C')}
    write(OUT/'C/dev-summary.json',dev)
    base=read(AB/'baseline/dev-summary.json');healthy,score=experiment.health_and_score(dev,base)
    c={'label':'C','trial':'C','lr':0,'presentations':0,'healthy':healthy,'score':score,'dev':dev}
    original=read(AB/'development-selection.json')['all_candidates']
    chosen=max(original+[c],key=lambda r:(r['healthy'],r['score'],-r['presentations'],-r['lr']))
    write(OUT/'global-development-selection.json',{'selected':chosen,'all_candidates':original+[c],
          'A_B_test_read_before_selection':False,'C_test_read_before_selection':False})
    print('V67 GLOBAL DEV LOCKED',chosen['label'],'C healthy',healthy,'C score',score,flush=True)
    # Only now is test output allowed to enter the combined report.
    original_test=read(AB/'summary.json');baseline=original_test['test']['baseline']
    if chosen['label']=='C':
        after={'files':experiment.file_eval(native,'test','C'),'public':experiment.public_eval(native,'test','C')}
    else:after=original_test['test'][chosen['label']]
    b,a=baseline['files'],after['files'];bp,ap=baseline['public'],after['public']
    lost=sorted(set(b['passed_ids'])-set(a['passed_ids']));gained=sorted(set(a['passed_ids'])-set(b['passed_ids']))
    adopted=(chosen['healthy'] and a['goal_and_stop']>=b['goal_and_stop']+5 and not lost
      and not a['unwanted_writes'] and not a['wrong_mode_writes']
      and a['required_correct_write']>=b['required_correct_write'] and a['no_call_correct']>=b['no_call_correct']
      and ap['call_name_correct']>=bp['call_name_correct'] and ap['call_accepted_correct']>=bp['call_accepted_correct']
      and ap['no_call_correct']>=bp['no_call_correct'])
    verify();write(OUT/'summary.json',{'selected':chosen['label'],'healthy_on_dev':chosen['healthy'],
      'baseline':baseline,'after':after,'gained':gained,'lost':lost,'adoptable_research_candidate':adopted,
      'production_changed':False,'A_B_only_result':original_test,
      'scope':'Protocol prompt chosen using dev only. Same pinned NF4 base and real-file/API comparison. No inference-code repair or per-tool decision branches. Not an independent human-gold or universal unknown-domain guarantee.'})
    print('V67 C COMPLETE',chosen['label'],'adoptable',adopted,flush=True)

if __name__=='__main__':main()
