"""Log four option scores and examine error vs margin; no model training.

Both the old observed development cases and newly authored adversarial probes
are exploratory, not human-reviewed or a representative calibration dataset.
All examples are synthetic. No threshold is deployed to the stateful agent.
"""
import csv,hashlib,json,math,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import SYMPTOMS,SymptomSession,empty_state
from scripts.compare_korean_decision_pilot import QUESTION,OPTIONS,CHECKSUMS
from scripts.evaluate_jev_style_qwen_pilot import NAMES,DESCRIPTIONS
from scripts.train_ko_symptom_6000_v1 import MODEL,DATA,OUT as PRIOR

DEST=ROOT/'output/symptom-score-margins-v1'
ADAPTER=ROOT/'adapters/ko-symptom-6000-v1/step-1500'
CHALLENGE=[
 [('もし顔が乾燥したらどうしたらいいですか？',{})],
 [('仮に赤みが出た場合は相談できますか？',{})],
 [('肌がかゆくなる可能性はありますか？',{})],
 [('製品で顔がヒリヒリすることってありますか？',{})],
 [('私は今かゆくて困っています。',{'itching':'present'})],
 [('顔が赤くなっているので、どうすればいい？',{'redness':'present'})],
 [('以前は乾燥していたけど今は乾燥していません。',{'dryness':'absent'})],
 [('前はニキビがなかったけど、今はできています。',{'breakout':'present'})],
 [('妹は頬が赤いけど私は赤くありません。',{'redness':'absent'})],
 [('友人が肌がかゆいと言ってました。',{})],
 [('肌がかゆいかどうか、はっきりしません。',{'itching':'unknown'})],
 [('乾燥していないわけではありません。',{'dryness':'present'})],
 [('赤いし、乾燥しています。',{'redness':'present','dryness':'present'})],
 [('私は顔が赤く、でもかゆみはありません。',{'redness':'present','itching':'absent'})],
 [('あいさつをしにきました。',{})],
 [('今、頬がかゆいです。',{'itching':'present'}),('もしニキビが出た場合はどうしたらいい？',{}),('かゆみが治まりました。',{'itching':'absent'})],
 [('顔が乾燥しています。',{'dryness':'present'}),('赤みが出るのか心配です。',{}),('乾燥は変わっていません。',{'dryness':'present'})],
 [('頬が赤いです。',{'redness':'present'}),('さっきの赤みがあるという話は間違いです。今は赤くないです。',{'redness':'absent'})],
]

def authored_cases():
    cases=[]
    for i,turns in enumerate(CHALLENGE,1):
        expected=empty_state();steps=[]
        for text,patch in turns:
            expected={**expected,**patch}
            steps.append({'input':text,'expected':dict(expected),'gold_patch':patch})
        cases.append({'id':f'challenge-{i:02}','turns':steps})
    return cases

def summarize(records):
    n=len(records);bad=[r for r in records if not r['state_correct']];good=[r for r in records if r['state_correct']]
    def desc(rs):
        vals=[r['gap'] for r in rs]
        return {'count':len(vals),'median_gap':statistics.median(vals) if vals else None,
                'min_gap':min(vals) if vals else None,'max_gap':max(vals) if vals else None,
                'mean_gap':statistics.mean(vals) if vals else None}
    curve=[]
    for threshold in [0,0.05,0.10,0.20,0.30,0.50,0.75,0.90,0.95,0.99]:
        # This is an offline field-level simulation: it does not invent user
        # answers, propagate state, or count full conversations as fixed.
        ask=[r for r in records if r['gap']<threshold];accept=[r for r in records if r['gap']>=threshold]
        curve.append({'gap_below':threshold,'ask':len(ask),'accepted':len(accept),
          'errors_total':len(bad),'errors_flagged':sum(not r['state_correct'] for r in ask),
          'errors_unflagged':sum(not r['state_correct'] for r in accept),
          'accepted_errors':sum(not r['state_correct'] for r in accept),
          'accepted_error_rate':sum(not r['state_correct'] for r in accept)/len(accept) if accept else None})
    return {'n':n,'errors':len(bad),'correct':desc(good),'incorrect':desc(bad),'threshold_curve':curve}

