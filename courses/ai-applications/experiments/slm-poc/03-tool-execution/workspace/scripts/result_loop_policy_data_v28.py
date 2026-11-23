"""Freeze fresh cases and two prespecified policies; no learning or cutoff search."""
import copy, itertools, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.result_loop_split_data_v27 import verify as previous_verify, OUT as V27, DATA as D27, MODEL, read,save,digest
from agent.result_loop_probe_v26 import STOP,Fixture
from agent.result_loop_split_v27 import selector_view,gate_view
DATA=ROOT/'data/processed/result-loop-policy-v28';OUT=ROOT/'output/diagnostics/result-loop-policy-v28'
SELECTOR=V27/'selector/final-adapter';GATE=V27/'gate/final-adapter';SEED=280020

def fresh_cases():
    specs=[
      ('archive','압축 파일이 손상되지 않았는지 검사해 줘. 정상일 때만 모의 압축 해제를 한 번 하고 손상됐으면 풀지 마.','inspect_mock_archive_integrity','extract_mock_archive','intact',False,'Check whether the current mock archive is intact.','Extract the current mock archive once, only in memory.'),
      ('membership','회원권이 활성 상태인지 알아본 다음, 활성 상태일 때만 가상 채널을 열어 줘. 비활성이면 열지 마.','inspect_virtual_membership','open_virtual_channel','active',False,'Check whether the current virtual membership is active.','Open the current virtual member channel once.'),
      ('wallet','가상 지갑에 결제할 잔액이 충분한지 먼저 확인해 줘. 충분하면 모의 결제를 한 번 하고 부족하면 결제하지 마.','inspect_virtual_wallet','pay_virtual_invoice','funds_sufficient',True,'Check whether the current virtual wallet has sufficient funds.','Pay the current virtual invoice once, without a real payment.'),
      ('barcode','이 바코드를 처리할 수 있는 형식인지 검사하고, 지원하는 형식일 때만 모의 해독을 한 번 해 줘. 지원하지 않으면 해독하지 마.','inspect_demo_barcode_format','decode_demo_barcode','supported',False,'Check whether the current demo barcode format is supported.','Decode the current demo barcode once.'),
      ('sensor','센서 표본이 유효한지 점검한 뒤, 유효한 표본일 때만 집계해 줘. 무효라면 집계하지 마.','validate_mock_sensor_sample','aggregate_mock_sensor_sample','sample_valid',False,'Check whether the current mock sensor sample is valid.','Aggregate the current mock sensor sample once.'),
      ('cache','캐시 값이 아직 유효한지 먼저 확인해 줘. 유효하면 한 번 보여 주고 만료됐으면 보여 주지 마.','inspect_mock_cache_freshness','show_mock_cached_value','fresh',False,'Check whether the current mock cached value is fresh.','Show the current mock cached value once.'),
      ('video','영상 코덱을 지원하는지 검사해 줘. 지원하면 시험 변환을 한 번 하고 지원하지 않으면 변환하지 마.','inspect_mock_video_codec','transcode_mock_video','codec_supported',False,'Check whether the codec of the current mock video is supported.','Transcode the current mock video once, without a real media file.'),
      ('signature','파일 서명이 신뢰할 수 있는지 검증한 뒤, 신뢰할 때만 가상 공간에 로드해 줘. 그렇지 않으면 로드하지 마.','verify_mock_file_signature','load_mock_signed_file','trusted',False,'Check whether the current mock file signature is trusted.','Load the current mock signed file once, in memory only.'),
      ('palette','색상 값이 허용 범위인지 먼저 검사해 줘. 범위 안이면 팔레트를 한 번 만들고 벗어나면 만들지 마.','validate_demo_color_range','create_demo_palette','in_range',False,'Check whether the current demo color values are in the allowed range.','Create the current demo palette once.'),
      ('invoice','가짜 청구서의 합계가 맞는지 검산해 줘. 맞으면 확인 표시를 한 번 하고 틀리면 표시하지 마.','verify_mock_invoice_total','mark_mock_invoice_checked','total_correct',False,'Check whether the total of the current fake invoice is correct.','Mark the current fake invoice as checked once.'),
      ('coordinates','좌표가 지도 범위 안에 있는지 검사해 줘. 안에 있을 때만 점을 한 번 그려 주고 밖이면 그리지 마.','inspect_demo_coordinate_bounds','plot_demo_coordinate','inside_bounds',False,'Check whether the current demo coordinate is inside the map bounds.','Plot the current demo coordinate once.'),
      ('schema','데이터 형식이 스키마와 맞는지 확인한 다음, 맞을 때만 요약을 한 번 만들어 줘. 맞지 않으면 요약하지 마.','validate_mock_dataset_schema','summarize_mock_dataset','schema_valid',False,'Check whether the current mock dataset matches its schema.','Summarize the current mock dataset once.'),
      ('game','게임 단계가 열려 있는지 확인해 줘. 열려 있으면 모의 플레이를 한 번 시작하고 잠겨 있으면 시작하지 마.','inspect_demo_level_access','start_demo_level','unlocked',False,'Check whether the current demo game level is unlocked.','Start the current demo game level once.'),
      ('queue','대기열에 자리가 있는지 먼저 확인해 줘. 있으면 시험 항목을 한 개 넣고 없으면 넣지 마.','inspect_mock_queue_capacity','enqueue_mock_item','slot_available',True,'Check whether the current mock queue has an available slot.','Enqueue the current mock item once.'),
      ('template','문서 양식의 변수가 다 채워졌는지 검사하고, 다 채워졌을 때만 한 번 렌더링해 줘. 빠진 값이 있으면 렌더링하지 마.','inspect_demo_template_values','render_demo_template','values_complete',False,'Check whether all values for the current demo template are complete.','Render the current demo template once.'),
      ('locker','물건이 보관함 크기에 맞는지 확인해 줘. 맞으면 모의 보관을 한 번 하고 맞지 않으면 보관하지 마.','inspect_mock_locker_fit','store_mock_parcel','fits',False,'Check whether the current mock parcel fits the current locker.','Store the current mock parcel once.'),
      ('volume','가상 저장 장치가 준비됐는지 먼저 확인해 줘. 준비됐을 때만 모의 연결을 한 번 하고 아니면 연결하지 마.','inspect_virtual_volume','mount_virtual_volume','ready',False,'Check whether the current virtual volume is ready.','Mount the current virtual volume once, without touching real storage.'),
      ('font','글꼴이 필요한 글자를 모두 지원하는지 검사해 줘. 지원하면 시험 문장을 한 번 그려 주고 아니면 그리지 마.','inspect_demo_font_coverage','draw_demo_text','glyphs_supported',False,'Check whether the current demo font supports all required glyphs.','Draw the current demo text once.'),
      ('license','가상 작업의 이용권이 유효한지 확인해 줘. 유효할 때만 작업을 한 번 시작하고 만료됐으면 시작하지 마.','inspect_virtual_job_license','start_virtual_licensed_job','license_valid',False,'Check whether the license for the current virtual job is valid.','Start the current virtual licensed job once.'),
      ('wavelength','파장 값이 장치의 시험 범위에 들어가는지 확인한 뒤, 범위 안일 때만 모의 측정을 한 번 해 줘. 밖이면 측정하지 마.','inspect_mock_wavelength_range','measure_mock_wavelength','within_range',False,'Check whether the current mock wavelength is within the test device range.','Measure the current mock wavelength once, without real hardware.'),
    ]
    rows=[]
    for i,(id_,request,check,act,pred,consumes,cd,ad) in enumerate(specs):
        params={'type':'object','properties':{},'required':[]}
        ct={'name':check,'description':cd+' Returns ok=true and '+pred+' as a boolean. It only observes and does not perform the requested follow-up action.','parameters':copy.deepcopy(params)}
        at={'name':act,'description':ad+' Requires the latest successful '+check+' result to have '+pred+'=true, and this task not already done. Returns ok=true and done=true. Otherwise returns an error without changing state.','parameters':copy.deepcopy(params)}
        order=[check,act,STOP];random.Random(SEED+i).shuffle(order)
        rows.append({'id':id_,'request':request,'check':ct,'act':at,'predicate':pred,'consumes_condition':consumes,'option_order':order})
    return rows

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V28 protected')
    for role in ['selector','gate']:
        if digest(V27/role/'final-adapter/adapter_model.safetensors')!=read(V27/role/'complete.json')['adapter_sha256']:raise ValueError('V27 output changed')
    fresh=fresh_cases();prior=read(D27/'known-cases.json')+read(D27/'fresh-cases.json')
    old_names={c[t]['name'] for c in prior for t in ['check','act']}
    fresh_names={c[t]['name'] for c in fresh for t in ['check','act']}
    adapted=__import__('json').dumps(read(D27/'selector-train.json')+read(D27/'gate-train.json'))
    if fresh_names&old_names or any(n in adapted for n in fresh_names):raise ValueError('Exact tool-name overlap')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;max_tokens=0
    for c in fresh+read(D27/'fresh-cases.json'):
        for truth in [True,False]:
            for size in range(3):
                for seq in itertools.product([c['check']['name'],c['act']['name']],repeat=size):
                    f=Fixture(c,truth)
                    for n in seq:f.invoke(n)
                    v=selector_view(c['request'],[c['check'],c['act']],f.events,c['option_order'])
                    for w in [v]+[gate_view(t,v['context']) for t in [c['check'],c['act']]]:
                        n=max(map(len,tok([w['question']+' '+x for x in w['options'].values()],[w['context']]*len(w['options']),truncation=False)['input_ids']));max_tokens=max(max_tokens,n)
    if max_tokens>512:raise ValueError('No truncation')
    from scripts.result_loop_split_data_v27 import oracle
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'fresh-cases.json',fresh);save(DATA/'previous-cases.json',read(D27/'fresh-cases.json'))
    save(DATA/'oracle.json',{k:{c['id']:oracle(c) for c in cs} for k,cs in [('fresh',fresh),('previous',read(D27/'fresh-cases.json'))]})
    paths=list(DATA.glob('*'))+[ROOT/p for p in ['agent/result_loop_policy_v28.py','scripts/result_loop_policy_data_v28.py','scripts/result_loop_policy_v28.py','scripts/report_result_loop_policy_v28.py','scripts/audit_result_loop_policy_v28.py','tests/test_result_loop_policy_v28.py']]
    paths += [V27/'both-fresh-snapshots.json',V27/'both-fresh-episodes.json',V27/'both-korean30.json']
    for path in [SELECTOR,GATE]:paths += [path/'adapter_model.safetensors',path/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'policies':['legacy','higher_score'],'seed':SEED,'fresh_cases':20,'max_tokens':max_tokens,
      'hypothesis':'Without weight or input changes, does replacing legacy margin>=-1.5 with yes>no decrease unnecessary execution without losing required progress?',
      'ties':'higher_score stops on exactly equal scores; legacy retains inclusive >=-1.5. Count ties explicitly.',
      'controls':'Same V27-final selector/gate weights, question, full tool definitions, raw scores for identical histories, order, real in-memory result delivery. Policies never appear in model input. No fallback or oracle routing. Both policies run their OWN complete loops, not pasted counterfactual continuations.',
      'evaluation':'New20 authored tasks with2 hidden conditions and4 observer states each. Previous12 are reference only; reproduce legacy previous12 input/score/choice/path outputs. Reuse fixed V27 Korean30 scores to compare single-decision policy retention, not autonomous loops. No old600 inference: unchanged selector weights cannot undo V27 selection regression.',
      'guard':'A positive signal requires fewer false-condition attempted followups and more strict episodes, with no loss of positive strict episodes or initial correct checking, and no loss of old Korean30 correct count. Report guards separately. No deployment or further threshold search.',
      'scope':'Korean requests, English tool definitions, empty arguments, two-tool check-then-act template, assistant-authored gold. Exact fresh names absent in V27 adaptation but not proof of pretraining novelty or all-domain unseen80-90 accuracy. No STT/Qwen/skin records or real external side effects.',
      'stop':'Run fixed comparison once, audit all traces and frozen weights, report. Do not train, change cutoffs, or select cases after seeing outcomes.'})
    print('V28 FROZEN:20 new pairs, two policies, no training, max_tokens',max_tokens,flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V28 changed:'+rel)
    return p

if __name__=='__main__':prepare()
