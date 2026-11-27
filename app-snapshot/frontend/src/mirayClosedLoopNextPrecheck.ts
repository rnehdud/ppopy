import config from "../../skin_engine/config/miray_closed_loop_next_precheck_review.json";
import {assertIntakeReviewOnly} from "./mirayClosedLoopIntake";
import {nextRef,type NextDecisionContext} from "./mirayClosedLoopNext";

export type NextPrecheckView={version:string;context:NextDecisionContext;plan:{status:"local_abstention"|"full_intake_required";reason:string|null;automatic_question_dispatch:false};evaluation_scope:"synthetic_local_review_only"};
const baseline=JSON.stringify(config);
export function assertNextPrecheckReviewOnly(){
  assertIntakeReviewOnly();
  if(JSON.stringify(config)!==baseline || config.deployment_context!=="synthetic_test" || !config.full_intake_still_required || [config.enabled,config.registered,config.real_user_question_exposure_enabled,config.automatic_retry,config.automatic_poll,config.precheck_creates_decision,config.automatic_question_dispatch,config.raw_state_exposure_enabled].some(v=>v!==false))throw new Error("Unapproved next precheck");
}
function exact(value:unknown,keys:string[]):Record<string,unknown>{if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected precheck fields");return value as Record<string,unknown>;}
export function parseNextPrecheckView(value:unknown):NextPrecheckView{
  assertNextPrecheckReviewOnly();if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Precheck response too large");
  const v=exact(value,["version","context","plan","evaluation_scope"]),c=exact(v.context,["next_ref","parent_decision_ref","snapshot_ref","portfolio_revision"]),p=exact(v.plan,["status","reason","automatic_question_dispatch"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope)throw new Error("Reviewed precheck required");
  [c.next_ref,c.parent_decision_ref,c.snapshot_ref].forEach(nextRef);
  if(new Set([c.next_ref,c.parent_decision_ref,c.snapshot_ref]).size!==3 || !Number.isSafeInteger(c.portfolio_revision) || (c.portfolio_revision as number)<0)throw new Error("Exact precheck context required");
  if(p.automatic_question_dispatch!==false || (p.status==="local_abstention"?!config.allowed_reasons.includes(p.reason as string):p.status!=="full_intake_required" || p.reason!==null))throw new Error("Categorical precheck required");
  return structuredClone(value) as NextPrecheckView;
}
export function matchNextPrecheck(value:unknown,context:NextDecisionContext){
  const v=parseNextPrecheckView(value);
  if((Object.keys(context) as (keyof NextDecisionContext)[]).some(k=>v.context[k]!==context[k]))throw new Error("Precheck target changed");return v;
}
