import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_next_review.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {assertNextReviewOnly,nextRef,parseNextDecisionView,type NextDecisionReviewStore} from "./mirayClosedLoopNext";
async function boundedText(response:Response,signal:AbortSignal|undefined,gate:()=>void){
  gate();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Episode response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Episode response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){gate();const part=await reader.read();gate();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Episode response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}

/** Explicit injected loopback transport. Never a runtime/native default. */
export function createNextDecisionHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):NextDecisionReviewStore{
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit next loopback transport required");
  const baseline=JSON.stringify([config,loop]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const gate=()=>{assertNextReviewOnly();if(JSON.stringify([config,loop])!==baseline)throw new Error("Next review drift");};gate();
  const run=(action:keyof typeof config.routes,ref:string|null,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const currentGate=()=>{scope.gate();gate();};currentGate();if(ref!==null)nextRef(ref);
    const encoded=ref===null?undefined:JSON.stringify({version:config.version,next_ref:ref});
    const load=scope.load,transport=scope.fetch(fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");currentGate();const route=config.routes[action];
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(encoded?{"Content-Type":"application/json"}:{})},body:encoded,signal,credentials:"omit",cache:"no-store",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Next response unavailable");
      const text=await boundedText(response,signal,currentGate);currentGate();const value=parseNextDecisionView(JSON.parse(text));
      if(ref!==null && value.context?.next_ref!==ref)throw new Error("Next correlation changed");return value;
    }));
  };
  return {read:o=>run("read",null,o),recover:(r,o)=>run("recover",r,o),submit:(r,o)=>run("submit",r,o),resume:(r,o)=>run("resume",r,o)};
}
