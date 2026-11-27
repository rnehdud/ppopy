import policy from "../../skin_engine/config/app_lookup_request_local.json";
import productPolicy from "../../skin_engine/config/product_web_match.json";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {checkedLookupStart,checkedLookupDelivery,checkedLookupMetadata,LookupStartUnconfirmed,LookupResponseSuperseded,type LookupStart,type LookupDelivery,type LookupMetadata} from "./appLookupDeliveryLocal";

/** Disabled transport review. Request IDs are not worker/member capabilities. */
export type LookupRequestConfirmation={version:"1.0.0";request_id:string;confirmed:true;start:LookupStart}
  | {version:"1.0.0";request_id:string;confirmed:false;start:null};
type Options={deploymentContext:"synthetic_test";baseUrl:string;allowedBaseUrls:readonly string[];
  loadSessionToken:()=>Promise<string|null>;isCurrent?:()=>boolean;onSessionChanged?:()=>void};
type RequestOptions={signal?:AbortSignal};
const invalid=()=>new Error("검색 요청의 확인 결과를 확인하지 못했어요.");
const uuid=(v:unknown):v is string=>typeof v==="string"&&/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(v);
function guard(){
  if(policy.version!=="1.0.0"||policy.scope!=="isolated_local_review"||[
    policy.runtime_registered,policy.public_enabled,policy.operational_mac_authorized,policy.operational_transport_authorized,
    policy.provider_dispatch_enabled,policy.native_connection_enabled,policy.automatic_poll_or_retry,policy.request_backfill_enabled,policy.metadata_deletion_enabled,
  ].some(v=>v!==false)||policy.namespace!=="lookup_accepted_request_binding"||policy.key_ref!=="synthetic:lookup-request-hmac-v1"
    ||policy.http.base_path!=="/v1/app/product-lookup"||policy.http.request_suffix!=="/requests"
    ||policy.http.maximum_request_bytes!==1024||policy.http.maximum_response_bytes!==69632
    ||policy.request_id!=="canonical_random_uuid_v4_not_authority"||policy.retry!=="explicit_same_key_and_same_normalized_query"
    ||policy.recovery!=="original_member_session_metadata_only"||policy.missing!=="unconfirmed_not_zero_work"
    ||policy.denial!=="not_persisted_not_an_accepted_request"||policy.acknowledgement!=="original_admission_not_current_outcome")throw invalid();
}

// Share the already reviewed policy/query/strict byte checks with the disabled
// restart adapter. This export does not change this live client's behavior.
export {guard as assertReviewLookupRequestPolicy,httpsBase as checkedReviewLookupBase,
  queryText as checkedReviewLookupQuery,responseJson as readReviewLookupResponseJson};
export function checkedLookupRequest(v:unknown,key:string,recovery=false):LookupRequestConfirmation{
  if(!uuid(key)||!v||typeof v!=="object"||Array.isArray(v))throw invalid();const x=v as Record<string,unknown>;
  if(Object.keys(x).sort().join("|")!==["version","request_id","confirmed","start"].sort().join("|")
    ||x.version!=="1.0.0"||x.request_id!==key||typeof x.confirmed!=="boolean")throw invalid();
  if(!x.confirmed){if(x.start!==null)throw invalid();return {version:"1.0.0",request_id:key,confirmed:false,start:null};}
  const start=checkedLookupStart(x.start);if(recovery&&!start.allowed)throw invalid();
  return {version:"1.0.0",request_id:key,confirmed:true,start};
}

