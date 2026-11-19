"""Freeze new task families and additions/removals/completed/renamed variants."""
import copy,itertools,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.review_candidate_rejection_v30 import verify as previous_verify,DATA as D30,GATE,SELECTOR,V29,D29,read,save,digest
from scripts.gate_pair_data_v29 import MODEL,D27,D28
from agent.candidate_loop_v31 import World,public_tools
from agent.result_loop_probe_v26 import STOP
from agent.result_loop_split_v27 import selector_view,gate_view
DATA=ROOT/'data/processed/candidate-loop-v31';OUT=ROOT/'output/diagnostics/candidate-loop-v31';SEED=310012
VARIANTS=['plain','distracted','missing_check','missing_act','renamed','completed','completed_distracted']

def fresh_cases():
    specs=[
      ('csv','CSV 구분자를 인식할 수 있는지 먼저 확인해 줘. 인식할 수 있으면 모의 읽기를 한 번 하고 아니면 읽지 마.','inspect_virtual_csv_delimiter','parse_virtual_csv','recognized',False,'Check whether the current virtual CSV delimiter is recognized.','Parse the current virtual CSV once.'),
      ('frames','시험 프레임의 시각 순서가 맞는지 검사해 줘. 순서가 맞을 때만 한 번 합치고 틀리면 합치지 마.','inspect_mock_frame_order','merge_mock_frames','ordered',False,'Check whether timestamps of the current mock frames are ordered.','Merge the current mock frames once.'),
      ('texture','질감 자료가 준비됐는지 먼저 확인하고, 준비됐을 때만 가상 표면에 한 번 적용해 줘. 준비되지 않았으면 적용하지 마.','inspect_virtual_texture_asset','apply_virtual_texture','prepared',False,'Check whether the current virtual texture asset is prepared.','Apply the current virtual texture once.'),
      ('draft','가상 편지함에 초안을 넣을 수 있는지 확인해 줘. 가능하면 가짜 초안을 한 번 저장하고 아니면 저장하지 마.','inspect_virtual_draft_mailbox','save_virtual_draft','writable',False,'Check whether the current virtual draft mailbox is writable.','Save the current fake draft once; do not send a real message.'),
      ('bin','가상 청소기의 먼지통에 여유가 있는지 확인해 줘. 여유가 있을 때만 모의 청소를 한 번 하고 없으면 하지 마.','inspect_virtual_dust_bin','simulate_virtual_cleaning','has_space',True,'Check whether the current virtual dust bin has space.','Perform the current virtual cleaning task once.'),
      ('track','가상 선로가 비어 있는지 먼저 확인해 줘. 비어 있을 때만 시험 수레를 한 번 움직이고 아니면 움직이지 마.','inspect_virtual_cart_track','move_virtual_cart','clear',False,'Check whether the current virtual cart track is clear.','Move the current virtual cart once; no real hardware.'),
      ('grammar','시험 문법의 규칙이 유효한지 검사하고, 유효할 때만 가짜 분석기를 한 번 만들어 줘. 무효면 만들지 마.','inspect_mock_grammar_rules','compile_mock_parser','valid',False,'Check whether the current mock grammar rules are valid.','Compile the current mock parser once.'),
      ('elevation','지형 높이 자료가 있는지 확인해 줘. 있으면 모의 음영 지도를 한 번 그리고 없으면 그리지 마.','inspect_virtual_elevation_data','shade_virtual_terrain','available',False,'Check whether the current virtual elevation data is available.','Shade the current virtual terrain once.'),
      ('consentlog','시험 로그를 저장해도 된다는 동의가 있는지 먼저 확인해 줘. 동의가 있으면 가짜 로그를 한 번 남기고 없으면 남기지 마.','inspect_mock_log_consent','save_mock_event_log','consented',False,'Check whether consent to save the current mock log is present.','Save the current mock event log once, in memory only.'),
      ('surface','도형의 길이가 모두 양수인지 검사해 줘. 모두 양수일 때만 모의 넓이를 한 번 계산하고 아니면 계산하지 마.','inspect_virtual_shape_lengths','compute_virtual_surface','positive',False,'Check whether all lengths of the current virtual shape are positive.','Compute the current virtual surface area once.'),
      ('numeric','시험 표의 값이 모두 숫자인지 확인한 다음, 모두 숫자일 때만 평균을 한 번 구하고 아니면 구하지 마.','inspect_mock_numeric_values','compute_mock_average','all_numeric',False,'Check whether all values in the current mock table are numeric.','Compute the current mock average once.'),
      ('samples','시험 표본이 충분한지 먼저 확인해 줘. 충분하면 모의 추정을 한 번 하고 부족하면 하지 마.','inspect_virtual_sample_count','estimate_virtual_value','sufficient',False,'Check whether the current virtual sample count is sufficient.','Estimate the current virtual value once.'),
    ];rows=[]
    concise={
      'csv':'먼저 CSV 구분자를 확인해. 인식 가능하면 한 번 읽고, 아니면 중단해.',
      'frames':'프레임 시각 순서를 검사해. 맞으면 한 번 합치고, 틀리면 중단해.',
      'texture':'질감 자료를 먼저 확인해. 준비됐으면 한 번 적용하고, 아니면 중단해.',
      'draft':'편지함에 쓸 수 있는지 확인해. 가능하면 가짜 초안을 한 번 저장하고, 아니면 중단해.',
      'bin':'먼지통 여유를 먼저 확인해. 있으면 모의 청소를 한 번 하고, 없으면 중단해.',
      'track':'선로부터 확인해. 비었으면 수레를 한 번 움직이고, 아니면 중단해.',
      'grammar':'문법 규칙을 검사해. 유효하면 모의 분석기를 한 번 만들고, 아니면 중단해.',
      'elevation':'높이 자료부터 확인해. 있으면 음영 지도를 한 번 그리고, 없으면 중단해.',
      'consentlog':'로그 저장 동의부터 확인해. 동의가 있으면 가짜 로그를 한 번 남기고, 없으면 중단해.',
      'surface':'도형 길이가 모두 양수인지 검사해. 맞으면 넓이를 한 번 계산하고, 아니면 중단해.',
      'numeric':'값이 모두 숫자인지 확인해. 맞으면 평균을 한 번 구하고, 아니면 중단해.',
      'samples':'표본 수부터 확인해. 충분하면 모의 추정을 한 번 하고, 아니면 중단해.'}
    short_actions={'csv':'Parse the virtual CSV once.','frames':'Merge the mock frames once.','texture':'Apply the virtual texture once.',
      'draft':'Save one mock draft.','bin':'Simulate cleaning once.','track':'Move the virtual cart once.',
      'grammar':'Compile the mock parser once.','elevation':'Shade the virtual terrain once.','consentlog':'Save one mock event log.',
      'surface':'Compute the virtual surface area once.','numeric':'Compute the mock average once.','samples':'Estimate the virtual value once.'}
    for i,(id_,req,check,act,pred,consumes,cd,ad) in enumerate(specs):
        p={'type':'object','properties':{},'required':[]};req=concise[id_]
        cd=cd.replace('the current virtual ','the ').replace('the current mock ','the ');ad=short_actions[id_]
        ct={'name':check,'description':cd+' Returns ok=true and '+pred+':boolean. Read-only.','parameters':copy.deepcopy(p)}
        at={'name':act,'description':ad+' Needs latest '+check+'.'+pred+'=true; task not done. Success done=true; else error,no change.','parameters':copy.deepcopy(p)}
        extras=[{'name':'utility_clock_'+id_,'description':'Return the current UTC time of a separate mock server. Read-only; does not change task state.','parameters':copy.deepcopy(p),'mock_kind':'clock'},
                {'name':'utility_note_'+id_,'description':'Append the default demo text to a separate scratchpad. Returns ok=true and note_saved=true.','parameters':copy.deepcopy(p),'mock_kind':'note'}]
        rows.append({'id':id_,'request':req,'check':ct,'act':at,'predicate':pred,'consumes_condition':consumes,'extras':extras})
    return rows

