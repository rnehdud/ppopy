import AppRoutineResult from "./AppRoutineResult";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import type {MirayRoutineResultStore} from "./mirayRoutineResult";
import { useContext, useCallback, useLayoutEffect, useMemo, useRef, useState } from "react";
import type {ReactNode} from "react";

import type { AppDeletionResult, AppLogoutResult } from "./appSessionTermination";
import type {AccountWithdrawalResult} from "./appAccountWithdrawal";
import type { AppExternalLinkOpener, AppExternalLinkPurpose, AppExternalLinkRouter } from "./appExternalLinks";
import AppSessionControls from "./AppSessionControls";
import AppSubscriptionStatus from "./AppSubscriptionStatus";
import AppQuotaStatus from "./AppQuotaStatus";
import AppStoreKitPurchaseReview from "./AppStoreKitPurchaseReview";
import AppStoreKitSessionReview from "./AppStoreKitSessionReview";
import type {IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";
import type {StoreKitPurchaseReviewPort} from "./storeKitPurchaseReviewContract";
import type {MirayQuotaStatusStore} from "./mirayQuotaStatus";
import FreemiumPlanComparison from "./FreemiumPlanComparison";
import {parseMiraySubscriptionStatus, type MiraySubscriptionStatusStore } from "./miraySubscriptionStatus";
import type { SubscriptionDisplayState } from "./subscriptionPresentation";

const policyLinks: Array<[AppExternalLinkPurpose, string]> = [
  ["service_terms", "서비스 이용약관"],
  ["privacy_policy", "개인정보처리방침"],
  ["support", "고객지원"],
  ["account_deletion", "앱 밖에서 삭제 요청"],
  ["subscription_terms", "무료·플러스 구독 안내"],
];

/** Reuse the canonical wire parser without accepting extra display fields. */
function checkedSubscription(value:unknown) {
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!=="serverVerified|state")throw new Error("Unconfirmed subscription response");
  const record=value as Record<string,unknown>;
  return parseMiraySubscriptionStatus({server_verified:record.serverVerified,state:record.state});
}

