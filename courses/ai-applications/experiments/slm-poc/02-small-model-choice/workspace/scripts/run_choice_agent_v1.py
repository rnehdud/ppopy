"""Interactive local Jev-style mock agent: no LLM and no real KB access.

Run after training. State lives only in this process; scores are not calibrated.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.choice_agent_v1 import ChoiceAgent
from scripts.train_choice_agent_v1 import MODEL,OUT
from scripts.train_question_conditioning_v1 import OUT as QUESTION_OUT

def main():
    from agent.local_choice_scorer_v1 import LocalChoiceScorer
    p=argparse.ArgumentParser()
    p.add_argument('--experiment',choices=['routing','questions'],default='routing',help='which local adapter experiment to use')
    p.add_argument('--model',choices=['before','selected','last'],default='selected')
    p.add_argument('--once',help='single Korean user turn, otherwise interactive')
    args=p.parse_args()
    location=OUT if args.experiment=='routing' else QUESTION_OUT
    result=json.loads((location/'results.json').read_text(encoding='utf-8'))
    entry=result['experiments'][args.model]
    scorer=LocalChoiceScorer(MODEL,ROOT/entry['adapter'])
    def mock_lookup(query,state):
        return {'ok':True,'mock':True,'message':'모의 검색입니다. 실제 지식베이스는 연결되어 있지 않습니다.',
                'query':query,'state':state}
    agent=ChoiceAgent(scorer,lookup=mock_lookup)
    print('실험용: 점수는 교정되지 않았고 지식베이스 검색은 모의 실행입니다. 종료: /quit',flush=True)
    def turn(text):
        print(json.dumps(agent.turn(text),ensure_ascii=False,indent=2),flush=True)
    if args.once:turn(args.once);return
    while True:
        try:text=input('사용자> ').strip()
        except (EOFError,KeyboardInterrupt):break
        if text in ['/quit','/exit']:break
        if text:
            try:turn(text)
            except (ValueError,RuntimeError) as e:print('오류: '+str(e),flush=True)
if __name__=='__main__':main()
