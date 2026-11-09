import http from "../../skin_engine/config/miray_closed_loop_frequency_http_review.json";
import config from "../../skin_engine/config/miray_closed_loop_frequency_review.json";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {assertFrequencyCorrectionReviewOnly,parseFrequencyCorrectionView,parseFrequencyCorrectionAck,validateFrequencyCorrectionRequest,type FrequencyCorrectionReviewStore,type FrequencyCorrectionRequest} from "./mirayClosedLoopFrequency";

async function boundedText(response:Response,signal:AbortSignal|undefined,gate:()=>void){
  gate();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>http.max_response_bytes))throw new Error("Frequency response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Frequency response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){gate();const part=await reader.read();gate();if(part.done)break;
      size+=part.value.byteLength;if(size>http.max_response_bytes)throw new Error("Frequency response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}

/** Explicit injected loopback review only; no native/default transport or retries. */
export function createFrequencyCorrectionHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):FrequencyCorrectionReviewStore{
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit frequency loopback transport required");
  const baseline=JSON.stringify([http,config,loop]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  let decision:string|undefined;
  const gate=()=>{assertFrequencyCorrectionReviewOnly();if(http.deployment_context!=="synthetic_test" || [http.enabled,http.registered,http.automatic_retry,http.automatic_poll].some(v=>v!==false) || JSON.stringify([http,config,loop])!==baseline)throw new Error("Frequency HTTP activation is not approved");};gate();
  const correlate=(ref:string)=>{if(decision!==undefined && decision!==ref)throw new Error("Frequency decision changed");decision=ref;};
  const run=async(action:"read"|"confirm",request?:FrequencyCorrectionRequest,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const currentGate=()=>{scope.gate();gate();};currentGate();
    // Clone and encode before any asynchronous session hook can mutate input.
    const frozen=request===undefined?undefined:validateFrequencyCorrectionRequest(request);
    if(frozen)correlate(frozen.decision_ref);
    const encoded=frozen===undefined?undefined:JSON.stringify(frozen);
    const load=scope.load,transport=scope.fetch(fetcher);
    const value=await scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");currentGate();const route=http.routes[action];
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(encoded?{"Content-Type":"application/json"}:{})},body:encoded,signal,credentials:"omit",cache:"no-store",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Frequency response unavailable");
      const text=await boundedText(response,signal,currentGate);currentGate();
      const parsed=action==="read"?parseFrequencyCorrectionView(JSON.parse(text)):parseFrequencyCorrectionAck(JSON.parse(text),frozen);
      correlate("view" in parsed?parsed.view.decision_ref:parsed.decision_ref);return parsed;
    }));
    currentGate();return value;
  };
  return {read:o=>run("read",undefined,o),confirm:(r,o)=>run("confirm",r,o)};
}