function httpsBase(value:string):string {
  const u=new URL(value);
  if (u.protocol!=="https:"||!u.hostname||u.username||u.password||u.search||u.hash) throw invalid();
  return `${u.origin}${u.pathname.replace(/\/+$/,"")}`;
}
function queryText(value:string):string {
  if (typeof value!=="string"||/[\r\n@]/.test(value)) throw invalid();
  const q=value.normalize("NFKC").trim().replace(/\s+/g," ");
  const length=Array.from(q).length;
  if (length<2||length>productPolicy.request.maximum_query_characters||q.includes("@")||/(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}/.test(q)) throw invalid();
  return q;
}
/** Bound JSON bytes, strict UTF-8, and duplicate object keys, including escaped keys. */
async function responseJson(response:Response,signal:AbortSignal):Promise<unknown> {
  if (response.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase()!=="application/json"||!response.body) throw invalid();
  const reader=response.body.getReader(),chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal.addEventListener("abort",abort,{once:true});
  try {
    signal.throwIfAborted();
    for (;;) {
      const {done,value}=await reader.read();signal.throwIfAborted();if(done)break;
      size+=value.byteLength;if(size>policy.http.maximum_response_bytes)throw invalid();chunks.push(value);
    }
  } catch(e) {await reader.cancel().catch(()=>{});throw e;}
  finally {signal.removeEventListener("abort",abort);reader.releaseLock();}
  const bytes=new Uint8Array(size);let offset=0;chunks.forEach(c=>{bytes.set(c,offset);offset+=c.byteLength;});
  const text=new TextDecoder("utf-8",{fatal:true}).decode(bytes),value:unknown=JSON.parse(text);
  const stack:(Set<string>|null)[]=[];
  for (let i=0;i<text.length;i++) {
    if (text[i]==='"') {
      const start=i;for(i++;i<text.length;i++){if(text[i]==='\\'){i++;continue;}if(text[i]==='"')break;}
      let next=i+1;while(/\s/.test(text[next]||"x"))next++;
      if(text[next]===":") {
        const keys=stack.at(-1),key=JSON.parse(text.slice(start,i+1)) as string;
        if(!keys||keys.has(key))throw invalid();keys.add(key);
      }
    } else if(text[i]==="{")stack.push(new Set());else if(text[i]==="[")stack.push(null);
    else if(text[i]==="}"||text[i]==="]")stack.pop();
  }
  return value;
}

/** Explicit recovery/retry only. Holds opaque IDs in this live connection;
 * no plaintext query/result cache, persistence, polling, or quota inference. */
