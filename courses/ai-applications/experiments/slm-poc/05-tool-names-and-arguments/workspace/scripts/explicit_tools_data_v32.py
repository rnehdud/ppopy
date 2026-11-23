"""Detailed tool contracts retained. Fresh evaluation separate from known V31 probes."""
import copy,itertools,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.candidate_loop_data_v31 import DATA as D31,OUT as V31,SELECTOR,GATE,MODEL,VARIANTS,scenario,oracle,verify as previous_verify,read,save,digest
from scripts.gate_pair_data_v29 import D27,D28,DATA as D29
from agent.candidate_loop_v31 import World,public_tools
from agent.result_loop_split_v27 import selector_view,gate_view
from agent.result_loop_probe_v26 import STOP
DATA=ROOT/'data/processed/explicit-tools-v32';OUT=ROOT/'output/diagnostics/explicit-tools-v32';SEED=320012

def contract(check,act,predicate,check_description,act_description):
    params={'type':'object','properties':{},'required':[]}
    return ({'name':check,'description':check_description+' Returns ok=true and '+predicate+' as a boolean. It only observes and does not perform the requested follow-up action.','parameters':copy.deepcopy(params)},
      {'name':act,'description':act_description+' Requires the latest successful '+check+' result to have '+predicate+'=true, and this task not already done. Returns ok=true and done=true. Otherwise returns an error without changing state.','parameters':copy.deepcopy(params)})

def fresh_cases():
    specs=[
      ('profile','색상 프로필이 호환되는지 먼저 확인해 줘. 호환될 때만 가상 그림을 한 번 변환하고, 아니면 변환하지 마.','inspect_virtual_color_profile','convert_virtual_picture','compatible',False,'Check whether the current virtual color profile is compatible.','Convert the current virtual picture once.'),
      ('snapshot','시험 스냅샷이 정상인지 먼저 검사해 줘. 정상일 때만 모의 복원을 한 번 하고, 손상됐으면 복원하지 마.','inspect_mock_snapshot_health','restore_mock_snapshot','healthy',False,'Check whether the current mock snapshot is healthy.','Restore the current mock snapshot once, in memory only.'),
      ('attachment','첨부 파일을 넣을 공간이 있는지 확인해 줘. 공간이 있을 때만 가짜 첨부를 한 번 넣고, 없으면 넣지 마.','inspect_virtual_attachment_quota','store_virtual_attachment','space_available',True,'Check whether space is available for the current virtual attachment.','Store the current virtual attachment once.'),
      ('anchors','문서의 제목 연결이 유효한지 먼저 검사해 줘. 유효할 때만 시험 목차를 한 번 만들고, 아니면 만들지 마.','inspect_mock_heading_anchors','generate_mock_contents','anchors_valid',False,'Check whether the current mock document heading anchors are valid.','Generate the current mock table of contents once.'),
      ('calendar','월간 자료가 다 준비됐는지 확인해 줘. 다 준비됐으면 가상 달력을 한 번 그리고, 부족하면 그리지 마.','inspect_virtual_month_data','draw_virtual_calendar','complete',False,'Check whether the current virtual month data is complete.','Draw the current virtual calendar once.'),
      ('browser','시험 페이지가 로드됐는지 먼저 확인해 줘. 로드됐을 때만 가짜 화면 캡처를 한 번 만들고, 아니면 만들지 마.','inspect_mock_page_load','capture_mock_page','loaded',False,'Check whether the current mock page has loaded.','Capture the current mock page once, without a real browser.'),
      ('weights','가상 그래프의 가중치가 조건에 맞는지 검사해 줘. 맞을 때만 모의 최단 경로를 한 번 구하고, 아니면 구하지 마.','inspect_virtual_graph_weights','compute_virtual_shortest_path','weights_valid',False,'Check whether weights in the current virtual graph satisfy the required condition.','Compute the current virtual shortest path once.'),
      ('board','시험 말이 움직여도 되는지 먼저 확인해 줘. 가능할 때만 가상 보드에서 한 번 움직이고, 불가능하면 움직이지 마.','inspect_virtual_board_move','perform_virtual_board_move','move_allowed',True,'Check whether the current virtual board move is allowed.','Perform the current virtual board move once.'),
      ('certificate','가짜 인증서가 유효한지 먼저 확인해 줘. 유효하면 모의 문서에 한 번 붙이고, 아니면 붙이지 마.','inspect_mock_certificate_validity','attach_mock_certificate','valid',False,'Check whether the current mock certificate is valid.','Attach the current mock certificate once.'),
      ('units','단위 변환에 필요한 정보가 있는지 확인해 줘. 있으면 시험 값을 한 번 변환하고, 없으면 변환하지 마.','inspect_mock_unit_metadata','convert_mock_measurement','metadata_available',False,'Check whether the metadata needed for the current mock unit conversion is available.','Convert the current mock measurement once.'),
      ('rotation','가상 부품이 회전할 공간이 있는지 먼저 확인해 줘. 공간이 있을 때만 한 번 회전시키고, 없으면 회전시키지 마.','inspect_virtual_rotation_space','rotate_virtual_component','rotation_clear',False,'Check whether space is clear for the current virtual component rotation.','Rotate the current virtual component once.'),
      ('session','가상 세션이 유효한지 먼저 확인해 줘. 유효할 때만 시험 결과를 한 번 저장하고, 만료됐으면 저장하지 마.','inspect_virtual_session_validity','save_virtual_trial_result','session_valid',False,'Check whether the current virtual session is valid.','Save the current virtual trial result once.'),
    ];rows=[]
    for id_,req,check,act,pred,consumes,cd,ad in specs:
        ct,at=contract(check,act,pred,cd,ad);params=ct['parameters']
        extras=[{'name':'utility_clock_'+id_,'description':'Return the current UTC time of a separate mock server. Read-only; does not change task state.','parameters':copy.deepcopy(params),'mock_kind':'clock'},
          {'name':'utility_note_'+id_,'description':'Append the default demo text to a separate scratchpad. Returns ok=true and note_saved=true.','parameters':copy.deepcopy(params),'mock_kind':'note'}]
        rows.append({'id':id_,'request':req,'check':ct,'act':at,'predicate':pred,'consumes_condition':consumes,'extras':extras})
    return rows

