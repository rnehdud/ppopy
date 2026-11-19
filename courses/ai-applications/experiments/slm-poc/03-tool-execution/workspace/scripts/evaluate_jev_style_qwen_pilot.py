"""Local Jev-style option-logit pilot using *existing Qwen*, not the OpenJev weights."""
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from transformers import AutoTokenizer
from agent.symptom_state_v1 import SymptomSession,SYMPTOMS
import scripts.evaluate_symptom_state_v1 as existing

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/jev-style-qwen-pilot-v1'
NAMES={'dryness':'건조함','breakout':'여드름이나 뾰루지','redness':'붉어짐','stinging':'따가움','itching':'가려움'}
DESCRIPTIONS={
 'present':'사용자 본인에게 이 증상이 현재 있다고 말했다.',
 'absent':'사용자 본인에게 이 증상이 현재 없다고 명확히 말했다.',
 'unchanged':'이 발화에는 사용자 본인의 이 증상 상태를 바꿀 정보가 없다. 일반론, 다른 사람, 가정도 여기에 포함한다.',
 'unknown':'사용자가 본인의 이 증상 여부를 모른다고 직접 정정하거나 말했다.'}
ORDERS={'forward':['present','absent','unchanged','unknown'],
        'reverse':['unknown','unchanged','absent','present']}
LETTERS='ABCD'
SYSTEM='''피부 증상 상태를 기록하기 위한 선택 문제다. 사용자 본인의 현재 발화에 근거해 이 증상 하나에 대한 판단을 고른다.
명시되지 않은 내용은 추측하지 않는다. 다른 사람이나 가상의 증상을 사용자의 상태로 기록하지 않는다.
이전 상태를 확인하되, 이번 발화에 없는 증상은 변경하지 않는다. 정확히 한 개의 선택지만 고르고 해당 영문 대문자 한 글자로 답한다.'''

def completion(prompt,n_probs):
    payload={'prompt':prompt,'n_predict':1,'temperature':-1,'n_probs':n_probs,'cache_prompt':False}
    req=urllib.request.Request('http://127.0.0.1:18081/completion',data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),
                               headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=180) as response:return json.load(response)

def choose(tokenizer,ids,field,state,text,order):
    options=ORDERS[order]
    question=('대상 증상: '+NAMES[field]+'\n현재 상태: '+json.dumps(state,ensure_ascii=False)+
       '\n이번 사용자 발화: '+text+'\n선택지:\n'+
       '\n'.join(LETTERS[i]+'. '+DESCRIPTIONS[option] for i,option in enumerate(options))+'\n정답 대문자:')
    prompt=tokenizer.apply_chat_template([{'role':'system','content':SYSTEM},{'role':'user','content':question}],
                                        tokenize=False,add_generation_prompt=True)
    started=time.perf_counter();top=None
    for count in [512,2048,8192]:
        out=completion(prompt,count)
        probs=out.get('completion_probabilities') or []
        if len(probs)!=1:raise ValueError('Missing native next-token probabilities')
        top=probs[0].get('top_logprobs') or []
        raw={x['id']:x['logprob'] for x in top}
        if all(i in raw for i in ids):break
    if not all(i in raw for i in ids):raise ValueError('At least one option score missing; no classification')
    scores=[float(raw[i]) for i in ids];best=max(range(4),key=lambda i:scores[i])
    # These are relative option scores, not calibrated probabilities of correctness.
    shifted=[math.exp(x-max(scores)) for x in scores];relative=[x/sum(shifted) for x in shifted]
    return {'decision':options[best],'option_letters':dict(zip(LETTERS,options)),
       'option_logprobs':dict(zip(LETTERS,scores)),'relative_scores_uncalibrated':dict(zip(LETTERS,relative)),
       'native_generated_token_ignored':out.get('content'),'top_n_requested':count,
       'prompt_sha256':hashlib.sha256(prompt.encode('utf-8')).hexdigest(),
       'seconds':time.perf_counter()-started}

