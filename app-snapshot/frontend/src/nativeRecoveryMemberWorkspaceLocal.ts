import policy from "../../skin_engine/config/app_native_recovery_ui_local.json";
import {createNativeMemberWorkspaceLocal} from "./nativeMemberWorkspaceLocal";
import type {IOSLookupNativeRetirementBridge} from "./iosLookupNativeRetirementConnectionLocal";
import {IOSLookupRestartUnavailable} from "./iosLookupRestartPortsLocal";
import {awaitSearchRequest} from "./searchRequestLifetime";
import {confirmedAccountWithdrawal} from "./appAccountWithdrawal";

export type NativeAccountClosureSnapshot=Readonly<{state:"none"}|{
  state:"accepted";history_deletion_scheduled:boolean;local_cleanup:"pending"|"cleared"|"required"|"session_changed";
}>;

export type NativeRecoveryChannelDriver={
  openOriginalChannel:()=>Promise<unknown>;
  activateOriginalOnce:()=>Promise<unknown>;
  invokeChannel:(ownerID:string,method:string,argumentsJSON:string)=>Promise<unknown>;
  observeChannel:(ownerID:string,listener:(event:unknown)=>void)=>Promise<unknown>;
  disposeChannel:(ownerID:string)=>Promise<void>;
  closeHost:()=>Promise<void>;
};
type Workspace=Awaited<ReturnType<typeof createNativeMemberWorkspaceLocal>>;
type Options=Parameters<typeof createNativeMemberWorkspaceLocal>[2];
const fail=()=>new IOSLookupRestartUnavailable();
export function nativeRecoveryUIConfigured(){
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
    maximum_activation_ms:5000,activation:"explicit_once_dispose_original_native_recovery_then_distinct_observed_member_workspace",
    mount:"channel_registration_only_no_vault_checkpoint_member_HTTP",
    late:"close_host_discard_lease_workspace_on_abort_timeout_member_replacement_unmount",
    failure:"terminal_disabled_retry_preserve_original_intent_no_new_search",questions:"routine_state_and_safety_2_plus_conditional_1",
    registration:"OFF_review_UI_not_default_shell_or_native_app"};
  return Object.keys(policy).sort().join("|")===Object.keys(expected).sort().join("|")&&
    Object.entries(expected).every(([k,v])=>policy[k as keyof typeof policy]===v);
}
function lease(value:unknown):string{
  if(!value||typeof value!=="object"||Array.isArray(value))throw fail();const v=value as Record<string,unknown>;
  if(Object.keys(v).sort().join("|")!=="owner_id|version"||v.version!=="1.0.0"||typeof v.owner_id!=="string"
    ||!/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(v.owner_id))throw fail();
  return v.owner_id;
}

/** OFF synthetic composition. The driver must be the private native channel,
 * not a caller-created replacement workspace. JS validates lease DTOs; only
 * native recovery authenticates the exact reservation. Neither proves OS auth. */
