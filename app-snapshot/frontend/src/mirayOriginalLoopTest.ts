import {checkedLoopTestTransportBase} from "./mirayLoopTestTransport";
import policy from "../../skin_engine/config/miray_closed_loop_app_test.json";
import {createTestLoopStatePort,type TestLoopStatePort} from "./mirayClosedLoopStateTest";
import {createTestLoopWorkerPort,type TestLoopWorkerPort} from "./mirayClosedLoopWorkerTest";
import {createTestFrequencyPort} from "./mirayClosedLoopFrequencyTest";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";

export interface OriginalLoopTestConnection {
  state:TestLoopStatePort;worker:TestLoopWorkerPort;
  isCurrent():boolean;invalidate():void;
}
export type OriginalLoopTestFactory=(member:{loadToken:()=>Promise<string|null>;onMemberChanged():void})=>OriginalLoopTestConnection;
export function assertOriginalLoopAppTest(){
  if(policy.scope!=="aws_test_candidate_not_applied" || [policy.runtime_enabled,policy.installed_factory,policy.automatic_retry,
    policy.automatic_poll,policy.registration_confirms_actual_use,policy.intake_review_dispatches_engine].some(v=>v!==false) ||
    policy.requires_current_member_and_separate_history_consent!==true || policy.requires_acknowledged_portfolio_revision!==true ||
    policy.requires_canonical_portfolio_after_frequency_view!==true)throw new Error("Original TEST app review unavailable");
}
/** Explicit loopback or branded native TEST transport factory. The shell supplies its original
 * member/consent lifetime; no native credential store or installed default. */
export function createOriginalLoopTestFactory({baseUrl,fetcher}:{baseUrl:string;fetcher:typeof fetch}):OriginalLoopTestFactory{
  assertOriginalLoopAppTest();const baseline=JSON.stringify(policy);
  checkedLoopTestTransportBase(baseUrl,fetcher);
  return ({loadToken,onMemberChanged})=>{
    let live=true;const pending=new Set<AbortController>();
    const current=()=>live && JSON.stringify(policy)===baseline;
    const invalidate=()=>{live=false;for(const c of pending)c.abort();pending.clear();};
    const gate=()=>{assertOriginalLoopAppTest();if(!current())throw new Error("Original TEST connection retired");};
    const changed=()=>{if(!live)return;invalidate();onMemberChanged();};
    const token=async()=>{gate();const value=await loadToken();gate();return value;};
    const state=createTestLoopStatePort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
    const worker=createTestLoopWorkerPort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
    const frequency=createTestFrequencyPort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
    const run=async<T,>(options:MemberStatusReadOptions|undefined,operation:(scope:MemberStatusReadOptions)=>Promise<T>)=>{
      gate();options?.signal?.throwIfAborted();if(options?.isCurrent && options.isCurrent()!==true)throw new Error("Original consumer retired");
      const c=new AbortController(),abort=()=>c.abort();pending.add(c);options?.signal?.addEventListener("abort",abort,{once:true});
      const scope={signal:c.signal,isCurrent:()=>{try{return current() && !c.signal.aborted && (!options?.isCurrent || options.isCurrent()===true);}catch{return false;}}};
      try{const value=await operation(scope);gate();c.signal.throwIfAborted();if(!scope.isCurrent())throw new Error("Original consumer retired");return value;}
      finally{options?.signal?.removeEventListener("abort",abort);pending.delete(c);}
    };
    return {isCurrent:current,invalidate,
      state:{read:o=>run(o,s=>state.read(s)),readEntry:o=>run(o,s=>state.readEntry!(s)),register:(r,o)=>run(o,s=>state.register(r,s)),
        confirmAddedProduct:(r,o)=>run(o,s=>state.confirmAddedProduct!(r,s)),
        episode:{read:o=>run(o,s=>state.episode.read(s)),confirmActual:(r,o)=>run(o,s=>state.episode.confirmActual(r,s)),saveFollowup:(r,o)=>run(o,s=>state.episode.saveFollowup(r,s)),
          frequencyCorrections:{read:o=>run(o,s=>frequency.projection.read(s)),confirm:(r,o)=>run(o,s=>frequency.projection.confirm(r,s))}}},
      worker:{resume:(t,o)=>run(o,s=>{if(!worker.resume)throw new Error("Resume unavailable");return worker.resume(t,s);}),read:o=>run(o,s=>worker.read(s)),submit:(t,a,v,o)=>run(o,s=>worker.submit(t,a,v,s))}};
  };
}
