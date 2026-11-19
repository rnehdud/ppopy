"""Matched-data CE control versus CE+within-tool counterfactual ranking."""
import copy,itertools,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.result_loop_policy_data_v28 import verify as previous_verify,DATA as D28,V27,D27,SELECTOR,GATE,MODEL,read,save,digest
from agent.result_loop_probe_v26 import STOP,Fixture,probe_states
from agent.result_loop_split_v27 import selector_view,gate_view
DATA=ROOT/'data/processed/gate-pair-v29';OUT=ROOT/'output/diagnostics/gate-pair-v29';SEED=290016

def fresh_cases():
    specs=[
      ('writable','문서를 수정할 수 있는지 먼저 검사해 줘. 수정 가능할 때만 시험 문구를 한 번 덧붙이고 아니면 덧붙이지 마.','inspect_virtual_document_writable','append_virtual_test_text','writable',False,'Check whether the current virtual document is writable.','Append the current test text once to the virtual document.'),
      ('bookmark','대상 페이지에 접근할 수 있는지 확인해 줘. 접근 가능할 때만 가짜 북마크를 저장하고 아니면 저장하지 마.','inspect_mock_bookmark_target','save_mock_bookmark','reachable',False,'Check whether the current mock bookmark target is reachable.','Save the current mock bookmark once.'),
      ('worker','가상 작업자에게 여유가 있는지 확인한 다음, 여유가 있을 때만 시험 작업을 한 번 배정해 줘. 아니면 배정하지 마.','inspect_virtual_worker_capacity','assign_virtual_task','capacity_free',True,'Check whether the current virtual worker has free capacity.','Assign the current virtual task once.'),
      ('rights','자료의 공개 권한이 있는지 먼저 확인해 줘. 권한이 있을 때만 가상 공개 처리를 한 번 하고 없으면 공개하지 마.','inspect_mock_asset_rights','publish_mock_asset','rights_granted',False,'Check whether publication rights are granted for the current mock asset.','Publish the current mock asset once, without a real publication.'),
      ('puzzle','퍼즐의 조건들이 서로 모순되지 않는지 검사하고, 모순이 없을 때만 모의 풀이를 한 번 해 줘. 모순되면 풀지 마.','inspect_demo_puzzle_consistency','solve_demo_puzzle','consistent',False,'Check whether the current demo puzzle constraints are consistent.','Solve the current demo puzzle once.'),
      ('playlist','재생 목록에 곡이 있는지 확인해 줘. 곡이 있으면 가상 미리듣기를 한 번 시작하고 비어 있으면 시작하지 마.','inspect_virtual_playlist_tracks','preview_virtual_playlist','has_tracks',False,'Check whether the current virtual playlist contains tracks.','Start one virtual playlist preview, without real audio playback.'),
      ('mesh','입체 모형의 표면이 닫혀 있는지 먼저 검사해 줘. 닫혀 있을 때만 부피를 한 번 계산하고 아니면 계산하지 마.','inspect_demo_mesh_closure','compute_demo_mesh_volume','closed',False,'Check whether the current demo mesh is closed.','Compute the current demo mesh volume once.'),
      ('keys','테이블의 키가 중복되지 않는지 검사한 뒤, 중복이 없을 때만 가상 색인을 한 번 만들어 줘. 중복되면 만들지 마.','inspect_mock_table_keys','index_mock_table','keys_unique',False,'Check whether keys in the current mock table are unique.','Create one index for the current mock table.'),
      ('compressor','시험 압축기를 쓸 수 있는지 확인하고, 쓸 수 있을 때만 가짜 자료를 한 번 압축해 줘. 쓸 수 없으면 압축하지 마.','inspect_mock_compressor','compress_mock_payload','available',False,'Check whether the current mock compressor is available.','Compress the current mock payload once.'),
      ('locale','번역 문구가 모두 준비됐는지 확인해 줘. 다 준비됐을 때만 해당 언어 화면을 한 번 그리고 빠진 문구가 있으면 그리지 마.','inspect_demo_locale_resources','render_demo_locale','resources_complete',False,'Check whether all resources for the current demo locale are complete.','Render the current demo locale view once.'),
      ('timezone','시간대가 알려져 있는지 먼저 확인해 줘. 알려져 있을 때만 가상 시각을 한 번 변환하고 모르면 변환하지 마.','inspect_virtual_timezone','convert_virtual_timestamp','timezone_known',False,'Check whether the timezone for the current virtual timestamp is known.','Convert the current virtual timestamp once.'),
      ('kettle','가상 주전자에 물이 충분한지 확인해 줘. 충분하면 모의 가열을 한 번 시작하고 부족하면 시작하지 마.','inspect_virtual_kettle_water','heat_virtual_kettle','water_sufficient',False,'Check whether the current virtual kettle has sufficient water.','Start one virtual kettle heating task, without real hardware.'),
      ('encoding','문자열이 UTF-8 규칙에 맞는지 검사하고, 맞으면 모의 디코딩을 한 번 해 줘. 규칙에 맞지 않으면 디코딩하지 마.','inspect_mock_utf8','decode_mock_utf8','encoding_valid',False,'Check whether the current mock byte string is valid UTF-8.','Decode the current mock byte string once.'),
      ('path','가상 경로의 노드가 모두 연결돼 있는지 검사해 줘. 연결됐을 때만 경로를 한 번 시뮬레이션하고 끊겼으면 하지 마.','inspect_virtual_path_connectivity','simulate_virtual_path','connected',False,'Check whether all nodes on the current virtual path are connected.','Simulate the current virtual path once.'),
      ('layers','시험 그림의 아래층이 말랐는지 확인한 뒤, 말랐을 때만 덧칠을 한 번 해 줘. 아직 젖어 있으면 덧칠하지 마.','inspect_demo_paint_layers','overlay_demo_paint','dry',False,'Check whether the lower layers of the current demo painting are dry.','Overlay paint on the current demo painting once.'),
      ('counter','가상 카운터를 더 올려도 되는지 먼저 확인해 줘. 한도가 남아 있으면 한 번만 올리고 남아 있지 않으면 올리지 마.','inspect_virtual_counter_limit','increment_virtual_counter','increment_allowed',True,'Check whether one increment is allowed by the current virtual counter limit.','Increment the current virtual counter once.'),
    ]
    rows=[]
    for i,(id_,req,check,act,pred,consumes,cd,ad) in enumerate(specs):
        params={'type':'object','properties':{},'required':[]}
        ct={'name':check,'description':cd+' Returns ok=true and '+pred+' as a boolean. It only observes and does not perform the requested follow-up action.','parameters':copy.deepcopy(params)}
        at={'name':act,'description':ad+' Requires the latest successful '+check+' result to have '+pred+'=true, and this task not already done. Returns ok=true and done=true. Otherwise returns an error without changing state.','parameters':copy.deepcopy(params)}
        order=[check,act,STOP];random.Random(SEED+i).shuffle(order)
        rows.append({'id':id_,'request':req,'check':ct,'act':at,'predicate':pred,'consumes_condition':consumes,'option_order':order})
    return rows

