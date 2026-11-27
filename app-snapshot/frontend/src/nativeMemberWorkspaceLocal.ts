import policy from "../../skin_engine/config/app_native_member_workspace_local.json";
import consentPolicy from "../../skin_engine/config/app_history_consent.json";
import withdrawalPolicy from "../../skin_engine/config/app_account_withdrawal.json";
import {createHttpMirayQuotaStatusStore} from "./mirayQuotaStatus";
import {createHttpMiraySubscriptionStatusStore} from "./miraySubscriptionStatus";
import {createHttpAccountWithdrawalClient,parseAccountWithdrawalAcceptance,requestAppAccountWithdrawal,confirmedAccountWithdrawal,
  type AccountWithdrawalAcceptance,type AccountWithdrawalResult} from "./appAccountWithdrawal";
import {APP_SESSION_VAULT_VERSION,type AppSessionCredential} from "./appSessionVault";
import {createBoundMemberResponseSessionLoader,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {checkedReviewLookupRestartRecord} from "./appLookupResumeLocal";
import {checkedReviewLookupBase} from "./appLookupRequestLocal";
import {createHttpAppHistoryConsentStore} from "./appHistoryConsent";
import {createConsentJourneyReviewConnection,type ConsentJourneyReviewConnection} from "./mirayClosedLoopConsentJourneyReview";
import {createClosedLoopJourneyHttpReviewStore} from "./mirayClosedLoopJourneyReview";
import {createReviewIOSLookupNativeRetirementConnection,type IOSLookupNativeRetirementBridge} from "./iosLookupNativeRetirementConnectionLocal";
import {awaitSearchRequest} from "./searchRequestLifetime";
import {memberStatusReadScope} from "./memberStatusReadScope";

type Lookup=Awaited<ReturnType<typeof createReviewIOSLookupNativeRetirementConnection>>;
type Options=Parameters<typeof createReviewIOSLookupNativeRetirementConnection>[2]&{
  loopbackBaseUrl:string;onAccountClosed?:(acceptance:AccountWithdrawalAcceptance)=>void;
  onAccountClosureSettled?:(result:AccountWithdrawalResult)=>void;
};
const unavailable=()=>new AppMemberResponseSessionChanged();
function guard(){
  const expected={version:"1.0.2",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
    operational_api_enabled:false,automatic_dispatch:false,automatic_retry:false,question_profile:"routine_state_and_safety",
    core_question_count:2,conditional_discomfort_detail_count:1,maximum_response_bytes:262144,
    member:"shared_original_bearer_and_expiry_no_extension",retirement:"close_native_lookup_consent_journeys_account_abort_all_local_transports",
    account:"read_only_quota_subscription_explicit_withdrawal_receipt_retire_before_original_credential_CAS",
    response:"bounded_complete_body_current_401_retire_except_unconfirmed_withdrawal_no_cache",consent:"optional_history_explicit_server_status_never_native_proxy",
    navigation:"no_actual_use_or_automatic_save",abort:"unknown_server_commit_no_retry_or_zero_work_claim"};
  if(Object.keys(policy).sort().join("|")!==Object.keys(expected).sort().join("|")
    ||Object.entries(expected).some(([k,v])=>policy[k as keyof typeof policy]!==v))throw unavailable();
}

/** Synthetic-only explicit composition, never imported by the default shell.
 * Native channel retirement closes lookup, consent/loop and account siblings. Local
 * callbacks do not attest membership, consent, OS key state or server settlement. */
export async function createNativeMemberWorkspaceLocal(fetcher:typeof fetch,bridge:IOSLookupNativeRetirementBridge,options:Options){
  guard();if(options.deploymentContext!=="synthetic_test"||typeof fetcher!=="function"||options.isNativeIOS?.()!==true||options.isCurrent?.()!==true)throw unavailable();
  const base=checkedReviewLookupBase(options.baseUrl),loop=new URL(options.loopbackBaseUrl);
  if(loop.protocol!=="http:"||loop.hostname!=="127.0.0.1"||!loop.port||loop.pathname!=="/"||loop.username||loop.password||loop.search||loop.hash)throw unavailable();
  const origins=[base,loop.origin];let current=true,notified=false,expiry:string|null=null,lastTime:number|null=null;
  let lookup:Lookup|null=null,journey:ConsentJourneyReviewConnection|null=null,cleanup:Promise<void>|null=null;
  let quota:ReturnType<typeof createHttpMirayQuotaStatusStore>,subscription:ReturnType<typeof createHttpMiraySubscriptionStatusStore>;
  let withdrawalClient:ReturnType<typeof createHttpAccountWithdrawalClient>;
  let unbindLookup=()=>{},unbindJourney=()=>{};
  type Category="lookup"|"consent"|"loop";
  const lifetime=new AbortController(),active=new Map<AbortController,Category>(),pending=new Set<Promise<unknown>>(),listeners=new Set<()=>void>();
  let loopEpoch=0,withdrawalInFlight=false;const childListeners=new Set<()=>void>();
  const abortCategory=(category:Category)=>{for(const [c,kind] of active)if(kind===category){c.abort(unavailable());active.delete(c);}};
  const closeLoop=()=>{loopEpoch++;abortCategory("loop");for(const unbind of childListeners)unbind();childListeners.clear();};
  const retire=()=>{
    if(!current)return;current=false;expiry=null;lastTime=null;lifetime.abort(unavailable());
    active.forEach((_category,c)=>c.abort(unavailable()));active.clear();closeLoop();
    journey?.invalidate();if(lookup){cleanup=lookup.dispose();void cleanup.catch(()=>{});}
    unbindLookup();unbindJourney();
    for(const notify of [...listeners])try{notify();}catch{/* Other siblings must still close. */}listeners.clear();
  };
  const changed=()=>{retire();if(notified)return;notified=true;try{options.onSessionChanged?.();}catch{/* Never reopen. */}};
  const gate=()=>{
    try{guard();if(!current||options.isCurrent()!==true||options.isNativeIOS()!==true)throw unavailable();}
    catch{retire();throw unavailable();}
  };
  const loadCredential=async(isConsumerCurrent:()=>boolean=()=>true):Promise<AppSessionCredential>=>{
    const consumerGate=()=>{let live=false;try{live=isConsumerCurrent();}catch{/* Uncertain consumer stays closed. */}if(!live)throw unavailable();};
    consumerGate();gate();let c:AppSessionCredential|null;
    try{c=await awaitSearchRequest(()=>track(Promise.resolve().then(()=>{consumerGate();gate();return options.vault.load();})),async()=>{},lifetime.signal);consumerGate();gate();const now=options.now();
      if(!c||Object.keys(c).sort().join("|")!=="contract_version|expires_at|session_token"||c.contract_version!==APP_SESSION_VAULT_VERSION
        ||typeof c.session_token!=="string"||!/^[A-Za-z0-9_-]{32,200}$/.test(c.session_token)||!Number.isFinite(now)
        ||lastTime!==null&&now<lastTime||Date.parse(c.expires_at)<=now||expiry!==null&&expiry!==c.expires_at)throw unavailable();
      checkedReviewLookupRestartRecord({version:"1.0.0",kind:"ready",request_id:null,expires_at:c.expires_at,key_ref:"synthetic:lookup-restart-hmac-v1",proof:"A".repeat(43)});
      consumerGate();gate();expiry??=c.expires_at;lastTime=now;return {...c};
    }catch{consumerGate();changed();throw unavailable();}
  };
  const credentialToken=Object.assign(async()=>(await loadCredential()).session_token,
    {within:(live:()=>boolean)=>async()=>(await loadCredential(live)).session_token});
  const loadToken=createBoundMemberResponseSessionLoader(credentialToken,changed,()=>current);
  const vaultLoad=async(live:()=>boolean)=>{const token=await loadToken.within(live)(),value=await loadCredential(live);gate();if(token!==value.session_token){changed();throw unavailable();}return value;};
  const vault={...options.vault,
    ...(options.vault.clearIfCurrent?{clearIfCurrent:(expectedToken:string)=>options.vault.clearIfCurrent!(expectedToken)}:{}),
    load:Object.assign(()=>vaultLoad(()=>true),{within:(live:()=>boolean)=>()=>vaultLoad(live)})};
  const track=<T,>(wire:Promise<T>)=>{pending.add(wire);void wire.then(()=>pending.delete(wire),()=>pending.delete(wire));return wire;};
  const transportFor=(isConsumerCurrent:()=>boolean):typeof fetch=>async(input,init)=>{
    const consumerLive=()=>{try{return isConsumerCurrent()===true;}catch{return false;}};
    const gateCall=()=>{if(!consumerLive())throw unavailable();gate();};
    gateCall();init?.signal?.throwIfAborted();
    if(typeof input!=="string"||!origins.some(origin=>input.startsWith(origin+"/")))throw unavailable();
    const category:Category=input.startsWith(loop.origin+"/")?"loop":input===base+consentPolicy.http.path?"consent":"lookup";
    const controller=new AbortController(),abort=()=>controller.abort(init?.signal?.reason);active.set(controller,category);
    init?.signal?.addEventListener("abort",abort,{once:true});let reader:ReadableStreamDefaultReader<Uint8Array>|undefined;
    try{
      const load=loadToken.within(()=>!controller.signal.aborted && consumerLive());
      const token=await awaitSearchRequest(load,async()=>{},controller.signal);gateCall();controller.signal.throwIfAborted();
      if(!token||new Headers(init?.headers).get("Authorization")!==`Bearer ${token}`)throw unavailable();
      const response=await awaitSearchRequest(()=>track(Promise.resolve().then(()=>{
        gateCall();controller.signal.throwIfAborted();return fetcher(input,{...init,signal:controller.signal});
      }).then(value=>{if(controller.signal.aborted&&value.body)void value.body.cancel().catch(()=>{});return value;})),async()=>{controller.abort();},controller.signal);
      reader=response.body?.getReader();
      gateCall();controller.signal.throwIfAborted();
      if(response.redirected||response.url&&response.url!==input)throw unavailable();
      const declared=response.headers.get("content-length");
      if(declared!==null&&(!/^\d+$/.test(declared)||Number(declared)>policy.maximum_response_bytes))throw unavailable();
      const release=(body:BodyInit|null)=>{
        // Only a complete, bounded response for the still-current consumer can
        // reject this original member. A late old 401 cannot retire a successor;
        // 403/transport failures do not prove that the account session ended.
        gateCall();controller.signal.throwIfAborted();
        // A rejected DELETE keeps the established withdrawal_unconfirmed
        // contract: no account-closure inference and original intent preserved.
        const withdrawal=input===base+withdrawalPolicy.http.path&&init?.method==="DELETE";
        if(response.status===401&&!withdrawal){changed();throw unavailable();}
        return new Response(body,{status:response.status,statusText:response.statusText,headers:response.headers});
      };
      if(!response.body){await load();return release(null);}
      const chunks:Uint8Array[]=[];let size=0;
      while(true){
        gateCall();controller.signal.throwIfAborted();
        const part=await awaitSearchRequest(()=>track(reader!.read()),async()=>{void reader!.cancel().catch(()=>{});},controller.signal);
        gateCall();controller.signal.throwIfAborted();if(part.done)break;
        size+=part.value.byteLength;if(size>policy.maximum_response_bytes)throw unavailable();chunks.push(part.value);
      }
      await load();gateCall();controller.signal.throwIfAborted();
      const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
      return release(bytes);
    }catch(error){if(reader)void reader.cancel().catch(()=>{});throw error;}
    finally{active.delete(controller);init?.signal?.removeEventListener("abort",abort);try{reader?.releaseLock();}catch{/* Late ignored stream operation is still tracked. */}}
  };
  const transport=Object.assign(transportFor(()=>true),{within:transportFor});
  try{
    // Concrete existing HTTP stores, sharing the exact loader and cancellation
    // transport. No factory can silently ignore the member/transport binding.
    const original=createConsentJourneyReviewConnection({deploymentContext:"synthetic_test",loadToken,onMemberChanged:changed,
      createConsent:member=>createHttpAppHistoryConsentStore(transport,{baseUrl:base,allowedBaseUrls:options.allowedBaseUrls,
        loadSessionToken:member.loadToken,onSessionChanged:member.onMemberChanged}),
      createJourney:member=>createClosedLoopJourneyHttpReviewStore({...member,baseUrl:loop.href,fetcher:transport})});
    journey={...original,
      consent:{
        read:async opts=>{memberStatusReadScope(loadToken,opts).gate();closeLoop();abortCategory("consent");return original.consent.read(opts);},
        choose:async(choice,expected,opts)=>{memberStatusReadScope(loadToken,opts).gate();closeLoop();abortCategory("consent");return original.consent.choose(choice,expected,opts);},
      },
      closeJourney(){closeLoop();original.closeJourney();},
      async openJourney(expected,signal){
        closeLoop();const own=loopEpoch,opened=await original.openJourney(expected,signal);gate();
        if(own!==loopEpoch){opened.invalidate();throw unavailable();}
        const unbind=opened.subscribeInvalidation(()=>{if(own===loopEpoch)closeLoop();});childListeners.add(unbind);return opened;
      },
    };
    unbindJourney=journey.subscribeInvalidation(retire);
    lookup=await createReviewIOSLookupNativeRetirementConnection(transport,bridge,{...options,vault,isCurrent:()=>current&&options.isCurrent(),onSessionChanged:changed});
    // View replacement/detach is not retirement of a whole account workspace.
    unbindLookup=lookup.subscribeInvalidation(event=>{if(event.lifecycle==="retired")retire();});gate();
    const memberOptions={baseUrl:base,allowedBaseUrls:options.allowedBaseUrls,loadSessionToken:loadToken,onSessionChanged:changed};
    // Partial construction must retire the already registered native owner.
    quota=createHttpMirayQuotaStatusStore(transport,memberOptions);
    subscription=createHttpMiraySubscriptionStatusStore(transport,memberOptions);
    withdrawalClient=createHttpAccountWithdrawalClient(transport,memberOptions);
  }catch{retire();if(lookup)await lookup.dispose().catch(()=>{});throw unavailable();}
  return {lookup,journey,quota,subscription,
    async withdrawAccount(){
      gate();if(withdrawalInFlight)throw unavailable();withdrawalInFlight=true;
      try{const result=await requestAppAccountWithdrawal(vault,async token=>{
        return parseAccountWithdrawalAcceptance(await withdrawalClient(token));
      },options.vault,receipt=>{
        // A complete server receipt ends every sibling before possibly delayed
        // local CAS cleanup. It proves scheduled deletion, never completed purge
        // or subscription cancellation. Unknown receipts must not close by guess.
        retire();
        // Only a complete accepted receipt ends the parent account owner.
        // Native retirement/background may still need explicit original recovery.
        // Notify before asynchronous credential CAS; listener failure cannot turn
        // known server acceptance into an unconfirmed response or reopen siblings.
        try{options.onAccountClosed?.(receipt);}catch{/* Other lifetime fences already closed. */}
      });
        if(confirmedAccountWithdrawal(result))try{options.onAccountClosureSettled?.(result);}catch{/* Acceptance stays terminal. */}
        return result;
      }finally{withdrawalInFlight=false;}
    },
    isCurrent(){try{gate();return true;}catch{return false;}},
    subscribeInvalidation(notify:()=>void){gate();listeners.add(notify);return()=>{listeners.delete(notify);};},
    invalidate:retire,
    async toBackground(){retire();},async toForeground(){/* Explicit new owner required; no auto calls. */},
    async settled(){await Promise.allSettled([...pending]);await lookup!.settled();},
    async dispose(){retire();await cleanup;},
  };
}
