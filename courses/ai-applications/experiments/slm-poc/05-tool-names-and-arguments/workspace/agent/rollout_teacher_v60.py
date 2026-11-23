"""Offline label checker. Never imported by execution runtimes."""
import copy

def valid_next(case,packet):
    """Label only recoverable prefixes; no gold routing during execution."""
    ids=case['ids'];inverse={n:r for r,n in ids.items()}
    plan=case['teacher_plan'];needed=[r for r in plan if r not in ('none','ask')]
    events=packet['events'];actual=[inverse.get(e['tool'],'?') for e in events]
    if any(e['result'].get('ok') is not True for e in events):return None,'error_ended_runtime'
    # All observed write effects must be those requested, in order. No invented
    # recovery labels after irreversible actions or missing mandated earlier reads.
    if actual!=needed[:len(actual)]:return None,'not_verified_recoverable_prefix'
    if len(actual)<len(needed):return ids[needed[len(actual)]],'continue' if actual else 'start'
    return plan[-1] if plan[-1] in ('none','ask') else 'none','end'

def row_for(case,entry,index):
    target,stage=valid_next(case,entry['packet'])
    if target is None:return None,stage
    view=entry['view'];raw=entry['response']['raw_scores'];prediction=max(view['options'],key=raw.get)
    return {'id':case['id']+':visited:'+str(index),'question':view['question'],'options':copy.deepcopy(view['options']),
        'context':view['context'],'target':target,'stage':stage,'prediction':prediction,'wrong':prediction!=target,
        'source_case':case['id'],'label_source':'existing assistant-authored training plan; checked actual recoverable event prefix; no independent human review'},None