export async function createNativeRecoveryMemberWorkspaceLocal(fetcher:typeof fetch,driver:NativeRecoveryChannelDriver,options:Options){
  if(!nativeRecoveryUIConfigured()||options.deploymentContext!=="synthetic_test"||options.isNativeIOS?.()!==true||options.isCurrent?.()!==true
    ||typeof fetcher!=="function"||["openOriginalChannel","activateOriginalOnce","invokeChannel","observeChannel","disposeChannel","closeHost"]
      .some(k=>typeof driver?.[k as keyof NativeRecoveryChannelDriver]!=="function"))throw fail();
  let closed=false,used=false,original:Workspace|null=null,fresh:Workspace|null=null,cleanup:Promise<void>|null=null;
  let closure:NativeAccountClosureSnapshot=Object.freeze({state:"none"});
  const closureListeners=new Set<()=>void>();
  const publishClosure=(value:NativeAccountClosureSnapshot)=>{
    closure=Object.freeze(value);
    for(const listener of [...closureListeners])try{listener();}catch{/* One detached view cannot block terminal retirement. */}
  };
  const close=()=>{
    if(closed)return;closed=true;original?.invalidate();fresh?.invalidate();
    cleanup=Promise.allSettled([Promise.resolve().then(()=>driver.closeHost()),original?.dispose(),fresh?.dispose()]).then(()=>{});
  };
  const gate=()=>{
    if(closed||!nativeRecoveryUIConfigured()||options.isCurrent()!==true||options.isNativeIOS()!==true){close();throw fail();}
  };
  const create=async(id:string,signal?:AbortSignal)=>{
    let alive=true;const check=()=>{gate();if(!alive)throw fail();};
    const invoke=(method:string,args:unknown)=>Promise.resolve().then(()=>{check();return driver.invokeChannel(id,method,JSON.stringify(args));})
      .then(v=>{check();return v;});
    const bridge:IOSLookupNativeRetirementBridge={
      readOriginalSlot:a=>invoke("readOriginalSlot",a),compareOriginalSlot:a=>invoke("compareOriginalSlot",a),
      signOriginalRecord:a=>invoke("signOriginalRecord",a),verifyOriginalRecord:a=>invoke("verifyOriginalRecord",a),
      async observeOwnerRetirement(listener){
        check();const value=await driver.observeChannel(id,event=>{alive=false;listener(event);});
        if(!value||typeof value!=="object"||Array.isArray(value))throw fail();const v=value as Record<string,unknown>;
        // Preserve a remover for malformed/late registration, but reject it.
        if(Object.keys(v).sort().join("|")!=="owner_id|remove|version"||typeof v.remove!=="function"||v.owner_id!==id||v.version!=="1.0.0"){
          if(typeof v.remove==="function")void Promise.resolve().then(()=>(v.remove as ()=>Promise<void>)()).catch(()=>{});
          throw fail();
        }
        return value;
      },
      async disposeOriginalOwner(){alive=false;await driver.disposeChannel(id);},
    };
    return createNativeMemberWorkspaceLocal(fetcher,bridge,{...options,setupSignal:signal,onAccountClosed:receipt=>{
      // Accepted withdrawal is terminal for original and recovered workspaces.
      // Closing only the child would otherwise leave native recovery actionable.
      // Publish only these safe fields before the parent drops its connection.
      // A late cleanup result changes metadata, never a member/native capability.
      publishClosure({state:"accepted",history_deletion_scheduled:receipt.history_deletion_scheduled,local_cleanup:"pending"});
      close();try{options.onAccountClosed?.(receipt);}catch{/* Known acceptance stays terminal. */}
    },onAccountClosureSettled:result=>{
      if(closure.state!=="accepted"||closure.local_cleanup!=="pending"||!confirmedAccountWithdrawal(result))return;
      publishClosure({...closure,local_cleanup:result.state==="account_closed"?"cleared":
        result.state==="account_closed_session_changed"?"session_changed":"required"});
      try{options.onAccountClosureSettled?.(result);}catch{/* Metadata cannot reopen an account. */}
    },isCurrent:()=>{
      try{check();return true;}catch{return false;}
    }});
  };
  let originalID:string;
  try{originalID=lease(await driver.openOriginalChannel());gate();original=await create(originalID);gate();}
  catch{close();await cleanup;throw fail();}
  const workspace=original;
  return {workspace,
    // Pure terminal projection remains observable after disposal while CAS is
    // pending. It carries no token, account, history payload or native lease.
    accountClosureSnapshot:()=>closure,
    subscribeAccountClosure(listener:()=>void){closureListeners.add(listener);return()=>{closureListeners.delete(listener);};},
    async recoverOriginalWorkspace(signal:AbortSignal):Promise<Workspace>{
      gate();signal.throwIfAborted();
      // Repeated presses never interfere with an admitted replacement or the
      // first in-flight request. A healthy original cannot be retired by this API.
      if(used||workspace.isCurrent())throw fail();used=true;
      const aborted=()=>close();signal.addEventListener("abort",aborted,{once:true});
      try{
        return await awaitSearchRequest(async()=>{
          workspace.invalidate();await workspace.dispose();gate();signal.throwIfAborted();
          const id=lease(await driver.activateOriginalOnce());gate();signal.throwIfAborted();if(id===originalID)throw fail();
          const candidate=await create(id,signal);fresh=candidate;
          try{gate();signal.throwIfAborted();if(!candidate.isCurrent())throw fail();return candidate;}
          catch{candidate.invalidate();await candidate.dispose().catch(()=>{});throw fail();}
        },async()=>{close();},signal,{milliseconds:policy.maximum_activation_ms,error:fail()});
      }catch{close();throw fail();}
      finally{signal.removeEventListener("abort",aborted);}
    },
    invalidate:close,
    async dispose(){close();await cleanup;},
  };
}
