import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_intake_ui_review.json";
import answersConfig from "../../skin_engine/config/miray_closed_loop_intake_review.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {assertIntakeReviewOnly,nextIntakeRef,parseIntakeAnswers,parseIntakeView,type NextIntakeReviewStore} from "./mirayClosedLoopIntake";
async function boundedText(response:Response,signal:AbortSignal|undefined,gate:()=>void){
  gate();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Input response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Input response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){gate();const part=await reader.read();gate();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Input response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}


/** Explicit synthetic loopback only; never a native/runtime default. */
export function createNextIntakeHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):NextIntakeReviewStore {
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit input loopback required");
  const baseline=JSON.stringify([config,answersConfig]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const gate=()=>{assertIntakeReviewOnly();if(JSON.stringify([config,answersConfig])!==baseline)throw new Error("Input review drift");};gate();
  const run=(ref:string|null,answers:unknown,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const currentGate=()=>{scope.gate();gate();};currentGate();if(ref!==null)nextIntakeRef(ref);
    const body=ref===null?undefined:JSON.stringify({version:config.version,next_ref:ref,answers:parseIntakeAnswers(answers)});
    if(body && new TextEncoder().encode(body).length>config.max_request_bytes)throw new Error("Input request too large");
    const load=scope.load,transport=scope.fetch(fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");currentGate();
      const route=config.routes[ref===null?"read":"save"];
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(body?{"Content-Type":"application/json"}:{})},body,signal,credentials:"omit",cache:"no-store",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Input response unavailable");
      const text=await boundedText(response,signal,currentGate);currentGate();const value=parseIntakeView(JSON.parse(text));
      if(ref!==null && value.context.next_ref!==ref)throw new Error("Input correlation changed");return value;
    }));
  };
  return {read:o=>run(null,null,o),save:(r,a,o)=>run(r,a,o)};
}
