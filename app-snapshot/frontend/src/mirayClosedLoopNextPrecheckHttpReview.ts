import {memberStatusReadScope} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_next_precheck_review.json";
import {createNextIntakeHttpReviewStore} from "./mirayClosedLoopIntakeHttpReview";
import {assertNextPrecheckReviewOnly,parseNextPrecheckView} from "./mirayClosedLoopNextPrecheck";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import type {NextIntakeReviewStore} from "./mirayClosedLoopIntake";

/** Explicit synthetic loopback channel only, never a runtime/native default. */
export function createNextPrecheckHttpReviewStore(options:Parameters<typeof createNextIntakeHttpReviewStore>[0]):NextIntakeReviewStore{
  assertNextPrecheckReviewOnly();
  const bound=createBoundMemberResponseSessionLoader(options.loadToken,options.onMemberChanged);
  const intake=createNextIntakeHttpReviewStore({...options,loadToken:bound});
  const url=new URL(options.baseUrl);
  return {...intake,precheck:o=>{
    const scope=memberStatusReadScope(bound,o),transport=scope.fetch(options.fetcher);
    const gate=()=>{scope.gate();assertNextPrecheckReviewOnly();};gate();
    const load=scope.load;
    return scope.wait(()=>runWithMemberResponseSession(load,options.onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");
      gate();
      const response=await transport(url.origin+config.route.path,{method:config.route.method,headers:{Authorization:`Bearer ${token}`},signal:o?.signal,credentials:"omit",cache:"no-store",redirect:"error"});
      gate();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(s=>s.trim()).includes("no-store"))throw new Error("Precheck response unavailable");
      const declared=response.headers.get("content-length");
      if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Precheck response too large");
      const reader=response.body?.getReader();if(!reader)throw new Error("Precheck response missing");
      const chunks:Uint8Array[]=[];let size=0;
      const abort=()=>{void reader.cancel().catch(()=>{});};o?.signal?.addEventListener("abort",abort,{once:true});
      try{
        while(true){gate();const part=await reader.read();gate();if(part.done)break;
          size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Precheck response too large");chunks.push(part.value);}
        const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
        gate();return parseNextPrecheckView(JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(bytes)));
      }catch(error){await reader.cancel().catch(()=>{});throw error;}
      finally{o?.signal?.removeEventListener("abort",abort);reader.releaseLock();}
    }));
  }};
}
