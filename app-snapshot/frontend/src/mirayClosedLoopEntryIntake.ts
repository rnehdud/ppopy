import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_entry_intake_http_review.json";
import storage from "../../skin_engine/config/miray_closed_loop_entry_intake_review.json";
import {assertIntakeReviewOnly,completeIntake,parseIntakeAnswers,type IntakeAnswers} from "./mirayClosedLoopIntake";
import {assertLoopEntryReviewOnly,parseLoopEntryContext,type LoopEntryContext} from "./mirayClosedLoopEntry";
export type EntryIntakeView={version:string;context:LoopEntryContext;stored:boolean;answers:IntakeAnswers;evaluation_scope:"synthetic_local_review_only"};
/** Disabled local input seam. A fresh read is explicit and does not start work. */
export interface EntryIntakeReviewStore {
  read(options?:MemberStatusReadOptions):Promise<unknown>;
  readFresh(originalEntryRef:string,options?:MemberStatusReadOptions):Promise<unknown>;
  save(entryRef:string,answers:IntakeAnswers,options?:MemberStatusReadOptions):Promise<unknown>;
}
export function assertEntryIntakeReviewOnly(){
  assertLoopEntryReviewOnly();assertIntakeReviewOnly();
  if(config.enabled || config.registered || config.automatic_retry || config.automatic_poll || config.real_user_question_exposure_enabled ||
     config.deployment_context!=="synthetic_test" || config.question_contract!=="miray_closed_loop_intake_ui_review" ||
     !config.stop_on_missing_answer || config.reuse_policy!=="same_current_entry_target_confirmed_ciphertext_only" ||
     storage.enabled || storage.registered || storage.automatic_retry || storage.automatic_poll || storage.deployment_context!=="synthetic_test")throw new Error("Unapproved entry intake review");
}
export function parseEntryIntakeView(value:unknown):EntryIntakeView{
  assertEntryIntakeReviewOnly();
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Entry input response too large");
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==["version","context","stored","answers","evaluation_scope"].sort().join("|"))throw new Error("Unexpected input fields");
  const v=value as Record<string,unknown>;
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || typeof v.stored!=="boolean")throw new Error("Reviewed entry input contract required");
  parseLoopEntryContext(v.context);const answers=parseIntakeAnswers(v.answers);
  if(v.stored?!completeIntake(answers):Object.values(answers).some(a=>a.state!=="not_asked"))throw new Error("Confirmed same-target answers required");
  return structuredClone(value) as EntryIntakeView;
}
