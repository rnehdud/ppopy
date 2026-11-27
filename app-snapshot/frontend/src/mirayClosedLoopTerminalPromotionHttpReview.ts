import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_terminal_promotion_review.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {nextRef} from "./mirayClosedLoopNext";
import {assertTerminalPromotionReviewOnly,parseTerminalPromotionView,type TerminalPromotionContext,type TerminalPromotionReviewStore} from "./mirayClosedLoopTerminalPromotionReview";

async function boundedBody(response:Response,signal:AbortSignal|undefined,gate:()=>void){
  gate();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Promotion response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Promotion response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){gate();const part=await reader.read();gate();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Promotion response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(bytes));
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}

/** Explicit loopback review only. Read, snapshot promotion and final dispatch
 * are separate calls. No UI mount, automatic calculation, retry or polling.
 */
export function createTerminalPromotionHttpReviewStore(options:{baseUrl:string;terminalNextRef:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):TerminalPromotionReviewStore{
  const url=new URL(options.baseUrl);nextRef(options.terminalNextRef);assertTerminalPromotionReviewOnly();
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof options.fetcher!=="function")throw new Error("Explicit promotion loopback required");
  const terminalRef=options.terminalNextRef,bound=createBoundMemberResponseSessionLoader(options.loadToken,options.onMemberChanged);
  let context:TerminalPromotionContext|null=null;
  const run=(action:"read"|"promote"|"resume",requestOptions?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,requestOptions),signal=requestOptions?.signal;
    const currentGate=()=>{scope.gate();assertTerminalPromotionReviewOnly();};currentGate();
    if(action!=="read" && context===null)throw new Error("Read current promotion context first");
    const body=JSON.stringify({version:config.version,terminal_next_ref:terminalRef});
    if(new TextEncoder().encode(body).length>config.max_request_bytes)throw new Error("Promotion request too large");
    const load=scope.load,transport=scope.fetch(options.fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,options.onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");currentGate();
      const route=config.routes[action];
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,"Content-Type":"application/json"},body,signal,cache:"no-store",credentials:"omit",redirect:"error"});
      currentGate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(s=>s.trim()).includes("no-store"))throw new Error("Promotion input response unavailable");
      const payload=await boundedBody(response,signal,currentGate);currentGate();
      const view=parseTerminalPromotionView(payload,terminalRef);
      if(context && (Object.keys(context) as (keyof TerminalPromotionContext)[]).some(k=>context![k]!==view.context[k]))throw new Error("Promotion parent changed");
      context=structuredClone(view.context);return view;
    }));
  };
  return {read:o=>run("read",o),promote:o=>run("promote",o),resume:o=>run("resume",o)};
}
