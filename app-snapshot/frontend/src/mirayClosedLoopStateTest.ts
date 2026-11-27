import {checkedLoopTestTransportBase} from "./mirayLoopTestTransport";
import config from "../../skin_engine/config/miray_closed_loop_state_http_test.json";
import ui from "../../skin_engine/config/miray_closed_loop_ui.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {loopTestFailure,loopTestFailureAt} from "./loopTestFailureCode";
import {loopTime,parseClosedLoopEpisode,type ClosedLoopEpisode,type ClosedLoopReviewStore,type ConfirmActualRequest,type SaveFollowupRequest} from "./mirayClosedLoop";
import {validateMiraySkinState,type MiraySkinState} from "./miraySkinState";

import {parseTestLoopWorkerView,type TestLoopWorkerView} from "./mirayClosedLoopWorkerTest";

export type TestLoopStateView={version:string;context:{target_ref:string;mode:"registration"|"episode";portfolio_revision:number};
  snapshot:null|{snapshot_ref:string;observation:MiraySkinState};episode:ClosedLoopEpisode|null;worker_view?:TestLoopWorkerView|null;
  unregistered_products?:{decision_ref:string;decision_at:string;confirmation_modes?:["newly_started","current_use"];products:{id:string;name:string;frequency:string}[];confirmations:{ref:string;product_id:string;frequency:string;effective_from:string;action_type?:"product_added"|"current_use_confirmed"}[]}|null;
  evaluation_scope:"aws_test_candidate_not_applied";execution_attested:false};
