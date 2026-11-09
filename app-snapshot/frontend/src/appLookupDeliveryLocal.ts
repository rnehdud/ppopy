import policy from "../../skin_engine/config/app_lookup_delivery_local.json";
import productPolicy from "../../skin_engine/config/product_web_match.json";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {parseMiraySavedCandidatesEnvelope,type MiraySavedCandidates,validateMirayCandidateSourceUrl} from "./miraySavedCandidates";
import {checkedIngredientDrafts,type ProductIngredientDraft} from "./productIngredientDraft";

/** Disabled local transport contract; never imported by the app connection. */
export type LookupResult = {version:"1.0.0";auto_confirmed:false} & (
  {kind:"candidates";data:MiraySavedCandidates} | {kind:"ingredient_drafts";data:ProductIngredientDraft[]}
);
export type LookupMetadata = {version:"1.0.0";lookup_id:string;status:"reserved"|"completed"|"failed"|"cancelled";cancel_requested:boolean;outcome_known:boolean};
export type LookupDelivery = LookupMetadata & {result_available:boolean;auto_confirmed:false;result:LookupResult|null};
export type LookupStart = {version:"1.0.0";lookup_id:string;status:"reserved";allowed:true}
  | {version:"1.0.0";lookup_id:null;status:"limit_reached"|"in_progress";allowed:false};
type Options = {deploymentContext:"synthetic_test";baseUrl:string;allowedBaseUrls:readonly string[];
  loadSessionToken:()=>Promise<string|null>;isCurrent?:()=>boolean;onSessionChanged?:()=>void};
type RequestOptions = {signal?:AbortSignal};
export class LookupStartUnconfirmed extends Error {
  constructor() {super("검색 시작 여부를 확인하지 못했어요. 자동으로 다시 시작하지 않습니다.");this.name="LookupStartUnconfirmed";}
}
export class LookupResponseSuperseded extends Error {
  constructor() {super("다른 검색을 시작하여 이전 결과를 표시하지 않습니다.");this.name="LookupResponseSuperseded";}
}
const invalid=()=>new Error("검색 응답 형식을 확인하지 못했어요.");
const object=(v:unknown):v is Record<string,unknown>=>Boolean(v)&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const uuid=(v:unknown):v is string=>typeof v==="string"&&/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(v);

function guard() {
  if (policy.version!=="1.0.0"||policy.scope!=="isolated_local_review"||[
    policy.runtime_registered,policy.public_enabled,policy.operational_transport_authorized,policy.provider_dispatch_enabled,
    policy.native_connection_enabled,policy.automatic_poll_or_retry,policy.response_cache_enabled,
  ].some(v=>v!==false)||policy.http.base_path!=="/v1/app/product-lookup"||policy.http.maximum_response_bytes!==69632
    ||policy.http.maximum_request_bytes!==1024||policy.deadline!=="explicit_server_deadline_not_after_origin_session_expiry"
    ||policy.delivery_scope!=="originating_member_session_only"||policy.result_confirmation!=="candidates_or_transcriptions_only"
    ||policy.unconfirmed_start!=="hold_without_automatic_restart_or_quota_inference"
    ||policy.http.start_method!=="POST"||policy.http.read_method!=="GET"||policy.http.cancel_method!=="POST"||policy.http.cancel_suffix!=="/cancel") {
    throw new Error("검색 로컬 검토 계약을 확인하지 못했어요.");
  }
}

