import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import type {EntryIntakeReviewStore} from "./mirayClosedLoopEntryIntake";
import config from "../../skin_engine/config/miray_closed_loop_entry_ui.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import dispatch from "../../skin_engine/config/miray_closed_loop_dispatch.json";
import {validateMiraySkinState, type MiraySkinState} from "./miraySkinState";
import {parseMirayRoutineDelivery, type MirayRoutineDelivery} from "./mirayRoutineResult";

/** Correlation only. The server must resolve its own bound immutable operation.
 * No client-supplied reference is a participant/consent/quota capability.
 * read/recover never create, reserve or dispatch a new operation.
 * ready requires separately prepared full intake and catalog/engine evidence;
 * the two state answers never manufacture that intake.
 */
export type LoopEntryContext = {entry_ref:string;mode:"initial"|"fresh";previous_snapshot_ref:string|null;portfolio_revision:number};
export type LoopEntryView = {
  version:string;context:LoopEntryContext|null;
  status:"ready"|"pending"|"completed"|"deferred"|"terminal_without_result"|"blocked";
  decision_ref:string|null;result:MirayRoutineDelivery|null;reason:string|null;
  evaluation_scope:"synthetic_local_review_only";
};
export type LoopEntryRequest = {version:string;entry_ref:string;previous_snapshot_ref:string|null;expected_portfolio_revision:number;observation:MiraySkinState};
/** Explicit injected local TEST seam. No runtime default or persistent client cache. */
export interface ClosedLoopEntryReviewStore {
  /** Explicit local input seam; never composed by a runtime default. */
  intake?:EntryIntakeReviewStore;
  read(options?:MemberStatusReadOptions):Promise<unknown>;
  recover(entryRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
  submit(request:LoopEntryRequest,options?:MemberStatusReadOptions):Promise<unknown>;
  /** Optional synthetic server port: reads its retained original input only. */
  resume?(entryRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
  /** Explicit terminal-original correlation; server resolves its own parent. */
  startFresh?(entryRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
}
export function assertLoopEntryReviewOnly(){
  if(config.enabled!==false || config.automatic_retry!==false || config.automatic_poll!==false || Object.values(loop.flags).some(Boolean))throw new Error("Unapproved loop entry runtime");
}
function exact(v:unknown,keys:string[]):Record<string,unknown>{
  if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected entry fields");
  return v as Record<string,unknown>;
}
function ref(v:unknown):asserts v is string{if(typeof v!=="string" || !/^sha256:[0-9a-f]{64}$/.test(v))throw new Error("Invalid entry reference");}
function revision(v:unknown):asserts v is number{if(!Number.isSafeInteger(v) || (v as number)<0)throw new Error("Invalid portfolio revision");}
export function parseLoopEntryContext(value:unknown):LoopEntryContext{
  const c=exact(value,["entry_ref","mode","previous_snapshot_ref","portfolio_revision"]);
  ref(c.entry_ref);revision(c.portfolio_revision);
  if(c.mode==="initial"){if(c.previous_snapshot_ref!==null)throw new Error("Initial entry has no parent");}
  else if(c.mode==="fresh")ref(c.previous_snapshot_ref);
  else throw new Error("Invalid entry mode");
  return structuredClone(value) as LoopEntryContext;
}
export function sameLoopEntry(a:LoopEntryContext,b:LoopEntryContext){
  return a.entry_ref===b.entry_ref && a.mode===b.mode && a.previous_snapshot_ref===b.previous_snapshot_ref && a.portfolio_revision===b.portfolio_revision;
}
export function parseLoopEntryView(value:unknown):LoopEntryView{
  assertLoopEntryReviewOnly();
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Entry response too large");
  const v=exact(value,["version","context","status","decision_ref","result","reason","evaluation_scope"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || !config.statuses.includes(v.status as string))throw new Error("Reviewed entry contract required");
  if(v.context!==null)parseLoopEntryContext(v.context);
  if(v.status!=="blocked" && v.context===null)throw new Error("Server-selected entry required");
  if(v.status==="completed"){
    ref(v.decision_ref);const result=parseMirayRoutineDelivery(v.result);
    if(result.state!=="available" || v.reason!==null)throw new Error("Completed result required");
  }else if(v.decision_ref!==null || v.result!==null)throw new Error("Uncompleted entry cannot deliver advice");
  if(v.status==="deferred"){
    if(!dispatch.known_defer_reasons.includes(v.reason as string))throw new Error("Known transient deferral required");
  }else if(v.status==="blocked"){
    if(!config.blocked_reasons.includes(v.reason as string))throw new Error("Known admission block required");
  }else if(v.reason!==null)throw new Error("Do not reconstruct past abstention reasons");
  return structuredClone(value) as LoopEntryView;
}
export function loopEntryRequest(context:LoopEntryContext,observation:MiraySkinState):LoopEntryRequest{
  assertLoopEntryReviewOnly();const c=parseLoopEntryContext(context);validateMiraySkinState(observation);
  if(observation.kind!==(c.mode==="initial"?"baseline":"checkin") || observation.concern_presence==="not_asked" || observation.discomfort_presence==="not_asked" || Date.parse(observation.observed_at)>Date.now())throw new Error("Explicit current state required");
  const value={version:config.version,entry_ref:c.entry_ref,previous_snapshot_ref:c.previous_snapshot_ref,expected_portfolio_revision:c.portfolio_revision,observation:structuredClone(observation)};
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_request_bytes)throw new Error("Entry input too large");
  return value;
}
export function validateLoopEntryRequest(value:unknown):asserts value is LoopEntryRequest{
  const v=exact(value,["version","entry_ref","previous_snapshot_ref","expected_portfolio_revision","observation"]);
  if(v.version!==config.version)throw new Error("Reviewed entry request required");
  const expected=loopEntryRequest({entry_ref:v.entry_ref as string,mode:v.previous_snapshot_ref===null?"initial":"fresh",previous_snapshot_ref:v.previous_snapshot_ref as string|null,portfolio_revision:v.expected_portfolio_revision as number},v.observation as MiraySkinState);
  if(JSON.stringify(expected)!==JSON.stringify({version:v.version,entry_ref:v.entry_ref,previous_snapshot_ref:v.previous_snapshot_ref,expected_portfolio_revision:v.expected_portfolio_revision,observation:v.observation}))throw new Error("Uncanonical entry request");
}
