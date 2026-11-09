import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";
import publicOwnerPolicy from "../../skin_engine/config/app_public_kakao_owner_review.json";
import ownerPolicy from "../../skin_engine/config/app_kakao_sdk_owner_local.json";
import handoff from "../../skin_engine/config/app_kakao_login_handoff.json";

/** Frozen paired-build selection; server responses cannot enable this path. */
export function kakaoOwnerHandoffSelected(): boolean {
  return handoff.selected===true && handoff.version==="1.0.0"
    && handoff.scope==="explicit_TEST_original_kakao_login_handoff"
    && handoff.native_owner_proof_version===KAKAO_OWNER_VERSION;
}
const KAKAO_OWNER_VERSION=ownerPolicy.session_vault_contract_version;

export type AppKakaoLoginClient = {
  exchange(accessToken: string, protectionBearer: string): Promise<AppAuthenticationSession>;
};

function allowedHttpsBase(value: string, allowed: readonly string[]): string {
  const normalize = (entry: string) => {
    const url = new URL(entry.trim());
    if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) {
      throw new Error("앱 API 주소를 확인해 주세요.");
    }
    return `${url.origin}${url.pathname.replace(/\/+$/, "")}`;
  };
  const base = normalize(value);
  if (!allowed.map(normalize).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  return base;
}

export function createHttpAppKakaoLoginClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]; requireSDKOwnerProof?: boolean;ownerProfile?:"public"},
): AppKakaoLoginClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  if(options.ownerProfile!==undefined && (options.ownerProfile!=="public" || options.requireSDKOwnerProof!==true))throw new Error("카카오 로그인 소유 확인 설정을 확인해 주세요.");
  const proofVersion=options.ownerProfile==="public"?publicOwnerPolicy.session_vault_contract_version:ownerPolicy.session_vault_contract_version;
  const maxEnvelope=options.ownerProfile==="public"?publicOwnerPolicy.algorithm.maximum_envelope_bytes:ownerPolicy.maximum_envelope_bytes;
  return {exchange: async (accessToken, protectionBearer) => {
    if (typeof accessToken !== "string" || !/^[A-Za-z0-9._~+/=-]{20,2048}$/.test(accessToken)
      || !/^[A-Za-z0-9_-]{32,200}$/.test(protectionBearer)) {
      throw new AppAuthenticationError("카카오 로그인 정보를 다시 확인해 주세요.", 400);
    }
    const response = await fetcher(`${base}/api/v1/app/auth/kakao`, {
      method:"POST", cache:"no-store",
      headers:{"Content-Type":"application/json",Authorization:`Bearer ${protectionBearer}`},
      body:JSON.stringify({access_token:accessToken,
        ...(options.requireSDKOwnerProof===true ? {native_owner_proof_version:proofVersion} : {})}),
    });
    let payload:unknown = null;
    try {payload=await response.json();} catch { /* reject below */ }
    if (response.status !== 200) throw new AppAuthenticationError("카카오 로그인을 완료하지 못했습니다.",response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).sort().join(",") !== (options.requireSDKOwnerProof===true
        ? "expires_at,native_cleanup_proof,session_token" : "expires_at,session_token")) {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.",502);
    }
    const session=payload as Record<string,unknown>;
    if (typeof session.session_token !== "string" || !/^[A-Za-z0-9_-]{32,200}$/.test(session.session_token)
      || (options.requireSDKOwnerProof===true && (typeof session.native_cleanup_proof!=="string"
        || session.native_cleanup_proof.length===0 || new TextEncoder().encode(session.native_cleanup_proof).length>maxEnvelope))
      || typeof session.expires_at !== "string" || !/^\d{4}-\d{2}-\d{2}T.*Z$/.test(session.expires_at)
      || !Number.isFinite(Date.parse(session.expires_at)) || Date.parse(session.expires_at) <= Date.now()) {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.",502);
    }
    return {session_token:session.session_token,expires_at:session.expires_at,
      ...(options.requireSDKOwnerProof===true ? {native_cleanup_proof:session.native_cleanup_proof as string,native_cleanup_provider:"kakao" as const} : {})};
  }};
}