export function checkedLookupStart(v:unknown):LookupStart {
  if (!object(v)||!exact(v,["version","lookup_id","status","allowed"])||v.version!=="1.0.0"||typeof v.status!=="string") throw invalid();
  if (v.allowed===true&&uuid(v.lookup_id)&&v.status==="reserved") return {...v} as LookupStart;
  if (v.allowed===false&&v.lookup_id===null&&["limit_reached","in_progress"].includes(String(v.status))) return {...v} as LookupStart;
  throw invalid();
}
export function checkedLookupMetadata(v:unknown,handle:string):LookupMetadata {
  if (!object(v)||!exact(v,["version","lookup_id","status","cancel_requested","outcome_known"])||v.version!=="1.0.0"
    ||!uuid(v.lookup_id)||v.lookup_id!==handle||typeof v.status!=="string"||!["reserved","completed","failed","cancelled"].includes(v.status)
    ||typeof v.cancel_requested!=="boolean"||v.outcome_known!==(v.status!=="reserved")) throw invalid();
  return {...v} as LookupMetadata;
}
export function checkedLookupDelivery(v:unknown,handle:string):LookupDelivery {
  if (!object(v)||!exact(v,["version","lookup_id","status","cancel_requested","outcome_known","result_available","auto_confirmed","result"])
    ||typeof v.result_available!=="boolean"||v.auto_confirmed!==false) throw invalid();
  const meta=checkedLookupMetadata({version:v.version,lookup_id:v.lookup_id,status:v.status,cancel_requested:v.cancel_requested,outcome_known:v.outcome_known},handle);
  if (!v.result_available) {
    if (v.result!==null) throw invalid();
    return {...meta,result_available:false,auto_confirmed:false,result:null};
  }
  if (meta.status!=="completed"||!object(v.result)||!exact(v.result,["version","kind","auto_confirmed","data"])
    ||v.result.version!=="1.0.0"||v.result.auto_confirmed!==false) throw invalid();
  let result:LookupResult;
  if (v.result.kind==="candidates") {
    const data=parseMiraySavedCandidatesEnvelope({revision:0,candidates:v.result.data}).candidates;
    if (data.candidates.some(c=>c.evidence_status!=="review_required")||new Set(data.candidates.map(c=>c.source)).size>1) throw invalid();
    result={version:"1.0.0",auto_confirmed:false,kind:"candidates",data};
  } else if (v.result.kind==="ingredient_drafts") {
    const data=checkedIngredientDrafts({provider:"openai_responses",auto_confirmed:false,drafts:v.result.data});
    // Reuse the server's public product-source restriction as well as draft bounds.
    if(data.length>productPolicy.ingredient_drafts.maximum_drafts)throw invalid();
    data.forEach(d=>{
      validateMirayCandidateSourceUrl(d.source_url);
      if(d.raw_ingredients.length>productPolicy.ingredient_drafts.maximum_raw_characters
        ||[d.product_name,d.option,d.version_note].some(s=>s.length>productPolicy.ingredient_drafts.maximum_label_characters))throw invalid();
    });
    result={version:"1.0.0",auto_confirmed:false,kind:"ingredient_drafts",data};
  } else throw invalid();
  return {...meta,result_available:true,auto_confirmed:false,result};
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

/** One live session and current handle. No caches, polling, retries or quota state. */
export function createReviewLookupDeliveryClient(fetcher:typeof fetch,options:Options) {
  guard();
  if(options.deploymentContext!=="synthetic_test"||typeof fetcher!=="function")throw invalid();
  const base=httpsBase(options.baseUrl);
  if(!options.allowedBaseUrls.map(httpsBase).includes(base))throw invalid();
  let phase:"idle"|"starting"|"active"|"terminal"|"uncertain"|"retired"="idle",handle:string|null=null;
  let generation=0;
  const active=new Set<AbortController>();
  const retire=()=>{generation++;phase="retired";handle=null;active.forEach(c=>c.abort());active.clear();};
  const isRetired=()=>phase==="retired";
  const load=createBoundMemberResponseSessionLoader(options.loadSessionToken,()=>{retire();options.onSessionChanged?.();},()=>phase!=="retired"&&(options.isCurrent?.()??true));
  const live=()=>{guard();if(phase==="retired")throw new AppMemberResponseSessionChanged();};
  const request=async<T>(method:"GET"|"POST",path:string,body:string|undefined,check:(v:unknown,status:number)=>T,opts?:RequestOptions,onSend?:()=>void):Promise<T>=>{
    live();opts?.signal?.throwIfAborted();const controller=new AbortController();active.add(controller);
    const abort=()=>controller.abort(opts?.signal?.reason);opts?.signal?.addEventListener("abort",abort,{once:true});
    try {
      const token=await load();if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new AppMemberResponseSessionChanged();
      await assertCurrentMemberResponseSession(load,token);controller.signal.throwIfAborted();live();onSend?.();
      const response=await fetcher(base+path,{method,cache:"no-store",credentials:"omit",redirect:"error",signal:controller.signal,
        headers:{Authorization:`Bearer ${token}`,...(body===undefined?{}:{"Content-Type":"application/json"})},...(body===undefined?{}:{body})});
      await assertCurrentMemberResponseSession(load,token);controller.signal.throwIfAborted();live();
      if(response.redirected||(response.url&&response.url!==base+path))throw invalid();
      if(!response.ok)throw new Error("검색 요청 결과를 확인하지 못했어요.");
      const data=await responseJson(response,controller.signal);
      await assertCurrentMemberResponseSession(load,token);controller.signal.throwIfAborted();live();
      return check(data,response.status);
    } catch(e) {
      // Failed HTTP/body reads also retire on credential or lifetime replacement.
      if(phase!=="retired")await load();
      if(e instanceof AppMemberResponseSessionChanged)throw e;
      controller.signal.throwIfAborted();throw new Error("검색 요청 결과를 확인하지 못했어요.");
    } finally {opts?.signal?.removeEventListener("abort",abort);active.delete(controller);}
  };
  return {
    async begin(query:string,opts?:RequestOptions):Promise<LookupStart> {
      live();if(phase==="starting"||phase==="active"||phase==="uncertain")throw new LookupStartUnconfirmed();
      const body=JSON.stringify({query:queryText(query)});if(new TextEncoder().encode(body).length>policy.http.maximum_request_bytes)throw invalid();
      const previous=phase;generation++;handle=null;phase="starting";let sent=false;
      try {
        const ack=await request("POST",policy.http.base_path,body,(v,status)=>{
          const ack=checkedLookupStart(v);if(status!==(ack.allowed?202:200))throw invalid();return ack;
        },opts,()=>{sent=true;});
        handle=ack.lookup_id;phase=ack.allowed?"active":"terminal";return ack;
      } catch(e) {
        if(!isRetired())phase=sent?"uncertain":previous;
        if(sent&&!(e instanceof AppMemberResponseSessionChanged))throw new LookupStartUnconfirmed();throw e;
      }
    },
    async read(opts?:RequestOptions):Promise<LookupDelivery> {
      live();if(!handle||phase==="starting"||phase==="uncertain")throw new LookupStartUnconfirmed();const current=handle,currentGeneration=generation;
      const value=await request("GET",`${policy.http.base_path}/${current}`,undefined,(v,status)=>{
        if(status!==200)throw invalid();return checkedLookupDelivery(v,current);
      },opts);
      if(handle!==current||generation!==currentGeneration)throw new LookupResponseSuperseded();if(value.outcome_known)phase="terminal";return value;
    },
    async cancel(opts?:RequestOptions):Promise<LookupMetadata> {
      live();if(!handle||phase==="starting"||phase==="uncertain")throw new LookupStartUnconfirmed();const current=handle,currentGeneration=generation;
      const value=await request("POST",`${policy.http.base_path}/${current}${policy.http.cancel_suffix}`,"{}",(v,status)=>{
        if(status!==200)throw invalid();return checkedLookupMetadata(v,current);
      },opts);
      if(handle!==current||generation!==currentGeneration)throw new LookupResponseSuperseded();if(value.outcome_known)phase="terminal";return value;
    },
    dispose:retire,
  };
}
