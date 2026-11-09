import {checkedPublicAppTransportBase} from "./publicAppTransport";
import policy from "../../skin_engine/config/app_public_loop_client_review.json";
import {createPublicLoopStatePort,type PublicLoopStatePort} from "./publicLoopState";
import {createPublicLoopWorkerPort,type PublicLoopWorkerPort} from "./publicLoopWorker";
import {createPublicFrequencyPort} from "./publicLoopFrequency";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";

export interface OriginalPublicLoopConnection {
  state:PublicLoopStatePort;worker:PublicLoopWorkerPort;
  isCurrent():boolean;invalidate():void;
}
export type OriginalPublicLoopFactory=(member:{loadToken:()=>Promise<string|null>;onMemberChanged():void})=>OriginalPublicLoopConnection;
export function assertOriginalPublicLoopApp(){
  if(policy.version!=="1.0.0-public-loop-app-20261021" || policy.scope!=="public_service_loop_UI_not_TEST_or_research" || [policy.research_enabled,policy.automatic_retry,
    policy.automatic_poll,policy.registration_confirms_actual_use,policy.intake_review_dispatches_engine].some(v=>v!==false) ||
    policy.requires_current_member_and_separate_history_consent!==true || policy.requires_acknowledged_portfolio_revision!==true ||
    policy.requires_canonical_portfolio_after_frequency_view!==true || policy.state_profile!=="routine_state_and_safety" ||
    JSON.stringify(policy.required_ports)!==JSON.stringify(["app_public_loop_state_http_review","app_public_loop_worker_http_review","app_public_loop_frequency_http_review"]))throw new Error("Original public app review unavailable");
}
/** Explicit original public native transport factory. The shell supplies its original
 * member/consent lifetime; no native credential store or installed default. */
export function createOriginalPublicLoopFactory({baseUrl,fetcher}:{baseUrl:string;fetcher:typeof fetch}):OriginalPublicLoopFactory{
  assertOriginalPublicLoopApp();const baseline=JSON.stringify(policy);
  checkedPublicAppTransportBase(baseUrl,fetcher);
  return ({loadToken,onMemberChanged})=>{
    let live=true;const pending=new Set<AbortController>();
    const current=()=>{try{checkedPublicAppTransportBase(baseUrl,fetcher);return live && JSON.stringify(policy)===baseline;}catch{return false;}};
    const invalidate=()=>{live=false;for(const c of pending)c.abort();pending.clear();};
    const gate=()=>{assertOriginalPublicLoopApp();if(!current())throw new Error("Original public connection retired");};
    const changed=()=>{if(!live)return;invalidate();onMemberChanged();};
    const token=async()=>{gate();const value=await loadToken();gate();return value;};
    const state=createPublicLoopStatePort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
    const worker=createPublicLoopWorkerPort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
    const frequency=createPublicFrequencyPort({baseUrl,fetcher,loadToken:token,onMemberChanged:changed});
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
