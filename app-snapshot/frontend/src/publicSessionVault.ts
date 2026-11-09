import policy from "../../skin_engine/config/app_public_session_vault_review.json";
import google from "../../skin_engine/config/app_public_google_owner_review.json";
import kakao from "../../skin_engine/config/app_public_kakao_owner_review.json";
import type {AppSessionCredential,SessionVault} from "./appSessionVault";

export interface PublicSessionStore {
  get(key:string):Promise<string|null>;
  /** Native implementation must serialize this comparison and write with all
   * other mutations of the exclusive public Keychain slot. */
  compareAndSwap(key:string,expectedValue:string|null,nextValue:string|null):Promise<boolean>;
}
export type PublicOwnerBinding={public_sha256:string;public_x963_b64:string};
export type PublicOwnerBindings={google:PublicOwnerBinding;kakao:PublicOwnerBinding};
export const PUBLIC_SESSION_KEY=policy.key;
const contracts=Object.freeze({plain:"1.0.0-public-session",google:"1.0.0-public-google-session",kakao:"1.0.0-public-kakao-session"} as const);
const unavailable=()=>new Error("공개 앱의 보안 로그인 정보를 확인하지 못했어요.");
const utf8=new TextEncoder(),bytes=(s:string)=>utf8.encode(s).byteLength;
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
function binary(value:unknown){
  if(typeof value!=="string"||!value||!/^[A-Za-z0-9+/]+={0,2}$/.test(value))throw unavailable();
  const raw=atob(value);if(btoa(raw)!==value)throw unavailable();return Uint8Array.from(raw,c=>c.charCodeAt(0));
}
const hex=(b:ArrayBuffer)=>Array.from(new Uint8Array(b),x=>x.toString(16).padStart(2,"0")).join("");
const queues=new WeakMap<PublicSessionStore,Promise<void>>();

/** Public codec only. It never reads, imports or repairs the TEST Keychain slot.
 * WebCrypto verifies the public signed owner commitment; native SDK identity
 * matching and actual Keychain storage guarantees are separate host duties. */
