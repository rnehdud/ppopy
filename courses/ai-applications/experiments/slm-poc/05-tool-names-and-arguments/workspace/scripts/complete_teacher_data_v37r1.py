"""Re-encode the SAME complete V37 material; no labels/cases/traces are changed."""
import copy,csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.complete_teacher_data_v37 import DATA as BASE_DATA,OUT as BASE_OUT,MODEL,GoldTeacherSession,read,save,digest,verify as parent_verify
from agent.decision_context_v37r1 import make_view,stable
DATA=ROOT/'data/processed/complete-next-action-v37r1';OUT=ROOT/'output/diagnostics/complete-next-action-v37r1'


def prepare():
    original_cfg=parent_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V37r1 protected')
    original_manifest=read(BASE_DATA/'build-manifest.json')
    if not all(digest(ROOT/p)==h for p,h in original_manifest['files'].items()):raise ValueError('Original material changed')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);rows=[]
    for split in ['train','heldout']:
        converted=[]
        for old in read(BASE_DATA/(split+'.json')):
            row=copy.deepcopy(old);view,meta=make_view(row['question'],row['options'],row['source_packet'],tok);row.update(view);row['encoding']=meta;converted.append(row)
        rows+=converted;save(DATA/(split+'.json'),converted)
    reviews=read(BASE_DATA/'teaching-review.json');save(DATA/'cases.json',read(BASE_DATA/'cases.json'));save(DATA/'teaching-review.json',reviews)
    with (DATA/'teaching-review.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','split','family','text','gold_observations','expected_stored_patch','teacher_plan','actual_tools','final_state','max_tokens']);w.writeheader()
        for x in reviews:
            c=x['case'];rs=[r for r in rows if r['case_id']==c['id']];w.writerow({'id':c['id'],'split':c['split'],'family':c['family'],'text':c['text'],'gold_observations':stable(c['gold_observations']),'expected_stored_patch':stable(c['expected_stored_patch']),'teacher_plan':' -> '.join(c['teacher_plan']),'actual_tools':' -> '.join(e['tool'] for e in x['actual_trace']['events']),'final_state':stable(x['actual_trace']['after']),'max_tokens':max(r['encoding']['tokens'] for r in rs)})
    audit=(ROOT/'scripts/audit_complete_teacher_v37.py').read_text(encoding='utf-8')
    audit=audit.replace('from scripts.complete_teacher_data_v37 import DATA,OUT,MODEL,GoldTeacherSession,verify,read,save,digest','from scripts.complete_teacher_data_v37r1 import DATA,OUT,MODEL,GoldTeacherSession,verify,read,save,digest')
    audit=audit.replace('from agent.decision_context_v37 import decode,legacy_context,stable','from agent.decision_context_v37r1 import decode,legacy_context,stable')
    audit=audit.replace('完全な操作履歴の教材確認-v37.txt','完全な操作履歴の教材確認-v37r1.txt').replace('（V37）','（V37r1）')
    audit_path=ROOT/'scripts/audit_complete_teacher_v37r1.py';audit_path.write_text(audit,encoding='utf-8')
    cfg=copy.deepcopy(original_cfg);cfg['revision']='Initial reversible envelope reached526 tokens and failed the gate. Flatten envelope + losslessly join whitespace-free action labels only. Every conversation, source packet, actual result, target and split is unchanged. No model scored or trained.'
    files=[Path(__file__),ROOT/'agent/decision_context_v37r1.py',ROOT/'tests/test_decision_context_v37r1.py',audit_path,BASE_DATA/'protocol.json',BASE_DATA/'build-manifest.json']+list(DATA.iterdir())
    cfg['frozen_files']={str(p.relative_to(ROOT)):digest(p) for p in files if p.is_file()};save(DATA/'protocol.json',cfg)
    save(DATA/'build-manifest.json',{'files':{str(p.relative_to(ROOT)):digest(p) for p in DATA.iterdir() if p.is_file() and p.name!='build-manifest.json'},'no_training':True,'no_model_scoring':True,'parent_label_and_case_provenance':digest(BASE_DATA/'build-manifest.json')})
    checks={}
    for split in ['train','heldout']:
        old=read(BASE_DATA/(split+'.json'));new=read(DATA/(split+'.json'))
        strip=lambda r:{k:v for k,v in r.items() if k not in ['context','encoding']}
        checks[split+'_all_non_encoding_fields_identical']=[strip(r) for r in old]==[strip(r) for r in new]
    checks['cases_identical']=read(DATA/'cases.json')==read(BASE_DATA/'cases.json');checks['full_actual_traces_identical']=read(DATA/'teaching-review.json')==read(BASE_DATA/'teaching-review.json')
    save(OUT/'revision-audit.json',{'checks':checks,'all_passed':all(checks.values()),'before_max_tokens':max(r['encoding']['tokens'] for s in ['train','heldout'] for r in read(BASE_DATA/(s+'.json'))),'after_max_tokens':max(r['encoding']['tokens'] for r in rows)})
    if not all(checks.values()):raise ValueError('Non-encoding material changed')
    print('V37r1 same420 rows re-encoded; max tokens',max(r['encoding']['tokens'] for r in rows),flush=True)


def verify():
    parent_verify();cfg=read(DATA/'protocol.json')
    for rel,h in cfg['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V37r1 changed: '+rel)
    return cfg
if __name__=='__main__':prepare()
