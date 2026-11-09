import {assertNextReviewOnly,nextRef,parseNextDecisionView,type NextDecisionReviewStore} from "./mirayClosedLoopNext";
import type {MirayRoutineResultStore} from "./mirayRoutineResult";
import {parseClosedLoopEpisode,type ClosedLoopReviewStore} from "./mirayClosedLoop";
import {assertLoopEntryReviewOnly,parseLoopEntryView,validateLoopEntryRequest,type ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";
import {parseProductChangeAck,parseProductChangeView} from "./mirayClosedLoopTransitions";
import type {AppHistoryConsentStore} from "./appHistoryConsent";
import type {MirayPortfolioStore} from "./mirayPortfolio";
import type {MiraySavedCandidatesStore} from "./miraySavedCandidates";
import type {MiraySkinStateStore} from "./miraySkinState";
import type {MiraySubscriptionStatusStore} from "./miraySubscriptionStatus";
import type {MirayQuotaStatusStore} from "./mirayQuotaStatus";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {assertOriginalEntryResumeReviewOnly} from "./mirayClosedLoopAdmission";
import {assertAccountEntrySelectorReviewOnly} from "./mirayClosedLoopEntrySelector";
import {assertIntakeReviewOnly,nextIntakeRef,parseIntakeAnswers,parseIntakeView,type NextIntakeReviewStore} from "./mirayClosedLoopIntake";

import {assertEntryIntakeReviewOnly,parseEntryIntakeView,type EntryIntakeReviewStore} from "./mirayClosedLoopEntryIntake";
import {assertFrequencyCorrectionReviewOnly,parseFrequencyCorrectionAck,parseFrequencyCorrectionView,validateFrequencyCorrectionRequest,type FrequencyCorrectionReviewStore} from "./mirayClosedLoopFrequency";
import {assertNextPrecheckReviewOnly,parseNextPrecheckView} from "./mirayClosedLoopNextPrecheck";
import {assertJourneyReviewOnly,type ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";

type LoadToken=()=>Promise<string|null>;
type Notify=()=>void;

/** The shell's original bearer and separate consent own every journey page. */
export function bindMemberClosedLoopJourneyReviewStore(store:ClosedLoopJourneyReviewStore,load:LoadToken,notify:Notify):ClosedLoopJourneyReviewStore {
  const changed=()=>{store.invalidate();notify();};
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const gate=()=>{assertJourneyReviewOnly();if(!store.isCurrent())throw new Error("Journey retired");};
  const run=<T,>(operation:()=>Promise<T>,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();gate();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();gate();const value=await scope.wait(operation);scope.gate();gate();return value;
    }));
  };
  return {
    entry:bindMemberClosedLoopEntryReviewStore(store.entry,bound,changed),
    episode:ref=>{gate();return bindMemberClosedLoopReviewStore(store.episode(ref),bound,changed);},
    terminal:context=>{
      gate();const child=store.terminal(structuredClone(context));
      return {fresh:{read:o=>run(()=>child.fresh.read(o),o),precheck:(v,o)=>{const frozen=structuredClone(v);return run(()=>child.fresh.precheck(frozen,o),o);},
        save:(v,a,o)=>{const observation=structuredClone(v),answers=structuredClone(a);return run(()=>child.fresh.save(observation,answers,o),o);}},
      promotion:{read:o=>run(()=>child.promotion.read(o),o),promote:o=>run(()=>child.promotion.promote(o),o),
        resume:o=>run(()=>child.promotion.resume(o),o)}};
    },
    assertCurrent:signal=>run(()=>store.assertCurrent(signal),{signal}),
    isCurrent:()=>store.isCurrent(),subscribeInvalidation:listener=>store.subscribeInvalidation(listener),invalidate:()=>store.invalidate(),
  };
}

export function bindMemberFrequencyCorrectionReviewStore(store:FrequencyCorrectionReviewStore,load:LoadToken,changed:Notify):FrequencyCorrectionReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(operation:()=>Promise<unknown>,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);
    scope.gate();assertFrequencyCorrectionReviewOnly();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertFrequencyCorrectionReviewOnly();const value=await scope.wait(operation);
      scope.gate();assertFrequencyCorrectionReviewOnly();return value;
    }));
  };
  return {read:o=>run(async()=>parseFrequencyCorrectionView(await store.read(o)),o),confirm:(r,o)=>{
    const frozen=validateFrequencyCorrectionRequest(r);return run(async()=>parseFrequencyCorrectionAck(await store.confirm(structuredClone(frozen),o),frozen),o);
  }};
}

