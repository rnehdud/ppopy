import policy from "../../skin_engine/config/app_lookup_native_ports_local.json";
import recordPolicy from "../../skin_engine/config/app_lookup_resume_local.json";
import {APP_SESSION_VAULT_VERSION,type SessionVault,type AppSessionCredential} from "./appSessionVault";
import {createBoundMemberResponseSessionLoader,assertCurrentMemberResponseSession,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {checkedReviewLookupBase,readReviewLookupResponseJson} from "./appLookupRequestLocal";
import {checkedReviewLookupRestartRecord,assertReviewLookupRestartPolicy,type LookupRestartStore,type LookupRestartMac} from "./appLookupResumeLocal";
import {assertLookupConsumerCurrent,loadLookupCredentialWithin,type LookupConsumerScope} from "./lookupConsumerScopeLocal";

type Slot={namespace:string;key_ref:string};
/** Trusted native boundary to be implemented and reviewed separately. No plugin
 * registration is supplied. CAS must be authoritative/durable across callers;
 * ordinary Keychain get/set and this TypeScript wrapper do not establish that. */
export type IOSLookupRestartBridge={
  readOriginalSlot:(options:Slot)=>Promise<unknown>;
  compareOriginalSlot:(options:Slot&{expected:string;next:string})=>Promise<unknown>;
  signOriginalRecord:(options:Slot&{message_base64url:string})=>Promise<unknown>;
  verifyOriginalRecord:(options:Slot&{message_base64url:string;proof:string})=>Promise<unknown>;
};
type Options={deploymentContext:"synthetic_test";baseUrl:string;allowedBaseUrls:readonly string[];
  vault:SessionVault;isNativeIOS:()=>boolean;isCurrent:()=>boolean;now:()=>number};
export class IOSLookupRestartUnavailable extends Error{
  constructor(){super("이전 검색의 보안 저장소 연결을 확인하지 못했어요.");this.name="IOSLookupRestartUnavailable";}
}
const fail=()=>new IOSLookupRestartUnavailable();
const signature=(x:unknown):x is string=>typeof x==="string"&&/^[A-Za-z0-9_-]{43}$/.test(x);
const encoder=new TextEncoder();
const base64=(bytes:Uint8Array)=>btoa(String.fromCharCode(...bytes)).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
function guard(){
  assertReviewLookupRestartPolicy();
  if(policy.version!=="1.0.0"||policy.scope!=="isolated_local_review"||[
    policy.runtime_registered,policy.public_enabled,policy.native_plugin_registered,policy.operational_secure_store_authorized,
    policy.operational_mac_authorized,policy.ready_provisioning_enabled,policy.key_creation_rotation_deletion_enabled,
  ].some(v=>v!==false)||policy.namespace!==recordPolicy.record_namespace||policy.key_ref!==recordPolicy.key_ref
    ||policy.maximum_message_bytes!==1024||policy.record_contract!=="app_lookup_resume_local"
    ||policy.store_contract!=="authoritative_durable_exact_atomic_cas_no_unattested_restore"
    ||policy.admission!=="existing_authenticated_slot_only_no_null_bootstrap"||policy.mac_contract!=="canonical_original_session_and_exact_https_base"
    ||policy.session_retirement!=="clear_memory_only_no_native_remove"||policy.key_access!=="existing_device_only_unlocked_key_no_fallback")throw fail();
}

/** Disabled native-port adapter. It checks bridge DTOs and original member lifetime;
 * it cannot prove Keychain durability, native MAC provenance or anti-rollback. */
export function createReviewIOSLookupRestartPorts(bridge:IOSLookupRestartBridge,options:Options){
  guard();if(options.deploymentContext!=="synthetic_test"||typeof options.isNativeIOS!=="function"||typeof options.isCurrent!=="function"
    ||typeof options.now!=="function"||typeof options.vault?.load!=="function"||[
      bridge?.readOriginalSlot,bridge?.compareOriginalSlot,bridge?.signOriginalRecord,bridge?.verifyOriginalRecord,
    ].some(v=>typeof v!=="function"))throw fail();
  const base=checkedReviewLookupBase(options.baseUrl);if(!options.allowedBaseUrls.map(checkedReviewLookupBase).includes(base))throw fail();
  const slot:Slot={namespace:policy.namespace,key_ref:policy.key_ref};let retired=false,expiry:string|null=null;
  const retire=()=>{retired=true;expiry=null;};
  const live=()=>{guard();if(retired||options.isCurrent()!==true){retire();throw new AppMemberResponseSessionChanged();}if(options.isNativeIOS()!==true)throw fail();};
  const credential=async(consumer:LookupConsumerScope):Promise<AppSessionCredential>=>{
    assertLookupConsumerCurrent(consumer);live();let c:AppSessionCredential|null;try{c=await loadLookupCredentialWithin(options.vault,consumer);}catch{assertLookupConsumerCurrent(consumer);retire();throw new AppMemberResponseSessionChanged();}assertLookupConsumerCurrent(consumer);live();
    const now=options.now();
    if(!c||Object.keys(c).sort().join("|")!=="contract_version|expires_at|session_token"||c.contract_version!==APP_SESSION_VAULT_VERSION
      ||typeof c.session_token!=="string"||!/^[A-Za-z0-9_-]{32,200}$/.test(c.session_token)||!Number.isFinite(now)){retire();throw new AppMemberResponseSessionChanged();}
    try{checkedReviewLookupRestartRecord({version:"1.0.0",kind:"ready",request_id:null,expires_at:c.expires_at,key_ref:policy.key_ref,proof:"A".repeat(43)});}catch{retire();throw new AppMemberResponseSessionChanged();}
    if(Date.parse(c.expires_at)<=now||(expiry!==null&&expiry!==c.expires_at)){retire();throw new AppMemberResponseSessionChanged();}expiry??=c.expires_at;return {...c};
  };
  const token=async(consumer:LookupConsumerScope)=>(await credential(consumer)).session_token;
  const load=createBoundMemberResponseSessionLoader(Object.assign(()=>token(()=>true),{within:(consumer:LookupConsumerScope)=>()=>token(consumer)}),retire,()=>!retired&&options.isCurrent());
  const member=async(consumer:LookupConsumerScope)=>{const scoped=load.within(consumer),token=await scoped();if(!token){retire();throw new AppMemberResponseSessionChanged();}const c=await credential(consumer);await assertCurrentMemberResponseSession(scoped,token,retire);if(c.session_token!==token){retire();throw new AppMemberResponseSessionChanged();}return c;};
  const envelope=(x:unknown,field:"value"|"committed"|"proof"|"valid")=>{
    if(!x||typeof x!=="object"||Array.isArray(x))throw fail();const v=x as Record<string,unknown>;
    if(Object.keys(v).sort().join("|")!==["version","namespace","key_ref",field].sort().join("|")
      ||v.version!==policy.version||v.namespace!==slot.namespace||v.key_ref!==slot.key_ref)throw fail();return v;
  };
  const parseRecord=async(raw:string,c:AppSessionCredential)=>{
    if(typeof raw!=="string"||encoder.encode(raw).length>recordPolicy.maximum_record_bytes)throw fail();
    let v:ReturnType<typeof checkedReviewLookupRestartRecord>;
    try{v=checkedReviewLookupRestartRecord(await readReviewLookupResponseJson(new Response(raw,{headers:{"Content-Type":"application/json"}}),new AbortController().signal));}catch{throw fail();}
    if(v.expires_at!==c.expires_at)throw fail();return v;
  };
  const recordMessage=(v:ReturnType<typeof checkedReviewLookupRestartRecord>,c:AppSessionCredential)=>encoder.encode(JSON.stringify([
    slot.namespace,base,v.version,v.kind,v.request_id,v.expires_at,v.key_ref,c.session_token,
  ]));
  const checkedMessage=(bytes:Uint8Array,c:AppSessionCredential,signing:boolean)=>{
    // TextEncoder/bridge byte views can come from a different JS realm.
    if(!ArrayBuffer.isView(bytes)||Object.prototype.toString.call(bytes)!=="[object Uint8Array]"||bytes.byteLength>policy.maximum_message_bytes)throw fail();
    let text:string,v:unknown;try{text=new TextDecoder("utf-8",{fatal:true}).decode(bytes);v=JSON.parse(text);}catch{throw fail();}
    if(!Array.isArray(v)||v.length!==8||JSON.stringify(v)!==text||v[0]!==slot.namespace||v[1]!==base||v[7]!==c.session_token)throw fail();
    const record=checkedReviewLookupRestartRecord({version:v[2],kind:v[3],request_id:v[4],expires_at:v[5],key_ref:v[6],proof:"A".repeat(43)});
    if(record.expires_at!==c.expires_at||(signing&&record.kind==="ready"))throw fail();return base64(bytes);
  };
  const call=async(consumer:LookupConsumerScope,field:"value"|"committed"|"proof"|"valid",run:()=>Promise<unknown>)=>{
    await member(consumer);let response:unknown;try{response=await run();}catch{await member(consumer);throw fail();}
    await member(consumer);return envelope(response,field);
  };
  const verified=async(consumer:LookupConsumerScope,bytes:Uint8Array,p:string)=>{
    if(!signature(p))throw fail();const c=await member(consumer),message_base64url=checkedMessage(bytes,c,false);
    const response=await call(consumer,"valid",()=>bridge.verifyOriginalRecord({...slot,message_base64url,proof:p}));
    if(typeof response.valid!=="boolean")throw fail();return response.valid;
  };
  const scopedStore=(consumer:LookupConsumerScope):LookupRestartStore=>({
    within:nested=>scopedStore(()=>consumer()&&nested()),
    async read(){
      const response=await call(consumer,"value",()=>bridge.readOriginalSlot({...slot}));
      if(response.value===null)return null;const c=await member(consumer),v=await parseRecord(response.value as string,c);
      if(await verified(consumer,recordMessage(v,c),v.proof)!==true)throw fail();return response.value as string;
    },
    async compareAndSwap(expected,next){
      const c=await member(consumer),old=await parseRecord(expected,c),value=await parseRecord(next,c);
      if(value.kind==="intent"?!["ready","closed"].includes(old.kind):value.kind!=="closed"||old.kind!=="intent"||old.request_id!==value.request_id)throw fail();
      if(await verified(consumer,recordMessage(old,c),old.proof)!==true||await verified(consumer,recordMessage(value,c),value.proof)!==true)throw fail();
      const response=await call(consumer,"committed",()=>bridge.compareOriginalSlot({...slot,expected,next}));
      if(typeof response.committed!=="boolean")throw fail();return response.committed;
    },
  });
  const scopedMac=(consumer:LookupConsumerScope):LookupRestartMac=>({
    within:nested=>scopedMac(()=>consumer()&&nested()),
    async sign(bytes){const c=await member(consumer),message_base64url=checkedMessage(bytes,c,true);
      const response=await call(consumer,"proof",()=>bridge.signOriginalRecord({...slot,message_base64url}));if(!signature(response.proof))throw fail();return response.proof;},
    verify:(bytes,p)=>verified(consumer,bytes,p),
  });
  return {store:scopedStore(()=>true),mac:scopedMac(()=>true),dispose:retire};
}
