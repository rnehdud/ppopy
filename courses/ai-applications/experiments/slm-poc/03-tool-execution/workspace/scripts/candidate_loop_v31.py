"""Run complete independent loops, with no cached decisions or training."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.candidate_loop_data_v31 import DATA,OUT,SELECTOR,GATE,verify,read,save,digest
from scripts.result_loop_split_v27 import Engine
from agent.candidate_loop_v31 import run,World,public_tools
from agent.result_loop_split_v27 import selector_view,gate_view

class UncachedEngine(Engine):
    def score(self,v):
        self.cache.clear()
        return super().score(v)

def main():
    cfg=verify()
    if (OUT/'started.json').exists():raise FileExistsError('Execution protected')
    save(OUT/'started.json',{'protocol':digest(DATA/'protocol.json')});s,g=UncachedEngine(SELECTOR),UncachedEngine(GATE);scenarios=read(DATA/'scenarios.json');results=[]
    warm=scenarios[0];w=World(warm);ts=public_tools(warm['tools']);v=selector_view(warm['case']['request'],ts,w.events,warm['option_order']);s.score(v);g.score(gate_view(ts[0],v['context']))
    for i,scenario in enumerate(scenarios):
        order=cfg['strategies'] if i%2==0 else list(reversed(cfg['strategies']))
        for strategy in order:
            trace=run(scenario,s.score,g.score,strategy,cfg['threshold'],cfg['max_steps']);results.append(trace)
        if (i+1)%12==0:
            save(OUT/'episodes-partial.json',results);print('V31 scenarios',i+1,'/',len(scenarios),'episodes',len(results),flush=True)
    save(OUT/'episodes.json',results);save(OUT/'complete.json',{'no_training':True,'no_deployment':True,'warmup_selector_forwards':1,'warmup_gate_forwards':1,'selector_forwards_including_warmup':s.calls,'gate_forwards_including_warmup':g.calls,'selector_max_tokens':s.max_tokens,'gate_max_tokens':g.max_tokens,'uncached':True})
    verify();print('V31 COMPLETE',len(results),'episodes',flush=True)
if __name__=='__main__':main()