export function bindMemberNextIntakeReviewStore(store:NextIntakeReviewStore,load:LoadToken,changed:Notify):NextIntakeReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(operation:()=>Promise<unknown>,ref:string|null,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();assertIntakeReviewOnly();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertIntakeReviewOnly();const value=parseIntakeView(await scope.wait(operation));
      scope.gate();assertIntakeReviewOnly();
      if(ref!==null && value.context.next_ref!==ref)throw new Error("Input correlation changed");return value;
    }));
  };
  return {...(store.precheck?{precheck:(o?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,o);scope.gate();assertNextPrecheckReviewOnly();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertNextPrecheckReviewOnly();const value=parseNextPrecheckView(await scope.wait(()=>store.precheck!(o)));
      scope.gate();assertNextPrecheckReviewOnly();return value;
    }));
  }}:{}),read:o=>run(()=>store.read(o),null,o),save:(r,a,o)=>{
    nextIntakeRef(r);const frozen=parseIntakeAnswers(a);return run(()=>store.save(r,frozen,o),r,o);
  }};
}

export function bindMemberEntryIntakeReviewStore(store:EntryIntakeReviewStore,load:LoadToken,changed:Notify):EntryIntakeReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(operation:()=>Promise<unknown>,mode:"initial"|"fresh"|null,ref:string|null,original:string|null,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();assertEntryIntakeReviewOnly();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertEntryIntakeReviewOnly();const value=parseEntryIntakeView(await scope.wait(operation));
      scope.gate();assertEntryIntakeReviewOnly();
      if((mode!==null && value.context.mode!==mode) || (ref!==null && value.context.entry_ref!==ref) || value.context.entry_ref===original)throw new Error("Input target changed");return value;
    }));
  };
  return {read:o=>run(()=>store.read(o),"initial",null,null,o),readFresh:(r,o)=>{
    nextRef(r);return run(()=>store.readFresh(r,o),"fresh",null,r,o);
  },save:(r,a,o)=>{nextRef(r);const frozen=parseIntakeAnswers(a);return run(()=>store.save(r,structuredClone(frozen),o),null,r,null,o);}};
}

export function bindMemberClosedLoopEntryReviewStore(store:ClosedLoopEntryReviewStore,load:LoadToken,changed:Notify):ClosedLoopEntryReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(operation:()=>Promise<unknown>,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();assertLoopEntryReviewOnly();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertLoopEntryReviewOnly();const result=parseLoopEntryView(await scope.wait(operation));scope.gate();assertLoopEntryReviewOnly();return result;
    }));
  };
  return {
    ...(store.intake?{intake:bindMemberEntryIntakeReviewStore(store.intake,bound,changed)}:{}),
    ...(store.startFresh?{startFresh:(entryRef:string,options?:MemberStatusReadOptions)=>{
      assertAccountEntrySelectorReviewOnly(entryRef);
      return run(async()=>{assertAccountEntrySelectorReviewOnly(entryRef);const value=await store.startFresh!(entryRef,options);assertAccountEntrySelectorReviewOnly(entryRef);return value;},options);
    }}:{}),
    ...(store.resume?{resume:(entryRef:string,options?:MemberStatusReadOptions)=>{
      assertOriginalEntryResumeReviewOnly(entryRef);
      return run(async()=>{assertOriginalEntryResumeReviewOnly(entryRef);const value=await store.resume!(entryRef,options);assertOriginalEntryResumeReviewOnly(entryRef);return value;},options);
    }}:{}),
    read:options=>run(()=>store.read(options),options),
    recover:(entryRef,options)=>run(()=>store.recover(entryRef,options),options),
    submit:(request,options)=>{validateLoopEntryRequest(request);const frozen=structuredClone(request);return run(()=>store.submit(frozen,options),options);},
  };
}

export function bindMemberNextDecisionReviewStore(store:NextDecisionReviewStore,load:LoadToken,changed:Notify):NextDecisionReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(action:"read"|"recover"|"submit"|"resume",ref:string|null,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();assertNextReviewOnly();if(ref!==null)nextRef(ref);
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertNextReviewOnly();
      const value=parseNextDecisionView(await scope.wait(()=>action==="read"?store.read(options):store[action](ref!,options)));
      scope.gate();assertNextReviewOnly();
      if(ref!==null && value.context?.next_ref!==ref)throw new Error("Next correlation changed");return value;
    }));
  };
  return {...(store.intake?{intake:bindMemberNextIntakeReviewStore(store.intake,bound,changed)}:{}),read:o=>run("read",null,o),recover:(r,o)=>run("recover",r,o),submit:(r,o)=>run("submit",r,o),resume:(r,o)=>run("resume",r,o)};
}

