import loginPlan from "../../skin_engine/config/app_login_plan.json";
import {AppAuthenticationError, type AppAuthenticationSession} from "./appAuthentication";

export type AppProtectionAcceptance = {
  age_gate: "over_or_equal_14";
  accepted_notices: {
    service_terms: string;
    general_personal_information: string;
    sensitive_information: string;
    history_storage?: string;
  };
};

export type AppProtectionSessionClient = {
  start(acceptance: AppProtectionAcceptance): Promise<AppAuthenticationSession>;
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

export function createHttpAppProtectionSessionClient(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]},
): AppProtectionSessionClient {
  const base = allowedHttpsBase(options.baseUrl, options.allowedBaseUrls);
  return {start: async acceptance => {
    const notices = acceptance?.accepted_notices;
    if (acceptance?.age_gate !== "over_or_equal_14" || !notices
      || Object.keys(acceptance).length !== 2
      || Object.keys(notices).sort().join(",") !== [...loginPlan.protection_session.required_notice_keys].sort().join(",")
      || !Object.values(notices).every(value => typeof value === "string" && value.length > 0)) {
      throw new AppAuthenticationError("연령과 동의 항목을 다시 확인해 주세요.", 422);
    }
    const response = await fetcher(`${base}/api/v1/app/auth/protection-session`, {
      method: "POST",
      cache: "no-store",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        schema_version: loginPlan.protection_session.schema_version,
        age_gate: acceptance.age_gate,
        accepted_notices: notices,
      }),
    });
    let payload: unknown = null;
    try { payload = await response.json(); } catch { /* reject below */ }
    if (response.status !== 201) throw new AppAuthenticationError("보호 세션을 시작하지 못했습니다.", response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).sort().join(",") !== "expires_at,session_token") {
      throw new AppAuthenticationError("보호 세션 응답을 확인하지 못했습니다.", 502);
    }
    const session = payload as Record<string, unknown>;
    if (typeof session.session_token !== "string" || !/^[A-Za-z0-9_-]{32,200}$/.test(session.session_token)
      || typeof session.expires_at !== "string" || !/^\d{4}-\d{2}-\d{2}T.*Z$/.test(session.expires_at)
      || !Number.isFinite(Date.parse(session.expires_at))) {
      throw new AppAuthenticationError("보호 세션 응답을 확인하지 못했습니다.", 502);
    }
    return {session_token: session.session_token, expires_at: session.expires_at};
  }};
}
