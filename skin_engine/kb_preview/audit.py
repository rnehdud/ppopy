"""Execute original acceptance facts unchanged; count gaps separately from success."""
import json
from pathlib import Path
from .engine import PreviewEngine, ROOT

def request(facts, cards=None):
    out={'mode':'development_preview','project':'Poppy','data_kind':'synthetic','population':'adult','body_site':facts.get('method.body_site','face'),
         'product_instance_id':'SYNTHETIC-ACCEPTANCE','facts':{k:{'state':'unknown' if v is None else 'known','value':v,'source':'synthetic_fixture','reference':'KB authored synthetic facts'} for k,v in facts.items()}}
    if cards is not None:out['card_ids']=cards
    return out

# Each prose expectation is translated independently; descriptions never fill input facts.
def prose_check(sid,statuses,actions,out):
    checks={
      'V06-T01':lambda: statuses['B-Q02']=='aligned' and 'refer_for_professional_review' in actions,
      'V06-T02':lambda: 'retrieve_product_evidence' in actions,
      'V06-T03':lambda: 'pause_specific_product_pending_quality_check' in actions and out['results'][1]['action_types']==['defer_specific_recommendation'],
      'V06-T04':lambda: 'avoid_unnecessary_active_stacking' in actions,
      'V06-T05':lambda: statuses['B-G15']=='exception' and 'avoid_unnecessary_active_stacking' not in actions,
      'V06-T06':lambda: statuses['B-G13']=='unknown',
      'V06-T07':lambda: statuses['B-G13']=='not_applicable',
      'V06-T08':lambda: statuses['B-G15']!='aligned' and 'maintain' not in actions,
      'V06-T09':lambda: statuses['B-C03']=='not_applicable' and 'review_current_label_scope' in actions,
      'V06-T10':lambda: 'review_current_label_scope' in actions and statuses['B-H01']!='difference',
      'V06-T11':lambda: 'check_product_batch_and_recall_scope' in actions and 'pause_specific_product_pending_quality_check' not in actions,
      'V06-T12':lambda: 'inform_general_practice' in actions and '손에 덜어' in out['results'][0]['recommendation_text'],
    }
    return checks[sid]()

GAP_REASONS={
 'T17':('input_spec_conflict','Description asserts basic protection; facts omit SPF/UVA and exposure. P01 must remain unknown.'),
 'T20':('policy_isolated','MP-01 opinion comparison works; using it as a candidate tiebreaker conflicts with production manufacturer_name_weight=0/prohibited name bonus. No ranking activated.'),
 'T37':('expectation_conflict','expected_comparison=exception conflicts with expected_by_card={B-G09:aligned,B-C03:not_applicable}. Both are preserved.'),
 'T45':('expectation_conflict','expected_comparison=not_applicable conflicts with expected_by_card including B-M04:unknown. Both are preserved.'),
 'V06-T04':('input_spec_conflict','Description says retinol+AHA; supplied facts only identify same-area timing. Reviewed roles and separate-product identity are absent.'),
}
KNOWN_GAP_SIGNATURES={
 'T17':(['expected_comparison'],{'B-P01':'unknown','B-P05':'aligned'}),
 'T20':([],{'B-P07':'aligned'}),
 'T37':(['expected_comparison'],{'B-G09':'aligned','B-C03':'not_applicable'}),
 'T45':(['expected_comparison'],{'B-C03':'not_applicable','B-M04':'unknown'}),
 'V06-T04':(['expected_behavior'],{'B-G13':'unknown'}),
}

def assess(scenario,out):
    statuses={r['card_id']:r['comparison_status'] for r in out['results']}
    actions={a for r in out['results'] for a in r['action_types']}
    if out['context_result']:actions.update(out['context_result']['action_types'])
    actual=set(statuses.values()) or {out['context_result']['comparison_status']}
    failures=[]
    if 'expected_by_card' in scenario and statuses!=scenario['expected_by_card']:failures.append('expected_by_card')
    expected=scenario.get('expected_comparison')
    if expected:
        matched=(len(actual)>1 if expected=='mixed_by_card' else (expected in actual if expected in ('difference','exception') else actual=={expected}))
        if not matched:failures.append('expected_comparison')
    if not set(scenario.get('expected_action_types',[]))<=actions:failures.append('expected_action_types')
    if scenario.get('expected_behavior') and not prose_check(scenario['id'],statuses,actions,out):failures.append('expected_behavior')
    rendered=json.dumps(out,ensure_ascii=False)
    failures += ['prohibited:'+p for p in scenario.get('prohibited_outputs',[]) if p in rendered]
    category='expected_satisfied' if not failures else 'implementation_failure'
    reason=None
    if scenario['id'] in GAP_REASONS and (failures,statuses)==KNOWN_GAP_SIGNATURES[scenario['id']]:
        category,reason=GAP_REASONS[scenario['id']]
    return {'id':scenario['id'],'original_expectation':{k:v for k,v in scenario.items() if k.startswith('expected')},
            'original_facts':scenario['facts'],'facts_unchanged':True,'statuses':statuses,'context_result':out['context_result'],
            'evidence_by_card':{r['card_id']:r['evidence']['source_ids'] for r in out['results']},
            'questions':out['questions'],'actions':sorted(actions),'failures':failures,'category':category,'reason':reason}

def run():
    engine=PreviewEngine();rows=[assess(s,engine.evaluate(request(s['facts'],s['card_ids']))) for s in engine.kb['acceptance_scenarios']]
    from collections import Counter
    return {'kb_sha256':engine.sha,'original_count':len(rows),'summary':dict(Counter(r['category'] for r in rows)),'scenarios':rows}

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();report=run();Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary']))
    raise SystemExit(1 if any(r['category']!='expected_satisfied' for r in report['scenarios']) else 0)
if __name__=='__main__':main()
