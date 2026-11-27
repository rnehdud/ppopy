import config from "../../skin_engine/config/miray_closed_loop_terminal_ui_review.json";
import questions from "../../skin_engine/config/miray_skin_state_questions.json";
import {assertStateFirstReviewOnly,stateFirstPlan} from "./mirayClosedLoopStateFirst";
import {assertTerminalPromotionReviewOnly,parseTerminalPromotionView,type TerminalPromotionReviewStore,type TerminalPromotionView} from "./mirayClosedLoopTerminalPromotionReview";
import {parseTerminalFreshView,parseTerminalFreshAck,validateTerminalFreshObservation,type TerminalFreshContext,type TerminalFreshReviewStore,type TerminalFreshView} from "./mirayClosedLoopTerminalFreshReview";
import {completeIntake,emptyIntake,parseIntakeAnswers,type IntakeAnswers} from "./mirayClosedLoopIntake";
import type {IntakePanelStore} from "./MirayIntakePanel";
import type {MiraySkinState} from "./miraySkinState";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";

export type TerminalUiReviewStore={fresh:TerminalFreshReviewStore;promotion:TerminalPromotionReviewStore};
export function terminalCanonical(value:unknown):string {
  if(Array.isArray(value))return JSON.stringify(value.map(v=>JSON.parse(terminalCanonical(v))));
  if(value && typeof value==="object")return JSON.stringify(Object.fromEntries(Object.entries(value).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>[k,JSON.parse(terminalCanonical(v))])));
  return JSON.stringify(value);
}
const baseline=terminalCanonical(config);
export function assertTerminalUiReviewOnly(){
  assertTerminalPromotionReviewOnly();assertStateFirstReviewOnly();
  if(terminalCanonical(config)!==baseline || config.enabled!==false || config.registered!==false || config.deployment_context!=="synthetic_test" ||
    [config.real_user_question_exposure_enabled,config.automatic_retry,config.automatic_poll,config.draft_storage_enabled,config.registration_confirms_actual_use,config.saved_ack_starts_dispatch,config.promotion_ack_starts_dispatch,config.recovery_recalculates].some(v=>v!==false) ||
    config.core_question_count!==2 || config.conditional_discomfort_detail_count!==1 || config.complete_engine_intake_required!==true ||
    terminalCanonical(questions.profiles[config.question_profile as keyof typeof questions.profiles])!==terminalCanonical(["concern_presence","discomfort_presence","discomfort_types"]))throw new Error("Unapproved terminal UI review");
}
export function matchTerminalFresh(value:unknown,fixed:TerminalFreshContext):TerminalFreshView {
  assertTerminalUiReviewOnly();const v=parseTerminalFreshView(value,fixed.terminal_next_ref);
  if(terminalCanonical(v.context)!==terminalCanonical(fixed))throw new Error("Fresh input target changed");return v;
}
export function matchTerminalPromotion(value:unknown,fixed:TerminalFreshContext,previous?:TerminalPromotionView):TerminalPromotionView {
  assertTerminalUiReviewOnly();const v=parseTerminalPromotionView(value,fixed.terminal_next_ref);
  for(const k of ["terminal_next_ref","fresh_ref","parent_decision_ref","portfolio_revision"] as const)if(v.context[k]!==fixed[k])throw new Error("Promotion input changed");
  if(v.context.snapshot_ref===fixed.previous_snapshot_ref || previous && terminalCanonical(v.context)!==terminalCanonical(previous.context))throw new Error("Promotion snapshot changed");return v;
}

/** Adapter for the existing seven-step panel. This saves only complete explicit
 * answers with the exact new observation; it never promotes or calculates. */
export function createTerminalUiIntakeStore(store:TerminalFreshReviewStore,initial:TerminalFreshView,observation:MiraySkinState,onRetained?:(v:TerminalFreshView)=>void,assertCurrent?:()=>void):IntakePanelStore<TerminalFreshContext>{
  assertTerminalUiReviewOnly();const selected=parseTerminalFreshView(initial,initial.context.terminal_next_ref),fixed=structuredClone(selected.context),candidate=structuredClone(observation);let first=true;
  let submission:IntakeAnswers|null=null;
  validateTerminalFreshObservation(candidate);
  if(stateFirstPlan(candidate).status!=="more_input_required" || selected.stored || selected.plan?.status!=="full_intake_required")throw new Error("New eligible state required");
  const gate=(options:MemberStatusReadOptions)=>{options.signal?.throwIfAborted();if(options.isCurrent && options.isCurrent()!==true)throw new Error("Terminal input consumer retired");assertTerminalUiReviewOnly();assertCurrent?.();};
  const within=(options:MemberStatusReadOptions)=>({...options,isCurrent:()=>{try{gate(options);return true;}catch{return false;}}});
  const view=(v:TerminalFreshView,options:MemberStatusReadOptions)=>{
    gate(options);
    if(v.stored && terminalCanonical(v.observation)!==terminalCanonical(candidate))throw new Error("Retained observation differs");
    if(v.stored && submission && terminalCanonical(v.answers)!==terminalCanonical(submission))throw new Error("Exact retained input required");
    if(v.stored)onRetained?.(structuredClone(v));
    // A retained observer may synchronously leave/retire this input frame.
    // Cached recovery and precheck replay need the same delivery fence as save.
    gate(options);
    return {context:structuredClone(fixed),stored:v.stored,answers:v.stored?parseIntakeAnswers(v.answers):emptyIntake()};
  };
  return {
    // Child layout reads wait for the parent to commit its exact intake frame.
    read:async o=>{await Promise.resolve();gate(o);if(first){first=false;return view(selected,o);}const v=matchTerminalFresh(await store.read(within(o)),fixed);gate(o);return view(v,o);},
    save:async(c,answers,o)=>{
      const requested=structuredClone(c),a=parseIntakeAnswers(answers);
      await Promise.resolve();gate(o);if(terminalCanonical(requested)!==terminalCanonical(fixed) || !completeIntake(a))throw new Error("Exact complete input required");
      if(submission && terminalCanonical(a)!==terminalCanonical(submission))throw new Error("Original confirmed input required");
      submission=structuredClone(a);
      const p=matchTerminalFresh(await store.precheck(structuredClone(candidate),within(o)),fixed);gate(o);
      if(p.stored){const retained=view(p,o);if(terminalCanonical(retained.answers)!==terminalCanonical(a))throw new Error("Different retained answers");return retained;}
      if(p.plan?.status!=="full_intake_required")throw new Error("Current state requires abstention");
      const ack=parseTerminalFreshAck(await store.save(structuredClone(candidate),structuredClone(a),within(o)),fixed.fresh_ref);gate(o);
      if(!ack.saved)throw new Error("Input was not retained");
      const raw=await store.read(within(o));gate(o);
      const saved=view(matchTerminalFresh(raw,fixed),o);gate(o);
      if(!saved.stored || terminalCanonical(saved.answers)!==terminalCanonical(a))throw new Error("Exact retained input required");return saved;
    }
  };
}
