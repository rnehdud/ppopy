import {checkedLoopTestTransportBase} from "./mirayLoopTestTransport";
import config from "../../skin_engine/config/miray_closed_loop_frequency_test.json";
import projection from "../../skin_engine/config/miray_closed_loop_frequency_review.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {parseFrequencyCorrectionView,parseFrequencyCorrectionAck,validateFrequencyCorrectionRequest,
  type FrequencyCorrectionView,type FrequencyCorrectionRequest,type FrequencyCorrectionReviewStore} from "./mirayClosedLoopFrequency";

export type TestFrequencyEnvelope={version:string;context:{target_ref:string;mode:"episode";portfolio_revision:number};
  view:FrequencyCorrectionView;saved_correction_ref:string|null;evaluation_scope:"aws_test_candidate_not_applied";execution_attested:false};
export interface TestFrequencyPort {
  read(options?:MemberStatusReadOptions):Promise<TestFrequencyEnvelope>;
  confirm(request:FrequencyCorrectionRequest,options?:MemberStatusReadOptions):Promise<TestFrequencyEnvelope>;
  projection:FrequencyCorrectionReviewStore;
}
const object=(v:unknown):v is Record<string,unknown>=>!!v && typeof v==="object" && !Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const ref=(v:unknown):v is string=>typeof v==="string" && /^sha256:[0-9a-f]{64}$/.test(v);
function gate(){
  if(config.scope!=="aws_test_candidate_not_applied" || [config.runtime_enabled,config.runtime_registered,
    config.automatic_correction,config.automatic_retry,config.automatic_poll,config.correction_confirms_new_actual_use].some(v=>v!==false))throw new Error("Original TEST frequency review unavailable");
}
export function parseTestFrequencyEnvelope(value:unknown,request?:FrequencyCorrectionRequest):TestFrequencyEnvelope{
  gate();
  if(!object(value) || !exact(value,["version","context","view","saved_correction_ref","evaluation_scope","execution_attested"]) ||
    value.version!==config.version || value.evaluation_scope!==config.scope || value.execution_attested!==false ||
    !object(value.context) || !exact(value.context,["target_ref","mode","portfolio_revision"]) || value.context.mode!=="episode" ||
    !ref(value.context.target_ref) || !Number.isSafeInteger(value.context.portfolio_revision) || (value.context.portfolio_revision as number)<0 ||
    new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Exact original frequency envelope required");
  const view=parseFrequencyCorrectionView(value.view);
  if(view.portfolio_revision!==value.context.portfolio_revision)throw new Error("Original frequency revision differs");
  if(request){
    parseFrequencyCorrectionAck({version:projection.version,saved_correction_ref:value.saved_correction_ref,view},request);
  }else if(value.saved_correction_ref!==null)throw new Error("Read cannot claim a correction write");
  return structuredClone(value) as TestFrequencyEnvelope;
}
async function boundedText(response:Response,signal:AbortSignal|undefined,current:()=>void){
  current();const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw new Error("Frequency response too large");
  const reader=response.body?.getReader();if(!reader)throw new Error("Frequency response missing");
  const chunks:Uint8Array[]=[];let size=0;const abort=()=>{void reader.cancel().catch(()=>{});};
  signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){current();const part=await reader.read();current();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw new Error("Frequency response too large");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const part of chunks){bytes.set(part,offset);offset+=part.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}
/** Original TEST envelope with a pure legacy UI projection. No old crypto,
 * native factory, authority upgrade, listener, polling or automatic retry. */
export function createTestFrequencyPort({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):TestFrequencyPort{
  gate();const url=checkedLoopTestTransportBase(baseUrl,fetcher);
  const baseline=JSON.stringify([config,projection]);let known:TestFrequencyEnvelope|null=null,decision:string|undefined;
  const attempts=new Map<string,string>();
  const changed=()=>{known=null;attempts.clear();onMemberChanged();};
  const bound=createBoundMemberResponseSessionLoader(loadToken,changed);
  const run=(request:FrequencyCorrectionRequest|undefined,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options),current=()=>{scope.gate();gate();if(JSON.stringify([config,projection])!==baseline)throw new Error("Frequency contract changed");};current();
    let body:string|undefined,frozen:FrequencyCorrectionRequest|undefined;
    if(request){
      frozen=validateFrequencyCorrectionRequest(request);
      if(!known || frozen.decision_ref!==known.view.decision_ref)throw new Error("Read original frequency before confirming");
      const prior=attempts.get(frozen.request_id);
      if(prior){
        if(JSON.stringify(JSON.parse(prior).request)!==JSON.stringify(frozen))throw new Error("Original correction request cannot change");body=prior;
      }else{
        if(known.view.followup_completed || frozen.expected_portfolio_revision!==known.view.portfolio_revision ||
          !known.view.conflicts.some(c=>c.actual_action_ref===frozen!.actual_action_ref && c.correctable))throw new Error("Current unresolved frequency conflict required");
        if(attempts.size>=projection.max_metadata_rows)throw new Error("Frequency request limit reached");
        body=JSON.stringify({version:config.version,target_ref:known.context.target_ref,request:frozen});attempts.set(frozen.request_id,body);
      }
    }
    if(body && new TextEncoder().encode(body).length>config.max_request_bytes)throw new Error("Frequency request too large");
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      const token=await scope.load();if(!token)throw new Error("Member session required");current();const route=config.routes[request?"confirm":"read"];
      const response=await scope.fetch(fetcher)(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,...(body?{"Content-Type":"application/json"}:{})},body,
        signal:options?.signal,credentials:"omit",cache:"no-store",redirect:"error"});current();
      if(response.status!==200 || response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" ||
        !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw new Error("Frequency response unavailable");
      const text=await boundedText(response,options?.signal,current);current();const result=parseTestFrequencyEnvelope(JSON.parse(text),frozen);
      if(decision!==undefined && result.view.decision_ref!==decision)throw new Error("Original frequency decision changed");
      decision=result.view.decision_ref;known=result;return result;
    }));
  };
  return {read:o=>run(undefined,o),confirm:(r,o)=>run(r,o),
    projection:{read:async o=>(await run(undefined,o)).view,
      confirm:async(r,o)=>{const result=await run(r,o);return parseFrequencyCorrectionAck({version:projection.version,
        saved_correction_ref:result.saved_correction_ref,view:result.view},r);}}};
}