def pair_indices(rows,cases):
    ids={r['id']:i for i,r in enumerate(rows)};pairs=[]
    for c in cases:
        a=ids[c['id']+':after_true:'+c['act']['name']];b=ids[c['id']+':after_false:'+c['act']['name']]
        x,y=rows[a],rows[b]
        if x['target']!='yes' or y['target']!='no' or x['question']!=y['question'] or x['options']!=y['options']:raise ValueError('Pair labels or tool mismatch')
        true_events=probe_states(c)['after_true'];false_events=probe_states(c)['after_false'];fix=copy.deepcopy(false_events);fix[0]['result'][c['predicate']]=True
        if fix!=true_events:raise ValueError('More than Boolean changed')
        pairs.append({'case_id':c['id'],'true_index':a,'false_index':b})
    return pairs

def schedule(n,pairs,epoch):
    rng=random.Random(SEED+epoch);ps=pairs.copy();rng.shuffle(ps);paired={p[k] for p in ps for k in ['true_index','false_index']}
    rest=[i for i in range(n) if i not in paired];rng.shuffle(rest)
    groups=[]
    for j in range(0,len(ps),2):groups.append([p[k] for p in ps[j:j+2] for k in ['true_index','false_index']])
    groups += [rest[j:j+4] for j in range(0,len(rest),4)];rng.shuffle(groups)
    assert sorted(i for g in groups for i in g)==list(range(n)) and len(groups)==18 and all(len(g)==4 for g in groups)
    return groups

