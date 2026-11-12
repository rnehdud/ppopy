import kb from "../../skin_engine/config/kb_choice_member_candidate.json";
import policy from "../../skin_engine/config/app_public_client_transport_review.json";
import routes from "../../skin_engine/config/app_public_auth_routes_review.json";
import state from "../../skin_engine/config/app_public_loop_state_http_review.json";
import externalSearch from "../../skin_engine/config/app_public_product_lookup_http_review.json";
import catalogSearch from "../../skin_engine/config/app_public_catalog_search_review.json";
import worker from "../../skin_engine/config/app_public_loop_worker_http_review.json";
import frequency from "../../skin_engine/config/app_public_loop_frequency_http_review.json";
import navigation from "../../skin_engine/config/miray_navigation.json";
import skin from "../../skin_engine/config/miray_skin_state.json";

/** Trusted final-build input, not a user-supplied runtime URL or GO receipt. */
export type PublicClientTransportBinding={api_id:string;api_stage:"$default";origin:string;auth_version_arn:string;
  server_source_manifest_sha256:string;binding_receipt_sha256:string;route_contract_version:string};
export type PublicNativeRequest=Readonly<{url:string;method:string;headers:Readonly<Record<string,string>>;
  body:string|null;timeoutMilliseconds:number;maximumResponseBytes:number;signal:AbortSignal}>;
export type PublicNativeResponse={url:string;status:number;headers:Record<string,string>;body:string};
/** Native implementation must enforce TLS, no redirects/cookies/cache and body
 * bounds while receiving bytes. This injected seam does not attest that code. */
export type PublicNativeRequestPort=(request:PublicNativeRequest)=>Promise<PublicNativeResponse>;
const unavailable=()=>new Error("서버 연결 결과를 확인하지 못했어요. 같은 요청은 자동으로 다시 보내지 않아요.");
const bytes=(v:string)=>new TextEncoder().encode(v).byteLength;
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const snapshot=()=>JSON.stringify([policy,routes,kb,state,worker,frequency,catalogSearch,externalSearch,navigation.portfolio_http,navigation.saved_candidates_http,skin.http]);
function checkedBinding(b:PublicClientTransportBinding):PublicClientTransportBinding{
  if(!object(b)||Object.keys(b).sort().join(",")!=="api_id,api_stage,auth_version_arn,binding_receipt_sha256,origin,route_contract_version,server_source_manifest_sha256"||
    !Object.values(b).every(v=>typeof v==="string")||b.api_stage!=="$default"||!/^[a-z0-9]{10}$/.test(b.api_id)||policy.known_TEST_api_ids.includes(b.api_id)||
    b.origin!==`https://${b.api_id}.execute-api.ap-northeast-2.amazonaws.com`||
    !/^arn:aws:lambda:ap-northeast-2:000000000000:function:skinanalysis-public-[a-z0-9-]{1,44}:[1-9][0-9]*$/.test(b.auth_version_arn)||
    !/^[a-f0-9]{64}$/.test(b.server_source_manifest_sha256)||!/^[a-f0-9]{64}$/.test(b.binding_receipt_sha256)||
    ![routes.version,kb.version].includes(b.route_contract_version))throw unavailable();
  return Object.freeze({...b});
}
function bounds(path:string){
  const candidate=kb.routes.find(r=>r.path===path);
  if(candidate)return {request:candidate.operation==="member_intake"?kb.max_intake_request_bytes:kb.max_request_bytes,response:kb.max_response_bytes};
  if(path===externalSearch.routes.search.path)return {request:externalSearch.max_request_bytes,response:externalSearch.max_response_bytes};
  for(const p of [state,worker,frequency,catalogSearch])if(Object.values(p.routes).some(r=>r.path===path))
    return {request:p.max_request_bytes,response:p.max_response_bytes};
  const request=path===navigation.portfolio_http.path?navigation.portfolio_http.max_request_bytes:
    path===navigation.saved_candidates_http.path?navigation.saved_candidates_http.max_request_bytes:
    path===skin.http.path?skin.http.max_request_bytes:policy.default_maximum_request_bytes;
  return {request,response:policy.default_maximum_response_bytes};
}
function validPolicy(){
  if(policy.version!=="1.0.0-public-client-transport-review-20261021"||
    policy.scope!=="public_client_wire_contract_not_native_registration_or_server_admission"||
    policy.automatic_retry!==false||policy.automatic_poll!==false||policy.browser_fallback!==false||
    !Number.isSafeInteger(policy.request_deadline_milliseconds)||policy.request_deadline_milliseconds<1||policy.request_deadline_milliseconds>35000||
    policy.maximum_queued_requests!==4||policy.maximum_response_headers!==64||policy.maximum_response_header_bytes!==8192||
    routes.routes.length!==26||new Set(routes.routes.map(r=>r.method+" "+r.path)).size!==26)throw unavailable();
}

