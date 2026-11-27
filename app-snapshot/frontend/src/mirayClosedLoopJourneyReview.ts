import config from "../../skin_engine/config/miray_closed_loop_journey_ui_review.json";
import {AppMemberResponseSessionChanged,createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {createAccountEntryHttpReviewStore} from "./mirayClosedLoopEntryHttpReview";
import {createEntryIntakeHttpReviewStore} from "./mirayClosedLoopEntryIntakeHttpReview";
import {createAccountEpisodeHttpReviewStore} from "./mirayClosedLoopEpisodeHttpReview";
import {createNextDecisionHttpReviewStore} from "./mirayClosedLoopNextHttpReview";
import {createNextPrecheckHttpReviewStore} from "./mirayClosedLoopNextPrecheckHttpReview";
import {createFrequencyCorrectionHttpReviewStore} from "./mirayClosedLoopFrequencyHttpReview";
import {createTerminalFreshHttpReviewStore} from "./mirayClosedLoopTerminalFreshHttpReview";
import {createTerminalPromotionHttpReviewStore} from "./mirayClosedLoopTerminalPromotionHttpReview";
import {parseClosedLoopEpisode,type ClosedLoopReviewStore} from "./mirayClosedLoop";
import type {ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";
import {nextRef,type NextDecisionContext} from "./mirayClosedLoopNext";
import {assertTerminalUiReviewOnly,terminalCanonical,type TerminalUiReviewStore} from "./mirayClosedLoopTerminalUiReview";
import type {TerminalFreshView} from "./mirayClosedLoopTerminalFreshReview";

const baseline=terminalCanonical(config);
export function assertJourneyReviewOnly(){
  assertTerminalUiReviewOnly();
  if(terminalCanonical(config)!==baseline || config.deployment_context!=="synthetic_test" || config.evaluation_scope!=="synthetic_local_review_only" ||
    [config.enabled,config.registered,config.real_user_question_exposure_enabled,config.automatic_retry,config.automatic_poll,config.draft_storage_enabled,config.automatic_dispatch,config.navigation_confirms_actual_use].some(v=>v!==false) ||
    !config.shared_member_lifetime_required || !config.explicit_navigation_required || config.question_profile!=="routine_state_and_safety" || config.core_question_count!==2 || config.conditional_discomfort_detail_count!==1)throw new Error("Unapproved journey review");
}
export interface ClosedLoopJourneyReviewStore {
  entry:ClosedLoopEntryReviewStore;
  episode(expectedDecisionRef?:string):ClosedLoopReviewStore;
  terminal(context:NextDecisionContext):TerminalUiReviewStore;
  assertCurrent(signal?:AbortSignal):Promise<void>;
  isCurrent():boolean;
  subscribeInvalidation(listener:()=>void):()=>void;
  invalidate():void;
}

/** All panels share one first bearer. Factories stay explicitly injected and
 * loopback only; replacing a login or ending consent requires a NEW connection.
 * Navigation checks credentials but never creates an event or calculates. */
export function createClosedLoopJourneyHttpReviewStore(options:Parameters<typeof createAccountEntryHttpReviewStore>[0]):ClosedLoopJourneyReviewStore {
  assertJourneyReviewOnly();let current=true,notified=false;
  const listeners=new Set<()=>void>();
  const invalidate=()=>{if(!current)return;current=false;for(const listener of [...listeners]){try{listener();}catch{/* revocation must continue */}}};
  const changed=()=>{invalidate();if(!notified){notified=true;try{options.onMemberChanged();}catch{/* never release old responses */}}};
  const gate=()=>{if(!current)throw new AppMemberResponseSessionChanged();try{assertJourneyReviewOnly();}catch(error){invalidate();throw error;}};
  const bound=createBoundMemberResponseSessionLoader(options.loadToken,changed);
  const within=(live:()=>boolean)=>{
    const load=bound.within(()=>current && live());
    return async()=>{gate();const token=await load();gate();return token;};
  };
  const loadToken=Object.assign(within(()=>true),{within});
  const shared={...options,loadToken,onMemberChanged:changed};
  const assertCurrent=async(signal?:AbortSignal)=>{
    signal?.throwIfAborted();gate();
    await runWithMemberResponseSession(loadToken.within(()=>!signal?.aborted),changed,async()=>{signal?.throwIfAborted();gate();});
    signal?.throwIfAborted();gate();
  };
  const entry={...createAccountEntryHttpReviewStore(shared),intake:createEntryIntakeHttpReviewStore(shared)};
  return {
    entry,assertCurrent,isCurrent:()=>current,subscribeInvalidation:listener=>{listeners.add(listener);return()=>{listeners.delete(listener);};},invalidate,
    episode:expectedDecisionRef=>{
      gate();if(expectedDecisionRef!==undefined)nextRef(expectedDecisionRef);
      const store=createAccountEpisodeHttpReviewStore(shared);
      let known:string|undefined;
      const requireEpisode=(ref:string)=>{gate();if(!known || ref!==known || expectedDecisionRef && ref!==expectedDecisionRef)throw new Error("Original episode must be read before writing");};
      return {...store,nextDecision:{...createNextDecisionHttpReviewStore(shared),intake:createNextPrecheckHttpReviewStore(shared)},frequencyCorrections:createFrequencyCorrectionHttpReviewStore(shared),
        read:async o=>{const value=parseClosedLoopEpisode(await store.read(o));if(expectedDecisionRef && value.decision_ref!==expectedDecisionRef || known && value.decision_ref!==known){invalidate();throw new Error("Current episode differs from handoff");}known=value.decision_ref;return value;},
        confirmActual:(r,o)=>{requireEpisode(r.decision_ref);return store.confirmActual(r,o);},saveFollowup:(r,o)=>{requireEpisode(r.decision_ref);return store.saveFollowup(r,o);}};
    },
    terminal:context=>{
      gate();const fixed=structuredClone(context);
      [fixed.next_ref,fixed.parent_decision_ref,fixed.snapshot_ref].forEach(nextRef);
      if(new Set([fixed.next_ref,fixed.parent_decision_ref,fixed.snapshot_ref]).size!==3 || !Number.isSafeInteger(fixed.portfolio_revision) || fixed.portfolio_revision<0)throw new Error("Exact terminal handoff required");
      const fresh=createTerminalFreshHttpReviewStore({...shared,terminalNextRef:fixed.next_ref});
      const promotion=createTerminalPromotionHttpReviewStore({...shared,terminalNextRef:fixed.next_ref});
      let retained:TerminalFreshView|null=null;
      const match=(value:TerminalFreshView)=>{
        gate();if(value.context.terminal_next_ref!==fixed.next_ref || value.context.parent_decision_ref!==fixed.parent_decision_ref || value.context.previous_snapshot_ref!==fixed.snapshot_ref || value.context.portfolio_revision!==fixed.portfolio_revision){invalidate();throw new Error("Terminal handoff changed");}retained=value;return value;
      };
      const matchPromotion=(value:Awaited<ReturnType<typeof promotion.read>>)=>{
        gate();if(!retained || !retained.stored || value.context.fresh_ref!==retained.context.fresh_ref || value.context.parent_decision_ref!==fixed.parent_decision_ref || value.context.portfolio_revision!==fixed.portfolio_revision || value.context.snapshot_ref===fixed.snapshot_ref){invalidate();throw new Error("Read exact retained input before promotion");}return value;
      };
      return {fresh:{...fresh,read:async o=>match(await fresh.read(o)),precheck:async(o,p)=>match(await fresh.precheck(o,p)),save:(o,a,p)=>{gate();if(!retained)throw new Error("Read exact new input before save");return fresh.save(o,a,p);}},
        promotion:{read:async o=>{gate();if(!retained?.stored)throw new Error("Read retained input first");return matchPromotion(await promotion.read(o));},promote:async o=>matchPromotion(await promotion.promote(o)),resume:async o=>matchPromotion(await promotion.resume(o))}};
    }
  };
}
