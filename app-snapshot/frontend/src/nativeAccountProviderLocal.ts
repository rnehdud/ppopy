import policy from "../../skin_engine/config/app_native_account_provider_local.json";
import {createNativeRecoveryMemberWorkspaceLocal} from "./nativeRecoveryMemberWorkspaceLocal";
import {awaitSearchRequest} from "./searchRequestLifetime";
import {createNativeAccountClosureProjectionLocal} from "./nativeAccountClosureProjectionLocal";

type Factory=typeof createNativeRecoveryMemberWorkspaceLocal;
type Connection=Awaited<ReturnType<Factory>>;
export type NativeAccountReviewContext={fetcher:Parameters<Factory>[0];driver:Parameters<Factory>[1];options:Parameters<Factory>[2]};
export type NativeAccountProviderFrame={state:"empty"|"connecting"|"ready"|"retired";connection:Connection|null};
export class NativeAccountProviderUnavailable extends Error {
  constructor(){super("계정 연결을 확인하지 못했어요.");this.name="NativeAccountProviderUnavailable";}
}
const fail=()=>new NativeAccountProviderUnavailable();
export function nativeAccountProviderConfigured(){
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
    maximum_transition_ms:5000,creation:"explicit_synthetic_context_only_no_mount_login_consent_or_read",
    replacement:"mask_retire_original_then_strict_native_close_receipt_before_distinct_driver_creation",
    context:"private_JS_generation_negative_guard_not_OS_member_identity_attestation",reentry:"reject_while_connecting_no_queue_or_retry",
    failure:"terminal_provider_discard_late_controller_preserve_credentials_and_intent",
    UI_detach:"StrictMode_detach_only_external_account_owner_disposes_provider",questions:"routine_state_and_safety_2_plus_conditional_1",
    registration:"OFF_review_provider_UI_not_default_app_or_native_plugin"};
  return Object.keys(policy).sort().join("|")===Object.keys(expected).sort().join("|")&&
    Object.entries(expected).every(([k,v])=>policy[k as keyof typeof policy]===v);
}
export function captureNativeAccountReviewContext(value:NativeAccountReviewContext):NativeAccountReviewContext{
  const options=value?.options,driver=value?.driver;
  if(!nativeAccountProviderConfigured()||!value||Object.keys(value).sort().join("|")!=="driver|fetcher|options"||typeof value.fetcher!=="function"
    ||options?.deploymentContext!=="synthetic_test"||typeof options.isCurrent!=="function"||typeof options.isNativeIOS!=="function"
    ||options.isCurrent()!==true||options.isNativeIOS()!==true||!Array.isArray(options.allowedBaseUrls)
    ||["openOriginalChannel","activateOriginalOnce","invokeChannel","observeChannel","disposeChannel","closeHost"]
      .some(k=>typeof driver?.[k as keyof typeof driver]!=="function"))throw fail();
  // Capture callback and base allowlist choices once. Vault/driver are trusted
  // injected synthetic ports, not authenticated OS capabilities.
  return {fetcher:value.fetcher,driver,options:{...options,allowedBaseUrls:[...options.allowedBaseUrls]}};
}

/** An unregistered, explicitly created account owner above React. No factory,
 * snapshot or UI mount authenticates a member, consumes consent or reads data.
 * Replacement requires the old private channel's close ACK, which still does
 * not attest OS socket/key cleanup or undo remote commits. */