export function createReviewLookupRequestClient(fetcher:typeof fetch,options:Options){
  guard();if(options.deploymentContext!=="synthetic_test"||typeof fetcher!=="function")throw invalid();
  const base=httpsBase(options.baseUrl);if(!options.allowedBaseUrls.map(httpsBase).includes(base))throw invalid();
  let phase:"idle"|"starting"|"active"|"terminal"|"uncertain"|"recovering"|"retrying"|"retired"="idle";
  let key:string|null=null,handle:string|null=null,generation=0;
  const active=new Set<AbortController>();
  const retire=()=>{generation++;phase="retired";key=null;handle=null;active.forEach(c=>c.abort());active.clear();};
  const isRetired=()=>phase==="retired";
  const load=createBoundMemberResponseSessionLoader(options.loadSessionToken,()=>{retire();options.onSessionChanged?.();},()=>!isRetired()&&(options.isCurrent?.()??true));
  const live=()=>{guard();if(isRetired())throw new AppMemberResponseSessionChanged();};
  const request=async<T>(method:"GET"|"POST",path:string,body:string|undefined,check:(v:unknown,status:number)=>T,opts?:RequestOptions,onSend?:()=>void):Promise<T>=>{
    live();opts?.signal?.throwIfAborted();const controller=new AbortController();active.add(controller);
    const scoped=load.within(()=>!controller.signal.aborted);
    const abort=()=>controller.abort(opts?.signal?.reason);opts?.signal?.addEventListener("abort",abort,{once:true});
    try{
      const token=await scoped();if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new AppMemberResponseSessionChanged();
      await assertCurrentMemberResponseSession(scoped,token);controller.signal.throwIfAborted();live();onSend?.();
      const response=await fetcher(base+path,{method,cache:"no-store",credentials:"omit",redirect:"error",signal:controller.signal,
        headers:{Authorization:`Bearer ${token}`,...(body===undefined?{}:{"Content-Type":"application/json"})},...(body===undefined?{}:{body})});
      await assertCurrentMemberResponseSession(scoped,token);controller.signal.throwIfAborted();live();
      if(response.redirected||(response.url&&response.url!==base+path)||!response.ok)throw invalid();
      const data=await responseJson(response,controller.signal);
      await assertCurrentMemberResponseSession(scoped,token);controller.signal.throwIfAborted();live();return check(data,response.status);
    }catch(e){
      if(!isRetired()){controller.signal.throwIfAborted();await scoped();}if(e instanceof AppMemberResponseSessionChanged)throw e;
      controller.signal.throwIfAborted();throw invalid();
    }finally{opts?.signal?.removeEventListener("abort",abort);active.delete(controller);}
  };
  const requestBase=policy.http.base_path+policy.http.request_suffix;
  const current=(k:string,g:number)=>{if(key!==k||generation!==g)throw new LookupResponseSuperseded();};
  const submit=async(query:string,retry:boolean,opts?:RequestOptions):Promise<LookupRequestConfirmation>=>{
    live();if(retry?phase!=="uncertain"||!key:phase!=="idle"&&phase!=="terminal")throw new LookupStartUnconfirmed();
    const normalized=queryText(query),previous=phase,previousKey=key,previousHandle=handle;
    const selected=retry?key!:crypto.randomUUID();if(!uuid(selected))throw invalid();
    const body=JSON.stringify({request_id:selected,query:normalized});if(new TextEncoder().encode(body).length>policy.http.maximum_request_bytes)throw invalid();
    key=selected;handle=null;generation++;const g=generation;phase=retry?"retrying":"starting";let sent=false;
    try{
      const ack=await request("POST",requestBase,body,(v,status)=>{
        const a=checkedLookupRequest(v,selected);if(!a.confirmed||status!==(a.start.allowed?202:200))throw invalid();return a;
      },opts,()=>{sent=true;});
      current(selected,g);if(!ack.confirmed)throw invalid();handle=ack.start.lookup_id;phase=ack.start.allowed?"active":"terminal";return ack;
    }catch(e){
      if(!isRetired()&&generation===g){phase=sent?"uncertain":previous;if(!sent){key=previousKey;handle=previousHandle;}}
      if(sent&&!(e instanceof AppMemberResponseSessionChanged)&&!(e instanceof LookupResponseSuperseded))throw new LookupStartUnconfirmed();throw e;
    }
  };
  return{
    begin:(query:string,opts?:RequestOptions)=>submit(query,false,opts),
    retryStart:(query:string,opts?:RequestOptions)=>submit(query,true,opts),
    async recover(opts?:RequestOptions):Promise<LookupRequestConfirmation>{
      live();if(phase!=="uncertain"||!key)throw new LookupStartUnconfirmed();const k=key,g=generation;phase="recovering";
      try{
        const value=await request("GET",requestBase+"/"+k,undefined,(v,status)=>{if(status!==200)throw invalid();return checkedLookupRequest(v,k,true);},opts);
        current(k,g);if(value.confirmed){handle=value.start.lookup_id;phase="active";}else phase="uncertain";return value;
      }catch(e){if(!isRetired()&&generation===g)phase="uncertain";throw e;}
    },
    async read(opts?:RequestOptions):Promise<LookupDelivery>{
      live();if(!handle||(phase!=="active"&&phase!=="terminal"))throw new LookupStartUnconfirmed();const h=handle,k=key!,g=generation;
      const value=await request("GET",policy.http.base_path+"/"+h,undefined,(v,status)=>{if(status!==200)throw invalid();return checkedLookupDelivery(v,h);},opts);
      current(k,g);if(handle!==h)throw new LookupResponseSuperseded();if(value.outcome_known)phase="terminal";return value;
    },
    async cancel(opts?:RequestOptions):Promise<LookupMetadata>{
      live();if(!handle||(phase!=="active"&&phase!=="terminal"))throw new LookupStartUnconfirmed();const h=handle,k=key!,g=generation;
      const value=await request("POST",policy.http.base_path+"/"+h+"/cancel","{}",(v,status)=>{if(status!==200)throw invalid();return checkedLookupMetadata(v,h);},opts);
      current(k,g);if(handle!==h)throw new LookupResponseSuperseded();if(value.outcome_known)phase="terminal";return value;
    },
    state:()=>({phase}),dispose:retire,
  };
}