def main():
    import torch,transformers,peft,bitsandbytes
    from transformers import AutoModelForSequenceClassification,AutoTokenizer,BitsAndBytesConfig
    from peft import PeftModel
    if DEST.exists():raise FileExistsError('Results are immutable')
    if not torch.cuda.is_available():raise RuntimeError('CUDA required')
    with (MODEL/'model.safetensors').open('rb') as f:
        digest=hashlib.file_digest(f,'sha256').hexdigest()
    if digest!=CHECKSUMS['ko']:raise ValueError('model digest mismatch')
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=digest:raise ValueError('data digest mismatch')
    old=json.loads((DATA/'heldout_cases.json').read_text(encoding='utf-8'))
    prior=json.loads((PRIOR/'results.json').read_text(encoding='utf-8'))['experiments']['all_6000']['heldout']['cases']
    train=[json.loads(x) for x in (DATA/'train.jsonl').read_text(encoding='utf-8').splitlines()]
    challenge=authored_cases()
    if {t['input'] for c in challenge for t in c['turns']}&{r['text'] for r in train}:
        raise ValueError('Challenge text overlaps fine-tuning data')
    if {t['input'] for c in challenge for t in c['turns']}&{t['input'] for c in old for t in c['turns']}:
        raise ValueError('Challenge text overlaps old examples')
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False);tok.padding_side='right'
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    base=AutoModelForSequenceClassification.from_pretrained(MODEL,quantization_config=quant,torch_dtype=torch.float16,
         device_map={'':0},local_files_only=True,trust_remote_code=False)
    model=PeftModel.from_pretrained(base,str(ADAPTER),is_trainable=False).eval()

    def logits_for(text,before):
        first=[];second=[]
        for field in SYMPTOMS:
            context='대상 증상: '+NAMES[field]+'\n이전 상태: '+before[field]+'\n이번 사용자 발화: '+text
            for option in OPTIONS:first.append(QUESTION+' '+DESCRIPTIONS[option]);second.append(context)
        batch=tok(first,second,padding=True,truncation=False,return_tensors='pt').to('cuda')
        if batch['input_ids'].shape[1]>512:raise ValueError('input over model limit')
        with torch.inference_mode():
            logits=model(**batch).logits[:,0].float().reshape(5,4).cpu()
        if not torch.isfinite(logits).all():raise ValueError('nonfinite scores')
        return logits

    def execute(cases,mode,prior_cases=None):
        result=[];sessions=[];disagreements=[]
        for case_index,case in enumerate(cases):
            session=SymptomSession();gold_before=empty_state();turns=[]
            for turn_index,spec in enumerate(case['turns']):
                before=dict(gold_before) if mode=='gold_previous' else session.state
                logits=logits_for(spec['input'],before)
                probabilities=torch.softmax(logits.double(),dim=-1)
                winners=logits.argmax(-1).tolist();patch={}
                if mode=='end_to_end':
                    for f,i in zip(SYMPTOMS,winners):
                        if OPTIONS[i]!='unchanged':patch[f]=OPTIONS[i]
                    if patch:session.update(patch)
                    if prior_cases is not None:
                        ref=prior_cases[case_index]['turns'][turn_index]
                        if before!=ref['before'] or session.state!=ref['after']:
                            disagreements.append({'case_id':case['id'],'turn':turn_index+1})
                for i,f in enumerate(SYMPTOMS):
                    scores=probabilities[i].tolist();sorted_scores=sorted(scores,reverse=True)
                    chosen=OPTIONS[winners[i]]
                    after=before[f] if chosen=='unchanged' else chosen
                    row={'group':mode,'case_id':case['id'],'turn':turn_index+1,'input':spec['input'],
                         'field':f,'previous':before[f],'gold_previous':gold_before[f],
                         'gold_patch':spec.get('gold_patch',{}).get(f,'unchanged'),
                         'expected_state':spec['expected'][f],'choice':chosen,'predicted_state':after,
                         'state_correct':after==spec['expected'][f],
                         'raw_logits':dict(zip(OPTIONS,logits[i].tolist())),
                         'relative_softmax_uncalibrated':dict(zip(OPTIONS,scores)),
                         'gap':sorted_scores[0]-sorted_scores[1],
                         'logit_gap':float(torch.topk(logits[i],2).values.diff().abs().item())}
                    result.append(row)
                turns.append({'input':spec['input'],'prior':before,'predicted':session.state if mode=='end_to_end' else None,
                              'expected':spec['expected'],'matches':session.state==spec['expected'] if mode=='end_to_end' else None})
                gold_before=dict(spec['expected'])
            sessions.append({'id':case['id'],'turns':turns,'passes':all(t['matches'] for t in turns) if mode=='end_to_end' else None})
        return result,sessions,disagreements

    old_rows,old_sessions,disagree=execute(old,'end_to_end',prior)
    if disagree:raise ValueError('Prior execution did not reproduce: '+str(disagree))
    old_teacher,_,_=execute(old,'gold_previous')
    challenge_rows,challenge_sessions,_=execute(challenge,'end_to_end')
    challenge_teacher,_,_=execute(challenge,'gold_previous')
    for group,rows in [('observed_end_to_end',old_rows),('observed_gold_previous',old_teacher),
                       ('challenge_end_to_end',challenge_rows),('challenge_gold_previous',challenge_teacher)]:
        for r in rows:r['group']=group
    DEST.mkdir(parents=True)
    allrows=old_rows+old_teacher+challenge_rows+challenge_teacher
    with (DEST/'scores.csv').open('x',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(allrows[0]));writer.writeheader()
        for r in allrows:
            writer.writerow({**r,'raw_logits':json.dumps(r['raw_logits'],ensure_ascii=False),
                             'relative_softmax_uncalibrated':json.dumps(r['relative_softmax_uncalibrated'],ensure_ascii=False)})
    case14=[r for r in old_rows if r['case_id']=='case-14' and r['turn']==1 and r['field']=='itching'][0]
    report={'model':'ko-decision-roberta-large with QLoRA step-1500; local NF4 fp16',
      'adapter_sha256':hashlib.sha256((ADAPTER/'adapter_model.safetensors').read_bytes()).hexdigest(),
      'versions':{'torch':torch.__version__,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__},
      'caveat':'all cases synthetic; labels not independently human reviewed; old cases previously observed; challenge written after observing error; no statistical calibration or deployment',
      'score_definition':'softmax across four model logits, T=1; relative scores, not probability of correctness; gap = top minus second',
      'evaluation_modes':'end_to_end propagates predictions; gold_previous resets to gold state each turn and isolates immediate update errors',
      'prior_run_reproduction_mismatches':disagree,'case14_itching':case14,
      'summaries':{'observed_end_to_end':summarize(old_rows),'observed_gold_previous':summarize(old_teacher),
                   'challenge_end_to_end':summarize(challenge_rows),'challenge_gold_previous':summarize(challenge_teacher)},
      'challenge_cases':challenge,'observed_sessions':old_sessions,'challenge_sessions':challenge_sessions}
    (DEST/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'case14_itching':case14,'summaries':report['summaries'],
                      'challenge_passes':sum(c['passes'] for c in challenge_sessions),
                      'challenge_scenarios':len(challenge_sessions)},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