export function createNativeAccountProviderLocal(deploymentContext:"synthetic_test"){
  if(deploymentContext!=="synthetic_test"||!nativeAccountProviderConfigured())throw fail();
  let frame:NativeAccountProviderFrame=Object.freeze({state:"empty",connection:null}),epoch=0,busy=false;
  const closure=createNativeAccountClosureProjectionLocal();
  let source:NativeAccountReviewContext|null=null,active:AbortController|null=null,cleanupFailed=false;
  const listeners=new Set<()=>void>(),drivers=new WeakSet<object>(),connections=new Set<Connection>();
  const startedSources=new Set<NativeAccountReviewContext>(),pending=new Set<Promise<unknown>>(),cleanups=new Set<Promise<unknown>>();
  const nativeClosures=new WeakMap<NativeAccountReviewContext,Promise<void>>();
  const retired=()=>frame.state==="retired";
  const track=<T,>(set:Set<Promise<unknown>>,p:Promise<T>)=>{set.add(p);void p.then(()=>set.delete(p),()=>set.delete(p));return p;};
  const notify=()=>{
    for(const listener of [...listeners])try{listener();}catch{/* A failed UI listener cannot block another sibling. */}
  };
  const publish=(state:NativeAccountProviderFrame["state"],connection:Connection|null=null)=>{frame=Object.freeze({state,connection});notify();};
  const closeNative=(s:NativeAccountReviewContext)=>{
    let result=nativeClosures.get(s);
    if(!result){result=track(cleanups,Promise.resolve().then(()=>s.driver.closeHost()).catch(()=>{cleanupFailed=true;throw fail();}));nativeClosures.set(s,result);}
    return result;
  };
  const cleanup=(c:Connection|null,s:NativeAccountReviewContext)=>track(cleanups,Promise.all([
    c?.dispose(),closeNative(s),
  ]).then(()=>{}).catch(()=>{cleanupFailed=true;throw fail();}));
  const invalidate=()=>{
    if(retired())return;epoch++;frame=Object.freeze({state:"retired",connection:null});
    closure.retire();
    // Latch retirement before abort/child callbacks can reenter this provider.
    active?.abort(fail());for(const c of connections)c.invalidate();notify();
    for(const s of startedSources)void cleanup(null,s).catch(()=>{});
    for(const c of connections)void track(cleanups,c.dispose()).catch(()=>{});
  };
  const valid=(own:number,s:NativeAccountReviewContext)=>{
    // A stale context must never invalidate a new account provider generation.
    if(own!==epoch||retired())return false;
    try{if(!nativeAccountProviderConfigured()||s.options.isCurrent()!==true||s.options.isNativeIOS()!==true)throw fail();return own===epoch&&!retired();}
    catch{invalidate();return false;}
  };
  const requireCurrent=(own:number,s:NativeAccountReviewContext)=>{if(!valid(own,s))throw fail();};
  return {
    // Stable, side-effect-free snapshots satisfy useSyncExternalStore. A private
    // connection reference exposes APIs, never a token or history payload DTO.
    snapshot:()=>frame,
    accountClosureSnapshot:closure.snapshot,
    subscribeAccountClosure:closure.subscribe,
    subscribe(listener:()=>void){listeners.add(listener);return()=>{listeners.delete(listener);};},
    async replaceSyntheticContext(value:NativeAccountReviewContext,signal?:AbortSignal):Promise<void>{
      if(retired()||busy)throw fail();signal?.throwIfAborted();const next=captureNativeAccountReviewContext(value);
      // Trusted port callbacks may reenter during validation. They cannot revive
      // a retired provider or bypass an in-flight replacement.
      if(retired()||busy)throw fail();signal?.throwIfAborted();
      if(drivers.has(next.driver))throw fail();
      const prior=frame.connection,oldSource=source,own=++epoch,controller=new AbortController();busy=true;active=controller;source=next;
      const abort=()=>invalidate();signal?.addEventListener("abort",abort,{once:true});
      closure.reset();prior?.invalidate();publish("connecting");
      try{
        await awaitSearchRequest(()=>track(pending,(async()=>{
          requireCurrent(own,next);controller.signal.throwIfAborted();
          if(oldSource){
            // The controller's dispose is deliberately best effort. This extra
            // strict channel ACK holds replacement on unknown/failed disposal.
            await cleanup(prior,oldSource);connections.delete(prior!);startedSources.delete(oldSource);
          }
          requireCurrent(own,next);controller.signal.throwIfAborted();drivers.add(next.driver);startedSources.add(next);
          const candidate=await createNativeRecoveryMemberWorkspaceLocal(next.fetcher,next.driver,
            {...next.options,isCurrent:()=>valid(own,next),setupSignal:controller.signal,onAccountClosed:receipt=>{
              // An obsolete accepted receipt cannot retire a successor provider.
              if(own!==epoch||retired())return;
              invalidate();try{next.options.onAccountClosed?.(receipt);}catch{/* Retirement cannot be undone. */}
            }});
          connections.add(candidate);
          closure.follow(candidate);
          try{
            requireCurrent(own,next);controller.signal.throwIfAborted();publish("ready",candidate);
            requireCurrent(own,next);controller.signal.throwIfAborted();
          }catch{candidate.invalidate();await cleanup(candidate,next).catch(()=>{});throw fail();}
        })()),async()=>{invalidate();},controller.signal,{milliseconds:policy.maximum_transition_ms,error:fail()});
      }catch{invalidate();throw fail();}
      finally{signal?.removeEventListener("abort",abort);if(active===controller)active=null;busy=false;}
    },
    invalidate,
    async dispose(){
      invalidate();
      // Release the caller on an unknown cleanup ACK, preserving pending work
      // tracking. This is not proof that the OS/remote worker has stopped.
      try{await awaitSearchRequest(async()=>{
        await Promise.allSettled([...pending,...cleanups]);
        if(cleanupFailed)throw fail();
      },async()=>{},undefined,{milliseconds:policy.maximum_transition_ms,error:fail()});}catch{throw fail();}
    },
  };
}
