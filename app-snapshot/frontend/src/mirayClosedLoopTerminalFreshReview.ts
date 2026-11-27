import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_terminal_fresh_review.json";
import precheck from "../../skin_engine/config/miray_closed_loop_next_precheck_review.json";
import {assertNextPrecheckReviewOnly} from "./mirayClosedLoopNextPrecheck";
import {parseIntakeAnswers,completeIntake,type IntakeAnswers} from "./mirayClosedLoopIntake";
import {validateMiraySkinState,type MiraySkinState} from "./miraySkinState";
import {nextRef} from "./mirayClosedLoopNext";

export type TerminalFreshContext={terminal_next_ref:string;fresh_ref:string;parent_decision_ref:string;previous_snapshot_ref:string;portfolio_revision:number};
export type TerminalFreshPlan={status:"local_abstention"|"full_intake_required";reason:string|null;automatic_question_dispatch:false};
export type TerminalFreshView={version:string;context:TerminalFreshContext;stored:boolean;observation:MiraySkinState|null;answers:IntakeAnswers|null;plan:TerminalFreshPlan|null;dispatch_ready:false;evaluation_scope:"synthetic_local_review_only"};
export type TerminalFreshAck={saved:boolean;replayed:boolean;fresh_ref:string;dispatch_ready:false;plan?:TerminalFreshPlan};
export interface TerminalFreshReviewStore {
  read(options?:MemberStatusReadOptions):Promise<TerminalFreshView>;
  precheck(observation:MiraySkinState,options?:MemberStatusReadOptions):Promise<TerminalFreshView>;
  save(observation:MiraySkinState,answers:IntakeAnswers,options?:MemberStatusReadOptions):Promise<TerminalFreshAck>;
}
const baseline=JSON.stringify(config);
export function assertTerminalFreshReviewOnly(){
  assertNextPrecheckReviewOnly();
  if(JSON.stringify(config)!==baseline || config.deployment_context!=="synthetic_test" || [config.enabled,config.registered,config.automatic_retry,config.automatic_poll,config.real_user_question_exposure_enabled,config.dispatch_enabled,config.state_record_is_loop_event,config.registration_confirms_actual_use,config.partial_input_storage_enabled].some(v=>v!==false))throw new Error("Unapproved terminal fresh review");
}
function exact(value:unknown,keys:string[]):Record<string,unknown>{
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected fresh fields");return value as Record<string,unknown>;
}
export function parseTerminalFreshPlan(value:unknown):TerminalFreshPlan{
  const v=exact(value,["status","reason","automatic_question_dispatch"]);
  if(v.automatic_question_dispatch!==false || (v.status==="local_abstention"?!precheck.allowed_reasons.includes(v.reason as string):v.status!=="full_intake_required" || v.reason!==null))throw new Error("Categorical fresh precheck required");return structuredClone(value) as TerminalFreshPlan;
}
export function validateTerminalFreshObservation(value:unknown):asserts value is MiraySkinState{
  validateMiraySkinState(value);
  if(value.kind!=="checkin")throw new Error("New checkin required");
}
export function parseTerminalFreshView(value:unknown,terminalRef:string):TerminalFreshView{
  assertTerminalFreshReviewOnly();nextRef(terminalRef);
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Fresh response too large");
  const v=exact(value,["version","context","stored","observation","answers","plan","dispatch_ready","evaluation_scope"]),c=exact(v.context,["terminal_next_ref","fresh_ref","parent_decision_ref","previous_snapshot_ref","portfolio_revision"]);
  [c.terminal_next_ref,c.fresh_ref,c.parent_decision_ref,c.previous_snapshot_ref].forEach(nextRef);
  if(c.terminal_next_ref!==terminalRef || new Set([c.terminal_next_ref,c.fresh_ref,c.parent_decision_ref,c.previous_snapshot_ref]).size!==4 || !Number.isSafeInteger(c.portfolio_revision) || (c.portfolio_revision as number)<0)throw new Error("Exact terminal fresh context required");
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || v.dispatch_ready!==false || typeof v.stored!=="boolean")throw new Error("Fresh input cannot authorize dispatch");
  if(v.stored){validateTerminalFreshObservation(v.observation);if(!completeIntake(parseIntakeAnswers(v.answers)) || v.plan!==null)throw new Error("Complete retained input required");}
  else if(v.observation!==null || v.answers!==null)throw new Error("Unretained input cannot be returned as saved");
  if(v.plan!==null)parseTerminalFreshPlan(v.plan);
  return structuredClone(value) as TerminalFreshView;
}
export function parseTerminalFreshAck(value:unknown,freshRef:string):TerminalFreshAck{
  assertTerminalFreshReviewOnly();nextRef(freshRef);
  const record=value as Record<string,unknown>,v=exact(value,["saved","replayed","fresh_ref","dispatch_ready",...(record?.saved===false?["plan"]:[])]);
  if(v.fresh_ref!==freshRef || v.dispatch_ready!==false || typeof v.saved!=="boolean" || typeof v.replayed!=="boolean" || (!v.saved && v.replayed))throw new Error("Exact fresh acknowledgement required");
  if(!v.saved)parseTerminalFreshPlan(v.plan);
  return structuredClone(value) as TerminalFreshAck;
}