def build_scenario(case,variant,truth,index,cohort):
    s=scenario(case,variant,truth,index,'fresh');s['cohort']=cohort;s['id']=cohort+':'+case['id']+':'+variant+':'+str(truth)
    order=[t['name'] for t in s['tools']]+[STOP];random.Random(SEED+index*20+VARIANTS.index(variant)).shuffle(order);s['option_order']=order
    s['decision_budget']=1 if s['seed_done'] else 3
    return s

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V32 protected')
    style_plan=read(V31/'input-style-plan.json')
    for rel,h in style_plan['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V31 style source changed')
    refs=[p['scenario'] for p in read(V31/'input-style-probes.json') if p['request_style']=='compact' and p['tool_style']=='detailed']
    fresh=fresh_cases();old=[]
    for path,name in [(D27,'known-cases.json'),(D27,'fresh-cases.json'),(D28,'fresh-cases.json'),(D29,'fresh-cases.json')]:old+=read(path/name)
    old+=[s['case'] for s in read(D31/'scenarios.json') if s['cohort']=='fresh' and s['variant']=='plain' and s['condition']]
    oldnames={c[k]['name'] for c in old for k in ['check','act']};newnames={c[k]['name'] for c in fresh for k in ['check','act']}
    if oldnames&newnames or len(fresh)!=12 or len(refs)!=12:raise ValueError('Name/count mismatch')
    scenarios=[]
    for i,c in enumerate(fresh):
        for variant in VARIANTS:
            for truth in ([True] if variant.startswith('completed') else [True,False]):scenarios.append(build_scenario(c,variant,truth,i,'fresh'))
    for i,r in enumerate(refs):
        for variant in ['plain','completed']:
            for truth in ([True] if variant=='completed' else [True,False]):
                s=build_scenario(r['case'],variant,truth,i,'reference')
                if variant=='plain':s['option_order']=r['option_order'][:]
                scenarios.append(s)
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;maximum=0;largest=None
    def length(v):return max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
    for s in scenarios:
        ts=public_tools(s['tools'])
        for n in range(s['decision_budget']):
            for seq in itertools.product([t['name'] for t in ts],repeat=n):
                w=World(s)
                for name in seq:w.invoke(name)
                v=selector_view(s['case']['request'],ts,w.events,s['option_order'])
                for label,x in [('selector',v)]+[(t['name'],gate_view(t,v['context'])) for t in ts]:
                    size=length(x)
                    if size>maximum:maximum=size;largest={'scenario':s['id'],'history':seq,'candidate':label,'tokens':size}
    if maximum>512:raise ValueError(('No truncation; do not shorten contracts',largest))
    assert len(scenarios)==180
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'scenarios.json',scenarios);save(DATA/'oracle.json',{s['id']:oracle(s) for s in scenarios})
    paths=list(DATA.glob('*'))+[ROOT/p for p in ['scripts/explicit_tools_data_v32.py','scripts/explicit_tools_v32.py','scripts/report_explicit_tools_v32.py','scripts/audit_explicit_tools_v32.py','tests/test_explicit_tools_v32.py']]
    paths += [V31/'input-style-probes.json',V31/'input-style-results.json',V31/'input-style-plan.json']
    for p in [SELECTOR,GATE]:paths += [p/'adapter_model.safetensors',p/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'strategies':['top1','all_candidates'],'threshold':-1.5,'max_tokens':maximum,
      'counts':'Fresh12 families x144 scenarios and known12 families x36 reference scenarios =180 per strategy,360 runs. Completed tests use one decision after actual seeded check+act; all other runs use up to3 decisions. Variants dependent; not180 independent tasks.',
      'controls':'Same fixed selector and V29-control gate, full question/options/context, candidate order and cutoff; only gating top1 versus all differs. NO learning or prompt/cutoff tuning after scores. Full natural-language effect, prerequisite and success/failure descriptions kept. No semantic rule compaction or input truncation.',
      'reference':'V31 post-hoc detailed-tool/compact-request12 FIRST-decision inputs and scores rechecked, then actual full loops. These12 are already seen reference only. NEW12 primary, all detailed descriptions from first construction.',
      'budget':'Completed task only asks whether NEXT decision is STOP. If any tool chosen, execute it, record stopped=False and FAIL at budget1; never count harness cutoff as AI stopping. This removes irrelevant further post-failure histories from context budget without deleting observed history or shortening contracts. Normal task budget3 supports check->act->stop.',
      'timing':'No memoized scores, warmup2forwards excluded; alternate strategy order per scenario. Logical calls and observed warm decision latency, not production latency benchmark.',
      'adoption_guard':'Fresh plain strict and positive execution improve, with no increase in negative followup attempts, unrelated calls, or repeats for plain/distracted/renamed. Missing-tool proper stop counts and completed stop counts must not decrease. Show every variant; no deployment regardless.',
      'scope':'Authored Korean12 new requests, English detailed tools, two functional tools plus distractors, zero arguments, positive-Boolean conditional template. Not independent human gold, real APIs, skincare/STT/Qwen evaluation or general unseen-domain90 proof. No unsupported claim that initial12/12 implies full success.',
      'stop':'One fixed run, verify every operation and first-decision replay, report enough to decide. Do not rewrite descriptions again after outcomes or select a winning prompt/threshold on these tasks.'})
    print('V32 FROZEN:',len(scenarios),'scenarios x2; full contracts retained; max_tokens',maximum,flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V32 frozen changed:'+rel)
    return p
if __name__=='__main__':prepare()
