"""Freeze tiny paired training and distinct tool tasks, before model inference."""
import copy, itertools, random, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.result_loop_data_v26 import verify as previous_verify, DATA as V26, read, save, digest
from scripts.selector_interface_data_v18 import MODEL, SELECTOR, view
from scripts.tool_split_data_v1 import gate_view as legacy_gate
from scripts.result_loop_data_v26 import cases as known_cases
from agent.result_loop_probe_v26 import Fixture, probe_states, STOP
from agent.result_loop_split_v27 import selector_view, gate_view

DATA = ROOT / 'data/processed/result-loop-split-v27'
OUT = ROOT / 'output/diagnostics/result-loop-split-v27'
LATEST = ROOT / 'output/diagnostics/selector-transfer-v24/new/final-adapter'
GATE = ROOT / 'output/training/tool-split-pilot-v1/gate_adapter'
SEED = 270012
TRAIN_IDS = {'stock', 'room', 'service', 'permission', 'seat', 'package'}


def readlines(path):
    return [__import__('json').loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x]


def fresh_cases():
    specs = [
      ('paper', '용지가 들어 있는지 먼저 확인해 줘. 들어 있으면 표를 한 번 인쇄하고 없으면 인쇄하지 마.', 'inspect_demo_paper_feed', 'print_demo_ticket', 'paper_loaded', False, 'Check whether paper is loaded in the current mock printer.', 'Print the current demo ticket once.'),
      ('coupon', '쿠폰을 쓸 수 있는지 확인한 다음, 쓸 수 있을 때만 한 번 사용해 줘. 쓸 수 없으면 사용하지 마.', 'inspect_demo_coupon', 'redeem_demo_coupon', 'eligible', True, 'Check whether the current demo coupon is eligible for redemption.', 'Redeem the current demo coupon once.'),
      ('entry', '입장권이 유효한지 먼저 확인해 줘. 유효하면 모의 입장을 한 번 처리하고 아니면 입장 처리하지 마.', 'verify_demo_entry_pass', 'admit_demo_guest', 'ticket_valid', True, 'Check whether the current mock entry pass is valid.', 'Process one mock admission for the current guest.'),
      ('soil', '흙에 물이 필요한지 확인해 줘. 필요할 때만 모의 물주기를 한 번 하고 필요 없으면 하지 마.', 'inspect_demo_soil', 'water_demo_seedling', 'needs_water', True, 'Check whether the current mock seedling needs water.', 'Water the current mock seedling once.'),
      ('image', '이미지를 읽을 수 있는지 검사하고, 읽을 수 있을 때만 미리보기 그림을 한 번 만들어 줘. 아니면 만들지 마.', 'validate_demo_image', 'create_demo_thumbnail', 'decodable', False, 'Check whether the current demo image can be decoded.', 'Create one thumbnail for the current demo image.'),
      ('chess', '체스판 배치가 규칙에 맞는지 확인해 줘. 맞으면 한 번 분석하고 맞지 않으면 분석하지 마.', 'validate_demo_chess_position', 'analyze_demo_chess_position', 'legal_position', False, 'Check whether the current demo chess position is legal.', 'Analyze the current demo chess position once.'),
      ('consent', '받는 사람이 동의했는지 먼저 확인해 줘. 동의했을 때만 가짜 메시지를 대기열에 한 번 넣고 아니면 넣지 마.', 'check_demo_recipient_consent', 'enqueue_demo_message', 'consent_given', False, 'Check whether the current mock recipient has consented.', 'Enqueue the current fake message once, without contacting anyone.'),
      ('wind', '바람이 모의 이륙에 안전한지 확인해 줘. 안전할 때만 이륙을 한 번 시뮬레이션하고 아니면 하지 마.', 'inspect_demo_wind', 'simulate_demo_takeoff', 'wind_safe', False, 'Check whether wind is safe for the current mock takeoff.', 'Simulate the current mock takeoff once, without a real drone.'),
      ('backup', '백업할 공간이 충분한지 확인해 줘. 충분하면 가짜 백업을 한 번 만들고 부족하면 만들지 마.', 'inspect_demo_backup_space', 'create_demo_backup', 'space_available', True, 'Check whether sufficient space exists for the current fake backup.', 'Create the current fake backup once, in memory only.'),
      ('microphone', '마이크 신호가 들어오는지 확인한 뒤, 신호가 있으면 모의 녹음을 한 번 시작하고 없으면 시작하지 마.', 'inspect_demo_microphone', 'start_demo_recording', 'signal_present', False, 'Check whether the current mock microphone has a signal.', 'Start one mock recording, without accessing a real microphone.'),
      ('power', '전원이 안정적인지 먼저 확인해 줘. 안정적이면 모의 충전을 한 번 시작하고 불안정하면 시작하지 마.', 'inspect_demo_power_source', 'start_demo_charging', 'supply_stable', False, 'Check whether the current mock power supply is stable.', 'Start the current mock charging task once.'),
      ('lesson', '연습 문제 답이 맞는지 확인해 줘. 맞을 때만 다음 수업을 한 번 열어 주고 틀리면 열지 마.', 'verify_demo_exercise_answer', 'unlock_demo_next_lesson', 'answer_correct', False, 'Check whether the current demo exercise answer is correct.', 'Unlock the current next demo lesson once.'),
    ]
    rows = []
    for i, (id_, request, check, act, predicate, consumes, cd, ad) in enumerate(specs):
        params = {'type': 'object', 'properties': {}, 'required': []}
        ct = {'name': check, 'description': cd + ' Returns ok=true and ' + predicate + ' as a boolean. It only observes and does not perform the requested follow-up action.', 'parameters': copy.deepcopy(params)}
        at = {'name': act, 'description': ad + ' Requires the latest successful ' + check + ' result to have ' + predicate + '=true, and this task not already done. Returns ok=true and done=true. Otherwise returns an error without changing state.', 'parameters': copy.deepcopy(params)}
        order = [check, act, STOP]; random.Random(SEED + i).shuffle(order)
        rows.append({'id': id_, 'request': request, 'check': ct, 'act': at, 'predicate': predicate, 'consumes_condition': consumes, 'option_order': order})
    return rows


