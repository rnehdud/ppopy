import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_entry_http_review.json";
import {assertAccountEntrySelectorReviewOnly} from "./mirayClosedLoopEntrySelector";
import {assertOriginalEntryResumeReviewOnly} from "./mirayClosedLoopAdmission";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {parseLoopEntryView,validateLoopEntryRequest,type ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";

async function boundedText(response:Response,signal:AbortSignal|undefined,gate:()=>void){
  gate();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Review response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Review response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){
      gate();const part=await reader.read();gate();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Review response too large");chunks.push(part.value);
    }
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}

/** Explicit injected loopback fetcher only. No global fetch/runtime/native default. */
export function createAccountEntryHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):ClosedLoopEntryReviewStore{
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit local review transport required");
  const baseline=JSON.stringify(config),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const gate=()=>{
    if(JSON.stringify(config)!==baseline || config.enabled!==false || config.registered!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false)throw new Error("Unapproved HTTP review");
  };
  gate();
  const run=(action:"read"|"recover"|"resume"|"fresh"|"submit",body:unknown,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const currentGate=()=>{scope.gate();gate();};currentGate();
    const load=scope.load,transport=scope.fetch(fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");
      currentGate();
      const route=config.routes[action],encoded=body===null?undefined:JSON.stringify(body);
      if(encoded && new TextEncoder().encode(encoded).length>config.max_request_bytes)throw new Error("Review request too large");
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(encoded?{"Content-Type":"application/json"}:{})},
        body:encoded,signal,credentials:"omit",cache:"no-store",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Review response unavailable");
      const text=await boundedText(response,signal,currentGate);currentGate();
      return parseLoopEntryView(JSON.parse(text));
    }));
  };
  return {
    read:options=>run("read",null,options),
    recover:(entryRef,options)=>{assertAccountEntrySelectorReviewOnly(entryRef);return run("recover",{entry_ref:entryRef},options);},
    resume:(entryRef,options)=>{assertOriginalEntryResumeReviewOnly(entryRef);return run("resume",{entry_ref:entryRef},options);},
    startFresh:(entryRef,options)=>{assertAccountEntrySelectorReviewOnly(entryRef);return run("fresh",{entry_ref:entryRef},options);},
    submit:(request,options)=>{validateLoopEntryRequest(request);return run("submit",structuredClone(request),options);},
  };
}
