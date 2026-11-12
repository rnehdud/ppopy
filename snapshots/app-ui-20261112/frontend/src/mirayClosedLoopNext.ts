import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_next_review.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import dispatch from "../../skin_engine/config/miray_closed_loop_dispatch.json";
import {parseMirayRoutineDelivery,type MirayRoutineDelivery} from "./mirayRoutineResult";
import type {NextIntakeReviewStore} from "./mirayClosedLoopIntake";
export type NextDecisionContext={next_ref:string;parent_decision_ref:string;snapshot_ref:string;portfolio_revision:number};
export type NextDecisionView={version:string;context:NextDecisionContext|null;status:"ready"|"blocked"|"pending"|"completed"|"deferred"|"terminal_without_result";decision_ref:string|null;result:MirayRoutineDelivery|null;reason:string|null;evaluation_scope:"synthetic_local_review_only"};
export interface NextDecisionReviewStore {
  intake?:NextIntakeReviewStore;
  read(options?:MemberStatusReadOptions):Promise<unknown>;
  recover(nextRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
  submit(nextRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
  resume(nextRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
}
export function assertNextReviewOnly(){if(config.enabled!==false || config.registered!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false || config.persistent_queue_enabled!==false || Object.values(loop.flags).some(Boolean))throw new Error("Unapproved next review");}
export function nextRef(v:unknown):asserts v is string{if(typeof v!=="string" || !/^sha256:[0-9a-f]{64}$/.test(v))throw new Error("Invalid next correlation");}
function exact(v:unknown,keys:string[]):Record<string,unknown>{if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected next fields");return v as Record<string,unknown>;}
export function parseNextDecisionView(value:unknown):NextDecisionView{
  assertNextReviewOnly();if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Next response too large");
  const v=exact(value,["version","context","status","decision_ref","result","reason","evaluation_scope"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || !config.statuses.includes(v.status as string))throw new Error("Reviewed next contract required");
  if(v.context!==null){const c=exact(v.context,["next_ref","parent_decision_ref","snapshot_ref","portfolio_revision"]);nextRef(c.next_ref);nextRef(c.parent_decision_ref);nextRef(c.snapshot_ref);
    if(c.parent_decision_ref===c.snapshot_ref || c.next_ref===c.snapshot_ref || c.next_ref===c.parent_decision_ref || !Number.isSafeInteger(c.portfolio_revision) || (c.portfolio_revision as number)<0)throw new Error("Exact next parent required");}
  else if(v.status!=="blocked" || v.reason!=="followup_required")throw new Error("Current next context required");
  if(v.status==="completed"){nextRef(v.decision_ref);if(v.decision_ref===(v.context as NextDecisionContext).parent_decision_ref || parseMirayRoutineDelivery(v.result).state!=="available" || v.reason!==null)throw new Error("Confirmed new next decision required");}
  else if(v.decision_ref!==null || v.result!==null)throw new Error("Unconfirmed next result");
  if(v.status==="blocked"){if(!config.blocked_reasons.includes(v.reason as string))throw new Error("Known next block required");}
  else if(v.status==="deferred"){if(!dispatch.known_defer_reasons.includes(v.reason as string))throw new Error("Known transient next deferral required");}
  else if(v.reason!==null)throw new Error("Do not invent retained deferral reasons");
  return structuredClone(value) as NextDecisionView;
}
