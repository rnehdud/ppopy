"""Executable coverage receipts, not a domain-completeness certification."""
from copy import deepcopy
from collections import Counter
import argparse
import json
from pathlib import Path
from .engine import PreviewEngine
from .audit import request, assess


def run():
    e=PreviewEngine();cards=[];total=0
    for cid,c in e.cards.items():
        executions=[]
        for branch in e.rules[cid]:
            if not branch['when']:continue
            facts={f:vs[0] for f,vs in branch['when'].items()}
            q=request(facts,[cid])
            if cid in ('B-M04','B-L02'):q['body_site']='hands'
            if cid in ('B-G13','B-G14','B-G15') and branch['status']=='difference':
                pair=next(p for p in e.kb['combination_policy']['pairs'] if p['card_id']==cid)
                q['facts'].update(request({'product.reviewed_role_pair':[pair['left'],pair['right']]})['facts'])
            result=e.evaluate(q)['results'][0]
            assert result['comparison_status']==branch['status'],branch['branch_id']
            missing=[]
            for field in branch['when']:
                changed=deepcopy(q);changed['facts'][field]['state']='unknown'
                after=e.evaluate(changed)['results'][0]
                assert after['matched_branch_id']!=branch['branch_id']
                missing.append({'removed':field,'status':after['comparison_status'],'reason':after['reason']})
            executions.append({'branch_id':branch['branch_id'],'kb_clause':branch['kb_clause'],'kb_text':branch['kb_text'],
                               'input':q,'expected':branch['status'],'actual':result['comparison_status'],'reason':result['reason'],
                               'effective_branch_id':result['matched_branch_id'],'overridden_by_shared_or_special':result['matched_branch_id']!=branch['branch_id'],
                               'actions':result['action_types'],'missing_antecedent_checks':missing,'source_ids':result['evidence']['source_ids']})
        # Actual shared missing/conflict/individual-plan checks for every card.
        empty=request({},[cid]);initial=e.evaluate(empty)['results'][0]
        assert initial['comparison_status']=='unknown'
        field=c['observable_inputs'][0]
        conflict=request({},[cid]);conflict['facts'][field]={'value':None,'state':'conflicting','source':'user_report','reference':'synthetic conflict fixture'}
        assert e.evaluate(conflict)['results'][0]['comparison_status']=='conflicting'
        conflict['facts'].update(request({'context.individual_instruction':True})['facts'])
        assert e.evaluate(conflict)['results'][0]['comparison_status']=='exception'
        linked=[]
        for scenario in e.kb['acceptance_scenarios']:
            if cid in scenario['card_ids']:
                full=e.evaluate(request(scenario['facts'],scenario['card_ids']))
                row=next(r for r in full['results'] if r['card_id']==cid)
                linked.append({'id':scenario['id'],'actual':row['comparison_status'],'reason':row['reason'],'audit_category':assess(scenario,full)['category']})
        special=cid in ('B-C03','B-P01','B-P05','B-P07','B-S06')
        rows={'card_id':cid,'title':c['title'],'loaded':True,'input_fields':sorted(set(c['observable_inputs'])|{f for b in e.rules[cid] for f in b['when']}),
              'selection':'field overlap + optional exact lifecycle stage; explicit selectors supported','lifecycle_stages':c['lifecycle_stage_ids'],
              'comparison_implementation':'special.py + rules.json' if special else 'rules.json',
              'conditional_branches_executed':len(executions),'branch_receipts':executions,
              'shared_exceptions_executed':['conflicting observation','individual instruction'],
              'original_exception_clauses':c['comparison_spec']['exception_when'],
              'missing_input_executed':initial['comparison_status'],'questions':initial['questions'],'evidence_requests':initial['evidence_requests'],
              'question_policy':'only KB consumer_question_allowed; decline respected; product evidence retrieved separately',
              'recommendation':deepcopy(c['recommendation']),'recommendation_selection':'six-state comparison + priority suppression + exact-text deduplication',
              'evidence_trace':{'source_ids':c['evidence']['source_ids'],'source_text_linked':True,'kb_sha256':e.sha},
              'acceptance_execution':linked,
              'tests':['tests/test_kb_preview_extended.py::test_every_card_unknown_conflict_instruction_and_evidence',
                       'tests/test_kb_preview_extended.py::test_branch_execution_and_missing_antecedents',
                       'tests/test_kb_preview_extended.py::test_semantic_boundaries',
                       'tests/test_kb_preview.py::test_acceptance'],
              'implementation_status':'structured_branches_executed_development_only',
              'not_claimed':['exhaustive interpretation of free text','validated real-world efficacy','production approval']}
        if cid in ('B-P05','B-P07'):rows['restricted_scope']='filter profile / recorded opinion only; not overall candidate suitability or rank'
        if cid in ('B-G13','B-G14','B-G15'):rows['data_requirement']='reviewed pair roles + separate product relationship; INCI alone insufficient'
        cards.append(rows);total+=len(executions)
    return {'kb_sha256':e.sha,'cards_loaded':len(cards),'cards_with_development_mapping':len(cards),
            'conditional_branches_executed':total,
            'direct_branch_receipts':sum(not b['overridden_by_shared_or_special'] for c in cards for b in c['branch_receipts']),
            'shared_or_special_override_receipts':sum(b['overridden_by_shared_or_special'] for c in cards for b in c['branch_receipts']),
            'shared_boundary_cases_executed':len(cards)*3,
            'scope':'compiled structured observations, not all possible natural-language interpretations','production_enabled':False,'cards':cards}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run()
    Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='cards'}))
if __name__=='__main__':main()
