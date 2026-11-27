import type {KbAppPort} from './KbOnboarding';
import {atLoginStartStage} from "./loginStartStage";
import type {OriginalPublicLoopFactory} from "./publicOriginalLoop";
import type {OriginalLoopTestFactory} from "./mirayOriginalLoopTest";
import {useMemberConsumerTransport} from "./useMemberConsumerTransport";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import {bindMemberClosedLoopReviewStore,bindMemberClosedLoopEntryReviewStore,bindMemberClosedLoopJourneyReviewStore} from "./appMemberStoreBinding";
import type {ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";
import type {ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";
import type {ClosedLoopReviewStore} from "./mirayClosedLoop";
import {createHttpMirayRoutineResultStore,type MirayRoutineResultStore} from "./mirayRoutineResult";
import AppHistoryConsentPanel from "./AppHistoryConsentPanel";
import {createHttpAppHistoryConsentStore,type AppHistoryConsentStore} from "./appHistoryConsent";
import {useAppHistoryConsent} from "./useAppHistoryConsent";
import {bindMemberHistoryConsentStore} from "./appMemberStoreBinding";
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import type {ReactNode} from "react";
import {abortMemberProductSearches,runMemberProductSearch} from "./appMemberSearch";
import type {ProductSearchOptions} from "./careApi";

import AccountStartScreen from "./AccountStartScreen";
import AppPrototype from "./AppPrototype";
import AppSettingsScreen from "./AppSettingsScreen";
import {bindMemberStoreKitPurchaseReviewPort,type StoreKitPurchaseReviewPort} from "./storeKitPurchaseReviewContract";
import {bindMemberStoreKitSessionConnectionLocal} from "./appStoreKitSessionBindingLocal";
import type {IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";
import type {StoreKitSessionReviewFactory} from "./appStoreKitSessionFactoryLocal";
import {useStoreKitSessionFactoryLocal} from "./useStoreKitSessionFactoryLocal";
import MirayWorkspace from "./MirayWorkspace";
import type {CandidateComparisonReader} from "./candidateComparisonModel";
import navigationConfig from "../../skin_engine/config/miray_navigation.json";
import releaseScope from "../../skin_engine/config/app_release_scope.json";
import {createHttpMirayPortfolioStore, type MirayPortfolioStore} from "./mirayPortfolio";
import {createHttpMiraySavedCandidatesStore, type MiraySavedCandidatesStore} from "./miraySavedCandidates";
import {createHttpMiraySkinStateStore, type MiraySkinStateStore} from "./miraySkinState";
import {createHttpMiraySubscriptionStatusStore, type MiraySubscriptionStatusStore} from "./miraySubscriptionStatus";
import {createHttpMirayQuotaStatusStore,type MirayQuotaStatusStore} from "./mirayQuotaStatus";
import type {HomeTask} from "./mirayNavigation";
import {logoutAppSession, type AppDeletionResult, type AppLogoutResult} from "./appSessionTermination";
import { createAppExternalLinkRouter, type AppExternalLinkOpener } from "./appExternalLinks";
import {AppAuthenticationError, createHttpAppSessionRevoker, restoreAuthenticatedSession, saveAuthenticatedSession, type AppAuthenticationSession, type AppSessionVerifier} from "./appAuthentication";
import privacy from "../../skin_engine/config/beta_privacy.json";
import {appLoginNotices} from "./appLoginNotices";
import {createHttpAppProtectionSessionClient} from "./appProtectionSession";
import {completeSignupHistoryConsent,signupHistoryBinding} from "./appSignupHistory";
import historySignupConfig from "../../skin_engine/config/app_history_consent.json";
import {createHttpAppGoogleLoginClient} from "./appGoogleLogin";
import {createHttpAppAppleLoginClient} from "./appAppleLogin";
import type {AppleLoginAuthorization} from "./iosAppleIdentity";
import {createHttpAppKakaoLoginClient} from "./appKakaoLogin";
import {createHttpAppNaverLoginClient} from "./appNaverLogin";
import {createHttpAppEmailOtpClient} from "./appEmailOtp";
import {clearSessionCredential,type SessionVault} from "./appSessionVault";
import type {CareApiClient} from "./careApi";
import {bindAccountWithdrawalClient,confirmedAccountWithdrawal,parseAccountWithdrawalAcceptance,requestAppAccountWithdrawal,
  type AccountWithdrawalClient,type AccountWithdrawalResult} from "./appAccountWithdrawal";

import {AppMemberResponseSessionChanged,createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {bindMemberPortfolioStore,bindMemberSavedCandidatesStore,bindMemberSkinStateStore,bindMemberSubscriptionStatusStore,bindMemberQuotaStatusStore,bindMemberRoutineResultStore} from "./appMemberStoreBinding";

type Screen = "account" | "routine" | "settings";
const unavailableDeletion=async ():Promise<AppDeletionResult>=>({state:"retryable_error"});

export default function AppLaunchShell({
  kbAppPort,
  initialAuthenticated = false,
  connectionsEnabled = false,
  availableProviders,
  emailEnabled,
  availabilityNotice,
  allowOwnerTestSession = false,
  newNavigationEnabled = navigationConfig.enabled,
  portfolioStore,
  memberCareClient,
  memberCareClientFactory,
  portfolioApiBaseUrl,
  allowedPortfolioApiBaseUrls,
  savedCandidateStore,
  candidateComparisonReader,
  closedLoopReviewStore,
  closedLoopEntryReviewStore,
  closedLoopJourneyReviewFactory,
  originalLoopTestFactory,
  publicLoopFactory,
  savedCandidatesApiBaseUrl,
  allowedSavedCandidatesApiBaseUrls,
  fetcher = fetch,
  skinStateEnabled = navigationConfig.checkin_enabled,
  replenishmentEnabled = navigationConfig.replenishment_enabled,
  sensitiveConsentVerified = false,
  historyStorageConsented = false,
  historyConsentStore,
  historyConsentApiBaseUrl,
  allowedHistoryConsentApiBaseUrls,
  skinStateStore,
  skinStateApiBaseUrl,
  allowedSkinStateApiBaseUrls,
  subscriptionEnabled = releaseScope.paid_subscription_enabled,
  subscriptionStatusStore,
  storeKitPurchaseReviewPort,
  storeKitSessionReviewConnection,
  storeKitSessionReviewFactory,
  subscriptionStatusApiBaseUrl,
  allowedSubscriptionStatusApiBaseUrls,
  quotaStatusStore,
  routineResultStore,
  routineResultApiBaseUrl,
  allowedRoutineResultApiBaseUrls,
  quotaStatusApiBaseUrl,
  allowedQuotaStatusApiBaseUrls,
  homeTasks,
  sessionVault,
  sessionVerifier,
  sessionApiBaseUrl,
  allowedSessionApiBaseUrls,
  protectionApiBaseUrl,
  allowedProtectionApiBaseUrls,
  googleApiBaseUrl,
  allowedGoogleApiBaseUrls,
  getGoogleIdToken,
  getGoogleLoginAuthorization,
  appleApiBaseUrl,
  allowedAppleApiBaseUrls,
  getAppleIdToken,
  getAppleLoginAuthorization,
  kakaoApiBaseUrl,
  allowedKakaoApiBaseUrls,
  getKakaoAccessToken,
  requireKakaoSDKOwnerProof = false,
  naverApiBaseUrl,
  allowedNaverApiBaseUrls,
  getNaverAccessToken,
  emailApiBaseUrl,
  allowedEmailApiBaseUrls,
  logout,
  withdrawAndDelete = unavailableDeletion,
  withdrawAccount,
  withdrawAccountClient,
  withdrawalTestControl,
}: {
  kbAppPort?: Omit<KbAppPort,"onClose">;
  initialAuthenticated?: boolean;
  connectionsEnabled?: boolean;
  availableProviders?: readonly ("apple" | "google" | "naver" | "kakao")[];
  emailEnabled?: boolean;
  availabilityNotice?: string;
  allowOwnerTestSession?: boolean;
  newNavigationEnabled?: boolean;
  portfolioStore?: MirayPortfolioStore;
  /** Verified member-facing product and analysis routes. Fixtures belong only to an explicit owner preview. */
  memberCareClient?: Pick<CareApiClient, "searchProducts"> & Partial<Pick<CareApiClient, "analyze" | "searchWebProducts">>;
  memberCareClientFactory?:(member:{loadToken:()=>Promise<string|null>;onMemberChanged():void})=>Pick<CareApiClient,"searchProducts"> & Partial<Pick<CareApiClient,"analyze"|"searchWebProducts">>;
  /** Only the real app composition supplies these exact HTTPS origins. */
  portfolioApiBaseUrl?: string;
  allowedPortfolioApiBaseUrls?: readonly string[];
  /** Explicit account-bound store for product candidates saved from Explore. */
  savedCandidateStore?: MiraySavedCandidatesStore;
  /** Explicit TEST comparison transport only; runtime supplies no default. */
  candidateComparisonReader?: CandidateComparisonReader;
  /** Explicit local TEST port; not constructed by runtime. */
  closedLoopReviewStore?: ClosedLoopReviewStore;
  /** Local initial/fresh-state seam; no installed runtime factory. */
  closedLoopEntryReviewStore?: ClosedLoopEntryReviewStore;
  /** Explicit local journey factory, opened only by a user action. */
  closedLoopJourneyReviewFactory?: ()=>ClosedLoopJourneyReviewStore;
  /** Held original TEST HTTP factory; default is absent. */
  originalLoopTestFactory?:OriginalLoopTestFactory;
  publicLoopFactory?:OriginalPublicLoopFactory;
  /** Exact HTTPS origin for the non-sensitive saved-candidate route. */
  savedCandidatesApiBaseUrl?: string;
  allowedSavedCandidatesApiBaseUrls?: readonly string[];
  fetcher?: typeof fetch;
  skinStateEnabled?: boolean;
  /** Launch-policy switch for the member-declared product availability aid. */
  replenishmentEnabled?: boolean;
  sensitiveConsentVerified?: boolean;
  historyStorageConsented?: boolean;
  /** Local-review seam only; installed runtime supplies no history transport. */
  historyConsentStore?: AppHistoryConsentStore;
  historyConsentApiBaseUrl?: string;
  allowedHistoryConsentApiBaseUrls?: readonly string[];
  skinStateStore?: MiraySkinStateStore;
  /** Exact HTTPS origin for the separately consented sensitive-state route. */
  skinStateApiBaseUrl?: string;
  allowedSkinStateApiBaseUrls?: readonly string[];
  /** Explicit account-bound reader for the minimal subscription display state. */
  subscriptionEnabled?: boolean;
  subscriptionStatusStore?: MiraySubscriptionStatusStore;
  /** Isolated purchase/restore UI review seam; absent from installed composition. */
  storeKitPurchaseReviewPort?: StoreKitPurchaseReviewPort;
  /** Explicit local native bootstrap seam; no installed SDK factory. */
  storeKitSessionReviewConnection?: IOSStoreKitSessionReviewConnection;
  /** Explicit local app factory; no plugin registration or operating default. */
  storeKitSessionReviewFactory?: StoreKitSessionReviewFactory;
  /** Exact HTTPS origin for the disabled subscription-status route. */
  subscriptionStatusApiBaseUrl?: string;
  allowedSubscriptionStatusApiBaseUrls?: readonly string[];
  /** Optional display-only quota reader; the installed runtime supplies none. */
  quotaStatusStore?: MirayQuotaStatusStore;
  /** Optional separately consented historical result reader; no runtime default. */
  routineResultStore?: MirayRoutineResultStore;
  routineResultApiBaseUrl?: string;
  allowedRoutineResultApiBaseUrls?: readonly string[];
  quotaStatusApiBaseUrl?: string;
  allowedQuotaStatusApiBaseUrls?: readonly string[];
  homeTasks?: HomeTask[];
  sessionVault?: SessionVault;
  sessionVerifier?: AppSessionVerifier;
  /** Exact HTTPS origin for the disabled server-side logout route. */
  sessionApiBaseUrl?: string;
  allowedSessionApiBaseUrls?: readonly string[];
  /** Exact HTTPS origin for the disabled age-and-notice protection session route. */
  protectionApiBaseUrl?: string;
  allowedProtectionApiBaseUrls?: readonly string[];
  /** Server exchange for a Google ID token obtained by the native iOS bridge. */
  googleApiBaseUrl?: string;
  allowedGoogleApiBaseUrls?: readonly string[];
  getGoogleIdToken?: () => Promise<string>;
  getGoogleLoginAuthorization?: () => Promise<{idToken: string; authorizationCode: string}>;
  /** Server challenge and exchange for a native Apple ID token. */
  appleApiBaseUrl?: string;
  allowedAppleApiBaseUrls?: readonly string[];
  getAppleIdToken?: (nonce: string) => Promise<string>;
  /** Original login code is passed once to an explicitly paired capture server. */
  getAppleLoginAuthorization?: (nonce: string) => Promise<AppleLoginAuthorization>;
  /** Kakao SDK credential callback and exact HTTPS server token-info exchange. */
  kakaoApiBaseUrl?: string;
  allowedKakaoApiBaseUrls?: readonly string[];
  getKakaoAccessToken?: () => Promise<string>;
  /** Enable only with the paired capture server and native 1.2 vault verifier. */
  requireKakaoSDKOwnerProof?: boolean;
  /** Naver SDK credential callback and client-bound server profile exchange. */
  naverApiBaseUrl?: string;
  allowedNaverApiBaseUrls?: readonly string[];
  getNaverAccessToken?: () => Promise<string>;
  /** Exact HTTPS route for server-issued, session-bound email OTP. */
  emailApiBaseUrl?: string;
  allowedEmailApiBaseUrls?: readonly string[];
  logout?: () => Promise<AppLogoutResult>;
  withdrawAndDelete?: () => Promise<AppDeletionResult>;
  /** Local explicit acceptance callback; no default HTTP route or feature activation. */
  withdrawAccount?: () => Promise<AccountWithdrawalResult>;
  /** Held exact HTTP client; the shell owns credential and confirmation lifetimes. */
  withdrawAccountClient?: AccountWithdrawalClient;
  /** Explicit native TEST UI, with its own observation/one-shot lifetime. */
  withdrawalTestControl?: ReactNode;
}) {
  const [authenticated, setAuthenticated] = useState(initialAuthenticated);
  const [sessionSensitiveVerified, setSessionSensitiveVerified] = useState(false);
  const [closureState,setClosureState]=useState<AccountWithdrawalResult["state"]|null>(null);
  const [sessionCleanupNotice,setSessionCleanupNotice]=useState<string|null>(null);
  const [restoreState, setRestoreState] = useState<"idle" | "checking" | "retryable" | "vault_error">(
    !initialAuthenticated && sessionVault && sessionVerifier ? "checking" : "idle",
  );
  const [screen, setScreen] = useState<Screen>(initialAuthenticated ? "routine" : "account");
  const [memberConnectionEpoch,setMemberConnectionEpoch]=useState(0);
  const memberConnectionEpochRef=useRef(0);
  const shellActive=useRef(true);
  const signupHistoryAcceptance=useRef<string|null>(null);
  let signupHistoryBasis:ReturnType<typeof signupHistoryBinding>=null;
  let signupHistoryConfigurationInvalid=false;
  try {signupHistoryBasis=signupHistoryBinding(historySignupConfig,appLoginNotices);}
  catch {signupHistoryConfigurationInvalid=true;}
  const pendingMemberSearches=useRef(new Set<AbortController>());
  useEffect(()=>{
    const searches=pendingMemberSearches.current;
    shellActive.current=true;
    return()=>{shellActive.current=false;abortMemberProductSearches(searches);};
  },[]);
  const advanceMemberConnection=useCallback(()=>{
    abortMemberProductSearches(pendingMemberSearches.current);
    memberConnectionEpochRef.current+=1;
    setMemberConnectionEpoch(memberConnectionEpochRef.current);
  },[]);
  // A committed credential provider owns its requests. Replacing the provider
  // retires old awaits even when the account epoch itself has not changed.
  const memberTransportBinding=useMemo(()=>({sessionVault,memberConnectionEpoch,live:false}),[sessionVault,memberConnectionEpoch]);
  const currentMemberTransportBinding=useRef(memberTransportBinding);
  useLayoutEffect(()=>{
    currentMemberTransportBinding.current=memberTransportBinding;
    memberTransportBinding.live=true;
    return()=>{memberTransportBinding.live=false;};
  },[memberTransportBinding]);
  const onMemberConnectionChanged=useMemo(()=>()=>{
    if(!shellActive.current || !memberTransportBinding.live || currentMemberTransportBinding.current!==memberTransportBinding
        || memberConnectionEpochRef.current!==memberConnectionEpoch)return;
    abortMemberProductSearches(pendingMemberSearches.current);
    // Invalidate sibling requests immediately, before React unmounts the old workspace.
    memberConnectionEpochRef.current+=1;
    setMemberConnectionEpoch(memberConnectionEpochRef.current);
    setAuthenticated(false);setSessionSensitiveVerified(false);setRestoreState("idle");setScreen("account");
    setSessionCleanupNotice("로그인 상태가 변경되어 이전 화면을 닫았습니다. 앱을 다시 열어 현재 로그인 상태를 확인해 주세요.");
  },[memberConnectionEpoch,memberTransportBinding]);
  const loadMemberSessionToken=useMemo(()=>createBoundMemberResponseSessionLoader(
    async()=>sessionVault ? (await sessionVault.load())?.session_token ?? null : null, onMemberConnectionChanged,
    () => shellActive.current && memberTransportBinding.live && currentMemberTransportBinding.current===memberTransportBinding
      && memberConnectionEpochRef.current === memberConnectionEpoch,
  ),[sessionVault,onMemberConnectionChanged,memberConnectionEpoch,memberTransportBinding]);
  const portfolioTransportBinding=useMemo(()=>({sessionVault,portfolioStore,fetcher,portfolioApiBaseUrl,allowedPortfolioApiBaseUrls,memberTransportBinding,live:false}),
    [sessionVault,portfolioStore,fetcher,portfolioApiBaseUrl,allowedPortfolioApiBaseUrls,memberTransportBinding]);
  const currentPortfolioTransportBinding=useRef(portfolioTransportBinding);
  useLayoutEffect(()=>{
    currentPortfolioTransportBinding.current=portfolioTransportBinding;
    portfolioTransportBinding.live=true;
    return()=>{portfolioTransportBinding.live=false;};
  },[portfolioTransportBinding]);
  const resolvedPortfolioStore = useMemo(() => {
    if(!sessionVault)return portfolioStore;
    const current=()=>shellActive.current && portfolioTransportBinding.live && currentPortfolioTransportBinding.current===portfolioTransportBinding
      && memberTransportBinding.live && currentMemberTransportBinding.current===memberTransportBinding
      && memberConnectionEpochRef.current===memberTransportBinding.memberConnectionEpoch;
    const changed=()=>{if(current())onMemberConnectionChanged();};
    // Keep the credential await inside this contract's lifetime. An obsolete
    // consumer's load error must not retire the replacement consumer/account.
    const load=loadMemberSessionToken.within(current);
    if (portfolioStore) return bindMemberPortfolioStore(portfolioStore,load,changed);
    if (!sessionVault || !portfolioApiBaseUrl || !allowedPortfolioApiBaseUrls?.length) return undefined;
    const ownedFetcher=(fetcher as typeof fetch & {within?:(live:()=>boolean,prepare?:()=>Promise<void>)=>typeof fetch})
      .within?.(current,async()=>{await load();})??fetcher;
    return createHttpMirayPortfolioStore(ownedFetcher, {
      baseUrl: portfolioApiBaseUrl,
      allowedBaseUrls: allowedPortfolioApiBaseUrls,
      loadSessionToken:load,
      onSessionChanged:changed,
    });
  }, [allowedPortfolioApiBaseUrls, fetcher, portfolioApiBaseUrl, portfolioStore, sessionVault, onMemberConnectionChanged, memberTransportBinding, portfolioTransportBinding, loadMemberSessionToken]);
  const savedCandidatesContract=useMemo(()=>({savedCandidateStore,savedCandidatesApiBaseUrl,allowedSavedCandidatesApiBaseUrls,fetcher}),[savedCandidateStore,savedCandidatesApiBaseUrl,allowedSavedCandidatesApiBaseUrls,fetcher]);
  const savedCandidatesTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,savedCandidatesContract);
  const resolvedSavedCandidateStore = useMemo(() => {
    if (savedCandidateStore) return sessionVault ? bindMemberSavedCandidatesStore(savedCandidateStore,savedCandidatesTransport.load,savedCandidatesTransport.changed) : savedCandidateStore;
    if (!sessionVault || !savedCandidatesApiBaseUrl || !allowedSavedCandidatesApiBaseUrls?.length) return undefined;
    return createHttpMiraySavedCandidatesStore(fetcher, {
      baseUrl: savedCandidatesApiBaseUrl,
      allowedBaseUrls: allowedSavedCandidatesApiBaseUrls,
      loadSessionToken:savedCandidatesTransport.load,
      onSessionChanged:savedCandidatesTransport.changed,
    });
  }, [allowedSavedCandidatesApiBaseUrls, fetcher, savedCandidateStore, savedCandidatesApiBaseUrl, sessionVault, savedCandidatesTransport]);
  const historyContract=useMemo(()=>({historyConsentStore,historyConsentApiBaseUrl,allowedHistoryConsentApiBaseUrls,fetcher}),[historyConsentStore,historyConsentApiBaseUrl,allowedHistoryConsentApiBaseUrls,fetcher]);
  const currentHistoryContract=useRef(historyContract);
  useLayoutEffect(()=>{currentHistoryContract.current=historyContract;},[historyContract]);
  const historyTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,historyContract);
  const resolvedHistoryConsentStore=useMemo(()=>{
    // Member storage requires its credential provider. Raw injected ports are
    // reserved for the explicit isolated preview, never a missing-vault fallback.
    if(connectionsEnabled && !sessionVault)return undefined;
    if(historyConsentStore)return sessionVault?bindMemberHistoryConsentStore(historyConsentStore,historyTransport.load,historyTransport.changed):historyConsentStore;
    if(!sessionVault || !historyConsentApiBaseUrl || !allowedHistoryConsentApiBaseUrls?.length)return undefined;
    return createHttpAppHistoryConsentStore(fetcher,{baseUrl:historyConsentApiBaseUrl,
      allowedBaseUrls:allowedHistoryConsentApiBaseUrls,loadSessionToken:historyTransport.load,onSessionChanged:historyTransport.changed});
  },[historyConsentStore,sessionVault,historyConsentApiBaseUrl,allowedHistoryConsentApiBaseUrls,fetcher,historyTransport,connectionsEnabled]);
  const historyConsent=useAppHistoryConsent(resolvedHistoryConsentStore,authenticated);
  // The old boolean is a synthetic-preview input only, never member authority.
  const historyConsented=resolvedHistoryConsentStore?historyConsent.storageConsented:!connectionsEnabled && historyStorageConsented;
  const historyControl=resolvedHistoryConsentStore?<AppHistoryConsentPanel control={historyConsent}/>:undefined;
  const historyStorageLifetime=connectionsEnabled || resolvedHistoryConsentStore?historyConsent.storageLifetime:undefined;
  const skinStateContract=useMemo(()=>({skinStateStore,skinStateApiBaseUrl,allowedSkinStateApiBaseUrls,fetcher}),[skinStateStore,skinStateApiBaseUrl,allowedSkinStateApiBaseUrls,fetcher]);
  const skinStateTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,skinStateContract,historyStorageLifetime);
  const resolvedSkinStateStore = useMemo(() => {
    if(connectionsEnabled && !sessionVault)return undefined;
    if (skinStateStore) return sessionVault ? bindMemberSkinStateStore(skinStateStore,skinStateTransport.load,skinStateTransport.changed) : skinStateStore;
    if (!sessionVault || !skinStateApiBaseUrl || !allowedSkinStateApiBaseUrls?.length) return undefined;
    return createHttpMiraySkinStateStore(fetcher, {
      baseUrl: skinStateApiBaseUrl,
      allowedBaseUrls: allowedSkinStateApiBaseUrls,
      loadSessionToken:skinStateTransport.load,
      onSessionChanged:skinStateTransport.changed,
    });
  }, [allowedSkinStateApiBaseUrls, fetcher, sessionVault, skinStateApiBaseUrl, skinStateStore, skinStateTransport, connectionsEnabled]);
  const closedLoopContract=useMemo(()=>({closedLoopReviewStore}),[closedLoopReviewStore]);
  const closedLoopTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,closedLoopContract,historyStorageLifetime);
  const resolvedClosedLoopReviewStore=useMemo(()=>connectionsEnabled && !sessionVault?undefined:closedLoopReviewStore
    ?sessionVault?bindMemberClosedLoopReviewStore(closedLoopReviewStore,closedLoopTransport.load,closedLoopTransport.changed):closedLoopReviewStore
    :undefined,[closedLoopReviewStore,sessionVault,closedLoopTransport,connectionsEnabled]);
  const entryContract=useMemo(()=>({closedLoopEntryReviewStore}),[closedLoopEntryReviewStore]);
  const entryTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,entryContract,historyStorageLifetime);
  const resolvedClosedLoopEntryReviewStore=useMemo(()=>connectionsEnabled && !sessionVault?undefined:closedLoopEntryReviewStore
    ?sessionVault?bindMemberClosedLoopEntryReviewStore(closedLoopEntryReviewStore,entryTransport.load,entryTransport.changed):closedLoopEntryReviewStore
    :undefined,[closedLoopEntryReviewStore,sessionVault,entryTransport,connectionsEnabled]);
  const journeyContract=useMemo(()=>({closedLoopJourneyReviewFactory}),[closedLoopJourneyReviewFactory]);
  const journeyTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,journeyContract,historyStorageLifetime);
  const resolvedClosedLoopJourneyReviewFactory=useMemo(()=>!closedLoopJourneyReviewFactory || closedLoopEntryReviewStore || closedLoopReviewStore || !sessionVault?undefined:
    ()=>bindMemberClosedLoopJourneyReviewStore(closedLoopJourneyReviewFactory(),journeyTransport.load,journeyTransport.changed),
  [closedLoopJourneyReviewFactory,closedLoopEntryReviewStore,closedLoopReviewStore,sessionVault,journeyTransport]);
  const originalLoopContract=useMemo(()=>({originalLoopTestFactory}),[originalLoopTestFactory]);
  const originalLoopTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,originalLoopContract,historyStorageLifetime);
  const resolvedOriginalLoopFactory=useMemo(()=>!originalLoopTestFactory || publicLoopFactory || !sessionVault || !connectionsEnabled || closedLoopEntryReviewStore || closedLoopReviewStore || closedLoopJourneyReviewFactory?undefined:
    ()=>originalLoopTestFactory({loadToken:originalLoopTransport.load,onMemberChanged:originalLoopTransport.changed}),
  [originalLoopTestFactory,publicLoopFactory,sessionVault,connectionsEnabled,closedLoopEntryReviewStore,closedLoopReviewStore,closedLoopJourneyReviewFactory,originalLoopTransport]);
  const subscriptionContract=useMemo(()=>({subscriptionEnabled,subscriptionStatusStore,subscriptionStatusApiBaseUrl,allowedSubscriptionStatusApiBaseUrls,fetcher}),[subscriptionEnabled,subscriptionStatusStore,subscriptionStatusApiBaseUrl,allowedSubscriptionStatusApiBaseUrls,fetcher]);
  const subscriptionTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,subscriptionContract);
  const resolvedSubscriptionStatusStore = useMemo(() => {
    if (!subscriptionEnabled) return undefined;
    if (subscriptionStatusStore) return sessionVault ? bindMemberSubscriptionStatusStore(subscriptionStatusStore,subscriptionTransport.load,subscriptionTransport.changed) : subscriptionStatusStore;
    if (!sessionVault || !subscriptionStatusApiBaseUrl || !allowedSubscriptionStatusApiBaseUrls?.length) return undefined;
    return createHttpMiraySubscriptionStatusStore(fetcher, {
      baseUrl: subscriptionStatusApiBaseUrl,
      allowedBaseUrls: allowedSubscriptionStatusApiBaseUrls,
      loadSessionToken:subscriptionTransport.load,
      onSessionChanged:subscriptionTransport.changed,
    });
  }, [subscriptionEnabled, allowedSubscriptionStatusApiBaseUrls, fetcher, sessionVault, subscriptionStatusApiBaseUrl, subscriptionStatusStore, subscriptionTransport]);
  const storeKitFactoryLifetime=useMemo(()=>({isCurrent:()=>subscriptionEnabled && shellActive.current && memberTransportBinding.live
    && currentMemberTransportBinding.current===memberTransportBinding
    && memberConnectionEpochRef.current===memberConnectionEpoch}),[subscriptionEnabled,memberTransportBinding,memberConnectionEpoch]);
  const ownedStoreKitSessionReviewConnection=useStoreKitSessionFactoryLocal(subscriptionEnabled ? storeKitSessionReviewFactory : undefined,
    authenticated && sessionVault && resolvedSubscriptionStatusStore && !storeKitPurchaseReviewPort && !storeKitSessionReviewConnection
      ?loadMemberSessionToken:undefined,storeKitFactoryLifetime);
  const effectiveStoreKitSessionReviewConnection=!subscriptionEnabled ? undefined : storeKitSessionReviewFactory
    ?!storeKitPurchaseReviewPort && !storeKitSessionReviewConnection?ownedStoreKitSessionReviewConnection:undefined
    :storeKitSessionReviewConnection;
  const storeKitContract=useMemo(()=>({subscriptionEnabled,storeKitPurchaseReviewPort,storeKitSessionReviewConnection:effectiveStoreKitSessionReviewConnection,storeKitSessionReviewFactory}),
    [subscriptionEnabled,storeKitPurchaseReviewPort,effectiveStoreKitSessionReviewConnection,storeKitSessionReviewFactory]);
  const storeKitTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,storeKitContract);
  const resolvedStoreKitPurchaseReviewPort=useMemo(()=>subscriptionEnabled && storeKitPurchaseReviewPort && !storeKitSessionReviewConnection && !storeKitSessionReviewFactory && sessionVault
    ?bindMemberStoreKitPurchaseReviewPort(storeKitPurchaseReviewPort,storeKitTransport.load,storeKitTransport.changed):undefined,
  [subscriptionEnabled,storeKitPurchaseReviewPort,storeKitSessionReviewConnection,storeKitSessionReviewFactory,sessionVault,storeKitTransport]);
  const resolvedStoreKitSessionReviewConnection=useMemo(()=>effectiveStoreKitSessionReviewConnection && !storeKitPurchaseReviewPort && sessionVault
    ?bindMemberStoreKitSessionConnectionLocal(effectiveStoreKitSessionReviewConnection,storeKitTransport.load,storeKitTransport.changed):undefined,
  [storeKitPurchaseReviewPort,effectiveStoreKitSessionReviewConnection,sessionVault,storeKitTransport]);
  const publicLoopContract=useMemo(()=>({publicLoopFactory}),[publicLoopFactory]);
  const publicLoopTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,publicLoopContract,historyStorageLifetime);
  const resolvedPublicLoopFactory=useMemo(()=>!publicLoopFactory || originalLoopTestFactory || !sessionVault || !connectionsEnabled || closedLoopEntryReviewStore || closedLoopReviewStore || closedLoopJourneyReviewFactory?undefined:
    ()=>publicLoopFactory({loadToken:publicLoopTransport.load,onMemberChanged:publicLoopTransport.changed}),
    [publicLoopFactory,originalLoopTestFactory,sessionVault,connectionsEnabled,closedLoopEntryReviewStore,closedLoopReviewStore,closedLoopJourneyReviewFactory,publicLoopTransport]);
  const quotaContract=useMemo(()=>({quotaStatusStore,quotaStatusApiBaseUrl,allowedQuotaStatusApiBaseUrls,fetcher}),[quotaStatusStore,quotaStatusApiBaseUrl,allowedQuotaStatusApiBaseUrls,fetcher]);
  const quotaTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,quotaContract);
  const resolvedQuotaStatusStore=useMemo(()=>{
    if(quotaStatusStore)return sessionVault?bindMemberQuotaStatusStore(quotaStatusStore,quotaTransport.load,quotaTransport.changed):quotaStatusStore;
    if(!sessionVault||!quotaStatusApiBaseUrl||!allowedQuotaStatusApiBaseUrls?.length)return undefined;
    return createHttpMirayQuotaStatusStore(fetcher,{
      baseUrl:quotaStatusApiBaseUrl,allowedBaseUrls:allowedQuotaStatusApiBaseUrls,
      loadSessionToken:quotaTransport.load,onSessionChanged:quotaTransport.changed,
    });
  },[quotaStatusStore,sessionVault,quotaStatusApiBaseUrl,allowedQuotaStatusApiBaseUrls,fetcher,quotaTransport]);
  const resultContract=useMemo(()=>({routineResultStore,routineResultApiBaseUrl,allowedRoutineResultApiBaseUrls,fetcher}),[routineResultStore,routineResultApiBaseUrl,allowedRoutineResultApiBaseUrls,fetcher]);
  const resultTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,resultContract,historyStorageLifetime);
  const resolvedRoutineResultStore=useMemo(()=>{
    if(connectionsEnabled && !sessionVault)return undefined;
    if(routineResultStore)return sessionVault?bindMemberRoutineResultStore(routineResultStore,resultTransport.load,resultTransport.changed):routineResultStore;
    if(!sessionVault||!routineResultApiBaseUrl||!allowedRoutineResultApiBaseUrls?.length)return undefined;
    return createHttpMirayRoutineResultStore(fetcher,{
      baseUrl:routineResultApiBaseUrl,allowedBaseUrls:allowedRoutineResultApiBaseUrls,
      loadSessionToken:resultTransport.load,onSessionChanged:resultTransport.changed,
    });
  },[routineResultStore,sessionVault,routineResultApiBaseUrl,allowedRoutineResultApiBaseUrls,fetcher,resultTransport,connectionsEnabled]);
  // A member-facing connection cannot expose sensitive recovery without its
  // current consent acknowledgement. Explicit isolated preview ports remain
  // available for the existing synthetic result/member-binding reviews.
  const visibleRoutineResultStore=(connectionsEnabled || resolvedHistoryConsentStore) && !historyConsented?undefined:resolvedRoutineResultStore;
  const comparisonContract=useMemo(()=>({candidateComparisonReader}),[candidateComparisonReader]);
  const comparisonTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,comparisonContract);
  const resolvedComparisonReader=useMemo(() => {
    if(!candidateComparisonReader || !sessionVault)return candidateComparisonReader;
    return (request: Parameters<CandidateComparisonReader>[0]) => {
      const snapshot=structuredClone(request);
      return runWithMemberResponseSession(comparisonTransport.load,comparisonTransport.changed,()=>candidateComparisonReader(snapshot));
    };
  },[candidateComparisonReader,sessionVault,comparisonTransport]);
  const careContract=useMemo(()=>({memberCareClient,memberCareClientFactory}),[memberCareClient,memberCareClientFactory]);
  const careTransport=useMemberConsumerTransport(loadMemberSessionToken,onMemberConnectionChanged,careContract,
    signupHistoryBasis?.key==="sensitive_information" ? historyStorageLifetime : undefined);
  const resolvedMemberCareClient=useMemo(() => {
    if(memberCareClientFactory&&memberCareClient)return undefined;
    const client=memberCareClientFactory&&sessionVault?memberCareClientFactory({loadToken:careTransport.load,onMemberChanged:careTransport.changed}):memberCareClient;
    if(!client || !sessionVault)return client;
    const wrap=<T,>(operation:()=>Promise<T>)=>runWithMemberResponseSession(careTransport.load,careTransport.changed,operation);
    return {
      searchProducts:(query:string,options?:ProductSearchOptions)=>runMemberProductSearch(careTransport.load,careTransport.changed,pendingMemberSearches.current,(q,o)=>client.searchProducts(q,o),query,options),
      ...(client.searchWebProducts ? {searchWebProducts:(query:string,options?:ProductSearchOptions)=>runMemberProductSearch(careTransport.load,careTransport.changed,pendingMemberSearches.current,(q,o)=>client.searchWebProducts!(q,o),query,options)} : {}),
      ...(client.analyze ? {analyze:(request:Parameters<NonNullable<typeof client.analyze>>[0])=>{
        const snapshot=structuredClone(request);
        return wrap(()=>client.analyze!(snapshot));
      }} : {}),
    };
  },[memberCareClient,memberCareClientFactory,sessionVault,careTransport]);
  const resolvedLogout = useMemo(() => {
    if (logout) return logout;
    if (!sessionVault || !sessionApiBaseUrl || !allowedSessionApiBaseUrls?.length) {
      return async (): Promise<AppLogoutResult> => ({state:"vault_unavailable"});
    }
    const revoker = createHttpAppSessionRevoker(fetcher, {
      baseUrl: sessionApiBaseUrl, allowedBaseUrls: allowedSessionApiBaseUrls,
    });
    return () => logoutAppSession(sessionVault, revoker);
  }, [allowedSessionApiBaseUrls, fetcher, logout, sessionApiBaseUrl, sessionVault]);
  const actionBinding=useMemo(()=>({resolvedLogout,withdrawAndDelete,withdrawAccount,withdrawAccountClient,sessionVault,memberConnectionEpoch,live:false}),[resolvedLogout,withdrawAndDelete,withdrawAccount,withdrawAccountClient,sessionVault,memberConnectionEpoch]);
  // Changing a settings consumer or callback is not proof that an uncertain
  // server request failed. The original member connection owns this admission.
  const withdrawalConnection=useMemo(()=>({sessionVault,memberConnectionEpoch,attempted:false}),[sessionVault,memberConnectionEpoch]);
  const currentActionBinding=useRef<typeof actionBinding|null>(null);
  useLayoutEffect(()=>{
    actionBinding.live=true;currentActionBinding.current=actionBinding;
    return()=>{
      actionBinding.live=false;
      if(currentActionBinding.current===actionBinding)currentActionBinding.current=null;
    };
  },[actionBinding]);
  const settingsLifetime=useMemo(()=>({actionBinding,authenticated,screen,live:false}),[actionBinding,authenticated,screen]);
  useLayoutEffect(()=>{
    settingsLifetime.live=authenticated && screen==="settings";
    return()=>{settingsLifetime.live=false;};
  },[settingsLifetime,authenticated,screen]);
  const {requestWithdrawal,handleLogout,handleDeletion}=useMemo(()=>{
    // Scope UI effects to the original committed connection. This is not an
    // authentication receipt and cannot undo an already dispatched request.
    const isCurrent=()=>shellActive.current && actionBinding.live && currentActionBinding.current===actionBinding
      && memberConnectionEpochRef.current===memberConnectionEpoch;
    const leaveMemberScreen=()=>{advanceMemberConnection();setAuthenticated(false);setSessionSensitiveVerified(false);setRestoreState("idle");setScreen("account");};
    return {
      // Contradictory providers stay unavailable; never pick one by precedence.
      requestWithdrawal:!(withdrawAccount && withdrawAccountClient) && (withdrawAccount || withdrawAccountClient && sessionVault) ? async ():Promise<AccountWithdrawalResult>=>{
        if(!isCurrent())return {state:"retryable_error"};
        if(!withdrawAccount && withdrawAccountClient && sessionVault){
          const canDispatch=()=>isCurrent() && authenticated;
          const load=loadMemberSessionToken.within(canDispatch);
          let acceptedEpoch:number|null=null;
          const scopedVault:SessionVault={...sessionVault,load:async()=>{
            if(!canDispatch())throw new AppMemberResponseSessionChanged();
            const credential=await sessionVault.load();
            if(!credential || await load()!==credential.session_token)throw new AppMemberResponseSessionChanged();
            return credential;
          }};
          const result=await requestAppAccountWithdrawal(scopedVault,bindAccountWithdrawalClient(withdrawAccountClient,async token=>{
            if(await load()!==token || !canDispatch())throw new AppMemberResponseSessionChanged();
            const acceptance=parseAccountWithdrawalAcceptance(await withdrawAccountClient(token),withdrawAccountClient.acceptanceSchemaVersion);
            // A complete receipt remains known even if the original view retired.
            // Retire siblings before asynchronous original-token CAS cleanup.
            if(isCurrent()){
              leaveMemberScreen();acceptedEpoch=memberConnectionEpochRef.current;
              setClosureState("account_closed_local_cleanup_required");
            }
            return acceptance;
          }),sessionVault);
          if(acceptedEpoch!==null && shellActive.current && memberConnectionEpochRef.current===acceptedEpoch
              && currentMemberTransportBinding.current.sessionVault===sessionVault && confirmedAccountWithdrawal(result))setClosureState(result.state);
          return result;
        }
        if(withdrawalConnection.attempted)return {state:"withdrawal_unconfirmed"};
        withdrawalConnection.attempted=true;
        const result=await withdrawAccount!();
        // These contract states precede dispatch. No other failure is evidence
        // that the original request did not reach the server.
        if(result.state==="vault_unavailable" || result.state==="signed_out" || result.state==="withdrawal_not_started")withdrawalConnection.attempted=false;
        if(isCurrent() && confirmedAccountWithdrawal(result)) {
          leaveMemberScreen();setClosureState(result.state);
        }
        return result;
      } : undefined,
      handleLogout:async ():Promise<AppLogoutResult>=>{
        if(!isCurrent())return {state:"retryable_error"};
        const result=await resolvedLogout();
        if(!isCurrent())return result;
        if(result.state === "logged_out")leaveMemberScreen();
        if(result.state === "server_revoked_local_cleanup_required" || result.state === "server_revoked_session_changed") {
          leaveMemberScreen();setSessionCleanupNotice("요청에 사용한 서버 세션은 종료됐습니다. 기기의 로그인 상태를 확인하려면 앱을 다시 열어 주세요. 다른 로그인 정보는 임의로 제거하지 않았습니다.");
        }
        return result;
      },
      handleDeletion:async ():Promise<AppDeletionResult>=>{
        if(!isCurrent())return {state:"retryable_error"};
        const result=await withdrawAndDelete();
        if(!isCurrent())return result;
        if(["deleted","signed_out","deletion_unconfirmed"].includes(result.state))leaveMemberScreen();
        if(["server_deleted_local_cleanup_required","server_deleted_session_changed","deletion_unconfirmed_session_changed"].includes(result.state)) {
          leaveMemberScreen();setSessionCleanupNotice(result.state === "deletion_unconfirmed_session_changed"
            ? "로그인 상태가 변경됐습니다. 이전 요청의 삭제 완료는 확인되지 않았습니다. 새 로그인 정보를 보존했으니 앱을 다시 열어 확인해 주세요."
            : "이전 요청의 삭제 영수증은 확인했습니다. 기기 로그인 상태를 확인하려면 앱을 다시 열어 주세요. 다른 로그인 정보는 임의로 제거하지 않았습니다.");
        }
        return result;
      },
    };
  },[actionBinding,memberConnectionEpoch,resolvedLogout,withdrawAccount,withdrawAccountClient,sessionVault,
    authenticated,loadMemberSessionToken,withdrawAndDelete,advanceMemberConnection,withdrawalConnection]);
  const protectionClient = useMemo(() => {
    if (!sessionVault || !protectionApiBaseUrl || !allowedProtectionApiBaseUrls?.length) return undefined;
    return createHttpAppProtectionSessionClient(fetcher, {
      baseUrl:protectionApiBaseUrl, allowedBaseUrls:allowedProtectionApiBaseUrls,
    });
  }, [allowedProtectionApiBaseUrls, fetcher, protectionApiBaseUrl, sessionVault]);
  const googleClient = useMemo(() => {
    if (!sessionVault || !googleApiBaseUrl || !allowedGoogleApiBaseUrls?.length || !(getGoogleIdToken || getGoogleLoginAuthorization)) return undefined;
    return createHttpAppGoogleLoginClient(fetcher, {
      baseUrl:googleApiBaseUrl, allowedBaseUrls:allowedGoogleApiBaseUrls,
      ...(getGoogleLoginAuthorization ? {captureAuthorizationCode: true} : {}),
    });
  }, [allowedGoogleApiBaseUrls, fetcher, getGoogleIdToken, getGoogleLoginAuthorization, googleApiBaseUrl, sessionVault]);
  const appleClient = useMemo(() => {
    if (!sessionVault || !appleApiBaseUrl || !allowedAppleApiBaseUrls?.length || !(getAppleIdToken || getAppleLoginAuthorization)) return undefined;
    return createHttpAppAppleLoginClient(fetcher, {
      baseUrl:appleApiBaseUrl, allowedBaseUrls:allowedAppleApiBaseUrls,
      ...(getAppleLoginAuthorization ? {captureAuthorizationCode: true} : {}),
    });
  }, [allowedAppleApiBaseUrls, appleApiBaseUrl, fetcher, getAppleIdToken, getAppleLoginAuthorization, sessionVault]);
  const kakaoClient = useMemo(() => {
    if (!sessionVault || !kakaoApiBaseUrl || !allowedKakaoApiBaseUrls?.length || !getKakaoAccessToken) return undefined;
    return createHttpAppKakaoLoginClient(fetcher, {
      baseUrl:kakaoApiBaseUrl, allowedBaseUrls:allowedKakaoApiBaseUrls,
      requireSDKOwnerProof:requireKakaoSDKOwnerProof,
      ...(sessionVault.authenticationContracts?.kakao==="1.0.0-public-kakao-session" ? {ownerProfile:"public" as const} : {}),
    });
  }, [allowedKakaoApiBaseUrls, fetcher, getKakaoAccessToken, kakaoApiBaseUrl, requireKakaoSDKOwnerProof, sessionVault]);
  const naverClient = useMemo(() => {
    if (!sessionVault || !naverApiBaseUrl || !allowedNaverApiBaseUrls?.length || !getNaverAccessToken) return undefined;
    return createHttpAppNaverLoginClient(fetcher, {
      baseUrl:naverApiBaseUrl, allowedBaseUrls:allowedNaverApiBaseUrls,
    });
  }, [allowedNaverApiBaseUrls, fetcher, getNaverAccessToken, naverApiBaseUrl, sessionVault]);
  const emailClient = useMemo(() => {
    if (!sessionVault || !emailApiBaseUrl || !allowedEmailApiBaseUrls?.length) return undefined;
    return createHttpAppEmailOtpClient(fetcher, {
      baseUrl:emailApiBaseUrl, allowedBaseUrls:allowedEmailApiBaseUrls,
    });
  }, [allowedEmailApiBaseUrls, emailApiBaseUrl, fetcher, sessionVault]);
  const emptyLinkRouter = useMemo(() => createAppExternalLinkRouter({firstPartyOrigins:[], links:[]}), []);
  const disabledLinkOpener = useMemo<AppExternalLinkOpener>(() => ({openExternal: async () => {
    throw new Error("Public links are not verified yet");
  }}), []);

  useEffect(() => {
    if (initialAuthenticated || !sessionVault || !sessionVerifier || restoreState !== "checking") return;
    let active = true;
    void restoreAuthenticatedSession(sessionVault, sessionVerifier, receipt => {
      if (active) setSessionSensitiveVerified(receipt?.sensitive_notice_version === privacy.notices.sensitive_information.version);
    }).then(result => {
      if (!active) return;
      if (result === "resumed") {
        setAuthenticated(true);
        setScreen("routine");
        setRestoreState("idle");
      } else if (result === "retryable_error" || result === "session_changed") setRestoreState("retryable");
      else if (result === "vault_unavailable") setRestoreState("vault_error");
      else setRestoreState("idle");
    });
    return () => { active = false; };
  }, [initialAuthenticated, restoreState, sessionVault, sessionVerifier]);

  useEffect(() => {
    const backFromSettings = (event: Event) => {
      if (screen !== "settings") return;
      event.stopImmediatePropagation();
      settingsLifetime.live=false;
      setScreen("routine");
    };
    window.addEventListener("skinanalysis:native-back", backFromSettings, {capture:true});
    return () => window.removeEventListener("skinanalysis:native-back", backFromSettings, {capture:true});
  }, [screen,settingsLifetime]);

  const finishAuthentication = async (session?: AppAuthenticationSession) => {
    if (!session || !sessionVault || !sessionVerifier) throw new Error("Server session was not issued or cannot be verified");
    const acceptedHistoryVersion=signupHistoryAcceptance.current;
    signupHistoryAcceptance.current=null;
    // Provider login rotates the protection bearer on the server. Persist the new bearer
    // before a retryable verifier failure can strand the device with the old one.
    await saveAuthenticatedSession(sessionVault, session);
    try {
      const receipt = await sessionVerifier.verify(session.session_token);
      const current=await sessionVault.load();
      if(!current || current.session_token!==session.session_token || Date.parse(current.expires_at)!==Date.parse(session.expires_at)) {
        setRestoreState("retryable");
        throw new Error("로그인 상태가 변경됐습니다. 다시 확인해 주세요.");
      }
      setSessionSensitiveVerified(receipt?.sensitive_notice_version === privacy.notices.sensitive_information.version);
      if(signupHistoryConfigurationInvalid)throw new Error("이력 저장 안내 연결을 확인하지 못했어요.");
      if(signupHistoryBasis) {
        const currentSession=async()=>{
          const stored=await sessionVault.load();
          if(!shellActive.current || !memberTransportBinding.live
              || currentMemberTransportBinding.current!==memberTransportBinding
              || memberConnectionEpochRef.current!==memberConnectionEpoch
              || currentHistoryContract.current!==historyContract
              || stored?.session_token!==session.session_token
              || Date.parse(stored.expires_at)!==Date.parse(session.expires_at))throw new AppMemberResponseSessionChanged();
          return session.session_token;
        };
        const store=historyConsentStore
          ? bindMemberHistoryConsentStore(historyConsentStore,currentSession,()=>{})
          : historyConsentApiBaseUrl && allowedHistoryConsentApiBaseUrls?.length
            ? createHttpAppHistoryConsentStore(fetcher,{baseUrl:historyConsentApiBaseUrl,
              allowedBaseUrls:allowedHistoryConsentApiBaseUrls,loadSessionToken:currentSession})
            : null;
        if(!store)throw new Error("이력 저장 연결을 확인하지 못했어요.");
        await completeSignupHistoryConsent({acceptedVersion:acceptedHistoryVersion,
          requiredVersion:signupHistoryBasis.version,store});
        await currentSession();
      }
    } catch (error) {
      if (error instanceof AppAuthenticationError && [401, 403].includes(error.status)) {
        const cleanup=await clearSessionCredential(sessionVault,session.session_token);
        if(cleanup!=="cleared")setRestoreState(cleanup === "changed" ? "retryable" : "vault_error");
      } else {
        setRestoreState("retryable");
      }
      throw error;
    }
    advanceMemberConnection();
    setAuthenticated(true);
    setClosureState(null);
    setSessionCleanupNotice(null);
    setScreen("routine");
  };

  if(sessionCleanupNotice)return <main className="account-start-screen"><h1>로그인 상태를 다시 확인해 주세요</h1><p role="alert">{sessionCleanupNotice}</p></main>;

  if(closureState === "account_closed_local_cleanup_required" || closureState === "account_closed_session_changed")return <main className="account-start-screen">
    <h1>탈퇴 요청을 접수했어요</h1>
    <p role="alert">계정 이용 중단은 확인됐지만 기기의 로그인 상태를 정리해야 합니다. 앱을 다시 열어 로그인 상태를 확인해 주세요.</p>
    <p>전체 데이터 삭제 완료는 아직 확인되지 않았습니다.{subscriptionEnabled && " 구독은 앱 스토어에서 별도로 확인해 주세요."}</p>
  </main>;

  if (!authenticated && restoreState !== "idle") return <main className="account-start-screen">
    <h1>{restoreState === "checking" ? "로그인 상태를 확인하고 있어요" : "로그인 상태를 확인하지 못했어요"}</h1>
    {restoreState === "retryable" && <><p>연결을 확인한 뒤 다시 시도해 주세요. 저장된 세션은 삭제하지 않았어요.</p><button type="button" onClick={() => setRestoreState("checking")}>다시 확인</button></>}
    {restoreState === "vault_error" && <p role="alert">기기의 보안 저장소를 사용할 수 없어요. 앱을 다시 열어 주세요.</p>}
  </main>;

  if (!authenticated) return <div className="app-settings-preview">
    <AccountStartScreen
      accountNotice={closureState === "account_closed" ? `탈퇴 요청을 접수하고 계정 이용을 중단했습니다. 전체 데이터 삭제 완료는 아직 확인되지 않았습니다.${subscriptionEnabled ? " 구독은 앱 스토어에서 별도로 확인해 주세요." : ""}` : undefined}
      previewMode={allowOwnerTestSession}
      connectionsEnabled={connectionsEnabled}
      availableProviders={availableProviders}
      emailEnabled={emailEnabled}
      availabilityNotice={availabilityNotice}
      loginNotices={signupHistoryConfigurationInvalid ? null : appLoginNotices}
      onProtectionStart={protectionClient && sessionVault ? async acceptance => {
        signupHistoryAcceptance.current=null;
        await atLoginStartStage("L01", async () => {
          const protection = await protectionClient.start(acceptance);
          await saveAuthenticatedSession(sessionVault, protection);
        });
        signupHistoryAcceptance.current=signupHistoryBasis ? acceptance.accepted_notices[signupHistoryBasis.key] ?? null : null;
      } : undefined}
      onProviderStart={async provider => {
        let session: AppAuthenticationSession | void;
        if (provider === "google") {
          if (!googleClient || !(getGoogleIdToken || getGoogleLoginAuthorization) || !sessionVault) throw new Error("Google adapter unavailable");
          const protectionBearer = (await sessionVault.load())?.session_token;
          if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
          if (getGoogleLoginAuthorization) {
            const authorization = await getGoogleLoginAuthorization();
            session = await googleClient.exchange(authorization.idToken, protectionBearer, authorization.authorizationCode);
          } else {
            if (!getGoogleIdToken) throw new Error("Google adapter unavailable");
            session = await googleClient.exchange(await getGoogleIdToken(), protectionBearer);
          }
        } else if (provider === "apple") {
          if (!appleClient || !(getAppleIdToken || getAppleLoginAuthorization) || !sessionVault) throw new Error("Apple adapter unavailable");
          const protectionBearer = (await sessionVault.load())?.session_token;
          if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
          const challenge = await atLoginStartStage("A01", () => appleClient.challenge(protectionBearer));
          if (getAppleLoginAuthorization) {
            const authorization = await atLoginStartStage("A02", () => getAppleLoginAuthorization(challenge.nonce));
            session = await atLoginStartStage("A03", () => appleClient.exchange(authorization.idToken, challenge.nonce,
              protectionBearer, authorization.authorizationCode));
          } else {
            if (!getAppleIdToken) throw new Error("Apple adapter unavailable");
            session = await appleClient.exchange(await getAppleIdToken(challenge.nonce),
              challenge.nonce, protectionBearer);
          }
        } else if (provider === "kakao") {
          if (!kakaoClient || !getKakaoAccessToken || !sessionVault) throw new Error("Kakao adapter unavailable");
          const protectionBearer = (await sessionVault.load())?.session_token;
          if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
          session = await kakaoClient.exchange(await getKakaoAccessToken(), protectionBearer);
        } else if (provider === "naver") {
          if (!naverClient || !getNaverAccessToken || !sessionVault) throw new Error("Naver adapter unavailable");
          const protectionBearer = (await sessionVault.load())?.session_token;
          if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
          session = await naverClient.exchange(await getNaverAccessToken(), protectionBearer);
        } else {
          const unsupportedProvider: never = provider;
          throw new Error(`Provider adapter unavailable: ${unsupportedProvider}`);
        }
        if (provider === "apple") await atLoginStartStage("A04", () => finishAuthentication(session || undefined));
        else await finishAuthentication(session || undefined);
      }}
      onEmailOtpStart={async email => {
        if (!emailClient || !sessionVault) throw new Error("Email OTP adapter unavailable");
        const protectionBearer = (await sessionVault.load())?.session_token;
        if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
        await emailClient.issue(email, protectionBearer);
      }}
      onEmailOtpVerify={emailClient && sessionVault ? async (email, code) => {
        const protectionBearer = (await sessionVault.load())?.session_token;
        if (!protectionBearer) throw new Error("보호 세션을 확인하지 못했습니다.");
        const session = await emailClient.verify(email, code, protectionBearer);
        await finishAuthentication(session);
      } : undefined}
      onTestSessionStart={allowOwnerTestSession ? () => { setAuthenticated(true); setScreen("routine"); } : undefined}
    />
  </div>;

  if (newNavigationEnabled && connectionsEnabled && !resolvedPortfolioStore) return <main className="account-start-screen">
    <h1>계정 기록을 준비하지 못했어요</h1>
    <p role="alert">화장품과 루틴을 계정에 안전하게 저장할 연결이 필요해요. 현재 세션에서만 기록을 유지한 채 시작하지 않아요.</p>
  </main>;

  const settings = <AppSettingsScreen
      subscriptionEnabled={subscriptionEnabled}
      historyConsentControl={historyControl}
      withdrawAccount={requestWithdrawal}
      withdrawalTestControl={withdrawalTestControl}
      subscription={{serverVerified:false}}
      subscriptionStatusStore={resolvedSubscriptionStatusStore}
      storeKitPurchaseReviewPort={resolvedStoreKitPurchaseReviewPort}
      storeKitSessionReviewConnection={resolvedStoreKitSessionReviewConnection}
      quotaStatusStore={resolvedQuotaStatusStore}
      routineResultStore={visibleRoutineResultStore}
      linkRouter={emptyLinkRouter}
      linkOpener={disabledLinkOpener}
      logout={handleLogout}
      withdrawAndDelete={handleDeletion}
    />;
  if (newNavigationEnabled) return <MirayWorkspace kbAppPort={kbAppPort} settings={settings} portfolioStore={resolvedPortfolioStore} savedCandidateStore={resolvedSavedCandidateStore} candidateComparisonReader={resolvedComparisonReader} closedLoopReviewStore={resolvedClosedLoopReviewStore} closedLoopEntryReviewStore={resolvedClosedLoopEntryReviewStore} closedLoopJourneyReviewFactory={resolvedClosedLoopJourneyReviewFactory} originalLoopTestFactory={resolvedOriginalLoopFactory} publicLoopFactory={resolvedPublicLoopFactory} quotaStatusStore={resolvedQuotaStatusStore} memberCareClient={resolvedMemberCareClient} skinStateEnabled={skinStateEnabled} replenishmentEnabled={replenishmentEnabled} sensitiveConsentVerified={connectionsEnabled ? sessionSensitiveVerified && !signupHistoryConfigurationInvalid && (signupHistoryBasis?.key!=="sensitive_information" || historyConsented) : sensitiveConsentVerified} historyStorageConsented={historyConsented} skinStateStore={resolvedSkinStateStore} homeTasks={homeTasks} />;

  return <div className="app-launch-shell">
    <div hidden={screen !== "routine"} aria-hidden={screen !== "routine"}>
      <AppPrototype active={screen === "routine"} onOpenSettings={() => setScreen("settings")} />
    </div>
    {screen === "settings" && <AppSettingsLifetimeContext.Provider value={settingsLifetime}><AppSettingsScreen
      subscriptionEnabled={subscriptionEnabled}
      historyConsentControl={historyControl}
      withdrawAccount={requestWithdrawal}
      withdrawalTestControl={withdrawalTestControl}
      subscription={{serverVerified:false}}
      subscriptionStatusStore={resolvedSubscriptionStatusStore}
      storeKitPurchaseReviewPort={resolvedStoreKitPurchaseReviewPort}
      storeKitSessionReviewConnection={resolvedStoreKitSessionReviewConnection}
      quotaStatusStore={resolvedQuotaStatusStore}
      routineResultStore={visibleRoutineResultStore}
      linkRouter={emptyLinkRouter}
      linkOpener={disabledLinkOpener}
      onBack={() => setScreen("routine")}
      logout={handleLogout}
      withdrawAndDelete={handleDeletion}
    /></AppSettingsLifetimeContext.Provider>}
  </div>;
}