export async function createPublicSessionVault(store:PublicSessionStore,options:{ownerBindings:PublicOwnerBindings;crypto?:Crypto;now?:()=>number}):Promise<SessionVault>{
  try{
    if(policy.version!=="1.0.0-public-session-vault-review-20261021"||policy.scope!=="public_device_session_only_not_TEST_or_research"||
      policy.key!=="poppy.public.session.v1"||policy.keychain_service!=="com.miraylab.poppy.public-session-vault"||policy.TEST_migration!==false||
      (!exact(policy.contract_versions,["plain","google","kakao"])||Object.entries(contracts).some(([k,v])=>policy.contract_versions[k as keyof typeof contracts]!==v))||policy.maximum_vault_bytes!==4096||policy.maximum_session_days!==google.algorithm.maximum_session_days||
      policy.maximum_session_days!==kakao.algorithm.maximum_session_days||policy.maximum_clock_skew_milliseconds!==30000||
      typeof store.get!=="function"||typeof store.compareAndSwap!=="function"||!object(options.ownerBindings)||!exact(options.ownerBindings,["google","kakao"]))throw unavailable();
    const crypto=options.crypto??globalThis.crypto,now=options.now??Date.now;
    if(!crypto?.subtle)throw unavailable();
    const snapshot=()=>JSON.stringify([policy,google,kakao,options.ownerBindings]);const baseline=snapshot();
    const gate=()=>{if(snapshot()!==baseline)throw unavailable();};
    const keys={} as Record<"google"|"kakao",CryptoKey>;
    for(const provider of ["google","kakao"] as const){
      const b=options.ownerBindings[provider];
      if(!object(b)||!exact(b,["public_sha256","public_x963_b64"])||!/^[a-f0-9]{64}$/.test(b.public_sha256))throw unavailable();
      const raw=binary(b.public_x963_b64);if(raw.length!==65||raw[0]!==4||hex(await crypto.subtle.digest("SHA-256",raw))!==b.public_sha256)throw unavailable();
      keys[provider]=await crypto.subtle.importKey("raw",raw,{name:"ECDSA",namedCurve:"P-256"},false,["verify"]);
    }
    if(options.ownerBindings.google.public_sha256===options.ownerBindings.kakao.public_sha256)throw unavailable();gate();
    const verify=async(value:unknown,allowExpired=false):Promise<AppSessionCredential>=>{
      gate();if(!object(value))throw unavailable();
      const provider=value.contract_version===contracts.google?"google":value.contract_version===contracts.kakao?"kakao":null;
      if(!exact(value,["contract_version","session_token","expires_at",...(provider?["native_cleanup_proof"]:[])])||
        !provider&&value.contract_version!==contracts.plain||typeof value.session_token!=="string"||!/^[A-Za-z0-9_-]{32,200}$/.test(value.session_token)||
        typeof value.expires_at!=="string"||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(value.expires_at))throw unavailable();
      const expiry=Date.parse(value.expires_at),at=now();
      if(!Number.isFinite(expiry)||!Number.isFinite(at)||new Date(expiry).toISOString().slice(0,19)!==value.expires_at.slice(0,19)||
        !allowExpired&&expiry<=at||expiry>at+policy.maximum_session_days*86400000+policy.maximum_clock_skew_milliseconds)throw unavailable();
      if(provider){
        const p=provider==="google"?google:kakao,proof=value.native_cleanup_proof;
        if(typeof proof!=="string"||bytes(proof)>p.algorithm.maximum_envelope_bytes)throw unavailable();
        const e:unknown=JSON.parse(proof);
        if(!object(e)||!exact(e,["version","scope","payload","signature"])||e.version!=="1.0.0"||e.scope!==p.proof_scope)throw unavailable();
        const payload=binary(e.payload),signature=binary(e.signature);
        if(payload.length>p.algorithm.maximum_payload_bytes||signature.length!==64||!await crypto.subtle.verify({name:"ECDSA",hash:"SHA-256"},keys[provider],signature,payload))throw unavailable();
        const raw:unknown=JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(payload));
        const clientField=provider==="google"?"client_id":"app_id";
        if(!object(raw)||!exact(raw,["version","scope","kind","provider","bundle_identifier",clientField,"session_ref","owner_nonce","owner_digest","issued_ms","expires_ms"])||
          raw.version!=="1.0.0"||raw.scope!==p.proof_scope||raw.kind!==p.algorithm.kind||raw.provider!==provider||raw.bundle_identifier!==p.algorithm.bundle_identifier||
          raw[clientField]!== (provider==="google"?google.client_id:kakao.app_id)||raw.expires_ms!==expiry||
          !Number.isSafeInteger(raw.issued_ms)||!Number.isSafeInteger(raw.expires_ms)||Number(raw.issued_ms)<=0||
          Number(raw.issued_ms)>at+policy.maximum_clock_skew_milliseconds||Number(raw.expires_ms)<=Number(raw.issued_ms)||
          Number(raw.expires_ms)>Number(raw.issued_ms)+policy.maximum_session_days*86400000||
          typeof raw.owner_digest!=="string"||!/^[a-f0-9]{64}$/.test(raw.owner_digest)||typeof raw.owner_nonce!=="string"||!/^[A-Za-z0-9_-]{43}$/.test(raw.owner_nonce)||
          raw.session_ref!=="sha256:"+hex(await crypto.subtle.digest("SHA-256",utf8.encode(value.session_token))))throw unavailable();
        const nonce=raw.owner_nonce.replace(/-/g,"+").replace(/_/g,"/")+"=";if(binary(nonce).length!==32)throw unavailable();
      }
      gate();if(!Number.isFinite(now())||!allowExpired&&expiry<=now())throw unavailable();
      const result={contract_version:value.contract_version,session_token:value.session_token,expires_at:new Date(expiry).toISOString(),
        ...(provider?{native_cleanup_proof:value.native_cleanup_proof as string}:{})} as AppSessionCredential;
      if(bytes(JSON.stringify(result))>policy.maximum_vault_bytes)throw unavailable();return result;
    };
    const read=async(raw:string):Promise<AppSessionCredential>=>{
      if(bytes(raw)>policy.maximum_vault_bytes)throw unavailable();const v:unknown=JSON.parse(raw);
      if(!object(v)||v.environment!=="production"||v.purpose!=="public_app_session")throw unavailable();
      const {environment:_,purpose:__,...credential}=v;return verify(credential,true);
    };
    const ordered=<T>(work:()=>Promise<T>):Promise<T>=>{
      const prior=queues.get(store)??Promise.resolve(),task=prior.then(async()=>{gate();try{return await work();}catch{throw unavailable();}});
      queues.set(store,task.then(()=>{},()=>{}));return task;
    };
    const slot=async()=>{const raw=await store.get(PUBLIC_SESSION_KEY);gate();if(raw!==null&&typeof raw!=="string")throw unavailable();return raw;};
    const remove=async(raw:string|null)=>{gate();const result=await store.compareAndSwap(PUBLIC_SESSION_KEY,raw,null);gate();if(typeof result!=="boolean")throw unavailable();return result;};
    return Object.freeze({authenticationContracts:contracts,
      load:()=>ordered(async()=>{
        const raw=await slot();if(raw===null)return null;
        const value=await read(raw);
        if(Date.parse(value.expires_at)<=now()){if(!await remove(raw))throw unavailable();return null;}return value;
      }),
      save:(value:AppSessionCredential)=>{const captured=Object.freeze({...value});return ordered(async()=>{
        const raw=await slot();const checked=await verify(captured);
        const next=JSON.stringify({...checked,environment:"production",purpose:"public_app_session"});
        if(bytes(next)>policy.maximum_vault_bytes||await store.compareAndSwap(PUBLIC_SESSION_KEY,raw,next)!==true)throw unavailable();gate();
      });},
      clear:()=>ordered(async()=>{const raw=await slot();if(raw!==null)await read(raw);if(!await remove(raw))throw unavailable();}),
      clearIfCurrent:(token:string)=>ordered(async()=>{
        const raw=await slot();if(raw===null)return remove(null);
        const value=await read(raw);if(value.session_token!==token)return false;return remove(raw);
      })});
  }catch{throw unavailable();}
}