export type TestLoopRegistrationRequest={request_id:string;expected_portfolio_revision:number;observation:MiraySkinState};
export type TestLoopAddedProductRequest={version:string;decision_ref:string;request_id:string;product_id:string;frequency:string;expected_portfolio_revision:number}&({action_type:"product_added";effective_from:string}|{action_type:"current_use_confirmed";effective_from:null});
export interface TestLoopStatePort{
  read(options?:MemberStatusReadOptions):Promise<TestLoopStateView>;
  readEntry?(options?:MemberStatusReadOptions):Promise<TestLoopStateView>;
  register(request:TestLoopRegistrationRequest,options?:MemberStatusReadOptions):Promise<TestLoopStateView>;
  confirmAddedProduct?(request:TestLoopAddedProductRequest,options?:MemberStatusReadOptions):Promise<TestLoopStateView>;
  episode:ClosedLoopReviewStore;
}
const object=(v:unknown):v is Record<string,unknown>=>!!v && typeof v==="object" && !Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const ref=(v:unknown):v is string=>typeof v==="string" && /^sha256:[0-9a-f]{64}$/.test(v);
const revision=(v:unknown)=>Number.isSafeInteger(v) && (v as number)>=0;
const uuid=(v:unknown)=>typeof v==="string" && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(v);
function gate(){
  if(config.scope!=="aws_test_candidate_not_applied" || [config.runtime_enabled,config.runtime_registered,config.automatic_retry,
    config.automatic_poll,config.registration_confirms_actual_use,config.portfolio_edit_confirms_actual_use].some(v=>v!==false))throw new Error("Original TEST state review unavailable");
}
export function parseTestLoopStateView(value:unknown):TestLoopStateView{
  gate();
  if(!object(value) || !exact(value,["version","context","snapshot","episode","evaluation_scope","execution_attested",...(Object.hasOwn(value,"worker_view")?["worker_view"]:[]),...(Object.hasOwn(value,"unregistered_products")?["unregistered_products"]:[])]) ||
    value.version!==config.version || value.evaluation_scope!==config.scope || value.execution_attested!==false ||
    !object(value.context) || !exact(value.context,["target_ref","mode","portfolio_revision"]) ||
    !ref(value.context.target_ref) || !revision(value.context.portfolio_revision) || !["registration","episode"].includes(String(value.context.mode)))throw new Error("Exact original state target required");
  if(value.snapshot!==null){
    if(!object(value.snapshot) || !exact(value.snapshot,["snapshot_ref","observation"]) || !ref(value.snapshot.snapshot_ref))throw new Error("Exact original snapshot required");
    validateMiraySkinState(value.snapshot.observation as MiraySkinState);
  }
  if(value.context.mode==="episode"){
    if(value.snapshot===null)throw new Error("Original episode snapshot required");
    const episode=parseClosedLoopEpisode(value.episode);
    if(episode.portfolio_revision!==value.context.portfolio_revision ||
      (episode.followup && (episode.followup.snapshot_ref!==value.snapshot.snapshot_ref || episode.followup.observed_at!==(value.snapshot.observation as MiraySkinState).observed_at)))throw new Error("Original episode/state correlation required");
  }else if(value.episode!==null)throw new Error("Registration cannot confirm actual use");
  if(Object.hasOwn(value,"unregistered_products") && value.unregistered_products!==null){
    const p=value.unregistered_products,e=value.episode as ClosedLoopEpisode|null;
    if(!object(p) || !exact(p,["decision_ref","decision_at","products","confirmations",...(Object.hasOwn(p,"confirmation_modes")?["confirmation_modes"]:[])]) || !e || p.decision_ref!==e.decision_ref || p.decision_at!==e.decision_at || !Array.isArray(p.products) || !Array.isArray(p.confirmations))throw new Error("Exact product continuity context required");
    const currentUse=Object.hasOwn(p,"confirmation_modes");
    if(currentUse && JSON.stringify(p.confirmation_modes)!==JSON.stringify(config.product_confirmation_modes))throw new Error("Exact current-use capability required");
    const seen=new Set<string>();
    for(const product of p.products){
      if(!object(product) || !exact(product,["id","name","frequency"]) || typeof product.id!=="string" || !product.id.length || product.id.length>300 || seen.has(product.id) || typeof product.name!=="string" || !product.name.length || product.name.length>300 || ![...ui.frequency_values,...ui.unconfirmed_values].includes(product.frequency as string))throw new Error("Exact current product required");
      seen.add(product.id);
    }
    const confirmed=new Set<string>(),actions=new Set<string>();
    for(const raw of p.confirmations){
      if(!object(raw) || !exact(raw,["ref","product_id","frequency","effective_from",...(currentUse?["action_type"]:[])]) || (currentUse && !["product_added","current_use_confirmed"].includes(String(raw.action_type))) || !ref(raw.ref) || actions.has(raw.ref) || typeof raw.product_id!=="string" || !raw.product_id.length || raw.product_id.length>300 || confirmed.has(raw.product_id) || seen.has(raw.product_id) || !["1","2","3","4","5","6","7"].includes(raw.frequency as string))throw new Error("Exact pending addition confirmation required");
      loopTime(raw.effective_from);if(Date.parse(raw.effective_from)<Date.parse(e.decision_at))throw new Error("Pending addition belongs to its decision");
      confirmed.add(raw.product_id);actions.add(raw.ref);
    }
  }
  if(Object.hasOwn(value,"worker_view")){
    if(value.snapshot===null){if(value.worker_view!==null)throw new Error("Unregistered state has no worker target");}
    else {
      const worker=parseTestLoopWorkerView(value.worker_view);
      if(worker.context.snapshot_ref!==value.snapshot.snapshot_ref || worker.context.portfolio_revision!==value.context.portfolio_revision ||
        (worker.context.mode==="next" && worker.context.previous_decision_ref!==(value.episode as ClosedLoopEpisode|null)?.decision_ref))throw new Error("Combined original entry correlation required");
    }
  }
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw loopTestFailure("S","B");
  return structuredClone(value) as TestLoopStateView;
}
async function boundedText(response:Response,signal:AbortSignal|undefined,current:()=>void){
  current();const declared=response.headers.get("content-length");
  if(declared!==null && (!/^\d+$/.test(declared) || Number(declared)>config.max_response_bytes))throw loopTestFailure("S","B");
  const reader=response.body?.getReader();if(!reader)throw new Error("State response missing");
  const chunks:Uint8Array[]=[];let size=0;
  const abort=()=>{void reader.cancel().catch(()=>{});};signal?.addEventListener("abort",abort,{once:true});
  try{
    while(true){current();const part=await reader.read();current();if(part.done)break;
      size+=part.value.byteLength;if(size>config.max_response_bytes)throw loopTestFailure("S","B");chunks.push(part.value);}
    const bytes=new Uint8Array(size);let offset=0;for(const part of chunks){bytes.set(part,offset);offset+=part.byteLength;}
    return new TextDecoder("utf-8",{fatal:true}).decode(bytes);
  }catch(error){await reader.cancel().catch(()=>{});throw error;}
  finally{signal?.removeEventListener("abort",abort);reader.releaseLock();}
}
type Action=keyof typeof config.routes;
function request(action:Action,value:unknown,known:TestLoopStateView){
  if(!object(value) || !uuid(value.request_id))throw new Error("Explicit original input required");
  const v=structuredClone(value);
  if(action==="actual" && Object.hasOwn(v,"action_type")){
    const p=known.unregistered_products?.products.find(p=>p.id===v.product_id);
    if(!exact(v,["version","decision_ref","request_id","action_type","product_id","frequency","effective_from","expected_portfolio_revision"]) || v.version!==ui.version || !["product_added","current_use_confirmed"].includes(String(v.action_type)) || known.context.mode!=="episode" || v.decision_ref!==known.episode?.decision_ref || v.expected_portfolio_revision!==known.context.portfolio_revision || !revision(v.expected_portfolio_revision) || !p || p.frequency!==v.frequency || !["1","2","3","4","5","6","7"].includes(v.frequency as string))throw new Error("Explicit current added-product use required");
    if(v.action_type==="current_use_confirmed"){
      if(!known.unregistered_products?.confirmation_modes?.includes("current_use") || v.effective_from!==null)throw new Error("Current-use confirmation has no historical start");
    }else loopTime(v.effective_from);
    return v;
  }
  if(action==="registration"){
    if(!exact(v,["request_id","expected_portfolio_revision","observation"]) || known.context.mode!=="registration")throw new Error("Explicit registration input required");
  }else{
    const fields=action==="actual"?["recommendation_id","frequency","effective_from"]:["observation","expected_portfolio_revision","other_changes"];
    if(!exact(v,["version","decision_ref","request_id",...fields]) || v.version!==ui.version || known.context.mode!=="episode" || v.decision_ref!==known.episode?.decision_ref)throw new Error("Read exact current episode before confirming");
  }
  if(action==="actual"){
    if(!ref(v.recommendation_id) || ![...ui.frequency_values,...ui.unconfirmed_values].includes(v.frequency as string))throw new Error("Explicit use response required");
    if(ui.unconfirmed_values.includes(v.frequency as string)){if(v.effective_from!==null)throw new Error("Unknown use has no invented action time");}else loopTime(v.effective_from);
  }else{
    if(!revision(v.expected_portfolio_revision) || v.expected_portfolio_revision!==known.context.portfolio_revision)throw new Error("Original portfolio revision required");
    validateMiraySkinState(v.observation as MiraySkinState);const o=v.observation as MiraySkinState;
    if(o.kind!==(action==="registration"?"baseline":"checkin") || o.concern_presence==="not_asked" || o.discomfort_presence==="not_asked" ||
      (action==="followup" && v.other_changes!==ui.other_changes_default))throw new Error("Two independent explicit answers required");
  }
  return v;
}

