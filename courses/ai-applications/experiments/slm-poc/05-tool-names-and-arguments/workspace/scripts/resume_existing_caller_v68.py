"""Resume the path-only interrupted V68 development run, retaining completed evidence."""
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import existing_caller_runtime_v68 as runtime
from scripts import existing_caller_v68 as run
from scripts.korean_material_v67 import write,sha
P=run.P
AMEND=P/'resume-amendment.json'


def summarize(rows):
    ts=[t for e in rows for t in e['turns']]
    return {'n':len(rows),'goal_and_stop':sum(e['goal_and_stop'] for e in rows),
        'required_write_n':sum(t['grade']['required_write'] for t in ts),
        'required_correct_write':sum(t['grade']['requested_correct_write'] for t in ts),
        'forbidden_write_turns':sum(not t['grade']['required_write'] for t in ts),
        'unwanted_writes':sum(t['grade']['unwanted_write'] for t in ts),
        'wrong_mode_writes':sum(t['grade']['wrong_mode_write'] for t in ts if t['grade']['required_write']),
        'no_call_n':sum(e['kind'] in ['ask','missing'] for e in rows),
        'no_call_correct':sum(e['goal_and_stop'] for e in rows if e['kind'] in ['ask','missing']),
        'passed_ids':[e['id'] for e in rows if e['goal_and_stop']],
        'attempts':sum(len(t['trace']['events']) for t in ts),
        'failed_attempts':sum(e['result'].get('ok') is not True for t in ts for e in t['trace']['events']),
        'recovered_episodes':sum(e['goal_and_stop'] and any(x['result'].get('ok') is not True for t in e['turns'] for x in t['trace']['events']) for e in rows)}


def files(native,split,label,recover):
    # Original matrix.files reads its own old OUT after exp.file_eval writes run.P.
    # Only the report-root defect is corrected; inference and grading are unchanged.
    run.matrix.engine(recover)
    path=P/label/(split+'-files.json')
    if path.exists():
        rows=run.read(path)
        cases=[r for r in run.read(run.exp.DATA/'file-cases.json') if r['split']==split]
        assert [e['id'] for e in rows]==[e['id'] for e in cases]
        for e,c in zip(rows,cases):
            assert [t['expected'] for t in e['turns']]==c['turns']
            assert run.read(P/label/(split+'-episodes')/(e['id'].replace(':','-')+'.json'))==e
        return summarize(rows)
    run.exp.file_eval(native,split,label)
    return summarize(run.read(path))


def verify():
    p=runtime.verify()
    for name,h in run.read(AMEND)['files'].items():assert sha(ROOT/name)==h,name
    return p


def dev():
    verify();assert not (P/'global-development-selection.json').exists()
    assert not (P/'started-resume.json').exists(),'Protected resume'
    write(P/'started-resume.json',{'final_read':False})
    run.exp.RUN=P
    n=run.load(run.F_MODEL,run.F_REV)
    candidates=run.read(run.matrix.OUT/'controls-rejected-before-final.json')['candidates']
    base=run.read(run.matrix.AB/'baseline/dev-summary.json')
    cache={}
    for e in run.read(P/'F-native/dev-files.json'):
        for t in e['turns']:
            for g in t['trace']['generations']:
                cache[g['input_ids_sha256']]=copy.deepcopy(g)
    first_public=first_retention=None
    for label,recover,policy in [('F-native',False,False),('F-feedback',True,False),('F-policy',True,True)]:
        n.generate=runtime.generated(n,policy,cache)
        f=files(n,'dev',label,recover)
        if label!='F-feedback':
            pub=run.exp.public_eval(n,'dev',label);ret=run.exp.retention_eval(n,label)
            if label=='F-native':first_public=pub;first_retention=ret
        else:pub=first_public;ret=first_retention
        r={'files':f,'public':pub,'retention':ret};write(P/label/'dev-summary.json',r)
        healthy,score=run.exp.health_and_score(r,base)
        candidates.append({'label':label,'model':run.F_MODEL,'lr':0,'presentations':0,'healthy':healthy,'score':score,'dev':r})
        print('V68 DEV',label,json.dumps(r),flush=True)
    chosen=max(candidates,key=lambda r:(r['healthy'],r['score'],-r['presentations'],-r['lr']))
    write(P/'global-development-selection.json',{'selected':chosen,'candidates':candidates,'final_read':False})
    if not chosen['healthy']:
        write(P/'no-healthy-candidate.json',{'reason':'All eight fixed dev arms failed preservation/permission conditions. No final outcomes generated.','selected_for_diagnosis':chosen['label']})
    verify();print('V68 DEV SELECTION',chosen['label'],'healthy',chosen['healthy'],flush=True)


if __name__=='__main__':
    if '--prepare' in sys.argv:
        runtime.verify();assert not AMEND.exists();assert not (P/'global-development-selection.json').exists()
        assert (P/'F-native/dev-files.json').exists()
        retained=[P/'F-native/dev-files.json']+list((P/'F-native/dev-episodes').glob('*.json'))
        paths=[Path(__file__),ROOT/'scripts/existing_caller_runtime_v68.py',P/'started-dev.json']+retained
        write(AMEND,{'reason':'Previous process ended after all16 F-native file episodes. Code inspection identifies matrix.files reading its old matrix.OUT rather than exp.RUN. Native dev-files exists; no public rows/summary, other F profiles, or final outcomes exist. Correct only report path; preserve all completed native episodes without regeneration. Original protected started marker remains.',
             'unchanged':'Pinned weights, three profiles, material, generation, strict parser, tool execution, graders, health gates and selection rule.',
             'files':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
        print('V68 path-only resume frozen;16 completed episodes retained.')
    else:
        run.matrix.files=files;run.verify=verify
        try:
            if '--dev' in sys.argv:dev()
            elif '--final-baseline' in sys.argv:run.final(True)
            elif '--final-selected' in sys.argv:run.final(False)
            else:raise ValueError('Choose a phase')
        except Exception as e:
            import traceback
            write(P/'resume-failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
            raise
