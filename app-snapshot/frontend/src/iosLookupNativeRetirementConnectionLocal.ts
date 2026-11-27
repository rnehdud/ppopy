import policy from "../../skin_engine/config/app_lookup_native_retirement_wire_local.json";
import {createReviewIOSLookupRestartConnection} from "./iosLookupRestartConnectionLocal";
import {IOSLookupRestartUnavailable,type IOSLookupRestartBridge} from "./iosLookupRestartPortsLocal";
import {awaitSearchRequest} from "./searchRequestLifetime";

// Native-origin observation. No JS method can admit/revive an owner or assert
// credential, key or protected-data state. remove detaches only this observer.
export type IOSLookupNativeRetirementBridge=IOSLookupRestartBridge&{
  observeOwnerRetirement:(listener:(event:unknown)=>void)=>Promise<unknown>;
  disposeOriginalOwner:()=>Promise<void>;
};
type Options=Parameters<typeof createReviewIOSLookupRestartConnection>[2]&{setupSignal?:AbortSignal};
type Observation={version:"1.0.0";owner_id:string;remove:()=>Promise<void>};
const fail=()=>new IOSLookupRestartUnavailable();
const uuid=(v:unknown):v is string=>typeof v==="string"&&/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(v);
function guard(){
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,
    native_plugin_registered:false,observer_registration_enabled:false,
    admission:"explicit_original_native_owner_subscription_before_view",
    retirement:"terminal_native_and_JS_owner_abort_local_transport",
    event:"version_owner_id_retired_only_no_personal_payload",foreground:"no_reactivation_or_automatic_http",
    storage:"preserve_original_record_no_key_vault_slot_writes",registration_failure:"retire_no_fallback_or_retry",
    transport:"abort_signal_no_server_cancel_or_zero_work_claim"};
  if(Object.keys(policy).sort().join("|")!==Object.keys(expected).sort().join("|")
    ||Object.entries(expected).some(([k,v])=>policy[k as keyof typeof policy]!==v))throw fail();
}
function observation(value:unknown):Observation{
  if(!value||typeof value!=="object"||Array.isArray(value))throw fail();const v=value as Record<string,unknown>;
  if(Object.keys(v).sort().join("|")!=="owner_id|remove|version"||v.version!=="1.0.0"||!uuid(v.owner_id)||typeof v.remove!=="function")throw fail();
  return v as Observation;
}

/** Unregistered synthetic-only composition: native retirement cancels the same
 * original JS owner, including in-flight HTTP and detached views. A native event
 * cannot be a positive admission. IPC delivery is not an OS lifecycle guarantee. */
export async function createReviewIOSLookupNativeRetirementConnection(fetcher:typeof fetch,bridge:IOSLookupNativeRetirementBridge,options:Options){
  guard();if(options.deploymentContext!=="synthetic_test"||options.isNativeIOS?.()!==true||options.isCurrent?.()!==true
    ||typeof bridge?.observeOwnerRetirement!=="function"||typeof bridge?.disposeOriginalOwner!=="function")throw fail();
  options.setupSignal?.throwIfAborted();
  const admission=new AbortController();
  const setupAborted=()=>admission.abort(options.setupSignal?.reason);
  let retired=false,ownerID:string|null=null,receipt:Observation|null=null;
  let cleanup:Promise<void>|null=null,removal:Promise<void>|null=null;
  const remove=()=>{
    if(!receipt)return Promise.resolve();
    removal??=Promise.resolve().then(()=>receipt!.remove()).catch(()=>{throw fail();});
    void removal.catch(()=>{});return removal;
  };
  const retire=()=>{
    if(retired)return;retired=true;
    // dispose() invalidates listeners and aborts transport synchronously before
    // its Promise settles. Native cleanup ACK may fail; never reopen on failure.
    const local=connection.dispose();
    admission.abort(fail());
    cleanup=Promise.all([local,Promise.resolve().then(()=>bridge.disposeOriginalOwner())]).then(()=>{}).catch(()=>{throw fail();});
    void cleanup.catch(()=>{});void remove().catch(()=>{});
  };
  const connection=createReviewIOSLookupRestartConnection(fetcher,bridge,{...options,
    isCurrent:()=>!retired&&options.isCurrent(),onSessionChanged:()=>{retire();options.onSessionChanged?.();}});
  options.setupSignal?.addEventListener("abort",setupAborted,{once:true});
  const listener=(event:unknown)=>{
    if(retired)return;
    // Malformed, misrouted or early events all fail closed. The exact event is
    // intentionally terminal; it contains no reason, key, member or record.
    try{
      if(!event||typeof event!=="object"||Array.isArray(event))throw fail();const e=event as Record<string,unknown>;
      if(Object.keys(e).sort().join("|")!=="owner_id|state|version"||e.version!=="1.0.0"||e.state!=="retired"||!uuid(e.owner_id)
        ||ownerID===null||e.owner_id!==ownerID)throw fail();
    }catch{/* Channel integrity failure also retires this owner. */}
    retire();
  };
  const registration=Promise.resolve().then(()=>bridge.observeOwnerRetirement(listener)).then(value=>{
    // Save a callable remover even when receipt metadata is invalid. A malformed
    // channel is not permission to leak a listener or use a fallback connection.
    if(value&&typeof value==="object"&&!Array.isArray(value)&&typeof (value as Record<string,unknown>).remove==="function"){
      const raw=value as Observation;receipt={version:"1.0.0",owner_id:"",remove:()=>raw.remove()};
    }
    let admitted:Observation;try{admitted=observation(value);}catch{retire();void remove().catch(()=>{});throw fail();}
    receipt=admitted;ownerID=admitted.owner_id;
    if(retired){void remove().catch(()=>{});throw fail();}
    return admitted;
  });
  try{
    await awaitSearchRequest(()=>registration,async()=>{retire();},admission.signal);
    guard();if(retired||options.isCurrent()!==true||options.isNativeIOS()!==true)throw fail();
  }catch{retire();throw fail();}
  finally{options.setupSignal?.removeEventListener("abort",setupAborted);}
  const rejectBrowser:typeof connection.bindBrowserLifecycle=async()=>{throw fail();};
  return {...connection,
    // A JS background notification may precede the native channel delivery.
    // Close conservatively rather than retain a client with a retired native lease.
    async toBackground(){retire();},
    bindIOSLifecycle(lifecycleBridge:Parameters<typeof connection.bindIOSLifecycle>[0]){
      return connection.bindIOSLifecycle({addListener(event,notify){
        return lifecycleBridge.addListener(event,state=>{if(state.isActive!==true)retire();notify(state);});
      }});
    },
    // This owner is native-iOS-only. The separate existing browser composition
    // remains available; it cannot be used to revive this native owner.
    bindBrowserLifecycle:rejectBrowser,
    async dispose(){retire();await Promise.all([cleanup,remove()]);},
  };
}
