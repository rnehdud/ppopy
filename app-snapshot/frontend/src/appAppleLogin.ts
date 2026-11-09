import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";

export type AppAppleLoginClient = {
  challenge(protectionBearer: string): Promise<{nonce: string; expires_at: string}>;
  exchange(idToken: string, nonce: string, protectionBearer: string, authorizationCode?: string): Promise<AppAuthenticationSession>;
};

const bearerPattern = /^[A-Za-z0-9_-]{32,200}$/;
const noncePattern = /^[A-Za-z0-9_-]{32,128}$/;
const jwtPattern = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/;

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

function validExpiry(value: unknown): value is string {
  return typeof value === "string" && /^\d{4}-\d{2}-\d{2}T.*Z$/.test(value)
    && Number.isFinite(Date.parse(value)) && Date.parse(value) > Date.now();
}

export function createHttpAppAppleLoginClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]; captureAuthorizationCode?: true},
): AppAppleLoginClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  return {
    challenge: async protectionBearer => {
      if (!bearerPattern.test(protectionBearer)) throw new AppAuthenticationError("보호 세션을 다시 확인해 주세요.", 401);
      const response = await fetcher(`${base}/api/v1/app/auth/apple/challenge`, {
        method: "POST", cache: "no-store",
        headers: {"Content-Type": "application/json", Authorization: `Bearer ${protectionBearer}`},
        body: "{}",
      });
      let payload: unknown = null;
      try { payload = await response.json(); } catch { /* reject below */ }
      if (response.status !== 201) throw new AppAuthenticationError("Apple 로그인을 준비하지 못했습니다.", response.status);
      if (!payload || typeof payload !== "object" || Array.isArray(payload)
        || Object.keys(payload).sort().join(",") !== "expires_at,nonce") {
        throw new AppAuthenticationError("Apple 로그인 요청을 확인하지 못했습니다.", 502);
      }
      const receipt = payload as Record<string, unknown>;
      if (typeof receipt.nonce !== "string" || !noncePattern.test(receipt.nonce)
        || !validExpiry(receipt.expires_at)) {
        throw new AppAuthenticationError("Apple 로그인 요청을 확인하지 못했습니다.", 502);
      }
      return {nonce: receipt.nonce, expires_at: receipt.expires_at};
    },
    exchange: async (idToken, nonce, protectionBearer, authorizationCode) => {
      if (typeof idToken !== "string" || idToken.length > 8192 || !jwtPattern.test(idToken)
        || !noncePattern.test(nonce) || !bearerPattern.test(protectionBearer)
        || (options.captureAuthorizationCode === true
          ? typeof authorizationCode !== "string" || authorizationCode.length < 16 || authorizationCode.length > 1024
            || /[^A-Za-z0-9._~+/=-]/.test(authorizationCode)
          : authorizationCode !== undefined)) {
        throw new AppAuthenticationError("Apple 로그인 정보를 다시 확인해 주세요.", 400);
      }
      const response = await fetcher(`${base}/api/v1/app/auth/apple`, {
        method: "POST", cache: "no-store", redirect: "error", credentials: "omit",
        headers: {"Content-Type": "application/json", Authorization: `Bearer ${protectionBearer}`},
        body: JSON.stringify({id_token: idToken, nonce,
          ...(options.captureAuthorizationCode === true ? {authorization_code: authorizationCode} : {})}),
      });
      let payload: unknown = null;
      try { payload = await response.json(); } catch { /* reject below */ }
      if (response.status !== 200) throw new AppAuthenticationError("Apple 로그인을 완료하지 못했습니다.", response.status);
      if (!payload || typeof payload !== "object" || Array.isArray(payload)
        || Object.keys(payload).sort().join(",") !== "expires_at,session_token") {
        throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
      }
      const session = payload as Record<string, unknown>;
      if (typeof session.session_token !== "string" || !bearerPattern.test(session.session_token)
        || !validExpiry(session.expires_at)) {
        throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
      }
      return {session_token: session.session_token, expires_at: session.expires_at};
    },
  };
}