def scenario(case,variant,truth,index,cohort='fresh'):
    c=copy.deepcopy(case)
    if variant=='renamed':
        old=c['check']['name'];c['check']['name']='op_'+str(index)+'_q7';c['act']['name']='op_'+str(index)+'_r2';c['act']['description']=c['act']['description'].replace(old,c['check']['name'])
    tools=[c['check'],c['act']]
    if variant in ['distracted','missing_check','missing_act','completed_distracted']:tools+=c['extras']
    if variant=='missing_check':tools=[t for t in tools if t['name']!=c['check']['name']]
    if variant=='missing_act':tools=[t for t in tools if t['name']!=c['act']['name']]
    order=[t['name'] for t in tools]+[STOP]
    if cohort=='previous':order=case['option_order'][:]
    else:random.Random(SEED+index*20+VARIANTS.index(variant)).shuffle(order)
    return {'id':cohort+':'+case['id']+':'+variant+':'+str(truth),'cohort':cohort,'variant':variant,'case':c,'condition':truth,'seed_done':variant.startswith('completed'),'tools':tools,'option_order':order}

def oracle(s):
    c=s['case'];variant=s['variant'];check=c['check']['name'];act=c['act']['name']
    if s['seed_done']:paths=[[STOP]];done=True
    elif variant=='missing_check':paths=[[STOP]];done=False
    elif variant=='missing_act':paths=[[STOP],[check,STOP]];done=False
    else:paths=[[check,act,STOP] if s['condition'] else [check,STOP]];done=s['condition']
    return {'allowed_paths':paths,'final_done':done}

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V31 protected')
    cases=fresh_cases();prior=read(D27/'known-cases.json')+read(D27/'fresh-cases.json')+read(D28/'fresh-cases.json')+read(D29/'fresh-cases.json')
    names={c[k]['name'] for c in cases for k in ['check','act']};old={c[k]['name'] for c in prior for k in ['check','act']}
    if names&old:raise ValueError('Name overlap')
    scenarios=[]
    for i,c in enumerate(cases):
        for v in VARIANTS:
            for truth in ([True] if v.startswith('completed') else [True,False]):scenarios.append(scenario(c,v,truth,i))
    for i,c in enumerate(read(D29/'fresh-cases.json')):scenarios.extend(scenario(c,'plain',t,i,'previous') for t in [True,False])
    # Actual fixture histories, including seeded completed tasks and unrelated calls.
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;maximum=0;largest=None
    def length(v):return max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
    for s in scenarios:
        ts=public_tools(s['tools'])
        for n in range(3):
            for seq in itertools.product([t['name'] for t in ts],repeat=n):
                w=World(s)
                for name in seq:w.invoke(name)
                v=selector_view(s['case']['request'],ts,w.events,s['option_order'])
                for label,vv in [('selector',v)]+[(t['name'],gate_view(t,v['context'])) for t in ts]:
                    size=length(vv)
                    if size>maximum:maximum=size;largest={'scenario':s['id'],'history':seq,'candidate':label,'tokens':size}
    if maximum>512:raise ValueError(('No truncation',largest))
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'scenarios.json',scenarios);save(DATA/'oracle.json',{s['id']:oracle(s) for s in scenarios})
    paths=list(DATA.glob('*'))+[ROOT/p for p in ['agent/candidate_loop_v31.py','scripts/candidate_loop_data_v31.py','scripts/candidate_loop_v31.py','scripts/report_candidate_loop_v31.py','scripts/audit_candidate_loop_v31.py','tests/test_candidate_loop_v31.py']]
    paths += [V29/'control-legacy-fresh-episodes.json',V29/'control/complete.json']
    for p in [SELECTOR,GATE]:paths += [p/'adapter_model.safetensors',p/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'strategies':['top1','all_candidates'],'threshold':-1.5,'max_steps':3,'max_tokens':maximum,
      'counts':'Fresh12 families,144 scenarios/strategy across7 variants; previous16 families32 plain scenarios/strategy.352 complete mock episodes total. Variants/Boolean pairs are dependent, not144 independent tasks.',
      'controls':'Same V27-final selector and V29-control gate, request/description/observations/order/threshold. Only whether gate evaluates top1 or every candidate differs. No raw-score product, no training, no pruning by true state, no gold routing or automatic termination on done. Fresh descriptions shortened before token checks and before scores, equally for both strategies.',
      'variants':'plain2tools; distracted4tools including unrelated clock/read and scratchpad/write; missing_check leaves followup+2extras; missing_act leaves check+2extras; renamed updates BOTH tool IDs and internal cross-reference, not semantics; completed and completed_distracted seed ACTUAL check+successful act results, then test model stop. Seeded calls are not agent achievements.',
      'missing_labels':'Missing check: STOP only. Missing act: STOP or one available check then STOP accepted as cautious decline/partial inspection; not task completion. No response text/explanation evaluated.',
      'evaluation':'Plain fresh strict paths primary. Added/removed/renamed/done variants are separate guard groups, never pooled into claimed task-completion accuracy. Positive progress, negative attempted followup, unrelated operations, repeats, blocked calls, actual model queries and warm observed latency separately. Previous top1 replays V29 paths/scores as reference, not fresh validation.',
      'timing':'No memoized scores during episodes. Warmup2forwards excluded; alternate strategy execution order by scenario index. Forward counts and observed decision times include all candidates. One local run, not a robust hardware/production latency benchmark.',
      'adoption_guard':'No deployment regardless. Positive signal requires higher fresh plain strict and positive requested execution, no increase false-condition followup attempts or unrelated calls, no worsening correct-stop counts for either completed variant, and no missing-tool guard loss. All guard groups shown; do not choose best strategy using only pooled success.',
      'scope':'Korean requests/English tool definitions, empty arguments, authored check-then-act positive-Boolean structure. No skin-state extraction, STT, Qwen, real APIs, pretraining-novelty or general unknown90 claim. Shared template and small12 sample limit conclusions.',
      'stop':'One fixed comparison; no threshold/prompt/weight tuning after outcomes. Audit every executed operation and compare original source replay, report even if alternative candidate access harms stopping.'})
    print('V31 FROZEN:',len(scenarios),'scenarios x2, max_tokens',maximum,flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V31 frozen changed:'+rel)
    return p
if __name__=='__main__':prepare()
