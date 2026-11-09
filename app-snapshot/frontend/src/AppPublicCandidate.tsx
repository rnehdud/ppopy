import {useEffect,useState,type ComponentProps} from "react";
import AppLaunchShell from "./AppLaunchShell";
import {createPublicWebProductSearchClient} from "./publicProductSearch";
import {createPublicCatalogSearchClient} from "./publicCatalogSearch";
import {createOriginalPublicLoopFactory} from "./publicOriginalLoop";
import {connectBundledPublicNativeRuntime,publicInitializationCode} from "./publicNativeBridge";
import {createHttpAppSessionVerifier} from "./appAuthentication";
import {createHttpAccountWithdrawalClient} from "./appAccountWithdrawal";
import transportPolicy from "../../skin_engine/config/app_public_client_transport_review.json";
import contract from "../../skin_engine/config/app_public_account_withdrawal_contract.json";
import {getIOSAppleLoginAuthorization} from "./iosAppleIdentity";
import {getIOSGoogleLoginAuthorization} from "./iosGoogleIdentity";
import {getIOSKakaoAccessToken} from "./iosKakaoIdentity";

type Connection=Awaited<ReturnType<typeof connectBundledPublicNativeRuntime>>;
/** Explicit public-only composition. Does not grant server admission or GO.
 * Public loop/product-search assembly is separate; no TEST factory injected. */
export function createPublicAppShellConnections(connection:Connection):ComponentProps<typeof AppLaunchShell>{
  const match=connection.transport.origin.match(/^https:\/\/([a-z0-9]{10})\.execute-api\.ap-northeast-2\.amazonaws\.com$/);
  const profile=connection.vault.authenticationContracts;
  if(!match||transportPolicy.known_TEST_api_ids.includes(match[1])||profile?.plain!=="1.0.0-public-session"||profile.google!=="1.0.0-public-google-session"||profile.kakao!=="1.0.0-public-kakao-session")throw new Error("공개 앱 연결을 확인하지 못했어요.");
  const base=connection.transport.origin,allowed=Object.freeze([base]),fetcher=connection.transport.fetcher;
  const publicLoopFactory=createOriginalPublicLoopFactory({baseUrl:base,fetcher});
  return Object.freeze({memberCareClientFactory:(member:{loadToken:()=>Promise<string|null>;onMemberChanged():void})=>( {...createPublicCatalogSearchClient({baseUrl:base,fetcher,loadToken:member.loadToken,onMemberChanged:member.onMemberChanged,includeIngredients:import.meta.env.VITE_PUBLIC_INGREDIENT_DISCLOSURE === "true"}),...createPublicWebProductSearchClient({baseUrl:base,fetcher,loadToken:member.loadToken,onMemberChanged:member.onMemberChanged})}),publicLoopFactory,connectionsEnabled:true,newNavigationEnabled:true,subscriptionEnabled:false,emailEnabled:false,
    availableProviders:["apple","google","kakao"] as const,availabilityNotice:"Apple, Google 또는 카카오로 로그인할 수 있어요.",
    sessionVault:connection.vault,sessionVerifier:createHttpAppSessionVerifier(fetcher,{baseUrl:base,allowedBaseUrls:allowed}),
    fetcher,sessionApiBaseUrl:base,allowedSessionApiBaseUrls:allowed,protectionApiBaseUrl:base,allowedProtectionApiBaseUrls:allowed,
    appleApiBaseUrl:base,allowedAppleApiBaseUrls:allowed,getAppleLoginAuthorization:getIOSAppleLoginAuthorization,
    googleApiBaseUrl:base,allowedGoogleApiBaseUrls:allowed,getGoogleLoginAuthorization:getIOSGoogleLoginAuthorization,
    kakaoApiBaseUrl:base,allowedKakaoApiBaseUrls:allowed,getKakaoAccessToken:getIOSKakaoAccessToken,requireKakaoSDKOwnerProof:true,
    portfolioApiBaseUrl:base,allowedPortfolioApiBaseUrls:allowed,savedCandidatesApiBaseUrl:base,allowedSavedCandidatesApiBaseUrls:allowed,
    quotaStatusApiBaseUrl:base,allowedQuotaStatusApiBaseUrls:allowed,skinStateEnabled:true,skinStateApiBaseUrl:base,allowedSkinStateApiBaseUrls:allowed,
    historyConsentApiBaseUrl:base,allowedHistoryConsentApiBaseUrls:allowed,
    withdrawAccountClient:createHttpAccountWithdrawalClient(fetcher,{baseUrl:base,allowedBaseUrls:allowed,responseSchemaVersion:contract.version})});
}
// One native connection per loaded bundle, including React StrictMode remounts.
// A failed initialization is not retried or redirected to a TEST/browser port.
let original:Promise<ComponentProps<typeof AppLaunchShell>>|undefined;
export default function AppPublicCandidate(){
  const [props,setProps]=useState<ComponentProps<typeof AppLaunchShell>|null>(null),[failed,setFailed]=useState<string|null>(null);
  useEffect(()=>{
    let live=true;original??=connectBundledPublicNativeRuntime().then(createPublicAppShellConnections);
    void original.then(value=>{if(live)setProps(value);},error=>{if(live)setFailed(publicInitializationCode(error));});return()=>{live=false;};
  },[]);
  if(!props)return <main className="account-start-screen"><p role="status">{failed?"앱 연결을 확인하지 못했어요. 앱을 완전히 닫은 뒤 다시 열어주세요.":"앱을 준비하고 있어요."}</p>{failed&&<p>연결 확인 코드: {failed}</p>}</main>;
  return <AppLaunchShell {...props}/>;
}
