import policy from "../../skin_engine/config/app_lookup_resume_local.json";
import wirePolicy from "../../skin_engine/config/app_lookup_request_local.json";
import {APP_SESSION_VAULT_VERSION,type SessionVault,type AppSessionCredential} from "./appSessionVault";
import {createBoundMemberResponseSessionLoader,assertCurrentMemberResponseSession,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {assertReviewLookupRequestPolicy,checkedReviewLookupBase,checkedReviewLookupQuery,readReviewLookupResponseJson,checkedLookupRequest,type LookupRequestConfirmation} from "./appLookupRequestLocal";
import {checkedLookupDelivery,checkedLookupMetadata,LookupStartUnconfirmed,type LookupDelivery,type LookupMetadata} from "./appLookupDeliveryLocal";
import {assertLookupConsumerCurrent,loadLookupCredentialWithin,type LookupConsumerScope} from "./lookupConsumerScopeLocal";

/** Trusted authoritative atomic secure-slot port. True means exact durable CAS
 * committed. Unattested rollback/restore is outside this port's guarantee.
 * No native adapter is supplied; ordinary get/set or read-then-write is insufficient. */
export type LookupRestartStore={read:()=>Promise<string|null>;compareAndSwap:(expected:string,next:string)=>Promise<boolean>;within?:(live:LookupConsumerScope)=>LookupRestartStore};
export type LookupRestartMac={sign:(message:Uint8Array)=>Promise<string>;verify:(message:Uint8Array,proof:string)=>Promise<boolean>;within?:(live:LookupConsumerScope)=>LookupRestartMac};
type RecordValue={version:"1.0.0";kind:"ready"|"intent"|"closed";request_id:string|null;expires_at:string;key_ref:string;proof:string};
type Options={deploymentContext:"synthetic_test";baseUrl:string;allowedBaseUrls:readonly string[];
  vault:SessionVault;store:LookupRestartStore;mac:LookupRestartMac;now:()=>number;isCurrent:()=>boolean;onSessionChanged?:()=>void};
type RequestOptions={signal?:AbortSignal};
type Phase="idle"|"starting"|"active"|"terminal"|"uncertain"|"recovering"|"retrying"|"retired";
export class LookupRestartUnconfirmed extends Error {
  constructor(){super("이전 검색 기록을 확인하지 못했어요. 새 검색을 자동으로 시작하지 않습니다.");this.name="LookupRestartUnconfirmed";}
}
const uuid=(x:unknown):x is string=>typeof x==="string"&&/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(x);
const proof=(x:unknown):x is string=>typeof x==="string"&&/^[A-Za-z0-9_-]{43}$/.test(x);
const utc=(x:unknown):x is string=>{
  if(typeof x!=="string"||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/.test(x)||!Number.isFinite(Date.parse(x)))return false;
  return new Date(x).toISOString()===x.replace(/(?:\.(\d{1,3}))?Z$/,(_all,fraction:string|undefined)=>"."+(fraction??"").padEnd(3,"0")+"Z");
};
const failed=()=>new LookupRestartUnconfirmed();
function guard(){
  assertReviewLookupRequestPolicy();
  if(policy.version!=="1.0.0"||policy.scope!=="isolated_local_review"||[
    policy.runtime_registered,policy.public_enabled,policy.native_connection_enabled,policy.operational_secure_store_authorized,
    policy.operational_mac_authorized,policy.automatic_poll_or_retry,
  ].some(v=>v!==false)||policy.record_namespace!=="original_session_lookup_restart_intent"||policy.key_ref!=="synthetic:lookup-restart-hmac-v1"
    ||policy.maximum_record_bytes!==1024||policy.retention!=="original_session_expiry_no_extension"
    ||policy.admission!=="verified_write_ahead_atomic_compare_and_swap"||policy.missing_or_invalid!=="hold_no_fresh_start_or_record_repair"
    ||policy.fresh_installation!=="separately_attested_signed_ready_record_required"||policy.retirement!=="preserve_record_clear_live_ids_no_vault_write"
    ||policy.recovery!=="explicit_original_session_only_no_query_cache")throw failed();
}
function checkedRecord(x:unknown):RecordValue{
  if(!x||typeof x!=="object"||Array.isArray(x))throw failed();const v=x as Record<string,unknown>;
  if(Object.keys(v).sort().join("|")!=="expires_at|key_ref|kind|proof|request_id|version"||v.version!=="1.0.0"
    ||!["ready","intent","closed"].includes(String(v.kind))||v.key_ref!==policy.key_ref||!proof(v.proof)
    ||!utc(v.expires_at)||(v.kind==="ready"?v.request_id!==null:!uuid(v.request_id)))throw failed();
  return {...v} as RecordValue;
}

// The unregistered native port shares the exact reviewed record validator.
export {checkedRecord as checkedReviewLookupRestartRecord,guard as assertReviewLookupRestartPolicy};

/** Disabled restart client. Signed ready provisioning and atomic Keychain/MAC
 * adapters remain separate unimplemented operational contracts. Missing is unknown. */
export function createReviewLookupRestartClient(fetcher:typeof fetch,options:Options){
  guard();if(options.deploymentContext!=="synthetic_test"||typeof fetcher!=="function"||typeof options.now!=="function"||typeof options.isCurrent!=="function"
    ||typeof options.vault?.load!=="function"||typeof options.store?.read!=="function"||typeof options.store?.compareAndSwap!=="function"
    ||typeof options.mac?.sign!=="function"||typeof options.mac?.verify!=="function")throw failed();
  const base=checkedReviewLookupBase(options.baseUrl);if(!options.allowedBaseUrls.map(checkedReviewLookupBase).includes(base))throw failed();
  let phase:Phase="uncertain",busy=false,handle:string|null=null,liveKey:string|null=null,notified=false,boundExpiry:string|null=null;
  const active=new Set<AbortController>();
  const retired=()=>phase==="retired";
  const retire=()=>{phase="retired";handle=null;liveKey=null;active.forEach(c=>c.abort(new AppMemberResponseSessionChanged()));active.clear();};
  const changed=()=>{retire();if(notified)return;notified=true;try{options.onSessionChanged?.();}catch{/* Terminal even if notification fails. */}};
  const credential=async(live:LookupConsumerScope):Promise<AppSessionCredential>=>{
    assertLookupConsumerCurrent(live);guard();if(retired())throw new AppMemberResponseSessionChanged();
    let c:AppSessionCredential|null;
    try{c=await loadLookupCredentialWithin(options.vault,live);}catch{assertLookupConsumerCurrent(live);changed();throw new AppMemberResponseSessionChanged();}
    assertLookupConsumerCurrent(live);if(retired()||!options.isCurrent()){changed();throw new AppMemberResponseSessionChanged();}
    const now=options.now();
    if(!c||Object.keys(c).sort().join("|")!=="contract_version|expires_at|session_token"||c.contract_version!==APP_SESSION_VAULT_VERSION
      ||typeof c.session_token!=="string"||!/^[A-Za-z0-9_-]{32,200}$/.test(c.session_token)||!Number.isFinite(now)||!utc(c.expires_at)||Date.parse(c.expires_at)<=now
      ||(boundExpiry!==null&&boundExpiry!==c.expires_at)){
      changed();throw new AppMemberResponseSessionChanged();
    }
    boundExpiry??=c.expires_at;
    return {...c};
  };
  const token=async(live:LookupConsumerScope)=>(await credential(live)).session_token;
  const load=createBoundMemberResponseSessionLoader(Object.assign(()=>token(()=>true),{within:(live:LookupConsumerScope)=>()=>token(live)}),changed,()=>!retired()&&options.isCurrent());
  const scope=(signal:AbortSignal)=>()=>!signal.aborted;
  const member=async(signal:AbortSignal)=>{const live=scope(signal),scoped=load.within(live),token=await scoped();if(!token){changed();throw new AppMemberResponseSessionChanged();}const c=await credential(live);await assertCurrentMemberResponseSession(scoped,token,changed);if(c.session_token!==token){changed();throw new AppMemberResponseSessionChanged();}return c;};
  const store=(signal:AbortSignal)=>options.store.within?.(scope(signal))??options.store;
  const mac=(signal:AbortSignal)=>options.mac.within?.(scope(signal))??options.mac;
  const message=(v:Omit<RecordValue,"proof">,c:AppSessionCredential)=>new TextEncoder().encode(JSON.stringify([
    policy.record_namespace,base,v.version,v.kind,v.request_id,v.expires_at,v.key_ref,c.session_token,
  ]));
  const read=async(signal:AbortSignal)=>{
    signal.throwIfAborted();const c=await member(signal),raw=await store(signal).read();signal.throwIfAborted();await member(signal);
    if(typeof raw!=="string"||new TextEncoder().encode(raw).length>policy.maximum_record_bytes)throw failed();
    const v=checkedRecord(await readReviewLookupResponseJson(new Response(raw,{headers:{"Content-Type":"application/json"}}),signal));
    if(v.expires_at!==c.expires_at||await mac(signal).verify(message(v,c),v.proof)!==true)throw failed();
    signal.throwIfAborted();await member(signal);return {raw,value:v};
  };
  const assertSlot=async(expected:string,signal:AbortSignal)=>{const v=await read(signal);if(v.raw!==expected)throw failed();return v;};
  const write=async(expected:string,kind:"intent"|"closed",key:string,signal:AbortSignal)=>{
    const prior=await assertSlot(expected,signal),c=await member(signal);
    if(kind==="intent"?!["ready","closed"].includes(prior.value.kind):prior.value.kind!=="intent"||prior.value.request_id!==key)throw failed();
    const value:Omit<RecordValue,"proof">={version:"1.0.0",kind,request_id:key,expires_at:c.expires_at,key_ref:policy.key_ref};
    const p=await mac(signal).sign(message(value,c));if(!proof(p)||await mac(signal).verify(message(value,c),p)!==true)throw failed();
    const raw=JSON.stringify({...value,proof:p});await assertSlot(expected,signal);await member(signal);signal.throwIfAborted();
    if(await store(signal).compareAndSwap(expected,raw)!==true)throw failed();
    // A write ACK alone does not permit HTTP; reread/MAC/current member must agree.
    return assertSlot(raw,signal);
  };
  const exclusive=async<T>(operation:(signal:AbortSignal)=>Promise<T>,opts?:RequestOptions):Promise<T>=>{
    guard();if(retired())throw new AppMemberResponseSessionChanged();if(busy)throw failed();opts?.signal?.throwIfAborted();
    busy=true;const controller=new AbortController(),abort=()=>controller.abort(opts?.signal?.reason);active.add(controller);opts?.signal?.addEventListener("abort",abort,{once:true});
    try{return await operation(controller.signal);}catch(e){
      if(!retired()){phase="uncertain";handle=null;liveKey=null;if(!controller.signal.aborted)await member(controller.signal);}
      if(e instanceof AppMemberResponseSessionChanged)throw e;controller.signal.throwIfAborted();throw failed();
    }finally{busy=false;active.delete(controller);opts?.signal?.removeEventListener("abort",abort);}
  };
  const request=async<T>(method:"POST"|"GET",path:string,body:string|undefined,raw:string,signal:AbortSignal,check:(v:unknown,status:number)=>T)=>{
    await assertSlot(raw,signal);const c=await member(signal);signal.throwIfAborted();
    const response=await fetcher(base+path,{method,signal,cache:"no-store",credentials:"omit",redirect:"error",
      headers:{Authorization:`Bearer ${c.session_token}`,...(body===undefined?{}:{"Content-Type":"application/json"})},...(body===undefined?{}:{body})});
    await assertSlot(raw,signal);await assertCurrentMemberResponseSession(load.within(scope(signal)),c.session_token,changed);signal.throwIfAborted();
    if(response.redirected||(response.url&&response.url!==base+path)||!response.ok)throw failed();
    const v=await readReviewLookupResponseJson(response,signal);await assertSlot(raw,signal);signal.throwIfAborted();return check(v,response.status);
  };
  const requests=wirePolicy.http.base_path+wirePolicy.http.request_suffix;
  const submit=(query:string,retry:boolean,opts?:RequestOptions)=>{
    if(retired())return Promise.reject(new AppMemberResponseSessionChanged());
    if(retry?phase!=="uncertain":!["idle","terminal","uncertain"].includes(phase))return Promise.reject(new LookupStartUnconfirmed());
    return exclusive(async signal=>{
    const normalized=checkedReviewLookupQuery(query),prior=await read(signal);
    if(retry?prior.value.kind!=="intent":!["ready","closed"].includes(prior.value.kind))throw new LookupStartUnconfirmed();
    const key=retry?prior.value.request_id!:crypto.randomUUID();if(!uuid(key))throw failed();
    const body=JSON.stringify({request_id:key,query:normalized});if(new TextEncoder().encode(body).length>wirePolicy.http.maximum_request_bytes)throw failed();
    const prepared=retry?prior:await write(prior.raw,"intent",key,signal);phase=retry?"retrying":"starting";
    const ack=await request("POST",requests,body,prepared.raw,signal,(v,status)=>{const a=checkedLookupRequest(v,key);if(!a.confirmed||status!==(a.start.allowed?202:200))throw failed();return a;});
    if(!ack.confirmed)throw failed();
    if(ack.start.allowed){handle=ack.start.lookup_id;liveKey=key;phase="active";}
    else{await write(prepared.raw,"closed",key,signal);handle=null;liveKey=null;phase="terminal";}
    return ack;
    },opts);
  };
  const result=async<T extends LookupMetadata>(method:"GET"|"POST",suffix:string,signal:AbortSignal,check:(v:unknown,h:string)=>T)=>{
    const prior=await read(signal),h=handle,k=liveKey;if(!h||!k||prior.value.kind!=="intent"||prior.value.request_id!==k)throw failed();
    const v=await request(method,wirePolicy.http.base_path+"/"+h+suffix,method==="POST"?"{}":undefined,prior.raw,signal,(x,status)=>{if(status!==200)throw failed();return check(x,h);});
    if(v.outcome_known){await write(prior.raw,"closed",k,signal);phase="terminal";handle=null;liveKey=null;}else phase="active";return v;
  };
  return {
    async inspectCheckpoint(opts?:RequestOptions){return exclusive(async signal=>{
      const v=await read(signal);handle=null;liveKey=null;phase=v.value.kind==="ready"?"idle":v.value.kind==="closed"?"terminal":"uncertain";return {phase};
    },opts);},
    begin:(query:string,opts?:RequestOptions)=>submit(query,false,opts),retryStart:(query:string,opts?:RequestOptions)=>submit(query,true,opts),
    recover:(opts?:RequestOptions):Promise<LookupRequestConfirmation>=>{
      if(retired())return Promise.reject(new AppMemberResponseSessionChanged());
      if(phase!=="uncertain")return Promise.reject(new LookupStartUnconfirmed());
      return exclusive(async signal=>{
      const prior=await read(signal);if(prior.value.kind!=="intent"||!prior.value.request_id)throw failed();const k=prior.value.request_id;phase="recovering";
      const ack=await request("GET",requests+"/"+k,undefined,prior.raw,signal,(x,status)=>{if(status!==200)throw failed();return checkedLookupRequest(x,k,true);});
      if(ack.confirmed){handle=ack.start.lookup_id;liveKey=k;phase="active";}else{handle=null;liveKey=null;phase="uncertain";}return ack;
      },opts);
    },
    read:(opts?:RequestOptions):Promise<LookupDelivery>=>exclusive(s=>result("GET","",s,checkedLookupDelivery),opts),
    cancel:(opts?:RequestOptions):Promise<LookupMetadata>=>exclusive(s=>result("POST","/cancel",s,checkedLookupMetadata),opts),
    state:()=>({phase}),dispose:retire,
  };
}
