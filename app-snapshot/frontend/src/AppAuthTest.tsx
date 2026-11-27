import AppLaunchShell from "./AppLaunchShell";
import releaseScope from "../../skin_engine/config/app_release_scope.json";
import appleLoginHandoff from "../../skin_engine/config/app_apple_login_handoff.json";
import googleLoginHandoff from "../../skin_engine/config/app_google_login_handoff.json";
import {searchNativeIOSCatalog} from "./iosCatalogSearch";
import {nativeIOSWebSearchAvailable,searchNativeIOSWebProducts} from "./iosProductWebSearch";
import {createHttpAppSessionVerifier} from "./appAuthentication";
import {createSessionVault} from "./appSessionVault";
import {createHttpAccountWithdrawalClient} from "./appAccountWithdrawal";
import {APP_AUTH_TEST_API_ORIGIN, createIOSAppAuthFetcher} from "./iosAppAuthFetcher";
import {getIOSAppleIDToken,getIOSAppleLoginAuthorization} from "./iosAppleIdentity";
import {getIOSGoogleIDToken,getIOSGoogleLoginAuthorization} from "./iosGoogleIdentity";
import {getIOSKakaoAccessToken} from "./iosKakaoIdentity";
import {kakaoOwnerHandoffSelected} from "./appKakaoLogin";
import {createNativeIOSKeychainStore} from "./iosSessionVaultStore";
import type {StoreKitSessionReviewFactory} from "./appStoreKitSessionFactoryLocal";
import type {MiraySubscriptionStatusStore} from "./miraySubscriptionStatus";
import type {ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";
import type {ClosedLoopReviewStore} from "./mirayClosedLoop";
import type {ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";

import type {OriginalLoopTestFactory} from "./mirayOriginalLoopTest";
import {useSyncExternalStore} from "react";
import {createIOSWithdrawalTestConnection} from "./iosWithdrawalTestConnection";
import NativeWithdrawalTestControl from "./NativeWithdrawalTestControl";
import {NATIVE_RELEASE_CANDIDATE_SELECTED} from "./nativeReleaseCandidateSelection";

const allowedOrigins = [APP_AUTH_TEST_API_ORIGIN] as const;
const releaseCandidate=NATIVE_RELEASE_CANDIDATE_SELECTED;
const connectedMode=releaseCandidate || import.meta.env.VITE_APP_MODE==="app_auth_test";
const captureAppleLogin=connectedMode && appleLoginHandoff.selected===true;
const captureGoogleLogin=connectedMode && googleLoginHandoff.selected===true;
const captureKakaoLogin=connectedMode && kakaoOwnerHandoffSelected();
const portfolioTestEnabled = releaseCandidate || import.meta.env.VITE_APP_PORTFOLIO_TEST === "true";
const skinStateTestEnabled = portfolioTestEnabled && (releaseCandidate || import.meta.env.VITE_APP_SKIN_STATE_TEST === "true");
// Prepared build only; the normal Q3 build never enables a new undeployed API.
const historyConsentTestEnabled = skinStateTestEnabled && (releaseCandidate || import.meta.env.VITE_APP_HISTORY_CONSENT_TEST === "true");
const coreTestReviewEnabled = releaseCandidate || (import.meta.env.VITE_APP_MODE === "app_auth_test"
  && portfolioTestEnabled && import.meta.env.VITE_APP_CORE_TEST_REVIEW === "true");
const accountWithdrawalTestEnabled=coreTestReviewEnabled && (releaseCandidate || import.meta.env.VITE_APP_ACCOUNT_WITHDRAWAL_TEST==="true");
const sessionVault = createSessionVault(createNativeIOSKeychainStore());
const fetcher = createIOSAppAuthFetcher({portfolioTestEnabled, skinStateTestEnabled, historyConsentTestEnabled,
  ...(coreTestReviewEnabled ? {coreTestReviewEnabled:true} : {}),
  ...(accountWithdrawalTestEnabled?{accountWithdrawalTestEnabled:true,beforeAccountWithdrawalDispatch:async(token:string)=>{
    if((await sessionVault.load())?.session_token!==token)throw new Error("기존 탈퇴 세션이 바뀌었어요.");
  }}:{})});
const accountWithdrawalClient=accountWithdrawalTestEnabled
  ?createHttpAccountWithdrawalClient(fetcher,{baseUrl:APP_AUTH_TEST_API_ORIGIN,allowedBaseUrls:allowedOrigins}):undefined;
const sessionVerifier = createHttpAppSessionVerifier(fetcher, {
  baseUrl:APP_AUTH_TEST_API_ORIGIN,
  allowedBaseUrls:allowedOrigins,
});
// The native owner keeps account/provider/bearer and original readback private.
// This module lifetime survives screen changes and an ambiguous native result.
const withdrawalTestConnection=coreTestReviewEnabled&&!accountWithdrawalTestEnabled?createIOSWithdrawalTestConnection():null;
const emptySubscribe=()=>()=>{};
const emptySnapshot=()=>null;

/** Physical-iPhone TEST composition. Public, production, email OTP, and Naver native login remain closed. */
export default function AppAuthTest({storeKitReview,routineReview}: {storeKitReview?: {
  factory:StoreKitSessionReviewFactory;subscriptionStatusStore:MiraySubscriptionStatusStore;
};routineReview?: {
  entry:ClosedLoopEntryReviewStore;episode:ClosedLoopReviewStore;
} | {journey:()=>ClosedLoopJourneyReviewStore} | {original:OriginalLoopTestFactory}} = {}) {
  const withdrawalState=useSyncExternalStore(withdrawalTestConnection?.subscribe??emptySubscribe,withdrawalTestConnection?.getSnapshot??emptySnapshot);
  const withdrawalTestControl=withdrawalTestConnection?<NativeWithdrawalTestControl connection={withdrawalTestConnection}/>:undefined;
  // Retire ordinary member consumers before interpreting any native result.
  // A TEST observation is never converted into AccountWithdrawalAcceptance.
  if(withdrawalState?.attempted)return <main className="account-start-screen">{withdrawalTestControl}</main>;
  return <AppLaunchShell
    connectionsEnabled
    subscriptionEnabled={Boolean(storeKitReview) || releaseScope.paid_subscription_enabled}
    newNavigationEnabled={portfolioTestEnabled}
    memberCareClient={portfolioTestEnabled ? {
      searchProducts:searchNativeIOSCatalog,
      ...(nativeIOSWebSearchAvailable() ? {searchWebProducts:searchNativeIOSWebProducts} : {}),
    } : undefined}
    portfolioApiBaseUrl={portfolioTestEnabled ? APP_AUTH_TEST_API_ORIGIN : undefined}
    allowedPortfolioApiBaseUrls={portfolioTestEnabled ? allowedOrigins : undefined}
    savedCandidatesApiBaseUrl={coreTestReviewEnabled ? APP_AUTH_TEST_API_ORIGIN : undefined}
    allowedSavedCandidatesApiBaseUrls={coreTestReviewEnabled ? allowedOrigins : undefined}
    quotaStatusApiBaseUrl={coreTestReviewEnabled ? APP_AUTH_TEST_API_ORIGIN : undefined}
    allowedQuotaStatusApiBaseUrls={coreTestReviewEnabled ? allowedOrigins : undefined}
    withdrawalTestControl={withdrawalTestControl}
    withdrawAccountClient={accountWithdrawalClient}
    skinStateEnabled={skinStateTestEnabled}
    skinStateApiBaseUrl={skinStateTestEnabled ? APP_AUTH_TEST_API_ORIGIN : undefined}
    allowedSkinStateApiBaseUrls={skinStateTestEnabled ? allowedOrigins : undefined}
    historyConsentApiBaseUrl={historyConsentTestEnabled ? APP_AUTH_TEST_API_ORIGIN : undefined}
    allowedHistoryConsentApiBaseUrls={historyConsentTestEnabled ? allowedOrigins : undefined}
    availableProviders={["apple", "google", "kakao"]}
    emailEnabled={false}
    availabilityNotice={releaseCandidate ? "Apple, Google 또는 카카오로 로그인할 수 있어요." : "현재 TEST에서는 Apple, Google, Kakao 로그인을 확인할 수 있어요. 네이버와 이메일은 연결 준비 중이에요."}
    sessionVault={sessionVault}
    sessionVerifier={sessionVerifier}
    sessionApiBaseUrl={APP_AUTH_TEST_API_ORIGIN}
    allowedSessionApiBaseUrls={allowedOrigins}
    protectionApiBaseUrl={APP_AUTH_TEST_API_ORIGIN}
    allowedProtectionApiBaseUrls={allowedOrigins}
    appleApiBaseUrl={APP_AUTH_TEST_API_ORIGIN}
    allowedAppleApiBaseUrls={allowedOrigins}
    {...(captureAppleLogin ? {getAppleLoginAuthorization:getIOSAppleLoginAuthorization} : {getAppleIdToken:getIOSAppleIDToken})}
    googleApiBaseUrl={APP_AUTH_TEST_API_ORIGIN}
    allowedGoogleApiBaseUrls={allowedOrigins}
    {...(captureGoogleLogin ? {getGoogleLoginAuthorization:getIOSGoogleLoginAuthorization} : {getGoogleIdToken:getIOSGoogleIDToken})}
    kakaoApiBaseUrl={APP_AUTH_TEST_API_ORIGIN}
    allowedKakaoApiBaseUrls={allowedOrigins}
    getKakaoAccessToken={getIOSKakaoAccessToken}
    requireKakaoSDKOwnerProof={captureKakaoLogin}
    fetcher={fetcher}
    storeKitSessionReviewFactory={storeKitReview?.factory}
    subscriptionStatusStore={storeKitReview?.subscriptionStatusStore}
    // Explicit local review ports still use the shell's original member and separate consent gates.
    closedLoopEntryReviewStore={historyConsentTestEnabled && routineReview && "entry" in routineReview ? routineReview.entry : undefined}
    closedLoopReviewStore={historyConsentTestEnabled && routineReview && "entry" in routineReview ? routineReview.episode : undefined}
    closedLoopJourneyReviewFactory={historyConsentTestEnabled && routineReview && "journey" in routineReview ? routineReview.journey : undefined}
    originalLoopTestFactory={historyConsentTestEnabled && routineReview && "original" in routineReview ? routineReview.original : undefined}
  />;
}
