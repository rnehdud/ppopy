"""Plots and explicitly labelled MLflow publication for measured EDA reports."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .tracking import LocalTracker


def render(directory, publish=False):
    directory=Path(directory).resolve();r=json.loads((directory/'report.json').read_text(encoding='utf-8'))
    charts=directory/'charts';charts.mkdir(exist_ok=True)
    def bar(name,values,title,ylabel):
        fig,ax=plt.subplots(figsize=(10,5.5),layout='constrained')
        ax.bar(list(values),list(values.values()),color='#3478b5');ax.set(title=title,ylabel=ylabel)
        ax.tick_params(axis='x',labelrotation=20);ax.bar_label(ax.containers[0],fmt='%.0f')
        fig.savefig(charts/name,dpi=145);plt.close(fig)
    bar('01-actions.png',r['action_counts'],'v67: selected action labels (all 2,453 turns)','Turns; not independent users')
    bar('02-lengths.png',r['scenario_length_histogram'],'v67: conversation length (1,025 scenarios)','Scenarios')
    bar('03-states.png',r['observation_snapshot_state_counts'],'v67: observation states in turn snapshots','Slot occurrences; repeated across turns')
    bar('04-response-gaps.png',r['enabled_consumer_ask_later_observation_occurrences'],
        'Enabled consumer asks: is a later observation event recorded?','Candidate occurrences; NOT missing-user-answer rate')
    fig,ax=plt.subplots(figsize=(10,15),layout='constrained')
    counts=sorted(r['card_scenario_memberships'].items(),key=lambda x:x[1])
    ax.barh([k for k,v in counts],[v for k,v in counts]);ax.set(title='Card references: 58 cards, 1,025 scenarios',xlabel='Scenario memberships (multi-card cases may count more than once)')
    fig.savefig(charts/'05-cards.png',dpi=140);plt.close(fig)
    actions=sorted(r['action_counts']);splits=list(r['actions_by_split'])
    fig,ax=plt.subplots(figsize=(11,5.5),layout='constrained')
    for j,s in enumerate(splits):
        vals=[100*r['actions_by_split'][s].get(a,0)/r['turn_splits'][s] for a in actions]
        ax.bar([i+(j-1)*.25 for i in range(len(actions))],vals,width=.25,label=s)
    ax.set(xticks=list(range(len(actions))),xticklabels=actions,ylabel='Percent within each split',title='Action mix differs across splits (different denominators)');ax.tick_params(axis='x',labelrotation=15);ax.legend()
    fig.savefig(charts/'06-split-mix.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(13,8),layout='constrained')
    ax=axes[0,0];ax.bar(['Train','Val','Test'],[r['turn_splits'][s] for s in splits]);ax.set(title='2,453 turns / 1,025 scenarios',ylabel='Turns')
    ax=axes[0,1];ax.bar(['Single turn','Multi turn'],[r['scenario_length_histogram']['1'],r['scenario_count']-r['scenario_length_histogram']['1']]);ax.set(title='964 / 1,025 scenarios are multi-turn',ylabel='Scenarios')
    ax=axes[1,0];ax.bar(['B-C01','Others'],[r['card_scenario_memberships']['B-C01'],r['scenario_count']-r['card_scenario_memberships']['B-C01']]);ax.set(title='B-C01 appears in 531 / 1,025 scenarios',ylabel='Scenarios (presence / absence)')
    ax=axes[1,1];ax.bar(['Later event','Not recorded'],[r['enabled_consumer_ask_later_observation_occurrences'].get(k,0) for k in ['later_event_present','not_recorded_later']]);ax.set(title='Recorded paths are not complete RL worlds',ylabel='Enabled consumer-ask occurrences')
    fig.suptitle('Whole-v67 EDA: structural diagnostics, not policy performance',fontsize=15)
    fig.savefig(charts/'00-overview.png',dpi=145);plt.close(fig)
    if not publish:return None
    tracker=LocalTracker();run_id=tracker.start('AFA-v67-EDA','E20-whole-v67-structural-analysis',
        tags={'record_kind':'new_eda_analysis','evidence_entry':'E20','new_training':'false'},
        params={'scope':r['scope'],'source_hashes':r['source_sha256'],'code_version':'eda-v1',
                'manual_review_sample':'12 train turns stratified by selected action; agent review, not expert approval'})
    try:
        tracker.log(run_id,{'scenarios':r['scenario_count'],'turns':r['turn_count'],'cards':r['unique_cards'],
            'multi_turn_scenarios':r['scenario_count']-r['scenario_length_histogram']['1'],
            'exact_input_duplicate_excess':r['exact_input_duplicate_excess'],
            'exact_input_multilabel_groups':r['exact_input_multilabel_groups'],
            'exact_input_cross_split_groups':r['exact_input_cross_split_groups'],
            'later_answer_event_not_recorded':r['enabled_consumer_ask_later_observation_occurrences']['not_recorded_later'],
            'new_policy_training_runs':0})
        tracker.client.log_artifacts(run_id,str(directory))
        tracker.finish(run_id)
    except BaseException:
        tracker.finish(run_id,failed=True);raise
    result={'run_id':run_id,'experiment_id':tracker.client.get_run(run_id).info.experiment_id,'tracking_uri':tracker.uri}
    (directory.parent/'mlflow-run.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result));return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--publish',action='store_true');a=p.parse_args();render(a.directory,a.publish)
