import policy from "../../skin_engine/config/app_native_account_owner_local.json";
import {captureNativeAccountReviewContext,createNativeAccountProviderLocal,nativeAccountProviderConfigured,
  NativeAccountProviderUnavailable,type NativeAccountProviderFrame,type NativeAccountReviewContext} from "./nativeAccountProviderLocal";
import {awaitSearchRequest} from "./searchRequestLifetime";
import {createNativeAccountClosureProjectionLocal} from "./nativeAccountClosureProjectionLocal";

type Provider=ReturnType<typeof createNativeAccountProviderLocal>;
const fail=()=>new NativeAccountProviderUnavailable();
export function nativeAccountOwnerConfigured(){
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
    maximum_transition_ms:5000,creation:"explicit_synthetic_context_only_private_provider_factory",
    replacement:"mask_retire_and_strict_dispose_previous_provider_before_creating_next",
    driver:"distinct_JS_object_no_OS_identity_attestation",reentry:"reject_while_connecting_no_queue_or_retry",
    failure:"terminal_owner_discard_late_provider_preserve_credentials_and_intent",
    UI_detach:"StrictMode_detach_only_external_account_owner_disposes",questions:"routine_state_and_safety_2_plus_conditional_1",
    registration:"OFF_review_owner_not_default_app_login_or_native_plugin"};
  return Object.keys(policy).sort().join("|")===Object.keys(expected).sort().join("|")&&
    Object.entries(expected).every(([k,v])=>policy[k as keyof typeof policy]===v)&&nativeAccountProviderConfigured();
}

/** Private providers share one caller-owned transition fence. No adoption of
 * externally opened providers, authentication, consent, or automatic reads.
 * A strict JS/native disposal receipt is not proof of OS or remote cleanup. */
export function createNativeAccountOwnerLocal(deploymentContext:"synthetic_test"){
  if(deploymentContext!=="synthetic_test"||!nativeAccountOwnerConfigured())throw fail();
  let frame:NativeAccountProviderFrame=Object.freeze({state:"empty",connection:null}),epoch=0,busy=false;
  const closure=createNativeAccountClosureProjectionLocal();
  let provider:Provider|null=null,active:AbortController|null=null,cleanupFailed=false,unsubscribe:(()=>void)|null=null;
  const listeners=new Set<()=>void>(),drivers=new WeakSet<object>(),providers=new Set<Provider>();
  const pending=new Set<Promise<unknown>>(),cleanups=new Set<Promise<unknown>>(),receipts=new WeakMap<Provider,Promise<void>>();
  const retired=()=>frame.state==="retired";
  const track=<T,>(set:Set<Promise<unknown>>,p:Promise<T>)=>{set.add(p);void p.then(()=>set.delete(p),()=>set.delete(p));return p;};
  const notify=()=>{for(const listener of [...listeners])try{listener();}catch{/* Sibling masking must still run. */}};
  const publish=(state:NativeAccountProviderFrame["state"],connection:NativeAccountProviderFrame["connection"]=null)=>{
    frame=Object.freeze({state,connection});notify();
  };
  const disposeProvider=(p:Provider)=>{
    let receipt=receipts.get(p);
    if(!receipt){
      receipt=track(cleanups,Promise.resolve().then(()=>p.dispose()).then(()=>{providers.delete(p);})
        .catch(()=>{cleanupFailed=true;throw fail();}));receipts.set(p,receipt);
    }
    return receipt;
  };
  const invalidate=()=>{
    if(retired())return;epoch++;frame=Object.freeze({state:"retired",connection:null});
    closure.retire();
    unsubscribe?.();unsubscribe=null;active?.abort(fail());
    for(const p of providers){p.invalidate();void disposeProvider(p).catch(()=>{});}notify();
  };
  const valid=(own:number,s:NativeAccountReviewContext)=>{
    // Calls through a previous provider must not retire its successor.
    if(own!==epoch||retired())return false;
    try{
      if(!nativeAccountOwnerConfigured()||s.options.isCurrent()!==true||s.options.isNativeIOS()!==true)throw fail();
      return own===epoch&&!retired();
    }catch{invalidate();return false;}
  };
  const requireCurrent=(own:number,s:NativeAccountReviewContext)=>{if(!valid(own,s))throw fail();};
  return {
    snapshot:()=>frame,
    accountClosureSnapshot:closure.snapshot,
    subscribeAccountClosure:closure.subscribe,
    subscribe(listener:()=>void){listeners.add(listener);return()=>{listeners.delete(listener);};},
    async replaceSyntheticContext(value:NativeAccountReviewContext,signal?:AbortSignal):Promise<void>{
      if(retired()||busy||!nativeAccountOwnerConfigured())throw fail();signal?.throwIfAborted();
      const next=captureNativeAccountReviewContext(value);
      // Trusted validation callbacks may reenter; reject before retiring anyone.
      if(retired()||busy||drivers.has(next.driver))throw fail();signal?.throwIfAborted();
      const prior=provider,own=++epoch,controller=new AbortController();busy=true;active=controller;provider=null;
      unsubscribe?.();unsubscribe=null;
      const abort=()=>invalidate();signal?.addEventListener("abort",abort,{once:true});
      closure.reset();publish("connecting");prior?.invalidate();
      try{
        await awaitSearchRequest(()=>track(pending,(async()=>{
          requireCurrent(own,next);controller.signal.throwIfAborted();
          if(prior)await disposeProvider(prior);
          requireCurrent(own,next);controller.signal.throwIfAborted();
          // No new provider or channel exists before the previous receipt.
          drivers.add(next.driver);const candidate=createNativeAccountProviderLocal(deploymentContext);
          providers.add(candidate);provider=candidate;
          closure.follow(candidate);
          unsubscribe=candidate.subscribe(()=>{
            if(own===epoch&&!retired()&&candidate.snapshot().state==="retired")invalidate();
          });
          await candidate.replaceSyntheticContext({...next,options:{...next.options,isCurrent:()=>valid(own,next)}},controller.signal);
          requireCurrent(own,next);controller.signal.throwIfAborted();
          const child=candidate.snapshot();if(child.state!=="ready"||!child.connection)throw fail();
          publish("ready",child.connection);requireCurrent(own,next);controller.signal.throwIfAborted();
        })()),async()=>{invalidate();},controller.signal,{milliseconds:policy.maximum_transition_ms,error:fail()});
      }catch{invalidate();throw fail();}
      finally{signal?.removeEventListener("abort",abort);if(active===controller)active=null;busy=false;}
    },
    invalidate,
    async dispose(){
      invalidate();
      // Unknown ACKs release the caller at the configured deadline. Failure
      // remains terminal even after tracked promises settle or a late ACK arrives.
      await awaitSearchRequest(async()=>{
        await Promise.allSettled([...pending,...cleanups]);if(cleanupFailed)throw fail();
      },async()=>{},undefined,{milliseconds:policy.maximum_transition_ms,error:fail()});
    },
  };
}
