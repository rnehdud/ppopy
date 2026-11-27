import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";

export type AppEmailOtpClient = {
  issue(email: string, protectionBearer: string): Promise<void>;
  verify(email: string, code: string, protectionBearer: string): Promise<AppAuthenticationSession>;
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

function validBearer(value: string): boolean {
  return typeof value === "string" && /^[A-Za-z0-9_-]{32,200}$/.test(value);
}

function validEmail(value: string): boolean {
  return typeof value === "string" && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function createHttpAppEmailOtpClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]},
): AppEmailOtpClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  const send = async (path: string, body: object, bearer: string): Promise<Response> => {
    if (!validBearer(bearer)) throw new AppAuthenticationError("보호 세션을 확인하지 못했습니다.", 401);
    return fetcher(`${base}${path}`, {
      method:"POST", cache:"no-store",
      headers:{"Content-Type":"application/json", Authorization:`Bearer ${bearer}`},
      body:JSON.stringify(body),
    });
  };
  return {
    issue: async (email, bearer) => {
      if (!validEmail(email)) throw new AppAuthenticationError("이메일 주소를 확인해 주세요.", 400);
      const response = await send("/api/v1/app/auth/email/challenge", {email}, bearer);
      let payload:unknown = null;
      try { payload = await response.json(); } catch { /* reject below */ }
      if (response.status !== 202) throw new AppAuthenticationError("인증 코드를 보내지 못했습니다.", response.status);
      if (!payload || typeof payload !== "object" || Array.isArray(payload)
        || Object.keys(payload).join(",") !== "status"
        || (payload as Record<string, unknown>).status !== "sent") {
        throw new AppAuthenticationError("이메일 전송 응답을 확인하지 못했습니다.", 502);
      }
    },
    verify: async (email, code, bearer) => {
      if (!validEmail(email) || typeof code !== "string" || !/^\d{6}$/.test(code)) {
        throw new AppAuthenticationError("인증 코드를 확인해 주세요.", 400);
      }
      const response = await send("/api/v1/app/auth/email/verify", {email, code}, bearer);
      let payload:unknown = null;
      try { payload = await response.json(); } catch { /* reject below */ }
      if (response.status !== 200) throw new AppAuthenticationError("이메일 인증을 완료하지 못했습니다.", response.status);
      if (!payload || typeof payload !== "object" || Array.isArray(payload)
        || Object.keys(payload).sort().join(",") !== "expires_at,session_token") {
        throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
      }
      const session = payload as Record<string, unknown>;
      if (typeof session.session_token !== "string" || !validBearer(session.session_token)
        || typeof session.expires_at !== "string" || !/^\d{4}-\d{2}-\d{2}T.*Z$/.test(session.expires_at)
        || !Number.isFinite(Date.parse(session.expires_at)) || Date.parse(session.expires_at) <= Date.now()) {
        throw new AppAuthenticationError("로그인 세션 응답을 확인하지 못했습니다.", 502);
      }
      return {session_token:session.session_token, expires_at:session.expires_at};
    },
  };
}
