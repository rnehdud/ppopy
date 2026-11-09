import { CareApiError, type BetaSessionHandle, type CareApiClient, type IntakeDraft } from "./careApi";
import {clearSessionCredential, APP_SESSION_VAULT_VERSION, type AppSessionCredential, type SessionVault } from "./appSessionVault";

export type AppSessionResumeResult =
  | { state: "signed_out" }
  | { state: "session_changed" }
  | { state: "resumed"; credential: AppSessionCredential; draft: IntakeDraft | null }
  | { state: "retryable_error"; credential: AppSessionCredential }
  | { state: "vault_unavailable" };

export async function saveStartedAppSession(vault: SessionVault, handle: BetaSessionHandle): Promise<AppSessionCredential> {
  const credential: AppSessionCredential = {
    contract_version: vault.authenticationContracts?.plain??APP_SESSION_VAULT_VERSION,
    session_token: handle.session_token,
    expires_at: handle.expires_at,
  };
  await vault.save(credential);
  const stored = await vault.load();
  if (!stored || stored.session_token!==credential.session_token || Date.parse(stored.expires_at)!==Date.parse(credential.expires_at)) throw new Error("앱 세션을 보안 저장소에서 다시 확인할 수 없습니다.");
  return stored;
}

export async function resumeAppSession(
  vault: SessionVault,
  client: Pick<CareApiClient, "readIntakeDraft">,
): Promise<AppSessionResumeResult> {
  let credential: AppSessionCredential | null;
  try {
    credential = await vault.load();
  } catch {
    return { state: "vault_unavailable" };
  }
  if (!credential) return { state: "signed_out" };
  if (!client.readIntakeDraft) return { state: "retryable_error", credential };

  try {
    const { draft } = await client.readIntakeDraft(credential.session_token);
    let current;
    try{current=await vault.load();}catch{return {state:"vault_unavailable"};}
    if(!current || current.session_token!==credential.session_token || current.expires_at!==credential.expires_at)return {state:"session_changed"};
    return { state: "resumed", credential, draft };
  } catch (error) {
    if (error instanceof CareApiError && (error.status === 401 || error.status === 403)) {
      const cleanup=await clearSessionCredential(vault,credential.session_token);
      return {state:cleanup === "cleared" ? "signed_out" : cleanup === "changed" ? "session_changed" : "vault_unavailable"};
    }
    let current;
    try{current=await vault.load();}catch{return {state:"vault_unavailable"};}
    if(!current || current.session_token!==credential.session_token || current.expires_at!==credential.expires_at)return {state:"session_changed"};
    return { state: "retryable_error", credential };
  }
}
