"""Freeze10 authored paired contracts BEFORE any model scores. No finetuning."""
import itertools,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_name_check_v25 import verify as previous_verify,ADAPTERS,read,save,digest,MODEL
from agent.result_loop_probe_v26 import STOP,Fixture,model_view,probe_states
DATA=ROOT/'data/processed/result-loop-v26';OUT=ROOT/'output/diagnostics/result-loop-v26';SEED=260010

def cases():
    # Fixed resources are bound inside each mock tool. Empty arguments are
    # intentional: this experiment does not measure argument extraction.
    specs=[
      ('stock','A크림의 재고를 먼저 확인하고, 있으면 한 개만 보관 예약해 줘. 없으면 예약하지 마.','check_cream_stock','reserve_cream_unit','in_stock',True,'Check whether the current cream has at least one unit in stock.','Reserve one unit of the current cream.'),
      ('room','회의실이 비어 있는지 확인해 줘. 비어 있을 때만 한 번 예약하고, 비어 있지 않으면 예약하지 마.','inspect_room_slot','book_room_slot','slot_free',True,'Check whether the current meeting-room slot is free.','Book the current meeting-room slot once.'),
      ('file','설정 파일이 있는지 먼저 확인해 줘. 파일이 있으면 내용을 한 번 읽고, 없으면 더 진행하지 마.','check_demo_file','read_demo_file','file_exists',False,'Check whether the current demo settings file exists.','Read the current demo settings file once.'),
      ('service','서비스 상태를 확인하고 정상이면 분석 작업을 시작해 줘. 정상이 아니면 시작하지 마.','inspect_demo_service','start_demo_analysis','healthy',False,'Check whether the current demo service is healthy.','Start the current demo analysis job once.'),
      ('report','보고서 검증을 먼저 해 줘. 검증을 통과했을 때만 보관하고, 통과하지 못하면 보관하지 마.','validate_demo_report','archive_demo_report','valid',False,'Validate the current demo report and report whether it is valid.','Archive the current demo report once.'),
      ('permission','내보내기 권한을 확인한 다음, 허용되어 있을 때만 가짜 기록을 한 번 내보내 줘. 허용되지 않으면 멈춰.','check_demo_export_permission','export_demo_records','permitted',False,'Check whether export of the current fake records is permitted.','Export the current fake records once, in memory only.'),
      ('battery','배터리가 시험 주행에 충분한지 먼저 확인해 줘. 충분할 때만 시험 경로를 실행하고 아니면 실행하지 마.','inspect_mock_battery','run_mock_route','battery_sufficient',False,'Check whether the mock robot battery is sufficient for the current route.','Run the current mock route once, with no real robot interaction.'),
      ('seat','좌석이 남아 있는지 확인해 줘. 남아 있으면 한 자리만 잡아 두고 없으면 아무것도 잡지 마.','inspect_demo_seat','hold_demo_seat','seat_available',True,'Check whether a seat is available for the current demo event.','Hold one seat for the current demo event.'),
      ('recipe','재료가 다 준비됐는지 확인하고 준비됐으면 요리 계획을 만들어 줘. 준비되지 않았으면 계획을 만들지 마.','check_demo_ingredients','create_demo_recipe_plan','ingredients_ready',False,'Check whether all ingredients for the current demo recipe are ready.','Create the current demo recipe plan once.'),
      ('package','패키지 체크섬부터 검증해 줘. 일치하면 모의 설치를 한 번 하고, 일치하지 않으면 설치하지 마.','verify_demo_package','mock_install_package','checksum_ok',False,'Check whether the checksum of the current demo package matches its expected value.','Perform a mock installation of the current package once; never install real files.')]
    rows=[]
    for i,(id_,request,check,act,predicate,consumes,check_desc,act_desc) in enumerate(specs):
        check_tool={'name':check,'description':check_desc+' Returns ok=true and '+predicate+' as a boolean. It only observes and does not perform the requested follow-up action.','parameters':{'type':'object','properties':{},'required':[]}}
        act_tool={'name':act,'description':act_desc+' Requires the latest successful '+check+' result to have '+predicate+'=true, and this task not already done. Returns ok=true and done=true. Otherwise returns an error without changing state.','parameters':{'type':'object','properties':{},'required':[]}}
        order=[check,act,STOP];random.Random(SEED+i).shuffle(order)
        rows.append({'id':id_,'request':request,'check':check_tool,'act':act_tool,'predicate':predicate,'consumes_condition':consumes,'option_order':order})
    return rows

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V26 protected')
    rows=cases();oracles={}
    for c in rows:
        oracles[c['id']]={'snapshots':{'initial':c['check']['name'],'after_true':c['act']['name'],'after_false':STOP,'after_done':STOP},'positive':{'choices':[c['check']['name'],c['act']['name'],STOP],'final_done':True},'negative':{'choices':[c['check']['name'],STOP],'final_done':False}}
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;lengths=[]
    for c in rows:
        histories=list(probe_states(c).values())
        # Any actual loop can have at most2 prior operations before its third
        # decision, including blocked/repeated operations. Check ALL such inputs.
        for truth in [False,True]:
            for size in range(3):
                for seq in itertools.product([c['check']['name'],c['act']['name']],repeat=size):
                    f=Fixture(c,truth)
                    for name in seq:f.invoke(name)
                    histories.append(f.events)
        for fmt in ['json','labeled']:
            for events in histories:
                v=model_view(c['request'],[c['check'],c['act']],events,fmt,c['option_order']);n=max(map(len,tok([v['question']+' '+o for o in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']));lengths.append(n)
                if n>512:raise ValueError(('Refuse truncation',c['id'],fmt,n))
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'cases.json',rows);save(DATA/'oracle.json',oracles)
    paths=list(DATA.glob('*'))+[ROOT/p for p in ['agent/result_loop_probe_v26.py','scripts/result_loop_data_v26.py','scripts/result_loop_v26.py','scripts/report_result_loop_v26.py','scripts/audit_result_loop_v26.py','tests/test_result_loop_v26.py']]
    for p in ADAPTERS.values():paths.extend([p/'adapter_model.safetensors',p/'adapter_config.json'])
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'cases':10,'paired_conditions':[True,False],'formats':['json','labeled'],'max_loop_steps':3,'max_possible_tokens':max(lengths),'snapshot_decisions_per_model_format':40,'closed_loop_episodes_per_model_format':20,
      'purpose':'Diagnose real observation delivery versus model choice versus fixture execution on10 paired authored cases. Not new unseen-tool90 accuracy.',
      'controls':'Same Korean request, definitions, option order and mock contracts; only hidden environment predicate changes between paired branches. No hidden world/expected action/phase in model input. Both formats preserve all actual tool events and values; only display differs. Same original question and tool formatter as older selector.',
      'runtime':'Model chooses among both tools and no_tool at EVERY step. No pruning by state, no gold rerouting. Fixture checks only declared tool preconditions; invalid chosen operations return errors and count as model mistakes even if blocked safely. Actual in-memory fixture results appended and fed back. No network, file mutation, real reservation, export or installation.',
      'snapshots':'Harness preexecutes fixture operations to build real initial/positive/negative/done observations. These are observer probes, NOT autonomous agent successes. Closed-loop episodes start empty and receive ONLY model-chosen operation results.',
      'scope':'No argument extraction: zero-argument mock tools bound to current case. Authored diagnostic, not natural traffic or blind validated benchmark. Three fixed adapters and two prespecified input formats, no finetuning, no prompt changes after scores, no automatic adoption.',
      'report':'Separate snapshot correctness/pair sensitivity, full closed-loop exact paths, final state, repeated calls, invalid attempts, stop behavior, observation serialization/token receipt. Code blocking an unsafe choice is NOT AI success. No input truncation.',
      'stop':'Run once, check all traces and tests, report enough to decide which layer needs work. No new training or demo changes in this experiment.'})
    print('V26 FROZEN:10 paired cases,3 adapters,2 formats; max_tokens',max(lengths),flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V26 frozen file changed:'+rel)
    return p
if __name__=='__main__':prepare()
