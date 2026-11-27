import {checkedPublicAppTransportBase} from "./publicAppTransport";
import config from "../../skin_engine/config/app_public_loop_worker_http_review.json";
import workerDomain from "../../skin_engine/config/app_public_loop_worker_review.json";
import consumer from "../../skin_engine/config/consumer_api.json";
import type {CareAnalysisEnvelope,RoutineObservation} from "./careApi";
import {isConsumerCareDelivery} from "./careDeliveryBoundary";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {publicLoopFailure,publicLoopFailureAt} from "./publicLoopFailure";
import {parseIntakeAnswers,type IntakeAnswers} from "./mirayClosedLoopIntake";

export type PublicLoopWorkerContext={target_ref:string;mode:"initial"|"next"|"original";snapshot_ref:string;previous_decision_ref:string|null;portfolio_revision:number};
export type PublicLoopWorkerView={version:string;context:PublicLoopWorkerContext;
  status:"not_started"|"pending"|"completed"|"terminal_without_result"|"not_dispatched"|"deferred";
  quota_status:null|"reserved"|"completed"|"failed"|"cancelled"|"cached";
  result:null|{decision_ref:string;response:CareAnalysisEnvelope};reason:string|null;
  evaluation_scope:"public_service_loop_worker_not_TEST_or_research";execution_attested:false};
export interface PublicLoopWorkerPort {
  resume?(targetRef:string,options?:MemberStatusReadOptions):Promise<PublicLoopWorkerView>;
  read(options?:MemberStatusReadOptions):Promise<PublicLoopWorkerView>;
  submit(targetRef:string,answers:IntakeAnswers,observation:RoutineObservation|null,options?:MemberStatusReadOptions):Promise<PublicLoopWorkerView>;
}
const object=(v:unknown):v is Record<string,unknown>=>!!v && typeof v==="object" && !Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const ref=(v:unknown):v is string=>typeof v==="string" && /^sha256:[0-9a-f]{64}$/.test(v);
function gate(){
  if(config.version!=="1.0.0-public-loop-worker-http-20261020" || config.scope!=="public_service_loop_worker_http_not_TEST_or_research" ||
    config.purpose!=="poppy_public_loop_worker_http" || config.automatic_retry!==false || config.automatic_poll!==false)throw new Error("Public worker contract unavailable");
  if(config.registration_confirms_actual_use!==false || workerDomain.scope!=="public_service_loop_worker_not_TEST_or_research" || workerDomain.version!=="1.0.0-public-loop-worker-20261020" || workerDomain.legacy_input_schema_versions.length!==0)throw new Error("Explicit public use confirmation required");
}
export function parsePublicLoopWorkerView(value:unknown):PublicLoopWorkerView{
  gate();
  if(!object(value) || !exact(value,["version","context","status","quota_status","result","reason","evaluation_scope","execution_attested"]) ||
    value.version!==config.version || value.evaluation_scope!==workerDomain.scope || value.execution_attested!==false ||
    !object(value.context) || !exact(value.context,["target_ref","mode","snapshot_ref","previous_decision_ref","portfolio_revision"]))throw new Error("Original public worker response required");
  const c=value.context;
  if(!ref(c.target_ref) || !ref(c.snapshot_ref) || (c.previous_decision_ref!==null && !ref(c.previous_decision_ref)) ||
    !["initial","next","original"].includes(String(c.mode)) || !Number.isSafeInteger(c.portfolio_revision) ||
    (c.portfolio_revision as number)<0 || (c.mode==="initial" && c.previous_decision_ref!==null) ||
    (c.mode==="next" && c.previous_decision_ref===null))throw new Error("Original worker target required");
  const statuses:Record<string,unknown[]>={not_started:[null],pending:["reserved"],completed:["completed"],
    terminal_without_result:["failed","cancelled","cached"],not_dispatched:[null],deferred:[null]};
  if(typeof value.status!=="string" || !Object.hasOwn(statuses,value.status) || !statuses[value.status].includes(value.quota_status))throw new Error("Original quota status required");
  const reasoned=value.status==="deferred" || value.status==="not_dispatched";
  if(reasoned?typeof value.reason!=="string" || !value.reason || value.reason.length>128:value.reason!==null)throw new Error("Original worker reason required");
  if(value.status==="completed"){
    const r=value.result;
    if(!object(r) || !exact(r,["decision_ref","response"]) || !ref(r.decision_ref) || !object(r.response) ||
      !exact(r.response,["api_schema_version","deployment_context","persistence","result"]) ||
      r.response.deployment_context!=="real_user" || r.response.persistence!=="none" || r.response.api_schema_version!==consumer.request_schema_version ||
      !isConsumerCareDelivery(r.response.result))throw new Error("Complete original engine result required");
  }else if(value.result!==null)throw new Error("Unconfirmed worker result withheld");
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw publicLoopFailure("W","B");
  return structuredClone(value) as PublicLoopWorkerView;
}

async function boundedText(response:Response,signal:AbortSignal|undefined,current:()=>void){
  current();const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw publicLoopFailure("W","B");
  const reader=response.body?.getReader();if(!reader)throw new Error("Worker response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){current();const part=await reader.read();current();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw publicLoopFailure("W","B");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const part of chunks){bytes.set(part,offset);offset+=part.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}

/** Injected local transport to the held server contract; no installed UI default. */
export function createPublicLoopWorkerPort({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):PublicLoopWorkerPort{
  gate();const url=checkedPublicAppTransportBase(baseUrl,fetcher);
  const baseline=JSON.stringify(config),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
  const run=(target:string|null,answers:IntakeAnswers|null,observation:RoutineObservation|null,options?:MemberStatusReadOptions,resume=false)=>{
    const scope=memberStatusReadScope(bound,options),current=()=>{scope.gate();gate();if(JSON.stringify(config)!==baseline)throw new Error("Worker contract changed");};current();
    if(target!==null && !ref(target))throw new Error("Original target correlation required");
    // Freeze the explicit form before any asynchronous credential or network work.
    const body=target===null?undefined:JSON.stringify(resume?{version:config.version,target_ref:target,resume:true}:{version:config.version,target_ref:target,answers:parseIntakeAnswers(answers),routine_observation:observation});
    if(body && new TextEncoder().encode(body).length>config.max_request_bytes)throw new Error("Worker input too large");
    const load=scope.load,transport=scope.fetch(fetcher);
    return scope.wait(()=>runWithMemberResponseSession(load,onMemberChanged,async()=>{
      const token=await load();if(!token)throw new Error("Member session required");current();
      const route=config.routes[target===null?"read":"submit"];
      const response=await transport(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(body?{"Content-Type":"application/json"}:{})},body,
        signal:options?.signal,credentials:"omit",cache:"no-store",redirect:"error"});current();
      if(response.status!==200)throw publicLoopFailure("W","H",response.status);
      if(response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" ||
        response.headers.get("cache-control")?.trim().toLowerCase()!=="no-store")throw publicLoopFailure("W","M");
      const text=await boundedText(response,options?.signal,current);current();
      let value:PublicLoopWorkerView;
      try{value=parsePublicLoopWorkerView(JSON.parse(text));}catch{throw publicLoopFailure("W","J");}
      if(target!==null && value.context.target_ref!==target)throw new Error("Original worker target changed");
      return value;
    })).catch(error=>{throw publicLoopFailureAt(error,"W");});
  };
  return {resume:(r,o)=>run(r,null,null,o,true),read:o=>run(null,null,null,o),submit:(r,a,s,o)=>run(r,a,s,o)};
}
