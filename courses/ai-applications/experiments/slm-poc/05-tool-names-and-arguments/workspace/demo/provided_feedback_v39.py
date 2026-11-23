"""Controlled upstream-observation probe, without changing the frozen controller."""
import copy
from demo.prepared_feedback_v38 import PreparedFeedbackSession


class ProvidedFeedbackSession(PreparedFeedbackSession):
    def __init__(self,neural,case,tokenizer):
        # Only supplied observations, never expected actions/final state, enter runtime.
        c={k:copy.deepcopy(case[k]) for k in ['text','initial','history','available']}
        c['gold_observations']=copy.deepcopy(case['provided_observations'])
        super().__init__(neural,c,tokenizer,'gold')

    def analyze(self,text):
        super().analyze(text)
        for d in self.analysis['decisions'].values():d['source']='controlled_upstream_observation_not_gold'
        return copy.deepcopy(self.analysis)
