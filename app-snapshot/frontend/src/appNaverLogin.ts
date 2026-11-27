import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";

export type AppNaverLoginClient = {
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

export function createHttpAppNaverLoginClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]},
): AppNaverLoginClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  return {exchange: async (accessToken, protectionBearer) => {
    if (typeof accessToken !== "string" || !/^[A-Za-z0-9._~+/=-]{20,2048}$/.test(accessToken)
      || !/^[A-Za-z0-9_-]{32,200}$/.test(protectionBearer)) {
      throw new AppAuthenticationError("네이버 로그인 정보를 다시 확인해 주세요.", 400);
    }
    const response = await fetcher(`${base}/api/v1/app/auth/naver`, {
      method:"POST", cache:"no-store",
      headers:{"Content-Type":"application/json",Authorization:`Bearer ${protectionBearer}`},
      body:JSON.stringify({access_token:accessToken}),
    });
    let payload:unknown = null;
    try {payload=await response.json();} catch { /* reject below */ }
    if (response.status !== 200) throw new AppAuthenticationError("네이버 로그인을 완료하지 못했습니다.",response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).sort().join(",") !== "expires_at,session_token") {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.",502);
    }
    const session=payload as Record<string,unknown>;
    if (typeof session.session_token !== "string" || !/^[A-Za-z0-9_-]{32,200}$/.test(session.session_token)
      || typeof session.expires_at !== "string" || !/^\d{4}-\d{2}-\d{2}T.*Z$/.test(session.expires_at)
      || !Number.isFinite(Date.parse(session.expires_at)) || Date.parse(session.expires_at) <= Date.now()) {
      throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.",502);
    }
    return {session_token:session.session_token,expires_at:session.expires_at};
  }};
}
