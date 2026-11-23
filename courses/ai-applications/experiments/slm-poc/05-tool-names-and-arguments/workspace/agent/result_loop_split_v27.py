"""Two-model dispatch: rank a tool, then judge that tool. No oracle or fallback."""
import copy
from agent.result_loop_probe_v26 import model_view, STOP, stable
from scripts.tool_split_data_v1 import GATE_QUESTION, YES, NO
from scripts.selector_interface_data_v18 import full


def selector_view(request, tools, events, order):
    v = model_view(request, tools, events, 'json', order)
    v['options'].pop(STOP)
    return v


def gate_view(tool, context):
    definition = full(tool)
    return {'question': GATE_QUESTION,
            'options': {'yes': YES + '\n' + definition, 'no': NO + '\n' + definition},
            'context': context}


def dispatch(request, tools, events, order, score_selector, score_gate, threshold):
    v = selector_view(request, tools, events, order)
    ranked = score_selector(v)
    chosen = max(v['options'], key=ranked['raw_scores'].get)
    tool = next(t for t in tools if t['name'] == chosen)
    gv = gate_view(tool, v['context'])
    checked = score_gate(gv)
    margin = checked['raw_scores']['yes'] - checked['raw_scores']['no']
    return {'selected': chosen if margin >= threshold else STOP,
            'proposed_tool': chosen, 'selector': ranked, 'gate': checked,
            'gate_margin': margin, 'gate_threshold': threshold,
            'observed_event_count': len(events), 'observation_payload': copy.deepcopy(events)}