/** Injected loopback or branded native TEST transport. The existing episode UI may consume the same DTO;
 * this does not install a native/AppAuth factory or expose real questions. */
export function createTestLoopStatePort({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):TestLoopStatePort{
  gate();const url=checkedLoopTestTransportBase(baseUrl,fetcher);
  const baseline=JSON.stringify([config,ui]),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);let known:TestLoopStateView|null=null;
  const run=(action:Action,value:unknown,options?:MemberStatusReadOptions,entry=false)=>{
    const scope=memberStatusReadScope(bound,options),current=()=>{scope.gate();gate();if(JSON.stringify([config,ui])!==baseline)throw new Error("State contract changed");};current();
    if(action!=="read" && known===null)throw new Error("Read original state before writing");
    const target=action==="read"?null:known!.context.target_ref;
    // Never retain a mutable form across credential/network awaits.
    const body=action==="read"?undefined:JSON.stringify({version:config.version,target_ref:target,request:request(action,value,known!)});
    if(body && new TextEncoder().encode(body).length>config.max_request_bytes)throw new Error("State input too large");
    return scope.wait(()=>runWithMemberResponseSession(scope.load,onMemberChanged,async()=>{
      const token=await scope.load();if(!token)throw new Error("Member session required");current();const route=config.routes[action];
      const response=await scope.fetch(fetcher)(url.origin+route.path,{method:route.method,headers:{Authorization:`Bearer ${token}`,Accept:entry?"application/vnd.poppy.loop-entry+json; products=2":"application/vnd.poppy.loop-products-v2+json",...(body?{"Content-Type":"application/json"}:{})},body,
        signal:options?.signal,credentials:"omit",cache:"no-store",redirect:"error"});current();
      if(response.status!==200)throw loopTestFailure("S","H",response.status);
      if(response.redirected || response.headers.get("content-type")?.split(";")[0]!=="application/json" ||
        !response.headers.get("cache-control")?.split(",").map(v=>v.trim()).includes("no-store"))throw loopTestFailure("S","M");
      const text=await boundedText(response,options?.signal,current);current();
      let result:TestLoopStateView;
      try{result=parseTestLoopStateView(JSON.parse(text));}catch{throw loopTestFailure("S","J");}
      if(target!==null && result.context.target_ref!==target)throw new Error("Original selected state changed");
      known=result;return result;
    })).catch(error=>{throw loopTestFailureAt(error,"S");});
  };
  const episode=(v:TestLoopStateView)=>{if(!v.episode)throw new Error("Original episode unavailable");return v.episode;};
  return {read:o=>run("read",null,o),readEntry:o=>run("read",null,o,true),register:(r,o)=>run("registration",r,o),confirmAddedProduct:(r,o)=>run("actual",r,o),
    episode:{read:async o=>episode(await run("read",null,o)),
      confirmActual:async(r:ConfirmActualRequest,o)=>episode(await run("actual",r,o)),
      saveFollowup:async(r:SaveFollowupRequest,o)=>episode(await run("followup",r,o))}};
}
