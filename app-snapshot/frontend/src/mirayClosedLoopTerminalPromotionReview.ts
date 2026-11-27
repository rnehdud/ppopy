import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_terminal_promotion_review.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import dispatch from "../../skin_engine/config/miray_closed_loop_dispatch.json";
import {nextRef} from "./mirayClosedLoopNext";
import {parseMirayRoutineDelivery,type MirayRoutineDelivery} from "./mirayRoutineResult";
import {assertTerminalFreshReviewOnly} from "./mirayClosedLoopTerminalFreshReview";

export type TerminalPromotionContext={terminal_next_ref:string;fresh_ref:string;parent_decision_ref:string;snapshot_ref:string;portfolio_revision:number};
export type TerminalPromotionView={version:string;context:TerminalPromotionContext;status:"input_ready"|"ready"|"blocked"|"pending"|"completed"|"deferred"|"terminal_without_result";reason:string|null;decision_ref:string|null;result:MirayRoutineDelivery|null;evaluation_scope:"synthetic_local_review_only"};
export interface TerminalPromotionReviewStore {
  read(options?:MemberStatusReadOptions):Promise<TerminalPromotionView>;
  promote(options?:MemberStatusReadOptions):Promise<TerminalPromotionView>;
  resume(options?:MemberStatusReadOptions):Promise<TerminalPromotionView>;
}
export function assertTerminalPromotionReviewOnly(){
  assertTerminalFreshReviewOnly();
  if(config.enabled!==false || config.registered!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false || config.real_user_question_exposure_enabled!==false || config.registration_confirms_actual_use!==false || Object.values(loop.flags).some(Boolean))throw new Error("Unapproved terminal promotion");
}
function exact(v:unknown,keys:string[]):Record<string,unknown>{
  if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected promotion fields");return v as Record<string,unknown>;
}
export function parseTerminalPromotionView(value:unknown,terminalRef:string):TerminalPromotionView{
  assertTerminalPromotionReviewOnly();nextRef(terminalRef);
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Promotion response too large");
  const v=exact(value,["version","context","status","reason","decision_ref","result","evaluation_scope"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || !config.statuses.includes(v.status as string))throw new Error("Reviewed promotion contract required");
  const c=exact(v.context,["terminal_next_ref","fresh_ref","parent_decision_ref","snapshot_ref","portfolio_revision"]);
  for(const k of ["terminal_next_ref","fresh_ref","parent_decision_ref","snapshot_ref"])nextRef(c[k]);
  if(c.terminal_next_ref!==terminalRef || new Set([c.terminal_next_ref,c.fresh_ref,c.parent_decision_ref,c.snapshot_ref]).size!==4 || !Number.isSafeInteger(c.portfolio_revision) || (c.portfolio_revision as number)<0)throw new Error("Exact promotion parent required");
  if(v.status==="completed"){
    nextRef(v.decision_ref);
    if([c.terminal_next_ref,c.fresh_ref,c.parent_decision_ref,c.snapshot_ref].includes(v.decision_ref) || parseMirayRoutineDelivery(v.result).state!=="available" || v.reason!==null)throw new Error("Confirmed new promotion decision required");
  }else if(v.decision_ref!==null || v.result!==null)throw new Error("Unconfirmed promotion result");
  if(v.status==="blocked"){if(!config.blocked_reasons.includes(v.reason as string))throw new Error("Known promotion block required");}
  else if(v.status==="deferred"){if(!dispatch.known_defer_reasons.includes(v.reason as string))throw new Error("Known transient promotion deferral required");}
  else if(v.reason!==null)throw new Error("Do not invent retained promotion reasons");
  return structuredClone(value) as TerminalPromotionView;
}
