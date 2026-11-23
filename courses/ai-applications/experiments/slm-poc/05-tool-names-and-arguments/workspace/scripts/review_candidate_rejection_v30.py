"""Read-only candidate matrix on known V29 trajectories; NOT a new agent rollout."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.gate_pair_data_v29 import verify as previous_verify,DATA as D29,OUT as V29,SELECTOR,read,save,digest
from scripts.result_loop_split_v27 import Engine
from agent.result_loop_split_v27 import selector_view,gate_view
from agent.result_loop_probe_v26 import STOP,stable
DATA=ROOT/'data/processed/candidate-rejection-review-v30';OUT=ROOT/'output/diagnostics/candidate-rejection-review-v30';GATE=V29/'control/final-adapter'

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V30 protected')
    if digest(GATE/'adapter_model.safetensors')!=read(V29/'control/complete.json')['adapter_sha256']:raise ValueError('Gate changed')
    cases={c['id']:c for c in read(D29/'fresh-cases.json')};gold=read(D29/'oracle.json')['fresh'];occ=[]
    for ei,e in enumerate(read(V29/'control-legacy-fresh-episodes.json')):
        c=cases[e['case_id']];expected=gold[e['case_id']]['positive' if e['condition'] else 'negative']['choices'];prefix=True
        for si,s in enumerate(e['steps']):
            d=s['decision'];v=selector_view(c['request'],[c['check'],c['act']],s['observation_before'],c['option_order'])
            if v!=d['selector']['model_input']:raise ValueError('Source input mismatch')
            exp=expected[si] if prefix and si<len(expected) else None
            occ.append({'episode':ei,'case_id':e['case_id'],'condition':e['condition'],'step':si,'tools':[c['check'],c['act']],
                'selector_view':v,'selector_scores':d['selector']['raw_scores'],'original':d['selected'],'original_proposal':d['proposed_tool'],
                'original_gate':d['gate'],'prefix_correct':prefix,'expected_if_correct_prefix':exp})
            if exp!=d['selected']:prefix=False
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'occurrences.json',occ)
    paths=[DATA/'occurrences.json',Path(__file__),D29/'fresh-cases.json',D29/'oracle.json',V29/'control-legacy-fresh-episodes.json',V29/'control/complete.json']
    for p in [SELECTOR,GATE]:paths += [p/'adapter_model.safetensors',p/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'threshold':-1.5,
      'proposal':'Compare original top1-then-gate with highest-selector-score among all gate-approved candidates. Same fixed selector scores, gate weights, context and threshold. No raw-score multiplication, no learned success-probability claim.',
      'scope':'Known V29 control primary32 trajectories, all observed steps, not just failures. Score both tools at the SAME observed input. No tool handlers called, no training, no independent validation or new autonomous rollout. Alternative histories are not executed; local repairs are NOT full episode successes.',
      'grading':'Only prefixes that matched the canonical expected path have a next-step label. Post-first-error states remain ungraded. Report fixes of first errors AND destruction of originally correct stops; no best cutoff or case selection.',
      'references':[{'title':'SayCan official project','url':'https://say-can.github.io/','use':'Candidate-wise usefulness and feasibility; NOT transplanting robot probabilities, pretrained value functions or success rates.'},{'title':'ToolSandbox official research','url':'https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark','use':'Actual state dependencies and intermediate/final outcomes in future rollout evaluation; not installed or benchmarked.'},{'title':'ToolRerank original publication','url':'https://aclanthology.org/2024.lrec-main.1413/','use':'Reviewed but not selected: retrieval over many APIs is not today\'s two-candidate top1-veto issue.'}]})
    print('V30 FROZEN:',len(occ),'known decision occurrences; no new rollout',flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V30 frozen changed:'+rel)
    return p

def run():
    cfg=verify()
    if (OUT/'started.json').exists():raise FileExistsError('V30 protected')
    save(OUT/'started.json',{'protocol':digest(DATA/'protocol.json')});g=Engine(GATE);records=[];maxerr=0.
    for r in read(DATA/'occurrences.json'):
        scores={t['name']:g.score(gate_view(t,r['selector_view']['context'])) for t in r['tools']}
        margins={k:d['raw_scores']['yes']-d['raw_scores']['no'] for k,d in scores.items()};allowed=[k for k in r['selector_view']['options'] if margins[k]>=cfg['threshold']]
        selected=max(allowed,key=r['selector_scores'].get) if allowed else STOP
        # The scoring and alternative-selection logic never uses expected labels.
        maxerr=max(maxerr,max(abs(scores[r['original_proposal']]['raw_scores'][k]-r['original_gate']['raw_scores'][k]) for k in ['yes','no']))
        records.append({'source':r,'all_tool_scores':scores,'margins':margins,'approved':allowed,'alternative_selected':selected})
    if maxerr>.05:raise ValueError('Original gate replay failed')
    save(OUT/'matrix.json',records);save(OUT/'complete.json',{'max_original_gate_logit_error':maxerr,'actual_gate_forwards':g.calls,'max_tokens':g.max_tokens,'no_training':True,'no_handlers_called':True,'no_deployment':True});verify();print('V30 MATRIX COMPLETE',flush=True)

def report():
    cfg=verify();receipt=read(OUT/'complete.json');records=read(OUT/'matrix.json');counts={'occurrences':len(records),'first_error_occurrences':0,'locally_fixed_first_errors':0,'original_correct_stops':0,'correct_stops_changed_to_tool':0,'original_correct_steps':0,'correct_steps_changed':0,'ungraded_post_error':0};changes=[];audit=True
    for x in records:
        r=x['source'];exp=r['expected_if_correct_prefix'];selected=x['alternative_selected']
        expected_views={t['name']:gate_view(t,r['selector_view']['context']) for t in r['tools']}
        audit &= all(d['model_input']==expected_views[k] and d['tokens']<=512 and d['adapter_sha256']==digest(GATE/'adapter_model.safetensors') for k,d in x['all_tool_scores'].items())
        approved=[k for k in r['selector_view']['options'] if x['margins'][k]>=cfg['threshold']]
        audit &= selected==(max(approved,key=r['selector_scores'].get) if approved else STOP)
        if not r['prefix_correct']:counts['ungraded_post_error']+=1;continue
        if r['original']==exp:
            counts['original_correct_steps']+=1;counts['correct_steps_changed']+=selected!=exp
            if exp==STOP:counts['original_correct_stops']+=1;counts['correct_stops_changed_to_tool']+=selected!=STOP
        else:
            counts['first_error_occurrences']+=1;counts['locally_fixed_first_errors']+=selected==exp
        if selected!=r['original']:changes.append({'case_id':r['case_id'],'condition':r['condition'],'step':r['step'],'expected':exp,'old':r['original'],'new':selected,'new_correct_at_this_state':selected==exp})
    assert audit and receipt['max_original_gate_logit_error']<=.05
    save(OUT/'summary.json',{'counts':counts,'changes':changes,'audit_all_inputs_and_choices':bool(audit),'scope':cfg['scope'],'no_full_episode_accuracy_claim':True});print(__import__('json').dumps({'counts':counts,'changes':changes},indent=2))
if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='run':run()
    elif sys.argv[1]=='report':report()
    else:raise ValueError(sys.argv[1])