export default function AppSettingsScreen({
  subscription,
  subscriptionEnabled = true,
  linkRouter,
  linkOpener,
  retrySubscription,
  subscriptionStatusStore,
  storeKitPurchaseReviewPort,
  storeKitSessionReviewConnection,
  quotaStatusStore,
  routineResultStore,
  historyConsentControl,
  logout,
  withdrawAndDelete,
  withdrawAccount,
  withdrawalTestControl,
  showPlanPreview = false,
  onBack,
}: {
  subscription: {serverVerified: boolean; state?: SubscriptionDisplayState};
  /** Release composition switch; never fabricates a FREE entitlement. */
  subscriptionEnabled?: boolean;
  linkRouter: AppExternalLinkRouter;
  linkOpener: AppExternalLinkOpener;
  retrySubscription?: () => void;
  /** Optional account-bound reader. It cannot perform store purchase or restore. */
  subscriptionStatusStore?: MiraySubscriptionStatusStore;
  /** Explicit isolated review only; no installed SDK/bridge factory. */
  storeKitPurchaseReviewPort?: StoreKitPurchaseReviewPort;
  /** Explicit local connection only. Runtime does not construct it. */
  storeKitSessionReviewConnection?: IOSStoreKitSessionReviewConnection;
  quotaStatusStore?: MirayQuotaStatusStore;
  routineResultStore?: MirayRoutineResultStore;
  historyConsentControl?: ReactNode;
  logout: () => Promise<AppLogoutResult>;
  withdrawAndDelete: () => Promise<AppDeletionResult>;
  withdrawAccount?: () => Promise<AccountWithdrawalResult>;
  withdrawalTestControl?: ReactNode;
  showPlanPreview?: boolean;
  onBack?: () => void;
}) {
  const parentLifetime=useContext(AppSettingsLifetimeContext);
  const screenBinding=useMemo(()=>{
    let live=false;
    return {linkRouter,linkOpener,logout,withdrawAndDelete,withdrawAccount,pendingLink:null as object|null,subscriptionController:null as AbortController|null,
      get live(){return live && (!parentLifetime || parentLifetime.live);},
      set live(value:boolean){live=value;}};
  },[parentLifetime,linkRouter,linkOpener,logout,withdrawAndDelete,withdrawAccount,subscriptionEnabled]);
  const owner=useRef<typeof screenBinding|null>(null);
  const [closed,setClosed]=useState<typeof screenBinding|null>(null);
  const [actionEpoch,setActionEpoch]=useState(0);
  const [linkStatus,setLinkStatus]=useState<{binding:typeof screenBinding;error:boolean;busy:boolean}|null>(null);
  const currentLink=linkStatus?.binding===screenBinding?linkStatus:null;
  const linkError=currentLink?.error??false,linkBusy=currentLink?.busy??false;
  const screenLive=useCallback(()=>screenBinding.live && owner.current===screenBinding,[screenBinding]);
  const updateLink=useCallback((patch:{error?:boolean;busy?:boolean})=>{
    if(screenLive())setLinkStatus(previous=>({binding:screenBinding,error:false,busy:false,...(previous?.binding===screenBinding?previous:{}),...patch}));
  },[screenBinding,screenLive]);
  useLayoutEffect(()=>{
    screenBinding.live=true;owner.current=screenBinding;
    return()=>{screenBinding.live=false;screenBinding.pendingLink=null;screenBinding.subscriptionController?.abort();screenBinding.subscriptionController=null;if(owner.current===screenBinding)owner.current=null;};
  },[screenBinding]);
  const {serverVerified,state}=subscription;
  const fallbackRetry=subscriptionStatusStore ? undefined : retrySubscription;
  const subscriptionBinding=useMemo(()=>({screenBinding,store:subscriptionStatusStore,retry:fallbackRetry,
    subscription:{serverVerified,state},live:false}),[screenBinding,subscriptionStatusStore,fallbackRetry,serverVerified,state]);
  const currentSubscriptionBinding=useRef<typeof subscriptionBinding|null>(null);
  const [resolvedSubscription, setResolvedSubscription] = useState<{
    binding:typeof subscriptionBinding;status:typeof subscription;loading:boolean;
  }|null>(null);
  const subscriptionAttempt = useRef(0);
  const pendingSubscription = useRef<object | null>(null);
  const refreshSubscription = useCallback((automaticRead=false) => {
    if (!subscriptionEnabled || (!automaticRead && !screenBinding.live) || owner.current!==screenBinding || !subscriptionBinding.live || currentSubscriptionBinding.current!==subscriptionBinding) return;
    const store=subscriptionBinding.store;
    if (!store) {
      subscriptionBinding.retry?.();
      return;
    }
    if (pendingSubscription.current) return;
    const attempt = ++subscriptionAttempt.current;
    const controller=new AbortController();screenBinding.subscriptionController=controller;
    const pending = {}; pendingSubscription.current = pending;
    const isCurrent=()=>screenBinding.live && owner.current===screenBinding && subscriptionBinding.live && currentSubscriptionBinding.current===subscriptionBinding && attempt===subscriptionAttempt.current;
    setResolvedSubscription({binding:subscriptionBinding,status:{serverVerified:false},loading:true});
    // An injected reader may throw before returning its promise. Treat that as
    // an unknown display state so the user can explicitly retry.
    const operation=async()=>{if(!isCurrent())return null;return checkedSubscription(await store.read({signal:controller.signal,isCurrent}));};
    void Promise.resolve().then(operation).then(
      next => { if (isCurrent()) setResolvedSubscription({binding:subscriptionBinding,status:next ?? {serverVerified:false},loading:false}); },
      () => { if (isCurrent()) setResolvedSubscription({binding:subscriptionBinding,status:{serverVerified:false},loading:false}); },
    ).finally(() => {
      if(screenBinding.subscriptionController===controller)screenBinding.subscriptionController=null;
      if (pendingSubscription.current === pending) {
        pendingSubscription.current = null;
      }
    });
  }, [screenBinding,subscriptionBinding,subscriptionEnabled]);
  useLayoutEffect(() => {
    subscriptionBinding.live=true;currentSubscriptionBinding.current=subscriptionBinding;
    subscriptionAttempt.current += 1;
    pendingSubscription.current = null;
    setResolvedSubscription(null);
    // Reserve the existing mount read before the parent's layout activation.
    // Dispatch still checks the committed parent and current attempt.
    if (subscriptionBinding.store) refreshSubscription(true);
    return () => {
      subscriptionBinding.live=false;
      screenBinding.subscriptionController?.abort();screenBinding.subscriptionController=null;
      if(currentSubscriptionBinding.current===subscriptionBinding){
        currentSubscriptionBinding.current=null;
        subscriptionAttempt.current += 1;
        pendingSubscription.current = null;
      }
    };
    // The injected store identity is the connection contract. Values returned
    // from it are deliberately not retained after a connection changes.
  }, [screenBinding,subscriptionBinding,refreshSubscription]);
  // A response belongs to one committed screen/connection lifetime.
  const currentSubscription=resolvedSubscription?.binding===subscriptionBinding?resolvedSubscription:null;
  const displayedSubscription = subscriptionStatusStore
    ? currentSubscription?.status ?? {serverVerified:false}
    : subscriptionBinding.subscription;
  const displayLoading = Boolean(subscriptionStatusStore && (!currentSubscription || currentSubscription.loading));
  const holdSubscriptionForStore=useCallback(()=>{
    if(!screenLive() || !subscriptionBinding.live || currentSubscriptionBinding.current!==subscriptionBinding)return;
    subscriptionAttempt.current+=1;pendingSubscription.current=null;
    screenBinding.subscriptionController?.abort();screenBinding.subscriptionController=null;
    setResolvedSubscription({binding:subscriptionBinding,status:{serverVerified:false},loading:false});
  },[screenLive,screenBinding,subscriptionBinding]);

  const frame=useMemo(()=>({screenBinding,subscriptionBinding,currentSubscription,currentLink,actionEpoch,closed}),[screenBinding,subscriptionBinding,currentSubscription,currentLink,actionEpoch,closed]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const frameLive=useCallback(()=>screenLive() && closed!==screenBinding && currentFrame.current===frame,[screenLive,closed,screenBinding,frame]);
  const consume=useCallback(()=>{if(currentFrame.current===frame)currentFrame.current=null;},[frame]);
  const retryCurrent=useCallback(()=>{if(!frameLive() || pendingSubscription.current)return;consume();setActionEpoch(value=>value+1);refreshSubscription();},[frameLive,consume,refreshSubscription]);
  const open=useCallback(async(purpose:AppExternalLinkPurpose)=>{
    if(!frameLive() || screenBinding.pendingLink || !linkRouter.configured(purpose)
      || (!subscriptionEnabled && (purpose === "manage_subscription" || purpose === "subscription_terms")))return;
    const attempt={};screenBinding.pendingLink=attempt;consume();updateLink({error:false,busy:true});
    const current=()=>screenLive() && screenBinding.pendingLink===attempt;
    try {
      await Promise.resolve();if(!current())return;
      const result=await linkRouter.open(purpose,linkOpener);
      if(current())updateLink({error:result?.state!=="opened"});
    }catch{if(current())updateLink({error:true});}
    finally{if(screenBinding.pendingLink===attempt){screenBinding.pendingLink=null;updateLink({busy:false});}}
  },[frameLive,screenBinding,linkRouter,linkOpener,consume,updateLink,screenLive,subscriptionEnabled]);
  const manage=useCallback(()=>void open("manage_subscription"),[open]);
  const backBinding=useMemo(()=>({screenBinding,onBack}),[screenBinding,onBack]);
  const currentBack=useRef<typeof backBinding|null>(null);
  useLayoutEffect(()=>{currentBack.current=backBinding;return()=>{if(currentBack.current===backBinding)currentBack.current=null;};},[backBinding]);
  const back=()=>{
    // Navigation may cancel an action queued by this same committed screen.
    if(!screenLive() || closed===screenBinding || currentBack.current!==backBinding || !onBack)return;
    consume();screenBinding.live=false;screenBinding.pendingLink=null;screenBinding.subscriptionController?.abort();screenBinding.subscriptionController=null;owner.current=null;setClosed(screenBinding);onBack();
  };
  if(closed===screenBinding)return <main className="app-settings-screen"><p>설정 화면을 닫았어요.</p></main>;

  return <AppSettingsLifetimeContext.Provider value={screenBinding}><main className="app-settings-screen">
    {onBack && <nav className="app-settings-nav" aria-label="설정 탐색"><button type="button" onClick={back}><span aria-hidden="true">‹</span> 루틴으로</button></nav>}
    <header><p id="app-settings-context" aria-hidden="true">설정</p><h1 aria-describedby="app-settings-context">내 이용 상태를 관리해요</h1><span>{subscriptionEnabled ? "구독, 도움말과 데이터 삭제는 서로 별도로 처리됩니다." : "이용 횟수와 내 기록을 확인하고 계정을 관리해요."}</span></header>
    {subscriptionEnabled && <><AppSubscriptionStatus
      serverVerified={displayedSubscription.serverVerified}
      state={displayedSubscription.state}
      loading={displayLoading}
      onRetry={subscriptionStatusStore || retrySubscription ? retryCurrent : undefined}
      onManage={linkRouter.configured("manage_subscription") ? manage : undefined}
    />
    {subscriptionStatusStore && displayedSubscription.serverVerified && !displayLoading && <button className="app-subscription-refresh" type="button" onClick={retryCurrent}>상태 다시 확인</button>}
    {storeKitSessionReviewConnection && !storeKitPurchaseReviewPort && subscriptionStatusStore && <AppStoreKitSessionReview connection={storeKitSessionReviewConnection} onInteractionStart={holdSubscriptionForStore}/>}
    {storeKitPurchaseReviewPort && !storeKitSessionReviewConnection && subscriptionStatusStore && <AppStoreKitPurchaseReview port={storeKitPurchaseReviewPort} onInteractionStart={holdSubscriptionForStore}/>}
    </>}
    {quotaStatusStore && <AppQuotaStatus store={quotaStatusStore} lifetime={screenBinding} subscriptionEnabled={subscriptionEnabled}/>}
    {routineResultStore && <AppRoutineResult store={routineResultStore}/>}
    {subscriptionEnabled && showPlanPreview && <FreemiumPlanComparison />}
    <section className="app-settings-links" aria-labelledby="app-settings-links-title">
      <h2 id="app-settings-links-title">도움과 정책</h2>
      {policyLinks.filter(([purpose]) => linkRouter.configured(purpose) && (subscriptionEnabled || purpose !== "subscription_terms")).map(([purpose, label]) =>
        <button type="button" key={purpose} disabled={linkBusy} onClick={() => void open(purpose)}>{label}<span aria-hidden="true">›</span></button>)}
      {linkError && <p role="alert">페이지를 열지 못했습니다. 잠시 뒤 다시 시도해 주세요.</p>}
    </section>
    <AppSessionControls logout={logout} withdrawAndDelete={withdrawAndDelete} withdrawAccount={withdrawAccount} lifetime={screenBinding} subscriptionEnabled={subscriptionEnabled} withdrawalTestControl={withdrawalTestControl} dataConsentControl={historyConsentControl}/>
  </main></AppSettingsLifetimeContext.Provider>;
}
