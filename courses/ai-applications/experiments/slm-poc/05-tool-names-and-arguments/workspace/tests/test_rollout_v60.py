import copy,tempfile,unittest
from pathlib import Path
from agent.rollout_files_v60 import Files,grade,names
from agent.rollout_teacher_v60 import valid_next
from scripts.rollout_data_v60 import make_files,training_cases,ROOT

class RolloutChecks(unittest.TestCase):
    def test_teacher_rejects_irreversible_wrong_prefix(self):
        c=next(c for c in training_cases() if len(c['teacher_plan'])==3)
        initial={'events':[]};target,stage=valid_next(c,initial)
        self.assertEqual(target,c['ids'][c['teacher_plan'][0]])
        read={'tool':target,'result':{'ok':True}}
        target,stage=valid_next(c,{'events':[read]});self.assertEqual(stage,'continue')
        wrong={'tool':c['ids'][c['teacher_plan'][1]],'result':{'ok':True}}
        self.assertIsNone(valid_next(c,{'events':[wrong]})[0])
    def test_actual_calculations_are_independent_manual_expected(self):
        parent=Path(tempfile.mkdtemp(prefix='rollout60-test-',dir=ROOT/'tmp'))
        for c in [x for x in make_files() if x['kind']=='read_process' and x['style']==0]:
            s=Files(parent/c['family'],c['family'],c['payload']);self.assertFalse(s.process()['ok']);self.assertFalse(s.output.exists())
            s.read();self.assertTrue(s.process()['ok']);self.assertEqual(s.snapshot()['output'],c['turns'][0]['output']);self.assertTrue(s.snapshot()['input_unchanged'])
    def test_no_call_and_early_stop_cannot_pass(self):
        parent=Path(tempfile.mkdtemp(prefix='rollout60-grade-',dir=ROOT/'tmp'))
        c=next(x for x in make_files() if x['kind']=='read_process');s=Files(parent/'a',c['family'],c['payload'])
        trace={'events':[],'steps':[{'choice':'none'}],'model_stopped':True,'stop_reason':'model_stop'}
        self.assertFalse(grade(c['turns'][0],trace,s)['goal_and_stop'])
        t={'roles':[],'output':None};trace['steps']=[{'choice':names(c['family'])['a']}]
        self.assertFalse(grade(t,trace,s)['goal_ok'])
    def test_case_counts_and_split(self):
        rows=make_files();self.assertEqual(len([c for c in rows if c['split']=='final']),120)
        self.assertEqual(sum(len(c['turns']) for c in rows if c['split']=='final'),144)
        self.assertEqual(len(training_cases()),120)
if __name__=='__main__':unittest.main()
