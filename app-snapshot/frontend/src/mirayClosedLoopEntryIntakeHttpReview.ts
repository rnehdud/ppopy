import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_entry_intake_http_review.json";
import storage from "../../skin_engine/config/miray_closed_loop_entry_intake_review.json";
import sharedQuestions from "../../skin_engine/config/miray_closed_loop_intake_ui_review.json";
import sharedAnswers from "../../skin_engine/config/miray_closed_loop_intake_review.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {assertEntryIntakeReviewOnly,parseEntryIntakeView,type EntryIntakeReviewStore} from "./mirayClosedLoopEntryIntake";
import {nextIntakeRef,parseIntakeAnswers} from "./mirayClosedLoopIntake";

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

/** Explicit injected loopback only; no default fetch, native/runtime or storage. */
export function createEntryIntakeHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):EntryIntakeReviewStore{
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit input loopback required");
  const baseline=JSON.stringify([config,storage,sharedQuestions,sharedAnswers]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const gate=()=>{assertEntryIntakeReviewOnly();if(JSON.stringify([config,storage,sharedQuestions,sharedAnswers])!==baseline)throw new Error("Entry input review drift");};gate();
  const run=(action:"read"|"fresh"|"save",ref:string|null,answers:unknown,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const currentGate=()=>{scope.gate();gate();};currentGate();if(ref!==null)nextIntakeRef(ref);
    const encoded=action==="read"?undefined:JSON.stringify(action==="fresh"?{entry_ref:ref}:{version:config.version,entry_ref:ref,answers:parseIntakeAnswers(answers)});
    if(encoded && new TextEncoder().encode(encoded).length>config.max_request_bytes)throw new Error("Input request too large");
    const load=scope.load,transport=scope.fetch(fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");currentGate();
      const route=config.routes[action],response=await transport(url.origin+route.path,{method:route.method,
        headers:{Authorization:`Bearer ${token}`,...(encoded?{"Content-Type":"application/json"}:{})},body:encoded,signal,credentials:"omit",cache:"no-store",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Input response unavailable");
      const text=await boundedText(response,signal,currentGate);currentGate();const value=parseEntryIntakeView(JSON.parse(text));
      if(action==="save" && value.context.entry_ref!==ref)throw new Error("Input correlation changed");
      if(action==="fresh" && (value.context.mode!=="fresh" || value.context.entry_ref===ref))throw new Error("Fresh input target unconfirmed");
      if(action==="read" && value.context.mode!=="initial")throw new Error("Initial input target unconfirmed");
      return value;
    }));
  };
  return {read:o=>run("read",null,null,o),readFresh:(r,o)=>run("fresh",r,null,o),save:(r,a,o)=>run("save",r,a,o)};
}
