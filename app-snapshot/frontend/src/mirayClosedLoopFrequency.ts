import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_frequency_review.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import {loopTime} from "./mirayClosedLoop";

export type FrequencyConflict={actual_action_ref:string;product_id:string;product_name:string;declared_frequency:string;confirmed_frequency:string;effective_from:string;confirmed_at:string;correctable:boolean};
export type FrequencyCorrection={record_ref:string;actual_action_ref:string;before_revision:number;after_revision:number;collected_at:string};
export type FrequencyCorrectionView={version:string;decision_ref:string;portfolio_revision:number;followup_completed:boolean;conflicts:FrequencyConflict[];corrections:FrequencyCorrection[];evaluation_scope:string};
export type FrequencyCorrectionRequest={version:string;decision_ref:string;request_id:string;actual_action_ref:string;expected_portfolio_revision:number};
export type FrequencyCorrectionAck={version:string;saved_correction_ref:string;view:FrequencyCorrectionView};
/** Disabled explicit port only. No URL, listener, default store or retry. */
export interface FrequencyCorrectionReviewStore {read(options?:MemberStatusReadOptions):Promise<unknown>;confirm(request:FrequencyCorrectionRequest,options?:MemberStatusReadOptions):Promise<unknown>;}
function exact(value:unknown,keys:string[]):Record<string,unknown>{
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected correction fields");return value as Record<string,unknown>;
}
function ref(v:unknown):asserts v is string{if(typeof v!=="string" || !/^sha256:[0-9a-f]{64}$/.test(v))throw new Error("Exact correction correlation required");}
function revision(v:unknown):asserts v is number{if(!Number.isSafeInteger(v) || (v as number)<0 || (v as number)>config.max_revision)throw new Error("Exact bounded revision required");}
export function assertFrequencyCorrectionReviewOnly(){
  if(config.deployment_context!=="synthetic_test" || [config.enabled,config.registered,config.automatic_correction,config.automatic_question,config.automatic_retry,config.automatic_poll,config.correction_confirms_new_actual_use,...Object.values(loop.flags)].some(v=>v!==false))throw new Error("Frequency correction activation is not approved");
}
export function parseFrequencyCorrectionView(value:unknown):FrequencyCorrectionView{
  assertFrequencyCorrectionReviewOnly();if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Bounded correction view required");
  const v=exact(value,["version","decision_ref","portfolio_revision","followup_completed","conflicts","corrections","evaluation_scope"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || typeof v.followup_completed!=="boolean")throw new Error("Exact correction contract required");ref(v.decision_ref);revision(v.portfolio_revision);
  if(!Array.isArray(v.conflicts) || v.conflicts.length>loop.max_actual_actions || !Array.isArray(v.corrections) || v.corrections.length>loop.max_actual_actions)throw new Error("Bounded correction list required");
  const corrected=new Set<string>(),records=new Set<string>();
  for(const item of v.corrections){const c=exact(item,["record_ref","actual_action_ref","before_revision","after_revision","collected_at"]);ref(c.record_ref);ref(c.actual_action_ref);revision(c.before_revision);revision(c.after_revision);loopTime(c.collected_at);
    if(c.after_revision!==c.before_revision+1 || c.after_revision>(v.portfolio_revision as number) || corrected.has(c.actual_action_ref) || records.has(c.record_ref))throw new Error("Immutable correction revision differs");corrected.add(c.actual_action_ref);records.add(c.record_ref);}
  const actions=new Set<string>(),products=new Set<string>();
  for(const item of v.conflicts){const c=exact(item,["actual_action_ref","product_id","product_name","declared_frequency","confirmed_frequency","effective_from","confirmed_at","correctable"]);ref(c.actual_action_ref);loopTime(c.effective_from);loopTime(c.confirmed_at);
    if(typeof c.product_id!=="string" || !c.product_id.trim() || c.product_id.length>300 || typeof c.product_name!=="string" || !c.product_name.trim() || c.product_name.length>300 || !loop.frequency_values.includes(c.declared_frequency as string) || !config.frequency_values.includes(c.confirmed_frequency as string) || c.declared_frequency===c.confirmed_frequency || typeof c.correctable!=="boolean" || Date.parse(c.effective_from)>Date.parse(c.confirmed_at) || actions.has(c.actual_action_ref) || products.has(c.product_id) || (c.correctable && (v.followup_completed || corrected.has(c.actual_action_ref))))throw new Error("Known distinct frequency conflict required");actions.add(c.actual_action_ref);products.add(c.product_id);}
  return structuredClone(value) as FrequencyCorrectionView;
}
export function validateFrequencyCorrectionRequest(value:unknown):FrequencyCorrectionRequest{
  assertFrequencyCorrectionReviewOnly();const r=exact(value,["version","decision_ref","request_id","actual_action_ref","expected_portfolio_revision"]);ref(r.decision_ref);ref(r.actual_action_ref);revision(r.expected_portfolio_revision);
  if(r.version!==config.version || r.expected_portfolio_revision===config.max_revision || typeof r.request_id!=="string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(r.request_id) || new TextEncoder().encode(JSON.stringify(value)).length>config.max_request_bytes)throw new Error("Exact explicit correction request required");return structuredClone(value) as FrequencyCorrectionRequest;
}
export function frequencyCorrectionRequest(view:FrequencyCorrectionView,actualRef:string,requestId=crypto.randomUUID()):FrequencyCorrectionRequest{
  const v=parseFrequencyCorrectionView(view);if(v.followup_completed || !v.conflicts.some(c=>c.actual_action_ref===actualRef && c.correctable))throw new Error("Unresolved current correction required");
  return validateFrequencyCorrectionRequest({version:config.version,decision_ref:v.decision_ref,request_id:requestId,actual_action_ref:actualRef,expected_portfolio_revision:v.portfolio_revision});
}
export function parseFrequencyCorrectionAck(value:unknown,request?:FrequencyCorrectionRequest):FrequencyCorrectionAck{
  const a=exact(value,["version","saved_correction_ref","view"]);ref(a.saved_correction_ref);const view=parseFrequencyCorrectionView(a.view);
  const record=view.corrections.find(c=>c.record_ref===a.saved_correction_ref);
  if(a.version!==config.version || !record)throw new Error("Saved correction missing from ACK");
  if(request){const r=validateFrequencyCorrectionRequest(request);if(view.decision_ref!==r.decision_ref || record.actual_action_ref!==r.actual_action_ref || record.before_revision!==r.expected_portfolio_revision || record.after_revision!==r.expected_portfolio_revision+1)throw new Error("Saved correction target differs");}
  return {version:a.version as string,saved_correction_ref:a.saved_correction_ref,view};
}
