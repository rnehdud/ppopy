"""Freeze 20 fresh authored domains and explicit, provider-declared tool contracts."""
import copy,itertools,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.explicit_tools_data_v32 import DATA as D32,OUT as V32,MODEL,SELECTOR,GATE,contract,build_scenario,VARIANTS,oracle,verify as previous_verify,read,save,digest
from agent.candidate_loop_v31 import World,public_tools
from agent.result_loop_split_v27 import selector_view,gate_view
from agent.result_loop_probe_v26 import STOP,probe_states
DATA=ROOT/'data/processed/contract-filter-v34';OUT=ROOT/'output/diagnostics/contract-filter-v34';SEED=340020


def fresh_cases():
    specs=[
      ('audio','시험 소리의 최대 크기를 확인해 줘. 범위 안이면 한 번 정규화하고, 벗어나면 바꾸지 마.','inspect_mock_audio_peak','normalize_mock_audio','within_range','Check whether the mock audio peak is within range.','Normalize the mock audio once.'),
      ('columns','가상 표의 열 이름이 서로 다른지 확인해 줘. 다르면 요약을 한 번 만들고, 중복이면 만들지 마.','inspect_virtual_column_uniqueness','summarize_virtual_columns','unique','Check whether the mock table column names are unique.','Summarize the virtual table columns once.'),
      ('palette','시험 팔레트의 색 수가 허용 범위인지 확인해 줘. 맞으면 한 번 적용하고, 아니면 적용하지 마.','inspect_mock_palette_size','apply_mock_palette','size_allowed','Check whether the mock palette size is allowed.','Apply the mock palette once.'),
      ('glyphs','가상 글꼴에 필요한 글자가 있는지 확인해 줘. 다 있으면 견본을 한 번 그리고, 없으면 그리지 마.','inspect_virtual_font_glyphs','render_virtual_font_sample','glyphs_present','Check whether required glyphs are present in the virtual font.','Render the virtual font sample once.'),
      ('lighting','시험 장면의 조명 값이 유효한지 확인해 줘. 유효하면 모의 그림자를 한 번 만들고, 아니면 만들지 마.','inspect_mock_light_settings','build_mock_shadows','settings_valid','Check whether the mock scene light settings are valid.','Build the mock shadows once.'),
      ('mesh','가상 입체에 구멍이 없는지 검사해 줘. 없으면 부피를 한 번 구하고, 있으면 구하지 마.','inspect_virtual_mesh_seal','compute_virtual_mesh_volume','sealed','Check whether the virtual mesh is sealed.','Compute the virtual mesh volume once.'),
      ('polygon','시험 다각형이 닫혀 있는지 확인해 줘. 닫혔으면 내부를 한 번 채우고, 아니면 채우지 마.','inspect_mock_polygon_closure','fill_mock_polygon','closed','Check whether the mock polygon is closed.','Fill the mock polygon once.'),
      ('vectors','가상 벡터들의 차원이 같은지 확인해 줘. 같으면 한 번 더하고, 다르면 더하지 마.','inspect_virtual_vector_dimensions','add_virtual_vectors','dimensions_equal','Check whether the virtual vectors have equal dimensions.','Add the virtual vectors once.'),
      ('archive','시험 압축 자료의 색인이 읽히는지 확인해 줘. 읽히면 목록을 한 번 만들고, 아니면 만들지 마.','inspect_mock_archive_index','list_mock_archive_members','index_readable','Check whether the mock archive index is readable.','List the mock archive members once.'),
      ('dictionary','가상 사전에 필요한 항목이 있는지 확인해 줘. 있으면 한 번 조회하고, 없으면 조회하지 마.','inspect_virtual_dictionary_entry','lookup_virtual_dictionary','entry_exists','Check whether the required virtual dictionary entry exists.','Look up the virtual dictionary entry once.'),
      ('sudoku','시험 숫자판에 모순이 없는지 검사해 줘. 없으면 후보를 한 번 구하고, 있으면 구하지 마.','inspect_mock_number_grid','derive_mock_grid_candidates','consistent','Check whether the mock number grid is consistent.','Derive the mock grid candidates once.'),
      ('timetable','가상 시간표에 겹침이 없는지 확인해 줘. 없으면 한 번 배치하고, 있으면 배치하지 마.','inspect_virtual_timetable_overlap','arrange_virtual_timetable','no_overlap','Check whether the virtual timetable has no overlap.','Arrange the virtual timetable once.'),
      ('subtitles','시험 자막의 시간이 맞는지 확인해 줘. 맞으면 한 번 연결하고, 아니면 연결하지 마.','inspect_mock_subtitle_timing','join_mock_subtitles','synchronized','Check whether the mock subtitle timing is synchronized.','Join the mock subtitles once.'),
      ('canvas','가상 캔버스 크기가 유효한지 확인해 줘. 유효하면 시험 격자를 한 번 그리고, 아니면 그리지 마.','inspect_virtual_canvas_size','draw_virtual_grid','size_valid','Check whether the virtual canvas size is valid.','Draw the virtual grid once.'),
      ('matrix','시험 행렬이 역행렬을 갖는지 확인해 줘. 가지면 한 번 구하고, 아니면 구하지 마.','inspect_mock_matrix_invertibility','invert_mock_matrix','invertible','Check whether the mock matrix is invertible.','Invert the mock matrix once.'),
      ('timezone','가상 시간의 시간대가 알려져 있는지 확인해 줘. 알면 한 번 변환하고, 모르면 변환하지 마.','inspect_virtual_time_zone','shift_virtual_time','zone_known','Check whether the virtual time zone is known.','Shift the virtual time once.'),
      ('checksum','시험 자료의 검증값이 맞는지 확인해 줘. 맞으면 한 번 가져오고, 아니면 가져오지 마.','inspect_mock_data_checksum','import_mock_data','checksum_matches','Check whether the mock data checksum matches.','Import the mock data once.'),
      ('puzzle','가상 퍼즐의 끝에 도달할 수 있는지 확인해 줘. 가능하면 경로를 한 번 그리고, 아니면 그리지 마.','inspect_virtual_puzzle_reachability','trace_virtual_puzzle_path','reachable','Check whether the virtual puzzle goal is reachable.','Trace the virtual puzzle path once.'),
      ('locale','시험 화면의 언어 자료가 있는지 확인해 줘. 있으면 한 번 바꾸고, 없으면 바꾸지 마.','inspect_mock_locale_resources','switch_mock_display_locale','resources_present','Check whether the mock locale resources are present.','Switch the mock display locale once.'),
      ('chart','가상 차트의 값이 모두 음수가 아닌지 확인해 줘. 맞으면 누적 차트를 한 번 그리고, 아니면 그리지 마.','inspect_virtual_chart_values','draw_virtual_stacked_chart','nonnegative','Check whether all virtual chart values are nonnegative.','Draw the virtual stacked chart once.'),
    ];cs=[]
    for id_,req,ch,ac,pred,cd,ad in specs:
        ct,at=contract(ch,ac,pred,cd,ad);params=ct['parameters']
        extras=[{'name':'utility_clock_'+id_,'description':'Return the current UTC time of a separate mock server. Read-only; does not change task state.','parameters':copy.deepcopy(params),'mock_kind':'clock'},
          {'name':'utility_note_'+id_,'description':'Append the default demo text to a separate scratchpad. Returns ok=true and note_saved=true.','parameters':copy.deepcopy(params),'mock_kind':'note'}]
        cs.append({'id':id_,'request':req,'check':ct,'act':at,'predicate':pred,'consumes_condition':False,'extras':extras})
    return cs


