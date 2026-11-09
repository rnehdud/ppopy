import { CareApiError, parseSessionDeletionReceipt, type CareApiClient, type SessionDeletionReceipt } from "./careApi";
import {clearSessionCredential,type SessionVault} from "./appSessionVault";
import { AppAuthenticationError, type AppSessionRevoker } from "./appAuthentication";

export type AppLogoutResult =
  | { state: "logged_out" }
  | { state: "retryable_error" }
  | { state: "server_revoked_local_cleanup_required" }
  | { state: "server_revoked_session_changed" }
  | { state: "vault_unavailable" };

export type AppDeletionResult =
  | { state: "signed_out" }
  | { state: "deleted"; receipt: SessionDeletionReceipt }
  | { state: "deletion_unconfirmed" }
  | { state: "deletion_unconfirmed_session_changed" }
  | { state: "retryable_error" }
  | { state: "server_deleted_local_cleanup_required"; receipt: SessionDeletionReceipt }
  | { state: "server_deleted_session_changed"; receipt: SessionDeletionReceipt }
  | { state: "vault_unavailable" };

export async function logoutAppSession(vault: SessionVault, revoker: AppSessionRevoker): Promise<AppLogoutResult> {
  let credential;
  try { credential = await vault.load(); }
  catch { return {state:"vault_unavailable"}; }
  if (credential) {
    try { await revoker.revoke(credential.session_token); }
    catch (error) {
      if (!(error instanceof AppAuthenticationError && (error.status === 401 || error.status === 403))) {
        return {state:"retryable_error"};
      }
    }
  }
  if(!credential)return {state:"logged_out"};
  const cleanup=await clearSessionCredential(vault,credential.session_token);
  return {state:cleanup === "cleared" ? "logged_out" : cleanup === "changed" ? "server_revoked_session_changed" : "server_revoked_local_cleanup_required"};
}

export async function withdrawAndDeleteAppSession(
  vault: SessionVault,
  client: Pick<CareApiClient, "deleteBetaSession">,
): Promise<AppDeletionResult> {
  let credential;
  try {
    credential = await vault.load();
  } catch {
    return { state: "vault_unavailable" };
  }
  if (!credential) return { state: "signed_out" };

  let receipt: SessionDeletionReceipt;
  try {
    receipt = parseSessionDeletionReceipt(await client.deleteBetaSession(credential.session_token));
  } catch (error) {
    if (error instanceof CareApiError && (error.status === 401 || error.status === 403)) {
      const cleanup=await clearSessionCredential(vault,credential.session_token);
      return {state:cleanup === "cleared" ? "deletion_unconfirmed" : cleanup === "changed" ? "deletion_unconfirmed_session_changed" : "vault_unavailable"};
    }
    return { state: "retryable_error" };
  }

  const cleanup=await clearSessionCredential(vault,credential.session_token);
  return {state:cleanup === "cleared" ? "deleted" : cleanup === "changed" ? "server_deleted_session_changed" : "server_deleted_local_cleanup_required",receipt};
}
