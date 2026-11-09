import config from "../../skin_engine/config/miray_closed_loop_ui.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import statePolicy from "../../skin_engine/config/miray_closed_loop_state_http_test.json";
import {validateMiraySkinState,type MiraySkinState} from "./miraySkinState";
import type {ProductChangeReviewStore} from "./mirayClosedLoopTransitions";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";

export type ActualUseQuestion={recommendation_id:string;product_id:string;product_name:string;previous_frequency:string;proposed_action:string;proposed_frequency:number|null};
export type ActualUseSummary={ref:string;recommendation_id:string|null;product_id:string;product_name:string;action_type:string;frequency:string|null;effective_from:string};
export type ClosedLoopEpisode={version:string;decision_ref:string;decision_at:string;portfolio_revision:number;actual_use_questions:ActualUseQuestion[];actual_actions:ActualUseSummary[];unconfirmed_count:number;unconfirmed_answers:Array<{recommendation_id:string;response:string}>;unsupported_count:number;followup:{snapshot_ref:string;observed_at:string}|null};
type Request={version:string;decision_ref:string;request_id:string};
export type ConfirmActualRequest=Request & {recommendation_id:string;frequency:string;effective_from:string|null};
export type SaveFollowupRequest=Request & {observation:MiraySkinState;expected_portfolio_revision:number;other_changes:"not_asked"};
/** Explicit synthetic TEST composition only. No HTTP implementation or fixture fallback. */
export interface ClosedLoopReviewStore {
  frequencyCorrections?:import("./mirayClosedLoopFrequency").FrequencyCorrectionReviewStore;
  nextDecision?:import("./mirayClosedLoopNext").NextDecisionReviewStore;
  productChanges?:ProductChangeReviewStore;
  read(options?:MemberStatusReadOptions):Promise<unknown>;
  confirmActual(request:ConfirmActualRequest,options?:MemberStatusReadOptions):Promise<unknown>;
  saveFollowup(request:SaveFollowupRequest,options?:MemberStatusReadOptions):Promise<unknown>;
}
function exact(v:unknown,keys:string[]):Record<string,unknown>{
  if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected loop fields");
  return v as Record<string,unknown>;
}
function text(v:unknown):asserts v is string{if(typeof v!=="string" || !v.trim() || v.length>300)throw new Error("Invalid loop text");}
function ref(v:unknown):asserts v is string{if(typeof v!=="string" || !/^sha256:[0-9a-f]{64}$/.test(v))throw new Error("Invalid loop ref");}
export function loopTime(v:unknown):asserts v is string {
  if(typeof v!=="string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(v) || !Number.isFinite(Date.parse(v)) || new Date(v).toISOString().slice(0,19)!==v.slice(0,19))throw new Error("UTC time required");
}
function count(v:unknown,max:number):asserts v is number{if(!Number.isSafeInteger(v) || (v as number)<0 || (v as number)>max)throw new Error("Invalid loop bound");}
export function parseClosedLoopEpisode(value:unknown):ClosedLoopEpisode {
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Loop response too large");
  const v=exact(value,["version","decision_ref","decision_at","portfolio_revision","actual_use_questions","actual_actions","unconfirmed_count","unconfirmed_answers","unsupported_count","followup"]);
  if(v.version!==config.version)throw new Error("Reviewed loop version required");
  ref(v.decision_ref);loopTime(v.decision_at);count(v.portfolio_revision,Number.MAX_SAFE_INTEGER);count(v.unconfirmed_count,loop.max_episode_events);count(v.unsupported_count,loop.max_recommendations);
  if(!Array.isArray(v.actual_use_questions) || v.actual_use_questions.length>loop.max_recommendations || !Array.isArray(v.actual_actions) || v.actual_actions.length>loop.max_actual_actions)throw new Error("Bounded loop required");
  if(!Array.isArray(v.unconfirmed_answers) || v.unconfirmed_answers.length!==v.unconfirmed_count)throw new Error("Explicit unconfirmed answers required");
  for(const raw of v.unconfirmed_answers){const a=exact(raw,["recommendation_id","response"]);ref(a.recommendation_id);if(!config.unconfirmed_values.includes(a.response as string))throw new Error("Invalid unconfirmed answer");}
  const ids=new Set<string>(),products=new Set<string>();
  for(const raw of v.actual_use_questions){
    const q=exact(raw,["recommendation_id","product_id","product_name","previous_frequency","proposed_action","proposed_frequency"]);
    ref(q.recommendation_id);text(q.product_id);text(q.product_name);
    if(ids.has(q.recommendation_id) || products.has(q.product_id) || !loop.frequency_values.includes(q.previous_frequency as string) || !config.supported_actual_use_actions.includes(q.proposed_action as string))throw new Error("Invalid actual-use question");
    ids.add(q.recommendation_id);products.add(q.product_id);
    if(q.proposed_frequency!==null)count(q.proposed_frequency,7);
    if(q.proposed_action==="REDUCE" && (!config.frequency_values.includes(q.previous_frequency as string) || q.proposed_frequency===null || (q.proposed_frequency as number)>=Number(q.previous_frequency)))throw new Error("Invalid proposed reduction");
  }
  const actions=new Set<string>();
  for(const raw of v.actual_actions){
    const a=exact(raw,["ref","recommendation_id","product_id","product_name","action_type","frequency","effective_from"]);
    ref(a.ref);if(a.recommendation_id!==null)ref(a.recommendation_id);text(a.product_id);text(a.product_name);loopTime(a.effective_from);
    if(actions.has(a.ref) || ![...loop.actual_action_types,statePolicy.current_use_action_type].includes(a.action_type as string) || (a.frequency!==null && !loop.frequency_values.includes(a.frequency as string)) || Date.parse(a.effective_from)<Date.parse(v.decision_at))throw new Error("Invalid actual-use summary");
    actions.add(a.ref);
  }
  if(v.followup!==null){const f=exact(v.followup,["snapshot_ref","observed_at"]);ref(f.snapshot_ref);loopTime(f.observed_at);
    if(v.actual_use_questions.length || Date.parse(f.observed_at)<Date.parse(v.decision_at) || v.actual_actions.some(a=>Date.parse(a.effective_from)>Date.parse(f.observed_at as string)))throw new Error("Invalid fresh followup");}
  return structuredClone(value) as ClosedLoopEpisode;
}
export function confirmActualRequest(episode:ClosedLoopEpisode,question:ActualUseQuestion,frequency:string,effectiveFrom:string|null,requestId=crypto.randomUUID()):ConfirmActualRequest{
  const current=parseClosedLoopEpisode(episode);
  const canonical=current.actual_use_questions.find(q=>q.recommendation_id===question.recommendation_id);
  if(!canonical || JSON.stringify(canonical)!==JSON.stringify(question) || ![...config.frequency_values,...config.unconfirmed_values].includes(frequency))throw new Error("Current unanswered use required");
  if(config.unconfirmed_values.includes(frequency)){if(effectiveFrom!==null)throw new Error("Unconfirmed use has no action time");}
  else {if(!config.frequency_values.includes(question.previous_frequency))throw new Error("Unknown before cannot prove change");loopTime(effectiveFrom);
    if(Date.parse(effectiveFrom)<Date.parse(current.decision_at) || Date.parse(effectiveFrom)>Date.now())throw new Error("Invalid action interval");}
  return {version:config.version,decision_ref:current.decision_ref,request_id:requestId,recommendation_id:question.recommendation_id,frequency,effective_from:effectiveFrom};
}
export class FollowupObservationError extends Error {
  constructor(readonly code:"F-C-E"|"F-C-V"|"F-C-D"|"F-C-K"|"F-C-Q"|"F-C-TD"|"F-C-TA") {
    // Fixed classifications only: never include answers, product/record IDs or times.
    super(code);
  }
}
export function followupCompletionCode(error:unknown):string {
  return error instanceof FollowupObservationError?error.code:"F-C-U";
}
export function validateFollowupObservation(episode:ClosedLoopEpisode,observation:MiraySkinState):ClosedLoopEpisode{
  let current:ClosedLoopEpisode;
  try{current=parseClosedLoopEpisode(episode);}catch{throw new FollowupObservationError("F-C-E");}
  try{validateMiraySkinState(observation);}catch{throw new FollowupObservationError("F-C-V");}
  if(current.followup)throw new FollowupObservationError("F-C-D");
  if(observation.kind!=="checkin")throw new FollowupObservationError("F-C-K");
  if(observation.concern_presence==="not_asked" || observation.discomfort_presence==="not_asked")throw new FollowupObservationError("F-C-Q");
  if(Date.parse(observation.observed_at)<Date.parse(current.decision_at))throw new FollowupObservationError("F-C-TD");
  if(current.actual_actions.some(a=>Date.parse(observation.observed_at)<Date.parse(a.effective_from)))throw new FollowupObservationError("F-C-TA");
  return current;
}
export function saveFollowupRequest(episode:ClosedLoopEpisode,observation:MiraySkinState,requestId=crypto.randomUUID()):SaveFollowupRequest{
  const current=validateFollowupObservation(episode,observation);
  return {version:config.version,decision_ref:current.decision_ref,request_id:requestId,observation:structuredClone(observation),expected_portfolio_revision:current.portfolio_revision,other_changes:"not_asked"};
}
