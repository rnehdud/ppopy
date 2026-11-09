import privacy from "../../skin_engine/config/beta_privacy.json";
import {clearSessionCredential,GOOGLE_OWNER_SESSION_VAULT_VERSION,KAKAO_OWNER_SESSION_VAULT_VERSION,type SessionVault} from "./appSessionVault";

export type AppAuthenticationSession = {
  session_token: string;
  expires_at: string;
  native_cleanup_proof?: string;
  /** Set by the selected login adapter, never copied from an HTTP payload. */
  native_cleanup_provider?: "google" | "kakao";
};

export class AppAuthenticationError extends Error {
  constructor(message: string, readonly status: number) {
    super(message);
  }
}

export type AppSessionVerification = {sensitive_notice_version: string};

export type AppSessionVerifier = {
  verify(token: string): Promise<AppSessionVerification | void>;
};

export type AppSessionRevoker = {
  revoke(token: string): Promise<void>;
};

function httpsBase(value: string): string {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) {
    throw new Error("앱 API 주소를 확인해 주세요.");
  }
  return `${url.origin}${url.pathname.replace(/\/+$/, "")}`;
}

export function createHttpAppSessionVerifier(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]},
): AppSessionVerifier {
  const base = httpsBase(options.baseUrl.trim());
  if (!options.allowedBaseUrls.map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  return {verify: async token => {
    if (!/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new AppAuthenticationError("로그인 세션을 다시 확인해 주세요.", 401);
    const response = await fetcher(`${base}/api/v1/app/auth/session`, {
      method: "GET",
      cache: "no-store",
      headers: {Authorization: `Bearer ${token}`},
    });
    let payload: unknown = null;
    try { payload = await response.json(); } catch { /* fail below */ }
    if (!response.ok) throw new AppAuthenticationError("로그인 상태를 확인하지 못했습니다.", response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).sort().join(",") !== "active,sensitive_notice_version" || (payload as {active?:unknown}).active !== true) {
      throw new AppAuthenticationError("로그인 상태 응답을 확인하지 못했습니다.", 502);
    }
    const receipt = payload as {sensitive_notice_version: unknown};
    if (receipt.sensitive_notice_version !== privacy.notices.sensitive_information.version) {
      throw new AppAuthenticationError("필수 동의를 다시 확인해 주세요.", 401);
    }
    return {sensitive_notice_version: receipt.sensitive_notice_version};
  }};
}

export function createHttpAppSessionRevoker(
  fetcher: typeof fetch,
  options: {baseUrl: string; allowedBaseUrls: readonly string[]},
): AppSessionRevoker {
  const base = httpsBase(options.baseUrl.trim());
  if (!options.allowedBaseUrls.map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  return {revoke: async token => {
    if (!/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new AppAuthenticationError("로그인 세션을 다시 확인해 주세요.", 401);
    const response = await fetcher(`${base}/api/v1/app/auth/session`, {
      method: "DELETE",
      cache: "no-store",
      headers: {Authorization: `Bearer ${token}`},
    });
    let payload: unknown = null;
    try { payload = await response.json(); } catch { /* fail below */ }
    if (!response.ok) throw new AppAuthenticationError("로그아웃 상태를 확인하지 못했습니다.", response.status);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)
      || Object.keys(payload).length !== 1 || (payload as {revoked?:unknown}).revoked !== true) {
      throw new AppAuthenticationError("로그아웃 응답을 확인하지 못했습니다.", 502);
    }
  }};
}

export async function saveAuthenticatedSession(
  vault: SessionVault,
  session: AppAuthenticationSession,
): Promise<void> {
  if(session.native_cleanup_provider!==undefined && (session.native_cleanup_proof===undefined
    || !["google","kakao"].includes(session.native_cleanup_provider)))throw new Error("로그인 세션 응답을 확인하지 못했습니다.");
  const contracts=vault.authenticationContracts??{plain:"1.0.0-app-draft" as const,google:GOOGLE_OWNER_SESSION_VAULT_VERSION,kakao:KAKAO_OWNER_SESSION_VAULT_VERSION};
  const contractVersion=session.native_cleanup_proof!==undefined
    ? session.native_cleanup_provider==="kakao" ? contracts.kakao : contracts.google
    : contracts.plain;
  await vault.save({
    contract_version: contractVersion,
    session_token: session.session_token,
    expires_at: session.expires_at,
    ...(session.native_cleanup_proof !== undefined ? {native_cleanup_proof:session.native_cleanup_proof} : {}),
  });
  const stored=await vault.load();
  if(!stored || stored.contract_version!==contractVersion || stored.session_token!==session.session_token || Date.parse(stored.expires_at)!==Date.parse(session.expires_at)
    || stored.native_cleanup_proof!==session.native_cleanup_proof)throw new Error("로그인 세션을 보안 저장소에서 확인하지 못했습니다.");
}

export async function restoreAuthenticatedSession(
  vault: SessionVault,
  verifier: AppSessionVerifier,
  onVerified?: (receipt: AppSessionVerification | void) => void,
): Promise<"resumed" | "signed_out" | "retryable_error" | "vault_unavailable" | "session_changed"> {
  let credential;
  try { credential = await vault.load(); } catch { return "vault_unavailable"; }
  if (!credential) return "signed_out";
  try {
    const receipt = await verifier.verify(credential.session_token);
    let current;
    try{current=await vault.load();}catch{return "vault_unavailable";}
    if(!current || current.session_token!==credential.session_token || current.expires_at!==credential.expires_at)return "session_changed";
    onVerified?.(receipt);
    return "resumed";
  } catch (error) {
    if (error instanceof AppAuthenticationError && (error.status === 401 || error.status === 403)) {
      const cleanup=await clearSessionCredential(vault,credential.session_token);
      return cleanup === "cleared" ? "signed_out" : cleanup === "changed" ? "session_changed" : "vault_unavailable";
    }
    return "retryable_error";
  }
}
