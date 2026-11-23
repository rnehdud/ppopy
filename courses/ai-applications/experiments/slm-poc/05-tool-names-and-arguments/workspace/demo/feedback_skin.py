"""Opt-in feedback loop: classify without saving, choose, execute, then choose again.

Uses the existing skin-trained scalar adapter. No forced record fallback, expected
tool sequence, new training, or inferred global completion is provided to it.
"""
import copy
from jsonschema import Draft202012Validator
from agent.choice_agent_v1 import choose,SYMPTOM_QUESTION,SYMPTOM_DESCRIPTIONS,NAMES,TOOL_QUESTION,TOOL_DESCRIPTIONS
from agent.symptom_state_v1 import SYMPTOMS,PATCH_SCHEMA
from agent.live_tool_agent import ToolRegistry
from agent.contract_filter_v34 import readiness
from agent.result_loop_probe_v26 import stable
from demo.skin_tools import SkinSession

DESCRIPTIONS={
 'record':'이번 발화에서 판정된 사용자 본인의 피부 증상 중 아직 기록에 반영되지 않은 변경을 저장한다. 저장할 변경이 없으면 이 도구를 쓰지 않는다.',
 'show':'사용자가 기록 확인을 요청하면 저장된 피부 상태를 읽어 보여준다. 새 증상을 저장하지 않는다. 이미 읽은 결과로 요청에 답할 수 있으면 반복하지 않는다.',
 'ask':TOOL_DESCRIPTIONS['ask'],
 'none':'이번 요청에 필요한 작업을 이미 했거나 지금 실행할 작업이 없으면 도구를 추가로 사용하지 않고 답변한다.'}


class FeedbackSkinSession(SkinSession):
    def analyze(self,text):
        before=self.record.state;decisions={};patch={};observations={}
        def score(q,opts,ctx):return self.score('symptom',{'question':q,'options':opts,'context':ctx})['raw_scores']
        for field in SYMPTOMS:
            ctx='대상 증상: '+NAMES[field]+'\n이전 상태: '+before[field]+'\n이번 사용자 발화: '+text
            d=choose(score,SYMPTOM_QUESTION,SYMPTOM_DESCRIPTIONS,ctx);decisions[field]=d
            if d['choice']!='unchanged':
                observations[field]=d['choice']
                if before[field]!=d['choice']:patch[field]=d['choice']
        if patch:Draft202012Validator(PATCH_SCHEMA).validate(patch)
        return {'base_version':self.record.version,'observations':observations,'proposed_patch':patch,'decisions':decisions}

    def bound_catalog(self,text,analysis):
        original=self.catalog(text);r=ToolRegistry()
        def save():
            # Bound to this statement and the version that was actually classified.
            if self.record.version!=analysis['base_version']:return {'ok':False,'reason':'stale_analysis','state':self.record.state,'version':self.record.version}
            patch={k:v for k,v in analysis['proposed_patch'].items() if self.record.state[k]!=v}
            if not patch:return {'ok':False,'reason':'no_supported_change','state':self.record.state,'version':self.record.version}
            return {**self.record.update(patch),'done':True,'patch':patch}
        for d in original.definitions():
            handler=save if d['name']=='record_skin_symptoms' else lambda name=d['name']:original.invoke(name,{})
            r.register(d,handler)
        return r

    def turn(self,text,max_steps=4):
        before=self.record.state
        try:analysis=self.analyze(text)
        except ValueError as exc:
            if 'context' not in str(exc).lower() and 'input exceeds' not in str(exc).lower():raise
            return self.finish(text,before,[],[],{'decisions':{},'observations':{},'proposed_patch':{}},[],'input_limit',False)
        registry=self.bound_catalog(text,analysis);defs=registry.definitions();aliases={'record_skin_symptoms':'record','read_skin_record':'show'}
        by={aliases.get(d['name'],d['name']):d for d in defs};options={k:DESCRIPTIONS.get(k,d['description']) for k,d in by.items()}
        options.update({k:DESCRIPTIONS[k] for k in ['ask','none']});events=[];steps=[];seen=set();reason='step_limit';model_stopped=False
        def score(q,opts,ctx):return self.score('symptom',{'question':q,'options':opts,'context':ctx})['raw_scores']
        for i in range(max_steps):
            pending={k:v for k,v in analysis['proposed_patch'].items() if self.record.state[k]!=v}
            # Full actual results retained. No gold action/route is passed in. The
            # pending difference is classifier output vs actual stored state.
            ctx='현재 기록: '+stable(self.record.state)+'\n사용자 발화: '+text+'\n이번 발화의 증상 판정: '+stable(analysis['observations'])+'\n아직 반영되지 않은 변경: '+stable(pending)+'\n이번 요청의 실제 실행 결과: '+stable(events)+'\n최근 사용자 발화: '+stable(self.history[-2:])+'\n사용 가능한 동작:\n'+'\n'.join('- '+k for k in options)
            try:decision=choose(score,TOOL_QUESTION,options,ctx)
            except ValueError as exc:
                if 'context' not in str(exc).lower() and 'input exceeds' not in str(exc).lower():raise
                reason='input_limit';break
            choice=decision['choice'];name=by[choice]['name'] if choice in by else 'no_tool'
            step={'index':i,'decision':{'raw_selected':name,'selected':name,'reason':'model_choice','domain_decision':decision,'model_context':ctx,'pending_patch':copy.deepcopy(pending)},'event':None};steps.append(step)
            if choice not in by:
                reason='model_stop' if choice=='none' else 'model_ask';model_stopped=True;break
            condition=readiness(by[choice],events);step['decision']['condition']=condition
            if not condition['eligible']:step['decision'].update(selected='no_tool',reason='condition_not_met');reason='condition_not_met';break
            key=(name,self.record.version)
            if key in seen:step['decision'].update(selected='no_tool',reason='duplicate_call');reason='duplicate_call';break
            seen.add(key)
            try:result=registry.invoke(name,{})
            except Exception:result={'ok':False,'reason':'handler_error','effects_unknown':True};reason='handler_error'
            event={'tool':name,'arguments':{},'executed':True,'result':result};events.append(event);step['event']=copy.deepcopy(event)
            if result.get('ok') is not True:
                if reason!='handler_error':reason='tool_error'
                break
        return self.finish(text,before,events,steps,analysis,defs,reason,model_stopped)

    def finish(self,text,before,events,steps,analysis,defs,reason,model_stopped):
        patch={k:v for k,v in self.record.state.items() if v!=before[k]}
        writes=any(e['tool']=='record_skin_symptoms' and e['result'].get('ok') is True for e in events)
        reads=any(e['tool']=='read_skin_record' and e['result'].get('ok') is True for e in events)
        action='record' if writes else 'show' if reads else 'none' if reason=='model_stop' else 'ask'
        self.history.append(text);self.history=self.history[-2:]
        return {'before':before,'after':self.record.state,'patch':patch,'action':action,'input':text,'symptom_decisions':analysis['decisions'],
          'state_analysis':{k:copy.deepcopy(analysis[k]) for k in ['observations','proposed_patch']},'events':events,'steps':steps,
          'stop_reason':reason,'model_stopped':model_stopped,'complete':False,'engine':'feedback-loop',
          'available_tools':[{'name':d['name'],'description':d['description']} for d in defs]}
