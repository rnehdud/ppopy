"""Same feedback controller, shared V37r1 rendering, explicit gold/parser conditions.

Gold observations are an evaluation input, not model predictions. Request targets,
teacher plans and expected final states are never given to this session.
"""
import copy
from demo.feedback_skin import FeedbackSkinSession
from scripts.complete_teacher_data_v37 import GoldTeacherSession
from agent.decision_context_v37r1 import make_view,legacy_context


def parser_view(v):return set(v['options'])=={'present','absent','unchanged','unknown'}


def public_case(c,upstream):
    result={k:copy.deepcopy(c[k]) for k in ['text','initial','history','available']}
    if upstream=='gold':result['gold_observations']=copy.deepcopy(c['gold_observations'])
    elif upstream!='parser':raise ValueError('Unknown upstream condition')
    return result


class PreparedFeedbackSession(GoldTeacherSession):
    def __init__(self,neural,c,tokenizer,upstream):
        self.neural=neural;self.tokenizer=tokenizer;self.upstream=upstream;self.scoring_inputs=[]
        super().__init__(self.routed_score,public_case(c,upstream))
    def analyze(self,text):
        if self.upstream=='gold':return super().analyze(text)
        self.analysis=FeedbackSkinSession.analyze(self,text)
        return copy.deepcopy(self.analysis)
    def routed_score(self,role,v):
        if parser_view(v):
            entry={'role':'parser','input':copy.deepcopy(v)};self.scoring_inputs.append(entry)
            try:response=self.neural('parser',v)
            except ValueError as exc:
                if str(exc)=='No truncation' or 'input exceeds' in str(exc).lower():entry['error']='input_limit';raise ValueError('Input exceeds parser context; no truncation') from exc
                raise
        else:
            packet={'request':self.c['text'],'state':self.record.state,'observations':copy.deepcopy(self.analysis['observations']),
              'pending':{k:value for k,value in self.analysis['proposed_patch'].items() if self.record.state[k]!=value},
              'events':copy.deepcopy(self.shadow_events),'history':self.history[-2:],'available_actions':list(v['options'])}
            if legacy_context(packet)!=v['context']:raise ValueError('Prepared input does not match actual runtime facts')
            converted,encoding=make_view(v['question'],v['options'],packet,self.tokenizer)
            entry={'role':'action','legacy_input':copy.deepcopy(v),'packet':packet,'input':converted,'encoding':encoding};self.scoring_inputs.append(entry)
            if encoding['tokens']>512:entry['error']='input_limit';raise ValueError('Input exceeds action context; no truncation')
            response=self.neural('action',converted)
        entry['response']=copy.deepcopy(response)
        return response