def oracle(c):
    return {'snapshots': {'initial': c['check']['name'], 'after_true': c['act']['name'], 'after_false': STOP, 'after_done': STOP},
            'positive': {'choices': [c['check']['name'], c['act']['name'], STOP], 'final_done': True},
            'negative': {'choices': [c['check']['name'], STOP], 'final_done': False}}


def new_training(cs):
    selectors, gates = [], []
    for c in cs:
        gold = oracle(c)['snapshots']
        for state, events in probe_states(c).items():
            v = selector_view(c['request'], [c['check'], c['act']], events, c['option_order'])
            if gold[state] != STOP:
                selectors.append({'id': c['id'] + ':' + state, 'case_id': c['id'], 'state': state, **v, 'target': gold[state], 'kind': 'paired'})
            for t in [c['check'], c['act']]:
                gates.append({'id': c['id'] + ':' + state + ':' + t['name'], 'case_id': c['id'], 'state': state, **gate_view(t, v['context']), 'target': 'yes' if gold[state] == t['name'] else 'no', 'kind': 'paired'})
    return selectors, gates


def prepare():
    previous_verify()
    if DATA.exists() or OUT.exists(): raise FileExistsError('V27 protected')
    known = read(V26 / 'cases.json'); fresh = fresh_cases()
    train = [c for c in known if c['id'] in TRAIN_IDS]
    selectors, gates = new_training(train)
    old_select = readlines(ROOT / 'data/processed/selector-transfer-v24/new_train.jsonl')[:12]
    for r in old_select:
        selectors.append({'id': 'replay:' + r['id'], **view(r, 'current_full'), 'target': r['expected'][0], 'kind': 'replay'})
    old_gate = readlines(ROOT / 'data/processed/tool-split-pilot-v1/gate_train.jsonl')
    for target in ['yes', 'no']:
        for r in [r for r in old_gate if r['target'] == target][:12]:
            gates.append({'id': 'replay:' + r['id'], 'question': r['question'], 'options': r['options'], 'context': r['context'], 'target': target, 'kind': 'replay'})
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True); tok.model_max_length = 1000000
    def length(v):
        return max(map(len, tok([v['question']+' '+x for x in v['options'].values()], [v['context']]*len(v['options']), truncation=False)['input_ids']))
    lengths = [length(r) for r in selectors + gates]
    for c in known + fresh:
        for truth in [True, False]:
            for size in range(3):
                for seq in itertools.product([c['check']['name'], c['act']['name']], repeat=size):
                    f = Fixture(c, truth)
                    for n in seq: f.invoke(n)
                    v = selector_view(c['request'], [c['check'], c['act']], f.events, c['option_order'])
                    lengths += [length(v)] + [length(gate_view(t, v['context'])) for t in [c['check'], c['act']]]
    if max(lengths) > 512: raise ValueError(('No truncation', max(lengths)))
    training_names = {c[t]['name'] for c in train for t in ['check','act']}
    # Exact tool-name exclusion from both NEW and REPLAY adaptation data.
    texts = __import__('json').dumps(selectors + gates, ensure_ascii=False)
    fresh_names = {c[t]['name'] for c in fresh for t in ['check','act']}
    if training_names & fresh_names or any(n in texts for n in fresh_names): raise ValueError('Fresh-tool overlap')
    assert len(selectors) == 24 and len(gates) == 72 and len(train) == 6 and len(fresh) == 12
    DATA.mkdir(parents=True); OUT.mkdir(parents=True)
    for n, x in [('known-cases.json', known), ('fresh-cases.json', fresh), ('selector-train.json', selectors), ('gate-train.json', gates)]: save(DATA/n, x)
    save(DATA/'oracle.json', {'known': {c['id']: oracle(c) for c in known}, 'fresh': {c['id']: oracle(c) for c in fresh}})
    paths = list(DATA.glob('*')) + [ROOT/p for p in ['agent/result_loop_split_v27.py','scripts/result_loop_split_data_v27.py','scripts/result_loop_split_v27.py','scripts/report_result_loop_split_v27.py','scripts/audit_result_loop_split_v27.py','tests/test_result_loop_split_v27.py']]
    paths += [ROOT/p for p in ['data/processed/selector-transfer-v24/new_train.jsonl','data/processed/tool-split-pilot-v1/gate_train.jsonl','data/processed/selector-interface-v18/reference.jsonl','data/processed/tool-split-pilot-v1/korean_seen_control.jsonl','output/training/tool-split-pilot-v1/dev-selection.json']]
    for p in [SELECTOR, LATEST, GATE]: paths += [p/'adapter_model.safetensors', p/'adapter_config.json']
    save(DATA/'protocol.json', {'frozen_files': {str(p.relative_to(ROOT)): digest(p) for p in paths}, 'seed': SEED, 'lr': 1e-4, 'epochs': 10, 'logical_batch': 4, 'read_epochs': [0,1,10], 'steps': {'selector':60,'gate':180}, 'gate_threshold': -1.5, 'train_case_ids': sorted(TRAIN_IDS), 'max_tokens': max(lengths),
      'baseline': 'Original selector+original gate (existing split pair), plus V24-new selector+original gate. Known V26 cases only before learning. No tuning on the new12 tasks.',
      'adaptation': 'Only if latest pair fails known20 strict paths. Separate q/v LoRA adaptation of V24-new selector and original gate. Selector12 new positive-state decisions+12 prior Korean replay; gate48 new tool-conditioned decisions+24 prior yes/no replay. Fixed10 epochs, no fresh/retention checkpoint selection.',
      'runtime': 'Rank the two actual tools, then binary judge ONLY that proposed tool. If rejected, stop with no tool. No fallback or oracle next tool. Same full Korean request and all actual JSON tool results to both models. Existing preconditions enforce execution only; blocked attempts are model errors.',
      'threshold': 'Unchanged split_after threshold -1.5 from old development-only choice. Not retuned for new states or learned adapters. Different score-scale calibration remains possible and is not isolated here.',
      'evaluation': 'After both final weights fixed: 12 authored new tool tasks,4 snapshots and2 autonomous episodes each;4 combinations (before/before, after/before, before/after, after/after). Also known10 diagnostics; original600 selector-only capability reference and30 old Korean full-pipeline reference for before and after. Prior tests are retention references, not new validation.',
      'scope': 'No generated arguments, real services, actual skin state extraction, Qwen replies, or demo deployment. Empty-argument mock tools. New12 share conditional template with training; exact names absent in adaptation, not proof of all-domain unseen90 accuracy. Assistant-authored labels, no independent human review.',
      'adoption_guard': 'Do not deploy in any case. Exploratory positive signal requires more fresh paired branches both correct and more strict episodes, no loss of initial checking; retention selector groups and Korean pipeline must not lose correct count. Report all4 arms; stop after fixed run even if not improved.'})
    print('V27 FROZEN: selector24, gate72, fresh12 pairs, max_tokens', max(lengths), flush=True)


def verify():
    previous_verify(); p = read(DATA/'protocol.json')
    for rel, h in p['frozen_files'].items():
        if digest(ROOT/rel) != h: raise ValueError('Frozen V27 changed: '+rel)
    return p


if __name__ == '__main__': prepare()