def attach_contracts(s):
    s=copy.deepcopy(s);c=s['case']
    # Provider-authored metadata: neither truth, seed_done, oracle nor world state used.
    ch=c['check']['name'];ac=c['act']['name'];pred=c['predicate']
    contracts={ch:{'requires':[],'not_after':[]},ac:{'requires':[{'tool':ch,'arguments':{},'field':pred,'equals':True}],
      'not_after':[{'tool':ac,'arguments':{},'field':'done','equals':True}]}}
    for t in s['tools']:t['execution_contract']=copy.deepcopy(contracts.get(t['name'],{'requires':[],'not_after':[]}))
    return s


def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V34 protected')
    cs=fresh_cases();oldnames={t['name'] for s in read(D32/'scenarios.json') for t in s['tools']};newnames={c[k]['name'] for c in cs for k in ['check','act']}
    if len(cs)!=20 or len(newnames)!=40 or oldnames&newnames:raise ValueError('Fresh task names')
    scenarios=[];probes=[]
    for i,c in enumerate(cs):
        for variant in VARIANTS:
            for truth in ([True] if variant.startswith('completed') else [True,False]):
                s=build_scenario(c,variant,truth,i,'fresh');order=s['option_order'];random.Random(SEED+i*20+VARIANTS.index(variant)).shuffle(order);scenarios.append(attach_contracts(s))
        s=attach_contracts(build_scenario(c,'plain',True,i,'fresh'))
        for state,ev in probe_states(c).items():
            target=c['check']['name'] if state=='initial' else c['act']['name'] if state=='after_true' else STOP
            probes.append({'id':c['id']+':'+state,'case_id':c['id'],'state':state,'request':c['request'],'tools':s['tools'],'option_order':s['option_order'],'events':ev,'target':target})
    for old in read(D32/'scenarios.json'):
        if old['cohort']=='fresh':
            s=copy.deepcopy(old);s['cohort']='reference';s['id']='reference:'+s['case']['id']+':'+s['variant']+':'+str(s['condition']);scenarios.append(attach_contracts(s))
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;maximum=0
    def check(v):
        nonlocal maximum
        maximum=max(maximum,max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids'])))
    for s in scenarios:
        ts=public_tools(s['tools'])
        for n in range(s['decision_budget']):
            for seq in itertools.product([t['name'] for t in ts],repeat=n):
                w=World(s)
                for name in seq:w.invoke(name)
                v=selector_view(s['case']['request'],ts,w.events,s['option_order']);check(v)
                for t in ts:check(gate_view(t,v['context']))
    if maximum>512:raise ValueError(('No truncation, no rewriting after scores',maximum))
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    save(DATA/'scenarios.json',scenarios);save(DATA/'probes.json',probes);save(DATA/'oracle.json',{s['id']:oracle(s) for s in scenarios})
    sources=['agent/contract_filter_v34.py','scripts/contract_filter_data_v34.py','scripts/contract_filter_v34.py','scripts/report_contract_filter_v34.py','scripts/audit_contract_filter_v34.py','tests/test_contract_filter_v34.py']
    paths=list(DATA.glob('*'))+[ROOT/p for p in sources]
    for p in [SELECTOR,GATE]:paths += [p/'adapter_model.safetensors',p/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'strategies':['baseline','contract_filter'],'threshold':-1.5,'max_tokens':maximum,
      'counts':{'fresh_families':20,'fresh_probes':80,'fresh_scenarios':240,'reference_scenarios':144,'episodes_total':768},
      'design':'Same frozen V27 selector/V29-control gate, full descriptions, old cutoff and actual histories. Baseline is V32 all_candidates, NOT top1. Gate and rank all candidates to log raw proposal; filter declared-ineligible candidates before final argmax only. Independent scalar scoring: schema metadata not added to encoder prompts; no changed question, training, threshold tuning, automatic prerequisite routing or global-goal termination.',
      'contracts':'New provider-declared metadata references exact tool+arguments and literal Boolean return fields. Latest matching evidence must be successful; unknown differs from false. Successful same-operation done is task-bound completion, not any tool done. Read-only checks/extras stay eligible. No timestamps, external invalidation, nonempty args or arbitrary precondition language supported by this evaluation.',
      'scope':'20 newly authored Korean tasks, English full tools, zero arguments, same check/positive-Boolean/act-once template. 80 probes and 240 variants are NOT independent tasks, not human-reviewed gold or proof of general unknown-domain90. Reference12 V32 tasks kept separate. Mock only, no real files/APIs, Qwen/STT or demo changes.',
      'adoption_guard':'Fresh plain strict and positive execution improve, no increase actual false-condition followup attempts, unrelated calls or repeats across plain/distracted/renamed; missing-tool and completed strict cannot worsen. Do not count filtered raw mistakes as model accuracy. No deployment even if guards pass.',
      'stop':'One fixed comparison, report failures. No post-score prompt/data/weight/threshold tuning. Any subsequent experiment is a new version.'})
    print('V34 FROZEN',len(scenarios),'scenarios x2 +',len(probes),'probes x2; max',maximum,flush=True)


def verify():
    previous_verify();cfg=read(DATA/'protocol.json')
    for rel,h in cfg['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V34 frozen changed: '+rel)
    return cfg
if __name__=='__main__':prepare()
