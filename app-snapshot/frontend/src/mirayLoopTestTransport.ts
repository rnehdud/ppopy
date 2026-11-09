import {Capacitor,CapacitorHttp,type HttpResponse} from "@capacitor/core";
import policy from "../../skin_engine/config/miray_closed_loop_native_test.json";
import state from "../../skin_engine/config/miray_closed_loop_state_http_test.json";
import worker from "../../skin_engine/config/miray_closed_loop_worker_http_test.json";
import frequency from "../../skin_engine/config/miray_closed_loop_frequency_test.json";
import {APP_AUTH_TEST_API_ORIGIN} from "./iosAppAuthFetcher";
import {serializeIOSAppTestRequest} from "./iosAppTestRequestQueue";
import {loopTestFailure} from "./loopTestFailureCode";
import executionBudget from "../../skin_engine/config/app_test_execution_budget.json";
import bootstrapResume from "../../skin_engine/config/app_loop_bootstrap_resume_test.json";

// An arbitrary injected fetch cannot open the native HTTPS surface. Existing
// loopback ports keep their original behavior; only this constructor brands it.
const nativeFetchers=new WeakSet<typeof fetch>();
const contracts={miray_closed_loop_state_http_test:state,miray_closed_loop_worker_http_test:worker,miray_closed_loop_frequency_test:frequency};
const object=(v:unknown):v is Record<string,unknown>=>!!v && typeof v==="object" && !Array.isArray(v);
const bytes=(v:string)=>new TextEncoder().encode(v).byteLength;
const unavailable=(kind:"P"|"N"|"M"|"B"|"J"="P",status?:number)=>loopTestFailure("T",kind,status);
function snapshot(){return JSON.stringify([policy,state,worker,frequency,executionBudget,bootstrapResume]);}
function nativeResponseText(data:unknown):string{
  if(typeof data==="string")return data;
  if(!object(data))throw unavailable("J");
  // iOS buildResponse decodes application/json even for responseType:"text".
  // Rebuild only JSON values; do not drop undefined, non-finite values or allow
  // custom toJSON/prototypes to silently change the received state.
  return JSON.stringify(data,function(key,value){
    const original=this[key];
    if(original!==value)throw unavailable("J");
    if(value===null || typeof value==="string" || typeof value==="boolean" ||
      (typeof value==="number" && Number.isFinite(value)))return value;
    if(typeof value==="object" && (Array.isArray(value) || Object.getPrototypeOf(value)===Object.prototype || Object.getPrototypeOf(value)===null))return value;
    throw unavailable("J");
  });
}
export function assertNativeLoopTestPolicy(){
  if(Object.keys(bootstrapResume).sort().join("|")!==[
    "version","scope","runtime_enabled","public_enabled","explicit_factory_option_required","reviewed_server_code_sha256",
    "retryable_status","retryable_error_code","route_dispatch_performed","max_attempts","delay_milliseconds",
    "budget_milliseconds","minimum_remaining_request_milliseconds","ambiguous_response_or_network_failure_retry","quota_reset_or_automatic_poll",
  ].sort().join("|") || bootstrapResume.version!=="1.0.0-test-bootstrap-resume-20261011" ||
    bootstrapResume.scope!=="existing_seoul_test_candidate_only" || bootstrapResume.runtime_enabled!==false ||
    bootstrapResume.public_enabled!==false || bootstrapResume.explicit_factory_option_required!==true ||
    bootstrapResume.reviewed_server_code_sha256!=="ae54e2e78447b3b6df84e34592dc55ec309df8575846715f1b07082b3d7ca7ab" ||
    bootstrapResume.retryable_status!==503 || bootstrapResume.retryable_error_code!=="auth_database_resuming" ||
    bootstrapResume.route_dispatch_performed!==false || bootstrapResume.max_attempts!==2 ||
    bootstrapResume.delay_milliseconds!==2000 || bootstrapResume.budget_milliseconds!==60000 ||
    bootstrapResume.minimum_remaining_request_milliseconds!==executionBudget.native_request_timeout_milliseconds ||
    bootstrapResume.ambiguous_response_or_network_failure_retry!==false || bootstrapResume.quota_reset_or_automatic_poll!==false)throw unavailable();
  if(executionBudget.scope!=="existing_seoul_test_runtime_only" ||
    executionBudget.lambda_timeout_seconds!==28 || executionBudget.api_integration_timeout_milliseconds!==30000 ||
    executionBudget.native_request_timeout_milliseconds!==35000 || executionBudget.ambiguous_write_retry!==false ||
    executionBudget.quota_reset_or_member_data_changes!==false)throw unavailable();
  if(policy.scope!=="aws_test_candidate_not_applied" || policy.origin!==APP_AUTH_TEST_API_ORIGIN ||
    [policy.runtime_enabled,policy.installed_factory,policy.apply_approval,policy.automatic_retry,policy.automatic_poll].some(v=>v!==false))throw unavailable();
  const routes=Object.entries(contracts).flatMap(([name,c])=>{
    if(c.scope!==policy.scope || c.version!==policy.contract_versions[name as keyof typeof contracts] ||
      c.runtime_enabled!==false || c.runtime_registered!==false || c.automatic_retry!==false || c.automatic_poll!==false)throw unavailable();
    return Object.entries(c.routes).map(([action,r])=>({contract:name,action,...r,max_request_bytes:c.max_request_bytes,max_response_bytes:c.max_response_bytes}));
  });
  if(JSON.stringify(routes)!==JSON.stringify(policy.routes) || routes.length!==8)throw unavailable();
}

