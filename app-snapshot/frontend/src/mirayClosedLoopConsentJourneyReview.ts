import config from "../../skin_engine/config/miray_closed_loop_consent_journey_review.json";
import {AppMemberResponseSessionChanged,createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {parseAppHistoryConsentStatus,type AppHistoryConsentStatus,type AppHistoryConsentStore} from "./appHistoryConsent";
import {assertJourneyReviewOnly,type ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";
import {terminalCanonical} from "./mirayClosedLoopTerminalUiReview";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

const baseline=terminalCanonical(config);
export function assertConsentJourneyReviewOnly(){
  assertJourneyReviewOnly();
  if(terminalCanonical(config)!==baseline || config.deployment_context!=="synthetic_test" || config.evaluation_scope!=="synthetic_local_review_only" ||
    [config.enabled,config.registered,config.real_user_question_exposure_enabled,config.automatic_retry,config.automatic_poll,config.draft_storage_enabled,config.automatic_dispatch,config.navigation_confirms_actual_use].some(v=>v!==false) ||
    !config.shared_member_lifetime_required || !config.explicit_navigation_required || !config.consent_refresh_retires_journey ||
    config.question_profile!=="routine_state_and_safety" || config.core_question_count!==2 || config.conditional_discomfort_detail_count!==1)throw new Error("Unapproved consent journey review");
}
type SharedMember={loadToken():Promise<string|null>;onMemberChanged():void};
export interface ConsentJourneyReviewConnection {
  consent:AppHistoryConsentStore;
  openJourney(expected:AppHistoryConsentStatus,signal?:AbortSignal):Promise<ClosedLoopJourneyReviewStore>;
  closeJourney():void;
  isCurrent():boolean;
  invalidate():void;
  subscribeInvalidation(listener:()=>void):()=>void;
}

/** Explicit synthetic composition only. No network default or route registration.
 * Both factories receive one first-bearer loader. Consent is still verified by
 * each server handler; this local lifetime only withholds stale UI/ports. */
export function createConsentJourneyReviewConnection(options:SharedMember & {
  deploymentContext:"synthetic_test";
  createConsent(member:SharedMember):AppHistoryConsentStore;
  createJourney(member:SharedMember):ClosedLoopJourneyReviewStore;
}):ConsentJourneyReviewConnection {
  assertConsentJourneyReviewOnly();
  if(options.deploymentContext!=="synthetic_test")throw new Error("Synthetic composition required");
  let current=true,notified=false,epoch=0,openingEpoch=0,status:AppHistoryConsentStatus|null=null;
  const journeys=new Set<ClosedLoopJourneyReviewStore>(),listeners=new Set<()=>void>();
  const closeOpenedJourneys=()=>{for(const journey of journeys)journey.invalidate();journeys.clear();};
  // Pending opens also belong to the explicitly requested screen. Closing or
  // replacing it withholds late credentials before an account-wide binder can
  // interpret them, without revoking the verified consent or a fresh sibling.
  const closeJourney=()=>{openingEpoch++;closeOpenedJourneys();};
  const suspend=()=>{epoch++;status=null;closeJourney();};
  const invalidate=()=>{if(!current)return;current=false;suspend();for(const fn of [...listeners]){try{fn();}catch{/* continue revocation */}}};
  const changed=()=>{invalidate();if(!notified){notified=true;try{options.onMemberChanged();}catch{/* withhold old responses */}}};
  const gate=()=>{if(!current)throw new AppMemberResponseSessionChanged();try{assertConsentJourneyReviewOnly();}catch(error){invalidate();throw error;}};
  const bound=createBoundMemberResponseSessionLoader(options.loadToken,changed);
  const same=(a:AppHistoryConsentStatus,b:AppHistoryConsentStatus)=>terminalCanonical(a)===terminalCanonical(b);
  const checkAttempt=(id:number,signal?:AbortSignal)=>{signal?.throwIfAborted();gate();if(id!==epoch)throw new Error("Consent attempt retired");};
  const attemptMember=(id:number,signal?:AbortSignal,isConsumerCurrent:()=>boolean=()=>true):SharedMember=>{
    const live=()=>current && id===epoch && !signal?.aborted && isConsumerCurrent();
    const within=(nested:()=>boolean)=>{
      const load=bound.within(()=>live() && nested());
      return async()=>{checkAttempt(id,signal);const value=await load();checkAttempt(id,signal);return value;};
    };
    return {
      loadToken:Object.assign(within(()=>true),{within}),
      onMemberChanged:()=>{if(live())changed();},
    };
  };
  const request=async(choice?:"grant"|"withdraw",expected?:AppHistoryConsentStatus,consumer?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,consumer),signal=consumer?.signal;
    scope.gate();gate();
    const fixed=expected?parseAppHistoryConsentStatus(expected):undefined;
    if(choice && (!fixed || !status || !same(fixed,status) || choice==="grant" && fixed.state!=="not_consented" || choice==="withdraw" && fixed.state==="not_consented"))throw new Error("Read exact consent before choosing");
    // Revocation starts before any asynchronous member or server check. A
    // failed/lost ACK can only recover through a new explicit read.
    suspend();const id=epoch;
    const live=()=>{try{scope.gate();return true;}catch{return false;}};
    const check=()=>{scope.gate();checkAttempt(id,signal);};
    const member=attemptMember(id,signal,live);
    // HTTP adapters also retain their first bearer. Give each attempt its own
    // adapter so an obsolete await cannot retire a later consent read.
    const consent=options.createConsent(member);
    check();
    const value=await scope.wait(()=>runWithMemberResponseSession(member.loadToken,member.onMemberChanged,async()=>{
      check();
      const result=choice && fixed?await consent.choose(choice,fixed,{signal,isCurrent:live}):await consent.read({signal,isCurrent:live});
      check();return result;
    }));
    check();const parsed=parseAppHistoryConsentStatus(value);
    if(choice && (parsed.state!==(choice==="grant"?"consented":"not_consented") || parsed.revision===fixed!.revision))throw new Error("Consent choice not acknowledged");
    status=parsed;return structuredClone(parsed);
  };
  return {
    consent:{read:o=>request(undefined,undefined,o),choose:(choice,expected,o)=>request(choice,expected,o)},
    isCurrent:()=>current,closeJourney,invalidate,
    subscribeInvalidation:fn=>{listeners.add(fn);return()=>{listeners.delete(fn);};},
    openJourney:async(expected,signal)=>{
      signal?.throwIfAborted();gate();const fixed=parseAppHistoryConsentStatus(expected),id=epoch;
      const own=++openingEpoch;
      const consentGate=()=>{checkAttempt(id,signal);if(own!==openingEpoch)throw new Error("Journey opening retired");if(!status || fixed.state!=="consented" || !same(fixed,status))throw new Error("Verified consent required");};
      const opening=attemptMember(id,signal,()=>own===openingEpoch);
      consentGate();await runWithMemberResponseSession(opening.loadToken,opening.onMemberChanged,async()=>{consentGate();});consentGate();
      closeOpenedJourneys();consentGate();
      // A closed journey can share the same consent epoch as its explicit
      // replacement. Its pending credential must not retire that replacement.
      const journey:ClosedLoopJourneyReviewStore=options.createJourney(
        attemptMember(id,undefined,()=>Boolean(journey.isCurrent() && status && same(fixed,status))));
      // An injected factory or revocation observer may synchronously close or
      // replace this open. Dispose only its own uncommitted store in that case.
      try{consentGate();}catch(error){journey.invalidate();throw error;}
      journeys.add(journey);return journey;
    }
  };
}