const publicFetchers=new WeakMap<typeof fetch,{binding:PublicClientTransportBinding;check():void}>();
/** Only an original public transport can create service loop ports. Wrapping a
 * TEST/browser fetch in a function cannot assert this native binding. */
export function checkedPublicAppTransportBase(baseUrl:string,fetcher:typeof fetch):URL{
  const original=publicFetchers.get(fetcher);
  if(!original||baseUrl!==original.binding.origin)throw unavailable();original.check();return new URL(baseUrl);
}

/** No default sender, TEST cast, native registration or activation. Final
 * public composition must supply the original-member guard and native port. */
export function createPublicAppTransport(binding:PublicClientTransportBinding,nativeRequest:PublicNativeRequestPort,
  beforeDispatch:(request:PublicNativeRequest)=>Promise<void>){
  validPolicy();const b=checkedBinding(binding),baseline=snapshot();let active=true,pending=0,tail=Promise.resolve();
  const kbCandidate=b.route_contract_version===kb.version && kb.production_enabled===false;
  const allowedRoutes=kbCandidate?[...routes.routes,...kb.routes]:routes.routes;
  const controls=new Set<AbortController>();
  const gate=()=>{if(!active||snapshot()!==baseline)throw unavailable();validPolicy();};
  const retire=()=>{active=false;for(const controller of controls)controller.abort();};
  const execute:typeof fetch=async(input,init)=>{
    gate();if(input instanceof Request||typeof nativeRequest!=="function"||typeof beforeDispatch!=="function")throw unavailable();
    const url=new URL(String(input)),method=init?.method??"GET";
    if(String(input)!==url.href||url.origin!==b.origin||url.href!==b.origin+url.pathname||!allowedRoutes.some(r=>r.path===url.pathname&&r.method===method)||
      (init?.credentials!==undefined&&init.credentials!=="omit")||(init?.cache!==undefined&&init.cache!=="no-store")||
      (init?.redirect!==undefined&&init.redirect!=="error")||init?.keepalive===true||init?.referrer||init?.integrity)throw unavailable();
    const headers=new Headers(init?.headers),out:Record<string,string>={};
    headers.forEach((v,k)=>{if(!["authorization","content-type","accept"].includes(k)||v.length>512)throw unavailable();out[k]=v;});
    const anonymous=url.pathname==="/api/v1/app/auth/protection-session";
    if(anonymous?headers.has("authorization"):!/^Bearer [A-Za-z0-9_-]{32,200}$/.test(headers.get("authorization")??""))throw unavailable();
    if(headers.has("accept")&&headers.get("accept")!=="application/json"){
      const accept=headers.get("accept")!,allowed=method==="GET"&&url.pathname===state.routes.read.path
        ?policy.state_read_accept:method==="POST"&&[state.routes.registration.path,state.routes.actual.path,state.routes.followup.path].includes(url.pathname)
          ?policy.state_write_accept:[];
      if(!allowed.includes(accept))throw unavailable();
    }
    const limit=bounds(url.pathname);let body:string|null=null;
    if(method==="GET"||method==="DELETE"){
      if(init?.body!=null&&init.body!==""||headers.has("content-type"))throw unavailable();
    }else{
      if(typeof init?.body!=="string"||headers.get("content-type")!=="application/json"||bytes(init.body)>limit.request)throw unavailable();
      try{if(!object(JSON.parse(init.body)))throw unavailable();}catch{throw unavailable();}body=init.body;
    }
    init?.signal?.throwIfAborted();if(pending>=policy.maximum_queued_requests)throw unavailable();
    const controller=new AbortController();controls.add(controller);pending++;
    const abort=()=>controller.abort();init?.signal?.addEventListener("abort",abort,{once:true});
    if(init?.signal?.aborted)controller.abort();
    const deadline=Date.now()+policy.request_deadline_milliseconds;
    let timer:ReturnType<typeof setTimeout>|undefined;
    const timed=new Promise<never>((_,reject)=>{
      const stop=()=>reject(unavailable());controller.signal.addEventListener("abort",stop,{once:true});
      if(controller.signal.aborted)stop();timer=setTimeout(()=>controller.abort(),policy.request_deadline_milliseconds);
    });
    const live=()=>{gate();if(controller.signal.aborted||Date.now()>=deadline)throw unavailable();};
    const task=tail.then(async()=>{
      live();const request=Object.freeze({url:url.href,method,headers:Object.freeze({...out}),body,
        timeoutMilliseconds:Math.max(1,deadline-Date.now()),maximumResponseBytes:limit.response,signal:controller.signal});
      await beforeDispatch(request);live();
      const result=await nativeRequest(Object.freeze({...request,timeoutMilliseconds:Math.max(1,deadline-Date.now())}));live();
      if(!object(result)||result.url!==url.href||!Number.isInteger(result.status)||result.status<200||result.status>599||result.status>=300&&result.status<400||
        !object(result.headers)||typeof result.body!=="string"||bytes(result.body)>limit.response)throw unavailable();
      const responseHeaders=new Headers();let size=0;const seen=new Set<string>(),entries=Object.entries(result.headers);
      if(entries.length>policy.maximum_response_headers)throw unavailable();
      for(const [k,v]of entries){
        const key=k.toLowerCase();size+=bytes(k)+bytes(String(v));
        if(typeof v!=="string"||seen.has(key)||key==="set-cookie"||size>policy.maximum_response_header_bytes)throw unavailable();
        seen.add(key);responseHeaders.set(k,v);
      }
      if(responseHeaders.get("content-type")?.split(";")[0]!=="application/json"||
        responseHeaders.get("cache-control")?.trim().toLowerCase()!=="no-store"||
        responseHeaders.has("content-encoding")&&responseHeaders.get("content-encoding")!=="identity")throw unavailable();
      const length=responseHeaders.get("content-length");
      if(length!==null&&(!/^\d+$/.test(length)||Number(length)!==bytes(result.body)))throw unavailable();
      if([204,205].includes(result.status)){if(result.body!=="")throw unavailable();return new Response(null,{status:result.status,headers:responseHeaders});}
      return new Response(result.body,{status:result.status,headers:responseHeaders});
    });
    // An abandoned native operation may still be in flight. Keep later work
    // behind its actual settlement; queued calls have their own total deadline.
    tail=task.then(()=>{},()=>{});
    // Capacity belongs to actual queued/native work, not an observer that may
    // have timed out. A hung port can retain at most the configured four slots.
    void task.then(()=>{controls.delete(controller);pending--;},()=>{controls.delete(controller);pending--;});
    try{return await Promise.race([task,timed]);}
    catch{throw unavailable();}
    finally{if(timer!==undefined)clearTimeout(timer);init?.signal?.removeEventListener("abort",abort);}
  };
  const fetcher:typeof fetch=async(input,init)=>{try{return await execute(input,init);}catch{throw unavailable();}};
  publicFetchers.set(fetcher,{binding:b,check:gate});
  return Object.freeze({origin:b.origin,fetcher,retire,kbCandidate});
}