export function bindMemberClosedLoopReviewStore(store:ClosedLoopReviewStore,load:LoadToken,changed:Notify):ClosedLoopReviewStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=(operation:()=>Promise<unknown>,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);
    scope.gate();
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      const result=parseClosedLoopEpisode(await scope.wait(operation));
      scope.gate();
      return result;
    }));
  };
  return {
    ...(store.frequencyCorrections?{frequencyCorrections:bindMemberFrequencyCorrectionReviewStore(store.frequencyCorrections,bound,changed)}:{}),
    ...(store.nextDecision?{nextDecision:bindMemberNextDecisionReviewStore(store.nextDecision,bound,changed)}:{}),
    ...(store.productChanges?{productChanges:{
      read:(options?:MemberStatusReadOptions)=>{
        const scope=memberStatusReadScope(bound,options);scope.gate();
        return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(async()=>parseProductChangeView(await store.productChanges!.read(options)))));
      },
      confirm:(request:Parameters<NonNullable<ClosedLoopReviewStore["productChanges"]>["confirm"]>[0],options?:MemberStatusReadOptions)=>{
        const scope=memberStatusReadScope(bound,options);scope.gate();const frozen=structuredClone(request);
        return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(async()=>parseProductChangeAck(await store.productChanges!.confirm(frozen,options)))));
      },
    }}:{}),
    read:options=>run(()=>store.read(options),options),
    confirmActual:(request,options)=>{const frozen=structuredClone(request);return run(()=>store.confirmActual(frozen,options),options);},
    saveFollowup:(request,options)=>{const frozen=structuredClone(request);return run(()=>store.saveFollowup(frozen,options),options);},
  };
}

export function bindMemberHistoryConsentStore(store:AppHistoryConsentStore,load:LoadToken,changed:Notify):AppHistoryConsentStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  return {
    read:options=>{
      const scope=memberStatusReadScope(bound,options);
      return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>store.read(options))));
    },
    choose:(choice,expected,options)=>{
      const snapshot=structuredClone(expected);
      const scope=memberStatusReadScope(bound,options);
      return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>store.choose(choice,snapshot,options))));
    },
  };
}

/** Bind injected member stores to the Shell's existing bearer lifetime. */
export function bindMemberPortfolioStore(store:MirayPortfolioStore,load:LoadToken,changed:Notify):MirayPortfolioStore {
  return {
    read:()=>runWithMemberResponseSession(load,changed,()=>store.read()),
    save:(portfolio,revision)=>{
      const snapshot=structuredClone(portfolio);
      return runWithMemberResponseSession(load,changed,()=>store.save(snapshot,revision));
    },
  };
}

export function bindMemberSavedCandidatesStore(store:MiraySavedCandidatesStore,load:LoadToken,changed:Notify):MiraySavedCandidatesStore {
  return {
    read:()=>runWithMemberResponseSession(load,changed,()=>store.read()),
    save:(candidates,revision)=>{
      const snapshot=structuredClone(candidates);
      return runWithMemberResponseSession(load,changed,()=>store.save(snapshot,revision));
    },
  };
}

export function bindMemberSkinStateStore(store:MiraySkinStateStore,load:LoadToken,changed:Notify):MiraySkinStateStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  return {
    save:async(state,options)=>{
      const scope=memberStatusReadScope(bound,options);
      scope.gate();
      const snapshot=structuredClone(state);
      return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>store.save(snapshot,options))));
    },
  };
}

export function bindMemberSubscriptionStatusStore(store:MiraySubscriptionStatusStore,load:LoadToken,changed:Notify):MiraySubscriptionStatusStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  return {read:o=>{
    const scope=memberStatusReadScope(bound,o);
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>o?store.read(o):store.read())));
  }};
}

export function bindMemberQuotaStatusStore(store:MirayQuotaStatusStore,load:LoadToken,changed:Notify):MirayQuotaStatusStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  return {read:o=>{
    const scope=memberStatusReadScope(bound,o);
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>o?store.read(o):store.read())));
  }};
}

export function bindMemberRoutineResultStore(store:MirayRoutineResultStore,load:LoadToken,changed:Notify):MirayRoutineResultStore {
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  return {read:o=>{
    const scope=memberStatusReadScope(bound,o);
    return scope.wait(()=>runWithMemberResponseSession(scope.load,changed,()=>scope.wait(()=>o?store.read(o):store.read())));
  }};
}
