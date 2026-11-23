"""Compare repeated-action filtering in isolated exploratory development cases.

Filtering is a backend rule, not an improvement in model weights. It is only
appropriate here because the four sandbox actions never need repeating within
one request. It must not be generalized to tools where repetition is valid.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.local_choice_scorer_v1 import LocalChoiceScorer
from scripts.train_choice_agent_v1 import MODEL
from scripts.eval_kotraj_multistep_loop import run,summary,AFTER

OUT=ROOT/'output/kotraj-loop-guard-dev-v1.json'
def mask_completed(base):
 def wrapped(question,options,context):
  events=json.loads(context.rsplit('\n이미 실행한 결과: ',1)[1])
  completed={event['도구'] for event in events}
  allowed={k:v for k,v in options.items() if k not in completed}
  values=base(question,allowed,context)
  # Zeros denote filtered choices, not a model probability.
  return {key:values.get(key,0.0) for key in options}
 return wrapped
def main():
 if OUT.exists():raise FileExistsError('Existing output protected')
 scorer=LocalChoiceScorer(MODEL,AFTER)
 ordinary=run(scorer);guarded=run(mask_completed(scorer))
 result={'raw_summary':summary(ordinary),'guarded_summary':summary(guarded),'raw':ordinary,'guarded':guarded,
   'note':'exploratory same 10 authored cases; completed actions removed from candidate set, not an independent test'}
 OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'raw':summary(ordinary),'guarded':summary(guarded)},ensure_ascii=False),flush=True)
 for r in guarded:print(json.dumps({k:r[k] for k in ('scenario','expected_sequence','actual_sequence','stop')},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
