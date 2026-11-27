import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";
import loginPlan from "../../skin_engine/config/app_login_plan.json";
import googleOwnerPolicy from "../../skin_engine/config/app_google_sdk_owner_local.json";

export type AppGoogleLoginClient = {
  exchange(idToken: string, protectionBearer: string, authorizationCode?: string): Promise<AppAuthenticationSession>;
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

export function createHttpAppGoogleLoginClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]; captureAuthorizationCode?: true},
): AppGoogleLoginClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  return {exchange: async (idToken, protectionBearer, authorizationCode) => {
    if (typeof idToken !== "string" || idToken.length > 8192
      || !/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(idToken)
      || !/^[A-Za-z0-9_-]{32,200}$/.test(protectionBearer)
      || (options.captureAuthorizationCode === true
          ? typeof authorizationCode !== "string" || authorizationCode.length < 16 || authorizationCode.length > 1024
            || /[^A-Za-z0-9._~+/=-]/.test(authorizationCode)
          : authorizationCode !== undefined)) {
      throw new AppAuthenticationError("Google 로그인 정보를 다시 확인해 주세요.", 400);
    }
    const body = JSON.stringify({id_token: idToken,
      ...(options.captureAuthorizationCode === true ? {authorization_code: authorizationCode} : {})});
    if (new TextEncoder().encode(body).length > loginPlan.google_login.max_request_bytes) {
      throw new AppAuthenticationError("Google 로그인 정보를 다시 확인해 주세요.", 400);
    }
    const response = await fetcher(`${base}/api/v1/app/auth/google`, {
      method: "POST",
      cache: "no-store",
      headers: {"Content-Type": "application/json", Authorization: `Bearer ${protectionBearer}`},
      body,
    });
    let payload: unknown = null;
    try { payload = await response.json(); } catch { /* reject below */ }
    if (response.status !== 200) throw new AppAuthenticationError("Google 로그인을 완료하지 못했습니다.", response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).sort().join(",") !== (options.captureAuthorizationCode===true
        ? "expires_at,native_cleanup_proof,session_token" : "expires_at,session_token")) {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
    }
    const session = payload as Record<string, unknown>;
    if (typeof session.session_token !== "string" || !/^[A-Za-z0-9_-]{32,200}$/.test(session.session_token)
      || (options.captureAuthorizationCode===true && (typeof session.native_cleanup_proof!=="string"
        || session.native_cleanup_proof.length===0 || new TextEncoder().encode(session.native_cleanup_proof).length>googleOwnerPolicy.maximum_envelope_bytes))
      || typeof session.expires_at !== "string" || !/^\d{4}-\d{2}-\d{2}T.*Z$/.test(session.expires_at)
      || !Number.isFinite(Date.parse(session.expires_at)) || Date.parse(session.expires_at) <= Date.now()) {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
    }
    return {session_token: session.session_token, expires_at: session.expires_at,
      ...(options.captureAuthorizationCode===true ? {native_cleanup_proof:session.native_cleanup_proof as string} : {})};
  }};
}
