import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import type {SubscriptionDisplayState} from "./subscriptionPresentation";

export type MiraySubscriptionStatus = {
  serverVerified: boolean;
  state: SubscriptionDisplayState;
};

export type MiraySubscriptionStatusStore = {
  read(options?:MemberStatusReadOptions): Promise<MiraySubscriptionStatus>;
};

export type MiraySubscriptionStatusHttpOptions = {
  baseUrl?: string;
  allowedBaseUrls?: readonly string[];
  loadSessionToken: () => Promise<string | null>;
  /** Explicit UI lifecycle notification; never clears credentials or retries HTTP. */
  onSessionChanged?: () => void;
};

const displayStates = new Set<SubscriptionDisplayState>([
  "FREE", "TRIALING", "ACTIVE", "CANCEL_AT_PERIOD_END", "GRACE_PERIOD",
  "VERIFICATION_PENDING", "ACCOUNT_HOLD", "EXPIRED", "REVOKED",
]);

const object = (value: unknown): value is Record<string, unknown> => Boolean(value) && typeof value === "object" && !Array.isArray(value);

export function parseMiraySubscriptionStatus(value: unknown): MiraySubscriptionStatus {
  if (!object(value) || Object.keys(value).sort().join("|") !== "server_verified|state" || typeof value.server_verified !== "boolean" || typeof value.state !== "string" || !displayStates.has(value.state as SubscriptionDisplayState)) {
    throw new Error("구독 상태 응답 형식을 확인하지 못했습니다.");
  }
  const state = value.state as SubscriptionDisplayState;
  if (state !== "VERIFICATION_PENDING" && value.server_verified !== true) {
    throw new Error("구독 상태 응답 형식을 확인하지 못했습니다.");
  }
  if (state === "VERIFICATION_PENDING" && value.server_verified !== false) {
    throw new Error("구독 상태 응답 형식을 확인하지 못했습니다.");
  }
  return {serverVerified:value.server_verified, state};
}

function httpsBase(value: string): string {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/, "")}`;
}

export function createHttpMiraySubscriptionStatusStore(fetcher: typeof fetch, options: MiraySubscriptionStatusHttpOptions): MiraySubscriptionStatusStore {
  const bound=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  const requested = options.baseUrl?.trim() || "";
  const base = requested ? httpsBase(requested) : "";
  if (base && !(options.allowedBaseUrls || []).map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  return {read: async consumer => {
    const {gate,load,wait,fetch}=memberStatusReadScope(bound,consumer);
    const token = await wait(load);
    if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response = await wait(()=>fetch(fetcher)(`${base}/api/v1/app/subscription-status`, {
      method:"GET", cache:"no-store", redirect:"error", credentials:"omit", headers:{Authorization:`Bearer ${token}`},signal:consumer?.signal,
    }));
    await wait(()=>assertCurrentMemberResponseSession(load, token, options.onSessionChanged));
    let payload: unknown = null;
    try { payload = await wait(()=>response.json()); } catch { gate();/* fail below */ }
    await wait(()=>assertCurrentMemberResponseSession(load, token, options.onSessionChanged));
    if (!response.ok) throw new Error("구독 상태를 확인하지 못했습니다.");
    return parseMiraySubscriptionStatus(payload);
  }};
}
