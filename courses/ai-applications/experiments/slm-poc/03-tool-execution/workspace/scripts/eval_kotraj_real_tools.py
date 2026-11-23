"""Run the saved choice model against real local, sandboxed Python tools.

Author-written, exploratory Korean examples. No Qwen or external APIs. Each
tool takes zero arguments; symptom-specific tools have a fixed effect. Files
are created only in a temporary per-scenario directory and removed afterward.
Model choice is executed as-is; scores are not confidence in correctness.
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
OUT=ROOT/'output/kotraj-tool-execution-v1.json'
QUESTION='사용자 요청과 대화 내용을 보고 다음에 실행할 동작 하나를 선택하세요.'
OPTIONS={
 'record_itch':'사용자 자신의 현재 가려움이 있다고 기록한다. 인자는 필요 없다.',
 'record_dry':'사용자 자신의 현재 건조함이 있다고 기록한다. 인자는 필요 없다.',
 'read_record':'저장된 사용자 피부 상태 기록을 읽어서 보여준다. 인자는 필요 없다.',
 'get_time':'현재 컴퓨터의 날짜와 시간을 조회한다. 인자는 필요 없다.',
 'no_tool':'지금은 도구를 호출하지 않고 사용자에게 직접 답하거나 필요한 정보를 확인한다.',
}
SYSTEM=('사용 가능한 도구는 피부 가려움 기록, 피부 건조함 기록, 기록 확인, 현재 시간 확인이다. '
        '기록과 무관한 대화나 제공되지 않은 기능은 도구를 호출하지 않는다. '
        '사용자 본인이 아닌 사람이나 가정에 관한 증상은 본인 기록에 넣지 않는다.')

# Expected label, expected resulting record, and response checks are fixed
# BEFORE running the model. Scenarios do not share state.
CASES=[
 ('itch_then_read', [('제 피부가 지금 가려워요. 가려움을 기록해 주세요.','record_itch',['가려움']),
                     ('방금 저장한 피부 기록을 보여 주세요.','read_record',['가려움'])]),
 ('dry_then_read', [('제 얼굴이 건조해요. 건조함으로 기록해 주세요.','record_dry',['건조함']),
                    ('현재 피부 기록을 확인해 줘요.','read_record',['건조함'])]),
 ('time', [('지금 몇 시인지 알려 주세요.','get_time',[])]),
 ('greeting', [('안녕하세요!','no_tool',[])]),
 ('thanks', [('고마워요.','no_tool',[])]),
 ('unsupported_product', [('저한테 선크림을 검색해 주세요.','no_tool',[])]),
 ('unsupported_recommend', [('제 피부에 맞는 화장품을 추천해 주세요.','no_tool',[])]),
 ('other_person', [('제 친구 얼굴이 건조하대요.','no_tool',[])]),
 ('hypothetical', [('만약 피부가 가렵다면 어떻게 해야 하나요?','no_tool',[])]),
 ('negative', [('지금 저는 가렵지 않아요.','no_tool',[])]),
 ('unknown', [('오늘 가려운지 잘 모르겠어요.','no_tool',[])]),
 ('empty_read', [('아직 아무것도 기록하지 않았는데 제 기록을 보여 주세요.','read_record',[])]),
 ('time_then_dry', [('현재 시간을 확인해 주세요.','get_time',[]),
                    ('저는 피부가 건조해요. 건조함을 저장해 주세요.','record_dry',['건조함'])]),
 ('itch_time_read', [('저는 가려움이 있어요. 기록 부탁해요.','record_itch',['가려움']),
                     ('지금 시간은 어떻게 돼요?','get_time',['가려움']),
                     ('저장해 둔 피부 상태를 확인해 주세요.','read_record',['가려움'])]),
 ('dry_then_other', [('제가 건조해요. 제 기록에 남겨 주세요.','record_dry',['건조함']),
                     ('동생은 가렵다고 하네요.','no_tool',['건조함'])]),
 ('no_clear', [('저장된 피부 기록을 모두 지워 주세요.','no_tool',[])]),
]

def run(scorer):
 results=[]
 for name,turns in CASES:
  with tempfile.TemporaryDirectory(prefix='skin_tool_test_') as folder:
   path=Path(folder)/'record.json';path.write_text('[]',encoding='utf8')
   def load():return json.loads(path.read_text(encoding='utf8'))
   def add(symptom):
    data=load()
    if symptom not in data:data.append(symptom)
    path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
    return {'stored':data}
   def clock():return {'local_time':datetime.now().astimezone().isoformat(timespec='seconds')}
   tools={'record_itch':lambda:add('가려움'),'record_dry':lambda:add('건조함'),
          'read_record':lambda:{'stored':load()},'get_time':clock}
   history=[]
   for number,(text,expected_action,expected_state) in enumerate(turns,1):
    before=load()
    messages=[{'role':'system','content':SYSTEM+' 현재 저장된 기록: '+json.dumps(before,ensure_ascii=False)}]+history
    context='대화:\n'+json.dumps(messages,ensure_ascii=False)+'\n이번 사용자 발화: '+text
    scores=scorer(QUESTION,OPTIONS,context)
    selected=max(OPTIONS,key=lambda k:scores[k])
    executed=False;result=None;error=None
    try:
     if selected!='no_tool':result=tools[selected]();executed=True
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    actual=load()
    state_ok=sorted(actual)==sorted(expected_state)
    result_ok=(error is None and (selected!='read_record' or result=={'stored':actual}) and
               (selected!='get_time' or bool(result and result.get('local_time'))))
    turn={'scenario':name,'turn':number,'input':text,'options':list(OPTIONS),
          'expected_action':expected_action,'selected':selected,'scores':scores,
          'action_ok':selected==expected_action,'executed':executed,'tool_result':result,'error':error,
          'before':before,'after':actual,'expected_after':expected_state,'state_ok':state_ok,'result_ok':result_ok}
    results.append(turn)
    history.extend([{'role':'user','content':text},
                    {'role':'assistant','content':json.dumps({'선택':selected,'실행결과':result},ensure_ascii=False)}])
 return results

def summary(results):
 scenarios={r['scenario'] for r in results}
 return {'turns':len(results),'correct_selection':sum(r['action_ok'] for r in results),
         'correct_state':sum(r['state_ok'] for r in results),'actual_tool_calls':sum(r['executed'] for r in results),
         'execution_errors':sum(r['error'] is not None for r in results),
         'all_correct_scenarios':sum(all(r['action_ok'] and r['state_ok'] and r['result_ok'] for r in results if r['scenario']==s) for s in scenarios),
         'scenarios':len(scenarios)}

def main():
 if OUT.exists():raise FileExistsError('Existing result protected')
 scorer=LocalChoiceScorer(MODEL,BEFORE)
 before=run(scorer);print('before',json.dumps(summary(before),ensure_ascii=False),flush=True)
 set_peft_model_state_dict(scorer.model,load_file(str(AFTER/'adapter_model.safetensors')));scorer.model.eval()
 after=run(scorer);print('after',json.dumps(summary(after),ensure_ascii=False),flush=True)
 out={'limitations':'author-written small Korean test; sandboxed local tools, no arguments, no external services or Qwen; not independent human review',
      'before_summary':summary(before),'after_summary':summary(after),'before':before,'after':after}
 OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 for r in after:
  print(json.dumps({k:r[k] for k in ('scenario','turn','input','expected_action','selected','executed','tool_result','state_ok')},ensure_ascii=False),flush=True)
 print('Saved:',OUT,flush=True)
if __name__=='__main__':main()