/** Same DTO/member/consent state machines for loopback and a branded native TEST
 * transport. HTTPS still needs an explicit review composition; no default. */
export function checkedLoopTestTransportBase(baseUrl:string,fetcher:typeof fetch):URL{
  const url=new URL(baseUrl);
  if(url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw unavailable();
  if(url.protocol==="http:" && url.hostname==="127.0.0.1" && url.port)return url;
  assertNativeLoopTestPolicy();
  if(url.origin!==policy.origin || !nativeFetchers.has(fetcher))throw unavailable();
  return url;
}

function abandoned<T>(operation:Promise<T>,signal?:AbortSignal|null):Promise<T>{
  if(!signal)return operation;
  return new Promise((resolve,reject)=>{
    const abort=()=>{signal.removeEventListener("abort",abort);reject(signal.reason??new DOMException("Aborted","AbortError"));};
    if(signal.aborted)abort();else signal.addEventListener("abort",abort,{once:true});
    operation.then(v=>{signal.removeEventListener("abort",abort);if(!signal.aborted)resolve(v);},e=>{signal.removeEventListener("abort",abort);reject(e);});
  });
}

/** Normally one native request. The explicitly selected TEST option permits
 * one additional attempt only after the exact pre-dispatch bootstrap receipt.
 * Retirement cannot cancel or undo a possibly committed native write. */
export function createNativeLoopTestFetcher(options:{bootstrapResumeEnabled?:boolean}={}):typeof fetch{
  assertNativeLoopTestPolicy();const baseline=snapshot();
  const resumeEnabled=options.bootstrapResumeEnabled===true;
  const gate=()=>{assertNativeLoopTestPolicy();if(snapshot()!==baseline)throw unavailable();};
  const execute=async(input:RequestInfo|URL,init:RequestInit|undefined,current:()=>boolean,prepare?:()=>Promise<void>)=>{
    const currentGate=()=>{gate();init?.signal?.throwIfAborted();if(!current())throw unavailable();};
    currentGate();
    gate();init?.signal?.throwIfAborted();
    if(!Capacitor.isNativePlatform() || Capacitor.getPlatform()!=="ios" || input instanceof Request)throw unavailable();
    const url=new URL(String(input)),method=init?.method??"GET";
    const route=policy.routes.find(r=>r.path===url.pathname && r.method===method);
    if(!route || url.origin!==policy.origin || url.username || url.password || url.search || url.hash ||
      init?.credentials!=="omit" || init.cache!=="no-store" || init.redirect!=="error")throw unavailable();
    const headers=new Headers(init.headers),headerValues:Record<string,string>={};
    headers.forEach((value,key)=>{if(!["authorization","content-type","accept"].includes(key))throw unavailable();headerValues[key]=value;});
    if(!new RegExp(policy.bearer_pattern).test(headers.get("authorization")??""))throw unavailable();
    if(headers.has("accept")){
      const accepted=headers.get("accept"),statePath=state.routes.read.path;
      const statePost=method==="POST" && [state.routes.registration.path,state.routes.actual.path,state.routes.followup.path].includes(url.pathname);
      const allowed=method==="GET" && url.pathname===statePath && ["application/vnd.poppy.loop-entry+json","application/vnd.poppy.loop-entry+json; products=1","application/vnd.poppy.loop-products+json","application/vnd.poppy.loop-entry+json; products=2","application/vnd.poppy.loop-products-v2+json"].includes(accepted??"") ||
        statePost && ["application/vnd.poppy.loop-products+json","application/vnd.poppy.loop-products-v2+json"].includes(accepted??"");
      if(!allowed)throw unavailable();
    }
    const capturedBody=typeof init.body==="string"?init.body:undefined;
    let data:unknown;
    if(method==="GET"){
      if(init.body!=null || headers.has("content-type"))throw unavailable();
    }else{
      if(typeof init.body!=="string" || headers.get("content-type")!=="application/json" || bytes(init.body)>route.max_request_bytes)throw unavailable();
      data=JSON.parse(init.body);
      // Preserve the port's frozen JSON; reject duplicate/non-finite or modified
      // serialization instead of silently changing the confirmed request.
      if(!object(data) || JSON.stringify(data)!==init.body)throw unavailable();
    }
    gate();init.signal?.throwIfAborted();
    const checkedResponse=(result:HttpResponse)=>{
      currentGate();
      if(result.url!==url.href || !Number.isInteger(result.status) || result.status<200 || result.status>599 ||
        !object(result.headers))throw unavailable("M",result.status);
      const text=nativeResponseText(result.data),responseBytes=bytes(text);
      if(responseBytes>route.max_response_bytes)throw unavailable("B",result.status);
      const responseHeaders=new Headers(),seen=new Set<string>();let headerBytes=0;
      const entries=Object.entries(result.headers);
      if(entries.length>policy.max_response_headers)throw unavailable("M",result.status);
      for(const [key,value]of entries){
        const normalized=key.toLowerCase();if(typeof value!=="string" || seen.has(normalized) || normalized==="set-cookie")throw unavailable("M",result.status);
        seen.add(normalized);headerBytes+=bytes(key)+bytes(value);if(headerBytes>policy.max_response_header_bytes)throw unavailable("B",result.status);
        responseHeaders.set(key,value);
      }
      if(responseHeaders.get("content-type")?.split(";")[0]!=="application/json" ||
        !responseHeaders.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store") ||
        (responseHeaders.has("content-encoding") && responseHeaders.get("content-encoding")!=="identity"))throw unavailable("M",result.status);
      const declared=responseHeaders.get("content-length");
      if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>route.max_response_bytes ||
        (typeof result.data==="string" && Number(declared)!==responseBytes)))throw unavailable("B",result.status);
      // Decoded objects no longer retain wire whitespace/escapes/number spelling.
      // Bound both the declared wire size and reconstructed UTF-8 size; give the
      // port the reconstructed length without claiming original byte identity.
      if(declared!==null && typeof result.data!=="string")responseHeaders.set("content-length",String(responseBytes));
      return {text,response:new Response(text,{status:result.status,headers:responseHeaders})};
    };
    const deadline=Date.now()+bootstrapResume.budget_milliseconds;
    return abandoned(serializeIOSAppTestRequest(url.origin,async()=>{
      const attempts=resumeEnabled?bootstrapResume.max_attempts:1;
      for(let attempt=0;attempt<attempts;attempt++){
        if(prepare)await prepare();currentGate();
        const remaining=deadline-Date.now();
        if(resumeEnabled && remaining<bootstrapResume.minimum_remaining_request_milliseconds)throw unavailable("N");
        // Each attempt gets the same captured JSON and headers, even if an SDK
        // mutates its arguments. The member port rechecks its original token.
        const result=await CapacitorHttp.request({url:url.href,method,headers:{...headerValues},
          data:data===undefined?undefined:JSON.parse(capturedBody!),
          connectTimeout:executionBudget.native_request_timeout_milliseconds,readTimeout:executionBudget.native_request_timeout_milliseconds,
          disableRedirects:true,responseType:"text"}).catch(()=>{throw unavailable("N");});
        const {text,response}=checkedResponse(result);
        // Both exact server json.dumps and Capacitor's decoded-object ABI.
        // Extra fields, generic 503, malformed headers and lost ACKs never retry.
        const code=bootstrapResume.retryable_error_code;
        const preDispatch=response.status===bootstrapResume.retryable_status &&
          (text===JSON.stringify({code}) || text===`{"code": "${code}"}`);
        if(!resumeEnabled || !preDispatch || attempt+1===attempts ||
          deadline-Date.now()<bootstrapResume.delay_milliseconds+bootstrapResume.minimum_remaining_request_milliseconds)return response;
        await abandoned(new Promise<void>(resolve=>setTimeout(resolve,bootstrapResume.delay_milliseconds)),init.signal);
        currentGate();
      }
      throw unavailable();
    },{signal:init.signal,beforeDispatch:currentGate}),init.signal);
  };
  const scoped=(current:()=>boolean,prepare?:()=>Promise<void>):typeof fetch=>{
    const fetcher=Object.assign(((input:RequestInfo|URL,init?:RequestInit)=>execute(input,init,current,prepare))as typeof fetch,
      {within:(nested:()=>boolean,nestedPrepare?:()=>Promise<void>)=>scoped(()=>current()&&nested(),
        prepare||nestedPrepare?async()=>{if(prepare)await prepare();if(nestedPrepare)await nestedPrepare();}:undefined)});
    nativeFetchers.add(fetcher);return fetcher;
  };
  return scoped(()=>true);
}
