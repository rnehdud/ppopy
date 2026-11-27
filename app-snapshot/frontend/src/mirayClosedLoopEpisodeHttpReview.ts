import config from "../../skin_engine/config/miray_closed_loop_episode_http_review.json";
import ui from "../../skin_engine/config/miray_closed_loop_ui.json";
import transitions from "../../skin_engine/config/miray_closed_loop_transitions.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {loopTime,parseClosedLoopEpisode,type ClosedLoopReviewStore} from "./mirayClosedLoop";
import {parseProductChangeView,parseProductChangeAck} from "./mirayClosedLoopTransitions";
import {validateMiraySkinState,type MiraySkinState} from "./miraySkinState";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

async function boundedText(response:Response,signal:AbortSignal|undefined,check:()=>void){
  check();
  const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Episode response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Episode response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){check();const part=await reader.read();check();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Episode response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}
type Action=keyof typeof config.routes;
function request(action:Action,value:unknown){
  if(!value || typeof value!=="object" || Array.isArray(value))throw new Error("Explicit episode request required");
  const v=structuredClone(value) as Record<string,unknown>;
  const fields={actual:["recommendation_id","frequency","effective_from"],followup:["observation","expected_portfolio_revision","other_changes"],change:["expected_portfolio_revision","action_type","before_product_id","after_product_id","frequency","effective_from"]};
  if(action!=="actual" && action!=="followup" && action!=="change")throw new Error("Explicit confirmation required");
  if(Object.keys(v).sort().join("|")!==[...fields[action],"version","decision_ref","request_id"].sort().join("|"))throw new Error("Unexpected episode fields");
  const ref=(s:unknown)=>typeof s==="string" && /^sha256:[0-9a-f]{64}$/.test(s);
  if(v.version!==(action==="change"?transitions.version:ui.version) || !ref(v.decision_ref) || typeof v.request_id!=="string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(v.request_id))throw new Error("Reviewed episode correlation required");
  if(action==="actual"){
    if(!ref(v.recommendation_id) || ![...ui.frequency_values,...ui.unconfirmed_values].includes(v.frequency as string))throw new Error("Explicit current use required");
    if(ui.unconfirmed_values.includes(v.frequency as string)){if(v.effective_from!==null)throw new Error("Unconfirmed use has no time");}else loopTime(v.effective_from);
  }else{
    if(!Number.isSafeInteger(v.expected_portfolio_revision) || (v.expected_portfolio_revision as number)<0)throw new Error("Current portfolio revision required");
    if(action==="followup"){
      validateMiraySkinState(v.observation as MiraySkinState);const observation=v.observation as MiraySkinState;
      if(observation.kind!=="checkin" || observation.concern_presence==="not_asked" || observation.discomfort_presence==="not_asked" || v.other_changes!=="not_asked")throw new Error("Two independent answered questions required");
    }else{
      if(!transitions.supported_actions.includes(v.action_type as string))throw new Error("Explicit supported product change required");loopTime(v.effective_from);
      for(const key of ["before_product_id","after_product_id"])if(v[key]!==null && (typeof v[key]!=="string" || !(v[key] as string).trim() || (v[key] as string).length>300))throw new Error("Bounded product required");
      if(v.action_type==="product_removed"?v.frequency!==null:!ui.frequency_values.includes(v.frequency as string) || v.frequency==="0")throw new Error("Explicit active use required");
    }
  }
  return v;
}

/** Injected loopback transport only; never supplied to the native/runtime app. */
export function createAccountEpisodeHttpReviewStore({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):ClosedLoopReviewStore{
  const url=new URL(baseUrl);
  if(url.protocol!=="http:" || url.hostname!=="127.0.0.1" || !url.port || url.pathname!=="/" || url.username || url.password || url.search || url.hash || typeof fetcher!=="function")throw new Error("Explicit local episode transport required");
  const baseline=JSON.stringify([config,ui,transitions,loop]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const gate=()=>{
    if(JSON.stringify([config,ui,transitions,loop])!==baseline || config.enabled!==false || config.registered!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false || ui.enabled!==false || transitions.enabled!==false || transitions.deployment_context!=="synthetic_test" || transitions.automatic_change_question!==false || transitions.purchase_click_confirms_actual_use!==false || transitions.portfolio_edit_confirms_actual_use!==false || Object.values(loop.flags).some(Boolean))throw new Error("Unapproved episode review");
  };gate();
  const run=(action:Action,body:unknown,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),signal=options?.signal;
    const check=()=>{scope.gate();gate();};
    check();const prepared=body===null?null:request(action,body),encoded=prepared===null?undefined:JSON.stringify(prepared);
    if(encoded && new TextEncoder().encode(encoded).length>config.max_request_bytes)throw new Error("Episode request too large");
    return scope.wait(()=>runWithMemberResponseSession(scope.load,onMemberChanged,async()=>{
      const token=await scope.wait(scope.load);if(!token)throw new Error("Member session required");check();const route=config.routes[action];
      const response=await scope.wait(()=>scope.fetch(fetcher)(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(encoded?{"Content-Type":"application/json"}:{})},body:encoded,signal,credentials:"omit",cache:"no-store",redirect:"error"}));
      check();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" || !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Episode response unavailable");
      const text=await scope.wait(()=>boundedText(response,signal,check));check();const value=JSON.parse(text);
      if(action==="changes")return parseProductChangeView(value);
      if(action==="change"){const ack=parseProductChangeAck(value);if(ack.view.decision_ref!==prepared?.decision_ref)throw new Error("Episode correlation changed");return ack;}
      const episode=parseClosedLoopEpisode(value);if(prepared && episode.decision_ref!==prepared.decision_ref)throw new Error("Episode correlation changed");return episode;
    }));
  };
  return {
    read:options=>run("read",null,options),
    confirmActual:(value,options)=>run("actual",value,options),
    saveFollowup:(value,options)=>run("followup",value,options),
    productChanges:{read:options=>run("changes",null,options),confirm:(value,options)=>run("change",value,options)},
  };
}
