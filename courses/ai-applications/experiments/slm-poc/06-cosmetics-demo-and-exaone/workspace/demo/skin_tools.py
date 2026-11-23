"""The two real, in-memory skin tools. No product DB or external KB is connected."""
import json
from pathlib import Path
from agent.live_tool_agent import ToolRegistry,run_turn
from agent.choice_agent_v1 import choose,SYMPTOM_QUESTION,SYMPTOM_DESCRIPTIONS,NAMES,TOOL_QUESTION,TOOL_DESCRIPTIONS
from agent.symptom_state_v1 import SYMPTOMS,SymptomSession,PATCH_SCHEMA

CONFIG=Path(__file__).with_name('skin_tools.json')
STATE_SCHEMA={'type':'object','properties':{k:{'enum':['present','absent','unknown']} for k in SYMPTOMS},'required':list(SYMPTOMS),'additionalProperties':False}
OUTPUT={'type':'object','properties':{'ok':{'type':'boolean'},'done':{'type':'boolean'},'reason':{'type':'string'},'patch':PATCH_SCHEMA,'state':STATE_SCHEMA,'version':{'type':'integer','minimum':0}},'required':['ok'],'additionalProperties':False}


def definition(name,description,once=False):
    return {'name':name,'description':description,'inputSchema':{'type':'object','properties':{},'additionalProperties':False},'outputSchema':OUTPUT,
      'execution_contract':{'requires':[],'not_after':[{'tool':name,'arguments':{},'field':'done','equals':True}] if once else []}}


class SkinSession:
    def __init__(self,score):self.score=score;self.record=SymptomSession();self.history=[]
    def catalog(self,text):
        r=ToolRegistry()
        def record():
            before=self.record.state;patch={};decisions={}
            def score_symptom(q,options,context):
                return self.score('symptom',{'question':q,'options':options,'context':context})['raw_scores']
            for field in SYMPTOMS:
                context='대상 증상: '+NAMES[field]+'\n이전 상태: '+before[field]+'\n이번 사용자 발화: '+text
                d=choose(score_symptom,SYMPTOM_QUESTION,SYMPTOM_DESCRIPTIONS,context);decisions[field]=d
                if d['choice']!='unchanged' and d['choice']!=before[field]:patch[field]=d['choice']
            self._symptom_decisions=decisions
            if not patch:return {'ok':False,'reason':'no_supported_change','state':before,'version':self.record.version}
            result=self.record.update(patch);return {**result,'done':True,'patch':patch}
        handlers={
          'record_skin_symptoms':(definition('record_skin_symptoms','Record or correct the current user\'s explicitly stated current skin symptoms: dryness, breakout, redness, stinging, itching. The tool extracts these five states from this message and updates the in-memory record. Do not use for general questions, other people or hypothetical symptoms. It does not store products or usage time. Returns ok=true, done=true, patch and state when changed; otherwise an error without updating. Do not repeat after success in this turn.',True),record),
          'read_skin_record':(definition('read_skin_record','Read and show this user\'s already saved skin symptom record when the user asks to see it. Read-only: does not infer new symptoms or update the record. Returns ok=true, done=true and state.'),lambda:{'ok':True,'done':True,'state':self.record.state,'version':self.record.version})}
        config=json.loads(CONFIG.read_text(encoding='utf-8'));enabled=config['enabled']
        if not isinstance(enabled,list) or len(set(enabled))!=len(enabled) or any(k not in handlers for k in enabled):raise ValueError('Invalid skin tool configuration')
        for name in enabled:r.register(*handlers[name])
        return r
    def turn(self,text):
        before=self.record.state;registry=self.catalog(text);self._symptom_decisions={}
        # Keep the last two user turns with their ACTUAL tool outcomes; never feed a
        # Qwen-written claim into the execution history as if it were a tool result.
        trace=run_turn(text,registry,self.history[-2:],self.score,lambda:self.record.version)
        writes=[e['result'] for e in trace['events'] if e['tool']=='record_skin_symptoms' and e['result'].get('ok') is True]
        reads=[e for e in trace['events'] if e['tool']=='read_skin_record' and e['result'].get('ok') is True]
        patch={k:v for k,v in self.record.state.items() if v!=before[k]}
        action='record' if writes else 'show' if reads else 'none' if trace['stop_reason']=='model_stop' else 'ask'
        self.history.append({'role':'user','content':text,'actual_tools':[{'tool':e['tool'],'ok':e['result'].get('ok')} for e in trace['events']]});self.history=self.history[-2:]
        return {**trace,'before':before,'after':self.record.state,'patch':patch,'action':action,'input':text,'symptom_decisions':self._symptom_decisions,
          'available_tools':[{'name':d['name'],'description':d['description']} for d in registry.definitions()]}


class DomainSkinSession(SkinSession):
    """Use the already skin-trained decision format, one operation per message.

    This is NOT the research multi-tool loop. The distinction is exposed in status
    and every trace. State persists across user turns; general coreference does not.
    """
    def turn(self,text):
        before=self.record.state;registry=self.catalog(text);defs=registry.definitions();self._symptom_decisions={}
        aliases={'record_skin_symptoms':'record','read_skin_record':'show'}
        by={aliases.get(d['name'],d['name']):d for d in defs}
        options={k:TOOL_DESCRIPTIONS.get(k,d['description']) for k,d in by.items()}
        options.update({k:TOOL_DESCRIPTIONS[k] for k in ['ask','none']})
        listing='\n'.join('- '+k for k in options)
        context='현재 기록: '+str(before)+'\n사용자 발화: '+text+'\n사용 가능한 동작:\n'+listing
        def routing(q,opts,c):return self.score('symptom',{'question':q,'options':opts,'context':c})['raw_scores']
        decision=choose(routing,TOOL_QUESTION,options,context);choice=decision['choice'];events=[];reason='no_tool_chosen';name=by[choice]['name'] if choice in by else 'no_tool';condition=None
        if choice in by:
            from agent.contract_filter_v34 import readiness
            condition=readiness(by[choice],[])
            if not condition['eligible']:reason='condition_not_met'
            else:
                try:
                    result=registry.invoke(name,{});reason='single_action' if result['ok'] else 'tool_error'
                except Exception:result={'ok':False,'reason':'handler_error','effects_unknown':True};reason='handler_error'
                events.append({'tool':name,'arguments':{},'executed':True,'result':result})
        patch={k:v for k,v in self.record.state.items() if v!=before[k]}
        successful=events and events[0]['result'].get('ok') is True
        action=choice if successful and choice in ['record','show'] else 'tool' if successful else 'ask' if choice=='record' or reason not in ['no_tool_chosen','single_action'] else choice if choice in ['ask','none'] else 'none'
        step={'index':0,'decision':{'raw_selected':name,'selected':name if events else 'no_tool','reason':reason,'condition':condition,'domain_decision':decision},'event':events[0] if events else None}
        return {'before':before,'after':self.record.state,'patch':patch,'action':action,'input':text,'symptom_decisions':self._symptom_decisions,
          'events':events,'steps':[step],'stop_reason':reason,'model_stopped':False,'complete':False,'engine':'domain-single-action',
          'available_tools':[{'name':d['name'],'description':d['description']} for d in defs]}
