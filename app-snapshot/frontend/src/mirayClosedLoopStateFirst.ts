import config from "../../skin_engine/config/miray_closed_loop_state_first_review.json";
import questions from "../../skin_engine/config/miray_skin_state_questions.json";
import skin from "../../skin_engine/config/miray_skin_state.json";
import product from "../../skin_engine/config/product_entry_flow.json";
import {assertEntryIntakeReviewOnly} from "./mirayClosedLoopEntryIntake";
import {validateMiraySkinState,type MiraySkinState} from "./miraySkinState";

function canonical(v:unknown):string {
  if(Array.isArray(v))return JSON.stringify(v.map(x=>JSON.parse(canonical(x))));
  if(v && typeof v==="object")return JSON.stringify(Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b)).map(([k,x])=>[k,JSON.parse(canonical(x))])));
  return JSON.stringify(v);
}
const dependencies=[config,questions,skin,product],baseline=dependencies.map(canonical);
export function assertStateFirstReviewOnly(){
  assertEntryIntakeReviewOnly();
  if(dependencies.some((v,i)=>canonical(v)!==baseline[i]) || config.enabled || config.registered || config.real_user_question_exposure_enabled || config.automatic_retry || config.automatic_poll ||
    config.deployment_context!=="synthetic_test" || config.partial_state_storage_enabled || config.early_abstention_creates_decision || !config.complete_engine_intake_required ||
    canonical(questions.profiles.routine_state_and_safety)!==canonical(config.profile_fields) || canonical(product.context_contract.followup_order)!==canonical(config.uncollected_discomfort_context))throw new Error("Unapproved state-first review");
}
export type StateFirstPlan={version:string;status:"more_input_required"|"local_abstention";reason:string|null;automatic_question_dispatch:false;evaluation_scope:"synthetic_local_review_only"};
/** Transient question-order precheck only; never an engine decision or receipt. */
export function stateFirstPlan(value:MiraySkinState):StateFirstPlan{
  assertStateFirstReviewOnly();validateMiraySkinState(value);
  if(Date.parse(value.observed_at)>Date.now() || value.sensitivity_history!=="not_asked" || [value.persistence,value.recent_change].some(v=>!["not_asked","not_applicable"].includes(v)))throw new Error("Reviewed current core profile required");
  let reason:string|null=null;
  for(const field of config.core_fields_in_engine_order as ("concern_presence"|"discomfort_presence")[]){
    if(config.missing_core_values.includes(value[field])){reason=`${field}:${value[field]}`;break;}
  }
  // Types do not supply the six observations still required by the existing
  // engine. Do not collect seven unrelated intake steps before this abstention.
  if(reason===null && value.discomfort_presence==="reported")reason="decision_abstained";
  return {version:config.version,status:reason?"local_abstention":"more_input_required",reason,automatic_question_dispatch:false,evaluation_scope:"synthetic_local_review_only"};
}
