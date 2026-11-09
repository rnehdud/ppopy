import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_intake_ui_review.json";
import answersConfig from "../../skin_engine/config/miray_closed_loop_intake_review.json";
import consumer from "../../skin_engine/config/consumer_api.json";
import palette from "../../skin_engine/config/ingredient_palette.json";
import safety from "../../skin_engine/config/safety_gate_rules.json";
import aggravating from "../../skin_engine/config/aggravating_factors.json";
import decisionConfig from "../../skin_engine/config/miray_closed_loop_intake_decision_review.json";
import {assertNextReviewOnly,nextRef,type NextDecisionContext} from "./mirayClosedLoopNext";
export type IntakeAnswer={state:"reported"|"none_reported"|"unknown"|"user_refused"|"not_asked";value:unknown};
export type IntakeAnswers=Record<string,IntakeAnswer>;
export type IntakeView={version:string;context:NextDecisionContext;stored:boolean;answers:IntakeAnswers;evaluation_scope:"synthetic_local_review_only"};
export interface NextIntakeReviewStore {precheck?(options?:MemberStatusReadOptions):Promise<unknown>;read(options?:MemberStatusReadOptions):Promise<unknown>;save(ref:string,answers:IntakeAnswers,options?:MemberStatusReadOptions):Promise<unknown>;}
export const intakeSteps=config.steps;
function canonical(value:unknown):string{return JSON.stringify(Array.isArray(value)?value.map(v=>JSON.parse(canonical(v))):value && typeof value==="object"?Object.fromEntries(Object.entries(value).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>[k,JSON.parse(canonical(v))])):value);}
const decisionDependencies=[decisionConfig,config,answersConfig,consumer,palette,safety,aggravating];
const decisionBaseline=decisionDependencies.map(canonical);
export const intakeDecisionLabels=decisionConfig.decision_labels;
function assertDecisionBindings(){
  if(decisionDependencies.some((v,i)=>canonical(v)!==decisionBaseline[i]) || decisionConfig.enabled || decisionConfig.registered || decisionConfig.automatic_poll || decisionConfig.automatic_retry || decisionConfig.real_user_question_exposure_enabled || decisionConfig.deployment_context!=="synthetic_test" || !decisionConfig.stop_on_unknown_or_refused || !decisionConfig.complete_engine_intake_required)throw new Error("Input decision contract changed");
  if(canonical(decisionConfig.bindings.map(b=>[b.step_id,b.fields]))!==canonical(config.steps.map(s=>[s.id,s.fields])) || canonical(decisionConfig.bindings.flatMap(b=>b.fields).sort())!==canonical([...answersConfig.fields].sort()) || decisionConfig.bindings.some(b=>!b.decision_areas.length || b.decision_areas.some(a=>!(a in intakeDecisionLabels))))throw new Error("Explicit decision bindings required");
  const habits=config.steps.find(s=>s.id==="habits")!.items!.map(i=>i.value).sort();
  const engineHabits=[...new Set(Object.values(aggravating.runtime_evaluator.factors).flatMap(f=>f.answer_ids))].sort();
  if(canonical(habits)!==canonical(engineHabits))throw new Error("Unreviewed habit question");
}
export function nextIntakeRef(value:unknown):asserts value is string {nextRef(value);}
export function assertIntakeReviewOnly(){assertNextReviewOnly();if(config.enabled || config.registered || config.automatic_retry || config.automatic_poll || config.real_user_question_exposure_enabled || config.deployment_context!=="synthetic_test" || !config.stop_on_missing_answer || config.reuse_policy!=="same_current_target_confirmed_ciphertext_only" || answersConfig.enabled || answersConfig.registered)throw new Error("Unapproved input review");}
function exact(value:unknown,keys:string[]):Record<string,unknown>{if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected input fields");return value as Record<string,unknown>;}
export function emptyIntake():IntakeAnswers{return Object.fromEntries(answersConfig.fields.map(k=>[k,{state:"not_asked",value:null}]));}
export function parseIntakeAnswers(value:unknown):IntakeAnswers{
  assertIntakeReviewOnly();assertDecisionBindings();const v=exact(value,answersConfig.fields);
  if(new TextEncoder().encode(JSON.stringify(value)).length>answersConfig.max_answer_bytes)throw new Error("Input answers too large");
  for(const field of answersConfig.fields){const a=exact(v[field],["state","value"]);if(!answersConfig.answer_states.includes(a.state as string))throw new Error("Explicit answer required");
    if(["unknown","user_refused","not_asked"].includes(a.state as string)){if(a.value!==null)throw new Error("Missing answer has value");continue;}
    if(a.state==="none_reported" && (!(field in answersConfig.none_values) || JSON.stringify(a.value)!==JSON.stringify(answersConfig.none_values[field as keyof typeof answersConfig.none_values])))throw new Error("Explicit none required");
    const x=a.value;let valid=false;
    if(["irritation_history","retinoid_in_use"].includes(field))valid=typeof x==="boolean";
    else if(field==="tightness_dryness_score")valid=Number.isInteger(x) && (x as number)>=0 && (x as number)<=safety.tightness_dryness.scale_max;
    else if(["care_priorities","current_actives"].includes(field)){const allowed=field==="current_actives"?consumer.allowed_current_actives:Object.keys(palette.care_priority_direction).filter(k=>!k.startsWith("_"));valid=Array.isArray(x) && x.every(y=>typeof y==="string" && allowed.includes(y)) && new Set(x).size===x.length;}
    else if(field==="aggravating_answers"){const ids=config.steps.find(s=>s.id==="habits")!.items!.map(i=>i.value);valid=x!==null && typeof x==="object" && !Array.isArray(x) && Object.entries(x).every(([k,y])=>ids.includes(k) && typeof y==="boolean");}
    else valid=typeof x==="string" && (field==="product_context_status"?consumer.allowed_product_context_statuses:safety.intake_policy.user_facing_status_values).includes(x);
    if(!valid)throw new Error("Invalid explicit input");
  }
  const active=v.current_actives as IntakeAnswer,retinoid=v.retinoid_in_use as IntakeAnswer;
  if(["reported","none_reported"].includes(active.state) && ["reported","none_reported"].includes(retinoid.state) && (active.value as string[]).includes("retinoid")!==retinoid.value)throw new Error("Contradictory active use requires explicit correction");
  return structuredClone(value) as IntakeAnswers;
}
export function completeIntake(value:IntakeAnswers){return Object.values(parseIntakeAnswers(value)).every(a=>a.state==="reported" || a.state==="none_reported");}
export function intakeDecisionGaps(value:IntakeAnswers){
  const draft=parseIntakeAnswers(value);
  const gaps=decisionConfig.bindings.flatMap(b=>{const missing=b.fields.filter(f=>!["reported","none_reported"].includes(draft[f].state)).map(field=>({field,state:draft[field].state}));return missing.length?[{step_id:b.step_id,missing,decision_areas:[...b.decision_areas]}]:[];});
  const stopped=gaps.some(g=>g.missing.some(a=>a.state==="unknown" || a.state==="user_refused"));
  const partial=gaps.some(g=>g.missing.length!==decisionConfig.bindings.find(b=>b.step_id===g.step_id)!.fields.length);
  return {version:decisionConfig.version,status:!gaps.length?"ready":stopped || partial?"deferred":"explicit_input_required",gaps,next_step_id:!gaps.length || stopped || partial?null:gaps[0].step_id,automatic_question_dispatch:false,evaluation_scope:decisionConfig.evaluation_scope};
}
export function pendingIntakeStep(value:IntakeAnswers){const plan=intakeDecisionGaps(value);return config.steps.find(s=>s.id===plan.next_step_id)??null;}
export function parseIntakeView(value:unknown):IntakeView{
  assertIntakeReviewOnly();if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Input response too large");
  const v=exact(value,["version","context","stored","answers","evaluation_scope"]),c=exact(v.context,["next_ref","parent_decision_ref","snapshot_ref","portfolio_revision"]);
  if(v.version!==config.version || v.evaluation_scope!==config.evaluation_scope || typeof v.stored!=="boolean")throw new Error("Reviewed input contract required");
  [c.next_ref,c.parent_decision_ref,c.snapshot_ref].forEach(nextRef);if(new Set([c.next_ref,c.parent_decision_ref,c.snapshot_ref]).size!==3 || !Number.isSafeInteger(c.portfolio_revision) || (c.portfolio_revision as number)<0)throw new Error("Exact input context required");
  const answers=parseIntakeAnswers(v.answers);
  if(v.stored?!completeIntake(answers):Object.values(answers).some(a=>a.state!=="not_asked"))throw new Error("Confirmed same-target answers required");
  return structuredClone(value) as IntakeView;
}