def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists():raise FileExistsError('V29 protected')
    rows=read(D27/'gate-train.json');known=read(D27/'known-cases.json');trainids=set(read(D27/'protocol.json')['train_case_ids']);train=[c for c in known if c['id'] in trainids];pairs=pair_indices(rows,train)
    fresh=fresh_cases();previous=read(D28/'fresh-cases.json');prior=known+read(D27/'fresh-cases.json')+previous
    oldnames={c[k]['name'] for c in prior for k in ['check','act']};newnames={c[k]['name'] for c in fresh for k in ['check','act']}
    if oldnames&newnames or len(fresh)!=16 or len(newnames)!=32:raise ValueError('Fresh name overlap/count')
    if any(n in __import__('json').dumps(rows) for n in newnames):raise ValueError('Fresh name in training')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;max_tokens=0
    def length(v):return max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
    for r in rows:max_tokens=max(max_tokens,length(r))
    for c in fresh+previous:
        for truth in [True,False]:
            for size in range(3):
                for seq in itertools.product([c['check']['name'],c['act']['name']],repeat=size):
                    f=Fixture(c,truth)
                    for n in seq:f.invoke(n)
                    v=selector_view(c['request'],[c['check'],c['act']],f.events,c['option_order']);max_tokens=max(max_tokens,length(v),*(length(gate_view(t,v['context'])) for t in [c['check'],c['act']]))
    if max_tokens>512:raise ValueError('No truncation')
    for epoch in range(1,11):schedule(len(rows),pairs,epoch)
    from scripts.result_loop_split_data_v27 import oracle
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for name,x in [('train.json',rows),('pairs.json',pairs),('fresh-cases.json',fresh),('previous-cases.json',previous)]:save(DATA/name,x)
    save(DATA/'oracle.json',{k:{c['id']:oracle(c) for c in cs} for k,cs in [('fresh',fresh),('previous',previous)]})
    paths=list(DATA.glob('*'))+[ROOT/p for p in ['scripts/gate_pair_data_v29.py','scripts/gate_pair_v29.py','scripts/report_gate_pair_v29.py','scripts/audit_gate_pair_v29.py','tests/test_gate_pair_v29.py']]
    paths += [D27/'gate-train.json',V27/'gate/own-epoch-10.json',V27/'both-korean30.json',D28/'fresh-cases.json']
    for p in [SELECTOR,GATE]:paths += [p/'adapter_model.safetensors',p/'adapter_config.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'arms':{'control':0.0,'paired':0.5},'epochs':10,'lr':1e-4,'batch':4,'steps':180,'rows':72,'pairs':6,'pair_gap':1.0,'read_epochs':[0,1,10],'policies':['legacy','higher_score'],'primary_policy':'legacy','max_tokens':max_tokens,
      'hypothesis':'With frozen selector, does CE+same-tool opposite-result ranking outperform matched CE-only control on new result-conditioned decisions and loops?',
      'training':'Both independently start from V27 final gate, not original pre-V27 gate. EXACT same72 rows, same grouped schedule and72 input exposures/epoch,180 updates,720 total rows. Groups contain complete true/false pairs in BOTH arms. Each row scored once per update. Both compute the same pair term from those logits; only its weight differs. Loss=mean per-row binary CE + weight*mean softplus(1-(m_true-m_false)) for pairs present in that group. No ranking term for no/no labels. Six distinct training requests, not72 independent requests.',
      'controls':'Same questions/options/JSON/context, NF4FP16 query/value LoRA only, dropout, seed, optimizer, clip, replay24 and48 new-state rows. Selector V27-final held unchanged. No new source data, prompt, threshold or checkpoint selection.',
      'evaluation':'Both final adapters fixed before new16 scoring. before/control/paired; direct same-followup-tool gate probes at true/false (ordering and both-sign correctness), four normal pipeline observer states, and autonomous two-condition loops. Previous20 from V28 are reference only. Both old legacy -1.5 and higher-score>0 policies frozen, legacy PRIMARY; no best-policy selection. Korean30 fixed-selector cached proposal inputs re-scored by each gate; report required-call and no-call separately. Selector600 not rerun because frozen; V27 selection regression remains unresolved.',
      'positive_signal':'Paired must exceed control in both-correct direct tool-result pairs at primary policy and strict autonomous episodes, without reducing positive task execution, increasing negative followup attempts, or reducing Korean required-call/no-call correct counts. Larger average gap or training accuracy alone is insufficient. No automatic deployment.',
      'scope':'Small assistant-authored16 tasks, Korean requests/English definitions, shared check-then-act positive-Boolean template, empty arguments. Exact names absent in adaptation/prior task sets, not global pretraining novelty or unknown-domain90 accuracy. No real effects, STT, Qwen, or skin-state extraction.',
      'stop':'One seed and budget, fit readouts only; score new final tests once. If not improved, report failure of this setup, not impossibility of every paired-learning method. No further tuning this run.'})
    print('V29 FROZEN:72 common rows,6 opposite-result pairs,180 updates/arm,new16 tasks,max_tokens',max_tokens,flush=True)

def verify():
    previous_verify();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V29 changed:'+rel)
    return p
if __name__=='__main__':prepare()
