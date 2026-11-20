from copy import deepcopy
import pytest
from beauty_agent.afa.eda import profile


def fixture():
    def turn(message,events=None):return {'message':message,'user_events':{'observations':events or {}}}
    scenarios=[{'scenario_id':'s1','card_ids':['C'],'turns':[turn('first'),turn('answer',{'x':{'state':'unknown','value':None}})]},
               {'scenario_id':'s2','card_ids':['C'],'turns':[turn('other')]}]
    ctx={'message':'first','available_actions':[{'action':'ask_user','target_id':'x','enabled':True}], 'observations':{}}
    def row(i,s,context,action):return {'id':i,'scenario_id':s,'input':context,'output':{'action':action,'target_id':'x'},'review':{'label_source':'authored'},'card_ids':['C']}
    rows=[row('a','s1',ctx,'ask_user'),row('b','s1',deepcopy(ctx),'hold'),row('c','s2',{**ctx,'message':'other'},'ask_user')]
    splits={'train':rows,'val_internal':[],'test_internal':[]}
    kb={'variables':[{'id':'x','consumer_question_allowed':True}], 'baseline_cards':[{'id':'C','observable_inputs':['x']}]}
    contract={'action_dictionary':[['ask_user','x']]}
    return scenarios,splits,kb,contract


def test_units_duplicates_and_multilabel_are_distinct():
    r,_=profile(*fixture())
    assert (r['scenario_count'],r['turn_count'])==(2,3)
    assert r['exact_input_duplicate_excess']==1 and r['exact_input_multilabel_groups']==1
    assert r['exact_input_cross_split_groups']==0


def test_response_presence_does_not_invent_known_value_or_merge_into_context():
    args=fixture();original=deepcopy(args)
    r,_=profile(*args)
    assert args==original
    assert r['enabled_consumer_ask_later_observation_occurrences']=={'later_event_present':2,'not_recorded_later':1}
    assert r['scenarios_with_all_declared_consumer_card_inputs_recorded']==1
    assert r['observation_snapshot_state_counts']=={}


def test_cross_split_input_and_scenario_overlap_are_different():
    args=fixture(); copied=deepcopy(args[1]['train'][0]);copied['id']='held';copied['scenario_id']='s2'
    args[1]['val_internal']=[copied];args[1]['train']=args[1]['train'][:2]
    r,_=profile(*args)
    assert r['exact_input_cross_split_groups']==1


def test_same_scenario_in_two_splits_is_rejected():
    args=fixture();args[1]['test_internal']=[deepcopy(args[1]['train'][0])]
    with pytest.raises(ValueError,match='crosses splits'):profile(*args)


def test_candidates_and_selected_pairs_have_separate_counts():
    args=fixture();args[1]['train'][0]['input']['available_actions'].append({'action':'retrieve_evidence','target_id':'product.instructions','enabled':False})
    r,_=profile(*args)
    assert r['unique_available_action_target_pairs']==2
    assert r['v2_scope_comparison']['v67_proposals_in_v2_8_pair_catalog']==2
