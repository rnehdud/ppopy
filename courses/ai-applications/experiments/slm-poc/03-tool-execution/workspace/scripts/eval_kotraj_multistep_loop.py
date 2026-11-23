"""Exploratory sequential calls: select, execute, observe, select again.

All functions run in a temporary sandbox and take no arguments. No Qwen,
external API, user records or hidden thoughts are used. Never install this
prototype into the real demo automatically.
"""
import json,sys,tempfile
from datetime import datetime
from pathlib import Path
from safetensors.torch import load_file
from peft import set_peft_model_state_dict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.local_choice_scorer_v1 import LocalChoiceScorer
from scripts.train_choice_agent_v1 import MODEL

BEFORE=ROOT/'adapters/cosmetics-chat-v1/step-0100'
AFTER=ROOT/'output/training/kotraj-kaggle-complete-v1/kotraj_choice/kotraj-choice-full-gpu-v1/final_adapter'
OUT=ROOT/'output/kotraj-multistep-loop-v1.json'
QUESTION='사용자 요청과 이미 실행된 결과를 보고 다음에 실행할 동작 하나를 선택하세요.'
OPTIONS={
 'record_itch':'사용자 자신의 현재 가려움이 있다고 기록한다. 인자는 필요 없다.',
 'record_dry':'사용자 자신의 현재 건조함이 있다고 기록한다. 인자는 필요 없다.',
 'read_record':'저장된 사용자 피부 상태 기록을 읽어서 보여준다. 인자는 필요 없다.',
 'get_time':'현재 컴퓨터의 날짜와 시간을 조회한다. 인자는 필요 없다.',
 'no_tool':'필요한 도구 작업이 끝났거나 사용할 도구가 없으면 도구를 더 호출하지 않는다.',
}
SYSTEM=('사용자의 요청을 수행하기 위해 도구를 하나씩 선택한다. 실행한 도구와 실제 결과를 확인한다. '
        '이미 수행한 일을 반복하지 않고, 필요하지 않거나 사용 가능한 도구가 없으면 no_tool을 선택한다. '
        '도구 목록에 없는 작업을 할 수 있다고 추정하지 않는다.')
# Expected sequence includes the model choosing no_tool to stop; a forced stop
# or prevention of a repeated call cannot count as successful completion.
CASES=[
 ('itch_read','제 피부가 가려워요. 가려움을 기록하고 나서 저장된 기록을 보여 주세요.', ['record_itch','read_record','no_tool'],['가려움']),
 ('dry_read','피부가 건조해요. 건조하다고 먼저 기록하고 그다음 기록을 보여 주세요.', ['record_dry','read_record','no_tool'],['건조함']),
 ('time_read','현재 시간을 먼저 확인하고, 그다음 저장된 피부 기록을 보여 주세요.', ['get_time','read_record','no_tool'],[]),
 ('itch_only','지금 저는 가려워요. 가려움을 기록해 주세요.', ['record_itch','no_tool'],['가려움']),
 ('time_only','지금 몇 시인가요?', ['get_time','no_tool'],[]),
 ('read_only','제 피부 기록을 보여 주세요.', ['read_record','no_tool'],[]),
 ('greeting','안녕하세요!', ['no_tool'],[]),
 ('unsupported','화장품을 검색해 주세요.', ['no_tool'],[]),
 ('other','친구는 피부가 가렵다고 해요.', ['no_tool'],[]),
 ('unclear','이것을 해 주세요.', ['no_tool'],[]),
]

def run(scorer):
 results=[]
 for name,text,expected,expected_record in CASES:
  with tempfile.TemporaryDirectory(prefix='skin_loop_') as folder:
   path=Path(folder)/'record.json';path.write_text('[]',encoding='utf8')
   def read():return json.loads(path.read_text(encoding='utf8'))
   def record(v):
    entries=read()
    if v not in entries:entries.append(v)
    path.write_text(json.dumps(entries,ensure_ascii=False),encoding='utf8')
    return {'저장된 기록':entries}
   tools={'record_itch':lambda:record('가려움'),'record_dry':lambda:record('건조함'),
          'read_record':lambda:{'저장된 기록':read()},
          'get_time':lambda:{'현재 시간':datetime.now().astimezone().isoformat(timespec='seconds')}}
   events=[];steps=[];stop='limit';done=set()
   for i in range(4):
    context='대화:\n'+json.dumps([{'role':'system','content':SYSTEM}],ensure_ascii=False)+'\n이번 사용자 발화: '+text+'\n이미 실행한 결과: '+json.dumps(events,ensure_ascii=False)
    try:scores=scorer(QUESTION,OPTIONS,context)
    except (ValueError,RuntimeError) as e:
     stop='model_error';steps.append({'error':str(e)});break
    choice=max(OPTIONS,key=lambda k:scores[k]);step={'number':i+1,'choice':choice,'scores':scores,'executed':False}
    if choice=='no_tool':stop='model_finished';steps.append(step);break
    if choice in done:
     stop='repeat_blocked';steps.append(step);break
    try:
     outcome=tools[choice]();step.update(executed=True,result=outcome);done.add(choice)
     events.append({'도구':choice,'결과':outcome});steps.append(step)
    except Exception as e:
     step['error']=type(e).__name__+': '+str(e);steps.append(step);stop='tool_error';break
   actual=[s['choice'] for s in steps if 'choice' in s];after=read()
   results.append({'scenario':name,'input':text,'expected_sequence':expected,'actual_sequence':actual,
       'expected_record':expected_record,'actual_record':after,'sequence_ok':actual==expected,
       'record_ok':sorted(after)==sorted(expected_record),'stop':stop,'steps':steps})
 return results
def summary(rows):
 return {'scenarios':len(rows),'correct_sequence':sum(r['sequence_ok'] for r in rows),
         'correct_record':sum(r['record_ok'] for r in rows),
         'model_finished':sum(r['stop']=='model_finished' for r in rows),
         'repeat_blocked':sum(r['stop']=='repeat_blocked' for r in rows),
         'model_or_tool_error':sum(r['stop'] in ('model_error','tool_error') for r in rows)}
def main():
 if OUT.exists():raise FileExistsError('Existing result protected')
 scorer=LocalChoiceScorer(MODEL,BEFORE)
 before=run(scorer);print('before',json.dumps(summary(before),ensure_ascii=False),flush=True)
 set_peft_model_state_dict(scorer.model,load_file(str(AFTER/'adapter_model.safetensors')));scorer.model.eval()
 after=run(scorer);print('after',json.dumps(summary(after),ensure_ascii=False),flush=True)
 result={'before_summary':summary(before),'after_summary':summary(after),'before':before,'after':after,
         'note':'small author-written test, local temporary tools, zero arguments, no Qwen; expected sequence may have legitimate alternatives'}
 OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 for r in after:print(json.dumps({k:r[k] for k in ('scenario','input','expected_sequence','actual_sequence','actual_record','stop')},ensure_ascii=False),flush=True)
 print('Saved:',OUT,flush=True)
if __name__=='__main__':main()