def main():
    cfg=json.loads((ROOT/'output/runtime-qwen3/server_config.json').read_text(encoding='utf-8-sig'))
    if cfg.get('adapter') or cfg.get('port')!=18081:raise ValueError('Expected local unadapted Qwen3')
    with urllib.request.urlopen('http://127.0.0.1:18081/lora-adapters',timeout=10) as f:active=json.load(f)
    if isinstance(active,dict):active=active.get('data',active.get('value',[]))
    if any(float(x.get('scale',0))!=0 for x in active):raise ValueError('Unexpected active adapter')
    if OUT.exists():raise FileExistsError('Previous pilot is protected')
    tokenizer=AutoTokenizer.from_pretrained(str(ROOT/'models/qwen3-4b-instruct-2507/tokenizer'),local_files_only=True)
    tokens=[tokenizer.encode(x,add_special_tokens=False) for x in LETTERS]
    if any(len(x)!=1 for x in tokens) or len({x[0] for x in tokens})!=4:raise ValueError('Choices are not distinct single tokens')
    ids=[x[0] for x in tokens]
    OUT.mkdir(parents=True)
    out={}
    for order in ORDERS:
        cases=[]
        for case in existing.CASES:
            session=SymptomSession();turns=[]
            for text,expected in case['turns']:
                before=session.state;start=time.perf_counter()
                choices={field:choose(tokenizer,ids,field,before,text,order) for field in SYMPTOMS}
                patch={field:r['decision'] for field,r in choices.items() if r['decision']!='unchanged'}
                result=session.update(patch) if patch else None
                turns.append({'input':text,'before':before,'expected':expected,'choices':choices,'patch':patch,
                  'tool_executed':bool(result),'after':session.state,'state_matches':session.state==expected,
                  'seconds':time.perf_counter()-start})
            cases.append({'id':case['id'],'turns':turns,'passes':all(t['state_matches'] for t in turns)})
            print(order,case['id'],[t['state_matches'] for t in turns],flush=True)
        out[order]=cases
    original=json.loads((ROOT/'output/symptom-state-v1/results.json').read_text(encoding='utf-8'))
    metrics={}
    for order,cases in out.items():
        ts=[t for c in cases for t in c['turns']]
        metrics[order]={'scenarios':len(cases),'scenario_passes':sum(c['passes'] for c in cases),
          'turns':len(ts),'turn_matches':sum(t['state_matches'] for t in ts),
          'mean_seconds_per_turn':sum(t['seconds'] for t in ts)/len(ts)}
    # First turns have identical empty prior state in both orderings.
    f={c['id']:c for c in out['forward']};r={c['id']:c for c in out['reverse']}
    sensitivity=[{'id':k,'field':field,'forward':f[k]['turns'][0]['choices'][field]['decision'],
                  'reverse':r[k]['turns'][0]['choices'][field]['decision']}
                 for k in f for field in SYMPTOMS
                 if f[k]['turns'][0]['choices'][field]['decision']!=r[k]['turns'][0]['choices'][field]['decision']]
    report={'model':'Qwen3-4B-Instruct-2507 Q4_K_M; local llama.cpp; no adapter or training',
      'method':'Per symptom, raw next-token option logprobs, no JSON content generated. Backend generates one unused token; application executes update.',
      'not_openjev':'Uses existing Qwen weights. It is not the openjev/openjev model or its calibrated helper.',
      'warning':'Six previously observed synthetic development scenarios; labels not independently human reviewed; single run; not general accuracy.',
      'token_ids':dict(zip(LETTERS,ids)),'server':cfg,'option_scores':'uncalibrated relative preference, not accuracy/confidence',
      'previous_native_tool_baseline':{'scenarios':len(original['cases']),'scenario_passes':sum(c['passes'] for c in original['cases']),
           'turns':sum(len(c['turns']) for c in original['cases']),
           'turn_matches':sum(t['matches'] for c in original['cases'] for t in c['turns'])},
      'pilot_metrics':metrics,'first_turn_option_order_disagreements':sensitivity,'results':out}
    (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'baseline':report['previous_native_tool_baseline'],'pilot':metrics,
      'first_turn_order_disagreement_count':len(sensitivity)},ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':main()
